# E002 on D3B Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1 leakage-aware split, evaluated on D3B ICDC-Glioma central slices.

## Inputs

- Checkpoint: `experiments/E002_D1_efficientnet_b0_baseline/best_model.pt`
- D3B manifest: `data/processed/D3B_selected_slices_manifest_phash.csv`
- D3B slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 117 | 0.4415 |
| meningioma | 34 | 0.1283 |
| notumor | 81 | 0.3057 |
| pituitary | 33 | 0.1245 |

## Core D3B Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.4415 |
| Mean glioma probability | 0.3879 |
| Median glioma probability | 0.3442 |
| Mean maximum softmax confidence | 0.6837 |
| Median maximum softmax confidence | 0.6796 |
| Mean entropy | 0.7970 |
| Median entropy | 0.8386 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 25 |
| meningioma | 5 |
| notumor | 17 |
| pituitary | 6 |

Patient-level majority glioma rate: `0.4717`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 25 |
| meningioma | 5 |
| notumor | 17 |
| pituitary | 6 |

Series-level majority glioma rate: `0.4717`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| GLIOMA01-i_6561 | FSPGR 3D | 1 | glioma | 0.4731 | 0.4731 | 1.0471 |
| GLIOMA01-i_6561 | FSPGR 3D | 2 | meningioma | 0.3487 | 0.5668 | 0.9565 |
| GLIOMA01-i_6561 | FSPGR 3D | 3 | glioma | 0.6765 | 0.6765 | 0.7970 |
| GLIOMA01-i_6561 | FSPGR 3D | 4 | glioma | 0.4982 | 0.4982 | 1.0825 |
| GLIOMA01-i_6561 | FSPGR 3D | 5 | meningioma | 0.2258 | 0.6985 | 0.8317 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 1 | notumor | 0.1575 | 0.7657 | 0.7397 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 2 | glioma | 0.5945 | 0.5945 | 0.9124 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 3 | notumor | 0.0950 | 0.8100 | 0.6767 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 4 | notumor | 0.3147 | 0.5214 | 1.1061 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 5 | notumor | 0.1897 | 0.6796 | 0.9343 |
| GLIOMA01-i_BF76 | Ax T1 +C | 1 | pituitary | 0.3412 | 0.4894 | 1.1037 |
| GLIOMA01-i_BF76 | Ax T1 +C | 2 | glioma | 0.7531 | 0.7531 | 0.7202 |
| GLIOMA01-i_BF76 | Ax T1 +C | 3 | pituitary | 0.3473 | 0.5169 | 1.0327 |
| GLIOMA01-i_BF76 | Ax T1 +C | 4 | pituitary | 0.3746 | 0.6009 | 0.7763 |
| GLIOMA01-i_BF76 | Ax T1 +C | 5 | pituitary | 0.1960 | 0.7042 | 0.8448 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 1 | glioma | 0.4990 | 0.4990 | 1.1140 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 2 | notumor | 0.2968 | 0.4985 | 1.1446 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 3 | glioma | 0.4841 | 0.4841 | 1.0352 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 4 | glioma | 0.4861 | 0.4861 | 1.1196 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 5 | notumor | 0.3442 | 0.5411 | 1.0172 |
| GLIOMA01-i_8743 | AX FSE T1 | 1 | meningioma | 0.1085 | 0.7801 | 0.7514 |
| GLIOMA01-i_8743 | AX FSE T1 | 2 | meningioma | 0.1721 | 0.7107 | 0.8704 |
| GLIOMA01-i_8743 | AX FSE T1 | 3 | meningioma | 0.0513 | 0.8857 | 0.4669 |
| GLIOMA01-i_8743 | AX FSE T1 | 4 | meningioma | 0.1557 | 0.7887 | 0.6715 |
| GLIOMA01-i_8743 | AX FSE T1 | 5 | meningioma | 0.2672 | 0.4503 | 1.1858 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 1 | meningioma | 0.1861 | 0.7102 | 0.8083 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 2 | meningioma | 0.2052 | 0.7890 | 0.5453 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 3 | meningioma | 0.0681 | 0.9209 | 0.3152 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 4 | meningioma | 0.0728 | 0.9180 | 0.3187 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 5 | meningioma | 0.0234 | 0.9713 | 0.1475 |

## Interpretation

This report evaluates whether the D1-trained E002 model recognises D3B glioma-domain images as glioma and how confident it is under domain shift. Because D3B labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E002 temperature scaling parameter to these D3B logits/probabilities and compare raw versus calibrated confidence under domain shift.
