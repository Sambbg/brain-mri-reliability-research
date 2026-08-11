# E003 on D3C — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1, evaluated on D3C UPENN-GBM central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3C predictions: `experiments/E003_D1_vit_b16_baseline/seed44/d3c_predictions.csv`
- Temperature metrics: `experiments/E003_D1_vit_b16_baseline/seed44/temperature_scaling_metrics.json`
- Learned temperature: `1.229500`
- Slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.2085 | 0.2085 |
| Mean glioma probability | 0.2151 | 0.2183 |
| Median glioma probability | 0.0261 | 0.0468 |
| Mean max confidence | 0.8384 | 0.8027 |
| Median max confidence | 0.9083 | 0.8535 |
| Mean entropy | 0.4068 | 0.5021 |
| Median entropy | 0.3505 | 0.4987 |
| Patient-majority glioma rate | 0.2016 | 0.2016 |
| Series-majority glioma rate | 0.2016 | 0.2016 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 636 | 0.2085 | 636 | 0.2085 |
| meningioma | 168 | 0.0551 | 168 | 0.0551 |
| notumor | 1948 | 0.6387 | 1948 | 0.6387 |
| pituitary | 298 | 0.0977 | 298 | 0.0977 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 123 | 123 |
| meningioma | 26 | 26 |
| notumor | 402 | 402 |
| pituitary | 59 | 59 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3C, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
