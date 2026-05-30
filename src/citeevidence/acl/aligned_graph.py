from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import pyarrow.parquet as pq

DEFAULT_CROSSWALK_PATH = Path("data/interim/acl_id_crosswalk.parquet")
DEFAULT_ALIGNED_GRAPH_PATH = Path("data/interim/acl_citation_graph_aligned.parquet")
DEFAULT_ALIGNMENT_REPORT_PATH = Path("reports/acl_citation_graph_alignment_report.md")

CROSSWALK_COLUMNS = [
    "acl_id",
    "corpus_paper_id",
    "title",
    "year",
    "authors",
    "doi",
    "venue",
    "url",
    "numcitedby",
]
ALIGNED_GRAPH_COLUMNS = [
    "graph_edge_id",
    "citing_acl_id",
    "citing_corpus_paper_id",
    "citing_title",
    "citing_year",
    "citing_authors",
    "citing_doi",
    "cited_acl_id",
    "cited_corpus_paper_id",
    "cited_title",
    "cited_year",
    "cited_authors",
    "cited_doi",
    "is_citingpaperid_acl",
    "is_citedpaperid_acl",
    "alignment_status",
]
GRAPH_COLUMNS = [
    "id",
    "citingpaperid",
    "citedpaperid",
    "is_citingpaperid_acl",
    "is_citedpaperid_acl",
]
CONTEXT_SAMPLE_COLUMNS = [
    "context_id",
    "citing_paper_id",
    "paragraph_id",
    "citation_marker",
    "sentence_text",
]


def build_aligned_acl_citation_graph(
    *,
    publication_info_path: str | Path,
    onlygraph_path: str | Path,
    contexts_path: str | Path,
    out_crosswalk: str | Path = DEFAULT_CROSSWALK_PATH,
    out_graph: str | Path = DEFAULT_ALIGNED_GRAPH_PATH,
    report_path: str | Path = DEFAULT_ALIGNMENT_REPORT_PATH,
    sample_size: int = 20,
) -> dict[str, Any]:
    """Build an ACL-ID-aligned citation graph from ACL-OCL publication metadata."""
    if sample_size < 1:
        raise ValueError("sample_size must be positive")

    publication_path = Path(publication_info_path)
    graph_path = Path(onlygraph_path)
    contexts = Path(contexts_path)
    for path in (publication_path, graph_path, contexts):
        if not path.exists():
            raise FileNotFoundError(f"Required input does not exist: {path}")

    publication_rows = pq.ParquetFile(publication_path).metadata.num_rows
    onlygraph_rows = pq.ParquetFile(graph_path).metadata.num_rows

    crosswalk = build_acl_id_crosswalk(publication_path)
    crosswalk_output = Path(out_crosswalk)
    crosswalk_output.parent.mkdir(parents=True, exist_ok=True)
    crosswalk.to_parquet(crosswalk_output, index=False)

    graph = build_aligned_graph_frame(graph_path, crosswalk)
    graph_output = Path(out_graph)
    graph_output.parent.mkdir(parents=True, exist_ok=True)
    graph.to_parquet(graph_output, index=False)

    metrics = build_alignment_metrics(
        publication_rows=publication_rows,
        onlygraph_rows=onlygraph_rows,
        crosswalk=crosswalk,
        graph=graph,
        contexts_path=contexts,
        sample_size=sample_size,
    )
    report = build_alignment_report(
        metrics=metrics,
        publication_info_path=publication_path,
        onlygraph_path=graph_path,
        contexts_path=contexts,
        out_crosswalk=crosswalk_output,
        out_graph=graph_output,
    )
    report_output = Path(report_path)
    report_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.write_text(report, encoding="utf-8")
    return metrics


