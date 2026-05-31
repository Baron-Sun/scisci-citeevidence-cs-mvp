# Object Matching Report

## Inputs
- Contexts: `data/processed/analysis_ready_strong_contexts.parquet`
- Registry: `configs/object_registry_seed.yaml`
- Configured limit: `full`

## Outputs
- Object mentions: `data/processed/object_mentions.parquet`
- Cited-title object profiles: `data/processed/cited_title_object_profiles.parquet`
- Object graph candidates: `data/processed/object_graph_candidate_mentions.parquet`
- Strict graph candidates: `data/processed/object_graph_candidate_mentions_strict.parquet`
- Broad graph candidates: `data/processed/object_graph_candidate_mentions_broad.parquet`
- Review sample: `data/processed/object_mentions_review_sample.csv`

## Core Counts
| metric | value |
| --- | --- |
| total_context_rows_processed | 1184634 |
| contexts_with_any_object_mention | 266234 |
| contexts_with_graph_candidate_mention | 215653 |
| raw_mentions_before_deduplication | 687299 |
| mentions_after_deduplication | 404228 |
| deduplicated_count | 283071 |
| cited_title_profile_count | 113550 |
| object_graph_candidate_count | 322688 |
| strict_graph_candidate_count | 205782 |
| broad_graph_candidate_count | 116906 |

## Mentions By Object Type
| object_type | mentions |
| --- | --- |
| model | 163600 |
| metric | 102465 |
| dataset_or_database | 51667 |
| method | 45654 |
| benchmark_or_protocol | 23813 |
| software_or_tool | 17029 |

## Mentions By Object Category
| object_category | mentions |
| --- | --- |
| named_object | 335801 |
| generic_metric | 59307 |
| generic_architecture | 7160 |
| ambiguous_short_alias | 1960 |

## Mentions By allow_in_object_graph
| allow_in_object_graph | mentions |
| --- | --- |
| True | 334322 |
| False | 69906 |

## Mentions By graph_eligible
| graph_eligible | mentions |
| --- | --- |
| True | 334322 |
| False | 69906 |

## Mentions By phase1_feature_eligible
| phase1_feature_eligible | mentions |
| --- | --- |
| True | 403484 |
| False | 744 |

## Graph Candidates By Object Type
| object_type | mentions |
| --- | --- |
| model | 142670 |
| dataset_or_database | 50578 |
| method | 45640 |
| metric | 43133 |
| benchmark_or_protocol | 23642 |
| software_or_tool | 17025 |

## Graph Candidates By Object Category
| object_category | mentions |
| --- | --- |
| named_object | 322688 |

## Graph Candidates By Normalized Section
| normalized_section | mentions |
| --- | --- |
| unknown | 82576 |
| introduction | 70489 |
| related_work | 61606 |
| experiment | 22426 |
| model | 20490 |
| dataset | 15125 |
| evaluation | 14610 |
| method | 9459 |
| results | 8445 |
| background | 3637 |
| conclusion | 3405 |
| implementation | 2400 |
| discussion | 2175 |
| analysis | 2021 |
| system_description | 1641 |
| abstract | 1494 |
| task_definition | 474 |
| error_analysis | 215 |

## Graph Candidates By Matched In
| matched_in | mentions |
| --- | --- |
| sentence_text | 205782 |
| context_window_neighbor | 116906 |

## Cited Title Profiles By Object Type
| object_type | profiles |
| --- | --- |
| model | 84974 |
| method | 10903 |
| metric | 8543 |
| benchmark_or_protocol | 7330 |
| software_or_tool | 1587 |
| dataset_or_database | 213 |

## Top 100 Named Objects By Mention Count
| object_id | canonical_name | object_type | mentions |
| --- | --- | --- | --- |
| obj_bert | BERT | model | 47170 |
| obj_lstm | LSTM | model | 35122 |
| obj_bleu | BLEU | metric | 27313 |
| obj_seq2seq | seq2seq | model | 25869 |
| obj_crf | CRF | method | 23527 |
| obj_transformer | Transformer | model | 23049 |
| obj_wordnet | WordNet | dataset_or_database | 18263 |
| obj_semeval | SemEval | benchmark_or_protocol | 12395 |
| obj_attention_mechanism | attention mechanism | method | 12027 |
| obj_rouge | ROUGE | metric | 10307 |
| obj_glove | GloVe | model | 10294 |
| obj_hmm | HMM | method | 10100 |
| obj_penn_treebank | Penn Treebank | dataset_or_database | 9458 |
| obj_word2vec | word2vec | model | 7361 |
| obj_moses | Moses | software_or_tool | 6788 |
| obj_elmo | ELMo | model | 6686 |
| obj_meteor | METEOR | metric | 5538 |
| obj_squad | SQuAD | dataset_or_database | 5504 |
| obj_wmt | WMT | benchmark_or_protocol | 5419 |
| obj_framenet | FrameNet | dataset_or_database | 5161 |
| obj_giza | GIZA++ | software_or_tool | 5013 |
| obj_propbank | PropBank | dataset_or_database | 4026 |
| obj_snli | SNLI | dataset_or_database | 3907 |
| obj_glue | GLUE | benchmark_or_protocol | 3165 |
| obj_ontonotes | OntoNotes | dataset_or_database | 3065 |
| obj_stanford_corenlp | Stanford CoreNLP | software_or_tool | 2026 |
| obj_conll_2003 | CoNLL-2003 | benchmark_or_protocol | 1298 |
| obj_nltk | NLTK | software_or_tool | 1228 |
| obj_multinli | MultiNLI | dataset_or_database | 1212 |
| obj_opus | OPUS | software_or_tool | 1207 |
| obj_conll_2012 | CoNLL-2012 | benchmark_or_protocol | 848 |
| obj_spacy | spaCy | software_or_tool | 767 |
| obj_superglue | SuperGLUE | benchmark_or_protocol | 688 |

## Top 100 Graph Candidate Objects
| object_id | canonical_name | object_type | mentions |
| --- | --- | --- | --- |
| obj_bert | BERT | model | 47170 |
| obj_lstm | LSTM | model | 34654 |
| obj_bleu | BLEU | metric | 27308 |
| obj_crf | CRF | method | 23524 |
| obj_transformer | Transformer | model | 23049 |
| obj_wordnet | WordNet | dataset_or_database | 18263 |
| obj_seq2seq | seq2seq | model | 13456 |
| obj_semeval | SemEval | benchmark_or_protocol | 12395 |
| obj_attention_mechanism | attention mechanism | method | 12020 |
| obj_rouge | ROUGE | metric | 10301 |
| obj_glove | GloVe | model | 10294 |
| obj_hmm | HMM | method | 10096 |
| obj_penn_treebank | Penn Treebank | dataset_or_database | 9441 |
| obj_word2vec | word2vec | model | 7361 |
| obj_moses | Moses | software_or_tool | 6784 |
| obj_elmo | ELMo | model | 6686 |
| obj_meteor | METEOR | metric | 5524 |
| obj_squad | SQuAD | dataset_or_database | 5503 |
| obj_wmt | WMT | benchmark_or_protocol | 5418 |
| obj_framenet | FrameNet | dataset_or_database | 5161 |
| obj_giza | GIZA++ | software_or_tool | 5013 |
| obj_propbank | PropBank | dataset_or_database | 4026 |
| obj_snli | SNLI | dataset_or_database | 3907 |
| obj_ontonotes | OntoNotes | dataset_or_database | 3065 |
| obj_glue | GLUE | benchmark_or_protocol | 3051 |
| obj_stanford_corenlp | Stanford CoreNLP | software_or_tool | 2026 |
| obj_conll_2003 | CoNLL-2003 | benchmark_or_protocol | 1243 |
| obj_nltk | NLTK | software_or_tool | 1228 |
| obj_multinli | MultiNLI | dataset_or_database | 1212 |
| obj_opus | OPUS | software_or_tool | 1207 |
| obj_conll_2012 | CoNLL-2012 | benchmark_or_protocol | 847 |
| obj_spacy | spaCy | software_or_tool | 767 |
| obj_superglue | SuperGLUE | benchmark_or_protocol | 688 |

## Top 50 Generic Metrics
| object_id | canonical_name | surface_form | mentions |
| --- | --- | --- | --- |
| obj_accuracy | accuracy | accuracy | 37159 |
| obj_f1 | F1 | F1 | 7997 |
| obj_perplexity | perplexity | perplexity | 3071 |
| obj_f1 | F1 | F1 score | 2515 |
| obj_f1 | F1 | F-score | 2470 |
| obj_accuracy | accuracy | Accuracy | 1500 |
| obj_f1 | F1 | F-measure | 1500 |
| obj_f1 | F1 | F1-score | 1100 |
| obj_accuracy | accuracy | classification accuracy | 1053 |
| obj_perplexity | perplexity | PPL | 286 |
| obj_perplexity | perplexity | Perplexity | 227 |
| obj_f1 | F1 | F score | 119 |
| obj_f1 | F1 | F measure | 111 |
| obj_f1 | F1 | F -score | 59 |
| obj_perplexity | perplexity | ppl | 40 |
| obj_f1 | F1 | F -measure | 32 |
| obj_accuracy | accuracy | Classification accuracy | 26 |
| obj_perplexity | perplexity | Ppl | 18 |
| obj_accuracy | accuracy | Classification Accuracy | 5 |
| obj_f1 | F1 | F(-measure | 4 |
| obj_f1 | F1 | F1" score | 4 |
| obj_f1 | F1 | F1) score | 4 |
| obj_f1 | F1 | F − score | 2 |
| obj_accuracy | accuracy | classification (accuracy | 1 |
| obj_f1 | F1 | F (score | 1 |
| obj_f1 | F1 | F) score | 1 |
| obj_f1 | F1 | F)-score | 1 |
| obj_f1 | F1 | F˙score | 1 |

