from __future__ import annotations

from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from citeevidence.cli import app
from citeevidence.review import (
    ingest_manual_resolution_review,
    normalize_review_frame,
)


def _strong_row(
    context_id: str,
    reviewer_correct: str = "",
    reviewer_notes: str = "",
) -> dict[str, object]:
    return {
        "context_id": context_id,
        "source_context_id": f"src_{context_id}",
        "citing_paper_id": "P00-0001",
        "normalized_section": "method",
        "marker_type": "parenthetical_author_year",
        "citation_marker": "(Smith, 2020)",
        "marker_component_text": "Smith, 2020",
        "resolved_cited_title": "A Strong Paper",
        "resolution_status": "author_year_clear",
        "resolution_confidence": 0.95,
        "reviewer_correct": reviewer_correct,
        "reviewer_notes": reviewer_notes,
    }


def _manual_row(
    context_id: str,
    *,
    review_bucket: str = "strong_author_year",
    resolution_level: str = "strong_author_year",
    resolution_status: str = "author_year_clear",
    reviewer_correct: str = "",
    reviewer_notes: str = "",
    reviewer_error_type: str = "",
) -> dict[str, object]:
    return {
        "review_bucket": review_bucket,
        "context_id": context_id,
        "source_context_id": f"src_{context_id}",
        "citing_paper_id": "P00-0001",
        "normalized_section": "related_work",
        "marker_type": "parenthetical_author_year",
        "citation_marker": "(Jones, 2021)",
        "marker_component_text": "Jones, 2021",
        "resolved_cited_title": "Another Paper",
        "resolution_status": resolution_status,
        "resolution_level": resolution_level,
        "resolution_confidence": 0.90,
        "reviewer_correct": reviewer_correct,
        "reviewer_notes": reviewer_notes,
        "reviewer_error_type": reviewer_error_type,
    }


def _write_review_inputs(tmp_path: Path) -> tuple[Path, Path]:
    strong_path = tmp_path / "strong_resolved_contexts_sample.csv"
    manual_path = tmp_path / "manual_resolution_review_sample.csv"
    pd.DataFrame(
        [
            _strong_row("strong_true", "true"),
            _strong_row("strong_false_missing_notes", "false"),
            _strong_row("strong_blank"),
        ]
    ).to_csv(strong_path, index=False)
    pd.DataFrame(
        [
            _manual_row("manual_unclear", reviewer_correct="unclear"),
            _manual_row(
                "manual_false_with_notes",
                reviewer_correct="false",
                reviewer_notes="Wrong cited paper.",
                reviewer_error_type="wrong_candidate",
            ),
            _manual_row(
                "manual_invalid",
                resolution_level="unresolved",
                resolution_status="bibliography_unresolved",
                reviewer_correct="yes",
            ),
            _manual_row(
                "manual_unreviewed",
                resolution_level="unresolved",
                resolution_status="bibliography_unresolved",
                reviewer_correct="",
            ),
        ]
    ).to_csv(manual_path, index=False)
    return strong_path, manual_path


def test_normalize_review_frame_accepts_blank_and_flags_invalid() -> None:
    frame = pd.DataFrame(
        [
            {"context_id": "blank", "source_context_id": "src_blank", "reviewer_correct": ""},
            {
                "context_id": "bad",
                "source_context_id": "src_bad",
                "reviewer_correct": "maybe",
            },
            {
                "context_id": "false_no_notes",
                "source_context_id": "src_false",
                "reviewer_correct": "false",
                "reviewer_notes": "",
            },
        ]
    )

    review = normalize_review_frame(frame)

    assert not bool(review.loc[review["context_id"].eq("blank"), "is_reviewed"].iloc[0])
    assert not bool(
        review.loc[review["context_id"].eq("bad"), "valid_reviewer_correct"].iloc[0]
    )
    assert bool(review.loc[review["context_id"].eq("bad"), "needs_check"].iloc[0])
    assert bool(
        review.loc[review["context_id"].eq("false_no_notes"), "needs_check"].iloc[0]
    )


def test_ingest_manual_resolution_review_outputs_report_and_needs_check(tmp_path: Path) -> None:
    strong_path, manual_path = _write_review_inputs(tmp_path)
    out_path = tmp_path / "manual_resolution_review_clean.parquet"
    needs_check_path = tmp_path / "manual_resolution_review_needs_check.csv"
    report_path = tmp_path / "manual_resolution_review_report.md"

    metrics = ingest_manual_resolution_review(
        strong_sample_path=strong_path,
        manual_sample_path=manual_path,
        out_path=out_path,
        needs_check_path=needs_check_path,
        report_path=report_path,
    )

    clean = pd.read_parquet(out_path)
    needs_check = pd.read_csv(needs_check_path)
    report = report_path.read_text(encoding="utf-8")

    assert metrics["reviewed_rows"] == 4
    assert metrics["unreviewed_rows"] == 2
    assert metrics["invalid_reviewer_correct_rows"] == 1
    assert metrics["precision_strong_author_year"] == "0.333"
    assert clean.shape[0] == 7
    assert set(["context_id", "source_context_id"]) <= set(clean.columns)
    assert set(needs_check["context_id"]) == {"strong_false_missing_notes", "manual_invalid"}
    assert "## Precision By Normalized Section" in report
    assert "wrong_candidate" in report


def test_ingest_prefers_completed_files_when_present(tmp_path: Path) -> None:
    strong_path, manual_path = _write_review_inputs(tmp_path)
    completed_manual = tmp_path / "manual_resolution_review_sample_completed.csv"
    pd.DataFrame([_manual_row("completed_true", reviewer_correct="true")]).to_csv(
        completed_manual,
        index=False,
    )

    metrics = ingest_manual_resolution_review(
        strong_sample_path=strong_path,
        manual_sample_path=manual_path,
        out_path=tmp_path / "clean.parquet",
        needs_check_path=tmp_path / "needs_check.csv",
        report_path=tmp_path / "report.md",
    )
    clean = pd.read_parquet(tmp_path / "clean.parquet")

    assert "completed_true" in set(clean["context_id"])
    assert "manual_invalid" not in set(clean["context_id"])
    assert metrics["total_rows"] == 4


def test_review_ingest_resolution_cli(tmp_path: Path) -> None:
    strong_path, manual_path = _write_review_inputs(tmp_path)
    out_path = tmp_path / "manual_resolution_review_clean.parquet"
    needs_check_path = tmp_path / "manual_resolution_review_needs_check.csv"
    report_path = tmp_path / "manual_resolution_review_report.md"
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "review",
            "ingest-resolution",
            "--strong-sample",
            str(strong_path),
            "--manual-sample",
            str(manual_path),
            "--out",
            str(out_path),
            "--needs-check",
            str(needs_check_path),
            "--report",
            str(report_path),
        ],
    )

    assert result.exit_code == 0
    assert "Ingested" in result.stdout
    assert out_path.exists()
    assert needs_check_path.exists()
    assert report_path.exists()
