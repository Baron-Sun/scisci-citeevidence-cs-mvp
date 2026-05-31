from __future__ import annotations

import matplotlib
import pandas as pd

matplotlib.use("Agg")

from citeevidence.final_release.figures import (
    plot_context_volume_vs_evidence_use_reversal,
)
from citeevidence.final_release.metrics import build_ranking_reversal_plot_table


def _ranking_rows() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "resolved_cited_acl_id": "A00-0001",
                "resolved_cited_title": (
                    "A Very Long Background Canon Paper Title That Needs Clean Truncation"
                ),
                "total_strong_contexts": 100,
                "evidence_use_count": 5,
                "evidence_use_share": 0.05,
                "background_share": 0.90,
            },
            {
                "resolved_cited_acl_id": "B00-0001",
                "resolved_cited_title": "Evidence Use Riser",
                "total_strong_contexts": 50,
                "evidence_use_count": 30,
                "evidence_use_share": 0.60,
                "background_share": 0.20,
            },
            {
                "resolved_cited_acl_id": "C00-0001",
                "resolved_cited_title": "Middle Paper",
                "total_strong_contexts": 40,
                "evidence_use_count": 10,
                "evidence_use_share": 0.25,
                "background_share": 0.50,
            },
            {
                "resolved_cited_acl_id": "D00-0001",
                "resolved_cited_title": "High Share Paper",
                "total_strong_contexts": 25,
                "evidence_use_count": 20,
                "evidence_use_share": 0.80,
                "background_share": 0.10,
            },
            {
                "resolved_cited_acl_id": "TAIL",
                "resolved_cited_title": "One Context Tail",
                "total_strong_contexts": 1,
                "evidence_use_count": 1,
                "evidence_use_share": 1.0,
                "background_share": 0.0,
            },
            {
                "resolved_cited_acl_id": "LOW",
                "resolved_cited_title": "Low Evidence Paper",
                "total_strong_contexts": 80,
                "evidence_use_count": 2,
                "evidence_use_share": 0.025,
                "background_share": 0.90,
            },
        ]
    )


def test_plot_table_excludes_one_context_tail_artifacts_by_default() -> None:
    table = build_ranking_reversal_plot_table(_ranking_rows())

    assert "One Context Tail" not in set(table["resolved_cited_title"])


def test_plot_table_includes_only_eligible_rows() -> None:
    table = build_ranking_reversal_plot_table(_ranking_rows())

    assert table["total_strong_contexts"].ge(20).all()
    assert table["evidence_use_count"].ge(5).all()
    assert "Low Evidence Paper" not in set(table["resolved_cited_title"])


def test_plot_table_count_mode_sorts_by_absolute_rank_difference_count() -> None:
    table = build_ranking_reversal_plot_table(_ranking_rows(), mode="count")
    diffs = table["rank_difference_count"].abs().tolist()

    assert diffs == sorted(diffs, reverse=True)


def test_plot_table_shrunk_share_mode_sorts_by_absolute_rank_difference() -> None:
    table = build_ranking_reversal_plot_table(_ranking_rows(), mode="shrunk_share")
    diffs = table["rank_difference_shrunk_share"].abs().tolist()

    assert diffs == sorted(diffs, reverse=True)


def test_plot_label_is_truncated_and_non_empty() -> None:
    table = build_ranking_reversal_plot_table(_ranking_rows(), top_n=4)
    long_label = table.loc[
        table["resolved_cited_acl_id"].eq("A00-0001"),
        "plot_label",
    ].iloc[0]

    assert long_label
    assert len(long_label) <= 46
    assert long_label.endswith("...")


def test_ranking_reversal_figure_writes_png_and_svg(tmp_path) -> None:
    png = tmp_path / "ranking_reversal.png"
    svg = tmp_path / "ranking_reversal.svg"

    outputs = plot_context_volume_vs_evidence_use_reversal(_ranking_rows(), png, svg)

    assert outputs["png"] == str(png)
    assert outputs["svg"] == str(svg)
    assert outputs["plotted_rows"] == "4"
    assert png.exists()
    assert svg.exists()
    assert png.stat().st_size > 0
    assert svg.stat().st_size > 0


def test_ranking_reversal_figure_wording_uses_guarded_terms(tmp_path) -> None:
    outputs = plot_context_volume_vs_evidence_use_reversal(
        _ranking_rows(),
        tmp_path / "ranking_reversal.png",
        mode="shrunk_share",
    )
    visible_text = " ".join([outputs["title"], outputs["left_label"], outputs["right_label"]])

    assert "citation-context volume" in visible_text.casefold()
    assert "citation count" not in visible_text.casefold()
    assert "citation volume" not in visible_text.casefold()
    assert outputs["right_label"] == "Rank by shrunk evidence-use share"


def test_ranking_reversal_figure_does_not_require_local_parquet_files(
    monkeypatch,
    tmp_path,
) -> None:
    def fail_read_parquet(*_: object, **__: object) -> None:
        raise AssertionError("ranking figure should use provided DataFrames")

    monkeypatch.setattr(pd, "read_parquet", fail_read_parquet)

    table = build_ranking_reversal_plot_table(_ranking_rows())
    outputs = plot_context_volume_vs_evidence_use_reversal(
        _ranking_rows(),
        tmp_path / "ranking_reversal.png",
    )

    assert not table.empty
    assert outputs["png"].startswith(str(tmp_path))
