# E001 on D3C Domain-Shift Evaluation

## Experiment

E001 ResNet18 trained on D1 leakage-aware split, evaluated on D3C UPENN-GBM central slices.

## Inputs

- Checkpoint: `experiments/E001_D1_resnet18_baseline/seed43/best_model.pt`
- D3C manifest: `data/processed/D3C_analysis_manifest.csv`
- D3C slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 1931 | 0.6331 |
| meningioma | 39 | 0.0128 |
| notumor | 705 | 0.2311 |
| pituitary | 375 | 0.1230 |

## Core D3C Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.6331 |
| Mean glioma probability | 0.5504 |
| Median glioma probability | 0.6045 |
| Mean maximum softmax confidence | 0.7395 |
| Median maximum softmax confidence | 0.7565 |
| Mean entropy | 0.6613 |
| Median entropy | 0.7078 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 397 |
| meningioma | 7 |
| notumor | 132 |
| pituitary | 74 |

Patient-level majority glioma rate: `0.6508`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 397 |
| meningioma | 7 |
| notumor | 132 |
| pituitary | 74 |

Series-level majority glioma rate: `0.6508`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.6709 | 0.6709 | 0.8577 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.7682 | 0.7682 | 0.7327 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.5947 | 0.5947 | 0.9734 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.4986 | 0.4986 | 1.1648 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.4956 | 0.4956 | 1.1457 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0734 | 0.9005 | 0.3917 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.1023 | 0.8203 | 0.6316 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.2112 | 0.6776 | 0.8942 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.3783 | 0.4999 | 1.0553 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.3196 | 0.6215 | 0.8586 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0819 | 0.8756 | 0.4722 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0128 | 0.9838 | 0.0928 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0425 | 0.9512 | 0.2171 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0386 | 0.9559 | 0.2007 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0210 | 0.9721 | 0.1473 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9839 | 0.9839 | 0.0978 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9894 | 0.9894 | 0.0687 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.9894 | 0.9894 | 0.0683 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9758 | 0.9758 | 0.1302 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.9740 | 0.9740 | 0.1327 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.3912 | 0.4315 | 1.0435 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.8031 | 0.8031 | 0.6388 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.2365 | 0.6492 | 0.8925 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.1609 | 0.6309 | 0.9256 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.4969 | 0.4969 | 1.0478 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9489 | 0.9489 | 0.2548 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.8352 | 0.8352 | 0.5968 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.7042 | 0.7042 | 0.7884 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.7915 | 0.7915 | 0.6573 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.4552 | 0.4552 | 0.9897 |

## Interpretation

This report evaluates whether the D1-trained E001 model recognises D3C glioma-domain images as glioma and how confident it is under domain shift. Because D3C labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E001 temperature scaling parameter to these D3C logits/probabilities and compare raw versus calibrated confidence under domain shift.
