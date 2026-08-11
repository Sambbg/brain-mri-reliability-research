# E003 on D3C — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1, evaluated on D3C UPENN-GBM central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3C predictions: `experiments/E003_D1_vit_b16_baseline/seed43/d3c_predictions.csv`
- Temperature metrics: `experiments/E003_D1_vit_b16_baseline/seed43/temperature_scaling_metrics.json`
- Learned temperature: `1.218531`
- Slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.2102 | 0.2102 |
| Mean glioma probability | 0.2165 | 0.2194 |
| Median glioma probability | 0.0194 | 0.0379 |
| Mean max confidence | 0.9018 | 0.8773 |
| Median max confidence | 0.9793 | 0.9565 |
| Mean entropy | 0.2542 | 0.3264 |
| Median entropy | 0.1077 | 0.2026 |
| Patient-majority glioma rate | 0.2016 | 0.2016 |
| Series-majority glioma rate | 0.2016 | 0.2016 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 641 | 0.2102 | 641 | 0.2102 |
| meningioma | 83 | 0.0272 | 83 | 0.0272 |
| notumor | 2307 | 0.7564 | 2307 | 0.7564 |
| pituitary | 19 | 0.0062 | 19 | 0.0062 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 123 | 123 |
| meningioma | 8 | 8 |
| notumor | 475 | 475 |
| pituitary | 4 | 4 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3C, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
