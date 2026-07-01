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

## 3. Results

### 3.1 Dataset audit and usage decisions

The dataset audit directly affected the experimental design. D1 was retained as the primary four-class dataset for internal training, validation, and testing. D2 was rejected as a clean external validation dataset after exact and perceptual overlap auditing showed substantial overlap with D1. This prevented D2 from being used in a way that could falsely strengthen external-validation claims.

D3B was retained as a visually distinct glioma-focused shifted-domain dataset. The D1-D3B audit found no exact or perceptual near-overlap under the selected threshold. However, because D3B did not reproduce the four-class label structure of D1, it was used only for glioma-focused shifted-domain prediction and confidence analysis, not full four-class external accuracy estimation.

The final dataset usage decisions are summarised in Table 1.

### 3.2 Internal D1 model performance

All three models achieved strong internal D1 test performance (Table 2; Figure 2). EfficientNet-B0 achieved the strongest internal classification result, with a test accuracy of 0.9676, balanced accuracy of 0.9677, and macro-F1 of 0.9680. ResNet18 performed similarly, with a test accuracy of 0.9667, balanced accuracy of 0.9662, and macro-F1 of 0.9666. ViT-B/16 achieved slightly lower internal performance, with a test accuracy of 0.9581, balanced accuracy of 0.9578, and macro-F1 of 0.9582.

These results show that high internal classification performance was achievable on D1 across convolutional and transformer-based architectures. However, the differences between models were small on the internal test set, and internal performance alone did not establish shifted-domain reliability.

### 3.3 Internal calibration and temperature scaling

Before temperature scaling, all three models showed mild overconfidence on the D1 test set (Table 3; Figure 3). ResNet18 had an expected calibration error of 0.0208, EfficientNet-B0 had an expected calibration error of 0.0186, and ViT-B/16 had an expected calibration error of 0.0198.

Post-hoc temperature scaling improved calibration for all three models without changing their classification predictions [REF-CAL-001]. ResNet18 ECE decreased from 0.0208 to 0.0145. EfficientNet-B0 ECE decreased from 0.0186 to 0.0152. ViT-B/16 ECE decreased from 0.0198 to 0.0109. Negative log-likelihood and confidence-accuracy gap also decreased for all models after temperature scaling.

The learned temperatures were 1.2328 for ResNet18, 1.1596 for EfficientNet-B0, and 1.2363 for ViT-B/16. These values indicate that the models required confidence softening rather than sharpening.

### 3.4 D3B shifted-domain prediction behaviour

The D3B shifted-domain evaluation showed a clear divergence between strong internal D1 performance and glioma-focused shifted-domain behaviour (Table 4; Figures 4–5) [REF-SHIFT-001; REF-SHIFT-002]. Although D3B was glioma-focused, none of the models consistently predicted glioma across the selected D3B slices.

ResNet18 predicted glioma for 29.43% of D3B slices and 26.42% of patients by majority vote. EfficientNet-B0 predicted glioma for 44.15% of slices and 47.17% of patients by majority vote. ViT-B/16 predicted glioma for 40.38% of slices and 37.74% of patients by majority vote.

EfficientNet-B0 showed the highest D3B glioma prediction rate among the three models, but it still predicted glioma for fewer than half of D3B patients by majority vote. This is important because EfficientNet-B0 also had the strongest internal D1 macro-F1. Therefore, the internally strongest model was not reliably consistent under the D3B shifted-domain test.

### 3.5 D3B confidence behaviour

The D3B confidence analysis showed that the models remained confident under shifted-domain conditions despite unstable class behaviour. Before temperature scaling, mean maximum confidence on D3B was 0.7209 for ResNet18, 0.6837 for EfficientNet-B0, and 0.7203 for ViT-B/16. Mean entropy was 0.7157 for ResNet18, 0.7970 for EfficientNet-B0, and 0.6748 for ViT-B/16.

These values show that the models did not simply become uniformly uncertain on D3B. Instead, they often made confident predictions even when glioma-focused D3B images were assigned to non-glioma classes. This supports the need to assess confidence behaviour alongside class predictions.

