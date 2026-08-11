# E003 on D3B Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1 leakage-aware split, evaluated on D3B ICDC-Glioma central slices.

## Inputs

- Checkpoint: `experiments/E003_D1_vit_b16_baseline/seed45/best_model.pt`
- D3B manifest: `data/processed/D3B_selected_slices_manifest_phash.csv`
- D3B slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 75 | 0.2830 |
| meningioma | 45 | 0.1698 |
| notumor | 145 | 0.5472 |
| pituitary | 0 | 0.0000 |

## Core D3B Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.2830 |
| Mean glioma probability | 0.3121 |
| Median glioma probability | 0.1847 |
| Mean maximum softmax confidence | 0.8172 |
| Median maximum softmax confidence | 0.8643 |
| Mean entropy | 0.4580 |
| Median entropy | 0.4636 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 13 |
| meningioma | 9 |
| notumor | 31 |
| pituitary | 0 |

Patient-level majority glioma rate: `0.2453`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 13 |
| meningioma | 9 |
| notumor | 31 |
| pituitary | 0 |

Series-level majority glioma rate: `0.2453`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| GLIOMA01-i_6561 | FSPGR 3D | 1 | notumor | 0.0162 | 0.9579 | 0.2062 |
| GLIOMA01-i_6561 | FSPGR 3D | 2 | notumor | 0.0078 | 0.9896 | 0.0643 |
| GLIOMA01-i_6561 | FSPGR 3D | 3 | notumor | 0.0029 | 0.9964 | 0.0262 |
| GLIOMA01-i_6561 | FSPGR 3D | 4 | notumor | 0.0013 | 0.9982 | 0.0144 |
| GLIOMA01-i_6561 | FSPGR 3D | 5 | notumor | 0.0029 | 0.9959 | 0.0296 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 1 | notumor | 0.0035 | 0.9963 | 0.0255 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 2 | notumor | 0.0084 | 0.9894 | 0.0645 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 3 | notumor | 0.0166 | 0.9705 | 0.1542 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 4 | meningioma | 0.3149 | 0.4314 | 1.0777 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 5 | notumor | 0.0243 | 0.9731 | 0.1328 |
| GLIOMA01-i_BF76 | Ax T1 +C | 1 | glioma | 0.7992 | 0.7992 | 0.6403 |
| GLIOMA01-i_BF76 | Ax T1 +C | 2 | glioma | 0.6192 | 0.6192 | 0.7720 |
| GLIOMA01-i_BF76 | Ax T1 +C | 3 | meningioma | 0.3494 | 0.5528 | 0.9278 |
| GLIOMA01-i_BF76 | Ax T1 +C | 4 | meningioma | 0.3589 | 0.6248 | 0.7331 |
| GLIOMA01-i_BF76 | Ax T1 +C | 5 | glioma | 0.7330 | 0.7330 | 0.6399 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 1 | glioma | 0.7555 | 0.7555 | 0.5817 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 2 | glioma | 0.4970 | 0.4970 | 0.7351 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 3 | notumor | 0.3636 | 0.6285 | 0.7028 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 4 | notumor | 0.4013 | 0.5935 | 0.7069 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 5 | notumor | 0.2144 | 0.7818 | 0.5465 |
| GLIOMA01-i_8743 | AX FSE T1 | 1 | glioma | 0.6307 | 0.6307 | 0.7258 |
| GLIOMA01-i_8743 | AX FSE T1 | 2 | glioma | 0.8456 | 0.8456 | 0.4636 |
| GLIOMA01-i_8743 | AX FSE T1 | 3 | glioma | 0.9344 | 0.9344 | 0.2493 |
| GLIOMA01-i_8743 | AX FSE T1 | 4 | glioma | 0.7263 | 0.7263 | 0.5955 |
| GLIOMA01-i_8743 | AX FSE T1 | 5 | notumor | 0.4297 | 0.5680 | 0.6991 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 1 | notumor | 0.3194 | 0.6101 | 0.8675 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 2 | notumor | 0.1996 | 0.7420 | 0.7229 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 3 | notumor | 0.0856 | 0.9108 | 0.3169 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 4 | meningioma | 0.2954 | 0.4300 | 1.0891 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 5 | meningioma | 0.1472 | 0.7491 | 0.7383 |

## Interpretation

This report evaluates whether the D1-trained E003 model recognises D3B glioma-domain images as glioma and how confident it is under domain shift. Because D3B labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E003 temperature scaling parameter to these D3B logits/probabilities and compare raw versus calibrated confidence under domain shift.
