from citeevidence.final_release.qa import (
    validate_citation_context_volume_terms,
    validate_forbidden_claims,
    validate_required_caveats,
)

GOOD_REPORT_TEXT = """
Phase-2 was run on the full high/medium Phase-1 queue, not all strong contexts.
Labels are LLM-assisted, schema-validated, evidence-grounded labels, not human gold
annotations. The object graph is a curated seed-registry object-use graph, not the
full universe of NLP methods. Current outputs are not a complete NLP method evolution
graph and are not an Intern-Atlas-scale method evolution graph.
Ranking tables use citation-context volume, not graph in-degree.
"""


def test_required_caveats_are_recognized_in_acceptable_report_text() -> None:
    assert validate_required_caveats(GOOD_REPORT_TEXT) == []


def test_missing_required_caveats_are_reported() -> None:
    missing = validate_required_caveats("This report has useful figures.")

    assert set(missing) == {
        "phase2_scope",
        "label_status",
        "seed_registry_graph",
        "not_method_evolution_graph",
    }


def test_forbidden_claims_are_caught() -> None:
    text = """
    These are human gold labels. Phase-2 was run on the full dataset.
    All strong contexts were Phase-2 labeled. This is a complete NLP method evolution graph.
    The project builds an Intern-Atlas-scale graph.
    """

    findings = validate_forbidden_claims(text)

    assert "human_gold_labels" in findings
    assert "phase2_full_dataset" in findings
    assert "all_strong_contexts_labeled" in findings
    assert "complete_method_evolution_graph" in findings
    assert "intern_atlas_scale_graph" in findings


def test_citation_context_volume_terms() -> None:
    assert validate_citation_context_volume_terms("citation-context volume rank") == []
    assert "citation_count" in validate_citation_context_volume_terms(
        "Rank by total_strong_contexts citation count."
    )
    assert "ambiguous_citation_volume" in validate_citation_context_volume_terms(
        "Final-release ranking reversal uses citation volume."
    )
    assert "slash_citation_context_volume" in validate_citation_context_volume_terms(
        "Citation/context volume is ambiguous."
    )
