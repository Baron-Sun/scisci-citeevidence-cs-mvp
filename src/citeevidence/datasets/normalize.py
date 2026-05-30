from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

import pandas as pd

from citeevidence.schemas import Intent, ObjectType

NORMALIZED_COLUMNS = [
    "dataset_name",
    "context_id",
    "citing_paper_id",
    "cited_paper_id",
    "section",
    "context_text",
    "citation_marker",
    "original_label",
    "normalized_intent",
    "normalized_object_type",
    "is_multisentence",
    "label_source",
    "mapping_notes",
]

FIELD_ALIASES = {
    "context_id": ["context_id", "id", "citation_id", "cite_id", "sample_id", "unique_id"],
    "citing_paper_id": [
        "citing_paper_id",
        "citingpaperid",
        "source_paper_id",
        "paper_id",
        "citing_id",
        "source_id",
        "source",
    ],
    "cited_paper_id": [
        "cited_paper_id",
        "citedpaperid",
        "target_paper_id",
        "reference_id",
        "ref_id",
        "cited_id",
        "target_id",
        "target",
    ],
    "section": ["section", "section_title", "section_name", "sectionname"],
    "context_text": [
        "context_text",
        "citation_context",
        "context",
        "text",
        "sentence",
        "string",
        "citing_sentence",
        "cite_context",
    ],
    "citation_marker": [
        "citation_marker",
        "cite_marker",
        "citation",
        "marker",
        "cite",
        "citation_string",
    ],
    "original_label": [
        "original_label",
        "label",
        "intent",
        "citation_intent",
        "class",
        "category",
        "gold_label",
        "annotation",
        "multicite_label",
    ],
    "is_multisentence": [
        "is_multisentence",
        "multi_sentence",
        "multisentence",
        "is_multi_sentence",
    ],
    "cite_start": ["cite_start", "citestart"],
    "cite_end": ["cite_end", "citeend"],
}

COMPARISON_CUES = {
    "against",
    "baseline",
    "better",
    "compare",
    "compared",
    "comparison",
    "contrast",
    "higher",
    "lower",
    "outperform",
    "outperforms",
    "similar",
    "than",
    "versus",
    "worse",
}

CRITIQUE_CUES = {
    "cannot",
    "fail",
    "fails",
    "failed",
    "however",
    "limitation",
    "limitations",
    "limited",
    "problem",
    "shortcoming",
    "shortcomings",
    "unlike",
    "weakness",
}

OBJECT_TYPE_CUES = {
    ObjectType.DATASET_OR_DATABASE.value: {
        "benchmark dataset",
        "corpus",
        "data set",
        "database",
        "dataset",
        "datasets",
        "knowledge base",
        "treebank",
    },
    ObjectType.SOFTWARE_OR_TOOL.value: {
        "code",
        "library",
        "package",
        "software",
        "tool",
        "toolkit",
    },
    ObjectType.BENCHMARK_OR_PROTOCOL.value: {
        "benchmark",
        "challenge",
        "evaluation protocol",
        "protocol",
        "shared task",
        "task",
    },
    ObjectType.METRIC.value: {
        "accuracy",
        "bleu",
        "f1",
        "metric",
        "precision",
        "recall",
        "score",
    },
    ObjectType.METHOD.value: {
        "algorithm",
        "architecture",
        "approach",
        "framework",
        "method",
        "model",
        "system",
    },
    ObjectType.THEORY_OR_CONCEPT.value: {
        "concept",
        "hypothesis",
        "principle",
        "theory",
    },
    ObjectType.CLAIM_OR_FINDING.value: {
        "claim",
        "finding",
        "observation",
        "result",
        "showed",
        "shows",
    },
}


def load_labeled_records(
    root: str | Path,
    *,
    dataset_name: str,
    label_source: str,
) -> pd.DataFrame:
    """Read raw labeled citation records and normalize them to project columns."""
    records = read_records(root)
    normalized = [
        normalize_record(record, dataset_name=dataset_name, label_source=label_source)
        for record in records
    ]
    return pd.DataFrame(normalized, columns=NORMALIZED_COLUMNS)


