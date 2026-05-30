from __future__ import annotations

import shutil
from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from citeevidence.acl.reader import (
    PAPER_COLUMNS,
    REFERENCE_COLUMNS,
    SECTION_COLUMNS,
    parse_acl_ocl_data,
)
from citeevidence.cli import app

FIXTURES = Path("tests/fixtures/acl_ocl")


def _make_reader_fixture_tree(tmp_path: Path) -> Path:
    raw_dir = tmp_path / "acl_ocl"
    shutil.copytree(FIXTURES, raw_dir)
    (raw_dir / "structured.json").write_text(
        """
{
  "paper_id": "P-json",
  "title": "Structured JSON Paper",
  "year": 2021,
  "venue": "ACL",
  "doi": "10.0000/json",
  "sections": [
    {
      "heading": "Introduction",
      "paragraphs": [
        {"paragraph_id": "json-p1", "text": "This paper cites prior work (Smith, 2020)."}
      ]
    }
  ],
  "references": [
    {
      "id": "R-json",
      "title": "Prior Work",
      "year": 2020,
      "authors": ["A. Smith"],
      "doi": "10.0000/ref",
      "raw": "Smith. 2020. Prior Work."
    }
  ]
}
""",
        encoding="utf-8",
    )
    pd.DataFrame(
        [
            {
                "paper_id": "P-parquet",
                "title": "Parquet Paper",
                "year": 2023,
                "venue": "EMNLP",
                "doi": "10.0000/parquet",
                "section": "Discussion",
                "paragraph_text": "The method cites (Miller, 2021).",
                "reference_key": "R-parquet",
                "cited_title": "Parquet Reference",
                "cited_year": 2021,
                "cited_authors": "Miller",
                "cited_doi": "10.0000/parquet-ref",
                "raw_reference": "Miller. 2021. Parquet Reference.",
            }
        ]
    ).to_parquet(raw_dir / "table.parquet", index=False)
    pd.DataFrame(
        [
            {
                "id": 1001,
                "citingpaperid": 111,
                "citedpaperid": 222,
                "is_citedpaperid_acl": True,
                "is_citingpaperid_acl": True,
            },
            {
                "id": 1002,
                "citingpaperid": 111,
                "citedpaperid": 333,
                "is_citedpaperid_acl": False,
                "is_citingpaperid_acl": True,
            },
        ]
    ).to_parquet(raw_dir / "z_citation_edges.parquet", index=False)
    (raw_dir / "bad.json").write_text('{"not valid": ', encoding="utf-8")
    (raw_dir / "raw.pdf").write_bytes(b"%PDF-1.4 fixture")
    return raw_dir


def test_parse_acl_ocl_data_writes_three_tables(tmp_path: Path) -> None:
    raw_dir = _make_reader_fixture_tree(tmp_path)
    out_dir = tmp_path / "interim"

    result = parse_acl_ocl_data(raw_dir, out_dir=out_dir)

    papers = pd.read_parquet(out_dir / "acl_papers.parquet")
    references = pd.read_parquet(out_dir / "acl_references.parquet")
    sections = pd.read_parquet(out_dir / "acl_sections.parquet")

    assert list(result.papers.columns) == PAPER_COLUMNS
    assert list(result.references.columns) == REFERENCE_COLUMNS
    assert list(result.sections.columns) == SECTION_COLUMNS
    assert list(papers.columns) == PAPER_COLUMNS
    assert list(references.columns) == REFERENCE_COLUMNS
    assert list(sections.columns) == SECTION_COLUMNS
    assert len(papers) == 9
    assert len(references) >= 7
    assert len(sections) >= 6


def test_parse_acl_ocl_data_extracts_tei_json_parquet_and_text(tmp_path: Path) -> None:
    raw_dir = _make_reader_fixture_tree(tmp_path)
    result = parse_acl_ocl_data(raw_dir, out_dir=tmp_path / "interim")

    tei_paper = result.papers.loc[result.papers["source_file"] == "paper.tei.xml"].iloc[0]
    assert tei_paper["title"] == "Neural Citation Contexts"
    assert tei_paper["year"] == 2020
    assert tei_paper["parse_status"] == "parsed"

    tei_reference = result.references.loc[
        result.references["citing_paper_id"] == tei_paper["paper_id"]
    ].iloc[0]
    assert tei_reference["cited_title"] == "Attention Is All You Need"
    assert tei_reference["cited_year"] == 2017

    json_paper = result.papers.loc[result.papers["paper_id"] == "P-json"].iloc[0]
    assert json_paper["doi_or_acl_id"] == "10.0000/json"
    assert "json-p1" in set(result.sections["paragraph_id"])
    assert "R-json" in set(result.references["reference_key"])

    parquet_paper = result.papers.loc[result.papers["paper_id"] == "P-parquet"].iloc[0]
    assert parquet_paper["venue"] == "EMNLP"
    assert "R-parquet" in set(result.references["reference_key"])

    edge_references = result.references.loc[
        result.references["reference_key"].isin(["1001", "1002"])
    ]
    assert len(edge_references) == 2
    assert set(edge_references["citing_paper_id"]) == {"111"}

    text_paper = result.papers.loc[result.papers["source_file"] == "plain.txt"].iloc[0]
    assert text_paper["title"] == "Plain Text Paper"
    assert result.sections.loc[
        result.sections["paper_id"] == text_paper["paper_id"],
        "paragraph_text",
    ].str.contains("prior sequence tagging").any()


def test_parse_acl_ocl_data_records_bad_files_and_skips_pdf(tmp_path: Path) -> None:
    raw_dir = _make_reader_fixture_tree(tmp_path)
    result = parse_acl_ocl_data(raw_dir, out_dir=tmp_path / "interim")

    bad = result.papers.loc[result.papers["source_file"] == "bad.json"].iloc[0]
    assert bad["parse_status"] == "error"
    assert "JSONDecodeError" in bad["parse_error"]

    pdf = result.papers.loc[result.papers["source_file"] == "raw.pdf"].iloc[0]
    assert pdf["parse_status"] == "skipped_pdf"
    assert "raw PDFs are not stored" in pdf["parse_error"]


def test_parse_acl_ocl_data_respects_max_files(tmp_path: Path) -> None:
    raw_dir = _make_reader_fixture_tree(tmp_path)
    result = parse_acl_ocl_data(raw_dir, out_dir=tmp_path / "interim", max_files=2)

    assert set(result.papers["source_file"]) <= {"bad.json", "contexts.jsonl"}
    assert "paper.tei.xml" not in set(result.papers["source_file"])


def test_acl_parse_cli(tmp_path: Path) -> None:
    raw_dir = _make_reader_fixture_tree(tmp_path)
    out_dir = tmp_path / "interim"
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "acl",
            "parse",
            "--input",
            str(raw_dir),
            "--max-files",
            "100",
            "--out-dir",
            str(out_dir),
        ],
    )

    assert result.exit_code == 0
    assert "Wrote 9 papers" in result.stdout
    assert (out_dir / "acl_papers.parquet").exists()
    assert (out_dir / "acl_references.parquet").exists()
    assert (out_dir / "acl_sections.parquet").exists()
