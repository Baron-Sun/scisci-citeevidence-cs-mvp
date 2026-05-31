from __future__ import annotations

import inspect
from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from citeevidence.cli import app
from citeevidence.final_release.metrics import build_critique_evidence_cards
from citeevidence.final_release.report import validate_final_release_report_text
from citeevidence.final_release.runner import run_final_release_analysis


def test_runner_writes_bounded_report_sources_figures_and_samples(tmp_path: Path) -> None:
    paths = _write_fixture_inputs(tmp_path)
    outputs = _run_fixture_runner(tmp_path, paths)

    report = tmp_path / "reports" / "final_scisci_results_report_release.md"
    evidence_cards = tmp_path / "data" / "final_release_evidence_cards.csv"
    qa_sample = tmp_path / "data" / "final_release_qa_sample.csv"

    assert outputs["figure_count"] == 4
    assert outputs["source_csv_count"] == 7
    assert report.exists()
    assert evidence_cards.exists()
    assert qa_sample.exists()
    assert not pd.read_csv(evidence_cards).empty
    assert not pd.read_csv(qa_sample).empty

    for name in [
        "qa_summary.csv",
        "confidence_by_intent.csv",
        "failure_categories.csv",
        "section_function_lift.csv",
        "object_role_signatures.csv",
        "ranking_reversal.csv",
        "critique_bottleneck_matrix.csv",
    ]:
        assert (tmp_path / "figures" / "source_data" / name).exists()

    for name in [
        "f02_section_function_lift",
        "f03_object_role_signature_map",
        "f04_context_volume_vs_evidence_use_reversal",
        "f05_critique_bottleneck_heatmap",
    ]:
        assert (tmp_path / "figures" / f"{name}.png").exists()
        assert (tmp_path / "figures" / f"{name}.svg").exists()


def test_runner_enriches_qa_sample_with_object_risk_columns(tmp_path: Path) -> None:
    paths = _write_fixture_inputs(tmp_path)
    _run_fixture_runner(tmp_path, paths)

    sample = pd.read_csv(tmp_path / "data" / "final_release_qa_sample.csv")
    shortfall = " ".join(sample["sample_shortfall"].dropna().astype(str))

    assert {"object_count", "object_candidate_rank", "matched_in"}.issubset(sample.columns)
    assert "missing risk columns" not in shortfall
    assert "multi_object_or_policy_risk" in set(sample["sample_stratum"])


def test_runner_writes_deduplicated_evidence_cards(tmp_path: Path) -> None:
    paths = _write_fixture_inputs(tmp_path)
    _run_fixture_runner(tmp_path, paths)

    cards = pd.read_csv(tmp_path / "data" / "final_release_evidence_cards.csv")
    key = ["bottleneck_family", "object_name", "object_type", "evidence_span"]

    assert not cards.duplicated(key).any()


def test_runner_report_passes_final_release_guardrails(tmp_path: Path) -> None:
    paths = _write_fixture_inputs(tmp_path)
    _run_fixture_runner(tmp_path, paths)

    report_text = (tmp_path / "reports" / "final_scisci_results_report_release.md").read_text(
        encoding="utf-8"
    )

    assert validate_final_release_report_text(report_text) == []
    assert "full high/medium Phase-1 queue, not all strong contexts" in report_text
    assert "LLM-assisted, schema-validated, evidence-grounded labels" in report_text
    assert "seed-registry object-use graph" in report_text
    assert "citation-context volume" in report_text
    assert "citation count" not in report_text.casefold()
    assert "citation volume" not in report_text.casefold()


def test_runner_ranking_source_excludes_one_context_tail_artifacts(
    tmp_path: Path,
) -> None:
    paths = _write_fixture_inputs(tmp_path)
    _run_fixture_runner(tmp_path, paths)

    ranking = pd.read_csv(tmp_path / "figures" / "source_data" / "ranking_reversal.csv")

    assert "One Context Tail" not in set(ranking["resolved_cited_title"])
    assert ranking["total_strong_contexts"].ge(20).all()
    assert ranking["evidence_use_count"].ge(5).all()


