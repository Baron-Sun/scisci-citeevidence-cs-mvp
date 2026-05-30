# Citation Marker Resolution Pilot Report

## Inputs
| name | path |
| --- | --- |
| citation_contexts | data/processed/citation_contexts.parquet |
| acl_citation_graph_aligned | data/interim/acl_citation_graph_aligned.parquet |
| acl_id_crosswalk | data/interim/acl_id_crosswalk.parquet |

## Outputs
| name | path |
| --- | --- |
| citation_contexts_resolved_pilot | data/processed/citation_contexts_resolved_pilot.parquet |
| citation_marker_resolution_pilot_failures | data/processed/citation_marker_resolution_pilot_failures.parquet |

- Limit: 100000
- Random sample: False

## Core Metrics
| metric | value |
| --- | --- |
| total input contexts processed | 100000 |
| output rows | 151401 |
| duplicate context_id count before | 0 |
| duplicate context_id count after | 0 |
| citing_paper_id coverage in aligned graph | 0.890 |
| author_year_clear rate | 0.395 |
| multi_candidate_ambiguous rate | 0.021 |
| ambiguous_year_only rate | 0.005 |
| numeric_marker_unresolved_no_bibliography rate | 0.044 |
| bibliography_unresolved rate | 0.461 |
| resolved_cited_title non-empty rate | 0.406 |

## Resolution Status Distribution
| status | rows |
| --- | --- |
| bibliography_unresolved | 69846 |
| author_year_clear | 59870 |
| citing_paper_not_in_aligned_graph | 9599 |
| numeric_marker_unresolved_no_bibliography | 6612 |
| multi_candidate_ambiguous | 3109 |
| author_year_weak_nonfirst_author | 1006 |
| ambiguous_year_only | 820 |
| year_only_unique_candidate | 539 |

## Before / After Comparison
| metric | before | after |
| --- | --- | --- |
| output_rows | 151401 | 151401 |
| author_year_clear_rate | 0.339 | 0.395 |
| ambiguous_year_only_count | 8763 | 820 |
| year_only_unique_candidate_count | 4680 | 539 |
| bibliography_unresolved_count | 64573 | 69846 |
| duplicate_context_id_count | 0 | 0 |

