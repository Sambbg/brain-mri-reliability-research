# E001 - Temperature Scaling Calibration Results

## Experiment

E001 - ResNet18 temperature scaling on D1 leakage-aware split

## Method

Temperature scaling was fitted using validation-set logits only. The learned temperature was then applied to the held-out test set. The model weights were not retrained.

## Temperature

- Learned temperature: `1.172485`

## Test Metrics Before and After Temperature Scaling

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| accuracy | 0.9715 | 0.9715 |
| balanced_accuracy | 0.9712 | 0.9712 |
| macro_f1 | 0.9715 | 0.9715 |
| mean_confidence | 0.9740 | 0.9673 |
| confidence_accuracy_gap | 0.0026 | -0.0042 |
| ece_15_bins | 0.0105 | 0.0092 |
| brier_score | 0.0464 | 0.0465 |
| negative_log_likelihood | 0.1053 | 0.1025 |

## Interpretation

Temperature scaling reduced ECE from 0.0105 to 0.0092. NLL also improved from 0.1053 to 0.1025. The confidence-accuracy gap changed from 0.0026 to -0.0042.

These results are still internal to D1 and should not be interpreted as external reliability evidence. The next major test is whether calibration behaviour changes under cross-dataset evaluation.
