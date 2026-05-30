from __future__ import annotations

from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from citeevidence.cli import app
from citeevidence.objects import (
    OBJECT_MENTION_COLUMNS,
    ObjectRegistryEntry,
    load_object_registry,
    match_object_mentions,
    match_objects_in_contexts,
)


def _context_row(
    context_id: str,
    sentence_text: str,
    *,
    resolved_cited_title: str = "A BERT Paper",
) -> dict[str, object]:
    return {
        "context_id": context_id,
        "source_context_id": f"src_{context_id}",
        "citing_paper_id": "P00-0001",
        "resolved_cited_acl_id": "P00-0002",
        "resolved_cited_title": resolved_cited_title,
        "normalized_section": "method",
        "raw_section_name": "Method",
        "sentence_text": sentence_text,
        "context_window_s3": sentence_text,
    }


def _entry(
    object_id: str,
    canonical_name: str,
    aliases: list[str],
    *,
    negative_aliases: list[str] | None = None,
    allow_short_alias: bool = False,
) -> ObjectRegistryEntry:
    return ObjectRegistryEntry(
        object_id=object_id,
        canonical_name=canonical_name,
        aliases=tuple(aliases),
        negative_aliases=tuple(negative_aliases or []),
        object_type="model",
        linked_paper_title=None,
        linked_acl_id=None,
        linked_doi=None,
        source="fixture",
        notes="fixture",
        allow_short_alias=allow_short_alias,
    )


def test_exact_and_case_insensitive_alias_match() -> None:
    contexts = pd.DataFrame(
        [
            _context_row("ctx_exact", "We fine-tune BERT for tagging."),
            _context_row("ctx_case", "We fine-tune bert for tagging."),
        ]
    )

    mentions, _ = match_object_mentions(contexts, [_entry("obj_bert", "BERT", ["BERT"])])

    assert set(mentions["context_id"]) == {"ctx_exact", "ctx_case"}
    assert "exact_alias" in set(mentions["match_type"])
    assert "case_insensitive_alias" in set(mentions["match_type"])
    assert set(OBJECT_MENTION_COLUMNS) <= set(mentions.columns)


def test_punctuation_normalized_match() -> None:
    contexts = pd.DataFrame([_context_row("ctx", "We evaluate on CoNLL 2003.")])
    registry = [
        _entry("obj_conll_2003", "CoNLL-2003", ["CoNLL-2003"]),
    ]

    mentions, _ = match_object_mentions(contexts, registry)

    assert mentions.shape[0] >= 1
    row = mentions.loc[mentions["matched_in"].eq("sentence_text")].iloc[0]
    assert row["surface_form"] == "CoNLL 2003"
    assert row["match_type"] == "punctuation_normalized_alias"


def test_longest_match_priority() -> None:
    contexts = pd.DataFrame([_context_row("ctx", "We use conditional random fields.")])
    registry = [
        _entry("obj_crf", "CRF", ["field", "conditional random fields"]),
    ]

    mentions, _ = match_object_mentions(contexts, registry)

    sentence_mentions = mentions.loc[mentions["matched_in"].eq("sentence_text")]
    assert sentence_mentions.shape[0] == 1
    assert sentence_mentions.iloc[0]["surface_form"] == "conditional random fields"


def test_word_boundary_prevents_false_positive() -> None:
    contexts = pd.DataFrame([_context_row("ctx", "This BERTology paper is different.")])

    mentions, _ = match_object_mentions(contexts, [_entry("obj_bert", "BERT", ["BERT"])])

    assert mentions.loc[mentions["matched_in"].eq("sentence_text")].empty


def test_negative_alias_blocks_match() -> None:
    contexts = pd.DataFrame([_context_row("ctx", "A decision tree baseline is included.")])
    registry = [
        _entry("obj_tree", "tree", ["tree"], negative_aliases=["decision tree"]),
    ]

    mentions, diagnostics = match_object_mentions(contexts, registry)

    assert mentions.loc[mentions["matched_in"].eq("sentence_text")].empty
    assert diagnostics["negative_alias_blocked_count"] >= 1


def test_short_alias_blocked_unless_allowed() -> None:
    contexts = pd.DataFrame([_context_row("ctx", "F1 improves over the baseline.")])
    blocked_registry = [_entry("obj_f1", "F1", ["F1"], allow_short_alias=False)]
    allowed_registry = [_entry("obj_f1", "F1", ["F1"], allow_short_alias=True)]

    blocked_mentions, _ = match_object_mentions(contexts, blocked_registry)
    allowed_mentions, _ = match_object_mentions(contexts, allowed_registry)

    assert blocked_mentions.empty
    assert not allowed_mentions.loc[allowed_mentions["matched_in"].eq("sentence_text")].empty


def test_provenance_field_is_set() -> None:
    contexts = pd.DataFrame([_context_row("ctx", "We use BERT.")])
    mentions, _ = match_object_mentions(contexts, [_entry("obj_bert", "BERT", ["BERT"])])

    assert mentions.iloc[0]["provenance"] == "registry_seed:obj_bert;alias=BERT"


def test_match_objects_cli_limit_and_outputs(tmp_path: Path) -> None:
    contexts_path = tmp_path / "contexts.parquet"
    registry_path = tmp_path / "registry.yaml"
    out_path = tmp_path / "object_mentions_sample.parquet"
    report_path = tmp_path / "object_matching_sample_report.md"
    pd.DataFrame(
        [
            _context_row("ctx1", "We use BERT."),
            _context_row("ctx2", "We use Transformer models."),
        ]
    ).to_parquet(contexts_path, index=False)
    registry_path.write_text(
        """
objects:
  - object_id: obj_bert
    canonical_name: BERT
    aliases: [BERT]
    negative_aliases: []
    object_type: model
    linked_paper_title:
    linked_acl_id:
    linked_doi:
    source: fixture
    notes: fixture
    allow_short_alias: false
""",
        encoding="utf-8",
    )

    metrics = match_objects_in_contexts(
        contexts_path=contexts_path,
        registry_path=registry_path,
        out_path=out_path,
        report_path=report_path,
        limit=1,
    )

    assert metrics["input_context_rows_processed"] == 1
    assert pd.read_parquet(out_path)["context_id"].nunique() == 1
    assert "## Core Metrics" in report_path.read_text(encoding="utf-8")

    runner = CliRunner()
    cli_out = tmp_path / "cli_mentions.parquet"
    cli_report = tmp_path / "cli_report.md"
    result = runner.invoke(
        app,
        [
            "objects",
            "match",
            "--contexts",
            str(contexts_path),
            "--registry",
            str(registry_path),
            "--out",
            str(cli_out),
            "--report",
            str(cli_report),
            "--limit",
            "1",
        ],
    )

    assert result.exit_code == 0
    assert "Processed 1 contexts" in result.stdout
    assert cli_out.exists()
    assert cli_report.exists()


def test_seed_registry_loads() -> None:
    registry = load_object_registry("configs/object_registry_seed.yaml")

    assert {entry.canonical_name for entry in registry} >= {"BERT", "BLEU", "SQuAD"}
