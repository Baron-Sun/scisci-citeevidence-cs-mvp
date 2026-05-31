from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib
import pandas as pd
import pyarrow.parquet as pq
from matplotlib import patches

from citeevidence.markdown import format_markdown_sections

matplotlib.use("Agg")
from matplotlib import pyplot as plt  # noqa: E402

DEFAULT_FINAL_V2_REPORT = Path("reports/final_scisci_results_report_v2.md")
DEFAULT_FINAL_V2_FIGURES_DIR = Path("figures/final_v2")
DEFAULT_FINAL_V2_SOURCE_DATA_DIR = Path("figures/final_v2/source_data")
DEFAULT_FINAL_V2_EVIDENCE_CARDS = Path("data/processed/final_v2_evidence_cards.csv")
DEFAULT_SECTIONED_CONTEXTS_PATH = Path("data/processed/citation_contexts_sectioned.parquet")
DEFAULT_RESOLVED_CONTEXTS_PATH = Path("data/processed/citation_contexts_resolved.parquet")

INTENT_ORDER = [
    "uses",
    "compares_against",
    "extends",
    "critiques",
    "applies",
    "background",
]
EVIDENCE_INTENTS = ["uses", "compares_against", "extends", "critiques", "applies"]
PSEUDO_OBJECT_NODE_NAMES = {
    "unknown",
    "method",
    "model",
    "metric",
    "software_or_tool",
    "dataset_or_database",
    "benchmark_or_protocol",
    "task",
    "claim_or_finding",
    "theory_or_concept",
}
INTENT_COLORS = {
    "uses": "#3B7EA1",
    "compares_against": "#D9892B",
    "extends": "#5B9A57",
    "critiques": "#B54A5A",
    "applies": "#7E62A3",
    "background": "#A9A9A9",
}
OBJECT_TYPE_COLORS = {
    "model": "#3B7EA1",
    "method": "#5B9A57",
    "metric": "#D9892B",
    "dataset_or_database": "#7E62A3",
    "benchmark_or_protocol": "#B54A5A",
    "software_or_tool": "#5D737E",
}
BOTTLENECK_FAMILIES = [
    "fail / cannot / unable",
    "limitation / drawback",
    "poor performance",
    "metric limitation",
    "data/resource requirement",
    "generalization / scalability",
    "other",
]
METRIC_BENCHMARK_PATTERNS = [
    ("BLEU", ("bleu",)),
    ("ROUGE", ("rouge",)),
    ("METEOR", ("meteor",)),
    ("WMT", ("wmt",)),
    ("SuperGLUE", ("superglue",)),
    ("GLUE", ("glue",)),
    ("SQuAD", ("squad",)),
    ("SemEval", ("semeval",)),
    ("CoNLL-2003", ("conll-2003", "conll 2003")),
    ("CoNLL-2012", ("conll-2012", "conll 2012")),
]


def run_final_results_v2_analysis(
    *,
    phase2_path: str | Path,
    excluded_path: str | Path,
    failed_diagnostics_path: str | Path,
    object_graph_candidates_path: str | Path,
    object_mentions_path: str | Path,
    contexts_path: str | Path,
    phase1_path: str | Path,
    out_report_path: str | Path = DEFAULT_FINAL_V2_REPORT,
    figures_dir: str | Path = DEFAULT_FINAL_V2_FIGURES_DIR,
    source_data_dir: str | Path = DEFAULT_FINAL_V2_SOURCE_DATA_DIR,
    out_cards_path: str | Path = DEFAULT_FINAL_V2_EVIDENCE_CARDS,
) -> dict[str, Any]:
    """Generate final_v2 publication-grade figures and report without API calls."""
    input_paths = [
        Path(phase2_path),
        Path(excluded_path),
        Path(failed_diagnostics_path),
        Path(object_graph_candidates_path),
        Path(object_mentions_path),
        Path(contexts_path),
        Path(phase1_path),
    ]
    for path in input_paths:
        if not path.exists():
            raise FileNotFoundError(f"Required input does not exist: {path}")

    phase2_raw = pd.read_parquet(phase2_path)
    excluded = pd.read_parquet(excluded_path)
    failed_diagnostics = pd.read_parquet(failed_diagnostics_path)
    object_graph = pd.read_parquet(object_graph_candidates_path)
    object_mentions = pd.read_parquet(object_mentions_path)
    contexts = pd.read_parquet(contexts_path)
    phase1 = pd.read_parquet(phase1_path)

    labels = prepare_final_v2_labels(phase2_raw)
    edges = build_final_v2_object_edges(labels, object_graph)
    pipeline = build_final_v2_evidence_pipeline(
        contexts=contexts,
        object_graph=object_graph,
        phase1=phase1,
        labels=labels,
        excluded=excluded,
        failed_diagnostics=failed_diagnostics,
        edges=edges,
    )
    section_profile = build_final_v2_section_role_profile(labels)
    object_profile = build_final_v2_object_role_profile(edges)
    infrastructure = build_final_v2_infrastructure_scores(edges)
    ranking_reversal = build_final_v2_ranking_reversal(contexts, labels)
    transition = build_final_v2_phase_transition(labels)
    critique_matrix = build_final_v2_critique_bottleneck_matrix(edges)
    metric_profile = build_final_v2_metric_benchmark_role_profiles(edges)
    evidence_cards = build_final_v2_evidence_cards(edges, ranking_reversal)
    summary = build_final_v2_summary(
        pipeline=pipeline,
        labels=labels,
        excluded=excluded,
        failed_diagnostics=failed_diagnostics,
        object_mentions=object_mentions,
        edges=edges,
    )

    report_path = Path(out_report_path)
    figures_path = Path(figures_dir)
    source_path = Path(source_data_dir)
    cards_path = Path(out_cards_path)
    for path in (report_path, figures_path, source_path, cards_path):
        if path.suffix:
            path.parent.mkdir(parents=True, exist_ok=True)
        else:
            path.mkdir(parents=True, exist_ok=True)

    evidence_cards.to_csv(cards_path, index=False)
    figure_paths = write_final_v2_figures(
        pipeline=pipeline,
        section_profile=section_profile,
        object_profile=object_profile,
        infrastructure=infrastructure,
        ranking_reversal=ranking_reversal,
        transition=transition,
        critique_matrix=critique_matrix,
        metric_profile=metric_profile,
        figures_dir=figures_path,
        source_data_dir=source_path,
    )
    report_path.write_text(
        build_final_v2_report(
            summary=summary,
            pipeline=pipeline,
            section_profile=section_profile,
            object_profile=object_profile,
            infrastructure=infrastructure,
            ranking_reversal=ranking_reversal,
            transition=transition,
            critique_matrix=critique_matrix,
            metric_profile=metric_profile,
            evidence_cards=evidence_cards,
            figure_paths=figure_paths,
            cards_path=cards_path,
        ),
        encoding="utf-8",
    )
    return {
        "analysis_ready_phase2_labels": int(len(labels)),
        "evidence_backed_object_edges": int(len(edges)),
        "figure_count": len(figure_paths),
        "report_path": str(report_path),
        "cards_path": str(cards_path),
        "source_data_dir": str(source_path),
    }


