from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Literal

import pandas as pd
import pyarrow.parquet as pq
from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator

from citeevidence.objects import (
    DEFAULT_CITED_TITLE_OBJECT_PROFILES_SAMPLE_PATH,
    DEFAULT_OBJECT_MENTIONS_SAMPLE_PATH,
    DEFAULT_OBJECT_REGISTRY_PATH,
    ObjectRegistryEntry,
    load_object_registry,
)

DEFAULT_LLM_OBJECT_REVIEW_SAMPLE_PATH = Path(
    "data/processed/object_mentions_llm_review_sample.csv"
)
DEFAULT_LLM_OBJECT_REVIEW_JSONL_PATH = Path(
    "data/processed/object_mentions_llm_review_results.jsonl"
)
DEFAULT_LLM_OBJECT_REVIEW_PARQUET_PATH = Path(
    "data/processed/object_mentions_llm_review_results.parquet"
)
DEFAULT_LLM_OBJECT_REVIEW_REPORT = Path("reports/object_mentions_llm_review_report.md")
DEFAULT_LLM_OBJECT_REVIEW_CACHE_DIR = Path("data/cache/llm_object_review")
DEFAULT_ANALYSIS_READY_CONTEXTS_PATH = Path(
    "data/processed/analysis_ready_strong_contexts.parquet"
)
DEFAULT_OPENAI_REVIEW_MODEL = "gpt-4o-mini"
LLM_OBJECT_REVIEW_PROMPT_VERSION = "object_mentions_llm_review_v1"

REVIEW_BOOL = Literal["true", "false", "unclear"]
ERROR_TYPES = Literal[
    "none",
    "alias_too_generic",
    "wrong_object_type",
    "matched_unrelated_word",
    "context_neighbor_not_relevant",
    "title_profile_only_not_context_use",
    "ambiguous_short_alias",
    "case_sensitive_issue",
    "correct_but_not_graph_object",
    "insufficient_context",
    "other",
]
RECOMMENDED_ACTIONS = Literal[
    "keep",
    "lower_confidence",
    "require_context_cue",
    "block_alias",
    "remove_alias",
    "change_object_type",
    "keep_as_feature_only",
    "other",
]

BASE_SAMPLE_QUOTAS = {
    "named_object_high_confidence": 60,
    "generic_metric": 40,
    "ambiguous_short_alias": 30,
    "generic_architecture": 30,
    "context_window_neighbor": 20,
    "cited_title_object_profiles": 20,
}

LLM_REVIEW_SAMPLE_COLUMNS = [
    "review_bucket",
    "source_table",
    "sample_row_id",
    "context_id",
    "source_context_id",
    "citing_paper_id",
    "resolved_cited_acl_id",
    "resolved_cited_title",
    "normalized_section",
    "raw_section_name",
    "sentence_text",
    "context_window_s3",
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
    "registry_notes",
    "registry_aliases",
    "registry_negative_aliases",
    "registry_require_context_cue",
    "prompt_version",
    "model",
    "cache_key",
]

LLM_REVIEW_RESULT_COLUMNS = [
    *LLM_REVIEW_SAMPLE_COLUMNS,
    "reviewer_correct",
    "object_type_correct",
    "surface_form_refers_to_object",
    "should_allow_in_object_graph",
    "should_use_as_phase1_feature",
    "error_type",
    "recommended_action",
    "llm_confidence",
    "evidence_quote",
    "rationale_short",
    "review_status",
    "validation_error",
    "attempts",
    "from_cache",
    "model_used",
    "input_tokens",
    "output_tokens",
    "total_tokens",
]


class LLMObjectReviewDecision(BaseModel):
    reviewer_correct: REVIEW_BOOL
    object_type_correct: REVIEW_BOOL
    surface_form_refers_to_object: REVIEW_BOOL
    should_allow_in_object_graph: bool
    should_use_as_phase1_feature: bool
    error_type: ERROR_TYPES
    recommended_action: RECOMMENDED_ACTIONS
    confidence: float = Field(ge=0, le=1)
    evidence_quote: str
    rationale_short: str

    @field_validator("evidence_quote", "rationale_short")
    @classmethod
    def _strip_text(cls, value: str) -> str:
        return value.strip()

    @model_validator(mode="after")
    def _false_requires_error_type(self) -> LLMObjectReviewDecision:
        if self.reviewer_correct == "false" and self.error_type == "none":
            raise ValueError("reviewer_correct=false requires error_type != none")
        return self


