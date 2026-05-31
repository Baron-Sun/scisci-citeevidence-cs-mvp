from __future__ import annotations

import pandas as pd
import pytest

from citeevidence.final_release.qa import (
    build_label_quality_summary,
    build_stratified_qa_sample,
    summarize_confidence_by_intent,
    summarize_failure_categories,
    validate_evidence_grounding,
)


def test_validate_evidence_grounding_checks_exact_substrings() -> None:
    labels = pd.DataFrame(
        [
            {
                "context_id": "c1",
                "evidence_span": "uses BERT",
                "sentence_text": "The model uses BERT as an encoder.",
                "context_window_s3": "",
                "evidence_supports_label": "true",
                "abstain": "false",
                "analysis_ready": True,
                "confidence": "0.91",
            },
            {
                "context_id": "c2",
                "evidence_span": "missing evidence",
                "sentence_text": "The evidence is absent.",
                "context_window_s3": "No matching span here.",
                "evidence_supports_label": False,
                "abstain": True,
                "analysis_ready": False,
                "confidence": "0.44",
            },
        ]
    )

    validated = validate_evidence_grounding(labels)

    assert bool(validated.loc[0, "evidence_span_grounded"])
    assert not bool(validated.loc[1, "evidence_span_grounded"])
    assert bool(validated.loc[0, "evidence_supports_label_bool"])
    assert bool(validated.loc[1, "abstain_bool"])
    assert validated.loc[0, "confidence_numeric"] == pytest.approx(0.91)


def test_validate_evidence_grounding_uses_evidence_and_confidence_fallbacks() -> None:
    labels = pd.DataFrame(
        [
            {
                "context_id": "c1",
                "analysis_evidence_span": "analysis span",
                "evidence_span_phase2": "phase2 span",
                "sentence_text": "The analysis span is grounded.",
                "analysis_confidence": "0.72",
                "phase2_confidence": "0.61",
            },
            {
                "context_id": "c2",
                "analysis_evidence_span": "",
                "evidence_span_phase2": "phase2 span",
                "sentence_text": "The phase2 span is grounded.",
                "analysis_confidence": None,
                "phase2_confidence": "0.64",
            },
        ]
    )

    validated = validate_evidence_grounding(labels)

    assert validated.loc[0, "unified_evidence_span"] == "analysis span"
    assert validated.loc[1, "unified_evidence_span"] == "phase2 span"
    assert validated.loc[0, "confidence_numeric"] == pytest.approx(0.72)
    assert validated.loc[1, "confidence_numeric"] == pytest.approx(0.64)
    assert validated["evidence_span_grounded"].tolist() == [True, True]


def test_label_quality_summary_counts_grounded_and_ungrounded_rows() -> None:
    labels = pd.DataFrame(
        [
            {
                "context_id": "c1",
                "final_intent": "uses",
                "evidence_span": "grounded span",
                "sentence_text": "A grounded span appears here.",
                "evidence_supports_label": True,
                "abstain": False,
                "analysis_ready": True,
                "confidence": 0.8,
                "normalized_section": "methods",
            },
            {
                "context_id": "c2",
                "final_intent": "background",
                "evidence_span": "not grounded",
                "sentence_text": "No match.",
                "evidence_supports_label": False,
                "abstain": True,
                "analysis_ready": True,
                "confidence": 0.6,
                "normalized_section": "introduction",
            },
            {
                "context_id": "c3",
                "final_intent": "uses",
                "evidence_span": "",
                "sentence_text": "Missing evidence span.",
                "analysis_ready": False,
                "confidence": 0.7,
                "normalized_section": "methods",
            },
        ]
    )

    summary = build_label_quality_summary(
        labels,
        excluded=pd.DataFrame({"context_id": ["x1", "x2"]}),
        failed_diagnostics=pd.DataFrame({"context_id": ["f1"]}),
    )
    values = dict(zip(summary["metric"], summary["value"], strict=True))

    assert values["total_labels"] == 3
    assert values["analysis_ready_rows"] == 2
    assert values["evidence_span_present_rows"] == 2
    assert values["evidence_span_grounded_rows"] == 1
    assert values["evidence_span_not_grounded_rows"] == 1
    assert values["evidence_supports_label_true_rows"] == 1
    assert values["abstain_true_rows"] == 1
    assert values["mean_confidence"] == pytest.approx(0.7)
    assert values["excluded_rows"] == 2
    assert values["remaining_failed_rows"] == 1
    assert values["distinct_final_intents"] == 2
    assert values["distinct_sections"] == 2


