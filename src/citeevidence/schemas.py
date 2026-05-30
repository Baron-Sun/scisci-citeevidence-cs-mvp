from __future__ import annotations

import hashlib
from enum import StrEnum
from typing import Annotated, Any, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
MetadataValue = str | int | float | bool | None


class AttributionStatus(StrEnum):
    SINGLE_CITATION_CLEAR = "single_citation_clear"
    MULTI_CITATION_GROUP = "multi_citation_group"
    CITATION_RANGE = "citation_range"
    BIBLIOGRAPHY_UNRESOLVED = "bibliography_unresolved"
    PARSER_ERROR = "parser_error"


class Intent(StrEnum):
    BACKGROUND = "background"
    USES = "uses"
    COMPARES_AGAINST = "compares_against"
    EXTENDS = "extends"
    CRITIQUES = "critiques"
    APPLIES = "applies"


class ObjectType(StrEnum):
    METHOD = "method"
    DATASET_OR_DATABASE = "dataset_or_database"
    SOFTWARE_OR_TOOL = "software_or_tool"
    BENCHMARK_OR_PROTOCOL = "benchmark_or_protocol"
    METRIC = "metric"
    CLAIM_OR_FINDING = "claim_or_finding"
    THEORY_OR_CONCEPT = "theory_or_concept"


class RelationSubtype(StrEnum):
    DIRECT_USE = "direct_use"
    ADAPT_TO_DOMAIN = "adapt_to_domain"
    COMBINE_WITH = "combine_with"
    COMPARE_AGAINST = "compare_against"
    CRITIQUE_LIMITATION = "critique_limitation"
    IMPROVE = "improve"
    REPLACE = "replace"
    COMPONENT_USE = "component_use"


class MethodEdgeType(StrEnum):
    EXTENDS = "extends"
    IMPROVES = "improves"
    REPLACES = "replaces"
    ADAPTS = "adapts"
    USES_COMPONENT = "uses_component"
    COMPARES = "compares"
    BACKGROUND = "background"
    NOT_METHOD_RELATED = "not_method_related"


class EvidenceValidationError(ValueError):
    """Raised when an evidence span or quote cannot be grounded in context text."""


class BaseRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")


class PaperRecord(BaseRecord):
    paper_id: NonEmptyStr
    title: NonEmptyStr
    year: int | None = Field(default=None, ge=0)
    doi: NonEmptyStr | None = None
    venue: NonEmptyStr | None = None
    authors: list[NonEmptyStr] = Field(default_factory=list)
    source_dataset: NonEmptyStr | None = None
    license: NonEmptyStr | None = None
    metadata: dict[str, MetadataValue] = Field(default_factory=dict)


class ReferenceRecord(BaseRecord):
    citing_paper_id: NonEmptyStr
    reference_key: NonEmptyStr
    cited_paper_id: NonEmptyStr | None = None
    cited_title: NonEmptyStr | None = None
    cited_year: int | None = Field(default=None, ge=0)
    cited_doi: NonEmptyStr | None = None
    raw_reference_text: NonEmptyStr | None = None
    source_dataset: NonEmptyStr | None = None
    metadata: dict[str, MetadataValue] = Field(default_factory=dict)


class CitationContext(BaseRecord):
    context_id: NonEmptyStr
    citing_paper_id: NonEmptyStr
    reference_key: NonEmptyStr
    cited_title: NonEmptyStr | None = None
    cited_year: int | None = Field(default=None, ge=0)
    cited_doi: NonEmptyStr | None = None
    section: NonEmptyStr | None = None
    paragraph_id: NonEmptyStr
    citation_marker: NonEmptyStr
    sentence_text: NonEmptyStr
    context_window_s3: NonEmptyStr
    context_window_paragraph: NonEmptyStr
    citation_group_size: int = Field(ge=1)
    attribution_status: AttributionStatus

    def contains_span(self, span: str) -> bool:
        return _span_in_context(span, self.context_window_s3, self.context_window_paragraph)


