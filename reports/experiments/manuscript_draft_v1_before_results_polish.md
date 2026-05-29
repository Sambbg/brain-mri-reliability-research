# Reliability Evaluation of Brain MRI Tumour Classification Models Under Calibration and Dataset Shift

## Abstract

Deep learning models for brain MRI tumour classification often report high internal accuracy on public benchmark datasets, but high accuracy alone may not establish clinical or cross-dataset reliability. This study evaluated whether internally high-performing brain MRI tumour classifiers remain reliable when assessed using leakage-aware splitting, calibration analysis, dataset overlap auditing, and glioma-focused domain-shift testing.

Three architectures were trained on a leakage-aware split of a public four-class brain MRI tumour dataset: ResNet18, EfficientNet-B0, and ViT-B/16. Internal performance was assessed using accuracy, balanced accuracy, and macro-F1. Calibration was evaluated using confidence-accuracy gap, expected calibration error, Brier score, and negative log-likelihood, with post-hoc temperature scaling fitted on validation logits only. Candidate external datasets were audited for exact and perceptual overlap. One candidate dataset was rejected because of substantial overlap with the training dataset. A visually distinct glioma-focused DICOM dataset, D3B, was selected, converted into reproducible central 2D slices, and used for domain-shift confidence and prediction-distribution analysis.

All three models achieved high internal test performance. EfficientNet-B0 achieved the strongest internal result, followed closely by ResNet18, while ViT-B/16 performed slightly worse. Temperature scaling improved internal calibration for all models without changing classification performance. However, all models showed unstable behaviour on D3B. ResNet18 predicted glioma for 29.43% of D3B slices, EfficientNet-B0 for 44.15%, and ViT-B/16 for 40.38%. Temperature scaling softened confidence under D3B shift but did not change predicted class distributions or patient-majority behaviour.

These findings show that high internal performance and improved internal calibration are insufficient evidence of cross-dataset reliability. Brain MRI tumour classification studies should include leakage-aware splitting, dataset overlap auditing, calibration analysis, and domain-shift evaluation before making reliability claims.

## Keywords

Brain MRI; tumour classification; calibration; temperature scaling; dataset shift; leakage; reliability; deep learning; external validation; uncertainty

## 1. Introduction

## 1. Introduction

Deep learning has become widely used for brain MRI tumour analysis, including tumour classification, detection, and segmentation [REF-BMRI-001; REF-BMRI-002; REF-BMRI-003]. Public brain MRI datasets have enabled rapid benchmarking of convolutional neural networks, transformer-based models, and hybrid architectures. Many studies report high internal classification performance on repeated benchmark datasets, often using accuracy, precision, recall, or F1-score as the main evidence of model quality [REF-BMRI-001; REF-BMRI-002; REF-BMRI-004].

However, high internal accuracy alone is not sufficient evidence of reliability. Medical imaging models can appear highly accurate when duplicate or near-duplicate images leak across training and test sets, when patient-level grouping is not respected, or when public datasets overlap across supposedly independent sources [REF-LEAK-001; REF-LEAK-002; REF-LEAK-003]. In this setting, model performance may partly reflect data contamination or memorisation rather than robust generalisation.

Reliability also depends on confidence quality. Modern neural networks can be accurate while remaining poorly calibrated, meaning that predicted probabilities may not correspond well to empirical correctness [REF-CAL-001; REF-CAL-002]. This is important in medical imaging because confidence scores may influence how model outputs are interpreted, even when the model is not used for autonomous diagnosis. Calibration metrics such as expected calibration error, negative log-likelihood, and Brier score therefore provide information that accuracy alone cannot capture [REF-CAL-001; REF-CAL-002; REF-CAL-003].

A further challenge is dataset shift. Models trained and tested internally may behave differently when applied to images from different institutions, acquisition protocols, scanners, or dataset construction processes [REF-SHIFT-001; REF-SHIFT-002; REF-SHIFT-003]. External validation is therefore important, but candidate external datasets must themselves be audited before being treated as independent evidence. If two public datasets substantially overlap, using one as external validation for the other can create a false impression of generalisability.

