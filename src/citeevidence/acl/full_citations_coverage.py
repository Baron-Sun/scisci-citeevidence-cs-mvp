from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import pyarrow.parquet as pq

from citeevidence.acl.aligned_graph import build_acl_id_crosswalk
from citeevidence.contexts.resolve import _candidate_surnames, _year_string

DEFAULT_FULL_CITATIONS_SAFE_ALIGNED_PATH = Path(
    "data/interim/acl_full_citations_safe_aligned.parquet"
)
DEFAULT_FULL_CITATIONS_COVERAGE_REPORT = Path(
    "reports/full_citations_candidate_coverage_report.md"
)
DEFAULT_ONLYGRAPH_ALIGNED_PATH = Path("data/interim/acl_citation_graph_aligned.parquet")
DEFAULT_RESOLVED_PILOT_PATH = Path("data/processed/citation_contexts_resolved_pilot.parquet")
DEFAULT_CONTEXTS_PATH = Path("data/processed/citation_contexts.parquet")
FULL_CITATIONS_COLUMNS = [
    "id",
    "citingpaperid",
    "citedpaperid",
    "is_citedpaperid_acl",
    "is_citingpaperid_acl",
]
SAFE_ALIGNED_COLUMNS = [
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
    "candidate_source",
]
ONLYGRAPH_READ_COLUMNS = [
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
]
RESOLVED_READ_COLUMNS = [
    "context_id",
    "source_context_id",
    "citing_paper_id",
    "citation_marker",
    "marker_component_text",
    "parsed_surnames",
    "parsed_year",
    "resolution_status",
    "resolution_method",
    "sentence_text",
]


@dataclass(frozen=True)
class FullCitationsCoverageResult:
    safe_full_citations: pd.DataFrame
    metrics: dict[str, Any]


def evaluate_full_citations_candidate_coverage(
    *,
    full_citations_path: str | Path,
    publication_info_path: str | Path,
    onlygraph_aligned_path: str | Path = DEFAULT_ONLYGRAPH_ALIGNED_PATH,
    resolved_pilot_path: str | Path = DEFAULT_RESOLVED_PILOT_PATH,
    contexts_path: str | Path = DEFAULT_CONTEXTS_PATH,
    out_safe_aligned: str | Path = DEFAULT_FULL_CITATIONS_SAFE_ALIGNED_PATH,
    report_path: str | Path = DEFAULT_FULL_CITATIONS_COVERAGE_REPORT,
    sample_size: int = 20,
) -> FullCitationsCoverageResult:
    """Evaluate safe `acl_full_citations` candidates without using them for resolution."""
    if sample_size < 1:
        raise ValueError("sample_size must be positive")
    paths = [
        Path(full_citations_path),
        Path(publication_info_path),
        Path(onlygraph_aligned_path),
        Path(resolved_pilot_path),
        Path(contexts_path),
    ]
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"Required input does not exist: {path}")

    full_citations_rows = pq.ParquetFile(full_citations_path).metadata.num_rows
    contexts_rows = pq.ParquetFile(contexts_path).metadata.num_rows
    crosswalk = build_acl_id_crosswalk(publication_info_path)
    safe_full = build_safe_full_citations_aligned(full_citations_path, crosswalk)

    output = Path(out_safe_aligned)
    output.parent.mkdir(parents=True, exist_ok=True)
    safe_full.to_parquet(output, index=False)

    onlygraph = pd.read_parquet(onlygraph_aligned_path, columns=ONLYGRAPH_READ_COLUMNS)
    resolved = pd.read_parquet(resolved_pilot_path, columns=RESOLVED_READ_COLUMNS)
    metrics = build_full_citations_coverage_metrics(
        full_citations_rows=full_citations_rows,
        contexts_rows=contexts_rows,
        crosswalk=crosswalk,
        onlygraph=onlygraph,
        safe_full=safe_full,
        resolved=resolved,
        sample_size=sample_size,
    )
    report = build_full_citations_coverage_report(
        metrics=metrics,
        full_citations_path=Path(full_citations_path),
        publication_info_path=Path(publication_info_path),
        onlygraph_aligned_path=Path(onlygraph_aligned_path),
        resolved_pilot_path=Path(resolved_pilot_path),
        contexts_path=Path(contexts_path),
        out_safe_aligned=output,
    )
    report_output = Path(report_path)
    report_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.write_text(report, encoding="utf-8")
    return FullCitationsCoverageResult(safe_full_citations=safe_full, metrics=metrics)


