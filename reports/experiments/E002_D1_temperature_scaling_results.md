# E002 - Temperature Scaling Calibration Results

## Experiment

E002 - EfficientNet-B0 temperature scaling on D1 leakage-aware split

## Method

Temperature scaling was fitted using validation-set logits only. The learned temperature was then applied to the held-out test set. The model weights were not retrained.

## Temperature

- Learned temperature: `1.307584`

## Test Metrics Before and After Temperature Scaling

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| accuracy | 0.9648 | 0.9648 |
| balanced_accuracy | 0.9645 | 0.9645 |
| macro_f1 | 0.9649 | 0.9649 |
| mean_confidence | 0.9854 | 0.9792 |
| confidence_accuracy_gap | 0.0206 | 0.0144 |
| ece_15_bins | 0.0206 | 0.0157 |
| brier_score | 0.0521 | 0.0498 |
| negative_log_likelihood | 0.1262 | 0.1081 |

## Interpretation

Temperature scaling reduced ECE from 0.0206 to 0.0157. NLL also improved from 0.1262 to 0.1081. The confidence-accuracy gap changed from 0.0206 to 0.0144.

These results are still internal to D1 and should not be interpreted as external reliability evidence. The next major test is whether calibration behaviour changes under cross-dataset evaluation.
