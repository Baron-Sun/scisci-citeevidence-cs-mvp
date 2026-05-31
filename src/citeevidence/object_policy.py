from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

DEFAULT_OBJECT_MENTIONS_REFINED_PATH = Path(
    "data/processed/object_mentions_sample_refined.parquet"
)
DEFAULT_CITED_TITLE_OBJECT_PROFILES_REFINED_PATH = Path(
    "data/processed/cited_title_object_profiles_sample.parquet"
)
DEFAULT_OBJECT_MENTIONS_LLM_REVIEW_PATH = Path(
    "data/processed/object_mentions_llm_review_results.parquet"
)
DEFAULT_OBJECT_MENTIONS_FINAL_PATH = Path("data/processed/object_mentions_sample_final.parquet")
DEFAULT_CITED_TITLE_OBJECT_PROFILES_FINAL_PATH = Path(
    "data/processed/cited_title_object_profiles_sample_final.parquet"
)
DEFAULT_OBJECT_GRAPH_CANDIDATES_PATH = Path(
    "data/processed/object_graph_candidate_mentions_sample.parquet"
)
DEFAULT_OBJECT_REGISTRY_POLICY_REPORT = Path("reports/object_registry_policy_update_report.md")
DEFAULT_OBJECT_MATCHING_FINAL_REPORT = Path("reports/object_matching_sample_final_report.md")

GENERIC_METRIC_IDS = {"obj_accuracy", "obj_f1", "obj_perplexity"}
NAMED_METRIC_IDS = {"obj_bleu", "obj_rouge", "obj_meteor"}
PTB_OBJECT_ID = "obj_penn_treebank"
TRANSFORMER_OBJECT_ID = "obj_transformer"
SEQ2SEQ_OBJECT_ID = "obj_seq2seq"

PTB_CUES = (
    "Penn Treebank",
    "Penn Tree Bank",
    "Wall Street Journal",
    "WSJ",
    "treebank",
    "corpus",
    "sections 02-21",
    "sections 2-21",
    "dataset",
)
TRANSFORMER_CUES = (
    "Vaswani",
    "self-attention",
    "Transformer model",
    "Transformer architecture",
    "encoder-decoder architecture",
)
SEQ2SEQ_CUES = (
    "model",
    "architecture",
    "encoder-decoder",
    "encoder decoder",
    "sequence-to-sequence",
    "sequence to sequence",
    "neural",
)

ORIGINAL_MENTION_COLUMNS = [
    "context_id",
    "source_context_id",
    "citing_paper_id",
    "resolved_cited_acl_id",
    "resolved_cited_title",
    "normalized_section",
    "raw_section_name",
    "object_id",
    "canonical_name",
    "object_type",
    "object_category",
    "surface_form",
    "normalized_surface",
    "match_type",
    "char_start",
    "char_end",
    "confidence",
    "matched_in",
    "match_policy",
    "allow_in_object_graph",
    "provenance",
]
LLM_POLICY_COLUMNS = [
    "llm_review_status",
    "llm_reviewer_correct",
    "llm_surface_form_refers_to_object",
    "llm_should_allow_in_object_graph",
    "llm_should_use_as_phase1_feature",
    "llm_error_type",
    "llm_recommended_action",
    "llm_evidence_quote",
    "llm_rationale_short",
]
FINAL_POLICY_COLUMNS = [
    *ORIGINAL_MENTION_COLUMNS,
    "original_allow_in_object_graph",
    *LLM_POLICY_COLUMNS,
    "mention_correct",
    "graph_eligible",
    "phase1_feature_eligible",
    "graph_candidate_level",
    "policy_reason",
]


