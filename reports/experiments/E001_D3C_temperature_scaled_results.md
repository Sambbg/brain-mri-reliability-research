# E001 on D3C — Temperature-Scaled Domain-Shift Evaluation

## Experiment

E001 ResNet18 trained on D1, evaluated on D3C UPENN-GBM central slices. The temperature value was learned previously using the D1 validation set only.

## Inputs

- Raw D3C predictions: `experiments/E001_D1_resnet18_baseline/seed45/d3c_predictions.csv`
- Temperature metrics: `experiments/E001_D1_resnet18_baseline/seed45/temperature_scaling_metrics.json`
- Learned temperature: `1.311330`
- Slices evaluated: 3050
- Patients represented: 610
- Series represented: 610

## Critical Interpretation Rule

D3C is glioma-focused and does not contain the full four-class label set. This is not four-class external accuracy. It is a domain-shift confidence and prediction-distribution analysis.

## Raw vs Temperature-Scaled Metrics

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Glioma prediction rate, slice-level | 0.6613 | 0.6613 |
| Mean glioma probability | 0.6159 | 0.5924 |
| Median glioma probability | 0.7470 | 0.6680 |
| Mean max confidence | 0.8219 | 0.7713 |
| Median max confidence | 0.8801 | 0.8035 |
| Mean entropy | 0.4442 | 0.5742 |
| Median entropy | 0.4160 | 0.6009 |
| Patient-majority glioma rate | 0.6787 | 0.6787 |
| Series-majority glioma rate | 0.6787 | 0.6787 |

## Slice-Level Prediction Distribution

| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |
|---|---:|---:|---:|---:|
| glioma | 2017 | 0.6613 | 2017 | 0.6613 |
| meningioma | 13 | 0.0043 | 13 | 0.0043 |
| notumor | 911 | 0.2987 | 911 | 0.2987 |
| pituitary | 109 | 0.0357 | 109 | 0.0357 |

## Patient-Level Majority Prediction Distribution

| Class | Raw patient count | Scaled patient count |
|---|---:|---:|
| glioma | 414 | 414 |
| meningioma | 2 | 2 |
| notumor | 179 | 179 |
| pituitary | 15 | 15 |

## Interpretation

Temperature scaling changes confidence values but does not retrain the model or change the underlying feature representation. If the prediction distribution remains unstable across D3C, this indicates that the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.
