"""Final-release analysis scaffolding for SciSci-CiteEvidence."""

from citeevidence.final_release.claims import ClaimRecord, EvidenceRecord
from citeevidence.final_release.io import ensure_directory, maybe_read_csv, write_source_csv
from citeevidence.final_release.metrics import (
    add_shrunk_evidence_use_share,
    build_paper_evidence_use_table,
    compute_ranking_reversal,
    filter_ranking_reversal_eligible,
)
from citeevidence.final_release.qa import (
    FORBIDDEN_CLAIMS,
    REQUIRED_CAVEATS,
    build_label_quality_summary,
    build_stratified_qa_sample,
    summarize_confidence_by_intent,
    summarize_failure_categories,
    validate_citation_context_volume_terms,
    validate_evidence_grounding,
    validate_forbidden_claims,
    validate_required_caveats,
)

__all__ = [
    "ClaimRecord",
    "EvidenceRecord",
    "FORBIDDEN_CLAIMS",
    "REQUIRED_CAVEATS",
    "add_shrunk_evidence_use_share",
    "build_label_quality_summary",
    "build_paper_evidence_use_table",
    "build_stratified_qa_sample",
    "compute_ranking_reversal",
    "ensure_directory",
    "filter_ranking_reversal_eligible",
    "maybe_read_csv",
    "summarize_confidence_by_intent",
    "summarize_failure_categories",
    "validate_citation_context_volume_terms",
    "validate_evidence_grounding",
    "validate_forbidden_claims",
    "validate_required_caveats",
    "write_source_csv",
]
