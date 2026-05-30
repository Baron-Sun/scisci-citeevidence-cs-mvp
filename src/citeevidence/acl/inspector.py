from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd
import pyarrow.parquet as pq
from lxml import etree

DEFAULT_INVENTORY_PATH = Path("data/interim/acl_ocl_file_inventory.parquet")
COMMON_XML_TAGS = ["TEI", "text", "body", "div", "p", "ref", "biblStruct"]
INVENTORY_COLUMNS = [
    "relative_path",
    "file_name",
    "extension",
    "size_bytes",
    "likely_format",
    "is_metadata_file",
    "root_tag",
    "xml_common_tags",
    "json_top_level_keys",
    "parquet_columns",
    "csv_columns",
    "contains_title",
    "contains_year",
    "contains_sections",
    "contains_paragraphs",
    "contains_references",
    "contains_inline_citations",
    "inspection_error",
]

TITLE_KEYS = {"title", "paper_title", "document_title"}
YEAR_KEYS = {"year", "publication_year", "pub_year", "date"}
SECTION_KEYS = {"section", "sections", "section_title", "headings", "heading"}
PARAGRAPH_KEYS = {"paragraph", "paragraphs", "paragraph_id", "p"}
REFERENCE_KEYS = {"reference", "references", "bibliography", "bibl", "bib_entries", "refs"}
CITATION_KEYS = {
    "citation",
    "citations",
    "citation_marker",
    "cite",
    "cite_spans",
    "inline_citations",
}
TEXT_EXTENSIONS = {".txt", ".text", ".md"}
XML_EXTENSIONS = {".xml", ".tei"}
JSON_EXTENSIONS = {".json", ".jsonl", ".ndjson"}
CSV_EXTENSIONS = {".csv", ".tsv"}
PARQUET_EXTENSIONS = {".parquet"}
METADATA_NAME_CUES = {
    "license",
    "manifest",
    "meta",
    "metadata",
    "readme",
    "schema",
}


