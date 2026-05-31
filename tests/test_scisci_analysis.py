from __future__ import annotations

from pathlib import Path

import pandas as pd

from citeevidence.analysis import (
    build_benchmark_metric_network,
    build_cited_paper_evidence_use_summary,
    build_critique_bottleneck_map,
    build_evidence_backed_object_graph,
    build_evidence_cards,
    build_evidence_funnel,
    build_object_function_matrix_phase1,
    build_object_function_matrix_phase2,
    build_object_graph_report,
    build_object_infrastructure_ranking,
    build_phase1_phase2_calibration,
    build_scisci_full_report,
    build_section_function_rates,
    write_scisci_full_figures,
)


def _contexts() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "context_id": "ctx1",
                "resolved_cited_acl_id": "P00-0001",
                "resolved_cited_title": "BERT",
                "normalized_section": "method",
            },
            {
                "context_id": "ctx2",
                "resolved_cited_acl_id": "P00-0002",
                "resolved_cited_title": "BLEU",
                "normalized_section": "evaluation",
            },
            {
                "context_id": "ctx3",
                "resolved_cited_acl_id": "P00-0001",
                "resolved_cited_title": "BERT",
                "normalized_section": "related_work",
            },
        ]
    )


def _object_graph() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "context_id": "ctx1",
                "canonical_name": "BERT",
                "object_type": "method",
                "object_category": "model",
            },
            {
                "context_id": "ctx2",
                "canonical_name": "BLEU",
                "object_type": "metric",
                "object_category": "metric",
            },
            {
                "context_id": "ctx5",
                "canonical_name": "GLUE",
                "object_type": "benchmark_or_protocol",
                "object_category": "benchmark",
            },
        ]
    )


def _object_mentions() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"context_id": "ctx1", "canonical_name": "BERT", "object_type": "method"},
            {"context_id": "ctx2", "canonical_name": "BLEU", "object_type": "metric"},
            {"context_id": "ctx3", "canonical_name": "BERT", "object_type": "method"},
            {"context_id": "ctx5", "canonical_name": "GLUE", "object_type": "benchmark"},
        ]
    )


def _phase1() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "context_id": "ctx1",
                "resolved_cited_acl_id": "P00-0001",
                "resolved_cited_title": "BERT",
                "primary_candidate_intent": "uses",
                "normalized_section": "method",
                "should_send_to_llm": True,
            },
            {
                "context_id": "ctx2",
                "resolved_cited_acl_id": "P00-0002",
                "resolved_cited_title": "BLEU",
                "primary_candidate_intent": "critiques",
                "normalized_section": "evaluation",
                "should_send_to_llm": True,
            },
            {
                "context_id": "ctx3",
                "resolved_cited_acl_id": "P00-0001",
                "resolved_cited_title": "BERT",
                "primary_candidate_intent": "background",
                "normalized_section": "related_work",
                "should_send_to_llm": False,
            },
            {
                "context_id": "ctx4",
                "resolved_cited_acl_id": "P00-0003",
                "resolved_cited_title": "High Count Background",
                "primary_candidate_intent": "background",
                "normalized_section": "introduction",
                "should_send_to_llm": False,
            },
            {
                "context_id": "ctx5",
                "resolved_cited_acl_id": "P00-0004",
                "resolved_cited_title": "GLUE",
                "primary_candidate_intent": "compares_against",
                "normalized_section": "results",
                "should_send_to_llm": True,
            },
        ]
    )


