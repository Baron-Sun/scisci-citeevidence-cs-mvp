# Phase-2 Pilot Analysis Report

Phase-2 labels are model-assisted structured evidence labels, not human gold annotation. All accepted non-abstain labels must retain exact local evidence and `evidence_supports_label=true`.

## Outputs
- Summary CSV: `data/processed/phase2_pilot_analysis_summary.csv`
- Case studies CSV: `data/processed/phase2_case_studies.csv`
- Phase-1 vs Phase-2 confusion CSV: `data/processed/phase2_phase1_vs_phase2_confusion.csv`
- Figures: `figures`

## Core Counts
| metric                                     |    value |
|:-------------------------------------------|---------:|
| total_phase2_labels                        | 582      |
| total_remaining_failed_rows                |  18      |
| final_failure_rate                         |   0.03   |
| abstain_count                              |   1      |
| abstain_rate                               |   0.0017 |
| evidence_span_non_empty_rate               |   1      |
| evidence_span_grounded_rate                |   1      |
| phase1_phase2_disagreement_count           | 133      |
| phase1_phase2_disagreement_rate            |   0.2285 |
| problem_or_motivation_quote_grounded_rate  |   1      |
| usage_or_mechanism_quote_grounded_rate     |   1      |
| comparison_or_tradeoff_quote_grounded_rate |   1      |

## Final Intent Distribution
| final_intent     |   rows |       rate |
|:-----------------|-------:|-----------:|
| compares_against |    153 | 0.262887   |
| uses             |    146 | 0.250859   |
| background       |    125 | 0.214777   |
| extends          |     63 | 0.108247   |
| critiques        |     53 | 0.0910653  |
| applies          |     41 | 0.0704467  |
| unclear          |      1 | 0.00171821 |

## Final Object Type Distribution
| final_object_type     |   rows |      rate |
|:----------------------|-------:|----------:|
| model                 |    136 | 0.233677  |
| method                |    116 | 0.199313  |
| unknown               |     91 | 0.156357  |
| metric                |     63 | 0.108247  |
| claim_or_finding      |     46 | 0.0790378 |
| dataset_or_database   |     46 | 0.0790378 |
| software_or_tool      |     42 | 0.0721649 |
| benchmark_or_protocol |     17 | 0.0292096 |
| task                  |     13 | 0.0223368 |
| theory_or_concept     |     12 | 0.0206186 |

## Final Relation Subtype Distribution
| final_relation_subtype   |   rows |       rate |
|:-------------------------|-------:|-----------:|
| compare_against          |    152 | 0.261168   |
| direct_use               |    146 | 0.250859   |
| none                     |    124 | 0.213058   |
| adapt_to_domain          |     63 | 0.108247   |
| critique_limitation      |     53 | 0.0910653  |
| improve                  |     31 | 0.0532646  |
| component_use            |      7 | 0.0120275  |
| report_metric            |      3 | 0.00515464 |
| evaluate_on              |      2 | 0.00343643 |
| combine_with             |      1 | 0.00171821 |

## Method Edge Type Distribution
| method_edge_type   |   rows |      rate |
|:-------------------|-------:|----------:|
| compares           |    159 | 0.273196  |
| background         |    153 | 0.262887  |
| uses_component     |    125 | 0.214777  |
| not_method_related |     57 | 0.0979381 |
| extends            |     43 | 0.0738832 |
| adapts             |     39 | 0.0670103 |
| improves           |      6 | 0.0103093 |

## Stance Distribution
| stance   |   rows |       rate |
|:---------|-------:|-----------:|
| neutral  |    458 | 0.786942   |
| positive |     60 | 0.103093   |
| negative |     58 | 0.0996564  |
| mixed    |      4 | 0.00687285 |
| unclear  |      2 | 0.00343643 |

## Evidence Supports Label Distribution
| evidence_supports_label   |   rows |       rate |
|:--------------------------|-------:|-----------:|
| true                      |    581 | 0.998282   |
| false                     |      1 | 0.00171821 |

## Confidence Distribution
| confidence_bin   |   rows |
|:-----------------|-------:|
| [0,0.2]          |      0 |
| (0.2,0.5]        |      1 |
| (0.5,0.7]        |      0 |
| (0.7,0.85]       |    182 |
| (0.85,1.0]       |    399 |

