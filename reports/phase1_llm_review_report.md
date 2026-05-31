# Phase-1 LLM-as-Judge Review Report

This is a model-based audit / LLM-assisted validation pass for Phase-1 candidate labels, not final gold labeling.

## Outputs
- Sample CSV: `data/processed/phase1_llm_review_sample.csv`
- JSONL results or dry-run prompts: `data/processed/phase1_llm_review_results.jsonl`
- Parquet results: `data/processed/phase1_llm_review_results.parquet`

## Core Metrics
| metric                      |   value |
|:----------------------------|--------:|
| dry_run                     |    True |
| total_sampled_rows          |     200 |
| reviewed_rows               |       0 |
| dry_run_prompt_records      |     200 |
| invalid_retry_fallback_rows |       0 |
| from_cache_rows             |       0 |
| input_tokens                |       0 |
| output_tokens               |       0 |
| total_tokens                |       0 |

## Sample Bucket Distribution
| review_bucket           |   rows |
|:------------------------|-------:|
| intent_background       |     30 |
| intent_uses             |     30 |
| intent_applies          |     25 |
| intent_compares_against |     25 |
| intent_critiques        |     25 |
| intent_extends          |     25 |
| cited_work_description  |     20 |
| intent_unclear          |     20 |

## Intent Correct Distribution
_No rows._

## Estimated Precision By Primary Candidate Intent
_No rows._

## Better Intent Distribution For Incorrect Rows
_No rows._

## Object Type Correct Distribution
_No rows._

## Relation Subtype Correct Distribution
_No rows._

## Evidence Supports Label Distribution
_No rows._

## Should Send To LLM Correct Distribution
_No rows._

## Better LLM Priority Distribution
_No rows._

## Cited Work Description Correct Distribution
_No rows._

## Error Type Distribution
_No rows._

## Recommended Rule Action Distribution
_No rows._

## Precision By LLM Priority
_No rows._

## Precision By Normalized Section
_No rows._

## Uses False Positive Examples
_No rows._

## Critiques False Positive Examples
_No rows._

## Compares False Positive Examples
_No rows._

## Extends / Applies False Positive Examples
_No rows._

## Cited Work Description Correct Cases
_No rows._

## LLM Priority Mistake Examples
_No rows._

