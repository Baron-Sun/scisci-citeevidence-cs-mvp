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
    *,
    refined_rules: bool = False,
    refined_rules_v2: bool = False,
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
        refined_rules=refined_rules,
        refined_rules_v2=refined_rules_v2,
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


def test_refined_described_task_is_cited_work_description_background(
    tmp_path: Path,
) -> None:
    frame = _run_phase1(
        tmp_path,
        [
            _context(
                "ctx_described",
                (
                    "Elsner and Charniak (2010) described the task as clustering "
                    "text using intrinsic information."
                ),
                normalized_section="introduction",
            )
        ],
        [],
        graph_mentions=[],
        refined_rules=True,
    )
    row = _row(frame, "ctx_described")
    assert row["primary_candidate_intent"] == "background"
    assert bool(row["cited_work_description"])
    assert "uses" not in row["candidate_intents"]


def test_refined_annotated_corpus_is_not_direct_use(tmp_path: Path) -> None:
    frame = _run_phase1(
        tmp_path,
        [
            _context(
                "ctx_annotated",
                "Carenini et al. (2008) annotated 39 email conversations from the Enron corpus.",
                normalized_section="introduction",
            )
        ],
        [],
        graph_mentions=[],
        refined_rules=True,
    )
    row = _row(frame, "ctx_annotated")
    assert row["primary_candidate_intent"] == "background"
    assert bool(row["cited_work_description"])
    assert "direct_use" not in row["candidate_relation_subtypes"]


def test_refined_we_use_and_our_model_uses_are_uses(tmp_path: Path) -> None:
    frame = _run_phase1(
        tmp_path,
        [
            _context("ctx_we_use", "We use BERT for tagging."),
            _context("ctx_our_model", "Our model uses BERT embeddings."),
        ],
        [_mention("ctx_we_use"), _mention("ctx_our_model")],
        refined_rules=True,
    )
    assert _row(frame, "ctx_we_use")["primary_candidate_intent"] == "uses"
    assert _row(frame, "ctx_our_model")["primary_candidate_intent"] == "uses"


def test_refined_using_without_current_subject_is_low_confidence(
    tmp_path: Path,
) -> None:
    frame = _run_phase1(
        tmp_path,
        [_context("ctx_using", "The task is solved using latent variables.")],
        [_mention("ctx_using")],
        graph_mentions=[],
        refined_rules=True,
    )
    row = _row(frame, "ctx_using")
    assert row["primary_candidate_intent"] == "unclear"
    assert row["confidence"] < 0.5
    assert row["llm_priority"] == "medium"


def test_refined_error_and_however_alone_do_not_trigger_critiques(
    tmp_path: Path,
) -> None:
    frame = _run_phase1(
        tmp_path,
        [
            _context("ctx_error_detection", "Error detection has been studied widely."),
            _context("ctx_alignment_error", "Alignment error rate is reported in prior work."),
            _context("ctx_however", "However, the task remains common."),
        ],
        [],
        graph_mentions=[],
        refined_rules=True,
    )
    assert _row(frame, "ctx_error_detection")["primary_candidate_intent"] != "critiques"
    assert _row(frame, "ctx_alignment_error")["primary_candidate_intent"] != "critiques"
    assert _row(frame, "ctx_however")["primary_candidate_intent"] != "critiques"


def test_refined_based_on_alone_does_not_trigger_compares_against(
    tmp_path: Path,
) -> None:
    frame = _run_phase1(
        tmp_path,
        [_context("ctx_based", "The tagger is based on BERT.")],
        [_mention("ctx_based")],
        refined_rules=True,
    )
    assert _row(frame, "ctx_based")["primary_candidate_intent"] != "compares_against"


def test_refined_explicit_compare_triggers_compares_against(tmp_path: Path) -> None:
    frame = _run_phase1(
        tmp_path,
        [_context("ctx_compare_refined", "We compared with BERT baselines.")],
        [_mention("ctx_compare_refined")],
        refined_rules=True,
    )
    row = _row(frame, "ctx_compare_refined")
    assert row["primary_candidate_intent"] == "compares_against"
    assert row["llm_priority"] == "high"


