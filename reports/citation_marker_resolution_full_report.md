# Citation Marker Resolution Report

## Inputs
| name | path |
| --- | --- |
| citation_contexts | data/processed/citation_contexts_sectioned.parquet |
| acl_citation_graph_aligned | data/interim/acl_citation_graph_aligned.parquet |
| acl_id_crosswalk | data/interim/acl_id_crosswalk.parquet |

## Outputs
| name | path |
| --- | --- |
| citation_contexts_resolved | data/processed/citation_contexts_resolved.parquet |
| citation_marker_resolution_failures | data/processed/citation_marker_resolution_failures.parquet |

- Limit: all
- Random sample: False

## Core Metrics
| metric | value |
| --- | --- |
| total input contexts processed | 1990689 |
| output rows | 3152073 |
| duplicate context_id count before | 0 |
| duplicate context_id count after | 0 |
| duplicate source_context_id count | 1161384 |
| citing_paper_id coverage in aligned graph | 0.882 |
| author_year_clear count | 1188319 |
| author_year_clear rate | 0.377 |
| weak_year_only count | 8931 |
| weak_year_only rate | 0.003 |
| author_year_weak_nonfirst_author count | 15936 |
| author_year_weak_nonfirst_author rate | 0.005 |
| multi_candidate_ambiguous rate | 0.018 |
| ambiguous_year_only rate | 0.005 |
| numeric_marker_unresolved_no_bibliography rate | 0.027 |
| numeric_marker_unresolved_no_bibliography count | 85782 |
| bibliography_unresolved rate | 0.493 |
| bibliography_unresolved count | 1554802 |
| resolved_cited_title non-empty rate | 0.385 |
| resolved_cited_title non-empty rate for strong rows | 1.000 |
| is_strongly_resolved count | 1188307 |
| is_strongly_resolved rate | 0.377 |

## Marker Type Distribution
| marker_type | rows |
| --- | --- |
| parenthetical_author_year | 2648550 |
| narrative_author_year | 384795 |
| numeric | 85782 |
| year_only | 32946 |

## Resolution Status Distribution
| status | rows |
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

## Resolution Status By Normalized Section
| normalized_section | resolution_status | rows |
| --- | --- | --- |
| abstract | bibliography_unresolved | 6025 |
| abstract | author_year_clear | 4602 |
| abstract | citing_paper_not_in_aligned_graph | 1555 |
| abstract | numeric_marker_unresolved_no_bibliography | 863 |
| abstract | multi_candidate_ambiguous | 274 |
| abstract | ambiguous_year_only | 187 |
| abstract | author_year_weak_nonfirst_author | 104 |
| abstract | year_only_unique_candidate | 100 |
| acknowledgement | bibliography_unresolved | 2504 |
| acknowledgement | author_year_clear | 358 |
| acknowledgement | citing_paper_not_in_aligned_graph | 333 |
| acknowledgement | ambiguous_year_only | 115 |
| acknowledgement | year_only_unique_candidate | 106 |
| acknowledgement | numeric_marker_unresolved_no_bibliography | 64 |
| acknowledgement | multi_candidate_ambiguous | 11 |
| acknowledgement | author_year_weak_nonfirst_author | 7 |
| analysis | bibliography_unresolved | 11999 |
| analysis | author_year_clear | 7526 |
| analysis | citing_paper_not_in_aligned_graph | 2218 |
| analysis | numeric_marker_unresolved_no_bibliography | 790 |
| analysis | multi_candidate_ambiguous | 343 |
| analysis | author_year_weak_nonfirst_author | 129 |
| analysis | ambiguous_year_only | 109 |
| analysis | year_only_unique_candidate | 59 |
| appendix | bibliography_unresolved | 1974 |
| appendix | author_year_clear | 974 |
| appendix | citing_paper_not_in_aligned_graph | 444 |
| appendix | numeric_marker_unresolved_no_bibliography | 437 |
| appendix | ambiguous_year_only | 66 |
| appendix | year_only_unique_candidate | 42 |
| appendix | multi_candidate_ambiguous | 35 |
| appendix | author_year_weak_nonfirst_author | 24 |
| background | bibliography_unresolved | 29016 |
| background | author_year_clear | 17069 |
| background | citing_paper_not_in_aligned_graph | 4328 |
| background | numeric_marker_unresolved_no_bibliography | 1104 |
| background | multi_candidate_ambiguous | 714 |
| background | author_year_weak_nonfirst_author | 269 |
| background | ambiguous_year_only | 193 |
| background | year_only_unique_candidate | 138 |
| conclusion | bibliography_unresolved | 21576 |
| conclusion | author_year_clear | 16322 |
| conclusion | citing_paper_not_in_aligned_graph | 3166 |
| conclusion | numeric_marker_unresolved_no_bibliography | 1520 |
| conclusion | multi_candidate_ambiguous | 842 |
| conclusion | author_year_weak_nonfirst_author | 296 |
| conclusion | ambiguous_year_only | 276 |
| conclusion | year_only_unique_candidate | 194 |
| dataset | bibliography_unresolved | 69481 |
| dataset | author_year_clear | 54387 |
| dataset | citing_paper_not_in_aligned_graph | 9620 |
| dataset | numeric_marker_unresolved_no_bibliography | 3984 |
| dataset | multi_candidate_ambiguous | 3077 |
| dataset | ambiguous_year_only | 816 |
| dataset | author_year_weak_nonfirst_author | 717 |
| dataset | year_only_unique_candidate | 468 |
| discussion | bibliography_unresolved | 18012 |
| discussion | author_year_clear | 11045 |
| discussion | citing_paper_not_in_aligned_graph | 4376 |
| discussion | numeric_marker_unresolved_no_bibliography | 953 |
| discussion | multi_candidate_ambiguous | 478 |
| discussion | author_year_weak_nonfirst_author | 224 |
| discussion | ambiguous_year_only | 190 |
| discussion | year_only_unique_candidate | 101 |
| error_analysis | author_year_clear | 929 |
| error_analysis | bibliography_unresolved | 925 |
| error_analysis | numeric_marker_unresolved_no_bibliography | 323 |
| error_analysis | citing_paper_not_in_aligned_graph | 105 |
| error_analysis | multi_candidate_ambiguous | 44 |
| error_analysis | ambiguous_year_only | 18 |
| error_analysis | year_only_unique_candidate | 14 |
| error_analysis | author_year_weak_nonfirst_author | 10 |
| evaluation | bibliography_unresolved | 26507 |
| evaluation | author_year_clear | 25972 |
| evaluation | citing_paper_not_in_aligned_graph | 3899 |
| evaluation | numeric_marker_unresolved_no_bibliography | 2224 |
| evaluation | multi_candidate_ambiguous | 1420 |
| evaluation | ambiguous_year_only | 466 |
| evaluation | author_year_weak_nonfirst_author | 316 |
| evaluation | year_only_unique_candidate | 217 |
| experiment | bibliography_unresolved | 39154 |
| experiment | author_year_clear | 39100 |
| experiment | citing_paper_not_in_aligned_graph | 4784 |
| experiment | numeric_marker_unresolved_no_bibliography | 2884 |
| experiment | multi_candidate_ambiguous | 2074 |
| experiment | ambiguous_year_only | 591 |
| experiment | author_year_weak_nonfirst_author | 325 |
| experiment | year_only_unique_candidate | 255 |
| implementation | bibliography_unresolved | 5821 |
| implementation | author_year_clear | 3322 |
| implementation | citing_paper_not_in_aligned_graph | 946 |
| implementation | numeric_marker_unresolved_no_bibliography | 532 |
| implementation | multi_candidate_ambiguous | 160 |
| implementation | ambiguous_year_only | 43 |
| implementation | author_year_weak_nonfirst_author | 43 |
| implementation | year_only_unique_candidate | 26 |
| introduction | bibliography_unresolved | 433797 |
| introduction | author_year_clear | 342742 |
| introduction | citing_paper_not_in_aligned_graph | 65466 |
| introduction | multi_candidate_ambiguous | 15251 |
| introduction | numeric_marker_unresolved_no_bibliography | 12751 |
| introduction | author_year_weak_nonfirst_author | 3625 |
| introduction | ambiguous_year_only | 2209 |
| introduction | year_only_unique_candidate | 1401 |
| method | bibliography_unresolved | 42857 |
| method | author_year_clear | 28484 |
| method | citing_paper_not_in_aligned_graph | 5434 |
| method | numeric_marker_unresolved_no_bibliography | 3180 |
| method | multi_candidate_ambiguous | 1430 |
| method | ambiguous_year_only | 504 |
| method | author_year_weak_nonfirst_author | 490 |
| method | year_only_unique_candidate | 262 |
| model | bibliography_unresolved | 55261 |
| model | author_year_clear | 40179 |
| model | citing_paper_not_in_aligned_graph | 6620 |
| model | numeric_marker_unresolved_no_bibliography | 4148 |
| model | multi_candidate_ambiguous | 2145 |
| model | ambiguous_year_only | 591 |
| model | author_year_weak_nonfirst_author | 486 |
| model | year_only_unique_candidate | 271 |
| references | bibliography_unresolved | 2723 |
| references | author_year_clear | 2341 |
| references | citing_paper_not_in_aligned_graph | 442 |
| references | ambiguous_year_only | 217 |
| references | year_only_unique_candidate | 188 |
| references | numeric_marker_unresolved_no_bibliography | 185 |
| references | multi_candidate_ambiguous | 162 |
| references | author_year_weak_nonfirst_author | 56 |
| related_work | bibliography_unresolved | 295704 |
| related_work | author_year_clear | 276977 |
| related_work | citing_paper_not_in_aligned_graph | 33614 |
| related_work | multi_candidate_ambiguous | 11441 |
| related_work | numeric_marker_unresolved_no_bibliography | 3999 |
| related_work | ambiguous_year_only | 3040 |
| related_work | author_year_weak_nonfirst_author | 2161 |
| related_work | year_only_unique_candidate | 1334 |
| results | author_year_clear | 16808 |
| results | bibliography_unresolved | 15978 |
| results | citing_paper_not_in_aligned_graph | 2895 |
| results | numeric_marker_unresolved_no_bibliography | 1455 |
| results | multi_candidate_ambiguous | 953 |
| results | ambiguous_year_only | 385 |
| results | author_year_weak_nonfirst_author | 193 |
| results | year_only_unique_candidate | 159 |
| system_description | author_year_clear | 2886 |
| system_description | bibliography_unresolved | 2345 |
| system_description | citing_paper_not_in_aligned_graph | 395 |
| system_description | numeric_marker_unresolved_no_bibliography | 387 |
| system_description | multi_candidate_ambiguous | 177 |
| system_description | ambiguous_year_only | 41 |
| system_description | author_year_weak_nonfirst_author | 36 |
| system_description | year_only_unique_candidate | 16 |
| task_definition | bibliography_unresolved | 2657 |
| task_definition | author_year_clear | 2481 |
| task_definition | citing_paper_not_in_aligned_graph | 487 |
| task_definition | numeric_marker_unresolved_no_bibliography | 168 |
| task_definition | multi_candidate_ambiguous | 121 |
| task_definition | ambiguous_year_only | 25 |
| task_definition | author_year_weak_nonfirst_author | 24 |
| task_definition | year_only_unique_candidate | 15 |
| unknown | bibliography_unresolved | 470486 |
| unknown | author_year_clear | 293815 |
| unknown | citing_paper_not_in_aligned_graph | 74548 |
| unknown | numeric_marker_unresolved_no_bibliography | 43831 |
| unknown | multi_candidate_ambiguous | 14693 |
| unknown | ambiguous_year_only | 6701 |
| unknown | author_year_weak_nonfirst_author | 6401 |
| unknown | year_only_unique_candidate | 3565 |

