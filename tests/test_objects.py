from __future__ import annotations

from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from citeevidence.cli import app
from citeevidence.objects import (
    OBJECT_MENTION_COLUMNS,
    OBJECT_REVIEW_SAMPLE_COLUMNS,
    ObjectRegistryEntry,
    build_object_mentions_review_sample,
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
    object_type: str = "model",
    object_category: str = "named_object",
    allow_in_object_graph: bool = True,
    require_case_sensitive: bool = False,
    require_context_cue: tuple[str, ...] = (),
    confidence_override: float | None = None,
) -> ObjectRegistryEntry:
    return ObjectRegistryEntry(
        object_id=object_id,
        canonical_name=canonical_name,
        aliases=tuple(aliases),
        negative_aliases=tuple(negative_aliases or []),
        object_type=object_type,
        linked_paper_title=None,
        linked_acl_id=None,
        linked_doi=None,
        source="fixture",
        notes="fixture",
        allow_short_alias=allow_short_alias,
        object_category=object_category,
        allow_in_object_graph=allow_in_object_graph,
        require_case_sensitive=require_case_sensitive,
        require_context_cue=require_context_cue,
        confidence_override=confidence_override,
    )


def test_exact_and_case_insensitive_alias_match() -> None:
    contexts = pd.DataFrame(
        [
            _context_row("ctx_exact", "We fine-tune BERT for tagging."),
            _context_row("ctx_case", "We fine-tune bert for tagging."),
        ]
    )

    mentions, _, _ = match_object_mentions(contexts, [_entry("obj_bert", "BERT", ["BERT"])])

    assert set(mentions["context_id"]) == {"ctx_exact", "ctx_case"}
    assert "exact_alias" in set(mentions["match_type"])
    assert "case_insensitive_alias" in set(mentions["match_type"])
    assert set(OBJECT_MENTION_COLUMNS) <= set(mentions.columns)


def test_punctuation_normalized_match() -> None:
    contexts = pd.DataFrame([_context_row("ctx", "We evaluate on CoNLL 2003.")])
    registry = [
        _entry("obj_conll_2003", "CoNLL-2003", ["CoNLL-2003"]),
    ]

    mentions, _, _ = match_object_mentions(contexts, registry)

    assert mentions.shape[0] >= 1
    row = mentions.loc[mentions["matched_in"].eq("sentence_text")].iloc[0]
    assert row["surface_form"] == "CoNLL 2003"
    assert row["match_type"] == "punctuation_normalized_alias"


def test_longest_match_priority() -> None:
    contexts = pd.DataFrame([_context_row("ctx", "We use conditional random fields.")])
    registry = [
        _entry("obj_crf", "CRF", ["field", "conditional random fields"]),
    ]

    mentions, _, _ = match_object_mentions(contexts, registry)

    sentence_mentions = mentions.loc[mentions["matched_in"].eq("sentence_text")]
    assert sentence_mentions.shape[0] == 1
    assert sentence_mentions.iloc[0]["surface_form"] == "conditional random fields"


def test_word_boundary_prevents_false_positive() -> None:
    contexts = pd.DataFrame([_context_row("ctx", "This BERTology paper is different.")])

    mentions, _, _ = match_object_mentions(contexts, [_entry("obj_bert", "BERT", ["BERT"])])

    assert mentions.loc[mentions["matched_in"].eq("sentence_text")].empty


def test_negative_alias_blocks_match() -> None:
    contexts = pd.DataFrame([_context_row("ctx", "A decision tree baseline is included.")])
    registry = [
        _entry("obj_tree", "tree", ["tree"], negative_aliases=["decision tree"]),
    ]

    mentions, _, diagnostics = match_object_mentions(contexts, registry)

    assert mentions.loc[mentions["matched_in"].eq("sentence_text")].empty
    assert diagnostics["negative_alias_blocked_count"] >= 1


