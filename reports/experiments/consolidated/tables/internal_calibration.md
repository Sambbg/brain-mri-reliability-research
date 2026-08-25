# Internal calibration before and after temperature scaling

Mean ± SD across seeds 42-46 on the D1 test split. Lower is better for all four metrics. Run set `2026-08-sweep-a`.

**The learned temperature is a property of the checkpoint, not the architecture** ? it varies materially across seeds, so it is reported with dispersion rather than as a single value.

| Architecture | T | ECE raw ? scaled | NLL raw ? scaled | Brier raw ? scaled | Conf?acc gap raw ? scaled |
|---|---|---|---|---|---|
| ResNet18 | 1.2257 ± 0.0663 [1.1519?1.3113] | 0.0158 ± 0.0030 ? 0.0113 ± 0.0016 | 0.1186 ± 0.0167 ? 0.1101 ± 0.0115 | 0.0529 ± 0.0077 ? 0.0519 ± 0.0071 | 0.0108 ± 0.0067 ? 0.0034 ± 0.0062 |
| EfficientNet-B0 | 1.2263 ± 0.1023 [1.0700?1.3076] | 0.0194 ± 0.0055 ? 0.0155 ± 0.0051 | 0.1190 ± 0.0147 ? 0.1069 ± 0.0141 | 0.0518 ± 0.0076 ? 0.0504 ± 0.0073 | 0.0160 ± 0.0066 ? 0.0113 ± 0.0062 |
| ViT-B/16 | 1.2341 ± 0.0145 [1.2185?1.2580] | 0.0259 ± 0.0036 ? 0.0208 ± 0.0048 | 0.1539 ± 0.0165 ? 0.1396 ± 0.0133 | 0.0707 ± 0.0066 ? 0.0683 ± 0.0058 | 0.0221 ± 0.0030 ? 0.0137 ± 0.0031 |
