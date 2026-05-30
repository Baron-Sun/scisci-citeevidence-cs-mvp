from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from citeevidence.contexts.resolve import OUTPUT_COLUMNS

DEFAULT_FINAL_RESOLVED_AUDIT_REPORT = Path("reports/final_resolved_context_audit.md")
DEFAULT_FINAL_RESOLVED_FLAGS_PATH = Path(
    "data/processed/final_resolved_context_quality_flags.parquet"
)
DEFAULT_STRONG_RESOLVED_SAMPLE_PATH = Path("data/processed/strong_resolved_contexts_sample.csv")
DEFAULT_MANUAL_RESOLUTION_SAMPLE_PATH = Path(
    "data/processed/manual_resolution_review_sample.csv"
)
DEFAULT_ANALYSIS_READY_STRONG_CONTEXTS_PATH = Path(
    "data/processed/analysis_ready_strong_contexts.parquet"
)

EXCLUDED_ANALYSIS_SECTIONS = {"references", "acknowledgement", "appendix"}
FLAG_COLUMNS = [
    "duplicate_context_id",
    "missing_context_window",
    "marker_not_in_sentence",
    "sentence_not_in_context_window",
    "strong_missing_resolved_title",
    "strong_missing_resolved_year",
    "strong_missing_resolved_authors",
    "strong_numeric_marker",
    "strong_year_only_marker",
    "strong_suspicious_citation_range",
    "strong_large_citation_group",
    "section_missing",
    "normalized_section_unknown",
    "strong_in_references_section",
    "strong_in_acknowledgement_section",
    "strong_in_appendix_section",
    "author_year_clear_not_strong",
]
FLAG_ID_COLUMNS = [
    "context_id",
    "source_context_id",
    "citing_paper_id",
    "raw_section_name",
    "normalized_section",
    "citation_marker",
    "marker_component_text",
    "marker_type",
    "resolution_status",
    "resolution_level",
    "is_strongly_resolved",
]
STRONG_SAMPLE_COLUMNS = [
    "context_id",
    "source_context_id",
    "citing_paper_id",
    "raw_section_name",
    "normalized_section",
    "citation_marker",
    "marker_component_text",
    "sentence_text",
    "context_window_s3",
    "resolved_cited_acl_id",
    "resolved_cited_title",
    "resolved_cited_year",
    "resolved_cited_authors",
    "resolution_status",
    "resolution_confidence",
    "reviewer_correct",
    "reviewer_notes",
]
MANUAL_SAMPLE_COLUMNS = [
    "review_bucket",
    "context_id",
    "source_context_id",
    "citing_paper_id",
    "raw_section_name",
    "normalized_section",
    "citation_marker",
    "marker_component_text",
    "marker_type",
    "parsed_surnames",
    "parsed_year",
    "sentence_text",
    "context_window_s3",
    "resolved_cited_acl_id",
    "resolved_cited_title",
    "resolved_cited_year",
    "resolved_cited_authors",
    "matched_candidate_acl_ids",
    "matched_candidate_count",
    "resolution_status",
    "resolution_level",
    "resolution_confidence",
    "reviewer_correct",
    "reviewer_notes",
]
REPORT_SAMPLE_COLUMNS = [
    "context_id",
    "source_context_id",
    "citing_paper_id",
    "normalized_section",
    "citation_marker",
    "marker_component_text",
    "marker_type",
    "resolution_status",
    "resolution_level",
    "is_strongly_resolved",
    "resolved_cited_title",
    "sentence_text",
]


