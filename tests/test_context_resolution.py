from __future__ import annotations

from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from citeevidence.cli import app
from citeevidence.contexts.extract import CONTEXT_COLUMNS
from citeevidence.contexts.resolve import OUTPUT_COLUMNS, resolve_citation_markers_pilot


def _context_row(context_id: str, citing_paper_id: str, marker: str) -> dict[str, object]:
    sentence = f"This sentence cites prior work {marker}."
    return {
        "context_id": context_id,
        "citing_paper_id": citing_paper_id,
        "reference_key": "unresolved",
        "cited_title": None,
        "cited_year": None,
        "cited_doi": None,
        "section": "Related Work",
        "paragraph_id": f"{citing_paper_id}_p0",
        "citation_marker": marker,
        "sentence_text": sentence,
        "context_window_s3": sentence,
        "context_window_paragraph": sentence,
        "citation_group_size": 1,
        "attribution_status": "bibliography_unresolved",
    }


def _write_resolution_inputs(tmp_path: Path) -> tuple[Path, Path, Path, Path, Path, Path]:
    contexts_path = tmp_path / "citation_contexts.parquet"
    graph_path = tmp_path / "acl_citation_graph_aligned.parquet"
    crosswalk_path = tmp_path / "acl_id_crosswalk.parquet"
    out_path = tmp_path / "citation_contexts_resolved_pilot.parquet"
    failures_path = tmp_path / "citation_marker_resolution_pilot_failures.parquet"
    report_path = tmp_path / "citation_marker_resolution_pilot_report.md"

    contexts = pd.DataFrame(
        [
            _context_row("ctx_vinyals", "P1", "(Vinyals et al., 2014)"),
            _context_row("ctx_elsner", "P1", "(Elsner and Charniak, 2010)"),
            _context_row("ctx_group", "P1", "(Yeh, 2006; Erera and Carmel, 2008)"),
            _context_row("ctx_year_unique", "P1", "(2021)"),
            _context_row("ctx_year_amb", "P1", "(2011)"),
            _context_row("ctx_numeric", "P1", "[1, 2]"),
            _context_row("ctx_no_graph", "NO-GRAPH", "(Smith, 2020)"),
            _context_row("ctx_ambiguous", "P1", "(Smith, 2020)"),
            _context_row("ctx_dup", "P1", "(Vinyals et al., 2014)"),
            _context_row("ctx_dup", "P1", "(Elsner and Charniak, 2010)"),
            _context_row("ctx_malformed", "P1", "(not a citation)"),
        ],
        columns=CONTEXT_COLUMNS,
    )
    contexts.to_parquet(contexts_path, index=False)

    graph = pd.DataFrame(
        [
            _candidate("P1", "C1", 101, "Show and Tell", 2014, "Vinyals, Oriol"),
            _candidate(
                "P1",
                "C2",
                102,
                "Disentangling Chat",
                2010,
                "Elsner, Micha and Charniak, Eugene",
            ),
            _candidate("P1", "C3", 103, "Thread Emails", 2006, "Yeh, Alexander"),
            _candidate("P1", "C4", 104, "Email Threads", 2008, "Erera, Shai and Carmel, David"),
            _candidate("P1", "C5", 105, "Unique Year", 2021, "Unique, Uma"),
            _candidate("P1", "C6", 106, "First 2011", 2011, "Doe, Jane"),
            _candidate("P1", "C7", 107, "Second 2011", 2011, "Roe, Richard"),
            _candidate("P1", "C8", 108, "First Smith", 2020, "Smith, Ann"),
            _candidate("P1", "C9", 109, "Second Smith", 2020, "Smith, Bob"),
        ]
    )
    graph.to_parquet(graph_path, index=False)
    pd.DataFrame(
        [
            {
                "acl_id": "P1",
                "corpus_paper_id": 1,
                "title": "Citing",
                "year": "2024",
                "authors": "Tester",
                "doi": None,
                "venue": "ACL",
                "url": None,
                "numcitedby": 0,
            }
        ]
    ).to_parquet(crosswalk_path, index=False)
    return contexts_path, graph_path, crosswalk_path, out_path, failures_path, report_path