This study evaluates brain MRI tumour classification models using a reliability-first framework. Rather than treating internal accuracy as sufficient, the study combines leakage-aware splitting, exact and perceptual overlap auditing, internal performance evaluation, calibration analysis, post-hoc temperature scaling, and glioma-focused domain-shift testing. Three architectures are evaluated: ResNet18, EfficientNet-B0, and ViT-B/16. The central research question is whether high-performing brain MRI tumour classifiers remain reliable when assessed using calibration, uncertainty-relevant confidence behaviour, and shifted-domain evaluation rather than internal accuracy alone.


## 2. Methods

### 2.1 Study design

This study used a reliability-focused experimental design to evaluate brain MRI tumour classification models beyond internal accuracy (Figure 1) [REF-SHIFT-001; REF-SHIFT-002; REF-REPORT-001]. The evaluation pipeline included leakage-aware dataset preparation, duplicate and overlap auditing, internal model evaluation, calibration analysis, post-hoc temperature scaling, and glioma-focused domain-shift testing.

Three model architectures were evaluated: ResNet18, EfficientNet-B0, and ViT-B/16. These architectures were selected to represent a compact convolutional baseline, a stronger convolutional architecture, and a transformer-based vision architecture. The purpose was not to claim universal architectural superiority, but to test whether high internal performance translated into reliable calibration and shifted-domain behaviour across model families.

### 2.2 Dataset sources and usage decisions

Three dataset roles were defined in the study (Table 1). D1 was used as the primary four-class brain MRI tumour dataset for internal model development and testing. Its labels consisted of glioma, meningioma, pituitary tumour, and no tumour.

D2 was initially considered as a candidate external validation dataset. However, exact and perceptual overlap auditing showed substantial overlap between D1 and D2. Because this overlap could compromise the independence of external validation, D2 was rejected as a clean external validation dataset [REF-LEAK-001; REF-LEAK-002; REF-LEAK-003; REF-LEAK-004]. D2 was therefore used only as evidence that public brain MRI datasets require overlap auditing before being treated as independent validation sources.

D3B was derived from the ICDC-Glioma / TCIA source and used as a glioma-focused shifted-domain dataset. Selected DICOM series were inspected, converted into reproducible central 2D slices, and audited against D1 using exact and perceptual hash checks. No D1-D3B exact or perceptual near-overlap was detected under the selected audit threshold. Because D3B is glioma-focused and does not reproduce the four-class label structure of D1, it was not used for full four-class external accuracy estimation. Instead, it was used for shifted-domain prediction and confidence-behaviour analysis [REF-SHIFT-001; REF-SHIFT-002; REF-SHIFT-003].

### 2.3 Leakage-aware preparation and overlap auditing

The D1 dataset was prepared using a leakage-aware workflow. Exact duplicate checks were performed before splitting. Train, validation, and test partitions were then created in a way intended to reduce leakage between development and evaluation data.

Candidate external datasets were also audited before use. Exact hash matching was used to detect identical files, while perceptual hashing was used to detect visually near-duplicate images. This was necessary because visually duplicated or near-duplicated medical images can inflate apparent model performance when they appear across training and evaluation partitions [REF-LEAK-001; REF-LEAK-002; REF-LEAK-003].

### 2.4 Model training

Three models were trained on D1: ResNet18, EfficientNet-B0, and ViT-B/16. Each model was trained using the same internal D1 split structure so that internal performance, calibration, and shifted-domain behaviour could be compared across architectures.

For each experiment, the best model checkpoint was selected using validation macro-F1. The final internal evaluation was then performed on the held-out D1 test set. Saved experiment artifacts were used to generate the manuscript tables and figures, rather than manually retyping result values.

### 2.5 Internal performance evaluation

