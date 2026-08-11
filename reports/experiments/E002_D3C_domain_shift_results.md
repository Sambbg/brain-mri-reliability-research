# E002 on D3C Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1 leakage-aware split, evaluated on D3C UPENN-GBM central slices.

## Inputs

- Checkpoint: `experiments/E002_D1_efficientnet_b0_baseline/seed44/best_model.pt`
- D3C manifest: `data/processed/D3C_analysis_manifest.csv`
- D3C slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 1603 | 0.5256 |
| meningioma | 54 | 0.0177 |
| notumor | 1237 | 0.4056 |
| pituitary | 156 | 0.0511 |

## Core D3C Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.5256 |
| Mean glioma probability | 0.5098 |
| Median glioma probability | 0.4932 |
| Mean maximum softmax confidence | 0.7950 |
| Median maximum softmax confidence | 0.8474 |
| Mean entropy | 0.5235 |
| Median entropy | 0.5180 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 326 |
| meningioma | 6 |
| notumor | 254 |
| pituitary | 24 |

Patient-level majority glioma rate: `0.5344`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 326 |
| meningioma | 6 |
| notumor | 254 |
| pituitary | 24 |

Series-level majority glioma rate: `0.5344`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0955 | 0.7518 | 0.7903 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.4731 | 0.4731 | 0.9963 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0554 | 0.8944 | 0.4369 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0509 | 0.8856 | 0.4615 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0603 | 0.8158 | 0.6434 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9911 | 0.9911 | 0.0525 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9518 | 0.9518 | 0.1948 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.5787 | 0.5787 | 0.6867 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9604 | 0.9604 | 0.1695 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.9527 | 0.9527 | 0.1967 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0145 | 0.9770 | 0.1301 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0070 | 0.9825 | 0.1066 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0173 | 0.9639 | 0.1932 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0320 | 0.9601 | 0.1927 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.1125 | 0.8791 | 0.4049 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.7031 | 0.7031 | 0.7139 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.7242 | 0.7242 | 0.7068 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.7066 | 0.7066 | 0.6824 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.7717 | 0.7717 | 0.6000 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.6776 | 0.6776 | 0.6495 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.4179 | 0.4179 | 1.1244 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.5377 | 0.5377 | 1.0159 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.4201 | 0.4652 | 1.0014 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.6659 | 0.6659 | 0.8153 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.2640 | 0.6060 | 0.9609 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9949 | 0.9949 | 0.0333 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9302 | 0.9302 | 0.2730 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.7853 | 0.7853 | 0.5565 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9298 | 0.9298 | 0.2690 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.1511 | 0.8388 | 0.4851 |

## Interpretation

This report evaluates whether the D1-trained E002 model recognises D3C glioma-domain images as glioma and how confident it is under domain shift. Because D3C labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E002 temperature scaling parameter to these D3C logits/probabilities and compare raw versus calibrated confidence under domain shift.
