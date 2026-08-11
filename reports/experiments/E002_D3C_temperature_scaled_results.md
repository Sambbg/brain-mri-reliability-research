# E002 on D3C — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E002 EfficientNet-B0 trained on D1, evaluated on D3C UPENN-GBM central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3C predictions: `experiments/E002_D1_efficientnet_b0_baseline/seed44/d3c_predictions.csv`
- Temperature metrics: `experiments/E002_D1_efficientnet_b0_baseline/seed44/temperature_scaling_metrics.json`
- Learned temperature: `1.176001`
- Slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.5256 | 0.5256 |
| Mean glioma probability | 0.5098 | 0.5018 |
| Median glioma probability | 0.4932 | 0.4706 |
| Mean max confidence | 0.7950 | 0.7627 |
| Median max confidence | 0.8474 | 0.7949 |
| Mean entropy | 0.5235 | 0.6056 |
| Median entropy | 0.5180 | 0.6342 |
| Patient-majority glioma rate | 0.5344 | 0.5344 |
| Series-majority glioma rate | 0.5344 | 0.5344 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 1603 | 0.5256 | 1603 | 0.5256 |
| meningioma | 54 | 0.0177 | 54 | 0.0177 |
| notumor | 1237 | 0.4056 | 1237 | 0.4056 |
| pituitary | 156 | 0.0511 | 156 | 0.0511 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 326 | 326 |
| meningioma | 6 | 6 |
| notumor | 254 | 254 |
| pituitary | 24 | 24 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3C, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
