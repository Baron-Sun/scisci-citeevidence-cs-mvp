"""Scientific guardrails for final-release reports and documentation."""

from __future__ import annotations

import re
from collections.abc import Callable

import pandas as pd

REQUIRED_CAVEATS = {
    "phase2_scope": (
        "Phase-2 covers the full high/medium Phase-1 queue, not all strong contexts "
        "or the full dataset."
    ),
    "label_status": (
        "Labels are LLM-assisted, schema-validated, evidence-grounded labels, "
        "not human gold annotations."
    ),
    "seed_registry_graph": (
        "Object graph claims are over a curated seed-registry object-use graph, "
        "not the full universe of NLP methods."
    ),
    "not_method_evolution_graph": (
        "Current outputs are not a complete NLP method evolution graph or "
        "Intern-Atlas-scale graph."
    ),
}

FORBIDDEN_CLAIMS = {
    "human_gold_labels": "human gold labels",
    "phase2_full_dataset": "Phase-2 was run on the full dataset",
    "all_strong_contexts_labeled": "all strong contexts were Phase-2 labeled",
    "complete_method_evolution_graph": "complete NLP method evolution graph",
    "intern_atlas_scale_graph": "Intern-Atlas-scale graph",
    "citation_count": "citation count",
    "ambiguous_citation_volume": "citation volume",
    "slash_citation_context_volume": "citation/context volume",
}

_ALLOWED_NEGATED_CAVEAT_PATTERNS = [
    re.compile(
        r"\bnot\s+a\s+complete\s+nlp\s+method\s+evolution\s+graph\s+"
        r"or\s+intern-atlas-scale\s+graph\b"
    ),
    re.compile(r"\bnot\s+an\s+intern-atlas-scale\s+method\s+evolution\s+graph\b"),
    re.compile(r"\bnot\s+intern-atlas-scale(?:\s+graph)?\b"),
]
_LOCAL_NEGATION_PREFIX = re.compile(
    r"(?:^|[\s(,;:])(?:not|no|never|do not|don't)\s+(?:(?:a|an|the)\s+)?$"
)

_CONFIDENCE_COLUMNS = ["confidence", "analysis_confidence", "phase2_confidence"]
_EVIDENCE_SPAN_COLUMNS = ["evidence_span", "analysis_evidence_span", "evidence_span_phase2"]
_FAILURE_CATEGORY_COLUMNS = [
    "failed_validator_type",
    "validator_failure_type",
    "failure_type",
    "error_type",
]
_REVIEWER_COLUMNS = [
    "reviewer_final_intent_correct",
    "reviewer_evidence_supports_label",
    "reviewer_object_type_correct",
    "reviewer_relation_subtype_correct",
    "reviewer_should_exclude",
    "reviewer_notes",
]
_QA_SAMPLE_TARGETS = {
    "background": 80,
    "uses": 80,
    "compares_against": 80,
    "critiques": 70,
    "extends": 60,
    "applies": 40,
    "confidence_boundary_near_0_70": 40,
    "multi_object_or_policy_risk": 50,
}
_QA_SAMPLE_SELECTION_ORDER = [
    "multi_object_or_policy_risk",
    "confidence_boundary_near_0_70",
    "background",
    "uses",
    "compares_against",
    "critiques",
    "extends",
    "applies",
]


def validate_required_caveats(text: str) -> list[str]:
    """Return required caveat identifiers whose meaning is missing from text."""
    normalized = _normalize(text)
    checks: dict[str, Callable[[str], bool]] = {
        "phase2_scope": _has_phase2_scope_caveat,
        "label_status": _has_label_status_caveat,
        "seed_registry_graph": _has_seed_registry_graph_caveat,
        "not_method_evolution_graph": _has_not_method_evolution_graph_caveat,
    }
    return [key for key, check in checks.items() if not check(normalized)]


def validate_forbidden_claims(text: str) -> list[str]:
    """Return forbidden claim identifiers found in text."""
    normalized = _normalize(text)
    findings = [
        key
        for key, phrase in FORBIDDEN_CLAIMS.items()
        if _contains_unqualified_phrase(normalized, _normalize(phrase))
    ]
    for issue in validate_citation_context_volume_terms(text):
        if issue not in findings:
            findings.append(issue)
    return findings


