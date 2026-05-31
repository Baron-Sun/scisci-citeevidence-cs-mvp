from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib
import pandas as pd
import pyarrow.parquet as pq

matplotlib.use("Agg")
from matplotlib import pyplot as plt  # noqa: E402

DEFAULT_PHASE2_ANALYSIS_REPORT = Path("reports/phase2_pilot_analysis_report.md")
DEFAULT_PHASE2_ANALYSIS_SUMMARY = Path("data/processed/phase2_pilot_analysis_summary.csv")
DEFAULT_PHASE2_CASE_STUDIES = Path("data/processed/phase2_case_studies.csv")
DEFAULT_PHASE2_CONFUSION = Path("data/processed/phase2_phase1_vs_phase2_confusion.csv")
DEFAULT_PHASE2_FIGURES_DIR = Path("figures")
DEFAULT_PHASE2_SOURCE_DATA_DIR = Path("figures/source_data")
DEFAULT_PHASE2_QUEUE_PATH = Path("data/processed/phase1_llm_queue_sample.parquet")
DEFAULT_SCISCI_FULL_REPORT = Path("reports/scisci_full_data_analysis_report.md")
DEFAULT_SCISCI_FUNNEL = Path("data/processed/scisci_evidence_funnel.csv")
DEFAULT_OBJECT_FUNCTION_MATRIX_PHASE1 = Path(
    "data/processed/object_function_matrix_full_phase1.csv"
)
DEFAULT_OBJECT_FUNCTION_MATRIX_PHASE2 = Path(
    "data/processed/object_function_matrix_phase2_batch.csv"
)
DEFAULT_PHASE1_PHASE2_CALIBRATION = Path(
    "data/processed/phase1_phase2_calibration_by_stratum.csv"
)
DEFAULT_SECTION_FUNCTION_RATES = Path("data/processed/section_function_rates.csv")
DEFAULT_CITED_PAPER_USE_SUMMARY = Path(
    "data/processed/cited_paper_evidence_use_summary.csv"
)
DEFAULT_SCISCI_CASE_STUDY_SHORTLIST = Path(
    "data/processed/scisci_case_study_shortlist.csv"
)
DEFAULT_OBJECT_GRAPH_NODES = Path("data/processed/evidence_backed_object_graph_nodes.csv")
DEFAULT_OBJECT_GRAPH_EDGES = Path("data/processed/evidence_backed_object_graph_edges.csv")
DEFAULT_EVIDENCE_CARDS = Path("data/processed/evidence_cards.csv")
DEFAULT_OBJECT_GRAPH_REPORT = Path("reports/evidence_backed_object_graph_report.md")
DEFAULT_SECTIONED_CONTEXTS_PATH = Path("data/processed/citation_contexts_sectioned.parquet")
DEFAULT_RESOLVED_CONTEXTS_PATH = Path("data/processed/citation_contexts_resolved.parquet")

CASE_STUDY_COLUMNS = [
    "context_id",
    "final_intent",
    "final_object_type",
    "final_relation_subtype",
    "method_edge_type",
    "normalized_section",
    "resolved_cited_title",
    "sentence_text",
    "context_window_s3",
    "evidence_span_phase2",
    "problem_or_motivation_quote",
    "usage_or_mechanism_quote",
    "comparison_or_tradeoff_quote",
    "phase2_confidence",
    "rationale_short",
    "report_comment",
]

INTENT_ORDER = [
    "uses",
    "compares_against",
    "extends",
    "critiques",
    "applies",
    "background",
    "unclear",
]
KNOWN_SECTIONS = {
    "abstract",
    "introduction",
    "related_work",
    "background",
    "method",
    "model",
    "experiment",
    "evaluation",
    "results",
    "discussion",
    "conclusion",
    "appendix",
    "analysis",
    "error_analysis",
}
PSEUDO_OBJECT_NODE_NAMES = {
    "unknown",
    "method",
    "model",
    "metric",
    "software_or_tool",
    "dataset_or_database",
    "benchmark_or_protocol",
    "claim_or_finding",
    "theory_or_concept",
    "task",
}


def run_phase2_pilot_analysis(
    *,
    labels_path: str | Path,
    failed_diagnostics_path: str | Path,
    failed_jsonl_path: str | Path,
    out_report_path: str | Path = DEFAULT_PHASE2_ANALYSIS_REPORT,
    out_summary_path: str | Path = DEFAULT_PHASE2_ANALYSIS_SUMMARY,
    out_case_studies_path: str | Path = DEFAULT_PHASE2_CASE_STUDIES,
    out_confusion_path: str | Path = DEFAULT_PHASE2_CONFUSION,
    figures_dir: str | Path = DEFAULT_PHASE2_FIGURES_DIR,
    source_data_dir: str | Path = DEFAULT_PHASE2_SOURCE_DATA_DIR,
    queue_path: str | Path | None = DEFAULT_PHASE2_QUEUE_PATH,
) -> dict[str, Any]:
    """Analyze the revalidated Phase-2 pilot and write report-ready outputs."""
    labels_file = Path(labels_path)
    failed_diagnostics_file = Path(failed_diagnostics_path)
    failed_jsonl_file = Path(failed_jsonl_path)
    for path in (labels_file, failed_diagnostics_file, failed_jsonl_file):
        if not path.exists():
            raise FileNotFoundError(f"Required input does not exist: {path}")

    labels = pd.read_parquet(labels_file)
    failed_diagnostics = pd.read_parquet(failed_diagnostics_file)
    failed_jsonl = _read_jsonl(failed_jsonl_file)
    queue = _read_optional_queue(queue_path)

    report_out = Path(out_report_path)
    summary_out = Path(out_summary_path)
    case_studies_out = Path(out_case_studies_path)
    confusion_out = Path(out_confusion_path)
    figures_output = Path(figures_dir)
    source_output = Path(source_data_dir)
    for path in (
        report_out,
        summary_out,
        case_studies_out,
        confusion_out,
        figures_output,
        source_output,
    ):
        if path.suffix:
            path.parent.mkdir(parents=True, exist_ok=True)
        else:
            path.mkdir(parents=True, exist_ok=True)

    metrics = build_phase2_pilot_summary_metrics(labels, failed_diagnostics, failed_jsonl)
    summary = build_phase2_pilot_summary_table(metrics)
    confusion = build_phase1_phase2_confusion(labels)
    case_studies = build_phase2_case_studies(
        labels=labels,
        failed_diagnostics=failed_diagnostics,
        queue=queue,
    )
    figure_paths = write_phase2_pilot_figures(
        labels=labels,
        figures_dir=figures_output,
        source_data_dir=source_output,
    )

    summary.to_csv(summary_out, index=False)
    confusion.to_csv(confusion_out, index=False)
    case_studies.to_csv(case_studies_out, index=False)
    report_out.write_text(
        build_phase2_pilot_analysis_report(
            labels=labels,
            failed_diagnostics=failed_diagnostics,
            metrics=metrics,
            summary_path=summary_out,
            case_studies_path=case_studies_out,
            confusion_path=confusion_out,
            figure_paths=figure_paths,
        ),
        encoding="utf-8",
    )
    return {
        **metrics,
        "summary_path": str(summary_out),
        "case_studies_path": str(case_studies_out),
        "confusion_path": str(confusion_out),
        "report_path": str(report_out),
        "figure_count": len(figure_paths),
    }


def build_phase2_pilot_summary_metrics(
    labels: pd.DataFrame,
    failed_diagnostics: pd.DataFrame,
    failed_jsonl: list[dict[str, Any]],
) -> dict[str, Any]:
    """Compute core Phase-2 pilot metrics for report and tests."""
    labels = _ensure_columns(labels.copy(), _required_label_columns())
    failed = _remaining_failed(failed_diagnostics)
    total_labels = int(len(labels))
    remaining_failed = int(len(failed_jsonl) if failed_jsonl else len(failed))
    denominator = total_labels + remaining_failed
    abstain_count = int(labels["abstain"].map(_bool_value).sum())
    evidence_non_empty = int(labels["evidence_span_phase2"].map(_clean).ne("").sum())
    evidence_grounded = int(labels.apply(_evidence_span_grounded, axis=1).sum())
    quote_rates = _quote_grounding_rates(labels)
    primary = labels["primary_candidate_intent"].map(_clean)
    final = labels["final_intent"].map(_clean)
    comparable = primary.ne("") & final.ne("")
    disagreement = int((primary.loc[comparable] != final.loc[comparable]).sum())
    comparable_count = int(comparable.sum())
    return {
        "total_phase2_labels": total_labels,
        "total_remaining_failed_rows": remaining_failed,
        "final_failure_rate": _safe_rate(remaining_failed, denominator),
        "abstain_count": abstain_count,
        "abstain_rate": _safe_rate(abstain_count, total_labels),
        "evidence_span_non_empty_count": evidence_non_empty,
        "evidence_span_non_empty_rate": _safe_rate(evidence_non_empty, total_labels),
        "evidence_span_grounded_count": evidence_grounded,
        "evidence_span_grounded_rate": _safe_rate(evidence_grounded, total_labels),
        "quote_grounding_rates": quote_rates,
        "phase1_phase2_comparable_rows": comparable_count,
        "phase1_phase2_disagreement_count": disagreement,
        "phase1_phase2_disagreement_rate": _safe_rate(disagreement, comparable_count),
        "evidence_supports_distribution": _value_counts(labels, "evidence_supports_label"),
        "confidence_distribution": _confidence_distribution(labels),
        "final_intent_distribution": _value_counts(labels, "final_intent"),
        "final_object_type_distribution": _value_counts(labels, "final_object_type"),
        "final_relation_subtype_distribution": _value_counts(
            labels,
            "final_relation_subtype",
        ),
        "method_edge_type_distribution": _value_counts(labels, "method_edge_type"),
        "stance_distribution": _value_counts(labels, "stance"),
        "failed_rows_by_failure_category": _value_counts(failed, "failed_validator_type"),
        "top_corrections": _top_corrections(labels),
        "intent_by_section": _intent_by_section(labels),
        "unknown_section_rows": _unknown_section_rows(labels),
        "intent_by_object_type": _intent_by_object_type(labels),
        "top_object_names": _top_object_names(labels),
        "named_vs_generic_metric": _named_vs_generic_metric(labels),
    }