def build_safe_full_citations_aligned(
    full_citations_path: str | Path,
    crosswalk: pd.DataFrame,
) -> pd.DataFrame:
    """Align `acl_full_citations` edges whose numeric endpoints both map to ACL metadata."""
    full = pd.read_parquet(full_citations_path, columns=FULL_CITATIONS_COLUMNS).copy()
    full["graph_edge_id"] = _integer_series(full["id"])
    full["citing_corpus_paper_id"] = _integer_series(full["citingpaperid"])
    full["cited_corpus_paper_id"] = _integer_series(full["citedpaperid"])

    citing = _endpoint_crosswalk(crosswalk, "citing")
    cited = _endpoint_crosswalk(crosswalk, "cited")
    aligned = full.merge(citing, on="citing_corpus_paper_id", how="left")
    aligned = aligned.merge(cited, on="cited_corpus_paper_id", how="left")
    safe = aligned.loc[
        aligned["citing_acl_id"].notna() & aligned["cited_acl_id"].notna()
    ].copy()
    safe["alignment_status"] = "both_aligned"
    safe["candidate_source"] = "full_citations"
    return safe[SAFE_ALIGNED_COLUMNS].reset_index(drop=True)


def build_full_citations_coverage_metrics(
    *,
    full_citations_rows: int,
    contexts_rows: int,
    crosswalk: pd.DataFrame,
    onlygraph: pd.DataFrame,
    safe_full: pd.DataFrame,
    resolved: pd.DataFrame,
    sample_size: int,
) -> dict[str, Any]:
    only_edges = _candidate_edges(onlygraph, "onlygraph")
    full_edges = _candidate_edges(safe_full, "full_citations")
    union_edges = _union_candidate_edges(only_edges, full_edges)
    only_pairs = _edge_pairs(only_edges)
    full_pairs = _edge_pairs(full_edges)
    union_pairs = _edge_pairs(union_edges)
    additional_pairs = full_pairs - only_pairs

    unresolved = _bibliography_unresolved_author_year_rows(resolved)
    only_index = _candidate_index(only_edges)
    full_index = _candidate_index(full_edges)
    union_index = _candidate_index(union_edges)
    coverage = _coverage_for_unresolved_rows(
        unresolved,
        only_index=only_index,
        full_index=full_index,
        union_index=union_index,
        sample_size=sample_size,
    )

    return {
        "full_citations_total_rows": int(full_citations_rows),
        "publication_crosswalk_rows": int(len(crosswalk)),
        "citation_contexts_rows": int(contexts_rows),
        "safe_full_citations_rows": int(len(safe_full)),
        "onlygraph_unique_candidate_edges": int(len(only_pairs)),
        "full_citations_safe_unique_candidate_edges": int(len(full_pairs)),
        "union_unique_candidate_edges": int(len(union_pairs)),
        "additional_candidate_edges_beyond_onlygraph": int(len(additional_pairs)),
        "additional_citing_acl_papers": int(
            len(
                set(full_edges["citing_acl_id"].dropna())
                - set(only_edges["citing_acl_id"].dropna())
            )
        ),
        "additional_cited_acl_papers": int(
            len(set(full_edges["cited_acl_id"].dropna()) - set(only_edges["cited_acl_id"].dropna()))
        ),
        "safe_full_citations_both_endpoint_rate": _rate(
            len(safe_full),
            full_citations_rows,
        ),
        "candidate_source_distribution": _records(
            union_edges["candidate_source"]
            .value_counts(dropna=False)
            .rename_axis("candidate_source")
            .reset_index(name="candidate_edges")
        ),
        "unresolved_author_year_coverage": coverage,
        "sample_additional_edges": _records(
            _sample_additional_edges(full_edges, only_pairs, sample_size)
        ),
    }