def test_refined_generic_metric_alone_is_not_compares_against(
    tmp_path: Path,
) -> None:
    frame = _run_phase1(
        tmp_path,
        [_context("ctx_metric_alone", "The paper reports F1.")],
        [
            _mention(
                "ctx_metric_alone",
                object_id="obj_f1",
                canonical_name="F1",
                object_type="metric",
                object_category="generic_metric",
                graph_eligible=False,
            )
        ],
        graph_mentions=[],
        refined_rules=True,
    )
    row = _row(frame, "ctx_metric_alone")
    assert row["primary_candidate_intent"] != "compares_against"
    assert "report_metric" not in row["candidate_relation_subtypes"]


def test_refined_generic_metric_with_compare_is_report_metric(
    tmp_path: Path,
) -> None:
    frame = _run_phase1(
        tmp_path,
        [_context("ctx_metric_compare", "Our system has better F1 than the baseline.")],
        [
            _mention(
                "ctx_metric_compare",
                object_id="obj_f1",
                canonical_name="F1",
                object_type="metric",
                object_category="generic_metric",
                graph_eligible=False,
            )
        ],
        graph_mentions=[],
        refined_rules=True,
    )
    row = _row(frame, "ctx_metric_compare")
    assert row["primary_candidate_intent"] == "compares_against"
    assert "report_metric" in row["candidate_relation_subtypes"]
    assert row["llm_priority"] == "high"


def test_refined_priority_controls_should_send_to_llm(tmp_path: Path) -> None:
    frame = _run_phase1(
        tmp_path,
        [
            _context(
                "ctx_low", "Previous work introduced BERT.", normalized_section="introduction"
            ),
            _context("ctx_none", "The task is common.", normalized_section="unknown"),
        ],
        [_mention("ctx_low")],
        graph_mentions=[],
        refined_rules=True,
    )
    low = _row(frame, "ctx_low")
    none = _row(frame, "ctx_none")
    assert low["llm_priority"] == "low"
    assert not bool(low["should_send_to_llm"])
    assert none["llm_priority"] == "none"
    assert not bool(none["should_send_to_llm"])
    for _, row in frame.iterrows():
        assert bool(row["should_send_to_llm"]) == (row["llm_priority"] in {"high", "medium"})


def test_refined_v2_applies_requires_current_paper_subject(tmp_path: Path) -> None:
    frame = _run_phase1(
        tmp_path,
        [
            _context("ctx_apply", "We apply BERT to biomedical tagging."),
            _context("ctx_task", "BERT is useful for the task of entity linking."),
        ],
        [_mention("ctx_apply"), _mention("ctx_task")],
        refined_rules_v2=True,
    )
    apply_row = _row(frame, "ctx_apply")
    task_row = _row(frame, "ctx_task")
    assert apply_row["primary_candidate_intent"] == "applies"
    assert "current_paper_apply_cue" in apply_row["matched_rules"]
    assert task_row["primary_candidate_intent"] != "applies"
    assert "weak_apply_context_feature" in task_row["matched_rules"]


def test_refined_v2_extends_requires_current_paper_subject(tmp_path: Path) -> None:
    frame = _run_phase1(
        tmp_path,
        [
            _context("ctx_extend", "We extend BERT with a discourse encoder."),
            _context("ctx_improving", "Improving BERT has been studied in prior work."),
        ],
        [_mention("ctx_extend"), _mention("ctx_improving")],
        refined_rules_v2=True,
    )
    extend_row = _row(frame, "ctx_extend")
    improving_row = _row(frame, "ctx_improving")
    assert extend_row["primary_candidate_intent"] == "extends"
    assert "current_paper_extend_cue" in extend_row["matched_rules"]
    assert improving_row["primary_candidate_intent"] != "extends"
    assert "weak_extend_context_feature" in improving_row["matched_rules"]