def apply_object_review_policy(
    *,
    object_mentions_path: str | Path = DEFAULT_OBJECT_MENTIONS_REFINED_PATH,
    cited_title_profiles_path: str | Path = DEFAULT_CITED_TITLE_OBJECT_PROFILES_REFINED_PATH,
    llm_review_path: str | Path = DEFAULT_OBJECT_MENTIONS_LLM_REVIEW_PATH,
    registry_path: str | Path,
    out_mentions: str | Path = DEFAULT_OBJECT_MENTIONS_FINAL_PATH,
    out_title_profiles: str | Path = DEFAULT_CITED_TITLE_OBJECT_PROFILES_FINAL_PATH,
    out_graph_candidates: str | Path = DEFAULT_OBJECT_GRAPH_CANDIDATES_PATH,
    policy_report: str | Path = DEFAULT_OBJECT_REGISTRY_POLICY_REPORT,
    report: str | Path = DEFAULT_OBJECT_MATCHING_FINAL_REPORT,
) -> dict[str, Any]:
    """Apply final object matching policies informed by LLM-as-judge review."""
    for path in (
        Path(object_mentions_path),
        Path(cited_title_profiles_path),
        Path(llm_review_path),
        Path(registry_path),
    ):
        if not path.exists():
            raise FileNotFoundError(f"Required input does not exist: {path}")

    mentions = _ensure_columns(pd.read_parquet(object_mentions_path), ORIGINAL_MENTION_COLUMNS)
    title_profiles = _ensure_columns(
        pd.read_parquet(cited_title_profiles_path),
        ORIGINAL_MENTION_COLUMNS,
    )
    llm_review = pd.read_parquet(llm_review_path)

    final_mentions = apply_final_policy_to_mentions(
        mentions=mentions,
        llm_review=llm_review,
        source_table="object_mentions",
        force_title_profile_policy=False,
    )
    final_title_profiles = apply_final_policy_to_mentions(
        mentions=title_profiles,
        llm_review=llm_review,
        source_table="cited_title_object_profiles",
        force_title_profile_policy=True,
    )
    graph_candidates = build_object_graph_candidates(final_mentions)

    for output_path, frame in (
        (Path(out_mentions), final_mentions),
        (Path(out_title_profiles), final_title_profiles),
        (Path(out_graph_candidates), graph_candidates),
    ):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        frame.to_parquet(output_path, index=False)

    metrics = build_final_policy_metrics(
        final_mentions=final_mentions,
        final_title_profiles=final_title_profiles,
        graph_candidates=graph_candidates,
        llm_review=llm_review,
    )

    policy_report_path = Path(policy_report)
    policy_report_path.parent.mkdir(parents=True, exist_ok=True)
    policy_report_path.write_text(
        build_object_registry_policy_update_report(
            metrics=metrics,
            registry_path=Path(registry_path),
            llm_review_path=Path(llm_review_path),
        ),
        encoding="utf-8",
    )

    report_path = Path(report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        build_object_matching_final_report(
            metrics=metrics,
            final_mentions=final_mentions,
            final_title_profiles=final_title_profiles,
            graph_candidates=graph_candidates,
            out_mentions=Path(out_mentions),
            out_title_profiles=Path(out_title_profiles),
            out_graph_candidates=Path(out_graph_candidates),
        ),
        encoding="utf-8",
    )
    return metrics


def apply_final_policy_to_mentions(
    *,
    mentions: pd.DataFrame,
    llm_review: pd.DataFrame,
    source_table: str,
    force_title_profile_policy: bool = False,
) -> pd.DataFrame:
    """Add final policy fields to mention rows."""
    base = _ensure_columns(mentions.copy(), ORIGINAL_MENTION_COLUMNS)
    merged = _merge_llm_review_signals(base, llm_review, source_table=source_table)
    records = []
    for row in merged.to_dict(orient="records"):
        updated = _apply_row_policy(row, force_title_profile_policy=force_title_profile_policy)
        records.append(updated)
    final = pd.DataFrame(records)
    final = _ensure_columns(final, FINAL_POLICY_COLUMNS)
    return _normalize_final_column_types(final[FINAL_POLICY_COLUMNS])


def build_object_graph_candidates(final_mentions: pd.DataFrame) -> pd.DataFrame:
    """Return strict and broad object graph candidate mentions."""
    if final_mentions.empty:
        return final_mentions.head(0).copy()
    candidates = final_mentions.loc[
        final_mentions["graph_candidate_level"].isin(["strict", "broad"])
    ]
    return candidates.reset_index(drop=True)


