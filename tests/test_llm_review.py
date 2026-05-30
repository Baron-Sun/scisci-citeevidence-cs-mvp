from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest
from pydantic import ValidationError
from typer.testing import CliRunner

from citeevidence.cli import app
from citeevidence.llm_review import (
    LLM_OBJECT_REVIEW_PROMPT_VERSION,
    LLMObjectReviewDecision,
    build_llm_object_review_sample,
    build_llm_review_metrics,
    build_llm_review_report,
    build_object_review_prompt,
    llm_object_review_cache_key,
    validate_review_decision,
)
from citeevidence.objects import ObjectRegistryEntry


def _context_row(context_id: str, sentence_text: str, context_window_s3: str | None = None) -> dict:
    return {
        "context_id": context_id,
        "source_context_id": f"src_{context_id}",
        "citing_paper_id": "P00-0001",
        "resolved_cited_acl_id": "P00-0002",
        "resolved_cited_title": "BERT: Pre-training of Deep Bidirectional Transformers",
        "normalized_section": "method",
        "raw_section_name": "Method",
        "sentence_text": sentence_text,
        "context_window_s3": context_window_s3 or sentence_text,
    }


def _mention_row(
    context_id: str,
    canonical_name: str,
    surface_form: str,
    *,
    object_id: str = "obj_bert",
    object_type: str = "model",
    object_category: str = "named_object",
    confidence: float = 0.95,
    matched_in: str = "sentence_text",
    allow_in_object_graph: bool = True,
) -> dict:
    return {
        **_context_row(context_id, f"We use {surface_form} for tagging."),
        "object_id": object_id,
        "canonical_name": canonical_name,
        "object_type": object_type,
        "object_category": object_category,
        "surface_form": surface_form,
        "normalized_surface": surface_form.lower(),
        "match_type": "exact_alias",
        "char_start": 7,
        "char_end": 7 + len(surface_form),
        "confidence": confidence,
        "matched_in": matched_in,
        "match_policy": "fixture",
        "allow_in_object_graph": allow_in_object_graph,
        "provenance": f"registry_seed:{object_id};alias={surface_form}",
    }


def _registry_entries() -> list[ObjectRegistryEntry]:
    return [
        ObjectRegistryEntry(
            object_id="obj_bert",
            canonical_name="BERT",
            aliases=("BERT",),
            negative_aliases=(),
            object_type="model",
            linked_paper_title=None,
            linked_acl_id=None,
            linked_doi=None,
            source="fixture",
            notes="fixture BERT object",
        ),
        ObjectRegistryEntry(
            object_id="obj_accuracy",
            canonical_name="accuracy",
            aliases=("accuracy",),
            negative_aliases=(),
            object_type="metric",
            linked_paper_title=None,
            linked_acl_id=None,
            linked_doi=None,
            source="fixture",
            notes="generic metric",
            object_category="generic_metric",
            allow_in_object_graph=False,
        ),
    ]


