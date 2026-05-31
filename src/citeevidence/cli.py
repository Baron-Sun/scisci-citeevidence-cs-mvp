from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError
from rich.console import Console

from citeevidence import __version__
from citeevidence.acl.aligned_graph import (
    DEFAULT_ALIGNED_GRAPH_PATH,
    DEFAULT_ALIGNMENT_REPORT_PATH,
    DEFAULT_CROSSWALK_PATH,
    build_aligned_acl_citation_graph,
)
from citeevidence.acl.full_citations_coverage import (
    DEFAULT_CONTEXTS_PATH,
    DEFAULT_FULL_CITATIONS_COVERAGE_REPORT,
    DEFAULT_FULL_CITATIONS_SAFE_ALIGNED_PATH,
    DEFAULT_ONLYGRAPH_ALIGNED_PATH,
    evaluate_full_citations_candidate_coverage,
)
from citeevidence.acl.full_citations_coverage import (
    DEFAULT_RESOLVED_PILOT_PATH as DEFAULT_FULL_CITATIONS_RESOLVED_PILOT_PATH,
)
from citeevidence.acl.full_sections import (
    DEFAULT_FULL_SECTIONS_PARSE_REPORT,
    DEFAULT_FULL_SECTIONS_STRUCTURE_REPORT,
    DEFAULT_SECTIONED_CONTEXT_SAMPLE_PATH,
    DEFAULT_SECTIONED_SAMPLE_REFERENCE_PATH,
    DEFAULT_SECTIONED_SECTIONS_PATH,
    inspect_full_sections_data,
    parse_full_sections_data,
)
from citeevidence.acl.id_audit import (
    DEFAULT_SCHEMA_ID_AUDIT_REPORT,
    DEFAULT_SCHEMA_INVENTORY_PATH,
    audit_acl_ocl_ids,
)
from citeevidence.acl.inspector import DEFAULT_INVENTORY_PATH, inspect_acl_ocl_data
from citeevidence.acl.reader import parse_acl_ocl_data
from citeevidence.acl.section_normalization import (
    DEFAULT_NORMALIZED_SECTIONED_SECTIONS_PATH,
    DEFAULT_SECTION_NORMALIZATION_REPORT,
    normalize_sectioned_sections,
)
from citeevidence.config import ConfigLoadError, load_project_config
from citeevidence.contexts.audit import DEFAULT_CONTEXT_FLAGS_PATH, audit_citation_contexts
from citeevidence.contexts.extract import (
    DEFAULT_SECTIONED_EXTRACTION_REPORT,
    extract_citation_contexts,
    write_context_extraction_report,
)
from citeevidence.contexts.final_audit import (
    DEFAULT_ANALYSIS_READY_STRONG_CONTEXTS_PATH,
    DEFAULT_FINAL_RESOLVED_AUDIT_REPORT,
    DEFAULT_FINAL_RESOLVED_FLAGS_PATH,
    DEFAULT_MANUAL_RESOLUTION_SAMPLE_PATH,
    DEFAULT_STRONG_RESOLVED_SAMPLE_PATH,
    audit_final_resolved_contexts,
)
from citeevidence.contexts.resolve import (
    DEFAULT_RESOLUTION_BASELINE_PATH,
    DEFAULT_RESOLUTION_FAILURES_PATH,
    DEFAULT_RESOLUTION_REPORT_PATH,
    DEFAULT_RESOLVED_PILOT_PATH,
    resolve_citation_markers_pilot,
)
from citeevidence.datasets.multicite import load_multicite
from citeevidence.datasets.normalize import write_labeled_contexts
from citeevidence.datasets.scicite import load_scicite
from citeevidence.llm_review import (
    DEFAULT_ANALYSIS_READY_CONTEXTS_PATH as DEFAULT_LLM_REVIEW_CONTEXTS_PATH,
)
from citeevidence.llm_review import (
    DEFAULT_CITED_TITLE_OBJECT_PROFILES_SAMPLE_PATH as DEFAULT_LLM_REVIEW_TITLE_PROFILES_PATH,
)
from citeevidence.llm_review import (
    DEFAULT_LLM_OBJECT_REVIEW_JSONL_PATH,
    DEFAULT_LLM_OBJECT_REVIEW_PARQUET_PATH,
    DEFAULT_LLM_OBJECT_REVIEW_REPORT,
    DEFAULT_LLM_OBJECT_REVIEW_SAMPLE_PATH,
    run_llm_object_review,
)
from citeevidence.llm_review import (
    DEFAULT_OBJECT_MENTIONS_SAMPLE_PATH as DEFAULT_LLM_REVIEW_OBJECT_MENTIONS_PATH,
)
from citeevidence.llm_review import (
    DEFAULT_OBJECT_REGISTRY_PATH as DEFAULT_LLM_REVIEW_REGISTRY_PATH,
)
from citeevidence.object_policy import (
    DEFAULT_CITED_TITLE_OBJECT_PROFILES_FINAL_PATH,
    DEFAULT_CITED_TITLE_OBJECT_PROFILES_REFINED_PATH,
    DEFAULT_OBJECT_GRAPH_CANDIDATES_PATH,
    DEFAULT_OBJECT_MATCHING_FINAL_REPORT,
    DEFAULT_OBJECT_MENTIONS_FINAL_PATH,
    DEFAULT_OBJECT_MENTIONS_LLM_REVIEW_PATH,
    DEFAULT_OBJECT_MENTIONS_REFINED_PATH,
    DEFAULT_OBJECT_REGISTRY_POLICY_REPORT,
    apply_object_review_policy,
)
from citeevidence.objects import (
    DEFAULT_BROAD_OBJECT_GRAPH_CANDIDATES_PATH,
    DEFAULT_CITED_TITLE_OBJECT_PROFILES_PATH,
    DEFAULT_OBJECT_MATCHING_REPORT,
    DEFAULT_OBJECT_MENTIONS_PATH,
    DEFAULT_OBJECT_MENTIONS_REVIEW_SAMPLE_PATH,
    DEFAULT_OBJECT_REGISTRY_PATH,
    DEFAULT_STRICT_OBJECT_GRAPH_CANDIDATES_PATH,
    match_objects_in_contexts,
)
from citeevidence.objects import (
    DEFAULT_OBJECT_GRAPH_CANDIDATES_PATH as DEFAULT_FULL_OBJECT_GRAPH_CANDIDATES_PATH,
)
from citeevidence.phase1 import (
    DEFAULT_PHASE1_CANDIDATES_PILOT_PATH,
    DEFAULT_PHASE1_CANDIDATES_PILOT_REFINED_PATH,
    DEFAULT_PHASE1_CITED_TITLE_PROFILES_PATH,
    DEFAULT_PHASE1_CONTEXTS_PATH,
    DEFAULT_PHASE1_FEATURES_PILOT_PATH,
    DEFAULT_PHASE1_FEATURES_PILOT_REFINED_PATH,
    DEFAULT_PHASE1_LIMIT,
    DEFAULT_PHASE1_OBJECT_GRAPH_CANDIDATES_PATH,
    DEFAULT_PHASE1_OBJECT_MENTIONS_PATH,
    DEFAULT_PHASE1_REPORT_PILOT_PATH,
    DEFAULT_PHASE1_REPORT_PILOT_REFINED_PATH,
    screen_phase1_citation_functions,
)
from citeevidence.phase1_llm_review import (
    DEFAULT_PHASE1_LLM_CACHE_DIR,
    DEFAULT_PHASE1_LLM_RECOMMENDATIONS_REPORT,
    DEFAULT_PHASE1_LLM_REVIEW_JSONL_PATH,
    DEFAULT_PHASE1_LLM_REVIEW_PARQUET_PATH,
    DEFAULT_PHASE1_LLM_REVIEW_REPORT,
    DEFAULT_PHASE1_LLM_REVIEW_SAMPLE_PATH,
    run_phase1_llm_review,
)
from citeevidence.review import (
    DEFAULT_MANUAL_REVIEW_CLEAN_PATH,
    DEFAULT_MANUAL_REVIEW_NEEDS_CHECK_PATH,
    DEFAULT_MANUAL_REVIEW_REPORT,
    ingest_manual_resolution_review,
)

