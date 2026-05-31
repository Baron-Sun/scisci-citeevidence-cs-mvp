from __future__ import annotations

from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from citeevidence.cli import app
from citeevidence.phase1 import OBJECT_COLUMNS, screen_phase1_citation_functions


def _context(
    context_id: str,
    sentence_text: str,
    *,
    normalized_section: str = "method",
) -> dict[str, object]:
    return {
        "context_id": context_id,
        "source_context_id": f"src_{context_id}",
        "citing_paper_id": "P00-0001",
        "resolved_cited_acl_id": "P00-0002",
        "resolved_cited_title": "A BERT Paper",
        "normalized_section": normalized_section,
        "raw_section_name": normalized_section.title(),
        "citation_marker": "(Devlin et al., 2019)",
        "sentence_text": sentence_text,
        "context_window_s3": sentence_text,
    }


def _mention(
    context_id: str,
    object_id: str = "obj_bert",
    canonical_name: str = "BERT",
    object_type: str = "model",
    object_category: str = "named_object",
    *,
    graph_eligible: bool = True,
) -> dict[str, object]:
    return {
        "context_id": context_id,
        "object_id": object_id,
        "canonical_name": canonical_name,
        "object_type": object_type,
        "object_category": object_category,
        "graph_eligible": graph_eligible,
        "phase1_feature_eligible": True,
    }


def _write_inputs(
    tmp_path: Path,
    contexts: list[dict[str, object]],
    mentions: list[dict[str, object]],
    graph_mentions: list[dict[str, object]] | None = None,
) -> tuple[Path, Path, Path, Path]:
    contexts_path = tmp_path / "contexts.parquet"
    mentions_path = tmp_path / "mentions.parquet"
    graph_path = tmp_path / "graph.parquet"
    title_profiles_path = tmp_path / "title_profiles.parquet"
    pd.DataFrame(contexts).to_parquet(contexts_path, index=False)
    pd.DataFrame(mentions, columns=OBJECT_COLUMNS).to_parquet(mentions_path, index=False)
    pd.DataFrame(
        graph_mentions if graph_mentions is not None else mentions, columns=OBJECT_COLUMNS
    ).to_parquet(
        graph_path,
        index=False,
    )
    pd.DataFrame([], columns=OBJECT_COLUMNS).to_parquet(title_profiles_path, index=False)
    return contexts_path, mentions_path, graph_path, title_profiles_path


def _run_phase1(
    tmp_path: Path,
    contexts: list[dict[str, object]],
    mentions: list[dict[str, object]],
    graph_mentions: list[dict[str, object]] | None = None,
) -> pd.DataFrame:
    contexts_path, mentions_path, graph_path, title_profiles_path = _write_inputs(
        tmp_path,
        contexts,
        mentions,
        graph_mentions,
    )
    out_candidates = tmp_path / "candidates.parquet"
    out_features = tmp_path / "features.parquet"
    report = tmp_path / "report.md"
    screen_phase1_citation_functions(
        contexts_path=contexts_path,
        object_mentions_path=mentions_path,
        object_graph_candidates_path=graph_path,
        cited_title_profiles_path=title_profiles_path,
        out_candidates_path=out_candidates,
        out_features_path=out_features,
        report_path=report,
        limit=100,
        seed=42,
    )
    assert out_features.exists()
    assert "## Core Counts" in report.read_text(encoding="utf-8")
    return pd.read_parquet(out_candidates)


def _row(frame: pd.DataFrame, context_id: str) -> pd.Series:
    return frame.loc[frame["context_id"].eq(context_id)].iloc[0]


def test_use_cue_produces_uses(tmp_path: Path) -> None:
    frame = _run_phase1(
        tmp_path,
        [_context("ctx_use", "We use BERT for tagging.")],
        [_mention("ctx_use")],
    )
    row = _row(frame, "ctx_use")
    assert row["primary_candidate_intent"] == "uses"
    assert "direct_use" in row["candidate_relation_subtypes"]
    assert row["evidence_span"] in row["sentence_text"]


def test_compare_cue_produces_compares_against(tmp_path: Path) -> None:
    frame = _run_phase1(
        tmp_path,
        [_context("ctx_compare", "We compare against BERT as a baseline.")],
        [_mention("ctx_compare")],
    )
    assert _row(frame, "ctx_compare")["primary_candidate_intent"] == "compares_against"


def test_extend_cue_produces_extends(tmp_path: Path) -> None:
    frame = _run_phase1(
        tmp_path,
        [_context("ctx_extend", "We extend BERT with a task adapter.")],
        [_mention("ctx_extend")],
    )
    assert _row(frame, "ctx_extend")["primary_candidate_intent"] == "extends"


