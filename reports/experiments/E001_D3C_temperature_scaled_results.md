# E001 on D3C — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E001 ResNet18 trained on D1, evaluated on D3C UPENN-GBM central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3C predictions: `experiments/E001_D1_resnet18_baseline/seed44/d3c_predictions.csv`
- Temperature metrics: `experiments/E001_D1_resnet18_baseline/seed44/temperature_scaling_metrics.json`
- Learned temperature: `1.172485`
- Slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.6541 | 0.6541 |
| Mean glioma probability | 0.5808 | 0.5630 |
| Median glioma probability | 0.6432 | 0.6024 |
| Mean max confidence | 0.7512 | 0.7171 |
| Median max confidence | 0.7639 | 0.7153 |
| Mean entropy | 0.6059 | 0.6871 |
| Median entropy | 0.6412 | 0.7219 |
| Patient-majority glioma rate | 0.6541 | 0.6541 |
| Series-majority glioma rate | 0.6541 | 0.6541 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 1995 | 0.6541 | 1995 | 0.6541 |
| meningioma | 21 | 0.0069 | 21 | 0.0069 |
| notumor | 853 | 0.2797 | 853 | 0.2797 |
| pituitary | 181 | 0.0593 | 181 | 0.0593 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 399 | 399 |
| meningioma | 5 | 5 |
| notumor | 170 | 170 |
| pituitary | 36 | 36 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3C, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