## Strong Resolution Rate By Normalized Section
| normalized_section | rows | strong_rows | strong_rate |
| --- | --- | --- | --- |
| unknown | 914040 | 293812 | 0.321 |
| introduction | 877242 | 342737 | 0.391 |
| related_work | 628270 | 276975 | 0.441 |
| dataset | 142550 | 54386 | 0.382 |
| model | 109701 | 40179 | 0.366 |
| experiment | 89167 | 39099 | 0.438 |
| method | 82641 | 28484 | 0.345 |
| evaluation | 61021 | 25972 | 0.426 |
| background | 52831 | 17069 | 0.323 |
| conclusion | 44192 | 16322 | 0.369 |
| results | 38826 | 16808 | 0.433 |
| discussion | 35379 | 11045 | 0.312 |
| analysis | 23173 | 7526 | 0.325 |
| abstract | 13710 | 4602 | 0.336 |
| implementation | 10893 | 3322 | 0.305 |
| references | 6314 | 2341 | 0.371 |
| system_description | 6283 | 2886 | 0.459 |
| task_definition | 5978 | 2481 | 0.415 |
| appendix | 3996 | 974 | 0.244 |
| acknowledgement | 3498 | 358 | 0.102 |
| error_analysis | 2368 | 929 | 0.392 |

## Large Citation Group Flags By Resolution Status
| resolution_status | rows | flagged_rows | flagged_rate |
| --- | --- | --- | --- |
| numeric_marker_unresolved_no_bibliography | 85782 | 1325 | 0.015 |
| ambiguous_year_only | 16783 | 0 | 0.000 |
| author_year_clear | 1188319 | 0 | 0.000 |
| author_year_weak_nonfirst_author | 15936 | 0 | 0.000 |
| bibliography_unresolved | 1554802 | 0 | 0.000 |
| citing_paper_not_in_aligned_graph | 225675 | 0 | 0.000 |
| multi_candidate_ambiguous | 55845 | 0 | 0.000 |
| year_only_unique_candidate | 8931 | 0 | 0.000 |

## Suspicious Citation Range Flags By Resolution Status
| resolution_status | rows | flagged_rows | flagged_rate |
| --- | --- | --- | --- |
| numeric_marker_unresolved_no_bibliography | 85782 | 1176 | 0.014 |
| ambiguous_year_only | 16783 | 0 | 0.000 |
| author_year_clear | 1188319 | 0 | 0.000 |
| author_year_weak_nonfirst_author | 15936 | 0 | 0.000 |
| bibliography_unresolved | 1554802 | 0 | 0.000 |
| citing_paper_not_in_aligned_graph | 225675 | 0 | 0.000 |
| multi_candidate_ambiguous | 55845 | 0 | 0.000 |
| year_only_unique_candidate | 8931 | 0 | 0.000 |

## Before / After Comparison
| metric | before | after |
| --- | --- | --- |
| output_rows | 151401 | 3152073 |
| author_year_clear_rate | 0.339 | 0.377 |
| ambiguous_year_only_count | 8763 | 16783 |
| year_only_unique_candidate_count | 4680 | 8931 |
| bibliography_unresolved_count | 64573 | 1554802 |
| duplicate_context_id_count | 0 | 0 |

