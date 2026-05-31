from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest
from typer.testing import CliRunner

from citeevidence.cli import app
from citeevidence.phase2 import (
    PHASE2_PROMPT_VERSION,
    PHASE2_RESULT_COLUMNS,
    Phase2StructuredLabel,
    build_phase2_input_queue,
    build_phase2_metrics,
    build_phase2_report,
    build_phase2_review_sample,
    extract_phase2_sample_row,
    phase2_structured_cache_key,
    validate_phase2_decision,
)


def _queue_row(
    context_id: str = "ctx_use",
    *,
    sentence_text: str = "In this paper, we use BERT for tagging.",
    primary_candidate_intent: str = "uses",
    evidence_span: str = "we use",
    object_type_source: str = "object_mention",
    object_names: str = "BERT",
    graph_candidate_object_names: str = "BERT",
    cited_title_profile_object_names: str = "",
    primary_candidate_object_type: str = "model",
) -> dict[str, object]:
    return {
        "context_id": context_id,
        "source_context_id": f"src_{context_id}",
        "citing_paper_id": "P00-0001",
        "resolved_cited_acl_id": "P00-0002",
        "resolved_cited_title": "BERT: Pre-training of Deep Bidirectional Transformers",
        "resolved_cited_year": "2019",
        "resolved_cited_authors": "Devlin, Jacob",
        "normalized_section": "method",
        "raw_section_name": "Method",
        "citation_marker": "(Devlin et al., 2019)",
        "sentence_text": sentence_text,
        "context_window_s3": sentence_text,
        "object_names": object_names,
        "object_types": primary_candidate_object_type,
        "graph_candidate_object_names": graph_candidate_object_names,
        "generic_metric_names": "",
        "cited_title_profile_object_names": cited_title_profile_object_names,
        "primary_candidate_intent": primary_candidate_intent,
        "candidate_intents": primary_candidate_intent,
        "primary_candidate_object_type": primary_candidate_object_type,
        "object_type_source": object_type_source,
        "object_type_confidence": 0.9,
        "candidate_relation_subtypes": "direct_use",
        "evidence_span": evidence_span,
        "confidence": 0.86,
        "llm_priority": "high",
        "llm_reason": "fixture",
        "phase2_candidate_type": "explicit_current_paper_relation",
        "cited_work_description": False,
        "phase1_reason": "fixture",
        "matched_rules": "current_paper_use_cue",
    }


def _valid_decision(**overrides: object) -> Phase2StructuredLabel:
    values = {
        "final_intent": "uses",
        "final_object_type": "model",
        "final_relation_subtype": "direct_use",
        "method_edge_type": "uses_component",
        "stance": "neutral",
        "evidence_span": "we use",
        "problem_or_motivation_quote": None,
        "usage_or_mechanism_quote": "we use",
        "comparison_or_tradeoff_quote": None,
        "evidence_supports_label": "true",
        "abstain": False,
        "abstain_reason": "null",
        "confidence": 0.88,
        "rationale_short": "The citation context states current-paper use.",
    }
    values.update(overrides)
    return Phase2StructuredLabel(**values)


def _write_inputs(tmp_path: Path, rows: list[dict[str, object]] | None = None) -> tuple[Path, ...]:
    queue = pd.DataFrame(rows or [_queue_row(), _queue_row("ctx_use2")])
    queue_path = tmp_path / "queue.parquet"
    candidates_path = tmp_path / "candidates.parquet"
    features_path = tmp_path / "features.parquet"
    contexts_path = tmp_path / "contexts.parquet"
    mentions_path = tmp_path / "object_mentions.parquet"
    graph_path = tmp_path / "graph.parquet"
    title_profiles_path = tmp_path / "title_profiles.parquet"
    queue.to_parquet(queue_path, index=False)
    queue.to_parquet(candidates_path, index=False)
    queue[["context_id", "matched_rules"]].to_parquet(features_path, index=False)
    queue[
        [
            "context_id",
            "source_context_id",
            "citing_paper_id",
            "resolved_cited_acl_id",
            "resolved_cited_title",
            "resolved_cited_year",
            "resolved_cited_authors",
            "normalized_section",
            "raw_section_name",
            "citation_marker",
            "sentence_text",
            "context_window_s3",
        ]
    ].to_parquet(contexts_path, index=False)
    pd.DataFrame({"context_id": []}).to_parquet(mentions_path, index=False)
    pd.DataFrame({"context_id": []}).to_parquet(graph_path, index=False)
    pd.DataFrame({"context_id": []}).to_parquet(title_profiles_path, index=False)
    return (
        queue_path,
        candidates_path,
        features_path,
        contexts_path,
        mentions_path,
        graph_path,
        title_profiles_path,
    )