def audit_final_resolved_contexts(
    *,
    resolved_path: str | Path,
    out_report: str | Path = DEFAULT_FINAL_RESOLVED_AUDIT_REPORT,
    flags_path: str | Path = DEFAULT_FINAL_RESOLVED_FLAGS_PATH,
    strong_sample_path: str | Path = DEFAULT_STRONG_RESOLVED_SAMPLE_PATH,
    manual_sample_path: str | Path = DEFAULT_MANUAL_RESOLUTION_SAMPLE_PATH,
    analysis_ready_path: str | Path = DEFAULT_ANALYSIS_READY_STRONG_CONTEXTS_PATH,
    random_seed: int = 13,
) -> dict[str, Any]:
    """Audit final resolved citation contexts and create analysis-ready outputs."""
    resolved_input = Path(resolved_path)
    if not resolved_input.exists():
        raise FileNotFoundError(f"Resolved contexts file does not exist: {resolved_input}")

    resolved = _ensure_columns(pd.read_parquet(resolved_input), OUTPUT_COLUMNS)
    flags = build_final_resolved_quality_flags(resolved)

    flags_output = Path(flags_path)
    flags_output.parent.mkdir(parents=True, exist_ok=True)
    flags.to_parquet(flags_output, index=False)

    analysis_ready = build_analysis_ready_strong_contexts(resolved)
    analysis_ready_output = Path(analysis_ready_path)
    analysis_ready_output.parent.mkdir(parents=True, exist_ok=True)
    analysis_ready.to_parquet(analysis_ready_output, index=False)

    strong_sample = build_strong_resolved_sample(resolved, sample_size=300, seed=random_seed)
    strong_sample_output = Path(strong_sample_path)
    strong_sample_output.parent.mkdir(parents=True, exist_ok=True)
    strong_sample.to_csv(strong_sample_output, index=False)

    manual_sample = build_manual_resolution_review_sample(resolved, seed=random_seed)
    manual_sample_output = Path(manual_sample_path)
    manual_sample_output.parent.mkdir(parents=True, exist_ok=True)
    manual_sample.to_csv(manual_sample_output, index=False)

    metrics = build_final_resolved_metrics(
        resolved=resolved,
        flags=flags,
        analysis_ready=analysis_ready,
        manual_sample=manual_sample,
    )
    report = build_final_resolved_audit_report(
        metrics=metrics,
        resolved=resolved,
        flags=flags,
        resolved_path=resolved_input,
        flags_path=flags_output,
        strong_sample_path=strong_sample_output,
        manual_sample_path=manual_sample_output,
        analysis_ready_path=analysis_ready_output,
    )
    report_output = Path(out_report)
    report_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.write_text(report, encoding="utf-8")
    return metrics


def build_final_resolved_quality_flags(resolved: pd.DataFrame) -> pd.DataFrame:
    """Build row-level quality flags for final resolved contexts."""
    frame = _ensure_columns(resolved.copy(), OUTPUT_COLUMNS)
    strong = _bool_series(frame["is_strongly_resolved"])
    normalized_section = frame["normalized_section"].map(_clean_lower)
    marker_type = frame["marker_type"].map(_clean_lower)
    status = frame["resolution_status"].map(_clean_lower)
    context_window = frame["context_window_s3"].fillna("").astype(str)
    sentence = frame["sentence_text"].fillna("").astype(str)
    marker = frame["citation_marker"].fillna("").astype(str)

    flags = frame[FLAG_ID_COLUMNS].copy()
    flags["duplicate_context_id"] = frame["context_id"].duplicated(keep=False)
    flags["missing_context_window"] = _missing_mask(frame["context_window_s3"])
    flags["marker_not_in_sentence"] = [
        bool(mark.strip()) and bool(sent.strip()) and mark not in sent
        for mark, sent in zip(marker, sentence, strict=True)
    ]
    flags["sentence_not_in_context_window"] = [
        bool(sent.strip()) and bool(window.strip()) and sent not in window
        for sent, window in zip(sentence, context_window, strict=True)
    ]
    flags["strong_missing_resolved_title"] = strong & _missing_mask(
        frame["resolved_cited_title"]
    )
    flags["strong_missing_resolved_year"] = strong & _missing_mask(frame["resolved_cited_year"])
    flags["strong_missing_resolved_authors"] = strong & _missing_mask(
        frame["resolved_cited_authors"]
    )
    flags["strong_numeric_marker"] = strong & marker_type.eq("numeric")
    flags["strong_year_only_marker"] = strong & marker_type.eq("year_only")
    flags["strong_suspicious_citation_range"] = strong & _bool_series(
        frame["suspicious_citation_range_flag"]
    )
    flags["strong_large_citation_group"] = strong & _bool_series(frame["large_citation_group_flag"])
    flags["section_missing"] = _missing_mask(frame["raw_section_name"]) & _missing_mask(
        frame["section"]
    )
    flags["normalized_section_unknown"] = normalized_section.isin({"", "unknown", "unavailable"})
    flags["strong_in_references_section"] = strong & normalized_section.eq("references")
    flags["strong_in_acknowledgement_section"] = strong & normalized_section.eq(
        "acknowledgement"
    )
    flags["strong_in_appendix_section"] = strong & normalized_section.eq("appendix")
    flags["author_year_clear_not_strong"] = status.eq("author_year_clear") & ~strong
    flags["flag_any"] = flags[FLAG_COLUMNS].any(axis=1)
    return flags


