"""Pure metric helpers for final-release citation-context volume analyses."""

from __future__ import annotations

from typing import Any

import numpy as np
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
ROLE_QUADRANT_RULE_VERSION = "v1_heuristic"


def safe_rate(numerator: int | float, denominator: int | float) -> float:
    """Return a numeric rate with zero-denominator protection."""
    return float(numerator / denominator) if denominator else 0.0


def format_section_label(section: str, total: int) -> str:
    """Format a readable section label with compact row count."""
    section_name = _clean(section) or "unknown"
    readable = section_name.replace("_", " ").replace("-", " ").title()
    return f"{readable} (N={_format_compact_count(total)})"


def build_section_function_counts(labels: pd.DataFrame) -> pd.DataFrame:
    """Build tidy section-by-function counts from final analysis-ready labels."""
    columns = _section_function_columns(include_lift=False)
    frame = _ensure_columns(labels.copy(), ["normalized_section", "final_intent"])
    frame = _clean_text_columns(frame, ["normalized_section", "final_intent"])
    frame["normalized_section"] = frame["normalized_section"].replace("", "unknown")
    frame = frame.loc[frame["final_intent"].ne("")].copy()
    if frame.empty:
        return pd.DataFrame(columns=columns)

    observed = (
        frame.groupby(["normalized_section", "final_intent"], dropna=False)
        .size()
        .reset_index(name="rows")
    )
    sections = _ordered_sections(frame["normalized_section"].unique())
    intents = _ordered_intents(frame["final_intent"].unique())
    grid = pd.MultiIndex.from_product(
        [sections, intents],
        names=["normalized_section", "final_intent"],
    ).to_frame(index=False)
    counts = grid.merge(observed, on=["normalized_section", "final_intent"], how="left")
    counts["rows"] = counts["rows"].fillna(0).astype(int)

    section_totals = (
        frame.groupby("normalized_section", dropna=False)
        .size()
        .reset_index(name="section_total")
    )
    intent_totals = (
        frame.groupby("final_intent", dropna=False)
        .size()
        .reset_index(name="intent_total")
    )
    counts = counts.merge(section_totals, on="normalized_section", how="left")
    counts = counts.merge(intent_totals, on="final_intent", how="left")
    counts["grand_total"] = len(frame)
    numeric_columns = ["section_total", "intent_total", "grand_total"]
    counts[numeric_columns] = counts[numeric_columns].fillna(0).astype(int)
    counts["row_share"] = _safe_series_rate(counts["rows"], counts["section_total"])
    counts["global_share"] = _safe_series_rate(counts["intent_total"], counts["grand_total"])
    counts["is_unknown_section"] = counts["normalized_section"].eq("unknown")
    counts["section_label"] = [
        format_section_label(section, int(total))
        for section, total in zip(
            counts["normalized_section"],
            counts["section_total"],
            strict=True,
        )
    ]
    counts["_section_order"] = counts["normalized_section"].map(
        {section: index for index, section in enumerate(sections)}
    )
    counts["_intent_order"] = counts["final_intent"].map(
        {intent: index for index, intent in enumerate(intents)}
    )
    counts = counts.sort_values(["_section_order", "_intent_order"]).drop(
        columns=["_section_order", "_intent_order"]
    )
    return counts[columns].reset_index(drop=True)


def build_section_function_lift(
    counts: pd.DataFrame,
    min_section_total: int = 100,
    smoothing: float = 0.5,
) -> pd.DataFrame:
    """Compute section-function log-odds lift from section count cells."""
    columns = _section_function_columns(include_lift=True)
    frame = _ensure_columns(counts.copy(), _section_function_columns(include_lift=False))
    if frame.empty:
        return pd.DataFrame(columns=columns)

    for column in ["rows", "section_total", "intent_total", "grand_total"]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0)
    if "is_unknown_section" not in counts:
        frame["is_unknown_section"] = _clean_text_columns(
            frame[["normalized_section"]].copy(),
            ["normalized_section"],
        )["normalized_section"].eq("unknown")
    else:
        frame["is_unknown_section"] = frame["is_unknown_section"].map(_parse_bool)
    frame = frame.loc[
        frame["is_unknown_section"] | frame["section_total"].ge(min_section_total)
    ].copy()
    if frame.empty:
        return pd.DataFrame(columns=columns)

    rows = frame["rows"]
    section_total = frame["section_total"]
    intent_total = frame["intent_total"]
    grand_total = frame["grand_total"]
    section_log_odds = np.log(
        (rows + smoothing)
        / ((section_total - rows).clip(lower=0) + smoothing)
    )
    global_log_odds = np.log(
        (intent_total + smoothing)
        / ((grand_total - intent_total).clip(lower=0) + smoothing)
    )
    frame["log_odds_lift"] = section_log_odds - global_log_odds
    frame["lift_direction"] = np.select(
        [frame["log_odds_lift"].gt(0), frame["log_odds_lift"].lt(0)],
        ["overrepresented", "underrepresented"],
        default="baseline",
    )
    frame["rows"] = frame["rows"].astype(int)
    for column in ["section_total", "intent_total", "grand_total"]:
        frame[column] = frame[column].astype(int)
    return frame[columns].reset_index(drop=True)