def test_short_alias_blocked_unless_allowed() -> None:
    contexts = pd.DataFrame([_context_row("ctx", "F1 improves over the baseline.")])
    blocked_registry = [_entry("obj_f1", "F1", ["F1"], allow_short_alias=False)]
    allowed_registry = [_entry("obj_f1", "F1", ["F1"], allow_short_alias=True)]

    blocked_mentions, _, _ = match_object_mentions(contexts, blocked_registry)
    allowed_mentions, _, _ = match_object_mentions(contexts, allowed_registry)

    assert blocked_mentions.empty
    assert not allowed_mentions.loc[allowed_mentions["matched_in"].eq("sentence_text")].empty


def test_provenance_field_is_set() -> None:
    contexts = pd.DataFrame([_context_row("ctx", "We use BERT.")])
    mentions, _, _ = match_object_mentions(contexts, [_entry("obj_bert", "BERT", ["BERT"])])

    assert mentions.iloc[0]["provenance"] == "registry_seed:obj_bert;alias=BERT"


def test_sentence_window_duplicate_is_deduplicated() -> None:
    contexts = pd.DataFrame(
        [
            _context_row(
                "ctx",
                "We use BERT.",
                resolved_cited_title="A different paper",
            )
        ]
    )

    mentions, title_profiles, diagnostics = match_object_mentions(
        contexts,
        [_entry("obj_bert", "BERT", ["BERT"])],
    )

    assert title_profiles.empty
    assert mentions.shape[0] == 1
    assert mentions.iloc[0]["matched_in"] == "sentence_text"
    assert diagnostics["deduplicated_count"] == 1


def test_context_window_neighbor_match_is_retained() -> None:
    contexts = pd.DataFrame(
        [
            {
                **_context_row(
                    "ctx",
                    "This sentence cites prior work.",
                    resolved_cited_title="A different paper",
                ),
                "context_window_s3": (
                    "Earlier context mentions BERT. This sentence cites prior work."
                ),
            }
        ]
    )

    mentions, _, _ = match_object_mentions(contexts, [_entry("obj_bert", "BERT", ["BERT"])])

    assert mentions.shape[0] == 1
    assert mentions.iloc[0]["matched_in"] == "context_window_neighbor"
    assert mentions.iloc[0]["confidence"] == 0.85


def test_resolved_cited_title_profile_is_separate() -> None:
    contexts = pd.DataFrame(
        [_context_row("ctx", "This sentence has no object.", resolved_cited_title="A BERT Paper")]
    )

    mentions, title_profiles, _ = match_object_mentions(
        contexts,
        [_entry("obj_bert", "BERT", ["BERT"])],
    )

    assert mentions.empty
    assert title_profiles.shape[0] == 1
    assert title_profiles.iloc[0]["matched_in"] == "resolved_cited_title"


def test_generic_metric_policy_and_graph_flag() -> None:
    contexts = pd.DataFrame(
        [_context_row("ctx", "The system improves accuracy and F1.")]
    )
    registry = [
        _entry(
            "obj_accuracy",
            "accuracy",
            ["accuracy"],
            object_type="metric",
            object_category="generic_metric",
            allow_in_object_graph=False,
            confidence_override=0.7,
        ),
        _entry(
            "obj_f1",
            "F1",
            ["F1"],
            object_type="metric",
            object_category="generic_metric",
            allow_in_object_graph=False,
            allow_short_alias=True,
            require_case_sensitive=True,
            confidence_override=0.7,
        ),
    ]

    mentions, _, _ = match_object_mentions(contexts, registry)

    assert set(mentions["object_category"]) == {"generic_metric"}
    assert not mentions["allow_in_object_graph"].any()
    assert set(mentions["confidence"]) == {0.7}