def build_full_citations_coverage_report(
    *,
    metrics: dict[str, Any],
    full_citations_path: Path,
    publication_info_path: Path,
    onlygraph_aligned_path: Path,
    resolved_pilot_path: Path,
    contexts_path: Path,
    out_safe_aligned: Path,
) -> str:
    coverage = metrics["unresolved_author_year_coverage"]
    core_rows = [
        {"metric": "full_citations total rows", "value": metrics["full_citations_total_rows"]},
        {
            "metric": "safe full_citations rows where both endpoints map",
            "value": metrics["safe_full_citations_rows"],
        },
        {
            "metric": "onlygraph unique candidate edges",
            "value": metrics["onlygraph_unique_candidate_edges"],
        },
        {
            "metric": "full_citations_safe unique candidate edges",
            "value": metrics["full_citations_safe_unique_candidate_edges"],
        },
        {
            "metric": "union unique candidate edges",
            "value": metrics["union_unique_candidate_edges"],
        },
        {
            "metric": "safe full_citations both-endpoint rate",
            "value": metrics["safe_full_citations_both_endpoint_rate"],
        },
        {
            "metric": "additional candidate edges beyond onlygraph",
            "value": metrics["additional_candidate_edges_beyond_onlygraph"],
        },
        {
            "metric": "additional citing ACL papers",
            "value": metrics["additional_citing_acl_papers"],
        },
        {
            "metric": "additional cited ACL papers",
            "value": metrics["additional_cited_acl_papers"],
        },
    ]
    unresolved_rows = [
        {
            "metric": "bibliography_unresolved author-year rows",
            "value": coverage["bibliography_unresolved_author_year_rows"],
        },
        {
            "metric": "gain at least one same-year candidate",
            "value": coverage["gain_same_year_candidate_rows"],
        },
        {
            "metric": "gain at least one same-year + surname candidate",
            "value": coverage["gain_same_year_surname_candidate_rows"],
        },
        {
            "metric": "become ambiguous due to multiple surname candidates",
            "value": coverage["become_ambiguous_surname_rows"],
        },
        {
            "metric": "union same-year + surname candidate rows",
            "value": coverage["union_same_year_surname_candidate_rows"],
        },
        {
            "metric": "full_citations-only same-year + surname candidate rows",
            "value": coverage["full_only_same_year_surname_candidate_rows"],
        },
    ]
    risk = _risk_analysis(coverage)
    return "\n".join(
        [
            "# Full Citations Candidate Coverage Report",
            "",
            "## Inputs",
            _table(
                [
                    {"name": "acl_full_citations", "path": full_citations_path},
                    {"name": "publication_info", "path": publication_info_path},
                    {"name": "onlygraph_aligned", "path": onlygraph_aligned_path},
                    {"name": "citation_contexts_resolved_pilot", "path": resolved_pilot_path},
                    {"name": "citation_contexts", "path": contexts_path},
                ]
            ),
            "",
            "## Outputs",
            _table(
                [
                    {
                        "name": "acl_full_citations_safe_aligned",
                        "path": out_safe_aligned,
                    }
                ]
            ),
            "",
            "## Candidate Source Sizes",
            _table(core_rows),
            "",
            (
                "Unique candidate edges are deduplicated by "
                "`(citing_acl_id, cited_acl_id)`."
            ),
            "",
            "## Candidate Source Distribution In Union",
            _table(metrics["candidate_source_distribution"]),
            "",
            "## Bibliography-Unresolved Author-Year Coverage",
            _table(unresolved_rows),
            "",
            "## Risk Analysis",
            risk,
            "",
            "## Sample Additional Safe Full-Citation Edges",
            _table(metrics["sample_additional_edges"]),
            "",
            "## Sample Rows Gaining Same-Year + Surname Candidates",
            _table(coverage["sample_gain_surname_rows"]),
            "",
            "## Sample Rows Becoming Ambiguous",
            _table(coverage["sample_ambiguous_rows"]),
            "",
            "## Recommendation",
            _recommendation(metrics, coverage),
            "",
        ]
    )