def test_critique_cue_produces_critiques(tmp_path: Path) -> None:
    frame = _run_phase1(
        tmp_path,
        [_context("ctx_critique", "BERT fails to handle noisy mentions.")],
        [_mention("ctx_critique")],
    )
    assert _row(frame, "ctx_critique")["primary_candidate_intent"] == "critiques"


def test_apply_cue_produces_applies(tmp_path: Path) -> None:
    frame = _run_phase1(
        tmp_path,
        [_context("ctx_apply", "We apply BERT to classify tweets.")],
        [_mention("ctx_apply")],
    )
    row = _row(frame, "ctx_apply")
    assert row["primary_candidate_intent"] == "applies"
    assert "direct_use" in row["candidate_relation_subtypes"]


def test_background_cue_produces_background(tmp_path: Path) -> None:
    frame = _run_phase1(
        tmp_path,
        [_context("ctx_background", "Previous work introduced BERT.")],
        [_mention("ctx_background")],
    )
    assert _row(frame, "ctx_background")["primary_candidate_intent"] == "background"


def test_non_background_cues_override_background_cues(tmp_path: Path) -> None:
    frame = _run_phase1(
        tmp_path,
        [_context("ctx_override", "Previous work introduced BERT, and we use it here.")],
        [_mention("ctx_override")],
    )
    row = _row(frame, "ctx_override")
    assert "background" in row["candidate_intents"]
    assert row["primary_candidate_intent"] == "uses"


def test_generic_metric_compare_cue_produces_report_metric(tmp_path: Path) -> None:
    frame = _run_phase1(
        tmp_path,
        [_context("ctx_metric", "Our model achieves better F1 than the baseline.")],
        [
            _mention(
                "ctx_metric",
                object_id="obj_f1",
                canonical_name="F1",
                object_type="metric",
                object_category="generic_metric",
                graph_eligible=False,
            )
        ],
        graph_mentions=[],
    )
    row = _row(frame, "ctx_metric")
    assert row["primary_candidate_intent"] == "compares_against"
    assert "report_metric" in row["candidate_relation_subtypes"]


def test_object_mention_without_cue_is_low_confidence_and_may_send_to_llm(
    tmp_path: Path,
) -> None:
    frame = _run_phase1(
        tmp_path,
        [_context("ctx_object_only", "BERT representations are included.")],
        [_mention("ctx_object_only")],
    )
    row = _row(frame, "ctx_object_only")
    assert row["primary_candidate_intent"] == "unclear"
    assert row["confidence"] < 0.5
    assert bool(row["should_send_to_llm"])


def test_section_prior_alone_is_low_confidence_and_not_llm(tmp_path: Path) -> None:
    frame = _run_phase1(
        tmp_path,
        [_context("ctx_intro", "This paper studies dialogue.", normalized_section="introduction")],
        [],
        graph_mentions=[],
    )
    row = _row(frame, "ctx_intro")
    assert row["primary_candidate_intent"] == "background"
    assert row["confidence"] < 0.5
    assert not bool(row["should_send_to_llm"])


def test_no_cues_and_no_object_is_unclear_not_llm(tmp_path: Path) -> None:
    frame = _run_phase1(
        tmp_path,
        [_context("ctx_none", "This paper studies dialogue.", normalized_section="unknown")],
        [],
        graph_mentions=[],
    )
    row = _row(frame, "ctx_none")
    assert row["primary_candidate_intent"] == "unclear"
    assert not bool(row["should_send_to_llm"])


def test_phase1_cli_screen_command_runs(tmp_path: Path) -> None:
    contexts_path, mentions_path, graph_path, title_profiles_path = _write_inputs(
        tmp_path,
        [_context("ctx_cli", "We use BERT.")],
        [_mention("ctx_cli")],
    )
    out_candidates = tmp_path / "cli_candidates.parquet"
    out_features = tmp_path / "cli_features.parquet"
    report = tmp_path / "cli_report.md"

    result = CliRunner().invoke(
        app,
        [
            "phase1",
            "screen",
            "--contexts",
            str(contexts_path),
            "--object-mentions",
            str(mentions_path),
            "--object-graph-candidates",
            str(graph_path),
            "--cited-title-profiles",
            str(title_profiles_path),
            "--out-candidates",
            str(out_candidates),
            "--out-features",
            str(out_features),
            "--report",
            str(report),
            "--limit",
            "10",
        ],
    )

    assert result.exit_code == 0
    assert pd.read_parquet(out_candidates).shape[0] == 1
    assert report.exists()