def _phase2() -> pd.DataFrame:
    rows = [
        {
            "context_id": "ctx1",
            "primary_candidate_intent": "uses",
            "final_intent": "uses",
            "final_object_type": "method",
            "final_relation_subtype": "direct_use",
            "method_edge_type": "uses_component",
            "stance": "neutral",
            "normalized_section": "method",
            "resolved_cited_acl_id": "P00-0001",
            "resolved_cited_title": "BERT",
            "sentence_text": "We use BERT as our encoder.",
            "context_window_s3": "We use BERT as our encoder.",
            "evidence_span_phase2": "use BERT as our encoder",
            "problem_or_motivation_quote": "",
            "usage_or_mechanism_quote": "use BERT as our encoder",
            "comparison_or_tradeoff_quote": "",
            "evidence_supports_label": "true",
            "abstain": False,
            "phase2_confidence": 0.92,
            "rationale_short": "The sentence says the current paper uses BERT.",
            "object_names": "BERT",
            "graph_candidate_object_names": "BERT",
            "object_types": "method",
            "generic_metric_names": "",
        },
        {
            "context_id": "ctx2",
            "primary_candidate_intent": "critiques",
            "final_intent": "critiques",
            "final_object_type": "metric",
            "final_relation_subtype": "critique_limitation",
            "method_edge_type": "not_method_related",
            "stance": "negative",
            "normalized_section": "evaluation",
            "resolved_cited_acl_id": "P00-0002",
            "resolved_cited_title": "BLEU",
            "sentence_text": "The BLEU metric does not capture meaning.",
            "context_window_s3": "The BLEU metric does not capture meaning.",
            "evidence_span_phase2": "BLEU metric does not capture meaning",
            "problem_or_motivation_quote": "does not capture meaning",
            "usage_or_mechanism_quote": "",
            "comparison_or_tradeoff_quote": "",
            "evidence_supports_label": "true",
            "abstain": False,
            "phase2_confidence": 0.81,
            "rationale_short": "The context criticizes BLEU as a metric.",
            "object_names": "BLEU",
            "graph_candidate_object_names": "BLEU",
            "object_types": "metric",
            "generic_metric_names": "BLEU",
        },
        {
            "context_id": "ctx3",
            "primary_candidate_intent": "background",
            "final_intent": "background",
            "final_object_type": "method",
            "final_relation_subtype": "direct_use",
            "method_edge_type": "background",
            "stance": "neutral",
            "normalized_section": "related_work",
            "resolved_cited_acl_id": "P00-0001",
            "resolved_cited_title": "BERT",
            "sentence_text": "Prior work describes BERT.",
            "context_window_s3": "Prior work describes BERT.",
            "evidence_span_phase2": "",
            "problem_or_motivation_quote": "",
            "usage_or_mechanism_quote": "",
            "comparison_or_tradeoff_quote": "",
            "evidence_supports_label": "false",
            "abstain": True,
            "phase2_confidence": 0.1,
            "rationale_short": "Ambiguous evidence.",
            "object_names": "BERT",
            "graph_candidate_object_names": "BERT",
            "object_types": "method",
            "generic_metric_names": "",
        },
        {
            "context_id": "ctx5",
            "primary_candidate_intent": "compares_against",
            "final_intent": "compares_against",
            "final_object_type": "benchmark_or_protocol",
            "final_relation_subtype": "compare_against",
            "method_edge_type": "compares",
            "stance": "neutral",
            "normalized_section": "results",
            "resolved_cited_acl_id": "P00-0004",
            "resolved_cited_title": "GLUE",
            "sentence_text": "We compare against GLUE leaderboard baselines.",
            "context_window_s3": "We compare against GLUE leaderboard baselines.",
            "evidence_span_phase2": "compare against GLUE leaderboard",
            "problem_or_motivation_quote": "",
            "usage_or_mechanism_quote": "",
            "comparison_or_tradeoff_quote": "compare against GLUE leaderboard",
            "evidence_supports_label": "false",
            "abstain": False,
            "phase2_confidence": 0.95,
            "rationale_short": "Unsupported labels are excluded from strict graph.",
            "object_names": "GLUE",
            "graph_candidate_object_names": "GLUE",
            "object_types": "benchmark_or_protocol",
            "generic_metric_names": "",
        },
    ]
    return pd.DataFrame(rows)


def test_evidence_funnel_counts_are_computed() -> None:
    funnel = build_evidence_funnel(
        contexts=_contexts(),
        object_mentions=_object_mentions(),
        object_graph=_object_graph(),
        phase1=_phase1(),
        phase2=_phase2(),
        sectioned_context_count=10,
        resolved_component_count=8,
    )

    counts = dict(zip(funnel["step"], funnel["count"], strict=True))
    assert counts["section_aware_citation_contexts"] == 10
    assert counts["resolved_citation_marker_components"] == 8
    assert counts["analysis_ready_strong_contexts"] == 3
    assert counts["phase1_llm_candidate_contexts"] == 3


def test_object_function_matrix_and_section_rates_are_stable() -> None:
    phase1_matrix = build_object_function_matrix_phase1(_phase1(), _object_graph())
    phase2_matrix = build_object_function_matrix_phase2(_phase2())
    section_rates = build_section_function_rates(_phase1())

    bert = phase1_matrix.loc[phase1_matrix["canonical_name"].eq("BERT")].iloc[0]
    assert bert["uses"] == 1
    assert {"BERT", "BLEU", "GLUE"}.issubset(set(phase2_matrix["canonical_name"]))
    sums = section_rates.groupby("normalized_section")["rate_within_section"].sum()
    assert all(abs(value - 1.0) < 1e-9 for value in sums)


def test_cited_paper_ranking_reversal_is_computed() -> None:
    summary = build_cited_paper_evidence_use_summary(_phase1())

    bert = summary.loc[summary["resolved_cited_acl_id"].eq("P00-0001")].iloc[0]
    glue = summary.loc[summary["resolved_cited_acl_id"].eq("P00-0004")].iloc[0]
    assert bert["total_strong_contexts"] == 2
    assert bert["evidence_use_count"] == 1
    assert glue["evidence_use_count"] == 1
    assert "rank_difference" in summary.columns


