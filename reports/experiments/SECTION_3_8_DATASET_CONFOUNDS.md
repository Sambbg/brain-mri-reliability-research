# §3.8 Dataset-Intrinsic Confounds in the Internal Benchmark

*New subsection, placed after §3.7 (Simpson's paradox and seed sensitivity) and
before the integrated interpretation, which becomes §3.9.*

*All values from `experiments/clever_hans/` and the D1 manifests. Wilson 95%
intervals throughout, computed over fixed denominators.*

---

## 3.8 Dataset-Intrinsic Confounds in the Internal Benchmark

The results reported so far treat internal macro-F1 as a measurement whose
reproducibility is in question but whose meaning is not. This section examines the
measurement itself. Two properties of the internal dataset are reported: the extent to
which its class labels are predictable from features that cannot encode tumour
appearance, and the extent to which one of its four classes is separable from the others
on acquisition properties alone. Both bear directly on the interpretation of every
internal figure in this study, and the second offers a candidate mechanism for the
shifted-domain behaviour reported in Section 3.4.

### 3.8.1 Class labels are partly predictable without tumour information

Wallis and Buvat [9] showed that high classification accuracy is achievable on a widely
used brain tumour MRI dataset using no information about the tumour itself, arising from
implicit radiologist input in two-dimensional slice selection. Because the internal
dataset used here derives from the same benchmark family, that finding was replicated
directly on the leakage-aware split.

Four features were extracted from each image: the count of exactly-zero pixels, the
maximum intensity, and the aspect ratio and fill fraction of the bounding box enclosing
the non-zero region. None encodes tumour appearance, location or morphology. The first
two describe how much of the frame is empty and how the image was encoded; the latter two
describe the outline of the imaged region, which is a property of framing and acquisition
geometry rather than of pathology. The strict three-feature replication drops the fill
fraction. A decision tree and a logistic regression were fitted on the training partition
and scored on the validation and test partitions. Following the source study, the
principal analysis is restricted to the three tumour classes, since the no-tumour class
is treated separately in Section 3.8.2.

| Feature set | Validation accuracy (95% CI) | Test accuracy (95% CI) |
|---|---|---|
| Three features (strict replication) | 0.6454 (0.6117, 0.6778) | 0.6737 (0.6405, 0.7053) |
| Four features | 0.6579 (0.6244, 0.6900) | 0.6825 (0.6494, 0.7138) |
| Image dimensions only | 0.3483 (0.3161, 0.3820) | 0.3463 (0.3141, 0.3799) |
| Chance floor (majority class) | 0.3358 (0.3040, 0.3693) | 0.3362 (0.3044, 0.3697) |

**Table 12.** Three-class accuracy from features that cannot encode tumour appearance
(n = 801 validation, 800 test). Wilson 95% intervals over fixed denominators.

The strict three-feature replication reaches 0.6737 (0.6405, 0.7053) on the test
partition against a chance floor whose upper bound is 0.3697 — the nearest bounds are
separated by 0.27. Validation and test agree as intervals rather than by assertion: every
feature set's two intervals overlap substantially, and the largest point difference is
0.0283 against interval widths of approximately 0.065.

This is a smaller effect than the source study reports, closing roughly 54% of the
chance-to-ceiling gap against their 81%. The fitted tree splits predominantly on the
count of exactly-zero pixels — 18 of its 30 splits, including the root — that is on
background extent, which is a property of how the slice was framed. Bounding-box fill
fraction accounts for a further 10 splits and aspect ratio for 2. Maximum intensity is
never used as a split, because the re-encoding applied when this benchmark was compiled
saturated it.

The implication is bounded but material. It does not show that the trained networks use
these features, and a tree reaching 0.67 does not explain a network reaching 0.97. It
shows that a substantial share of the label information in this benchmark is carried by
properties that are not the pathology, so internal accuracy on it overstates
tumour-recognition ability by an amount this study cannot quantify. That is a statement
about the benchmark rather than about the architectures, and it applies equally to every
published result on the same data.

### 3.8.2 The no-tumour class has different provenance

A second and distinct property emerged from the same analysis. Where the three-class
result above uses features describing image content, the control condition used image
dimensions alone — width and height, with no pixel information whatsoever.

| Label scope | Dimensions-only accuracy (95% CI) | Chance floor (95% CI) |
|---|---|---|
| Three tumour classes | 0.3463 (0.3141, 0.3799) | 0.3362 (0.3044, 0.3697) |
| All four classes | 0.4548 (0.4249, 0.4850) | 0.2559 (0.2305, 0.2832) |

**Table 13.** Accuracy from image dimensions alone (n = 800 and 1,051 test). Wilson 95%
intervals.

Among the three tumour classes, image dimensions carry no information: the interval
(0.3141, 0.3799) sits almost entirely inside the chance interval (0.3044, 0.3697). Adding
the no-tumour class changes this completely — 0.4548 (0.4249, 0.4850) against a floor of
0.2559 (0.2305, 0.2832), with the nearest bounds 0.14 apart. Image dimensions are
uninformative until the no-tumour class enters, at which point they become substantially
predictive.

Three independent signals establish that this class differs from the others in how its
files were produced.

**Geometry.** 96.4% of glioma, 86.3% of meningioma and 96.7% of pituitary images are
512×512 pixels, against 1.0% of no-tumour images. The tumour classes span 27 to 126
distinct image sizes; the no-tumour class spans 250.

**Encoder signature.** JPEG quantisation tables record which encoder and quality setting
a file last passed through and survive renaming, which matters here because the benchmark
rewrites all filenames to a uniform scheme. The three tumour classes carry two to four
distinct quantisation tables each. The no-tumour class carries fifty. Its dominant table
appears in no non-augmented tumour image.

**Persistence across compilations.** The candidate external dataset rejected in Section
3.1 was compiled independently from the same public source. Matching by perceptual hash,
so that re-encoded copies still count, 98.2% of its glioma images, 97.7% of its
meningioma images and 100.0% of its pituitary images also appear in the internal dataset
— against 4.4% of its no-tumour images. The three tumour classes constitute a stable
corpus that travels between independently assembled compilations. The no-tumour images do
not.

The three signals agree and none depends on documentation. The compiler of this benchmark
describes the tumour classes as drawn from two upstream collections and the no-tumour
class from a third; that attribution is consistent with what is measured here but was not
independently verified in this study, and none of the claims above rests on it. What is
established is that the no-tumour class was sourced differently and is separable from the
tumour classes on acquisition properties alone.

### 3.8.3 A candidate mechanism for the shifted-domain result, and its limits

Section 3.4 reported that misassigned human glioma slices concentrate in the no-tumour
class, from 0.271 ± 0.066 for ResNet18 to 0.628 ± 0.169 for ViT-B/16, and that the
between-architecture difference cannot be attributed to slice selection because all
architectures were evaluated on identical slices. Section 3.8.2 establishes that the
no-tumour class is the one class in the internal dataset separable on acquisition
properties alone.

These two observations suggest a mechanism. If part of what a model learns about the
no-tumour class is the acquisition signature of the files that carry that label rather
than the absence of pathology, then the corresponding decision region is defined partly
by properties that no external cohort shares. Under shift, where those properties are
absent or scrambled, that region would become permissive, and images the model cannot
otherwise place would be drawn into it. The architecture-dependent magnitude would then
reflect how heavily each architecture relies on the acquisition cue rather than on
pathology.

**This is a hypothesis the present evidence supports but does not establish.** What has
been measured is that the no-tumour class is separable on acquisition properties. What has
not been shown is that the trained networks use that separability, or that it drives the
behaviour observed on the human probe. A competing explanation is available and is not
excluded by anything reported here: the no-tumour class may simply be the default
destination for low-confidence predictions under distribution shift, in which case the
concentration would occur whatever the class's provenance.

Two experiments would separate these accounts, and neither was performed. Retraining with
the no-tumour class resampled to match the tumour classes' size and encoder distribution
would remove the acquisition cue while preserving the label; if the shifted-domain
no-tumour share falls, the cue is implicated. Alternatively, sourcing a no-tumour set
from the same corpus as the tumour classes would achieve the same test by construction.
Attribution analysis on misassigned probe slices would provide weaker but cheaper
evidence about which image regions drive the assignment. All three are recorded as future
work.

The result is reported here despite being incomplete because it qualifies the
interpretation of every internal figure in this study, and because the direction of the
qualification is not favourable to the study's own numbers. The internal performance
reported in Section 3.2 is measured on a benchmark in which a substantial share of label
information is carried by properties that are not the pathology, and in which one class is
distinguishable from the others without reference to image content at all.

---

## Methods footnote (for §2.9 or §2.12)

> A further ablation binarised the internal test images at a fixed intensity threshold,
> retaining a skull outline and discarding internal structure, and evaluated all fifteen
> checkpoints without retraining. Accuracy fell below the chance floor for twelve of
> fifteen checkpoints, with entire 95% intervals lying beneath it for two of the three
> architectures. A model retaining usable signal cannot score below the accuracy obtained
> by always predicting the largest class, so this condition measures the effect of severe
> distribution shift on models trained on unmodified images rather than the information
> content of a skull outline. The ablation is therefore reported as uninformative and no
> conclusion is drawn from it. Establishing what a skull outline supports would require
> training on binarised images, which was not performed.

---

## Notes on this draft

**Placement.** After the Simpson's paradox section and before the integrated
interpretation. It qualifies the internal measurement, so it needs to precede the
synthesis rather than follow it. The existing §3.8 becomes §3.9.

**Two new tables**, numbered 12 and 13 following the existing eleven.

**Framing of the attribution.** The named upstream sources appear once, described as
the compiler's account, explicitly marked unverified, and load-bearing on nothing. Every
claim rests on measurement. This follows the same discipline applied to the
skull-stripping question in §2.5.

**The ablation is excluded from Results** and appears only as a methods footnote. A model
scoring below the majority-class floor is measuring distribution shift, and presenting it
otherwise would be the kind of over-reading this paper argues against.

**Reference [9]** is Wallis and Buvat (2022), already in the reference list.

**What this adds to the paper.** It converts a limitation into a finding, and gives §3.4
a candidate mechanism it previously lacked. It also strengthens the central argument:
internal accuracy on this benchmark is not only irreproducible across seeds but partly
measures something other than pathology.

**Abstract.** Consider one sentence: *"A metadata-only classifier using features that
cannot encode tumour appearance reached 0.674 (0.641, 0.705) on the three tumour classes
against a chance floor of 0.336, and the no-tumour class proved separable from the tumour
classes on image dimensions alone."* It is a strong finding and currently invisible above
the fold.
