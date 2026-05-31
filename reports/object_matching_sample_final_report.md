# Object Matching Sample Final Report

## Outputs
- Final mentions: `data/processed/object_mentions_sample_final.parquet`
- Final cited-title profiles: `data/processed/cited_title_object_profiles_sample_final.parquet`
- Object graph candidates: `data/processed/object_graph_candidate_mentions_sample.parquet`

## Core Metrics
| metric | value |
| --- | --- |
| input contexts | 10870 |
| mentions after final policy | 15993 |
| cited title profile count | 3425 |
| graph eligible count | 12988 |
| phase1 feature eligible count | 15879 |
| strict graph candidate count | 8454 |
| broad graph candidate count | 4525 |
| graph candidate rows | 12979 |

## Mention Correct Distribution
| mention_correct | mentions |
| --- | --- |
| unreviewed | 15764 |
| true | 196 |
| false | 30 |
| unclear | 3 |

## Graph Eligible Distribution
| graph_eligible | mentions |
| --- | --- |
| True | 12988 |
| False | 3005 |

## Phase-1 Feature Eligible Distribution
| phase1_feature_eligible | mentions |
| --- | --- |
| True | 15879 |
| False | 114 |

## Graph Candidate Level Distribution
| graph_candidate_level | mentions |
| --- | --- |
| strict | 8454 |
| broad | 4525 |
| none | 3014 |

## Mentions By Object Category
| object_category | mentions |
| --- | --- |
| named_object | 13529 |
| generic_metric | 2183 |
| generic_architecture | 239 |
| ambiguous_short_alias | 42 |

## Top Named Objects
| object_id | canonical_name | object_type | mentions |
| --- | --- | --- | --- |
| obj_bleu | BLEU | metric | 1893 |
| obj_crf | CRF | method | 1403 |
| obj_bert | BERT | model | 1056 |
| obj_lstm | LSTM | model | 1033 |
| obj_wordnet | WordNet | dataset_or_database | 992 |
| obj_moses | Moses | software_or_tool | 811 |
| obj_penn_treebank | Penn Treebank | dataset_or_database | 759 |
| obj_giza | GIZA++ | software_or_tool | 653 |
| obj_semeval | SemEval | benchmark_or_protocol | 560 |
| obj_hmm | HMM | method | 556 |
| obj_transformer | Transformer | model | 548 |
| obj_seq2seq | seq2seq | model | 519 |
| obj_wmt | WMT | benchmark_or_protocol | 397 |
| obj_meteor | METEOR | metric | 297 |
| obj_word2vec | word2vec | model | 273 |
| obj_framenet | FrameNet | dataset_or_database | 271 |
| obj_rouge | ROUGE | metric | 194 |
| obj_attention_mechanism | attention mechanism | method | 186 |
| obj_propbank | PropBank | dataset_or_database | 174 |
| obj_glove | GloVe | model | 160 |
| obj_elmo | ELMo | model | 153 |
| obj_conll_2003 | CoNLL-2003 | benchmark_or_protocol | 106 |
| obj_squad | SQuAD | dataset_or_database | 96 |
| obj_ontonotes | OntoNotes | dataset_or_database | 81 |
| obj_opus | OPUS | software_or_tool | 78 |
| obj_stanford_corenlp | Stanford CoreNLP | software_or_tool | 77 |
| obj_glue | GLUE | benchmark_or_protocol | 48 |
| obj_nltk | NLTK | software_or_tool | 45 |
| obj_snli | SNLI | dataset_or_database | 43 |
| obj_conll_2012 | CoNLL-2012 | benchmark_or_protocol | 31 |

## Top Generic Metrics
| object_id | canonical_name | surface_form | mentions |
| --- | --- | --- | --- |
| obj_accuracy | accuracy | accuracy | 1399 |
| obj_f1 | F1 | F1 | 207 |
| obj_perplexity | perplexity | perplexity | 163 |
| obj_f1 | F1 | F-score | 137 |
| obj_f1 | F1 | F-measure | 110 |
| obj_f1 | F1 | F1 score | 47 |
| obj_f1 | F1 | F1-score | 45 |
| obj_accuracy | accuracy | Accuracy | 30 |
| obj_accuracy | accuracy | classification accuracy | 21 |
| obj_perplexity | perplexity | Perplexity | 10 |
| obj_f1 | F1 | F -measure | 6 |
| obj_perplexity | perplexity | PPL | 3 |
| obj_f1 | F1 | F measure | 2 |
| obj_perplexity | perplexity | ppl | 2 |
| obj_f1 | F1 | F score | 1 |

