from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest
from typer.testing import CliRunner

from citeevidence.cli import app
from citeevidence.phase1_llm_review import (
    PHASE1_LLM_RESULT_COLUMNS,
    PHASE1_LLM_REVIEW_PROMPT_VERSION,
    Phase1LLMReviewDecision,
    build_phase1_llm_review_metrics,
    build_phase1_llm_review_report,
    build_phase1_llm_review_sample,
    build_phase1_rule_recommendations,
    phase1_llm_review_cache_key,
    validate_phase1_review_decision,
)


def _candidate(
    context_id: str,
    primary_intent: str,
    *,
    llm_priority: str = "high",
    object_names: str = "BERT",
    object_types: str = "model",
    generic_metric_names: str = "",
    cited_work_description: bool = False,
    candidate_intents: str | None = None,
    has_graph_candidate_object: bool = True,
    evidence_span: str = "we use",
    sentence_text: str | None = None,
) -> dict[str, object]:
    sentence = sentence_text or "In this paper, we use BERT for tagging."
    return {
        "context_id": context_id,
        "citing_paper_id": "P00-0001",
        "resolved_cited_title": "BERT: Pre-training of Deep Bidirectional Transformers",
        "normalized_section": "method",
        "raw_section_name": "Method",
        "citation_marker": "(Devlin et al., 2019)",
        "sentence_text": sentence,
        "context_window_s3": sentence,
        "object_names": object_names,
        "object_types": object_types,
        "generic_metric_names": generic_metric_names,
        "cited_title_profile_object_names": "",
        "primary_candidate_intent": primary_intent,
        "candidate_intents": candidate_intents or primary_intent,
        "primary_candidate_object_type": object_types.split(";")[0] if object_types else "unknown",
        "candidate_relation_subtypes": "direct_use" if primary_intent == "uses" else "none",
        "evidence_span": evidence_span,
        "confidence": 0.85,
        "should_send_to_llm": llm_priority in {"high", "medium"},
        "llm_priority": llm_priority,
        "llm_reason": "fixture",
        "cited_work_description": cited_work_description,
        "matched_rules": "current_paper_use_cue",
        "phase1_reason": "fixture",
        "has_object_mention": bool(object_names),
        "has_graph_candidate_object": has_graph_candidate_object,
    }


def _fixture_candidates() -> pd.DataFrame:
    rows = [
        _candidate("ctx_use", "uses", llm_priority="high"),
        _candidate(
            "ctx_bg",
            "background",
            llm_priority="low",
            cited_work_description=True,
            evidence_span="described",
            sentence_text="Smith et al. (2020) described the task.",
        ),
        _candidate("ctx_ext", "extends", llm_priority="high", evidence_span="improve"),
        _candidate("ctx_app", "applies", llm_priority="medium", evidence_span="applied to"),
        _candidate("ctx_crit", "critiques", llm_priority="high", evidence_span="fails to"),
        _candidate(
            "ctx_cmp",
            "compares_against",
            llm_priority="high",
            generic_metric_names="F1",
            evidence_span="better than",
        ),
        _candidate(
            "ctx_unclear",
            "unclear",
            llm_priority="medium",
            has_graph_candidate_object=True,
            evidence_span="",
        ),
        _candidate(
            "ctx_multi",
            "extends",
            llm_priority="high",
            candidate_intents="uses;compares_against;extends",
            evidence_span="variant of",
        ),
        _candidate(
            "ctx_none",
            "background",
            llm_priority="none",
            object_names="",
            object_types="",
            has_graph_candidate_object=False,
            evidence_span="previous work",
            sentence_text="Previous work has studied this setting.",
        ),
    ]
    return pd.DataFrame(rows)


def _fixture_contexts(candidates: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "context_id": candidates["context_id"],
            "resolved_cited_authors": ["Devlin, Jacob"] * len(candidates),
        }
    )


