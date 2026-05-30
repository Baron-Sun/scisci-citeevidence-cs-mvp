from __future__ import annotations

import pytest
from pydantic import ValidationError

from citeevidence.schemas import (
    AttributionStatus,
    CitationContext,
    CitationContextLabel,
    Intent,
    MethodEdgeType,
    ObjectType,
    RelationSubtype,
    StructuredEvidenceRecord,
    ValidatedEvidenceRecord,
    make_context_id,
)


def _context(
    *,
    attribution_status: AttributionStatus = AttributionStatus.SINGLE_CITATION_CLEAR,
    citation_group_size: int = 1,
) -> CitationContext:
    sentence_text = "We use the Transformer architecture for sequence modeling."
    context_id = make_context_id(
        citing_paper_id="paper-001",
        reference_key="vaswani-2017",
        paragraph_id="p3",
        citation_marker="(Vaswani et al., 2017)",
        sentence_text=sentence_text,
    )
    return CitationContext(
        context_id=context_id,
        citing_paper_id="paper-001",
        reference_key="vaswani-2017",
        cited_title="Attention Is All You Need",
        cited_year=2017,
        cited_doi="10.5555/example",
        section="Methods",
        paragraph_id="p3",
        citation_marker="(Vaswani et al., 2017)",
        sentence_text=sentence_text,
        context_window_s3=(
            "Prior work introduced attention-only models. "
            "We use the Transformer architecture for sequence modeling. "
            "This avoids recurrent components."
        ),
        context_window_paragraph=(
            "In our method, we use the Transformer architecture for sequence modeling "
            "because it provides parallel training and strong contextual representations."
        ),
        citation_group_size=citation_group_size,
        attribution_status=attribution_status,
    )


def _evidence(**overrides: object) -> StructuredEvidenceRecord:
    values = {
        "context_id": _context().context_id,
        "intent": Intent.USES,
        "object_type": ObjectType.METHOD,
        "relation_subtype": RelationSubtype.DIRECT_USE,
        "method_edge_type": MethodEdgeType.USES_COMPONENT,
        "evidence_span": "use the Transformer architecture",
        "problem_or_motivation_quote": None,
        "usage_or_mechanism_quote": "Transformer architecture",
        "comparison_or_tradeoff_quote": None,
        "confidence": 0.92,
        "abstain": False,
    }
    values.update(overrides)
    return StructuredEvidenceRecord(**values)


def test_valid_context() -> None:
    context = _context()

    assert context.context_id.startswith("ctx_")
    assert context.contains_span("Transformer architecture")
    assert context.attribution_status is AttributionStatus.SINGLE_CITATION_CLEAR


def test_valid_label() -> None:
    label = CitationContextLabel(
        context_id=_context().context_id,
        intent=Intent.USES,
        object_type=ObjectType.METHOD,
        relation_subtype=RelationSubtype.DIRECT_USE,
        method_edge_type=MethodEdgeType.USES_COMPONENT,
        evidence_span="use the Transformer architecture",
        confidence=0.9,
        abstain=False,
        label_source="rules",
        matched_rules=["uses-pattern"],
        model_version=None,
        prompt_version=None,
    )

    assert label.intent is Intent.USES
    assert label.object_type is ObjectType.METHOD


def test_invalid_evidence_span() -> None:
    context = _context()
    evidence = _evidence(evidence_span="not present in the context")

    with pytest.raises(ValidationError, match="evidence_span"):
        ValidatedEvidenceRecord.from_context_and_evidence(context, evidence)


def test_valid_abstain_label() -> None:
    label = CitationContextLabel(
        context_id=_context().context_id,
        intent=None,
        object_type=None,
        relation_subtype=None,
        method_edge_type=None,
        evidence_span=None,
        confidence=0.0,
        abstain=True,
        label_source="rules",
        matched_rules=[],
        model_version=None,
        prompt_version=None,
    )

    assert label.abstain is True
    assert label.intent is None
    assert label.object_type is None


def test_grouped_citation_confidence_cap() -> None:
    context = _context(
        attribution_status=AttributionStatus.MULTI_CITATION_GROUP,
        citation_group_size=2,
    )
    evidence = _evidence(confidence=0.95, context_id=context.context_id)

    with pytest.raises(ValidationError, match="confidence must be <= 0.7"):
        ValidatedEvidenceRecord.from_context_and_evidence(context, evidence)

    validated = ValidatedEvidenceRecord.from_context_and_evidence(
        context,
        evidence,
        disambiguation_note="The sentence explicitly names the cited Transformer method.",
    )
    assert validated.confidence == 0.95


def test_invalid_quote_field() -> None:
    context = _context()
    evidence = _evidence(usage_or_mechanism_quote="a quote that is not grounded")

    with pytest.raises(ValidationError, match="usage_or_mechanism_quote"):
        ValidatedEvidenceRecord.from_context_and_evidence(context, evidence)