def build_final_policy_metrics(
    *,
    final_mentions: pd.DataFrame,
    final_title_profiles: pd.DataFrame,
    graph_candidates: pd.DataFrame,
    llm_review: pd.DataFrame,
) -> dict[str, Any]:
    """Build metrics used by the policy and final matching reports."""
    return {
        "input_mentions": int(len(final_mentions)),
        "final_mentions": int(len(final_mentions)),
        "cited_title_profile_count": int(len(final_title_profiles)),
        "graph_candidates": int(len(graph_candidates)),
        "graph_eligible_count": _true_count(final_mentions, "graph_eligible"),
        "phase1_feature_eligible_count": _true_count(final_mentions, "phase1_feature_eligible"),
        "strict_graph_candidate_count": int(
            final_mentions["graph_candidate_level"].eq("strict").sum()
        ),
        "broad_graph_candidate_count": int(
            final_mentions["graph_candidate_level"].eq("broad").sum()
        ),
        "mention_correct_distribution": _value_counts(
            final_mentions,
            ["mention_correct"],
            "mentions",
        ),
        "graph_eligible_distribution": _value_counts(
            final_mentions,
            ["graph_eligible"],
            "mentions",
        ),
        "phase1_feature_distribution": _value_counts(
            final_mentions,
            ["phase1_feature_eligible"],
            "mentions",
        ),
        "graph_candidate_level_distribution": _value_counts(
            final_mentions,
            ["graph_candidate_level"],
            "mentions",
        ),
        "mentions_by_object_category": _value_counts(
            final_mentions,
            ["object_category"],
            "mentions",
        ),
        "top_named_objects": _value_counts(
            final_mentions.loc[final_mentions["object_category"].eq("named_object")],
            ["object_id", "canonical_name", "object_type"],
            "mentions",
            limit=30,
        ),
        "top_generic_metrics": _value_counts(
            final_mentions.loc[final_mentions["object_category"].eq("generic_metric")],
            ["object_id", "canonical_name", "surface_form"],
            "mentions",
            limit=20,
        ),
        "top_ambiguous_aliases": _value_counts(
            final_mentions.loc[final_mentions["object_category"].eq("ambiguous_short_alias")],
            ["object_id", "canonical_name", "surface_form", "policy_reason"],
            "mentions",
            limit=20,
        ),
        "llm_recommended_actions": _value_counts(
            llm_review,
            ["recommended_action"],
            "rows",
        ),
        "llm_error_types": _value_counts(llm_review, ["error_type"], "rows"),
        "object_graph_eligibility_changes": _value_counts(
            final_mentions,
            ["original_allow_in_object_graph", "graph_eligible"],
            "mentions",
        ),
    }


def build_object_registry_policy_update_report(
    *,
    metrics: dict[str, Any],
    registry_path: Path,
    llm_review_path: Path,
) -> str:
    """Build the registry and policy update report."""
    updated = pd.DataFrame(
        [
            {
                "object_or_group": "accuracy / F1 / perplexity",
                "policy_update": "generic_metric; feature-only; excluded from object graph",
            },
            {
                "object_or_group": "Penn Treebank / PTB",
                "policy_update": "PTB requires nearby treebank/corpus/WSJ/dataset cues",
            },
            {
                "object_or_group": "Transformer",
                "policy_update": "lowercase transformer defaults to generic_architecture",
            },
            {
                "object_or_group": "seq2seq",
                "policy_update": "lower confidence and require model/architecture cues",
            },
            {
                "object_or_group": "WordNet",
                "policy_update": "kept globally; graph eligibility remains context dependent",
            },
            {
                "object_or_group": "BLEU / ROUGE / METEOR",
                "policy_update": "kept as named metrics eligible for graph use",
            },
            {
                "object_or_group": "resolved_cited_title profiles",
                "policy_update": "kept separate from direct context object evidence",
            },
        ]
    )
    cue_table = pd.DataFrame(
        [
            {"object": "PTB", "cues": "; ".join(PTB_CUES)},
            {"object": "lowercase transformer", "cues": "; ".join(TRANSFORMER_CUES)},
            {"object": "seq2seq", "cues": "; ".join(SEQ2SEQ_CUES)},
        ]
    )
    sections = [
        "# Object Registry Policy Update Report",
        "",
        "## Inputs",
        f"- Registry: `{registry_path}`",
        f"- LLM-as-judge review: `{llm_review_path}`",
        "",
        "## Registry Objects Updated",
        _table(updated),
        "",
        "## Aliases Requiring Context Cue",
        _table(cue_table),
        "",
        "## Generic Metrics Kept Feature-Only",
        "accuracy, F1, and perplexity are retained as phase-1 citation-function "
        "features and excluded from object graph candidates.",
        "",
        "## Object Graph Eligibility Changes",
        _table(metrics["object_graph_eligibility_changes"]),
        "",
        "## LLM Review Signals Used",
        "The policy uses `surface_form_refers_to_object` as the primary mention "
        "correctness signal when available, falling back to `reviewer_correct`. "
        "Graph and feature eligibility use `should_allow_in_object_graph`, "
        "`should_use_as_phase1_feature`, `recommended_action`, and `error_type` "
        "as advisory signals under the deterministic policy.",
        "",
        "### Recommended Action Counts",
        _table(metrics["llm_recommended_actions"]),
        "",
        "### Error Type Counts",
        _table(metrics["llm_error_types"]),
        "",
    ]
    return "\n".join(sections)


