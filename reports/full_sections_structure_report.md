# ACL-OCL Full-Sections Structure Report

## Source Availability
| source | available | path | bytes | files | samples |
| --- | --- | --- | --- | --- | --- |
| full_sections_pkl | True | data/raw/acl_ocl/acl-publication-info.74k.v2.full-sections.pkl | 1436448852 | unavailable | unavailable |
| Full_text_JSON.tar.gz | False | data/raw/acl_ocl/Full_text_JSON.tar.gz | unavailable | unavailable | unavailable |
| GROBID / TEI XML | False | unavailable | unavailable | 0 |  |

## Pickle Object
| metric | value |
| --- | --- |
| object_type | pandas.core.frame.DataFrame |
| shape | 67732 26 |
| raw_dir | data/raw/acl_ocl |

## Top-Level Columns / Keys
| columns | keys |
| --- | --- |
| acl_id; abstract; full_text; corpus_paper_id; pdf_hash; numcitedby; url; publisher; address; year; month; booktitle; author; title; pages; doi; number; volum... |  |

## Sample Records
| record |
| --- |
| {"abstract": "Thread disentanglement is the task of separating out conversations whose thread structure is implicit, distorted, or lost. In this paper, we pe... |
| {"abstract": "In this paper, we describe a word alignment algorithm for English-Hindi parallel data. The system was developed to participate in the shared ta... |
| {"abstract": "The paper 1 presents a rule-based approach to semantic relation recognition within the Polish noun phrase. A set of semantic relations, includi... |

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

## Normalization Note
`Experiments and Results` is normalized to `experiment`; the parser uses explicit section headings only and does not infer headings from paragraph content.
