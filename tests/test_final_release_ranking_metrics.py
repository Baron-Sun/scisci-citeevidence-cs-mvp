from __future__ import annotations

import inspect
from pathlib import Path

import pandas as pd

from citeevidence.final_release.metrics import (
    add_shrunk_evidence_use_share,
    build_paper_evidence_use_table,
    compute_ranking_reversal,
    filter_ranking_reversal_eligible,
)


def _contexts() -> pd.DataFrame:
    rows = []
    for index in range(30):
        rows.append(
            {
                "context_id": f"a{index}",
                "resolved_cited_acl_id": "A00-0001",
                "resolved_cited_title": "Paper A",
            }
        )
    for index in range(25):
        rows.append(
            {
                "context_id": f"b{index}",
                "resolved_cited_acl_id": "B00-0001",
                "resolved_cited_title": "Paper B",
            }
        )
    rows.extend(
        [
            {
                "context_id": "tail0",
                "resolved_cited_acl_id": "T00-0001",
                "resolved_cited_title": "Tail Paper",
            },
            {
                "context_id": "missing-title",
                "resolved_cited_acl_id": "M00-0001",
                "resolved_cited_title": "",
            },
        ]
    )
    return pd.DataFrame(rows)


def _labels() -> pd.DataFrame:
    rows = [
        ("A00-0001", "Paper A", "a0", "background"),
        ("A00-0001", "Paper A", "a0", "background"),
        ("A00-0001", "Paper A", "a1", "uses"),
        ("A00-0001", "Paper A", "a1", "uses"),
        ("A00-0001", "Paper A", "a2", "uses"),
        ("A00-0001", "Paper A", "a3", "compares_against"),
        ("A00-0001", "Paper A", "a4", "extends"),
        ("A00-0001", "Paper A", "a5", "critiques"),
        ("A00-0001", "Paper A", "a6", "applies"),
        ("B00-0001", "Paper B", "b0", "uses"),
        ("B00-0001", "Paper B", "b1", "uses"),
        ("B00-0001", "Paper B", "b2", "uses"),
        ("B00-0001", "Paper B", "b3", "uses"),
        ("B00-0001", "Paper B", "b4", "uses"),
        ("T00-0001", "Tail Paper", "tail0", "uses"),
    ]
    return pd.DataFrame(
        [
            {
                "resolved_cited_acl_id": acl_id,
                "resolved_cited_title": title,
                "context_id": context_id,
                "final_intent": intent,
            }
            for acl_id, title, context_id, intent in rows
        ]
    )


def test_paper_evidence_use_counts_exclude_background_and_deduplicate_labels() -> None:
    table = build_paper_evidence_use_table(_contexts(), _labels())
    paper_a = table.loc[table["resolved_cited_title"].eq("Paper A")].iloc[0]

    assert paper_a["total_strong_contexts"] == 30
    assert paper_a["background_count"] == 1
    assert paper_a["uses_count"] == 2
    assert paper_a["compares_against_count"] == 1
    assert paper_a["extends_count"] == 1
    assert paper_a["critiques_count"] == 1
    assert paper_a["applies_count"] == 1
    assert paper_a["evidence_use_count"] == 6
    assert paper_a["labeled_contexts"] == 7


def test_missing_intent_columns_are_filled_with_zero() -> None:
    contexts = pd.DataFrame(
        [{"context_id": "x1", "resolved_cited_acl_id": "X", "resolved_cited_title": "X Paper"}]
    )
    labels = pd.DataFrame(
        [
            {
                "context_id": "x1",
                "resolved_cited_acl_id": "X",
                "resolved_cited_title": "X Paper",
                "final_intent": "background",
            }
        ]
    )

    table = build_paper_evidence_use_table(contexts, labels)
    row = table.iloc[0]

    assert row["uses_count"] == 0
    assert row["compares_against_count"] == 0
    assert row["extends_count"] == 0
    assert row["critiques_count"] == 0
    assert row["applies_count"] == 0
    assert row["evidence_use_count"] == 0


def test_one_context_papers_are_excluded_by_default_eligibility_filter() -> None:
    table = build_paper_evidence_use_table(_contexts(), _labels())
    eligible = filter_ranking_reversal_eligible(table)

    assert "Tail Paper" not in set(eligible["resolved_cited_title"])
    assert set(eligible["resolved_cited_title"]) == {"Paper A", "Paper B"}


def test_shrinkage_reduces_extreme_one_context_evidence_use_share() -> None:
    table = build_paper_evidence_use_table(_contexts(), _labels())
    shrunk = add_shrunk_evidence_use_share(table)
    tail = shrunk.loc[shrunk["resolved_cited_title"].eq("Tail Paper")].iloc[0]

    assert tail["evidence_use_share"] == 1.0
    assert tail["shrunk_evidence_use_share"] < tail["evidence_use_share"]


def test_rank_difference_count_has_expected_sign() -> None:
    table = pd.DataFrame(
        [
            {
                "resolved_cited_title": "High volume",
                "total_strong_contexts": 100,
                "evidence_use_count": 5,
                "evidence_use_share": 0.05,
            },
            {
                "resolved_cited_title": "Evidence riser",
                "total_strong_contexts": 50,
                "evidence_use_count": 10,
                "evidence_use_share": 0.20,
            },
        ]
    )

    ranked = compute_ranking_reversal(table)
    riser = ranked.loc[ranked["resolved_cited_title"].eq("Evidence riser")].iloc[0]
    volume = ranked.loc[ranked["resolved_cited_title"].eq("High volume")].iloc[0]

    assert riser["rank_difference_count"] > 0
    assert riser["reversal_type"] == "evidence-use riser"
    assert volume["rank_difference_count"] < 0
    assert volume["reversal_type"] == "context-volume riser"


def test_empty_missing_cited_titles_are_filtered() -> None:
    table = build_paper_evidence_use_table(_contexts(), _labels())

    assert "" not in set(table["resolved_cited_title"])
    assert "M00-0001" not in set(table["resolved_cited_acl_id"])


def test_metrics_do_not_require_local_parquet_files(monkeypatch) -> None:
    def fail_read_parquet(*_: object, **__: object) -> None:
        raise AssertionError("ranking metrics should use provided DataFrames")

    monkeypatch.setattr(pd, "read_parquet", fail_read_parquet)

    table = build_paper_evidence_use_table(_contexts(), _labels())

    assert not table.empty


def test_metrics_use_citation_context_volume_terminology() -> None:
    import citeevidence.final_release.metrics as metrics

    source = Path(inspect.getsourcefile(metrics) or "").read_text(encoding="utf-8")
    public_docstrings = "\n".join(
        inspect.getdoc(function) or ""
        for function in [
            build_paper_evidence_use_table,
            add_shrunk_evidence_use_share,
            filter_ranking_reversal_eligible,
            compute_ranking_reversal,
        ]
    )

    assert "citation-context volume" in public_docstrings
    assert "citation count" not in source.casefold()
    assert "citation volume" not in source.casefold()