class CitationContextLabel(BaseRecord):
    context_id: NonEmptyStr
    intent: Intent | None = None
    object_type: ObjectType | None = None
    relation_subtype: RelationSubtype | None = None
    method_edge_type: MethodEdgeType | None = None
    evidence_span: NonEmptyStr | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    abstain: bool
    label_source: NonEmptyStr
    matched_rules: list[NonEmptyStr] = Field(default_factory=list)
    model_version: NonEmptyStr | None = None
    prompt_version: NonEmptyStr | None = None

    @model_validator(mode="after")
    def validate_label_requirements(self) -> Self:
        if self.abstain:
            return self
        if self.intent is None:
            raise ValueError("intent is required when abstain=False")
        if self.object_type is None:
            raise ValueError("object_type is required when abstain=False")
        if self.evidence_span is None:
            raise ValueError("evidence_span is required when abstain=False")
        return self


class ObjectRegistryEntry(BaseRecord):
    object_id: NonEmptyStr
    canonical_name: NonEmptyStr
    object_type: ObjectType
    source_paper_id: NonEmptyStr | None = None
    aliases: list[NonEmptyStr] = Field(default_factory=list)
    description: NonEmptyStr | None = None
    evidence_context_ids: list[NonEmptyStr] = Field(default_factory=list)
    metadata: dict[str, MetadataValue] = Field(default_factory=dict)


class ObjectMention(BaseRecord):
    mention_id: NonEmptyStr
    context_id: NonEmptyStr
    mention_text: NonEmptyStr
    object_id: NonEmptyStr | None = None
    object_type: ObjectType | None = None
    char_start: int | None = Field(default=None, ge=0)
    char_end: int | None = Field(default=None, ge=0)
    confidence: float = Field(ge=0.0, le=1.0)

    @model_validator(mode="after")
    def validate_offsets(self) -> Self:
        if self.char_start is None or self.char_end is None:
            return self
        if self.char_end <= self.char_start:
            raise ValueError("char_end must be greater than char_start")
        return self


class StructuredEvidenceRecord(BaseRecord):
    context_id: NonEmptyStr
    intent: Intent | None = None
    object_type: ObjectType | None = None
    relation_subtype: RelationSubtype | None = None
    method_edge_type: MethodEdgeType | None = None
    evidence_span: NonEmptyStr | None = None
    problem_or_motivation_quote: NonEmptyStr | None = None
    usage_or_mechanism_quote: NonEmptyStr | None = None
    comparison_or_tradeoff_quote: NonEmptyStr | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    abstain: bool

    @model_validator(mode="after")
    def validate_evidence_requirements(self) -> Self:
        if self.abstain:
            return self
        if self.intent is None:
            raise ValueError("intent is required when abstain=False")
        if self.object_type is None:
            raise ValueError("object_type is required when abstain=False")
        if self.evidence_span is None:
            raise ValueError("evidence_span is required when abstain=False")
        return self


class ValidatedEvidenceRecord(StructuredEvidenceRecord):
    context_window_s3: NonEmptyStr
    context_window_paragraph: NonEmptyStr
    attribution_status: AttributionStatus
    disambiguation_note: NonEmptyStr | None = None

    @model_validator(mode="after")
    def validate_grounding_and_attribution(self) -> Self:
        if not self.abstain and self.evidence_span is not None:
            _require_span_in_context(
                span=self.evidence_span,
                span_name="evidence_span",
                context_window_s3=self.context_window_s3,
                context_window_paragraph=self.context_window_paragraph,
            )

        for field_name in (
            "problem_or_motivation_quote",
            "usage_or_mechanism_quote",
            "comparison_or_tradeoff_quote",
        ):
            quote = getattr(self, field_name)
            if quote is not None:
                _require_span_in_context(
                    span=quote,
                    span_name=field_name,
                    context_window_s3=self.context_window_s3,
                    context_window_paragraph=self.context_window_paragraph,
                )

        needs_cap = self.attribution_status in {
            AttributionStatus.MULTI_CITATION_GROUP,
            AttributionStatus.CITATION_RANGE,
        }
        if needs_cap and self.confidence > 0.7 and self.disambiguation_note is None:
            raise ValueError(
                "confidence must be <= 0.7 for grouped/ranged citations unless "
                "disambiguation_note exists"
            )
        return self

    @classmethod
    def from_context_and_evidence(
        cls,
        context: CitationContext,
        evidence: StructuredEvidenceRecord,
        *,
        disambiguation_note: str | None = None,
    ) -> Self:
        return cls(
            **evidence.model_dump(),
            context_window_s3=context.context_window_s3,
            context_window_paragraph=context.context_window_paragraph,
            attribution_status=context.attribution_status,
            disambiguation_note=disambiguation_note,
        )

    @classmethod
    def from_context_and_label(
        cls,
        context: CitationContext,
        label: CitationContextLabel,
        *,
        disambiguation_note: str | None = None,
    ) -> Self:
        return cls(
            context_id=label.context_id,
            intent=label.intent,
            object_type=label.object_type,
            relation_subtype=label.relation_subtype,
            method_edge_type=label.method_edge_type,
            evidence_span=label.evidence_span,
            confidence=label.confidence,
            abstain=label.abstain,
            context_window_s3=context.context_window_s3,
            context_window_paragraph=context.context_window_paragraph,
            attribution_status=context.attribution_status,
            disambiguation_note=disambiguation_note,
        )