## Top Ambiguous Aliases
| object_id | canonical_name | surface_form | policy_reason | mentions |
| --- | --- | --- | --- | --- |
| obj_penn_treebank | Penn Treebank | PTB | ptb_context_cue_missing | 30 |
| obj_penn_treebank | Penn Treebank | PTB | llm_graph_signal;llm_phase1_signal;mention_not_correct;ptb_context_cue_missing | 8 |
| obj_penn_treebank | Penn Treebank | PTB | llm_graph_signal;llm_phase1_signal;ptb_context_cue_missing | 4 |

## PTB Examples After Policy
| context_id | canonical_name | object_category | surface_form | confidence | matched_in | mention_correct | graph_eligible | phase1_feature_eligible | graph_candidate_level | policy_reason | match_policy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_caa50477f333d1e3c48b | Penn Treebank | named_object | Penn Treebank | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | context_cue_present |
| ctxr_caa50477f333d1e3c48b | Penn Treebank | named_object | PTB | 0.95 | sentence_text | unreviewed | True | True | strict | ptb_context_cue_present | context_cue_present |
| ctxr_d2f7e10dccf772790070 | Penn Treebank | ambiguous_short_alias | PTB | 0.5 | sentence_text | false | False | False | none | llm_graph_signal;llm_phase1_signal;mention_not_correct;ptb_context_cue_missing | weak_context_cue_missing;require_context_cue |
| ctxr_2979ac016ccbda9a9d17 | Penn Treebank | named_object | Penn Treebank | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | context_cue_present |
| ctxr_d544de6c0a2ad003d1d6 | Penn Treebank | named_object | Penn Treebank | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | context_cue_present |
| ctxr_6edb0510d2fe095b579b | Penn Treebank | named_object | Penn Treebank | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | context_cue_present |
| ctxr_96c4a8a9b4fc7f241235 | Penn Treebank | named_object | Penn Treebank | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | context_cue_present |
| ctxr_ad2f6a927842f44ff3de | Penn Treebank | named_object | Penn Treebank | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | context_cue_present |
| ctxr_859c265421edb55fcafa | Penn Treebank | named_object | Penn Treebank | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | context_cue_present |
| ctxr_7ab4579c8192ce5c7d30 | Penn Treebank | named_object | Penn Treebank | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | context_cue_present |
| ctxr_571fd66b4a9222ffeaf3 | Penn Treebank | named_object | Penn Treebank | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | context_cue_present |
| ctxr_5cdd1425eccbb2fd4583 | Penn Treebank | named_object | Penn Treebank | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | context_cue_present |
| ctxr_1d96f3b8f6d608ba9df5 | Penn Treebank | named_object | Penn Treebank | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | context_cue_present |
| ctxr_ad6d5cba1986347247a5 | Penn Treebank | named_object | Penn Treebank | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | context_cue_present |
| ctxr_57e6bb7cb2e848b60c49 | Penn Treebank | named_object | Penn Treebank | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | context_cue_present |
| ctxr_b03d94651701398d2c00 | Penn Treebank | named_object | Penn Treebank | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | context_cue_present |
| ctxr_e38f3d0b439d3318c906 | Penn Treebank | named_object | Penn Treebank | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | context_cue_present |
| ctxr_113b4eaa85c8aa049d19 | Penn Treebank | named_object | Penn Treebank | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | context_cue_present |
| ctxr_5df42d9042b6967e047d | Penn Treebank | named_object | Penn Treebank | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | context_cue_present |
| ctxr_e539f13709c19a79e9f4 | Penn Treebank | named_object | Penn Treebank | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | context_cue_present |

