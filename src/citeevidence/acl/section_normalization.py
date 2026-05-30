from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from citeevidence.acl.full_sections import SECTIONED_COLUMNS, normalize_section_name

DEFAULT_NORMALIZED_SECTIONED_SECTIONS_PATH = Path(
    "data/interim/acl_sections_sectioned_normalized.parquet"
)
DEFAULT_SECTION_NORMALIZATION_REPORT = Path("reports/section_normalization_audit.md")


def normalize_sectioned_sections(
    *,
    input_path: str | Path,
    out_path: str | Path = DEFAULT_NORMALIZED_SECTIONED_SECTIONS_PATH,
    report_path: str | Path = DEFAULT_SECTION_NORMALIZATION_REPORT,
    top_n_unknown: int = 300,
) -> dict[str, Any]:
    """Normalize explicit ACL section headings and write an audit report."""
    if top_n_unknown < 1:
        raise ValueError("top_n_unknown must be positive")

    source = Path(input_path)
    if not source.exists():
        raise FileNotFoundError(f"Sectioned ACL sections parquet does not exist: {source}")

    sections = pd.read_parquet(source)
    missing_columns = [column for column in SECTIONED_COLUMNS if column not in sections]
    if missing_columns:
        raise ValueError(
            "Sectioned ACL sections parquet is missing required columns: "
            + ", ".join(missing_columns)
        )

    before = _before_normalized_sections(sections)
    after = sections["section_name"].map(normalize_section_name)
    normalized = sections[SECTIONED_COLUMNS].copy()
    normalized["normalized_section"] = after

    output = Path(out_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    normalized.to_parquet(output, index=False)

    metrics = {
        "input_rows": int(len(sections)),
        "output_rows": int(len(normalized)),
        "section_name_non_empty_rate": _rate(
            int(sections["section_name"].map(_clean_text_or_none).notna().sum()),
            len(sections),
        ),
        "unknown_rate_before": _rate(int(before.eq("unknown").sum()), len(before)),
        "unknown_rate_after": _rate(int(after.eq("unknown").sum()), len(after)),
        "distribution_before": _distribution(before),
        "distribution_after": _distribution(after),
        "top_unknown_before": _top_unknown_raw_sections(sections, before, top_n_unknown),
        "top_unknown_after": _top_unknown_raw_sections(sections, after, top_n_unknown),
    }

    report = _build_report(
        input_path=source,
        out_path=output,
        metrics=metrics,
        top_n_unknown=top_n_unknown,
    )
    report_output = Path(report_path)
    report_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.write_text(report, encoding="utf-8")
    return metrics


def _before_normalized_sections(sections: pd.DataFrame) -> pd.Series:
    if "normalized_section" not in sections:
        return pd.Series(["unknown"] * len(sections), index=sections.index)
    return sections["normalized_section"].map(
        lambda value: _clean_text_or_none(value) or "unknown"
    )


def _top_unknown_raw_sections(
    sections: pd.DataFrame,
    normalized: pd.Series,
    limit: int,
) -> list[dict[str, Any]]:
    unknown = sections.loc[normalized.eq("unknown"), "section_name"].map(
        lambda value: _clean_text_or_none(value) or "<empty>"
    )
    if unknown.empty:
        return []
    counts = (
        unknown.value_counts(dropna=False)
        .head(limit)
        .rename_axis("section_name")
        .reset_index(name="paragraph_rows")
    )
    return _records(counts)


def _distribution(values: pd.Series) -> list[dict[str, Any]]:
    counts = (
        values.fillna("unknown")
        .astype(str)
        .value_counts(dropna=False)
        .rename_axis("normalized_section")
        .reset_index(name="paragraph_rows")
    )
    return _records(counts)


def _build_report(
    *,
    input_path: Path,
    out_path: Path,
    metrics: dict[str, Any],
    top_n_unknown: int,
) -> str:
    return "\n".join(
        [
            "# Section Normalization Audit",
            "",
            "## Inputs / Outputs",
            _table(
                [
                    {"name": "input", "path": input_path, "rows": metrics["input_rows"]},
                    {
                        "name": "normalized_sections",
                        "path": out_path,
                        "rows": metrics["output_rows"],
                    },
                ]
            ),
            "",
            "## Core Metrics",
            _table(
                [
                    {
                        "metric": "section_name non-empty rate",
                        "value": metrics["section_name_non_empty_rate"],
                    },
                    {"metric": "unknown rate before", "value": metrics["unknown_rate_before"]},
                    {"metric": "unknown rate after", "value": metrics["unknown_rate_after"]},
                ]
            ),
            "",
            "## Normalized Section Distribution Before",
            _table(metrics["distribution_before"]),
            "",
            "## Normalized Section Distribution After",
            _table(metrics["distribution_after"]),
            "",
            f"## Top {top_n_unknown} Raw Section Names Mapped To Unknown Before",
            _table(metrics["top_unknown_before"]),
            "",
            f"## Top {top_n_unknown} Raw Section Names Mapped To Unknown After",
            _table(metrics["top_unknown_after"]),
            "",
            "## Normalization Note",
            (
                "Rules are conservative and use only explicit section headings. Paragraph "
                "content is not used to infer section labels."
            ),
            "",
        ]
    )


def _clean_text_or_none(value: Any) -> str | None:
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    text = " ".join(str(value).split())
    return text or None


def _rate(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.000"
    return f"{numerator / denominator:.3f}"


def _records(frame: pd.DataFrame) -> list[dict[str, Any]]:
    if frame.empty:
        return []
    clean = frame.where(pd.notna(frame), None)
    return clean.to_dict(orient="records")


def _table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "No records available."
    columns = list(dict.fromkeys(column for row in rows for column in row))
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(_markdown_cell(row.get(column)) for column in columns)
            + " |"
        )
    return "\n".join(lines)


def _markdown_cell(value: Any) -> str:
    if value is None:
        return "unavailable"
    text = str(value)
    if len(text) > 160:
        text = f"{text[:157]}..."
    return text.replace("|", "\\|")