app = typer.Typer(
    add_completion=False,
    help="Evidence-grounded citation function analysis CLI scaffold.",
    no_args_is_help=True,
)
acl_app = typer.Typer(help="Inspect ACL-OCL raw data layouts.", no_args_is_help=True)
config_app = typer.Typer(help="Inspect and validate project configuration.", no_args_is_help=True)
contexts_app = typer.Typer(help="Extract bounded citation contexts.", no_args_is_help=True)
datasets_app = typer.Typer(
    help="Load and normalize citation-context datasets.",
    no_args_is_help=True,
)
objects_app = typer.Typer(help="Match registered NLP objects in contexts.", no_args_is_help=True)
phase1_app = typer.Typer(
    help="Screen citation-function candidates with rule-based Phase-1 cues.",
    no_args_is_help=True,
)
review_app = typer.Typer(
    help="Ingest review files and run model-based audits.",
    no_args_is_help=True,
)
console = Console()
error_console = Console(stderr=True)
DEFAULT_PROJECT_CONFIG = Path("configs/project.yaml")
DEFAULT_LABELED_REPORT = Path("reports/labeled_dataset_profile.md")
DEFAULT_ACL_REPORT = Path("reports/acl_ocl_data_inspection.md")

app.add_typer(acl_app, name="acl")
app.add_typer(config_app, name="config")
app.add_typer(contexts_app, name="contexts")
app.add_typer(datasets_app, name="datasets")
app.add_typer(objects_app, name="objects")
app.add_typer(phase1_app, name="phase1")
app.add_typer(review_app, name="review")


@app.callback()
def callback(
    version: Annotated[
        bool,
        typer.Option("--version", help="Show the installed citeevidence version and exit."),
    ] = False,
) -> None:
    """Course-scale citation evidence analysis scaffold."""
    if version:
        console.print(f"citeevidence {__version__}")
        raise typer.Exit()


@app.command()
def status() -> None:
    """Show scaffold status."""
    console.print("citeevidence scaffold is installed. Real data logic is not implemented yet.")


@acl_app.command("inspect")
def inspect_acl(
    input_dir: Annotated[
        Path,
        typer.Option("--input", help="Path to raw ACL-OCL files."),
    ],
    out: Annotated[
        Path,
        typer.Option("--out", help="Output markdown inspection report path."),
    ] = DEFAULT_ACL_REPORT,
    inventory: Annotated[
        Path,
        typer.Option("--inventory", help="Output parquet file inventory path."),
    ] = DEFAULT_INVENTORY_PATH,
) -> None:
    """Inspect ACL-OCL file formats and citation-evidence signals."""
    try:
        file_inventory = inspect_acl_ocl_data(
            input_dir,
            out_report=out,
            inventory_path=inventory,
        )
    except (FileNotFoundError, NotADirectoryError, OSError, ValueError) as exc:
        error_console.print(f"[red]Failed to inspect ACL-OCL data:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(
        f"Inspected {len(file_inventory)} files. Wrote report to {out} and inventory to "
        f"{inventory}."
    )


@acl_app.command("parse")
def parse_acl(
    input_dir: Annotated[
        Path,
        typer.Option("--input", help="Path to raw ACL-OCL files."),
    ],
    out_dir: Annotated[
        Path,
        typer.Option("--out-dir", help="Output directory for ACL interim parquet tables."),
    ] = Path("data/interim"),
    max_files: Annotated[
        int | None,
        typer.Option("--max-files", min=1, help="Maximum number of files to parse."),
    ] = None,
) -> None:
    """Parse ACL-OCL files into paper, reference, and section parquet tables."""
    try:
        result = parse_acl_ocl_data(input_dir, out_dir=out_dir, max_files=max_files)
    except (FileNotFoundError, NotADirectoryError, OSError, ValueError) as exc:
        error_console.print(f"[red]Failed to parse ACL-OCL data:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(
        f"Wrote {len(result.papers)} papers, {len(result.references)} references, and "
        f"{len(result.sections)} sections to {out_dir}."
    )


@acl_app.command("inspect-full-sections")
def inspect_full_sections(
    raw_dir: Annotated[
        Path,
        typer.Option("--raw-dir", help="Directory containing raw ACL-OCL files."),
    ],
    out_report: Annotated[
        Path,
        typer.Option("--out-report", help="Output markdown structure report path."),
    ] = DEFAULT_FULL_SECTIONS_STRUCTURE_REPORT,
) -> None:
    """Inspect ACL-OCL full-sections sources without assuming pickle structure."""
    try:
        result = inspect_full_sections_data(raw_dir=raw_dir, out_report=out_report)
    except (FileNotFoundError, NotADirectoryError, OSError, ValueError) as exc:
        error_console.print(f"[red]Failed to inspect full-sections data:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(
        f"Wrote full-sections structure report to {out_report}. "
        f"Recoverable paragraph rows: {result.metrics.get('recoverable_paragraph_rows', 0)}."
    )


