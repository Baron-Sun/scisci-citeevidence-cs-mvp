# Object Matching Sample Report

## Inputs
- Contexts: `data/processed/analysis_ready_strong_contexts.parquet`
- Registry: `configs/object_registry_seed.yaml`

## Outputs
- Object mentions sample: `data/processed/object_mentions_sample.parquet`

## Core Metrics
| metric | value |
| --- | --- |
| input context rows processed | 50000 |
| configured limit | 50000 |
| registry objects | 36 |
| contexts with at least one object mention | 12255 |
| total object mentions | 31291 |
| negative alias blocked count | 0 |

## Object Mentions By Object Type
| object_type | mentions |
| --- | --- |
| model | 8727 |
| metric | 8181 |
| dataset_or_database | 4536 |
| method | 4260 |
| software_or_tool | 3058 |
| benchmark_or_protocol | 2529 |

## Top 50 Matched Objects
| object_id | canonical_name | object_type | mentions |
| --- | --- | --- | --- |
| obj_bleu | BLEU | metric | 3477 |
| obj_crf | CRF | method | 2893 |
| obj_bert | BERT | model | 2442 |
| obj_accuracy | accuracy | metric | 2300 |
| obj_lstm | LSTM | model | 2135 |
| obj_transformer | Transformer | model | 1833 |
| obj_penn_treebank | Penn Treebank | dataset_or_database | 1668 |
| obj_wordnet | WordNet | dataset_or_database | 1656 |
| obj_moses | Moses | software_or_tool | 1408 |
| obj_giza | GIZA++ | software_or_tool | 1183 |
| obj_wmt | WMT | benchmark_or_protocol | 1178 |
| obj_seq2seq | seq2seq | model | 1127 |
| obj_hmm | HMM | method | 1049 |
| obj_semeval | SemEval | benchmark_or_protocol | 994 |
| obj_f1 | F1 | metric | 922 |
| obj_meteor | METEOR | metric | 707 |
| obj_framenet | FrameNet | dataset_or_database | 505 |
| obj_word2vec | word2vec | model | 493 |
| obj_rouge | ROUGE | metric | 455 |
| obj_glove | GloVe | model | 408 |
| obj_perplexity | perplexity | metric | 320 |
| obj_attention_mechanism | attention mechanism | method | 318 |
| obj_propbank | PropBank | dataset_or_database | 307 |
| obj_elmo | ELMo | model | 289 |
| obj_opus | OPUS | software_or_tool | 192 |
| obj_conll_2003 | CoNLL-2003 | benchmark_or_protocol | 191 |
| obj_squad | SQuAD | dataset_or_database | 178 |
| obj_stanford_corenlp | Stanford CoreNLP | software_or_tool | 140 |
| obj_ontonotes | OntoNotes | dataset_or_database | 139 |
| obj_glue | GLUE | benchmark_or_protocol | 95 |
| obj_nltk | NLTK | software_or_tool | 95 |
| obj_snli | SNLI | dataset_or_database | 73 |
| obj_conll_2012 | CoNLL-2012 | benchmark_or_protocol | 64 |
| obj_spacy | spaCy | software_or_tool | 40 |
| obj_multinli | MultiNLI | dataset_or_database | 10 |
| obj_superglue | SuperGLUE | benchmark_or_protocol | 7 |

