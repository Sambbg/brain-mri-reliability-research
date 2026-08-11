# E001 - Temperature Scaling Calibration Results

## Experiment

E001 - ResNet18 temperature scaling on D1 leakage-aware split

## Method

Temperature scaling was fitted using validation-set logits only. The learned temperature was then applied to the held-out test set. The model weights were not retrained.

## Temperature

- Learned temperature: `1.311330`

## Test Metrics Before and After Temperature Scaling

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| accuracy | 0.9724 | 0.9724 |
| balanced_accuracy | 0.9719 | 0.9719 |
| macro_f1 | 0.9723 | 0.9723 |
| mean_confidence | 0.9880 | 0.9816 |
| confidence_accuracy_gap | 0.0156 | 0.0092 |
| ece_15_bins | 0.0173 | 0.0124 |
| brier_score | 0.0474 | 0.0461 |
| negative_log_likelihood | 0.1355 | 0.1141 |

## Interpretation

Temperature scaling reduced ECE from 0.0173 to 0.0124. NLL also improved from 0.1355 to 0.1141. The confidence-accuracy gap changed from 0.0156 to 0.0092.

These results are still internal to D1 and should not be interpreted as external reliability evidence. The next major test is whether calibration behaviour changes under cross-dataset evaluation.
