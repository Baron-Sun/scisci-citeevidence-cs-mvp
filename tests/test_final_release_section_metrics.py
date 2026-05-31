from __future__ import annotations

import pandas as pd
import pytest

from citeevidence.final_release.metrics import (
    build_section_function_counts,
    build_section_function_lift,
    format_section_label,
)
from citeevidence.final_release.qa import validate_citation_context_volume_terms


def _section_labels() -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    rows.extend(
        {"normalized_section": "methods", "final_intent": "uses"}
        for _ in range(4)
    )
    rows.extend(
        [
            {"normalized_section": "methods", "final_intent": "background"},
            {"normalized_section": "methods", "final_intent": "compares_against"},
        ]
    )
    rows.extend(
        {"normalized_section": "introduction", "final_intent": "background"}
        for _ in range(5)
    )
    rows.append({"normalized_section": "introduction", "final_intent": "uses"})
    rows.extend(
        {"normalized_section": "results", "final_intent": "compares_against"}
        for _ in range(4)
    )
    rows.extend(
        [
            {"normalized_section": "results", "final_intent": "uses"},
            {"normalized_section": "results", "final_intent": "background"},
            {"normalized_section": "appendix", "final_intent": "uses"},
            {"normalized_section": "appendix", "final_intent": "background"},
            {"normalized_section": "", "final_intent": "critiques"},
            {"normalized_section": None, "final_intent": "critiques"},
            {"normalized_section": "methods", "final_intent": ""},
        ]
    )
    return pd.DataFrame(rows)


def test_missing_and_empty_sections_become_unknown() -> None:
    counts = build_section_function_counts(
        pd.DataFrame(
            [
                {"final_intent": "uses"},
                {"normalized_section": "", "final_intent": "background"},
            ]
        )
    )

    unknown = counts.loc[counts["normalized_section"].eq("unknown")]

    assert not unknown.empty
    assert unknown["is_unknown_section"].all()
    assert set(unknown["final_intent"]) == {"background", "uses"}
    assert unknown["section_total"].eq(2).all()


def test_empty_final_intent_rows_are_excluded() -> None:
    counts = build_section_function_counts(_section_labels())

    assert counts["grand_total"].iloc[0] == 22
    assert "" not in set(counts["final_intent"])


def test_section_function_counts_totals_and_shares_are_correct() -> None:
    counts = build_section_function_counts(_section_labels())
    methods_uses = counts.loc[
        counts["normalized_section"].eq("methods")
        & counts["final_intent"].eq("uses")
    ].iloc[0]

    assert methods_uses["rows"] == 4
    assert methods_uses["section_total"] == 6
    assert methods_uses["intent_total"] == 7
    assert methods_uses["grand_total"] == 22
    assert methods_uses["row_share"] == pytest.approx(4 / 6)
    assert methods_uses["global_share"] == pytest.approx(7 / 22)
    assert methods_uses["section_label"] == "Methods (N=6)"
    assert format_section_label("methods", 6300) == "Methods (N=6.3k)"


def test_section_function_lift_detects_overrepresented_cells() -> None:
    counts = build_section_function_counts(_section_labels())
    lift = build_section_function_lift(counts, min_section_total=3)
    methods_uses = lift.loc[
        lift["normalized_section"].eq("methods")
        & lift["final_intent"].eq("uses")
    ].iloc[0]

    assert methods_uses["log_odds_lift"] > 0
    assert methods_uses["lift_direction"] == "overrepresented"


def test_low_count_sections_are_filtered_but_unknown_is_retained() -> None:
    counts = build_section_function_counts(_section_labels())
    lift = build_section_function_lift(counts, min_section_total=3)

    assert "appendix" not in set(lift["normalized_section"])
    assert "unknown" in set(lift["normalized_section"])
    assert lift.loc[lift["normalized_section"].eq("unknown"), "is_unknown_section"].all()


def test_section_metrics_do_not_require_local_parquet_files(monkeypatch) -> None:
    def fail_read_parquet(*_: object, **__: object) -> None:
        raise AssertionError("section metrics should use provided DataFrames")

    monkeypatch.setattr(pd, "read_parquet", fail_read_parquet)

    counts = build_section_function_counts(_section_labels())
    lift = build_section_function_lift(counts, min_section_total=3)

    assert not counts.empty
    assert not lift.empty


def test_section_metric_text_preserves_terminology_guardrails() -> None:
    assert validate_citation_context_volume_terms(
        "Section-function results use final analysis-ready Phase-2 labels."
    ) == []