def test_phase2_dry_run_cli_creates_prompts_without_api_key(tmp_path: Path) -> None:
    (
        queue_path,
        candidates_path,
        features_path,
        contexts_path,
        mentions_path,
        graph_path,
        title_profiles_path,
    ) = _write_inputs(tmp_path)
    jsonl_out = tmp_path / "phase2.jsonl"
    parquet_out = tmp_path / "phase2.parquet"
    failed_out = tmp_path / "failed.jsonl"
    prompts_out = tmp_path / "prompts.jsonl"
    report = tmp_path / "report.md"
    review_sample = tmp_path / "review.csv"
    jsonl_out.write_text("existing labels\n", encoding="utf-8")

    result = CliRunner().invoke(
        app,
        [
            "phase2",
            "extract-structured",
            "--queue",
            str(queue_path),
            "--candidates",
            str(candidates_path),
            "--features",
            str(features_path),
            "--contexts",
            str(contexts_path),
            "--object-mentions",
            str(mentions_path),
            "--object-graph-candidates",
            str(graph_path),
            "--cited-title-profiles",
            str(title_profiles_path),
            "--jsonl-out",
            str(jsonl_out),
            "--parquet-out",
            str(parquet_out),
            "--failed-out",
            str(failed_out),
            "--dry-run-prompts-out",
            str(prompts_out),
            "--report",
            str(report),
            "--review-sample",
            str(review_sample),
            "--limit",
            "2",
            "--dry-run",
        ],
    )

    assert result.exit_code == 0
    assert jsonl_out.read_text(encoding="utf-8") == "existing labels\n"
    assert len(prompts_out.read_text(encoding="utf-8").splitlines()) == 2
    assert failed_out.read_text(encoding="utf-8") == ""
    assert pd.read_parquet(parquet_out).empty
    assert pd.read_csv(review_sample).empty
    assert "Phase-2 LLM Structured Evidence Extraction" in report.read_text(encoding="utf-8")


def test_phase2_pydantic_validation_catches_invalid_enum() -> None:
    with pytest.raises(ValueError):
        _valid_decision(final_intent="maybe")


def test_phase2_invalid_evidence_span_is_rejected() -> None:
    row = _queue_row()
    decision = _valid_decision(evidence_span="not in the sentence")

    with pytest.raises(ValueError, match="evidence_span"):
        validate_phase2_decision(decision, row)


def test_phase2_non_null_quote_must_be_in_context() -> None:
    row = _queue_row()
    decision = _valid_decision(usage_or_mechanism_quote="missing quote")

    with pytest.raises(ValueError, match="usage_or_mechanism_quote"):
        validate_phase2_decision(decision, row)


def test_phase2_abstain_rules_are_conservative() -> None:
    with pytest.raises(ValueError, match="confidence"):
        _valid_decision(
            final_intent="unclear",
            evidence_span="",
            evidence_supports_label="unclear",
            abstain=True,
            abstain_reason="insufficient_evidence",
            confidence=0.8,
        )

    decision = _valid_decision(
        final_intent="unclear",
        final_object_type="unknown",
        final_relation_subtype="none",
        method_edge_type="not_method_related",
        stance="unclear",
        evidence_span="",
        usage_or_mechanism_quote=None,
        evidence_supports_label="unclear",
        abstain=True,
        abstain_reason="insufficient_evidence",
        confidence=0.3,
    )
    validate_phase2_decision(decision, _queue_row())


def test_phase2_non_abstain_requires_evidence_supports_true() -> None:
    row = _queue_row()
    with pytest.raises(ValueError, match="evidence_supports_label=true"):
        validate_phase2_decision(
            _valid_decision(evidence_supports_label="false"),
            row,
        )
    with pytest.raises(ValueError, match="evidence_supports_label=true"):
        validate_phase2_decision(
            _valid_decision(evidence_supports_label="unclear"),
            row,
        )


def test_phase2_abstain_accepts_false_evidence_support_with_low_confidence() -> None:
    decision = _valid_decision(
        final_intent="unclear",
        final_object_type="unknown",
        final_relation_subtype="none",
        method_edge_type="not_method_related",
        stance="unclear",
        evidence_span="",
        usage_or_mechanism_quote=None,
        evidence_supports_label="false",
        abstain=True,
        abstain_reason="insufficient_evidence",
        confidence=0.2,
    )
    validate_phase2_decision(decision, _queue_row())