def test_f1_case_sensitive_short_alias_policy() -> None:
    contexts = pd.DataFrame([_context_row("ctx", "F1 improves, but f1 should not match.")])
    registry = [
        _entry(
            "obj_f1",
            "F1",
            ["F1"],
            object_type="metric",
            object_category="generic_metric",
            allow_in_object_graph=False,
            allow_short_alias=True,
            require_case_sensitive=True,
        )
    ]

    mentions, _, diagnostics = match_object_mentions(contexts, registry)

    assert mentions.loc[mentions["matched_in"].eq("sentence_text")].shape[0] == 1
    assert diagnostics["case_blocked_count"] >= 1


def test_ptb_requires_context_cue_for_high_confidence() -> None:
    contexts = pd.DataFrame(
        [
            _context_row("ctx_cue", "We evaluate on PTB corpus."),
            _context_row("ctx_no_cue", "We use PTB in preprocessing."),
        ]
    )
    registry = [
        _entry(
            "obj_ptb",
            "Penn Treebank",
            ["PTB"],
            object_type="dataset_or_database",
            require_context_cue=("treebank", "corpus", "Penn Treebank", "WSJ", "dataset"),
        )
    ]

    mentions, _, _ = match_object_mentions(contexts, registry)
    cue = mentions.loc[mentions["context_id"].eq("ctx_cue")].iloc[0]
    no_cue = mentions.loc[mentions["context_id"].eq("ctx_no_cue")].iloc[0]

    assert cue["confidence"] == 0.95
    assert cue["object_category"] == "named_object"
    assert no_cue["confidence"] == 0.50
    assert no_cue["object_category"] == "ambiguous_short_alias"
    assert not bool(no_cue["allow_in_object_graph"])


def test_lowercase_transformer_gets_lower_confidence() -> None:
    contexts = pd.DataFrame(
        [
            _context_row("ctx_upper", "We use Transformer layers."),
            _context_row("ctx_lower", "We use transformer layers."),
        ]
    )

    mentions, _, _ = match_object_mentions(
        contexts,
        [_entry("obj_transformer", "Transformer", ["Transformer"])],
    )
    upper = mentions.loc[mentions["context_id"].eq("ctx_upper")].iloc[0]
    lower = mentions.loc[mentions["context_id"].eq("ctx_lower")].iloc[0]

    assert upper["confidence"] == 0.95
    assert lower["confidence"] == 0.65
    assert lower["object_category"] == "generic_architecture"
    assert not bool(lower["allow_in_object_graph"])


def test_manual_review_sample_has_required_columns() -> None:
    contexts = pd.DataFrame(
        [_context_row("ctx", "We report F1.", resolved_cited_title="A BERT Paper")]
    )
    mentions, title_profiles, _ = match_object_mentions(
        contexts,
        [
            _entry(
                "obj_f1",
                "F1",
                ["F1"],
                object_type="metric",
                object_category="generic_metric",
                allow_in_object_graph=False,
                allow_short_alias=True,
            ),
            _entry("obj_bert", "BERT", ["BERT"]),
        ],
    )

    sample = build_object_mentions_review_sample(
        contexts=contexts,
        mentions=mentions,
        cited_title_profiles=title_profiles,
    )

    assert set(OBJECT_REVIEW_SAMPLE_COLUMNS) <= set(sample.columns)


