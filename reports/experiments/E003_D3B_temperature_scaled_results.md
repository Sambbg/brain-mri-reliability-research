# E003 on D3B — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1, evaluated on D3B ICDC-Glioma central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3B predictions: `experiments/E003_D1_vit_b16_baseline/seed43/d3b_predictions.csv`
- Temperature metrics: `experiments/E003_D1_vit_b16_baseline/seed43/temperature_scaling_metrics.json`
- Learned temperature: `1.218531`
- Slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.2453 | 0.2453 |
| Mean glioma probability | 0.2557 | 0.2609 |
| Median glioma probability | 0.1100 | 0.1439 |
| Mean max confidence | 0.7965 | 0.7532 |
| Median max confidence | 0.8565 | 0.7914 |
| Mean entropy | 0.5312 | 0.6416 |
| Median entropy | 0.5022 | 0.6725 |
| Patient-majority glioma rate | 0.2642 | 0.2642 |
| Series-majority glioma rate | 0.2642 | 0.2642 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 65 | 0.2453 | 65 | 0.2453 |
| meningioma | 65 | 0.2453 | 65 | 0.2453 |
| notumor | 131 | 0.4943 | 131 | 0.4943 |
| pituitary | 4 | 0.0151 | 4 | 0.0151 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 14 | 14 |
| meningioma | 14 | 14 |
| notumor | 25 | 25 |
| pituitary | 0 | 0 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3B, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
