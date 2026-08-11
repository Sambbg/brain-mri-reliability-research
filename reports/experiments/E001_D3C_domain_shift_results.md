# E001 on D3C Domain-Shift Evaluation

## Experiment

E001 ResNet18 trained on D1 leakage-aware split, evaluated on D3C UPENN-GBM central slices.

## Inputs

- Checkpoint: `experiments/E001_D1_resnet18_baseline/seed42/best_model.pt`
- D3C manifest: `data/processed/D3C_analysis_manifest.csv`
- D3C slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 2444 | 0.8013 |
| meningioma | 6 | 0.0020 |
| notumor | 565 | 0.1852 |
| pituitary | 35 | 0.0115 |

## Core D3C Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.8013 |
| Mean glioma probability | 0.7410 |
| Median glioma probability | 0.8883 |
| Mean maximum softmax confidence | 0.8564 |
| Median maximum softmax confidence | 0.9176 |
| Mean entropy | 0.3721 |
| Median entropy | 0.3158 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 501 |
| meningioma | 0 |
| notumor | 104 |
| pituitary | 5 |

Patient-level majority glioma rate: `0.8213`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 501 |
| meningioma | 0 |
| notumor | 104 |
| pituitary | 5 |

Series-level majority glioma rate: `0.8213`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9727 | 0.9727 | 0.1500 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9879 | 0.9879 | 0.0743 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.8846 | 0.8846 | 0.4062 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.7490 | 0.7490 | 0.6670 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.8643 | 0.8643 | 0.5184 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.2933 | 0.6948 | 0.6699 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.3309 | 0.6559 | 0.7036 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.3060 | 0.6872 | 0.6576 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9486 | 0.9486 | 0.2404 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.4803 | 0.5047 | 0.7706 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0922 | 0.9020 | 0.3446 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0393 | 0.9571 | 0.1909 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0710 | 0.9249 | 0.2841 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.0943 | 0.9017 | 0.3394 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.4585 | 0.5319 | 0.7406 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9982 | 0.9982 | 0.0138 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9991 | 0.9991 | 0.0078 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.9992 | 0.9992 | 0.0069 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9993 | 0.9993 | 0.0061 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.9943 | 0.9943 | 0.0367 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.7915 | 0.7915 | 0.5535 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9781 | 0.9781 | 0.1128 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.8592 | 0.8592 | 0.4304 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.7612 | 0.7612 | 0.5814 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.9243 | 0.9243 | 0.2872 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9671 | 0.9671 | 0.1571 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9044 | 0.9044 | 0.3744 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.7830 | 0.7830 | 0.5613 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9469 | 0.9469 | 0.2291 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.7607 | 0.7607 | 0.6299 |

## Interpretation

This report evaluates whether the D1-trained E001 model recognises D3C glioma-domain images as glioma and how confident it is under domain shift. Because D3C labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E001 temperature scaling parameter to these D3C logits/probabilities and compare raw versus calibrated confidence under domain shift.