@acl_app.command("parse-full-sections")
def parse_full_sections(
    input_path: Annotated[
        Path,
        typer.Option("--input", help="Path to ACL-OCL full-sections pickle."),
    ],
    out: Annotated[
        Path,
        typer.Option("--out", help="Output section-aware ACL sections parquet path."),
    ] = DEFAULT_SECTIONED_SECTIONS_PATH,
    report: Annotated[
        Path,
        typer.Option("--report", help="Output full-sections parse report path."),
    ] = DEFAULT_FULL_SECTIONS_PARSE_REPORT,
    references: Annotated[
        Path,
        typer.Option("--references", help="Optional references parquet for sample contexts."),
    ] = DEFAULT_SECTIONED_SAMPLE_REFERENCE_PATH,
    sample_contexts_out: Annotated[
        Path | None,
        typer.Option(
            "--sample-contexts-out",
            help="Optional output path for bounded sectioned citation-context sample.",
        ),
    ] = DEFAULT_SECTIONED_CONTEXT_SAMPLE_PATH,
    sample_context_section_rows: Annotated[
        int,
        typer.Option(
            "--sample-context-section-rows",
            min=1,
            help="Number of section rows to use for the sample context extraction.",
        ),
    ] = 10_000,
) -> None:
    """Parse ACL-OCL full-sections pickle into section-aware paragraph rows."""
    try:
        result = parse_full_sections_data(
            input_path=input_path,
            out_path=out,
            report_path=report,
            references_path=references,
            sample_contexts_out=sample_contexts_out,
            sample_context_section_rows=sample_context_section_rows,
        )
    except (FileNotFoundError, OSError, ValueError) as exc:
        error_console.print(f"[red]Failed to parse full-sections data:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(
        f"Wrote {len(result.sections)} section-aware paragraphs to {out}. "
        f"Section name non-empty rate: {result.metrics['section_name_non_empty_rate']}. "
        f"Report: {report}."
    )


@acl_app.command("audit-ids")
def audit_acl_ids(
    raw_dir: Annotated[
        Path,
        typer.Option("--raw-dir", help="Directory containing raw ACL-OCL parquet files."),
    ],
    interim_dir: Annotated[
        Path,
        typer.Option("--interim-dir", help="Directory containing interim ACL parquet tables."),
    ],
    contexts: Annotated[
        Path,
        typer.Option("--contexts", help="Path to citation_contexts.parquet."),
    ],
    out: Annotated[
        Path,
        typer.Option("--out", help="Output markdown schema and ID audit report path."),
    ] = DEFAULT_SCHEMA_ID_AUDIT_REPORT,
    inventory: Annotated[
        Path,
        typer.Option("--inventory", help="Output JSON schema inventory path."),
    ] = DEFAULT_SCHEMA_INVENTORY_PATH,
) -> None:
    """Audit ACL-OCL schemas and numeric-to-ACL ID mapping candidates."""
    try:
        schema_inventory = audit_acl_ocl_ids(
            raw_dir=raw_dir,
            interim_dir=interim_dir,
            contexts_path=contexts,
            out_report=out,
            inventory_path=inventory,
        )
    except (FileNotFoundError, OSError, ValueError) as exc:
        error_console.print(f"[red]Failed to audit ACL-OCL IDs:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(
        f"Wrote ACL-OCL ID audit report to {out} and schema inventory to {inventory}. "
        f"Inspected {len(schema_inventory['files'])} parquet files."
    )


@acl_app.command("build-aligned-graph")
def build_aligned_graph(
    publication_info: Annotated[
        Path,
        typer.Option("--publication-info", help="Path to ACL-OCL publication metadata."),
    ],
    onlygraph: Annotated[
        Path,
        typer.Option("--onlygraph", help="Path to acl_onlygraph.parquet."),
    ],
    contexts: Annotated[
        Path,
        typer.Option("--contexts", help="Path to citation_contexts.parquet."),
    ],
    out_crosswalk: Annotated[
        Path,
        typer.Option("--out-crosswalk", help="Output ACL ID crosswalk parquet path."),
    ] = DEFAULT_CROSSWALK_PATH,
    out_graph: Annotated[
        Path,
        typer.Option("--out-graph", help="Output aligned ACL citation graph parquet path."),
    ] = DEFAULT_ALIGNED_GRAPH_PATH,
    report: Annotated[
        Path,
        typer.Option("--report", help="Output alignment report markdown path."),
    ] = DEFAULT_ALIGNMENT_REPORT_PATH,
) -> None:
    """Build a clean ACL-to-ACL citation graph from ACL-OCL graph IDs."""
    try:
        metrics = build_aligned_acl_citation_graph(
            publication_info_path=publication_info,
            onlygraph_path=onlygraph,
            contexts_path=contexts,
            out_crosswalk=out_crosswalk,
            out_graph=out_graph,
            report_path=report,
        )
    except (FileNotFoundError, OSError, ValueError) as exc:
        error_console.print(f"[red]Failed to build aligned ACL graph:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(
        f"Wrote {metrics['acl_id_crosswalk_rows']} crosswalk rows to {out_crosswalk}, "
        f"{metrics['aligned_graph_edges']} aligned graph edges to {out_graph}, and report "
        f"to {report}."
    )


@acl_app.command("evaluate-full-citations")
def evaluate_full_citations(
    full_citations: Annotated[
        Path,
        typer.Option("--full-citations", help="Path to acl_full_citations.parquet."),
    ],
    publication_info: Annotated[
        Path,
        typer.Option("--publication-info", help="Path to ACL-OCL publication metadata."),
    ],
    onlygraph_aligned: Annotated[
        Path,
        typer.Option("--onlygraph-aligned", help="Path to aligned onlygraph parquet."),
    ] = DEFAULT_ONLYGRAPH_ALIGNED_PATH,
    resolved: Annotated[
        Path,
        typer.Option("--resolved", help="Path to citation_contexts_resolved_pilot.parquet."),
    ] = DEFAULT_FULL_CITATIONS_RESOLVED_PILOT_PATH,
    contexts: Annotated[
        Path,
        typer.Option("--contexts", help="Path to citation_contexts.parquet."),
    ] = DEFAULT_CONTEXTS_PATH,
    out_safe: Annotated[
        Path,
        typer.Option("--out-safe", help="Output safe aligned full-citations parquet path."),
    ] = DEFAULT_FULL_CITATIONS_SAFE_ALIGNED_PATH,
    report: Annotated[
        Path,
        typer.Option("--report", help="Output coverage report markdown path."),
    ] = DEFAULT_FULL_CITATIONS_COVERAGE_REPORT,
) -> None:
    """Evaluate safe acl_full_citations candidates without changing resolution."""
    try:
        result = evaluate_full_citations_candidate_coverage(
            full_citations_path=full_citations,
            publication_info_path=publication_info,
            onlygraph_aligned_path=onlygraph_aligned,
            resolved_pilot_path=resolved,
            contexts_path=contexts,
            out_safe_aligned=out_safe,
            report_path=report,
        )
    except (FileNotFoundError, OSError, ValueError) as exc:
        error_console.print(f"[red]Failed to evaluate full citations:[/red] {exc}")
        raise typer.Exit(1) from exc

    coverage = result.metrics["unresolved_author_year_coverage"]
    console.print(
        f"Wrote {len(result.safe_full_citations)} safe aligned full-citation rows to "
        f"{out_safe}. Report: {report}. "
        f"Recovered surname candidates for "
        f"{coverage['gain_same_year_surname_candidate_rows']} unresolved rows."
    )


