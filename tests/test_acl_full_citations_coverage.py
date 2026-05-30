from __future__ import annotations

from pathlib import Path

import pandas as pd

from citeevidence.acl.full_citations_coverage import (
    SAFE_ALIGNED_COLUMNS,
    evaluate_full_citations_candidate_coverage,
)


def test_evaluate_full_citations_candidate_coverage(tmp_path: Path) -> None:
    publication_info = tmp_path / "publication.parquet"
    full_citations = tmp_path / "acl_full_citations.parquet"
    onlygraph_aligned = tmp_path / "acl_citation_graph_aligned.parquet"
    resolved = tmp_path / "citation_contexts_resolved_pilot.parquet"
    contexts = tmp_path / "citation_contexts.parquet"
    out_safe = tmp_path / "acl_full_citations_safe_aligned.parquet"
    report = tmp_path / "full_citations_candidate_coverage_report.md"

    pd.DataFrame(
        [
            _publication("P1", 1, "Citing One", 2024, "Tester, T"),
            _publication("P4", 4, "Additional Citing", 2024, "Tester, U"),
            _publication("C0", 13, "Old Candidate", 2019, "Doe, Jane"),
            _publication("C1", 10, "Smith Candidate A", 2020, "Smith, Alice"),
            _publication("C2", 11, "Jones Candidate", 2021, "Jones, Bob"),
            _publication("C3", 12, "Smith Candidate B", 2020, "Smith, Carol"),
            _publication("C5", 14, "Extra Cited", 2022, "Extra, Erin"),
        ]
    ).to_parquet(publication_info, index=False)
    pd.DataFrame(
        [
            _full_edge(100, 1, 10),
            _full_edge(101, 1, 11),
            _full_edge(102, 1, 12),
            _full_edge(103, 4, 14),
            _full_edge(104, 1, 999999),
        ]
    ).to_parquet(full_citations, index=False)
    pd.DataFrame(
        [
            {
                "graph_edge_id": 1,
                "citing_acl_id": "P1",
                "citing_corpus_paper_id": 1,
                "citing_title": "Citing One",
                "citing_year": "2024",
                "citing_authors": "Tester, T",
                "citing_doi": None,
                "cited_acl_id": "C0",
                "cited_corpus_paper_id": 13,
                "cited_title": "Old Candidate",
                "cited_year": "2019",
                "cited_authors": "Doe, Jane",
                "cited_doi": None,
            }
        ]
    ).to_parquet(onlygraph_aligned, index=False)
    pd.DataFrame(
        [
            _resolved_row("ctx_smith", "P1", "(Smith, 2020)", "smith", "2020"),
            _resolved_row("ctx_jones", "P1", "(Jones, 2021)", "jones", "2021"),
            _resolved_row("ctx_numeric", "P1", "[1]", "", None),
        ]
    ).to_parquet(resolved, index=False)
    pd.DataFrame([{"context_id": "ctx_smith"}]).to_parquet(contexts, index=False)

    result = evaluate_full_citations_candidate_coverage(
        full_citations_path=full_citations,
        publication_info_path=publication_info,
        onlygraph_aligned_path=onlygraph_aligned,
        resolved_pilot_path=resolved,
        contexts_path=contexts,
        out_safe_aligned=out_safe,
        report_path=report,
    )

    safe = pd.read_parquet(out_safe)
    report_text = report.read_text(encoding="utf-8")
    coverage = result.metrics["unresolved_author_year_coverage"]

    assert list(safe.columns) == SAFE_ALIGNED_COLUMNS
    assert len(safe) == 4
    assert set(safe["candidate_source"]) == {"full_citations"}
    assert result.metrics["additional_candidate_edges_beyond_onlygraph"] == 4
    assert result.metrics["additional_citing_acl_papers"] == 1
    assert coverage["bibliography_unresolved_author_year_rows"] == 2
    assert coverage["gain_same_year_candidate_rows"] == 2
    assert coverage["gain_same_year_surname_candidate_rows"] == 2
    assert coverage["become_ambiguous_surname_rows"] == 1
    assert "Risk Analysis" in report_text


def _publication(
    acl_id: str,
    corpus_paper_id: int,
    title: str,
    year: int,
    author: str,
) -> dict[str, object]:
    return {
        "acl_id": acl_id,
        "corpus_paper_id": corpus_paper_id,
        "title": title,
        "year": str(year),
        "author": author,
        "doi": None,
    }


def _full_edge(edge_id: int, citing: int, cited: int) -> dict[str, object]:
    return {
        "id": edge_id,
        "citingpaperid": citing,
        "citedpaperid": cited,
        "is_citedpaperid_acl": True,
        "is_citingpaperid_acl": True,
    }


def _resolved_row(
    context_id: str,
    citing_paper_id: str,
    marker: str,
    surnames: str,
    year: str | None,
) -> dict[str, object]:
    return {
        "context_id": f"resolved_{context_id}",
        "source_context_id": context_id,
        "citing_paper_id": citing_paper_id,
        "citation_marker": marker,
        "marker_component_text": marker.strip("()"),
        "parsed_surnames": surnames,
        "parsed_year": year,
        "resolution_status": "bibliography_unresolved",
        "resolution_method": "author_year_no_candidate",
        "sentence_text": f"Prior work {marker} is discussed.",
    }
