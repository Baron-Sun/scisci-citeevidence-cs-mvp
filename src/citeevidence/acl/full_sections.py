from __future__ import annotations

import gzip
import json
import pickle
import re
import sys
import tempfile
import types
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from citeevidence.contexts.extract import extract_citation_contexts

DEFAULT_FULL_SECTIONS_FILENAME = "acl-publication-info.74k.v2.full-sections.pkl"
DEFAULT_FULL_SECTIONS_STRUCTURE_REPORT = Path("reports/full_sections_structure_report.md")
DEFAULT_FULL_SECTIONS_PARSE_REPORT = Path("reports/full_sections_parse_report.md")
DEFAULT_SECTIONED_SECTIONS_PATH = Path("data/interim/acl_sections_sectioned.parquet")
DEFAULT_SECTIONED_CONTEXT_SAMPLE_PATH = Path(
    "data/processed/citation_contexts_sectioned_sample.parquet"
)
DEFAULT_SECTIONED_SAMPLE_REFERENCE_PATH = Path("data/interim/acl_references.parquet")
SECTIONED_COLUMNS = [
    "paper_id",
    "section_name",
    "normalized_section",
    "section_index",
    "paragraph_id",
    "paragraph_index",
    "paragraph_text",
]
CONTEXT_SECTION_COLUMNS = ["paper_id", "section_name", "paragraph_id", "paragraph_text"]
REFERENCE_COLUMNS = [
    "citing_paper_id",
    "reference_key",
    "cited_title",
    "cited_year",
    "cited_authors",
    "cited_doi",
    "raw_reference",
]
NORMALIZED_SECTIONS = [
    "abstract",
    "introduction",
    "related_work",
    "background",
    "method",
    "model",
    "experiment",
    "evaluation",
    "results",
    "discussion",
    "conclusion",
    "appendix",
    "references",
    "unknown",
]
CITATION_MARKER_RE = re.compile(
    r"\[[0-9,\-–—;\s]+\]|\((?=[^)]*(?:19|20)\d{2})[^()]{1,250}\)"
)
YEAR_RE = re.compile(r"\b(?:19|20)\d{2}\b")


@dataclass(frozen=True)
class FullSectionsInspectResult:
    report: str
    metrics: dict[str, Any]


@dataclass(frozen=True)
class FullSectionsParseResult:
    sections: pd.DataFrame
    metrics: dict[str, Any]


@dataclass(frozen=True)
class _ParagraphCandidate:
    section_name: str | None
    paragraph_text: str
    citation_marker_count: int


