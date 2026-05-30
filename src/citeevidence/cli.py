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
review_app = typer.Typer(help="Ingest human review files.", no_args_is_help=True)
console = Console()
error_console = Console(stderr=True)
DEFAULT_PROJECT_CONFIG = Path("configs/project.yaml")
DEFAULT_LABELED_REPORT = Path("reports/labeled_dataset_profile.md")
DEFAULT_ACL_REPORT = Path("reports/acl_ocl_data_inspection.md")

app.add_typer(acl_app, name="acl")
app.add_typer(config_app, name="config")
app.add_typer(contexts_app, name="contexts")
app.add_typer(datasets_app, name="datasets")
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