Internal D1 performance was evaluated using accuracy, balanced accuracy, and macro-F1. Macro-F1 was treated as the main classification summary metric because it gives equal weight to each class and is less dominated by majority-class performance than raw accuracy.

The internal performance comparison is reported in Table 2 and Figure 2.

### 2.6 Calibration and probabilistic evaluation

Calibration was evaluated because classification accuracy alone does not indicate whether predicted confidence values are reliable [REF-CAL-001; REF-CAL-002]. The calibration analysis included expected calibration error, negative log-likelihood, Brier score, and confidence-accuracy gap [REF-CAL-001; REF-CAL-002; REF-CAL-003].

Post-hoc temperature scaling was applied using validation logits. A single scalar temperature was learned and then applied to the D1 test logits and D3B shifted-domain logits. This procedure was used to test whether confidence calibration improved without changing the predicted class labels [REF-CAL-001].

Internal calibration results are reported in Table 3 and Figure 3.

### 2.7 D3B shifted-domain evaluation

D3B was evaluated as a glioma-focused shifted-domain dataset. Because all selected D3B samples came from a glioma-focused source, the main shifted-domain question was not four-class accuracy. Instead, the analysis examined whether D1-trained models assigned D3B images to the glioma class and how confident the models were under this shift.

The D3B analysis included slice-level glioma prediction rate, patient-majority glioma prediction rate, series-majority glioma prediction rate, mean glioma probability, median glioma probability, mean maximum confidence, and entropy. These metrics were used to describe shifted-domain behaviour without overstating D3B as a full external validation dataset.

D3B shifted-domain results are reported in Table 4 and Figures 4–5.

### 2.8 Temperature-scaled D3B confidence analysis

The temperature values learned from D1 validation logits were also applied to D3B logits. This tested whether internal calibration adjustment softened model confidence under shifted-domain conditions. Because temperature scaling does not change class ranking, it was expected to affect confidence values and entropy but not predicted class labels.

Temperature-scaled D3B confidence results are reported in Table 5 and Figure 6.

### 2.9 Reproducibility and reporting

All major outputs were generated from saved experiment artifacts. Summary tables, figures, and audits were generated using scripts stored in the repository. The project includes dataset usage decisions, overlap audit outputs, model comparison summaries, manuscript asset indexes, and citation-integrity tracking. This structure was used to improve transparency and reduce the risk of unsupported manuscript claims [REF-REPORT-001; REF-REPORT-002].
## 3. Results

### 3.1 Dataset integrity and overlap auditing

The initial D1 dataset was prepared using a leakage-aware workflow. Exact duplicate analysis was performed before model evaluation, and the final D1 split was constructed to reduce the risk of duplicate leakage between training, validation, and test subsets.

D2 was initially considered as an external validation candidate. However, exact and perceptual overlap auditing revealed substantial overlap between D1 and D2. As a result, D2 was rejected as a clean independent external validation dataset. This finding is methodologically important because it demonstrates that public brain MRI benchmark datasets may not be independent even when they are distributed as separate sources.

D3B, derived from ICDC-Glioma, was therefore selected as a visually distinct glioma-focused domain-shift dataset [REF-SHIFT-001; REF-SHIFT-002]. The usage decision for D1, D2, and D3B is summarised in Table 1 [REF-LEAK-001; REF-LEAK-003; REF-LEAK-004]. Selected DICOM series were downloaded, inspected, converted into reproducible central 2D slices, and audited against D1 using exact and perceptual hash checks. No exact or pHash near-overlap was detected between D1 and D3B under the selected threshold. D3B was therefore used for glioma-focused domain-shift analysis. However, because D3B does not contain the same four-class label structure as D1, it was not treated as a full four-class external validation dataset.

### 3.2 Internal D1 model performance

Three architectures were trained and evaluated on the D1 leakage-aware split: ResNet18, EfficientNet-B0, and ViT-B/16.