## Phase-1 Vs Phase-2 Confusion
| primary_candidate_intent   | final_intent     |   rows |   row_rate |
|:---------------------------|:-----------------|-------:|-----------:|
| applies                    | applies          |     37 | 0.560606   |
| applies                    | uses             |     13 | 0.19697    |
| applies                    | compares_against |     11 | 0.166667   |
| applies                    | background       |      4 | 0.0606061  |
| applies                    | critiques        |      1 | 0.0151515  |
| background                 | background       |     64 | 0.864865   |
| background                 | compares_against |      7 | 0.0945946  |
| background                 | critiques        |      2 | 0.027027   |
| background                 | extends          |      1 | 0.0135135  |
| compares_against           | compares_against |    113 | 0.869231   |
| compares_against           | background       |     14 | 0.107692   |
| compares_against           | uses             |      2 | 0.0153846  |
| compares_against           | critiques        |      1 | 0.00769231 |
| critiques                  | critiques        |     49 | 0.662162   |
| critiques                  | background       |     15 | 0.202703   |
| critiques                  | compares_against |      9 | 0.121622   |
| critiques                  | extends          |      1 | 0.0135135  |
| extends                    | extends          |     60 | 0.882353   |
| extends                    | background       |      3 | 0.0441176  |
| extends                    | compares_against |      2 | 0.0294118  |
| extends                    | applies          |      1 | 0.0147059  |
| extends                    | unclear          |      1 | 0.0147059  |
| extends                    | uses             |      1 | 0.0147059  |
| unclear                    | background       |     11 | 0.52381    |
| unclear                    | compares_against |      4 | 0.190476   |
| unclear                    | uses             |      4 | 0.190476   |
| unclear                    | applies          |      1 | 0.047619   |
| unclear                    | extends          |      1 | 0.047619   |
| uses                       | uses             |    126 | 0.845638   |
| uses                       | background       |     14 | 0.0939597  |
| uses                       | compares_against |      7 | 0.0469799  |
| uses                       | applies          |      2 | 0.0134228  |

## Most Common Phase-1 To Phase-2 Corrections
| primary_candidate_intent   | final_intent     |   rows |
|:---------------------------|:-----------------|-------:|
| critiques                  | background       |     15 |
| compares_against           | background       |     14 |
| uses                       | background       |     14 |
| applies                    | uses             |     13 |
| applies                    | compares_against |     11 |
| unclear                    | background       |     11 |
| critiques                  | compares_against |      9 |
| background                 | compares_against |      7 |
| uses                       | compares_against |      7 |
| applies                    | background       |      4 |
| unclear                    | compares_against |      4 |
| unclear                    | uses             |      4 |
| extends                    | background       |      3 |
| background                 | critiques        |      2 |
| compares_against           | uses             |      2 |

## Final Intent By Known Section
| normalized_section   | final_intent     |   rows |
|:---------------------|:-----------------|-------:|
| abstract             | extends          |      4 |
| abstract             | applies          |      2 |
| abstract             | compares_against |      2 |
| abstract             | uses             |      1 |
| analysis             | compares_against |      3 |
| analysis             | extends          |      1 |
| analysis             | uses             |      1 |
| background           | background       |      2 |
| background           | compares_against |      1 |
| background           | critiques        |      1 |
| conclusion           | compares_against |      3 |
| conclusion           | uses             |      2 |
| conclusion           | background       |      1 |
| conclusion           | critiques        |      1 |
| conclusion           | extends          |      1 |
| discussion           | critiques        |      2 |
| discussion           | compares_against |      1 |
| discussion           | uses             |      1 |
| evaluation           | uses             |      8 |
| evaluation           | compares_against |      5 |
| evaluation           | background       |      3 |
| evaluation           | critiques        |      3 |
| evaluation           | applies          |      1 |
| experiment           | uses             |     28 |
| experiment           | compares_against |     18 |
| experiment           | background       |      4 |
| experiment           | critiques        |      2 |
| experiment           | applies          |      1 |
| experiment           | extends          |      1 |
| introduction         | background       |     45 |
| introduction         | compares_against |     28 |
| introduction         | extends          |     22 |
| introduction         | critiques        |     21 |
| introduction         | applies          |     11 |
| introduction         | uses             |      5 |
| introduction         | unclear          |      1 |
| method               | uses             |      9 |
| method               | compares_against |      6 |
| method               | background       |      2 |
| method               | applies          |      1 |
| method               | extends          |      1 |
| model                | uses             |     11 |
| model                | background       |      5 |
| model                | compares_against |      5 |
| model                | extends          |      5 |
| model                | critiques        |      3 |
| model                | applies          |      2 |
| related_work         | compares_against |     23 |
| related_work         | background       |     18 |
| related_work         | critiques        |      9 |
| related_work         | extends          |      8 |
| related_work         | uses             |      4 |
| related_work         | applies          |      3 |
| results              | compares_against |     14 |
| results              | critiques        |      3 |
| results              | uses             |      2 |
| results              | applies          |      1 |
| results              | extends          |      1 |