def test_label_quality_summary_marks_analysis_ready_missing_when_column_absent() -> None:
    labels = pd.DataFrame(
        [
            {
                "context_id": "c1",
                "final_intent": "uses",
                "evidence_span": "grounded span",
                "sentence_text": "A grounded span appears here.",
            }
        ]
    )

    summary = build_label_quality_summary(labels)
    row = summary.loc[summary["metric"].eq("analysis_ready_rows")].iloc[0]

    assert pd.isna(row["value"])
    assert "analysis_ready column not present" in row["note"]


def test_label_quality_summary_counts_analysis_ready_when_column_present() -> None:
    labels = pd.DataFrame(
        [
            {"context_id": "c1", "analysis_ready": True},
            {"context_id": "c2", "analysis_ready": "true"},
            {"context_id": "c3", "analysis_ready": False},
            {"context_id": "c4", "analysis_ready": ""},
        ]
    )

    summary = build_label_quality_summary(labels)
    row = summary.loc[summary["metric"].eq("analysis_ready_rows")].iloc[0]

    assert row["value"] == 2
    assert row["note"] == ""


def test_label_quality_summary_counts_unrevalidated_failed_rows() -> None:
    labels = pd.DataFrame([{"context_id": "c1"}])
    failed = pd.DataFrame(
        [
            {"context_id": "f1", "revalidated": True},
            {"context_id": "f2", "revalidated": "true"},
            {"context_id": "f3", "revalidated": False},
            {"context_id": "f4", "revalidated": ""},
        ]
    )

    summary = build_label_quality_summary(labels, failed_diagnostics=failed)
    values = dict(zip(summary["metric"], summary["value"], strict=True))

    assert values["remaining_failed_rows"] == 2


def test_label_quality_summary_counts_all_failed_rows_without_revalidated_column() -> None:
    labels = pd.DataFrame([{"context_id": "c1"}])
    failed = pd.DataFrame({"context_id": ["f1", "f2", "f3"]})

    summary = build_label_quality_summary(labels, failed_diagnostics=failed)
    values = dict(zip(summary["metric"], summary["value"], strict=True))

    assert values["remaining_failed_rows"] == 3


def test_summarize_confidence_by_intent_computes_expected_stats() -> None:
    labels = pd.DataFrame(
        [
            {"final_intent": "background", "confidence": 0.6},
            {"final_intent": "background", "confidence": 0.8},
            {"final_intent": "uses", "confidence": 0.9},
        ]
    )

    summary = summarize_confidence_by_intent(labels)
    background = summary.loc[summary["final_intent"].eq("background")].iloc[0]
    uses = summary.loc[summary["final_intent"].eq("uses")].iloc[0]

    assert background["rows"] == 2
    assert background["mean_confidence"] == pytest.approx(0.7)
    assert background["median_confidence"] == pytest.approx(0.7)
    assert background["min_confidence"] == pytest.approx(0.6)
    assert background["max_confidence"] == pytest.approx(0.8)
    assert background["share_below_0_7"] == pytest.approx(0.5)
    assert uses["share_below_0_7"] == pytest.approx(0.0)


def test_summarize_failure_categories_uses_best_available_failure_column() -> None:
    failed = pd.DataFrame(
        {
            "validator_failure_type": ["schema", "schema", "grounding"],
            "error_type": ["unused", "unused", "unused"],
        }
    )

    summary = summarize_failure_categories(failed)

    assert summary.loc[0, "failure_category"] == "schema"
    assert summary.loc[0, "rows"] == 2
    assert summary.loc[0, "row_share"] == pytest.approx(2 / 3)
    assert list(summarize_failure_categories(None).columns) == [
        "failure_category",
        "rows",
        "row_share",
    ]


