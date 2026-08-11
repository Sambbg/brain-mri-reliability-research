# E002 on D3C — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1, evaluated on D3C UPENN-GBM central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3C predictions: `experiments/E002_D1_efficientnet_b0_baseline/seed43/d3c_predictions.csv`
- Temperature metrics: `experiments/E002_D1_efficientnet_b0_baseline/seed43/temperature_scaling_metrics.json`
- Learned temperature: `1.307584`
- Slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.6118 | 0.6118 |
| Mean glioma probability | 0.5834 | 0.5663 |
| Median glioma probability | 0.7163 | 0.6402 |
| Mean max confidence | 0.8360 | 0.7864 |
| Median max confidence | 0.9131 | 0.8356 |
| Mean entropy | 0.4308 | 0.5633 |
| Median entropy | 0.3535 | 0.5702 |
| Patient-majority glioma rate | 0.6344 | 0.6344 |
| Series-majority glioma rate | 0.6344 | 0.6344 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 1866 | 0.6118 | 1866 | 0.6118 |
| meningioma | 46 | 0.0151 | 46 | 0.0151 |
| notumor | 816 | 0.2675 | 816 | 0.2675 |
| pituitary | 322 | 0.1056 | 322 | 0.1056 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 387 | 387 |
| meningioma | 7 | 7 |
| notumor | 156 | 156 |
| pituitary | 60 | 60 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3C, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