def test_match_objects_cli_limit_and_outputs(tmp_path: Path) -> None:
    contexts_path = tmp_path / "contexts.parquet"
    registry_path = tmp_path / "registry.yaml"
    out_path = tmp_path / "object_mentions_sample.parquet"
    cited_title_profiles_path = tmp_path / "cited_title_object_profiles.parquet"
    review_sample_path = tmp_path / "object_mentions_review_sample.csv"
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
        cited_title_profiles_path=cited_title_profiles_path,
        review_sample_path=review_sample_path,
        report_path=report_path,
        limit=1,
    )

    assert metrics["input_context_rows_processed"] == 1
    assert pd.read_parquet(out_path)["context_id"].nunique() == 1
    assert pd.read_parquet(cited_title_profiles_path).shape[0] == 1
    assert pd.read_csv(review_sample_path).shape[0] >= 1
    assert "## Core Counts" in report_path.read_text(encoding="utf-8")

    runner = CliRunner()
    cli_out = tmp_path / "cli_mentions.parquet"
    cli_profiles = tmp_path / "cli_profiles.parquet"
    cli_review = tmp_path / "cli_review.csv"
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
            "--cited-title-profiles",
            str(cli_profiles),
            "--review-sample",
            str(cli_review),
            "--report",
            str(cli_report),
            "--limit",
            "1",
        ],
    )

    assert result.exit_code == 0
    assert "Processed 1 contexts" in result.stdout
    assert cli_out.exists()
    assert cli_profiles.exists()
    assert cli_review.exists()
    assert cli_report.exists()


