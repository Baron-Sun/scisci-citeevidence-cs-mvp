# SciSci-CiteEvidence CS MVP - AGENTS.md

## Project goal
Build a course-scale evidence-grounded citation function analysis pipeline for NLP / Computational Linguistics papers.

The project is a pilot of a broader SciSciNet-scale citation semantics framework. The course project focuses on citation context evidence, not full SciSciNet coverage.

## Core principle
Do not assign strong citation-function labels without citation context evidence from the citing paper.

## Data sources
Primary:
- ACL-OCL / ACL Anthology-derived full text for large-scale citation context extraction.
- MultiCite and SciCite for labeled citation-intent references.

Optional:
- unarXive open subset after the main pipeline works.

## Data safety
- Do not commit raw PDFs.
- Do not commit large raw corpora.
- Do not commit API keys.
- Store only bounded citation context windows and derived outputs.
- Preserve source dataset and license metadata where available.

## Evidence rules
- evidence_span must be an exact substring of context_window_s3 or context_window_paragraph.
- If evidence is insufficient, set abstain=True.
- Grouped citations must be marked as multi_citation_group and cannot receive high-confidence single-reference labels unless disambiguated.
- Every structured evidence record must preserve context_id.

## Label taxonomy
Intent:
- background
- uses
- compares_against
- extends
- critiques
- applies

Object type:
- method
- dataset_or_database
- software_or_tool
- benchmark_or_protocol
- metric
- claim_or_finding
- theory_or_concept

Method edge type:
- extends
- improves
- replaces
- adapts
- uses_component
- compares
- background
- not_method_related

## Engineering rules
- Use Python 3.11+.
- Use Pydantic schemas for structured records.
- Use Parquet for processed data.
- Every CLI command must have --help.
- Every parser, labeler, validator, and aggregator must have tests.
- Core logic belongs in src/citeevidence, not notebooks.
- Figures must be reproducible from CLI commands.

## Required checks
Before completing a task, run:
- ruff check
- pytest

## Review guidelines
Flag as high priority:
- labels without valid evidence_span
- grouped citations receiving high confidence
- raw full text or PDFs committed to repo
- missing tests
- nondeterministic context_id
- hidden API keys or local absolute paths
