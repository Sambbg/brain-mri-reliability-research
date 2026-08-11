# E003 on D3B Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1 leakage-aware split, evaluated on D3B ICDC-Glioma central slices.

## Inputs

- Checkpoint: `experiments/E003_D1_vit_b16_baseline/seed43/best_model.pt`
- D3B manifest: `data/processed/D3B_selected_slices_manifest_phash.csv`
- D3B slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 65 | 0.2453 |
| meningioma | 65 | 0.2453 |
| notumor | 131 | 0.4943 |
| pituitary | 4 | 0.0151 |

## Core D3B Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.2453 |
| Mean glioma probability | 0.2557 |
| Median glioma probability | 0.1100 |
| Mean maximum softmax confidence | 0.7965 |
| Median maximum softmax confidence | 0.8565 |
| Mean entropy | 0.5312 |
| Median entropy | 0.5022 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 14 |
| meningioma | 14 |
| notumor | 25 |
| pituitary | 0 |

Patient-level majority glioma rate: `0.2642`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 14 |
| meningioma | 14 |
| notumor | 25 |
| pituitary | 0 |

Series-level majority glioma rate: `0.2642`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| GLIOMA01-i_6561 | FSPGR 3D | 1 | notumor | 0.2378 | 0.6722 | 0.8445 |
| GLIOMA01-i_6561 | FSPGR 3D | 2 | notumor | 0.3288 | 0.6287 | 0.8045 |
| GLIOMA01-i_6561 | FSPGR 3D | 3 | notumor | 0.0796 | 0.8973 | 0.3937 |
| GLIOMA01-i_6561 | FSPGR 3D | 4 | notumor | 0.0859 | 0.8258 | 0.5992 |
| GLIOMA01-i_6561 | FSPGR 3D | 5 | notumor | 0.1568 | 0.7386 | 0.7771 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 1 | notumor | 0.0488 | 0.9247 | 0.3242 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 2 | notumor | 0.0546 | 0.9148 | 0.3514 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 3 | meningioma | 0.1410 | 0.8397 | 0.5009 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 4 | meningioma | 0.4842 | 0.5068 | 0.7398 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 5 | meningioma | 0.0414 | 0.9366 | 0.2787 |
| GLIOMA01-i_BF76 | Ax T1 +C | 1 | glioma | 0.6004 | 0.6004 | 1.0073 |
| GLIOMA01-i_BF76 | Ax T1 +C | 2 | glioma | 0.5886 | 0.5886 | 0.9956 |
| GLIOMA01-i_BF76 | Ax T1 +C | 3 | meningioma | 0.3441 | 0.4646 | 1.0638 |
| GLIOMA01-i_BF76 | Ax T1 +C | 4 | glioma | 0.5548 | 0.5548 | 0.8971 |
| GLIOMA01-i_BF76 | Ax T1 +C | 5 | glioma | 0.4635 | 0.4635 | 1.0714 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 1 | notumor | 0.0147 | 0.9603 | 0.2055 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 2 | notumor | 0.0283 | 0.8440 | 0.5613 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 3 | notumor | 0.0385 | 0.9117 | 0.3838 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 4 | notumor | 0.0219 | 0.9597 | 0.2076 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 5 | notumor | 0.0049 | 0.9886 | 0.0745 |
| GLIOMA01-i_8743 | AX FSE T1 | 1 | notumor | 0.4086 | 0.5118 | 0.9450 |
| GLIOMA01-i_8743 | AX FSE T1 | 2 | glioma | 0.5643 | 0.5643 | 0.9565 |
| GLIOMA01-i_8743 | AX FSE T1 | 3 | glioma | 0.7478 | 0.7478 | 0.6144 |
| GLIOMA01-i_8743 | AX FSE T1 | 4 | glioma | 0.6663 | 0.6663 | 0.6568 |
| GLIOMA01-i_8743 | AX FSE T1 | 5 | glioma | 0.9873 | 0.9873 | 0.0717 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 1 | glioma | 0.5746 | 0.5746 | 0.9905 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 2 | glioma | 0.4838 | 0.4838 | 1.0039 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 3 | glioma | 0.6351 | 0.6351 | 0.9199 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 4 | meningioma | 0.1212 | 0.6748 | 0.8611 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 5 | meningioma | 0.1630 | 0.7999 | 0.6011 |

## Interpretation

This report evaluates whether the D1-trained E003 model recognises D3B glioma-domain images as glioma and how confident it is under domain shift. Because D3B labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E003 temperature scaling parameter to these D3B logits/probabilities and compare raw versus calibrated confidence under domain shift.
