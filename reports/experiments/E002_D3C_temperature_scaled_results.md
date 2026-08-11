# E002 on D3C — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1, evaluated on D3C UPENN-GBM central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3C predictions: `experiments/E002_D1_efficientnet_b0_baseline/seed46/d3c_predictions.csv`
- Temperature metrics: `experiments/E002_D1_efficientnet_b0_baseline/seed46/temperature_scaling_metrics.json`
- Learned temperature: `1.303988`
- Slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.5213 | 0.5213 |
| Mean glioma probability | 0.5060 | 0.4945 |
| Median glioma probability | 0.4991 | 0.4577 |
| Mean max confidence | 0.8264 | 0.7750 |
| Median max confidence | 0.8999 | 0.8195 |
| Mean entropy | 0.4545 | 0.5910 |
| Median entropy | 0.3948 | 0.6110 |
| Patient-majority glioma rate | 0.5328 | 0.5328 |
| Series-majority glioma rate | 0.5328 | 0.5328 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 1590 | 0.5213 | 1590 | 0.5213 |
| meningioma | 49 | 0.0161 | 49 | 0.0161 |
| notumor | 1214 | 0.3980 | 1214 | 0.3980 |
| pituitary | 197 | 0.0646 | 197 | 0.0646 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 325 | 325 |
| meningioma | 6 | 6 |
| notumor | 249 | 249 |
| pituitary | 30 | 30 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3C, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
