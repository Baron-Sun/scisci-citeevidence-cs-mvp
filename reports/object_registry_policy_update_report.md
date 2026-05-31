# Object Registry Policy Update Report

## Inputs
- Registry: `configs/object_registry_seed.yaml`
- LLM-as-judge review: `data/processed/object_mentions_llm_review_results.parquet`

## Registry Objects Updated
| object_or_group | policy_update |
| --- | --- |
| accuracy / F1 / perplexity | generic_metric; feature-only; excluded from object graph |
| Penn Treebank / PTB | PTB requires nearby treebank/corpus/WSJ/dataset cues |
| Transformer | lowercase transformer defaults to generic_architecture |
| seq2seq | lower confidence and require model/architecture cues |
| WordNet | kept globally; graph eligibility remains context dependent |
| BLEU / ROUGE / METEOR | kept as named metrics eligible for graph use |
| resolved_cited_title profiles | kept separate from direct context object evidence |

## Aliases Requiring Context Cue
| object | cues |
| --- | --- |
| PTB | Penn Treebank; Penn Tree Bank; Wall Street Journal; WSJ; treebank; corpus; sections 02-21; sections 2-21; dataset |
| lowercase transformer | Vaswani; self-attention; Transformer model; Transformer architecture; encoder-decoder architecture |
| seq2seq | model; architecture; encoder-decoder; encoder decoder; sequence-to-sequence; sequence to sequence; neural |

## Generic Metrics Kept Feature-Only
accuracy, F1, and perplexity are retained as phase-1 citation-function features and excluded from object graph candidates.

## Object Graph Eligibility Changes
| original_allow_in_object_graph | graph_eligible | mentions |
| --- | --- | --- |
| True | True | 12976 |
| False | False | 2474 |
| True | False | 531 |
| False | True | 12 |

## LLM Review Signals Used
The policy uses `surface_form_refers_to_object` as the primary mention correctness signal when available, falling back to `reviewer_correct`. Graph and feature eligibility use `should_allow_in_object_graph`, `should_use_as_phase1_feature`, `recommended_action`, and `error_type` as advisory signals under the deterministic policy.

### Recommended Action Counts
| recommended_action | rows |
| --- | --- |
| keep | 143 |
| require_context_cue | 28 |
| block_alias | 14 |
| keep_as_feature_only | 10 |
| lower_confidence | 2 |
| other | 2 |
| change_object_type | 1 |

### Error Type Counts
| error_type | rows |
| --- | --- |
| none | 145 |
| ambiguous_short_alias | 18 |
| insufficient_context | 10 |
| case_sensitive_issue | 7 |
| alias_too_generic | 6 |
| matched_unrelated_word | 6 |
| other | 3 |
| context_neighbor_not_relevant | 2 |
| correct_but_not_graph_object | 2 |
| wrong_object_type | 1 |