def build_analysis_ready_strong_contexts(resolved: pd.DataFrame) -> pd.DataFrame:
    """Filter final resolved rows to the default strong-evidence analysis input."""
    frame = _ensure_columns(resolved.copy(), OUTPUT_COLUMNS)
    strong = _bool_series(frame["is_strongly_resolved"])
    normalized_section = frame["normalized_section"].map(_clean_lower)
    marker_type = frame["marker_type"].map(_clean_lower)
    eligible = (
        strong
        & ~normalized_section.isin(EXCLUDED_ANALYSIS_SECTIONS)
        & ~marker_type.isin({"numeric", "year_only"})
        & ~_bool_series(frame["suspicious_citation_range_flag"])
        & ~_bool_series(frame["large_citation_group_flag"])
        & ~_missing_mask(frame["resolved_cited_title"])
        & ~_missing_mask(frame["context_window_s3"])
    )
    return frame.loc[eligible].copy()


def build_strong_resolved_sample(
    resolved: pd.DataFrame,
    *,
    sample_size: int,
    seed: int,
) -> pd.DataFrame:
    """Create a deterministic section-stratified strong-row review sample."""
    frame = _ensure_columns(resolved.copy(), OUTPUT_COLUMNS)
    strong = frame.loc[_bool_series(frame["is_strongly_resolved"])].copy()
    sample = _stratified_sample(strong, "normalized_section", sample_size, seed)
    sample = _ensure_columns(sample, STRONG_SAMPLE_COLUMNS)
    sample["reviewer_correct"] = ""
    sample["reviewer_notes"] = ""
    return sample[STRONG_SAMPLE_COLUMNS]


def build_manual_resolution_review_sample(
    resolved: pd.DataFrame,
    *,
    seed: int,
) -> pd.DataFrame:
    """Create the mixed manual review sample requested for final resolution audit."""
    frame = _ensure_columns(resolved.copy(), OUTPUT_COLUMNS)
    buckets = [
        (
            "strong_author_year",
            frame["resolution_level"].map(_clean_lower).eq("strong_author_year"),
            200,
        ),
        (
            "bibliography_unresolved",
            frame["resolution_status"].map(_clean_lower).eq("bibliography_unresolved"),
            100,
        ),
        (
            "multi_candidate_ambiguous",
            frame["resolution_status"].map(_clean_lower).eq("multi_candidate_ambiguous"),
            75,
        ),
        (
            "numeric_unresolved",
            frame["resolution_level"].map(_clean_lower).eq("numeric_unresolved"),
            75,
        ),
        (
            "weak_year_or_nonfirst_author",
            frame["resolution_level"]
            .map(_clean_lower)
            .isin({"weak_year_only", "weak_nonfirst_author"}),
            50,
        ),
    ]
    samples = []
    for index, (bucket, mask, requested) in enumerate(buckets):
        sample = _sample_rows(frame.loc[mask], requested, seed + index)
        sample = sample.copy()
        sample["review_bucket"] = bucket
        samples.append(sample)
    if samples:
        combined = pd.concat(samples, ignore_index=True)
    else:
        combined = pd.DataFrame(columns=OUTPUT_COLUMNS)
    combined = _ensure_columns(combined, MANUAL_SAMPLE_COLUMNS)
    combined["reviewer_correct"] = ""
    combined["reviewer_notes"] = ""
    return combined[MANUAL_SAMPLE_COLUMNS]


