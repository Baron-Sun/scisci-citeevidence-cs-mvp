"""Lightweight schemas for final-release claims and supporting evidence."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, field_validator


class EvidenceRecord(BaseModel):
    """A bounded evidence metric that supports a release claim."""

    model_config = ConfigDict(extra="forbid")

    claim_id: str
    evidence_key: str
    metric: str
    value: str
    source_table: str
    interpretation: str = ""

    @field_validator("claim_id", "evidence_key", "metric", "value", "source_table")
    @classmethod
    def require_text(cls, value: str) -> str:
        """Reject empty required text fields."""
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("required text field cannot be empty")
        return cleaned


class ClaimRecord(BaseModel):
    """A release claim with an explicit caveat and source artifact."""

    model_config = ConfigDict(extra="forbid")

    claim_id: str
    research_claim: str
    support_status: str
    key_result: str
    primary_artifact: str
    caveat: str

    @field_validator(
        "claim_id",
        "research_claim",
        "support_status",
        "key_result",
        "primary_artifact",
        "caveat",
    )
    @classmethod
    def require_text(cls, value: str) -> str:
        """Reject empty required text fields."""
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("required text field cannot be empty")
        return cleaned
