# E003 on D3C — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1, evaluated on D3C UPENN-GBM central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3C predictions: `experiments/E003_D1_vit_b16_baseline/seed45/d3c_predictions.csv`
- Temperature metrics: `experiments/E003_D1_vit_b16_baseline/seed45/temperature_scaling_metrics.json`
- Learned temperature: `1.233862`
- Slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.2502 | 0.2502 |
| Mean glioma probability | 0.2597 | 0.2643 |
| Median glioma probability | 0.0728 | 0.1098 |
| Mean max confidence | 0.8697 | 0.8395 |
| Median max confidence | 0.9473 | 0.9066 |
| Mean entropy | 0.3245 | 0.4037 |
| Median entropy | 0.2221 | 0.3437 |
| Patient-majority glioma rate | 0.2377 | 0.2377 |
| Series-majority glioma rate | 0.2377 | 0.2377 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 763 | 0.2502 | 763 | 0.2502 |
| meningioma | 126 | 0.0413 | 126 | 0.0413 |
| notumor | 2152 | 0.7056 | 2152 | 0.7056 |
| pituitary | 9 | 0.0030 | 9 | 0.0030 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 145 | 145 |
| meningioma | 18 | 18 |
| notumor | 446 | 446 |
| pituitary | 1 | 1 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3C, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
