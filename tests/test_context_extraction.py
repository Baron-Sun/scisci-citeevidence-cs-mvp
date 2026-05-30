from __future__ import annotations

from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from citeevidence.cli import app
from citeevidence.contexts.extract import (
    CONTEXT_COLUMNS,
    extract_citation_contexts,
    write_context_extraction_report,
)


def _write_inputs(
    tmp_path: Path,
    *,
    sections: list[dict[str, object]],
    references: list[dict[str, object]] | None = None,
) -> tuple[Path, Path, Path]:
    sections_path = tmp_path / "acl_sections.parquet"
    references_path = tmp_path / "acl_references.parquet"
    out_path = tmp_path / "citation_contexts.parquet"

    pd.DataFrame(sections).to_parquet(sections_path, index=False)
    pd.DataFrame(
        references
        if references is not None
        else [
            {
                "citing_paper_id": "p1",
                "reference_key": "1",
                "cited_title": "Baseline Method",
                "cited_year": 2020,
                "cited_authors": "Smith",
                "cited_doi": "10.0000/baseline",
                "raw_reference": "Smith. 2020. Baseline Method.",
            },
            {
                "citing_paper_id": "p1",
                "reference_key": "2",
                "cited_title": "Comparison Method",
                "cited_year": 2021,
                "cited_authors": "Jones",
                "cited_doi": "10.0000/comparison",
                "raw_reference": "Jones. 2021. Comparison Method.",
            },
            {
                "citing_paper_id": "p1",
                "reference_key": "3",
                "cited_title": "Third Method",
                "cited_year": 2022,
                "cited_authors": "Lee",
                "cited_doi": None,
                "raw_reference": "Lee. 2022. Third Method.",
            },
        ]
    ).to_parquet(references_path, index=False)
    return sections_path, references_path, out_path


def test_single_citation(tmp_path: Path) -> None:
    sections_path, references_path, out_path = _write_inputs(
        tmp_path,
        sections=[
            {
                "paper_id": "p1",
                "section_name": "Methods",
                "paragraph_id": "p1-para-1",
                "paragraph_text": "We use the baseline method [1]. It is efficient.",
            }
        ],
    )

    contexts = extract_citation_contexts(
        sections_path=sections_path,
        references_path=references_path,
        out_path=out_path,
        max_window_chars=300,
        use_bibliography=True,
    )

    assert list(contexts.columns) == CONTEXT_COLUMNS
    assert len(contexts) == 1
    row = contexts.iloc[0]
    assert row["reference_key"] == "1"
    assert row["cited_title"] == "Baseline Method"
    assert row["marker_type"] == "numeric"
    assert row["citation_group_size"] == 1
    assert row["attribution_status"] == "single_citation_clear"


def test_grouped_citation(tmp_path: Path) -> None:
    sections_path, references_path, out_path = _write_inputs(
        tmp_path,
        sections=[
            {
                "paper_id": "p1",
                "section_name": "Related Work",
                "paragraph_id": "p1-para-2",
                "paragraph_text": "Several systems use similar components [1, 2].",
            }
        ],
    )

    contexts = extract_citation_contexts(
        sections_path=sections_path,
        references_path=references_path,
        out_path=out_path,
        use_bibliography=True,
    )

    assert len(contexts) == 2
    assert set(contexts["reference_key"]) == {"1", "2"}
    assert set(contexts["citation_group_size"]) == {2}
    assert set(contexts["attribution_status"]) == {"multi_citation_group"}


def test_unresolved_citation(tmp_path: Path) -> None:
    sections_path, references_path, out_path = _write_inputs(
        tmp_path,
        sections=[
            {
                "paper_id": "p1",
                "section_name": "Discussion",
                "paragraph_id": "p1-para-3",
                "paragraph_text": "The claim appears in an unavailable reference [99].",
            }
        ],
    )

    contexts = extract_citation_contexts(
        sections_path=sections_path,
        references_path=references_path,
        out_path=out_path,
        use_bibliography=True,
    )

    assert len(contexts) == 1
    row = contexts.iloc[0]
    assert row["reference_key"] == "99"
    assert pd.isna(row["cited_title"])
    assert row["attribution_status"] == "bibliography_unresolved"