## Unknown Section Rows
209

## Final Intent By Object Type
| final_intent     | final_object_type     |   rows |
|:-----------------|:----------------------|-------:|
| applies          | method                |     19 |
| applies          | software_or_tool      |      9 |
| applies          | dataset_or_database   |      4 |
| applies          | model                 |      4 |
| applies          | benchmark_or_protocol |      2 |
| applies          | task                  |      2 |
| applies          | unknown               |      1 |
| background       | unknown               |     30 |
| background       | model                 |     26 |
| background       | method                |     21 |
| background       | claim_or_finding      |     19 |
| background       | dataset_or_database   |      9 |
| background       | metric                |      6 |
| background       | task                  |      6 |
| background       | theory_or_concept     |      6 |
| background       | benchmark_or_protocol |      2 |
| compares_against | model                 |     42 |
| compares_against | metric                |     34 |
| compares_against | unknown               |     26 |
| compares_against | method                |     20 |
| compares_against | claim_or_finding      |     14 |
| compares_against | dataset_or_database   |      6 |
| compares_against | benchmark_or_protocol |      5 |
| compares_against | task                  |      4 |
| compares_against | software_or_tool      |      1 |
| compares_against | theory_or_concept     |      1 |
| critiques        | unknown               |     17 |
| critiques        | model                 |     12 |
| critiques        | claim_or_finding      |     10 |
| critiques        | metric                |      8 |
| critiques        | method                |      4 |
| critiques        | dataset_or_database   |      1 |
| critiques        | theory_or_concept     |      1 |
| extends          | method                |     25 |
| extends          | model                 |     16 |
| extends          | unknown               |     12 |
| extends          | software_or_tool      |      6 |
| extends          | claim_or_finding      |      2 |
| extends          | benchmark_or_protocol |      1 |
| extends          | dataset_or_database   |      1 |
| unclear          | unknown               |      1 |
| uses             | model                 |     36 |
| uses             | method                |     27 |
| uses             | software_or_tool      |     26 |
| uses             | dataset_or_database   |     25 |
| uses             | metric                |     15 |
| uses             | benchmark_or_protocol |      7 |
| uses             | theory_or_concept     |      4 |
| uses             | unknown               |      4 |
| uses             | claim_or_finding      |      1 |
| uses             | task                  |      1 |

## Top Object Names
| object_name         |   rows |
|:--------------------|-------:|
| accuracy            |     70 |
| BERT                |     52 |
| BLEU                |     38 |
| LSTM                |     35 |
| F1                  |     27 |
| Transformer         |     27 |
| seq2seq             |     23 |
| CRF                 |     21 |
| Penn Treebank       |     15 |
| ROUGE               |     14 |
| word2vec            |     14 |
| GloVe               |     14 |
| WordNet             |     13 |
| METEOR              |     10 |
| attention mechanism |     10 |
| ELMo                |     10 |
| WMT                 |     10 |
| SemEval             |      8 |
| Moses               |      8 |
| CoNLL-2003          |      5 |
| perplexity          |      5 |
| Stanford CoreNLP    |      5 |
| HMM                 |      5 |
| GIZA++              |      5 |
| OntoNotes           |      5 |

## Named Objects Vs Generic Metrics
| object_signal                   |   rows |
|:--------------------------------|-------:|
| neither                         |    248 |
| named_object_only               |    205 |
| named_object_and_generic_metric |    129 |

## Evidence Quality
| metric                                     |   value |
|:-------------------------------------------|--------:|
| evidence_span_non_empty_rate               |       1 |
| evidence_span_grounded_rate                |       1 |
| problem_or_motivation_quote_grounded_rate  |       1 |
| usage_or_mechanism_quote_grounded_rate     |       1 |
| comparison_or_tradeoff_quote_grounded_rate |       1 |