def _sample_fixture(include_risk_columns: bool = True) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    intents = ["background", "uses", "compares_against", "critiques", "extends", "applies"]
    for intent in intents:
        for index in range(4):
            rows.append(
                {
                    "context_id": f"{intent}-{index}",
                    "final_intent": intent,
                    "confidence": 0.82 + index / 100,
                    "evidence_span": f"{intent} evidence {index}",
                    "sentence_text": f"This sentence contains {intent} evidence {index}.",
                    "resolved_cited_title": f"{intent.title()} Paper",
                    "normalized_section": "methods",
                }
            )
    rows.append(
        {
            "context_id": "boundary-1",
            "final_intent": "background",
            "confidence": 0.69,
            "evidence_span": "boundary evidence",
            "sentence_text": "The boundary evidence is present.",
            "normalized_section": "results",
        }
    )
    rows.append(
        {
            "context_id": "boundary-2",
            "final_intent": "uses",
            "confidence": 0.71,
            "evidence_span": "second boundary evidence",
            "sentence_text": "The second boundary evidence is present.",
            "normalized_section": "experiments",
        }
    )
    if include_risk_columns:
        rows.extend(
            [
                {
                    "context_id": "risk-object-count",
                    "final_intent": "uses",
                    "confidence": 0.88,
                    "evidence_span": "risk evidence",
                    "sentence_text": "The risk evidence is present.",
                    "object_count": 2,
                    "object_candidate_rank": 1,
                    "matched_in": "sentence_text",
                },
                {
                    "context_id": "risk-matched-in",
                    "final_intent": "critiques",
                    "confidence": 0.86,
                    "evidence_span": "policy risk evidence",
                    "sentence_text": "The policy risk evidence is present.",
                    "object_count": 1,
                    "object_candidate_rank": 2,
                    "matched_in": "title",
                },
            ]
        )
    return pd.DataFrame(rows)


def test_stratified_qa_sample_is_deterministic_and_has_reviewer_columns() -> None:
    labels = _sample_fixture()

    first = build_stratified_qa_sample(labels, n=20, seed=7).reset_index(drop=True)
    second = build_stratified_qa_sample(labels, n=20, seed=7).reset_index(drop=True)

    pd.testing.assert_frame_equal(first, second)
    for column in [
        "reviewer_final_intent_correct",
        "reviewer_evidence_supports_label",
        "reviewer_object_type_correct",
        "reviewer_relation_subtype_correct",
        "reviewer_should_exclude",
        "reviewer_notes",
    ]:
        assert column in first


def test_stratified_qa_sample_includes_boundary_and_risk_rows() -> None:
    sample = build_stratified_qa_sample(_sample_fixture(), n=20, seed=7)

    assert "confidence_boundary_near_0_70" in set(sample["sample_stratum"])
    assert "multi_object_or_policy_risk" in set(sample["sample_stratum"])
    assert {"boundary-1", "boundary-2"} & set(sample["context_id"])
    assert {"risk-object-count", "risk-matched-in"} & set(sample["context_id"])


def test_stratified_qa_sample_missing_risk_columns_does_not_crash() -> None:
    sample = build_stratified_qa_sample(_sample_fixture(include_risk_columns=False), n=20, seed=7)

    assert "multi_object_or_policy_risk" not in set(sample["sample_stratum"])
    assert "sample_shortfall" in sample
    assert sample["sample_shortfall"].str.contains("missing risk columns").any()


def test_qa_helpers_do_not_require_local_parquet_files(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_read_parquet(*_: object, **__: object) -> None:
        raise AssertionError("final-release QA helpers should use provided DataFrames")

    monkeypatch.setattr(pd, "read_parquet", fail_read_parquet)
    labels = _sample_fixture()

    assert not validate_evidence_grounding(labels).empty
    assert not build_label_quality_summary(labels).empty
    assert not summarize_confidence_by_intent(labels).empty
    assert not build_stratified_qa_sample(labels, n=10).empty
