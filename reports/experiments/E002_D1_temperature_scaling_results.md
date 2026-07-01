# E002 - Temperature Scaling Calibration Results

## Experiment

E002 - EfficientNet-B0 temperature scaling on D1 leakage-aware split

## Method

Temperature scaling was fitted using validation-set logits only. The learned temperature was then applied to the held-out test set. The model weights were not retrained.

## Temperature

- Learned temperature: `1.159631`

## Test Metrics Before and After Temperature Scaling

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| accuracy | 0.9676 | 0.9676 |
| balanced_accuracy | 0.9677 | 0.9677 |
| macro_f1 | 0.9680 | 0.9680 |
| mean_confidence | 0.9812 | 0.9759 |
| confidence_accuracy_gap | 0.0135 | 0.0082 |
| ece_15_bins | 0.0186 | 0.0152 |
| brier_score | 0.0533 | 0.0523 |
| negative_log_likelihood | 0.1091 | 0.1034 |

## Interpretation

Temperature scaling reduced ECE from 0.0186 to 0.0152. NLL also improved from 0.1091 to 0.1034. The confidence-accuracy gap changed from 0.0135 to 0.0082.

These results are still internal to D1 and should not be interpreted as external reliability evidence. The next major test is whether calibration behaviour changes under cross-dataset evaluation.