## Sample Rows
| review_bucket   | context_id                | normalized_section   | primary_candidate_intent   | llm_priority   | cited_work_description   | object_names        | generic_metric_names   | evidence_span   | sentence_text                                                                                                                                                                        |
|:----------------|:--------------------------|:---------------------|:---------------------------|:---------------|:-------------------------|:--------------------|:-----------------------|:----------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| intent_uses     | ctxr_cdc6fead41394e6c2bc9 | introduction         | uses                       | high           | True                     | Penn Treebank       |                        | We use          | We use both the new parser and rparse, the parser used in our previous work (Kallmeyer and Maier, 2010) .                                                                            |
| intent_uses     | ctxr_7e609202c7a2933a9633 | unknown              | uses                       | medium         | False                    |                     |                        | we use          | Number of Queries Some existing attack algorithms achieve high attack success rate through massive queries to the model (Yoo et al., 2020) .                                         |
| intent_uses     | ctxr_f477ead0357985edd43b | model                | uses                       | medium         | False                    | SemEval             |                        | using           | Every sentence pair is tokenized, lemmatized and POS tagged using Freeling tool (Atserias et al., 2006) .                                                                            |
| intent_uses     | ctxr_f1e02e0c927ceccbe62e | related_work         | uses                       | high           | False                    | attention mechanism |                        | We used         | We used a similar architecture to that of the Tweet2Vec model (Dhingra et al., 2016) .                                                                                               |
| intent_uses     | ctxr_8c4339996e5a5c41ffaa | introduction         | uses                       | high           | False                    | Penn Treebank       |                        | We use          | We use the state-of-the-art Berkeley Neural Parser (Kitaev et al., 2019) on the SPMRL data set (Seddah et al., 2013 (Seddah et al., , 2014 , and we add the English Penn Treebank... |
| intent_uses     | ctxr_aeeefca6ae2a9272e078 | experiment           | uses                       | medium         | False                    | Moses;BLEU          |                        | using           | In both experiments, the translation model was built using the phrase extraction algorithm (Paul et al., 2010) , with commonly used features in Moses (Ex: probability, lexical w... |
| intent_uses     | ctxr_20326030212f758abf7b | related_work         | uses                       | medium         | False                    | seq2seq;ROUGE       |                        | evaluated on    | Re-cently, sequence-to-sequence models (Sutskever et al., 2014) with attention Chopra et al., 2016) , copy mechanism Gu et al., 2016) , pointer-generator (See et al., 2017) , gr... |
| intent_uses     | ctxr_e4cb4caca81127385de8 | related_work         | uses                       | medium         | False                    | ROUGE;seq2seq       |                        | evaluated on    | Since the system generated summaries are usually evaluated on ROUGE, its been beneficial to directly optimize this metric during training via a suitable policy using reinforceme... |
| intent_uses     | ctxr_5b3fe6cf245dee3f93c6 | unknown              | uses                       | none           | False                    |                     |                        | trained on      | This ability is crucial to achieve good performance and has to be preserved no matter the difficulties that occur when one moves away from conventional phrase-based systems (Chi... |
| intent_uses     | ctxr_f3fb562ee8a12f0abf79 | unknown              | uses                       | medium         | True                     |                     |                        | We used         | We used the same data split as (Lee and Dernoncourt, 2016; Ortega and Vu, 2017; Ravi and Kozareva, 2018 ).                                                                           |
| intent_uses     | ctxr_4c7aa6fa75d59fbf5491 | implementation       | uses                       | high           | False                    | BERT                |                        | We employ       | We employ the open-source framework OpenKE (Han et al., 2018) to obtain the embedding of entities and relations with the BILINEAR model (Yang et al., 2015) .                        |
| intent_uses     | ctxr_e2d72636f7c562b036ea | experiment           | uses                       | medium         | False                    |                     |                        | we use          | Pre-trained Embedding Based on Shao et al. (2017) ; , n-grams are of great benefit to CWS and POS tagging tasks.                                                                     |
| intent_uses     | ctxr_ceb1e87bc6746263be6a | related_work         | uses                       | medium         | False                    |                     |                        | we use          | In contrast, we use massively multilingual sentence embeddings trained on almost 100 languages, and then conduct margin-based mining in the multilingual embedding space (Schwenk... |
| intent_uses     | ctxr_cb4c12a9b710601e9739 | results              | uses                       | medium         | False                    |                     |                        | we use          | Those kinds of methods were used in previous opinion mining works (Wu et al., 2009; Kobayashi et al., 2007) .                                                                        |
| intent_uses     | ctxr_d75d55b48bbd898d33d4 | unknown              | uses                       | medium         | False                    |                     |                        | We use          | 5 • Entity Features: Noting that mentions of named entities provide strong topical cues, we extract such mentions in the Tweet text using an off-the-shelf Twitter NER model (Mis... |
| intent_uses     | ctxr_cd0d74263b5337762160 | method               | uses                       | high           | False                    | BLEU                |                        | we used         | During our work, we used BLEU (Papineni et al., 2002) on news-valid (concatenation of news-test 2012 and 2013) to ensure that our models stayed good on a more general domain, an... |
| intent_uses     | ctxr_75d132d8be03e8e8a08c | unknown              | uses                       | medium         | True                     |                     |                        | We used         | We were also inspired by the English-tweet POS tagset defined by Gimpel et al. (2011) , and have aimed to stay closely aligned to it in order to facilitate any future work on cr... |
| intent_uses     | ctxr_01db04650958b8dba98e | experiment           | uses                       | medium         | True                     |                     |                        | We use          | Visual Reasoning We use the published pretrained weights and the same training configuration of LXMERT (Tan and Bansal, 2019) , with 36 bounding boxes proposed per image.           |
| intent_uses     | ctxr_1cca63de84693dd1d3ca | experiment           | uses                       | medium         | False                    |                     |                        | we employ       | Then, we employ byte pair encoding (BPE) (Sennrich et al., 2016) with 50,000 operations to alleviate Out-of-Vocabulary problem.                                                      |
| intent_uses     | ctxr_a36748e0f2bcac250fe5 | evaluation           | uses                       | medium         | False                    | BLEU;METEOR         |                        | using           | We also evaluated the performances of the MT systems using a set of state-of-the-art automatic evaluation metrics: BLEU (Papineni et al., 2002) , NIST (Doddington, 2002) , METEO... |