@acl_app.command("normalize-sections")
def normalize_sections(
    input_path: Annotated[
        Path,
        typer.Option("--input", help="Path to acl_sections_sectioned.parquet."),
    ] = DEFAULT_SECTIONED_SECTIONS_PATH,
    out: Annotated[
        Path,
        typer.Option("--out", help="Output normalized section-aware sections parquet path."),
    ] = DEFAULT_NORMALIZED_SECTIONED_SECTIONS_PATH,
    report: Annotated[
        Path,
        typer.Option("--report", help="Output section normalization audit report path."),
    ] = DEFAULT_SECTION_NORMALIZATION_REPORT,
    top_n_unknown: Annotated[
        int,
        typer.Option(
            "--top-n-unknown",
            min=1,
            help="Number of raw unknown section names to include in the audit.",
        ),
    ] = 300,
) -> None:
    """Normalize explicit section headings and audit unknown rates."""
    try:
        metrics = normalize_sectioned_sections(
            input_path=input_path,
            out_path=out,
            report_path=report,
            top_n_unknown=top_n_unknown,
        )
    except (FileNotFoundError, OSError, ValueError) as exc:
        error_console.print(f"[red]Failed to normalize section headings:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(
        f"Wrote {metrics['output_rows']} normalized section rows to {out}. "
        f"Unknown rate: {metrics['unknown_rate_before']} -> "
        f"{metrics['unknown_rate_after']}. Report: {report}."
    )