def test_final_release_cli_help_is_registered() -> None:
    runner = CliRunner()
    analysis_help = runner.invoke(app, ["analysis", "--help"])
    result = runner.invoke(app, ["analysis", "final-release", "--help"])

    assert analysis_help.exit_code == 0
    assert "final-release" in analysis_help.stdout
    assert result.exit_code == 0
    assert "--phase2" in result.stdout
    assert "--out-qa-sample" in result.stdout
    assert "--min-ranking-total-contexts" in result.stdout


def test_runner_raises_clear_error_for_missing_required_input(tmp_path: Path) -> None:
    paths = _write_fixture_inputs(tmp_path)
    missing = tmp_path / "missing_phase2.parquet"

    try:
        _run_fixture_runner(tmp_path, {**paths, "phase2": missing})
    except FileNotFoundError as exc:
        assert "Required final-release input does not exist (phase2_path)" in str(exc)
    else:
        raise AssertionError("Expected FileNotFoundError for missing Phase-2 labels")


def test_runner_source_does_not_call_apis_or_batch_jobs() -> None:
    source = inspect.getsource(run_final_release_analysis).casefold()

    assert "openai" not in source
    assert "requests." not in source
    assert "submit_batch" not in source
    assert "data/batch" not in source


def test_critique_evidence_cards_deduplicate_repeated_spans() -> None:
    edges = pd.DataFrame(
        [
            _critique_edge("c1", "BLEU does not capture human judgment."),
            _critique_edge("c2", "BLEU does not capture human judgment."),
            _critique_edge("c3", "BLEU score has weak correlation with human judgment."),
        ]
    )

    cards = build_critique_evidence_cards(edges, per_family=2)
    key = ["bottleneck_family", "object_name", "object_type", "evidence_span"]

    assert len(cards) == 2
    assert not cards.duplicated(key).any()
    assert cards["evidence_span"].nunique() == 2


def _run_fixture_runner(tmp_path: Path, paths: dict[str, Path]) -> dict[str, object]:
    return run_final_release_analysis(
        phase2_path=paths["phase2"],
        excluded_path=paths["excluded"],
        failed_diagnostics_path=paths["failed"],
        object_graph_candidates_path=paths["object_graph"],
        object_mentions_path=paths["object_mentions"],
        contexts_path=paths["contexts"],
        phase1_path=paths["phase1"],
        out_report=tmp_path / "reports" / "final_scisci_results_report_release.md",
        figures_dir=tmp_path / "figures",
        source_data_dir=tmp_path / "figures" / "source_data",
        out_evidence_cards=tmp_path / "data" / "final_release_evidence_cards.csv",
        out_qa_sample=tmp_path / "data" / "final_release_qa_sample.csv",
    )


def _write_fixture_inputs(tmp_path: Path) -> dict[str, Path]:
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    paths = {
        "phase2": inputs / "phase2.parquet",
        "excluded": inputs / "excluded.parquet",
        "failed": inputs / "failed.parquet",
        "object_graph": inputs / "object_graph.parquet",
        "object_mentions": inputs / "object_mentions.parquet",
        "contexts": inputs / "contexts.parquet",
        "phase1": inputs / "phase1.parquet",
    }
    _contexts_fixture().to_parquet(paths["contexts"], index=False)
    labels = _labels_fixture()
    labels.to_parquet(paths["phase2"], index=False)
    labels.head(2).assign(analysis_ready=False, exclusion_reason="synthetic").to_parquet(
        paths["excluded"],
        index=False,
    )
    pd.DataFrame(
        [
            {"context_id": "f1", "failed_validator_type": "schema", "revalidated": False},
            {"context_id": "f2", "failed_validator_type": "schema", "revalidated": True},
            {"context_id": "f3", "failed_validator_type": "evidence", "revalidated": False},
        ]
    ).to_parquet(paths["failed"], index=False)
    _object_graph_fixture(labels["context_id"].tolist()).to_parquet(
        paths["object_graph"],
        index=False,
    )
    pd.DataFrame({"context_id": labels["context_id"]}).to_parquet(
        paths["object_mentions"],
        index=False,
    )
    pd.DataFrame({"context_id": _contexts_fixture()["context_id"]}).to_parquet(
        paths["phase1"],
        index=False,
    )
    return paths