def build_final_resolved_metrics(
    *,
    resolved: pd.DataFrame,
    flags: pd.DataFrame,
    analysis_ready: pd.DataFrame,
    manual_sample: pd.DataFrame,
) -> dict[str, Any]:
    """Build report metrics for the final resolved audit."""
    frame = _ensure_columns(resolved.copy(), OUTPUT_COLUMNS)
    strong = frame.loc[_bool_series(frame["is_strongly_resolved"])].copy()
    total = len(frame)
    duplicate_context_id_count = int(total - frame["context_id"].nunique(dropna=True))
    flag_any = _bool_series(flags["flag_any"]) if "flag_any" in flags else pd.Series([], dtype=bool)
    flagged_strong = flags.loc[
        flag_any & _bool_series(flags["is_strongly_resolved"])
    ].shape[0]
    return {
        "total_rows": total,
        "unique_source_context_id": int(frame["source_context_id"].nunique(dropna=True)),
        "unique_context_id": int(frame["context_id"].nunique(dropna=True)),
        "duplicate_context_id_count": duplicate_context_id_count,
        "is_strongly_resolved_count": int(strong.shape[0]),
        "is_strongly_resolved_rate": _rate(int(strong.shape[0]), total),
        "strong_resolved_cited_title_non_empty_rate": _non_empty_rate(
            strong,
            "resolved_cited_title",
        ),
        "strong_resolved_cited_year_non_empty_rate": _non_empty_rate(
            strong,
            "resolved_cited_year",
        ),
        "strong_resolved_cited_authors_non_empty_rate": _non_empty_rate(
            strong,
            "resolved_cited_authors",
        ),
        "raw_section_name_coverage": _non_empty_rate(frame, "raw_section_name"),
        "citation_marker_in_sentence_rate": _substring_rate(
            frame["citation_marker"],
            frame["sentence_text"],
        ),
        "sentence_text_in_context_window_s3_rate": _substring_rate(
            frame["sentence_text"],
            frame["context_window_s3"],
        ),
        "flagged_rows_that_are_strong": int(flagged_strong),
        "analysis_ready_rows": int(len(analysis_ready)),
        "manual_sample_counts": _value_counts(manual_sample, ["review_bucket"], "rows"),
        "marker_type_distribution": _value_counts(frame, ["marker_type"], "rows"),
        "resolution_status_distribution": _value_counts(
            frame,
            ["resolution_status"],
            "rows",
        ),
        "resolution_level_distribution": _value_counts(frame, ["resolution_level"], "rows"),
        "normalized_section_distribution": _value_counts(
            frame,
            ["normalized_section"],
            "rows",
        ),
        "strong_rows_by_normalized_section": _value_counts(
            strong,
            ["normalized_section"],
            "strong_rows",
        ),
        "unresolved_rows_by_normalized_section": _value_counts(
            frame.loc[~_bool_series(frame["is_strongly_resolved"])],
            ["normalized_section"],
            "unresolved_rows",
        ),
        "analysis_ready_rows_by_normalized_section": _value_counts(
            analysis_ready,
            ["normalized_section"],
            "analysis_ready_rows",
        ),
        "large_citation_group_flag_counts": _flag_value_counts(
            frame,
            "large_citation_group_flag",
        ),
        "very_large_citation_group_flag_counts": _flag_value_counts(
            frame,
            "very_large_citation_group_flag",
        ),
        "suspicious_citation_range_flag_counts": _flag_value_counts(
            frame,
            "suspicious_citation_range_flag",
        ),
        "quality_flag_summary": _flag_summary(flags),
        "top_unresolved_failure_modes": _top_unresolved_failure_modes(frame),
        "special_check_counts": _special_check_counts(flags),
    }


