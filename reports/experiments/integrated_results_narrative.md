# Integrated Results Narrative

## 1. Overview

This study evaluated whether high internal classification performance on a leakage-aware brain MRI tumour dataset is sufficient evidence of model reliability. Three architectures were tested: ResNet18, EfficientNet-B0, and ViT-B/16.

The evaluation focused on internal D1 performance, calibration behaviour, dataset overlap auditing, and glioma-focused domain-shift behaviour on D3B.

## 2. D1 Internal Performance

All three models achieved high internal performance on the D1 leakage-aware test split. EfficientNet-B0 achieved the strongest internal result, followed closely by ResNet18. ViT-B/16 performed slightly worse than both CNN baselines.

This shows that strong internal accuracy is achievable even when duplicate leakage is controlled. However, internal performance alone does not establish external reliability.

## 3. Internal Calibration

All three models were slightly overconfident on the D1 test set before temperature scaling. Temperature scaling improved calibration metrics for all models without changing accuracy or macro-F1.

This supports the use of post-hoc calibration as a useful internal reliability tool. However, calibration improvement on the same dataset distribution should not be treated as evidence of robustness to dataset shift.

## 4. D2 Dataset Rejection

D2 was initially considered as an external validation candidate. However, exact and perceptual overlap auditing revealed substantial D1-D2 overlap.

Because of this overlap, D2 could not be treated as a clean independent external dataset. This was a critical methodological finding because it showed that public benchmark datasets may not be independent even when they appear to come from different sources.

## 5. D3B Dataset Construction

D3B was selected as a visually distinct glioma-focused domain-shift dataset. Selected DICOM series were downloaded, inspected, converted into central 2D slices, and audited against D1 using exact and perceptual hash checks.

No exact or near-overlap was detected between D1 and D3B. Therefore, D3B was suitable for glioma-focused domain-shift analysis, but not for full four-class external accuracy because it does not contain the same four-class label structure as D1.

## 6. D3B Domain-Shift Behaviour

All three D1-trained models showed unstable prediction behaviour on D3B.

ResNet18 predicted glioma for only 29.43% of D3B slices. EfficientNet-B0 improved this to 44.15%, while ViT-B/16 predicted glioma for 40.38% of D3B slices.

Although EfficientNet-B0 performed best under D3B shift, none of the models predicted glioma for a majority of D3B slices. This shows that high internal performance did not translate into stable external glioma-domain behaviour.

## 7. Temperature Scaling Under D3B Shift

Temperature scaling softened confidence values on D3B for all models. Mean maximum confidence decreased and entropy increased.

However, temperature scaling did not change the class prediction distribution or patient-majority behaviour. Therefore, the D3B failure was not merely a calibration issue. It reflected domain-shift sensitivity in the learned feature representations.

## 8. Main Finding

The central finding is that internal accuracy and internal calibration are insufficient evidence of cross-dataset reliability.

A model can perform well on a leakage-aware internal test set and still behave unstably when evaluated on visually distinct MRI data from a different source.

## 9. Conservative Claim

A leakage-aware, calibration-aware, cross-dataset evaluation pipeline showed that three high-performing D1-trained models did not maintain stable glioma-domain prediction behaviour on visually distinct D3B images. Post-hoc temperature scaling improved confidence softness but did not correct prediction distribution under dataset shift.

## 10. Limitations

D3B is glioma-focused and does not support full four-class external accuracy evaluation.

The D3B labels are collection-level glioma labels rather than slice-level tumour annotations.

Only three architectures were tested.

The analysis evaluates prediction behaviour and confidence under domain shift, not clinical diagnostic validity.

## 11. Implication

Brain MRI tumour classification studies should not rely on internal accuracy alone. Reliability claims require leakage-aware splitting, dataset overlap auditing, calibration analysis, and external or domain-shift evaluation.
