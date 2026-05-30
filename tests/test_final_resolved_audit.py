from __future__ import annotations

from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from citeevidence.cli import app
from citeevidence.contexts.final_audit import (
    FLAG_COLUMNS,
    MANUAL_SAMPLE_COLUMNS,
    STRONG_SAMPLE_COLUMNS,
    audit_final_resolved_contexts,
    build_analysis_ready_strong_contexts,
    build_final_resolved_quality_flags,
)
from citeevidence.contexts.resolve import OUTPUT_COLUMNS


def _resolved_row(
    context_id: str,
    *,
    source_context_id: str | None = None,
    normalized_section: str = "method",
    marker_type: str = "parenthetical_author_year",
    resolution_status: str = "author_year_clear",
    resolution_level: str = "strong_author_year",
    is_strongly_resolved: bool = True,
    citation_marker: str = "(Smith, 2020)",
    sentence_text: str | None = None,
    context_window_s3: str | None = None,
    suspicious_citation_range_flag: bool = False,
    large_citation_group_flag: bool = False,
    resolved_cited_title: str | None = "A Strong Paper",
    resolved_cited_year: str | None = "2020",
    resolved_cited_authors: str | None = "Smith",
) -> dict[str, object]:
    sentence = sentence_text or f"We use prior work {citation_marker}."
    window = context_window_s3 or f"Earlier sentence. {sentence} Later sentence."
    return {
        "context_id": context_id,
        "citing_paper_id": "P00-0001",
        "reference_key": "",
        "cited_title": None,
        "cited_year": None,
        "cited_doi": None,
        "raw_section_name": normalized_section.title(),
        "normalized_section": normalized_section,
        "section": normalized_section.title(),
        "paragraph_id": f"{context_id}_p0",
        "citation_marker": citation_marker,
        "marker_start_offset": 0,
        "marker_end_offset": len(citation_marker),
        "marker_type": marker_type,
        "sentence_text": sentence,
        "context_window_s3": window,
        "context_window_paragraph": window,
        "citation_group_size": 1,
        "large_citation_group_flag": large_citation_group_flag,
        "very_large_citation_group_flag": False,
        "suspicious_citation_range_flag": suspicious_citation_range_flag,
        "attribution_status": "bibliography_unresolved",
        "source_context_id": source_context_id or context_id,
        "marker_component_index": 0,
        "marker_component_text": citation_marker.strip("()"),
        "parsed_surnames": "smith",
        "parsed_year": "2020",
        "parsed_year_suffix": None,
        "candidate_count_for_citing_paper": 1,
        "matched_candidate_count": 1,
        "matched_candidate_acl_ids": "P00-0002",
        "resolved_cited_acl_id": "P00-0002",
        "resolved_cited_corpus_paper_id": 123,
        "resolved_cited_title": resolved_cited_title,
        "resolved_cited_year": resolved_cited_year,
        "resolved_cited_authors": resolved_cited_authors,
        "resolved_cited_doi": None,
        "resolution_status": resolution_status,
        "resolution_confidence": 0.95,
        "resolution_method": "fixture",
        "resolution_level": resolution_level,
        "is_strongly_resolved": is_strongly_resolved,
    }


def _fixture_frame() -> pd.DataFrame:
    rows = [
        _resolved_row("eligible"),
        _resolved_row("dup", source_context_id="dup_a"),
        _resolved_row("dup", source_context_id="dup_b"),
        _resolved_row(
            "marker_bad",
            citation_marker="(Missing, 2020)",
            sentence_text="We cite something else (Smith, 2020).",
            is_strongly_resolved=False,
            resolution_status="bibliography_unresolved",
            resolution_level="unresolved",
            resolved_cited_title=None,
            resolved_cited_year=None,
            resolved_cited_authors=None,
        ),
        _resolved_row(
            "window_bad",
            sentence_text="This sentence is not in the window (Smith, 2020).",
            context_window_s3="A different bounded context.",
            is_strongly_resolved=False,
            resolution_status="bibliography_unresolved",
            resolution_level="unresolved",
            resolved_cited_title=None,
            resolved_cited_year=None,
            resolved_cited_authors=None,
        ),
        _resolved_row("numeric_bad", marker_type="numeric", citation_marker="[12]"),
        _resolved_row("year_bad", marker_type="year_only", citation_marker="(2020)"),
        _resolved_row("range_bad", suspicious_citation_range_flag=True),
        _resolved_row("large_bad", large_citation_group_flag=True),
        _resolved_row("references_bad", normalized_section="references"),
        _resolved_row(
            "not_strong_clear",
            resolution_status="author_year_clear",
            resolution_level="unresolved",
            is_strongly_resolved=False,
        ),
        _resolved_row(
            "bibliography_unresolved",
            resolution_status="bibliography_unresolved",
            resolution_level="unresolved",
            is_strongly_resolved=False,
            resolved_cited_title=None,
            resolved_cited_year=None,
            resolved_cited_authors=None,
        ),
        _resolved_row(
            "ambiguous",
            resolution_status="multi_candidate_ambiguous",
            resolution_level="ambiguous",
            is_strongly_resolved=False,
            resolved_cited_title=None,
            resolved_cited_year=None,
            resolved_cited_authors=None,
        ),
        _resolved_row(
            "numeric_unresolved",
            marker_type="numeric",
            citation_marker="[5]",
            resolution_status="numeric_marker_unresolved_no_bibliography",
            resolution_level="numeric_unresolved",
            is_strongly_resolved=False,
            resolved_cited_title=None,
            resolved_cited_year=None,
            resolved_cited_authors=None,
        ),
        _resolved_row(
            "weak",
            resolution_status="year_only_unique_candidate",
            resolution_level="weak_year_only",
            is_strongly_resolved=False,
        ),
    ]
    return pd.DataFrame(rows, columns=OUTPUT_COLUMNS)