def inspect_acl_ocl_data(
    input_dir: str | Path,
    *,
    out_report: str | Path,
    inventory_path: str | Path = DEFAULT_INVENTORY_PATH,
    sample_size: int = 10,
) -> pd.DataFrame:
    """Inspect an ACL-OCL-style raw data directory and write inventory artifacts."""
    root = Path(input_dir)
    if not root.exists():
        raise FileNotFoundError(f"ACL-OCL input path does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"ACL-OCL input path must be a directory: {root}")

    rows = [_inspect_file(path, root) for path in sorted(root.rglob("*")) if path.is_file()]
    inventory = pd.DataFrame(rows, columns=INVENTORY_COLUMNS)

    inventory_output = Path(inventory_path)
    inventory_output.parent.mkdir(parents=True, exist_ok=True)
    inventory.to_parquet(inventory_output, index=False)

    report_output = Path(out_report)
    report_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.write_text(
        build_acl_ocl_inspection_report(
            inventory,
            input_dir=root,
            inventory_path=inventory_output,
            sample_size=sample_size,
        ),
        encoding="utf-8",
    )
    return inventory


def build_acl_ocl_inspection_report(
    inventory: pd.DataFrame,
    *,
    input_dir: Path,
    inventory_path: Path,
    sample_size: int = 10,
) -> str:
    """Build a markdown report from the file inventory dataframe."""
    total_files = len(inventory)
    total_bytes = int(inventory["size_bytes"].sum()) if total_files else 0

    sections = [
        "# ACL-OCL Data Inspection",
        "",
        f"- Input directory: `{input_dir}`",
        f"- Inventory parquet: `{inventory_path}`",
        f"- Total files: {total_files}",
        f"- Total bytes: {total_bytes}",
        "",
        "## Files by Extension",
        _table(_value_counts(inventory, ["extension"], "files")),
        "",
        "## Likely Formats",
        _table(_value_counts(inventory, ["likely_format"], "files")),
        "",
        "## Metadata Files",
        _metadata_summary(inventory),
        "",
        "## Sample File Paths",
        _sample_paths(inventory, sample_size),
        "",
        "## XML Inspection",
        "### Root Tags",
        _table(_value_counts(inventory, ["root_tag"], "files")),
        "",
        "### Common XML Tags",
        _counter_table(_split_counter(inventory["xml_common_tags"]), "tag", "files"),
        "",
        "## JSON / JSONL Inspection",
        "### Top-Level Keys",
        _counter_table(_split_counter(inventory["json_top_level_keys"]), "key", "files"),
        "",
        "## Parquet Inspection",
        "### Columns",
        _counter_table(_split_counter(inventory["parquet_columns"]), "column", "files"),
        "",
        "## Content Signals",
        _content_signal_table(inventory),
        "",
    ]
    return "\n".join(sections)


def _inspect_file(path: Path, root: Path) -> dict[str, Any]:
    extension = _normalized_extension(path)
    row: dict[str, Any] = {
        "relative_path": path.relative_to(root).as_posix(),
        "file_name": path.name,
        "extension": extension,
        "size_bytes": path.stat().st_size,
        "likely_format": "unknown",
        "is_metadata_file": _is_metadata_file(path),
        "root_tag": None,
        "xml_common_tags": None,
        "json_top_level_keys": None,
        "parquet_columns": None,
        "csv_columns": None,
        "contains_title": False,
        "contains_year": False,
        "contains_sections": False,
        "contains_paragraphs": False,
        "contains_references": False,
        "contains_inline_citations": False,
        "inspection_error": None,
    }

    try:
        if extension in XML_EXTENSIONS:
            _inspect_xml(path, row)
        elif extension in {".jsonl", ".ndjson"}:
            _inspect_jsonl(path, row)
        elif extension == ".json":
            _inspect_json(path, row)
        elif extension in PARQUET_EXTENSIONS:
            _inspect_parquet(path, row)
        elif extension in CSV_EXTENSIONS:
            _inspect_csv(path, row)
        elif extension in TEXT_EXTENSIONS:
            _inspect_plain_text(path, row)
        elif row["is_metadata_file"]:
            row["likely_format"] = "metadata file"
            _inspect_plain_text(path, row)
        else:
            _inspect_unknown(path, row)
    except (OSError, UnicodeDecodeError, ValueError, etree.XMLSyntaxError) as exc:
        row["inspection_error"] = f"{type(exc).__name__}: {exc}"

    if row["is_metadata_file"] and row["likely_format"] == "unknown":
        row["likely_format"] = "metadata file"

    return row


def _inspect_xml(path: Path, row: dict[str, Any]) -> None:
    root_tag: str | None = None
    tag_names: set[str] = set()
    title_seen = False
    year_seen = False
    parser = etree.iterparse(str(path), events=("start",), recover=True)

    for _, element in parser:
        tag_name = _local_name(element.tag)
        if root_tag is None:
            root_tag = tag_name
        tag_names.add(tag_name)
        if tag_name in {"title", "titleStmt"}:
            title_seen = True
        if tag_name in {"date"}:
            year_seen = True
        element.clear()

    row["root_tag"] = root_tag
    row["xml_common_tags"] = _join_values(tag for tag in COMMON_XML_TAGS if tag in tag_names)
    if root_tag == "TEI" and ("biblStruct" in tag_names or _file_contains(path, "grobid")):
        row["likely_format"] = "GROBID XML"
    elif root_tag == "TEI":
        row["likely_format"] = "TEI XML"
    else:
        row["likely_format"] = "XML"

    text_sample = _read_text_sample(path)
    row["contains_title"] = title_seen or _contains_any(tag_names, TITLE_KEYS)
    row["contains_year"] = year_seen or _has_year(text_sample)
    row["contains_sections"] = _contains_any(tag_names, {"div", "head", "body"})
    row["contains_paragraphs"] = "p" in tag_names
    row["contains_references"] = _contains_any(tag_names, {"ref", "biblStruct", "listBibl", "bibl"})
    row["contains_inline_citations"] = "ref" in tag_names or _has_inline_citation(text_sample)


def _inspect_json(path: Path, row: dict[str, Any]) -> None:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    keys = _json_top_level_keys(loaded)
    row["likely_format"] = "JSON"
    row["json_top_level_keys"] = _join_values(keys)
    _apply_key_signals(row, keys)
    json_sample = path.read_text(encoding="utf-8")[:4096]
    row["contains_year"] = row["contains_year"] or _has_year(json_sample)


def _inspect_jsonl(path: Path, row: dict[str, Any]) -> None:
    keys: set[str] = set()
    sample_text_parts: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines()[:50]:
        if not line.strip():
            continue
        loaded = json.loads(line)
        if not isinstance(loaded, dict):
            raise ValueError(f"Expected JSON object per JSONL row in {path}")
        keys.update(loaded.keys())
        sample_text_parts.append(line)

    row["likely_format"] = "JSONL"
    row["json_top_level_keys"] = _join_values(keys)
    _apply_key_signals(row, keys)
    sample_text = "\n".join(sample_text_parts)
    row["contains_year"] = row["contains_year"] or _has_year(sample_text)
    row["contains_inline_citations"] = row["contains_inline_citations"] or _has_inline_citation(
        sample_text
    )


def _inspect_parquet(path: Path, row: dict[str, Any]) -> None:
    columns = list(pq.read_schema(path).names)
    row["likely_format"] = "Parquet"
    row["parquet_columns"] = _join_values(columns)
    _apply_key_signals(row, set(columns))


def _inspect_csv(path: Path, row: dict[str, Any]) -> None:
    separator = "\t" if path.suffix.lower() == ".tsv" else ","
    frame = pd.read_csv(path, nrows=5, sep=separator)
    columns = list(frame.columns)
    row["likely_format"] = "CSV"
    row["csv_columns"] = _join_values(columns)
    _apply_key_signals(row, set(columns))
    sample_text = frame.to_csv(index=False)
    row["contains_year"] = row["contains_year"] or _has_year(sample_text)
    row["contains_inline_citations"] = row["contains_inline_citations"] or _has_inline_citation(
        sample_text
    )


def _inspect_plain_text(path: Path, row: dict[str, Any]) -> None:
    text = _read_text_sample(path)
    if row["likely_format"] == "unknown":
        row["likely_format"] = "plain text"
    _apply_text_signals(row, text)


def _inspect_unknown(path: Path, row: dict[str, Any]) -> None:
    text = _read_text_sample(path)
    if text:
        _apply_text_signals(row, text)


def _apply_key_signals(row: dict[str, Any], keys: set[str]) -> None:
    normalized = {_normalize_key(key) for key in keys}
    row["contains_title"] = row["contains_title"] or bool(normalized & TITLE_KEYS)
    row["contains_year"] = row["contains_year"] or bool(normalized & YEAR_KEYS)
    row["contains_sections"] = row["contains_sections"] or bool(normalized & SECTION_KEYS)
    row["contains_paragraphs"] = row["contains_paragraphs"] or bool(normalized & PARAGRAPH_KEYS)
    row["contains_references"] = row["contains_references"] or bool(normalized & REFERENCE_KEYS)
    row["contains_inline_citations"] = row["contains_inline_citations"] or bool(
        normalized & CITATION_KEYS
    )


def _apply_text_signals(row: dict[str, Any], text: str) -> None:
    lowered = text.lower()
    row["contains_title"] = row["contains_title"] or "title" in lowered
    row["contains_year"] = row["contains_year"] or _has_year(text)
    row["contains_sections"] = row["contains_sections"] or bool(
        re.search(r"\b(introduction|methods?|results?|discussion|conclusion)\b", lowered)
    )
    row["contains_paragraphs"] = row["contains_paragraphs"] or "\n\n" in text
    row["contains_references"] = row["contains_references"] or bool(
        re.search(r"\b(references|bibliography)\b", lowered)
    )
    row["contains_inline_citations"] = row["contains_inline_citations"] or _has_inline_citation(
        text
    )


def _json_top_level_keys(loaded: Any) -> set[str]:
    if isinstance(loaded, dict):
        return set(loaded.keys())
    if isinstance(loaded, list):
        keys: set[str] = set()
        for item in loaded[:50]:
            if isinstance(item, dict):
                keys.update(item.keys())
        return keys
    return set()


def _normalized_extension(path: Path) -> str:
    suffixes = [suffix.lower() for suffix in path.suffixes]
    if suffixes[-2:] == [".jsonl", ".gz"]:
        return ".jsonl.gz"
    if suffixes[-2:] == [".xml", ".gz"]:
        return ".xml.gz"
    if suffixes[-2:] == [".parquet", ".gz"]:
        return ".parquet.gz"
    return path.suffix.lower() or "none"


def _is_metadata_file(path: Path) -> bool:
    name_parts = {_normalize_key(part) for part in re.split(r"[^A-Za-z0-9]+", path.stem)}
    return bool(name_parts & METADATA_NAME_CUES)


def _normalize_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def _local_name(tag: str) -> str:
    return etree.QName(tag).localname if isinstance(tag, str) else str(tag)


def _contains_any(values: set[str], candidates: set[str]) -> bool:
    return bool(values & candidates)


def _has_year(text: str) -> bool:
    return bool(re.search(r"\b(?:19|20)\d{2}\b", text))


def _has_inline_citation(text: str) -> bool:
    return bool(
        re.search(r"\([A-Z][^)]{0,80}\b(?:19|20)\d{2}[a-z]?\)", text)
        or re.search(r"\[[0-9,\-\s;]+\]", text)
    )


def _file_contains(path: Path, needle: str) -> bool:
    return needle.lower() in _read_text_sample(path, limit=8192).lower()


def _read_text_sample(path: Path, limit: int = 65536) -> str:
    return path.read_bytes()[:limit].decode("utf-8", errors="ignore")


def _join_values(values: Any) -> str | None:
    cleaned = sorted({str(value) for value in values if str(value)})
    return ", ".join(cleaned) if cleaned else None


def _value_counts(df: pd.DataFrame, columns: list[str], count_name: str) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=[*columns, count_name])
    filled = df.copy()
    for column in columns:
        filled[column] = filled[column].fillna("unavailable")
    return (
        filled.groupby(columns, dropna=False)
        .size()
        .reset_index(name=count_name)
        .sort_values([count_name, *columns], ascending=[False, *([True] * len(columns))])
    )


