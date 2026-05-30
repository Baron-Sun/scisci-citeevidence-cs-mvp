# Object Matching Sample Refined Report

## Inputs
- Contexts: `data/processed/analysis_ready_strong_contexts.parquet`
- Registry: `configs/object_registry_seed.yaml`

## Outputs
- Context object mentions sample: `data/processed/object_mentions_sample_refined.parquet`
- Cited-title object profiles sample: `data/processed/cited_title_object_profiles_sample.parquet`
- Manual object mention review sample: `data/processed/object_mentions_review_sample.csv`

## Core Metrics
| metric | value |
| --- | --- |
| input context rows processed | 50000 |
| configured limit | 50000 |
| registry objects | 36 |
| raw mentions before deduplication | 27781 |
| deduplicated mentions after deduplication | 15993 |
| deduplicated_count | 11788 |
| context mentions count | 15993 |
| cited title profile count | 3425 |
| contexts with at least one object mention | 10870 |
| total object mentions | 15993 |
| negative alias blocked count | 0 |
| blocked_by_context_cue count | 0 |
| case blocked count | 132 |
| low_confidence_match count | 2486 |

## Object Mentions By Object Type
| object_type | mentions |
| --- | --- |
| metric | 4567 |
| model | 3981 |
| dataset_or_database | 2464 |
| method | 2145 |
| software_or_tool | 1689 |
| benchmark_or_protocol | 1147 |

## Object Mentions By Object Category
| object_category | mentions |
| --- | --- |
| named_object | 13507 |
| generic_metric | 2183 |
| generic_architecture | 243 |
| ambiguous_short_alias | 60 |

## Object Mentions By allow_in_object_graph
| allow_in_object_graph | mentions |
| --- | --- |
| True | 13507 |
| False | 2486 |

## Top 50 Matched Objects
| object_id | canonical_name | object_type | mentions |
| --- | --- | --- | --- |
| obj_bleu | BLEU | metric | 1893 |
| obj_accuracy | accuracy | metric | 1450 |
| obj_crf | CRF | method | 1403 |
| obj_bert | BERT | model | 1056 |
| obj_lstm | LSTM | model | 1033 |
| obj_wordnet | WordNet | dataset_or_database | 992 |
| obj_moses | Moses | software_or_tool | 811 |
| obj_penn_treebank | Penn Treebank | dataset_or_database | 801 |
| obj_transformer | Transformer | model | 787 |
| obj_giza | GIZA++ | software_or_tool | 653 |
| obj_semeval | SemEval | benchmark_or_protocol | 560 |
| obj_hmm | HMM | method | 556 |
| obj_f1 | F1 | metric | 555 |
| obj_seq2seq | seq2seq | model | 519 |
| obj_wmt | WMT | benchmark_or_protocol | 397 |
| obj_meteor | METEOR | metric | 297 |
| obj_word2vec | word2vec | model | 273 |
| obj_framenet | FrameNet | dataset_or_database | 271 |
| obj_rouge | ROUGE | metric | 194 |
| obj_attention_mechanism | attention mechanism | method | 186 |
| obj_perplexity | perplexity | metric | 178 |
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
| obj_spacy | spaCy | software_or_tool | 25 |
| obj_multinli | MultiNLI | dataset_or_database | 6 |
| obj_superglue | SuperGLUE | benchmark_or_protocol | 5 |

## Top 50 Surface Forms
| surface_form | canonical_name | object_type | mentions |
| --- | --- | --- | --- |
| BLEU | BLEU | metric | 1555 |
| accuracy | accuracy | metric | 1399 |
| BERT | BERT | model | 973 |
| LSTM | LSTM | model | 881 |
| WordNet | WordNet | dataset_or_database | 817 |
| CRF | CRF | method | 727 |
| Moses | Moses | software_or_tool | 577 |
| GIZA++ | GIZA++ | software_or_tool | 484 |
| SemEval | SemEval | benchmark_or_protocol | 482 |
| Penn Treebank | Penn Treebank | dataset_or_database | 475 |
| HMM | HMM | method | 401 |
| Transformer | Transformer | model | 386 |
| WMT | WMT | benchmark_or_protocol | 384 |
| CRFs | CRF | method | 294 |
| BLEU score | BLEU | metric | 288 |
| PTB | Penn Treebank | dataset_or_database | 271 |
| FrameNet | FrameNet | dataset_or_database | 258 |
| METEOR | METEOR | metric | 244 |
| transformer | Transformer | model | 210 |
| F1 | F1 | metric | 207 |
| encoder-decoder | seq2seq | model | 206 |
| word2vec | word2vec | model | 184 |
| ROUGE | ROUGE | metric | 179 |
| perplexity | perplexity | metric | 163 |
| attention mechanism | attention mechanism | method | 156 |
| Giza++ | GIZA++ | software_or_tool | 148 |
| PropBank | PropBank | dataset_or_database | 146 |
| Conditional Random Fields | CRF | method | 145 |
| F-score | F1 | metric | 137 |
| ELMo | ELMo | model | 126 |
| sequence-to-sequence | seq2seq | model | 118 |
| GloVe | GloVe | model | 113 |
| F-measure | F1 | metric | 110 |
| seq2seq | seq2seq | model | 108 |
| Moses toolkit | Moses | software_or_tool | 91 |
| Wordnet | WordNet | dataset_or_database | 87 |
| Conditional Random Field | CRF | method | 82 |
| wordnet | WordNet | dataset_or_database | 82 |
| MOSES | Moses | software_or_tool | 80 |
| SQuAD | SQuAD | dataset_or_database | 77 |
| Word2Vec | word2vec | model | 77 |
| OntoNotes | OntoNotes | dataset_or_database | 69 |
| Transformers | Transformer | model | 69 |
| Stanford CoreNLP | Stanford CoreNLP | software_or_tool | 64 |
| conditional random field | CRF | method | 63 |
| conditional random fields | CRF | method | 61 |
| CoNLL'03 | CoNLL-2003 | benchmark_or_protocol | 57 |
| OPUS | OPUS | software_or_tool | 53 |
| Meteor | METEOR | metric | 50 |
| F1 score | F1 | metric | 47 |

## Matches By Normalized Section
| normalized_section | mentions |
| --- | --- |
| unknown | 4553 |
| introduction | 3600 |
| related_work | 2578 |
| experiment | 977 |
| dataset | 807 |
| model | 727 |
| evaluation | 707 |
| method | 597 |
| results | 517 |
| conclusion | 222 |
| background | 202 |
| system_description | 170 |
| abstract | 108 |
| discussion | 105 |
| implementation | 58 |
| analysis | 49 |
| task_definition | 10 |
| error_analysis | 6 |

## Matches By Matched In
| matched_in | mentions |
| --- | --- |
| sentence_text | 9903 |
| context_window_neighbor | 6090 |

