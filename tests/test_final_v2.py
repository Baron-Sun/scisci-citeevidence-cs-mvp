from __future__ import annotations

from pathlib import Path

import pandas as pd

from citeevidence.final_v2 import (
    build_final_v2_evidence_cards,
    build_final_v2_object_edges,
    build_final_v2_object_role_profile,
    build_final_v2_ranking_reversal,
    build_final_v2_section_role_profile,
    prepare_final_v2_labels,
    run_final_results_v2_analysis,
)


def _phase2() -> pd.DataFrame:
    rows = [
        ("ctx1", "uses", "uses", "method", "direct_use", "uses_component", "method", "BERT"),
        (
            "ctx2",
            "compares_against",
            "compares_against",
            "metric",
            "compare_against",
            "compares",
            "results",
            "BLEU",
        ),
        (
            "ctx3",
            "critiques",
            "critiques",
            "metric",
            "critique_limitation",
            "not_method_related",
            "evaluation",
            "ROUGE",
        ),
        ("ctx4", "background", "background", "method", "none", "background", "introduction", "CRF"),
        ("ctx5", "extends", "extends", "model", "improve", "extends", "model", "Transformer"),
        (
            "ctx6",
            "applies",
            "applies",
            "dataset_or_database",
            "evaluate_on",
            "uses_component",
            "dataset",
            "SQuAD",
        ),
    ]
    records = []
    for context_id, primary, intent, obj_type, subtype, edge_type, section, obj in rows:
        sentence = f"We discuss {obj} and the evidence says {intent}."
        evidence = f"evidence says {intent}"
        records.append(
            {
                "context_id": context_id,
                "source_context_id": context_id,
                "resolved_cited_acl_id": f"P00-000{context_id[-1]}",
                "resolved_cited_title": f"{obj} Paper",
                "resolved_cited_year": "2020",
                "resolved_cited_authors": "Author",
                "normalized_section": section,
                "raw_section_name": section,
                "sentence_text": sentence,
                "context_window_s3": sentence,
                "primary_candidate_intent": primary,
                "final_intent": intent,
                "final_object_type": obj_type,
                "final_relation_subtype": subtype,
                "method_edge_type": edge_type,
                "evidence_span_phase2": evidence,
                "analysis_evidence_span": evidence,
                "evidence_supports_label": "true",
                "abstain": False,
                "phase2_confidence": 0.9,
                "analysis_confidence": 0.9,
                "analysis_ready": True,
                "rationale_short": "Grounded evidence span.",
            }
        )
    return pd.DataFrame(records)


def _object_graph() -> pd.DataFrame:
    rows = []
    for idx, name in enumerate(["BERT", "BLEU", "ROUGE", "CRF", "Transformer", "SQuAD"], start=1):
        rows.append(
            {
                "context_id": f"ctx{idx}",
                "object_id": f"obj{idx}",
                "canonical_name": name,
                "object_type": "metric" if name in {"BLEU", "ROUGE"} else "model",
                "object_category": "named_object",
                "confidence": 0.95,
                "matched_in": "sentence_text",
                "allow_in_object_graph": True,
                "graph_eligible": True,
            }
        )
    rows.append({**rows[0], "confidence": 0.8})
    rows.append(
        {
            "context_id": "ctx1",
            "object_id": "pseudo",
            "canonical_name": "method",
            "object_type": "method",
            "object_category": "pseudo",
            "confidence": 1.0,
            "matched_in": "sentence_text",
            "allow_in_object_graph": True,
            "graph_eligible": True,
        }
    )
    return pd.DataFrame(rows)


def _contexts() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"context_id": "ctx1", "resolved_cited_acl_id": "A", "resolved_cited_title": "A"},
            {"context_id": "ctx2", "resolved_cited_acl_id": "A", "resolved_cited_title": "A"},
            {"context_id": "ctx3", "resolved_cited_acl_id": "A", "resolved_cited_title": "A"},
            {"context_id": "ctx4", "resolved_cited_acl_id": "B", "resolved_cited_title": "B"},
            {"context_id": "ctx5", "resolved_cited_acl_id": "B", "resolved_cited_title": "B"},
            {"context_id": "ctx6", "resolved_cited_acl_id": "C", "resolved_cited_title": "C"},
        ]
    )


