# Final Resolved Citation Context Audit

## Inputs
- Resolved contexts: `data/processed/citation_contexts_resolved.parquet`

## Outputs
- Quality flags: `data/processed/final_resolved_context_quality_flags.parquet`
- Strong resolved review sample: `data/processed/strong_resolved_contexts_sample.csv`
- Manual resolution review sample: `data/processed/manual_resolution_review_sample.csv`
- Analysis-ready strong contexts: `data/processed/analysis_ready_strong_contexts.parquet`

## Core Metrics
| metric | value |
| --- | --- |
| total rows | 3152073 |
| unique source_context_id | 1990689 |
| unique context_id | 3152073 |
| duplicate context_id count | 0 |
| is_strongly_resolved count | 1188307 |
| is_strongly_resolved rate | 0.377 |
| resolved_cited_title non-empty rate for strong rows | 1.000 |
| resolved_cited_year non-empty rate for strong rows | 1.000 |
| resolved_cited_authors non-empty rate for strong rows | 1.000 |
| raw_section_name coverage | 0.985 |
| citation_marker in sentence_text rate | 1.000 |
| sentence_text in context_window_s3 rate | 1.000 |
| flagged rows that are also is_strongly_resolved | 297568 |
| analysis_ready_strong_contexts rows | 1184634 |

## Marker Type Distribution
| marker_type | rows |
| --- | --- |
| parenthetical_author_year | 2648550 |
| narrative_author_year | 384795 |
| numeric | 85782 |
| year_only | 32946 |

## Resolution Status Distribution
| resolution_status | rows |
| --- | --- |
| bibliography_unresolved | 1554802 |
| author_year_clear | 1188319 |
| citing_paper_not_in_aligned_graph | 225675 |
| numeric_marker_unresolved_no_bibliography | 85782 |
| multi_candidate_ambiguous | 55845 |
| ambiguous_year_only | 16783 |
| author_year_weak_nonfirst_author | 15936 |
| year_only_unique_candidate | 8931 |

## Resolution Level Distribution
| resolution_level | rows |
| --- | --- |
| unresolved | 1554814 |
| strong_author_year | 1188307 |
| out_of_graph | 225675 |
| numeric_unresolved | 85782 |
| ambiguous | 72628 |
| weak_nonfirst_author | 15936 |
| weak_year_only | 8931 |

## Normalized Section Distribution
| normalized_section | rows |
| --- | --- |
| unknown | 914040 |
| introduction | 877242 |
| related_work | 628270 |
| dataset | 142550 |
| model | 109701 |
| experiment | 89167 |
| method | 82641 |
| evaluation | 61021 |
| background | 52831 |
| conclusion | 44192 |
| results | 38826 |
| discussion | 35379 |
| analysis | 23173 |
| abstract | 13710 |
| implementation | 10893 |
| references | 6314 |
| system_description | 6283 |
| task_definition | 5978 |
| appendix | 3996 |
| acknowledgement | 3498 |
| error_analysis | 2368 |

## Strong Rows By Normalized Section
| normalized_section | strong_rows |
| --- | --- |
| introduction | 342737 |
| unknown | 293812 |
| related_work | 276975 |
| dataset | 54386 |
| model | 40179 |
| experiment | 39099 |
| method | 28484 |
| evaluation | 25972 |
| background | 17069 |
| results | 16808 |
| conclusion | 16322 |
| discussion | 11045 |
| analysis | 7526 |
| abstract | 4602 |
| implementation | 3322 |
| system_description | 2886 |
| task_definition | 2481 |
| references | 2341 |
| appendix | 974 |
| error_analysis | 929 |
| acknowledgement | 358 |

## Unresolved Rows By Normalized Section
| normalized_section | unresolved_rows |
| --- | --- |
| unknown | 620228 |
| introduction | 534505 |
| related_work | 351295 |
| dataset | 88164 |
| model | 69522 |
| method | 54157 |
| experiment | 50068 |
| background | 35762 |
| evaluation | 35049 |
| conclusion | 27870 |
| discussion | 24334 |
| results | 22018 |
| analysis | 15647 |
| abstract | 9108 |
| implementation | 7571 |
| references | 3973 |
| task_definition | 3497 |
| system_description | 3397 |
| acknowledgement | 3140 |
| appendix | 3022 |
| error_analysis | 1439 |

## Analysis-Ready Rows By Normalized Section
| normalized_section | analysis_ready_rows |
| --- | --- |
| introduction | 342737 |
| unknown | 293812 |
| related_work | 276975 |
| dataset | 54386 |
| model | 40179 |
| experiment | 39099 |
| method | 28484 |
| evaluation | 25972 |
| background | 17069 |
| results | 16808 |
| conclusion | 16322 |
| discussion | 11045 |
| analysis | 7526 |
| abstract | 4602 |
| implementation | 3322 |
| system_description | 2886 |
| task_definition | 2481 |
| error_analysis | 929 |

## Citation Group And Range Flags
### large_citation_group_flag
| large_citation_group_flag | rows |
| --- | --- |
| False | 3150748 |
| True | 1325 |

### very_large_citation_group_flag
| very_large_citation_group_flag | rows |
| --- | --- |
| False | 3151260 |
| True | 813 |

### suspicious_citation_range_flag
| suspicious_citation_range_flag | rows |
| --- | --- |
| False | 3150897 |
| True | 1176 |

## Quality Flag Summary
| flag | rows | rate |
| --- | --- | --- |
| duplicate_context_id | 0 | 0.000 |
| missing_context_window | 0 | 0.000 |
| marker_not_in_sentence | 0 | 0.000 |
| sentence_not_in_context_window | 530 | 0.000 |
| strong_missing_resolved_title | 0 | 0.000 |
| strong_missing_resolved_year | 0 | 0.000 |
| strong_missing_resolved_authors | 0 | 0.000 |
| strong_numeric_marker | 0 | 0.000 |
| strong_year_only_marker | 0 | 0.000 |
| strong_suspicious_citation_range | 0 | 0.000 |
| strong_large_citation_group | 0 | 0.000 |
| section_missing | 0 | 0.000 |
| normalized_section_unknown | 914040 | 0.290 |
| strong_in_references_section | 2341 | 0.001 |
| strong_in_acknowledgement_section | 358 | 0.000 |
| strong_in_appendix_section | 974 | 0.000 |
| author_year_clear_not_strong | 12 | 0.000 |
| flag_any | 917923 | 0.291 |