### 3.6 Temperature-scaled D3B confidence behaviour

Temperature scaling softened confidence under D3B shift for all three models (Table 5; Figure 6). Mean maximum confidence decreased from 0.7209 to 0.6678 for ResNet18, from 0.6837 to 0.6451 for EfficientNet-B0, and from 0.7203 to 0.6710 for ViT-B/16. Mean entropy increased from 0.7157 to 0.8363 for ResNet18, from 0.7970 to 0.8838 for EfficientNet-B0, and from 0.6748 to 0.7913 for ViT-B/16.

However, temperature scaling did not change the predicted class labels. The D3B glioma prediction rates remained unchanged after scaling. Therefore, temperature scaling improved confidence softness but did not correct shifted-domain class behaviour.

### 3.7 Summary of main empirical findings

The results support four main findings. First, all three models achieved high internal D1 performance. Second, temperature scaling improved internal calibration. Third, D2 was not suitable as clean external validation because overlap auditing revealed substantial overlap with D1. Fourth, D3B shifted-domain evaluation showed that high internal performance and improved calibration did not guarantee stable glioma prediction behaviour under dataset shift.

Taken together, these findings support the central argument of the study: internal accuracy is insufficient evidence of reliability for brain MRI tumour classification models.
## 4. Discussion

## 4. Discussion

### 4.1 Principal findings

This study evaluated brain MRI tumour classification models using a reliability-first framework rather than relying on internal accuracy alone. The main finding is that high internal D1 performance did not translate into stable glioma-focused shifted-domain behaviour on D3B. All three models achieved strong internal macro-F1 scores, and temperature scaling improved internal calibration. However, D3B evaluation showed that the models frequently failed to assign glioma-focused D3B images to the glioma class.

This result supports the central argument that internal classification performance is not sufficient evidence of reliability in medical imaging AI [REF-SHIFT-001; REF-SHIFT-002; REF-REPORT-001]. A model can perform well on an internal held-out test set while still behaving inconsistently when evaluated on visually distinct data from a different source.

### 4.2 Importance of leakage and overlap auditing

A major methodological finding was the rejection of D2 as a clean external validation dataset. Although D2 initially appeared suitable as an external benchmark, exact and perceptual overlap auditing revealed substantial overlap with D1. Using D2 as external validation would therefore have risked overstating generalisation.

This is important because public medical imaging datasets are often reused, repackaged, or redistributed in ways that are not obvious from dataset names alone. Without overlap auditing, apparent external validation can become contaminated validation [REF-LEAK-001; REF-LEAK-002; REF-LEAK-003]. In this study, the D2 rejection strengthened the experimental design by preventing a misleading external-validation claim.

### 4.3 Internal performance versus shifted-domain behaviour

EfficientNet-B0 achieved the strongest internal D1 result, with the highest macro-F1 among the three architectures. However, it predicted glioma for fewer than half of D3B patients by majority vote. This shows that the internally strongest model was not necessarily reliable under the D3B shifted-domain test.

The result should not be interpreted as proof that EfficientNet-B0 is unreliable in all settings, nor that ViT-B/16 or ResNet18 are generally inferior. The more defensible interpretation is narrower: under this specific D1-to-D3B evaluation, high internal performance did not guarantee stable shifted-domain glioma prediction behaviour.

### 4.4 Calibration and temperature scaling

Temperature scaling improved internal calibration for all three models. Expected calibration error, negative log-likelihood, Brier score, and confidence-accuracy gap decreased after scaling. This confirms that post-hoc calibration can improve confidence quality without changing predicted labels [REF-CAL-001; REF-CAL-002; REF-CAL-003].

However, temperature scaling did not correct shifted-domain class behaviour on D3B. The D3B glioma prediction rates remained unchanged after scaling because temperature scaling changes probability softness but not class ranking. This distinction is important: calibration can improve the reliability of confidence estimates, but it does not automatically solve dataset shift or class-mapping instability [REF-SHIFT-001; REF-SHIFT-002].

### 4.5 Interpretation of D3B findings

