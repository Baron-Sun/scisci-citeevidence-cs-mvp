# Citation Contexts Sectioned Extraction Report

## Inputs / Outputs
| name | path |
| --- | --- |
| sections | data/interim/acl_sections_sectioned_normalized.parquet |
| citation_contexts_sectioned | data/processed/citation_contexts_sectioned.parquet |

- Max context window chars: 2000
- Extraction mode: pre-resolution / no bibliography

## Core Metrics
| metric | value |
| --- | --- |
| context rows | 1990689 |
| unique context_id | 1990689 |
| duplicate context_id | 0 |
| sentence_text in context_window_s3 rate | 1.000 |
| sentence_text in context_window_paragraph rate | 1.000 |
| citation_marker in sentence_text rate | 1.000 |

## Marker Type Distribution
| marker_type | rows |
| --- | --- |
| parenthetical_author_year | 1489814 |
| narrative_author_year | 384795 |
| numeric | 85782 |
| year_only | 30298 |

## Attribution Status Distribution
| attribution_status | rows |
| --- | --- |
| author_year_unresolved_pre_resolution | 1367218 |
| multi_citation_group | 569388 |
| numeric_unresolved_pre_resolution | 50040 |
| citation_range | 4043 |

## Normalized Section Distribution
| section | rows |
| --- | --- |
| unknown | 664506 |
| introduction | 443426 |
| related_work | 325560 |
| dataset | 111456 |
| model | 82565 |
| experiment | 75639 |
| method | 61561 |
| evaluation | 47236 |
| conclusion | 32228 |
| results | 31744 |
| background | 31134 |
| discussion | 23236 |
| analysis | 16621 |
| abstract | 11234 |
| implementation | 9741 |
| system_description | 5466 |
| references | 4845 |
| task_definition | 4174 |
| appendix | 3438 |
| acknowledgement | 3004 |
| error_analysis | 1875 |

## Citation Group Size Distribution
| citation_group_size | rows |
| --- | --- |
| 1 | 1417287 |
| 2 | 270478 |
| 3 | 143403 |
| 4 | 72136 |
| 5 | 37415 |
| 6 | 20034 |
| 7 | 11585 |
| 8 | 6968 |
| 10 | 3730 |
| 9 | 3708 |
| 11 | 1441 |
| 12 | 504 |
| 101 | 404 |
| 100 | 200 |
| 14 | 140 |
| 20 | 120 |
| 17 | 102 |
| 16 | 96 |
| 13 | 91 |
| 15 | 90 |
| 29 | 87 |
| 41 | 82 |
| 78 | 78 |
| 25 | 75 |
| 73 | 73 |
| 33 | 66 |
| 58 | 58 |
| 26 | 52 |
| 50 | 50 |
| 46 | 46 |
| 18 | 36 |
| 32 | 32 |
| 22 | 22 |

