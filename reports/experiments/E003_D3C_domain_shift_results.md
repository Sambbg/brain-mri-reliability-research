# E003 on D3C Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1 leakage-aware split, evaluated on D3C UPENN-GBM central slices.

## Inputs

- Checkpoint: `experiments/E003_D1_vit_b16_baseline/seed43/best_model.pt`
- D3C manifest: `data/processed/D3C_analysis_manifest.csv`
- D3C slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 641 | 0.2102 |
| meningioma | 83 | 0.0272 |
| notumor | 2307 | 0.7564 |
| pituitary | 19 | 0.0062 |

## Core D3C Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.2102 |
| Mean glioma probability | 0.2165 |
| Median glioma probability | 0.0194 |
| Mean maximum softmax confidence | 0.9018 |
| Median maximum softmax confidence | 0.9793 |
| Mean entropy | 0.2542 |
| Median entropy | 0.1077 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 123 |
| meningioma | 8 |
| notumor | 475 |
| pituitary | 4 |

Patient-level majority glioma rate: `0.2016`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 123 |
| meningioma | 8 |
| notumor | 475 |
| pituitary | 4 |

Series-level majority glioma rate: `0.2016`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0048 | 0.9938 | 0.0415 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0166 | 0.9770 | 0.1242 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0060 | 0.9930 | 0.0451 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0010 | 0.9984 | 0.0130 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0018 | 0.9976 | 0.0189 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0646 | 0.9143 | 0.3423 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.3026 | 0.4216 | 1.0907 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.4054 | 0.4725 | 0.9846 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.2007 | 0.7378 | 0.7231 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0126 | 0.9535 | 0.2183 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0007 | 0.9982 | 0.0147 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0002 | 0.9997 | 0.0031 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0003 | 0.9996 | 0.0039 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0008 | 0.9990 | 0.0084 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0006 | 0.9993 | 0.0060 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9470 | 0.9470 | 0.2124 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9701 | 0.9701 | 0.1386 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.8271 | 0.8271 | 0.4676 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9228 | 0.9228 | 0.2759 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.6140 | 0.6140 | 0.6734 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0004 | 0.9993 | 0.0061 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0041 | 0.9954 | 0.0310 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0026 | 0.9970 | 0.0221 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0108 | 0.9887 | 0.0643 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0513 | 0.9472 | 0.2139 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9729 | 0.9729 | 0.1369 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.3447 | 0.6420 | 0.7175 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0518 | 0.9475 | 0.2099 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0009 | 0.9989 | 0.0092 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0031 | 0.9966 | 0.0237 |

## Interpretation

This report evaluates whether the D1-trained E003 model recognises D3C glioma-domain images as glioma and how confident it is under domain shift. Because D3C labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E003 temperature scaling parameter to these D3C logits/probabilities and compare raw versus calibrated confidence under domain shift.
