# E001 on D3B Domain-Shift Evaluation

## Experiment

E001 ResNet18 trained on D1 leakage-aware split, evaluated on D3B ICDC-Glioma central slices.

## Inputs

- Checkpoint: `experiments/E001_D1_resnet18_baseline/seed43/best_model.pt`
- D3B manifest: `data/processed/D3B_selected_slices_manifest_phash.csv`
- D3B slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 122 | 0.4604 |
| meningioma | 51 | 0.1925 |
| notumor | 55 | 0.2075 |
| pituitary | 37 | 0.1396 |

## Core D3B Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.4604 |
| Mean glioma probability | 0.3977 |
| Median glioma probability | 0.3495 |
| Mean maximum softmax confidence | 0.6769 |
| Median maximum softmax confidence | 0.6682 |
| Mean entropy | 0.7902 |
| Median entropy | 0.8507 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 27 |
| meningioma | 10 |
| notumor | 10 |
| pituitary | 6 |

Patient-level majority glioma rate: `0.5094`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 27 |
| meningioma | 10 |
| notumor | 10 |
| pituitary | 6 |

Series-level majority glioma rate: `0.5094`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| GLIOMA01-i_6561 | FSPGR 3D | 1 | glioma | 0.9204 | 0.9204 | 0.3242 |
| GLIOMA01-i_6561 | FSPGR 3D | 2 | glioma | 0.9128 | 0.9128 | 0.3351 |
| GLIOMA01-i_6561 | FSPGR 3D | 3 | glioma | 0.8458 | 0.8458 | 0.5084 |
| GLIOMA01-i_6561 | FSPGR 3D | 4 | glioma | 0.8948 | 0.8948 | 0.4005 |
| GLIOMA01-i_6561 | FSPGR 3D | 5 | glioma | 0.8937 | 0.8937 | 0.4028 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 1 | glioma | 0.7943 | 0.7943 | 0.6477 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 2 | glioma | 0.5071 | 0.5071 | 1.0747 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 3 | glioma | 0.5862 | 0.5862 | 0.8703 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 4 | glioma | 0.5227 | 0.5227 | 0.8190 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 5 | glioma | 0.6157 | 0.6157 | 0.9475 |
| GLIOMA01-i_BF76 | Ax T1 +C | 1 | glioma | 0.7862 | 0.7862 | 0.6979 |
| GLIOMA01-i_BF76 | Ax T1 +C | 2 | glioma | 0.6447 | 0.6447 | 1.0323 |
| GLIOMA01-i_BF76 | Ax T1 +C | 3 | notumor | 0.2580 | 0.3773 | 1.3378 |
| GLIOMA01-i_BF76 | Ax T1 +C | 4 | glioma | 0.4358 | 0.4358 | 1.2959 |
| GLIOMA01-i_BF76 | Ax T1 +C | 5 | glioma | 0.5688 | 0.5688 | 1.1219 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 1 | pituitary | 0.0038 | 0.9894 | 0.0696 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 2 | pituitary | 0.0045 | 0.9892 | 0.0703 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 3 | pituitary | 0.0022 | 0.9944 | 0.0405 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 4 | pituitary | 0.0010 | 0.9952 | 0.0354 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 5 | pituitary | 0.0050 | 0.9857 | 0.0907 |
| GLIOMA01-i_8743 | AX FSE T1 | 1 | glioma | 0.7490 | 0.7490 | 0.6824 |
| GLIOMA01-i_8743 | AX FSE T1 | 2 | glioma | 0.8014 | 0.8014 | 0.5905 |
| GLIOMA01-i_8743 | AX FSE T1 | 3 | glioma | 0.8959 | 0.8959 | 0.4022 |
| GLIOMA01-i_8743 | AX FSE T1 | 4 | glioma | 0.9553 | 0.9553 | 0.2212 |
| GLIOMA01-i_8743 | AX FSE T1 | 5 | glioma | 0.9786 | 0.9786 | 0.1220 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 1 | meningioma | 0.2663 | 0.6682 | 0.8201 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 2 | meningioma | 0.0600 | 0.8212 | 0.6002 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 3 | meningioma | 0.2273 | 0.5701 | 0.9911 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 4 | meningioma | 0.0652 | 0.8995 | 0.3945 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 5 | meningioma | 0.0194 | 0.9487 | 0.2378 |

## Interpretation

This report evaluates whether the D1-trained E001 model recognises D3B glioma-domain images as glioma and how confident it is under domain shift. Because D3B labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E001 temperature scaling parameter to these D3B logits/probabilities and compare raw versus calibrated confidence under domain shift.
