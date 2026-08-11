# E002 on D3C Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1 leakage-aware split, evaluated on D3C UPENN-GBM central slices.

## Inputs

- Checkpoint: `experiments/E002_D1_efficientnet_b0_baseline/seed46/best_model.pt`
- D3C manifest: `data/processed/D3C_analysis_manifest.csv`
- D3C slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 1590 | 0.5213 |
| meningioma | 49 | 0.0161 |
| notumor | 1214 | 0.3980 |
| pituitary | 197 | 0.0646 |

## Core D3C Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.5213 |
| Mean glioma probability | 0.5060 |
| Median glioma probability | 0.4991 |
| Mean maximum softmax confidence | 0.8264 |
| Median maximum softmax confidence | 0.8999 |
| Mean entropy | 0.4545 |
| Median entropy | 0.3948 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 325 |
| meningioma | 6 |
| notumor | 249 |
| pituitary | 30 |

Patient-level majority glioma rate: `0.5328`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 325 |
| meningioma | 6 |
| notumor | 249 |
| pituitary | 30 |

Series-level majority glioma rate: `0.5328`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.1228 | 0.7538 | 0.8046 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.7365 | 0.7365 | 0.7453 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0157 | 0.9656 | 0.1850 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0082 | 0.9647 | 0.1829 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0263 | 0.9282 | 0.3226 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9890 | 0.9890 | 0.0642 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9911 | 0.9911 | 0.0523 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.9846 | 0.9846 | 0.0853 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9990 | 0.9990 | 0.0086 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.9994 | 0.9994 | 0.0056 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0180 | 0.9372 | 0.2975 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0218 | 0.9304 | 0.3283 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0084 | 0.9532 | 0.2372 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.1406 | 0.7871 | 0.6844 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0300 | 0.9622 | 0.1841 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9079 | 0.9079 | 0.3460 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9534 | 0.9534 | 0.2099 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.9293 | 0.9293 | 0.2665 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9050 | 0.9050 | 0.3366 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.8264 | 0.8264 | 0.4766 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.6707 | 0.6707 | 0.8798 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.8880 | 0.8880 | 0.4597 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.6838 | 0.6838 | 0.7349 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9119 | 0.9119 | 0.3598 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.9774 | 0.9774 | 0.1245 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9679 | 0.9679 | 0.1582 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0235 | 0.9469 | 0.2603 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0264 | 0.9573 | 0.2141 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0574 | 0.9204 | 0.3352 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0031 | 0.9883 | 0.0754 |

## Interpretation

This report evaluates whether the D1-trained E002 model recognises D3C glioma-domain images as glioma and how confident it is under domain shift. Because D3C labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E002 temperature scaling parameter to these D3C logits/probabilities and compare raw versus calibrated confidence under domain shift.
