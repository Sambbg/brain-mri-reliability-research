# E003 on D3B — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1, evaluated on D3B ICDC-Glioma central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3B predictions: `experiments/E003_D1_vit_b16_baseline/seed42/d3b_predictions.csv`
- Temperature metrics: `experiments/E003_D1_vit_b16_baseline/seed42/temperature_scaling_metrics.json`
- Learned temperature: `1.257989`
- Slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.2377 | 0.2377 |
| Mean glioma probability | 0.2623 | 0.2665 |
| Median glioma probability | 0.1052 | 0.1393 |
| Mean max confidence | 0.7460 | 0.6931 |
| Median max confidence | 0.7631 | 0.6880 |
| Mean entropy | 0.6224 | 0.7497 |
| Median entropy | 0.6770 | 0.8072 |
| Patient-majority glioma rate | 0.2075 | 0.2075 |
| Series-majority glioma rate | 0.2075 | 0.2075 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 63 | 0.2377 | 63 | 0.2377 |
| meningioma | 116 | 0.4377 | 116 | 0.4377 |
| notumor | 72 | 0.2717 | 72 | 0.2717 |
| pituitary | 14 | 0.0528 | 14 | 0.0528 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 11 | 11 |
| meningioma | 24 | 24 |
| notumor | 15 | 15 |
| pituitary | 3 | 3 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3B, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