class HumanValidationRecord(BaseRecord):
    validation_id: NonEmptyStr
    context_id: NonEmptyStr
    validator_id: NonEmptyStr
    accepted: bool
    corrected_intent: Intent | None = None
    corrected_object_type: ObjectType | None = None
    corrected_relation_subtype: RelationSubtype | None = None
    corrected_method_edge_type: MethodEdgeType | None = None
    corrected_evidence_span: NonEmptyStr | None = None
    notes: NonEmptyStr | None = None


class CitedPaperUseSummary(BaseRecord):
    cited_paper_id: NonEmptyStr | None = None
    cited_title: NonEmptyStr | None = None
    cited_year: int | None = Field(default=None, ge=0)
    total_contexts: int = Field(ge=0)
    intent_counts: dict[Intent, int] = Field(default_factory=dict)
    object_type_counts: dict[ObjectType, int] = Field(default_factory=dict)
    method_edge_type_counts: dict[MethodEdgeType, int] = Field(default_factory=dict)
    high_confidence_context_ids: list[NonEmptyStr] = Field(default_factory=list)
    abstained_context_ids: list[NonEmptyStr] = Field(default_factory=list)

    @field_validator("intent_counts", "object_type_counts", "method_edge_type_counts")
    @classmethod
    def validate_nonnegative_counts(cls, counts: dict[Any, int]) -> dict[Any, int]:
        if any(count < 0 for count in counts.values()):
            raise ValueError("summary counts must be nonnegative")
        return counts


def make_context_id(
    *,
    citing_paper_id: str,
    reference_key: str,
    paragraph_id: str,
    citation_marker: str,
    sentence_text: str,
) -> str:
    """Build a stable context identifier from citation-local source fields."""
    payload = "\x1f".join(
        [
            citing_paper_id.strip(),
            reference_key.strip(),
            paragraph_id.strip(),
            citation_marker.strip(),
            " ".join(sentence_text.split()),
        ]
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"ctx_{digest}"


def _span_in_context(
    span: str,
    context_window_s3: str,
    context_window_paragraph: str,
) -> bool:
    return span in context_window_s3 or span in context_window_paragraph


def _require_span_in_context(
    *,
    span: str,
    span_name: str,
    context_window_s3: str,
    context_window_paragraph: str,
) -> None:
    if not _span_in_context(span, context_window_s3, context_window_paragraph):
        raise EvidenceValidationError(
            f"{span_name} must be an exact substring of context_window_s3 "
            "or context_window_paragraph"
        )


__all__ = [
    "AttributionStatus",
    "CitedPaperUseSummary",
    "CitationContext",
    "CitationContextLabel",
    "EvidenceValidationError",
    "HumanValidationRecord",
    "Intent",
    "MethodEdgeType",
    "ObjectMention",
    "ObjectRegistryEntry",
    "ObjectType",
    "PaperRecord",
    "ReferenceRecord",
    "RelationSubtype",
    "StructuredEvidenceRecord",
    "ValidatedEvidenceRecord",
    "make_context_id",
]