## Top 50 Surface Forms
| surface_form | canonical_name | object_type | mentions |
| --- | --- | --- | --- |
| BLEU | BLEU | metric | 2920 |
| BERT | BERT | model | 2301 |
| accuracy | accuracy | metric | 2131 |
| LSTM | LSTM | model | 1818 |
| CRF | CRF | method | 1448 |
| WordNet | WordNet | dataset_or_database | 1361 |
| WMT | WMT | benchmark_or_protocol | 1070 |
| Moses | Moses | software_or_tool | 1003 |
| Penn Treebank | Penn Treebank | dataset_or_database | 983 |
| GIZA++ | GIZA++ | software_or_tool | 899 |
| SemEval | SemEval | benchmark_or_protocol | 857 |
| Transformer | Transformer | model | 843 |
| HMM | HMM | method | 814 |
| PTB | Penn Treebank | dataset_or_database | 588 |
| METEOR | METEOR | metric | 557 |
| CRFs | CRF | method | 509 |
| FrameNet | FrameNet | dataset_or_database | 478 |
| BLEU score | BLEU | metric | 453 |
| Conditional Random Fields | CRF | method | 451 |
| ROUGE | ROUGE | metric | 432 |
| Transformers | Transformer | model | 423 |
| transformer | Transformer | model | 385 |
| encoder-decoder | seq2seq | model | 374 |
| word2vec | word2vec | model | 336 |
| F1 | F1 | metric | 322 |
| perplexity | perplexity | metric | 262 |
| PropBank | PropBank | dataset_or_database | 255 |
| Giza++ | GIZA++ | software_or_tool | 241 |
| attention mechanism | attention mechanism | method | 238 |
| ELMo | ELMo | model | 234 |
| Conditional Random Field | CRF | method | 211 |
| F-score | F1 | metric | 199 |
| GloVe | GloVe | model | 197 |
| seq2seq | seq2seq | model | 187 |
| sequence-to-sequence | seq2seq | model | 164 |
| F-measure | F1 | metric | 161 |
| Moses toolkit | Moses | software_or_tool | 158 |
| Wordnet | WordNet | dataset_or_database | 158 |
| SQuAD | SQuAD | dataset_or_database | 146 |
| Meteor | METEOR | metric | 143 |
| Accuracy | accuracy | metric | 142 |
| OPUS | OPUS | software_or_tool | 142 |
| MOSES | Moses | software_or_tool | 140 |
| Word2Vec | word2vec | model | 137 |
| Long Short-Term Memory | LSTM | model | 129 |
| wordnet | WordNet | dataset_or_database | 126 |
| OntoNotes | OntoNotes | dataset_or_database | 118 |
| Global Vectors for Word Representation | GloVe | model | 116 |
| Stanford CoreNLP | Stanford CoreNLP | software_or_tool | 116 |
| CoNLL'03 | CoNLL-2003 | benchmark_or_protocol | 114 |

## Matches By Normalized Section
| normalized_section | mentions |
| --- | --- |
| unknown | 8945 |
| introduction | 7403 |
| related_work | 4622 |
| experiment | 1894 |
| dataset | 1562 |
| model | 1477 |
| evaluation | 1401 |
| method | 1145 |
| results | 993 |
| background | 447 |
| conclusion | 435 |
| system_description | 295 |
| discussion | 233 |
| abstract | 200 |
| implementation | 118 |
| analysis | 90 |
| task_definition | 18 |
| error_analysis | 13 |

## Matches By Matched In
| matched_in | mentions |
| --- | --- |
| context_window_s3 | 17932 |
| sentence_text | 9930 |
| resolved_cited_title | 3429 |