## Examples Per Object Type
| example_group | context_id | source_context_id | citing_paper_id | resolved_cited_acl_id | resolved_cited_title | normalized_section | raw_section_name | object_id | canonical_name | object_type | object_category | surface_form | normalized_surface | match_type | char_start | char_end | confidence | matched_in | match_policy | allow_in_object_graph | provenance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| benchmark_or_protocol | ctxr_f6863fcab52657a5c16e | ctx_f31d14d5a204a23fdb80 | R13-1044 | S10-1049 | {ISI}: Automatic Classification of Relations Between Nominals Using a Maximum Entropy Classifier | related_work | Related work | obj_semeval | SemEval | benchmark_or_protocol | named_object | SemEval | semeval | exact_alias | 13 | 20 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_semeval;alias=SemEval |
| benchmark_or_protocol | ctxr_5d48c41b1f5fe52a0a74 | ctx_2e80df002a498416e487 | 2020.nlp4convai-1.15 | P18-1198 | What you can cram into a single {\$}{\&}!{\#}* vector: Probing sentence embeddings for linguistic properties | related_work | Related Work | obj_glue | GLUE | benchmark_or_protocol | named_object | GLUE | glue | exact_alias | 543 | 547 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_glue;alias=GLUE |
| benchmark_or_protocol | ctxr_5d48c41b1f5fe52a0a74 | ctx_2e80df002a498416e487 | 2020.nlp4convai-1.15 | P18-1198 | What you can cram into a single {\$}{\&}!{\#}* vector: Probing sentence embeddings for linguistic properties | related_work | Related Work | obj_superglue | SuperGLUE | benchmark_or_protocol | named_object | SuperGLUE | superglue | exact_alias | 572 | 581 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_superglue;alias=SuperGLUE |
| benchmark_or_protocol | ctxr_2e1b725a056f254d1a31 | ctx_b83f0fe222eebdccc4ad | 2020.nlp4convai-1.15 | P18-1198 | What you can cram into a single {\$}{\&}!{\#}* vector: Probing sentence embeddings for linguistic properties | related_work | Related Work | obj_glue | GLUE | benchmark_or_protocol | named_object | GLUE | glue | exact_alias | 543 | 547 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_glue;alias=GLUE |
| benchmark_or_protocol | ctxr_2e1b725a056f254d1a31 | ctx_b83f0fe222eebdccc4ad | 2020.nlp4convai-1.15 | P18-1198 | What you can cram into a single {\$}{\&}!{\#}* vector: Probing sentence embeddings for linguistic properties | related_work | Related Work | obj_superglue | SuperGLUE | benchmark_or_protocol | named_object | SuperGLUE | superglue | exact_alias | 572 | 581 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_superglue;alias=SuperGLUE |
| dataset_or_database | ctxr_caa50477f333d1e3c48b | ctx_1cf74ef13884c4116a34 | R13-1046 | J93-2004 | Building a Large Annotated Corpus of {E}nglish: The {P}enn {T}reebank | dataset | Data | obj_penn_treebank | Penn Treebank | dataset_or_database | named_object | Penn Treebank | penn treebank | exact_alias | 93 | 106 | 0.95 | sentence_text | context_cue_present | True | registry_seed:obj_penn_treebank;alias=Penn Treebank |
| dataset_or_database | ctxr_caa50477f333d1e3c48b | ctx_1cf74ef13884c4116a34 | R13-1046 | J93-2004 | Building a Large Annotated Corpus of {E}nglish: The {P}enn {T}reebank | dataset | Data | obj_penn_treebank | Penn Treebank | dataset_or_database | named_object | PTB | ptb | exact_alias | 108 | 111 | 0.95 | sentence_text | context_cue_present | True | registry_seed:obj_penn_treebank;alias=PTB |
| dataset_or_database | ctxr_d2f7e10dccf772790070 | ctx_3052c12f694776848067 | R13-1046 | W08-1301 | The {S}tanford Typed Dependencies Representation | dataset | Data | obj_penn_treebank | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | ptb | exact_alias | 36 | 39 | 0.5 | sentence_text | weak_context_cue_missing | False | registry_seed:obj_penn_treebank;alias=PTB |
| dataset_or_database | ctxr_c222d4c1bd43d71f629d | ctx_658af6609e37dc607c43 | Y18-1058 | J02-3001 | Automatic Labeling of Semantic Roles | introduction | Introduction | obj_propbank | PropBank | dataset_or_database | named_object | PropBank | propbank | exact_alias | 375 | 383 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_propbank;alias=PropBank |
| dataset_or_database | ctxr_c222d4c1bd43d71f629d | ctx_658af6609e37dc607c43 | Y18-1058 | J02-3001 | Automatic Labeling of Semantic Roles | introduction | Introduction | obj_framenet | FrameNet | dataset_or_database | named_object | FrameNet | framenet | exact_alias | 411 | 419 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_framenet;alias=FrameNet |
| method | ctxr_3e4722d1950da619a7dd | ctx_ca6cc2ce8812268acdb7 | R13-1044 | L12-1574 | {KPW}r: Towards a Free Corpus of {P}olish | unknown | Recognizing word pairs and triples | obj_crf | CRF | method | named_object | CRF | crf | exact_alias | 17 | 20 | 0.95 | sentence_text | standard | True | registry_seed:obj_crf;alias=CRF |
| method | ctxr_023a8eacb53c5fb15079 | ctx_fda17dcdd461f7773e54 | R13-1051 | N04-4028 | Confidence Estimation for Information Extraction | related_work | Related Work | obj_hmm | HMM | method | named_object | hidden Markov models | hidden markov models | exact_alias | 32 | 52 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_hmm;alias=hidden Markov models |
| method | ctxr_023a8eacb53c5fb15079 | ctx_fda17dcdd461f7773e54 | R13-1051 | N04-4028 | Confidence Estimation for Information Extraction | related_work | Related Work | obj_crf | CRF | method | named_object | Conditional Random Field | conditional random field | case_insensitive_alias | 442 | 466 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_crf;alias=conditional random field |
| method | ctxr_023a8eacb53c5fb15079 | ctx_fda17dcdd461f7773e54 | R13-1051 | N04-4028 | Confidence Estimation for Information Extraction | related_work | Related Work | obj_crf | CRF | method | named_object | CRF | crf | exact_alias | 468 | 471 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_crf;alias=CRF |
| method | ctxr_5d60b328d89597812f9a | ctx_868f78e15e5cbbdd14d5 | W05-0831 | J03-1002 | A Systematic Comparison of Various Statistical Alignment Models | unknown | Reordering in Training | obj_hmm | HMM | method | named_object | HMM | hmm | exact_alias | 152 | 155 | 0.95 | sentence_text | standard | True | registry_seed:obj_hmm;alias=HMM |
| metric | ctxr_d573e73d4a69363cdfc0 | ctx_2058502beaf095f8c9d9 | R13-1042 | P11-1118 | Disentangling Chat with Local Coherence Models | results | Results | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 215 | 223 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| metric | ctxr_fde2b4fe687323ff4bd3 | ctx_ce3b0066680b71c0ab36 | W05-0818 | W03-0301 | An Evaluation Exercise for Word Alignment | experiment | Experiments | obj_f1 | F1 | metric | generic_metric | F -measure | f measure | punctuation_normalized_alias | 58 | 68 | 0.7 | sentence_text | generic_metric | False | registry_seed:obj_f1;alias=F measure |
| metric | ctxr_794ff11af106441610a2 | ctx_7f225179a64758da5dba | W05-0821 | C04-1022 | Automatic Learning of Language Model Structure | model | Factored Language Models | obj_perplexity | perplexity | metric | generic_metric | perplexity | perplexity | exact_alias | 408 | 418 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_perplexity;alias=perplexity |
| metric | ctxr_794ff11af106441610a2 | ctx_7f225179a64758da5dba | W05-0821 | C04-1022 | Automatic Learning of Language Model Structure | model | Factored Language Models | obj_bleu | BLEU | metric | named_object | BLEU | bleu | exact_alias | 481 | 485 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_bleu;alias=BLEU |
| metric | ctxr_b4edfcd618c4edc4d4dc | ctx_baae2db29cd713e28052 | R13-1046 | W13-1101 | Does Size Matter? Text and Grammar Revision for Parsing Social Media Data | introduction | Introduction and Motivation | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 274 | 282 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| model | ctxr_1527f42ff080e1df1961 | ctx_32be8b860cb0185b7c19 | Y18-1058 | P15-1109 | End-to-end learning of semantic role labeling using recurrent neural networks | related_work | Related Work | obj_lstm | LSTM | model | named_object | LSTM | lstm | exact_alias | 100 | 104 | 0.95 | sentence_text | standard | True | registry_seed:obj_lstm;alias=LSTM |
| model | ctxr_378723e2689534552b44 | ctx_031529e47516f4dc37b8 | Y18-1058 | P16-1113 | Neural Semantic Role Labeling with Dependency Path Embeddings | related_work | Related Work | obj_lstm | LSTM | model | named_object | LSTM | lstm | exact_alias | 54 | 58 | 0.95 | sentence_text | standard | True | registry_seed:obj_lstm;alias=LSTM |
| model | ctxr_e29d4de098ff144543d9 | ctx_a3f4dc606ed46a0bdcdd | Y18-1058 | P17-1044 | Deep Semantic Role Labeling: What Works and What{'}s Next | related_work | Related Work | obj_lstm | LSTM | model | named_object | LSTM | lstm | exact_alias | 54 | 58 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_lstm;alias=LSTM |
| model | ctxr_86389b1dfa2cf6f4f642 | ctx_bda3e4db3dad62f4da02 | 2020.emnlp-main.380 | D18-1116 | Toward Fast and Accurate Neural Discourse Segmentation | introduction | Introduction | obj_lstm | LSTM | model | named_object | LSTMs | lstms | exact_alias | 16 | 21 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_lstm;alias=LSTMs |
| model | ctxr_5015c0ea1b26d296ffa6 | ctx_6add866df3a383ab1432 | 2020.emnlp-main.380 | N18-1202 | Deep Contextualized Word Representations | introduction | Introduction | obj_lstm | LSTM | model | named_object | LSTMs | lstms | exact_alias | 16 | 21 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_lstm;alias=LSTMs |
| software_or_tool | ctxr_4355448353bdd023508c | ctx_e33a1b32079c54fb1946 | W05-0820 | J03-1002 | A Systematic Comparison of Various Statistical Alignment Models | unknown | Work on new language pairs, new problems: | obj_giza | GIZA++ | software_or_tool | named_object | GIZA++ | giza++ | exact_alias | 128 | 134 | 0.95 | sentence_text | standard | True | registry_seed:obj_giza;alias=GIZA++ |
| software_or_tool | ctxr_e4bd8b3cb291ec3f4e15 | ctx_2a912ffa75455b48a752 | W05-0823 | P00-1056 | Improved Statistical Alignment Models | method | Preprocessing and Alignment | obj_giza | GIZA++ | software_or_tool | named_object | GIZA++ | giza++ | exact_alias | 147 | 153 | 0.95 | sentence_text | standard | True | registry_seed:obj_giza;alias=GIZA++ |
| software_or_tool | ctxr_059fae894b25c9864d24 | ctx_57cb88547b3a3b152a3c | W05-0825 | J03-1002 | A Systematic Comparison of Various Statistical Alignment Models | experiment | Experimental Results | obj_giza | GIZA++ | software_or_tool | named_object | GIZA++ | giza++ | exact_alias | 64 | 70 | 0.95 | sentence_text | standard | True | registry_seed:obj_giza;alias=GIZA++ |
| software_or_tool | ctxr_a7a32c62150dc08cd73f | ctx_5681d6a3d69945b1c761 | W05-0824 | P00-1056 | Improved Statistical Alignment Models | unknown | The core system | obj_giza | GIZA++ | software_or_tool | named_object | Giza | giza | case_insensitive_alias | 39 | 43 | 0.95 | sentence_text | standard | True | registry_seed:obj_giza;alias=GIZA |
| software_or_tool | ctxr_b05afaa70827ae54fae7 | ctx_4c554b1512241b16aba5 | 2009.mtsummit-posters.17 | W08-0509 | Parallel Implementations of Word Alignment Tool | system_description | Baseline system | obj_giza | GIZA++ | software_or_tool | named_object | GIZA++ | giza++ | exact_alias | 40 | 46 | 0.95 | sentence_text | standard | True | registry_seed:obj_giza;alias=GIZA++ |

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

## Top Ambiguous Short Alias Matches
| object_id | canonical_name | surface_form | match_policy | mentions |
| --- | --- | --- | --- | --- |
| obj_penn_treebank | Penn Treebank | PTB | weak_context_cue_missing | 33 |
| obj_penn_treebank | Penn Treebank | PTB | weak_context_cue_missing;neighbor_context_match | 27 |

## PTB Match Examples
| context_id | source_context_id | citing_paper_id | resolved_cited_acl_id | resolved_cited_title | normalized_section | raw_section_name | object_id | canonical_name | object_type | object_category | surface_form | normalized_surface | match_type | char_start | char_end | confidence | matched_in | match_policy | allow_in_object_graph | provenance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_caa50477f333d1e3c48b | ctx_1cf74ef13884c4116a34 | R13-1046 | J93-2004 | Building a Large Annotated Corpus of {E}nglish: The {P}enn {T}reebank | dataset | Data | obj_penn_treebank | Penn Treebank | dataset_or_database | named_object | PTB | ptb | exact_alias | 108 | 111 | 0.95 | sentence_text | context_cue_present | True | registry_seed:obj_penn_treebank;alias=PTB |
| ctxr_d2f7e10dccf772790070 | ctx_3052c12f694776848067 | R13-1046 | W08-1301 | The {S}tanford Typed Dependencies Representation | dataset | Data | obj_penn_treebank | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | ptb | exact_alias | 36 | 39 | 0.5 | sentence_text | weak_context_cue_missing | False | registry_seed:obj_penn_treebank;alias=PTB |
| ctxr_7eebce6c90b1ab8d2d3d | ctx_8998a1ed39a479b81f71 | R13-1008 | J93-2004 | Building a Large Annotated Corpus of {E}nglish: The {P}enn {T}reebank | dataset | Data Sets | obj_penn_treebank | Penn Treebank | dataset_or_database | named_object | PTB | ptb | exact_alias | 51 | 54 | 0.95 | sentence_text | context_cue_present | True | registry_seed:obj_penn_treebank;alias=PTB |
| ctxr_e90af008e39f29815e47 | ctx_f62f61e3dee349a88de7 | R13-1008 | A00-1031 | {T}n{T} {--} A Statistical Part-of-Speech Tagger | unknown | Parsers | obj_penn_treebank | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | ptb | exact_alias | 61 | 64 | 0.5 | sentence_text | weak_context_cue_missing | False | registry_seed:obj_penn_treebank;alias=PTB |
| ctxr_fb56106a126513c8b39c | ctx_211fedf8e97b27632796 | R13-1011 | N03-1033 | Feature-Rich Part-of-Speech Tagging with a Cyclic Dependency Network | unknown | Part-of-speech Tagging | obj_penn_treebank | Penn Treebank | dataset_or_database | named_object | PTB | ptb | exact_alias | 119 | 122 | 0.95 | sentence_text | context_cue_present | True | registry_seed:obj_penn_treebank;alias=PTB |
| ctxr_cb37bb4fb9b009e8f4e2 | ctx_4e97d591466f79d5595b | R13-1011 | D11-1141 | Named Entity Recognition in Tweets: An Experimental Study | unknown | Part-of-speech Tagging | obj_penn_treebank | Penn Treebank | dataset_or_database | named_object | PTB | ptb | exact_alias | 143 | 146 | 0.95 | sentence_text | context_cue_present | True | registry_seed:obj_penn_treebank;alias=PTB |
| ctxr_a5bc90bafa5096481006 | ctx_a2389b9f250486fc5b15 | R13-1011 | J93-2004 | Building a Large Annotated Corpus of {E}nglish: The {P}enn {T}reebank | unknown | Part-of-speech Tagging | obj_penn_treebank | Penn Treebank | dataset_or_database | named_object | PTB | ptb | exact_alias | 143 | 146 | 0.95 | sentence_text | context_cue_present | True | registry_seed:obj_penn_treebank;alias=PTB |
| ctxr_065657af5543ed78d301 | ctx_54d8e3a522dbb95e29ae | R13-1011 | D11-1141 | Named Entity Recognition in Tweets: An Experimental Study | unknown | Part-of-speech Tagging | obj_penn_treebank | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | ptb | exact_alias | 273 | 276 | 0.5 | sentence_text | weak_context_cue_missing | False | registry_seed:obj_penn_treebank;alias=PTB |
| ctxr_e5b701b6d20ba1498357 | ctx_58b37fe4234122671169 | R13-1011 | P11-2008 | Part-of-Speech Tagging for {T}witter: Annotation, Features, and Experiments | unknown | Part-of-speech Tagging | obj_penn_treebank | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | ptb | exact_alias | 273 | 276 | 0.5 | sentence_text | weak_context_cue_missing | False | registry_seed:obj_penn_treebank;alias=PTB |
| ctxr_b25c05e9a146e65cf7f4 | ctx_f5b38c07d06824ff48e2 | R13-1026 | D11-1141 | Named Entity Recognition in Tweets: An Experimental Study | dataset | Labeled Tweet Corpora | obj_penn_treebank | Penn Treebank | dataset_or_database | named_object | PTB | ptb | exact_alias | 367 | 370 | 0.85 | context_window_neighbor | context_cue_present;neighbor_context_match | True | registry_seed:obj_penn_treebank;alias=PTB |
| ctxr_9da88ff6c9701d288368 | ctx_0ec75856acac472eeb71 | R13-1026 | P11-2008 | Part-of-Speech Tagging for {T}witter: Annotation, Features, and Experiments | dataset | Labeled Tweet Corpora | obj_penn_treebank | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | ptb | exact_alias | 158 | 161 | 0.5 | sentence_text | weak_context_cue_missing | False | registry_seed:obj_penn_treebank;alias=PTB |
| ctxr_e2ce85d756baa9a37469 | ctx_8dd81e0554f6a4b25988 | R13-1034 | C12-1179 | {ISO}-{T}ime{ML} Event Extraction in {P}ersian Text | introduction | Introduction | obj_penn_treebank | Penn Treebank | dataset_or_database | named_object | PTB | ptb | exact_alias | 70 | 73 | 0.95 | sentence_text | context_cue_present | True | registry_seed:obj_penn_treebank;alias=PTB |
| ctxr_cd65f52db26c481dcc6b | ctx_32796ad2ab4ffbf6584b | R13-1034 | C10-1011 | Top Accuracy and Fast Dependency Parsing is not a Contradiction | experiment | Experimental Results | obj_penn_treebank | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | ptb | exact_alias | 250 | 253 | 0.4 | context_window_neighbor | weak_context_cue_missing;neighbor_context_match | False | registry_seed:obj_penn_treebank;alias=PTB |
| ctxr_6afbbcf00698a5f24d61 | ctx_8ac020175c1229527e3b | D19-5728 | I05-2038 | Syntax Annotation for the {GENIA} Corpus | unknown | What did not work | obj_penn_treebank | Penn Treebank | dataset_or_database | ambiguous_short_alias | PTB | ptb | exact_alias | 60 | 63 | 0.5 | sentence_text | weak_context_cue_missing | False | registry_seed:obj_penn_treebank;alias=PTB |
| ctxr_2b097aea007a1bd9f688 | ctx_76e466e66355cf025d26 | W11-2832 | W05-1510 | Probabilistic Models for Disambiguation of an {HPSG}-Based Chart Generator | introduction | Introduction and Overview | obj_penn_treebank | Penn Treebank | dataset_or_database | named_object | PTB | ptb | exact_alias | 248 | 251 | 0.95 | sentence_text | context_cue_present | True | registry_seed:obj_penn_treebank;alias=PTB |
| ctxr_cf2236f2e0d3e5a90e55 | ctx_76e466e66355cf025d26 | W11-2832 | P06-1130 | Robust {PCFG}-Based Generation Using Automatically Acquired {LFG} Approximations | introduction | Introduction and Overview | obj_penn_treebank | Penn Treebank | dataset_or_database | named_object | PTB | ptb | exact_alias | 248 | 251 | 0.95 | sentence_text | context_cue_present | True | registry_seed:obj_penn_treebank;alias=PTB |
| ctxr_a8649a69846823fc94b3 | ctx_76e466e66355cf025d26 | W11-2832 | D09-1043 | Perceptron Reranking for {CCG} Realization | introduction | Introduction and Overview | obj_penn_treebank | Penn Treebank | dataset_or_database | named_object | PTB | ptb | exact_alias | 248 | 251 | 0.95 | sentence_text | context_cue_present | True | registry_seed:obj_penn_treebank;alias=PTB |
| ctxr_1f2b8616463c9f520bad | ctx_fdacf02a3d128f46640f | W11-2832 | W05-1510 | Probabilistic Models for Disambiguation of an {HPSG}-Based Chart Generator | introduction | Introduction and Overview | obj_penn_treebank | Penn Treebank | dataset_or_database | named_object | PTB | ptb | exact_alias | 248 | 251 | 0.95 | sentence_text | context_cue_present | True | registry_seed:obj_penn_treebank;alias=PTB |
| ctxr_378aa5922b6ffa1f3d10 | ctx_fdacf02a3d128f46640f | W11-2832 | P06-1130 | Robust {PCFG}-Based Generation Using Automatically Acquired {LFG} Approximations | introduction | Introduction and Overview | obj_penn_treebank | Penn Treebank | dataset_or_database | named_object | PTB | ptb | exact_alias | 248 | 251 | 0.95 | sentence_text | context_cue_present | True | registry_seed:obj_penn_treebank;alias=PTB |
| ctxr_9b62a06c4a1d1795320e | ctx_fdacf02a3d128f46640f | W11-2832 | D09-1043 | Perceptron Reranking for {CCG} Realization | introduction | Introduction and Overview | obj_penn_treebank | Penn Treebank | dataset_or_database | named_object | PTB | ptb | exact_alias | 248 | 251 | 0.95 | sentence_text | context_cue_present | True | registry_seed:obj_penn_treebank;alias=PTB |

## Accuracy / F1 / Perplexity Examples
| context_id | source_context_id | citing_paper_id | resolved_cited_acl_id | resolved_cited_title | normalized_section | raw_section_name | object_id | canonical_name | object_type | object_category | surface_form | normalized_surface | match_type | char_start | char_end | confidence | matched_in | match_policy | allow_in_object_graph | provenance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_d573e73d4a69363cdfc0 | ctx_2058502beaf095f8c9d9 | R13-1042 | P11-1118 | Disentangling Chat with Local Coherence Models | results | Results | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 215 | 223 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_fde2b4fe687323ff4bd3 | ctx_ce3b0066680b71c0ab36 | W05-0818 | W03-0301 | An Evaluation Exercise for Word Alignment | experiment | Experiments | obj_f1 | F1 | metric | generic_metric | F -measure | f measure | punctuation_normalized_alias | 58 | 68 | 0.7 | sentence_text | generic_metric | False | registry_seed:obj_f1;alias=F measure |
| ctxr_794ff11af106441610a2 | ctx_7f225179a64758da5dba | W05-0821 | C04-1022 | Automatic Learning of Language Model Structure | model | Factored Language Models | obj_perplexity | perplexity | metric | generic_metric | perplexity | perplexity | exact_alias | 408 | 418 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_perplexity;alias=perplexity |
| ctxr_b4edfcd618c4edc4d4dc | ctx_baae2db29cd713e28052 | R13-1046 | W13-1101 | Does Size Matter? Text and Grammar Revision for Parsing Social Media Data | introduction | Introduction and Motivation | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 274 | 282 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_f7c720ac514891b21f33 | ctx_9467c404bd35ecd142b4 | R13-1046 | E06-1011 | Online Learning of Approximate Dependency Parsing Algorithms | unknown | Parser | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 105 | 113 | 0.7 | sentence_text | generic_metric | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_26559d1672acccfd09ea | ctx_9c84cb4ef671e246a5be | R13-1046 | P05-1012 | Online Large-Margin Training of Dependency Parsers | unknown | Parser | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 105 | 113 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_c223321394c5bbc2bcec | ctx_c68731c0340fcd07d57b | R13-1046 | A00-1031 | {T}n{T} {--} A Statistical Part-of-Speech Tagger | unknown | The effect of POS tagging | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 30 | 38 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_c223321394c5bbc2bcec | ctx_c68731c0340fcd07d57b | R13-1046 | A00-1031 | {T}n{T} {--} A Statistical Part-of-Speech Tagger | unknown | The effect of POS tagging | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 217 | 225 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_72089786b736eb3c1d50 | ctx_2868157b89a3f8bb0973 | R13-1046 | W13-1101 | Does Size Matter? Text and Grammar Revision for Parsing Social Media Data | unknown | The effect of POS tagging | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 151 | 159 | 0.7 | sentence_text | generic_metric | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_1348abfe0d9ee416094f | ctx_75f51b85f7f3b4850622 | 2009.mtsummit-posters.23 | 2007.mtsummit-papers.64 | {J}apanese-{H}ungarian dictionary generation using ontology resources | dataset | Resource issues | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 356 | 364 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_9af9bd56af035c2cee84 | ctx_4ef870281b839f0e6cad | R13-1048 | P06-1041 | Hybrid Parsing: Using Probabilistic Models as Predictors for a Symbolic Parser | unknown | MaltParser as a Predictor for jwcdg | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 94 | 102 | 0.7 | sentence_text | generic_metric | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_9ecca4bac0344e435a50 | ctx_08464d970bac736b3c5a | R13-1048 | W03-3017 | An Efficient Algorithm for Projective Dependency Parsing | unknown | MaltParser as a Predictor for jwcdg | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 338 | 346 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_9ecca4bac0344e435a50 | ctx_08464d970bac736b3c5a | R13-1048 | W03-3017 | An Efficient Algorithm for Projective Dependency Parsing | unknown | MaltParser as a Predictor for jwcdg | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 392 | 400 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_12dda98b18b7e159cf6c | ctx_f9ad96418feda15bffe7 | R13-1048 | W09-3816 | Co-Parsing with Competitive Models | unknown | MaltParser as a Predictor for jwcdg | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 97 | 105 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_12dda98b18b7e159cf6c | ctx_f9ad96418feda15bffe7 | R13-1048 | W09-3816 | Co-Parsing with Competitive Models | unknown | MaltParser as a Predictor for jwcdg | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 151 | 159 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_6f4fbb5a1e4f3b2f971a | ctx_b4f5a1a27ec820df30f4 | R13-1048 | W06-2932 | Multilingual Dependency Analysis with a Two-Stage Discriminative Parser | unknown | MaltParser as a Predictor for jwcdg | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 97 | 105 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_6f4fbb5a1e4f3b2f971a | ctx_b4f5a1a27ec820df30f4 | R13-1048 | W06-2932 | Multilingual Dependency Analysis with a Two-Stage Discriminative Parser | unknown | MaltParser as a Predictor for jwcdg | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 151 | 159 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_448d50f47d83c101d92f | ctx_3e66b0fb7777637aa22e | R13-1048 | A00-1031 | {T}n{T} {--} A Statistical Part-of-Speech Tagger | unknown | MaltParser as a Predictor for jwcdg | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 157 | 165 | 0.7 | sentence_text | generic_metric | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_cb27bb574c756f008de2 | ctx_da4ba23393fcc1c80f81 | Y18-1058 | J02-3001 | Automatic Labeling of Semantic Roles | related_work | Related Work | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 134 | 142 | 0.7 | sentence_text | generic_metric | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_b3f99b73329db6bbf332 | ctx_b1e4dd030768fc6c52f7 | Y18-1058 | P03-1002 | Using Predicate-Argument Structures for Information Extraction | related_work | Related Work | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 134 | 142 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |

## Transformer Uppercase / Lowercase Examples
| context_id | source_context_id | citing_paper_id | resolved_cited_acl_id | resolved_cited_title | normalized_section | raw_section_name | object_id | canonical_name | object_type | object_category | surface_form | normalized_surface | match_type | char_start | char_end | confidence | matched_in | match_policy | allow_in_object_graph | provenance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_aa1b7e3f43fffb4f92b0 | ctx_3bdef62d8f1f790095de | 2020.emnlp-main.380 | P19-1499 | {HIBERT}: Document Level Pre-training of Hierarchical Bidirectional Transformers for Document Summarization | unknown | Hierarchical BERT | obj_transformer | Transformer | model | generic_architecture | transformer | transformer | case_insensitive_alias | 156 | 167 | 0.55 | context_window_neighbor | lowercase_generic_architecture;neighbor_context_match | False | registry_seed:obj_transformer;alias=Transformer |
| ctxr_ab7617f2f9592a20ff6a | ctx_8cd9f7d7ef72314a504d | 2021.ranlp-1.12 | N19-1408 | Rethinking Complex Neural Network Architectures for Document Classification | introduction | Introduction | obj_transformer | Transformer | model | named_object | Transformers | transformers | exact_alias | 360 | 372 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_transformer;alias=Transformers |
| ctxr_7be2d2360c50b43f3fcd | ctx_8cd9f7d7ef72314a504d | 2021.ranlp-1.12 | S19-2123 | Nikolov-Radivchev at {S}em{E}val-2019 Task 6: Offensive Tweet Classification with {BERT} and Ensembles | introduction | Introduction | obj_transformer | Transformer | model | named_object | Transformers | transformers | exact_alias | 360 | 372 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_transformer;alias=Transformers |
| ctxr_082cd21660027a05e63f | ctx_2c78251489008a76e2b1 | 2021.ranlp-1.12 | N19-1408 | Rethinking Complex Neural Network Architectures for Document Classification | introduction | Introduction | obj_transformer | Transformer | model | named_object | Transformers | transformers | exact_alias | 360 | 372 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_transformer;alias=Transformers |
| ctxr_89e33f91e0ca4aa47fe6 | ctx_2c78251489008a76e2b1 | 2021.ranlp-1.12 | S19-2123 | Nikolov-Radivchev at {S}em{E}val-2019 Task 6: Offensive Tweet Classification with {BERT} and Ensembles | introduction | Introduction | obj_transformer | Transformer | model | named_object | Transformers | transformers | exact_alias | 360 | 372 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_transformer;alias=Transformers |
| ctxr_8a018d33416b7ece9ac6 | ctx_e7adf803f3b0416013ce | 2021.ranlp-1.12 | N19-1423 | {BERT}: Pre-training of Deep Bidirectional Transformers for Language Understanding | introduction | Introduction | obj_transformer | Transformer | model | named_object | Transformers | transformers | exact_alias | 151 | 163 | 0.95 | sentence_text | standard | True | registry_seed:obj_transformer;alias=Transformers |
| ctxr_11674fda9622e62cf411 | ctx_0a475cf6f07be6508002 | 2021.ranlp-1.12 | L12-1519 | {JRC} Eurovoc Indexer {JEX} - A freely available multi-label categorisation tool | introduction | Introduction | obj_transformer | Transformer | model | named_object | Transformers | transformers | exact_alias | 151 | 163 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_transformer;alias=Transformers |
| ctxr_29fb8dc8cb651ec8b717 | ctx_5e4f13d97190a50a966e | 2020.nlp4convai-1.14 | P18-1205 | Personalizing Dialogue Agents: {I} have a dog, do you have pets too? | unknown | Empirical Validation | obj_transformer | Transformer | model | named_object | Transformer | transformer | exact_alias | 51 | 62 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_transformer;alias=Transformer |
| ctxr_d8985cbc91aaf9f28e3f | ctx_c51fbd7cf7e26109a828 | 2020.nlp4convai-1.15 | D17-2014 | {P}arl{AI}: A Dialog Research Software Platform | dataset | Models and Data | obj_transformer | Transformer | model | named_object | Transformers | transformers | exact_alias | 185 | 197 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_transformer;alias=Transformers |
| ctxr_bbb1ce2f4d76174a40a8 | ctx_cb95ffee767bbafc26c5 | 2021.nlp4convai-1.2 | N19-1423 | {BERT}: Pre-training of Deep Bidirectional Transformers for Language Understanding | method | Method 2.1 Natural Language Inference | obj_transformer | Transformer | model | generic_architecture | transformer | transformer | case_insensitive_alias | 12 | 23 | 0.65 | sentence_text | lowercase_generic_architecture | False | registry_seed:obj_transformer;alias=Transformer |
| ctxr_f046d453884a870316f0 | ctx_871c458051c8446baaf2 | 2021.nlp4convai-1.2 | N18-1101 | A Broad-Coverage Challenge Corpus for Sentence Understanding through Inference | dataset | General NLI corpus for pre-training | obj_transformer | Transformer | model | named_object | transformer model | transformer model | case_insensitive_alias | 33 | 50 | 0.95 | sentence_text | standard | True | registry_seed:obj_transformer;alias=Transformer model |
| ctxr_5aac81c6d759c1e1a986 | ctx_84595b317e169ffc05d3 | 2021.nlp4convai-1.2 | W18-5446 | {GLUE}: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding | dataset | General NLI corpus for pre-training | obj_transformer | Transformer | model | named_object | transformer model | transformer model | case_insensitive_alias | 33 | 50 | 0.95 | sentence_text | standard | True | registry_seed:obj_transformer;alias=Transformer model |
| ctxr_686b28273ac8dd11a1b3 | ctx_c41daf6c5fd829c76a3c | 2021.nlp4convai-1.2 | 2020.emnlp-demos.6 | Transformers: State-of-the-Art Natural Language Processing | unknown | Training | obj_transformer | Transformer | model | generic_architecture | transformer | transformer | case_insensitive_alias | 11 | 22 | 0.65 | sentence_text | lowercase_generic_architecture | False | registry_seed:obj_transformer;alias=Transformer |
| ctxr_65fdc1db1863225e9bf2 | ctx_4104bb7826f2a45118f5 | 2021.nlp4convai-1.4 | 2020.findings-emnlp.303 | Composed Variational Natural Language Generation for Few-shot Intents | related_work | Related work | obj_transformer | Transformer | model | generic_architecture | transformer | transformer | case_insensitive_alias | 28 | 39 | 0.65 | sentence_text | lowercase_generic_architecture | False | registry_seed:obj_transformer;alias=Transformer |
| ctxr_0f075d7177b37dcc6ea4 | ctx_b7c30588a8e85f0d4b2b | 2021.nlp4convai-1.4 | W19-2306 | Paraphrase Generation for Semi-Supervised Learning in {NLU} | related_work | Related work | obj_transformer | Transformer | model | generic_architecture | transformer | transformer | case_insensitive_alias | 64 | 75 | 0.65 | sentence_text | lowercase_generic_architecture | False | registry_seed:obj_transformer;alias=Transformer |
| ctxr_97857c8cfe503e3e220c | ctx_a84e8a8247982b797193 | 2021.nlp4convai-1.4 | 2020.coling-industry.2 | Data-Efficient Paraphrase Generation to Bootstrap Intent Classification and Slot Labeling for New Features in Task-Oriented Dialog Systems | related_work | Related work | obj_transformer | Transformer | model | generic_architecture | transformer | transformer | case_insensitive_alias | 79 | 90 | 0.65 | sentence_text | lowercase_generic_architecture | False | registry_seed:obj_transformer;alias=Transformer |
| ctxr_74fb2d78af593db2157e | ctx_ec4ae67ece178ccda336 | 2021.nlp4convai-1.5 | P16-1002 | Data Recombination for Neural Semantic Parsing | model | Base Model | obj_transformer | Transformer | model | named_object | transformer architecture | transformer architecture | case_insensitive_alias | 99 | 123 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_transformer;alias=Transformer architecture |
| ctxr_1a5cc7b3721802ef8458 | ctx_ec4ae67ece178ccda336 | 2021.nlp4convai-1.5 | P16-1004 | Language to Logical Form with Neural Attention | model | Base Model | obj_transformer | Transformer | model | named_object | transformer architecture | transformer architecture | case_insensitive_alias | 99 | 123 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_transformer;alias=Transformer architecture |
| ctxr_78d18bccd45aa0b5bf41 | ctx_3966fbbe289709a4305f | 2021.nlp4convai-1.5 | P16-1002 | Data Recombination for Neural Semantic Parsing | model | Base Model | obj_transformer | Transformer | model | named_object | transformer architecture | transformer architecture | case_insensitive_alias | 99 | 123 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_transformer;alias=Transformer architecture |
| ctxr_95ed71dd70a95cc93060 | ctx_3966fbbe289709a4305f | 2021.nlp4convai-1.5 | P16-1004 | Language to Logical Form with Neural Attention | model | Base Model | obj_transformer | Transformer | model | named_object | transformer architecture | transformer architecture | case_insensitive_alias | 99 | 123 | 0.85 | context_window_neighbor | standard;neighbor_context_match | True | registry_seed:obj_transformer;alias=Transformer architecture |

## Cited Title Profile Examples
| context_id | source_context_id | citing_paper_id | resolved_cited_acl_id | resolved_cited_title | normalized_section | raw_section_name | object_id | canonical_name | object_type | object_category | surface_form | normalized_surface | match_type | char_start | char_end | confidence | matched_in | match_policy | allow_in_object_graph | provenance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_6ec7b60115b4d5e6dcf1 | ctx_8ee4e60043981a38782e | R13-1046 | N10-1120 | Dependency Tree-based Sentiment Classification using {CRF}s with Hidden Variables | introduction | Introduction and Motivation | obj_crf | CRF | method | named_object | CRF | crf | exact_alias | 54 | 57 | 0.95 | resolved_cited_title | standard | True | registry_seed:obj_crf;alias=CRF |
| ctxr_5cf962d606f5bb683922 | ctx_ef689b946fb8a015c84f | W05-0828 | L04-1489 | Interpreting {BLEU}/{NIST} Scores: How Much Improvement do We Need to Have a Better System? | unknown | Statistical Selection | obj_bleu | BLEU | metric | named_object | BLEU | bleu | exact_alias | 14 | 18 | 0.95 | resolved_cited_title | standard | True | registry_seed:obj_bleu;alias=BLEU |
| ctxr_f2fc5d3298a427695aa8 | ctx_6414e0d8fa5fc825be29 | W05-0835 | C96-2141 | {HMM}-Based Word Alignment in Statistical Translation | introduction | Introduction | obj_hmm | HMM | method | named_object | HMM | hmm | exact_alias | 1 | 4 | 0.95 | resolved_cited_title | standard | True | registry_seed:obj_hmm;alias=HMM |
| ctxr_52bb41aed58f89be7736 | ctx_5a97bb6434d27f5918d4 | W05-0835 | C96-2141 | {HMM}-Based Word Alignment in Statistical Translation | introduction | Introduction | obj_hmm | HMM | method | named_object | HMM | hmm | exact_alias | 1 | 4 | 0.95 | resolved_cited_title | standard | True | registry_seed:obj_hmm;alias=HMM |
| ctxr_fa827b5872437cd3481b | ctx_60363e917b2f927cbc6f | W05-0835 | C96-2141 | {HMM}-Based Word Alignment in Statistical Translation | introduction | Introduction | obj_hmm | HMM | method | named_object | HMM | hmm | exact_alias | 1 | 4 | 0.95 | resolved_cited_title | standard | True | registry_seed:obj_hmm;alias=HMM |
| ctxr_348ed735539164c215ec | ctx_330dcf7dff7e71dc926f | W05-0835 | C96-2141 | {HMM}-Based Word Alignment in Statistical Translation | introduction | Introduction | obj_hmm | HMM | method | named_object | HMM | hmm | exact_alias | 1 | 4 | 0.95 | resolved_cited_title | standard | True | registry_seed:obj_hmm;alias=HMM |
| ctxr_c0ecda4d16dd1fa0c113 | ctx_29315694bbce4b7e0b4e | 2020.emnlp-main.380 | D14-1162 | {G}lo{V}e: Global Vectors for Word Representation | introduction | Introduction | obj_glove | GloVe | model | named_object | Global Vectors for Word Representation | global vectors for word representation | exact_alias | 11 | 49 | 0.95 | resolved_cited_title | standard | True | registry_seed:obj_glove;alias=Global Vectors for Word Representation |
| ctxr_aa1b7e3f43fffb4f92b0 | ctx_3bdef62d8f1f790095de | 2020.emnlp-main.380 | P19-1499 | {HIBERT}: Document Level Pre-training of Hierarchical Bidirectional Transformers for Document Summarization | unknown | Hierarchical BERT | obj_transformer | Transformer | model | named_object | Transformers | transformers | exact_alias | 68 | 80 | 0.95 | resolved_cited_title | standard | True | registry_seed:obj_transformer;alias=Transformers |
| ctxr_4ece378a815889ac5290 | ctx_b184efd8391ef2e33b3d | 2020.emnlp-main.380 | P19-1499 | {HIBERT}: Document Level Pre-training of Hierarchical Bidirectional Transformers for Document Summarization | unknown | Hierarchical BERT | obj_transformer | Transformer | model | named_object | Transformers | transformers | exact_alias | 68 | 80 | 0.95 | resolved_cited_title | standard | True | registry_seed:obj_transformer;alias=Transformers |
| ctxr_74d9fd93d7822354fb0f | ctx_e9e132f9224a9dab7d52 | 2020.emnlp-main.380 | P19-1499 | {HIBERT}: Document Level Pre-training of Hierarchical Bidirectional Transformers for Document Summarization | results | Results | obj_transformer | Transformer | model | named_object | Transformers | transformers | exact_alias | 68 | 80 | 0.95 | resolved_cited_title | standard | True | registry_seed:obj_transformer;alias=Transformers |
| ctxr_135f1a3a6cc1d78491d8 | ctx_d7e25a73c7aea82de3b1 | 2020.emnlp-main.380 | P19-1499 | {HIBERT}: Document Level Pre-training of Hierarchical Bidirectional Transformers for Document Summarization | conclusion | Conclusion | obj_transformer | Transformer | model | named_object | Transformers | transformers | exact_alias | 68 | 80 | 0.95 | resolved_cited_title | standard | True | registry_seed:obj_transformer;alias=Transformers |
| ctxr_c7102908c01762631958 | ctx_5da2fc6a58942d8f4475 | 2020.emnlp-main.380 | P19-1499 | {HIBERT}: Document Level Pre-training of Hierarchical Bidirectional Transformers for Document Summarization | conclusion | Conclusion | obj_transformer | Transformer | model | named_object | Transformers | transformers | exact_alias | 68 | 80 | 0.95 | resolved_cited_title | standard | True | registry_seed:obj_transformer;alias=Transformers |
| ctxr_30ddd765062e3abcb42a | ctx_db8d0553710501958f1e | 2020.emnlp-main.380 | 2020.emnlp-main.405 | Semantic Label Smoothing for Sequence to Sequence Problems | conclusion | Conclusion | obj_seq2seq | seq2seq | model | named_object | Sequence to Sequence | sequence to sequence | case_insensitive_alias | 29 | 49 | 0.95 | resolved_cited_title | standard | True | registry_seed:obj_seq2seq;alias=sequence to sequence |
| ctxr_a66cd052e5042059ea1b | ctx_b100d59132cbd267913b | 2020.emnlp-main.380 | 2020.emnlp-main.405 | Semantic Label Smoothing for Sequence to Sequence Problems | conclusion | Conclusion | obj_seq2seq | seq2seq | model | named_object | Sequence to Sequence | sequence to sequence | case_insensitive_alias | 29 | 49 | 0.95 | resolved_cited_title | standard | True | registry_seed:obj_seq2seq;alias=sequence to sequence |
| ctxr_92a39f9773361a0b10a6 | ctx_d0e150d930b1702a75bb | 2020.emnlp-main.380 | 2020.emnlp-main.405 | Semantic Label Smoothing for Sequence to Sequence Problems | conclusion | Conclusion | obj_seq2seq | seq2seq | model | named_object | Sequence to Sequence | sequence to sequence | case_insensitive_alias | 29 | 49 | 0.95 | resolved_cited_title | standard | True | registry_seed:obj_seq2seq;alias=sequence to sequence |
| ctxr_013ff32b6a1daff30375 | ctx_c956c98986bcd3569d1a | 2020.emnlp-main.380 | 2020.emnlp-main.405 | Semantic Label Smoothing for Sequence to Sequence Problems | conclusion | Conclusion | obj_seq2seq | seq2seq | model | named_object | Sequence to Sequence | sequence to sequence | case_insensitive_alias | 29 | 49 | 0.95 | resolved_cited_title | standard | True | registry_seed:obj_seq2seq;alias=sequence to sequence |
| ctxr_7be2d2360c50b43f3fcd | ctx_8cd9f7d7ef72314a504d | 2021.ranlp-1.12 | S19-2123 | Nikolov-Radivchev at {S}em{E}val-2019 Task 6: Offensive Tweet Classification with {BERT} and Ensembles | introduction | Introduction | obj_bert | BERT | model | named_object | BERT | bert | exact_alias | 83 | 87 | 0.95 | resolved_cited_title | standard | True | registry_seed:obj_bert;alias=BERT |
| ctxr_89e33f91e0ca4aa47fe6 | ctx_2c78251489008a76e2b1 | 2021.ranlp-1.12 | S19-2123 | Nikolov-Radivchev at {S}em{E}val-2019 Task 6: Offensive Tweet Classification with {BERT} and Ensembles | introduction | Introduction | obj_bert | BERT | model | named_object | BERT | bert | exact_alias | 83 | 87 | 0.95 | resolved_cited_title | standard | True | registry_seed:obj_bert;alias=BERT |
| ctxr_8a018d33416b7ece9ac6 | ctx_e7adf803f3b0416013ce | 2021.ranlp-1.12 | N19-1423 | {BERT}: Pre-training of Deep Bidirectional Transformers for Language Understanding | introduction | Introduction | obj_bert | BERT | model | named_object | BERT | bert | exact_alias | 1 | 5 | 0.95 | resolved_cited_title | standard | True | registry_seed:obj_bert;alias=BERT |
| ctxr_8a018d33416b7ece9ac6 | ctx_e7adf803f3b0416013ce | 2021.ranlp-1.12 | N19-1423 | {BERT}: Pre-training of Deep Bidirectional Transformers for Language Understanding | introduction | Introduction | obj_transformer | Transformer | model | named_object | Transformers | transformers | exact_alias | 43 | 55 | 0.95 | resolved_cited_title | standard | True | registry_seed:obj_transformer;alias=Transformers |

## Potential False Positives: Short Aliases
| context_id | source_context_id | citing_paper_id | resolved_cited_acl_id | resolved_cited_title | normalized_section | raw_section_name | object_id | canonical_name | object_type | object_category | surface_form | normalized_surface | match_type | char_start | char_end | confidence | matched_in | match_policy | allow_in_object_graph | provenance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_e95bf185b7763672a3fb | ctx_f25016042ecb1f4a27bc | 2021.ranlp-1.12 | L12-1519 | {JRC} Eurovoc Indexer {JEX} - A freely available multi-label categorisation tool | results | Results | obj_f1 | F1 | metric | generic_metric | F1 | f1 | exact_alias | 303 | 305 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_f1;alias=F1 |
| ctxr_0d792967967b7e61ce96 | ctx_be7d56079c57867d8945 | 2020.nlp4convai-1.12 | W19-4302 | To Tune or Not to Tune? Adapting Pretrained Representations to Diverse Tasks | model | Model Variants | obj_f1 | F1 | metric | generic_metric | F1 | f1 | exact_alias | 76 | 78 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_f1;alias=F1 |
| ctxr_0d792967967b7e61ce96 | ctx_be7d56079c57867d8945 | 2020.nlp4convai-1.12 | W19-4302 | To Tune or Not to Tune? Adapting Pretrained Representations to Diverse Tasks | model | Model Variants | obj_f1 | F1 | metric | generic_metric | F1 | f1 | exact_alias | 107 | 109 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_f1;alias=F1 |
| ctxr_acb5296965477dcd7fc1 | ctx_c2d09fdaf080118f5a47 | W09-1304 | W08-0607 | Recognizing Speculative Language in Biomedical Research Articles: A Linguistically Motivated Perspective | related_work | Related work | obj_f1 | F1 | metric | generic_metric | F1 | f1 | exact_alias | 37 | 39 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_f1;alias=F1 |
| ctxr_bf3a49c02b8d1648eeed | ctx_7345dcdfebfed6d9f7ff | 2020.lrec-1.337 | K18-2017 | {NLP}-Cube: End-to-End Raw Text Processing With Neural Networks | dataset | Linguistic Annotation | obj_f1 | F1 | metric | generic_metric | F1 | f1 | exact_alias | 615 | 617 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_f1;alias=F1 |
| ctxr_a301ae3146c0df1bd958 | ctx_aed4cd20d032b7acf653 | R13-1011 | D11-1141 | Named Entity Recognition in Tweets: An Experimental Study | related_work | Related Work | obj_f1 | F1 | metric | generic_metric | F1 | f1 | exact_alias | 383 | 385 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_f1;alias=F1 |
| ctxr_5996b8e55aa47f88c8bc | ctx_cb7547dca250c54f4aee | R13-1011 | P12-1055 | Joint Inference of Named Entity Recognition and Normalization for Tweets | related_work | Related Work | obj_f1 | F1 | metric | generic_metric | F1 | f1 | exact_alias | 136 | 138 | 0.7 | sentence_text | generic_metric | False | registry_seed:obj_f1;alias=F1 |
| ctxr_4576a187b2316db2076e | ctx_c483e011434345ed021b | R13-1011 | R13-1026 | {T}witter Part-of-Speech Tagging for All: Overcoming Sparse and Noisy Data | unknown | Named Entity Recognition | obj_f1 | F1 | metric | generic_metric | F1 | f1 | exact_alias | 173 | 175 | 0.7 | sentence_text | generic_metric | False | registry_seed:obj_f1;alias=F1 |
| ctxr_d1d006db73b0c50f7eda | ctx_18d9e4addeb84b24a7ea | R13-1011 | D11-1141 | Named Entity Recognition in Tweets: An Experimental Study | unknown | Named Entity Recognition | obj_f1 | F1 | metric | generic_metric | F1 | f1 | exact_alias | 173 | 175 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_f1;alias=F1 |
| ctxr_787e02d85318362f0c93 | ctx_13988ca97286da2b8d27 | R13-1011 | R13-1026 | {T}witter Part-of-Speech Tagging for All: Overcoming Sparse and Noisy Data | unknown | Named Entity Recognition | obj_f1 | F1 | metric | generic_metric | F1 | f1 | exact_alias | 173 | 175 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_f1;alias=F1 |
| ctxr_3bdfbc3c70f3a1503828 | ctx_b2ae8b715fdce6f50697 | 2021.codi-sharedtask.6 | C18-1003 | They Exist! Introducing Plural Mentions to Coreference Resolution and Entity Linking | introduction | Introduction | obj_f1 | F1 | metric | generic_metric | F1 | f1 | exact_alias | 154 | 156 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_f1;alias=F1 |
| ctxr_159cb3ad56563fda84a8 | ctx_2a89e67a3c11ebaaf608 | 2021.codi-sharedtask.6 | N09-2051 | Improving Coreference Resolution by Using Conversational Metadata | introduction | Introduction | obj_f1 | F1 | metric | generic_metric | F1 | f1 | exact_alias | 193 | 195 | 0.7 | sentence_text | generic_metric | False | registry_seed:obj_f1;alias=F1 |
| ctxr_63960aeea9692ba7046e | ctx_3044f297215ebbd030fa | 2020.emnlp-main.686 | 2020.tacl-1.5 | {S}pan{BERT}: Improving Pre-training by Representing and Predicting Spans | results | Results | obj_f1 | F1 | metric | generic_metric | F1 | f1 | exact_alias | 47 | 49 | 0.7 | sentence_text | generic_metric | False | registry_seed:obj_f1;alias=F1 |
| ctxr_c061f13123edb2679720 | ctx_6c17c4583f96f7e26949 | 2020.acl-main.259 | D18-1060 | Neural Metaphor Detection in Context | system_description | System Description | obj_f1 | F1 | metric | generic_metric | F1 | f1 | exact_alias | 171 | 173 | 0.7 | sentence_text | generic_metric | False | registry_seed:obj_f1;alias=F1 |
| ctxr_c061f13123edb2679720 | ctx_6c17c4583f96f7e26949 | 2020.acl-main.259 | D18-1060 | Neural Metaphor Detection in Context | system_description | System Description | obj_f1 | F1 | metric | generic_metric | F1 | f1 | exact_alias | 182 | 184 | 0.7 | sentence_text | generic_metric | False | registry_seed:obj_f1;alias=F1 |
| ctxr_cebfed44a2a7543138b1 | ctx_52f8c6380918bb92c42a | 2020.acl-main.259 | P19-1378 | End-to-End Sequential Metaphor Identification Inspired by Linguistic Theories | system_description | System Description | obj_f1 | F1 | metric | generic_metric | F1 | f1 | exact_alias | 171 | 173 | 0.7 | sentence_text | generic_metric | False | registry_seed:obj_f1;alias=F1 |
| ctxr_cebfed44a2a7543138b1 | ctx_52f8c6380918bb92c42a | 2020.acl-main.259 | P19-1378 | End-to-End Sequential Metaphor Identification Inspired by Linguistic Theories | system_description | System Description | obj_f1 | F1 | metric | generic_metric | F1 | f1 | exact_alias | 182 | 184 | 0.7 | sentence_text | generic_metric | False | registry_seed:obj_f1;alias=F1 |
| ctxr_b4deba2d578dce15ff68 | ctx_84a3aef3a5d1e07b6223 | 2020.acl-main.259 | P19-1378 | End-to-End Sequential Metaphor Identification Inspired by Linguistic Theories | system_description | System Description | obj_f1 | F1 | metric | generic_metric | F1 | f1 | exact_alias | 171 | 173 | 0.7 | sentence_text | generic_metric | False | registry_seed:obj_f1;alias=F1 |
| ctxr_b4deba2d578dce15ff68 | ctx_84a3aef3a5d1e07b6223 | 2020.acl-main.259 | P19-1378 | End-to-End Sequential Metaphor Identification Inspired by Linguistic Theories | system_description | System Description | obj_f1 | F1 | metric | generic_metric | F1 | f1 | exact_alias | 182 | 184 | 0.7 | sentence_text | generic_metric | False | registry_seed:obj_f1;alias=F1 |
| ctxr_68b823825c212fb278ca | ctx_ef39fe1e3f8a6df16dfa | 2021.nlp4convai-1.14 | N16-1014 | A Diversity-Promoting Objective Function for Neural Conversation Models | experiment | Experimental Results | obj_f1 | F1 | metric | generic_metric | F1 | f1 | exact_alias | 50 | 52 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_f1;alias=F1 |

## Potential False Positives: Inside Longer Words
No records available.

## Potential False Positives: Very Common Terms
| context_id | source_context_id | citing_paper_id | resolved_cited_acl_id | resolved_cited_title | normalized_section | raw_section_name | object_id | canonical_name | object_type | object_category | surface_form | normalized_surface | match_type | char_start | char_end | confidence | matched_in | match_policy | allow_in_object_graph | provenance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_d573e73d4a69363cdfc0 | ctx_2058502beaf095f8c9d9 | R13-1042 | P11-1118 | Disentangling Chat with Local Coherence Models | results | Results | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 215 | 223 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_fde2b4fe687323ff4bd3 | ctx_ce3b0066680b71c0ab36 | W05-0818 | W03-0301 | An Evaluation Exercise for Word Alignment | experiment | Experiments | obj_f1 | F1 | metric | generic_metric | F -measure | f measure | punctuation_normalized_alias | 58 | 68 | 0.7 | sentence_text | generic_metric | False | registry_seed:obj_f1;alias=F measure |
| ctxr_794ff11af106441610a2 | ctx_7f225179a64758da5dba | W05-0821 | C04-1022 | Automatic Learning of Language Model Structure | model | Factored Language Models | obj_perplexity | perplexity | metric | generic_metric | perplexity | perplexity | exact_alias | 408 | 418 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_perplexity;alias=perplexity |
| ctxr_b4edfcd618c4edc4d4dc | ctx_baae2db29cd713e28052 | R13-1046 | W13-1101 | Does Size Matter? Text and Grammar Revision for Parsing Social Media Data | introduction | Introduction and Motivation | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 274 | 282 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_f7c720ac514891b21f33 | ctx_9467c404bd35ecd142b4 | R13-1046 | E06-1011 | Online Learning of Approximate Dependency Parsing Algorithms | unknown | Parser | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 105 | 113 | 0.7 | sentence_text | generic_metric | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_26559d1672acccfd09ea | ctx_9c84cb4ef671e246a5be | R13-1046 | P05-1012 | Online Large-Margin Training of Dependency Parsers | unknown | Parser | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 105 | 113 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_c223321394c5bbc2bcec | ctx_c68731c0340fcd07d57b | R13-1046 | A00-1031 | {T}n{T} {--} A Statistical Part-of-Speech Tagger | unknown | The effect of POS tagging | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 30 | 38 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_c223321394c5bbc2bcec | ctx_c68731c0340fcd07d57b | R13-1046 | A00-1031 | {T}n{T} {--} A Statistical Part-of-Speech Tagger | unknown | The effect of POS tagging | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 217 | 225 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_72089786b736eb3c1d50 | ctx_2868157b89a3f8bb0973 | R13-1046 | W13-1101 | Does Size Matter? Text and Grammar Revision for Parsing Social Media Data | unknown | The effect of POS tagging | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 151 | 159 | 0.7 | sentence_text | generic_metric | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_1348abfe0d9ee416094f | ctx_75f51b85f7f3b4850622 | 2009.mtsummit-posters.23 | 2007.mtsummit-papers.64 | {J}apanese-{H}ungarian dictionary generation using ontology resources | dataset | Resource issues | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 356 | 364 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_9af9bd56af035c2cee84 | ctx_4ef870281b839f0e6cad | R13-1048 | P06-1041 | Hybrid Parsing: Using Probabilistic Models as Predictors for a Symbolic Parser | unknown | MaltParser as a Predictor for jwcdg | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 94 | 102 | 0.7 | sentence_text | generic_metric | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_9ecca4bac0344e435a50 | ctx_08464d970bac736b3c5a | R13-1048 | W03-3017 | An Efficient Algorithm for Projective Dependency Parsing | unknown | MaltParser as a Predictor for jwcdg | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 338 | 346 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_9ecca4bac0344e435a50 | ctx_08464d970bac736b3c5a | R13-1048 | W03-3017 | An Efficient Algorithm for Projective Dependency Parsing | unknown | MaltParser as a Predictor for jwcdg | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 392 | 400 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_12dda98b18b7e159cf6c | ctx_f9ad96418feda15bffe7 | R13-1048 | W09-3816 | Co-Parsing with Competitive Models | unknown | MaltParser as a Predictor for jwcdg | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 97 | 105 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_12dda98b18b7e159cf6c | ctx_f9ad96418feda15bffe7 | R13-1048 | W09-3816 | Co-Parsing with Competitive Models | unknown | MaltParser as a Predictor for jwcdg | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 151 | 159 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_6f4fbb5a1e4f3b2f971a | ctx_b4f5a1a27ec820df30f4 | R13-1048 | W06-2932 | Multilingual Dependency Analysis with a Two-Stage Discriminative Parser | unknown | MaltParser as a Predictor for jwcdg | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 97 | 105 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_6f4fbb5a1e4f3b2f971a | ctx_b4f5a1a27ec820df30f4 | R13-1048 | W06-2932 | Multilingual Dependency Analysis with a Two-Stage Discriminative Parser | unknown | MaltParser as a Predictor for jwcdg | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 151 | 159 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_448d50f47d83c101d92f | ctx_3e66b0fb7777637aa22e | R13-1048 | A00-1031 | {T}n{T} {--} A Statistical Part-of-Speech Tagger | unknown | MaltParser as a Predictor for jwcdg | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 157 | 165 | 0.7 | sentence_text | generic_metric | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_cb27bb574c756f008de2 | ctx_da4ba23393fcc1c80f81 | Y18-1058 | J02-3001 | Automatic Labeling of Semantic Roles | related_work | Related Work | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 134 | 142 | 0.7 | sentence_text | generic_metric | False | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_b3f99b73329db6bbf332 | ctx_b1e4dd030768fc6c52f7 | Y18-1058 | P03-1002 | Using Predicate-Argument Structures for Information Extraction | related_work | Related Work | obj_accuracy | accuracy | metric | generic_metric | accuracy | accuracy | exact_alias | 134 | 142 | 0.6 | context_window_neighbor | generic_metric;neighbor_context_match | False | registry_seed:obj_accuracy;alias=accuracy |

## Negative Alias Blocked Examples
No records available.

## Recommendations
Review short aliases and common metric/model terms before a full run. The sample output is suitable for registry refinement, but noisy terms such as accuracy, F1, perplexity, Transformer, or PTB should be checked manually.
