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

Labeling, object registry construction, LLM labeling, and final aggregation are not implemented yet.

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

`citeevidence contexts extract` also defaults to no bibliography. Use `--use-bibliography --references PATH` only with a true local bibliography table. The current `data/interim/acl_references.parquet` is kept for backward compatibility, but it is not authoritative for ACL-OCL citation attribution.

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

Do not commit raw PDFs, full corpora, XML dumps, API keys, local absolute paths, or large generated files. The repository commits code and bounded markdown reports; raw corpora and large generated Parquet outputs stay local.