@config_app.command("show")
def show_config(
    config: Annotated[
        Path,
        typer.Option("--config", help="Path to the project YAML config."),
    ] = DEFAULT_PROJECT_CONFIG,
) -> None:
    """Load, validate, and print the parsed project config."""
    try:
        project_config = load_project_config(config)
    except (ConfigLoadError, ValidationError) as exc:
        error_console.print(f"[red]Invalid config:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print_json(data=project_config.model_dump(mode="json"))


@contexts_app.command("extract")
def extract_contexts(
    sections: Annotated[
        Path,
        typer.Option("--sections", help="Path to acl_sections.parquet."),
    ],
    out: Annotated[
        Path,
        typer.Option("--out", help="Output parquet path for citation contexts."),
    ],
    references: Annotated[
        Path | None,
        typer.Option(
            "--references",
            help="Optional true local bibliography parquet path.",
        ),
    ] = None,
    max_window_chars: Annotated[
        int,
        typer.Option(
            "--max-window-chars",
            min=100,
            help="Maximum characters retained in bounded context windows.",
        ),
    ] = 2000,
    use_bibliography: Annotated[
        bool,
        typer.Option(
            "--use-bibliography",
            help=(
                "Resolve markers against --references. By default extraction is "
                "pre-resolution and cited metadata is left empty."
            ),
        ),
    ] = False,
) -> None:
    """Extract citation contexts from parsed ACL sections."""
    try:
        contexts = extract_citation_contexts(
            sections_path=sections,
            references_path=references,
            out_path=out,
            max_window_chars=max_window_chars,
            use_bibliography=use_bibliography,
        )
    except (FileNotFoundError, OSError, ValueError) as exc:
        error_console.print(f"[red]Failed to extract citation contexts:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(f"Wrote {len(contexts)} citation contexts to {out}.")


@contexts_app.command("extract-sectioned")
def extract_sectioned_contexts(
    sections: Annotated[
        Path,
        typer.Option(
            "--sections",
            help="Path to section-aware ACL sections parquet.",
        ),
    ] = DEFAULT_SECTIONED_SECTIONS_PATH,
    out: Annotated[
        Path,
        typer.Option("--out", help="Output parquet path for sectioned citation contexts."),
    ] = Path("data/processed/citation_contexts_sectioned.parquet"),
    max_window_chars: Annotated[
        int,
        typer.Option(
            "--max-window-chars",
            min=100,
            help="Maximum characters retained in bounded context windows.",
        ),
    ] = 2000,
    report: Annotated[
        Path,
        typer.Option("--report", help="Output sectioned extraction report path."),
    ] = DEFAULT_SECTIONED_EXTRACTION_REPORT,
) -> None:
    """Extract pre-resolution citation contexts from section-aware ACL paragraphs."""
    try:
        contexts = extract_citation_contexts(
            sections_path=sections,
            out_path=out,
            references_path=None,
            max_window_chars=max_window_chars,
            use_bibliography=False,
        )
        write_context_extraction_report(
            contexts=contexts,
            sections_path=sections,
            out_path=out,
            report_path=report,
            max_window_chars=max_window_chars,
        )
    except (FileNotFoundError, OSError, ValueError) as exc:
        error_console.print(f"[red]Failed to extract sectioned citation contexts:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(
        f"Wrote {len(contexts)} pre-resolution citation contexts to {out}. "
        f"Report: {report}."
    )


@contexts_app.command("audit")
def audit_contexts(
    contexts: Annotated[
        Path,
        typer.Option("--contexts", help="Path to citation_contexts.parquet."),
    ],
    sections: Annotated[
        Path,
        typer.Option("--sections", help="Path to acl_sections.parquet."),
    ],
    references: Annotated[
        Path,
        typer.Option("--references", help="Path to acl_references.parquet."),
    ],
    out: Annotated[
        Path,
        typer.Option("--out", help="Output markdown audit report path."),
    ],
    flags: Annotated[
        Path,
        typer.Option("--flags", help="Output parquet path for row-level quality flags."),
    ] = DEFAULT_CONTEXT_FLAGS_PATH,
    max_window_chars: Annotated[
        int,
        typer.Option(
            "--max-window-chars",
            min=100,
            help="Configured maximum context_window_s3 length.",
        ),
    ] = 2000,
) -> None:
    """Audit extracted citation contexts for Task 6 quality checks."""
    try:
        quality_flags = audit_citation_contexts(
            contexts_path=contexts,
            sections_path=sections,
            references_path=references,
            out_report=out,
            flags_path=flags,
            max_window_chars=max_window_chars,
        )
    except (FileNotFoundError, OSError, ValueError) as exc:
        error_console.print(f"[red]Failed to audit citation contexts:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(
        f"Wrote audit report to {out} and {len(quality_flags)} quality flags to {flags}."
    )


@contexts_app.command("resolve-markers")
def resolve_markers(
    contexts: Annotated[
        Path,
        typer.Option("--contexts", help="Path to citation_contexts.parquet."),
    ],
    aligned_graph: Annotated[
        Path,
        typer.Option("--aligned-graph", help="Path to aligned ACL citation graph parquet."),
    ],
    crosswalk: Annotated[
        Path,
        typer.Option("--crosswalk", help="Path to ACL ID crosswalk parquet."),
    ],
    out: Annotated[
        Path,
        typer.Option("--out", help="Output resolved pilot parquet path."),
    ] = DEFAULT_RESOLVED_PILOT_PATH,
    failures: Annotated[
        Path,
        typer.Option("--failures", help="Output unresolved/ambiguous failures parquet path."),
    ] = DEFAULT_RESOLUTION_FAILURES_PATH,
    report: Annotated[
        Path,
        typer.Option("--report", help="Output marker resolution pilot report path."),
    ] = DEFAULT_RESOLUTION_REPORT_PATH,
    baseline_metrics: Annotated[
        Path | None,
        typer.Option(
            "--baseline-metrics",
            help="Optional JSON metrics file to use as the before snapshot.",
        ),
    ] = DEFAULT_RESOLUTION_BASELINE_PATH,
    limit: Annotated[
        int | None,
        typer.Option(
            "--limit",
            min=1,
            help="Maximum contexts to process. Omit for full resolution.",
        ),
    ] = None,
    sample: Annotated[
        bool,
        typer.Option("--sample", help="Randomly sample contexts instead of taking the first rows."),
    ] = False,
) -> None:
    """Resolve author-year citation markers against aligned ACL graph candidates."""
    try:
        metrics = resolve_citation_markers_pilot(
            contexts_path=contexts,
            aligned_graph_path=aligned_graph,
            crosswalk_path=crosswalk,
            out_path=out,
            failures_path=failures,
            report_path=report,
            baseline_metrics_path=baseline_metrics,
            limit=limit,
            sample=sample,
        )
    except (FileNotFoundError, OSError, ValueError) as exc:
        error_console.print(f"[red]Failed to resolve citation markers:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(
        f"Processed {metrics['total_input_contexts']} contexts into {metrics['output_rows']} "
        f"resolved rows. Wrote {out}, {failures}, and {report}."
    )


@contexts_app.command("audit-final-resolved")
def audit_final_resolved(
    resolved: Annotated[
        Path,
        typer.Option("--resolved", help="Path to citation_contexts_resolved.parquet."),
    ],
    out: Annotated[
        Path,
        typer.Option("--out", help="Output final resolved audit markdown report path."),
    ] = DEFAULT_FINAL_RESOLVED_AUDIT_REPORT,
    flags: Annotated[
        Path,
        typer.Option("--flags", help="Output row-level final quality flags parquet path."),
    ] = DEFAULT_FINAL_RESOLVED_FLAGS_PATH,
    strong_sample: Annotated[
        Path,
        typer.Option("--strong-sample", help="Output strong resolved review sample CSV path."),
    ] = DEFAULT_STRONG_RESOLVED_SAMPLE_PATH,
    manual_sample: Annotated[
        Path,
        typer.Option("--manual-sample", help="Output mixed manual resolution review CSV path."),
    ] = DEFAULT_MANUAL_RESOLUTION_SAMPLE_PATH,
    analysis_ready: Annotated[
        Path,
        typer.Option(
            "--analysis-ready",
            help="Output analysis-ready strong contexts parquet path.",
        ),
    ] = DEFAULT_ANALYSIS_READY_STRONG_CONTEXTS_PATH,
) -> None:
    """Audit final resolved citation contexts and build analysis-ready strong rows."""
    try:
        metrics = audit_final_resolved_contexts(
            resolved_path=resolved,
            out_report=out,
            flags_path=flags,
            strong_sample_path=strong_sample,
            manual_sample_path=manual_sample,
            analysis_ready_path=analysis_ready,
        )
    except (FileNotFoundError, OSError, ValueError) as exc:
        error_console.print(f"[red]Failed to audit final resolved contexts:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(
        f"Audited {metrics['total_rows']} resolved rows. "
        f"Analysis-ready strong rows: {metrics['analysis_ready_rows']}. "
        f"Wrote {out}, {flags}, {strong_sample}, {manual_sample}, and {analysis_ready}."
    )


@review_app.command("ingest-resolution")
def ingest_resolution_review(
    strong_sample: Annotated[
        Path,
        typer.Option("--strong-sample", help="Path to strong resolved review sample CSV."),
    ],
    manual_sample: Annotated[
        Path,
        typer.Option("--manual-sample", help="Path to mixed manual review sample CSV."),
    ],
    out: Annotated[
        Path,
        typer.Option("--out", help="Output clean manual review parquet path."),
    ] = DEFAULT_MANUAL_REVIEW_CLEAN_PATH,
    needs_check: Annotated[
        Path,
        typer.Option("--needs-check", help="Output rows needing reviewer cleanup CSV path."),
    ] = DEFAULT_MANUAL_REVIEW_NEEDS_CHECK_PATH,
    report: Annotated[
        Path,
        typer.Option("--report", help="Output manual resolution review report path."),
    ] = DEFAULT_MANUAL_REVIEW_REPORT,
) -> None:
    """Ingest manual resolution review CSVs and report precision."""
    try:
        metrics = ingest_manual_resolution_review(
            strong_sample_path=strong_sample,
            manual_sample_path=manual_sample,
            out_path=out,
            needs_check_path=needs_check,
            report_path=report,
        )
    except (FileNotFoundError, OSError, ValueError) as exc:
        error_console.print(f"[red]Failed to ingest manual resolution review:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(
        f"Ingested {metrics['total_rows']} review rows; "
        f"reviewed={metrics['reviewed_rows']}, "
        f"unreviewed={metrics['unreviewed_rows']}. "
        f"Wrote {out}, {needs_check}, and {report}."
    )


@review_app.command("llm-objects")
def review_llm_objects(
    object_mentions: Annotated[
        Path,
        typer.Option("--object-mentions", help="Path to object mentions sample parquet."),
    ] = DEFAULT_LLM_REVIEW_OBJECT_MENTIONS_PATH,
    cited_title_profiles: Annotated[
        Path,
        typer.Option(
            "--cited-title-profiles",
            help="Path to cited-title object profile parquet.",
        ),
    ] = DEFAULT_LLM_REVIEW_TITLE_PROFILES_PATH,
    contexts: Annotated[
        Path,
        typer.Option("--contexts", help="Path to analysis-ready strong contexts parquet."),
    ] = DEFAULT_LLM_REVIEW_CONTEXTS_PATH,
    registry: Annotated[
        Path,
        typer.Option("--registry", help="Path to object registry YAML."),
    ] = DEFAULT_LLM_REVIEW_REGISTRY_PATH,
    sample_out: Annotated[
        Path,
        typer.Option("--sample-out", help="Output LLM review sample CSV path."),
    ] = DEFAULT_LLM_OBJECT_REVIEW_SAMPLE_PATH,
    jsonl_out: Annotated[
        Path,
        typer.Option("--jsonl-out", help="Output LLM review JSONL results path."),
    ] = DEFAULT_LLM_OBJECT_REVIEW_JSONL_PATH,
    parquet_out: Annotated[
        Path,
        typer.Option("--parquet-out", help="Output LLM review parquet results path."),
    ] = DEFAULT_LLM_OBJECT_REVIEW_PARQUET_PATH,
    report: Annotated[
        Path,
        typer.Option("--report", help="Output LLM-as-judge review report path."),
    ] = DEFAULT_LLM_OBJECT_REVIEW_REPORT,
    limit: Annotated[
        int,
        typer.Option("--limit", min=1, help="Maximum sampled rows to review."),
    ] = 200,
    model: Annotated[
        str | None,
        typer.Option(
            "--model",
            help="OpenAI model name. Defaults to OPENAI_REVIEW_MODEL or project default.",
        ),
    ] = None,
    seed: Annotated[
        int,
        typer.Option("--seed", help="Deterministic sampling seed."),
    ] = 42,
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Generate sample and prompts without API calls."),
    ] = False,
) -> None:
    """Run an LLM-as-judge audit for extracted object mentions."""
    try:
        metrics = run_llm_object_review(
            object_mentions_path=object_mentions,
            cited_title_profiles_path=cited_title_profiles,
            contexts_path=contexts,
            registry_path=registry,
            sample_out=sample_out,
            jsonl_out=jsonl_out,
            parquet_out=parquet_out,
            report_path=report,
            limit=limit,
            model=model,
            seed=seed,
            dry_run=dry_run,
        )
    except (FileNotFoundError, OSError, ValueError) as exc:
        error_console.print(f"[red]Failed to run LLM object review:[/red] {exc}")
        raise typer.Exit(1) from exc

    mode = "dry-run prompts" if dry_run else "model review rows"
    completed_rows = (
        metrics["dry_run_prompt_records"] if dry_run else metrics["reviewed_rows"]
    )
    console.print(
        f"Prepared {metrics['sample_rows']} object mention review rows; "
        f"{completed_rows} {mode}. "
        f"Wrote {sample_out}, {jsonl_out}, {parquet_out}, and {report}."
    )


@review_app.command("llm-phase1")
def review_llm_phase1(
    candidates: Annotated[
        Path,
        typer.Option("--candidates", help="Path to refined Phase-1 candidates parquet."),
    ] = DEFAULT_PHASE1_CANDIDATES_PILOT_REFINED_PATH,
    features: Annotated[
        Path,
        typer.Option("--features", help="Path to refined Phase-1 features parquet."),
    ] = DEFAULT_PHASE1_FEATURES_PILOT_REFINED_PATH,
    contexts: Annotated[
        Path,
        typer.Option("--contexts", help="Path to analysis-ready strong contexts parquet."),
    ] = DEFAULT_PHASE1_CONTEXTS_PATH,
    object_mentions: Annotated[
        Path,
        typer.Option("--object-mentions", help="Path to object mentions parquet."),
    ] = DEFAULT_PHASE1_OBJECT_MENTIONS_PATH,
    object_graph_candidates: Annotated[
        Path,
        typer.Option("--object-graph-candidates", help="Path to object graph candidates parquet."),
    ] = DEFAULT_PHASE1_OBJECT_GRAPH_CANDIDATES_PATH,
    cited_title_profiles: Annotated[
        Path,
        typer.Option("--cited-title-profiles", help="Path to cited-title profiles parquet."),
    ] = DEFAULT_PHASE1_CITED_TITLE_PROFILES_PATH,
    sample_out: Annotated[
        Path,
        typer.Option("--sample-out", help="Output Phase-1 LLM review sample CSV path."),
    ] = DEFAULT_PHASE1_LLM_REVIEW_SAMPLE_PATH,
    jsonl_out: Annotated[
        Path,
        typer.Option("--jsonl-out", help="Output Phase-1 LLM review JSONL path."),
    ] = DEFAULT_PHASE1_LLM_REVIEW_JSONL_PATH,
    parquet_out: Annotated[
        Path,
        typer.Option("--parquet-out", help="Output Phase-1 LLM review parquet path."),
    ] = DEFAULT_PHASE1_LLM_REVIEW_PARQUET_PATH,
    report: Annotated[
        Path,
        typer.Option("--report", help="Output Phase-1 LLM-as-judge report path."),
    ] = DEFAULT_PHASE1_LLM_REVIEW_REPORT,
    recommendations: Annotated[
        Path,
        typer.Option("--recommendations", help="Output rule recommendations report path."),
    ] = DEFAULT_PHASE1_LLM_RECOMMENDATIONS_REPORT,
    cache_dir: Annotated[
        Path,
        typer.Option("--cache-dir", help="Local cache directory for model review results."),
    ] = DEFAULT_PHASE1_LLM_CACHE_DIR,
    limit: Annotated[
        int,
        typer.Option("--limit", min=1, help="Maximum sampled rows to review."),
    ] = 200,
    model: Annotated[
        str | None,
        typer.Option(
            "--model",
            help="OpenAI model name. Defaults to OPENAI_REVIEW_MODEL or project default.",
        ),
    ] = None,
    seed: Annotated[
        int,
        typer.Option("--seed", help="Deterministic sampling seed."),
    ] = 42,
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Generate sample and prompts without API calls."),
    ] = False,
) -> None:
    """Run an LLM-as-judge audit for refined Phase-1 candidate labels."""
    try:
        metrics = run_phase1_llm_review(
            candidates_path=candidates,
            features_path=features,
            contexts_path=contexts,
            object_mentions_path=object_mentions,
            object_graph_candidates_path=object_graph_candidates,
            cited_title_profiles_path=cited_title_profiles,
            sample_out=sample_out,
            jsonl_out=jsonl_out,
            parquet_out=parquet_out,
            report_path=report,
            recommendations_path=recommendations,
            cache_dir=cache_dir,
            limit=limit,
            model=model,
            seed=seed,
            dry_run=dry_run,
        )
    except (FileNotFoundError, OSError, ValueError) as exc:
        error_console.print(f"[red]Failed to run Phase-1 LLM review:[/red] {exc}")
        raise typer.Exit(1) from exc

    mode = "dry-run prompts" if dry_run else "model review rows"
    completed_rows = metrics["dry_run_prompt_records"] if dry_run else metrics["reviewed_rows"]
    console.print(
        f"Prepared {metrics['total_sampled_rows']} Phase-1 review rows; "
        f"{completed_rows} {mode}. "
        f"Wrote {sample_out}, {jsonl_out}, {parquet_out}, {report}, and "
        f"{recommendations}."
    )


