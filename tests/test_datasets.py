from __future__ import annotations

from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from citeevidence.cli import app
from citeevidence.datasets.multicite import load_multicite
from citeevidence.datasets.normalize import NORMALIZED_COLUMNS, write_labeled_contexts
from citeevidence.datasets.scicite import load_scicite

FIXTURES = Path("tests/fixtures")


def test_load_multicite_jsonl_fixture() -> None:
    frame = load_multicite(FIXTURES / "multicite")

    assert list(frame.columns) == NORMALIZED_COLUMNS
    assert len(frame) == 2
    assert frame.loc[frame["original_label"] == "Uses", "normalized_intent"].item() == "uses"

    differences = frame.loc[frame["original_label"] == "Differences"].iloc[0]
    assert differences["normalized_intent"] == "critiques"
    assert "Differences mapped to critiques" in differences["mapping_notes"]


def test_load_scicite_csv_fixture() -> None:
    frame = load_scicite(FIXTURES / "scicite")

    assert len(frame) == 3
    method = frame.loc[frame["original_label"] == "method"].iloc[0]
    assert method["normalized_intent"] == "uses"
    assert method["normalized_object_type"] == "method"

    result = frame.loc[frame["original_label"] == "result"].iloc[0]
    assert result["normalized_intent"] == "compares_against"
    assert result["is_multisentence"] == 1


def test_write_labeled_contexts_parquet_and_report(tmp_path: Path) -> None:
    out = tmp_path / "labeled_contexts.parquet"
    report = tmp_path / "labeled_dataset_profile.md"

    combined = write_labeled_contexts(
        [
            load_multicite(FIXTURES / "multicite"),
            load_scicite(FIXTURES / "scicite"),
        ],
        out_path=out,
        report_path=report,
    )

    loaded = pd.read_parquet(out)
    report_text = report.read_text(encoding="utf-8")

    assert len(combined) == 5
    assert len(loaded) == 5
    assert "## Number of Contexts by Dataset" in report_text
    assert "## Original Label Distribution" in report_text
    assert "## Normalized Label Distribution" in report_text
    assert "## Section Distribution" in report_text
    assert "## Multisentence Rate" in report_text


def test_datasets_load_labeled_cli(tmp_path: Path) -> None:
    runner = CliRunner()
    out = tmp_path / "labeled_contexts.parquet"
    report = tmp_path / "profile.md"

    result = runner.invoke(
        app,
        [
            "datasets",
            "load-labeled",
            "--multicite",
            str(FIXTURES / "multicite"),
            "--scicite",
            str(FIXTURES / "scicite"),
            "--out",
            str(out),
            "--report",
            str(report),
        ],
    )

    assert result.exit_code == 0
    assert "Wrote 5 labeled contexts" in result.stdout
    assert pd.read_parquet(out).shape[0] == 5
    assert report.exists()
