from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import pyarrow.parquet as pq

from citeevidence.schemas import AttributionStatus

DEFAULT_SECTIONED_EXTRACTION_REPORT = Path(
    "reports/citation_contexts_sectioned_extraction_report.md"
)
CONTEXT_COLUMNS = [
    "context_id",
    "citing_paper_id",
    "reference_key",
    "cited_title",
    "cited_year",
    "cited_doi",
    "raw_section_name",
    "normalized_section",
    "section",
    "paragraph_id",
    "citation_marker",
    "marker_start_offset",
    "marker_end_offset",
    "marker_type",
    "sentence_text",
    "context_window_s3",
    "context_window_paragraph",
    "citation_group_size",
    "large_citation_group_flag",
    "very_large_citation_group_flag",
    "suspicious_citation_range_flag",
    "attribution_status",
]

SECTION_COLUMNS = ["paper_id", "section_name", "paragraph_id", "paragraph_text"]
NORMALIZED_SECTION_COLUMN = "normalized_section"
REFERENCE_COLUMNS = [
    "citing_paper_id",
    "reference_key",
    "cited_title",
    "cited_year",
    "cited_authors",
    "cited_doi",
    "raw_reference",
]

BRACKET_CITATION_RE = re.compile(r"\[(?:\s*\d+\s*(?:(?:[,;]\s*\d+)|(?:[-–—]\s*\d+))*\s*)\]")
AUTHOR_YEAR_CITATION_RE = re.compile(r"\((?=[^)]*(?:19|20)\d{2})[^()]{1,250}\)")
CAPITALIZED_SURNAME_RE = r"[A-Z][a-z][A-Za-z'`-]*"
PARTICLE_SURNAME_RE = (
    r"(?:de|del|da|di|le|la|von)\s+[A-Z][A-Za-z'`-]*"
    r"|(?:de\s+la|van\s+der|van|del)\s+[A-Z][A-Za-z'`-]*"
)
SURNAME_TOKEN_RE = rf"(?:{CAPITALIZED_SURNAME_RE}|{PARTICLE_SURNAME_RE})"
NARRATIVE_AUTHOR_YEAR_RE = re.compile(
    rf"(?<![A-Za-z])(?P<authors>{SURNAME_TOKEN_RE}"
    rf"(?:\s+(?:and|&)\s+{SURNAME_TOKEN_RE})?"
    r"(?:\s+et\s+al\.?)?)\s*\(\s*(?P<year>(?:19|20)\d{2}[a-z]?)\s*\)"
)
LEFT_AUTHOR_PHRASE_RE = re.compile(
    rf"(?<![A-Za-z])(?P<authors>{SURNAME_TOKEN_RE}"
    rf"(?:\s+(?:and|&)\s+{SURNAME_TOKEN_RE})?"
    r"(?:\s+et\s+al\.?)?)\s*$"
)
NARRATIVE_YEAR_PAREN_RE = re.compile(r"\(\s*(?P<year>(?:19|20)\d{2}[a-z]?)\s*\)")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\[])")
YEAR_RE = re.compile(r"\b(?:19|20)\d{2}[a-z]?\b")
NON_AUTHOR_SINGLETONS = {
    "appendix",
    "chapter",
    "equation",
    "example",
    "experiment",
    "figure",
    "model",
    "section",
    "system",
    "table",
    "year",
}


@dataclass(frozen=True)
class SentenceSpan:
    text: str
    start: int
    end: int


@dataclass(frozen=True)
class CitationMarker:
    marker: str
    start: int
    end: int
    reference_keys: list[str]
    is_range: bool
    unresolved_entries: list[str]
    marker_type: str