@phase1_app.command("screen")
def screen_phase1(
    contexts: Annotated[
        Path,
        typer.Option("--contexts", help="Path to analysis_ready_strong_contexts.parquet."),
    ] = DEFAULT_PHASE1_CONTEXTS_PATH,
    object_mentions: Annotated[
        Path,
        typer.Option("--object-mentions", help="Path to object_mentions.parquet."),
    ] = DEFAULT_PHASE1_OBJECT_MENTIONS_PATH,
    object_graph_candidates: Annotated[
        Path,
        typer.Option(
            "--object-graph-candidates",
            help="Path to object_graph_candidate_mentions.parquet.",
        ),
    ] = DEFAULT_PHASE1_OBJECT_GRAPH_CANDIDATES_PATH,
    cited_title_profiles: Annotated[
        Path,
        typer.Option(
            "--cited-title-profiles",
            help="Path to cited_title_object_profiles.parquet.",
        ),
    ] = DEFAULT_PHASE1_CITED_TITLE_PROFILES_PATH,
    out_candidates: Annotated[
        Path,
        typer.Option("--out-candidates", help="Output Phase-1 candidate parquet path."),
    ] = DEFAULT_PHASE1_CANDIDATES_PILOT_PATH,
    out_features: Annotated[
        Path,
        typer.Option("--out-features", help="Output Phase-1 context feature parquet path."),
    ] = DEFAULT_PHASE1_FEATURES_PILOT_PATH,
    report: Annotated[
        Path,
        typer.Option("--report", help="Output Phase-1 markdown report path."),
    ] = DEFAULT_PHASE1_REPORT_PILOT_PATH,
    limit: Annotated[
        int | None,
        typer.Option(
            "--limit",
            min=1,
            help="Maximum context rows to process. Default is the 100000-row pilot.",
        ),
    ] = DEFAULT_PHASE1_LIMIT,
    seed: Annotated[
        int,
        typer.Option("--seed", help="Deterministic report/sample seed."),
    ] = 42,
    refined_rules: Annotated[
        bool,
        typer.Option(
            "--refined-rules",
            help="Use tightened Task 9A.1 rules and write refined pilot outputs.",
        ),
    ] = False,
) -> None:
    """Run rule-based Phase-1 citation-function candidate screening."""
    try:
        if refined_rules:
            if out_candidates == DEFAULT_PHASE1_CANDIDATES_PILOT_PATH:
                out_candidates = DEFAULT_PHASE1_CANDIDATES_PILOT_REFINED_PATH
            if out_features == DEFAULT_PHASE1_FEATURES_PILOT_PATH:
                out_features = DEFAULT_PHASE1_FEATURES_PILOT_REFINED_PATH
            if report == DEFAULT_PHASE1_REPORT_PILOT_PATH:
                report = DEFAULT_PHASE1_REPORT_PILOT_REFINED_PATH
        metrics = screen_phase1_citation_functions(
            contexts_path=contexts,
            object_mentions_path=object_mentions,
            object_graph_candidates_path=object_graph_candidates,
            cited_title_profiles_path=cited_title_profiles,
            out_candidates_path=out_candidates,
            out_features_path=out_features,
            report_path=report,
            limit=limit,
            seed=seed,
            refined_rules=refined_rules,
        )
    except (FileNotFoundError, OSError, ValueError) as exc:
        error_console.print(f"[red]Failed to run Phase-1 screening:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(
        f"Processed {metrics['input_contexts_processed']} contexts; "
        f"{metrics['contexts_with_object_mentions']} had object mentions and "
        f"{metrics['contexts_with_graph_candidate_objects']} had graph candidate objects. "
        f"Flagged {metrics['should_send_to_llm_count']} "
        f"({metrics['should_send_to_llm_rate']:.1%}) for LLM review. "
        f"Wrote {out_candidates}, {out_features}, and {report}."
    )