## Remaining Failed Rows By Failure Category
| failed_validator_type            |   rows |      rate |
|:---------------------------------|-------:|----------:|
| evidence_span_not_substring      |      7 | 0.388889  |
| compare_cue_not_accepted         |      6 | 0.333333  |
| cited_title_only_object_rejected |      2 | 0.111111  |
| quote_not_substring              |      2 | 0.111111  |
| use_cue_not_accepted             |      1 | 0.0555556 |

## Report-Ready Examples
### uses

| intent   | cited_paper_title                                                                  | citation_sentence                                                                                                                                                | evidence_span                                                                 | why_label_is_correct                                                                                                                                   |
|:---------|:-----------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| uses     | {G}lo{V}e: Global Vectors for Word Representation                                  | For parameters setups, we initialize the word embedding layer with 200-dimensional Glove embedding (Pennington et al., 2014) , where the Twitter version is u... | we initialize the word embedding layer with 200-dimensional Glove embedding   | The text indicates the use of GloVe embeddings to initialize the word embedding layer, indicating a 'uses' relationship with a 'component_use' subt... |
| uses     | Unsupervised Cross-lingual Representation Learning at Scale                        | For passage representation, we use the publicly available, pre-trained XLM-RoBERTa (Conneau et al., 2020) , a variant of BERT which removes the standard BERT... | we use the publicly available, pre-trained XLM-RoBERTa (Conneau et al., 2020) | The context explicitly states the use of XLM-RoBERTa for passage representation, indicating direct use of the model.                                   |
| uses     | {BERT}: Pre-training of Deep Bidirectional Transformers for Language Understanding | We use the BERT-base model (Devlin et al., 2019) for our experiments.                                                                                            | We use the BERT-base model (Devlin et al., 2019) for our experiments.         | The citation explicitly states that the BERT-base model is used for experiments.                                                                       |

### compares_against

