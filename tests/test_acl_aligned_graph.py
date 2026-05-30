from __future__ import annotations

from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from citeevidence.acl.aligned_graph import (
    ALIGNED_GRAPH_COLUMNS,
    CROSSWALK_COLUMNS,
    build_aligned_acl_citation_graph,
)
from citeevidence.cli import app


def _write_aligned_graph_inputs(tmp_path: Path) -> tuple[Path, Path, Path, Path, Path, Path]:
    publication_path = tmp_path / "acl-publication-info.74k.v2.parquet"
    onlygraph_path = tmp_path / "acl_onlygraph.parquet"
    contexts_path = tmp_path / "citation_contexts.parquet"
    out_crosswalk = tmp_path / "acl_id_crosswalk.parquet"
    out_graph = tmp_path / "acl_citation_graph_aligned.parquet"
    report_path = tmp_path / "acl_citation_graph_alignment_report.md"

    pd.DataFrame(
        [
            {
                "acl_id": "P00-1013",
                "corpus_paper_id": 1001,
                "title": "Dialogue Planning",
                "year": "2000",
                "author": "Walker",
                "doi": "10.1/p00",
                "booktitle": "ACL",
                "url": "https://aclanthology.org/P00-1013",
                "numcitedby": 7,
            },
            {
                "acl_id": "R13-1042",
                "corpus_paper_id": 1002,
                "title": "Thread Disentanglement",
                "year": "2013",
                "author": "Elsner",
                "doi": None,
                "booktitle": "RANLP",
                "url": "https://aclanthology.org/R13-1042",
                "numcitedby": 13,
            },
        ]
    ).to_parquet(publication_path, index=False)
    pd.DataFrame(
        [
            {
                "id": 1,
                "citingpaperid": 1001,
                "citedpaperid": 1002,
                "is_citingpaperid_acl": True,
                "is_citedpaperid_acl": True,
            },
            {
                "id": 2,
                "citingpaperid": 9998,
                "citedpaperid": 1002,
                "is_citingpaperid_acl": False,
                "is_citedpaperid_acl": True,
            },
            {
                "id": 3,
                "citingpaperid": 1001,
                "citedpaperid": 9999,
                "is_citingpaperid_acl": True,
                "is_citedpaperid_acl": False,
            },
        ]
    ).to_parquet(onlygraph_path, index=False)
    pd.DataFrame(
        [
            {
                "context_id": "ctx_1",
                "citing_paper_id": "P00-1013",
                "paragraph_id": "P00-1013_p0",
                "citation_marker": "(Elsner, 2013)",
                "sentence_text": "We cite thread disentanglement (Elsner, 2013).",
            },
            {
                "context_id": "ctx_2",
                "citing_paper_id": "C16-1275",
                "paragraph_id": "C16-1275_p0",
                "citation_marker": "[1]",
                "sentence_text": "An uncovered paper cites something [1].",
            },
        ]
    ).to_parquet(contexts_path, index=False)
    return publication_path, onlygraph_path, contexts_path, out_crosswalk, out_graph, report_path


def test_build_aligned_acl_citation_graph_outputs_schema_and_statuses(tmp_path: Path) -> None:
    publication_path, onlygraph_path, contexts_path, out_crosswalk, out_graph, report_path = (
        _write_aligned_graph_inputs(tmp_path)
    )

    metrics = build_aligned_acl_citation_graph(
        publication_info_path=publication_path,
        onlygraph_path=onlygraph_path,
        contexts_path=contexts_path,
        out_crosswalk=out_crosswalk,
        out_graph=out_graph,
        report_path=report_path,
    )

    crosswalk = pd.read_parquet(out_crosswalk)
    graph = pd.read_parquet(out_graph)
    report = report_path.read_text(encoding="utf-8")

    assert list(crosswalk.columns) == CROSSWALK_COLUMNS
    assert list(graph.columns) == ALIGNED_GRAPH_COLUMNS
    assert set(graph["alignment_status"]) == {
        "both_aligned",
        "missing_citing",
        "missing_cited",
    }
    assert metrics["aligned_graph_edges"] == 1
    assert metrics["both_sides_alignment_rate"] == "0.333"
    assert metrics["citation_contexts_citing_paper_id_coverage"] == "0.500"
    assert "both sides alignment rate" in report
    assert "C16-1275" in report


def test_build_aligned_graph_cli(tmp_path: Path) -> None:
    publication_path, onlygraph_path, contexts_path, out_crosswalk, out_graph, report_path = (
        _write_aligned_graph_inputs(tmp_path)
    )
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "acl",
            "build-aligned-graph",
            "--publication-info",
            str(publication_path),
            "--onlygraph",
            str(onlygraph_path),
            "--contexts",
            str(contexts_path),
            "--out-crosswalk",
            str(out_crosswalk),
            "--out-graph",
            str(out_graph),
            "--report",
            str(report_path),
        ],
    )

    assert result.exit_code == 0
    assert "Wrote 2 crosswalk rows" in result.stdout
    assert out_crosswalk.exists()
    assert out_graph.exists()
    assert report_path.exists()