def _write_fixture_inputs(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    object_mentions_path = tmp_path / "object_mentions.parquet"
    title_profiles_path = tmp_path / "title_profiles.parquet"
    contexts_path = tmp_path / "contexts.parquet"
    registry_path = tmp_path / "registry.yaml"

    mentions = pd.DataFrame(
        [
            _mention_row("ctx_named", "BERT", "BERT"),
            _mention_row(
                "ctx_metric",
                "accuracy",
                "accuracy",
                object_id="obj_accuracy",
                object_type="metric",
                object_category="generic_metric",
                confidence=0.7,
                allow_in_object_graph=False,
            ),
            _mention_row(
                "ctx_ptb",
                "Penn Treebank",
                "PTB",
                object_id="obj_ptb",
                object_type="dataset_or_database",
                object_category="ambiguous_short_alias",
                confidence=0.5,
                allow_in_object_graph=False,
            ),
            _mention_row(
                "ctx_transformer",
                "Transformer",
                "transformer",
                object_id="obj_transformer",
                object_category="generic_architecture",
                confidence=0.65,
                allow_in_object_graph=False,
            ),
            {
                **_mention_row(
                    "ctx_neighbor",
                    "BERT",
                    "BERT",
                    matched_in="context_window_neighbor",
                    confidence=0.85,
                ),
                "sentence_text": "This sentence cites prior work.",
                "context_window_s3": "Earlier BERT baseline. This sentence cites prior work.",
            },
        ]
    )
    profiles = pd.DataFrame(
        [
            {
                **_mention_row("ctx_title", "BERT", "BERT", matched_in="resolved_cited_title"),
                "sentence_text": "This sentence has no local object mention.",
            }
        ]
    )
    contexts = pd.DataFrame(
        [
            _context_row("ctx_named", "We use BERT for tagging."),
            _context_row("ctx_metric", "We report accuracy and F1."),
            _context_row("ctx_ptb", "We use PTB in preprocessing."),
            _context_row("ctx_transformer", "The transformer layer is generic."),
            _context_row(
                "ctx_neighbor",
                "This sentence cites prior work.",
                "Earlier BERT baseline. This sentence cites prior work.",
            ),
            _context_row("ctx_title", "This sentence has no local object mention."),
        ]
    )
    mentions.to_parquet(object_mentions_path, index=False)
    profiles.to_parquet(title_profiles_path, index=False)
    contexts.to_parquet(contexts_path, index=False)
    registry_path.write_text(
        """
objects:
  - object_id: obj_bert
    canonical_name: BERT
    aliases: [BERT]
    negative_aliases: []
    object_type: model
    linked_paper_title:
    linked_acl_id:
    linked_doi:
    source: fixture
    notes: fixture BERT object
    allow_short_alias: false
  - object_id: obj_accuracy
    canonical_name: accuracy
    aliases: [accuracy]
    negative_aliases: []
    object_type: metric
    linked_paper_title:
    linked_acl_id:
    linked_doi:
    source: fixture
    notes: generic metric
    object_category: generic_metric
    allow_in_object_graph: false
    allow_short_alias: false
""",
        encoding="utf-8",
    )
    return object_mentions_path, title_profiles_path, contexts_path, registry_path


def test_llm_objects_dry_run_cli_creates_sample_and_prompts(tmp_path: Path) -> None:
    object_mentions_path, title_profiles_path, contexts_path, registry_path = _write_fixture_inputs(
        tmp_path
    )
    sample_out = tmp_path / "sample.csv"
    jsonl_out = tmp_path / "results.jsonl"
    parquet_out = tmp_path / "results.parquet"
    report = tmp_path / "report.md"
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "review",
            "llm-objects",
            "--object-mentions",
            str(object_mentions_path),
            "--cited-title-profiles",
            str(title_profiles_path),
            "--contexts",
            str(contexts_path),
            "--registry",
            str(registry_path),
            "--sample-out",
            str(sample_out),
            "--jsonl-out",
            str(jsonl_out),
            "--parquet-out",
            str(parquet_out),
            "--report",
            str(report),
            "--limit",
            "6",
            "--dry-run",
        ],
    )

    assert result.exit_code == 0
    sample = pd.read_csv(sample_out)
    assert sample.shape[0] == 6
    prompt_records = [json.loads(line) for line in jsonl_out.read_text().splitlines()]
    assert len(prompt_records) == 6
    assert prompt_records[0]["dry_run"] is True
    assert "LLM-assisted validation" in report.read_text(encoding="utf-8")
    assert pd.read_parquet(parquet_out).empty


def test_cache_key_is_deterministic_and_model_sensitive() -> None:
    row = {
        "context_id": "ctx",
        "object_id": "obj_bert",
        "surface_form": "BERT",
        "matched_in": "sentence_text",
        "prompt_version": LLM_OBJECT_REVIEW_PROMPT_VERSION,
        "model": "model-a",
    }

    assert llm_object_review_cache_key(row) == llm_object_review_cache_key(dict(row))
    other = dict(row)
    other["model"] = "model-b"
    assert llm_object_review_cache_key(row) != llm_object_review_cache_key(other)


def test_decision_schema_rejects_false_without_error_type() -> None:
    with pytest.raises(ValidationError):
        LLMObjectReviewDecision(
            reviewer_correct="false",
            object_type_correct="true",
            surface_form_refers_to_object="true",
            should_allow_in_object_graph=True,
            should_use_as_phase1_feature=True,
            error_type="none",
            recommended_action="keep",
            confidence=0.8,
            evidence_quote="BERT",
            rationale_short="bad fixture",
        )


def test_invalid_evidence_quote_is_caught() -> None:
    decision = LLMObjectReviewDecision(
        reviewer_correct="true",
        object_type_correct="true",
        surface_form_refers_to_object="true",
        should_allow_in_object_graph=True,
        should_use_as_phase1_feature=True,
        error_type="none",
        recommended_action="keep",
        confidence=0.9,
        evidence_quote="not in text",
        rationale_short="fixture",
    )

    with pytest.raises(ValueError, match="evidence_quote"):
        validate_review_decision(decision, _mention_row("ctx", "BERT", "BERT"))


