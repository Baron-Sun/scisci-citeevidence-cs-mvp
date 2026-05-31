# Phase-2 Batch Cost Estimate

This estimate uses local configured Batch prices and observed pilot token averages when available. It does not call the OpenAI API.

## Queue Counts
| queue_path                                     |   rows |
|:-----------------------------------------------|-------:|
| data/processed/phase1_llm_queue_high.parquet   |  34540 |
| data/processed/phase1_llm_queue_medium.parquet | 271691 |

## Estimate
| metric                    | value                                                             |
|:--------------------------|:------------------------------------------------------------------|
| model                     | gpt-5.4-mini                                                      |
| total_rows                | 306231                                                            |
| input_tokens_per_row      | 1829.27                                                           |
| output_tokens_per_row     | 157.68                                                            |
| estimated_input_tokens    | 560178198                                                         |
| estimated_output_tokens   | 48285570                                                          |
| estimated_total_tokens    | 608463768                                                         |
| estimated_input_cost_usd  | $210.07                                                           |
| estimated_output_cost_usd | $108.64                                                           |
| estimated_total_cost_usd  | $318.71                                                           |
| pilot_average_source      | data/processed/phase2_structured_labels_pilot_revalidated.parquet |
| pricing_source            | local_batch_price_config                                          |