def _metadata_summary(inventory: pd.DataFrame) -> str:
    if inventory.empty:
        return "No records available."
    metadata_count = int(inventory["is_metadata_file"].sum())
    return f"{metadata_count} files look like metadata, manifest, schema, README, or license files."


def _sample_paths(inventory: pd.DataFrame, sample_size: int) -> str:
    if inventory.empty:
        return "No records available."
    sample = inventory[["relative_path", "likely_format", "size_bytes"]].head(sample_size)
    return _table(sample)


def _split_counter(values: pd.Series) -> Counter[str]:
    counter: Counter[str] = Counter()
    for value in values.dropna():
        for part in str(value).split(","):
            stripped = part.strip()
            if stripped:
                counter[stripped] += 1
    return counter


def _counter_table(counter: Counter[str], key_name: str, count_name: str) -> str:
    if not counter:
        return "No records available."
    frame = pd.DataFrame(
        [{key_name: key, count_name: count} for key, count in counter.most_common()]
    )
    return _table(frame)


def _content_signal_table(inventory: pd.DataFrame) -> str:
    signals = [
        "contains_title",
        "contains_year",
        "contains_sections",
        "contains_paragraphs",
        "contains_references",
        "contains_inline_citations",
    ]
    rows = [
        {"signal": signal, "files_with_signal": int(inventory[signal].sum())}
        for signal in signals
    ]
    return _table(pd.DataFrame(rows))


def _table(df: pd.DataFrame) -> str:
    if df.empty:
        return "No records available."

    columns = list(df.columns)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in df.itertuples(index=False, name=None):
        values = [_markdown_cell(value) for value in row]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def _markdown_cell(value: Any) -> str:
    if pd.isna(value):
        return "unavailable"
    return str(value).replace("|", "\\|")
