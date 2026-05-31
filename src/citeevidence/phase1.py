from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import pyarrow.parquet as pq

DEFAULT_PHASE1_CONTEXTS_PATH = Path("data/processed/analysis_ready_strong_contexts.parquet")
DEFAULT_PHASE1_OBJECT_MENTIONS_PATH = Path("data/processed/object_mentions.parquet")
DEFAULT_PHASE1_OBJECT_GRAPH_CANDIDATES_PATH = Path(
    "data/processed/object_graph_candidate_mentions.parquet"
)
DEFAULT_PHASE1_CITED_TITLE_PROFILES_PATH = Path(
    "data/processed/cited_title_object_profiles.parquet"
)
DEFAULT_PHASE1_CANDIDATES_PILOT_PATH = Path(
    "data/processed/phase1_citation_function_candidates_pilot.parquet"
)
DEFAULT_PHASE1_FEATURES_PILOT_PATH = Path("data/processed/phase1_context_features_pilot.parquet")
DEFAULT_PHASE1_REPORT_PILOT_PATH = Path(
    "reports/phase1_citation_function_screening_pilot_report.md"
)
DEFAULT_PHASE1_LIMIT = 100_000

CONTEXT_COLUMNS = [
    "context_id",
    "source_context_id",
    "citing_paper_id",
    "resolved_cited_acl_id",
    "resolved_cited_title",
    "normalized_section",
    "raw_section_name",
    "citation_marker",
    "sentence_text",
    "context_window_s3",
]

OBJECT_COLUMNS = [
    "context_id",
    "object_id",
    "canonical_name",
    "object_type",
    "object_category",
    "graph_eligible",
    "phase1_feature_eligible",
]

OUTPUT_COLUMNS = [
    *CONTEXT_COLUMNS,
    "has_object_mention",
    "has_graph_candidate_object",
    "object_ids",
    "object_names",
    "object_types",
    "graph_candidate_object_ids",
    "graph_candidate_object_names",
    "generic_metric_names",
    "cited_title_profile_object_names",
    "matched_use_cues",
    "matched_compare_cues",
    "matched_extend_cues",
    "matched_critique_cues",
    "matched_apply_cues",
    "matched_background_cues",
    "matched_evaluation_cues",
    "evidence_span",
    "candidate_intents",
    "primary_candidate_intent",
    "candidate_object_types",
    "primary_candidate_object_type",
    "candidate_relation_subtypes",
    "confidence",
    "should_send_to_llm",
    "phase1_reason",
    "matched_rules",
]

FEATURE_COLUMNS = [
    "context_id",
    "source_context_id",
    "normalized_section",
    "has_object_mention",
    "has_graph_candidate_object",
    "object_ids",
    "object_names",
    "object_types",
    "graph_candidate_object_ids",
    "graph_candidate_object_names",
    "generic_metric_names",
    "cited_title_profile_object_names",
    "matched_use_cues",
    "matched_compare_cues",
    "matched_extend_cues",
    "matched_critique_cues",
    "matched_apply_cues",
    "matched_background_cues",
    "matched_evaluation_cues",
    "evidence_span",
    "matched_rules",
]

HIGH_VALUE_SECTIONS = {
    "method",
    "model",
    "implementation",
    "system_description",
    "dataset",
    "experiment",
    "evaluation",
    "results",
    "error_analysis",
}

BACKGROUND_SECTIONS = {"introduction", "related_work", "background"}
CRITIQUE_SECTIONS = {"discussion", "error_analysis"}
CONCLUSION_SECTIONS = {"conclusion"}


@dataclass(frozen=True)
class CuePattern:
    label: str
    pattern: re.Pattern[str]
    relation_subtype: str | None = None


USE_CUES = [
    CuePattern("we use", re.compile(r"\bwe\s+use\b", re.IGNORECASE), "direct_use"),
    CuePattern("we used", re.compile(r"\bwe\s+used\b", re.IGNORECASE), "direct_use"),
    CuePattern("we employ", re.compile(r"\bwe\s+employ\b", re.IGNORECASE), "direct_use"),
    CuePattern("we employed", re.compile(r"\bwe\s+employed\b", re.IGNORECASE), "direct_use"),
    CuePattern("we adopt", re.compile(r"\bwe\s+adopt\b", re.IGNORECASE), "direct_use"),
    CuePattern("we adopted", re.compile(r"\bwe\s+adopted\b", re.IGNORECASE), "direct_use"),
    CuePattern("we utilize", re.compile(r"\bwe\s+utili[sz]e\b", re.IGNORECASE), "direct_use"),
    CuePattern("we apply", re.compile(r"\bwe\s+appl(?:y|ied)\b", re.IGNORECASE), "direct_use"),
    CuePattern("based on", re.compile(r"\bbased\s+on\b", re.IGNORECASE), "direct_use"),
    CuePattern("following", re.compile(r"\bfollowing\b", re.IGNORECASE), "direct_use"),
    CuePattern("using", re.compile(r"\busing\b", re.IGNORECASE), "direct_use"),
    CuePattern("trained with", re.compile(r"\btrained\s+with\b", re.IGNORECASE), "direct_use"),
    CuePattern(
        "implemented using",
        re.compile(r"\bimplemented\s+using\b", re.IGNORECASE),
        "component_use",
    ),
    CuePattern("built on", re.compile(r"\bbuilt\s+on\b", re.IGNORECASE), "direct_use"),
    CuePattern(
        "initialized with",
        re.compile(r"\binitiali[sz]ed\s+with\b", re.IGNORECASE),
        "component_use",
    ),
]