## Transformer Examples After Policy
| context_id | canonical_name | object_category | surface_form | confidence | matched_in | mention_correct | graph_eligible | phase1_feature_eligible | graph_candidate_level | policy_reason | match_policy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_aa1b7e3f43fffb4f92b0 | Transformer | generic_architecture | transformer | 0.55 | context_window_neighbor | unreviewed | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture;neighbor_context_match |
| ctxr_ab7617f2f9592a20ff6a | Transformer | named_object | Transformers | 0.85 | context_window_neighbor | unreviewed | True | True | broad | default_policy | standard;neighbor_context_match |
| ctxr_7be2d2360c50b43f3fcd | Transformer | named_object | Transformers | 0.85 | context_window_neighbor | unreviewed | True | True | broad | default_policy | standard;neighbor_context_match |
| ctxr_082cd21660027a05e63f | Transformer | named_object | Transformers | 0.85 | context_window_neighbor | unreviewed | True | True | broad | default_policy | standard;neighbor_context_match |
| ctxr_89e33f91e0ca4aa47fe6 | Transformer | named_object | Transformers | 0.85 | context_window_neighbor | unreviewed | True | True | broad | default_policy | standard;neighbor_context_match |
| ctxr_8a018d33416b7ece9ac6 | Transformer | named_object | Transformers | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | standard |
| ctxr_11674fda9622e62cf411 | Transformer | named_object | Transformers | 0.85 | context_window_neighbor | unreviewed | True | True | broad | default_policy | standard;neighbor_context_match |
| ctxr_29fb8dc8cb651ec8b717 | Transformer | named_object | Transformer | 0.85 | context_window_neighbor | unreviewed | True | True | broad | default_policy | standard;neighbor_context_match |
| ctxr_d8985cbc91aaf9f28e3f | Transformer | named_object | Transformers | 0.85 | context_window_neighbor | unreviewed | True | True | broad | default_policy | standard;neighbor_context_match |
| ctxr_bbb1ce2f4d76174a40a8 | Transformer | generic_architecture | transformer | 0.65 | sentence_text | unreviewed | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture |
| ctxr_f046d453884a870316f0 | Transformer | named_object | transformer model | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | standard |
| ctxr_5aac81c6d759c1e1a986 | Transformer | named_object | transformer model | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | standard |
| ctxr_686b28273ac8dd11a1b3 | Transformer | generic_architecture | transformer | 0.65 | sentence_text | unreviewed | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture |
| ctxr_65fdc1db1863225e9bf2 | Transformer | generic_architecture | transformer | 0.65 | sentence_text | true | False | True | none | llm_graph_signal;llm_phase1_signal;lowercase_transformer_feature_only | lowercase_generic_architecture |
| ctxr_0f075d7177b37dcc6ea4 | Transformer | generic_architecture | transformer | 0.65 | sentence_text | unreviewed | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture |
| ctxr_97857c8cfe503e3e220c | Transformer | generic_architecture | transformer | 0.65 | sentence_text | unreviewed | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture |
| ctxr_74fb2d78af593db2157e | Transformer | named_object | transformer architecture | 0.85 | context_window_neighbor | unreviewed | True | True | broad | default_policy | standard;neighbor_context_match |
| ctxr_1a5cc7b3721802ef8458 | Transformer | named_object | transformer architecture | 0.85 | context_window_neighbor | unreviewed | True | True | broad | default_policy | standard;neighbor_context_match |
| ctxr_78d18bccd45aa0b5bf41 | Transformer | named_object | transformer architecture | 0.85 | context_window_neighbor | unreviewed | True | True | broad | default_policy | standard;neighbor_context_match |
| ctxr_95ed71dd70a95cc93060 | Transformer | named_object | transformer architecture | 0.85 | context_window_neighbor | unreviewed | True | True | broad | default_policy | standard;neighbor_context_match |

