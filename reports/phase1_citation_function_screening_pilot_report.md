# Phase-1 Citation-Function Screening Pilot Report

## Inputs
- Contexts: `data/processed/analysis_ready_strong_contexts.parquet`
- Object mentions: `data/processed/object_mentions.parquet`
- Object graph candidates: `data/processed/object_graph_candidate_mentions.parquet`
- Cited-title object profiles: `data/processed/cited_title_object_profiles.parquet`
- Seed: `42`

## Outputs
- Candidate rows: `data/processed/phase1_citation_function_candidates_pilot.parquet`
- Feature rows: `data/processed/phase1_context_features_pilot.parquet`

## Core Counts
| metric                                |     value |
|:--------------------------------------|----------:|
| input_contexts_processed              | 100000    |
| configured_limit                      | 100000    |
| contexts_with_object_mentions         |  21704    |
| contexts_with_graph_candidate_objects |  17508    |
| object_mentions_input_rows            |  32301    |
| graph_candidate_input_rows            |  25907    |
| cited_title_profile_input_rows        |   7565    |
| should_send_to_llm_count              |  75959    |
| should_send_to_llm_rate               |      0.76 |

## Candidate Intent Distribution
| candidate_intent   |   contexts |
|:-------------------|-----------:|
| uses               |      46628 |
| background         |      33768 |
| critiques          |      16749 |
| compares_against   |      15131 |
| extends            |      14108 |
| applies            |      11564 |
| unclear            |      10345 |

## Primary Candidate Intent Distribution
| primary_candidate_intent   |   contexts |
|:---------------------------|-----------:|
| uses                       |      25729 |
| background                 |      17859 |
| critiques                  |      16749 |
| extends                    |      11523 |
| compares_against           |      10686 |
| unclear                    |      10345 |
| applies                    |       7109 |

## Candidate Object Type Distribution
| object_type           |   contexts |
|:----------------------|-----------:|
| unknown               |      75362 |
| model                 |       8746 |
| metric                |       7181 |
| method                |       3735 |
| dataset_or_database   |       3480 |
| software_or_tool      |       2054 |
| benchmark_or_protocol |       1884 |

## Relation Subtype Distribution
| relation_subtype    |   contexts |
|:--------------------|-----------:|
| direct_use          |      36123 |
| none                |      28415 |
| evaluate_on         |      22759 |
| critique_limitation |      16538 |
| compare_against     |      10553 |
| adapt_to_domain     |       9771 |
| improve             |       9503 |
| report_metric       |       6771 |
| replace             |        977 |
| combine_with        |        447 |
| component_use       |        108 |

## Matched Cue Counts By Group
| cue_group   |   contexts |
|:------------|-----------:|
| use         |      32279 |
| compare     |      14291 |
| extend      |      14108 |
| critique    |      16538 |
| apply       |      11564 |
| background  |      20990 |
| evaluation  |      22759 |

## Candidate Intent By Normalized Section
| normalized_section   | candidate_intent   |   contexts |
|:---------------------|:-------------------|-----------:|
| introduction         | background         |      13405 |
| introduction         | uses               |      12714 |
| unknown              | uses               |      12066 |
| related_work         | background         |      10751 |
| related_work         | uses               |       8889 |
| introduction         | critiques          |       7306 |
| unknown              | unclear            |       6817 |
| introduction         | compares_against   |       5079 |
| introduction         | extends            |       4719 |
| introduction         | applies            |       4657 |
| unknown              | background         |       4428 |
| related_work         | extends            |       3746 |
| unknown              | critiques          |       3359 |
| dataset              | uses               |       3332 |
| related_work         | critiques          |       3300 |
| unknown              | compares_against   |       3232 |
| unknown              | extends            |       2845 |
| related_work         | compares_against   |       2644 |
| related_work         | applies            |       2598 |
| unknown              | applies            |       2383 |
| experiment           | uses               |       2289 |
| method               | uses               |       1581 |
| model                | uses               |       1546 |
| evaluation           | uses               |       1128 |
| experiment           | compares_against   |        819 |
| method               | unclear            |        810 |
| model                | unclear            |        792 |
| dataset              | background         |        712 |
| conclusion           | background         |        699 |
| model                | background         |        632 |
| results              | uses               |        623 |
| experiment           | background         |        601 |
| background           | background         |        600 |
| results              | compares_against   |        596 |
| method               | background         |        581 |
| conclusion           | uses               |        571 |
| dataset              | unclear            |        568 |
| background           | uses               |        559 |
| evaluation           | background         |        489 |
| dataset              | compares_against   |        468 |
| evaluation           | compares_against   |        440 |
| method               | compares_against   |        438 |
| evaluation           | unclear            |        438 |
| experiment           | unclear            |        424 |
| model                | extends            |        410 |
| model                | compares_against   |        410 |
| dataset              | critiques          |        390 |
| dataset              | extends            |        382 |
| discussion           | critiques          |        367 |
| conclusion           | extends            |        364 |
| experiment           | extends            |        356 |
| dataset              | applies            |        341 |
| discussion           | uses               |        337 |
| method               | critiques          |        325 |
| model                | critiques          |        324 |
| method               | extends            |        318 |
| model                | applies            |        315 |
| abstract             | uses               |        308 |
| results              | background         |        298 |
| method               | applies            |        290 |
| background           | critiques          |        285 |
| conclusion           | compares_against   |        267 |
| experiment           | critiques          |        251 |
| discussion           | background         |        245 |
| evaluation           | critiques          |        238 |
| experiment           | applies            |        229 |
| system_description   | uses               |        227 |
| results              | unclear            |        223 |
| results              | extends            |        200 |
| conclusion           | critiques          |        190 |
| background           | applies            |        190 |
| evaluation           | extends            |        175 |
| background           | extends            |        175 |
| analysis             | uses               |        174 |
| background           | compares_against   |        174 |
| implementation       | uses               |        173 |
| abstract             | compares_against   |        170 |
| results              | critiques          |        149 |
| discussion           | extends            |        146 |
| conclusion           | applies            |        145 |
| discussion           | compares_against   |        143 |
| abstract             | extends            |        128 |
| system_description   | compares_against   |        126 |
| evaluation           | applies            |        123 |
| analysis             | unclear            |        111 |
| abstract             | background         |         90 |
| system_description   | background         |         86 |
| discussion           | applies            |         78 |
| analysis             | background         |         70 |
| analysis             | extends            |         70 |
| analysis             | compares_against   |         68 |
| analysis             | critiques          |         62 |
| task_definition      | uses               |         61 |
| error_analysis       | critiques          |         58 |
| analysis             | applies            |         56 |
| results              | applies            |         55 |
| system_description   | unclear            |         52 |
| abstract             | critiques          |         51 |
| error_analysis       | uses               |         50 |
| system_description   | critiques          |         49 |
| implementation       | unclear            |         44 |
| implementation       | background         |         42 |
| system_description   | applies            |         38 |
| abstract             | unclear            |         38 |
| implementation       | compares_against   |         34 |
| task_definition      | critiques          |         32 |
| task_definition      | unclear            |         28 |
| system_description   | extends            |         27 |
| abstract             | applies            |         27 |
| error_analysis       | extends            |         24 |
| error_analysis       | background         |         21 |
| error_analysis       | compares_against   |         19 |
| task_definition      | background         |         18 |
| implementation       | applies            |         17 |
| implementation       | extends            |         17 |
| task_definition      | applies            |         13 |
| implementation       | critiques          |         13 |
| error_analysis       | applies            |          9 |
| task_definition      | extends            |          6 |
| task_definition      | compares_against   |          4 |

