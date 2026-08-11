# E002 on D3C Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1 leakage-aware split, evaluated on D3C UPENN-GBM central slices.

## Inputs

- Checkpoint: `experiments/E002_D1_efficientnet_b0_baseline/seed45/best_model.pt`
- D3C manifest: `data/processed/D3C_analysis_manifest.csv`
- D3C slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 1380 | 0.4525 |
| meningioma | 24 | 0.0079 |
| notumor | 1483 | 0.4862 |
| pituitary | 163 | 0.0534 |

## Core D3C Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.4525 |
| Mean glioma probability | 0.4378 |
| Median glioma probability | 0.3539 |
| Mean maximum softmax confidence | 0.7368 |
| Median maximum softmax confidence | 0.7556 |
| Mean entropy | 0.6764 |
| Median entropy | 0.7288 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 270 |
| meningioma | 3 |
| notumor | 308 |
| pituitary | 29 |

Patient-level majority glioma rate: `0.4426`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 270 |
| meningioma | 3 |
| notumor | 308 |
| pituitary | 29 |

Series-level majority glioma rate: `0.4426`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.1380 | 0.7379 | 0.8260 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.6571 | 0.6571 | 0.8498 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.2268 | 0.7244 | 0.7512 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.1443 | 0.8136 | 0.6085 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.1487 | 0.7876 | 0.6879 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.7058 | 0.7058 | 0.8381 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.6339 | 0.6339 | 0.9318 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.8250 | 0.8250 | 0.6063 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.3913 | 0.5057 | 1.0168 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.9496 | 0.9496 | 0.2449 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0221 | 0.9168 | 0.3653 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0131 | 0.9511 | 0.2430 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0182 | 0.9356 | 0.3034 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0371 | 0.9199 | 0.3596 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0184 | 0.9695 | 0.1638 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.8776 | 0.8776 | 0.4215 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.7966 | 0.7966 | 0.5776 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.8367 | 0.8367 | 0.4910 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9093 | 0.9093 | 0.3379 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.6678 | 0.6678 | 0.6682 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.2818 | 0.4710 | 1.1453 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.6363 | 0.6363 | 0.9570 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.3899 | 0.4550 | 1.1026 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.5575 | 0.5575 | 1.0056 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.4508 | 0.4548 | 1.0006 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.6660 | 0.6660 | 0.7416 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0358 | 0.9295 | 0.3238 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.1237 | 0.8204 | 0.6156 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.1317 | 0.8261 | 0.5821 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0193 | 0.9625 | 0.1969 |

## Interpretation

This report evaluates whether the D1-trained E002 model recognises D3C glioma-domain images as glioma and how confident it is under domain shift. Because D3C labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E002 temperature scaling parameter to these D3C logits/probabilities and compare raw versus calibrated confidence under domain shift.
