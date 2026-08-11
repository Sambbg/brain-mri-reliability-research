# E003 on D3B Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1 leakage-aware split, evaluated on D3B ICDC-Glioma central slices.

## Inputs

- Checkpoint: `experiments/E003_D1_vit_b16_baseline/seed46/best_model.pt`
- D3B manifest: `data/processed/D3B_selected_slices_manifest_phash.csv`
- D3B slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 40 | 0.1509 |
| meningioma | 123 | 0.4642 |
| notumor | 101 | 0.3811 |
| pituitary | 1 | 0.0038 |

## Core D3B Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.1509 |
| Mean glioma probability | 0.1810 |
| Median glioma probability | 0.0718 |
| Mean maximum softmax confidence | 0.7989 |
| Median maximum softmax confidence | 0.8506 |
| Mean entropy | 0.5000 |
| Median entropy | 0.5016 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 7 |
| meningioma | 26 |
| notumor | 20 |
| pituitary | 0 |

Patient-level majority glioma rate: `0.1321`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 7 |
| meningioma | 26 |
| notumor | 20 |
| pituitary | 0 |

Series-level majority glioma rate: `0.1321`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| GLIOMA01-i_6561 | FSPGR 3D | 1 | notumor | 0.0135 | 0.7609 | 0.6055 |
| GLIOMA01-i_6561 | FSPGR 3D | 2 | notumor | 0.0136 | 0.5412 | 0.7550 |
| GLIOMA01-i_6561 | FSPGR 3D | 3 | notumor | 0.0114 | 0.5769 | 0.7367 |
| GLIOMA01-i_6561 | FSPGR 3D | 4 | notumor | 0.0086 | 0.5153 | 0.7386 |
| GLIOMA01-i_6561 | FSPGR 3D | 5 | notumor | 0.0090 | 0.5504 | 0.7354 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 1 | notumor | 0.0016 | 0.9979 | 0.0162 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 2 | notumor | 0.1171 | 0.8438 | 0.5237 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 3 | meningioma | 0.0175 | 0.9808 | 0.1009 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 4 | meningioma | 0.0912 | 0.9044 | 0.3341 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 5 | meningioma | 0.4346 | 0.4964 | 0.8993 |
| GLIOMA01-i_BF76 | Ax T1 +C | 1 | meningioma | 0.3247 | 0.6692 | 0.6687 |
| GLIOMA01-i_BF76 | Ax T1 +C | 2 | meningioma | 0.0861 | 0.9095 | 0.3240 |
| GLIOMA01-i_BF76 | Ax T1 +C | 3 | meningioma | 0.3683 | 0.6172 | 0.7329 |
| GLIOMA01-i_BF76 | Ax T1 +C | 4 | meningioma | 0.3876 | 0.6070 | 0.7022 |
| GLIOMA01-i_BF76 | Ax T1 +C | 5 | meningioma | 0.2863 | 0.7083 | 0.6343 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 1 | notumor | 0.0453 | 0.5570 | 0.9254 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 2 | meningioma | 0.0274 | 0.4954 | 0.9429 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 3 | notumor | 0.0189 | 0.7125 | 0.7277 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 4 | notumor | 0.0048 | 0.9822 | 0.1059 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 5 | notumor | 0.0008 | 0.9974 | 0.0212 |
| GLIOMA01-i_8743 | AX FSE T1 | 1 | glioma | 0.5704 | 0.5704 | 0.8530 |
| GLIOMA01-i_8743 | AX FSE T1 | 2 | meningioma | 0.3562 | 0.6340 | 0.7038 |
| GLIOMA01-i_8743 | AX FSE T1 | 3 | glioma | 0.8723 | 0.8723 | 0.4623 |
| GLIOMA01-i_8743 | AX FSE T1 | 4 | glioma | 0.6241 | 0.6241 | 0.6764 |
| GLIOMA01-i_8743 | AX FSE T1 | 5 | glioma | 0.5004 | 0.5004 | 0.7080 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 1 | meningioma | 0.0433 | 0.9212 | 0.3318 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 2 | meningioma | 0.1323 | 0.7823 | 0.6722 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 3 | meningioma | 0.1532 | 0.6218 | 0.9219 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 4 | meningioma | 0.0172 | 0.9710 | 0.1516 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 5 | meningioma | 0.0770 | 0.8896 | 0.4162 |

## Interpretation

This report evaluates whether the D1-trained E003 model recognises D3B glioma-domain images as glioma and how confident it is under domain shift. Because D3B labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E003 temperature scaling parameter to these D3B logits/probabilities and compare raw versus calibrated confidence under domain shift.