@objects_app.command("match")
def match_objects(
    contexts: Annotated[
        Path,
        typer.Option("--contexts", help="Path to analysis_ready_strong_contexts.parquet."),
    ],
    registry: Annotated[
        Path,
        typer.Option("--registry", help="Path to object registry YAML."),
    ] = DEFAULT_OBJECT_REGISTRY_PATH,
    out: Annotated[
        Path,
        typer.Option("--out", help="Output object mentions parquet path."),
    ] = DEFAULT_OBJECT_MENTIONS_PATH,
    cited_title_profiles: Annotated[
        Path,
        typer.Option(
            "--cited-title-profiles",
            help="Output cited-title object profile parquet path.",
        ),
    ] = DEFAULT_CITED_TITLE_OBJECT_PROFILES_PATH,
    object_graph_candidates: Annotated[
        Path,
        typer.Option(
            "--object-graph-candidates",
            help="Output graph-eligible object mentions parquet path.",
        ),
    ] = DEFAULT_FULL_OBJECT_GRAPH_CANDIDATES_PATH,
    strict_object_graph_candidates: Annotated[
        Path,
        typer.Option(
            "--strict-object-graph-candidates",
            help="Output strict sentence-text graph candidates parquet path.",
        ),
    ] = DEFAULT_STRICT_OBJECT_GRAPH_CANDIDATES_PATH,
    broad_object_graph_candidates: Annotated[
        Path,
        typer.Option(
            "--broad-object-graph-candidates",
            help="Output broad context-window-neighbor graph candidates parquet path.",
        ),
    ] = DEFAULT_BROAD_OBJECT_GRAPH_CANDIDATES_PATH,
    review_sample: Annotated[
        Path,
        typer.Option("--review-sample", help="Output manual object mention review CSV path."),
    ] = DEFAULT_OBJECT_MENTIONS_REVIEW_SAMPLE_PATH,
    report: Annotated[
        Path,
        typer.Option("--report", help="Output object matching report path."),
    ] = DEFAULT_OBJECT_MATCHING_REPORT,
    limit: Annotated[
        int | None,
        typer.Option(
            "--limit",
            min=1,
            help="Maximum context rows to process. Omit for full matching.",
        ),
    ] = None,
) -> None:
    """Match seed NLP object mentions in analysis-ready citation contexts."""
    try:
        metrics = match_objects_in_contexts(
            contexts_path=contexts,
            registry_path=registry,
            out_path=out,
            cited_title_profiles_path=cited_title_profiles,
            object_graph_candidates_path=object_graph_candidates,
            strict_object_graph_candidates_path=strict_object_graph_candidates,
            broad_object_graph_candidates_path=broad_object_graph_candidates,
            review_sample_path=review_sample,
            report_path=report,
            limit=limit,
        )
    except (FileNotFoundError, OSError, ValueError) as exc:
        error_console.print(f"[red]Failed to match objects:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(
        f"Processed {metrics['input_context_rows_processed']} contexts; "
        f"matched {metrics['total_object_mentions']} object mentions in "
        f"{metrics['contexts_with_at_least_one_object_mention']} contexts. "
        f"Graph candidates: {metrics['object_graph_candidate_count']}. "
        f"Wrote {out}, {cited_title_profiles}, {object_graph_candidates}, "
        f"{strict_object_graph_candidates}, {broad_object_graph_candidates}, "
        f"{review_sample}, and {report}."
    )