def read_records(root: str | Path) -> list[dict[str, Any]]:
    """Read JSONL, JSON, and CSV records from a file or directory."""
    path = Path(root)
    if not path.exists():
        raise FileNotFoundError(f"Dataset input path does not exist: {path}")

    files = [path] if path.is_file() else sorted(_supported_files(path))
    records: list[dict[str, Any]] = []
    for file_path in files:
        records.extend(_read_file(file_path))
    return records


def normalize_record(
    record: dict[str, Any],
    *,
    dataset_name: str,
    label_source: str,
) -> dict[str, Any]:
    """Normalize one raw dataset row into the shared labeled-context shape."""
    context_text = _field_as_string(record, "context_text") or ""
    original_label = _field_as_string(record, "original_label")
    context_id = _field_as_string(record, "context_id") or _make_context_id(
        dataset_name=dataset_name,
        citing_paper_id=_field_as_string(record, "citing_paper_id"),
        cited_paper_id=_field_as_string(record, "cited_paper_id"),
        context_text=context_text,
        original_label=original_label,
    )

    mapping = map_label(
        dataset_name=dataset_name,
        original_label=original_label,
        context_text=context_text,
    )

    return {
        "dataset_name": dataset_name,
        "context_id": f"{dataset_name}_{context_id}",
        "citing_paper_id": _field_as_string(record, "citing_paper_id"),
        "cited_paper_id": _field_as_string(record, "cited_paper_id"),
        "section": _field_as_string(record, "section"),
        "context_text": context_text or None,
        "citation_marker": _field_as_string(record, "citation_marker")
        or _citation_marker_from_offsets(record, context_text),
        "original_label": original_label,
        "normalized_intent": mapping["normalized_intent"],
        "normalized_object_type": mapping["normalized_object_type"],
        "is_multisentence": _field_as_bool(record, "is_multisentence", context_text),
        "label_source": label_source,
        "mapping_notes": mapping["mapping_notes"],
    }


def map_label(
    *,
    dataset_name: str,
    original_label: str | None,
    context_text: str | None,
) -> dict[str, str | None]:
    """Map source labels to the project intent/object taxonomy."""
    label_key = _label_key(original_label)
    object_type = _infer_object_type(context_text)

    if label_key in {"0", "background", "back"}:
        return _mapping(Intent.BACKGROUND.value, object_type, "Direct background mapping.")

    if label_key in {"1", "method"}:
        return _mapping(
            Intent.USES.value,
            ObjectType.METHOD.value,
            "SciCite method mapped to uses with object_type=method.",
        )

    if label_key in {"uses", "use"}:
        return _mapping(
            Intent.USES.value,
            object_type,
            "MultiCite Uses mapped to uses; object_type inferred when possible.",
        )

    if label_key in {"extends", "extension", "extend", "ext"}:
        return _mapping(
            Intent.EXTENDS.value,
            object_type,
            "MultiCite Extends mapped to extends; object_type inferred when possible.",
        )

    if label_key in {"result_comparison", "results_comparison", "comparison", "compare"}:
        return _mapping(
            Intent.COMPARES_AGAINST.value,
            object_type or ObjectType.CLAIM_OR_FINDING.value,
            "Result comparison label mapped to compares_against.",
        )

    if label_key in {"2", "result", "results"}:
        if _has_any_cue(context_text, COMPARISON_CUES):
            return _mapping(
                Intent.COMPARES_AGAINST.value,
                object_type or ObjectType.CLAIM_OR_FINDING.value,
                "Result label mapped to compares_against because comparison cues were present.",
            )
        return _mapping(
            None,
            object_type,
            "Result label is not confidently mapped without comparison cues.",
        )

    if label_key in {"differences", "difference", "dif"}:
        if _has_any_cue(context_text, CRITIQUE_CUES):
            return _mapping(
                Intent.CRITIQUES.value,
                object_type,
                "MultiCite Differences mapped to critiques based on critique/limitation cues.",
            )
        return _mapping(
            Intent.COMPARES_AGAINST.value,
            object_type,
            "MultiCite Differences mapped to compares_against; review critique boundary.",
        )

    if label_key in {"similarities", "similarity", "sim"}:
        return _mapping(
            Intent.COMPARES_AGAINST.value,
            object_type,
            "MultiCite Similarities mapped to compares_against as a comparison label.",
        )

    if label_key in {"critique", "critiques", "limitation", "limitations"}:
        return _mapping(Intent.CRITIQUES.value, object_type, "Critique label mapped directly.")

    if label_key in {"applies", "application", "apply"}:
        return _mapping(Intent.APPLIES.value, object_type, "Application label mapped to applies.")

    if dataset_name == "scicite" and label_key == "":
        return _mapping(None, None, "Missing SciCite label cannot be mapped confidently.")

    if dataset_name == "multicite" and label_key == "":
        return _mapping(None, None, "Missing MultiCite label cannot be mapped confidently.")

    label_name = original_label if original_label is not None else "missing label"
    return _mapping(None, object_type, f"Label '{label_name}' cannot be mapped confidently.")