def test_phase2_background_phase1_can_be_corrected_to_uses() -> None:
    row = _queue_row(primary_candidate_intent="background")
    decision = _valid_decision(final_intent="uses", evidence_span="we use")

    validate_phase2_decision(decision, row)


def test_phase2_cited_title_only_object_is_not_direct_evidence() -> None:
    row = _queue_row(
        sentence_text="This method improves tagging accuracy.",
        primary_candidate_intent="background",
        evidence_span="improves",
        object_type_source="cited_title_profile",
        object_names="",
        graph_candidate_object_names="",
        cited_title_profile_object_names="BERT",
    )
    decision = _valid_decision(
        final_intent="extends",
        final_object_type="model",
        final_relation_subtype="improve",
        method_edge_type="improves",
        evidence_span="improves",
        usage_or_mechanism_quote=None,
    )

    with pytest.raises(ValueError, match="cited-title-only"):
        validate_phase2_decision(decision, row)


def test_phase2_report_generation_with_fake_outputs(tmp_path: Path) -> None:
    row = _queue_row()
    decision = _valid_decision()
    record = {
        **row,
        "prompt_version": PHASE2_PROMPT_VERSION,
        "model": "fixture-model",
        "cache_key": phase2_structured_cache_key(
            {**row, "prompt_version": PHASE2_PROMPT_VERSION, "model": "fixture-model"}
        ),
        "sample_row_id": "phase2_structured_0001",
        "final_intent": decision.final_intent,
        "final_object_type": decision.final_object_type,
        "final_relation_subtype": decision.final_relation_subtype,
        "method_edge_type": decision.method_edge_type,
        "stance": decision.stance,
        "evidence_span_phase2": decision.evidence_span,
        "problem_or_motivation_quote": decision.problem_or_motivation_quote,
        "usage_or_mechanism_quote": decision.usage_or_mechanism_quote,
        "comparison_or_tradeoff_quote": decision.comparison_or_tradeoff_quote,
        "evidence_supports_label": decision.evidence_supports_label,
        "abstain": decision.abstain,
        "abstain_reason": decision.abstain_reason,
        "phase2_confidence": decision.confidence,
        "rationale_short": decision.rationale_short,
        "review_status": "structured_extracted",
        "validation_error": "",
        "attempts": 1,
        "from_cache": False,
        "model_used": "fixture-model",
        "input_tokens": 10,
        "output_tokens": 5,
        "total_tokens": 15,
    }
    results = pd.DataFrame([record]).reindex(columns=PHASE2_RESULT_COLUMNS)
    queue = pd.DataFrame([row])
    failed = pd.DataFrame()

    metrics = build_phase2_metrics(
        queue=queue,
        results=results,
        failed=failed,
        dry_run=False,
        dry_run_prompt_records=0,
    )
    report = build_phase2_report(
        metrics=metrics,
        results=results,
        failed=failed,
        jsonl_out=tmp_path / "labels.jsonl",
        parquet_out=tmp_path / "labels.parquet",
        failed_out=tmp_path / "failed.jsonl",
        review_sample_out=tmp_path / "review.csv",
        dry_run=False,
    )
    review_sample = build_phase2_review_sample(results, seed=42)

    assert "Final Intent Distribution" in report
    assert metrics["successful_rows"] == 1
    assert metrics["token_usage"]["total_tokens"] == 15
    assert review_sample.shape[0] == 1
    assert {"reviewer_correct", "reviewer_notes"} <= set(review_sample.columns)