def build_final_resolved_audit_report(
    *,
    metrics: dict[str, Any],
    resolved: pd.DataFrame,
    flags: pd.DataFrame,
    resolved_path: Path,
    flags_path: Path,
    strong_sample_path: Path,
    manual_sample_path: Path,
    analysis_ready_path: Path,
) -> str:
    """Build the markdown final audit report."""
    core_rows = pd.DataFrame(
        [
            {"metric": "total rows", "value": metrics["total_rows"]},
            {"metric": "unique source_context_id", "value": metrics["unique_source_context_id"]},
            {"metric": "unique context_id", "value": metrics["unique_context_id"]},
            {
                "metric": "duplicate context_id count",
                "value": metrics["duplicate_context_id_count"],
            },
            {
                "metric": "is_strongly_resolved count",
                "value": metrics["is_strongly_resolved_count"],
            },
            {
                "metric": "is_strongly_resolved rate",
                "value": metrics["is_strongly_resolved_rate"],
            },
            {
                "metric": "resolved_cited_title non-empty rate for strong rows",
                "value": metrics["strong_resolved_cited_title_non_empty_rate"],
            },
            {
                "metric": "resolved_cited_year non-empty rate for strong rows",
                "value": metrics["strong_resolved_cited_year_non_empty_rate"],
            },
            {
                "metric": "resolved_cited_authors non-empty rate for strong rows",
                "value": metrics["strong_resolved_cited_authors_non_empty_rate"],
            },
            {"metric": "raw_section_name coverage", "value": metrics["raw_section_name_coverage"]},
            {
                "metric": "citation_marker in sentence_text rate",
                "value": metrics["citation_marker_in_sentence_rate"],
            },
            {
                "metric": "sentence_text in context_window_s3 rate",
                "value": metrics["sentence_text_in_context_window_s3_rate"],
            },
            {
                "metric": "flagged rows that are also is_strongly_resolved",
                "value": metrics["flagged_rows_that_are_strong"],
            },
            {
                "metric": "analysis_ready_strong_contexts rows",
                "value": metrics["analysis_ready_rows"],
            },
        ]
    )
    lines = [
        "# Final Resolved Citation Context Audit",
        "",
        "## Inputs",
        f"- Resolved contexts: `{resolved_path}`",
        "",
        "## Outputs",
        f"- Quality flags: `{flags_path}`",
        f"- Strong resolved review sample: `{strong_sample_path}`",
        f"- Manual resolution review sample: `{manual_sample_path}`",
        f"- Analysis-ready strong contexts: `{analysis_ready_path}`",
        "",
        "## Core Metrics",
        _table(core_rows),
        "",
        "## Marker Type Distribution",
        _table(metrics["marker_type_distribution"]),
        "",
        "## Resolution Status Distribution",
        _table(metrics["resolution_status_distribution"]),
        "",
        "## Resolution Level Distribution",
        _table(metrics["resolution_level_distribution"]),
        "",
        "## Normalized Section Distribution",
        _table(metrics["normalized_section_distribution"]),
        "",
        "## Strong Rows By Normalized Section",
        _table(metrics["strong_rows_by_normalized_section"]),
        "",
        "## Unresolved Rows By Normalized Section",
        _table(metrics["unresolved_rows_by_normalized_section"]),
        "",
        "## Analysis-Ready Rows By Normalized Section",
        _table(metrics["analysis_ready_rows_by_normalized_section"]),
        "",
        "## Citation Group And Range Flags",
        "### large_citation_group_flag",
        _table(metrics["large_citation_group_flag_counts"]),
        "",
        "### very_large_citation_group_flag",
        _table(metrics["very_large_citation_group_flag_counts"]),
        "",
        "### suspicious_citation_range_flag",
        _table(metrics["suspicious_citation_range_flag_counts"]),
        "",
        "## Quality Flag Summary",
        _table(metrics["quality_flag_summary"]),
        "",
        "## Special Consistency Checks",
        _table(metrics["special_check_counts"]),
        "",
        "Rows with `resolution_status = author_year_clear` are strong only when the marker "
        "is not numeric or year-only, `suspicious_citation_range_flag` is false, and the "
        "resolver assigns `resolution_level = strong_author_year`.",
        "",
        "## Top Unresolved Failure Modes",
        _table(metrics["top_unresolved_failure_modes"]),
        "",
        "## Manual Review Sampling Counts",
        _table(metrics["manual_sample_counts"]),
        "",
        "## Examples: author_year_clear_not_strong",
        _table(
            _sample_with_reason(
                resolved,
                flags,
                "author_year_clear_not_strong",
                20,
            )
        ),
        "",
        "## Examples: strong_in_references_section",
        _table(_sample_flagged(resolved, flags, "strong_in_references_section", 10)),
        "",
        "## Examples: strong_in_acknowledgement_section",
        _table(_sample_flagged(resolved, flags, "strong_in_acknowledgement_section", 10)),
        "",
        "## Examples: strong_in_appendix_section",
        _table(_sample_flagged(resolved, flags, "strong_in_appendix_section", 10)),
        "",
        "## Random Examples By Resolution Level",
        _table(_examples_by_resolution_level(resolved, per_level=5, seed=13)),
        "",
    ]
    return "\n".join(lines)


