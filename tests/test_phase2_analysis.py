from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from citeevidence.analysis import (
    build_phase1_phase2_confusion,
    build_phase2_case_studies,
    build_phase2_pilot_summary_metrics,
    run_phase2_pilot_analysis,
    write_phase2_pilot_figures,
)


def _label_rows() -> pd.DataFrame:
    rows = [
        {
            "context_id": "ctx_use",
            "primary_candidate_intent": "uses",
            "final_intent": "uses",
            "final_object_type": "dataset_or_database",
            "final_relation_subtype": "direct_use",
            "method_edge_type": "uses_component",
            "stance": "neutral",
            "normalized_section": "method",
            "resolved_cited_title": "Penn Treebank",
            "sentence_text": "We use the Penn Treebank for evaluation.",
            "context_window_s3": "We use the Penn Treebank for evaluation.",
            "evidence_span_phase2": "We use the Penn Treebank",
            "problem_or_motivation_quote": "",
            "usage_or_mechanism_quote": "We use the Penn Treebank",
            "comparison_or_tradeoff_quote": "",
            "evidence_supports_label": "true",
            "abstain": False,
            "phase2_confidence": 0.95,
            "rationale_short": "The context states direct current-paper use.",
            "object_names": "Penn Treebank",
            "generic_metric_names": "",
        },
        {
            "context_id": "ctx_compare",
            "primary_candidate_intent": "uses",
            "final_intent": "compares_against",
            "final_object_type": "model",
            "final_relation_subtype": "compare_against",
            "method_edge_type": "compares",
            "stance": "positive",
            "normalized_section": "results",
            "resolved_cited_title": "A Baseline Model",
            "sentence_text": "Our model performs better than the baseline.",
            "context_window_s3": "Our model performs better than the baseline.",
            "evidence_span_phase2": "performs better than the baseline",
            "problem_or_motivation_quote": "",
            "usage_or_mechanism_quote": "",
            "comparison_or_tradeoff_quote": "performs better than the baseline",
            "evidence_supports_label": "true",
            "abstain": False,
            "phase2_confidence": 0.9,
            "rationale_short": "The context compares performance against a baseline.",
            "object_names": "Baseline",
            "generic_metric_names": "accuracy",
        },
        {
            "context_id": "ctx_background",
            "primary_candidate_intent": "background",
            "final_intent": "background",
            "final_object_type": "theory_or_concept",
            "final_relation_subtype": "none",
            "method_edge_type": "background",
            "stance": "neutral",
            "normalized_section": "related_work",
            "resolved_cited_title": "Prior Theory",
            "sentence_text": "Prior work introduced the concept.",
            "context_window_s3": "Prior work introduced the concept.",
            "evidence_span_phase2": "introduced the concept",
            "problem_or_motivation_quote": "introduced the concept",
            "usage_or_mechanism_quote": "",
            "comparison_or_tradeoff_quote": "",
            "evidence_supports_label": "true",
            "abstain": False,
            "phase2_confidence": 0.82,
            "rationale_short": "The citation provides background.",
            "object_names": "",
            "generic_metric_names": "",
        },
        {
            "context_id": "ctx_abstain",
            "primary_candidate_intent": "unclear",
            "final_intent": "unclear",
            "final_object_type": "unknown",
            "final_relation_subtype": "none",
            "method_edge_type": "not_method_related",
            "stance": "unclear",
            "normalized_section": "unknown",
            "resolved_cited_title": "Grouped Citation",
            "sentence_text": "Several studies discuss this.",
            "context_window_s3": "Several studies discuss this.",
            "evidence_span_phase2": "",
            "problem_or_motivation_quote": "",
            "usage_or_mechanism_quote": "",
            "comparison_or_tradeoff_quote": "",
            "evidence_supports_label": "false",
            "abstain": True,
            "phase2_confidence": 0.3,
            "rationale_short": "The grouped citation is ambiguous.",
            "object_names": "",
            "generic_metric_names": "",
        },
    ]
    return pd.DataFrame(rows)


