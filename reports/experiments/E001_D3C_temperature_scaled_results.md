# E001 on D3C — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E001 ResNet18 trained on D1, evaluated on D3C UPENN-GBM central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3C predictions: `experiments/E001_D1_resnet18_baseline/seed42/d3c_predictions.csv`
- Temperature metrics: `experiments/E001_D1_resnet18_baseline/seed42/temperature_scaling_metrics.json`
- Learned temperature: `1.269943`
- Slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.8013 | 0.8013 |
| Mean glioma probability | 0.7410 | 0.7105 |
| Median glioma probability | 0.8883 | 0.8237 |
| Mean max confidence | 0.8564 | 0.8129 |
| Median max confidence | 0.9176 | 0.8574 |
| Mean entropy | 0.3721 | 0.4922 |
| Median entropy | 0.3158 | 0.4843 |
| Patient-majority glioma rate | 0.8213 | 0.8213 |
| Series-majority glioma rate | 0.8213 | 0.8213 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 2444 | 0.8013 | 2444 | 0.8013 |
| meningioma | 6 | 0.0020 | 6 | 0.0020 |
| notumor | 565 | 0.1852 | 565 | 0.1852 |
| pituitary | 35 | 0.0115 | 35 | 0.0115 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 501 | 501 |
| meningioma | 0 | 0 |
| notumor | 104 | 104 |
| pituitary | 5 | 5 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3C, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