| intent           | cited_paper_title                                                                          | citation_sentence                                                                                                                                                | evidence_span                                                                                                            | why_label_is_correct                                                                                              |
|:-----------------|:-------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------|
| compares_against | A Systematic Comparison of Phrase-Based, Hierarchical and Syntax-Augmented Statistical ... | While producing smaller translation models and believed to contain more useful (syntax-aware) phrases than the standard string-based extraction, the syntaxba... | perform worse than the PB-SMT string-based baseline                                                                      | The context explicitly compares syntax-based extractions with PB-SMT using performance metrics.                   |
| compares_against | Deep Unordered Composition Rivals Syntactic Methods for Text Classification                | Compared to previous data augmentaion methods (Iyyer et al., 2015; Xie et al., 2017; Fadaee et al., 2017; Artetxe et al., 2018; Lample et al., 2018) , the so... | Compared to previous data augmentaion methods (Iyyer et al., 2015; Xie et al., 2017; Fadaee et al., 2017; Artetxe et ... | The context explicitly compares the new method against those in the cited paper, indicating improved performance. |
| compares_against | Improving the Scalability of Semi-{M}arkov Conditional Random Fields for Named Entity R... | Existing work has shown that Semi-CRFs outperform CRFs on segment-level tagging tasks such as sequence segmentation (Andrew, 2006) , NER (Sarawagi and Cohen,... | Semi-CRFs outperform CRFs                                                                                                | The evidence indicates that Semi-CRFs outperform CRFs, showing a comparison between methods.                      |

### extends

| intent   | cited_paper_title                                                                        | citation_sentence                                                                                                                  | evidence_span                                                                                                   | why_label_is_correct                                                                                                                                   |
|:---------|:-----------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| extends  | A Hierarchical Reinforced Sequence Operation Method for Unsupervised Text Style Transfer | Specifically, we adapt the Mask-And-Infill (M&I) framework of Wu et al. (2019b) .                                                  | we adapt                                                                                                        | The sentence explicitly states that the current paper adapts the cited framework, indicating an extension.                                             |
| extends  | Learning to Generate Market Comments from Stock Prices                                   | In this study, we extend Murakami et al. (2017) 's model with a new architecture to solve the problem due to the noisy alignments. | we extend Murakami et al. (2017) 's model with a new architecture                                               | The sentence explicitly states that the current study extends the model proposed by Murakami et al. (2017) to improve its handling of noisy alignme... |
| extends  | Neural Architectures for Named Entity Recognition                                        | Here we modify the LSTM model proposed by Lample et al. (2016) by augmenting the network with 'crowd worker vectors'.              | we modify the LSTM model proposed by Lample et al. (2016) by augmenting the network with 'crowd worker vectors' | The text explicitly states that the paper modifies the LSTM model from Lample et al. (2016) by augmenting it with additional vectors, indicating an... |

### critiques

| intent    | cited_paper_title                                                                   | citation_sentence                                                                                                                                                | evidence_span                         | why_label_is_correct                                                                                     |
|:----------|:------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------|:---------------------------------------------------------------------------------------------------------|
| critiques | Combining Distributional and Morphological Information for Part of Speech Induction | While there has been much prior work on this task (Brown et al., 1992; Clark, 2003; Christodoulopoulos et al., 2010; Toutanova and Johnson, 2008; Goldwater a... | structure suffer from                 | The citation critiques the HMM method for its tendency to assign too many tags, indicating a limitation. |
| critiques | The limits of automatic summarisation according to {ROUGE}                          | We focus on evaluating the fluency and faithfulness since the ROUGE score often fails to quan- tify them (Schluter, 2017; Cao et al., 2018) .                    | ROUGE score often fails to quan- tify | The citation critiques the ROUGE metric by highlighting its failure to quantify certain aspects.         |
| critiques | Word Sense Disambiguation using Conceptual Density                                  | On the other hand, Knowledge based approaches (Lesk, 1986; Walker and Amsler, 1986; Agirre and Rigau, 1996; Rada, 2005; Agirre and Soroa, 2009) which use wor... | but fail to deliver good results      | The citation context critiques the effectiveness of knowledge-based approaches.                          |

### applies

| intent   | cited_paper_title                                                                  | citation_sentence                                                                                                                                                | evidence_span                                                                       | why_label_is_correct                                                                                                                                   |
|:---------|:-----------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| applies  | Intelligent Selection of Language Model Training Data                              | We applied cross-entropy filtering (Moore and Lewis, 2010) to the German Common Crawl corpus performing the following steps:                                     | We applied cross-entropy filtering (Moore and Lewis, 2010) to                       | The citing paper applies the cross-entropy filtering method from Moore and Lewis (2010) to a specific dataset, indicating application and adaptation.  |
| applies  | Learning to recognize features of valid textual entailments                        | Based on this representation, we apply a two stage entailment process similar to MacCartney et al. (2006) developed for textual entailment: an alignment stag... | we apply a two stage entailment process similar to                                  | The context indicates that the paper applies and adapts a two-stage entailment process similar to the one developed by the cited work, indicating a... |
| applies  | {BERT}: Pre-training of Deep Bidirectional Transformers for Language Understanding | We apply the standard transformer encoder (Devlin et al., 2019) to train our models, one for TDM triple prediction, and one for score 8 We randomly choose 10... | We apply the standard transformer encoder (Devlin et al., 2019) to train our models | The provided context states the application of the transformer encoder from Devlin et al., indicating an adaptation to a specific task.                |

### background

| intent     | cited_paper_title                                                                          | citation_sentence                                                                                                                                                | evidence_span                                                                                                            | why_label_is_correct                                                                                                                                |
|:-----------|:-------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------|
| background | Constituency Parsing with a Self-Attentive Encoder                                         | Our model follows the encoder-decoder architecture commonly used in state-of-the-art neural parsing models (Kitaev and Klein, 2018; Kiperwasser and Goldberg,... | Our model follows the encoder-decoder architecture commonly used in state-of-the-art neural parsing models (Kitaev an... | The context describes common architecture usage; hence labeled as background.                                                                       |
| background | A Classifier-Based Parser with Linear Run-Time Complexity                                  | Conventionally, we use 18 coarse-grained relations and binarize non-binary relations with right-branching (Sagae and Lavie, 2005) .                              | Conventionally, we use 18 coarse-grained relations and binarize non-binary relations with right-branching (Sagae and ... | The citation merely explains a convention in binarizing relations and does not indicate a direct use or application; thus, it serves as background. |
| background | Large-Scale Discriminative Training for Statistical Machine Translation Using Held-Out ... | While some variants have been considered (Och, 2003; Flanigan et al., 2013) , we use an expected BLEU approximation, assuming hypotheses are drawn from a log... | While some variants have been considered (Och, 2003; Flanigan et al., 2013)                                              | The citation describes variants considered by the cited works, indicating background context for the current paper's method.                        |


## Figure Files
| figure                        | path                                             |
|:------------------------------|:-------------------------------------------------|
| final_intent_distribution     | figures/phase2_final_intent_distribution.png     |
| object_type_distribution      | figures/phase2_object_type_distribution.png      |
| relation_subtype_distribution | figures/phase2_relation_subtype_distribution.png |
| method_edge_type_distribution | figures/phase2_method_edge_type_distribution.png |
| intent_by_section             | figures/phase2_intent_by_section.png             |
| phase1_vs_phase2_disagreement | figures/phase2_phase1_vs_phase2_disagreement.png |

## Remaining Failure Examples
| context_id                | primary_candidate_intent   | validation_error                                                      | failed_validator_type            | candidate_repair_action                             | revalidated   | revalidation_error                                                    | final_intent     | final_object_type   | evidence_span                                                                                                                                                                                                                                                                                                                                                                                                                                               | raw_response                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|:--------------------------|:---------------------------|:----------------------------------------------------------------------|:---------------------------------|:----------------------------------------------------|:--------------|:----------------------------------------------------------------------|:-----------------|:--------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ctxr_97d7b630afa246025e57 | critiques                  | cited-title-only object type cannot be used as direct evidence        | cited_title_only_object_rejected | keep_failed_direct_context_object_evidence_required | False         | cited-title-only object type cannot be used as direct evidence        | compares_against | model               | Compared to the recently published works on ERC (Chen et al., 2018; Zhou et al., 2018; Qin et al., 2020; Zhong et al., 2019; Zhang et al., 2019) , both lexicon-based (Wu et al., 2006; Mohammad and Turney, 2010; Shaheen et al., 2014) and modern deep learning-based (Kratzwald et al., 2018; Colneriĉ and Demsar, 2018) vanilla emotion recognition approaches fail to work well on ERC datasets as this work ignores the conversation specific factors | {"final_intent":"compares_against","final_object_type":"model","final_relation_subtype":"compare_against","method_edge_type":"compares","stance":"negative","evidence_span":"Compared to the recently published works on ERC (Chen et al., 2018; Zhou et al., 2018; Qin et al., 2020; Zhong et al., 2019; Zhang et al., 2019) , both lexicon-based (Wu et al., 2006; Mohammad and Turney, 2010; Shaheen et al., 2014) and modern deep learning-based (Kratzwald et al., 2018; Colneriĉ and Demsar, 2018) vanilla emotion recognition approaches fail to work well on ERC datasets as this work ignores the conversation specific factors","problem_or_motivation_quote":null,"usage_or_mechanism_quote":null,"comparison_or_tradeoff_quote":"Compared to the recently published works on ERC (Chen et al., 2018; Zhou et al., 2018; Qin et al., 2020; Zhong et al., 2019; Zhang et al., 2019) , both lexicon-based (Wu et al., 2006; Mohammad and Turney, 2010; Shaheen et al., 2014) and modern deep learning-based (Kratzwald et al., 2018; Colneriĉ and Demsar, 2018) vanilla emotion recognition approaches fail to work well on ERC datasets","evidence_supports_label":"true","abstain":false,"abstain_reason":null,"confidence":0.9,"rationale_short":"The citation contrasts the performance of various models, including Zhong et al., against other approaches, indicating a comparison."} |
| ctxr_fe6c93581c049b7293eb | critiques                  | evidence_span is not an exact substring of evidence fields            | evidence_span_not_substring      | needs_model_retry_or_manual_review                  | False         | evidence_span is not an exact substring of evidence fields            | compares_against | metric              | compare model performances with additional metrics, including ... Sentence Mover's Similarity (SMS) (Clark et al., 2019)                                                                                                                                                                                                                                                                                                                                    | {"final_intent":"compares_against","final_object_type":"metric","final_relation_subtype":"compare_against","method_edge_type":"compares","stance":"neutral","evidence_span":"compare model performances with additional metrics, including ... Sentence Mover's Similarity (SMS) (Clark et al., 2019)","problem_or_motivation_quote":"recognizing the limitation of ROUGE scores","usage_or_mechanism_quote":null,"comparison_or_tradeoff_quote":"compare model performances with additional metrics, including ... Sentence Mover's Similarity (SMS) (Clark et al., 2019)","evidence_supports_label":"true","abstain":false,"abstain_reason":null,"confidence":0.9,"rationale_short":"The context indicates a comparison of Sentence Mover's Similarity (SMS) against other metrics, fitting the 'compares_against' intent."}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ctxr_004aee8a00d8284e80c1 | uses                       | evidence_span is not an exact substring of evidence fields            | evidence_span_not_substring      | needs_model_retry_or_manual_review                  | False         | evidence_span is not an exact substring of evidence fields            | uses             | method              | combine the forward and backward Viterbi alignments to obtain many-to-many word alignments as described in Koehn et al. (2003)                                                                                                                                                                                                                                                                                                                              | {"final_intent":"uses","final_object_type":"method","final_relation_subtype":"combine_with","method_edge_type":"background","stance":"neutral","evidence_span":"combine the forward and backward Viterbi alignments to obtain many-to-many word alignments as described in Koehn et al. (2003)","problem_or_motivation_quote":null,"usage_or_mechanism_quote":"We use the GIZA++ toolkit...combine the forward and backward Viterbi alignments to obtain many-to-many word alignments as described in Koehn et al. (2003)","comparison_or_tradeoff_quote":null,"evidence_supports_label":"true","abstain":false,"abstain_reason":null,"confidence":0.9,"rationale_short":"The context shows the authors using a combination method involving Koehn et al. (2003), indicating 'uses' and 'combine_with' as the label."}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ctxr_01dfe9c1d79e5b737aec | uses                       | evidence_span is not an exact substring of evidence fields            | evidence_span_not_substring      | needs_model_retry_or_manual_review                  | False         | evidence_span is not an exact substring of evidence fields            | uses             | software_or_tool    | we use open-sourced third-party libraries including ... Transformers (Wolf et al., 2020)                                                                                                                                                                                                                                                                                                                                                                    | {"final_intent":"uses","final_object_type":"software_or_tool","final_relation_subtype":"direct_use","method_edge_type":"uses_component","stance":"neutral","evidence_span":"we use open-sourced third-party libraries including ... Transformers (Wolf et al., 2020)","problem_or_motivation_quote":null,"usage_or_mechanism_quote":"we use open-sourced third-party libraries including ... Transformers (Wolf et al., 2020)","comparison_or_tradeoff_quote":null,"evidence_supports_label":"true","abstain":false,"abstain_reason":null,"confidence":0.95,"rationale_short":"The paper explicitly states the use of 'Transformers' library, indicating direct use."}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ctxr_363efd3c3ba0c73a9cc2 | uses                       | evidence_span is not an exact substring of evidence fields            | evidence_span_not_substring      | needs_model_retry_or_manual_review                  | False         | evidence_span is not an exact substring of evidence fields            | background       | software_or_tool    | The parser can be used with ... the Berkeley parser (Petrov et al., 2006; Fowler and Penn, 2010)                                                                                                                                                                                                                                                                                                                                                            | {"final_intent":"background","final_object_type":"software_or_tool","final_relation_subtype":"none","method_edge_type":"background","stance":"neutral","evidence_span":"The parser can be used with ... the Berkeley parser (Petrov et al., 2006; Fowler and Penn, 2010)","problem_or_motivation_quote":null,"usage_or_mechanism_quote":null,"comparison_or_tradeoff_quote":null,"evidence_supports_label":"true","abstain":false,"abstain_reason":null,"confidence":0.85,"rationale_short":"The context describes the use of the Berkeley parser as a background option without focusing on its implementation or improvement."}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ctxr_ee161df70fc5a9623218 | applies                    | cited-title-only object type cannot be used as direct evidence        | cited_title_only_object_rejected | keep_failed_direct_context_object_evidence_required | False         | cited-title-only object type cannot be used as direct evidence        | uses             | software_or_tool    | we used TIPSem (Llorens et al., 2010) to generate the tense and aspect of events and find time expressions                                                                                                                                                                                                                                                                                                                                                  | {"final_intent":"uses","final_object_type":"software_or_tool","final_relation_subtype":"direct_use","method_edge_type":"uses_component","stance":"neutral","evidence_span":"we used TIPSem (Llorens et al., 2010) to generate the tense and aspect of events and find time expressions","problem_or_motivation_quote":"Because these features are known to be the most important for relating events to document creation time","usage_or_mechanism_quote":"we used TIPSem (Llorens et al., 2010) to generate the tense and aspect of events and find time expressions","comparison_or_tradeoff_quote":null,"evidence_supports_label":"true","abstain":false,"abstain_reason":null,"confidence":0.85,"rationale_short":"The context explicitly states the use of TIPSem for generating tense and aspect, indicating direct usage of the tool in the study."}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ctxr_f331f388751fdb0b0a54 | uses                       | final_intent=compares_against requires compare evidence               | compare_cue_not_accepted         | revalidate_after_cue_expansion                      | False         | final_intent=compares_against requires compare evidence               | compares_against | unknown             | Carreras et al. (2008) 90.7 91.4 91.1                                                                                                                                                                                                                                                                                                                                                                                                                       | {"final_intent":"compares_against","final_object_type":"unknown","final_relation_subtype":"compare_against","method_edge_type":"compares","stance":"neutral","evidence_span":"Carreras et al. (2008) 90.7 91.4 91.1","problem_or_motivation_quote":null,"usage_or_mechanism_quote":null,"comparison_or_tradeoff_quote":"Carreras et al. (2008) 90.7 91.4 91.1","evidence_supports_label":"true","abstain":false,"abstain_reason":null,"confidence":0.75,"rationale_short":"The citation is presented in a list of performance scores, indicating comparison."}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ctxr_9e2342ad3dd3776cb838 | compares_against           | usage_or_mechanism_quote is not an exact substring of evidence fields | quote_not_substring              | needs_model_retry_or_manual_review                  | False         | usage_or_mechanism_quote is not an exact substring of evidence fields | compares_against | model               | Compared with OneIE (Lin et al., 2020)                                                                                                                                                                                                                                                                                                                                                                                                                      | {"final_intent":"compares_against","final_object_type":"model","final_relation_subtype":"compare_against","method_edge_type":"compares","stance":"neutral","evidence_span":"Compared with OneIE (Lin et al., 2020)","problem_or_motivation_quote":null,"usage_or_mechanism_quote":"we creatively incorporate the AMR hierarchy to decide a more organized decoding order instead of a simple left-to-right order based on the word positions in the original sentence","comparison_or_tradeoff_quote":"Compared with OneIE (Lin et al., 2020)","evidence_supports_label":"true","abstain":false,"abstain_reason":null,"confidence":0.9,"rationale_short":"The context explicitly compares the current work with OneIE, revealing a comparison function."}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ctxr_e0075462c35abfa9a3a7 | extends                    | evidence_span is not an exact substring of evidence fields            | evidence_span_not_substring      | needs_model_retry_or_manual_review                  | False         | evidence_span is not an exact substring of evidence fields            | extends          | metric              | we adapt cross-entropy difference...and propose an extension to cross entropy difference with a vocabulary saturation filter (Lewis and Eetemadi, 2013)                                                                                                                                                                                                                                                                                                     | {"final_intent":"extends","final_object_type":"metric","final_relation_subtype":"improve","method_edge_type":"extends","stance":"neutral","evidence_span":"we adapt cross-entropy difference...and propose an extension to cross entropy difference with a vocabulary saturation filter (Lewis and Eetemadi, 2013)","problem_or_motivation_quote":null,"usage_or_mechanism_quote":"we adapt cross-entropy difference...and propose an extension to cross entropy difference with a vocabulary saturation filter (Lewis and Eetemadi, 2013)","comparison_or_tradeoff_quote":null,"evidence_supports_label":"true","abstain":false,"abstain_reason":null,"confidence":0.9,"rationale_short":"The context indicates an extension of a metric using the work of Lewis and Eetemadi (2013) with a vocabulary saturation filter."}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ctxr_e6655d1a1e4609cd177e | extends                    | final_intent=compares_against requires compare evidence               | compare_cue_not_accepted         | revalidate_after_cue_expansion                      | False         | final_intent=compares_against requires compare evidence               | compares_against | model               | most recent state-of-the-art models (Zhao et al., 2019; Grundkiewicz et al., 2019) , are trained on up to one hundred million additional synthetic parallel sentences                                                                                                                                                                                                                                                                                       | {"final_intent":"compares_against","final_object_type":"model","final_relation_subtype":"compare_against","method_edge_type":"compares","stance":"neutral","evidence_span":"most recent state-of-the-art models (Zhao et al., 2019; Grundkiewicz et al., 2019) , are trained on up to one hundred million additional synthetic parallel sentences","problem_or_motivation_quote":null,"usage_or_mechanism_quote":"we adapt models with only eight thousand parallel sentences","comparison_or_tradeoff_quote":"most recent state-of-the-art models (Zhao et al., 2019; Grundkiewicz et al., 2019) , are trained on up to one hundred million additional synthetic parallel sentences","evidence_supports_label":"true","abstain":false,"abstain_reason":null,"confidence":0.9,"rationale_short":"The context compares recent models by Grundkiewicz et al. (2019), highlighting the difference in training data size."}                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
