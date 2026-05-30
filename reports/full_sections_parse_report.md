# ACL-OCL Full-Sections Parse Report

## Inputs / Outputs
| name | path | status |
| --- | --- | --- |
| input | data/raw/acl_ocl/acl-publication-info.74k.v2.full-sections.pkl | read |
| acl_sections_sectioned | data/interim/acl_sections_sectioned.parquet | written |
| citation_contexts_sectioned_sample | data/processed/citation_contexts_sectioned_sample.parquet | written |

## Pickle Object
| metric | value |
| --- | --- |
| object_type | pandas.core.frame.DataFrame |
| shape | 67732 26 |

## Recoverable Signals
| signal | present |
| --- | --- |
| acl_id | True |
| section title | True |
| paragraph text | True |
| paragraph order | True |
| citation markers | True |

## Section Metrics
| metric | value |
| --- | --- |
| input records | 67732 |
| papers with acl_id | 67732 |
| papers with section data | 66321 |
| papers with citation markers | 64408 |
| recoverable section / paragraph rows | 3240481 |
| section name non-empty rate | 0.948 |

## Normalized Section Distribution
| normalized_section | paragraph_rows |
| --- | --- |
| unknown | 1977096 |
| introduction | 308365 |
| model | 163291 |
| results | 132730 |
| conclusion | 115095 |
| method | 114716 |
| experiment | 109192 |
| related_work | 88770 |
| evaluation | 83736 |
| abstract | 66857 |
| discussion | 40893 |
| background | 25769 |
| references | 10260 |
| appendix | 3711 |

## Sample Context Extraction
| status | path | section_rows_sampled | context_rows |
| --- | --- | --- | --- |
| written | data/processed/citation_contexts_sectioned_sample.parquet | 10000 | 5064 |

## Normalization Note
`Experiments and Results` is normalized to `experiment`; section names are taken from explicit full-sections metadata, not inferred from paragraph text.
