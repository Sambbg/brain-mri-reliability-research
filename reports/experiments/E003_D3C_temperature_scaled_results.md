# E003 on D3C — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1, evaluated on D3C UPENN-GBM central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3C predictions: `experiments\E003_D1_vit_b16_baseline\d3c_predictions.csv`
- Temperature metrics: `experiments\E003_D1_vit_b16_baseline\temperature_scaling_metrics.json`
- Learned temperature: `1.377024`
- Slices evaluated: 2845
- Patients represented: 569
- Series represented: 569

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.2179 | 0.2179 |
| Mean glioma probability | 0.2132 | 0.2119 |
| Median glioma probability | 0.0036 | 0.0157 |
| Mean max confidence | 0.9115 | 0.8744 |
| Median max confidence | 0.9877 | 0.9535 |
| Mean entropy | 0.2261 | 0.3332 |
| Median entropy | 0.0728 | 0.2156 |
| Patient-majority glioma rate | 0.2250 | 0.2250 |
| Series-majority glioma rate | 0.2250 | 0.2250 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 620 | 0.2179 | 620 | 0.2179 |
| meningioma | 210 | 0.0738 | 210 | 0.0738 |
| notumor | 1973 | 0.6935 | 1973 | 0.6935 |
| pituitary | 42 | 0.0148 | 42 | 0.0148 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 128 | 128 |
| meningioma | 30 | 30 |
| notumor | 403 | 403 |
| pituitary | 8 | 8 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3C, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
