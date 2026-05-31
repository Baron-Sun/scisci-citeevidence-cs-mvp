from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from citeevidence.cli import app
from citeevidence.phase2 import finalize_phase2_batch_labels


def _label_row(
    context_id: str,
    *,
    evidence_supports_label: str = "true",
    abstain: bool = False,
    phase2_confidence: float = 0.9,
    evidence_span_phase2: str = "use BERT",
    evidence_span: str = "phase1 span",
    final_intent: str = "uses",
    sentence_text: str = "We use BERT for tagging.",
) -> dict[str, object]:
    return {
        "context_id": context_id,
        "primary_candidate_intent": "uses",
        "final_intent": final_intent,
        "final_object_type": "model",
        "final_relation_subtype": "direct_use",
        "method_edge_type": "uses_component",
        "stance": "neutral",
        "normalized_section": "method",
        "resolved_cited_acl_id": "P00-0001",
        "resolved_cited_title": "BERT",
        "sentence_text": sentence_text,
        "context_window_s3": sentence_text,
        "evidence_span_phase2": evidence_span_phase2,
        "evidence_span": evidence_span,
        "problem_or_motivation_quote": "",
        "usage_or_mechanism_quote": evidence_span_phase2,
        "comparison_or_tradeoff_quote": "",
        "evidence_supports_label": evidence_supports_label,
        "abstain": abstain,
        "phase2_confidence": phase2_confidence,
        "rationale_short": "Fixture.",
    }


def test_finalize_batch_labels_filters_and_reports(tmp_path: Path) -> None:
    labels = pd.DataFrame(
        [
            _label_row("ctx_valid"),
            _label_row("ctx_false", evidence_supports_label="false"),
            _label_row("ctx_unclear_support", evidence_supports_label="unclear"),
            _label_row("ctx_abstain", abstain=True),
            _label_row("ctx_low_confidence", phase2_confidence=0.65),
            _label_row(
                "ctx_missing_span",
                evidence_span_phase2="",
                evidence_span="",
                sentence_text="We use BERT.",
            ),
            _label_row("ctx_unclear_intent", final_intent="unclear"),
            _label_row("ctx_ungrounded", evidence_span_phase2="missing span"),
            _label_row("ctx_valid", evidence_span_phase2="use BERT for tagging"),
        ]
    )
    object_graph = pd.DataFrame(
        [
            {
                "context_id": "ctx_valid",
                "canonical_name": "BERT",
                "object_type": "model",
                "object_category": "named_object",
                "confidence": 0.95,
                "matched_in": "sentence",
            },
            {
                "context_id": "ctx_valid",
                "canonical_name": "unknown",
                "object_type": "unknown",
                "object_category": "pseudo",
                "confidence": 0.99,
                "matched_in": "sentence",
            },
        ]
    )
    diagnostics = pd.DataFrame(
        [
            {
                "context_id": "ctx_failed",
                "revalidated": False,
                "failed_validator_type": "schema_error",
            }
        ]
    )
    failed_record = {
        "context_id": "ctx_failed",
        "validation_error": "1 validation error for Phase2StructuredLabel",
    }
    labels_path = tmp_path / "labels.parquet"
    failed_path = tmp_path / "failed.jsonl"
    diagnostics_path = tmp_path / "diagnostics.parquet"
    object_graph_path = tmp_path / "object_graph.parquet"
    out_labels = tmp_path / "analysis_ready.parquet"
    out_excluded = tmp_path / "excluded.parquet"
    out_summary = tmp_path / "summary.csv"
    report = tmp_path / "audit.md"
    labels.to_parquet(labels_path, index=False)
    object_graph.to_parquet(object_graph_path, index=False)
    diagnostics.to_parquet(diagnostics_path, index=False)
    failed_path.write_text(json.dumps(failed_record) + "\n", encoding="utf-8")

    metrics = finalize_phase2_batch_labels(
        labels_path=labels_path,
        failed_path=failed_path,
        failed_diagnostics_path=diagnostics_path,
        object_graph_candidates_path=object_graph_path,
        out_labels_path=out_labels,
        out_excluded_path=out_excluded,
        out_summary_path=out_summary,
        report_path=report,
        stored_object_graph_edges_path=tmp_path / "missing_edges.csv",
    )

    ready = pd.read_parquet(out_labels)
    excluded = pd.read_parquet(out_excluded)
    reasons = set(excluded["exclusion_reason"])
    report_text = report.read_text(encoding="utf-8")
    assert set(ready["context_id"]) == {"ctx_valid"}
    assert metrics["analysis_ready_rows"] == 2
    assert metrics["duplicate_context_id_count_after"] == 2
    assert metrics["recomputed_object_graph_edges"] == 2
    assert metrics["pseudo_node_count"] == 0
    assert {
        "evidence_supports_label_false",
        "evidence_supports_label_unclear",
        "abstain_true",
        "low_confidence",
        "missing_evidence_span",
        "final_intent_unclear",
        "evidence_span_not_grounded",
    }.issubset(reasons)
    assert out_summary.exists()
    assert "\n## Core Metrics\n" in report_text


def test_finalize_batch_labels_cli_help() -> None:
    result = CliRunner().invoke(app, ["phase2", "finalize-batch-labels", "--help"])
    assert result.exit_code == 0
    assert "--out-excluded" in result.output
