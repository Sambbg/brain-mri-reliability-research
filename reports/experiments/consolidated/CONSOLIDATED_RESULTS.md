# Consolidated Seed-Sweep Results

Generated: 2026-08-25T18:23:49
Run set: 2026-08-sweep-a
Runs: 15 (3 architectures x 5 seeds)

**This file is the authoritative result set.** Any table reporting a single seed, or the Run A / Run B numbers, is superseded.

## Provenance check

All runs share one run_id, one split hash, an identical seed set, and identical probe cohorts. Both probes present for every run.

- D3B cohort: 53 patients, 265 slices
- D3C cohort: 610 patients, 3050 slices

## Per-run results

| Exp | Arch | Seed | macro-F1 | D3B rate | D3C rate | T | commit |
|---|---|---|---|---|---|---|---|
| E001 | ResNet18 | 42 | 0.9546 | 0.3094 | 0.8013 | 1.2699 | `4ec3a01d51ff` |
| E001 | ResNet18 | 43 | 0.9677 | 0.4604 | 0.6331 | 1.2226 | `3a0406b536e7` |
| E001 | ResNet18 | 44 | 0.9715 | 0.3245 | 0.6541 | 1.1725 | `a057978ac883` |
| E001 | ResNet18 | 45 | 0.9723 | 0.5925 | 0.6613 | 1.3113 | `75a89d13c2ac` |
| E001 | ResNet18 | 46 | 0.9650 | 0.3245 | 0.6220 | 1.1519 | `11aab7630af1` |
| E002 | EfficientNet-B0 | 42 | 0.9744 | 0.5962 | 0.4577 | 1.2740 | `d198a69817a6` |
| E002 | EfficientNet-B0 | 43 | 0.9649 | 0.2226 | 0.6118 | 1.3076 | `52d2ee49ec84` |
| E002 | EfficientNet-B0 | 44 | 0.9632 | 0.3811 | 0.5256 | 1.1760 | `b6adecd59871` |
| E002 | EfficientNet-B0 | 45 | 0.9661 | 0.3132 | 0.4525 | 1.0700 | `423dedd2d600` |
| E002 | EfficientNet-B0 | 46 | 0.9678 | 0.3283 | 0.5213 | 1.3040 | `2e2b35191aae` |
| E003 | ViT-B/16 | 42 | 0.9537 | 0.2377 | 0.4630 | 1.2580 | `3e67c73c3711` |
| E003 | ViT-B/16 | 43 | 0.9565 | 0.2453 | 0.2102 | 1.2185 | `11040791e960` |
| E003 | ViT-B/16 | 44 | 0.9588 | 0.3283 | 0.2085 | 1.2295 | `eb12191f403c` |
| E003 | ViT-B/16 | 45 | 0.9564 | 0.2830 | 0.2502 | 1.2339 | `e89841235c46` |
| E003 | ViT-B/16 | 46 | 0.9529 | 0.1509 | 0.1856 | 1.2306 | `36c6809e03e5` |

## Per-architecture summary (mean +/- sd over seeds)

| Arch | n | Internal macro-F1 | D3B glioma rate | D3C glioma rate |
|---|---|---|---|---|
| ResNet18 | 5 | 0.9662 ± 0.0071 | 0.4023 ± 0.1227 | 0.6744 ± 0.0727 |
| EfficientNet-B0 | 5 | 0.9673 ± 0.0043 | 0.3683 ± 0.1396 | 0.5138 ± 0.0646 |
| ViT-B/16 | 5 | 0.9557 ± 0.0024 | 0.2491 ± 0.0656 | 0.2635 ± 0.1139 |

## Ranking stability

How often the architecture ordering changes between seeds. A stable evaluation gives one ordering; an unstable one gives many.

| Evaluation | Seeds | Distinct orderings | Breakdown |
|---|---|---|---|
| test_macro_f1 | 5 | 2 | E001 > E002 > E003 (3); E002 > E001 > E003 (2) |
| d3b_glioma_rate | 5 | 4 | E002 > E001 > E003 (2); E001 > E003 > E002 (1); E002 > E003 > E001 (1); E001 > E002 > E003 (1) |
| d3c_glioma_rate | 5 | 2 | E001 > E002 > E003 (4); E001 > E003 > E002 (1) |

## Signal to noise

Between-architecture spread divided by the mean within-architecture seed SD. Below ~2 the architecture differences are not resolvable against seed variation.

| Evaluation | Spread | Mean seed SD | S/N | Overlapping pairs |
|---|---|---|---|---|
| test_macro_f1 | 0.0116 | 0.0046 | **2.52** | 2/3 |
| d3b_glioma_rate | 0.1532 | 0.1093 | **1.4** | 3/3 |
| d3c_glioma_rate | 0.4109 | 0.0837 | **4.91** | 1/3 |

**test_macro_f1** pairwise ranges:

- E001 vs E002: overlap ? [0.9546, 0.9723] vs [0.9632, 0.9744]
- E001 vs E003: overlap ? [0.9546, 0.9723] vs [0.9529, 0.9588]
- E002 vs E003: separated ? [0.9632, 0.9744] vs [0.9529, 0.9588]

**d3b_glioma_rate** pairwise ranges:

- E001 vs E002: overlap ? [0.3094, 0.5925] vs [0.2226, 0.5962]
- E001 vs E003: overlap ? [0.3094, 0.5925] vs [0.1509, 0.3283]
- E002 vs E003: overlap ? [0.2226, 0.5962] vs [0.1509, 0.3283]

**d3c_glioma_rate** pairwise ranges:

- E001 vs E002: separated ? [0.6220, 0.8013] vs [0.4525, 0.6118]
- E001 vs E003: separated ? [0.6220, 0.8013] vs [0.1856, 0.4630]
- E002 vs E003: overlap ? [0.4525, 0.6118] vs [0.1856, 0.4630]

## Correlation decomposition

Internal macro-F1 against shifted-domain glioma rate, pooled across runs, between architecture means, and within architecture after centring. A sign change between the between- and within- terms is Simpson's paradox.

| Probe | n | r pooled | r between-arch | r within-arch |
|---|---|---|---|---|
| D3B | 15 | +0.756 | +0.956 | +0.664 |
| D3C | 15 | +0.474 | +0.886 | -0.514 |

## Superseded numbers

Do not report these. They are retained as the historical record only.

| Source | What it contains |
|---|---|
| Run A (Ubuntu) | internal, calibration, D3B; no D3C |
| Run B (Windows) | D3C on the earlier 569-patient cohort |
| `tables/table_2`, `table_4` | a single seed presented as the result |
| `tables/table_6` | Run B D3C, superseded cohort |

