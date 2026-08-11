# E003 on D3C Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1 leakage-aware split, evaluated on D3C UPENN-GBM central slices.

## Inputs

- Checkpoint: `experiments/E003_D1_vit_b16_baseline/seed45/best_model.pt`
- D3C manifest: `data/processed/D3C_analysis_manifest.csv`
- D3C slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 763 | 0.2502 |
| meningioma | 126 | 0.0413 |
| notumor | 2152 | 0.7056 |
| pituitary | 9 | 0.0030 |

## Core D3C Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.2502 |
| Mean glioma probability | 0.2597 |
| Median glioma probability | 0.0728 |
| Mean maximum softmax confidence | 0.8697 |
| Median maximum softmax confidence | 0.9473 |
| Mean entropy | 0.3245 |
| Median entropy | 0.2221 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 145 |
| meningioma | 18 |
| notumor | 446 |
| pituitary | 1 |

Patient-level majority glioma rate: `0.2377`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 145 |
| meningioma | 18 |
| notumor | 446 |
| pituitary | 1 |

Series-level majority glioma rate: `0.2377`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0447 | 0.9544 | 0.1899 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0320 | 0.9669 | 0.1508 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0459 | 0.9535 | 0.1919 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0146 | 0.9851 | 0.0791 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0082 | 0.9916 | 0.0498 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.1044 | 0.8851 | 0.3934 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.8765 | 0.8765 | 0.4286 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.9139 | 0.9139 | 0.3505 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.7978 | 0.7978 | 0.6097 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.6251 | 0.6251 | 0.6974 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0039 | 0.9959 | 0.0276 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0008 | 0.9992 | 0.0070 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0007 | 0.9992 | 0.0065 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0016 | 0.9983 | 0.0125 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0006 | 0.9993 | 0.0057 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.5671 | 0.5671 | 0.6919 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9135 | 0.9135 | 0.2985 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.9517 | 0.9517 | 0.1964 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.8711 | 0.8711 | 0.3883 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.8814 | 0.8814 | 0.3693 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0021 | 0.9978 | 0.0163 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0025 | 0.9974 | 0.0189 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0006 | 0.9982 | 0.0143 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0067 | 0.9932 | 0.0415 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0028 | 0.9971 | 0.0202 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0695 | 0.9301 | 0.2560 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0051 | 0.9946 | 0.0346 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0015 | 0.9984 | 0.0120 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0018 | 0.9981 | 0.0140 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0094 | 0.9905 | 0.0545 |

## Interpretation

This report evaluates whether the D1-trained E003 model recognises D3C glioma-domain images as glioma and how confident it is under domain shift. Because D3C labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E003 temperature scaling parameter to these D3C logits/probabilities and compare raw versus calibrated confidence under domain shift.
