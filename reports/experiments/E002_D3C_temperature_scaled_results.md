# E002 on D3C — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1, evaluated on D3C UPENN-GBM central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3C predictions: `experiments/E002_D1_efficientnet_b0_baseline/seed42/d3c_predictions.csv`
- Temperature metrics: `experiments/E002_D1_efficientnet_b0_baseline/seed42/temperature_scaling_metrics.json`
- Learned temperature: `1.274009`
- Slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.4577 | 0.4577 |
| Mean glioma probability | 0.4643 | 0.4636 |
| Median glioma probability | 0.3592 | 0.3783 |
| Mean max confidence | 0.8632 | 0.8247 |
| Median max confidence | 0.9354 | 0.8808 |
| Mean entropy | 0.3443 | 0.4474 |
| Median entropy | 0.2640 | 0.4244 |
| Patient-majority glioma rate | 0.4590 | 0.4590 |
| Series-majority glioma rate | 0.4590 | 0.4590 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 1396 | 0.4577 | 1396 | 0.4577 |
| meningioma | 25 | 0.0082 | 25 | 0.0082 |
| notumor | 1597 | 0.5236 | 1597 | 0.5236 |
| pituitary | 32 | 0.0105 | 32 | 0.0105 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 280 | 280 |
| meningioma | 5 | 5 |
| notumor | 319 | 319 |
| pituitary | 6 | 6 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3C, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