def build_phase2_pilot_summary_table(metrics: dict[str, Any]) -> pd.DataFrame:
    """Flatten the most important metrics to a two-column CSV table."""
    rows = [
        ("total_phase2_labels", metrics["total_phase2_labels"]),
        ("total_remaining_failed_rows", metrics["total_remaining_failed_rows"]),
        ("final_failure_rate", f"{metrics['final_failure_rate']:.4f}"),
        ("abstain_count", metrics["abstain_count"]),
        ("abstain_rate", f"{metrics['abstain_rate']:.4f}"),
        ("evidence_span_non_empty_rate", f"{metrics['evidence_span_non_empty_rate']:.4f}"),
        ("evidence_span_grounded_rate", f"{metrics['evidence_span_grounded_rate']:.4f}"),
        (
            "phase1_phase2_disagreement_count",
            metrics["phase1_phase2_disagreement_count"],
        ),
        (
            "phase1_phase2_disagreement_rate",
            f"{metrics['phase1_phase2_disagreement_rate']:.4f}",
        ),
    ]
    for name, rate in metrics["quote_grounding_rates"].items():
        rows.append((f"{name}_grounded_rate", f"{rate:.4f}"))
    return pd.DataFrame(rows, columns=["metric", "value"])


def build_phase1_phase2_confusion(labels: pd.DataFrame) -> pd.DataFrame:
    """Build Phase-1 primary intent by Phase-2 final intent confusion counts."""
    frame = _ensure_columns(labels.copy(), ["primary_candidate_intent", "final_intent"])
    frame["primary_candidate_intent"] = frame["primary_candidate_intent"].map(_clean)
    frame["final_intent"] = frame["final_intent"].map(_clean)
    frame = frame.loc[
        frame["primary_candidate_intent"].ne("") & frame["final_intent"].ne("")
    ]
    if frame.empty:
        return pd.DataFrame(
            columns=["primary_candidate_intent", "final_intent", "rows", "row_rate"]
        )
    counts = (
        frame.groupby(["primary_candidate_intent", "final_intent"], dropna=False)
        .size()
        .reset_index(name="rows")
        .sort_values(
            ["primary_candidate_intent", "rows", "final_intent"],
            ascending=[True, False, True],
        )
    )
    totals = counts.groupby("primary_candidate_intent")["rows"].transform("sum")
    counts["row_rate"] = counts["rows"] / totals
    return counts


def build_phase2_case_studies(
    *,
    labels: pd.DataFrame,
    failed_diagnostics: pd.DataFrame,
    queue: pd.DataFrame | None = None,
    per_intent: int = 10,
    failure_count: int = 5,
) -> pd.DataFrame:
    """Create report-facing case study examples by intent plus remaining failures."""
    labels = _ensure_columns(labels.copy(), _required_label_columns())
    rows: list[dict[str, Any]] = []
    for intent in INTENT_ORDER:
        if intent == "unclear":
            continue
        subset = labels.loc[labels["final_intent"].map(_clean).eq(intent)].copy()
        subset = subset.sort_values(
            ["phase2_confidence", "context_id"],
            ascending=[False, True],
        )
        for row in subset.head(per_intent).to_dict(orient="records"):
            rows.append(_case_study_from_label(row, f"Representative {intent} label."))

    failed = _remaining_failed(failed_diagnostics).head(failure_count)
    queue_by_context = _queue_lookup(queue)
    for failed_row in failed.to_dict(orient="records"):
        context_id = _clean(failed_row.get("context_id"))
        queue_row = queue_by_context.get(context_id, {})
        rows.append(_case_study_from_failed(failed_row, queue_row))

    return _ensure_columns(pd.DataFrame(rows), CASE_STUDY_COLUMNS)[CASE_STUDY_COLUMNS]


def write_phase2_pilot_figures(
    *,
    labels: pd.DataFrame,
    figures_dir: Path,
    source_data_dir: Path,
) -> dict[str, str]:
    """Write matplotlib figures and per-figure source CSVs."""
    labels = _ensure_columns(labels.copy(), _required_label_columns())
    figures_dir.mkdir(parents=True, exist_ok=True)
    source_data_dir.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, str] = {}

    specs = [
        ("final_intent_distribution", _value_counts(labels, "final_intent"), "final_intent"),
        (
            "object_type_distribution",
            _value_counts(labels, "final_object_type"),
            "final_object_type",
        ),
        (
            "relation_subtype_distribution",
            _value_counts(labels, "final_relation_subtype"),
            "final_relation_subtype",
        ),
        (
            "method_edge_type_distribution",
            _value_counts(labels, "method_edge_type"),
            "method_edge_type",
        ),
    ]
    for name, data, label_column in specs:
        source = source_data_dir / f"phase2_{name}.csv"
        figure = figures_dir / f"phase2_{name}.png"
        data.to_csv(source, index=False)
        _plot_bar(data, label_column, "rows", figure, _title_from_name(name))
        outputs[name] = str(figure)

    section_data = _intent_by_section(labels)
    section_source = source_data_dir / "phase2_intent_by_section.csv"
    section_figure = figures_dir / "phase2_intent_by_section.png"
    section_data.to_csv(section_source, index=False)
    _plot_stacked_section_intents(section_data, section_figure)
    outputs["intent_by_section"] = str(section_figure)

    disagreement_data = _disagreement_source(labels)
    disagreement_source = source_data_dir / "phase2_phase1_vs_phase2_disagreement.csv"
    disagreement_figure = figures_dir / "phase2_phase1_vs_phase2_disagreement.png"
    disagreement_data.to_csv(disagreement_source, index=False)
    _plot_bar(
        disagreement_data,
        "status",
        "rows",
        disagreement_figure,
        "Phase-1 vs Phase-2 Agreement",
    )
    outputs["phase1_vs_phase2_disagreement"] = str(disagreement_figure)
    return outputs


def build_phase2_pilot_analysis_report(
    *,
    labels: pd.DataFrame,
    failed_diagnostics: pd.DataFrame,
    metrics: dict[str, Any],
    summary_path: Path,
    case_studies_path: Path,
    confusion_path: Path,
    figure_paths: dict[str, str],
) -> str:
    """Build the markdown Phase-2 pilot analysis report."""
    sections = [
        "# Phase-2 Pilot Analysis Report",
        "",
        "Phase-2 labels are model-assisted structured evidence labels, not human gold annotation. "
        "All accepted non-abstain labels must retain exact local evidence and "
        "`evidence_supports_label=true`.",
        "",
        "## Outputs",
        f"- Summary CSV: `{summary_path}`",
        f"- Case studies CSV: `{case_studies_path}`",
        f"- Phase-1 vs Phase-2 confusion CSV: `{confusion_path}`",
        f"- Figures: `{Path(next(iter(figure_paths.values()), 'figures')).parent}`",
        "",
        "## Core Counts",
        _table(build_phase2_pilot_summary_table(metrics)),
        "",
        "## Final Intent Distribution",
        _table(metrics["final_intent_distribution"]),
        "",
        "## Final Object Type Distribution",
        _table(metrics["final_object_type_distribution"]),
        "",
        "## Final Relation Subtype Distribution",
        _table(metrics["final_relation_subtype_distribution"]),
        "",
        "## Method Edge Type Distribution",
        _table(metrics["method_edge_type_distribution"]),
        "",
        "## Stance Distribution",
        _table(metrics["stance_distribution"]),
        "",
        "## Evidence Supports Label Distribution",
        _table(metrics["evidence_supports_distribution"]),
        "",
        "## Confidence Distribution",
        _table(metrics["confidence_distribution"]),
        "",
        "## Phase-1 Vs Phase-2 Confusion",
        _table(build_phase1_phase2_confusion(labels)),
        "",
        "## Most Common Phase-1 To Phase-2 Corrections",
        _table(metrics["top_corrections"]),
        "",
        "## Final Intent By Known Section",
        _table(metrics["intent_by_section"]),
        "",
        "## Unknown Section Rows",
        str(metrics["unknown_section_rows"]),
        "",
        "## Final Intent By Object Type",
        _table(metrics["intent_by_object_type"]),
        "",
        "## Top Object Names",
        _table(metrics["top_object_names"]),
        "",
        "## Named Objects Vs Generic Metrics",
        _table(metrics["named_vs_generic_metric"]),
        "",
        "## Evidence Quality",
        _table(_evidence_quality_table(metrics)),
        "",
        "## Remaining Failed Rows By Failure Category",
        _table(metrics["failed_rows_by_failure_category"]),
        "",
        "## Report-Ready Examples",
        _report_examples(labels),
        "",
        "## Figure Files",
        _table(
            pd.DataFrame(
                [{"figure": name, "path": path} for name, path in figure_paths.items()]
            )
        ),
        "",
        "## Remaining Failure Examples",
        _table(_remaining_failed(failed_diagnostics).head(10)),
        "",
    ]
    return "\n".join(sections)


def _required_label_columns() -> list[str]:
    return [
        "context_id",
        "primary_candidate_intent",
        "final_intent",
        "final_object_type",
        "final_relation_subtype",
        "method_edge_type",
        "stance",
        "normalized_section",
        "resolved_cited_title",
        "sentence_text",
        "context_window_s3",
        "evidence_span_phase2",
        "problem_or_motivation_quote",
        "usage_or_mechanism_quote",
        "comparison_or_tradeoff_quote",
        "evidence_supports_label",
        "abstain",
        "phase2_confidence",
        "rationale_short",
        "object_names",
        "generic_metric_names",
    ]


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def _read_optional_queue(path: str | Path | None) -> pd.DataFrame | None:
    if path is None:
        return None
    queue_path = Path(path)
    if not queue_path.exists():
        return None
    return pd.read_parquet(queue_path)


def _remaining_failed(failed_diagnostics: pd.DataFrame) -> pd.DataFrame:
    frame = _ensure_columns(failed_diagnostics.copy(), ["revalidated", "failed_validator_type"])
    if frame.empty:
        return frame
    if "revalidated" in frame:
        return frame.loc[~frame["revalidated"].map(_bool_value)].copy()
    return frame


def _value_counts(frame: pd.DataFrame, column: str, limit: int | None = None) -> pd.DataFrame:
    if frame.empty or column not in frame:
        return pd.DataFrame(columns=[column, "rows", "rate"])
    prepared = frame.copy()
    prepared[column] = prepared[column].map(_clean)
    prepared.loc[prepared[column].eq(""), column] = "blank"
    counts = (
        prepared[column]
        .value_counts(dropna=False)
        .rename_axis(column)
        .reset_index(name="rows")
    )
    counts["rate"] = counts["rows"] / max(int(len(prepared)), 1)
    counts = counts.sort_values(["rows", column], ascending=[False, True])
    return counts.head(limit) if limit else counts


