# E002 on D3B Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1 leakage-aware split, evaluated on D3B ICDC-Glioma central slices.

## Inputs

- Checkpoint: `experiments/E002_D1_efficientnet_b0_baseline/seed44/best_model.pt`
- D3B manifest: `data/processed/D3B_selected_slices_manifest_phash.csv`
- D3B slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 101 | 0.3811 |
| meningioma | 56 | 0.2113 |
| notumor | 50 | 0.1887 |
| pituitary | 58 | 0.2189 |

## Core D3B Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.3811 |
| Mean glioma probability | 0.3522 |
| Median glioma probability | 0.2269 |
| Mean maximum softmax confidence | 0.7259 |
| Median maximum softmax confidence | 0.7509 |
| Mean entropy | 0.6866 |
| Median entropy | 0.7194 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 21 |
| meningioma | 11 |
| notumor | 10 |
| pituitary | 11 |

Patient-level majority glioma rate: `0.3962`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 21 |
| meningioma | 11 |
| notumor | 10 |
| pituitary | 11 |

Series-level majority glioma rate: `0.3962`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| GLIOMA01-i_6561 | FSPGR 3D | 1 | meningioma | 0.3687 | 0.6148 | 0.7450 |
| GLIOMA01-i_6561 | FSPGR 3D | 2 | meningioma | 0.2882 | 0.7006 | 0.6651 |
| GLIOMA01-i_6561 | FSPGR 3D | 3 | glioma | 0.5793 | 0.5793 | 0.7581 |
| GLIOMA01-i_6561 | FSPGR 3D | 4 | glioma | 0.5229 | 0.5229 | 0.7946 |
| GLIOMA01-i_6561 | FSPGR 3D | 5 | meningioma | 0.3398 | 0.6471 | 0.7145 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 1 | meningioma | 0.2407 | 0.3760 | 1.3266 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 2 | glioma | 0.8631 | 0.8631 | 0.5245 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 3 | meningioma | 0.1053 | 0.7369 | 0.8224 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 4 | meningioma | 0.4058 | 0.4803 | 1.0079 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 5 | notumor | 0.2722 | 0.6338 | 0.9291 |
| GLIOMA01-i_BF76 | Ax T1 +C | 1 | meningioma | 0.1017 | 0.5122 | 0.9793 |
| GLIOMA01-i_BF76 | Ax T1 +C | 2 | meningioma | 0.2404 | 0.4894 | 1.1000 |
| GLIOMA01-i_BF76 | Ax T1 +C | 3 | pituitary | 0.0441 | 0.8663 | 0.5056 |
| GLIOMA01-i_BF76 | Ax T1 +C | 4 | pituitary | 0.1207 | 0.8431 | 0.5350 |
| GLIOMA01-i_BF76 | Ax T1 +C | 5 | pituitary | 0.1819 | 0.6735 | 0.9344 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 1 | notumor | 0.0241 | 0.9117 | 0.3832 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 2 | notumor | 0.0581 | 0.7858 | 0.7269 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 3 | notumor | 0.0820 | 0.7320 | 0.8552 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 4 | notumor | 0.0616 | 0.7812 | 0.7394 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 5 | notumor | 0.1373 | 0.4833 | 1.1863 |
| GLIOMA01-i_8743 | AX FSE T1 | 1 | glioma | 0.4059 | 0.4059 | 1.1807 |
| GLIOMA01-i_8743 | AX FSE T1 | 2 | glioma | 0.5470 | 0.5470 | 1.1370 |
| GLIOMA01-i_8743 | AX FSE T1 | 3 | glioma | 0.7015 | 0.7015 | 0.8616 |
| GLIOMA01-i_8743 | AX FSE T1 | 4 | glioma | 0.9503 | 0.9503 | 0.2465 |
| GLIOMA01-i_8743 | AX FSE T1 | 5 | glioma | 0.9934 | 0.9934 | 0.0466 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 1 | meningioma | 0.0051 | 0.9896 | 0.0665 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 2 | meningioma | 0.0183 | 0.9803 | 0.1026 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 3 | meningioma | 0.0347 | 0.9552 | 0.2097 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 4 | meningioma | 0.0159 | 0.9796 | 0.1126 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 5 | meningioma | 0.0015 | 0.9965 | 0.0273 |

## Interpretation

This report evaluates whether the D1-trained E002 model recognises D3B glioma-domain images as glioma and how confident it is under domain shift. Because D3B labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E002 temperature scaling parameter to these D3B logits/probabilities and compare raw versus calibrated confidence under domain shift.
