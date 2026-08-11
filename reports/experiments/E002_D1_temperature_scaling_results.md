# E002 - Temperature Scaling Calibration Results

## Experiment

E002 - EfficientNet-B0 temperature scaling on D1 leakage-aware split

## Method

Temperature scaling was fitted using validation-set logits only. The learned temperature was then applied to the held-out test set. The model weights were not retrained.

## Temperature

- Learned temperature: `1.303988`

## Test Metrics Before and After Temperature Scaling

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| accuracy | 0.9676 | 0.9676 |
| balanced_accuracy | 0.9674 | 0.9674 |
| macro_f1 | 0.9678 | 0.9678 |
| mean_confidence | 0.9867 | 0.9809 |
| confidence_accuracy_gap | 0.0190 | 0.0132 |
| ece_15_bins | 0.0206 | 0.0142 |
| brier_score | 0.0496 | 0.0474 |
| negative_log_likelihood | 0.1102 | 0.0951 |

## Interpretation

Temperature scaling reduced ECE from 0.0206 to 0.0142. NLL also improved from 0.1102 to 0.0951. The confidence-accuracy gap changed from 0.0190 to 0.0132.

These results are still internal to D1 and should not be interpreted as external reliability evidence. The next major test is whether calibration behaviour changes under cross-dataset evaluation.