def build_acl_id_crosswalk(publication_info_path: str | Path) -> pd.DataFrame:
    """Build the deduplicated ACL ID to corpus paper ID crosswalk."""
    path = Path(publication_info_path)
    available = set(pq.ParquetFile(path).schema_arrow.names)
    required = {"acl_id", "corpus_paper_id"}
    missing = sorted(required - available)
    if missing:
        raise ValueError(f"Publication metadata missing required columns: {', '.join(missing)}")

    read_columns = [
        column
        for column in [
            "acl_id",
            "corpus_paper_id",
            "title",
            "year",
            "author",
            "authors",
            "doi",
            "booktitle",
            "journal",
            "publisher",
            "venue",
            "url",
            "numcitedby",
        ]
        if column in available
    ]
    frame = pd.read_parquet(path, columns=read_columns).copy()
    crosswalk = pd.DataFrame()
    crosswalk["acl_id"] = frame["acl_id"].map(_clean_string)
    crosswalk["corpus_paper_id"] = _integer_series(frame["corpus_paper_id"])
    crosswalk["title"] = _optional_clean_series(frame, "title")
    crosswalk["year"] = _optional_clean_series(frame, "year")
    crosswalk["authors"] = _first_available_series(frame, ["author", "authors"])
    crosswalk["doi"] = _optional_clean_series(frame, "doi")
    crosswalk["venue"] = _first_available_series(
        frame,
        ["venue", "booktitle", "journal", "publisher"],
    )
    crosswalk["url"] = _optional_clean_series(frame, "url")
    crosswalk["numcitedby"] = (
        pd.to_numeric(frame["numcitedby"], errors="coerce").astype("Int64")
        if "numcitedby" in frame
        else pd.Series(pd.NA, index=frame.index, dtype="Int64")
    )
    crosswalk = crosswalk.dropna(subset=["acl_id", "corpus_paper_id"])
    return crosswalk.drop_duplicates(subset=["corpus_paper_id"], keep="first").reset_index(
        drop=True
    )[CROSSWALK_COLUMNS]


def build_aligned_graph_frame(
    onlygraph_path: str | Path,
    crosswalk: pd.DataFrame,
) -> pd.DataFrame:
    """Join ACL-only graph numeric IDs to ACL publication metadata on both endpoints."""
    path = Path(onlygraph_path)
    available = set(pq.ParquetFile(path).schema_arrow.names)
    missing = sorted(set(GRAPH_COLUMNS) - available)
    if missing:
        raise ValueError(f"ACL-only graph missing required columns: {', '.join(missing)}")

    graph = pd.read_parquet(path, columns=GRAPH_COLUMNS).copy()
    graph["graph_edge_id"] = _integer_series(graph["id"])
    graph["citing_corpus_paper_id"] = _integer_series(graph["citingpaperid"])
    graph["cited_corpus_paper_id"] = _integer_series(graph["citedpaperid"])

    citing = _endpoint_crosswalk(crosswalk, "citing")
    cited = _endpoint_crosswalk(crosswalk, "cited")
    aligned = graph.merge(citing, on="citing_corpus_paper_id", how="left")
    aligned = aligned.merge(cited, on="cited_corpus_paper_id", how="left")
    aligned["alignment_status"] = _alignment_status(aligned)
    aligned = aligned.rename(
        columns={
            "is_citingpaperid_acl": "is_citingpaperid_acl",
            "is_citedpaperid_acl": "is_citedpaperid_acl",
        }
    )
    return aligned[ALIGNED_GRAPH_COLUMNS]


def build_alignment_metrics(
    *,
    publication_rows: int,
    onlygraph_rows: int,
    crosswalk: pd.DataFrame,
    graph: pd.DataFrame,
    contexts_path: Path,
    sample_size: int,
) -> dict[str, Any]:
    """Compute report metrics for the aligned ACL citation graph."""
    total = len(graph)
    citing_aligned = int(graph["citing_acl_id"].notna().sum())
    cited_aligned = int(graph["cited_acl_id"].notna().sum())
    both_aligned = int(
        (graph["citing_acl_id"].notna() & graph["cited_acl_id"].notna()).sum()
    )
    context_coverage = _context_coverage(contexts_path, set(graph["citing_acl_id"].dropna()))
    return {
        "publication_info_rows": int(publication_rows),
        "acl_id_crosswalk_rows": int(len(crosswalk)),
        "acl_onlygraph_rows": int(onlygraph_rows),
        "aligned_graph_edges": both_aligned,
        "citing_side_alignment_rate": _rate(citing_aligned, total),
        "cited_side_alignment_rate": _rate(cited_aligned, total),
        "both_sides_alignment_rate": _rate(both_aligned, total),
        "unique_citing_acl_papers": int(graph["citing_acl_id"].nunique(dropna=True)),
        "unique_cited_acl_papers": int(graph["cited_acl_id"].nunique(dropna=True)),
        "citation_contexts_citing_paper_id_coverage": context_coverage["coverage_rate"],
        "citation_contexts_unique_citing_paper_ids": context_coverage["unique_context_ids"],
        "citation_contexts_covered_citing_paper_ids": context_coverage["covered_ids"],
        "cited_title_non_empty_rate": _non_empty_rate(graph["cited_title"]),
        "cited_year_non_empty_rate": _non_empty_rate(graph["cited_year"]),
        "cited_authors_non_empty_rate": _non_empty_rate(graph["cited_authors"]),
        "cited_doi_non_empty_rate": _non_empty_rate(graph["cited_doi"]),
        "alignment_status_distribution": _records(
            graph.groupby("alignment_status", dropna=False)
            .size()
            .reset_index(name="edges")
            .sort_values("edges", ascending=False)
        ),
        "sample_aligned_edges": _records(_sample_aligned_edges(graph, sample_size)),
        "uncovered_context_samples": context_coverage["uncovered_context_samples"],
    }