## Candidate Intent By Object Type
| candidate_intent   | object_type           |   contexts |
|:-------------------|:----------------------|-----------:|
| uses               | unknown               |      33139 |
| background         | unknown               |      26541 |
| critiques          | unknown               |      13136 |
| extends            | unknown               |       9994 |
| applies            | unknown               |       8968 |
| compares_against   | unknown               |       8725 |
| unclear            | unknown               |       8042 |
| uses               | model                 |       4206 |
| uses               | metric                |       3952 |
| background         | model                 |       2940 |
| compares_against   | metric                |       2830 |
| uses               | dataset_or_database   |       2500 |
| compares_against   | model                 |       2313 |
| background         | metric                |       1994 |
| uses               | method                |       1809 |
| uses               | software_or_tool      |       1546 |
| extends            | metric                |       1505 |
| extends            | model                 |       1272 |
| critiques          | metric                |       1254 |
| background         | method                |       1183 |
| critiques          | model                 |       1120 |
| uses               | benchmark_or_protocol |       1051 |
| applies            | model                 |        979 |
| background         | dataset_or_database   |        922 |
| unclear            | model                 |        872 |
| compares_against   | method                |        833 |
| extends            | method                |        702 |
| extends            | dataset_or_database   |        682 |
| compares_against   | dataset_or_database   |        656 |
| unclear            | metric                |        646 |
| applies            | metric                |        608 |
| background         | benchmark_or_protocol |        606 |
| critiques          | method                |        592 |
| applies            | method                |        457 |
| compares_against   | benchmark_or_protocol |        435 |
| critiques          | dataset_or_database   |        435 |
| unclear            | method                |        433 |
| compares_against   | software_or_tool      |        394 |
| applies            | dataset_or_database   |        368 |
| background         | software_or_tool      |        338 |
| critiques          | software_or_tool      |        233 |
| critiques          | benchmark_or_protocol |        219 |
| extends            | software_or_tool      |        214 |
| unclear            | dataset_or_database   |        211 |
| unclear            | software_or_tool      |        198 |
| applies            | software_or_tool      |        197 |
| applies            | benchmark_or_protocol |        189 |
| unclear            | benchmark_or_protocol |        170 |
| extends            | benchmark_or_protocol |        159 |

## Top Object Names By Candidate Intent
| candidate_intent   | object_name         |   contexts |
|:-------------------|:--------------------|-----------:|
| compares_against   | accuracy            |       1539 |
| uses               | accuracy            |       1518 |
| uses               | BLEU                |       1472 |
| uses               | BERT                |       1109 |
| uses               | Penn Treebank       |       1017 |
| uses               | CRF                 |        939 |
| background         | accuracy            |        930 |
| uses               | LSTM                |        923 |
| extends            | accuracy            |        884 |
| uses               | Transformer         |        788 |
| uses               | Moses               |        788 |
| uses               | WordNet             |        711 |
| compares_against   | F1                  |        709 |
| uses               | F1                  |        694 |
| compares_against   | BERT                |        666 |
| background         | BLEU                |        664 |
| uses               | GIZA++              |        659 |
| background         | seq2seq             |        649 |
| background         | LSTM                |        638 |
| uses               | seq2seq             |        631 |
| critiques          | accuracy            |        607 |
| background         | Transformer         |        563 |
| compares_against   | BLEU                |        538 |
| background         | BERT                |        519 |
| background         | CRF                 |        510 |
| compares_against   | seq2seq             |        499 |
| compares_against   | Transformer         |        498 |
| uses               | HMM                 |        459 |
| critiques          | BLEU                |        456 |
| compares_against   | LSTM                |        444 |
| background         | WordNet             |        438 |
| uses               | SemEval             |        404 |
| compares_against   | CRF                 |        379 |
| extends            | BLEU                |        377 |
| critiques          | seq2seq             |        373 |
| extends            | BERT                |        342 |
| uses               | GloVe               |        337 |
| applies            | seq2seq             |        336 |
| unclear            | BLEU                |        331 |
| background         | SemEval             |        324 |
| extends            | seq2seq             |        305 |
| background         | attention mechanism |        294 |
| uses               | SQuAD               |        285 |
| compares_against   | Moses               |        280 |
| background         | F1                  |        279 |
| extends            | Penn Treebank       |        277 |
| applies            | accuracy            |        276 |
| compares_against   | Penn Treebank       |        273 |
| uses               | METEOR              |        267 |
| unclear            | BERT                |        267 |
| unclear            | LSTM                |        259 |
| uses               | word2vec            |        259 |
| extends            | CRF                 |        257 |
| uses               | ROUGE               |        256 |
| background         | HMM                 |        250 |
| extends            | LSTM                |        249 |
| background         | Penn Treebank       |        248 |
| uses               | attention mechanism |        246 |
| critiques          | CRF                 |        241 |
| uses               | WMT                 |        241 |
| critiques          | BERT                |        219 |
| extends            | WordNet             |        209 |
| applies            | CRF                 |        200 |
| uses               | ELMo                |        199 |
| extends            | Transformer         |        198 |
| unclear            | CRF                 |        196 |
| background         | GIZA++              |        190 |
| compares_against   | attention mechanism |        186 |
| extends            | attention mechanism |        184 |
| uses               | FrameNet            |        184 |
| applies            | BLEU                |        183 |
| compares_against   | HMM                 |        181 |
| critiques          | WordNet             |        178 |
| background         | Moses               |        171 |
| extends            | F1                  |        165 |
| applies            | BERT                |        163 |
| compares_against   | GIZA++              |        161 |
| critiques          | HMM                 |        159 |
| uses               | perplexity          |        159 |
| unclear            | Transformer         |        157 |
| unclear            | accuracy            |        157 |
| extends            | HMM                 |        155 |
| uses               | PropBank            |        155 |
| compares_against   | SemEval             |        154 |
| critiques          | LSTM                |        146 |
| applies            | Transformer         |        146 |
| critiques          | Transformer         |        140 |
| applies            | LSTM                |        139 |
| uses               | OntoNotes           |        138 |
| applies            | WordNet             |        136 |
| compares_against   | WordNet             |        130 |
| applies            | F1                  |        129 |
| uses               | SNLI                |        129 |
| critiques          | attention mechanism |        127 |
| compares_against   | perplexity          |        125 |
| applies            | attention mechanism |        125 |
| critiques          | Moses               |        125 |
| applies            | GIZA++              |        125 |
| unclear            | F1                  |        123 |
| critiques          | F1                  |        123 |

