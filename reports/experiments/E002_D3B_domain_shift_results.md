# E002 on D3B Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1 leakage-aware split, evaluated on D3B ICDC-Glioma central slices.

## Inputs

- Checkpoint: `experiments/E002_D1_efficientnet_b0_baseline/seed42/best_model.pt`
- D3B manifest: `data/processed/D3B_selected_slices_manifest_phash.csv`
- D3B slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 158 | 0.5962 |
| meningioma | 29 | 0.1094 |
| notumor | 65 | 0.2453 |
| pituitary | 13 | 0.0491 |

## Core D3B Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.5962 |
| Mean glioma probability | 0.5314 |
| Median glioma probability | 0.5725 |
| Mean maximum softmax confidence | 0.7553 |
| Median maximum softmax confidence | 0.7978 |
| Mean entropy | 0.6298 |
| Median entropy | 0.6247 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 35 |
| meningioma | 4 |
| notumor | 12 |
| pituitary | 2 |

Patient-level majority glioma rate: `0.6604`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 35 |
| meningioma | 4 |
| notumor | 12 |
| pituitary | 2 |

Series-level majority glioma rate: `0.6604`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| GLIOMA01-i_6561 | FSPGR 3D | 1 | glioma | 0.7209 | 0.7209 | 0.7515 |
| GLIOMA01-i_6561 | FSPGR 3D | 2 | glioma | 0.7810 | 0.7810 | 0.6239 |
| GLIOMA01-i_6561 | FSPGR 3D | 3 | glioma | 0.8935 | 0.8935 | 0.3882 |
| GLIOMA01-i_6561 | FSPGR 3D | 4 | glioma | 0.7254 | 0.7254 | 0.7209 |
| GLIOMA01-i_6561 | FSPGR 3D | 5 | meningioma | 0.3833 | 0.5926 | 0.7841 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 1 | glioma | 0.8958 | 0.8958 | 0.3442 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 2 | glioma | 0.9971 | 0.9971 | 0.0228 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 3 | glioma | 0.8436 | 0.8436 | 0.5223 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 4 | glioma | 0.9830 | 0.9830 | 0.1001 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 5 | glioma | 0.9272 | 0.9272 | 0.3183 |
| GLIOMA01-i_BF76 | Ax T1 +C | 1 | glioma | 0.4309 | 0.4309 | 1.1883 |
| GLIOMA01-i_BF76 | Ax T1 +C | 2 | glioma | 0.6652 | 0.6652 | 0.8219 |
| GLIOMA01-i_BF76 | Ax T1 +C | 3 | glioma | 0.8140 | 0.8140 | 0.6160 |
| GLIOMA01-i_BF76 | Ax T1 +C | 4 | glioma | 0.9334 | 0.9334 | 0.2996 |
| GLIOMA01-i_BF76 | Ax T1 +C | 5 | glioma | 0.8662 | 0.8662 | 0.5103 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 1 | notumor | 0.4108 | 0.5493 | 0.8406 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 2 | notumor | 0.1988 | 0.7757 | 0.6247 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 3 | notumor | 0.0780 | 0.8915 | 0.4220 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 4 | notumor | 0.1879 | 0.7751 | 0.6526 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 5 | notumor | 0.1824 | 0.7898 | 0.6112 |
| GLIOMA01-i_8743 | AX FSE T1 | 1 | meningioma | 0.2833 | 0.4321 | 1.1777 |
| GLIOMA01-i_8743 | AX FSE T1 | 2 | glioma | 0.6154 | 0.6154 | 0.9723 |
| GLIOMA01-i_8743 | AX FSE T1 | 3 | meningioma | 0.3133 | 0.3591 | 1.2251 |
| GLIOMA01-i_8743 | AX FSE T1 | 4 | glioma | 0.7481 | 0.7481 | 0.7461 |
| GLIOMA01-i_8743 | AX FSE T1 | 5 | glioma | 0.8690 | 0.8690 | 0.4674 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 1 | glioma | 0.4513 | 0.4513 | 1.0346 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 2 | glioma | 0.8022 | 0.8022 | 0.5154 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 3 | meningioma | 0.2411 | 0.5440 | 1.0228 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 4 | meningioma | 0.2251 | 0.7293 | 0.7277 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 5 | meningioma | 0.2408 | 0.6530 | 0.9268 |

## Interpretation

This report evaluates whether the D1-trained E002 model recognises D3B glioma-domain images as glioma and how confident it is under domain shift. Because D3B labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E002 temperature scaling parameter to these D3B logits/probabilities and compare raw versus calibrated confidence under domain shift.
