"""Markdown report assembly for final-release analyses."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd

from citeevidence.final_release.qa import validate_forbidden_claims, validate_required_caveats

REQUIRED_REPORT_SECTIONS = (
    "executive_summary",
    "scope",
    "qa_summary",
    "section_function_grammar",
    "object_role_signatures",
    "ranking_reversal",
    "critique_bottlenecks",
    "evidence_cards",
    "limitations",
    "reproducibility",
)


def build_final_release_report(
    *,
    qa_summary: pd.DataFrame,
    confidence_by_intent: pd.DataFrame,
    failure_categories: pd.DataFrame,
    section_lift: pd.DataFrame,
    object_roles: pd.DataFrame,
    ranking_reversal: pd.DataFrame,
    critique_matrix: pd.DataFrame,
    evidence_cards: pd.DataFrame | None = None,
    figure_paths: dict[str, str] | None = None,
    source_paths: dict[str, str] | None = None,
) -> str:
    """Assemble the final-release Markdown report without writing artifacts."""
    manifest = build_final_release_figure_manifest(figure_paths, source_paths)
    sections = [
        "# SciSci-CiteEvidence Final Release Report",
        _executive_summary(),
        _scope_section(),
        _qa_section(qa_summary, confidence_by_intent, failure_categories),
        _section_function_finding(section_lift, figure_paths),
        _object_role_finding(object_roles, figure_paths),
        _ranking_reversal_finding(ranking_reversal, figure_paths),
        _critique_bottleneck_finding(critique_matrix, figure_paths),
        _evidence_cards_section(evidence_cards),
        _limitations_section(),
        _reproducibility_section(manifest),
    ]
    return "\n\n".join(section.strip() for section in sections if section.strip()) + "\n"


def build_final_release_limitations() -> list[str]:
    """Return standard final-release limitations and QA caveats."""
    return [
        "ACL-OCL / ACL-centric scope: this release analyzes ACL-derived citation contexts.",
        "Phase-2 covers the full high/medium Phase-1 queue, not all strong contexts.",
        (
            "Labels are LLM-assisted, schema-validated, evidence-grounded labels, "
            "not human gold annotations."
        ),
        (
            "Object graph claims are over a curated seed-registry object-use graph, "
            "not the full universe of NLP methods."
        ),
        "Unknown sections are retained explicitly and should not be mixed into main panels.",
        "Strict validation excludes failed rows from final analysis-ready summaries.",
        "Critique bottleneck families are an exploratory heuristic cue-family map.",
        (
            "Current outputs are an object-use/citation-function graph, not a completed "
            "Intern-Atlas-scale method evolution graph."
        ),
    ]


def build_final_release_figure_manifest(
    figure_paths: dict[str, str] | None,
    source_paths: dict[str, str] | None,
) -> pd.DataFrame:
    """Build a source-artifact manifest for final-release figures and tables."""
    figure_paths = figure_paths or {}
    source_paths = source_paths or {}
    artifacts = {
        "qa_summary": (
            "Document label QA status and validation exclusions.",
            "Labels are LLM-assisted, schema-validated, evidence-grounded labels.",
        ),
        "section_function_lift": (
            "Show whether citation functions follow paper rhetorical structure.",
            "Based on final analysis-ready Phase-2 labels; unknown sections are explicit.",
        ),
        "object_role_signature_map": (
            "Summarize functional role profiles for curated seed-registry objects.",
            "Seed-registry object-use graph, not the full universe of NLP methods.",
        ),
        "ranking_reversal": (
            "Compare citation-context volume ranks against evidence-use ranks.",
            "total_strong_contexts is citation-context volume rather than graph in-degree.",
        ),
        "critique_bottleneck_heatmap": (
            "Map recurring critique cue families by seed-registry object type.",
            "Exploratory heuristic cue-family map; not a validated bottleneck taxonomy.",
        ),
        "evidence_cards": (
            "Provide compact reviewer-facing examples for report claims.",
            "Examples support interpretation but are not gold annotations.",
        ),
    }
    rows = [
        {
            "artifact": artifact,
            "figure_path": figure_paths.get(artifact, ""),
            "source_path": source_paths.get(artifact, ""),
            "purpose": purpose,
            "caveat": caveat,
        }
        for artifact, (purpose, caveat) in artifacts.items()
    ]
    return pd.DataFrame(
        rows,
        columns=["artifact", "figure_path", "source_path", "purpose", "caveat"],
    )


def validate_final_release_report_text(text: str) -> list[str]:
    """Validate report text against required caveats and forbidden claims."""
    issues = [f"missing_required_caveat:{issue}" for issue in validate_required_caveats(text)]
    issues.extend(f"forbidden_claim:{issue}" for issue in validate_forbidden_claims(text))
    return issues


def _executive_summary() -> str:
    return "\n".join(
        [
            "## Executive summary",
            (
                "SciSci-CiteEvidence turns section-aware citation contexts into an "
                "evidence-grounded view of how NLP objects are cited and used."
            ),
            (
                "The release supports four claim families: section-function structure, "
                "seed-registry object role signatures, citation-context volume versus "
                "evidence-use rank reversals, and exploratory critique cue families."
            ),
            (
                "The main scientific point is that citation-context volume, rhetorical "
                "section, object type, and evidence-use function are distinct signals."
            ),
        ]
    )


def _scope_section() -> str:
    bullets = [
        "Phase-2 covers the full high/medium Phase-1 queue, not all strong contexts.",
        (
            "Labels are LLM-assisted, schema-validated, evidence-grounded labels, "
            "not human gold annotations."
        ),
        (
            "Object graph claims are over a curated seed-registry object-use graph, "
            "not the full universe of NLP methods."
        ),
        (
            "Current outputs are an object-use/citation-function graph, not a completed "
            "Intern-Atlas-scale method evolution graph."
        ),
        "total_strong_contexts is citation-context volume rather than graph in-degree.",
    ]
    return "\n".join(
        [
            "## What this release is and is not",
            (
                "This report assembles final-release analyses around grounded citation "
                "contexts. It is a course-scale evidence layer, not a universal map of NLP."
            ),
            _bullet_list(bullets),
            "",
            "## Data and evidence scope",
            (
                "All claims below are conditioned on final analysis-ready Phase-2 labels "
                "and their retained evidence spans. Source artifacts are listed at the end "
                "so figures can be regenerated or audited."
            ),
        ]
    )


def _qa_section(
    qa_summary: pd.DataFrame,
    confidence_by_intent: pd.DataFrame,
    failure_categories: pd.DataFrame,
) -> str:
    return "\n".join(
        [
            "## QA summary",
            (
                "QA is reported as release diagnostics, not as human adjudication. "
                "The label set remains LLM-assisted, schema-validated, evidence-grounded "
                "labels, not human gold annotations."
            ),
            _markdown_table(qa_summary, max_rows=8),
            "",
            "### Confidence By Intent",
            _markdown_table(confidence_by_intent, max_rows=6),
            "",
            "### Remaining Failure Categories",
            _markdown_table(failure_categories, max_rows=6),
        ]
    )


def _section_function_finding(
    section_lift: pd.DataFrame,
    figure_paths: dict[str, str] | None,
) -> str:
    top = _top_rows(section_lift, "log_odds_lift", max_rows=5)
    return "\n".join(
        [
            "## Finding 1: Section-function grammar",
            (
                "Citation roles follow paper rhetorical structure: implementation and "
                "experiment sections can emphasize use, while related-work and introduction "
                "sections can emphasize background roles."
            ),
            (
                "Caveat: section-function results are based on final analysis-ready "
                "Phase-2 labels, and unknown sections are handled explicitly rather than "
                "silently merged into the main panel."
            ),
            _artifact_sentence("section_function_lift", figure_paths),
            _markdown_table(top, max_rows=5),
        ]
    )


def _object_role_finding(
    object_roles: pd.DataFrame,
    figure_paths: dict[str, str] | None,
) -> str:
    top = _top_rows(object_roles, "non_background_edges", max_rows=5)
    return "\n".join(
        [
            "## Finding 2: Seed-registry object role signatures",
            (
                "Seed-registry objects occupy different citation-use roles, including "
                "background canon, operational infrastructure, evaluation anchors, critique "
                "targets, and mixed roles."
            ),
            (
                "Caveat: these roles describe a curated seed-registry object-use graph, "
                "not the full universe of NLP methods."
            ),
            _artifact_sentence("object_role_signature_map", figure_paths),
            _markdown_table(top, max_rows=5),
        ]
    )


def _ranking_reversal_finding(
    ranking_reversal: pd.DataFrame,
    figure_paths: dict[str, str] | None,
) -> str:
    top = _top_rows(ranking_reversal, "rank_difference_count", max_rows=5, absolute=True)
    return "\n".join(
        [
            "## Finding 3: Citation-context volume vs evidence-use ranking reversal",
            (
                "Citation-context volume is not the same as evidence use. Some cited "
                "papers are frequent context anchors but mostly background, while others "
                "have fewer contexts and stronger direct evidence-use profiles."
            ),
            (
                "Caveat: total_strong_contexts measures citation-context volume rather "
                "than graph in-degree, and default ranking figures exclude thin-tail rows."
            ),
            _artifact_sentence("ranking_reversal", figure_paths),
            _markdown_table(top, max_rows=5),
        ]
    )


def _critique_bottleneck_finding(
    critique_matrix: pd.DataFrame,
    figure_paths: dict[str, str] | None,
) -> str:
    top = _top_rows(critique_matrix, "lift_vs_global", max_rows=5)
    return "\n".join(
        [
            "## Finding 4: Exploratory critique bottlenecks",
            (
                "Critique contexts can be grouped into recurring limitation cue families "
                "such as metric validity, generalization, data requirements, cost, and "
                "tooling reproducibility."
            ),
            (
                "Caveat: this is an exploratory heuristic cue-family map, not a validated "
                "bottleneck taxonomy."
            ),
            _artifact_sentence("critique_bottleneck_heatmap", figure_paths),
            _markdown_table(top, max_rows=5),
        ]
    )


def _evidence_cards_section(evidence_cards: pd.DataFrame | None) -> str:
    return "\n".join(
        [
            "## Evidence cards / examples",
            (
                "Evidence cards provide compact examples for reviewers. They illustrate "
                "the evidence surface but do not convert the release into gold annotation."
            ),
            _markdown_table(evidence_cards, max_rows=6),
        ]
    )


def _limitations_section() -> str:
    return "\n".join(["## Limitations", _bullet_list(build_final_release_limitations())])


def _reproducibility_section(manifest: pd.DataFrame) -> str:
    return "\n".join(
        [
            "## Reproducibility and source artifacts",
            (
                "The report is assembled from source tables and figure paths supplied by "
                "the caller. This builder does not create repository artifacts."
            ),
            _markdown_table(manifest, max_rows=8),
        ]
    )


def _artifact_sentence(artifact: str, figure_paths: dict[str, str] | None) -> str:
    figure_paths = figure_paths or {}
    path = figure_paths.get(artifact)
    if not path:
        return f"Figure artifact: `{artifact}` path not supplied."
    return f"Figure artifact: `{path}`."


def _top_rows(
    frame: pd.DataFrame,
    sort_column: str,
    *,
    max_rows: int,
    absolute: bool = False,
) -> pd.DataFrame:
    if frame is None or frame.empty or sort_column not in frame:
        return pd.DataFrame()
    output = frame.copy()
    values = pd.to_numeric(output[sort_column], errors="coerce").fillna(0)
    output["_sort_value"] = values.abs() if absolute else values
    output = output.sort_values("_sort_value", ascending=False).drop(columns=["_sort_value"])
    return _narrow_columns(output).head(max_rows)


def _narrow_columns(frame: pd.DataFrame) -> pd.DataFrame:
    preferred = [
        "metric",
        "value",
        "note",
        "final_intent",
        "rows",
        "mean_confidence",
        "failure_category",
        "row_share",
        "normalized_section",
        "section_label",
        "log_odds_lift",
        "canonical_name",
        "object_type",
        "role_quadrant",
        "non_background_edges",
        "resolved_cited_title",
        "plot_label",
        "rank_difference_count",
        "bottleneck_family",
        "lift_vs_global",
        "evidence_span",
        "source_path",
        "figure_path",
        "purpose",
        "caveat",
    ]
    columns = [column for column in preferred if column in frame]
    return frame[columns] if columns else frame.iloc[:, : min(4, len(frame.columns))]


def _markdown_table(frame: pd.DataFrame | None, *, max_rows: int) -> str:
    if frame is None or frame.empty:
        return "_No rows provided._"
    clean = _narrow_columns(frame).head(max_rows).copy()
    clean = clean.apply(lambda column: column.map(_format_cell))
    headers = [str(column) for column in clean.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in clean.iterrows():
        cells = [_escape_table_cell(row[column]) for column in clean.columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def _format_cell(value: object) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    if isinstance(value, float):
        return f"{value:.3g}"
    text = str(value).strip()
    return text if len(text) <= 96 else f"{text[:93].rstrip()}..."


def _escape_table_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _bullet_list(items: Iterable[str]) -> str:
    return "\n".join(f"- {item}" for item in items)