def _confidence_distribution(labels: pd.DataFrame) -> pd.DataFrame:
    scores = pd.to_numeric(labels.get("phase2_confidence", pd.Series(dtype=float)), errors="coerce")
    scores = scores.fillna(0)
    bins = pd.cut(
        scores,
        bins=[-0.001, 0.2, 0.5, 0.7, 0.85, 1.0],
        labels=["[0,0.2]", "(0.2,0.5]", "(0.5,0.7]", "(0.7,0.85]", "(0.85,1.0]"],
    )
    return bins.value_counts(sort=False).rename_axis("confidence_bin").reset_index(name="rows")


def _top_corrections(labels: pd.DataFrame, limit: int = 15) -> pd.DataFrame:
    frame = _ensure_columns(labels.copy(), ["primary_candidate_intent", "final_intent"])
    frame["primary_candidate_intent"] = frame["primary_candidate_intent"].map(_clean)
    frame["final_intent"] = frame["final_intent"].map(_clean)
    frame = frame.loc[
        frame["primary_candidate_intent"].ne("")
        & frame["final_intent"].ne("")
        & frame["primary_candidate_intent"].ne(frame["final_intent"])
    ]
    if frame.empty:
        return pd.DataFrame(columns=["primary_candidate_intent", "final_intent", "rows"])
    return (
        frame.groupby(["primary_candidate_intent", "final_intent"], dropna=False)
        .size()
        .reset_index(name="rows")
        .sort_values(
            ["rows", "primary_candidate_intent", "final_intent"],
            ascending=[False, True, True],
        )
        .head(limit)
    )


def _intent_by_section(labels: pd.DataFrame) -> pd.DataFrame:
    frame = _ensure_columns(labels.copy(), ["normalized_section", "final_intent"])
    frame["normalized_section"] = frame["normalized_section"].map(_clean).str.lower()
    frame.loc[frame["normalized_section"].eq(""), "normalized_section"] = "unknown"
    frame = frame.loc[frame["normalized_section"].isin(KNOWN_SECTIONS)].copy()
    if frame.empty:
        return pd.DataFrame(columns=["normalized_section", "final_intent", "rows"])
    return (
        frame.groupby(["normalized_section", "final_intent"], dropna=False)
        .size()
        .reset_index(name="rows")
        .sort_values(["normalized_section", "rows"], ascending=[True, False])
    )


def _unknown_section_rows(labels: pd.DataFrame) -> int:
    sections = labels.get("normalized_section", pd.Series(dtype=str)).map(_clean).str.lower()
    return int((sections.eq("") | sections.eq("unknown") | ~sections.isin(KNOWN_SECTIONS)).sum())


def _intent_by_object_type(labels: pd.DataFrame) -> pd.DataFrame:
    frame = _ensure_columns(labels.copy(), ["final_intent", "final_object_type"])
    if frame.empty:
        return pd.DataFrame(columns=["final_intent", "final_object_type", "rows"])
    return (
        frame.groupby(["final_intent", "final_object_type"], dropna=False)
        .size()
        .reset_index(name="rows")
        .sort_values(["final_intent", "rows"], ascending=[True, False])
    )


def _top_object_names(labels: pd.DataFrame, limit: int = 25) -> pd.DataFrame:
    if "object_names" not in labels:
        return pd.DataFrame(columns=["object_name", "rows"])
    names: list[str] = []
    for value in labels["object_names"]:
        names.extend([part.strip() for part in _clean(value).split(";") if part.strip()])
    if not names:
        return pd.DataFrame(columns=["object_name", "rows"])
    frame = pd.DataFrame({"object_name": names})
    return frame.value_counts("object_name").reset_index(name="rows").head(limit)


def _named_vs_generic_metric(labels: pd.DataFrame) -> pd.DataFrame:
    frame = _ensure_columns(labels.copy(), ["object_names", "generic_metric_names"])
    named = frame["object_names"].map(_clean).ne("")
    generic_metric = frame["generic_metric_names"].map(_clean).ne("")
    categories = pd.Series("neither", index=frame.index)
    categories.loc[named & ~generic_metric] = "named_object_only"
    categories.loc[~named & generic_metric] = "generic_metric_only"
    categories.loc[named & generic_metric] = "named_object_and_generic_metric"
    return (
        categories.value_counts()
        .rename_axis("object_signal")
        .reset_index(name="rows")
        .sort_values("rows", ascending=False)
    )


def _quote_grounding_rates(labels: pd.DataFrame) -> dict[str, float]:
    rates: dict[str, float] = {}
    for column in (
        "problem_or_motivation_quote",
        "usage_or_mechanism_quote",
        "comparison_or_tradeoff_quote",
    ):
        if column not in labels:
            rates[column] = 1.0
            continue
        non_empty = labels[column].map(_clean).ne("")
        if not bool(non_empty.any()):
            rates[column] = 1.0
            continue
        grounded = labels.loc[non_empty].apply(
            lambda row, quote_column=column: _quote_grounded(row, quote_column),
            axis=1,
        )
        rates[column] = _safe_rate(int(grounded.sum()), int(non_empty.sum()))
    return rates


def _evidence_span_grounded(row: pd.Series) -> bool:
    evidence = _clean(row.get("evidence_span_phase2"))
    if not evidence:
        return False
    return evidence in _clean(row.get("sentence_text")) or evidence in _clean(
        row.get("context_window_s3")
    )


def _quote_grounded(row: pd.Series, column: str) -> bool:
    quote = _clean(row.get(column))
    if not quote:
        return True
    return quote in _clean(row.get("sentence_text")) or quote in _clean(
        row.get("context_window_s3")
    )


def _disagreement_source(labels: pd.DataFrame) -> pd.DataFrame:
    frame = _ensure_columns(labels.copy(), ["primary_candidate_intent", "final_intent"])
    primary = frame["primary_candidate_intent"].map(_clean)
    final = frame["final_intent"].map(_clean)
    comparable = primary.ne("") & final.ne("")
    disagreement = int((primary.loc[comparable] != final.loc[comparable]).sum())
    agreement = int(comparable.sum()) - disagreement
    return pd.DataFrame(
        [
            {"status": "agreement", "rows": agreement},
            {"status": "disagreement", "rows": disagreement},
        ]
    )


def _case_study_from_label(row: dict[str, Any], comment: str) -> dict[str, Any]:
    return {
        "context_id": _clean(row.get("context_id")),
        "final_intent": _clean(row.get("final_intent")),
        "final_object_type": _clean(row.get("final_object_type")),
        "final_relation_subtype": _clean(row.get("final_relation_subtype")),
        "method_edge_type": _clean(row.get("method_edge_type")),
        "normalized_section": _clean(row.get("normalized_section")),
        "resolved_cited_title": _clean(row.get("resolved_cited_title")),
        "sentence_text": _clean(row.get("sentence_text")),
        "context_window_s3": _clean(row.get("context_window_s3")),
        "evidence_span_phase2": _clean(row.get("evidence_span_phase2")),
        "problem_or_motivation_quote": _clean(row.get("problem_or_motivation_quote")),
        "usage_or_mechanism_quote": _clean(row.get("usage_or_mechanism_quote")),
        "comparison_or_tradeoff_quote": _clean(row.get("comparison_or_tradeoff_quote")),
        "phase2_confidence": _clean(row.get("phase2_confidence")),
        "rationale_short": _clean(row.get("rationale_short")),
        "report_comment": comment,
    }


def _case_study_from_failed(
    failed_row: dict[str, Any],
    queue_row: dict[str, Any],
) -> dict[str, Any]:
    raw = _parse_raw_response(_clean(failed_row.get("raw_response")))
    failure_detail = _clean(failed_row.get("revalidation_error")) or _clean(
        failed_row.get("validation_error")
    )
    return {
        "context_id": _clean(failed_row.get("context_id")),
        "final_intent": _clean(failed_row.get("final_intent")) or _clean(raw.get("final_intent")),
        "final_object_type": _clean(failed_row.get("final_object_type"))
        or _clean(raw.get("final_object_type")),
        "final_relation_subtype": _clean(raw.get("final_relation_subtype")),
        "method_edge_type": _clean(raw.get("method_edge_type")),
        "normalized_section": _clean(queue_row.get("normalized_section")),
        "resolved_cited_title": _clean(queue_row.get("resolved_cited_title")),
        "sentence_text": _clean(queue_row.get("sentence_text")),
        "context_window_s3": _clean(queue_row.get("context_window_s3")),
        "evidence_span_phase2": _clean(failed_row.get("evidence_span"))
        or _clean(raw.get("evidence_span")),
        "problem_or_motivation_quote": _clean(raw.get("problem_or_motivation_quote")),
        "usage_or_mechanism_quote": _clean(raw.get("usage_or_mechanism_quote")),
        "comparison_or_tradeoff_quote": _clean(raw.get("comparison_or_tradeoff_quote")),
        "phase2_confidence": _clean(raw.get("confidence")),
        "rationale_short": _clean(raw.get("rationale_short")),
        "report_comment": (
            "Remaining failed row: "
            f"{_clean(failed_row.get('failed_validator_type'))}; "
            f"{failure_detail}"
        ),
    }


def _queue_lookup(queue: pd.DataFrame | None) -> dict[str, dict[str, Any]]:
    if queue is None or queue.empty or "context_id" not in queue:
        return {}
    return {str(row["context_id"]): row.to_dict() for _, row in queue.iterrows()}


def _parse_raw_response(raw_response: str) -> dict[str, Any]:
    if not raw_response:
        return {}
    try:
        parsed = json.loads(raw_response)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _evidence_quality_table(metrics: dict[str, Any]) -> pd.DataFrame:
    rows = [
        {
            "metric": "evidence_span_non_empty_rate",
            "value": f"{metrics['evidence_span_non_empty_rate']:.3f}",
        },
        {
            "metric": "evidence_span_grounded_rate",
            "value": f"{metrics['evidence_span_grounded_rate']:.3f}",
        },
    ]
    for column, rate in metrics["quote_grounding_rates"].items():
        rows.append({"metric": f"{column}_grounded_rate", "value": f"{rate:.3f}"})
    return pd.DataFrame(rows)


