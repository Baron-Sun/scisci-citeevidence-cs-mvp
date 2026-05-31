from __future__ import annotations

from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from citeevidence.cli import app
from citeevidence.object_policy import (
    apply_final_policy_to_mentions,
    apply_object_review_policy,
    build_object_graph_candidates,
)


def _mention(
    context_id: str,
    object_id: str,
    canonical_name: str,
    surface_form: str,
    sentence_text: str,
    *,
    object_type: str = "model",
    object_category: str = "named_object",
    confidence: float = 0.95,
    matched_in: str = "sentence_text",
    allow_in_object_graph: bool = True,
    match_policy: str = "standard",
) -> dict[str, object]:
    return {
        "context_id": context_id,
        "source_context_id": f"src_{context_id}",
        "citing_paper_id": "P00-0001",
        "resolved_cited_acl_id": "P00-0002",
        "resolved_cited_title": "Fixture cited title",
        "normalized_section": "method",
        "raw_section_name": "Method",
        "sentence_text": sentence_text,
        "context_window_s3": sentence_text,
        "object_id": object_id,
        "canonical_name": canonical_name,
        "object_type": object_type,
        "object_category": object_category,
        "surface_form": surface_form,
        "normalized_surface": surface_form.lower(),
        "match_type": "exact_alias",
        "char_start": 0,
        "char_end": len(surface_form),
        "confidence": confidence,
        "matched_in": matched_in,
        "match_policy": match_policy,
        "allow_in_object_graph": allow_in_object_graph,
        "provenance": f"registry_seed:{object_id};alias={surface_form}",
    }


def _empty_llm_review() -> pd.DataFrame:
    return pd.DataFrame(
        columns=[
            "context_id",
            "source_context_id",
            "object_id",
            "surface_form",
            "matched_in",
            "source_table",
            "review_status",
            "reviewer_correct",
            "surface_form_refers_to_object",
            "should_allow_in_object_graph",
            "should_use_as_phase1_feature",
            "error_type",
            "recommended_action",
            "evidence_quote",
            "rationale_short",
        ]
    )


def _apply(rows: list[dict[str, object]]) -> pd.DataFrame:
    return apply_final_policy_to_mentions(
        mentions=pd.DataFrame(rows),
        llm_review=_empty_llm_review(),
        source_table="object_mentions",
    )


def test_generic_metric_is_feature_only_and_excluded_from_graph_candidates() -> None:
    final = _apply(
        [
            _mention(
                "ctx_accuracy",
                "obj_accuracy",
                "accuracy",
                "accuracy",
                "We report accuracy.",
                object_type="metric",
                object_category="generic_metric",
                allow_in_object_graph=False,
            )
        ]
    )

    row = final.iloc[0]
    assert row["phase1_feature_eligible"]
    assert not row["graph_eligible"]
    assert row["graph_candidate_level"] == "none"
    assert build_object_graph_candidates(final).empty


def test_ptb_with_cue_is_graph_eligible_and_without_cue_is_not() -> None:
    final = _apply(
        [
            _mention(
                "ctx_ptb_cue",
                "obj_penn_treebank",
                "Penn Treebank",
                "PTB",
                "We train on Penn Treebank (PTB) sections 02-21.",
                object_type="dataset_or_database",
            ),
            _mention(
                "ctx_ptb_no_cue",
                "obj_penn_treebank",
                "Penn Treebank",
                "PTB",
                "We use PTB in preprocessing.",
                object_type="dataset_or_database",
            ),
        ]
    )

    cue = final.loc[final["context_id"].eq("ctx_ptb_cue")].iloc[0]
    no_cue = final.loc[final["context_id"].eq("ctx_ptb_no_cue")].iloc[0]
    assert cue["graph_eligible"]
    assert cue["object_category"] == "named_object"
    assert cue["graph_candidate_level"] == "strict"
    assert not no_cue["graph_eligible"]
    assert no_cue["object_category"] == "ambiguous_short_alias"


def test_transformer_case_policy() -> None:
    final = _apply(
        [
            _mention(
                "ctx_lower",
                "obj_transformer",
                "Transformer",
                "transformer",
                "The transformer layer is a generic component.",
                object_category="generic_architecture",
            ),
            _mention(
                "ctx_upper",
                "obj_transformer",
                "Transformer",
                "Transformer",
                "We use the Transformer model.",
            ),
        ]
    )

    lower = final.loc[final["context_id"].eq("ctx_lower")].iloc[0]
    upper = final.loc[final["context_id"].eq("ctx_upper")].iloc[0]
    assert not lower["graph_eligible"]
    assert lower["phase1_feature_eligible"]
    assert lower["object_category"] == "generic_architecture"
    assert upper["graph_eligible"]
    assert upper["graph_candidate_level"] == "strict"


def test_seq2seq_without_cue_is_downgraded() -> None:
    final = _apply(
        [
            _mention(
                "ctx_seq",
                "obj_seq2seq",
                "seq2seq",
                "seq2seq",
                "We add a baseline.",
            )
        ]
    )

    row = final.iloc[0]
    assert not row["graph_eligible"]
    assert row["confidence"] == 0.85
    assert "seq2seq_context_cue_missing" in row["policy_reason"]


