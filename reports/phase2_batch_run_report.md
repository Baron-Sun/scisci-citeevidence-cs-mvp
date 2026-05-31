# Phase-2 Batch Structured Evidence Extraction Report

Batch outputs are parsed and revalidated locally with the same Phase-2 evidence-span and cue validators used by the pilot workflow.

## Outputs
- Manifest: `data/batch/phase2_full_batch_manifest.json`
- Valid labels parquet: `data/processed/phase2_structured_labels_batch.parquet`
- Failed rows JSONL: `data/processed/phase2_structured_labels_batch_failed.jsonl`

## Core Metrics
| metric                          | value     |
|:--------------------------------|:----------|
| total_queue_rows                | 306231    |
| processed_rows                  | 306231    |
| successful_rows                 | 236755    |
| failed_rows                     | 69476     |
| missing_batch_output_rows       | 1         |
| batch_output_lines              | 306230    |
| abstain_count                   | 1598      |
| abstain_rate                    | 0.007     |
| phase1_phase2_disagreement_rate | 0.250     |
| input_tokens                    | 238350952 |
| output_tokens                   | 50443056  |
| total_tokens                    | 288794008 |
| batch_output_input_tokens       | 311199755 |
| batch_output_output_tokens      | 65632936  |
| batch_output_total_tokens       | 376832691 |
| estimated_batch_output_cost_usd | $264.37   |

## Batch Output Files
| batch_id                               | path                                                           |
|:---------------------------------------|:---------------------------------------------------------------|
| batch_6a1bfedd433c8190b221f3ec5ebd1ff2 | data/batch/batch_6a1bfedd433c8190b221f3ec5ebd1ff2.output.jsonl |
| batch_6a1bfef4dca8819084d1b2e64bdb13e5 | data/batch/batch_6a1bfef4dca8819084d1b2e64bdb13e5.output.jsonl |
| batch_6a1bff0a2f048190b066ed87f9761eb3 | data/batch/batch_6a1bff0a2f048190b066ed87f9761eb3.output.jsonl |
| batch_6a1bff1d739481908b0949ebf51d7362 | data/batch/batch_6a1bff1d739481908b0949ebf51d7362.output.jsonl |
| batch_6a1bff3b75e4819095b1855ca2b5ae40 | data/batch/batch_6a1bff3b75e4819095b1855ca2b5ae40.output.jsonl |
| batch_6a1bff510294819090327e3a4fd5c56f | data/batch/batch_6a1bff510294819090327e3a4fd5c56f.output.jsonl |
| batch_6a1bff67023c81909ef42e0d2644a557 | data/batch/batch_6a1bff67023c81909ef42e0d2644a557.output.jsonl |
| batch_6a1bff7697a08190b70ada7bb9600644 | data/batch/batch_6a1bff7697a08190b70ada7bb9600644.output.jsonl |
| batch_6a1bff7ef6a88190b0528031ef094a25 | data/batch/batch_6a1bff7ef6a88190b0528031ef094a25.output.jsonl |

## Final Intent Distribution
| final_intent     |   rows |
|:-----------------|-------:|
| background       | 145978 |
| uses             |  50493 |
| compares_against |  27355 |
| critiques        |   6410 |
| extends          |   4768 |
| applies          |   1152 |
| unclear          |    599 |

## Final Object Type Distribution
| final_object_type     |   rows |
|:----------------------|-------:|
| method                |  72960 |
| model                 |  59017 |
| dataset_or_database   |  29979 |
| metric                |  24462 |
| benchmark_or_protocol |  12731 |
| software_or_tool      |  11188 |
| unknown               |   7877 |
| task                  |   7209 |
| theory_or_concept     |   5784 |
| claim_or_finding      |   5548 |

## Evidence Supports Label Distribution
| evidence_supports_label   |   rows |
|:--------------------------|-------:|
| true                      | 235185 |
| false                     |   1094 |
| unclear                   |    476 |

## Final Intent By Phase-1 Primary Candidate Intent
| primary_candidate_intent   | final_intent     |   rows |
|:---------------------------|:-----------------|-------:|
| background                 | background       | 102890 |
| uses                       | uses             |  43335 |
| unclear                    | background       |  38915 |
| compares_against           | compares_against |  21225 |
| critiques                  | critiques        |   5897 |
| unclear                    | uses             |   5624 |
| unclear                    | compares_against |   3723 |
| extends                    | extends          |   1895 |
| compares_against           | background       |   1801 |
| uses                       | background       |   1761 |
| background                 | compares_against |   1590 |
| unclear                    | extends          |   1526 |
| applies                    | applies          |   1040 |
| background                 | extends          |    957 |
| background                 | uses             |    680 |
| uses                       | compares_against |    642 |
| unclear                    | unclear          |    598 |
| critiques                  | background       |    576 |
| applies                    | uses             |    572 |
| unclear                    | critiques        |    350 |
| uses                       | extends          |    272 |
| compares_against           | uses             |    242 |
| background                 | critiques        |    131 |
| critiques                  | compares_against |    127 |
| unclear                    | applies          |     76 |
| compares_against           | extends          |     75 |
| critiques                  | extends          |     39 |
| critiques                  | uses             |     36 |
| applies                    | compares_against |     24 |
| background                 | applies          |     24 |
| extends                    | compares_against |     24 |
| applies                    | background       |     22 |
| compares_against           | critiques        |     18 |
| uses                       | critiques        |     14 |
| extends                    | background       |     13 |
| uses                       | applies          |      5 |
| applies                    | extends          |      4 |
| compares_against           | applies          |      4 |
| extends                    | uses             |      4 |
| extends                    | applies          |      2 |
| critiques                  | applies          |      1 |
| critiques                  | unclear          |      1 |

## Failed Row Note
Failed rows are kept in JSONL for local revalidation or targeted retry.
