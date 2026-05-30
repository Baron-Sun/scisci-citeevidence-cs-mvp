# ACL-OCL Schema and ID Mapping Audit

## Executive Summary
- Publication metadata contains exact `acl_id`: True
- Publication metadata contains exact `corpus_paper_id`: True
- Publication metadata contains both exact crosswalk columns: True
- Authoritative crosswalk: `data/raw/acl_ocl/acl-publication-info.74k.v2.parquet`
- Best citing mapping: `citingpaperid` -> `acl_id`
- Best cited mapping: `citedpaperid` -> `acl_id`

## Inputs
| name | path |
| --- | --- |
| publication_info | data/raw/acl_ocl/acl-publication-info.74k.v2.parquet |
| acl_full_citations | data/raw/acl_ocl/acl_full_citations.parquet |
| acl_onlygraph | data/raw/acl_ocl/acl_onlygraph.parquet |
| acl_papers | data/interim/acl_papers.parquet |
| acl_references | data/interim/acl_references.parquet |
| acl_sections | data/interim/acl_sections.parquet |
| citation_contexts | data/processed/citation_contexts.parquet |

## Publication Crosswalk Check
| acl_column | numeric_column | exact_column_check | rows | unique_acl_ids | unique_numeric_ids |
| --- | --- | --- | --- | --- | --- |
| acl_id | corpus_paper_id | {"acl_id": true, "corpus_paper_id": true, "both_present": true} | 73285 | 73285 | 73284 |

## Candidate ACL ID Columns
| file | column | dtype | sample_checked | acl_id_match_rate | integer_like_rate | sample_unique_values | examples |
| --- | --- | --- | --- | --- | --- | --- | --- |
| publication_info | acl_id | string | 50000 | 0.705 | 0.000 | 50000 | O02-2002; L02-1310; R13-1042; W05-0819; L02-1309 |
| publication_info | url | string | 50000 | 0.618 | 0.000 | 50000 | https://aclanthology.org/O02-2002; http://www.lrec-conf.org/proceedings/lrec2002/pdf/310.pdf; https://aclanthology.org/R13-1042; https://aclanthology.org/W05-0819; http://www.lrec-conf.org/proceedings/lrec2002/pdf/309.pdf |
| acl_papers | paper_id | string | 50000 | 0.705 | 0.000 | 50000 | acl_bdbb15b79d8ca2d2; acl_793271a60e45b250; acl_059ac990dc28667c; acl_697184fa5f81f4e6; acl_5bef37e9330a1633 |
| acl_sections | paper_id | string | 50000 | 0.682 | 0.000 | 50000 | O02-2002; R13-1042; W05-0819; R13-1044; W05-0818 |
| citation_contexts | citing_paper_id | string | 50000 | 0.654 | 0.000 | 1907 | R13-1042; R13-1042; R13-1042; R13-1042; R13-1042 |

## Candidate Numeric Paper ID Columns
| file | column | dtype | sample_checked | acl_id_match_rate | integer_like_rate | sample_unique_values | examples |
| --- | --- | --- | --- | --- | --- | --- | --- |
| publication_info | corpus_paper_id | int64 | 50000 | 0.000 | 1.000 | 50000 | 18022704; 8220988; 16703040; 1215281; 18078432 |
| acl_full_citations | id | int64 | 50000 | 0.000 | 1.000 | 50000 | 868703600; 3216252045; 437616166; 3349792001; 3313665988 |
| acl_full_citations | citingpaperid | int64 | 50000 | 0.000 | 1.000 | 42529 | 52046747; 229723601; 16841192; 235196103; 233365331 |
| acl_full_citations | citedpaperid | int64 | 50000 | 0.000 | 1.000 | 17605 | 16228715; 1373518; 629094; 19121210; 218974137 |
| acl_full_citations | __index_level_0__ | int64 | 50000 | 0.000 | 1.000 | 50000 | 0; 1; 2; 3; 4 |
| acl_onlygraph | id | int64 | 50000 | 0.000 | 1.000 | 50000 | 3313665988; 244015897; 2084450101; 504040985; 63101789 |
| acl_onlygraph | citingpaperid | int64 | 50000 | 0.000 | 1.000 | 29264 | 233365331; 3841628; 218974058; 53242563; 1009868 |
| acl_onlygraph | citedpaperid | int64 | 50000 | 0.000 | 1.000 | 17730 | 218974137; 18998986; 204896994; 15453873; 680757 |
| acl_onlygraph | __index_level_0__ | int64 | 50000 | 0.000 | 1.000 | 50000 | 4; 5; 8; 12; 14 |
| acl_references | citing_paper_id | string | 50000 | 0.000 | 1.000 | 42529 | 52046747; 229723601; 16841192; 235196103; 233365331 |
| acl_references | reference_key | string | 50000 | 0.000 | 1.000 | 50000 | 868703600; 3216252045; 437616166; 3349792001; 3313665988 |
| acl_references | raw_reference | string | 50000 | 0.000 | 1.000 | 17605 | 16228715; 1373518; 629094; 19121210; 218974137 |

