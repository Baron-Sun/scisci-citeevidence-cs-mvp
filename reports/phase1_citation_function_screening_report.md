# Phase-1 Citation-Function Screening Full Report

Phase-1 is a conservative candidate screening layer, not final citation-function labeling.

## Inputs
- Contexts: `data/processed/analysis_ready_strong_contexts.parquet`
- Object mentions: `data/processed/object_mentions.parquet`
- Object graph candidates: `data/processed/object_graph_candidate_mentions.parquet`
- Cited-title object profiles: `data/processed/cited_title_object_profiles.parquet`
- Seed: `42`

## Outputs
- Candidate rows: `data/processed/phase1_citation_function_candidates.parquet`
- Feature rows: `data/processed/phase1_context_features.parquet`
- High-priority LLM queue: `data/processed/phase1_llm_queue_high.parquet`
- Medium-priority LLM queue: `data/processed/phase1_llm_queue_medium.parquet`
- Stratified LLM sample queue: `data/processed/phase1_llm_queue_sample.parquet`

## Core Counts
| metric                                | value   |
|:--------------------------------------|:--------|
| input_contexts_processed              | 1184634 |
| configured_limit                      | full    |
| contexts_with_object_mentions         | 265779  |
| contexts_with_graph_candidate_objects | 215653  |
| object_mentions_input_rows            | 404228  |
| graph_candidate_input_rows            | 322688  |
| cited_title_profile_input_rows        | 113550  |
| should_send_to_llm_count              | 306231  |
| should_send_to_llm_rate               | 0.259   |
| high_priority_count                   | 34540   |
| medium_priority_count                 | 271691  |
| low_priority_count                    | 431686  |
| none_priority_count                   | 446717  |

## LLM Audit Guidance
| audit_metric                                     |   value |
|:-------------------------------------------------|--------:|
| reviewed_rows                                    | 100     |
| llm_review_precision:applies                     |   0.846 |
| llm_review_precision:background                  |   0.92  |
| llm_review_precision:compares_against            |   0.667 |
| llm_review_precision:critiques                   |   0.833 |
| llm_review_precision:extends                     |   0.917 |
| llm_review_precision:unclear                     |   0.111 |
| llm_review_precision:uses                        |   0.933 |
| recommended_action:keep                          |  50     |
| recommended_action:other                         |  17     |
| recommended_action:fix_evidence_span             |  10     |
| recommended_action:tighten_use_rule              |   8     |
| recommended_action:tighten_compare_rule          |   7     |
| recommended_action:tighten_critique_rule         |   3     |
| recommended_action:adjust_llm_priority           |   2     |
| recommended_action:tighten_extends_rule          |   1     |
| error_type:none                                  |  51     |
| error_type:object_type_wrong                     |  21     |
| error_type:cited_work_description_misread_as_use |   9     |
| error_type:compare_overtriggered                 |   6     |
| error_type:evidence_span_wrong                   |   3     |
| error_type:llm_priority_wrong                    |   2     |
| error_type:other                                 |   2     |
| error_type:critique_overtriggered                |   2     |

## Object Type Source Distribution
| object_type_source     |   contexts |
|:-----------------------|-----------:|
| none                   |     876866 |
| object_graph_candidate |     215653 |
| cited_title_profile    |      41989 |
| generic_metric_feature |      38288 |
| object_mention         |      11838 |

## Primary Intent By Object Type Source
| object_type_source     | primary_candidate_intent   |   contexts |
|:-----------------------|:---------------------------|-----------:|
| none                   | background                 |     560894 |
| none                   | unclear                    |     255708 |
| object_graph_candidate | background                 |     108538 |
| object_graph_candidate | unclear                    |      78330 |
| none                   | uses                       |      33906 |
| cited_title_profile    | background                 |      25982 |
| generic_metric_feature | background                 |      21253 |
| object_graph_candidate | uses                       |      18357 |
| none                   | compares_against           |      17149 |
| generic_metric_feature | unclear                    |      12565 |
| cited_title_profile    | unclear                    |      12555 |
| object_mention         | background                 |       8136 |
| object_graph_candidate | compares_against           |       8009 |
| none                   | critiques                  |       6357 |
| object_mention         | unclear                    |       2819 |
| generic_metric_feature | compares_against           |       2161 |
| cited_title_profile    | uses                       |       2058 |
| generic_metric_feature | uses                       |       1885 |
| none                   | extends                    |       1626 |
| object_graph_candidate | critiques                  |       1426 |
| none                   | applies                    |       1226 |
| cited_title_profile    | compares_against           |        922 |
| object_graph_candidate | applies                    |        543 |
| object_graph_candidate | extends                    |        450 |
| object_mention         | uses                       |        362 |
| object_mention         | compares_against           |        356 |
| generic_metric_feature | critiques                  |        310 |
| cited_title_profile    | critiques                  |        310 |
| object_mention         | critiques                  |        100 |
| cited_title_profile    | extends                    |         93 |
| cited_title_profile    | applies                    |         69 |
| generic_metric_feature | extends                    |         58 |
| generic_metric_feature | applies                    |         56 |
| object_mention         | extends                    |         43 |
| object_mention         | applies                    |         22 |

## Evidence Span Support Sanity Checks
| check                                           |   rows |   rate |
|:------------------------------------------------|-------:|-------:|
| rows_with_evidence_span                         | 579250 |  0.489 |
| evidence_span_exactly_grounded                  | 579250 |  1     |
| evidence_span_missing_or_ungrounded             |      0 |  0     |
| high_current_relation_rows                      |  21479 |  0.018 |
| high_current_relation_has_current_cue           |  21479 |  1     |
| object_type_source_none_has_unknown_object_type | 876866 |  1     |
| generic_metric_feature_not_graph_evidence       |  38288 |  1     |
| cited_title_profile_not_direct_context_evidence |  41989 |  1     |

## Candidate Intent Distribution
| candidate_intent   |   contexts |
|:-------------------|-----------:|
| background         |     749079 |
| unclear            |     361977 |
| uses               |      60007 |
| compares_against   |      28931 |
| critiques          |       8503 |
| extends            |       2272 |
| applies            |       2240 |

## Primary Candidate Intent Distribution
| primary_candidate_intent   |   contexts |
|:---------------------------|-----------:|
| background                 |     724803 |
| unclear                    |     361977 |
| uses                       |      56568 |
| compares_against           |      28597 |
| critiques                  |       8503 |
| extends                    |       2270 |
| applies                    |       1916 |

## Primary Candidate Intent By Normalized Section
| normalized_section   | primary_candidate_intent   |   contexts |
|:---------------------|:---------------------------|-----------:|
| introduction         | background                 |     327409 |
| related_work         | background                 |     269940 |
| unknown              | unclear                    |     206912 |
| unknown              | background                 |      54159 |
| dataset              | unclear                    |      35347 |
| model                | unclear                    |      27067 |
| experiment           | unclear                    |      22973 |
| unknown              | uses                       |      22156 |
| method               | unclear                    |      19373 |
| evaluation           | unclear                    |      16585 |
| background           | background                 |      16360 |
| conclusion           | background                 |      15201 |
| results              | unclear                    |      10907 |
| dataset              | background                 |       9371 |
| dataset              | uses                       |       8160 |
| discussion           | unclear                    |       8086 |
| experiment           | uses                       |       7821 |
| introduction         | compares_against           |       7232 |
| unknown              | compares_against           |       7223 |
| model                | background                 |       7197 |
| experiment           | background                 |       5895 |
| method               | background                 |       5572 |
| analysis             | unclear                    |       5312 |
| evaluation           | background                 |       4922 |
| model                | uses                       |       4119 |
| related_work         | compares_against           |       3915 |
| introduction         | critiques                  |       3776 |
| introduction         | uses                       |       3521 |
| abstract             | unclear                    |       3270 |
| evaluation           | uses                       |       3139 |
| results              | background                 |       2838 |
| method               | uses                       |       2358 |
| discussion           | background                 |       2228 |
| results              | compares_against           |       1971 |
| experiment           | compares_against           |       1968 |
| system_description   | unclear                    |       1843 |
| implementation       | unclear                    |       1835 |
| task_definition      | unclear                    |       1818 |
| unknown              | critiques                  |       1762 |
| related_work         | uses                       |       1523 |
| analysis             | background                 |       1474 |
| related_work         | critiques                  |       1392 |
| model                | compares_against           |       1344 |
| dataset              | compares_against           |       1016 |
| evaluation           | compares_against           |       1011 |
| implementation       | uses                       |       1010 |
| results              | uses                       |        904 |
| method               | compares_against           |        839 |
| unknown              | extends                    |        823 |
| abstract             | background                 |        780 |
| unknown              | applies                    |        777 |
| error_analysis       | unclear                    |        649 |
| conclusion           | compares_against           |        596 |
| system_description   | background                 |        518 |
| introduction         | extends                    |        516 |
| discussion           | compares_against           |        439 |
| task_definition      | background                 |        403 |
| analysis             | uses                       |        394 |
| implementation       | background                 |        353 |
| system_description   | uses                       |        311 |
| background           | uses                       |        298 |
| conclusion           | uses                       |        286 |
| introduction         | applies                    |        283 |
| analysis             | compares_against           |        243 |
| background           | compares_against           |        230 |
| dataset              | critiques                  |        226 |
| abstract             | compares_against           |        217 |
| experiment           | applies                    |        202 |
| evaluation           | critiques                  |        200 |
| task_definition      | uses                       |        193 |
| abstract             | uses                       |        190 |
| system_description   | compares_against           |        189 |
| error_analysis       | background                 |        183 |
| dataset              | applies                    |        172 |
| model                | extends                    |        167 |
| background           | critiques                  |        166 |
| model                | critiques                  |        160 |
| related_work         | extends                    |        153 |
| experiment           | critiques                  |        150 |
| discussion           | uses                       |        148 |
| results              | critiques                  |        136 |
| discussion           | critiques                  |        135 |
| method               | critiques                  |        134 |
| model                | applies                    |        125 |
| method               | extends                    |        113 |
| conclusion           | critiques                  |        109 |
| conclusion           | extends                    |         97 |
| method               | applies                    |         95 |
| dataset              | extends                    |         94 |
| experiment           | extends                    |         90 |
| abstract             | extends                    |         84 |
| implementation       | compares_against           |         83 |
| analysis             | critiques                  |         68 |
| evaluation           | applies                    |         58 |
| evaluation           | extends                    |         57 |
| related_work         | applies                    |         52 |
| error_analysis       | compares_against           |         46 |
| abstract             | critiques                  |         40 |
| error_analysis       | uses                       |         37 |
| task_definition      | compares_against           |         35 |
| conclusion           | applies                    |         33 |
| results              | applies                    |         33 |
| task_definition      | critiques                  |         25 |
| implementation       | applies                    |         22 |
| abstract             | applies                    |         21 |
| analysis             | applies                    |         21 |
| results              | extends                    |         19 |
| analysis             | extends                    |         14 |
| background           | extends                    |         12 |
| system_description   | applies                    |         12 |
| error_analysis       | critiques                  |         11 |
| implementation       | extends                    |         11 |
| system_description   | extends                    |          8 |
| implementation       | critiques                  |          8 |
| task_definition      | extends                    |          5 |
| discussion           | extends                    |          5 |
| system_description   | critiques                  |          5 |
| discussion           | applies                    |          4 |
| background           | applies                    |          3 |
| error_analysis       | extends                    |          2 |
| task_definition      | applies                    |          2 |
| error_analysis       | applies                    |          1 |

## Primary Candidate Intent By LLM Priority
| llm_priority   | primary_candidate_intent   |   contexts |
|:---------------|:---------------------------|-----------:|
| low            | background                 |     420131 |
| none           | unclear                    |     268263 |
| none           | background                 |     175646 |
| medium         | background                 |     129026 |
| medium         | unclear                    |      83533 |
| medium         | uses                       |      34895 |
| high           | uses                       |      18719 |
| medium         | compares_against           |      16603 |
| high           | compares_against           |      11248 |
| low            | unclear                    |      10181 |
| medium         | critiques                  |       6293 |
| high           | applies                    |       1889 |
| high           | critiques                  |       1813 |
| none           | uses                       |       1748 |
| medium         | extends                    |       1314 |
| low            | uses                       |       1206 |
| high           | extends                    |        871 |
| none           | compares_against           |        746 |
| none           | critiques                  |        250 |
| low            | critiques                  |        147 |
| none           | extends                    |         64 |
| medium         | applies                    |         27 |
| low            | extends                    |         21 |

## Candidate Object Type Distribution
| object_type           |   contexts |
|:----------------------|-----------:|
| unknown               |     876866 |
| model                 |     139679 |
| metric                |      70647 |
| dataset_or_database   |      40832 |
| method                |      39285 |
| benchmark_or_protocol |      23716 |
| software_or_tool      |      14992 |

## Primary Candidate Object Type Distribution
| primary_candidate_object_type   |   contexts |
|:--------------------------------|-----------:|
| unknown                         |     876866 |
| model                           |     134297 |
| metric                          |      68706 |
| dataset_or_database             |      37842 |
| method                          |      32695 |
| benchmark_or_protocol           |      20774 |
| software_or_tool                |      13454 |

## Object Type Confidence Distribution
| object_type_confidence_bin   |   contexts |
|:-----------------------------|-----------:|
| 0                            |     876866 |
| (0,0.5]                      |      41989 |
| (0.5,0.8]                    |      50126 |
| (0.8,0.95]                   |     215653 |
| (0.95,1.0]                   |          0 |

## Relation Subtype Distribution
| relation_subtype    |   contexts |
|:--------------------|-----------:|
| none                |    1085761 |
| direct_use          |      59285 |
| compare_against     |      28931 |
| critique_limitation |       8503 |
| report_metric       |       4290 |
| adapt_to_domain     |       2405 |
| improve             |       1199 |
| evaluate_on         |        376 |
| component_use       |        366 |

## Phase2 Candidate Type Distribution
| phase2_candidate_type           |   contexts |
|:--------------------------------|-----------:|
| background_prior                |     483078 |
| no_cue                          |     221732 |
| cited_work_description          |     169293 |
| weak_cue_feature                |     128247 |
| explicit_current_paper_relation |      93824 |
| object_only_unclear             |      57641 |
| generic_metric_feature          |      26789 |
| ambiguous_multi_intent          |       4030 |

## LLM Priority Distribution
| llm_priority   |   contexts |
|:---------------|-----------:|
| none           |     446717 |
| low            |     431686 |
| medium         |     271691 |
| high           |      34540 |

## LLM Queue Stats
| queue   |   rows |
|:--------|-------:|
| high    |  34540 |
| medium  | 271691 |
| sample  |    600 |

## High Queue By Primary Candidate Intent
| primary_candidate_intent   |   contexts |
|:---------------------------|-----------:|
| uses                       |      18719 |
| compares_against           |      11248 |
| applies                    |       1889 |
| critiques                  |       1813 |
| extends                    |        871 |

## Medium Queue By Primary Candidate Intent
| primary_candidate_intent   |   contexts |
|:---------------------------|-----------:|
| background                 |     129026 |
| unclear                    |      83533 |
| uses                       |      34895 |
| compares_against           |      16603 |
| critiques                  |       6293 |
| extends                    |       1314 |
| applies                    |         27 |

## High Queue By Normalized Section
| normalized_section   |   contexts |
|:---------------------|-----------:|
| unknown              |      10977 |
| experiment           |       4694 |
| introduction         |       4523 |
| dataset              |       2765 |
| model                |       2719 |
| related_work         |       2038 |
| evaluation           |       1994 |
| results              |       1440 |
| method               |       1163 |
| implementation       |        684 |
| conclusion           |        366 |
| system_description   |        268 |
| discussion           |        223 |
| analysis             |        217 |
| background           |        196 |
| abstract             |        188 |
| task_definition      |         68 |
| error_analysis       |         17 |

## Medium Queue By Normalized Section
| normalized_section   |   contexts |
|:---------------------|-----------:|
| unknown              |      72421 |
| introduction         |      62871 |
| related_work         |      51632 |
| experiment           |      16179 |
| dataset              |      15566 |
| model                |      13700 |
| evaluation           |       9744 |
| method               |       7950 |
| results              |       6220 |
| conclusion           |       3424 |
| background           |       3287 |
| discussion           |       2324 |
| analysis             |       1868 |
| abstract             |       1397 |
| implementation       |       1257 |
| system_description   |       1083 |
| task_definition      |        526 |
| error_analysis       |        242 |

