# E003 on D3C — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1, evaluated on D3C UPENN-GBM central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3C predictions: `experiments/E003_D1_vit_b16_baseline/seed42/d3c_predictions.csv`
- Temperature metrics: `experiments/E003_D1_vit_b16_baseline/seed42/temperature_scaling_metrics.json`
- Learned temperature: `1.257989`
- Slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.4630 | 0.4630 |
| Mean glioma probability | 0.4402 | 0.4301 |
| Median glioma probability | 0.3769 | 0.3829 |
| Mean max confidence | 0.8041 | 0.7586 |
| Median max confidence | 0.8556 | 0.7854 |
| Mean entropy | 0.4888 | 0.6060 |
| Median entropy | 0.4720 | 0.6286 |
| Patient-majority glioma rate | 0.4770 | 0.4770 |
| Series-majority glioma rate | 0.4770 | 0.4770 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 1412 | 0.4630 | 1412 | 0.4630 |
| meningioma | 456 | 0.1495 | 456 | 0.1495 |
| notumor | 1021 | 0.3348 | 1021 | 0.3348 |
| pituitary | 161 | 0.0528 | 161 | 0.0528 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 291 | 291 |
| meningioma | 84 | 84 |
| notumor | 211 | 211 |
| pituitary | 24 | 24 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3C, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
