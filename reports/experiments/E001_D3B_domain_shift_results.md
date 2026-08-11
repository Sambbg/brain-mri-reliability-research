# E001 on D3B Domain-Shift Evaluation

## Experiment

E001 ResNet18 trained on D1 leakage-aware split, evaluated on D3B ICDC-Glioma central slices.

## Inputs

- Checkpoint: `experiments/E001_D1_resnet18_baseline/seed42/best_model.pt`
- D3B manifest: `data/processed/D3B_selected_slices_manifest_phash.csv`
- D3B slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 82 | 0.3094 |
| meningioma | 48 | 0.1811 |
| notumor | 115 | 0.4340 |
| pituitary | 20 | 0.0755 |

## Core D3B Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.3094 |
| Mean glioma probability | 0.2970 |
| Median glioma probability | 0.1469 |
| Mean maximum softmax confidence | 0.7020 |
| Median maximum softmax confidence | 0.6944 |
| Mean entropy | 0.7302 |
| Median entropy | 0.7777 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 15 |
| meningioma | 9 |
| notumor | 27 |
| pituitary | 2 |

Patient-level majority glioma rate: `0.2830`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 15 |
| meningioma | 9 |
| notumor | 27 |
| pituitary | 2 |

Series-level majority glioma rate: `0.2830`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| GLIOMA01-i_6561 | FSPGR 3D | 1 | glioma | 0.9660 | 0.9660 | 0.1685 |
| GLIOMA01-i_6561 | FSPGR 3D | 2 | glioma | 0.9687 | 0.9687 | 0.1570 |
| GLIOMA01-i_6561 | FSPGR 3D | 3 | glioma | 0.8880 | 0.8880 | 0.4164 |
| GLIOMA01-i_6561 | FSPGR 3D | 4 | glioma | 0.8799 | 0.8799 | 0.4416 |
| GLIOMA01-i_6561 | FSPGR 3D | 5 | glioma | 0.8877 | 0.8877 | 0.4272 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 1 | notumor | 0.2740 | 0.6529 | 0.8272 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 2 | glioma | 0.9138 | 0.9138 | 0.3476 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 3 | notumor | 0.1460 | 0.4348 | 1.0111 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 4 | meningioma | 0.0554 | 0.8895 | 0.4271 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 5 | notumor | 0.0594 | 0.8144 | 0.6043 |
| GLIOMA01-i_BF76 | Ax T1 +C | 1 | glioma | 0.8753 | 0.8753 | 0.4466 |
| GLIOMA01-i_BF76 | Ax T1 +C | 2 | glioma | 0.8477 | 0.8477 | 0.5600 |
| GLIOMA01-i_BF76 | Ax T1 +C | 3 | meningioma | 0.4415 | 0.4433 | 1.0350 |
| GLIOMA01-i_BF76 | Ax T1 +C | 4 | meningioma | 0.2775 | 0.6495 | 0.8751 |
| GLIOMA01-i_BF76 | Ax T1 +C | 5 | meningioma | 0.3879 | 0.4907 | 1.0536 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 1 | glioma | 0.7837 | 0.7837 | 0.7056 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 2 | glioma | 0.4394 | 0.4394 | 1.0761 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 3 | glioma | 0.5619 | 0.5619 | 0.9340 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 4 | glioma | 0.5470 | 0.5470 | 0.8905 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 5 | pituitary | 0.1978 | 0.6956 | 0.8419 |
| GLIOMA01-i_8743 | AX FSE T1 | 1 | glioma | 0.5291 | 0.5291 | 1.0345 |
| GLIOMA01-i_8743 | AX FSE T1 | 2 | notumor | 0.4107 | 0.5015 | 0.9425 |
| GLIOMA01-i_8743 | AX FSE T1 | 3 | glioma | 0.6546 | 0.6546 | 0.8611 |
| GLIOMA01-i_8743 | AX FSE T1 | 4 | glioma | 0.6489 | 0.6489 | 0.7124 |
| GLIOMA01-i_8743 | AX FSE T1 | 5 | glioma | 0.7927 | 0.7927 | 0.5360 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 1 | meningioma | 0.2333 | 0.7519 | 0.6209 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 2 | meningioma | 0.1469 | 0.8407 | 0.4892 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 3 | meningioma | 0.2632 | 0.7146 | 0.6853 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 4 | meningioma | 0.1349 | 0.8272 | 0.5707 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 5 | meningioma | 0.0172 | 0.9641 | 0.1851 |

## Interpretation

This report evaluates whether the D1-trained E001 model recognises D3B glioma-domain images as glioma and how confident it is under domain shift. Because D3B labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E001 temperature scaling parameter to these D3B logits/probabilities and compare raw versus calibrated confidence under domain shift.