def _report_examples(labels: pd.DataFrame) -> str:
    chunks: list[str] = []
    for intent in INTENT_ORDER:
        if intent == "unclear":
            continue
        subset = labels.loc[labels["final_intent"].map(_clean).eq(intent)].head(3)
        if subset.empty:
            continue
        rows = []
        for row in subset.to_dict(orient="records"):
            rows.append(
                {
                    "intent": intent,
                    "cited_paper_title": _truncate(_clean(row.get("resolved_cited_title")), 90),
                    "citation_sentence": _truncate(_clean(row.get("sentence_text")), 160),
                    "evidence_span": _truncate(_clean(row.get("evidence_span_phase2")), 120),
                    "why_label_is_correct": _truncate(_clean(row.get("rationale_short")), 150),
                }
            )
        chunks.extend([f"### {intent}", "", _table(pd.DataFrame(rows)), ""])
    return "\n".join(chunks)


def _plot_bar(
    data: pd.DataFrame,
    label_column: str,
    value_column: str,
    output: Path,
    title: str,
) -> None:
    fig_width = max(7.0, min(12.0, len(data) * 0.75))
    fig, ax = plt.subplots(figsize=(fig_width, 4.8))
    if data.empty:
        ax.text(0.5, 0.5, "No data", ha="center", va="center")
        ax.set_axis_off()
    else:
        labels = data[label_column].astype(str).tolist()
        values = pd.to_numeric(data[value_column], errors="coerce").fillna(0).tolist()
        ax.bar(labels, values, color="#4B7F9F")
        ax.set_ylabel("Rows")
        ax.set_title(title)
        ax.tick_params(axis="x", rotation=35)
        for tick in ax.get_xticklabels():
            tick.set_ha("right")
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)


def _plot_stacked_section_intents(data: pd.DataFrame, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(11, 5.5))
    if data.empty:
        ax.text(0.5, 0.5, "No known section data", ha="center", va="center")
        ax.set_axis_off()
    else:
        pivot = data.pivot_table(
            index="normalized_section",
            columns="final_intent",
            values="rows",
            aggfunc="sum",
            fill_value=0,
        )
        pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=False).index]
        pivot = pivot[[column for column in INTENT_ORDER if column in pivot.columns]]
        bottom = pd.Series(0, index=pivot.index)
        colors = [
            "#4B7F9F",
            "#D17A22",
            "#6A994E",
            "#B56576",
            "#7A6F9B",
            "#5D737E",
            "#999999",
        ]
        for index, column in enumerate(pivot.columns):
            values = pivot[column]
            ax.bar(
                pivot.index,
                values,
                bottom=bottom,
                label=column,
                color=colors[index % len(colors)],
            )
            bottom = bottom + values
        ax.set_ylabel("Rows")
        ax.set_title("Phase-2 Final Intent By Known Section")
        ax.tick_params(axis="x", rotation=35)
        for tick in ax.get_xticklabels():
            tick.set_ha("right")
        ax.legend(loc="upper right", fontsize="small")
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)


def run_scisci_full_analysis(
    *,
    contexts_path: str | Path,
    object_mentions_path: str | Path,
    object_graph_candidates_path: str | Path,
    phase1_path: str | Path,
    phase2_path: str | Path,
    out_report_path: str | Path = DEFAULT_SCISCI_FULL_REPORT,
    figures_dir: str | Path = DEFAULT_PHASE2_FIGURES_DIR,
    source_data_dir: str | Path = DEFAULT_PHASE2_SOURCE_DATA_DIR,
    strict_object_graph_candidates_path: str | Path | None = None,
    broad_object_graph_candidates_path: str | Path | None = None,
    cited_title_profiles_path: str | Path | None = None,
    phase1_features_path: str | Path | None = None,
    failed_diagnostics_path: str | Path | None = None,
) -> dict[str, Any]:
    """Run deterministic SciSci-style full-data analysis outputs."""
    required = [
        Path(contexts_path),
        Path(object_mentions_path),
        Path(object_graph_candidates_path),
        Path(phase1_path),
        Path(phase2_path),
    ]
    for path in required:
        if not path.exists():
            raise FileNotFoundError(f"Required input does not exist: {path}")

    contexts = pd.read_parquet(contexts_path)
    object_mentions = pd.read_parquet(object_mentions_path)
    object_graph = pd.read_parquet(object_graph_candidates_path)
    phase1 = pd.read_parquet(phase1_path)
    phase2 = pd.read_parquet(phase2_path)
    strict_graph = _optional_parquet(strict_object_graph_candidates_path)
    broad_graph = _optional_parquet(broad_object_graph_candidates_path)
    cited_profiles = _optional_parquet(cited_title_profiles_path)
    phase1_features = _optional_parquet(phase1_features_path)
    failed_diagnostics = _optional_parquet(failed_diagnostics_path)

    report_out = Path(out_report_path)
    figures_output = Path(figures_dir)
    source_output = Path(source_data_dir)
    for path in (report_out, figures_output, source_output):
        if path.suffix:
            path.parent.mkdir(parents=True, exist_ok=True)
        else:
            path.mkdir(parents=True, exist_ok=True)

    funnel = build_evidence_funnel(
        contexts=contexts,
        object_mentions=object_mentions,
        object_graph=object_graph,
        phase1=phase1,
        phase2=phase2,
    )
    object_matrix_phase1 = build_object_function_matrix_phase1(phase1, object_graph)
    object_matrix_phase2 = build_object_function_matrix_phase2(phase2)
    calibration = build_phase1_phase2_calibration(phase2)
    section_rates = build_section_function_rates(phase1)
    infrastructure = build_object_infrastructure_ranking(phase1, object_graph)
    cited_summary = build_cited_paper_evidence_use_summary(phase1)
    shortlist = build_scisci_case_study_shortlist(cited_summary, infrastructure)

    outputs = {
        "funnel": DEFAULT_SCISCI_FUNNEL,
        "object_matrix_phase1": DEFAULT_OBJECT_FUNCTION_MATRIX_PHASE1,
        "object_matrix_phase2": DEFAULT_OBJECT_FUNCTION_MATRIX_PHASE2,
        "calibration": DEFAULT_PHASE1_PHASE2_CALIBRATION,
        "section_rates": DEFAULT_SECTION_FUNCTION_RATES,
        "cited_summary": DEFAULT_CITED_PAPER_USE_SUMMARY,
        "shortlist": DEFAULT_SCISCI_CASE_STUDY_SHORTLIST,
    }
    for output in outputs.values():
        output.parent.mkdir(parents=True, exist_ok=True)

    funnel.to_csv(outputs["funnel"], index=False)
    object_matrix_phase1.to_csv(outputs["object_matrix_phase1"], index=False)
    object_matrix_phase2.to_csv(outputs["object_matrix_phase2"], index=False)
    calibration.to_csv(outputs["calibration"], index=False)
    section_rates.to_csv(outputs["section_rates"], index=False)
    cited_summary.to_csv(outputs["cited_summary"], index=False)
    shortlist.to_csv(outputs["shortlist"], index=False)

    figure_paths = write_scisci_full_figures(
        funnel=funnel,
        object_matrix_phase1=object_matrix_phase1,
        object_matrix_phase2=object_matrix_phase2,
        section_rates=section_rates,
        calibration=calibration,
        infrastructure=infrastructure,
        figures_dir=figures_output,
        source_data_dir=source_output,
    )

    report_out.write_text(
        build_scisci_full_report(
            funnel=funnel,
            object_matrix_phase1=object_matrix_phase1,
            object_matrix_phase2=object_matrix_phase2,
            calibration=calibration,
            section_rates=section_rates,
            infrastructure=infrastructure,
            cited_summary=cited_summary,
            shortlist=shortlist,
            figure_paths=figure_paths,
            strict_graph=strict_graph,
            broad_graph=broad_graph,
            cited_profiles=cited_profiles,
            phase1_features=phase1_features,
            failed_diagnostics=failed_diagnostics,
        ),
        encoding="utf-8",
    )
    return {
        "analysis_ready_strong_contexts": int(len(contexts)),
        "object_mentions": int(len(object_mentions)),
        "object_graph_candidates": int(len(object_graph)),
        "phase1_rows": int(len(phase1)),
        "phase2_rows": int(len(phase2)),
        "figure_count": len(figure_paths),
        "report_path": str(report_out),
    }


def build_evidence_funnel(
    *,
    contexts: pd.DataFrame,
    object_mentions: pd.DataFrame,
    object_graph: pd.DataFrame,
    phase1: pd.DataFrame,
    phase2: pd.DataFrame,
    sectioned_context_count: int | None = None,
    resolved_component_count: int | None = None,
) -> pd.DataFrame:
    """Build the evidence funnel table used as a core SciSci-style result."""
    sectioned_count = (
        sectioned_context_count
        if sectioned_context_count is not None
        else _optional_parquet_row_count(DEFAULT_SECTIONED_CONTEXTS_PATH)
    )
    resolved_count = (
        resolved_component_count
        if resolved_component_count is not None
        else _optional_parquet_row_count(DEFAULT_RESOLVED_CONTEXTS_PATH)
    )
    steps = [
        ("section_aware_citation_contexts", sectioned_count),
        ("resolved_citation_marker_components", resolved_count),
        ("analysis_ready_strong_contexts", len(contexts)),
        ("object_mentions", len(object_mentions)),
        ("object_graph_candidate_mentions", len(object_graph)),
        ("phase1_llm_candidate_contexts", int(_bool_series(phase1, "should_send_to_llm").sum())),
        ("phase2_valid_structured_labels", len(phase2)),
    ]
    rows = []
    previous: int | None = None
    for step, count in steps:
        count_int = int(count) if count is not None else 0
        rows.append(
            {
                "step": step,
                "count": count_int,
                "retention_from_previous": _safe_rate(count_int, previous or 0)
                if previous
                else 1.0,
                "retention_from_first": _safe_rate(count_int, int(steps[0][1] or count_int)),
            }
        )
        if count is not None and count_int > 0:
            previous = count_int
    return pd.DataFrame(rows)


def build_object_function_matrix_phase1(
    phase1: pd.DataFrame,
    object_graph: pd.DataFrame,
    *,
    top_n: int = 30,
) -> pd.DataFrame:
    """Compute top object by Phase-1 candidate intent matrix."""
    phase1_small = _ensure_columns(
        phase1[["context_id", "primary_candidate_intent"]].copy(),
        ["context_id", "primary_candidate_intent"],
    )
    graph = _ensure_columns(
        object_graph[["context_id", "canonical_name", "object_type"]].copy(),
        ["context_id", "canonical_name", "object_type"],
    )
    graph["canonical_name"] = graph["canonical_name"].map(_clean)
    graph = graph.loc[graph["canonical_name"].ne("")]
    joined = graph.merge(phase1_small, on="context_id", how="inner")
    joined["primary_candidate_intent"] = joined["primary_candidate_intent"].map(_clean)
    top_objects = joined["canonical_name"].value_counts().head(top_n).index
    joined = joined.loc[joined["canonical_name"].isin(top_objects)]
    return _object_intent_matrix(
        joined,
        object_column="canonical_name",
        type_column="object_type",
        intent_column="primary_candidate_intent",
    )


