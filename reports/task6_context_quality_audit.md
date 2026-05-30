# Task 6.1 Citation Context Quality Audit

## Inputs
- Contexts: `data/processed/citation_contexts.parquet`
- Sections: `data/interim/acl_sections.parquet` (67414 rows)
- References: `data/interim/acl_references.parquet` (5151670 rows)
- Flags: `data/processed/task6_context_quality_flags.parquet`
- Configured max context window length: 2000

## Core Counts
| metric | value |
| --- | --- |
| contexts | 2112564 |
| unique_context_id | 2112346 |
| duplicate_context_id_count | 218 |

## Null / Empty Rates
| column | null_or_empty | rate |
| --- | --- | --- |
| context_id | 0 | 0.000 |
| citing_paper_id | 0 | 0.000 |
| reference_key | 0 | 0.000 |
| cited_title | 2112564 | 1.000 |
| cited_year | 2112564 | 1.000 |
| cited_doi | 2112564 | 1.000 |
| section | 2112564 | 1.000 |
| paragraph_id | 0 | 0.000 |
| citation_marker | 0 | 0.000 |
| sentence_text | 0 | 0.000 |
| context_window_s3 | 0 | 0.000 |
| context_window_paragraph | 0 | 0.000 |
| citation_group_size | 0 | 0.000 |
| attribution_status | 0 | 0.000 |

## Attribution Status Distribution
| attribution_status | contexts |
| --- | --- |
| bibliography_unresolved | 1452512 |
| multi_citation_group | 653692 |
| citation_range | 6360 |

## Section Distribution
| section | contexts |
| --- | --- |
| unavailable | 2112564 |

## Citation Group Size Distribution
| citation_group_size | contexts |
| --- | --- |
| 1 | 1452550 |
| 2 | 296456 |
| 3 | 164727 |
| 4 | 85680 |
| 5 | 46480 |
| 6 | 25536 |
| 7 | 15106 |
| 8 | 9560 |
| 10 | 5660 |
| 9 | 5211 |
| 11 | 1980 |
| 12 | 780 |
| 101 | 606 |
| 100 | 400 |
| 14 | 168 |
| 17 | 153 |
| 13 | 130 |
| 41 | 123 |
| 20 | 120 |
| 16 | 112 |
| 25 | 100 |
| 15 | 90 |
| 44 | 88 |
| 75 | 75 |
| 37 | 74 |
| 73 | 73 |
| 29 | 58 |
| 58 | 58 |
| 51 | 51 |
| 50 | 50 |
| 46 | 46 |
| 43 | 43 |
| 40 | 40 |
| 18 | 36 |
| 33 | 33 |
| 32 | 32 |
| 31 | 31 |
| 26 | 26 |
| 22 | 22 |

## Grounding Checks
| check | passed | total | rate |
| --- | --- | --- | --- |
| sentence_text appears inside context_window_s3 | 2110258 | 2112564 | 0.999 |
| sentence_text appears inside context_window_paragraph | 2107441 | 2112564 | 0.998 |
| citation_marker appears inside sentence_text | 2112564 | 2112564 | 1.000 |

## Suspicious Rows
| flag | rows | rate |
| --- | --- | --- |
| flag_single_clear_group_size_gt_1 | 0 | 0.000 |
| flag_empty_context_window_s3 | 0 | 0.000 |
| flag_empty_sentence_text | 0 | 0.000 |
| flag_empty_reference_key | 0 | 0.000 |
| flag_unresolved_with_cited_title | 0 | 0.000 |
| flag_context_window_s3_too_long | 0 | 0.000 |
| flag_any | 0 | 0.000 |

