# SciSci-CiteEvidence CS MVP

Course-scale, data-rich, evidence-grounded citation function analysis for NLP and Computational Linguistics papers.

This repository is a scaffold for a pilot of a broader SciSciNet-scale citation semantics framework. The MVP focuses on citation context evidence from citing papers and deliberately avoids assigning strong citation-function labels without evidence.

## Status

Active course MVP pipeline. Implemented pieces include:

- validated project and label config loading
- MultiCite / SciCite labeled-context normalization
- ACL-OCL schema, ID, and full-sections inspection
- aligned ACL-to-ACL citation graph construction from `acl_onlygraph`
- bounded citation-context extraction from parsed ACL paragraphs
- pre-resolution marker extraction that does not trust `acl_references.parquet`
- author-year marker resolution pilot and full section-aware resolution against the aligned graph
- context quality, ID mapping, full-citations coverage, and section-normalization audit reports
- manual resolution review ingestion
- full analysis-ready strong citation contexts
- seed NLP object registry and full object mention matching
- object matching LLM-as-judge audit and review-policy application
- full Phase-1 citation-function screening and LLM queue construction
- Phase-1 LLM-as-judge audit
- Phase-2 LLM structured evidence extraction pilot
- Phase-2 failed-row diagnostics and conservative local revalidation
- Phase-2 pilot analysis report, case-study tables, and reproducible figures
- SciSci-style full-data candidate analysis over the full Phase-1/object-match outputs
- evidence-backed object-use mini graph from strict Phase-2 labels

The current Phase-2 pilot has 582 valid model-assisted structured evidence labels and 18 remaining failed rows after revalidation. Phase-2 labels are evidence-grounded, schema-validated LLM-assisted labels; they are not human gold annotations.

Not yet complete:

- course report and slides

## Requirements

- Python 3.11+

## Quickstart

```bash
pip install -e .
citeevidence --help
pytest
ruff check
```

## Reproduce Current Pipeline

The large raw and generated Parquet files are local-only and ignored by git. The commands below assume the ACL-OCL, MultiCite, and SciCite files have already been downloaded into `data/raw/`.

```bash
citeevidence datasets load-labeled \
  --multicite data/raw/multicite \
  --scicite data/raw/scicite \
  --out data/processed/labeled_contexts.parquet

citeevidence acl inspect \
  --input data/raw/acl_ocl \
  --out reports/acl_ocl_data_inspection.md

citeevidence acl parse-full-sections \
  --input data/raw/acl_ocl/acl-publication-info.74k.v2.full-sections.pkl \
  --out data/interim/acl_sections_sectioned.parquet \
  --report reports/full_sections_parse_report.md

citeevidence acl normalize-sections \
  --input data/interim/acl_sections_sectioned.parquet \
  --out data/interim/acl_sections_sectioned_normalized.parquet \
  --report reports/section_normalization_audit.md

citeevidence acl build-aligned-graph \
  --publication-info data/raw/acl_ocl/acl-publication-info.74k.v2.parquet \
  --onlygraph data/raw/acl_ocl/acl_onlygraph.parquet \
  --contexts data/processed/citation_contexts.parquet

citeevidence contexts resolve-markers \
  --contexts data/processed/citation_contexts.parquet \
  --aligned-graph data/interim/acl_citation_graph_aligned.parquet \
  --crosswalk data/interim/acl_id_crosswalk.parquet \
  --limit 100000
```

For new section-aware extraction, use the pre-resolution path:

```bash
citeevidence contexts extract-sectioned \
  --sections data/interim/acl_sections_sectioned_normalized.parquet \
  --out data/processed/citation_contexts_sectioned.parquet \
  --report reports/citation_contexts_sectioned_extraction_report.md

citeevidence contexts resolve-markers \
  --contexts data/processed/citation_contexts_sectioned.parquet \
  --aligned-graph data/interim/acl_citation_graph_aligned.parquet \
  --crosswalk data/interim/acl_id_crosswalk.parquet \
  --out data/processed/citation_contexts_sectioned_resolved_pilot.parquet \
  --failures data/processed/citation_marker_resolution_sectioned_pilot_failures.parquet \
  --report reports/citation_marker_resolution_sectioned_pilot_report.md \
  --limit 100000
```

For full section-aware resolution, omit `--limit`:

```bash
citeevidence contexts resolve-markers \
  --contexts data/processed/citation_contexts_sectioned.parquet \
  --aligned-graph data/interim/acl_citation_graph_aligned.parquet \
  --crosswalk data/interim/acl_id_crosswalk.parquet \
  --out data/processed/citation_contexts_resolved.parquet \
  --failures data/processed/citation_marker_resolution_failures.parquet \
  --report reports/citation_marker_resolution_full_report.md
```

Audit the final resolved table and create the default strong-evidence input:

