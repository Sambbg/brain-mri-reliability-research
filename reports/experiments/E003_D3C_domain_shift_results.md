# E003 on D3C Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1 leakage-aware split, evaluated on D3C UPENN-GBM central slices.

## Inputs

- Checkpoint: `experiments/E003_D1_vit_b16_baseline/seed44/best_model.pt`
- D3C manifest: `data/processed/D3C_analysis_manifest.csv`
- D3C slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 636 | 0.2085 |
| meningioma | 168 | 0.0551 |
| notumor | 1948 | 0.6387 |
| pituitary | 298 | 0.0977 |

## Core D3C Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.2085 |
| Mean glioma probability | 0.2151 |
| Median glioma probability | 0.0261 |
| Mean maximum softmax confidence | 0.8384 |
| Median maximum softmax confidence | 0.9083 |
| Mean entropy | 0.4068 |
| Median entropy | 0.3505 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 123 |
| meningioma | 26 |
| notumor | 402 |
| pituitary | 59 |

Patient-level majority glioma rate: `0.2016`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 123 |
| meningioma | 26 |
| notumor | 402 |
| pituitary | 59 |

Series-level majority glioma rate: `0.2016`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0702 | 0.9124 | 0.3424 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.1078 | 0.8757 | 0.4259 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0140 | 0.9843 | 0.0867 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0014 | 0.9980 | 0.0157 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0026 | 0.9960 | 0.0296 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0088 | 0.9882 | 0.0720 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0137 | 0.9808 | 0.1095 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0397 | 0.9528 | 0.2151 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0241 | 0.9737 | 0.1307 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0608 | 0.9354 | 0.2554 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0005 | 0.9993 | 0.0064 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0003 | 0.9995 | 0.0046 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0003 | 0.9996 | 0.0037 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0005 | 0.9994 | 0.0054 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0006 | 0.9994 | 0.0057 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9915 | 0.9915 | 0.0527 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9933 | 0.9933 | 0.0435 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.9946 | 0.9946 | 0.0357 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9946 | 0.9946 | 0.0369 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.9885 | 0.9885 | 0.0676 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0006 | 0.9991 | 0.0076 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0013 | 0.9981 | 0.0152 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0007 | 0.9989 | 0.0092 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0047 | 0.9943 | 0.0386 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0076 | 0.9898 | 0.0644 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.2442 | 0.7489 | 0.5985 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0129 | 0.9793 | 0.1162 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0007 | 0.9992 | 0.0068 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0034 | 0.9962 | 0.0263 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0276 | 0.9650 | 0.1706 |

## Interpretation

This report evaluates whether the D1-trained E003 model recognises D3C glioma-domain images as glioma and how confident it is under domain shift. Because D3C labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E003 temperature scaling parameter to these D3C logits/probabilities and compare raw versus calibrated confidence under domain shift.
