# Per-class internal performance (D1 test)

Mean ± SD across seeds 42-46. Run set `2026-08-sweep-a`.

| Architecture | Class | Precision | Recall | F1 | Support |
|---|---|---|---|---|---|
| ResNet18 | Glioma | 0.9693 ± 0.0131 | 0.9613 ± 0.0090 | 0.9653 ± 0.0106 | 269 |
| ResNet18 | Meningioma | 0.9289 ± 0.0088 | 0.9693 ± 0.0148 | 0.9487 ± 0.0112 | 267 |
| ResNet18 | No tumour | 0.9747 ± 0.0094 | 0.9474 ± 0.0103 | 0.9608 ± 0.0047 | 251 |
| ResNet18 | Pituitary | 0.9947 ± 0.0020 | 0.9856 ± 0.0098 | 0.9901 ± 0.0044 | 264 |
| EfficientNet-B0 | Glioma | 0.9689 ± 0.0217 | 0.9539 ± 0.0119 | 0.9611 ± 0.0081 | 269 |
| EfficientNet-B0 | Meningioma | 0.9276 ± 0.0263 | 0.9768 ± 0.0125 | 0.9513 ± 0.0102 | 267 |
| EfficientNet-B0 | No tumour | 0.9859 ± 0.0022 | 0.9474 ± 0.0086 | 0.9663 ± 0.0046 | 251 |
| EfficientNet-B0 | Pituitary | 0.9917 ± 0.0066 | 0.9894 ± 0.0049 | 0.9905 ± 0.0023 | 264 |
| ViT-B/16 | Glioma | 0.9502 ± 0.0235 | 0.9517 ± 0.0112 | 0.9507 ± 0.0071 | 269 |
| ViT-B/16 | Meningioma | 0.9217 ± 0.0256 | 0.9603 ± 0.0063 | 0.9404 ± 0.0106 | 267 |
| ViT-B/16 | No tumour | 0.9817 ± 0.0129 | 0.9291 ± 0.0044 | 0.9546 ± 0.0040 | 251 |
| ViT-B/16 | Pituitary | 0.9747 ± 0.0158 | 0.9795 ± 0.0124 | 0.9770 ± 0.0037 | 264 |
