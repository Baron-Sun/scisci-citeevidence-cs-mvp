# SciSci-CiteEvidence Final Release Report

## Executive summary
SciSci-CiteEvidence turns section-aware citation contexts into an evidence-grounded view of how NLP objects are cited and used.
The release supports four claim families: section-function structure, seed-registry object role signatures, citation-context volume versus evidence-use rank reversals, and exploratory critique cue families.
The main scientific point is that context volume, rhetorical section, object type, and evidence-use function are distinct signals.

## What this release is and is not
This report assembles final-release analyses around grounded citation contexts. It is a course-scale evidence layer, not a universal map of NLP.
- Phase-2 covers the full high/medium Phase-1 queue, not all strong contexts.
- Labels are LLM-assisted, schema-validated, evidence-grounded labels, not human gold annotations.
- Object graph claims are over a curated seed-registry object-use graph, not the full universe of NLP methods.
- Current outputs are an object-use/citation-function graph, not a completed Intern-Atlas-scale method evolution graph.
- total_strong_contexts is citation-context volume rather than graph in-degree.
## Data and evidence scope
All claims below are conditioned on final analysis-ready Phase-2 labels and their retained evidence spans. Source artifacts are listed at the end so figures can be regenerated or audited.

## QA summary
QA is reported as release diagnostics, not as human adjudication. The label set remains LLM-assisted, schema-validated, evidence-grounded labels, not human gold annotations.
| metric | value | note |
| --- | --- | --- |
| total_labels | 2.3e+05 |  |
| analysis_ready_rows | 2.3e+05 |  |
| evidence_span_present_rows | 2.3e+05 |  |
| evidence_span_grounded_rows | 2.3e+05 |  |
| evidence_span_not_grounded_rows | 0 | Rows with a non-empty evidence span that is not an exact substring. |
| evidence_supports_label_true_rows | 2.3e+05 |  |
| abstain_true_rows | 0 |  |
| mean_confidence | 0.892 |  |
### Confidence By Intent
| final_intent | rows | mean_confidence |
| --- | --- | --- |
| applies | 1137 | 0.929 |
| background | 139823 | 0.868 |
| compares_against | 27435 | 0.926 |
| critiques | 6402 | 0.893 |
| extends | 4763 | 0.889 |
| uses | 50191 | 0.937 |
### Remaining Failure Categories
| rows | failure_category | row_share |
| --- | --- | --- |
| 25311 | evidence_span_not_substring | 0.364 |
| 20648 | use_cue_not_accepted | 0.297 |
| 10058 | quote_not_substring | 0.145 |
| 4902 | compare_cue_not_accepted | 0.0706 |
| 2099 | extend_cue_not_accepted | 0.0302 |
| 1798 | schema_error | 0.0259 |

## Finding 1: Section-function grammar
Citation roles follow paper rhetorical structure: implementation and experiment sections can emphasize use, while related-work and introduction sections can emphasize background roles.
Caveat: section-function results are based on final analysis-ready Phase-2 labels, and unknown sections are handled explicitly rather than silently merged into the main panel.
Figure artifact: `figures/final_release/f02_section_function_lift.png`.
| final_intent | rows | row_share | normalized_section | section_label | log_odds_lift |
| --- | --- | --- | --- | --- | --- |
| uses | 973 | 0.764 | implementation | Implementation (N=1.3k) | 2.45 |
| compares_against | 2368 | 0.455 | results | Results (N=5.2k) | 1.82 |
| extends | 131 | 0.113 | abstract | Abstract (N=1.2k) | 1.8 |
| background | 39398 | 0.88 | related_work | Related Work (N=44.8k) | 1.55 |
| uses | 7228 | 0.538 | dataset | Dataset (N=13.4k) | 1.43 |

## Finding 2: Seed-registry object role signatures
Seed-registry objects occupy different citation-use roles, including background canon, operational infrastructure, evaluation anchors, critique targets, and mixed roles.
Caveat: these roles describe a curated seed-registry object-use graph, not the full universe of NLP methods.
Figure artifact: `figures/final_release/f03_object_role_signature_map.png`.
| mean_confidence | canonical_name | object_type | role_quadrant | non_background_edges |
| --- | --- | --- | --- | --- |
| 0.888 | BERT | model | mixed_role | 6982 |
| 0.898 | BLEU | metric | mixed_role | 5521 |
| 0.887 | LSTM | model | canonical_background | 4066 |
| 0.882 | Transformer | model | canonical_background | 2842 |
| 0.911 | GloVe | model | operational_infrastructure | 2613 |

