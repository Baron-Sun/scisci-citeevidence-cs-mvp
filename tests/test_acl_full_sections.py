from __future__ import annotations

import gzip
import pickle
from pathlib import Path

import pandas as pd

from citeevidence.acl.full_sections import (
    SECTIONED_COLUMNS,
    inspect_full_sections_data,
    normalize_section_name,
    parse_full_sections_data,
)
from citeevidence.acl.section_normalization import normalize_sectioned_sections


def test_normalize_section_variants() -> None:
    assert normalize_section_name("Related Work") == "related_work"
    assert normalize_section_name("Experiments and Results") == "experiment"
    assert normalize_section_name("Methodology") == "method"
    assert normalize_section_name("Evaluation") == "evaluation"
    assert normalize_section_name("Data and Resources") == "dataset"
    assert normalize_section_name("Error Analysis") == "error_analysis"
    assert normalize_section_name("System Description") == "system_description"
    assert normalize_section_name("Task Definition") == "task_definition"


def test_parse_full_sections_like_pickle(tmp_path: Path) -> None:
    raw = tmp_path / "raw"
    raw.mkdir()
    input_path = raw / "acl-publication-info.74k.v2.full-sections.pkl"
    out_path = tmp_path / "acl_sections_sectioned.parquet"
    report_path = tmp_path / "full_sections_parse_report.md"
    sample_contexts_path = tmp_path / "citation_contexts_sectioned_sample.parquet"
    references_path = tmp_path / "missing_references.parquet"

    frame = pd.DataFrame(
        [
            {
                "acl_id": "P00-1001",
                "title": "A Sectioned Paper",
                "json_contents": {
                    "pdf_parse": {
                        "abstract": [
                            {
                                "text": "This paper introduces a parser.",
                                "section": "Abstract",
                                "cite_spans": [],
                            }
                        ],
                        "body_text": [
                            {
                                "text": "Prior systems are strong (Smith, 2020).",
                                "section": "Related Work",
                                "sec_num": "1",
                                "cite_spans": [
                                    {
                                        "start": 25,
                                        "end": 38,
                                        "text": "(Smith, 2020)",
                                        "ref_id": "BIBREF0",
                                    }
                                ],
                            },
                            {
                                "text": "We run experiments and report results.",
                                "section": "Experiments and Results",
                                "sec_num": "2",
                                "cite_spans": [],
                            },
                        ],
                        "back_matter": [],
                    }
                },
            }
        ]
    )
    with gzip.open(input_path, "wb") as handle:
        pickle.dump(frame, handle)

    result = parse_full_sections_data(
        input_path=input_path,
        out_path=out_path,
        report_path=report_path,
        references_path=references_path,
        sample_contexts_out=sample_contexts_path,
        sample_context_section_rows=10,
    )

    parsed = pd.read_parquet(out_path)

    assert list(parsed.columns) == SECTIONED_COLUMNS
    assert len(parsed) == 3
    assert result.metrics["papers_with_section_data"] == 1
    assert result.metrics["section_name_non_empty_rate"] == "1.000"
    assert set(parsed["normalized_section"]) == {"abstract", "related_work", "experiment"}
    assert sample_contexts_path.exists()
    assert "section name non-empty rate" in report_path.read_text(encoding="utf-8")


def test_inspect_full_sections_missing_file_writes_clear_report(tmp_path: Path) -> None:
    raw = tmp_path / "raw"
    raw.mkdir()
    report_path = tmp_path / "full_sections_structure_report.md"

    result = inspect_full_sections_data(raw_dir=raw, out_report=report_path)
    report = report_path.read_text(encoding="utf-8")

    assert result.metrics["full_sections_exists"] is False
    assert "was not found" in report
    assert "inspection completed without crashing" in report


def test_normalize_sectioned_sections_audit(tmp_path: Path) -> None:
    input_path = tmp_path / "acl_sections_sectioned.parquet"
    out_path = tmp_path / "acl_sections_sectioned_normalized.parquet"
    report_path = tmp_path / "section_normalization_audit.md"
    pd.DataFrame(
        [
            {
                "paper_id": "P1",
                "section_name": "Data and Resources",
                "normalized_section": "unknown",
                "section_index": 0,
                "paragraph_id": "P1_s0000_p0000",
                "paragraph_index": 0,
                "paragraph_text": "Dataset paragraph.",
            },
            {
                "paper_id": "P1",
                "section_name": "Unusual Heading",
                "normalized_section": "unknown",
                "section_index": 1,
                "paragraph_id": "P1_s0001_p0000",
                "paragraph_index": 0,
                "paragraph_text": "Unknown paragraph.",
            },
        ]
    ).to_parquet(input_path, index=False)

    metrics = normalize_sectioned_sections(
        input_path=input_path,
        out_path=out_path,
        report_path=report_path,
        top_n_unknown=5,
    )
    normalized = pd.read_parquet(out_path)
    report = report_path.read_text(encoding="utf-8")

    assert list(normalized.columns) == SECTIONED_COLUMNS
    assert normalized["normalized_section"].tolist() == ["dataset", "unknown"]
    assert metrics["unknown_rate_before"] == "1.000"
    assert metrics["unknown_rate_after"] == "0.500"
    assert "Top 5 Raw Section Names Mapped To Unknown" in report