## Special Consistency Checks
| check | rows |
| --- | --- |
| author_year_clear_not_strong | 12 |
| strong_in_references_section | 2341 |
| strong_in_acknowledgement_section | 358 |
| strong_in_appendix_section | 974 |
| strong_numeric_marker | 0 |
| strong_year_only_marker | 0 |
| strong_suspicious_citation_range | 0 |
| strong_large_citation_group | 0 |

Rows with `resolution_status = author_year_clear` are strong only when the marker is not numeric or year-only, `suspicious_citation_range_flag` is false, and the resolver assigns `resolution_level = strong_author_year`.

## Top Unresolved Failure Modes
| resolution_level | resolution_status | rows |
| --- | --- | --- |
| unresolved | bibliography_unresolved | 1554802 |
| out_of_graph | citing_paper_not_in_aligned_graph | 225675 |
| numeric_unresolved | numeric_marker_unresolved_no_bibliography | 85782 |
| ambiguous | multi_candidate_ambiguous | 55845 |
| ambiguous | ambiguous_year_only | 16783 |
| weak_nonfirst_author | author_year_weak_nonfirst_author | 15936 |
| weak_year_only | year_only_unique_candidate | 8931 |
| unresolved | author_year_clear | 12 |

## Manual Review Sampling Counts
| review_bucket | rows |
| --- | --- |
| strong_author_year | 200 |
| bibliography_unresolved | 100 |
| multi_candidate_ambiguous | 75 |
| numeric_unresolved | 75 |
| weak_year_or_nonfirst_author | 50 |