## High Queue Top Object Names
| object_name         |   contexts |
|:--------------------|-----------:|
| BERT                |       5360 |
| BLEU                |       4097 |
| LSTM                |       3449 |
| Transformer         |       3141 |
| accuracy            |       2646 |
| GloVe               |       2169 |
| seq2seq             |       1875 |
| Moses               |       1699 |
| F1                  |       1695 |
| CRF                 |       1668 |
| ROUGE               |       1511 |
| Penn Treebank       |       1179 |
| WordNet             |       1170 |
| SemEval             |       1046 |
| GIZA++              |       1017 |
| METEOR              |        988 |
| word2vec            |        959 |
| attention mechanism |        910 |
| WMT                 |        850 |
| ELMo                |        789 |
| SQuAD               |        774 |
| HMM                 |        615 |
| Stanford CoreNLP    |        524 |
| OntoNotes           |        458 |
| GLUE                |        426 |
| SNLI                |        405 |
| perplexity          |        295 |
| OPUS                |        271 |
| NLTK                |        270 |
| PropBank            |        240 |
| CoNLL-2003          |        229 |
| FrameNet            |        212 |
| spaCy               |        179 |
| MultiNLI            |        146 |
| CoNLL-2012          |        143 |
| SuperGLUE           |         27 |

## Medium Queue Top Object Names
| object_name         |   contexts |
|:--------------------|-----------:|
| BERT                |      32984 |
| LSTM                |      22726 |
| Transformer         |      21510 |
| accuracy            |      19282 |
| BLEU                |      19204 |
| seq2seq             |      15947 |
| CRF                 |      15013 |
| WordNet             |      14850 |
| attention mechanism |      10356 |
| SemEval             |       9605 |
| GloVe               |       7282 |
| F1                  |       7190 |
| HMM                 |       7140 |
| Penn Treebank       |       7065 |
| ROUGE               |       6555 |
| word2vec            |       6025 |
| ELMo                |       5321 |
| Moses               |       4682 |
| FrameNet            |       4460 |
| METEOR              |       4237 |
| SQuAD               |       3955 |
| WMT                 |       3943 |
| GIZA++              |       3685 |
| PropBank            |       3540 |
| SNLI                |       2915 |
| OntoNotes           |       2345 |
| GLUE                |       2063 |
| perplexity          |       1850 |
| Stanford CoreNLP    |       1446 |
| CoNLL-2003          |       1033 |
| MultiNLI            |        985 |
| NLTK                |        839 |
| OPUS                |        836 |
| CoNLL-2012          |        650 |
| spaCy               |        549 |
| SuperGLUE           |        405 |

## Matched Cue Counts By Group
| cue_group   |   contexts |
|:------------|-----------:|
| use         |     224277 |
| compare     |      28931 |
| extend      |      98417 |
| critique    |       8503 |
| apply       |      36258 |
| background  |     253695 |
| evaluation  |     160583 |

## Candidate Intent By Normalized Section
| normalized_section   | candidate_intent   |   contexts |
|:---------------------|:-------------------|-----------:|
| introduction         | background         |     330775 |
| related_work         | background         |     271883 |
| unknown              | unclear            |     206912 |
| unknown              | background         |      62202 |
| dataset              | unclear            |      35347 |
| model                | unclear            |      27067 |
| unknown              | uses               |      23483 |
| experiment           | unclear            |      22973 |
| method               | unclear            |      19373 |
| evaluation           | unclear            |      16585 |
| background           | background         |      16489 |
| conclusion           | background         |      15502 |
| dataset              | background         |      11951 |
| results              | unclear            |      10907 |
| model                | background         |       8652 |
| experiment           | background         |       8437 |
| dataset              | uses               |       8414 |
| experiment           | uses               |       8238 |
| discussion           | unclear            |       8086 |
| introduction         | compares_against   |       7364 |
| unknown              | compares_against   |       7290 |
| method               | background         |       6564 |
| evaluation           | background         |       6166 |
| analysis             | unclear            |       5312 |
| model                | uses               |       4372 |
| introduction         | uses               |       3960 |
| related_work         | compares_against   |       3940 |
| introduction         | critiques          |       3776 |
| results              | background         |       3574 |
| evaluation           | uses               |       3272 |
| abstract             | unclear            |       3270 |
| method               | uses               |       2508 |
| discussion           | background         |       2457 |
| results              | compares_against   |       1988 |
| experiment           | compares_against   |       1983 |
| system_description   | unclear            |       1843 |
| implementation       | unclear            |       1835 |
| task_definition      | unclear            |       1818 |
| unknown              | critiques          |       1762 |
| related_work         | uses               |       1674 |
| analysis             | background         |       1663 |
| related_work         | critiques          |       1392 |
| model                | compares_against   |       1352 |
| implementation       | uses               |       1058 |
| evaluation           | compares_against   |       1027 |
| dataset              | compares_against   |       1026 |
| results              | uses               |       1002 |
| abstract             | background         |        902 |
| unknown              | applies            |        892 |
| method               | compares_against   |        855 |
| unknown              | extends            |        823 |
| system_description   | background         |        663 |
| error_analysis       | unclear            |        649 |
| conclusion           | compares_against   |        607 |
| implementation       | background         |        539 |
| introduction         | extends            |        517 |
| task_definition      | background         |        457 |
| discussion           | compares_against   |        445 |
| analysis             | uses               |        422 |
| introduction         | applies            |        353 |
| system_description   | uses               |        350 |
| conclusion           | uses               |        336 |
| background           | uses               |        306 |
| analysis             | compares_against   |        243 |
| background           | compares_against   |        235 |
| dataset              | critiques          |        226 |
| experiment           | applies            |        224 |
| abstract             | compares_against   |        222 |
| abstract             | uses               |        217 |
| error_analysis       | background         |        203 |
| evaluation           | critiques          |        200 |
| task_definition      | uses               |        198 |
| dataset              | applies            |        196 |
| system_description   | compares_against   |        189 |
| model                | extends            |        168 |
| background           | critiques          |        166 |
| model                | critiques          |        160 |
| discussion           | uses               |        159 |
| model                | applies            |        153 |
| related_work         | extends            |        153 |
| experiment           | critiques          |        150 |
| results              | critiques          |        136 |
| discussion           | critiques          |        135 |
| method               | critiques          |        134 |
| method               | extends            |        113 |
| method               | applies            |        111 |
| conclusion           | critiques          |        109 |
| conclusion           | extends            |         97 |
| dataset              | extends            |         94 |
| experiment           | extends            |         90 |
| abstract             | extends            |         84 |
| implementation       | compares_against   |         83 |
| related_work         | applies            |         73 |
| analysis             | critiques          |         68 |
| evaluation           | applies            |         63 |
| evaluation           | extends            |         57 |
| error_analysis       | compares_against   |         47 |
| conclusion           | applies            |         40 |
| abstract             | critiques          |         40 |
| error_analysis       | uses               |         38 |
| results              | applies            |         36 |
| task_definition      | compares_against   |         35 |
| abstract             | applies            |         28 |
| task_definition      | critiques          |         25 |
| analysis             | applies            |         24 |
| implementation       | applies            |         23 |
| results              | extends            |         19 |
| analysis             | extends            |         14 |
| system_description   | applies            |         13 |
| background           | extends            |         12 |
| error_analysis       | critiques          |         11 |
| implementation       | extends            |         11 |
| implementation       | critiques          |          8 |
| system_description   | extends            |          8 |
| system_description   | critiques          |          5 |
| discussion           | extends            |          5 |
| task_definition      | extends            |          5 |
| discussion           | applies            |          4 |
| task_definition      | applies            |          3 |
| background           | applies            |          3 |
| error_analysis       | extends            |          2 |
| error_analysis       | applies            |          1 |

## Candidate Intent By Object Type
| candidate_intent   | object_type           |   contexts |
|:-------------------|:----------------------|-----------:|
| background         | unknown               |     576668 |
| unclear            | unknown               |     255708 |
| background         | model                 |      80148 |
| unclear            | model                 |      46119 |
| background         | metric                |      36777 |
| uses               | unknown               |      35982 |
| unclear            | metric                |      26620 |
| background         | method                |      25654 |
| background         | dataset_or_database   |      23427 |
| compares_against   | unknown               |      17384 |
| unclear            | dataset_or_database   |      14078 |
| background         | benchmark_or_protocol |      13120 |
| unclear            | method                |      11021 |
| uses               | model                 |      10455 |
| unclear            | benchmark_or_protocol |       8292 |
| unclear            | software_or_tool      |       8032 |
| critiques          | unknown               |       6357 |
| uses               | metric                |       5479 |
| compares_against   | model                 |       5427 |
| background         | software_or_tool      |       4124 |
| compares_against   | metric                |       3763 |
| uses               | software_or_tool      |       3114 |
| uses               | dataset_or_database   |       3110 |
| uses               | benchmark_or_protocol |       2166 |
| uses               | method                |       2071 |
| extends            | unknown               |       1627 |
| applies            | unknown               |       1449 |
| compares_against   | method                |       1295 |
| critiques          | model                 |        906 |
| compares_against   | dataset_or_database   |        903 |
| compares_against   | benchmark_or_protocol |        770 |
| critiques          | metric                |        710 |
| compares_against   | software_or_tool      |        575 |
| applies            | model                 |        388 |
| extends            | model                 |        352 |
| critiques          | dataset_or_database   |        269 |
| critiques          | method                |        227 |
| applies            | metric                |        135 |
| extends            | metric                |        114 |
| applies            | dataset_or_database   |        113 |
| extends            | method                |        100 |
| applies            | software_or_tool      |         98 |
| applies            | method                |         79 |
| critiques          | benchmark_or_protocol |         66 |
| applies            | benchmark_or_protocol |         51 |
| extends            | benchmark_or_protocol |         50 |
| critiques          | software_or_tool      |         48 |
| extends            | dataset_or_database   |         47 |
| extends            | software_or_tool      |         29 |

## Top Object Names By Candidate Intent
| candidate_intent   | object_name         |   contexts |
|:-------------------|:--------------------|-----------:|
| background         | accuracy            |      22234 |
| background         | BERT                |      18882 |
| background         | seq2seq             |      15672 |
| background         | Transformer         |      15528 |
| unclear            | BERT                |      14984 |
| background         | LSTM                |      14470 |
| unclear            | accuracy            |      11168 |
| background         | CRF                 |      10927 |
| unclear            | BLEU                |      10454 |
| background         | WordNet             |      10259 |
| background         | BLEU                |       9786 |
| unclear            | LSTM                |       9167 |
| unclear            | Transformer         |       8473 |
| background         | attention mechanism |       7613 |
| background         | SemEval             |       6793 |
| unclear            | F1                  |       5944 |
| background         | F1                  |       5249 |
| unclear            | seq2seq             |       5200 |
| background         | HMM                 |       5076 |
| unclear            | WordNet             |       4902 |
| unclear            | CRF                 |       4572 |
| background         | Penn Treebank       |       4485 |
| unclear            | GloVe               |       4437 |
| background         | ROUGE               |       3661 |
| background         | word2vec            |       3626 |
| unclear            | Moses               |       3388 |
| uses               | BERT                |       3338 |
| unclear            | ROUGE               |       3255 |
| background         | FrameNet            |       3186 |
| background         | ELMo                |       3128 |
| background         | GloVe               |       3118 |
| unclear            | SemEval             |       3088 |
| unclear            | Penn Treebank       |       3064 |
| unclear            | attention mechanism |       2961 |
| uses               | BLEU                |       2636 |
| unclear            | word2vec            |       2599 |
| background         | METEOR              |       2474 |
| unclear            | GIZA++              |       2388 |
| background         | PropBank            |       2371 |
| unclear            | ELMo                |       2359 |
| unclear            | HMM                 |       2264 |
| background         | SQuAD               |       2181 |
| background         | WMT                 |       2174 |
| unclear            | METEOR              |       2099 |
| compares_against   | accuracy            |       2025 |
| uses               | Transformer         |       1968 |
| uses               | LSTM                |       1963 |
| unclear            | WMT                 |       1957 |
| unclear            | SQuAD               |       1867 |
| compares_against   | BERT                |       1861 |
| uses               | GloVe               |       1811 |
| uses               | accuracy            |       1784 |
| background         | GIZA++              |       1664 |
| background         | Moses               |       1645 |
| unclear            | SNLI                |       1542 |
| background         | perplexity          |       1526 |
| background         | SNLI                |       1432 |
| background         | OntoNotes           |       1410 |
| uses               | Moses               |       1397 |
| compares_against   | LSTM                |       1365 |
| unclear            | perplexity          |       1335 |
| unclear            | FrameNet            |       1315 |
| uses               | F1                  |       1279 |
| unclear            | PropBank            |       1240 |
| compares_against   | BLEU                |       1211 |
| unclear            | Stanford CoreNLP    |       1174 |
| compares_against   | F1                  |       1154 |
| background         | GLUE                |       1123 |
| uses               | ROUGE               |       1050 |
| unclear            | GLUE                |       1042 |
| unclear            | OntoNotes           |       1025 |
| compares_against   | Transformer         |       1005 |
| uses               | CRF                 |        998 |
| uses               | Penn Treebank       |        954 |
| uses               | seq2seq             |        890 |
| compares_against   | seq2seq             |        827 |
| uses               | GIZA++              |        798 |
| uses               | WordNet             |        733 |
| uses               | SemEval             |        727 |
| uses               | word2vec            |        696 |
| uses               | METEOR              |        679 |
| background         | CoNLL-2003          |        657 |
| unclear            | NLTK                |        642 |
| unclear            | OPUS                |        638 |
| uses               | WMT                 |        617 |
| compares_against   | CRF                 |        598 |
| uses               | SQuAD               |        549 |
| unclear            | MultiNLI            |        537 |
| uses               | Stanford CoreNLP    |        498 |
| uses               | ELMo                |        491 |
| background         | MultiNLI            |        469 |
| background         | CoNLL-2012          |        457 |
| uses               | attention mechanism |        446 |
| unclear            | CoNLL-2003          |        443 |
| compares_against   | GloVe               |        364 |
| compares_against   | attention mechanism |        363 |
| uses               | HMM                 |        352 |
| uses               | OntoNotes           |        345 |
| unclear            | spaCy               |        344 |
| compares_against   | Moses               |        332 |

## Generic Metric Contexts By Candidate Intent
| candidate_intent   |   contexts |
|:-------------------|-----------:|
| background         |      28040 |
| unclear            |      17477 |
| compares_against   |       3189 |
| uses               |       3074 |
| critiques          |        413 |
| applies            |         98 |
| extends            |         77 |

