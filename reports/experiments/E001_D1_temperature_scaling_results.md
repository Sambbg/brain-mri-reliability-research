# E001 - Temperature Scaling Calibration Results

## Experiment

E001 - ResNet18 temperature scaling on D1 leakage-aware split

## Method

Temperature scaling was fitted using validation-set logits only. The learned temperature was then applied to the held-out test set. The model weights were not retrained.

## Temperature

- Learned temperature: `1.222596`

## Test Metrics Before and After Temperature Scaling

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| accuracy | 0.9676 | 0.9676 |
| balanced_accuracy | 0.9674 | 0.9674 |
| macro_f1 | 0.9677 | 0.9677 |
| mean_confidence | 0.9823 | 0.9752 |
| confidence_accuracy_gap | 0.0146 | 0.0075 |
| ece_15_bins | 0.0169 | 0.0121 |
| brier_score | 0.0517 | 0.0501 |
| negative_log_likelihood | 0.1073 | 0.0998 |

## Interpretation

Temperature scaling reduced ECE from 0.0169 to 0.0121. NLL also improved from 0.1073 to 0.0998. The confidence-accuracy gap changed from 0.0146 to 0.0075.

These results are still internal to D1 and should not be interpreted as external reliability evidence. The next major test is whether calibration behaviour changes under cross-dataset evaluation.