EVALUATION_CUES = [
    CuePattern("evaluated on", re.compile(r"\bevaluated\s+on\b", re.IGNORECASE), "evaluate_on"),
    CuePattern("trained on", re.compile(r"\btrained\s+on\b", re.IGNORECASE), "evaluate_on"),
    CuePattern("tested on", re.compile(r"\btested\s+on\b", re.IGNORECASE), "evaluate_on"),
    CuePattern(
        "experiments on",
        re.compile(r"\bexperiments?\s+on\b", re.IGNORECASE),
        "evaluate_on",
    ),
    CuePattern(
        "using the dataset",
        re.compile(r"\busing\s+the\s+dataset\b", re.IGNORECASE),
        "evaluate_on",
    ),
    CuePattern("on the corpus", re.compile(r"\bon\s+the\s+corpus\b", re.IGNORECASE), "evaluate_on"),
    CuePattern(
        "benchmark dataset",
        re.compile(r"\bbenchmark\s+dataset\b", re.IGNORECASE),
        "evaluate_on",
    ),
    CuePattern("dataset", re.compile(r"\bdatasets?\b", re.IGNORECASE), "evaluate_on"),
    CuePattern("corpus", re.compile(r"\bcorpus|corpora\b", re.IGNORECASE), "evaluate_on"),
    CuePattern("treebank", re.compile(r"\btreebank\b", re.IGNORECASE), "evaluate_on"),
]

COMPARE_CUES = [
    CuePattern(
        "compare with", re.compile(r"\bcompare[sd]?\s+with\b", re.IGNORECASE), "compare_against"
    ),
    CuePattern(
        "compare against",
        re.compile(r"\bcompare[sd]?\s+against\b", re.IGNORECASE),
        "compare_against",
    ),
    CuePattern("compared to", re.compile(r"\bcompared\s+to\b", re.IGNORECASE), "compare_against"),
    CuePattern("baseline", re.compile(r"\bbaselines?\b", re.IGNORECASE), "compare_against"),
    CuePattern(
        "outperform", re.compile(r"\boutperform(?:s|ed|ing)?\b", re.IGNORECASE), "compare_against"
    ),
    CuePattern("better than", re.compile(r"\bbetter\s+than\b", re.IGNORECASE), "compare_against"),
    CuePattern("worse than", re.compile(r"\bworse\s+than\b", re.IGNORECASE), "compare_against"),
    CuePattern("versus", re.compile(r"\bversus\b", re.IGNORECASE), "compare_against"),
    CuePattern("vs.", re.compile(r"\bvs\.?\b", re.IGNORECASE), "compare_against"),
    CuePattern("benchmark", re.compile(r"\bbenchmarks?\b", re.IGNORECASE), "compare_against"),
    CuePattern(
        "state-of-the-art",
        re.compile(r"\bstate[- ]of[- ]the[- ]art\b", re.IGNORECASE),
        "compare_against",
    ),
    CuePattern("SOTA", re.compile(r"\bSOTA\b", re.IGNORECASE), "compare_against"),
    CuePattern(
        "achieves", re.compile(r"\bachiev(?:e|es|ed|ing)\b", re.IGNORECASE), "report_metric"
    ),
    CuePattern(
        "improves over",
        re.compile(r"\bimprov(?:e|es|ed|ing)\s+over\b", re.IGNORECASE),
        "compare_against",
    ),
]

EXTEND_CUES = [
    CuePattern("extend", re.compile(r"\bextend(?:s|ed|ing)?\b", re.IGNORECASE), "improve"),
    CuePattern("adapt", re.compile(r"\badapt(?:s|ed|ing)?\b", re.IGNORECASE), "adapt_to_domain"),
    CuePattern(
        "modify", re.compile(r"\bmodif(?:y|ies|ied|ying)\b", re.IGNORECASE), "adapt_to_domain"
    ),
    CuePattern("improve", re.compile(r"\bimprov(?:e|es|ed|ing)\b", re.IGNORECASE), "improve"),
    CuePattern(
        "generalize",
        re.compile(r"\bgenerali[sz](?:e|es|ed|ing)\b", re.IGNORECASE),
        "adapt_to_domain",
    ),
    CuePattern("build upon", re.compile(r"\bbuild(?:s|ing)?\s+upon\b", re.IGNORECASE), "improve"),
    CuePattern("builds on", re.compile(r"\bbuilds?\s+on\b", re.IGNORECASE), "improve"),
    CuePattern("derived from", re.compile(r"\bderived\s+from\b", re.IGNORECASE), "adapt_to_domain"),
    CuePattern("variant of", re.compile(r"\bvariant\s+of\b", re.IGNORECASE), "adapt_to_domain"),
    CuePattern("replace", re.compile(r"\breplac(?:e|es|ed|ing)\b", re.IGNORECASE), "replace"),
    CuePattern(
        "combine with",
        re.compile(r"\bcombin(?:e|es|ed|ing)\s+with\b", re.IGNORECASE),
        "combine_with",
    ),
]

