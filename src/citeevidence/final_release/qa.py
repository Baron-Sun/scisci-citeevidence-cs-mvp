"""Scientific guardrails for final-release reports and documentation."""

from __future__ import annotations

import re
from collections.abc import Callable

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
        prefix = text[max(0, match.start() - 32) : match.start()]
        if any(marker in prefix for marker in ["not ", "no ", "never ", "do not ", "don't "]):
            continue
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