All three models achieved strong internal test performance (Table 2; Figure 2). ResNet18 achieved a test macro-F1 of 0.9666. EfficientNet-B0 achieved the strongest internal result, with a test macro-F1 of 0.9680. ViT-B/16 achieved a lower but still high test macro-F1 of 0.9582.

These findings show that high internal classification performance is achievable even after duplicate-aware splitting. However, internal performance alone does not establish cross-dataset reliability.

### 3.3 Internal calibration and temperature scaling

Before temperature scaling, all three models showed mild overconfidence on the D1 test set. ResNet18 had a confidence-accuracy gap of 0.0169, EfficientNet-B0 had a gap of 0.0135, and ViT-B/16 had a gap of 0.0159.

Post-hoc temperature scaling improved internal calibration for all three models without changing accuracy or macro-F1 (Table 3; Figure 3) [REF-CAL-001]. ResNet18 ECE decreased from 0.0208 to 0.0145. EfficientNet-B0 ECE decreased from 0.0186 to 0.0152. ViT-B/16 ECE decreased from 0.0198 to 0.0109.

These results show that temperature scaling improved confidence calibration on the internal D1 distribution. However, this improvement does not necessarily imply robustness to dataset shift.

### 3.4 D3B domain-shift prediction behaviour

All three D1-trained models showed unstable prediction behaviour on D3B.

ResNet18 predicted glioma for only 29.43% of D3B slices and 26.42% of patients by majority vote (Table 4; Figure 4) [REF-SHIFT-001; REF-SHIFT-002]. EfficientNet-B0 performed better, predicting glioma for 44.15% of slices and 47.17% of patients by majority vote. ViT-B/16 predicted glioma for 40.38% of slices and 37.74% of patients by majority vote. The full D3B prediction distribution is shown in Figure 5.

Although EfficientNet-B0 showed the strongest D3B glioma recognition among the tested models, none of the models predicted glioma for a majority of D3B slices. This indicates that high internal D1 performance did not translate into stable glioma-domain behaviour on visually distinct D3B images.

### 3.5 Temperature scaling under D3B shift

Temperature scaling softened model confidence under D3B shift for all three architectures (Table 5; Figure 6) [REF-CAL-001; REF-SHIFT-001]. Mean maximum confidence decreased and entropy increased after applying the learned temperature values.

However, temperature scaling did not change the predicted class distribution or patient-majority predictions. This is important because it shows that the D3B failure was not merely a calibration problem. The unstable prediction distribution reflects domain-shift sensitivity in the learned representations.

### 3.6 Cross-model comparison

Across the three architectures, EfficientNet-B0 achieved the best internal D1 performance and the strongest D3B glioma prediction rate. ResNet18 and ViT-B/16 also achieved high internal performance, but both showed weaker D3B glioma-domain recognition.

The transformer-based ViT-B/16 did not outperform the CNN baselines in this experimental setting. This does not prove that transformers are generally inferior for brain MRI tumour classification, but it does show that architecture choice alone is insufficient to guarantee reliability under dataset shift.

## 4. Discussion

### 4.1 Principal finding

This study shows that high internal classification performance is not sufficient evidence of reliability in brain MRI tumour classification. Across ResNet18, EfficientNet-B0, and ViT-B/16, all models achieved strong internal performance on the leakage-aware D1 test split, yet none maintained stable glioma-domain prediction behaviour on visually distinct D3B images.

This finding directly challenges the common assumption that high test accuracy on public brain MRI datasets is enough to support reliability claims. Even when duplicate leakage was controlled and internal calibration was improved using temperature scaling, the models remained unstable under cross-dataset shift.

### 4.2 Internal performance can hide external fragility

The internal D1 results were strong across all three architectures. EfficientNet-B0 achieved the highest internal macro-F1, followed closely by ResNet18, while ViT-B/16 remained slightly lower but still high.