STRONG_CRITIQUE_CUES = [
    CuePattern("limitation", re.compile(r"\blimitations?\b", re.IGNORECASE), "critique_limitation"),
    CuePattern("limited by", re.compile(r"\blimited\s+by\b", re.IGNORECASE), "critique_limitation"),
    CuePattern("fails to", re.compile(r"\bfails?\s+to\b", re.IGNORECASE), "critique_limitation"),
    CuePattern(
        "cannot", re.compile(r"\bcannot\b|\bcan\s+not\b", re.IGNORECASE), "critique_limitation"
    ),
    CuePattern("does not", re.compile(r"\bdoes\s+not\b", re.IGNORECASE), "critique_limitation"),
    CuePattern("problem", re.compile(r"\bproblems?\b", re.IGNORECASE), "critique_limitation"),
    CuePattern("drawback", re.compile(r"\bdrawbacks?\b", re.IGNORECASE), "critique_limitation"),
    CuePattern("bias", re.compile(r"\bbias(?:es|ed)?\b", re.IGNORECASE), "critique_limitation"),
    CuePattern("error", re.compile(r"\berrors?\b", re.IGNORECASE), "critique_limitation"),
    CuePattern(
        "weakness", re.compile(r"\bweakness(?:es)?\b", re.IGNORECASE), "critique_limitation"
    ),
    CuePattern("challenge", re.compile(r"\bchallenges?\b", re.IGNORECASE), "critique_limitation"),
    CuePattern("expensive", re.compile(r"\bexpensive\b", re.IGNORECASE), "critique_limitation"),
    CuePattern("inefficient", re.compile(r"\binefficient\b", re.IGNORECASE), "critique_limitation"),
]
WEAK_CRITIQUE_CUE = CuePattern(
    "however", re.compile(r"\bhowever\b", re.IGNORECASE), "critique_limitation"
)

APPLY_CUES = [
    CuePattern(
        "apply to", re.compile(r"\bappl(?:y|ies|ied)\s+to\b", re.IGNORECASE), "adapt_to_domain"
    ),
    CuePattern("applied to", re.compile(r"\bapplied\s+to\b", re.IGNORECASE), "adapt_to_domain"),
    CuePattern("application", re.compile(r"\bapplications?\b", re.IGNORECASE), "adapt_to_domain"),
    CuePattern(
        "for the task of", re.compile(r"\bfor\s+the\s+task\s+of\b", re.IGNORECASE), "direct_use"
    ),
    CuePattern("used for", re.compile(r"\bused\s+for\b", re.IGNORECASE), "direct_use"),
    CuePattern("to predict", re.compile(r"\bto\s+predict\b", re.IGNORECASE), "direct_use"),
    CuePattern("to classify", re.compile(r"\bto\s+classify\b", re.IGNORECASE), "direct_use"),
    CuePattern("to generate", re.compile(r"\bto\s+generate\b", re.IGNORECASE), "direct_use"),
    CuePattern("to translate", re.compile(r"\bto\s+translate\b", re.IGNORECASE), "direct_use"),
    CuePattern("to parse", re.compile(r"\bto\s+parse\b", re.IGNORECASE), "direct_use"),
    CuePattern("to tag", re.compile(r"\bto\s+tag\b", re.IGNORECASE), "direct_use"),
]

BACKGROUND_CUES = [
    CuePattern("previous work", re.compile(r"\bprevious\s+work\b", re.IGNORECASE), "none"),
    CuePattern("prior work", re.compile(r"\bprior\s+work\b", re.IGNORECASE), "none"),
    CuePattern("has been studied", re.compile(r"\bhas\s+been\s+studied\b", re.IGNORECASE), "none"),
    CuePattern(
        "have been studied", re.compile(r"\bhave\s+been\s+studied\b", re.IGNORECASE), "none"
    ),
    CuePattern(
        "has been proposed", re.compile(r"\bhas\s+been\s+proposed\b", re.IGNORECASE), "none"
    ),
    CuePattern("has been shown", re.compile(r"\bhas\s+been\s+shown\b", re.IGNORECASE), "none"),
    CuePattern("reported", re.compile(r"\breported\b", re.IGNORECASE), "none"),
    CuePattern("introduced", re.compile(r"\bintroduced\b", re.IGNORECASE), "none"),
    CuePattern("proposed", re.compile(r"\bproposed\b", re.IGNORECASE), "none"),
    CuePattern("described", re.compile(r"\bdescribed\b", re.IGNORECASE), "none"),
    CuePattern("related work", re.compile(r"\brelated\s+work\b", re.IGNORECASE), "none"),
    CuePattern("following work", re.compile(r"\bfollowing\s+work\b", re.IGNORECASE), "none"),
    CuePattern("line of work", re.compile(r"\bline\s+of\s+work\b", re.IGNORECASE), "none"),
]

INTENT_PRIORITY = [
    "critiques",
    "extends",
    "compares_against",
    "applies",
    "uses",
    "background",
    "unclear",
]