def _special_check_counts(flags: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for column in [
        "author_year_clear_not_strong",
        "strong_in_references_section",
        "strong_in_acknowledgement_section",
        "strong_in_appendix_section",
        "strong_numeric_marker",
        "strong_year_only_marker",
        "strong_suspicious_citation_range",
        "strong_large_citation_group",
    ]:
        rows.append({"check": column, "rows": int(flags[column].sum())})
    return pd.DataFrame(rows)


def _sample_with_reason(
    resolved: pd.DataFrame,
    flags: pd.DataFrame,
    flag_column: str,
    limit: int,
) -> pd.DataFrame:
    sample = _sample_flagged(resolved, flags, flag_column, limit)
    if sample.empty:
        return sample.assign(exclusion_reason=pd.Series(dtype="object"))
    sample["exclusion_reason"] = sample.apply(_not_strong_reason, axis=1)
    return sample


def _sample_flagged(
    resolved: pd.DataFrame,
    flags: pd.DataFrame,
    flag_column: str,
    limit: int,
) -> pd.DataFrame:
    if flags.empty or flag_column not in flags:
        return pd.DataFrame(columns=REPORT_SAMPLE_COLUMNS)
    frame = _ensure_columns(resolved.copy(), OUTPUT_COLUMNS)
    sample = frame.loc[_bool_series(flags[flag_column])].head(limit).copy()
    return _report_sample_columns(sample)


def _examples_by_resolution_level(
    resolved: pd.DataFrame,
    *,
    per_level: int,
    seed: int,
) -> pd.DataFrame:
    if resolved.empty:
        return pd.DataFrame(columns=["example_bucket", *REPORT_SAMPLE_COLUMNS])
    samples = []
    for index, (level, group) in enumerate(
        resolved.groupby(resolved["resolution_level"].fillna("unavailable"), dropna=False)
    ):
        sample = _sample_rows(group, per_level, seed + index)
        sample = _report_sample_columns(sample)
        sample.insert(0, "example_bucket", str(level))
        samples.append(sample)
    if not samples:
        return pd.DataFrame(columns=["example_bucket", *REPORT_SAMPLE_COLUMNS])
    return pd.concat(samples, ignore_index=True)


def _top_unresolved_failure_modes(frame: pd.DataFrame) -> pd.DataFrame:
    non_strong = frame.loc[~_bool_series(frame["is_strongly_resolved"])].copy()
    if non_strong.empty:
        return pd.DataFrame(columns=["resolution_level", "resolution_status", "rows"])
    return (
        non_strong.assign(
            resolution_level=non_strong["resolution_level"].fillna("unavailable"),
            resolution_status=non_strong["resolution_status"].fillna("unavailable"),
        )
        .groupby(["resolution_level", "resolution_status"], dropna=False)
        .size()
        .reset_index(name="rows")
        .sort_values("rows", ascending=False)
    )


def _flag_summary(flags: pd.DataFrame) -> pd.DataFrame:
    if flags.empty:
        return pd.DataFrame(columns=["flag", "rows", "rate"])
    total = len(flags)
    rows = []
    for column in FLAG_COLUMNS:
        count = int(flags[column].sum())
        rows.append({"flag": column, "rows": count, "rate": _rate(count, total)})
    rows.append(
        {
            "flag": "flag_any",
            "rows": int(flags["flag_any"].sum()),
            "rate": _rate(int(flags["flag_any"].sum()), total),
        }
    )
    return pd.DataFrame(rows)


def _flag_value_counts(frame: pd.DataFrame, column: str) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(columns=[column, "rows"])
    counts = (
        _bool_series(frame[column])
        .value_counts(dropna=False)
        .rename_axis(column)
        .reset_index(name="rows")
    )
    return counts.sort_values("rows", ascending=False)


def _value_counts(df: pd.DataFrame, columns: list[str], count_name: str) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=[*columns, count_name])
    filled = df.copy()
    for column in columns:
        filled[column] = filled[column].fillna("unavailable").astype(str)
    return (
        filled.groupby(columns, dropna=False)
        .size()
        .reset_index(name=count_name)
        .sort_values([count_name, *columns], ascending=[False, *([True] * len(columns))])
    )


