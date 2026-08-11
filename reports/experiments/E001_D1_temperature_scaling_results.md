# E001 - Temperature Scaling Calibration Results

## Experiment

E001 - ResNet18 temperature scaling on D1 leakage-aware split

## Method

Temperature scaling was fitted using validation-set logits only. The learned temperature was then applied to the held-out test set. The model weights were not retrained.

## Temperature

- Learned temperature: `1.269943`

## Test Metrics Before and After Temperature Scaling

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| accuracy | 0.9543 | 0.9543 |
| balanced_accuracy | 0.9542 | 0.9542 |
| macro_f1 | 0.9546 | 0.9546 |
| mean_confidence | 0.9710 | 0.9612 |
| confidence_accuracy_gap | 0.0167 | 0.0069 |
| ece_15_bins | 0.0181 | 0.0128 |
| brier_score | 0.0656 | 0.0633 |
| negative_log_likelihood | 0.1383 | 0.1283 |

## Interpretation

Temperature scaling reduced ECE from 0.0181 to 0.0128. NLL also improved from 0.1383 to 0.1283. The confidence-accuracy gap changed from 0.0167 to 0.0069.

These results are still internal to D1 and should not be interpreted as external reliability evidence. The next major test is whether calibration behaviour changes under cross-dataset evaluation.
