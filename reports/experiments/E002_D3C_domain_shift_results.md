# E002 on D3C Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1 leakage-aware split, evaluated on D3C UPENN-GBM central slices.

## Inputs

- Checkpoint: `experiments\E002_D1_efficientnet_b0_baseline\best_model.pt`
- D3C manifest: `data\processed\D3C_selected_slices_manifest_phash.csv`
- D3C slices evaluated: 2845
- Patients represented: 569
- Series represented: 569

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 1316 | 0.4626 |
| meningioma | 54 | 0.0190 |
| notumor | 1455 | 0.5114 |
| pituitary | 20 | 0.0070 |

## Core D3C Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.4626 |
| Mean glioma probability | 0.4512 |
| Median glioma probability | 0.3755 |
| Mean maximum softmax confidence | 0.8033 |
| Median maximum softmax confidence | 0.8546 |
| Mean entropy | 0.5195 |
| Median entropy | 0.5210 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 260 |
| meningioma | 8 |
| notumor | 299 |
| pituitary | 2 |

Patient-level majority glioma rate: `0.4569`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 260 |
| meningioma | 8 |
| notumor | 299 |
| pituitary | 2 |

Series-level majority glioma rate: `0.4569`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| UPENN-GBM-00349 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.5130 | 0.5130 | 0.8762 |
| UPENN-GBM-00349 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.7481 | 0.7481 | 0.7326 |
| UPENN-GBM-00349 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.8340 | 0.8340 | 0.5630 |
| UPENN-GBM-00349 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.6367 | 0.6367 | 0.9076 |
| UPENN-GBM-00349 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.5718 | 0.5718 | 0.9662 |
| UPENN-GBM-00342 | AX T1 POST STEALTH: Processed_CaPTk | 1 | notumor | 0.1523 | 0.8271 | 0.5334 |
| UPENN-GBM-00342 | AX T1 POST STEALTH: Processed_CaPTk | 2 | notumor | 0.0091 | 0.9877 | 0.0756 |
| UPENN-GBM-00342 | AX T1 POST STEALTH: Processed_CaPTk | 3 | notumor | 0.0520 | 0.9407 | 0.2520 |
| UPENN-GBM-00342 | AX T1 POST STEALTH: Processed_CaPTk | 4 | notumor | 0.0100 | 0.9829 | 0.1024 |
| UPENN-GBM-00342 | AX T1 POST STEALTH: Processed_CaPTk | 5 | notumor | 0.0808 | 0.9034 | 0.3714 |
| UPENN-GBM-00554 | AX T1 POST STEALTH_TERA : Processed_CaPTk | 1 | glioma | 0.5222 | 0.5222 | 0.7945 |
| UPENN-GBM-00554 | AX T1 POST STEALTH_TERA : Processed_CaPTk | 2 | glioma | 0.5066 | 0.5066 | 0.7925 |
| UPENN-GBM-00554 | AX T1 POST STEALTH_TERA : Processed_CaPTk | 3 | glioma | 0.8875 | 0.8875 | 0.3814 |
| UPENN-GBM-00554 | AX T1 POST STEALTH_TERA : Processed_CaPTk | 4 | glioma | 0.5889 | 0.5889 | 0.8125 |
| UPENN-GBM-00554 | AX T1 POST STEALTH_TERA : Processed_CaPTk | 5 | glioma | 0.9820 | 0.9820 | 0.1018 |
| UPENN-GBM-00177 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9603 | 0.9603 | 0.2024 |
| UPENN-GBM-00177 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9934 | 0.9934 | 0.0456 |
| UPENN-GBM-00177 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.9969 | 0.9969 | 0.0234 |
| UPENN-GBM-00177 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9920 | 0.9920 | 0.0527 |
| UPENN-GBM-00177 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.9901 | 0.9901 | 0.0628 |
| UPENN-GBM-00346 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9935 | 0.9935 | 0.0447 |
| UPENN-GBM-00346 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9539 | 0.9539 | 0.2121 |
| UPENN-GBM-00346 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.9866 | 0.9866 | 0.0840 |
| UPENN-GBM-00346 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.8859 | 0.8859 | 0.4119 |
| UPENN-GBM-00346 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.9917 | 0.9917 | 0.0541 |
| UPENN-GBM-00266 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.4084 | 0.4084 | 1.1784 |
| UPENN-GBM-00266 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.1474 | 0.6008 | 1.0287 |
| UPENN-GBM-00266 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.2177 | 0.4406 | 1.2104 |
| UPENN-GBM-00266 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.3674 | 0.4460 | 1.1325 |
| UPENN-GBM-00266 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.6741 | 0.6741 | 0.9127 |

## Interpretation

This report evaluates whether the D1-trained E002 model recognises D3C glioma-domain images as glioma and how confident it is under domain shift. Because D3C labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E002 temperature scaling parameter to these D3C logits/probabilities and compare raw versus calibrated confidence under domain shift.
