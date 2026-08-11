# E002 on D3B Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1 leakage-aware split, evaluated on D3B ICDC-Glioma central slices.

## Inputs

- Checkpoint: `experiments/E002_D1_efficientnet_b0_baseline/seed45/best_model.pt`
- D3B manifest: `data/processed/D3B_selected_slices_manifest_phash.csv`
- D3B slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 83 | 0.3132 |
| meningioma | 27 | 0.1019 |
| notumor | 58 | 0.2189 |
| pituitary | 97 | 0.3660 |

## Core D3B Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.3132 |
| Mean glioma probability | 0.2772 |
| Median glioma probability | 0.1445 |
| Mean maximum softmax confidence | 0.6914 |
| Median maximum softmax confidence | 0.6996 |
| Mean entropy | 0.7973 |
| Median entropy | 0.8574 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 16 |
| meningioma | 6 |
| notumor | 12 |
| pituitary | 19 |

Patient-level majority glioma rate: `0.3019`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 16 |
| meningioma | 6 |
| notumor | 12 |
| pituitary | 19 |

Series-level majority glioma rate: `0.3019`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| GLIOMA01-i_6561 | FSPGR 3D | 1 | glioma | 0.8444 | 0.8444 | 0.5691 |
| GLIOMA01-i_6561 | FSPGR 3D | 2 | glioma | 0.7869 | 0.7869 | 0.6658 |
| GLIOMA01-i_6561 | FSPGR 3D | 3 | glioma | 0.7872 | 0.7872 | 0.6512 |
| GLIOMA01-i_6561 | FSPGR 3D | 4 | glioma | 0.6635 | 0.6635 | 0.8798 |
| GLIOMA01-i_6561 | FSPGR 3D | 5 | glioma | 0.7078 | 0.7078 | 0.7585 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 1 | notumor | 0.2139 | 0.5599 | 1.1112 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 2 | glioma | 0.3656 | 0.3656 | 1.2560 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 3 | notumor | 0.1182 | 0.6456 | 1.0024 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 4 | glioma | 0.5375 | 0.5375 | 1.0668 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 5 | notumor | 0.1810 | 0.5824 | 1.1178 |
| GLIOMA01-i_BF76 | Ax T1 +C | 1 | pituitary | 0.0184 | 0.9307 | 0.3166 |
| GLIOMA01-i_BF76 | Ax T1 +C | 2 | pituitary | 0.2401 | 0.6703 | 0.8878 |
| GLIOMA01-i_BF76 | Ax T1 +C | 3 | pituitary | 0.2366 | 0.6819 | 0.8574 |
| GLIOMA01-i_BF76 | Ax T1 +C | 4 | pituitary | 0.2936 | 0.6648 | 0.7919 |
| GLIOMA01-i_BF76 | Ax T1 +C | 5 | pituitary | 0.1297 | 0.8141 | 0.6320 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 1 | notumor | 0.0664 | 0.7771 | 0.7437 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 2 | notumor | 0.0857 | 0.6658 | 0.9635 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 3 | notumor | 0.0305 | 0.8683 | 0.5098 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 4 | notumor | 0.0719 | 0.7402 | 0.8083 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 5 | notumor | 0.1088 | 0.6152 | 1.0179 |
| GLIOMA01-i_8743 | AX FSE T1 | 1 | notumor | 0.2660 | 0.3345 | 1.3181 |
| GLIOMA01-i_8743 | AX FSE T1 | 2 | glioma | 0.3893 | 0.3893 | 1.2335 |
| GLIOMA01-i_8743 | AX FSE T1 | 3 | pituitary | 0.1599 | 0.4461 | 1.2880 |
| GLIOMA01-i_8743 | AX FSE T1 | 4 | glioma | 0.5768 | 0.5768 | 1.1386 |
| GLIOMA01-i_8743 | AX FSE T1 | 5 | glioma | 0.6928 | 0.6928 | 0.8654 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 1 | meningioma | 0.1607 | 0.7050 | 0.8903 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 2 | meningioma | 0.1475 | 0.8188 | 0.5835 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 3 | meningioma | 0.1179 | 0.8387 | 0.5583 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 4 | meningioma | 0.0206 | 0.9565 | 0.2245 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 5 | meningioma | 0.0273 | 0.9087 | 0.3961 |

## Interpretation

This report evaluates whether the D1-trained E002 model recognises D3B glioma-domain images as glioma and how confident it is under domain shift. Because D3B labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E002 temperature scaling parameter to these D3B logits/probabilities and compare raw versus calibrated confidence under domain shift.
