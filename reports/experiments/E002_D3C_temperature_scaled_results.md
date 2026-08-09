# E002 on D3C — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1, evaluated on D3C UPENN-GBM central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3C predictions: `experiments\E002_D1_efficientnet_b0_baseline\d3c_predictions.csv`
- Temperature metrics: `experiments\E002_D1_efficientnet_b0_baseline\temperature_scaling_metrics.json`
- Learned temperature: `1.159784`
- Slices evaluated: 2845
- Patients represented: 569
- Series represented: 569

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.4626 | 0.4626 |
| Mean glioma probability | 0.4512 | 0.4455 |
| Median glioma probability | 0.3755 | 0.3752 |
| Mean max confidence | 0.8033 | 0.7717 |
| Median max confidence | 0.8546 | 0.8070 |
| Mean entropy | 0.5195 | 0.6034 |
| Median entropy | 0.5210 | 0.6425 |
| Patient-majority glioma rate | 0.4569 | 0.4569 |
| Series-majority glioma rate | 0.4569 | 0.4569 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 1316 | 0.4626 | 1316 | 0.4626 |
| meningioma | 54 | 0.0190 | 54 | 0.0190 |
| notumor | 1455 | 0.5114 | 1455 | 0.5114 |
| pituitary | 20 | 0.0070 | 20 | 0.0070 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 260 | 260 |
| meningioma | 8 | 8 |
| notumor | 299 | 299 |
| pituitary | 2 | 2 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3C, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