def build_object_function_matrix_phase2(
    phase2: pd.DataFrame,
    *,
    top_n: int = 30,
) -> pd.DataFrame:
    """Compute top object by Phase-2 final intent matrix from pilot labels."""
    rows = []
    for row in phase2.to_dict(orient="records"):
        names = _split_semicolon(
            _clean(row.get("graph_candidate_object_names"))
        ) or _split_semicolon(
            _clean(row.get("object_names"))
        )
        if not names:
            names = [_clean(row.get("final_object_type")) or "unknown_object"]
        object_types = _split_semicolon(_clean(row.get("object_types")))
        for index, name in enumerate(names):
            rows.append(
                {
                    "canonical_name": name,
                    "object_type": object_types[index]
                    if index < len(object_types)
                    else _clean(row.get("final_object_type")),
                    "final_intent": _clean(row.get("final_intent")),
                }
            )
    frame = pd.DataFrame(rows)
    if frame.empty:
        return pd.DataFrame(columns=["canonical_name", "object_type", "total"])
    top_objects = frame["canonical_name"].value_counts().head(top_n).index
    frame = frame.loc[frame["canonical_name"].isin(top_objects)]
    return _object_intent_matrix(
        frame,
        object_column="canonical_name",
        type_column="object_type",
        intent_column="final_intent",
    )


def build_phase1_phase2_calibration(phase2: pd.DataFrame) -> pd.DataFrame:
    """Build source-target flow table for Phase-1 primary intent to Phase-2 final intent."""
    confusion = build_phase1_phase2_confusion(phase2)
    if confusion.empty:
        return pd.DataFrame(columns=["source", "target", "rows", "rate_within_source"])
    return confusion.rename(
        columns={
            "primary_candidate_intent": "source",
            "final_intent": "target",
            "row_rate": "rate_within_source",
        }
    )[["source", "target", "rows", "rate_within_source"]]


def build_section_function_rates(phase1: pd.DataFrame) -> pd.DataFrame:
    """Compute P(primary_candidate_intent | normalized_section) from full Phase-1 data."""
    frame = _ensure_columns(
        phase1[["normalized_section", "primary_candidate_intent"]].copy(),
        ["normalized_section", "primary_candidate_intent"],
    )
    frame["normalized_section"] = frame["normalized_section"].map(_clean).str.lower()
    frame.loc[frame["normalized_section"].eq(""), "normalized_section"] = "unknown"
    frame["primary_candidate_intent"] = frame["primary_candidate_intent"].map(_clean)
    counts = (
        frame.groupby(["normalized_section", "primary_candidate_intent"], dropna=False)
        .size()
        .reset_index(name="rows")
    )
    totals = counts.groupby("normalized_section")["rows"].transform("sum")
    counts["section_total"] = totals
    counts["rate_within_section"] = counts["rows"] / totals
    counts["is_known_section"] = counts["normalized_section"].isin(KNOWN_SECTIONS)
    return counts.sort_values(
        ["is_known_section", "normalized_section", "rows"],
        ascending=[False, True, False],
    )


