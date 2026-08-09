# E003 on D3C Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1 leakage-aware split, evaluated on D3C UPENN-GBM central slices.

## Inputs

- Checkpoint: `experiments\E003_D1_vit_b16_baseline\best_model.pt`
- D3C manifest: `data\processed\D3C_selected_slices_manifest_phash.csv`
- D3C slices evaluated: 2845
- Patients represented: 569
- Series represented: 569

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 620 | 0.2179 |
| meningioma | 210 | 0.0738 |
| notumor | 1973 | 0.6935 |
| pituitary | 42 | 0.0148 |

## Core D3C Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.2179 |
| Mean glioma probability | 0.2132 |
| Median glioma probability | 0.0036 |
| Mean maximum softmax confidence | 0.9115 |
| Median maximum softmax confidence | 0.9877 |
| Mean entropy | 0.2261 |
| Median entropy | 0.0728 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 128 |
| meningioma | 30 |
| notumor | 403 |
| pituitary | 8 |

Patient-level majority glioma rate: `0.2250`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 128 |
| meningioma | 30 |
| notumor | 403 |
| pituitary | 8 |

Series-level majority glioma rate: `0.2250`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| UPENN-GBM-00349 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.1187 | 0.5549 | 1.0165 |
| UPENN-GBM-00349 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0538 | 0.9284 | 0.3099 |
| UPENN-GBM-00349 | t1 axial stealth-post : Processed_CaPTk | 3 | meningioma | 0.0191 | 0.8316 | 0.5897 |
| UPENN-GBM-00349 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0340 | 0.9487 | 0.2456 |
| UPENN-GBM-00349 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0433 | 0.9355 | 0.2866 |
| UPENN-GBM-00342 | AX T1 POST STEALTH: Processed_CaPTk | 1 | notumor | 0.0414 | 0.9579 | 0.1784 |
| UPENN-GBM-00342 | AX T1 POST STEALTH: Processed_CaPTk | 2 | notumor | 0.0020 | 0.9979 | 0.0161 |
| UPENN-GBM-00342 | AX T1 POST STEALTH: Processed_CaPTk | 3 | notumor | 0.0026 | 0.9972 | 0.0197 |
| UPENN-GBM-00342 | AX T1 POST STEALTH: Processed_CaPTk | 4 | notumor | 0.0010 | 0.9989 | 0.0088 |
| UPENN-GBM-00342 | AX T1 POST STEALTH: Processed_CaPTk | 5 | notumor | 0.0009 | 0.9990 | 0.0081 |
| UPENN-GBM-00554 | AX T1 POST STEALTH_TERA : Processed_CaPTk | 1 | notumor | 0.0001 | 0.9989 | 0.0091 |
| UPENN-GBM-00554 | AX T1 POST STEALTH_TERA : Processed_CaPTk | 2 | notumor | 0.0003 | 0.9981 | 0.0147 |
| UPENN-GBM-00554 | AX T1 POST STEALTH_TERA : Processed_CaPTk | 3 | notumor | 0.0002 | 0.9994 | 0.0052 |
| UPENN-GBM-00554 | AX T1 POST STEALTH_TERA : Processed_CaPTk | 4 | notumor | 0.0006 | 0.9982 | 0.0150 |
| UPENN-GBM-00554 | AX T1 POST STEALTH_TERA : Processed_CaPTk | 5 | notumor | 0.0607 | 0.9294 | 0.2894 |
| UPENN-GBM-00177 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9359 | 0.9359 | 0.2427 |
| UPENN-GBM-00177 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9788 | 0.9788 | 0.1081 |
| UPENN-GBM-00177 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.9974 | 0.9974 | 0.0196 |
| UPENN-GBM-00177 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9986 | 0.9986 | 0.0116 |
| UPENN-GBM-00177 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.9957 | 0.9957 | 0.0293 |
| UPENN-GBM-00346 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9956 | 0.9956 | 0.0322 |
| UPENN-GBM-00346 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9920 | 0.9920 | 0.0528 |
| UPENN-GBM-00346 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.9652 | 0.9652 | 0.1662 |
| UPENN-GBM-00346 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9856 | 0.9856 | 0.0864 |
| UPENN-GBM-00346 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.9404 | 0.9404 | 0.2402 |
| UPENN-GBM-00266 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0011 | 0.9985 | 0.0122 |
| UPENN-GBM-00266 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0052 | 0.9944 | 0.0365 |
| UPENN-GBM-00266 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0001 | 0.9998 | 0.0017 |
| UPENN-GBM-00266 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0001 | 0.9993 | 0.0063 |
| UPENN-GBM-00266 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0001 | 0.9996 | 0.0037 |

## Interpretation

This report evaluates whether the D1-trained E003 model recognises D3C glioma-domain images as glioma and how confident it is under domain shift. Because D3C labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E003 temperature scaling parameter to these D3C logits/probabilities and compare raw versus calibrated confidence under domain shift.
