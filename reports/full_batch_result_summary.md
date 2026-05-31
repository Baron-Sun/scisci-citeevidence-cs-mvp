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
| valid evidence-grounded Phase-2 labels | 236,755 |
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

## Updated Full Evidence-Backed Object Graph

After replacing the 582-row pilot labels with the full valid Batch labels, the strict
object graph expanded substantially:

| metric | pilot after pseudo-node fix | full Batch valid labels |
|:--|--:|--:|
| strict object nodes | 30 | 33 |
| strict object edges | 345 | 192,350 |
| pseudo nodes | 0 | 0 |

Top strict evidence-backed object nodes:

| object | type | evidence-backed edges |
|:--|:--|--:|
| BERT | model | 27,240 |
| LSTM | model | 18,129 |
| BLEU | metric | 15,750 |
| Transformer | model | 14,082 |
| CRF | method | 12,714 |
| WordNet | dataset_or_database | 12,061 |
| seq2seq | model | 8,649 |
| attention mechanism | method | 8,486 |
| SemEval | benchmark_or_protocol | 8,294 |
| HMM | method | 5,899 |

The full edge CSV is large (`141MB`) and is kept as a local audit artifact. Reports,
figures, source data, node tables, and evidence cards are regenerated from the full
Batch-valid labels.

## Interpretation

The project has moved from a 582-label pilot to a large evidence-backed Phase-2
dataset with 236,755 locally validated structured labels. The difference matters:
the previous figures were a prototype over a small validated sample, while the current
figures are grounded in the full high+medium LLM candidate set after strict local
evidence validation.

The 22.69% local failure rate is useful rather than alarming: it shows the guardrails
are rejecting labels whose evidence span, quote fields, or intent cues do not satisfy
the project rules. For a course paper, the cleanest claim is:

> We generated 306,231 model-assisted structured citation-function responses through
> Batch API and retained 236,755 evidence-grounded Phase-2 labels after exact-span and
> local policy validation.