def _phase1() -> pd.DataFrame:
    frame = _phase2()[["context_id", "primary_candidate_intent"]].copy()
    frame["should_send_to_llm"] = True
    return frame


def test_final_v2_edges_use_unique_context_object_intent_and_exclude_pseudo() -> None:
    labels = prepare_final_v2_labels(_phase2())
    edges = build_final_v2_object_edges(labels, _object_graph(), max_objects_per_context=3)

    assert len(edges) == 6
    assert not edges["canonical_name"].eq("method").any()
    assert edges.drop_duplicates(["context_id", "object_id", "final_intent"]).shape[0] == 6
    assert set(edges["edge_unit"]) == {"unique_context_object_intent"}


def test_final_v2_section_and_object_profiles_sum_to_one() -> None:
    labels = prepare_final_v2_labels(_phase2())
    edges = build_final_v2_object_edges(labels, _object_graph())

    section_profile = build_final_v2_section_role_profile(labels)
    object_profile = build_final_v2_object_role_profile(edges)

    section_sums = section_profile.groupby("normalized_section")["row_share"].sum()
    object_sums = object_profile.groupby("object_id")["row_share"].sum()
    assert all(abs(value - 1.0) < 1e-9 for value in section_sums)
    assert all(abs(value - 1.0) < 1e-9 for value in object_sums)


def test_final_v2_ranking_reversal_and_cards_are_grounded() -> None:
    labels = prepare_final_v2_labels(_phase2())
    edges = build_final_v2_object_edges(labels, _object_graph())
    ranking = build_final_v2_ranking_reversal(_contexts(), labels)
    cards = build_final_v2_evidence_cards(edges, ranking)

    assert {
        "rank_by_total_strong_contexts",
        "rank_by_evidence_use_count",
        "rank_difference",
        "absolute_rank_difference",
    }.issubset(ranking.columns)
    assert not cards.empty
    for _, card in cards.iterrows():
        assert card["evidence_span"] in card["sentence_text"]


def test_final_v2_report_figures_and_source_data_are_written(tmp_path: Path) -> None:
    phase2_path = tmp_path / "phase2.parquet"
    excluded_path = tmp_path / "excluded.parquet"
    failed_path = tmp_path / "failed.parquet"
    object_graph_path = tmp_path / "object_graph.parquet"
    object_mentions_path = tmp_path / "object_mentions.parquet"
    contexts_path = tmp_path / "contexts.parquet"
    phase1_path = tmp_path / "phase1.parquet"

    _phase2().to_parquet(phase2_path)
    _phase2().iloc[0:0].to_parquet(excluded_path)
    pd.DataFrame([{"context_id": "failed", "revalidated": False}]).to_parquet(failed_path)
    _object_graph().to_parquet(object_graph_path)
    _object_graph().to_parquet(object_mentions_path)
    _contexts().to_parquet(contexts_path)
    _phase1().to_parquet(phase1_path)

    metrics = run_final_results_v2_analysis(
        phase2_path=phase2_path,
        excluded_path=excluded_path,
        failed_diagnostics_path=failed_path,
        object_graph_candidates_path=object_graph_path,
        object_mentions_path=object_mentions_path,
        contexts_path=contexts_path,
        phase1_path=phase1_path,
        out_report_path=tmp_path / "report.md",
        figures_dir=tmp_path / "figures",
        source_data_dir=tmp_path / "source",
        out_cards_path=tmp_path / "cards.csv",
    )

    report = (tmp_path / "report.md").read_text(encoding="utf-8")
    source_files = sorted((tmp_path / "source").glob("f*.csv"))

    assert metrics["figure_count"] == 8
    assert len(source_files) == 8
    assert (tmp_path / "figures" / "f01_evidence_pipeline.png").exists()
    assert (tmp_path / "figures" / "f01_evidence_pipeline.svg").exists()
    assert len(report.splitlines()) > 50
    assert "\n\n## Figure 1: Evidence Pipeline\n\n" in report
    assert "# Final SciSci-CiteEvidence Results V2" in report.splitlines()[0]