## Sample Rows
| context_id | citing_paper_id | section | paragraph_id | citation_marker | marker_type | attribution_status | citation_group_size | sentence_text | context_window_s3 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctx_4c265fc01e3bc9f11872 | R13-1042 | introduction | R13-1042_s0001_p0003 | Elsner and Charniak (2010) | narrative_author_year | author_year_unresolved_pre_resolution | 1 | In NLP, Elsner and Charniak (2010) described the task of thread disentanglement as "the clustering task of dividing a transcript into a set of distinct conve... | In NLP, Elsner and Charniak (2010) described the task of thread disentanglement as "the clustering task of dividing a transcript into a set of distinct conve... |
| ctx_e7f13d44394b4c7c137f | R13-1042 | introduction | R13-1042_s0001_p0004 | (Elsner and Charniak, 2010) | parenthetical_author_year | author_year_unresolved_pre_resolution | 1 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki et al., 2003) , and... | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki et al., 2003) , and... |
| ctx_caa30bbd1d1b6df7a22c | R13-1042 | introduction | R13-1042_s0001_p0004 | (Aoki et al., 2003) | parenthetical_author_year | author_year_unresolved_pre_resolution | 1 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki et al., 2003) , and... | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki et al., 2003) , and... |
| ctx_874e02c7114e7d74abc1 | R13-1042 | introduction | R13-1042_s0001_p0004 | (Yeh, 2006; Erera and Carmel, 2008) | parenthetical_author_year | multi_citation_group | 2 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki et al., 2003) , and... | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki et al., 2003) , and... |
| ctx_3a0085973d5d3f39e130 | R13-1042 | introduction | R13-1042_s0001_p0004 | (Yeh, 2006; Erera and Carmel, 2008) | parenthetical_author_year | multi_citation_group | 2 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki et al., 2003) , and... | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki et al., 2003) , and... |
| ctx_83e770e8729de84c3dda | R13-1042 | introduction | R13-1042_s0001_p0005 | Joti et al. (2010) | narrative_author_year | author_year_unresolved_pre_resolution | 1 | Joti et al. (2010) used the BC3 corpus of 40 email threads and 3222 emails for topic segmentation. | Previous researchers have used a number of email corpora with high-precision (non-Subject-clustered) thread marking. Joti et al. (2010) used the BC3 corpus o... |
| ctx_0f0eb448b401dd51cdf3 | R13-1042 | introduction | R13-1042_s0001_p0005 | Carenini et al. (2008) | narrative_author_year | author_year_unresolved_pre_resolution | 1 | Carenini et al. (2008) annotated 39 email "conversations" from the Enron Email Corpus for email summariation. | Joti et al. (2010) used the BC3 corpus of 40 email threads and 3222 emails for topic segmentation. Carenini et al. (2008) annotated 39 email "conversations" ... |
| ctx_5316b90745ae591db502 | R13-1042 | introduction | R13-1042_s0001_p0005 | Wan and McKeown (2004) | narrative_author_year | author_year_unresolved_pre_resolution | 1 | Wan and McKeown (2004) used a privatelyavailable corpus of 300 threads for summary generation. | Carenini et al. (2008) annotated 39 email "conversations" from the Enron Email Corpus for email summariation. Wan and McKeown (2004) used a privatelyavailabl... |
| ctx_c272b15a642e8261f522 | R13-1042 | introduction | R13-1042_s0001_p0005 | Rambow et al. (2004) | narrative_author_year | author_year_unresolved_pre_resolution | 1 | Rambow et al. (2004) used a privatelyavailable corpus of 96 email threads for thread summarization. | Wan and McKeown (2004) used a privatelyavailable corpus of 300 threads for summary generation. Rambow et al. (2004) used a privatelyavailable corpus of 96 em... |
| ctx_b75c50a3489f0ec6113e | R13-1042 | dataset | R13-1042_s0003_p0000 | Wu and Oard (2005) | narrative_author_year | author_year_unresolved_pre_resolution | 1 | Wu and Oard (2005) , and Zhu et al. (2005) auto-threaded all messages with identical, non-trivial, Fwd: and Re:-stripped Subject headers. | Previous researchers have derived email thread structure from a variety of sources. Wu and Oard (2005) , and Zhu et al. (2005) auto-threaded all messages wit... |
| ctx_3db879d855179f1fd5e7 | R13-1042 | dataset | R13-1042_s0003_p0000 | Zhu et al. (2005) | narrative_author_year | author_year_unresolved_pre_resolution | 1 | Wu and Oard (2005) , and Zhu et al. (2005) auto-threaded all messages with identical, non-trivial, Fwd: and Re:-stripped Subject headers. | Previous researchers have derived email thread structure from a variety of sources. Wu and Oard (2005) , and Zhu et al. (2005) auto-threaded all messages wit... |
| ctx_98144c4450bb8b1c0c28 | R13-1042 | dataset | R13-1042_s0003_p0000 | Klimt and Yang (2004) | narrative_author_year | author_year_unresolved_pre_resolution | 1 | Klimt and Yang (2004) auto-threaded messages that had stripped Subject headers and were among the same users (addresses). | Wu and Oard (2005) , and Zhu et al. (2005) auto-threaded all messages with identical, non-trivial, Fwd: and Re:-stripped Subject headers. Klimt and Yang (200... |
| ctx_a7ebe2b9e68fc592f67e | R13-1042 | dataset | R13-1042_s0003_p0000 | Lewis and Knowles (1997) | narrative_author_year | author_year_unresolved_pre_resolution | 1 | Lewis and Knowles (1997) assigned emails to threads by matching quotation structures between emails. | Klimt and Yang (2004) auto-threaded messages that had stripped Subject headers and were among the same users (addresses). Lewis and Knowles (1997) assigned e... |
| ctx_749b7cb80bcc70164ca3 | R13-1042 | dataset | R13-1042_s0003_p0000 | Wan and McKeown (2004) | narrative_author_year | author_year_unresolved_pre_resolution | 1 | Wan and McKeown (2004) reconstructed threads by header Message-ID information. | Lewis and Knowles (1997) assigned emails to threads by matching quotation structures between emails. Wan and McKeown (2004) reconstructed threads by header M... |
| ctx_82c232f3d1dfc98f4dff | R13-1042 | dataset | R13-1042_s0003_p0000 | Rambow et al. (2004) | narrative_author_year | author_year_unresolved_pre_resolution | 1 | Rambow et al. (2004) used a privately-available corpus of 96 email threads, but did not specify how they determined the threads. | Wan and McKeown (2004) reconstructed threads by header Message-ID information. Rambow et al. (2004) used a privately-available corpus of 96 email threads, bu... |
| ctx_36791895b781e4b296a8 | R13-1042 | dataset | R13-1042_s0003_p0001 | Klimt and Yang (2004) | narrative_author_year | author_year_unresolved_pre_resolution | 1 | First, we implemented Klimt and Yang (2004) 's technique of clustering the emails into threads that have the same Subject header (after it has been stripped ... | As the emails in the EEC do not contain any inherent thread structure, it was necessary for us to create email threads. First, we implemented Klimt and Yang ... |
| ctx_782bb2eba603a747dbcd | R13-1042 | dataset | R13-1042_s0003_p0002 | Klimt and Yang (2004) | narrative_author_year | author_year_unresolved_pre_resolution | 1 | In addition, many clusters consisted of all of the issues of a monthly subscription newsletter, or nearly identical petitions (see Klimt and Yang (2004) 's d... | Clusters tended to over-group, because a single user included as a recipient for two different threads with the Subject "Monday Meeting" would cause the thre... |
| ctx_72b300fea9c097b56058 | R13-1042 | dataset | R13-1042_s0003_p0003 | Klimt and Yang (2004) | narrative_author_year | author_year_unresolved_pre_resolution | 1 | In order to avoid creating redundant threads, which would be an information leak risk during evaluation, we selected as the thread source the email from each... | Threads in the EEC are quoted multiple times at various points in the conversation in multiple surviving emails. In order to avoid creating redundant threads... |
| ctx_67186a992135f73ff4ea | R13-1042 | dataset | R13-1042_s0003_p0003 | Yeh (2006) | narrative_author_year | author_year_unresolved_pre_resolution | 1 | We used the quoteidentifying regular expressions from Yeh (2006) (see Table 1 ) to identify quoted previous emails. | In order to avoid creating redundant threads, which would be an information leak risk during evaluation, we selected as the thread source the email from each... |
| ctx_42406514152d2d31a609 | R13-1042 | unknown | R13-1042_s0004_p0000 | (2011) | year_only | author_year_unresolved_pre_resolution | 1 | We evaluate a number of text similarity measures, divided according to Bär et al. (2011) 's three groups: Content Similarity, Structural Similarity, Style Si... | Ideally, there exists a text similarity measure that marks pairs of emails from the system misidentified about 1% of emails from regular expression error. sa... |