def test_match_objects_full_mode_outputs_graph_candidates_and_policy_checks(
    tmp_path: Path,
) -> None:
    contexts_path = tmp_path / "contexts.parquet"
    registry_path = tmp_path / "registry.yaml"
    out_path = tmp_path / "object_mentions.parquet"
    cited_title_profiles_path = tmp_path / "cited_title_object_profiles.parquet"
    graph_path = tmp_path / "object_graph_candidate_mentions.parquet"
    strict_path = tmp_path / "object_graph_candidate_mentions_strict.parquet"
    broad_path = tmp_path / "object_graph_candidate_mentions_broad.parquet"
    review_sample_path = tmp_path / "review.csv"
    report_path = tmp_path / "object_matching_report.md"
    pd.DataFrame(
        [
            _context_row("ctx_bert", "We use BERT.", resolved_cited_title="A BERT Paper"),
            _context_row("ctx_metric", "We report accuracy and F1."),
            _context_row("ctx_ptb_cue", "We train on Penn Treebank (PTB) corpus."),
            _context_row("ctx_ptb_no_cue", "We use PTB in preprocessing."),
            _context_row("ctx_upper_transformer", "We use Transformer layers."),
            _context_row("ctx_lower_transformer", "The transformer layer is generic."),
            _context_row("ctx_seq2seq", "We add seq2seq."),
            _context_row("ctx_bleu", "We optimize BLEU."),
            {
                **_context_row(
                    "ctx_neighbor",
                    "This sentence cites prior work.",
                    resolved_cited_title="No object in title",
                ),
                "context_window_s3": (
                    "Earlier context mentions BERT. This sentence cites prior work."
                ),
            },
            _context_row(
                "ctx_title_only",
                "This sentence has no object mention.",
                resolved_cited_title="BERT: Pre-training of Deep Bidirectional Transformers",
            ),
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
  - object_id: obj_accuracy
    canonical_name: accuracy
    aliases: [accuracy]
    negative_aliases: []
    object_type: metric
    linked_paper_title:
    linked_acl_id:
    linked_doi:
    source: fixture
    notes: generic metric
    allow_short_alias: false
    object_category: generic_metric
    allow_in_object_graph: false
    confidence_override: 0.7
  - object_id: obj_f1
    canonical_name: F1
    aliases: [F1]
    negative_aliases: []
    object_type: metric
    linked_paper_title:
    linked_acl_id:
    linked_doi:
    source: fixture
    notes: generic metric
    allow_short_alias: true
    require_case_sensitive: true
    object_category: generic_metric
    allow_in_object_graph: false
    confidence_override: 0.7
  - object_id: obj_perplexity
    canonical_name: perplexity
    aliases: [perplexity]
    negative_aliases: []
    object_type: metric
    linked_paper_title:
    linked_acl_id:
    linked_doi:
    source: fixture
    notes: generic metric
    allow_short_alias: false
    object_category: generic_metric
    allow_in_object_graph: false
    confidence_override: 0.7
  - object_id: obj_penn_treebank
    canonical_name: Penn Treebank
    aliases: [Penn Treebank, PTB]
    negative_aliases: []
    object_type: dataset_or_database
    linked_paper_title:
    linked_acl_id:
    linked_doi:
    source: fixture
    notes: cue controlled
    allow_short_alias: false
    require_context_cue: [Penn Treebank, treebank, corpus, WSJ, dataset]
  - object_id: obj_transformer
    canonical_name: Transformer
    aliases: [Transformer]
    negative_aliases: []
    object_type: model
    linked_paper_title:
    linked_acl_id:
    linked_doi:
    source: fixture
    notes: fixture
    allow_short_alias: false
  - object_id: obj_seq2seq
    canonical_name: seq2seq
    aliases: [seq2seq]
    negative_aliases: []
    object_type: model
    linked_paper_title:
    linked_acl_id:
    linked_doi:
    source: fixture
    notes: cue controlled
    allow_short_alias: false
    require_context_cue: [model, architecture, encoder-decoder, sequence-to-sequence, neural]
    confidence_override: 0.85
  - object_id: obj_bleu
    canonical_name: BLEU
    aliases: [BLEU]
    negative_aliases: []
    object_type: metric
    linked_paper_title:
    linked_acl_id:
    linked_doi:
    source: fixture
    notes: named metric
    allow_short_alias: false
""",
        encoding="utf-8",
    )

    metrics = match_objects_in_contexts(
        contexts_path=contexts_path,
        registry_path=registry_path,
        out_path=out_path,
        cited_title_profiles_path=cited_title_profiles_path,
        object_graph_candidates_path=graph_path,
        strict_object_graph_candidates_path=strict_path,
        broad_object_graph_candidates_path=broad_path,
        review_sample_path=review_sample_path,
        report_path=report_path,
        limit=None,
    )

    mentions = pd.read_parquet(out_path)
    profiles = pd.read_parquet(cited_title_profiles_path)
    graph = pd.read_parquet(graph_path)
    strict = pd.read_parquet(strict_path)
    broad = pd.read_parquet(broad_path)
    report = report_path.read_text(encoding="utf-8")

    assert metrics["total_context_rows_processed"] == 10
    assert "total_context_rows_processed" in report
    assert "contexts_with_any_object_mention" in report
    assert "graph_eligible" in mentions.columns
    assert "phase1_feature_eligible" in mentions.columns
    assert "graph_candidate_level" in mentions.columns
    assert not graph["object_category"].eq("generic_metric").any()
    assert not graph["object_id"].isin(["obj_accuracy", "obj_f1", "obj_perplexity"]).any()
    assert not mentions["matched_in"].eq("resolved_cited_title").any()
    assert not graph["matched_in"].eq("resolved_cited_title").any()
    assert set(strict["matched_in"]) <= {"sentence_text"}
    assert set(broad["matched_in"]) <= {"context_window_neighbor"}
    assert profiles["matched_in"].eq("resolved_cited_title").any()
    assert metrics["deduplicated_count"] >= 1

    ptb_cue = mentions.loc[
        mentions["context_id"].eq("ctx_ptb_cue") & mentions["surface_form"].eq("PTB")
    ].iloc[0]
    ptb_no_cue = mentions.loc[
        mentions["context_id"].eq("ctx_ptb_no_cue") & mentions["surface_form"].eq("PTB")
    ].iloc[0]
    lower_transformer = mentions.loc[
        mentions["context_id"].eq("ctx_lower_transformer")
    ].iloc[0]

    assert bool(ptb_cue["graph_eligible"])
    assert not bool(ptb_no_cue["graph_eligible"])
    assert not bool(lower_transformer["graph_eligible"])


def test_seed_registry_loads() -> None:
    registry = load_object_registry("configs/object_registry_seed.yaml")

    assert {entry.canonical_name for entry in registry} >= {"BERT", "BLEU", "SQuAD"}
