# Full Phase-2 Batch Result Summary

## What Was Implemented Earlier

Commit `62cb76b` added the large-scale Phase-2 Batch API workflow:

- `citeevidence phase2 estimate-batch-cost`
- `citeevidence phase2 prepare-batch`
- `citeevidence phase2 submit-batch`
- `citeevidence phase2 check-batch`
- `citeevidence phase2 collect-batch`

It also prepared the full high+medium queue for `gpt-5.4-mini`:

| queue | rows |
|:--|--:|
| high | 34,540 |
| medium | 271,691 |
| total | 306,231 |

The 306,231 requests were split into 9 Batch JSONL files under `data/batch/`.
`data/batch/` is gitignored and is kept local because the request/output files are large.

The same commit also fixed the object-graph pseudo-node issue:

- object graph nodes now come from real object candidates only
- category names such as `unknown`, `method`, `model`, `metric`, and `software_or_tool`
  are not allowed as graph nodes
- pilot strict object graph changed from `58 nodes / 657 edges` to `30 nodes / 345 edges`
- pseudo nodes after filtering: `[]`

## Batch Run Status

The submitted Batch run completed successfully at the API request layer:

| metric | value |
|:--|--:|
| submitted batch files | 9 |
| requested rows | 306,231 |
| completed requests reported by Batch API | 306,231 |
| failed requests reported by Batch API | 0 |
| downloaded output lines | 306,230 |
| missing output rows recorded locally | 1 |

One request, `ctxr_782024847895d6125cd5`, was reported complete by the Batch API but
was not present in the downloaded output JSONL. The collector records this as a local
failed row with `missing_batch_output`.

## Local Evidence Validation Result

The model returned structured responses for nearly all requests, but the local project
validators remain intentionally strict. They require grounded evidence spans and cue
consistency before accepting a non-abstain label.

| metric | value |
|:--|--:|
| processed rows | 306,231 |
| locally accepted Phase-2 rows before revalidation | 236,755 |
| local failed rows | 69,476 |
| local validation success rate | 77.31% |
| local validation failure rate | 22.69% |
| abstain labels among valid rows | 1,598 |
| Phase-1 / Phase-2 disagreement rate among valid rows | 25.29% |

Outputs:

- `data/processed/phase2_structured_labels_batch.parquet`
- `data/processed/phase2_structured_labels_batch_failed.jsonl`
- `reports/phase2_batch_run_report.md`

## Token And Cost

The full downloaded Batch output contains:

| token type | tokens |
|:--|--:|
| input tokens | 311,199,755 |
| output tokens | 65,632,936 |
| total tokens | 376,832,691 |

Using the local configured `gpt-5.4-mini` Batch rates, the estimated actual cost is
`$264.37`.

## Valid Label Distribution

| final_intent | rows |
|:--|--:|
| background | 145,978 |
| uses | 50,493 |
| compares_against | 27,355 |
| critiques | 6,410 |
| extends | 4,768 |
| applies | 1,152 |
| unclear | 599 |

| final_object_type | rows |
|:--|--:|
| method | 72,960 |
| model | 59,017 |
| dataset_or_database | 29,979 |
| metric | 24,462 |
| benchmark_or_protocol | 12,731 |
| software_or_tool | 11,188 |
| unknown | 7,877 |
| task | 7,209 |
| theory_or_concept | 5,784 |
| claim_or_finding | 5,548 |

## Failed Row Distribution

| failure category | rows |
|:--|--:|
| evidence_span_not_substring | 25,311 |
| use_cue_not_accepted | 20,648 |
| quote_not_substring | 10,058 |
| compare_cue_not_accepted | 4,902 |
| extend_cue_not_accepted | 2,099 |
| schema_error | 1,798 |
| cited_title_only_object_rejected | 1,609 |
| other | 1,287 |
| critique_cue_not_accepted | 1,180 |
| apply_cue_not_accepted | 584 |

These failed rows are not API failures. They are rows that did not pass the local
evidence-grounding policy and should be treated as rejected or retry candidates.

## Full Batch QA/Revalidation

Task 10C adds a full Batch failed-row diagnostic pass and a conservative local
revalidation pass. It only recovers rows whose previous failure was an intent-specific
cue validator and whose raw model output still passes exact evidence-span validation,
exact quote validation, evidence_supports_label consistency, and the cited-title-only
object safeguard.

