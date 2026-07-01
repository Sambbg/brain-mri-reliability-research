# E001 on D3B — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E001 ResNet18 trained on D1, evaluated on D3B ICDC-Glioma central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3B predictions: `experiments/E001_D1_resnet18_baseline/d3b_predictions.csv`
- Temperature metrics: `experiments/E001_D1_resnet18_baseline/temperature_scaling_metrics.json`
- Learned temperature: `1.232835`
- Slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.2943 | 0.2943 |
| Mean glioma probability | 0.2936 | 0.2927 |
| Median glioma probability | 0.1478 | 0.1796 |
| Mean max confidence | 0.7209 | 0.6678 |
| Median max confidence | 0.7263 | 0.6548 |
| Mean entropy | 0.7157 | 0.8363 |
| Median entropy | 0.7693 | 0.9087 |
| Patient-majority glioma rate | 0.2642 | 0.2642 |
| Series-majority glioma rate | 0.2642 | 0.2642 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 78 | 0.2943 | 78 | 0.2943 |
| meningioma | 79 | 0.2981 | 79 | 0.2981 |
| notumor | 35 | 0.1321 | 35 | 0.1321 |
| pituitary | 73 | 0.2755 | 73 | 0.2755 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 14 | 14 |
| meningioma | 18 | 18 |
| notumor | 6 | 6 |
| pituitary | 15 | 15 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3B, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