def run_llm_object_review(
    *,
    object_mentions_path: str | Path = DEFAULT_OBJECT_MENTIONS_SAMPLE_PATH,
    cited_title_profiles_path: str | Path = DEFAULT_CITED_TITLE_OBJECT_PROFILES_SAMPLE_PATH,
    contexts_path: str | Path = DEFAULT_ANALYSIS_READY_CONTEXTS_PATH,
    registry_path: str | Path = DEFAULT_OBJECT_REGISTRY_PATH,
    sample_out: str | Path = DEFAULT_LLM_OBJECT_REVIEW_SAMPLE_PATH,
    jsonl_out: str | Path = DEFAULT_LLM_OBJECT_REVIEW_JSONL_PATH,
    parquet_out: str | Path = DEFAULT_LLM_OBJECT_REVIEW_PARQUET_PATH,
    report_path: str | Path = DEFAULT_LLM_OBJECT_REVIEW_REPORT,
    cache_dir: str | Path = DEFAULT_LLM_OBJECT_REVIEW_CACHE_DIR,
    limit: int = 200,
    model: str | None = None,
    seed: int = 42,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Run or dry-run LLM-as-judge review for object mention samples."""
    if limit < 1:
        raise ValueError("limit must be positive")
    review_model = resolve_review_model(model)
    for path in (
        Path(object_mentions_path),
        Path(cited_title_profiles_path),
        Path(contexts_path),
        Path(registry_path),
    ):
        if not path.exists():
            raise FileNotFoundError(f"Required input does not exist: {path}")

    object_mentions = _read_parquet_with_columns(
        Path(object_mentions_path),
        _object_input_columns(),
    )
    cited_title_profiles = _read_parquet_with_columns(
        Path(cited_title_profiles_path),
        _object_input_columns(),
    )
    contexts = _read_parquet_with_columns(Path(contexts_path), _context_input_columns())
    registry = load_object_registry(registry_path)
    sample = build_llm_object_review_sample(
        object_mentions=object_mentions,
        cited_title_profiles=cited_title_profiles,
        contexts=contexts,
        registry=registry,
        limit=limit,
        seed=seed,
        model=review_model,
    )

    sample_output = Path(sample_out)
    sample_output.parent.mkdir(parents=True, exist_ok=True)
    sample.to_csv(sample_output, index=False)

    jsonl_output = Path(jsonl_out)
    parquet_output = Path(parquet_out)
    report_output = Path(report_path)
    for output_path in (jsonl_output, parquet_output, report_output):
        output_path.parent.mkdir(parents=True, exist_ok=True)

    if dry_run:
        dry_run_records = _write_dry_run_prompts(sample, jsonl_output)
        results = pd.DataFrame(columns=LLM_REVIEW_RESULT_COLUMNS)
        results.to_parquet(parquet_output, index=False)
        metrics = build_llm_review_metrics(
            sample=sample,
            results=results,
            dry_run=True,
            dry_run_prompt_records=dry_run_records,
        )
        report_output.write_text(
            build_llm_review_report(
                sample=sample,
                results=results,
                metrics=metrics,
                sample_out=sample_output,
                jsonl_out=jsonl_output,
                parquet_out=parquet_output,
                dry_run=True,
            ),
            encoding="utf-8",
        )
        return metrics

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required unless --dry-run is set")

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    cache_path = Path(cache_dir)
    cache_path.mkdir(parents=True, exist_ok=True)
    result_records: list[dict[str, Any]] = []
    with jsonl_output.open("w", encoding="utf-8") as handle:
        for row in sample.to_dict(orient="records"):
            record = review_sample_row(
                row=row,
                client=client,
                model=review_model,
                cache_dir=cache_path,
            )
            result_records.append(record)
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    results = pd.DataFrame(result_records)
    results = _ensure_columns(results, LLM_REVIEW_RESULT_COLUMNS)
    results[LLM_REVIEW_RESULT_COLUMNS].to_parquet(parquet_output, index=False)
    metrics = build_llm_review_metrics(sample=sample, results=results, dry_run=False)
    report_output.write_text(
        build_llm_review_report(
            sample=sample,
            results=results,
            metrics=metrics,
            sample_out=sample_output,
            jsonl_out=jsonl_output,
            parquet_out=parquet_output,
            dry_run=False,
        ),
        encoding="utf-8",
    )
    return metrics


def resolve_review_model(model: str | None = None) -> str:
    """Resolve review model from CLI value, environment, or the single project default."""
    cli_value = (model or "").strip()
    if cli_value:
        return cli_value
    env_value = os.getenv("OPENAI_REVIEW_MODEL", "").strip()
    return env_value or DEFAULT_OPENAI_REVIEW_MODEL


def build_llm_object_review_sample(
    *,
    object_mentions: pd.DataFrame,
    cited_title_profiles: pd.DataFrame,
    contexts: pd.DataFrame,
    registry: list[ObjectRegistryEntry],
    limit: int = 200,
    seed: int = 42,
    model: str = DEFAULT_OPENAI_REVIEW_MODEL,
) -> pd.DataFrame:
    """Build a deterministic stratified sample for LLM-as-judge review."""
    if limit < 1:
        raise ValueError("limit must be positive")
    mentions = _prepare_object_frame(object_mentions, source_table="object_mentions")
    profiles = _prepare_object_frame(
        cited_title_profiles,
        source_table="cited_title_object_profiles",
    )
    if not profiles.empty:
        profiles["matched_in"] = "resolved_cited_title"
        profiles["allow_in_object_graph"] = False

    buckets = [
        (
            "named_object_high_confidence",
            mentions.loc[
                mentions["object_category"].eq("named_object")
                & mentions["confidence"].fillna(0).astype(float).ge(0.85)
            ],
        ),
        (
            "generic_metric",
            mentions.loc[mentions["object_category"].eq("generic_metric")],
        ),
        (
            "ambiguous_short_alias",
            mentions.loc[mentions["object_category"].eq("ambiguous_short_alias")],
        ),
        (
            "generic_architecture",
            mentions.loc[mentions["object_category"].eq("generic_architecture")],
        ),
        (
            "context_window_neighbor",
            mentions.loc[mentions["matched_in"].eq("context_window_neighbor")],
        ),
        ("cited_title_object_profiles", profiles),
    ]
    quotas = _scaled_quotas(limit)
    selected_parts: list[pd.DataFrame] = []
    selected_keys: set[str] = set()
    for index, (bucket_name, bucket_frame) in enumerate(buckets):
        available = _drop_selected(bucket_frame, selected_keys)
        sample = _sample_frame(available, quotas[bucket_name], seed + index)
        if sample.empty:
            continue
        sample = sample.copy()
        sample["review_bucket"] = bucket_name
        selected_keys.update(sample["_sample_identity"].astype(str))
        selected_parts.append(sample)

    selected = (
        pd.concat(selected_parts, ignore_index=True)
        if selected_parts
        else pd.DataFrame(columns=[*mentions.columns, "review_bucket"])
    )
    if len(selected) < limit:
        fill_pool = _drop_selected(
            pd.concat([mentions, profiles], ignore_index=True),
            selected_keys,
        )
        fill = _sample_frame(fill_pool, limit - len(selected), seed + 99)
        if not fill.empty:
            fill = fill.copy()
            fill["review_bucket"] = "quota_fill"
            selected = pd.concat([selected, fill], ignore_index=True)

    selected = selected.head(limit).copy()
    selected = _attach_context_text(selected, contexts)
    selected = _attach_registry_notes(selected, registry)
    selected["prompt_version"] = LLM_OBJECT_REVIEW_PROMPT_VERSION
    selected["model"] = model
    selected["cache_key"] = selected.apply(
        lambda row: llm_object_review_cache_key(row.to_dict()),
        axis=1,
    )
    selected["sample_row_id"] = [
        f"llm_obj_review_{index:04d}" for index in range(1, len(selected) + 1)
    ]
    selected = _ensure_columns(selected, LLM_REVIEW_SAMPLE_COLUMNS)
    return selected[LLM_REVIEW_SAMPLE_COLUMNS]


def review_sample_row(
    *,
    row: dict[str, Any],
    client: Any,
    model: str,
    cache_dir: Path,
) -> dict[str, Any]:
    """Review one sampled object mention, using a local JSON cache when possible."""
    cache_key = llm_object_review_cache_key(row)
    cache_file = cache_dir / f"{cache_key}.json"
    if cache_file.exists():
        cached = json.loads(cache_file.read_text(encoding="utf-8"))
        cached["from_cache"] = True
        return cached

    validation_error = ""
    raw_response = ""
    usage: dict[str, int | None] = {}
    for attempt in range(1, 3):
        try:
            decision, raw_response, usage = call_openai_review_decision(
                client=client,
                row=row,
                model=model,
            )
            validate_review_decision(decision, row)
            record = _result_record_from_decision(
                row=row,
                decision=decision,
                review_status="reviewed",
                validation_error="",
                attempts=attempt,
                from_cache=False,
                model_used=model,
                usage=usage,
            )
            cache_file.write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")
            return record
        except (ValidationError, ValueError, json.JSONDecodeError) as exc:
            validation_error = str(exc)
        except Exception as exc:  # pragma: no cover - exercised only with live API failures.
            validation_error = f"{type(exc).__name__}: {exc}"

    fallback = fallback_unclear_record(
        row=row,
        model=model,
        validation_error=validation_error,
        raw_response=raw_response,
        usage=usage,
    )
    cache_file.write_text(json.dumps(fallback, ensure_ascii=False), encoding="utf-8")
    return fallback


def call_openai_review_decision(
    *,
    client: Any,
    row: dict[str, Any],
    model: str,
) -> tuple[LLMObjectReviewDecision, str, dict[str, int | None]]:
    """Call OpenAI Structured Outputs for one LLM-as-judge decision."""
    system_prompt, user_prompt = build_object_review_prompt(row)
    response = client.responses.parse(
        model=model,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        text_format=LLMObjectReviewDecision,
    )
    parsed = response.output_parsed
    if parsed is None:
        raw = getattr(response, "output_text", "")
        parsed = LLMObjectReviewDecision.model_validate_json(raw)
    raw_response = (
        parsed.model_dump_json() if isinstance(parsed, LLMObjectReviewDecision) else str(parsed)
    )
    return parsed, raw_response, _usage_to_dict(getattr(response, "usage", None))


def build_object_review_prompt(row: dict[str, Any]) -> tuple[str, str]:
    """Build the system/user prompt pair for one object mention review."""
    system_prompt = (
        "You are performing an LLM-as-judge review for citation evidence object "
        "mentions in NLP / Computational Linguistics papers. Return only the "
        "structured JSON object requested by the schema. Refer to this pass as "
        "LLM-as-judge review, model-based audit, or LLM-assisted validation. "
        "Judge whether the matched surface form truly refers to the registered "
        "object in the local citation context, and whether it should be allowed "
        "into an object graph."
    )
    payload = {
        "task": "model-based audit of one extracted object mention",
        "prompt_version": row.get("prompt_version", LLM_OBJECT_REVIEW_PROMPT_VERSION),
        "local_policy": [
            "Use only the provided sentence_text, context_window_s3, and "
            "resolved_cited_title as evidence.",
            "evidence_quote must be an exact substring of those fields unless "
            "reviewer_correct is unclear.",
            "generic_metric mentions such as accuracy, F1, and perplexity should "
            "usually be should_allow_in_object_graph=false and "
            "should_use_as_phase1_feature=true.",
            "resolved_cited_title-only matches should not enter the object graph "
            "unless the sentence or context window directly supports local use.",
            "PTB should enter the graph only when local evidence cues such as "
            "Penn Treebank, treebank, corpus, dataset, or WSJ disambiguate it.",
            "lowercase transformer should usually be treated as generic_architecture, "
            "not a graph object.",
            "For context_window_neighbor matches, verify that the neighbor text is "
            "actually relevant to the cited sentence.",
        ],
        "mention": _prompt_row_payload(row),
        "required_output_fields": [
            "reviewer_correct",
            "object_type_correct",
            "surface_form_refers_to_object",
            "should_allow_in_object_graph",
            "should_use_as_phase1_feature",
            "error_type",
            "recommended_action",
            "confidence",
            "evidence_quote",
            "rationale_short",
        ],
    }
    return system_prompt, json.dumps(payload, ensure_ascii=False, indent=2)


def llm_object_review_cache_key(row: dict[str, Any]) -> str:
    """Deterministic cache key for a sampled LLM object review row."""
    payload = {
        "context_id": _clean(row.get("context_id")),
        "object_id": _clean(row.get("object_id")),
        "surface_form": _clean(row.get("surface_form")),
        "matched_in": _clean(row.get("matched_in")),
        "prompt_version": _clean(row.get("prompt_version"))
        or LLM_OBJECT_REVIEW_PROMPT_VERSION,
        "model": _clean(row.get("model")) or DEFAULT_OPENAI_REVIEW_MODEL,
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_review_decision(decision: LLMObjectReviewDecision, row: dict[str, Any]) -> None:
    """Validate model output against evidence and conservative graph policies."""
    quote = decision.evidence_quote.strip()
    if quote and decision.reviewer_correct != "unclear":
        evidence_fields = [
            _clean(row.get("sentence_text")),
            _clean(row.get("context_window_s3")),
            _clean(row.get("resolved_cited_title")),
        ]
        if not any(quote in field for field in evidence_fields):
            raise ValueError("evidence_quote is not an exact substring of local evidence fields")

    object_category = _clean(row.get("object_category"))
    matched_in = _clean(row.get("matched_in"))
    surface = _clean(row.get("surface_form"))
    context_text = " ".join(
        [_clean(row.get("sentence_text")), _clean(row.get("context_window_s3"))]
    )

    if object_category == "generic_metric" and decision.should_allow_in_object_graph:
        raise ValueError("generic_metric mentions should not be graph objects by default")

    if object_category == "generic_metric" and not decision.should_use_as_phase1_feature:
        raise ValueError("generic_metric mentions should remain phase-1 features by default")

    if matched_in == "resolved_cited_title" and decision.should_allow_in_object_graph:
        if not (_contains_casefold(context_text, surface) and quote and quote in context_text):
            raise ValueError(
                "resolved_cited_title-only matches require direct context evidence "
                "before graph use"
            )

    if surface == "transformer" and decision.should_allow_in_object_graph:
        raise ValueError("lowercase transformer is a generic_architecture mention by default")

    if surface.upper() == "PTB" and decision.should_allow_in_object_graph:
        cues = ("penn treebank", "treebank", "corpus", "dataset", "wsj")
        if not any(cue in context_text.lower() for cue in cues):
            raise ValueError("PTB graph use requires a local disambiguating cue")


def fallback_unclear_record(
    *,
    row: dict[str, Any],
    model: str,
    validation_error: str,
    raw_response: str,
    usage: dict[str, int | None],
) -> dict[str, Any]:
    """Build an explicit unclear record after repeated model/schema failures."""
    decision = LLMObjectReviewDecision(
        reviewer_correct="unclear",
        object_type_correct="unclear",
        surface_form_refers_to_object="unclear",
        should_allow_in_object_graph=False,
        should_use_as_phase1_feature=True,
        error_type="other",
        recommended_action="other",
        confidence=0.0,
        evidence_quote="",
        rationale_short=_truncate(
            f"Could not validate model output. {validation_error}. Raw: {raw_response}",
            240,
        ),
    )
    return _result_record_from_decision(
        row=row,
        decision=decision,
        review_status="fallback_unclear",
        validation_error=validation_error,
        attempts=2,
        from_cache=False,
        model_used=model,
        usage=usage,
    )


def build_llm_review_metrics(
    *,
    sample: pd.DataFrame,
    results: pd.DataFrame,
    dry_run: bool,
    dry_run_prompt_records: int = 0,
) -> dict[str, Any]:
    """Build aggregate metrics for the LLM-as-judge object review report."""
    reviewed = (
        results.loc[results["review_status"].isin(["reviewed", "fallback_unclear"])]
        if not results.empty and "review_status" in results
        else pd.DataFrame(columns=LLM_REVIEW_RESULT_COLUMNS)
    )
    true_false = (
        results.loc[results["reviewer_correct"].isin(["true", "false"])]
        if not results.empty and "reviewer_correct" in results
        else pd.DataFrame(columns=LLM_REVIEW_RESULT_COLUMNS)
    )
    return {
        "dry_run": dry_run,
        "sample_rows": int(len(sample)),
        "reviewed_rows": int(len(reviewed)),
        "dry_run_prompt_records": int(dry_run_prompt_records),
        "fallback_unclear_rows": _count_equals(results, "review_status", "fallback_unclear"),
        "from_cache_rows": int(results["from_cache"].sum()) if "from_cache" in results else 0,
        "reviewer_correct_distribution": _value_counts(
            results,
            ["reviewer_correct"],
            "rows",
        ),
        "error_type_distribution": _value_counts(results, ["error_type"], "rows"),
        "recommended_action_distribution": _value_counts(
            results,
            ["recommended_action"],
            "rows",
        ),
        "review_bucket_distribution": _value_counts(sample, ["review_bucket"], "rows"),
        "precision_over_true_false": _precision(true_false),
        "precision_by_object_category": _precision_by_group(results, "object_category"),
        "precision_by_matched_in": _precision_by_group(results, "matched_in"),
        "precision_by_canonical_name": _precision_by_group(results, "canonical_name", 30),
        "graph_allow_distribution": _value_counts(
            results,
            ["should_allow_in_object_graph"],
            "rows",
        ),
        "phase1_feature_distribution": _value_counts(
            results,
            ["should_use_as_phase1_feature"],
            "rows",
        ),
        "token_usage": {
            "input_tokens": _sum_numeric(results, "input_tokens"),
            "output_tokens": _sum_numeric(results, "output_tokens"),
            "total_tokens": _sum_numeric(results, "total_tokens"),
        },
    }


def build_llm_review_report(
    *,
    sample: pd.DataFrame,
    results: pd.DataFrame,
    metrics: dict[str, Any],
    sample_out: Path,
    jsonl_out: Path,
    parquet_out: Path,
    dry_run: bool,
) -> str:
    """Build a markdown report for the object mention LLM-as-judge review."""
    core = pd.DataFrame(
        [
            {"metric": "dry run", "value": metrics["dry_run"]},
            {"metric": "sample rows", "value": metrics["sample_rows"]},
            {"metric": "reviewed rows", "value": metrics["reviewed_rows"]},
            {
                "metric": "dry-run prompt records",
                "value": metrics["dry_run_prompt_records"],
            },
            {"metric": "fallback unclear rows", "value": metrics["fallback_unclear_rows"]},
            {"metric": "from cache rows", "value": metrics["from_cache_rows"]},
            {
                "metric": "precision over true/false reviews",
                "value": metrics["precision_over_true_false"],
            },
            {
                "metric": "input tokens",
                "value": metrics["token_usage"]["input_tokens"],
            },
            {
                "metric": "output tokens",
                "value": metrics["token_usage"]["output_tokens"],
            },
            {
                "metric": "total tokens",
                "value": metrics["token_usage"]["total_tokens"],
            },
        ]
    )
    false_or_unclear = (
        results.loc[results["reviewer_correct"].isin(["false", "unclear"])]
        if "reviewer_correct" in results
        else pd.DataFrame(columns=LLM_REVIEW_RESULT_COLUMNS)
    )
    sections = [
        "# Object Mentions LLM-as-Judge Review Report",
        "",
        "This is a model-based audit / LLM-assisted validation pass.",
        "",
        "## Outputs",
        f"- Sample CSV: `{sample_out}`",
        f"- JSONL results or dry-run prompts: `{jsonl_out}`",
        f"- Parquet results: `{parquet_out}`",
        "",
        "## Core Metrics",
        _table(core),
        "",
        "## Sample Bucket Distribution",
        _table(metrics["review_bucket_distribution"]),
        "",
        "## Reviewer Correct Distribution",
        _table(metrics["reviewer_correct_distribution"]),
        "",
        "## Error Type Distribution",
        _table(metrics["error_type_distribution"]),
        "",
        "## Recommended Action Distribution",
        _table(metrics["recommended_action_distribution"]),
        "",
        "## Graph Allow Distribution",
        _table(metrics["graph_allow_distribution"]),
        "",
        "## Phase-1 Feature Distribution",
        _table(metrics["phase1_feature_distribution"]),
        "",
        "## Precision By Object Category",
        _table(metrics["precision_by_object_category"]),
        "",
        "## Precision By Matched In",
        _table(metrics["precision_by_matched_in"]),
        "",
        "## Precision By Canonical Name",
        _table(metrics["precision_by_canonical_name"]),
        "",
        "## False Or Unclear Examples",
        _table(_review_examples(false_or_unclear, 25)),
        "",
        "## Registry Refinement Recommendations",
        _registry_refinement_recommendations(results, dry_run=dry_run),
        "",
        "## Sample Rows",
        _table(_sample_examples(sample, 20)),
        "",
    ]
    return "\n".join(sections)


def _write_dry_run_prompts(sample: pd.DataFrame, jsonl_output: Path) -> int:
    count = 0
    with jsonl_output.open("w", encoding="utf-8") as handle:
        for row in sample.to_dict(orient="records"):
            system_prompt, user_prompt = build_object_review_prompt(row)
            record = {
                "dry_run": True,
                "cache_key": row.get("cache_key", llm_object_review_cache_key(row)),
                "context_id": row.get("context_id", ""),
                "object_id": row.get("object_id", ""),
                "surface_form": row.get("surface_form", ""),
                "matched_in": row.get("matched_in", ""),
                "prompt_version": row.get("prompt_version", LLM_OBJECT_REVIEW_PROMPT_VERSION),
                "model": row.get("model", DEFAULT_OPENAI_REVIEW_MODEL),
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
            }
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1
    return count


def _result_record_from_decision(
    *,
    row: dict[str, Any],
    decision: LLMObjectReviewDecision,
    review_status: str,
    validation_error: str,
    attempts: int,
    from_cache: bool,
    model_used: str,
    usage: dict[str, int | None],
) -> dict[str, Any]:
    sample_part = {column: row.get(column, "") for column in LLM_REVIEW_SAMPLE_COLUMNS}
    result = {
        **sample_part,
        "reviewer_correct": decision.reviewer_correct,
        "object_type_correct": decision.object_type_correct,
        "surface_form_refers_to_object": decision.surface_form_refers_to_object,
        "should_allow_in_object_graph": decision.should_allow_in_object_graph,
        "should_use_as_phase1_feature": decision.should_use_as_phase1_feature,
        "error_type": decision.error_type,
        "recommended_action": decision.recommended_action,
        "llm_confidence": decision.confidence,
        "evidence_quote": decision.evidence_quote,
        "rationale_short": decision.rationale_short,
        "review_status": review_status,
        "validation_error": validation_error,
        "attempts": attempts,
        "from_cache": from_cache,
        "model_used": model_used,
        "input_tokens": usage.get("input_tokens"),
        "output_tokens": usage.get("output_tokens"),
        "total_tokens": usage.get("total_tokens"),
    }
    return result


def _scaled_quotas(limit: int) -> dict[str, int]:
    if limit == 200:
        return dict(BASE_SAMPLE_QUOTAS)
    total = sum(BASE_SAMPLE_QUOTAS.values())
    raw = {
        name: quota * limit / total
        for name, quota in BASE_SAMPLE_QUOTAS.items()
    }
    quotas = {name: int(value) for name, value in raw.items()}
    remaining = limit - sum(quotas.values())
    order = sorted(
        raw,
        key=lambda name: (raw[name] - quotas[name], BASE_SAMPLE_QUOTAS[name]),
        reverse=True,
    )
    for name in order[:remaining]:
        quotas[name] += 1
    return quotas


def _prepare_object_frame(frame: pd.DataFrame, *, source_table: str) -> pd.DataFrame:
    prepared = frame.copy()
    prepared = _ensure_columns(prepared, _object_input_columns())
    prepared["source_table"] = source_table
    prepared["confidence"] = pd.to_numeric(prepared["confidence"], errors="coerce").fillna(0.0)
    prepared["allow_in_object_graph"] = prepared["allow_in_object_graph"].map(_bool_value)
    prepared["_sample_identity"] = [
        "|".join(
            [
                str(row.context_id),
                str(row.object_id),
                str(row.surface_form),
                str(row.matched_in),
                source_table,
            ]
        )
        for row in prepared.itertuples(index=False)
    ]
    return prepared


def _attach_context_text(selected: pd.DataFrame, contexts: pd.DataFrame) -> pd.DataFrame:
    context_frame = _ensure_columns(contexts.copy(), _context_input_columns())
    context_frame = context_frame.drop_duplicates(subset=["context_id", "source_context_id"])
    merged = selected.merge(
        context_frame,
        on=["context_id", "source_context_id"],
        how="left",
        suffixes=("", "_context"),
    )
    for column in ("sentence_text", "context_window_s3"):
        context_column = f"{column}_context"
        if context_column in merged:
            is_empty = merged[column].isna() | merged[column].astype(str).str.strip().eq("")
            merged[column] = merged[column].where(
                ~is_empty,
                merged[context_column],
            )
            merged = merged.drop(columns=[context_column])
    return merged


def _attach_registry_notes(
    selected: pd.DataFrame,
    registry: list[ObjectRegistryEntry],
) -> pd.DataFrame:
    by_id = {entry.object_id: entry for entry in registry}
    notes = []
    aliases = []
    negative_aliases = []
    cues = []
    for object_id in selected["object_id"].fillna("").astype(str):
        entry = by_id.get(object_id)
        notes.append(entry.notes if entry else "")
        aliases.append("; ".join(entry.aliases) if entry else "")
        negative_aliases.append("; ".join(entry.negative_aliases) if entry else "")
        cues.append("; ".join(entry.require_context_cue) if entry else "")
    selected = selected.copy()
    selected["registry_notes"] = notes
    selected["registry_aliases"] = aliases
    selected["registry_negative_aliases"] = negative_aliases
    selected["registry_require_context_cue"] = cues
    return selected


def _prompt_row_payload(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "review_bucket": _clean(row.get("review_bucket")),
        "source_table": _clean(row.get("source_table")),
        "context_id": _clean(row.get("context_id")),
        "source_context_id": _clean(row.get("source_context_id")),
        "normalized_section": _clean(row.get("normalized_section")),
        "sentence_text": _clean(row.get("sentence_text")),
        "context_window_s3": _clean(row.get("context_window_s3")),
        "resolved_cited_title": _clean(row.get("resolved_cited_title")),
        "object_id": _clean(row.get("object_id")),
        "canonical_name": _clean(row.get("canonical_name")),
        "object_type": _clean(row.get("object_type")),
        "object_category": _clean(row.get("object_category")),
        "surface_form": _clean(row.get("surface_form")),
        "matched_in": _clean(row.get("matched_in")),
        "matcher_confidence": row.get("confidence", ""),
        "matcher_allow_in_object_graph": row.get("allow_in_object_graph", ""),
        "match_policy": _clean(row.get("match_policy")),
        "registry_notes": _clean(row.get("registry_notes")),
        "registry_aliases": _clean(row.get("registry_aliases")),
        "registry_negative_aliases": _clean(row.get("registry_negative_aliases")),
        "registry_require_context_cue": _clean(row.get("registry_require_context_cue")),
    }


def _read_parquet_with_columns(path: Path, columns: list[str]) -> pd.DataFrame:
    available = set(pq.read_schema(path).names)
    read_columns = [column for column in columns if column in available]
    frame = pd.read_parquet(path, columns=read_columns)
    return _ensure_columns(frame, columns)


def _object_input_columns() -> list[str]:
    return [
        "context_id",
        "source_context_id",
        "citing_paper_id",
        "resolved_cited_acl_id",
        "resolved_cited_title",
        "normalized_section",
        "raw_section_name",
        "sentence_text",
        "context_window_s3",
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


def _context_input_columns() -> list[str]:
    return [
        "context_id",
        "source_context_id",
        "citing_paper_id",
        "resolved_cited_acl_id",
        "resolved_cited_title",
        "normalized_section",
        "raw_section_name",
        "sentence_text",
        "context_window_s3",
    ]


def _drop_selected(frame: pd.DataFrame, selected_keys: set[str]) -> pd.DataFrame:
    if frame.empty or not selected_keys:
        return frame
    return frame.loc[~frame["_sample_identity"].astype(str).isin(selected_keys)]


def _sample_frame(frame: pd.DataFrame, requested: int, seed: int) -> pd.DataFrame:
    if requested <= 0 or frame.empty:
        return frame.head(0).copy()
    count = min(requested, len(frame))
    return frame.sample(n=count, random_state=seed).copy()


def _usage_to_dict(usage: Any) -> dict[str, int | None]:
    if usage is None:
        return {"input_tokens": None, "output_tokens": None, "total_tokens": None}
    return {
        "input_tokens": getattr(usage, "input_tokens", None)
        or getattr(usage, "prompt_tokens", None),
        "output_tokens": getattr(usage, "output_tokens", None)
        or getattr(usage, "completion_tokens", None),
        "total_tokens": getattr(usage, "total_tokens", None),
    }


def _contains_casefold(text: str, needle: str) -> bool:
    return needle.casefold() in text.casefold() if needle else False


def _ensure_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        if column not in df.columns:
            df[column] = ""
    return df


def _bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None or pd.isna(value):
        return False
    return str(value).strip().lower() in {"true", "1", "yes"}


def _clean(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


def _count_equals(frame: pd.DataFrame, column: str, value: str) -> int:
    if column not in frame:
        return 0
    return int(frame[column].fillna("").astype(str).eq(value).sum())


def _sum_numeric(frame: pd.DataFrame, column: str) -> int:
    if column not in frame or frame.empty:
        return 0
    return int(pd.to_numeric(frame[column], errors="coerce").fillna(0).sum())


def _precision(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "unavailable"
    denominator = int(frame["reviewer_correct"].isin(["true", "false"]).sum())
    if denominator == 0:
        return "unavailable"
    correct = int(frame["reviewer_correct"].eq("true").sum())
    return f"{correct / denominator:.3f}"


def _precision_by_group(
    frame: pd.DataFrame,
    column: str,
    limit: int | None = None,
) -> pd.DataFrame:
    columns = [column, "reviewed_true_false", "correct", "incorrect", "precision"]
    if frame.empty or column not in frame or "reviewer_correct" not in frame:
        return pd.DataFrame(columns=columns)
    eligible = frame.loc[frame["reviewer_correct"].isin(["true", "false"])].copy()
    if eligible.empty:
        return pd.DataFrame(columns=columns)
    eligible[column] = eligible[column].fillna("unavailable").astype(str)
    grouped = (
        eligible.assign(
            correct=eligible["reviewer_correct"].eq("true"),
            incorrect=eligible["reviewer_correct"].eq("false"),
        )
        .groupby(column, dropna=False)
        .agg(
            reviewed_true_false=("reviewer_correct", "size"),
            correct=("correct", "sum"),
            incorrect=("incorrect", "sum"),
        )
        .reset_index()
    )
    grouped["precision"] = grouped.apply(
        lambda row: f"{int(row['correct']) / int(row['reviewed_true_false']):.3f}",
        axis=1,
    )
    grouped = grouped.sort_values("reviewed_true_false", ascending=False)
    return grouped.head(limit) if limit else grouped


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


def _review_examples(frame: pd.DataFrame, limit: int) -> pd.DataFrame:
    columns = [
        "review_bucket",
        "context_id",
        "canonical_name",
        "object_category",
        "surface_form",
        "matched_in",
        "reviewer_correct",
        "error_type",
        "recommended_action",
        "evidence_quote",
        "rationale_short",
    ]
    if frame.empty:
        return pd.DataFrame(columns=columns)
    sample = _ensure_columns(frame.head(limit).copy(), columns)
    for column in ("evidence_quote", "rationale_short"):
        sample[column] = sample[column].map(lambda value: _truncate(value, 160))
    return sample[columns]


def _sample_examples(frame: pd.DataFrame, limit: int) -> pd.DataFrame:
    columns = [
        "review_bucket",
        "context_id",
        "canonical_name",
        "object_category",
        "surface_form",
        "matched_in",
        "confidence",
        "allow_in_object_graph",
        "sentence_text",
    ]
    if frame.empty:
        return pd.DataFrame(columns=columns)
    sample = _ensure_columns(frame.head(limit).copy(), columns)
    sample["sentence_text"] = sample["sentence_text"].map(lambda value: _truncate(value, 160))
    return sample[columns]


def _registry_refinement_recommendations(results: pd.DataFrame, *, dry_run: bool) -> str:
    if dry_run:
        return (
            "Dry-run only: prompts and sample were generated, but no model decisions "
            "were collected."
        )
    if results.empty:
        return "No model-based review decisions are available."
    flagged = results.loc[
        results["recommended_action"].isin(
            [
                "lower_confidence",
                "require_context_cue",
                "block_alias",
                "remove_alias",
                "change_object_type",
                "keep_as_feature_only",
            ]
        )
    ]
    if flagged.empty:
        return "No registry refinement actions were recommended by this review sample."
    counts = _value_counts(
        flagged,
        ["recommended_action", "object_id", "canonical_name", "surface_form"],
        "rows",
        limit=30,
    )
    return _table(counts)


def _truncate(value: Any, max_chars: int) -> str:
    text = _clean(value).replace("\n", " ")
    if len(text) <= max_chars:
        return text
    return f"{text[: max_chars - 3]}..."


def _table(df: pd.DataFrame) -> str:
    if df.empty:
        return "No records available."
    columns = list(df.columns)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in df.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(_markdown_cell(value) for value in row) + " |")
    return "\n".join(lines)


def _markdown_cell(value: Any) -> str:
    if value is None or pd.isna(value):
        return "unavailable"
    return str(value).replace("|", "\\|")
