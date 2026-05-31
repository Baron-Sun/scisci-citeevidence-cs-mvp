"""Pure metric helpers for final-release citation-context volume analyses."""

from __future__ import annotations

from typing import Any

import pandas as pd

INTENT_ORDER = (
    "background",
    "uses",
    "compares_against",
    "extends",
    "critiques",
    "applies",
)
EVIDENCE_USE_INTENTS = (
    "uses",
    "compares_against",
    "extends",
    "critiques",
    "applies",
)
INTENT_COUNT_COLUMNS = {intent: f"{intent}_count" for intent in INTENT_ORDER}
PAPER_KEY_COLUMNS = ["resolved_cited_acl_id", "resolved_cited_title"]
OPTIONAL_PAPER_COLUMNS = ["resolved_cited_year", "resolved_cited_authors"]


def safe_rate(numerator: int | float, denominator: int | float) -> float:
    """Return a numeric rate with zero-denominator protection."""
    return float(numerator / denominator) if denominator else 0.0


def build_paper_evidence_use_table(contexts: pd.DataFrame, labels: pd.DataFrame) -> pd.DataFrame:
    """Build cited-paper citation-context volume and evidence-use metrics.

    ``total_strong_contexts`` is a citation-context volume measure: it counts unique
    strong context rows per cited paper, not graph in-degree. Evidence-use counts
    exclude background labels and are computed only from final analysis-ready labels.
    """
    context_columns = ["context_id", *PAPER_KEY_COLUMNS, *OPTIONAL_PAPER_COLUMNS]
    contexts_small = _ensure_columns(contexts.copy(), context_columns)
    contexts_small = _clean_text_columns(contexts_small, context_columns)
    contexts_small = contexts_small.loc[
        contexts_small["context_id"].ne("")
        & contexts_small["resolved_cited_title"].ne("")
    ].copy()

    output_columns = _paper_evidence_use_columns(include_optional=True)
    if contexts_small.empty:
        return pd.DataFrame(columns=output_columns)

    total_contexts = (
        contexts_small.groupby(PAPER_KEY_COLUMNS, dropna=False)
        .agg(total_strong_contexts=("context_id", "nunique"))
        .reset_index()
    )
    optional = _optional_paper_metadata(contexts_small)
    table = total_contexts.merge(optional, on=PAPER_KEY_COLUMNS, how="left")

    label_counts = _build_label_counts(labels)
    table = table.merge(label_counts, on=PAPER_KEY_COLUMNS, how="left")
    count_columns = [*INTENT_COUNT_COLUMNS.values(), "labeled_contexts"]
    for column in count_columns:
        if column not in table:
            table[column] = 0
    table[count_columns] = table[count_columns].fillna(0).astype(int)
    evidence_columns = [INTENT_COUNT_COLUMNS[intent] for intent in EVIDENCE_USE_INTENTS]
    table["evidence_use_count"] = table[evidence_columns].sum(axis=1).astype(int)
    table["evidence_use_share"] = _safe_series_rate(
        table["evidence_use_count"],
        table["total_strong_contexts"],
    )
    table["background_share"] = _safe_series_rate(
        table["background_count"],
        table["total_strong_contexts"],
    )
    table = _ensure_columns(table, output_columns)
    return table[output_columns].sort_values(
        ["total_strong_contexts", "evidence_use_count", "resolved_cited_title"],
        ascending=[False, False, True],
    )


def add_shrunk_evidence_use_share(
    table: pd.DataFrame,
    alpha: float = 2.0,
    beta: float = 8.0,
) -> pd.DataFrame:
    """Add a smoothed evidence-use share for citation-context volume rankings."""
    frame = table.copy()
    frame = _ensure_columns(frame, ["evidence_use_count", "total_strong_contexts"])
    frame["evidence_use_count"] = pd.to_numeric(
        frame["evidence_use_count"],
        errors="coerce",
    ).fillna(0)
    frame["total_strong_contexts"] = pd.to_numeric(
        frame["total_strong_contexts"],
        errors="coerce",
    ).fillna(0)
    frame["shrunk_evidence_use_share"] = (
        (frame["evidence_use_count"] + alpha)
        / (frame["total_strong_contexts"] + alpha + beta)
    )
    return frame


def filter_ranking_reversal_eligible(
    table: pd.DataFrame,
    min_total_contexts: int = 20,
    min_evidence_use_count: int = 5,
) -> pd.DataFrame:
    """Filter to papers with enough citation-context volume for stable rankings."""
    frame = _ensure_columns(table.copy(), ["total_strong_contexts", "evidence_use_count"])
    total_contexts = pd.to_numeric(frame["total_strong_contexts"], errors="coerce").fillna(0)
    evidence_use = pd.to_numeric(frame["evidence_use_count"], errors="coerce").fillna(0)
    mask = total_contexts.ge(min_total_contexts) & evidence_use.ge(min_evidence_use_count)
    return frame.loc[mask].copy()


