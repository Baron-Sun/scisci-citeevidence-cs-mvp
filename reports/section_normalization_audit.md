# Section Normalization Audit

## Inputs / Outputs
| name | path | rows |
| --- | --- | --- |
| input | data/interim/acl_sections_sectioned.parquet | 3240481 |
| normalized_sections | data/interim/acl_sections_sectioned_normalized.parquet | 3240481 |

## Core Metrics
| metric | value |
| --- | --- |
| section_name non-empty rate | 0.948 |
| unknown rate before | 0.610 |
| unknown rate after | 0.526 |

## Normalized Section Distribution Before
| normalized_section | paragraph_rows |
| --- | --- |
| unknown | 1977096 |
| introduction | 308365 |
| model | 163291 |
| results | 132730 |
| conclusion | 115095 |
| method | 114716 |
| experiment | 109192 |
| related_work | 88770 |
| evaluation | 83736 |
| abstract | 66857 |
| discussion | 40893 |
| background | 25769 |
| references | 10260 |
| appendix | 3711 |

## Normalized Section Distribution After
| normalized_section | paragraph_rows |
| --- | --- |
| unknown | 1703158 |
| introduction | 308365 |
| dataset | 171304 |
| model | 160387 |
| method | 128407 |
| conclusion | 116596 |
| experiment | 103964 |
| related_work | 89626 |
| evaluation | 89532 |
| results | 81265 |
| abstract | 66857 |
| discussion | 43797 |
| analysis | 42825 |
| acknowledgement | 38188 |
| background | 35097 |
| task_definition | 13557 |
| implementation | 12760 |
| references | 9650 |
| error_analysis | 8873 |
| appendix | 8336 |
| system_description | 7937 |

