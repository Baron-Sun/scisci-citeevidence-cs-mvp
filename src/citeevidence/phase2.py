from __future__ import annotations

import hashlib
import json
import os
import random
import time
from pathlib import Path
from typing import Any, Literal

import pandas as pd
import pyarrow.parquet as pq
from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    ValidationInfo,
    field_validator,
    model_validator,
)

from citeevidence.llm_review import DEFAULT_OPENAI_REVIEW_MODEL, resolve_review_model
from citeevidence.phase1 import (
    DEFAULT_PHASE1_CANDIDATES_FULL_PATH,
    DEFAULT_PHASE1_CITED_TITLE_PROFILES_PATH,
    DEFAULT_PHASE1_CONTEXTS_PATH,
    DEFAULT_PHASE1_FEATURES_FULL_PATH,
    DEFAULT_PHASE1_LLM_QUEUE_SAMPLE_PATH,
    DEFAULT_PHASE1_OBJECT_GRAPH_CANDIDATES_PATH,
    DEFAULT_PHASE1_OBJECT_MENTIONS_PATH,
)

DEFAULT_PHASE2_STRUCTURED_JSONL_PATH = Path(
    "data/processed/phase2_structured_labels_pilot.jsonl"
)
DEFAULT_PHASE2_STRUCTURED_PARQUET_PATH = Path(
    "data/processed/phase2_structured_labels_pilot.parquet"
)
DEFAULT_PHASE2_STRUCTURED_FAILED_PATH = Path(
    "data/processed/phase2_structured_labels_failed.jsonl"
)
DEFAULT_PHASE2_DRY_RUN_PROMPTS_PATH = Path(
    "data/processed/phase2_structured_prompts_dryrun.jsonl"
)
DEFAULT_PHASE2_STRUCTURED_REPORT = Path(
    "reports/phase2_structured_extraction_pilot_report.md"
)
DEFAULT_PHASE2_REVIEW_SAMPLE_PATH = Path("data/processed/phase2_label_review_sample.csv")
DEFAULT_PHASE2_CACHE_DIR = Path("data/cache/llm_phase2_structured")
PHASE2_PROMPT_VERSION = "phase2_structured_extraction_v1"