def write_labeled_contexts(
    frames: list[pd.DataFrame],
    *,
    out_path: str | Path,
    report_path: str | Path,
) -> pd.DataFrame:
    """Combine normalized frames, write parquet, and write a markdown profile."""
    nonempty_frames = [frame for frame in frames if not frame.empty]
    if nonempty_frames:
        combined = pd.concat(nonempty_frames, ignore_index=True)
        combined = combined[NORMALIZED_COLUMNS]
    else:
        combined = pd.DataFrame(columns=NORMALIZED_COLUMNS)

    output = Path(out_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    combined.to_parquet(output, index=False)

    write_labeled_dataset_profile(combined, report_path)
    return combined


def write_labeled_dataset_profile(df: pd.DataFrame, report_path: str | Path) -> None:
    """Write a compact markdown profile for the normalized labeled dataset."""
    report = Path(report_path)
    report.parent.mkdir(parents=True, exist_ok=True)

    sections = [
        "# Labeled Dataset Profile",
        "",
        "## Number of Contexts by Dataset",
        _table(_value_counts(df, ["dataset_name"], "contexts")),
        "",
        "## Original Label Distribution",
        _table(_value_counts(df, ["dataset_name", "original_label"], "contexts")),
        "",
        "## Normalized Label Distribution",
        "### Intent",
        _table(_value_counts(df, ["dataset_name", "normalized_intent"], "contexts")),
        "",
        "### Object Type",
        _table(_value_counts(df, ["dataset_name", "normalized_object_type"], "contexts")),
        "",
        "## Section Distribution",
        _section_distribution(df),
        "",
        "## Multisentence Rate",
        _multisentence_rate(df),
        "",
    ]
    report.write_text("\n".join(sections), encoding="utf-8")


def _read_file(path: Path) -> list[dict[str, Any]]:
    suffix = "".join(path.suffixes[-2:]) if path.name.endswith(".jsonl.gz") else path.suffix
    if suffix == ".jsonl":
        return _read_jsonl(path)
    if suffix == ".json":
        return _read_json(path)
    if suffix == ".csv":
        frame = pd.read_csv(path, keep_default_na=False)
        return list(frame.to_dict(orient="records"))
    return []


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        loaded = json.loads(line)
        if not isinstance(loaded, dict):
            raise ValueError(f"Expected JSON object at {path}:{line_number}")
        records.append(loaded)
    return records


def _read_json(path: Path) -> list[dict[str, Any]]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(loaded, list):
        return _ensure_records(loaded, path)
    if isinstance(loaded, dict):
        for key in ("data", "examples", "records", "instances"):
            value = loaded.get(key)
            if isinstance(value, list):
                return _ensure_records(value, path)
        return [loaded]
    raise ValueError(f"Expected JSON object or array in {path}")


def _ensure_records(values: list[Any], path: Path) -> list[dict[str, Any]]:
    if not all(isinstance(value, dict) for value in values):
        raise ValueError(f"Expected all JSON array values to be objects in {path}")
    return values


def _supported_files(path: Path) -> list[Path]:
    return [
        file_path
        for file_path in path.rglob("*")
        if file_path.is_file() and file_path.suffix in {".jsonl", ".json", ".csv"}
    ]


def _field_as_string(record: dict[str, Any], canonical_name: str) -> str | None:
    value = _first_value(record, FIELD_ALIASES[canonical_name])
    return _clean_string(value)


def _field_as_bool(
    record: dict[str, Any],
    canonical_name: str,
    context_text: str | None,
) -> bool | None:
    value = _first_value(record, FIELD_ALIASES[canonical_name])
    if value is None or value == "":
        if context_text:
            return _looks_multisentence(context_text)
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, int | float):
        return bool(value)
    if isinstance(value, str):
        value_key = value.strip().lower()
        if value_key in {"true", "t", "yes", "y", "1"}:
            return True
        if value_key in {"false", "f", "no", "n", "0"}:
            return False
    return None