def build_object_infrastructure_ranking(
    phase1: pd.DataFrame,
    object_graph: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate object-level candidate function counts and shares."""
    phase1_small = _ensure_columns(
        phase1[["context_id", "primary_candidate_intent", "normalized_section"]].copy(),
        ["context_id", "primary_candidate_intent", "normalized_section"],
    )
    graph = _ensure_columns(
        object_graph[["context_id", "canonical_name", "object_type", "object_category"]].copy(),
        ["context_id", "canonical_name", "object_type", "object_category"],
    )
    graph["canonical_name"] = graph["canonical_name"].map(_clean)
    graph = graph.loc[graph["canonical_name"].ne("")]
    joined = graph.merge(phase1_small, on="context_id", how="inner")
    if joined.empty:
        return pd.DataFrame()
    joined["primary_candidate_intent"] = joined["primary_candidate_intent"].map(_clean)
    joined["normalized_section"] = joined["normalized_section"].map(_clean).str.lower()
    joined["known_section"] = joined["normalized_section"].isin(KNOWN_SECTIONS)
    base = (
        joined.groupby(["canonical_name", "object_type", "object_category"], dropna=False)
        .agg(
            total_graph_candidate_mentions=("context_id", "size"),
            known_section_count=("known_section", "sum"),
        )
        .reset_index()
    )
    counts = (
        joined.groupby(
            ["canonical_name", "object_type", "object_category", "primary_candidate_intent"],
            dropna=False,
        )
        .size()
        .reset_index(name="rows")
        .pivot_table(
            index=["canonical_name", "object_type", "object_category"],
            columns="primary_candidate_intent",
            values="rows",
            fill_value=0,
            aggfunc="sum",
        )
        .reset_index()
    )
    output = base.merge(counts, on=["canonical_name", "object_type", "object_category"], how="left")
    for intent in INTENT_ORDER:
        if intent not in output:
            output[intent] = 0
    output["unknown_section_count"] = (
        output["total_graph_candidate_mentions"] - output["known_section_count"]
    )
    output["phase1_uses_count"] = output["uses"]
    output["phase1_compares_count"] = output["compares_against"]
    output["phase1_extends_count"] = output["extends"]
    output["phase1_critiques_count"] = output["critiques"]
    output["phase1_applies_count"] = output["applies"]
    output["background_count"] = output["background"]
    denom = output["total_graph_candidate_mentions"].replace(0, pd.NA)
    output["use_share"] = output["phase1_uses_count"] / denom
    output["compare_share"] = output["phase1_compares_count"] / denom
    output["critique_share"] = output["phase1_critiques_count"] / denom
    output["extension_share"] = output["phase1_extends_count"] / denom
    return output.sort_values("total_graph_candidate_mentions", ascending=False)


def build_cited_paper_evidence_use_summary(phase1: pd.DataFrame) -> pd.DataFrame:
    """Group cited papers by candidate evidence-use functions and ranking reversals."""
    columns = [
        "resolved_cited_acl_id",
        "resolved_cited_title",
        "primary_candidate_intent",
        "context_id",
    ]
    frame = _ensure_columns(phase1[columns].copy(), columns)
    frame["resolved_cited_acl_id"] = frame["resolved_cited_acl_id"].map(_clean)
    frame["resolved_cited_title"] = frame["resolved_cited_title"].map(_clean)
    frame["primary_candidate_intent"] = frame["primary_candidate_intent"].map(_clean)
    grouped = (
        frame.groupby(
            ["resolved_cited_acl_id", "resolved_cited_title", "primary_candidate_intent"],
            dropna=False,
        )
        .size()
        .reset_index(name="rows")
    )
    pivot = grouped.pivot_table(
        index=["resolved_cited_acl_id", "resolved_cited_title"],
        columns="primary_candidate_intent",
        values="rows",
        fill_value=0,
        aggfunc="sum",
    ).reset_index()
    for intent in INTENT_ORDER:
        if intent not in pivot:
            pivot[intent] = 0
    pivot["total_strong_contexts"] = pivot[INTENT_ORDER].sum(axis=1)
    evidence_intents = ["uses", "compares_against", "extends", "critiques", "applies"]
    pivot["evidence_use_count"] = pivot[evidence_intents].sum(axis=1)
    denom = pivot["total_strong_contexts"].replace(0, pd.NA)
    pivot["background_share"] = pivot["background"] / denom
    pivot["use_share"] = pivot["evidence_use_count"] / denom
    pivot["compare_share"] = pivot["compares_against"] / denom
    pivot["critique_share"] = pivot["critiques"] / denom
    pivot["ranking_by_total_contexts"] = pivot["total_strong_contexts"].rank(
        method="min",
        ascending=False,
    )
    pivot["ranking_by_evidence_use_count"] = pivot["evidence_use_count"].rank(
        method="min",
        ascending=False,
    )
    pivot["rank_difference"] = (
        pivot["ranking_by_total_contexts"] - pivot["ranking_by_evidence_use_count"]
    )
    return pivot.sort_values("total_strong_contexts", ascending=False)


def build_scisci_case_study_shortlist(
    cited_summary: pd.DataFrame,
    infrastructure: pd.DataFrame,
    *,
    per_group: int = 15,
) -> pd.DataFrame:
    """Create shortlist tables for ranking reversals and object infrastructure stories."""
    rows: list[dict[str, Any]] = []
    rows.extend(
        _shortlist_rows(
            cited_summary.sort_values("evidence_use_count", ascending=False).head(per_group),
            "top_evidence_use_cited_paper",
        )
    )
    rows.extend(
        _shortlist_rows(
            cited_summary.loc[cited_summary["total_strong_contexts"].ge(20)]
            .sort_values(["background_share", "total_strong_contexts"], ascending=[False, False])
            .head(per_group),
            "high_citation_low_evidence_use_share",
        )
    )
    rows.extend(
        _shortlist_rows(
            cited_summary.loc[cited_summary["total_strong_contexts"].ge(10)]
            .sort_values(["compare_share", "total_strong_contexts"], ascending=[False, False])
            .head(per_group),
            "benchmark_comparison_cited_paper",
        )
    )
    rows.extend(
        _shortlist_rows(
            cited_summary.loc[cited_summary["total_strong_contexts"].ge(10)]
            .sort_values(["critique_share", "total_strong_contexts"], ascending=[False, False])
            .head(per_group),
            "critique_bottleneck_cited_paper",
        )
    )
    if not infrastructure.empty:
        for group, frame in (
            (
                "dataset_tool_model_infrastructure_object",
                infrastructure.sort_values("total_graph_candidate_mentions", ascending=False),
            ),
            (
                "high_use_share_object",
                infrastructure.loc[infrastructure["total_graph_candidate_mentions"].ge(10)]
                .sort_values(
                    ["use_share", "total_graph_candidate_mentions"],
                    ascending=[False, False],
                ),
            ),
        ):
            for row in frame.head(per_group).to_dict(orient="records"):
                rows.append(
                    {
                        "case_type": group,
                        "entity_id": _clean(row.get("canonical_name")),
                        "entity_title_or_name": _clean(row.get("canonical_name")),
                        "object_type": _clean(row.get("object_type")),
                        "total_count": int(row.get("total_graph_candidate_mentions", 0)),
                        "evidence_use_count": int(row.get("phase1_uses_count", 0))
                        + int(row.get("phase1_compares_count", 0))
                        + int(row.get("phase1_extends_count", 0))
                        + int(row.get("phase1_critiques_count", 0))
                        + int(row.get("phase1_applies_count", 0)),
                        "share": _float_value(row.get("use_share")),
                    }
                )
    return pd.DataFrame(rows)


def write_scisci_full_figures(
    *,
    funnel: pd.DataFrame,
    object_matrix_phase1: pd.DataFrame,
    object_matrix_phase2: pd.DataFrame,
    section_rates: pd.DataFrame,
    calibration: pd.DataFrame,
    infrastructure: pd.DataFrame,
    figures_dir: Path,
    source_data_dir: Path,
) -> dict[str, str]:
    """Write SciSci full-analysis figures and source CSVs."""
    figures_dir.mkdir(parents=True, exist_ok=True)
    source_data_dir.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, str] = {}
    source_map = {
        "scisci_evidence_funnel": funnel,
        "object_function_heatmap_phase1": object_matrix_phase1,
        "object_function_heatmap_phase2": object_matrix_phase2,
        "section_function_rate_heatmap": section_rates,
        "phase1_phase2_sankey_like_flow": calibration,
        "top_objects_by_function": infrastructure.head(40),
        "infrastructure_quadrant": infrastructure.head(80),
    }
    for name, data in source_map.items():
        data.to_csv(source_data_dir / f"{name}.csv", index=False)

    _plot_horizontal_bar(
        funnel.sort_values("count"),
        "step",
        "count",
        figures_dir / "scisci_evidence_funnel.png",
        "Evidence Funnel",
    )
    outputs["scisci_evidence_funnel"] = str(figures_dir / "scisci_evidence_funnel.png")

    _plot_matrix_heatmap(
        object_matrix_phase1.head(20),
        figures_dir / "object_function_heatmap_phase1.png",
        "Full Phase-1 Object-Function Matrix",
    )
    outputs["object_function_heatmap_phase1"] = str(
        figures_dir / "object_function_heatmap_phase1.png"
    )
    _plot_matrix_heatmap(
        object_matrix_phase2.head(20),
        figures_dir / "object_function_heatmap_phase2.png",
        "Phase-2 Pilot Object-Function Matrix",
    )
    outputs["object_function_heatmap_phase2"] = str(
        figures_dir / "object_function_heatmap_phase2.png"
    )
    _plot_section_rate_heatmap(
        section_rates.loc[section_rates["is_known_section"].map(_bool_value)],
        figures_dir / "section_function_rate_heatmap.png",
    )
    outputs["section_function_rate_heatmap"] = str(
        figures_dir / "section_function_rate_heatmap.png"
    )
    _plot_flow_stacked_bar(
        calibration,
        figures_dir / "phase1_phase2_sankey_like_flow.png",
    )
    outputs["phase1_phase2_sankey_like_flow"] = str(
        figures_dir / "phase1_phase2_sankey_like_flow.png"
    )
    _plot_top_objects_by_function(
        infrastructure.head(25),
        figures_dir / "top_objects_by_function.png",
    )
    outputs["top_objects_by_function"] = str(figures_dir / "top_objects_by_function.png")
    _plot_infrastructure_quadrant(
        infrastructure.head(80),
        figures_dir / "infrastructure_quadrant.png",
    )
    outputs["infrastructure_quadrant"] = str(figures_dir / "infrastructure_quadrant.png")
    return outputs


def build_scisci_full_report(
    *,
    funnel: pd.DataFrame,
    object_matrix_phase1: pd.DataFrame,
    object_matrix_phase2: pd.DataFrame,
    calibration: pd.DataFrame,
    section_rates: pd.DataFrame,
    infrastructure: pd.DataFrame,
    cited_summary: pd.DataFrame,
    shortlist: pd.DataFrame,
    figure_paths: dict[str, str],
    strict_graph: pd.DataFrame | None,
    broad_graph: pd.DataFrame | None,
    cited_profiles: pd.DataFrame | None,
    phase1_features: pd.DataFrame | None,
    failed_diagnostics: pd.DataFrame | None,
) -> str:
    """Build the full deterministic SciSci-style analysis report."""
    optional_counts = pd.DataFrame(
        [
            {"input": "strict_object_graph_candidates", "rows": _optional_len(strict_graph)},
            {"input": "broad_object_graph_candidates", "rows": _optional_len(broad_graph)},
            {"input": "cited_title_object_profiles", "rows": _optional_len(cited_profiles)},
            {"input": "phase1_context_features", "rows": _optional_len(phase1_features)},
            {"input": "phase2_failed_diagnostics", "rows": _optional_len(failed_diagnostics)},
        ]
    )
    return "\n".join(
        [
            "# SciSci Full-Data Analysis Report",
            "",
            "This report uses deterministic full-data Phase-1 candidates and object matches. "
            "These full-data counts are candidate-level signals, not human gold labels. "
            "The Phase-2 Batch analysis-ready table is the final evidence-backed sample.",
            "",
            "## Evidence Funnel",
            _table(funnel),
            "",
            "## Optional Input Coverage",
            _table(optional_counts),
            "",
            "## Top Full Phase-1 Object-Function Matrix",
            _table(object_matrix_phase1.head(30)),
            "",
            "## Top Phase-2 Batch Analysis-Ready Object-Function Matrix",
            _table(object_matrix_phase2.head(30)),
            "",
            "## Phase-1 To Phase-2 Correction Flow",
            _table(calibration),
            "",
            "## Section Function Rates",
            _table(section_rates.head(80)),
            "",
            "## Object Infrastructure Ranking",
            _table(infrastructure.head(40)),
            "",
            "## Cited Paper Evidence-Use Summary",
            _table(cited_summary.head(40)),
            "",
            "## Ranking Reversal And Case-Study Shortlist",
            _table(shortlist.head(80)),
            "",
            "## Figure Files",
            _table(pd.DataFrame([{"figure": k, "path": v} for k, v in figure_paths.items()])),
            "",
        ]
    )


def run_object_graph_analysis(
    *,
    phase2_path: str | Path,
    object_graph_candidates_path: str | Path,
    object_mentions_path: str | Path,
    phase1_path: str | Path,
    out_nodes_path: str | Path = DEFAULT_OBJECT_GRAPH_NODES,
    out_edges_path: str | Path = DEFAULT_OBJECT_GRAPH_EDGES,
    out_cards_path: str | Path = DEFAULT_EVIDENCE_CARDS,
    out_report_path: str | Path = DEFAULT_OBJECT_GRAPH_REPORT,
    figures_dir: str | Path = DEFAULT_PHASE2_FIGURES_DIR,
    source_data_dir: str | Path = DEFAULT_PHASE2_SOURCE_DATA_DIR,
) -> dict[str, Any]:
    """Build evidence-backed object-use graph outputs from Phase-2 and Phase-1 data."""
    for path in (
        Path(phase2_path),
        Path(object_graph_candidates_path),
        Path(object_mentions_path),
        Path(phase1_path),
    ):
        if not path.exists():
            raise FileNotFoundError(f"Required input does not exist: {path}")
    phase2 = pd.read_parquet(phase2_path)
    object_graph = pd.read_parquet(object_graph_candidates_path)
    object_mentions = pd.read_parquet(object_mentions_path)
    phase1 = pd.read_parquet(phase1_path)

    nodes, edges = build_evidence_backed_object_graph(phase2, object_graph)
    cards = build_evidence_cards(edges, limit_per_intent=5)
    broad_ranking = build_object_infrastructure_ranking(phase1, object_graph)
    critique_map = build_critique_bottleneck_map(edges)
    benchmark_network = build_benchmark_metric_network(edges)

    out_nodes = Path(out_nodes_path)
    out_edges = Path(out_edges_path)
    out_cards = Path(out_cards_path)
    out_report = Path(out_report_path)
    figures_output = Path(figures_dir)
    source_output = Path(source_data_dir)
    for path in (out_nodes, out_edges, out_cards, out_report, figures_output, source_output):
        if path.suffix:
            path.parent.mkdir(parents=True, exist_ok=True)
        else:
            path.mkdir(parents=True, exist_ok=True)

    nodes.to_csv(out_nodes, index=False)
    edges.to_csv(out_edges, index=False)
    cards.to_csv(out_cards, index=False)
    figure_paths = write_object_graph_figures(
        nodes=nodes,
        edges=edges,
        broad_ranking=broad_ranking,
        critique_map=critique_map,
        benchmark_network=benchmark_network,
        figures_dir=figures_output,
        source_data_dir=source_output,
    )
    out_report.write_text(
        build_object_graph_report(
            nodes=nodes,
            edges=edges,
            cards=cards,
            broad_ranking=broad_ranking,
            critique_map=critique_map,
            benchmark_network=benchmark_network,
            figure_paths=figure_paths,
            object_mentions=object_mentions,
        ),
        encoding="utf-8",
    )
    return {
        "strict_nodes": int(len(nodes)),
        "strict_edges": int(len(edges)),
        "evidence_cards": int(len(cards)),
        "figure_count": len(figure_paths),
        "report_path": str(out_report),
    }


def build_evidence_backed_object_graph(
    phase2: pd.DataFrame,
    object_graph: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Build strict Phase-2 object graph nodes and edges."""
    strict = _strict_phase2_labels(phase2)
    graph_contexts = _prepared_object_graph_contexts(object_graph)
    edges = strict.merge(graph_contexts, on="context_id", how="inner")
    edge_columns = [
        "context_id",
        "canonical_name",
        "object_type",
        "object_category",
        "final_intent",
        "final_relation_subtype",
        "method_edge_type",
        "evidence_span_phase2",
        "phase2_confidence",
        "resolved_cited_acl_id",
        "resolved_cited_title",
        "sentence_text",
        "rationale_short",
    ]
    edges = _ensure_columns(edges, edge_columns)[edge_columns].drop_duplicates()
    edges["phase2_confidence"] = pd.to_numeric(
        edges["phase2_confidence"],
        errors="coerce",
    ).fillna(0)
    nodes = (
        edges.groupby(["canonical_name", "object_type"], dropna=False)
        .agg(
            evidence_backed_edge_count=("context_id", "size"),
            distinct_contexts=("context_id", "nunique"),
            mean_confidence=("phase2_confidence", "mean"),
        )
        .reset_index()
        .sort_values("evidence_backed_edge_count", ascending=False)
    )
    return nodes, edges


def build_evidence_cards(edges: pd.DataFrame, *, limit_per_intent: int = 5) -> pd.DataFrame:
    """Create report-ready evidence cards from strict graph edges."""
    rows = []
    for intent in [i for i in INTENT_ORDER if i != "unclear"]:
        subset = edges.loc[edges["final_intent"].eq(intent)].copy()
        subset = subset.sort_values(["phase2_confidence", "context_id"], ascending=[False, True])
        for row in subset.head(limit_per_intent).to_dict(orient="records"):
            rows.append(
                {
                    "context_id": _clean(row.get("context_id")),
                    "final_intent": intent,
                    "object_name": _clean(row.get("canonical_name")),
                    "object_type": _clean(row.get("object_type")),
                    "cited_title": _clean(row.get("resolved_cited_title")),
                    "citation_sentence": _clean(row.get("sentence_text")),
                    "evidence_span": _clean(row.get("evidence_span_phase2")),
                    "relation_subtype": _clean(row.get("final_relation_subtype")),
                    "method_edge_type": _clean(row.get("method_edge_type")),
                    "why_interesting": _clean(row.get("rationale_short")),
                }
            )
    return pd.DataFrame(rows)


def assign_critique_cue_family(text: str) -> str:
    """Assign a simple critique/bottleneck cue family."""
    lowered = _clean(text).casefold()
    families = [
        ("fails", ("fails", "fail to", "often fails")),
        ("cannot_or_unable", ("cannot", "can not", "unable")),
        ("limited_or_limitation", ("limited", "limitation", "limitations")),
        ("drawback_or_problem", ("drawback", "problem", "problematic")),
        ("poor_performance", ("poor", "performs poorly", "worse")),
        ("metric_limitation", ("metric", "score", "rouge", "bleu", "does not capture")),
        (
            "data_or_resource_requirement",
            ("requires", "required", "low-resource", "parallel sentences"),
        ),
        ("generalization_or_scalability", ("generaliz", "scalab", "domain")),
    ]
    for family, cues in families:
        if any(cue in lowered for cue in cues):
            return family
    return "other"


def build_critique_bottleneck_map(edges: pd.DataFrame) -> pd.DataFrame:
    critiques = edges.loc[edges["final_intent"].eq("critiques")].copy()
    if critiques.empty:
        return pd.DataFrame(columns=["cue_family", "object_type", "rows"])
    critiques["cue_family"] = critiques["evidence_span_phase2"].map(assign_critique_cue_family)
    return (
        critiques.groupby(["cue_family", "object_type"], dropna=False)
        .size()
        .reset_index(name="rows")
        .sort_values("rows", ascending=False)
    )


def build_benchmark_metric_network(edges: pd.DataFrame) -> pd.DataFrame:
    """Filter strict edges for common metric/benchmark names."""
    metric_pattern = (
        "bleu|rouge|meteor|f1|accuracy|perplexity|bertscore|squad|glue|semeval|wmt"
    )
    mask = edges["canonical_name"].str.contains(metric_pattern, case=False, na=False) | edges[
        "object_type"
    ].isin(["metric", "benchmark_or_protocol"])
    network = edges.loc[mask].copy()
    if network.empty:
        return pd.DataFrame(columns=["canonical_name", "final_intent", "rows"])
    return (
        network.groupby(["canonical_name", "object_type", "final_intent"], dropna=False)
        .size()
        .reset_index(name="rows")
        .sort_values("rows", ascending=False)
    )


def write_object_graph_figures(
    *,
    nodes: pd.DataFrame,
    edges: pd.DataFrame,
    broad_ranking: pd.DataFrame,
    critique_map: pd.DataFrame,
    benchmark_network: pd.DataFrame,
    figures_dir: Path,
    source_data_dir: Path,
) -> dict[str, str]:
    figures_dir.mkdir(parents=True, exist_ok=True)
    source_data_dir.mkdir(parents=True, exist_ok=True)
    source_map = {
        "evidence_backed_object_graph_top20": nodes.head(20),
        "method_edge_type_by_object_type": _method_edge_by_object_type(edges),
        "critique_bottleneck_map": critique_map,
        "benchmark_metric_network": benchmark_network,
        "strict_vs_broad_object_rankings": _strict_vs_broad_rankings(nodes, broad_ranking),
    }
    for name, data in source_map.items():
        data.to_csv(source_data_dir / f"{name}.csv", index=False)
    outputs = {}
    _plot_horizontal_bar(
        nodes.head(20).sort_values("evidence_backed_edge_count"),
        "canonical_name",
        "evidence_backed_edge_count",
        figures_dir / "evidence_backed_object_graph_top20.png",
        "Top Evidence-Backed Object Nodes",
    )
    outputs["evidence_backed_object_graph_top20"] = str(
        figures_dir / "evidence_backed_object_graph_top20.png"
    )
    _plot_matrix_heatmap(
        _method_edge_by_object_type(edges),
        figures_dir / "method_edge_type_by_object_type.png",
        "Method Edge Type By Object Type",
        index_column="object_type",
        columns_column="method_edge_type",
    )
    outputs["method_edge_type_by_object_type"] = str(
        figures_dir / "method_edge_type_by_object_type.png"
    )
    _plot_bubble_table(
        critique_map,
        "cue_family",
        "object_type",
        "rows",
        figures_dir / "critique_bottleneck_map.png",
        "Critique Bottleneck Map",
    )
    outputs["critique_bottleneck_map"] = str(figures_dir / "critique_bottleneck_map.png")
    _plot_matrix_heatmap(
        benchmark_network.head(30),
        figures_dir / "benchmark_metric_network.png",
        "Benchmark And Metric Network",
        index_column="canonical_name",
        columns_column="final_intent",
    )
    outputs["benchmark_metric_network"] = str(figures_dir / "benchmark_metric_network.png")
    return outputs


def build_object_graph_report(
    *,
    nodes: pd.DataFrame,
    edges: pd.DataFrame,
    cards: pd.DataFrame,
    broad_ranking: pd.DataFrame,
    critique_map: pd.DataFrame,
    benchmark_network: pd.DataFrame,
    figure_paths: dict[str, str],
    object_mentions: pd.DataFrame,
) -> str:
    return "\n".join(
        [
            "# Evidence-Backed Object-Use Mini Graph Report",
            "",
            "This is a course-scale object-use graph inspired by evidence-grounded "
            "methodological evolution graphs. It is not a full method evolution graph. "
            "Strict edges use Phase-2 labels with grounded evidence and confidence >= 0.7.",
            "",
            "## Core Counts",
            _table(
                pd.DataFrame(
                    [
                        {"metric": "strict_object_nodes", "value": len(nodes)},
                        {"metric": "strict_object_edges", "value": len(edges)},
                        {"metric": "evidence_cards", "value": len(cards)},
                        {"metric": "full_object_mentions", "value": len(object_mentions)},
                        {"metric": "broad_phase1_objects", "value": len(broad_ranking)},
                    ]
                )
            ),
            "",
            "## Top Strict Evidence-Backed Object Nodes",
            _table(nodes.head(40)),
            "",
            "## Broad Candidate-Level Object Ranking",
            _table(broad_ranking.head(40)),
            "",
            "## Critique Bottleneck Map",
            _table(critique_map),
            "",
            "## Benchmark Metric Network",
            _table(benchmark_network.head(60)),
            "",
            "## Evidence Cards",
            _table(cards),
            "",
            "## Figure Files",
            _table(pd.DataFrame([{"figure": k, "path": v} for k, v in figure_paths.items()])),
            "",
        ]
    )


def _optional_parquet(path: str | Path | None) -> pd.DataFrame | None:
    if path is None:
        return None
    parquet_path = Path(path)
    if not parquet_path.exists():
        return None
    return pd.read_parquet(parquet_path)


def _optional_parquet_row_count(path: str | Path) -> int | None:
    parquet_path = Path(path)
    if not parquet_path.exists():
        return None
    return int(pq.ParquetFile(parquet_path).metadata.num_rows)


def _optional_len(frame: pd.DataFrame | None) -> int:
    return int(len(frame)) if frame is not None else 0


def _bool_series(frame: pd.DataFrame, column: str) -> pd.Series:
    if column not in frame:
        return pd.Series(False, index=frame.index)
    return frame[column].map(_bool_value)


def _split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in _clean(value).split(";") if part.strip()]


