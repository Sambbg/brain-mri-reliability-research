# E002 on D3B — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1, evaluated on D3B ICDC-Glioma central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3B predictions: `experiments/E002_D1_efficientnet_b0_baseline/seed45/d3b_predictions.csv`
- Temperature metrics: `experiments/E002_D1_efficientnet_b0_baseline/seed45/temperature_scaling_metrics.json`
- Learned temperature: `1.070038`
- Slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.3132 | 0.3132 |
| Mean glioma probability | 0.2772 | 0.2756 |
| Median glioma probability | 0.1445 | 0.1568 |
| Mean max confidence | 0.6914 | 0.6734 |
| Median max confidence | 0.6996 | 0.6742 |
| Mean entropy | 0.7973 | 0.8385 |
| Median entropy | 0.8574 | 0.9017 |
| Patient-majority glioma rate | 0.3019 | 0.3019 |
| Series-majority glioma rate | 0.3019 | 0.3019 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 83 | 0.3132 | 83 | 0.3132 |
| meningioma | 27 | 0.1019 | 27 | 0.1019 |
| notumor | 58 | 0.2189 | 58 | 0.2189 |
| pituitary | 97 | 0.3660 | 97 | 0.3660 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 16 | 16 |
| meningioma | 6 | 6 |
| notumor | 12 | 12 |
| pituitary | 19 | 19 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3B, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