def build_object_matching_final_report(
    *,
    metrics: dict[str, Any],
    final_mentions: pd.DataFrame,
    final_title_profiles: pd.DataFrame,
    graph_candidates: pd.DataFrame,
    out_mentions: Path,
    out_title_profiles: Path,
    out_graph_candidates: Path,
) -> str:
    """Build final object matching sample report."""
    core = pd.DataFrame(
        [
            {"metric": "input contexts", "value": final_mentions["context_id"].nunique()},
            {"metric": "mentions after final policy", "value": metrics["final_mentions"]},
            {
                "metric": "cited title profile count",
                "value": metrics["cited_title_profile_count"],
            },
            {"metric": "graph eligible count", "value": metrics["graph_eligible_count"]},
            {
                "metric": "phase1 feature eligible count",
                "value": metrics["phase1_feature_eligible_count"],
            },
            {
                "metric": "strict graph candidate count",
                "value": metrics["strict_graph_candidate_count"],
            },
            {
                "metric": "broad graph candidate count",
                "value": metrics["broad_graph_candidate_count"],
            },
            {"metric": "graph candidate rows", "value": metrics["graph_candidates"]},
        ]
    )
    excluded_feature = final_mentions.loc[
        (~final_mentions["graph_eligible"].map(_bool_value))
        & final_mentions["phase1_feature_eligible"].map(_bool_value)
    ]
    sections = [
        "# Object Matching Sample Final Report",
        "",
        "## Outputs",
        f"- Final mentions: `{out_mentions}`",
        f"- Final cited-title profiles: `{out_title_profiles}`",
        f"- Object graph candidates: `{out_graph_candidates}`",
        "",
        "## Core Metrics",
        _table(core),
        "",
        "## Mention Correct Distribution",
        _table(metrics["mention_correct_distribution"]),
        "",
        "## Graph Eligible Distribution",
        _table(metrics["graph_eligible_distribution"]),
        "",
        "## Phase-1 Feature Eligible Distribution",
        _table(metrics["phase1_feature_distribution"]),
        "",
        "## Graph Candidate Level Distribution",
        _table(metrics["graph_candidate_level_distribution"]),
        "",
        "## Mentions By Object Category",
        _table(metrics["mentions_by_object_category"]),
        "",
        "## Top Named Objects",
        _table(metrics["top_named_objects"]),
        "",
        "## Top Generic Metrics",
        _table(metrics["top_generic_metrics"]),
        "",
        "## Top Ambiguous Aliases",
        _table(metrics["top_ambiguous_aliases"]),
        "",
        "## PTB Examples After Policy",
        _table(_object_examples(final_mentions, PTB_OBJECT_ID, 20)),
        "",
        "## Transformer Examples After Policy",
        _table(_object_examples(final_mentions, TRANSFORMER_OBJECT_ID, 20)),
        "",
        "## seq2seq Examples After Policy",
        _table(_object_examples(final_mentions, SEQ2SEQ_OBJECT_ID, 20)),
        "",
        "## Examples Excluded From Graph But Kept As Features",
        _table(_policy_examples(excluded_feature, 25)),
        "",
        "## Graph Candidate Examples",
        _table(_policy_examples(graph_candidates, 25)),
        "",
        "## Cited Title Profiles Remain Separate",
        _table(_policy_examples(final_title_profiles, 15)),
        "",
    ]
    return "\n".join(sections)


