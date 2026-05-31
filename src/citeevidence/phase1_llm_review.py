from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Literal

import pandas as pd
import pyarrow.parquet as pq
from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator

from citeevidence.llm_review import DEFAULT_OPENAI_REVIEW_MODEL, resolve_review_model
from citeevidence.phase1 import (
    DEFAULT_PHASE1_CANDIDATES_PILOT_REFINED_PATH,
    DEFAULT_PHASE1_CITED_TITLE_PROFILES_PATH,
    DEFAULT_PHASE1_CONTEXTS_PATH,
    DEFAULT_PHASE1_FEATURES_PILOT_REFINED_PATH,
    DEFAULT_PHASE1_OBJECT_GRAPH_CANDIDATES_PATH,
    DEFAULT_PHASE1_OBJECT_MENTIONS_PATH,
)

DEFAULT_PHASE1_LLM_REVIEW_SAMPLE_PATH = Path("data/processed/phase1_llm_review_sample.csv")
DEFAULT_PHASE1_LLM_REVIEW_JSONL_PATH = Path("data/processed/phase1_llm_review_results.jsonl")
DEFAULT_PHASE1_LLM_REVIEW_PARQUET_PATH = Path("data/processed/phase1_llm_review_results.parquet")
DEFAULT_PHASE1_LLM_REVIEW_REPORT = Path("reports/phase1_llm_review_report.md")
DEFAULT_PHASE1_LLM_RECOMMENDATIONS_REPORT = Path(
    "reports/phase1_rule_refinement_recommendations.md"
)
DEFAULT_PHASE1_LLM_CACHE_DIR = Path("data/cache/llm_phase1_review")
PHASE1_LLM_REVIEW_PROMPT_VERSION = "phase1_llm_review_v1"

REVIEW_BOOL = Literal["true", "false", "unclear"]
INTENT = Literal[
    "background",
    "uses",
    "compares_against",
    "extends",
    "critiques",
    "applies",
    "unclear",
]
OBJECT_TYPE = Literal[
    "method",
    "model",
    "dataset_or_database",
    "software_or_tool",
    "benchmark_or_protocol",
    "metric",
    "task",
    "theory_or_concept",
    "claim_or_finding",
    "unknown",
]
RELATION_SUBTYPE = Literal[
    "direct_use",
    "adapt_to_domain",
    "combine_with",
    "compare_against",
    "critique_limitation",
    "improve",
    "replace",
    "component_use",
    "evaluate_on",
    "report_metric",
    "none",
]
LLM_PRIORITY = Literal["high", "medium", "low", "none"]
ERROR_TYPE = Literal[
    "none",
    "cited_work_description_misread_as_use",
    "use_missed",
    "compare_overtriggered",
    "critique_overtriggered",
    "extends_overtriggered",
    "applies_overtriggered",
    "background_overtriggered",
    "object_type_wrong",
    "evidence_span_wrong",
    "llm_priority_wrong",
    "insufficient_context",
    "other",
]
RECOMMENDED_RULE_ACTION = Literal[
    "keep",
    "tighten_use_rule",
    "loosen_use_rule",
    "tighten_compare_rule",
    "loosen_compare_rule",
    "tighten_critique_rule",
    "loosen_critique_rule",
    "tighten_extends_rule",
    "loosen_extends_rule",
    "tighten_applies_rule",
    "loosen_applies_rule",
    "adjust_llm_priority",
    "fix_evidence_span",
    "other",
]

BASE_PHASE1_SAMPLE_QUOTAS = {
    "intent_uses": 30,
    "intent_background": 30,
    "intent_extends": 25,
    "intent_applies": 25,
    "intent_critiques": 25,
    "intent_compares_against": 25,
    "intent_unclear": 20,
    "cited_work_description": 20,
}

PHASE1_REVIEW_INPUT_COLUMNS = [
    "context_id",
    "citing_paper_id",
    "resolved_cited_title",
    "resolved_cited_authors",
    "normalized_section",
    "raw_section_name",
    "citation_marker",
    "sentence_text",
    "context_window_s3",
    "object_names",
    "object_types",
    "generic_metric_names",
    "cited_title_profile_object_names",
    "primary_candidate_intent",
    "candidate_intents",
    "primary_candidate_object_type",
    "candidate_relation_subtypes",
    "evidence_span",
    "confidence",
    "should_send_to_llm",
    "llm_priority",
    "llm_reason",
    "cited_work_description",
    "matched_rules",
    "phase1_reason",
    "has_object_mention",
    "has_graph_candidate_object",
]

PHASE1_LLM_SAMPLE_COLUMNS = [
    "review_bucket",
    "sample_row_id",
    "prompt_version",
    "model",
    "cache_key",
    *PHASE1_REVIEW_INPUT_COLUMNS,
]

