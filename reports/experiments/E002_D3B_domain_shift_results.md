# E002 on D3B Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1 leakage-aware split, evaluated on D3B ICDC-Glioma central slices.

## Inputs

- Checkpoint: `experiments/E002_D1_efficientnet_b0_baseline/seed43/best_model.pt`
- D3B manifest: `data/processed/D3B_selected_slices_manifest_phash.csv`
- D3B slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 59 | 0.2226 |
| meningioma | 33 | 0.1245 |
| notumor | 58 | 0.2189 |
| pituitary | 115 | 0.4340 |

## Core D3B Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.2226 |
| Mean glioma probability | 0.2268 |
| Median glioma probability | 0.0706 |
| Mean maximum softmax confidence | 0.7670 |
| Median maximum softmax confidence | 0.8006 |
| Mean entropy | 0.5998 |
| Median entropy | 0.6187 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 12 |
| meningioma | 5 |
| notumor | 13 |
| pituitary | 23 |

Patient-level majority glioma rate: `0.2264`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 12 |
| meningioma | 5 |
| notumor | 13 |
| pituitary | 23 |

Series-level majority glioma rate: `0.2264`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| GLIOMA01-i_6561 | FSPGR 3D | 1 | meningioma | 0.0831 | 0.5293 | 1.1241 |
| GLIOMA01-i_6561 | FSPGR 3D | 2 | meningioma | 0.1382 | 0.4873 | 1.1458 |
| GLIOMA01-i_6561 | FSPGR 3D | 3 | meningioma | 0.2221 | 0.4369 | 1.1793 |
| GLIOMA01-i_6561 | FSPGR 3D | 4 | meningioma | 0.1893 | 0.5021 | 1.1341 |
| GLIOMA01-i_6561 | FSPGR 3D | 5 | meningioma | 0.1145 | 0.7300 | 0.8501 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 1 | glioma | 0.6074 | 0.6074 | 1.0222 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 2 | glioma | 0.9207 | 0.9207 | 0.3630 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 3 | meningioma | 0.0260 | 0.9465 | 0.2643 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 4 | meningioma | 0.1777 | 0.7993 | 0.5880 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 5 | pituitary | 0.1795 | 0.4979 | 1.2422 |
| GLIOMA01-i_BF76 | Ax T1 +C | 1 | pituitary | 0.0140 | 0.9122 | 0.3700 |
| GLIOMA01-i_BF76 | Ax T1 +C | 2 | pituitary | 0.0219 | 0.9369 | 0.3011 |
| GLIOMA01-i_BF76 | Ax T1 +C | 3 | pituitary | 0.0426 | 0.9353 | 0.2948 |
| GLIOMA01-i_BF76 | Ax T1 +C | 4 | pituitary | 0.0966 | 0.8797 | 0.4437 |
| GLIOMA01-i_BF76 | Ax T1 +C | 5 | pituitary | 0.0255 | 0.9581 | 0.2133 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 1 | notumor | 0.0772 | 0.6875 | 0.8897 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 2 | notumor | 0.0286 | 0.7374 | 0.7657 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 3 | notumor | 0.0295 | 0.8635 | 0.5234 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 4 | notumor | 0.0401 | 0.8572 | 0.5545 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 5 | notumor | 0.0348 | 0.8708 | 0.5145 |
| GLIOMA01-i_8743 | AX FSE T1 | 1 | pituitary | 0.1653 | 0.5312 | 1.1931 |
| GLIOMA01-i_8743 | AX FSE T1 | 2 | glioma | 0.4163 | 0.4163 | 1.2527 |
| GLIOMA01-i_8743 | AX FSE T1 | 3 | pituitary | 0.3120 | 0.4274 | 1.2340 |
| GLIOMA01-i_8743 | AX FSE T1 | 4 | glioma | 0.4563 | 0.4563 | 1.1489 |
| GLIOMA01-i_8743 | AX FSE T1 | 5 | glioma | 0.7280 | 0.7280 | 0.7376 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 1 | meningioma | 0.0225 | 0.9469 | 0.2536 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 2 | meningioma | 0.0472 | 0.8843 | 0.4455 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 3 | meningioma | 0.0178 | 0.9644 | 0.1848 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 4 | meningioma | 0.0249 | 0.9709 | 0.1467 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 5 | meningioma | 0.0170 | 0.9578 | 0.2205 |

## Interpretation

This report evaluates whether the D1-trained E002 model recognises D3B glioma-domain images as glioma and how confident it is under domain shift. Because D3B labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E002 temperature scaling parameter to these D3B logits/probabilities and compare raw versus calibrated confidence under domain shift.