def validate_citation_context_volume_terms(text: str) -> list[str]:
    """Detect forbidden terminology for context-volume ranking language."""
    normalized = _normalize(text)
    findings: list[str] = []
    if _contains_unqualified_phrase(normalized, "citation count"):
        findings.append("citation_count")
    if _contains_unqualified_phrase(normalized, "citation volume"):
        findings.append("ambiguous_citation_volume")
    if _contains_unqualified_phrase(normalized, "citation/context volume"):
        findings.append("slash_citation_context_volume")
    return findings


def validate_evidence_grounding(labels: pd.DataFrame) -> pd.DataFrame:
    """Add evidence-grounding QA columns to a final-label table."""
    frame = labels.copy()
    frame["unified_evidence_span"] = _coalesce_text_columns(frame, _EVIDENCE_SPAN_COLUMNS)
    frame["evidence_span_present"] = frame["unified_evidence_span"].ne("")

    sentence_text = _text_series(frame, "sentence_text")
    context_window = _text_series(frame, "context_window_s3")
    frame["evidence_span_grounded"] = [
        bool(span) and (span in sentence or span in context)
        for span, sentence, context in zip(
            frame["unified_evidence_span"],
            sentence_text,
            context_window,
            strict=True,
        )
    ]
    frame["evidence_supports_label_bool"] = _bool_series(frame, "evidence_supports_label")
    frame["abstain_bool"] = _bool_series(frame, "abstain")
    frame["analysis_ready_bool"] = _bool_series(frame, "analysis_ready")
    frame["confidence_numeric"] = _coalesce_numeric_columns(frame, _CONFIDENCE_COLUMNS)
    return frame


