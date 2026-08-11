# D3C Seed Sweep Statistics

Generated: 2026-08-12T00:02:42

Run set `2026-08-sweep-a`, 15 runs (3 architectures x 5 seeds). D3C analysis cohort: 610 patients, 3050 slices.

## Part 1: Internal Performance against Shifted-Domain Behaviour

Pearson r with a Fisher-z interval, and Spearman rho. Read the architecture-centred row, not the pooled one: architecture is a confounder, and a pooled correlation mixes the between-architecture relationship with the within-architecture one.

| Grouping | n | Pearson r | 95% CI | p | Spearman rho | p |
|---|---:|---:|---|---:|---:|---:|
| pooled (all 15 runs) | 15 | 0.474 | [-0.050, 0.794] | 0.0741 | 0.421 | 0.1177 |
| E001 ResNet18 (within, n=5) | 5 | -0.799 | [-0.986, 0.282] | 0.1049 | 0.000 | 1.0000 |
| E002 EfficientNet-B0 (within, n=5) | 5 | -0.542 | [-0.964, 0.652] | 0.3448 | -0.600 | 0.2848 |
| E003 ViT-B/16 (within, n=5) | 5 | -0.376 | [-0.945, 0.757] | 0.5324 | 0.000 | 1.0000 |
| architecture-centred (within-architecture pooled) | 15 | -0.514 | [-0.840, 0.084] | 0.0498 | -0.389 | 0.1515 |

Notes:

- pooled (all 15 runs): confounded by architecture; reported for completeness only
- E001 ResNet18 (within, n=5): n=5, very low power; |r| must exceed about 0.88 for p<0.05
- E002 EfficientNet-B0 (within, n=5): n=5, very low power; |r| must exceed about 0.88 for p<0.05
- E003 ViT-B/16 (within, n=5): n=5, very low power; |r| must exceed about 0.88 for p<0.05
- architecture-centred (within-architecture pooled): architecture means removed; this is the within-architecture estimate

## Part 2a: Patient-Clustered Bootstrap Intervals

2000 resamples of patients, not slices. Each patient contributes five correlated slices, so a slice-level interval would be too narrow by roughly the design effect.

| Model | Seed | Glioma rate | 95% CI | Width | ICC |
|---|---:|---:|---|---:|---:|
| E001 ResNet18 | 42 | 0.8013 | [0.7731, 0.8279] | 0.0548 | 0.664 |
| E001 ResNet18 | 43 | 0.6331 | [0.6007, 0.6646] | 0.0639 | 0.629 |
| E001 ResNet18 | 44 | 0.6541 | [0.6226, 0.6852] | 0.0626 | 0.595 |
| E001 ResNet18 | 45 | 0.6613 | [0.6302, 0.6921] | 0.0620 | 0.622 |
| E001 ResNet18 | 46 | 0.6220 | [0.5908, 0.6548] | 0.0639 | 0.630 |
| E002 EfficientNet-B0 | 42 | 0.4577 | [0.4246, 0.4915] | 0.0669 | 0.679 |
| E002 EfficientNet-B0 | 43 | 0.6118 | [0.5780, 0.6449] | 0.0669 | 0.644 |
| E002 EfficientNet-B0 | 44 | 0.5256 | [0.4928, 0.5587] | 0.0659 | 0.649 |
| E002 EfficientNet-B0 | 45 | 0.4525 | [0.4190, 0.4843] | 0.0653 | 0.631 |
| E002 EfficientNet-B0 | 46 | 0.5213 | [0.4879, 0.5541] | 0.0662 | 0.690 |
| E003 ViT-B/16 | 42 | 0.4630 | [0.4338, 0.4935] | 0.0597 | 0.489 |
| E003 ViT-B/16 | 43 | 0.2102 | [0.1846, 0.2367] | 0.0521 | 0.570 |
| E003 ViT-B/16 | 44 | 0.2085 | [0.1833, 0.2361] | 0.0528 | 0.606 |
| E003 ViT-B/16 | 45 | 0.2502 | [0.2213, 0.2767] | 0.0554 | 0.550 |
| E003 ViT-B/16 | 46 | 0.1856 | [0.1616, 0.2108] | 0.0492 | 0.547 |

## Part 2b: McNemar with Holm Correction

Paired over identical slices, corrected across the three comparisons within each seed.

