# E003 on D3B Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1 leakage-aware split, evaluated on D3B ICDC-Glioma central slices.

## Inputs

- Checkpoint: `experiments/E003_D1_vit_b16_baseline/best_model.pt`
- D3B manifest: `data/processed/D3B_selected_slices_manifest_phash.csv`
- D3B slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 107 | 0.4038 |
| meningioma | 21 | 0.0792 |
| notumor | 131 | 0.4943 |
| pituitary | 6 | 0.0226 |

## Core D3B Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.4038 |
| Mean glioma probability | 0.3553 |
| Median glioma probability | 0.3185 |
| Mean maximum softmax confidence | 0.7203 |
| Median maximum softmax confidence | 0.7289 |
| Mean entropy | 0.6748 |
| Median entropy | 0.7326 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 20 |
| meningioma | 4 |
| notumor | 28 |
| pituitary | 1 |

Patient-level majority glioma rate: `0.3774`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 20 |
| meningioma | 4 |
| notumor | 28 |
| pituitary | 1 |

Series-level majority glioma rate: `0.3774`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| GLIOMA01-i_6561 | FSPGR 3D | 1 | glioma | 0.4855 | 0.4855 | 0.8379 |
| GLIOMA01-i_6561 | FSPGR 3D | 2 | glioma | 0.6050 | 0.6050 | 0.7975 |
| GLIOMA01-i_6561 | FSPGR 3D | 3 | glioma | 0.5277 | 0.5277 | 0.8421 |
| GLIOMA01-i_6561 | FSPGR 3D | 4 | glioma | 0.5266 | 0.5266 | 0.9394 |
| GLIOMA01-i_6561 | FSPGR 3D | 5 | glioma | 0.6154 | 0.6154 | 0.9035 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 1 | notumor | 0.1524 | 0.8457 | 0.4418 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 2 | notumor | 0.2160 | 0.7794 | 0.5533 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 3 | glioma | 0.6345 | 0.6345 | 0.8047 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 4 | glioma | 0.4869 | 0.4869 | 0.8198 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 5 | notumor | 0.2872 | 0.6915 | 0.7075 |
| GLIOMA01-i_BF76 | Ax T1 +C | 1 | glioma | 0.8613 | 0.8613 | 0.5196 |
| GLIOMA01-i_BF76 | Ax T1 +C | 2 | glioma | 0.6716 | 0.6716 | 0.8896 |
| GLIOMA01-i_BF76 | Ax T1 +C | 3 | glioma | 0.5046 | 0.5046 | 1.0047 |
| GLIOMA01-i_BF76 | Ax T1 +C | 4 | glioma | 0.6421 | 0.6421 | 0.8532 |
| GLIOMA01-i_BF76 | Ax T1 +C | 5 | glioma | 0.6481 | 0.6481 | 0.8129 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 1 | notumor | 0.0990 | 0.8878 | 0.4004 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 2 | notumor | 0.0945 | 0.8876 | 0.4125 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 3 | notumor | 0.2101 | 0.7715 | 0.6141 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 4 | notumor | 0.1685 | 0.8211 | 0.5167 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 5 | notumor | 0.0875 | 0.9079 | 0.3285 |
| GLIOMA01-i_8743 | AX FSE T1 | 1 | glioma | 0.6083 | 0.6083 | 0.8093 |
| GLIOMA01-i_8743 | AX FSE T1 | 2 | glioma | 0.6168 | 0.6168 | 0.8518 |
| GLIOMA01-i_8743 | AX FSE T1 | 3 | notumor | 0.3185 | 0.6539 | 0.7535 |
| GLIOMA01-i_8743 | AX FSE T1 | 4 | notumor | 0.4267 | 0.5701 | 0.7036 |
| GLIOMA01-i_8743 | AX FSE T1 | 5 | notumor | 0.4567 | 0.5387 | 0.7195 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 1 | glioma | 0.4874 | 0.4874 | 0.9224 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 2 | glioma | 0.7400 | 0.7400 | 0.7326 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 3 | notumor | 0.2168 | 0.7201 | 0.7471 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 4 | glioma | 0.4670 | 0.4670 | 1.0500 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 5 | meningioma | 0.2252 | 0.5720 | 0.9874 |

## Interpretation

This report evaluates whether the D1-trained E003 model recognises D3B glioma-domain images as glioma and how confident it is under domain shift. Because D3B labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E003 temperature scaling parameter to these D3B logits/probabilities and compare raw versus calibrated confidence under domain shift.