## Finding 3: Citation-context volume vs evidence-use ranking reversal
Citation-context volume is not the same as evidence use. Some cited papers are frequent context anchors but mostly background, while others have fewer contexts and stronger direct evidence-use profiles.
Caveat: total_strong_contexts measures citation-context volume rather than graph in-degree, and default ranking figures exclude thin-tail rows.
Figure artifact: `figures/final_release/f04_context_volume_vs_evidence_use_reversal.png`.
| resolved_cited_title | plot_label | rank_difference_count |
| --- | --- | --- |
| {C}entering: A Framework for Modeling the Local Coherence of Discourse | {C}entering: A Framework for Modeling the... | -2.97e+03 |
| Learning Synchronous Grammars for Semantic Parsing with Lambda Calculus | Learning Synchronous Grammars for Semantic... | -2.92e+03 |
| Improving a Statistical {MT} System with Automatically Learned Rewrite Patterns | Improving a Statistical {MT} System with... | -2.91e+03 |
| Towards Answering Opinion Questions: Separating Facts from Opinions and Identifying the Polar... | Towards Answering Opinion Questions... | -2.9e+03 |
| Learning surface text patterns for a Question Answering System | Learning surface text patterns for a... | -2.87e+03 |

## Finding 4: Exploratory critique bottlenecks
Critique contexts can be grouped into recurring limitation cue families such as metric validity, generalization, data requirements, cost, and tooling reproducibility.
Caveat: this is an exploratory heuristic cue-family map, not a validated bottleneck taxonomy.
Figure artifact: `figures/final_release/f05_critique_bottleneck_heatmap.png`.
| rows | object_type | bottleneck_family | lift_vs_global |
| --- | --- | --- | --- |
| 10 | software_or_tool | reproducibility_tooling | 4.48 |
| 476 | metric | metric_validity | 2.79 |
| 7 | metric | scalability | 2.67 |
| 66 | method | other | 2.47 |
| 6 | software_or_tool | poor_performance | 2.31 |

## Evidence cards / examples
Evidence cards provide compact examples for reviewers. They illustrate the evidence surface but do not convert the release into gold annotation.
| normalized_section | object_type | bottleneck_family | evidence_span |
| --- | --- | --- | --- |
| introduction | metric | computational_cost | they generally suffer from slow and unstable training due to the high variance of policy grad... |
| related_work | model | computational_cost | This contrasts with our results with Transformer-based architecture and is probably explained... |
| introduction | metric | data_resource_requirement | Previous work (Ng and Abrecht, 2015; Liu and Liu, 2008; Liu et al., 2016; Shang et al., 2018)... |
| introduction | metric | data_resource_requirement | Previous work (Ng and Abrecht, 2015; Liu and Liu, 2008; Liu et al., 2016; Shang et al., 2018)... |
| unknown | method | failure_limitation | The cascaded CRF layers of Ju et al. (2018) are the limitation in inference speed. |
| unknown | method | failure_limitation | the attention mechanism fails to provide explanation |

## Limitations
- ACL-OCL / ACL-centric scope: this release analyzes ACL-derived citation contexts.
- Phase-2 covers the full high/medium Phase-1 queue, not all strong contexts.
- Labels are LLM-assisted, schema-validated, evidence-grounded labels, not human gold annotations.
- Object graph claims are over a curated seed-registry object-use graph, not the full universe of NLP methods.
- Unknown sections are retained explicitly and should not be mixed into main panels.
- Strict validation excludes failed rows from final analysis-ready summaries.
- Critique bottleneck families are an exploratory heuristic cue-family map.
- Current outputs are an object-use/citation-function graph, not a completed Intern-Atlas-scale method evolution graph.

## Reproducibility and source artifacts
The report is assembled from source tables and figure paths supplied by the caller. This builder does not create repository artifacts.
| source_path | figure_path | purpose | caveat |
| --- | --- | --- | --- |
| figures/final_release/source_data/qa_summary.csv |  | Document label QA status and validation exclusions. | Labels are LLM-assisted, schema-validated, evidence-grounded labels. |
| figures/final_release/source_data/section_function_lift.csv | figures/final_release/f02_section_function_lift.png | Show whether citation functions follow paper rhetorical structure. | Based on final analysis-ready Phase-2 labels; unknown sections are explicit. |
| figures/final_release/source_data/object_role_signatures.csv | figures/final_release/f03_object_role_signature_map.png | Summarize functional role profiles for curated seed-registry objects. | Seed-registry object-use graph, not the full universe of NLP methods. |
| figures/final_release/source_data/ranking_reversal.csv | figures/final_release/f04_context_volume_vs_evidence_use_reversal.png | Compare citation-context volume ranks against evidence-use ranks. | total_strong_contexts is citation-context volume rather than graph in-degree. |
| figures/final_release/source_data/critique_bottleneck_matrix.csv | figures/final_release/f05_critique_bottleneck_heatmap.png | Map recurring critique cue families by seed-registry object type. | Exploratory heuristic cue-family map; not a validated bottleneck taxonomy. |
|  |  | Provide compact reviewer-facing examples for report claims. | Examples support interpretation but are not gold annotations. |
