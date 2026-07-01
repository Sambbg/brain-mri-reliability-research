# Paper-Ready Introduction Section Draft

## Introduction

Deep learning has become widely used for brain MRI tumour classification, with many studies reporting high accuracy on public benchmark datasets. Convolutional neural networks, transformer-based models, and hybrid architectures have all been applied to classify tumour types such as glioma, meningioma, pituitary tumour, and no tumour. These reported results often suggest strong diagnostic potential.

However, high internal accuracy alone is not sufficient evidence of reliability. In medical imaging, a model may perform well on an internal test split while still failing under dataset shift, scanner variation, acquisition differences, image preprocessing differences, or hidden overlap between public datasets. This is especially important in brain MRI tumour classification, where public datasets are frequently reused, redistributed, augmented, or combined without rigorous independence auditing.

A major weakness in many classification studies is the assumption that test performance on a public dataset reflects generalisable reliability. This assumption may be unsafe for several reasons. First, duplicate or near-duplicate images can leak between training and test partitions. Second, datasets presented as separate sources may still contain overlapping images. Third, standard accuracy, precision, recall, and F1-score do not measure whether predicted confidence is calibrated. Fourth, internal calibration does not guarantee robustness under external dataset shift.

Calibration is particularly important in medical imaging because a model's confidence may influence how predictions are interpreted. A classifier that is highly accurate but overconfident may still be unreliable in uncertain or shifted conditions. Post-hoc calibration methods such as temperature scaling can improve the relationship between confidence and correctness on an internal validation or test distribution. However, calibration does not change the model's learned features and may not solve domain-shift failure.

Therefore, reliability evaluation should go beyond internal accuracy. A stronger evaluation should include leakage-aware splitting, duplicate and overlap auditing, calibration analysis, and external or domain-shift testing. These steps are necessary before making claims about robustness, generalisation, or clinical usefulness.

This study evaluates brain MRI tumour classification models using a reliability-first pipeline. Three architectures were tested: ResNet18, EfficientNet-B0, and ViT-B/16. Each model was trained on the same leakage-aware D1 split and evaluated internally using classification and calibration metrics. Temperature scaling was applied using validation-set logits only. Candidate external datasets were audited for exact and perceptual overlap. One candidate dataset, D2, was rejected because of substantial overlap with D1. A visually distinct glioma-focused DICOM dataset, D3B, was selected, converted into reproducible central 2D slices, and used for domain-shift confidence and prediction-distribution analysis.

The central research question is whether high-performing brain MRI tumour classifiers remain reliable when evaluated beyond internal accuracy, using leakage-aware splitting, calibration, overlap auditing, and domain-shift testing.

The main contribution of this study is a reproducible evaluation pipeline showing that strong internal performance and improved internal calibration do not necessarily imply stable cross-dataset behaviour. Across three architectures, models achieved high internal D1 performance but failed to maintain stable glioma-domain prediction behaviour on visually distinct D3B images. This supports the argument that brain MRI tumour classification studies should not rely on internal accuracy alone when making reliability claims.

## Research Gap

Existing brain MRI tumour classification studies commonly report high internal performance on public datasets, but many do not sufficiently address dataset leakage, dataset overlap, calibration quality, or domain-shift behaviour.

The key gap addressed in this study is the lack of a reproducible, reliability-focused evaluation workflow that combines:

1. Leakage-aware dataset splitting.
2. Duplicate and overlap auditing.
3. Internal calibration analysis.
4. Post-hoc temperature scaling.
5. Cross-dataset or domain-shift evaluation.
6. Conservative interpretation of external evidence.

## Research Question

How reliable are deep learning-based brain MRI tumour classification models when evaluated using leakage-aware splitting, calibration analysis, dataset overlap auditing, and glioma-focused domain-shift testing?

## Aim

To evaluate whether high internal brain MRI tumour classification performance translates into reliable prediction behaviour under calibration assessment and dataset shift.

## Objectives

1. Prepare a leakage-aware D1 brain MRI tumour classification split.
2. Train and evaluate ResNet18, EfficientNet-B0, and ViT-B/16 on the same D1 split.
3. Measure internal classification performance using accuracy, balanced accuracy, macro-F1, and confusion matrices.
4. Evaluate internal calibration using confidence-accuracy gap, expected calibration error, Brier score, and negative log-likelihood.
5. Apply post-hoc temperature scaling using validation logits only.
6. Audit candidate external datasets for exact and perceptual overlap.
7. Reject unsuitable external datasets where overlap is detected.
8. Construct a visually distinct D3B glioma-focused domain-shift dataset.
9. Evaluate D1-trained models on D3B using glioma prediction rate, confidence, entropy, and prediction distribution.
10. Determine whether temperature scaling corrects D3B prediction instability.

## Hypothesis

High internal D1 classification performance and improved internal calibration will not be sufficient to guarantee stable prediction behaviour under D3B domain shift.

## Contribution

This study contributes a reproducible reliability-first evaluation framework for brain MRI tumour classification. It demonstrates that internal accuracy, even when paired with improved calibration, can overstate reliability if dataset overlap and domain-shift behaviour are not explicitly tested.
