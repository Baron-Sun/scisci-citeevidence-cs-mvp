# Phase-2 Failed Validation Diagnostics

- Diagnostics parquet: `data/processed/phase2_batch_failed_validation_diagnostics.parquet`

## Core Metrics
| metric                                     |   value |
|:-------------------------------------------|--------:|
| diagnostic_rows                            |   69476 |
| cue_failure_rows                           |   29413 |
| revalidated_success_rows                   |     942 |
| remaining_failed_rows                      |   68534 |
| remaining_evidence_span_not_substring      |   25311 |
| remaining_cited_title_only_object_rejected |    1609 |

## Failure Category By Phase-1 Intent
| primary_candidate_intent   | failed_validator_type            |   rows |
|:---------------------------|:---------------------------------|-------:|
| unclear                    | use_cue_not_accepted             |  17033 |
| background                 | evidence_span_not_substring      |  12587 |
| unclear                    | evidence_span_not_substring      |   5935 |
| background                 | quote_not_substring              |   4563 |
| uses                       | evidence_span_not_substring      |   3766 |
| unclear                    | compare_cue_not_accepted         |   3307 |
| unclear                    | quote_not_substring              |   2417 |
| background                 | use_cue_not_accepted             |   2355 |
| compares_against           | evidence_span_not_substring      |   2211 |
| uses                       | quote_not_substring              |   1569 |
| background                 | cited_title_only_object_rejected |   1401 |
| unclear                    | extend_cue_not_accepted          |   1299 |
| unclear                    | schema_error                     |   1147 |
| uses                       | use_cue_not_accepted             |    981 |
| compares_against           | quote_not_substring              |    964 |
| background                 | compare_cue_not_accepted         |    906 |
| unclear                    | critique_cue_not_accepted        |    754 |
| critiques                  | evidence_span_not_substring      |    635 |
| unclear                    | apply_cue_not_accepted           |    532 |
| background                 | extend_cue_not_accepted          |    454 |
| compares_against           | other                            |    444 |
| compares_against           | compare_cue_not_accepted         |    387 |
| critiques                  | quote_not_substring              |    387 |
| uses                       | other                            |    335 |
| unclear                    | other                            |    297 |
| uses                       | schema_error                     |    282 |
| uses                       | compare_cue_not_accepted         |    269 |
| background                 | critique_cue_not_accepted        |    236 |
| uses                       | extend_cue_not_accepted          |    236 |
| compares_against           | use_cue_not_accepted             |    209 |
| compares_against           | schema_error                     |    147 |
| background                 | schema_error                     |    138 |
| critiques                  | critique_cue_not_accepted        |    125 |
| critiques                  | other                            |    117 |
| uses                       | cited_title_only_object_rejected |    116 |
| extends                    | evidence_span_not_substring      |    103 |
| extends                    | quote_not_substring              |    102 |
| background                 | other                            |     80 |
| applies                    | evidence_span_not_substring      |     74 |
| critiques                  | schema_error                     |     74 |
| applies                    | quote_not_substring              |     56 |
| compares_against           | cited_title_only_object_rejected |     43 |
| compares_against           | extend_cue_not_accepted          |     39 |
| compares_against           | critique_cue_not_accepted        |     36 |
| applies                    | use_cue_not_accepted             |     34 |
| background                 | apply_cue_not_accepted           |     33 |
| applies                    | cited_title_only_object_rejected |     32 |
| critiques                  | extend_cue_not_accepted          |     30 |
| uses                       | critique_cue_not_accepted        |     29 |
| applies                    | extend_cue_not_accepted          |     28 |
| critiques                  | use_cue_not_accepted             |     27 |
| critiques                  | compare_cue_not_accepted         |     21 |
| extends                    | extend_cue_not_accepted          |     13 |
| applies                    | compare_cue_not_accepted         |      9 |
| applies                    | other                            |      9 |
| critiques                  | cited_title_only_object_rejected |      9 |
| extends                    | use_cue_not_accepted             |      9 |
| extends                    | cited_title_only_object_rejected |      8 |
| applies                    | apply_cue_not_accepted           |      7 |
| compares_against           | apply_cue_not_accepted           |      6 |
| applies                    | schema_error                     |      5 |
| extends                    | schema_error                     |      5 |
| critiques                  | apply_cue_not_accepted           |      4 |
| extends                    | other                            |      4 |
| extends                    | compare_cue_not_accepted         |      3 |
| uses                       | apply_cue_not_accepted           |      2 |
| background                 | missing_batch_output             |      1 |