def build_alignment_report(
    *,
    metrics: dict[str, Any],
    publication_info_path: Path,
    onlygraph_path: Path,
    contexts_path: Path,
    out_crosswalk: Path,
    out_graph: Path,
) -> str:
    """Build the markdown report for the aligned citation graph."""
    core_metrics = [
        {"metric": "publication_info row count", "value": metrics["publication_info_rows"]},
        {"metric": "acl_id_crosswalk row count", "value": metrics["acl_id_crosswalk_rows"]},
        {"metric": "acl_onlygraph row count", "value": metrics["acl_onlygraph_rows"]},
        {"metric": "aligned graph edges", "value": metrics["aligned_graph_edges"]},
        {
            "metric": "citing side alignment rate",
            "value": metrics["citing_side_alignment_rate"],
        },
        {"metric": "cited side alignment rate", "value": metrics["cited_side_alignment_rate"]},
        {"metric": "both sides alignment rate", "value": metrics["both_sides_alignment_rate"]},
        {"metric": "unique citing ACL papers", "value": metrics["unique_citing_acl_papers"]},
        {"metric": "unique cited ACL papers", "value": metrics["unique_cited_acl_papers"]},
        {
            "metric": "citation_contexts.citing_paper_id coverage",
            "value": metrics["citation_contexts_citing_paper_id_coverage"],
        },
        {"metric": "cited_title non-empty rate", "value": metrics["cited_title_non_empty_rate"]},
        {"metric": "cited_year non-empty rate", "value": metrics["cited_year_non_empty_rate"]},
        {
            "metric": "cited_authors non-empty rate",
            "value": metrics["cited_authors_non_empty_rate"],
        },
        {"metric": "cited_doi non-empty rate", "value": metrics["cited_doi_non_empty_rate"]},
    ]
    sections = [
        "# ACL Citation Graph Alignment Report",
        "",
        "## Inputs",
        _table(
            [
                {"name": "publication_info", "path": publication_info_path},
                {"name": "acl_onlygraph", "path": onlygraph_path},
                {"name": "citation_contexts", "path": contexts_path},
            ]
        ),
        "",
        "## Outputs",
        _table(
            [
                {"name": "acl_id_crosswalk", "path": out_crosswalk},
                {"name": "acl_citation_graph_aligned", "path": out_graph},
            ]
        ),
        "",
        "## Core Metrics",
        _table(core_metrics),
        "",
        "## Alignment Status Distribution",
        _table(metrics["alignment_status_distribution"]),
        "",
        "## Sample 20 Aligned Edges",
        _table(metrics["sample_aligned_edges"]),
        "",
        "## Contexts Not Covered By Aligned Citing ACL IDs",
        _table(metrics["uncovered_context_samples"]),
        "",
        "## Notes",
        (
            "This table is a candidate ACL-to-ACL citation graph. It does not resolve "
            "individual citation markers to bibliography entries. Numeric markers such as "
            "`[12]` still require local bibliography order, and author-year markers should "
            "be resolved in a later task."
        ),
        "",
    ]
    return "\n".join(sections)


