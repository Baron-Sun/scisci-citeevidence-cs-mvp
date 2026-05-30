from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from citeevidence.contexts.extract import CONTEXT_COLUMNS

DEFAULT_CONTEXT_FLAGS_PATH = Path("data/processed/task6_context_quality_flags.parquet")
FLAG_COLUMNS = [
    "flag_single_clear_group_size_gt_1",
    "flag_empty_context_window_s3",
    "flag_empty_sentence_text",
    "flag_empty_reference_key",
    "flag_unresolved_with_cited_title",
    "flag_context_window_s3_too_long",
]
FLAG_ID_COLUMNS = [
    "context_id",
    "citing_paper_id",
    "reference_key",
    "section",
    "paragraph_id",
    "citation_marker",
    "citation_group_size",
    "attribution_status",
]
SAMPLE_COLUMNS = [
    "context_id",
    "citing_paper_id",
    "reference_key",
    "section",
    "paragraph_id",
    "citation_marker",
    "attribution_status",
    "sentence_text",
    "context_window_s3",
    "context_window_paragraph",
]


def audit_citation_contexts(
    *,
    contexts_path: str | Path,
    sections_path: str | Path,
    references_path: str | Path,
    out_report: str | Path,
    flags_path: str | Path = DEFAULT_CONTEXT_FLAGS_PATH,
    max_window_chars: int = 2000,
    sample_size: int = 20,
) -> pd.DataFrame:
    """Audit extracted citation contexts and write a markdown report plus flag parquet."""
    if max_window_chars < 100:
        raise ValueError("max_window_chars must be at least 100")
    if sample_size < 1:
        raise ValueError("sample_size must be positive")

    contexts = pd.read_parquet(contexts_path)
    sections = pd.read_parquet(sections_path, columns=["paper_id", "paragraph_id"])
    references = pd.read_parquet(references_path, columns=["citing_paper_id", "reference_key"])

    flags = build_context_quality_flags(contexts, max_window_chars=max_window_chars)
    flag_output = Path(flags_path)
    flag_output.parent.mkdir(parents=True, exist_ok=True)
    flags.to_parquet(flag_output, index=False)

    report = build_context_quality_report(
        contexts=contexts,
        sections=sections,
        references=references,
        flags=flags,
        contexts_path=Path(contexts_path),
        sections_path=Path(sections_path),
        references_path=Path(references_path),
        flags_path=flag_output,
        max_window_chars=max_window_chars,
        sample_size=sample_size,
    )
    report_output = Path(out_report)
    report_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.write_text(report, encoding="utf-8")
    return flags


def build_context_quality_flags(
    contexts: pd.DataFrame,
    *,
    max_window_chars: int,
) -> pd.DataFrame:
    """Build row-level quality flags for extracted citation contexts."""
    frame = _ensure_columns(contexts.copy(), CONTEXT_COLUMNS)
    flags = frame[FLAG_ID_COLUMNS].copy()
    flags["flag_single_clear_group_size_gt_1"] = (
        frame["attribution_status"].astype("string").eq("single_citation_clear")
        & pd.to_numeric(frame["citation_group_size"], errors="coerce").fillna(0).gt(1)
    )
    flags["flag_empty_context_window_s3"] = _missing_mask(frame["context_window_s3"])
    flags["flag_empty_sentence_text"] = _missing_mask(frame["sentence_text"])
    flags["flag_empty_reference_key"] = _missing_mask(frame["reference_key"])
    flags["flag_unresolved_with_cited_title"] = (
        frame["attribution_status"].astype("string").eq("bibliography_unresolved")
        & ~_missing_mask(frame["cited_title"])
    )
    flags["flag_context_window_s3_too_long"] = (
        frame["context_window_s3"].fillna("").astype(str).str.len() > max_window_chars
    )
    flags["flag_any"] = flags[FLAG_COLUMNS].any(axis=1)
    return flags


