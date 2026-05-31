import pytest
from pydantic import ValidationError

from citeevidence.final_release.claims import ClaimRecord, EvidenceRecord


def test_evidence_record_validates_minimal_good_record() -> None:
    record = EvidenceRecord(
        claim_id="C1",
        evidence_key="labels_per_strong_context",
        metric="analysis-ready labels / strong contexts",
        value="19.4%",
        source_table="f01_evidence_pipeline.csv",
    )

    assert record.claim_id == "C1"
    assert record.interpretation == ""


def test_claim_record_validates_minimal_good_record() -> None:
    record = ClaimRecord(
        claim_id="C1",
        research_claim="Citation-context volume is not the same as evidence use.",
        support_status="supported_with_scope",
        key_result="Evidence labels are downstream of the high/medium Phase-1 queue.",
        primary_artifact="f01_evidence_pipeline.csv",
        caveat="Phase-2 covers high/medium Phase-1 queue contexts, not all strong contexts.",
    )

    assert record.primary_artifact == "f01_evidence_pipeline.csv"


def test_claim_and_evidence_records_reject_empty_required_text() -> None:
    with pytest.raises(ValidationError):
        EvidenceRecord(
            claim_id="",
            evidence_key="metric",
            metric="metric",
            value="1",
            source_table="source.csv",
        )

    with pytest.raises(ValidationError):
        ClaimRecord(
            claim_id="C1",
            research_claim="",
            support_status="supported",
            key_result="result",
            primary_artifact="source.csv",
            caveat="caveat",
        )