## Top 50 Ambiguous Aliases
| object_id | canonical_name | surface_form | match_policy | mentions |
| --- | --- | --- | --- | --- |
| obj_penn_treebank | Penn Treebank | PTB | weak_context_cue_missing;require_context_cue | 668 |
| obj_penn_treebank | Penn Treebank | PTB | weak_context_cue_missing;neighbor_context_match;require_context_cue | 402 |
| obj_seq2seq | seq2seq | seq2seq | weak_context_cue_missing;require_context_cue | 263 |
| obj_seq2seq | seq2seq | Seq2Seq | weak_context_cue_missing;require_context_cue | 187 |
| obj_seq2seq | seq2seq | seq2seq | weak_context_cue_missing;neighbor_context_match;require_context_cue | 168 |
| obj_seq2seq | seq2seq | Seq2Seq | weak_context_cue_missing;neighbor_context_match;require_context_cue | 85 |
| obj_seq2seq | seq2seq | encoder/decoder | weak_context_cue_missing;neighbor_context_match;require_context_cue | 43 |
| obj_seq2seq | seq2seq | Seq2seq | weak_context_cue_missing;require_context_cue | 36 |
| obj_seq2seq | seq2seq | SEQ2SEQ | weak_context_cue_missing;require_context_cue | 34 |
| obj_seq2seq | seq2seq | Seq2seq | weak_context_cue_missing;neighbor_context_match;require_context_cue | 27 |
| obj_seq2seq | seq2seq | encoder/decoder | weak_context_cue_missing;require_context_cue | 25 |
| obj_seq2seq | seq2seq | SEQ2SEQ | weak_context_cue_missing;neighbor_context_match;require_context_cue | 17 |
| obj_seq2seq | seq2seq | encoder, decoder | weak_context_cue_missing;require_context_cue | 2 |
| obj_penn_treebank | Penn Treebank | ptb | weak_context_cue_missing;require_context_cue | 1 |
| obj_seq2seq | seq2seq | Encoder, decoder | weak_context_cue_missing;neighbor_context_match;require_context_cue | 1 |
| obj_seq2seq | seq2seq | encoder, decoder | weak_context_cue_missing;neighbor_context_match;require_context_cue | 1 |

## Top 50 Cited-Title Profile Objects
| object_id | canonical_name | object_type | profiles |
| --- | --- | --- | --- |
| obj_bert | BERT | model | 29732 |
| obj_transformer | Transformer | model | 21911 |
| obj_lstm | LSTM | model | 16353 |
| obj_seq2seq | seq2seq | model | 9944 |
| obj_crf | CRF | method | 8194 |
| obj_glove | GloVe | model | 6990 |
| obj_wmt | WMT | benchmark_or_protocol | 6256 |
| obj_rouge | ROUGE | metric | 2333 |
| obj_accuracy | accuracy | metric | 2103 |
| obj_meteor | METEOR | metric | 2034 |
| obj_hmm | HMM | method | 1876 |
| obj_bleu | BLEU | metric | 1806 |
| obj_glue | GLUE | benchmark_or_protocol | 843 |
| obj_attention_mechanism | attention mechanism | method | 833 |
| obj_opus | OPUS | software_or_tool | 802 |
| obj_nltk | NLTK | software_or_tool | 699 |
| obj_perplexity | perplexity | metric | 255 |
| obj_semeval | SemEval | benchmark_or_protocol | 231 |
| obj_penn_treebank | Penn Treebank | dataset_or_database | 155 |
| obj_giza | GIZA++ | software_or_tool | 86 |
| obj_elmo | ELMo | model | 39 |
| obj_multinli | MultiNLI | dataset_or_database | 30 |
| obj_f1 | F1 | metric | 12 |
| obj_snli | SNLI | dataset_or_database | 10 |
| obj_squad | SQuAD | dataset_or_database | 10 |
| obj_wordnet | WordNet | dataset_or_database | 8 |
| obj_word2vec | word2vec | model | 5 |

## Top 50 Surface Forms
| surface_form | canonical_name | object_type | mentions |
| --- | --- | --- | --- |
| BERT | BERT | model | 45400 |
| accuracy | accuracy | metric | 37159 |
| LSTM | LSTM | model | 26000 |
| BLEU | BLEU | metric | 22548 |
| WordNet | WordNet | dataset_or_database | 16378 |
| CRF | CRF | method | 13549 |
| Transformer | Transformer | model | 12438 |
| SemEval | SemEval | benchmark_or_protocol | 11207 |
| ROUGE | ROUGE | metric | 9472 |
| attention mechanism | attention mechanism | method | 8819 |
| transformer | Transformer | model | 8053 |
| F1 | F1 | metric | 7997 |
| GloVe | GloVe | model | 7841 |
| sequence-to-sequence | seq2seq | model | 7492 |
| encoder-decoder | seq2seq | model | 7353 |
| Penn Treebank | Penn Treebank | dataset_or_database | 6436 |
| ELMo | ELMo | model | 5797 |
| HMM | HMM | method | 5597 |
| LSTMs | LSTM | model | 5253 |
| WMT | WMT | benchmark_or_protocol | 5107 |
| FrameNet | FrameNet | dataset_or_database | 5020 |
| Moses | Moses | software_or_tool | 4985 |
| seq2seq | seq2seq | model | 4760 |
| word2vec | word2vec | model | 4683 |
| METEOR | METEOR | metric | 4581 |
| SQuAD | SQuAD | dataset_or_database | 4372 |
| GIZA++ | GIZA++ | software_or_tool | 4217 |
| BLEU score | BLEU | metric | 3836 |
| CRFs | CRF | method | 3692 |
| SNLI | SNLI | dataset_or_database | 3441 |
| PropBank | PropBank | dataset_or_database | 3388 |
| Transformers | Transformer | model | 3381 |
| Seq2Seq | seq2seq | model | 3329 |
| perplexity | perplexity | metric | 3071 |
| PTB | Penn Treebank | dataset_or_database | 3067 |
| transformers | Transformer | model | 2763 |
| attention mechanisms | attention mechanism | method | 2730 |
| F1 score | F1 | metric | 2515 |
| F-score | F1 | metric | 2470 |
| Conditional Random Fields | CRF | method | 2287 |
| Word2Vec | word2vec | model | 2149 |
| OntoNotes | OntoNotes | dataset_or_database | 2130 |
| conditional random fields | CRF | method | 2032 |
| GLUE | GLUE | benchmark_or_protocol | 1535 |
| Stanford CoreNLP | Stanford CoreNLP | software_or_tool | 1525 |
| Glove | GloVe | model | 1519 |
| Accuracy | accuracy | metric | 1500 |
| F-measure | F1 | metric | 1500 |
| long short-term memory | LSTM | model | 1398 |
| sequence to sequence | seq2seq | model | 1248 |

## Policy Checks
| policy_check | rows | status |
| --- | --- | --- |
| generic_metric rows in object_graph_candidate_mentions | 0 | pass |
| accuracy rows in object_graph_candidate_mentions | 0 | pass |
| F1 rows in object_graph_candidate_mentions | 0 | pass |
| perplexity rows in object_graph_candidate_mentions | 0 | pass |
| resolved_cited_title rows in object_mentions | 0 | pass |
| resolved_cited_title rows in object_graph_candidate_mentions | 0 | pass |
| strict candidates with matched_in != sentence_text | 0 | pass |
| broad candidates with matched_in != context_window_neighbor | 0 | pass |
| ambiguous_short_alias rows in strict graph candidates | 0 | pass |
| original_allow_in_object_graph=False but graph_eligible=True | 4130 | review |

