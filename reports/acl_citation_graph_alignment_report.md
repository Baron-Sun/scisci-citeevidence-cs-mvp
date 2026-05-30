# ACL Citation Graph Alignment Report

## Inputs
| name | path |
| --- | --- |
| publication_info | data/raw/acl_ocl/acl-publication-info.74k.v2.parquet |
| acl_onlygraph | data/raw/acl_ocl/acl_onlygraph.parquet |
| citation_contexts | data/processed/citation_contexts.parquet |

## Outputs
| name | path |
| --- | --- |
| acl_id_crosswalk | data/interim/acl_id_crosswalk.parquet |
| acl_citation_graph_aligned | data/interim/acl_citation_graph_aligned.parquet |

## Core Metrics
| metric | value |
| --- | --- |
| publication_info row count | 73285 |
| acl_id_crosswalk row count | 73284 |
| acl_onlygraph row count | 1339414 |
| aligned graph edges | 1339414 |
| citing side alignment rate | 1.000 |
| cited side alignment rate | 1.000 |
| both sides alignment rate | 1.000 |
| unique citing ACL papers | 60997 |
| unique cited ACL papers | 48300 |
| citation_contexts.citing_paper_id coverage | 0.882 |
| cited_title non-empty rate | 1.000 |
| cited_year non-empty rate | 1.000 |
| cited_authors non-empty rate | 1.000 |
| cited_doi non-empty rate | 0.504 |

## Alignment Status Distribution
| alignment_status | edges |
| --- | --- |
| both_aligned | 1339414 |