def _candidate(
    citing_acl_id: str,
    cited_acl_id: str,
    cited_corpus_paper_id: int,
    cited_title: str,
    cited_year: int,
    cited_authors: str,
) -> dict[str, object]:
    return {
        "graph_edge_id": cited_corpus_paper_id,
        "citing_acl_id": citing_acl_id,
        "citing_corpus_paper_id": 1,
        "citing_title": "Citing Paper",
        "citing_year": "2024",
        "citing_authors": "Tester",
        "citing_doi": None,
        "cited_acl_id": cited_acl_id,
        "cited_corpus_paper_id": cited_corpus_paper_id,
        "cited_title": cited_title,
        "cited_year": str(cited_year),
        "cited_authors": cited_authors,
        "cited_doi": f"10.1/{cited_acl_id.lower()}",
        "is_citingpaperid_acl": True,
        "is_citedpaperid_acl": True,
        "alignment_status": "both_aligned",
    }


def test_resolve_citation_markers_pilot_rules(tmp_path: Path) -> None:
    contexts_path, graph_path, crosswalk_path, out_path, failures_path, report_path = (
        _write_resolution_inputs(tmp_path)
    )

    metrics = resolve_citation_markers_pilot(
        contexts_path=contexts_path,
        aligned_graph_path=graph_path,
        crosswalk_path=crosswalk_path,
        out_path=out_path,
        failures_path=failures_path,
        report_path=report_path,
        limit=100,
    )

    resolved = pd.read_parquet(out_path)
    report = report_path.read_text(encoding="utf-8")

    assert list(resolved.columns) == OUTPUT_COLUMNS
    assert resolved["context_id"].is_unique
    assert metrics["duplicate_context_id_before"] == 1
    assert metrics["duplicate_context_id_after"] == 0
    assert _status_for(resolved, "ctx_vinyals") == "author_year_clear"
    assert _status_for(resolved, "ctx_elsner") == "author_year_clear"
    assert _status_for(resolved, "ctx_year_unique") == "year_only_unique_candidate"
    assert _row_for(resolved, "ctx_year_unique")["resolution_confidence"] <= 0.60
    assert _status_for(resolved, "ctx_year_amb") == "ambiguous_year_only"
    assert _status_for(resolved, "ctx_numeric") == "numeric_marker_unresolved_no_bibliography"
    assert _status_for(resolved, "ctx_no_graph") == "citing_paper_not_in_aligned_graph"
    assert _status_for(resolved, "ctx_ambiguous") == "multi_candidate_ambiguous"
    assert _status_for(resolved, "ctx_malformed") == "bibliography_unresolved"
    assert resolved.loc[resolved["source_context_id"].eq("ctx_group")].shape[0] == 2
    group_statuses = set(
        resolved.loc[resolved["source_context_id"].eq("ctx_group"), "resolution_status"]
    )
    assert group_statuses == {
        "author_year_clear"
    }
    assert pd.read_parquet(failures_path)["resolution_status"].ne("author_year_clear").all()
    assert "resolved_cited_title non-empty rate" in report


def test_resolve_markers_cli(tmp_path: Path) -> None:
    contexts_path, graph_path, crosswalk_path, out_path, failures_path, report_path = (
        _write_resolution_inputs(tmp_path)
    )
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "contexts",
            "resolve-markers",
            "--contexts",
            str(contexts_path),
            "--aligned-graph",
            str(graph_path),
            "--crosswalk",
            str(crosswalk_path),
            "--out",
            str(out_path),
            "--failures",
            str(failures_path),
            "--report",
            str(report_path),
            "--limit",
            "100",
        ],
    )

    assert result.exit_code == 0
    assert "Processed 11 contexts" in result.stdout
    assert out_path.exists()
    assert failures_path.exists()
    assert report_path.exists()


def _row_for(frame: pd.DataFrame, source_context_id: str) -> pd.Series:
    return frame.loc[frame["source_context_id"].eq(source_context_id)].iloc[0]


def _status_for(frame: pd.DataFrame, source_context_id: str) -> str:
    return str(_row_for(frame, source_context_id)["resolution_status"])