def test_scisci_report_and_figures_are_written(tmp_path: Path) -> None:
    funnel = build_evidence_funnel(
        contexts=_contexts(),
        object_mentions=_object_mentions(),
        object_graph=_object_graph(),
        phase1=_phase1(),
        phase2=_phase2(),
        sectioned_context_count=10,
        resolved_component_count=8,
    )
    phase1_matrix = build_object_function_matrix_phase1(_phase1(), _object_graph())
    phase2_matrix = build_object_function_matrix_phase2(_phase2())
    calibration = build_phase1_phase2_calibration(_phase2())
    section_rates = build_section_function_rates(_phase1())
    infrastructure = build_object_infrastructure_ranking(_phase1(), _object_graph())
    cited_summary = build_cited_paper_evidence_use_summary(_phase1())

    figures = write_scisci_full_figures(
        funnel=funnel,
        object_matrix_phase1=phase1_matrix,
        object_matrix_phase2=phase2_matrix,
        section_rates=section_rates,
        calibration=calibration,
        infrastructure=infrastructure,
        figures_dir=tmp_path / "figures",
        source_data_dir=tmp_path / "source",
    )
    report = build_scisci_full_report(
        funnel=funnel,
        object_matrix_phase1=phase1_matrix,
        object_matrix_phase2=phase2_matrix,
        calibration=calibration,
        section_rates=section_rates,
        infrastructure=infrastructure,
        cited_summary=cited_summary,
        shortlist=pd.DataFrame(),
        figure_paths=figures,
        strict_graph=None,
        broad_graph=None,
        cited_profiles=None,
        phase1_features=None,
        failed_diagnostics=None,
    )

    assert "candidate-level signals" in report
    assert (tmp_path / "source" / "scisci_evidence_funnel.csv").exists()
    assert (tmp_path / "source" / "object_function_heatmap_phase1.csv").exists()
    for figure in figures.values():
        assert Path(figure).exists()


def test_strict_object_graph_excludes_abstain_and_unsupported_labels() -> None:
    nodes, edges = build_evidence_backed_object_graph(_phase2(), _object_graph())

    assert set(edges["context_id"]) == {"ctx1", "ctx2"}
    assert not edges["context_id"].isin(["ctx3", "ctx5"]).any()
    assert set(nodes["canonical_name"]) == {"BERT", "BLEU"}
    assert {"context_id", "canonical_name", "final_intent", "evidence_span_phase2"}.issubset(
        edges.columns
    )


def test_object_graph_excludes_pseudo_nodes_and_missing_candidates() -> None:
    extra_phase2 = pd.concat(
        [
            _phase2(),
            pd.DataFrame(
                [
                    {
                        **_phase2().iloc[0].to_dict(),
                        "context_id": "ctx_pseudo",
                        "sentence_text": "We use method directly.",
                        "context_window_s3": "We use method directly.",
                        "evidence_span_phase2": "use method directly",
                        "graph_candidate_object_names": "method",
                        "object_names": "method",
                    },
                    {
                        **_phase2().iloc[0].to_dict(),
                        "context_id": "ctx_missing",
                        "sentence_text": "We use a real system.",
                        "context_window_s3": "We use a real system.",
                        "evidence_span_phase2": "use a real system",
                        "graph_candidate_object_names": "",
                        "object_names": "",
                    },
                ]
            ),
        ],
        ignore_index=True,
    )
    extra_graph = pd.concat(
        [
            _object_graph(),
            pd.DataFrame(
                [
                    {
                        "context_id": "ctx_pseudo",
                        "canonical_name": "method",
                        "object_type": "method",
                        "object_category": "named_object",
                        "confidence": 1.0,
                        "matched_in": "sentence_text",
                        "allow_in_object_graph": True,
                        "graph_eligible": True,
                    }
                ]
            ),
        ],
        ignore_index=True,
    )

    _, edges = build_evidence_backed_object_graph(extra_phase2, extra_graph)

    assert "method" not in set(edges["canonical_name"])
    assert "ctx_pseudo" not in set(edges["context_id"])
    assert "ctx_missing" not in set(edges["context_id"])


def test_evidence_cards_include_grounded_spans() -> None:
    _, edges = build_evidence_backed_object_graph(_phase2(), _object_graph())
    cards = build_evidence_cards(edges)

    assert not cards.empty
    for _, card in cards.iterrows():
        assert card["evidence_span"] in card["citation_sentence"]


def test_critique_and_benchmark_helpers() -> None:
    _, edges = build_evidence_backed_object_graph(_phase2(), _object_graph())
    critique_map = build_critique_bottleneck_map(edges)
    benchmark_network = build_benchmark_metric_network(edges)

    assert "metric_limitation" in set(critique_map["cue_family"])
    assert set(benchmark_network["canonical_name"]) == {"BLEU"}


def test_object_graph_report_generation_works() -> None:
    nodes, edges = build_evidence_backed_object_graph(_phase2(), _object_graph())
    cards = build_evidence_cards(edges)
    broad = build_object_infrastructure_ranking(_phase1(), _object_graph())

    report = build_object_graph_report(
        nodes=nodes,
        edges=edges,
        cards=cards,
        broad_ranking=broad,
        critique_map=build_critique_bottleneck_map(edges),
        benchmark_network=build_benchmark_metric_network(edges),
        figure_paths={"example": "figures/example.png"},
        object_mentions=_object_mentions(),
    )

    assert "Evidence-Backed Object-Use Mini Graph Report" in report
    assert "strict_object_edges" in report
