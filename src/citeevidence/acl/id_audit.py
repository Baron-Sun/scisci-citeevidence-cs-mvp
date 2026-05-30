from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pandas as pd
import pyarrow.compute as pc
import pyarrow.parquet as pq

DEFAULT_SCHEMA_ID_AUDIT_REPORT = Path("reports/acl_ocl_schema_id_audit.md")
DEFAULT_SCHEMA_INVENTORY_PATH = Path("data/interim/acl_ocl_schema_inventory.json")

RAW_INPUTS = {
    "publication_info": "acl-publication-info.74k.v2.parquet",
    "acl_full_citations": "acl_full_citations.parquet",
    "acl_onlygraph": "acl_onlygraph.parquet",
}
INTERIM_INPUTS = {
    "acl_papers": "acl_papers.parquet",
    "acl_references": "acl_references.parquet",
    "acl_sections": "acl_sections.parquet",
}
ACL_ID_RE = re.compile(r"\b[A-Z][0-9]{2}-[0-9]{3,5}[A-Za-z]?\b")
INTEGER_ID_RE = re.compile(r"\d+")
FLOAT_INTEGER_ID_RE = re.compile(r"(\d+)\.0")
SOURCE_ROLE_RE = re.compile(r"(citing|source|src|from)", re.IGNORECASE)
TARGET_ROLE_RE = re.compile(r"(cited|target|dst|to)", re.IGNORECASE)


