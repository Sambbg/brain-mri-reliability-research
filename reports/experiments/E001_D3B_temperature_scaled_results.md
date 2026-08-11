# E001 on D3B — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E001 ResNet18 trained on D1, evaluated on D3B ICDC-Glioma central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3B predictions: `experiments/E001_D1_resnet18_baseline/seed46/d3b_predictions.csv`
- Temperature metrics: `experiments/E001_D1_resnet18_baseline/seed46/temperature_scaling_metrics.json`
- Learned temperature: `1.151924`
- Slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.3245 | 0.3245 |
| Mean glioma probability | 0.3224 | 0.3196 |
| Median glioma probability | 0.2060 | 0.2211 |
| Mean max confidence | 0.6958 | 0.6616 |
| Median max confidence | 0.6926 | 0.6430 |
| Mean entropy | 0.7487 | 0.8257 |
| Median entropy | 0.7971 | 0.8811 |
| Patient-majority glioma rate | 0.3019 | 0.3019 |
| Series-majority glioma rate | 0.3019 | 0.3019 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 86 | 0.3245 | 86 | 0.3245 |
| meningioma | 45 | 0.1698 | 45 | 0.1698 |
| notumor | 100 | 0.3774 | 100 | 0.3774 |
| pituitary | 34 | 0.1283 | 34 | 0.1283 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 16 | 16 |
| meningioma | 8 | 8 |
| notumor | 23 | 23 |
| pituitary | 6 | 6 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3B, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