def test_named_metric_bleu_is_graph_eligible_but_accuracy_is_not() -> None:
    final = _apply(
        [
            _mention(
                "ctx_bleu",
                "obj_bleu",
                "BLEU",
                "BLEU",
                "We optimize BLEU.",
                object_type="metric",
            ),
            _mention(
                "ctx_accuracy",
                "obj_accuracy",
                "accuracy",
                "accuracy",
                "We report accuracy.",
                object_type="metric",
                object_category="generic_metric",
                allow_in_object_graph=False,
            ),
        ]
    )

    bleu = final.loc[final["object_id"].eq("obj_bleu")].iloc[0]
    accuracy = final.loc[final["object_id"].eq("obj_accuracy")].iloc[0]
    assert bleu["graph_eligible"]
    assert bleu["graph_candidate_level"] == "strict"
    assert not accuracy["graph_eligible"]
    assert accuracy["phase1_feature_eligible"]


def test_resolved_cited_title_profiles_remain_separate_and_not_graph() -> None:
    title_profile = pd.DataFrame(
        [
            _mention(
                "ctx_title",
                "obj_bert",
                "BERT",
                "BERT",
                "No direct local object evidence.",
                matched_in="resolved_cited_title",
            ),
            _mention(
                "ctx_title_metric",
                "obj_bleu",
                "BLEU",
                "BLEU",
                "No direct local object evidence.",
                matched_in="resolved_cited_title",
                object_type="metric",
            )
        ]
    )

    final = apply_final_policy_to_mentions(
        mentions=title_profile,
        llm_review=_empty_llm_review(),
        source_table="cited_title_object_profiles",
        force_title_profile_policy=True,
    )

    assert set(final["matched_in"]) == {"resolved_cited_title"}
    assert not final["graph_eligible"].any()
    assert not final["phase1_feature_eligible"].any()
    assert set(final["graph_candidate_level"]) == {"none"}


def test_strict_candidates_sentence_only_and_broad_may_use_neighbor() -> None:
    final = _apply(
        [
            _mention("ctx_sentence", "obj_bert", "BERT", "BERT", "We use BERT."),
            _mention(
                "ctx_neighbor",
                "obj_bert",
                "BERT",
                "BERT",
                "The previous sentence mentioned BERT.",
                matched_in="context_window_neighbor",
                confidence=0.85,
            ),
        ]
    )

    candidates = build_object_graph_candidates(final)
    levels = dict(zip(candidates["context_id"], candidates["graph_candidate_level"], strict=True))
    assert levels["ctx_sentence"] == "strict"
    assert levels["ctx_neighbor"] == "broad"


def test_apply_review_policy_cli_outputs_reports(tmp_path: Path) -> None:
    mentions_path = tmp_path / "mentions.parquet"
    title_profiles_path = tmp_path / "title_profiles.parquet"
    llm_review_path = tmp_path / "llm_review.parquet"
    registry_path = tmp_path / "registry.yaml"
    out_mentions = tmp_path / "mentions_final.parquet"
    out_profiles = tmp_path / "profiles_final.parquet"
    out_graph = tmp_path / "graph.parquet"
    policy_report = tmp_path / "policy.md"
    report = tmp_path / "final.md"

    pd.DataFrame(
        [
            _mention("ctx_bleu", "obj_bleu", "BLEU", "BLEU", "We optimize BLEU."),
            _mention(
                "ctx_accuracy",
                "obj_accuracy",
                "accuracy",
                "accuracy",
                "We report accuracy.",
                object_type="metric",
                object_category="generic_metric",
                allow_in_object_graph=False,
            ),
        ]
    ).to_parquet(mentions_path, index=False)
    pd.DataFrame(
        [
            _mention(
                "ctx_title",
                "obj_bert",
                "BERT",
                "BERT",
                "No direct evidence.",
                matched_in="resolved_cited_title",
            )
        ]
    ).to_parquet(title_profiles_path, index=False)
    _empty_llm_review().to_parquet(llm_review_path, index=False)
    registry_path.write_text("objects: []\n", encoding="utf-8")

    metrics = apply_object_review_policy(
        object_mentions_path=mentions_path,
        cited_title_profiles_path=title_profiles_path,
        llm_review_path=llm_review_path,
        registry_path=registry_path,
        out_mentions=out_mentions,
        out_title_profiles=out_profiles,
        out_graph_candidates=out_graph,
        policy_report=policy_report,
        report=report,
    )

    assert metrics["strict_graph_candidate_count"] == 1
    assert out_mentions.exists()
    assert out_profiles.exists()
    assert out_graph.exists()
    assert "Generic Metrics Kept Feature-Only" in policy_report.read_text(encoding="utf-8")
    assert "Object Matching Sample Final Report" in report.read_text(encoding="utf-8")

    runner = CliRunner()
    cli_out_mentions = tmp_path / "cli_mentions.parquet"
    cli_out_profiles = tmp_path / "cli_profiles.parquet"
    cli_out_graph = tmp_path / "cli_graph.parquet"
    result = runner.invoke(
        app,
        [
            "objects",
            "apply-review-policy",
            "--object-mentions",
            str(mentions_path),
            "--cited-title-profiles",
            str(title_profiles_path),
            "--llm-review",
            str(llm_review_path),
            "--registry",
            str(registry_path),
            "--out-mentions",
            str(cli_out_mentions),
            "--out-title-profiles",
            str(cli_out_profiles),
            "--out-graph-candidates",
            str(cli_out_graph),
            "--policy-report",
            str(tmp_path / "cli_policy.md"),
            "--report",
            str(tmp_path / "cli_report.md"),
        ],
    )

    assert result.exit_code == 0
    assert "Graph candidates" in result.stdout
    assert cli_out_mentions.exists()
    assert cli_out_profiles.exists()
    assert cli_out_graph.exists()
