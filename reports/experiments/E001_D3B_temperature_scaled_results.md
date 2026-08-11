# E001 on D3B — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E001 ResNet18 trained on D1, evaluated on D3B ICDC-Glioma central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3B predictions: `experiments/E001_D1_resnet18_baseline/seed44/d3b_predictions.csv`
- Temperature metrics: `experiments/E001_D1_resnet18_baseline/seed44/temperature_scaling_metrics.json`
- Learned temperature: `1.172485`
- Slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.3245 | 0.3245 |
| Mean glioma probability | 0.3320 | 0.3281 |
| Median glioma probability | 0.1474 | 0.1636 |
| Mean max confidence | 0.7273 | 0.6901 |
| Median max confidence | 0.7428 | 0.6949 |
| Mean entropy | 0.6810 | 0.7684 |
| Median entropy | 0.7006 | 0.7722 |
| Patient-majority glioma rate | 0.3208 | 0.3208 |
| Series-majority glioma rate | 0.3208 | 0.3208 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 86 | 0.3245 | 86 | 0.3245 |
| meningioma | 52 | 0.1962 | 52 | 0.1962 |
| notumor | 30 | 0.1132 | 30 | 0.1132 |
| pituitary | 97 | 0.3660 | 97 | 0.3660 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 17 | 17 |
| meningioma | 10 | 10 |
| notumor | 6 | 6 |
| pituitary | 20 | 20 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3B, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