FINAL_INTENT = Literal[
    "background",
    "uses",
    "compares_against",
    "extends",
    "critiques",
    "applies",
    "unclear",
]
FINAL_OBJECT_TYPE = Literal[
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
FINAL_RELATION_SUBTYPE = Literal[
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
METHOD_EDGE_TYPE = Literal[
    "extends",
    "improves",
    "replaces",
    "adapts",
    "uses_component",
    "compares",
    "background",
    "not_method_related",
]
STANCE = Literal["neutral", "positive", "negative", "mixed", "unclear"]
EVIDENCE_SUPPORT = Literal["true", "false", "unclear"]
ABSTAIN_REASON = Literal[
    "insufficient_evidence",
    "ambiguous_context",
    "grouped_citation",
    "wrong_phase1_candidate",
    "no_relevant_function",
    "other",
    "null",
]

PHASE2_INPUT_COLUMNS = [
    "context_id",
    "source_context_id",
    "citing_paper_id",
    "resolved_cited_acl_id",
    "resolved_cited_title",
    "resolved_cited_year",
    "resolved_cited_authors",
    "normalized_section",
    "raw_section_name",
    "citation_marker",
    "sentence_text",
    "context_window_s3",
    "object_names",
    "object_types",
    "graph_candidate_object_names",
    "generic_metric_names",
    "cited_title_profile_object_names",
    "primary_candidate_intent",
    "candidate_intents",
    "primary_candidate_object_type",
    "object_type_source",
    "object_type_confidence",
    "candidate_relation_subtypes",
    "evidence_span",
    "confidence",
    "llm_priority",
    "llm_reason",
    "phase2_candidate_type",
    "cited_work_description",
    "phase1_reason",
    "matched_rules",
    "prompt_version",
    "model",
    "cache_key",
    "sample_row_id",
]

PHASE2_RESULT_COLUMNS = [
    *PHASE2_INPUT_COLUMNS,
    "final_intent",
    "final_object_type",
    "final_relation_subtype",
    "method_edge_type",
    "stance",
    "evidence_span_phase2",
    "problem_or_motivation_quote",
    "usage_or_mechanism_quote",
    "comparison_or_tradeoff_quote",
    "evidence_supports_label",
    "abstain",
    "abstain_reason",
    "phase2_confidence",
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

PHASE2_FAILED_COLUMNS = [
    "context_id",
    "cache_key",
    "prompt_version",
    "model",
    "primary_candidate_intent",
    "validation_error",
    "raw_response",
    "attempts",
]

PHASE2_REVIEW_SAMPLE_COLUMNS = [
    "context_id",
    "sentence_text",
    "context_window_s3",
    "resolved_cited_title",
    "primary_candidate_intent",
    "final_intent",
    "final_object_type",
    "final_relation_subtype",
    "evidence_span",
    "confidence",
    "abstain",
    "rationale_short",
    "reviewer_correct",
    "reviewer_notes",
]


class Phase2StructuredLabel(BaseModel):
    final_intent: FINAL_INTENT
    final_object_type: FINAL_OBJECT_TYPE
    final_relation_subtype: FINAL_RELATION_SUBTYPE
    method_edge_type: METHOD_EDGE_TYPE
    stance: STANCE
    evidence_span: str
    problem_or_motivation_quote: str | None = None
    usage_or_mechanism_quote: str | None = None
    comparison_or_tradeoff_quote: str | None = None
    evidence_supports_label: EVIDENCE_SUPPORT
    abstain: bool
    abstain_reason: ABSTAIN_REASON | None = None
    confidence: float = Field(ge=0, le=1)
    rationale_short: str

    @field_validator(
        "evidence_span",
        "problem_or_motivation_quote",
        "usage_or_mechanism_quote",
        "comparison_or_tradeoff_quote",
        "rationale_short",
        mode="before",
    )
    @classmethod
    def _strip_text(cls, value: Any, info: ValidationInfo) -> Any:
        if value is None:
            return None
        text = str(value).strip()
        quote_fields = {
            "problem_or_motivation_quote",
            "usage_or_mechanism_quote",
            "comparison_or_tradeoff_quote",
        }
        if info.field_name in quote_fields and text.lower() in {"", "null", "none"}:
            return None
        return text

    @model_validator(mode="after")
    def _abstain_is_conservative(self) -> Phase2StructuredLabel:
        if self.abstain:
            if self.final_intent not in {"background", "unclear"}:
                raise ValueError("abstain=true requires final_intent background or unclear")
            if self.confidence > 0.5:
                raise ValueError("abstain=true requires confidence <= 0.5")
            if self.abstain_reason in {None, "null"}:
                raise ValueError("abstain=true requires a non-null abstain_reason")
        elif self.abstain_reason not in {None, "null"}:
            raise ValueError("abstain=false requires abstain_reason=null")
        return self


def run_phase2_structured_extraction(
    *,
    queue_path: str | Path = DEFAULT_PHASE1_LLM_QUEUE_SAMPLE_PATH,
    candidates_path: str | Path = DEFAULT_PHASE1_CANDIDATES_FULL_PATH,
    features_path: str | Path = DEFAULT_PHASE1_FEATURES_FULL_PATH,
    contexts_path: str | Path = DEFAULT_PHASE1_CONTEXTS_PATH,
    object_mentions_path: str | Path = DEFAULT_PHASE1_OBJECT_MENTIONS_PATH,
    object_graph_candidates_path: str | Path = DEFAULT_PHASE1_OBJECT_GRAPH_CANDIDATES_PATH,
    cited_title_profiles_path: str | Path = DEFAULT_PHASE1_CITED_TITLE_PROFILES_PATH,
    jsonl_out: str | Path = DEFAULT_PHASE2_STRUCTURED_JSONL_PATH,
    parquet_out: str | Path = DEFAULT_PHASE2_STRUCTURED_PARQUET_PATH,
    failed_out: str | Path = DEFAULT_PHASE2_STRUCTURED_FAILED_PATH,
    dry_run_prompts_out: str | Path = DEFAULT_PHASE2_DRY_RUN_PROMPTS_PATH,
    report_path: str | Path = DEFAULT_PHASE2_STRUCTURED_REPORT,
    review_sample_out: str | Path = DEFAULT_PHASE2_REVIEW_SAMPLE_PATH,
    cache_dir: str | Path = DEFAULT_PHASE2_CACHE_DIR,
    limit: int = 600,
    model: str | None = None,
    seed: int = 42,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Run Phase-2 LLM structured evidence extraction for a Phase-1 queue."""
    if limit < 1:
        raise ValueError("limit must be positive")
    input_paths = [
        Path(queue_path),
        Path(candidates_path),
        Path(features_path),
        Path(contexts_path),
        Path(object_mentions_path),
        Path(object_graph_candidates_path),
        Path(cited_title_profiles_path),
    ]
    for path in input_paths:
        if not path.exists():
            raise FileNotFoundError(f"Required input does not exist: {path}")

    review_model = resolve_review_model(model)
    queue = _read_parquet_with_columns(Path(queue_path), _queue_columns())
    candidates = _read_parquet_with_columns(Path(candidates_path), _candidate_fill_columns())
    contexts = _read_parquet_with_columns(Path(contexts_path), _context_fill_columns())
    object_mentions = _read_parquet_with_columns(Path(object_mentions_path), _object_fill_columns())
    object_graph_candidates = _read_parquet_with_columns(
        Path(object_graph_candidates_path),
        _object_fill_columns(),
    )
    cited_title_profiles = _read_parquet_with_columns(
        Path(cited_title_profiles_path),
        _object_fill_columns(),
    )
    phase2_queue = build_phase2_input_queue(
        queue=queue,
        candidates=candidates,
        contexts=contexts,
        object_mentions=object_mentions,
        object_graph_candidates=object_graph_candidates,
        cited_title_profiles=cited_title_profiles,
        limit=limit,
        seed=seed,
        model=review_model,
    )

    jsonl_output = Path(jsonl_out)
    parquet_output = Path(parquet_out)
    failed_output = Path(failed_out)
    dry_run_prompts_output = Path(dry_run_prompts_out)
    report_output = Path(report_path)
    review_sample_output = Path(review_sample_out)
    for output_path in (
        jsonl_output,
        parquet_output,
        failed_output,
        dry_run_prompts_output,
        report_output,
        review_sample_output,
    ):
        output_path.parent.mkdir(parents=True, exist_ok=True)

    if dry_run:
        dry_run_records = write_phase2_dry_run_prompts(phase2_queue, dry_run_prompts_output)
        failed_output.write_text("", encoding="utf-8")
        results = pd.DataFrame(columns=PHASE2_RESULT_COLUMNS)
        failed = pd.DataFrame(columns=PHASE2_FAILED_COLUMNS)
        results.to_parquet(parquet_output, index=False)
        _write_phase2_review_sample(results, review_sample_output, seed=seed)
        metrics = build_phase2_metrics(
            queue=phase2_queue,
            results=results,
            failed=failed,
            dry_run=True,
            dry_run_prompt_records=dry_run_records,
        )
        report_output.write_text(
            build_phase2_report(
                metrics=metrics,
                results=results,
                failed=failed,
                jsonl_out=jsonl_output,
                parquet_out=parquet_output,
                failed_out=failed_output,
                dry_run_prompts_out=dry_run_prompts_output,
                review_sample_out=review_sample_output,
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
    failed_records: list[dict[str, Any]] = []
    with (
        jsonl_output.open("w", encoding="utf-8") as result_handle,
        failed_output.open("w", encoding="utf-8") as failed_handle,
    ):
        for row in phase2_queue.to_dict(orient="records"):
            record, failed_record = extract_phase2_sample_row(
                row=row,
                client=client,
                model=review_model,
                cache_dir=cache_path,
            )
            if record is not None:
                result_records.append(record)
                result_handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            if failed_record is not None:
                failed_records.append(failed_record)
                failed_handle.write(json.dumps(failed_record, ensure_ascii=False) + "\n")

    results = _ensure_columns(pd.DataFrame(result_records), PHASE2_RESULT_COLUMNS)
    failed = _ensure_columns(pd.DataFrame(failed_records), PHASE2_FAILED_COLUMNS)
    results[PHASE2_RESULT_COLUMNS].to_parquet(parquet_output, index=False)
    _write_phase2_review_sample(results, review_sample_output, seed=seed)
    metrics = build_phase2_metrics(
        queue=phase2_queue,
        results=results,
        failed=failed,
        dry_run=False,
        dry_run_prompt_records=0,
    )
    report_output.write_text(
        build_phase2_report(
            metrics=metrics,
            results=results,
            failed=failed,
            jsonl_out=jsonl_output,
            parquet_out=parquet_output,
            failed_out=failed_output,
            dry_run_prompts_out=dry_run_prompts_output,
            review_sample_out=review_sample_output,
            dry_run=False,
        ),
        encoding="utf-8",
    )
    return metrics


def build_phase2_input_queue(
    *,
    queue: pd.DataFrame,
    candidates: pd.DataFrame,
    contexts: pd.DataFrame,
    object_mentions: pd.DataFrame | None = None,
    object_graph_candidates: pd.DataFrame | None = None,
    cited_title_profiles: pd.DataFrame | None = None,
    limit: int = 600,
    seed: int = 42,
    model: str = DEFAULT_OPENAI_REVIEW_MODEL,
) -> pd.DataFrame:
    """Prepare the Phase-2 prompt table from a Phase-1 LLM queue."""
    prepared = _ensure_columns(queue.copy(), _queue_columns())
    prepared = _fill_from_contexts(prepared, contexts)
    prepared = _fill_from_candidates(prepared, candidates)
    prepared = _fill_object_fields_from_tables(
        prepared,
        object_mentions=object_mentions,
        object_graph_candidates=object_graph_candidates,
        cited_title_profiles=cited_title_profiles,
    )
    if len(prepared) > limit:
        prepared = prepared.sample(n=limit, random_state=seed).sort_values("context_id")
    prepared = prepared.drop_duplicates(subset=["context_id"], keep="first").head(limit).copy()
    prepared["prompt_version"] = PHASE2_PROMPT_VERSION
    prepared["model"] = model
    prepared["cache_key"] = prepared.apply(
        lambda row: phase2_structured_cache_key(row.to_dict()),
        axis=1,
    )
    prepared["sample_row_id"] = [
        f"phase2_structured_{index:04d}" for index in range(1, len(prepared) + 1)
    ]
    prepared = _ensure_columns(prepared, PHASE2_INPUT_COLUMNS)
    for column in (
        "context_id",
        "primary_candidate_intent",
        "sentence_text",
        "context_window_s3",
    ):
        prepared[column] = prepared[column].map(_clean)
    return prepared[PHASE2_INPUT_COLUMNS]


def extract_phase2_sample_row(
    *,
    row: dict[str, Any],
    client: Any,
    model: str,
    cache_dir: Path,
    max_attempts: int = 2,
    backoff_base_seconds: float = 1.0,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    """Extract one structured Phase-2 label, using deterministic local cache."""
    cache_key = phase2_structured_cache_key(row)
    cache_file = cache_dir / f"{cache_key}.json"
    if cache_file.exists():
        cached = json.loads(cache_file.read_text(encoding="utf-8"))
        cached["from_cache"] = True
        return cached, None

    validation_error = ""
    raw_response = ""
    usage: dict[str, int | None] = {}
    final_attempt = 0
    for attempt in range(1, max_attempts + 1):
        final_attempt = attempt
        try:
            decision, raw_response, usage = call_openai_phase2_decision(
                client=client,
                row=row,
                model=model,
            )
            validate_phase2_decision(decision, row)
            record = _phase2_result_record_from_decision(
                row=row,
                decision=decision,
                review_status="structured_extracted",
                validation_error="",
                attempts=attempt,
                from_cache=False,
                model_used=model,
                usage=usage,
            )
            cache_file.write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")
            return record, None
        except (ValidationError, ValueError, json.JSONDecodeError) as exc:
            validation_error = str(exc)
        except Exception as exc:  # pragma: no cover - live API/network failures are flaky.
            validation_error = f"{type(exc).__name__}: {exc}"
            if _is_transient_api_error(exc) and attempt < max_attempts:
                _sleep_before_retry(attempt, backoff_base_seconds, cache_key)
                continue
            break

    failed_record = _phase2_failed_record(
        row=row,
        model=model,
        validation_error=validation_error,
        raw_response=raw_response,
        attempts=final_attempt,
    )
    return None, failed_record


def call_openai_phase2_decision(
    *,
    client: Any,
    row: dict[str, Any],
    model: str,
) -> tuple[Phase2StructuredLabel, str, dict[str, int | None]]:
    """Call OpenAI Structured Outputs for one Phase-2 extraction decision."""
    system_prompt, user_prompt = build_phase2_prompt(row)
    response = client.responses.parse(
        model=model,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        text_format=Phase2StructuredLabel,
    )
    parsed = response.output_parsed
    if parsed is None:
        raw = getattr(response, "output_text", "")
        parsed = Phase2StructuredLabel.model_validate_json(raw)
    raw_response = (
        parsed.model_dump_json() if isinstance(parsed, Phase2StructuredLabel) else str(parsed)
    )
    return parsed, raw_response, _usage_to_dict(getattr(response, "usage", None))


def build_phase2_prompt(row: dict[str, Any]) -> tuple[str, str]:
    """Build the system/user prompt pair for Phase-2 structured extraction."""
    system_prompt = (
        "You are performing Phase-2 LLM structured evidence extraction for "
        "citation-function analysis in NLP / Computational Linguistics papers. "
        "This is model-assisted evidence-grounded labeling, not gold human "
        "annotation and not human validation. Return only the structured JSON "
        "object requested by the schema. Use only the provided citation context "
        "as evidence."
    )
    payload = {
        "task": "Phase-2 structured citation-function evidence extraction",
        "prompt_version": row.get("prompt_version", PHASE2_PROMPT_VERSION),
        "core_principle": (
            "Do not assign a strong citation-function label without exact "
            "citation context evidence."
        ),
        "guidelines": [
            "Judge the citation function in the citing paper.",
            "The cited paper title helps identify the cited work but is not itself evidence.",
            "Use only sentence_text and context_window_s3 as evidence fields.",
            "If the context merely describes what cited authors did, label background.",
            "Use uses only for current-paper use, e.g. we use, we employ, our model uses.",
            "Use compares_against for compare, baseline, outperform, versus, benchmark language.",
            "Use extends for current-paper extends, adapts, improves, modifies, builds upon.",
            (
                "Use critiques for explicit limitation, failure, drawback, inability, "
                "poor performance."
            ),
            "Use applies when the current paper applies a method/model/resource to a task/domain.",
            (
                "Generic metrics support report_metric or compares only with "
                "evaluation/compare language."
            ),
            (
                "cited_title_profile_object_names can help identify paper type but must not "
                "be treated as direct context evidence unless the object also appears in "
                "sentence_text or context_window_s3."
            ),
            "Prefer abstain when evidence is insufficient or ambiguous.",
        ],
        "phase1_candidate": _prompt_row_payload(row),
        "required_output_schema": {
            "final_intent": "background|uses|compares_against|extends|critiques|applies|unclear",
            "final_object_type": (
                "method|model|dataset_or_database|software_or_tool|benchmark_or_protocol|"
                "metric|task|theory_or_concept|claim_or_finding|unknown"
            ),
            "final_relation_subtype": (
                "direct_use|adapt_to_domain|combine_with|compare_against|critique_limitation|"
                "improve|replace|component_use|evaluate_on|report_metric|none"
            ),
            "method_edge_type": (
                "extends|improves|replaces|adapts|uses_component|compares|background|"
                "not_method_related"
            ),
            "stance": "neutral|positive|negative|mixed|unclear",
            "evidence_span": (
                "exact substring of sentence_text/context_window_s3, or empty if abstain"
            ),
            "problem_or_motivation_quote": "exact substring or null",
            "usage_or_mechanism_quote": "exact substring or null",
            "comparison_or_tradeoff_quote": "exact substring or null",
            "evidence_supports_label": "true|false|unclear",
            "abstain": "true|false",
            "abstain_reason": (
                "insufficient_evidence|ambiguous_context|grouped_citation|"
                "wrong_phase1_candidate|no_relevant_function|other|null"
            ),
            "confidence": "number between 0 and 1",
            "rationale_short": "brief explanation",
        },
    }
    return system_prompt, json.dumps(payload, ensure_ascii=False, indent=2)


def phase2_structured_cache_key(row: dict[str, Any]) -> str:
    """Deterministic cache key for one Phase-2 structured extraction row."""
    payload = {
        "context_id": _clean(row.get("context_id")),
        "prompt_version": _clean(row.get("prompt_version")) or PHASE2_PROMPT_VERSION,
        "model": _clean(row.get("model")) or DEFAULT_OPENAI_REVIEW_MODEL,
        "primary_candidate_intent": _clean(row.get("primary_candidate_intent")),
        "evidence_span": _clean(row.get("evidence_span")),
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_phase2_decision(decision: Phase2StructuredLabel, row: dict[str, Any]) -> None:
    """Validate Phase-2 model output against exact local evidence rules."""
    sentence = _clean(row.get("sentence_text"))
    context = _clean(row.get("context_window_s3"))
    evidence_fields = [sentence, context]
    evidence = decision.evidence_span.strip()

    if not decision.abstain:
        if decision.evidence_supports_label != "true":
            raise ValueError("non-abstain final labels require evidence_supports_label=true")
        if not evidence:
            raise ValueError("non-abstain labels require non-empty evidence_span")
        if not any(evidence in field for field in evidence_fields):
            raise ValueError("evidence_span is not an exact substring of evidence fields")
    elif evidence and not any(evidence in field for field in evidence_fields):
        raise ValueError("abstain evidence_span, when present, must be an exact substring")

    for field_name in (
        "problem_or_motivation_quote",
        "usage_or_mechanism_quote",
        "comparison_or_tradeoff_quote",
    ):
        quote = getattr(decision, field_name)
        if quote and not any(quote in field for field in evidence_fields):
            raise ValueError(f"{field_name} is not an exact substring of evidence fields")

    if decision.final_intent == "uses" and not _has_current_paper_use_cue(evidence):
        raise ValueError("final_intent=uses requires current-paper use evidence")

    if decision.final_intent == "compares_against" and not _has_compare_cue(evidence):
        raise ValueError("final_intent=compares_against requires compare evidence")

    if decision.final_intent == "extends" and not _has_extend_cue(evidence):
        raise ValueError("final_intent=extends requires extend/adapt/improve evidence")

    if decision.final_intent == "critiques" and not _has_critique_cue(evidence):
        raise ValueError("final_intent=critiques requires explicit critique evidence")

    if decision.final_intent == "applies" and not _has_apply_cue(evidence):
        raise ValueError("final_intent=applies requires apply evidence")

    if (
        _is_cited_title_only_object(row)
        and decision.final_object_type != "unknown"
        and not _local_text_supports_object_type(row, decision.final_object_type)
    ):
        raise ValueError("cited-title-only object type cannot be used as direct evidence")


def write_phase2_dry_run_prompts(sample: pd.DataFrame, jsonl_output: Path) -> int:
    """Write dry-run prompt records without requiring an API key."""
    count = 0
    with jsonl_output.open("w", encoding="utf-8") as handle:
        for row in sample.to_dict(orient="records"):
            system_prompt, user_prompt = build_phase2_prompt(row)
            record = {
                "dry_run": True,
                "cache_key": row.get("cache_key", phase2_structured_cache_key(row)),
                "context_id": row.get("context_id", ""),
                "prompt_version": row.get("prompt_version", PHASE2_PROMPT_VERSION),
                "model": row.get("model", DEFAULT_OPENAI_REVIEW_MODEL),
                "primary_candidate_intent": row.get("primary_candidate_intent", ""),
                "llm_priority": row.get("llm_priority", ""),
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
            }
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1
    return count


def build_phase2_metrics(
    *,
    queue: pd.DataFrame,
    results: pd.DataFrame,
    failed: pd.DataFrame,
    dry_run: bool,
    dry_run_prompt_records: int,
) -> dict[str, Any]:
    """Build aggregate metrics for the Phase-2 structured extraction report."""
    successful_rows = int(len(results))
    failed_rows = int(len(failed))
    processed_rows = successful_rows + failed_rows
    abstain_count = (
        int(results["abstain"].map(_bool_value).sum())
        if "abstain" in results and not results.empty
        else 0
    )
    disagreement = _phase1_phase2_disagreement(results)
    return {
        "dry_run": dry_run,
        "total_queue_rows": int(len(queue)),
        "processed_rows": int(processed_rows),
        "successful_rows": successful_rows,
        "failed_rows": failed_rows,
        "invalid_schema_rows": failed_rows,
        "retry_count": _retry_count(results, failed),
        "dry_run_prompt_records": int(dry_run_prompt_records),
        "from_cache_rows": int(results["from_cache"].sum()) if "from_cache" in results else 0,
        "abstain_count": abstain_count,
        "abstain_rate": _safe_rate(abstain_count, successful_rows),
        "final_intent_distribution": _value_counts(results, ["final_intent"], "rows"),
        "final_object_type_distribution": _value_counts(
            results,
            ["final_object_type"],
            "rows",
        ),
        "final_relation_subtype_distribution": _value_counts(
            results,
            ["final_relation_subtype"],
            "rows",
        ),
        "method_edge_type_distribution": _value_counts(results, ["method_edge_type"], "rows"),
        "evidence_supports_label_distribution": _value_counts(
            results,
            ["evidence_supports_label"],
            "rows",
        ),
        "confidence_distribution": _confidence_distribution(results),
        "final_intent_by_phase1_intent": _value_counts(
            results,
            ["primary_candidate_intent", "final_intent"],
            "rows",
        ),
        "phase1_phase2_disagreement_count": disagreement["count"],
        "phase1_phase2_disagreement_rate": disagreement["rate"],
        "abstain_rate_by_phase1_intent": _abstain_rate_by_group(
            results,
            "primary_candidate_intent",
        ),
        "final_intent_by_normalized_section": _value_counts(
            results,
            ["normalized_section", "final_intent"],
            "rows",
            limit=100,
        ),
        "final_intent_by_object_type": _value_counts(
            results,
            ["final_object_type", "final_intent"],
            "rows",
        ),
        "token_usage": {
            "input_tokens": _sum_numeric(results, "input_tokens"),
            "output_tokens": _sum_numeric(results, "output_tokens"),
            "total_tokens": _sum_numeric(results, "total_tokens"),
        },
    }


def build_phase2_report(
    *,
    metrics: dict[str, Any],
    results: pd.DataFrame,
    failed: pd.DataFrame,
    jsonl_out: Path,
    parquet_out: Path,
    failed_out: Path,
    dry_run_prompts_out: Path = DEFAULT_PHASE2_DRY_RUN_PROMPTS_PATH,
    review_sample_out: Path,
    dry_run: bool,
) -> str:
    """Build markdown report for Phase-2 structured evidence extraction."""
    core = pd.DataFrame(
        [
            {"metric": "dry_run", "value": metrics["dry_run"]},
            {"metric": "total_queue_rows", "value": metrics["total_queue_rows"]},
            {"metric": "processed_rows", "value": metrics["processed_rows"]},
            {"metric": "successful_rows", "value": metrics["successful_rows"]},
            {"metric": "failed_rows", "value": metrics["failed_rows"]},
            {"metric": "invalid_schema_rows", "value": metrics["invalid_schema_rows"]},
            {"metric": "retry_count", "value": metrics["retry_count"]},
            {
                "metric": "dry_run_prompt_records",
                "value": metrics["dry_run_prompt_records"],
            },
            {"metric": "from_cache_rows", "value": metrics["from_cache_rows"]},
            {"metric": "abstain_count", "value": metrics["abstain_count"]},
            {"metric": "abstain_rate", "value": f"{metrics['abstain_rate']:.3f}"},
            {
                "metric": "phase1_phase2_disagreement_count",
                "value": metrics["phase1_phase2_disagreement_count"],
            },
            {
                "metric": "phase1_phase2_disagreement_rate",
                "value": f"{metrics['phase1_phase2_disagreement_rate']:.3f}",
            },
            {"metric": "input_tokens", "value": metrics["token_usage"]["input_tokens"]},
            {"metric": "output_tokens", "value": metrics["token_usage"]["output_tokens"]},
            {"metric": "total_tokens", "value": metrics["token_usage"]["total_tokens"]},
        ]
    )
    sections = [
        "# Phase-2 LLM Structured Evidence Extraction Pilot Report",
        "",
        "This is Phase-2 LLM structured evidence extraction, not human validation "
        "and not gold human annotation.",
        "",
        "## Outputs",
        f"- JSONL labels: `{jsonl_out}`",
        f"- Parquet labels: `{parquet_out}`",
        f"- Failed rows: `{failed_out}`",
        f"- Dry-run prompts: `{dry_run_prompts_out}`",
        f"- Review sample CSV: `{review_sample_out}`",
        "",
        "## Object Field Handling",
        (
            "Object fields are read from the Phase-1 queue/candidates and filled from "
            "`object_mentions`, `object_graph_candidate_mentions`, and "
            "`cited_title_object_profiles` when those queue fields are blank."
        ),
        "",
        "## Core Metrics",
        _table(core),
        "",
        "## Final Intent Distribution",
        _table(metrics["final_intent_distribution"]),
        "",
        "## Final Object Type Distribution",
        _table(metrics["final_object_type_distribution"]),
        "",
        "## Final Relation Subtype Distribution",
        _table(metrics["final_relation_subtype_distribution"]),
        "",
        "## Method Edge Type Distribution",
        _table(metrics["method_edge_type_distribution"]),
        "",
        "## Evidence Supports Label Distribution",
        _table(metrics["evidence_supports_label_distribution"]),
        "",
        "## Confidence Distribution",
        _table(metrics["confidence_distribution"]),
        "",
        "## Final Intent By Phase-1 Primary Candidate Intent",
        _table(metrics["final_intent_by_phase1_intent"]),
        "",
        "## Abstain Rate By Phase-1 Intent",
        _table(metrics["abstain_rate_by_phase1_intent"]),
        "",
        "## Final Intent By Normalized Section",
        _table(metrics["final_intent_by_normalized_section"]),
        "",
        "## Final Intent By Object Type",
        _table(metrics["final_intent_by_object_type"]),
        "",
        "## Example Uses",
        _table(_phase2_examples(results, "uses", 5)),
        "",
        "## Example Compares Against",
        _table(_phase2_examples(results, "compares_against", 5)),
        "",
        "## Example Extends",
        _table(_phase2_examples(results, "extends", 5)),
        "",
        "## Example Critiques",
        _table(_phase2_examples(results, "critiques", 5)),
        "",
        "## Example Applies",
        _table(_phase2_examples(results, "applies", 5)),
        "",
        "## Example Background",
        _table(_phase2_examples(results, "background", 5)),
        "",
        "## Example Abstain",
        _table(_abstain_examples(results, 5)),
        "",
        "## Phase-1 Wrong But Phase-2 Corrected Examples",
        _table(_corrected_examples(results, 5)),
        "",
        "## Failed Row Examples",
        _table(
            failed.head(20) if not failed.empty else pd.DataFrame(columns=PHASE2_FAILED_COLUMNS)
        ),
        "",
    ]
    if dry_run:
        sections.extend(
            [
                "## Dry Run Note",
                (
                    "No API calls were made. The dry-run prompts JSONL contains prompt "
                    "records only, not structured labels."
                ),
                "",
            ]
        )
    return "\n".join(sections)


def _phase2_result_record_from_decision(
    *,
    row: dict[str, Any],
    decision: Phase2StructuredLabel,
    review_status: str,
    validation_error: str,
    attempts: int,
    from_cache: bool,
    model_used: str,
    usage: dict[str, int | None],
) -> dict[str, Any]:
    sample_part = {column: row.get(column, "") for column in PHASE2_INPUT_COLUMNS}
    return {
        **sample_part,
        "final_intent": decision.final_intent,
        "final_object_type": decision.final_object_type,
        "final_relation_subtype": decision.final_relation_subtype,
        "method_edge_type": decision.method_edge_type,
        "stance": decision.stance,
        "evidence_span_phase2": decision.evidence_span,
        "problem_or_motivation_quote": decision.problem_or_motivation_quote,
        "usage_or_mechanism_quote": decision.usage_or_mechanism_quote,
        "comparison_or_tradeoff_quote": decision.comparison_or_tradeoff_quote,
        "evidence_supports_label": decision.evidence_supports_label,
        "abstain": decision.abstain,
        "abstain_reason": decision.abstain_reason or "null",
        "phase2_confidence": decision.confidence,
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


def _phase2_failed_record(
    *,
    row: dict[str, Any],
    model: str,
    validation_error: str,
    raw_response: str,
    attempts: int,
) -> dict[str, Any]:
    return {
        "context_id": _clean(row.get("context_id")),
        "cache_key": phase2_structured_cache_key(row),
        "prompt_version": _clean(row.get("prompt_version")) or PHASE2_PROMPT_VERSION,
        "model": model,
        "primary_candidate_intent": _clean(row.get("primary_candidate_intent")),
        "validation_error": _truncate(validation_error, 2000),
        "raw_response": _truncate(raw_response, 4000),
        "attempts": attempts,
    }


def _write_phase2_review_sample(results: pd.DataFrame, output: Path, *, seed: int) -> None:
    sample = build_phase2_review_sample(results, seed=seed)
    sample.to_csv(output, index=False)


def build_phase2_review_sample(
    results: pd.DataFrame,
    *,
    seed: int = 42,
    limit: int = 300,
) -> pd.DataFrame:
    """Build a reviewer-facing CSV sample stratified by final_intent and abstain."""
    if results.empty:
        return pd.DataFrame(columns=PHASE2_REVIEW_SAMPLE_COLUMNS)
    prepared = results.copy()
    prepared["evidence_span"] = prepared["evidence_span_phase2"]
    prepared["confidence"] = prepared["phase2_confidence"]
    groups = [
        group
        for _, group in prepared.groupby(["abstain", "final_intent"], dropna=False)
        if not group.empty
    ]
    if not groups:
        sample = prepared.head(0)
    else:
        quota = max(1, limit // len(groups))
        parts = [
            group.sample(n=min(quota, len(group)), random_state=seed + index)
            for index, group in enumerate(groups)
        ]
        sample = pd.concat(parts, ignore_index=True)
        if len(sample) < min(limit, len(prepared)):
            remaining = prepared.loc[~prepared["context_id"].isin(sample["context_id"])]
            fill = remaining.sample(
                n=min(limit - len(sample), len(remaining)),
                random_state=seed + 100,
            )
            sample = pd.concat([sample, fill], ignore_index=True)
    sample = sample.drop_duplicates(subset=["context_id"], keep="first").head(limit).copy()
    sample["reviewer_correct"] = ""
    sample["reviewer_notes"] = ""
    sample = _ensure_columns(sample, PHASE2_REVIEW_SAMPLE_COLUMNS)
    return sample[PHASE2_REVIEW_SAMPLE_COLUMNS]


def _fill_from_contexts(queue: pd.DataFrame, contexts: pd.DataFrame) -> pd.DataFrame:
    context_columns = [
        "context_id",
        "source_context_id",
        "citing_paper_id",
        "resolved_cited_acl_id",
        "resolved_cited_title",
        "resolved_cited_year",
        "resolved_cited_authors",
        "normalized_section",
        "raw_section_name",
        "citation_marker",
        "sentence_text",
        "context_window_s3",
    ]
    context_frame = _ensure_columns(contexts.copy(), context_columns)[context_columns]
    context_frame = context_frame.drop_duplicates(subset=["context_id"])
    merged = queue.merge(
        context_frame,
        on="context_id",
        how="left",
        suffixes=("", "_context"),
    )
    for column in context_columns:
        if column == "context_id":
            continue
        context_column = f"{column}_context"
        if context_column in merged:
            merged[column] = _fill_empty(merged[column], merged[context_column])
            merged = merged.drop(columns=[context_column])
    return merged


def _fill_from_candidates(queue: pd.DataFrame, candidates: pd.DataFrame) -> pd.DataFrame:
    candidate_columns = [column for column in _queue_columns() if column in candidates.columns]
    if "context_id" not in candidate_columns:
        return queue
    candidate_frame = candidates[candidate_columns].drop_duplicates(subset=["context_id"])
    merged = queue.merge(
        candidate_frame,
        on="context_id",
        how="left",
        suffixes=("", "_candidate"),
    )
    for column in candidate_columns:
        if column == "context_id":
            continue
        candidate_column = f"{column}_candidate"
        if candidate_column in merged:
            merged[column] = _fill_empty(merged[column], merged[candidate_column])
            merged = merged.drop(columns=[candidate_column])
    return merged


def _fill_object_fields_from_tables(
    queue: pd.DataFrame,
    *,
    object_mentions: pd.DataFrame | None,
    object_graph_candidates: pd.DataFrame | None,
    cited_title_profiles: pd.DataFrame | None,
) -> pd.DataFrame:
    merged = queue.copy()
    object_summary = _object_summary(object_mentions)
    if not object_summary.empty:
        merged = merged.merge(object_summary, on="context_id", how="left")
        for column in ("object_names", "generic_metric_names"):
            merged[column] = _fill_empty(merged[column], merged[f"{column}_from_objects"])
            merged = merged.drop(columns=[f"{column}_from_objects"])
        merged["object_types"] = _fill_empty_or_unknown(
            merged["object_types"],
            merged["object_types_from_objects"],
        )
        merged = merged.drop(columns=["object_types_from_objects"])

    graph_summary = _object_summary(object_graph_candidates)
    if not graph_summary.empty:
        graph_summary = graph_summary.rename(
            columns={"object_names_from_objects": "graph_candidate_object_names_from_graph"}
        )
        keep_columns = ["context_id", "graph_candidate_object_names_from_graph"]
        merged = merged.merge(graph_summary[keep_columns], on="context_id", how="left")
        merged["graph_candidate_object_names"] = _fill_empty(
            merged["graph_candidate_object_names"],
            merged["graph_candidate_object_names_from_graph"],
        )
        merged = merged.drop(columns=["graph_candidate_object_names_from_graph"])

    title_summary = _object_summary(cited_title_profiles)
    if not title_summary.empty:
        title_summary = title_summary.rename(
            columns={
                "object_names_from_objects": "cited_title_profile_object_names_from_profiles"
            }
        )
        keep_columns = ["context_id", "cited_title_profile_object_names_from_profiles"]
        merged = merged.merge(title_summary[keep_columns], on="context_id", how="left")
        merged["cited_title_profile_object_names"] = _fill_empty(
            merged["cited_title_profile_object_names"],
            merged["cited_title_profile_object_names_from_profiles"],
        )
        merged = merged.drop(columns=["cited_title_profile_object_names_from_profiles"])
    return merged


def _object_summary(frame: pd.DataFrame | None) -> pd.DataFrame:
    columns = [
        "context_id",
        "object_names_from_objects",
        "object_types_from_objects",
        "generic_metric_names_from_objects",
    ]
    if frame is None or frame.empty:
        return pd.DataFrame(columns=columns)
    prepared = _ensure_columns(frame.copy(), _object_fill_columns())
    if prepared.empty:
        return pd.DataFrame(columns=columns)
    prepared["canonical_name"] = prepared["canonical_name"].map(_clean)
    prepared["object_type"] = prepared["object_type"].map(_clean)
    prepared["object_category"] = prepared["object_category"].map(_clean)
    prepared = prepared.loc[prepared["context_id"].map(_clean).ne("")]
    rows = []
    for context_id, group in prepared.groupby("context_id", dropna=False):
        rows.append(
            {
                "context_id": context_id,
                "object_names_from_objects": _join_unique(group["canonical_name"]),
                "object_types_from_objects": _join_unique(group["object_type"]),
                "generic_metric_names_from_objects": _join_unique(
                    group.loc[
                        group["object_category"].eq("generic_metric")
                        | group["object_type"].eq("metric"),
                        "canonical_name",
                    ]
                ),
            }
        )
    return pd.DataFrame(rows, columns=columns)


def _read_parquet_with_columns(path: Path, columns: list[str]) -> pd.DataFrame:
    available = set(pq.read_schema(path).names)
    read_columns = [column for column in columns if column in available]
    frame = pd.read_parquet(path, columns=read_columns)
    return _ensure_columns(frame, columns)


def _queue_columns() -> list[str]:
    return [
        "context_id",
        "source_context_id",
        "citing_paper_id",
        "resolved_cited_acl_id",
        "resolved_cited_title",
        "resolved_cited_year",
        "resolved_cited_authors",
        "normalized_section",
        "raw_section_name",
        "citation_marker",
        "sentence_text",
        "context_window_s3",
        "object_names",
        "object_types",
        "graph_candidate_object_names",
        "generic_metric_names",
        "cited_title_profile_object_names",
        "primary_candidate_intent",
        "candidate_intents",
        "primary_candidate_object_type",
        "object_type_source",
        "object_type_confidence",
        "candidate_relation_subtypes",
        "evidence_span",
        "confidence",
        "llm_priority",
        "llm_reason",
        "phase2_candidate_type",
        "cited_work_description",
        "phase1_reason",
        "matched_rules",
    ]


def _candidate_fill_columns() -> list[str]:
    return _queue_columns()


def _context_fill_columns() -> list[str]:
    return [
        "context_id",
        "source_context_id",
        "citing_paper_id",
        "resolved_cited_acl_id",
        "resolved_cited_title",
        "resolved_cited_year",
        "resolved_cited_authors",
        "normalized_section",
        "raw_section_name",
        "citation_marker",
        "sentence_text",
        "context_window_s3",
    ]


def _object_fill_columns() -> list[str]:
    return ["context_id", "canonical_name", "object_type", "object_category"]


def _prompt_row_payload(row: dict[str, Any]) -> dict[str, Any]:
    return {column: _clean(row.get(column)) for column in PHASE2_INPUT_COLUMNS}


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


def _is_transient_api_error(exc: Exception) -> bool:
    name = type(exc).__name__
    transient_names = (
        "RateLimitError",
        "APITimeoutError",
        "APIConnectionError",
        "InternalServerError",
        "ServiceUnavailableError",
        "TimeoutError",
        "ConnectionError",
    )
    if any(token in name for token in transient_names):
        return True
    status_code = getattr(exc, "status_code", None)
    return isinstance(status_code, int) and (status_code == 429 or status_code >= 500)


def _sleep_before_retry(attempt: int, base_seconds: float, cache_key: str) -> None:
    if base_seconds <= 0:
        return
    jitter_seed = f"{cache_key}:{attempt}".encode()
    jitter = random.Random(jitter_seed).uniform(0, base_seconds / 2)
    time.sleep((base_seconds * (2 ** (attempt - 1))) + jitter)


def _phase1_phase2_disagreement(results: pd.DataFrame) -> dict[str, float | int]:
    if results.empty:
        return {"count": 0, "rate": 0.0}
    eligible = results.loc[~results["abstain"].map(_bool_value)].copy()
    if eligible.empty:
        return {"count": 0, "rate": 0.0}
    count = int(
        eligible["primary_candidate_intent"].fillna("").astype(str).ne(
            eligible["final_intent"].fillna("").astype(str)
        ).sum()
    )
    return {"count": count, "rate": _safe_rate(count, len(eligible))}


def _abstain_rate_by_group(results: pd.DataFrame, column: str) -> pd.DataFrame:
    output_columns = [column, "rows", "abstain_count", "abstain_rate"]
    if results.empty or column not in results:
        return pd.DataFrame(columns=output_columns)
    frame = results.copy()
    frame[column] = frame[column].fillna("unavailable").astype(str)
    frame["is_abstain"] = frame["abstain"].map(_bool_value)
    grouped = (
        frame.groupby(column, dropna=False)
        .agg(rows=("context_id", "size"), abstain_count=("is_abstain", "sum"))
        .reset_index()
    )
    grouped["abstain_rate"] = grouped.apply(
        lambda row: f"{int(row['abstain_count']) / int(row['rows']):.3f}",
        axis=1,
    )
    return grouped.sort_values("rows", ascending=False)


def _confidence_distribution(results: pd.DataFrame) -> pd.DataFrame:
    if results.empty or "phase2_confidence" not in results:
        return pd.DataFrame(columns=["confidence_bin", "rows"])
    scores = pd.to_numeric(results["phase2_confidence"], errors="coerce").fillna(0)
    bins = pd.cut(
        scores,
        bins=[-0.001, 0.2, 0.5, 0.7, 0.85, 1.0],
        labels=["[0,0.2]", "(0.2,0.5]", "(0.5,0.7]", "(0.7,0.85]", "(0.85,1.0]"],
    )
    return bins.value_counts(sort=False).rename_axis("confidence_bin").reset_index(name="rows")


def _retry_count(results: pd.DataFrame, failed: pd.DataFrame) -> int:
    count = 0
    for frame in (results, failed):
        if "attempts" in frame:
            attempts = pd.to_numeric(frame["attempts"], errors="coerce").fillna(0).astype(int)
            count += int((attempts - 1).clip(lower=0).sum())
    return count


def _phase2_examples(results: pd.DataFrame, intent: str, limit: int) -> pd.DataFrame:
    if results.empty:
        return _empty_examples()
    mask = results["final_intent"].eq(intent) & ~results["abstain"].map(_bool_value)
    return _format_examples(results.loc[mask], limit)


def _abstain_examples(results: pd.DataFrame, limit: int) -> pd.DataFrame:
    if results.empty:
        return _empty_examples()
    return _format_examples(results.loc[results["abstain"].map(_bool_value)], limit)


def _corrected_examples(results: pd.DataFrame, limit: int) -> pd.DataFrame:
    if results.empty:
        return _empty_examples()
    mask = (
        ~results["abstain"].map(_bool_value)
        & results["primary_candidate_intent"].fillna("").astype(str).ne(
            results["final_intent"].fillna("").astype(str)
        )
    )
    return _format_examples(results.loc[mask], limit)


def _format_examples(frame: pd.DataFrame, limit: int) -> pd.DataFrame:
    columns = [
        "context_id",
        "primary_candidate_intent",
        "final_intent",
        "final_object_type",
        "final_relation_subtype",
        "evidence_span_phase2",
        "phase2_confidence",
        "abstain",
        "rationale_short",
        "sentence_text",
    ]
    if frame.empty:
        return pd.DataFrame(columns=columns)
    sample = _ensure_columns(frame.head(limit).copy(), columns)
    for column in ("sentence_text", "rationale_short", "evidence_span_phase2"):
        sample[column] = sample[column].map(lambda value: _truncate(_clean(value), 220))
    return sample[columns]


def _empty_examples() -> pd.DataFrame:
    return pd.DataFrame(
        columns=[
            "context_id",
            "primary_candidate_intent",
            "final_intent",
            "final_object_type",
            "final_relation_subtype",
            "evidence_span_phase2",
            "phase2_confidence",
            "abstain",
            "rationale_short",
            "sentence_text",
        ]
    )


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
        return "_No rows._"
    return frame.to_markdown(index=False)


def _fill_empty(left: pd.Series, right: pd.Series) -> pd.Series:
    left_text = left.fillna("").astype(str)
    right_text = right.fillna("").astype(str)
    return left_text.where(left_text.str.strip().ne(""), right_text)


def _fill_empty_or_unknown(left: pd.Series, right: pd.Series) -> pd.Series:
    left_text = left.fillna("").astype(str)
    right_text = right.fillna("").astype(str)
    keep_left = left_text.str.strip().ne("") & ~left_text.str.strip().str.lower().eq("unknown")
    return left_text.where(keep_left, right_text)


def _join_unique(values: pd.Series) -> str:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        text = _clean(value)
        if not text or text in seen:
            continue
        seen.add(text)
        output.append(text)
    return ";".join(output)


def _ensure_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        if column not in df.columns:
            df[column] = ""
    return df


def _clean(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


def _bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None or pd.isna(value):
        return False
    return str(value).strip().lower() in {"true", "1", "yes"}


def _sum_numeric(frame: pd.DataFrame, column: str) -> int:
    if column not in frame or frame.empty:
        return 0
    return int(pd.to_numeric(frame[column], errors="coerce").fillna(0).sum())


def _safe_rate(numerator: int, denominator: int) -> float:
    return float(numerator / denominator) if denominator else 0.0


def _truncate(value: str, length: int) -> str:
    text = _clean(value).replace("\n", " ")
    return text if len(text) <= length else f"{text[: length - 3]}..."


def _contains_any(text: str, cues: tuple[str, ...]) -> bool:
    lowered = text.casefold()
    return any(cue in lowered for cue in cues)


def _has_current_paper_use_cue(text: str) -> bool:
    return _contains_any(
        text,
        (
            "we use",
            "we used",
            "we follow",
            "we followed",
            "we employ",
            "we employed",
            "we utilize",
            "we utilized",
            "we apply",
            "we applied",
            "we adopt",
            "we adopted",
            "we leverage",
            "we leveraged",
            "we incorporate",
            "we incorporated",
            "we initialize",
            "we initialized",
            "we make use of",
            "we rely on",
            "we train with",
            "we trained with",
            "we evaluate on",
            "we evaluated on",
            "our model uses",
            "our system uses",
            "using the",
            "using a",
            "using an",
            "using our",
            "in our experiments, we use",
        ),
    )


def _has_compare_cue(text: str) -> bool:
    lowered = text.casefold()
    if any(cue in lowered for cue in ("better", "worse", "higher", "lower")) and "than" in lowered:
        return True
    if "improve" in lowered and "over" in lowered:
        return True
    return _contains_any(
        text,
        (
            "compare",
            "compared",
            "comparison",
            "baseline",
            "outperform",
            "better than",
            "worse than",
            "versus",
            " vs ",
            "benchmark",
            "competitive with",
            "relative to",
        ),
    )


def _has_extend_cue(text: str) -> bool:
    return _contains_any(
        text,
        (
            "extend",
            "extends",
            "extended",
            "adapt",
            "adapts",
            "adapted",
            "improve",
            "improves",
            "improved",
            "generalize",
            "generalizes",
            "generalized",
            "modify",
            "modified",
            "build upon",
            "builds upon",
            "built upon",
            "variant of",
            "extension of",
            "our extension",
        ),
    )


def _has_critique_cue(text: str) -> bool:
    return _contains_any(
        text,
        (
            "fail",
            "fails",
            "failed",
            "suffer",
            "suffers",
            "suffered",
            "cannot",
            "can not",
            "unable",
            "limitation",
            "limited",
            "drawback",
            "poor",
            "worse",
            "does not",
            "do not",
            "not able",
            "problem with",
        ),
    )


def _has_apply_cue(text: str) -> bool:
    return _contains_any(
        text,
        (
            "we apply",
            "we applied",
            "we use",
            "we used",
            "applied to",
            "apply",
            "applies",
            "application of",
            "to the task",
            "to this task",
            "to our task",
            "for tagging",
            "for parsing",
            "for classification",
        ),
    )


def _is_cited_title_only_object(row: dict[str, Any]) -> bool:
    if _clean(row.get("object_type_source")) != "cited_title_profile":
        return False
    if _clean(row.get("object_names")) or _clean(row.get("graph_candidate_object_names")):
        return False
    profile_names = [
        name.strip()
        for name in _clean(row.get("cited_title_profile_object_names")).split(";")
        if name.strip()
    ]
    if not profile_names:
        return False
    evidence_text = f"{_clean(row.get('sentence_text'))} {_clean(row.get('context_window_s3'))}"
    return not any(name.casefold() in evidence_text.casefold() for name in profile_names)


def _local_text_supports_object_type(row: dict[str, Any], object_type: str) -> bool:
    text = f"{_clean(row.get('sentence_text'))} {_clean(row.get('context_window_s3'))}".casefold()
    cues_by_type = {
        "method": ("method", "technique", "approach", "algorithm", "procedure"),
        "model": ("model", "architecture", "network", "encoder", "decoder", "embedding"),
        "dataset_or_database": ("dataset", "data set", "corpus", "treebank", "database"),
        "software_or_tool": ("tool", "toolkit", "software", "package", "system"),
        "benchmark_or_protocol": ("benchmark", "protocol", "task", "evaluation"),
        "metric": ("metric", "score", "accuracy", "f1", "bleu", "rouge", "perplexity"),
        "task": ("task",),
        "theory_or_concept": ("theory", "concept", "framework"),
        "claim_or_finding": ("finding", "result", "claim"),
    }
    return any(cue in text for cue in cues_by_type.get(object_type, ()))
