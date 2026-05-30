# Citation Marker Resolution Pilot Report

## Inputs
| name | path |
| --- | --- |
| citation_contexts | data/processed/citation_contexts_sectioned.parquet |
| acl_citation_graph_aligned | data/interim/acl_citation_graph_aligned.parquet |
| acl_id_crosswalk | data/interim/acl_id_crosswalk.parquet |

## Outputs
| name | path |
| --- | --- |
| citation_contexts_resolved_pilot | data/processed/citation_contexts_sectioned_resolved_pilot.parquet |
| citation_marker_resolution_pilot_failures | data/processed/citation_marker_resolution_sectioned_pilot_failures.parquet |

- Limit: 100000
- Random sample: False

## Core Metrics
| metric | value |
| --- | --- |
| total input contexts processed | 100000 |
| output rows | 147542 |
| duplicate context_id count before | 0 |
| duplicate context_id count after | 0 |
| citing_paper_id coverage in aligned graph | 0.890 |
| author_year_clear rate | 0.395 |
| multi_candidate_ambiguous rate | 0.018 |
| ambiguous_year_only rate | 0.005 |
| numeric_marker_unresolved_no_bibliography rate | 0.040 |
| bibliography_unresolved rate | 0.469 |
| resolved_cited_title non-empty rate | 0.405 |

## Resolution Status Distribution
| status | rows |
| --- | --- |
| bibliography_unresolved | 69166 |
| author_year_clear | 58298 |
| citing_paper_not_in_aligned_graph | 9213 |
| numeric_marker_unresolved_no_bibliography | 5960 |
| multi_candidate_ambiguous | 2609 |
| author_year_weak_nonfirst_author | 970 |
| ambiguous_year_only | 771 |
| year_only_unique_candidate | 555 |

## Before / After Comparison
| metric | before | after |
| --- | --- | --- |
| output_rows | 151401 | 147542 |
| author_year_clear_rate | 0.339 | 0.395 |
| ambiguous_year_only_count | 8763 | 771 |
| year_only_unique_candidate_count | 4680 | 555 |
| bibliography_unresolved_count | 64573 | 69166 |
| duplicate_context_id_count | 0 | 0 |

