# Abstract ? rewritten against run set `2026-08-sweep-a`

---

## Version A ? thesis abstract (~300 words)

Deep learning models for brain MRI tumour classification routinely report internal test
accuracies above 98% on public benchmark datasets, and these figures are commonly used to
compare architectures. This study evaluated whether such internal performance is
reproducible enough to support that comparison, and whether it predicts behaviour under
dataset shift. Three architectures ? ResNet18, EfficientNet-B0, and ViT-B/16 ? were each
trained at five random seeds on an identical leakage-aware split of a public four-class
brain MRI dataset, giving fifteen runs. The split was constructed after exact-duplicate
removal and perceptual near-duplicate grouping, which detected 1,926 near-duplicate pairs
crossing the distributed train/test boundary. Candidate external datasets were audited for
overlap; one was rejected after 4,740 of its 5,950 images proved byte-identical to the
training data. Two glioma-focused shifted-domain probes were retained: a cross-species
canine collection (53 patients, 265 slices) and a same-species human adult-glioblastoma
collection (610 patients, 3,050 slices). Internal test macro-F1 was high but did not
reliably rank the architectures: the spread between architecture means (0.0116) was only
2.52 times the mean within-architecture standard deviation across seeds (0.0046), the two
best models differed by 0.0011, and the ordering changed between seeds. The same-species
probe separated the architectures consistently, with glioma prediction rates of
0.674 ± 0.073, 0.514 ± 0.065 and 0.264 ± 0.114 and one architecture ranked first at every
seed. Misassigned human glioma slices went predominantly to the no-tumour class, and
confidence was inversely related to glioma recognition: the architecture least able to
recognise human glioma was the most confident at every seed. The association between
internal performance and shifted-domain behaviour was positive between architectures
(+0.886) but negative within them (?0.514). Temperature scaling improved every internal
calibration metric but changed no prediction on either probe. Internal accuracy on this
benchmark is therefore insufficient evidence of reliability, and at this level of
performance it does not distinguish architectures against seed variation.

---

## Version B ? journal abstract, structured (~250 words)

**Background.** Brain MRI tumour classification studies routinely report internal test
accuracies above 98% on a small number of public benchmarks, and use these figures to
compare architectures. Such comparisons are almost always based on a single training run.

**Methods.** Three architectures (ResNet18, EfficientNet-B0, ViT-B/16) were each trained
at five random seeds on an identical leakage-aware split of a public four-class brain MRI
dataset, giving fifteen runs. The split was constructed after exact and perceptual
duplicate auditing. Candidate external datasets were audited for overlap against the
training data. Behaviour under shift was assessed on two glioma-focused probes: a
cross-species canine collection (53 patients) and a same-species human adult-glioblastoma
collection (610 patients). Calibration was assessed with expected calibration error,
negative log-likelihood, Brier score and the confidence?accuracy gap, before and after
post-hoc temperature scaling.

**Results.** Internal test macro-F1 spanned 0.9557?0.9673 but did not reliably rank the
architectures: the between-architecture spread (0.0116) was 2.52 times the mean seed-induced
standard deviation (0.0046), the two best models differed by 0.0011, and the ordering
changed across seeds. The same-species probe separated the architectures at a
signal-to-noise ratio of 4.91, with glioma prediction rates of 0.674 ± 0.073, 0.514 ± 0.065
and 0.264 ± 0.114 and one architecture first at all five seeds. Misassigned glioma slices
concentrated in the no-tumour class (0.271?0.628), and the least glioma-recognising
architecture was the most confident at every seed. Internal performance correlated
positively with shift behaviour between architectures (+0.886) and negatively within them
(?0.514). One candidate external dataset was rejected after 4,740 of 5,950 images proved
byte-identical to the training data.

**Conclusions.** Single-run internal accuracy on this benchmark does not distinguish these
architectures against seed variation and does not predict behaviour under shift. Reliability
claims require repeated runs with dispersion, overlap auditing, and shifted-domain
evaluation reported jointly.

---

## Keywords

brain MRI; tumour classification; reliability; dataset shift; calibration; data leakage;
seed variance; underspecification; external validation

---

## What changed from the previous abstract

| Previous | Corrected |
|---|---|
| macro-F1 "0.9666?0.9680" for all three models | ViT-B/16 is 0.9557; range is 0.9557?0.9673 |
| D3C "2,845 central slices from 569 patients" | 3,050 slices from 610 patients |
| Glioma rates "29.4%, 44.2%, 40.4%" (D3B) and "69.4%, 46.3%, 21.8%" (D3C) | Seed means with SD; the single-seed figures are withdrawn |
| "reversing the model ordering between probes" | No reversal; ordering is the same on both probes |
| "ViT-B/16 ... was the most confident (0.91; median glioma probability 0.004)" | Holds directionally, but as a seed mean: confidence 0.860 ± 0.039, median glioma probability 0.102 ± 0.156 |
| Framed as: high internal performance is insufficient evidence of reliability | Framed as: internal performance does not even rank these architectures reproducibly, *and* is insufficient evidence of reliability |

The previous abstract made no mention of seeds, reported every figure as a point estimate,
and led with a finding that did not survive. The corrected version leads with the
reproducibility result, which is both better evidenced and more directly useful to the
literature it addresses.
