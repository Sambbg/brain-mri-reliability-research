# E001 on D3C Domain-Shift Evaluation

## Experiment

E001 ResNet18 trained on D1 leakage-aware split, evaluated on D3C UPENN-GBM central slices.

## Inputs

- Checkpoint: `experiments\E001_D1_resnet18_baseline\best_model.pt`
- D3C manifest: `data\processed\D3C_selected_slices_manifest_phash.csv`
- D3C slices evaluated: 2845
- Patients represented: 569
- Series represented: 569

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 1974 | 0.6938 |
| meningioma | 9 | 0.0032 |
| notumor | 687 | 0.2415 |
| pituitary | 175 | 0.0615 |

## Core D3C Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.6938 |
| Mean glioma probability | 0.6438 |
| Median glioma probability | 0.7937 |
| Mean maximum softmax confidence | 0.8315 |
| Median maximum softmax confidence | 0.8922 |
| Mean entropy | 0.4279 |
| Median entropy | 0.3925 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 399 |
| meningioma | 1 |
| notumor | 132 |
| pituitary | 37 |

Patient-level majority glioma rate: `0.7012`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 399 |
| meningioma | 1 |
| notumor | 132 |
| pituitary | 37 |

Series-level majority glioma rate: `0.7012`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| UPENN-GBM-00349 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9765 | 0.9765 | 0.1131 |
| UPENN-GBM-00349 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9887 | 0.9887 | 0.0641 |
| UPENN-GBM-00349 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.9941 | 0.9941 | 0.0369 |
| UPENN-GBM-00349 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.8401 | 0.8401 | 0.4498 |
| UPENN-GBM-00349 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.8427 | 0.8427 | 0.4454 |
| UPENN-GBM-00342 | AX T1 POST STEALTH: Processed_CaPTk | 1 | glioma | 0.7965 | 0.7965 | 0.6259 |
| UPENN-GBM-00342 | AX T1 POST STEALTH: Processed_CaPTk | 2 | notumor | 0.2354 | 0.7364 | 0.6849 |
| UPENN-GBM-00342 | AX T1 POST STEALTH: Processed_CaPTk | 3 | notumor | 0.2912 | 0.6897 | 0.7043 |
| UPENN-GBM-00342 | AX T1 POST STEALTH: Processed_CaPTk | 4 | notumor | 0.0843 | 0.8988 | 0.3849 |
| UPENN-GBM-00342 | AX T1 POST STEALTH: Processed_CaPTk | 5 | notumor | 0.3663 | 0.5096 | 1.0392 |
| UPENN-GBM-00554 | AX T1 POST STEALTH_TERA : Processed_CaPTk | 1 | glioma | 0.5119 | 0.5119 | 0.9847 |
| UPENN-GBM-00554 | AX T1 POST STEALTH_TERA : Processed_CaPTk | 2 | notumor | 0.3048 | 0.5092 | 1.0193 |
| UPENN-GBM-00554 | AX T1 POST STEALTH_TERA : Processed_CaPTk | 3 | notumor | 0.0374 | 0.9350 | 0.2851 |
| UPENN-GBM-00554 | AX T1 POST STEALTH_TERA : Processed_CaPTk | 4 | notumor | 0.1536 | 0.7889 | 0.6421 |
| UPENN-GBM-00554 | AX T1 POST STEALTH_TERA : Processed_CaPTk | 5 | glioma | 0.6766 | 0.6766 | 0.8125 |
| UPENN-GBM-00177 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.4540 | 0.5112 | 0.8402 |
| UPENN-GBM-00177 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.8122 | 0.8122 | 0.5450 |
| UPENN-GBM-00177 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.7012 | 0.7012 | 0.6589 |
| UPENN-GBM-00177 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.4576 | 0.5273 | 0.7685 |
| UPENN-GBM-00177 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.2621 | 0.7266 | 0.6413 |
| UPENN-GBM-00346 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9495 | 0.9495 | 0.2445 |
| UPENN-GBM-00346 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.8908 | 0.8908 | 0.4270 |
| UPENN-GBM-00346 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.9288 | 0.9288 | 0.3124 |
| UPENN-GBM-00346 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9759 | 0.9759 | 0.1271 |
| UPENN-GBM-00346 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.9896 | 0.9896 | 0.0649 |
| UPENN-GBM-00266 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.1454 | 0.5298 | 0.9839 |
| UPENN-GBM-00266 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0738 | 0.7949 | 0.6429 |
| UPENN-GBM-00266 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0864 | 0.6986 | 0.7947 |
| UPENN-GBM-00266 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0990 | 0.6179 | 0.8857 |
| UPENN-GBM-00266 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0796 | 0.6074 | 0.8741 |

## Interpretation

This report evaluates whether the D1-trained E001 model recognises D3C glioma-domain images as glioma and how confident it is under domain shift. Because D3C labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E001 temperature scaling parameter to these D3C logits/probabilities and compare raw versus calibrated confidence under domain shift.