@objects_app.command("apply-review-policy")
def apply_review_policy(
    object_mentions: Annotated[
        Path,
        typer.Option("--object-mentions", help="Path to refined object mentions parquet."),
    ] = DEFAULT_OBJECT_MENTIONS_REFINED_PATH,
    cited_title_profiles: Annotated[
        Path,
        typer.Option(
            "--cited-title-profiles",
            help="Path to refined cited-title object profiles parquet.",
        ),
    ] = DEFAULT_CITED_TITLE_OBJECT_PROFILES_REFINED_PATH,
    llm_review: Annotated[
        Path,
        typer.Option("--llm-review", help="Path to LLM-as-judge review parquet."),
    ] = DEFAULT_OBJECT_MENTIONS_LLM_REVIEW_PATH,
    registry: Annotated[
        Path,
        typer.Option("--registry", help="Path to updated object registry YAML."),
    ] = DEFAULT_OBJECT_REGISTRY_PATH,
    out_mentions: Annotated[
        Path,
        typer.Option("--out-mentions", help="Output final object mentions parquet path."),
    ] = DEFAULT_OBJECT_MENTIONS_FINAL_PATH,
    out_title_profiles: Annotated[
        Path,
        typer.Option(
            "--out-title-profiles",
            help="Output final cited-title object profiles parquet path.",
        ),
    ] = DEFAULT_CITED_TITLE_OBJECT_PROFILES_FINAL_PATH,
    out_graph_candidates: Annotated[
        Path,
        typer.Option(
            "--out-graph-candidates",
            help="Output object graph candidate mentions parquet path.",
        ),
    ] = DEFAULT_OBJECT_GRAPH_CANDIDATES_PATH,
    policy_report: Annotated[
        Path,
        typer.Option(
            "--policy-report",
            help="Output registry policy update report path.",
        ),
    ] = DEFAULT_OBJECT_REGISTRY_POLICY_REPORT,
    report: Annotated[
        Path,
        typer.Option("--report", help="Output final object matching report path."),
    ] = DEFAULT_OBJECT_MATCHING_FINAL_REPORT,
) -> None:
    """Apply LLM-informed object registry and matching policy updates."""
    try:
        metrics = apply_object_review_policy(
            object_mentions_path=object_mentions,
            cited_title_profiles_path=cited_title_profiles,
            llm_review_path=llm_review,
            registry_path=registry,
            out_mentions=out_mentions,
            out_title_profiles=out_title_profiles,
            out_graph_candidates=out_graph_candidates,
            policy_report=policy_report,
            report=report,
        )
    except (FileNotFoundError, OSError, ValueError) as exc:
        error_console.print(f"[red]Failed to apply object review policy:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(
        f"Applied final object policy to {metrics['final_mentions']} mentions. "
        f"Graph candidates: strict={metrics['strict_graph_candidate_count']}, "
        f"broad={metrics['broad_graph_candidate_count']}. "
        f"Wrote {out_mentions}, {out_title_profiles}, {out_graph_candidates}, "
        f"{policy_report}, and {report}."
    )


@datasets_app.command("load-labeled")
def load_labeled_datasets(
    multicite: Annotated[
        Path,
        typer.Option("--multicite", help="Path to raw MultiCite JSONL/JSON/CSV files."),
    ],
    scicite: Annotated[
        Path,
        typer.Option("--scicite", help="Path to raw SciCite JSONL/JSON/CSV files."),
    ],
    out: Annotated[
        Path,
        typer.Option("--out", help="Output parquet path for normalized labeled contexts."),
    ],
    report: Annotated[
        Path,
        typer.Option("--report", help="Output markdown profile path."),
    ] = DEFAULT_LABELED_REPORT,
) -> None:
    """Load MultiCite and SciCite citation contexts into one normalized parquet file."""
    try:
        multicite_frame = load_multicite(multicite)
        scicite_frame = load_scicite(scicite)
        combined = write_labeled_contexts(
            [multicite_frame, scicite_frame],
            out_path=out,
            report_path=report,
        )
    except (FileNotFoundError, ValueError) as exc:
        error_console.print(f"[red]Failed to load labeled datasets:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(
        f"Wrote {len(combined)} labeled contexts to {out} and profile report to {report}."
    )


def main() -> None:
    app()