def _merge_llm_review_signals(
    mentions: pd.DataFrame,
    llm_review: pd.DataFrame,
    *,
    source_table: str,
) -> pd.DataFrame:
    frame = mentions.copy()
    key_columns = ["context_id", "source_context_id", "object_id", "surface_form", "matched_in"]
    review_columns = [
        *key_columns,
        "source_table",
        "review_status",
        "reviewer_correct",
        "surface_form_refers_to_object",
        "should_allow_in_object_graph",
        "should_use_as_phase1_feature",
        "error_type",
        "recommended_action",
        "evidence_quote",
        "rationale_short",
        "sentence_text",
        "context_window_s3",
    ]
    review = _ensure_columns(llm_review.copy(), review_columns)
    review = review.loc[review["source_table"].fillna("").astype(str).eq(source_table)]
    if review.empty:
        for column in LLM_POLICY_COLUMNS:
            frame[column] = ""
        return frame
    review = review.drop_duplicates(subset=key_columns, keep="last")
    review = review.rename(
        columns={
            "review_status": "llm_review_status",
            "reviewer_correct": "llm_reviewer_correct",
            "surface_form_refers_to_object": "llm_surface_form_refers_to_object",
            "should_allow_in_object_graph": "llm_should_allow_in_object_graph",
            "should_use_as_phase1_feature": "llm_should_use_as_phase1_feature",
            "error_type": "llm_error_type",
            "recommended_action": "llm_recommended_action",
            "evidence_quote": "llm_evidence_quote",
            "rationale_short": "llm_rationale_short",
            "sentence_text": "_llm_sentence_text",
            "context_window_s3": "_llm_context_window_s3",
        }
    )
    merged = frame.merge(
        review[
            [
                *key_columns,
                *LLM_POLICY_COLUMNS,
                "_llm_sentence_text",
                "_llm_context_window_s3",
            ]
        ],
        on=key_columns,
        how="left",
    )
    for column in LLM_POLICY_COLUMNS:
        merged[column] = merged[column].fillna("")
    return merged