def _failed_diagnostics() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "context_id": "ctx_failed",
                "primary_candidate_intent": "uses",
                "validation_error": "evidence_span is not an exact substring",
                "failed_validator_type": "evidence_span_not_substring",
                "candidate_repair_action": "needs_model_retry_or_manual_review",
                "revalidated": False,
                "revalidation_error": "evidence_span is not an exact substring",
                "final_intent": "uses",
                "final_object_type": "method",
                "evidence_span": "not exact",
                "raw_response": json.dumps(
                    {
                        "final_intent": "uses",
                        "final_object_type": "method",
                        "final_relation_subtype": "direct_use",
                        "method_edge_type": "uses_component",
                        "evidence_span": "not exact",
                        "confidence": 0.8,
                        "rationale_short": "Invalid span.",
                    }
                ),
            },
            {
                "context_id": "ctx_recovered",
                "primary_candidate_intent": "uses",
                "validation_error": "final_intent=uses requires current-paper use evidence",
                "failed_validator_type": "use_cue_not_accepted",
                "candidate_repair_action": "revalidate_after_cue_expansion",
                "revalidated": True,
                "revalidation_error": "",
                "final_intent": "uses",
                "final_object_type": "software_or_tool",
                "evidence_span": "using Sacre-BLEU",
                "raw_response": "{}",
            },
        ]
    )


def _queue_rows() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "context_id": "ctx_failed",
                "normalized_section": "method",
                "resolved_cited_title": "Failed Citation",
                "sentence_text": "We use the method but the model returned a bad span.",
                "context_window_s3": "We use the method but the model returned a bad span.",
            }
        ]
    )


def test_phase2_analysis_summary_metrics_are_computed() -> None:
    metrics = build_phase2_pilot_summary_metrics(
        _label_rows(),
        _failed_diagnostics(),
        [{"context_id": "ctx_failed"}],
    )

    assert metrics["total_phase2_labels"] == 4
    assert metrics["total_remaining_failed_rows"] == 1
    assert metrics["final_failure_rate"] == 0.2
    assert metrics["abstain_count"] == 1
    assert metrics["phase1_phase2_disagreement_count"] == 1
    assert metrics["evidence_span_grounded_count"] == 3


def test_phase2_analysis_confusion_matrix_counts_pairs() -> None:
    confusion = build_phase1_phase2_confusion(_label_rows())

    match = confusion.loc[
        confusion["primary_candidate_intent"].eq("uses")
        & confusion["final_intent"].eq("compares_against"),
        "rows",
    ]
    assert match.iloc[0] == 1


def test_phase2_case_studies_include_available_intents_and_failures() -> None:
    cases = build_phase2_case_studies(
        labels=_label_rows(),
        failed_diagnostics=_failed_diagnostics(),
        queue=_queue_rows(),
        per_intent=1,
        failure_count=1,
    )

    assert {"uses", "compares_against", "background"}.issubset(set(cases["final_intent"]))
    assert cases["report_comment"].str.contains("Remaining failed row").any()
    assert "sentence_text" in cases.columns


def test_phase2_analysis_figures_and_source_data_are_written(tmp_path: Path) -> None:
    figures = write_phase2_pilot_figures(
        labels=_label_rows(),
        figures_dir=tmp_path / "figures",
        source_data_dir=tmp_path / "source",
    )

    assert len(figures) == 6
    for figure in figures.values():
        assert Path(figure).exists()
        assert Path(figure).stat().st_size > 0
    assert (tmp_path / "source" / "phase2_final_intent_distribution.csv").exists()
    assert (tmp_path / "source" / "phase2_intent_by_section.csv").exists()


def test_phase2_analysis_report_generation_works_without_api(tmp_path: Path) -> None:
    labels_path = tmp_path / "labels.parquet"
    failed_diagnostics_path = tmp_path / "failed.parquet"
    failed_jsonl_path = tmp_path / "failed.jsonl"
    queue_path = tmp_path / "queue.parquet"
    _label_rows().to_parquet(labels_path, index=False)
    _failed_diagnostics().to_parquet(failed_diagnostics_path, index=False)
    _queue_rows().to_parquet(queue_path, index=False)
    failed_jsonl_path.write_text(json.dumps({"context_id": "ctx_failed"}) + "\n")

    metrics = run_phase2_pilot_analysis(
        labels_path=labels_path,
        failed_diagnostics_path=failed_diagnostics_path,
        failed_jsonl_path=failed_jsonl_path,
        out_report_path=tmp_path / "report.md",
        out_summary_path=tmp_path / "summary.csv",
        out_case_studies_path=tmp_path / "cases.csv",
        out_confusion_path=tmp_path / "confusion.csv",
        figures_dir=tmp_path / "figures",
        source_data_dir=tmp_path / "source_data",
        queue_path=queue_path,
    )

    assert metrics["total_phase2_labels"] == 4
    assert (tmp_path / "report.md").exists()
    assert "Phase-2 Pilot Analysis Report" in (tmp_path / "report.md").read_text()
    assert pd.read_csv(tmp_path / "summary.csv").shape[0] > 0
    assert pd.read_csv(tmp_path / "cases.csv").shape[0] >= 4