## Sample 20 Rows
| context_id | citing_paper_id | reference_key | section | paragraph_id | citation_marker | attribution_status | sentence_text | context_window_s3 | context_window_paragraph |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctx_49cf24ac775d09eb1025 | R13-1042 | unresolved_7d12ba56e9f8 | unavailable | R13-1042_p0 | (2010) | bibliography_unresolved | In NLP, Elsner and Charniak (2010) described the task of thread disentanglement as "the clustering task of dividing a transcript into a set of distinct conversations," in which extrinsic thread delimitation is unavail... | We also found that contentbased features continue to outperform the others in both a class-balanced and class-imbalanced setting, as well as with semantically controlled or non-controlled negative instances. In NLP, E... | ple email accounts for one person; sharing one email account among multiple persons; changing the Subject header; and removing quoted material from earlier in the thread. How can emails be organized by thread without ... |
| ctx_1b8dbeb14bcb86f7e95b | R13-1042 | unresolved_f04e10ac0205 | unavailable | R13-1042_p0 | (Elsner and Charniak, 2010) | bibliography_unresolved | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki et al., 2003) , and emails with headers and quoted material (Yeh, 2006; Erera a... | In addition to emails with missing or incorrect MIME headers, entangled electronic conversations occur in environments such as interspersed Internet Relay Chat conversations, web 2.0 article response conversations tha... | adding these latter feature groups does not significantly improve total performance. We also found that contentbased features continue to outperform the others in both a class-balanced and class-imbalanced setting, as... |
| ctx_7098ddac36c149ad6c4f | R13-1042 | unresolved_b0ba75106da6 | unavailable | R13-1042_p0 | (Aoki et al., 2003) | bibliography_unresolved | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki et al., 2003) , and emails with headers and quoted material (Yeh, 2006; Erera a... | In addition to emails with missing or incorrect MIME headers, entangled electronic conversations occur in environments such as interspersed Internet Relay Chat conversations, web 2.0 article response conversations tha... | es not significantly improve total performance. We also found that contentbased features continue to outperform the others in both a class-balanced and class-imbalanced setting, as well as with semantically controlled... |
| ctx_d92aaae0a320f5b57d2b | R13-1042 | unresolved_8d72fccd9b83 | unavailable | R13-1042_p0 | (Yeh, 2006; Erera and Carmel, 2008) | multi_citation_group | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki et al., 2003) , and emails with headers and quoted material (Yeh, 2006; Erera a... | In addition to emails with missing or incorrect MIME headers, entangled electronic conversations occur in environments such as interspersed Internet Relay Chat conversations, web 2.0 article response conversations tha... | based features continue to outperform the others in both a class-balanced and class-imbalanced setting, as well as with semantically controlled or non-controlled negative instances. In NLP, Elsner and Charniak (2010) ... |
| ctx_1644879268ac4613e866 | R13-1042 | unresolved_50512fbb0b7d | unavailable | R13-1042_p0 | (Yeh, 2006; Erera and Carmel, 2008) | multi_citation_group | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki et al., 2003) , and emails with headers and quoted material (Yeh, 2006; Erera a... | In addition to emails with missing or incorrect MIME headers, entangled electronic conversations occur in environments such as interspersed Internet Relay Chat conversations, web 2.0 article response conversations tha... | based features continue to outperform the others in both a class-balanced and class-imbalanced setting, as well as with semantically controlled or non-controlled negative instances. In NLP, Elsner and Charniak (2010) ... |
| ctx_d76dde89813c8f48ed46 | R13-1042 | unresolved_7d12ba56e9f8 | unavailable | R13-1042_p0 | (2010) | bibliography_unresolved | Joti et al. (2010) used the BC3 corpus of 40 email threads and 3222 emails for topic segmentation. | Previous researchers have used a number of email corpora with high-precision (non-Subject-clustered) thread marking. Joti et al. (2010) used the BC3 corpus of 40 email threads and 3222 emails for topic segmentation. C... | script into a set of distinct conversations," in which extrinsic thread delimitation is unavailable and the threads must be disentangled using only intrinsic information. In addition to emails with missing or incorrec... |
| ctx_0257043554992fa70a0d | R13-1042 | unresolved_e5e53c784d5d | unavailable | R13-1042_p0 | (2008) | bibliography_unresolved | Carenini et al. (2008) annotated 39 email "conversations" from the Enron Email Corpus for email summariation. | Joti et al. (2010) used the BC3 corpus of 40 email threads and 3222 emails for topic segmentation. Carenini et al. (2008) annotated 39 email "conversations" from the Enron Email Corpus for email summariation. Wan and ... | the threads must be disentangled using only intrinsic information. In addition to emails with missing or incorrect MIME headers, entangled electronic conversations occur in environments such as interspersed Internet R... |
| ctx_c00c937fc4e5efc32b5b | R13-1042 | unresolved_483029d52621 | unavailable | R13-1042_p0 | (2004) | bibliography_unresolved | Wan and McKeown (2004) used a privatelyavailable corpus of 300 threads for summary generation. | Carenini et al. (2008) annotated 39 email "conversations" from the Enron Email Corpus for email summariation. Wan and McKeown (2004) used a privatelyavailable corpus of 300 threads for summary generation. Rambow et al... | rrect MIME headers, entangled electronic conversations occur in environments such as interspersed Internet Relay Chat conversations, web 2.0 article response conversations that do not have a hierarchical display order... |
| ctx_6cff1d6fcaede47b691f | R13-1042 | unresolved_483029d52621 | unavailable | R13-1042_p0 | (2004) | bibliography_unresolved | Rambow et al. (2004) used a privatelyavailable corpus of 96 email threads for thread summarization. | Wan and McKeown (2004) used a privatelyavailable corpus of 300 threads for summary generation. Rambow et al. (2004) used a privatelyavailable corpus of 96 email threads for thread summarization. Data The Enron Email C... | rsed Internet Relay Chat conversations, web 2.0 article response conversations that do not have a hierarchical display order, and misplaced comments in Wiki Talk discussions. Research on disentanglement of conversatio... |
| ctx_28b3c707e054f0d54e0f | R13-1042 | unresolved_a20a2b7bb084 | unavailable | R13-1042_p0 | (2005) | bibliography_unresolved | Wu and Oard (2005) , and Zhu et al. (2005) auto-threaded all messages with identical, non-trivial, Fwd: and Re:-stripped Subject headers. | Previous researchers have derived email thread structure from a variety of sources. Wu and Oard (2005) , and Zhu et al. (2005) auto-threaded all messages with identical, non-trivial, Fwd: and Re:-stripped Subject head... | 39 email "conversations" from the Enron Email Corpus for email summariation. Wan and McKeown (2004) used a privatelyavailable corpus of 300 threads for summary generation. Rambow et al. (2004) used a privatelyavailabl... |
| ctx_922fddecc7dd1ca7ca20 | R13-1042 | unresolved_a20a2b7bb084 | unavailable | R13-1042_p0 | (2005) | bibliography_unresolved | Wu and Oard (2005) , and Zhu et al. (2005) auto-threaded all messages with identical, non-trivial, Fwd: and Re:-stripped Subject headers. | Previous researchers have derived email thread structure from a variety of sources. Wu and Oard (2005) , and Zhu et al. (2005) auto-threaded all messages with identical, non-trivial, Fwd: and Re:-stripped Subject head... | " from the Enron Email Corpus for email summariation. Wan and McKeown (2004) used a privatelyavailable corpus of 300 threads for summary generation. Rambow et al. (2004) used a privatelyavailable corpus of 96 email th... |
| ctx_12de59cea39d76e21607 | R13-1042 | unresolved_483029d52621 | unavailable | R13-1042_p0 | (2004) | bibliography_unresolved | Klimt and Yang (2004) auto-threaded messages that had stripped Subject headers and were among the same users (addresses). | Wu and Oard (2005) , and Zhu et al. (2005) auto-threaded all messages with identical, non-trivial, Fwd: and Re:-stripped Subject headers. Klimt and Yang (2004) auto-threaded messages that had stripped Subject headers ... | threads for summary generation. Rambow et al. (2004) used a privatelyavailable corpus of 96 email threads for thread summarization. Data The Enron Email Corpus (EEC) 1 consists of the 517,424 emails (159 users' accoun... |
| ctx_45df5f192a5ae3798599 | R13-1042 | unresolved_0985b889a1fe | unavailable | R13-1042_p0 | (1997) | bibliography_unresolved | Lewis and Knowles (1997) assigned emails to threads by matching quotation structures between emails. | Klimt and Yang (2004) auto-threaded messages that had stripped Subject headers and were among the same users (addresses). Lewis and Knowles (1997) assigned emails to threads by matching quotation structures between em... | ation. Data The Enron Email Corpus (EEC) 1 consists of the 517,424 emails (159 users' accounts and 19,675 total senders) that existed on the Enron Corporation's email server (i.e., other emails had been previously del... |
| ctx_7dff41f01b98fa4473e2 | R13-1042 | unresolved_483029d52621 | unavailable | R13-1042_p0 | (2004) | bibliography_unresolved | Wan and McKeown (2004) reconstructed threads by header Message-ID information. | Lewis and Knowles (1997) assigned emails to threads by matching quotation structures between emails. Wan and McKeown (2004) reconstructed threads by header Message-ID information. Rambow et al. (2004) used a privately... | 19,675 total senders) that existed on the Enron Corporation's email server (i.e., other emails had been previously deleted, etc) when it was made public . Gold Standard Thread Extraction from the Enron Email Corpus We... |
| ctx_c6958263c9adf95a7660 | R13-1042 | unresolved_483029d52621 | unavailable | R13-1042_p0 | (2004) | bibliography_unresolved | Rambow et al. (2004) used a privately-available corpus of 96 email threads, but did not specify how they determined the threads. | Wan and McKeown (2004) reconstructed threads by header Message-ID information. Rambow et al. (2004) used a privately-available corpus of 96 email threads, but did not specify how they determined the threads. As the em... | .e., other emails had been previously deleted, etc) when it was made public . Gold Standard Thread Extraction from the Enron Email Corpus We define an email thread as a directed graph of emails connected by Reply and ... |
| ctx_7775eec7f7b3b27cb67f | R13-1042 | unresolved_483029d52621 | unavailable | R13-1042_p0 | (2004) | bibliography_unresolved | First, we implemented Klimt and Yang (2004) 's technique of clustering the emails into threads that have the same Subject header (after it has been stripped of pre-fixes such as Re: and Fwd:) and shared participants. | As the emails in the EEC do not contain any inherent thread structure, it was necessary for us to create email threads. First, we implemented Klimt and Yang (2004) 's technique of clustering the emails into threads th... | email discussions between users. However, the precise definition of an email thread actually depends on the implementation that we, or any other researchers, used to identify the thread. Previous researchers have deri... |
| ctx_e1d8a6a3a2df9db0c256 | R13-1042 | unresolved_483029d52621 | unavailable | R13-1042_p0 | (2004) | bibliography_unresolved | In addition, many clusters consisted of all of the issues of a monthly subscription newsletter, or nearly identical petitions (see Klimt and Yang (2004) 's description of the "Demand Ken Lay Donate Proceeds from Enron... | Clusters tended to over-group, because a single user included as a recipient for two different threads with the Subject "Monday Meeting" would cause the threads to be merged into a single cluster. In addition, many cl... | w they determined the threads. As the emails in the EEC do not contain any inherent thread structure, it was necessary for us to create email threads. First, we implemented Klimt and Yang (2004) 's technique of cluste... |
| ctx_ad3875e1f850cc709f7d | R13-1042 | unresolved_483029d52621 | unavailable | R13-1042_p0 | (2004) | bibliography_unresolved | In order to avoid creating redundant threads, which would be an information leak risk during evaluation, we selected as the thread source the email from each Klimt and Yang (2004) cluster with the most quoted emails, ... | Threads in the EEC are quoted multiple times at various points in the conversation in multiple surviving emails. In order to avoid creating redundant threads, which would be an information leak risk during evaluation,... | tter, or nearly identical petitions (see Klimt and Yang (2004) 's description of the "Demand Ken Lay Donate Proceeds from Enron Stock Sales" thread), or an auto-generated log of Enron computer network problems auto-em... |
| ctx_2c880ccdcfe1a936c590 | R13-1042 | unresolved_6f6a4e56098c | unavailable | R13-1042_p0 | (2006) | bibliography_unresolved | We used the quoteidentifying regular expressions from Yeh (2006) (see Table 1 ) to identify quoted previous emails. | In order to avoid creating redundant threads, which would be an information leak risk during evaluation, we selected as the thread source the email from each Klimt and Yang (2004) cluster with the most quoted emails, ... | or an auto-generated log of Enron computer network problems auto-emailed to the Enron employees in charge of the network. Such clusters of "broadcast" emails do not satisfy our goal of identifying email discussions be... |
| ctx_aca4a6d15999787c7341 | R13-1042 | unresolved_72d1b5da6eea | unavailable | R13-1042_p0 | (2011) | bibliography_unresolved | We evaluate a number of text similarity measures, divided according to Bär et al. (2011) 's three groups: Content Similarity, Structural Similarity, Style Similarity. | Ideally, there exists a text similarity measure that marks pairs of emails from the system misidentified about 1% of emails from regular expression error. same thread as more similar than pairs of emails from differen... | ted by this reduced recall, because each experimental instance includes only a pair of emails, and not the entire thread. Second, because the thread source did not require human annotation, using quoted emails gives u... |