def build_object_role_signature(edges: pd.DataFrame) -> pd.DataFrame:
    """Build seed-registry object role signatures from evidence-backed edge rows."""
    columns = _object_role_signature_columns(include_quadrant=False)
    source_has_context_id = "context_id" in edges
    frame = _ensure_columns(
        edges.copy(),
        [
            "object_id",
            "canonical_name",
            "object_type",
            "final_intent",
            "context_id",
            "evidence_span",
            "confidence",
            "normalized_section",
        ],
    )
    text_columns = [
        "object_id",
        "canonical_name",
        "object_type",
        "final_intent",
        "context_id",
        "evidence_span",
        "normalized_section",
    ]
    frame = _clean_text_columns(frame, text_columns)
    frame = frame.loc[
        frame["object_id"].ne("")
        & frame["canonical_name"].ne("")
        & frame["final_intent"].ne("")
    ].copy()
    if frame.empty:
        return pd.DataFrame(columns=columns)

    deduped = _deduplicate_object_edges(frame, source_has_context_id=source_has_context_id)
    if deduped.empty:
        return pd.DataFrame(columns=columns)

    metadata = (
        deduped[["object_id", "canonical_name", "object_type"]]
        .groupby("object_id", dropna=False)
        .agg(
            canonical_name=("canonical_name", _first_non_empty),
            object_type=("object_type", _first_non_empty),
        )
        .reset_index()
    )
    total_edges = (
        deduped.groupby("object_id", dropna=False)
        .size()
        .reset_index(name="total_edges")
    )
    intent_counts = _object_intent_counts(deduped)
    distinct_contexts = _object_distinct_contexts(deduped)
    confidence = _object_mean_confidence(deduped)

    signature = (
        metadata.merge(total_edges, on="object_id", how="left")
        .merge(intent_counts, on="object_id", how="left")
        .merge(distinct_contexts, on="object_id", how="left")
        .merge(confidence, on="object_id", how="left")
    )
    count_columns = [
        "total_edges",
        "background_edges",
        "uses_count",
        "compares_against_count",
        "extends_count",
        "critiques_count",
        "applies_count",
        "distinct_contexts",
    ]
    for column in count_columns:
        if column not in signature:
            signature[column] = 0
    signature[count_columns] = signature[count_columns].fillna(0).astype(int)
    evidence_columns = [
        "uses_count",
        "compares_against_count",
        "extends_count",
        "critiques_count",
        "applies_count",
    ]
    signature["evidence_use_count"] = signature[evidence_columns].sum(axis=1).astype(int)
    signature["non_background_edges"] = signature["evidence_use_count"]
    signature["use_share_non_background"] = _safe_series_rate(
        signature["uses_count"],
        signature["non_background_edges"],
    )
    signature["compare_critique_share_non_background"] = _safe_series_rate(
        signature["compares_against_count"] + signature["critiques_count"],
        signature["non_background_edges"],
    )
    signature["critique_share_non_background"] = _safe_series_rate(
        signature["critiques_count"],
        signature["non_background_edges"],
    )
    signature["background_share"] = _safe_series_rate(
        signature["background_edges"],
        signature["total_edges"],
    )
    signature = _ensure_columns(signature, columns)
    return signature[columns].sort_values(
        ["non_background_edges", "total_edges", "canonical_name"],
        ascending=[False, False, True],
    ).reset_index(drop=True)