def _endpoint_crosswalk(crosswalk: pd.DataFrame, prefix: str) -> pd.DataFrame:
    renamed = crosswalk.rename(
        columns={
            "acl_id": f"{prefix}_acl_id",
            "corpus_paper_id": f"{prefix}_corpus_paper_id",
            "title": f"{prefix}_title",
            "year": f"{prefix}_year",
            "authors": f"{prefix}_authors",
            "doi": f"{prefix}_doi",
        }
    )
    return renamed[
        [
            f"{prefix}_acl_id",
            f"{prefix}_corpus_paper_id",
            f"{prefix}_title",
            f"{prefix}_year",
            f"{prefix}_authors",
            f"{prefix}_doi",
        ]
    ]


def _alignment_status(frame: pd.DataFrame) -> pd.Series:
    citing = frame["citing_acl_id"].notna()
    cited = frame["cited_acl_id"].notna()
    status = pd.Series("missing_both", index=frame.index, dtype="string")
    status.loc[citing & cited] = "both_aligned"
    status.loc[~citing & cited] = "missing_citing"
    status.loc[citing & ~cited] = "missing_cited"
    return status


def _context_coverage(contexts_path: Path, aligned_citing_acl_ids: set[str]) -> dict[str, Any]:
    contexts = pd.read_parquet(contexts_path, columns=CONTEXT_SAMPLE_COLUMNS).copy()
    contexts["citing_paper_id"] = contexts["citing_paper_id"].map(_clean_string)
    unique_context_ids = set(contexts["citing_paper_id"].dropna())
    covered = unique_context_ids & aligned_citing_acl_ids
    uncovered = sorted(unique_context_ids - aligned_citing_acl_ids)
    sample = contexts.loc[contexts["citing_paper_id"].isin(uncovered)].head(20).copy()
    sample["sentence_text"] = sample["sentence_text"].map(lambda value: _truncate(value, 180))
    return {
        "unique_context_ids": int(len(unique_context_ids)),
        "covered_ids": int(len(covered)),
        "coverage_rate": _rate(len(covered), len(unique_context_ids)),
        "uncovered_context_samples": _records(sample),
    }


def _sample_aligned_edges(graph: pd.DataFrame, sample_size: int) -> pd.DataFrame:
    sample = graph.loc[graph["alignment_status"].eq("both_aligned")].head(sample_size).copy()
    columns = [
        "graph_edge_id",
        "citing_acl_id",
        "citing_title",
        "citing_year",
        "cited_acl_id",
        "cited_title",
        "cited_year",
        "alignment_status",
    ]
    for column in ("citing_title", "cited_title"):
        sample[column] = sample[column].map(lambda value: _truncate(value, 120))
    return sample[columns]


def _first_available_series(frame: pd.DataFrame, columns: list[str]) -> pd.Series:
    result = pd.Series(pd.NA, index=frame.index, dtype="string")
    for column in columns:
        if column not in frame:
            continue
        values = _optional_clean_series(frame, column)
        result = result.where(result.notna(), values)
    return result


def _optional_clean_series(frame: pd.DataFrame, column: str) -> pd.Series:
    if column not in frame:
        return pd.Series(pd.NA, index=frame.index, dtype="string")
    return frame[column].map(_clean_string).astype("string")


def _integer_series(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").astype("Int64")


def _clean_string(value: Any) -> str | None:
    if value is None or pd.isna(value):
        return None
    text = str(value).strip()
    return text or None


def _non_empty_rate(series: pd.Series) -> str:
    return _rate(int(series.map(_clean_string).notna().sum()), len(series))


def _rate(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.000"
    return f"{numerator / denominator:.3f}"


def _records(frame: pd.DataFrame) -> list[dict[str, Any]]:
    if frame.empty:
        return []
    clean = frame.where(pd.notna(frame), None)
    return [
        {key: _json_value(value) for key, value in row.items()}
        for row in clean.to_dict(orient="records")
    ]


def _json_value(value: Any) -> Any:
    if value is None or pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def _truncate(value: Any, max_chars: int) -> str:
    text = _clean_string(value) or ""
    text = text.replace("\n", " ")
    if len(text) <= max_chars:
        return text
    return f"{text[: max_chars - 3]}..."


def _table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "No records available."
    columns = list(dict.fromkeys(column for row in rows for column in row))
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = [_markdown_cell(row.get(column)) for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def _markdown_cell(value: Any) -> str:
    if value is None or pd.isna(value):
        return "unavailable"
    return _truncate(value, 140).replace("|", "\\|")
