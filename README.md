# SciSci-CiteEvidence CS MVP

Course-scale, data-rich, evidence-grounded citation function analysis for NLP and Computational Linguistics papers.

This repository is a scaffold for a pilot of a broader SciSciNet-scale citation semantics framework. The MVP focuses on citation context evidence from citing papers and deliberately avoids assigning strong citation-function labels without evidence.

## Status

Initial project skeleton only. Real data parsing, labeling, validation, and aggregation logic is intentionally not implemented yet.

## Requirements

- Python 3.11+

## Quickstart

```bash
pip install -e .
citeevidence --help
pytest
ruff check
```

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

Do not commit raw PDFs, full corpora, XML dumps, API keys, local absolute paths, or large generated files.