## seq2seq Examples After Policy
| context_id | canonical_name | object_category | surface_form | confidence | matched_in | mention_correct | graph_eligible | phase1_feature_eligible | graph_candidate_level | policy_reason | match_policy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_f8dcc633c98228a064d4 | seq2seq | named_object | sequence-to-sequence | 0.85 | context_window_neighbor | unreviewed | False | True | none | seq2seq_context_cue_missing | standard;neighbor_context_match;require_context_cue |
| ctxr_510b44c52aa7f5d8c1e4 | seq2seq | named_object | seq2seq | 0.85 | sentence_text | unreviewed | False | True | none | seq2seq_context_cue_missing | standard;require_context_cue |
| ctxr_b6f126193997ab840ece | seq2seq | named_object | seq2seq | 0.85 | sentence_text | unreviewed | False | True | none | seq2seq_context_cue_missing | standard;require_context_cue |
| ctxr_d8a8f729eac30739b9bb | seq2seq | named_object | seq2seq | 0.85 | sentence_text | unreviewed | False | True | none | seq2seq_context_cue_missing | standard;require_context_cue |
| ctxr_869a0ebf2573f5cc9855 | seq2seq | named_object | seq2seq | 0.85 | sentence_text | unreviewed | False | True | none | seq2seq_context_cue_missing | standard;require_context_cue |
| ctxr_e30badd9abe205b9b24c | seq2seq | named_object | seq2seq | 0.85 | sentence_text | unreviewed | False | True | none | seq2seq_context_cue_missing | standard;require_context_cue |
| ctxr_4d5a6ae64d3722d3981d | seq2seq | named_object | seq2seq | 0.85 | sentence_text | unreviewed | False | True | none | seq2seq_context_cue_missing | standard;require_context_cue |
| ctxr_7411a8bdc389811286d8 | seq2seq | named_object | seq2seq | 0.85 | sentence_text | unreviewed | False | True | none | seq2seq_context_cue_missing | standard;require_context_cue |
| ctxr_c1a557bcb858aef9f904 | seq2seq | named_object | seq2seq | 0.85 | sentence_text | unreviewed | False | True | none | seq2seq_context_cue_missing | standard;require_context_cue |
| ctxr_38652b77e41dd4a6cb05 | seq2seq | named_object | seq2seq | 0.85 | context_window_neighbor | unreviewed | False | True | none | seq2seq_context_cue_missing | standard;neighbor_context_match;require_context_cue |
| ctxr_29fb8dc8cb651ec8b717 | seq2seq | named_object | Seq2Seq | 0.85 | sentence_text | unreviewed | False | True | none | seq2seq_context_cue_missing | standard;require_context_cue |
| ctxr_b3abb75cd988299e374a | seq2seq | named_object | encoder-decoder | 0.85 | sentence_text | unreviewed | False | True | none | seq2seq_context_cue_missing | standard;require_context_cue |
| ctxr_fd8ae860bb1047e0ec7d | seq2seq | named_object | encoder-decoder | 0.85 | context_window_neighbor | unreviewed | False | True | none | seq2seq_context_cue_missing | standard;neighbor_context_match;require_context_cue |
| ctxr_0902c9c5db455e4d34f8 | seq2seq | named_object | encoder-decoder | 0.85 | context_window_neighbor | unreviewed | False | True | none | seq2seq_context_cue_missing | standard;neighbor_context_match;require_context_cue |
| ctxr_0902c9c5db455e4d34f8 | seq2seq | named_object | seq2seq | 0.85 | context_window_neighbor | unreviewed | False | True | none | seq2seq_context_cue_missing | standard;neighbor_context_match;require_context_cue |
| ctxr_65fdc1db1863225e9bf2 | seq2seq | named_object | seq2seq | 0.85 | context_window_neighbor | unreviewed | False | True | none | seq2seq_context_cue_missing | standard;neighbor_context_match;require_context_cue |
| ctxr_0f075d7177b37dcc6ea4 | seq2seq | named_object | seq2seq | 0.85 | sentence_text | unreviewed | False | True | none | seq2seq_context_cue_missing | standard;require_context_cue |
| ctxr_14243579effcdcfe8d1a | seq2seq | named_object | seq2seq | 0.85 | sentence_text | unreviewed | False | True | none | seq2seq_context_cue_missing | standard;require_context_cue |
| ctxr_14243579effcdcfe8d1a | seq2seq | named_object | seq2seq | 0.85 | sentence_text | unreviewed | False | True | none | seq2seq_context_cue_missing | standard;require_context_cue |
| ctxr_6c4b8d1fa22b2270218b | seq2seq | named_object | seq2seq | 0.85 | sentence_text | unreviewed | False | True | none | seq2seq_context_cue_missing | standard;require_context_cue |

