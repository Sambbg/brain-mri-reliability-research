# E003 on D3C — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E003 ViT-B/16 trained on D1, evaluated on D3C UPENN-GBM central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3C predictions: `experiments/E003_D1_vit_b16_baseline/seed46/d3c_predictions.csv`
- Temperature metrics: `experiments/E003_D1_vit_b16_baseline/seed46/temperature_scaling_metrics.json`
- Learned temperature: `1.230566`
- Slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.1856 | 0.1856 |
| Mean glioma probability | 0.1853 | 0.1872 |
| Median glioma probability | 0.0132 | 0.0286 |
| Mean max confidence | 0.8839 | 0.8579 |
| Median max confidence | 0.9767 | 0.9497 |
| Mean entropy | 0.2899 | 0.3597 |
| Median entropy | 0.1213 | 0.2317 |
| Patient-majority glioma rate | 0.1852 | 0.1852 |
| Series-majority glioma rate | 0.1852 | 0.1852 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 566 | 0.1856 | 566 | 0.1856 |
| meningioma | 336 | 0.1102 | 336 | 0.1102 |
| notumor | 2142 | 0.7023 | 2142 | 0.7023 |
| pituitary | 6 | 0.0020 | 6 | 0.0020 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 113 | 113 |
| meningioma | 57 | 57 |
| notumor | 439 | 439 |
| pituitary | 1 | 1 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3C, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
