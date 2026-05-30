from __future__ import annotations

from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from citeevidence.cli import app
from citeevidence.contexts.extract import CONTEXT_COLUMNS, extract_citation_contexts


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
    )

    assert list(contexts.columns) == CONTEXT_COLUMNS
    assert len(contexts) == 1
    row = contexts.iloc[0]
    assert row["reference_key"] == "1"
    assert row["cited_title"] == "Baseline Method"
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
    )

    assert len(contexts) == 1
    row = contexts.iloc[0]
    assert row["reference_key"] == "99"
    assert pd.isna(row["cited_title"])
    assert row["attribution_status"] == "bibliography_unresolved"


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
    )
    second = extract_citation_contexts(
        sections_path=sections_path,
        references_path=references_path,
        out_path=tmp_path / "citation_contexts_second.parquet",
    )

    assert len(first) == 2
    assert set(first["reference_key"]) == {"1"}
    assert first["context_id"].nunique() == 2
    assert first["context_id"].tolist() == second["context_id"].tolist()


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
            "--out",
            str(out_path),
            "--max-window-chars",
            "300",
        ],
    )

    assert result.exit_code == 0
    assert "Wrote 1 citation contexts" in result.stdout
    assert pd.read_parquet(out_path).shape == (1, len(CONTEXT_COLUMNS))