def _write_fixture(tmp_path: Path) -> Path:
    path = tmp_path / "citation_contexts_resolved.parquet"
    _fixture_frame().to_parquet(path, index=False)
    return path


def test_final_resolved_quality_flags() -> None:
    frame = _fixture_frame()

    flags = build_final_resolved_quality_flags(frame)

    assert set(FLAG_COLUMNS) <= set(flags.columns)
    assert flags.loc[flags["context_id"].eq("dup"), "duplicate_context_id"].all()
    assert _flag_for(flags, "marker_bad", "marker_not_in_sentence")
    assert _flag_for(flags, "window_bad", "sentence_not_in_context_window")
    assert _flag_for(flags, "numeric_bad", "strong_numeric_marker")
    assert _flag_for(flags, "year_bad", "strong_year_only_marker")
    assert _flag_for(flags, "range_bad", "strong_suspicious_citation_range")
    assert _flag_for(flags, "large_bad", "strong_large_citation_group")
    assert _flag_for(flags, "references_bad", "strong_in_references_section")
    assert _flag_for(flags, "not_strong_clear", "author_year_clear_not_strong")


def test_analysis_ready_filters_to_eligible_strong_rows() -> None:
    analysis_ready = build_analysis_ready_strong_contexts(_fixture_frame())

    assert "eligible" in set(analysis_ready["context_id"])
    assert "references_bad" not in set(analysis_ready["context_id"])
    assert not analysis_ready["marker_type"].isin({"numeric", "year_only"}).any()
    assert not analysis_ready["suspicious_citation_range_flag"].any()
    assert not analysis_ready["large_citation_group_flag"].any()
    assert analysis_ready["is_strongly_resolved"].all()


def test_audit_final_resolved_contexts_writes_outputs(tmp_path: Path) -> None:
    resolved_path = _write_fixture(tmp_path)
    report_path = tmp_path / "final_resolved_context_audit.md"
    flags_path = tmp_path / "final_resolved_context_quality_flags.parquet"
    strong_sample_path = tmp_path / "strong_resolved_contexts_sample.csv"
    manual_sample_path = tmp_path / "manual_resolution_review_sample.csv"
    analysis_ready_path = tmp_path / "analysis_ready_strong_contexts.parquet"

    metrics = audit_final_resolved_contexts(
        resolved_path=resolved_path,
        out_report=report_path,
        flags_path=flags_path,
        strong_sample_path=strong_sample_path,
        manual_sample_path=manual_sample_path,
        analysis_ready_path=analysis_ready_path,
    )

    report = report_path.read_text(encoding="utf-8")
    flags = pd.read_parquet(flags_path)
    strong_sample = pd.read_csv(strong_sample_path)
    manual_sample = pd.read_csv(manual_sample_path)
    analysis_ready = pd.read_parquet(analysis_ready_path)

    assert metrics["duplicate_context_id_count"] == 1
    assert "## Special Consistency Checks" in report
    assert int(flags["strong_numeric_marker"].sum()) == 1
    assert set(STRONG_SAMPLE_COLUMNS) <= set(strong_sample.columns)
    assert set(MANUAL_SAMPLE_COLUMNS) <= set(manual_sample.columns)
    assert "references_bad" not in set(analysis_ready["context_id"])


def test_contexts_audit_final_resolved_cli(tmp_path: Path) -> None:
    resolved_path = _write_fixture(tmp_path)
    report_path = tmp_path / "final_resolved_context_audit.md"
    flags_path = tmp_path / "final_resolved_context_quality_flags.parquet"
    strong_sample_path = tmp_path / "strong_resolved_contexts_sample.csv"
    manual_sample_path = tmp_path / "manual_resolution_review_sample.csv"
    analysis_ready_path = tmp_path / "analysis_ready_strong_contexts.parquet"
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "contexts",
            "audit-final-resolved",
            "--resolved",
            str(resolved_path),
            "--out",
            str(report_path),
            "--flags",
            str(flags_path),
            "--strong-sample",
            str(strong_sample_path),
            "--manual-sample",
            str(manual_sample_path),
            "--analysis-ready",
            str(analysis_ready_path),
        ],
    )

    assert result.exit_code == 0
    assert "Analysis-ready strong rows" in result.stdout
    assert report_path.exists()
    assert pd.read_parquet(analysis_ready_path).shape[0] >= 1


def _flag_for(flags: pd.DataFrame, context_id: str, column: str) -> bool:
    rows = flags.loc[flags["context_id"].eq(context_id), column]
    assert not rows.empty
    return bool(rows.iloc[0])
