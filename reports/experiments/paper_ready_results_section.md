# Paper-Ready Results Section Draft

## Results

### Dataset integrity and overlap auditing

The initial D1 dataset was prepared using a leakage-aware workflow. Exact duplicate analysis was performed before model evaluation, and the final D1 split was constructed to reduce the risk of duplicate leakage between training, validation, and test subsets.

A second public dataset, D2, was initially considered as an external validation candidate. However, exact and perceptual overlap auditing revealed substantial overlap between D1 and D2. As a result, D2 was rejected as a clean independent external validation dataset. This finding is methodologically important because it demonstrates that public brain MRI benchmark datasets may not be independent even when they are distributed as separate sources.

D3B, derived from ICDC-Glioma, was therefore selected as a visually distinct glioma-focused domain-shift dataset. Selected DICOM series were downloaded, inspected, converted into reproducible central 2D slices, and audited against D1 using exact and perceptual hash checks. No exact or pHash near-overlap was detected between D1 and D3B under the selected threshold. D3B was therefore used for glioma-focused domain-shift analysis. However, because D3B does not contain the same four-class label structure as D1, it was not treated as a full four-class external validation dataset.

### Internal D1 model performance

Three architectures were trained and evaluated on the D1 leakage-aware split: ResNet18, EfficientNet-B0, and ViT-B/16.

All three models achieved strong internal test performance. ResNet18 achieved a test macro-F1 of 0.9666. EfficientNet-B0 achieved the strongest internal result, with a test macro-F1 of 0.9680. ViT-B/16 achieved a lower but still high test macro-F1 of 0.9582.

These findings show that high internal classification performance is achievable even after duplicate-aware splitting. However, internal performance alone does not establish cross-dataset reliability.

### Internal calibration and temperature scaling

Before temperature scaling, all three models showed mild overconfidence on the D1 test set. ResNet18 had a confidence-accuracy gap of 0.0169, EfficientNet-B0 had a gap of 0.0135, and ViT-B/16 had a gap of 0.0159.

Post-hoc temperature scaling improved internal calibration for all three models without changing accuracy or macro-F1. ResNet18 ECE decreased from 0.0193 to 0.0145. EfficientNet-B0 ECE decreased from 0.0186 to 0.0152. ViT-B/16 ECE decreased from 0.0198 to 0.0109.

These results show that temperature scaling improved confidence calibration on the internal D1 distribution. However, this improvement does not necessarily imply robustness to dataset shift.

### D3B domain-shift prediction behaviour

All three D1-trained models showed unstable prediction behaviour on D3B.

ResNet18 predicted glioma for only 29.43% of D3B slices and 26.42% of patients by majority vote. EfficientNet-B0 performed better, predicting glioma for 44.15% of slices and 47.17% of patients by majority vote. ViT-B/16 predicted glioma for 40.38% of slices and 37.74% of patients by majority vote.

Although EfficientNet-B0 showed the strongest D3B glioma recognition among the tested models, none of the models predicted glioma for a majority of D3B slices. This indicates that high internal D1 performance did not translate into stable glioma-domain behaviour on visually distinct D3B images.

### Temperature scaling under D3B shift

Temperature scaling softened model confidence under D3B shift for all three architectures. Mean maximum confidence decreased and entropy increased after applying the learned temperature values.

However, temperature scaling did not change the predicted class distribution or patient-majority predictions. This is important because it shows that the D3B failure was not merely a calibration problem. The unstable prediction distribution reflects domain-shift sensitivity in the learned representations.

### Cross-model comparison

Across the three architectures, EfficientNet-B0 achieved the best internal D1 performance and the strongest D3B glioma prediction rate. ResNet18 and ViT-B/16 also achieved high internal performance, but both showed weaker D3B glioma-domain recognition.

The transformer-based ViT-B/16 did not outperform the CNN baselines in this experimental setting. This does not prove that transformers are generally inferior for brain MRI tumour classification, but it does show that architecture choice alone is insufficient to guarantee reliability under dataset shift.

### Main finding

The central finding is that high internal accuracy and improved internal calibration are insufficient evidence of cross-dataset reliability. Across three model architectures, strong D1 test performance did not guarantee stable prediction behaviour on visually distinct D3B glioma-domain images.

Post-hoc temperature scaling improved confidence softness but did not correct the D3B prediction distribution. Therefore, calibration should be treated as one component of reliability evaluation, not as a substitute for independent dataset auditing and domain-shift testing.

### Conservative interpretation

A leakage-aware, calibration-aware, cross-dataset evaluation pipeline showed that three high-performing D1-trained brain MRI tumour classifiers did not maintain stable glioma-domain prediction behaviour on visually distinct D3B images. This supports the argument that standard internal accuracy reporting is insufficient for reliability claims in medical image classification.

### Limitations

D3B is glioma-focused and does not support full four-class external accuracy evaluation.

D3B labels are collection-level glioma labels rather than slice-level tumour annotations.

Only three architectures were evaluated.

The study evaluates model prediction behaviour and confidence under dataset shift, not clinical diagnostic validity.

The D3B central-slice conversion strategy is reproducible but does not guarantee tumour-containing slices.

### Summary

The results support a reliability-first evaluation framework for brain MRI tumour classification. Dataset leakage auditing, calibration analysis, and domain-shift evaluation provide evidence that cannot be captured by internal accuracy alone.