def classify_object_role_quadrant(signature_table: pd.DataFrame) -> pd.DataFrame:
    """Add heuristic descriptive role quadrants for seed-registry objects."""
    columns = _object_role_signature_columns(include_quadrant=True)
    frame = _ensure_columns(signature_table.copy(), _object_role_signature_columns(False))
    for column in [
        "background_share",
        "non_background_edges",
        "use_share_non_background",
        "compare_critique_share_non_background",
        "critique_share_non_background",
        "critiques_count",
    ]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0)

    canonical_background = (
        frame["background_share"].ge(0.75)
        & frame["non_background_edges"].ge(20)
    )
    operational_infrastructure = (
        frame["use_share_non_background"].ge(0.60)
        & frame["non_background_edges"].ge(20)
    )
    critique_target = (
        frame["critique_share_non_background"].ge(0.15)
        & frame["critiques_count"].ge(10)
    )
    evaluation_anchor = (
        frame["compare_critique_share_non_background"].ge(0.45)
        & frame["non_background_edges"].ge(20)
    )
    frame["role_quadrant"] = np.select(
        [
            canonical_background,
            operational_infrastructure,
            critique_target,
            evaluation_anchor,
        ],
        [
            "canonical_background",
            "operational_infrastructure",
            "critique_target",
            "evaluation_anchor",
        ],
        default="mixed_role",
    )
    frame["role_quadrant_rule_version"] = ROLE_QUADRANT_RULE_VERSION
    return frame[columns].reset_index(drop=True)


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


def build_ranking_reversal_plot_table(
    ranking: pd.DataFrame,
    *,
    top_n: int = 20,
    min_total_contexts: int = 20,
    min_evidence_use_count: int = 5,
    mode: str = "count",
) -> pd.DataFrame:
    """Build an eligible citation-context volume vs evidence-use plot table."""
    columns = _ranking_reversal_plot_columns()
    if mode not in {"count", "shrunk_share"}:
        raise ValueError("mode must be 'count' or 'shrunk_share'")

    frame = filter_ranking_reversal_eligible(
        ranking,
        min_total_contexts=min_total_contexts,
        min_evidence_use_count=min_evidence_use_count,
    )
    if frame.empty or top_n <= 0:
        return pd.DataFrame(columns=columns)

    frame = compute_ranking_reversal(frame)
    frame = _ensure_columns(frame, columns)
    numeric_columns = [
        "total_strong_contexts",
        "evidence_use_count",
        "evidence_use_share",
        "shrunk_evidence_use_share",
        "background_share",
        "rank_by_context_volume",
        "rank_by_evidence_use_count",
        "rank_by_shrunk_evidence_use_share",
        "rank_difference_count",
        "rank_difference_shrunk_share",
    ]
    for column in numeric_columns:
        frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0)
    sort_column = (
        "rank_difference_count"
        if mode == "count"
        else "rank_difference_shrunk_share"
    )
    frame["_abs_rank_difference"] = frame[sort_column].abs()
    frame["plot_label"] = [
        _ranking_plot_label(title, acl_id)
        for title, acl_id in zip(
            frame["resolved_cited_title"],
            frame["resolved_cited_acl_id"],
            strict=True,
        )
    ]
    frame = frame.sort_values(
        ["_abs_rank_difference", "total_strong_contexts", "plot_label"],
        ascending=[False, False, True],
    ).head(top_n)
    return frame[columns].reset_index(drop=True)


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


def _section_function_columns(*, include_lift: bool) -> list[str]:
    columns = [
        "normalized_section",
        "final_intent",
        "rows",
        "section_total",
        "intent_total",
        "grand_total",
        "row_share",
        "global_share",
        "is_unknown_section",
        "section_label",
    ]
    if include_lift:
        columns.extend(["log_odds_lift", "lift_direction"])
    return columns


def _object_role_signature_columns(include_quadrant: bool) -> list[str]:
    columns = [
        "object_id",
        "canonical_name",
        "object_type",
        "total_edges",
        "background_edges",
        "non_background_edges",
        "uses_count",
        "compares_against_count",
        "extends_count",
        "critiques_count",
        "applies_count",
        "use_share_non_background",
        "compare_critique_share_non_background",
        "critique_share_non_background",
        "background_share",
        "evidence_use_count",
        "distinct_contexts",
        "mean_confidence",
    ]
    if include_quadrant:
        columns.extend(["role_quadrant", "role_quadrant_rule_version"])
    return columns


def _ranking_reversal_plot_columns() -> list[str]:
    return [
        "resolved_cited_acl_id",
        "resolved_cited_title",
        "total_strong_contexts",
        "evidence_use_count",
        "evidence_use_share",
        "shrunk_evidence_use_share",
        "background_share",
        "rank_by_context_volume",
        "rank_by_evidence_use_count",
        "rank_by_shrunk_evidence_use_share",
        "rank_difference_count",
        "rank_difference_shrunk_share",
        "reversal_type",
        "plot_label",
    ]