def screen_phase1_citation_functions(
    *,
    contexts_path: str | Path = DEFAULT_PHASE1_CONTEXTS_PATH,
    object_mentions_path: str | Path = DEFAULT_PHASE1_OBJECT_MENTIONS_PATH,
    object_graph_candidates_path: str | Path = DEFAULT_PHASE1_OBJECT_GRAPH_CANDIDATES_PATH,
    cited_title_profiles_path: str | Path = DEFAULT_PHASE1_CITED_TITLE_PROFILES_PATH,
    out_candidates_path: str | Path = DEFAULT_PHASE1_CANDIDATES_PILOT_PATH,
    out_features_path: str | Path = DEFAULT_PHASE1_FEATURES_PILOT_PATH,
    report_path: str | Path = DEFAULT_PHASE1_REPORT_PILOT_PATH,
    limit: int | None = DEFAULT_PHASE1_LIMIT,
    seed: int = 42,
) -> dict[str, Any]:
    """Run rule-based Phase-1 citation-function screening."""
    if limit is not None and limit < 1:
        raise ValueError("limit must be positive")

    contexts_input = Path(contexts_path)
    contexts = _read_contexts(contexts_input, limit=limit)
    contexts = _ensure_columns(contexts, CONTEXT_COLUMNS).drop_duplicates(
        subset=["context_id"],
        keep="first",
    )
    context_ids = set(contexts["context_id"].dropna().astype(str))

    object_mentions = _read_object_table(Path(object_mentions_path), context_ids)
    graph_candidates = _read_object_table(Path(object_graph_candidates_path), context_ids)
    cited_title_profiles = _read_object_table(Path(cited_title_profiles_path), context_ids)

    object_features = _build_object_feature_map(
        object_mentions=object_mentions,
        graph_candidates=graph_candidates,
        cited_title_profiles=cited_title_profiles,
    )
    screened_rows = [
        _screen_context(row, object_features.get(str(row["context_id"]), {}))
        for row in contexts.to_dict("records")
    ]
    candidates = pd.DataFrame(screened_rows)
    candidates = _ensure_columns(candidates, OUTPUT_COLUMNS)[OUTPUT_COLUMNS]
    features = _ensure_columns(candidates.copy(), FEATURE_COLUMNS)[FEATURE_COLUMNS]

    out_candidates = Path(out_candidates_path)
    out_candidates.parent.mkdir(parents=True, exist_ok=True)
    candidates.to_parquet(out_candidates, index=False)

    out_features = Path(out_features_path)
    out_features.parent.mkdir(parents=True, exist_ok=True)
    features.to_parquet(out_features, index=False)

    metrics = build_phase1_metrics(
        candidates=candidates,
        object_mentions=object_mentions,
        graph_candidates=graph_candidates,
        cited_title_profiles=cited_title_profiles,
        limit=limit,
        seed=seed,
    )
    report = build_phase1_report(
        metrics=metrics,
        candidates=candidates,
        contexts_path=contexts_input,
        object_mentions_path=Path(object_mentions_path),
        object_graph_candidates_path=Path(object_graph_candidates_path),
        cited_title_profiles_path=Path(cited_title_profiles_path),
        out_candidates_path=out_candidates,
        out_features_path=out_features,
    )
    report_output = Path(report_path)
    report_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.write_text(report, encoding="utf-8")
    return metrics


def build_phase1_metrics(
    *,
    candidates: pd.DataFrame,
    object_mentions: pd.DataFrame,
    graph_candidates: pd.DataFrame,
    cited_title_profiles: pd.DataFrame,
    limit: int | None,
    seed: int,
) -> dict[str, Any]:
    """Build summary metrics for the Phase-1 screening report."""
    input_count = int(len(candidates))
    send_count = int(candidates["should_send_to_llm"].sum()) if input_count else 0
    return {
        "input_contexts_processed": input_count,
        "configured_limit": "full" if limit is None else int(limit),
        "seed": int(seed),
        "contexts_with_object_mentions": int(candidates["has_object_mention"].sum()),
        "contexts_with_graph_candidate_objects": int(
            candidates["has_graph_candidate_object"].sum()
        ),
        "object_mentions_input_rows": int(len(object_mentions)),
        "graph_candidate_input_rows": int(len(graph_candidates)),
        "cited_title_profile_input_rows": int(len(cited_title_profiles)),
        "should_send_to_llm_count": send_count,
        "should_send_to_llm_rate": _safe_rate(send_count, input_count),
        "candidate_intent_distribution": _explode_value_counts(
            candidates,
            "candidate_intents",
            "candidate_intent",
            "contexts",
        ),
        "primary_candidate_intent_distribution": _value_counts(
            candidates,
            ["primary_candidate_intent"],
            "contexts",
        ),
        "candidate_object_type_distribution": _explode_value_counts(
            candidates,
            "candidate_object_types",
            "object_type",
            "contexts",
        ),
        "relation_subtype_distribution": _explode_value_counts(
            candidates,
            "candidate_relation_subtypes",
            "relation_subtype",
            "contexts",
        ),
        "cue_counts": _cue_counts(candidates),
        "candidate_intent_by_section": _group_counts(
            _explode_values(candidates, "candidate_intents", "candidate_intent"),
            ["normalized_section", "candidate_intent"],
            "contexts",
        ),
        "candidate_intent_by_object_type": _candidate_intent_by_object_type(candidates),
        "top_object_names_by_candidate_intent": _top_object_names_by_intent(candidates),
        "generic_metric_contexts_by_candidate_intent": _group_counts(
            _explode_values(
                candidates.loc[candidates["generic_metric_names"].ne("")],
                "candidate_intents",
                "candidate_intent",
            ),
            ["candidate_intent"],
            "contexts",
        ),
    }


