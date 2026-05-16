# E001 Integrated Summary — D1 Internal Reliability and D3B Domain-Shift Behaviour

## Experiment

E001 evaluates a ResNet18 baseline trained on the D1 leakage-aware split.

The purpose of E001 is not to claim clinical reliability. The purpose is to establish a reproducible baseline and test whether strong internal performance remains stable when evaluated beyond the original D1 benchmark.

## D1 Internal Test Performance

The E001 ResNet18 baseline achieved strong internal performance on the D1 leakage-aware test split.

| Metric | Value |
|---|---:|
| Test accuracy | 0.9667 |
| Test balanced accuracy | 0.9662 |
| Test macro-F1 | 0.9666 |
| Best validation macro-F1 | 0.9704 |
| Best epoch | 8 |

## D1 Calibration Before Temperature Scaling

The uncalibrated E001 model was slightly overconfident on the internal D1 test set.

| Metric | Value |
|---|---:|
| Accuracy | 0.9667 |
| Mean confidence | 0.9836 |
| Confidence-accuracy gap | 0.0169 |
| ECE, 15 bins | 0.0193 |
| Brier score | 0.0557 |
| Negative log-likelihood | 0.1176 |

## D1 Calibration After Temperature Scaling

Temperature scaling was fitted using the D1 validation set only and evaluated on the D1 test set.

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Accuracy | 0.9667 | 0.9667 |
| Balanced accuracy | 0.9662 | 0.9662 |
| Macro-F1 | 0.9666 | 0.9666 |
| Mean confidence | 0.9836 | 0.9773 |
| Confidence-accuracy gap | 0.0169 | 0.0106 |
| ECE, 15 bins | 0.0208 | 0.0145 |
| Brier score | 0.0557 | 0.0536 |
| Negative log-likelihood | 0.1176 | 0.1063 |

Temperature scaling improved calibration-related metrics internally without changing classification accuracy.

## D2 External Dataset Audit Result

D2, BRISC2025, was initially considered as a possible external dataset. However, D1-D2 overlap auditing showed that D2 is not independent from D1.

| Audit | Result |
|---|---:|
| D1-D2 shared exact SHA256 hashes | 4740 |
| D1-D2 exact overlap pairs | 4740 |
| D1-D2 pHash near-overlap pairs | 7290 |
| D1-D2 cross-class near-overlap pairs | 68 |

Therefore, D2 must not be used as clean external validation evidence against D1.

This is a major reliability finding: a dataset that appears external at the dataset-name level may not be independent at the image-content level.

## D3B External Domain-Shift Dataset Preparation

D3B, ICDC-Glioma, was selected as a glioma-focused domain-shift dataset from TCIA/NBIA.

D3B was not treated as a four-class external validation dataset. It was treated as a glioma-focused domain-shift set.

| Item | Value |
|---|---:|
| Selected DICOM series | 53 |
| Patients represented | 53 |
| Valid MR DICOM image files | 2935 |
| Converted central slices | 265 |
| Slices per series | 5 |

## D1-D3B Overlap Audit

D3B central-slice PNG images were checked against D1 before model evaluation.

| Audit | Result |
|---|---:|
| D1-D3B exact SHA256 overlap pairs | 0 |
| D1-D3B pHash near-overlap pairs | 0 |

This supports treating D3B as visually distinct from D1 for domain-shift analysis, although it does not prove patient-level independence.

## E001 Raw D3B Domain-Shift Evaluation

When the D1-trained E001 model was evaluated on D3B glioma-domain central slices, prediction behaviour changed substantially.

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 78 | 0.2943 |
| meningioma | 79 | 0.2981 |
| notumor | 35 | 0.1321 |
| pituitary | 73 | 0.2755 |

Core D3B metrics:

| Metric | Value |
|---|---:|
| Slice-level glioma prediction rate | 0.2943 |
| Patient-majority glioma rate | 0.2642 |
| Series-majority glioma rate | 0.2642 |
| Mean glioma probability | 0.2936 |
| Median glioma probability | 0.1478 |
| Mean maximum softmax confidence | 0.7209 |
| Mean entropy | 0.7157 |

This result should not be described as four-class external accuracy. The correct interpretation is that only 29.43% of D3B glioma-domain central slices were predicted as glioma.

## E001 D3B Temperature-Scaled Evaluation

The D1 validation-learned temperature was then applied to D3B logits.

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Slice-level glioma prediction rate | 0.2943 | 0.2943 |
| Mean glioma probability | 0.2936 | 0.2927 |
| Median glioma probability | 0.1478 | 0.1796 |
| Mean max confidence | 0.7209 | 0.6678 |
| Median max confidence | 0.7263 | 0.6548 |
| Mean entropy | 0.7157 | 0.8363 |
| Patient-majority glioma rate | 0.2642 | 0.2642 |
| Series-majority glioma rate | 0.2642 | 0.2642 |

Temperature scaling reduced confidence sharpness and increased entropy, but it did not change the predicted class distribution.

## Main Interpretation

E001 demonstrates a clear distinction between internal benchmark performance and external/domain-shift behaviour.

Internally, the ResNet18 model achieved high D1 test performance and modestly improved calibration after temperature scaling.

However, external dataset auditing showed that D2 was unsuitable as clean external evidence because of substantial D1-D2 overlap.

When evaluated on visually distinct D3B glioma-domain images, the model predicted glioma for only 29.43% of slices and only 26.42% of patients by majority vote. Temperature scaling softened confidence but did not correct the prediction distribution.

This supports the central research argument: high internal accuracy and even improved internal calibration are insufficient evidence of reliability unless dataset independence, overlap, calibration, and domain-shift behaviour are explicitly audited.

## Conservative Claim

The defensible claim from E001 is:

A leakage-aware and calibration-aware evaluation pipeline revealed that a high-performing D1-trained ResNet18 model did not maintain stable glioma prediction behaviour on a visually distinct glioma-focused D3B domain-shift set. Post-hoc temperature scaling improved confidence softness but did not correct the domain-shift prediction instability.

## Do Not Claim

This experiment does not prove:

1. Clinical diagnostic reliability.
2. Full four-class external accuracy.
3. Patient-level tumour classification accuracy on D3B.
4. Generalisation to all MRI datasets.
5. Superiority of ResNet18 over other architectures.

## Next Required Step

The next experiment should test whether this domain-shift behaviour is specific to ResNet18 or also appears in another architecture.

Recommended next experiment:

E002 — EfficientNet-B0 or DenseNet121 baseline trained on the same D1 leakage-aware split, followed by the same internal calibration and D3B domain-shift evaluation.
