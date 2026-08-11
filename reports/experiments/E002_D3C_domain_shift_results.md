# E002 on D3C Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1 leakage-aware split, evaluated on D3C UPENN-GBM central slices.

## Inputs

- Checkpoint: `experiments/E002_D1_efficientnet_b0_baseline/seed43/best_model.pt`
- D3C manifest: `data/processed/D3C_analysis_manifest.csv`
- D3C slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 1866 | 0.6118 |
| meningioma | 46 | 0.0151 |
| notumor | 816 | 0.2675 |
| pituitary | 322 | 0.1056 |

## Core D3C Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.6118 |
| Mean glioma probability | 0.5834 |
| Median glioma probability | 0.7163 |
| Mean maximum softmax confidence | 0.8360 |
| Median maximum softmax confidence | 0.9131 |
| Mean entropy | 0.4308 |
| Median entropy | 0.3535 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 387 |
| meningioma | 7 |
| notumor | 156 |
| pituitary | 60 |

Patient-level majority glioma rate: `0.6344`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 387 |
| meningioma | 7 |
| notumor | 156 |
| pituitary | 60 |

Series-level majority glioma rate: `0.6344`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0147 | 0.9679 | 0.1748 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.5448 | 0.5448 | 0.8821 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0601 | 0.9270 | 0.3041 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.1835 | 0.7781 | 0.6545 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0582 | 0.9084 | 0.3848 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9932 | 0.9932 | 0.0432 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.8496 | 0.8496 | 0.4326 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.9330 | 0.9330 | 0.2516 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9970 | 0.9970 | 0.0225 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.9955 | 0.9955 | 0.0322 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0120 | 0.9204 | 0.3368 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0109 | 0.9386 | 0.2787 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0168 | 0.9379 | 0.2983 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.1408 | 0.7636 | 0.7557 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0438 | 0.9097 | 0.3883 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9910 | 0.9910 | 0.0585 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9910 | 0.9910 | 0.0581 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.9957 | 0.9957 | 0.0312 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9925 | 0.9925 | 0.0491 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.9355 | 0.9355 | 0.2455 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.6827 | 0.6827 | 0.7470 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9391 | 0.9391 | 0.2734 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.8485 | 0.8485 | 0.5043 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9563 | 0.9563 | 0.2125 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.7652 | 0.7652 | 0.6655 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.8850 | 0.8850 | 0.3973 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0084 | 0.9804 | 0.1138 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0190 | 0.9710 | 0.1541 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.2340 | 0.7237 | 0.7216 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0389 | 0.9532 | 0.2148 |

## Interpretation

This report evaluates whether the D1-trained E002 model recognises D3C glioma-domain images as glioma and how confident it is under domain shift. Because D3C labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E002 temperature scaling parameter to these D3C logits/probabilities and compare raw versus calibrated confidence under domain shift.
