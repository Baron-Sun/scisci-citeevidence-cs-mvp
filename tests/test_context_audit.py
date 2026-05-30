from __future__ import annotations

from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from citeevidence.cli import app
from citeevidence.contexts.audit import (
    FLAG_COLUMNS,
    audit_citation_contexts,
    build_context_quality_flags,
)
from citeevidence.contexts.extract import CONTEXT_COLUMNS


def _write_audit_inputs(tmp_path: Path) -> tuple[Path, Path, Path, Path, Path]:
    contexts_path = tmp_path / "citation_contexts.parquet"
    sections_path = tmp_path / "acl_sections.parquet"
    references_path = tmp_path / "acl_references.parquet"
    report_path = tmp_path / "task6_context_quality_audit.md"
    flags_path = tmp_path / "task6_context_quality_flags.parquet"

    contexts = pd.DataFrame(
        [
            {
                "context_id": "ctx_1",
                "citing_paper_id": "p1",
                "reference_key": "1",
                "cited_title": "A Method",
                "cited_year": 2020,
                "cited_doi": "10.1/method",
                "section": "Methods",
                "paragraph_id": "p1-p1",
                "citation_marker": "[1]",
                "sentence_text": "We use A Method [1].",
                "context_window_s3": "We use A Method [1]. It works.",
                "context_window_paragraph": "We use A Method [1]. It works.",
                "citation_group_size": 1,
                "attribution_status": "single_citation_clear",
            },
            {
                "context_id": "ctx_1",
                "citing_paper_id": "p1",
                "reference_key": "2",
                "cited_title": None,
                "cited_year": None,
                "cited_doi": None,
                "section": "Related Work",
                "paragraph_id": "p1-p2",
                "citation_marker": "[2, 3]",
                "sentence_text": "Prior systems are similar [2, 3].",
                "context_window_s3": "Prior systems are similar [2, 3].",
                "context_window_paragraph": "Prior systems are similar [2, 3].",
                "citation_group_size": 2,
                "attribution_status": "single_citation_clear",
            },
            {
                "context_id": "ctx_3",
                "citing_paper_id": "p2",
                "reference_key": "",
                "cited_title": "Should Not Be Present",
                "cited_year": None,
                "cited_doi": None,
                "section": None,
                "paragraph_id": "p2-p1",
                "citation_marker": "[99]",
                "sentence_text": "",
                "context_window_s3": "",
                "context_window_paragraph": "Missing citation sentence [99].",
                "citation_group_size": 1,
                "attribution_status": "bibliography_unresolved",
            },
            {
                "context_id": "ctx_4",
                "citing_paper_id": "p3",
                "reference_key": "4",
                "cited_title": None,
                "cited_year": None,
                "cited_doi": None,
                "section": "Results",
                "paragraph_id": "p3-p1",
                "citation_marker": "[4]",
                "sentence_text": "We compare to a result [4].",
                "context_window_s3": "x" * 121,
                "context_window_paragraph": "We compare to a result [4].",
                "citation_group_size": 1,
                "attribution_status": "bibliography_unresolved",
            },
        ],
        columns=CONTEXT_COLUMNS,
    )
    contexts.to_parquet(contexts_path, index=False)
    pd.DataFrame(
        [
            {"paper_id": "p1", "paragraph_id": "p1-p1"},
            {"paper_id": "p2", "paragraph_id": "p2-p1"},
        ]
    ).to_parquet(sections_path, index=False)
    pd.DataFrame(
        [
            {"citing_paper_id": "p1", "reference_key": "1"},
            {"citing_paper_id": "p1", "reference_key": "2"},
        ]
    ).to_parquet(references_path, index=False)
    return contexts_path, sections_path, references_path, report_path, flags_path


def test_build_context_quality_flags() -> None:
    contexts = pd.DataFrame(
        [
            {
                "context_id": "ctx",
                "reference_key": "",
                "cited_title": "Title",
                "sentence_text": "",
                "context_window_s3": "x" * 101,
                "attribution_status": "bibliography_unresolved",
                "citation_group_size": 2,
            }
        ]
    )

    flags = build_context_quality_flags(contexts, max_window_chars=100)

    assert set(FLAG_COLUMNS) <= set(flags.columns)
    assert flags.loc[0, "flag_empty_reference_key"]
    assert flags.loc[0, "flag_empty_sentence_text"]
    assert flags.loc[0, "flag_unresolved_with_cited_title"]
    assert flags.loc[0, "flag_context_window_s3_too_long"]
    assert flags.loc[0, "flag_any"]


def test_audit_citation_contexts_writes_report_and_flags(tmp_path: Path) -> None:
    contexts_path, sections_path, references_path, report_path, flags_path = _write_audit_inputs(
        tmp_path
    )

    flags = audit_citation_contexts(
        contexts_path=contexts_path,
        sections_path=sections_path,
        references_path=references_path,
        out_report=report_path,
        flags_path=flags_path,
        max_window_chars=120,
        sample_size=3,
    )

    report = report_path.read_text(encoding="utf-8")
    loaded_flags = pd.read_parquet(flags_path)

    assert len(flags) == 4
    assert len(loaded_flags) == 4
    assert "## Core Counts" in report
    assert "duplicate_context_id_count" in report
    assert "## Null / Empty Rates" in report
    assert "## Grounding Checks" in report
    assert "## Suspicious Rows" in report
    assert "flag_single_clear_group_size_gt_1" in report
    assert int(flags["flag_any"].sum()) == 3


def test_contexts_audit_cli(tmp_path: Path) -> None:
    contexts_path, sections_path, references_path, report_path, flags_path = _write_audit_inputs(
        tmp_path
    )
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "contexts",
            "audit",
            "--contexts",
            str(contexts_path),
            "--sections",
            str(sections_path),
            "--references",
            str(references_path),
            "--out",
            str(report_path),
            "--flags",
            str(flags_path),
            "--max-window-chars",
            "120",
        ],
    )

    assert result.exit_code == 0
    assert "Wrote audit report" in result.stdout
    assert report_path.exists()
    assert pd.read_parquet(flags_path).shape[0] == 4
