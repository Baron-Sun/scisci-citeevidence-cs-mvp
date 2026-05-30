from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import pyarrow.parquet as pq
import yaml

DEFAULT_OBJECT_REGISTRY_PATH = Path("configs/object_registry_seed.yaml")
DEFAULT_OBJECT_MENTIONS_SAMPLE_PATH = Path("data/processed/object_mentions_sample.parquet")
DEFAULT_OBJECT_MATCHING_SAMPLE_REPORT = Path("reports/object_matching_sample_report.md")

OBJECT_TYPES = {
    "method",
    "model",
    "dataset_or_database",
    "software_or_tool",
    "benchmark_or_protocol",
    "metric",
    "task",
    "theory_or_concept",
    "claim_or_finding",
}
MATCHED_IN_COLUMNS = ["sentence_text", "context_window_s3", "resolved_cited_title"]
CONTEXT_READ_COLUMNS = [
    "context_id",
    "source_context_id",
    "citing_paper_id",
    "resolved_cited_acl_id",
    "resolved_cited_title",
    "normalized_section",
    "raw_section_name",
    "sentence_text",
    "context_window_s3",
]
OBJECT_MENTION_COLUMNS = [
    "context_id",
    "source_context_id",
    "citing_paper_id",
    "resolved_cited_acl_id",
    "resolved_cited_title",
    "normalized_section",
    "raw_section_name",
    "object_id",
    "canonical_name",
    "object_type",
    "surface_form",
    "match_type",
    "char_start",
    "char_end",
    "confidence",
    "matched_in",
    "provenance",
]
COMMON_TERM_SURFACES = {
    "accuracy",
    "classification accuracy",
    "f1",
    "f1 score",
    "f-score",
    "f measure",
    "f-measure",
    "perplexity",
    "ppl",
    "transformer",
    "transformers",
}
WORD_CHAR_RE = re.compile(r"[a-z0-9+#]")
ALNUM_RE = re.compile(r"[A-Za-z0-9]")


@dataclass(frozen=True)
class ObjectRegistryEntry:
    object_id: str
    canonical_name: str
    aliases: tuple[str, ...]
    negative_aliases: tuple[str, ...]
    object_type: str
    linked_paper_title: str | None
    linked_acl_id: str | None
    linked_doi: str | None
    source: str
    notes: str
    allow_short_alias: bool = False


@dataclass(frozen=True)
class AliasSpec:
    entry: ObjectRegistryEntry
    alias: str
    normalized_alias: str
    pattern: re.Pattern[str]
    first_token: str
    alias_length: int
    is_short_alias: bool
    is_common_term: bool
    is_negative: bool = False