## 20 Examples: author_year_clear
| context_id | source_context_id | citing_paper_id | citation_marker | marker_type | marker_component_text | parsed_surnames | parsed_year | parsed_year_suffix | resolved_cited_acl_id | resolved_cited_title | matched_candidate_count | resolution_status | resolution_confidence | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_8acd2c1309a01d7d9fbe | ctx_f5a8ef448e419a5962e9 | R13-1042 | Elsner and Charniak (2010) | narrative_author_year | Elsner and Charniak (2010) | elsner;charniak | 2010 | unavailable | J10-3004 | Disentangling Chat | 1 | author_year_clear | 0.95 | In NLP, Elsner and Charniak (2010) described the task of thread disentanglement as "the clustering task of dividing a transcript into a s... |
| ctxr_a81b774daf34da164986 | ctx_c96effc8990421130b1a | R13-1042 | (Elsner and Charniak, 2010) | parenthetical_author_year | Elsner and Charniak, 2010 | elsner;charniak | 2010 | unavailable | J10-3004 | Disentangling Chat | 1 | author_year_clear | 0.95 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_cb9204c9bc2046a74509 | ctx_16fc322d29d6d468898f | R13-1042 | Carenini et al. (2008) | narrative_author_year | Carenini et al. (2008) | carenini | 2008 | unavailable | P08-1041 | Summarizing Emails with Conversational Cohesion and Subjectivity | 1 | author_year_clear | 0.9 | Carenini et al. (2008) annotated 39 email "conversations" from the Enron Email Corpus for email summariation. |
| ctxr_a9ff67947ca8f4d3196b | ctx_3f0445d761995bc0b49a | R13-1042 | Wan and McKeown (2004) | narrative_author_year | Wan and McKeown (2004) | wan;mckeown | 2004 | unavailable | C04-1079 | Generating Overview Summaries of Ongoing Email Thread Discussions | 1 | author_year_clear | 0.95 | Wan and McKeown (2004) used a privatelyavailable corpus of 300 threads for summary generation. |
| ctxr_34c632eb16326af33f2c | ctx_8e7c554e21eecfe607c1 | R13-1042 | Rambow et al. (2004) | narrative_author_year | Rambow et al. (2004) | rambow | 2004 | unavailable | N04-4027 | Summarizing Email Threads | 1 | author_year_clear | 0.9 | Rambow et al. (2004) used a privatelyavailable corpus of 96 email threads for thread summarization. |
| ctxr_d3619079fb0cec400e72 | ctx_3995d33895edc650d05c | R13-1042 | Wan and McKeown (2004) | narrative_author_year | Wan and McKeown (2004) | wan;mckeown | 2004 | unavailable | C04-1079 | Generating Overview Summaries of Ongoing Email Thread Discussions | 1 | author_year_clear | 0.95 | Wan and McKeown (2004) reconstructed threads by header Message-ID information. |
| ctxr_be9f543903e1b82b6c23 | ctx_2617301cece88373eeed | R13-1042 | Rambow et al. (2004) | narrative_author_year | Rambow et al. (2004) | rambow | 2004 | unavailable | N04-4027 | Summarizing Email Threads | 1 | author_year_clear | 0.9 | Rambow et al. (2004) used a privately-available corpus of 96 email threads, but did not specify how they determined the threads. |
| ctxr_811cabbfb97255595932 | ctx_60a86164b026b1c82887 | R13-1042 | (Hatzivassiloglou et al., 1999) | parenthetical_author_year | Hatzivassiloglou et al., 1999 | hatzivassiloglou | 1999 | unavailable | W99-0625 | Detecting Text Similarity over Short Passages: Exploring Linguistic Feature Combinations via Machine Learning | 1 | author_year_clear | 0.9 | 1999 ) uses pairs of words occurring in the same order for the two emails; Token Pair Distance (Hatzivassiloglou et al., 1999) measures t... |
| ctxr_271ba5f1663080d77db0 | ctx_1a5b77355c072a0fad2c | R13-1044 | (Rosario and Hearst, 2001) | parenthetical_author_year | Rosario and Hearst, 2001 | rosario;hearst | 2001 | unavailable | W01-0511 | Classifying the Semantic Relations in Noun Compounds via a Domain-Specific Lexical Hierarchy | 1 | author_year_clear | 0.95 | In (Rosario and Hearst, 2001) authors used neural networks to determine 20 semantic relationssimilarily to (Nastase et al., 2006) -betwee... |
| ctxr_960469994ac4a440b729 | ctx_e77ed08bc72bff473396 | R13-1044 | (Tratz and Hovy, 2010) | parenthetical_author_year | Tratz and Hovy, 2010 | tratz;hovy | 2010 | unavailable | S10-1049 | {ISI}: Automatic Classification of Relations Between Nominals Using a Maximum Entropy Classifier | 1 | author_year_clear | 0.95 | In (Tratz and Hovy, 2010) the authors developed a system based on the Maximum Entropy classifier, able to detect 10 bidirectional semanti... |
| ctxr_2555ecb4712cb7e2db1c | ctx_9bdb1387cc200719e735 | R13-1044 | (Rink and Harabagiu, 2010) | parenthetical_author_year | Rink and Harabagiu, 2010 | rink;harabagiu | 2010 | unavailable | S10-1057 | {UTD}: Classifying Semantic Relations by Combining Lexical and Semantic Resources | 1 | author_year_clear | 0.95 | The same set of semantic relations was used in (Rink and Harabagiu, 2010) . |
| ctxr_5ed06e05f15b91082bec | ctx_986f87d549660bd38028 | R13-1044 | (Tymoshenko and Giuliano, 2010 ) | parenthetical_author_year | Tymoshenko and Giuliano, 2010 | tymoshenko;giuliano | 2010 | unavailable | S10-1047 | {FBK}-{IRST}: Semantic Relation Extraction Using {C}yc | 1 | author_year_clear | 0.95 | Authors in (Tymoshenko and Giuliano, 2010 ) used shallow syntactic parsing and semantic information from ResearchCyc (Lenat, 1995) in the... |
| ctxr_dbc3c42dc58e91642641 | ctx_906e8bec7828fe5e4bf1 | R13-1044 | (Hearst, 1992) | parenthetical_author_year | Hearst, 1992 | hearst | 1992 | unavailable | C92-2082 | Automatic Acquisition of Hyponyms from Large Text Corpora | 1 | author_year_clear | 0.9 | In (Hearst, 1992) authors used set of manually written rules for identification of hyperonymy relations. (Ben Abacha and Zweigenbaum, 201... |
| ctxr_d5ae927b69268d4721a3 | ctx_0b022dfa768255504380 | R13-1044 | (Broda et al., 2012) | parenthetical_author_year | Broda et al., 2012 | broda | 2012 | unavailable | L12-1574 | {KPW}r: Towards a Free Corpus of {P}olish | 1 | author_year_clear | 0.9 | We made use of a CRF shallow parser (Radziszewski and Pawlaczek, 2012) trained on an annotated corpus of Polish (KPWr) (Broda et al., 201... |
| ctxr_aaae79f136fe2a820510 | ctx_9ac1e28cf348e55ace28 | W05-0818 | (Ayan et al., 2004; Och and Ney, 2000) | parenthetical_author_year | Ayan et al., 2004 | ayan | 2004 | unavailable | 2004.amta-papers.3 | Multi-Align: combining linguistic and statistical techniques to improve alignments for adaptable {MT} | 1 | author_year_clear | 0.9 | Introduction Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such ... |
| ctxr_b96ea3af7c6ad4307c10 | ctx_9ac1e28cf348e55ace28 | W05-0818 | (Ayan et al., 2004; Och and Ney, 2000) | parenthetical_author_year | Och and Ney, 2000 | och;ney | 2000 | unavailable | P00-1056 | Improved Statistical Alignment Models | 1 | author_year_clear | 0.95 | Introduction Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such ... |
| ctxr_65e85a750a4840b9d7f2 | ctx_fdc6755df3154c8dcd18 | W05-0818 | (Ayan et al., 2004; Och and Ney, 2000) | parenthetical_author_year | Ayan et al., 2004 | ayan | 2004 | unavailable | 2004.amta-papers.3 | Multi-Align: combining linguistic and statistical techniques to improve alignments for adaptable {MT} | 1 | author_year_clear | 0.9 | Introduction Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such ... |
| ctxr_952c4e093732c10af1af | ctx_fdc6755df3154c8dcd18 | W05-0818 | (Ayan et al., 2004; Och and Ney, 2000) | parenthetical_author_year | Och and Ney, 2000 | och;ney | 2000 | unavailable | P00-1056 | Improved Statistical Alignment Models | 1 | author_year_clear | 0.95 | Introduction Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such ... |
| ctxr_bd8a1e78d7f124a91e3f | ctx_a2131a243ac3fc1d8d97 | W05-0818 | (Carl, 2001; Menezes and Richardson, 2001) | parenthetical_author_year | Carl, 2001 | carl | 2001 | unavailable | W01-0718 | Inducing probabilistic invertible translation grammars from aligned texts | 1 | author_year_clear | 0.9 | Introduction Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such ... |
| ctxr_32ccd236fac9499ecb2e | ctx_a2131a243ac3fc1d8d97 | W05-0818 | (Carl, 2001; Menezes and Richardson, 2001) | parenthetical_author_year | Menezes and Richardson, 2001 | menezes;richardson | 2001 | unavailable | W01-1406 | A best-first alignment algorithm for automatic extraction of transfer mappings from bilingual corpora | 1 | author_year_clear | 0.95 | Introduction Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such ... |

## 20 Examples: multi_candidate_ambiguous
| context_id | source_context_id | citing_paper_id | citation_marker | marker_type | marker_component_text | parsed_surnames | parsed_year | parsed_year_suffix | resolved_cited_acl_id | resolved_cited_title | matched_candidate_count | resolution_status | resolution_confidence | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_61890b276ec1791ea871 | ctx_9d4e7b766d7ef29394e6 | W05-0820 | Koehn et al. (2003) | narrative_author_year | Koehn et al. (2003) | koehn | 2003 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | The focus of the task was to build a probabilistic phrase translation table, since most of the other resources were provided -for more on... |
| ctxr_f318041029151e2f45e0 | ctx_fff467db8f9d0e00bbe9 | W05-0820 | (Och, 2003) | parenthetical_author_year | Och, 2003 | och | 2003 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | However, the field is moving fast, and a number of steps help to improve upon the provided baseline setup, e.g., larger language models t... |
| ctxr_368e4f80df3daf5528e8 | ctx_c7f05049d870d09a4883 | R13-1049 | Gandon (2013b) | narrative_author_year | Gandon (2013b) | gandon | 2013 | b | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Lefranc ¸ois and Gandon (2013b) therefore introduced a deeper level of representation to describe meanings: the deep semantic level, and ... |
| ctxr_dae06ff483940445f7c1 | ctx_09cf0273f979fe54f560 | R13-1049 | Gandon (2013a) | narrative_author_year | Gandon (2013a) | gandon | 2013 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Reasoning with UGs-Homomorphisms Lefranc ¸ois and Gandon (2013a) proposed to use the notion of UGs homomorphism to define this entailment... |
| ctxr_93652e9edd0ea145482f | ctx_026b3e0967ee5174c966 | R13-1049 | Gandon (2013a) | narrative_author_year | Gandon (2013a) | gandon | 2013 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | More generally, Lefranc ¸ois and Gandon (2013a) listed a set of rules which defines the axiomatization of the UGs semantics. |
| ctxr_5d2b8596cd6a67347369 | ctx_215b1f20278ce7e94b57 | R13-1049 | Gandon (2013a) | narrative_author_year | Gandon (2013a) | gandon | 2013 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Lefranc ¸ois and Gandon (2013a) illustrated problematic cases where the closure is infinite for finite UGs. |
| ctxr_f2d383d14ae734c87333 | ctx_6bcace7d35adbf4208be | R13-1049 | Gandon (2013c) | narrative_author_year | Gandon (2013c) | gandon | 2013 | c | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | In order to deal with the problem of prohibited and optional ASlots, D contains a special element denoted • that represents nothing, plus... |
| ctxr_f75ec33af02057c8dd39 | ctx_03a39c4083f54c7e650b | R13-1052 | (Teufel et al., 2006a) | parenthetical_author_year | Teufel et al., 2006a | teufel | 2006 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Therefore, this task has attracted researchers from the fields of discourse analysis, sociology of science, and information sciences for ... |
| ctxr_dbe01ea829a5a6d8dfd8 | ctx_da2274fcb5133b61c73a | R13-1052 | (Teufel et al., 2006a) | parenthetical_author_year | Teufel et al., 2006a | teufel | 2006 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Most of the existing research in this area focused on the analysis of citation sentiment, which has achieved good accuracy (see, e.g., (T... |
| ctxr_8e00f920759af7341e23 | ctx_57924bea47f6bb335335 | R13-1052 | Teufel et al. (2006a) | narrative_author_year | Teufel et al. (2006a) | teufel | 2006 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Regarding the automatic recognition of citation functions or citation categories, Teufel et al. (2006a) presented a supervised learning f... |
| ctxr_8e7d99a0d7d50a66dfc4 | ctx_b98cd13ca6a596debb64 | R13-1052 | Teufel et al. (2006a) | narrative_author_year | Teufel et al. (2006a) | teufel | 2006 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | It is also worth noting that Teufel et al. (2006a) , Athar (2011) , and Dong and Schäfer (2011) all worked on citations in computational ... |
| ctxr_d1e69052d74ba431997f | ctx_bf4afe06eeb309cb290b | W05-0824 | Koehn et al. (2003) | narrative_author_year | Koehn et al. (2003) | koehn | 2003 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | For acquiring a PBM, we followed the approach described by Koehn et al. (2003) . |
| ctxr_79b8327d78ede51192f4 | ctx_6f0542735039fb46a5a1 | W05-0824 | Koehn et al. (2003) | narrative_author_year | Koehn et al. (2003) | koehn | 2003 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | We did try to use the alignment produced with IBM model 4, but did not notice significant differences over our experiments; an observatio... |
| ctxr_8b6c6fe677dca8f06dc4 | ctx_206aa54b8da42f815d43 | 2009.mtsummit-posters.17 | (Koehn et al., 2007) | parenthetical_author_year | Koehn et al., 2007 | koehn | 2007 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | We are only aware of one other large Arabic/French news translation system, the one that was developed during the TRAMES project (Hasan a... |
| ctxr_6cf781662242f92b2d7c | ctx_926be6c7c9b051cb72bf | R13-1053 | Kholy and Habash (2012) | narrative_author_year | Kholy and Habash (2012) | kholy;habash | 2012 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | To do so, like Kholy and Habash (2012) , who use aligned sentence pair of reference translations (reference experiments) instead of the o... |
| ctxr_653f06c8524678a05170 | ctx_43a196365b442397b525 | R13-1053 | Kholy and Habash (2012) | narrative_author_year | Kholy and Habash (2012) | kholy;habash | 2012 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | In comparison with the baseline used by El Kholy and Habash (2012) , this baseline is more stringent. |
| ctxr_3cfd3bdb47119569159d | ctx_4b833fbdfe890b8945f1 | R13-1053 | Kholy and Habash (2012) | narrative_author_year | Kholy and Habash (2012) | kholy;habash | 2012 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Recently, a novel approach to generate rich morphology is proposed by El Kholy and Habash (2012) . |
| ctxr_f30b0e5fbf1b070cfa67 | ctx_a16ac1fab726475739e8 | R13-1053 | (El Kholy and Habash, 2012) | parenthetical_author_year | El Kholy and Habash, 2012 | kholy;habash | 2012 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | They also have used their proposed method to model rich morphology in SMT (El Kholy and Habash, 2012) . |
| ctxr_32ca9ef9579c49021523 | ctx_c4b74b1e97e4399ead1f | R13-1053 | Kholy and Habash (2012) | narrative_author_year | Kholy and Habash (2012) | kholy;habash | 2012 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | So, our baseline is more stringent than the baseline used by El Kholy and Habash (2012) . |
| ctxr_24f6600d62738fdfef04 | ctx_3a46e6d6f15739ac8af6 | R13-1058 | (Fellbaum, 1998; Broda et al., 2012b) | parenthetical_author_year | Broda et al., 2012b | broda | 2012 | b | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | The construction process Wordnet construction is rather like writing a dictionary (Fellbaum, 1998; Broda et al., 2012b) . |

## 20 Examples: unresolved markers
| context_id | source_context_id | citing_paper_id | citation_marker | marker_type | marker_component_text | parsed_surnames | parsed_year | parsed_year_suffix | resolved_cited_acl_id | resolved_cited_title | matched_candidate_count | resolution_status | resolution_confidence | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_bb07ab8e63946662466e | ctx_067ce962ce3e28d300dc | R13-1042 | (Aoki et al., 2003) | parenthetical_author_year | Aoki et al., 2003 | aoki | 2003 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_f1c290e295f3a75af395 | ctx_caed847ef55be44e5728 | R13-1042 | (Yeh, 2006; Erera and Carmel, 2008) | parenthetical_author_year | Yeh, 2006 | yeh | 2006 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_cc0991ffc997c3591f4e | ctx_caed847ef55be44e5728 | R13-1042 | (Yeh, 2006; Erera and Carmel, 2008) | parenthetical_author_year | Erera and Carmel, 2008 | erera;carmel | 2008 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_7497761333f5a3bc5e7b | ctx_84911bcb87933038f4ef | R13-1042 | (Yeh, 2006; Erera and Carmel, 2008) | parenthetical_author_year | Yeh, 2006 | yeh | 2006 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_26b905891a80c2899342 | ctx_84911bcb87933038f4ef | R13-1042 | (Yeh, 2006; Erera and Carmel, 2008) | parenthetical_author_year | Erera and Carmel, 2008 | erera;carmel | 2008 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_d235fb7807b9c99ba196 | ctx_0654fb914da78fe27f64 | R13-1042 | Joti et al. (2010) | narrative_author_year | Joti et al. (2010) | joti | 2010 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Joti et al. (2010) used the BC3 corpus of 40 email threads and 3222 emails for topic segmentation. |
| ctxr_d322f7ff4d50fbac5054 | ctx_dfa13b651de4c8a38ac8 | R13-1042 | Wu and Oard (2005) | narrative_author_year | Wu and Oard (2005) | wu;oard | 2005 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Wu and Oard (2005) , and Zhu et al. (2005) auto-threaded all messages with identical, non-trivial, Fwd: and Re:-stripped Subject headers. |
| ctxr_90321b21ef931f0e3153 | ctx_76bfce41e4c188115fe0 | R13-1042 | Zhu et al. (2005) | narrative_author_year | Zhu et al. (2005) | zhu | 2005 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Wu and Oard (2005) , and Zhu et al. (2005) auto-threaded all messages with identical, non-trivial, Fwd: and Re:-stripped Subject headers. |
| ctxr_c6f0b16d3775fdc2a4a2 | ctx_5316c651106c2cd46fe9 | R13-1042 | Klimt and Yang (2004) | narrative_author_year | Klimt and Yang (2004) | klimt;yang | 2004 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Klimt and Yang (2004) auto-threaded messages that had stripped Subject headers and were among the same users (addresses). |
| ctxr_ca78bb440577b72276c6 | ctx_6def7a00a3f4ce76a5f2 | R13-1042 | Lewis and Knowles (1997) | narrative_author_year | Lewis and Knowles (1997) | lewis;knowles | 1997 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Lewis and Knowles (1997) assigned emails to threads by matching quotation structures between emails. |
| ctxr_99e495a37bfdd522f8b1 | ctx_aebefe0b75286ed91920 | R13-1042 | Klimt and Yang (2004) | narrative_author_year | Klimt and Yang (2004) | klimt;yang | 2004 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | First, we implemented Klimt and Yang (2004) 's technique of clustering the emails into threads that have the same Subject header (after i... |
| ctxr_32fe6755730a4e8322ed | ctx_d7851e0e9cedd00716ca | R13-1042 | Klimt and Yang (2004) | narrative_author_year | Klimt and Yang (2004) | klimt;yang | 2004 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | In addition, many clusters consisted of all of the issues of a monthly subscription newsletter, or nearly identical petitions (see Klimt ... |
| ctxr_b497ec8b8e56455595c1 | ctx_7326cac7c1759aa26da9 | R13-1042 | Klimt and Yang (2004) | narrative_author_year | Klimt and Yang (2004) | klimt;yang | 2004 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | In order to avoid creating redundant threads, which would be an information leak risk during evaluation, we selected as the thread source... |
| ctxr_4bce172c47afa248433b | ctx_c0ca7e2fa6fe568cbcdb | R13-1042 | Yeh (2006) | narrative_author_year | Yeh (2006) | yeh | 2006 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | We used the quoteidentifying regular expressions from Yeh (2006) (see Table 1 ) to identify quoted previous emails. |
| ctxr_2d439beb4a497a00d6ad | ctx_705aee42cff2db25eec0 | R13-1042 | (2011) | year_only | 2011 |  | 2011 | unavailable | unavailable |  | 2 | ambiguous_year_only | 0.0 | We evaluate a number of text similarity measures, divided according to Bär et al. (2011) 's three groups: Content Similarity, Structural ... |
| ctxr_8ee3bf3af7318e13edcc | ctx_60ecb7ed462c462f850b | R13-1042 | (Gusfield, 1997) | parenthetical_author_year | Gusfield, 1997 | gusfield | 1997 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | The Longest Common Substring measure (Gusfield, 1997) identifies uninterrupted common strings, while the Longest Common Subsequence measu... |
| ctxr_28b6c151683f24b3a374 | ctx_f3cb4976b437f49ebf0f | R13-1042 | (Allison and Dix, 1986 ) | parenthetical_author_year | Allison and Dix, 1986 | allison;dix | 1986 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | The Longest Common Substring measure (Gusfield, 1997) identifies uninterrupted common strings, while the Longest Common Subsequence measu... |
| ctxr_e18eae5b7940413e6cd1 | ctx_6f9a8263a7428098ef3a | R13-1042 | (Wise, 1996) | parenthetical_author_year | Wise, 1996 | wise | 1996 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | The Longest Common Substring measure (Gusfield, 1997) identifies uninterrupted common strings, while the Longest Common Subsequence measu... |
| ctxr_ca63e53d64061933278d | ctx_b6c21e9af1bf1db9c03d | R13-1042 | Levenshtein (1966) | narrative_author_year | Levenshtein (1966) | levenshtein | 1966 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Other measures which treat texts as sequences of characters and compute similarities with various metrics include Levenshtein (1966) , Mo... |
| ctxr_54e7766205423dd6ec6d | ctx_808e2c4ba31264e7687d | R13-1042 | (Monge and Elkan, 1997) | parenthetical_author_year | Monge and Elkan, 1997 | monge;elkan | 1997 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Other measures which treat texts as sequences of characters and compute similarities with various metrics include Levenshtein (1966) , Mo... |

## Common Failure Patterns
| resolution_status | resolution_method | rows |
| --- | --- | --- |
| bibliography_unresolved | author_year_no_candidate | 68703 |
| citing_paper_not_in_aligned_graph | no_candidate_graph_for_citing_paper | 9599 |
| numeric_marker_unresolved_no_bibliography | numeric_marker | 6612 |
| multi_candidate_ambiguous | author_year_multiple_candidates | 3034 |
| author_year_weak_nonfirst_author | author_year_nonfirst_author_candidate_graph | 1006 |
| bibliography_unresolved | year_only_no_candidate | 927 |
| ambiguous_year_only | year_only_multiple_candidates | 820 |
| year_only_unique_candidate | year_only_unique_candidate | 539 |
| bibliography_unresolved | marker_parse_failed | 216 |
| multi_candidate_ambiguous | author_year_multiple_weak_nonfirst_candidates | 75 |