def test_pre_resolution_extraction_without_references(tmp_path: Path) -> None:
    sections_path, _, out_path = _write_inputs(
        tmp_path,
        sections=[
            {
                "paper_id": "p1",
                "section_name": "Related Work",
                "paragraph_id": "p1-para-pre",
                "paragraph_text": (
                    "We use a prior system [1]. Smith (2020) described the task. "
                    "Other work is grouped (Smith, 2020; Jones, 2021)."
                ),
            }
        ],
    )

    contexts = extract_citation_contexts(
        sections_path=sections_path,
        out_path=out_path,
        max_window_chars=300,
    )

    assert len(contexts) == 4
    assert contexts["cited_title"].isna().all()
    numeric = contexts.loc[contexts["marker_type"].eq("numeric")].iloc[0]
    author_year = contexts.loc[contexts["marker_type"].eq("narrative_author_year")].iloc[0]
    grouped = contexts.loc[contexts["citation_group_size"].eq(2)]
    assert str(numeric["reference_key"]).startswith("marker_component_0_")
    assert numeric["attribution_status"] == "numeric_unresolved_pre_resolution"
    assert author_year["attribution_status"] == "author_year_unresolved_pre_resolution"
    assert set(grouped["attribution_status"]) == {"multi_citation_group"}


def test_sectioned_extraction_uses_normalized_section_and_report(tmp_path: Path) -> None:
    sections_path = tmp_path / "acl_sections_sectioned_normalized.parquet"
    out_path = tmp_path / "citation_contexts_sectioned.parquet"
    report_path = tmp_path / "citation_contexts_sectioned_extraction_report.md"
    pd.DataFrame(
        [
            {
                "paper_id": "p1",
                "section_name": "Methodology",
                "normalized_section": "method",
                "section_index": 0,
                "paragraph_id": "p1_s0000_p0000",
                "paragraph_index": 0,
                "paragraph_text": "We use the baseline [1].",
            }
        ]
    ).to_parquet(sections_path, index=False)

    contexts = extract_citation_contexts(
        sections_path=sections_path,
        out_path=out_path,
        max_window_chars=300,
    )
    metrics = write_context_extraction_report(
        contexts=contexts,
        sections_path=sections_path,
        out_path=out_path,
        report_path=report_path,
        max_window_chars=300,
    )

    assert contexts.iloc[0]["section"] == "method"
    assert contexts.iloc[0]["raw_section_name"] == "Methodology"
    assert contexts.iloc[0]["normalized_section"] == "method"
    assert not bool(contexts.iloc[0]["large_citation_group_flag"])
    assert not bool(contexts.iloc[0]["very_large_citation_group_flag"])
    assert not bool(contexts.iloc[0]["suspicious_citation_range_flag"])
    assert metrics["duplicate_context_id"] == 0
    assert metrics["raw_section_name_non_empty_rate"] == "1.000"
    report = report_path.read_text(encoding="utf-8")
    assert "raw_section_name non-empty rate" in report
    assert "Normalized Section Distribution" in report


def test_large_citation_group_flags(tmp_path: Path) -> None:
    sections_path, _, out_path = _write_inputs(
        tmp_path,
        sections=[
            {
                "paper_id": "p1",
                "section_name": "Experiments",
                "paragraph_id": "p1-para-large",
                "paragraph_text": (
                    "Normal grouped citations are [1, 2]. "
                    "A suspicious citation range is [1-21]."
                ),
            }
        ],
    )

    contexts = extract_citation_contexts(
        sections_path=sections_path,
        out_path=out_path,
        max_window_chars=300,
    )

    normal_group = contexts.loc[contexts["citation_marker"].eq("[1, 2]")]
    large_range = contexts.loc[contexts["citation_marker"].eq("[1-21]")]
    assert len(normal_group) == 2
    assert len(large_range) == 21
    assert normal_group["large_citation_group_flag"].eq(False).all()
    assert normal_group["very_large_citation_group_flag"].eq(False).all()
    assert normal_group["suspicious_citation_range_flag"].eq(False).all()
    assert large_range["large_citation_group_flag"].eq(True).all()
    assert large_range["very_large_citation_group_flag"].eq(False).all()
    assert large_range["suspicious_citation_range_flag"].eq(True).all()