def _contexts_fixture() -> pd.DataFrame:
    rows = []
    for index in range(25):
        rows.append(_context_row(f"a{index}", "PAPER-A", "Background Anchor"))
    for index in range(22):
        rows.append(_context_row(f"b{index}", "PAPER-B", "Evidence Use Riser"))
    rows.append(_context_row("tail0", "TAIL", "One Context Tail"))
    return pd.DataFrame(rows)


def _context_row(context_id: str, acl_id: str, title: str) -> dict[str, object]:
    return {
        "context_id": context_id,
        "resolved_cited_acl_id": acl_id,
        "resolved_cited_title": title,
        "resolved_cited_year": 2020,
        "resolved_cited_authors": "Doe",
    }


def _labels_fixture() -> pd.DataFrame:
    rows = []
    for index in range(6):
        rows.append(_label_row(f"a{index}", "PAPER-A", "Background Anchor", "uses", "methods"))
    for index in range(6, 11):
        rows.append(
            _label_row(
                f"a{index}",
                "PAPER-A",
                "Background Anchor",
                "critiques",
                "results",
                span=f"BLEU does not capture human judgment for a{index}",
            )
        )
    for index in range(5):
        rows.append(
            _label_row(
                f"b{index}",
                "PAPER-B",
                "Evidence Use Riser",
                "compares_against",
                "experiments",
            )
        )
    rows.append(_label_row("tail0", "TAIL", "One Context Tail", "uses", "methods"))
    return pd.DataFrame(rows)


def _label_row(
    context_id: str,
    acl_id: str,
    title: str,
    final_intent: str,
    section: str,
    *,
    span: str | None = None,
) -> dict[str, object]:
    evidence_span = span or f"{final_intent} evidence for {context_id}"
    sentence = f"This sentence contains {evidence_span}."
    return {
        "context_id": context_id,
        "source_context_id": context_id,
        "resolved_cited_acl_id": acl_id,
        "resolved_cited_title": title,
        "resolved_cited_year": 2020,
        "resolved_cited_authors": "Doe",
        "normalized_section": section,
        "raw_section_name": section.title(),
        "sentence_text": sentence,
        "context_window_s3": sentence,
        "primary_candidate_intent": final_intent,
        "final_intent": final_intent,
        "final_object_type": "method",
        "final_relation_subtype": "",
        "method_edge_type": "",
        "analysis_evidence_span": evidence_span,
        "evidence_supports_label": True,
        "abstain": False,
        "analysis_confidence": 0.83,
        "analysis_ready": True,
        "rationale_short": "synthetic fixture",
    }


def _object_graph_fixture(context_ids: list[str]) -> pd.DataFrame:
    rows = []
    for context_id in context_ids:
        if context_id.startswith("a") and int(context_id[1:]) >= 6:
            object_id = "metric::bleu"
            canonical_name = "BLEU"
            object_type = "metric"
        elif context_id.startswith("b"):
            object_id = "benchmark::squad"
            canonical_name = "SQuAD"
            object_type = "benchmark_or_protocol"
        else:
            object_id = "method::bert"
            canonical_name = "BERT"
            object_type = "method"
        rows.append(
            {
                "context_id": context_id,
                "object_id": object_id,
                "canonical_name": canonical_name,
                "object_type": object_type,
                "object_category": object_type,
                "confidence": 0.95,
                "matched_in": "sentence",
                "allow_in_object_graph": True,
                "graph_eligible": True,
            }
        )
        if context_id.startswith("a") and context_id not in {"a0", "a1"}:
            rows.append(
                {
                    "context_id": context_id,
                    "object_id": "method::auxiliary",
                    "canonical_name": "Auxiliary Method",
                    "object_type": "method",
                    "object_category": "method",
                    "confidence": 0.60,
                    "matched_in": "context_window",
                    "allow_in_object_graph": True,
                    "graph_eligible": True,
                }
            )
    return pd.DataFrame(rows)


def _critique_edge(context_id: str, evidence_span: str) -> dict[str, object]:
    return {
        "context_id": context_id,
        "object_id": "metric::bleu",
        "canonical_name": "BLEU",
        "object_type": "metric",
        "final_intent": "critiques",
        "evidence_span": evidence_span,
        "normalized_section": "results",
        "confidence": 0.9,
    }
