# E001 - Temperature Scaling Calibration Results

## Experiment

E001 - ResNet18 temperature scaling on D1 leakage-aware split

## Method

Temperature scaling was fitted using validation-set logits only. The learned temperature was then applied to the held-out test set. The model weights were not retrained.

## Temperature

- Learned temperature: `1.272483`

## Test Metrics Before and After Temperature Scaling

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| accuracy | 0.9753 | 0.9753 |
| balanced_accuracy | 0.9753 | 0.9753 |
| macro_f1 | 0.9753 | 0.9753 |
| mean_confidence | 0.9838 | 0.9773 |
| confidence_accuracy_gap | 0.0085 | 0.0021 |
| ece_15_bins | 0.0149 | 0.0119 |
| brier_score | 0.0435 | 0.0434 |
| negative_log_likelihood | 0.1223 | 0.1080 |

## Interpretation

Temperature scaling reduced ECE from 0.0149 to 0.0119. NLL also improved from 0.1223 to 0.1080. The confidence-accuracy gap changed from 0.0085 to 0.0021.

These results are still internal to D1 and should not be interpreted as external reliability evidence. The next major test is whether calibration behaviour changes under cross-dataset evaluation.