PHASE1_LLM_RESULT_COLUMNS = [
    *PHASE1_LLM_SAMPLE_COLUMNS,
    "intent_correct",
    "better_intent",
    "object_type_correct",
    "better_object_type",
    "relation_subtype_correct",
    "better_relation_subtype",
    "evidence_supports_label",
    "evidence_quote",
    "should_send_to_llm_correct",
    "better_llm_priority",
    "cited_work_description_correct",
    "error_type",
    "recommended_rule_action",
    "reviewer_confidence",
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


class Phase1LLMReviewDecision(BaseModel):
    intent_correct: REVIEW_BOOL
    better_intent: INTENT
    object_type_correct: REVIEW_BOOL
    better_object_type: OBJECT_TYPE
    relation_subtype_correct: REVIEW_BOOL
    better_relation_subtype: RELATION_SUBTYPE
    evidence_supports_label: REVIEW_BOOL
    evidence_quote: str
    should_send_to_llm_correct: REVIEW_BOOL
    better_llm_priority: LLM_PRIORITY
    cited_work_description_correct: REVIEW_BOOL
    error_type: ERROR_TYPE
    recommended_rule_action: RECOMMENDED_RULE_ACTION
    confidence: float = Field(ge=0, le=1)
    rationale_short: str

    @field_validator("evidence_quote", "rationale_short")
    @classmethod
    def _strip_text(cls, value: str) -> str:
        return value.strip()

    @model_validator(mode="after")
    def _incorrect_requires_error(self) -> Phase1LLMReviewDecision:
        has_false = any(
            value == "false"
            for value in (
                self.intent_correct,
                self.object_type_correct,
                self.relation_subtype_correct,
                self.evidence_supports_label,
                self.should_send_to_llm_correct,
                self.cited_work_description_correct,
            )
        )
        if has_false and self.error_type == "none":
            raise ValueError("false review fields require error_type != none")
        return self


def run_phase1_llm_review(
    *,
    candidates_path: str | Path = DEFAULT_PHASE1_CANDIDATES_PILOT_REFINED_PATH,
    features_path: str | Path = DEFAULT_PHASE1_FEATURES_PILOT_REFINED_PATH,
    contexts_path: str | Path = DEFAULT_PHASE1_CONTEXTS_PATH,
    object_mentions_path: str | Path = DEFAULT_PHASE1_OBJECT_MENTIONS_PATH,
    object_graph_candidates_path: str | Path = DEFAULT_PHASE1_OBJECT_GRAPH_CANDIDATES_PATH,
    cited_title_profiles_path: str | Path = DEFAULT_PHASE1_CITED_TITLE_PROFILES_PATH,
    sample_out: str | Path = DEFAULT_PHASE1_LLM_REVIEW_SAMPLE_PATH,
    jsonl_out: str | Path = DEFAULT_PHASE1_LLM_REVIEW_JSONL_PATH,
    parquet_out: str | Path = DEFAULT_PHASE1_LLM_REVIEW_PARQUET_PATH,
    report_path: str | Path = DEFAULT_PHASE1_LLM_REVIEW_REPORT,
    recommendations_path: str | Path = DEFAULT_PHASE1_LLM_RECOMMENDATIONS_REPORT,
    cache_dir: str | Path = DEFAULT_PHASE1_LLM_CACHE_DIR,
    limit: int = 200,
    model: str | None = None,
    seed: int = 42,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Run or dry-run an LLM-as-judge audit for refined Phase-1 candidates."""
    if limit < 1:
        raise ValueError("limit must be positive")
    for path in (
        Path(candidates_path),
        Path(features_path),
        Path(contexts_path),
        Path(object_mentions_path),
        Path(object_graph_candidates_path),
        Path(cited_title_profiles_path),
    ):
        if not path.exists():
            raise FileNotFoundError(f"Required input does not exist: {path}")

    review_model = resolve_review_model(model)
    candidates = _read_parquet_with_columns(Path(candidates_path), _candidate_columns())
    contexts = _read_parquet_with_columns(Path(contexts_path), _context_columns())
    sample = build_phase1_llm_review_sample(
        candidates=candidates,
        contexts=contexts,
        limit=limit,
        seed=seed,
        model=review_model,
    )

    sample_output = Path(sample_out)
    jsonl_output = Path(jsonl_out)
    parquet_output = Path(parquet_out)
    report_output = Path(report_path)
    recommendations_output = Path(recommendations_path)
    for output_path in (
        sample_output,
        jsonl_output,
        parquet_output,
        report_output,
        recommendations_output,
    ):
        output_path.parent.mkdir(parents=True, exist_ok=True)

    sample.to_csv(sample_output, index=False)

    if dry_run:
        dry_run_records = write_phase1_dry_run_prompts(sample, jsonl_output)
        results = pd.DataFrame(columns=PHASE1_LLM_RESULT_COLUMNS)
        results.to_parquet(parquet_output, index=False)
        metrics = build_phase1_llm_review_metrics(
            sample=sample,
            results=results,
            dry_run=True,
            dry_run_prompt_records=dry_run_records,
        )
        report_output.write_text(
            build_phase1_llm_review_report(
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
        recommendations_output.write_text(
            build_phase1_rule_recommendations(results, metrics, dry_run=True),
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
            record = review_phase1_sample_row(
                row=row,
                client=client,
                model=review_model,
                cache_dir=cache_path,
            )
            result_records.append(record)
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    results = _ensure_columns(pd.DataFrame(result_records), PHASE1_LLM_RESULT_COLUMNS)
    results[PHASE1_LLM_RESULT_COLUMNS].to_parquet(parquet_output, index=False)
    metrics = build_phase1_llm_review_metrics(sample=sample, results=results, dry_run=False)
    report_output.write_text(
        build_phase1_llm_review_report(
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
    recommendations_output.write_text(
        build_phase1_rule_recommendations(results, metrics, dry_run=False),
        encoding="utf-8",
    )
    return metrics


def build_phase1_llm_review_sample(
    *,
    candidates: pd.DataFrame,
    contexts: pd.DataFrame,
    limit: int = 200,
    seed: int = 42,
    model: str = DEFAULT_OPENAI_REVIEW_MODEL,
) -> pd.DataFrame:
    """Build a deterministic stratified sample for Phase-1 LLM-as-judge audit."""
    if limit < 1:
        raise ValueError("limit must be positive")
    prepared = _prepare_candidate_frame(candidates, contexts)
    quotas = _scaled_phase1_quotas(limit)
    selected_parts: list[pd.DataFrame] = []
    selected_ids: set[str] = set()

    buckets = [
        (
            "intent_uses",
            prepared.loc[prepared["primary_candidate_intent"].eq("uses")],
        ),
        (
            "intent_background",
            prepared.loc[prepared["primary_candidate_intent"].eq("background")],
        ),
        (
            "intent_extends",
            prepared.loc[prepared["primary_candidate_intent"].eq("extends")],
        ),
        (
            "intent_applies",
            prepared.loc[prepared["primary_candidate_intent"].eq("applies")],
        ),
        (
            "intent_critiques",
            prepared.loc[prepared["primary_candidate_intent"].eq("critiques")],
        ),
        (
            "intent_compares_against",
            prepared.loc[prepared["primary_candidate_intent"].eq("compares_against")],
        ),
        (
            "intent_unclear",
            prepared.loc[prepared["primary_candidate_intent"].eq("unclear")],
        ),
        (
            "cited_work_description",
            prepared.loc[prepared["cited_work_description"].map(_bool_value)],
        ),
    ]
    for index, (bucket_name, bucket_frame) in enumerate(buckets):
        available = _drop_selected_contexts(bucket_frame, selected_ids)
        sample = _sample_frame(available, quotas[bucket_name], seed + index)
        if sample.empty:
            continue
        sample = sample.copy()
        sample["review_bucket"] = bucket_name
        selected_ids.update(sample["context_id"].astype(str))
        selected_parts.append(sample)

    selected = (
        pd.concat(selected_parts, ignore_index=True)
        if selected_parts
        else pd.DataFrame(columns=[*prepared.columns, "review_bucket"])
    )
    selected = _ensure_sample_coverage(selected, prepared, selected_ids, seed)
    if len(selected) < limit:
        fill_pool = _drop_selected_contexts(prepared, selected_ids)
        fill = _sample_frame(fill_pool, limit - len(selected), seed + 99)
        if not fill.empty:
            fill = fill.copy()
            fill["review_bucket"] = "quota_fill"
            selected = pd.concat([selected, fill], ignore_index=True)
    selected = selected.drop_duplicates(subset=["context_id"], keep="first").head(limit).copy()
    selected["prompt_version"] = PHASE1_LLM_REVIEW_PROMPT_VERSION
    selected["model"] = model
    selected["cache_key"] = selected.apply(
        lambda row: phase1_llm_review_cache_key(row.to_dict()),
        axis=1,
    )
    selected["sample_row_id"] = [
        f"phase1_llm_review_{index:04d}" for index in range(1, len(selected) + 1)
    ]
    selected = _ensure_columns(selected, PHASE1_LLM_SAMPLE_COLUMNS)
    return selected[PHASE1_LLM_SAMPLE_COLUMNS]


def review_phase1_sample_row(
    *,
    row: dict[str, Any],
    client: Any,
    model: str,
    cache_dir: Path,
) -> dict[str, Any]:
    """Review one sampled Phase-1 row, using deterministic local cache."""
    cache_key = phase1_llm_review_cache_key(row)
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
            decision, raw_response, usage = call_openai_phase1_review_decision(
                client=client,
                row=row,
                model=model,
            )
            validate_phase1_review_decision(decision, row)
            record = _phase1_result_record_from_decision(
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
        except Exception as exc:  # pragma: no cover - live API/network failures only.
            validation_error = f"{type(exc).__name__}: {exc}"

    fallback = phase1_fallback_unclear_record(
        row=row,
        model=model,
        validation_error=validation_error,
        raw_response=raw_response,
        usage=usage,
    )
    cache_file.write_text(json.dumps(fallback, ensure_ascii=False), encoding="utf-8")
    return fallback


def call_openai_phase1_review_decision(
    *,
    client: Any,
    row: dict[str, Any],
    model: str,
) -> tuple[Phase1LLMReviewDecision, str, dict[str, int | None]]:
    """Call OpenAI Structured Outputs for one Phase-1 LLM-as-judge decision."""
    system_prompt, user_prompt = build_phase1_review_prompt(row)
    response = client.responses.parse(
        model=model,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        text_format=Phase1LLMReviewDecision,
    )
    parsed = response.output_parsed
    if parsed is None:
        raw = getattr(response, "output_text", "")
        parsed = Phase1LLMReviewDecision.model_validate_json(raw)
    raw_response = (
        parsed.model_dump_json() if isinstance(parsed, Phase1LLMReviewDecision) else str(parsed)
    )
    return parsed, raw_response, _usage_to_dict(getattr(response, "usage", None))


def build_phase1_review_prompt(row: dict[str, Any]) -> tuple[str, str]:
    """Build the system/user prompt pair for one refined Phase-1 review."""
    system_prompt = (
        "You are performing an LLM-as-judge audit of rule-based Phase-1 "
        "citation-function screening for NLP / Computational Linguistics papers. "
        "This is model-based audit, not human validation and not final gold labeling. "
        "Return only the structured JSON object requested by the schema. Use only "
        "the provided citation context and object evidence."
    )
    payload = {
        "task": "LLM-as-judge audit of one refined Phase-1 citation-function candidate",
        "prompt_version": row.get("prompt_version", PHASE1_LLM_REVIEW_PROMPT_VERSION),
        "review_guidelines": [
            "Judge whether primary_candidate_intent is reasonable, not whether it is final gold.",
            "Distinguish current-paper use from cited-work description.",
            "'we use', 'our model uses', and 'we evaluate on' are current-paper use cues.",
            (
                "Smith et al. proposed/used/described usually describes the cited "
                "work and is background unless current-paper use is also present."
            ),
            (
                "Generic metrics alone do not imply compares_against unless explicit "
                "compare/evaluation language exists."
            ),
            (
                "Critique requires a negative relation such as fails to, cannot, "
                "does not, limited by, drawback of, unable to, or performs poorly."
            ),
            (
                "evidence_quote must be an exact substring of sentence_text or "
                "context_window_s3 when evidence_supports_label=true."
            ),
            "Assess should_send_to_llm and llm_priority as triage for later structured extraction.",
        ],
        "candidate": _prompt_row_payload(row),
        "required_output_schema": {
            "intent_correct": "true|false|unclear",
            "better_intent": "background|uses|compares_against|extends|critiques|applies|unclear",
            "object_type_correct": "true|false|unclear",
            "better_object_type": (
                "method|model|dataset_or_database|software_or_tool|"
                "benchmark_or_protocol|metric|task|theory_or_concept|"
                "claim_or_finding|unknown"
            ),
            "relation_subtype_correct": "true|false|unclear",
            "better_relation_subtype": (
                "direct_use|adapt_to_domain|combine_with|compare_against|"
                "critique_limitation|improve|replace|component_use|"
                "evaluate_on|report_metric|none"
            ),
            "evidence_supports_label": "true|false|unclear",
            "evidence_quote": "exact substring or empty",
            "should_send_to_llm_correct": "true|false|unclear",
            "better_llm_priority": "high|medium|low|none",
            "cited_work_description_correct": "true|false|unclear",
            "error_type": "one enum value",
            "recommended_rule_action": "one enum value",
            "confidence": "0..1",
            "rationale_short": "brief explanation",
        },
    }
    return system_prompt, json.dumps(payload, ensure_ascii=False, indent=2)


def phase1_llm_review_cache_key(row: dict[str, Any]) -> str:
    """Deterministic cache key for one Phase-1 LLM review row."""
    payload = {
        "context_id": _clean(row.get("context_id")),
        "prompt_version": _clean(row.get("prompt_version")) or PHASE1_LLM_REVIEW_PROMPT_VERSION,
        "model": _clean(row.get("model")) or DEFAULT_OPENAI_REVIEW_MODEL,
        "primary_candidate_intent": _clean(row.get("primary_candidate_intent")),
        "evidence_span": _clean(row.get("evidence_span")),
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_phase1_review_decision(
    decision: Phase1LLMReviewDecision,
    row: dict[str, Any],
) -> None:
    """Validate model output against schema-dependent evidence rules."""
    primary_intent = _clean(row.get("primary_candidate_intent"))
    if decision.intent_correct == "false" and decision.better_intent == primary_intent:
        raise ValueError("intent_correct=false requires better_intent to differ")

    quote = decision.evidence_quote.strip()
    evidence_fields = [_clean(row.get("sentence_text")), _clean(row.get("context_window_s3"))]
    if decision.evidence_supports_label == "true":
        if not quote:
            raise ValueError("evidence_supports_label=true requires non-empty evidence_quote")
        if not any(quote in field for field in evidence_fields):
            raise ValueError("evidence_quote is not an exact substring of local evidence fields")


def phase1_fallback_unclear_record(
    *,
    row: dict[str, Any],
    model: str,
    validation_error: str,
    raw_response: str,
    usage: dict[str, int | None],
) -> dict[str, Any]:
    """Build an explicit fallback record after repeated invalid outputs."""
    decision = Phase1LLMReviewDecision(
        intent_correct="unclear",
        better_intent="unclear",
        object_type_correct="unclear",
        better_object_type="unknown",
        relation_subtype_correct="unclear",
        better_relation_subtype="none",
        evidence_supports_label="unclear",
        evidence_quote="",
        should_send_to_llm_correct="unclear",
        better_llm_priority="medium",
        cited_work_description_correct="unclear",
        error_type="other",
        recommended_rule_action="other",
        confidence=0.0,
        rationale_short=_truncate(
            f"Could not validate model output. {validation_error}. Raw: {raw_response}",
            240,
        ),
    )
    return _phase1_result_record_from_decision(
        row=row,
        decision=decision,
        review_status="fallback_unclear",
        validation_error=validation_error,
        attempts=2,
        from_cache=False,
        model_used=model,
        usage=usage,
    )


def build_phase1_llm_review_metrics(
    *,
    sample: pd.DataFrame,
    results: pd.DataFrame,
    dry_run: bool,
    dry_run_prompt_records: int = 0,
) -> dict[str, Any]:
    """Build aggregate metrics for the Phase-1 LLM-as-judge audit report."""
    reviewed = (
        results.loc[results["review_status"].isin(["reviewed", "fallback_unclear"])]
        if not results.empty and "review_status" in results
        else pd.DataFrame(columns=PHASE1_LLM_RESULT_COLUMNS)
    )
    invalid_or_fallback = (
        int(results["review_status"].eq("fallback_unclear").sum())
        if "review_status" in results
        else 0
    )
    return {
        "dry_run": dry_run,
        "total_sampled_rows": int(len(sample)),
        "reviewed_rows": int(len(reviewed)),
        "dry_run_prompt_records": int(dry_run_prompt_records),
        "invalid_retry_fallback_rows": invalid_or_fallback,
        "from_cache_rows": int(results["from_cache"].sum()) if "from_cache" in results else 0,
        "intent_correct_distribution": _value_counts(results, ["intent_correct"], "rows"),
        "estimated_precision_by_primary_candidate_intent": _precision_by_group(
            results,
            "primary_candidate_intent",
            correctness_column="intent_correct",
        ),
        "better_intent_distribution_for_incorrect_rows": _value_counts(
            results.loc[results["intent_correct"].eq("false")]
            if "intent_correct" in results
            else pd.DataFrame(),
            ["better_intent"],
            "rows",
        ),
        "object_type_correct_distribution": _value_counts(
            results,
            ["object_type_correct"],
            "rows",
        ),
        "relation_subtype_correct_distribution": _value_counts(
            results,
            ["relation_subtype_correct"],
            "rows",
        ),
        "evidence_supports_label_distribution": _value_counts(
            results,
            ["evidence_supports_label"],
            "rows",
        ),
        "should_send_to_llm_correct_distribution": _value_counts(
            results,
            ["should_send_to_llm_correct"],
            "rows",
        ),
        "better_llm_priority_distribution": _value_counts(
            results,
            ["better_llm_priority"],
            "rows",
        ),
        "cited_work_description_correct_distribution": _value_counts(
            results,
            ["cited_work_description_correct"],
            "rows",
        ),
        "error_type_distribution": _value_counts(results, ["error_type"], "rows"),
        "recommended_rule_action_distribution": _value_counts(
            results,
            ["recommended_rule_action"],
            "rows",
        ),
        "precision_by_llm_priority": _precision_by_group(
            results,
            "llm_priority",
            correctness_column="intent_correct",
        ),
        "precision_by_normalized_section": _precision_by_group(
            results,
            "normalized_section",
            correctness_column="intent_correct",
        ),
        "sample_bucket_distribution": _value_counts(sample, ["review_bucket"], "rows"),
        "token_usage": {
            "input_tokens": _sum_numeric(results, "input_tokens"),
            "output_tokens": _sum_numeric(results, "output_tokens"),
            "total_tokens": _sum_numeric(results, "total_tokens"),
        },
    }


def build_phase1_llm_review_report(
    *,
    sample: pd.DataFrame,
    results: pd.DataFrame,
    metrics: dict[str, Any],
    sample_out: Path,
    jsonl_out: Path,
    parquet_out: Path,
    dry_run: bool,
) -> str:
    """Build markdown report for Phase-1 LLM-as-judge audit."""
    core = pd.DataFrame(
        [
            {"metric": "dry_run", "value": metrics["dry_run"]},
            {"metric": "total_sampled_rows", "value": metrics["total_sampled_rows"]},
            {"metric": "reviewed_rows", "value": metrics["reviewed_rows"]},
            {
                "metric": "dry_run_prompt_records",
                "value": metrics["dry_run_prompt_records"],
            },
            {
                "metric": "invalid_retry_fallback_rows",
                "value": metrics["invalid_retry_fallback_rows"],
            },
            {"metric": "from_cache_rows", "value": metrics["from_cache_rows"]},
            {"metric": "input_tokens", "value": metrics["token_usage"]["input_tokens"]},
            {"metric": "output_tokens", "value": metrics["token_usage"]["output_tokens"]},
            {"metric": "total_tokens", "value": metrics["token_usage"]["total_tokens"]},
        ]
    )
    sections = [
        "# Phase-1 LLM-as-Judge Review Report",
        "",
        "This is a model-based audit / LLM-assisted validation pass for Phase-1 "
        "candidate labels, not final gold labeling.",
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
        _table(metrics["sample_bucket_distribution"]),
        "",
        "## Intent Correct Distribution",
        _table(metrics["intent_correct_distribution"]),
        "",
        "## Estimated Precision By Primary Candidate Intent",
        _table(metrics["estimated_precision_by_primary_candidate_intent"]),
        "",
        "## Better Intent Distribution For Incorrect Rows",
        _table(metrics["better_intent_distribution_for_incorrect_rows"]),
        "",
        "## Object Type Correct Distribution",
        _table(metrics["object_type_correct_distribution"]),
        "",
        "## Relation Subtype Correct Distribution",
        _table(metrics["relation_subtype_correct_distribution"]),
        "",
        "## Evidence Supports Label Distribution",
        _table(metrics["evidence_supports_label_distribution"]),
        "",
        "## Should Send To LLM Correct Distribution",
        _table(metrics["should_send_to_llm_correct_distribution"]),
        "",
        "## Better LLM Priority Distribution",
        _table(metrics["better_llm_priority_distribution"]),
        "",
        "## Cited Work Description Correct Distribution",
        _table(metrics["cited_work_description_correct_distribution"]),
        "",
        "## Error Type Distribution",
        _table(metrics["error_type_distribution"]),
        "",
        "## Recommended Rule Action Distribution",
        _table(metrics["recommended_rule_action_distribution"]),
        "",
        "## Precision By LLM Priority",
        _table(metrics["precision_by_llm_priority"]),
        "",
        "## Precision By Normalized Section",
        _table(metrics["precision_by_normalized_section"]),
        "",
        "## Uses False Positive Examples",
        _table(_false_positive_examples(results, {"uses"}, 10)),
        "",
        "## Critiques False Positive Examples",
        _table(_false_positive_examples(results, {"critiques"}, 10)),
        "",
        "## Compares False Positive Examples",
        _table(_false_positive_examples(results, {"compares_against"}, 10)),
        "",
        "## Extends / Applies False Positive Examples",
        _table(_false_positive_examples(results, {"extends", "applies"}, 10)),
        "",
        "## Cited Work Description Correct Cases",
        _table(_cited_work_correct_examples(results, 10)),
        "",
        "## LLM Priority Mistake Examples",
        _table(_priority_mistake_examples(results, 10)),
        "",
        "## Sample Rows",
        _table(_sample_examples(sample, 20)),
        "",
    ]
    return "\n".join(sections)


def build_phase1_rule_recommendations(
    results: pd.DataFrame,
    metrics: dict[str, Any],
    *,
    dry_run: bool,
) -> str:
    """Build markdown rule refinement recommendations from review outcomes."""
    sections = [
        "# Phase-1 Rule Refinement Recommendations",
        "",
        "This report summarizes model-based audit signals. It is not human validation.",
        "",
    ]
    if dry_run or results.empty:
        sections.extend(
            [
                "No model review results are available yet because this was a dry run.",
                "",
                "Recommended next step: run the same command without `--dry-run` after "
                "setting `OPENAI_API_KEY`.",
                "",
            ]
        )
        return "\n".join(sections)

    sections.extend(
        [
            "## Highest Volume Error Types",
            _table(metrics["error_type_distribution"].head(15)),
            "",
            "## Highest Volume Recommended Actions",
            _table(metrics["recommended_rule_action_distribution"].head(15)),
            "",
            "## Actionable Recommendations",
            _recommendation_bullets(results),
            "",
            "## Representative Mistakes",
            _table(_mistake_examples(results, 20)),
            "",
        ]
    )
    return "\n".join(sections)


def write_phase1_dry_run_prompts(sample: pd.DataFrame, jsonl_output: Path) -> int:
    """Write dry-run prompt records without requiring an API key."""
    count = 0
    with jsonl_output.open("w", encoding="utf-8") as handle:
        for row in sample.to_dict(orient="records"):
            system_prompt, user_prompt = build_phase1_review_prompt(row)
            record = {
                "dry_run": True,
                "cache_key": row.get("cache_key", phase1_llm_review_cache_key(row)),
                "context_id": row.get("context_id", ""),
                "prompt_version": row.get("prompt_version", PHASE1_LLM_REVIEW_PROMPT_VERSION),
                "model": row.get("model", DEFAULT_OPENAI_REVIEW_MODEL),
                "primary_candidate_intent": row.get("primary_candidate_intent", ""),
                "llm_priority": row.get("llm_priority", ""),
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
            }
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1
    return count


def _phase1_result_record_from_decision(
    *,
    row: dict[str, Any],
    decision: Phase1LLMReviewDecision,
    review_status: str,
    validation_error: str,
    attempts: int,
    from_cache: bool,
    model_used: str,
    usage: dict[str, int | None],
) -> dict[str, Any]:
    sample_part = {column: row.get(column, "") for column in PHASE1_LLM_SAMPLE_COLUMNS}
    return {
        **sample_part,
        "intent_correct": decision.intent_correct,
        "better_intent": decision.better_intent,
        "object_type_correct": decision.object_type_correct,
        "better_object_type": decision.better_object_type,
        "relation_subtype_correct": decision.relation_subtype_correct,
        "better_relation_subtype": decision.better_relation_subtype,
        "evidence_supports_label": decision.evidence_supports_label,
        "evidence_quote": decision.evidence_quote,
        "should_send_to_llm_correct": decision.should_send_to_llm_correct,
        "better_llm_priority": decision.better_llm_priority,
        "cited_work_description_correct": decision.cited_work_description_correct,
        "error_type": decision.error_type,
        "recommended_rule_action": decision.recommended_rule_action,
        "reviewer_confidence": decision.confidence,
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


def _prepare_candidate_frame(candidates: pd.DataFrame, contexts: pd.DataFrame) -> pd.DataFrame:
    prepared = _ensure_columns(candidates.copy(), _candidate_columns())
    context_columns = ["context_id", "resolved_cited_authors"]
    context_frame = _ensure_columns(contexts.copy(), context_columns)[context_columns]
    context_frame = context_frame.drop_duplicates(subset=["context_id"])
    prepared = prepared.merge(context_frame, on="context_id", how="left")
    prepared["resolved_cited_authors"] = prepared["resolved_cited_authors"].fillna("")
    prepared = _ensure_columns(prepared, PHASE1_REVIEW_INPUT_COLUMNS)
    prepared["confidence"] = pd.to_numeric(prepared["confidence"], errors="coerce").fillna(0.0)
    for column in (
        "should_send_to_llm",
        "cited_work_description",
        "has_object_mention",
        "has_graph_candidate_object",
    ):
        prepared[column] = prepared[column].map(_bool_value)
    return prepared


def _scaled_phase1_quotas(limit: int) -> dict[str, int]:
    if limit == 200:
        return dict(BASE_PHASE1_SAMPLE_QUOTAS)
    total = sum(BASE_PHASE1_SAMPLE_QUOTAS.values())
    raw = {name: quota * limit / total for name, quota in BASE_PHASE1_SAMPLE_QUOTAS.items()}
    quotas = {name: int(value) for name, value in raw.items()}
    remaining = limit - sum(quotas.values())
    order = sorted(
        raw,
        key=lambda name: (raw[name] - quotas[name], BASE_PHASE1_SAMPLE_QUOTAS[name]),
        reverse=True,
    )
    for name in order[:remaining]:
        quotas[name] += 1
    return quotas


def _ensure_sample_coverage(
    selected: pd.DataFrame,
    prepared: pd.DataFrame,
    selected_ids: set[str],
    seed: int,
) -> pd.DataFrame:
    coverage_specs = [
        ("coverage_high_priority", prepared["llm_priority"].eq("high")),
        ("coverage_medium_priority", prepared["llm_priority"].eq("medium")),
        ("coverage_low_priority", prepared["llm_priority"].eq("low")),
        ("coverage_graph_candidate", prepared["has_graph_candidate_object"].map(_bool_value)),
        ("coverage_generic_metric", prepared["generic_metric_names"].fillna("").astype(str).ne("")),
        ("coverage_multiple_intents", prepared["candidate_intents"].fillna("").str.contains(";")),
    ]
    output = selected.copy()
    for offset, (bucket, mask) in enumerate(coverage_specs):
        if _selected_has_coverage(output, bucket, mask_name=bucket):
            continue
        available = _drop_selected_contexts(prepared.loc[mask], selected_ids)
        addition = _sample_frame(available, 1, seed + 200 + offset)
        if addition.empty:
            continue
        addition = addition.copy()
        addition["review_bucket"] = bucket
        selected_ids.update(addition["context_id"].astype(str))
        output = pd.concat([output, addition], ignore_index=True)
    return output


def _selected_has_coverage(selected: pd.DataFrame, bucket: str, *, mask_name: str) -> bool:
    if selected.empty:
        return False
    if bucket in set(selected.get("review_bucket", pd.Series(dtype=str)).astype(str)):
        return True
    if mask_name == "coverage_high_priority":
        return bool(selected["llm_priority"].eq("high").any())
    if mask_name == "coverage_medium_priority":
        return bool(selected["llm_priority"].eq("medium").any())
    if mask_name == "coverage_low_priority":
        return bool(selected["llm_priority"].eq("low").any())
    if mask_name == "coverage_graph_candidate":
        return bool(selected["has_graph_candidate_object"].map(_bool_value).any())
    if mask_name == "coverage_generic_metric":
        return bool(selected["generic_metric_names"].fillna("").astype(str).ne("").any())
    if mask_name == "coverage_multiple_intents":
        return bool(selected["candidate_intents"].fillna("").str.contains(";").any())
    return False


def _drop_selected_contexts(frame: pd.DataFrame, selected_ids: set[str]) -> pd.DataFrame:
    if frame.empty or not selected_ids:
        return frame
    return frame.loc[~frame["context_id"].astype(str).isin(selected_ids)]


def _sample_frame(frame: pd.DataFrame, requested: int, seed: int) -> pd.DataFrame:
    if requested <= 0 or frame.empty:
        return frame.head(0).copy()
    count = min(requested, len(frame))
    return frame.sample(n=count, random_state=seed).copy()


def _prompt_row_payload(row: dict[str, Any]) -> dict[str, Any]:
    return {column: _clean(row.get(column)) for column in PHASE1_REVIEW_INPUT_COLUMNS}


def _candidate_columns() -> list[str]:
    return [
        "context_id",
        "citing_paper_id",
        "resolved_cited_title",
        "normalized_section",
        "raw_section_name",
        "citation_marker",
        "sentence_text",
        "context_window_s3",
        "object_names",
        "object_types",
        "generic_metric_names",
        "cited_title_profile_object_names",
        "primary_candidate_intent",
        "candidate_intents",
        "primary_candidate_object_type",
        "candidate_relation_subtypes",
        "evidence_span",
        "confidence",
        "should_send_to_llm",
        "llm_priority",
        "llm_reason",
        "cited_work_description",
        "matched_rules",
        "phase1_reason",
        "has_object_mention",
        "has_graph_candidate_object",
    ]


def _context_columns() -> list[str]:
    return ["context_id", "resolved_cited_authors"]


def _read_parquet_with_columns(path: Path, columns: list[str]) -> pd.DataFrame:
    available = set(pq.read_schema(path).names)
    read_columns = [column for column in columns if column in available]
    frame = pd.read_parquet(path, columns=read_columns)
    return _ensure_columns(frame, columns)


def _false_positive_examples(
    results: pd.DataFrame,
    intents: set[str],
    limit: int,
) -> pd.DataFrame:
    if results.empty or "intent_correct" not in results:
        return pd.DataFrame()
    mask = results["primary_candidate_intent"].isin(intents) & results["intent_correct"].eq("false")
    return _review_examples(results.loc[mask], limit)


def _cited_work_correct_examples(results: pd.DataFrame, limit: int) -> pd.DataFrame:
    if results.empty:
        return pd.DataFrame()
    mask = results["cited_work_description"].map(_bool_value) & results[
        "cited_work_description_correct"
    ].eq("true")
    return _review_examples(results.loc[mask], limit)


def _priority_mistake_examples(results: pd.DataFrame, limit: int) -> pd.DataFrame:
    if results.empty:
        return pd.DataFrame()
    mask = results["should_send_to_llm_correct"].eq("false") | (
        results["better_llm_priority"].fillna("").astype(str)
        != results["llm_priority"].fillna("").astype(str)
    )
    return _review_examples(results.loc[mask], limit)


def _mistake_examples(results: pd.DataFrame, limit: int) -> pd.DataFrame:
    if results.empty:
        return pd.DataFrame()
    mask = (
        results["intent_correct"].eq("false")
        | results["should_send_to_llm_correct"].eq("false")
        | results["evidence_supports_label"].eq("false")
    )
    return _review_examples(results.loc[mask], limit)


def _review_examples(frame: pd.DataFrame, limit: int) -> pd.DataFrame:
    columns = [
        "context_id",
        "normalized_section",
        "primary_candidate_intent",
        "better_intent",
        "intent_correct",
        "llm_priority",
        "better_llm_priority",
        "should_send_to_llm_correct",
        "cited_work_description",
        "cited_work_description_correct",
        "error_type",
        "recommended_rule_action",
        "evidence_span",
        "evidence_quote",
        "rationale_short",
        "sentence_text",
    ]
    sample = _ensure_columns(frame.head(limit).copy(), columns)
    for column in ("sentence_text", "rationale_short", "evidence_quote"):
        sample[column] = sample[column].map(lambda value: _truncate(value, 180))
    return sample[columns]


def _sample_examples(sample: pd.DataFrame, limit: int) -> pd.DataFrame:
    columns = [
        "review_bucket",
        "context_id",
        "normalized_section",
        "primary_candidate_intent",
        "llm_priority",
        "cited_work_description",
        "object_names",
        "generic_metric_names",
        "evidence_span",
        "sentence_text",
    ]
    frame = _ensure_columns(sample.head(limit).copy(), columns)
    for column in ("sentence_text", "object_names", "generic_metric_names"):
        frame[column] = frame[column].map(lambda value: _truncate(value, 180))
    return frame[columns]


def _recommendation_bullets(results: pd.DataFrame) -> str:
    if results.empty:
        return "_No reviewed rows._"
    action_counts = results["recommended_rule_action"].value_counts()
    error_counts = results["error_type"].value_counts()
    bullets = []
    for action, count in action_counts.head(8).items():
        if action == "keep":
            continue
        bullets.append(f"- `{action}`: {int(count)} reviewed rows suggested this action.")
    for error_type, count in error_counts.head(8).items():
        if error_type == "none":
            continue
        bullets.append(f"- Watch `{error_type}`: {int(count)} reviewed rows flagged it.")
    if not bullets:
        return "- Most reviewed rows recommended keeping the current refined rules."
    return "\n".join(bullets)


def _value_counts(frame: pd.DataFrame, columns: list[str], count_name: str) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(columns=[*columns, count_name])
    return (
        frame.groupby(columns, dropna=False)
        .size()
        .reset_index(name=count_name)
        .sort_values(count_name, ascending=False)
        .reset_index(drop=True)
    )


def _precision_by_group(
    frame: pd.DataFrame,
    group_column: str,
    *,
    correctness_column: str,
    limit: int | None = None,
) -> pd.DataFrame:
    columns = [group_column, "reviewed_true_false", "correct", "incorrect", "precision"]
    if frame.empty or group_column not in frame or correctness_column not in frame:
        return pd.DataFrame(columns=columns)
    eligible = frame.loc[frame[correctness_column].isin(["true", "false"])].copy()
    if eligible.empty:
        return pd.DataFrame(columns=columns)
    grouped = (
        eligible.assign(
            _correct=eligible[correctness_column].eq("true").astype(int),
            _incorrect=eligible[correctness_column].eq("false").astype(int),
        )
        .groupby(group_column, dropna=False)
        .agg(
            reviewed_true_false=(correctness_column, "size"),
            correct=("_correct", "sum"),
            incorrect=("_incorrect", "sum"),
        )
        .reset_index()
    )
    grouped["precision"] = grouped["correct"] / grouped["reviewed_true_false"]
    grouped = grouped.sort_values("reviewed_true_false", ascending=False).reset_index(drop=True)
    if limit is not None:
        grouped = grouped.head(limit)
    return grouped[columns]


def _sum_numeric(frame: pd.DataFrame, column: str) -> int:
    if column not in frame or frame.empty:
        return 0
    return int(pd.to_numeric(frame[column], errors="coerce").fillna(0).sum())


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


def _ensure_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    output = df.copy()
    for column in columns:
        if column not in output.columns:
            output[column] = ""
    return output


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


def _truncate(value: Any, max_chars: int) -> str:
    text = _clean(value)
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3] + "..."


def _table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    safe = frame.copy()
    for column in safe.columns:
        safe[column] = safe[column].map(lambda value: _truncate(value, 220))
    return safe.to_markdown(index=False)