def _first_semicolon(value: Any) -> str:
    parts = _split_semicolon(_clean(value))
    return parts[0] if parts else ""


def _object_intent_matrix(
    frame: pd.DataFrame,
    *,
    object_column: str,
    type_column: str,
    intent_column: str,
) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(columns=["canonical_name", "object_type", "total"])
    counts = (
        frame.groupby([object_column, type_column, intent_column], dropna=False)
        .size()
        .reset_index(name="rows")
    )
    pivot = counts.pivot_table(
        index=[object_column, type_column],
        columns=intent_column,
        values="rows",
        fill_value=0,
        aggfunc="sum",
    ).reset_index()
    for intent in INTENT_ORDER:
        if intent not in pivot:
            pivot[intent] = 0
    pivot["total"] = pivot[[intent for intent in INTENT_ORDER if intent in pivot]].sum(axis=1)
    return pivot.sort_values("total", ascending=False).rename(
        columns={object_column: "canonical_name", type_column: "object_type"}
    )


def _shortlist_rows(frame: pd.DataFrame, case_type: str) -> list[dict[str, Any]]:
    rows = []
    for row in frame.to_dict(orient="records"):
        rows.append(
            {
                "case_type": case_type,
                "entity_id": _clean(row.get("resolved_cited_acl_id")),
                "entity_title_or_name": _clean(row.get("resolved_cited_title")),
                "object_type": "",
                "total_count": int(row.get("total_strong_contexts", 0)),
                "evidence_use_count": int(row.get("evidence_use_count", 0)),
                "share": _float_value(row.get("use_share")),
            }
        )
    return rows


def _strict_phase2_labels(phase2: pd.DataFrame) -> pd.DataFrame:
    frame = _ensure_columns(phase2.copy(), _required_label_columns())
    confidence = pd.to_numeric(frame["phase2_confidence"], errors="coerce").fillna(0)
    mask = (
        ~frame["abstain"].map(_bool_value)
        & frame["evidence_supports_label"].map(_clean).eq("true")
        & confidence.ge(0.7)
        & frame.apply(_evidence_span_grounded, axis=1)
    )
    return frame.loc[mask].copy()


