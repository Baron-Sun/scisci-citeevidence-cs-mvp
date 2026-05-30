from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

import pandas as pd

from citeevidence.datasets.normalize import (
    NORMALIZED_COLUMNS,
    load_labeled_records,
    map_label,
)


def load_multicite(root: str | Path) -> pd.DataFrame:
    """Load and normalize MultiCite labeled citation contexts."""
    path = Path(root)
    full_json = path / "full-v20210918.json" if path.is_dir() else path
    if full_json.name == "full-v20210918.json" and full_json.exists():
        return _load_full_v20210918(full_json)
    return load_labeled_records(root, dataset_name="multicite", label_source="multicite_gold")


def _load_full_v20210918(path: Path) -> pd.DataFrame:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        return load_labeled_records(path, dataset_name="multicite", label_source="multicite_gold")

    rows: list[dict[str, Any]] = []
    for example_id, example in loaded.items():
        if not isinstance(example, dict):
            continue
        sentence_lookup = _sentence_lookup(example.get("x"))
        label_payload = example.get("y")
        if not isinstance(label_payload, dict):
            continue

        for original_label, details in label_payload.items():
            if not isinstance(details, dict):
                continue
            gold_contexts = details.get("gold_contexts")
            if not isinstance(gold_contexts, list):
                gold_contexts = []
            cite_sentences = details.get("cite_sentences")
            cite_sentence_ids = cite_sentences if isinstance(cite_sentences, list) else []

            contexts = gold_contexts or [[sentence_id] for sentence_id in cite_sentence_ids]
            for context_index, sentence_ids in enumerate(contexts):
                sentence_id_list = _sentence_id_list(sentence_ids)
                context_text = " ".join(
                    sentence_lookup[sentence_id]
                    for sentence_id in sentence_id_list
                    if sentence_id in sentence_lookup
                ).strip()
                if not context_text:
                    continue

                first_sentence_id = sentence_id_list[0] if sentence_id_list else None
                citing_paper_id = _paper_id_from_sentence_id(first_sentence_id) or example_id
                mapping = map_label(
                    dataset_name="multicite",
                    original_label=original_label,
                    context_text=context_text,
                )
                context_id = _multicite_context_id(
                    example_id=example_id,
                    original_label=original_label,
                    context_index=context_index,
                    sentence_ids=sentence_id_list,
                )
                rows.append(
                    {
                        "dataset_name": "multicite",
                        "context_id": context_id,
                        "citing_paper_id": citing_paper_id,
                        "cited_paper_id": example_id,
                        "section": None,
                        "context_text": context_text,
                        "citation_marker": _citation_marker(context_text),
                        "original_label": original_label,
                        "normalized_intent": mapping["normalized_intent"],
                        "normalized_object_type": mapping["normalized_object_type"],
                        "is_multisentence": len(sentence_id_list) > 1,
                        "label_source": "multicite_gold",
                        "mapping_notes": mapping["mapping_notes"],
                    }
                )

    return pd.DataFrame(rows, columns=NORMALIZED_COLUMNS)


def _sentence_lookup(value: Any) -> dict[str, str]:
    if not isinstance(value, list):
        return {}
    lookup: dict[str, str] = {}
    for sentence in value:
        if not isinstance(sentence, dict):
            continue
        sentence_id = sentence.get("sent_id")
        text = sentence.get("text")
        if isinstance(sentence_id, str) and isinstance(text, str):
            lookup[sentence_id] = _clean_text(text)
    return lookup


def _sentence_id_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def _paper_id_from_sentence_id(sentence_id: str | None) -> str | None:
    if not sentence_id:
        return None
    if "-C" in sentence_id:
        return sentence_id.split("-C", 1)[0]
    return sentence_id.rsplit("-", 1)[0] if "-" in sentence_id else sentence_id


def _multicite_context_id(
    *,
    example_id: str,
    original_label: str,
    context_index: int,
    sentence_ids: list[str],
) -> str:
    payload = "\x1f".join([example_id, original_label, str(context_index), *sentence_ids])
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"multicite_{digest}"


def _citation_marker(context_text: str) -> str | None:
    span_match = re.search(r"<span[^>]*>(.*?)</span>", context_text)
    if span_match:
        return _clean_text(span_match.group(1))
    parenthetical = re.search(r"\([A-Z][^)]{0,120}\b(?:19|20)\d{2}[a-z]?\)", context_text)
    if parenthetical:
        return parenthetical.group(0)
    bracket = re.search(r"\[[0-9,\-\s;]+\]", context_text)
    return bracket.group(0) if bracket else None


def _clean_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", text).strip()
