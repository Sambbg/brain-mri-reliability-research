# E002 on D3B Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1 leakage-aware split, evaluated on D3B ICDC-Glioma central slices.

## Inputs

- Checkpoint: `experiments/E002_D1_efficientnet_b0_baseline/seed46/best_model.pt`
- D3B manifest: `data/processed/D3B_selected_slices_manifest_phash.csv`
- D3B slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 87 | 0.3283 |
| meningioma | 60 | 0.2264 |
| notumor | 41 | 0.1547 |
| pituitary | 77 | 0.2906 |

## Core D3B Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.3283 |
| Mean glioma probability | 0.3144 |
| Median glioma probability | 0.1656 |
| Mean maximum softmax confidence | 0.7135 |
| Median maximum softmax confidence | 0.7122 |
| Mean entropy | 0.7112 |
| Median entropy | 0.7610 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 19 |
| meningioma | 10 |
| notumor | 8 |
| pituitary | 16 |

Patient-level majority glioma rate: `0.3585`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 19 |
| meningioma | 10 |
| notumor | 8 |
| pituitary | 16 |

Series-level majority glioma rate: `0.3585`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| GLIOMA01-i_6561 | FSPGR 3D | 1 | meningioma | 0.1137 | 0.4571 | 1.1603 |
| GLIOMA01-i_6561 | FSPGR 3D | 2 | notumor | 0.1652 | 0.4513 | 1.1918 |
| GLIOMA01-i_6561 | FSPGR 3D | 3 | notumor | 0.1818 | 0.4260 | 1.2024 |
| GLIOMA01-i_6561 | FSPGR 3D | 4 | notumor | 0.1124 | 0.4384 | 1.1013 |
| GLIOMA01-i_6561 | FSPGR 3D | 5 | meningioma | 0.0919 | 0.7006 | 0.9122 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 1 | glioma | 0.5630 | 0.5630 | 1.0810 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 2 | glioma | 0.6424 | 0.6424 | 1.0315 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 3 | meningioma | 0.1892 | 0.7105 | 0.8482 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 4 | glioma | 0.6989 | 0.6989 | 0.9123 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 5 | meningioma | 0.2888 | 0.4028 | 1.3014 |
| GLIOMA01-i_BF76 | Ax T1 +C | 1 | meningioma | 0.0056 | 0.9858 | 0.0851 |
| GLIOMA01-i_BF76 | Ax T1 +C | 2 | meningioma | 0.1535 | 0.4769 | 1.0334 |
| GLIOMA01-i_BF76 | Ax T1 +C | 3 | pituitary | 0.0193 | 0.8846 | 0.4174 |
| GLIOMA01-i_BF76 | Ax T1 +C | 4 | pituitary | 0.1539 | 0.8224 | 0.5436 |
| GLIOMA01-i_BF76 | Ax T1 +C | 5 | pituitary | 0.0247 | 0.7433 | 0.6862 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 1 | notumor | 0.2434 | 0.6669 | 0.8901 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 2 | notumor | 0.0319 | 0.9354 | 0.3024 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 3 | notumor | 0.0715 | 0.8765 | 0.4889 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 4 | notumor | 0.0991 | 0.8542 | 0.5341 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 5 | notumor | 0.0446 | 0.9195 | 0.3561 |
| GLIOMA01-i_8743 | AX FSE T1 | 1 | notumor | 0.1831 | 0.3515 | 1.3546 |
| GLIOMA01-i_8743 | AX FSE T1 | 2 | notumor | 0.2593 | 0.4224 | 1.2948 |
| GLIOMA01-i_8743 | AX FSE T1 | 3 | pituitary | 0.1630 | 0.3430 | 1.3477 |
| GLIOMA01-i_8743 | AX FSE T1 | 4 | notumor | 0.3571 | 0.3619 | 1.2840 |
| GLIOMA01-i_8743 | AX FSE T1 | 5 | glioma | 0.6307 | 0.6307 | 0.9890 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 1 | meningioma | 0.2315 | 0.4718 | 1.0883 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 2 | meningioma | 0.0519 | 0.8885 | 0.4470 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 3 | meningioma | 0.0088 | 0.9863 | 0.0831 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 4 | meningioma | 0.0051 | 0.9917 | 0.0551 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 5 | meningioma | 0.0069 | 0.9842 | 0.0979 |

## Interpretation

This report evaluates whether the D1-trained E002 model recognises D3B glioma-domain images as glioma and how confident it is under domain shift. Because D3B labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E002 temperature scaling parameter to these D3B logits/probabilities and compare raw versus calibrated confidence under domain shift.