D3B was used as a glioma-focused shifted-domain dataset, not as a full four-class external validation set. This distinction is critical. Because D3B does not reproduce the D1 label structure, this study cannot report conventional four-class external accuracy on D3B.

The valid interpretation is that D1-trained models showed unstable glioma-focused prediction behaviour when applied to a visually distinct glioma-domain source. This is still useful evidence, but it is not the same as full external validation. The manuscript should therefore avoid claiming clinical generalisation, deployment readiness, or external diagnostic validity.

### 4.6 Relationship to uncertainty-aware modelling

This study evaluated calibration and confidence behaviour, but it did not implement full uncertainty-aware methods such as Monte Carlo dropout, deep ensembles, Bayesian neural networks, or evidential learning. Calibration and uncertainty are related but not identical. A model may be calibrated on an internal test set while still failing to express useful uncertainty under dataset shift.

Future work should evaluate uncertainty-aware methods under the same leakage-aware and shifted-domain conditions used here [REF-UNC-001; REF-UNC-002; REF-UNC-003; REF-UNC-004; REF-UNC-005]. In particular, future experiments should test whether uncertainty-aware methods can identify shifted or unreliable inputs more effectively than temperature scaling alone.

### 4.7 Strengths

The main strength of this study is its conservative evaluation design. The project did not treat high internal accuracy as sufficient evidence of reliability. Instead, it combined duplicate auditing, public dataset overlap checks, internal performance evaluation, calibration analysis, temperature scaling, and shifted-domain testing.

Another strength is reproducibility. Tables and figures were generated from saved experiment artifacts, and the project includes explicit audit files, manuscript asset indexes, citation tracking, and dataset usage decisions. This reduces the risk of unsupported or manually altered result reporting.

### 4.8 Limitations

This study has several limitations. First, D3B is glioma-focused and cannot support full four-class external accuracy estimation. Second, the D3B analysis used selected central slices rather than full volumetric modelling. Third, only three architectures were evaluated. Fourth, temperature scaling was the only post-hoc calibration method tested. Fifth, the study did not yet implement full uncertainty-aware approaches such as ensembles or Monte Carlo dropout.

The findings should therefore be interpreted as evidence of reliability limitations under the current experimental design, not as a complete assessment of all possible brain MRI tumour classification models.

### 4.9 Implications

The results suggest that brain MRI tumour classification studies should report more than internal accuracy. At minimum, future studies should include leakage-aware splitting, duplicate and overlap audits, calibration metrics, and carefully described external or shifted-domain evaluation. Candidate external datasets should not be assumed independent without evidence.

For clinical translation, the evidence threshold would be much higher. Prospective validation, site-diverse testing, transparent reporting, and clinically meaningful evaluation protocols would be required before any deployment claim could be justified [REF-REPORT-001; REF-REPORT-002; REF-REPORT-003].
## 5. Conclusion

This study demonstrates that high internal classification performance does not guarantee reliable behaviour under dataset shift. Three D1-trained models — ResNet18, EfficientNet-B0, and ViT-B/16 — achieved strong internal test performance on a leakage-aware brain MRI tumour classification split. However, none maintained stable glioma-domain prediction behaviour on visually distinct D3B images.

The results also show that calibration and domain-shift robustness are different problems. Post-hoc temperature scaling improved internal calibration and softened confidence under D3B shift, but it did not correct unstable prediction distributions. This means calibration is useful but insufficient as a standalone reliability solution.

A major methodological finding was that one candidate external dataset, D2, could not be treated as clean independent evidence because it showed substantial overlap with D1. This highlights the importance of dataset overlap auditing before making external validation claims.

The strongest defensible conclusion is that brain MRI tumour classifiers should not be judged by internal accuracy alone. Reliability-focused evaluation requires duplicate-aware splitting, dataset independence checks, calibration assessment, and domain-shift testing. Without these steps, reported performance may overstate the real reliability of medical image classification models.


## Manuscript Assets

Generated manuscript-ready tables are stored in `reports/experiments/tables/`. Generated figures are stored in `reports/experiments/figures/`. Captions are stored in `reports/experiments/figure_captions.md` and `reports/experiments/table_captions.md`.
