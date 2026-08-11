# E002 on D3B — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1, evaluated on D3B ICDC-Glioma central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3B predictions: `experiments/E002_D1_efficientnet_b0_baseline/seed43/d3b_predictions.csv`
- Temperature metrics: `experiments/E002_D1_efficientnet_b0_baseline/seed43/temperature_scaling_metrics.json`
- Learned temperature: `1.307584`
- Slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.2226 | 0.2226 |
| Mean glioma probability | 0.2268 | 0.2301 |
| Median glioma probability | 0.0706 | 0.1113 |
| Mean max confidence | 0.7670 | 0.7052 |
| Median max confidence | 0.8006 | 0.7113 |
| Mean entropy | 0.5998 | 0.7512 |
| Median entropy | 0.6187 | 0.7863 |
| Patient-majority glioma rate | 0.2264 | 0.2264 |
| Series-majority glioma rate | 0.2264 | 0.2264 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 59 | 0.2226 | 59 | 0.2226 |
| meningioma | 33 | 0.1245 | 33 | 0.1245 |
| notumor | 58 | 0.2189 | 58 | 0.2189 |
| pituitary | 115 | 0.4340 | 115 | 0.4340 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 12 | 12 |
| meningioma | 5 | 5 |
| notumor | 13 | 13 |
| pituitary | 23 | 23 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3B, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
