# E002 - Temperature Scaling Calibration Results

## Experiment

E002 - EfficientNet-B0 temperature scaling on D1 leakage-aware split

## Method

Temperature scaling was fitted using validation-set logits only. The learned temperature was then applied to the held-out test set. The model weights were not retrained.

## Temperature

- Learned temperature: `1.274009`

## Test Metrics Before and After Temperature Scaling

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| accuracy | 0.9743 | 0.9743 |
| balanced_accuracy | 0.9742 | 0.9742 |
| macro_f1 | 0.9744 | 0.9744 |
| mean_confidence | 0.9834 | 0.9781 |
| confidence_accuracy_gap | 0.0091 | 0.0037 |
| ece_15_bins | 0.0150 | 0.0098 |
| brier_score | 0.0409 | 0.0405 |
| negative_log_likelihood | 0.1026 | 0.0917 |

## Interpretation

Temperature scaling reduced ECE from 0.0150 to 0.0098. NLL also improved from 0.1026 to 0.0917. The confidence-accuracy gap changed from 0.0091 to 0.0037.

These results are still internal to D1 and should not be interpreted as external reliability evidence. The next major test is whether calibration behaviour changes under cross-dataset evaluation.