def _apply_row_policy(
    row: dict[str, Any],
    *,
    force_title_profile_policy: bool,
) -> dict[str, Any]:
    updated = row.copy()
    reasons: list[str] = []
    confidence = float(row.get("confidence") or 0)
    object_id = _clean(row.get("object_id"))
    surface = _clean(row.get("surface_form"))
    matched_in = _clean(row.get("matched_in"))
    mention_correct = _mention_correct(row)
    graph_eligible = _bool_value(row.get("allow_in_object_graph"))
    phase1_feature = mention_correct != "false"
    object_category = _clean(row.get("object_category"))
    match_policy = _clean(row.get("match_policy"))

    llm_should_graph = _optional_bool(row.get("llm_should_allow_in_object_graph"))
    if llm_should_graph is not None:
        graph_eligible = llm_should_graph
        reasons.append("llm_graph_signal")
    llm_should_feature = _optional_bool(row.get("llm_should_use_as_phase1_feature"))
    if llm_should_feature is not None:
        phase1_feature = llm_should_feature
        reasons.append("llm_phase1_signal")

    if mention_correct == "false":
        graph_eligible = False
        if llm_should_feature is None:
            phase1_feature = False
        reasons.append("mention_not_correct")

    if object_id in GENERIC_METRIC_IDS or object_category == "generic_metric":
        object_category = "generic_metric"
        graph_eligible = False
        phase1_feature = True
        reasons.append("generic_metric_feature_only")

    if object_id == PTB_OBJECT_ID and _normalized(surface) == "ptb":
        if _has_cue(row, PTB_CUES) or "context_cue_present" in match_policy:
            graph_eligible = mention_correct != "false"
            object_category = "named_object"
            match_policy = _append_policy(match_policy, "context_cue_present")
            confidence = max(confidence, 0.85)
            reasons.append("ptb_context_cue_present")
        else:
            graph_eligible = False
            phase1_feature = mention_correct != "false" and confidence >= 0.50
            object_category = "ambiguous_short_alias"
            match_policy = _append_policy(match_policy, "require_context_cue")
            confidence = min(confidence, 0.50)
            reasons.append("ptb_context_cue_missing")

    if object_id == TRANSFORMER_OBJECT_ID and _is_lowercase_transformer(surface):
        if _has_cue(row, TRANSFORMER_CUES):
            graph_eligible = mention_correct != "false"
            object_category = "named_object"
            confidence = max(confidence, 0.85)
            match_policy = _append_policy(match_policy, "lowercase_context_cue_present")
            reasons.append("lowercase_transformer_context_cue_present")
        else:
            graph_eligible = False
            phase1_feature = mention_correct != "false"
            object_category = "generic_architecture"
            confidence = min(confidence, 0.65)
            match_policy = _append_policy(match_policy, "lowercase_generic_architecture")
            reasons.append("lowercase_transformer_feature_only")

    if object_id == SEQ2SEQ_OBJECT_ID:
        confidence = min(confidence, 0.85)
        if _has_cue(row, SEQ2SEQ_CUES) or "context_cue_present" in match_policy:
            object_category = "named_object"
            graph_eligible = mention_correct != "false" and graph_eligible
            match_policy = _append_policy(match_policy, "context_cue_present")
            reasons.append("seq2seq_context_cue_present")
        else:
            graph_eligible = False
            phase1_feature = mention_correct != "false" and confidence >= 0.50
            match_policy = _append_policy(match_policy, "require_context_cue")
            reasons.append("seq2seq_context_cue_missing")

    if object_id in NAMED_METRIC_IDS and mention_correct != "false":
        object_category = "named_object"
        if llm_should_graph is None:
            graph_eligible = True
        reasons.append("named_metric_graph_eligible")

    if force_title_profile_policy or matched_in == "resolved_cited_title":
        graph_eligible = False
        phase1_feature = False
        reasons.append("resolved_cited_title_profile_not_direct_context_evidence")

    graph_candidate_level = _graph_candidate_level(
        mention_correct=mention_correct,
        graph_eligible=graph_eligible,
        object_category=object_category,
        confidence=confidence,
        matched_in=matched_in,
    )

    updated["object_category"] = object_category
    updated["confidence"] = round(confidence, 3)
    updated["match_policy"] = match_policy
    updated["original_allow_in_object_graph"] = _bool_value(row.get("allow_in_object_graph"))
    updated["allow_in_object_graph"] = bool(graph_eligible)
    updated["mention_correct"] = mention_correct
    updated["graph_eligible"] = bool(graph_eligible)
    updated["phase1_feature_eligible"] = bool(phase1_feature)
    updated["graph_candidate_level"] = graph_candidate_level
    updated["policy_reason"] = ";".join(_unique_preserve_order(reasons)) or "default_policy"
    return updated


def _mention_correct(row: dict[str, Any]) -> str:
    surface_signal = _clean(row.get("llm_surface_form_refers_to_object")).lower()
    if surface_signal in {"true", "false", "unclear"}:
        return surface_signal
    reviewer_signal = _clean(row.get("llm_reviewer_correct")).lower()
    if reviewer_signal in {"true", "false", "unclear"}:
        return reviewer_signal
    return "unreviewed"


def _graph_candidate_level(
    *,
    mention_correct: str,
    graph_eligible: bool,
    object_category: str,
    confidence: float,
    matched_in: str,
) -> str:
    if mention_correct == "false" or not graph_eligible:
        return "none"
    if object_category != "named_object" or confidence < 0.85:
        return "none"
    if matched_in == "sentence_text":
        return "strict"
    if matched_in == "context_window_neighbor":
        return "broad"
    return "none"