## original_allow_in_object_graph=False but graph_eligible=True Examples
| context_id | source_context_id | canonical_name | object_type | object_category | surface_form | confidence | matched_in | allow_in_object_graph | graph_eligible | phase1_feature_eligible | graph_candidate_level | policy_reason | match_policy | normalized_section | resolved_cited_title |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_bbb1ce2f4d76174a40a8 | ctx_cb95ffee767bbafc26c5 | Transformer | model | named_object | transformer | 0.85 | sentence_text | True | True | True | strict | lowercase_transformer_context_cue_present | lowercase_generic_architecture;lowercase_context_cue_present | method | {BERT}: Pre-training of Deep Bidirectional Transformers for Language Understanding |
| ctxr_310a6be229709f5b2c34 | ctx_b0373c0611d126e15041 | Transformer | model | named_object | transformer | 0.85 | context_window_neighbor | True | True | True | broad | lowercase_transformer_context_cue_present | lowercase_generic_architecture;neighbor_context_match;lowercase_context_cue_present | unknown | Transfer Learning in Biomedical Natural Language Processing: An Evaluation of {BERT} and {ELM}o on Ten Benchmarking Datasets |
| ctxr_6de29b3ac8a8ba731152 | ctx_49e99fd2a7589129d5b0 | Transformer | model | named_object | transformer | 0.85 | context_window_neighbor | True | True | True | broad | lowercase_transformer_context_cue_present | lowercase_generic_architecture;neighbor_context_match;lowercase_context_cue_present | related_work | Convolutional neural networks for chemical-disease relation extraction are improved with character-based word embeddings |
| ctxr_3bf6635a07eea82ad4b9 | ctx_8d82326c94d2ef9df6e7 | Transformer | model | named_object | transformer | 0.85 | context_window_neighbor | True | True | True | broad | lowercase_transformer_context_cue_present | lowercase_generic_architecture;neighbor_context_match;lowercase_context_cue_present | related_work | Convolutional neural networks for chemical-disease relation extraction are improved with character-based word embeddings |
| ctxr_cd0879c061b38c70abff | ctx_05d410e3bbc61057b1a7 | Transformer | model | named_object | transformer | 0.85 | sentence_text | True | True | True | strict | lowercase_transformer_context_cue_present | lowercase_generic_architecture;lowercase_context_cue_present | related_work | Simultaneously Self-Attending to All Mentions for Full-Abstract Biological Relation Extraction |
| ctxr_132a36f8e50fa6daf3a4 | ctx_17a2b07f4d248b259880 | Transformer | model | named_object | transformer | 0.85 | context_window_neighbor | True | True | True | broad | lowercase_transformer_context_cue_present | lowercase_generic_architecture;neighbor_context_match;lowercase_context_cue_present | model | {BART}: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension |
| ctxr_9da88ff6c9701d288368 | ctx_0ec75856acac472eeb71 | Penn Treebank | dataset_or_database | named_object | PTB | 0.85 | sentence_text | True | True | True | strict | ptb_context_cue_present | weak_context_cue_missing;context_cue_present | dataset | Part-of-Speech Tagging for {T}witter: Annotation, Features, and Experiments |
| ctxr_f0e6f07cc090e6d41797 | ctx_f0579fd6a022c5d0eb71 | Transformer | model | named_object | transformer | 0.85 | context_window_neighbor | True | True | True | broad | lowercase_transformer_context_cue_present | lowercase_generic_architecture;neighbor_context_match;lowercase_context_cue_present | related_work | Paragraph-level Neural Question Generation with Maxout Pointer and Gated Self-attention Networks |
| ctxr_9adf20a0810b9850cf4c | ctx_391b7a233562add90bb5 | Transformer | model | named_object | transformer | 0.85 | sentence_text | True | True | True | strict | lowercase_transformer_context_cue_present | lowercase_generic_architecture;lowercase_context_cue_present | related_work | Self-Attention Architectures for Answer-Agnostic Neural Question Generation |
| ctxr_f285d5ec5d57632262d3 | ctx_cec0ba39f3b866bfe36a | Transformer | model | named_object | transformer | 0.85 | sentence_text | True | True | True | strict | lowercase_transformer_context_cue_present | lowercase_generic_architecture;lowercase_context_cue_present | unknown | {A} Structural Probe for Finding Syntax in Word Representations |
| ctxr_4ac19d16322d3fe2ce02 | ctx_5b9cac54fe9adc953286 | Transformer | model | named_object | transformer | 0.85 | sentence_text | True | True | True | strict | lowercase_transformer_context_cue_present | lowercase_generic_architecture;lowercase_context_cue_present | unknown | {A} Structural Probe for Finding Syntax in Word Representations |
| ctxr_cd1fac0f6c443763707e | ctx_1da753538f39e4834c43 | Transformer | model | named_object | transformer | 0.85 | sentence_text | True | True | True | strict | lowercase_transformer_context_cue_present | lowercase_generic_architecture;lowercase_context_cue_present | introduction | {R}e{C}o{S}a: Detecting the Relevant Contexts with Self-Attention for Multi-turn Dialogue Generation |
| ctxr_74f007630f84d8bbc61a | ctx_48fec63ba703d903e350 | Transformer | model | named_object | transformer | 0.85 | sentence_text | True | True | True | strict | lowercase_transformer_context_cue_present | lowercase_generic_architecture;lowercase_context_cue_present | unknown | fairseq: A Fast, Extensible Toolkit for Sequence Modeling |
| ctxr_d5557e0dde5af96f572d | ctx_ccd51b1e4a5e3e286c1c | Penn Treebank | dataset_or_database | named_object | PTB | 0.85 | context_window_neighbor | True | True | True | broad | ptb_context_cue_present | weak_context_cue_missing;neighbor_context_match;context_cue_present | unknown | Annotating Coordination in the {P}enn {T}reebank |
| ctxr_2b5201587fd1ce18b9c2 | ctx_417ac8073584c199cd6e | Penn Treebank | dataset_or_database | named_object | PTB | 0.85 | context_window_neighbor | True | True | True | broad | ptb_context_cue_present | weak_context_cue_missing;neighbor_context_match;context_cue_present | introduction | {PLCFRS} Parsing of {E}nglish Discontinuous Constituents |
| ctxr_22c643691688041f985d | ctx_7a4af905223785c8810b | Penn Treebank | dataset_or_database | named_object | PTB | 0.85 | context_window_neighbor | True | True | True | broad | ptb_context_cue_present | weak_context_cue_missing;neighbor_context_match;context_cue_present | introduction | An Annotation Scheme for Free Word Order Languages |
| ctxr_f33f15351a38203640bb | ctx_b7ba5c6748e931bbc96b | Penn Treebank | dataset_or_database | named_object | PTB | 0.85 | context_window_neighbor | True | True | True | broad | ptb_context_cue_present | weak_context_cue_missing;neighbor_context_match;context_cue_present | introduction | Building a Large Annotated Corpus of {E}nglish: The {P}enn {T}reebank |
| ctxr_e213a1a20a6d8933fd3f | ctx_8b673717cd8a519930f8 | Penn Treebank | dataset_or_database | named_object | PTB | 0.85 | sentence_text | True | True | True | strict | ptb_context_cue_present | weak_context_cue_missing;context_cue_present | introduction | From {T}ree{B}ank to {P}rop{B}ank |
| ctxr_e1b7e8fb0bfe10e2387c | ctx_c007351288aadc2e1a5d | Penn Treebank | dataset_or_database | named_object | PTB | 0.85 | sentence_text | True | True | True | strict | ptb_context_cue_present | weak_context_cue_missing;context_cue_present | dataset | Building a Large Annotated Corpus of {E}nglish: The {P}enn {T}reebank |
| ctxr_ade313a487a2e6dd4583 | ctx_9aa91c7c99336a8d8fe7 | Penn Treebank | dataset_or_database | named_object | PTB | 0.85 | context_window_neighbor | True | True | True | broad | ptb_context_cue_present | weak_context_cue_missing;neighbor_context_match;context_cue_present | introduction | Head-Driven Statistical Models for Natural Language Parsing |

## Named Object Strict Candidate Examples
| context_id | source_context_id | canonical_name | object_type | object_category | surface_form | confidence | matched_in | allow_in_object_graph | graph_eligible | phase1_feature_eligible | graph_candidate_level | policy_reason | match_policy | normalized_section | resolved_cited_title |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_3e4722d1950da619a7dd | ctx_ca6cc2ce8812268acdb7 | CRF | method | named_object | CRF | 0.95 | sentence_text | True | True | True | strict | default_policy | standard | unknown | {KPW}r: Towards a Free Corpus of {P}olish |
| ctxr_caa50477f333d1e3c48b | ctx_1cf74ef13884c4116a34 | Penn Treebank | dataset_or_database | named_object | Penn Treebank | 0.95 | sentence_text | True | True | True | strict | default_policy | context_cue_present | dataset | Building a Large Annotated Corpus of {E}nglish: The {P}enn {T}reebank |
| ctxr_caa50477f333d1e3c48b | ctx_1cf74ef13884c4116a34 | Penn Treebank | dataset_or_database | named_object | PTB | 0.95 | sentence_text | True | True | True | strict | ptb_context_cue_present | context_cue_present | dataset | Building a Large Annotated Corpus of {E}nglish: The {P}enn {T}reebank |
| ctxr_4355448353bdd023508c | ctx_e33a1b32079c54fb1946 | GIZA++ | software_or_tool | named_object | GIZA++ | 0.95 | sentence_text | True | True | True | strict | default_policy | standard | unknown | A Systematic Comparison of Various Statistical Alignment Models |
| ctxr_e68e33d8515b22b2c3ce | ctx_e7b701fba3d099912dd6 | BLEU | metric | named_object | BLEU score | 0.95 | sentence_text | True | True | True | strict | named_metric_graph_eligible | standard | results | {B}leu: a Method for Automatic Evaluation of Machine Translation |
| ctxr_e4bd8b3cb291ec3f4e15 | ctx_2a912ffa75455b48a752 | GIZA++ | software_or_tool | named_object | GIZA++ | 0.95 | sentence_text | True | True | True | strict | default_policy | standard | method | Improved Statistical Alignment Models |
| ctxr_99f7530c7394c4ee6f33 | ctx_e4ba8f99069e1b01841d | BLEU | metric | named_object | BLEU | 0.95 | sentence_text | True | True | True | strict | named_metric_graph_eligible | standard | method | {B}leu: a Method for Automatic Evaluation of Machine Translation |
| ctxr_cda6ba0e4cd02c1152fb | ctx_f713902f0bb80232d3fb | BLEU | metric | named_object | BLEU score | 0.95 | sentence_text | True | True | True | strict | named_metric_graph_eligible | standard | unknown | {B}leu: a Method for Automatic Evaluation of Machine Translation |
| ctxr_e3dec93bf83ff55bb70a | ctx_aa06ab554ff08d94dcd9 | ROUGE | metric | named_object | ROUGE | 0.95 | sentence_text | True | True | True | strict | named_metric_graph_eligible | standard | related_work | {L}ex{P}age{R}ank: Prestige in Multi-Document Text Summarization |
| ctxr_cbf322775aa793d09591 | ctx_55957fe8e3d126161928 | ROUGE | metric | named_object | ROUGE | 0.95 | sentence_text | True | True | True | strict | named_metric_graph_eligible | standard | related_work | {T}ext{R}ank: Bringing Order into Text |
| ctxr_7e729e2f9c3e394d22a2 | ctx_4781909a166d3ffa180d | ROUGE | metric | named_object | ROUGE | 0.95 | sentence_text | True | True | True | strict | named_metric_graph_eligible | standard | evaluation | Automatic Evaluation of Summaries Using N-gram Co-occurrence Statistics |
| ctxr_bcc118cb881cd6af4c4e | ctx_d2bab7b021e784dc9e64 | ROUGE | metric | named_object | ROUGE | 0.95 | sentence_text | True | True | True | strict | named_metric_graph_eligible | standard | evaluation | Automatic Evaluation of Summaries Using N-gram Co-occurrence Statistics |
| ctxr_fc364de7c4a52b630606 | ctx_cb76a08f3615c99d92cb | ROUGE | metric | named_object | ROUGE | 0.95 | sentence_text | True | True | True | strict | named_metric_graph_eligible | standard | evaluation | Automatic Evaluation of Summaries Using N-gram Co-occurrence Statistics |
| ctxr_fc364de7c4a52b630606 | ctx_cb76a08f3615c99d92cb | ROUGE | metric | named_object | ROUGE | 0.95 | sentence_text | True | True | True | strict | named_metric_graph_eligible | standard | evaluation | Automatic Evaluation of Summaries Using N-gram Co-occurrence Statistics |
| ctxr_fc364de7c4a52b630606 | ctx_cb76a08f3615c99d92cb | ROUGE | metric | named_object | ROUGE | 0.95 | sentence_text | True | True | True | strict | named_metric_graph_eligible | standard | evaluation | Automatic Evaluation of Summaries Using N-gram Co-occurrence Statistics |
| ctxr_11a201fb38db6ec2b675 | ctx_1d7ab4be830eb141a339 | ROUGE | metric | named_object | ROUGE | 0.95 | sentence_text | True | True | True | strict | named_metric_graph_eligible | standard | evaluation | Automatic Evaluation of Summaries Using N-gram Co-occurrence Statistics |
| ctxr_9756d01b7f59460f7acb | ctx_7b782943152ba440b880 | PropBank | dataset_or_database | named_object | PropBank | 0.95 | sentence_text | True | True | True | strict | default_policy | standard | introduction | The {B}erkeley {F}rame{N}et Project |
| ctxr_9756d01b7f59460f7acb | ctx_7b782943152ba440b880 | FrameNet | dataset_or_database | named_object | FrameNet | 0.95 | sentence_text | True | True | True | strict | default_policy | standard | introduction | The {B}erkeley {F}rame{N}et Project |
| ctxr_344bcf5eb41c21d0081a | ctx_a313706134b38b7989f6 | PropBank | dataset_or_database | named_object | PropBank | 0.95 | sentence_text | True | True | True | strict | default_policy | standard | introduction | {C}o{NLL}-2012 Shared Task: Modeling Multilingual Unrestricted Coreference in {O}nto{N}otes |
| ctxr_344bcf5eb41c21d0081a | ctx_a313706134b38b7989f6 | FrameNet | dataset_or_database | named_object | FrameNet | 0.95 | sentence_text | True | True | True | strict | default_policy | standard | introduction | {C}o{NLL}-2012 Shared Task: Modeling Multilingual Unrestricted Coreference in {O}nto{N}otes |