## Examples Excluded From Graph But Kept As Features
| context_id | canonical_name | object_category | surface_form | confidence | matched_in | mention_correct | graph_eligible | phase1_feature_eligible | graph_candidate_level | policy_reason | match_policy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_d573e73d4a69363cdfc0 | accuracy | generic_metric | accuracy | 0.6 | context_window_neighbor | unreviewed | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match |
| ctxr_fde2b4fe687323ff4bd3 | F1 | generic_metric | F -measure | 0.7 | sentence_text | unreviewed | False | True | none | generic_metric_feature_only | generic_metric |
| ctxr_794ff11af106441610a2 | perplexity | generic_metric | perplexity | 0.6 | context_window_neighbor | unreviewed | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match |
| ctxr_b4edfcd618c4edc4d4dc | accuracy | generic_metric | accuracy | 0.6 | context_window_neighbor | unreviewed | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match |
| ctxr_f7c720ac514891b21f33 | accuracy | generic_metric | accuracy | 0.7 | sentence_text | unreviewed | False | True | none | generic_metric_feature_only | generic_metric |
| ctxr_26559d1672acccfd09ea | accuracy | generic_metric | accuracy | 0.6 | context_window_neighbor | unreviewed | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match |
| ctxr_c223321394c5bbc2bcec | accuracy | generic_metric | accuracy | 0.6 | context_window_neighbor | unreviewed | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match |
| ctxr_c223321394c5bbc2bcec | accuracy | generic_metric | accuracy | 0.6 | context_window_neighbor | unreviewed | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match |
| ctxr_72089786b736eb3c1d50 | accuracy | generic_metric | accuracy | 0.7 | sentence_text | unreviewed | False | True | none | generic_metric_feature_only | generic_metric |
| ctxr_1348abfe0d9ee416094f | accuracy | generic_metric | accuracy | 0.6 | context_window_neighbor | unreviewed | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match |
| ctxr_9af9bd56af035c2cee84 | accuracy | generic_metric | accuracy | 0.7 | sentence_text | unreviewed | False | True | none | generic_metric_feature_only | generic_metric |
| ctxr_9ecca4bac0344e435a50 | accuracy | generic_metric | accuracy | 0.6 | context_window_neighbor | unreviewed | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match |
| ctxr_9ecca4bac0344e435a50 | accuracy | generic_metric | accuracy | 0.6 | context_window_neighbor | unreviewed | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match |
| ctxr_12dda98b18b7e159cf6c | accuracy | generic_metric | accuracy | 0.6 | context_window_neighbor | unreviewed | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match |
| ctxr_12dda98b18b7e159cf6c | accuracy | generic_metric | accuracy | 0.6 | context_window_neighbor | unreviewed | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match |
| ctxr_6f4fbb5a1e4f3b2f971a | accuracy | generic_metric | accuracy | 0.6 | context_window_neighbor | true | False | True | none | llm_graph_signal;llm_phase1_signal;generic_metric_feature_only | generic_metric;neighbor_context_match |
| ctxr_6f4fbb5a1e4f3b2f971a | accuracy | generic_metric | accuracy | 0.6 | context_window_neighbor | true | False | True | none | llm_graph_signal;llm_phase1_signal;generic_metric_feature_only | generic_metric;neighbor_context_match |
| ctxr_448d50f47d83c101d92f | accuracy | generic_metric | accuracy | 0.7 | sentence_text | unreviewed | False | True | none | generic_metric_feature_only | generic_metric |
| ctxr_cb27bb574c756f008de2 | accuracy | generic_metric | accuracy | 0.7 | sentence_text | unreviewed | False | True | none | generic_metric_feature_only | generic_metric |
| ctxr_b3f99b73329db6bbf332 | accuracy | generic_metric | accuracy | 0.6 | context_window_neighbor | unreviewed | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match |
| ctxr_2f5e46e03d46668bbce5 | accuracy | generic_metric | accuracy | 0.6 | context_window_neighbor | unreviewed | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match |
| ctxr_bfa0c45f2b3bb8eab029 | accuracy | generic_metric | accuracy | 0.6 | context_window_neighbor | unreviewed | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match |
| ctxr_ecd4f003f9eaf6db9c22 | accuracy | generic_metric | accuracy | 0.6 | context_window_neighbor | unreviewed | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match |
| ctxr_b12cc8b450c89e4eb018 | accuracy | generic_metric | accuracy | 0.6 | context_window_neighbor | true | False | True | none | llm_graph_signal;llm_phase1_signal;generic_metric_feature_only | generic_metric;neighbor_context_match |
| ctxr_3993cd48c52c692f24b2 | accuracy | generic_metric | accuracy | 0.6 | context_window_neighbor | unreviewed | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match |