## Generic Metric Contexts By Candidate Intent
| candidate_intent   |   contexts |
|:-------------------|-----------:|
| compares_against   |       2256 |
| uses               |       2255 |
| background         |       1226 |
| extends            |       1083 |
| critiques          |        746 |
| applies            |        386 |
| unclear            |        281 |

## Example Uses
| context_id                | normalized_section   | primary_candidate_intent   | candidate_intents               | candidate_relation_subtypes                                  |   confidence | should_send_to_llm   | object_names   | generic_metric_names   | evidence_span   | matched_rules                                                                  | sentence_text                                                                                                                                                                        |
|:--------------------------|:---------------------|:---------------------------|:--------------------------------|:-------------------------------------------------------------|-------------:|:---------------------|:---------------|:-----------------------|:----------------|:-------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ctxr_4771edcc3e42c8bb07c7 | introduction         | uses                       | uses;background                 | direct_use                                                   |         0.65 | True                 |                |                        | described       | use_cue;background_cue                                                         | In NLP, Elsner and Charniak (2010) described the task of thread disentanglement as "the clustering task of dividing a transcript into a set of distinct conversations," in which ... |
| ctxr_d06d69e8921c81b378ac | introduction         | uses                       | uses                            | evaluate_on                                                  |         0.65 | True                 |                |                        | Corpus          | evaluation_cue                                                                 | Carenini et al. (2008) annotated 39 email "conversations" from the Enron Email Corpus for email summariation.                                                                        |
| ctxr_68d4edb5f20b826f715b | introduction         | uses                       | uses                            | evaluate_on                                                  |         0.65 | True                 |                |                        | corpus          | evaluation_cue                                                                 | Wan and McKeown (2004) used a privatelyavailable corpus of 300 threads for summary generation.                                                                                       |
| ctxr_b166bf8511a77353542f | introduction         | uses                       | uses                            | evaluate_on                                                  |         0.65 | True                 |                |                        | corpus          | evaluation_cue                                                                 | Rambow et al. (2004) used a privatelyavailable corpus of 96 email threads for thread summarization.                                                                                  |
| ctxr_6739ef248e0241672c80 | dataset              | uses                       | uses                            | evaluate_on                                                  |         0.65 | True                 |                |                        | corpus          | evaluation_cue                                                                 | Wan and McKeown (2004) reconstructed threads by header Message-ID information.                                                                                                       |
| ctxr_4ba57d063d3c71fa78df | dataset              | uses                       | uses                            | evaluate_on                                                  |         0.65 | True                 |                |                        | corpus          | evaluation_cue                                                                 | Rambow et al. (2004) used a privately-available corpus of 96 email threads, but did not specify how they determined the threads.                                                     |
| ctxr_d573e73d4a69363cdfc0 | results              | critiques                  | uses;compares_against;critiques | direct_use;compare_against;critique_limitation;report_metric |         0.85 | True                 | accuracy       | accuracy               | using           | use_cue;compare_cue;critique_cue;generic_metric_with_compare_or_evaluation_cue | Elsner and Charniak (2011) use coherence models to disentangle chat, using some features (entity grid, topical entity grid) which correspond to the information in our content fe... |
| ctxr_f6863fcab52657a5c16e | related_work         | compares_against           | uses;compares_against           | direct_use;report_metric                                     |         0.9  | True                 | SemEval        |                        | based on        | use_cue;compare_cue                                                            | In (Tratz and Hovy, 2010) the authors developed a system based on the Maximum Entropy classifier, able to detect 10 bidirectional semantic relations Achieved F-measures depended... |
| ctxr_71d08900475d9c8505ab | related_work         | compares_against           | uses;compares_against           | direct_use;report_metric                                     |         0.65 | True                 |                |                        | based on        | use_cue;compare_cue                                                            | The same set of semantic relations was used in (Rink and Harabagiu, 2010) .                                                                                                          |
| ctxr_b1bfb1536bcb5cbbf8b5 | related_work         | uses                       | uses                            | direct_use                                                   |         0.65 | True                 |                |                        | using           | use_cue                                                                        | Authors in (Tymoshenko and Giuliano, 2010 ) used shallow syntactic parsing and semantic information from ResearchCyc (Lenat, 1995) in the same task of recognizing semantic relat... |

