from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
from lxml import etree

PAPER_COLUMNS = [
    "paper_id",
    "title",
    "year",
    "venue",
    "doi_or_acl_id",
    "source_file",
    "parse_status",
    "parse_error",
]
REFERENCE_COLUMNS = [
    "citing_paper_id",
    "reference_key",
    "cited_title",
    "cited_year",
    "cited_authors",
    "cited_doi",
    "raw_reference",
]
SECTION_COLUMNS = [
    "paper_id",
    "section_name",
    "paragraph_id",
    "paragraph_text",
]

SUPPORTED_EXTENSIONS = {
    ".xml",
    ".tei",
    ".json",
    ".jsonl",
    ".ndjson",
    ".parquet",
    ".txt",
    ".text",
    ".md",
    ".pdf",
}


@dataclass(frozen=True)
class AclParseResult:
    papers: pd.DataFrame
    references: pd.DataFrame
    sections: pd.DataFrame


def parse_acl_ocl_data(
    input_dir: str | Path,
    *,
    out_dir: str | Path,
    max_files: int | None = None,
) -> AclParseResult:
    """Parse flexible ACL-OCL raw inputs into normalized interim parquet tables."""
    root = Path(input_dir)
    if not root.exists():
        raise FileNotFoundError(f"ACL-OCL input path does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"ACL-OCL input path must be a directory: {root}")
    if max_files is not None and max_files < 1:
        raise ValueError("max_files must be positive when provided")

    files = [path for path in sorted(root.rglob("*")) if path.is_file()]
    if max_files is not None:
        files = files[:max_files]

    paper_rows: list[dict[str, Any]] = []
    reference_rows: list[dict[str, Any]] = []
    section_rows: list[dict[str, Any]] = []

    for path in files:
        parsed = _parse_file(path, root)
        paper_rows.extend(parsed.papers)
        reference_rows.extend(parsed.references)
        section_rows.extend(parsed.sections)

    papers = pd.DataFrame(paper_rows, columns=PAPER_COLUMNS)
    references = pd.DataFrame(reference_rows, columns=REFERENCE_COLUMNS)
    sections = pd.DataFrame(section_rows, columns=SECTION_COLUMNS)

    output_dir = Path(out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    papers.to_parquet(output_dir / "acl_papers.parquet", index=False)
    references.to_parquet(output_dir / "acl_references.parquet", index=False)
    sections.to_parquet(output_dir / "acl_sections.parquet", index=False)

    return AclParseResult(papers=papers, references=references, sections=sections)


@dataclass
class _ParsedFile:
    papers: list[dict[str, Any]]
    references: list[dict[str, Any]]
    sections: list[dict[str, Any]]


def _parse_file(path: Path, root: Path) -> _ParsedFile:
    source_file = path.relative_to(root).as_posix()
    extension = path.suffix.lower()

    try:
        if extension == ".pdf":
            return _skipped_pdf(path, source_file)
        if extension in {".xml", ".tei"}:
            return _parse_tei_xml(path, source_file)
        if extension == ".json":
            return _parse_json(path, source_file)
        if extension in {".jsonl", ".ndjson"}:
            return _parse_jsonl(path, source_file)
        if extension == ".parquet":
            return _parse_parquet(path, source_file)
        if extension in {".txt", ".text", ".md"}:
            return _parse_plain_text(path, source_file)
        if extension not in SUPPORTED_EXTENSIONS:
            return _unsupported_file(path, source_file, f"Unsupported file extension: {extension}")
    except Exception as exc:  # noqa: BLE001 - file-level parse failures become status rows.
        return _error_file(path, source_file, exc)

    return _unsupported_file(path, source_file, f"Unsupported file extension: {extension}")


def _parse_tei_xml(path: Path, source_file: str) -> _ParsedFile:
    parser = etree.XMLParser(recover=False, resolve_entities=False, no_network=True)
    tree = etree.parse(str(path), parser)
    root = tree.getroot()
    title = _first_xpath_text(
        root,
        [
            ".//*[local-name()='teiHeader']//*[local-name()='titleStmt']/*[local-name()='title']",
            ".//*[local-name()='title']",
        ],
    )
    year = _first_year(
        [
            _first_xpath_attr(root, ".//*[local-name()='date']", "when"),
            _first_xpath_text(root, [".//*[local-name()='date']"]),
            title,
            etree.tostring(root, encoding="unicode", method="text")[:4096],
        ]
    )
    venue = _first_xpath_text(
        root,
        [
            ".//*[local-name()='monogr']/*[local-name()='title']",
            ".//*[local-name()='series']/*[local-name()='title']",
        ],
    )
    doi_or_acl_id = _first_idno(root)
    paper_id = _deterministic_paper_id(
        source_file=source_file,
        title=title,
        doi_or_acl_id=doi_or_acl_id,
        content_hint=_text_content(root)[:2048],
    )

    papers = [
        _paper_row(
            paper_id=paper_id,
            title=title,
            year=year,
            venue=venue,
            doi_or_acl_id=doi_or_acl_id,
            source_file=source_file,
            parse_status="parsed",
            parse_error=None,
        )
    ]

    references = _references_from_tei(root, paper_id)
    sections = _sections_from_tei(root, paper_id)
    return _ParsedFile(papers=papers, references=references, sections=sections)


def _parse_json(path: Path, source_file: str) -> _ParsedFile:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    records = _json_records(loaded)
    return _parse_structured_records(records, source_file=source_file)


def _parse_jsonl(path: Path, source_file: str) -> _ParsedFile:
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        loaded = json.loads(line)
        if not isinstance(loaded, dict):
            raise ValueError(f"Expected JSON object at {source_file}:{line_number}")
        records.append(loaded)
    return _parse_structured_records(records, source_file=source_file)


def _parse_parquet(path: Path, source_file: str) -> _ParsedFile:
    frame = pd.read_parquet(path)
    if _is_acl_citation_edge_frame(frame):
        return _parse_acl_citation_edges(frame)
    records = [
        _json_like_record(row)
        for row in frame.to_dict(orient="records")
    ]
    return _parse_structured_records(records, source_file=source_file)


def _is_acl_citation_edge_frame(frame: pd.DataFrame) -> bool:
    required = {"id", "citingpaperid", "citedpaperid"}
    return required <= {column.lower() for column in frame.columns}


def _parse_acl_citation_edges(frame: pd.DataFrame) -> _ParsedFile:
    references = pd.DataFrame(
        {
            "citing_paper_id": frame["citingpaperid"].astype("string"),
            "reference_key": frame["id"].astype("string"),
            "cited_title": None,
            "cited_year": None,
            "cited_authors": None,
            "cited_doi": None,
            "raw_reference": frame["citedpaperid"].astype("string"),
        },
        columns=REFERENCE_COLUMNS,
    )
    return _ParsedFile(
        papers=[],
        references=list(references.to_dict(orient="records")),
        sections=[],
    )


def _parse_structured_records(
    records: list[dict[str, Any]],
    *,
    source_file: str,
) -> _ParsedFile:
    papers: list[dict[str, Any]] = []
    references: list[dict[str, Any]] = []
    sections: list[dict[str, Any]] = []

    if not records:
        paper_id = _deterministic_paper_id(source_file=source_file)
        papers.append(
            _paper_row(
                paper_id=paper_id,
                title=None,
                year=None,
                venue=None,
                doi_or_acl_id=None,
                source_file=source_file,
                parse_status="empty",
                parse_error="Structured file contained no records.",
            )
        )
        return _ParsedFile(papers=papers, references=references, sections=sections)

    for index, record in enumerate(records):
        title = _clean_string(_first_value(record, ["title", "paper_title", "document_title"]))
        year = _parse_year(_first_value(record, ["year", "publication_year", "pub_year", "date"]))
        venue = _clean_string(
            _first_value(record, ["venue", "booktitle", "journal", "conference", "event"])
        )
        doi_or_acl_id = _clean_string(
            _first_value(record, ["doi_or_acl_id", "doi", "acl_id", "anthology_id"])
        )
        paper_id = _clean_string(
            _first_value(record, ["paper_id", "acl_id", "anthology_id", "document_id", "id"])
        ) or _deterministic_paper_id(
            source_file=source_file,
            title=title,
            doi_or_acl_id=doi_or_acl_id,
            content_hint=json.dumps(record, sort_keys=True, default=str)[:2048],
            record_index=index,
        )

        record_sections = _sections_from_record(record, paper_id)
        record_references = _references_from_record(record, paper_id)
        status = "parsed" if title or record_sections or record_references else "partial"
        error = None if status == "parsed" else "No title, sections, or references found."

        papers.append(
            _paper_row(
                paper_id=paper_id,
                title=title,
                year=year,
                venue=venue,
                doi_or_acl_id=doi_or_acl_id,
                source_file=source_file,
                parse_status=status,
                parse_error=error,
            )
        )
        sections.extend(record_sections)
        references.extend(record_references)

    return _ParsedFile(papers=papers, references=references, sections=sections)


def _parse_plain_text(path: Path, source_file: str) -> _ParsedFile:
    text = path.read_text(encoding="utf-8", errors="ignore")
    title = _title_from_plain_text(text)
    year = _first_year([text[:4096]])
    paper_id = _deterministic_paper_id(
        source_file=source_file,
        title=title,
        content_hint=text[:2048],
    )
    sections = _sections_from_plain_text(text, paper_id)
    references = _references_from_plain_text(text, paper_id)
    return _ParsedFile(
        papers=[
            _paper_row(
                paper_id=paper_id,
                title=title,
                year=year,
                venue=None,
                doi_or_acl_id=None,
                source_file=source_file,
                parse_status="parsed",
                parse_error=None,
            )
        ],
        references=references,
        sections=sections,
    )


def _skipped_pdf(path: Path, source_file: str) -> _ParsedFile:
    paper_id = _deterministic_paper_id(source_file=source_file, content_hint=path.name)
    return _ParsedFile(
        papers=[
            _paper_row(
                paper_id=paper_id,
                title=None,
                year=None,
                venue=None,
                doi_or_acl_id=None,
                source_file=source_file,
                parse_status="skipped_pdf",
                parse_error="PDF parsing is intentionally unsupported; raw PDFs are not stored.",
            )
        ],
        references=[],
        sections=[],
    )


def _unsupported_file(path: Path, source_file: str, message: str) -> _ParsedFile:
    paper_id = _deterministic_paper_id(source_file=source_file, content_hint=path.name)
    return _ParsedFile(
        papers=[
            _paper_row(
                paper_id=paper_id,
                title=None,
                year=None,
                venue=None,
                doi_or_acl_id=None,
                source_file=source_file,
                parse_status="unsupported",
                parse_error=message,
            )
        ],
        references=[],
        sections=[],
    )


def _error_file(path: Path, source_file: str, exc: Exception) -> _ParsedFile:
    paper_id = _deterministic_paper_id(source_file=source_file, content_hint=path.name)
    return _ParsedFile(
        papers=[
            _paper_row(
                paper_id=paper_id,
                title=None,
                year=None,
                venue=None,
                doi_or_acl_id=None,
                source_file=source_file,
                parse_status="error",
                parse_error=f"{type(exc).__name__}: {str(exc)[:500]}",
            )
        ],
        references=[],
        sections=[],
    )


def _paper_row(
    *,
    paper_id: str,
    title: str | None,
    year: int | None,
    venue: str | None,
    doi_or_acl_id: str | None,
    source_file: str,
    parse_status: str,
    parse_error: str | None,
) -> dict[str, Any]:
    return {
        "paper_id": paper_id,
        "title": title,
        "year": year,
        "venue": venue,
        "doi_or_acl_id": doi_or_acl_id,
        "source_file": source_file,
        "parse_status": parse_status,
        "parse_error": parse_error,
    }


def _reference_row(
    *,
    citing_paper_id: str,
    reference_key: str,
    cited_title: str | None,
    cited_year: int | None,
    cited_authors: str | None,
    cited_doi: str | None,
    raw_reference: str | None,
) -> dict[str, Any]:
    return {
        "citing_paper_id": citing_paper_id,
        "reference_key": reference_key,
        "cited_title": cited_title,
        "cited_year": cited_year,
        "cited_authors": cited_authors,
        "cited_doi": cited_doi,
        "raw_reference": raw_reference,
    }


def _section_row(
    *,
    paper_id: str,
    section_name: str | None,
    paragraph_id: str,
    paragraph_text: str,
) -> dict[str, Any]:
    return {
        "paper_id": paper_id,
        "section_name": section_name,
        "paragraph_id": paragraph_id,
        "paragraph_text": paragraph_text,
    }


def _sections_from_tei(root: etree._Element, paper_id: str) -> list[dict[str, Any]]:
    section_rows: list[dict[str, Any]] = []
    divs = root.xpath(".//*[local-name()='body']//*[local-name()='div']")
    if divs:
        for div_index, div in enumerate(divs):
            section_name = _first_child_text(div, "head") or _attribute(div, "type")
            paragraphs = div.xpath(".//*[local-name()='p']")
            for paragraph_index, paragraph in enumerate(paragraphs):
                text = _clean_string(" ".join(paragraph.itertext()))
                if text:
                    paragraph_id = (
                        _element_id(paragraph) or f"{paper_id}_d{div_index}_p{paragraph_index}"
                    )
                    section_rows.append(
                        _section_row(
                            paper_id=paper_id,
                            section_name=section_name,
                            paragraph_id=paragraph_id,
                            paragraph_text=text,
                        )
                    )
    else:
        paragraphs = root.xpath(".//*[local-name()='body']//*[local-name()='p']")
        for paragraph_index, paragraph in enumerate(paragraphs):
            text = _clean_string(" ".join(paragraph.itertext()))
            if text:
                paragraph_id = _element_id(paragraph) or f"{paper_id}_p{paragraph_index}"
                section_rows.append(
                    _section_row(
                        paper_id=paper_id,
                        section_name=None,
                        paragraph_id=paragraph_id,
                        paragraph_text=text,
                    )
                )
    return section_rows


def _references_from_tei(root: etree._Element, paper_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    bibliographic_nodes = root.xpath(".//*[local-name()='biblStruct' or local-name()='bibl']")
    for index, bibl in enumerate(bibliographic_nodes):
        reference_key = _element_id(bibl) or f"ref_{index}"
        cited_title = _first_xpath_text(
            bibl,
            [
                ".//*[local-name()='analytic']/*[local-name()='title']",
                ".//*[local-name()='title']",
            ],
        )
        cited_year = _first_year(
            [
                _first_xpath_attr(bibl, ".//*[local-name()='date']", "when"),
                _first_xpath_text(bibl, [".//*[local-name()='date']"]),
                _text_content(bibl),
            ]
        )
        cited_authors = _authors_from_tei_bibl(bibl)
        cited_doi = _first_idno(bibl, id_types={"doi"})
        raw_reference = _clean_string(" ".join(bibl.itertext()))
        rows.append(
            _reference_row(
                citing_paper_id=paper_id,
                reference_key=reference_key,
                cited_title=cited_title,
                cited_year=cited_year,
                cited_authors=cited_authors,
                cited_doi=cited_doi,
                raw_reference=raw_reference,
            )
        )
    return rows


def _sections_from_record(record: dict[str, Any], paper_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sections = _coerce_sequence(_first_value(record, ["sections", "section_list"]))
    for section_index, section in enumerate(sections):
        if isinstance(section, dict):
            section_name = _clean_string(
                _first_value(section, ["section_name", "name", "heading", "title"])
            )
            paragraph_values = _coerce_sequence(
                _first_value(section, ["paragraphs", "paragraph", "text", "body"])
            )
            for paragraph_index, paragraph in enumerate(paragraph_values):
                paragraph_text = _paragraph_text(paragraph)
                if paragraph_text:
                    paragraph_id = _paragraph_id(
                        paragraph,
                        default=f"{paper_id}_s{section_index}_p{paragraph_index}",
                    )
                    rows.append(
                        _section_row(
                            paper_id=paper_id,
                            section_name=section_name,
                            paragraph_id=paragraph_id,
                            paragraph_text=paragraph_text,
                        )
                    )
        else:
            paragraph_text = _clean_string(section)
            if paragraph_text:
                rows.append(
                    _section_row(
                        paper_id=paper_id,
                        section_name=None,
                        paragraph_id=f"{paper_id}_s{section_index}",
                        paragraph_text=paragraph_text,
                    )
                )

    paragraph_values = _coerce_sequence(
        _first_value(record, ["paragraphs", "paragraph", "paragraph_text"])
    )
    for paragraph_index, paragraph in enumerate(paragraph_values):
        paragraph_text = _paragraph_text(paragraph)
        if paragraph_text:
            section_name = _paragraph_section(paragraph) or _clean_string(
                _first_value(record, ["section", "section_name", "section_title"])
            )
            paragraph_id = _paragraph_id(paragraph, default=f"{paper_id}_p{paragraph_index}")
            rows.append(
                _section_row(
                    paper_id=paper_id,
                    section_name=section_name,
                    paragraph_id=paragraph_id,
                    paragraph_text=paragraph_text,
                )
            )

    if not rows:
        text = _clean_string(_first_value(record, ["full_text", "body", "text", "abstract"]))
        if text:
            rows.extend(_sections_from_plain_text(text, paper_id))
    return rows


def _references_from_record(record: dict[str, Any], paper_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    references = _first_value(record, ["references", "reference", "bib_entries", "bibs", "refs"])
    if isinstance(references, dict):
        iterable = [
            (str(reference_key), _json_like_record(reference_value))
            for reference_key, reference_value in references.items()
        ]
    else:
        iterable = [
            (None, _json_like_record(reference))
            for reference in _coerce_sequence(references)
        ]

    for index, (reference_key, reference) in enumerate(iterable):
        key = reference_key or _clean_string(
            _first_value(reference, ["reference_key", "id", "ref_id", "bib_id", "key"])
        )
        raw_reference = _clean_string(
            _first_value(reference, ["raw_reference", "raw", "text", "reference", "bib_entry"])
        )
        cited_title = _clean_string(
            _first_value(reference, ["cited_title", "title", "paper_title"])
        )
        cited_year = _parse_year(_first_value(reference, ["cited_year", "year", "date"]))
        cited_doi = _clean_string(_first_value(reference, ["cited_doi", "doi"]))
        cited_authors = _authors_from_value(_first_value(reference, ["cited_authors", "authors"]))

        if key or raw_reference or cited_title or cited_year or cited_doi or cited_authors:
            rows.append(
                _reference_row(
                    citing_paper_id=paper_id,
                    reference_key=key or f"ref_{index}",
                    cited_title=cited_title,
                    cited_year=cited_year,
                    cited_authors=cited_authors,
                    cited_doi=cited_doi,
                    raw_reference=raw_reference,
                )
            )

    scalar_reference_title = _clean_string(
        _first_value(record, ["cited_title", "reference_title", "target_title"])
    )
    scalar_reference = _clean_string(_first_value(record, ["raw_reference", "reference_text"]))
    if not rows and (scalar_reference_title or scalar_reference):
        rows.append(
            _reference_row(
                citing_paper_id=paper_id,
                reference_key=_clean_string(_first_value(record, ["reference_key", "ref_id"]))
                or "ref_0",
                cited_title=scalar_reference_title,
                cited_year=_parse_year(_first_value(record, ["cited_year", "reference_year"])),
                cited_authors=_authors_from_value(
                    _first_value(record, ["cited_authors", "reference_authors"])
                ),
                cited_doi=_clean_string(_first_value(record, ["cited_doi", "reference_doi"])),
                raw_reference=scalar_reference,
            )
        )
    return rows


def _sections_from_plain_text(text: str, paper_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    current_section: str | None = None
    paragraph_lines: list[str] = []
    paragraph_index = 0

    def flush() -> None:
        nonlocal paragraph_index
        paragraph_text = _clean_string(" ".join(paragraph_lines))
        paragraph_lines.clear()
        if paragraph_text:
            rows.append(
                _section_row(
                    paper_id=paper_id,
                    section_name=current_section,
                    paragraph_id=f"{paper_id}_p{paragraph_index}",
                    paragraph_text=paragraph_text,
                )
            )
            paragraph_index += 1

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            flush()
            continue
        if _is_plain_section_heading(line):
            flush()
            current_section = line.rstrip(":")
            continue
        if line.lower().startswith("title:"):
            continue
        paragraph_lines.append(line)

    flush()
    if not rows and text.strip():
        rows.append(
            _section_row(
                paper_id=paper_id,
                section_name=None,
                paragraph_id=f"{paper_id}_p0",
                paragraph_text=_clean_string(text) or "",
            )
        )
    return rows


def _references_from_plain_text(text: str, paper_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    in_references = False
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.lower().rstrip(":") in {"references", "bibliography"}:
            in_references = True
            continue
        if in_references:
            cited_year = _parse_year(stripped)
            rows.append(
                _reference_row(
                    citing_paper_id=paper_id,
                    reference_key=f"ref_{len(rows)}",
                    cited_title=None,
                    cited_year=cited_year,
                    cited_authors=None,
                    cited_doi=None,
                    raw_reference=stripped,
                )
            )
    return rows


def _json_records(loaded: Any) -> list[dict[str, Any]]:
    if isinstance(loaded, list):
        return [_json_like_record(item) for item in loaded]
    if isinstance(loaded, dict):
        for key in ("papers", "documents", "records", "data", "examples", "instances"):
            value = loaded.get(key)
            if isinstance(value, list):
                return [_json_like_record(item) for item in value]
        return [loaded]
    raise ValueError("Expected JSON object or array")


def _json_like_record(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return {
            str(key): _maybe_parse_json_string(_null_if_missing(item))
            for key, item in value.items()
        }
    if isinstance(value, str):
        return {"raw_reference": value}
    return {"value": _null_if_missing(value)}


def _maybe_parse_json_string(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    stripped = value.strip()
    if not stripped or stripped[0] not in "[{":
        return value
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        return value


def _null_if_missing(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, float) and pd.isna(value):
        return None
    return value


def _first_value(record: dict[str, Any], aliases: list[str]) -> Any:
    lower_lookup = {key.lower(): value for key, value in record.items()}
    for alias in aliases:
        if alias.lower() in lower_lookup:
            return lower_lookup[alias.lower()]
    return None


def _clean_string(value: Any) -> str | None:
    value = _null_if_missing(value)
    if value is None:
        return None
    if isinstance(value, list):
        text = "; ".join(_clean_string(item) or "" for item in value)
    elif isinstance(value, dict):
        text = json.dumps(value, sort_keys=True, default=str)
    else:
        text = str(value)
    text = re.sub(r"\s+", " ", text).strip()
    return text or None


def _parse_year(value: Any) -> int | None:
    text = _clean_string(value)
    if not text:
        return None
    match = re.search(r"\b(?:19|20)\d{2}\b", text)
    return int(match.group(0)) if match else None


def _first_year(values: list[Any]) -> int | None:
    for value in values:
        year = _parse_year(value)
        if year is not None:
            return year
    return None


def _coerce_sequence(value: Any) -> list[Any]:
    value = _maybe_parse_json_string(_null_if_missing(value))
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, dict):
        return [value]
    return [value]


def _paragraph_text(value: Any) -> str | None:
    if isinstance(value, dict):
        return _clean_string(
            _first_value(value, ["paragraph_text", "text", "content", "paragraph", "body"])
        )
    return _clean_string(value)


def _paragraph_id(value: Any, *, default: str) -> str:
    if isinstance(value, dict):
        return _clean_string(_first_value(value, ["paragraph_id", "id", "pid"])) or default
    return default


def _paragraph_section(value: Any) -> str | None:
    if isinstance(value, dict):
        return _clean_string(_first_value(value, ["section", "section_name", "section_title"]))
    return None


def _authors_from_value(value: Any) -> str | None:
    value = _maybe_parse_json_string(_null_if_missing(value))
    if value is None:
        return None
    if isinstance(value, list):
        authors: list[str] = []
        for author in value:
            if isinstance(author, dict):
                name = _clean_string(_first_value(author, ["name", "full_name"]))
                if name is None:
                    parts = [
                        _clean_string(_first_value(author, ["first", "forename", "given"])),
                        _clean_string(_first_value(author, ["last", "surname", "family"])),
                    ]
                    name = " ".join(part for part in parts if part) or None
                if name:
                    authors.append(name)
            else:
                name = _clean_string(author)
                if name:
                    authors.append(name)
        return "; ".join(authors) if authors else None
    return _clean_string(value)


def _authors_from_tei_bibl(bibl: etree._Element) -> str | None:
    authors: list[str] = []
    for author in bibl.xpath(".//*[local-name()='author']"):
        surname = _first_child_text(author, "surname")
        forename = _first_child_text(author, "forename")
        name = _clean_string(" ".join(part for part in [forename, surname] if part))
        if name is None:
            name = _clean_string(" ".join(author.itertext()))
        if name:
            authors.append(name)
    return "; ".join(authors) if authors else None


def _title_from_plain_text(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.lower().startswith("title:"):
            return _clean_string(stripped.split(":", 1)[1])
        if not _is_plain_section_heading(stripped):
            return _clean_string(stripped)
    return None


def _is_plain_section_heading(line: str) -> bool:
    if len(line) > 80:
        return False
    normalized = line.lower().rstrip(":")
    known = {
        "abstract",
        "background",
        "bibliography",
        "conclusion",
        "discussion",
        "experiments",
        "introduction",
        "method",
        "methods",
        "references",
        "related work",
        "results",
    }
    return normalized in known or bool(re.fullmatch(r"\d+(?:\.\d+)*\.?\s+[A-Z][A-Za-z ]+", line))


def _first_xpath_text(element: etree._Element, expressions: list[str]) -> str | None:
    for expression in expressions:
        values = element.xpath(expression)
        for value in values:
            if isinstance(value, etree._Element):
                text = _clean_string(" ".join(value.itertext()))
            else:
                text = _clean_string(value)
            if text:
                return text
    return None


def _first_xpath_attr(element: etree._Element, expression: str, attr_name: str) -> str | None:
    values = element.xpath(expression)
    for value in values:
        if isinstance(value, etree._Element):
            attr_value = _attribute(value, attr_name)
            if attr_value:
                return attr_value
    return None


def _first_child_text(element: etree._Element, child_name: str) -> str | None:
    values = element.xpath(f"./*[local-name()='{child_name}']")
    for value in values:
        text = _clean_string(" ".join(value.itertext()))
        if text:
            return text
    return None


def _first_idno(element: etree._Element, id_types: set[str] | None = None) -> str | None:
    fallback: str | None = None
    for idno in element.xpath(".//*[local-name()='idno']"):
        id_type = (_attribute(idno, "type") or "").lower()
        text = _clean_string(" ".join(idno.itertext()))
        if not text:
            continue
        if id_types is not None:
            if id_type in id_types:
                return text
        elif id_type in {"doi", "acl", "acl_id", "anthology"}:
            return text
        fallback = fallback or text
    return fallback if id_types is None else None


def _attribute(element: etree._Element, attr_name: str) -> str | None:
    if attr_name in element.attrib:
        return _clean_string(element.attrib[attr_name])
    for key, value in element.attrib.items():
        if key.endswith(f"}}{attr_name}"):
            return _clean_string(value)
    return None


def _element_id(element: etree._Element) -> str | None:
    return _attribute(element, "id") or _attribute(element, "xml:id") or _attribute(element, "n")


def _text_content(element: etree._Element) -> str:
    return _clean_string(" ".join(element.itertext())) or ""


def _deterministic_paper_id(
    *,
    source_file: str,
    title: str | None = None,
    doi_or_acl_id: str | None = None,
    content_hint: str | None = None,
    record_index: int | None = None,
) -> str:
    payload = "\x1f".join(
        [
            source_file,
            str(record_index) if record_index is not None else "",
            doi_or_acl_id or "",
            title or "",
            content_hint or "",
        ]
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"acl_{digest}"
