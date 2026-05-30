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
| duplicate context_id count before | 4 |
| duplicate context_id count after | 0 |
| citing_paper_id coverage in aligned graph | 0.890 |
| author_year_clear rate | 0.339 |
| multi_candidate_ambiguous rate | 0.038 |
| ambiguous_year_only rate | 0.058 |
| numeric_marker_unresolved_no_bibliography rate | 0.044 |
| bibliography_unresolved rate | 0.427 |
| resolved_cited_title non-empty rate | 0.370 |

## Resolution Status Distribution
| status | rows |
| --- | --- |
| bibliography_unresolved | 64573 |
| author_year_clear | 51394 |
| citing_paper_not_in_aligned_graph | 9599 |
| ambiguous_year_only | 8763 |
| numeric_marker_unresolved_no_bibliography | 6612 |
| multi_candidate_ambiguous | 5780 |
| year_only_unique_candidate | 4680 |

## 20 Examples: author_year_clear
| context_id | source_context_id | citing_paper_id | citation_marker | marker_component_text | parsed_surnames | parsed_year | resolved_cited_acl_id | resolved_cited_title | matched_candidate_count | resolution_status | resolution_confidence | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_48e5a6cc7ce0e0ee8d77 | ctx_1b8dbeb14bcb86f7e95b | R13-1042 | (Elsner and Charniak, 2010) | Elsner and Charniak, 2010 | elsner | 2010 | J10-3004 | Disentangling Chat | 1 | author_year_clear | 0.9 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_92415600da27ead20c13 | ctx_f42ce1b3c4e973e9e519 | R13-1042 | (Hatzivassiloglou et al., 1999) | Hatzivassiloglou et al., 1999 | hatzivassiloglou | 1999 | W99-0625 | Detecting Text Similarity over Short Passages: Exploring Linguistic Feature Combinations via Machine Learning | 1 | author_year_clear | 0.9 | 1999 ) uses pairs of words occurring in the same order for the two emails; Token Pair Distance (Hatzivassiloglou et al., 1999) measures t... |
| ctxr_658e4fa9d9ae430ba17c | ctx_7df785a8a6c956ae8a95 | R13-1044 | (Rosario and Hearst, 2001) | Rosario and Hearst, 2001 | rosario | 2001 | W01-0511 | Classifying the Semantic Relations in Noun Compounds via a Domain-Specific Lexical Hierarchy | 1 | author_year_clear | 0.9 | In (Rosario and Hearst, 2001) authors used neural networks to determine 20 semantic relationssimilarily to (Nastase et al., 2006) -betwee... |
| ctxr_75483684663d1635361e | ctx_8623305e066a2aaf5daf | R13-1044 | (Tratz and Hovy, 2010) | Tratz and Hovy, 2010 | tratz | 2010 | S10-1049 | {ISI}: Automatic Classification of Relations Between Nominals Using a Maximum Entropy Classifier | 1 | author_year_clear | 0.9 | In (Tratz and Hovy, 2010) the authors developed a system based on the Maximum Entropy classifier, able to detect 10 bidirectional semanti... |
| ctxr_1dadc83745ef74eff655 | ctx_242e7310127ee186952b | R13-1044 | (Rink and Harabagiu, 2010) | Rink and Harabagiu, 2010 | rink | 2010 | S10-1057 | {UTD}: Classifying Semantic Relations by Combining Lexical and Semantic Resources | 1 | author_year_clear | 0.9 | The same set of semantic relations was used in (Rink and Harabagiu, 2010) . |
| ctxr_4293189d51473c3d209b | ctx_7432464e809a045d5448 | R13-1044 | (Tymoshenko and Giuliano, 2010 ) | Tymoshenko and Giuliano, 2010 | tymoshenko | 2010 | S10-1047 | {FBK}-{IRST}: Semantic Relation Extraction Using {C}yc | 1 | author_year_clear | 0.9 | Authors in (Tymoshenko and Giuliano, 2010 ) used shallow syntactic parsing and semantic information from ResearchCyc (Lenat, 1995) in the... |
| ctxr_ecd0da6273a15797ab90 | ctx_76aab29e37e064b31f36 | R13-1044 | (Hearst, 1992) | Hearst, 1992 | hearst | 1992 | C92-2082 | Automatic Acquisition of Hyponyms from Large Text Corpora | 1 | author_year_clear | 0.9 | In (Hearst, 1992) authors used set of manually written rules for identification of hyperonymy relations. (Ben Abacha and Zweigenbaum, 201... |
| ctxr_0ad64c0e68fffdd961d1 | ctx_d526ea8e7eb6d2cf6d90 | R13-1044 | (Radziszewski and Pawlaczek, 2012) | Radziszewski and Pawlaczek, 2012 | radziszewski | 2012 | L12-1574 | {KPW}r: Towards a Free Corpus of {P}olish | 1 | author_year_clear | 0.9 | We made use of a CRF shallow parser (Radziszewski and Pawlaczek, 2012) trained on an annotated corpus of Polish (KPWr) (Broda et al., 201... |
| ctxr_6e46f8a950fdb3459b70 | ctx_5d9885b63ccfa9770c6e | R13-1044 | (Broda et al., 2012) | Broda et al., 2012 | broda | 2012 | L12-1574 | {KPW}r: Towards a Free Corpus of {P}olish | 1 | author_year_clear | 0.9 | We made use of a CRF shallow parser (Radziszewski and Pawlaczek, 2012) trained on an annotated corpus of Polish (KPWr) (Broda et al., 201... |
| ctxr_6ce0bb8783b7310cf360 | ctx_98c664380373bf6e1901 | R13-1044 | (Radziszewski et al., 2012) | Radziszewski et al., 2012 | radziszewski | 2012 | L12-1574 | {KPW}r: Towards a Free Corpus of {P}olish | 1 | author_year_clear | 0.9 | We made use of a CRF shallow parser (Radziszewski and Pawlaczek, 2012) trained on an annotated corpus of Polish (KPWr) (Broda et al., 201... |
| ctxr_9dfc9d032258b81cfb48 | ctx_3af26583905232b00b29 | R13-1044 | (Radziszewski and Pawlaczek, 2012) | Radziszewski and Pawlaczek, 2012 | radziszewski | 2012 | L12-1574 | {KPW}r: Towards a Free Corpus of {P}olish | 1 | author_year_clear | 0.9 | Parsing rules make use of an output from the CRF shallow parser (Radziszewski and Pawlaczek, 2012) , in particular: borders of whole NPs/... |
| ctxr_163abaeb95f7b29010ec | ctx_5bf9425ded80e8740d7a | R13-1044 | (Maziarz et al., 2012) | Maziarz et al., 2012 | maziarz | 2012 | L12-1574 | {KPW}r: Towards a Free Corpus of {P}olish | 1 | author_year_clear | 0.9 | The operators are language-specific and utilize morphosyntactic features (POS, case, number and gender), domains of Polish WordNet lexica... |
| ctxr_12dcf61b4bf1374b359f | ctx_36bb41d2a77b280d9109 | W05-0818 | (Ayan et al., 2004; Och and Ney, 2000) | Ayan et al., 2004 | ayan | 2004 | 2004.amta-papers.3 | Multi-Align: combining linguistic and statistical techniques to improve alignments for adaptable {MT} | 1 | author_year_clear | 0.9 | Introduction Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such ... |
| ctxr_7a96da2de417e5a00620 | ctx_36bb41d2a77b280d9109 | W05-0818 | (Ayan et al., 2004; Och and Ney, 2000) | Och and Ney, 2000 | och | 2000 | P00-1056 | Improved Statistical Alignment Models | 1 | author_year_clear | 0.9 | Introduction Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such ... |
| ctxr_d80c2745bc71f571e610 | ctx_b8504710f93ec4dbb070 | W05-0818 | (Ayan et al., 2004; Och and Ney, 2000) | Ayan et al., 2004 | ayan | 2004 | 2004.amta-papers.3 | Multi-Align: combining linguistic and statistical techniques to improve alignments for adaptable {MT} | 1 | author_year_clear | 0.9 | Introduction Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such ... |
| ctxr_24770a889864d5df6a1d | ctx_b8504710f93ec4dbb070 | W05-0818 | (Ayan et al., 2004; Och and Ney, 2000) | Och and Ney, 2000 | och | 2000 | P00-1056 | Improved Statistical Alignment Models | 1 | author_year_clear | 0.9 | Introduction Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such ... |
| ctxr_3f0ef65ed71928f97d83 | ctx_71b60b97b259412faebf | W05-0818 | (Carl, 2001; Menezes and Richardson, 2001) | Carl, 2001 | carl | 2001 | W01-0718 | Inducing probabilistic invertible translation grammars from aligned texts | 1 | author_year_clear | 0.9 | Introduction Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such ... |
| ctxr_d8ce50bf0cdf279c3526 | ctx_71b60b97b259412faebf | W05-0818 | (Carl, 2001; Menezes and Richardson, 2001) | Menezes and Richardson, 2001 | menezes | 2001 | W01-1406 | A best-first alignment algorithm for automatic extraction of transfer mappings from bilingual corpora | 1 | author_year_clear | 0.9 | Introduction Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such ... |
| ctxr_a62b54c8998349ce459b | ctx_34c622c6247ca0a429b3 | W05-0818 | (Carl, 2001; Menezes and Richardson, 2001) | Carl, 2001 | carl | 2001 | W01-0718 | Inducing probabilistic invertible translation grammars from aligned texts | 1 | author_year_clear | 0.9 | Introduction Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such ... |
| ctxr_b9ae3a03c73b4704f556 | ctx_34c622c6247ca0a429b3 | W05-0818 | (Carl, 2001; Menezes and Richardson, 2001) | Menezes and Richardson, 2001 | menezes | 2001 | W01-1406 | A best-first alignment algorithm for automatic extraction of transfer mappings from bilingual corpora | 1 | author_year_clear | 0.9 | Introduction Alignment of words and multiword units plays an important role in many natural language processing (NLP) applications, such ... |

## 20 Examples: multi_candidate_ambiguous
| context_id | source_context_id | citing_paper_id | citation_marker | marker_component_text | parsed_surnames | parsed_year | resolved_cited_acl_id | resolved_cited_title | matched_candidate_count | resolution_status | resolution_confidence | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_74aed5cdbc383ae000e6 | ctx_3519dbdd8a7066d06708 | W05-0820 | (Koehn, 2005) | Koehn, 2005 | koehn | 2005 | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | We provided not only training data from the Europarl corpus (Koehn, 2005) , but also additional resources: sentence and word alignments, ... |
| ctxr_53350e9d45c94e67afee | ctx_dc196b097506a7864234 | W05-0820 | (Och and Ney, 2003) | Och and Ney, 2003 | och | 2003 | unavailable |  | 3 | multi_candidate_ambiguous | 0.0 | The field of statistical machine translation has been blessed with a long tradition of freely available software tools -such as GIZA++ (O... |
| ctxr_e0edb2a0cbaba0d30233 | ctx_b974a0d3406a8321667e | W05-0820 | (Koehn and Knight, 2003) | Koehn and Knight, 2003 | koehn | 2003 | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | However, the field is moving fast, and a number of steps help to improve upon the provided baseline setup, e.g., larger language models t... |
| ctxr_8ef70f688bc41e3c0a49 | ctx_e421976d8ead09177e82 | W05-0820 | (Och, 2003) | Och, 2003 | och | 2003 | unavailable |  | 3 | multi_candidate_ambiguous | 0.0 | However, the field is moving fast, and a number of steps help to improve upon the provided baseline setup, e.g., larger language models t... |
| ctxr_cbcb7e51e5c43938cfba | ctx_189446524eb9dbb3c7ff | 2009.mtsummit-posters.22 | (Abekawa and Kageura, 2007a) | Abekawa and Kageura, 2007a | abekawa | 2007 | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | However, they lack proper translation support tools (Abekawa and Kageura, 2007a) . |
| ctxr_5d94daa0612e262e1e07 | ctx_28fbe9b21f434d3df47c | 2009.mtsummit-posters.22 | (Abekawa and Kageura, 2007a) | Abekawa and Kageura, 2007a | abekawa | 2007 | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | This situation sharply contrasts to the usual situation of volunteer translators in which they do not use translation aid systems for a v... |
| ctxr_34dc69641fdd3ea78417 | ctx_72e2c4175b589f4bd1ca | 2009.mtsummit-posters.22 | (Abekawa and Kageura, 2007a) | Abekawa and Kageura, 2007a | abekawa | 2007 | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | 7 Translation aid editor: QRedit About QRedit QRedit is a translation aid system which is designed for volunteer translators working main... |
| ctxr_c018106fb1cc4830642b | ctx_e385cb55721b59caae99 | 2009.mtsummit-posters.22 | (Abekawa and Kageura, 2007a) | Abekawa and Kageura, 2007a | abekawa | 2007 | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | These requirements stem from the requests made by volunteer translators (Abekawa and Kageura, 2007a) . |
| ctxr_a61abcad52455a847399 | ctx_45f1b0e5ab0085705552 | 2009.mtsummit-posters.22 | (Abekawa and Kageura, 2007b) | Abekawa and Kageura, 2007b | abekawa | 2007 | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | These levels are decided according to a four criteria: "composition," "difficulty," "specialty" and "resource type." See Figure 5 for an ... |
| ctxr_8df2ec30dd7bd650f280 | ctx_7c677b9bd3b605a172de | R13-1052 | (Teufel et al., 2006a) | Teufel et al., 2006a | teufel | 2006 | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Therefore, this task has attracted researchers from the fields of discourse analysis, sociology of science, and information sciences for ... |
| ctxr_9e4830f20a7eb704e546 | ctx_ac64060aea4d0183eeca | R13-1052 | (Teufel et al., 2006a) | Teufel et al., 2006a | teufel | 2006 | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Most of the existing research in this area focused on the analysis of citation sentiment, which has achieved good accuracy (see, e.g., (T... |
| ctxr_a680e58a3bd496a1e05e | ctx_b246d796b4738827466a | W16-4705 | (Grefenstette, 1999; Tonoike et al., 2005; Tonoike et al., 2006; Daille and Morin, 2008) | Tonoike et al., 2006 | tonoike | 2006 | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Some use the correspondence at the level of constituent elements of terms in finding term translations (Grefenstette, 1999; Tonoike et al... |
| ctxr_0d6170184e022528e018 | ctx_7d2af6113e01259227ca | W16-4705 | (Grefenstette, 1999; Tonoike et al., 2005; Tonoike et al., 2006; Daille and Morin, 2008) | Tonoike et al., 2006 | tonoike | 2006 | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Some use the correspondence at the level of constituent elements of terms in finding term translations (Grefenstette, 1999; Tonoike et al... |
| ctxr_3331742ae4e96c84f8cf | ctx_18004f296593b8a95cf9 | W16-4705 | (Grefenstette, 1999; Tonoike et al., 2005; Tonoike et al., 2006; Daille and Morin, 2008) | Tonoike et al., 2006 | tonoike | 2006 | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Some use the correspondence at the level of constituent elements of terms in finding term translations (Grefenstette, 1999; Tonoike et al... |
| ctxr_8acd23502771e2ee15ef | ctx_d9d6772168ca80cbaea7 | W16-4705 | (Grefenstette, 1999; Tonoike et al., 2005; Tonoike et al., 2006; Daille and Morin, 2008) | Tonoike et al., 2006 | tonoike | 2006 | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | Some use the correspondence at the level of constituent elements of terms in finding term translations (Grefenstette, 1999; Tonoike et al... |
| ctxr_1e02ec08dc305d826513 | ctx_74178a79bfab65fd0918 | 2009.mtsummit-posters.17 | (Zhao et al., 2004; Koehn and Schroeder, 2007) | Koehn and Schroeder, 2007 | koehn | 2007 | unavailable |  | 3 | multi_candidate_ambiguous | 0.0 | This was investigated in the framework of SMT by several authors, for instance for word alignment (Civera and Juan, 2007) , for language ... |
| ctxr_f6f31d0640a2c300fe62 | ctx_b09544809d3775ecdaf7 | 2009.mtsummit-posters.17 | (Zhao et al., 2004; Koehn and Schroeder, 2007) | Koehn and Schroeder, 2007 | koehn | 2007 | unavailable |  | 3 | multi_candidate_ambiguous | 0.0 | This was investigated in the framework of SMT by several authors, for instance for word alignment (Civera and Juan, 2007) , for language ... |
| ctxr_0d48a4ba29e51cb2b205 | ctx_2d4b2acaef3ca8f434f4 | 2009.mtsummit-posters.17 | (Callison-Burch et al., 2007; Callison-Burch et al., 2008) | Callison-Burch et al., 2007 | callison | 2007 | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | 3 This data source is already used to build SMT systems to translate between European languages, in particular in the framework of the ev... |
| ctxr_02991aed0ed0060b6509 | ctx_1e97006da0be2e91e63f | 2009.mtsummit-posters.17 | (Callison-Burch et al., 2007; Callison-Burch et al., 2008) | Callison-Burch et al., 2007 | callison | 2007 | unavailable |  | 2 | multi_candidate_ambiguous | 0.0 | 3 This data source is already used to build SMT systems to translate between European languages, in particular in the framework of the ev... |
| ctxr_2fc0f2038a3d319e066b | ctx_fbcf1a7ce8630ecf3df4 | 2009.mtsummit-posters.17 | (Koehn et al., 2007) | Koehn et al., 2007 | koehn | 2007 | unavailable |  | 3 | multi_candidate_ambiguous | 0.0 | We are only aware of one other large Arabic/French news translation system, the one that was developed during the TRAMES project (Hasan a... |

## 20 Examples: unresolved markers
| context_id | source_context_id | citing_paper_id | citation_marker | marker_component_text | parsed_surnames | parsed_year | resolved_cited_acl_id | resolved_cited_title | matched_candidate_count | resolution_status | resolution_confidence | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctxr_df219f521781ca10e9a9 | ctx_49cf24ac775d09eb1025 | R13-1042 | (2010) | 2010 |  | 2010 | unavailable |  | 2 | ambiguous_year_only | 0.0 | In NLP, Elsner and Charniak (2010) described the task of thread disentanglement as "the clustering task of dividing a transcript into a s... |
| ctxr_e4bef603dc9fc251691f | ctx_7098ddac36c149ad6c4f | R13-1042 | (Aoki et al., 2003) | Aoki et al., 2003 | aoki | 2003 | unavailable |  | 0 | bibliography_unresolved | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_2c03720e257491560239 | ctx_d92aaae0a320f5b57d2b | R13-1042 | (Yeh, 2006; Erera and Carmel, 2008) | Yeh, 2006 | yeh | 2006 | unavailable |  | 0 | bibliography_unresolved | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_ca7736eef4bade23c386 | ctx_d92aaae0a320f5b57d2b | R13-1042 | (Yeh, 2006; Erera and Carmel, 2008) | Erera and Carmel, 2008 | erera | 2008 | unavailable |  | 0 | bibliography_unresolved | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_d9d52169c570a9aa21e3 | ctx_1644879268ac4613e866 | R13-1042 | (Yeh, 2006; Erera and Carmel, 2008) | Yeh, 2006 | yeh | 2006 | unavailable |  | 0 | bibliography_unresolved | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_af6c5f1168ea2d6b4119 | ctx_1644879268ac4613e866 | R13-1042 | (Yeh, 2006; Erera and Carmel, 2008) | Erera and Carmel, 2008 | erera | 2008 | unavailable |  | 0 | bibliography_unresolved | 0.0 | Research on disentanglement of conversation threads has been done on internet relay chats (Elsner and Charniak, 2010) , audio chats (Aoki... |
| ctxr_d1a5f9b6430d05997606 | ctx_d76dde89813c8f48ed46 | R13-1042 | (2010) | 2010 |  | 2010 | unavailable |  | 2 | ambiguous_year_only | 0.0 | Joti et al. (2010) used the BC3 corpus of 40 email threads and 3222 emails for topic segmentation. |
| ctxr_10bc7351f828d60f8060 | ctx_c00c937fc4e5efc32b5b | R13-1042 | (2004) | 2004 |  | 2004 | unavailable |  | 2 | ambiguous_year_only | 0.0 | Wan and McKeown (2004) used a privatelyavailable corpus of 300 threads for summary generation. |
| ctxr_1febe329c8e7f2e1cbf9 | ctx_6cff1d6fcaede47b691f | R13-1042 | (2004) | 2004 |  | 2004 | unavailable |  | 2 | ambiguous_year_only | 0.0 | Rambow et al. (2004) used a privatelyavailable corpus of 96 email threads for thread summarization. |
| ctxr_18c98f3ddb5b8cf0c037 | ctx_28b3c707e054f0d54e0f | R13-1042 | (2005) | 2005 |  | 2005 | unavailable |  | 0 | bibliography_unresolved | 0.0 | Wu and Oard (2005) , and Zhu et al. (2005) auto-threaded all messages with identical, non-trivial, Fwd: and Re:-stripped Subject headers. |
| ctxr_87bfced7bc33accb9df2 | ctx_922fddecc7dd1ca7ca20 | R13-1042 | (2005) | 2005 |  | 2005 | unavailable |  | 0 | bibliography_unresolved | 0.0 | Wu and Oard (2005) , and Zhu et al. (2005) auto-threaded all messages with identical, non-trivial, Fwd: and Re:-stripped Subject headers. |
| ctxr_8df0e4a194d230c3c6ea | ctx_12de59cea39d76e21607 | R13-1042 | (2004) | 2004 |  | 2004 | unavailable |  | 2 | ambiguous_year_only | 0.0 | Klimt and Yang (2004) auto-threaded messages that had stripped Subject headers and were among the same users (addresses). |
| ctxr_d5ea94206e0c55d19bfc | ctx_45df5f192a5ae3798599 | R13-1042 | (1997) | 1997 |  | 1997 | unavailable |  | 0 | bibliography_unresolved | 0.0 | Lewis and Knowles (1997) assigned emails to threads by matching quotation structures between emails. |
| ctxr_a9af3d3da87b9e777367 | ctx_7dff41f01b98fa4473e2 | R13-1042 | (2004) | 2004 |  | 2004 | unavailable |  | 2 | ambiguous_year_only | 0.0 | Wan and McKeown (2004) reconstructed threads by header Message-ID information. |
| ctxr_6f4791edce6cadc207bd | ctx_c6958263c9adf95a7660 | R13-1042 | (2004) | 2004 |  | 2004 | unavailable |  | 2 | ambiguous_year_only | 0.0 | Rambow et al. (2004) used a privately-available corpus of 96 email threads, but did not specify how they determined the threads. |
| ctxr_e1c6ca6e000b0636a2c7 | ctx_7775eec7f7b3b27cb67f | R13-1042 | (2004) | 2004 |  | 2004 | unavailable |  | 2 | ambiguous_year_only | 0.0 | First, we implemented Klimt and Yang (2004) 's technique of clustering the emails into threads that have the same Subject header (after i... |
| ctxr_31160ed3781ca3051211 | ctx_e1d8a6a3a2df9db0c256 | R13-1042 | (2004) | 2004 |  | 2004 | unavailable |  | 2 | ambiguous_year_only | 0.0 | In addition, many clusters consisted of all of the issues of a monthly subscription newsletter, or nearly identical petitions (see Klimt ... |
| ctxr_a0997d9d5ce5178b007a | ctx_ad3875e1f850cc709f7d | R13-1042 | (2004) | 2004 |  | 2004 | unavailable |  | 2 | ambiguous_year_only | 0.0 | In order to avoid creating redundant threads, which would be an information leak risk during evaluation, we selected as the thread source... |
| ctxr_dafe573d8540a5139b3c | ctx_2c880ccdcfe1a936c590 | R13-1042 | (2006) | 2006 |  | 2006 | unavailable |  | 0 | bibliography_unresolved | 0.0 | We used the quoteidentifying regular expressions from Yeh (2006) (see Table 1 ) to identify quoted previous emails. |
| ctxr_3ab33b33bebcda204086 | ctx_aca4a6d15999787c7341 | R13-1042 | (2011) | 2011 |  | 2011 | unavailable |  | 2 | ambiguous_year_only | 0.0 | We evaluate a number of text similarity measures, divided according to Bär et al. (2011) 's three groups: Content Similarity, Structural ... |

## Common Failure Patterns
| resolution_status | resolution_method | rows |
| --- | --- | --- |
| bibliography_unresolved | author_year_no_candidate | 59685 |
| citing_paper_not_in_aligned_graph | no_candidate_graph_for_citing_paper | 9599 |
| ambiguous_year_only | year_only_multiple_candidates | 8763 |
| numeric_marker_unresolved_no_bibliography | numeric_marker | 6612 |
| multi_candidate_ambiguous | author_year_multiple_candidates | 5780 |
| year_only_unique_candidate | year_only_unique_candidate | 4680 |
| bibliography_unresolved | year_only_no_candidate | 4672 |
| bibliography_unresolved | marker_parse_failed | 216 |