## Reference Overlap Checks
| file | column | target | unique_values | overlap_count | overlap_rate |
| --- | --- | --- | --- | --- | --- |
| acl_references | citing_paper_id | publication corpus_paper_id | 447712 | 66386 | 0.148 |
| acl_references | reference_key | publication corpus_paper_id | 3142549 | 133 | 0.000 |
| acl_references | raw_reference | publication corpus_paper_id | 267127 | 59783 | 0.224 |

## Section and Context ACL ID Checks
| file | column | target | unique_values | overlap_count | overlap_rate |
| --- | --- | --- | --- | --- | --- |
| acl_sections.parquet | paper_id | publication acl_id | 67414 | 67414 | 1.000 |
| citation_contexts.parquet | citing_paper_id | publication acl_id | 62671 | 62671 | 1.000 |

## Graph Overlap Checks
### acl_full_citations
| file | column | target | unique_values | overlap_count | overlap_rate |
| --- | --- | --- | --- | --- | --- |
| acl_full_citations.parquet | id | publication corpus_paper_id | 3142549 | 133 | 0.000 |
| acl_full_citations.parquet | citingpaperid | publication corpus_paper_id | 447712 | 66386 | 0.148 |
| acl_full_citations.parquet | citedpaperid | publication corpus_paper_id | 267127 | 59783 | 0.224 |
| acl_full_citations.parquet | __index_level_0__ | publication corpus_paper_id | 2344725 | 7640 | 0.003 |

### acl_onlygraph
| file | column | target | unique_values | overlap_count | overlap_rate |
| --- | --- | --- | --- | --- | --- |
| acl_onlygraph.parquet | id | publication corpus_paper_id | 669707 | 39 | 0.000 |
| acl_onlygraph.parquet | citingpaperid | publication corpus_paper_id | 60997 | 60997 | 1.000 |
| acl_onlygraph.parquet | citedpaperid | publication corpus_paper_id | 48300 | 48300 | 1.000 |
| acl_onlygraph.parquet | __index_level_0__ | publication corpus_paper_id | 1150402 | 3840 | 0.003 |

