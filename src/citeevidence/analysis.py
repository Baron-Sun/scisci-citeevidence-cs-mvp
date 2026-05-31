from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib
import pandas as pd

matplotlib.use("Agg")
from matplotlib import pyplot as plt  # noqa: E402

DEFAULT_PHASE2_ANALYSIS_REPORT = Path("reports/phase2_pilot_analysis_report.md")
DEFAULT_PHASE2_ANALYSIS_SUMMARY = Path("data/processed/phase2_pilot_analysis_summary.csv")
DEFAULT_PHASE2_CASE_STUDIES = Path("data/processed/phase2_case_studies.csv")
DEFAULT_PHASE2_CONFUSION = Path("data/processed/phase2_phase1_vs_phase2_confusion.csv")
DEFAULT_PHASE2_FIGURES_DIR = Path("figures")
DEFAULT_PHASE2_SOURCE_DATA_DIR = Path("figures/source_data")
DEFAULT_PHASE2_QUEUE_PATH = Path("data/processed/phase1_llm_queue_sample.parquet")

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