def _write_cli_inputs(tmp_path: Path) -> tuple[Path, Path, Path, Path, Path, Path]:
    candidates = _fixture_candidates()
    contexts = _fixture_contexts(candidates)
    candidates_path = tmp_path / "candidates.parquet"
    features_path = tmp_path / "features.parquet"
    contexts_path = tmp_path / "contexts.parquet"
    object_mentions_path = tmp_path / "object_mentions.parquet"
    graph_path = tmp_path / "graph.parquet"
    title_profiles_path = tmp_path / "title_profiles.parquet"
    candidates.to_parquet(candidates_path, index=False)
    candidates[["context_id", "matched_rules"]].to_parquet(features_path, index=False)
    contexts.to_parquet(contexts_path, index=False)
    pd.DataFrame({"context_id": []}).to_parquet(object_mentions_path, index=False)
    pd.DataFrame({"context_id": []}).to_parquet(graph_path, index=False)
    pd.DataFrame({"context_id": []}).to_parquet(title_profiles_path, index=False)
    return (
        candidates_path,
        features_path,
        contexts_path,
        object_mentions_path,
        graph_path,
        title_profiles_path,
    )


def _valid_decision(**overrides: object) -> Phase1LLMReviewDecision:
    values = {
        "intent_correct": "true",
        "better_intent": "uses",
        "object_type_correct": "true",
        "better_object_type": "model",
        "relation_subtype_correct": "true",
        "better_relation_subtype": "direct_use",
        "evidence_supports_label": "true",
        "evidence_quote": "we use",
        "should_send_to_llm_correct": "true",
        "better_llm_priority": "high",
        "cited_work_description_correct": "true",
        "error_type": "none",
        "recommended_rule_action": "keep",
        "confidence": 0.9,
        "rationale_short": "The cue supports current-paper use.",
    }
    values.update(overrides)
    return Phase1LLMReviewDecision(**values)


def test_phase1_llm_dry_run_cli_creates_sample_and_prompts(tmp_path: Path) -> None:
    (
        candidates_path,
        features_path,
        contexts_path,
        object_mentions_path,
        graph_path,
        title_profiles_path,
    ) = _write_cli_inputs(tmp_path)
    sample_out = tmp_path / "sample.csv"
    jsonl_out = tmp_path / "prompts.jsonl"
    parquet_out = tmp_path / "results.parquet"
    report = tmp_path / "report.md"
    recommendations = tmp_path / "recommendations.md"

    result = CliRunner().invoke(
        app,
        [
            "review",
            "llm-phase1",
            "--candidates",
            str(candidates_path),
            "--features",
            str(features_path),
            "--contexts",
            str(contexts_path),
            "--object-mentions",
            str(object_mentions_path),
            "--object-graph-candidates",
            str(graph_path),
            "--cited-title-profiles",
            str(title_profiles_path),
            "--sample-out",
            str(sample_out),
            "--jsonl-out",
            str(jsonl_out),
            "--parquet-out",
            str(parquet_out),
            "--report",
            str(report),
            "--recommendations",
            str(recommendations),
            "--limit",
            "8",
            "--dry-run",
        ],
    )

    assert result.exit_code == 0
    assert pd.read_csv(sample_out).shape[0] == 8
    assert len(jsonl_out.read_text(encoding="utf-8").splitlines()) == 8
    assert "Phase-1 LLM-as-Judge" in report.read_text(encoding="utf-8")
    assert "dry run" in recommendations.read_text(encoding="utf-8")


def test_phase1_stratified_sample_covers_available_groups() -> None:
    candidates = _fixture_candidates()
    sample = build_phase1_llm_review_sample(
        candidates=candidates,
        contexts=_fixture_contexts(candidates),
        limit=9,
        seed=7,
        model="fixture-model",
    )

    assert set(sample["primary_candidate_intent"]) >= {
        "uses",
        "background",
        "extends",
        "applies",
        "critiques",
        "compares_against",
        "unclear",
    }
    assert {"high", "medium", "low"} <= set(sample["llm_priority"])
    assert sample["generic_metric_names"].astype(str).str.len().gt(0).any()
    assert sample["candidate_intents"].astype(str).str.contains(";").any()


