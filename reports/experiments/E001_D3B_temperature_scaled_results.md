# E001 on D3B — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E001 ResNet18 trained on D1, evaluated on D3B ICDC-Glioma central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3B predictions: `experiments/E001_D1_resnet18_baseline/seed43/d3b_predictions.csv`
- Temperature metrics: `experiments/E001_D1_resnet18_baseline/seed43/temperature_scaling_metrics.json`
- Learned temperature: `1.222596`
- Slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.4604 | 0.4604 |
| Mean glioma probability | 0.3977 | 0.3806 |
| Median glioma probability | 0.3495 | 0.3398 |
| Mean max confidence | 0.6769 | 0.6287 |
| Median max confidence | 0.6682 | 0.6054 |
| Mean entropy | 0.7902 | 0.8928 |
| Median entropy | 0.8507 | 0.9621 |
| Patient-majority glioma rate | 0.5094 | 0.5094 |
| Series-majority glioma rate | 0.5094 | 0.5094 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 122 | 0.4604 | 122 | 0.4604 |
| meningioma | 51 | 0.1925 | 51 | 0.1925 |
| notumor | 55 | 0.2075 | 55 | 0.2075 |
| pituitary | 37 | 0.1396 | 37 | 0.1396 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 27 | 27 |
| meningioma | 10 | 10 |
| notumor | 10 | 10 |
| pituitary | 6 | 6 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3B, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