def _ranking_plot_label(title: object, acl_id: object, max_length: int = 46) -> str:
    label = _clean(title) or _clean(acl_id) or "Untitled cited paper"
    if len(label) <= max_length:
        return label
    prefix = label[: max_length - 1].rstrip()
    if " " in prefix:
        prefix = prefix.rsplit(" ", 1)[0]
    return f"{prefix.rstrip('.,;:')}..."


def _deduplicate_object_edges(
    frame: pd.DataFrame,
    *,
    source_has_context_id: bool,
) -> pd.DataFrame:
    fallback_keys = ["object_id", "canonical_name", "final_intent", "evidence_span"]
    if not source_has_context_id:
        return frame.drop_duplicates(fallback_keys).copy()

    with_context = frame.loc[frame["context_id"].ne("")].drop_duplicates(
        ["context_id", "object_id", "final_intent"],
    )
    without_context = frame.loc[frame["context_id"].eq("")].drop_duplicates(fallback_keys)
    return pd.concat([with_context, without_context], ignore_index=True)


def _object_intent_counts(deduped: pd.DataFrame) -> pd.DataFrame:
    counts = (
        deduped.groupby(["object_id", "final_intent"], dropna=False)
        .size()
        .reset_index(name="rows")
    )
    pivot = counts.pivot_table(
        index="object_id",
        columns="final_intent",
        values="rows",
        fill_value=0,
        aggfunc="sum",
    ).reset_index()
    for intent in INTENT_ORDER:
        if intent not in pivot:
            pivot[intent] = 0
    pivot["background_edges"] = pd.to_numeric(
        pivot["background"],
        errors="coerce",
    ).fillna(0).astype(int)
    for intent in EVIDENCE_USE_INTENTS:
        pivot[f"{intent}_count"] = pd.to_numeric(
            pivot[intent],
            errors="coerce",
        ).fillna(0).astype(int)
    return pivot[
        [
            "object_id",
            "background_edges",
            "uses_count",
            "compares_against_count",
            "extends_count",
            "critiques_count",
            "applies_count",
        ]
    ]


def _object_distinct_contexts(deduped: pd.DataFrame) -> pd.DataFrame:
    contexts = deduped.loc[deduped["context_id"].ne("")]
    if contexts.empty:
        return deduped[["object_id"]].drop_duplicates().assign(distinct_contexts=0)
    return (
        contexts.groupby("object_id", dropna=False)
        .agg(distinct_contexts=("context_id", "nunique"))
        .reset_index()
    )


def _object_mean_confidence(deduped: pd.DataFrame) -> pd.DataFrame:
    frame = deduped[["object_id", "confidence"]].copy()
    frame["confidence"] = pd.to_numeric(frame["confidence"], errors="coerce")
    return (
        frame.groupby("object_id", dropna=False)
        .agg(mean_confidence=("confidence", "mean"))
        .reset_index()
    )


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


def _parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    try:
        if pd.isna(value):
            return False
    except (TypeError, ValueError):
        pass
    if isinstance(value, int | float):
        return value != 0
    return str(value).strip().casefold() in {"1", "t", "true", "y", "yes"}


def _ordered_intents(intents: Any) -> list[str]:
    cleaned = {_clean(intent) for intent in intents}
    cleaned.discard("")
    ordered = [intent for intent in INTENT_ORDER if intent in cleaned]
    ordered.extend(sorted(cleaned.difference(INTENT_ORDER)))
    return ordered


def _ordered_sections(sections: Any) -> list[str]:
    cleaned = {_clean(section) or "unknown" for section in sections}
    section_totals = {section: 0 for section in cleaned}
    return sorted(
        cleaned,
        key=lambda section: (section == "unknown", section_totals[section], section),
    )


def _format_compact_count(total: int) -> str:
    if total >= 1_000_000:
        return f"{total / 1_000_000:.1f}M"
    if total >= 1_000:
        return f"{total / 1_000:.1f}k"
    return str(total)


def _first_non_empty(values: pd.Series) -> str:
    for value in values:
        cleaned = _clean(value)
        if cleaned:
            return cleaned
    return ""


def _safe_series_rate(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    denom = pd.to_numeric(denominator, errors="coerce").astype(float)
    num = pd.to_numeric(numerator, errors="coerce").fillna(0).astype(float)
    return num.div(denom.where(denom.ne(0))).fillna(0.0)
