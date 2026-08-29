# Figure captions

Error bars and axis choices are stated explicitly. Reviewers routinely
query figures where these are left undefined.

**Figure 1.** System architecture of the reliability-first evaluation
framework. Datasets are prepared and audited for contamination against the
internal dataset D1; a candidate failing the audit is excluded from any
external-validation role. Three architectures are trained on the fixed
leakage-aware split at five seeds each, and evaluation proceeds across
internal, calibration and shifted-domain layers.

**Figure 2.** Internal test macro-F1 for each of the 15 runs, grouped by
architecture. Points are individual runs with horizontal jitter applied for
visibility; horizontal bars are architecture means and shaded bands span
±1 standard deviation across the 5 seeds. **The vertical axis is
truncated to 0.948-0.978** to resolve differences that are small in absolute
terms; this truncation is the point of the figure, since the between-
architecture spread is only 2.52 times the mean within-architecture standard
deviation.

**Figure 3.** Reliability diagrams on the internal test partition, pooled
across 5 seeds per architecture and weighted by bin count. Solid lines
with filled markers are raw probabilities; dashed lines with open markers are
temperature-scaled. The diagonal indicates perfect calibration. Bins
containing fewer than five predictions are omitted.

**Figure 4.** Internal test macro-F1 and shifted-domain glioma prediction
rate for the three architectures. Bars are means across 5 seeds and error
bars are ±1 standard deviation. The signal-to-noise ratio above each group is
the between-architecture spread divided by the mean within-architecture
standard deviation (equation 10); values near or below 2 indicate that the
evaluation does not resolve the architectures against seed variation.

**Figure 5.** Distribution of predicted classes on the two shifted-domain
probes. Bars are means across 5 seeds and error bars are ±1 standard
deviation. All architectures were evaluated on identical slices, so
between-architecture differences reflect learned behaviour rather than slice
selection.

**Figure 6.** Human-probe glioma prediction rate against mean maximum
confidence for each of the 15 runs. Small markers are individual runs;
large outlined markers are architecture means. The dotted line is the
least-squares fit pooled across all runs. Confidence increases as glioma
recognition falls.

**Figure 7.** Internal test macro-F1 against shifted-domain glioma prediction
rate for the 15 runs. Coloured lines are within-architecture least-squares
fits; the dashed black line is the fit through the three architecture means,
shown as large open circles. On the human probe (a) the between-architecture
association is positive while the within-architecture association is negative,
a Simpson’s paradox. On the canine probe (b) both are positive.