def _has_cue(row: dict[str, Any], cues: tuple[str, ...]) -> bool:
    text = " ".join(
        [
            _clean(row.get("sentence_text")),
            _clean(row.get("context_window_s3")),
            _clean(row.get("_llm_sentence_text")),
            _clean(row.get("_llm_context_window_s3")),
            _clean(row.get("llm_evidence_quote")),
        ]
    ).lower()
    return any(cue.lower() in text for cue in cues)


def _is_lowercase_transformer(surface: str) -> bool:
    return _normalized(surface) in {"transformer", "transformers"} and surface[:1].islower()


def _append_policy(current: str, policy: str) -> str:
    pieces = [piece for piece in current.split(";") if piece]
    pieces.append(policy)
    return ";".join(_unique_preserve_order(pieces))


def _object_examples(frame: pd.DataFrame, object_id: str, limit: int) -> pd.DataFrame:
    return _policy_examples(frame.loc[frame["object_id"].eq(object_id)], limit)


def _policy_examples(frame: pd.DataFrame, limit: int) -> pd.DataFrame:
    columns = [
        "context_id",
        "canonical_name",
        "object_category",
        "surface_form",
        "confidence",
        "matched_in",
        "mention_correct",
        "graph_eligible",
        "phase1_feature_eligible",
        "graph_candidate_level",
        "policy_reason",
        "match_policy",
    ]
    if frame.empty:
        return pd.DataFrame(columns=columns)
    sample = _ensure_columns(frame.head(limit).copy(), columns)
    return sample[columns]


def _ensure_columns(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        if column not in frame.columns:
            frame[column] = ""
    return frame


def _normalize_final_column_types(frame: pd.DataFrame) -> pd.DataFrame:
    normalized = frame.copy()
    bool_columns = [
        "allow_in_object_graph",
        "original_allow_in_object_graph",
        "graph_eligible",
        "phase1_feature_eligible",
    ]
    for column in bool_columns:
        normalized[column] = normalized[column].map(_bool_value)
    for column in ["confidence"]:
        normalized[column] = pd.to_numeric(normalized[column], errors="coerce").fillna(0.0)
    for column in ["char_start", "char_end"]:
        normalized[column] = (
            pd.to_numeric(normalized[column], errors="coerce").fillna(-1).astype(int)
        )
    non_text_columns = {*bool_columns, "confidence", "char_start", "char_end"}
    text_columns = [column for column in normalized.columns if column not in non_text_columns]
    for column in text_columns:
        normalized[column] = normalized[column].map(_clean)
    return normalized


def _true_count(frame: pd.DataFrame, column: str) -> int:
    if column not in frame:
        return 0
    return int(frame[column].map(_bool_value).sum())


def _optional_bool(value: Any) -> bool | None:
    if value is None or pd.isna(value):
        return None
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"true", "1", "yes"}:
        return True
    if text in {"false", "0", "no"}:
        return False
    return None


def _bool_value(value: Any) -> bool:
    result = _optional_bool(value)
    return bool(result) if result is not None else False


def _clean(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


def _normalized(value: Any) -> str:
    return " ".join(_clean(value).lower().replace("-", " ").split())


def _unique_preserve_order(values: list[str]) -> list[str]:
    seen = set()
    output = []
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


def _value_counts(
    frame: pd.DataFrame,
    columns: list[str],
    count_name: str,
    limit: int | None = None,
) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(columns=[*columns, count_name])
    filled = frame.copy()
    for column in columns:
        if column not in filled:
            filled[column] = "unavailable"
        filled[column] = filled[column].fillna("unavailable").astype(str)
        filled.loc[filled[column].str.strip().eq(""), column] = "blank"
    counts = (
        filled.groupby(columns, dropna=False)
        .size()
        .reset_index(name=count_name)
        .sort_values([count_name, *columns], ascending=[False, *([True] * len(columns))])
    )
    return counts.head(limit) if limit else counts


def _table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "No records available."
    columns = list(frame.columns)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in frame.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(_markdown_cell(value) for value in row) + " |")
    return "\n".join(lines)


def _markdown_cell(value: Any) -> str:
    if value is None or pd.isna(value):
        return "unavailable"
    return str(value).replace("|", "\\|").replace("\n", " ")
