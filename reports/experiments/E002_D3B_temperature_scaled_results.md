# E002 on D3B — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1, evaluated on D3B ICDC-Glioma central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3B predictions: `experiments/E002_D1_efficientnet_b0_baseline/d3b_predictions.csv`
- Temperature metrics: `experiments/E002_D1_efficientnet_b0_baseline/temperature_scaling_metrics.json`
- Learned temperature: `1.159631`
- Slices evaluated: 265
- Patients represented: 53
- Series represented: 53

## Critical Interpretation Rule

D3B is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.4415 | 0.4415 |
| Mean glioma probability | 0.3879 | 0.3776 |
| Median glioma probability | 0.3442 | 0.3457 |
| Mean max confidence | 0.6837 | 0.6451 |
| Median max confidence | 0.6796 | 0.6262 |
| Mean entropy | 0.7970 | 0.8838 |
| Median entropy | 0.8386 | 0.9302 |
| Patient-majority glioma rate | 0.4717 | 0.4717 |
| Series-majority glioma rate | 0.4717 | 0.4717 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 117 | 0.4415 | 117 | 0.4415 |
| meningioma | 34 | 0.1283 | 34 | 0.1283 |
| notumor | 81 | 0.3057 | 81 | 0.3057 |
| pituitary | 33 | 0.1245 | 33 | 0.1245 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 25 | 25 |
| meningioma | 5 | 5 |
| notumor | 17 | 17 |
| pituitary | 6 | 6 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3B, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
