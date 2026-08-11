# E003 on D3B Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1 leakage-aware split, evaluated on D3B ICDC-Glioma central slices.

## Inputs

- Checkpoint: `experiments/E003_D1_vit_b16_baseline/seed42/best_model.pt`
- D3B manifest: `data/processed/D3B_selected_slices_manifest_phash.csv`
- D3B slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 63 | 0.2377 |
| meningioma | 116 | 0.4377 |
| notumor | 72 | 0.2717 |
| pituitary | 14 | 0.0528 |

## Core D3B Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.2377 |
| Mean glioma probability | 0.2623 |
| Median glioma probability | 0.1052 |
| Mean maximum softmax confidence | 0.7460 |
| Median maximum softmax confidence | 0.7631 |
| Mean entropy | 0.6224 |
| Median entropy | 0.6770 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 11 |
| meningioma | 24 |
| notumor | 15 |
| pituitary | 3 |

Patient-level majority glioma rate: `0.2075`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 11 |
| meningioma | 24 |
| notumor | 15 |
| pituitary | 3 |

Series-level majority glioma rate: `0.2075`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| GLIOMA01-i_6561 | FSPGR 3D | 1 | meningioma | 0.0106 | 0.7352 | 0.6599 |
| GLIOMA01-i_6561 | FSPGR 3D | 2 | meningioma | 0.0123 | 0.6823 | 0.7133 |
| GLIOMA01-i_6561 | FSPGR 3D | 3 | notumor | 0.0098 | 0.5247 | 0.7799 |
| GLIOMA01-i_6561 | FSPGR 3D | 4 | notumor | 0.0054 | 0.5530 | 0.7528 |
| GLIOMA01-i_6561 | FSPGR 3D | 5 | meningioma | 0.0063 | 0.6216 | 0.7484 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 1 | meningioma | 0.2659 | 0.5253 | 1.0291 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 2 | meningioma | 0.1935 | 0.6811 | 0.8580 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 3 | meningioma | 0.0321 | 0.9619 | 0.1812 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 4 | meningioma | 0.3509 | 0.6448 | 0.6770 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 5 | glioma | 0.5470 | 0.5470 | 1.0077 |
| GLIOMA01-i_BF76 | Ax T1 +C | 1 | meningioma | 0.1091 | 0.8860 | 0.3782 |
| GLIOMA01-i_BF76 | Ax T1 +C | 2 | meningioma | 0.0562 | 0.9206 | 0.3298 |
| GLIOMA01-i_BF76 | Ax T1 +C | 3 | meningioma | 0.4003 | 0.5930 | 0.7123 |
| GLIOMA01-i_BF76 | Ax T1 +C | 4 | meningioma | 0.4923 | 0.5012 | 0.7318 |
| GLIOMA01-i_BF76 | Ax T1 +C | 5 | glioma | 0.5408 | 0.5408 | 0.7648 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 1 | notumor | 0.0242 | 0.9652 | 0.1767 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 2 | notumor | 0.0060 | 0.9841 | 0.0950 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 3 | notumor | 0.0027 | 0.9942 | 0.0407 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 4 | notumor | 0.0032 | 0.9918 | 0.0546 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 5 | notumor | 0.0015 | 0.9961 | 0.0290 |
| GLIOMA01-i_8743 | AX FSE T1 | 1 | notumor | 0.0326 | 0.5936 | 0.8726 |
| GLIOMA01-i_8743 | AX FSE T1 | 2 | meningioma | 0.0236 | 0.8241 | 0.6351 |
| GLIOMA01-i_8743 | AX FSE T1 | 3 | notumor | 0.1759 | 0.7401 | 0.7865 |
| GLIOMA01-i_8743 | AX FSE T1 | 4 | glioma | 0.9854 | 0.9854 | 0.0855 |
| GLIOMA01-i_8743 | AX FSE T1 | 5 | glioma | 0.9583 | 0.9583 | 0.1878 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 1 | notumor | 0.0738 | 0.7748 | 0.6785 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 2 | notumor | 0.0748 | 0.4743 | 0.9125 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 3 | notumor | 0.0276 | 0.8025 | 0.5813 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 4 | notumor | 0.0320 | 0.7401 | 0.6725 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 5 | notumor | 0.1052 | 0.5007 | 0.9535 |

## Interpretation

This report evaluates whether the D1-trained E003 model recognises D3B glioma-domain images as glioma and how confident it is under domain shift. Because D3B labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E003 temperature scaling parameter to these D3B logits/probabilities and compare raw versus calibrated confidence under domain shift.
