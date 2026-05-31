"""Reproducible final-release analysis runner."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import pyarrow.parquet as pq

from citeevidence.final_release.figures import (
    plot_context_volume_vs_evidence_use_reversal,
    plot_critique_bottleneck_heatmap,
    plot_object_role_signature_map,
    plot_section_function_lift_heatmap,
)
from citeevidence.final_release.io import ensure_directory, write_source_csv
from citeevidence.final_release.metrics import (
    build_critique_bottleneck_matrix,
    build_critique_evidence_cards,
    build_object_role_signature,
    build_paper_evidence_use_table,
    build_ranking_reversal_plot_table,
    build_section_function_counts,
    build_section_function_lift,
    classify_object_role_quadrant,
)
from citeevidence.final_release.qa import (
    build_label_quality_summary,
    build_stratified_qa_sample,
    summarize_confidence_by_intent,
    summarize_failure_categories,
)
from citeevidence.final_release.report import (
    build_final_release_report,
    validate_final_release_report_text,
)

DEFAULT_PHASE2_LABELS_PATH = Path("data/processed/phase2_batch_analysis_ready_labels.parquet")
DEFAULT_EXCLUDED_LABELS_PATH = Path("data/processed/phase2_batch_excluded_labels.parquet")
DEFAULT_FAILED_DIAGNOSTICS_PATH = Path(
    "data/processed/phase2_batch_failed_validation_diagnostics.parquet"
)
DEFAULT_OBJECT_GRAPH_CANDIDATES_PATH = Path(
    "data/processed/object_graph_candidate_mentions.parquet"
)
DEFAULT_OBJECT_MENTIONS_PATH = Path("data/processed/object_mentions.parquet")
DEFAULT_CONTEXTS_PATH = Path("data/processed/analysis_ready_strong_contexts.parquet")
DEFAULT_PHASE1_PATH = Path("data/processed/phase1_citation_function_candidates.parquet")
DEFAULT_FINAL_RELEASE_REPORT = Path("reports/final_scisci_results_report_release.md")
DEFAULT_FINAL_RELEASE_FIGURES_DIR = Path("figures/final_release")
DEFAULT_FINAL_RELEASE_SOURCE_DATA_DIR = Path("figures/final_release/source_data")
DEFAULT_FINAL_RELEASE_EVIDENCE_CARDS = Path(
    "data/processed/final_release_evidence_cards.csv"
)
DEFAULT_FINAL_RELEASE_QA_SAMPLE = Path("data/processed/final_release_qa_sample.csv")

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

_PHASE2_COLUMNS = [
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
    "evidence_span_phase2",
    "analysis_evidence_span",
    "evidence_supports_label",
    "abstain",
    "phase2_confidence",
    "analysis_confidence",
    "confidence",
    "analysis_ready",
    "rationale_short",
]
_EXCLUDED_COLUMNS = ["context_id", "analysis_ready", "exclusion_reason"]
_FAILED_COLUMNS = [
    "context_id",
    "failed_validator_type",
    "validator_failure_type",
    "failure_type",
    "error_type",
    "validation_error",
    "revalidated",
]
_OBJECT_GRAPH_COLUMNS = [
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
_CONTEXT_COLUMNS = [
    "context_id",
    "resolved_cited_acl_id",
    "resolved_cited_title",
    "resolved_cited_year",
    "resolved_cited_authors",
]


def run_final_release_analysis(
    *,
    phase2_path: str | Path = DEFAULT_PHASE2_LABELS_PATH,
    excluded_path: str | Path = DEFAULT_EXCLUDED_LABELS_PATH,
    failed_diagnostics_path: str | Path = DEFAULT_FAILED_DIAGNOSTICS_PATH,
    object_graph_candidates_path: str | Path = DEFAULT_OBJECT_GRAPH_CANDIDATES_PATH,
    object_mentions_path: str | Path = DEFAULT_OBJECT_MENTIONS_PATH,
    contexts_path: str | Path = DEFAULT_CONTEXTS_PATH,
    phase1_path: str | Path = DEFAULT_PHASE1_PATH,
    out_report: str | Path = DEFAULT_FINAL_RELEASE_REPORT,
    figures_dir: str | Path = DEFAULT_FINAL_RELEASE_FIGURES_DIR,
    source_data_dir: str | Path = DEFAULT_FINAL_RELEASE_SOURCE_DATA_DIR,
    out_evidence_cards: str | Path = DEFAULT_FINAL_RELEASE_EVIDENCE_CARDS,
    out_qa_sample: str | Path = DEFAULT_FINAL_RELEASE_QA_SAMPLE,
    min_ranking_total_contexts: int = 20,
    min_ranking_evidence_use_count: int = 5,
) -> dict[str, object]:
    """Run final-release analyses from existing local derived data."""
    required_paths = {
        "phase2_path": Path(phase2_path),
        "object_graph_candidates_path": Path(object_graph_candidates_path),
        "contexts_path": Path(contexts_path),
    }
    for name, path in required_paths.items():
        if not path.exists():
            raise FileNotFoundError(f"Required final-release input does not exist ({name}): {path}")

    labels_raw = _read_parquet_columns(phase2_path, _PHASE2_COLUMNS)
    excluded = _read_optional_parquet(excluded_path, _EXCLUDED_COLUMNS)
    failed_diagnostics = _read_optional_parquet(failed_diagnostics_path, _FAILED_COLUMNS)
    object_graph = _read_parquet_columns(object_graph_candidates_path, _OBJECT_GRAPH_COLUMNS)
    contexts = _read_parquet_columns(contexts_path, _CONTEXT_COLUMNS)
    object_mentions_rows = _optional_parquet_row_count(object_mentions_path)
    phase1_rows = _optional_parquet_row_count(phase1_path)

    labels = prepare_final_release_labels(labels_raw)
    labels_with_risk = enrich_labels_with_object_risk(labels, object_graph)
    object_edges = build_final_release_object_edges(labels, object_graph)

    qa_summary = build_label_quality_summary(labels, excluded, failed_diagnostics)
    confidence_by_intent = summarize_confidence_by_intent(labels)
    failure_categories = summarize_failure_categories(failed_diagnostics)
    qa_sample = build_stratified_qa_sample(labels_with_risk)

    section_counts = build_section_function_counts(labels)
    section_lift = build_section_function_lift(section_counts)

    object_signature = build_object_role_signature(object_edges)
    object_roles = classify_object_role_quadrant(object_signature)

    paper_evidence_use = build_paper_evidence_use_table(contexts, labels)
    ranking_reversal = build_ranking_reversal_plot_table(
        paper_evidence_use,
        min_total_contexts=min_ranking_total_contexts,
        min_evidence_use_count=min_ranking_evidence_use_count,
    )

    critique_matrix = build_critique_bottleneck_matrix(object_edges)
    evidence_cards = build_critique_evidence_cards(object_edges)

    report_path = Path(out_report)
    figures_path = ensure_directory(figures_dir)
    source_path = ensure_directory(source_data_dir)
    cards_path = Path(out_evidence_cards)
    sample_path = Path(out_qa_sample)
    ensure_directory(report_path.parent)
    ensure_directory(cards_path.parent)
    ensure_directory(sample_path.parent)

    source_paths = {
        "qa_summary": write_source_csv(qa_summary, source_path / "qa_summary.csv"),
        "confidence_by_intent": write_source_csv(
            confidence_by_intent,
            source_path / "confidence_by_intent.csv",
        ),
        "failure_categories": write_source_csv(
            failure_categories,
            source_path / "failure_categories.csv",
        ),
        "section_function_lift": write_source_csv(
            section_lift,
            source_path / "section_function_lift.csv",
        ),
        "object_role_signature_map": write_source_csv(
            object_roles,
            source_path / "object_role_signatures.csv",
        ),
        "ranking_reversal": write_source_csv(
            ranking_reversal,
            source_path / "ranking_reversal.csv",
        ),
        "critique_bottleneck_heatmap": write_source_csv(
            critique_matrix,
            source_path / "critique_bottleneck_matrix.csv",
        ),
    }
    write_source_csv(evidence_cards, cards_path)
    write_source_csv(qa_sample, sample_path)

    figure_paths = _write_final_release_figures(
        section_lift=section_lift,
        object_roles=object_roles,
        paper_evidence_use=paper_evidence_use,
        critique_matrix=critique_matrix,
        figures_dir=figures_path,
    )
    report_text = build_final_release_report(
        qa_summary=qa_summary,
        confidence_by_intent=confidence_by_intent,
        failure_categories=failure_categories,
        section_lift=section_lift,
        object_roles=object_roles,
        ranking_reversal=ranking_reversal,
        critique_matrix=critique_matrix,
        evidence_cards=evidence_cards,
        figure_paths={key: _display_path(path) for key, path in figure_paths.items()},
        source_paths={key: _display_path(path) for key, path in source_paths.items()},
    )
    validation_issues = validate_final_release_report_text(report_text)
    if validation_issues:
        joined = ", ".join(validation_issues)
        raise ValueError(f"Final-release report failed guardrail validation: {joined}")
    report_path.write_text(report_text, encoding="utf-8")

    return {
        "analysis_ready_phase2_labels": int(len(labels)),
        "object_graph_candidate_mentions": int(len(object_graph)),
        "object_mentions_rows": object_mentions_rows,
        "phase1_rows": phase1_rows,
        "evidence_backed_object_edges": int(len(object_edges)),
        "evidence_backed_object_nodes": int(object_roles["object_id"].nunique())
        if "object_id" in object_roles
        else 0,
        "qa_sample_rows": int(len(qa_sample)),
        "evidence_cards": int(len(evidence_cards)),
        "ranking_reversal_rows": int(len(ranking_reversal)),
        "source_csv_count": len(source_paths),
        "figure_count": len(figure_paths),
        "report_path": str(report_path),
        "figures_dir": str(figures_path),
        "source_data_dir": str(source_path),
        "evidence_cards_path": str(cards_path),
        "qa_sample_path": str(sample_path),
        "report_validation_issues": validation_issues,
    }


def prepare_final_release_labels(labels: pd.DataFrame) -> pd.DataFrame:
    """Prepare final analysis-ready labels with unified evidence and confidence columns."""
    original_columns = set(labels.columns)
    frame = _ensure_columns(labels.copy(), _PHASE2_COLUMNS)
    text_columns = [
        column
        for column in _PHASE2_COLUMNS
        if column
        not in {
            "phase2_confidence",
            "analysis_confidence",
            "confidence",
            "abstain",
            "analysis_ready",
        }
    ]
    for column in text_columns:
        frame[column] = frame[column].map(_clean)

    frame["evidence_span"] = _coalesce_text(
        frame,
        ["analysis_evidence_span", "evidence_span_phase2", "evidence_span"],
    )
    frame["confidence"] = _coalesce_numeric(
        frame,
        ["analysis_confidence", "phase2_confidence", "confidence"],
    ).fillna(0)
    mask = frame["context_id"].ne("") & frame["final_intent"].ne("")
    mask &= ~frame["final_intent"].str.casefold().eq("unclear")
    if "analysis_ready" in original_columns:
        mask &= frame["analysis_ready"].map(_bool_value)
    if "evidence_supports_label" in original_columns:
        supports = frame["evidence_supports_label"].map(_clean)
        if supports.ne("").any():
            mask &= frame["evidence_supports_label"].map(_bool_value)
    if "abstain" in original_columns:
        mask &= ~frame["abstain"].map(_bool_value)
    if {"evidence_span", "evidence_span_phase2", "analysis_evidence_span"} & original_columns:
        grounded = pd.Series(
            [
                _evidence_span_grounded(span, sentence, context)
                for span, sentence, context in zip(
                    frame["evidence_span"],
                    frame["sentence_text"],
                    frame["context_window_s3"],
                    strict=True,
                )
            ],
            index=frame.index,
            dtype=bool,
        )
        mask &= grounded
    return frame.loc[mask].copy()


def build_final_release_object_edges(
    labels: pd.DataFrame,
    object_graph: pd.DataFrame,
    *,
    max_objects_per_context: int = 3,
) -> pd.DataFrame:
    """Join final labels to curated seed-registry object candidates."""
    graph = _prepare_object_graph_candidates(object_graph)
    if max_objects_per_context > 0 and not graph.empty:
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
    columns = _object_edge_columns()
    if edges.empty:
        return pd.DataFrame(columns=columns)
    edges = edges.drop_duplicates(["context_id", "object_id", "final_intent"])
    edges["edge_unit"] = "unique_context_object_intent"
    return _ensure_columns(edges, columns)[columns].sort_values(
        ["canonical_name", "context_id", "final_intent"],
    )


def enrich_labels_with_object_risk(
    labels: pd.DataFrame,
    object_graph: pd.DataFrame,
) -> pd.DataFrame:
    """Add context-level object-risk fields for reviewer QA sampling."""
    frame = labels.copy()
    graph = _prepare_object_graph_candidates(object_graph)
    risk_columns = ["object_count", "object_candidate_rank", "matched_in"]
    if graph.empty:
        frame["object_count"] = 0
        frame["object_candidate_rank"] = pd.NA
        frame["matched_in"] = ""
        return frame

    counts = graph.groupby("context_id", dropna=False).size().reset_index(name="object_count")
    best_candidates = (
        graph.sort_values(["context_id", "object_candidate_rank"])
        .groupby("context_id", dropna=False)
        .agg(
            object_candidate_rank=("object_candidate_rank", "min"),
            matched_in=("matched_in", _first_non_empty),
        )
        .reset_index()
    )
    context_risk = counts.merge(best_candidates, on="context_id", how="left")
    frame = frame.drop(columns=[column for column in risk_columns if column in frame])
    frame = frame.merge(context_risk, on="context_id", how="left")
    frame["object_count"] = pd.to_numeric(frame["object_count"], errors="coerce").fillna(0)
    frame["object_candidate_rank"] = pd.to_numeric(
        frame["object_candidate_rank"],
        errors="coerce",
    ).astype("Float64")
    frame["matched_in"] = frame["matched_in"].fillna("").map(_clean)
    return frame


def _write_final_release_figures(
    *,
    section_lift: pd.DataFrame,
    object_roles: pd.DataFrame,
    paper_evidence_use: pd.DataFrame,
    critique_matrix: pd.DataFrame,
    figures_dir: Path,
) -> dict[str, Path]:
    outputs = {
        "section_function_lift": (
            figures_dir / "f02_section_function_lift.png",
            figures_dir / "f02_section_function_lift.svg",
        ),
        "object_role_signature_map": (
            figures_dir / "f03_object_role_signature_map.png",
            figures_dir / "f03_object_role_signature_map.svg",
        ),
        "ranking_reversal": (
            figures_dir / "f04_context_volume_vs_evidence_use_reversal.png",
            figures_dir / "f04_context_volume_vs_evidence_use_reversal.svg",
        ),
        "critique_bottleneck_heatmap": (
            figures_dir / "f05_critique_bottleneck_heatmap.png",
            figures_dir / "f05_critique_bottleneck_heatmap.svg",
        ),
    }
    plot_section_function_lift_heatmap(section_lift, *outputs["section_function_lift"])
    plot_object_role_signature_map(object_roles, *outputs["object_role_signature_map"])
    plot_context_volume_vs_evidence_use_reversal(
        paper_evidence_use,
        *outputs["ranking_reversal"],
    )
    plot_critique_bottleneck_heatmap(critique_matrix, *outputs["critique_bottleneck_heatmap"])
    return {key: png for key, (png, _) in outputs.items()}


def _prepare_object_graph_candidates(object_graph: pd.DataFrame) -> pd.DataFrame:
    original_columns = set(object_graph.columns)
    graph = _ensure_columns(object_graph.copy(), _OBJECT_GRAPH_COLUMNS)
    for column in ["context_id", "object_id", "canonical_name", "object_type", "object_category"]:
        graph[column] = graph[column].map(_clean)
    graph = graph.loc[graph["context_id"].ne("") & graph["canonical_name"].ne("")].copy()
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
    graph["object_candidate_rank"] = graph.groupby("context_id", dropna=False).cumcount() + 1
    return graph[
        [
            "context_id",
            "object_id",
            "canonical_name",
            "object_type",
            "object_category",
            "object_confidence",
            "object_candidate_rank",
            "matched_in",
        ]
    ]


def _read_parquet_columns(path: str | Path, columns: list[str]) -> pd.DataFrame:
    parquet_path = Path(path)
    available = set(pq.ParquetFile(parquet_path).schema.names)
    selected = [column for column in columns if column in available]
    if not selected:
        return pd.DataFrame()
    return pd.read_parquet(parquet_path, columns=selected)


def _read_optional_parquet(path: str | Path, columns: list[str]) -> pd.DataFrame | None:
    parquet_path = Path(path)
    if not parquet_path.exists():
        return None
    return _read_parquet_columns(parquet_path, columns)


def _optional_parquet_row_count(path: str | Path) -> int | None:
    parquet_path = Path(path)
    if not parquet_path.exists():
        return None
    return int(pq.ParquetFile(parquet_path).metadata.num_rows)


def _object_edge_columns() -> list[str]:
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


def _ensure_columns(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        if column not in frame:
            frame[column] = ""
    return frame


def _coalesce_text(frame: pd.DataFrame, columns: list[str]) -> pd.Series:
    result = pd.Series("", index=frame.index, dtype=object)
    for column in columns:
        candidate = frame[column].map(_clean) if column in frame else result
        result = result.where(result.ne(""), candidate)
    return result


def _coalesce_numeric(frame: pd.DataFrame, columns: list[str]) -> pd.Series:
    result = pd.Series(pd.NA, index=frame.index, dtype="Float64")
    for column in columns:
        if column not in frame:
            continue
        candidate = pd.to_numeric(frame[column], errors="coerce").astype("Float64")
        result = result.where(result.notna(), candidate)
    return result


def _evidence_span_grounded(span: str, sentence: str, context: str) -> bool:
    evidence = _clean(span)
    return bool(evidence) and (evidence in _clean(sentence) or evidence in _clean(context))


def _matched_in_priority(value: Any) -> int:
    text = _clean(value).casefold()
    if "sentence" in text:
        return 3
    if "context_window" in text:
        return 2
    if "neighbor" in text:
        return 1
    return 0


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
    if isinstance(value, int | float):
        return value != 0
    return str(value).strip().casefold() in {"true", "1", "yes", "y", "t"}


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
        text = _clean(value)
        if text:
            return text
    return ""


def _display_path(path: str | Path) -> str:
    return Path(path).as_posix()
