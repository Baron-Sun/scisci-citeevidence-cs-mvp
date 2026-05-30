# Full Citations Candidate Coverage Report

## Inputs
| name | path |
| --- | --- |
| acl_full_citations | data/raw/acl_ocl/acl_full_citations.parquet |
| publication_info | data/raw/acl_ocl/acl-publication-info.74k.v2.parquet |
| onlygraph_aligned | data/interim/acl_citation_graph_aligned.parquet |
| citation_contexts_resolved_pilot | data/processed/citation_contexts_resolved_pilot.parquet |
| citation_contexts | data/processed/citation_contexts.parquet |

## Outputs
| name | path |
| --- | --- |
| acl_full_citations_safe_aligned | data/interim/acl_full_citations_safe_aligned.parquet |

## Candidate Source Sizes
| metric | value |
| --- | --- |
| full_citations total rows | 3812256 |
| safe full_citations rows where both endpoints map | 1339414 |
| onlygraph unique candidate edges | 669650 |
| full_citations_safe unique candidate edges | 669650 |
| union unique candidate edges | 669650 |
| safe full_citations both-endpoint rate | 0.351 |
| additional candidate edges beyond onlygraph | 0 |
| additional citing ACL papers | 0 |
| additional cited ACL papers | 0 |

Unique candidate edges are deduplicated by `(citing_acl_id, cited_acl_id)`.

## Candidate Source Distribution In Union
| candidate_source | candidate_edges |
| --- | --- |
| both | 669650 |

## Bibliography-Unresolved Author-Year Coverage
| metric | value |
| --- | --- |
| bibliography_unresolved author-year rows | 68703 |
| gain at least one same-year candidate | 0 |
| gain at least one same-year + surname candidate | 0 |
| become ambiguous due to multiple surname candidates | 0 |
| union same-year + surname candidate rows | 1165 |
| full_citations-only same-year + surname candidate rows | 0 |

## Risk Analysis
- Same-year + surname recovery rate among unresolved author-year rows: 0.000
- New ambiguity rate among unresolved author-year rows: 0.000
- The safe full-citations subset does not recover same-year + surname candidates in this pilot, so it should not be promoted.

## Sample Additional Safe Full-Citation Edges
No records available.

## Sample Rows Gaining Same-Year + Surname Candidates
No records available.

## Sample Rows Becoming Ambiguous
No records available.

## Recommendation
Do not use `acl_full_citations` for final resolution. In this safe aligned subset, all unique ACL-to-ACL candidate pairs are already present in `acl_onlygraph`, so it adds no reviewed coverage for the current pilot.
