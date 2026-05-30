# Object Mentions LLM-as-Judge Review Report

This is a model-based audit / LLM-assisted validation pass.

## Outputs
- Sample CSV: `data/processed/object_mentions_llm_review_sample.csv`
- JSONL results or dry-run prompts: `data/processed/object_mentions_llm_review_results.jsonl`
- Parquet results: `data/processed/object_mentions_llm_review_results.parquet`

## Core Metrics
| metric | value |
| --- | --- |
| dry run | True |
| sample rows | 200 |
| reviewed rows | 0 |
| dry-run prompt records | 200 |
| fallback unclear rows | 0 |
| from cache rows | 0 |
| precision over true/false reviews | unavailable |
| input tokens | 0 |
| output tokens | 0 |
| total tokens | 0 |

## Sample Bucket Distribution
| review_bucket | rows |
| --- | --- |
| named_object_high_confidence | 60 |
| generic_metric | 40 |
| ambiguous_short_alias | 30 |
| generic_architecture | 30 |
| cited_title_object_profiles | 20 |
| context_window_neighbor | 20 |

## Reviewer Correct Distribution
No records available.

## Error Type Distribution
No records available.

## Recommended Action Distribution
No records available.

## Graph Allow Distribution
No records available.

## Phase-1 Feature Distribution
No records available.

## Precision By Object Category
No records available.

## Precision By Matched In
No records available.

## Precision By Canonical Name
No records available.

## False Or Unclear Examples
No records available.

## Registry Refinement Recommendations
Dry-run only: prompts and sample were generated, but no model decisions were collected.

## Sample Rows
| review_bucket | context_id | canonical_name | object_category | surface_form | matched_in | confidence | allow_in_object_graph | sentence_text |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| named_object_high_confidence | ctxr_c3916fd64523daff6d3a | GloVe | named_object | glove | sentence_text | 0.95 | True | The models were trained using the GloVe embeddings (Pennington et al., 2014) from SBWC 10 (from now on baseline-glove) and the Medical Word Embeddings for Sp... |
| named_object_high_confidence | ctxr_6051079d4ab639d5f668 | BLEU | named_object | BLEU score | sentence_text | 0.95 | True | We would like to mention that in the literature there are efficient algorithms to find the oracle BLEU (the hypothesis with the highest attainable BLEU score... |
| named_object_high_confidence | ctxr_026ea0fa3fa4021d7843 | LSTM | named_object | LSTM | sentence_text | 0.95 | True | This suggests that the transformer architecture has the capability of implicitly modelling sequential dependencies of the output labels, unlike earlier neura... |
| named_object_high_confidence | ctxr_152cde5443e55ceed4a1 | BERT | named_object | BERT | context_window_neighbor | 0.85 | True | In favor of the former, other research has suggested that Transformer-based architectures perform syntactic operations (Raganato and Tiedemann, 2018; Hewitt ... |
| named_object_high_confidence | ctxr_564c8a17b8bc709ecb67 | Transformer | named_object | Transformer | sentence_text | 0.95 | True | Alt et al. (2019) extended Generative Pre-trained Transformer (GPT) to learn semantic and syntactic features for DSRE. |
| named_object_high_confidence | ctxr_7cacde29db89c41748f1 | NLTK | named_object | NLTK | context_window_neighbor | 0.85 | True | To incorporate exemplars into the training set, Kshirsagar et al. (2015) apply an extra layer of filtering by excluding annotationsets containing no overt fr... |
| named_object_high_confidence | ctxr_27c6dbeab7ca7522678d | ROUGE | named_object | ROUGE | sentence_text | 0.95 | True | We evaluated our approach for all datasets using ROUGE-1 (R1), ROUGE-2 (R2), and ROUGE-L (RL) (Lin, 2004) , which calculate the word-overlap between the refe... |
| named_object_high_confidence | ctxr_4c8bd6da4c7e6083f4d0 | HMM | named_object | HMM | sentence_text | 0.95 | True | We collect bidirectional (bi) refined word alignment by growing the intersection of Chinese-to-English (CE) alignments and English-to-Chinese (EC) alignments... |
| named_object_high_confidence | ctxr_fa36552f3b98ccb348ae | BLEU | named_object | BLEU score | sentence_text | 0.95 | True | We also compared our system to a setup that follows (Eisele et al., 2008) and achieve much more reliable improvements over both indomain and out-of-domain ta... |
| named_object_high_confidence | ctxr_b28f095e068c5a29e8d6 | CRF | named_object | CRF | sentence_text | 0.95 | True | In one group, term extraction is treated as any other extraction task and is usually solved as a classification task using statistical, e.g., CRF, (Zhang, 20... |
| named_object_high_confidence | ctxr_bf651e31ba1cd92e3404 | LSTM | named_object | LSTM | sentence_text | 0.95 | True | For our LSTM model, we follow a standard bidirectional LSTM architecture (Huang et al., 2015; Ma and Hovy, 2016; Lample et al., 2016) . |
| named_object_high_confidence | ctxr_afde6618f08f1abea534 | HMM | named_object | HMM | context_window_neighbor | 0.85 | True | They can be seen as extensions of the simpler IBM models 1 and 2 (Brown et al., 1993) . |
| named_object_high_confidence | ctxr_4350b96e690d41c5e2e5 | WMT | named_object | WMT | sentence_text | 0.95 | True | These texts were back-translated (Sennrich et al., 2016a; Burlot and Yvon, 2018) into French using a relatively basic neural French-English engine trained wi... |
| named_object_high_confidence | ctxr_9eb834ab29a9cb639ede | FrameNet | named_object | Framenet | sentence_text | 0.95 | True | Das et al. (2010) , for example, use heuristics to detect frame triggers and pick the appropriate frame using a classifier that only considers the frames lic... |
| named_object_high_confidence | ctxr_831068f9b15e7e487393 | CRF | named_object | Conditional Random Fields | sentence_text | 0.95 | True | Many traditional NER methods are based on statistical sequence modeling methods, such as Hidden Markov Models (HMM) and Conditional Random Fields (CRF) (Cohe... |
| named_object_high_confidence | ctxr_df381934a802683bac79 | Transformer | named_object | Transformer | sentence_text | 0.95 | True | With rapid advances in neural based NLP, word alignment has recently regained some traction (Legrand et al., 2016) and improvements of the state of the art f... |
| named_object_high_confidence | ctxr_ca61e6e7be23d802775e | ROUGE | named_object | ROUGE | sentence_text | 0.95 | True | As in Nallapati et al. (2017) and Zhou et al. (2018) , we extract ground truth extraction labels by greedily selecting sentences which maximize the relative ... |
| named_object_high_confidence | ctxr_439de1fca6c445b4ee67 | CRF | named_object | CRF | context_window_neighbor | 0.85 | True | Recently, the language model pre-training (Peters et al., 2018; Radford et al., 2018; Devlin et al., 2019) has proven to be effective for improving many NLP ... |
| named_object_high_confidence | ctxr_0b03e7c7ae55f8fa48a5 | BLEU | named_object | BLEU | sentence_text | 0.95 | True | DP-based measures and BLEU have different characteristics (Yasuda et al., 2003) . |
| named_object_high_confidence | ctxr_e385146ded5d5db94eca | Moses | named_object | Moses decoder | context_window_neighbor | 0.85 | True | Integrating in-domain and out-of-domain language models one using log-linear features of an SMT model was carried out by Koehn and Schroeder (2007) . |