def build_label_quality_summary(
    labels: pd.DataFrame,
    excluded: pd.DataFrame | None = None,
    failed_diagnostics: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Build a tidy QA summary for final analysis-ready label tables."""
    frame = validate_evidence_grounding(labels)
    grounded = frame["evidence_span_grounded"]
    present = frame["evidence_span_present"]
    confidence = frame["confidence_numeric"].dropna()
    rows: list[dict[str, object]] = []

    def add(metric: str, value: object, note: str = "") -> None:
        rows.append({"metric": metric, "value": value, "note": note})

    add("total_labels", len(frame))
    if "analysis_ready" in labels:
        add("analysis_ready_rows", int(frame["analysis_ready_bool"].sum()))
    else:
        add("analysis_ready_rows", pd.NA, "analysis_ready column not present")
    add("evidence_span_present_rows", int(present.sum()))
    add("evidence_span_grounded_rows", int(grounded.sum()))
    add(
        "evidence_span_not_grounded_rows",
        int((present & ~grounded).sum()),
        "Rows with a non-empty evidence span that is not an exact substring.",
    )
    add("evidence_supports_label_true_rows", int(frame["evidence_supports_label_bool"].sum()))
    add("abstain_true_rows", int(frame["abstain_bool"].sum()))
    add("mean_confidence", float(confidence.mean()) if not confidence.empty else pd.NA)
    if excluded is not None:
        add("excluded_rows", len(excluded))
    if failed_diagnostics is not None:
        add("remaining_failed_rows", _remaining_failed_rows(failed_diagnostics))
    add("distinct_final_intents", _distinct_non_empty(frame, "final_intent"))
    if "normalized_section" in frame:
        add("distinct_sections", _distinct_non_empty(frame, "normalized_section"))
    return pd.DataFrame(rows, columns=["metric", "value", "note"])


def summarize_confidence_by_intent(labels: pd.DataFrame) -> pd.DataFrame:
    """Summarize confidence distributions by final citation intent."""
    frame = validate_evidence_grounding(labels)
    frame["final_intent"] = _text_series(frame, "final_intent")
    frame = frame.loc[frame["final_intent"].ne("")].copy()
    columns = [
        "final_intent",
        "rows",
        "mean_confidence",
        "median_confidence",
        "min_confidence",
        "max_confidence",
        "share_below_0_7",
    ]
    if frame.empty:
        return pd.DataFrame(columns=columns)

    rows = []
    for intent, group in frame.groupby("final_intent", sort=True):
        confidence = group["confidence_numeric"].dropna()
        rows.append(
            {
                "final_intent": intent,
                "rows": len(group),
                "mean_confidence": _confidence_stat(confidence, "mean"),
                "median_confidence": _confidence_stat(confidence, "median"),
                "min_confidence": _confidence_stat(confidence, "min"),
                "max_confidence": _confidence_stat(confidence, "max"),
                "share_below_0_7": _confidence_share_below(confidence, 0.7),
            }
        )
    return pd.DataFrame(rows, columns=columns)


def summarize_failure_categories(failed_diagnostics: pd.DataFrame | None) -> pd.DataFrame:
    """Summarize failed-label diagnostics by the best available failure column."""
    columns = ["failure_category", "rows", "row_share"]
    if failed_diagnostics is None or failed_diagnostics.empty:
        return pd.DataFrame(columns=columns)

    frame = failed_diagnostics.copy()
    category_column = next(
        (column for column in _FAILURE_CATEGORY_COLUMNS if column in frame),
        None,
    )
    if category_column is None:
        categories = pd.Series("unknown", index=frame.index)
    else:
        categories = _text_series(frame, category_column).replace("", "unknown")
    counts = categories.value_counts(dropna=False).rename_axis("failure_category").reset_index()
    counts.columns = ["failure_category", "rows"]
    counts["row_share"] = counts["rows"] / len(frame)
    return counts[columns].sort_values(
        ["rows", "failure_category"],
        ascending=[False, True],
    ).reset_index(drop=True)


def build_stratified_qa_sample(
    labels: pd.DataFrame,
    n: int = 500,
    seed: int = 42,
) -> pd.DataFrame:
    """Build a deterministic reviewer-facing stratified QA sample."""
    frame = validate_evidence_grounding(labels)
    frame["final_intent"] = _text_series(frame, "final_intent")
    targets = _scaled_sample_targets(n)
    selected_context_ids: set[str] = set()
    samples: list[pd.DataFrame] = []
    shortfalls: list[str] = []

    for offset, stratum in enumerate(_QA_SAMPLE_SELECTION_ORDER):
        target = min(targets[stratum], max(n - sum(len(sample) for sample in samples), 0))
        if target <= 0:
            continue
        candidates, stratum_shortfall, randomize = _qa_stratum_candidates(frame, stratum)
        if stratum_shortfall:
            shortfalls.append(stratum_shortfall)
        sample = _take_qa_sample(
            candidates,
            target=target,
            selected_context_ids=selected_context_ids,
            seed=seed + offset,
            randomize=randomize,
        )
        if len(sample) < target:
            shortfalls.append(f"{stratum}: requested {target}, selected {len(sample)}")
        if sample.empty:
            continue
        sample = sample.copy()
        sample["sample_stratum"] = stratum
        selected_context_ids.update(
            context_id
            for context_id in _text_series(sample, "context_id")
            if context_id
        )
        samples.append(sample)

    if samples:
        output = pd.concat(samples, ignore_index=True)
        temp_columns = [column for column in output if column.startswith("_qa_")]
        output = output.drop(columns=temp_columns)
    else:
        output = frame.head(0).copy()
        output["sample_stratum"] = pd.Series(dtype=object)

    for column in _REVIEWER_COLUMNS:
        output[column] = ""
    output["sample_shortfall"] = "; ".join(dict.fromkeys(shortfalls))
    return output


def _remaining_failed_rows(failed_diagnostics: pd.DataFrame) -> int:
    if "revalidated" not in failed_diagnostics:
        return len(failed_diagnostics)
    revalidated = failed_diagnostics["revalidated"].map(_parse_bool).astype(bool)
    return int((~revalidated).sum())


def _coalesce_text_columns(frame: pd.DataFrame, columns: list[str]) -> pd.Series:
    result = pd.Series("", index=frame.index, dtype=object)
    for column in columns:
        if column not in frame:
            continue
        candidate = _text_series(frame, column)
        result = result.where(result.ne(""), candidate)
    return result


def _coalesce_numeric_columns(frame: pd.DataFrame, columns: list[str]) -> pd.Series:
    result = pd.Series(pd.NA, index=frame.index, dtype="Float64")
    for column in columns:
        if column not in frame:
            continue
        candidate = pd.to_numeric(frame[column], errors="coerce").astype("Float64")
        result = result.where(result.notna(), candidate)
    return result


def _text_series(frame: pd.DataFrame, column: str) -> pd.Series:
    if column not in frame:
        return pd.Series("", index=frame.index, dtype=object)
    return frame[column].map(_clean_text_value)


def _bool_series(frame: pd.DataFrame, column: str) -> pd.Series:
    if column not in frame:
        return pd.Series(False, index=frame.index, dtype=bool)
    return frame[column].map(_parse_bool).astype(bool)


def _parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    try:
        if pd.isna(value):
            return False
    except (TypeError, ValueError):
        pass
    if isinstance(value, int | float):
        return value != 0
    return str(value).strip().casefold() in {"1", "t", "true", "y", "yes"}


def _distinct_non_empty(frame: pd.DataFrame, column: str) -> int:
    values = _text_series(frame, column)
    return int(values.loc[values.ne("")].nunique())


def _confidence_stat(confidence: pd.Series, method: str) -> float | object:
    if confidence.empty:
        return pd.NA
    return float(getattr(confidence, method)())


def _confidence_share_below(confidence: pd.Series, threshold: float) -> float:
    if confidence.empty:
        return 0.0
    return float(confidence.lt(threshold).mean())


def _scaled_sample_targets(n: int) -> dict[str, int]:
    if n <= 0:
        return {stratum: 0 for stratum in _QA_SAMPLE_TARGETS}
    total = sum(_QA_SAMPLE_TARGETS.values())
    raw_targets = {
        stratum: target * n / total
        for stratum, target in _QA_SAMPLE_TARGETS.items()
    }
    targets = {stratum: int(raw) for stratum, raw in raw_targets.items()}
    remaining = n - sum(targets.values())
    strata_by_remainder = sorted(
        _QA_SAMPLE_TARGETS,
        key=lambda stratum: (
            raw_targets[stratum] - targets[stratum],
            _QA_SAMPLE_TARGETS[stratum],
            stratum,
        ),
        reverse=True,
    )
    for stratum in strata_by_remainder[:remaining]:
        targets[stratum] += 1
    return targets


def _qa_stratum_candidates(frame: pd.DataFrame, stratum: str) -> tuple[pd.DataFrame, str, bool]:
    if stratum in {"background", "uses", "compares_against", "critiques", "extends", "applies"}:
        return frame.loc[frame["final_intent"].eq(stratum)].copy(), "", True
    if stratum == "confidence_boundary_near_0_70":
        confidence = frame["confidence_numeric"]
        distance = (confidence - 0.70).abs()
        candidates = frame.loc[confidence.notna() & distance.le(0.05)].copy()
        candidates["_qa_boundary_distance"] = distance.loc[candidates.index]
        candidates = candidates.sort_values(
            ["_qa_boundary_distance", "confidence_numeric"],
            ascending=[True, True],
        )
        return candidates, "", False
    if stratum == "multi_object_or_policy_risk":
        return _risk_candidates(frame)
    return frame.head(0).copy(), f"{stratum}: unknown stratum", False


def _risk_candidates(frame: pd.DataFrame) -> tuple[pd.DataFrame, str, bool]:
    has_object_count = "object_count" in frame
    has_candidate_rank = "object_candidate_rank" in frame
    has_matched_in = "matched_in" in frame
    if not any([has_object_count, has_candidate_rank, has_matched_in]):
        return (
            frame.head(0).copy(),
            "multi_object_or_policy_risk: missing risk columns",
            False,
        )

    risk_score = pd.Series(0, index=frame.index, dtype=int)
    if has_object_count:
        risk_score += (
            pd.to_numeric(frame["object_count"], errors="coerce")
            .fillna(0)
            .gt(1)
            .astype(int)
        )
    if has_candidate_rank:
        rank = pd.to_numeric(frame["object_candidate_rank"], errors="coerce").fillna(1)
        risk_score += rank.gt(1).astype(int)
    if has_matched_in:
        matched_in = _text_series(frame, "matched_in").str.casefold()
        risk_score += (matched_in.ne("") & matched_in.ne("sentence_text")).astype(int)

    candidates = frame.loc[risk_score.gt(0)].copy()
    candidates["_qa_risk_score"] = risk_score.loc[candidates.index]
    candidates = candidates.sort_values(
        ["_qa_risk_score", "confidence_numeric"],
        ascending=[False, True],
    )
    shortfall = "" if not candidates.empty else "multi_object_or_policy_risk: no risk rows"
    return candidates, shortfall, False


def _take_qa_sample(
    candidates: pd.DataFrame,
    *,
    target: int,
    selected_context_ids: set[str],
    seed: int,
    randomize: bool,
) -> pd.DataFrame:
    if target <= 0 or candidates.empty:
        return candidates.head(0).copy()

    if "context_id" in candidates:
        context_ids = _text_series(candidates, "context_id")
        unused = candidates.loc[~context_ids.isin(selected_context_ids)].copy()
        pool = unused if not unused.empty else candidates
    else:
        pool = candidates

    take = min(target, len(pool))
    if randomize:
        return pool.sample(n=take, random_state=seed)
    return pool.head(take).copy()


def _clean_text_value(value: object) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()


def _has_phase2_scope_caveat(text: str) -> bool:
    has_queue_scope = all(token in text for token in ["phase-2", "high/medium", "phase-1", "queue"])
    has_not_full_scope = any(
        phrase in text
        for phrase in [
            "not all strong contexts",
            "not every strong context",
            "not all 1.18m strong contexts",
            "not the full dataset",
        ]
    )
    return has_queue_scope and has_not_full_scope


def _has_label_status_caveat(text: str) -> bool:
    has_positive_status = all(
        token in text
        for token in ["llm-assisted", "schema-validated", "evidence-grounded"]
    )
    has_not_human_gold = any(
        phrase in text
        for phrase in ["not human gold", "not human-gold", "not gold annotations"]
    )
    return has_positive_status and has_not_human_gold


def _has_seed_registry_graph_caveat(text: str) -> bool:
    has_seed_registry = "seed" in text and "registry" in text
    has_object_use = "object-use graph" in text or "object use graph" in text
    has_not_universe = any(
        phrase in text
        for phrase in [
            "not the full universe of nlp methods",
            "not a complete nlp method universe",
            "not complete nlp method universe",
        ]
    )
    return has_seed_registry and has_object_use and has_not_universe


def _has_not_method_evolution_graph_caveat(text: str) -> bool:
    has_not_complete = any(
        phrase in text
        for phrase in [
            "not a complete nlp method evolution graph",
            "not a completed intern-atlas-scale method evolution graph",
            "not an intern-atlas-scale method evolution graph",
            "not intern-atlas-scale",
        ]
    )
    has_evolution_context = "method evolution graph" in text or "intern-atlas-scale" in text
    return has_not_complete and has_evolution_context


def _contains_unqualified_phrase(text: str, phrase: str) -> bool:
    for match in re.finditer(re.escape(phrase), text):
        if _is_allowed_negated_caveat(text, match.start(), match.end()):
            continue
        prefix = text[max(0, match.start() - 24) : match.start()]
        if _LOCAL_NEGATION_PREFIX.search(prefix):
            continue
        return True
    return False


def _is_allowed_negated_caveat(text: str, start: int, end: int) -> bool:
    for pattern in _ALLOWED_NEGATED_CAVEAT_PATTERNS:
        for match in pattern.finditer(text):
            if match.start() <= start and end <= match.end():
                return True
    return False


def _normalize(text: str) -> str:
    normalized = (
        text.casefold()
        .replace("phase 2", "phase-2")
        .replace("phase 1", "phase-1")
        .replace("human gold", "human gold")
        .replace("human-gold", "human-gold")
        .replace("schema validated", "schema-validated")
        .replace("evidence grounded", "evidence-grounded")
        .replace("llm assisted", "llm-assisted")
    )
    return re.sub(r"\s+", " ", normalized).strip()