def match_objects_in_contexts(
    *,
    contexts_path: str | Path,
    registry_path: str | Path = DEFAULT_OBJECT_REGISTRY_PATH,
    out_path: str | Path = DEFAULT_OBJECT_MENTIONS_SAMPLE_PATH,
    report_path: str | Path = DEFAULT_OBJECT_MATCHING_SAMPLE_REPORT,
    limit: int = 50_000,
) -> dict[str, Any]:
    """Match seed NLP object mentions in analysis-ready citation contexts."""
    if limit < 1:
        raise ValueError("limit must be positive")
    contexts_input = Path(contexts_path)
    registry_input = Path(registry_path)
    if not contexts_input.exists():
        raise FileNotFoundError(f"Contexts file does not exist: {contexts_input}")
    if not registry_input.exists():
        raise FileNotFoundError(f"Object registry file does not exist: {registry_input}")

    registry = load_object_registry(registry_input)
    contexts = _read_contexts(contexts_input, limit=limit)
    mentions, diagnostics = match_object_mentions(contexts, registry)

    output = Path(out_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    mentions.to_parquet(output, index=False)

    metrics = build_object_matching_metrics(
        contexts=contexts,
        mentions=mentions,
        diagnostics=diagnostics,
        registry=registry,
        limit=limit,
    )
    report = build_object_matching_report(
        metrics=metrics,
        mentions=mentions,
        contexts_path=contexts_input,
        registry_path=registry_input,
        out_path=output,
    )
    report_output = Path(report_path)
    report_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.write_text(report, encoding="utf-8")
    return metrics


def load_object_registry(path: str | Path) -> list[ObjectRegistryEntry]:
    """Load and validate object registry seed YAML."""
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    raw_objects = data.get("objects", data if isinstance(data, list) else [])
    if not isinstance(raw_objects, list):
        raise ValueError("Object registry must contain an 'objects' list")

    entries = []
    seen_ids = set()
    for index, raw in enumerate(raw_objects):
        if not isinstance(raw, dict):
            raise ValueError(f"Registry entry {index} must be a mapping")
        entry = _registry_entry_from_mapping(raw, index=index)
        if entry.object_id in seen_ids:
            raise ValueError(f"Duplicate object_id in registry: {entry.object_id}")
        seen_ids.add(entry.object_id)
        entries.append(entry)
    if not entries:
        raise ValueError("Object registry is empty")
    return entries


def match_object_mentions(
    contexts: pd.DataFrame,
    registry: list[ObjectRegistryEntry],
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Return object mention rows and matcher diagnostics."""
    frame = _ensure_columns(contexts.copy(), CONTEXT_READ_COLUMNS)
    positive_specs, negative_specs = _build_alias_specs(registry)
    mentions: list[dict[str, Any]] = []
    blocked_examples: list[dict[str, Any]] = []
    negative_blocked_count = 0

    for row in frame.to_dict(orient="records"):
        for matched_in in MATCHED_IN_COLUMNS:
            text = _clean_text(row.get(matched_in))
            if not text:
                continue
            normalized_text, char_map = _normalize_text_with_map(text)
            raw_matches = []
            negative_cache: dict[str, list[tuple[int, int, str]]] = {}
            for spec in positive_specs:
                if spec.first_token and spec.first_token not in normalized_text:
                    continue
                for match in spec.pattern.finditer(normalized_text):
                    if not _span_has_word_boundary(normalized_text, match.start(), match.end()):
                        continue
                    blocked_by = _blocking_negative_alias(
                        spec,
                        match.start(),
                        match.end(),
                        normalized_text,
                        negative_specs,
                        negative_cache,
                    )
                    if blocked_by is not None:
                        negative_blocked_count += 1
                        if len(blocked_examples) < 50:
                            blocked_examples.append(
                                _blocked_example(
                                    row,
                                    spec,
                                    matched_in,
                                    text,
                                    match,
                                    char_map,
                                    blocked_by=blocked_by,
                                )
                            )
                        continue
                    raw_matches.append(
                        _candidate_match(row, spec, matched_in, text, match, char_map)
                    )
            mentions.extend(_dedupe_overlapping_matches(raw_matches))

    mentions_df = pd.DataFrame(mentions, columns=OBJECT_MENTION_COLUMNS)
    diagnostics = {
        "negative_alias_blocked_count": negative_blocked_count,
        "negative_alias_blocked_examples": pd.DataFrame(blocked_examples),
    }
    return mentions_df, diagnostics


def build_object_matching_metrics(
    *,
    contexts: pd.DataFrame,
    mentions: pd.DataFrame,
    diagnostics: dict[str, Any],
    registry: list[ObjectRegistryEntry],
    limit: int,
) -> dict[str, Any]:
    """Build metrics for the object matching sample report."""
    contexts_with_mentions = (
        int(mentions["context_id"].nunique(dropna=True)) if not mentions.empty else 0
    )
    return {
        "input_context_rows_processed": int(len(contexts)),
        "limit": limit,
        "registry_objects": len(registry),
        "contexts_with_at_least_one_object_mention": contexts_with_mentions,
        "total_object_mentions": int(len(mentions)),
        "object_mentions_by_object_type": _value_counts(mentions, ["object_type"], "mentions"),
        "top_50_matched_objects": _value_counts(
            mentions,
            ["object_id", "canonical_name", "object_type"],
            "mentions",
            limit=50,
        ),
        "top_50_surface_forms": _value_counts(
            mentions,
            ["surface_form", "canonical_name", "object_type"],
            "mentions",
            limit=50,
        ),
        "matches_by_normalized_section": _value_counts(
            mentions,
            ["normalized_section"],
            "mentions",
        ),
        "matches_by_matched_in": _value_counts(mentions, ["matched_in"], "mentions"),
        "examples_per_object_type": _examples_per_group(mentions, "object_type", 5),
        "potential_short_alias_false_positives": _short_alias_examples(mentions, 20),
        "potential_inside_longer_word_false_positives": pd.DataFrame(
            columns=OBJECT_MENTION_COLUMNS
        ),
        "potential_common_term_false_positives": _common_term_examples(mentions, 20),
        "negative_alias_blocked_count": int(diagnostics["negative_alias_blocked_count"]),
        "negative_alias_blocked_examples": diagnostics[
            "negative_alias_blocked_examples"
        ].head(20),
    }


def build_object_matching_report(
    *,
    metrics: dict[str, Any],
    mentions: pd.DataFrame,
    contexts_path: Path,
    registry_path: Path,
    out_path: Path,
) -> str:
    """Build a markdown report for Task 8A object mention matching."""
    core = pd.DataFrame(
        [
            {
                "metric": "input context rows processed",
                "value": metrics["input_context_rows_processed"],
            },
            {"metric": "configured limit", "value": metrics["limit"]},
            {"metric": "registry objects", "value": metrics["registry_objects"]},
            {
                "metric": "contexts with at least one object mention",
                "value": metrics["contexts_with_at_least_one_object_mention"],
            },
            {"metric": "total object mentions", "value": metrics["total_object_mentions"]},
            {
                "metric": "negative alias blocked count",
                "value": metrics["negative_alias_blocked_count"],
            },
        ]
    )
    sections = [
        "# Object Matching Sample Report",
        "",
        "## Inputs",
        f"- Contexts: `{contexts_path}`",
        f"- Registry: `{registry_path}`",
        "",
        "## Outputs",
        f"- Object mentions sample: `{out_path}`",
        "",
        "## Core Metrics",
        _table(core),
        "",
        "## Object Mentions By Object Type",
        _table(metrics["object_mentions_by_object_type"]),
        "",
        "## Top 50 Matched Objects",
        _table(metrics["top_50_matched_objects"]),
        "",
        "## Top 50 Surface Forms",
        _table(metrics["top_50_surface_forms"]),
        "",
        "## Matches By Normalized Section",
        _table(metrics["matches_by_normalized_section"]),
        "",
        "## Matches By Matched In",
        _table(metrics["matches_by_matched_in"]),
        "",
        "## Examples Per Object Type",
        _table(metrics["examples_per_object_type"]),
        "",
        "## Potential False Positives: Short Aliases",
        _table(metrics["potential_short_alias_false_positives"]),
        "",
        "## Potential False Positives: Inside Longer Words",
        _table(metrics["potential_inside_longer_word_false_positives"]),
        "",
        "## Potential False Positives: Very Common Terms",
        _table(metrics["potential_common_term_false_positives"]),
        "",
        "## Negative Alias Blocked Examples",
        _table(metrics["negative_alias_blocked_examples"]),
        "",
        "## Recommendations",
        _registry_recommendation(metrics, mentions),
        "",
    ]
    return "\n".join(sections)


def _registry_entry_from_mapping(raw: dict[str, Any], *, index: int) -> ObjectRegistryEntry:
    required = [
        "object_id",
        "canonical_name",
        "aliases",
        "negative_aliases",
        "object_type",
        "source",
        "notes",
    ]
    missing = [field for field in required if field not in raw]
    if missing:
        raise ValueError(f"Registry entry {index} missing fields: {missing}")
    object_type = _clean_text(raw["object_type"])
    if object_type not in OBJECT_TYPES:
        raise ValueError(f"Registry entry {index} has unknown object_type: {object_type}")
    aliases = _as_text_tuple(raw.get("aliases"))
    if not aliases:
        raise ValueError(f"Registry entry {index} must have at least one alias")
    return ObjectRegistryEntry(
        object_id=_clean_text(raw["object_id"]),
        canonical_name=_clean_text(raw["canonical_name"]),
        aliases=aliases,
        negative_aliases=_as_text_tuple(raw.get("negative_aliases")),
        object_type=object_type,
        linked_paper_title=_clean_text_or_none(raw.get("linked_paper_title")),
        linked_acl_id=_clean_text_or_none(raw.get("linked_acl_id")),
        linked_doi=_clean_text_or_none(raw.get("linked_doi")),
        source=_clean_text(raw["source"]),
        notes=_clean_text(raw["notes"]),
        allow_short_alias=bool(raw.get("allow_short_alias", False)),
    )


def _build_alias_specs(
    registry: list[ObjectRegistryEntry],
) -> tuple[list[AliasSpec], dict[str, list[AliasSpec]]]:
    positive = []
    negative: dict[str, list[AliasSpec]] = {}
    for entry in registry:
        aliases = _unique_preserve_order([entry.canonical_name, *entry.aliases])
        for alias in aliases:
            spec = _alias_spec(entry, alias, is_negative=False)
            if spec is None:
                continue
            positive.append(spec)
        negative[entry.object_id] = []
        for alias in entry.negative_aliases:
            spec = _alias_spec(entry, alias, is_negative=True)
            if spec is not None:
                negative[entry.object_id].append(spec)
    positive.sort(key=lambda spec: spec.alias_length, reverse=True)
    return positive, negative


def _alias_spec(
    entry: ObjectRegistryEntry,
    alias: str,
    *,
    is_negative: bool,
) -> AliasSpec | None:
    normalized_alias, _ = _normalize_text_with_map(alias)
    normalized_alias = re.sub(r"\s+", " ", normalized_alias).strip()
    if not normalized_alias:
        return None
    alias_length = len(ALNUM_RE.findall(alias))
    is_short = alias_length < 3
    if is_short and not (entry.allow_short_alias or is_negative):
        return None
    pattern = _alias_pattern(normalized_alias)
    first_token = normalized_alias.split(" ", 1)[0]
    return AliasSpec(
        entry=entry,
        alias=alias,
        normalized_alias=normalized_alias,
        pattern=pattern,
        first_token=first_token,
        alias_length=len(normalized_alias),
        is_short_alias=is_short,
        is_common_term=normalized_alias in COMMON_TERM_SURFACES,
        is_negative=is_negative,
    )


def _alias_pattern(normalized_alias: str) -> re.Pattern[str]:
    pieces = [re.escape(piece) for piece in normalized_alias.split(" ") if piece]
    pattern = r"\s+".join(pieces)
    return re.compile(rf"(?<![a-z0-9+#]){pattern}(?![a-z0-9+#])")


def _read_contexts(path: Path, *, limit: int) -> pd.DataFrame:
    parquet_file = pq.ParquetFile(path)
    available_columns = set(parquet_file.schema_arrow.names)
    columns = [column for column in CONTEXT_READ_COLUMNS if column in available_columns]
    batches = []
    remaining = limit
    for batch in parquet_file.iter_batches(batch_size=min(50_000, limit), columns=columns):
        take = min(remaining, batch.num_rows)
        batches.append(batch.slice(0, take).to_pandas())
        remaining -= take
        if remaining <= 0:
            break
    if not batches:
        return pd.DataFrame(columns=CONTEXT_READ_COLUMNS)
    return _ensure_columns(pd.concat(batches, ignore_index=True), CONTEXT_READ_COLUMNS)


def _candidate_match(
    row: dict[str, Any],
    spec: AliasSpec,
    matched_in: str,
    text: str,
    match: re.Match[str],
    char_map: list[int],
) -> dict[str, Any]:
    char_start = char_map[match.start()]
    char_end = char_map[match.end() - 1] + 1
    surface = text[char_start:char_end]
    match_type = _match_type(surface, spec.alias)
    confidence = _confidence(match_type, spec)
    return {
        "context_id": row.get("context_id"),
        "source_context_id": row.get("source_context_id"),
        "citing_paper_id": row.get("citing_paper_id"),
        "resolved_cited_acl_id": row.get("resolved_cited_acl_id"),
        "resolved_cited_title": row.get("resolved_cited_title"),
        "normalized_section": row.get("normalized_section"),
        "raw_section_name": row.get("raw_section_name"),
        "object_id": spec.entry.object_id,
        "canonical_name": spec.entry.canonical_name,
        "object_type": spec.entry.object_type,
        "surface_form": surface,
        "match_type": match_type,
        "char_start": char_start,
        "char_end": char_end,
        "confidence": confidence,
        "matched_in": matched_in,
        "provenance": f"registry_seed:{spec.entry.object_id};alias={spec.alias}",
        "_span": (char_start, char_end),
        "_alias_length": spec.alias_length,
    }


def _blocked_example(
    row: dict[str, Any],
    spec: AliasSpec,
    matched_in: str,
    text: str,
    match: re.Match[str],
    char_map: list[int],
    *,
    blocked_by: str,
) -> dict[str, Any]:
    char_start = char_map[match.start()]
    char_end = char_map[match.end() - 1] + 1
    return {
        "context_id": row.get("context_id"),
        "object_id": spec.entry.object_id,
        "canonical_name": spec.entry.canonical_name,
        "alias": spec.alias,
        "blocked_by_negative_alias": blocked_by,
        "surface_form": text[char_start:char_end],
        "matched_in": matched_in,
        "char_start": char_start,
        "char_end": char_end,
    }


def _blocking_negative_alias(
    spec: AliasSpec,
    start: int,
    end: int,
    normalized_text: str,
    negative_specs: dict[str, list[AliasSpec]],
    negative_cache: dict[str, list[tuple[int, int, str]]],
) -> str | None:
    object_id = spec.entry.object_id
    if object_id not in negative_cache:
        spans = []
        for negative_spec in negative_specs.get(object_id, []):
            if negative_spec.first_token and negative_spec.first_token not in normalized_text:
                continue
            for match in negative_spec.pattern.finditer(normalized_text):
                spans.append((match.start(), match.end(), negative_spec.alias))
        negative_cache[object_id] = spans
    for neg_start, neg_end, alias in negative_cache[object_id]:
        if _overlaps(start, end, neg_start, neg_end):
            return alias
    return None


def _dedupe_overlapping_matches(matches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for match in sorted(
        matches,
        key=lambda item: (
            -int(item["_alias_length"]),
            -float(item["confidence"]),
            int(item["char_start"]),
            str(item["object_id"]),
        ),
    ):
        start, end = match["_span"]
        overlaps_existing = any(
            _overlaps(start, end, existing["_span"][0], existing["_span"][1])
            for existing in selected
        )
        if overlaps_existing:
            continue
        selected.append(match)
    output = []
    for match in sorted(selected, key=lambda item: (item["matched_in"], item["char_start"])):
        clean = {key: value for key, value in match.items() if not key.startswith("_")}
        output.append(clean)
    return output


def _match_type(surface: str, alias: str) -> str:
    if surface == alias:
        return "exact_alias"
    if surface.lower() == alias.lower():
        return "case_insensitive_alias"
    return "punctuation_normalized_alias"


def _confidence(match_type: str, spec: AliasSpec) -> float:
    if spec.is_short_alias or spec.is_common_term:
        return 0.70
    if match_type == "punctuation_normalized_alias":
        return 0.90
    return 0.95


def _span_has_word_boundary(normalized_text: str, start: int, end: int) -> bool:
    before = normalized_text[start - 1] if start > 0 else " "
    after = normalized_text[end] if end < len(normalized_text) else " "
    return not WORD_CHAR_RE.fullmatch(before) and not WORD_CHAR_RE.fullmatch(after)


def _normalize_text_with_map(text: Any) -> tuple[str, list[int]]:
    raw = "" if text is None or pd.isna(text) else str(text)
    chars = []
    char_map = []
    for index, char in enumerate(raw):
        lowered = char.lower()
        if lowered.isalnum() or lowered in {"+", "#"}:
            chars.append(lowered)
        else:
            chars.append(" ")
        char_map.append(index)
    if not chars:
        return "", []
    return "".join(chars), char_map


def _short_alias_examples(mentions: pd.DataFrame, limit: int) -> pd.DataFrame:
    if mentions.empty:
        return pd.DataFrame(columns=OBJECT_MENTION_COLUMNS)
    short = mentions.loc[
        mentions["surface_form"].map(lambda value: len(ALNUM_RE.findall(str(value))) < 3)
    ]
    return _sample_mentions(short, limit)


def _common_term_examples(mentions: pd.DataFrame, limit: int) -> pd.DataFrame:
    if mentions.empty:
        return pd.DataFrame(columns=OBJECT_MENTION_COLUMNS)
    common = mentions.loc[
        mentions["surface_form"].map(_normalized_surface).isin(COMMON_TERM_SURFACES)
    ]
    return _sample_mentions(common, limit)


def _examples_per_group(mentions: pd.DataFrame, column: str, per_group: int) -> pd.DataFrame:
    if mentions.empty or column not in mentions:
        return pd.DataFrame(columns=["example_group", *OBJECT_MENTION_COLUMNS])
    samples = []
    for group_name, group in mentions.groupby(column, dropna=False):
        sample = _sample_mentions(group, per_group)
        sample.insert(0, "example_group", str(group_name))
        samples.append(sample)
    if not samples:
        return pd.DataFrame(columns=["example_group", *OBJECT_MENTION_COLUMNS])
    return pd.concat(samples, ignore_index=True)


def _sample_mentions(mentions: pd.DataFrame, limit: int) -> pd.DataFrame:
    if mentions.empty:
        return pd.DataFrame(columns=OBJECT_MENTION_COLUMNS)
    sample = mentions[OBJECT_MENTION_COLUMNS].head(limit).copy()
    for column in ("resolved_cited_title", "surface_form"):
        sample[column] = sample[column].map(lambda value: _truncate(value, 140))
    return sample


def _value_counts(
    df: pd.DataFrame,
    columns: list[str],
    count_name: str,
    *,
    limit: int | None = None,
) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=[*columns, count_name])
    filled = df.copy()
    for column in columns:
        if column not in filled:
            filled[column] = "unavailable"
        filled[column] = filled[column].fillna("unavailable").astype(str)
    counts = (
        filled.groupby(columns, dropna=False)
        .size()
        .reset_index(name=count_name)
        .sort_values([count_name, *columns], ascending=[False, *([True] * len(columns))])
    )
    return counts.head(limit) if limit is not None else counts


def _registry_recommendation(metrics: dict[str, Any], mentions: pd.DataFrame) -> str:
    if mentions.empty:
        return (
            "No seed objects matched in the sample. Expand aliases or inspect the input sample "
            "before running full matching."
        )
    common_count = len(metrics["potential_common_term_false_positives"])
    short_count = len(metrics["potential_short_alias_false_positives"])
    if common_count or short_count:
        return (
            "Review short aliases and common metric/model terms before a full run. "
            "The sample output is suitable for registry refinement, but noisy terms such as "
            "accuracy, F1, perplexity, Transformer, or PTB should be checked manually."
        )
    return (
        "The sample matcher produced bounded, provenance-rich object mentions. Inspect the "
        "examples per object type, then proceed to full matching if false positives look low."
    )


def _normalized_surface(value: Any) -> str:
    normalized, _ = _normalize_text_with_map(value)
    return re.sub(r"\s+", " ", normalized).strip()


def _unique_preserve_order(values: list[str]) -> list[str]:
    seen = set()
    unique = []
    for value in values:
        text = _clean_text(value)
        key = text.lower()
        if text and key not in seen:
            unique.append(text)
            seen.add(key)
    return unique


def _as_text_tuple(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, list):
        return tuple(_clean_text(item) for item in value if _clean_text(item))
    raise ValueError(f"Expected string or list of strings, got {type(value).__name__}")


def _clean_text(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


def _clean_text_or_none(value: Any) -> str | None:
    text = _clean_text(value)
    return text or None


def _ensure_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        if column not in df.columns:
            df[column] = None
    return df


def _overlaps(start: int, end: int, other_start: int, other_end: int) -> bool:
    return start < other_end and other_start < end


def _truncate(value: Any, max_chars: int) -> str:
    if value is None or pd.isna(value):
        return ""
    text = str(value).replace("\n", " ")
    if len(text) <= max_chars:
        return text
    return f"{text[: max_chars - 3]}..."


def _table(df: pd.DataFrame) -> str:
    if df.empty:
        return "No records available."
    columns = list(df.columns)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in df.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(_markdown_cell(value) for value in row) + " |")
    return "\n".join(lines)


def _markdown_cell(value: Any) -> str:
    if value is None or pd.isna(value):
        return "unavailable"
    return str(value).replace("|", "\\|")
