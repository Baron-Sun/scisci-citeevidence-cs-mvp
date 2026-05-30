from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

DEFAULT_MANUAL_REVIEW_REPORT = Path("reports/manual_resolution_review_report.md")
DEFAULT_MANUAL_REVIEW_CLEAN_PATH = Path("data/processed/manual_resolution_review_clean.parquet")
DEFAULT_MANUAL_REVIEW_NEEDS_CHECK_PATH = Path(
    "data/processed/manual_resolution_review_needs_check.csv"
)

REQUIRED_REVIEWER_COLUMNS = ["reviewer_correct", "reviewer_notes"]
OPTIONAL_REVIEWER_COLUMNS = [
    "reviewer_error_type",
    "reviewer_corrected_cited_title",
    "reviewer_corrected_cited_acl_id",
]
ALLOWED_REVIEW_VALUES = {"", "true", "false", "unclear"}
IDENTITY_COLUMNS = ["context_id", "source_context_id"]
REPORT_EXAMPLE_COLUMNS = [
    "review_sample_source",
    "review_bucket",
    "context_id",
    "source_context_id",
    "citing_paper_id",
    "normalized_section",
    "marker_type",
    "citation_marker",
    "marker_component_text",
    "resolved_cited_title",
    "resolution_status",
    "resolution_level",
    "reviewer_correct",
    "reviewer_notes",
    "reviewer_error_type",
    "needs_check_reason",
]


def ingest_manual_resolution_review(
    *,
    strong_sample_path: str | Path,
    manual_sample_path: str | Path,
    out_path: str | Path = DEFAULT_MANUAL_REVIEW_CLEAN_PATH,
    needs_check_path: str | Path = DEFAULT_MANUAL_REVIEW_NEEDS_CHECK_PATH,
    report_path: str | Path = DEFAULT_MANUAL_REVIEW_REPORT,
) -> dict[str, Any]:
    """Ingest manual resolution review CSVs and write clean data plus a report."""
    strong_input = _prefer_completed_path(Path(strong_sample_path))
    manual_input = _prefer_completed_path(Path(manual_sample_path))
    for path in (strong_input, manual_input):
        if not path.exists():
            raise FileNotFoundError(f"Manual review input does not exist: {path}")

    strong = _read_review_csv(strong_input, sample_source="strong_sample")
    manual = _read_review_csv(manual_input, sample_source="manual_sample")
    review = normalize_review_frame(pd.concat([strong, manual], ignore_index=True))

    clean_output = Path(out_path)
    clean_output.parent.mkdir(parents=True, exist_ok=True)
    review.to_parquet(clean_output, index=False)

    needs_check = review.loc[review["needs_check"]].copy()
    needs_check_output = Path(needs_check_path)
    needs_check_output.parent.mkdir(parents=True, exist_ok=True)
    needs_check.to_csv(needs_check_output, index=False)

    metrics = build_manual_review_metrics(review)
    report = build_manual_review_report(
        review=review,
        needs_check=needs_check,
        metrics=metrics,
        strong_input=strong_input,
        manual_input=manual_input,
        clean_output=clean_output,
        needs_check_output=needs_check_output,
    )
    report_output = Path(report_path)
    report_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.write_text(report, encoding="utf-8")
    return metrics


