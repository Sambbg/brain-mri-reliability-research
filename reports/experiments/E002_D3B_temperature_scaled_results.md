# E002 on D3B — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1, evaluated on D3B ICDC-Glioma central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3B predictions: `experiments/E002_D1_efficientnet_b0_baseline/seed42/d3b_predictions.csv`
- Temperature metrics: `experiments/E002_D1_efficientnet_b0_baseline/seed42/temperature_scaling_metrics.json`
- Learned temperature: `1.274009`
- Slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.5962 | 0.5962 |
| Mean glioma probability | 0.5314 | 0.5061 |
| Median glioma probability | 0.5725 | 0.5276 |
| Mean max confidence | 0.7553 | 0.6988 |
| Median max confidence | 0.7978 | 0.7174 |
| Mean entropy | 0.6298 | 0.7644 |
| Median entropy | 0.6247 | 0.8011 |
| Patient-majority glioma rate | 0.6604 | 0.6604 |
| Series-majority glioma rate | 0.6604 | 0.6604 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 158 | 0.5962 | 158 | 0.5962 |
| meningioma | 29 | 0.1094 | 29 | 0.1094 |
| notumor | 65 | 0.2453 | 65 | 0.2453 |
| pituitary | 13 | 0.0491 | 13 | 0.0491 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 35 | 35 |
| meningioma | 4 | 4 |
| notumor | 12 | 12 |
| pituitary | 2 | 2 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3B, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