def _citation_marker_from_offsets(record: dict[str, Any], context_text: str | None) -> str | None:
    if not context_text:
        return None
    start_value = _first_value(record, FIELD_ALIASES["cite_start"])
    end_value = _first_value(record, FIELD_ALIASES["cite_end"])
    try:
        start = int(start_value)
        end = int(end_value)
    except (TypeError, ValueError):
        return None
    if 0 <= start < end <= len(context_text):
        return context_text[start:end].strip() or None
    return None


def _first_value(record: dict[str, Any], aliases: list[str]) -> Any:
    lower_lookup = {key.lower(): value for key, value in record.items()}
    for alias in aliases:
        if alias.lower() in lower_lookup:
            return lower_lookup[alias.lower()]
    return None


def _clean_string(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, list):
        value = " ".join(str(item) for item in value)
    elif isinstance(value, dict):
        value = json.dumps(value, sort_keys=True)
    elif pd.isna(value):
        return None
    text = str(value).strip()
    return text or None


def _make_context_id(
    *,
    dataset_name: str,
    citing_paper_id: str | None,
    cited_paper_id: str | None,
    context_text: str | None,
    original_label: str | None,
) -> str:
    payload = "\x1f".join(
        [
            dataset_name,
            citing_paper_id or "",
            cited_paper_id or "",
            " ".join((context_text or "").split()),
            original_label or "",
        ]
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _label_key(label: str | None) -> str:
    if label is None:
        return ""
    cleaned = label.strip().lower()
    cleaned = re.sub(r"[^a-z0-9]+", "_", cleaned)
    return cleaned.strip("_")


def _mapping(
    normalized_intent: str | None,
    normalized_object_type: str | None,
    mapping_notes: str,
) -> dict[str, str | None]:
    return {
        "normalized_intent": normalized_intent,
        "normalized_object_type": normalized_object_type,
        "mapping_notes": mapping_notes,
    }


def _infer_object_type(context_text: str | None) -> str | None:
    if not context_text:
        return None
    lowered = context_text.lower()
    for object_type, cues in OBJECT_TYPE_CUES.items():
        if any(cue in lowered for cue in cues):
            return object_type
    return None


def _has_any_cue(context_text: str | None, cues: set[str]) -> bool:
    if not context_text:
        return False
    lowered = context_text.lower()
    return any(cue in lowered for cue in cues)


def _looks_multisentence(context_text: str) -> bool:
    sentence_endings = re.findall(r"[.!?]+(?=\s|$)", context_text)
    return len(sentence_endings) > 1


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
        .sort_values([*columns])
    )


def _section_distribution(df: pd.DataFrame) -> str:
    if df.empty or not df["section"].notna().any():
        return "No section values available."
    return _table(_value_counts(df, ["dataset_name", "section"], "contexts"))


def _multisentence_rate(df: pd.DataFrame) -> str:
    if df.empty or not df["is_multisentence"].notna().any():
        return "No multisentence values available."

    rows = []
    for dataset_name, group in df.groupby("dataset_name", dropna=False):
        available = group["is_multisentence"].dropna()
        total = len(available)
        multisentence = int(available.sum()) if total else 0
        rate = multisentence / total if total else 0.0
        rows.append(
            {
                "dataset_name": dataset_name,
                "contexts_with_signal": total,
                "multisentence_contexts": multisentence,
                "multisentence_rate": f"{rate:.3f}",
            }
        )
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