## 20 Examples: author_year_clear
| context_id | source_context_id | citing_paper_id | raw_section_name | normalized_section | citation_marker | marker_type | marker_component_text | parsed_surnames | parsed_year | parsed_year_suffix | resolved_cited_acl_id | resolved_cited_title | matched_candidate_count | resolution_status | resolution_level | is_strongly_resolved | resolution_confidence | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_4771edcc3e42c8bb07c7 | ctx_4c265fc01e3bc9f11872 | R13-1042 | Introduction | introduction | Elsner and Charniak (2010) | narrative_author_year | Elsner and Charniak (2010) | elsner;charniak | 2010 | unavailable | J10-3004 | Disentangling Chat | 1 | author_year_clear | strong_author_year | True | 0.95 | In NLP, Elsner and Charniak (2010) described the task of thread disentanglement as "the clustering task of dividing a transcript into a s... |
| ctxr_fc94564ed0054ac2126f | ctx_e7f13d44394b4c7c137f | R13-1042 | Introduction | introduction | (Elsner and Charniak, 2010) | parenthetical_author_year | Elsner and Charniak, 2010 | elsner;charniak | 2010 | unavailable | J10-3004 | Disentangling Chat | 1 | author_year_clear | strong_author_year | True | 0.95 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_d06d69e8921c81b378ac | ctx_0f0eb448b401dd51cdf3 | R13-1042 | Introduction | introduction | Carenini et al. (2008) | narrative_author_year | Carenini et al. (2008) | carenini | 2008 | unavailable | P08-1041 | Summarizing Emails with Conversational Cohesion and Subjectivity | 1 | author_year_clear | strong_author_year | True | 0.9 | Carenini et al. (2008) annotated 39 email "conversations" from the Enron Email Corpus for email summariation. |
| ctxr_68d4edb5f20b826f715b | ctx_5316b90745ae591db502 | R13-1042 | Introduction | introduction | Wan and McKeown (2004) | narrative_author_year | Wan and McKeown (2004) | wan;mckeown | 2004 | unavailable | C04-1079 | Generating Overview Summaries of Ongoing Email Thread Discussions | 1 | author_year_clear | strong_author_year | True | 0.95 | Wan and McKeown (2004) used a privatelyavailable corpus of 300 threads for summary generation. |
| ctxr_b166bf8511a77353542f | ctx_c272b15a642e8261f522 | R13-1042 | Introduction | introduction | Rambow et al. (2004) | narrative_author_year | Rambow et al. (2004) | rambow | 2004 | unavailable | N04-4027 | Summarizing Email Threads | 1 | author_year_clear | strong_author_year | True | 0.9 | Rambow et al. (2004) used a privatelyavailable corpus of 96 email threads for thread summarization. |
| ctxr_6739ef248e0241672c80 | ctx_749b7cb80bcc70164ca3 | R13-1042 | Gold Standard Thread Extraction from the Enron Email Corpus | dataset | Wan and McKeown (2004) | narrative_author_year | Wan and McKeown (2004) | wan;mckeown | 2004 | unavailable | C04-1079 | Generating Overview Summaries of Ongoing Email Thread Discussions | 1 | author_year_clear | strong_author_year | True | 0.95 | Wan and McKeown (2004) reconstructed threads by header Message-ID information. |
| ctxr_4ba57d063d3c71fa78df | ctx_82c232f3d1dfc98f4dff | R13-1042 | Gold Standard Thread Extraction from the Enron Email Corpus | dataset | Rambow et al. (2004) | narrative_author_year | Rambow et al. (2004) | rambow | 2004 | unavailable | N04-4027 | Summarizing Email Threads | 1 | author_year_clear | strong_author_year | True | 0.9 | Rambow et al. (2004) used a privately-available corpus of 96 email threads, but did not specify how they determined the threads. |
| ctxr_8361b89d504826d53df9 | ctx_e5dad8f0492b6fb3d95b | R13-1042 | Text Similarity Features | unknown | (Hatzivassiloglou et al., 1999) | parenthetical_author_year | Hatzivassiloglou et al., 1999 | hatzivassiloglou | 1999 | unavailable | W99-0625 | Detecting Text Similarity over Short Passages: Exploring Linguistic Feature Combinations via Machine Learning | 1 | author_year_clear | strong_author_year | True | 0.9 | 1999 ) uses pairs of words occurring in the same order for the two emails; Token Pair Distance (Hatzivassiloglou et al., 1999) measures t... |
| ctxr_d573e73d4a69363cdfc0 | ctx_2058502beaf095f8c9d9 | R13-1042 | Results | results | Elsner and Charniak (2011) | narrative_author_year | Elsner and Charniak (2011) | elsner;charniak | 2011 | unavailable | P11-1118 | Disentangling Chat with Local Coherence Models | 1 | author_year_clear | strong_author_year | True | 0.95 | Elsner and Charniak (2011) use coherence models to disentangle chat, using some features (entity grid, topical entity grid) which corresp... |
| ctxr_044c96a8f9c2342b58ff | ctx_871fbe98e387051e0e49 | R13-1044 | Related work | related_work | (Rosario and Hearst, 2001 ) | parenthetical_author_year | Rosario and Hearst, 2001 | rosario;hearst | 2001 | unavailable | W01-0511 | Classifying the Semantic Relations in Noun Compounds via a Domain-Specific Lexical Hierarchy | 1 | author_year_clear | strong_author_year | True | 0.95 | In (Rosario and Hearst, 2001 ) authors used neural networks to determine 20 semantic relationssimilarily to (Nastase et al., 2006) -betwe... |
| ctxr_f6863fcab52657a5c16e | ctx_f31d14d5a204a23fdb80 | R13-1044 | Related work | related_work | (Tratz and Hovy, 2010) | parenthetical_author_year | Tratz and Hovy, 2010 | tratz;hovy | 2010 | unavailable | S10-1049 | {ISI}: Automatic Classification of Relations Between Nominals Using a Maximum Entropy Classifier | 1 | author_year_clear | strong_author_year | True | 0.95 | In (Tratz and Hovy, 2010) the authors developed a system based on the Maximum Entropy classifier, able to detect 10 bidirectional semanti... |
| ctxr_71d08900475d9c8505ab | ctx_fe6ec05f96144fa5a36e | R13-1044 | Related work | related_work | (Rink and Harabagiu, 2010) | parenthetical_author_year | Rink and Harabagiu, 2010 | rink;harabagiu | 2010 | unavailable | S10-1057 | {UTD}: Classifying Semantic Relations by Combining Lexical and Semantic Resources | 1 | author_year_clear | strong_author_year | True | 0.95 | The same set of semantic relations was used in (Rink and Harabagiu, 2010) . |
| ctxr_b1bfb1536bcb5cbbf8b5 | ctx_797eaae178b0d5c3ea41 | R13-1044 | Related work | related_work | (Tymoshenko and Giuliano, 2010 ) | parenthetical_author_year | Tymoshenko and Giuliano, 2010 | tymoshenko;giuliano | 2010 | unavailable | S10-1047 | {FBK}-{IRST}: Semantic Relation Extraction Using {C}yc | 1 | author_year_clear | strong_author_year | True | 0.95 | Authors in (Tymoshenko and Giuliano, 2010 ) used shallow syntactic parsing and semantic information from ResearchCyc (Lenat, 1995) in the... |
| ctxr_f8a4c2e6aa2834642a71 | ctx_35ba2ace18b7d4ee7211 | R13-1044 | Related work | related_work | (Hearst, 1992) | parenthetical_author_year | Hearst, 1992 | hearst | 1992 | unavailable | C92-2082 | Automatic Acquisition of Hyponyms from Large Text Corpora | 1 | author_year_clear | strong_author_year | True | 0.9 | In (Hearst, 1992) authors used set of manually written rules for identification of hyperonymy relations. (Ben Abacha and Zweigenbaum, 201... |
| ctxr_3e4722d1950da619a7dd | ctx_ca6cc2ce8812268acdb7 | R13-1044 | Recognizing word pairs and triples | unknown | (Broda et al., 2012) | parenthetical_author_year | Broda et al., 2012 | broda | 2012 | unavailable | L12-1574 | {KPW}r: Towards a Free Corpus of {P}olish | 1 | author_year_clear | strong_author_year | True | 0.9 | We made use of a CRF shallow parser (Radziszewski and Pawlaczek, 2012) trained on an annotated corpus of Polish (KPWr) (Broda et al., 201... |
| ctxr_9ab7ad32be76baef24a4 | ctx_31e57195fc09648f4ccb | W05-0818 | Introduction | introduction | (Ayan et al., 2004; Och and Ney, 2000) | parenthetical_author_year | Ayan et al., 2004 | ayan | 2004 | unavailable | 2004.amta-papers.3 | Multi-Align: combining linguistic and statistical techniques to improve alignments for adaptable {MT} | 1 | author_year_clear | strong_author_year | True | 0.9 | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-ba... |
| ctxr_008f302607deda562c24 | ctx_31e57195fc09648f4ccb | W05-0818 | Introduction | introduction | (Ayan et al., 2004; Och and Ney, 2000) | parenthetical_author_year | Och and Ney, 2000 | och;ney | 2000 | unavailable | P00-1056 | Improved Statistical Alignment Models | 1 | author_year_clear | strong_author_year | True | 0.95 | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-ba... |
| ctxr_373b75e6049f7bde6cca | ctx_e70cc82cf2e10336956d | W05-0818 | Introduction | introduction | (Ayan et al., 2004; Och and Ney, 2000) | parenthetical_author_year | Ayan et al., 2004 | ayan | 2004 | unavailable | 2004.amta-papers.3 | Multi-Align: combining linguistic and statistical techniques to improve alignments for adaptable {MT} | 1 | author_year_clear | strong_author_year | True | 0.9 | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-ba... |
| ctxr_18b9cd4865ae3fef4d3f | ctx_e70cc82cf2e10336956d | W05-0818 | Introduction | introduction | (Ayan et al., 2004; Och and Ney, 2000) | parenthetical_author_year | Och and Ney, 2000 | och;ney | 2000 | unavailable | P00-1056 | Improved Statistical Alignment Models | 1 | author_year_clear | strong_author_year | True | 0.95 | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-ba... |
| ctxr_7d7d31957a351c96c69d | ctx_b950942cfc6e4043e721 | W05-0818 | Introduction | introduction | (Carl, 2001; Menezes and Richardson, 2001) | parenthetical_author_year | Carl, 2001 | carl | 2001 | unavailable | W01-0718 | Inducing probabilistic invertible translation grammars from aligned texts | 1 | author_year_clear | strong_author_year | True | 0.9 | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-ba... |

## 20 Examples: weak_nonfirst_author
| context_id | source_context_id | citing_paper_id | raw_section_name | normalized_section | citation_marker | marker_type | marker_component_text | parsed_surnames | parsed_year | parsed_year_suffix | resolved_cited_acl_id | resolved_cited_title | matched_candidate_count | resolution_status | resolution_level | is_strongly_resolved | resolution_confidence | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_183e18795fd3e1474a3d | ctx_62b7d2c916aaa43a9102 | R13-1048 | Related Work | related_work | Nivre (2010) | narrative_author_year | Nivre (2010) | nivre | 2010 | unavailable | P10-1151 | A Transition-Based Parser for 2-Planar Dependency Structures | 1 | author_year_weak_nonfirst_author | weak_nonfirst_author | False | 0.55 | In this paper, the 2planar algorithm described in Gómez-Rodríguez and Nivre (2010) will be used, which is able to produce non-projective ... |
| ctxr_51683d2c05401a58b6c5 | ctx_f1283249548232e3613a | 2009.mtsummit-posters.21 | Parallel Coupling | unknown | (Hildebrand/Vogel 2008) | parenthetical_author_year | Hildebrand/Vogel 2008 | vogel | 2008 | unavailable | 2008.amta-srw.3 | Combination of Machine Translation Systems via Hypothesis Selection from Combined N-Best Lists | 1 | author_year_weak_nonfirst_author | weak_nonfirst_author | False | 0.55 | The first approach identifies the best translations from a list of n-best translations (Hildebrand/Vogel 2008) . |
| ctxr_b886d37e8d2c8ccce973 | ctx_2cb057430f176c397e47 | 2009.mtsummit-posters.21 | Pre-editing | unknown | (Koehn/Hoang 2007) | parenthetical_author_year | Koehn/Hoang 2007 | hoang | 2007 | unavailable | D07-1091 | Factored Translation Models | 1 | author_year_weak_nonfirst_author | weak_nonfirst_author | False | 0.55 | Also, it seems that both textform and lemma based analysis should be done, as surface information has also shown to be beneficial (Koehn/... |
| ctxr_a8db25714a87679b1f20 | ctx_1e3f70e3b2b063fb55cf | 2009.mtsummit-posters.21 | Pre-editing | unknown | (Niehues/Kolss 2009) | parenthetical_author_year | Niehues/Kolss 2009 | kolss | 2009 | unavailable | W09-0435 | A {POS}-Based Model for Long-Range Reorderings in {SMT} | 1 | author_year_weak_nonfirst_author | weak_nonfirst_author | False | 0.55 | Distortion rules can be set up manually or automatically, for contiguous and discontinuous POS sequences (Niehues/Kolss 2009), by matchin... |
| ctxr_9df4ea9d27ddceccd798 | ctx_092257b19e198312c1f4 | 2009.mtsummit-posters.21 | Domain Adaptation | unknown | (Koehn/Schroeder 2007) | parenthetical_author_year | Koehn/Schroeder 2007 | schroeder | 2007 | unavailable | W07-0733 | Experiments in Domain Adaptation for Statistical Machine Translation | 1 | author_year_weak_nonfirst_author | weak_nonfirst_author | False | 0.55 | While the phrase tables of the out-ofdomain data moderately improve the in-domain ones (by closing gaps in the translations), the most ef... |
| ctxr_fff645a8c396f61183ec | ctx_d4408012b96662d2953f | 2009.mtsummit-posters.21 | Domain Adaptation | unknown | (Itagaki/Aikawa 2008) | parenthetical_author_year | Itagaki/Aikawa 2008 | aikawa | 2008 | unavailable | L08-1112 | Post-{MT} Term Swapper: Supplementing a Statistical Machine Translation System with a User Dictionary | 1 | author_year_weak_nonfirst_author | weak_nonfirst_author | False | 0.55 | Experiments have also been made for integrating customer terminology (a bilingual list of terms) into an SMT system (Itagaki/Aikawa 2008). |
| ctxr_e2c3bca0bd08410134f1 | ctx_e591dd915c4c40dd1473 | 2009.mtsummit-posters.21 | Conclusion | conclusion | (Nießen/Ney 2004) | parenthetical_author_year | Nießen/Ney 2004 | ney | 2004 | unavailable | J04-2003 | Statistical Machine Translation with Scarce Resources Using Morpho-syntactic Information | 1 | author_year_weak_nonfirst_author | weak_nonfirst_author | False | 0.55 | SMT approaches to lowresource languages are presented e.g. in (Nießen/Ney 2004)  the translation quality which can be achieved, both for... |
| ctxr_b5fea282cd0e2c1b457e | ctx_789c9b7bc1cff26937c9 | R13-1062 | Feature Weighting | unknown | (Hayashi, Watanabe, Tsukada, & Isozaki, 2009) | parenthetical_author_year | Hayashi, Watanabe, Tsukada, & Isozaki, 2009 | tsukada;isozaki | 2009 | unavailable | 2009.iwslt-papers.3 | Structural support vector machines for log-linear approach in statistical machine translation | 1 | author_year_weak_nonfirst_author | weak_nonfirst_author | False | 0.55 | Like (Hayashi, Watanabe, Tsukada, & Isozaki, 2009) , we use SVM-rank to obtain the weight of each feature. |
| ctxr_e7fae89ac3d01a6c6e0c | ctx_135550357f43ba2f9059 | R13-1043 | Background | background | (Fišer, 2007; Sagot, 2008; Shahid, 2009; Shahid, 2010; Lefever, 2009; Lefever, 2010a; Lefever, 2010b) | parenthetical_author_year | Shahid, 2009 | shahid | 2009 | unavailable | W09-4202 | Unsupervised Construction of a Multilingual {W}ord{N}et from Parallel Corpora | 1 | author_year_weak_nonfirst_author | weak_nonfirst_author | False | 0.55 | More recently, parallel corpora have been used to create new linguistic resources, such as lexicons and WordNet-like resources (Fišer, 20... |
| ctxr_361e68eb8d41e03d7093 | ctx_57dc96d67a62e3c9be44 | R13-1043 | Background | background | (Fišer, 2007; Sagot, 2008; Shahid, 2009; Shahid, 2010; Lefever, 2009; Lefever, 2010a; Lefever, 2010b) | parenthetical_author_year | Shahid, 2009 | shahid | 2009 | unavailable | W09-4202 | Unsupervised Construction of a Multilingual {W}ord{N}et from Parallel Corpora | 1 | author_year_weak_nonfirst_author | weak_nonfirst_author | False | 0.55 | More recently, parallel corpora have been used to create new linguistic resources, such as lexicons and WordNet-like resources (Fišer, 20... |
| ctxr_8992073c57427d511173 | ctx_92ff4ae43489697d96cd | R13-1043 | Background | background | (Fišer, 2007; Sagot, 2008; Shahid, 2009; Shahid, 2010; Lefever, 2009; Lefever, 2010a; Lefever, 2010b) | parenthetical_author_year | Shahid, 2009 | shahid | 2009 | unavailable | W09-4202 | Unsupervised Construction of a Multilingual {W}ord{N}et from Parallel Corpora | 1 | author_year_weak_nonfirst_author | weak_nonfirst_author | False | 0.55 | More recently, parallel corpora have been used to create new linguistic resources, such as lexicons and WordNet-like resources (Fišer, 20... |
| ctxr_d3cf3c9c07e7f31171f1 | ctx_b465ce049f1446020daf | R13-1043 | Background | background | (Fišer, 2007; Sagot, 2008; Shahid, 2009; Shahid, 2010; Lefever, 2009; Lefever, 2010a; Lefever, 2010b) | parenthetical_author_year | Shahid, 2009 | shahid | 2009 | unavailable | W09-4202 | Unsupervised Construction of a Multilingual {W}ord{N}et from Parallel Corpora | 1 | author_year_weak_nonfirst_author | weak_nonfirst_author | False | 0.55 | More recently, parallel corpora have been used to create new linguistic resources, such as lexicons and WordNet-like resources (Fišer, 20... |
| ctxr_f955501531f746ff188f | ctx_a6a500e6556821e01844 | R13-1043 | Background | background | (Fišer, 2007; Sagot, 2008; Shahid, 2009; Shahid, 2010; Lefever, 2009; Lefever, 2010a; Lefever, 2010b) | parenthetical_author_year | Shahid, 2009 | shahid | 2009 | unavailable | W09-4202 | Unsupervised Construction of a Multilingual {W}ord{N}et from Parallel Corpora | 1 | author_year_weak_nonfirst_author | weak_nonfirst_author | False | 0.55 | More recently, parallel corpora have been used to create new linguistic resources, such as lexicons and WordNet-like resources (Fišer, 20... |
| ctxr_f7c531583deb9cc989d2 | ctx_0ed8f46b8714158311c4 | R13-1043 | Background | background | (Fišer, 2007; Sagot, 2008; Shahid, 2009; Shahid, 2010; Lefever, 2009; Lefever, 2010a; Lefever, 2010b) | parenthetical_author_year | Shahid, 2009 | shahid | 2009 | unavailable | W09-4202 | Unsupervised Construction of a Multilingual {W}ord{N}et from Parallel Corpora | 1 | author_year_weak_nonfirst_author | weak_nonfirst_author | False | 0.55 | More recently, parallel corpora have been used to create new linguistic resources, such as lexicons and WordNet-like resources (Fišer, 20... |
| ctxr_8597df6b234b1705faeb | ctx_ad10bec6c472952cdd8e | R13-1043 | Background | background | (Fišer, 2007; Sagot, 2008; Shahid, 2009; Shahid, 2010; Lefever, 2009; Lefever, 2010a; Lefever, 2010b) | parenthetical_author_year | Shahid, 2009 | shahid | 2009 | unavailable | W09-4202 | Unsupervised Construction of a Multilingual {W}ord{N}et from Parallel Corpora | 1 | author_year_weak_nonfirst_author | weak_nonfirst_author | False | 0.55 | More recently, parallel corpora have been used to create new linguistic resources, such as lexicons and WordNet-like resources (Fišer, 20... |
| ctxr_f70f19b7334bebef244d | ctx_d306c731c25804e455aa | P12-3016 | Introduction | introduction | (Koehn, 2010) | parenthetical_author_year | Koehn, 2010 | koehn | 2010 | unavailable | W10-1703 | Findings of the 2010 Joint Workshop on Statistical Machine Translation and Metrics for Machine Translation | 1 | author_year_weak_nonfirst_author | weak_nonfirst_author | False | 0.55 | While methods for the use of parallel corpora in machine translation are well studied (Koehn, 2010) , similar techniques for comparable c... |
| ctxr_01b29c7cabedc3dbc024 | ctx_d292849c82e6ccdbdc4c | P12-3016 | Introduction | introduction | (Munteanu and Marcu, 2005; Lu et al., 2010; Smith et al., 2010; Schwenk, 2009 and 2011) | parenthetical_author_year | Schwenk, 2009 and 2011 | schwenk | 2009 | unavailable | E09-1003 | On the Use of Comparable Corpora to Improve {SMT} performance | 1 | author_year_weak_nonfirst_author | weak_nonfirst_author | False | 0.55 | Only the latest research has shown that language pairs and domains with little parallel data can benefit from the exploitation of compara... |
| ctxr_e81ae00be5fcc92069a1 | ctx_aed5dd0fd4d7c841244d | P12-3016 | Introduction | introduction | (Munteanu and Marcu, 2005; Lu et al., 2010; Smith et al., 2010; Schwenk, 2009 and 2011) | parenthetical_author_year | Schwenk, 2009 and 2011 | schwenk | 2009 | unavailable | E09-1003 | On the Use of Comparable Corpora to Improve {SMT} performance | 1 | author_year_weak_nonfirst_author | weak_nonfirst_author | False | 0.55 | Only the latest research has shown that language pairs and domains with little parallel data can benefit from the exploitation of compara... |
| ctxr_e0a3b0256787906c921a | ctx_ca60e3ab67f25d2ec0b4 | P12-3016 | Introduction | introduction | (Munteanu and Marcu, 2005; Lu et al., 2010; Smith et al., 2010; Schwenk, 2009 and 2011) | parenthetical_author_year | Schwenk, 2009 and 2011 | schwenk | 2009 | unavailable | E09-1003 | On the Use of Comparable Corpora to Improve {SMT} performance | 1 | author_year_weak_nonfirst_author | weak_nonfirst_author | False | 0.55 | Only the latest research has shown that language pairs and domains with little parallel data can benefit from the exploitation of compara... |
| ctxr_f6c0714695b298aff097 | ctx_6b7baaba12e84416cce8 | P12-3016 | Introduction | introduction | (Munteanu and Marcu, 2005; Lu et al., 2010; Smith et al., 2010; Schwenk, 2009 and 2011) | parenthetical_author_year | Schwenk, 2009 and 2011 | schwenk | 2009 | unavailable | E09-1003 | On the Use of Comparable Corpora to Improve {SMT} performance | 1 | author_year_weak_nonfirst_author | weak_nonfirst_author | False | 0.55 | Only the latest research has shown that language pairs and domains with little parallel data can benefit from the exploitation of compara... |

## 20 Examples: multi_candidate_ambiguous
| context_id | source_context_id | citing_paper_id | raw_section_name | normalized_section | citation_marker | marker_type | marker_component_text | parsed_surnames | parsed_year | parsed_year_suffix | resolved_cited_acl_id | resolved_cited_title | matched_candidate_count | resolution_status | resolution_level | is_strongly_resolved | resolution_confidence | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_e48cf879e2f66fc29b89 | ctx_ebb2bf87b454fbcc6a35 | W05-0820 | unavailable | unknown | Koehn et al. (2003) | narrative_author_year | Koehn et al. (2003) | koehn | 2003 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | The focus of the task was to build a probabilistic phrase translation table, since most of the other resources were provided -for more on... |
| ctxr_58c25c30dd82c38881bb | ctx_d5504eb13dd65543782a | W05-0820 | Rules of Engagement | unknown | (Och, 2003) | parenthetical_author_year | Och, 2003 | och | 2003 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | However, the field is moving fast, and a number of steps help to improve upon the provided baseline setup, e.g., larger language models t... |
| ctxr_b2167b01cb827f01e9fc | ctx_ac8919acb76fb2ee9d36 | R13-1049 | A Deep-Semantic Representation Level | unknown | Gandon (2013b) | narrative_author_year | Gandon (2013b) | gandon | 2013 | b | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | Lefrançois and Gandon (2013b) therefore introduced a deeper level of representation to describe meanings: the deep semantic level, and de... |
| ctxr_da493e241cd1cd8c2bf6 | ctx_5785da21214d960fe1ce | R13-1049 | Reasoning with UGs-Homomorphisms | unknown | Gandon (2013a) | narrative_author_year | Gandon (2013a) | gandon | 2013 | a | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | Lefrançois and Gandon (2013a) proposed to use the notion of UGs homomorphism to define this entailment problem. |
| ctxr_cce3eff94f503802dcaf | ctx_dc77f495fe41279b99b7 | R13-1049 | Reasoning with UGs-Homomorphisms | unknown | Gandon (2013a) | narrative_author_year | Gandon (2013a) | gandon | 2013 | a | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | More generally, Lefrançois and Gandon (2013a) listed a set of rules which defines the axiomatization of the UGs semantics. |
| ctxr_215af6eda62875174cb7 | ctx_f0f039be652926fe0a20 | R13-1049 | Reasoning with UGs-Homomorphisms | unknown | Gandon (2013a) | narrative_author_year | Gandon (2013a) | gandon | 2013 | a | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | Lefrançois and Gandon (2013a) illustrated problematic cases where the closure is infinite for finite UGs. |
| ctxr_99b12e760624891c3b57 | ctx_12a4a517ae0a5c895ef5 | R13-1049 | Model Semantics for the UGs framework | model | Gandon (2013c) | narrative_author_year | Gandon (2013c) | gandon | 2013 | c | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | Lefrançois and Gandon (2013c) listed the different equations that the interpretation function must satisfy so that a model is a model of ... |
| ctxr_bba4196867a8719d1005 | ctx_d1e8229ece9aef375c4d | R13-1052 | Introduction | introduction | (Teufel et al., 2006a) | parenthetical_author_year | Teufel et al., 2006a | teufel | 2006 | a | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | Therefore, this task has attracted researchers from the fields of discourse analysis, sociology of science, and information sciences for ... |
| ctxr_69a2ba58eff77370d7af | ctx_13eec0405338ff381dc7 | R13-1052 | Introduction | introduction | (Teufel et al., 2006a) | parenthetical_author_year | Teufel et al., 2006a | teufel | 2006 | a | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | Most of the existing research in this area focused on the analysis of citation sentiment, which has achieved good accuracy (see, e.g., (T... |
| ctxr_4bbe9e5dbfade2085ced | ctx_d6bff0684aeeb70b0364 | R13-1052 | Based on + | unknown | Teufel et al. (2006b) | narrative_author_year | Teufel et al. (2006b) | teufel | 2006 | b | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | The weakness of the cited work is discussed Teufel et al. (2006b) is the most related to ours. |
| ctxr_d379efec19d3cd3d2a0b | ctx_fea6387f2f078daebc09 | R13-1052 | Based on + | unknown | Teufel et al. (2006a) | narrative_author_year | Teufel et al. (2006a) | teufel | 2006 | a | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | Regarding the automatic recognition of citation functions or citation categories, Teufel et al. (2006a) presented a supervised learning f... |
| ctxr_87750c2349f5ef2aeb99 | ctx_052f15ac80217fa2f715 | R13-1052 | Based on + | unknown | Teufel et al. (2006a) | narrative_author_year | Teufel et al. (2006a) | teufel | 2006 | a | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | It is also worth noting that Teufel et al. (2006a) , Athar (2011) , and Dong and Schäfer (2011) all worked on citations in computational ... |
| ctxr_9d047da0f9850b5c08ab | ctx_0c4dc34767d14cd0050f | R13-1058 | The construction process | unknown | (Fellbaum, 1998; Broda et al., 2012b) | parenthetical_author_year | Broda et al., 2012b | broda | 2012 | b | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | Wordnet construction is rather like writing a dictionary (Fellbaum, 1998; Broda et al., 2012b) . |
| ctxr_0d1791de0ca1782618cf | ctx_bb4a884a5ada6aa43cf1 | R13-1058 | The construction process | unknown | (Fellbaum, 1998; Broda et al., 2012b) | parenthetical_author_year | Broda et al., 2012b | broda | 2012 | b | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | Wordnet construction is rather like writing a dictionary (Fellbaum, 1998; Broda et al., 2012b) . |
| ctxr_17ffe60329ab0c48240a | ctx_03cf61674e7d40e921fe | R13-1058 | The construction process | unknown | (Broda et al., 2012a) | parenthetical_author_year | Broda et al., 2012a | broda | 2012 | a | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | 10 The corpus consists of 250 million tokens in the ICS PAS Corpus (Przepiórkowski, 2004) ; 113m tokens of news items (Weiss, 2008) ; ≈80... |
| ctxr_35a3a6111af2bb1ca371 | ctx_6c7f26ebd5ac82abdb80 | R13-1058 | The construction process | unknown | (Broda et al., 2012b) | parenthetical_author_year | Broda et al., 2012b | broda | 2012 | b | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | 11 Usage examples, welcome by the editors, help them distinguish senses (Broda et al., 2012b) . ported by WordnetWeaver (Piasecki et al.,... |
| ctxr_c9035d58731a119072ec | ctx_2b0bf0ad417068d2068b | R13-1059 | Grammar induction methods | method | (Black et al., 1992; Jelinek et al., 1992; Jelinek et al., 1994) | parenthetical_author_year | Black et al., 1992 | black | 1992 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | History based models were initially developed at IBM (Black et al., 1992; Jelinek et al., 1992; Jelinek et al., 1994) . |
| ctxr_5692e0cfb59087d20edc | ctx_34db2f8a1266a55afd75 | R13-1059 | Grammar induction methods | method | (Black et al., 1992; Jelinek et al., 1992; Jelinek et al., 1994) | parenthetical_author_year | Black et al., 1992 | black | 1992 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | History based models were initially developed at IBM (Black et al., 1992; Jelinek et al., 1992; Jelinek et al., 1994) . |
| ctxr_062629ccb13e7620e79c | ctx_c0d3ee2530a568a8e76c | R13-1059 | Grammar induction methods | method | (Black et al., 1992; Jelinek et al., 1992; Jelinek et al., 1994) | parenthetical_author_year | Black et al., 1992 | black | 1992 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | History based models were initially developed at IBM (Black et al., 1992; Jelinek et al., 1992; Jelinek et al., 1994) . |
| ctxr_13e7f6a8ac68fa4cdaf1 | ctx_0623b7fee9802a8f6924 | W05-0833 | Abstract | abstract | (Gough & Way, 2004b) | parenthetical_author_year | Gough & Way, 2004b | gough;way | 2004 | b | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | While for the most part the EBMT system of (Gough & Way, 2004b) outperforms any flavour of the phrasebased SMT systems constructed in our... |

## 20 Examples: ambiguous
| context_id | source_context_id | citing_paper_id | raw_section_name | normalized_section | citation_marker | marker_type | marker_component_text | parsed_surnames | parsed_year | parsed_year_suffix | resolved_cited_acl_id | resolved_cited_title | matched_candidate_count | resolution_status | resolution_level | is_strongly_resolved | resolution_confidence | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_77b5217607ceb30638bb | ctx_42406514152d2d31a609 | R13-1042 | Text Similarity Features | unknown | (2011) | year_only | 2011 |  | 2011 | unavailable | unavailable |  | 2 | ambiguous_year_only | ambiguous | False | 0.0 | We evaluate a number of text similarity measures, divided according to Bär et al. (2011) 's three groups: Content Similarity, Structural ... |
| ctxr_44612955c3e496b72ae3 | ctx_f718b60096bff191909c | R13-1042 | Text Similarity Features | unknown | (2011) | year_only | 2011 |  | 2011 | unavailable | unavailable |  | 2 | ambiguous_year_only | ambiguous | False | 0.0 | Stamatatos's Stopword n-grams (2011) capture syntactic similarities, by identifying text reuse where just the content words have been rep... |
| ctxr_8f4e41415475394c6cc2 | ctx_35f19bdc9e1135f061c3 | R13-1046 | Related Work | related_work | (2011a,b) | parenthetical_author_year | 2011a,b |  | 2011 | a | unavailable |  | 3 | ambiguous_year_only | ambiguous | False | 0.0 | Foster et al. (2011a,b) , e.g., note that propagation of POS errors is a serious problem, especially for Twitter data. |
| ctxr_e48cf879e2f66fc29b89 | ctx_ebb2bf87b454fbcc6a35 | W05-0820 | unavailable | unknown | Koehn et al. (2003) | narrative_author_year | Koehn et al. (2003) | koehn | 2003 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | The focus of the task was to build a probabilistic phrase translation table, since most of the other resources were provided -for more on... |
| ctxr_58c25c30dd82c38881bb | ctx_d5504eb13dd65543782a | W05-0820 | Rules of Engagement | unknown | (Och, 2003) | parenthetical_author_year | Och, 2003 | och | 2003 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | However, the field is moving fast, and a number of steps help to improve upon the provided baseline setup, e.g., larger language models t... |
| ctxr_719cabfc7197fb0ce8d3 | ctx_b472ed175ad023d74995 | W05-0820 | Outlook | unknown | (2005) | year_only | 2005 |  | 2005 | unavailable | unavailable |  | 2 | ambiguous_year_only | ambiguous | False | 0.0 | Koehn, P. (2005) . |
| ctxr_c98bad181139883b5e34 | ctx_8cdcfe38f8dd4878b2dc | W05-0820 | Outlook | unknown | (2003) | year_only | 2003 |  | 2003 | unavailable | unavailable |  | 4 | ambiguous_year_only | ambiguous | False | 0.0 | Koehn, P. and Knight, K. (2003) . |
| ctxr_18e6bd907f52367b1991 | ctx_b5bcb4a3ffe4186ea62d | W05-0820 | Outlook | unknown | (2003) | year_only | 2003 |  | 2003 | unavailable | unavailable |  | 4 | ambiguous_year_only | ambiguous | False | 0.0 | J., and Marcu, D. (2003) . |
| ctxr_f3ae8a0a891423ff54ec | ctx_139de11628481b00ccaa | W05-0820 | Outlook | unknown | (2004) | year_only | 2004 |  | 2004 | unavailable | unavailable |  | 2 | ambiguous_year_only | ambiguous | False | 0.0 | J., Gildea, D., Khudanpur, S., Sarkar, A., Yamada, K., Fraser, A., Kumar, S., Shen, L., Smith, D., Eng, K., Jain, V., Jin, Z., and Radev,... |
| ctxr_37b6fce0d4bd6234685c | ctx_0f2851dcb5d8daace436 | R13-1047 | Abstract | abstract | (2008; 2010) | year_only | 2008 |  | 2008 | unavailable | unavailable |  | 4 | ambiguous_year_only | ambiguous | False | 0.0 | Vecchi et al. (2011) have shown that some compositional models, including the additive and multiplicative models of Mitchell and Lapata (... |
| ctxr_041791b768cf19dee4b0 | ctx_0f2851dcb5d8daace436 | R13-1047 | Abstract | abstract | (2008; 2010) | year_only | 2010 |  | 2010 | unavailable | unavailable |  | 2 | ambiguous_year_only | ambiguous | False | 0.0 | Vecchi et al. (2011) have shown that some compositional models, including the additive and multiplicative models of Mitchell and Lapata (... |
| ctxr_14b17a7492724c3fd587 | ctx_69de474350cb329a1b1a | R13-1047 | Abstract | abstract | (2008; 2010) | year_only | 2008 |  | 2008 | unavailable | unavailable |  | 4 | ambiguous_year_only | ambiguous | False | 0.0 | Vecchi et al. (2011) have shown that some compositional models, including the additive and multiplicative models of Mitchell and Lapata (... |
| ctxr_b5ee4f568023d41fce4c | ctx_69de474350cb329a1b1a | R13-1047 | Abstract | abstract | (2008; 2010) | year_only | 2010 |  | 2010 | unavailable | unavailable |  | 2 | ambiguous_year_only | ambiguous | False | 0.0 | Vecchi et al. (2011) have shown that some compositional models, including the additive and multiplicative models of Mitchell and Lapata (... |
| ctxr_8313e8a1dce505d7e7fb | ctx_bd98001e2d1c8dc87ac8 | R13-1047 | Conclusion | conclusion | (2008) | year_only | 2008 |  | 2008 | unavailable | unavailable |  | 4 | ambiguous_year_only | ambiguous | False | 0.0 | Some other models such as the ones by Erk and Padó (2008) and Thater et al. (2010) which take selectional preferences and context into ac... |
| ctxr_ad87343ade0b9ec6bc51 | ctx_ef9f5360f2dce3eb20ae | W05-0823 | Introduction | introduction | (2002) | year_only | 2002 |  | 2002 | unavailable | unavailable |  | 2 | ambiguous_year_only | ambiguous | False | 0.0 | This translation model was developed by de Gispert and Mariño (2002) , and it differs from the well known phrase-based translation model ... |
| ctxr_c60b07939b3df6e20621 | ctx_215bbeb1571219de92e2 | R13-1049 | Rationale: Representation of Valency-based Predicates | unknown | (2013) | year_only | 2013 |  | 2013 | unavailable | unavailable |  | 2 | ambiguous_year_only | ambiguous | False | 0.0 | Yet Lefrançois (2013) showed that neither of these KR formalisms can represent valency-based predicates, therefore lexicographic definiti... |
| ctxr_b2167b01cb827f01e9fc | ctx_ac8919acb76fb2ee9d36 | R13-1049 | A Deep-Semantic Representation Level | unknown | Gandon (2013b) | narrative_author_year | Gandon (2013b) | gandon | 2013 | b | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | Lefrançois and Gandon (2013b) therefore introduced a deeper level of representation to describe meanings: the deep semantic level, and de... |
| ctxr_da493e241cd1cd8c2bf6 | ctx_5785da21214d960fe1ce | R13-1049 | Reasoning with UGs-Homomorphisms | unknown | Gandon (2013a) | narrative_author_year | Gandon (2013a) | gandon | 2013 | a | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | Lefrançois and Gandon (2013a) proposed to use the notion of UGs homomorphism to define this entailment problem. |
| ctxr_cce3eff94f503802dcaf | ctx_dc77f495fe41279b99b7 | R13-1049 | Reasoning with UGs-Homomorphisms | unknown | Gandon (2013a) | narrative_author_year | Gandon (2013a) | gandon | 2013 | a | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | More generally, Lefrançois and Gandon (2013a) listed a set of rules which defines the axiomatization of the UGs semantics. |
| ctxr_215af6eda62875174cb7 | ctx_f0f039be652926fe0a20 | R13-1049 | Reasoning with UGs-Homomorphisms | unknown | Gandon (2013a) | narrative_author_year | Gandon (2013a) | gandon | 2013 | a | unavailable |  | 2 | multi_candidate_ambiguous | ambiguous | False | 0.0 | Lefrançois and Gandon (2013a) illustrated problematic cases where the closure is infinite for finite UGs. |

## 20 Examples: numeric_unresolved
| context_id | source_context_id | citing_paper_id | raw_section_name | normalized_section | citation_marker | marker_type | marker_component_text | parsed_surnames | parsed_year | parsed_year_suffix | resolved_cited_acl_id | resolved_cited_title | matched_candidate_count | resolution_status | resolution_level | is_strongly_resolved | resolution_confidence | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_0225307ee9f49a7ff613 | ctx_464012bcdae4388248fe | W05-0827 | Introduction | introduction | [1] | numeric | [1] |  | unavailable | unavailable | unavailable |  | 0 | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False | 0.0 | This translation model is known as the sourcechannel approach [1] and it consists on a language model P (e) and a separate translation mo... |
| ctxr_f1244943a889359a4f6e | ctx_cea9984147aa5443cb9a | W05-0827 | Introduction | introduction | [5] | numeric | [5] |  | unavailable | unavailable | unavailable |  | 0 | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False | 0.0 | This translation model is known as the sourcechannel approach [1] and it consists on a language model P (e) and a separate translation mo... |
| ctxr_e9278adb7102901a5b8d | ctx_a46c75cd4c9f80db1a3a | W05-0827 | Introduction | introduction | [8] | numeric | [8] |  | unavailable | unavailable | unavailable |  | 0 | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False | 0.0 | In the last few years, new systems tend to use sequences of words, commonly called phrases [8] , aiming at introducing word context in th... |
| ctxr_5ab0155ad535031ee47e | ctx_46250c629f37191a0ef4 | W05-0827 | Introduction | introduction | [13] | numeric | [13] |  | unavailable | unavailable | unavailable |  | 0 | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False | 0.0 | It is derived from the Maximum Entropy approach suggested by [13] [14] for a natural language understanding task. |
| ctxr_4313f57eb70a6d9e7867 | ctx_cb9b585cb8cb9f3eee41 | W05-0827 | Introduction | introduction | [14] | numeric | [14] |  | unavailable | unavailable | unavailable |  | 0 | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False | 0.0 | It is derived from the Maximum Entropy approach suggested by [13] [14] for a natural language understanding task. |
| ctxr_3afec3dba10d96530775 | ctx_11805e1ed67f1bb6aa0a | W05-0827 | Introduction | introduction | [11] | numeric | [11] |  | unavailable | unavailable | unavailable |  | 0 | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False | 0.0 | This paper addresses a modification of the phrase-extraction algorythm in [11] . |
| ctxr_c085ed5f456617a7cc4f | ctx_de0c96652ea640315f19 | W05-0827 | Baseline | unknown | [17] | numeric | [17] |  | unavailable | unavailable | unavailable |  | 0 | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False | 0.0 | Therefore, the basic idea of phrase-based translation is to segment the given source sentence into phrases, then translate each phrase an... |
| ctxr_bb8a531f7633c69c93bb | ctx_6907627031ab46820c87 | W05-0827 | Baseline | unknown | [6] | numeric | [6] |  | unavailable | unavailable | unavailable |  | 0 | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False | 0.0 | We begin by aligning the training corpus using GIZA++ [6] , which is done in both translation directions. |
| ctxr_126a5fbcc3428c12aa6a | ctx_45b71ac211c6d4b3a2e5 | W05-0827 | Baseline | unknown | [11] | numeric | [11] |  | unavailable | unavailable | unavailable |  | 0 | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False | 0.0 | Next, we define the criterion to extract the set of BP of the sentence pair (f j2 j1 ; e i2 i1 ) and the alignment matrix A ⊆ J * I, whic... |
| ctxr_74a759fc6923efd5210d | ctx_41d055dd29f1c9db2fc1 | W05-0827 | Phrase Extraction | unknown | [8] | numeric | [8] |  | unavailable | unavailable | unavailable |  | 0 | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False | 0.0 | Moreover, the huge increase in computational and storage cost of including longer phrases does not provide a significant improve in quali... |
| ctxr_2bb7cfb4b8a289687904 | ctx_b27f12c33fef506ac7c4 | W05-0827 | Conditional probability P (f \|e) | unknown | [17] | numeric | [17] |  | unavailable | unavailable | unavailable |  | 0 | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False | 0.0 | If a phrase e has N > 1 possible translations, then each one contributes as 1/N [17] . |
| ctxr_d908afb2ac3de1a79a2a | ctx_e1a9401063b36808c05c | W05-0827 | Conditional probability P (f \|e) | unknown | [12] | numeric | [12] |  | unavailable | unavailable | unavailable |  | 0 | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False | 0.0 | In order to somehow compensate these unreiliable probabilities we have studied the inclusion of the posterior [12] and lexical probabilit... |
| ctxr_d52d307a65c625c1d81e | ctx_ce4dd53249066b748b7c | W05-0827 | Conditional probability P (f \|e) | unknown | [1] | numeric | [1] |  | unavailable | unavailable | unavailable |  | 0 | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False | 0.0 | In order to somehow compensate these unreiliable probabilities we have studied the inclusion of the posterior [12] and lexical probabilit... |
| ctxr_aea1250c5fddf6b0de4b | ctx_780fde6e7013e69167b5 | W05-0827 | Conditional probability P (f \|e) | unknown | [10] | numeric | [10] |  | unavailable | unavailable | unavailable |  | 0 | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False | 0.0 | In order to somehow compensate these unreiliable probabilities we have studied the inclusion of the posterior [12] and lexical probabilit... |
| ctxr_150208b7eee35924fc59 | ctx_8fad895867b430907a83 | W05-0827 | Language Model | model | [16] | numeric | [16] |  | unavailable | unavailable | unavailable |  | 0 | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False | 0.0 | As default language model feature, we use a standard word-based trigram language model generated with smoothing Kneser-Ney and interpolat... |
| ctxr_eb6e4efa758cecbd0883 | ctx_91a58cbae6e418e7c957 | W05-0827 | Word and Phrase Penalty | unknown | [7] | numeric | [7] |  | unavailable | unavailable | unavailable |  | 0 | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False | 0.0 | To compensate the preference of the target language model for shorter sentences, we added two [7] . |
| ctxr_eab6df31b1406ac14373 | ctx_c400e8ad529eb85966f7 | W05-0827 | Experiments | experiment | [2] | numeric | [2] |  | unavailable | unavailable | unavailable |  | 0 | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False | 0.0 | The decoder used for the presented translation system is reported in [2] . |
| ctxr_926adca65715c84c2463 | ctx_ad9d46bd18fec377447b | W05-0827 | Experiments | experiment | [15] | numeric | [15] |  | unavailable | unavailable | unavailable |  | 0 | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False | 0.0 | As evaluation criteria we use: the Word Error Rate (WER), the BLEU score [15] and the NIST score [3] . |
| ctxr_37a51f5f840bbaae9b82 | ctx_cac6cf596d2e9157fc8b | W05-0827 | Experiments | experiment | [3] | numeric | [3] |  | unavailable | unavailable | unavailable |  | 0 | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False | 0.0 | As evaluation criteria we use: the Word Error Rate (WER), the BLEU score [15] and the NIST score [3] . |
| ctxr_125b151d0fdc4298a8ab | ctx_9ea1cb24aeda4c91502b | W05-0827 | Experiments | experiment | [9] | numeric | [9] |  | unavailable | unavailable | unavailable |  | 0 | numeric_marker_unresolved_no_bibliography | numeric_unresolved | False | 0.0 | We applied the widely used algorithm SIMPLEX to optimise [9] . |

## 20 Examples: bibliography_unresolved
| context_id | source_context_id | citing_paper_id | raw_section_name | normalized_section | citation_marker | marker_type | marker_component_text | parsed_surnames | parsed_year | parsed_year_suffix | resolved_cited_acl_id | resolved_cited_title | matched_candidate_count | resolution_status | resolution_level | is_strongly_resolved | resolution_confidence | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_26ef99dbe1db8dd54215 | ctx_caa30bbd1d1b6df7a22c | R13-1042 | Introduction | introduction | (Aoki et al., 2003) | parenthetical_author_year | Aoki et al., 2003 | aoki | 2003 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_f90327445945bae94871 | ctx_874e02c7114e7d74abc1 | R13-1042 | Introduction | introduction | (Yeh, 2006; Erera and Carmel, 2008) | parenthetical_author_year | Yeh, 2006 | yeh | 2006 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_bf74e38773678ca7c73c | ctx_874e02c7114e7d74abc1 | R13-1042 | Introduction | introduction | (Yeh, 2006; Erera and Carmel, 2008) | parenthetical_author_year | Erera and Carmel, 2008 | erera;carmel | 2008 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_7c7e126007513aeb74c7 | ctx_3a0085973d5d3f39e130 | R13-1042 | Introduction | introduction | (Yeh, 2006; Erera and Carmel, 2008) | parenthetical_author_year | Yeh, 2006 | yeh | 2006 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_979e78129a9cb7cf04e6 | ctx_3a0085973d5d3f39e130 | R13-1042 | Introduction | introduction | (Yeh, 2006; Erera and Carmel, 2008) | parenthetical_author_year | Erera and Carmel, 2008 | erera;carmel | 2008 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_a92d141fe7c9f1db8405 | ctx_83e770e8729de84c3dda | R13-1042 | Introduction | introduction | Joti et al. (2010) | narrative_author_year | Joti et al. (2010) | joti | 2010 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Joti et al. (2010) used the BC3 corpus of 40 email threads and 3222 emails for topic segmentation. |
| ctxr_30903fb804475456d47c | ctx_b75c50a3489f0ec6113e | R13-1042 | Gold Standard Thread Extraction from the Enron Email Corpus | dataset | Wu and Oard (2005) | narrative_author_year | Wu and Oard (2005) | wu;oard | 2005 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Wu and Oard (2005) , and Zhu et al. (2005) auto-threaded all messages with identical, non-trivial, Fwd: and Re:-stripped Subject headers. |
| ctxr_06483519d5239540f8ad | ctx_3db879d855179f1fd5e7 | R13-1042 | Gold Standard Thread Extraction from the Enron Email Corpus | dataset | Zhu et al. (2005) | narrative_author_year | Zhu et al. (2005) | zhu | 2005 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Wu and Oard (2005) , and Zhu et al. (2005) auto-threaded all messages with identical, non-trivial, Fwd: and Re:-stripped Subject headers. |
| ctxr_2e14793ab64c0c1d527b | ctx_98144c4450bb8b1c0c28 | R13-1042 | Gold Standard Thread Extraction from the Enron Email Corpus | dataset | Klimt and Yang (2004) | narrative_author_year | Klimt and Yang (2004) | klimt;yang | 2004 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Klimt and Yang (2004) auto-threaded messages that had stripped Subject headers and were among the same users (addresses). |
| ctxr_9486cce96e49b81c4732 | ctx_a7ebe2b9e68fc592f67e | R13-1042 | Gold Standard Thread Extraction from the Enron Email Corpus | dataset | Lewis and Knowles (1997) | narrative_author_year | Lewis and Knowles (1997) | lewis;knowles | 1997 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Lewis and Knowles (1997) assigned emails to threads by matching quotation structures between emails. |
| ctxr_f6890f8b41fe4e573895 | ctx_36791895b781e4b296a8 | R13-1042 | Gold Standard Thread Extraction from the Enron Email Corpus | dataset | Klimt and Yang (2004) | narrative_author_year | Klimt and Yang (2004) | klimt;yang | 2004 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | First, we implemented Klimt and Yang (2004) 's technique of clustering the emails into threads that have the same Subject header (after i... |
| ctxr_e00783143d6ac1ac7fe5 | ctx_782bb2eba603a747dbcd | R13-1042 | Gold Standard Thread Extraction from the Enron Email Corpus | dataset | Klimt and Yang (2004) | narrative_author_year | Klimt and Yang (2004) | klimt;yang | 2004 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | In addition, many clusters consisted of all of the issues of a monthly subscription newsletter, or nearly identical petitions (see Klimt ... |
| ctxr_1cd3139fa2d367e9718a | ctx_72b300fea9c097b56058 | R13-1042 | Gold Standard Thread Extraction from the Enron Email Corpus | dataset | Klimt and Yang (2004) | narrative_author_year | Klimt and Yang (2004) | klimt;yang | 2004 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | In order to avoid creating redundant threads, which would be an information leak risk during evaluation, we selected as the thread source... |
| ctxr_8e97d40c51c76600aea0 | ctx_67186a992135f73ff4ea | R13-1042 | Gold Standard Thread Extraction from the Enron Email Corpus | dataset | Yeh (2006) | narrative_author_year | Yeh (2006) | yeh | 2006 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | We used the quoteidentifying regular expressions from Yeh (2006) (see Table 1 ) to identify quoted previous emails. |
| ctxr_81662dd84711ad7b8524 | ctx_09e1fe05d365fd881476 | R13-1042 | Text Similarity Features | unknown | (Gusfield, 1997) | parenthetical_author_year | Gusfield, 1997 | gusfield | 1997 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | The Longest Common Substring measure (Gusfield, 1997) identifies uninterrupted common strings, while the Longest Common Subsequence measu... |
| ctxr_2efa0196a03571fae5ff | ctx_acaf6987af2a31216ca9 | R13-1042 | Text Similarity Features | unknown | (Allison and Dix, 1986) | parenthetical_author_year | Allison and Dix, 1986 | allison;dix | 1986 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | The Longest Common Substring measure (Gusfield, 1997) identifies uninterrupted common strings, while the Longest Common Subsequence measu... |
| ctxr_428cdc0a9745535183fa | ctx_e88e90eaec0ae58b2452 | R13-1042 | Text Similarity Features | unknown | (Wise, 1996) | parenthetical_author_year | Wise, 1996 | wise | 1996 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | The Longest Common Substring measure (Gusfield, 1997) identifies uninterrupted common strings, while the Longest Common Subsequence measu... |
| ctxr_6b947f6fb2a9c48adae0 | ctx_c9f40bf1aa9610b46fb2 | R13-1042 | Text Similarity Features | unknown | Levenshtein (1966) | narrative_author_year | Levenshtein (1966) | levenshtein | 1966 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Other measures which treat texts as sequences of characters and compute similarities with various metrics include Levenshtein (1966) , Mo... |
| ctxr_e8895c5af830b1ebf3ab | ctx_638081887b0da8f57688 | R13-1042 | Text Similarity Features | unknown | (Monge and Elkan, 1997) | parenthetical_author_year | Monge and Elkan, 1997 | monge;elkan | 1997 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Other measures which treat texts as sequences of characters and compute similarities with various metrics include Levenshtein (1966) , Mo... |
| ctxr_a44d451c4a7259943a15 | ctx_4234a53204d4f1e616b9 | R13-1042 | Text Similarity Features | unknown | (Jaro, 1989) | parenthetical_author_year | Jaro, 1989 | jaro | 1989 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Other measures which treat texts as sequences of characters and compute similarities with various metrics include Levenshtein (1966) , Mo... |

## 20 Examples: unresolved markers
| context_id | source_context_id | citing_paper_id | raw_section_name | normalized_section | citation_marker | marker_type | marker_component_text | parsed_surnames | parsed_year | parsed_year_suffix | resolved_cited_acl_id | resolved_cited_title | matched_candidate_count | resolution_status | resolution_level | is_strongly_resolved | resolution_confidence | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_26ef99dbe1db8dd54215 | ctx_caa30bbd1d1b6df7a22c | R13-1042 | Introduction | introduction | (Aoki et al., 2003) | parenthetical_author_year | Aoki et al., 2003 | aoki | 2003 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_f90327445945bae94871 | ctx_874e02c7114e7d74abc1 | R13-1042 | Introduction | introduction | (Yeh, 2006; Erera and Carmel, 2008) | parenthetical_author_year | Yeh, 2006 | yeh | 2006 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_bf74e38773678ca7c73c | ctx_874e02c7114e7d74abc1 | R13-1042 | Introduction | introduction | (Yeh, 2006; Erera and Carmel, 2008) | parenthetical_author_year | Erera and Carmel, 2008 | erera;carmel | 2008 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_7c7e126007513aeb74c7 | ctx_3a0085973d5d3f39e130 | R13-1042 | Introduction | introduction | (Yeh, 2006; Erera and Carmel, 2008) | parenthetical_author_year | Yeh, 2006 | yeh | 2006 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_979e78129a9cb7cf04e6 | ctx_3a0085973d5d3f39e130 | R13-1042 | Introduction | introduction | (Yeh, 2006; Erera and Carmel, 2008) | parenthetical_author_year | Erera and Carmel, 2008 | erera;carmel | 2008 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_a92d141fe7c9f1db8405 | ctx_83e770e8729de84c3dda | R13-1042 | Introduction | introduction | Joti et al. (2010) | narrative_author_year | Joti et al. (2010) | joti | 2010 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Joti et al. (2010) used the BC3 corpus of 40 email threads and 3222 emails for topic segmentation. |
| ctxr_30903fb804475456d47c | ctx_b75c50a3489f0ec6113e | R13-1042 | Gold Standard Thread Extraction from the Enron Email Corpus | dataset | Wu and Oard (2005) | narrative_author_year | Wu and Oard (2005) | wu;oard | 2005 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Wu and Oard (2005) , and Zhu et al. (2005) auto-threaded all messages with identical, non-trivial, Fwd: and Re:-stripped Subject headers. |
| ctxr_06483519d5239540f8ad | ctx_3db879d855179f1fd5e7 | R13-1042 | Gold Standard Thread Extraction from the Enron Email Corpus | dataset | Zhu et al. (2005) | narrative_author_year | Zhu et al. (2005) | zhu | 2005 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Wu and Oard (2005) , and Zhu et al. (2005) auto-threaded all messages with identical, non-trivial, Fwd: and Re:-stripped Subject headers. |
| ctxr_2e14793ab64c0c1d527b | ctx_98144c4450bb8b1c0c28 | R13-1042 | Gold Standard Thread Extraction from the Enron Email Corpus | dataset | Klimt and Yang (2004) | narrative_author_year | Klimt and Yang (2004) | klimt;yang | 2004 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Klimt and Yang (2004) auto-threaded messages that had stripped Subject headers and were among the same users (addresses). |
| ctxr_9486cce96e49b81c4732 | ctx_a7ebe2b9e68fc592f67e | R13-1042 | Gold Standard Thread Extraction from the Enron Email Corpus | dataset | Lewis and Knowles (1997) | narrative_author_year | Lewis and Knowles (1997) | lewis;knowles | 1997 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Lewis and Knowles (1997) assigned emails to threads by matching quotation structures between emails. |
| ctxr_f6890f8b41fe4e573895 | ctx_36791895b781e4b296a8 | R13-1042 | Gold Standard Thread Extraction from the Enron Email Corpus | dataset | Klimt and Yang (2004) | narrative_author_year | Klimt and Yang (2004) | klimt;yang | 2004 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | First, we implemented Klimt and Yang (2004) 's technique of clustering the emails into threads that have the same Subject header (after i... |
| ctxr_e00783143d6ac1ac7fe5 | ctx_782bb2eba603a747dbcd | R13-1042 | Gold Standard Thread Extraction from the Enron Email Corpus | dataset | Klimt and Yang (2004) | narrative_author_year | Klimt and Yang (2004) | klimt;yang | 2004 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | In addition, many clusters consisted of all of the issues of a monthly subscription newsletter, or nearly identical petitions (see Klimt ... |
| ctxr_1cd3139fa2d367e9718a | ctx_72b300fea9c097b56058 | R13-1042 | Gold Standard Thread Extraction from the Enron Email Corpus | dataset | Klimt and Yang (2004) | narrative_author_year | Klimt and Yang (2004) | klimt;yang | 2004 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | In order to avoid creating redundant threads, which would be an information leak risk during evaluation, we selected as the thread source... |
| ctxr_8e97d40c51c76600aea0 | ctx_67186a992135f73ff4ea | R13-1042 | Gold Standard Thread Extraction from the Enron Email Corpus | dataset | Yeh (2006) | narrative_author_year | Yeh (2006) | yeh | 2006 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | We used the quoteidentifying regular expressions from Yeh (2006) (see Table 1 ) to identify quoted previous emails. |
| ctxr_77b5217607ceb30638bb | ctx_42406514152d2d31a609 | R13-1042 | Text Similarity Features | unknown | (2011) | year_only | 2011 |  | 2011 | unavailable | unavailable |  | 2 | ambiguous_year_only | ambiguous | False | 0.0 | We evaluate a number of text similarity measures, divided according to Bär et al. (2011) 's three groups: Content Similarity, Structural ... |
| ctxr_81662dd84711ad7b8524 | ctx_09e1fe05d365fd881476 | R13-1042 | Text Similarity Features | unknown | (Gusfield, 1997) | parenthetical_author_year | Gusfield, 1997 | gusfield | 1997 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | The Longest Common Substring measure (Gusfield, 1997) identifies uninterrupted common strings, while the Longest Common Subsequence measu... |
| ctxr_2efa0196a03571fae5ff | ctx_acaf6987af2a31216ca9 | R13-1042 | Text Similarity Features | unknown | (Allison and Dix, 1986) | parenthetical_author_year | Allison and Dix, 1986 | allison;dix | 1986 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | The Longest Common Substring measure (Gusfield, 1997) identifies uninterrupted common strings, while the Longest Common Subsequence measu... |
| ctxr_428cdc0a9745535183fa | ctx_e88e90eaec0ae58b2452 | R13-1042 | Text Similarity Features | unknown | (Wise, 1996) | parenthetical_author_year | Wise, 1996 | wise | 1996 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | The Longest Common Substring measure (Gusfield, 1997) identifies uninterrupted common strings, while the Longest Common Subsequence measu... |
| ctxr_6b947f6fb2a9c48adae0 | ctx_c9f40bf1aa9610b46fb2 | R13-1042 | Text Similarity Features | unknown | Levenshtein (1966) | narrative_author_year | Levenshtein (1966) | levenshtein | 1966 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Other measures which treat texts as sequences of characters and compute similarities with various metrics include Levenshtein (1966) , Mo... |
| ctxr_e8895c5af830b1ebf3ab | ctx_638081887b0da8f57688 | R13-1042 | Text Similarity Features | unknown | (Monge and Elkan, 1997) | parenthetical_author_year | Monge and Elkan, 1997 | monge;elkan | 1997 | unavailable | unavailable |  | 0 | bibliography_unresolved | unresolved | False | 0.0 | Other measures which treat texts as sequences of characters and compute similarities with various metrics include Levenshtein (1966) , Mo... |

## Common Failure Patterns
| resolution_status | resolution_method | rows |
| --- | --- | --- |
| bibliography_unresolved | author_year_no_candidate | 1533898 |
| citing_paper_not_in_aligned_graph | no_candidate_graph_for_citing_paper | 225675 |
| numeric_marker_unresolved_no_bibliography | numeric_marker | 85782 |
| multi_candidate_ambiguous | author_year_multiple_candidates | 54689 |
| ambiguous_year_only | year_only_multiple_candidates | 16783 |
| author_year_weak_nonfirst_author | author_year_nonfirst_author_candidate_graph | 15936 |
| bibliography_unresolved | year_only_no_candidate | 14264 |
| year_only_unique_candidate | year_only_unique_candidate | 8931 |
| bibliography_unresolved | marker_parse_failed | 6640 |
| multi_candidate_ambiguous | author_year_multiple_weak_nonfirst_candidates | 1156 |
| author_year_clear | author_year_candidate_graph | 12 |