def test_phase1_review_validation_catches_invalid_evidence_quote() -> None:
    row = _candidate("ctx", "uses")
    decision = _valid_decision(evidence_quote="not in context")

    with pytest.raises(ValueError, match="evidence_quote"):
        validate_phase1_review_decision(decision, row)


def test_phase1_review_validation_requires_different_better_intent() -> None:
    row = _candidate("ctx", "uses")
    decision = _valid_decision(
        intent_correct="false",
        better_intent="uses",
        error_type="other",
        recommended_rule_action="other",
        evidence_supports_label="unclear",
        evidence_quote="",
    )

    with pytest.raises(ValueError, match="better_intent"):
        validate_phase1_review_decision(decision, row)


def test_phase1_review_pydantic_validation_catches_invalid_output() -> None:
    with pytest.raises(ValueError):
        Phase1LLMReviewDecision(
            intent_correct="maybe",
            better_intent="uses",
            object_type_correct="true",
            better_object_type="model",
            relation_subtype_correct="true",
            better_relation_subtype="direct_use",
            evidence_supports_label="true",
            evidence_quote="we use",
            should_send_to_llm_correct="true",
            better_llm_priority="high",
            cited_work_description_correct="true",
            error_type="none",
            recommended_rule_action="keep",
            confidence=0.5,
            rationale_short="bad enum",
        )


def test_phase1_cache_key_is_deterministic() -> None:
    row = _candidate("ctx", "uses")
    row["prompt_version"] = PHASE1_LLM_REVIEW_PROMPT_VERSION
    row["model"] = "fixture-model"

    assert phase1_llm_review_cache_key(row) == phase1_llm_review_cache_key(dict(row))
    changed = dict(row)
    changed["evidence_span"] = "we apply"
    assert phase1_llm_review_cache_key(row) != phase1_llm_review_cache_key(changed)


def test_phase1_report_generation_with_fake_outputs(tmp_path: Path) -> None:
    candidates = _fixture_candidates()
    sample = build_phase1_llm_review_sample(
        candidates=candidates,
        contexts=_fixture_contexts(candidates),
        limit=4,
        seed=42,
        model="fixture-model",
    )
    records = []
    for row in sample.to_dict("records"):
        decision = _valid_decision(
            intent_correct="false" if row["primary_candidate_intent"] == "uses" else "true",
            better_intent="background"
            if row["primary_candidate_intent"] == "uses"
            else row["primary_candidate_intent"],
            error_type=(
                "cited_work_description_misread_as_use"
                if row["primary_candidate_intent"] == "uses"
                else "none"
            ),
            recommended_rule_action=(
                "tighten_use_rule" if row["primary_candidate_intent"] == "uses" else "keep"
            ),
            evidence_quote=row["evidence_span"] or "",
            evidence_supports_label="unclear" if not row["evidence_span"] else "true",
            better_llm_priority=row["llm_priority"],
        )
        record = {**row, **decision.model_dump()}
        record["reviewer_confidence"] = record.pop("confidence")
        record["review_status"] = "reviewed"
        record["validation_error"] = ""
        record["attempts"] = 1
        record["from_cache"] = False
        record["model_used"] = "fixture-model"
        record["input_tokens"] = 1
        record["output_tokens"] = 1
        record["total_tokens"] = 2
        records.append(record)
    results = pd.DataFrame(records)
    results = results.reindex(columns=PHASE1_LLM_RESULT_COLUMNS)

    metrics = build_phase1_llm_review_metrics(sample=sample, results=results, dry_run=False)
    report = build_phase1_llm_review_report(
        sample=sample,
        results=results,
        metrics=metrics,
        sample_out=tmp_path / "sample.csv",
        jsonl_out=tmp_path / "results.jsonl",
        parquet_out=tmp_path / "results.parquet",
        dry_run=False,
    )
    recommendations = build_phase1_rule_recommendations(results, metrics, dry_run=False)

    assert "Estimated Precision By Primary Candidate Intent" in report
    assert "Recommended Rule Action" in report
    assert "tighten_use_rule" in recommendations