## Successful Candidate Joins
| graph_file | id | citing_numeric_id | citing_acl_id | citing_year | citing_title | cited_numeric_id | cited_acl_id | cited_year | cited_title |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| acl_onlygraph | 3313665988 | 233365331 | 2021.vardial-1.12 | 2021 | Comparing the Performance of {CNN}s and Shallow Models for Language Identification | 218974137 | 2020.sltu-1.25 | 2020 | A Sentiment Analysis Dataset for Code-Mixed {M}alayalam-{E}nglish |
| acl_onlygraph | 244015897 | 3841628 | U17-1003 | 2017 | Joint Sentence-Document Model for Manifesto Text Analysis | 18998986 | I11-1019 | 2011 | Keyphrase Extraction from Online News Using Binary Integer Programming |
| acl_onlygraph | 2084450101 | 218974058 | 2020.lrec-1.393 | 2020 | {OF}r{L}ex: A Computational Morphological and Syntactic Lexicon for {O}ld {F}rench | 204896994 | W19-7816 | 2019 | Challenges of language change and variation: towards an extended treebank of Medieval {F}rench |
| acl_onlygraph | 504040985 | 53242563 | W18-6453 | 2018 | Findings of the {WMT} 2018 Shared Task on Parallel Corpus Filtering | 15453873 | L12-1246 | 2012 | Parallel Data, Tools and Interfaces in {OPUS} |
| acl_onlygraph | 63101789 | 1009868 | W13-2201 | 2013 | Findings of the 2013 {W}orkshop on {S}tatistical {M}achine {T}ranslation | 680757 | P10-2016 | 2010 | Tackling Sparse Data Issue in Machine Translation Evaluation |
| acl_onlygraph | 1562532567 | 196173298 | W19-5904 | 2019 | Few-Shot Dialogue Generation Without Annotated Data: A Transfer Learning Approach | 52967399 | N19-1423 | 2019 | {BERT}: Pre-training of Deep Bidirectional Transformers for Language Understanding |
| acl_onlygraph | 3521563751 | 229376920 | 2022.cl-1.6 | 2022 | Deep Learning for Text Style Transfer: A Survey | 52068673 | D18-1138 | 2018 | Learning Sentiment Memories for Sentiment Modification without Parallel Data |
| acl_onlygraph | 8311199 | 30276928 | L16-1533 | 2016 | Government Domain Named Entity Recognition for {S}outh {A}frican Languages | 2894113 | L14-1106 | 2014 | Developing Text Resources for Ten {S}outh {A}frican Languages |
| acl_onlygraph | 321747530 | 9302891 | R09-1028 | 2009 | Topic-based Multi-Document Summarization with Probabilistic Latent Semantic Analysis | 8598694 | C00-1072 | 2000 | The Automated Acquisition of Topic Signatures for Text Summarization |
| acl_onlygraph | 386231268 | 13484934 | W16-2306 | 2016 | {P}ar{FDA} for Instance Selection for Statistical Machine Translation | 15435354 | S16-1117 | 2016 | {RTM} at {S}em{E}val-2016 Task 1: Predicting Semantic Similarity with Referential Translation Machines and Related Statistics |
| acl_onlygraph | 3179495017 | 227183229 | 2020.law-1.10 | 2020 | {PASTRIE}: A Corpus of Prepositions Annotated with Supersense Tags in {R}eddit International {E}nglish | 53099899 | K18-2016 | 2018 | {U}niversal {D}ependency Parsing from Scratch |
| acl_onlygraph | 3150901241 | 226262359 | 2020.emnlp-main.705 | 2020 | {C}ap{WAP}: Image Captioning with a Purpose | 52290620 | D18-1083 | 2018 | Improving Reinforcement Learning Based Image Captioning with Natural Language Prior |
| acl_onlygraph | 854677951 | 16856890 | W16-4110 | 2016 | A Preliminary Study of Statistically Predictive Syntactic Complexity Features and Manual Simplifications in {B}asque | 13603486 | W14-5604 | 2014 | The Fewer, the Better? A Contrastive Study about Ways to Simplify |
| acl_onlygraph | 24327070 | 14094341 | W17-1711 | 2017 | Discovering Light Verb Constructions and their Translations from Parallel Corpora without Word Alignment | 6049307 | D11-1077 | 2011 | Identification of Multi-word Expressions by Combining Multiple Linguistic Information Sources |
| acl_onlygraph | 1940049190 | 10096627 | F13-1033 | 2013 | A fully discriminative training framework for Statistical Machine Translation (Un cadre d{'}apprentissage int{\'e}gralement discriminant ... | 12259852 | W11-2168 | 2011 | From n-gram-based to {CRF}-based Translation Models |
| acl_onlygraph | 2083264458 | 14716985 | W10-3217 | 2010 | A Supervised Learning based Chunking in {T}hai using Categorial Grammar | 109854 | W00-0731 | 2000 | Shallow Parsing as Part-of-Speech Tagging |
| acl_onlygraph | 1187050437 | 184486746 | W19-4828 | 2019 | What Does {BERT} Look at? An Analysis of {BERT}{'}s Attention | 1114678 | P16-1162 | 2016 | Neural Machine Translation of Rare Words with Subword Units |
| acl_onlygraph | 820457544 | 15515545 | S15-2014 | 2015 | yi{G}ou: A Semantic Text Similarity Computing System Based on {SVM} | 12549805 | S12-1051 | 2012 | {S}em{E}val-2012 Task 6: A Pilot on Semantic Textual Similarity |
| acl_onlygraph | 4824975 | 10531943 | W17-4007 | 2017 | Word Transduction for Addressing the {OOV} Problem in Machine Translation for Similar Resource-Scarce Languages | 11990721 | W09-3510 | 2009 | Transliteration by Bidirectional Statistical Machine Translation |
| acl_onlygraph | 3470644076 | 237502863 | 2021.emnlp-main.1 | 2021 | {A}lig{NART}: Non-autoregressive Neural Machine Translation by Jointly Learning to Estimate Alignment and Translate | 6826069 | P07-1091 | 2007 | A Probabilistic Approach to Syntax-based Reordering for Statistical Machine Translation |

## Failed Candidate Joins
| graph_file | id | citing_numeric_id | citing_acl_id | citing_year | citing_title | cited_numeric_id | cited_acl_id | cited_year | cited_title |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| acl_full_citations | 868703600 | 52046747 | unavailable | unavailable | unavailable | 16228715 | L12-1587 | 2012 | {PET}: a Tool for Post-editing and Assessing Machine Translation |
| acl_full_citations | 3216252045 | 229723601 | unavailable | unavailable | unavailable | 1373518 | D15-1237 | 2015 | {W}iki{QA}: A Challenge Dataset for Open-Domain Question Answering |
| acl_full_citations | 437616166 | 16841192 | unavailable | unavailable | unavailable | 629094 | P10-1040 | 2010 | Word Representations: A Simple and General Method for Semi-Supervised Learning |
| acl_full_citations | 3349792001 | 235196103 | unavailable | unavailable | unavailable | 19121210 | P17-4020 | 2017 | {W}eb{C}hild 2.0 : Fine-Grained Commonsense Knowledge Distillation |
| acl_full_citations | 1834185123 | 212684412 | unavailable | unavailable | unavailable | 3626819 | N18-1202 | 2018 | Deep Contextualized Word Representations |
| acl_full_citations | 2041475843 | 201141234 | unavailable | unavailable | unavailable | 3626819 | N18-1202 | 2018 | Deep Contextualized Word Representations |
| acl_full_citations | 3173432873 | 142814013 | unavailable | unavailable | unavailable | 16684206 | L04-1026 | 2004 | Designing and Recording an Audiovisual Database of Emotional Speech in {B}asque |
| acl_full_citations | 1729983307 | 209517056 | unavailable | unavailable | unavailable | 2988106 | P10-4003 | 2010 | Beetle {II}: A System for Tutoring and Computational Linguistics Experimentation |
| acl_full_citations | 2540827620 | 64333196 | unavailable | unavailable | unavailable | 1002552 | P10-1122 | 2010 | {``}Ask Not What Textual Entailment Can Do for You...{''} |
| acl_full_citations | 3381066467 | 225862815 | unavailable | unavailable | unavailable | 12861120 | D11-1141 | 2011 | Named Entity Recognition in Tweets: An Experimental Study |
| acl_full_citations | 3319499362 | 233486429 | unavailable | unavailable | unavailable | 207556454 | Q17-1010 | 2017 | Enriching Word Vectors with Subword Information |
| acl_full_citations | 283213670 | 292331 | unavailable | unavailable | unavailable | 6247656 | L06-1225 | 2006 | {SENTIWORDNET}: A Publicly Available Lexical Resource for Opinion Mining |
| acl_full_citations | 3543188190 | 238999115 | unavailable | unavailable | unavailable | 52967399 | N19-1423 | 2019 | {BERT}: Pre-training of Deep Bidirectional Transformers for Language Understanding |
| acl_full_citations | 1269219897 | 84840080 | unavailable | unavailable | unavailable | 226239080 | 2011.eamt-1.44 | 2011 | {ATLAS} |
| acl_full_citations | 3621030204 | 244714786 | unavailable | unavailable | unavailable | 207556454 | Q17-1010 | 2017 | Enriching Word Vectors with Subword Information |
| acl_full_citations | 2970298658 | 195646530 | unavailable | unavailable | unavailable | 32954707 | C90-2036 | 1990 | A Spelling Correction Program Based on a Noisy Channel Model |
| acl_full_citations | 3135316257 | 225454150 | unavailable | unavailable | unavailable | 8894136 | W16-5605 | 2016 | Generating Politically-Relevant Event Data |
| acl_full_citations | 281912223 | 12617355 | unavailable | unavailable | unavailable | 18780207 | D07-1055 | 2007 | A Systematic Comparison of Training Criteria for Statistical Machine Translation |
| acl_full_citations | 3646485913 | 245986674 | unavailable | unavailable | unavailable | 252796 | J93-2004 | 1993 | Building a Large Annotated Corpus of {E}nglish: The {P}enn {T}reebank |
| acl_full_citations | 329428000 | 29002555 | unavailable | unavailable | unavailable | 5273348 | P05-1052 | 2005 | Extracting Relations with Integrated Information Using Kernel Methods |

## Authoritative Crosswalk Recommendation
`acl-publication-info.74k.v2.parquet` should be used as the authoritative crosswalk. It contains an ACL Anthology ID column and a numeric corpus paper ID column in the same row, so graph IDs can be mapped back to ACL IDs before citation context extraction. The current extracted contexts use ACL IDs from `acl_sections.paper_id`, while `acl_references.citing_paper_id` is numeric, which explains the bibliography-unresolved contexts.

## File Schemas and Column Profiles
### publication_info
- Path: `data/raw/acl_ocl/acl-publication-info.74k.v2.parquet`
- Shape: 73285 rows x 25 columns
- Columns: `acl_id, abstract, full_text, corpus_paper_id, pdf_hash, numcitedby, url, publisher, address, year, month, booktitle, author, title, pages, doi, number, volume, journal, editor, isbn, ENTRYTYPE, ID, language, note`

| column | dtype | non_null_rate | examples | sample_checked | acl_id_match_rate | integer_like_rate | sample_unique_values | is_acl_id_candidate | is_numeric_paper_id_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| acl_id | string | 1.000 | O02-2002; L02-1310; R13-1042; W05-0819; L02-1309 | 50000 | 0.705 | 0.000 | 50000 | True | False |
| abstract | string | 0.923 | There is a need to measure word similarity when processin...; Thread disentanglement is the task of separating out conv...; In this paper, we describe a word alignment algorithm for...; The paper 1 presents a rule-based approach to semantic re...; In this paper we describe LIHLA, a lexical aligner which ... | 50000 | 0.000 | 0.000 | 49911 | False | False |
| full_text | string | 0.920 | There is a need to measure word similarity when processin...; Thread disentanglement is the task of separating out conv...; In this paper, we describe a word alignment algorithm for...; The paper 1 presents a rule-based approach to semantic re...; In this paper we describe LIHLA, a lexical aligner which ... | 50000 | 0.001 | 0.000 | 49974 | False | False |
| corpus_paper_id | int64 | 1.000 | 18022704; 8220988; 16703040; 1215281; 18078432 | 50000 | 0.000 | 1.000 | 50000 | False | True |
| pdf_hash | string | 0.984 | 0b09178ac8d17a92f16140365363d8df88c757d0; 8d5e31610bc82c2abc86bc20ceba684c97e66024; 3eb736b17a5acb583b9a9bd99837427753632cdb; b20450f67116e59d1348fc472cfc09f96e348f55; 011e943b64a78dadc3440674419821ee080f0de3 | 50000 | 0.000 | 0.000 | 49990 | False | False |
| numcitedby | int64 | 1.000 | 14; 93; 10; 15; 12 | 50000 | 0.000 | 1.000 | 728 | False | False |
| url | string | 1.000 | https://aclanthology.org/O02-2002; http://www.lrec-conf.org/proceedings/lrec2002/pdf/310.pdf; https://aclanthology.org/R13-1042; https://aclanthology.org/W05-0819; http://www.lrec-conf.org/proceedings/lrec2002/pdf/309.pdf | 50000 | 0.618 | 0.000 | 50000 | True | False |
| publisher | string | 0.862 | European Language Resources Association (ELRA); INCOMA Ltd. Shoumen, BULGARIA; Association for Computational Linguistics; European Language Resources Association (ELRA); INCOMA Ltd. Shoumen, BULGARIA | 50000 | 0.000 | 0.000 | 111 | False | False |
| address | string | 0.902 | Las Palmas, Canary Islands - Spain; Hissar, Bulgaria; Ann Arbor, Michigan; Las Palmas, Canary Islands - Spain; Hissar, Bulgaria | 50000 | 0.000 | 0.000 | 388 | False | False |
| year | string | 1.000 | 2002; 2002; 2013; 2005; 2002 | 50000 | 0.000 | 1.000 | 59 | False | False |
| month | string | 0.900 | August; May; September; June; May | 50000 | 0.000 | 0.009 | 173 | False | False |
| booktitle | string | 0.972 | International Journal of Computational Linguistics {\&} {...; Proceedings of the Third International Conference on Lang...; Proceedings of the International Conference Recent Advanc...; Proceedings of the {ACL} Workshop on Building and Using P...; Proceedings of the Third International Conference on Lang... | 50000 | 0.000 | 0.000 | 2129 | False | False |
| author | string | 0.991 | Chen, Keh-Jiann  and You, Jia-Ming; Mihalcea, Rada F.; Jamison, Emily  and Gurevych, Iryna; Aswani, Niraj  and Gaizauskas, Robert; Suyaga, Fumiaki  and Takezawa, Toshiyuki  and Kikui, Geni... | 50000 | 0.000 | 0.000 | 43042 | False | False |
| title | string | 1.000 | A Study on Word Similarity using Context Vector Models; Bootstrapping Large Sense Tagged Corpora; Headerless, Quoteless, but not Hopeless? Using Pairwise E...; Aligning Words in {E}nglish-{H}indi Parallel Corpora; Proposal of a very-large-corpus acquisition method by cel... | 50000 | 0.000 | 0.000 | 49829 | False | False |
| pages | string | 0.812 | 37--58; 327--335; 115--118; 342--349; 111--114 | 50000 | 0.000 | 0.005 | 21679 | False | False |
| doi | string | 0.405 | 10.18653/v1/2020.emnlp-main.380; 10.18653/v1/P19-1161; 10.18653/v1/2020.nlp4convai-1.10; 10.18653/v1/2022.semeval-1.215; 10.18653/v1/W16-5615 | 29678 | 0.471 | 0.000 | 29676 | False | False |
| number | string | 0.020 | 1; 1; 4; 2; 1 | 1474 | 0.000 | 0.961 | 6 | False | False |
| volume | string | 0.025 | 30; 12; 43; 9; 22 | 1840 | 0.000 | 1.000 | 48 | False | False |
| journal | string | 0.028 | American Journal of Computational Linguistics; Computational Linguistics; Computational Linguistics; Computational Linguistics; Transactions of the Association for Computational Linguis... | 2037 | 0.000 | 0.000 | 3 | False | False |
| editor | string | 0.000 | Waller, Annalu; Somers, Harold  and McGee Wood, Mary; Hays, David G.  and Mathias, J.; Waltz, David L.; Waltz, David L. | 13 | 0.000 | 0.000 | 7 | False | False |
| isbn | string | 0.019 | 979-10-95546-34-4; 979-10-95546-70-2; 979-10-95546-46-7; 979-10-95546-34-4; 979-10-95546-57-3 | 1370 | 0.000 | 0.000 | 37 | False | False |
| ENTRYTYPE | string | 1.000 | inproceedings; inproceedings; inproceedings; inproceedings; inproceedings | 50000 | 0.000 | 0.000 | 3 | False | False |
| ID | string | 1.000 | chen-you-2002-study; mihalcea-2002-bootstrapping; jamison-gurevych-2013-headerless; aswani-gaizauskas-2005-aligning; suyaga-etal-2002-proposal | 50000 | 0.000 | 0.000 | 50000 | False | False |
| language | string | 0.041 | English; French; English; English; English | 3020 | 0.000 | 0.000 | 5 | False | False |
| note | string | 0.003 | Microfiche 77; Microfiche 17; Microfiche 32; Microfiche 78; Microfiche 79 | 197 | 0.000 | 0.000 | 83 | False | False |

### acl_full_citations
- Path: `data/raw/acl_ocl/acl_full_citations.parquet`
- Shape: 3812256 rows x 6 columns
- Columns: `id, citingpaperid, citedpaperid, is_citedpaperid_acl, is_citingpaperid_acl, __index_level_0__`

| column | dtype | non_null_rate | examples | sample_checked | acl_id_match_rate | integer_like_rate | sample_unique_values | is_acl_id_candidate | is_numeric_paper_id_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| id | int64 | 1.000 | 868703600; 3216252045; 437616166; 3349792001; 3313665988 | 50000 | 0.000 | 1.000 | 50000 | False | True |
| citingpaperid | int64 | 1.000 | 52046747; 229723601; 16841192; 235196103; 233365331 | 50000 | 0.000 | 1.000 | 42529 | False | True |
| citedpaperid | int64 | 1.000 | 16228715; 1373518; 629094; 19121210; 218974137 | 50000 | 0.000 | 1.000 | 17605 | False | True |
| is_citedpaperid_acl | bool | 1.000 | True; True; True; True; True | 50000 | 0.000 | 0.000 | 1 | False | False |
| is_citingpaperid_acl | bool | 1.000 | False; False; False; False; True | 50000 | 0.000 | 0.000 | 2 | False | False |
| __index_level_0__ | int64 | 1.000 | 0; 1; 2; 3; 4 | 50000 | 0.000 | 1.000 | 50000 | False | True |

### acl_onlygraph
- Path: `data/raw/acl_ocl/acl_onlygraph.parquet`
- Shape: 1339414 rows x 6 columns
- Columns: `id, citingpaperid, citedpaperid, is_citedpaperid_acl, is_citingpaperid_acl, __index_level_0__`

| column | dtype | non_null_rate | examples | sample_checked | acl_id_match_rate | integer_like_rate | sample_unique_values | is_acl_id_candidate | is_numeric_paper_id_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| id | int64 | 1.000 | 3313665988; 244015897; 2084450101; 504040985; 63101789 | 50000 | 0.000 | 1.000 | 50000 | False | True |
| citingpaperid | int64 | 1.000 | 233365331; 3841628; 218974058; 53242563; 1009868 | 50000 | 0.000 | 1.000 | 29264 | False | True |
| citedpaperid | int64 | 1.000 | 218974137; 18998986; 204896994; 15453873; 680757 | 50000 | 0.000 | 1.000 | 17730 | False | True |
| is_citedpaperid_acl | bool | 1.000 | True; True; True; True; True | 50000 | 0.000 | 0.000 | 1 | False | False |
| is_citingpaperid_acl | bool | 1.000 | True; True; True; True; True | 50000 | 0.000 | 0.000 | 1 | False | False |
| __index_level_0__ | int64 | 1.000 | 4; 5; 8; 12; 14 | 50000 | 0.000 | 1.000 | 50000 | False | True |

### acl_papers
- Path: `data/interim/acl_papers.parquet`
- Shape: 73296 rows x 8 columns
- Columns: `paper_id, title, year, venue, doi_or_acl_id, source_file, parse_status, parse_error`

| column | dtype | non_null_rate | examples | sample_checked | acl_id_match_rate | integer_like_rate | sample_unique_values | is_acl_id_candidate | is_numeric_paper_id_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| paper_id | string | 1.000 | acl_bdbb15b79d8ca2d2; acl_793271a60e45b250; acl_059ac990dc28667c; acl_697184fa5f81f4e6; acl_5bef37e9330a1633 | 50000 | 0.705 | 0.000 | 50000 | True | False |
| title | string | 1.000 | A Study on Word Similarity using Context Vector Models; Bootstrapping Large Sense Tagged Corpora; Headerless, Quoteless, but not Hopeless? Using Pairwise E...; Aligning Words in {E}nglish-{H}indi Parallel Corpora; Proposal of a very-large-corpus acquisition method by cel... | 50000 | 0.000 | 0.000 | 49829 | False | False |
| year | double | 1.000 | 2002.0; 2002.0; 2013.0; 2005.0; 2002.0 | 50000 | 0.000 | 1.000 | 59 | False | False |
| venue | string | 0.972 | International Journal of Computational Linguistics {\&} {...; Proceedings of the Third International Conference on Lang...; Proceedings of the International Conference Recent Advanc...; Proceedings of the {ACL} Workshop on Building and Using P...; Proceedings of the Third International Conference on Lang... | 50000 | 0.000 | 0.000 | 2129 | False | False |
| doi_or_acl_id | string | 0.405 | 10.18653/v1/2020.emnlp-main.380; 10.18653/v1/P19-1161; 10.18653/v1/2020.nlp4convai-1.10; 10.18653/v1/2022.semeval-1.215; 10.18653/v1/W16-5615 | 29678 | 0.471 | 0.000 | 29676 | False | False |
| source_file | string | 1.000 | .cache/huggingface/.gitignore; .cache/huggingface/CACHEDIR.TAG; .cache/huggingface/download/acl-publication-info.74k.v2.f...; .cache/huggingface/download/acl-publication-info.74k.v2.f...; .cache/huggingface/download/acl-publication-info.74k.v2.p... | 50000 | 0.000 | 0.000 | 12 | False | False |
| parse_status | string | 1.000 | unsupported; unsupported; unsupported; unsupported; unsupported | 50000 | 0.000 | 0.000 | 2 | False | False |
| parse_error | string | 0.000 | Unsupported file extension:; Unsupported file extension: .tag; Unsupported file extension: .lock; Unsupported file extension: .metadata; Unsupported file extension: .lock | 11 | 0.000 | 0.000 | 5 | False | False |

### acl_references
- Path: `data/interim/acl_references.parquet`
- Shape: 5151670 rows x 7 columns
- Columns: `citing_paper_id, reference_key, cited_title, cited_year, cited_authors, cited_doi, raw_reference`

| column | dtype | non_null_rate | examples | sample_checked | acl_id_match_rate | integer_like_rate | sample_unique_values | is_acl_id_candidate | is_numeric_paper_id_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| citing_paper_id | string | 1.000 | 52046747; 229723601; 16841192; 235196103; 233365331 | 50000 | 0.000 | 1.000 | 42529 | False | True |
| reference_key | string | 1.000 | 868703600; 3216252045; 437616166; 3349792001; 3313665988 | 50000 | 0.000 | 1.000 | 50000 | False | True |
| cited_title | double | 0.000 |  | 0 | 0.000 | 0.000 | 0 | False | False |
| cited_year | double | 0.000 |  | 0 | 0.000 | 0.000 | 0 | False | False |
| cited_authors | double | 0.000 |  | 0 | 0.000 | 0.000 | 0 | False | False |
| cited_doi | double | 0.000 |  | 0 | 0.000 | 0.000 | 0 | False | False |
| raw_reference | string | 1.000 | 16228715; 1373518; 629094; 19121210; 218974137 | 50000 | 0.000 | 1.000 | 17605 | False | True |

### acl_sections
- Path: `data/interim/acl_sections.parquet`
- Shape: 67414 rows x 4 columns
- Columns: `paper_id, section_name, paragraph_id, paragraph_text`

| column | dtype | non_null_rate | examples | sample_checked | acl_id_match_rate | integer_like_rate | sample_unique_values | is_acl_id_candidate | is_numeric_paper_id_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| paper_id | string | 1.000 | O02-2002; R13-1042; W05-0819; R13-1044; W05-0818 | 50000 | 0.682 | 0.000 | 50000 | True | False |
| section_name | null | 0.000 |  | 0 | 0.000 | 0.000 | 0 | False | False |
| paragraph_id | string | 1.000 | O02-2002_p0; R13-1042_p0; W05-0819_p0; R13-1044_p0; W05-0818_p0 | 50000 | 0.000 | 0.000 | 50000 | False | False |
| paragraph_text | string | 1.000 | There is a need to measure word similarity when processin...; Thread disentanglement is the task of separating out conv...; In this paper, we describe a word alignment algorithm for...; The paper 1 presents a rule-based approach to semantic re...; In this paper we describe LIHLA, a lexical aligner which ... | 50000 | 0.001 | 0.000 | 49974 | False | False |

### citation_contexts
- Path: `data/processed/citation_contexts.parquet`
- Shape: 2112564 rows x 14 columns
- Columns: `context_id, citing_paper_id, reference_key, cited_title, cited_year, cited_doi, section, paragraph_id, citation_marker, sentence_text, context_window_s3, context_window_paragraph, citation_group_size, attribution_status`

| column | dtype | non_null_rate | examples | sample_checked | acl_id_match_rate | integer_like_rate | sample_unique_values | is_acl_id_candidate | is_numeric_paper_id_candidate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| context_id | string | 1.000 | ctx_49cf24ac775d09eb1025; ctx_1b8dbeb14bcb86f7e95b; ctx_7098ddac36c149ad6c4f; ctx_d92aaae0a320f5b57d2b; ctx_1644879268ac4613e866 | 50000 | 0.000 | 0.000 | 49999 | False | False |
| citing_paper_id | string | 1.000 | R13-1042; R13-1042; R13-1042; R13-1042; R13-1042 | 50000 | 0.654 | 0.000 | 1907 | True | False |
| reference_key | string | 1.000 | unresolved_7d12ba56e9f8; unresolved_f04e10ac0205; unresolved_b0ba75106da6; unresolved_8d72fccd9b83; unresolved_50512fbb0b7d | 50000 | 0.000 | 0.072 | 18332 | False | False |
| cited_title | null | 0.000 |  | 0 | 0.000 | 0.000 | 0 | False | False |
| cited_year | null | 0.000 |  | 0 | 0.000 | 0.000 | 0 | False | False |
| cited_doi | null | 0.000 |  | 0 | 0.000 | 0.000 | 0 | False | False |
| section | null | 0.000 |  | 0 | 0.000 | 0.000 | 0 | False | False |
| paragraph_id | string | 1.000 | R13-1042_p0; R13-1042_p0; R13-1042_p0; R13-1042_p0; R13-1042_p0 | 50000 | 0.000 | 0.000 | 1907 | False | False |
| citation_marker | string | 1.000 | (2010); (Elsner and Charniak, 2010); (Aoki et al., 2003); (Yeh, 2006; Erera and Carmel, 2008); (Yeh, 2006; Erera and Carmel, 2008) | 50000 | 0.000 | 0.000 | 18486 | False | False |
| sentence_text | string | 1.000 | In NLP, Elsner and Charniak (2010) described the task of ...; Research on disentanglement of conversation threads has b...; Research on disentanglement of conversation threads has b...; Research on disentanglement of conversation threads has b...; Research on disentanglement of conversation threads has b... | 50000 | 0.000 | 0.000 | 32212 | False | False |
| context_window_s3 | string | 1.000 | We also found that contentbased features continue to outp...; In addition to emails with missing or incorrect MIME head...; In addition to emails with missing or incorrect MIME head...; In addition to emails with missing or incorrect MIME head...; In addition to emails with missing or incorrect MIME head... | 50000 | 0.000 | 0.000 | 32372 | False | False |
| context_window_paragraph | string | 1.000 | ple email accounts for one person; sharing one email acco...; adding these latter feature groups does not significantly...; es not significantly improve total performance. We also f...; based features continue to outperform the others in both ...; based features continue to outperform the others in both ... | 50000 | 0.000 | 0.000 | 40883 | False | False |
| citation_group_size | int64 | 1.000 | 1; 1; 1; 2; 2 | 50000 | 0.000 | 1.000 | 13 | False | False |
| attribution_status | string | 1.000 | bibliography_unresolved; bibliography_unresolved; bibliography_unresolved; multi_citation_group; multi_citation_group | 50000 | 0.000 | 0.000 | 3 | False | False |
