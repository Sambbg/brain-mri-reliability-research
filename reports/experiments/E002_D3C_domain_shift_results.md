# E002 on D3C Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1 leakage-aware split, evaluated on D3C UPENN-GBM central slices.

## Inputs

- Checkpoint: `experiments/E002_D1_efficientnet_b0_baseline/seed42/best_model.pt`
- D3C manifest: `data/processed/D3C_analysis_manifest.csv`
- D3C slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 1396 | 0.4577 |
| meningioma | 25 | 0.0082 |
| notumor | 1597 | 0.5236 |
| pituitary | 32 | 0.0105 |

## Core D3C Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.4577 |
| Mean glioma probability | 0.4643 |
| Median glioma probability | 0.3592 |
| Mean maximum softmax confidence | 0.8632 |
| Median maximum softmax confidence | 0.9354 |
| Mean entropy | 0.3443 |
| Median entropy | 0.2640 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 280 |
| meningioma | 5 |
| notumor | 319 |
| pituitary | 6 |

Patient-level majority glioma rate: `0.4590`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 280 |
| meningioma | 5 |
| notumor | 319 |
| pituitary | 6 |

Series-level majority glioma rate: `0.4590`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0054 | 0.9927 | 0.0483 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0182 | 0.9805 | 0.1014 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0028 | 0.9966 | 0.0248 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0008 | 0.9989 | 0.0094 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0293 | 0.9672 | 0.1573 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9998 | 0.9998 | 0.0025 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9974 | 0.9974 | 0.0182 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.9989 | 0.9989 | 0.0089 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9985 | 0.9985 | 0.0119 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.9992 | 0.9992 | 0.0070 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0392 | 0.9534 | 0.2117 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0108 | 0.9796 | 0.1184 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0047 | 0.9916 | 0.0565 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0444 | 0.9456 | 0.2444 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0056 | 0.9937 | 0.0410 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9944 | 0.9944 | 0.0351 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9950 | 0.9950 | 0.0318 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.9911 | 0.9911 | 0.0516 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9921 | 0.9921 | 0.0465 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.9901 | 0.9901 | 0.0557 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.1280 | 0.7817 | 0.6829 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.2684 | 0.7146 | 0.6657 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0311 | 0.9651 | 0.1643 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.3474 | 0.6443 | 0.6930 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0828 | 0.9129 | 0.3140 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9708 | 0.9708 | 0.1361 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.2020 | 0.7860 | 0.5718 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.2528 | 0.7436 | 0.5903 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.5340 | 0.5340 | 0.7257 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0084 | 0.9907 | 0.0559 |

## Interpretation

This report evaluates whether the D1-trained E002 model recognises D3C glioma-domain images as glioma and how confident it is under domain shift. Because D3C labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E002 temperature scaling parameter to these D3C logits/probabilities and compare raw versus calibrated confidence under domain shift.
