# Variance decomposition of the architecture comparison

The manuscript reports a signal-to-noise ratio, defined as the
between-architecture spread divided by the mean within-architecture standard
deviation across seeds. That quantity is defined by this study and has no
distributional theory behind it, so a reader cannot judge whether 2.52 is
small without accepting the manuscript's interpretation.

The design is balanced: three architectures, five seeds, every seed appearing
once with every architecture. That is a randomised complete block design with
architecture as the treatment and seed as the block, and it admits an exact
classical analysis. Blocking on seed is what makes this correct rather than a
one-way ANOVA: the same five seeds are used for every architecture, so runs
are paired across architectures.

    y_ij = mu + alpha_i + b_j + e_ij,   b_j ~ N(0, s_b^2),  e_ij ~ N(0, s_e^2)

## Summary

| Evaluation | F (arch) | df | p | partial eta^2 | omega^2 | Manuscript SNR |
|---|---|---|---|---|---|---|
| Internal test macro-F1 | 6.23 | 2,8 | 0.0234 | 0.609 | 0.464 | 2.52 |
| D3B glioma assignment rate (canine, n = 53) | 2.12 | 2,8 | 0.1830 | 0.346 | 0.145 | 1.40 |
| D3C glioma assignment rate (human, n = 610) | 30.38 | 2,8 | 0.0002 | 0.884 | 0.789 | 4.91 |

## Variance components

Estimated from expected mean squares. The seed component is the variance
attributable to the random seed, shared across architectures within a run.

| Evaluation | Seed variance | Residual variance | Seed share | Residual share |
|---|---|---|---|---|
| Internal test macro-F1 | 0.000e+00 | 3.313e-05 | 0.0% | 100.0% |
| D3B glioma assignment rate (canine, n = 53) | 0.000e+00 | 1.530e-02 | 0.0% | 100.0% |
| D3C glioma assignment rate (human, n = 610) | 4.222e-04 | 7.057e-03 | 5.6% | 94.4% |

## Internal test macro-F1

### ANOVA table

| Source | SS | df | MS | F | p |
|---|---|---|---|---|---|
| Architecture | 4.12835e-04 | 2 | 2.06417e-04 | 6.230 | 0.0234 |
| Seed (block) | 3.50812e-05 | 4 | 8.77029e-06 | 0.265 | 0.8926 |
| Residual | 2.65074e-04 | 8 | 3.31342e-05 | | |
| Total | 7.12989e-04 | 14 | | | |

### Pairwise contrasts

| Comparison | Difference | 95% CI | t | p raw | p Holm |
|---|---|---|---|---|---|
| ResNet18 - EfficientNet-B0 | -0.0011 | [-0.0095, +0.0073] | -0.30 | 0.7748 | 0.7748 |
| ResNet18 - ViT-B/16 | +0.0106 | [+0.0022, +0.0189] | +2.90 | 0.0199 | 0.0399 * |
| EfficientNet-B0 - ViT-B/16 | +0.0116 | [+0.0032, +0.0200] | +3.19 | 0.0127 | 0.0382 * |

Not separated after correction: ResNet18 vs EfficientNet-B0.

## D3B glioma assignment rate (canine, n = 53)

### ANOVA table

| Source | SS | df | MS | F | p |
|---|---|---|---|---|---|
| Architecture | 6.47424e-02 | 2 | 3.23712e-02 | 2.116 | 0.1830 |
| Seed (block) | 3.30120e-02 | 4 | 8.25300e-03 | 0.539 | 0.7117 |
| Residual | 1.22408e-01 | 8 | 1.53011e-02 | | |
| Total | 2.20163e-01 | 14 | | | |

### Pairwise contrasts

| Comparison | Difference | 95% CI | t | p raw | p Holm |
|---|---|---|---|---|---|
| ResNet18 - EfficientNet-B0 | +0.0340 | [-0.1464, +0.2144] | +0.43 | 0.6757 | 0.6757 |
| ResNet18 - ViT-B/16 | +0.1532 | [-0.0272, +0.3336] | +1.96 | 0.0859 | 0.2576 |
| EfficientNet-B0 - ViT-B/16 | +0.1192 | [-0.0612, +0.2997] | +1.52 | 0.1660 | 0.3319 |

Not separated after correction: ResNet18 vs EfficientNet-B0; ResNet18 vs ViT-B/16; EfficientNet-B0 vs ViT-B/16.

## D3C glioma assignment rate (human, n = 610)

### ANOVA table

| Source | SS | df | MS | F | p |
|---|---|---|---|---|---|
| Architecture | 4.28773e-01 | 2 | 2.14386e-01 | 30.379 | 0.0002 |
| Seed (block) | 3.32942e-02 | 4 | 8.32356e-03 | 1.179 | 0.3889 |
| Residual | 5.64565e-02 | 8 | 7.05706e-03 | | |
| Total | 5.18523e-01 | 14 | | | |

### Pairwise contrasts

| Comparison | Difference | 95% CI | t | p raw | p Holm |
|---|---|---|---|---|---|
| ResNet18 - EfficientNet-B0 | +0.1606 | [+0.0381, +0.2831] | +3.02 | 0.0165 | 0.0165 * |
| ResNet18 - ViT-B/16 | +0.4109 | [+0.2884, +0.5334] | +7.73 | 0.0001 | 0.0002 * |
| EfficientNet-B0 - ViT-B/16 | +0.2503 | [+0.1278, +0.3728] | +4.71 | 0.0015 | 0.0030 * |

All pairwise differences remain significant after Holm correction.

## Relation to the reported signal-to-noise ratio

| Evaluation | Spread | Mean seed SD | SNR | F | p |
|---|---|---|---|---|---|
| Internal test macro-F1 | 0.0116 | 0.0046 | 2.52 | 6.23 | 0.0234 |
| D3B glioma assignment rate (canine, n = 53) | 0.1532 | 0.1093 | 1.40 | 2.12 | 0.1830 |
| D3C glioma assignment rate (human, n = 610) | 0.4109 | 0.0837 | 4.91 | 30.38 | 0.0002 |

The two quantities measure related things but are not interchangeable. The
signal-to-noise ratio compares the spread of architecture means against the
average scatter within an architecture; the F statistic compares the same
spread against residual variation after removing the seed effect, which is
the correct denominator for a blocked design. Where the seed effect is large,
the F test has more power than the ratio suggests, because blocking removes
that variation from the error term.

Recommendation: report the F test, its p value and the pairwise contrasts as
the primary analysis, and retain the signal-to-noise ratio only as a
descriptive summary with its definition stated. That answers the objection
that the ratio and its threshold are defined by this study.

