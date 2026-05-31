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
DEFAULT_PHASE1_CANDIDATES_PILOT_REFINED_PATH = Path(
    "data/processed/phase1_citation_function_candidates_pilot_refined.parquet"
)
DEFAULT_PHASE1_CANDIDATES_PILOT_REFINED_V2_PATH = Path(
    "data/processed/phase1_citation_function_candidates_pilot_refined_v2.parquet"
)
DEFAULT_PHASE1_FEATURES_PILOT_PATH = Path("data/processed/phase1_context_features_pilot.parquet")
DEFAULT_PHASE1_FEATURES_PILOT_REFINED_PATH = Path(
    "data/processed/phase1_context_features_pilot_refined.parquet"
)
DEFAULT_PHASE1_FEATURES_PILOT_REFINED_V2_PATH = Path(
    "data/processed/phase1_context_features_pilot_refined_v2.parquet"
)
DEFAULT_PHASE1_REPORT_PILOT_PATH = Path(
    "reports/phase1_citation_function_screening_pilot_report.md"
)
DEFAULT_PHASE1_REPORT_PILOT_REFINED_PATH = Path(
    "reports/phase1_citation_function_screening_pilot_refined_report.md"
)
DEFAULT_PHASE1_REPORT_PILOT_REFINED_V2_PATH = Path(
    "reports/phase1_citation_function_screening_pilot_refined_v2_report.md"
)
DEFAULT_PHASE1_LLM_REVIEW_RESULTS_PATH = Path(
    "data/processed/phase1_llm_review_results.parquet"
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
    "cited_work_description",
    "evidence_span",
    "candidate_intents",
    "primary_candidate_intent",
    "candidate_object_types",
    "primary_candidate_object_type",
    "object_type_source",
    "object_type_confidence",
    "candidate_relation_subtypes",
    "confidence",
    "llm_priority",
    "llm_reason",
    "should_send_to_llm",
    "phase2_candidate_type",
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
    "cited_work_description",
    "evidence_span",
    "object_type_source",
    "object_type_confidence",
    "llm_priority",
    "llm_reason",
    "phase2_candidate_type",
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
OBJECT_CONTEXT_SECTIONS = {
    "method",
    "model",
    "implementation",
    "system_description",
    "dataset",
    "experiment",
    "evaluation",
    "results",
}


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

CITED_WORK_DESCRIPTION_CUES = [
    CuePattern("described", re.compile(r"\bdescribed\b", re.IGNORECASE), "none"),
    CuePattern("proposed", re.compile(r"\bproposed\b", re.IGNORECASE), "none"),
    CuePattern("introduced", re.compile(r"\bintroduced\b", re.IGNORECASE), "none"),
    CuePattern("annotated", re.compile(r"\bannotated\b", re.IGNORECASE), "none"),
    CuePattern("used", re.compile(r"\bused\b", re.IGNORECASE), "none"),
    CuePattern("reported", re.compile(r"\breported\b", re.IGNORECASE), "none"),
    CuePattern("showed", re.compile(r"\bshow(?:ed|n)\b", re.IGNORECASE), "none"),
    CuePattern("presented", re.compile(r"\bpresented\b", re.IGNORECASE), "none"),
    CuePattern("developed", re.compile(r"\bdeveloped\b", re.IGNORECASE), "none"),
]

CURRENT_WORK_USE_CUES = [
    CuePattern("we use", re.compile(r"\bwe\s+use\b", re.IGNORECASE), "direct_use"),
    CuePattern("we used", re.compile(r"\bwe\s+used\b", re.IGNORECASE), "direct_use"),
    CuePattern("we employ", re.compile(r"\bwe\s+employ(?:ed)?\b", re.IGNORECASE), "direct_use"),
    CuePattern("we adopt", re.compile(r"\bwe\s+adopt(?:ed)?\b", re.IGNORECASE), "direct_use"),
    CuePattern("we follow", re.compile(r"\bwe\s+follow(?:ed)?\b", re.IGNORECASE), "direct_use"),
    CuePattern("we build on", re.compile(r"\bwe\s+build\s+on\b", re.IGNORECASE), "direct_use"),
    CuePattern("we build upon", re.compile(r"\bwe\s+build\s+upon\b", re.IGNORECASE), "direct_use"),
    CuePattern(
        "we initialize", re.compile(r"\bwe\s+initiali[sz]e(?:d)?\b", re.IGNORECASE), "component_use"
    ),
    CuePattern(
        "we train with", re.compile(r"\bwe\s+train(?:ed)?\s+with\b", re.IGNORECASE), "direct_use"
    ),
    CuePattern(
        "we evaluate on", re.compile(r"\bwe\s+evaluate(?:d)?\s+on\b", re.IGNORECASE), "evaluate_on"
    ),
    CuePattern("we apply", re.compile(r"\bwe\s+appl(?:y|ied)\b", re.IGNORECASE), "direct_use"),
    CuePattern(
        "our method uses",
        re.compile(r"\bour\s+(?:method|approach|model|system|framework)\s+uses?\b", re.IGNORECASE),
        "direct_use",
    ),
    CuePattern(
        "this work uses",
        re.compile(r"\bthis\s+(?:paper|work|study|system|model)\s+uses?\b", re.IGNORECASE),
        "direct_use",
    ),
]

WEAK_USE_CUES = [
    CuePattern("using", re.compile(r"\busing\b", re.IGNORECASE), "direct_use"),
    CuePattern("based on", re.compile(r"\bbased\s+on\b", re.IGNORECASE), "direct_use"),
    CuePattern("following", re.compile(r"\bfollowing\b", re.IGNORECASE), "direct_use"),
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

REFINED_EVALUATION_CUES = [
    CuePattern("evaluated on", re.compile(r"\bevaluated\s+on\b", re.IGNORECASE), "evaluate_on"),
    CuePattern("trained on", re.compile(r"\btrained\s+on\b", re.IGNORECASE), "evaluate_on"),
    CuePattern("tested on", re.compile(r"\btested\s+on\b", re.IGNORECASE), "evaluate_on"),
    CuePattern(
        "experiments on",
        re.compile(r"\bexperiments?\s+on\b", re.IGNORECASE),
        "evaluate_on",
    ),
    CuePattern(
        "use the dataset",
        re.compile(r"\buse(?:d|s|ing)?\s+the\s+datasets?\b", re.IGNORECASE),
        "evaluate_on",
    ),
    CuePattern(
        "using the corpus",
        re.compile(r"\busing\s+the\s+corpus\b", re.IGNORECASE),
        "evaluate_on",
    ),
    CuePattern(
        "on the dataset", re.compile(r"\bon\s+the\s+datasets?\b", re.IGNORECASE), "evaluate_on"
    ),
    CuePattern("on the corpus", re.compile(r"\bon\s+the\s+corpus\b", re.IGNORECASE), "evaluate_on"),
    CuePattern("benchmarked on", re.compile(r"\bbenchmarked\s+on\b", re.IGNORECASE), "evaluate_on"),
]

DATASET_FEATURE_CUES = [
    CuePattern("dataset", re.compile(r"\bdatasets?\b", re.IGNORECASE), "none"),
    CuePattern("corpus", re.compile(r"\bcorpus|corpora\b", re.IGNORECASE), "none"),
    CuePattern("treebank", re.compile(r"\btreebank\b", re.IGNORECASE), "none"),
    CuePattern("benchmark", re.compile(r"\bbenchmarks?\b", re.IGNORECASE), "none"),
]

REFINED_COMPARE_CUES = [
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
    CuePattern(
        "benchmark against",
        re.compile(r"\bbenchmarks?(?:ed|ing)?\s+against\b", re.IGNORECASE),
        "compare_against",
    ),
    CuePattern(
        "achieves compared",
        re.compile(r"\bachiev(?:e|es|ed|ing)\b.{0,80}\bcompared\b", re.IGNORECASE),
        "report_metric",
    ),
    CuePattern(
        "state-of-the-art baseline",
        re.compile(r"\bstate[- ]of[- ]the[- ]art\s+baselines?\b", re.IGNORECASE),
        "compare_against",
    ),
    CuePattern(
        "improves over",
        re.compile(r"\bimprov(?:e|es|ed|ing)\s+over\b", re.IGNORECASE),
        "compare_against",
    ),
]

REFINED_CRITIQUE_CUES = [
    CuePattern("fails to", re.compile(r"\bfails?\s+to\b", re.IGNORECASE), "critique_limitation"),
    CuePattern(
        "cannot", re.compile(r"\bcannot\b|\bcan\s+not\b", re.IGNORECASE), "critique_limitation"
    ),
    CuePattern("does not", re.compile(r"\bdoes\s+not\b", re.IGNORECASE), "critique_limitation"),
    CuePattern(
        "is limited by", re.compile(r"\bis\s+limited\s+by\b", re.IGNORECASE), "critique_limitation"
    ),
    CuePattern(
        "limitation of", re.compile(r"\blimitations?\s+of\b", re.IGNORECASE), "critique_limitation"
    ),
    CuePattern(
        "drawback of", re.compile(r"\bdrawbacks?\s+of\b", re.IGNORECASE), "critique_limitation"
    ),
    CuePattern(
        "suffers from", re.compile(r"\bsuffers?\s+from\b", re.IGNORECASE), "critique_limitation"
    ),
    CuePattern(
        "however negative",
        re.compile(
            r"\bhowever\b.{0,80}\b(?:fails?|cannot|can\s+not|does\s+not|limited)\b",
            re.IGNORECASE,
        ),
        "critique_limitation",
    ),
    CuePattern("unlike", re.compile(r"\bunlike\b", re.IGNORECASE), "critique_limitation"),
    CuePattern("unable to", re.compile(r"\bunable\s+to\b", re.IGNORECASE), "critique_limitation"),
    CuePattern(
        "performs poorly",
        re.compile(r"\bperforms?\s+poorly\b", re.IGNORECASE),
        "critique_limitation",
    ),
]

V2_CURRENT_WORK_USE_CUES = [
    *CURRENT_WORK_USE_CUES,
    CuePattern(
        "in this work we use",
        re.compile(r"\bin\s+this\s+work,\s+we\s+use\b", re.IGNORECASE),
        "direct_use",
    ),
    CuePattern(
        "our system uses",
        re.compile(
            r"\bour\s+(?:method|approach|model|system|framework|parser|algorithm)\s+"
            r"(?:use|uses|used|employs?|adopts?|follows?)\b",
            re.IGNORECASE,
        ),
        "direct_use",
    ),
]

V2_CURRENT_APPLY_CUES = [
    CuePattern(
        "we apply to",
        re.compile(r"\bwe\s+appl(?:y|ied)\b.{0,80}\bto\b", re.IGNORECASE),
        "adapt_to_domain",
    ),
    CuePattern(
        "we adapt to",
        re.compile(r"\bwe\s+adapt(?:ed)?\b.{0,80}\bto\b", re.IGNORECASE),
        "adapt_to_domain",
    ),
    CuePattern(
        "we use for task",
        re.compile(
            r"\bwe\s+use(?:d)?\b.{0,100}\bfor\s+the\s+task\s+of\b",
            re.IGNORECASE,
        ),
        "direct_use",
    ),
    CuePattern(
        "we use to",
        re.compile(
            r"\bwe\s+use(?:d)?\b.{0,100}\bto\s+"
            r"(?:predict|classify|generate|translate|parse|tag)\b",
            re.IGNORECASE,
        ),
        "direct_use",
    ),
    CuePattern(
        "our method applies to",
        re.compile(
            r"\bour\s+(?:method|approach|model|system|framework)\s+applies\b.{0,80}\bto\b",
            re.IGNORECASE,
        ),
        "adapt_to_domain",
    ),
    CuePattern(
        "this work applies to",
        re.compile(
            r"\bthis\s+(?:paper|work|study|system|model)\s+applies\b.{0,80}\bto\b",
            re.IGNORECASE,
        ),
        "adapt_to_domain",
    ),
]

V2_WEAK_APPLY_CUES = [
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

V2_CURRENT_EXTEND_CUES = [
    CuePattern(
        "we extend", re.compile(r"\bwe\s+extend(?:ed|s|ing)?\b", re.IGNORECASE), "improve"
    ),
    CuePattern(
        "we improve", re.compile(r"\bwe\s+improv(?:e|ed|es|ing)\b", re.IGNORECASE), "improve"
    ),
    CuePattern(
        "we adapt",
        re.compile(r"\bwe\s+adapt(?:ed|s|ing)?\b", re.IGNORECASE),
        "adapt_to_domain",
    ),
    CuePattern(
        "we modify",
        re.compile(r"\bwe\s+modif(?:y|ied|ies|ying)\b", re.IGNORECASE),
        "adapt_to_domain",
    ),
    CuePattern(
        "we generalize",
        re.compile(r"\bwe\s+generali[sz](?:e|ed|es|ing)\b", re.IGNORECASE),
        "adapt_to_domain",
    ),
    CuePattern("we build upon", re.compile(r"\bwe\s+build\s+upon\b", re.IGNORECASE), "improve"),
    CuePattern(
        "our extension of",
        re.compile(r"\bour\s+extension\s+of\b", re.IGNORECASE),
        "improve",
    ),
    CuePattern(
        "our adaptation of",
        re.compile(r"\bour\s+adaptation\s+of\b", re.IGNORECASE),
        "adapt_to_domain",
    ),
]

V2_WEAK_EXTEND_CUES = [
    CuePattern("improve", re.compile(r"\bimprov(?:e|es|ed|ing)\b", re.IGNORECASE), "improve"),
    CuePattern("derived from", re.compile(r"\bderived\s+from\b", re.IGNORECASE), "adapt_to_domain"),
    CuePattern("based on", re.compile(r"\bbased\s+on\b", re.IGNORECASE), "adapt_to_domain"),
    CuePattern("variant of", re.compile(r"\bvariant\s+of\b", re.IGNORECASE), "adapt_to_domain"),
    CuePattern(
        "generalization of",
        re.compile(r"\bgeneralization\s+of\b", re.IGNORECASE),
        "adapt_to_domain",
    ),
    CuePattern("extension of", re.compile(r"\bextension\s+of\b", re.IGNORECASE), "improve"),
]

V2_COMPARE_CUES = [
    CuePattern(
        "we compare with",
        re.compile(r"\bwe\s+compare[sd]?\s+with\b", re.IGNORECASE),
        "compare_against",
    ),
    CuePattern(
        "we compare against",
        re.compile(r"\bwe\s+compare[sd]?\s+against\b", re.IGNORECASE),
        "compare_against",
    ),
    CuePattern(
        "compared to", re.compile(r"\bcompared\s+to\b", re.IGNORECASE), "compare_against"
    ),
    CuePattern(
        "compared with",
        re.compile(r"\bcompared\s+with\b", re.IGNORECASE),
        "compare_against",
    ),
    CuePattern(
        "as baseline",
        re.compile(r"\bas\s+(?:a\s+)?baselines?\b", re.IGNORECASE),
        "compare_against",
    ),
    CuePattern(
        "baseline system",
        re.compile(r"\bbaseline\s+(?:systems?|models?|methods?|approaches?)\b", re.IGNORECASE),
        "compare_against",
    ),
    CuePattern(
        "outperform", re.compile(r"\boutperform(?:s|ed|ing)?\b", re.IGNORECASE), "compare_against"
    ),
    CuePattern(
        "better than", re.compile(r"\bbetter\b.{0,40}\bthan\b", re.IGNORECASE), "compare_against"
    ),
    CuePattern(
        "worse than", re.compile(r"\bworse\b.{0,40}\bthan\b", re.IGNORECASE), "compare_against"
    ),
    CuePattern("versus", re.compile(r"\bversus\b", re.IGNORECASE), "compare_against"),
    CuePattern("vs.", re.compile(r"\bvs\.?\b", re.IGNORECASE), "compare_against"),
    CuePattern(
        "benchmark against",
        re.compile(r"\bbenchmarks?(?:ed|ing)?\s+against\b", re.IGNORECASE),
        "compare_against",
    ),
]

V2_CRITIQUE_CUES = [
    CuePattern(
        "target fails to",
        re.compile(
            r"\b(?:[A-Z][A-Za-z0-9._+-]{1,}|the\s+(?:method|model|approach|system|parser|algorithm)|"
            r"their\s+(?:method|model|approach|system|parser|algorithm))\s+fails?\s+to\b",
            re.IGNORECASE,
        ),
        "critique_limitation",
    ),
    CuePattern(
        "target cannot",
        re.compile(
            r"\b(?:[A-Z][A-Za-z0-9._+-]{1,}|the\s+(?:method|model|approach|system|parser|algorithm)|"
            r"their\s+(?:method|model|approach|system|parser|algorithm))\s+(?:cannot|can\s+not)\b",
            re.IGNORECASE,
        ),
        "critique_limitation",
    ),
    CuePattern(
        "target does not handle",
        re.compile(
            r"\b(?:[A-Z][A-Za-z0-9._+-]{1,}|the\s+(?:method|model|approach|system|parser|algorithm)|"
            r"their\s+(?:method|model|approach|system|parser|algorithm))\s+does\s+not\s+handle\b",
            re.IGNORECASE,
        ),
        "critique_limitation",
    ),
    CuePattern(
        "target is limited by",
        re.compile(
            r"\b(?:[A-Z][A-Za-z0-9._+-]{1,}|the\s+(?:method|model|approach|system|parser|algorithm)|"
            r"their\s+(?:method|model|approach|system|parser|algorithm))\s+is\s+limited\s+by\b",
            re.IGNORECASE,
        ),
        "critique_limitation",
    ),
    CuePattern(
        "limitation of target",
        re.compile(
            r"\blimitations?\s+of\s+(?:[A-Z][A-Za-z0-9._+-]{1,}|the\s+"
            r"(?:method|model|approach|system|parser|algorithm))\b",
            re.IGNORECASE,
        ),
        "critique_limitation",
    ),
    CuePattern(
        "drawback of target",
        re.compile(
            r"\bdrawbacks?\s+of\s+(?:[A-Z][A-Za-z0-9._+-]{1,}|the\s+"
            r"(?:method|model|approach|system|parser|algorithm))\b",
            re.IGNORECASE,
        ),
        "critique_limitation",
    ),
    CuePattern(
        "target suffers from",
        re.compile(
            r"\b(?:[A-Z][A-Za-z0-9._+-]{1,}|the\s+(?:method|model|approach|system|parser|algorithm)|"
            r"their\s+(?:method|model|approach|system|parser|algorithm))\s+suffers?\s+from\b",
            re.IGNORECASE,
        ),
        "critique_limitation",
    ),
    CuePattern(
        "target performs poorly",
        re.compile(
            r"\b(?:[A-Z][A-Za-z0-9._+-]{1,}|the\s+(?:method|model|approach|system|parser|algorithm)|"
            r"their\s+(?:method|model|approach|system|parser|algorithm))\s+performs?\s+poorly\b",
            re.IGNORECASE,
        ),
        "critique_limitation",
    ),
    CuePattern(
        "target unable to",
        re.compile(
            r"\b(?:[A-Z][A-Za-z0-9._+-]{1,}|the\s+(?:method|model|approach|system|parser|algorithm)|"
            r"their\s+(?:method|model|approach|system|parser|algorithm))\s+is\s+unable\s+to\b",
            re.IGNORECASE,
        ),
        "critique_limitation",
    ),
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
    refined_rules: bool = False,
    refined_rules_v2: bool = False,
    baseline_candidates_path: str | Path = DEFAULT_PHASE1_CANDIDATES_PILOT_REFINED_PATH,
    llm_review_results_path: str | Path = DEFAULT_PHASE1_LLM_REVIEW_RESULTS_PATH,
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
    baseline_candidates = pd.DataFrame()
    if refined_rules_v2:
        baseline_candidates = _read_baseline_candidates(
            Path(baseline_candidates_path),
            context_ids,
        )
        if baseline_candidates.empty:
            baseline_rows = [
                _screen_context(
                    row,
                    object_features.get(str(row["context_id"]), {}),
                    refined_rules=True,
                )
                for row in contexts.to_dict("records")
            ]
            baseline_candidates = _ensure_columns(pd.DataFrame(baseline_rows), OUTPUT_COLUMNS)[
                OUTPUT_COLUMNS
            ]
    elif refined_rules:
        baseline_rows = [
            _screen_context(row, object_features.get(str(row["context_id"]), {}))
            for row in contexts.to_dict("records")
        ]
        baseline_candidates = _ensure_columns(pd.DataFrame(baseline_rows), OUTPUT_COLUMNS)[
            OUTPUT_COLUMNS
        ]
    screened_rows = [
        _screen_context(
            row,
            object_features.get(str(row["context_id"]), {}),
            refined_rules=refined_rules,
            refined_rules_v2=refined_rules_v2,
        )
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
    baseline_metrics = (
        build_phase1_metrics(
            candidates=baseline_candidates,
            object_mentions=object_mentions,
            graph_candidates=graph_candidates,
            cited_title_profiles=cited_title_profiles,
            limit=limit,
            seed=seed,
        )
        if refined_rules or refined_rules_v2
        else None
    )
    report = build_phase1_report(
        metrics=metrics,
        candidates=candidates,
        baseline_metrics=baseline_metrics,
        baseline_candidates=baseline_candidates,
        llm_review_metrics=_read_llm_review_guidance(Path(llm_review_results_path)),
        contexts_path=contexts_input,
        object_mentions_path=Path(object_mentions_path),
        object_graph_candidates_path=Path(object_graph_candidates_path),
        cited_title_profiles_path=Path(cited_title_profiles_path),
        out_candidates_path=out_candidates,
        out_features_path=out_features,
        refined_rules=refined_rules,
        refined_rules_v2=refined_rules_v2,
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
        "llm_priority_distribution": _value_counts(
            candidates,
            ["llm_priority"],
            "contexts",
        ),
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
        "object_type_source_distribution": _value_counts(
            _ensure_columns(candidates, ["object_type_source"]),
            ["object_type_source"],
            "contexts",
        ),
        "primary_intent_by_object_type_source": _group_counts(
            _ensure_columns(
                candidates,
                ["object_type_source", "primary_candidate_intent"],
            ),
            ["object_type_source", "primary_candidate_intent"],
            "contexts",
        ),
        "evidence_span_support_sanity": _evidence_span_support_sanity(candidates),
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
    baseline_metrics: dict[str, Any] | None = None,
    baseline_candidates: pd.DataFrame | None = None,
    llm_review_metrics: pd.DataFrame | None = None,
    contexts_path: Path,
    object_mentions_path: Path,
    object_graph_candidates_path: Path,
    cited_title_profiles_path: Path,
    out_candidates_path: Path,
    out_features_path: Path,
    refined_rules: bool = False,
    refined_rules_v2: bool = False,
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
    if refined_rules_v2:
        title = "# Phase-1 Citation-Function Screening Pilot Refined V2 Report"
    elif refined_rules:
        title = "# Phase-1 Citation-Function Screening Pilot Refined Report"
    else:
        title = "# Phase-1 Citation-Function Screening Pilot Report"
    sections = [
        title,
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
    ]
    has_baseline = baseline_metrics is not None and baseline_candidates is not None
    if (refined_rules or refined_rules_v2) and has_baseline:
        sections.extend(
            [
                "## Before / After Primary Candidate Intent Distribution",
                _table(
                    _before_after_table(
                        baseline_metrics["primary_candidate_intent_distribution"],
                        metrics["primary_candidate_intent_distribution"],
                        key="primary_candidate_intent",
                    )
                ),
                "",
                "## Before / After LLM Routing",
                _table(_before_after_llm_table(baseline_metrics, metrics)),
                "",
                "## Before / After Selected Intent Counts",
                _table(_selected_intent_before_after(baseline_metrics, metrics)),
                "",
                "## Before / After LLM Priority Distribution",
                _table(
                    _before_after_table(
                        baseline_metrics["llm_priority_distribution"],
                        metrics["llm_priority_distribution"],
                        key="llm_priority",
                    )
                ),
                "",
            ]
        )
    if refined_rules_v2:
        sections.extend(
            [
                "## Task 9A.2 LLM Audit Guidance",
                _table(llm_review_metrics if llm_review_metrics is not None else pd.DataFrame()),
                "",
                "## Object Type Source Distribution",
                _table(metrics["object_type_source_distribution"]),
                "",
                "## Primary Intent By Object Type Source",
                _table(metrics["primary_intent_by_object_type_source"]),
                "",
                "## Evidence Span Support Sanity Checks",
                _table(metrics["evidence_span_support_sanity"]),
                "",
            ]
        )
    sections.extend(
        [
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
            "## LLM Priority Distribution",
            _table(metrics["llm_priority_distribution"]),
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
    )
    if (refined_rules or refined_rules_v2) and baseline_candidates is not None:
        sections.extend(
            [
                "## Changed Label Examples: applies -> background/unclear",
                _table(
                    _changed_examples(
                        baseline_candidates,
                        candidates,
                        "applies",
                        {"background", "unclear"},
                        10,
                    )
                ),
                "",
                "## Changed Label Examples: extends -> background/uses/critiques",
                _table(
                    _changed_examples(
                        baseline_candidates,
                        candidates,
                        "extends",
                        {"background", "uses", "critiques"},
                        10,
                    )
                ),
                "",
                "## Changed Label Examples: uses -> background",
                _table(
                    _changed_examples(baseline_candidates, candidates, "uses", {"background"}, 10)
                ),
                "",
                "## Changed Label Examples: critiques -> background/unclear",
                _table(
                    _changed_examples(
                        baseline_candidates,
                        candidates,
                        "critiques",
                        {"background", "unclear"},
                        10,
                    )
                ),
                "",
                "## Changed Label Examples: compares_against -> background/uses",
                _table(
                    _changed_examples(
                        baseline_candidates,
                        candidates,
                        "compares_against",
                        {"background", "uses"},
                        10,
                    )
                ),
                "",
                "## Changed Routing Examples: should_send_to_llm true -> false",
                _table(_routing_changed_examples(baseline_candidates, candidates, 10)),
                "",
                "## High Priority LLM Examples",
                _table(_priority_examples(candidates, "high", 10)),
                "",
                "## Medium Priority LLM Examples",
                _table(_priority_examples(candidates, "medium", 10)),
                "",
                "## Cited-Work Description Examples",
                _table(_cited_work_description_examples(candidates, 10)),
                "",
                "## Current-Paper Use Examples",
                _table(_current_paper_use_examples(candidates, 10)),
                "",
                "## Current-Paper Extend Examples",
                _table(_current_paper_extend_examples(candidates, 10)),
                "",
                "## True Compares Against Examples",
                _table(_true_compare_examples(candidates, 10)),
                "",
            ]
        )
    return "\n".join(sections)


def _screen_context(
    context: dict[str, Any],
    object_feature: dict[str, str],
    *,
    refined_rules: bool = False,
    refined_rules_v2: bool = False,
) -> dict[str, Any]:
    if refined_rules_v2:
        return _screen_context_refined_v2(context, object_feature)
    if refined_rules:
        return _screen_context_refined(context, object_feature)

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
    llm_priority = "medium" if should_send else "none"
    llm_reason = ";".join(send_reasons)
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
            "cited_work_description": False,
            "evidence_span": evidence_span,
            "candidate_intents": _join(intents),
            "primary_candidate_intent": primary_intent,
            "candidate_object_types": candidate_object_types,
            "primary_candidate_object_type": _first_split(candidate_object_types, "unknown"),
            "candidate_relation_subtypes": _join(relation_subtypes),
            "confidence": round(confidence, 3),
            "llm_priority": llm_priority,
            "llm_reason": llm_reason,
            "should_send_to_llm": should_send,
            "phase1_reason": phase1_reason,
            "matched_rules": _join(_unique_preserve_order(matched_rules)),
        }
    )
    return row


def _screen_context_refined(
    context: dict[str, Any],
    object_feature: dict[str, str],
) -> dict[str, Any]:
    sentence = _clean_text(context.get("sentence_text"))
    window = _clean_text(context.get("context_window_s3"))
    normalized_section = _clean_text(context.get("normalized_section")).lower() or "unknown"
    has_object = _as_bool(object_feature.get("has_object_mention"))
    has_graph_candidate = _as_bool(object_feature.get("has_graph_candidate_object"))
    has_generic_metric = bool(object_feature.get("generic_metric_names"))
    has_title_profile_object = bool(object_feature.get("cited_title_profile_object_names"))

    cited_description_matches = _match_cited_work_description(sentence, window)
    cited_work_description = bool(cited_description_matches)
    cue_matches = {
        "use": _match_cues(CURRENT_WORK_USE_CUES, sentence, window),
        "weak_use": _match_cues(WEAK_USE_CUES, sentence, window),
        "compare": _match_cues(REFINED_COMPARE_CUES, sentence, window),
        "extend": _match_cues(EXTEND_CUES, sentence, window),
        "critique": _match_cues(REFINED_CRITIQUE_CUES, sentence, window),
        "apply": _match_cues(APPLY_CUES, sentence, window),
        "background": _match_cues(BACKGROUND_CUES, sentence, window),
        "evaluation": _match_cues(REFINED_EVALUATION_CUES, sentence, window),
        "dataset_feature": _match_cues(DATASET_FEATURE_CUES, sentence, window),
        "cited_description": cited_description_matches,
    }
    cues_by_group = {
        group: [match["label"] for match in matches] for group, matches in cue_matches.items()
    }
    matched_rules = []
    intents = []
    relation_subtypes = []
    strong_current_use = bool(cue_matches["use"])
    explicit_evaluation = bool(cue_matches["evaluation"])
    explicit_compare = bool(cue_matches["compare"])
    weak_use_as_current_use = (
        bool(cue_matches["weak_use"])
        and not cited_work_description
        and has_graph_candidate
        and normalized_section in OBJECT_CONTEXT_SECTIONS
    )

    if cited_work_description:
        intents.append("background")
        matched_rules.append("cited_work_description")
    if cue_matches["background"]:
        intents.append("background")
        matched_rules.append("background_cue")
    if strong_current_use:
        intents.append("uses")
        relation_subtypes.extend(_relation_subtypes_from_matches(cue_matches["use"]))
        matched_rules.append("current_paper_use_cue")
    elif weak_use_as_current_use:
        intents.append("uses")
        relation_subtypes.extend(_relation_subtypes_from_matches(cue_matches["weak_use"]))
        matched_rules.append("weak_use_cue_with_graph_object_in_high_value_section")
    elif cue_matches["weak_use"]:
        matched_rules.append("weak_use_context_feature")

    if explicit_evaluation:
        intents.append("uses")
        relation_subtypes.extend(_relation_subtypes_from_matches(cue_matches["evaluation"]))
        matched_rules.append("explicit_evaluation_cue")
    elif cue_matches["dataset_feature"]:
        matched_rules.append("dataset_context_feature")

    if explicit_compare:
        intents.append("compares_against")
        relation_subtypes.extend(_relation_subtypes_from_matches(cue_matches["compare"]))
        matched_rules.append("explicit_compare_cue")
    if cue_matches["extend"]:
        intents.append("extends")
        relation_subtypes.extend(_relation_subtypes_from_matches(cue_matches["extend"]))
        matched_rules.append("extend_cue")
    if cue_matches["critique"]:
        intents.append("critiques")
        relation_subtypes.extend(_relation_subtypes_from_matches(cue_matches["critique"]))
        matched_rules.append("strong_critique_cue")
    if cue_matches["apply"]:
        intents.append("applies")
        relation_subtypes.extend(_relation_subtypes_from_matches(cue_matches["apply"]))
        matched_rules.append("apply_cue")

    if has_generic_metric and explicit_compare:
        intents.append("compares_against")
        relation_subtypes.append("report_metric")
        matched_rules.append("generic_metric_with_explicit_compare_cue")
    elif has_generic_metric and explicit_evaluation:
        relation_subtypes.append("report_metric")
        matched_rules.append("generic_metric_with_evaluation_cue")
    elif has_generic_metric:
        matched_rules.append("generic_metric_feature_only")

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
    evidence_span = _choose_refined_evidence_span(
        cue_matches=cue_matches,
        primary_intent=primary_intent,
        cited_work_description=cited_work_description,
    )
    confidence = _refined_confidence(
        primary_intent=primary_intent,
        matched_rules=matched_rules,
        has_object=has_object,
        has_graph_candidate=has_graph_candidate,
    )
    llm_priority, llm_reason = _llm_priority(
        intents=intents,
        primary_intent=primary_intent,
        matched_rules=matched_rules,
        normalized_section=normalized_section,
        has_object=has_object,
        has_graph_candidate=has_graph_candidate,
        has_title_profile_object=has_title_profile_object,
        strong_current_use=strong_current_use,
        explicit_compare=explicit_compare,
        explicit_evaluation=explicit_evaluation,
        cited_work_description=cited_work_description,
    )
    should_send = llm_priority in {"high", "medium"}
    phase1_reason = _build_phase1_reason(
        primary_intent=primary_intent,
        confidence=confidence,
        send_reasons=llm_reason.split(";") if llm_reason else [],
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
            "matched_use_cues": _join(cues_by_group["use"] + cues_by_group["weak_use"]),
            "matched_compare_cues": _join(cues_by_group["compare"]),
            "matched_extend_cues": _join(cues_by_group["extend"]),
            "matched_critique_cues": _join(cues_by_group["critique"]),
            "matched_apply_cues": _join(cues_by_group["apply"]),
            "matched_background_cues": _join(
                cues_by_group["background"] + cues_by_group["cited_description"]
            ),
            "matched_evaluation_cues": _join(
                cues_by_group["evaluation"] + cues_by_group["dataset_feature"]
            ),
            "cited_work_description": cited_work_description,
            "evidence_span": evidence_span,
            "candidate_intents": _join(intents),
            "primary_candidate_intent": primary_intent,
            "candidate_object_types": candidate_object_types,
            "primary_candidate_object_type": _first_split(candidate_object_types, "unknown"),
            "candidate_relation_subtypes": _join(relation_subtypes),
            "confidence": round(confidence, 3),
            "llm_priority": llm_priority,
            "llm_reason": llm_reason,
            "should_send_to_llm": should_send,
            "phase1_reason": phase1_reason,
            "matched_rules": _join(_unique_preserve_order(matched_rules)),
        }
    )
    return row


def _screen_context_refined_v2(
    context: dict[str, Any],
    object_feature: dict[str, str],
) -> dict[str, Any]:
    sentence = _clean_text(context.get("sentence_text"))
    normalized_section = _clean_text(context.get("normalized_section")).lower() or "unknown"
    has_object = _as_bool(object_feature.get("has_object_mention"))
    has_graph_candidate = _as_bool(object_feature.get("has_graph_candidate_object"))
    has_generic_metric = bool(object_feature.get("generic_metric_names"))
    has_title_profile_object = bool(object_feature.get("cited_title_profile_object_names"))
    object_type, object_type_source, object_type_confidence = _assign_object_type_v2(
        object_feature
    )

    cited_description_matches = _match_cited_work_description(sentence, "")
    cited_work_description = bool(cited_description_matches)
    cue_matches = {
        "use": _match_sentence_cues(V2_CURRENT_WORK_USE_CUES, sentence),
        "weak_use": _match_sentence_cues(WEAK_USE_CUES, sentence),
        "compare": _match_sentence_cues(V2_COMPARE_CUES, sentence),
        "extend": _match_sentence_cues(V2_CURRENT_EXTEND_CUES, sentence),
        "weak_extend": _match_sentence_cues(V2_WEAK_EXTEND_CUES, sentence),
        "critique": _match_sentence_cues(V2_CRITIQUE_CUES, sentence),
        "apply": _match_sentence_cues(V2_CURRENT_APPLY_CUES, sentence),
        "weak_apply": _match_sentence_cues(V2_WEAK_APPLY_CUES, sentence),
        "background": _match_sentence_cues(BACKGROUND_CUES, sentence),
        "evaluation": _match_sentence_cues(REFINED_EVALUATION_CUES, sentence),
        "dataset_feature": _match_sentence_cues(DATASET_FEATURE_CUES, sentence),
        "cited_description": cited_description_matches,
    }
    cues_by_group = {
        group: [match["label"] for match in matches] for group, matches in cue_matches.items()
    }
    matched_rules = []
    intents = []
    relation_subtypes = []
    strong_current_use = bool(cue_matches["use"])
    explicit_apply = bool(cue_matches["apply"])
    explicit_extend = bool(cue_matches["extend"])
    explicit_compare = bool(cue_matches["compare"])
    explicit_critique = bool(cue_matches["critique"])
    weak_cue = bool(
        cue_matches["weak_use"]
        or cue_matches["weak_apply"]
        or cue_matches["weak_extend"]
        or cue_matches["evaluation"]
        or cue_matches["dataset_feature"]
    )

    if cited_work_description:
        intents.append("background")
        matched_rules.append("cited_work_description")
    if cue_matches["background"]:
        intents.append("background")
        matched_rules.append("background_cue")
    if explicit_critique:
        intents.append("critiques")
        relation_subtypes.extend(_relation_subtypes_from_matches(cue_matches["critique"]))
        matched_rules.append("targeted_critique_cue")
    if explicit_extend:
        intents.append("extends")
        relation_subtypes.extend(_relation_subtypes_from_matches(cue_matches["extend"]))
        matched_rules.append("current_paper_extend_cue")
    elif cue_matches["weak_extend"]:
        matched_rules.append("weak_extend_context_feature")
    if explicit_compare:
        intents.append("compares_against")
        relation_subtypes.extend(_relation_subtypes_from_matches(cue_matches["compare"]))
        matched_rules.append("explicit_compare_cue")
    if explicit_apply:
        intents.append("applies")
        relation_subtypes.extend(_relation_subtypes_from_matches(cue_matches["apply"]))
        matched_rules.append("current_paper_apply_cue")
    elif cue_matches["weak_apply"]:
        matched_rules.append("weak_apply_context_feature")
    if strong_current_use:
        intents.append("uses")
        relation_subtypes.extend(_relation_subtypes_from_matches(cue_matches["use"]))
        matched_rules.append("current_paper_use_cue")
    elif cue_matches["weak_use"]:
        matched_rules.append("weak_use_context_feature")

    if has_generic_metric and explicit_compare:
        intents.append("compares_against")
        relation_subtypes.append("report_metric")
        matched_rules.append("generic_metric_with_explicit_compare_cue")
    elif has_generic_metric and cue_matches["evaluation"]:
        relation_subtypes.append("report_metric")
        matched_rules.append("generic_metric_with_evaluation_cue")
    elif has_generic_metric:
        matched_rules.append("generic_metric_feature_only")

    if cue_matches["evaluation"] and not strong_current_use:
        matched_rules.append("evaluation_context_feature")
    if cue_matches["dataset_feature"]:
        matched_rules.append("dataset_context_feature")

    if not intents:
        section_prior = _section_prior_intent_v2(normalized_section)
        if section_prior is not None:
            intents.append(section_prior)
            matched_rules.append(f"weak_section_prior:{normalized_section}")
        else:
            intents.append("unclear")
            matched_rules.append("no_cue" if not weak_cue else "weak_cue_without_current_subject")

    intents = _unique_preserve_order(intents)
    relation_subtypes = _unique_preserve_order(relation_subtypes) or ["none"]
    primary_intent = _primary_intent(intents)
    evidence_span = _choose_refined_v2_evidence_span(
        cue_matches=cue_matches,
        primary_intent=primary_intent,
        cited_work_description=cited_work_description,
    )
    confidence = _refined_v2_confidence(
        primary_intent=primary_intent,
        matched_rules=matched_rules,
        object_type_source=object_type_source,
        has_object=has_object,
        has_graph_candidate=has_graph_candidate,
    )
    llm_priority, llm_reason = _llm_priority_v2(
        intents=intents,
        primary_intent=primary_intent,
        matched_rules=matched_rules,
        object_type_source=object_type_source,
        normalized_section=normalized_section,
        has_object=has_object,
        has_graph_candidate=has_graph_candidate,
        has_generic_metric=has_generic_metric,
        has_title_profile_object=has_title_profile_object,
        cited_work_description=cited_work_description,
    )
    should_send = llm_priority in {"high", "medium"}
    phase2_candidate_type = _phase2_candidate_type(
        primary_intent=primary_intent,
        intents=intents,
        matched_rules=matched_rules,
        object_type_source=object_type_source,
        cited_work_description=cited_work_description,
    )
    phase1_reason = _build_phase1_reason(
        primary_intent=primary_intent,
        confidence=confidence,
        send_reasons=llm_reason.split(";") if llm_reason else [],
        has_object=has_object,
        has_graph_candidate=has_graph_candidate,
    )
    candidate_object_types = _candidate_object_types_v2(object_feature, object_type_source)
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
            "matched_use_cues": _join(cues_by_group["use"] + cues_by_group["weak_use"]),
            "matched_compare_cues": _join(cues_by_group["compare"]),
            "matched_extend_cues": _join(cues_by_group["extend"] + cues_by_group["weak_extend"]),
            "matched_critique_cues": _join(cues_by_group["critique"]),
            "matched_apply_cues": _join(cues_by_group["apply"] + cues_by_group["weak_apply"]),
            "matched_background_cues": _join(
                cues_by_group["background"] + cues_by_group["cited_description"]
            ),
            "matched_evaluation_cues": _join(
                cues_by_group["evaluation"] + cues_by_group["dataset_feature"]
            ),
            "cited_work_description": cited_work_description,
            "evidence_span": evidence_span,
            "candidate_intents": _join(intents),
            "primary_candidate_intent": primary_intent,
            "candidate_object_types": candidate_object_types,
            "primary_candidate_object_type": object_type,
            "object_type_source": object_type_source,
            "object_type_confidence": round(object_type_confidence, 3),
            "candidate_relation_subtypes": _join(relation_subtypes),
            "confidence": round(confidence, 3),
            "llm_priority": llm_priority,
            "llm_reason": llm_reason,
            "should_send_to_llm": should_send,
            "phase2_candidate_type": phase2_candidate_type,
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


def _read_baseline_candidates(path: Path, context_ids: set[str]) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=OUTPUT_COLUMNS)
    parquet_file = pq.ParquetFile(path)
    available_columns = set(parquet_file.schema_arrow.names)
    if "context_id" not in available_columns:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)
    columns = [column for column in OUTPUT_COLUMNS if column in available_columns]
    batches = []
    for batch in parquet_file.iter_batches(batch_size=100_000, columns=columns):
        frame = batch.to_pandas()
        frame["context_id"] = frame["context_id"].astype(str)
        frame = frame.loc[frame["context_id"].isin(context_ids)]
        if not frame.empty:
            batches.append(frame)
    if not batches:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)
    return _ensure_columns(pd.concat(batches, ignore_index=True), OUTPUT_COLUMNS)[OUTPUT_COLUMNS]


def _read_llm_review_guidance(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        review = pd.read_parquet(path)
    except (OSError, ValueError):
        return pd.DataFrame()
    if review.empty or "primary_candidate_intent" not in review.columns:
        return pd.DataFrame()
    rows = [
        {"audit_metric": "reviewed_rows", "value": int(len(review))},
    ]
    if "intent_correct" in review.columns:
        reviewed = review.loc[review["intent_correct"].isin(["true", "false"])]
        for intent, group in reviewed.groupby("primary_candidate_intent", dropna=False):
            rows.append(
                {
                    "audit_metric": f"task9a2_precision:{intent}",
                    "value": round(float(group["intent_correct"].eq("true").mean()), 3),
                }
            )
    if "recommended_rule_action" in review.columns:
        top_actions = review["recommended_rule_action"].value_counts().head(8)
        for action, count in top_actions.items():
            rows.append(
                {
                    "audit_metric": f"recommended_action:{action}",
                    "value": int(count),
                }
            )
    if "error_type" in review.columns:
        top_errors = review["error_type"].value_counts().head(8)
        for error_type, count in top_errors.items():
            rows.append(
                {
                    "audit_metric": f"error_type:{error_type}",
                    "value": int(count),
                }
            )
    return pd.DataFrame(rows)


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
        item["graph_candidate_object_types"] = _join_unique(group["object_type"])
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
        item.setdefault("graph_candidate_object_types", "")
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


def _match_sentence_cues(
    cue_patterns: list[CuePattern],
    sentence: str,
) -> list[dict[str, str | int]]:
    return _match_cues(cue_patterns, sentence, "")


def _match_critique_cues(sentence: str, context_window: str) -> list[dict[str, str | int]]:
    strong = _match_cues(STRONG_CRITIQUE_CUES, sentence, context_window)
    weak = _match_cues([WEAK_CRITIQUE_CUE], sentence, context_window)
    if strong:
        return strong + weak
    return []


def _match_cited_work_description(sentence: str, context_window: str) -> list[dict[str, str | int]]:
    matches = _match_cues(CITED_WORK_DESCRIPTION_CUES, sentence, context_window)
    if not matches:
        return []
    citation_like = bool(
        re.search(r"\b[A-Z][A-Za-z'`-]+(?:\s+et\s+al\.)?\s*\(\d{4}[a-z]?\)", sentence)
        or re.search(r"\b[A-Z][A-Za-z'`-]+\s+and\s+[A-Z][A-Za-z'`-]+", sentence)
        or re.search(r"\bauthors?\s+(?:in\s+)?\(", sentence, re.IGNORECASE)
    )
    if citation_like:
        return matches
    return []


def _relation_subtypes_from_cues(cue_matches: dict[str, list[dict[str, str | int]]]) -> list[str]:
    relation_subtypes = []
    for matches in cue_matches.values():
        relation_subtypes.extend(_relation_subtypes_from_matches(matches))
    return relation_subtypes


def _relation_subtypes_from_matches(matches: list[dict[str, str | int]]) -> list[str]:
    relation_subtypes = []
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


def _choose_refined_evidence_span(
    *,
    cue_matches: dict[str, list[dict[str, str | int]]],
    primary_intent: str,
    cited_work_description: bool,
) -> str:
    if cited_work_description and primary_intent == "background":
        description_span = _first_evidence_match(cue_matches["cited_description"])
        if description_span:
            return description_span
    priority = [
        "critique",
        "extend",
        "compare",
        "use",
        "evaluation",
        "apply",
        "background",
        "cited_description",
        "weak_use",
        "dataset_feature",
    ]
    if primary_intent == "uses":
        priority = ["use", "evaluation", "weak_use", *priority]
    elif primary_intent == "compares_against":
        priority = ["compare", *priority]
    elif primary_intent == "extends":
        priority = ["extend", *priority]
    elif primary_intent == "critiques":
        priority = ["critique", *priority]
    elif primary_intent == "applies":
        priority = ["apply", *priority]
    elif primary_intent == "background":
        priority = ["background", "cited_description", *priority]
    seen = set()
    for group in priority:
        if group in seen:
            continue
        seen.add(group)
        span = _first_evidence_match(cue_matches.get(group, []))
        if span:
            return span
    return ""


def _first_evidence_match(matches: list[dict[str, str | int]]) -> str:
    if not matches:
        return ""
    sentence_matches = [match for match in matches if match["matched_in"] == "sentence_text"]
    selected = sorted(sentence_matches or matches, key=lambda item: int(item["start"]))[0]
    return str(selected["span"])


def _choose_refined_v2_evidence_span(
    *,
    cue_matches: dict[str, list[dict[str, str | int]]],
    primary_intent: str,
    cited_work_description: bool,
) -> str:
    if cited_work_description and primary_intent == "background":
        description_span = _first_evidence_match(cue_matches["cited_description"])
        if description_span:
            return description_span
    priority = [
        "critique",
        "extend",
        "compare",
        "apply",
        "use",
        "background",
        "cited_description",
        "evaluation",
        "weak_use",
        "weak_apply",
        "weak_extend",
        "dataset_feature",
    ]
    if primary_intent == "uses":
        priority = ["use", *priority]
    elif primary_intent == "applies":
        priority = ["apply", *priority]
    elif primary_intent == "extends":
        priority = ["extend", *priority]
    elif primary_intent == "compares_against":
        priority = ["compare", *priority]
    elif primary_intent == "critiques":
        priority = ["critique", *priority]
    elif primary_intent == "background":
        priority = ["background", "cited_description", *priority]
    seen = set()
    for group in priority:
        if group in seen:
            continue
        seen.add(group)
        span = _first_evidence_match(cue_matches.get(group, []))
        if span:
            return span
    return ""


def _assign_object_type_v2(object_feature: dict[str, str]) -> tuple[str, str, float]:
    graph_types = object_feature.get("graph_candidate_object_types", "")
    direct_types = object_feature.get("object_types", "")
    title_types = object_feature.get("cited_title_profile_object_types", "")
    has_graph_candidate = _as_bool(object_feature.get("has_graph_candidate_object"))
    has_direct_object = _as_bool(object_feature.get("has_object_mention"))
    has_generic_metric = bool(object_feature.get("generic_metric_names"))
    direct_type_values = _split_semicolon(direct_types)
    has_non_metric_direct = any(value != "metric" for value in direct_type_values)
    if has_graph_candidate:
        return _first_split(graph_types or direct_types, "unknown"), "object_graph_candidate", 0.95
    if has_generic_metric and not has_non_metric_direct:
        return "metric", "generic_metric_feature", 0.75
    if has_direct_object and direct_types:
        return _first_split(direct_types, "unknown"), "object_mention", 0.8
    if title_types:
        return _first_split(title_types, "unknown"), "cited_title_profile", 0.45
    return "unknown", "none", 0.0


def _candidate_object_types_v2(object_feature: dict[str, str], object_type_source: str) -> str:
    if object_type_source == "object_graph_candidate":
        return object_feature.get("graph_candidate_object_types") or object_feature.get(
            "object_types",
            "unknown",
        )
    if object_type_source == "generic_metric_feature":
        return "metric"
    if object_type_source == "object_mention":
        return object_feature.get("object_types", "unknown")
    if object_type_source == "cited_title_profile":
        return object_feature.get("cited_title_profile_object_types", "unknown")
    return "unknown"


def _section_prior_intent(normalized_section: str) -> str | None:
    if normalized_section in BACKGROUND_SECTIONS:
        return "background"
    if normalized_section in CRITIQUE_SECTIONS:
        return "critiques"
    if normalized_section in CONCLUSION_SECTIONS:
        return "background"
    return None


def _section_prior_intent_v2(normalized_section: str) -> str | None:
    if normalized_section in BACKGROUND_SECTIONS or normalized_section in CONCLUSION_SECTIONS:
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


def _refined_confidence(
    *,
    primary_intent: str,
    matched_rules: list[str],
    has_object: bool,
    has_graph_candidate: bool,
) -> float:
    if "weak_section_prior" in ";".join(matched_rules):
        return 0.35 if primary_intent == "background" else 0.4
    if "no_cue" in matched_rules:
        return 0.42 if has_graph_candidate else 0.35 if has_object else 0.2
    if "cited_work_description" in matched_rules and primary_intent == "background":
        return 0.6 if has_object or has_graph_candidate else 0.55
    if primary_intent in {"compares_against", "extends", "critiques"}:
        return 0.9 if has_graph_candidate else 0.75
    if primary_intent in {"uses", "applies"}:
        if "current_paper_use_cue" in matched_rules and has_graph_candidate:
            return 0.9
        if "current_paper_use_cue" in matched_rules and has_object:
            return 0.85
        if "weak_use_cue_with_graph_object_in_high_value_section" in matched_rules:
            return 0.65
        return 0.65
    if primary_intent == "background":
        return 0.55
    return 0.45 if has_object else 0.25


def _refined_v2_confidence(
    *,
    primary_intent: str,
    matched_rules: list[str],
    object_type_source: str,
    has_object: bool,
    has_graph_candidate: bool,
) -> float:
    strong_object_source = object_type_source in {"object_graph_candidate", "object_mention"}
    if any(rule.startswith("weak_section_prior:") for rule in matched_rules):
        return 0.35
    if "no_cue" in matched_rules:
        return 0.35 if has_object or has_graph_candidate else 0.2
    if "weak_cue_without_current_subject" in matched_rules:
        return 0.42 if has_object or has_graph_candidate else 0.3
    if "cited_work_description" in matched_rules and primary_intent == "background":
        return 0.62 if object_type_source != "none" else 0.55
    if primary_intent == "uses":
        if "current_paper_use_cue" in matched_rules and has_graph_candidate:
            return 0.9
        if "current_paper_use_cue" in matched_rules and strong_object_source:
            return 0.84
        return 0.62
    if primary_intent == "applies":
        if "current_paper_apply_cue" in matched_rules and has_graph_candidate:
            return 0.88
        if "current_paper_apply_cue" in matched_rules and strong_object_source:
            return 0.82
        return 0.62
    if primary_intent == "extends":
        if "current_paper_extend_cue" in matched_rules and has_graph_candidate:
            return 0.88
        if "current_paper_extend_cue" in matched_rules and strong_object_source:
            return 0.82
        return 0.62
    if primary_intent == "compares_against":
        if "explicit_compare_cue" in matched_rules and (has_graph_candidate or has_object):
            return 0.85
        if "generic_metric_with_explicit_compare_cue" in matched_rules:
            return 0.78
        return 0.65
    if primary_intent == "critiques":
        return 0.82 if strong_object_source else 0.65
    if primary_intent == "background":
        return 0.58 if object_type_source != "none" else 0.5
    return 0.35 if object_type_source != "none" else 0.22


def _llm_priority(
    *,
    intents: list[str],
    primary_intent: str,
    matched_rules: list[str],
    normalized_section: str,
    has_object: bool,
    has_graph_candidate: bool,
    has_title_profile_object: bool,
    strong_current_use: bool,
    explicit_compare: bool,
    explicit_evaluation: bool,
    cited_work_description: bool,
) -> tuple[str, str]:
    reasons = []
    non_background = {intent for intent in intents if intent not in {"background", "unclear"}}
    if primary_intent in {"extends", "critiques", "compares_against"} and any(
        rule in matched_rules
        for rule in {"extend_cue", "strong_critique_cue", "explicit_compare_cue"}
    ):
        reasons.append("strong_explicit_non_background_cue")
    if has_graph_candidate and (
        strong_current_use or explicit_compare or "extend_cue" in matched_rules
    ):
        reasons.append("graph_object_with_current_use_compare_or_extend")
    if len(non_background) > 1:
        reasons.append("multiple_conflicting_non_background_labels")
    if "generic_metric_with_explicit_compare_cue" in matched_rules:
        reasons.append("generic_metric_with_explicit_compare_cue")
    if reasons:
        return "high", ";".join(_unique_preserve_order(reasons))

    if has_object and any(
        rule in matched_rules
        for rule in {
            "weak_use_context_feature",
            "weak_use_cue_with_graph_object_in_high_value_section",
            "dataset_context_feature",
            "generic_metric_with_evaluation_cue",
        }
    ):
        reasons.append("object_mention_with_weak_cue")
    if cited_work_description and (has_object or has_graph_candidate or has_title_profile_object):
        reasons.append("cited_work_description_with_high_value_object")
    if primary_intent == "unclear" and has_graph_candidate:
        reasons.append("unclear_with_graph_candidate")
    if strong_current_use and not has_object:
        reasons.append("current_paper_use_without_object_evidence")
    if explicit_evaluation and has_object:
        reasons.append("object_mention_with_evaluation_cue")
    if reasons:
        return "medium", ";".join(_unique_preserve_order(reasons))

    if primary_intent == "background" and has_object:
        return "low", "background_with_object_mention"
    if "no_cue" in matched_rules and has_object:
        return "low", "no_cue_object_mention"
    if any(rule.startswith("weak_section_prior:") for rule in matched_rules):
        return "low", "section_prior_only"
    if primary_intent == "background" and not has_object:
        return "none", "clear_background_no_object"
    if "no_cue" in matched_rules and not has_object:
        return "none", "no_cue_no_object"
    if normalized_section in HIGH_VALUE_SECTIONS and has_object:
        return "low", f"high_value_section_object:{normalized_section}"
    return "none", "no_priority_rule"


def _llm_priority_v2(
    *,
    intents: list[str],
    primary_intent: str,
    matched_rules: list[str],
    object_type_source: str,
    normalized_section: str,
    has_object: bool,
    has_graph_candidate: bool,
    has_generic_metric: bool,
    has_title_profile_object: bool,
    cited_work_description: bool,
) -> tuple[str, str]:
    reasons = []
    strong_object = object_type_source in {"object_graph_candidate", "object_mention"}
    strong_non_background_rules = {
        "current_paper_use_cue",
        "current_paper_apply_cue",
        "current_paper_extend_cue",
        "explicit_compare_cue",
        "targeted_critique_cue",
    }
    matched_strong = any(rule in matched_rules for rule in strong_non_background_rules)
    non_background = {intent for intent in intents if intent not in {"background", "unclear"}}
    if matched_strong and (has_graph_candidate or strong_object):
        reasons.append("explicit_current_relation_with_strong_object")
    if (
        primary_intent == "compares_against"
        and has_generic_metric
        and "explicit_compare_cue" in matched_rules
    ):
        reasons.append("explicit_compare_with_metric")
    if len(non_background) > 1 and matched_strong:
        reasons.append("multiple_strong_non_background_cues")
    if reasons:
        return "high", ";".join(_unique_preserve_order(reasons))

    weak_rules = {
        "weak_use_context_feature",
        "weak_apply_context_feature",
        "weak_extend_context_feature",
        "evaluation_context_feature",
        "dataset_context_feature",
        "generic_metric_with_evaluation_cue",
    }
    if has_object and any(rule in matched_rules for rule in weak_rules):
        reasons.append("weak_cue_with_object_mention")
    if cited_work_description and (has_object or has_graph_candidate or has_title_profile_object):
        reasons.append("cited_work_description_with_high_value_object")
    if primary_intent == "unclear" and has_graph_candidate:
        reasons.append("unclear_with_graph_candidate")
    if matched_strong and object_type_source == "none":
        reasons.append("explicit_relation_without_object_evidence")
    if has_generic_metric and "generic_metric_with_evaluation_cue" in matched_rules:
        reasons.append("generic_metric_with_evaluation_cue")
    if reasons:
        return "medium", ";".join(_unique_preserve_order(reasons))

    if primary_intent == "background" and has_graph_candidate:
        return "medium", "background_with_graph_candidate_object"
    if primary_intent == "background" and has_object:
        return "low", "background_with_object_mention"
    if object_type_source == "generic_metric_feature":
        return "low", "generic_metric_feature_only"
    if "no_cue" in matched_rules and has_object:
        return "low", "object_mention_but_no_cue"
    if any(rule.startswith("weak_section_prior:") for rule in matched_rules):
        return "low", "section_prior_only"
    if normalized_section in HIGH_VALUE_SECTIONS and has_object:
        return "low", f"high_value_section_object:{normalized_section}"
    if primary_intent == "background" and not has_object:
        return "none", "clear_background_no_object"
    if "no_cue" in matched_rules and not has_object:
        return "none", "no_cue_no_object"
    return "none", "no_priority_rule"


def _phase2_candidate_type(
    *,
    primary_intent: str,
    intents: list[str],
    matched_rules: list[str],
    object_type_source: str,
    cited_work_description: bool,
) -> str:
    non_background = [intent for intent in intents if intent not in {"background", "unclear"}]
    if len(non_background) > 1:
        return "ambiguous_multi_intent"
    if any(
        rule in matched_rules
        for rule in {
            "current_paper_use_cue",
            "current_paper_apply_cue",
            "current_paper_extend_cue",
            "explicit_compare_cue",
            "targeted_critique_cue",
        }
    ):
        return "explicit_current_paper_relation"
    if cited_work_description:
        return "cited_work_description"
    if object_type_source == "generic_metric_feature":
        return "generic_metric_feature"
    if any(rule.startswith("weak_section_prior:") for rule in matched_rules):
        return "background_prior"
    if any("weak_" in rule or "evaluation_context_feature" in rule for rule in matched_rules):
        return "weak_cue_feature"
    if primary_intent == "unclear" and object_type_source != "none":
        return "object_only_unclear"
    return "no_cue"


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


def _priority_examples(candidates: pd.DataFrame, priority: str, limit: int) -> pd.DataFrame:
    return _format_examples(candidates.loc[candidates["llm_priority"].eq(priority)], limit)


def _cited_work_description_examples(candidates: pd.DataFrame, limit: int) -> pd.DataFrame:
    return _format_examples(
        candidates.loc[candidates["cited_work_description"].map(_as_bool)], limit
    )


def _current_paper_use_examples(candidates: pd.DataFrame, limit: int) -> pd.DataFrame:
    mask = candidates["matched_rules"].fillna("").astype(str).str.contains("current_paper_use_cue")
    return _format_examples(candidates.loc[mask], limit)


def _current_paper_extend_examples(candidates: pd.DataFrame, limit: int) -> pd.DataFrame:
    mask = (
        candidates["matched_rules"]
        .fillna("")
        .astype(str)
        .str.contains("current_paper_extend_cue")
    )
    return _format_examples(candidates.loc[mask], limit)


def _true_compare_examples(candidates: pd.DataFrame, limit: int) -> pd.DataFrame:
    mask = candidates["matched_rules"].fillna("").astype(str).str.contains("explicit_compare_cue")
    return _format_examples(candidates.loc[mask], limit)


def _changed_examples(
    before: pd.DataFrame,
    after: pd.DataFrame,
    before_intent: str,
    after_intents: set[str],
    limit: int,
) -> pd.DataFrame:
    merged = _merge_before_after(before, after)
    mask = merged["before_primary_candidate_intent"].eq(before_intent) & merged[
        "primary_candidate_intent"
    ].isin(after_intents)
    return _format_changed_examples(merged.loc[mask], limit)


def _routing_changed_examples(
    before: pd.DataFrame, after: pd.DataFrame, limit: int
) -> pd.DataFrame:
    merged = _merge_before_after(before, after)
    mask = merged["before_should_send_to_llm"].map(_as_bool) & ~merged["should_send_to_llm"].map(
        _as_bool
    )
    return _format_changed_examples(merged.loc[mask], limit)


def _merge_before_after(before: pd.DataFrame, after: pd.DataFrame) -> pd.DataFrame:
    before_columns = [
        "context_id",
        "primary_candidate_intent",
        "candidate_intents",
        "should_send_to_llm",
    ]
    before_slim = _ensure_columns(before.copy(), before_columns)[before_columns].rename(
        columns={
            "primary_candidate_intent": "before_primary_candidate_intent",
            "candidate_intents": "before_candidate_intents",
            "should_send_to_llm": "before_should_send_to_llm",
        }
    )
    return after.merge(before_slim, on="context_id", how="left")


def _format_changed_examples(frame: pd.DataFrame, limit: int) -> pd.DataFrame:
    columns = [
        "context_id",
        "normalized_section",
        "before_primary_candidate_intent",
        "primary_candidate_intent",
        "before_candidate_intents",
        "candidate_intents",
        "llm_priority",
        "should_send_to_llm",
        "cited_work_description",
        "object_names",
        "evidence_span",
        "matched_rules",
        "sentence_text",
    ]
    sample = _ensure_columns(frame.head(limit).copy(), columns)
    for column in ("sentence_text", "object_names", "matched_rules"):
        sample[column] = sample[column].map(lambda value: _truncate(value, 180))
    return sample[columns]


def _format_examples(frame: pd.DataFrame, limit: int) -> pd.DataFrame:
    columns = [
        "context_id",
        "normalized_section",
        "primary_candidate_intent",
        "phase2_candidate_type",
        "candidate_intents",
        "candidate_relation_subtypes",
        "confidence",
        "llm_priority",
        "llm_reason",
        "should_send_to_llm",
        "cited_work_description",
        "object_type_source",
        "primary_candidate_object_type",
        "object_names",
        "generic_metric_names",
        "evidence_span",
        "matched_rules",
        "sentence_text",
    ]
    sample = _ensure_columns(frame.head(limit).copy(), columns)
    for column in (
        "sentence_text",
        "object_names",
        "generic_metric_names",
        "matched_rules",
        "llm_reason",
    ):
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


def _before_after_table(
    before: pd.DataFrame,
    after: pd.DataFrame,
    *,
    key: str,
) -> pd.DataFrame:
    before_slim = _ensure_columns(before.copy(), [key, "contexts"]).rename(
        columns={"contexts": "before_contexts"}
    )
    after_slim = _ensure_columns(after.copy(), [key, "contexts"]).rename(
        columns={"contexts": "after_contexts"}
    )
    merged = before_slim.merge(after_slim, on=key, how="outer").fillna(0)
    merged["before_contexts"] = merged["before_contexts"].astype(int)
    merged["after_contexts"] = merged["after_contexts"].astype(int)
    merged["delta"] = merged["after_contexts"] - merged["before_contexts"]
    return merged.sort_values("after_contexts", ascending=False).reset_index(drop=True)


def _before_after_llm_table(
    before_metrics: dict[str, Any],
    after_metrics: dict[str, Any],
) -> pd.DataFrame:
    before_rate = before_metrics["should_send_to_llm_rate"]
    after_rate = after_metrics["should_send_to_llm_rate"]
    return pd.DataFrame(
        [
            {
                "metric": "should_send_to_llm_count",
                "before": before_metrics["should_send_to_llm_count"],
                "after": after_metrics["should_send_to_llm_count"],
                "delta": after_metrics["should_send_to_llm_count"]
                - before_metrics["should_send_to_llm_count"],
            },
            {
                "metric": "should_send_to_llm_rate",
                "before": f"{before_rate:.3f}",
                "after": f"{after_rate:.3f}",
                "delta": f"{after_rate - before_rate:.3f}",
            },
        ]
    )


def _evidence_span_support_sanity(candidates: pd.DataFrame) -> pd.DataFrame:
    if candidates.empty:
        return pd.DataFrame(columns=["check", "rows", "rate"])
    frame = _ensure_columns(
        candidates,
        [
            "evidence_span",
            "sentence_text",
            "context_window_s3",
            "primary_candidate_intent",
            "llm_priority",
            "matched_rules",
        ],
    )
    spans = frame["evidence_span"].fillna("").astype(str)
    has_span = spans.ne("")
    in_sentence = [
        bool(span and span in _clean_text(sentence))
        for span, sentence in zip(spans, frame["sentence_text"], strict=False)
    ]
    in_window = [
        bool(span and span in _clean_text(window))
        for span, window in zip(spans, frame["context_window_s3"], strict=False)
    ]
    grounded = pd.Series(in_sentence, index=frame.index) | pd.Series(in_window, index=frame.index)
    high_current = frame["llm_priority"].eq("high") & frame["primary_candidate_intent"].isin(
        ["uses", "extends", "applies"]
    )
    current_rule = frame["matched_rules"].fillna("").astype(str).str.contains(
        "current_paper_(?:use|extend|apply)_cue",
        regex=True,
    )
    return pd.DataFrame(
        [
            {
                "check": "rows_with_evidence_span",
                "rows": int(has_span.sum()),
                "rate": round(_safe_rate(int(has_span.sum()), len(frame)), 3),
            },
            {
                "check": "evidence_span_exactly_grounded",
                "rows": int((has_span & grounded).sum()),
                "rate": round(_safe_rate(int((has_span & grounded).sum()), int(has_span.sum())), 3),
            },
            {
                "check": "evidence_span_missing_or_ungrounded",
                "rows": int((has_span & ~grounded).sum()),
                "rate": round(_safe_rate(int((has_span & ~grounded).sum()), len(frame)), 3),
            },
            {
                "check": "high_current_relation_rows",
                "rows": int(high_current.sum()),
                "rate": round(_safe_rate(int(high_current.sum()), len(frame)), 3),
            },
            {
                "check": "high_current_relation_has_current_cue",
                "rows": int((high_current & current_rule).sum()),
                "rate": round(
                    _safe_rate(int((high_current & current_rule).sum()), int(high_current.sum())),
                    3,
                ),
            },
        ]
    )


def _selected_intent_before_after(
    before_metrics: dict[str, Any],
    after_metrics: dict[str, Any],
) -> pd.DataFrame:
    before = before_metrics["primary_candidate_intent_distribution"].set_index(
        "primary_candidate_intent"
    )["contexts"]
    after = after_metrics["primary_candidate_intent_distribution"].set_index(
        "primary_candidate_intent"
    )["contexts"]
    rows = []
    for intent in [
        "applies",
        "extends",
        "uses",
        "critiques",
        "compares_against",
        "background",
        "unclear",
    ]:
        before_count = int(before.get(intent, 0))
        after_count = int(after.get(intent, 0))
        rows.append(
            {
                "primary_candidate_intent": intent,
                "before_contexts": before_count,
                "after_contexts": after_count,
                "delta": after_count - before_count,
            }
        )
    return pd.DataFrame(rows)


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


def _split_semicolon(value: Any) -> list[str]:
    text = _clean_text(value)
    if not text:
        return []
    return [part.strip() for part in text.split(";") if part.strip()]


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