def normalize_review_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize reviewer fields and add validation columns."""
    review = frame.copy()
    for column in [*REQUIRED_REVIEWER_COLUMNS, *OPTIONAL_REVIEWER_COLUMNS, *IDENTITY_COLUMNS]:
        if column not in review.columns:
            review[column] = ""
    review["reviewer_correct_raw"] = review["reviewer_correct"].fillna("").astype(str)
    review["reviewer_correct"] = review["reviewer_correct_raw"].map(_normalize_review_value)
    review["reviewer_notes"] = review["reviewer_notes"].fillna("").astype(str).str.strip()
    for column in OPTIONAL_REVIEWER_COLUMNS:
        review[column] = review[column].fillna("").astype(str).str.strip()

    valid = review["reviewer_correct"].isin(ALLOWED_REVIEW_VALUES)
    reviewed = valid & review["reviewer_correct"].isin({"true", "false", "unclear"})
    precision_eligible = valid & review["reviewer_correct"].isin({"true", "false"})
    false_without_notes = review["reviewer_correct"].eq("false") & review["reviewer_notes"].eq("")

    review["valid_reviewer_correct"] = valid
    review["is_reviewed"] = reviewed
    review["is_precision_eligible"] = precision_eligible
    review["review_is_correct"] = review["reviewer_correct"].eq("true")
    review["needs_check_reason"] = [
        _needs_check_reason(is_valid, correct, has_missing_notes)
        for is_valid, correct, has_missing_notes in zip(
            valid,
            review["reviewer_correct"],
            false_without_notes,
            strict=True,
        )
    ]
    review["needs_check"] = review["needs_check_reason"].ne("")
    return review


def build_manual_review_metrics(review: pd.DataFrame) -> dict[str, Any]:
    """Build aggregate metrics for manual review reporting."""
    reviewed = review.loc[review["is_reviewed"]]
    unreviewed = review.loc[review["reviewer_correct"].eq("")]
    strong = review.loc[_is_strong_author_year(review)]
    reviewed_strong = strong.loc[strong["is_precision_eligible"]]
    return {
        "total_rows": int(len(review)),
        "reviewed_rows": int(len(reviewed)),
        "unreviewed_rows": int(len(unreviewed)),
        "invalid_reviewer_correct_rows": int((~review["valid_reviewer_correct"]).sum()),
        "needs_check_rows": int(review["needs_check"].sum()),
        "reviewed_strong_author_year_rows": int(len(reviewed_strong)),
        "precision_strong_author_year": _precision(reviewed_strong),
        "precision_by_normalized_section": _precision_by_group(review, "normalized_section"),
        "precision_by_marker_type": _precision_by_group(review, "marker_type"),
        "precision_by_resolution_status": _precision_by_group(review, "resolution_status"),
        "reviewer_error_type_counts": _value_counts(
            review.loc[review["reviewer_error_type"].ne("")],
            ["reviewer_error_type"],
            "rows",
        ),
        "review_value_counts": _value_counts(review, ["reviewer_correct"], "rows"),
        "sample_source_counts": _value_counts(review, ["review_sample_source"], "rows"),
    }


def build_manual_review_report(
    *,
    review: pd.DataFrame,
    needs_check: pd.DataFrame,
    metrics: dict[str, Any],
    strong_input: Path,
    manual_input: Path,
    clean_output: Path,
    needs_check_output: Path,
) -> str:
    """Build the manual resolution review markdown report."""
    core = pd.DataFrame(
        [
            {"metric": "total rows", "value": metrics["total_rows"]},
            {"metric": "reviewed rows", "value": metrics["reviewed_rows"]},
            {"metric": "unreviewed rows", "value": metrics["unreviewed_rows"]},
            {
                "metric": "invalid reviewer_correct rows",
                "value": metrics["invalid_reviewer_correct_rows"],
            },
            {"metric": "needs_check rows", "value": metrics["needs_check_rows"]},
            {
                "metric": "reviewed strong_author_year rows",
                "value": metrics["reviewed_strong_author_year_rows"],
            },
            {
                "metric": "precision among reviewed strong_author_year rows",
                "value": metrics["precision_strong_author_year"],
            },
        ]
    )
    false_or_unclear = review.loc[review["reviewer_correct"].isin({"false", "unclear"})]
    sections = [
        "# Manual Resolution Review Report",
        "",
        "## Inputs",
        f"- Strong sample: `{strong_input}`",
        f"- Manual mixed sample: `{manual_input}`",
        "",
        "## Outputs",
        f"- Clean review parquet: `{clean_output}`",
        f"- Needs-check CSV: `{needs_check_output}`",
        "",
        "## Core Metrics",
        _table(core),
        "",
        "## Review Value Counts",
        _table(metrics["review_value_counts"]),
        "",
        "## Sample Source Counts",
        _table(metrics["sample_source_counts"]),
        "",
        "## Precision By Normalized Section",
        _table(metrics["precision_by_normalized_section"]),
        "",
        "## Precision By Marker Type",
        _table(metrics["precision_by_marker_type"]),
        "",
        "## Precision By Resolution Status",
        _table(metrics["precision_by_resolution_status"]),
        "",
        "## Reviewer Error Type Counts",
        _table(metrics["reviewer_error_type_counts"]),
        "",
        "## Examples: False Or Unclear Rows",
        _table(_example_rows(false_or_unclear, 20)),
        "",
        "## Rows Needing Check",
        _table(_example_rows(needs_check, 20)),
        "",
        "## Recommendation",
        _recommendation(metrics),
        "",
    ]
    return "\n".join(sections)


def _read_review_csv(path: Path, *, sample_source: str) -> pd.DataFrame:
    frame = pd.read_csv(path, keep_default_na=False, dtype=str)
    frame["review_sample_source"] = sample_source
    frame["review_input_path"] = str(path)
    if "review_bucket" not in frame.columns:
        frame["review_bucket"] = sample_source
    return frame


def _prefer_completed_path(path: Path) -> Path:
    completed = path.with_name(f"{path.stem}_completed{path.suffix}")
    return completed if completed.exists() else path


def _normalize_review_value(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value).strip().lower()


def _needs_check_reason(is_valid: bool, reviewer_correct: str, false_without_notes: bool) -> str:
    reasons = []
    if not is_valid:
        reasons.append("invalid_reviewer_correct")
    if reviewer_correct == "false" and false_without_notes:
        reasons.append("false_without_reviewer_notes")
    return "; ".join(reasons)


def _is_strong_author_year(review: pd.DataFrame) -> pd.Series:
    resolution_level = _series_or_blank(review, "resolution_level").str.lower()
    resolution_status = _series_or_blank(review, "resolution_status").str.lower()
    sample_source = _series_or_blank(review, "review_sample_source").str.lower()
    return resolution_level.eq("strong_author_year") | (
        sample_source.eq("strong_sample") & resolution_status.eq("author_year_clear")
    )


def _precision(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "unavailable"
    correct = int(frame["reviewer_correct"].eq("true").sum())
    denominator = int(frame["reviewer_correct"].isin({"true", "false"}).sum())
    if denominator == 0:
        return "unavailable"
    return f"{correct / denominator:.3f}"


def _precision_by_group(review: pd.DataFrame, column: str) -> pd.DataFrame:
    empty_columns = [column, "reviewed_true_false", "correct", "incorrect", "precision"]
    if column not in review.columns:
        return pd.DataFrame(columns=empty_columns)
    eligible = review.loc[review["is_precision_eligible"]].copy()
    if eligible.empty:
        return pd.DataFrame(columns=empty_columns)
    eligible[column] = eligible[column].fillna("unavailable").astype(str)
    grouped = (
        eligible.assign(
            correct=eligible["reviewer_correct"].eq("true"),
            incorrect=eligible["reviewer_correct"].eq("false"),
        )
        .groupby(column, dropna=False)
        .agg(
            reviewed_true_false=("reviewer_correct", "size"),
            correct=("correct", "sum"),
            incorrect=("incorrect", "sum"),
        )
        .reset_index()
    )
    grouped["precision"] = grouped.apply(
        lambda row: _rate(int(row["correct"]), int(row["reviewed_true_false"])),
        axis=1,
    )
    return grouped.sort_values("reviewed_true_false", ascending=False)


def _value_counts(df: pd.DataFrame, columns: list[str], count_name: str) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=[*columns, count_name])
    filled = df.copy()
    for column in columns:
        if column not in filled.columns:
            filled[column] = "unavailable"
        filled[column] = filled[column].fillna("unavailable").astype(str)
        filled.loc[filled[column].str.strip().eq(""), column] = "blank"
    return (
        filled.groupby(columns, dropna=False)
        .size()
        .reset_index(name=count_name)
        .sort_values([count_name, *columns], ascending=[False, *([True] * len(columns))])
    )


def _example_rows(frame: pd.DataFrame, limit: int) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(columns=REPORT_EXAMPLE_COLUMNS)
    sample = _ensure_columns(frame.head(limit).copy(), REPORT_EXAMPLE_COLUMNS)
    sample = sample[REPORT_EXAMPLE_COLUMNS]
    for column in ("resolved_cited_title", "reviewer_notes"):
        sample[column] = sample[column].map(lambda value: _truncate(value, 160))
    return sample


def _recommendation(metrics: dict[str, Any]) -> str:
    reviewed = int(metrics["reviewed_strong_author_year_rows"])
    precision = metrics["precision_strong_author_year"]
    if reviewed == 0 or precision == "unavailable":
        return (
            "No reviewed true/false strong_author_year rows are available yet. "
            "The analysis-ready table can be used to develop downstream code, but a "
            "manual precision estimate should be completed before reporting final accuracy."
        )
    if float(precision) >= 0.95:
        return (
            "Reviewed strong_author_year precision is high enough to proceed with "
            "object matching and citation-function labeling, while continuing to track "
            "any reviewer-noted error patterns."
        )
    return (
        "Reviewed strong_author_year precision is below 0.95. Inspect false and unclear "
        "examples before treating the full analysis-ready table as a high-precision input."
    )


def _series_or_blank(frame: pd.DataFrame, column: str) -> pd.Series:
    if column not in frame:
        return pd.Series([""] * len(frame), index=frame.index, dtype="string")
    return frame[column].fillna("").astype(str)


def _ensure_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        if column not in df.columns:
            df[column] = ""
    return df


def _rate(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "unavailable"
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
