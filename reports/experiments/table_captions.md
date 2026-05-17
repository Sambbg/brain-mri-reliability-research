# Table Captions

## Table 1. Dataset summary and usage decision

Summary of the datasets considered in the study, including their role, label structure, and final usage decision. D1 was used as the primary internal four-class dataset. D2 was rejected as a clean external validation dataset because overlap auditing showed substantial overlap with D1. D3B was used as a visually distinct glioma-focused domain-shift dataset.

## Table 2. Internal D1 test performance across models

Comparison of ResNet18, EfficientNet-B0, and ViT-B/16 on the D1 leakage-aware test split. Metrics include test accuracy, balanced accuracy, macro-F1, best validation macro-F1, and best epoch. EfficientNet-B0 achieved the strongest internal performance, while ViT-B/16 performed lowest among the three models.

## Table 3. Internal calibration before and after temperature scaling

Internal D1 calibration metrics before and after post-hoc temperature scaling. Temperature scaling was fitted using validation logits only and evaluated on the held-out D1 test split. Calibration improved across all three models, as shown by reduced ECE, NLL, and confidence-accuracy gap.

## Table 4. D3B domain-shift behaviour across models

Glioma-focused domain-shift behaviour on D3B. Because D3B is not a full four-class external validation dataset, results are interpreted as prediction-distribution and confidence behaviour rather than conventional external accuracy. None of the three models predicted glioma for a majority of D3B slices.

## Table 5. D3B raw versus temperature-scaled behaviour

Comparison of raw and temperature-scaled confidence behaviour on D3B. Temperature scaling softened confidence and increased entropy, but it did not change glioma prediction rates or patient-majority/series-majority prediction behaviour.
