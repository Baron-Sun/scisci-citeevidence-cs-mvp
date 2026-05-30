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
| author_year_clear rate | 0.391 |
| multi_candidate_ambiguous rate | 0.039 |
| ambiguous_year_only rate | 0.005 |
| numeric_marker_unresolved_no_bibliography rate | 0.044 |
| bibliography_unresolved rate | 0.454 |
| resolved_cited_title non-empty rate | 0.395 |

## Resolution Status Distribution
| status | rows |
| --- | --- |
| bibliography_unresolved | 68681 |
| author_year_clear | 59237 |
| citing_paper_not_in_aligned_graph | 9599 |
| numeric_marker_unresolved_no_bibliography | 6612 |
| multi_candidate_ambiguous | 5913 |
| ambiguous_year_only | 820 |
| year_only_unique_candidate | 539 |

## Before / After Comparison
| metric | before | after |
| --- | --- | --- |
| output_rows | 151401 | 151401 |
| author_year_clear_rate | 0.339 | 0.391 |
| ambiguous_year_only_count | 8763 | 820 |
| year_only_unique_candidate_count | 4680 | 539 |
| bibliography_unresolved_count | 64573 | 68681 |
| duplicate_context_id_count | 0 | 0 |

## 20 Examples: author_year_clear
| context_id | source_context_id | citing_paper_id | citation_marker | marker_type | marker_component_text | parsed_surnames | parsed_year | parsed_year_suffix | resolved_cited_acl_id | resolved_cited_title | matched_candidate_count | resolution_status | resolution_confidence | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_080877be7b27070708b2 | ctx_f5a8ef448e419a5962e9 | R13-1042 | Elsner and Charniak (2010) | narrative_author_year | Elsner and Charniak (2010) | elsner;charniak | 2010 | unavailable | J10-3004 | Disentangling Chat | 1 | author_year_clear | 0.95 | In NLP, Elsner and Charniak (2010) described the task of thread disentanglement as "the clustering task of dividing a transcript into a s... |
| ctxr_9a48ff35ae92c59def3c | ctx_c96effc8990421130b1a | R13-1042 | (Elsner and Charniak, 2010) | parenthetical_author_year | Elsner and Charniak, 2010 | elsner;charniak | 2010 | unavailable | J10-3004 | Disentangling Chat | 1 | author_year_clear | 0.95 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_858183e005c3734068ac | ctx_16fc322d29d6d468898f | R13-1042 | Carenini et al. (2008) | narrative_author_year | Carenini et al. (2008) | carenini | 2008 | unavailable | P08-1041 | Summarizing Emails with Conversational Cohesion and Subjectivity | 1 | author_year_clear | 0.9 | Carenini et al. (2008) annotated 39 email "conversations" from the Enron Email Corpus for email summariation. |
| ctxr_e347679b1eb6d29ce610 | ctx_3f0445d761995bc0b49a | R13-1042 | Wan and McKeown (2004) | narrative_author_year | Wan and McKeown (2004) | wan;mckeown | 2004 | unavailable | C04-1079 | Generating Overview Summaries of Ongoing Email Thread Discussions | 1 | author_year_clear | 0.95 | Wan and McKeown (2004) used a privatelyavailable corpus of 300 threads for summary generation. |
| ctxr_51fae22bc946cd4baab4 | ctx_8e7c554e21eecfe607c1 | R13-1042 | Rambow et al. (2004) | narrative_author_year | Rambow et al. (2004) | rambow | 2004 | unavailable | N04-4027 | Summarizing Email Threads | 1 | author_year_clear | 0.9 | Rambow et al. (2004) used a privatelyavailable corpus of 96 email threads for thread summarization. |
| ctxr_bd2c7c36bdcc321046c1 | ctx_3995d33895edc650d05c | R13-1042 | Wan and McKeown (2004) | narrative_author_year | Wan and McKeown (2004) | wan;mckeown | 2004 | unavailable | C04-1079 | Generating Overview Summaries of Ongoing Email Thread Discussions | 1 | author_year_clear | 0.95 | Wan and McKeown (2004) reconstructed threads by header Message-ID information. |
| ctxr_f000b152a55f6da27ee3 | ctx_2617301cece88373eeed | R13-1042 | Rambow et al. (2004) | narrative_author_year | Rambow et al. (2004) | rambow | 2004 | unavailable | N04-4027 | Summarizing Email Threads | 1 | author_year_clear | 0.9 | Rambow et al. (2004) used a privately-available corpus of 96 email threads, but did not specify how they determined the threads. |
| ctxr_3d574f3886fc6fbcd408 | ctx_60a86164b026b1c82887 | R13-1042 | (Hatzivassiloglou et al., 1999) | parenthetical_author_year | Hatzivassiloglou et al., 1999 | hatzivassiloglou | 1999 | unavailable | W99-0625 | Detecting Text Similarity over Short Passages: Exploring Linguistic Feature Combinations via Machine Learning | 1 | author_year_clear | 0.9 | 1999 ) uses pairs of words occurring in the same order for the two emails; Token Pair Distance (Hatzivassiloglou et al., 1999) measures t... |
| ctxr_2479d585508f63ab060b | ctx_1a5b77355c072a0fad2c | R13-1044 | (Rosario and Hearst, 2001) | parenthetical_author_year | Rosario and Hearst, 2001 | rosario;hearst | 2001 | unavailable | W01-0511 | Classifying the Semantic Relations in Noun Compounds via a Domain-Specific Lexical Hierarchy | 1 | author_year_clear | 0.95 | In (Rosario and Hearst, 2001) authors used neural networks to determine 20 semantic relationssimilarily to (Nastase et al., 2006) -betwee... |
| ctxr_6b3119f16cbb901d7fa9 | ctx_e77ed08bc72bff473396 | R13-1044 | (Tratz and Hovy, 2010) | parenthetical_author_year | Tratz and Hovy, 2010 | tratz;hovy | 2010 | unavailable | S10-1049 | {ISI}: Automatic Classification of Relations Between Nominals Using a Maximum Entropy Classifier | 1 | author_year_clear | 0.95 | In (Tratz and Hovy, 2010) the authors developed a system based on the Maximum Entropy classifier, able to detect 10 bidirectional semanti... |
| ctxr_a333b2856eb29293a4d1 | ctx_9bdb1387cc200719e735 | R13-1044 | (Rink and Harabagiu, 2010) | parenthetical_author_year | Rink and Harabagiu, 2010 | rink;harabagiu | 2010 | unavailable | S10-1057 | {UTD}: Classifying Semantic Relations by Combining Lexical and Semantic Resources | 1 | author_year_clear | 0.95 | The same set of semantic relations was used in (Rink and Harabagiu, 2010) . |
| ctxr_f4e1cc80ff80bc243634 | ctx_986f87d549660bd38028 | R13-1044 | (Tymoshenko and Giuliano, 2010 ) | parenthetical_author_year | Tymoshenko and Giuliano, 2010 | tymoshenko;giuliano | 2010 | unavailable | S10-1047 | {FBK}-{IRST}: Semantic Relation Extraction Using {C}yc | 1 | author_year_clear | 0.95 | Authors in (Tymoshenko and Giuliano, 2010 ) used shallow syntactic parsing and semantic information from ResearchCyc (Lenat, 1995) in the... |
| ctxr_43b1ba4d10cbc95c2230 | ctx_906e8bec7828fe5e4bf1 | R13-1044 | (Hearst, 1992) | parenthetical_author_year | Hearst, 1992 | hearst | 1992 | unavailable | C92-2082 | Automatic Acquisition of Hyponyms from Large Text Corpora | 1 | author_year_clear | 0.9 | In (Hearst, 1992) authors used set of manually written rules for identification of hyperonymy relations. (Ben Abacha and Zweigenbaum, 201... |
| ctxr_8abd632c34ecc38c0905 | ctx_0b022dfa768255504380 | R13-1044 | (Broda et al., 2012) | parenthetical_author_year | Broda et al., 2012 | broda | 2012 | unavailable | L12-1574 | {KPW}r: Towards a Free Corpus of {P}olish | 1 | author_year_clear | 0.9 | We made use of a CRF shallow parser (Radziszewski and Pawlaczek, 2012) trained on an annotated corpus of Polish (KPWr) (Broda et al., 201... |
| ctxr_f7a117679ae9451f73ac | ctx_2b3f9399bec9820f936d | R13-1044 | (Radziszewski et al., 2012) | parenthetical_author_year | Radziszewski et al., 2012 | radziszewski | 2012 | unavailable | L12-1574 | {KPW}r: Towards a Free Corpus of {P}olish | 1 | author_year_clear | 0.9 | We made use of a CRF shallow parser (Radziszewski and Pawlaczek, 2012) trained on an annotated corpus of Polish (KPWr) (Broda et al., 201... |
| ctxr_bdafc0e55cd457b92f18 | ctx_f2020e350a3cdeaa6d2a | R13-1044 | (Maziarz et al., 2012) | parenthetical_author_year | Maziarz et al., 2012 | maziarz | 2012 | unavailable | L12-1574 | {KPW}r: Towards a Free Corpus of {P}olish | 1 | author_year_clear | 0.9 | The operators are language-specific and utilize morphosyntactic features (POS, case, number and gender), domains of Polish WordNet lexica... |
| ctxr_88a18aac1e996ffd26c3 | ctx_9ac1e28cf348e55ace28 | W05-0818 | (Ayan et al., 2004; Och and Ney, 2000) | parenthetical_author_year | Ayan et al., 2004 | ayan | 2004 | unavailable | 2004.amta-papers.3 | Multi-Align: combining linguistic and statistical techniques to improve alignments for adaptable {MT} | 1 | author_year_clear | 0.9 | Introduction Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such ... |
| ctxr_f7b6a5b16e9ff0bebd24 | ctx_9ac1e28cf348e55ace28 | W05-0818 | (Ayan et al., 2004; Och and Ney, 2000) | parenthetical_author_year | Och and Ney, 2000 | och;ney | 2000 | unavailable | P00-1056 | Improved Statistical Alignment Models | 1 | author_year_clear | 0.95 | Introduction Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such ... |
| ctxr_441cbbb13e78fa1e16dd | ctx_fdc6755df3154c8dcd18 | W05-0818 | (Ayan et al., 2004; Och and Ney, 2000) | parenthetical_author_year | Ayan et al., 2004 | ayan | 2004 | unavailable | 2004.amta-papers.3 | Multi-Align: combining linguistic and statistical techniques to improve alignments for adaptable {MT} | 1 | author_year_clear | 0.9 | Introduction Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such ... |
| ctxr_8b932e2211789facdef8 | ctx_fdc6755df3154c8dcd18 | W05-0818 | (Ayan et al., 2004; Och and Ney, 2000) | parenthetical_author_year | Och and Ney, 2000 | och;ney | 2000 | unavailable | P00-1056 | Improved Statistical Alignment Models | 1 | author_year_clear | 0.95 | Introduction Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such ... |

## 20 Examples: multi_candidate_ambiguous
| context_id | source_context_id | citing_paper_id | citation_marker | marker_type | marker_component_text | parsed_surnames | parsed_year | parsed_year_suffix | resolved_cited_acl_id | resolved_cited_title | matched_candidate_count | resolution_status | resolution_confidence | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_240e2ca1ded99d01bf92 | ctx_e2408d24f1cf405125ab | W05-0820 | (Koehn, 2005) | parenthetical_author_year | Koehn, 2005 | koehn | 2005 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | We provided not only training data from the Europarl corpus (Koehn, 2005) , but also additional resources: sentence and word alignments, ... |
| ctxr_8c3ab01906c7d6360b39 | ctx_9d4e7b766d7ef29394e6 | W05-0820 | Koehn et al. (2003) | narrative_author_year | Koehn et al. (2003) | koehn | 2003 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | The focus of the task was to build a probabilistic phrase translation table, since most of the other resources were provided -for more on... |
| ctxr_997e31791c89cb29d091 | ctx_fff467db8f9d0e00bbe9 | W05-0820 | (Och, 2003) | parenthetical_author_year | Och, 2003 | och | 2003 | unavailable | unavailable |  | 3 | multi_candidate_ambiguous | 0.0 | However, the field is moving fast, and a number of steps help to improve upon the provided baseline setup, e.g., larger language models t... |
| ctxr_2f21bfd1f619816d1f37 | ctx_c7f05049d870d09a4883 | R13-1049 | Gandon (2013b) | narrative_author_year | Gandon (2013b) | gandon | 2013 | b | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Lefranc ¸ois and Gandon (2013b) therefore introduced a deeper level of representation to describe meanings: the deep semantic level, and ... |
| ctxr_4afd32597ce8f1566874 | ctx_09cf0273f979fe54f560 | R13-1049 | Gandon (2013a) | narrative_author_year | Gandon (2013a) | gandon | 2013 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Reasoning with UGs-Homomorphisms Lefranc ¸ois and Gandon (2013a) proposed to use the notion of UGs homomorphism to define this entailment... |
| ctxr_9c9eb9124477bd214101 | ctx_026b3e0967ee5174c966 | R13-1049 | Gandon (2013a) | narrative_author_year | Gandon (2013a) | gandon | 2013 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | More generally, Lefranc ¸ois and Gandon (2013a) listed a set of rules which defines the axiomatization of the UGs semantics. |
| ctxr_5aba7d7b099a18b5d8ff | ctx_215b1f20278ce7e94b57 | R13-1049 | Gandon (2013a) | narrative_author_year | Gandon (2013a) | gandon | 2013 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Lefranc ¸ois and Gandon (2013a) illustrated problematic cases where the closure is infinite for finite UGs. |
| ctxr_042910969671ab84ff98 | ctx_6bcace7d35adbf4208be | R13-1049 | Gandon (2013c) | narrative_author_year | Gandon (2013c) | gandon | 2013 | c | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | In order to deal with the problem of prohibited and optional ASlots, D contains a special element denoted • that represents nothing, plus... |
| ctxr_393cf914a2be7857dd68 | ctx_784ec7bf3e17a0940214 | 2009.mtsummit-posters.22 | (Abekawa and Kageura, 2007a) | parenthetical_author_year | Abekawa and Kageura, 2007a | abekawa;kageura | 2007 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | However, they lack proper translation support tools (Abekawa and Kageura, 2007a) . |
| ctxr_26823efe3f06257b1e6d | ctx_6e2230d16abb49d81184 | 2009.mtsummit-posters.22 | Abekawa and Kageura (2007a) | narrative_author_year | Abekawa and Kageura (2007a) | abekawa;kageura | 2007 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | 2 Hosting volunteer translators Abekawa and Kageura (2007a) have developed a translation aid editor, QRedit, which has been experimentall... |
| ctxr_04ac9ad149aa71dd0d7d | ctx_2aba43f51bfb4945fde8 | 2009.mtsummit-posters.22 | (Abekawa and Kageura, 2007a) | parenthetical_author_year | Abekawa and Kageura, 2007a | abekawa;kageura | 2007 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | This situation sharply contrasts to the usual situation of volunteer translators in which they do not use translation aid systems for a v... |
| ctxr_a5eb69e8ffee3688d4f4 | ctx_82fe83efa66b934c8594 | 2009.mtsummit-posters.22 | (Abekawa and Kageura, 2007a) | parenthetical_author_year | Abekawa and Kageura, 2007a | abekawa;kageura | 2007 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | 7 Translation aid editor: QRedit About QRedit QRedit is a translation aid system which is designed for volunteer translators working main... |
| ctxr_dd93d829eb2179c2f414 | ctx_352d0ad9b2ef24403d22 | 2009.mtsummit-posters.22 | (Abekawa and Kageura, 2007a) | parenthetical_author_year | Abekawa and Kageura, 2007a | abekawa;kageura | 2007 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | These requirements stem from the requests made by volunteer translators (Abekawa and Kageura, 2007a) . |
| ctxr_9c84c78f031d03d032c6 | ctx_6b1bc02e55b066ce81c9 | 2009.mtsummit-posters.22 | (Abekawa and Kageura, 2007b) | parenthetical_author_year | Abekawa and Kageura, 2007b | abekawa;kageura | 2007 | b | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | These levels are decided according to a four criteria: "composition," "difficulty," "specialty" and "resource type." See Figure 5 for an ... |
| ctxr_84631d046703191a1732 | ctx_03a39c4083f54c7e650b | R13-1052 | (Teufel et al., 2006a) | parenthetical_author_year | Teufel et al., 2006a | teufel | 2006 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Therefore, this task has attracted researchers from the fields of discourse analysis, sociology of science, and information sciences for ... |
| ctxr_70a1f949e595e067053d | ctx_da2274fcb5133b61c73a | R13-1052 | (Teufel et al., 2006a) | parenthetical_author_year | Teufel et al., 2006a | teufel | 2006 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Most of the existing research in this area focused on the analysis of citation sentiment, which has achieved good accuracy (see, e.g., (T... |
| ctxr_c4b798cbb21f43d00d0a | ctx_57924bea47f6bb335335 | R13-1052 | Teufel et al. (2006a) | narrative_author_year | Teufel et al. (2006a) | teufel | 2006 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Regarding the automatic recognition of citation functions or citation categories, Teufel et al. (2006a) presented a supervised learning f... |
| ctxr_b614b13920608fd45248 | ctx_b98cd13ca6a596debb64 | R13-1052 | Teufel et al. (2006a) | narrative_author_year | Teufel et al. (2006a) | teufel | 2006 | a | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | It is also worth noting that Teufel et al. (2006a) , Athar (2011) , and Dong and Schäfer (2011) all worked on citations in computational ... |
| ctxr_d320501a1e0f33d51ca0 | ctx_bf4afe06eeb309cb290b | W05-0824 | Koehn et al. (2003) | narrative_author_year | Koehn et al. (2003) | koehn | 2003 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | For acquiring a PBM, we followed the approach described by Koehn et al. (2003) . |
| ctxr_800f688d19becf0cdfbe | ctx_6f0542735039fb46a5a1 | W05-0824 | Koehn et al. (2003) | narrative_author_year | Koehn et al. (2003) | koehn | 2003 | unavailable | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | We did try to use the alignment produced with IBM model 4, but did not notice significant differences over our experiments; an observatio... |

## 20 Examples: unresolved markers
| context_id | source_context_id | citing_paper_id | citation_marker | marker_type | marker_component_text | parsed_surnames | parsed_year | parsed_year_suffix | resolved_cited_acl_id | resolved_cited_title | matched_candidate_count | resolution_status | resolution_confidence | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_c7f56a215cf89c1c157f | ctx_067ce962ce3e28d300dc | R13-1042 | (Aoki et al., 2003) | parenthetical_author_year | Aoki et al., 2003 | aoki | 2003 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_9892bd81329a91b0fc5f | ctx_caed847ef55be44e5728 | R13-1042 | (Yeh, 2006; Erera and Carmel, 2008) | parenthetical_author_year | Yeh, 2006 | yeh | 2006 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_bfab187112e5a2706773 | ctx_caed847ef55be44e5728 | R13-1042 | (Yeh, 2006; Erera and Carmel, 2008) | parenthetical_author_year | Erera and Carmel, 2008 | erera;carmel | 2008 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_308f45b8680249aa41c3 | ctx_84911bcb87933038f4ef | R13-1042 | (Yeh, 2006; Erera and Carmel, 2008) | parenthetical_author_year | Yeh, 2006 | yeh | 2006 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_9542cb6a30d0d899a0c7 | ctx_84911bcb87933038f4ef | R13-1042 | (Yeh, 2006; Erera and Carmel, 2008) | parenthetical_author_year | Erera and Carmel, 2008 | erera;carmel | 2008 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_ee8f8c85fa0fa72fc6ec | ctx_0654fb914da78fe27f64 | R13-1042 | Joti et al. (2010) | narrative_author_year | Joti et al. (2010) | joti | 2010 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Joti et al. (2010) used the BC3 corpus of 40 email threads and 3222 emails for topic segmentation. |
| ctxr_8ab7872bdf0a5a570079 | ctx_dfa13b651de4c8a38ac8 | R13-1042 | Wu and Oard (2005) | narrative_author_year | Wu and Oard (2005) | wu;oard | 2005 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Wu and Oard (2005) , and Zhu et al. (2005) auto-threaded all messages with identical, non-trivial, Fwd: and Re:-stripped Subject headers. |
| ctxr_672cb0e146a4869c354a | ctx_76bfce41e4c188115fe0 | R13-1042 | Zhu et al. (2005) | narrative_author_year | Zhu et al. (2005) | zhu | 2005 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Wu and Oard (2005) , and Zhu et al. (2005) auto-threaded all messages with identical, non-trivial, Fwd: and Re:-stripped Subject headers. |
| ctxr_1f86e324163888270ee2 | ctx_5316c651106c2cd46fe9 | R13-1042 | Klimt and Yang (2004) | narrative_author_year | Klimt and Yang (2004) | klimt;yang | 2004 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Klimt and Yang (2004) auto-threaded messages that had stripped Subject headers and were among the same users (addresses). |
| ctxr_c0b1eac52d206fb6cc0e | ctx_6def7a00a3f4ce76a5f2 | R13-1042 | Lewis and Knowles (1997) | narrative_author_year | Lewis and Knowles (1997) | lewis;knowles | 1997 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Lewis and Knowles (1997) assigned emails to threads by matching quotation structures between emails. |
| ctxr_c01c8e428740f7f3a146 | ctx_aebefe0b75286ed91920 | R13-1042 | Klimt and Yang (2004) | narrative_author_year | Klimt and Yang (2004) | klimt;yang | 2004 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | First, we implemented Klimt and Yang (2004) 's technique of clustering the emails into threads that have the same Subject header (after i... |
| ctxr_00f59d9ebc434c12882e | ctx_d7851e0e9cedd00716ca | R13-1042 | Klimt and Yang (2004) | narrative_author_year | Klimt and Yang (2004) | klimt;yang | 2004 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | In addition, many clusters consisted of all of the issues of a monthly subscription newsletter, or nearly identical petitions (see Klimt ... |
| ctxr_0350262fc52b0279814a | ctx_7326cac7c1759aa26da9 | R13-1042 | Klimt and Yang (2004) | narrative_author_year | Klimt and Yang (2004) | klimt;yang | 2004 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | In order to avoid creating redundant threads, which would be an information leak risk during evaluation, we selected as the thread source... |
| ctxr_a8aa7b3c306a76f44a2b | ctx_c0ca7e2fa6fe568cbcdb | R13-1042 | Yeh (2006) | narrative_author_year | Yeh (2006) | yeh | 2006 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | We used the quoteidentifying regular expressions from Yeh (2006) (see Table 1 ) to identify quoted previous emails. |
| ctxr_2dc67dfdace249fc9432 | ctx_705aee42cff2db25eec0 | R13-1042 | (2011) | year_only | 2011 |  | 2011 | unavailable | unavailable |  | 2 | ambiguous_year_only | 0.0 | We evaluate a number of text similarity measures, divided according to Bär et al. (2011) 's three groups: Content Similarity, Structural ... |
| ctxr_8d97b8e1e398fe226e22 | ctx_60ecb7ed462c462f850b | R13-1042 | (Gusfield, 1997) | parenthetical_author_year | Gusfield, 1997 | gusfield | 1997 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | The Longest Common Substring measure (Gusfield, 1997) identifies uninterrupted common strings, while the Longest Common Subsequence measu... |
| ctxr_3ded7f9bb06fc04571ae | ctx_f3cb4976b437f49ebf0f | R13-1042 | (Allison and Dix, 1986 ) | parenthetical_author_year | Allison and Dix, 1986 | allison;dix | 1986 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | The Longest Common Substring measure (Gusfield, 1997) identifies uninterrupted common strings, while the Longest Common Subsequence measu... |
| ctxr_5e3cedc400623ad26c1a | ctx_6f9a8263a7428098ef3a | R13-1042 | (Wise, 1996) | parenthetical_author_year | Wise, 1996 | wise | 1996 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | The Longest Common Substring measure (Gusfield, 1997) identifies uninterrupted common strings, while the Longest Common Subsequence measu... |
| ctxr_83ad668218de72ac03b5 | ctx_b6c21e9af1bf1db9c03d | R13-1042 | Levenshtein (1966) | narrative_author_year | Levenshtein (1966) | levenshtein | 1966 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Other measures which treat texts as sequences of characters and compute similarities with various metrics include Levenshtein (1966) , Mo... |
| ctxr_08ba5d105c0673d0158f | ctx_808e2c4ba31264e7687d | R13-1042 | (Monge and Elkan, 1997) | parenthetical_author_year | Monge and Elkan, 1997 | monge;elkan | 1997 | unavailable | unavailable |  | 0 | bibliography_unresolved | 0.0 | Other measures which treat texts as sequences of characters and compute similarities with various metrics include Levenshtein (1966) , Mo... |

## Common Failure Patterns
| resolution_status | resolution_method | rows |
| --- | --- | --- |
| bibliography_unresolved | author_year_no_candidate | 67538 |
| citing_paper_not_in_aligned_graph | no_candidate_graph_for_citing_paper | 9599 |
| numeric_marker_unresolved_no_bibliography | numeric_marker | 6612 |
| multi_candidate_ambiguous | author_year_multiple_candidates | 5913 |
| bibliography_unresolved | year_only_no_candidate | 927 |
| ambiguous_year_only | year_only_multiple_candidates | 820 |
| year_only_unique_candidate | year_only_unique_candidate | 539 |
| bibliography_unresolved | marker_parse_failed | 216 |