def test_multiple_citations_in_one_paragraph(tmp_path: Path) -> None:
    sections_path, references_path, out_path = _write_inputs(
        tmp_path,
        sections=[
            {
                "paper_id": "p1",
                "section_name": "Experiments",
                "paragraph_id": "p1-para-4",
                "paragraph_text": "We train with the first method [1]. We compare against [2].",
            }
        ],
    )

    contexts = extract_citation_contexts(
        sections_path=sections_path,
        references_path=references_path,
        out_path=out_path,
        use_bibliography=True,
    )

    assert len(contexts) == 2
    assert list(contexts["reference_key"]) == ["1", "2"]
    assert contexts["sentence_text"].str.contains(r"\[1\]|\[2\]", regex=True).all()


def test_repeated_citation_to_same_reference(tmp_path: Path) -> None:
    sections_path, references_path, out_path = _write_inputs(
        tmp_path,
        sections=[
            {
                "paper_id": "p1",
                "section_name": "Methods",
                "paragraph_id": "p1-para-5",
                "paragraph_text": "We use the baseline [1]. Later, we tune the baseline [1].",
            }
        ],
    )

    first = extract_citation_contexts(
        sections_path=sections_path,
        references_path=references_path,
        out_path=out_path,
        use_bibliography=True,
    )
    second = extract_citation_contexts(
        sections_path=sections_path,
        references_path=references_path,
        out_path=tmp_path / "citation_contexts_second.parquet",
        use_bibliography=True,
    )

    assert len(first) == 2
    assert set(first["reference_key"]) == {"1"}
    assert first["context_id"].nunique() == 2
    assert first["context_id"].tolist() == second["context_id"].tolist()


def test_narrative_author_year_emits_single_marker(tmp_path: Path) -> None:
    sentence = "Elsner and Charniak (2010) described conversation disentanglement."
    sections_path, references_path, out_path = _write_inputs(
        tmp_path,
        sections=[
            {
                "paper_id": "p1",
                "section_name": "Related Work",
                "paragraph_id": "p1-para-7",
                "paragraph_text": sentence,
            }
        ],
    )

    contexts = extract_citation_contexts(
        sections_path=sections_path,
        references_path=references_path,
        out_path=out_path,
        use_bibliography=True,
    )

    assert len(contexts) == 1
    row = contexts.iloc[0]
    assert row["citation_marker"] == "Elsner and Charniak (2010)"
    assert row["marker_type"] == "narrative_author_year"
    assert row["marker_start_offset"] == sentence.index("Elsner")
    assert row["marker_end_offset"] == sentence.index(")") + 1


def test_et_al_narrative_author_year_marker(tmp_path: Path) -> None:
    sections_path, references_path, out_path = _write_inputs(
        tmp_path,
        sections=[
            {
                "paper_id": "p1",
                "section_name": "Related Work",
                "paragraph_id": "p1-para-8",
                "paragraph_text": "Hatzivassiloglou et al. (1999) proposed a method.",
            }
        ],
    )

    contexts = extract_citation_contexts(
        sections_path=sections_path,
        references_path=references_path,
        out_path=out_path,
        use_bibliography=True,
    )

    assert len(contexts) == 1
    assert contexts.iloc[0]["citation_marker"] == "Hatzivassiloglou et al. (1999)"
    assert contexts.iloc[0]["marker_type"] == "narrative_author_year"