def build_context_quality_report(
    *,
    contexts: pd.DataFrame,
    sections: pd.DataFrame,
    references: pd.DataFrame,
    flags: pd.DataFrame,
    contexts_path: Path,
    sections_path: Path,
    references_path: Path,
    flags_path: Path,
    max_window_chars: int,
    sample_size: int,
) -> str:
    """Build the Task 6.1 markdown quality audit report."""
    contexts = _ensure_columns(contexts.copy(), CONTEXT_COLUMNS)
    total = len(contexts)
    unique_context_ids = contexts["context_id"].nunique(dropna=True)
    duplicate_context_ids = int(total - unique_context_ids)

    sections_text = [
        "# Task 6.1 Citation Context Quality Audit",
        "",
        "## Inputs",
        f"- Contexts: `{contexts_path}`",
        f"- Sections: `{sections_path}` ({len(sections)} rows)",
        f"- References: `{references_path}` ({len(references)} rows)",
        f"- Flags: `{flags_path}`",
        f"- Configured max context window length: {max_window_chars}",
        "",
        "## Core Counts",
        _table(
            pd.DataFrame(
                [
                    {"metric": "contexts", "value": total},
                    {"metric": "unique_context_id", "value": unique_context_ids},
                    {"metric": "duplicate_context_id_count", "value": duplicate_context_ids},
                ]
            )
        ),
        "",
        "## Null / Empty Rates",
        _table(_null_empty_rates(contexts)),
        "",
        "## Attribution Status Distribution",
        _table(_value_counts(contexts, ["attribution_status"], "contexts")),
        "",
        "## Section Distribution",
        _table(_value_counts(contexts, ["section"], "contexts")),
        "",
        "## Citation Group Size Distribution",
        _table(_value_counts(contexts, ["citation_group_size"], "contexts")),
        "",
        "## Grounding Checks",
        _table(_grounding_rates(contexts)),
        "",
        "## Suspicious Rows",
        _table(_flag_summary(flags)),
        "",
        "## Sample 20 Rows",
        _table(_sample_contexts(contexts, sample_size)),
        "",
    ]
    return "\n".join(sections_text)


def _null_empty_rates(contexts: pd.DataFrame) -> pd.DataFrame:
    total = len(contexts)
    rows = []
    for column in CONTEXT_COLUMNS:
        missing = int(_missing_mask(contexts[column]).sum())
        rows.append(
            {
                "column": column,
                "null_or_empty": missing,
                "rate": _rate(missing, total),
            }
        )
    return pd.DataFrame(rows)


def _grounding_rates(contexts: pd.DataFrame) -> pd.DataFrame:
    total = len(contexts)
    sentence = contexts["sentence_text"].fillna("").astype(str)
    window_s3 = contexts["context_window_s3"].fillna("").astype(str)
    window_paragraph = contexts["context_window_paragraph"].fillna("").astype(str)
    marker = contexts["citation_marker"].fillna("").astype(str)

    checks = [
        {
            "check": "sentence_text appears inside context_window_s3",
            "passed": int(
                pd.Series(
                    [
                        bool(value) and value in window
                        for value, window in zip(sentence, window_s3, strict=True)
                    ]
                ).sum()
            ),
        },
        {
            "check": "sentence_text appears inside context_window_paragraph",
            "passed": int(
                pd.Series(
                    [
                        bool(value) and value in window
                        for value, window in zip(sentence, window_paragraph, strict=True)
                    ]
                ).sum()
            ),
        },
        {
            "check": "citation_marker appears inside sentence_text",
            "passed": int(
                pd.Series(
                    [
                        bool(value) and value in sent
                        for value, sent in zip(marker, sentence, strict=True)
                    ]
                ).sum()
            ),
        },
    ]
    for check in checks:
        check["total"] = total
        check["rate"] = _rate(int(check["passed"]), total)
    return pd.DataFrame(checks)


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


def _sample_contexts(contexts: pd.DataFrame, sample_size: int) -> pd.DataFrame:
    if contexts.empty:
        return pd.DataFrame(columns=SAMPLE_COLUMNS)
    sample = contexts[SAMPLE_COLUMNS].head(sample_size).copy()
    for column in ("sentence_text", "context_window_s3", "context_window_paragraph"):
        sample[column] = sample[column].map(lambda value: _truncate(value, 220))
    return sample


def _value_counts(df: pd.DataFrame, columns: list[str], count_name: str) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=[*columns, count_name])
    filled = df.copy()
    for column in columns:
        filled[column] = filled[column].fillna("unavailable")
    return (
        filled.groupby(columns, dropna=False)
        .size()
        .reset_index(name=count_name)
        .sort_values([count_name, *columns], ascending=[False, *([True] * len(columns))])
    )


def _ensure_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        if column not in df.columns:
            df[column] = None
    return df


def _missing_mask(series: pd.Series) -> pd.Series:
    return series.isna() | series.astype("string").str.strip().fillna("").eq("")


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