def test_refined_v2_uses_requires_current_paper_subject(tmp_path: Path) -> None:
    frame = _run_phase1(
        tmp_path,
        [
            _context("ctx_we_use", "We use BERT for tagging."),
            _context("ctx_previous", "Previous work used BERT for tagging."),
            _context("ctx_widely", "BERT is widely used for tagging."),
        ],
        [_mention("ctx_we_use"), _mention("ctx_previous"), _mention("ctx_widely")],
        refined_rules_v2=True,
    )
    assert _row(frame, "ctx_we_use")["primary_candidate_intent"] == "uses"
    assert _row(frame, "ctx_previous")["primary_candidate_intent"] == "background"
    assert _row(frame, "ctx_widely")["primary_candidate_intent"] != "uses"


def test_refined_v2_critique_requires_targeted_negative_relation(tmp_path: Path) -> None:
    frame = _run_phase1(
        tmp_path,
        [
            _context("ctx_error", "Error detection has been studied widely."),
            _context("ctx_however", "However, the task remains common."),
            _context("ctx_does_not", "This does not require supervision."),
            _context("ctx_target", "BERT fails to handle noisy mentions."),
        ],
        [_mention("ctx_target")],
        refined_rules_v2=True,
    )
    assert _row(frame, "ctx_error")["primary_candidate_intent"] != "critiques"
    assert _row(frame, "ctx_however")["primary_candidate_intent"] != "critiques"
    assert _row(frame, "ctx_does_not")["primary_candidate_intent"] != "critiques"
    assert _row(frame, "ctx_target")["primary_candidate_intent"] == "critiques"


def test_refined_v2_metric_alone_does_not_trigger_compare(tmp_path: Path) -> None:
    frame = _run_phase1(
        tmp_path,
        [
            _context("ctx_metric", "The paper reports BLEU."),
            _context("ctx_compare", "Our system has better BLEU than the baseline."),
        ],
        [
            _mention(
                "ctx_metric",
                object_id="obj_bleu",
                canonical_name="BLEU",
                object_type="metric",
                object_category="generic_metric",
                graph_eligible=False,
            ),
            _mention(
                "ctx_compare",
                object_id="obj_bleu",
                canonical_name="BLEU",
                object_type="metric",
                object_category="generic_metric",
                graph_eligible=False,
            ),
        ],
        graph_mentions=[],
        refined_rules_v2=True,
    )
    metric_row = _row(frame, "ctx_metric")
    compare_row = _row(frame, "ctx_compare")
    assert metric_row["primary_candidate_intent"] != "compares_against"
    assert metric_row["object_type_source"] == "generic_metric_feature"
    assert compare_row["primary_candidate_intent"] == "compares_against"
    assert "report_metric" in compare_row["candidate_relation_subtypes"]


def test_refined_v2_object_type_source_assignment(tmp_path: Path) -> None:
    contexts = [
        _context("ctx_graph", "We use BERT."),
        _context("ctx_direct", "We use the parser."),
        _context("ctx_metric", "The paper reports F1."),
        _context("ctx_title", "Previous work introduced alignment."),
        _context("ctx_none", "The task is common."),
    ]
    mentions = [
        _mention("ctx_graph"),
        _mention(
            "ctx_direct",
            object_id="obj_parser",
            canonical_name="parser",
            object_type="method",
        ),
        _mention(
            "ctx_metric",
            object_id="obj_f1",
            canonical_name="F1",
            object_type="metric",
            object_category="generic_metric",
            graph_eligible=False,
        ),
    ]
    contexts_path, mentions_path, graph_path, title_profiles_path = _write_inputs(
        tmp_path,
        contexts,
        mentions,
        graph_mentions=[_mention("ctx_graph")],
    )
    pd.DataFrame(
        [
            _mention(
                "ctx_title",
                object_id="obj_align",
                canonical_name="alignment",
                object_type="method",
            )
        ],
        columns=OBJECT_COLUMNS,
    ).to_parquet(title_profiles_path, index=False)
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
        refined_rules_v2=True,
    )
    frame = pd.read_parquet(out_candidates)
    assert _row(frame, "ctx_graph")["object_type_source"] == "object_graph_candidate"
    assert _row(frame, "ctx_direct")["object_type_source"] == "object_mention"
    assert _row(frame, "ctx_metric")["object_type_source"] == "generic_metric_feature"
    assert _row(frame, "ctx_title")["object_type_source"] == "cited_title_profile"
    assert _row(frame, "ctx_none")["object_type_source"] == "none"