def extract_citation_contexts(
    *,
    sections_path: str | Path,
    out_path: str | Path,
    references_path: str | Path | None = None,
    max_window_chars: int = 2000,
    use_bibliography: bool = False,
) -> pd.DataFrame:
    """Extract bounded citation-context windows from parsed ACL-OCL sections.

    ACL-OCL extraction is pre-resolution by default: citation markers are grounded
    in local text, but cited-paper metadata stays empty until a later resolver has
    an authoritative bibliography or aligned citation graph.
    """
    if max_window_chars < 100:
        raise ValueError("max_window_chars must be at least 100")

    sections = _read_sections(sections_path)
    paper_ids = set(sections["paper_id"].dropna().astype(str))
    if use_bibliography:
        if references_path is None:
            raise ValueError("references_path is required when use_bibliography=True")
        references = _load_references(references_path, paper_ids)
    else:
        references = pd.DataFrame(columns=REFERENCE_COLUMNS)
    reference_index = _build_reference_index(references)

    rows: list[dict[str, Any]] = []
    for section in sections.itertuples(index=False):
        rows.extend(
            _extract_from_section(
                paper_id=str(section.paper_id),
                raw_section_name=_none_if_missing(section.section_name),
                normalized_section=_normalized_section_label(section),
                paragraph_id=str(section.paragraph_id),
                paragraph_text=_clean_text(section.paragraph_text),
                references=reference_index.get(str(section.paper_id), {}),
                max_window_chars=max_window_chars,
                use_bibliography=use_bibliography,
            )
        )

    contexts = pd.DataFrame(rows, columns=CONTEXT_COLUMNS)
    output = Path(out_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    contexts.to_parquet(output, index=False)
    return contexts


def write_context_extraction_report(
    *,
    contexts: pd.DataFrame,
    sections_path: str | Path,
    out_path: str | Path,
    report_path: str | Path,
    max_window_chars: int,
) -> dict[str, Any]:
    """Write a markdown report for extracted citation contexts."""
    metrics = {
        "context_rows": int(len(contexts)),
        "unique_context_id": int(contexts["context_id"].nunique(dropna=True)),
        "duplicate_context_id": int(
            len(contexts) - contexts["context_id"].nunique(dropna=True)
        ),
        "sentence_text_in_context_window_s3_rate": _substring_rate(
            contexts,
            needle="sentence_text",
            haystack="context_window_s3",
        ),
        "sentence_text_in_context_window_paragraph_rate": _substring_rate(
            contexts,
            needle="sentence_text",
            haystack="context_window_paragraph",
        ),
        "citation_marker_in_sentence_text_rate": _substring_rate(
            contexts,
            needle="citation_marker",
            haystack="sentence_text",
        ),
        "raw_section_name_non_empty_rate": _non_empty_rate(contexts, "raw_section_name"),
        "marker_type_distribution": _value_distribution(contexts, "marker_type"),
        "attribution_status_distribution": _value_distribution(
            contexts,
            "attribution_status",
        ),
        "normalized_section_distribution": _value_distribution(
            contexts,
            "normalized_section",
        ),
        "citation_group_size_distribution": _value_distribution(
            contexts,
            "citation_group_size",
        ),
        "large_citation_group_count": _flag_count(contexts, "large_citation_group_flag"),
        "very_large_citation_group_count": _flag_count(
            contexts,
            "very_large_citation_group_flag",
        ),
        "suspicious_citation_range_count": _flag_count(
            contexts,
            "suspicious_citation_range_flag",
        ),
        "large_citation_group_examples": _large_citation_group_examples(contexts, 20),
        "samples": _sample_context_rows(contexts, 20),
    }
    report = _build_extraction_report(
        metrics=metrics,
        sections_path=Path(sections_path),
        out_path=Path(out_path),
        max_window_chars=max_window_chars,
    )
    output = Path(report_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    return metrics


def _read_sections(sections_path: str | Path) -> pd.DataFrame:
    path = Path(sections_path)
    available = set(pq.ParquetFile(path).schema_arrow.names)
    missing = [column for column in SECTION_COLUMNS if column not in available]
    if missing:
        raise ValueError(
            "Sections parquet is missing required columns: " + ", ".join(missing)
        )
    columns = [*SECTION_COLUMNS]
    if NORMALIZED_SECTION_COLUMN in available:
        columns.append(NORMALIZED_SECTION_COLUMN)
    return pd.read_parquet(path, columns=columns)


def _normalized_section_label(section: Any) -> str | None:
    return _none_if_missing(getattr(section, NORMALIZED_SECTION_COLUMN, None))


def _load_references(references_path: str | Path, paper_ids: set[str]) -> pd.DataFrame:
    references = pd.read_parquet(references_path, columns=REFERENCE_COLUMNS)
    if references.empty:
        return references
    references = references.copy()
    references["citing_paper_id"] = references["citing_paper_id"].astype(str)
    return references.loc[references["citing_paper_id"].isin(paper_ids)]


def _build_reference_index(references: pd.DataFrame) -> dict[str, dict[str, dict[str, Any]]]:
    index: dict[str, dict[str, dict[str, Any]]] = {}
    for row in references.to_dict(orient="records"):
        citing_paper_id = str(row["citing_paper_id"])
        reference_key = str(row["reference_key"])
        index.setdefault(citing_paper_id, {})[reference_key] = row
    return index


def _extract_from_section(
    *,
    paper_id: str,
    raw_section_name: str | None,
    normalized_section: str | None,
    paragraph_id: str,
    paragraph_text: str,
    references: dict[str, dict[str, Any]],
    max_window_chars: int,
    use_bibliography: bool,
) -> list[dict[str, Any]]:
    sentences = _split_sentences(paragraph_text)
    rows: list[dict[str, Any]] = []
    for sentence_index, sentence in enumerate(sentences):
        occurrence_counts: dict[str, int] = {}
        markers = _find_citation_markers(
            sentence.text,
            sentence.start,
            references,
            use_bibliography=use_bibliography,
        )
        for marker in markers:
            occurrence_index = occurrence_counts.get(marker.marker, 0)
            occurrence_counts[marker.marker] = occurrence_index + 1
            status = _attribution_status(
                marker,
                references,
                use_bibliography=use_bibliography,
            )
            citation_group_size = len(marker.reference_keys)
            large_group_flag = citation_group_size > 20
            very_large_group_flag = citation_group_size > 50
            suspicious_range_flag = marker.is_range and citation_group_size > 20
            for component_index, reference_key in enumerate(marker.reference_keys):
                reference = references.get(reference_key)
                marker_start_in_sentence = marker.start - sentence.start
                marker_end_in_sentence = marker.end - sentence.start
                sentence_text = _bounded_text(
                    sentence.text,
                    center_start=marker_start_in_sentence,
                    center_end=marker_end_in_sentence,
                    max_chars=max_window_chars,
                )
                row = {
                    "context_id": _context_id(
                        paper_id=paper_id,
                        paragraph_id=paragraph_id,
                        sentence_index=sentence_index,
                        reference_key=reference_key,
                        marker=marker.marker,
                        marker_start=marker_start_in_sentence,
                        marker_end=marker_end_in_sentence,
                        marker_type=marker.marker_type,
                        component_index=component_index,
                        occurrence_index=occurrence_index,
                        sentence_text=sentence.text,
                    ),
                    "citing_paper_id": paper_id,
                    "reference_key": reference_key,
                    "cited_title": _reference_value(reference, "cited_title"),
                    "cited_year": _reference_year(reference),
                    "cited_doi": _reference_value(reference, "cited_doi"),
                    "raw_section_name": raw_section_name,
                    "normalized_section": normalized_section,
                    "section": normalized_section or raw_section_name,
                    "paragraph_id": paragraph_id,
                    "citation_marker": marker.marker,
                    "marker_start_offset": marker_start_in_sentence,
                    "marker_end_offset": marker_end_in_sentence,
                    "marker_type": marker.marker_type,
                    "sentence_text": sentence_text,
                    "context_window_s3": _sentence_window(
                        sentences,
                        sentence_index,
                        marker_start=marker.start,
                        marker_end=marker.end,
                        max_window_chars=max_window_chars,
                    ),
                    "context_window_paragraph": _bounded_text(
                        paragraph_text,
                        center_start=marker.start,
                        center_end=marker.end,
                        max_chars=max_window_chars,
                    ),
                    "citation_group_size": citation_group_size,
                    "large_citation_group_flag": large_group_flag,
                    "very_large_citation_group_flag": very_large_group_flag,
                    "suspicious_citation_range_flag": suspicious_range_flag,
                    "attribution_status": status.value,
                }
                rows.append(row)
    return rows


def _find_citation_markers(
    sentence_text: str,
    sentence_start: int,
    references: dict[str, dict[str, Any]],
    *,
    use_bibliography: bool,
) -> list[CitationMarker]:
    markers: list[CitationMarker] = []
    occupied: list[tuple[int, int]] = []

    if "(" in sentence_text and YEAR_RE.search(sentence_text):
        narrative_markers = _find_narrative_author_year_markers(
            sentence_text,
            sentence_start,
            references,
            use_bibliography=use_bibliography,
        )
        markers.extend(narrative_markers)
        occupied.extend(
            (marker.start - sentence_start, marker.end - sentence_start)
            for marker in narrative_markers
        )

    if "[" in sentence_text:
        for match in BRACKET_CITATION_RE.finditer(sentence_text):
            if _overlaps(match.start(), match.end(), occupied):
                continue
            marker = match.group(0)
            reference_keys, is_range = _parse_bracket_marker(marker)
            if not use_bibliography:
                reference_keys = _pre_resolution_reference_keys(marker, reference_keys)
            markers.append(
                CitationMarker(
                    marker=marker,
                    start=sentence_start + match.start(),
                    end=sentence_start + match.end(),
                    reference_keys=reference_keys,
                    is_range=is_range,
                    unresolved_entries=[],
                    marker_type="numeric",
                )
            )
            occupied.append((match.start(), match.end()))

    if "(" in sentence_text and YEAR_RE.search(sentence_text):
        for match in AUTHOR_YEAR_CITATION_RE.finditer(sentence_text):
            if _overlaps(match.start(), match.end(), occupied):
                continue
            marker = match.group(0)
            entries = _author_year_entries(marker)
            reference_keys, unresolved_entries = _reference_keys_for_author_year_entries(
                entries,
                references,
                use_bibliography=use_bibliography,
            )
            if reference_keys:
                markers.append(
                    CitationMarker(
                        marker=marker,
                        start=sentence_start + match.start(),
                        end=sentence_start + match.end(),
                        reference_keys=reference_keys,
                        is_range=False,
                        unresolved_entries=unresolved_entries,
                        marker_type=_parenthetical_marker_type(entries),
                    )
                )

    return sorted(markers, key=lambda marker: marker.start)


def _find_narrative_author_year_markers(
    sentence_text: str,
    sentence_start: int,
    references: dict[str, dict[str, Any]],
    *,
    use_bibliography: bool,
) -> list[CitationMarker]:
    markers: list[CitationMarker] = []
    for year_match in NARRATIVE_YEAR_PAREN_RE.finditer(sentence_text):
        left_start = max(0, year_match.start() - 120)
        left_context = sentence_text[left_start : year_match.start()]
        author_match = LEFT_AUTHOR_PHRASE_RE.search(left_context)
        if author_match is None:
            continue
        authors = author_match.group("authors").strip()
        if not _is_plausible_narrative_author_phrase(authors):
            continue
        marker_start = left_start + author_match.start("authors")
        marker_end = year_match.end()
        marker = sentence_text[marker_start:marker_end]
        entries = _author_year_entries(marker)
        reference_keys, unresolved_entries = _reference_keys_for_author_year_entries(
            entries,
            references,
            use_bibliography=use_bibliography,
        )
        if reference_keys:
            markers.append(
                CitationMarker(
                    marker=marker,
                    start=sentence_start + marker_start,
                    end=sentence_start + marker_end,
                    reference_keys=reference_keys,
                    is_range=False,
                    unresolved_entries=unresolved_entries,
                    marker_type="narrative_author_year",
                )
            )
    return markers


def _is_plausible_narrative_author_phrase(authors: str) -> bool:
    normalized = authors.lower().strip()
    if " and " in normalized or " & " in normalized or "et al" in normalized:
        return True
    return normalized not in NON_AUTHOR_SINGLETONS


def _parse_bracket_marker(marker: str) -> tuple[list[str], bool]:
    body = marker.strip()[1:-1]
    body = body.replace("–", "-").replace("—", "-")
    is_range = False
    keys: list[str] = []
    for part in re.split(r"[,;]", body):
        part = part.strip()
        if not part:
            continue
        range_match = re.fullmatch(r"(\d+)\s*-\s*(\d+)", part)
        if range_match:
            start = int(range_match.group(1))
            end = int(range_match.group(2))
            if start <= end and end - start <= 100:
                keys.extend(str(value) for value in range(start, end + 1))
                is_range = True
            else:
                keys.append(part)
            continue
        keys.append(str(int(part)) if part.isdigit() else part)
    return list(dict.fromkeys(keys)), is_range


def _author_year_entries(marker: str) -> list[str]:
    narrative_match = NARRATIVE_AUTHOR_YEAR_RE.fullmatch(marker.strip())
    if narrative_match is not None:
        return [f"{narrative_match.group('authors')}, {narrative_match.group('year')}"]
    body = marker.strip()[1:-1]
    entries = [entry.strip() for entry in body.split(";")]
    return [entry for entry in entries if YEAR_RE.search(entry)]


def _reference_keys_for_author_year_entries(
    entries: list[str],
    references: dict[str, dict[str, Any]],
    *,
    use_bibliography: bool,
) -> tuple[list[str], list[str]]:
    reference_keys: list[str] = []
    unresolved_entries: list[str] = []
    for entry in entries:
        if use_bibliography:
            reference_key = _match_author_year_reference(entry, references)
            if reference_key is None:
                reference_key = _unresolved_reference_key(entry)
                unresolved_entries.append(entry)
        else:
            reference_key = _unresolved_reference_key(entry)
            unresolved_entries.append(entry)
        reference_keys.append(reference_key)
    return reference_keys, unresolved_entries


def _parenthetical_marker_type(entries: list[str]) -> str:
    if entries and all(_is_year_only_entry(entry) for entry in entries):
        return "year_only"
    return "parenthetical_author_year"


def _is_year_only_entry(entry: str) -> bool:
    return bool(re.fullmatch(r"\s*(?:19|20)\d{2}[a-z]?\s*", entry))


def _match_author_year_reference(
    entry: str,
    references: dict[str, dict[str, Any]],
) -> str | None:
    year_match = YEAR_RE.search(entry)
    if year_match is None:
        return None
    year = year_match.group(0)[:4]
    surname = _surname_from_author_year_entry(entry)
    candidates: list[str] = []
    for reference_key, reference in references.items():
        reference_year = _reference_year(reference)
        if reference_year is None or str(reference_year) != year:
            continue
        if surname is None or surname in _reference_search_text(reference):
            candidates.append(reference_key)
    if len(candidates) == 1:
        return candidates[0]
    return None


def _surname_from_author_year_entry(entry: str) -> str | None:
    year_match = YEAR_RE.search(entry)
    before_year = entry[: year_match.start()] if year_match else entry
    match = re.search(r"([A-Z][A-Za-z'`-]+)", before_year)
    return match.group(1).lower() if match else None


def _reference_search_text(reference: dict[str, Any]) -> str:
    values = [
        reference.get("cited_authors"),
        reference.get("raw_reference"),
        reference.get("cited_title"),
    ]
    return " ".join(str(value).lower() for value in values if not pd.isna(value))


def _attribution_status(
    marker: CitationMarker,
    references: dict[str, dict[str, Any]],
    *,
    use_bibliography: bool,
) -> AttributionStatus:
    if marker.is_range:
        return AttributionStatus.CITATION_RANGE
    if len(marker.reference_keys) > 1:
        return AttributionStatus.MULTI_CITATION_GROUP
    if not use_bibliography:
        if marker.marker_type == "numeric":
            return AttributionStatus.NUMERIC_UNRESOLVED_PRE_RESOLUTION
        return AttributionStatus.AUTHOR_YEAR_UNRESOLVED_PRE_RESOLUTION
    if marker.unresolved_entries:
        return AttributionStatus.BIBLIOGRAPHY_UNRESOLVED
    if marker.reference_keys and marker.reference_keys[0] not in references:
        return AttributionStatus.BIBLIOGRAPHY_UNRESOLVED
    return AttributionStatus.SINGLE_CITATION_CLEAR


def _split_sentences(paragraph_text: str) -> list[SentenceSpan]:
    normalized = re.sub(r"\s+", " ", paragraph_text).strip()
    if not normalized:
        return []

    spans: list[SentenceSpan] = []
    start = 0
    for match in SENTENCE_SPLIT_RE.finditer(normalized):
        end = match.start()
        text = normalized[start:end].strip()
        if text:
            leading = len(normalized[start:end]) - len(normalized[start:end].lstrip())
            spans.append(SentenceSpan(text=text, start=start + leading, end=end))
        start = match.end()
    text = normalized[start:].strip()
    if text:
        leading = len(normalized[start:]) - len(normalized[start:].lstrip())
        spans.append(SentenceSpan(text=text, start=start + leading, end=len(normalized)))
    return spans


def _sentence_window(
    sentences: list[SentenceSpan],
    sentence_index: int,
    *,
    marker_start: int,
    marker_end: int,
    max_window_chars: int,
) -> str:
    start_index = max(0, sentence_index - 1)
    end_index = min(len(sentences), sentence_index + 2)
    selected = sentences[start_index:end_index]
    window_text = " ".join(sentence.text for sentence in selected)
    first_start = selected[0].start
    return _bounded_text(
        window_text,
        center_start=max(0, marker_start - first_start),
        center_end=max(0, marker_end - first_start),
        max_chars=max_window_chars,
    )


def _bounded_text(
    text: str,
    *,
    center_start: int,
    center_end: int,
    max_chars: int,
) -> str:
    text = _clean_text(text)
    if len(text) <= max_chars:
        return text

    center = max(0, min(len(text), (center_start + center_end) // 2))
    half = max_chars // 2
    start = max(0, center - half)
    end = min(len(text), start + max_chars)
    start = max(0, end - max_chars)
    return text[start:end].strip()


def _context_id(
    *,
    paper_id: str,
    paragraph_id: str,
    sentence_index: int,
    reference_key: str,
    marker: str,
    marker_start: int,
    marker_end: int,
    marker_type: str,
    component_index: int,
    occurrence_index: int,
    sentence_text: str,
) -> str:
    payload = "\x1f".join(
        [
            paper_id,
            paragraph_id,
            str(sentence_index),
            reference_key,
            marker,
            str(marker_start),
            str(marker_end),
            marker_type,
            str(component_index),
            str(occurrence_index),
            " ".join(sentence_text.split()),
        ]
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:20]
    return f"ctx_{digest}"


def _reference_value(reference: dict[str, Any] | None, key: str) -> Any:
    if reference is None:
        return None
    value = reference.get(key)
    return None if value is None or pd.isna(value) else value


def _reference_year(reference: dict[str, Any] | None) -> int | None:
    value = _reference_value(reference, "cited_year")
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        match = YEAR_RE.search(str(value))
        return int(match.group(0)[:4]) if match else None


def _unresolved_reference_key(entry: str) -> str:
    digest = hashlib.sha256(entry.encode("utf-8")).hexdigest()[:12]
    return f"unresolved_{digest}"


def _pre_resolution_reference_keys(marker: str, components: list[str]) -> list[str]:
    keys = []
    for index, component in enumerate(components):
        payload = f"{marker}\x1f{index}\x1f{component}"
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]
        keys.append(f"marker_component_{index}_{digest}")
    return keys


def _build_extraction_report(
    *,
    metrics: dict[str, Any],
    sections_path: Path,
    out_path: Path,
    max_window_chars: int,
) -> str:
    return "\n".join(
        [
            "# Citation Contexts Sectioned Extraction Report",
            "",
            "## Inputs / Outputs",
            _table(
                [
                    {"name": "sections", "path": sections_path},
                    {"name": "citation_contexts_sectioned", "path": out_path},
                ]
            ),
            "",
            f"- Max context window chars: {max_window_chars}",
            "- Extraction mode: pre-resolution / no bibliography",
            "",
            "## Core Metrics",
            _table(
                [
                    {"metric": "context rows", "value": metrics["context_rows"]},
                    {"metric": "unique context_id", "value": metrics["unique_context_id"]},
                    {
                        "metric": "duplicate context_id",
                        "value": metrics["duplicate_context_id"],
                    },
                    {
                        "metric": "sentence_text in context_window_s3 rate",
                        "value": metrics["sentence_text_in_context_window_s3_rate"],
                    },
                    {
                        "metric": "sentence_text in context_window_paragraph rate",
                        "value": metrics[
                            "sentence_text_in_context_window_paragraph_rate"
                        ],
                    },
                    {
                        "metric": "citation_marker in sentence_text rate",
                        "value": metrics["citation_marker_in_sentence_text_rate"],
                    },
                    {
                        "metric": "raw_section_name non-empty rate",
                        "value": metrics["raw_section_name_non_empty_rate"],
                    },
                    {
                        "metric": "large citation group count",
                        "value": metrics["large_citation_group_count"],
                    },
                    {
                        "metric": "very large citation group count",
                        "value": metrics["very_large_citation_group_count"],
                    },
                    {
                        "metric": "suspicious citation range count",
                        "value": metrics["suspicious_citation_range_count"],
                    },
                ]
            ),
            "",
            "## Marker Type Distribution",
            _table(metrics["marker_type_distribution"]),
            "",
            "## Attribution Status Distribution",
            _table(metrics["attribution_status_distribution"]),
            "",
            "## Normalized Section Distribution",
            _table(metrics["normalized_section_distribution"]),
            "",
            "## Citation Group Size Distribution",
            _table(metrics["citation_group_size_distribution"]),
            "",
            "## Large Citation Group Examples",
            _table(metrics["large_citation_group_examples"]),
            "",
            "## Sample Rows",
            _table(metrics["samples"]),
            "",
        ]
    )


def _substring_rate(frame: pd.DataFrame, *, needle: str, haystack: str) -> str:
    if frame.empty:
        return "0.000"
    contained = 0
    for row in frame[[needle, haystack]].itertuples(index=False):
        needle_text = _clean_text(getattr(row, needle))
        haystack_text = _clean_text(getattr(row, haystack))
        if needle_text and needle_text in haystack_text:
            contained += 1
    return _rate(contained, len(frame))


def _non_empty_rate(frame: pd.DataFrame, column: str) -> str:
    if frame.empty or column not in frame:
        return "0.000"
    return _rate(int(frame[column].map(_none_if_missing).notna().sum()), len(frame))


def _flag_count(frame: pd.DataFrame, column: str) -> int:
    if frame.empty or column not in frame:
        return 0
    return int(frame[column].fillna(False).astype(bool).sum())


def _value_distribution(frame: pd.DataFrame, column: str) -> list[dict[str, Any]]:
    if frame.empty or column not in frame:
        return []
    counts = (
        frame[column]
        .fillna("unavailable")
        .astype(str)
        .value_counts(dropna=False)
        .rename_axis(column)
        .reset_index(name="rows")
    )
    return _records(counts)


def _large_citation_group_examples(frame: pd.DataFrame, limit: int) -> list[dict[str, Any]]:
    if frame.empty or "large_citation_group_flag" not in frame:
        return []
    large = frame.loc[frame["large_citation_group_flag"].fillna(False).astype(bool)].copy()
    if large.empty:
        return []
    columns = [
        "context_id",
        "citing_paper_id",
        "raw_section_name",
        "normalized_section",
        "citation_marker",
        "marker_type",
        "attribution_status",
        "citation_group_size",
        "large_citation_group_flag",
        "very_large_citation_group_flag",
        "suspicious_citation_range_flag",
        "sentence_text",
    ]
    sample = (
        large.sort_values("citation_group_size", ascending=False)
        .drop_duplicates(subset=["citing_paper_id", "paragraph_id", "citation_marker"])
        .head(limit)[columns]
        .copy()
    )
    for column in ("citation_marker", "sentence_text"):
        sample[column] = sample[column].map(lambda value: _truncate(value, 180))
    return _records(sample)


def _sample_context_rows(frame: pd.DataFrame, limit: int) -> list[dict[str, Any]]:
    if frame.empty:
        return []
    columns = [
        "context_id",
        "citing_paper_id",
        "raw_section_name",
        "normalized_section",
        "paragraph_id",
        "citation_marker",
        "marker_type",
        "attribution_status",
        "citation_group_size",
        "sentence_text",
        "context_window_s3",
    ]
    sample = frame[columns].head(limit).copy()
    for column in ("sentence_text", "context_window_s3"):
        sample[column] = sample[column].map(lambda value: _truncate(value, 180))
    return _records(sample)


def _records(frame: pd.DataFrame) -> list[dict[str, Any]]:
    if frame.empty:
        return []
    clean = frame.where(pd.notna(frame), None)
    return clean.to_dict(orient="records")


def _rate(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.000"
    return f"{numerator / denominator:.3f}"


def _truncate(value: Any, max_chars: int) -> str:
    text = _clean_text(value)
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
    return _truncate(value, 160).replace("|", "\\|")


def _overlaps(start: int, end: int, occupied: list[tuple[int, int]]) -> bool:
    return any(
        start < occupied_end and end > occupied_start
        for occupied_start, occupied_end in occupied
    )


def _none_if_missing(value: Any) -> str | None:
    if value is None or pd.isna(value):
        return None
    text = str(value).strip()
    return text or None


def _clean_text(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()
