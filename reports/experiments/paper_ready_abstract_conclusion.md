# Paper-Ready Abstract and Conclusion Draft

## Abstract

Deep learning models for brain MRI tumour classification often report high internal accuracy on public benchmark datasets, but high accuracy alone may not establish clinical or cross-dataset reliability. This study evaluated whether internally high-performing brain MRI tumour classifiers remain reliable when assessed using leakage-aware splitting, calibration analysis, dataset overlap auditing, and glioma-focused domain-shift testing.

Three architectures were trained on a leakage-aware split of a public four-class brain MRI tumour dataset: ResNet18, EfficientNet-B0, and ViT-B/16. Internal performance was assessed using accuracy, balanced accuracy, and macro-F1. Calibration was evaluated using confidence-accuracy gap, expected calibration error, Brier score, and negative log-likelihood, with post-hoc temperature scaling fitted on validation logits only. Candidate external datasets were audited for exact and perceptual overlap. One candidate dataset was rejected because of substantial overlap with the training dataset. A visually distinct glioma-focused DICOM dataset, D3B, was selected, converted into reproducible central 2D slices, and used for domain-shift confidence and prediction-distribution analysis.

All three models achieved high internal test performance. EfficientNet-B0 achieved the strongest internal result, followed closely by ResNet18, while ViT-B/16 performed slightly worse. Temperature scaling improved internal calibration for all models without changing classification performance. However, all models showed unstable behaviour on D3B. ResNet18 predicted glioma for 29.43% of D3B slices, EfficientNet-B0 for 44.15%, and ViT-B/16 for 40.38%. Temperature scaling softened confidence under D3B shift but did not change predicted class distributions or patient-majority behaviour.

These findings show that high internal performance and improved internal calibration are insufficient evidence of cross-dataset reliability. Brain MRI tumour classification studies should include leakage-aware splitting, dataset overlap auditing, calibration analysis, and domain-shift evaluation before making reliability claims.

## Keywords

Brain MRI; tumour classification; calibration; temperature scaling; dataset shift; leakage; reliability; deep learning; external validation; uncertainty

## Conclusion

This study demonstrates that high internal classification performance does not guarantee reliable behaviour under dataset shift. Three D1-trained models — ResNet18, EfficientNet-B0, and ViT-B/16 — achieved strong internal test performance on a leakage-aware brain MRI tumour classification split. However, none maintained stable glioma-domain prediction behaviour on visually distinct D3B images.

The results also show that calibration and domain-shift robustness are different problems. Post-hoc temperature scaling improved internal calibration and softened confidence under D3B shift, but it did not correct unstable prediction distributions. This means calibration is useful but insufficient as a standalone reliability solution.

A major methodological finding was that one candidate external dataset, D2, could not be treated as clean independent evidence because it showed substantial overlap with D1. This highlights the importance of dataset overlap auditing before making external validation claims.

The strongest defensible conclusion is that brain MRI tumour classifiers should not be judged by internal accuracy alone. Reliability-focused evaluation requires duplicate-aware splitting, dataset independence checks, calibration assessment, and domain-shift testing. Without these steps, reported performance may overstate the real reliability of medical image classification models.

## Strongest Conservative Thesis Statement

A leakage-aware, calibration-aware, cross-dataset evaluation pipeline showed that three high-performing D1-trained brain MRI tumour classifiers did not maintain stable glioma-domain prediction behaviour on visually distinct D3B images. Post-hoc temperature scaling improved confidence softness but did not correct prediction distribution under dataset shift.

## One-Sentence Contribution Statement

This study contributes a reproducible reliability-first evaluation pipeline showing that internal accuracy and calibration alone are insufficient evidence of cross-dataset reliability in brain MRI tumour classification.

## Manuscript-Style Final Conclusion Paragraph

In conclusion, this study provides evidence that strong internal performance on public brain MRI tumour datasets can mask substantial fragility under dataset shift. Across three architectures, high D1 test performance did not translate into stable glioma-domain behaviour on visually distinct D3B images. Although temperature scaling improved calibration metrics, it did not change the underlying prediction distribution under shift. These findings support a reliability-first evaluation framework in which accuracy, calibration, leakage auditing, and domain-shift testing are considered together before claims of robustness or clinical reliability are made.