def _candidate_edges(frame: pd.DataFrame, source: str) -> pd.DataFrame:
    edges = frame[
        [
            "citing_acl_id",
            "citing_corpus_paper_id",
            "cited_acl_id",
            "cited_corpus_paper_id",
            "cited_title",
            "cited_year",
            "cited_authors",
            "cited_doi",
        ]
    ].copy()
    edges = edges.dropna(subset=["citing_acl_id", "cited_acl_id"])
    edges["candidate_source"] = source
    edges["candidate_year"] = edges["cited_year"].map(_year_string)
    edges["candidate_surnames"] = edges["cited_authors"].map(_candidate_surnames)
    return edges.drop_duplicates(subset=["citing_acl_id", "cited_acl_id"]).reset_index(drop=True)


def _union_candidate_edges(only_edges: pd.DataFrame, full_edges: pd.DataFrame) -> pd.DataFrame:
    combined = pd.concat([only_edges, full_edges], ignore_index=True)
    if combined.empty:
        return combined
    combined["_source_rank"] = combined["candidate_source"].map(
        {"onlygraph": 0, "full_citations": 1}
    )
    combined = combined.sort_values(["citing_acl_id", "cited_acl_id", "_source_rank"])
    grouped = combined.groupby(["citing_acl_id", "cited_acl_id"], sort=False, dropna=False)
    rows = []
    for _, group in grouped:
        row = group.iloc[0].drop(labels=["_source_rank"]).to_dict()
        sources = set(group["candidate_source"])
        row["candidate_source"] = "both" if len(sources) > 1 else next(iter(sources))
        rows.append(row)
    columns = [column for column in combined.columns if column != "_source_rank"]
    return pd.DataFrame(rows, columns=columns)


def _edge_pairs(frame: pd.DataFrame) -> set[tuple[str, str]]:
    return set(
        zip(
            frame["citing_acl_id"].astype(str),
            frame["cited_acl_id"].astype(str),
            strict=True,
        )
    )


def _candidate_index(edges: pd.DataFrame) -> dict[str, pd.DataFrame]:
    return {
        str(citing_acl_id): group.reset_index(drop=True)
        for citing_acl_id, group in edges.groupby("citing_acl_id", dropna=False)
    }


def _bibliography_unresolved_author_year_rows(resolved: pd.DataFrame) -> pd.DataFrame:
    frame = resolved.loc[resolved["resolution_status"].eq("bibliography_unresolved")].copy()
    frame["parsed_year"] = frame["parsed_year"].map(_clean_string)
    frame["parsed_surnames"] = frame["parsed_surnames"].map(_clean_string)
    return frame.loc[
        frame["parsed_year"].notna()
        & frame["parsed_surnames"].notna()
        & frame["parsed_surnames"].ne("")
    ].reset_index(drop=True)


