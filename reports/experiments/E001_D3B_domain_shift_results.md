# E001 on D3B Domain-Shift Evaluation

## Experiment

E001 ResNet18 trained on D1 leakage-aware split, evaluated on D3B ICDC-Glioma central slices.

## Inputs

- Checkpoint: `experiments/E001_D1_resnet18_baseline/best_model.pt`
- D3B manifest: `data/processed/D3B_selected_slices_manifest_phash.csv`
- D3B slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 78 | 0.2943 |
| meningioma | 79 | 0.2981 |
| notumor | 35 | 0.1321 |
| pituitary | 73 | 0.2755 |

## Core D3B Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.2943 |
| Mean glioma probability | 0.2936 |
| Median glioma probability | 0.1478 |
| Mean maximum softmax confidence | 0.7209 |
| Median maximum softmax confidence | 0.7263 |
| Mean entropy | 0.7157 |
| Median entropy | 0.7693 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 14 |
| meningioma | 18 |
| notumor | 6 |
| pituitary | 15 |

Patient-level majority glioma rate: `0.2642`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 14 |
| meningioma | 18 |
| notumor | 6 |
| pituitary | 15 |

Series-level majority glioma rate: `0.2642`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| GLIOMA01-i_6561 | FSPGR 3D | 1 | glioma | 0.5652 | 0.5652 | 0.9825 |
| GLIOMA01-i_6561 | FSPGR 3D | 2 | meningioma | 0.3601 | 0.5324 | 0.9622 |
| GLIOMA01-i_6561 | FSPGR 3D | 3 | meningioma | 0.3906 | 0.4427 | 1.0494 |
| GLIOMA01-i_6561 | FSPGR 3D | 4 | meningioma | 0.3037 | 0.3679 | 1.1167 |
| GLIOMA01-i_6561 | FSPGR 3D | 5 | meningioma | 0.2027 | 0.4019 | 1.0773 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 1 | pituitary | 0.0519 | 0.4224 | 1.1858 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 2 | meningioma | 0.1793 | 0.7678 | 0.6956 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 3 | meningioma | 0.0815 | 0.7174 | 0.9032 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 4 | meningioma | 0.0280 | 0.8147 | 0.6141 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 5 | meningioma | 0.0229 | 0.7119 | 0.7725 |
| GLIOMA01-i_BF76 | Ax T1 +C | 1 | pituitary | 0.2789 | 0.5481 | 1.0386 |
| GLIOMA01-i_BF76 | Ax T1 +C | 2 | pituitary | 0.2672 | 0.5669 | 1.0449 |
| GLIOMA01-i_BF76 | Ax T1 +C | 3 | pituitary | 0.1674 | 0.5843 | 1.0391 |
| GLIOMA01-i_BF76 | Ax T1 +C | 4 | pituitary | 0.0748 | 0.8706 | 0.5062 |
| GLIOMA01-i_BF76 | Ax T1 +C | 5 | glioma | 0.5569 | 0.5569 | 0.9264 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 1 | notumor | 0.0262 | 0.9102 | 0.3609 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 2 | notumor | 0.0112 | 0.9669 | 0.1683 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 3 | notumor | 0.0133 | 0.9392 | 0.2630 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 4 | notumor | 0.0238 | 0.8597 | 0.4766 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 5 | notumor | 0.0470 | 0.8694 | 0.4856 |
| GLIOMA01-i_8743 | AX FSE T1 | 1 | glioma | 0.4389 | 0.4389 | 1.0928 |
| GLIOMA01-i_8743 | AX FSE T1 | 2 | glioma | 0.5353 | 0.5353 | 1.1744 |
| GLIOMA01-i_8743 | AX FSE T1 | 3 | glioma | 0.6541 | 0.6541 | 1.0203 |
| GLIOMA01-i_8743 | AX FSE T1 | 4 | glioma | 0.9284 | 0.9284 | 0.3290 |
| GLIOMA01-i_8743 | AX FSE T1 | 5 | glioma | 0.9549 | 0.9549 | 0.2290 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 1 | meningioma | 0.2384 | 0.5251 | 1.0823 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 2 | meningioma | 0.3097 | 0.6586 | 0.7693 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 3 | meningioma | 0.1524 | 0.7798 | 0.6841 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 4 | meningioma | 0.0941 | 0.8316 | 0.5928 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 5 | meningioma | 0.0135 | 0.9609 | 0.1948 |

## Interpretation

This report evaluates whether the D1-trained E001 model recognises D3B glioma-domain images as glioma and how confident it is under domain shift. Because D3B labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E001 temperature scaling parameter to these D3B logits/probabilities and compare raw versus calibrated confidence under domain shift.
