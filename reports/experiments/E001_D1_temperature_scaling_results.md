# E001 - Temperature Scaling Calibration Results

## Experiment

E001 - ResNet18 temperature scaling on D1 leakage-aware split

## Method

Temperature scaling was fitted using validation-set logits only. The learned temperature was then applied to the held-out test set. The model weights were not retrained.

## Temperature

- Learned temperature: `1.232835`

## Test Metrics Before and After Temperature Scaling

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| accuracy | 0.9667 | 0.9667 |
| balanced_accuracy | 0.9662 | 0.9662 |
| macro_f1 | 0.9666 | 0.9666 |
| mean_confidence | 0.9836 | 0.9773 |
| confidence_accuracy_gap | 0.0169 | 0.0106 |
| ece_15_bins | 0.0208 | 0.0145 |
| brier_score | 0.0557 | 0.0536 |
| negative_log_likelihood | 0.1176 | 0.1063 |

## Interpretation

Temperature scaling reduced ECE from 0.0208 to 0.0145. NLL also improved from 0.1176 to 0.1063. The confidence-accuracy gap changed from 0.0169 to 0.0106.

These results are still internal to D1 and should not be interpreted as external reliability evidence. The next major test is whether calibration behaviour changes under cross-dataset evaluation.
