from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from citeevidence.contexts.extract import CONTEXT_COLUMNS

DEFAULT_RESOLVED_PILOT_PATH = Path("data/processed/citation_contexts_resolved_pilot.parquet")
DEFAULT_RESOLUTION_FAILURES_PATH = Path(
    "data/processed/citation_marker_resolution_pilot_failures.parquet"
)
DEFAULT_RESOLUTION_REPORT_PATH = Path("reports/citation_marker_resolution_pilot_report.md")

RESOLUTION_COLUMNS = [
    "source_context_id",
    "marker_component_index",
    "marker_component_text",
    "parsed_surnames",
    "parsed_year",
    "candidate_count_for_citing_paper",
    "matched_candidate_count",
    "matched_candidate_acl_ids",
    "resolved_cited_acl_id",
    "resolved_cited_corpus_paper_id",
    "resolved_cited_title",
    "resolved_cited_year",
    "resolved_cited_authors",
    "resolved_cited_doi",
    "resolution_status",
    "resolution_confidence",
    "resolution_method",
]
OUTPUT_COLUMNS = [*CONTEXT_COLUMNS, *RESOLUTION_COLUMNS]
GRAPH_READ_COLUMNS = [
    "citing_acl_id",
    "cited_acl_id",
    "cited_corpus_paper_id",
    "cited_title",
    "cited_year",
    "cited_authors",
    "cited_doi",
]
YEAR_RE = re.compile(r"\b((?:19|20)\d{2})[a-z]?\b", re.IGNORECASE)
NUMERIC_BRACKET_RE = re.compile(r"\[\s*\d+\s*(?:(?:[,;]\s*\d+)|(?:[-–—]\s*\d+))*\s*\]")
FILLER_RE = re.compile(r"\b(?:see|cf|e\.g|e\.g\.|eg|also|and|or|in)\b", re.IGNORECASE)


@dataclass(frozen=True)
class MarkerComponent:
    text: str
    surnames: list[str]
    year: str | None
    is_numeric: bool = False
    is_year_only: bool = False
    is_et_al: bool = False


@dataclass(frozen=True)
class CandidatePaper:
    cited_acl_id: str
    cited_corpus_paper_id: int | None
    cited_title: str | None
    cited_year: str | None
    cited_authors: str | None
    cited_doi: str | None
    surnames: frozenset[str]