## Top 300 Raw Section Names Mapped To Unknown Before
| section_name | paragraph_rows |
| --- | --- |
| <empty> | 167546 |
| Acknowledgments | 18667 |
| Acknowledgements | 13095 |
| Data | 11571 |
| Features | 7663 |
| Datasets | 6854 |
| Baselines | 6190 |
| Dataset | 5984 |
| Training | 5711 |
| annex | 4146 |
| Motivation | 3669 |
| 2. | 2956 |
| Implementation | 2933 |
| Problem Formulation | 2571 |
| Ablation Study | 2518 |
| Implementation Details | 2404 |
| Preprocessing | 2384 |
| Inference | 2365 |
| Corpus | 2312 |
| Acknowledgement | 2210 |
| 2 | 2143 |
| System Description | 2015 |
| 4. | 1938 |
| acknowledgement | 1891 |
| Data Collection | 1861 |
| Learning | 1843 |
| 3 | 1810 |
| System | 1778 |
| Problem Definition | 1749 |
| • | 1693 |
| Annotation | 1692 |
| 5 | 1582 |
| Task Definition | 1566 |
| Baseline | 1555 |
| 3. | 1548 |
| Metrics | 1516 |
| 4 | 1473 |
| Case Study | 1453 |
| Task Description | 1431 |
| Settings | 1401 |
| Decoder | 1398 |
| Corpora | 1393 |
| Decoding | 1349 |
| 5. | 1344 |
| 1 | 1256 |
| Definitions | 1233 |
| 1. | 1161 |
| Proof | 1161 |
| Neural Machine Translation | 1147 |
| Ethical Considerations | 1136 |
| Figure 1 | 1122 |
| Encoder | 1112 |
| Feature Extraction | 1093 |
| Parameter Estimation | 1078 |
| Concluding Remarks | 1071 |
| Data Preparation | 1053 |
| Problem Statement | 1046 |
| Definition | 1035 |
| Example | 1028 |
| Figure 2 | 1028 |
| Classification | 1027 |
| 6 | 991 |
| Figure 3 | 983 |
| Examples | 914 |
| Systems | 910 |
| Acknowledgment | 873 |
| Notation | 865 |
| Procedure | 863 |
| Training Details | 858 |
| Parsing | 789 |
| Optimization | 788 |
| Feature Selection | 770 |
| Task | 769 |
| Framework | 768 |
| Data Sets | 763 |
| Description | 736 |
| Pre-processing | 720 |
| Résultats | 703 |
| Training Data | 690 |
| 5: | 679 |
| Data Preprocessing | 679 |
| Machine Translation | 678 |
| Participants | 672 |
| Resources | 666 |
| Conditional Random Fields | 658 |
| Figure 4 | 655 |
| Figure 6 | 648 |
| Tasks | 633 |
| Context | 631 |
| Figure 5 | 612 |
| Data Set | 596 |
| Source | 584 |
| Annotation Process | 579 |
| Applications | 578 |
| Training Objective | 574 |
| System description | 569 |
| Setting | 569 |
| Figure 7 | 566 |
| Data Augmentation | 564 |
| Training and Inference | 555 |
| Remerciements | 553 |
| Clustering | 553 |
| Materials | 551 |
| Related Research | 543 |
| Baseline System | 532 |
| Data collection | 531 |
| An Example | 527 |
| Graph Construction | 518 |
| Ablation Studies | 498 |
| A Appendices | 495 |
| Dependency Parsing | 492 |
| Constraints | 490 |
| Concluding remarks | 482 |
| 4: | 480 |
| Contributions | 478 |
| Task Formulation | 478 |
| Baseline Systems | 476 |
| Alignment | 472 |
| Performance | 469 |
| Data Annotation | 465 |
| Word Embeddings | 464 |
| Annotation Guidelines | 459 |
| Classifiers | 455 |
| Annotation Scheme | 453 |
| Challenges | 450 |
| Dataset Construction | 447 |
| Example 1 | 447 |
| Data Description | 443 |
| Generation | 439 |
| Objective Function | 436 |
| Implementation details | 434 |
| Segmentation | 429 |
| Feature Engineering | 428 |
| Scoring | 427 |
| Adversarial Training | 423 |
| Sentence | 420 |
| Classifier | 415 |
| Loss Function | 415 |
| Inter-Annotator Agreement | 415 |
| Input: | 408 |
| English | 408 |
| Syntax | 406 |
| Comparison | 406 |
| Named Entity Recognition | 405 |
| 7. | 400 |
| Input | 400 |
| Domain Adaptation | 398 |
| Representation | 397 |
| Formulation | 396 |
| Combinatory Categorial Grammar | 396 |
| Overall Performance | 396 |
| Observations | 395 |
| 7 | 395 |
| Search | 393 |
| Translation | 385 |
| Support Vector Machines | 383 |
| Figure 10 | 379 |
| BERT | 374 |
| Hyperparameters | 373 |
| Training Procedure | 369 |
| Figure 8 | 364 |
| Normalization | 363 |
| The Corpus | 361 |
| Example 2 | 358 |
| Design | 356 |
| Figure 9 | 355 |
| Reinforcement Learning | 354 |
| The Problem | 354 |
| I | 354 |
| Language | 351 |
| Post-processing | 345 |
| Future Directions | 344 |
| 6: | 343 |
| . | 342 |
| Relation Extraction | 339 |
| Problem Description | 337 |
| 6. | 336 |
| Feature extraction | 334 |
| Dataset Description | 334 |
| Feature Set | 333 |
| Prediction | 331 |
| The Data | 327 |
| Statistical Machine Translation | 321 |
| Category | 321 |
| Data sets | 319 |
| État de l'art | 316 |
| Syntactic Features | 315 |
| Visualization | 314 |
| 3.1 | 309 |
| Type | 308 |
| Data preparation | 308 |
| Data Pre-processing | 307 |
| Parser | 305 |
| Accuracy | 304 |
| Word Alignment | 304 |
| 7: | 303 |
| Lexical Features | 302 |
| Problem Setting | 301 |
| Terminology | 299 |
| Data set | 297 |
| Feature selection | 296 |
| Figure 12 | 296 |
| Feature | 295 |
| System Combination | 294 |
| Word Sense Disambiguation | 293 |
| 2.1 | 291 |
| Research Questions | 290 |
| Évaluation | 290 |
| Transformer | 287 |
| Task description | 284 |
| Hypotheses | 281 |
| Smoothing | 279 |
| Morphology | 278 |
| Ethics Statement | 278 |
| Sentiment Classification | 278 |
| Semantics | 277 |
| Lexicon | 276 |
| Disambiguation | 274 |
| An example | 274 |
| Candidate Generation | 273 |
| Application | 271 |
| Submissions | 270 |
| Word | 269 |
| Basic Idea | 268 |
| Rules | 268 |
| Outline | 267 |
| Parameters | 267 |
| Active Learning | 266 |
| Tokenization | 265 |
| Test Data | 264 |
| User Interface | 264 |
| Training data | 262 |
| Knowledge Distillation | 260 |
| Input Representation | 259 |
| Figure 11 | 259 |
| Filtering | 259 |
| Pre-training | 258 |
| Linguistic Features | 258 |
| Attention | 258 |
| Generator | 257 |
| Properties | 256 |
| - | 255 |
| Metric | 254 |
| Semantic Role Labeling | 253 |
| Corpus Description | 252 |
| Statistics | 251 |
| Corpus Annotation | 251 |
| Motivations | 249 |
| Ensemble | 248 |
| Sentence Encoder | 248 |
| Learning and Inference | 248 |
| Parameter estimation | 247 |
| 2.2 | 246 |
| Measures | 245 |
| Corpus Construction | 245 |
| Rule Extraction | 245 |
| Inter-annotator agreement | 244 |
| Objectives | 244 |
| Example 3 | 244 |
| Corpus Statistics | 243 |
| Performance Comparison | 243 |
| 3.2 | 241 |
| Feature Representation | 241 |
| 10: | 240 |
| Fine-tuning | 240 |
| Data Processing | 240 |
| Data and Preprocessing | 240 |
| Complexity | 238 |
| Data Sources | 237 |
| 8 | 236 |
| Baseline systems | 236 |
| Annotation Procedure | 235 |
| Dataset Creation | 235 |
| ) | 235 |
| Notations | 234 |
| Data preprocessing | 232 |
| Annotations | 232 |
| Pruning | 232 |
| Inter-annotator Agreement | 231 |
| (a) | 230 |
| Class | 230 |
| Formalization | 230 |
| Annotation scheme | 228 |
| (4) | 227 |
| Grammar | 227 |
| Natural Language Inference | 226 |
| ACKNOWLEDGEMENTS | 226 |
| Ranking | 224 |
| Joint Training | 223 |
| PLANS FOR THE COMING YEAR | 222 |
| 2.3 | 222 |
| Sentence Selection | 222 |
| Question Answering | 221 |
| Similarity Measures | 221 |
| Task definition | 220 |
| Tools | 219 |
| Efficiency | 218 |
| Word Similarity | 217 |
| Correctness | 216 |
| Multi-task Learning | 216 |