## Example Uses
| context_id                | normalized_section   | primary_candidate_intent   | phase2_candidate_type           | candidate_intents   | candidate_relation_subtypes   |   confidence | llm_priority   | llm_reason                                   | should_send_to_llm   | cited_work_description   | object_type_source     | primary_candidate_object_type   | object_names    | generic_metric_names   | evidence_span   | matched_rules                                                                            | sentence_text                                                                                                                                                                        |
|:--------------------------|:---------------------|:---------------------------|:--------------------------------|:--------------------|:------------------------------|-------------:|:---------------|:---------------------------------------------|:---------------------|:-------------------------|:-----------------------|:--------------------------------|:----------------|:-----------------------|:----------------|:-----------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ctxr_794ff11af106441610a2 | model                | uses                       | explicit_current_paper_relation | uses                | direct_use                    |         0.9  | high           | explicit_current_relation_with_strong_object | True                 | False                    | object_graph_candidate | metric                          | perplexity;BLEU | perplexity             | we use          | weak_extend_context_feature;current_paper_use_cue;generic_metric_feature_only            | Since the space of different combinations is too large to be searched exhaustively, we use a guided search procedure based on Genetic Algorithms (Duh and Kirchhoff, 2004) , whic... |
| ctxr_caa50477f333d1e3c48b | dataset              | uses                       | explicit_current_paper_relation | uses                | direct_use                    |         0.9  | high           | explicit_current_relation_with_strong_object | True                 | False                    | object_graph_candidate | dataset_or_database             | Penn Treebank   |                        | we use          | current_paper_use_cue;dataset_context_feature                                            | For our experiments, we use two main resources, the Wall Street Journal (WSJ) portion of the Penn Treebank (PTB) (Marcus et al., 1993) and the English Web Treebank (EWT) (Bies e... |
| ctxr_a7ac70660d93318c89cc | unknown              | uses                       | explicit_current_paper_relation | uses                | direct_use                    |         0.62 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                 |                        | We use          | current_paper_use_cue                                                                    | We use TnT (Brants, 2000) , a Markov model POS tagger using a trigram model.                                                                                                         |
| ctxr_f7c720ac514891b21f33 | unknown              | uses                       | explicit_current_paper_relation | uses                | direct_use                    |         0.62 | low            | generic_metric_feature_only                  | False                | False                    | generic_metric_feature | metric                          | accuracy        | accuracy               | We use          | current_paper_use_cue;generic_metric_feature_only                                        | We use MSTParser (McDonald and Pereira, 2006) , 2 a freely-available parser that reaches stateof-the-art accuracy in dependency parsing for English.                                 |
| ctxr_1e11c4efff7667aaac0f | unknown              | uses                       | explicit_current_paper_relation | background;uses     | direct_use                    |         0.62 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                 |                        | we use          | background_cue;current_paper_use_cue;dataset_context_feature                             | In our previous work (Khan et al., 2013) , we showed that we obtain the best results when we use a balanced training corpus with the same number of sentences from the EWT and th... |
| ctxr_2a01ec9e66ff7695b86c | unknown              | uses                       | explicit_current_paper_relation | uses                | direct_use                    |         0.62 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                 |                        | we follow       | current_paper_use_cue                                                                    | In constructing the semantic space we follow the procedure outlined in Vecchi et al. (2011) .                                                                                        |
| ctxr_4d915798d0f58abecb43 | method               | uses                       | explicit_current_paper_relation | background;uses     | direct_use                    |         0.62 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                 |                        | we used         | background_cue;weak_extend_context_feature;current_paper_use_cue;dataset_context_feature | For the Hansard corpus used to supplement our French-English resources (described in section 3 below), we used our own alignment based on Moore's algorithm (Moore, 2002) , segme... |
| ctxr_67cec04d10f6043867bf | method               | uses                       | explicit_current_paper_relation | uses                | direct_use                    |         0.62 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                 |                        | we use          | current_paper_use_cue                                                                    | In this regard, we use a method similar to Lin and Hovy (2000) to identify signature terms and subsequently use them 2 http://ir.ohsu.edu/genomics/ to discard sentences that con... |
| ctxr_d10c27e8df9fea13044e | introduction         | uses                       | explicit_current_paper_relation | uses                | direct_use                    |         0.62 | low            | generic_metric_feature_only                  | False                | False                    | generic_metric_feature | metric                          | F1              | F1                     | we use          | current_paper_use_cue;generic_metric_feature_only                                        | In this paper, we use the Maximum Entropy (MaxEnt) framework (Berger et al., 1996) to automatically predict the correctness of KBP SF intermediate responses (Section 4).            |
| ctxr_a7a32c62150dc08cd73f | unknown              | uses                       | explicit_current_paper_relation | background;uses     | direct_use                    |         0.9  | high           | explicit_current_relation_with_strong_object | True                 | True                     | object_graph_candidate | software_or_tool                | GIZA++          |                        | We used         | cited_work_description;current_paper_use_cue                                             | We used the word alignment produced by Giza (Och and Ney, 2000) out of an IBM model 2.                                                                                               |
| ctxr_b05afaa70827ae54fae7 | system_description   | uses                       | explicit_current_paper_relation | background;uses     | direct_use                    |         0.9  | high           | explicit_current_relation_with_strong_object | True                 | True                     | object_graph_candidate | software_or_tool                | GIZA++          |                        | We used         | cited_work_description;current_paper_use_cue                                             | We used a multi-threaded version of the GIZA++ tool (Gao and Vogel, 2008) .                                                                                                          |
| ctxr_29c335e2fd7d84765c11 | conclusion           | uses                       | explicit_current_paper_relation | background;uses     | direct_use                    |         0.62 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                 |                        | we use          | background_cue;current_paper_use_cue                                                     | It is interesting to compare our approach to self-learning as proposed in (Ueffing, 2006) Selflearning was applied to small amounts of test data only while we use several hundre... |
| ctxr_cb70f1051a86fda2b96e | unknown              | uses                       | explicit_current_paper_relation | uses                | direct_use                    |         0.62 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                 |                        | we use          | current_paper_use_cue                                                                    | As for a dictionary, we use the Lexeed database (Fujita et al., 2006) , which consists of more than 20,000 verbs with explanations of word sense and example sentences.              |
| ctxr_ae1fdaa8e140e1f7ab56 | unknown              | uses                       | explicit_current_paper_relation | background;uses     | direct_use                    |         0.62 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                 |                        | We employed     | cited_work_description;current_paper_use_cue;dataset_context_feature                     | We employed the four domains datasets used in Blitzer et al. (2007) to train and test the all-in one and the ensemble classifiers.                                                   |
| ctxr_de3dbd5f86a182402ba0 | evaluation           | uses                       | explicit_current_paper_relation | background;uses     | direct_use                    |         0.9  | high           | explicit_current_relation_with_strong_object | True                 | True                     | object_graph_candidate | metric                          | BLEU;accuracy   | accuracy               | we used         | cited_work_description;current_paper_use_cue;generic_metric_feature_only                 | For the automatic evaluation, we used the criteria from the IWSLT evaluation campaign (Akiba et al., 2004) , namely word error rate (WER), positionindependent word error rate (P... |
| ctxr_578992fe86888ec95c7e | evaluation           | uses                       | explicit_current_paper_relation | background;uses     | direct_use                    |         0.9  | high           | explicit_current_relation_with_strong_object | True                 | True                     | object_graph_candidate | metric                          | BLEU;accuracy   | accuracy               | we used         | cited_work_description;current_paper_use_cue;generic_metric_feature_only                 | For the automatic evaluation, we used the criteria from the IWSLT evaluation campaign (Akiba et al., 2004) , namely word error rate (WER), positionindependent word error rate (P... |
| ctxr_55dc3c17d39b66939b1a | evaluation           | uses                       | explicit_current_paper_relation | background;uses     | direct_use                    |         0.9  | high           | explicit_current_relation_with_strong_object | True                 | True                     | object_graph_candidate | metric                          | BLEU;accuracy   | accuracy               | we used         | cited_work_description;current_paper_use_cue;generic_metric_feature_only                 | For the automatic evaluation, we used the criteria from the IWSLT evaluation campaign (Akiba et al., 2004) , namely word error rate (WER), positionindependent word error rate (P... |
| ctxr_e7f73b840ee08776841c | evaluation           | uses                       | explicit_current_paper_relation | uses                | direct_use                    |         0.62 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                 |                        | we used         | current_paper_use_cue;dataset_context_feature                                            | In the evaluation we used the KPWr corpus (Broda et al., 2012) 5 , which is the only available corpus annotated with semantic relations between proper names for Polish.             |
| ctxr_81a1469fbea3021f2b62 | unknown              | uses                       | explicit_current_paper_relation | background;uses     | direct_use                    |         0.62 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                 |                        | We used         | cited_work_description;current_paper_use_cue                                             | A sahen-noun is a verbal noun in Japanese, which acts as a verb in the form of "sahen-noun + suru".5 We used the statistical Japanese dependency parser CaboCha(Kudo and Matsumot... |
| ctxr_f57fd4886e69d192fe52 | unknown              | uses                       | explicit_current_paper_relation | background;uses     | direct_use                    |         0.62 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                 |                        | We use          | cited_work_description;background_cue;current_paper_use_cue                              | We use a phrase-based translation approach as described in (Zens and Ney, 2004) .                                                                                                    |

## Example Compares Against
| context_id                | normalized_section   | primary_candidate_intent   | phase2_candidate_type           | candidate_intents           | candidate_relation_subtypes   |   confidence | llm_priority   | llm_reason                                   | should_send_to_llm   | cited_work_description   | object_type_source     | primary_candidate_object_type   | object_names   | generic_metric_names   | evidence_span   | matched_rules                                    | sentence_text                                                                                                                                                                        |
|:--------------------------|:---------------------|:---------------------------|:--------------------------------|:----------------------------|:------------------------------|-------------:|:---------------|:---------------------------------------------|:---------------------|:-------------------------|:-----------------------|:--------------------------------|:---------------|:-----------------------|:----------------|:-------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ctxr_5d4459ab2a2de3c5c83b | evaluation           | compares_against           | explicit_current_paper_relation | compares_against            | compare_against               |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | compared to     | explicit_compare_cue                             | Despite of its performance, LIHLA has some advantages when compared to other lexical alignment methods found in the literature, such as: it does not need to be trained for a new... |
| ctxr_cda6ba0e4cd02c1152fb | unknown              | compares_against           | explicit_current_paper_relation | compares_against            | compare_against               |         0.85 | high           | explicit_current_relation_with_strong_object | True                 | False                    | object_graph_candidate | metric                          | BLEU           |                        | compared to     | weak_extend_context_feature;explicit_compare_cue | Once this is accomplished, a variant of Powell's algorithm is used to find weights that optimize BLEU score (Papineni et al, 2002) over these hypotheses, compared to reference t... |
| ctxr_a7a35b2c49d3022a8e23 | unknown              | compares_against           | explicit_current_paper_relation | compares_against            | compare_against               |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | better than     | explicit_compare_cue                             | Table 8 shows that except for "pairing" by Jaccard in computer science, our method is consistently better than Sato et al. (2013) in terms of precision as well.                     |
| ctxr_12de4c93a55ba6a754de | background           | compares_against           | explicit_current_paper_relation | compares_against            | compare_against               |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | better than     | explicit_compare_cue                             | The increasing availability of MT engines and the need for better quality has motivated considerable efforts to combine multiple engines into one "super-engine" that is hopefull... |
| ctxr_c959197a3d98bb457e27 | background           | compares_against           | explicit_current_paper_relation | compares_against            | compare_against               |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | better than     | explicit_compare_cue                             | But also the more challenging problem of decomposing the candidates and re-assembling from the pieces a new sentence, hopefully better than any of the given inputs, has recently... |
| ctxr_5b3aece616f48617bdd8 | background           | compares_against           | explicit_current_paper_relation | compares_against            | compare_against               |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | better than     | explicit_compare_cue                             | But also the more challenging problem of decomposing the candidates and re-assembling from the pieces a new sentence, hopefully better than any of the given inputs, has recently... |
| ctxr_4f5451576fa932cbe38d | background           | compares_against           | explicit_current_paper_relation | compares_against            | compare_against               |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | better than     | explicit_compare_cue                             | But also the more challenging problem of decomposing the candidates and re-assembling from the pieces a new sentence, hopefully better than any of the given inputs, has recently... |
| ctxr_cee26ca2d82add04305a | background           | compares_against           | explicit_current_paper_relation | compares_against            | compare_against               |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | better than     | explicit_compare_cue                             | But also the more challenging problem of decomposing the candidates and re-assembling from the pieces a new sentence, hopefully better than any of the given inputs, has recently... |
| ctxr_8bb065d8ebe7021cee39 | background           | compares_against           | explicit_current_paper_relation | compares_against            | compare_against               |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | better than     | explicit_compare_cue                             | But also the more challenging problem of decomposing the candidates and re-assembling from the pieces a new sentence, hopefully better than any of the given inputs, has recently... |
| ctxr_ca1f78fd1f05bd0e85fa | background           | compares_against           | explicit_current_paper_relation | compares_against            | compare_against               |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | better than     | explicit_compare_cue                             | But also the more challenging problem of decomposing the candidates and re-assembling from the pieces a new sentence, hopefully better than any of the given inputs, has recently... |
| ctxr_d5a37314794986e68d19 | background           | compares_against           | explicit_current_paper_relation | compares_against            | compare_against               |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | better than     | explicit_compare_cue                             | But also the more challenging problem of decomposing the candidates and re-assembling from the pieces a new sentence, hopefully better than any of the given inputs, has recently... |
| ctxr_81cc73c5cb625e99f478 | background           | compares_against           | explicit_current_paper_relation | compares_against            | compare_against               |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | better than     | explicit_compare_cue                             | But also the more challenging problem of decomposing the candidates and re-assembling from the pieces a new sentence, hopefully better than any of the given inputs, has recently... |
| ctxr_ce7b7c2abc63d8e7c2b0 | introduction         | compares_against           | explicit_current_paper_relation | background;compares_against | compare_against               |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                |                        | outperform      | cited_work_description;explicit_compare_cue      | In recent years, various phrase translation approaches (Marcu and Wong, 2002; Och et al., 1999; Koehn et al., 2003) have been shown to outperform word-to-word translation models... |
| ctxr_cb993c72289862a3e0a8 | introduction         | compares_against           | explicit_current_paper_relation | background;compares_against | compare_against               |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                |                        | outperform      | cited_work_description;explicit_compare_cue      | In recent years, various phrase translation approaches (Marcu and Wong, 2002; Och et al., 1999; Koehn et al., 2003) have been shown to outperform word-to-word translation models... |
| ctxr_acbc70964be0994952f5 | introduction         | compares_against           | explicit_current_paper_relation | background;compares_against | compare_against               |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                |                        | outperform      | cited_work_description;explicit_compare_cue      | In recent years, various phrase translation approaches (Marcu and Wong, 2002; Och et al., 1999; Koehn et al., 2003) have been shown to outperform word-to-word translation models... |
| ctxr_284e5e42bf08296ed11a | introduction         | compares_against           | explicit_current_paper_relation | background;compares_against | compare_against               |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                |                        | outperform      | cited_work_description;explicit_compare_cue      | In recent years, various phrase translation approaches (Marcu and Wong, 2002; Och et al., 1999; Koehn et al., 2003) have been shown to outperform word-to-word translation models... |
| ctxr_065af744384b98cb9518 | introduction         | compares_against           | explicit_current_paper_relation | background;compares_against | compare_against               |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                |                        | outperform      | cited_work_description;explicit_compare_cue      | In recent years, various phrase translation approaches (Marcu and Wong, 2002; Och et al., 1999; Koehn et al., 2003) have been shown to outperform word-to-word translation models... |
| ctxr_cf9c160ab659a50ec679 | introduction         | compares_against           | explicit_current_paper_relation | background;compares_against | compare_against               |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                |                        | outperform      | cited_work_description;explicit_compare_cue      | In recent years, various phrase translation approaches (Marcu and Wong, 2002; Och et al., 1999; Koehn et al., 2003) have been shown to outperform word-to-word translation models... |
| ctxr_9bb4afe1307875e6671b | introduction         | compares_against           | explicit_current_paper_relation | background;compares_against | compare_against               |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                |                        | outperform      | cited_work_description;explicit_compare_cue      | In recent years, various phrase translation approaches (Marcu and Wong, 2002; Och et al., 1999; Koehn et al., 2003) have been shown to outperform word-to-word translation models... |
| ctxr_7da556905b4b181daeb2 | introduction         | compares_against           | explicit_current_paper_relation | background;compares_against | compare_against               |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                |                        | outperform      | cited_work_description;explicit_compare_cue      | In recent years, various phrase translation approaches (Marcu and Wong, 2002; Och et al., 1999; Koehn et al., 2003) have been shown to outperform word-to-word translation models... |

## Example Extends
| context_id                | normalized_section   | primary_candidate_intent   | phase2_candidate_type           | candidate_intents        | candidate_relation_subtypes                   |   confidence | llm_priority   | llm_reason                                   | should_send_to_llm   | cited_work_description   | object_type_source     | primary_candidate_object_type   | object_names   | generic_metric_names   | evidence_span     | matched_rules                                                                                                   | sentence_text                                                                                                                                                                        |
|:--------------------------|:---------------------|:---------------------------|:--------------------------------|:-------------------------|:----------------------------------------------|-------------:|:---------------|:---------------------------------------------|:---------------------|:-------------------------|:-----------------------|:--------------------------------|:---------------|:-----------------------|:------------------|:----------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ctxr_6cb4fa73da2bed944cf5 | unknown              | extends                    | explicit_current_paper_relation | extends                  | improve                                       |         0.62 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | We extended       | current_paper_extend_cue                                                                                        | We extended the monotone search algorithm from (Zens and Ney, 2004) such that reorderings are possible.                                                                              |
| ctxr_4b0ca5a7044fff28520d | related_work         | extends                    | explicit_current_paper_relation | extends                  | improve                                       |         0.62 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | we improve        | current_paper_extend_cue                                                                                        | In (Litvak et al., 2010) we improve the summarization quality by identifying the best linear combination of the metrics evaluated in this paper.                                     |
| ctxr_dc841951bb85c039a52e | unknown              | extends                    | ambiguous_multi_intent          | extends;applies          | adapt_to_domain                               |         0.62 | high           | multiple_strong_non_background_cues          | True                 | False                    | none                   | unknown                         |                |                        | we adapt          | current_paper_extend_cue;current_paper_apply_cue;weak_use_context_feature                                       | Following Sagae and Tsujii (2007) and (Chen et al., 2008) , we adapt the approach to the task of parsing by retraining with agreed upon parses from only a part of the ensemble a... |
| ctxr_2045360cadb1c82521c2 | unknown              | extends                    | ambiguous_multi_intent          | extends;applies          | adapt_to_domain                               |         0.62 | high           | multiple_strong_non_background_cues          | True                 | False                    | none                   | unknown                         |                |                        | we adapt          | current_paper_extend_cue;current_paper_apply_cue;weak_use_context_feature                                       | Following Sagae and Tsujii (2007) and (Chen et al., 2008) , we adapt the approach to the task of parsing by retraining with agreed upon parses from only a part of the ensemble a... |
| ctxr_2d132256604de2008e2b | unknown              | extends                    | explicit_current_paper_relation | extends                  | improve                                       |         0.62 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | we extend         | current_paper_extend_cue                                                                                        | In this paper, we extend the experiments of Hearne et al. (2008) by adding another syntax-aware phrase extraction methodology, namely percolated dependencies.                       |
| ctxr_d1d006db73b0c50f7eda | unknown              | extends                    | ambiguous_multi_intent          | extends;compares_against | adapt_to_domain;compare_against;report_metric |         0.62 | high           | multiple_strong_non_background_cues          | True                 | False                    | generic_metric_feature | metric                          | F1             | F1                     | our adaptation of | current_paper_extend_cue;explicit_compare_cue;weak_use_context_feature;generic_metric_with_explicit_compare_cue | TwitIE also outperforms Ritter's Twitter NER algorithm (Ritter et al., 2011) and our adaptation of the Stanford NER, which we trained using both tweets and newswire (see (Derczy... |
| ctxr_787e02d85318362f0c93 | unknown              | extends                    | ambiguous_multi_intent          | extends;compares_against | adapt_to_domain;compare_against;report_metric |         0.62 | high           | multiple_strong_non_background_cues          | True                 | False                    | generic_metric_feature | metric                          | F1             | F1                     | our adaptation of | current_paper_extend_cue;explicit_compare_cue;weak_use_context_feature;generic_metric_with_explicit_compare_cue | TwitIE also outperforms Ritter's Twitter NER algorithm (Ritter et al., 2011) and our adaptation of the Stanford NER, which we trained using both tweets and newswire (see (Derczy... |
| ctxr_6f3e65a24d8b2c7cfd49 | introduction         | extends                    | explicit_current_paper_relation | background;extends       | adapt_to_domain                               |         0.88 | high           | explicit_current_relation_with_strong_object | True                 | False                    | object_graph_candidate | model                           | LSTM;CRF       |                        | we adapt          | background_cue;current_paper_extend_cue                                                                         | To do this, we adapt the NeuroNER model proposed in (Dernoncourt et al., 2017) for track 1 (NER offset and entity classification) of the Phar-maCoNER task .                         |
| ctxr_2634141c9f23e9507a89 | unknown              | extends                    | explicit_current_paper_relation | extends                  | adapt_to_domain                               |         0.88 | high           | explicit_current_relation_with_strong_object | True                 | False                    | object_graph_candidate | model                           | BERT;CRF       |                        | we modify         | current_paper_extend_cue                                                                                        | In our implementation we modify BERT (Devlin et al., 2019) model by adding dense layer and CRF layer on top of BERT model for Named Entity detection.                                |
| ctxr_0f32daa1084cb02f1fda | unknown              | extends                    | ambiguous_multi_intent          | extends;applies          | adapt_to_domain                               |         0.62 | high           | multiple_strong_non_background_cues          | True                 | False                    | cited_title_profile    | model                           |                |                        | we adapt          | current_paper_extend_cue;current_paper_apply_cue                                                                | In this step, we adapt a pre-trained sentence encoder E to the in-domain data, i.e., non-knowledgeseeking turns, (Devlin et al., 2019) .                                             |
| ctxr_607b81dc45375652a379 | introduction         | extends                    | explicit_current_paper_relation | extends                  | improve                                       |         0.62 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | we extended       | current_paper_extend_cue                                                                                        | To remedy the above mentioned effects, we extended the normalized frequency of Bai et al. (2009) to a normalized correlation criterion to spot translation equivalents.              |
| ctxr_b32977a1054f98bce5ad | evaluation           | extends                    | explicit_current_paper_relation | extends                  | adapt_to_domain                               |         0.62 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | we adapted        | current_paper_extend_cue                                                                                        | For this evaluation, we adapted the Appraise evaluation tool (Federmann, 2010) so that the interface shows the source sentence, reference translation and the two anonymised tran... |
| ctxr_bdb0dd5ddc719598a90d | unknown              | extends                    | explicit_current_paper_relation | extends                  | improve                                       |         0.88 | high           | explicit_current_relation_with_strong_object | True                 | False                    | object_graph_candidate | software_or_tool                | Moses          |                        | we extend         | current_paper_extend_cue                                                                                        | The system produces distinct 1000-best lists, for which we extend the feature set with the 17 baseline black-box features from sentencelevel Quality Estimation (QE) produced wit... |
| ctxr_70664c650e3fd75821ba | evaluation           | extends                    | explicit_current_paper_relation | extends                  | adapt_to_domain                               |         0.62 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | we adapt          | current_paper_extend_cue;dataset_context_feature                                                                | To evaluate these three approaches, we adapt three standard TableQA datasets: WikiSQL (Zhong et al., 2017) , WikiTableQuestions (Pasupat and Liang, 2015) and TabMCQ (Jauhar et a... |
| ctxr_3f7d65073884dfbd052d | abstract             | extends                    | explicit_current_paper_relation | background;extends       | improve                                       |         0.88 | high           | explicit_current_relation_with_strong_object | True                 | True                     | object_graph_candidate | benchmark_or_protocol           | WMT            |                        | we extend         | cited_work_description;background_cue;current_paper_extend_cue                                                  | In this paper, we extend the Morpheval protocol introduced by Burlot and Yvon (2017) for the English-to-Czech and English-to-Latvian translation directions to three additional l... |
| ctxr_c2c1e87990bda4ff18f4 | unknown              | extends                    | explicit_current_paper_relation | extends                  | improve                                       |         0.62 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | we extended       | current_paper_extend_cue                                                                                        | For illustration purposes, we extended it here by MUC (Grishman and Sundheim, 1996) entity types such as Person, Organization, etc.                                                  |
| ctxr_15ca6d18994ffffa1813 | introduction         | extends                    | explicit_current_paper_relation | extends                  | improve                                       |         0.62 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | we extend         | current_paper_extend_cue                                                                                        | First, we extend the mechanism of adding gap variables for nodes dominating a site of discontinuity (Collins, 1997) .                                                                |
| ctxr_9fd7c0f42e1af7787bcf | related_work         | extends                    | explicit_current_paper_relation | background;extends       | improve                                       |         0.62 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | we improved       | background_cue;current_paper_extend_cue;dataset_context_feature                                                 | In our previous work (Zhang 2001) , the way we improved the segmenter was by augmenting the frequency list with a list of new words found in the corpus.                             |
| ctxr_3d8428866651f6c99251 | introduction         | extends                    | explicit_current_paper_relation | extends                  | improve                                       |         0.62 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | we extend         | current_paper_extend_cue                                                                                        | The main contribution of this work is a reexamination of (Ayan and Dorr, 2006 ) work which we extend in several ways.                                                                |
| ctxr_d21067ac7dfc6e8bffcb | introduction         | extends                    | explicit_current_paper_relation | extends                  | improve                                       |         0.62 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | We extend         | current_paper_extend_cue                                                                                        | • We extend Filippova (2010)'s word graphbased MSC approach to produce wellpunctuated and more informative compressions.                                                             |

## Example Critiques
| context_id                | normalized_section   | primary_candidate_intent   | phase2_candidate_type           | candidate_intents    | candidate_relation_subtypes   |   confidence | llm_priority   | llm_reason                                   | should_send_to_llm   | cited_work_description   | object_type_source     | primary_candidate_object_type   | object_names   | generic_metric_names   | evidence_span                   | matched_rules                                                                                                                  | sentence_text                                                                                                                                                                        |
|:--------------------------|:---------------------|:---------------------------|:--------------------------------|:---------------------|:------------------------------|-------------:|:---------------|:---------------------------------------------|:---------------------|:-------------------------|:-----------------------|:--------------------------------|:---------------|:-----------------------|:--------------------------------|:-------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ctxr_56ad9f51105d23c96ad1 | related_work         | critiques                  | explicit_current_paper_relation | background;critiques | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                |                        | drawbacks of the                | cited_work_description;background_cue;targeted_critique_cue                                                                    | As a possible solution to the drawbacks of the pure statistical machine translation (weak on reordering; lack of target language fluency), syntactic approaches were proposed tha... |
| ctxr_bf0b4bf611ada8efce34 | related_work         | critiques                  | explicit_current_paper_relation | background;critiques | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                |                        | drawbacks of the                | cited_work_description;background_cue;targeted_critique_cue                                                                    | As a possible solution to the drawbacks of the pure statistical machine translation (weak on reordering; lack of target language fluency), syntactic approaches were proposed tha... |
| ctxr_3f4b77da44444ee3815f | related_work         | critiques                  | explicit_current_paper_relation | background;critiques | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                |                        | drawbacks of the                | cited_work_description;background_cue;targeted_critique_cue                                                                    | As a possible solution to the drawbacks of the pure statistical machine translation (weak on reordering; lack of target language fluency), syntactic approaches were proposed tha... |
| ctxr_7a6a8ea86f8168b62726 | related_work         | critiques                  | explicit_current_paper_relation | background;critiques | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                |                        | drawbacks of the                | cited_work_description;background_cue;targeted_critique_cue                                                                    | As a possible solution to the drawbacks of the pure statistical machine translation (weak on reordering; lack of target language fluency), syntactic approaches were proposed tha... |
| ctxr_61495d6b3572b3b7b0a6 | related_work         | critiques                  | explicit_current_paper_relation | background;critiques | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                |                        | drawbacks of the                | cited_work_description;background_cue;targeted_critique_cue                                                                    | As a possible solution to the drawbacks of the pure statistical machine translation (weak on reordering; lack of target language fluency), syntactic approaches were proposed tha... |
| ctxr_cc8878dfc0e0046de376 | related_work         | critiques                  | explicit_current_paper_relation | background;critiques | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                |                        | drawbacks of the                | cited_work_description;background_cue;targeted_critique_cue                                                                    | As a possible solution to the drawbacks of the pure statistical machine translation (weak on reordering; lack of target language fluency), syntactic approaches were proposed tha... |
| ctxr_205f922d750c8d8bed22 | related_work         | critiques                  | explicit_current_paper_relation | background;critiques | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                |                        | drawbacks of the                | cited_work_description;background_cue;targeted_critique_cue                                                                    | As a possible solution to the drawbacks of the pure statistical machine translation (weak on reordering; lack of target language fluency), syntactic approaches were proposed tha... |
| ctxr_491de660009417c3a5c3 | related_work         | critiques                  | explicit_current_paper_relation | background;critiques | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                |                        | drawbacks of the                | cited_work_description;background_cue;targeted_critique_cue                                                                    | As a possible solution to the drawbacks of the pure statistical machine translation (weak on reordering; lack of target language fluency), syntactic approaches were proposed tha... |
| ctxr_e3bb7e1608994c9a3fd2 | related_work         | critiques                  | explicit_current_paper_relation | background;critiques | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                |                        | drawbacks of the                | cited_work_description;background_cue;targeted_critique_cue                                                                    | As a possible solution to the drawbacks of the pure statistical machine translation (weak on reordering; lack of target language fluency), syntactic approaches were proposed tha... |
| ctxr_f57feca6f99aef2f9031 | related_work         | critiques                  | explicit_current_paper_relation | background;critiques | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                |                        | drawbacks of the                | cited_work_description;background_cue;targeted_critique_cue                                                                    | As a possible solution to the drawbacks of the pure statistical machine translation (weak on reordering; lack of target language fluency), syntactic approaches were proposed tha... |
| ctxr_18f1191f75eaf360775f | related_work         | critiques                  | explicit_current_paper_relation | background;critiques | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                |                        | drawbacks of the                | cited_work_description;background_cue;targeted_critique_cue                                                                    | As a possible solution to the drawbacks of the pure statistical machine translation (weak on reordering; lack of target language fluency), syntactic approaches were proposed tha... |
| ctxr_aecefba42c83ddce6eb5 | introduction         | critiques                  | explicit_current_paper_relation | critiques            | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | limitations of statistical      | targeted_critique_cue                                                                                                          | One of the main limitations of statistical machine translation (SMT) is the sensitivity to data sparseness, due to the word-based or phrased-based approach incorporated in SMT (... |
| ctxr_74898fe56cc634a3b42f | unknown              | critiques                  | explicit_current_paper_relation | critiques            | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | False                    | none                   | unknown                         |                |                        | MWT cannot                      | targeted_critique_cue;weak_use_context_feature                                                                                 | If an MWT cannot be directly translated, we generate possible translations by using a compositional method (Grefenstette, 1999).                                                     |
| ctxr_687f54fc84502a8d9360 | related_work         | critiques                  | explicit_current_paper_relation | background;critiques | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                |                        | and cannot                      | cited_work_description;targeted_critique_cue                                                                                   | One of the critical issues that we face in paraphrase generation is how to develop and maintain knowledge resources that covers a sufficiently wide range of paraphrasing pattern... |
| ctxr_78cd108a298f45c67880 | related_work         | critiques                  | explicit_current_paper_relation | background;critiques | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                |                        | and cannot                      | cited_work_description;targeted_critique_cue                                                                                   | One of the critical issues that we face in paraphrase generation is how to develop and maintain knowledge resources that covers a sufficiently wide range of paraphrasing pattern... |
| ctxr_e7ff60f4aa2e59325b28 | related_work         | critiques                  | explicit_current_paper_relation | background;critiques | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence    | True                 | True                     | none                   | unknown                         |                |                        | and cannot                      | cited_work_description;targeted_critique_cue                                                                                   | One of the critical issues that we face in paraphrase generation is how to develop and maintain knowledge resources that covers a sufficiently wide range of paraphrasing pattern... |
| ctxr_c5e8b5d3130ff9a4f023 | evaluation           | critiques                  | explicit_current_paper_relation | critiques            | critique_limitation           |         0.65 | low            | generic_metric_feature_only                  | False                | False                    | generic_metric_feature | metric                          | F1             | F1                     | to suffer from                  | targeted_critique_cue;generic_metric_feature_only                                                                              | It is important to note that P k metric is known to suffer from biases, for example penalizing false negatives more than false positives and discounting errors close to the docu... |
| ctxr_629de95313bc65835807 | model                | critiques                  | explicit_current_paper_relation | critiques            | critique_limitation           |         0.82 | high           | explicit_current_relation_with_strong_object | True                 | False                    | object_graph_candidate | model                           | word2vec;LSTM  |                        | we cannot                       | targeted_critique_cue                                                                                                          | Unfortunately, we cannot directly compare model sizes with (Koshorek et al., 2018) since they rely on a subset of the embeddings from a public word2vec archive that includes ove... |
| ctxr_efccee3025d156f2b70f | related_work         | critiques                  | explicit_current_paper_relation | critiques            | critique_limitation           |         0.65 | medium         | weak_cue_with_object_mention                 | True                 | False                    | generic_metric_feature | metric                          | F1             | F1                     | Their algorithm does not handle | targeted_critique_cue;weak_extend_context_feature;weak_use_context_feature;generic_metric_feature_only;dataset_context_feature | Their algorithm does not handle multiple affixes per word. (Goldsmith 2000) presents an unsupervised technique based on the expectationmaximization algorithm and minimum descrip... |
| ctxr_4c800d4da50feefb74eb | related_work         | critiques                  | explicit_current_paper_relation | critiques            | critique_limitation           |         0.65 | medium         | weak_cue_with_object_mention                 | True                 | False                    | generic_metric_feature | metric                          | F1             | F1                     | Their algorithm does not handle | targeted_critique_cue;weak_extend_context_feature;weak_use_context_feature;generic_metric_feature_only;dataset_context_feature | Their algorithm does not handle multiple affixes per word. (Goldsmith 2000) presents an unsupervised technique based on the expectationmaximization algorithm and minimum descrip... |

## Example Applies
| context_id                | normalized_section   | primary_candidate_intent   | phase2_candidate_type   | candidate_intents               | candidate_relation_subtypes   |   confidence | llm_priority   | llm_reason                                                                       | should_send_to_llm   | cited_work_description   | object_type_source     | primary_candidate_object_type   | object_names   | generic_metric_names   | evidence_span                                                                                | matched_rules                                                                                                | sentence_text                                                                                                                                                                        |
|:--------------------------|:---------------------|:---------------------------|:------------------------|:--------------------------------|:------------------------------|-------------:|:---------------|:---------------------------------------------------------------------------------|:---------------------|:-------------------------|:-----------------------|:--------------------------------|:---------------|:-----------------------|:---------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ctxr_2cecf89740d4eb3330bb | introduction         | applies                    | ambiguous_multi_intent  | applies;uses                    | adapt_to_domain;direct_use    |         0.82 | high           | explicit_current_relation_with_strong_object;multiple_strong_non_background_cues | True                 | False                    | object_mention         | model                           | LSTM           |                        | we apply a two-tier dropout methodology (explained in Section 3) in order to                 | current_paper_apply_cue;current_paper_use_cue                                                                | Instead, we use a strategy inspired by the graph-based parser of Kiperwasser and Goldberg (2016) , with the following major differences: (a) the network is trained to produce fu... |
| ctxr_dc841951bb85c039a52e | unknown              | extends                    | ambiguous_multi_intent  | extends;applies                 | adapt_to_domain               |         0.62 | high           | multiple_strong_non_background_cues                                              | True                 | False                    | none                   | unknown                         |                |                        | we adapt                                                                                     | current_paper_extend_cue;current_paper_apply_cue;weak_use_context_feature                                    | Following Sagae and Tsujii (2007) and (Chen et al., 2008) , we adapt the approach to the task of parsing by retraining with agreed upon parses from only a part of the ensemble a... |
| ctxr_2045360cadb1c82521c2 | unknown              | extends                    | ambiguous_multi_intent  | extends;applies                 | adapt_to_domain               |         0.62 | high           | multiple_strong_non_background_cues                                              | True                 | False                    | none                   | unknown                         |                |                        | we adapt                                                                                     | current_paper_extend_cue;current_paper_apply_cue;weak_use_context_feature                                    | Following Sagae and Tsujii (2007) and (Chen et al., 2008) , we adapt the approach to the task of parsing by retraining with agreed upon parses from only a part of the ensemble a... |
| ctxr_4958a31524fd0d121108 | evaluation           | applies                    | ambiguous_multi_intent  | applies;uses                    | direct_use                    |         0.88 | high           | explicit_current_relation_with_strong_object;multiple_strong_non_background_cues | True                 | False                    | object_graph_candidate | model                           | LSTM;F1        | F1                     | we use a set of binary deep, bidirectional Long Short Term Memory (LSTM) networks to predict | current_paper_apply_cue;current_paper_use_cue;generic_metric_feature_only                                    | Inspired by recent semantic parsing models, e.g., Zhou and Xu (2015) , we use a set of binary deep, bidirectional Long Short Term Memory (LSTM) networks to predict frame labels.    |
| ctxr_8f1f0afe1a5a6e13508a | unknown              | applies                    | ambiguous_multi_intent  | applies;uses                    | adapt_to_domain;direct_use    |         0.62 | high           | multiple_strong_non_background_cues                                              | True                 | False                    | none                   | unknown                         |                |                        | we applied Pointwise Mutual Information (Church and Hanks, 1990 ) as a weighting function to | current_paper_apply_cue;current_paper_use_cue                                                                | In a second step, we applied Pointwise Mutual Information (Church and Hanks, 1990 ) as a weighting function to discover informative semantic similarity relations between words.     |
| ctxr_0f32daa1084cb02f1fda | unknown              | extends                    | ambiguous_multi_intent  | extends;applies                 | adapt_to_domain               |         0.62 | high           | multiple_strong_non_background_cues                                              | True                 | False                    | cited_title_profile    | model                           |                |                        | we adapt                                                                                     | current_paper_extend_cue;current_paper_apply_cue                                                             | In this step, we adapt a pre-trained sentence encoder E to the in-domain data, i.e., non-knowledgeseeking turns, (Devlin et al., 2019) .                                             |
| ctxr_cdf34a3eb7dbe69b6d51 | model                | applies                    | ambiguous_multi_intent  | background;applies;uses         | direct_use                    |         0.88 | high           | explicit_current_relation_with_strong_object;multiple_strong_non_background_cues | True                 | True                     | object_graph_candidate | software_or_tool                | GIZA++         |                        | we used GIZA++ (Och and Ney, 2003) to generate                                               | cited_work_description;current_paper_apply_cue;current_paper_use_cue                                         | Hence, we used GIZA++ (Och and Ney, 2003) to generate IBM model 4 alignments (Brown et al., 1993) for character n-grams, which we symmetrized using the grow-diag-final-and heuri... |
| ctxr_7690fb65d3f0a46715e9 | model                | applies                    | ambiguous_multi_intent  | background;applies;uses         | direct_use                    |         0.88 | high           | explicit_current_relation_with_strong_object;multiple_strong_non_background_cues | True                 | True                     | object_graph_candidate | software_or_tool                | GIZA++         |                        | we used GIZA++ (Och and Ney, 2003) to generate                                               | cited_work_description;current_paper_apply_cue;current_paper_use_cue                                         | Hence, we used GIZA++ (Och and Ney, 2003) to generate IBM model 4 alignments (Brown et al., 1993) for character n-grams, which we symmetrized using the grow-diag-final-and heuri... |
| ctxr_9a87f2b5789ed00ca650 | experiment           | applies                    | ambiguous_multi_intent  | applies;uses                    | direct_use                    |         0.62 | high           | multiple_strong_non_background_cues                                              | True                 | False                    | none                   | unknown                         |                |                        | we used byte pair encoding (BPE) to generate                                                 | current_paper_apply_cue;current_paper_use_cue                                                                | To overcome this limitation, we used byte pair encoding (BPE) to generate subword units (Sennrich et al., 2016) .                                                                    |
| ctxr_adb950518503f5b67762 | experiment           | applies                    | ambiguous_multi_intent  | background;applies;uses         | direct_use                    |         0.62 | high           | multiple_strong_non_background_cues                                              | True                 | True                     | none                   | unknown                         |                |                        | We used the Stanford Named Entity tagger by Finkel et al. (2005) to tag                      | cited_work_description;current_paper_apply_cue;current_paper_use_cue                                         | We used the Stanford Named Entity tagger by Finkel et al. (2005) to tag the named entities.                                                                                          |
| ctxr_3a1af4f53f5fa583399d | introduction         | applies                    | ambiguous_multi_intent  | applies;uses                    | adapt_to_domain;direct_use    |         0.88 | high           | explicit_current_relation_with_strong_object;multiple_strong_non_background_cues | True                 | False                    | object_graph_candidate | model                           | BERT           |                        | We apply our benchmarks to                                                                   | current_paper_apply_cue;current_paper_use_cue;dataset_context_feature                                        | We apply our benchmarks to a set of neural models including BERT (Devlin et al., 2018) and DPR (Karpukhin et al., 2020) , test for gender bias, and conclude with a discussion of... |
| ctxr_d1c1f7e1f296411c5190 | unknown              | applies                    | ambiguous_multi_intent  | applies;uses                    | direct_use                    |         0.62 | high           | multiple_strong_non_background_cues                                              | True                 | False                    | none                   | unknown                         |                |                        | we use sent2vec 3 (Pagliardini et al., 2018) to generate                                     | current_paper_apply_cue;current_paper_use_cue                                                                | S2V: we use sent2vec 3 (Pagliardini et al., 2018) to generate sentence embeddings.                                                                                                   |
| ctxr_4f3b609ef1380f60bbb0 | results              | applies                    | ambiguous_multi_intent  | applies;uses                    | adapt_to_domain;direct_use    |         0.62 | high           | multiple_strong_non_background_cues                                              | True                 | False                    | none                   | unknown                         |                |                        | we applied the class-based smoothing procedure to                                            | current_paper_apply_cue;current_paper_use_cue;dataset_context_feature                                        | To address this question, we applied the class-based smoothing procedure to a set of adjective-noun pairs that occur in the corpus with varying frequencies, using the materials ... |
| ctxr_5bd28805329a6bf86ef2 | evaluation           | applies                    | ambiguous_multi_intent  | background;applies;uses         | adapt_to_domain;direct_use    |         0.88 | high           | explicit_current_relation_with_strong_object;multiple_strong_non_background_cues | True                 | True                     | object_graph_candidate | dataset_or_database             | Penn Treebank  |                        | We applied our tagger with the best configuration to                                         | cited_work_description;current_paper_apply_cue;current_paper_use_cue;dataset_context_feature                 | We applied our tagger with the best configuration to the annotated dataset provided by Ritter et al. (2011) .                                                                        |
| ctxr_fa9c8ad940d986218934 | unknown              | applies                    | ambiguous_multi_intent  | applies;uses                    | adapt_to_domain;direct_use    |         0.62 | high           | multiple_strong_non_background_cues                                              | True                 | False                    | none                   | unknown                         |                |                        | we apply softmax to S, and zero out probabilities below a threshold to                       | current_paper_apply_cue;current_paper_use_cue                                                                | To this end, first, inspired by probability thresholding (Dou and Neubig, 2021), we apply softmax to S, and zero out probabilities below a threshold to get a sourceto-target pro... |
| ctxr_a688a58d3fe766727b7d | introduction         | applies                    | ambiguous_multi_intent  | background;applies;uses         | direct_use                    |         0.62 | high           | multiple_strong_non_background_cues                                              | True                 | True                     | none                   | unknown                         |                |                        | We used FreeLing (http:nlp.lsi.upc.edu/ freeling/) to predict                                | cited_work_description;current_paper_apply_cue;current_paper_use_cue                                         | 2 We used FreeLing (http:nlp.lsi.upc.edu/ freeling/) to predict the POS tags of the translation hypotheses and, for the sake of clarity, mapped the 71 tags used by FreeLing to t... |
| ctxr_d9ff98bc559193ab47d9 | unknown              | applies                    | ambiguous_multi_intent  | applies;uses                    | adapt_to_domain;direct_use    |         0.62 | high           | multiple_strong_non_background_cues                                              | True                 | False                    | none                   | unknown                         |                |                        | we apply beam search and Huang and Sagae (2010)'s DP techniques to                           | current_paper_apply_cue;current_paper_use_cue                                                                | As mentioned in Section 1, we apply beam search and Huang and Sagae (2010)'s DP techniques to our top-down parser.                                                                   |
| ctxr_daa73505994c88bd47dc | error_analysis       | applies                    | ambiguous_multi_intent  | applies;uses                    | adapt_to_domain;direct_use    |         0.62 | high           | multiple_strong_non_background_cues                                              | True                 | False                    | none                   | unknown                         |                |                        | we apply it to a dependency parser in order to                                               | current_paper_apply_cue;current_paper_use_cue                                                                | Our variational model is inspired by the study of Li et al. (2009) and we apply it to a dependency parser in order to select better candidates with third-order information.         |
| ctxr_dec376636a7e5a07d35b | analysis             | applies                    | ambiguous_multi_intent  | background;applies;uses         | adapt_to_domain;direct_use    |         0.88 | high           | explicit_current_relation_with_strong_object;multiple_strong_non_background_cues | True                 | False                    | object_graph_candidate | benchmark_or_protocol           | SemEval        |                        | we apply the NLSE model to                                                                   | background_cue;current_paper_apply_cue;current_paper_use_cue                                                 | In this section, we apply the NLSE model to the message polarity classification task proposed by SemEval, for their well-known Twitter sentiment analysis challenge (Nakov et al.... |
| ctxr_02b361668c9f884f39af | introduction         | extends                    | ambiguous_multi_intent  | background;extends;applies;uses | adapt_to_domain;direct_use    |         0.88 | high           | explicit_current_relation_with_strong_object;multiple_strong_non_background_cues | True                 | True                     | object_graph_candidate | method                          | CRF            |                        | we adapt                                                                                     | cited_work_description;background_cue;current_paper_extend_cue;current_paper_apply_cue;current_paper_use_cue | Accordingly, we adapt MAST for the purpose of the PARSEME shared task; but, in contrast to Saied et al. (2017) , instead of using a linear SVM for learning and predicting transi... |

## Example Background
| context_id                | normalized_section   | primary_candidate_intent   | phase2_candidate_type   | candidate_intents   | candidate_relation_subtypes   |   confidence | llm_priority   | llm_reason                                                                 | should_send_to_llm   | cited_work_description   | object_type_source     | primary_candidate_object_type   | object_names   | generic_metric_names   | evidence_span   | matched_rules                                                               | sentence_text                                                                                                                                                                        |
|:--------------------------|:---------------------|:---------------------------|:------------------------|:--------------------|:------------------------------|-------------:|:---------------|:---------------------------------------------------------------------------|:---------------------|:-------------------------|:-----------------------|:--------------------------------|:---------------|:-----------------------|:----------------|:----------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ctxr_4771edcc3e42c8bb07c7 | introduction         | background                 | cited_work_description  | background          | none                          |         0.55 | none           | clear_background_no_object                                                 | False                | True                     | none                   | unknown                         |                |                        | described       | cited_work_description;background_cue;weak_use_context_feature              | In NLP, Elsner and Charniak (2010) described the task of thread disentanglement as "the clustering task of dividing a transcript into a set of distinct conversations," in which ... |
| ctxr_fc94564ed0054ac2126f | introduction         | background                 | background_prior        | background          | none                          |         0.35 | low            | section_prior_only                                                         | False                | False                    | none                   | unknown                         |                |                        |                 | weak_section_prior:introduction                                             | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki et al., 2003) , and emails with headers... |
| ctxr_d06d69e8921c81b378ac | introduction         | background                 | cited_work_description  | background          | none                          |         0.55 | none           | clear_background_no_object                                                 | False                | True                     | none                   | unknown                         |                |                        | annotated       | cited_work_description;dataset_context_feature                              | Carenini et al. (2008) annotated 39 email "conversations" from the Enron Email Corpus for email summariation.                                                                        |
| ctxr_68d4edb5f20b826f715b | introduction         | background                 | cited_work_description  | background          | none                          |         0.55 | none           | clear_background_no_object                                                 | False                | True                     | none                   | unknown                         |                |                        | used            | cited_work_description;dataset_context_feature                              | Wan and McKeown (2004) used a privatelyavailable corpus of 300 threads for summary generation.                                                                                       |
| ctxr_b166bf8511a77353542f | introduction         | background                 | cited_work_description  | background          | none                          |         0.55 | none           | clear_background_no_object                                                 | False                | True                     | none                   | unknown                         |                |                        | used            | cited_work_description;dataset_context_feature                              | Rambow et al. (2004) used a privatelyavailable corpus of 96 email threads for thread summarization.                                                                                  |
| ctxr_4ba57d063d3c71fa78df | dataset              | background                 | cited_work_description  | background          | none                          |         0.55 | none           | clear_background_no_object                                                 | False                | True                     | none                   | unknown                         |                |                        | used            | cited_work_description;dataset_context_feature                              | Rambow et al. (2004) used a privately-available corpus of 96 email threads, but did not specify how they determined the threads.                                                     |
| ctxr_044c96a8f9c2342b58ff | related_work         | background                 | cited_work_description  | background          | none                          |         0.55 | none           | clear_background_no_object                                                 | False                | True                     | none                   | unknown                         |                |                        | used            | cited_work_description                                                      | In (Rosario and Hearst, 2001 ) authors used neural networks to determine 20 semantic relationssimilarily to (Nastase et al., 2006) -between a head and a modifier of noun phrase.    |
| ctxr_f6863fcab52657a5c16e | related_work         | background                 | cited_work_description  | background          | none                          |         0.62 | medium         | weak_cue_with_object_mention;cited_work_description_with_high_value_object | True                 | True                     | object_graph_candidate | benchmark_or_protocol           | SemEval        |                        | developed       | cited_work_description;weak_extend_context_feature;weak_use_context_feature | In (Tratz and Hovy, 2010) the authors developed a system based on the Maximum Entropy classifier, able to detect 10 bidirectional semantic relations Achieved F-measures depended... |
| ctxr_71d08900475d9c8505ab | related_work         | background                 | cited_work_description  | background          | none                          |         0.55 | none           | clear_background_no_object                                                 | False                | True                     | none                   | unknown                         |                |                        | used            | cited_work_description                                                      | The same set of semantic relations was used in (Rink and Harabagiu, 2010) .                                                                                                          |
| ctxr_b1bfb1536bcb5cbbf8b5 | related_work         | background                 | cited_work_description  | background          | none                          |         0.55 | none           | clear_background_no_object                                                 | False                | True                     | none                   | unknown                         |                |                        | used            | cited_work_description                                                      | Authors in (Tymoshenko and Giuliano, 2010 ) used shallow syntactic parsing and semantic information from ResearchCyc (Lenat, 1995) in the same task of recognizing semantic relat... |
| ctxr_f8a4c2e6aa2834642a71 | related_work         | background                 | cited_work_description  | background          | none                          |         0.55 | none           | clear_background_no_object                                                 | False                | True                     | none                   | unknown                         |                |                        | used            | cited_work_description;dataset_context_feature                              | In (Hearst, 1992) authors used set of manually written rules for identification of hyperonymy relations. (Ben Abacha and Zweigenbaum, 2011) used linguistic patterns (built semi-... |
| ctxr_3e4722d1950da619a7dd | unknown              | background                 | cited_work_description  | background          | none                          |         0.62 | medium         | weak_cue_with_object_mention;cited_work_description_with_high_value_object | True                 | True                     | object_graph_candidate | method                          | CRF            |                        | annotated       | cited_work_description;evaluation_context_feature;dataset_context_feature   | We made use of a CRF shallow parser (Radziszewski and Pawlaczek, 2012) trained on an annotated corpus of Polish (KPWr) (Broda et al., 2012) which comprises shallow syntactic ann... |
| ctxr_9ab7ad32be76baef24a4 | introduction         | background                 | background_prior        | background          | none                          |         0.35 | low            | section_prior_only                                                         | False                | False                    | none                   | unknown                         |                |                        |                 | weak_section_prior:introduction                                             | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-based machine translation (EBMT) (Somers, ... |
| ctxr_008f302607deda562c24 | introduction         | background                 | background_prior        | background          | none                          |         0.35 | low            | section_prior_only                                                         | False                | False                    | none                   | unknown                         |                |                        |                 | weak_section_prior:introduction                                             | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-based machine translation (EBMT) (Somers, ... |
| ctxr_373b75e6049f7bde6cca | introduction         | background                 | background_prior        | background          | none                          |         0.35 | low            | section_prior_only                                                         | False                | False                    | none                   | unknown                         |                |                        |                 | weak_section_prior:introduction                                             | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-based machine translation (EBMT) (Somers, ... |
| ctxr_18b9cd4865ae3fef4d3f | introduction         | background                 | background_prior        | background          | none                          |         0.35 | low            | section_prior_only                                                         | False                | False                    | none                   | unknown                         |                |                        |                 | weak_section_prior:introduction                                             | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-based machine translation (EBMT) (Somers, ... |
| ctxr_7d7d31957a351c96c69d | introduction         | background                 | background_prior        | background          | none                          |         0.35 | low            | section_prior_only                                                         | False                | False                    | none                   | unknown                         |                |                        |                 | weak_section_prior:introduction                                             | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-based machine translation (EBMT) (Somers, ... |
| ctxr_8fb909e0fd3aae1d73e8 | introduction         | background                 | background_prior        | background          | none                          |         0.35 | low            | section_prior_only                                                         | False                | False                    | none                   | unknown                         |                |                        |                 | weak_section_prior:introduction                                             | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-based machine translation (EBMT) (Somers, ... |
| ctxr_4bb1b170fe1966db7825 | introduction         | background                 | background_prior        | background          | none                          |         0.35 | low            | section_prior_only                                                         | False                | False                    | none                   | unknown                         |                |                        |                 | weak_section_prior:introduction                                             | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-based machine translation (EBMT) (Somers, ... |
| ctxr_f657889e88c427521c67 | introduction         | background                 | background_prior        | background          | none                          |         0.35 | low            | section_prior_only                                                         | False                | False                    | none                   | unknown                         |                |                        |                 | weak_section_prior:introduction                                             | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-based machine translation (EBMT) (Somers, ... |

## Example Unclear
| context_id                | normalized_section   | primary_candidate_intent   | phase2_candidate_type   | candidate_intents   | candidate_relation_subtypes   |   confidence | llm_priority   | llm_reason                                                      | should_send_to_llm   | cited_work_description   | object_type_source     | primary_candidate_object_type   | object_names   | generic_metric_names   | evidence_span   | matched_rules                                                                                  | sentence_text                                                                                                                                                                        |
|:--------------------------|:---------------------|:---------------------------|:------------------------|:--------------------|:------------------------------|-------------:|:---------------|:----------------------------------------------------------------|:---------------------|:-------------------------|:-----------------------|:--------------------------------|:---------------|:-----------------------|:----------------|:-----------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ctxr_6739ef248e0241672c80 | dataset              | unclear                    | no_cue                  | unclear             | none                          |         0.2  | none           | no_cue_no_object                                                | False                | False                    | none                   | unknown                         |                |                        |                 | no_cue                                                                                         | Wan and McKeown (2004) reconstructed threads by header Message-ID information.                                                                                                       |
| ctxr_8361b89d504826d53df9 | unknown              | unclear                    | no_cue                  | unclear             | none                          |         0.2  | none           | no_cue_no_object                                                | False                | False                    | none                   | unknown                         |                |                        |                 | no_cue                                                                                         | 1999 ) uses pairs of words occurring in the same order for the two emails; Token Pair Distance (Hatzivassiloglou et al., 1999) measures the distance between pairs of words.         |
| ctxr_d573e73d4a69363cdfc0 | results              | unclear                    | generic_metric_feature  | unclear             | none                          |         0.42 | medium         | weak_cue_with_object_mention                                    | True                 | False                    | generic_metric_feature | metric                          | accuracy       | accuracy               | using           | weak_use_context_feature;generic_metric_feature_only;weak_cue_without_current_subject          | Elsner and Charniak (2011) use coherence models to disentangle chat, using some features (entity grid, topical entity grid) which correspond to the information in our content fe... |
| ctxr_fde2b4fe687323ff4bd3 | experiment           | unclear                    | generic_metric_feature  | unclear             | none                          |         0.35 | low            | generic_metric_feature_only                                     | False                | False                    | generic_metric_feature | metric                          | F1             | F1                     |                 | generic_metric_feature_only;no_cue                                                             | The evaluation was run with respect to precision, recall, F -measure, and alignment error rate (AER) considering sure and probable alignments but not NULL ones (Mihalcea and Ped... |
| ctxr_d6e2c97936b9e4f1b547 | unknown              | unclear                    | no_cue                  | unclear             | none                          |         0.2  | none           | no_cue_no_object                                                | False                | False                    | none                   | unknown                         |                |                        |                 | no_cue                                                                                         | The intuition for adjustment formula comes from the work of (Chung and Gildea, 2009) and (Liang and Klein, 2009) , who use a exponential Length Penalty measure to adjust their m... |
| ctxr_3d90b8c7895d21cc88e6 | unknown              | unclear                    | no_cue                  | unclear             | none                          |         0.2  | none           | no_cue_no_object                                                | False                | False                    | none                   | unknown                         |                |                        |                 | no_cue                                                                                         | The intuition for adjustment formula comes from the work of (Chung and Gildea, 2009) and (Liang and Klein, 2009) , who use a exponential Length Penalty measure to adjust their m... |
| ctxr_2ad99a8ed8d7768f006a | dataset              | unclear                    | no_cue                  | unclear             | none                          |         0.2  | none           | no_cue_no_object                                                | False                | False                    | none                   | unknown                         |                |                        |                 | no_cue                                                                                         | For example, the technique of Poon et al (2009) could be used to obtain accurate stems for each word.                                                                                |
| ctxr_ed05fb392fd1423ed712 | model                | unclear                    | weak_cue_feature        | unclear             | none                          |         0.3  | none           | no_priority_rule                                                | False                | False                    | none                   | unknown                         |                |                        | based on        | weak_extend_context_feature;weak_use_context_feature;weak_cue_without_current_subject          | A factored language model (FLM) (Bilmes and Kirchhoff, 2003) is based on a representation of words as feature vectors and can utilize a variety of additional information sources... |
| ctxr_ecb9324b4abca2fe76b6 | model                | unclear                    | weak_cue_feature        | unclear             | none                          |         0.3  | none           | no_priority_rule                                                | False                | False                    | none                   | unknown                         |                |                        | using           | weak_use_context_feature;weak_cue_without_current_subject                                      | For the factored language models, a feature-based word representation was obtained by tagging the text with Rathnaparki's maximum-entropy tagger (Ratnaparkhi, 1996) and by stemm... |
| ctxr_d2f7e10dccf772790070 | dataset              | unclear                    | weak_cue_feature        | unclear             | none                          |         0.42 | medium         | weak_cue_with_object_mention                                    | True                 | False                    | object_mention         | dataset_or_database             | Penn Treebank  |                        | using           | weak_use_context_feature;dataset_context_feature;weak_cue_without_current_subject              | The two corpora were converted from PTB constituency trees into dependency trees using the Stanford dependency converter (de Marneffe and Manning, 2008).                            |
| ctxr_26559d1672acccfd09ea | unknown              | unclear                    | generic_metric_feature  | unclear             | none                          |         0.42 | medium         | weak_cue_with_object_mention                                    | True                 | False                    | generic_metric_feature | metric                          | accuracy       | accuracy               | using           | weak_use_context_feature;generic_metric_feature_only;weak_cue_without_current_subject          | MST is a graph-based parser which optimizes its parse tree globally (McDonald et al., 2005) , using a variety of feature sets, i.e., edge,                                           |
| ctxr_c223321394c5bbc2bcec | unknown              | unclear                    | generic_metric_feature  | unclear             | none                          |         0.35 | low            | generic_metric_feature_only                                     | False                | False                    | generic_metric_feature | metric                          | accuracy       | accuracy               |                 | generic_metric_feature_only;no_cue                                                             | This corroborates findings by Brants (2000) .                                                                                                                                        |
| ctxr_72089786b736eb3c1d50 | unknown              | unclear                    | generic_metric_feature  | unclear             | report_metric                 |         0.42 | medium         | weak_cue_with_object_mention;generic_metric_with_evaluation_cue | True                 | False                    | generic_metric_feature | metric                          | accuracy       | accuracy               | experiments on  | generic_metric_with_evaluation_cue;evaluation_context_feature;weak_cue_without_current_subject | Even if we balance the source and target domain data, which proved beneficial in our previous experiments on parsing (Khan et al., 2013) , we reach an accuracy of 93.48%, well b... |
| ctxr_a1a94117eac1ba73330e | unknown              | unclear                    | weak_cue_feature        | unclear             | none                          |         0.3  | none           | no_priority_rule                                                | False                | False                    | none                   | unknown                         |                |                        | corpus          | dataset_context_feature;weak_cue_without_current_subject                                       | We provided not only training data from the Europarl corpus (Koehn, 2005) , but also additional resources: sentence and word alignments, the decoder Pharaoh 1 (Koehn, 2004b) , a... |
| ctxr_4355448353bdd023508c | unknown              | unclear                    | weak_cue_feature        | unclear             | none                          |         0.42 | medium         | weak_cue_with_object_mention;unclear_with_graph_candidate       | True                 | False                    | object_graph_candidate | software_or_tool                | GIZA++         |                        | corpora         | dataset_context_feature;weak_cue_without_current_subject                                       | The field of statistical machine translation has been blessed with a long tradition of freely available software tools -such as GIZA++ (Och and Ney, 2003) -and parallel corpora ... |
| ctxr_e68e33d8515b22b2c3ce | results              | unclear                    | weak_cue_feature        | unclear             | none                          |         0.42 | medium         | weak_cue_with_object_mention;unclear_with_graph_candidate       | True                 | False                    | object_graph_candidate | metric                          | BLEU           |                        | using           | weak_use_context_feature;weak_cue_without_current_subject                                      | Translation performance was measured using the BLEU score (Papineni et al., 2002) , which measures n-gram overlap with a reference translation.                                      |
| ctxr_e26629ae935ada16333a | unknown              | unclear                    | no_cue                  | unclear             | none                          |         0.2  | none           | no_cue_no_object                                                | False                | False                    | none                   | unknown                         |                |                        |                 | no_cue                                                                                         | Research on error detection has mostly been concerned with function words, such as determiners and prepositions (Leacock et al., 2010; Dale et al., 2012) .                          |
| ctxr_b603a1e2ca89b7bbae13 | unknown              | unclear                    | no_cue                  | unclear             | none                          |         0.2  | none           | no_cue_no_object                                                | False                | False                    | none                   | unknown                         |                |                        |                 | no_cue                                                                                         | Research on error detection has mostly been concerned with function words, such as determiners and prepositions (Leacock et al., 2010; Dale et al., 2012) .                          |
| ctxr_f946ef9a51fa97e2db2e | unknown              | unclear                    | no_cue                  | unclear             | none                          |         0.2  | none           | no_cue_no_object                                                | False                | False                    | none                   | unknown                         |                |                        |                 | no_cue                                                                                         | They have also been shown to be promising models of composition in a number of NLP tasks, including semantic anomaly detection (Vecchi et al., 2011) .                               |
| ctxr_61f00a3b28c59addb75e | unknown              | unclear                    | no_cue                  | unclear             | none                          |         0.2  | none           | no_cue_no_object                                                | False                | False                    | none                   | unknown                         |                |                        |                 | no_cue                                                                                         | The adjective-specific linear maps of Baroni and Zamparelli (2010) take the grammatical functions of the words within a combination into account.                                    |

## Multiple Candidate Intent Examples
| context_id                | normalized_section   | primary_candidate_intent   | phase2_candidate_type           | candidate_intents    | candidate_relation_subtypes   |   confidence | llm_priority   | llm_reason                                | should_send_to_llm   | cited_work_description   | object_type_source   | primary_candidate_object_type   | object_names   | generic_metric_names   | evidence_span    | matched_rules                                                | sentence_text                                                                                                                                                                        |
|:--------------------------|:---------------------|:---------------------------|:--------------------------------|:---------------------|:------------------------------|-------------:|:---------------|:------------------------------------------|:---------------------|:-------------------------|:---------------------|:--------------------------------|:---------------|:-----------------------|:-----------------|:-------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ctxr_1e11c4efff7667aaac0f | unknown              | uses                       | explicit_current_paper_relation | background;uses      | direct_use                    |         0.62 | medium         | explicit_relation_without_object_evidence | True                 | False                    | none                 | unknown                         |                |                        | we use           | background_cue;current_paper_use_cue;dataset_context_feature | In our previous work (Khan et al., 2013) , we showed that we obtain the best results when we use a balanced training corpus with the same number of sentences from the EWT and th... |
| ctxr_56ad9f51105d23c96ad1 | related_work         | critiques                  | explicit_current_paper_relation | background;critiques | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence | True                 | True                     | none                 | unknown                         |                |                        | drawbacks of the | cited_work_description;background_cue;targeted_critique_cue  | As a possible solution to the drawbacks of the pure statistical machine translation (weak on reordering; lack of target language fluency), syntactic approaches were proposed tha... |
| ctxr_bf0b4bf611ada8efce34 | related_work         | critiques                  | explicit_current_paper_relation | background;critiques | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence | True                 | True                     | none                 | unknown                         |                |                        | drawbacks of the | cited_work_description;background_cue;targeted_critique_cue  | As a possible solution to the drawbacks of the pure statistical machine translation (weak on reordering; lack of target language fluency), syntactic approaches were proposed tha... |
| ctxr_3f4b77da44444ee3815f | related_work         | critiques                  | explicit_current_paper_relation | background;critiques | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence | True                 | True                     | none                 | unknown                         |                |                        | drawbacks of the | cited_work_description;background_cue;targeted_critique_cue  | As a possible solution to the drawbacks of the pure statistical machine translation (weak on reordering; lack of target language fluency), syntactic approaches were proposed tha... |
| ctxr_7a6a8ea86f8168b62726 | related_work         | critiques                  | explicit_current_paper_relation | background;critiques | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence | True                 | True                     | none                 | unknown                         |                |                        | drawbacks of the | cited_work_description;background_cue;targeted_critique_cue  | As a possible solution to the drawbacks of the pure statistical machine translation (weak on reordering; lack of target language fluency), syntactic approaches were proposed tha... |
| ctxr_61495d6b3572b3b7b0a6 | related_work         | critiques                  | explicit_current_paper_relation | background;critiques | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence | True                 | True                     | none                 | unknown                         |                |                        | drawbacks of the | cited_work_description;background_cue;targeted_critique_cue  | As a possible solution to the drawbacks of the pure statistical machine translation (weak on reordering; lack of target language fluency), syntactic approaches were proposed tha... |
| ctxr_cc8878dfc0e0046de376 | related_work         | critiques                  | explicit_current_paper_relation | background;critiques | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence | True                 | True                     | none                 | unknown                         |                |                        | drawbacks of the | cited_work_description;background_cue;targeted_critique_cue  | As a possible solution to the drawbacks of the pure statistical machine translation (weak on reordering; lack of target language fluency), syntactic approaches were proposed tha... |
| ctxr_205f922d750c8d8bed22 | related_work         | critiques                  | explicit_current_paper_relation | background;critiques | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence | True                 | True                     | none                 | unknown                         |                |                        | drawbacks of the | cited_work_description;background_cue;targeted_critique_cue  | As a possible solution to the drawbacks of the pure statistical machine translation (weak on reordering; lack of target language fluency), syntactic approaches were proposed tha... |
| ctxr_491de660009417c3a5c3 | related_work         | critiques                  | explicit_current_paper_relation | background;critiques | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence | True                 | True                     | none                 | unknown                         |                |                        | drawbacks of the | cited_work_description;background_cue;targeted_critique_cue  | As a possible solution to the drawbacks of the pure statistical machine translation (weak on reordering; lack of target language fluency), syntactic approaches were proposed tha... |
| ctxr_e3bb7e1608994c9a3fd2 | related_work         | critiques                  | explicit_current_paper_relation | background;critiques | critique_limitation           |         0.65 | medium         | explicit_relation_without_object_evidence | True                 | True                     | none                 | unknown                         |                |                        | drawbacks of the | cited_work_description;background_cue;targeted_critique_cue  | As a possible solution to the drawbacks of the pure statistical machine translation (weak on reordering; lack of target language fluency), syntactic approaches were proposed tha... |

## Object Mention But Background Intent Examples
| context_id                | normalized_section   | primary_candidate_intent   | phase2_candidate_type   | candidate_intents   | candidate_relation_subtypes   |   confidence | llm_priority   | llm_reason                                                                 | should_send_to_llm   | cited_work_description   | object_type_source     | primary_candidate_object_type   | object_names      | generic_metric_names   | evidence_span   | matched_rules                                                                           | sentence_text                                                                                                                                                                        |
|:--------------------------|:---------------------|:---------------------------|:------------------------|:--------------------|:------------------------------|-------------:|:---------------|:---------------------------------------------------------------------------|:---------------------|:-------------------------|:-----------------------|:--------------------------------|:------------------|:-----------------------|:----------------|:----------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ctxr_f6863fcab52657a5c16e | related_work         | background                 | cited_work_description  | background          | none                          |         0.62 | medium         | weak_cue_with_object_mention;cited_work_description_with_high_value_object | True                 | True                     | object_graph_candidate | benchmark_or_protocol           | SemEval           |                        | developed       | cited_work_description;weak_extend_context_feature;weak_use_context_feature             | In (Tratz and Hovy, 2010) the authors developed a system based on the Maximum Entropy classifier, able to detect 10 bidirectional semantic relations Achieved F-measures depended... |
| ctxr_3e4722d1950da619a7dd | unknown              | background                 | cited_work_description  | background          | none                          |         0.62 | medium         | weak_cue_with_object_mention;cited_work_description_with_high_value_object | True                 | True                     | object_graph_candidate | method                          | CRF               |                        | annotated       | cited_work_description;evaluation_context_feature;dataset_context_feature               | We made use of a CRF shallow parser (Radziszewski and Pawlaczek, 2012) trained on an annotated corpus of Polish (KPWr) (Broda et al., 2012) which comprises shallow syntactic ann... |
| ctxr_b4edfcd618c4edc4d4dc | introduction         | background                 | generic_metric_feature  | background          | none                          |         0.35 | medium         | weak_cue_with_object_mention                                               | True                 | False                    | generic_metric_feature | metric                          | accuracy          | accuracy               | Treebank        | generic_metric_feature_only;dataset_context_feature;weak_section_prior:introduction     | We continue our work (Khan et al., 2013) on dependency parsing web data from the English Web Treebank (Bies et al., 2012) .                                                          |
| ctxr_9af9bd56af035c2cee84 | unknown              | background                 | cited_work_description  | background          | none                          |         0.62 | medium         | cited_work_description_with_high_value_object                              | True                 | True                     | generic_metric_feature | metric                          | accuracy          | accuracy               | showed          | cited_work_description;generic_metric_feature_only                                      | Foth and Menzel (2006) showed that WCDG can be augmented by trainable components to raise the accuracy of WCDG.                                                                      |
| ctxr_12dda98b18b7e159cf6c | unknown              | background                 | cited_work_description  | background          | none                          |         0.62 | medium         | cited_work_description_with_high_value_object                              | True                 | True                     | generic_metric_feature | metric                          | accuracy          | accuracy               | used            | cited_work_description;generic_metric_feature_only                                      | This approach has later been used by Khmylko et al. (2009) to integrate MST-Parser (McDonald et al., 2006 ) (which does not work incrementally) as an external data source for WCDG. |
| ctxr_6f4fbb5a1e4f3b2f971a | unknown              | background                 | cited_work_description  | background          | none                          |         0.62 | medium         | cited_work_description_with_high_value_object                              | True                 | True                     | generic_metric_feature | metric                          | accuracy          | accuracy               | used            | cited_work_description;generic_metric_feature_only                                      | This approach has later been used by Khmylko et al. (2009) to integrate MST-Parser (McDonald et al., 2006 ) (which does not work incrementally) as an external data source for WCDG. |
| ctxr_e3dec93bf83ff55bb70a | related_work         | background                 | cited_work_description  | background          | none                          |         0.62 | medium         | cited_work_description_with_high_value_object                              | True                 | True                     | object_graph_candidate | metric                          | ROUGE             |                        | proposed        | cited_work_description;background_cue                                                   | Recently, graph-based ranking methods, such as LexPageRank (Erkan and Radev, 2004) and TextRank (Mihalcea and Tarau, 2004 ), 1 http://haydn.isi.edu/ROUGE/ have been proposed for... |
| ctxr_cbf322775aa793d09591 | related_work         | background                 | cited_work_description  | background          | none                          |         0.62 | medium         | cited_work_description_with_high_value_object                              | True                 | True                     | object_graph_candidate | metric                          | ROUGE             |                        | proposed        | cited_work_description;background_cue                                                   | Recently, graph-based ranking methods, such as LexPageRank (Erkan and Radev, 2004) and TextRank (Mihalcea and Tarau, 2004 ), 1 http://haydn.isi.edu/ROUGE/ have been proposed for... |
| ctxr_7e729e2f9c3e394d22a2 | evaluation           | background                 | cited_work_description  | background          | none                          |         0.62 | medium         | cited_work_description_with_high_value_object                              | True                 | True                     | object_graph_candidate | metric                          | ROUGE             |                        | used            | cited_work_description                                                                  | For the intrinsic evaluation of a large number of summaries, we made use of the ROUGE metrics that has been widely used in automatic evaluation of summarization systems (Lin and... |
| ctxr_bcc118cb881cd6af4c4e | evaluation           | background                 | cited_work_description  | background          | none                          |         0.62 | medium         | cited_work_description_with_high_value_object                              | True                 | True                     | object_graph_candidate | metric                          | ROUGE             |                        | used            | cited_work_description                                                                  | For the intrinsic evaluation of a large number of summaries, we made use of the ROUGE metrics that has been widely used in automatic evaluation of summarization systems (Lin and... |
| ctxr_11a201fb38db6ec2b675 | evaluation           | background                 | cited_work_description  | background          | none                          |         0.62 | medium         | cited_work_description_with_high_value_object                              | True                 | True                     | object_graph_candidate | metric                          | ROUGE             |                        | shown           | cited_work_description;background_cue                                                   | Among them, ROUGE-1 has been shown to agree most with human judgments (Lin and Hovy, 2003) .                                                                                         |
| ctxr_c222d4c1bd43d71f629d | introduction         | background                 | background_prior        | background          | none                          |         0.35 | medium         | background_with_graph_candidate_object                                     | True                 | False                    | object_graph_candidate | dataset_or_database             | PropBank;FrameNet |                        |                 | weak_section_prior:introduction                                                         | Several studies on semantic role labeling (SRL) have been conducted, mainly for English texts with a wide coverage from revealing syntactic and grammatical features that impact ... |
| ctxr_9756d01b7f59460f7acb | introduction         | background                 | background_prior        | background          | none                          |         0.35 | medium         | weak_cue_with_object_mention                                               | True                 | False                    | object_graph_candidate | dataset_or_database             | PropBank;FrameNet |                        | corpora         | dataset_context_feature;weak_section_prior:introduction                                 | This is because current rich language resources are related to annotated corpora with semantic roles such as PropBank (Kingsbury et al., 2002) , FrameNet (Baker et al., 1998) , ... |
| ctxr_344bcf5eb41c21d0081a | introduction         | background                 | background_prior        | background          | none                          |         0.35 | medium         | weak_cue_with_object_mention                                               | True                 | False                    | object_graph_candidate | dataset_or_database             | PropBank;FrameNet |                        | corpora         | dataset_context_feature;weak_section_prior:introduction                                 | This is because current rich language resources are related to annotated corpora with semantic roles such as PropBank (Kingsbury et al., 2002) , FrameNet (Baker et al., 1998) , ... |
| ctxr_bf6577bd218dc6da6e42 | introduction         | background                 | background_prior        | background          | none                          |         0.35 | medium         | weak_cue_with_object_mention                                               | True                 | False                    | object_graph_candidate | dataset_or_database             | FrameNet          |                        | corpora         | dataset_context_feature;weak_section_prior:introduction                                 | This is because large-scale corpora annotated with these three labels have been developed (Kyoto Corpus (Kawahara et al., 2002) and NAIST Text Corpus (Iida et al., 2007) ) and w... |
| ctxr_296955737e98c10a5151 | introduction         | background                 | background_prior        | background          | none                          |         0.35 | medium         | weak_cue_with_object_mention                                               | True                 | False                    | object_graph_candidate | dataset_or_database             | FrameNet          |                        | corpora         | dataset_context_feature;weak_section_prior:introduction                                 | This is because large-scale corpora annotated with these three labels have been developed (Kyoto Corpus (Kawahara et al., 2002) and NAIST Text Corpus (Iida et al., 2007) ) and w... |
| ctxr_b5fe83d862f4395270f0 | experiment           | background                 | cited_work_description  | background          | none                          |         0.62 | medium         | weak_cue_with_object_mention;cited_work_description_with_high_value_object | True                 | True                     | object_graph_candidate | dataset_or_database             | PropBank          |                        | shown           | cited_work_description;dataset_context_feature                                          | The semantic role labels of Theme and Agent were most frequent, which indicates the same tendency shown in PropBank (Palmer et al., 2005) , which is an English semantic-role-lab... |
| ctxr_cb27bb574c756f008de2 | related_work         | background                 | generic_metric_feature  | background          | none                          |         0.35 | medium         | weak_cue_with_object_mention                                               | True                 | False                    | generic_metric_feature | metric                          | accuracy          | accuracy               | improve         | weak_extend_context_feature;generic_metric_feature_only;weak_section_prior:related_work | Gildea and Jurafsky (2002) revealed that several syntactic features, such as parse tree path, phrase type, and voice, can improve the accuracy of a statistical learning model.      |
| ctxr_b3f99b73329db6bbf332 | related_work         | background                 | generic_metric_feature  | background          | none                          |         0.35 | low            | background_with_object_mention                                             | False                | False                    | generic_metric_feature | metric                          | accuracy          | accuracy               |                 | generic_metric_feature_only;weak_section_prior:related_work                             | More detailed features were studied by Surdeanu et al. (2003) and Xue and Palmer (2004) .                                                                                            |
| ctxr_2f5e46e03d46668bbce5 | related_work         | background                 | generic_metric_feature  | background          | none                          |         0.35 | low            | background_with_object_mention                                             | False                | False                    | generic_metric_feature | metric                          | accuracy          | accuracy               |                 | generic_metric_feature_only;weak_section_prior:related_work                             | More detailed features were studied by Surdeanu et al. (2003) and Xue and Palmer (2004) .                                                                                            |

## Object Mention But Unclear Intent Examples
| context_id                | normalized_section   | primary_candidate_intent   | phase2_candidate_type   | candidate_intents   | candidate_relation_subtypes   |   confidence | llm_priority   | llm_reason                                                      | should_send_to_llm   | cited_work_description   | object_type_source     | primary_candidate_object_type   | object_names              | generic_metric_names   | evidence_span   | matched_rules                                                                                  | sentence_text                                                                                                                                                                        |
|:--------------------------|:---------------------|:---------------------------|:------------------------|:--------------------|:------------------------------|-------------:|:---------------|:----------------------------------------------------------------|:---------------------|:-------------------------|:-----------------------|:--------------------------------|:--------------------------|:-----------------------|:----------------|:-----------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ctxr_d573e73d4a69363cdfc0 | results              | unclear                    | generic_metric_feature  | unclear             | none                          |         0.42 | medium         | weak_cue_with_object_mention                                    | True                 | False                    | generic_metric_feature | metric                          | accuracy                  | accuracy               | using           | weak_use_context_feature;generic_metric_feature_only;weak_cue_without_current_subject          | Elsner and Charniak (2011) use coherence models to disentangle chat, using some features (entity grid, topical entity grid) which correspond to the information in our content fe... |
| ctxr_fde2b4fe687323ff4bd3 | experiment           | unclear                    | generic_metric_feature  | unclear             | none                          |         0.35 | low            | generic_metric_feature_only                                     | False                | False                    | generic_metric_feature | metric                          | F1                        | F1                     |                 | generic_metric_feature_only;no_cue                                                             | The evaluation was run with respect to precision, recall, F -measure, and alignment error rate (AER) considering sure and probable alignments but not NULL ones (Mihalcea and Ped... |
| ctxr_d2f7e10dccf772790070 | dataset              | unclear                    | weak_cue_feature        | unclear             | none                          |         0.42 | medium         | weak_cue_with_object_mention                                    | True                 | False                    | object_mention         | dataset_or_database             | Penn Treebank             |                        | using           | weak_use_context_feature;dataset_context_feature;weak_cue_without_current_subject              | The two corpora were converted from PTB constituency trees into dependency trees using the Stanford dependency converter (de Marneffe and Manning, 2008).                            |
| ctxr_26559d1672acccfd09ea | unknown              | unclear                    | generic_metric_feature  | unclear             | none                          |         0.42 | medium         | weak_cue_with_object_mention                                    | True                 | False                    | generic_metric_feature | metric                          | accuracy                  | accuracy               | using           | weak_use_context_feature;generic_metric_feature_only;weak_cue_without_current_subject          | MST is a graph-based parser which optimizes its parse tree globally (McDonald et al., 2005) , using a variety of feature sets, i.e., edge,                                           |
| ctxr_c223321394c5bbc2bcec | unknown              | unclear                    | generic_metric_feature  | unclear             | none                          |         0.35 | low            | generic_metric_feature_only                                     | False                | False                    | generic_metric_feature | metric                          | accuracy                  | accuracy               |                 | generic_metric_feature_only;no_cue                                                             | This corroborates findings by Brants (2000) .                                                                                                                                        |
| ctxr_72089786b736eb3c1d50 | unknown              | unclear                    | generic_metric_feature  | unclear             | report_metric                 |         0.42 | medium         | weak_cue_with_object_mention;generic_metric_with_evaluation_cue | True                 | False                    | generic_metric_feature | metric                          | accuracy                  | accuracy               | experiments on  | generic_metric_with_evaluation_cue;evaluation_context_feature;weak_cue_without_current_subject | Even if we balance the source and target domain data, which proved beneficial in our previous experiments on parsing (Khan et al., 2013) , we reach an accuracy of 93.48%, well b... |
| ctxr_4355448353bdd023508c | unknown              | unclear                    | weak_cue_feature        | unclear             | none                          |         0.42 | medium         | weak_cue_with_object_mention;unclear_with_graph_candidate       | True                 | False                    | object_graph_candidate | software_or_tool                | GIZA++                    |                        | corpora         | dataset_context_feature;weak_cue_without_current_subject                                       | The field of statistical machine translation has been blessed with a long tradition of freely available software tools -such as GIZA++ (Och and Ney, 2003) -and parallel corpora ... |
| ctxr_e68e33d8515b22b2c3ce | results              | unclear                    | weak_cue_feature        | unclear             | none                          |         0.42 | medium         | weak_cue_with_object_mention;unclear_with_graph_candidate       | True                 | False                    | object_graph_candidate | metric                          | BLEU                      |                        | using           | weak_use_context_feature;weak_cue_without_current_subject                                      | Translation performance was measured using the BLEU score (Papineni et al., 2002) , which measures n-gram overlap with a reference translation.                                      |
| ctxr_e4bd8b3cb291ec3f4e15 | method               | unclear                    | weak_cue_feature        | unclear             | none                          |         0.42 | medium         | weak_cue_with_object_mention;unclear_with_graph_candidate       | True                 | False                    | object_graph_candidate | software_or_tool                | GIZA++                    |                        | using           | weak_use_context_feature;weak_cue_without_current_subject                                      | Once the training data was preprocessed, a wordto-word alignment was performed in both directions, source-to-target and target-to-source, by using GIZA++ (Och and Ney, 2000) .      |
| ctxr_99f7530c7394c4ee6f33 | method               | unclear                    | object_only_unclear     | unclear             | none                          |         0.35 | medium         | unclear_with_graph_candidate                                    | True                 | False                    | object_graph_candidate | metric                          | BLEU                      |                        |                 | no_cue                                                                                         | This algorithm adjusts the log-linear weights so that BLEU (Papineni et al., 2002) is maximized over a given development set.                                                        |
| ctxr_1348abfe0d9ee416094f | dataset              | unclear                    | generic_metric_feature  | unclear             | none                          |         0.42 | medium         | weak_cue_with_object_mention                                    | True                 | False                    | generic_metric_feature | metric                          | accuracy                  | accuracy               | using           | weak_use_context_feature;generic_metric_feature_only;weak_cue_without_current_subject          | Our bilingual dictionary is noisy, because it was automatically generated using a pivot language (Varga and Yokoyama, 2007) .                                                        |
| ctxr_9ecca4bac0344e435a50 | unknown              | unclear                    | generic_metric_feature  | unclear             | none                          |         0.35 | low            | generic_metric_feature_only                                     | False                | False                    | generic_metric_feature | metric                          | accuracy                  | accuracy               |                 | generic_metric_feature_only;no_cue                                                             | One of the components was a shift-reduce parser modeled after Nivre (2003) , which was the first description of the MaltParser architecture.                                         |
| ctxr_448d50f47d83c101d92f | unknown              | unclear                    | generic_metric_feature  | unclear             | none                          |         0.35 | low            | generic_metric_feature_only                                     | False                | False                    | generic_metric_feature | metric                          | accuracy                  | accuracy               |                 | generic_metric_feature_only;no_cue                                                             | As a delay is not acceptable for our application scenario, we will use MaltParser and the TnT tagger (Brants, 2000) without lookahead despite their inferior accuracy in that mod... |
| ctxr_fc364de7c4a52b630606 | evaluation           | unclear                    | object_only_unclear     | unclear             | none                          |         0.35 | medium         | unclear_with_graph_candidate                                    | True                 | False                    | object_graph_candidate | metric                          | ROUGE                     |                        |                 | no_cue                                                                                         | We computed three ROUGE measures for each summary, namely ROUGE-1 (unigram based), ROUGE-2 (bigram based) and (Lin and Hovy, 2003) .                                                 |
| ctxr_059fae894b25c9864d24 | experiment           | unclear                    | weak_cue_feature        | unclear             | none                          |         0.42 | medium         | weak_cue_with_object_mention;unclear_with_graph_candidate       | True                 | False                    | object_graph_candidate | software_or_tool                | GIZA++                    |                        | using           | weak_use_context_feature;weak_cue_without_current_subject                                      | We train IBM Model 4 with a scheme of 1 7 2 0 h 7 3 0 4 3 using GIZA++ (Och and Ney, 2003) .                                                                                         |
| ctxr_54f5835f3a453d286c07 | model                | unclear                    | object_only_unclear     | unclear             | none                          |         0.35 | medium         | unclear_with_graph_candidate                                    | True                 | False                    | object_graph_candidate | software_or_tool                | GIZA++                    |                        |                 | no_cue                                                                                         | This was partially investigated in the framework of pivot translation to produce artificially bitexts in another language (Bertoldi et al., 2008) .                                  |
| ctxr_977bba59559518243ba7 | results              | unclear                    | object_only_unclear     | unclear             | none                          |         0.35 | medium         | unclear_with_graph_candidate                                    | True                 | False                    | object_graph_candidate | metric                          | BLEU                      |                        |                 | no_cue                                                                                         | The BLEU scores (Papineni et al., 2002) Table 1 .                                                                                                                                    |
| ctxr_5cf962d606f5bb683922 | unknown              | unclear                    | object_only_unclear     | unclear             | none                          |         0.35 | medium         | unclear_with_graph_candidate                                    | True                 | False                    | object_graph_candidate | metric                          | BLEU                      |                        |                 | no_cue                                                                                         | The results, also displayed in Table 1 , show that this approach can lead to slight improvements of the BLEU score, which however turn out not to be statistically sigificant in ... |
| ctxr_8e8837d4ace18526bebf | dataset              | unclear                    | object_only_unclear     | unclear             | none                          |         0.35 | medium         | unclear_with_graph_candidate                                    | True                 | False                    | object_graph_candidate | dataset_or_database             | FrameNet;WordNet;PropBank |                        |                 | no_cue                                                                                         | From the view of previous lexical databases In English, several well-considered lexical databases are available, e.g., EVCA, Dorr's LCS (Dorr, 1997 ), FrameNet, WordNet (Fellbau... |
| ctxr_a9b33c3ed7a11a859b50 | dataset              | unclear                    | weak_cue_feature        | unclear             | none                          |         0.42 | medium         | weak_cue_with_object_mention;unclear_with_graph_candidate       | True                 | False                    | object_graph_candidate | dataset_or_database             | FrameNet;WordNet;PropBank |                        | Treebank        | dataset_context_feature;weak_cue_without_current_subject                                       | Besides there is the research project (Pustejovsky and Meyers, 2005) to Ànd general descriptional framework of predicate argument structure by merging several lexical databases ... |

## No Cue But Object Mention Examples
| context_id                | normalized_section   | primary_candidate_intent   | phase2_candidate_type   | candidate_intents   | candidate_relation_subtypes   |   confidence | llm_priority   | llm_reason                             | should_send_to_llm   | cited_work_description   | object_type_source     | primary_candidate_object_type   | object_names      | generic_metric_names   | evidence_span   | matched_rules                                               | sentence_text                                                                                                                                                                        |
|:--------------------------|:---------------------|:---------------------------|:------------------------|:--------------------|:------------------------------|-------------:|:---------------|:---------------------------------------|:---------------------|:-------------------------|:-----------------------|:--------------------------------|:------------------|:-----------------------|:----------------|:------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ctxr_fde2b4fe687323ff4bd3 | experiment           | unclear                    | generic_metric_feature  | unclear             | none                          |         0.35 | low            | generic_metric_feature_only            | False                | False                    | generic_metric_feature | metric                          | F1                | F1                     |                 | generic_metric_feature_only;no_cue                          | The evaluation was run with respect to precision, recall, F -measure, and alignment error rate (AER) considering sure and probable alignments but not NULL ones (Mihalcea and Ped... |
| ctxr_c223321394c5bbc2bcec | unknown              | unclear                    | generic_metric_feature  | unclear             | none                          |         0.35 | low            | generic_metric_feature_only            | False                | False                    | generic_metric_feature | metric                          | accuracy          | accuracy               |                 | generic_metric_feature_only;no_cue                          | This corroborates findings by Brants (2000) .                                                                                                                                        |
| ctxr_99f7530c7394c4ee6f33 | method               | unclear                    | object_only_unclear     | unclear             | none                          |         0.35 | medium         | unclear_with_graph_candidate           | True                 | False                    | object_graph_candidate | metric                          | BLEU              |                        |                 | no_cue                                                      | This algorithm adjusts the log-linear weights so that BLEU (Papineni et al., 2002) is maximized over a given development set.                                                        |
| ctxr_9ecca4bac0344e435a50 | unknown              | unclear                    | generic_metric_feature  | unclear             | none                          |         0.35 | low            | generic_metric_feature_only            | False                | False                    | generic_metric_feature | metric                          | accuracy          | accuracy               |                 | generic_metric_feature_only;no_cue                          | One of the components was a shift-reduce parser modeled after Nivre (2003) , which was the first description of the MaltParser architecture.                                         |
| ctxr_448d50f47d83c101d92f | unknown              | unclear                    | generic_metric_feature  | unclear             | none                          |         0.35 | low            | generic_metric_feature_only            | False                | False                    | generic_metric_feature | metric                          | accuracy          | accuracy               |                 | generic_metric_feature_only;no_cue                          | As a delay is not acceptable for our application scenario, we will use MaltParser and the TnT tagger (Brants, 2000) without lookahead despite their inferior accuracy in that mod... |
| ctxr_fc364de7c4a52b630606 | evaluation           | unclear                    | object_only_unclear     | unclear             | none                          |         0.35 | medium         | unclear_with_graph_candidate           | True                 | False                    | object_graph_candidate | metric                          | ROUGE             |                        |                 | no_cue                                                      | We computed three ROUGE measures for each summary, namely ROUGE-1 (unigram based), ROUGE-2 (bigram based) and (Lin and Hovy, 2003) .                                                 |
| ctxr_c222d4c1bd43d71f629d | introduction         | background                 | background_prior        | background          | none                          |         0.35 | medium         | background_with_graph_candidate_object | True                 | False                    | object_graph_candidate | dataset_or_database             | PropBank;FrameNet |                        |                 | weak_section_prior:introduction                             | Several studies on semantic role labeling (SRL) have been conducted, mainly for English texts with a wide coverage from revealing syntactic and grammatical features that impact ... |
| ctxr_b3f99b73329db6bbf332 | related_work         | background                 | generic_metric_feature  | background          | none                          |         0.35 | low            | background_with_object_mention         | False                | False                    | generic_metric_feature | metric                          | accuracy          | accuracy               |                 | generic_metric_feature_only;weak_section_prior:related_work | More detailed features were studied by Surdeanu et al. (2003) and Xue and Palmer (2004) .                                                                                            |
| ctxr_2f5e46e03d46668bbce5 | related_work         | background                 | generic_metric_feature  | background          | none                          |         0.35 | low            | background_with_object_mention         | False                | False                    | generic_metric_feature | metric                          | accuracy          | accuracy               |                 | generic_metric_feature_only;weak_section_prior:related_work | More detailed features were studied by Surdeanu et al. (2003) and Xue and Palmer (2004) .                                                                                            |
| ctxr_e29d4de098ff144543d9 | related_work         | background                 | background_prior        | background          | none                          |         0.35 | medium         | background_with_graph_candidate_object | True                 | False                    | object_graph_candidate | model                           | LSTM              |                        |                 | weak_section_prior:related_work                             | The dependency path is convenient, but He et al. (2017) revealed that higher accuracies on neural-network-based SRL models could be obtained if correct parsed information is ava... |

## LLM Flagged Examples
| context_id                | normalized_section   | primary_candidate_intent   | phase2_candidate_type           | candidate_intents   | candidate_relation_subtypes   |   confidence | llm_priority   | llm_reason                                                                 | should_send_to_llm   | cited_work_description   | object_type_source     | primary_candidate_object_type   | object_names    | generic_metric_names   | evidence_span   | matched_rules                                                                         | sentence_text                                                                                                                                                                        |
|:--------------------------|:---------------------|:---------------------------|:--------------------------------|:--------------------|:------------------------------|-------------:|:---------------|:---------------------------------------------------------------------------|:---------------------|:-------------------------|:-----------------------|:--------------------------------|:----------------|:-----------------------|:----------------|:--------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ctxr_d573e73d4a69363cdfc0 | results              | unclear                    | generic_metric_feature          | unclear             | none                          |         0.42 | medium         | weak_cue_with_object_mention                                               | True                 | False                    | generic_metric_feature | metric                          | accuracy        | accuracy               | using           | weak_use_context_feature;generic_metric_feature_only;weak_cue_without_current_subject | Elsner and Charniak (2011) use coherence models to disentangle chat, using some features (entity grid, topical entity grid) which correspond to the information in our content fe... |
| ctxr_f6863fcab52657a5c16e | related_work         | background                 | cited_work_description          | background          | none                          |         0.62 | medium         | weak_cue_with_object_mention;cited_work_description_with_high_value_object | True                 | True                     | object_graph_candidate | benchmark_or_protocol           | SemEval         |                        | developed       | cited_work_description;weak_extend_context_feature;weak_use_context_feature           | In (Tratz and Hovy, 2010) the authors developed a system based on the Maximum Entropy classifier, able to detect 10 bidirectional semantic relations Achieved F-measures depended... |
| ctxr_3e4722d1950da619a7dd | unknown              | background                 | cited_work_description          | background          | none                          |         0.62 | medium         | weak_cue_with_object_mention;cited_work_description_with_high_value_object | True                 | True                     | object_graph_candidate | method                          | CRF             |                        | annotated       | cited_work_description;evaluation_context_feature;dataset_context_feature             | We made use of a CRF shallow parser (Radziszewski and Pawlaczek, 2012) trained on an annotated corpus of Polish (KPWr) (Broda et al., 2012) which comprises shallow syntactic ann... |
| ctxr_5d4459ab2a2de3c5c83b | evaluation           | compares_against           | explicit_current_paper_relation | compares_against    | compare_against               |         0.65 | medium         | explicit_relation_without_object_evidence                                  | True                 | False                    | none                   | unknown                         |                 |                        | compared to     | explicit_compare_cue                                                                  | Despite of its performance, LIHLA has some advantages when compared to other lexical alignment methods found in the literature, such as: it does not need to be trained for a new... |
| ctxr_794ff11af106441610a2 | model                | uses                       | explicit_current_paper_relation | uses                | direct_use                    |         0.9  | high           | explicit_current_relation_with_strong_object                               | True                 | False                    | object_graph_candidate | metric                          | perplexity;BLEU | perplexity             | we use          | weak_extend_context_feature;current_paper_use_cue;generic_metric_feature_only         | Since the space of different combinations is too large to be searched exhaustively, we use a guided search procedure based on Genetic Algorithms (Duh and Kirchhoff, 2004) , whic... |
| ctxr_b4edfcd618c4edc4d4dc | introduction         | background                 | generic_metric_feature          | background          | none                          |         0.35 | medium         | weak_cue_with_object_mention                                               | True                 | False                    | generic_metric_feature | metric                          | accuracy        | accuracy               | Treebank        | generic_metric_feature_only;dataset_context_feature;weak_section_prior:introduction   | We continue our work (Khan et al., 2013) on dependency parsing web data from the English Web Treebank (Bies et al., 2012) .                                                          |
| ctxr_caa50477f333d1e3c48b | dataset              | uses                       | explicit_current_paper_relation | uses                | direct_use                    |         0.9  | high           | explicit_current_relation_with_strong_object                               | True                 | False                    | object_graph_candidate | dataset_or_database             | Penn Treebank   |                        | we use          | current_paper_use_cue;dataset_context_feature                                         | For our experiments, we use two main resources, the Wall Street Journal (WSJ) portion of the Penn Treebank (PTB) (Marcus et al., 1993) and the English Web Treebank (EWT) (Bies e... |
| ctxr_d2f7e10dccf772790070 | dataset              | unclear                    | weak_cue_feature                | unclear             | none                          |         0.42 | medium         | weak_cue_with_object_mention                                               | True                 | False                    | object_mention         | dataset_or_database             | Penn Treebank   |                        | using           | weak_use_context_feature;dataset_context_feature;weak_cue_without_current_subject     | The two corpora were converted from PTB constituency trees into dependency trees using the Stanford dependency converter (de Marneffe and Manning, 2008).                            |
| ctxr_a7ac70660d93318c89cc | unknown              | uses                       | explicit_current_paper_relation | uses                | direct_use                    |         0.62 | medium         | explicit_relation_without_object_evidence                                  | True                 | False                    | none                   | unknown                         |                 |                        | We use          | current_paper_use_cue                                                                 | We use TnT (Brants, 2000) , a Markov model POS tagger using a trigram model.                                                                                                         |
| ctxr_26559d1672acccfd09ea | unknown              | unclear                    | generic_metric_feature          | unclear             | none                          |         0.42 | medium         | weak_cue_with_object_mention                                               | True                 | False                    | generic_metric_feature | metric                          | accuracy        | accuracy               | using           | weak_use_context_feature;generic_metric_feature_only;weak_cue_without_current_subject | MST is a graph-based parser which optimizes its parse tree globally (McDonald et al., 2005) , using a variety of feature sets, i.e., edge,                                           |