def test_phase2_input_queue_fills_missing_object_fields_from_tables() -> None:
    queue = pd.DataFrame(
        [
            _queue_row(
                object_names="",
                graph_candidate_object_names="",
                cited_title_profile_object_names="",
                primary_candidate_object_type="unknown",
            )
        ]
    )
    candidates = queue.copy()
    contexts = queue[
        [
            "context_id",
            "source_context_id",
            "citing_paper_id",
            "resolved_cited_acl_id",
            "resolved_cited_title",
            "resolved_cited_year",
            "resolved_cited_authors",
            "normalized_section",
            "raw_section_name",
            "citation_marker",
            "sentence_text",
            "context_window_s3",
        ]
    ].copy()
    object_mentions = pd.DataFrame(
        [
            {
                "context_id": "ctx_use",
                "canonical_name": "BERT",
                "object_type": "model",
                "object_category": "named_object",
            },
            {
                "context_id": "ctx_use",
                "canonical_name": "F1",
                "object_type": "metric",
                "object_category": "generic_metric",
            },
        ]
    )
    graph = pd.DataFrame(
        [
            {
                "context_id": "ctx_use",
                "canonical_name": "BERT",
                "object_type": "model",
                "object_category": "named_object",
            }
        ]
    )
    title_profiles = pd.DataFrame(
        [
            {
                "context_id": "ctx_use",
                "canonical_name": "Transformer",
                "object_type": "model",
                "object_category": "named_object",
            }
        ]
    )

    prepared = build_phase2_input_queue(
        queue=queue,
        candidates=candidates,
        contexts=contexts,
        object_mentions=object_mentions,
        object_graph_candidates=graph,
        cited_title_profiles=title_profiles,
        model="fixture-model",
    )

    row = prepared.iloc[0]
    assert row["object_names"] == "BERT;F1"
    assert row["object_types"] == "model;metric"
    assert row["generic_metric_names"] == "F1"
    assert row["graph_candidate_object_names"] == "BERT"
    assert row["cited_title_profile_object_names"] == "Transformer"


def test_phase2_cache_key_is_deterministic() -> None:
    row = _queue_row()
    row["prompt_version"] = PHASE2_PROMPT_VERSION
    row["model"] = "fixture-model"

    assert phase2_structured_cache_key(row) == phase2_structured_cache_key(dict(row))
    changed = dict(row)
    changed["evidence_span"] = "we employ"
    assert phase2_structured_cache_key(row) != phase2_structured_cache_key(changed)


class _TransientError(Exception):
    status_code = 429


class _FakeUsage:
    input_tokens = 10
    output_tokens = 5
    total_tokens = 15


class _FakeResponse:
    def __init__(self, parsed: Phase2StructuredLabel | None = None, output_text: str = "") -> None:
        self.output_parsed = parsed
        self.output_text = output_text
        self.usage = _FakeUsage()


class _FakeResponses:
    def __init__(self, outcomes: list[object]) -> None:
        self.outcomes = outcomes
        self.calls = 0

    def parse(self, **_: object) -> _FakeResponse:
        outcome = self.outcomes[self.calls]
        self.calls += 1
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


class _FakeClient:
    def __init__(self, outcomes: list[object]) -> None:
        self.responses = _FakeResponses(outcomes)


def test_phase2_transient_failure_then_success_has_attempts_two(tmp_path: Path) -> None:
    row = _queue_row()
    row["prompt_version"] = PHASE2_PROMPT_VERSION
    row["model"] = "fixture-model"
    client = _FakeClient([_TransientError("rate limit"), _FakeResponse(_valid_decision())])

    record, failed = extract_phase2_sample_row(
        row=row,
        client=client,
        model="fixture-model",
        cache_dir=tmp_path,
        backoff_base_seconds=0,
    )

    assert failed is None
    assert record is not None
    assert record["review_status"] == "structured_extracted"
    assert record["attempts"] == 2


def test_phase2_repeated_transient_failure_writes_failed_row(tmp_path: Path) -> None:
    row = _queue_row()
    row["prompt_version"] = PHASE2_PROMPT_VERSION
    row["model"] = "fixture-model"
    client = _FakeClient([_TransientError("rate limit"), _TransientError("still limited")])

    record, failed = extract_phase2_sample_row(
        row=row,
        client=client,
        model="fixture-model",
        cache_dir=tmp_path,
        backoff_base_seconds=0,
    )

    assert record is None
    assert failed is not None
    assert failed["attempts"] == 2
    assert "TransientError" in failed["validation_error"]


def test_phase2_schema_invalid_response_fails_after_retry(tmp_path: Path) -> None:
    row = _queue_row()
    row["prompt_version"] = PHASE2_PROMPT_VERSION
    row["model"] = "fixture-model"
    client = _FakeClient(
        [
            _FakeResponse(output_text='{"final_intent":"bad"}'),
            _FakeResponse(output_text='{"final_intent":"bad"}'),
        ]
    )

    record, failed = extract_phase2_sample_row(
        row=row,
        client=client,
        model="fixture-model",
        cache_dir=tmp_path,
        backoff_base_seconds=0,
    )

    assert record is None
    assert failed is not None
    assert failed["attempts"] == 2
