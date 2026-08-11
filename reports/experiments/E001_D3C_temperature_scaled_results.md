# E001 on D3C — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E001 ResNet18 trained on D1, evaluated on D3C UPENN-GBM central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3C predictions: `experiments/E001_D1_resnet18_baseline/seed43/d3c_predictions.csv`
- Temperature metrics: `experiments/E001_D1_resnet18_baseline/seed43/temperature_scaling_metrics.json`
- Learned temperature: `1.222596`
- Slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.6331 | 0.6331 |
| Mean glioma probability | 0.5504 | 0.5248 |
| Median glioma probability | 0.6045 | 0.5540 |
| Mean max confidence | 0.7395 | 0.6920 |
| Median max confidence | 0.7565 | 0.6868 |
| Mean entropy | 0.6613 | 0.7740 |
| Median entropy | 0.7078 | 0.8391 |
| Patient-majority glioma rate | 0.6508 | 0.6508 |
| Series-majority glioma rate | 0.6508 | 0.6508 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 1931 | 0.6331 | 1931 | 0.6331 |
| meningioma | 39 | 0.0128 | 39 | 0.0128 |
| notumor | 705 | 0.2311 | 705 | 0.2311 |
| pituitary | 375 | 0.1230 | 375 | 0.1230 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 397 | 397 |
| meningioma | 7 | 7 |
| notumor | 132 | 132 |
| pituitary | 74 | 74 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3C, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
