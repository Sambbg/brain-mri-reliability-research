# E002 on D3B — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1, evaluated on D3B ICDC-Glioma central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3B predictions: `experiments/E002_D1_efficientnet_b0_baseline/seed46/d3b_predictions.csv`
- Temperature metrics: `experiments/E002_D1_efficientnet_b0_baseline/seed46/temperature_scaling_metrics.json`
- Learned temperature: `1.303988`
- Slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.3283 | 0.3283 |
| Mean glioma probability | 0.3144 | 0.3067 |
| Median glioma probability | 0.1656 | 0.1980 |
| Mean max confidence | 0.7135 | 0.6517 |
| Median max confidence | 0.7122 | 0.6285 |
| Mean entropy | 0.7112 | 0.8519 |
| Median entropy | 0.7610 | 0.9197 |
| Patient-majority glioma rate | 0.3585 | 0.3585 |
| Series-majority glioma rate | 0.3585 | 0.3585 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 87 | 0.3283 | 87 | 0.3283 |
| meningioma | 60 | 0.2264 | 60 | 0.2264 |
| notumor | 41 | 0.1547 | 41 | 0.1547 |
| pituitary | 77 | 0.2906 | 77 | 0.2906 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 19 | 19 |
| meningioma | 10 | 10 |
| notumor | 8 | 8 |
| pituitary | 16 | 16 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3B, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
