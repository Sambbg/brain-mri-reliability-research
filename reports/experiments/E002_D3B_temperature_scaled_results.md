# E002 on D3B — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1, evaluated on D3B ICDC-Glioma central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3B predictions: `experiments/E002_D1_efficientnet_b0_baseline/seed44/d3b_predictions.csv`
- Temperature metrics: `experiments/E002_D1_efficientnet_b0_baseline/seed44/temperature_scaling_metrics.json`
- Learned temperature: `1.176001`
- Slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.3811 | 0.3811 |
| Mean glioma probability | 0.3522 | 0.3464 |
| Median glioma probability | 0.2269 | 0.2380 |
| Mean max confidence | 0.7259 | 0.6881 |
| Median max confidence | 0.7509 | 0.6940 |
| Mean entropy | 0.6866 | 0.7775 |
| Median entropy | 0.7194 | 0.8253 |
| Patient-majority glioma rate | 0.3962 | 0.3962 |
| Series-majority glioma rate | 0.3962 | 0.3962 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 101 | 0.3811 | 101 | 0.3811 |
| meningioma | 56 | 0.2113 | 56 | 0.2113 |
| notumor | 50 | 0.1887 | 50 | 0.1887 |
| pituitary | 58 | 0.2189 | 58 | 0.2189 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 21 | 21 |
| meningioma | 11 | 11 |
| notumor | 10 | 10 |
| pituitary | 11 | 11 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3B, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
