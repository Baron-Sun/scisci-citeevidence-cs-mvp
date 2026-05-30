# Object Mentions LLM-as-Judge Review Report

This is a model-based audit / LLM-assisted validation pass.

## Outputs
- Sample CSV: `data/processed/object_mentions_llm_review_sample.csv`
- JSONL results or dry-run prompts: `data/processed/object_mentions_llm_review_results.jsonl`
- Parquet results: `data/processed/object_mentions_llm_review_results.parquet`

## Core Metrics
| metric | value |
| --- | --- |
| dry run | False |
| sample rows | 200 |
| reviewed rows | 200 |
| dry-run prompt records | 0 |
| fallback unclear rows | 2 |
| from cache rows | 2 |
| precision over true/false reviews | 0.768 |
| input tokens | 232844 |
| output tokens | 28839 |
| total tokens | 261683 |

## Sample Bucket Distribution
| review_bucket | rows |
| --- | --- |
| named_object_high_confidence | 60 |
| generic_metric | 40 |
| ambiguous_short_alias | 30 |
| generic_architecture | 30 |
| cited_title_object_profiles | 20 |
| context_window_neighbor | 20 |

## Reviewer Correct Distribution
| reviewer_correct | rows |
| --- | --- |
| true | 152 |
| false | 46 |
| unclear | 2 |

## Error Type Distribution
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

## Recommended Action Distribution
| recommended_action | rows |
| --- | --- |
| keep | 143 |
| require_context_cue | 28 |
| block_alias | 14 |
| keep_as_feature_only | 10 |
| lower_confidence | 2 |
| other | 2 |
| change_object_type | 1 |

## Graph Allow Distribution
| should_allow_in_object_graph | rows |
| --- | --- |
| False | 133 |
| True | 67 |

## Phase-1 Feature Distribution
| should_use_as_phase1_feature | rows |
| --- | --- |
| True | 142 |
| False | 58 |

## Precision By Object Category
| object_category | reviewed_true_false | correct | incorrect | precision |
| --- | --- | --- | --- | --- |
| named_object | 94 | 85 | 9 | 0.904 |
| generic_metric | 44 | 44 | 0 | 1.000 |
| ambiguous_short_alias | 30 | 0 | 30 | 0.000 |
| generic_architecture | 30 | 23 | 7 | 0.767 |

## Precision By Matched In
| matched_in | reviewed_true_false | correct | incorrect | precision |
| --- | --- | --- | --- | --- |
| sentence_text | 93 | 75 | 18 | 0.806 |
| context_window_neighbor | 86 | 63 | 23 | 0.733 |
| resolved_cited_title | 19 | 14 | 5 | 0.737 |

## Precision By Canonical Name
| canonical_name | reviewed_true_false | correct | incorrect | precision |
| --- | --- | --- | --- | --- |
| Transformer | 38 | 31 | 7 | 0.816 |
| Penn Treebank | 34 | 4 | 30 | 0.118 |
| accuracy | 26 | 26 | 0 | 1.000 |
| F1 | 14 | 14 | 0 | 1.000 |
| BERT | 10 | 9 | 1 | 0.900 |
| CRF | 9 | 9 | 0 | 1.000 |
| BLEU | 8 | 7 | 1 | 0.875 |
| WordNet | 7 | 5 | 2 | 0.714 |
| HMM | 7 | 7 | 0 | 1.000 |
| LSTM | 6 | 6 | 0 | 1.000 |
| seq2seq | 6 | 3 | 3 | 0.500 |
| WMT | 6 | 6 | 0 | 1.000 |
| FrameNet | 5 | 5 | 0 | 1.000 |
| perplexity | 4 | 4 | 0 | 1.000 |
| Moses | 3 | 3 | 0 | 1.000 |
| ROUGE | 3 | 3 | 0 | 1.000 |
| METEOR | 2 | 1 | 1 | 0.500 |
| GIZA++ | 2 | 2 | 0 | 1.000 |
| attention mechanism | 2 | 2 | 0 | 1.000 |
| NLTK | 1 | 1 | 0 | 1.000 |
| SemEval | 1 | 1 | 0 | 1.000 |
| SQuAD | 1 | 0 | 1 | 0.000 |
| GloVe | 1 | 1 | 0 | 1.000 |
| ELMo | 1 | 1 | 0 | 1.000 |
| word2vec | 1 | 1 | 0 | 1.000 |