## Top 300 Raw Section Names Mapped To Unknown After
| section_name | paragraph_rows |
| --- | --- |
| <empty> | 167546 |
| Features | 7663 |
| Baselines | 6190 |
| Training | 5711 |
| 2. | 2956 |
| Inference | 2365 |
| 2 | 2143 |
| 4. | 1938 |
| Learning | 1843 |
| 3 | 1810 |
| • | 1693 |
| 5 | 1582 |
| Baseline | 1555 |
| 3. | 1548 |
| 4 | 1473 |
| Case Study | 1453 |
| Settings | 1401 |
| Decoder | 1398 |
| Decoding | 1349 |
| 5. | 1344 |
| 1 | 1256 |
| 1. | 1161 |
| Proof | 1161 |
| Neural Machine Translation | 1147 |
| Figure 1 | 1122 |
| Encoder | 1112 |
| Example | 1028 |
| Figure 2 | 1028 |
| Classification | 1027 |
| 6 | 991 |
| Figure 3 | 983 |
| Examples | 914 |
| Procedure | 863 |
| Training Details | 858 |
| Parsing | 789 |
| Framework | 768 |
| Description | 736 |
| Pre-processing | 720 |
| 5: | 679 |
| Machine Translation | 678 |
| Participants | 672 |
| Conditional Random Fields | 658 |
| Figure 4 | 655 |
| Figure 6 | 648 |
| Context | 631 |
| Figure 5 | 612 |
| Source | 584 |
| Applications | 578 |
| Training Objective | 574 |
| Setting | 569 |
| Figure 7 | 566 |
| Training and Inference | 555 |
| Clustering | 553 |
| Materials | 551 |
| An Example | 527 |
| Graph Construction | 518 |
| Dependency Parsing | 492 |
| Constraints | 490 |
| 4: | 480 |
| Contributions | 478 |
| Alignment | 472 |
| Performance | 469 |
| Word Embeddings | 464 |
| Classifiers | 455 |
| Challenges | 450 |
| Example 1 | 447 |
| Generation | 439 |
| Objective Function | 436 |
| Segmentation | 429 |
| Scoring | 427 |
| Adversarial Training | 423 |
| Sentence | 420 |
| Classifier | 415 |
| Inter-Annotator Agreement | 415 |
| Loss Function | 415 |
| English | 408 |
| Input: | 408 |
| Comparison | 406 |
| Syntax | 406 |
| Named Entity Recognition | 405 |
| Input | 400 |
| 7. | 400 |
| Domain Adaptation | 398 |
| Representation | 397 |
| Formulation | 396 |
| Overall Performance | 396 |
| Combinatory Categorial Grammar | 396 |
| 7 | 395 |
| Observations | 395 |
| Search | 393 |
| Translation | 385 |
| Support Vector Machines | 383 |
| Figure 10 | 379 |
| BERT | 374 |
| Hyperparameters | 373 |
| Training Procedure | 369 |
| Figure 8 | 364 |
| Normalization | 363 |
| Example 2 | 358 |
| Design | 356 |
| Figure 9 | 355 |
| I | 354 |
| The Problem | 354 |
| Reinforcement Learning | 354 |
| Language | 351 |
| Post-processing | 345 |
| Future Directions | 344 |
| 6: | 343 |
| . | 342 |
| Relation Extraction | 339 |
| Problem Description | 337 |
| 6. | 336 |
| Feature Set | 333 |
| Prediction | 331 |
| Statistical Machine Translation | 321 |
| Category | 321 |
| État de l'art | 316 |
| Syntactic Features | 315 |
| Visualization | 314 |
| 3.1 | 309 |
| Type | 308 |
| Parser | 305 |
| Accuracy | 304 |
| Word Alignment | 304 |
| 7: | 303 |
| Lexical Features | 302 |
| Problem Setting | 301 |
| Terminology | 299 |
| Figure 12 | 296 |
| Feature | 295 |
| System Combination | 294 |
| Word Sense Disambiguation | 293 |
| 2.1 | 291 |
| Research Questions | 290 |
| Transformer | 287 |
| Hypotheses | 281 |
| Smoothing | 279 |
| Morphology | 278 |
| Sentiment Classification | 278 |
| Semantics | 277 |
| Lexicon | 276 |
| Disambiguation | 274 |
| An example | 274 |
| Candidate Generation | 273 |
| Application | 271 |
| Submissions | 270 |
| Word | 269 |
| Rules | 268 |
| Basic Idea | 268 |
| Parameters | 267 |
| Outline | 267 |
| Active Learning | 266 |
| Tokenization | 265 |
| User Interface | 264 |
| Knowledge Distillation | 260 |
| Input Representation | 259 |
| Filtering | 259 |
| Figure 11 | 259 |
| Attention | 258 |
| Linguistic Features | 258 |
| Pre-training | 258 |
| Generator | 257 |
| Properties | 256 |
| - | 255 |
| Semantic Role Labeling | 253 |
| Statistics | 251 |
| Sentence Encoder | 248 |
| Ensemble | 248 |
| Learning and Inference | 248 |
| 2.2 | 246 |
| Measures | 245 |
| Rule Extraction | 245 |
| Objectives | 244 |
| Inter-annotator agreement | 244 |
| Example 3 | 244 |
| Performance Comparison | 243 |
| Feature Representation | 241 |
| 3.2 | 241 |
| 10: | 240 |
| Fine-tuning | 240 |
| Complexity | 238 |
| 8 | 236 |
| ) | 235 |
| Notations | 234 |
| Pruning | 232 |
| Inter-annotator Agreement | 231 |
| (a) | 230 |
| Formalization | 230 |
| Class | 230 |
| Grammar | 227 |
| (4) | 227 |
| Natural Language Inference | 226 |
| Ranking | 224 |
| Joint Training | 223 |
| Sentence Selection | 222 |
| PLANS FOR THE COMING YEAR | 222 |
| 2.3 | 222 |
| Similarity Measures | 221 |
| Question Answering | 221 |
| Tools | 219 |
| Efficiency | 218 |
| Word Similarity | 217 |
| Multi-task Learning | 216 |
| Correctness | 216 |
| Testing | 216 |
| Problem | 215 |
| Training Objectives | 214 |
| Condition | 214 |
| Extensions | 213 |
| Initialization | 213 |
| The | 213 |
| Question Generation | 212 |
| Input Layer | 212 |
| Feature Design | 211 |
| Output | 210 |
| Output Layer | 209 |
| I I | 208 |
| Sampling | 207 |
| Nouns | 205 |
| Broader Impact | 205 |
| ¡ | 203 |
| Question | 203 |
| Structure | 203 |
| 11: | 202 |
| Attention Mechanism | 201 |
| b. | 200 |
| 3.3 | 198 |
| Verbs | 198 |
| Proposed Framework | 198 |
| State of the Art | 197 |
| Previous Research | 197 |
| 9 | 197 |
| Part-of-Speech Tagging | 196 |
| Parameterization | 196 |
| 10 | 195 |
| Expériences | 194 |
| Extraction | 193 |
| Relation | 193 |
| Outlook | 192 |
| Participating Systems | 190 |
| Theory | 190 |
| Domain | 188 |
| Table 1 | 188 |
| User Study | 188 |
| Case Studies | 187 |
| Embedding Layer | 187 |
| Validation | 186 |
| Semantic Features | 186 |
| (b) | 185 |
| Text Classification | 184 |
| Composition | 184 |
| S | 183 |
| Problems | 183 |
| Interpretation | 183 |
| String Kernels | 182 |
| Regularization | 182 |
| Training details | 181 |
| Coverage | 180 |
| 1) | 180 |
| Relations | 180 |
| Coordination | 180 |
| Reranking | 180 |
| The Task | 179 |
| Supervised Learning | 179 |
| Text | 177 |
| 4.1 | 176 |
| Problem Formalization | 176 |
| Embeddings | 175 |
| Final Remarks | 175 |
| Feature Sets | 174 |
| Word Embedding | 174 |
| Perspectives | 173 |
| Mutual Information | 173 |
| Workflow | 172 |
| Feature Templates | 172 |
| Baseline Features | 171 |
| Graph Encoder | 171 |
| Word Segmentation | 170 |
| German | 170 |
| Unsupervised Learning | 170 |
| Negation | 170 |
| Name | 169 |
| Figure 13 | 169 |
| Transfer | 169 |
| Pronouns | 168 |
| Languages | 168 |
| Example: | 168 |
| Learning Objective | 168 |
| BLEU | 167 |
| Logistic Regression | 167 |
| Transition System | 167 |
| Mention Detection | 167 |
| Findings | 167 |
| Speech Recognition | 166 |
| Generalization | 166 |
| WordNet | 165 |
| Word embeddings | 165 |
| Recommendations | 165 |
| Lexical features | 165 |
| Output: | 164 |

## Normalization Note
Rules are conservative and use only explicit section headings. Paragraph content is not used to infer section labels.
