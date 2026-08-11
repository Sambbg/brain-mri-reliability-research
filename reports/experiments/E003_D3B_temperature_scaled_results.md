# E003 on D3B — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1, evaluated on D3B ICDC-Glioma central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3B predictions: `experiments/E003_D1_vit_b16_baseline/seed45/d3b_predictions.csv`
- Temperature metrics: `experiments/E003_D1_vit_b16_baseline/seed45/temperature_scaling_metrics.json`
- Learned temperature: `1.233862`
- Slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.2830 | 0.2830 |
| Mean glioma probability | 0.3121 | 0.3166 |
| Median glioma probability | 0.1847 | 0.2282 |
| Mean max confidence | 0.8172 | 0.7758 |
| Median max confidence | 0.8643 | 0.7993 |
| Mean entropy | 0.4580 | 0.5601 |
| Median entropy | 0.4636 | 0.5909 |
| Patient-majority glioma rate | 0.2453 | 0.2453 |
| Series-majority glioma rate | 0.2453 | 0.2453 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 75 | 0.2830 | 75 | 0.2830 |
| meningioma | 45 | 0.1698 | 45 | 0.1698 |
| notumor | 145 | 0.5472 | 145 | 0.5472 |
| pituitary | 0 | 0.0000 | 0 | 0.0000 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 13 | 13 |
| meningioma | 9 | 9 |
| notumor | 31 | 31 |
| pituitary | 0 | 0 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3B, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