## Named Object Broad Candidate Examples
| context_id | source_context_id | canonical_name | object_type | object_category | surface_form | confidence | matched_in | allow_in_object_graph | graph_eligible | phase1_feature_eligible | graph_candidate_level | policy_reason | match_policy | normalized_section | resolved_cited_title |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_f6863fcab52657a5c16e | ctx_f31d14d5a204a23fdb80 | SemEval | benchmark_or_protocol | named_object | SemEval | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | related_work | {ISI}: Automatic Classification of Relations Between Nominals Using a Maximum Entropy Classifier |
| ctxr_794ff11af106441610a2 | ctx_7f225179a64758da5dba | BLEU | metric | named_object | BLEU | 0.85 | context_window_neighbor | True | True | True | broad | named_metric_graph_eligible | standard;neighbor_context_match | model | Automatic Learning of Language Model Structure |
| ctxr_c222d4c1bd43d71f629d | ctx_658af6609e37dc607c43 | PropBank | dataset_or_database | named_object | PropBank | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | introduction | Automatic Labeling of Semantic Roles |
| ctxr_c222d4c1bd43d71f629d | ctx_658af6609e37dc607c43 | FrameNet | dataset_or_database | named_object | FrameNet | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | introduction | Automatic Labeling of Semantic Roles |
| ctxr_bf6577bd218dc6da6e42 | ctx_0ab6922d1f93eec7ecd6 | FrameNet | dataset_or_database | named_object | FrameNet | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | introduction | Construction of a {J}apanese Relevance-tagged Corpus |
| ctxr_296955737e98c10a5151 | ctx_dad0d78b442b14953017 | FrameNet | dataset_or_database | named_object | FrameNet | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | introduction | Annotating a {J}apanese Text Corpus with Predicate-Argument and Coreference Relations |
| ctxr_e29d4de098ff144543d9 | ctx_a3f4dc606ed46a0bdcdd | LSTM | model | named_object | LSTM | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | related_work | Deep Semantic Role Labeling: What Works and What{'}s Next |
| ctxr_023a8eacb53c5fb15079 | ctx_fda17dcdd461f7773e54 | HMM | method | named_object | hidden Markov models | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | related_work | Confidence Estimation for Information Extraction |
| ctxr_023a8eacb53c5fb15079 | ctx_fda17dcdd461f7773e54 | CRF | method | named_object | Conditional Random Field | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | related_work | Confidence Estimation for Information Extraction |
| ctxr_023a8eacb53c5fb15079 | ctx_fda17dcdd461f7773e54 | CRF | method | named_object | CRF | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | related_work | Confidence Estimation for Information Extraction |
| ctxr_05b1c9a945b814c67384 | ctx_9eb8fd9db9428e83b0af | PropBank | dataset_or_database | named_object | PropBank | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | introduction | {AMR} Parsing as Sequence-to-Graph Transduction |
| ctxr_05b1c9a945b814c67384 | ctx_9eb8fd9db9428e83b0af | FrameNet | dataset_or_database | named_object | FrameNet | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | introduction | {AMR} Parsing as Sequence-to-Graph Transduction |
| ctxr_3bb54eb9ce1ea3a10314 | ctx_f32caf4cb30898e342b9 | PropBank | dataset_or_database | named_object | PropBank | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | unknown | The {B}erkeley {F}rame{N}et Project |
| ctxr_86b64fa23a8373fd802f | ctx_aeb8d0ae431272cb2928 | PropBank | dataset_or_database | named_object | PropBank | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | unknown | The {B}erkeley {F}rame{N}et Project |
| ctxr_f35b77144b6ee9eec336 | ctx_28e9b6a0e606d538a800 | PropBank | dataset_or_database | named_object | PropBank | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | unknown | The {B}erkeley {F}rame{N}et Project |
| ctxr_5ba2d9c30511a7fdaed3 | ctx_c1c6aad4d4c8fb0b2fec | PropBank | dataset_or_database | named_object | PropBank | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | unknown | The {B}erkeley {F}rame{N}et Project |
| ctxr_2a2219ca05bdc9420528 | ctx_b9b52138f33372fd28e1 | BLEU | metric | named_object | BLEU score | 0.85 | context_window_neighbor | True | True | True | broad | named_metric_graph_eligible | standard;neighbor_context_match | introduction | Using monolingual source-language data to improve {MT} performance |
| ctxr_54f5835f3a453d286c07 | ctx_c5f99b4f69372a9abc26 | GIZA++ | software_or_tool | named_object | GIZA++ | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | model | Phrase-based statistical machine translation with pivot languages. |
| ctxr_a9b33c3ed7a11a859b50 | ctx_2af866795a5778fe8235 | FrameNet | dataset_or_database | named_object | FrameNet | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | dataset | Merging {P}rop{B}ank, {N}om{B}ank, {T}ime{B}ank, {P}enn {D}iscourse {T}reebank and Coreference |
| ctxr_a9b33c3ed7a11a859b50 | ctx_2af866795a5778fe8235 | WordNet | dataset_or_database | named_object | WordNet | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | dataset | Merging {P}rop{B}ank, {N}om{B}ank, {T}ime{B}ank, {P}enn {D}iscourse {T}reebank and Coreference |

## Generic Metric Feature-Only Examples
| context_id | source_context_id | canonical_name | object_type | object_category | surface_form | confidence | matched_in | allow_in_object_graph | graph_eligible | phase1_feature_eligible | graph_candidate_level | policy_reason | match_policy | normalized_section | resolved_cited_title |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_d573e73d4a69363cdfc0 | ctx_2058502beaf095f8c9d9 | accuracy | metric | generic_metric | accuracy | 0.6 | context_window_neighbor | False | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match | results | Disentangling Chat with Local Coherence Models |
| ctxr_fde2b4fe687323ff4bd3 | ctx_ce3b0066680b71c0ab36 | F1 | metric | generic_metric | F -measure | 0.7 | sentence_text | False | False | True | none | generic_metric_feature_only | generic_metric | experiment | An Evaluation Exercise for Word Alignment |
| ctxr_794ff11af106441610a2 | ctx_7f225179a64758da5dba | perplexity | metric | generic_metric | perplexity | 0.6 | context_window_neighbor | False | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match | model | Automatic Learning of Language Model Structure |
| ctxr_b4edfcd618c4edc4d4dc | ctx_baae2db29cd713e28052 | accuracy | metric | generic_metric | accuracy | 0.6 | context_window_neighbor | False | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match | introduction | Does Size Matter? Text and Grammar Revision for Parsing Social Media Data |
| ctxr_f7c720ac514891b21f33 | ctx_9467c404bd35ecd142b4 | accuracy | metric | generic_metric | accuracy | 0.7 | sentence_text | False | False | True | none | generic_metric_feature_only | generic_metric | unknown | Online Learning of Approximate Dependency Parsing Algorithms |
| ctxr_26559d1672acccfd09ea | ctx_9c84cb4ef671e246a5be | accuracy | metric | generic_metric | accuracy | 0.6 | context_window_neighbor | False | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match | unknown | Online Large-Margin Training of Dependency Parsers |
| ctxr_c223321394c5bbc2bcec | ctx_c68731c0340fcd07d57b | accuracy | metric | generic_metric | accuracy | 0.6 | context_window_neighbor | False | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match | unknown | {T}n{T} {--} A Statistical Part-of-Speech Tagger |
| ctxr_c223321394c5bbc2bcec | ctx_c68731c0340fcd07d57b | accuracy | metric | generic_metric | accuracy | 0.6 | context_window_neighbor | False | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match | unknown | {T}n{T} {--} A Statistical Part-of-Speech Tagger |
| ctxr_72089786b736eb3c1d50 | ctx_2868157b89a3f8bb0973 | accuracy | metric | generic_metric | accuracy | 0.7 | sentence_text | False | False | True | none | generic_metric_feature_only | generic_metric | unknown | Does Size Matter? Text and Grammar Revision for Parsing Social Media Data |
| ctxr_1348abfe0d9ee416094f | ctx_75f51b85f7f3b4850622 | accuracy | metric | generic_metric | accuracy | 0.6 | context_window_neighbor | False | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match | dataset | {J}apanese-{H}ungarian dictionary generation using ontology resources |
| ctxr_9af9bd56af035c2cee84 | ctx_4ef870281b839f0e6cad | accuracy | metric | generic_metric | accuracy | 0.7 | sentence_text | False | False | True | none | generic_metric_feature_only | generic_metric | unknown | Hybrid Parsing: Using Probabilistic Models as Predictors for a Symbolic Parser |
| ctxr_9ecca4bac0344e435a50 | ctx_08464d970bac736b3c5a | accuracy | metric | generic_metric | accuracy | 0.6 | context_window_neighbor | False | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match | unknown | An Efficient Algorithm for Projective Dependency Parsing |
| ctxr_9ecca4bac0344e435a50 | ctx_08464d970bac736b3c5a | accuracy | metric | generic_metric | accuracy | 0.6 | context_window_neighbor | False | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match | unknown | An Efficient Algorithm for Projective Dependency Parsing |
| ctxr_12dda98b18b7e159cf6c | ctx_f9ad96418feda15bffe7 | accuracy | metric | generic_metric | accuracy | 0.6 | context_window_neighbor | False | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match | unknown | Co-Parsing with Competitive Models |
| ctxr_12dda98b18b7e159cf6c | ctx_f9ad96418feda15bffe7 | accuracy | metric | generic_metric | accuracy | 0.6 | context_window_neighbor | False | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match | unknown | Co-Parsing with Competitive Models |
| ctxr_6f4fbb5a1e4f3b2f971a | ctx_b4f5a1a27ec820df30f4 | accuracy | metric | generic_metric | accuracy | 0.6 | context_window_neighbor | False | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match | unknown | Multilingual Dependency Analysis with a Two-Stage Discriminative Parser |
| ctxr_6f4fbb5a1e4f3b2f971a | ctx_b4f5a1a27ec820df30f4 | accuracy | metric | generic_metric | accuracy | 0.6 | context_window_neighbor | False | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match | unknown | Multilingual Dependency Analysis with a Two-Stage Discriminative Parser |
| ctxr_448d50f47d83c101d92f | ctx_3e66b0fb7777637aa22e | accuracy | metric | generic_metric | accuracy | 0.7 | sentence_text | False | False | True | none | generic_metric_feature_only | generic_metric | unknown | {T}n{T} {--} A Statistical Part-of-Speech Tagger |
| ctxr_cb27bb574c756f008de2 | ctx_da4ba23393fcc1c80f81 | accuracy | metric | generic_metric | accuracy | 0.7 | sentence_text | False | False | True | none | generic_metric_feature_only | generic_metric | related_work | Automatic Labeling of Semantic Roles |
| ctxr_b3f99b73329db6bbf332 | ctx_b1e4dd030768fc6c52f7 | accuracy | metric | generic_metric | accuracy | 0.6 | context_window_neighbor | False | False | True | none | generic_metric_feature_only | generic_metric;neighbor_context_match | related_work | Using Predicate-Argument Structures for Information Extraction |

## PTB With Cue Examples
| context_id | source_context_id | canonical_name | object_type | object_category | surface_form | confidence | matched_in | allow_in_object_graph | graph_eligible | phase1_feature_eligible | graph_candidate_level | policy_reason | match_policy | normalized_section | resolved_cited_title |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_caa50477f333d1e3c48b | ctx_1cf74ef13884c4116a34 | Penn Treebank | dataset_or_database | named_object | PTB | 0.95 | sentence_text | True | True | True | strict | ptb_context_cue_present | context_cue_present | dataset | Building a Large Annotated Corpus of {E}nglish: The {P}enn {T}reebank |
| ctxr_7eebce6c90b1ab8d2d3d | ctx_8998a1ed39a479b81f71 | Penn Treebank | dataset_or_database | named_object | PTB | 0.95 | sentence_text | True | True | True | strict | ptb_context_cue_present | context_cue_present | dataset | Building a Large Annotated Corpus of {E}nglish: The {P}enn {T}reebank |
| ctxr_fb56106a126513c8b39c | ctx_211fedf8e97b27632796 | Penn Treebank | dataset_or_database | named_object | PTB | 0.95 | sentence_text | True | True | True | strict | ptb_context_cue_present | context_cue_present | unknown | Feature-Rich Part-of-Speech Tagging with a Cyclic Dependency Network |
| ctxr_cb37bb4fb9b009e8f4e2 | ctx_4e97d591466f79d5595b | Penn Treebank | dataset_or_database | named_object | PTB | 0.95 | sentence_text | True | True | True | strict | ptb_context_cue_present | context_cue_present | unknown | Named Entity Recognition in Tweets: An Experimental Study |
| ctxr_a5bc90bafa5096481006 | ctx_a2389b9f250486fc5b15 | Penn Treebank | dataset_or_database | named_object | PTB | 0.95 | sentence_text | True | True | True | strict | ptb_context_cue_present | context_cue_present | unknown | Building a Large Annotated Corpus of {E}nglish: The {P}enn {T}reebank |
| ctxr_b25c05e9a146e65cf7f4 | ctx_f5b38c07d06824ff48e2 | Penn Treebank | dataset_or_database | named_object | PTB | 0.85 | context_window_neighbor | True | True | True | broad | ptb_context_cue_present | context_cue_present;neighbor_context_match | dataset | Named Entity Recognition in Tweets: An Experimental Study |
| ctxr_9da88ff6c9701d288368 | ctx_0ec75856acac472eeb71 | Penn Treebank | dataset_or_database | named_object | PTB | 0.85 | sentence_text | True | True | True | strict | ptb_context_cue_present | weak_context_cue_missing;context_cue_present | dataset | Part-of-Speech Tagging for {T}witter: Annotation, Features, and Experiments |
| ctxr_e2ce85d756baa9a37469 | ctx_8dd81e0554f6a4b25988 | Penn Treebank | dataset_or_database | named_object | PTB | 0.95 | sentence_text | True | True | True | strict | ptb_context_cue_present | context_cue_present | introduction | {ISO}-{T}ime{ML} Event Extraction in {P}ersian Text |
| ctxr_6afbbcf00698a5f24d61 | ctx_8ac020175c1229527e3b | Penn Treebank | dataset_or_database | named_object | PTB | 0.95 | sentence_text | True | True | True | strict | ptb_context_cue_present | context_cue_present | unknown | Syntax Annotation for the {GENIA} Corpus |
| ctxr_2b097aea007a1bd9f688 | ctx_76e466e66355cf025d26 | Penn Treebank | dataset_or_database | named_object | PTB | 0.95 | sentence_text | True | True | True | strict | ptb_context_cue_present | context_cue_present | introduction | Probabilistic Models for Disambiguation of an {HPSG}-Based Chart Generator |
| ctxr_cf2236f2e0d3e5a90e55 | ctx_76e466e66355cf025d26 | Penn Treebank | dataset_or_database | named_object | PTB | 0.95 | sentence_text | True | True | True | strict | ptb_context_cue_present | context_cue_present | introduction | Robust {PCFG}-Based Generation Using Automatically Acquired {LFG} Approximations |
| ctxr_a8649a69846823fc94b3 | ctx_76e466e66355cf025d26 | Penn Treebank | dataset_or_database | named_object | PTB | 0.95 | sentence_text | True | True | True | strict | ptb_context_cue_present | context_cue_present | introduction | Perceptron Reranking for {CCG} Realization |
| ctxr_1f2b8616463c9f520bad | ctx_fdacf02a3d128f46640f | Penn Treebank | dataset_or_database | named_object | PTB | 0.95 | sentence_text | True | True | True | strict | ptb_context_cue_present | context_cue_present | introduction | Probabilistic Models for Disambiguation of an {HPSG}-Based Chart Generator |
| ctxr_378aa5922b6ffa1f3d10 | ctx_fdacf02a3d128f46640f | Penn Treebank | dataset_or_database | named_object | PTB | 0.95 | sentence_text | True | True | True | strict | ptb_context_cue_present | context_cue_present | introduction | Robust {PCFG}-Based Generation Using Automatically Acquired {LFG} Approximations |
| ctxr_9b62a06c4a1d1795320e | ctx_fdacf02a3d128f46640f | Penn Treebank | dataset_or_database | named_object | PTB | 0.95 | sentence_text | True | True | True | strict | ptb_context_cue_present | context_cue_present | introduction | Perceptron Reranking for {CCG} Realization |
| ctxr_53fdb7ae6587a457aa97 | ctx_81e26f980dbd53fbf479 | Penn Treebank | dataset_or_database | named_object | PTB | 0.95 | sentence_text | True | True | True | strict | ptb_context_cue_present | context_cue_present | introduction | Probabilistic Models for Disambiguation of an {HPSG}-Based Chart Generator |
| ctxr_e68e00448180ba81353f | ctx_81e26f980dbd53fbf479 | Penn Treebank | dataset_or_database | named_object | PTB | 0.95 | sentence_text | True | True | True | strict | ptb_context_cue_present | context_cue_present | introduction | Robust {PCFG}-Based Generation Using Automatically Acquired {LFG} Approximations |
| ctxr_f3371bd6e7c8f1a7482a | ctx_81e26f980dbd53fbf479 | Penn Treebank | dataset_or_database | named_object | PTB | 0.95 | sentence_text | True | True | True | strict | ptb_context_cue_present | context_cue_present | introduction | Perceptron Reranking for {CCG} Realization |
| ctxr_500d9944b021ea5096e1 | ctx_948d1a5e723b1030f317 | Penn Treebank | dataset_or_database | named_object | PTB | 0.95 | sentence_text | True | True | True | strict | ptb_context_cue_present | context_cue_present | introduction | Probabilistic Models for Disambiguation of an {HPSG}-Based Chart Generator |
| ctxr_a85be2b0b97f036b0441 | ctx_948d1a5e723b1030f317 | Penn Treebank | dataset_or_database | named_object | PTB | 0.95 | sentence_text | True | True | True | strict | ptb_context_cue_present | context_cue_present | introduction | Robust {PCFG}-Based Generation Using Automatically Acquired {LFG} Approximations |

## PTB Without Cue / Downgraded Examples
| context_id | source_context_id | canonical_name | object_type | object_category | surface_form | confidence | matched_in | allow_in_object_graph | graph_eligible | phase1_feature_eligible | graph_candidate_level | policy_reason | match_policy | normalized_section | resolved_cited_title |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_d2f7e10dccf772790070 | ctx_3052c12f694776848067 | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | 0.5 | sentence_text | False | False | True | none | ptb_context_cue_missing | weak_context_cue_missing;require_context_cue | dataset | The {S}tanford Typed Dependencies Representation |
| ctxr_e90af008e39f29815e47 | ctx_f62f61e3dee349a88de7 | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | 0.5 | sentence_text | False | False | True | none | ptb_context_cue_missing | weak_context_cue_missing;require_context_cue | unknown | {T}n{T} {--} A Statistical Part-of-Speech Tagger |
| ctxr_065657af5543ed78d301 | ctx_54d8e3a522dbb95e29ae | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | 0.5 | sentence_text | False | False | True | none | ptb_context_cue_missing | weak_context_cue_missing;require_context_cue | unknown | Named Entity Recognition in Tweets: An Experimental Study |
| ctxr_e5b701b6d20ba1498357 | ctx_58b37fe4234122671169 | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | 0.5 | sentence_text | False | False | True | none | ptb_context_cue_missing | weak_context_cue_missing;require_context_cue | unknown | Part-of-Speech Tagging for {T}witter: Annotation, Features, and Experiments |
| ctxr_cd65f52db26c481dcc6b | ctx_32796ad2ab4ffbf6584b | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | 0.4 | context_window_neighbor | False | False | False | none | ptb_context_cue_missing | weak_context_cue_missing;neighbor_context_match;require_context_cue | experiment | Top Accuracy and Fast Dependency Parsing is not a Contradiction |
| ctxr_f4c827a51a4c2a36b5a7 | ctx_e3cad2ed818bb95f1fb9 | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | 0.5 | sentence_text | False | False | True | none | ptb_context_cue_missing | weak_context_cue_missing;require_context_cue | unknown | Named Entity Recognition in Tweets: An Experimental Study |
| ctxr_d0a9e60ca0cad6aefb16 | ctx_5018016206e293ddeba8 | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | 0.5 | sentence_text | False | False | True | none | ptb_context_cue_missing | weak_context_cue_missing;require_context_cue | unknown | Improved Part-of-Speech Tagging for Online Conversational Text with Word Clusters |
| ctxr_d69a50583fc1f5638082 | ctx_b3851c4e14540df5ea54 | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | 0.5 | sentence_text | False | False | True | none | ptb_context_cue_missing | weak_context_cue_missing;require_context_cue | unknown | The {P}enn {T}reebank: Annotating Predicate Argument Structure |
| ctxr_4d629f70f30300c8a7e0 | ctx_0ef74772a86415b1e298 | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | 0.5 | sentence_text | False | False | True | none | ptb_context_cue_missing | weak_context_cue_missing;require_context_cue | introduction | {PLCFRS} Parsing of {E}nglish Discontinuous Constituents |
| ctxr_fca466f7c46193cf633b | ctx_cd8b752d71b28d1baf3d | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | 0.5 | sentence_text | False | False | True | none | ptb_context_cue_missing | weak_context_cue_missing;require_context_cue | introduction | {PLCFRS} Parsing of {E}nglish Discontinuous Constituents |
| ctxr_d859659758e453381153 | ctx_96e46d34850ef2c92775 | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | 0.4 | context_window_neighbor | False | False | False | none | ptb_context_cue_missing | weak_context_cue_missing;neighbor_context_match;require_context_cue | unknown | Accurate Unlexicalized Parsing |
| ctxr_1b7b716079f3ae244511 | ctx_d67ef27d854e5c57ee31 | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | 0.4 | context_window_neighbor | False | False | False | none | ptb_context_cue_missing | weak_context_cue_missing;neighbor_context_match;require_context_cue | unknown | A Fast and Accurate Dependency Parser using Neural Networks |
| ctxr_0ea4495d0afa47383b6b | ctx_afe12ef282b8289e7875 | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | 0.4 | context_window_neighbor | False | False | False | none | ptb_context_cue_missing | weak_context_cue_missing;neighbor_context_match;require_context_cue | dataset | Temporal Ontology and Temporal Reference |
| ctxr_605607b48f9bafd412ab | ctx_2cbec3e9a2d7931aa96d | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | 0.5 | sentence_text | False | False | True | none | ptb_context_cue_missing | weak_context_cue_missing;require_context_cue | introduction | Building a Large Annotated Corpus of {E}nglish: The {P}enn {T}reebank |
| ctxr_982d273dbc84aceeee0c | ctx_f87c8e107da2feafd461 | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | 0.5 | sentence_text | False | False | True | none | ptb_context_cue_missing | weak_context_cue_missing;require_context_cue | introduction | From {T}ree{B}ank to {P}rop{B}ank |
| ctxr_eba17a4f9d74deca1540 | ctx_d1c30db8761ff4bf8967 | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | 0.5 | sentence_text | False | False | True | none | ptb_context_cue_missing | weak_context_cue_missing;require_context_cue | unknown | Attribution and the (Non-)Alignment of Syntactic and Discourse Arguments of Connectives |
| ctxr_494161a5316eec1bd588 | ctx_6db9db8f1b148235ad46 | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | 0.5 | sentence_text | False | False | True | none | ptb_context_cue_missing | weak_context_cue_missing;require_context_cue | introduction | {CCG}bank: A Corpus of {CCG} Derivations and Dependency Structures Extracted from the {P}enn {T}reebank |
| ctxr_11d594ca118d2c064e60 | ctx_d37b1899591e0546c0fd | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | 0.4 | context_window_neighbor | False | False | False | none | ptb_context_cue_missing | weak_context_cue_missing;neighbor_context_match;require_context_cue | introduction | Accurate Unlexicalized Parsing |
| ctxr_3dbf9121aa5be39d9a33 | ctx_fd2e018c1c99acf069da | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | 0.4 | context_window_neighbor | False | False | False | none | ptb_context_cue_missing | weak_context_cue_missing;neighbor_context_match;require_context_cue | introduction | Wide-Coverage Efficient Statistical Parsing with {CCG} and Log-Linear Models |
| ctxr_c1e51204081f77558e20 | ctx_f8d07187a904a3dacd4a | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | 0.5 | sentence_text | False | False | True | none | ptb_context_cue_missing | weak_context_cue_missing;require_context_cue | experiment | {G}lo{V}e: Global Vectors for Word Representation |

## Uppercase Transformer Examples
| context_id | source_context_id | canonical_name | object_type | object_category | surface_form | confidence | matched_in | allow_in_object_graph | graph_eligible | phase1_feature_eligible | graph_candidate_level | policy_reason | match_policy | normalized_section | resolved_cited_title |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_ab7617f2f9592a20ff6a | ctx_8cd9f7d7ef72314a504d | Transformer | model | named_object | Transformers | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | introduction | Rethinking Complex Neural Network Architectures for Document Classification |
| ctxr_7be2d2360c50b43f3fcd | ctx_8cd9f7d7ef72314a504d | Transformer | model | named_object | Transformers | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | introduction | Nikolov-Radivchev at {S}em{E}val-2019 Task 6: Offensive Tweet Classification with {BERT} and Ensembles |
| ctxr_082cd21660027a05e63f | ctx_2c78251489008a76e2b1 | Transformer | model | named_object | Transformers | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | introduction | Rethinking Complex Neural Network Architectures for Document Classification |
| ctxr_89e33f91e0ca4aa47fe6 | ctx_2c78251489008a76e2b1 | Transformer | model | named_object | Transformers | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | introduction | Nikolov-Radivchev at {S}em{E}val-2019 Task 6: Offensive Tweet Classification with {BERT} and Ensembles |
| ctxr_8a018d33416b7ece9ac6 | ctx_e7adf803f3b0416013ce | Transformer | model | named_object | Transformers | 0.95 | sentence_text | True | True | True | strict | default_policy | standard | introduction | {BERT}: Pre-training of Deep Bidirectional Transformers for Language Understanding |
| ctxr_11674fda9622e62cf411 | ctx_0a475cf6f07be6508002 | Transformer | model | named_object | Transformers | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | introduction | {JRC} Eurovoc Indexer {JEX} - A freely available multi-label categorisation tool |
| ctxr_29fb8dc8cb651ec8b717 | ctx_5e4f13d97190a50a966e | Transformer | model | named_object | Transformer | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | unknown | Personalizing Dialogue Agents: {I} have a dog, do you have pets too? |
| ctxr_d8985cbc91aaf9f28e3f | ctx_c51fbd7cf7e26109a828 | Transformer | model | named_object | Transformers | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | dataset | {P}arl{AI}: A Dialog Research Software Platform |
| ctxr_ff1cdc9b1334d29ba81d | ctx_c8d37acdc557d3e4d35b | Transformer | model | named_object | Transformer | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | introduction | A Probabilistic {E}arley Parser as a Psycholinguistic Model |
| ctxr_4244e92377d00a09dc34 | ctx_074c6992fcdf673f8431 | Transformer | model | named_object | Transformer | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | introduction | A Probabilistic {E}arley Parser as a Psycholinguistic Model |
| ctxr_a48c744ca6bbc3b569a4 | ctx_c17a6f2ece1d01d4cf48 | Transformer | model | named_object | Transformer model | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | model | {KIT}{'}s Multilingual Neural Machine Translation systems for {IWSLT} 2017 |
| ctxr_36ac0506bf347a744df4 | ctx_42c8ef17af15306f6b8a | Transformer | model | named_object | Transformer model | 0.95 | sentence_text | True | True | True | strict | default_policy | standard | model | {E}nglish-{C}zech Systems in {WMT}19: Document-Level Transformer |
| ctxr_3496ed73243783b0de75 | ctx_48d4ace69284dfca39c5 | Transformer | model | named_object | Transformer model | 0.95 | sentence_text | True | True | True | strict | default_policy | standard | model | {E}nglish-{C}zech Systems in {WMT}19: Document-Level Transformer |
| ctxr_159cb3ad56563fda84a8 | ctx_2a89e67a3c11ebaaf608 | Transformer | model | named_object | Transformers | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | introduction | Improving Coreference Resolution by Using Conversational Metadata |
| ctxr_e7c1af75746d4bf8f397 | ctx_7cf7993231b51533c9bb | Transformer | model | named_object | Transformers | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | implementation | Revealing the Myth of Higher-Order Inference in Coreference Resolution |
| ctxr_7f22e45dac4981784868 | ctx_d9060786aa633d433e35 | Transformer | model | named_object | Transformers | 0.95 | sentence_text | True | True | True | strict | default_policy | standard | implementation | {S}pan{BERT}: Improving Pre-training by Representing and Predicting Spans |
| ctxr_1b7f478e049f18a031f6 | ctx_de586ac549638e1b7851 | Transformer | model | named_object | Transformers | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | implementation | {BERT} for Coreference Resolution: Baselines and Analysis |
| ctxr_01c7601c28e61477de53 | ctx_51091bce3c8762073247 | Transformer | model | named_object | Transformers | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | unknown | Revealing the Myth of Higher-Order Inference in Coreference Resolution |
| ctxr_373bdebb50348bcce6e0 | ctx_0a90ba50667c8484f47d | Transformer | model | named_object | Transformer | 0.85 | context_window_neighbor | True | True | True | broad | default_policy | standard;neighbor_context_match | experiment | {M}arian: Fast Neural Machine Translation in {C}++ |
| ctxr_2dff16ec5e2697def717 | ctx_39454be1f8c1d574c63e | Transformer | model | named_object | Transformer | 0.95 | sentence_text | True | True | True | strict | default_policy | standard | experiment | Sockeye 2: A Toolkit for Neural Machine Translation |

## Lowercase transformer Downgraded Examples
| context_id | source_context_id | canonical_name | object_type | object_category | surface_form | confidence | matched_in | allow_in_object_graph | graph_eligible | phase1_feature_eligible | graph_candidate_level | policy_reason | match_policy | normalized_section | resolved_cited_title |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_aa1b7e3f43fffb4f92b0 | ctx_3bdef62d8f1f790095de | Transformer | model | generic_architecture | transformer | 0.55 | context_window_neighbor | False | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture;neighbor_context_match | unknown | {HIBERT}: Document Level Pre-training of Hierarchical Bidirectional Transformers for Document Summarization |
| ctxr_686b28273ac8dd11a1b3 | ctx_c41daf6c5fd829c76a3c | Transformer | model | generic_architecture | transformer | 0.65 | sentence_text | False | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture | unknown | Transformers: State-of-the-Art Natural Language Processing |
| ctxr_65fdc1db1863225e9bf2 | ctx_4104bb7826f2a45118f5 | Transformer | model | generic_architecture | transformer | 0.65 | sentence_text | False | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture | related_work | Composed Variational Natural Language Generation for Few-shot Intents |
| ctxr_0f075d7177b37dcc6ea4 | ctx_b7c30588a8e85f0d4b2b | Transformer | model | generic_architecture | transformer | 0.65 | sentence_text | False | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture | related_work | Paraphrase Generation for Semi-Supervised Learning in {NLU} |
| ctxr_97857c8cfe503e3e220c | ctx_a84e8a8247982b797193 | Transformer | model | generic_architecture | transformer | 0.65 | sentence_text | False | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture | related_work | Data-Efficient Paraphrase Generation to Bootstrap Intent Classification and Slot Labeling for New Features in Task-Oriented Dialog Systems |
| ctxr_0fcf10831c6a097b32dd | ctx_74e3f883bbaad0198f60 | Transformer | model | generic_architecture | transformer | 0.55 | context_window_neighbor | False | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture;neighbor_context_match | unknown | Supervised Learning of Universal Sentence Representations from Natural Language Inference Data |
| ctxr_d8822be9e73f66a9b9ad | ctx_84c4bb967b5a0c041af8 | Transformer | model | generic_architecture | transformer | 0.65 | sentence_text | False | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture | unknown | {BERT}: Pre-training of Deep Bidirectional Transformers for Language Understanding |
| ctxr_8c2cb27855cf6ecef874 | ctx_f79d47113149cd51feca | Transformer | model | generic_architecture | transformer | 0.55 | context_window_neighbor | False | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture;neighbor_context_match | unknown | Featureless Domain-Specific Term Extraction with Minimal Labelled Data |
| ctxr_8994643867d5822698fe | ctx_dbdfce9d3fd995a7b42d | Transformer | model | generic_architecture | transformer | 0.65 | sentence_text | False | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture | introduction | {T}a{BERT}: Pretraining for Joint Understanding of Textual and Tabular Data |
| ctxr_8994643867d5822698fe | ctx_dbdfce9d3fd995a7b42d | Transformer | model | generic_architecture | transformers | 0.55 | context_window_neighbor | False | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture;neighbor_context_match | introduction | {T}a{BERT}: Pretraining for Joint Understanding of Textual and Tabular Data |
| ctxr_b46cb35851fba6437937 | ctx_9e6480dc9b82614e93eb | Transformer | model | generic_architecture | transformer | 0.65 | sentence_text | False | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture | introduction | {T}a{P}as: Weakly Supervised Table Parsing via Pre-training |
| ctxr_b46cb35851fba6437937 | ctx_9e6480dc9b82614e93eb | Transformer | model | generic_architecture | transformers | 0.55 | context_window_neighbor | False | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture;neighbor_context_match | introduction | {T}a{P}as: Weakly Supervised Table Parsing via Pre-training |
| ctxr_5867a60d23965cd86667 | ctx_1a51297ac01023237310 | Transformer | model | generic_architecture | transformer | 0.65 | sentence_text | False | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture | unknown | {T}a{P}as: Weakly Supervised Table Parsing via Pre-training |
| ctxr_ebdda9bdfd8f02795cfa | ctx_55212ff08f3f36bea566 | Transformer | model | generic_architecture | transformer | 0.65 | sentence_text | False | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture | unknown | {T}a{BERT}: Pretraining for Joint Understanding of Textual and Tabular Data |
| ctxr_46bab1ef85d23e83609d | ctx_fd0e35228dfe1128235a | Transformer | model | generic_architecture | transformer | 0.65 | sentence_text | False | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture | unknown | {T}a{P}as: Weakly Supervised Table Parsing via Pre-training |
| ctxr_f11efdbf30eca66b44c4 | ctx_a9f4fdce1423fcce9221 | Transformer | model | generic_architecture | transformer | 0.65 | sentence_text | False | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture | unknown | {T}a{BERT}: Pretraining for Joint Understanding of Textual and Tabular Data |
| ctxr_78ae080aec50f80badc4 | ctx_2dda541d5547a03d31b6 | Transformer | model | generic_architecture | transformers | 0.55 | context_window_neighbor | False | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture;neighbor_context_match | related_work | {BART}: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension |
| ctxr_4415ccd79a4fcc305d36 | ctx_98711c830d549d8d518b | Transformer | model | generic_architecture | transformer | 0.65 | sentence_text | False | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture | related_work | {S}pan{BERT}: Improving Pre-training by Representing and Predicting Spans |
| ctxr_a73e183cafcdab6ffd3a | ctx_122286f339bd783db9f5 | Transformer | model | generic_architecture | transformers | 0.65 | sentence_text | False | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture | unknown | Dense Passage Retrieval for Open-Domain Question Answering |
| ctxr_73c224b6afd66d9ac8fe | ctx_522620569201dafd1bdb | Transformer | model | generic_architecture | transformer | 0.55 | context_window_neighbor | False | False | True | none | lowercase_transformer_feature_only | lowercase_generic_architecture;neighbor_context_match | model | Group-wise Contrastive Learning for Neural Dialogue Generation |

## seq2seq Kept / Downgraded Examples
| context_id | source_context_id | canonical_name | object_type | object_category | surface_form | confidence | matched_in | allow_in_object_graph | graph_eligible | phase1_feature_eligible | graph_candidate_level | policy_reason | match_policy | normalized_section | resolved_cited_title |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_f8dcc633c98228a064d4 | ctx_9a50d63359c3ead45b32 | seq2seq | model | named_object | sequence-to-sequence | 0.75 | context_window_neighbor | True | True | True | none | seq2seq_context_cue_present | context_cue_present;neighbor_context_match | introduction | Advances in domain independent linear text segmentation |
| ctxr_510b44c52aa7f5d8c1e4 | ctx_04ec41b760cfe12e25e0 | seq2seq | model | named_object | seq2seq | 0.85 | sentence_text | True | True | True | strict | seq2seq_context_cue_present | context_cue_present | related_work | A Neural Network Approach to Context-Sensitive Generation of Conversational Responses |
| ctxr_b6f126193997ab840ece | ctx_04ec41b760cfe12e25e0 | seq2seq | model | named_object | seq2seq | 0.85 | sentence_text | True | True | True | strict | seq2seq_context_cue_present | context_cue_present | related_work | A Persona-Based Neural Conversation Model |
| ctxr_d8a8f729eac30739b9bb | ctx_285fec441757cc4260e5 | seq2seq | model | named_object | seq2seq | 0.85 | sentence_text | True | True | True | strict | seq2seq_context_cue_present | context_cue_present | related_work | A Neural Network Approach to Context-Sensitive Generation of Conversational Responses |
| ctxr_869a0ebf2573f5cc9855 | ctx_285fec441757cc4260e5 | seq2seq | model | named_object | seq2seq | 0.85 | sentence_text | True | True | True | strict | seq2seq_context_cue_present | context_cue_present | related_work | A Persona-Based Neural Conversation Model |
| ctxr_e30badd9abe205b9b24c | ctx_beeebe74ba7f9c071233 | seq2seq | model | named_object | seq2seq | 0.85 | sentence_text | True | True | True | strict | seq2seq_context_cue_present | context_cue_present | related_work | A Neural Network Approach to Context-Sensitive Generation of Conversational Responses |
| ctxr_4d5a6ae64d3722d3981d | ctx_beeebe74ba7f9c071233 | seq2seq | model | named_object | seq2seq | 0.85 | sentence_text | True | True | True | strict | seq2seq_context_cue_present | context_cue_present | related_work | A Persona-Based Neural Conversation Model |
| ctxr_7411a8bdc389811286d8 | ctx_9423fcf1c31338a556a4 | seq2seq | model | named_object | seq2seq | 0.85 | sentence_text | True | True | True | strict | seq2seq_context_cue_present | context_cue_present | related_work | A Neural Network Approach to Context-Sensitive Generation of Conversational Responses |
| ctxr_c1a557bcb858aef9f904 | ctx_9423fcf1c31338a556a4 | seq2seq | model | named_object | seq2seq | 0.85 | sentence_text | True | True | True | strict | seq2seq_context_cue_present | context_cue_present | related_work | A Persona-Based Neural Conversation Model |
| ctxr_38652b77e41dd4a6cb05 | ctx_42a02f559e897fda75dc | seq2seq | model | named_object | seq2seq | 0.75 | context_window_neighbor | True | True | True | none | seq2seq_context_cue_present | context_cue_present;neighbor_context_match | related_work | Personalizing Dialogue Agents: {I} have a dog, do you have pets too? |
| ctxr_29fb8dc8cb651ec8b717 | ctx_5e4f13d97190a50a966e | seq2seq | model | named_object | Seq2Seq | 0.5 | sentence_text | False | False | True | none | seq2seq_context_cue_present | weak_context_cue_missing;context_cue_present | unknown | Personalizing Dialogue Agents: {I} have a dog, do you have pets too? |
| ctxr_b3abb75cd988299e374a | ctx_8ff98d0062f102c69848 | seq2seq | model | named_object | encoder-decoder | 0.85 | sentence_text | True | True | True | strict | seq2seq_context_cue_present | context_cue_present | introduction | Data-Efficient Paraphrase Generation to Bootstrap Intent Classification and Slot Labeling for New Features in Task-Oriented Dialog Systems |
| ctxr_fd8ae860bb1047e0ec7d | ctx_c0b8cf6af1fad8cf6679 | seq2seq | model | named_object | encoder-decoder | 0.75 | context_window_neighbor | True | True | True | none | seq2seq_context_cue_present | context_cue_present;neighbor_context_match | related_work | Generating Sentences from a Continuous Space |
| ctxr_0902c9c5db455e4d34f8 | ctx_1f70a142b3f70cdcb19f | seq2seq | model | named_object | encoder-decoder | 0.75 | context_window_neighbor | True | True | True | none | seq2seq_context_cue_present | context_cue_present;neighbor_context_match | related_work | Controlled Text Generation for Data Augmentation in Intelligent Artificial Agents |
| ctxr_0902c9c5db455e4d34f8 | ctx_1f70a142b3f70cdcb19f | seq2seq | model | named_object | seq2seq | 0.75 | context_window_neighbor | True | True | True | none | seq2seq_context_cue_present | context_cue_present;neighbor_context_match | related_work | Controlled Text Generation for Data Augmentation in Intelligent Artificial Agents |
| ctxr_65fdc1db1863225e9bf2 | ctx_4104bb7826f2a45118f5 | seq2seq | model | named_object | seq2seq | 0.75 | context_window_neighbor | True | True | True | none | seq2seq_context_cue_present | context_cue_present;neighbor_context_match | related_work | Composed Variational Natural Language Generation for Few-shot Intents |
| ctxr_0f075d7177b37dcc6ea4 | ctx_b7c30588a8e85f0d4b2b | seq2seq | model | named_object | seq2seq | 0.85 | sentence_text | True | True | True | strict | seq2seq_context_cue_present | context_cue_present | related_work | Paraphrase Generation for Semi-Supervised Learning in {NLU} |
| ctxr_14243579effcdcfe8d1a | ctx_e73a6e0de85bc58f8760 | seq2seq | model | named_object | seq2seq | 0.85 | sentence_text | True | True | True | strict | seq2seq_context_cue_present | context_cue_present | model | Controlled Text Generation for Data Augmentation in Intelligent Artificial Agents |
| ctxr_14243579effcdcfe8d1a | ctx_e73a6e0de85bc58f8760 | seq2seq | model | named_object | seq2seq | 0.85 | sentence_text | True | True | True | strict | seq2seq_context_cue_present | context_cue_present | model | Controlled Text Generation for Data Augmentation in Intelligent Artificial Agents |
| ctxr_6c4b8d1fa22b2270218b | ctx_c7c996865f319d884467 | seq2seq | model | named_object | seq2seq | 0.85 | sentence_text | True | True | True | strict | seq2seq_context_cue_present | context_cue_present | model | Controlled Text Generation for Data Augmentation in Intelligent Artificial Agents |

## Cited-Title Object Profile Examples
| context_id | source_context_id | canonical_name | object_type | object_category | surface_form | confidence | matched_in | allow_in_object_graph | graph_eligible | phase1_feature_eligible | graph_candidate_level | policy_reason | match_policy | normalized_section | resolved_cited_title |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_6ec7b60115b4d5e6dcf1 | ctx_8ee4e60043981a38782e | CRF | method | named_object | CRF | 0.95 | resolved_cited_title | False | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard | introduction | Dependency Tree-based Sentiment Classification using {CRF}s with Hidden Variables |
| ctxr_5cf962d606f5bb683922 | ctx_ef689b946fb8a015c84f | BLEU | metric | named_object | BLEU | 0.95 | resolved_cited_title | False | False | False | none | named_metric_graph_eligible;resolved_cited_title_profile_not_direct_context_evidence | standard | unknown | Interpreting {BLEU}/{NIST} Scores: How Much Improvement do We Need to Have a Better System? |
| ctxr_f2fc5d3298a427695aa8 | ctx_6414e0d8fa5fc825be29 | HMM | method | named_object | HMM | 0.95 | resolved_cited_title | False | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard | introduction | {HMM}-Based Word Alignment in Statistical Translation |
| ctxr_52bb41aed58f89be7736 | ctx_5a97bb6434d27f5918d4 | HMM | method | named_object | HMM | 0.95 | resolved_cited_title | False | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard | introduction | {HMM}-Based Word Alignment in Statistical Translation |
| ctxr_fa827b5872437cd3481b | ctx_60363e917b2f927cbc6f | HMM | method | named_object | HMM | 0.95 | resolved_cited_title | False | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard | introduction | {HMM}-Based Word Alignment in Statistical Translation |
| ctxr_348ed735539164c215ec | ctx_330dcf7dff7e71dc926f | HMM | method | named_object | HMM | 0.95 | resolved_cited_title | False | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard | introduction | {HMM}-Based Word Alignment in Statistical Translation |
| ctxr_c0ecda4d16dd1fa0c113 | ctx_29315694bbce4b7e0b4e | GloVe | model | named_object | Global Vectors for Word Representation | 0.95 | resolved_cited_title | False | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard | introduction | {G}lo{V}e: Global Vectors for Word Representation |
| ctxr_aa1b7e3f43fffb4f92b0 | ctx_3bdef62d8f1f790095de | Transformer | model | named_object | Transformers | 0.95 | resolved_cited_title | False | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard | unknown | {HIBERT}: Document Level Pre-training of Hierarchical Bidirectional Transformers for Document Summarization |
| ctxr_4ece378a815889ac5290 | ctx_b184efd8391ef2e33b3d | Transformer | model | named_object | Transformers | 0.95 | resolved_cited_title | False | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard | unknown | {HIBERT}: Document Level Pre-training of Hierarchical Bidirectional Transformers for Document Summarization |
| ctxr_74d9fd93d7822354fb0f | ctx_e9e132f9224a9dab7d52 | Transformer | model | named_object | Transformers | 0.95 | resolved_cited_title | False | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard | results | {HIBERT}: Document Level Pre-training of Hierarchical Bidirectional Transformers for Document Summarization |
| ctxr_135f1a3a6cc1d78491d8 | ctx_d7e25a73c7aea82de3b1 | Transformer | model | named_object | Transformers | 0.95 | resolved_cited_title | False | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard | conclusion | {HIBERT}: Document Level Pre-training of Hierarchical Bidirectional Transformers for Document Summarization |
| ctxr_c7102908c01762631958 | ctx_5da2fc6a58942d8f4475 | Transformer | model | named_object | Transformers | 0.95 | resolved_cited_title | False | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard | conclusion | {HIBERT}: Document Level Pre-training of Hierarchical Bidirectional Transformers for Document Summarization |
| ctxr_30ddd765062e3abcb42a | ctx_db8d0553710501958f1e | seq2seq | model | named_object | Sequence to Sequence | 0.85 | resolved_cited_title | False | False | False | none | seq2seq_context_cue_present;resolved_cited_title_profile_not_direct_context_evidence | context_cue_present | conclusion | Semantic Label Smoothing for Sequence to Sequence Problems |
| ctxr_a66cd052e5042059ea1b | ctx_b100d59132cbd267913b | seq2seq | model | named_object | Sequence to Sequence | 0.85 | resolved_cited_title | False | False | False | none | seq2seq_context_cue_present;resolved_cited_title_profile_not_direct_context_evidence | context_cue_present | conclusion | Semantic Label Smoothing for Sequence to Sequence Problems |
| ctxr_92a39f9773361a0b10a6 | ctx_d0e150d930b1702a75bb | seq2seq | model | named_object | Sequence to Sequence | 0.85 | resolved_cited_title | False | False | False | none | seq2seq_context_cue_present;resolved_cited_title_profile_not_direct_context_evidence | context_cue_present | conclusion | Semantic Label Smoothing for Sequence to Sequence Problems |
| ctxr_013ff32b6a1daff30375 | ctx_c956c98986bcd3569d1a | seq2seq | model | named_object | Sequence to Sequence | 0.85 | resolved_cited_title | False | False | False | none | seq2seq_context_cue_present;resolved_cited_title_profile_not_direct_context_evidence | context_cue_present | conclusion | Semantic Label Smoothing for Sequence to Sequence Problems |
| ctxr_7be2d2360c50b43f3fcd | ctx_8cd9f7d7ef72314a504d | BERT | model | named_object | BERT | 0.95 | resolved_cited_title | False | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard | introduction | Nikolov-Radivchev at {S}em{E}val-2019 Task 6: Offensive Tweet Classification with {BERT} and Ensembles |
| ctxr_89e33f91e0ca4aa47fe6 | ctx_2c78251489008a76e2b1 | BERT | model | named_object | BERT | 0.95 | resolved_cited_title | False | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard | introduction | Nikolov-Radivchev at {S}em{E}val-2019 Task 6: Offensive Tweet Classification with {BERT} and Ensembles |
| ctxr_8a018d33416b7ece9ac6 | ctx_e7adf803f3b0416013ce | BERT | model | named_object | BERT | 0.95 | resolved_cited_title | False | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard | introduction | {BERT}: Pre-training of Deep Bidirectional Transformers for Language Understanding |
| ctxr_8a018d33416b7ece9ac6 | ctx_e7adf803f3b0416013ce | Transformer | model | named_object | Transformers | 0.95 | resolved_cited_title | False | False | False | none | resolved_cited_title_profile_not_direct_context_evidence | standard | introduction | {BERT}: Pre-training of Deep Bidirectional Transformers for Language Understanding |