## Example Compares Against
| context_id                | normalized_section   | primary_candidate_intent   | candidate_intents                | candidate_relation_subtypes                                  |   confidence | should_send_to_llm   | object_names    | generic_metric_names   | evidence_span   | matched_rules                                                                       | sentence_text                                                                                                                                                                        |
|:--------------------------|:---------------------|:---------------------------|:---------------------------------|:-------------------------------------------------------------|-------------:|:---------------------|:----------------|:-----------------------|:----------------|:------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ctxr_8361b89d504826d53df9 | unknown              | compares_against           | compares_against                 | compare_against                                              |         0.65 | True                 |                 |                        | compared with   | compare_cue                                                                         | 1999 ) uses pairs of words occurring in the same order for the two emails; Token Pair Distance (Hatzivassiloglou et al., 1999) measures the distance between pairs of words.         |
| ctxr_d573e73d4a69363cdfc0 | results              | critiques                  | uses;compares_against;critiques  | direct_use;compare_against;critique_limitation;report_metric |         0.85 | True                 | accuracy        | accuracy               | using           | use_cue;compare_cue;critique_cue;generic_metric_with_compare_or_evaluation_cue      | Elsner and Charniak (2011) use coherence models to disentangle chat, using some features (entity grid, topical entity grid) which correspond to the information in our content fe... |
| ctxr_f6863fcab52657a5c16e | related_work         | compares_against           | uses;compares_against            | direct_use;report_metric                                     |         0.9  | True                 | SemEval         |                        | based on        | use_cue;compare_cue                                                                 | In (Tratz and Hovy, 2010) the authors developed a system based on the Maximum Entropy classifier, able to detect 10 bidirectional semantic relations Achieved F-measures depended... |
| ctxr_71d08900475d9c8505ab | related_work         | compares_against           | uses;compares_against            | direct_use;report_metric                                     |         0.65 | True                 |                 |                        | based on        | use_cue;compare_cue                                                                 | The same set of semantic relations was used in (Rink and Harabagiu, 2010) .                                                                                                          |
| ctxr_f8a4c2e6aa2834642a71 | related_work         | compares_against           | uses;compares_against            | report_metric;evaluate_on                                    |         0.65 | True                 |                 |                        | corpora         | evaluation_cue;compare_cue                                                          | In (Hearst, 1992) authors used set of manually written rules for identification of hyperonymy relations. (Ben Abacha and Zweigenbaum, 2011) used linguistic patterns (built semi-... |
| ctxr_5d4459ab2a2de3c5c83b | evaluation           | critiques                  | compares_against;critiques       | compare_against;critique_limitation                          |         0.65 | True                 |                 |                        | compared to     | compare_cue;critique_cue                                                            | Despite of its performance, LIHLA has some advantages when compared to other lexical alignment methods found in the literature, such as: it does not need to be trained for a new... |
| ctxr_794ff11af106441610a2 | model                | compares_against           | uses;background;compares_against | direct_use;evaluate_on;report_metric                         |         0.9  | True                 | perplexity;BLEU | perplexity             | we use          | use_cue;evaluation_cue;background_cue;generic_metric_with_compare_or_evaluation_cue | Since the space of different combinations is too large to be searched exhaustively, we use a guided search procedure based on Genetic Algorithms (Duh and Kirchhoff, 2004) , whic... |
| ctxr_b4edfcd618c4edc4d4dc | introduction         | extends                    | uses;extends;compares_against    | improve;evaluate_on;report_metric                            |         0.85 | True                 | accuracy        | accuracy               | Treebank        | evaluation_cue;extend_cue;generic_metric_with_compare_or_evaluation_cue             | We continue our work (Khan et al., 2013) on dependency parsing web data from the English Web Treebank (Bies et al., 2012) .                                                          |
| ctxr_a7ac70660d93318c89cc | unknown              | compares_against           | uses;compares_against            | direct_use;compare_against                                   |         0.65 | True                 |                 |                        | We use          | use_cue;compare_cue                                                                 | We use TnT (Brants, 2000) , a Markov model POS tagger using a trigram model.                                                                                                         |
| ctxr_c223321394c5bbc2bcec | unknown              | compares_against           | uses;compares_against            | evaluate_on;report_metric                                    |         0.85 | True                 | accuracy        | accuracy               | tested on       | evaluation_cue;generic_metric_with_compare_or_evaluation_cue                        | This corroborates findings by Brants (2000) .                                                                                                                                        |

## Example Extends
| context_id                | normalized_section   | primary_candidate_intent   | candidate_intents             | candidate_relation_subtypes       |   confidence | should_send_to_llm   | object_names   | generic_metric_names   | evidence_span   | matched_rules                                                           | sentence_text                                                                                                                                                                        |
|:--------------------------|:---------------------|:---------------------------|:------------------------------|:----------------------------------|-------------:|:---------------------|:---------------|:-----------------------|:----------------|:------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ctxr_b4edfcd618c4edc4d4dc | introduction         | extends                    | uses;extends;compares_against | improve;evaluate_on;report_metric |         0.85 | True                 | accuracy       | accuracy               | Treebank        | evaluation_cue;extend_cue;generic_metric_with_compare_or_evaluation_cue | We continue our work (Khan et al., 2013) on dependency parsing web data from the English Web Treebank (Bies et al., 2012) .                                                          |
| ctxr_ee35106f6e6c4c292b4f | related_work         | extends                    | extends                       | improve                           |         0.65 | True                 |                |                        | improving       | extend_cue                                                              | There have been many techniques employed for improving parsing models, including normalizing the potentially ill-formed text (Foster, 2010; Gadde et al., 2011; Øvrelid and Skjae... |
| ctxr_620e87f9bfa931e21dfa | related_work         | extends                    | extends                       | improve                           |         0.65 | True                 |                |                        | improving       | extend_cue                                                              | There have been many techniques employed for improving parsing models, including normalizing the potentially ill-formed text (Foster, 2010; Gadde et al., 2011; Øvrelid and Skjae... |
| ctxr_e56c5cf546c8848cfdce | related_work         | extends                    | extends                       | improve                           |         0.65 | True                 |                |                        | improving       | extend_cue                                                              | There have been many techniques employed for improving parsing models, including normalizing the potentially ill-formed text (Foster, 2010; Gadde et al., 2011; Øvrelid and Skjae... |
| ctxr_ba6efe95fca9618d0d19 | related_work         | extends                    | extends                       | improve                           |         0.65 | True                 |                |                        | improving       | extend_cue                                                              | There have been many techniques employed for improving parsing models, including normalizing the potentially ill-formed text (Foster, 2010; Gadde et al., 2011; Øvrelid and Skjae... |
| ctxr_122e4920b496f1fab008 | related_work         | extends                    | extends                       | improve                           |         0.65 | True                 |                |                        | improving       | extend_cue                                                              | There have been many techniques employed for improving parsing models, including normalizing the potentially ill-formed text (Foster, 2010; Gadde et al., 2011; Øvrelid and Skjae... |
| ctxr_ce34d84f3750233884ae | related_work         | extends                    | extends                       | improve                           |         0.65 | True                 |                |                        | improving       | extend_cue                                                              | There have been many techniques employed for improving parsing models, including normalizing the potentially ill-formed text (Foster, 2010; Gadde et al., 2011; Øvrelid and Skjae... |
| ctxr_d8dcafcf47fd73f2bcc3 | related_work         | extends                    | extends                       | improve                           |         0.65 | True                 |                |                        | improve         | extend_cue                                                              | In general, identifying sentences which are similar to a particular domain is a concept familiar in active learning (e.g., Mirroshandel and Nasr, 2011; Sassano and Kurohashi, 20... |
| ctxr_3076972defbd316cf48c | related_work         | extends                    | extends                       | improve                           |         0.65 | True                 |                |                        | improve         | extend_cue                                                              | In general, identifying sentences which are similar to a particular domain is a concept familiar in active learning (e.g., Mirroshandel and Nasr, 2011; Sassano and Kurohashi, 20... |
| ctxr_eb3468813df46a070631 | related_work         | extends                    | extends                       | improve                           |         0.65 | True                 |                |                        | improve         | extend_cue                                                              | In general, identifying sentences which are similar to a particular domain is a concept familiar in active learning (e.g., Mirroshandel and Nasr, 2011; Sassano and Kurohashi, 20... |

## Example Critiques
| context_id                | normalized_section   | primary_candidate_intent   | candidate_intents                       | candidate_relation_subtypes                                        |   confidence | should_send_to_llm   | object_names   | generic_metric_names   | evidence_span   | matched_rules                                                                  | sentence_text                                                                                                                                                                        |
|:--------------------------|:---------------------|:---------------------------|:----------------------------------------|:-------------------------------------------------------------------|-------------:|:---------------------|:---------------|:-----------------------|:----------------|:-------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ctxr_d573e73d4a69363cdfc0 | results              | critiques                  | uses;compares_against;critiques         | direct_use;compare_against;critique_limitation;report_metric       |         0.85 | True                 | accuracy       | accuracy               | using           | use_cue;compare_cue;critique_cue;generic_metric_with_compare_or_evaluation_cue | Elsner and Charniak (2011) use coherence models to disentangle chat, using some features (entity grid, topical entity grid) which correspond to the information in our content fe... |
| ctxr_fde2b4fe687323ff4bd3 | experiment           | critiques                  | critiques                               | critique_limitation                                                |         0.85 | True                 | F1             | F1                     | error           | critique_cue                                                                   | The evaluation was run with respect to precision, recall, F -measure, and alignment error rate (AER) considering sure and probable alignments but not NULL ones (Mihalcea and Ped... |
| ctxr_5d4459ab2a2de3c5c83b | evaluation           | critiques                  | compares_against;critiques              | compare_against;critique_limitation                                |         0.65 | True                 |                |                        | compared to     | compare_cue;critique_cue                                                       | Despite of its performance, LIHLA has some advantages when compared to other lexical alignment methods found in the literature, such as: it does not need to be trained for a new... |
| ctxr_80a719941f90174ecb9f | unknown              | critiques                  | uses;compares_against;extends;critiques | direct_use;compare_against;improve;critique_limitation;evaluate_on |         0.65 | True                 |                |                        | However         | use_cue;evaluation_cue;compare_cue;extend_cue;critique_cue                     | However, the field is moving fast, and a number of steps help to improve upon the provided baseline setup, e.g., larger language models trained on general text (up to a billion ... |
| ctxr_1fd3c995f1b87a28d097 | unknown              | critiques                  | uses;compares_against;extends;critiques | direct_use;compare_against;improve;critique_limitation;evaluate_on |         0.65 | True                 |                |                        | However         | use_cue;evaluation_cue;compare_cue;extend_cue;critique_cue                     | However, the field is moving fast, and a number of steps help to improve upon the provided baseline setup, e.g., larger language models trained on general text (up to a billion ... |
| ctxr_267a14cdce7b61e229de | unknown              | critiques                  | uses;compares_against;extends;critiques | direct_use;compare_against;improve;critique_limitation;evaluate_on |         0.65 | True                 |                |                        | However         | use_cue;evaluation_cue;compare_cue;extend_cue;critique_cue                     | However, the field is moving fast, and a number of steps help to improve upon the provided baseline setup, e.g., larger language models trained on general text (up to a billion ... |
| ctxr_8e6ebdce8f00845e7578 | introduction         | critiques                  | uses;critiques                          | critique_limitation;evaluate_on                                    |         0.65 | True                 |                |                        | does not        | evaluation_cue;critique_cue                                                    | Vecchi et al. (2011) have focused on unattested adjective-noun (AN) combinations and noted that if a combination does not occur in a corpus, it may be due to various reasons inc... |
| ctxr_e26629ae935ada16333a | unknown              | critiques                  | critiques                               | critique_limitation                                                |         0.65 | True                 |                |                        | error           | critique_cue                                                                   | Research on error detection has mostly been concerned with function words, such as determiners and prepositions (Leacock et al., 2010; Dale et al., 2012) .                          |
| ctxr_b603a1e2ca89b7bbae13 | unknown              | critiques                  | critiques                               | critique_limitation                                                |         0.65 | True                 |                |                        | error           | critique_cue                                                                   | Research on error detection has mostly been concerned with function words, such as determiners and prepositions (Leacock et al., 2010; Dale et al., 2012) .                          |
| ctxr_57efabdf07b07f291edc | unknown              | critiques                  | critiques;background                    | critique_limitation                                                |         0.65 | True                 |                |                        | Previous work   | critique_cue;background_cue                                                    | Previous work has either focused on correction alone assuming that errors are already detected (Liu et al., 2009; Dahlmeier and Ng, 2011) , or has reformulated the task as writi... |

## Example Applies
| context_id                | normalized_section   | primary_candidate_intent   | candidate_intents   | candidate_relation_subtypes   |   confidence | should_send_to_llm   | object_names   | generic_metric_names   | evidence_span   | matched_rules        | sentence_text                                                                                                                                                                        |
|:--------------------------|:---------------------|:---------------------------|:--------------------|:------------------------------|-------------:|:---------------------|:---------------|:-----------------------|:----------------|:---------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ctxr_9ab7ad32be76baef24a4 | introduction         | applies                    | applies             | adapt_to_domain               |         0.65 | True                 |                |                        | applications    | apply_cue            | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-based machine translation (EBMT) (Somers, ... |
| ctxr_008f302607deda562c24 | introduction         | applies                    | applies             | adapt_to_domain               |         0.65 | True                 |                |                        | applications    | apply_cue            | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-based machine translation (EBMT) (Somers, ... |
| ctxr_373b75e6049f7bde6cca | introduction         | applies                    | applies             | adapt_to_domain               |         0.65 | True                 |                |                        | applications    | apply_cue            | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-based machine translation (EBMT) (Somers, ... |
| ctxr_18b9cd4865ae3fef4d3f | introduction         | applies                    | applies             | adapt_to_domain               |         0.65 | True                 |                |                        | applications    | apply_cue            | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-based machine translation (EBMT) (Somers, ... |
| ctxr_7d7d31957a351c96c69d | introduction         | applies                    | applies             | adapt_to_domain               |         0.65 | True                 |                |                        | applications    | apply_cue            | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-based machine translation (EBMT) (Somers, ... |
| ctxr_8fb909e0fd3aae1d73e8 | introduction         | applies                    | applies             | adapt_to_domain               |         0.65 | True                 |                |                        | applications    | apply_cue            | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-based machine translation (EBMT) (Somers, ... |
| ctxr_4bb1b170fe1966db7825 | introduction         | applies                    | applies             | adapt_to_domain               |         0.65 | True                 |                |                        | applications    | apply_cue            | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-based machine translation (EBMT) (Somers, ... |
| ctxr_f657889e88c427521c67 | introduction         | applies                    | applies             | adapt_to_domain               |         0.65 | True                 |                |                        | applications    | apply_cue            | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-based machine translation (EBMT) (Somers, ... |
| ctxr_e8da62e0b0c0cead8f84 | introduction         | applies                    | applies             | adapt_to_domain               |         0.65 | True                 |                |                        | applications    | apply_cue            | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-based machine translation (EBMT) (Somers, ... |
| ctxr_2c7c0df00dc4b5946339 | abstract             | extends                    | extends;applies     | improve;adapt_to_domain       |         0.65 | True                 |                |                        | applied to      | extend_cue;apply_cue | Vecchi et al. (2011) have shown that some compositional models, including the additive and multiplicative models of Mitchell and Lapata (2008; 2010) and the linear map-based mod... |

## Example Background
| context_id                | normalized_section   | primary_candidate_intent   | candidate_intents                | candidate_relation_subtypes          |   confidence | should_send_to_llm   | object_names    | generic_metric_names   | evidence_span   | matched_rules                                                                       | sentence_text                                                                                                                                                                        |
|:--------------------------|:---------------------|:---------------------------|:---------------------------------|:-------------------------------------|-------------:|:---------------------|:----------------|:-----------------------|:----------------|:------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ctxr_4771edcc3e42c8bb07c7 | introduction         | uses                       | uses;background                  | direct_use                           |         0.65 | True                 |                 |                        | described       | use_cue;background_cue                                                              | In NLP, Elsner and Charniak (2010) described the task of thread disentanglement as "the clustering task of dividing a transcript into a set of distinct conversations," in which ... |
| ctxr_fc94564ed0054ac2126f | introduction         | background                 | background                       | none                                 |         0.35 | False                |                 |                        |                 | weak_section_prior:introduction                                                     | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki et al., 2003) , and emails with headers... |
| ctxr_044c96a8f9c2342b58ff | related_work         | background                 | background                       | none                                 |         0.35 | False                |                 |                        |                 | weak_section_prior:related_work                                                     | In (Rosario and Hearst, 2001 ) authors used neural networks to determine 20 semantic relationssimilarily to (Nastase et al., 2006) -between a head and a modifier of noun phrase.    |
| ctxr_57f21305fc2f8b29fb6c | introduction         | uses                       | uses;background                  | direct_use                           |         0.65 | True                 |                 |                        | Following       | use_cue;background_cue                                                              | Following the same idea of many recently proposed approaches on lexical alignment (e.g., Wu and Wang (2004) and Ayan et al. (2004) ), the method described in this paper, LIHLA (... |
| ctxr_fa4d5bdd61b0b1a46bc4 | introduction         | uses                       | uses;background                  | direct_use                           |         0.65 | True                 |                 |                        | Following       | use_cue;background_cue                                                              | Following the same idea of many recently proposed approaches on lexical alignment (e.g., Wu and Wang (2004) and Ayan et al. (2004) ), the method described in this paper, LIHLA (... |
| ctxr_794ff11af106441610a2 | model                | compares_against           | uses;background;compares_against | direct_use;evaluate_on;report_metric |         0.9  | True                 | perplexity;BLEU | perplexity             | we use          | use_cue;evaluation_cue;background_cue;generic_metric_with_compare_or_evaluation_cue | Since the space of different combinations is too large to be searched exhaustively, we use a guided search procedure based on Genetic Algorithms (Duh and Kirchhoff, 2004) , whic... |
| ctxr_6ec7b60115b4d5e6dcf1 | introduction         | background                 | background                       | none                                 |         0.35 | False                |                 |                        |                 | weak_section_prior:introduction                                                     | To perform tasks such as sentiment analysis (Nakagawa et al., 2010) or information extraction (McClosky et al., 2011) , it helps to partof-speech (POS) tag and parse the data, a... |
| ctxr_9b7a73a22bca0542f3cf | introduction         | background                 | background                       | none                                 |         0.35 | False                |                 |                        |                 | weak_section_prior:introduction                                                     | To perform tasks such as sentiment analysis (Nakagawa et al., 2010) or information extraction (McClosky et al., 2011) , it helps to partof-speech (POS) tag and parse the data, a... |
| ctxr_150b3e5d87bf69e7aeff | dataset              | background                 | background                       | none                                 |         0.55 | False                |                 |                        | previous work   | background_cue                                                                      | Note that our data sets are different from the ones in Khan et al. (2013) since in the previous work we had removed sentences with POS labels AFX and GW.                            |
| ctxr_1e11c4efff7667aaac0f | unknown              | uses                       | uses;background                  | direct_use;evaluate_on               |         0.65 | True                 |                 |                        | previous work   | use_cue;evaluation_cue;background_cue                                               | In our previous work (Khan et al., 2013) , we showed that we obtain the best results when we use a balanced training corpus with the same number of sentences from the EWT and th... |

## Multiple Candidate Intent Examples
| context_id                | normalized_section   | primary_candidate_intent   | candidate_intents                | candidate_relation_subtypes                                  |   confidence | should_send_to_llm   | object_names    | generic_metric_names   | evidence_span   | matched_rules                                                                       | sentence_text                                                                                                                                                                        |
|:--------------------------|:---------------------|:---------------------------|:---------------------------------|:-------------------------------------------------------------|-------------:|:---------------------|:----------------|:-----------------------|:----------------|:------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ctxr_4771edcc3e42c8bb07c7 | introduction         | uses                       | uses;background                  | direct_use                                                   |         0.65 | True                 |                 |                        | described       | use_cue;background_cue                                                              | In NLP, Elsner and Charniak (2010) described the task of thread disentanglement as "the clustering task of dividing a transcript into a set of distinct conversations," in which ... |
| ctxr_d573e73d4a69363cdfc0 | results              | critiques                  | uses;compares_against;critiques  | direct_use;compare_against;critique_limitation;report_metric |         0.85 | True                 | accuracy        | accuracy               | using           | use_cue;compare_cue;critique_cue;generic_metric_with_compare_or_evaluation_cue      | Elsner and Charniak (2011) use coherence models to disentangle chat, using some features (entity grid, topical entity grid) which correspond to the information in our content fe... |
| ctxr_f6863fcab52657a5c16e | related_work         | compares_against           | uses;compares_against            | direct_use;report_metric                                     |         0.9  | True                 | SemEval         |                        | based on        | use_cue;compare_cue                                                                 | In (Tratz and Hovy, 2010) the authors developed a system based on the Maximum Entropy classifier, able to detect 10 bidirectional semantic relations Achieved F-measures depended... |
| ctxr_71d08900475d9c8505ab | related_work         | compares_against           | uses;compares_against            | direct_use;report_metric                                     |         0.65 | True                 |                 |                        | based on        | use_cue;compare_cue                                                                 | The same set of semantic relations was used in (Rink and Harabagiu, 2010) .                                                                                                          |
| ctxr_f8a4c2e6aa2834642a71 | related_work         | compares_against           | uses;compares_against            | report_metric;evaluate_on                                    |         0.65 | True                 |                 |                        | corpora         | evaluation_cue;compare_cue                                                          | In (Hearst, 1992) authors used set of manually written rules for identification of hyperonymy relations. (Ben Abacha and Zweigenbaum, 2011) used linguistic patterns (built semi-... |
| ctxr_57f21305fc2f8b29fb6c | introduction         | uses                       | uses;background                  | direct_use                                                   |         0.65 | True                 |                 |                        | Following       | use_cue;background_cue                                                              | Following the same idea of many recently proposed approaches on lexical alignment (e.g., Wu and Wang (2004) and Ayan et al. (2004) ), the method described in this paper, LIHLA (... |
| ctxr_fa4d5bdd61b0b1a46bc4 | introduction         | uses                       | uses;background                  | direct_use                                                   |         0.65 | True                 |                 |                        | Following       | use_cue;background_cue                                                              | Following the same idea of many recently proposed approaches on lexical alignment (e.g., Wu and Wang (2004) and Ayan et al. (2004) ), the method described in this paper, LIHLA (... |
| ctxr_5d4459ab2a2de3c5c83b | evaluation           | critiques                  | compares_against;critiques       | compare_against;critique_limitation                          |         0.65 | True                 |                 |                        | compared to     | compare_cue;critique_cue                                                            | Despite of its performance, LIHLA has some advantages when compared to other lexical alignment methods found in the literature, such as: it does not need to be trained for a new... |
| ctxr_794ff11af106441610a2 | model                | compares_against           | uses;background;compares_against | direct_use;evaluate_on;report_metric                         |         0.9  | True                 | perplexity;BLEU | perplexity             | we use          | use_cue;evaluation_cue;background_cue;generic_metric_with_compare_or_evaluation_cue | Since the space of different combinations is too large to be searched exhaustively, we use a guided search procedure based on Genetic Algorithms (Duh and Kirchhoff, 2004) , whic... |
| ctxr_b4edfcd618c4edc4d4dc | introduction         | extends                    | uses;extends;compares_against    | improve;evaluate_on;report_metric                            |         0.85 | True                 | accuracy        | accuracy               | Treebank        | evaluation_cue;extend_cue;generic_metric_with_compare_or_evaluation_cue             | We continue our work (Khan et al., 2013) on dependency parsing web data from the English Web Treebank (Bies et al., 2012) .                                                          |

## Object Mention But Background Intent Examples
| context_id                | normalized_section   | primary_candidate_intent   | candidate_intents   | candidate_relation_subtypes   |   confidence | should_send_to_llm   | object_names     | generic_metric_names   | evidence_span   | matched_rules                   | sentence_text                                                                                                                                                                        |
|:--------------------------|:---------------------|:---------------------------|:--------------------|:------------------------------|-------------:|:---------------------|:-----------------|:-----------------------|:----------------|:--------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ctxr_fc364de7c4a52b630606 | evaluation           | background                 | background          | none                          |         0.55 | True                 | ROUGE            |                        | has been shown  | background_cue                  | We computed three ROUGE measures for each summary, namely ROUGE-1 (unigram based), ROUGE-2 (bigram based) and (Lin and Hovy, 2003) .                                                 |
| ctxr_11a201fb38db6ec2b675 | evaluation           | background                 | background          | none                          |         0.55 | True                 | ROUGE            |                        | has been shown  | background_cue                  | Among them, ROUGE-1 has been shown to agree most with human judgments (Lin and Hovy, 2003) .                                                                                         |
| ctxr_e29d4de098ff144543d9 | related_work         | background                 | background          | none                          |         0.35 | True                 | LSTM             |                        |                 | weak_section_prior:related_work | The dependency path is convenient, but He et al. (2017) revealed that higher accuracies on neural-network-based SRL models could be obtained if correct parsed information is ava... |
| ctxr_3bb54eb9ce1ea3a10314 | unknown              | background                 | background          | none                          |         0.55 | True                 | PropBank         |                        | proposed        | background_cue                  | Several different systems of semantic roles are proposed in previous studies (Fillmore, 1968; Palmer et al., 2010; Loper et al., 2007; Baker et al., 1998) .                         |
| ctxr_86b64fa23a8373fd802f | unknown              | background                 | background          | none                          |         0.55 | True                 | PropBank         |                        | proposed        | background_cue                  | Several different systems of semantic roles are proposed in previous studies (Fillmore, 1968; Palmer et al., 2010; Loper et al., 2007; Baker et al., 1998) .                         |
| ctxr_f35b77144b6ee9eec336 | unknown              | background                 | background          | none                          |         0.55 | True                 | PropBank         |                        | proposed        | background_cue                  | Several different systems of semantic roles are proposed in previous studies (Fillmore, 1968; Palmer et al., 2010; Loper et al., 2007; Baker et al., 1998) .                         |
| ctxr_5ba2d9c30511a7fdaed3 | unknown              | background                 | background          | none                          |         0.55 | True                 | PropBank         |                        | proposed        | background_cue                  | Several different systems of semantic roles are proposed in previous studies (Fillmore, 1968; Palmer et al., 2010; Loper et al., 2007; Baker et al., 1998) .                         |
| ctxr_451b07b4e810c91327a6 | introduction         | background                 | background          | none                          |         0.35 | True                 | FrameNet         |                        |                 | weak_section_prior:introduction | For example, the meaning of lend and give in the above sentences is not categorized into the same Frame in FrameNet (Baker et al., 1998) .                                           |
| ctxr_ab7617f2f9592a20ff6a | introduction         | background                 | background          | none                          |         0.35 | True                 | Transformer;BERT |                        |                 | weak_section_prior:introduction | One of the most successful recent approaches in document and text classification involves finetuning large pretrained language models on a specific task (Adhikari et al., 2019a;... |
| ctxr_7be2d2360c50b43f3fcd | introduction         | background                 | background          | none                          |         0.35 | True                 | Transformer;BERT |                        |                 | weak_section_prior:introduction | One of the most successful recent approaches in document and text classification involves finetuning large pretrained language models on a specific task (Adhikari et al., 2019a;... |

## No Cue But Object Mention Examples
| context_id                | normalized_section   | primary_candidate_intent   | candidate_intents   | candidate_relation_subtypes   |   confidence | should_send_to_llm   | object_names   | generic_metric_names   | evidence_span   | matched_rules                   | sentence_text                                                                                                                                                                        |
|:--------------------------|:---------------------|:---------------------------|:--------------------|:------------------------------|-------------:|:---------------------|:---------------|:-----------------------|:----------------|:--------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ctxr_7e729e2f9c3e394d22a2 | evaluation           | unclear                    | unclear             | none                          |         0.45 | True                 | ROUGE          |                        |                 | no_cue                          | For the intrinsic evaluation of a large number of summaries, we made use of the ROUGE metrics that has been widely used in automatic evaluation of summarization systems (Lin and... |
| ctxr_bcc118cb881cd6af4c4e | evaluation           | unclear                    | unclear             | none                          |         0.45 | True                 | ROUGE          |                        |                 | no_cue                          | For the intrinsic evaluation of a large number of summaries, we made use of the ROUGE metrics that has been widely used in automatic evaluation of summarization systems (Lin and... |
| ctxr_e29d4de098ff144543d9 | related_work         | background                 | background          | none                          |         0.35 | True                 | LSTM           |                        |                 | weak_section_prior:related_work | The dependency path is convenient, but He et al. (2017) revealed that higher accuracies on neural-network-based SRL models could be obtained if correct parsed information is ava... |
| ctxr_977bba59559518243ba7 | results              | unclear                    | unclear             | none                          |         0.45 | True                 | BLEU           |                        |                 | no_cue                          | The BLEU scores (Papineni et al., 2002) Table 1 .                                                                                                                                    |
| ctxr_451b07b4e810c91327a6 | introduction         | background                 | background          | none                          |         0.35 | True                 | FrameNet       |                        |                 | weak_section_prior:introduction | For example, the meaning of lend and give in the above sentences is not categorized into the same Frame in FrameNet (Baker et al., 1998) .                                           |
| ctxr_a0651642b9a07ddadb5d | unknown              | unclear                    | unclear             | none                          |         0.45 | True                 | WordNet        |                        |                 | no_cue                          | It is referred to in other work on wordnets and semantic lexicons (Pedersen et al., 2009; Lindén and Carlson, 2010; Borin and Forsberg, 2010; Mititelu, 2012; Zafar et al., 2012;... |
| ctxr_46d67b9bc578c8c367d0 | unknown              | unclear                    | unclear             | none                          |         0.45 | True                 | WordNet        |                        |                 | no_cue                          | It is referred to in other work on wordnets and semantic lexicons (Pedersen et al., 2009; Lindén and Carlson, 2010; Borin and Forsberg, 2010; Mititelu, 2012; Zafar et al., 2012;... |
| ctxr_dcfc76f6f9808a3f63a8 | unknown              | unclear                    | unclear             | none                          |         0.45 | True                 | WordNet        |                        |                 | no_cue                          | It is referred to in other work on wordnets and semantic lexicons (Pedersen et al., 2009; Lindén and Carlson, 2010; Borin and Forsberg, 2010; Mititelu, 2012; Zafar et al., 2012;... |
| ctxr_b5b931545a5ce6631ab3 | unknown              | unclear                    | unclear             | none                          |         0.45 | True                 | WordNet        |                        |                 | no_cue                          | It is referred to in other work on wordnets and semantic lexicons (Pedersen et al., 2009; Lindén and Carlson, 2010; Borin and Forsberg, 2010; Mititelu, 2012; Zafar et al., 2012;... |
| ctxr_0929cd41422d69e626d0 | unknown              | unclear                    | unclear             | none                          |         0.45 | True                 | WordNet        |                        |                 | no_cue                          | It is referred to in other work on wordnets and semantic lexicons (Pedersen et al., 2009; Lindén and Carlson, 2010; Borin and Forsberg, 2010; Mititelu, 2012; Zafar et al., 2012;... |

## LLM Flagged Examples
| context_id                | normalized_section   | primary_candidate_intent   | candidate_intents               | candidate_relation_subtypes                                  |   confidence | should_send_to_llm   | object_names   | generic_metric_names   | evidence_span   | matched_rules                                                                  | sentence_text                                                                                                                                                                        |
|:--------------------------|:---------------------|:---------------------------|:--------------------------------|:-------------------------------------------------------------|-------------:|:---------------------|:---------------|:-----------------------|:----------------|:-------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ctxr_4771edcc3e42c8bb07c7 | introduction         | uses                       | uses;background                 | direct_use                                                   |         0.65 | True                 |                |                        | described       | use_cue;background_cue                                                         | In NLP, Elsner and Charniak (2010) described the task of thread disentanglement as "the clustering task of dividing a transcript into a set of distinct conversations," in which ... |
| ctxr_d06d69e8921c81b378ac | introduction         | uses                       | uses                            | evaluate_on                                                  |         0.65 | True                 |                |                        | Corpus          | evaluation_cue                                                                 | Carenini et al. (2008) annotated 39 email "conversations" from the Enron Email Corpus for email summariation.                                                                        |
| ctxr_68d4edb5f20b826f715b | introduction         | uses                       | uses                            | evaluate_on                                                  |         0.65 | True                 |                |                        | corpus          | evaluation_cue                                                                 | Wan and McKeown (2004) used a privatelyavailable corpus of 300 threads for summary generation.                                                                                       |
| ctxr_b166bf8511a77353542f | introduction         | uses                       | uses                            | evaluate_on                                                  |         0.65 | True                 |                |                        | corpus          | evaluation_cue                                                                 | Rambow et al. (2004) used a privatelyavailable corpus of 96 email threads for thread summarization.                                                                                  |
| ctxr_6739ef248e0241672c80 | dataset              | uses                       | uses                            | evaluate_on                                                  |         0.65 | True                 |                |                        | corpus          | evaluation_cue                                                                 | Wan and McKeown (2004) reconstructed threads by header Message-ID information.                                                                                                       |
| ctxr_4ba57d063d3c71fa78df | dataset              | uses                       | uses                            | evaluate_on                                                  |         0.65 | True                 |                |                        | corpus          | evaluation_cue                                                                 | Rambow et al. (2004) used a privately-available corpus of 96 email threads, but did not specify how they determined the threads.                                                     |
| ctxr_8361b89d504826d53df9 | unknown              | compares_against           | compares_against                | compare_against                                              |         0.65 | True                 |                |                        | compared with   | compare_cue                                                                    | 1999 ) uses pairs of words occurring in the same order for the two emails; Token Pair Distance (Hatzivassiloglou et al., 1999) measures the distance between pairs of words.         |
| ctxr_d573e73d4a69363cdfc0 | results              | critiques                  | uses;compares_against;critiques | direct_use;compare_against;critique_limitation;report_metric |         0.85 | True                 | accuracy       | accuracy               | using           | use_cue;compare_cue;critique_cue;generic_metric_with_compare_or_evaluation_cue | Elsner and Charniak (2011) use coherence models to disentangle chat, using some features (entity grid, topical entity grid) which correspond to the information in our content fe... |
| ctxr_f6863fcab52657a5c16e | related_work         | compares_against           | uses;compares_against           | direct_use;report_metric                                     |         0.9  | True                 | SemEval        |                        | based on        | use_cue;compare_cue                                                            | In (Tratz and Hovy, 2010) the authors developed a system based on the Maximum Entropy classifier, able to detect 10 bidirectional semantic relations Achieved F-measures depended... |
| ctxr_71d08900475d9c8505ab | related_work         | compares_against           | uses;compares_against           | direct_use;report_metric                                     |         0.65 | True                 |                |                        | based on        | use_cue;compare_cue                                                            | The same set of semantic relations was used in (Rink and Harabagiu, 2010) .                                                                                                          |