def audit_acl_ocl_ids(
    *,
    raw_dir: str | Path,
    interim_dir: str | Path,
    contexts_path: str | Path,
    out_report: str | Path = DEFAULT_SCHEMA_ID_AUDIT_REPORT,
    inventory_path: str | Path = DEFAULT_SCHEMA_INVENTORY_PATH,
    sample_rows: int = 50_000,
    example_values: int = 5,
    join_examples: int = 20,
) -> dict[str, Any]:
    """Audit ACL-OCL schemas and candidate numeric-to-ACL ID crosswalks."""
    raw_root = Path(raw_dir)
    interim_root = Path(interim_dir)
    contexts = Path(contexts_path)
    if not raw_root.exists():
        raise FileNotFoundError(f"Raw ACL-OCL directory does not exist: {raw_root}")
    if not interim_root.exists():
        raise FileNotFoundError(f"Interim directory does not exist: {interim_root}")
    if not contexts.exists():
        raise FileNotFoundError(f"Citation contexts parquet does not exist: {contexts}")

    input_paths = {
        **{name: raw_root / file_name for name, file_name in RAW_INPUTS.items()},
        **{name: interim_root / file_name for name, file_name in INTERIM_INPUTS.items()},
        "citation_contexts": contexts,
    }
    missing = [str(path) for path in input_paths.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing required ACL-OCL audit inputs: {', '.join(missing)}")

    files = {
        name: _inspect_parquet_file(path, sample_rows=sample_rows, example_values=example_values)
        for name, path in input_paths.items()
    }
    publication = files["publication_info"]
    pub_acl_column = _best_acl_id_column(publication)
    pub_corpus_column = _best_numeric_id_column(publication)
    exact_crosswalk_columns = {
        "acl_id": "acl_id" in publication["columns"],
        "corpus_paper_id": "corpus_paper_id" in publication["columns"],
        "both_present": {"acl_id", "corpus_paper_id"} <= set(publication["columns"]),
    }

    corpus_ids: set[str] = set()
    acl_ids: set[str] = set()
    crosswalk = pd.DataFrame()
    if pub_acl_column and pub_corpus_column:
        crosswalk = _load_publication_crosswalk(
            input_paths["publication_info"],
            acl_column=pub_acl_column,
            corpus_column=pub_corpus_column,
        )
        corpus_ids = set(crosswalk["corpus_paper_id"].dropna())
        acl_ids = set(crosswalk["acl_id"].dropna())

    overlap_checks = {
        "acl_references_vs_publication": _reference_overlap_checks(
            input_paths["acl_references"],
            corpus_ids=corpus_ids,
        ),
        "acl_sections_vs_publication": _string_overlap_check(
            input_paths["acl_sections"],
            column="paper_id",
            target_values=acl_ids,
            target_name="publication acl_id",
        ),
        "citation_contexts_vs_publication": _string_overlap_check(
            input_paths["citation_contexts"],
            column="citing_paper_id",
            target_values=acl_ids,
            target_name="publication acl_id",
        ),
    }

    graph_checks: dict[str, Any] = {}
    graph_role_columns: dict[str, dict[str, str | None]] = {}
    for graph_name in ("acl_full_citations", "acl_onlygraph"):
        graph_profile = files[graph_name]
        graph_overlap = _graph_overlap_checks(input_paths[graph_name], graph_profile, corpus_ids)
        graph_checks[graph_name] = graph_overlap
        graph_role_columns[graph_name] = _select_graph_role_columns(graph_profile, graph_overlap)
    overlap_checks["graph_vs_publication"] = graph_checks

    preferred_graph = _preferred_graph_name(graph_role_columns)
    preferred_roles = graph_role_columns.get(preferred_graph, {})
    success_examples, failed_examples = _join_examples(
        graph_name=preferred_graph,
        graph_path=input_paths[preferred_graph],
        crosswalk=crosswalk,
        source_column=preferred_roles.get("source"),
        target_column=preferred_roles.get("target"),
        limit=join_examples,
    )
    if len(failed_examples) < join_examples and preferred_graph != "acl_full_citations":
        full_roles = graph_role_columns.get("acl_full_citations", {})
        _, full_failed_examples = _join_examples(
            graph_name="acl_full_citations",
            graph_path=input_paths["acl_full_citations"],
            crosswalk=crosswalk,
            source_column=full_roles.get("source"),
            target_column=full_roles.get("target"),
            limit=join_examples,
        )
        failed_examples = [*failed_examples, *full_failed_examples][:join_examples]

    inventory = {
        "inputs": {name: str(path) for name, path in input_paths.items()},
        "files": files,
        "candidate_acl_id_columns": _collect_candidates(files, "is_acl_id_candidate"),
        "candidate_numeric_paper_id_columns": _collect_candidates(
            files,
            "is_numeric_paper_id_candidate",
        ),
        "publication_crosswalk": {
            "acl_column": pub_acl_column,
            "numeric_column": pub_corpus_column,
            "exact_column_check": exact_crosswalk_columns,
            "rows": int(len(crosswalk)),
            "unique_acl_ids": int(crosswalk["acl_id"].nunique()) if not crosswalk.empty else 0,
            "unique_numeric_ids": (
                int(crosswalk["corpus_paper_id"].nunique()) if not crosswalk.empty else 0
            ),
        },
        "overlap_checks": overlap_checks,
        "best_candidate_mapping": {
            "authoritative_crosswalk_file": str(input_paths["publication_info"])
            if pub_acl_column and pub_corpus_column
            else None,
            "citing_numeric_id_to_acl_id": {
                "graph_file": preferred_graph,
                "numeric_column": preferred_roles.get("source"),
                "crosswalk_numeric_column": pub_corpus_column,
                "crosswalk_acl_column": pub_acl_column,
            },
            "cited_numeric_id_to_acl_id": {
                "graph_file": preferred_graph,
                "numeric_column": preferred_roles.get("target"),
                "crosswalk_numeric_column": pub_corpus_column,
                "crosswalk_acl_column": pub_acl_column,
            },
        },
        "successful_candidate_join_examples": success_examples,
        "failed_candidate_join_examples": failed_examples,
    }

    report = build_acl_ocl_id_audit_report(inventory)
    report_output = Path(out_report)
    report_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.write_text(report, encoding="utf-8")

    inventory_output = Path(inventory_path)
    inventory_output.parent.mkdir(parents=True, exist_ok=True)
    inventory_json = json.dumps(inventory, indent=2, ensure_ascii=False)
    inventory_output.write_text(inventory_json, encoding="utf-8")
    return inventory


def build_acl_ocl_id_audit_report(inventory: dict[str, Any]) -> str:
    """Build the ACL-OCL schema and ID mapping audit markdown report."""
    files = inventory["files"]
    publication = inventory["publication_crosswalk"]
    overlap = inventory["overlap_checks"]
    best_mapping = inventory["best_candidate_mapping"]
    exact = publication["exact_column_check"]

    sections = [
        "# ACL-OCL Schema and ID Mapping Audit",
        "",
        "## Executive Summary",
        f"- Publication metadata contains exact `acl_id`: {exact['acl_id']}",
        f"- Publication metadata contains exact `corpus_paper_id`: {exact['corpus_paper_id']}",
        f"- Publication metadata contains both exact crosswalk columns: {exact['both_present']}",
        (
            "- Authoritative crosswalk: "
            f"`{best_mapping['authoritative_crosswalk_file']}`"
            if best_mapping["authoritative_crosswalk_file"]
            else "- Authoritative crosswalk: unavailable"
        ),
        (
            "- Best citing mapping: "
            f"`{best_mapping['citing_numeric_id_to_acl_id']['numeric_column']}` -> "
            f"`{best_mapping['citing_numeric_id_to_acl_id']['crosswalk_acl_column']}`"
        ),
        (
            "- Best cited mapping: "
            f"`{best_mapping['cited_numeric_id_to_acl_id']['numeric_column']}` -> "
            f"`{best_mapping['cited_numeric_id_to_acl_id']['crosswalk_acl_column']}`"
        ),
        "",
        "## Inputs",
        _table(
            [
                {"name": name, "path": path}
                for name, path in inventory["inputs"].items()
            ]
        ),
        "",
        "## Publication Crosswalk Check",
        _table([publication]),
        "",
        "## Candidate ACL ID Columns",
        _table(inventory["candidate_acl_id_columns"]),
        "",
        "## Candidate Numeric Paper ID Columns",
        _table(inventory["candidate_numeric_paper_id_columns"]),
        "",
        "## Reference Overlap Checks",
        _table(overlap["acl_references_vs_publication"]),
        "",
        "## Section and Context ACL ID Checks",
        _table(
            [
                overlap["acl_sections_vs_publication"],
                overlap["citation_contexts_vs_publication"],
            ]
        ),
        "",
        "## Graph Overlap Checks",
    ]

    for graph_name, checks in overlap["graph_vs_publication"].items():
        sections.extend([f"### {graph_name}", _table(checks), ""])

    sections.extend(
        [
            "## Successful Candidate Joins",
            _table(inventory["successful_candidate_join_examples"]),
            "",
            "## Failed Candidate Joins",
            _table(inventory["failed_candidate_join_examples"]),
            "",
            "## Authoritative Crosswalk Recommendation",
            _crosswalk_recommendation(inventory),
            "",
            "## File Schemas and Column Profiles",
        ]
    )

    for file_name, profile in files.items():
        sections.extend(
            [
                f"### {file_name}",
                f"- Path: `{profile['path']}`",
                f"- Shape: {profile['rows']} rows x {len(profile['columns'])} columns",
                f"- Columns: `{', '.join(profile['columns'])}`",
                "",
                _table(profile["column_profiles"]),
                "",
            ]
        )
    return "\n".join(sections)


def _inspect_parquet_file(path: Path, *, sample_rows: int, example_values: int) -> dict[str, Any]:
    parquet_file = pq.ParquetFile(path)
    schema = parquet_file.schema_arrow
    columns = schema.names
    rows = parquet_file.metadata.num_rows
    column_profiles = []
    for column_index, field in enumerate(schema):
        non_null = _non_null_count(parquet_file, column_index)
        sample_profile = _sample_column_profile(
            path,
            field.name,
            sample_rows=sample_rows,
            example_values=example_values,
        )
        column_profiles.append(
            {
                "column": field.name,
                "dtype": str(field.type),
                "non_null_rate": _rate(non_null, rows),
                "examples": sample_profile["examples"],
                "sample_checked": sample_profile["sample_checked"],
                "acl_id_match_rate": sample_profile["acl_id_match_rate"],
                "integer_like_rate": sample_profile["integer_like_rate"],
                "sample_unique_values": sample_profile["sample_unique_values"],
                "is_acl_id_candidate": sample_profile["is_acl_id_candidate"],
                "is_numeric_paper_id_candidate": sample_profile[
                    "is_numeric_paper_id_candidate"
                ],
            }
        )
    return {
        "path": str(path),
        "rows": int(rows),
        "columns": columns,
        "column_profiles": column_profiles,
    }


def _non_null_count(parquet_file: pq.ParquetFile, column_index: int) -> int:
    rows = parquet_file.metadata.num_rows
    nulls = 0
    for row_group_index in range(parquet_file.metadata.num_row_groups):
        row_group = parquet_file.metadata.row_group(row_group_index)
        statistics = row_group.column(column_index).statistics
        if statistics is None or statistics.null_count is None:
            column = parquet_file.schema_arrow.names[column_index]
            return _scan_non_null_count(parquet_file, column)
        nulls += statistics.null_count
    return int(rows - nulls)


def _scan_non_null_count(parquet_file: pq.ParquetFile, column: str) -> int:
    non_null = 0
    for batch in parquet_file.iter_batches(batch_size=20_000, columns=[column]):
        non_null += int(pc.sum(pc.is_valid(batch.column(0))).as_py())
    return non_null


def _sample_column_profile(
    path: Path,
    column: str,
    *,
    sample_rows: int,
    example_values: int,
) -> dict[str, Any]:
    examples: list[str] = []
    checked = 0
    acl_matches = 0
    integer_like = 0
    unique_values: set[str] = set()
    unique_integer_values: set[str] = set()

    parquet_file = pq.ParquetFile(path)
    for batch in parquet_file.iter_batches(batch_size=4096, columns=[column]):
        for value in batch.column(0).to_pylist():
            if value is None or pd.isna(value):
                continue
            text = _stringify(value)
            if not text:
                continue
            if len(examples) < example_values:
                examples.append(_truncate(text))
            checked += 1
            unique_values.add(text)
            if ACL_ID_RE.fullmatch(text) or ACL_ID_RE.search(text):
                acl_matches += 1
            integer_value = _normalize_integer_id(value)
            if integer_value is not None:
                integer_like += 1
                unique_integer_values.add(integer_value)
            if checked >= sample_rows:
                break
        if checked >= sample_rows:
            break

    acl_rate = _ratio(acl_matches, checked)
    integer_rate = _ratio(integer_like, checked)
    is_acl_candidate = checked > 0 and acl_matches > 0 and acl_rate >= 0.5
    is_numeric_candidate = (
        checked > 0
        and integer_rate >= 0.95
        and len(unique_integer_values) >= _many_unique_threshold(checked)
    )
    return {
        "examples": examples,
        "sample_checked": checked,
        "acl_id_match_rate": _format_rate(acl_rate),
        "integer_like_rate": _format_rate(integer_rate),
        "sample_unique_values": int(len(unique_values)),
        "is_acl_id_candidate": is_acl_candidate,
        "is_numeric_paper_id_candidate": is_numeric_candidate,
    }


def _load_publication_crosswalk(
    path: Path,
    *,
    acl_column: str,
    corpus_column: str,
) -> pd.DataFrame:
    requested = [acl_column, corpus_column]
    optional = ["title", "year", "doi", "author"]
    available = set(pq.ParquetFile(path).schema_arrow.names)
    columns = [*requested, *[column for column in optional if column in available]]
    frame = pd.read_parquet(path, columns=columns).copy()
    frame = frame.rename(columns={acl_column: "acl_id", corpus_column: "corpus_paper_id"})
    frame["acl_id"] = frame["acl_id"].map(_normalize_nonempty_string)
    frame["corpus_paper_id"] = frame["corpus_paper_id"].map(_normalize_integer_id)
    return frame.dropna(subset=["acl_id", "corpus_paper_id"]).drop_duplicates(
        subset=["acl_id", "corpus_paper_id"]
    )


def _reference_overlap_checks(path: Path, *, corpus_ids: set[str]) -> list[dict[str, Any]]:
    rows = []
    for column in ("citing_paper_id", "reference_key", "raw_reference"):
        if column not in pq.ParquetFile(path).schema_arrow.names:
            continue
        values = _unique_integer_ids(path, column)
        rows.append(
            _overlap_row(
                "acl_references",
                column,
                values,
                corpus_ids,
                target_name="publication corpus_paper_id",
            )
        )
    return rows


def _graph_overlap_checks(
    path: Path,
    profile: dict[str, Any],
    corpus_ids: set[str],
) -> list[dict[str, Any]]:
    rows = []
    for column_profile in profile["column_profiles"]:
        if not column_profile["is_numeric_paper_id_candidate"]:
            continue
        column = column_profile["column"]
        values = _unique_integer_ids(path, column)
        rows.append(
            _overlap_row(
                Path(profile["path"]).name,
                column,
                values,
                corpus_ids,
                target_name="publication corpus_paper_id",
            )
        )
    return rows


def _string_overlap_check(
    path: Path,
    *,
    column: str,
    target_values: set[str],
    target_name: str,
) -> dict[str, Any]:
    values = _unique_strings(path, column)
    return _overlap_row(Path(path).name, column, values, target_values, target_name=target_name)


def _overlap_row(
    file_name: str,
    column: str,
    values: set[str],
    target_values: set[str],
    *,
    target_name: str,
) -> dict[str, Any]:
    overlap = values & target_values
    return {
        "file": file_name,
        "column": column,
        "target": target_name,
        "unique_values": int(len(values)),
        "overlap_count": int(len(overlap)),
        "overlap_rate": _rate(len(overlap), len(values)),
    }


def _select_graph_role_columns(
    graph_profile: dict[str, Any],
    graph_overlap: list[dict[str, Any]],
) -> dict[str, str | None]:
    numeric_columns = [
        profile["column"]
        for profile in graph_profile["column_profiles"]
        if profile["is_numeric_paper_id_candidate"]
    ]
    source = next((column for column in numeric_columns if SOURCE_ROLE_RE.search(column)), None)
    target = next((column for column in numeric_columns if TARGET_ROLE_RE.search(column)), None)
    if source and target:
        return {"source": source, "target": target}

    ranked = sorted(
        graph_overlap,
        key=lambda row: row["overlap_count"],
        reverse=True,
    )
    fallback = [row["column"] for row in ranked[:2]]
    return {
        "source": source or (fallback[0] if fallback else None),
        "target": target or (fallback[1] if len(fallback) > 1 else None),
    }


def _preferred_graph_name(graph_roles: dict[str, dict[str, str | None]]) -> str:
    if graph_roles.get("acl_onlygraph", {}).get("source") and graph_roles.get(
        "acl_onlygraph",
        {},
    ).get("target"):
        return "acl_onlygraph"
    return "acl_full_citations"


def _join_examples(
    *,
    graph_name: str,
    graph_path: Path,
    crosswalk: pd.DataFrame,
    source_column: str | None,
    target_column: str | None,
    limit: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if crosswalk.empty or source_column is None or target_column is None:
        return [], []

    graph_columns = [column for column in ("id", source_column, target_column) if column]
    graph = pd.read_parquet(graph_path, columns=list(dict.fromkeys(graph_columns)))
    source_map = crosswalk.set_index("corpus_paper_id")
    acl_map = source_map["acl_id"].to_dict()
    title_map = source_map["title"].to_dict() if "title" in source_map.columns else {}
    year_map = source_map["year"].to_dict() if "year" in source_map.columns else {}

    graph = graph.copy()
    graph["citing_numeric_id"] = graph[source_column].map(_normalize_integer_id)
    graph["cited_numeric_id"] = graph[target_column].map(_normalize_integer_id)
    graph["citing_acl_id"] = graph["citing_numeric_id"].map(acl_map)
    graph["cited_acl_id"] = graph["cited_numeric_id"].map(acl_map)
    graph["citing_title"] = graph["citing_numeric_id"].map(title_map)
    graph["cited_title"] = graph["cited_numeric_id"].map(title_map)
    graph["citing_year"] = graph["citing_numeric_id"].map(year_map)
    graph["cited_year"] = graph["cited_numeric_id"].map(year_map)
    graph["graph_file"] = graph_name

    base_columns = [
        "graph_file",
        "id",
        "citing_numeric_id",
        "citing_acl_id",
        "citing_year",
        "citing_title",
        "cited_numeric_id",
        "cited_acl_id",
        "cited_year",
        "cited_title",
    ]
    available_columns = [column for column in base_columns if column in graph.columns]
    both_joined = graph["citing_acl_id"].notna() & graph["cited_acl_id"].notna()
    any_failed = graph["citing_acl_id"].isna() | graph["cited_acl_id"].isna()

    successes = graph.loc[both_joined, available_columns].head(limit)
    if successes.empty:
        successes = graph.loc[
            graph["citing_acl_id"].notna() | graph["cited_acl_id"].notna(),
            available_columns,
        ].head(limit)
    failures = graph.loc[any_failed, available_columns].head(limit)
    return _records(successes), _records(failures)


def _best_acl_id_column(file_profile: dict[str, Any]) -> str | None:
    candidates = [
        profile
        for profile in file_profile["column_profiles"]
        if profile["is_acl_id_candidate"]
    ]
    if not candidates:
        return None
    return max(
        candidates,
        key=lambda profile: (
            float(profile["acl_id_match_rate"]),
            profile["sample_checked"],
            profile["sample_unique_values"],
        ),
    )["column"]


def _best_numeric_id_column(file_profile: dict[str, Any]) -> str | None:
    candidates = [
        profile
        for profile in file_profile["column_profiles"]
        if profile["is_numeric_paper_id_candidate"]
    ]
    if not candidates:
        return None
    return max(
        candidates,
        key=lambda profile: (
            profile["sample_unique_values"],
            profile["sample_checked"],
        ),
    )["column"]


def _collect_candidates(files: dict[str, Any], candidate_flag: str) -> list[dict[str, Any]]:
    rows = []
    for file_name, profile in files.items():
        for column_profile in profile["column_profiles"]:
            if not column_profile[candidate_flag]:
                continue
            rows.append(
                {
                    "file": file_name,
                    "column": column_profile["column"],
                    "dtype": column_profile["dtype"],
                    "sample_checked": column_profile["sample_checked"],
                    "acl_id_match_rate": column_profile["acl_id_match_rate"],
                    "integer_like_rate": column_profile["integer_like_rate"],
                    "sample_unique_values": column_profile["sample_unique_values"],
                    "examples": column_profile["examples"],
                }
            )
    return rows


def _unique_integer_ids(path: Path, column: str) -> set[str]:
    values: set[str] = set()
    parquet_file = pq.ParquetFile(path)
    for batch in parquet_file.iter_batches(batch_size=100_000, columns=[column]):
        for value in batch.column(0).to_pylist():
            normalized = _normalize_integer_id(value)
            if normalized is not None:
                values.add(normalized)
    return values


def _unique_strings(path: Path, column: str) -> set[str]:
    values: set[str] = set()
    if column not in pq.ParquetFile(path).schema_arrow.names:
        return values
    parquet_file = pq.ParquetFile(path)
    for batch in parquet_file.iter_batches(batch_size=100_000, columns=[column]):
        for value in batch.column(0).to_pylist():
            normalized = _normalize_nonempty_string(value)
            if normalized is not None:
                values.add(normalized)
    return values


def _normalize_acl_id(value: Any) -> str | None:
    if value is None or pd.isna(value):
        return None
    text = _stringify(value)
    match = ACL_ID_RE.search(text)
    return match.group(0) if match else None


def _normalize_nonempty_string(value: Any) -> str | None:
    if value is None or pd.isna(value):
        return None
    text = _stringify(value)
    return text or None


def _normalize_integer_id(value: Any) -> str | None:
    if value is None or pd.isna(value):
        return None
    text = _stringify(value)
    if INTEGER_ID_RE.fullmatch(text):
        return str(int(text))
    match = FLOAT_INTEGER_ID_RE.fullmatch(text)
    if match:
        return str(int(match.group(1)))
    return None


def _many_unique_threshold(checked: int) -> int:
    if checked < 20:
        return max(2, checked // 2)
    return min(1000, max(20, checked // 5))


def _crosswalk_recommendation(inventory: dict[str, Any]) -> str:
    crosswalk = inventory["publication_crosswalk"]
    exact = crosswalk["exact_column_check"]
    if crosswalk["acl_column"] and crosswalk["numeric_column"] and exact["both_present"]:
        return (
            "`acl-publication-info.74k.v2.parquet` should be used as the authoritative "
            "crosswalk. It contains an ACL Anthology ID column and a numeric corpus paper "
            "ID column in the same row, so graph IDs can be mapped back to ACL IDs before "
            "citation context extraction. The current extracted contexts use ACL IDs from "
            "`acl_sections.paper_id`, while `acl_references.citing_paper_id` is numeric, "
            "which explains the bibliography-unresolved contexts."
        )
    return (
        "No authoritative crosswalk was detected. A reliable mapping from numeric graph IDs "
        "to ACL Anthology IDs must be created before high-confidence citation attribution."
    )


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
    if isinstance(value, int | float | str | bool):
        return value
    if hasattr(value, "item"):
        return value.item()
    return str(value)


def _ratio(numerator: int, denominator: int) -> float:
    return 0.0 if denominator == 0 else numerator / denominator


def _rate(numerator: int, denominator: int) -> str:
    return _format_rate(_ratio(numerator, denominator))


def _format_rate(value: float) -> str:
    return f"{value:.3f}"


def _stringify(value: Any) -> str:
    return str(value).strip()


def _truncate(value: Any, max_chars: int = 140) -> str:
    text = _stringify(value).replace("\n", " ")
    if len(text) <= max_chars:
        return text
    return f"{text[: max_chars - 3]}..."


def _table(rows: list[dict[str, Any]] | dict[str, Any]) -> str:
    if isinstance(rows, dict):
        rows = [rows]
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
    if isinstance(value, list):
        value = "; ".join(_truncate(item, 60) for item in value)
    elif isinstance(value, dict):
        value = json.dumps(value, ensure_ascii=False)
    elif value is None or pd.isna(value):
        return "unavailable"
    else:
        value = _truncate(value)
    return str(value).replace("|", "\\|")
