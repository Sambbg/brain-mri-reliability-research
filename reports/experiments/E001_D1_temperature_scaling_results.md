# E001 - Temperature Scaling Calibration Results

## Experiment

E001 - ResNet18 temperature scaling on D1 leakage-aware split

## Method

Temperature scaling was fitted using validation-set logits only. The learned temperature was then applied to the held-out test set. The model weights were not retrained.

## Temperature

- Learned temperature: `1.151924`

## Test Metrics Before and After Temperature Scaling

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| accuracy | 0.9648 | 0.9648 |
| balanced_accuracy | 0.9648 | 0.9648 |
| macro_f1 | 0.9650 | 0.9650 |
| mean_confidence | 0.9693 | 0.9625 |
| confidence_accuracy_gap | 0.0045 | -0.0023 |
| ece_15_bins | 0.0162 | 0.0099 |
| brier_score | 0.0535 | 0.0534 |
| negative_log_likelihood | 0.1066 | 0.1056 |

## Interpretation

Temperature scaling reduced ECE from 0.0162 to 0.0099. NLL also improved from 0.1066 to 0.1056. The confidence-accuracy gap changed from 0.0045 to -0.0023.

These results are still internal to D1 and should not be interpreted as external reliability evidence. The next major test is whether calibration behaviour changes under cross-dataset evaluation.