def test_generic_metric_policy_is_in_prompt_and_validation() -> None:
    row = _mention_row(
        "ctx_metric",
        "accuracy",
        "accuracy",
        object_id="obj_accuracy",
        object_type="metric",
        object_category="generic_metric",
        allow_in_object_graph=False,
    )
    _, user_prompt = build_object_review_prompt(row)
    assert "generic_metric" in user_prompt
    assert "should_use_as_phase1_feature=true" in user_prompt

    decision = LLMObjectReviewDecision(
        reviewer_correct="true",
        object_type_correct="true",
        surface_form_refers_to_object="true",
        should_allow_in_object_graph=True,
        should_use_as_phase1_feature=True,
        error_type="none",
        recommended_action="keep",
        confidence=0.9,
        evidence_quote="accuracy",
        rationale_short="fixture",
    )
    with pytest.raises(ValueError, match="generic_metric"):
        validate_review_decision(decision, row)


def test_resolved_cited_title_profile_is_not_graph_object_by_default() -> None:
    object_mentions = pd.DataFrame([_mention_row("ctx_named", "BERT", "BERT")])
    profiles = pd.DataFrame(
        [
            {
                **_mention_row(
                    "ctx_title",
                    "BERT",
                    "BERT",
                    matched_in="resolved_cited_title",
                ),
                "sentence_text": "No local object mention here.",
                "context_window_s3": "No local object mention here.",
            }
        ]
    )
    contexts = pd.DataFrame(
        [
            _context_row("ctx_named", "We use BERT."),
            _context_row("ctx_title", "No local object mention here."),
        ]
    )

    sample = build_llm_object_review_sample(
        object_mentions=object_mentions,
        cited_title_profiles=profiles,
        contexts=contexts,
        registry=_registry_entries(),
        limit=10,
        seed=1,
        model="fixture-model",
    )

    title_rows = sample.loc[sample["matched_in"].eq("resolved_cited_title")]
    assert not title_rows.empty
    assert not bool(title_rows.iloc[0]["allow_in_object_graph"])

    decision = LLMObjectReviewDecision(
        reviewer_correct="true",
        object_type_correct="true",
        surface_form_refers_to_object="true",
        should_allow_in_object_graph=True,
        should_use_as_phase1_feature=True,
        error_type="none",
        recommended_action="keep",
        confidence=0.9,
        evidence_quote="BERT",
        rationale_short="fixture",
    )
    with pytest.raises(ValueError, match="resolved_cited_title"):
        validate_review_decision(decision, title_rows.iloc[0].to_dict())


def test_report_generation_with_fake_llm_outputs(tmp_path: Path) -> None:
    sample = pd.DataFrame([_mention_row("ctx", "BERT", "BERT")])
    sample["review_bucket"] = "named_object_high_confidence"
    sample["source_table"] = "object_mentions"
    sample["sample_row_id"] = "llm_obj_review_0001"
    sample["registry_notes"] = "fixture"
    sample["registry_aliases"] = "BERT"
    sample["registry_negative_aliases"] = ""
    sample["registry_require_context_cue"] = ""
    sample["prompt_version"] = LLM_OBJECT_REVIEW_PROMPT_VERSION
    sample["model"] = "fixture-model"
    sample["cache_key"] = sample.apply(
        lambda row: llm_object_review_cache_key(row.to_dict()),
        axis=1,
    )
    results = sample.copy()
    results["reviewer_correct"] = "false"
    results["object_type_correct"] = "true"
    results["surface_form_refers_to_object"] = "false"
    results["should_allow_in_object_graph"] = False
    results["should_use_as_phase1_feature"] = True
    results["error_type"] = "matched_unrelated_word"
    results["recommended_action"] = "block_alias"
    results["llm_confidence"] = 0.8
    results["evidence_quote"] = "BERT"
    results["rationale_short"] = "Fixture false positive."
    results["review_status"] = "reviewed"
    results["validation_error"] = ""
    results["attempts"] = 1
    results["from_cache"] = False
    results["model_used"] = "fixture-model"
    results["input_tokens"] = 10
    results["output_tokens"] = 5
    results["total_tokens"] = 15

    metrics = build_llm_review_metrics(sample=sample, results=results, dry_run=False)
    report = build_llm_review_report(
        sample=sample,
        results=results,
        metrics=metrics,
        sample_out=tmp_path / "sample.csv",
        jsonl_out=tmp_path / "results.jsonl",
        parquet_out=tmp_path / "results.parquet",
        dry_run=False,
    )

    assert "Object Mentions LLM-as-Judge Review Report" in report
    assert "Registry Refinement Recommendations" in report
    assert "matched_unrelated_word" in report
