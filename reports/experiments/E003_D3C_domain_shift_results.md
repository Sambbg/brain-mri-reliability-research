# E003 on D3C Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1 leakage-aware split, evaluated on D3C UPENN-GBM central slices.

## Inputs

- Checkpoint: `experiments/E003_D1_vit_b16_baseline/seed42/best_model.pt`
- D3C manifest: `data/processed/D3C_analysis_manifest.csv`
- D3C slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 1412 | 0.4630 |
| meningioma | 456 | 0.1495 |
| notumor | 1021 | 0.3348 |
| pituitary | 161 | 0.0528 |

## Core D3C Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.4630 |
| Mean glioma probability | 0.4402 |
| Median glioma probability | 0.3769 |
| Mean maximum softmax confidence | 0.8041 |
| Median maximum softmax confidence | 0.8556 |
| Mean entropy | 0.4888 |
| Median entropy | 0.4720 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 291 |
| meningioma | 84 |
| notumor | 211 |
| pituitary | 24 |

Patient-level majority glioma rate: `0.4770`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 291 |
| meningioma | 84 |
| notumor | 211 |
| pituitary | 24 |

Series-level majority glioma rate: `0.4770`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.3114 | 0.6566 | 0.7708 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0977 | 0.8886 | 0.3986 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0042 | 0.9938 | 0.0428 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0118 | 0.9688 | 0.1635 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0168 | 0.9384 | 0.2915 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.7472 | 0.7472 | 0.6817 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.5680 | 0.5680 | 0.7832 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.7257 | 0.7257 | 0.6729 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9284 | 0.9284 | 0.2946 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.6608 | 0.6608 | 0.8493 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0269 | 0.9551 | 0.2151 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0547 | 0.9380 | 0.2563 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0090 | 0.9887 | 0.0687 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0104 | 0.9887 | 0.0657 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0045 | 0.9947 | 0.0355 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9973 | 0.9973 | 0.0213 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9951 | 0.9951 | 0.0359 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.9969 | 0.9969 | 0.0242 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9860 | 0.9860 | 0.0801 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.9884 | 0.9884 | 0.0696 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.7023 | 0.7023 | 0.6700 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.3642 | 0.6148 | 0.7591 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0307 | 0.9659 | 0.1614 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9777 | 0.9777 | 0.1235 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.5630 | 0.5630 | 0.7339 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9794 | 0.9794 | 0.1121 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.7697 | 0.7697 | 0.5910 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0338 | 0.9547 | 0.2119 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0030 | 0.9957 | 0.0305 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0034 | 0.9960 | 0.0283 |

## Interpretation

This report evaluates whether the D1-trained E003 model recognises D3C glioma-domain images as glioma and how confident it is under domain shift. Because D3C labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E003 temperature scaling parameter to these D3C logits/probabilities and compare raw versus calibrated confidence under domain shift.
