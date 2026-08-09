# E001 on D3C — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E001 ResNet18 trained on D1, evaluated on D3C UPENN-GBM central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3C predictions: `experiments\E001_D1_resnet18_baseline\d3c_predictions.csv`
- Temperature metrics: `experiments\E001_D1_resnet18_baseline\temperature_scaling_metrics.json`
- Learned temperature: `1.272483`
- Slices evaluated: 2845
- Patients represented: 569
- Series represented: 569

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.6938 | 0.6938 |
| Mean glioma probability | 0.6438 | 0.6189 |
| Median glioma probability | 0.7937 | 0.7211 |
| Mean max confidence | 0.8315 | 0.7877 |
| Median max confidence | 0.8922 | 0.8243 |
| Mean entropy | 0.4279 | 0.5401 |
| Median entropy | 0.3925 | 0.5600 |
| Patient-majority glioma rate | 0.7012 | 0.7012 |
| Series-majority glioma rate | 0.7012 | 0.7012 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 1974 | 0.6938 | 1974 | 0.6938 |
| meningioma | 9 | 0.0032 | 9 | 0.0032 |
| notumor | 687 | 0.2415 | 687 | 0.2415 |
| pituitary | 175 | 0.0615 | 175 | 0.0615 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 399 | 399 |
| meningioma | 1 | 1 |
| notumor | 132 | 132 |
| pituitary | 37 | 37 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3C, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