## False Or Unclear Examples
| review_bucket | context_id | canonical_name | object_category | surface_form | matched_in | reviewer_correct | error_type | recommended_action | evidence_quote | rationale_short |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| named_object_high_confidence | ctxr_b877c7732d26928338d5 | CRF | named_object | CRFs | sentence_text | unclear | other | other |  | Could not validate model output. evidence_quote is not an exact substring of local evidence fields. Raw: {"reviewer_correct":"true","object_type_correct":"tr... |
| named_object_high_confidence | ctxr_34723d66261374f9e339 | BLEU | named_object | BLEU | context_window_neighbor | false | matched_unrelated_word | block_alias | higher BLEU scores than an equivalent system forcing the output of WSD for isolated words into the translation model | While 'BLEU' is correctly identified as a metric, the context suggests it is used as a generic reference rather than specifically as a graph object. |
| named_object_high_confidence | ctxr_7e69cf3813454546b4a4 | WordNet | named_object | WordNet | sentence_text | false | matched_unrelated_word | block_alias | We thus applied three generalization techniques to the head nouns: 1. GermaNet (GN) is the German version of WordNet (Hamp and Feldweg, 1997) . | While 'WordNet' refers correctly to the object, it does not meet the criterial context for entering the graph since the mention does not promote a specific u... |
| ambiguous_short_alias | ctxr_4fa2cff178a6aaaea7a4 | Penn Treebank | ambiguous_short_alias | PTB | sentence_text | false | insufficient_context | require_context_cue | The parser was optimised on sections 02-21 of the Wall Street Journal of the Penn Tree Bank (PTB) | While PTB is mentioned, there is insufficient context to confidently establish it as referring to the Penn Treebank dataset without additional contextual cues. |
| ambiguous_short_alias | ctxr_6afbbcf00698a5f24d61 | Penn Treebank | ambiguous_short_alias | PTB | sentence_text | false | ambiguous_short_alias | require_context_cue | PTB Wall Street Journal section | The evidence contains 'PTB' near the context of 'Wall Street Journal', but lacks strong disambiguation cues for it to enter the object graph. |
| ambiguous_short_alias | ctxr_d2f7e10dccf772790070 | Penn Treebank | ambiguous_short_alias | PTB | sentence_text | false | ambiguous_short_alias | require_context_cue | The two corpora were converted from PTB constituency trees into dependency trees using the Stanford dependency converter (de Marneffe and Manning, 2008). | PTB lacks sufficient context cues indicating it refers to the Penn Treebank dataset. |
| ambiguous_short_alias | ctxr_7b934ef7e74a56789682 | Penn Treebank | ambiguous_short_alias | PTB | sentence_text | false | ambiguous_short_alias | block_alias | a version of the PTB with function labels intact | The mention 'PTB' is too ambiguous without further context to specify 'Penn Treebank', given its other potential meanings. |
| ambiguous_short_alias | ctxr_cd65f52db26c481dcc6b | Penn Treebank | ambiguous_short_alias | PTB | context_window_neighbor | false | ambiguous_short_alias | block_alias | We made use of LIBSVM Matlab source (Chang and Lin, 2001) for SVM classification, the MateParser (Bohnet, 2010) for dependency parsing, and JAWS (Spell, 2008... | The surface form 'PTB' does not refer directly to the object 'Penn Treebank' given the lack of strong context cues. |
| ambiguous_short_alias | ctxr_ade313a487a2e6dd4583 | Penn Treebank | ambiguous_short_alias | PTB | context_window_neighbor | false | insufficient_context | require_context_cue | Based on them, many state-of-art English parser were built, including the well-known Collins parser (Collins, 2003) , Charniak parser (Charniak and Johnson, ... | The reference to 'PTB' lacks explicit context cues (e.g., treebank, corpus) to support its identification as the Penn Treebank. |
| ambiguous_short_alias | ctxr_9da88ff6c9701d288368 | Penn Treebank | ambiguous_short_alias | PTB | sentence_text | false | insufficient_context | require_context_cue | PTB sets on many points. | The mention of 'PTB' lacks sufficient context to be confidently included in the object graph without supporting evidence from disambiguating terms like treeb... |
| ambiguous_short_alias | ctxr_030e2aa31b6e2a88cfd3 | Penn Treebank | ambiguous_short_alias | PTB | context_window_neighbor | false | ambiguous_short_alias | require_context_cue | The split-mergesmooth implementation of (Petrov et al., 2006) consistently outperform various lexicalized and unlexicalized models for French (Seddah et al.,... | PTB is not sufficiently supported by local evidence cues to enter the object graph. |
| ambiguous_short_alias | ctxr_494161a5316eec1bd588 | Penn Treebank | ambiguous_short_alias | PTB | sentence_text | false | ambiguous_short_alias | require_context_cue | PTB | The mention 'PTB' is too ambiguous without clear context cues and does not directly refer to the Penn Treebank. |
| ambiguous_short_alias | ctxr_f33f15351a38203640bb | Penn Treebank | ambiguous_short_alias | PTB | context_window_neighbor | false | ambiguous_short_alias | require_context_cue | Penn TreeBank (Marcus et al., 1993) | The mention 'PTB' is an ambiguous shorthand for 'Penn Treebank' and lacks sufficient contextual cues to be confidently included in the object graph. |
| ambiguous_short_alias | ctxr_7833ec3ab05c98cf6b34 | Penn Treebank | ambiguous_short_alias | PTB | context_window_neighbor | false | ambiguous_short_alias | require_context_cue | this system does not use products of latent models and more generally their method is orthogonal to ours | The surface form 'PTB' lacks sufficient contextual cues to be confidently associated with 'Penn Treebank'. |
| ambiguous_short_alias | ctxr_d5557e0dde5af96f572d | Penn Treebank | ambiguous_short_alias | PTB | context_window_neighbor | false | insufficient_context | require_context_cue | PTB analyses. The first involves ambiguous punctuation, as al-ready noted (Maier et al., 2012) , where VPs separated by comma-punctuation are not actually co... | While 'PTB' refers to the 'Penn Treebank', the absence of strong contextual cues means it does not belong in the object graph. |
| ambiguous_short_alias | ctxr_d859659758e453381153 | Penn Treebank | ambiguous_short_alias | PTB | context_window_neighbor | false | insufficient_context | require_context_cue | PTB | The mention 'PTB' lacks sufficient context to disambiguate it as the 'Penn Treebank', and is considered a generic term without the required context cues. |
| ambiguous_short_alias | ctxr_fca466f7c46193cf633b | Penn Treebank | ambiguous_short_alias | PTB | sentence_text | false | ambiguous_short_alias | require_context_cue | PTB contain discontinuities | The mention 'PTB' can refer to the 'Penn Treebank', but lacks sufficient context cues to confidently place it in the object graph. |
| ambiguous_short_alias | ctxr_2b5201587fd1ce18b9c2 | Penn Treebank | ambiguous_short_alias | PTB | context_window_neighbor | false | ambiguous_short_alias | require_context_cue | This has been done in the Discontinuous Penn Treebank (DPTB) (Evang and Kallmeyer, 2011) . | The context lacks the necessary cues (like 'treebank' or 'dataset') to confidently link PTB to Penn Treebank, hence it doesn't meet the requirement for objec... |
| ambiguous_short_alias | ctxr_065657af5543ed78d301 | Penn Treebank | ambiguous_short_alias | PTB | sentence_text | false | ambiguous_short_alias | require_context_cue | using the PTB tagset (better than state-of-the-art) | The mention 'PTB' does not have sufficient context cues to reliably reference 'Penn Treebank'; therefore, it should not be included in the object graph witho... |
| ambiguous_short_alias | ctxr_4d629f70f30300c8a7e0 | Penn Treebank | ambiguous_short_alias | PTB | sentence_text | false | ambiguous_short_alias | require_context_cue | PTB contain discontinuities | The mention 'PTB' lacks sufficient contextual cues related to 'Penn Treebank' and appears ambiguous in this context. |
| ambiguous_short_alias | ctxr_41ca948307ad12754aee | Penn Treebank | ambiguous_short_alias | PTB | context_window_neighbor | false | insufficient_context | block_alias | the performance level, both for Charniak's parser (Charniak, 2000) and the Berke-ley parser (Petrov et al., 2006) was higher for parsing the PTB than it was ... | The mention 'PTB' does not have sufficient contextual cues to clarify its reference to the 'Penn Treebank', leading to a classification of ambiguous short al... |
| ambiguous_short_alias | ctxr_c1e543f5ce3752dd2844 | Penn Treebank | ambiguous_short_alias | PTB | context_window_neighbor | false | context_neighbor_not_relevant | require_context_cue | After the release of the Penn Treebank (PTB) (Marcus et al., 1993) and the PARSEVAL metrics (Black et al., 1991) , some new corpusbased syntactic parsing tec... | The context does not provide the necessary cues to support the use of 'PTB' directly in the object graph. |
| ambiguous_short_alias | ctxr_e5f409b1523584a4866d | Penn Treebank | ambiguous_short_alias | PTB | sentence_text | false | ambiguous_short_alias | lower_confidence | which employ hand-crafted grammars and treebank-trained disambiguators in order to determine whether a system less tuned to the PTB is more appropriate for t... | The use of 'PTB' is valid but lacks the necessary context cues (like 'treebank' or 'dataset') to support inclusion in the object graph. |
| ambiguous_short_alias | ctxr_1ebbe156b30502e2af7a | Penn Treebank | ambiguous_short_alias | PTB | sentence_text | false | ambiguous_short_alias | require_context_cue | Cahill et al. (2004) automatically construct LFG f-structures from PTB trees, a work adapted for various other languages including French (Schluter and van G... | The abbreviation PTB refers to Penn Treebank but lacks necessary context cues to support its inclusion in the object graph. |
| ambiguous_short_alias | ctxr_11d594ca118d2c064e60 | Penn Treebank | ambiguous_short_alias | PTB | context_window_neighbor | false | ambiguous_short_alias | require_context_cue | By automatically transforming the constituent structure trees annotated in PTB to other linguistic formalisms, such as dependency grammar, and combinatory ca... | The mention 'PTB' lacks sufficient context cues to support its inclusion in the object graph despite correctly referring to the 'Penn Treebank'. |

## Registry Refinement Recommendations
| recommended_action | object_id | canonical_name | surface_form | rows |
| --- | --- | --- | --- | --- |
| require_context_cue | obj_penn_treebank | Penn Treebank | PTB | 26 |
| keep_as_feature_only | obj_transformer | Transformer | transformer | 8 |
| block_alias | obj_bleu | BLEU | BLEU | 3 |
| block_alias | obj_penn_treebank | Penn Treebank | PTB | 3 |
| block_alias | obj_transformer | Transformer | transformer | 3 |
| block_alias | obj_seq2seq | seq2seq | Encoder{--}Decoder | 2 |
| block_alias | obj_wordnet | WordNet | WordNet | 2 |
| block_alias | obj_squad | SQuAD | Stanford Question Answering Dataset | 1 |
| change_object_type | obj_transformer | Transformer | transformers | 1 |
| keep_as_feature_only | obj_meteor | METEOR | METEOR | 1 |
| keep_as_feature_only | obj_transformer | Transformer | transformers | 1 |
| lower_confidence | obj_penn_treebank | Penn Treebank | PTB | 1 |
| lower_confidence | obj_transformer | Transformer | transformer | 1 |
| require_context_cue | obj_bert | BERT | BERT | 1 |
| require_context_cue | obj_seq2seq | seq2seq | Encoder{--}Decoder | 1 |

## Sample Rows
| review_bucket | context_id | canonical_name | object_category | surface_form | matched_in | confidence | allow_in_object_graph | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| named_object_high_confidence | ctxr_c3916fd64523daff6d3a | GloVe | named_object | glove | sentence_text | 0.95 | True | The models were trained using the GloVe embeddings (Pennington et al., 2014) from SBWC 10 (from now on baseline-glove) and the Medical Word Embeddings for Sp... |
| named_object_high_confidence | ctxr_6051079d4ab639d5f668 | BLEU | named_object | BLEU score | sentence_text | 0.95 | True | We would like to mention that in the literature there are efficient algorithms to find the oracle BLEU (the hypothesis with the highest attainable BLEU score... |
| named_object_high_confidence | ctxr_026ea0fa3fa4021d7843 | LSTM | named_object | LSTM | sentence_text | 0.95 | True | This suggests that the transformer architecture has the capability of implicitly modelling sequential dependencies of the output labels, unlike earlier neura... |
| named_object_high_confidence | ctxr_152cde5443e55ceed4a1 | BERT | named_object | BERT | context_window_neighbor | 0.85 | True | In favor of the former, other research has suggested that Transformer-based architectures perform syntactic operations (Raganato and Tiedemann, 2018; Hewitt ... |
| named_object_high_confidence | ctxr_564c8a17b8bc709ecb67 | Transformer | named_object | Transformer | sentence_text | 0.95 | True | Alt et al. (2019) extended Generative Pre-trained Transformer (GPT) to learn semantic and syntactic features for DSRE. |
| named_object_high_confidence | ctxr_7cacde29db89c41748f1 | NLTK | named_object | NLTK | context_window_neighbor | 0.85 | True | To incorporate exemplars into the training set, Kshirsagar et al. (2015) apply an extra layer of filtering by excluding annotationsets containing no overt fr... |
| named_object_high_confidence | ctxr_27c6dbeab7ca7522678d | ROUGE | named_object | ROUGE | sentence_text | 0.95 | True | We evaluated our approach for all datasets using ROUGE-1 (R1), ROUGE-2 (R2), and ROUGE-L (RL) (Lin, 2004) , which calculate the word-overlap between the refe... |
| named_object_high_confidence | ctxr_4c8bd6da4c7e6083f4d0 | HMM | named_object | HMM | sentence_text | 0.95 | True | We collect bidirectional (bi) refined word alignment by growing the intersection of Chinese-to-English (CE) alignments and English-to-Chinese (EC) alignments... |
| named_object_high_confidence | ctxr_fa36552f3b98ccb348ae | BLEU | named_object | BLEU score | sentence_text | 0.95 | True | We also compared our system to a setup that follows (Eisele et al., 2008) and achieve much more reliable improvements over both indomain and out-of-domain ta... |
| named_object_high_confidence | ctxr_b28f095e068c5a29e8d6 | CRF | named_object | CRF | sentence_text | 0.95 | True | In one group, term extraction is treated as any other extraction task and is usually solved as a classification task using statistical, e.g., CRF, (Zhang, 20... |
| named_object_high_confidence | ctxr_bf651e31ba1cd92e3404 | LSTM | named_object | LSTM | sentence_text | 0.95 | True | For our LSTM model, we follow a standard bidirectional LSTM architecture (Huang et al., 2015; Ma and Hovy, 2016; Lample et al., 2016) . |
| named_object_high_confidence | ctxr_afde6618f08f1abea534 | HMM | named_object | HMM | context_window_neighbor | 0.85 | True | They can be seen as extensions of the simpler IBM models 1 and 2 (Brown et al., 1993) . |
| named_object_high_confidence | ctxr_4350b96e690d41c5e2e5 | WMT | named_object | WMT | sentence_text | 0.95 | True | These texts were back-translated (Sennrich et al., 2016a; Burlot and Yvon, 2018) into French using a relatively basic neural French-English engine trained wi... |
| named_object_high_confidence | ctxr_9eb834ab29a9cb639ede | FrameNet | named_object | Framenet | sentence_text | 0.95 | True | Das et al. (2010) , for example, use heuristics to detect frame triggers and pick the appropriate frame using a classifier that only considers the frames lic... |
| named_object_high_confidence | ctxr_831068f9b15e7e487393 | CRF | named_object | Conditional Random Fields | sentence_text | 0.95 | True | Many traditional NER methods are based on statistical sequence modeling methods, such as Hidden Markov Models (HMM) and Conditional Random Fields (CRF) (Cohe... |
| named_object_high_confidence | ctxr_df381934a802683bac79 | Transformer | named_object | Transformer | sentence_text | 0.95 | True | With rapid advances in neural based NLP, word alignment has recently regained some traction (Legrand et al., 2016) and improvements of the state of the art f... |
| named_object_high_confidence | ctxr_ca61e6e7be23d802775e | ROUGE | named_object | ROUGE | sentence_text | 0.95 | True | As in Nallapati et al. (2017) and Zhou et al. (2018) , we extract ground truth extraction labels by greedily selecting sentences which maximize the relative ... |
| named_object_high_confidence | ctxr_439de1fca6c445b4ee67 | CRF | named_object | CRF | context_window_neighbor | 0.85 | True | Recently, the language model pre-training (Peters et al., 2018; Radford et al., 2018; Devlin et al., 2019) has proven to be effective for improving many NLP ... |
| named_object_high_confidence | ctxr_0b03e7c7ae55f8fa48a5 | BLEU | named_object | BLEU | sentence_text | 0.95 | True | DP-based measures and BLEU have different characteristics (Yasuda et al., 2003) . |
| named_object_high_confidence | ctxr_e385146ded5d5db94eca | Moses | named_object | Moses decoder | context_window_neighbor | 0.85 | True | Integrating in-domain and out-of-domain language models one using log-linear features of an SMT model was carried out by Koehn and Schroeder (2007) . |
