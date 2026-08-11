# E001 on D3B Domain-Shift Evaluation

## Experiment

E001 ResNet18 trained on D1 leakage-aware split, evaluated on D3B ICDC-Glioma central slices.

## Inputs

- Checkpoint: `experiments/E001_D1_resnet18_baseline/seed46/best_model.pt`
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
| meningioma | 45 | 0.1698 |
| notumor | 100 | 0.3774 |
| pituitary | 34 | 0.1283 |

## Core D3B Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.3245 |
| Mean glioma probability | 0.3224 |
| Median glioma probability | 0.2060 |
| Mean maximum softmax confidence | 0.6958 |
| Median maximum softmax confidence | 0.6926 |
| Mean entropy | 0.7487 |
| Median entropy | 0.7971 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 16 |
| meningioma | 8 |
| notumor | 23 |
| pituitary | 6 |

Patient-level majority glioma rate: `0.3019`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 16 |
| meningioma | 8 |
| notumor | 23 |
| pituitary | 6 |

Series-level majority glioma rate: `0.3019`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| GLIOMA01-i_6561 | FSPGR 3D | 1 | glioma | 0.7386 | 0.7386 | 0.6351 |
| GLIOMA01-i_6561 | FSPGR 3D | 2 | glioma | 0.7653 | 0.7653 | 0.6082 |
| GLIOMA01-i_6561 | FSPGR 3D | 3 | glioma | 0.6273 | 0.6273 | 0.7498 |
| GLIOMA01-i_6561 | FSPGR 3D | 4 | glioma | 0.5413 | 0.5413 | 0.8303 |
| GLIOMA01-i_6561 | FSPGR 3D | 5 | glioma | 0.5625 | 0.5625 | 0.7987 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 1 | notumor | 0.1864 | 0.3858 | 1.2333 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 2 | meningioma | 0.2902 | 0.5510 | 1.0299 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 3 | meningioma | 0.2796 | 0.6601 | 0.8104 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 4 | meningioma | 0.3429 | 0.5614 | 0.9337 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 5 | notumor | 0.2132 | 0.3835 | 1.1819 |
| GLIOMA01-i_BF76 | Ax T1 +C | 1 | glioma | 0.7845 | 0.7845 | 0.7291 |
| GLIOMA01-i_BF76 | Ax T1 +C | 2 | glioma | 0.6991 | 0.6991 | 0.9417 |
| GLIOMA01-i_BF76 | Ax T1 +C | 3 | pituitary | 0.2958 | 0.3898 | 1.2926 |
| GLIOMA01-i_BF76 | Ax T1 +C | 4 | notumor | 0.3572 | 0.3753 | 1.2684 |
| GLIOMA01-i_BF76 | Ax T1 +C | 5 | glioma | 0.5155 | 0.5155 | 1.1543 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 1 | pituitary | 0.0741 | 0.7836 | 0.6790 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 2 | pituitary | 0.0345 | 0.8360 | 0.5467 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 3 | pituitary | 0.0153 | 0.8369 | 0.5047 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 4 | pituitary | 0.0319 | 0.8287 | 0.5580 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 5 | pituitary | 0.0355 | 0.8392 | 0.5553 |
| GLIOMA01-i_8743 | AX FSE T1 | 1 | glioma | 0.4173 | 0.4173 | 1.1762 |
| GLIOMA01-i_8743 | AX FSE T1 | 2 | glioma | 0.6926 | 0.6926 | 0.8906 |
| GLIOMA01-i_8743 | AX FSE T1 | 3 | glioma | 0.7698 | 0.7698 | 0.7386 |
| GLIOMA01-i_8743 | AX FSE T1 | 4 | glioma | 0.8551 | 0.8551 | 0.4730 |
| GLIOMA01-i_8743 | AX FSE T1 | 5 | glioma | 0.9831 | 0.9831 | 0.0937 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 1 | meningioma | 0.0807 | 0.9175 | 0.2941 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 2 | meningioma | 0.1110 | 0.8845 | 0.3799 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 3 | glioma | 0.5493 | 0.5493 | 0.7354 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 4 | meningioma | 0.0660 | 0.9280 | 0.2819 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 5 | meningioma | 0.0676 | 0.9209 | 0.3116 |

## Interpretation

This report evaluates whether the D1-trained E001 model recognises D3B glioma-domain images as glioma and how confident it is under domain shift. Because D3B labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E001 temperature scaling parameter to these D3B logits/probabilities and compare raw versus calibrated confidence under domain shift.