def test_refined_v2_high_priority_is_strict_and_evidence_uses_current_cue(
    tmp_path: Path,
) -> None:
    frame = _run_phase1(
        tmp_path,
        [
            _context("ctx_high", "We use BERT for tagging."),
            _context("ctx_weak", "The task is solved using BERT."),
        ],
        [_mention("ctx_high"), _mention("ctx_weak")],
        graph_mentions=[_mention("ctx_high")],
        refined_rules_v2=True,
    )
    high = _row(frame, "ctx_high")
    weak = _row(frame, "ctx_weak")
    assert high["llm_priority"] == "high"
    assert high["should_send_to_llm"]
    assert "we use" in high["evidence_span"].lower()
    assert weak["llm_priority"] != "high"


def test_refined_v2_full_mode_writes_llm_queues_and_report(tmp_path: Path) -> None:
    contexts = [
        _context("ctx_use", "We use BERT for tagging."),
        _context("ctx_compare", "We compare against BERT as a baseline."),
        _context("ctx_bg_graph", "Previous work introduced BERT."),
        _context("ctx_metric", "Our model has better F1 than the baseline."),
        _context("ctx_unclear", "BERT representations are included."),
    ]
    mentions = [
        _mention("ctx_use"),
        _mention("ctx_compare"),
        _mention("ctx_bg_graph"),
        _mention(
            "ctx_metric",
            object_id="obj_f1",
            canonical_name="F1",
            object_type="metric",
            object_category="generic_metric",
            graph_eligible=False,
        ),
        _mention("ctx_unclear"),
    ]
    contexts_path, mentions_path, graph_path, title_profiles_path = _write_inputs(
        tmp_path,
        contexts,
        mentions,
        graph_mentions=[
            _mention("ctx_use"),
            _mention("ctx_compare"),
            _mention("ctx_bg_graph"),
        ],
    )
    out_candidates = tmp_path / "full_candidates.parquet"
    out_features = tmp_path / "full_features.parquet"
    out_high = tmp_path / "queue_high.parquet"
    out_medium = tmp_path / "queue_medium.parquet"
    out_sample = tmp_path / "queue_sample.parquet"
    report = tmp_path / "full_report.md"

    metrics = screen_phase1_citation_functions(
        contexts_path=contexts_path,
        object_mentions_path=mentions_path,
        object_graph_candidates_path=graph_path,
        cited_title_profiles_path=title_profiles_path,
        out_candidates_path=out_candidates,
        out_features_path=out_features,
        out_llm_high_path=out_high,
        out_llm_medium_path=out_medium,
        out_llm_sample_path=out_sample,
        report_path=report,
        limit=None,
        seed=42,
        refined_rules_v2=True,
    )

    candidates = pd.read_parquet(out_candidates)
    high = pd.read_parquet(out_high)
    medium = pd.read_parquet(out_medium)
    sample = pd.read_parquet(out_sample)
    text = report.read_text(encoding="utf-8")
    assert metrics["configured_limit"] == "full"
    assert candidates.shape[0] == len(contexts)
    assert not high.empty
    assert set(high["llm_priority"]) == {"high"}
    assert set(medium["llm_priority"]).issubset({"medium"})
    assert sample.shape[0] == high.shape[0] + medium.shape[0]
    assert "## LLM Queue Stats" in text
    assert "## Evidence Span Support Sanity Checks" in text


def test_refined_v2_object_source_quality_checks(tmp_path: Path) -> None:
    frame = _run_phase1(
        tmp_path,
        [
            _context("ctx_none", "The task is common."),
            _context("ctx_metric", "The paper reports F1."),
            _context("ctx_title", "Previous work introduced alignment."),
        ],
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
        refined_rules_v2=True,
    )
    none = _row(frame, "ctx_none")
    metric = _row(frame, "ctx_metric")
    assert none["object_type_source"] == "none"
    assert none["primary_candidate_object_type"] == "unknown"
    assert metric["object_type_source"] == "generic_metric_feature"
    assert not bool(metric["has_graph_candidate_object"])
