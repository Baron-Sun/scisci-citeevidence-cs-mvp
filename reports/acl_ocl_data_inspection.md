# ACL-OCL Data Inspection

- Input directory: `data/raw/acl_ocl`
- Inventory parquet: `data/interim/acl_ocl_file_inventory.parquet`
- Total files: 14
- Total bytes: 2044677053

## Files by Extension
| extension | files |
| --- | --- |
| .lock | 4 |
| .metadata | 4 |
| .parquet | 3 |
| .pkl | 1 |
| .tag | 1 |
| none | 1 |

## Likely Formats
| likely_format | files |
| --- | --- |
| unknown | 11 |
| Parquet | 3 |

## Metadata Files
0 files look like metadata, manifest, schema, README, or license files.

## Sample File Paths
| relative_path | likely_format | size_bytes |
| --- | --- | --- |
| .cache/huggingface/.gitignore | unknown | 1 |
| .cache/huggingface/CACHEDIR.TAG | unknown | 191 |
| .cache/huggingface/download/acl-publication-info.74k.v2.full-sections.pkl.lock | unknown | 0 |
| .cache/huggingface/download/acl-publication-info.74k.v2.full-sections.pkl.metadata | unknown | 124 |
| .cache/huggingface/download/acl-publication-info.74k.v2.parquet.lock | unknown | 0 |
| .cache/huggingface/download/acl-publication-info.74k.v2.parquet.metadata | unknown | 124 |
| .cache/huggingface/download/acl_full_citations.parquet.lock | unknown | 0 |
| .cache/huggingface/download/acl_full_citations.parquet.metadata | unknown | 125 |
| .cache/huggingface/download/acl_onlygraph.parquet.lock | unknown | 0 |
| .cache/huggingface/download/acl_onlygraph.parquet.metadata | unknown | 123 |

## XML Inspection
### Root Tags
| root_tag | files |
| --- | --- |
| unavailable | 14 |

### Common XML Tags
No records available.

## JSON / JSONL Inspection
### Top-Level Keys
No records available.

## Parquet Inspection
### Columns
| column | files |
| --- | --- |
| __index_level_0__ | 2 |
| citedpaperid | 2 |
| citingpaperid | 2 |
| id | 2 |
| is_citedpaperid_acl | 2 |
| is_citingpaperid_acl | 2 |
| ENTRYTYPE | 1 |
| ID | 1 |
| abstract | 1 |
| acl_id | 1 |
| address | 1 |
| author | 1 |
| booktitle | 1 |
| corpus_paper_id | 1 |
| doi | 1 |
| editor | 1 |
| full_text | 1 |
| isbn | 1 |
| journal | 1 |
| language | 1 |
| month | 1 |
| note | 1 |
| number | 1 |
| numcitedby | 1 |
| pages | 1 |
| pdf_hash | 1 |
| publisher | 1 |
| title | 1 |
| url | 1 |
| volume | 1 |
| year | 1 |

## Content Signals
| signal | files_with_signal |
| --- | --- |
| contains_title | 1 |
| contains_year | 1 |
| contains_sections | 0 |
| contains_paragraphs | 0 |
| contains_references | 0 |
| contains_inline_citations | 0 |
