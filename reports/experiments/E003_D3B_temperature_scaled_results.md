# E003 on D3B — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1, evaluated on D3B ICDC-Glioma central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3B predictions: `experiments/E003_D1_vit_b16_baseline/seed46/d3b_predictions.csv`
- Temperature metrics: `experiments/E003_D1_vit_b16_baseline/seed46/temperature_scaling_metrics.json`
- Learned temperature: `1.230566`
- Slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.1509 | 0.1509 |
| Mean glioma probability | 0.1810 | 0.1924 |
| Median glioma probability | 0.0718 | 0.1026 |
| Mean max confidence | 0.7989 | 0.7585 |
| Median max confidence | 0.8506 | 0.7906 |
| Mean entropy | 0.5000 | 0.6010 |
| Median entropy | 0.5016 | 0.6603 |
| Patient-majority glioma rate | 0.1321 | 0.1321 |
| Series-majority glioma rate | 0.1321 | 0.1321 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 40 | 0.1509 | 40 | 0.1509 |
| meningioma | 123 | 0.4642 | 123 | 0.4642 |
| notumor | 101 | 0.3811 | 101 | 0.3811 |
| pituitary | 1 | 0.0038 | 1 | 0.0038 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 7 | 7 |
| meningioma | 26 | 26 |
| notumor | 20 | 20 |
| pituitary | 0 | 0 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3B, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
