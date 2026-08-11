# E002 - Temperature Scaling Calibration Results

## Experiment

E002 - EfficientNet-B0 temperature scaling on D1 leakage-aware split

## Method

Temperature scaling was fitted using validation-set logits only. The learned temperature was then applied to the held-out test set. The model weights were not retrained.

## Temperature

- Learned temperature: `1.070038`

## Test Metrics Before and After Temperature Scaling

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| accuracy | 0.9657 | 0.9657 |
| balanced_accuracy | 0.9656 | 0.9656 |
| macro_f1 | 0.9661 | 0.9661 |
| mean_confidence | 0.9745 | 0.9719 |
| confidence_accuracy_gap | 0.0087 | 0.0062 |
| ece_15_bins | 0.0133 | 0.0139 |
| brier_score | 0.0549 | 0.0547 |
| negative_log_likelihood | 0.1156 | 0.1131 |

## Interpretation

Temperature scaling did not reduce ECE; ECE changed from 0.0133 to 0.0139. NLL also improved from 0.1156 to 0.1131. The confidence-accuracy gap changed from 0.0087 to 0.0062.

These results are still internal to D1 and should not be interpreted as external reliability evidence. The next major test is whether calibration behaviour changes under cross-dataset evaluation.
