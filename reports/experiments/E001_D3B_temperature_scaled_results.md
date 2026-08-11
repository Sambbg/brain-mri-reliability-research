# E001 on D3B — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E001 ResNet18 trained on D1, evaluated on D3B ICDC-Glioma central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3B predictions: `experiments/E001_D1_resnet18_baseline/seed42/d3b_predictions.csv`
- Temperature metrics: `experiments/E001_D1_resnet18_baseline/seed42/temperature_scaling_metrics.json`
- Learned temperature: `1.269943`
- Slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.3094 | 0.3094 |
| Mean glioma probability | 0.2970 | 0.2936 |
| Median glioma probability | 0.1469 | 0.1791 |
| Mean max confidence | 0.7020 | 0.6448 |
| Median max confidence | 0.6944 | 0.6155 |
| Mean entropy | 0.7302 | 0.8566 |
| Median entropy | 0.7777 | 0.9051 |
| Patient-majority glioma rate | 0.2830 | 0.2830 |
| Series-majority glioma rate | 0.2830 | 0.2830 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 82 | 0.3094 | 82 | 0.3094 |
| meningioma | 48 | 0.1811 | 48 | 0.1811 |
| notumor | 115 | 0.4340 | 115 | 0.4340 |
| pituitary | 20 | 0.0755 | 20 | 0.0755 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 15 | 15 |
| meningioma | 9 | 9 |
| notumor | 27 | 27 |
| pituitary | 2 | 2 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3B, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
