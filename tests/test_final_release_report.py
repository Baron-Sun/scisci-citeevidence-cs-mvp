from __future__ import annotations

import pandas as pd

from citeevidence.final_release.report import (
    build_final_release_figure_manifest,
    build_final_release_limitations,
    build_final_release_report,
    validate_final_release_report_text,
)


def _report_text() -> str:
    return build_final_release_report(
        qa_summary=pd.DataFrame(
            [
                {"metric": "total_labels", "value": 229751, "note": ""},
                {"metric": "evidence_span_grounded_rows", "value": 229000, "note": ""},
            ]
        ),
        confidence_by_intent=pd.DataFrame(
            [
                {"final_intent": "background", "rows": 100, "mean_confidence": 0.86},
                {"final_intent": "uses", "rows": 80, "mean_confidence": 0.84},
            ]
        ),
        failure_categories=pd.DataFrame(
            [{"failure_category": "schema", "rows": 3, "row_share": 0.3}]
        ),
        section_lift=pd.DataFrame(
            [
                {
                    "normalized_section": "methods",
                    "final_intent": "uses",
                    "rows": 20,
                    "section_label": "Methods (N=30)",
                    "log_odds_lift": 1.5,
                }
            ]
        ),
        object_roles=pd.DataFrame(
            [
                {
                    "canonical_name": "BERT",
                    "object_type": "method",
                    "role_quadrant": "canonical_background",
                    "non_background_edges": 30,
                }
            ]
        ),
        ranking_reversal=pd.DataFrame(
            [
                {
                    "resolved_cited_title": "Background Anchor",
                    "plot_label": "Background Anchor",
                    "rank_difference_count": -12,
                    "total_strong_contexts": 100,
                    "evidence_use_count": 5,
                }
            ]
        ),
        critique_matrix=pd.DataFrame(
            [
                {
                    "object_type": "metric",
                    "bottleneck_family": "metric_validity",
                    "rows": 8,
                    "lift_vs_global": 2.0,
                }
            ]
        ),
        evidence_cards=pd.DataFrame(
            [
                {
                    "bottleneck_family": "metric_validity",
                    "object_name": "BLEU",
                    "object_type": "metric",
                    "context_id": "c1",
                    "evidence_span": "BLEU does not capture human judgment.",
                    "confidence": 0.82,
                }
            ]
        ),
        figure_paths={
            "section_function_lift": "figures/final_release/section_function_lift.png",
            "object_role_signature_map": "figures/final_release/object_role_map.png",
            "ranking_reversal": "figures/final_release/ranking_reversal.png",
            "critique_bottleneck_heatmap": "figures/final_release/critique_heatmap.png",
        },
        source_paths={
            "section_function_lift": "figures/final_release/source_data/section_lift.csv",
            "object_role_signature_map": "figures/final_release/source_data/object_roles.csv",
            "ranking_reversal": "figures/final_release/source_data/ranking_reversal.csv",
            "critique_bottleneck_heatmap": "figures/final_release/source_data/critique.csv",
        },
    )


def test_report_contains_all_required_sections() -> None:
    report = _report_text()

    for heading in [
        "# SciSci-CiteEvidence Final Release Report",
        "## Executive summary",
        "## What this release is and is not",
        "## Data and evidence scope",
        "## QA summary",
        "## Finding 1: Section-function grammar",
        "## Finding 2: Seed-registry object role signatures",
        "## Finding 3: Citation-context volume vs evidence-use ranking reversal",
        "## Finding 4: Exploratory critique bottlenecks",
        "## Evidence cards / examples",
        "## Limitations",
        "## Reproducibility and source artifacts",
    ]:
        assert heading in report


def test_report_contains_all_required_caveats() -> None:
    report = _report_text()

    assert "full high/medium Phase-1 queue, not all strong contexts" in report
    assert "LLM-assisted, schema-validated, evidence-grounded labels" in report
    assert "not human gold annotations" in report
    assert "seed-registry object-use graph" in report
    assert "not the full universe of NLP methods" in report
    assert "not a completed Intern-Atlas-scale method evolution graph" in report
    assert "total_strong_contexts is citation-context volume" in report


def test_validate_generated_report_returns_no_issues() -> None:
    assert validate_final_release_report_text(_report_text()) == []


def test_report_avoids_forbidden_terms() -> None:
    report = _report_text().casefold()

    for forbidden in [
        "citation count",
        "citation volume",
        "human gold labels",
        "full dataset phase-2",
        "all strong contexts were phase-2 labeled",
        "complete nlp method evolution graph",
        "intern-atlas-scale graph",
    ]:
        assert forbidden not in report


def test_report_uses_required_final_release_wording() -> None:
    report = _report_text().casefold()

    assert "citation-context volume" in report
    assert "seed-registry object-use graph" in report
    assert "exploratory heuristic cue-family map" in report
    assert "not a validated bottleneck taxonomy" in report


def test_figure_manifest_has_expected_columns() -> None:
    manifest = build_final_release_figure_manifest(
        {"ranking_reversal": "figures/ranking.png"},
        {"ranking_reversal": "source/ranking.csv"},
    )

    assert list(manifest.columns) == [
        "artifact",
        "figure_path",
        "source_path",
        "purpose",
        "caveat",
    ]
    row = manifest.loc[manifest["artifact"].eq("ranking_reversal")].iloc[0]
    assert row["figure_path"] == "figures/ranking.png"
    assert row["source_path"] == "source/ranking.csv"


def test_limitations_include_required_themes() -> None:
    limitations = " ".join(build_final_release_limitations()).casefold()

    for theme in [
        "acl-ocl",
        "high/medium phase-1 queue",
        "llm-assisted",
        "seed-registry",
        "unknown sections",
        "strict validation",
        "heuristic cue-family",
        "object-use/citation-function graph",
    ]:
        assert theme in limitations


def test_report_does_not_include_large_raw_table_dumps() -> None:
    report = _report_text()
    sections = report.split("\n## ")

    for section in sections:
        table_lines = [line for line in section.splitlines() if line.startswith("|")]
        assert len(table_lines) <= 20


def test_report_builder_does_not_require_local_parquet_files(monkeypatch) -> None:
    def fail_read_parquet(*_: object, **__: object) -> None:
        raise AssertionError("report builder should use provided DataFrames")

    monkeypatch.setattr(pd, "read_parquet", fail_read_parquet)

    assert "# SciSci-CiteEvidence Final Release Report" in _report_text()
