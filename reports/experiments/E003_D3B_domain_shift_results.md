# E003 on D3B Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1 leakage-aware split, evaluated on D3B ICDC-Glioma central slices.

## Inputs

- Checkpoint: `experiments/E003_D1_vit_b16_baseline/seed44/best_model.pt`
- D3B manifest: `data/processed/D3B_selected_slices_manifest_phash.csv`
- D3B slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 87 | 0.3283 |
| meningioma | 37 | 0.1396 |
| notumor | 121 | 0.4566 |
| pituitary | 20 | 0.0755 |

## Core D3B Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.3283 |
| Mean glioma probability | 0.3215 |
| Median glioma probability | 0.1840 |
| Mean maximum softmax confidence | 0.7519 |
| Median maximum softmax confidence | 0.7652 |
| Mean entropy | 0.6297 |
| Median entropy | 0.6919 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 18 |
| meningioma | 8 |
| notumor | 24 |
| pituitary | 3 |

Patient-level majority glioma rate: `0.3396`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 18 |
| meningioma | 8 |
| notumor | 24 |
| pituitary | 3 |

Series-level majority glioma rate: `0.3396`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| GLIOMA01-i_6561 | FSPGR 3D | 1 | glioma | 0.8124 | 0.8124 | 0.5897 |
| GLIOMA01-i_6561 | FSPGR 3D | 2 | glioma | 0.8414 | 0.8414 | 0.5117 |
| GLIOMA01-i_6561 | FSPGR 3D | 3 | glioma | 0.6635 | 0.6635 | 0.7403 |
| GLIOMA01-i_6561 | FSPGR 3D | 4 | glioma | 0.5279 | 0.5279 | 0.8374 |
| GLIOMA01-i_6561 | FSPGR 3D | 5 | glioma | 0.5115 | 0.5115 | 0.9504 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 1 | notumor | 0.2480 | 0.4341 | 1.1141 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 2 | meningioma | 0.0577 | 0.8731 | 0.4972 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 3 | meningioma | 0.0351 | 0.9547 | 0.2112 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 4 | meningioma | 0.0834 | 0.8730 | 0.4834 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 5 | notumor | 0.1693 | 0.8224 | 0.5055 |
| GLIOMA01-i_BF76 | Ax T1 +C | 1 | glioma | 0.7413 | 0.7413 | 0.7747 |
| GLIOMA01-i_BF76 | Ax T1 +C | 2 | notumor | 0.1865 | 0.7064 | 0.8693 |
| GLIOMA01-i_BF76 | Ax T1 +C | 3 | notumor | 0.1840 | 0.6069 | 1.0335 |
| GLIOMA01-i_BF76 | Ax T1 +C | 4 | glioma | 0.4357 | 0.4357 | 1.1322 |
| GLIOMA01-i_BF76 | Ax T1 +C | 5 | notumor | 0.1676 | 0.5199 | 1.1509 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 1 | notumor | 0.1436 | 0.7616 | 0.7714 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 2 | notumor | 0.0740 | 0.8235 | 0.6552 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 3 | notumor | 0.0708 | 0.8409 | 0.6086 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 4 | notumor | 0.0753 | 0.8136 | 0.6831 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 5 | notumor | 0.0171 | 0.9662 | 0.1799 |
| GLIOMA01-i_8743 | AX FSE T1 | 1 | glioma | 0.8806 | 0.8806 | 0.4778 |
| GLIOMA01-i_8743 | AX FSE T1 | 2 | glioma | 0.9358 | 0.9358 | 0.3011 |
| GLIOMA01-i_8743 | AX FSE T1 | 3 | glioma | 0.9691 | 0.9691 | 0.1542 |
| GLIOMA01-i_8743 | AX FSE T1 | 4 | glioma | 0.9827 | 0.9827 | 0.0943 |
| GLIOMA01-i_8743 | AX FSE T1 | 5 | glioma | 0.9870 | 0.9870 | 0.0748 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 1 | notumor | 0.2916 | 0.4689 | 1.0660 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 2 | glioma | 0.7346 | 0.7346 | 0.7501 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 3 | notumor | 0.3164 | 0.6672 | 0.7063 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 4 | notumor | 0.2881 | 0.6625 | 0.7857 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 5 | glioma | 0.4481 | 0.4481 | 1.0785 |

## Interpretation

This report evaluates whether the D1-trained E003 model recognises D3B glioma-domain images as glioma and how confident it is under domain shift. Because D3B labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E003 temperature scaling parameter to these D3B logits/probabilities and compare raw versus calibrated confidence under domain shift.