## Sample 20 Aligned Edges
| graph_edge_id | citing_acl_id | citing_title | citing_year | cited_acl_id | cited_title | cited_year | alignment_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3313665988 | 2021.vardial-1.12 | Comparing the Performance of {CNN}s and Shallow Models for Language Identification | 2021 | 2020.sltu-1.25 | A Sentiment Analysis Dataset for Code-Mixed {M}alayalam-{E}nglish | 2020 | both_aligned |
| 244015897 | U17-1003 | Joint Sentence-Document Model for Manifesto Text Analysis | 2017 | I11-1019 | Keyphrase Extraction from Online News Using Binary Integer Programming | 2011 | both_aligned |
| 2084450101 | 2020.lrec-1.393 | {OF}r{L}ex: A Computational Morphological and Syntactic Lexicon for {O}ld {F}rench | 2020 | W19-7816 | Challenges of language change and variation: towards an extended treebank of Medieval {F}rench | 2019 | both_aligned |
| 504040985 | W18-6453 | Findings of the {WMT} 2018 Shared Task on Parallel Corpus Filtering | 2018 | L12-1246 | Parallel Data, Tools and Interfaces in {OPUS} | 2012 | both_aligned |
| 63101789 | W13-2201 | Findings of the 2013 {W}orkshop on {S}tatistical {M}achine {T}ranslation | 2013 | P10-2016 | Tackling Sparse Data Issue in Machine Translation Evaluation | 2010 | both_aligned |
| 1562532567 | W19-5904 | Few-Shot Dialogue Generation Without Annotated Data: A Transfer Learning Approach | 2019 | N19-1423 | {BERT}: Pre-training of Deep Bidirectional Transformers for Language Understanding | 2019 | both_aligned |
| 3521563751 | 2022.cl-1.6 | Deep Learning for Text Style Transfer: A Survey | 2022 | D18-1138 | Learning Sentiment Memories for Sentiment Modification without Parallel Data | 2018 | both_aligned |
| 8311199 | L16-1533 | Government Domain Named Entity Recognition for {S}outh {A}frican Languages | 2016 | L14-1106 | Developing Text Resources for Ten {S}outh {A}frican Languages | 2014 | both_aligned |
| 321747530 | R09-1028 | Topic-based Multi-Document Summarization with Probabilistic Latent Semantic Analysis | 2009 | C00-1072 | The Automated Acquisition of Topic Signatures for Text Summarization | 2000 | both_aligned |
| 386231268 | W16-2306 | {P}ar{FDA} for Instance Selection for Statistical Machine Translation | 2016 | S16-1117 | {RTM} at {S}em{E}val-2016 Task 1: Predicting Semantic Similarity with Referential Translation Machines and Related St... | 2016 | both_aligned |
| 3179495017 | 2020.law-1.10 | {PASTRIE}: A Corpus of Prepositions Annotated with Supersense Tags in {R}eddit International {E}nglish | 2020 | K18-2016 | {U}niversal {D}ependency Parsing from Scratch | 2018 | both_aligned |
| 3150901241 | 2020.emnlp-main.705 | {C}ap{WAP}: Image Captioning with a Purpose | 2020 | D18-1083 | Improving Reinforcement Learning Based Image Captioning with Natural Language Prior | 2018 | both_aligned |
| 854677951 | W16-4110 | A Preliminary Study of Statistically Predictive Syntactic Complexity Features and Manual Simplifications in {B}asque | 2016 | W14-5604 | The Fewer, the Better? A Contrastive Study about Ways to Simplify | 2014 | both_aligned |
| 24327070 | W17-1711 | Discovering Light Verb Constructions and their Translations from Parallel Corpora without Word Alignment | 2017 | D11-1077 | Identification of Multi-word Expressions by Combining Multiple Linguistic Information Sources | 2011 | both_aligned |
| 1940049190 | F13-1033 | A fully discriminative training framework for Statistical Machine Translation (Un cadre d{'}apprentissage int{\'e}gra... | 2013 | W11-2168 | From n-gram-based to {CRF}-based Translation Models | 2011 | both_aligned |
| 2083264458 | W10-3217 | A Supervised Learning based Chunking in {T}hai using Categorial Grammar | 2010 | W00-0731 | Shallow Parsing as Part-of-Speech Tagging | 2000 | both_aligned |
| 1187050437 | W19-4828 | What Does {BERT} Look at? An Analysis of {BERT}{'}s Attention | 2019 | P16-1162 | Neural Machine Translation of Rare Words with Subword Units | 2016 | both_aligned |
| 820457544 | S15-2014 | yi{G}ou: A Semantic Text Similarity Computing System Based on {SVM} | 2015 | S12-1051 | {S}em{E}val-2012 Task 6: A Pilot on Semantic Textual Similarity | 2012 | both_aligned |
| 4824975 | W17-4007 | Word Transduction for Addressing the {OOV} Problem in Machine Translation for Similar Resource-Scarce Languages | 2017 | W09-3510 | Transliteration by Bidirectional Statistical Machine Translation | 2009 | both_aligned |
| 3470644076 | 2021.emnlp-main.1 | {A}lig{NART}: Non-autoregressive Neural Machine Translation by Jointly Learning to Estimate Alignment and Translate | 2021 | P07-1091 | A Probabilistic Approach to Syntax-based Reordering for Statistical Machine Translation | 2007 | both_aligned |

## Contexts Not Covered By Aligned Citing ACL IDs
| context_id | citing_paper_id | paragraph_id | citation_marker | sentence_text |
| --- | --- | --- | --- | --- |
| ctx_f2c1a8e86fa494f4c4db | W05-0819 | W05-0819_p0 | (Baker et al., 2004) | Training Data The training data set was composed of approximately 3441 English-Hindi parallel sentence pairs drawn from the EMILLE (Enabl... |
| ctx_7c9b43965df6205fab40 | W05-0819 | W05-0819_p0 | (Maynard et al., 2003) | This gazetteer list is distributed as a part of Hindi Gazetteer processing resource in GATE (Maynard et al., 2003) . |
| ctx_ed5f8e7c4f6e3db051dc | W05-0819 | W05-0819_p0 | (2001) | We derived a set of more than 250 rules to group such patterns by consulting the provided training data and other grammar resources such ... |
| ctx_9e3f02696c4eecebd415 | W09-1315 | W09-1315_p0 | (Baral, 2003) | One such formalism is Answer Set Programming (ASP) (Baral, 2003) . |
| ctx_75dc0aaafd24678780f1 | W09-1315 | W09-1315_p0 | (Bodenreider et al., 2008) | For instance, in (Bodenreider et al., 2008) , the authors illustrate the applicability and effectiveness of using ASP to represent a rule... |
| ctx_fa59000163db60d29b70 | W09-1315 | W09-1315_p0 | (Bodenreider et al., 2008) | In (Bodenreider et al., 2008) , biomedical queries are represented as programs in ASP; however, these programs are constructed manually. |
| ctx_4c3c8385f13bc5fbcda7 | W09-1315 | W09-1315_p0 | (Bodenreider et al., 2008) | The idea is to automatically compute an answer to the query using methods of (Bodenreider et al., 2008) , once the user types the query. |
| ctx_7c24edac56e506b78ef4 | W09-1315 | W09-1315_p0 | (Bernstein et al., 2005) | For instance, (Bernstein et al., 2005) considers queries in the controlled natural language, Attempto Controlled English (ACE) (Attempto,... |
| ctx_d0841f3fbecfcf3f0574 | W09-1315 | W09-1315_p0 | (Attempto, 2008) | For instance, (Bernstein et al., 2005) considers queries in the controlled natural language, Attempto Controlled English (ACE) (Attempto,... |
| ctx_e1433df68a83e72f2f29 | W09-1315 | W09-1315_p0 | (Klein and Bernstein, 2004) | For instance, (Bernstein et al., 2005) considers queries in the controlled natural language, Attempto Controlled English (ACE) (Attempto,... |
| ctx_3bdb0bc3193503f34547 | W09-1315 | W09-1315_p0 | (Bernstein et al., 2006) | For instance, (Bernstein et al., 2005) considers queries in the controlled natural language, Attempto Controlled English (ACE) (Attempto,... |
| ctx_59510caf0ca734a1f631 | W09-1315 | W09-1315_p0 | (Jena, 2008) | For instance, (Bernstein et al., 2005) considers queries in the controlled natural language, Attempto Controlled English (ACE) (Attempto,... |
| ctx_36ae2c4ea7adb8f60031 | W09-1315 | W09-1315_p0 | (Kaufmann et al., 2006) | On the other hand, (Kaufmann et al., 2006) transforms a given natural language query to a SPARQL query (using the Stan-ford Parser and WO... |
| ctx_a1b53d6761d3b826d89e | W09-1315 | W09-1315_p0 | (Baral et al., 2008) | Transformations of natural language sentences into ASP has been studied in (Baral et al., 2008) and (Baral et al., 2007) . |
| ctx_116f97a54d9593afde55 | W09-1315 | W09-1315_p0 | (Baral et al., 2007) | Transformations of natural language sentences into ASP has been studied in (Baral et al., 2008) and (Baral et al., 2007) . |
| ctx_1f8253617140010bb349 | W09-1315 | W09-1315_p0 | (Baral et al., 2008) | In (Baral et al., 2008) , the authors introduce methods to transform some simple forms of sentences into ASP using Lambda Calculus. |
| ctx_b417f7bff79be2f350f9 | W09-1315 | W09-1315_p0 | (Baral et al., 2007) | In (Baral et al., 2007) , the authors use C&C tools (CC, 2009) to parse the some forms of natural language input, and perform a semantic ... |
| ctx_7d7bda7dcf4526d0d8d7 | W09-1315 | W09-1315_p0 | (CC, 2009) | In (Baral et al., 2007) , the authors use C&C tools (CC, 2009) to parse the some forms of natural language input, and perform a semantic ... |
| ctx_77982f5ea03da951af29 | W09-1315 | W09-1315_p0 | (Boxer, 2009) | In (Baral et al., 2007) , the authors use C&C tools (CC, 2009) to parse the some forms of natural language input, and perform a semantic ... |
| ctx_f77b5229b87beda0add2 | W09-1315 | W09-1315_p0 | (Kamp, 1981) | Our work is different in that we consider a CNL to express queries, and introduce a different method for converting CNL to a program in A... |

## Notes
This table is a candidate ACL-to-ACL citation graph. It does not resolve individual citation markers to bibliography entries. Numeric markers such as `[12]` still require local bibliography order, and author-year markers should be resolved in a later task.