def build_phase1_report(
    *,
    metrics: dict[str, Any],
    candidates: pd.DataFrame,
    contexts_path: Path,
    object_mentions_path: Path,
    object_graph_candidates_path: Path,
    cited_title_profiles_path: Path,
    out_candidates_path: Path,
    out_features_path: Path,
) -> str:
    """Build a markdown report for Phase-1 citation-function screening."""
    core = pd.DataFrame(
        [
            {"metric": "input_contexts_processed", "value": metrics["input_contexts_processed"]},
            {"metric": "configured_limit", "value": metrics["configured_limit"]},
            {
                "metric": "contexts_with_object_mentions",
                "value": metrics["contexts_with_object_mentions"],
            },
            {
                "metric": "contexts_with_graph_candidate_objects",
                "value": metrics["contexts_with_graph_candidate_objects"],
            },
            {
                "metric": "object_mentions_input_rows",
                "value": metrics["object_mentions_input_rows"],
            },
            {
                "metric": "graph_candidate_input_rows",
                "value": metrics["graph_candidate_input_rows"],
            },
            {
                "metric": "cited_title_profile_input_rows",
                "value": metrics["cited_title_profile_input_rows"],
            },
            {"metric": "should_send_to_llm_count", "value": metrics["should_send_to_llm_count"]},
            {
                "metric": "should_send_to_llm_rate",
                "value": f"{metrics['should_send_to_llm_rate']:.3f}",
            },
        ]
    )
    sections = [
        "# Phase-1 Citation-Function Screening Pilot Report",
        "",
        "## Inputs",
        f"- Contexts: `{contexts_path}`",
        f"- Object mentions: `{object_mentions_path}`",
        f"- Object graph candidates: `{object_graph_candidates_path}`",
        f"- Cited-title object profiles: `{cited_title_profiles_path}`",
        f"- Seed: `{metrics['seed']}`",
        "",
        "## Outputs",
        f"- Candidate rows: `{out_candidates_path}`",
        f"- Feature rows: `{out_features_path}`",
        "",
        "## Core Counts",
        _table(core),
        "",
        "## Candidate Intent Distribution",
        _table(metrics["candidate_intent_distribution"]),
        "",
        "## Primary Candidate Intent Distribution",
        _table(metrics["primary_candidate_intent_distribution"]),
        "",
        "## Candidate Object Type Distribution",
        _table(metrics["candidate_object_type_distribution"]),
        "",
        "## Relation Subtype Distribution",
        _table(metrics["relation_subtype_distribution"]),
        "",
        "## Matched Cue Counts By Group",
        _table(metrics["cue_counts"]),
        "",
        "## Candidate Intent By Normalized Section",
        _table(metrics["candidate_intent_by_section"]),
        "",
        "## Candidate Intent By Object Type",
        _table(metrics["candidate_intent_by_object_type"]),
        "",
        "## Top Object Names By Candidate Intent",
        _table(metrics["top_object_names_by_candidate_intent"]),
        "",
        "## Generic Metric Contexts By Candidate Intent",
        _table(metrics["generic_metric_contexts_by_candidate_intent"]),
        "",
        "## Example Uses",
        _table(_example_rows(candidates, "uses", 10)),
        "",
        "## Example Compares Against",
        _table(_example_rows(candidates, "compares_against", 10)),
        "",
        "## Example Extends",
        _table(_example_rows(candidates, "extends", 10)),
        "",
        "## Example Critiques",
        _table(_example_rows(candidates, "critiques", 10)),
        "",
        "## Example Applies",
        _table(_example_rows(candidates, "applies", 10)),
        "",
        "## Example Background",
        _table(_example_rows(candidates, "background", 10)),
        "",
        "## Multiple Candidate Intent Examples",
        _table(_multiple_intent_examples(candidates, 10)),
        "",
        "## Object Mention But Background Intent Examples",
        _table(_object_background_examples(candidates, 10)),
        "",
        "## No Cue But Object Mention Examples",
        _table(_no_cue_object_examples(candidates, 10)),
        "",
        "## LLM Flagged Examples",
        _table(_llm_flagged_examples(candidates, 10)),
        "",
    ]
    return "\n".join(sections)


def _screen_context(context: dict[str, Any], object_feature: dict[str, str]) -> dict[str, Any]:
    sentence = _clean_text(context.get("sentence_text"))
    window = _clean_text(context.get("context_window_s3"))
    normalized_section = _clean_text(context.get("normalized_section")).lower() or "unknown"
    cue_matches = {
        "use": _match_cues(USE_CUES, sentence, window),
        "compare": _match_cues(COMPARE_CUES, sentence, window),
        "extend": _match_cues(EXTEND_CUES, sentence, window),
        "critique": _match_critique_cues(sentence, window),
        "apply": _match_cues(APPLY_CUES, sentence, window),
        "background": _match_cues(BACKGROUND_CUES, sentence, window),
        "evaluation": _match_cues(EVALUATION_CUES, sentence, window),
    }
    cues_by_group = {
        group: [match["label"] for match in matches] for group, matches in cue_matches.items()
    }
    relation_subtypes = _relation_subtypes_from_cues(cue_matches)
    matched_rules = []
    intents = []

    if cue_matches["use"]:
        intents.append("uses")
        matched_rules.append("use_cue")
    if cue_matches["evaluation"]:
        intents.append("uses")
        matched_rules.append("evaluation_cue")
    if cue_matches["compare"]:
        intents.append("compares_against")
        matched_rules.append("compare_cue")
    if cue_matches["extend"]:
        intents.append("extends")
        matched_rules.append("extend_cue")
    if cue_matches["critique"]:
        intents.append("critiques")
        matched_rules.append("critique_cue")
    if cue_matches["apply"]:
        intents.append("applies")
        matched_rules.append("apply_cue")
    if cue_matches["background"]:
        intents.append("background")
        matched_rules.append("background_cue")

    has_object = _as_bool(object_feature.get("has_object_mention"))
    has_graph_candidate = _as_bool(object_feature.get("has_graph_candidate_object"))
    has_generic_metric = bool(object_feature.get("generic_metric_names"))
    has_compare_or_evaluation = bool(cue_matches["compare"] or cue_matches["evaluation"])
    if has_generic_metric and has_compare_or_evaluation:
        intents.append("compares_against")
        relation_subtypes.append("report_metric")
        matched_rules.append("generic_metric_with_compare_or_evaluation_cue")

    if not intents:
        section_prior = _section_prior_intent(normalized_section)
        if section_prior is not None:
            intents.append(section_prior)
            matched_rules.append(f"weak_section_prior:{normalized_section}")
        else:
            intents.append("unclear")
            matched_rules.append("no_cue")

    intents = _unique_preserve_order(intents)
    relation_subtypes = _unique_preserve_order(relation_subtypes) or ["none"]
    primary_intent = _primary_intent(intents)
    evidence_span = _choose_evidence_span(cue_matches)
    confidence = _confidence(
        primary_intent=primary_intent,
        cue_matches=cue_matches,
        has_object=has_object,
        has_graph_candidate=has_graph_candidate,
        section_prior_only=matched_rules == [f"weak_section_prior:{normalized_section}"],
    )
    should_send, send_reasons = _should_send_to_llm(
        intents=intents,
        primary_intent=primary_intent,
        confidence=confidence,
        normalized_section=normalized_section,
        has_object=has_object,
        has_graph_candidate=has_graph_candidate,
        has_generic_metric=has_generic_metric,
        has_compare_or_evaluation=has_compare_or_evaluation,
        matched_rules=matched_rules,
    )
    phase1_reason = _build_phase1_reason(
        primary_intent=primary_intent,
        confidence=confidence,
        send_reasons=send_reasons,
        has_object=has_object,
        has_graph_candidate=has_graph_candidate,
    )
    candidate_object_types = object_feature.get("object_types") or object_feature.get(
        "cited_title_profile_object_types",
        "unknown",
    )
    row = {column: context.get(column, "") for column in CONTEXT_COLUMNS}
    row.update(
        {
            "has_object_mention": has_object,
            "has_graph_candidate_object": has_graph_candidate,
            "object_ids": object_feature.get("object_ids", ""),
            "object_names": object_feature.get("object_names", ""),
            "object_types": object_feature.get("object_types", ""),
            "graph_candidate_object_ids": object_feature.get("graph_candidate_object_ids", ""),
            "graph_candidate_object_names": object_feature.get("graph_candidate_object_names", ""),
            "generic_metric_names": object_feature.get("generic_metric_names", ""),
            "cited_title_profile_object_names": object_feature.get(
                "cited_title_profile_object_names",
                "",
            ),
            "matched_use_cues": _join(cues_by_group["use"]),
            "matched_compare_cues": _join(cues_by_group["compare"]),
            "matched_extend_cues": _join(cues_by_group["extend"]),
            "matched_critique_cues": _join(cues_by_group["critique"]),
            "matched_apply_cues": _join(cues_by_group["apply"]),
            "matched_background_cues": _join(cues_by_group["background"]),
            "matched_evaluation_cues": _join(cues_by_group["evaluation"]),
            "evidence_span": evidence_span,
            "candidate_intents": _join(intents),
            "primary_candidate_intent": primary_intent,
            "candidate_object_types": candidate_object_types,
            "primary_candidate_object_type": _first_split(candidate_object_types, "unknown"),
            "candidate_relation_subtypes": _join(relation_subtypes),
            "confidence": round(confidence, 3),
            "should_send_to_llm": should_send,
            "phase1_reason": phase1_reason,
            "matched_rules": _join(_unique_preserve_order(matched_rules)),
        }
    )
    return row