## Graph Candidate Examples
| context_id | canonical_name | object_category | surface_form | confidence | matched_in | mention_correct | graph_eligible | phase1_feature_eligible | graph_candidate_level | policy_reason | match_policy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_f6863fcab52657a5c16e | SemEval | named_object | SemEval | 0.85 | context_window_neighbor | unreviewed | True | True | broad | default_policy | standard;neighbor_context_match |
| ctxr_3e4722d1950da619a7dd | CRF | named_object | CRF | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | standard |
| ctxr_794ff11af106441610a2 | BLEU | named_object | BLEU | 0.85 | context_window_neighbor | unreviewed | True | True | broad | named_metric_graph_eligible | standard;neighbor_context_match |
| ctxr_caa50477f333d1e3c48b | Penn Treebank | named_object | Penn Treebank | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | context_cue_present |
| ctxr_caa50477f333d1e3c48b | Penn Treebank | named_object | PTB | 0.95 | sentence_text | unreviewed | True | True | strict | ptb_context_cue_present | context_cue_present |
| ctxr_4355448353bdd023508c | GIZA++ | named_object | GIZA++ | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | standard |
| ctxr_e68e33d8515b22b2c3ce | BLEU | named_object | BLEU score | 0.95 | sentence_text | unreviewed | True | True | strict | named_metric_graph_eligible | standard |
| ctxr_e4bd8b3cb291ec3f4e15 | GIZA++ | named_object | GIZA++ | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | standard |
| ctxr_99f7530c7394c4ee6f33 | BLEU | named_object | BLEU | 0.95 | sentence_text | unreviewed | True | True | strict | named_metric_graph_eligible | standard |
| ctxr_cda6ba0e4cd02c1152fb | BLEU | named_object | BLEU score | 0.95 | sentence_text | unreviewed | True | True | strict | named_metric_graph_eligible | standard |
| ctxr_e3dec93bf83ff55bb70a | ROUGE | named_object | ROUGE | 0.95 | sentence_text | unreviewed | True | True | strict | named_metric_graph_eligible | standard |
| ctxr_cbf322775aa793d09591 | ROUGE | named_object | ROUGE | 0.95 | sentence_text | unreviewed | True | True | strict | named_metric_graph_eligible | standard |
| ctxr_7e729e2f9c3e394d22a2 | ROUGE | named_object | ROUGE | 0.95 | sentence_text | unreviewed | True | True | strict | named_metric_graph_eligible | standard |
| ctxr_bcc118cb881cd6af4c4e | ROUGE | named_object | ROUGE | 0.95 | sentence_text | unreviewed | True | True | strict | named_metric_graph_eligible | standard |
| ctxr_fc364de7c4a52b630606 | ROUGE | named_object | ROUGE | 0.95 | sentence_text | unreviewed | True | True | strict | named_metric_graph_eligible | standard |
| ctxr_fc364de7c4a52b630606 | ROUGE | named_object | ROUGE | 0.95 | sentence_text | unreviewed | True | True | strict | named_metric_graph_eligible | standard |
| ctxr_fc364de7c4a52b630606 | ROUGE | named_object | ROUGE | 0.95 | sentence_text | unreviewed | True | True | strict | named_metric_graph_eligible | standard |
| ctxr_11a201fb38db6ec2b675 | ROUGE | named_object | ROUGE | 0.95 | sentence_text | unreviewed | True | True | strict | named_metric_graph_eligible | standard |
| ctxr_c222d4c1bd43d71f629d | PropBank | named_object | PropBank | 0.85 | context_window_neighbor | unreviewed | True | True | broad | default_policy | standard;neighbor_context_match |
| ctxr_c222d4c1bd43d71f629d | FrameNet | named_object | FrameNet | 0.85 | context_window_neighbor | unreviewed | True | True | broad | default_policy | standard;neighbor_context_match |
| ctxr_9756d01b7f59460f7acb | PropBank | named_object | PropBank | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | standard |
| ctxr_9756d01b7f59460f7acb | FrameNet | named_object | FrameNet | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | standard |
| ctxr_344bcf5eb41c21d0081a | PropBank | named_object | PropBank | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | standard |
| ctxr_344bcf5eb41c21d0081a | FrameNet | named_object | FrameNet | 0.95 | sentence_text | unreviewed | True | True | strict | default_policy | standard |
| ctxr_bf6577bd218dc6da6e42 | FrameNet | named_object | FrameNet | 0.85 | context_window_neighbor | unreviewed | True | True | broad | default_policy | standard;neighbor_context_match |

