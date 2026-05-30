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
from citeevidence.acl.id_audit import (
    DEFAULT_SCHEMA_ID_AUDIT_REPORT,
    DEFAULT_SCHEMA_INVENTORY_PATH,
    audit_acl_ocl_ids,
)
from citeevidence.acl.inspector import DEFAULT_INVENTORY_PATH, inspect_acl_ocl_data
from citeevidence.acl.reader import parse_acl_ocl_data
from citeevidence.config import ConfigLoadError, load_project_config
from citeevidence.contexts.audit import DEFAULT_CONTEXT_FLAGS_PATH, audit_citation_contexts
from citeevidence.contexts.extract import extract_citation_contexts
from citeevidence.contexts.resolve import (
    DEFAULT_RESOLUTION_FAILURES_PATH,
    DEFAULT_RESOLUTION_REPORT_PATH,
    DEFAULT_RESOLVED_PILOT_PATH,
    resolve_citation_markers_pilot,
)
from citeevidence.datasets.multicite import load_multicite
from citeevidence.datasets.normalize import write_labeled_contexts
from citeevidence.datasets.scicite import load_scicite

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
console = Console()
error_console = Console(stderr=True)
DEFAULT_PROJECT_CONFIG = Path("configs/project.yaml")
DEFAULT_LABELED_REPORT = Path("reports/labeled_dataset_profile.md")
DEFAULT_ACL_REPORT = Path("reports/acl_ocl_data_inspection.md")

app.add_typer(acl_app, name="acl")
app.add_typer(config_app, name="config")
app.add_typer(contexts_app, name="contexts")
app.add_typer(datasets_app, name="datasets")


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
    references: Annotated[
        Path,
        typer.Option("--references", help="Path to acl_references.parquet."),
    ],
    out: Annotated[
        Path,
        typer.Option("--out", help="Output parquet path for citation contexts."),
    ],
    max_window_chars: Annotated[
        int,
        typer.Option(
            "--max-window-chars",
            min=100,
            help="Maximum characters retained in bounded context windows.",
        ),
    ] = 2000,
) -> None:
    """Extract citation contexts from parsed ACL sections and references."""
    try:
        contexts = extract_citation_contexts(
            sections_path=sections,
            references_path=references,
            out_path=out,
            max_window_chars=max_window_chars,
        )
    except (FileNotFoundError, OSError, ValueError) as exc:
        error_console.print(f"[red]Failed to extract citation contexts:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(f"Wrote {len(contexts)} citation contexts to {out}.")


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
    limit: Annotated[
        int,
        typer.Option("--limit", min=1, help="Maximum contexts to process for the pilot."),
    ] = 100_000,
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
