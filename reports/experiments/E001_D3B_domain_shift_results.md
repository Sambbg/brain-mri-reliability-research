# E001 on D3B Domain-Shift Evaluation

## Experiment

E001 ResNet18 trained on D1 leakage-aware split, evaluated on D3B ICDC-Glioma central slices.

## Inputs

- Checkpoint: `experiments/E001_D1_resnet18_baseline/seed44/best_model.pt`
- D3B manifest: `data/processed/D3B_selected_slices_manifest_phash.csv`
- D3B slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 86 | 0.3245 |
| meningioma | 52 | 0.1962 |
| notumor | 30 | 0.1132 |
| pituitary | 97 | 0.3660 |

## Core D3B Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.3245 |
| Mean glioma probability | 0.3320 |
| Median glioma probability | 0.1474 |
| Mean maximum softmax confidence | 0.7273 |
| Median maximum softmax confidence | 0.7428 |
| Mean entropy | 0.6810 |
| Median entropy | 0.7006 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 17 |
| meningioma | 10 |
| notumor | 6 |
| pituitary | 20 |

Patient-level majority glioma rate: `0.3208`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 17 |
| meningioma | 10 |
| notumor | 6 |
| pituitary | 20 |

Series-level majority glioma rate: `0.3208`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| GLIOMA01-i_6561 | FSPGR 3D | 1 | glioma | 0.9701 | 0.9701 | 0.1548 |
| GLIOMA01-i_6561 | FSPGR 3D | 2 | glioma | 0.9740 | 0.9740 | 0.1358 |
| GLIOMA01-i_6561 | FSPGR 3D | 3 | glioma | 0.9796 | 0.9796 | 0.1128 |
| GLIOMA01-i_6561 | FSPGR 3D | 4 | glioma | 0.9792 | 0.9792 | 0.1183 |
| GLIOMA01-i_6561 | FSPGR 3D | 5 | glioma | 0.9785 | 0.9785 | 0.1196 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 1 | glioma | 0.5779 | 0.5779 | 1.0272 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 2 | meningioma | 0.4670 | 0.4937 | 0.8538 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 3 | meningioma | 0.2598 | 0.7313 | 0.6260 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 4 | meningioma | 0.3674 | 0.5956 | 0.8236 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 5 | meningioma | 0.3342 | 0.5566 | 1.0097 |
| GLIOMA01-i_BF76 | Ax T1 +C | 1 | glioma | 0.5767 | 0.5767 | 1.0289 |
| GLIOMA01-i_BF76 | Ax T1 +C | 2 | pituitary | 0.2574 | 0.4894 | 1.1162 |
| GLIOMA01-i_BF76 | Ax T1 +C | 3 | pituitary | 0.0247 | 0.9010 | 0.4120 |
| GLIOMA01-i_BF76 | Ax T1 +C | 4 | pituitary | 0.1387 | 0.7013 | 0.9205 |
| GLIOMA01-i_BF76 | Ax T1 +C | 5 | pituitary | 0.1334 | 0.6718 | 0.9528 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 1 | pituitary | 0.0145 | 0.5308 | 0.7780 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 2 | notumor | 0.0065 | 0.6013 | 0.7168 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 3 | pituitary | 0.0055 | 0.6514 | 0.6795 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 4 | notumor | 0.0046 | 0.6232 | 0.6953 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 5 | notumor | 0.0083 | 0.6076 | 0.7367 |
| GLIOMA01-i_8743 | AX FSE T1 | 1 | glioma | 0.7197 | 0.7197 | 0.8416 |
| GLIOMA01-i_8743 | AX FSE T1 | 2 | glioma | 0.7602 | 0.7602 | 0.7767 |
| GLIOMA01-i_8743 | AX FSE T1 | 3 | glioma | 0.8758 | 0.8758 | 0.4985 |
| GLIOMA01-i_8743 | AX FSE T1 | 4 | glioma | 0.9781 | 0.9781 | 0.1294 |
| GLIOMA01-i_8743 | AX FSE T1 | 5 | glioma | 0.9795 | 0.9795 | 0.1220 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 1 | meningioma | 0.0062 | 0.9820 | 0.1046 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 2 | meningioma | 0.0917 | 0.7515 | 0.7652 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 3 | meningioma | 0.1189 | 0.8342 | 0.5804 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 4 | meningioma | 0.0204 | 0.9494 | 0.2538 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 5 | meningioma | 0.0186 | 0.9755 | 0.1327 |

## Interpretation

This report evaluates whether the D1-trained E001 model recognises D3B glioma-domain images as glioma and how confident it is under domain shift. Because D3B labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E001 temperature scaling parameter to these D3B logits/probabilities and compare raw versus calibrated confidence under domain shift.