## Failure Category By Batch File
| batch_id                               | failed_validator_type            |   rows |
|:---------------------------------------|:---------------------------------|-------:|
| batch_6a1bff510294819090327e3a4fd5c56f | evidence_span_not_substring      |   3367 |
| batch_6a1bff1d739481908b0949ebf51d7362 | evidence_span_not_substring      |   3210 |
| batch_6a1bff7697a08190b70ada7bb9600644 | evidence_span_not_substring      |   3140 |
| batch_6a1bff0a2f048190b066ed87f9761eb3 | evidence_span_not_substring      |   3102 |
| batch_6a1bff3b75e4819095b1855ca2b5ae40 | evidence_span_not_substring      |   2965 |
| batch_6a1bff67023c81909ef42e0d2644a557 | evidence_span_not_substring      |   2959 |
| batch_6a1bfef4dca8819084d1b2e64bdb13e5 | evidence_span_not_substring      |   2952 |
| batch_6a1bff0a2f048190b066ed87f9761eb3 | use_cue_not_accepted             |   2900 |
| batch_6a1bfef4dca8819084d1b2e64bdb13e5 | use_cue_not_accepted             |   2800 |
| batch_6a1bff1d739481908b0949ebf51d7362 | use_cue_not_accepted             |   2685 |
| batch_6a1bff67023c81909ef42e0d2644a557 | use_cue_not_accepted             |   2676 |
| batch_6a1bff510294819090327e3a4fd5c56f | use_cue_not_accepted             |   2632 |
| batch_6a1bfedd433c8190b221f3ec5ebd1ff2 | evidence_span_not_substring      |   2525 |
| batch_6a1bff3b75e4819095b1855ca2b5ae40 | use_cue_not_accepted             |   2513 |
| batch_6a1bff7697a08190b70ada7bb9600644 | use_cue_not_accepted             |   2317 |
| batch_6a1bff7ef6a88190b0528031ef094a25 | use_cue_not_accepted             |   1389 |
| batch_6a1bfedd433c8190b221f3ec5ebd1ff2 | quote_not_substring              |   1316 |
| batch_6a1bff1d739481908b0949ebf51d7362 | quote_not_substring              |   1274 |
| batch_6a1bff7697a08190b70ada7bb9600644 | quote_not_substring              |   1246 |
| batch_6a1bff67023c81909ef42e0d2644a557 | quote_not_substring              |   1232 |
| batch_6a1bff510294819090327e3a4fd5c56f | quote_not_substring              |   1201 |
| batch_6a1bff0a2f048190b066ed87f9761eb3 | quote_not_substring              |   1139 |
| batch_6a1bfef4dca8819084d1b2e64bdb13e5 | quote_not_substring              |   1101 |
| batch_6a1bff7ef6a88190b0528031ef094a25 | evidence_span_not_substring      |   1091 |
| batch_6a1bff3b75e4819095b1855ca2b5ae40 | quote_not_substring              |   1081 |
| batch_6a1bfedd433c8190b221f3ec5ebd1ff2 | use_cue_not_accepted             |    736 |
| batch_6a1bff7697a08190b70ada7bb9600644 | compare_cue_not_accepted         |    696 |
| batch_6a1bfef4dca8819084d1b2e64bdb13e5 | compare_cue_not_accepted         |    665 |
| batch_6a1bff67023c81909ef42e0d2644a557 | compare_cue_not_accepted         |    632 |
| batch_6a1bff510294819090327e3a4fd5c56f | compare_cue_not_accepted         |    609 |
| batch_6a1bff0a2f048190b066ed87f9761eb3 | compare_cue_not_accepted         |    589 |
| batch_6a1bff1d739481908b0949ebf51d7362 | compare_cue_not_accepted         |    588 |
| batch_6a1bff3b75e4819095b1855ca2b5ae40 | compare_cue_not_accepted         |    582 |
| batch_6a1bff7ef6a88190b0528031ef094a25 | quote_not_substring              |    468 |
| batch_6a1bfedd433c8190b221f3ec5ebd1ff2 | other                            |    353 |
| batch_6a1bfef4dca8819084d1b2e64bdb13e5 | extend_cue_not_accepted          |    318 |
| batch_6a1bfedd433c8190b221f3ec5ebd1ff2 | compare_cue_not_accepted         |    312 |
| batch_6a1bfef4dca8819084d1b2e64bdb13e5 | cited_title_only_object_rejected |    290 |
| batch_6a1bff7697a08190b70ada7bb9600644 | extend_cue_not_accepted          |    276 |
| batch_6a1bff510294819090327e3a4fd5c56f | extend_cue_not_accepted          |    267 |
| batch_6a1bff67023c81909ef42e0d2644a557 | extend_cue_not_accepted          |    263 |
| batch_6a1bff3b75e4819095b1855ca2b5ae40 | extend_cue_not_accepted          |    255 |
| batch_6a1bff1d739481908b0949ebf51d7362 | cited_title_only_object_rejected |    238 |
| batch_6a1bfef4dca8819084d1b2e64bdb13e5 | schema_error                     |    235 |
| batch_6a1bff1d739481908b0949ebf51d7362 | extend_cue_not_accepted          |    234 |
| batch_6a1bff1d739481908b0949ebf51d7362 | schema_error                     |    232 |
| batch_6a1bff510294819090327e3a4fd5c56f | schema_error                     |    230 |
| batch_6a1bff7ef6a88190b0528031ef094a25 | compare_cue_not_accepted         |    229 |
| batch_6a1bff0a2f048190b066ed87f9761eb3 | cited_title_only_object_rejected |    222 |
| batch_6a1bff3b75e4819095b1855ca2b5ae40 | schema_error                     |    222 |
| batch_6a1bff0a2f048190b066ed87f9761eb3 | extend_cue_not_accepted          |    220 |
| batch_6a1bff7697a08190b70ada7bb9600644 | schema_error                     |    219 |
| batch_6a1bff0a2f048190b066ed87f9761eb3 | schema_error                     |    201 |
| batch_6a1bff7697a08190b70ada7bb9600644 | cited_title_only_object_rejected |    200 |
| batch_6a1bfedd433c8190b221f3ec5ebd1ff2 | schema_error                     |    195 |
| batch_6a1bff510294819090327e3a4fd5c56f | cited_title_only_object_rejected |    187 |
| batch_6a1bff67023c81909ef42e0d2644a557 | schema_error                     |    187 |
| batch_6a1bff7697a08190b70ada7bb9600644 | critique_cue_not_accepted        |    182 |
| batch_6a1bfef4dca8819084d1b2e64bdb13e5 | critique_cue_not_accepted        |    173 |
| batch_6a1bff3b75e4819095b1855ca2b5ae40 | cited_title_only_object_rejected |    170 |
| batch_6a1bff7697a08190b70ada7bb9600644 | other                            |    166 |
| batch_6a1bff67023c81909ef42e0d2644a557 | cited_title_only_object_rejected |    164 |
| batch_6a1bff3b75e4819095b1855ca2b5ae40 | critique_cue_not_accepted        |    157 |
| batch_6a1bff67023c81909ef42e0d2644a557 | critique_cue_not_accepted        |    145 |
| batch_6a1bff510294819090327e3a4fd5c56f | critique_cue_not_accepted        |    144 |
| batch_6a1bff0a2f048190b066ed87f9761eb3 | critique_cue_not_accepted        |    143 |
| batch_6a1bfedd433c8190b221f3ec5ebd1ff2 | extend_cue_not_accepted          |    136 |
| batch_6a1bff1d739481908b0949ebf51d7362 | critique_cue_not_accepted        |    130 |
| batch_6a1bff7ef6a88190b0528031ef094a25 | extend_cue_not_accepted          |    130 |
| batch_6a1bff510294819090327e3a4fd5c56f | other                            |    124 |
| batch_6a1bff0a2f048190b066ed87f9761eb3 | other                            |    123 |
| batch_6a1bff67023c81909ef42e0d2644a557 | other                            |    123 |
| batch_6a1bfef4dca8819084d1b2e64bdb13e5 | other                            |    119 |
| batch_6a1bff3b75e4819095b1855ca2b5ae40 | other                            |    119 |
| batch_6a1bff1d739481908b0949ebf51d7362 | other                            |    112 |
| batch_6a1bff510294819090327e3a4fd5c56f | apply_cue_not_accepted           |     94 |
| batch_6a1bfef4dca8819084d1b2e64bdb13e5 | apply_cue_not_accepted           |     83 |
| batch_6a1bff7ef6a88190b0528031ef094a25 | cited_title_only_object_rejected |     82 |
| batch_6a1bff7697a08190b70ada7bb9600644 | apply_cue_not_accepted           |     78 |
| batch_6a1bff7ef6a88190b0528031ef094a25 | schema_error                     |     77 |
| batch_6a1bff1d739481908b0949ebf51d7362 | apply_cue_not_accepted           |     75 |
| batch_6a1bff67023c81909ef42e0d2644a557 | apply_cue_not_accepted           |     74 |
| batch_6a1bff0a2f048190b066ed87f9761eb3 | apply_cue_not_accepted           |     68 |
| batch_6a1bff7ef6a88190b0528031ef094a25 | critique_cue_not_accepted        |     67 |
| batch_6a1bff3b75e4819095b1855ca2b5ae40 | apply_cue_not_accepted           |     63 |
| batch_6a1bfedd433c8190b221f3ec5ebd1ff2 | cited_title_only_object_rejected |     56 |
| batch_6a1bff7ef6a88190b0528031ef094a25 | other                            |     47 |
| batch_6a1bfedd433c8190b221f3ec5ebd1ff2 | critique_cue_not_accepted        |     39 |
| batch_6a1bff7ef6a88190b0528031ef094a25 | apply_cue_not_accepted           |     38 |
| batch_6a1bfedd433c8190b221f3ec5ebd1ff2 | apply_cue_not_accepted           |     11 |
| blank                                  | missing_batch_output             |      1 |