def _coverage_for_unresolved_rows(
    unresolved: pd.DataFrame,
    *,
    only_index: dict[str, pd.DataFrame],
    full_index: dict[str, pd.DataFrame],
    union_index: dict[str, pd.DataFrame],
    sample_size: int,
) -> dict[str, Any]:
    if unresolved.empty:
        return {
            "bibliography_unresolved_author_year_rows": 0,
            "gain_same_year_candidate_rows": 0,
            "gain_same_year_surname_candidate_rows": 0,
            "become_ambiguous_surname_rows": 0,
            "union_same_year_surname_candidate_rows": 0,
            "full_only_same_year_surname_candidate_rows": 0,
            "sample_gain_surname_rows": [],
            "sample_ambiguous_rows": [],
        }

    rows: list[dict[str, Any]] = []
    for row in unresolved.to_dict(orient="records"):
        citing_acl_id = _clean_string(row.get("citing_paper_id")) or ""
        year = _clean_string(row.get("parsed_year"))
        surnames = _surname_list(row.get("parsed_surnames"))
        only_counts = _candidate_counts(only_index.get(citing_acl_id), year, surnames)
        full_counts = _candidate_counts(full_index.get(citing_acl_id), year, surnames)
        union_counts = _candidate_counts(union_index.get(citing_acl_id), year, surnames)
        rows.append(
            {
                **row,
                "only_same_year_count": only_counts["same_year"],
                "only_same_year_surname_count": only_counts["same_year_surname"],
                "full_same_year_count": full_counts["same_year"],
                "full_same_year_surname_count": full_counts["same_year_surname"],
                "union_same_year_count": union_counts["same_year"],
                "union_same_year_surname_count": union_counts["same_year_surname"],
                "union_same_year_surname_acl_ids": ";".join(union_counts["surname_acl_ids"]),
            }
        )
    coverage = pd.DataFrame(rows)
    gain_same_year = coverage["only_same_year_count"].eq(0) & coverage[
        "union_same_year_count"
    ].gt(0)
    gain_surname = coverage["only_same_year_surname_count"].eq(0) & coverage[
        "union_same_year_surname_count"
    ].gt(0)
    become_ambiguous = coverage["only_same_year_surname_count"].le(1) & coverage[
        "union_same_year_surname_count"
    ].gt(1)
    full_only_surname = coverage["full_same_year_surname_count"].gt(0) & coverage[
        "only_same_year_surname_count"
    ].eq(0)

    return {
        "bibliography_unresolved_author_year_rows": int(len(coverage)),
        "gain_same_year_candidate_rows": int(gain_same_year.sum()),
        "gain_same_year_surname_candidate_rows": int(gain_surname.sum()),
        "become_ambiguous_surname_rows": int(become_ambiguous.sum()),
        "union_same_year_surname_candidate_rows": int(
            coverage["union_same_year_surname_count"].gt(0).sum()
        ),
        "full_only_same_year_surname_candidate_rows": int(full_only_surname.sum()),
        "sample_gain_surname_rows": _sample_coverage_rows(coverage.loc[gain_surname], sample_size),
        "sample_ambiguous_rows": _sample_coverage_rows(
            coverage.loc[become_ambiguous],
            sample_size,
        ),
    }


def _candidate_counts(
    candidates: pd.DataFrame | None,
    year: str | None,
    surnames: list[str],
) -> dict[str, Any]:
    if candidates is None or candidates.empty or year is None:
        return {"same_year": 0, "same_year_surname": 0, "surname_acl_ids": []}
    year_matches = candidates.loc[candidates["candidate_year"].eq(year)]
    surname_matches = year_matches.loc[
        year_matches["candidate_surnames"].map(lambda value: _candidate_matches(value, surnames))
    ]
    return {
        "same_year": int(len(year_matches)),
        "same_year_surname": int(len(surname_matches)),
        "surname_acl_ids": sorted(surname_matches["cited_acl_id"].astype(str).unique()),
    }


def _candidate_matches(candidate_surnames: Any, parsed_surnames: list[str]) -> bool:
    if not parsed_surnames:
        return False
    candidate_set = set(candidate_surnames or [])
    if not candidate_set:
        return False
    if parsed_surnames[0] not in candidate_set:
        return False
    if len(parsed_surnames) == 1:
        return True
    return all(surname in candidate_set for surname in parsed_surnames)


def _surname_list(value: Any) -> list[str]:
    text = _clean_string(value)
    if text is None:
        return []
    return [piece for piece in text.split(";") if piece]


