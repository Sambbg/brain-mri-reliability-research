# Figure Captions

## Figure 2. Internal D1 test macro-F1 across models

Comparison of test macro-F1 for ResNet18, EfficientNet-B0, and ViT-B/16 on the D1 leakage-aware test split. All models achieved high internal performance, with EfficientNet-B0 performing slightly best and ViT-B/16 performing lowest among the three models.

## Figure 3. Internal calibration before and after temperature scaling

Expected calibration error before and after post-hoc temperature scaling on the D1 test split. Temperature scaling reduced ECE for all three models, indicating improved internal confidence calibration without changing classification accuracy.

## Figure 4. D3B glioma prediction rate across models

Slice-level glioma prediction rate on D3B, a visually distinct glioma-focused domain-shift dataset. None of the three D1-trained models predicted glioma for a majority of D3B slices, despite strong internal D1 test performance.

## Figure 5. D3B prediction distribution across models

Distribution of predicted D1 classes for D3B images. The models assigned many D3B glioma-domain slices to non-glioma classes, showing unstable prediction behaviour under dataset shift.

## Figure 6. D3B confidence before and after temperature scaling

Mean maximum softmax confidence on D3B before and after applying temperature values learned from D1 validation logits. Temperature scaling softened confidence under domain shift but did not change the class prediction distribution.