def test_parenthetical_author_year_still_emits(tmp_path: Path) -> None:
    sections_path, references_path, out_path = _write_inputs(
        tmp_path,
        sections=[
            {
                "paper_id": "p1",
                "section_name": "Related Work",
                "paragraph_id": "p1-para-9",
                "paragraph_text": "This approach is common (Rosario and Hearst, 2001).",
            }
        ],
    )

    contexts = extract_citation_contexts(
        sections_path=sections_path,
        references_path=references_path,
        out_path=out_path,
        use_bibliography=True,
    )

    assert len(contexts) == 1
    assert contexts.iloc[0]["citation_marker"] == "(Rosario and Hearst, 2001)"
    assert contexts.iloc[0]["marker_type"] == "parenthetical_author_year"


def test_repeated_identical_author_year_markers_have_unique_ids(tmp_path: Path) -> None:
    sections_path, references_path, out_path = _write_inputs(
        tmp_path,
        sections=[
            {
                "paper_id": "p1",
                "section_name": "Related Work",
                "paragraph_id": "p1-para-10",
                "paragraph_text": "Smith (2020) introduced it. Smith (2020) extended it.",
            }
        ],
    )

    contexts = extract_citation_contexts(
        sections_path=sections_path,
        references_path=references_path,
        out_path=out_path,
        use_bibliography=True,
    )

    assert len(contexts) == 2
    assert contexts["citation_marker"].tolist() == ["Smith (2020)", "Smith (2020)"]
    assert contexts["context_id"].nunique() == 2


def test_narrative_author_detection_does_not_start_inside_word(tmp_path: Path) -> None:
    sections_path, references_path, out_path = _write_inputs(
        tmp_path,
        sections=[
            {
                "paper_id": "p1",
                "section_name": "Methods",
                "paragraph_id": "p1-para-11",
                "paragraph_text": "Other measures include Levenshtein (1966).",
            }
        ],
    )

    contexts = extract_citation_contexts(
        sections_path=sections_path,
        references_path=references_path,
        out_path=out_path,
        use_bibliography=True,
    )

    assert len(contexts) == 1
    assert contexts.iloc[0]["citation_marker"] == "Levenshtein (1966)"


def test_contexts_extract_cli(tmp_path: Path) -> None:
    sections_path, references_path, out_path = _write_inputs(
        tmp_path,
        sections=[
            {
                "paper_id": "p1",
                "section_name": "Methods",
                "paragraph_id": "p1-para-6",
                "paragraph_text": "We use the baseline method [1].",
            }
        ],
    )
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "contexts",
            "extract",
            "--sections",
            str(sections_path),
            "--references",
            str(references_path),
            "--use-bibliography",
            "--out",
            str(out_path),
            "--max-window-chars",
            "300",
        ],
    )

    assert result.exit_code == 0
    assert "Wrote 1 citation contexts" in result.stdout
    assert pd.read_parquet(out_path).shape == (1, len(CONTEXT_COLUMNS))


def test_contexts_extract_sectioned_cli_without_references(tmp_path: Path) -> None:
    sections_path = tmp_path / "acl_sections_sectioned_normalized.parquet"
    out_path = tmp_path / "citation_contexts_sectioned.parquet"
    report_path = tmp_path / "citation_contexts_sectioned_extraction_report.md"
    pd.DataFrame(
        [
            {
                "paper_id": "p1",
                "section_name": "Methods",
                "normalized_section": "method",
                "section_index": 0,
                "paragraph_id": "p1-para-sectioned",
                "paragraph_index": 0,
                "paragraph_text": "We use the baseline method [1].",
            }
        ]
    ).to_parquet(sections_path, index=False)
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "contexts",
            "extract-sectioned",
            "--sections",
            str(sections_path),
            "--out",
            str(out_path),
            "--max-window-chars",
            "300",
            "--report",
            str(report_path),
        ],
    )

    assert result.exit_code == 0
    assert "pre-resolution citation contexts" in result.stdout
    assert report_path.exists()
    contexts = pd.read_parquet(out_path)
    assert contexts.shape == (1, len(CONTEXT_COLUMNS))
    assert contexts.iloc[0]["section"] == "method"
    assert contexts.iloc[0]["attribution_status"] == "numeric_unresolved_pre_resolution"
