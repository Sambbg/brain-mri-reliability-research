# E001 on D3C Domain-Shift Evaluation

## Experiment

E001 ResNet18 trained on D1 leakage-aware split, evaluated on D3C UPENN-GBM central slices.

## Inputs

- Checkpoint: `experiments/E001_D1_resnet18_baseline/seed46/best_model.pt`
- D3C manifest: `data/processed/D3C_analysis_manifest.csv`
- D3C slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full D1 four-class label set. Therefore, this evaluation must not be interpreted as four-class external accuracy. It is a glioma-focused domain-shift confidence and prediction-distribution analysis.

## Slice-Level Prediction Distribution

| Predicted class | Count | Proportion |
|---|---:|---:|
| glioma | 1897 | 0.6220 |
| meningioma | 21 | 0.0069 |
| notumor | 1093 | 0.3584 |
| pituitary | 39 | 0.0128 |

## Core D3C Metrics

| Metric | Value |
|---|---:|
| Glioma prediction rate, slice-level | 0.6220 |
| Mean glioma probability | 0.5627 |
| Median glioma probability | 0.6063 |
| Mean maximum softmax confidence | 0.7494 |
| Median maximum softmax confidence | 0.7644 |
| Mean entropy | 0.6255 |
| Median entropy | 0.6640 |

## Patient-Level Majority Prediction

| Majority predicted class | Patient count |
|---|---:|
| glioma | 388 |
| meningioma | 2 |
| notumor | 213 |
| pituitary | 7 |

Patient-level majority glioma rate: `0.6361`

## Series-Level Majority Prediction

| Majority predicted class | Series count |
|---|---:|
| glioma | 388 |
| meningioma | 2 |
| notumor | 213 |
| pituitary | 7 |

Series-level majority glioma rate: `0.6361`

## Example Predictions

| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |
|---|---|---:|---|---:|---:|---:|
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.8839 | 0.8839 | 0.4195 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9539 | 0.9539 | 0.2302 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.5495 | 0.5495 | 0.8176 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.2837 | 0.6444 | 0.8421 |
| UPENN-GBM-00001 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.4842 | 0.4842 | 1.0572 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.4789 | 0.4789 | 1.0792 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.3682 | 0.3682 | 1.1150 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.4462 | 0.4462 | 1.0932 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.7468 | 0.7468 | 0.7562 |
| UPENN-GBM-00002 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.7239 | 0.7239 | 0.8112 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.0679 | 0.9094 | 0.3635 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 2 | notumor | 0.0131 | 0.9843 | 0.0892 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.0437 | 0.9519 | 0.2102 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.1221 | 0.8688 | 0.4252 |
| UPENN-GBM-00003 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.0497 | 0.9457 | 0.2280 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9952 | 0.9952 | 0.0345 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9951 | 0.9951 | 0.0350 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.9872 | 0.9872 | 0.0782 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.9898 | 0.9898 | 0.0640 |
| UPENN-GBM-00004 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.9587 | 0.9587 | 0.1963 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 1 | notumor | 0.3086 | 0.6423 | 0.8220 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.9650 | 0.9650 | 0.1711 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 3 | notumor | 0.2701 | 0.7056 | 0.7045 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 4 | notumor | 0.2546 | 0.7251 | 0.6739 |
| UPENN-GBM-00005 | t1 axial stealth-post : Processed_CaPTk | 5 | glioma | 0.8712 | 0.8712 | 0.4581 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 1 | glioma | 0.9556 | 0.9556 | 0.2089 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 2 | glioma | 0.7709 | 0.7709 | 0.6368 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 3 | glioma | 0.6093 | 0.6093 | 0.7312 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 4 | glioma | 0.4991 | 0.4991 | 0.7573 |
| UPENN-GBM-00006 | t1 axial stealth-post : Processed_CaPTk | 5 | notumor | 0.4096 | 0.5518 | 0.8434 |

## Interpretation

This report evaluates whether the D1-trained E001 model recognises D3C glioma-domain images as glioma and how confident it is under domain shift. Because D3C labels are collection-level glioma labels rather than slice-level tumour annotations, the results should be interpreted as domain-shift behaviour, not clinical diagnostic accuracy.

The next step is to apply the E001 temperature scaling parameter to these D3C logits/probabilities and compare raw versus calibrated confidence under domain shift.