## Recovered By Failure Category
| failed_validator_type     |   rows |
|:--------------------------|-------:|
| use_cue_not_accepted      |    511 |
| compare_cue_not_accepted  |    255 |
| extend_cue_not_accepted   |    153 |
| critique_cue_not_accepted |     23 |

## Remaining By Failure Category
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

## Recovered Examples
| context_id                | primary_candidate_intent   | failed_validator_type     | candidate_repair_action        | final_intent     | final_object_type     | evidence_span                                                                                                                                                                                                                | validation_error                                            | revalidation_error   |
|:--------------------------|:---------------------------|:--------------------------|:-------------------------------|:-----------------|:----------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------|:---------------------|
| ctxr_2cecf89740d4eb3330bb | applies                    | extend_cue_not_accepted   | revalidate_after_cue_expansion | extends          | method                | we use a strategy inspired by the graph-based parser of Kiperwasser and Goldberg (2016) , with the following major differences: (a) the network is trained to produce fully connected subgraphs (not parsing trees); (b) ... | final_intent=extends requires extend/adapt/improve evidence |                      |
| ctxr_f046d453884a870316f0 | uses                       | use_cue_not_accepted      | revalidate_after_cue_expansion | uses             | dataset_or_database   | combine three NLI corpus (SNLI (Bowman (Williams et al., 2018) , and WNLI (Levesque, 2011)) from the GLUE benchmark (Wang et al., 2018) and use them for NLI pre-training                                                    | final_intent=uses requires current-paper use evidence       |                      |
| ctxr_5cf92f14e496bd040833 | compares_against           | compare_cue_not_accepted  | revalidate_after_cue_expansion | compares_against | model                 | we use dense features to represent each utterance and explore the use of different embedding types-GloVe (Pennington et al., 2014) , ELMo (Peters et al., 2018b,a) , and BERT (Devlin et al., 2018)as well as the effect ... | final_intent=compares_against requires compare evidence     |                      |
| ctxr_3cefa61de8fe78a5fcec | compares_against           | compare_cue_not_accepted  | revalidate_after_cue_expansion | compares_against | metric                | show comparable ∆G and WinoMT accuracy results to those reported by Stanovsky et al. (2019)                                                                                                                                  | final_intent=compares_against requires compare evidence     |                      |
| ctxr_c4316423318971e19ce5 | uses                       | extend_cue_not_accepted   | revalidate_after_cue_expansion | extends          | model                 | we used the bi-directional representations to take the differences for LSTM-Minus unlike the original one(Wang and Chang, 2016)                                                                                              | final_intent=extends requires extend/adapt/improve evidence |                      |
| ctxr_6f993ef990da587ca311 | uses                       | use_cue_not_accepted      | revalidate_after_cue_expansion | uses             | model                 | our method uses BERT-large with only 340 million parameters                                                                                                                                                                  | final_intent=uses requires current-paper use evidence       |                      |
| ctxr_76afc634994e1338589a | compares_against           | use_cue_not_accepted      | revalidate_after_cue_expansion | uses             | metric                | we performed automatic evaluation of all NMT systems (both baseline and adapted systems) using BLEU (Papineni et al., 2002) , ChrF2 (Popović, 2015) , and CharacTER (Wang et al., 2016 )                                     | final_intent=uses requires current-paper use evidence       |                      |
| ctxr_0dc5ac94944f382034ef | compares_against           | use_cue_not_accepted      | revalidate_after_cue_expansion | uses             | metric                | We evaluated all MT systems using multiple automatic evaluation metrics including BLEU (Papineni et al., 2002) , BEER 2.0 (Stanojevic and Sima'an, 2014) , CharacTER (Wang et al., 2016)                                     | final_intent=uses requires current-paper use evidence       |                      |
| ctxr_fa9c8ad940d986218934 | applies                    | extend_cue_not_accepted   | revalidate_after_cue_expansion | extends          | method                | inspired by probability thresholding (Dou and Neubig, 2021), we apply softmax to S, and zero out probabilities below a threshold                                                                                             | final_intent=extends requires extend/adapt/improve evidence |                      |
| ctxr_a25452a7dec77f158a2c | uses                       | use_cue_not_accepted      | revalidate_after_cue_expansion | uses             | model                 | Our method employs recent pre-training language models such as ELMo (Peters et al., 2018) and BERT (Devlin et al., 2019) to measure the similarities of words                                                                | final_intent=uses requires current-paper use evidence       |                      |
| ctxr_3b84970ca0eb39891c89 | uses                       | use_cue_not_accepted      | revalidate_after_cue_expansion | uses             | model                 | Our method employs recent pre-training language models such as ELMo (Peters et al., 2018) and BERT (Devlin et al., 2019) to measure the similarities of words                                                                | final_intent=uses requires current-paper use evidence       |                      |
| ctxr_f4f722966e90836bb181 | critiques                  | critique_cue_not_accepted | revalidate_after_cue_expansion | critiques        | dataset_or_database   | results on the standard test set are not reliable due to the small set of just 761 relations                                                                                                                                 | final_intent=critiques requires explicit critique evidence  |                      |
| ctxr_9d1edd70a7ee83962ba0 | uses                       | use_cue_not_accepted      | revalidate_after_cue_expansion | uses             | method                | Our method uses relation-specific tables (Miwa and Sasaki, 2014) to handle each relation separately.                                                                                                                         | final_intent=uses requires current-paper use evidence       |                      |
| ctxr_0ec2224c27c2139b732b | critiques                  | use_cue_not_accepted      | revalidate_after_cue_expansion | uses             | software_or_tool      | we perform word alignment using some publicly available tools, such as Giza++ (Och and Ney, 2003)                                                                                                                            | final_intent=uses requires current-paper use evidence       |                      |
| ctxr_91621cdfe38d3ee26cad | critiques                  | use_cue_not_accepted      | revalidate_after_cue_expansion | uses             | software_or_tool      | we perform word alignment using some publicly available tools, such as Giza++ (Och and Ney, 2003) or Berkeley Aligner (Liang et al., 2006; DeNero and Klein, 2007)                                                           | final_intent=uses requires current-paper use evidence       |                      |
| ctxr_08935d09b1ad7bfe9a5a | critiques                  | use_cue_not_accepted      | revalidate_after_cue_expansion | uses             | software_or_tool      | we perform word alignment using some publicly available tools, such as Giza++ (Och and Ney, 2003) or Berkeley Aligner (Liang et al., 2006; DeNero and Klein, 2007)                                                           | final_intent=uses requires current-paper use evidence       |                      |
| ctxr_8e8a66ec54f040160430 | critiques                  | use_cue_not_accepted      | revalidate_after_cue_expansion | uses             | software_or_tool      | we perform word alignment using some publicly available tools, such as Giza++ (Och and Ney, 2003) or Berkeley Aligner (Liang et al., 2006; DeNero and Klein, 2007)                                                           | final_intent=uses requires current-paper use evidence       |                      |
| ctxr_21a9577989b179178a8f | compares_against           | use_cue_not_accepted      | revalidate_after_cue_expansion | uses             | metric                | We compute corpus-level performance statistics using four standard generation evaluation metrics: ROUGE-L (Lin, 2004) , CIDEr (Vedantam et al., 2015) , (Papineni et al., 2002) and METEOR (Banerjee and Lavie, 2005 ) (h... | final_intent=uses requires current-paper use evidence       |                      |
| ctxr_6457cff3c19df3d13e55 | uses                       | critique_cue_not_accepted | revalidate_after_cue_expansion | critiques        | metric                | BLEU is not known to work well on a per-sentence level (Lavie et al., 2004) as needed for oracle selection.                                                                                                                  | final_intent=critiques requires explicit critique evidence  |                      |
| ctxr_352dc318ddad9535b628 | uses                       | compare_cue_not_accepted  | revalidate_after_cue_expansion | compares_against | benchmark_or_protocol | to make our experimental results directly comparable to Wong and Mooney (2007) , we used the identical training and test data splits for the 4 runs of 10-fold cross validation used by Wong and Mooney (2007) on both co... | final_intent=compares_against requires compare evidence     |                      |

## Remaining Failure Examples
| context_id                | primary_candidate_intent   | failed_validator_type       | candidate_repair_action            | final_intent     | final_object_type     | evidence_span                                                                                                                                                                                                                | validation_error                                                          | revalidation_error                                                   |
|:--------------------------|:---------------------------|:----------------------------|:-----------------------------------|:-----------------|:----------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------|:---------------------------------------------------------------------|
| ctxr_578992fe86888ec95c7e | uses                       | evidence_span_not_substring | needs_model_retry_or_manual_review | uses             | metric                | we used the criteria from the IWSLT evaluation campaign ... namely word error rate (WER), positionindependent word error rate (PER), and the BLEU and NIST scores                                                            | evidence_span is not an exact substring of evidence fields                | not eligible for local cue revalidation: evidence_span_not_substring |
| ctxr_55dc3c17d39b66939b1a | uses                       | evidence_span_not_substring | needs_model_retry_or_manual_review | uses             | metric                | we used the criteria from the IWSLT evaluation campaign ... namely word error rate (WER), positionindependent word error rate (PER), and the BLEU and NIST scores                                                            | evidence_span is not an exact substring of evidence fields                | not eligible for local cue revalidation: evidence_span_not_substring |
| ctxr_6e4bfc824061dc46c72e | compares_against           | quote_not_substring         | needs_model_retry_or_manual_review | compares_against | metric                | We provide results using a range of automatic evaluation metrics: BLEU (Papineni et al., 2002) , Precision and Recall (Turian et al., 2003) , and Word-and Sentence Error Rates.                                             | comparison_or_tradeoff_quote is not an exact substring of evidence fields | not eligible for local cue revalidation: quote_not_substring         |
| ctxr_615070e2a2c69b21eda3 | uses                       | evidence_span_not_substring | needs_model_retry_or_manual_review | uses             | software_or_tool      | We used Stanford CoreNLP for all other corpora (Toutanova et al., 2003; Manning et al., 2014)                                                                                                                                | evidence_span is not an exact substring of evidence fields                | not eligible for local cue revalidation: evidence_span_not_substring |
| ctxr_8771caf81628bc56acb7 | uses                       | evidence_span_not_substring | needs_model_retry_or_manual_review | uses             | software_or_tool      | We used Stanford CoreNLP for all other corpora                                                                                                                                                                               | evidence_span is not an exact substring of evidence fields                | not eligible for local cue revalidation: evidence_span_not_substring |
| ctxr_b633d4085a7fb8665c11 | uses                       | evidence_span_not_substring | needs_model_retry_or_manual_review | uses             | software_or_tool      | We used Stanford CoreNLP for all other corpora                                                                                                                                                                               | evidence_span is not an exact substring of evidence fields                | not eligible for local cue revalidation: evidence_span_not_substring |
| ctxr_26b6c756ccb8d31c3efd | uses                       | evidence_span_not_substring | needs_model_retry_or_manual_review | uses             | software_or_tool      | We used Stanford CoreNLP for all other corpora (Toutanova et al., 2003; Manning et al., 2014)                                                                                                                                | evidence_span is not an exact substring of evidence fields                | not eligible for local cue revalidation: evidence_span_not_substring |
| ctxr_80b5af2dfbb995510268 | uses                       | quote_not_substring         | needs_model_retry_or_manual_review | uses             | benchmark_or_protocol | We use the Winograd NLI dataset, a variant of the Winograd Schema Challenge (Levesque et al., 2012) , provided in the GLUE benchmark (Wang et al., 2018) to probe for commonsense reasoning.                                 | problem_or_motivation_quote is not an exact substring of evidence fields  | not eligible for local cue revalidation: quote_not_substring         |
| ctxr_5aac81c6d759c1e1a986 | uses                       | quote_not_substring         | needs_model_retry_or_manual_review | uses             | benchmark_or_protocol | combine three NLI corpus (SNLI (Bowman (Williams et al., 2018) , and WNLI (Levesque, 2011)) from the GLUE benchmark (Wang et al., 2018) and use them for NLI pre-training                                                    | usage_or_mechanism_quote is not an exact substring of evidence fields     | not eligible for local cue revalidation: quote_not_substring         |
| ctxr_f776d4baec9cecbfaf0e | uses                       | evidence_span_not_substring | needs_model_retry_or_manual_review | uses             | model                 | we use 0.01 as the threshold; ... BL-100shot a and BL-100shot b are based on bert-large model, reported by Larson et al. (2019)                                                                                              | evidence_span is not an exact substring of evidence fields                | not eligible for local cue revalidation: evidence_span_not_substring |
| ctxr_95ed71dd70a95cc93060 | uses                       | other                       | manual_review                      | background       | model                 | We use a sequence-to-sequence model because of their flexibility and widespread use in semantic parsing (Jia and Liang, 2016; Dong and Lapata, 2016; Rongali et al., 2020) and NLP in general.                               | non-abstain final labels require evidence_supports_label=true             | not eligible for local cue revalidation: other                       |
| ctxr_302414f73676904e8e4a | uses                       | quote_not_substring         | needs_model_retry_or_manual_review | uses             | software_or_tool      | We used GIZA++ (Och and Ney, 2003) for word alignment, SRILM (Stolcke, 2002) for building a 5gram language model, Minimum Error Rate Training (Och, 2003) for tuning, and the Moses decoder (Koehn et al., 2007) in each ... | usage_or_mechanism_quote is not an exact substring of evidence fields     | not eligible for local cue revalidation: quote_not_substring         |
| ctxr_112811c100f28ba003ed | uses                       | evidence_span_not_substring | needs_model_retry_or_manual_review | uses             | dataset_or_database   | For non-UA format data (OD), we use two datasets in the CoNLL format: OntoNotes (ON) (Pradhan et al., 2012) and BOLT (Li et al., 2016).                                                                                      | evidence_span is not an exact substring of evidence fields                | not eligible for local cue revalidation: evidence_span_not_substring |
| ctxr_61f9dd648cc3300b539f | compares_against           | compare_cue_not_accepted    | revalidate_after_cue_expansion     | compares_against | metric                | the system using the tagger by Paikens et al. (2013)                                                                                                                                                                         | final_intent=compares_against requires compare evidence                   | final_intent=compares_against requires compare evidence              |
| ctxr_91d37fcc765310f003ce | uses                       | evidence_span_not_substring | needs_model_retry_or_manual_review | uses             | model                 | we employed a neural network based architecture, more precisely an specific Bi-LSTM ... with a CRF on top of it (Lample et al., 2016; Ma and Hovy, 2016) using as input raw text and the word-embeddings                     | evidence_span is not an exact substring of evidence fields                | not eligible for local cue revalidation: evidence_span_not_substring |
| ctxr_dad052e37a1bab2329fd | uses                       | evidence_span_not_substring | needs_model_retry_or_manual_review | uses             | model                 | we employed a neural network based architecture, more precisely an specific Bi-LSTM ... with a CRF on top of it (Lample et al., 2016; Ma and Hovy, 2016) using as input raw text and the word-embeddings                     | evidence_span is not an exact substring of evidence fields                | not eligible for local cue revalidation: evidence_span_not_substring |
| ctxr_92f342a77075f46e489f | uses                       | evidence_span_not_substring | needs_model_retry_or_manual_review | uses             | model                 | we employed a neural network based architecture, more precisely an specific Bi-LSTM ... with a CRF on top of it (Lample et al., 2016; Ma and Hovy, 2016) using as input raw text and the word-embeddings                     | evidence_span is not an exact substring of evidence fields                | not eligible for local cue revalidation: evidence_span_not_substring |
| ctxr_d00980750603a5628ab8 | uses                       | evidence_span_not_substring | needs_model_retry_or_manual_review | uses             | model                 | we employed a neural network based architecture, more precisely an specific Bi-LSTM ... with a CRF on top of it (Lample et al., 2016; Ma and Hovy, 2016) using as input raw text and the word-embeddings                     | evidence_span is not an exact substring of evidence fields                | not eligible for local cue revalidation: evidence_span_not_substring |
| ctxr_8cdc420f345af6606850 | uses                       | evidence_span_not_substring | needs_model_retry_or_manual_review | uses             | method                | We use word cluster features (Uszkoreit and Brants, 2008) for the current word, and transition features of the cluster of the current and previous word.                                                                     | evidence_span is not an exact substring of evidence fields                | not eligible for local cue revalidation: evidence_span_not_substring |
| ctxr_317ec5bf2714c49c7ce8 | compares_against           | evidence_span_not_substring | needs_model_retry_or_manual_review | compares_against | model                 | pretrained Transformer-based architectures ... have considerably outperformed prior state of the art in various downstream tasks (Devlin et al., 2019; Yang et al., 2019a; Radford et al., 2019)                             | evidence_span is not an exact substring of evidence fields                | not eligible for local cue revalidation: evidence_span_not_substring |