def prepare_final_v2_labels(phase2: pd.DataFrame) -> pd.DataFrame:
    """Prepare analysis-ready labels with a unified evidence span column."""
    original_columns = set(phase2.columns)
    columns = [
        "context_id",
        "source_context_id",
        "resolved_cited_acl_id",
        "resolved_cited_title",
        "resolved_cited_year",
        "resolved_cited_authors",
        "normalized_section",
        "raw_section_name",
        "sentence_text",
        "context_window_s3",
        "primary_candidate_intent",
        "final_intent",
        "final_object_type",
        "final_relation_subtype",
        "method_edge_type",
        "evidence_span_phase2",
        "analysis_evidence_span",
        "evidence_supports_label",
        "abstain",
        "phase2_confidence",
        "analysis_confidence",
        "analysis_ready",
        "rationale_short",
    ]
    frame = _ensure_columns(phase2.copy(), columns)
    for column in columns:
        if column not in {"phase2_confidence", "analysis_confidence", "abstain", "analysis_ready"}:
            frame[column] = frame[column].map(_clean)
    frame["evidence_span"] = frame["analysis_evidence_span"]
    frame.loc[frame["evidence_span"].eq(""), "evidence_span"] = frame["evidence_span_phase2"]
    frame["confidence"] = pd.to_numeric(frame["analysis_confidence"], errors="coerce")
    frame.loc[frame["confidence"].isna(), "confidence"] = pd.to_numeric(
        frame["phase2_confidence"],
        errors="coerce",
    )
    frame["confidence"] = frame["confidence"].fillna(0)
    mask = frame["context_id"].ne("") & frame["final_intent"].ne("")
    mask &= ~frame["final_intent"].eq("unclear")
    if "analysis_ready" in original_columns:
        mask &= frame["analysis_ready"].map(_bool_value)
    if "evidence_supports_label" in original_columns:
        mask &= frame["evidence_supports_label"].map(_clean).eq("true")
    if "abstain" in original_columns:
        mask &= ~frame["abstain"].map(_bool_value)
    if {"evidence_span_phase2", "analysis_evidence_span"} & original_columns:
        mask &= frame.apply(_evidence_span_grounded, axis=1)
    return frame.loc[mask].copy()


def build_final_v2_object_edges(
    labels: pd.DataFrame,
    object_graph: pd.DataFrame,
    *,
    max_objects_per_context: int = 3,
) -> pd.DataFrame:
    """Build object-use edges with unit unique(context_id, object_id, final_intent)."""
    graph = prepare_final_v2_object_graph_candidates(object_graph)
    if max_objects_per_context:
        graph = graph.groupby("context_id", dropna=False).head(max_objects_per_context)
    label_columns = [
        "context_id",
        "source_context_id",
        "resolved_cited_acl_id",
        "resolved_cited_title",
        "resolved_cited_year",
        "resolved_cited_authors",
        "normalized_section",
        "raw_section_name",
        "sentence_text",
        "context_window_s3",
        "primary_candidate_intent",
        "final_intent",
        "final_object_type",
        "final_relation_subtype",
        "method_edge_type",
        "evidence_span",
        "confidence",
        "rationale_short",
    ]
    labels_small = _ensure_columns(labels.copy(), label_columns)[label_columns]
    edges = labels_small.merge(graph, on="context_id", how="inner")
    if edges.empty:
        return _ensure_columns(pd.DataFrame(), _edge_columns())[_edge_columns()]
    edges = edges.drop_duplicates(["context_id", "object_id", "final_intent"])
    edges["edge_unit"] = "unique_context_object_intent"
    return _ensure_columns(edges, _edge_columns())[_edge_columns()].sort_values(
        ["canonical_name", "context_id", "final_intent"],
    )


def prepare_final_v2_object_graph_candidates(object_graph: pd.DataFrame) -> pd.DataFrame:
    """Prepare eligible object candidates and exclude pseudo-object category names."""
    original_columns = set(object_graph.columns)
    columns = [
        "context_id",
        "object_id",
        "canonical_name",
        "object_type",
        "object_category",
        "confidence",
        "matched_in",
        "allow_in_object_graph",
        "graph_eligible",
    ]
    graph = _ensure_columns(object_graph.copy(), columns)
    for column in ("context_id", "object_id", "canonical_name", "object_type", "object_category"):
        graph[column] = graph[column].map(_clean)
    graph = graph.loc[graph["context_id"].ne("") & graph["canonical_name"].ne("")]
    graph = graph.loc[~graph["canonical_name"].str.casefold().isin(PSEUDO_OBJECT_NODE_NAMES)]
    if "allow_in_object_graph" in original_columns:
        graph = graph.loc[graph["allow_in_object_graph"].map(_bool_value)]
    if "graph_eligible" in original_columns:
        graph = graph.loc[graph["graph_eligible"].map(_bool_value)]
    graph.loc[graph["object_id"].eq(""), "object_id"] = (
        "fallback::" + graph["canonical_name"] + "::" + graph["object_type"]
    )
    graph["object_confidence"] = pd.to_numeric(graph["confidence"], errors="coerce").fillna(0)
    graph["matched_in_priority"] = graph["matched_in"].map(_matched_in_priority)
    graph = graph.sort_values(
        ["context_id", "object_confidence", "matched_in_priority", "canonical_name"],
        ascending=[True, False, False, True],
    )
    return graph[
        [
            "context_id",
            "object_id",
            "canonical_name",
            "object_type",
            "object_category",
            "object_confidence",
            "matched_in",
        ]
    ]


