from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from citeevidence.acl.id_audit import audit_acl_ocl_ids
from citeevidence.cli import app


def _write_acl_id_audit_fixture(tmp_path: Path) -> tuple[Path, Path, Path, Path, Path]:
    raw_dir = tmp_path / "raw" / "acl_ocl"
    interim_dir = tmp_path / "interim"
    raw_dir.mkdir(parents=True)
    interim_dir.mkdir(parents=True)
    contexts_path = tmp_path / "processed" / "citation_contexts.parquet"
    contexts_path.parent.mkdir(parents=True)
    report_path = tmp_path / "reports" / "acl_ocl_schema_id_audit.md"
    inventory_path = tmp_path / "interim" / "acl_ocl_schema_inventory.json"

    publication = pd.DataFrame(
        [
            {
                "acl_id": "P00-1013",
                "corpus_paper_id": 1001,
                "title": "Dialogue Planning",
                "year": "2000",
                "doi": "10.1/p00",
                "author": "Walker",
            },
            {
                "acl_id": "R13-1042",
                "corpus_paper_id": 1002,
                "title": "Thread Disentanglement",
                "year": "2013",
                "doi": None,
                "author": "Elsner",
            },
            {
                "acl_id": "C16-1275",
                "corpus_paper_id": 1003,
                "title": "Caption Generation",
                "year": "2016",
                "doi": "10.1/c16",
                "author": "Vinyals",
            },
        ]
    )
    publication.to_parquet(raw_dir / "acl-publication-info.74k.v2.parquet", index=False)

    graph = pd.DataFrame(
        [
            {
                "id": 9001,
                "citingpaperid": 1001,
                "citedpaperid": 1002,
                "is_citedpaperid_acl": True,
                "is_citingpaperid_acl": True,
            },
            {
                "id": 9002,
                "citingpaperid": 1003,
                "citedpaperid": 9999,
                "is_citedpaperid_acl": False,
                "is_citingpaperid_acl": True,
            },
        ]
    )
    graph.to_parquet(raw_dir / "acl_full_citations.parquet", index=False)
    graph.iloc[[0]].to_parquet(raw_dir / "acl_onlygraph.parquet", index=False)

    pd.DataFrame(
        [
            {
                "paper_id": "P00-1013",
                "title": "Dialogue Planning",
                "year": 2000,
                "venue": None,
                "doi_or_acl_id": "P00-1013",
                "source_file": "fixture",
                "parse_status": "parsed",
                "parse_error": None,
            }
        ]
    ).to_parquet(interim_dir / "acl_papers.parquet", index=False)
    pd.DataFrame(
        [
            {
                "citing_paper_id": "1001",
                "reference_key": "9001",
                "cited_title": None,
                "cited_year": None,
                "cited_authors": None,
                "cited_doi": None,
                "raw_reference": "1002",
            },
            {
                "citing_paper_id": "1003",
                "reference_key": "9002",
                "cited_title": None,
                "cited_year": None,
                "cited_authors": None,
                "cited_doi": None,
                "raw_reference": "9999",
            },
        ]
    ).to_parquet(interim_dir / "acl_references.parquet", index=False)
    pd.DataFrame(
        [
            {
                "paper_id": "P00-1013",
                "section_name": "Methods",
                "paragraph_id": "P00-1013_p0",
                "paragraph_text": "We cite prior work (Elsner, 2013).",
            }
        ]
    ).to_parquet(interim_dir / "acl_sections.parquet", index=False)
    pd.DataFrame(
        [
            {
                "context_id": "ctx_1",
                "citing_paper_id": "P00-1013",
                "reference_key": "unresolved",
                "cited_title": None,
                "cited_year": None,
                "cited_doi": None,
                "section": "Methods",
                "paragraph_id": "P00-1013_p0",
                "citation_marker": "(Elsner, 2013)",
                "sentence_text": "We cite prior work (Elsner, 2013).",
                "context_window_s3": "We cite prior work (Elsner, 2013).",
                "context_window_paragraph": "We cite prior work (Elsner, 2013).",
                "citation_group_size": 1,
                "attribution_status": "bibliography_unresolved",
            }
        ]
    ).to_parquet(contexts_path, index=False)

    return raw_dir, interim_dir, contexts_path, report_path, inventory_path


def test_audit_acl_ocl_ids_detects_crosswalk(tmp_path: Path) -> None:
    raw_dir, interim_dir, contexts_path, report_path, inventory_path = (
        _write_acl_id_audit_fixture(tmp_path)
    )

    inventory = audit_acl_ocl_ids(
        raw_dir=raw_dir,
        interim_dir=interim_dir,
        contexts_path=contexts_path,
        out_report=report_path,
        inventory_path=inventory_path,
        sample_rows=20,
        join_examples=2,
    )

    report = report_path.read_text(encoding="utf-8")
    loaded_inventory = json.loads(inventory_path.read_text(encoding="utf-8"))

    assert inventory["publication_crosswalk"]["exact_column_check"]["both_present"]
    assert inventory["publication_crosswalk"]["acl_column"] == "acl_id"
    assert inventory["publication_crosswalk"]["numeric_column"] == "corpus_paper_id"
    assert inventory["successful_candidate_join_examples"][0]["citing_acl_id"] == "P00-1013"
    assert inventory["successful_candidate_join_examples"][0]["cited_acl_id"] == "R13-1042"
    assert inventory["failed_candidate_join_examples"][0]["cited_numeric_id"] == "9999"
    assert "corpus_paper_id" in report
    assert "Authoritative crosswalk" in report
    assert loaded_inventory["publication_crosswalk"]["rows"] == 3


def test_acl_audit_ids_cli(tmp_path: Path) -> None:
    raw_dir, interim_dir, contexts_path, report_path, inventory_path = (
        _write_acl_id_audit_fixture(tmp_path)
    )
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "acl",
            "audit-ids",
            "--raw-dir",
            str(raw_dir),
            "--interim-dir",
            str(interim_dir),
            "--contexts",
            str(contexts_path),
            "--out",
            str(report_path),
            "--inventory",
            str(inventory_path),
        ],
    )

    assert result.exit_code == 0
    assert "Wrote ACL-OCL ID audit report" in result.stdout
    assert report_path.exists()
    assert inventory_path.exists()
