from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import pyarrow.parquet as pq
import yaml

from citeevidence.object_policy import (
    apply_final_policy_to_mentions,
    build_object_graph_candidates,
)

DEFAULT_OBJECT_REGISTRY_PATH = Path("configs/object_registry_seed.yaml")
DEFAULT_OBJECT_MENTIONS_PATH = Path("data/processed/object_mentions.parquet")
DEFAULT_CITED_TITLE_OBJECT_PROFILES_PATH = Path(
    "data/processed/cited_title_object_profiles.parquet"
)
DEFAULT_OBJECT_GRAPH_CANDIDATES_PATH = Path(
    "data/processed/object_graph_candidate_mentions.parquet"
)
DEFAULT_STRICT_OBJECT_GRAPH_CANDIDATES_PATH = Path(
    "data/processed/object_graph_candidate_mentions_strict.parquet"
)
DEFAULT_BROAD_OBJECT_GRAPH_CANDIDATES_PATH = Path(
    "data/processed/object_graph_candidate_mentions_broad.parquet"
)
DEFAULT_OBJECT_MATCHING_REPORT = Path("reports/object_matching_report.md")
DEFAULT_OBJECT_MENTIONS_SAMPLE_PATH = Path(
    "data/processed/object_mentions_sample_refined.parquet"
)
DEFAULT_CITED_TITLE_OBJECT_PROFILES_SAMPLE_PATH = Path(
    "data/processed/cited_title_object_profiles_sample.parquet"
)
DEFAULT_OBJECT_MENTIONS_REVIEW_SAMPLE_PATH = Path(
    "data/processed/object_mentions_review_sample.csv"
)
DEFAULT_OBJECT_MATCHING_SAMPLE_REPORT = Path("reports/object_matching_sample_refined_report.md")

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
OBJECT_CATEGORIES = {
    "named_object",
    "generic_metric",
    "generic_architecture",
    "ambiguous_short_alias",
}
MATCHED_IN_COLUMNS = ["sentence_text", "context_window_s3", "resolved_cited_title"]
CONTEXT_MATCHED_IN_COLUMNS = ["sentence_text", "context_window_s3"]
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
    "object_category",
    "surface_form",
    "normalized_surface",
    "match_type",
    "char_start",
    "char_end",
    "confidence",
    "matched_in",
    "match_policy",
    "allow_in_object_graph",
    "provenance",
]
OBJECT_REVIEW_SAMPLE_COLUMNS = [
    "review_bucket",
    "context_id",
    "source_context_id",
    "citing_paper_id",
    "resolved_cited_acl_id",
    "resolved_cited_title",
    "normalized_section",
    "raw_section_name",
    "sentence_text",
    "context_window_s3",
    "object_id",
    "canonical_name",
    "object_type",
    "object_category",
    "surface_form",
    "matched_in",
    "confidence",
    "match_policy",
    "allow_in_object_graph",
    "reviewer_correct",
    "reviewer_notes",
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
    object_category: str = "named_object"
    allow_in_object_graph: bool = True
    require_case_sensitive: bool = False
    require_context_cue: tuple[str, ...] = ()
    confidence_override: float | None = None


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
    cited_title_profiles_path: str | Path = DEFAULT_CITED_TITLE_OBJECT_PROFILES_SAMPLE_PATH,
    object_graph_candidates_path: str | Path | None = None,
    strict_object_graph_candidates_path: str | Path | None = None,
    broad_object_graph_candidates_path: str | Path | None = None,
    review_sample_path: str | Path = DEFAULT_OBJECT_MENTIONS_REVIEW_SAMPLE_PATH,
    report_path: str | Path = DEFAULT_OBJECT_MATCHING_SAMPLE_REPORT,
    limit: int | None = 50_000,
) -> dict[str, Any]:
    """Match seed NLP object mentions in analysis-ready citation contexts."""
    if limit is not None and limit < 1:
        raise ValueError("limit must be positive")
    contexts_input = Path(contexts_path)
    registry_input = Path(registry_path)
    if not contexts_input.exists():
        raise FileNotFoundError(f"Contexts file does not exist: {contexts_input}")
    if not registry_input.exists():
        raise FileNotFoundError(f"Object registry file does not exist: {registry_input}")

    registry = load_object_registry(registry_input)
    contexts = _read_contexts(contexts_input, limit=limit)
    mentions, cited_title_profiles, diagnostics = match_object_mentions(contexts, registry)
    mentions_with_context = _attach_context_text_for_policy(mentions, contexts)
    cited_title_profiles_with_context = _attach_context_text_for_policy(
        cited_title_profiles,
        contexts,
    )
    final_mentions = apply_final_policy_to_mentions(
        mentions=mentions_with_context,
        llm_review=pd.DataFrame(),
        source_table="object_mentions",
    )
    final_title_profiles = apply_final_policy_to_mentions(
        mentions=cited_title_profiles_with_context,
        llm_review=pd.DataFrame(),
        source_table="cited_title_object_profiles",
        force_title_profile_policy=True,
    )
    graph_candidates = build_object_graph_candidates(final_mentions)
    strict_graph_candidates = graph_candidates.loc[
        graph_candidates["graph_candidate_level"].eq("strict")
    ].reset_index(drop=True)
    broad_graph_candidates = graph_candidates.loc[
        graph_candidates["graph_candidate_level"].eq("broad")
    ].reset_index(drop=True)

    output = Path(out_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    final_mentions.to_parquet(output, index=False)

    cited_title_output = Path(cited_title_profiles_path)
    cited_title_output.parent.mkdir(parents=True, exist_ok=True)
    final_title_profiles.to_parquet(cited_title_output, index=False)

    graph_output = Path(object_graph_candidates_path) if object_graph_candidates_path else None
    strict_output = (
        Path(strict_object_graph_candidates_path) if strict_object_graph_candidates_path else None
    )
    broad_output = (
        Path(broad_object_graph_candidates_path) if broad_object_graph_candidates_path else None
    )
    if graph_output is not None:
        graph_output.parent.mkdir(parents=True, exist_ok=True)
        graph_candidates.to_parquet(graph_output, index=False)
    if strict_output is not None:
        strict_output.parent.mkdir(parents=True, exist_ok=True)
        strict_graph_candidates.to_parquet(strict_output, index=False)
    if broad_output is not None:
        broad_output.parent.mkdir(parents=True, exist_ok=True)
        broad_graph_candidates.to_parquet(broad_output, index=False)

    review_sample = build_object_mentions_review_sample(
        contexts=contexts,
        mentions=final_mentions,
        cited_title_profiles=final_title_profiles,
    )
    review_sample_output = Path(review_sample_path)
    review_sample_output.parent.mkdir(parents=True, exist_ok=True)
    review_sample.to_csv(review_sample_output, index=False)

    metrics = build_object_matching_metrics(
        contexts=contexts,
        mentions=final_mentions,
        cited_title_profiles=final_title_profiles,
        graph_candidates=graph_candidates,
        strict_graph_candidates=strict_graph_candidates,
        broad_graph_candidates=broad_graph_candidates,
        diagnostics=diagnostics,
        registry=registry,
        limit=limit,
    )
    report = build_full_object_matching_report(
        metrics=metrics,
        mentions=final_mentions,
        cited_title_profiles=final_title_profiles,
        graph_candidates=graph_candidates,
        contexts_path=contexts_input,
        registry_path=registry_input,
        out_path=output,
        cited_title_profiles_path=cited_title_output,
        object_graph_candidates_path=graph_output,
        strict_object_graph_candidates_path=strict_output,
        broad_object_graph_candidates_path=broad_output,
        review_sample_path=review_sample_output,
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
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    """Return object mention rows and matcher diagnostics."""
    frame = _ensure_columns(contexts.copy(), CONTEXT_READ_COLUMNS)
    positive_specs, negative_specs = _build_alias_specs(registry)
    raw_context_mentions: list[dict[str, Any]] = []
    cited_title_profiles: list[dict[str, Any]] = []
    blocked_examples: list[dict[str, Any]] = []
    negative_blocked_count = 0
    case_blocked_count = 0

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
                    surface = _surface_from_match(text, match, char_map)
                    if not _case_policy_allows(surface, spec):
                        case_blocked_count += 1
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
                        _candidate_match(
                            row,
                            spec,
                            matched_in,
                            text,
                            match,
                            char_map,
                            normalized_text=normalized_text,
                        )
                    )
            field_mentions = _dedupe_overlapping_matches(raw_matches)
            if matched_in == "resolved_cited_title":
                cited_title_profiles.extend(field_mentions)
            else:
                raw_context_mentions.extend(field_mentions)

    context_mentions, deduplicated_count = _dedupe_sentence_window_mentions(
        raw_context_mentions
    )
    mentions_df = pd.DataFrame(context_mentions, columns=OBJECT_MENTION_COLUMNS)
    cited_title_df = pd.DataFrame(cited_title_profiles, columns=OBJECT_MENTION_COLUMNS)
    diagnostics = {
        "raw_context_mentions_before_deduplication": len(raw_context_mentions),
        "deduplicated_count": deduplicated_count,
        "cited_title_profile_count": len(cited_title_df),
        "negative_alias_blocked_count": negative_blocked_count,
        "case_blocked_count": case_blocked_count,
        "negative_alias_blocked_examples": pd.DataFrame(blocked_examples),
        "blocked_by_context_cue_count": 0,
    }
    return mentions_df, cited_title_df, diagnostics


def build_object_matching_metrics(
    *,
    contexts: pd.DataFrame,
    mentions: pd.DataFrame,
    cited_title_profiles: pd.DataFrame,
    graph_candidates: pd.DataFrame,
    strict_graph_candidates: pd.DataFrame,
    broad_graph_candidates: pd.DataFrame,
    diagnostics: dict[str, Any],
    registry: list[ObjectRegistryEntry],
    limit: int | None,
) -> dict[str, Any]:
    """Build metrics for object matching reports."""
    contexts_with_mentions = (
        int(mentions["context_id"].nunique(dropna=True)) if not mentions.empty else 0
    )
    contexts_with_graph_candidates = (
        int(graph_candidates["context_id"].nunique(dropna=True))
        if not graph_candidates.empty
        else 0
    )
    policy_checks = build_object_matching_policy_checks(
        mentions=mentions,
        graph_candidates=graph_candidates,
        strict_graph_candidates=strict_graph_candidates,
        broad_graph_candidates=broad_graph_candidates,
    )
    return {
        "total_context_rows_processed": int(len(contexts)),
        "contexts_with_any_object_mention": contexts_with_mentions,
        "contexts_with_graph_candidate_mention": contexts_with_graph_candidates,
        "input_context_rows_processed": int(len(contexts)),
        "limit": "full" if limit is None else limit,
        "registry_objects": len(registry),
        "raw_mentions_before_deduplication": int(
            diagnostics["raw_context_mentions_before_deduplication"]
        ),
        "mentions_after_deduplication": int(len(mentions)),
        "deduplicated_mentions_after_deduplication": int(len(mentions)),
        "deduplicated_count": int(diagnostics["deduplicated_count"]),
        "context_mentions_count": int(len(mentions)),
        "cited_title_profile_count": int(len(cited_title_profiles)),
        "contexts_with_at_least_one_object_mention": contexts_with_mentions,
        "total_object_mentions": int(len(mentions)),
        "object_graph_candidate_count": int(len(graph_candidates)),
        "strict_graph_candidate_count": int(len(strict_graph_candidates)),
        "broad_graph_candidate_count": int(len(broad_graph_candidates)),
        "policy_checks": policy_checks,
        "object_mentions_by_object_type": _value_counts(mentions, ["object_type"], "mentions"),
        "object_mentions_by_object_category": _value_counts(
            mentions,
            ["object_category"],
            "mentions",
        ),
        "object_mentions_by_allow_in_object_graph": _value_counts(
            mentions,
            ["allow_in_object_graph"],
            "mentions",
        ),
        "object_mentions_by_graph_eligible": _value_counts(
            mentions,
            ["graph_eligible"],
            "mentions",
        ),
        "object_mentions_by_phase1_feature_eligible": _value_counts(
            mentions,
            ["phase1_feature_eligible"],
            "mentions",
        ),
        "graph_candidates_by_object_type": _value_counts(
            graph_candidates,
            ["object_type"],
            "mentions",
        ),
        "graph_candidates_by_object_category": _value_counts(
            graph_candidates,
            ["object_category"],
            "mentions",
        ),
        "graph_candidates_by_normalized_section": _value_counts(
            graph_candidates,
            ["normalized_section"],
            "mentions",
        ),
        "graph_candidates_by_matched_in": _value_counts(
            graph_candidates,
            ["matched_in"],
            "mentions",
        ),
        "cited_title_profiles_by_object_type": _value_counts(
            cited_title_profiles,
            ["object_type"],
            "profiles",
        ),
        "top_50_matched_objects": _value_counts(
            mentions,
            ["object_id", "canonical_name", "object_type"],
            "mentions",
            limit=50,
        ),
        "top_100_named_objects": _value_counts(
            mentions.loc[mentions["object_category"].eq("named_object")],
            ["object_id", "canonical_name", "object_type"],
            "mentions",
            limit=100,
        ),
        "top_100_graph_candidate_objects": _value_counts(
            graph_candidates,
            ["object_id", "canonical_name", "object_type"],
            "mentions",
            limit=100,
        ),
        "top_50_cited_title_profile_objects": _value_counts(
            cited_title_profiles,
            ["object_id", "canonical_name", "object_type"],
            "profiles",
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
        "top_generic_metrics": _value_counts(
            mentions.loc[mentions["object_category"].eq("generic_metric")],
            ["object_id", "canonical_name", "surface_form"],
            "mentions",
            limit=50,
        ),
        "top_ambiguous_short_alias_matches": _value_counts(
            mentions.loc[mentions["object_category"].eq("ambiguous_short_alias")],
            ["object_id", "canonical_name", "surface_form", "match_policy"],
            "mentions",
            limit=50,
        ),
        "ptb_examples": _surface_examples(mentions, "PTB", 20),
        "generic_metric_examples": _generic_metric_examples(mentions, 20),
        "transformer_case_examples": _transformer_case_examples(mentions, 20),
        "cited_title_profile_examples": _sample_mentions(cited_title_profiles, 20),
        "potential_short_alias_false_positives": _short_alias_examples(mentions, 20),
        "potential_inside_longer_word_false_positives": pd.DataFrame(
            columns=OBJECT_MENTION_COLUMNS
        ),
        "potential_common_term_false_positives": _common_term_examples(mentions, 20),
        "negative_alias_blocked_count": int(diagnostics["negative_alias_blocked_count"]),
        "blocked_by_context_cue_count": int(diagnostics["blocked_by_context_cue_count"]),
        "case_blocked_count": int(diagnostics["case_blocked_count"]),
        "low_confidence_match_count": int(
            mentions["confidence"].fillna(0).astype(float).lt(0.75).sum()
        ),
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
    cited_title_profiles_path: Path,
    review_sample_path: Path,
) -> str:
    """Build a markdown report for Task 8A.1 refined object mention matching."""
    core = pd.DataFrame(
        [
            {
                "metric": "input context rows processed",
                "value": metrics["input_context_rows_processed"],
            },
            {"metric": "configured limit", "value": metrics["limit"]},
            {"metric": "registry objects", "value": metrics["registry_objects"]},
            {
                "metric": "raw mentions before deduplication",
                "value": metrics["raw_mentions_before_deduplication"],
            },
            {
                "metric": "deduplicated mentions after deduplication",
                "value": metrics["deduplicated_mentions_after_deduplication"],
            },
            {"metric": "deduplicated_count", "value": metrics["deduplicated_count"]},
            {"metric": "context mentions count", "value": metrics["context_mentions_count"]},
            {
                "metric": "cited title profile count",
                "value": metrics["cited_title_profile_count"],
            },
            {
                "metric": "contexts with at least one object mention",
                "value": metrics["contexts_with_at_least_one_object_mention"],
            },
            {"metric": "total object mentions", "value": metrics["total_object_mentions"]},
            {
                "metric": "negative alias blocked count",
                "value": metrics["negative_alias_blocked_count"],
            },
            {
                "metric": "blocked_by_context_cue count",
                "value": metrics["blocked_by_context_cue_count"],
            },
            {"metric": "case blocked count", "value": metrics["case_blocked_count"]},
            {
                "metric": "low_confidence_match count",
                "value": metrics["low_confidence_match_count"],
            },
        ]
    )
    sections = [
        "# Object Matching Sample Refined Report",
        "",
        "## Inputs",
        f"- Contexts: `{contexts_path}`",
        f"- Registry: `{registry_path}`",
        "",
        "## Outputs",
        f"- Context object mentions sample: `{out_path}`",
        f"- Cited-title object profiles sample: `{cited_title_profiles_path}`",
        f"- Manual object mention review sample: `{review_sample_path}`",
        "",
        "## Core Metrics",
        _table(core),
        "",
        "## Object Mentions By Object Type",
        _table(metrics["object_mentions_by_object_type"]),
        "",
        "## Object Mentions By Object Category",
        _table(metrics["object_mentions_by_object_category"]),
        "",
        "## Object Mentions By allow_in_object_graph",
        _table(metrics["object_mentions_by_allow_in_object_graph"]),
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
        "## Top Generic Metrics",
        _table(metrics["top_generic_metrics"]),
        "",
        "## Top Ambiguous Short Alias Matches",
        _table(metrics["top_ambiguous_short_alias_matches"]),
        "",
        "## PTB Match Examples",
        _table(metrics["ptb_examples"]),
        "",
        "## Accuracy / F1 / Perplexity Examples",
        _table(metrics["generic_metric_examples"]),
        "",
        "## Transformer Uppercase / Lowercase Examples",
        _table(metrics["transformer_case_examples"]),
        "",
        "## Cited Title Profile Examples",
        _table(metrics["cited_title_profile_examples"]),
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


def build_full_object_matching_report(
    *,
    metrics: dict[str, Any],
    mentions: pd.DataFrame,
    cited_title_profiles: pd.DataFrame,
    graph_candidates: pd.DataFrame,
    contexts_path: Path,
    registry_path: Path,
    out_path: Path,
    cited_title_profiles_path: Path,
    object_graph_candidates_path: Path | None,
    strict_object_graph_candidates_path: Path | None,
    broad_object_graph_candidates_path: Path | None,
    review_sample_path: Path,
) -> str:
    """Build the full object matching report for Task 8B."""
    core = pd.DataFrame(
        [
            {
                "metric": "total_context_rows_processed",
                "value": metrics["total_context_rows_processed"],
            },
            {
                "metric": "contexts_with_any_object_mention",
                "value": metrics["contexts_with_any_object_mention"],
            },
            {
                "metric": "contexts_with_graph_candidate_mention",
                "value": metrics["contexts_with_graph_candidate_mention"],
            },
            {
                "metric": "raw_mentions_before_deduplication",
                "value": metrics["raw_mentions_before_deduplication"],
            },
            {
                "metric": "mentions_after_deduplication",
                "value": metrics["mentions_after_deduplication"],
            },
            {"metric": "deduplicated_count", "value": metrics["deduplicated_count"]},
            {
                "metric": "cited_title_profile_count",
                "value": metrics["cited_title_profile_count"],
            },
            {
                "metric": "object_graph_candidate_count",
                "value": metrics["object_graph_candidate_count"],
            },
            {
                "metric": "strict_graph_candidate_count",
                "value": metrics["strict_graph_candidate_count"],
            },
            {
                "metric": "broad_graph_candidate_count",
                "value": metrics["broad_graph_candidate_count"],
            },
        ]
    )
    sections = [
        "# Object Matching Report",
        "",
        "## Inputs",
        f"- Contexts: `{contexts_path}`",
        f"- Registry: `{registry_path}`",
        f"- Configured limit: `{metrics['limit']}`",
        "",
        "## Outputs",
        f"- Object mentions: `{out_path}`",
        f"- Cited-title object profiles: `{cited_title_profiles_path}`",
        f"- Object graph candidates: `{object_graph_candidates_path or 'not written'}`",
        f"- Strict graph candidates: `{strict_object_graph_candidates_path or 'not written'}`",
        f"- Broad graph candidates: `{broad_object_graph_candidates_path or 'not written'}`",
        f"- Review sample: `{review_sample_path}`",
        "",
        "## Core Counts",
        _table(core),
        "",
        "## Mentions By Object Type",
        _table(metrics["object_mentions_by_object_type"]),
        "",
        "## Mentions By Object Category",
        _table(metrics["object_mentions_by_object_category"]),
        "",
        "## Mentions By allow_in_object_graph",
        _table(metrics["object_mentions_by_allow_in_object_graph"]),
        "",
        "## Mentions By graph_eligible",
        _table(metrics["object_mentions_by_graph_eligible"]),
        "",
        "## Mentions By phase1_feature_eligible",
        _table(metrics["object_mentions_by_phase1_feature_eligible"]),
        "",
        "## Graph Candidates By Object Type",
        _table(metrics["graph_candidates_by_object_type"]),
        "",
        "## Graph Candidates By Object Category",
        _table(metrics["graph_candidates_by_object_category"]),
        "",
        "## Graph Candidates By Normalized Section",
        _table(metrics["graph_candidates_by_normalized_section"]),
        "",
        "## Graph Candidates By Matched In",
        _table(metrics["graph_candidates_by_matched_in"]),
        "",
        "## Cited Title Profiles By Object Type",
        _table(metrics["cited_title_profiles_by_object_type"]),
        "",
        "## Top 100 Named Objects By Mention Count",
        _table(metrics["top_100_named_objects"]),
        "",
        "## Top 100 Graph Candidate Objects",
        _table(metrics["top_100_graph_candidate_objects"]),
        "",
        "## Top 50 Generic Metrics",
        _table(metrics["top_generic_metrics"]),
        "",
        "## Top 50 Ambiguous Aliases",
        _table(metrics["top_ambiguous_short_alias_matches"]),
        "",
        "## Top 50 Cited-Title Profile Objects",
        _table(metrics["top_50_cited_title_profile_objects"]),
        "",
        "## Top 50 Surface Forms",
        _table(metrics["top_50_surface_forms"]),
        "",
        "## Policy Checks",
        _table(metrics["policy_checks"]),
        "",
        "## original_allow_in_object_graph=False but graph_eligible=True Examples",
        _table(_original_false_graph_true_examples(mentions, 20)),
        "",
        "## Named Object Strict Candidate Examples",
        _table(_policy_examples(_named_strict_candidates(graph_candidates), 20)),
        "",
        "## Named Object Broad Candidate Examples",
        _table(_policy_examples(_named_broad_candidates(graph_candidates), 20)),
        "",
        "## Generic Metric Feature-Only Examples",
        _table(_policy_examples(_generic_feature_only(mentions), 20)),
        "",
        "## PTB With Cue Examples",
        _table(_policy_examples(_ptb_with_cue(mentions), 20)),
        "",
        "## PTB Without Cue / Downgraded Examples",
        _table(_policy_examples(_ptb_without_cue(mentions), 20)),
        "",
        "## Uppercase Transformer Examples",
        _table(_policy_examples(_uppercase_transformer(mentions), 20)),
        "",
        "## Lowercase transformer Downgraded Examples",
        _table(_policy_examples(_lowercase_transformer_downgraded(mentions), 20)),
        "",
        "## seq2seq Kept / Downgraded Examples",
        _table(_policy_examples(_seq2seq_examples(mentions), 20)),
        "",
        "## Cited-Title Object Profile Examples",
        _table(_policy_examples(cited_title_profiles, 20)),
        "",
    ]
    return "\n".join(sections)


def build_object_mentions_review_sample(
    *,
    contexts: pd.DataFrame,
    mentions: pd.DataFrame,
    cited_title_profiles: pd.DataFrame,
    seed: int = 13,
) -> pd.DataFrame:
    """Build a deterministic 300-row object mention review sample."""
    buckets = [
        (
            "named_object_high_confidence",
            mentions.loc[
                mentions["object_category"].eq("named_object")
                & mentions["confidence"].fillna(0).astype(float).ge(0.85)
            ],
            75,
        ),
        (
            "generic_metric",
            mentions.loc[mentions["object_category"].eq("generic_metric")],
            75,
        ),
        (
            "ambiguous_short_alias",
            mentions.loc[mentions["object_category"].eq("ambiguous_short_alias")],
            50,
        ),
        ("resolved_title_profile", cited_title_profiles, 50),
        (
            "low_confidence_or_context_cue_missing",
            mentions.loc[
                mentions["confidence"].fillna(0).astype(float).lt(0.75)
                | mentions["match_policy"].fillna("").astype(str).str.contains(
                    "weak_context_cue_missing",
                    regex=False,
                )
            ],
            50,
        ),
    ]
    samples = []
    for index, (bucket, frame, requested) in enumerate(buckets):
        sample = _sample_frame(frame, requested, seed + index).copy()
        if sample.empty:
            continue
        sample["review_bucket"] = bucket
        samples.append(sample)
    if samples:
        review = pd.concat(samples, ignore_index=True)
    else:
        review = pd.DataFrame(columns=OBJECT_MENTION_COLUMNS)
    context_columns = contexts[
        ["context_id", "source_context_id", "sentence_text", "context_window_s3"]
    ].drop_duplicates(subset=["context_id", "source_context_id"])
    review = review.merge(
        context_columns,
        on=["context_id", "source_context_id"],
        how="left",
        suffixes=("", "_context"),
    )
    review["reviewer_correct"] = ""
    review["reviewer_notes"] = ""
    review = _ensure_columns(review, OBJECT_REVIEW_SAMPLE_COLUMNS)
    return review[OBJECT_REVIEW_SAMPLE_COLUMNS]


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
    object_category = _clean_text(raw.get("object_category") or "named_object")
    if object_category not in OBJECT_CATEGORIES:
        raise ValueError(
            f"Registry entry {index} has unknown object_category: {object_category}"
        )
    aliases = _as_text_tuple(raw.get("aliases"))
    if not aliases:
        raise ValueError(f"Registry entry {index} must have at least one alias")
    confidence_override = raw.get("confidence_override")
    if confidence_override in ("", None):
        confidence_override = None
    elif not isinstance(confidence_override, int | float):
        raise ValueError(f"Registry entry {index} confidence_override must be numeric")
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
        object_category=object_category,
        allow_in_object_graph=bool(raw.get("allow_in_object_graph", True)),
        require_case_sensitive=bool(raw.get("require_case_sensitive", False)),
        require_context_cue=_as_text_tuple(raw.get("require_context_cue")),
        confidence_override=float(confidence_override)
        if confidence_override is not None
        else None,
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


def _read_contexts(path: Path, *, limit: int | None) -> pd.DataFrame:
    parquet_file = pq.ParquetFile(path)
    available_columns = set(parquet_file.schema_arrow.names)
    columns = [column for column in CONTEXT_READ_COLUMNS if column in available_columns]
    batches = []
    remaining = limit
    batch_size = 50_000 if limit is None else min(50_000, limit)
    for batch in parquet_file.iter_batches(batch_size=batch_size, columns=columns):
        take = batch.num_rows if remaining is None else min(remaining, batch.num_rows)
        batches.append(batch.slice(0, take).to_pandas())
        if remaining is None:
            continue
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
    *,
    normalized_text: str,
) -> dict[str, Any]:
    char_start = char_map[match.start()]
    char_end = char_map[match.end() - 1] + 1
    surface = text[char_start:char_end]
    match_type = _match_type(surface, spec.alias)
    confidence, match_policy, object_category, allow_in_object_graph = _confidence_policy(
        surface=surface,
        match_type=match_type,
        spec=spec,
        matched_in=matched_in,
        text=text,
        char_start=char_start,
        char_end=char_end,
    )
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
        "object_category": object_category,
        "surface_form": surface,
        "normalized_surface": _normalized_surface(surface),
        "match_type": match_type,
        "char_start": char_start,
        "char_end": char_end,
        "confidence": confidence,
        "matched_in": matched_in,
        "match_policy": match_policy,
        "allow_in_object_graph": allow_in_object_graph,
        "provenance": f"registry_seed:{spec.entry.object_id};alias={spec.alias}",
        "_span": (char_start, char_end),
        "_normalized_span": (match.start(), match.end()),
        "_alias_length": spec.alias_length,
        "_normalized_text": normalized_text,
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


def _dedupe_sentence_window_mentions(
    mentions: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], int]:
    sentence_keys = {
        _dedupe_key(mention)
        for mention in mentions
        if mention.get("matched_in") == "sentence_text"
    }
    output = []
    dropped = 0
    for mention in mentions:
        if mention.get("matched_in") != "context_window_s3":
            output.append(mention)
            continue
        if _dedupe_key(mention) in sentence_keys:
            dropped += 1
            continue
        neighbor = mention.copy()
        neighbor["matched_in"] = "context_window_neighbor"
        neighbor["confidence"] = round(max(0.0, float(neighbor["confidence"]) - 0.10), 3)
        neighbor["match_policy"] = f"{neighbor['match_policy']};neighbor_context_match"
        output.append(neighbor)
    return output, dropped


def _dedupe_key(mention: dict[str, Any]) -> tuple[str, str, str]:
    return (
        _clean_text(mention.get("context_id")),
        _clean_text(mention.get("object_id")),
        _clean_text(mention.get("normalized_surface")),
    )


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


def _confidence_policy(
    *,
    surface: str,
    match_type: str,
    spec: AliasSpec,
    matched_in: str,
    text: str,
    char_start: int,
    char_end: int,
) -> tuple[float, str, str, bool]:
    confidence = (
        spec.entry.confidence_override
        if spec.entry.confidence_override is not None
        else _confidence(match_type, spec)
    )
    match_policy = "standard"
    object_category = spec.entry.object_category
    allow_in_object_graph = spec.entry.allow_in_object_graph

    if spec.entry.object_category == "generic_metric":
        confidence = min(confidence, 0.70)
        allow_in_object_graph = False
        match_policy = "generic_metric"

    if _is_lowercase_transformer(surface, spec):
        confidence = min(confidence, 0.65)
        object_category = "generic_architecture"
        allow_in_object_graph = False
        match_policy = "lowercase_generic_architecture"
    elif spec.entry.object_id == "obj_transformer":
        confidence = max(confidence, 0.95)

    if spec.entry.require_context_cue:
        if _has_context_cue(text, char_start, char_end, spec.entry.require_context_cue):
            match_policy = "context_cue_present"
        else:
            confidence = min(confidence, 0.50)
            object_category = "ambiguous_short_alias"
            allow_in_object_graph = False
            match_policy = "weak_context_cue_missing"

    if matched_in == "context_window_neighbor":
        confidence = max(0.0, confidence - 0.10)
        match_policy = f"{match_policy};neighbor_context_match"

    return round(confidence, 3), match_policy, object_category, allow_in_object_graph


def _is_lowercase_transformer(surface: str, spec: AliasSpec) -> bool:
    return (
        spec.entry.object_id == "obj_transformer"
        and _normalized_surface(surface) in {"transformer", "transformers"}
        and surface[:1].islower()
    )


def _has_context_cue(
    text: str,
    char_start: int,
    char_end: int,
    cues: tuple[str, ...],
    *,
    window_chars: int = 80,
) -> bool:
    start = max(0, char_start - window_chars)
    end = min(len(text), char_end + window_chars)
    window = text[start:end].lower()
    return any(cue.lower() in window for cue in cues if cue)


def _case_policy_allows(surface: str, spec: AliasSpec) -> bool:
    if not spec.entry.require_case_sensitive:
        return True
    return _alnum_case_key(surface) == _alnum_case_key(spec.alias)


def _alnum_case_key(value: str) -> str:
    return "".join(char for char in value if char.isalnum() or char in {"+", "#"})


def _surface_from_match(text: str, match: re.Match[str], char_map: list[int]) -> str:
    char_start = char_map[match.start()]
    char_end = char_map[match.end() - 1] + 1
    return text[char_start:char_end]


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


def _surface_examples(mentions: pd.DataFrame, surface: str, limit: int) -> pd.DataFrame:
    if mentions.empty:
        return pd.DataFrame(columns=OBJECT_MENTION_COLUMNS)
    matches = mentions.loc[
        mentions["surface_form"].fillna("").astype(str).str.lower().eq(surface.lower())
    ]
    return _sample_mentions(matches, limit)


def _generic_metric_examples(mentions: pd.DataFrame, limit: int) -> pd.DataFrame:
    if mentions.empty:
        return pd.DataFrame(columns=OBJECT_MENTION_COLUMNS)
    generic = mentions.loc[
        mentions["canonical_name"].isin(["accuracy", "F1", "perplexity"])
    ]
    return _sample_mentions(generic, limit)


def _transformer_case_examples(mentions: pd.DataFrame, limit: int) -> pd.DataFrame:
    if mentions.empty:
        return pd.DataFrame(columns=OBJECT_MENTION_COLUMNS)
    transformer = mentions.loc[mentions["canonical_name"].eq("Transformer")]
    return _sample_mentions(transformer, limit)


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


def build_object_matching_policy_checks(
    *,
    mentions: pd.DataFrame,
    graph_candidates: pd.DataFrame,
    strict_graph_candidates: pd.DataFrame,
    broad_graph_candidates: pd.DataFrame,
) -> pd.DataFrame:
    """Return Task 8B policy consistency checks."""
    checks = [
        (
            "generic_metric rows in object_graph_candidate_mentions",
            _count_rows(graph_candidates, graph_candidates["object_category"].eq("generic_metric")),
        ),
        (
            "accuracy rows in object_graph_candidate_mentions",
            _count_rows(graph_candidates, graph_candidates["object_id"].eq("obj_accuracy")),
        ),
        (
            "F1 rows in object_graph_candidate_mentions",
            _count_rows(graph_candidates, graph_candidates["object_id"].eq("obj_f1")),
        ),
        (
            "perplexity rows in object_graph_candidate_mentions",
            _count_rows(graph_candidates, graph_candidates["object_id"].eq("obj_perplexity")),
        ),
        (
            "resolved_cited_title rows in object_mentions",
            _count_rows(mentions, mentions["matched_in"].eq("resolved_cited_title")),
        ),
        (
            "resolved_cited_title rows in object_graph_candidate_mentions",
            _count_rows(
                graph_candidates,
                graph_candidates["matched_in"].eq("resolved_cited_title"),
            ),
        ),
        (
            "strict candidates with matched_in != sentence_text",
            _count_rows(
                strict_graph_candidates,
                ~strict_graph_candidates["matched_in"].eq("sentence_text"),
            ),
        ),
        (
            "broad candidates with matched_in != context_window_neighbor",
            _count_rows(
                broad_graph_candidates,
                ~broad_graph_candidates["matched_in"].eq("context_window_neighbor"),
            ),
        ),
        (
            "ambiguous_short_alias rows in strict graph candidates",
            _count_rows(
                strict_graph_candidates,
                strict_graph_candidates["object_category"].eq("ambiguous_short_alias"),
            ),
        ),
    ]
    rows = [
        {"policy_check": name, "rows": rows, "status": "pass" if rows == 0 else "fail"}
        for name, rows in checks
    ]
    review_count = _count_rows(
        mentions,
        (~mentions["original_allow_in_object_graph"].map(_bool_value))
        & mentions["graph_eligible"].map(_bool_value),
    )
    rows.append(
        {
            "policy_check": "original_allow_in_object_graph=False but graph_eligible=True",
            "rows": review_count,
            "status": "review",
        }
    )
    return pd.DataFrame(rows)


def _policy_examples(frame: pd.DataFrame, limit: int) -> pd.DataFrame:
    columns = [
        "context_id",
        "source_context_id",
        "canonical_name",
        "object_type",
        "object_category",
        "surface_form",
        "confidence",
        "matched_in",
        "allow_in_object_graph",
        "graph_eligible",
        "phase1_feature_eligible",
        "graph_candidate_level",
        "policy_reason",
        "match_policy",
        "normalized_section",
        "resolved_cited_title",
    ]
    if frame.empty:
        return pd.DataFrame(columns=columns)
    sample = _ensure_columns(frame.head(limit).copy(), columns)
    for column in ("resolved_cited_title", "policy_reason", "match_policy"):
        sample[column] = sample[column].map(lambda value: _truncate(value, 140))
    return sample[columns]


def _original_false_graph_true_examples(mentions: pd.DataFrame, limit: int) -> pd.DataFrame:
    if mentions.empty:
        return pd.DataFrame()
    mask = (~mentions["original_allow_in_object_graph"].map(_bool_value)) & mentions[
        "graph_eligible"
    ].map(_bool_value)
    return _policy_examples(mentions.loc[mask], limit)


def _named_strict_candidates(graph_candidates: pd.DataFrame) -> pd.DataFrame:
    return graph_candidates.loc[
        graph_candidates["object_category"].eq("named_object")
        & graph_candidates["graph_candidate_level"].eq("strict")
    ]


def _named_broad_candidates(graph_candidates: pd.DataFrame) -> pd.DataFrame:
    return graph_candidates.loc[
        graph_candidates["object_category"].eq("named_object")
        & graph_candidates["graph_candidate_level"].eq("broad")
    ]


def _generic_feature_only(mentions: pd.DataFrame) -> pd.DataFrame:
    return mentions.loc[
        mentions["object_category"].eq("generic_metric")
        & mentions["phase1_feature_eligible"].map(_bool_value)
        & (~mentions["graph_eligible"].map(_bool_value))
    ]


def _ptb_with_cue(mentions: pd.DataFrame) -> pd.DataFrame:
    return mentions.loc[
        mentions["object_id"].eq("obj_penn_treebank")
        & mentions["policy_reason"].fillna("").astype(str).str.contains("cue_present")
    ]


def _ptb_without_cue(mentions: pd.DataFrame) -> pd.DataFrame:
    return mentions.loc[
        mentions["object_id"].eq("obj_penn_treebank")
        & mentions["policy_reason"].fillna("").astype(str).str.contains("cue_missing")
    ]


def _uppercase_transformer(mentions: pd.DataFrame) -> pd.DataFrame:
    transformer = mentions.loc[mentions["object_id"].eq("obj_transformer")]
    return transformer.loc[transformer["surface_form"].fillna("").astype(str).str.startswith("T")]


def _lowercase_transformer_downgraded(mentions: pd.DataFrame) -> pd.DataFrame:
    transformer = mentions.loc[mentions["object_id"].eq("obj_transformer")]
    return transformer.loc[
        transformer["surface_form"].fillna("").astype(str).str.startswith("t")
        & transformer["policy_reason"].fillna("").astype(str).str.contains("feature_only")
    ]


def _seq2seq_examples(mentions: pd.DataFrame) -> pd.DataFrame:
    return mentions.loc[mentions["object_id"].eq("obj_seq2seq")]


def _count_rows(frame: pd.DataFrame, mask: pd.Series) -> int:
    if frame.empty:
        return 0
    return int(mask.sum())


def _sample_frame(frame: pd.DataFrame, n: int, seed: int) -> pd.DataFrame:
    if frame.empty or n <= 0:
        return pd.DataFrame(columns=frame.columns)
    if len(frame) <= n:
        return frame.sample(frac=1, random_state=seed).reset_index(drop=True)
    return frame.sample(n=n, random_state=seed).reset_index(drop=True)


def _attach_context_text_for_policy(mentions: pd.DataFrame, contexts: pd.DataFrame) -> pd.DataFrame:
    if mentions.empty:
        return mentions.copy()
    context_columns = [
        "context_id",
        "source_context_id",
        "sentence_text",
        "context_window_s3",
    ]
    context_frame = _ensure_columns(contexts.copy(), context_columns)
    context_frame = context_frame[context_columns].drop_duplicates(
        subset=["context_id", "source_context_id"]
    )
    return mentions.merge(
        context_frame,
        on=["context_id", "source_context_id"],
        how="left",
    )


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


def _bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None or pd.isna(value):
        return False
    return str(value).strip().lower() in {"true", "1", "yes"}


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