def _read_contexts(path: Path, *, limit: int | None) -> pd.DataFrame:
    parquet_file = pq.ParquetFile(path)
    available_columns = set(parquet_file.schema_arrow.names)
    columns = [column for column in CONTEXT_COLUMNS if column in available_columns]
    batches = []
    remaining = limit
    batch_size = 50_000 if limit is None else min(50_000, limit)
    for batch in parquet_file.iter_batches(batch_size=batch_size, columns=columns):
        take = batch.num_rows if remaining is None else min(remaining, batch.num_rows)
        batches.append(batch.slice(0, take).to_pandas())
        if remaining is None:
            continue
        remaining -= take
        if remaining <= 0:
            break
    if not batches:
        return pd.DataFrame(columns=CONTEXT_COLUMNS)
    return pd.concat(batches, ignore_index=True)


def _read_object_table(path: Path, context_ids: set[str]) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    parquet_file = pq.ParquetFile(path)
    available_columns = set(parquet_file.schema_arrow.names)
    columns = [column for column in OBJECT_COLUMNS if column in available_columns]
    if "context_id" not in columns:
        return pd.DataFrame(columns=OBJECT_COLUMNS)
    batches = []
    for batch in parquet_file.iter_batches(batch_size=100_000, columns=columns):
        frame = batch.to_pandas()
        frame["context_id"] = frame["context_id"].astype(str)
        frame = frame.loc[frame["context_id"].isin(context_ids)]
        if not frame.empty:
            batches.append(frame)
    if not batches:
        return pd.DataFrame(columns=OBJECT_COLUMNS)
    return _ensure_columns(pd.concat(batches, ignore_index=True), OBJECT_COLUMNS)


def _build_object_feature_map(
    *,
    object_mentions: pd.DataFrame,
    graph_candidates: pd.DataFrame,
    cited_title_profiles: pd.DataFrame,
) -> dict[str, dict[str, str]]:
    features: dict[str, dict[str, str]] = {}
    direct = object_mentions.loc[object_mentions["phase1_feature_eligible"].map(_as_bool)].copy()
    direct_groups = direct.groupby("context_id", dropna=True) if not direct.empty else []
    for context_id, group in direct_groups:
        features[str(context_id)] = {
            "has_object_mention": "true",
            "object_ids": _join_unique(group["object_id"]),
            "object_names": _join_unique(group["canonical_name"]),
            "object_types": _join_unique(group["object_type"]),
            "generic_metric_names": _join_unique(
                group.loc[group["object_category"].eq("generic_metric"), "canonical_name"]
            ),
        }
    graph_groups = (
        graph_candidates.groupby("context_id", dropna=True) if not graph_candidates.empty else []
    )
    for context_id, group in graph_groups:
        item = features.setdefault(str(context_id), {})
        item["has_graph_candidate_object"] = "true"
        item["graph_candidate_object_ids"] = _join_unique(group["object_id"])
        item["graph_candidate_object_names"] = _join_unique(group["canonical_name"])
    profile_groups = (
        cited_title_profiles.groupby("context_id", dropna=True)
        if not cited_title_profiles.empty
        else []
    )
    for context_id, group in profile_groups:
        item = features.setdefault(str(context_id), {})
        item["cited_title_profile_object_names"] = _join_unique(group["canonical_name"])
        item["cited_title_profile_object_types"] = _join_unique(group["object_type"])
    for item in features.values():
        item.setdefault("has_object_mention", "false")
        item.setdefault("has_graph_candidate_object", "false")
        item.setdefault("object_ids", "")
        item.setdefault("object_names", "")
        item.setdefault("object_types", "")
        item.setdefault("graph_candidate_object_ids", "")
        item.setdefault("graph_candidate_object_names", "")
        item.setdefault("generic_metric_names", "")
        item.setdefault("cited_title_profile_object_names", "")
        item.setdefault("cited_title_profile_object_types", "")
    return features