| Seed | Comparison | b | c | Discordant | Method | p | Holm p | Sig. |
|---|---|---:|---:|---:|---|---:|---:|---|
| 42 | E001 vs E002 | 1203 | 155 | 1358 | chi2_continuity_corrected | 1.451e-177 | 4.353e-177 | yes |
| 42 | E001 vs E003 | 1177 | 145 | 1322 | chi2_continuity_corrected | 7.086e-177 | 1.417e-176 | yes |
| 42 | E002 vs E003 | 456 | 472 | 928 | chi2_continuity_corrected | 6.224e-01 | 6.224e-01 | no |
| 43 | E001 vs E002 | 474 | 409 | 883 | chi2_continuity_corrected | 3.126e-02 | 3.126e-02 | yes |
| 43 | E001 vs E003 | 1362 | 72 | 1434 | chi2_continuity_corrected | 5.880e-254 | 1.764e-253 | yes |
| 43 | E002 vs E003 | 1273 | 48 | 1321 | chi2_continuity_corrected | 1.267e-248 | 2.533e-248 | yes |
| 44 | E001 vs E002 | 713 | 321 | 1034 | chi2_continuity_corrected | 5.106e-34 | 5.106e-34 | yes |
| 44 | E001 vs E003 | 1434 | 75 | 1509 | chi2_continuity_corrected | 9.555e-268 | 2.866e-267 | yes |
| 44 | E002 vs E003 | 1034 | 67 | 1101 | chi2_continuity_corrected | 2.475e-186 | 4.949e-186 | yes |
| 45 | E001 vs E002 | 767 | 130 | 897 | chi2_continuity_corrected | 4.496e-100 | 8.993e-100 | yes |
| 45 | E001 vs E003 | 1329 | 75 | 1404 | chi2_continuity_corrected | 3.585e-245 | 1.076e-244 | yes |
| 45 | E002 vs E003 | 807 | 190 | 997 | chi2_continuity_corrected | 9.222e-85 | 9.222e-85 | yes |
| 46 | E001 vs E002 | 628 | 321 | 949 | chi2_continuity_corrected | 2.986e-23 | 2.986e-23 | yes |
| 46 | E001 vs E003 | 1399 | 68 | 1467 | chi2_continuity_corrected | 3.358e-264 | 1.007e-263 | yes |
| 46 | E002 vs E003 | 1082 | 58 | 1140 | chi2_continuity_corrected | 1.194e-201 | 2.389e-201 | yes |

## Part 2c: Random-Intercept Logistic Regression

`glioma_predicted ~ model + (1|patient)`, fitted per seed with E001 as the reference level. The `model[E002]` coefficient is therefore the E001-vs-E002 contrast: a log odds ratio for predicting glioma, holding the patient fixed.

| Seed | Term | log OR | SE | OR | 95% CI | p | Patient SD | ICC |
|---|---|---:|---:|---:|---|---:|---:|---:|
| 42 | intercept | 2.3056 | 0.1061 | 10.0302 | [8.1466, 12.3492] | 1.167e-104 | 2.206 | 0.597 |
| 42 | model[E002] | -2.5707 | 0.0827 | 0.0765 | [0.0650, 0.0899] | 6.147e-212 | 2.206 | 0.597 |
| 42 | model[E003] | -2.5349 | 0.0825 | 0.0793 | [0.0674, 0.0932] | 2.942e-207 | 2.206 | 0.597 |
| 43 | intercept | 1.0169 | 0.1198 | 2.7647 | [2.1859, 3.4967] | 2.155e-17 | 2.591 | 0.671 |
| 43 | model[E002] | -0.1703 | 0.0725 | 0.8434 | [0.7318, 0.9721] | 1.877e-02 | 2.591 | 0.671 |
| 43 | model[E003] | -3.5220 | 0.0997 | 0.0295 | [0.0243, 0.0359] | 3.515e-273 | 2.591 | 0.671 |
| 44 | intercept | 1.0970 | 0.1290 | 2.9953 | [2.3261, 3.8571] | 1.843e-17 | 2.439 | 0.644 |
| 44 | model[E002] | -0.9566 | 0.0719 | 0.3842 | [0.3337, 0.4424] | 2.448e-40 | 2.439 | 0.644 |
| 44 | model[E003] | -3.5525 | 0.0964 | 0.0287 | [0.0237, 0.0346] | 1.833e-297 | 2.439 | 0.644 |
| 45 | intercept | 1.2470 | 0.1215 | 3.4800 | [2.7424, 4.4161] | 1.063e-24 | 2.584 | 0.670 |
| 45 | model[E002] | -1.6544 | 0.0785 | 0.1912 | [0.1639, 0.2230] | 1.676e-98 | 2.584 | 0.670 |
| 45 | model[E003] | -3.3451 | 0.0940 | 0.0353 | [0.0293, 0.0424] | 1.181e-277 | 2.584 | 0.670 |
| 46 | intercept | 0.8780 | 0.1281 | 2.4061 | [1.8718, 3.0930] | 7.255e-12 | 2.551 | 0.664 |
| 46 | model[E002] | -0.7786 | 0.0727 | 0.4590 | [0.3981, 0.5293] | 9.001e-27 | 2.551 | 0.664 |
| 46 | model[E003] | -3.6826 | 0.1015 | 0.0252 | [0.0206, 0.0307] | 1.925e-288 | 2.551 | 0.664 |

## The E001 vs E002 Contrast

The paper's central comparison. Internally these two models are separated by 0.0011 macro-F1, a fraction of their seed-to-seed spread, and they swap rank between seeds. Under shift:

| Seed | OR (E002 vs E001) | 95% CI | p | Direction |
|---|---:|---|---:|---|
| 42 | 0.0765 | [0.0650, 0.0899] | 6.147e-212 | E002 lower |
| 43 | 0.8434 | [0.7318, 0.9721] | 1.877e-02 | E002 lower |
| 44 | 0.3842 | [0.3337, 0.4424] | 2.448e-40 | E002 lower |
| 45 | 0.1912 | [0.1639, 0.2230] | 1.676e-98 | E002 lower |
| 46 | 0.4590 | [0.3981, 0.5293] | 9.001e-27 | E002 lower |

Direction consistent across all 5 seeds: yes. Significant at every seed: yes.

## Limitations

- The within-architecture correlations have n=5. They are descriptive; |r| must exceed about 0.88 to reach p<0.05 at that size.
- The mixed model is fitted per seed. Pooling seeds would need a second random effect for seed, which is not implemented.
- Quadrature is fixed at 31 nodes and is not adaptive; stability against node count was checked at this data shape in the src/stats test suite.
- D3C carries no slice-level ground truth. These are prediction rates under shift, not accuracy.