If this study had stopped at internal accuracy and macro-F1, the models would appear highly reliable. However, the D3B evaluation showed a different picture. ResNet18 predicted glioma for only 29.43% of D3B slices, EfficientNet-B0 for 44.15%, and ViT-B/16 for 40.38%.

This means that internal performance substantially overestimated model reliability under domain shift.

### 4.3 Dataset overlap auditing is essential

One of the most important methodological findings was the rejection of D2 as an external validation dataset. D2 initially appeared useful as an external candidate, but exact and perceptual overlap auditing revealed substantial D1-D2 overlap.

This matters because many medical imaging studies treat public datasets as independent simply because they have different names or sources. This study shows that such an assumption is unsafe. Without overlap auditing, an apparently external evaluation may actually contain reused or visually duplicated samples, leading to inflated generalisation claims.

Therefore, dataset independence should be treated as an empirical question, not an assumption.

### 4.4 Calibration improved confidence but did not solve domain shift

Temperature scaling improved internal calibration for all three models. It reduced ECE, reduced confidence-accuracy gaps, and improved negative log-likelihood. This confirms that post-hoc calibration is useful for improving confidence quality on the internal distribution.

However, temperature scaling did not correct the D3B prediction distribution. The class predictions and patient-majority behaviour remained unchanged after scaling. This is expected because temperature scaling modifies probability sharpness but does not change the learned feature representation.

This distinction is important. Calibration can make confidence values less extreme, but it cannot force a model to learn domain-invariant tumour features after training. Therefore, calibration should not be presented as a solution to dataset shift.

### 4.5 Architecture alone did not solve reliability

EfficientNet-B0 performed best overall, both internally and on D3B. However, even EfficientNet-B0 failed to predict glioma for a majority of D3B slices. ViT-B/16 did not outperform the CNN baselines and showed substantial D3B instability, including frequent notumor predictions on glioma-domain images.

This weakens any simplistic claim that transformer-based models are inherently more reliable than CNNs. Architecture may improve performance, but reliability depends on data quality, dataset independence, calibration, and robustness under shift.

### 4.6 Limitations

D3B is not a full four-class external validation dataset. It is a glioma-focused domain-shift dataset. Therefore, the D3B results should not be described as four-class external accuracy.

D3B labels are collection-level glioma labels rather than slice-level tumour annotations. The central-slice conversion strategy is reproducible, but it does not guarantee that every selected slice contains visible tumour tissue.

Only three architectures were evaluated. Additional architectures, including DenseNet, Swin Transformer, ConvNeXt, and uncertainty-aware models, may produce different results.

This study evaluates prediction behaviour and confidence under dataset shift. It does not establish clinical diagnostic validity.

## 5. Conclusion

This study demonstrates that high internal classification performance does not guarantee reliable behaviour under dataset shift. Three D1-trained models — ResNet18, EfficientNet-B0, and ViT-B/16 — achieved strong internal test performance on a leakage-aware brain MRI tumour classification split. However, none maintained stable glioma-domain prediction behaviour on visually distinct D3B images.

The results also show that calibration and domain-shift robustness are different problems. Post-hoc temperature scaling improved internal calibration and softened confidence under D3B shift, but it did not correct unstable prediction distributions. This means calibration is useful but insufficient as a standalone reliability solution.

A major methodological finding was that one candidate external dataset, D2, could not be treated as clean independent evidence because it showed substantial overlap with D1. This highlights the importance of dataset overlap auditing before making external validation claims.

The strongest defensible conclusion is that brain MRI tumour classifiers should not be judged by internal accuracy alone. Reliability-focused evaluation requires duplicate-aware splitting, dataset independence checks, calibration assessment, and domain-shift testing. Without these steps, reported performance may overstate the real reliability of medical image classification models.


## Manuscript Assets

Generated manuscript-ready tables are stored in `reports/experiments/tables/`. Generated figures are stored in `reports/experiments/figures/`. Captions are stored in `reports/experiments/figure_captions.md` and `reports/experiments/table_captions.md`.
