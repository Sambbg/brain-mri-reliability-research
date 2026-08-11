# E002 on D3C — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1, evaluated on D3C UPENN-GBM central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3C predictions: `experiments/E002_D1_efficientnet_b0_baseline/seed45/d3c_predictions.csv`
- Temperature metrics: `experiments/E002_D1_efficientnet_b0_baseline/seed45/temperature_scaling_metrics.json`
- Learned temperature: `1.070038`
- Slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.4525 | 0.4525 |
| Mean glioma probability | 0.4378 | 0.4345 |
| Median glioma probability | 0.3539 | 0.3529 |
| Mean max confidence | 0.7368 | 0.7210 |
| Median max confidence | 0.7556 | 0.7329 |
| Mean entropy | 0.6764 | 0.7153 |
| Median entropy | 0.7288 | 0.7727 |
| Patient-majority glioma rate | 0.4426 | 0.4426 |
| Series-majority glioma rate | 0.4426 | 0.4426 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 1380 | 0.4525 | 1380 | 0.4525 |
| meningioma | 24 | 0.0079 | 24 | 0.0079 |
| notumor | 1483 | 0.4862 | 1483 | 0.4862 |
| pituitary | 163 | 0.0534 | 163 | 0.0534 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 270 | 270 |
| meningioma | 3 | 3 |
| notumor | 308 | 308 |
| pituitary | 29 | 29 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3C, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