| metric | value |
|:--|--:|
| original successful rows | 236,755 |
| original failed rows | 69,476 |
| locally revalidated rows | 942 |
| remaining failed rows | 68,534 |
| final successful rows | 237,697 |
| final success rate | 77.62% |
| retry manifest rows | 1,799 |

Recovered rows by failure category:

| failure category | recovered rows |
|:--|--:|
| use_cue_not_accepted | 511 |
| compare_cue_not_accepted | 255 |
| extend_cue_not_accepted | 153 |
| critique_cue_not_accepted | 23 |

The generated retry manifest targets only `schema_error`, `api_error`, and
`missing_batch_output` rows. It is prepared locally at
`data/batch/phase2_retry_batch_manifest.json` and has not been submitted.

Outputs:

- `data/processed/phase2_structured_labels_batch_revalidated.parquet`
- `data/processed/phase2_structured_labels_batch_failed_after_revalidation.jsonl`
- `data/processed/phase2_batch_failed_validation_diagnostics.parquet`
- `reports/phase2_batch_failed_validation_diagnostics.md`
- `reports/phase2_batch_revalidated_report.md`

## Final Analysis-Ready Phase-2 Labels

Task 10C.1 defines the final downstream-analysis table. It filters the 237,697
revalidated rows to non-abstain, evidence-supported, confidence >= 0.7, non-unclear
labels whose evidence span is an exact substring of the citation sentence or context
window.

| metric | value |
|:--|--:|
| total Batch requested rows | 306,231 |
| revalidated rows | 237,697 |
| analysis-ready rows | 229,751 |
| excluded revalidated rows | 7,946 |
| remaining failed rows | 68,534 |
| final effective success rate | 75.03% |
| duplicate context_id after filtering | 0 |
| ungrounded evidence spans after filtering | 0 |

Excluded rows by reason:

| exclusion reason | rows |
|:--|--:|
| low_confidence | 6,317 |
| evidence_supports_label_false | 1,094 |
| evidence_supports_label_unclear | 476 |
| final_intent_unclear | 31 |
| abstain_true | 28 |

Final downstream table:

- `data/processed/phase2_batch_analysis_ready_labels.parquet`
- `data/processed/phase2_batch_excluded_labels.parquet`
- `reports/phase2_batch_analysis_ready_audit.md`

## Updated Full Evidence-Backed Object Graph

After replacing the 582-row pilot labels with the final analysis-ready Batch labels, the strict
object graph expanded substantially:

| metric | pilot after pseudo-node fix | full Batch analysis-ready labels |
|:--|--:|--:|
| strict object nodes | 30 | 33 |
| strict object edges | 345 | 193,287 |
| pseudo nodes | 0 | 0 |

Top strict evidence-backed object nodes:

| object | type | evidence-backed edges |
|:--|:--|--:|
| BERT | model | 27,380 |
| LSTM | model | 18,200 |
| BLEU | metric | 15,991 |
| Transformer | model | 14,137 |
| CRF | method | 12,733 |
| WordNet | dataset_or_database | 12,086 |
| seq2seq | model | 8,669 |
| attention mechanism | method | 8,513 |
| SemEval | benchmark_or_protocol | 8,306 |
| HMM | method | 5,912 |

The full edge CSV is large and is kept as a local audit artifact. Reports,
figures, source data, node tables, and evidence cards are regenerated from the final
analysis-ready labels.

## Interpretation

The project has moved from a 582-label pilot to a large evidence-backed Phase-2
dataset with 229,751 final analysis-ready labels. The difference matters:
the previous figures were a prototype over a small validated sample, while the current
figures are grounded in the full high+medium LLM candidate set after strict local
evidence validation.

The 22.69% local failure rate is useful rather than alarming: it shows the guardrails
are rejecting labels whose evidence span, quote fields, or intent cues do not satisfy
the project rules. For a course paper, the cleanest claim is:

> We generated 306,231 model-assisted structured citation-function responses through
> Batch API and retained 229,751 analysis-ready Phase-2 labels after exact-span,
> local policy validation, conservative failed-row revalidation, and final
> evidence-supported filtering.