def inspect_full_sections_data(
    *,
    raw_dir: str | Path,
    out_report: str | Path,
) -> FullSectionsInspectResult:
    """Inspect ACL-OCL full-sections sources and write a markdown structure report."""
    root = Path(raw_dir)
    if not root.exists():
        raise FileNotFoundError(f"ACL-OCL raw directory does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"ACL-OCL raw path must be a directory: {root}")

    full_sections_path = root / DEFAULT_FULL_SECTIONS_FILENAME
    metrics = _source_availability(root, full_sections_path)
    if not full_sections_path.exists():
        report = _build_missing_full_sections_report(root, metrics)
        _write_report(out_report, report)
        return FullSectionsInspectResult(report=report, metrics=metrics)

    loaded = _load_full_sections_pickle(full_sections_path)
    structure = _object_structure(loaded)
    scan = _scan_records(loaded, collect_rows=False)
    metrics.update(structure)
    metrics.update(scan)

    report = _build_structure_report(
        raw_dir=root,
        full_sections_path=full_sections_path,
        metrics=metrics,
    )
    _write_report(out_report, report)
    return FullSectionsInspectResult(report=report, metrics=metrics)


def parse_full_sections_data(
    *,
    input_path: str | Path,
    out_path: str | Path,
    report_path: str | Path,
    sample_contexts_out: str | Path | None = DEFAULT_SECTIONED_CONTEXT_SAMPLE_PATH,
    references_path: str | Path = DEFAULT_SECTIONED_SAMPLE_REFERENCE_PATH,
    sample_context_section_rows: int = 10_000,
) -> FullSectionsParseResult:
    """Parse ACL-OCL full-sections pickle into section-aware paragraph rows."""
    source = Path(input_path)
    if not source.exists():
        raise FileNotFoundError(f"Full-sections pickle does not exist: {source}")
    if sample_context_section_rows < 1:
        raise ValueError("sample_context_section_rows must be positive")

    loaded = _load_full_sections_pickle(source)
    structure = _object_structure(loaded)
    scan = _scan_records(loaded, collect_rows=True)
    sections = pd.DataFrame(scan.pop("rows"), columns=SECTIONED_COLUMNS)

    output = Path(out_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    sections.to_parquet(output, index=False)

    sample_metrics = _write_sectioned_context_sample(
        sections,
        references_path=Path(references_path),
        out_path=Path(sample_contexts_out) if sample_contexts_out is not None else None,
        sample_section_rows=sample_context_section_rows,
    )

    metrics = {
        **structure,
        **scan,
        "out_path": output,
        "sample_contexts": sample_metrics,
    }
    report = _build_parse_report(
        input_path=source,
        out_path=output,
        metrics=metrics,
    )
    _write_report(report_path, report)
    return FullSectionsParseResult(sections=sections, metrics=metrics)


def normalize_section_name(section_name: Any) -> str:
    """Normalize explicit section headings into the Task 6.4A section taxonomy.

    Precedence is intentionally conservative. For compound headings such as
    "Experiments and Results", `experiment` wins because those sections usually define
    experimental setup before reporting outcomes.
    """
    text = _clean_text(section_name)
    if text is None:
        return "unknown"
    normalized = _normalize_heading_text(text)
    if not normalized:
        return "unknown"

    if _contains_any(normalized, ["abstract"]):
        return "abstract"
    if _contains_any(normalized, ["intro", "introduction", "overview"]):
        return "introduction"
    if _contains_any(
        normalized,
        ["related work", "previous work", "prior work", "literature review"],
    ):
        return "related_work"
    if _contains_any(normalized, ["background", "preliminar"]):
        return "background"
    if _contains_any(normalized, ["method", "methodology", "approach", "algorithm"]):
        return "method"
    if _contains_any(normalized, ["model", "architecture"]):
        return "model"
    if _contains_any(normalized, ["experiment", "experimental", "setup"]):
        return "experiment"
    if _contains_any(normalized, ["evaluation", "eval", "assessment"]):
        return "evaluation"
    if _contains_any(normalized, ["result", "analysis"]):
        return "results"
    if _contains_any(normalized, ["discussion", "error analysis", "limitations"]):
        return "discussion"
    if _contains_any(normalized, ["conclusion", "future work", "summary"]):
        return "conclusion"
    if _contains_any(normalized, ["appendix", "supplement"]):
        return "appendix"
    if _contains_any(normalized, ["reference", "bibliography"]):
        return "references"
    return "unknown"


def _load_full_sections_pickle(path: Path) -> Any:
    _install_pandas_pickle_compat()
    opener = gzip.open if _is_gzip(path) else open
    with opener(path, "rb") as handle:
        return pickle.load(handle)


def _install_pandas_pickle_compat() -> None:
    if "pandas.core.indexes.numeric" in sys.modules:
        return
    numeric_module = types.ModuleType("pandas.core.indexes.numeric")
    numeric_module.Int64Index = pd.Index
    numeric_module.UInt64Index = pd.Index
    numeric_module.Float64Index = pd.Index
    sys.modules["pandas.core.indexes.numeric"] = numeric_module


def _is_gzip(path: Path) -> bool:
    with path.open("rb") as handle:
        return handle.read(2) == b"\x1f\x8b"


def _source_availability(root: Path, full_sections_path: Path) -> dict[str, Any]:
    tei_files = [
        path.relative_to(root).as_posix()
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.suffix.lower() in {".tei", ".xml"}
    ]
    full_text_json = root / "Full_text_JSON.tar.gz"
    return {
        "full_sections_exists": full_sections_path.exists(),
        "full_sections_path": full_sections_path,
        "full_sections_size_bytes": (
            full_sections_path.stat().st_size if full_sections_path.exists() else None
        ),
        "full_text_json_exists": full_text_json.exists(),
        "full_text_json_path": full_text_json,
        "tei_or_xml_file_count": len(tei_files),
        "tei_or_xml_samples": tei_files[:10],
    }


def _object_structure(obj: Any) -> dict[str, Any]:
    rows: list[dict[str, Any]]
    if isinstance(obj, pd.DataFrame):
        rows = _sample_records(obj.head(3).to_dict(orient="records"))
        return {
            "pickle_object_type": f"{type(obj).__module__}.{type(obj).__name__}",
            "pickle_shape": [int(obj.shape[0]), int(obj.shape[1])],
            "top_level_columns": list(obj.columns),
            "top_level_keys": None,
            "sample_records": rows,
        }
    if isinstance(obj, dict):
        return {
            "pickle_object_type": f"{type(obj).__module__}.{type(obj).__name__}",
            "pickle_shape": [len(obj)],
            "top_level_columns": None,
            "top_level_keys": [str(key) for key in list(obj.keys())[:20]],
            "sample_records": _sample_records(
                [record for _, record in zip(range(3), _iter_records(obj), strict=False)]
            ),
        }
    if isinstance(obj, list):
        return {
            "pickle_object_type": f"{type(obj).__module__}.{type(obj).__name__}",
            "pickle_shape": [len(obj)],
            "top_level_columns": None,
            "top_level_keys": None,
            "sample_records": _sample_records(obj[:3]),
        }
    return {
        "pickle_object_type": f"{type(obj).__module__}.{type(obj).__name__}",
        "pickle_shape": None,
        "top_level_columns": None,
        "top_level_keys": None,
        "sample_records": [_truncate_repr(obj)],
    }


def _scan_records(obj: Any, *, collect_rows: bool) -> dict[str, Any]:
    total_records = 0
    papers_with_acl_id = 0
    papers_with_section_data = 0
    papers_with_citation_markers = 0
    paragraph_rows = 0
    non_empty_section_names = 0
    normalized_counts = dict.fromkeys(NORMALIZED_SECTIONS, 0)
    rows: list[dict[str, Any]] = []

    for record_index, record in enumerate(_iter_records(obj)):
        total_records += 1
        paper_id = _paper_id(record, record_index)
        if _clean_text(_first_value(record, ["acl_id", "paper_id", "anthology_id", "id"])):
            papers_with_acl_id += 1
        paragraphs = _paragraph_candidates_from_record(record)
        if any(paragraph.section_name for paragraph in paragraphs):
            papers_with_section_data += 1
        if any(paragraph.citation_marker_count for paragraph in paragraphs):
            papers_with_citation_markers += 1

        section_indexes: dict[str, int] = {}
        paragraph_indexes: dict[int, int] = {}
        for paragraph in paragraphs:
            section_key = paragraph.section_name or "unknown"
            if section_key not in section_indexes:
                section_indexes[section_key] = len(section_indexes)
            section_index = section_indexes[section_key]
            paragraph_index = paragraph_indexes.get(section_index, 0)
            paragraph_indexes[section_index] = paragraph_index + 1

            paragraph_rows += 1
            if paragraph.section_name:
                non_empty_section_names += 1
            normalized_section = normalize_section_name(paragraph.section_name)
            normalized_counts[normalized_section] = normalized_counts.get(
                normalized_section,
                0,
            ) + 1
            if collect_rows:
                rows.append(
                    {
                        "paper_id": paper_id,
                        "section_name": paragraph.section_name,
                        "normalized_section": normalized_section,
                        "section_index": section_index,
                        "paragraph_id": (
                            f"{paper_id}_s{section_index:04d}_p{paragraph_index:04d}"
                        ),
                        "paragraph_index": paragraph_index,
                        "paragraph_text": paragraph.paragraph_text,
                    }
                )

    distribution = _normalized_distribution_from_counts(normalized_counts)
    return {
        "input_record_count": total_records,
        "papers_with_acl_id": papers_with_acl_id,
        "papers_with_section_data": papers_with_section_data,
        "papers_with_citation_markers": papers_with_citation_markers,
        "recoverable_paragraph_rows": paragraph_rows,
        "section_name_non_empty_rate": _rate(non_empty_section_names, paragraph_rows),
        "contains_acl_id": papers_with_acl_id > 0,
        "contains_section_title": non_empty_section_names > 0,
        "contains_paragraph_text": paragraph_rows > 0,
        "contains_paragraph_order": paragraph_rows > 0,
        "contains_citation_markers": papers_with_citation_markers > 0,
        "normalized_section_distribution": distribution,
        "rows": rows,
    }


def _iter_records(obj: Any) -> Iterator[dict[str, Any]]:
    if isinstance(obj, pd.DataFrame):
        columns = list(obj.columns)
        for row in obj.itertuples(index=False, name=None):
            yield {column: value for column, value in zip(columns, row, strict=True)}
        return
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, dict):
                record = dict(value)
                record.setdefault("acl_id", key)
                yield record
            else:
                yield {"acl_id": key, "json_contents": value}
        return
    if isinstance(obj, list):
        for index, value in enumerate(obj):
            if isinstance(value, dict):
                yield dict(value)
            else:
                yield {"id": index, "json_contents": value}
        return
    yield {"json_contents": obj}


def _paragraph_candidates_from_record(record: dict[str, Any]) -> list[_ParagraphCandidate]:
    paragraphs: list[_ParagraphCandidate] = []
    contents = _maybe_json(_first_value(record, ["json_contents", "json", "contents"]))
    if isinstance(contents, dict):
        pdf_parse = _maybe_json(contents.get("pdf_parse"))
        if isinstance(pdf_parse, dict):
            paragraphs.extend(_paragraphs_from_s2orc_parse(pdf_parse))
        else:
            paragraphs.extend(_paragraphs_from_s2orc_parse(contents))
            paragraphs.extend(_paragraphs_from_sections(contents))

    paragraphs.extend(_paragraphs_from_sections(record))
    if not paragraphs:
        abstract = _clean_text(_first_value(record, ["abstract"]))
        if abstract:
            paragraphs.append(
                _ParagraphCandidate(
                    section_name="Abstract",
                    paragraph_text=abstract,
                    citation_marker_count=_citation_marker_count(abstract, None),
                )
            )
    return _dedupe_paragraphs(paragraphs)


def _paragraphs_from_s2orc_parse(parse: dict[str, Any]) -> list[_ParagraphCandidate]:
    rows: list[_ParagraphCandidate] = []
    for key in ("abstract", "body_text", "back_matter"):
        for item in _coerce_sequence(parse.get(key)):
            text, section_name, cite_spans = _paragraph_fields(
                item,
                default_section="Abstract" if key == "abstract" else None,
            )
            if text:
                rows.append(
                    _ParagraphCandidate(
                        section_name=section_name,
                        paragraph_text=text,
                        citation_marker_count=_citation_marker_count(text, cite_spans),
                    )
                )
    return rows


def _paragraphs_from_sections(record: dict[str, Any]) -> list[_ParagraphCandidate]:
    rows: list[_ParagraphCandidate] = []
    sections = _coerce_sequence(_first_value(record, ["sections", "section_list"]))
    for section in sections:
        if isinstance(section, dict):
            section_name = _clean_text(
                _first_value(section, ["section_name", "section", "name", "heading", "title"])
            )
            paragraphs = _coerce_sequence(
                _first_value(section, ["paragraphs", "paragraph", "text", "body"])
            )
            for paragraph in paragraphs:
                text, paragraph_section, cite_spans = _paragraph_fields(
                    paragraph,
                    default_section=section_name,
                )
                if text:
                    rows.append(
                        _ParagraphCandidate(
                            section_name=paragraph_section,
                            paragraph_text=text,
                            citation_marker_count=_citation_marker_count(text, cite_spans),
                        )
                    )
        else:
            text = _clean_text(section)
            if text:
                rows.append(
                    _ParagraphCandidate(
                        section_name=None,
                        paragraph_text=text,
                        citation_marker_count=_citation_marker_count(text, None),
                    )
                )

    flat_paragraphs = _coerce_sequence(
        _first_value(record, ["paragraphs", "paragraph", "paragraph_text"])
    )
    for paragraph in flat_paragraphs:
        text, section_name, cite_spans = _paragraph_fields(paragraph, default_section=None)
        if text:
            rows.append(
                _ParagraphCandidate(
                    section_name=section_name,
                    paragraph_text=text,
                    citation_marker_count=_citation_marker_count(text, cite_spans),
                )
            )
    return rows


def _paragraph_fields(
    value: Any,
    *,
    default_section: str | None,
) -> tuple[str | None, str | None, Any]:
    value = _maybe_json(value)
    if isinstance(value, dict):
        text = _clean_text(
            _first_value(value, ["paragraph_text", "text", "content", "paragraph", "body"])
        )
        section_name = _clean_text(
            _first_value(value, ["section", "section_name", "section_title", "heading"])
        ) or default_section
        cite_spans = _first_value(value, ["cite_spans", "citation_spans", "citations"])
        return text, section_name, cite_spans
    return _clean_text(value), default_section, None


def _dedupe_paragraphs(paragraphs: list[_ParagraphCandidate]) -> list[_ParagraphCandidate]:
    seen: set[tuple[str | None, str]] = set()
    deduped: list[_ParagraphCandidate] = []
    for paragraph in paragraphs:
        key = (paragraph.section_name, paragraph.paragraph_text)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(paragraph)
    return deduped


def _paper_id(record: dict[str, Any], record_index: int) -> str:
    value = _clean_text(_first_value(record, ["acl_id", "paper_id", "anthology_id", "id", "ID"]))
    return value or f"unknown_{record_index:06d}"


def _write_sectioned_context_sample(
    sections: pd.DataFrame,
    *,
    references_path: Path,
    out_path: Path | None,
    sample_section_rows: int,
) -> dict[str, Any]:
    if out_path is None:
        return {"status": "skipped", "reason": "sample_contexts_out was not provided"}
    if sections.empty:
        return {"status": "skipped", "reason": "no section rows were parsed"}

    sample_sections = sections.head(sample_section_rows)[CONTEXT_SECTION_COLUMNS].copy()
    with tempfile.TemporaryDirectory(prefix="citeevidence_sections_") as tmp:
        tmp_dir = Path(tmp)
        sections_path = tmp_dir / "sections.parquet"
        refs_path = references_path if references_path.exists() else tmp_dir / "references.parquet"
        sample_sections.to_parquet(sections_path, index=False)
        if not references_path.exists():
            pd.DataFrame(columns=REFERENCE_COLUMNS).to_parquet(refs_path, index=False)
        contexts = extract_citation_contexts(
            sections_path=sections_path,
            references_path=refs_path,
            out_path=out_path,
        )
    return {
        "status": "written",
        "path": out_path,
        "section_rows_sampled": int(len(sample_sections)),
        "context_rows": int(len(contexts)),
    }


def _normalized_distribution(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not rows:
        return []
    frame = pd.DataFrame(rows)
    counts = (
        frame["normalized_section"]
        .value_counts(dropna=False)
        .rename_axis("normalized_section")
        .reset_index(name="paragraph_rows")
    )
    return _records(counts)


def _normalized_distribution_from_counts(counts: dict[str, int]) -> list[dict[str, Any]]:
    rows = [
        {"normalized_section": section, "paragraph_rows": int(count)}
        for section, count in counts.items()
        if count
    ]
    return sorted(rows, key=lambda row: row["paragraph_rows"], reverse=True)


def _build_missing_full_sections_report(root: Path, metrics: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# ACL-OCL Full-Sections Structure Report",
            "",
            "## Source Availability",
            _table(
                [
                    {"source": "full_sections_pkl", "available": False, "path": root},
                    {
                        "source": "Full_text_JSON.tar.gz",
                        "available": metrics["full_text_json_exists"],
                        "path": metrics["full_text_json_path"],
                    },
                    {
                        "source": "GROBID / TEI XML",
                        "available": metrics["tei_or_xml_file_count"] > 0,
                        "files": metrics["tei_or_xml_file_count"],
                    },
                ]
            ),
            "",
            "The expected full-sections pickle was not found; inspection completed without "
            "crashing.",
            "",
        ]
    )


def _build_structure_report(
    *,
    raw_dir: Path,
    full_sections_path: Path,
    metrics: dict[str, Any],
) -> str:
    return "\n".join(
        [
            "# ACL-OCL Full-Sections Structure Report",
            "",
            "## Source Availability",
            _table(
                [
                    {
                        "source": "full_sections_pkl",
                        "available": metrics["full_sections_exists"],
                        "path": full_sections_path,
                        "bytes": metrics["full_sections_size_bytes"],
                    },
                    {
                        "source": "Full_text_JSON.tar.gz",
                        "available": metrics["full_text_json_exists"],
                        "path": metrics["full_text_json_path"],
                    },
                    {
                        "source": "GROBID / TEI XML",
                        "available": metrics["tei_or_xml_file_count"] > 0,
                        "files": metrics["tei_or_xml_file_count"],
                        "samples": "; ".join(metrics["tei_or_xml_samples"]),
                    },
                ]
            ),
            "",
            "## Pickle Object",
            _table(
                [
                    {
                        "metric": "object_type",
                        "value": metrics["pickle_object_type"],
                    },
                    {"metric": "shape", "value": metrics["pickle_shape"]},
                    {"metric": "raw_dir", "value": raw_dir},
                ]
            ),
            "",
            "## Top-Level Columns / Keys",
            _table(
                [
                    {
                        "columns": "; ".join(metrics["top_level_columns"] or []),
                        "keys": "; ".join(metrics["top_level_keys"] or []),
                    }
                ]
            ),
            "",
            "## Sample Records",
            _table([{"record": record} for record in metrics["sample_records"]]),
            "",
            "## Recoverable Signals",
            _table(_signal_rows(metrics)),
            "",
            "## Section Metrics",
            _table(_section_metric_rows(metrics)),
            "",
            "## Normalized Section Distribution",
            _table(metrics["normalized_section_distribution"]),
            "",
            "## Normalization Note",
            (
                "`Experiments and Results` is normalized to `experiment`; the parser uses "
                "explicit section headings only and does not infer headings from paragraph "
                "content."
            ),
            "",
        ]
    )


def _build_parse_report(
    *,
    input_path: Path,
    out_path: Path,
    metrics: dict[str, Any],
) -> str:
    sample = metrics["sample_contexts"]
    return "\n".join(
        [
            "# ACL-OCL Full-Sections Parse Report",
            "",
            "## Inputs / Outputs",
            _table(
                [
                    {"name": "input", "path": input_path, "status": "read"},
                    {"name": "acl_sections_sectioned", "path": out_path, "status": "written"},
                    {
                        "name": "citation_contexts_sectioned_sample",
                        "path": sample.get("path"),
                        "status": sample.get("status"),
                    },
                ]
            ),
            "",
            "## Pickle Object",
            _table(
                [
                    {"metric": "object_type", "value": metrics["pickle_object_type"]},
                    {"metric": "shape", "value": metrics["pickle_shape"]},
                ]
            ),
            "",
            "## Recoverable Signals",
            _table(_signal_rows(metrics)),
            "",
            "## Section Metrics",
            _table(_section_metric_rows(metrics)),
            "",
            "## Normalized Section Distribution",
            _table(metrics["normalized_section_distribution"]),
            "",
            "## Sample Context Extraction",
            _table([sample]),
            "",
            "## Normalization Note",
            (
                "`Experiments and Results` is normalized to `experiment`; section names are "
                "taken from explicit full-sections metadata, not inferred from paragraph text."
            ),
            "",
        ]
    )


def _signal_rows(metrics: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {"signal": "acl_id", "present": metrics["contains_acl_id"]},
        {"signal": "section title", "present": metrics["contains_section_title"]},
        {"signal": "paragraph text", "present": metrics["contains_paragraph_text"]},
        {"signal": "paragraph order", "present": metrics["contains_paragraph_order"]},
        {"signal": "citation markers", "present": metrics["contains_citation_markers"]},
    ]


def _section_metric_rows(metrics: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {"metric": "input records", "value": metrics["input_record_count"]},
        {"metric": "papers with acl_id", "value": metrics["papers_with_acl_id"]},
        {"metric": "papers with section data", "value": metrics["papers_with_section_data"]},
        {
            "metric": "papers with citation markers",
            "value": metrics["papers_with_citation_markers"],
        },
        {
            "metric": "recoverable section / paragraph rows",
            "value": metrics["recoverable_paragraph_rows"],
        },
        {
            "metric": "section name non-empty rate",
            "value": metrics["section_name_non_empty_rate"],
        },
    ]


def _sample_records(records: list[Any]) -> list[str]:
    return [_truncate_record(record) for record in records]


def _truncate_record(record: Any) -> str:
    value = _maybe_json(record)
    if isinstance(value, dict):
        safe: dict[str, Any] = {}
        for key, item in list(value.items())[:12]:
            safe[str(key)] = _truncate_value(item)
        return json.dumps(safe, ensure_ascii=False, sort_keys=True, default=str)
    return _truncate_repr(value)


def _truncate_value(value: Any, max_chars: int = 220) -> Any:
    value = _maybe_json(value)
    if isinstance(value, dict):
        return {str(key): _truncate_value(item, 80) for key, item in list(value.items())[:8]}
    if isinstance(value, list):
        return [_truncate_value(item, 80) for item in value[:3]]
    text = _clean_text(value)
    if text is None:
        return None
    return text if len(text) <= max_chars else f"{text[: max_chars - 3]}..."


def _truncate_repr(value: Any, max_chars: int = 1000) -> str:
    text = repr(value)
    return text if len(text) <= max_chars else f"{text[: max_chars - 3]}..."


def _citation_marker_count(text: str, cite_spans: Any) -> int:
    spans = _coerce_sequence(cite_spans)
    if spans:
        return len(spans)
    return len(CITATION_MARKER_RE.findall(text))


def _contains_any(text: str, needles: list[str]) -> bool:
    return any(needle in text for needle in needles)


def _normalize_heading_text(text: str) -> str:
    text = re.sub(r"^\s*(?:appendix\s+)?[0-9ivxlcdm]+(?:\.[0-9]+)*\.?\s+", "", text)
    text = re.sub(r"[^a-zA-Z0-9&/ -]", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def _first_value(record: dict[str, Any], aliases: list[str]) -> Any:
    lower_lookup = {str(key).lower(): value for key, value in record.items()}
    for alias in aliases:
        if alias.lower() in lower_lookup:
            return lower_lookup[alias.lower()]
    return None


def _maybe_json(value: Any) -> Any:
    if isinstance(value, str):
        stripped = value.strip()
        if stripped and stripped[0] in "[{":
            try:
                return json.loads(stripped)
            except json.JSONDecodeError:
                return value
    return value


def _coerce_sequence(value: Any) -> list[Any]:
    value = _maybe_json(value)
    if value is None or _is_missing(value):
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, dict):
        return [value]
    return [value]


def _clean_text(value: Any) -> str | None:
    value = _maybe_json(value)
    if value is None or _is_missing(value):
        return None
    if isinstance(value, dict):
        text = json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
    elif isinstance(value, list):
        text = " ".join(_clean_text(item) or "" for item in value)
    else:
        text = str(value)
    text = re.sub(r"\s+", " ", text).strip()
    return text or None


def _is_missing(value: Any) -> bool:
    if isinstance(value, (list, dict, tuple)):
        return False
    try:
        return bool(pd.isna(value))
    except (TypeError, ValueError):
        return False


def _rate(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.000"
    return f"{numerator / denominator:.3f}"


def _records(frame: pd.DataFrame) -> list[dict[str, Any]]:
    if frame.empty:
        return []
    clean = frame.where(pd.notna(frame), None)
    return clean.to_dict(orient="records")


def _write_report(path: str | Path, report: str) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")


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
    if value is None or _is_missing(value):
        return "unavailable"
    text = _clean_text(value) or ""
    if len(text) > 160:
        text = f"{text[:157]}..."
    return text.replace("|", "\\|")
