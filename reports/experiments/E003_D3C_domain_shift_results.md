# E003 on D3C Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1 leakage-aware split, evaluated on D3C UPENN-GBM central slices.

## Inputs

- Checkpoint: `experiments/E003_D1_vit_b16_baseline/seed46/best_model.pt`
- D3C manifest: `data/processed/D3C_analysis_manifest.csv`
- D3C slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 566 | 0.1856 |
| meningioma | 336 | 0.1102 |
| notumor | 2142 | 0.7023 |
| pituitary | 6 | 0.0020 |

## Core D3C Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.1856 |
| Mean glioma probability | 0.1853 |
| Median glioma probability | 0.0132 |
| Mean maximum softmax confidence | 0.8839 |
| Median maximum softmax confidence | 0.9767 |
| Mean entropy | 0.2899 |
| Median entropy | 0.1213 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 113 |
| meningioma | 57 |
| notumor | 439 |
| pituitary | 1 |

Patient-level majority glioma rate: `0.1852`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 113 |
| meningioma | 57 |
| notumor | 439 |
| pituitary | 1 |

Series-level majority glioma rate: `0.1852`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0002 | 0.9996 | 0.0042 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0002 | 0.9993 | 0.0065 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0001 | 0.9995 | 0.0043 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0003 | 0.9988 | 0.0099 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0001 | 0.9994 | 0.0052 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 1 | meningioma | 0.3775 | 0.5493 | 0.8931 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 2 | meningioma | 0.3602 | 0.6343 | 0.6877 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.6578 | 0.6578 | 0.6763 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.7310 | 0.7310 | 0.6579 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.6110 | 0.6110 | 0.9270 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0056 | 0.9861 | 0.0831 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0002 | 0.9996 | 0.0036 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0002 | 0.9997 | 0.0030 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0002 | 0.9997 | 0.0030 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0003 | 0.9996 | 0.0039 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.6002 | 0.6002 | 0.6799 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.3519 | 0.6472 | 0.6560 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0573 | 0.9423 | 0.2232 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0600 | 0.9396 | 0.2305 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0920 | 0.9074 | 0.3123 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0002 | 0.9997 | 0.0026 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0042 | 0.9955 | 0.0302 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0005 | 0.9994 | 0.0055 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.4050 | 0.5917 | 0.6958 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0150 | 0.9847 | 0.0809 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.5679 | 0.5679 | 0.7255 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0169 | 0.9808 | 0.1021 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0003 | 0.9997 | 0.0032 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0009 | 0.9989 | 0.0087 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0005 | 0.9994 | 0.0055 |

## Interpretation

This report evaluates whether the D1-trained E003 model recognises D3C glioma-domain images as glioma and how confident it is under domain shift. Because D3C labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E003 temperature scaling parameter to these D3C logits/probabilities and compare raw versus calibrated confidence under domain shift.