## Examples: author_year_clear_not_strong
| context_id | source_context_id | citing_paper_id | normalized_section | citation_marker | marker_component_text | marker_type | resolution_status | resolution_level | is_strongly_resolved | resolved_cited_title | sentence_text | exclusion_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_43ebf3aaee0f00284d0a | ctx_6a190c942795d6fa2325 | C10-1105 | introduction | (2004; ) | Florian et al., 2004 | year_only | author_year_clear | unresolved | False | A Statistical Model for Multilingual Entity Detection and Tracking | In recent years, supervised semantic class determination has been tackled primarily in the context of (1) coreference resolution (e.g., Ng (2007) , Huang et al. (2009) ), where ... | marker_type=year_only; resolution_level=unresolved |
| ctxr_14e9b4cff72b72812ffe | ctx_74bb88e631760ac8cf9d | C14-1147 | related_work | (2008; ) | Agirre and Soroa, 2008 | year_only | author_year_clear | unresolved | False | Using the Multilingual Central Repository for Graph-Based Word Sense Disambiguation | Sinha and Mihalcea (2007) , Agirre and Soroa (2008; ). | marker_type=year_only; resolution_level=unresolved |
| ctxr_e0070c35bbf24491925d | ctx_73c69376a2a856f70dea | N15-1165 | introduction | (2009; ) | Agirre et al., 2009 | year_only | author_year_clear | unresolved | False | A Study on Similarity and Relatedness Using Distributional and {W}ord{N}et-based Approaches | For instance, Agirre et al. (2009; ) apply a random walk algorithm based on Personalized PageRank to WordNet, pre- Figure 1 : Main architecture for generating KB word embeddings. | marker_type=year_only; resolution_level=unresolved |
| ctxr_c4a8b9e6e9c583824403 | ctx_eabb348a3d9eb0c00040 | W13-1201 | experiment | (2007; ) | Delmonte, 2007 | year_only | author_year_clear | unresolved | False | Entailment and Anaphora Resolution in {RTE}3 | The categories used are fully explained in Delmonte (2007; ) and here we limit ourselves to a short description. | marker_type=year_only; resolution_level=unresolved |
| ctxr_b594369ae62f08bc51dd | ctx_d136f82825ea4f0541ed | L16-1631 | related_work | (2013; ) | Chen and Ng, 2013 | year_only | author_year_clear | unresolved | False | {C}hinese Event Coreference Resolution: Understanding the State of the Art | Most ACE event coreference resolvers are supervised, training a pairwise model to determine whether two event mentions are coreferent (e.g., Ahn (2006) , Chen and Ng (2013; ). | marker_type=year_only; resolution_level=unresolved |
| ctxr_e933a4d5608109c08f52 | ctx_f02e7b83d97b069774db | D10-1023 | unknown | (2002; ) | Barzilay and Lee, 2002 | year_only | author_year_clear | unresolved | False | Bootstrapping Lexical Choice via Multiple-Sequence Alignment | While sequence alignment has also been used in text and paraphrase generation (e.g., Barzilay and Lee (2002; ), it has not been extensively applied to other areas of language pr... | marker_type=year_only; resolution_level=unresolved |
| ctxr_49ac95d8f05e51d222e4 | ctx_43869a404159508f91da | P10-1142 | introduction | (1983; ) | Grosz et al., 1983 | year_only | author_year_clear | unresolved | False | Providing a Unified Account of Definite Noun Phrases in Discourse | Computational theories of discourse, in particular focusing (see Grosz (1977) and Sidner (1979) ) and centering (Grosz et al. (1983; ), have heavily influenced coreference resea... | marker_type=year_only; resolution_level=unresolved |
| ctxr_5fed6c18b145f7ca2577 | ctx_607ef1c66241dc9498f6 | N15-1116 | unknown | (2009; ) | Rahman and Ng, 2009 | year_only | author_year_clear | unresolved | False | Supervised Models for Coreference Resolution | This joint modeling method has proven effective in earlier work on supervised entity coreference resolution (e.g., Rahman and Ng (2009; ). | marker_type=year_only; resolution_level=unresolved |
| ctxr_563c5abcaa5efd83fafb | ctx_b79c93bf3741aa91c9fe | 2020.acl-main.418 | unknown | (2017) | Larson, 2017 | year_only | author_year_clear | unresolved | False | Gender as a Variable in Natural-Language Processing: Ethical Considerations | - - Weller et al. (2013) N Y N Y - - - - Ciot et al. (2013) N N Y N - Y Y - Volkova et al. (2013) N N Y Y - Y Y N Levitan (2013) N N Y Y - N N N Bojar et al. (2013) N Y N N - - ... | marker_type=year_only; resolution_level=unresolved |
| ctxr_ee225ffe442834ed87da | ctx_3aeef8ec85542251a90a | W19-4411 | dataset | (2017; ) | Johnson & Zhang, 2017 | year_only | author_year_clear | unresolved | False | Deep Pyramid Convolutional Neural Networks for Text Categorization | Johnson & Zhang (2017; ). | marker_type=year_only; resolution_level=unresolved |
| ctxr_46efb585b00ffb668822 | ctx_e97b3ff11a8d59a43c50 | W14-2004 | introduction | (2011b; ) | Stabler, 2011b | year_only | author_year_clear | unresolved | False | Top-Down Recognizers for {MCFG}s and {MG}s | A new kind of top-down parser for MGs has recently been presented by Stabler (2011b; ). | marker_type=year_only; resolution_level=unresolved |
| ctxr_4b0f1bf17b3a9ba8645a | ctx_91b71266063c97b4af43 | W08-0904 | introduction | (2004; ) | Han et al., 2004 | year_only | author_year_clear | unresolved | False | Detecting Errors in {E}nglish Article Usage with a Maximum Entropy Classifier Trained on a Large, Diverse Corpus | In error detection, most methods such as Chodorow and Leacock (2000) , Izumi et al. (2003) , Nagata et al. (2005; , and Han et al. (2004; ) use a POS tagger and/or a chunker to ... | marker_type=year_only; resolution_level=unresolved |

## Examples: strong_in_references_section
| context_id | source_context_id | citing_paper_id | normalized_section | citation_marker | marker_component_text | marker_type | resolution_status | resolution_level | is_strongly_resolved | resolved_cited_title | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_dcd0bbf45971dcca9242 | ctx_d7dbfcd45044c46775ea | 2020.emnlp-main.686 | references | Joshi et al. (2019) | Joshi et al. (2019) | narrative_author_year | author_year_clear | strong_author_year | True | {BERT} for Coreference Resolution: Baselines and Analysis | We use different Transformers-based encoders, and follow the "independent" setup for long documents as suggested by Joshi et al. (2019) . |
| ctxr_5e9494b448f62276b750 | ctx_5be90e05a30b1b4087b8 | 2021.codi-sharedtask.8 | references | (Xu and Choi, 2021) | Xu and Choi, 2021 | parenthetical_author_year | author_year_clear | strong_author_year | True | Adapted End-to-End Coreference Resolution System for Anaphoric Identities in Dialogues | In this section, we analyze the results of the four teams that participated in the anaphora resolution track and submitted a shared task paper, namely the team from Emory Univer... |
| ctxr_96d91ea19bf5d4a17ac9 | ctx_80129b530c3a8c9c67e7 | 2021.codi-sharedtask.8 | references | (Kobayashi et al., 2021 ) | Kobayashi et al., 2021 | parenthetical_author_year | author_year_clear | strong_author_year | True | Neural Anaphora Resolution in Dialogue | In this section, we analyze the results of the four teams that participated in the anaphora resolution track and submitted a shared task paper, namely the team from Emory Univer... |
| ctxr_b949d3c5b89f68c90aab | ctx_656c1a9a40e5fdd03315 | 2021.codi-sharedtask.8 | references | (Kim et al., 2021 ) | Kim et al., 2021 | parenthetical_author_year | author_year_clear | strong_author_year | True | The Pipeline Model for Resolution of Anaphoric Reference and Resolution of Entity Reference | In this section, we analyze the results of the four teams that participated in the anaphora resolution track and submitted a shared task paper, namely the team from Emory Univer... |
| ctxr_f0f6d0d7a024d138ccee | ctx_d55e2d9d1d2735ee16fe | 2021.codi-sharedtask.8 | references | (Anikina et al., 2021) | Anikina et al., 2021 | parenthetical_author_year | author_year_clear | strong_author_year | True | Anaphora Resolution in Dialogue: Description of the {DFKI}-{T}alking{R}obots System for the {CODI}-{CRAC} 2021 Shared-Task | In this section, we analyze the results of the four teams that participated in the anaphora resolution track and submitted a shared task paper, namely the team from Emory Univer... |
| ctxr_fde293c9340adba7e068 | ctx_3283b6a365b583e1cedd | 2009.mtsummit-posters.8 | references | (Papineni et al., 2002) | Papineni et al., 2002 | parenthetical_author_year | author_year_clear | strong_author_year | True | {B}leu: a Method for Automatic Evaluation of Machine Translation | In (Papineni et al., 2002) , the single means of capturing variation in translation is to use multiple references. |
| ctxr_3bbbf671a47454cbc0e7 | ctx_9ea8bf8df94f330e7247 | D19-5725 | references | (Hovy et al., 2006) | Hovy et al., 2006 | parenthetical_author_year | author_year_clear | strong_author_year | True | {O}nto{N}otes: The 90{\%} Solution | Coreference resolution is an active area in the NLP research community, and the most relevant previous shared task on coreference resolution is the CoNLL-2012 Shared Task (Pradh... |
| ctxr_aaa22264f6e62d3ff64f | ctx_d503e755617ab4e4aeff | D19-5727 | references | (Devlin et al., 2019) | Devlin et al., 2019 | parenthetical_author_year | author_year_clear | strong_author_year | True | {BERT}: Pre-training of Deep Bidirectional Transformers for Language Understanding | Recently, BERT (Devlin et al., 2019) shows significant improvement on various tasks in comparison with other deep learning models including LSTMs. |
| ctxr_19bfac4747d83af65320 | ctx_c5c3648bd05baba5d056 | F13-1033 | references | (Liang et al., 2006) | Liang et al., 2006 | parenthetical_author_year | author_year_clear | strong_author_year | True | An End-to-End Discriminative Approach to Machine Translation | Un problème spécifique qui se pose dans le cadre de l'apprentissage discriminant pour la traduction est celui de la non atteignabilité des références, correspondant aux situatio... |
| ctxr_346287520f48946cefcf | ctx_16bd88bd6c07891fe1c9 | F13-1033 | references | (Blunsom et al., 2008; Dyer et Resnik, 2010 ) | Blunsom et al., 2008 | parenthetical_author_year | author_year_clear | strong_author_year | True | A Discriminative Latent Variable Model for Statistical Machine Translation | Un remède radical consiste alors à supprimer ces cas problématiques du corpus d'apprentissage (Blunsom et al., 2008; Dyer et Resnik, 2010 ) -conduisant ainsi à abandonner de nom... |

## Examples: strong_in_acknowledgement_section
| context_id | source_context_id | citing_paper_id | normalized_section | citation_marker | marker_component_text | marker_type | resolution_status | resolution_level | is_strongly_resolved | resolved_cited_title | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_9fa2ecfafd55891e3690 | ctx_d39b2a3705e40dea3082 | 2020.tlt-1.4 | acknowledgement | (McDonald et al., 2013) | McDonald et al., 2013 | parenthetical_author_year | author_year_clear | strong_author_year | True | {U}niversal {D}ependency Annotation for Multilingual Parsing | We will also start annotating the corpus for Universal Dependencies (McDonald et al., 2013). |
| ctxr_05fc42df1a03c711bcd4 | ctx_ed0fbf74a5d16cb7cda4 | W10-3404 | acknowledgement | (Shnarch et al., 2009) | Shnarch et al., 2009 | parenthetical_author_year | author_year_clear | strong_author_year | True | Extracting Lexical Reference Rules from {W}ikipedia | Shnarch et al. (Shnarch et al., 2009) researched the extraction from Wikipedia of lexical reference rules, identifying references to term meaning triggered by other terms. |
| ctxr_e596bad0d87f54278ded | ctx_3d1efae0f5274511000b | W09-1212 | acknowledgement | (Taulé et al., 2008; Palmer and Xue, 2009; Hajič et al., 2006; Surdeanu et al., 2008; Burchardt et al., 2006; Kawahara et al., 2002) | Surdeanu et al., 2008 | parenthetical_author_year | author_year_clear | strong_author_year | True | The {C}o{NLL} 2008 Shared Task on Joint Parsing of Syntactic and Semantic Dependencies | We thank the corpus providers (Taulé et al., 2008; Palmer and Xue, 2009; Hajič et al., 2006; Surdeanu et al., 2008; Burchardt et al., 2006; Kawahara et al., 2002) for their effo... |
| ctxr_c070f4a20f7b2c79a0a9 | ctx_3d1efae0f5274511000b | W09-1212 | acknowledgement | (Taulé et al., 2008; Palmer and Xue, 2009; Hajič et al., 2006; Surdeanu et al., 2008; Burchardt et al., 2006; Kawahara et al., 2002) | Burchardt et al., 2006 | parenthetical_author_year | author_year_clear | strong_author_year | True | The {SALSA} Corpus: a {G}erman Corpus Resource for Lexical Semantics | We thank the corpus providers (Taulé et al., 2008; Palmer and Xue, 2009; Hajič et al., 2006; Surdeanu et al., 2008; Burchardt et al., 2006; Kawahara et al., 2002) for their effo... |
| ctxr_6b5efc408e7e4d373197 | ctx_3d1efae0f5274511000b | W09-1212 | acknowledgement | (Taulé et al., 2008; Palmer and Xue, 2009; Hajič et al., 2006; Surdeanu et al., 2008; Burchardt et al., 2006; Kawahara et al., 2002) | Kawahara et al., 2002 | parenthetical_author_year | author_year_clear | strong_author_year | True | Construction of a {J}apanese Relevance-tagged Corpus | We thank the corpus providers (Taulé et al., 2008; Palmer and Xue, 2009; Hajič et al., 2006; Surdeanu et al., 2008; Burchardt et al., 2006; Kawahara et al., 2002) for their effo... |
| ctxr_184e9b46ddd5a2f751d9 | ctx_acc0e4bf5da67ed553e7 | W09-1212 | acknowledgement | (Taulé et al., 2008; Palmer and Xue, 2009; Hajič et al., 2006; Surdeanu et al., 2008; Burchardt et al., 2006; Kawahara et al., 2002) | Surdeanu et al., 2008 | parenthetical_author_year | author_year_clear | strong_author_year | True | The {C}o{NLL} 2008 Shared Task on Joint Parsing of Syntactic and Semantic Dependencies | We thank the corpus providers (Taulé et al., 2008; Palmer and Xue, 2009; Hajič et al., 2006; Surdeanu et al., 2008; Burchardt et al., 2006; Kawahara et al., 2002) for their effo... |
| ctxr_22ac67b25ed8a0bbe580 | ctx_acc0e4bf5da67ed553e7 | W09-1212 | acknowledgement | (Taulé et al., 2008; Palmer and Xue, 2009; Hajič et al., 2006; Surdeanu et al., 2008; Burchardt et al., 2006; Kawahara et al., 2002) | Burchardt et al., 2006 | parenthetical_author_year | author_year_clear | strong_author_year | True | The {SALSA} Corpus: a {G}erman Corpus Resource for Lexical Semantics | We thank the corpus providers (Taulé et al., 2008; Palmer and Xue, 2009; Hajič et al., 2006; Surdeanu et al., 2008; Burchardt et al., 2006; Kawahara et al., 2002) for their effo... |
| ctxr_60a088725f76fd2d1ac9 | ctx_acc0e4bf5da67ed553e7 | W09-1212 | acknowledgement | (Taulé et al., 2008; Palmer and Xue, 2009; Hajič et al., 2006; Surdeanu et al., 2008; Burchardt et al., 2006; Kawahara et al., 2002) | Kawahara et al., 2002 | parenthetical_author_year | author_year_clear | strong_author_year | True | Construction of a {J}apanese Relevance-tagged Corpus | We thank the corpus providers (Taulé et al., 2008; Palmer and Xue, 2009; Hajič et al., 2006; Surdeanu et al., 2008; Burchardt et al., 2006; Kawahara et al., 2002) for their effo... |
| ctxr_ebd182184baa124b483e | ctx_79cec45078a4c45fcf09 | W09-1212 | acknowledgement | (Taulé et al., 2008; Palmer and Xue, 2009; Hajič et al., 2006; Surdeanu et al., 2008; Burchardt et al., 2006; Kawahara et al., 2002) | Surdeanu et al., 2008 | parenthetical_author_year | author_year_clear | strong_author_year | True | The {C}o{NLL} 2008 Shared Task on Joint Parsing of Syntactic and Semantic Dependencies | We thank the corpus providers (Taulé et al., 2008; Palmer and Xue, 2009; Hajič et al., 2006; Surdeanu et al., 2008; Burchardt et al., 2006; Kawahara et al., 2002) for their effo... |
| ctxr_718001e8e1b043e271b6 | ctx_79cec45078a4c45fcf09 | W09-1212 | acknowledgement | (Taulé et al., 2008; Palmer and Xue, 2009; Hajič et al., 2006; Surdeanu et al., 2008; Burchardt et al., 2006; Kawahara et al., 2002) | Burchardt et al., 2006 | parenthetical_author_year | author_year_clear | strong_author_year | True | The {SALSA} Corpus: a {G}erman Corpus Resource for Lexical Semantics | We thank the corpus providers (Taulé et al., 2008; Palmer and Xue, 2009; Hajič et al., 2006; Surdeanu et al., 2008; Burchardt et al., 2006; Kawahara et al., 2002) for their effo... |

## Examples: strong_in_appendix_section
| context_id | source_context_id | citing_paper_id | normalized_section | citation_marker | marker_component_text | marker_type | resolution_status | resolution_level | is_strongly_resolved | resolved_cited_title | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_e20070a4f58b71917085 | ctx_2768af87b2ee9d1584fb | D14-1161 | appendix | Mohammad et al. (2008) | Mohammad et al. (2008) | narrative_author_year | author_year_clear | strong_author_year | True | Computing Word-Pair Antonymy | Mohammad et al. (2008) reproted a 23% F-score look-up performance of WordNet which support this claim as well. |
| ctxr_5de78048265027e0de61 | ctx_307379417eddb01d78d9 | 2022.nlp4convai-1.6 | appendix | (Miller et al., 2017) | Miller et al., 2017 | parenthetical_author_year | author_year_clear | strong_author_year | True | {P}arl{AI}: A Dialog Research Software Platform | All experiments were conducted using ParlAI (Miller et al., 2017) . |
| ctxr_f61154f922f7f4cd26c2 | ctx_8e5414a2af11e8e288dd | 2021.wnut-1.9 | appendix | Sasano et al. (2013) | Sasano et al. (2013) | narrative_author_year | author_year_clear | strong_author_year | True | A Simple Approach to Unknown Word Processing in {J}apanese Morphological Analysis | The IDs with "S" and "I" indicate that similar rules were used in Sasano et al. (2013) and Ikeda et al. (2016) , respectively. |
| ctxr_132542908bcf04b8edfa | ctx_7b8a5050aae2a940fabc | 2021.wnut-1.9 | appendix | Ikeda et al. (2016) | Ikeda et al. (2016) | narrative_author_year | author_year_clear | strong_author_year | True | {J}apanese Text Normalization with Encoder-Decoder Model | The IDs with "S" and "I" indicate that similar rules were used in Sasano et al. (2013) and Ikeda et al. (2016) , respectively. |
| ctxr_b52474078bfe9c1dfbd9 | ctx_65a60673d7e001f95c38 | 2020.coling-main.595 | appendix | (Shieber et al., 1995; Nederhof, 2003) | Nederhof, 2003 | parenthetical_author_year | author_year_clear | strong_author_year | True | Squibs and Discussions: Weighted Deductive Parsing and {K}nuth{'}s Algorithm | SA:PW: Our TWG parser is specified in terms of weighted deduction rules (Shieber et al., 1995; Nederhof, 2003) . |
| ctxr_6fb947c4063101701058 | ctx_933c12a39e12d8301028 | 2020.coling-main.595 | appendix | (Shieber et al., 1995; Nederhof, 2003) | Nederhof, 2003 | parenthetical_author_year | author_year_clear | strong_author_year | True | Squibs and Discussions: Weighted Deductive Parsing and {K}nuth{'}s Algorithm | SA:PW: Our TWG parser is specified in terms of weighted deduction rules (Shieber et al., 1995; Nederhof, 2003) . |
| ctxr_9e9cc9329951ec0e4122 | ctx_68f3475ff9408b653ddf | 2022.naacl-main.395 | appendix | Lee et al. (2018) | Lee et al. (2018) | narrative_author_year | author_year_clear | strong_author_year | True | Higher-Order Coreference Resolution with Coarse-to-Fine Inference | A.1 Baseline: COREFWe use the Transformers-based end-to-end coreference model from Lee et al. (2018) ; Joshi et al. (2019) without higher-order inference (Xu and Choi, 2020) whi... |
| ctxr_83a800ba33502468880d | ctx_cc53c06a42d2ae25078d | 2022.naacl-main.395 | appendix | Joshi et al. (2019) | Joshi et al. (2019) | narrative_author_year | author_year_clear | strong_author_year | True | {BERT} for Coreference Resolution: Baselines and Analysis | A.1 Baseline: COREFWe use the Transformers-based end-to-end coreference model from Lee et al. (2018) ; Joshi et al. (2019) without higher-order inference (Xu and Choi, 2020) whi... |
| ctxr_406fc1b45cc755e8a2b9 | ctx_aca786af7a1f406a72f9 | 2022.naacl-main.395 | appendix | (Xu and Choi, 2020) | Xu and Choi, 2020 | parenthetical_author_year | author_year_clear | strong_author_year | True | Revealing the Myth of Higher-Order Inference in Coreference Resolution | A.1 Baseline: COREFWe use the Transformers-based end-to-end coreference model from Lee et al. (2018) ; Joshi et al. (2019) without higher-order inference (Xu and Choi, 2020) whi... |
| ctxr_861ab1f7a5fad9cca08e | ctx_946095a13007c0194345 | 2022.naacl-main.395 | appendix | (Pradhan et al., 2012) | Pradhan et al., 2012 | parenthetical_author_year | author_year_clear | strong_author_year | True | {C}o{NLL}-2012 Shared Task: Modeling Multilingual Unrestricted Coreference in {O}nto{N}otes | A.1 Baseline: COREFWe use the Transformers-based end-to-end coreference model from Lee et al. (2018) ; Joshi et al. (2019) without higher-order inference (Xu and Choi, 2020) whi... |

## Random Examples By Resolution Level
| example_bucket | context_id | source_context_id | citing_paper_id | normalized_section | citation_marker | marker_component_text | marker_type | resolution_status | resolution_level | is_strongly_resolved | resolved_cited_title | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ambiguous | ctxr_7b65757c3162f22ab519 | ctx_57b536119ac7e3600d9c | K19-1038 | unknown | (Rankel et al., 2013; Owczarzak et al., 2012a,b; Rankel et al., 2011) | Owczarzak et al., 2012a,b | parenthetical_author_year | multi_candidate_ambiguous | ambiguous | False |  | Analyses of over a decade of NIST data from automated summarizers that evaluate ROUGE against manual pyramid and another manual score led to a solution to this problem (Rankel e... |
| ambiguous | ctxr_ed83ab2cda7d06616301 | ctx_e59c7b7dc553d79bd564 | J00-2001 | unknown | (e.g., McDonald 1983; Hovy 1988a ) | Hovy 1988a | parenthetical_author_year | multi_candidate_ambiguous | ambiguous | False |  | The names given to the components vary; they have been called "strategic" and "tactical" components (e.g., McKeown 1985; Thompson 1977; Danlos 1987) 1, "planning" and "realizati... |
| ambiguous | ctxr_6ff548940ff9f915c5c3 | ctx_3561122766f865063915 | C92-2082 | related_work | (Brent 1991) | Brent 1991 | parenthetical_author_year | multi_candidate_ambiguous | ambiguous | False |  | Work on acquisition of syntactic information from text corpora includes Brent's (Brent 1991) verb subcategorization frame recognition technique and Smadja's (Smadja & McKeown 19... |
| ambiguous | ctxr_79f50f163cd65e9ef97d | ctx_7c212f6267491d20c6f3 | 2014.amta-workshop.2 | related_work | (Specia et al., 2009; Buck, 2012; Beck et al., 2013; C. de Souza et al., 2014a) | C. de Souza et al., 2014a | parenthetical_author_year | multi_candidate_ambiguous | ambiguous | False |  | State-of-the-art in QE explores different supervised linear or non-linear learning methods for regression or classification such as, among others, support vector machines (SVM),... |
| ambiguous | ctxr_3dd204edac5649fc82df | ctx_eac4b6dc758e6dff3090 | D19-5323 | experiment | (Luan et al., 2018b) | Luan et al., 2018b | parenthetical_author_year | multi_candidate_ambiguous | ambiguous | False |  | The top three reported submissions in the SemEval leaderboard were: UWNLP (Luan et al., 2018b) , ETH-DS3Labl (Rotsztejn et al., 2018) , and SIRIUS-LTG-UiO (Nooralahzadeh et al.,... |
| numeric_unresolved | ctxr_fefbf8ab5e2e86b1a214 | ctx_5ce2cc7fc9fdd7a98d88 | 1992.tmi-1.5 | unknown | [14, 15, 16, 17 ] | [14, 15, 16, 17 ] | numeric | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False |  | Some of them are related with the problems of knowledge-based MT system [14, 15, 16, 17 ]. |
| numeric_unresolved | ctxr_a5710d9ecc566430f2ad | ctx_2508f5198b1ad8895013 | C12-2066 | unknown | [7, 8, 3, 4] | [7, 8, 3, 4] | numeric | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False |  | 1 S [0, 1, 0, 1] 2 S [0, 1, 0, 1] [1, 2, 6, 7] 3 S [0, 1, 0, 1] [1, 2, 6, 7] [2, 3, 7, 8] 4 R M [0, 1, 0, 1] [1, 3, 6, 8] 5 S [0, 1, 0, 1] [1, 3, 6, 8] [3, 4, 4, 5] 6 S [0, 1, 0... |
| numeric_unresolved | ctxr_9e8dbff2eb2acd5a55d8 | ctx_5156827bc24c220998e3 | W13-1802 | model | [0, 1] | [0, 1] | numeric | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False |  | • P f : Q → [0, 1] and P : δ → [0, 1] define the final and transition probability distributions as before in Section 3. |
| numeric_unresolved | ctxr_56208981535d56a45cd0 | ctx_f04fa085416475190fc1 | 2005.iwslt-1.3 | model | [1] | [1] | numeric | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False |  | The experimental results in [1] have shown that minimizing the translation distortion in development data is an effective method to improve translation qualities of test data. |
| numeric_unresolved | ctxr_512df278ab962729f9a4 | ctx_63170184b4cce50c63f5 | R09-1029 | unknown | [18] | [18] | numeric | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False |  | In the debate within cognitive psychology about the distinction between "abstractive" versus "non-abstractive" models of memory [18] [21] , LSA has been proposed as belonging to... |
| out_of_graph | ctxr_b694bb06e5a58d8c61b1 | ctx_909b8c003067c76f207c | W11-2310 | unknown | (1998) | 1998 | year_only | citing_paper_not_in_aligned_graph | out_of_graph | False |  | Here, we go one step forward, because if we say that a product must be usable as described in ISO 9241-11 (1998) , it must also be satisfying. |
| out_of_graph | ctxr_0be2a4e2439a9373f235 | ctx_85d413ce69e8d6471b8c | 2022.findings-acl.82 | introduction | (Richardson et al., 2013; Chen et al., 2016; Lai et al., 2017; Trischler et al., 2017; Rajpurkar et al., 2018; Yu et al., 2020) | Trischler et al., 2017 | parenthetical_author_year | citing_paper_not_in_aligned_graph | out_of_graph | False |  | In recent years, popular MRC datasets (Richardson et al., 2013; Chen et al., 2016; Lai et al., 2017; Trischler et al., 2017; Rajpurkar et al., 2018; Yu et al., 2020) have consis... |
| out_of_graph | ctxr_6ba1557661e101d4b16a | ctx_5419e432b48c6455bfa6 | 2022.naacl-main.88 | unknown | (Ippolito et al., 2020; Munir et al., 2021) | Munir et al., 2021 | parenthetical_author_year | citing_paper_not_in_aligned_graph | out_of_graph | False |  | Similar results can also be found in (Ippolito et al., 2020; Munir et al., 2021) . |
| out_of_graph | ctxr_f255115c800689b6407f | ctx_4053b184f169539b3516 | 2020.findings-emnlp.143 | related_work | (Popowich, 2005; Van Arkel et al., 2013) | Popowich, 2005 | parenthetical_author_year | citing_paper_not_in_aligned_graph | out_of_graph | False |  | The technology is used for assessing fraud risk in health care claims (Popowich, 2005; Van Arkel et al., 2013) and financial reports (Seemakurthi et al., 2015; Goel and Uzuner, ... |
| out_of_graph | ctxr_bc7cb694b5edd0b81b52 | ctx_6697db31c9e6f39255b1 | 2021.ranlp-srw.22 | introduction | (Batali, 1998; Kirby, 1999; Levin, 1995; Kirby, 2001) | Kirby, 2001 | parenthetical_author_year | citing_paper_not_in_aligned_graph | out_of_graph | False |  | Within this perspective, a plethora of works suggested to use Genetic Algorithms (GA), an optimization method inspired by evolutionary principles, in order to investigate typolo... |
| strong_author_year | ctxr_30fbbbf08a803293d10e | ctx_5c3eb44050e1fc8f8082 | N13-1076 | dataset | (Hovy et al., 2006) | Hovy et al., 2006 | parenthetical_author_year | author_year_clear | strong_author_year | True | {O}nto{N}otes: The 90{\%} Solution | Further, OntoNotes contains named entity annotations for Arabic (Hovy et al., 2006) . |
| strong_author_year | ctxr_2389663c72663023e597 | ctx_9799ebebe80de1ef9caf | I17-1051 | model | Duong et al. (2016) | Duong et al. (2016) | narrative_author_year | author_year_clear | strong_author_year | True | Learning Crosslingual Word Embeddings without Bilingual Corpora | A lower-cost alternative to these expensive jointly trained models was proposed by Duong et al. (2016) and later used to project multiple languages in the same vector space (Duo... |
| strong_author_year | ctxr_21ea5f5f960a19e5c427 | ctx_cdee3a1a2523b25f7f4f | 2020.emnlp-main.311 | related_work | (Malmaud et al., 2014; Jermsurawong and Habash, 2015) | Jermsurawong and Habash, 2015 | parenthetical_author_year | author_year_clear | strong_author_year | True | Predicting the Structure of Cooking Recipes | Recipes have been gaining interest in recent researches, including recipe processing (Mori et al., 2012 (Mori et al., , 2014 Bosselut et al., 2017) , recipe parsing (Malmaud et ... |
| strong_author_year | ctxr_7a7be45fa77ca9710c80 | ctx_c2ea42d13492a7644a87 | 2020.coling-main.477 | model | (Jacovi et al., 2018) | Jacovi et al., 2018 | parenthetical_author_year | author_year_clear | strong_author_year | True | Understanding Convolutional Neural Networks for Text Classification | We do this by considering the contribution of each filter to the two target classes, which is defined by the parameters in W ∈ R d+d×2 (Jacovi et al., 2018) . |
| strong_author_year | ctxr_52465f689e82ce3ec27d | ctx_3a0492060c6eb1b83f4c | 2022.acl-long.317 | introduction | (Wang et al., 2019; Wadden et al., 2019; Lin et al., 2020) | Lin et al., 2020 | parenthetical_author_year | author_year_clear | strong_author_year | True | A Joint Neural Model for Information Extraction with Global Features | Compared to the traditional classification-based models (Wang et al., 2019; Wadden et al., 2019; Lin et al., 2020) , they better capture the structures and dependencies between ... |
| unresolved | ctxr_fe2454e56df526b8fc9e | ctx_a965b50ed68a00d4c0f2 | P13-1013 | unknown | (Xue, 2001; Ma et al., 2012) | Xue, 2001 | parenthetical_author_year | bibliography_unresolved | unresolved | False |  | Chinese words have internal structures (Xue, 2001; Ma et al., 2012) . |
| unresolved | ctxr_7725d18837973abebe0d | ctx_22ac98f3d9507c6debfa | W19-5334 | model | (Vaswani et al., 2017) | Vaswani et al., 2017 | parenthetical_author_year | bibliography_unresolved | unresolved | False |  | We trained only base transformer models (Vaswani et al., 2017) in all language pairs except for Fr→De and En→Lt, where we also tried experimenting with a big transformer. |
| unresolved | ctxr_92c91755210f57897baa | ctx_a1767fb0f80cb7107f15 | 2020.acl-srw.42 | model | (Andreas et al., 2016; Hudson and Manning, 2018; Johnson et al., 2017; Perez et al., 2018; Hu et al., 2017) | Perez et al., 2018 | parenthetical_author_year | bibliography_unresolved | unresolved | False |  | In particular, the issue has been explored in the visual-question answering (VQA) setting (Andreas et al., 2016; Hudson and Manning, 2018; Johnson et al., 2017; Perez et al., 20... |
| unresolved | ctxr_bcd0582d495d1072ba86 | ctx_dcdb5a38f9bcb1cd0ac1 | 2020.coling-main.367 | introduction | (Zhang et al., 2014; Gkotsis et al., 2016; Shen et al., 2020) | Shen et al., 2020 | parenthetical_author_year | bibliography_unresolved | unresolved | False |  | Conversational Emotion Recognition (CER) has attracted increasing interests for its promising applications in intelligent interactive systems with diverse functionalities, inclu... |
| unresolved | ctxr_126998e77b7b16cceb53 | ctx_cc8a8195fc8eace5b993 | N15-1173 | model | (Lin et al., 2014) | Lin et al., 2014 | parenthetical_author_year | bibliography_unresolved | unresolved | False |  | LSTM-YT coco is first trained on the COCO2014 (Lin et al., 2014) dataset and then fine-tuned on the video dataset. |
| weak_nonfirst_author | ctxr_5fe461f06f48bc236278 | ctx_4b3241254a0d6db441bb | J15-3003 | unknown | Ordelman (2006) | Ordelman (2006) | narrative_author_year | author_year_weak_nonfirst_author | weak_nonfirst_author | False | Annotating Emotions in Meetings | As explained by Reidsma, Heylen, and Ordelman (2006) , because of the lack of specialized coefficients coping with unitizing, a fairly standard practice is to use categorization... |
| weak_nonfirst_author | ctxr_bcf143d52fb149280de7 | ctx_747ba3860a34b885d68e | J14-1004 | unknown | (Ushioda 1996; Miller, Guinness, and Zamanian 2004; Koo, Carreras, and Collins 2008; Lin and Wu 2009; Ratinov and Roth 2009) | Koo, Carreras, and Collins 2008 | parenthetical_author_year | author_year_weak_nonfirst_author | weak_nonfirst_author | False | Simple Semi-supervised Dependency Parsing | Nevertheless, this model closely mirrors many of the clustering algorithms used in previous approaches to representation learning for sequence labeling (Ushioda 1996; Miller, Gu... |
| weak_nonfirst_author | ctxr_0a3fe7575410a194e9a3 | ctx_f2a6017a824eff74e7c9 | W08-2204 | unknown | (Flickinger, 2000) | Flickinger, 2000 | parenthetical_author_year | author_year_weak_nonfirst_author | weak_nonfirst_author | False | An Open Source Grammar Development Environment and Broad-coverage {E}nglish Grammar Using {HPSG} | In addition, there are grammar engineering techniques that improve efficiency (e.g. (Flickinger, 2000) ) that are also exploited in our implementation. |
| weak_nonfirst_author | ctxr_6ab1931adf51fe0d8b37 | ctx_88370ec3bb5a6afbc060 | D13-1060 | related_work | Tiedemann (2006) | Tiedemann (2006) | narrative_author_year | author_year_weak_nonfirst_author | weak_nonfirst_author | False | Identifying idiomatic expressions using automatic word-alignment | Villada Moirón and Tiedemann (2006) use word-aligned parallel corpora to identify Dutch MWEs, testing the assumption that the distributions of alignments of MWEs will generally ... |
| weak_nonfirst_author | ctxr_be079ef9b2a24670abc5 | ctx_628b59efb5c5b54061b4 | W15-2115 | unknown | Temperley (2007) | Temperley (2007) | narrative_author_year | author_year_weak_nonfirst_author | weak_nonfirst_author | False | Optimizing Grammars for Minimum Dependency Length | Temperley (2007) finds evidence for DLM in a variety of syntactic choice phenomena in written English. |
| weak_year_only | ctxr_3d6abdb1360fc142e5b4 | ctx_19b815c6b4238f69ee45 | P16-1015 | unknown | (2009) | 2009 | year_only | year_only_unique_candidate | weak_year_only | False | Non-Projective Dependency Parsing in Expected Linear Time | The definition is mostly equivalent to that of Kübler et al. (2009) but deviates in the potential handling of the root on the right (Ballesteros and Nivre, 2013) . |
| weak_year_only | ctxr_0553f7e932bc32b03338 | ctx_23e260d3f971b660ca36 | 2020.lrec-1.507 | acknowledgement | (2012) | 2012 | year_only | year_only_unique_candidate | weak_year_only | False | A Universal Part-of-Speech Tagset | Petrov, S., Das, D., and McDonald, R. (2012). "A Universal Part-of-Speech Tagset". |
| weak_year_only | ctxr_fff9cedb8995159ea4cb | ctx_5043602adfe197b4cc8c | 2021.emnlp-main.376 | unknown | (2021) | 2021 | year_only | year_only_unique_candidate | weak_year_only | False | Introducing Orthogonal Constraint in Structural Probes | In line with the findings of Limisiewicz and Mareček (2021) we have observed that in multilingual setting Orthogonal Structural Probes disentangle the subspaces responsible for ... |
| weak_year_only | ctxr_1c0a569801fe18a870d6 | ctx_64a0f3580e278a5f42d6 | P17-1160 | introduction | (2012) | 2012 | year_only | year_only_unique_candidate | weak_year_only | False | Refining the Design of a Contracting Finite-State Dependency Parser | Cubic-time parsing algorithms that are incidentally or intentionally applicable to this kind of homomorphic representations have been considered, e.g., by Nederhof and Satta (20... |
| weak_year_only | ctxr_b8f6b2b857ad47ad6376 | ctx_1dda515eb98ca05edd8d | W13-2314 | unknown | (1989) | 1989 | year_only | year_only_unique_candidate | weak_year_only | False | Getting at Discourse Referents | This confirmsPassonneau's (1989) observation that nonnominal antecedents tend to be close to the anaphors. |