def _stratified_sample(
    frame: pd.DataFrame,
    column: str,
    sample_size: int,
    seed: int,
) -> pd.DataFrame:
    if frame.empty or sample_size <= 0:
        return pd.DataFrame(columns=frame.columns)
    if len(frame) <= sample_size:
        return frame.sample(frac=1, random_state=seed).reset_index(drop=True)
    grouped = list(frame.groupby(frame[column].fillna("unavailable"), dropna=False))
    total = len(frame)
    quotas = []
    for label, group in grouped:
        exact = len(group) / total * sample_size
        quota = max(1, int(exact))
        quotas.append({"label": label, "rows": group, "quota": quota, "remainder": exact % 1})

    while sum(int(item["quota"]) for item in quotas) > sample_size:
        removable = [item for item in quotas if int(item["quota"]) > 1]
        if not removable:
            break
        target = min(removable, key=lambda item: (float(item["remainder"]), int(item["quota"])))
        target["quota"] = int(target["quota"]) - 1

    while sum(int(item["quota"]) for item in quotas) < sample_size:
        target = max(quotas, key=lambda item: float(item["remainder"]))
        target["quota"] = int(target["quota"]) + 1

    samples = []
    for index, item in enumerate(quotas):
        group = item["rows"]
        quota = min(int(item["quota"]), len(group))
        samples.append(group.sample(n=quota, random_state=seed + index))
    return pd.concat(samples, ignore_index=True)


def _sample_rows(frame: pd.DataFrame, n: int, seed: int) -> pd.DataFrame:
    if frame.empty or n <= 0:
        return pd.DataFrame(columns=frame.columns)
    if len(frame) <= n:
        return frame.sample(frac=1, random_state=seed).reset_index(drop=True)
    return frame.sample(n=n, random_state=seed).reset_index(drop=True)


def _report_sample_columns(frame: pd.DataFrame) -> pd.DataFrame:
    sample = _ensure_columns(frame.copy(), REPORT_SAMPLE_COLUMNS)
    sample = sample[REPORT_SAMPLE_COLUMNS].copy()
    for column in ("sentence_text", "resolved_cited_title"):
        sample[column] = sample[column].map(lambda value: _truncate(value, 180))
    return sample


def _not_strong_reason(row: pd.Series) -> str:
    reasons = []
    marker_type = _clean_lower(row.get("marker_type"))
    if marker_type in {"numeric", "year_only"}:
        reasons.append(f"marker_type={marker_type}")
    if _bool_value(row.get("suspicious_citation_range_flag")):
        reasons.append("suspicious_citation_range_flag=true")
    if _clean_lower(row.get("resolution_level")) != "strong_author_year":
        reasons.append(f"resolution_level={row.get('resolution_level')}")
    if not reasons:
        reasons.append("is_strongly_resolved=false")
    return "; ".join(reasons)


def _substring_rate(needles: pd.Series, haystacks: pd.Series) -> str:
    passed = 0
    total = len(needles)
    for needle, haystack in zip(
        needles.fillna("").astype(str),
        haystacks.fillna("").astype(str),
        strict=True,
    ):
        if needle.strip() and haystack.strip() and needle in haystack:
            passed += 1
    return _rate(passed, total)


def _non_empty_rate(frame: pd.DataFrame, column: str) -> str:
    if frame.empty or column not in frame:
        return "0.000"
    return _rate(int((~_missing_mask(frame[column])).sum()), len(frame))


def _missing_mask(series: pd.Series) -> pd.Series:
    return series.isna() | series.astype("string").str.strip().fillna("").eq("")


def _bool_series(series: pd.Series) -> pd.Series:
    return series.map(_bool_value).fillna(False).astype(bool)


def _bool_value(value: Any) -> bool:
    if value is None or pd.isna(value):
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def _clean_lower(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value).strip().lower()


def _ensure_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        if column not in df.columns:
            df[column] = None
    return df


def _rate(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.000"
    return f"{numerator / denominator:.3f}"


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
