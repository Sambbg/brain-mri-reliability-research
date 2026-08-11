# E001 on D3B Domain-Shift Evaluation

## Experiment

E001 ResNet18 trained on D1 leakage-aware split, evaluated on D3B ICDC-Glioma central slices.

## Inputs

- Checkpoint: `experiments/E001_D1_resnet18_baseline/seed45/best_model.pt`
- D3B manifest: `data/processed/D3B_selected_slices_manifest_phash.csv`
- D3B slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 157 | 0.5925 |
| meningioma | 29 | 0.1094 |
| notumor | 46 | 0.1736 |
| pituitary | 33 | 0.1245 |

## Core D3B Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.5925 |
| Mean glioma probability | 0.5425 |
| Median glioma probability | 0.6383 |
| Mean maximum softmax confidence | 0.7670 |
| Median maximum softmax confidence | 0.7876 |
| Mean entropy | 0.5757 |
| Median entropy | 0.6199 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 33 |
| meningioma | 5 |
| notumor | 10 |
| pituitary | 5 |

Patient-level majority glioma rate: `0.6226`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 33 |
| meningioma | 5 |
| notumor | 10 |
| pituitary | 5 |

Series-level majority glioma rate: `0.6226`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| GLIOMA01-i_6561 | FSPGR 3D | 1 | glioma | 0.9952 | 0.9952 | 0.0319 |
| GLIOMA01-i_6561 | FSPGR 3D | 2 | glioma | 0.9956 | 0.9956 | 0.0294 |
| GLIOMA01-i_6561 | FSPGR 3D | 3 | glioma | 0.9950 | 0.9950 | 0.0330 |
| GLIOMA01-i_6561 | FSPGR 3D | 4 | glioma | 0.9925 | 0.9925 | 0.0474 |
| GLIOMA01-i_6561 | FSPGR 3D | 5 | glioma | 0.9933 | 0.9933 | 0.0427 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 1 | meningioma | 0.1736 | 0.4550 | 1.2820 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 2 | glioma | 0.6694 | 0.6694 | 0.7582 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 3 | glioma | 0.5135 | 0.5135 | 0.7755 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 4 | glioma | 0.7301 | 0.7301 | 0.6213 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 5 | meningioma | 0.3850 | 0.4618 | 1.0725 |
| GLIOMA01-i_BF76 | Ax T1 +C | 1 | glioma | 0.9916 | 0.9916 | 0.0549 |
| GLIOMA01-i_BF76 | Ax T1 +C | 2 | glioma | 0.9787 | 0.9787 | 0.1241 |
| GLIOMA01-i_BF76 | Ax T1 +C | 3 | glioma | 0.7876 | 0.7876 | 0.7476 |
| GLIOMA01-i_BF76 | Ax T1 +C | 4 | glioma | 0.9381 | 0.9381 | 0.2942 |
| GLIOMA01-i_BF76 | Ax T1 +C | 5 | glioma | 0.9903 | 0.9903 | 0.0624 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 1 | glioma | 0.6305 | 0.6305 | 0.8450 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 2 | glioma | 0.5801 | 0.5801 | 0.9083 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 3 | glioma | 0.4429 | 0.4429 | 0.9784 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 4 | notumor | 0.3426 | 0.4834 | 1.0332 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 5 | notumor | 0.4163 | 0.4832 | 0.9607 |
| GLIOMA01-i_8743 | AX FSE T1 | 1 | glioma | 0.7941 | 0.7941 | 0.6942 |
| GLIOMA01-i_8743 | AX FSE T1 | 2 | glioma | 0.9109 | 0.9109 | 0.3945 |
| GLIOMA01-i_8743 | AX FSE T1 | 3 | glioma | 0.9709 | 0.9709 | 0.1594 |
| GLIOMA01-i_8743 | AX FSE T1 | 4 | glioma | 0.9901 | 0.9901 | 0.0638 |
| GLIOMA01-i_8743 | AX FSE T1 | 5 | glioma | 0.9976 | 0.9976 | 0.0191 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 1 | meningioma | 0.4756 | 0.5006 | 0.8052 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 2 | meningioma | 0.2279 | 0.7458 | 0.6668 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 3 | meningioma | 0.2689 | 0.6890 | 0.7689 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 4 | meningioma | 0.1539 | 0.8094 | 0.5987 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 5 | meningioma | 0.3492 | 0.6378 | 0.7183 |

## Interpretation

This report evaluates whether the D1-trained E001 model recognises D3B glioma-domain images as glioma and how confident it is under domain shift. Because D3B labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E001 temperature scaling parameter to these D3B logits/probabilities and compare raw versus calibrated confidence under domain shift.
