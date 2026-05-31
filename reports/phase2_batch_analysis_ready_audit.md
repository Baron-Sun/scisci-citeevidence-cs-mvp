# Phase-2 Batch Analysis-Ready Label Audit

This report defines the final downstream-analysis table for full high+medium Phase-2 Batch labels. Analysis-ready rows must be non-abstain, `evidence_supports_label=true`, confidence >= 0.7, non-unclear, and grounded by an exact evidence substring.

## Inputs
- Revalidated labels: `data/processed/phase2_structured_labels_batch_revalidated.parquet`
- Remaining failed rows: `data/processed/phase2_structured_labels_batch_failed_after_revalidation.jsonl`
- Failed diagnostics: `data/processed/phase2_batch_failed_validation_diagnostics.parquet`
- Object graph candidates: `data/processed/object_graph_candidate_mentions.parquet`

## Outputs
- Analysis-ready labels: `data/processed/phase2_batch_analysis_ready_labels.parquet`
- Excluded labels: `data/processed/phase2_batch_excluded_labels.parquet`
- Summary CSV: `data/processed/phase2_batch_analysis_ready_summary.csv`

## Core Metrics
| metric                            | value   |
|:----------------------------------|:--------|
| total_batch_requested_rows        | 306231  |
| total_revalidated_rows            | 237697  |
| analysis_ready_rows               | 229751  |
| excluded_rows                     | 7946    |
| remaining_failed_rows             | 68534   |
| final_effective_success_rate      | 0.7503  |
| duplicate_context_id_count_before | 0       |
| duplicate_context_id_count_after  | 0       |
| evidence_span_not_grounded_after  | 0       |
| stored_object_graph_edges         | 193287  |
| recomputed_object_graph_edges     | 193287  |
| object_graph_edge_count_delta     | 0       |
| pseudo_node_count                 | 0       |
| pseudo_nodes                      |         |

## Evidence Supports Label Before Filtering
| evidence_supports_label   |   rows |
|:--------------------------|-------:|
| true                      | 236127 |
| false                     |   1094 |
| unclear                   |    476 |

## Abstain Before Filtering
| abstain   |   rows |
|:----------|-------:|
| False     | 236099 |
| True      |   1598 |

## Confidence Distribution Before Filtering
| confidence_bin   |   rows |
|:-----------------|-------:|
| [0,0.2]          |    226 |
| (0.2,0.5]        |   1721 |
| (0.5,0.7]        |   6165 |
| (0.7,0.85]       |  54835 |
| (0.85,1.0]       | 174750 |

## Confidence Distribution After Filtering
| confidence_bin   |   rows |
|:-----------------|-------:|
| [0,0.2]          |      0 |
| (0.2,0.5]        |      0 |
| (0.5,0.7]        |    197 |
| (0.7,0.85]       |  54813 |
| (0.85,1.0]       | 174741 |

## Final Intent Before Filtering
| final_intent     |   rows |
|:-----------------|-------:|
| background       | 145978 |
| uses             |  51004 |
| compares_against |  27610 |
| critiques        |   6433 |
| extends          |   4921 |
| applies          |   1152 |
| unclear          |    599 |

## Final Intent After Filtering
| final_intent     |   rows |
|:-----------------|-------:|
| background       | 139823 |
| uses             |  50191 |
| compares_against |  27435 |
| critiques        |   6402 |
| extends          |   4763 |
| applies          |   1137 |

## Final Object Type Before Filtering
| final_object_type     |   rows |
|:----------------------|-------:|
| method                |  73190 |
| model                 |  59225 |
| dataset_or_database   |  30024 |
| metric                |  24797 |
| benchmark_or_protocol |  12788 |
| software_or_tool      |  11234 |
| unknown               |   7880 |
| task                  |   7211 |
| theory_or_concept     |   5787 |
| claim_or_finding      |   5561 |

## Final Object Type After Filtering
| final_object_type     |   rows |
|:----------------------|-------:|
| method                |  70228 |
| model                 |  57377 |
| dataset_or_database   |  29106 |
| metric                |  23903 |
| benchmark_or_protocol |  12355 |
| software_or_tool      |  11045 |
| unknown               |   7668 |
| task                  |   7045 |
| theory_or_concept     |   5622 |
| claim_or_finding      |   5402 |

## Final Relation Subtype Before Filtering
| final_relation_subtype   |   rows |
|:-------------------------|-------:|
| none                     | 142868 |
| direct_use               |  51935 |
| compare_against          |  27386 |
| critique_limitation      |   6433 |
| adapt_to_domain          |   2858 |
| improve                  |   2817 |
| component_use            |   1794 |
| report_metric            |    789 |
| evaluate_on              |    721 |
| combine_with             |     76 |
| replace                  |     20 |

## Final Relation Subtype After Filtering
| final_relation_subtype   |   rows |
|:-------------------------|-------:|
| none                     | 136533 |
| direct_use               |  50971 |
| compare_against          |  27207 |
| critique_limitation      |   6402 |
| adapt_to_domain          |   2802 |
| improve                  |   2704 |
| component_use            |   1643 |
| report_metric            |    711 |
| evaluate_on              |    686 |
| combine_with             |     73 |
| replace                  |     19 |

## Excluded Rows By Reason
| exclusion_reason                |   rows |
|:--------------------------------|-------:|
| low_confidence                  |   6317 |
| evidence_supports_label_false   |   1094 |
| evidence_supports_label_unclear |    476 |
| final_intent_unclear            |     31 |
| abstain_true                    |     28 |

## Remaining Failed Rows By Validator Failure Category
| failed_validator_type            |   rows |
|:---------------------------------|-------:|
| evidence_span_not_substring      |  25311 |
| use_cue_not_accepted             |  20137 |
| quote_not_substring              |  10058 |
| compare_cue_not_accepted         |   4647 |
| extend_cue_not_accepted          |   1946 |
| schema_error                     |   1798 |
| cited_title_only_object_rejected |   1609 |
| other                            |   1286 |
| critique_cue_not_accepted        |   1157 |
| apply_cue_not_accepted           |    584 |
| missing_batch_output             |      1 |

## Final Recommended Downstream Table
`data/processed/phase2_batch_analysis_ready_labels.parquet`