def build_final_v2_evidence_pipeline(
    *,
    contexts: pd.DataFrame,
    object_graph: pd.DataFrame,
    phase1: pd.DataFrame,
    labels: pd.DataFrame,
    excluded: pd.DataFrame,
    failed_diagnostics: pd.DataFrame,
    edges: pd.DataFrame,
) -> pd.DataFrame:
    """Build final_v2 staged pipeline counts."""
    sectioned_count = _optional_parquet_row_count(DEFAULT_SECTIONED_CONTEXTS_PATH) or len(contexts)
    resolved_count = _optional_parquet_row_count(DEFAULT_RESOLVED_CONTEXTS_PATH) or len(contexts)
    revalidated_rows = int(len(labels) + len(excluded))
    steps = [
        (
            "section_aware_contexts",
            "Section-aware contexts",
            int(sectioned_count),
            "Full deterministic extraction layer.",
        ),
        (
            "marker_components",
            "Marker components",
            int(resolved_count),
            "Can exceed contexts because grouped citations split.",
        ),
        (
            "strong_contexts",
            "Strong resolved contexts",
            int(len(contexts)),
            "Full deterministic high-confidence context layer.",
        ),
        (
            "object_graph_candidates",
            "Object graph candidates",
            int(len(object_graph)),
            "Full object candidate layer.",
        ),
        (
            "phase2_high_medium_queue",
            "Phase-2 high/medium queue",
            int(_bool_series(phase1, "should_send_to_llm").sum()),
            "Full high/medium Phase-1 LLM queue.",
        ),
        (
            "revalidated_phase2_rows",
            "Revalidated Phase-2 rows",
            revalidated_rows,
            "Batch rows that parsed or were recovered by local revalidation.",
        ),
        (
            "analysis_ready_phase2_labels",
            "Analysis-ready labels",
            int(len(labels)),
            "Grounded non-abstain Phase-2 semantic labels.",
        ),
        (
            "evidence_backed_object_edges",
            "Object-use edges",
            int(len(edges)),
            "Unique context-object-intent edges after top-3 object policy.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    first = max(steps[0][2], 1)
    previous: int | None = None
    for index, (step, label, count, note) in enumerate(steps, start=1):
        rows.append(
            {
                "step_order": index,
                "step": step,
                "display_label": label,
                "count": count,
                "count_label": _human_count(count),
                "retention_from_previous": _safe_rate(count, previous or 0)
                if previous
                else 1.0,
                "retention_from_first": _safe_rate(count, first),
                "note": note,
            }
        )
        if count:
            previous = count
    rows.append(
        {
            "step_order": len(steps) + 1,
            "step": "remaining_failed_phase2_rows",
            "display_label": "Remaining failed rows",
            "count": _remaining_failed_count(failed_diagnostics),
            "count_label": _human_count(_remaining_failed_count(failed_diagnostics)),
            "retention_from_previous": _safe_rate(
                _remaining_failed_count(failed_diagnostics),
                revalidated_rows,
            ),
            "retention_from_first": _safe_rate(_remaining_failed_count(failed_diagnostics), first),
            "note": "Excluded from final semantic figures.",
        }
    )
    return pd.DataFrame(rows)


def build_final_v2_section_role_profile(labels: pd.DataFrame) -> pd.DataFrame:
    """Build row-normalized final intent rates by normalized section."""
    frame = _ensure_columns(labels.copy(), ["normalized_section", "final_intent"])
    frame["normalized_section"] = frame["normalized_section"].map(_clean).str.lower()
    frame.loc[frame["normalized_section"].eq(""), "normalized_section"] = "unknown"
    counts = (
        frame.groupby(["normalized_section", "final_intent"], dropna=False)
        .size()
        .reset_index(name="rows")
    )
    totals = counts.groupby("normalized_section")["rows"].transform("sum")
    counts["section_total"] = totals
    counts["row_share"] = counts["rows"] / totals
    counts["is_unknown_section"] = counts["normalized_section"].eq("unknown")
    counts["section_label"] = counts.apply(
        lambda row: (
            f"{_display_label(row['normalized_section'])} "
            f"(N={_human_count(row['section_total'])})"
        ),
        axis=1,
    )
    return counts.sort_values(["is_unknown_section", "section_total", "normalized_section"])


def build_final_v2_object_role_profile(
    edges: pd.DataFrame,
    *,
    top_n: int = 20,
) -> pd.DataFrame:
    """Build 100% object role profiles for top objects by non-background evidence."""
    if edges.empty:
        return pd.DataFrame(columns=_role_profile_columns("object"))
    counts = (
        edges.groupby(["object_id", "canonical_name", "object_type", "final_intent"], dropna=False)
        .size()
        .reset_index(name="rows")
    )
    totals = counts.groupby("object_id")["rows"].transform("sum")
    counts["object_total"] = totals
    background = counts.loc[counts["final_intent"].eq("background"), ["object_id", "rows"]]
    background = background.rename(columns={"rows": "background_edges"})
    counts = counts.merge(background, on="object_id", how="left")
    counts["background_edges"] = counts["background_edges"].fillna(0).astype(int)
    counts["non_background_edges"] = counts["object_total"] - counts["background_edges"]
    counts["row_share"] = counts["rows"] / counts["object_total"].replace(0, pd.NA)
    counts["non_background_share"] = (
        counts["non_background_edges"] / counts["object_total"].replace(0, pd.NA)
    ).fillna(0)
    top_ids = (
        counts[["object_id", "non_background_edges", "non_background_share", "object_total"]]
        .drop_duplicates()
        .sort_values(
            ["non_background_edges", "non_background_share", "object_total"],
            ascending=[False, False, False],
        )
        .head(top_n)["object_id"]
    )
    counts = counts.loc[counts["object_id"].isin(top_ids)].copy()
    counts["object_label"] = counts.apply(
        lambda row: f"{_clean(row['canonical_name'])} (N={_human_count(row['object_total'])})",
        axis=1,
    )
    return counts.sort_values(
        ["non_background_edges", "object_total", "canonical_name", "final_intent"],
        ascending=[False, False, True, True],
    )


def build_final_v2_infrastructure_scores(edges: pd.DataFrame) -> pd.DataFrame:
    """Build clean infrastructure quadrant scores from unique object edges."""
    if edges.empty:
        return pd.DataFrame()
    counts = (
        edges.groupby(["object_id", "canonical_name", "object_type", "final_intent"], dropna=False)
        .size()
        .reset_index(name="rows")
    )
    pivot = counts.pivot_table(
        index=["object_id", "canonical_name", "object_type"],
        columns="final_intent",
        values="rows",
        fill_value=0,
        aggfunc="sum",
    ).reset_index()
    for intent in INTENT_ORDER:
        if intent not in pivot:
            pivot[intent] = 0
    pivot["total_edges"] = pivot[INTENT_ORDER].sum(axis=1)
    pivot["non_background_edges"] = pivot[EVIDENCE_INTENTS].sum(axis=1)
    denom = pivot["non_background_edges"].replace(0, float("nan"))
    pivot["uses_share_non_background"] = (pivot["uses"] / denom).fillna(0)
    pivot["compares_share_non_background"] = (pivot["compares_against"] / denom).fillna(0)
    pivot["critiques_share_non_background"] = (pivot["critiques"] / denom).fillna(0)
    pivot["background_share"] = (
        pivot["background"] / pivot["total_edges"].replace(0, float("nan"))
    ).fillna(0)
    return pivot.sort_values("total_edges", ascending=False)


def build_final_v2_ranking_reversal(
    contexts: pd.DataFrame,
    labels: pd.DataFrame,
) -> pd.DataFrame:
    """Compute cited-paper citation-context rank vs evidence-use rank."""
    context_columns = ["resolved_cited_acl_id", "resolved_cited_title", "context_id"]
    contexts_small = _ensure_columns(contexts.copy(), context_columns)[context_columns]
    for column in ("resolved_cited_acl_id", "resolved_cited_title", "context_id"):
        contexts_small[column] = contexts_small[column].map(_clean)
    contexts_small = contexts_small.loc[contexts_small["resolved_cited_title"].ne("")]
    total_counts = (
        contexts_small.groupby(["resolved_cited_acl_id", "resolved_cited_title"], dropna=False)
        .agg(total_strong_contexts=("context_id", "nunique"))
        .reset_index()
    )
    label_columns = [
        "resolved_cited_acl_id",
        "resolved_cited_title",
        "context_id",
        "final_intent",
    ]
    label_small = _ensure_columns(labels.copy(), label_columns)[label_columns]
    for column in ("resolved_cited_acl_id", "resolved_cited_title", "context_id", "final_intent"):
        label_small[column] = label_small[column].map(_clean)
    label_small = label_small.loc[label_small["resolved_cited_title"].ne("")]
    intent_counts = (
        label_small.groupby(
            ["resolved_cited_acl_id", "resolved_cited_title", "final_intent"],
            dropna=False,
        )
        .size()
        .reset_index(name="rows")
    )
    pivot = intent_counts.pivot_table(
        index=["resolved_cited_acl_id", "resolved_cited_title"],
        columns="final_intent",
        values="rows",
        fill_value=0,
        aggfunc="sum",
    ).reset_index()
    joined = total_counts.merge(
        pivot,
        on=["resolved_cited_acl_id", "resolved_cited_title"],
        how="left",
    )
    for intent in INTENT_ORDER:
        if intent not in joined:
            joined[intent] = 0
    joined[INTENT_ORDER] = joined[INTENT_ORDER].fillna(0).astype(int)
    joined["evidence_use_count"] = joined[EVIDENCE_INTENTS].sum(axis=1)
    joined["background_share"] = (
        joined["background"] / joined["total_strong_contexts"].replace(0, pd.NA)
    ).fillna(0)
    joined["evidence_use_share"] = (
        joined["evidence_use_count"] / joined["total_strong_contexts"].replace(0, pd.NA)
    ).fillna(0)
    joined["rank_by_total_strong_contexts"] = joined["total_strong_contexts"].rank(
        method="min",
        ascending=False,
    )
    joined["rank_by_evidence_use_count"] = joined["evidence_use_count"].rank(
        method="min",
        ascending=False,
    )
    joined["rank_difference"] = (
        joined["rank_by_total_strong_contexts"] - joined["rank_by_evidence_use_count"]
    )
    joined["absolute_rank_difference"] = joined["rank_difference"].abs()
    joined["reversal_type"] = "balanced"
    joined.loc[joined["rank_difference"].gt(0), "reversal_type"] = "evidence-use riser"
    joined.loc[joined["rank_difference"].lt(0), "reversal_type"] = "citation-volume riser"
    return joined.sort_values("absolute_rank_difference", ascending=False)


def build_final_v2_phase_transition(labels: pd.DataFrame) -> pd.DataFrame:
    """Build Phase-1 to Phase-2 transition counts and row percentages."""
    columns = ["primary_candidate_intent", "final_intent"]
    frame = _ensure_columns(labels.copy(), columns)[columns]
    frame["source_intent"] = frame["primary_candidate_intent"].map(_clean)
    frame["target_intent"] = frame["final_intent"].map(_clean)
    frame = frame.loc[frame["source_intent"].ne("") & frame["target_intent"].ne("")]
    counts = (
        frame.groupby(["source_intent", "target_intent"], dropna=False)
        .size()
        .reset_index(name="rows")
    )
    totals = counts.groupby("source_intent")["rows"].transform("sum")
    counts["source_total"] = totals
    counts["row_share"] = counts["rows"] / totals
    return counts.sort_values(["source_intent", "target_intent"])


def build_final_v2_critique_bottleneck_matrix(edges: pd.DataFrame) -> pd.DataFrame:
    """Build critique bottleneck counts and normalized rates by object type."""
    critiques = edges.loc[edges["final_intent"].eq("critiques")].copy()
    if critiques.empty:
        return pd.DataFrame(columns=["object_type", "bottleneck_family", "rows", "row_share"])
    critiques["bottleneck_family"] = critiques["evidence_span"].map(classify_bottleneck_family)
    counts = (
        critiques.groupby(["object_type", "bottleneck_family"], dropna=False)
        .size()
        .reset_index(name="rows")
    )
    totals = counts.groupby("object_type")["rows"].transform("sum")
    counts["object_type_total"] = totals
    counts["row_share"] = counts["rows"] / totals
    return counts.sort_values(["object_type_total", "object_type"], ascending=[False, True])


def classify_bottleneck_family(text: str) -> str:
    """Classify critique spans into a small bottleneck taxonomy."""
    lowered = _clean(text).casefold()
    if any(token in lowered for token in ("cannot", "can not", "unable", "fail", "fails")):
        return "fail / cannot / unable"
    if any(token in lowered for token in ("limitation", "limited", "drawback", "problem")):
        return "limitation / drawback"
    if any(token in lowered for token in ("poor", "worse", "low quality")):
        return "poor performance"
    if any(token in lowered for token in ("bleu", "rouge", "metric", "score", "does not capture")):
        return "metric limitation"
    if any(token in lowered for token in ("requires", "required", "resource", "data", "parallel")):
        return "data/resource requirement"
    if any(token in lowered for token in ("generaliz", "scalab", "domain")):
        return "generalization / scalability"
    return "other"


def build_final_v2_metric_benchmark_role_profiles(edges: pd.DataFrame) -> pd.DataFrame:
    """Build role profiles for named metrics and benchmarks."""
    if edges.empty:
        return pd.DataFrame(columns=_role_profile_columns("metric_benchmark"))
    rows = []
    for edge in edges.to_dict(orient="records"):
        display_name = _metric_benchmark_display_name(_clean(edge.get("canonical_name")))
        if not display_name:
            continue
        rows.append({**edge, "metric_benchmark": display_name})
    frame = pd.DataFrame(rows)
    if frame.empty:
        return pd.DataFrame(columns=_role_profile_columns("metric_benchmark"))
    counts = (
        frame.groupby(["metric_benchmark", "final_intent"], dropna=False)
        .size()
        .reset_index(name="rows")
    )
    totals = counts.groupby("metric_benchmark")["rows"].transform("sum")
    counts["metric_benchmark_total"] = totals
    counts["row_share"] = counts["rows"] / totals
    counts["compare_critique_share"] = counts.groupby("metric_benchmark")["rows"].transform(
        lambda values: 0.0,
    )
    compare_critique = (
        counts.loc[counts["final_intent"].isin(["compares_against", "critiques"])]
        .groupby("metric_benchmark")["rows"]
        .sum()
        .rename("compare_critique_edges")
        .reset_index()
    )
    counts = counts.merge(compare_critique, on="metric_benchmark", how="left")
    counts["compare_critique_edges"] = counts["compare_critique_edges"].fillna(0)
    counts["compare_critique_share"] = (
        counts["compare_critique_edges"] / counts["metric_benchmark_total"].replace(0, pd.NA)
    ).fillna(0)
    return counts.sort_values(
        ["compare_critique_share", "metric_benchmark_total", "metric_benchmark"],
        ascending=[False, False, True],
    )


def build_final_v2_evidence_cards(
    edges: pd.DataFrame,
    ranking_reversal: pd.DataFrame,
) -> pd.DataFrame:
    """Create the final_v2 60-card evidence sample."""
    quotas = {
        "uses": 10,
        "compares_against": 10,
        "extends": 10,
        "critiques": 10,
        "applies": 5,
        "background": 10,
    }
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for intent, quota in quotas.items():
        subset = edges.loc[edges["final_intent"].eq(intent)].copy()
        subset = subset.sort_values(["confidence", "context_id"], ascending=[False, True])
        for row in subset.to_dict(orient="records"):
            key = (_clean(row.get("context_id")), _clean(row.get("object_id")), intent)
            if key in seen:
                continue
            rows.append(_evidence_card_from_edge(row, "role quota"))
            seen.add(key)
            if sum(1 for item in rows if item["final_intent"] == intent) >= quota:
                break
    top_reversal_titles = set(
        ranking_reversal.sort_values("absolute_rank_difference", ascending=False)
        .head(50)["resolved_cited_title"]
        .map(_clean)
    )
    reversal_edges = edges.loc[edges["resolved_cited_title"].map(_clean).isin(top_reversal_titles)]
    reversal_edges = reversal_edges.sort_values(
        ["confidence", "context_id"],
        ascending=[False, True],
    )
    added_reversals = 0
    for row in reversal_edges.to_dict(orient="records"):
        key = (
            _clean(row.get("context_id")),
            _clean(row.get("object_id")),
            _clean(row.get("final_intent")),
        )
        if key in seen:
            continue
        rows.append(_evidence_card_from_edge(row, "ranking reversal"))
        seen.add(key)
        added_reversals += 1
        if added_reversals >= 5:
            break
    if len(rows) < 60:
        backfill = edges.sort_values(["confidence", "context_id"], ascending=[False, True])
        for row in backfill.to_dict(orient="records"):
            key = (
                _clean(row.get("context_id")),
                _clean(row.get("object_id")),
                _clean(row.get("final_intent")),
            )
            if key in seen:
                continue
            rows.append(_evidence_card_from_edge(row, "backfill"))
            seen.add(key)
            if len(rows) >= 60:
                break
    return _ensure_columns(pd.DataFrame(rows).head(60), _evidence_card_columns())[
        _evidence_card_columns()
    ]


def build_final_v2_summary(
    *,
    pipeline: pd.DataFrame,
    labels: pd.DataFrame,
    excluded: pd.DataFrame,
    failed_diagnostics: pd.DataFrame,
    object_mentions: pd.DataFrame,
    edges: pd.DataFrame,
) -> pd.DataFrame:
    """Build final_v2 summary table."""
    counts = dict(zip(pipeline["step"], pipeline["count"], strict=False))
    rows = [
        ("full_strong_context_layer", counts.get("strong_contexts", 0)),
        ("full_object_mentions", len(object_mentions)),
        ("full_object_graph_candidates", counts.get("object_graph_candidates", 0)),
        ("phase2_high_medium_queue", counts.get("phase2_high_medium_queue", 0)),
        ("revalidated_phase2_rows", counts.get("revalidated_phase2_rows", 0)),
        ("analysis_ready_phase2_labels", len(labels)),
        ("excluded_revalidated_labels", len(excluded)),
        ("remaining_failed_phase2_rows", _remaining_failed_count(failed_diagnostics)),
        ("evidence_backed_object_edges", len(edges)),
        ("evidence_backed_object_nodes", edges["object_id"].nunique() if not edges.empty else 0),
        ("edge_unit", "unique(context_id, object_id, final_intent)"),
        ("object_policy", "top 3 eligible object candidates per context"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value"])


def write_final_v2_figures(
    *,
    pipeline: pd.DataFrame,
    section_profile: pd.DataFrame,
    object_profile: pd.DataFrame,
    infrastructure: pd.DataFrame,
    ranking_reversal: pd.DataFrame,
    transition: pd.DataFrame,
    critique_matrix: pd.DataFrame,
    metric_profile: pd.DataFrame,
    figures_dir: Path,
    source_data_dir: Path,
) -> dict[str, str]:
    """Write final_v2 PNG/SVG figures and source CSVs."""
    figures_dir.mkdir(parents=True, exist_ok=True)
    source_data_dir.mkdir(parents=True, exist_ok=True)
    sources = {
        "f01_evidence_pipeline": pipeline,
        "f02_section_role_profile": section_profile,
        "f03_top_object_role_profiles": object_profile,
        "f04_infrastructure_quadrant_clean": infrastructure,
        "f05_ranking_reversal_lollipop": ranking_reversal.head(200),
        "f06_phase1_phase2_transition": transition,
        "f07_critique_bottleneck_matrix": critique_matrix,
        "f08_metric_benchmark_role_profiles": metric_profile,
    }
    for name, data in sources.items():
        data.to_csv(source_data_dir / f"{name}.csv", index=False)

    outputs: dict[str, str] = {}
    figure_specs = [
        ("f01_evidence_pipeline", plot_evidence_pipeline, pipeline),
        ("f02_section_role_profile", plot_section_role_profile, section_profile),
        ("f03_top_object_role_profiles", plot_object_role_profiles, object_profile),
        ("f04_infrastructure_quadrant_clean", plot_infrastructure_quadrant, infrastructure),
        ("f05_ranking_reversal_lollipop", plot_ranking_reversal_lollipop, ranking_reversal),
        ("f06_phase1_phase2_transition", plot_phase_transition_matrix, transition),
        ("f07_critique_bottleneck_matrix", plot_critique_bottleneck_matrix, critique_matrix),
        ("f08_metric_benchmark_role_profiles", plot_metric_benchmark_profiles, metric_profile),
    ]
    for name, plotter, data in figure_specs:
        png = figures_dir / f"{name}.png"
        svg = figures_dir / f"{name}.svg"
        plotter(data, png)
        plotter(data, svg)
        outputs[name] = str(png)
    return outputs


def build_final_v2_report(
    *,
    summary: pd.DataFrame,
    pipeline: pd.DataFrame,
    section_profile: pd.DataFrame,
    object_profile: pd.DataFrame,
    infrastructure: pd.DataFrame,
    ranking_reversal: pd.DataFrame,
    transition: pd.DataFrame,
    critique_matrix: pd.DataFrame,
    metric_profile: pd.DataFrame,
    evidence_cards: pd.DataFrame,
    figure_paths: dict[str, str],
    cards_path: Path,
) -> str:
    """Build readable GitHub markdown for final_v2 results."""
    figure_rows = [
        {
            "figure": name,
            "path": path,
            "source_csv": f"figures/final_v2/source_data/{name}.csv",
            "data_layer": _figure_data_layer(name),
        }
        for name, path in figure_paths.items()
    ]
    findings = [
        "- The project now has 229,751 grounded analysis-ready Phase-2 labels from "
        "the full high/medium Phase-1 queue.",
        "- Phase-2 covers the routed high/medium queue, not all 1.18M strong contexts; "
        "the full deterministic layers are still reported in the evidence pipeline.",
        "- The v2 object edge unit is unique(context_id, object_id, final_intent), "
        "with pseudo object category names excluded.",
        "- Background dominates many citation contexts, so v2 object figures use role "
        "profiles instead of raw count heatmaps.",
        "- Metrics and benchmarks are separated into role-profile plots, making "
        "comparison and critique anchors easier to see.",
        "- Ranking reversal highlights the difference between citation volume and "
        "direct evidence of use, comparison, extension, critique, or application.",
    ]
    return format_markdown_sections(
        [
            "# Final SciSci-CiteEvidence Results V2",
            (
                "This report is the presentation-ready final analysis for the course-scale "
                "SciSci-CiteEvidence MVP. It uses final analysis-ready Phase-2 labels, "
                "not pilot labels, and it does not call any API."
            ),
            "## Data Layers",
            (
                "The full strong-context layer contains 1,184,634 resolved citation "
                "contexts. Object matching was run on that full layer. Phase-2 structured "
                "semantic labeling was run on the full high/medium Phase-1 LLM queue, "
                "not on every strong context."
            ),
            _table(summary),
            "## Main Findings",
            "\n".join(findings),
            "## Figure Files",
            _table(pd.DataFrame(figure_rows)),
            "## Figure 1: Evidence Pipeline",
            (
                "Data layer: full deterministic pipeline counts plus final Phase-2 "
                "Batch outputs. The marker-component stage can exceed the context "
                "stage because grouped citations split into multiple marker components. "
                "Do not interpret this as a monotonic sample-retention funnel."
            ),
            _table(pipeline),
            "## Figure 2: Section Role Profile",
            (
                "Data layer: final analysis-ready Phase-2 labels. Rows are known "
                "normalized sections and bars show row-normalized role percentages. "
                "Unknown sections are retained in the source CSV but excluded from the "
                "main plotted panel."
            ),
            _table(section_profile.head(80)),
            "## Figure 3: Top Object Role Profiles",
            (
                "Data layer: unique context-object-intent edges. This figure is sorted "
                "by non-background evidence so object roles are not visually flattened "
                "by background mentions."
            ),
            _table(object_profile.head(80)),
            "## Figure 4: Infrastructure Quadrant",
            (
                "Data layer: unique object-use edges. X and Y show uses and comparison "
                "shares among non-background evidence; bubble size encodes total edge "
                "volume on a log-like scale."
            ),
            _table(infrastructure.head(40)),
            "## Figure 5: Ranking Reversal",
            (
                "Data layer: total strong citation contexts for citation volume and "
                "analysis-ready Phase-2 labels for evidence-use counts. This separates "
                "papers cited frequently as background from papers with direct evidence "
                "of use, comparison, extension, critique, or application."
            ),
            _table(ranking_reversal.head(40)),
            "## Figure 6: Phase-1 To Phase-2 Transition",
            (
                "Data layer: analysis-ready Phase-2 labels. Counts and row percentages "
                "show how deterministic candidate intents map into final structured labels."
            ),
            _table(transition),
            "## Figure 7: Critique Bottleneck Matrix",
            (
                "Data layer: critique edges only. Bottleneck families are heuristic "
                "summaries of exact grounded evidence spans, not manually validated "
                "taxonomy labels."
            ),
            _table(critique_matrix.head(80)),
            "## Figure 8: Metric And Benchmark Role Profiles",
            (
                "Data layer: unique object-use edges for named metrics and benchmarks. "
                "This replaces the earlier count heatmap with a role-profile view."
            ),
            _table(metric_profile),
            "## Evidence Cards",
            f"- Evidence card CSV: `{cards_path}`",
            _table(evidence_cards.head(20)),
            "## Limitations",
            "\n".join(
                [
                    "- ACL-OCL coverage is ACL-centric and not a complete NLP literature graph.",
                    "- The object registry is seed-based, so object coverage is incomplete.",
                    "- Section labels depend on recoverable section metadata.",
                    "- Failed, ambiguous, or ungrounded Phase-2 rows are excluded.",
                    "- Low/none Phase-1 contexts were not Phase-2 labeled in this run.",
                    "- Phase-2 labels are LLM-assisted structured evidence labels, "
                    "not human gold annotations.",
                ]
            ),
        ]
    )


def plot_evidence_pipeline(data: pd.DataFrame, output: Path) -> None:
    _apply_plot_style()
    plot_data = data.loc[~data["step"].eq("remaining_failed_phase2_rows")].copy()
    fig, ax = plt.subplots(figsize=(15.5, 5.6))
    ax.set_axis_off()
    if plot_data.empty:
        ax.text(0.5, 0.5, "No pipeline data", ha="center", va="center")
        _save_figure(fig, output)
        return
    max_count = max(float(plot_data["count"].max()), 1.0)
    for index, (_, row) in enumerate(plot_data.iterrows()):
        height = 0.38 + 0.34 * (float(row["count"]) / max_count) ** 0.35
        y = 0.56 - height / 2
        color = "#3B7EA1" if index < 5 else "#5B9A57"
        box = patches.FancyBboxPatch(
            (index - 0.43, y),
            0.86,
            height,
            boxstyle="round,pad=0.02,rounding_size=0.03",
            linewidth=1.0,
            facecolor=color,
            edgecolor="#333333",
            alpha=0.92,
        )
        ax.add_patch(box)
        ax.text(
            index,
            0.62,
            _clean(row["count_label"]),
            ha="center",
            va="center",
            color="white",
            fontsize=13,
            fontweight="bold",
        )
        ax.text(
            index,
            0.47,
            _clean(row["display_label"]),
            ha="center",
            va="center",
            color="white",
            fontsize=8.2,
            wrap=True,
        )
        if index > 0:
            retention = float(row["retention_from_previous"])
            ax.annotate(
                "",
                xy=(index - 0.48, 0.56),
                xytext=(index - 0.78, 0.56),
                arrowprops={"arrowstyle": "->", "lw": 1.2, "color": "#555555"},
            )
            ax.text(
                index - 0.64,
                0.74,
                f"{retention:.0%}",
                ha="center",
                va="center",
                fontsize=8,
                color="#333333",
            )
    ax.text(
        0,
        1.03,
        "Evidence pipeline from full deterministic extraction to final "
        "evidence-backed object-use edges",
        ha="left",
        va="bottom",
        fontsize=15,
        fontweight="bold",
    )
    ax.text(
        0,
        0.06,
        "Note: marker components can exceed contexts because grouped citations "
        "split into components.",
        ha="left",
        va="center",
        fontsize=9,
        color="#555555",
    )
    ax.set_xlim(-0.7, len(plot_data) - 0.3)
    ax.set_ylim(0, 1.1)
    _save_figure(fig, output)


def plot_section_role_profile(data: pd.DataFrame, output: Path) -> None:
    plot_data = data.loc[~data["is_unknown_section"].map(_bool_value)].copy()
    plot_data = _top_groups_by_total(
        plot_data,
        group_column="normalized_section",
        total_column="section_total",
        limit=22,
    )
    plot_data = plot_data.sort_values("section_total", ascending=True)
    _plot_100pct_stacked_barh(
        data=plot_data,
        group_column="section_label",
        title="Citation Roles By Section",
        output=output,
        max_rows=22,
    )


def plot_object_role_profiles(data: pd.DataFrame, output: Path) -> None:
    plot_data = data.sort_values(
        ["non_background_edges", "object_total"],
        ascending=[True, True],
    )
    _plot_100pct_stacked_barh(
        data=plot_data,
        group_column="object_label",
        title="Top Object Role Profiles",
        output=output,
        max_rows=20,
    )


def plot_infrastructure_quadrant(data: pd.DataFrame, output: Path) -> None:
    _apply_plot_style()
    fig, ax = plt.subplots(figsize=(10.5, 7))
    if data.empty:
        ax.text(0.5, 0.5, "No infrastructure data", ha="center", va="center")
        ax.set_axis_off()
        _save_figure(fig, output)
        return
    plot_data = data.head(40).copy()
    sizes = (plot_data["total_edges"].clip(lower=1).pow(0.5) * 18).clip(70, 1200)
    for object_type, subset in plot_data.groupby("object_type", dropna=False):
        color = OBJECT_TYPE_COLORS.get(_clean(object_type), "#6C757D")
        ax.scatter(
            subset["uses_share_non_background"],
            subset["compares_share_non_background"],
            s=sizes.loc[subset.index],
            alpha=0.72,
            color=color,
            edgecolors="white",
            linewidths=0.7,
            label=_display_label(object_type),
        )
    x_median = float(plot_data["uses_share_non_background"].median())
    y_median = float(plot_data["compares_share_non_background"].median())
    ax.axvline(x_median, color="#666666", lw=1.0, ls="--", alpha=0.65)
    ax.axhline(y_median, color="#666666", lw=1.0, ls="--", alpha=0.65)
    label_rows = plot_data.sort_values("total_edges", ascending=False).head(12)
    offsets = [(6, 8), (8, -10), (-34, 8), (6, -14), (-38, -12), (10, 12)]
    for index, (_, row) in enumerate(label_rows.iterrows()):
        ax.annotate(
            _truncate(_clean(row.get("canonical_name")), 24),
            (
                float(row.get("uses_share_non_background") or 0),
                float(row.get("compares_share_non_background") or 0),
            ),
            fontsize=8,
            xytext=offsets[index % len(offsets)],
            textcoords="offset points",
            bbox={
                "boxstyle": "round,pad=0.1",
                "facecolor": "white",
                "edgecolor": "none",
                "alpha": 0.7,
            },
        )
    quadrant_box = {
        "boxstyle": "round,pad=0.22",
        "facecolor": "white",
        "edgecolor": "#DDDDDD",
        "alpha": 0.86,
    }
    ax.text(
        0.03,
        0.96,
        "Benchmark / comparison anchors",
        transform=ax.transAxes,
        fontsize=8,
        bbox=quadrant_box,
    )
    ax.text(
        0.66,
        0.05,
        "High-use infrastructure",
        transform=ax.transAxes,
        fontsize=8,
        bbox=quadrant_box,
    )
    ax.set_xlabel("Uses share among non-background edges")
    ax.set_ylabel("Compares-against share among non-background edges")
    ax.set_title("Infrastructure Quadrant")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=8, frameon=False)
    _save_figure(fig, output)


def plot_ranking_reversal_lollipop(data: pd.DataFrame, output: Path) -> None:
    _apply_plot_style()
    candidates = data.loc[data["total_strong_contexts"].ge(10)].copy()
    candidates = candidates.sort_values("absolute_rank_difference", ascending=False).head(20)
    candidates = candidates.iloc[::-1].reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(12, 8))
    if candidates.empty:
        ax.text(0.5, 0.5, "No ranking reversal data", ha="center", va="center")
        ax.set_axis_off()
        _save_figure(fig, output)
        return
    y_positions = range(len(candidates))
    ax.set_xlim(-0.12, 1.12)
    ax.set_ylim(-0.8, len(candidates) - 0.2)
    ax.axvline(0, color="#333333", lw=1)
    ax.axvline(1, color="#333333", lw=1)
    for y, row in zip(y_positions, candidates.to_dict(orient="records"), strict=False):
        color = "#5B9A57" if row["rank_difference"] > 0 else "#B54A5A"
        ax.plot([0, 1], [y, y], color=color, alpha=0.45, lw=2)
        ax.scatter([0, 1], [y, y], color=[color, color], s=60, zorder=3)
        ax.text(
            -0.035,
            y,
            f"#{int(row['rank_by_total_strong_contexts'])}",
            ha="right",
            va="center",
            fontsize=8,
        )
        ax.text(
            1.035,
            y,
            f"#{int(row['rank_by_evidence_use_count'])}",
            ha="left",
            va="center",
            fontsize=8,
        )
        ax.text(
            0.5,
            y,
            _truncate(
                _clean(row.get("resolved_cited_title")).replace("{", "").replace("}", ""),
                58,
            ),
            ha="center",
            va="center",
            fontsize=8,
            bbox={"boxstyle": "round,pad=0.15", "facecolor": "white", "edgecolor": "none"},
        )
    ax.text(0, len(candidates) - 0.02, "Citation-context rank", ha="center", fontsize=10)
    ax.text(1, len(candidates) - 0.02, "Evidence-use rank", ha="center", fontsize=10)
    ax.set_title("Citation Volume vs Evidence-Use Ranking Reversal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    _save_figure(fig, output)


def plot_phase_transition_matrix(data: pd.DataFrame, output: Path) -> None:
    _apply_plot_style()
    fig, ax = plt.subplots(figsize=(9.5, 6.3))
    if data.empty:
        ax.text(0.5, 0.5, "No transition data", ha="center", va="center")
        ax.set_axis_off()
        _save_figure(fig, output)
        return
    matrix = data.pivot_table(
        index="source_intent",
        columns="target_intent",
        values="row_share",
        fill_value=0,
        aggfunc="sum",
    )
    counts = data.pivot_table(
        index="source_intent",
        columns="target_intent",
        values="rows",
        fill_value=0,
        aggfunc="sum",
    )
    matrix = matrix.reindex(index=[i for i in INTENT_ORDER if i in matrix.index])
    matrix = matrix[[i for i in INTENT_ORDER if i in matrix.columns]]
    counts = counts.reindex(index=matrix.index, columns=matrix.columns, fill_value=0)
    image = ax.imshow(matrix.to_numpy(dtype=float), aspect="auto", cmap="YlGnBu", vmin=0, vmax=1)
    ax.set_xticks(range(len(matrix.columns)))
    ax.set_xticklabels([_display_label(col) for col in matrix.columns], rotation=35, ha="right")
    ax.set_yticks(range(len(matrix.index)))
    ax.set_yticklabels([_display_label(row) for row in matrix.index])
    for row_idx, source in enumerate(matrix.index):
        for col_idx, target in enumerate(matrix.columns):
            value = float(matrix.loc[source, target])
            count = int(counts.loc[source, target])
            if count <= 0:
                continue
            color = "white" if value > 0.45 else "#222222"
            ax.text(
                col_idx,
                row_idx,
                f"{_human_count(count)}\n{value:.0%}",
                ha="center",
                va="center",
                fontsize=7,
                color=color,
            )
    ax.set_title("Phase-1 Candidate Intent to Final Phase-2 Intent")
    ax.set_xlabel("Final Phase-2 intent")
    ax.set_ylabel("Phase-1 primary candidate")
    fig.colorbar(image, ax=ax, fraction=0.03, pad=0.02, label="Row percentage")
    _save_figure(fig, output)


def plot_critique_bottleneck_matrix(data: pd.DataFrame, output: Path) -> None:
    _apply_plot_style()
    fig, ax = plt.subplots(figsize=(11, 5.8))
    if data.empty:
        ax.text(0.5, 0.5, "No critique bottleneck data", ha="center", va="center")
        ax.set_axis_off()
        _save_figure(fig, output)
        return
    matrix = data.pivot_table(
        index="object_type",
        columns="bottleneck_family",
        values="rows",
        fill_value=0,
        aggfunc="sum",
    )
    matrix = matrix.reindex(columns=[col for col in BOTTLENECK_FAMILIES if col in matrix.columns])
    matrix = matrix.loc[matrix.sum(axis=1).sort_values(ascending=False).index]
    image = ax.imshow(matrix.to_numpy(dtype=float), aspect="auto", cmap="OrRd")
    ax.set_xticks(range(len(matrix.columns)))
    ax.set_xticklabels([_display_label(col) for col in matrix.columns], rotation=35, ha="right")
    ax.set_yticks(range(len(matrix.index)))
    ax.set_yticklabels([_display_label(row) for row in matrix.index])
    for row_idx, source in enumerate(matrix.index):
        for col_idx, target in enumerate(matrix.columns):
            count = int(matrix.loc[source, target])
            if count:
                ax.text(col_idx, row_idx, _human_count(count), ha="center", va="center", fontsize=7)
    ax.set_title("Critique Bottleneck Matrix")
    ax.set_xlabel("Bottleneck family")
    ax.set_ylabel("Object type")
    fig.colorbar(image, ax=ax, fraction=0.03, pad=0.02, label="Critique edges")
    _save_figure(fig, output)


def plot_metric_benchmark_profiles(data: pd.DataFrame, output: Path) -> None:
    plot_data = data.sort_values(
        ["compare_critique_share", "metric_benchmark_total"],
        ascending=[True, True],
    )
    plot_data["metric_label"] = plot_data.apply(
        lambda row: (
            f"{_clean(row['metric_benchmark'])} "
            f"(N={_human_count(row['metric_benchmark_total'])})"
        ),
        axis=1,
    )
    _plot_100pct_stacked_barh(
        data=plot_data,
        group_column="metric_label",
        title="Metric and Benchmark Role Profiles",
        output=output,
        max_rows=12,
    )


def _plot_100pct_stacked_barh(
    *,
    data: pd.DataFrame,
    group_column: str,
    title: str,
    output: Path,
    max_rows: int,
) -> None:
    _apply_plot_style()
    fig_height = max(4.8, min(10.8, data[group_column].nunique() * 0.42 + 1.8))
    fig, ax = plt.subplots(figsize=(11.5, fig_height))
    if data.empty:
        ax.text(0.5, 0.5, "No role-profile data", ha="center", va="center")
        ax.set_axis_off()
        _save_figure(fig, output)
        return
    groups = data[group_column].drop_duplicates().tail(max_rows).tolist()
    pivot = data.pivot_table(
        index=group_column,
        columns="final_intent",
        values="row_share",
        fill_value=0,
        aggfunc="sum",
    )
    pivot = pivot.reindex(groups)
    pivot = pivot[[intent for intent in INTENT_ORDER if intent in pivot.columns]]
    left = pd.Series(0.0, index=pivot.index)
    for intent in pivot.columns:
        values = pivot[intent].astype(float)
        ax.barh(
            pivot.index,
            values,
            left=left,
            label=_display_label(intent),
            color=INTENT_COLORS.get(intent, "#999999"),
        )
        for y_idx, (group, value) in enumerate(values.items()):
            if value >= 0.08:
                ax.text(
                    left.loc[group] + value / 2,
                    y_idx,
                    f"{value:.0%}",
                    ha="center",
                    va="center",
                    fontsize=7,
                    color="white" if intent != "background" else "#222222",
                )
        left = left + values
    ax.set_xlim(0, 1)
    ax.set_xlabel("Share of evidence-backed labels")
    ax.set_title(title)
    ax.xaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
    ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), frameon=False, fontsize=8)
    _save_figure(fig, output)


def _save_figure(fig: Any, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _apply_plot_style() -> None:
    plt.rcParams.update(
        {
            "font.size": 9,
            "axes.titlesize": 13,
            "axes.labelsize": 10,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 8,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.grid": False,
            "savefig.facecolor": "white",
        }
    )


def _figure_data_layer(name: str) -> str:
    layers = {
        "f01_evidence_pipeline": "Full deterministic layers plus final Phase-2 Batch counts.",
        "f02_section_role_profile": "Final analysis-ready Phase-2 labels by section.",
        "f03_top_object_role_profiles": "Unique context-object-intent edge role profiles.",
        "f04_infrastructure_quadrant_clean": "Unique object-use edge infrastructure scores.",
        "f05_ranking_reversal_lollipop": "Strong context totals plus Phase-2 evidence-use counts.",
        "f06_phase1_phase2_transition": "Phase-1 primary intent to Phase-2 final intent.",
        "f07_critique_bottleneck_matrix": "Final critique edges grouped by cue family.",
        "f08_metric_benchmark_role_profiles": "Metric and benchmark object-use edges.",
    }
    return layers.get(name, "Final v2 analysis layer.")


def _evidence_card_from_edge(row: dict[str, Any], card_type: str) -> dict[str, Any]:
    return {
        "card_type": card_type,
        "context_id": _clean(row.get("context_id")),
        "object_name": _clean(row.get("canonical_name")),
        "final_intent": _clean(row.get("final_intent")),
        "final_object_type": _clean(row.get("final_object_type")),
        "final_relation_subtype": _clean(row.get("final_relation_subtype")),
        "method_edge_type": _clean(row.get("method_edge_type")),
        "resolved_cited_title": _clean(row.get("resolved_cited_title")),
        "normalized_section": _clean(row.get("normalized_section")),
        "sentence_text": _clean(row.get("sentence_text")),
        "evidence_span": _clean(row.get("evidence_span")),
        "confidence": _float_value(row.get("confidence")),
        "why_interesting": _clean(row.get("rationale_short")),
    }


def _evidence_card_columns() -> list[str]:
    return [
        "card_type",
        "context_id",
        "object_name",
        "final_intent",
        "final_object_type",
        "final_relation_subtype",
        "method_edge_type",
        "resolved_cited_title",
        "normalized_section",
        "sentence_text",
        "evidence_span",
        "confidence",
        "why_interesting",
    ]


def _edge_columns() -> list[str]:
    return [
        "context_id",
        "source_context_id",
        "object_id",
        "canonical_name",
        "object_type",
        "object_category",
        "final_intent",
        "final_object_type",
        "final_relation_subtype",
        "method_edge_type",
        "primary_candidate_intent",
        "normalized_section",
        "raw_section_name",
        "resolved_cited_acl_id",
        "resolved_cited_title",
        "resolved_cited_year",
        "resolved_cited_authors",
        "sentence_text",
        "context_window_s3",
        "evidence_span",
        "confidence",
        "rationale_short",
        "object_confidence",
        "matched_in",
        "edge_unit",
    ]


def _role_profile_columns(prefix: str) -> list[str]:
    return [prefix, "final_intent", "rows", f"{prefix}_total", "row_share"]


def _metric_benchmark_display_name(name: str) -> str:
    lowered = name.casefold()
    for display_name, aliases in METRIC_BENCHMARK_PATTERNS:
        if any(alias in lowered for alias in aliases):
            return display_name
    return ""


def _top_groups_by_total(
    data: pd.DataFrame,
    *,
    group_column: str,
    total_column: str,
    limit: int,
) -> pd.DataFrame:
    if data.empty:
        return data
    top_groups = (
        data[[group_column, total_column]]
        .drop_duplicates()
        .sort_values(total_column, ascending=False)
        .head(limit)[group_column]
    )
    return data.loc[data[group_column].isin(top_groups)].copy()


def _matched_in_priority(value: Any) -> int:
    text = _clean(value).casefold()
    if "sentence" in text:
        return 3
    if "context_window" in text:
        return 2
    if "neighbor" in text:
        return 1
    return 0


def _remaining_failed_count(failed_diagnostics: pd.DataFrame) -> int:
    if failed_diagnostics.empty:
        return 0
    if "revalidated" in failed_diagnostics:
        return int((~failed_diagnostics["revalidated"].map(_bool_value)).sum())
    return int(len(failed_diagnostics))


def _optional_parquet_row_count(path: str | Path) -> int | None:
    parquet_path = Path(path)
    if not parquet_path.exists():
        return None
    return int(pq.ParquetFile(parquet_path).metadata.num_rows)


def _evidence_span_grounded(row: pd.Series) -> bool:
    evidence = _clean(row.get("evidence_span"))
    if not evidence:
        return False
    return evidence in _clean(row.get("sentence_text")) or evidence in _clean(
        row.get("context_window_s3")
    )


def _bool_series(frame: pd.DataFrame, column: str) -> pd.Series:
    if column not in frame:
        return pd.Series(False, index=frame.index)
    return frame[column].map(_bool_value)


def _bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    try:
        if pd.isna(value):
            return False
    except (TypeError, ValueError):
        return False
    return str(value).strip().casefold() in {"true", "1", "yes"}


def _float_value(value: Any) -> float:
    if value is None:
        return 0.0
    try:
        if pd.isna(value):
            return 0.0
    except (TypeError, ValueError):
        return 0.0
    return float(value)


def _safe_rate(numerator: int | float, denominator: int | float) -> float:
    return float(numerator / denominator) if denominator else 0.0


def _human_count(value: Any) -> str:
    number = float(value)
    if abs(number) >= 1_000_000:
        return f"{number / 1_000_000:.2f}M"
    if abs(number) >= 100_000:
        return f"{number / 1_000:.1f}k"
    if abs(number) >= 10_000:
        return f"{number / 1_000:.1f}k"
    if abs(number) >= 1_000:
        return f"{number / 1_000:.1f}k"
    return str(int(number))


def _display_label(value: Any) -> str:
    return _clean(value).replace("_", " ").title()


def _truncate(value: str, length: int) -> str:
    text = _clean(value).replace("\n", " ")
    return text if len(text) <= length else f"{text[: length - 3]}..."


def _table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    return frame.to_markdown(index=False)


def _ensure_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        if column not in df:
            df[column] = ""
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
