# E001 on D3C — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E001 ResNet18 trained on D1, evaluated on D3C UPENN-GBM central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3C predictions: `experiments/E001_D1_resnet18_baseline/seed46/d3c_predictions.csv`
- Temperature metrics: `experiments/E001_D1_resnet18_baseline/seed46/temperature_scaling_metrics.json`
- Learned temperature: `1.151924`
- Slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.6220 | 0.6220 |
| Mean glioma probability | 0.5627 | 0.5474 |
| Median glioma probability | 0.6063 | 0.5712 |
| Mean max confidence | 0.7494 | 0.7176 |
| Median max confidence | 0.7644 | 0.7193 |
| Mean entropy | 0.6255 | 0.7032 |
| Median entropy | 0.6640 | 0.7510 |
| Patient-majority glioma rate | 0.6361 | 0.6361 |
| Series-majority glioma rate | 0.6361 | 0.6361 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 1897 | 0.6220 | 1897 | 0.6220 |
| meningioma | 21 | 0.0069 | 21 | 0.0069 |
| notumor | 1093 | 0.3584 | 1093 | 0.3584 |
| pituitary | 39 | 0.0128 | 39 | 0.0128 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 388 | 388 |
| meningioma | 2 | 2 |
| notumor | 213 | 213 |
| pituitary | 7 | 7 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3C, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