def _sample_coverage_rows(frame: pd.DataFrame, sample_size: int) -> list[dict[str, Any]]:
    if frame.empty:
        return []
    columns = [
        "source_context_id",
        "citing_paper_id",
        "citation_marker",
        "marker_component_text",
        "parsed_surnames",
        "parsed_year",
        "only_same_year_count",
        "only_same_year_surname_count",
        "full_same_year_count",
        "full_same_year_surname_count",
        "union_same_year_count",
        "union_same_year_surname_count",
        "union_same_year_surname_acl_ids",
        "sentence_text",
    ]
    sample = frame[columns].head(sample_size).copy()
    sample["sentence_text"] = sample["sentence_text"].map(lambda value: _truncate(value, 160))
    return _records(sample)


def _sample_additional_edges(
    full_edges: pd.DataFrame,
    only_pairs: set[tuple[str, str]],
    sample_size: int,
) -> pd.DataFrame:
    mask = [
        (str(row.citing_acl_id), str(row.cited_acl_id)) not in only_pairs
        for row in full_edges.itertuples(index=False)
    ]
    sample = full_edges.loc[mask].head(sample_size).copy()
    columns = [
        "citing_acl_id",
        "cited_acl_id",
        "cited_title",
        "cited_year",
        "cited_authors",
        "candidate_source",
    ]
    for column in ("cited_title", "cited_authors"):
        sample[column] = sample[column].map(lambda value: _truncate(value, 120))
    return sample[columns]


def _risk_analysis(coverage: dict[str, Any]) -> str:
    recovered = coverage["gain_same_year_surname_candidate_rows"]
    ambiguous = coverage["become_ambiguous_surname_rows"]
    total = coverage["bibliography_unresolved_author_year_rows"]
    recovery_rate = _rate(recovered, total)
    ambiguity_rate = _rate(ambiguous, total)
    if recovered == 0:
        recommendation = (
            "The safe full-citations subset does not recover same-year + surname candidates "
            "in this pilot, so it should not be promoted."
        )
    elif ambiguous > recovered:
        recommendation = (
            "Ambiguity grows faster than direct surname-level recovery; use only for "
            "audited candidate expansion, not automatic resolution."
        )
    else:
        recommendation = (
            "Surname-level recovery exceeds the new ambiguous row count in this pilot, "
            "but review is still required before enabling it in resolution."
        )
    return (
        f"- Same-year + surname recovery rate among unresolved author-year rows: "
        f"{recovery_rate}\n"
        f"- New ambiguity rate among unresolved author-year rows: {ambiguity_rate}\n"
        f"- {recommendation}"
    )


def _recommendation(metrics: dict[str, Any], coverage: dict[str, Any]) -> str:
    if (
        metrics["additional_candidate_edges_beyond_onlygraph"] == 0
        and coverage["gain_same_year_surname_candidate_rows"] == 0
    ):
        return (
            "Do not use `acl_full_citations` for final resolution. In this safe aligned "
            "subset, all unique ACL-to-ACL candidate pairs are already present in "
            "`acl_onlygraph`, so it adds no reviewed coverage for the current pilot."
        )
    return (
        "Do not use `acl_full_citations` for final resolution yet. Keep it as a reviewed "
        "candidate-source experiment until the recovered candidates and ambiguity profile "
        "are manually audited."
    )


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


def _integer_series(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").astype("Int64")


def _clean_string(value: Any) -> str | None:
    if value is None or pd.isna(value):
        return None
    text = str(value).strip()
    return text or None


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
        lines.append(
            "| "
            + " | ".join(_markdown_cell(row.get(column)) for column in columns)
            + " |"
        )
    return "\n".join(lines)


def _markdown_cell(value: Any) -> str:
    if value is None or pd.isna(value):
        return "unavailable"
    return _truncate(value, 140).replace("|", "\\|")