## Cited Title Profiles Remain Separate
| context_id | canonical_name | object_category | surface_form | confidence | matched_in | mention_correct | graph_eligible | phase1_feature_eligible | graph_candidate_level | policy_reason | match_policy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_6ec7b60115b4d5e6dcf1 | CRF | named_object | CRF | 0.95 | resolved_cited_title | unreviewed | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard |
| ctxr_5cf962d606f5bb683922 | BLEU | named_object | BLEU | 0.95 | resolved_cited_title | unreviewed | False | False | none | named_metric_graph_eligible;resolved_cited_title_profile_not_direct_context_evidence | standard |
| ctxr_f2fc5d3298a427695aa8 | HMM | named_object | HMM | 0.95 | resolved_cited_title | unreviewed | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard |
| ctxr_52bb41aed58f89be7736 | HMM | named_object | HMM | 0.95 | resolved_cited_title | unreviewed | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard |
| ctxr_fa827b5872437cd3481b | HMM | named_object | HMM | 0.95 | resolved_cited_title | unreviewed | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard |
| ctxr_348ed735539164c215ec | HMM | named_object | HMM | 0.95 | resolved_cited_title | unreviewed | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard |
| ctxr_c0ecda4d16dd1fa0c113 | GloVe | named_object | Global Vectors for Word Representation | 0.95 | resolved_cited_title | unreviewed | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard |
| ctxr_aa1b7e3f43fffb4f92b0 | Transformer | named_object | Transformers | 0.95 | resolved_cited_title | unreviewed | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard |
| ctxr_4ece378a815889ac5290 | Transformer | named_object | Transformers | 0.95 | resolved_cited_title | unreviewed | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard |
| ctxr_74d9fd93d7822354fb0f | Transformer | named_object | Transformers | 0.95 | resolved_cited_title | unreviewed | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard |
| ctxr_135f1a3a6cc1d78491d8 | Transformer | named_object | Transformers | 0.95 | resolved_cited_title | true | False | False | none | llm_graph_signal;llm_phase1_signal;resolved_cited_title_profile_not_direct_context_evidence | standard |
| ctxr_c7102908c01762631958 | Transformer | named_object | Transformers | 0.95 | resolved_cited_title | unreviewed | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard |
| ctxr_30ddd765062e3abcb42a | seq2seq | named_object | Sequence to Sequence | 0.85 | resolved_cited_title | unreviewed | False | False | none | seq2seq_context_cue_missing;resolved_cited_title_profile_not_direct_context_evidence | standard;require_context_cue |
| ctxr_a66cd052e5042059ea1b | seq2seq | named_object | Sequence to Sequence | 0.85 | resolved_cited_title | unreviewed | False | False | none | seq2seq_context_cue_missing;resolved_cited_title_profile_not_direct_context_evidence | standard;require_context_cue |
| ctxr_92a39f9773361a0b10a6 | seq2seq | named_object | Sequence to Sequence | 0.85 | resolved_cited_title | unreviewed | False | False | none | seq2seq_context_cue_missing;resolved_cited_title_profile_not_direct_context_evidence | standard;require_context_cue |