```bash
citeevidence contexts audit-final-resolved \
  --resolved data/processed/citation_contexts_resolved.parquet \
  --out reports/final_resolved_context_audit.md \
  --flags data/processed/final_resolved_context_quality_flags.parquet \
  --strong-sample data/processed/strong_resolved_contexts_sample.csv \
  --manual-sample data/processed/manual_resolution_review_sample.csv \
  --analysis-ready data/processed/analysis_ready_strong_contexts.parquet

citeevidence objects match \
  --contexts data/processed/analysis_ready_strong_contexts.parquet \
  --registry configs/object_registry_seed.yaml \
  --out data/processed/object_mentions.parquet \
  --cited-title-profiles data/processed/cited_title_object_profiles.parquet \
  --object-graph-candidates data/processed/object_graph_candidate_mentions.parquet \
  --strict-object-graph-candidates data/processed/object_graph_candidate_mentions_strict.parquet \
  --broad-object-graph-candidates data/processed/object_graph_candidate_mentions_broad.parquet \
  --review-sample data/processed/object_mentions_review_sample.csv \
  --report reports/object_matching_report.md
```

`citeevidence contexts extract` also defaults to no bibliography. Use `--use-bibliography --references PATH` only with a true local bibliography table. The current `data/interim/acl_references.parquet` is kept for backward compatibility, but it is not authoritative for ACL-OCL citation attribution.

Run full Phase-1 citation-function screening:

```bash
citeevidence phase1 screen \
  --contexts data/processed/analysis_ready_strong_contexts.parquet \
  --object-mentions data/processed/object_mentions.parquet \
  --object-graph-candidates data/processed/object_graph_candidate_mentions.parquet \
  --cited-title-profiles data/processed/cited_title_object_profiles.parquet \
  --out-candidates data/processed/phase1_citation_function_candidates.parquet \
  --out-features data/processed/phase1_context_features.parquet \
  --out-llm-high data/processed/phase1_llm_queue_high.parquet \
  --out-llm-medium data/processed/phase1_llm_queue_medium.parquet \
  --out-llm-sample data/processed/phase1_llm_queue_sample.parquet \
  --report reports/phase1_citation_function_screening_report.md \
  --refined-rules-v2
```

Omit `--limit` for the full run.

For Phase-2, generate prompts without API calls first:

```bash
citeevidence phase2 extract-structured \
  --queue data/processed/phase1_llm_queue_sample.parquet \
  --candidates data/processed/phase1_citation_function_candidates.parquet \
  --features data/processed/phase1_context_features.parquet \
  --contexts data/processed/analysis_ready_strong_contexts.parquet \
  --object-mentions data/processed/object_mentions.parquet \
  --object-graph-candidates data/processed/object_graph_candidate_mentions.parquet \
  --cited-title-profiles data/processed/cited_title_object_profiles.parquet \
  --dry-run
```

Run the Phase-2 live pilot only with `OPENAI_API_KEY` set in the environment:

```bash
citeevidence phase2 extract-structured \
  --queue data/processed/phase1_llm_queue_sample.parquet \
  --candidates data/processed/phase1_citation_function_candidates.parquet \
  --features data/processed/phase1_context_features.parquet \
  --contexts data/processed/analysis_ready_strong_contexts.parquet \
  --object-mentions data/processed/object_mentions.parquet \
  --object-graph-candidates data/processed/object_graph_candidate_mentions.parquet \
  --cited-title-profiles data/processed/cited_title_object_profiles.parquet \
  --limit 600
```

For large Phase-2 runs, prepare and submit OpenAI Batch API jobs. The workflow reads
`OPENAI_API_KEY` only from the environment; keys should never be written into commands,
files, reports, or commits. `data/batch/` is ignored by git because it contains large
request and result files.

```bash
citeevidence phase2 estimate-batch-cost \
  --queue data/processed/phase1_llm_queue_high.parquet \
  --queue data/processed/phase1_llm_queue_medium.parquet \
  --model gpt-5.4-mini \
  --out reports/phase2_batch_cost_estimate.md

citeevidence phase2 prepare-batch \
  --queue data/processed/phase1_llm_queue_high.parquet \
  --queue data/processed/phase1_llm_queue_medium.parquet \
  --model gpt-5.4-mini \
  --out-jsonl data/batch/phase2_full_batch_requests.jsonl \
  --manifest data/batch/phase2_full_batch_manifest.json \
  --skip-enrichment

citeevidence phase2 submit-batch \
  --manifest data/batch/phase2_full_batch_manifest.json \
  --status-out data/batch/phase2_full_batch_status.json

citeevidence phase2 check-batch \
  --manifest data/batch/phase2_full_batch_manifest.json \
  --status-out data/batch/phase2_full_batch_status.json

citeevidence phase2 collect-batch \
  --manifest data/batch/phase2_full_batch_manifest.json \
  --queue data/processed/phase1_llm_queue_high.parquet \
  --queue data/processed/phase1_llm_queue_medium.parquet \
  --out-labels data/processed/phase2_structured_labels_batch.parquet \
  --out-failed data/processed/phase2_structured_labels_batch_failed.jsonl \
  --report reports/phase2_batch_run_report.md
```

