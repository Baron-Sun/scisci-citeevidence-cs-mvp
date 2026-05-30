# Manual Resolution Review Report

## Inputs
- Strong sample: `data/processed/strong_resolved_contexts_sample.csv`
- Manual mixed sample: `data/processed/manual_resolution_review_sample.csv`

## Outputs
- Clean review parquet: `data/processed/manual_resolution_review_clean.parquet`
- Needs-check CSV: `data/processed/manual_resolution_review_needs_check.csv`

## Core Metrics
| metric | value |
| --- | --- |
| total rows | 800 |
| reviewed rows | 0 |
| unreviewed rows | 800 |
| invalid reviewer_correct rows | 0 |
| needs_check rows | 0 |
| reviewed strong_author_year rows | 0 |
| precision among reviewed strong_author_year rows | unavailable |

## Review Value Counts
| reviewer_correct | rows |
| --- | --- |
| blank | 800 |

## Sample Source Counts
| review_sample_source | rows |
| --- | --- |
| manual_sample | 500 |
| strong_sample | 300 |

## Precision By Normalized Section
No records available.

## Precision By Marker Type
No records available.

## Precision By Resolution Status
No records available.

## Reviewer Error Type Counts
No records available.

## Examples: False Or Unclear Rows
No records available.

## Rows Needing Check
No records available.

## Recommendation
No reviewed true/false strong_author_year rows are available yet. The analysis-ready table can be used to develop downstream code, but a manual precision estimate should be completed before reporting final accuracy.
