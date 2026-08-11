# E003 on D3B — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1, evaluated on D3B ICDC-Glioma central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3B predictions: `experiments/E003_D1_vit_b16_baseline/seed44/d3b_predictions.csv`
- Temperature metrics: `experiments/E003_D1_vit_b16_baseline/seed44/temperature_scaling_metrics.json`
- Learned temperature: `1.229500`
- Slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.3283 | 0.3283 |
| Mean glioma probability | 0.3215 | 0.3195 |
| Median glioma probability | 0.1840 | 0.2216 |
| Mean max confidence | 0.7519 | 0.7033 |
| Median max confidence | 0.7652 | 0.6918 |
| Mean entropy | 0.6297 | 0.7476 |
| Median entropy | 0.6919 | 0.8274 |
| Patient-majority glioma rate | 0.3396 | 0.3396 |
| Series-majority glioma rate | 0.3396 | 0.3396 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 87 | 0.3283 | 87 | 0.3283 |
| meningioma | 37 | 0.1396 | 37 | 0.1396 |
| notumor | 121 | 0.4566 | 121 | 0.4566 |
| pituitary | 20 | 0.0755 | 20 | 0.0755 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 18 | 18 |
| meningioma | 8 | 8 |
| notumor | 24 | 24 |
| pituitary | 3 | 3 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3B, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