def compute_ranking_reversal(table: pd.DataFrame) -> pd.DataFrame:
    """Compute citation-context volume vs evidence-use ranking reversals."""
    frame = add_shrunk_evidence_use_share(table)
    rank_inputs = {
        "rank_by_context_volume": "total_strong_contexts",
        "rank_by_evidence_use_count": "evidence_use_count",
        "rank_by_evidence_use_share": "evidence_use_share",
        "rank_by_shrunk_evidence_use_share": "shrunk_evidence_use_share",
    }
    frame = _ensure_columns(frame, list(rank_inputs.values()))
    for rank_column, source_column in rank_inputs.items():
        values = pd.to_numeric(frame[source_column], errors="coerce").fillna(0)
        frame[rank_column] = values.rank(method="min", ascending=False)
    frame["rank_difference_count"] = (
        frame["rank_by_context_volume"] - frame["rank_by_evidence_use_count"]
    )
    frame["rank_difference_shrunk_share"] = (
        frame["rank_by_context_volume"] - frame["rank_by_shrunk_evidence_use_share"]
    )
    frame["reversal_type"] = "balanced"
    frame.loc[frame["rank_difference_count"].gt(0), "reversal_type"] = "evidence-use riser"
    frame.loc[frame["rank_difference_count"].lt(0), "reversal_type"] = "context-volume riser"
    return frame


def _build_label_counts(labels: pd.DataFrame) -> pd.DataFrame:
    label_columns = ["context_id", *PAPER_KEY_COLUMNS, "final_intent"]
    labels_small = _ensure_columns(labels.copy(), label_columns)
    labels_small = _clean_text_columns(labels_small, label_columns)
    labels_small = labels_small.loc[
        labels_small["context_id"].ne("")
        & labels_small["resolved_cited_title"].ne("")
        & labels_small["final_intent"].ne("")
    ].copy()
    if labels_small.empty:
        return pd.DataFrame(columns=[*PAPER_KEY_COLUMNS, *_label_count_columns()])
    labels_small = labels_small.drop_duplicates(
        [*PAPER_KEY_COLUMNS, "context_id", "final_intent"],
    )
    intent_counts = (
        labels_small.groupby([*PAPER_KEY_COLUMNS, "final_intent"], dropna=False)
        .size()
        .reset_index(name="rows")
    )
    pivot = intent_counts.pivot_table(
        index=PAPER_KEY_COLUMNS,
        columns="final_intent",
        values="rows",
        fill_value=0,
        aggfunc="sum",
    ).reset_index()
    for intent in INTENT_ORDER:
        if intent not in pivot:
            pivot[intent] = 0
        pivot[INTENT_COUNT_COLUMNS[intent]] = pd.to_numeric(
            pivot[intent],
            errors="coerce",
        ).fillna(0).astype(int)
    labeled_contexts = (
        labels_small.groupby(PAPER_KEY_COLUMNS, dropna=False)
        .agg(labeled_contexts=("context_id", "nunique"))
        .reset_index()
    )
    counts = pivot[[*PAPER_KEY_COLUMNS, *INTENT_COUNT_COLUMNS.values()]]
    return counts.merge(labeled_contexts, on=PAPER_KEY_COLUMNS, how="left")


def _optional_paper_metadata(contexts: pd.DataFrame) -> pd.DataFrame:
    present_columns = [column for column in OPTIONAL_PAPER_COLUMNS if column in contexts]
    if not present_columns:
        return contexts[PAPER_KEY_COLUMNS].drop_duplicates().copy()
    metadata = (
        contexts[[*PAPER_KEY_COLUMNS, *present_columns]]
        .sort_values(PAPER_KEY_COLUMNS)
        .groupby(PAPER_KEY_COLUMNS, dropna=False)
        .agg({column: _first_non_empty for column in present_columns})
        .reset_index()
    )
    for column in OPTIONAL_PAPER_COLUMNS:
        if column not in metadata:
            metadata[column] = ""
    return metadata[[*PAPER_KEY_COLUMNS, *OPTIONAL_PAPER_COLUMNS]]


def _paper_evidence_use_columns(*, include_optional: bool) -> list[str]:
    optional = OPTIONAL_PAPER_COLUMNS if include_optional else []
    return [
        *PAPER_KEY_COLUMNS,
        *optional,
        "total_strong_contexts",
        *INTENT_COUNT_COLUMNS.values(),
        "evidence_use_count",
        "labeled_contexts",
        "evidence_use_share",
        "background_share",
    ]


def _label_count_columns() -> list[str]:
    return [*INTENT_COUNT_COLUMNS.values(), "labeled_contexts"]


def _ensure_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        if column not in df:
            df[column] = ""
    return df


def _clean_text_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        df[column] = df[column].map(_clean)
    return df


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        return str(value).strip()
    return str(value).strip()


def _first_non_empty(values: pd.Series) -> str:
    for value in values:
        cleaned = _clean(value)
        if cleaned:
            return cleaned
    return ""


def _safe_series_rate(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    denom = pd.to_numeric(denominator, errors="coerce").replace(0, pd.NA)
    num = pd.to_numeric(numerator, errors="coerce").fillna(0)
    return (num / denom).fillna(0.0)