## Examples Per Object Type
| example_group | context_id | source_context_id | citing_paper_id | resolved_cited_acl_id | resolved_cited_title | normalized_section | raw_section_name | object_id | canonical_name | object_type | surface_form | match_type | char_start | char_end | confidence | matched_in | provenance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| benchmark_or_protocol | ctxr_f6863fcab52657a5c16e | ctx_f31d14d5a204a23fdb80 | R13-1044 | S10-1049 | {ISI}: Automatic Classification of Relations Between Nominals Using a Maximum Entropy Classifier | related_work | Related work | obj_semeval | SemEval | benchmark_or_protocol | SemEval | exact_alias | 13 | 20 | 0.95 | context_window_s3 | registry_seed:obj_semeval;alias=SemEval |
| benchmark_or_protocol | ctxr_5d48c41b1f5fe52a0a74 | ctx_2e80df002a498416e487 | 2020.nlp4convai-1.15 | P18-1198 | What you can cram into a single {\$}{\&}!{\#}* vector: Probing sentence embeddings for linguistic properties | related_work | Related Work | obj_glue | GLUE | benchmark_or_protocol | GLUE | exact_alias | 543 | 547 | 0.95 | context_window_s3 | registry_seed:obj_glue;alias=GLUE |
| benchmark_or_protocol | ctxr_5d48c41b1f5fe52a0a74 | ctx_2e80df002a498416e487 | 2020.nlp4convai-1.15 | P18-1198 | What you can cram into a single {\$}{\&}!{\#}* vector: Probing sentence embeddings for linguistic properties | related_work | Related Work | obj_superglue | SuperGLUE | benchmark_or_protocol | SuperGLUE | exact_alias | 572 | 581 | 0.95 | context_window_s3 | registry_seed:obj_superglue;alias=SuperGLUE |
| benchmark_or_protocol | ctxr_2e1b725a056f254d1a31 | ctx_b83f0fe222eebdccc4ad | 2020.nlp4convai-1.15 | P18-1198 | What you can cram into a single {\$}{\&}!{\#}* vector: Probing sentence embeddings for linguistic properties | related_work | Related Work | obj_glue | GLUE | benchmark_or_protocol | GLUE | exact_alias | 543 | 547 | 0.95 | context_window_s3 | registry_seed:obj_glue;alias=GLUE |
| benchmark_or_protocol | ctxr_2e1b725a056f254d1a31 | ctx_b83f0fe222eebdccc4ad | 2020.nlp4convai-1.15 | P18-1198 | What you can cram into a single {\$}{\&}!{\#}* vector: Probing sentence embeddings for linguistic properties | related_work | Related Work | obj_superglue | SuperGLUE | benchmark_or_protocol | SuperGLUE | exact_alias | 572 | 581 | 0.95 | context_window_s3 | registry_seed:obj_superglue;alias=SuperGLUE |
| dataset_or_database | ctxr_caa50477f333d1e3c48b | ctx_1cf74ef13884c4116a34 | R13-1046 | J93-2004 | Building a Large Annotated Corpus of {E}nglish: The {P}enn {T}reebank | dataset | Data | obj_penn_treebank | Penn Treebank | dataset_or_database | Penn Treebank | exact_alias | 93 | 106 | 0.95 | sentence_text | registry_seed:obj_penn_treebank;alias=Penn Treebank |
| dataset_or_database | ctxr_caa50477f333d1e3c48b | ctx_1cf74ef13884c4116a34 | R13-1046 | J93-2004 | Building a Large Annotated Corpus of {E}nglish: The {P}enn {T}reebank | dataset | Data | obj_penn_treebank | Penn Treebank | dataset_or_database | PTB | exact_alias | 108 | 111 | 0.95 | sentence_text | registry_seed:obj_penn_treebank;alias=PTB |
| dataset_or_database | ctxr_caa50477f333d1e3c48b | ctx_1cf74ef13884c4116a34 | R13-1046 | J93-2004 | Building a Large Annotated Corpus of {E}nglish: The {P}enn {T}reebank | dataset | Data | obj_penn_treebank | Penn Treebank | dataset_or_database | Penn Treebank | exact_alias | 93 | 106 | 0.95 | context_window_s3 | registry_seed:obj_penn_treebank;alias=Penn Treebank |
| dataset_or_database | ctxr_caa50477f333d1e3c48b | ctx_1cf74ef13884c4116a34 | R13-1046 | J93-2004 | Building a Large Annotated Corpus of {E}nglish: The {P}enn {T}reebank | dataset | Data | obj_penn_treebank | Penn Treebank | dataset_or_database | PTB | exact_alias | 108 | 111 | 0.95 | context_window_s3 | registry_seed:obj_penn_treebank;alias=PTB |
| dataset_or_database | ctxr_d2f7e10dccf772790070 | ctx_3052c12f694776848067 | R13-1046 | W08-1301 | The {S}tanford Typed Dependencies Representation | dataset | Data | obj_penn_treebank | Penn Treebank | dataset_or_database | PTB | exact_alias | 36 | 39 | 0.95 | sentence_text | registry_seed:obj_penn_treebank;alias=PTB |
| method | ctxr_3e4722d1950da619a7dd | ctx_ca6cc2ce8812268acdb7 | R13-1044 | L12-1574 | {KPW}r: Towards a Free Corpus of {P}olish | unknown | Recognizing word pairs and triples | obj_crf | CRF | method | CRF | exact_alias | 17 | 20 | 0.95 | sentence_text | registry_seed:obj_crf;alias=CRF |
| method | ctxr_3e4722d1950da619a7dd | ctx_ca6cc2ce8812268acdb7 | R13-1044 | L12-1574 | {KPW}r: Towards a Free Corpus of {P}olish | unknown | Recognizing word pairs and triples | obj_crf | CRF | method | CRF | exact_alias | 99 | 102 | 0.95 | context_window_s3 | registry_seed:obj_crf;alias=CRF |
| method | ctxr_6ec7b60115b4d5e6dcf1 | ctx_8ee4e60043981a38782e | R13-1046 | N10-1120 | Dependency Tree-based Sentiment Classification using {CRF}s with Hidden Variables | introduction | Introduction and Motivation | obj_crf | CRF | method | CRF | exact_alias | 54 | 57 | 0.95 | resolved_cited_title | registry_seed:obj_crf;alias=CRF |
| method | ctxr_023a8eacb53c5fb15079 | ctx_fda17dcdd461f7773e54 | R13-1051 | N04-4028 | Confidence Estimation for Information Extraction | related_work | Related Work | obj_hmm | HMM | method | hidden Markov models | exact_alias | 32 | 52 | 0.95 | context_window_s3 | registry_seed:obj_hmm;alias=hidden Markov models |
| method | ctxr_023a8eacb53c5fb15079 | ctx_fda17dcdd461f7773e54 | R13-1051 | N04-4028 | Confidence Estimation for Information Extraction | related_work | Related Work | obj_crf | CRF | method | Conditional Random Field | case_insensitive_alias | 442 | 466 | 0.95 | context_window_s3 | registry_seed:obj_crf;alias=conditional random field |
| metric | ctxr_d573e73d4a69363cdfc0 | ctx_2058502beaf095f8c9d9 | R13-1042 | P11-1118 | Disentangling Chat with Local Coherence Models | results | Results | obj_accuracy | accuracy | metric | accuracy | exact_alias | 215 | 223 | 0.7 | context_window_s3 | registry_seed:obj_accuracy;alias=accuracy |
| metric | ctxr_fde2b4fe687323ff4bd3 | ctx_ce3b0066680b71c0ab36 | W05-0818 | W03-0301 | An Evaluation Exercise for Word Alignment | experiment | Experiments | obj_f1 | F1 | metric | F -measure | punctuation_normalized_alias | 58 | 68 | 0.7 | sentence_text | registry_seed:obj_f1;alias=F measure |
| metric | ctxr_fde2b4fe687323ff4bd3 | ctx_ce3b0066680b71c0ab36 | W05-0818 | W03-0301 | An Evaluation Exercise for Word Alignment | experiment | Experiments | obj_f1 | F1 | metric | F -measure | punctuation_normalized_alias | 58 | 68 | 0.7 | context_window_s3 | registry_seed:obj_f1;alias=F measure |
| metric | ctxr_794ff11af106441610a2 | ctx_7f225179a64758da5dba | W05-0821 | C04-1022 | Automatic Learning of Language Model Structure | model | Factored Language Models | obj_perplexity | perplexity | metric | perplexity | exact_alias | 408 | 418 | 0.7 | context_window_s3 | registry_seed:obj_perplexity;alias=perplexity |
| metric | ctxr_794ff11af106441610a2 | ctx_7f225179a64758da5dba | W05-0821 | C04-1022 | Automatic Learning of Language Model Structure | model | Factored Language Models | obj_bleu | BLEU | metric | BLEU | exact_alias | 481 | 485 | 0.95 | context_window_s3 | registry_seed:obj_bleu;alias=BLEU |
| model | ctxr_1527f42ff080e1df1961 | ctx_32be8b860cb0185b7c19 | Y18-1058 | P15-1109 | End-to-end learning of semantic role labeling using recurrent neural networks | related_work | Related Work | obj_lstm | LSTM | model | LSTM | exact_alias | 100 | 104 | 0.95 | sentence_text | registry_seed:obj_lstm;alias=LSTM |
| model | ctxr_1527f42ff080e1df1961 | ctx_32be8b860cb0185b7c19 | Y18-1058 | P15-1109 | End-to-end learning of semantic role labeling using recurrent neural networks | related_work | Related Work | obj_lstm | LSTM | model | LSTM | exact_alias | 200 | 204 | 0.95 | context_window_s3 | registry_seed:obj_lstm;alias=LSTM |
| model | ctxr_1527f42ff080e1df1961 | ctx_32be8b860cb0185b7c19 | Y18-1058 | P15-1109 | End-to-end learning of semantic role labeling using recurrent neural networks | related_work | Related Work | obj_lstm | LSTM | model | LSTM | exact_alias | 292 | 296 | 0.95 | context_window_s3 | registry_seed:obj_lstm;alias=LSTM |
| model | ctxr_378723e2689534552b44 | ctx_031529e47516f4dc37b8 | Y18-1058 | P16-1113 | Neural Semantic Role Labeling with Dependency Path Embeddings | related_work | Related Work | obj_lstm | LSTM | model | LSTM | exact_alias | 54 | 58 | 0.95 | sentence_text | registry_seed:obj_lstm;alias=LSTM |
| model | ctxr_378723e2689534552b44 | ctx_031529e47516f4dc37b8 | Y18-1058 | P16-1113 | Neural Semantic Role Labeling with Dependency Path Embeddings | related_work | Related Work | obj_lstm | LSTM | model | LSTM | exact_alias | 100 | 104 | 0.95 | context_window_s3 | registry_seed:obj_lstm;alias=LSTM |
| software_or_tool | ctxr_4355448353bdd023508c | ctx_e33a1b32079c54fb1946 | W05-0820 | J03-1002 | A Systematic Comparison of Various Statistical Alignment Models | unknown | Work on new language pairs, new problems: | obj_giza | GIZA++ | software_or_tool | GIZA++ | exact_alias | 128 | 134 | 0.95 | sentence_text | registry_seed:obj_giza;alias=GIZA++ |
| software_or_tool | ctxr_4355448353bdd023508c | ctx_e33a1b32079c54fb1946 | W05-0820 | J03-1002 | A Systematic Comparison of Various Statistical Alignment Models | unknown | Work on new language pairs, new problems: | obj_giza | GIZA++ | software_or_tool | GIZA++ | exact_alias | 220 | 226 | 0.95 | context_window_s3 | registry_seed:obj_giza;alias=GIZA++ |
| software_or_tool | ctxr_e4bd8b3cb291ec3f4e15 | ctx_2a912ffa75455b48a752 | W05-0823 | P00-1056 | Improved Statistical Alignment Models | method | Preprocessing and Alignment | obj_giza | GIZA++ | software_or_tool | GIZA++ | exact_alias | 147 | 153 | 0.95 | sentence_text | registry_seed:obj_giza;alias=GIZA++ |
| software_or_tool | ctxr_e4bd8b3cb291ec3f4e15 | ctx_2a912ffa75455b48a752 | W05-0823 | P00-1056 | Improved Statistical Alignment Models | method | Preprocessing and Alignment | obj_giza | GIZA++ | software_or_tool | GIZA++ | exact_alias | 147 | 153 | 0.95 | context_window_s3 | registry_seed:obj_giza;alias=GIZA++ |
| software_or_tool | ctxr_059fae894b25c9864d24 | ctx_57cb88547b3a3b152a3c | W05-0825 | J03-1002 | A Systematic Comparison of Various Statistical Alignment Models | experiment | Experimental Results | obj_giza | GIZA++ | software_or_tool | GIZA++ | exact_alias | 64 | 70 | 0.95 | sentence_text | registry_seed:obj_giza;alias=GIZA++ |

## Potential False Positives: Short Aliases
| context_id | source_context_id | citing_paper_id | resolved_cited_acl_id | resolved_cited_title | normalized_section | raw_section_name | object_id | canonical_name | object_type | surface_form | match_type | char_start | char_end | confidence | matched_in | provenance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_e95bf185b7763672a3fb | ctx_f25016042ecb1f4a27bc | 2021.ranlp-1.12 | L12-1519 | {JRC} Eurovoc Indexer {JEX} - A freely available multi-label categorisation tool | results | Results | obj_f1 | F1 | metric | F1 | exact_alias | 303 | 305 | 0.7 | context_window_s3 | registry_seed:obj_f1;alias=F1 |
| ctxr_0d792967967b7e61ce96 | ctx_be7d56079c57867d8945 | 2020.nlp4convai-1.12 | W19-4302 | To Tune or Not to Tune? Adapting Pretrained Representations to Diverse Tasks | model | Model Variants | obj_f1 | F1 | metric | F1 | exact_alias | 76 | 78 | 0.7 | context_window_s3 | registry_seed:obj_f1;alias=F1 |
| ctxr_0d792967967b7e61ce96 | ctx_be7d56079c57867d8945 | 2020.nlp4convai-1.12 | W19-4302 | To Tune or Not to Tune? Adapting Pretrained Representations to Diverse Tasks | model | Model Variants | obj_f1 | F1 | metric | F1 | exact_alias | 107 | 109 | 0.7 | context_window_s3 | registry_seed:obj_f1;alias=F1 |
| ctxr_acb5296965477dcd7fc1 | ctx_c2d09fdaf080118f5a47 | W09-1304 | W08-0607 | Recognizing Speculative Language in Biomedical Research Articles: A Linguistically Motivated Perspective | related_work | Related work | obj_f1 | F1 | metric | F1 | exact_alias | 37 | 39 | 0.7 | context_window_s3 | registry_seed:obj_f1;alias=F1 |
| ctxr_bf3a49c02b8d1648eeed | ctx_7345dcdfebfed6d9f7ff | 2020.lrec-1.337 | K18-2017 | {NLP}-Cube: End-to-End Raw Text Processing With Neural Networks | dataset | Linguistic Annotation | obj_f1 | F1 | metric | F1 | exact_alias | 615 | 617 | 0.7 | context_window_s3 | registry_seed:obj_f1;alias=F1 |
| ctxr_a301ae3146c0df1bd958 | ctx_aed4cd20d032b7acf653 | R13-1011 | D11-1141 | Named Entity Recognition in Tweets: An Experimental Study | related_work | Related Work | obj_f1 | F1 | metric | F1 | exact_alias | 383 | 385 | 0.7 | context_window_s3 | registry_seed:obj_f1;alias=F1 |
| ctxr_5996b8e55aa47f88c8bc | ctx_cb7547dca250c54f4aee | R13-1011 | P12-1055 | Joint Inference of Named Entity Recognition and Normalization for Tweets | related_work | Related Work | obj_f1 | F1 | metric | F1 | exact_alias | 136 | 138 | 0.7 | sentence_text | registry_seed:obj_f1;alias=F1 |
| ctxr_5996b8e55aa47f88c8bc | ctx_cb7547dca250c54f4aee | R13-1011 | P12-1055 | Joint Inference of Named Entity Recognition and Normalization for Tweets | related_work | Related Work | obj_f1 | F1 | metric | F1 | exact_alias | 294 | 296 | 0.7 | context_window_s3 | registry_seed:obj_f1;alias=F1 |
| ctxr_4576a187b2316db2076e | ctx_c483e011434345ed021b | R13-1011 | R13-1026 | {T}witter Part-of-Speech Tagging for All: Overcoming Sparse and Noisy Data | unknown | Named Entity Recognition | obj_f1 | F1 | metric | F1 | exact_alias | 173 | 175 | 0.7 | sentence_text | registry_seed:obj_f1;alias=F1 |
| ctxr_4576a187b2316db2076e | ctx_c483e011434345ed021b | R13-1011 | R13-1026 | {T}witter Part-of-Speech Tagging for All: Overcoming Sparse and Noisy Data | unknown | Named Entity Recognition | obj_f1 | F1 | metric | F1 | exact_alias | 383 | 385 | 0.7 | context_window_s3 | registry_seed:obj_f1;alias=F1 |
| ctxr_d1d006db73b0c50f7eda | ctx_18d9e4addeb84b24a7ea | R13-1011 | D11-1141 | Named Entity Recognition in Tweets: An Experimental Study | unknown | Named Entity Recognition | obj_f1 | F1 | metric | F1 | exact_alias | 173 | 175 | 0.7 | context_window_s3 | registry_seed:obj_f1;alias=F1 |
| ctxr_787e02d85318362f0c93 | ctx_13988ca97286da2b8d27 | R13-1011 | R13-1026 | {T}witter Part-of-Speech Tagging for All: Overcoming Sparse and Noisy Data | unknown | Named Entity Recognition | obj_f1 | F1 | metric | F1 | exact_alias | 173 | 175 | 0.7 | context_window_s3 | registry_seed:obj_f1;alias=F1 |
| ctxr_3bdfbc3c70f3a1503828 | ctx_b2ae8b715fdce6f50697 | 2021.codi-sharedtask.6 | C18-1003 | They Exist! Introducing Plural Mentions to Coreference Resolution and Entity Linking | introduction | Introduction | obj_f1 | F1 | metric | F1 | exact_alias | 154 | 156 | 0.7 | context_window_s3 | registry_seed:obj_f1;alias=F1 |
| ctxr_159cb3ad56563fda84a8 | ctx_2a89e67a3c11ebaaf608 | 2021.codi-sharedtask.6 | N09-2051 | Improving Coreference Resolution by Using Conversational Metadata | introduction | Introduction | obj_f1 | F1 | metric | F1 | exact_alias | 193 | 195 | 0.7 | sentence_text | registry_seed:obj_f1;alias=F1 |
| ctxr_159cb3ad56563fda84a8 | ctx_2a89e67a3c11ebaaf608 | 2021.codi-sharedtask.6 | N09-2051 | Improving Coreference Resolution by Using Conversational Metadata | introduction | Introduction | obj_f1 | F1 | metric | F1 | exact_alias | 371 | 373 | 0.7 | context_window_s3 | registry_seed:obj_f1;alias=F1 |
| ctxr_63960aeea9692ba7046e | ctx_3044f297215ebbd030fa | 2020.emnlp-main.686 | 2020.tacl-1.5 | {S}pan{BERT}: Improving Pre-training by Representing and Predicting Spans | results | Results | obj_f1 | F1 | metric | F1 | exact_alias | 47 | 49 | 0.7 | sentence_text | registry_seed:obj_f1;alias=F1 |
| ctxr_63960aeea9692ba7046e | ctx_3044f297215ebbd030fa | 2020.emnlp-main.686 | 2020.tacl-1.5 | {S}pan{BERT}: Improving Pre-training by Representing and Predicting Spans | results | Results | obj_f1 | F1 | metric | F1 | exact_alias | 107 | 109 | 0.7 | context_window_s3 | registry_seed:obj_f1;alias=F1 |
| ctxr_c061f13123edb2679720 | ctx_6c17c4583f96f7e26949 | 2020.acl-main.259 | D18-1060 | Neural Metaphor Detection in Context | system_description | System Description | obj_f1 | F1 | metric | F1 | exact_alias | 171 | 173 | 0.7 | sentence_text | registry_seed:obj_f1;alias=F1 |
| ctxr_c061f13123edb2679720 | ctx_6c17c4583f96f7e26949 | 2020.acl-main.259 | D18-1060 | Neural Metaphor Detection in Context | system_description | System Description | obj_f1 | F1 | metric | F1 | exact_alias | 182 | 184 | 0.7 | sentence_text | registry_seed:obj_f1;alias=F1 |
| ctxr_c061f13123edb2679720 | ctx_6c17c4583f96f7e26949 | 2020.acl-main.259 | D18-1060 | Neural Metaphor Detection in Context | system_description | System Description | obj_f1 | F1 | metric | F1 | exact_alias | 171 | 173 | 0.7 | context_window_s3 | registry_seed:obj_f1;alias=F1 |

## Potential False Positives: Inside Longer Words
No records available.

## Potential False Positives: Very Common Terms
| context_id | source_context_id | citing_paper_id | resolved_cited_acl_id | resolved_cited_title | normalized_section | raw_section_name | object_id | canonical_name | object_type | surface_form | match_type | char_start | char_end | confidence | matched_in | provenance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_d573e73d4a69363cdfc0 | ctx_2058502beaf095f8c9d9 | R13-1042 | P11-1118 | Disentangling Chat with Local Coherence Models | results | Results | obj_accuracy | accuracy | metric | accuracy | exact_alias | 215 | 223 | 0.7 | context_window_s3 | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_fde2b4fe687323ff4bd3 | ctx_ce3b0066680b71c0ab36 | W05-0818 | W03-0301 | An Evaluation Exercise for Word Alignment | experiment | Experiments | obj_f1 | F1 | metric | F -measure | punctuation_normalized_alias | 58 | 68 | 0.7 | sentence_text | registry_seed:obj_f1;alias=F measure |
| ctxr_fde2b4fe687323ff4bd3 | ctx_ce3b0066680b71c0ab36 | W05-0818 | W03-0301 | An Evaluation Exercise for Word Alignment | experiment | Experiments | obj_f1 | F1 | metric | F -measure | punctuation_normalized_alias | 58 | 68 | 0.7 | context_window_s3 | registry_seed:obj_f1;alias=F measure |
| ctxr_794ff11af106441610a2 | ctx_7f225179a64758da5dba | W05-0821 | C04-1022 | Automatic Learning of Language Model Structure | model | Factored Language Models | obj_perplexity | perplexity | metric | perplexity | exact_alias | 408 | 418 | 0.7 | context_window_s3 | registry_seed:obj_perplexity;alias=perplexity |
| ctxr_b4edfcd618c4edc4d4dc | ctx_baae2db29cd713e28052 | R13-1046 | W13-1101 | Does Size Matter? Text and Grammar Revision for Parsing Social Media Data | introduction | Introduction and Motivation | obj_accuracy | accuracy | metric | accuracy | exact_alias | 274 | 282 | 0.7 | context_window_s3 | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_f7c720ac514891b21f33 | ctx_9467c404bd35ecd142b4 | R13-1046 | E06-1011 | Online Learning of Approximate Dependency Parsing Algorithms | unknown | Parser | obj_accuracy | accuracy | metric | accuracy | exact_alias | 105 | 113 | 0.7 | sentence_text | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_f7c720ac514891b21f33 | ctx_9467c404bd35ecd142b4 | R13-1046 | E06-1011 | Online Learning of Approximate Dependency Parsing Algorithms | unknown | Parser | obj_accuracy | accuracy | metric | accuracy | exact_alias | 105 | 113 | 0.7 | context_window_s3 | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_26559d1672acccfd09ea | ctx_9c84cb4ef671e246a5be | R13-1046 | P05-1012 | Online Large-Margin Training of Dependency Parsers | unknown | Parser | obj_accuracy | accuracy | metric | accuracy | exact_alias | 105 | 113 | 0.7 | context_window_s3 | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_c223321394c5bbc2bcec | ctx_c68731c0340fcd07d57b | R13-1046 | A00-1031 | {T}n{T} {--} A Statistical Part-of-Speech Tagger | unknown | The effect of POS tagging | obj_accuracy | accuracy | metric | accuracy | exact_alias | 30 | 38 | 0.7 | context_window_s3 | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_c223321394c5bbc2bcec | ctx_c68731c0340fcd07d57b | R13-1046 | A00-1031 | {T}n{T} {--} A Statistical Part-of-Speech Tagger | unknown | The effect of POS tagging | obj_accuracy | accuracy | metric | accuracy | exact_alias | 217 | 225 | 0.7 | context_window_s3 | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_72089786b736eb3c1d50 | ctx_2868157b89a3f8bb0973 | R13-1046 | W13-1101 | Does Size Matter? Text and Grammar Revision for Parsing Social Media Data | unknown | The effect of POS tagging | obj_accuracy | accuracy | metric | accuracy | exact_alias | 151 | 159 | 0.7 | sentence_text | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_72089786b736eb3c1d50 | ctx_2868157b89a3f8bb0973 | R13-1046 | W13-1101 | Does Size Matter? Text and Grammar Revision for Parsing Social Media Data | unknown | The effect of POS tagging | obj_accuracy | accuracy | metric | accuracy | exact_alias | 95 | 103 | 0.7 | context_window_s3 | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_72089786b736eb3c1d50 | ctx_2868157b89a3f8bb0973 | R13-1046 | W13-1101 | Does Size Matter? Text and Grammar Revision for Parsing Social Media Data | unknown | The effect of POS tagging | obj_accuracy | accuracy | metric | accuracy | exact_alias | 266 | 274 | 0.7 | context_window_s3 | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_1348abfe0d9ee416094f | ctx_75f51b85f7f3b4850622 | 2009.mtsummit-posters.23 | 2007.mtsummit-papers.64 | {J}apanese-{H}ungarian dictionary generation using ontology resources | dataset | Resource issues | obj_accuracy | accuracy | metric | accuracy | exact_alias | 356 | 364 | 0.7 | context_window_s3 | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_9af9bd56af035c2cee84 | ctx_4ef870281b839f0e6cad | R13-1048 | P06-1041 | Hybrid Parsing: Using Probabilistic Models as Predictors for a Symbolic Parser | unknown | MaltParser as a Predictor for jwcdg | obj_accuracy | accuracy | metric | accuracy | exact_alias | 94 | 102 | 0.7 | sentence_text | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_9af9bd56af035c2cee84 | ctx_4ef870281b839f0e6cad | R13-1048 | P06-1041 | Hybrid Parsing: Using Probabilistic Models as Predictors for a Symbolic Parser | unknown | MaltParser as a Predictor for jwcdg | obj_accuracy | accuracy | metric | accuracy | exact_alias | 295 | 303 | 0.7 | context_window_s3 | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_9ecca4bac0344e435a50 | ctx_08464d970bac736b3c5a | R13-1048 | W03-3017 | An Efficient Algorithm for Projective Dependency Parsing | unknown | MaltParser as a Predictor for jwcdg | obj_accuracy | accuracy | metric | accuracy | exact_alias | 338 | 346 | 0.7 | context_window_s3 | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_9ecca4bac0344e435a50 | ctx_08464d970bac736b3c5a | R13-1048 | W03-3017 | An Efficient Algorithm for Projective Dependency Parsing | unknown | MaltParser as a Predictor for jwcdg | obj_accuracy | accuracy | metric | accuracy | exact_alias | 392 | 400 | 0.7 | context_window_s3 | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_12dda98b18b7e159cf6c | ctx_f9ad96418feda15bffe7 | R13-1048 | W09-3816 | Co-Parsing with Competitive Models | unknown | MaltParser as a Predictor for jwcdg | obj_accuracy | accuracy | metric | accuracy | exact_alias | 97 | 105 | 0.7 | context_window_s3 | registry_seed:obj_accuracy;alias=accuracy |
| ctxr_12dda98b18b7e159cf6c | ctx_f9ad96418feda15bffe7 | R13-1048 | W09-3816 | Co-Parsing with Competitive Models | unknown | MaltParser as a Predictor for jwcdg | obj_accuracy | accuracy | metric | accuracy | exact_alias | 151 | 159 | 0.7 | context_window_s3 | registry_seed:obj_accuracy;alias=accuracy |

## Negative Alias Blocked Examples
No records available.

## Recommendations
Review short aliases and common metric/model terms before a full run. The sample output is suitable for registry refinement, but noisy terms such as accuracy, F1, perplexity, Transformer, or PTB should be checked manually.