def _method_edge_by_object_type(edges: pd.DataFrame) -> pd.DataFrame:
    if edges.empty:
        return pd.DataFrame(columns=["object_type", "method_edge_type", "rows"])
    return (
        edges.groupby(["object_type", "method_edge_type"], dropna=False)
        .size()
        .reset_index(name="rows")
        .sort_values(["object_type", "rows"], ascending=[True, False])
    )


def _prepared_object_graph_contexts(object_graph: pd.DataFrame) -> pd.DataFrame:
    has_allow = "allow_in_object_graph" in object_graph.columns
    has_graph_eligible = "graph_eligible" in object_graph.columns
    columns = [
        "context_id",
        "canonical_name",
        "object_type",
        "object_category",
        "confidence",
        "matched_in",
        "allow_in_object_graph",
        "graph_eligible",
    ]
    graph = _ensure_columns(object_graph.copy(), columns)
    graph["context_id"] = graph["context_id"].map(_clean)
    graph["canonical_name"] = graph["canonical_name"].map(_clean)
    graph["object_type"] = graph["object_type"].map(_clean)
    graph["object_category"] = graph["object_category"].map(_clean)
    graph = graph.loc[graph["context_id"].ne("") & graph["canonical_name"].ne("")]
    graph = graph.loc[~graph["canonical_name"].str.casefold().isin(PSEUDO_OBJECT_NODE_NAMES)]
    if has_allow:
        graph = graph.loc[graph["allow_in_object_graph"].map(_bool_value)]
    if has_graph_eligible:
        graph = graph.loc[graph["graph_eligible"].map(_bool_value)]
    graph["confidence"] = pd.to_numeric(graph["confidence"], errors="coerce").fillna(0)
    graph["matched_in_priority"] = graph["matched_in"].map(_matched_in_priority)
    graph = graph.sort_values(
        ["context_id", "confidence", "matched_in_priority", "canonical_name"],
        ascending=[True, False, False, True],
    )
    graph = graph.groupby("context_id", dropna=False).head(3)
    return graph[["context_id", "canonical_name", "object_type", "object_category"]]


def _matched_in_priority(value: Any) -> int:
    text = _clean(value).casefold()
    if "sentence" in text:
        return 3
    if "context_window" in text:
        return 2
    if "neighbor" in text:
        return 1
    return 0


def _strict_vs_broad_rankings(nodes: pd.DataFrame, broad_ranking: pd.DataFrame) -> pd.DataFrame:
    strict = nodes[["canonical_name", "evidence_backed_edge_count"]].copy()
    strict["strict_rank"] = strict["evidence_backed_edge_count"].rank(
        method="min",
        ascending=False,
    )
    if broad_ranking.empty:
        broad = pd.DataFrame(columns=["canonical_name", "total_graph_candidate_mentions"])
    else:
        broad = broad_ranking[["canonical_name", "total_graph_candidate_mentions"]].copy()
    broad["broad_rank"] = broad["total_graph_candidate_mentions"].rank(
        method="min",
        ascending=False,
    )
    return strict.merge(broad, on="canonical_name", how="outer").sort_values(
        ["strict_rank", "broad_rank"],
        na_position="last",
    )


def _plot_horizontal_bar(
    data: pd.DataFrame,
    label_column: str,
    value_column: str,
    output: Path,
    title: str,
) -> None:
    fig_height = max(4.5, min(12.0, len(data) * 0.35))
    fig, ax = plt.subplots(figsize=(9, fig_height))
    if data.empty:
        ax.text(0.5, 0.5, "No data", ha="center", va="center")
        ax.set_axis_off()
    else:
        labels = data[label_column].astype(str)
        values = pd.to_numeric(data[value_column], errors="coerce").fillna(0)
        ax.barh(labels, values, color="#4B7F9F")
        ax.set_xlabel("Rows")
        ax.set_title(title)
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)


def _plot_matrix_heatmap(
    data: pd.DataFrame,
    output: Path,
    title: str,
    *,
    index_column: str = "canonical_name",
    columns_column: str | None = None,
) -> None:
    fig, ax = plt.subplots(figsize=(10, max(4, min(10, len(data) * 0.35))))
    if data.empty:
        ax.text(0.5, 0.5, "No data", ha="center", va="center")
        ax.set_axis_off()
    else:
        if columns_column:
            matrix = data.pivot_table(
                index=index_column,
                columns=columns_column,
                values="rows",
                aggfunc="sum",
                fill_value=0,
            )
        else:
            value_columns = [col for col in INTENT_ORDER if col in data.columns]
            matrix = data.set_index(index_column)[value_columns]
        image = ax.imshow(matrix.to_numpy(dtype=float), aspect="auto", cmap="Blues")
        ax.set_xticks(range(len(matrix.columns)))
        ax.set_xticklabels(matrix.columns, rotation=35, ha="right")
        ax.set_yticks(range(len(matrix.index)))
        ax.set_yticklabels(matrix.index)
        ax.set_title(title)
        fig.colorbar(image, ax=ax, fraction=0.03, pad=0.02)
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)


def _plot_section_rate_heatmap(data: pd.DataFrame, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    if data.empty:
        ax.text(0.5, 0.5, "No section data", ha="center", va="center")
        ax.set_axis_off()
    else:
        matrix = data.pivot_table(
            index="normalized_section",
            columns="primary_candidate_intent",
            values="rate_within_section",
            aggfunc="sum",
            fill_value=0,
        )
        matrix = matrix[[col for col in INTENT_ORDER if col in matrix.columns]]
        image = ax.imshow(matrix.to_numpy(dtype=float), aspect="auto", cmap="YlGnBu", vmin=0)
        ax.set_xticks(range(len(matrix.columns)))
        ax.set_xticklabels(matrix.columns, rotation=35, ha="right")
        ax.set_yticks(range(len(matrix.index)))
        ax.set_yticklabels(matrix.index)
        ax.set_title("P(Phase-1 Function | Section)")
        fig.colorbar(image, ax=ax, fraction=0.03, pad=0.02)
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)


def _plot_flow_stacked_bar(data: pd.DataFrame, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    if data.empty:
        ax.text(0.5, 0.5, "No flow data", ha="center", va="center")
        ax.set_axis_off()
    else:
        pivot = data.pivot_table(
            index="source",
            columns="target",
            values="rows",
            aggfunc="sum",
            fill_value=0,
        )
        pivot = pivot[[col for col in INTENT_ORDER if col in pivot.columns]]
        bottom = pd.Series(0, index=pivot.index)
        colors = [
            "#4B7F9F",
            "#D17A22",
            "#6A994E",
            "#B56576",
            "#7A6F9B",
            "#5D737E",
            "#999999",
        ]
        for index, column in enumerate(pivot.columns):
            ax.bar(
                pivot.index,
                pivot[column],
                bottom=bottom,
                label=column,
                color=colors[index % len(colors)],
            )
            bottom += pivot[column]
        ax.set_title("Phase-1 To Phase-2 Correction Flow")
        ax.set_ylabel("Rows")
        ax.tick_params(axis="x", rotation=30)
        ax.legend(fontsize="small")
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)


def _plot_top_objects_by_function(data: pd.DataFrame, output: Path) -> None:
    columns = [
        "phase1_uses_count",
        "phase1_compares_count",
        "phase1_extends_count",
        "phase1_critiques_count",
        "phase1_applies_count",
        "background_count",
    ]
    plot_data = data[["canonical_name", *columns]].copy() if not data.empty else data
    renamed = plot_data.rename(
        columns={
            "phase1_uses_count": "uses",
            "phase1_compares_count": "compares_against",
            "phase1_extends_count": "extends",
            "phase1_critiques_count": "critiques",
            "phase1_applies_count": "applies",
            "background_count": "background",
        }
    )
    _plot_matrix_heatmap(
        renamed,
        output,
        "Top Objects By Candidate Function",
        index_column="canonical_name",
    )


def _plot_infrastructure_quadrant(data: pd.DataFrame, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 6))
    if data.empty:
        ax.text(0.5, 0.5, "No object data", ha="center", va="center")
        ax.set_axis_off()
    else:
        sizes = (
            pd.to_numeric(data["total_graph_candidate_mentions"], errors="coerce")
            .fillna(0)
            .clip(lower=1)
            .pow(0.5)
            * 18
        )
        ax.scatter(
            data["use_share"],
            data["compare_share"],
            s=sizes,
            alpha=0.65,
            color="#4B7F9F",
        )
        for _, row in data.head(15).iterrows():
            ax.annotate(
                _clean(row.get("canonical_name")),
                (row.get("use_share", 0), row.get("compare_share", 0)),
                fontsize=7,
            )
        ax.set_xlabel("Use Share")
        ax.set_ylabel("Compare Share")
        ax.set_title("Infrastructure Quadrant")
        ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)


def _plot_bubble_table(
    data: pd.DataFrame,
    x_column: str,
    y_column: str,
    size_column: str,
    output: Path,
    title: str,
) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    if data.empty:
        ax.text(0.5, 0.5, "No data", ha="center", va="center")
        ax.set_axis_off()
    else:
        x_values = sorted(data[x_column].map(_clean).unique())
        y_values = sorted(data[y_column].map(_clean).unique())
        x_index = {value: idx for idx, value in enumerate(x_values)}
        y_index = {value: idx for idx, value in enumerate(y_values)}
        sizes = pd.to_numeric(data[size_column], errors="coerce").fillna(0) * 80
        ax.scatter(
            data[x_column].map(_clean).map(x_index),
            data[y_column].map(_clean).map(y_index),
            s=sizes,
            alpha=0.65,
            color="#B56576",
        )
        ax.set_xticks(range(len(x_values)))
        ax.set_xticklabels(x_values, rotation=35, ha="right")
        ax.set_yticks(range(len(y_values)))
        ax.set_yticklabels(y_values)
        ax.set_title(title)
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)


def _title_from_name(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("_"))


def _ensure_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        if column not in df:
            df[column] = ""
    return df


def _clean(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


def _float_value(value: Any) -> float:
    if value is None or pd.isna(value):
        return 0.0
    return float(value)


def _bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None or pd.isna(value):
        return False
    return str(value).strip().lower() in {"true", "1", "yes"}


def _safe_rate(numerator: int, denominator: int) -> float:
    return float(numerator / denominator) if denominator else 0.0


def _truncate(value: str, length: int) -> str:
    text = _clean(value).replace("\n", " ")
    return text if len(text) <= length else f"{text[: length - 3]}..."


def _table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    return frame.to_markdown(index=False)
