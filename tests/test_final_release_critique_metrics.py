from __future__ import annotations

import pandas as pd
import pytest

from citeevidence.final_release.metrics import (
    CRITIQUE_BOTTLENECK_RULE_VERSION,
    build_critique_bottleneck_matrix,
    build_critique_evidence_cards,
    classify_critique_bottleneck_family,
)


@pytest.mark.parametrize(
    ("text", "family"),
    [
        ("BLEU does not capture human judgment well.", "metric_validity"),
        ("The method does not generalize to cross-domain transfer.", "generalization_domain"),
        ("The system requires annotated training data.", "data_resource_requirement"),
        ("The model is computationally expensive and slow.", "computational_cost"),
        ("The approach is not scalable to large-scale settings.", "scalability"),
        ("The code and implementation are unavailable.", "reproducibility_tooling"),
        ("The model misses multilingual morphology and syntax.", "linguistic_coverage"),
        ("The outputs are poor and noisy with many errors.", "poor_performance"),
        ("The method fails and has a serious limitation.", "failure_limitation"),
    ],
)
def test_classify_critique_bottleneck_family_returns_expected_family(
    text: str,
    family: str,
) -> None:
    assert classify_critique_bottleneck_family(text) == family


def test_classify_critique_bottleneck_family_empty_text_returns_other() -> None:
    assert classify_critique_bottleneck_family("") == "other"


def _critique_edges() -> pd.DataFrame:
    rows = [
        {
            "final_intent": "critiques",
            "object_type": "method",
            "canonical_name": "BERT",
            "object_id": "bert",
            "evidence_span": "BLEU does not capture human judgment.",
            "context_id": "c1",
            "confidence": 0.82,
            "normalized_section": "results",
        },
        {
            "final_intent": "critiques",
            "object_type": "method",
            "canonical_name": "BERT",
            "object_id": "bert",
            "evidence_span": "BLEU does not capture human judgment.",
            "context_id": "c1",
            "confidence": 0.82,
            "normalized_section": "results",
        },
        {
            "final_intent": "critiques",
            "object_type": "method",
            "canonical_name": "BERT",
            "object_id": "bert",
            "evidence_span": "Fails on out-of-domain transfer.",
            "context_id": "c2",
            "confidence": 0.80,
            "normalized_section": "discussion",
        },
        {
            "final_intent": "critiques",
            "object_type": "method",
            "canonical_name": "BERT",
            "object_id": "bert",
            "evidence_span": "Requires annotated training data.",
            "context_id": "c3",
            "confidence": 0.78,
            "normalized_section": "discussion",
        },
        {
            "final_intent": "critiques",
            "object_type": "dataset_or_database",
            "canonical_name": "Treebank",
            "object_id": "treebank",
            "evidence_span": "The resource is expensive to use.",
            "context_id": "c4",
            "confidence": 0.74,
            "normalized_section": "limitations",
        },
        {
            "final_intent": "critiques",
            "object_type": "dataset_or_database",
            "canonical_name": "Treebank",
            "object_id": "treebank",
            "evidence_span": "The annotation process is costly.",
            "context_id": "c5",
            "confidence": 0.76,
            "normalized_section": "limitations",
        },
        {
            "final_intent": "critiques",
            "object_type": "software_or_tool",
            "canonical_name": "Toolkit",
            "object_id": "toolkit",
            "evidence_span": "The implementation code is unavailable.",
            "context_id": "c6",
            "confidence": 0.70,
            "normalized_section": "limitations",
        },
        {
            "final_intent": "critiques",
            "object_type": "",
            "canonical_name": "Parser",
            "object_id": "parser",
            "evidence_span": "The model misses multilingual morphology.",
            "context_id": "c7",
            "confidence": 0.77,
            "normalized_section": "analysis",
        },
        {
            "final_intent": "uses",
            "object_type": "method",
            "canonical_name": "BERT",
            "object_id": "bert",
            "evidence_span": "The paper uses BERT.",
            "context_id": "u1",
            "confidence": 0.90,
            "normalized_section": "methods",
        },
    ]
    return pd.DataFrame(rows)


def test_critique_matrix_includes_only_critiques_and_deduplicates_rows() -> None:
    matrix = build_critique_bottleneck_matrix(_critique_edges())

    assert matrix["grand_total"].iloc[0] == 7
    assert "uses" not in set(matrix.get("final_intent", []))
    method_metric = matrix.loc[
        matrix["object_type"].eq("method")
        & matrix["bottleneck_family"].eq("metric_validity")
    ].iloc[0]
    assert method_metric["rows"] == 1


def test_critique_matrix_totals_and_lift_are_correct() -> None:
    matrix = build_critique_bottleneck_matrix(_critique_edges())
    method_metric = matrix.loc[
        matrix["object_type"].eq("method")
        & matrix["bottleneck_family"].eq("metric_validity")
    ].iloc[0]

    assert method_metric["object_type_total"] == 3
    assert method_metric["family_total"] == 1
    assert method_metric["grand_total"] == 7
    assert method_metric["row_share_within_object_type"] == pytest.approx(1 / 3)
    assert method_metric["row_share_global"] == pytest.approx(1 / 7)
    assert method_metric["lift_vs_global"] == pytest.approx((1 / 3) / (1 / 7))
    assert method_metric["lift_vs_global"] > 0
    assert method_metric["rule_version"] == CRITIQUE_BOTTLENECK_RULE_VERSION


def test_critique_matrix_handles_unknown_object_type() -> None:
    matrix = build_critique_bottleneck_matrix(_critique_edges())

    assert "unknown" in set(matrix["object_type"])


def test_critique_evidence_cards_are_deterministic_and_capped() -> None:
    first = build_critique_evidence_cards(_critique_edges(), per_family=1, seed=7)
    second = build_critique_evidence_cards(_critique_edges(), per_family=1, seed=7)

    pd.testing.assert_frame_equal(first, second)
    assert first.groupby("bottleneck_family").size().max() == 1


def test_critique_evidence_cards_include_caveat_friendly_fields() -> None:
    cards = build_critique_evidence_cards(_critique_edges(), per_family=1, seed=7)

    assert set(cards.columns) == {
        "bottleneck_family",
        "object_name",
        "object_type",
        "context_id",
        "normalized_section",
        "evidence_span",
        "confidence",
    }
    assert cards["evidence_span"].ne("").all()


def test_critique_metrics_do_not_require_local_parquet_files(monkeypatch) -> None:
    def fail_read_parquet(*_: object, **__: object) -> None:
        raise AssertionError("critique metrics should use provided DataFrames")

    monkeypatch.setattr(pd, "read_parquet", fail_read_parquet)

    assert not build_critique_bottleneck_matrix(_critique_edges()).empty
    assert not build_critique_evidence_cards(_critique_edges()).empty