def resolve_citation_markers_pilot(
    *,
    contexts_path: str | Path,
    aligned_graph_path: str | Path,
    crosswalk_path: str | Path,
    out_path: str | Path = DEFAULT_RESOLVED_PILOT_PATH,
    failures_path: str | Path = DEFAULT_RESOLUTION_FAILURES_PATH,
    report_path: str | Path = DEFAULT_RESOLUTION_REPORT_PATH,
    limit: int = 100_000,
    sample: bool = False,
    random_seed: int = 13,
) -> dict[str, Any]:
    """Resolve author-year citation markers against ACL-to-ACL graph candidates."""
    if limit < 1:
        raise ValueError("limit must be positive")
    paths = [Path(contexts_path), Path(aligned_graph_path), Path(crosswalk_path)]
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"Required input does not exist: {path}")

    contexts = _read_contexts(Path(contexts_path), limit=limit, sample=sample, seed=random_seed)
    contexts = _ensure_columns(contexts, CONTEXT_COLUMNS)
    duplicate_before = int(len(contexts) - contexts["context_id"].nunique(dropna=True))

    candidate_index = _load_candidate_index(
        Path(aligned_graph_path),
        citing_paper_ids=set(contexts["citing_paper_id"].dropna().astype(str)),
    )
    resolved = _resolve_contexts(contexts, candidate_index)
    duplicate_after = int(len(resolved) - resolved["context_id"].nunique(dropna=True))

    output = Path(out_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    resolved.to_parquet(output, index=False)

    failures = resolved.loc[resolved["resolution_status"].ne("author_year_clear")].copy()
    failures_output = Path(failures_path)
    failures_output.parent.mkdir(parents=True, exist_ok=True)
    failures.to_parquet(failures_output, index=False)

    metrics = _build_metrics(
        contexts=contexts,
        resolved=resolved,
        failures=failures,
        duplicate_before=duplicate_before,
        duplicate_after=duplicate_after,
        candidate_index=candidate_index,
    )
    report = build_resolution_report(
        metrics,
        contexts_path=Path(contexts_path),
        aligned_graph_path=Path(aligned_graph_path),
        crosswalk_path=Path(crosswalk_path),
        out_path=output,
        failures_path=failures_output,
        limit=limit,
        sample=sample,
    )
    report_output = Path(report_path)
    report_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.write_text(report, encoding="utf-8")
    return metrics


def parse_citation_marker(marker: Any) -> list[MarkerComponent]:
    """Parse a citation marker into numeric or author-year components."""
    text = _clean_text(marker)
    if not text:
        return [MarkerComponent(text="", surnames=[], year=None)]
    if NUMERIC_BRACKET_RE.fullmatch(text):
        return [MarkerComponent(text=text, surnames=[], year=None, is_numeric=True)]

    body = _strip_outer_parens(text)
    components = []
    for raw_component in [part.strip() for part in body.split(";") if part.strip()]:
        year_match = YEAR_RE.search(raw_component)
        if year_match is None:
            components.append(MarkerComponent(text=raw_component, surnames=[], year=None))
            continue
        year = year_match.group(1)
        before_year = raw_component[: year_match.start()]
        is_et_al = bool(re.search(r"\bet\s+al\.?\b", before_year, flags=re.IGNORECASE))
        surnames = _parsed_surnames(before_year)
        is_year_only = len(surnames) == 0
        components.append(
            MarkerComponent(
                text=raw_component,
                surnames=surnames,
                year=year,
                is_year_only=is_year_only,
                is_et_al=is_et_al,
            )
        )
    if not components:
        return [MarkerComponent(text=text, surnames=[], year=None)]
    return components


def build_resolution_report(
    metrics: dict[str, Any],
    *,
    contexts_path: Path,
    aligned_graph_path: Path,
    crosswalk_path: Path,
    out_path: Path,
    failures_path: Path,
    limit: int,
    sample: bool,
) -> str:
    """Build a markdown report for the citation marker resolution pilot."""
    core_rows = [
        {"metric": "total input contexts processed", "value": metrics["total_input_contexts"]},
        {"metric": "output rows", "value": metrics["output_rows"]},
        {
            "metric": "duplicate context_id count before",
            "value": metrics["duplicate_context_id_before"],
        },
        {
            "metric": "duplicate context_id count after",
            "value": metrics["duplicate_context_id_after"],
        },
        {
            "metric": "citing_paper_id coverage in aligned graph",
            "value": metrics["citing_paper_id_coverage_in_aligned_graph"],
        },
        {"metric": "author_year_clear rate", "value": metrics["author_year_clear_rate"]},
        {
            "metric": "multi_candidate_ambiguous rate",
            "value": metrics["multi_candidate_ambiguous_rate"],
        },
        {"metric": "ambiguous_year_only rate", "value": metrics["ambiguous_year_only_rate"]},
        {
            "metric": "numeric_marker_unresolved_no_bibliography rate",
            "value": metrics["numeric_marker_unresolved_no_bibliography_rate"],
        },
        {
            "metric": "bibliography_unresolved rate",
            "value": metrics["bibliography_unresolved_rate"],
        },
        {
            "metric": "resolved_cited_title non-empty rate",
            "value": metrics["resolved_cited_title_non_empty_rate"],
        },
    ]
    sections = [
        "# Citation Marker Resolution Pilot Report",
        "",
        "## Inputs",
        _table(
            [
                {"name": "citation_contexts", "path": contexts_path},
                {"name": "acl_citation_graph_aligned", "path": aligned_graph_path},
                {"name": "acl_id_crosswalk", "path": crosswalk_path},
            ]
        ),
        "",
        "## Outputs",
        _table(
            [
                {"name": "citation_contexts_resolved_pilot", "path": out_path},
                {"name": "citation_marker_resolution_pilot_failures", "path": failures_path},
            ]
        ),
        "",
        f"- Limit: {limit}",
        f"- Random sample: {sample}",
        "",
        "## Core Metrics",
        _table(core_rows),
        "",
        "## Resolution Status Distribution",
        _table(metrics["resolution_status_distribution"]),
        "",
        "## 20 Examples: author_year_clear",
        _table(metrics["samples"]["author_year_clear"]),
        "",
        "## 20 Examples: multi_candidate_ambiguous",
        _table(metrics["samples"]["multi_candidate_ambiguous"]),
        "",
        "## 20 Examples: unresolved markers",
        _table(metrics["samples"]["unresolved_markers"]),
        "",
        "## Common Failure Patterns",
        _table(metrics["common_failure_patterns"]),
        "",
    ]
    return "\n".join(sections)


def _read_contexts(path: Path, *, limit: int, sample: bool, seed: int) -> pd.DataFrame:
    parquet_file = pq.ParquetFile(path)
    if not sample:
        batches = []
        remaining = limit
        for batch in parquet_file.iter_batches(batch_size=min(50_000, limit)):
            take = min(remaining, batch.num_rows)
            batches.append(batch.slice(0, take).to_pandas())
            remaining -= take
            if remaining <= 0:
                break
        return pd.concat(batches, ignore_index=True) if batches else pd.DataFrame()

    total = parquet_file.metadata.num_rows
    sample_size = min(limit, total)
    rng = np.random.default_rng(seed)
    wanted = sorted(int(index) for index in rng.choice(total, size=sample_size, replace=False))
    wanted_set = set(wanted)
    rows = []
    offset = 0
    for batch in parquet_file.iter_batches(batch_size=50_000):
        local = [index - offset for index in wanted if offset <= index < offset + batch.num_rows]
        if local:
            rows.append(batch.take(pa.array(local)).to_pandas())
        offset += batch.num_rows
        wanted_set.difference_update({index for index in wanted_set if index < offset})
        if not wanted_set:
            break
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def _load_candidate_index(
    aligned_graph_path: Path,
    *,
    citing_paper_ids: set[str],
) -> dict[str, list[CandidatePaper]]:
    graph = pd.read_parquet(aligned_graph_path, columns=GRAPH_READ_COLUMNS)
    graph = graph.loc[graph["citing_acl_id"].astype("string").isin(citing_paper_ids)].copy()
    graph = graph.drop_duplicates(subset=["citing_acl_id", "cited_acl_id"])
    graph["candidate_surnames"] = graph["cited_authors"].map(_candidate_surnames)
    graph["candidate_year"] = graph["cited_year"].map(_year_string)

    index: dict[str, list[CandidatePaper]] = {}
    for row in graph.itertuples(index=False):
        candidate = CandidatePaper(
            cited_acl_id=str(row.cited_acl_id),
            cited_corpus_paper_id=_int_or_none(row.cited_corpus_paper_id),
            cited_title=_clean_text_or_none(row.cited_title),
            cited_year=_year_string(row.cited_year),
            cited_authors=_clean_text_or_none(row.cited_authors),
            cited_doi=_clean_text_or_none(row.cited_doi),
            surnames=frozenset(row.candidate_surnames),
        )
        index.setdefault(str(row.citing_acl_id), []).append(candidate)
    return index


def _resolve_contexts(
    contexts: pd.DataFrame,
    candidate_index: dict[str, list[CandidatePaper]],
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for row_number, row in enumerate(contexts.to_dict(orient="records")):
        source_context_id = _clean_text(row.get("context_id"))
        citing_paper_id = _clean_text(row.get("citing_paper_id"))
        components = parse_citation_marker(row.get("citation_marker"))
        candidates = candidate_index.get(citing_paper_id, [])
        for component_index, component in enumerate(components):
            resolved_fields = _resolve_component(component, candidates)
            output_row = {column: row.get(column) for column in CONTEXT_COLUMNS}
            output_row.update(resolved_fields)
            output_row["source_context_id"] = source_context_id
            output_row["marker_component_index"] = component_index
            output_row["marker_component_text"] = component.text
            output_row["parsed_surnames"] = ";".join(component.surnames)
            output_row["parsed_year"] = component.year
            output_row["candidate_count_for_citing_paper"] = len(candidates)
            output_row["context_id"] = _resolved_context_id(
                source_context_id=source_context_id,
                row_number=row_number,
                component_index=component_index,
                resolution_status=output_row["resolution_status"],
                matched_candidate_acl_ids=output_row["matched_candidate_acl_ids"],
            )
            rows.append(output_row)
    return pd.DataFrame(rows, columns=OUTPUT_COLUMNS)


def _resolve_component(
    component: MarkerComponent,
    candidates: list[CandidatePaper],
) -> dict[str, Any]:
    if component.is_numeric:
        return _unresolved_fields(
            status="numeric_marker_unresolved_no_bibliography",
            method="numeric_marker",
            candidates=[],
        )
    if not candidates:
        return _unresolved_fields(
            status="citing_paper_not_in_aligned_graph",
            method="no_candidate_graph_for_citing_paper",
            candidates=[],
        )
    if component.year is None:
        return _unresolved_fields(
            status="bibliography_unresolved",
            method="marker_parse_failed",
            candidates=[],
        )

    year_candidates = [
        candidate for candidate in candidates if candidate.cited_year == component.year
    ]
    if component.is_year_only:
        if len(year_candidates) == 1:
            return _resolved_fields(
                year_candidates[0],
                status="year_only_unique_candidate",
                confidence=0.60,
                method="year_only_unique_candidate",
                matched_candidates=year_candidates,
            )
        if len(year_candidates) > 1:
            return _unresolved_fields(
                status="ambiguous_year_only",
                method="year_only_multiple_candidates",
                candidates=year_candidates,
            )
        return _unresolved_fields(
            status="bibliography_unresolved",
            method="year_only_no_candidate",
            candidates=[],
        )

    matched = [
        candidate
        for candidate in year_candidates
        if _candidate_matches_surnames(component, candidate)
    ]
    if len(matched) == 1:
        confidence = 0.95 if len(component.surnames) >= 2 and not component.is_et_al else 0.90
        return _resolved_fields(
            matched[0],
            status="author_year_clear",
            confidence=confidence,
            method="author_year_candidate_graph",
            matched_candidates=matched,
        )
    if len(matched) > 1:
        return _unresolved_fields(
            status="multi_candidate_ambiguous",
            method="author_year_multiple_candidates",
            candidates=matched,
        )
    return _unresolved_fields(
        status="bibliography_unresolved",
        method="author_year_no_candidate",
        candidates=[],
    )


def _candidate_matches_surnames(component: MarkerComponent, candidate: CandidatePaper) -> bool:
    if not component.surnames or not candidate.surnames:
        return False
    if component.surnames[0] not in candidate.surnames:
        return False
    if component.is_et_al or len(component.surnames) == 1:
        return True
    return all(surname in candidate.surnames for surname in component.surnames)


def _resolved_fields(
    candidate: CandidatePaper,
    *,
    status: str,
    confidence: float,
    method: str,
    matched_candidates: list[CandidatePaper],
) -> dict[str, Any]:
    fields = _unresolved_fields(status=status, method=method, candidates=matched_candidates)
    fields.update(
        {
            "resolved_cited_acl_id": candidate.cited_acl_id,
            "resolved_cited_corpus_paper_id": candidate.cited_corpus_paper_id,
            "resolved_cited_title": candidate.cited_title,
            "resolved_cited_year": candidate.cited_year,
            "resolved_cited_authors": candidate.cited_authors,
            "resolved_cited_doi": candidate.cited_doi,
            "resolution_confidence": confidence,
        }
    )
    return fields


def _unresolved_fields(
    *,
    status: str,
    method: str,
    candidates: list[CandidatePaper],
) -> dict[str, Any]:
    return {
        "matched_candidate_count": len(candidates),
        "matched_candidate_acl_ids": ";".join(candidate.cited_acl_id for candidate in candidates),
        "resolved_cited_acl_id": None,
        "resolved_cited_corpus_paper_id": None,
        "resolved_cited_title": None,
        "resolved_cited_year": None,
        "resolved_cited_authors": None,
        "resolved_cited_doi": None,
        "resolution_status": status,
        "resolution_confidence": 0.0,
        "resolution_method": method,
    }


def _build_metrics(
    *,
    contexts: pd.DataFrame,
    resolved: pd.DataFrame,
    failures: pd.DataFrame,
    duplicate_before: int,
    duplicate_after: int,
    candidate_index: dict[str, list[CandidatePaper]],
) -> dict[str, Any]:
    total_context_ids = set(contexts["citing_paper_id"].dropna().astype(str))
    covered_context_ids = total_context_ids & set(candidate_index)
    status_counts = (
        resolved["resolution_status"].value_counts(dropna=False).reset_index(name="rows")
    )
    status_counts = status_counts.rename(columns={"resolution_status": "status"})
    output_rows = len(resolved)
    metrics = {
        "total_input_contexts": int(len(contexts)),
        "output_rows": int(output_rows),
        "duplicate_context_id_before": duplicate_before,
        "duplicate_context_id_after": duplicate_after,
        "citing_paper_id_coverage_in_aligned_graph": _rate(
            len(covered_context_ids),
            len(total_context_ids),
        ),
        "resolution_status_distribution": _records(status_counts),
        "author_year_clear_rate": _status_rate(resolved, "author_year_clear"),
        "multi_candidate_ambiguous_rate": _status_rate(resolved, "multi_candidate_ambiguous"),
        "ambiguous_year_only_rate": _status_rate(resolved, "ambiguous_year_only"),
        "numeric_marker_unresolved_no_bibliography_rate": _status_rate(
            resolved,
            "numeric_marker_unresolved_no_bibliography",
        ),
        "bibliography_unresolved_rate": _status_rate(resolved, "bibliography_unresolved"),
        "resolved_cited_title_non_empty_rate": _rate(
            int(resolved["resolved_cited_title"].map(_clean_text_or_none).notna().sum()),
            output_rows,
        ),
        "samples": {
            "author_year_clear": _sample_status(resolved, "author_year_clear", 20),
            "multi_candidate_ambiguous": _sample_status(
                resolved,
                "multi_candidate_ambiguous",
                20,
            ),
            "unresolved_markers": _sample_unresolved(resolved, 20),
        },
        "common_failure_patterns": _failure_patterns(failures),
    }
    return metrics


def _sample_status(frame: pd.DataFrame, status: str, limit: int) -> list[dict[str, Any]]:
    return _sample_rows(frame.loc[frame["resolution_status"].eq(status)], limit)


def _sample_unresolved(frame: pd.DataFrame, limit: int) -> list[dict[str, Any]]:
    unresolved_statuses = [
        "bibliography_unresolved",
        "numeric_marker_unresolved_no_bibliography",
        "ambiguous_year_only",
        "citing_paper_not_in_aligned_graph",
    ]
    return _sample_rows(frame.loc[frame["resolution_status"].isin(unresolved_statuses)], limit)


def _sample_rows(frame: pd.DataFrame, limit: int) -> list[dict[str, Any]]:
    columns = [
        "context_id",
        "source_context_id",
        "citing_paper_id",
        "citation_marker",
        "marker_component_text",
        "parsed_surnames",
        "parsed_year",
        "resolved_cited_acl_id",
        "resolved_cited_title",
        "matched_candidate_count",
        "resolution_status",
        "resolution_confidence",
        "sentence_text",
    ]
    sample = frame[columns].head(limit).copy()
    for column in ("sentence_text", "resolved_cited_title"):
        sample[column] = sample[column].map(lambda value: _truncate(value, 180))
    return _records(sample)


def _failure_patterns(failures: pd.DataFrame) -> list[dict[str, Any]]:
    if failures.empty:
        return []
    grouped = (
        failures.groupby(["resolution_status", "resolution_method"], dropna=False)
        .size()
        .reset_index(name="rows")
        .sort_values("rows", ascending=False)
        .head(20)
    )
    return _records(grouped)


def _status_rate(frame: pd.DataFrame, status: str) -> str:
    return _rate(int(frame["resolution_status"].eq(status).sum()), len(frame))


def _parsed_surnames(text: str) -> list[str]:
    cleaned = re.sub(r"\bet\s+al\.?\b", " ", text, flags=re.IGNORECASE)
    cleaned = FILLER_RE.sub(" ", cleaned)
    cleaned = cleaned.replace("&", " and ")
    cleaned = re.sub(r"\([^)]*\)", " ", cleaned)
    pieces = re.split(r"\band\b|,", cleaned, flags=re.IGNORECASE)
    surnames = []
    for piece in pieces:
        surname = _normalize_name(piece)
        if surname and surname not in surnames:
            surnames.append(surname)
    return surnames


def _candidate_surnames(authors: Any) -> list[str]:
    text = _clean_text_or_none(authors)
    if text is None:
        return []
    text = text.replace("\n", " ")
    pieces = re.split(r"\s+and\s+", text)
    surnames = []
    for piece in pieces:
        surname_source = piece.split(",", maxsplit=1)[0] if "," in piece else piece.split()[0]
        surname = _normalize_name(surname_source)
        if surname and surname not in surnames:
            surnames.append(surname)
    return surnames


def _normalize_name(text: Any) -> str | None:
    value = _clean_text_or_none(text)
    if value is None:
        return None
    value = value.replace("{", "").replace("}", "")
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = re.sub(r"[^A-Za-z\s-]", " ", value)
    value = re.sub(r"[-\s]+", " ", value).strip().lower()
    if not value:
        return None
    return value.split()[0]


def _strip_outer_parens(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("(") and stripped.endswith(")"):
        return stripped[1:-1].strip()
    return stripped


def _resolved_context_id(
    *,
    source_context_id: str,
    row_number: int,
    component_index: int,
    resolution_status: str,
    matched_candidate_acl_ids: str,
) -> str:
    payload = "\x1f".join(
        [
            source_context_id,
            str(row_number),
            str(component_index),
            resolution_status,
            matched_candidate_acl_ids,
        ]
    )
    return f"ctxr_{hashlib.sha256(payload.encode('utf-8')).hexdigest()[:20]}"


def _ensure_columns(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        if column not in frame:
            frame[column] = None
    return frame[columns].copy()


def _year_string(value: Any) -> str | None:
    text = _clean_text_or_none(value)
    if text is None:
        return None
    match = YEAR_RE.search(text)
    return match.group(1) if match else None


def _int_or_none(value: Any) -> int | None:
    if value is None or pd.isna(value):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _clean_text(value: Any) -> str:
    return _clean_text_or_none(value) or ""


def _clean_text_or_none(value: Any) -> str | None:
    if value is None or pd.isna(value):
        return None
    text = re.sub(r"\s+", " ", str(value)).strip()
    return text or None


def _rate(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.000"
    return f"{numerator / denominator:.3f}"


def _records(frame: pd.DataFrame) -> list[dict[str, Any]]:
    if frame.empty:
        return []
    clean = frame.where(pd.notna(frame), None)
    return [
        {key: _json_value(value) for key, value in row.items()}
        for row in clean.to_dict(orient="records")
    ]


def _json_value(value: Any) -> Any:
    if value is None or pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def _truncate(value: Any, max_chars: int) -> str:
    text = _clean_text_or_none(value) or ""
    if len(text) <= max_chars:
        return text
    return f"{text[: max_chars - 3]}..."


def _table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "No records available."
    columns = list(dict.fromkeys(column for row in rows for column in row))
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = [_markdown_cell(row.get(column)) for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def _markdown_cell(value: Any) -> str:
    if value is None or pd.isna(value):
        return "unavailable"
    return _truncate(value, 140).replace("|", "\\|")
