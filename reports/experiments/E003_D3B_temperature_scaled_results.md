# E003 on D3B — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1, evaluated on D3B ICDC-Glioma central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3B predictions: `experiments/E003_D1_vit_b16_baseline/d3b_predictions.csv`
- Temperature metrics: `experiments/E003_D1_vit_b16_baseline/temperature_scaling_metrics.json`
- Learned temperature: `1.236274`
- Slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.4038 | 0.4038 |
| Mean glioma probability | 0.3553 | 0.3488 |
| Median glioma probability | 0.3185 | 0.3349 |
| Mean max confidence | 0.7203 | 0.6710 |
| Median max confidence | 0.7289 | 0.6610 |
| Mean entropy | 0.6748 | 0.7913 |
| Median entropy | 0.7326 | 0.8572 |
| Patient-majority glioma rate | 0.3774 | 0.3774 |
| Series-majority glioma rate | 0.3774 | 0.3774 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 107 | 0.4038 | 107 | 0.4038 |
| meningioma | 21 | 0.0792 | 21 | 0.0792 |
| notumor | 131 | 0.4943 | 131 | 0.4943 |
| pituitary | 6 | 0.0226 | 6 | 0.0226 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 20 | 20 |
| meningioma | 4 | 4 |
| notumor | 28 | 28 |
| pituitary | 1 | 1 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3B, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