def _match_cues(
    cue_patterns: list[CuePattern],
    sentence: str,
    context_window: str,
) -> list[dict[str, str | int]]:
    matches = []
    for cue in cue_patterns:
        match = cue.pattern.search(sentence)
        matched_in = "sentence_text"
        if match is None and context_window:
            match = cue.pattern.search(context_window)
            matched_in = "context_window_s3"
        if match is not None:
            matches.append(
                {
                    "label": cue.label,
                    "span": match.group(0).strip(),
                    "start": match.start(),
                    "matched_in": matched_in,
                    "relation_subtype": cue.relation_subtype or "none",
                }
            )
    return matches


def _match_critique_cues(sentence: str, context_window: str) -> list[dict[str, str | int]]:
    strong = _match_cues(STRONG_CRITIQUE_CUES, sentence, context_window)
    weak = _match_cues([WEAK_CRITIQUE_CUE], sentence, context_window)
    if strong:
        return strong + weak
    return []


def _relation_subtypes_from_cues(cue_matches: dict[str, list[dict[str, str | int]]]) -> list[str]:
    relation_subtypes = []
    for matches in cue_matches.values():
        for match in matches:
            subtype = str(match.get("relation_subtype") or "")
            if subtype and subtype != "none":
                relation_subtypes.append(subtype)
    return relation_subtypes


def _choose_evidence_span(cue_matches: dict[str, list[dict[str, str | int]]]) -> str:
    all_matches = [
        match
        for group in ("use", "compare", "extend", "critique", "apply", "evaluation", "background")
        for match in cue_matches[group]
    ]
    if not all_matches:
        return ""
    sentence_matches = [match for match in all_matches if match["matched_in"] == "sentence_text"]
    selected = sorted(sentence_matches or all_matches, key=lambda item: int(item["start"]))[0]
    return str(selected["span"])


def _section_prior_intent(normalized_section: str) -> str | None:
    if normalized_section in BACKGROUND_SECTIONS:
        return "background"
    if normalized_section in CRITIQUE_SECTIONS:
        return "critiques"
    if normalized_section in CONCLUSION_SECTIONS:
        return "background"
    return None


def _primary_intent(intents: list[str]) -> str:
    for intent in INTENT_PRIORITY:
        if intent in intents:
            return intent
    return "unclear"


def _confidence(
    *,
    primary_intent: str,
    cue_matches: dict[str, list[dict[str, str | int]]],
    has_object: bool,
    has_graph_candidate: bool,
    section_prior_only: bool,
) -> float:
    has_any_cue = any(cue_matches[group] for group in cue_matches)
    if primary_intent == "unclear":
        return 0.45 if has_object else 0.2
    if section_prior_only:
        return 0.35 if primary_intent == "background" else 0.4
    if primary_intent == "background":
        return 0.55 if has_any_cue else 0.35
    if has_any_cue and has_graph_candidate:
        return 0.9
    if has_any_cue and has_object:
        return 0.85
    if has_any_cue:
        return 0.65
    if has_object:
        return 0.45
    return 0.25


def _should_send_to_llm(
    *,
    intents: list[str],
    primary_intent: str,
    confidence: float,
    normalized_section: str,
    has_object: bool,
    has_graph_candidate: bool,
    has_generic_metric: bool,
    has_compare_or_evaluation: bool,
    matched_rules: list[str],
) -> tuple[bool, list[str]]:
    if "no_cue" in matched_rules and not has_object:
        return False, ["no_cues_no_object"]
    reasons = []
    if any(
        intent in {"uses", "compares_against", "extends", "critiques", "applies"}
        for intent in intents
    ):
        reasons.append("non_background_candidate_intent")
    if has_graph_candidate:
        reasons.append("has_graph_candidate_object")
    if has_generic_metric and has_compare_or_evaluation:
        reasons.append("generic_metric_compare_or_evaluation")
    non_unclear_intents = [intent for intent in intents if intent != "unclear"]
    if len(non_unclear_intents) > 1:
        reasons.append("multiple_candidate_intents")
    if 0.4 <= confidence <= 0.8:
        reasons.append("medium_confidence")
    if normalized_section in HIGH_VALUE_SECTIONS and (has_object or primary_intent != "unclear"):
        reasons.append(f"high_value_section:{normalized_section}")
    if primary_intent == "background" and not has_object:
        return False, reasons or ["clear_background_no_object"]
    return bool(reasons), reasons


def _build_phase1_reason(
    *,
    primary_intent: str,
    confidence: float,
    send_reasons: list[str],
    has_object: bool,
    has_graph_candidate: bool,
) -> str:
    parts = [
        f"primary={primary_intent}",
        f"confidence={confidence:.2f}",
        f"object={str(has_object).lower()}",
        f"graph_object={str(has_graph_candidate).lower()}",
    ]
    if send_reasons:
        parts.append(f"llm_reasons={';'.join(send_reasons)}")
    return "|".join(parts)