## 20 Examples: author_year_clear
| context_id | source_context_id | citing_paper_id | citation_marker | marker_type | marker_component_text | parsed_surnames | parsed_year | parsed_year_suffix | resolved_cited_acl_id | resolved_cited_title | matched_candidate_count | resolution_status | resolution_confidence | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_4771edcc3e42c8bb07c7 | ctx_4c265fc01e3bc9f11872 | R13-1042 | Elsner and Charniak (2010) | narrative_author_year | Elsner and Charniak (2010) | elsner;charniak | 2010 | unavailable | J10-3004 | Disentangling Chat | 1 | author_year_clear | 0.95 | In NLP, Elsner and Charniak (2010) described the task of thread disentanglement as "the clustering task of dividing a transcript into a s... |
| ctxr_fc94564ed0054ac2126f | ctx_e7f13d44394b4c7c137f | R13-1042 | (Elsner and Charniak, 2010) | parenthetical_author_year | Elsner and Charniak, 2010 | elsner;charniak | 2010 | unavailable | J10-3004 | Disentangling Chat | 1 | author_year_clear | 0.95 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_d06d69e8921c81b378ac | ctx_0f0eb448b401dd51cdf3 | R13-1042 | Carenini et al. (2008) | narrative_author_year | Carenini et al. (2008) | carenini | 2008 | unavailable | P08-1041 | Summarizing Emails with Conversational Cohesion and Subjectivity | 1 | author_year_clear | 0.9 | Carenini et al. (2008) annotated 39 email "conversations" from the Enron Email Corpus for email summariation. |
| ctxr_68d4edb5f20b826f715b | ctx_5316b90745ae591db502 | R13-1042 | Wan and McKeown (2004) | narrative_author_year | Wan and McKeown (2004) | wan;mckeown | 2004 | unavailable | C04-1079 | Generating Overview Summaries of Ongoing Email Thread Discussions | 1 | author_year_clear | 0.95 | Wan and McKeown (2004) used a privatelyavailable corpus of 300 threads for summary generation. |
| ctxr_b166bf8511a77353542f | ctx_c272b15a642e8261f522 | R13-1042 | Rambow et al. (2004) | narrative_author_year | Rambow et al. (2004) | rambow | 2004 | unavailable | N04-4027 | Summarizing Email Threads | 1 | author_year_clear | 0.9 | Rambow et al. (2004) used a privatelyavailable corpus of 96 email threads for thread summarization. |
| ctxr_6739ef248e0241672c80 | ctx_749b7cb80bcc70164ca3 | R13-1042 | Wan and McKeown (2004) | narrative_author_year | Wan and McKeown (2004) | wan;mckeown | 2004 | unavailable | C04-1079 | Generating Overview Summaries of Ongoing Email Thread Discussions | 1 | author_year_clear | 0.95 | Wan and McKeown (2004) reconstructed threads by header Message-ID information. |
| ctxr_4ba57d063d3c71fa78df | ctx_82c232f3d1dfc98f4dff | R13-1042 | Rambow et al. (2004) | narrative_author_year | Rambow et al. (2004) | rambow | 2004 | unavailable | N04-4027 | Summarizing Email Threads | 1 | author_year_clear | 0.9 | Rambow et al. (2004) used a privately-available corpus of 96 email threads, but did not specify how they determined the threads. |
| ctxr_8361b89d504826d53df9 | ctx_e5dad8f0492b6fb3d95b | R13-1042 | (Hatzivassiloglou et al., 1999) | parenthetical_author_year | Hatzivassiloglou et al., 1999 | hatzivassiloglou | 1999 | unavailable | W99-0625 | Detecting Text Similarity over Short Passages: Exploring Linguistic Feature Combinations via Machine Learning | 1 | author_year_clear | 0.9 | 1999 ) uses pairs of words occurring in the same order for the two emails; Token Pair Distance (Hatzivassiloglou et al., 1999) measures t... |
| ctxr_d573e73d4a69363cdfc0 | ctx_2058502beaf095f8c9d9 | R13-1042 | Elsner and Charniak (2011) | narrative_author_year | Elsner and Charniak (2011) | elsner;charniak | 2011 | unavailable | P11-1118 | Disentangling Chat with Local Coherence Models | 1 | author_year_clear | 0.95 | Elsner and Charniak (2011) use coherence models to disentangle chat, using some features (entity grid, topical entity grid) which corresp... |
| ctxr_044c96a8f9c2342b58ff | ctx_871fbe98e387051e0e49 | R13-1044 | (Rosario and Hearst, 2001 ) | parenthetical_author_year | Rosario and Hearst, 2001 | rosario;hearst | 2001 | unavailable | W01-0511 | Classifying the Semantic Relations in Noun Compounds via a Domain-Specific Lexical Hierarchy | 1 | author_year_clear | 0.95 | In (Rosario and Hearst, 2001 ) authors used neural networks to determine 20 semantic relationssimilarily to (Nastase et al., 2006) -betwe... |
| ctxr_f6863fcab52657a5c16e | ctx_f31d14d5a204a23fdb80 | R13-1044 | (Tratz and Hovy, 2010) | parenthetical_author_year | Tratz and Hovy, 2010 | tratz;hovy | 2010 | unavailable | S10-1049 | {ISI}: Automatic Classification of Relations Between Nominals Using a Maximum Entropy Classifier | 1 | author_year_clear | 0.95 | In (Tratz and Hovy, 2010) the authors developed a system based on the Maximum Entropy classifier, able to detect 10 bidirectional semanti... |
| ctxr_71d08900475d9c8505ab | ctx_fe6ec05f96144fa5a36e | R13-1044 | (Rink and Harabagiu, 2010) | parenthetical_author_year | Rink and Harabagiu, 2010 | rink;harabagiu | 2010 | unavailable | S10-1057 | {UTD}: Classifying Semantic Relations by Combining Lexical and Semantic Resources | 1 | author_year_clear | 0.95 | The same set of semantic relations was used in (Rink and Harabagiu, 2010) . |
| ctxr_b1bfb1536bcb5cbbf8b5 | ctx_797eaae178b0d5c3ea41 | R13-1044 | (Tymoshenko and Giuliano, 2010 ) | parenthetical_author_year | Tymoshenko and Giuliano, 2010 | tymoshenko;giuliano | 2010 | unavailable | S10-1047 | {FBK}-{IRST}: Semantic Relation Extraction Using {C}yc | 1 | author_year_clear | 0.95 | Authors in (Tymoshenko and Giuliano, 2010 ) used shallow syntactic parsing and semantic information from ResearchCyc (Lenat, 1995) in the... |
| ctxr_f8a4c2e6aa2834642a71 | ctx_35ba2ace18b7d4ee7211 | R13-1044 | (Hearst, 1992) | parenthetical_author_year | Hearst, 1992 | hearst | 1992 | unavailable | C92-2082 | Automatic Acquisition of Hyponyms from Large Text Corpora | 1 | author_year_clear | 0.9 | In (Hearst, 1992) authors used set of manually written rules for identification of hyperonymy relations. (Ben Abacha and Zweigenbaum, 201... |
| ctxr_3e4722d1950da619a7dd | ctx_ca6cc2ce8812268acdb7 | R13-1044 | (Broda et al., 2012) | parenthetical_author_year | Broda et al., 2012 | broda | 2012 | unavailable | L12-1574 | {KPW}r: Towards a Free Corpus of {P}olish | 1 | author_year_clear | 0.9 | We made use of a CRF shallow parser (Radziszewski and Pawlaczek, 2012) trained on an annotated corpus of Polish (KPWr) (Broda et al., 201... |
| ctxr_9ab7ad32be76baef24a4 | ctx_31e57195fc09648f4ccb | W05-0818 | (Ayan et al., 2004; Och and Ney, 2000) | parenthetical_author_year | Ayan et al., 2004 | ayan | 2004 | unavailable | 2004.amta-papers.3 | Multi-Align: combining linguistic and statistical techniques to improve alignments for adaptable {MT} | 1 | author_year_clear | 0.9 | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-ba... |
| ctxr_008f302607deda562c24 | ctx_31e57195fc09648f4ccb | W05-0818 | (Ayan et al., 2004; Och and Ney, 2000) | parenthetical_author_year | Och and Ney, 2000 | och;ney | 2000 | unavailable | P00-1056 | Improved Statistical Alignment Models | 1 | author_year_clear | 0.95 | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-ba... |
| ctxr_373b75e6049f7bde6cca | ctx_e70cc82cf2e10336956d | W05-0818 | (Ayan et al., 2004; Och and Ney, 2000) | parenthetical_author_year | Ayan et al., 2004 | ayan | 2004 | unavailable | 2004.amta-papers.3 | Multi-Align: combining linguistic and statistical techniques to improve alignments for adaptable {MT} | 1 | author_year_clear | 0.9 | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-ba... |
| ctxr_18b9cd4865ae3fef4d3f | ctx_e70cc82cf2e10336956d | W05-0818 | (Ayan et al., 2004; Och and Ney, 2000) | parenthetical_author_year | Och and Ney, 2000 | och;ney | 2000 | unavailable | P00-1056 | Improved Statistical Alignment Models | 1 | author_year_clear | 0.95 | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-ba... |
| ctxr_7d7d31957a351c96c69d | ctx_b950942cfc6e4043e721 | W05-0818 | (Carl, 2001; Menezes and Richardson, 2001) | parenthetical_author_year | Carl, 2001 | carl | 2001 | unavailable | W01-0718 | Inducing probabilistic invertible translation grammars from aligned texts | 1 | author_year_clear | 0.9 | Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such as example-ba... |

## 20 Examples: multi_candidate_ambiguous
| context_id | source_context_id | citing_paper_id | citation_marker | marker_type | marker_component_text | parsed_surnames | parsed_year | parsed_year_suffix | resolved_cited_acl_id | resolved_cited_title | matched_candidate_count | resolution_status | resolution_confidence | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_e48cf879e2f66fc29b89 | ctx_ebb2bf87b454fbcc6a35 | W05-0820 | Koehn et al. (2003) | narrative_author_year | Koehn et al. (2003) | koehn | 2003 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | The focus of the task was to build a probabilistic phrase translation table, since most of the other resources were provided -for more on... |
| ctxr_58c25c30dd82c38881bb | ctx_d5504eb13dd65543782a | W05-0820 | (Och, 2003) | parenthetical_author_year | Och, 2003 | och | 2003 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | However, the field is moving fast, and a number of steps help to improve upon the provided baseline setup, e.g., larger language models t... |
| ctxr_b2167b01cb827f01e9fc | ctx_ac8919acb76fb2ee9d36 | R13-1049 | Gandon (2013b) | narrative_author_year | Gandon (2013b) | gandon | 2013 | b | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Lefrançois and Gandon (2013b) therefore introduced a deeper level of representation to describe meanings: the deep semantic level, and de... |
| ctxr_da493e241cd1cd8c2bf6 | ctx_5785da21214d960fe1ce | R13-1049 | Gandon (2013a) | narrative_author_year | Gandon (2013a) | gandon | 2013 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Lefrançois and Gandon (2013a) proposed to use the notion of UGs homomorphism to define this entailment problem. |
| ctxr_cce3eff94f503802dcaf | ctx_dc77f495fe41279b99b7 | R13-1049 | Gandon (2013a) | narrative_author_year | Gandon (2013a) | gandon | 2013 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | More generally, Lefrançois and Gandon (2013a) listed a set of rules which defines the axiomatization of the UGs semantics. |
| ctxr_215af6eda62875174cb7 | ctx_f0f039be652926fe0a20 | R13-1049 | Gandon (2013a) | narrative_author_year | Gandon (2013a) | gandon | 2013 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Lefrançois and Gandon (2013a) illustrated problematic cases where the closure is infinite for finite UGs. |
| ctxr_99b12e760624891c3b57 | ctx_12a4a517ae0a5c895ef5 | R13-1049 | Gandon (2013c) | narrative_author_year | Gandon (2013c) | gandon | 2013 | c | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Lefrançois and Gandon (2013c) listed the different equations that the interpretation function must satisfy so that a model is a model of ... |
| ctxr_bba4196867a8719d1005 | ctx_d1e8229ece9aef375c4d | R13-1052 | (Teufel et al., 2006a) | parenthetical_author_year | Teufel et al., 2006a | teufel | 2006 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Therefore, this task has attracted researchers from the fields of discourse analysis, sociology of science, and information sciences for ... |
| ctxr_69a2ba58eff77370d7af | ctx_13eec0405338ff381dc7 | R13-1052 | (Teufel et al., 2006a) | parenthetical_author_year | Teufel et al., 2006a | teufel | 2006 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Most of the existing research in this area focused on the analysis of citation sentiment, which has achieved good accuracy (see, e.g., (T... |
| ctxr_4bbe9e5dbfade2085ced | ctx_d6bff0684aeeb70b0364 | R13-1052 | Teufel et al. (2006b) | narrative_author_year | Teufel et al. (2006b) | teufel | 2006 | b | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | The weakness of the cited work is discussed Teufel et al. (2006b) is the most related to ours. |
| ctxr_d379efec19d3cd3d2a0b | ctx_fea6387f2f078daebc09 | R13-1052 | Teufel et al. (2006a) | narrative_author_year | Teufel et al. (2006a) | teufel | 2006 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Regarding the automatic recognition of citation functions or citation categories, Teufel et al. (2006a) presented a supervised learning f... |
| ctxr_87750c2349f5ef2aeb99 | ctx_052f15ac80217fa2f715 | R13-1052 | Teufel et al. (2006a) | narrative_author_year | Teufel et al. (2006a) | teufel | 2006 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | It is also worth noting that Teufel et al. (2006a) , Athar (2011) , and Dong and Schäfer (2011) all worked on citations in computational ... |
| ctxr_9d047da0f9850b5c08ab | ctx_0c4dc34767d14cd0050f | R13-1058 | (Fellbaum, 1998; Broda et al., 2012b) | parenthetical_author_year | Broda et al., 2012b | broda | 2012 | b | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Wordnet construction is rather like writing a dictionary (Fellbaum, 1998; Broda et al., 2012b) . |
| ctxr_0d1791de0ca1782618cf | ctx_bb4a884a5ada6aa43cf1 | R13-1058 | (Fellbaum, 1998; Broda et al., 2012b) | parenthetical_author_year | Broda et al., 2012b | broda | 2012 | b | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Wordnet construction is rather like writing a dictionary (Fellbaum, 1998; Broda et al., 2012b) . |
| ctxr_17ffe60329ab0c48240a | ctx_03cf61674e7d40e921fe | R13-1058 | (Broda et al., 2012a) | parenthetical_author_year | Broda et al., 2012a | broda | 2012 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | 10 The corpus consists of 250 million tokens in the ICS PAS Corpus (Przepiórkowski, 2004) ; 113m tokens of news items (Weiss, 2008) ; ≈80... |
| ctxr_35a3a6111af2bb1ca371 | ctx_6c7f26ebd5ac82abdb80 | R13-1058 | (Broda et al., 2012b) | parenthetical_author_year | Broda et al., 2012b | broda | 2012 | b | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | 11 Usage examples, welcome by the editors, help them distinguish senses (Broda et al., 2012b) . ported by WordnetWeaver (Piasecki et al.,... |
| ctxr_c9035d58731a119072ec | ctx_2b0bf0ad417068d2068b | R13-1059 | (Black et al., 1992; Jelinek et al., 1992; Jelinek et al., 1994) | parenthetical_author_year | Black et al., 1992 | black | 1992 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | History based models were initially developed at IBM (Black et al., 1992; Jelinek et al., 1992; Jelinek et al., 1994) . |
| ctxr_5692e0cfb59087d20edc | ctx_34db2f8a1266a55afd75 | R13-1059 | (Black et al., 1992; Jelinek et al., 1992; Jelinek et al., 1994) | parenthetical_author_year | Black et al., 1992 | black | 1992 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | History based models were initially developed at IBM (Black et al., 1992; Jelinek et al., 1992; Jelinek et al., 1994) . |
| ctxr_062629ccb13e7620e79c | ctx_c0d3ee2530a568a8e76c | R13-1059 | (Black et al., 1992; Jelinek et al., 1992; Jelinek et al., 1994) | parenthetical_author_year | Black et al., 1992 | black | 1992 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | History based models were initially developed at IBM (Black et al., 1992; Jelinek et al., 1992; Jelinek et al., 1994) . |
| ctxr_13e7f6a8ac68fa4cdaf1 | ctx_0623b7fee9802a8f6924 | W05-0833 | (Gough & Way, 2004b) | parenthetical_author_year | Gough & Way, 2004b | gough;way | 2004 | b | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | While for the most part the EBMT system of (Gough & Way, 2004b) outperforms any flavour of the phrasebased SMT systems constructed in our... |

## 20 Examples: unresolved markers
| context_id | source_context_id | citing_paper_id | citation_marker | marker_type | marker_component_text | parsed_surnames | parsed_year | parsed_year_suffix | resolved_cited_acl_id | resolved_cited_title | matched_candidate_count | resolution_status | resolution_confidence | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_26ef99dbe1db8dd54215 | ctx_caa30bbd1d1b6df7a22c | R13-1042 | (Aoki et al., 2003) | parenthetical_author_year | Aoki et al., 2003 | aoki | 2003 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_f90327445945bae94871 | ctx_874e02c7114e7d74abc1 | R13-1042 | (Yeh, 2006; Erera and Carmel, 2008) | parenthetical_author_year | Yeh, 2006 | yeh | 2006 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_bf74e38773678ca7c73c | ctx_874e02c7114e7d74abc1 | R13-1042 | (Yeh, 2006; Erera and Carmel, 2008) | parenthetical_author_year | Erera and Carmel, 2008 | erera;carmel | 2008 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_7c7e126007513aeb74c7 | ctx_3a0085973d5d3f39e130 | R13-1042 | (Yeh, 2006; Erera and Carmel, 2008) | parenthetical_author_year | Yeh, 2006 | yeh | 2006 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_979e78129a9cb7cf04e6 | ctx_3a0085973d5d3f39e130 | R13-1042 | (Yeh, 2006; Erera and Carmel, 2008) | parenthetical_author_year | Erera and Carmel, 2008 | erera;carmel | 2008 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_a92d141fe7c9f1db8405 | ctx_83e770e8729de84c3dda | R13-1042 | Joti et al. (2010) | narrative_author_year | Joti et al. (2010) | joti | 2010 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Joti et al. (2010) used the BC3 corpus of 40 email threads and 3222 emails for topic segmentation. |
| ctxr_30903fb804475456d47c | ctx_b75c50a3489f0ec6113e | R13-1042 | Wu and Oard (2005) | narrative_author_year | Wu and Oard (2005) | wu;oard | 2005 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Wu and Oard (2005) , and Zhu et al. (2005) auto-threaded all messages with identical, non-trivial, Fwd: and Re:-stripped Subject headers. |
| ctxr_06483519d5239540f8ad | ctx_3db879d855179f1fd5e7 | R13-1042 | Zhu et al. (2005) | narrative_author_year | Zhu et al. (2005) | zhu | 2005 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Wu and Oard (2005) , and Zhu et al. (2005) auto-threaded all messages with identical, non-trivial, Fwd: and Re:-stripped Subject headers. |
| ctxr_2e14793ab64c0c1d527b | ctx_98144c4450bb8b1c0c28 | R13-1042 | Klimt and Yang (2004) | narrative_author_year | Klimt and Yang (2004) | klimt;yang | 2004 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Klimt and Yang (2004) auto-threaded messages that had stripped Subject headers and were among the same users (addresses). |
| ctxr_9486cce96e49b81c4732 | ctx_a7ebe2b9e68fc592f67e | R13-1042 | Lewis and Knowles (1997) | narrative_author_year | Lewis and Knowles (1997) | lewis;knowles | 1997 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Lewis and Knowles (1997) assigned emails to threads by matching quotation structures between emails. |
| ctxr_f6890f8b41fe4e573895 | ctx_36791895b781e4b296a8 | R13-1042 | Klimt and Yang (2004) | narrative_author_year | Klimt and Yang (2004) | klimt;yang | 2004 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | First, we implemented Klimt and Yang (2004) 's technique of clustering the emails into threads that have the same Subject header (after i... |
| ctxr_e00783143d6ac1ac7fe5 | ctx_782bb2eba603a747dbcd | R13-1042 | Klimt and Yang (2004) | narrative_author_year | Klimt and Yang (2004) | klimt;yang | 2004 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | In addition, many clusters consisted of all of the issues of a monthly subscription newsletter, or nearly identical petitions (see Klimt ... |
| ctxr_1cd3139fa2d367e9718a | ctx_72b300fea9c097b56058 | R13-1042 | Klimt and Yang (2004) | narrative_author_year | Klimt and Yang (2004) | klimt;yang | 2004 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | In order to avoid creating redundant threads, which would be an information leak risk during evaluation, we selected as the thread source... |
| ctxr_8e97d40c51c76600aea0 | ctx_67186a992135f73ff4ea | R13-1042 | Yeh (2006) | narrative_author_year | Yeh (2006) | yeh | 2006 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | We used the quoteidentifying regular expressions from Yeh (2006) (see Table 1 ) to identify quoted previous emails. |
| ctxr_77b5217607ceb30638bb | ctx_42406514152d2d31a609 | R13-1042 | (2011) | year_only | 2011 |  | 2011 | unavailable | unavailable |  | 2 | ambiguous_year_only | 0.0 | We evaluate a number of text similarity measures, divided according to Bär et al. (2011) 's three groups: Content Similarity, Structural ... |
| ctxr_81662dd84711ad7b8524 | ctx_09e1fe05d365fd881476 | R13-1042 | (Gusfield, 1997) | parenthetical_author_year | Gusfield, 1997 | gusfield | 1997 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | The Longest Common Substring measure (Gusfield, 1997) identifies uninterrupted common strings, while the Longest Common Subsequence measu... |
| ctxr_2efa0196a03571fae5ff | ctx_acaf6987af2a31216ca9 | R13-1042 | (Allison and Dix, 1986) | parenthetical_author_year | Allison and Dix, 1986 | allison;dix | 1986 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | The Longest Common Substring measure (Gusfield, 1997) identifies uninterrupted common strings, while the Longest Common Subsequence measu... |
| ctxr_428cdc0a9745535183fa | ctx_e88e90eaec0ae58b2452 | R13-1042 | (Wise, 1996) | parenthetical_author_year | Wise, 1996 | wise | 1996 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | The Longest Common Substring measure (Gusfield, 1997) identifies uninterrupted common strings, while the Longest Common Subsequence measu... |
| ctxr_6b947f6fb2a9c48adae0 | ctx_c9f40bf1aa9610b46fb2 | R13-1042 | Levenshtein (1966) | narrative_author_year | Levenshtein (1966) | levenshtein | 1966 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Other measures which treat texts as sequences of characters and compute similarities with various metrics include Levenshtein (1966) , Mo... |
| ctxr_e8895c5af830b1ebf3ab | ctx_638081887b0da8f57688 | R13-1042 | (Monge and Elkan, 1997) | parenthetical_author_year | Monge and Elkan, 1997 | monge;elkan | 1997 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Other measures which treat texts as sequences of characters and compute similarities with various metrics include Levenshtein (1966) , Mo... |

## Common Failure Patterns
| resolution_status | resolution_method | rows |
| --- | --- | --- |
| bibliography_unresolved | author_year_no_candidate | 68053 |
| citing_paper_not_in_aligned_graph | no_candidate_graph_for_citing_paper | 9213 |
| numeric_marker_unresolved_no_bibliography | numeric_marker | 5960 |
| multi_candidate_ambiguous | author_year_multiple_candidates | 2536 |
| author_year_weak_nonfirst_author | author_year_nonfirst_author_candidate_graph | 970 |
| bibliography_unresolved | year_only_no_candidate | 910 |
| ambiguous_year_only | year_only_multiple_candidates | 771 |
| year_only_unique_candidate | year_only_unique_candidate | 555 |
| bibliography_unresolved | marker_parse_failed | 203 |
| multi_candidate_ambiguous | author_year_multiple_weak_nonfirst_candidates | 73 |