Before committing after any API work, run a local secret scan over staged text files:

```bash
git diff --cached --name-only | xargs grep -nE 'sk-(proj|[A-Za-z0-9])[-A-Za-z0-9_]{20,}' || true
```

Revalidate failed Phase-2 rows locally without calling the API:

```bash
citeevidence phase2 revalidate-failed \
  --labels data/processed/phase2_structured_labels_pilot.parquet \
  --failed data/processed/phase2_structured_labels_failed.jsonl \
  --queue data/processed/phase1_llm_queue_sample.parquet \
  --out-labels data/processed/phase2_structured_labels_pilot_revalidated.parquet \
  --out-failed data/processed/phase2_structured_labels_failed_after_revalidation.jsonl \
  --diagnostics data/processed/phase2_failed_validation_diagnostics.parquet \
  --diagnostics-report reports/phase2_failed_validation_diagnostics.md \
  --report reports/phase2_structured_extraction_pilot_revalidated_report.md
```

Generate the Phase-2 pilot analysis report, figures, case studies, and figure source data:

```bash
citeevidence analysis phase2-pilot \
  --labels data/processed/phase2_structured_labels_pilot_revalidated.parquet \
  --failed-diagnostics data/processed/phase2_failed_validation_diagnostics.parquet \
  --failed-jsonl data/processed/phase2_structured_labels_failed_after_revalidation.jsonl \
  --out-report reports/phase2_pilot_analysis_report.md \
  --out-summary data/processed/phase2_pilot_analysis_summary.csv \
  --out-case-studies data/processed/phase2_case_studies.csv \
  --out-confusion data/processed/phase2_phase1_vs_phase2_confusion.csv \
  --figures-dir figures \
  --source-data-dir figures/source_data
```

Run the deterministic full-data SciSci analysis. Full Phase-1 counts are candidate-level
signals; the Phase-2 pilot remains the evidence-backed validated sample:

```bash
citeevidence analysis scisci-full \
  --contexts data/processed/analysis_ready_strong_contexts.parquet \
  --object-mentions data/processed/object_mentions.parquet \
  --object-graph-candidates data/processed/object_graph_candidate_mentions.parquet \
  --phase1 data/processed/phase1_citation_function_candidates.parquet \
  --phase2 data/processed/phase2_structured_labels_pilot_revalidated.parquet \
  --out-report reports/scisci_full_data_analysis_report.md \
  --figures-dir figures \
  --source-data-dir figures/source_data
```

Build the strict evidence-backed object-use mini graph:

```bash
citeevidence analysis object-graph \
  --phase2 data/processed/phase2_structured_labels_pilot_revalidated.parquet \
  --object-graph-candidates data/processed/object_graph_candidate_mentions.parquet \
  --object-mentions data/processed/object_mentions.parquet \
  --phase1 data/processed/phase1_citation_function_candidates.parquet \
  --out-nodes data/processed/evidence_backed_object_graph_nodes.csv \
  --out-edges data/processed/evidence_backed_object_graph_edges.csv \
  --out-cards data/processed/evidence_cards.csv \
  --out-report reports/evidence_backed_object_graph_report.md \
  --figures-dir figures \
  --source-data-dir figures/source_data
```

## Current Key Outputs

- `data/processed/analysis_ready_strong_contexts.parquet`
- `data/processed/object_mentions.parquet`
- `data/processed/object_graph_candidate_mentions.parquet`
- `data/processed/phase1_citation_function_candidates.parquet`
- `data/processed/phase1_llm_queue_sample.parquet`
- `data/processed/phase2_structured_labels_pilot_revalidated.parquet`
- `reports/phase2_structured_extraction_pilot_revalidated_report.md`
- `reports/phase2_pilot_analysis_report.md`
- `reports/scisci_full_data_analysis_report.md`
- `reports/evidence_backed_object_graph_report.md`
- `data/processed/scisci_evidence_funnel.csv`
- `data/processed/evidence_backed_object_graph_nodes.csv`
- `data/processed/evidence_backed_object_graph_edges.csv`
- `data/processed/evidence_cards.csv`

## Project Layout

```text
configs/              Configuration files for reproducible runs
src/citeevidence/     Python package and CLI entrypoint
tests/                Unit and smoke tests
data/raw/             Local raw inputs only; not committed
data/interim/         Intermediate local outputs
data/processed/       Processed derived outputs
data/benchmark/       Benchmark fixtures and derived evaluation data
reports/              Reproducible reports
figures/              Reproducible figures
slides/               Course presentation materials
```

## Core Principle

Do not assign strong citation-function labels without citation context evidence from the citing paper.

## Safety

Do not commit raw PDFs, full corpora, XML dumps, API keys, local absolute paths, or large generated files. The repository commits code, bounded reports, and selected bounded derived outputs needed for audit; raw corpora and large local Parquet outputs stay local.