def _cue_counts(candidates: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for group, column in [
        ("use", "matched_use_cues"),
        ("compare", "matched_compare_cues"),
        ("extend", "matched_extend_cues"),
        ("critique", "matched_critique_cues"),
        ("apply", "matched_apply_cues"),
        ("background", "matched_background_cues"),
        ("evaluation", "matched_evaluation_cues"),
    ]:
        rows.append(
            {
                "cue_group": group,
                "contexts": int(candidates[column].fillna("").astype(str).ne("").sum()),
            }
        )
    return pd.DataFrame(rows)


def _candidate_intent_by_object_type(candidates: pd.DataFrame) -> pd.DataFrame:
    exploded = _explode_values(candidates, "candidate_intents", "candidate_intent")
    exploded = _explode_values(exploded, "candidate_object_types", "object_type")
    return _group_counts(exploded, ["candidate_intent", "object_type"], "contexts")


def _top_object_names_by_intent(candidates: pd.DataFrame) -> pd.DataFrame:
    exploded = _explode_values(candidates, "candidate_intents", "candidate_intent")
    exploded = _explode_values(exploded, "object_names", "object_name")
    exploded = exploded.loc[exploded["object_name"].ne("")]
    return _group_counts(exploded, ["candidate_intent", "object_name"], "contexts", limit=100)


def _example_rows(candidates: pd.DataFrame, intent: str, limit: int) -> pd.DataFrame:
    mask = (
        candidates["candidate_intents"]
        .fillna("")
        .astype(str)
        .str.split(";")
        .map(lambda values: intent in values)
    )
    return _format_examples(candidates.loc[mask], limit)


def _multiple_intent_examples(candidates: pd.DataFrame, limit: int) -> pd.DataFrame:
    mask = candidates["candidate_intents"].fillna("").astype(str).str.contains(";")
    return _format_examples(candidates.loc[mask], limit)


def _object_background_examples(candidates: pd.DataFrame, limit: int) -> pd.DataFrame:
    mask = candidates["has_object_mention"] & candidates["primary_candidate_intent"].eq(
        "background"
    )
    return _format_examples(candidates.loc[mask], limit)


def _no_cue_object_examples(candidates: pd.DataFrame, limit: int) -> pd.DataFrame:
    cue_columns = [
        "matched_use_cues",
        "matched_compare_cues",
        "matched_extend_cues",
        "matched_critique_cues",
        "matched_apply_cues",
        "matched_background_cues",
        "matched_evaluation_cues",
    ]
    no_cues = candidates[cue_columns].fillna("").astype(str).eq("").all(axis=1)
    mask = candidates["has_object_mention"] & no_cues
    return _format_examples(candidates.loc[mask], limit)


def _llm_flagged_examples(candidates: pd.DataFrame, limit: int) -> pd.DataFrame:
    return _format_examples(candidates.loc[candidates["should_send_to_llm"]], limit)


def _format_examples(frame: pd.DataFrame, limit: int) -> pd.DataFrame:
    columns = [
        "context_id",
        "normalized_section",
        "primary_candidate_intent",
        "candidate_intents",
        "candidate_relation_subtypes",
        "confidence",
        "should_send_to_llm",
        "object_names",
        "generic_metric_names",
        "evidence_span",
        "matched_rules",
        "sentence_text",
    ]
    sample = _ensure_columns(frame.head(limit).copy(), columns)
    for column in ("sentence_text", "object_names", "generic_metric_names", "matched_rules"):
        sample[column] = sample[column].map(lambda value: _truncate(value, 180))
    return sample[columns]


def _explode_value_counts(
    frame: pd.DataFrame,
    source_column: str,
    output_column: str,
    count_name: str,
) -> pd.DataFrame:
    return _group_counts(
        _explode_values(frame, source_column, output_column),
        [output_column],
        count_name,
    )


def _explode_values(frame: pd.DataFrame, source_column: str, output_column: str) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(columns=[*frame.columns, output_column])
    exploded = frame.copy()
    exploded[output_column] = exploded[source_column].fillna("").astype(str).str.split(";")
    exploded = exploded.explode(output_column)
    exploded[output_column] = exploded[output_column].fillna("").astype(str).str.strip()
    return exploded.loc[exploded[output_column].ne("")]


def _value_counts(
    frame: pd.DataFrame,
    columns: list[str],
    count_name: str,
    *,
    limit: int | None = None,
) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(columns=[*columns, count_name])
    counts = (
        frame.groupby(columns, dropna=False)
        .size()
        .reset_index(name=count_name)
        .sort_values(count_name, ascending=False)
        .reset_index(drop=True)
    )
    if limit is not None:
        counts = counts.head(limit)
    return counts


def _group_counts(
    frame: pd.DataFrame,
    columns: list[str],
    count_name: str,
    *,
    limit: int | None = None,
) -> pd.DataFrame:
    return _value_counts(frame, columns, count_name, limit=limit)


def _ensure_columns(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    output = frame.copy()
    for column in columns:
        if column not in output.columns:
            output[column] = ""
    return output


def _safe_rate(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def _join(values: list[Any]) -> str:
    return ";".join(str(value) for value in values if str(value) != "")


def _join_unique(values: pd.Series) -> str:
    return _join(_unique_preserve_order([_clean_text(value) for value in values]))


def _unique_preserve_order(values: list[Any]) -> list[str]:
    seen = set()
    output = []
    for value in values:
        text = _clean_text(value)
        if not text or text in seen:
            continue
        seen.add(text)
        output.append(text)
    return output


def _first_split(value: str, default: str) -> str:
    text = _clean_text(value)
    if not text:
        return default
    return text.split(";")[0] or default


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None or pd.isna(value):
        return False
    return str(value).strip().lower() in {"true", "1", "yes"}


def _clean_text(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


def _truncate(value: Any, max_chars: int) -> str:
    text = _clean_text(value)
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
