from __future__ import annotations

import shutil
from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from citeevidence.acl.inspector import INVENTORY_COLUMNS, inspect_acl_ocl_data
from citeevidence.cli import app

FIXTURES = Path("tests/fixtures/acl_ocl")


def _make_acl_fixture_tree(tmp_path: Path) -> Path:
    raw_dir = tmp_path / "acl_ocl"
    shutil.copytree(FIXTURES, raw_dir)
    pd.DataFrame(
        [
            {
                "paper_id": "P3",
                "title": "Parquet Paper",
                "year": 2023,
                "section": "Discussion",
                "paragraph": "The method cites (Miller, 2021).",
                "references": "Miller 2021",
                "citation_marker": "(Miller, 2021)",
            }
        ]
    ).to_parquet(raw_dir / "table.parquet", index=False)
    return raw_dir


def test_acl_inspector_writes_inventory_and_report(tmp_path: Path) -> None:
    raw_dir = _make_acl_fixture_tree(tmp_path)
    report = tmp_path / "reports" / "acl_ocl_data_inspection.md"
    inventory_path = tmp_path / "data" / "interim" / "acl_ocl_file_inventory.parquet"

    inventory = inspect_acl_ocl_data(
        raw_dir,
        out_report=report,
        inventory_path=inventory_path,
    )

    loaded_inventory = pd.read_parquet(inventory_path)
    report_text = report.read_text(encoding="utf-8")

    assert list(inventory.columns) == INVENTORY_COLUMNS
    assert len(loaded_inventory) == 5
    assert {"GROBID XML", "JSONL", "JSON", "Parquet", "plain text"} <= set(
        loaded_inventory["likely_format"]
    )
    assert "## Files by Extension" in report_text
    assert "## Likely Formats" in report_text
    assert "## XML Inspection" in report_text
    assert "## JSON / JSONL Inspection" in report_text
    assert "## Parquet Inspection" in report_text
    assert "## Content Signals" in report_text


def test_acl_inspector_detects_xml_json_parquet_signals(tmp_path: Path) -> None:
    raw_dir = _make_acl_fixture_tree(tmp_path)
    inventory = inspect_acl_ocl_data(
        raw_dir,
        out_report=tmp_path / "report.md",
        inventory_path=tmp_path / "inventory.parquet",
    )

    xml_row = inventory.loc[inventory["relative_path"] == "paper.tei.xml"].iloc[0]
    assert xml_row["root_tag"] == "TEI"
    assert "biblStruct" in xml_row["xml_common_tags"]
    assert xml_row["contains_references"]
    assert xml_row["contains_inline_citations"]

    jsonl_row = inventory.loc[inventory["relative_path"] == "contexts.jsonl"].iloc[0]
    assert "sections" in jsonl_row["json_top_level_keys"]
    assert "references" in jsonl_row["json_top_level_keys"]
    assert jsonl_row["contains_paragraphs"]

    parquet_row = inventory.loc[inventory["relative_path"] == "table.parquet"].iloc[0]
    assert "title" in parquet_row["parquet_columns"]
    assert parquet_row["contains_title"]
    assert parquet_row["contains_year"]
    assert parquet_row["contains_sections"]

    metadata_row = inventory.loc[inventory["relative_path"] == "metadata.json"].iloc[0]
    assert metadata_row["is_metadata_file"]


def test_acl_inspect_cli(tmp_path: Path) -> None:
    raw_dir = _make_acl_fixture_tree(tmp_path)
    report = tmp_path / "report.md"
    inventory = tmp_path / "inventory.parquet"
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "acl",
            "inspect",
            "--input",
            str(raw_dir),
            "--out",
            str(report),
            "--inventory",
            str(inventory),
        ],
    )

    assert result.exit_code == 0
    assert "Inspected 5 files" in result.stdout
    assert report.exists()
    assert pd.read_parquet(inventory).shape[0] == 5
