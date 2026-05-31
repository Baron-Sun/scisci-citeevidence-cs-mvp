# AGENTS.md - SciSci-CiteEvidence

## Project
SciSci-CiteEvidence is a Science-of-Science citation-context semantics project over ACL-OCL.

## Core rule
Do not assign or report strong citation-function claims without grounded citation-context evidence.

## Scientific caveats
Always preserve these caveats in reports and documentation:
- Phase-2 was run on the full high/medium Phase-1 queue, not all strong contexts.
- Final labels are LLM-assisted, schema-validated, evidence-grounded labels, not human gold annotations.
- Object graph claims are over a curated seed registry, not the full universe of NLP methods.
- Current outputs are an object-use/citation-function graph, not a completed Intern-Atlas-scale method evolution graph.
- Do not call total_strong_contexts "citation count." Call it "citation-context volume" unless true graph in-degree is joined.

## Safety and cost
- Do not call OpenAI APIs.
- Do not submit Batch jobs.
- Do not write secrets.
- Do not commit raw corpora, local Parquet dumps, API keys, or data/batch files.
- Do not commit generated large data files or large generated CSV outputs.
- Do not rerun the full pipeline unless explicitly asked.
- Prefer tests with small synthetic fixtures.

## Commands
Use these commands after code changes:
- ruff check
- pytest

If mypy is already passing or relevant to touched modules, also run:
- mypy src/citeevidence

## Style
- Keep analysis code modular.
- Prefer small pure functions over large monolithic scripts.
- Every final figure should have a source CSV.
- Every scientific figure should answer a research question, not just show a distribution.
- Every report should distinguish findings, limitations, and QA status.
