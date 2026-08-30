# D1 Clever Hans probe - metadata-only feature classifier

Replication of experiment 5 of Wallis & Buvat (2022, *Medical Image Analysis* 77:102368) on the D1 leakage-aware split. A trivial classifier is fitted on features that cannot encode tumour appearance, trained on the train split and scored on val and test. No CNN is involved and nothing is retrained.

## Provenance

| Field | Value |
|---|---|
| Analysis commit | `b72aa7708afc34b88d884950412816e2bb669205` |
| Split csv sha256 | `944ce00e4be958f3688a0996f6fb928fc7717e7c2804abb8000f28976efe0d43` |
| Mask threshold | 100 |
| Decision tree max depth | 4 |
| random_state | 0 |
| Images with an empty tissue mask | 0 |

## Feature sets

| Name | Features | Purpose |
|---|---|---|
| `wallis_4` | `n_zero`, `max_intensity`, `bbox_aspect`, `bbox_fill` | Primary. The orientation proxy is two features, so this is four not three. |
| `wallis_3_strict` | `n_zero`, `max_intensity`, `bbox_aspect` | Exact three-feature replication: primary minus bbox_fill. |
| `frac_zero_sensitivity` | `frac_zero`, `max_intensity`, `bbox_aspect`, `bbox_fill` | n_zero replaced by its fraction, removing image-size confounding. |
| `shape_only` | `bbox_aspect`, `bbox_fill` | Orientation proxy alone, without the intensity features. |
| `geometry_control` | `width`, `height` | Image dimensions alone. Separates source-of-file bias from slice-selection bias. |

## CNN comparator

Test-split accuracy of the trained models, mean +/- SD over seeds 42-46. This is what the trivial classifier is being measured against.

| Model | Four-class | Three-class |
|---|---:|---:|
| E001 | 0.9661 +/- 0.0073 | 0.9720 +/- 0.0106 |
| E002 | 0.9671 +/- 0.0044 | 0.9732 +/- 0.0037 |
| E003 | 0.9555 +/- 0.0026 | 0.9637 +/- 0.0029 |

## Four classes (all of D1)

Majority-class floor: 0.2559 (0.2305, 0.2832) on test, 0.2555 (0.2300, 0.2827) on val. A classifier whose interval overlaps the floor's has not been shown to beat chance.

Accuracies carry 95% Wilson intervals. Each is a proportion of correct predictions over a fixed denominator, so the interval is exact for that quantity and needs no resampling. Val and test are shown side by side so their agreement is visible as overlapping intervals rather than asserted.

| Feature set | Classifier | Val acc (95% CI) | Test acc (95% CI) | Test macro-F1 |
|---|---|---|---|---:|
| `wallis_4` | decision_tree | 0.6306 (0.6010, 0.6592) | 0.6118 (0.5820, 0.6408) | 0.6157 |
| `wallis_4` | logistic_regression | 0.5679 (0.5378, 0.5975) | 0.5480 (0.5178, 0.5779) | 0.5456 |
| `wallis_3_strict` | decision_tree | 0.5062 (0.4760, 0.5363) | 0.5186 (0.4883, 0.5486) | 0.5053 |
| `wallis_3_strict` | logistic_regression | 0.4255 (0.3959, 0.4555) | 0.4434 (0.4136, 0.4736) | 0.4166 |
| `frac_zero_sensitivity` | decision_tree | 0.6448 (0.6154, 0.6732) | 0.6327 (0.6032, 0.6613) | 0.6183 |
| `frac_zero_sensitivity` | logistic_regression | 0.5394 (0.5092, 0.5693) | 0.5309 (0.5007, 0.5609) | 0.5249 |
| `shape_only` | decision_tree | 0.5299 (0.4997, 0.5599) | 0.5224 (0.4921, 0.5524) | 0.5087 |
| `shape_only` | logistic_regression | 0.4843 (0.4543, 0.5145) | 0.4843 (0.4542, 0.5145) | 0.4821 |
| `geometry_control` | decision_tree | 0.4568 (0.4269, 0.4870) | 0.4548 (0.4249, 0.4850) | 0.3559 |
| `geometry_control` | logistic_regression | 0.4274 (0.3978, 0.4574) | 0.4329 (0.4033, 0.4631) | 0.3364 |

### Per-class recall on test, primary feature set, decision tree

| Class | Recall |
|---|---:|
| glioma | 0.4535 |
| meningioma | 0.5281 |
| notumor | 0.7211 |
| pituitary | 0.7538 |

### Fitted tree

The splits are the evidence. A tree that separates classes on background extent or head shape is reading acquisition and selection, not pathology.

```
|--- bbox_fill <= 0.25
|   |--- n_zero <= 56078.00
|   |   |--- n_zero <= 26590.50
|   |   |   |--- n_zero <= 19595.00
|   |   |   |   |--- class: 3
|   |   |   |--- n_zero >  19595.00
|   |   |   |   |--- class: 3
|   |   |--- n_zero >  26590.50
|   |   |   |--- bbox_fill <= 0.08
|   |   |   |   |--- class: 2
|   |   |   |--- bbox_fill >  0.08
|   |   |   |   |--- class: 1
|   |--- n_zero >  56078.00
|   |   |--- bbox_fill <= 0.10
|   |   |   |--- n_zero <= 78994.50
|   |   |   |   |--- class: 0
|   |   |   |--- n_zero >  78994.50
|   |   |   |   |--- class: 0
|   |   |--- bbox_fill >  0.10
|   |   |   |--- n_zero <= 65721.50
|   |   |   |   |--- class: 0
|   |   |   |--- n_zero >  65721.50
|   |   |   |   |--- class: 1
|--- bbox_fill >  0.25
|   |--- bbox_aspect <= 1.15
|   |   |--- n_zero <= 45478.00
|   |   |   |--- n_zero <= 4236.50
|   |   |   |   |--- class: 2
|   |   |   |--- n_zero >  4236.50
|   |   |   |   |--- class: 2
|   |   |--- n_zero >  45478.00
|   |   |   |--- n_zero <= 76662.50
|   |   |   |   |--- class: 1
|   |   |   |--- n_zero >  76662.50
|   |   |   |   |--- class: 2
|   |--- bbox_aspect >  1.15
|   |   |--- n_zero <= 34417.50
|   |   |   |--- bbox_aspect <= 1.25
|   |   |   |   |--- class: 2
|   |   |   |--- bbox_aspect >  1.25
|   |   |   |   |--- class: 2
|   |   |--- n_zero >  34417.50
|   |   |   |--- bbox_fill <= 0.35
|   |   |   |   |--- class: 1
|   |   |   |--- bbox_fill >  0.35
|   |   |   |   |--- class: 2
```

## Three Figshare-derived classes, refitted

notumor is dropped from both training and evaluation here, so this classifier is genuinely three-way. This is the faithful comparison with Wallis & Buvat, who reported 0.77 on Figshare.

Majority-class floor: 0.3362 (0.3044, 0.3697) on test, 0.3358 (0.3040, 0.3693) on val. A classifier whose interval overlaps the floor's has not been shown to beat chance.

Accuracies carry 95% Wilson intervals. Each is a proportion of correct predictions over a fixed denominator, so the interval is exact for that quantity and needs no resampling. Val and test are shown side by side so their agreement is visible as overlapping intervals rather than asserted.

| Feature set | Classifier | Val acc (95% CI) | Test acc (95% CI) | Test macro-F1 |
|---|---|---|---|---:|
| `wallis_4` | decision_tree | 0.6579 (0.6244, 0.6900) | 0.6825 (0.6494, 0.7138) | 0.6861 |
| `wallis_4` | logistic_regression | 0.5693 (0.5347, 0.6032) | 0.5575 (0.5229, 0.5916) | 0.5546 |
| `wallis_3_strict` | decision_tree | 0.6454 (0.6117, 0.6778) | 0.6737 (0.6405, 0.7053) | 0.6766 |
| `wallis_3_strict` | logistic_regression | 0.4744 (0.4400, 0.5090) | 0.5088 (0.4741, 0.5433) | 0.5027 |
| `frac_zero_sensitivity` | decision_tree | 0.6866 (0.6537, 0.7178) | 0.6700 (0.6367, 0.7017) | 0.6684 |
| `frac_zero_sensitivity` | logistic_regression | 0.5718 (0.5373, 0.6056) | 0.5575 (0.5229, 0.5916) | 0.5543 |
| `shape_only` | decision_tree | 0.5194 (0.4847, 0.5538) | 0.5138 (0.4791, 0.5482) | 0.5078 |
| `shape_only` | logistic_regression | 0.4906 (0.4561, 0.5252) | 0.4925 (0.4580, 0.5271) | 0.4917 |
| `geometry_control` | decision_tree | 0.3483 (0.3161, 0.3820) | 0.3463 (0.3141, 0.3799) | 0.2089 |
| `geometry_control` | logistic_regression | 0.3308 (0.2991, 0.3642) | 0.3325 (0.3007, 0.3659) | 0.1859 |

### Per-class recall on test, primary feature set, decision tree

| Class | Recall |
|---|---:|
| glioma | 0.5428 |
| meningioma | 0.7603 |
| pituitary | 0.7462 |

### Fitted tree

The splits are the evidence. A tree that separates classes on background extent or head shape is reading acquisition and selection, not pathology.

```
|--- n_zero <= 55508.00
|   |--- n_zero <= 25563.00
|   |   |--- n_zero <= 19967.50
|   |   |   |--- n_zero <= 6294.00
|   |   |   |   |--- class: 3
|   |   |   |--- n_zero >  6294.00
|   |   |   |   |--- class: 1
|   |   |--- n_zero >  19967.50
|   |   |   |--- bbox_fill <= 0.37
|   |   |   |   |--- class: 3
|   |   |   |--- bbox_fill >  0.37
|   |   |   |   |--- class: 1
|   |--- n_zero >  25563.00
|   |   |--- bbox_fill <= 0.08
|   |   |   |--- bbox_fill <= 0.06
|   |   |   |   |--- class: 3
|   |   |   |--- bbox_fill >  0.06
|   |   |   |   |--- class: 0
|   |   |--- bbox_fill >  0.08
|   |   |   |--- bbox_aspect <= 1.25
|   |   |   |   |--- class: 1
|   |   |   |--- bbox_aspect >  1.25
|   |   |   |   |--- class: 1
|--- n_zero >  55508.00
|   |--- bbox_fill <= 0.12
|   |   |--- n_zero <= 79008.00
|   |   |   |--- n_zero <= 70018.50
|   |   |   |   |--- class: 0
|   |   |   |--- n_zero >  70018.50
|   |   |   |   |--- class: 1
|   |   |--- n_zero >  79008.00
|   |   |   |--- n_zero <= 115035.00
|   |   |   |   |--- class: 0
|   |   |   |--- n_zero >  115035.00
|   |   |   |   |--- class: 1
|   |--- bbox_fill >  0.12
|   |   |--- n_zero <= 64908.50
|   |   |   |--- bbox_fill <= 0.27
|   |   |   |   |--- class: 0
|   |   |   |--- bbox_fill >  0.27
|   |   |   |   |--- class: 1
|   |   |--- n_zero >  64908.50
|   |   |   |--- n_zero <= 76954.00
|   |   |   |   |--- class: 1
|   |   |   |--- n_zero >  76954.00
|   |   |   |   |--- class: 0
```

## Feature distributions by class

Median [min, max] over the whole split file.

| Class | n_zero | max_intensity | bbox_aspect | bbox_fill |
|---|---:|---:|---:|---:|
| glioma | 6.02e+04 [0, 1.54e+05] | 255 [208, 255] | 1.15 [0.669, 1.53] | 0.111 [0.00537, 0.69] |
| meningioma | 4.2e+04 [0, 2.32e+05] | 255 [181, 255] | 1.13 [0.632, 1.87] | 0.172 [0.0202, 0.746] |
| notumor | 6.99e+03 [0, 4.15e+05] | 255 [130, 255] | 1.21 [0.735, 1.59] | 0.377 [0.0106, 0.801] |
| pituitary | 7.99e+03 [0, 8.41e+04] | 255 [234, 255] | 1.09 [0.72, 1.42] | 0.13 [0.00855, 0.532] |

## Image dimensions by class

The evidence behind the geometry control, and behind the source-class reading below. Dimensions are a property of how a file was produced, not of the anatomy inside it.

| Class | n | 512x512 | Distinct sizes | Most common size |
|---|---:|---:|---:|---|
| glioma | 1786 | 1721 (96.4%) | 62 | 512x512 (96.4%) |
| meningioma | 1784 | 1540 (86.3%) | 126 | 512x512 (86.3%) |
| notumor | 1681 | 16 (1.0%) | 250 | 225x225 (18.1%) |
| pituitary | 1762 | 1703 (96.7%) | 27 | 512x512 (96.7%) |

## A source-class confound, and what it may explain

The geometry control is the strongest single result on this page, and it is worth stating plainly what it shows. Image width and height carry no anatomy whatsoever. On the three tumour classes they classify at 0.3463 (0.3141, 0.3799), an interval that contains the chance floor of 0.3362. On all four classes the same two numbers reach 0.4548 (0.4249, 0.4850) against a floor of 0.2559, and the two intervals are far apart. The entire gain comes from the notumor class.

The measured fact is the size distribution itself, tabulated immediately above: the three tumour classes are overwhelmingly 512x512 while notumor spans many smaller sizes. Whatever produced it, **notumor in D1 is separable from the tumour classes on acquisition-level properties that carry no anatomy**, and a classifier is free to use that instead of pathology.

The section below tests, against files already on disk, whether that separation reflects a difference in provenance. It does: three independent signals agree that the notumor class did not arrive with the tumour classes.

That raises a hypothesis for a result reported elsewhere in this project. On the human glioma probe (D3C), the dominant destination for misassigned slices is the no-tumour class, and it rises steeply across architectures:

| Model | D3C slices predicted notumor |
|---|---:|
| E001 | 0.2706 +/- 0.0660 |
| E002 | 0.4162 +/- 0.0987 |
| E003 | 0.6275 +/- 0.1689 |

If a model has partly learned notumor as *images that look like they came from Br35H* rather than *images with no tumour*, then any out-of-distribution image is a candidate for that class, because the discriminating cue is acquisition provenance rather than pathology. D3C slices are CaPTk-processed, co-registered and resampled, so they resemble neither source. Under that reading, the no-tumour class acts as a residual bin for unfamiliar acquisitions, and the glioma-recognition failure on D3C is partly a dataset-construction artefact rather than purely a failure to generalise tumour appearance.

**This is a hypothesis the geometry control supports, not one it proves.** What is established is that notumor is separable from the tumour classes on image dimensions alone, which is a property of D1's construction. What is not established is that the models actually use that cue, nor that it is what drives the D3C behaviour: the ordering of the notumor share across architectures is not predicted by anything measured here, and an equally consistent explanation is that no-tumour is simply the lowest-confidence default under shift. Distinguishing them needs a direct test -- for instance retraining with the notumor class resampled to match the tumour classes' size distribution, or sourcing a no-tumour set from Figshare itself, and checking whether the D3C no-tumour share moves.

## Provenance evidence from files on disk

The source composition above is a claim from a dataset description. It can be tested directly, without re-downloading anything, and the tests below do not depend on that description being accurate.

### JPEG encoder signatures

The quantisation table records which encoder and quality setting a JPEG last passed through. It survives renaming, so it says something about a file's history that the filename does not. A class re-encoded wholesale by one pipeline shows very few tables; a class assembled from heterogeneous originals shows many, including tables occurring only once or twice in all of D1.

| Class | n | Distinct tables | Modal table (share) | Images with a table seen <=5 times in D1 |
|---|---:|---:|---|---:|
| glioma | 1786 | 2 | `7c566016` (78.3%) | 0 (0.0%) |
| meningioma | 1784 | 4 | `8637136d` (49.7%) | 0 (0.0%) |
| notumor | 1681 | 50 | `3584b57f` (75.0%) | 52 (3.1%) |
| pituitary | 1762 | 2 | `7c566016` (52.8%) | 0 (0.0%) |

The three tumour classes are near-uniform. Their tables correspond to grayscale versus RGB encoding by a single pipeline, not to distinct origins. notumor is not uniform, and its dominant table is one that appears among the tumour images only in the augmented meningioma files -- so it is shared tooling, not a shared corpus.

### Whether each class travels to another compilation

D2 (BRISC2025) was compiled independently from the same Kaggle source. If a class belongs to a corpus that compilers draw from, it should reappear there; if it was sourced separately for D1, it need not. Matching is by pHash, so a re-encoded copy still counts and a low rate means genuinely different images.

| D2 class | n in D2 | Also in D1 | Share |
|---|---:|---:|---:|
| glioma | 1400 | 1375 | 98.2% |
| meningioma | 1613 | 1576 | 97.7% |
| notumor | 1197 | 53 | 4.4% |
| pituitary | 1740 | 1740 | 100.0% |

This is the clearest signal on the page. The three tumour classes reappear almost in their entirety in an independently assembled dataset. The no-tumour class does not.

### What this establishes, and what it does not

**Established, by measurement:** the notumor class in D1 has a different provenance from the three tumour classes. Three independent signals agree -- image geometry, JPEG encoder history, and whether the class reappears in an independently compiled dataset. The tumour classes form a stable corpus that travels between compilations; the no-tumour images do not travel with it. This does not rest on any dataset description.

**Not established:** the identity of the sources. Nothing on disk names Figshare CE-MRI, SARTAJ or Br35H, and none of those datasets is present in this repository, so no direct comparison is possible. The 512x512 uniformity of the tumour classes is consistent with Figshare CE-MRI, which is uniformly 512x512, but that is a weak fingerprint since many collections are. The specific attribution therefore remains quoted from nickparvar's dataset description rather than verified here.

**Not separable at all:** any SARTAJ contribution to the tumour classes. The three tumour classes are indistinguishable from each other on every signal measured here, so if they were assembled from two upstream sources, nothing on disk resolves the boundary. The 65 glioma, 244 meningioma and 59 pituitary images that are not 512x512 are the natural candidates for a second source, but they share the tumour classes' encoder signatures and are equally consistent with rescaling within one corpus.

The practical consequence is that the confound can be stated without the attribution. *notumor is separable from the tumour classes on acquisition properties alone, and was sourced differently* is measured here. Whether Br35H is the source it came from is a separate claim, and the argument does not need it.


## How to read this

- A three-class test accuracy approaching the CNN comparator means D1 inherits the Figshare slice-selection bias, and internal accuracy is not evidence that the models read tumours.
- A four-class accuracy far above the three-class one is driven by notumor, which comes from a different source in nickparvar's merge. Compare it against `geometry_control`: if image dimensions alone reach the same accuracy, the effect is source-of-file bias, which is a different limitation from the one Wallis & Buvat describe.
- `wallis_3_strict` is the number to quote when claiming a replication; `wallis_4` adds the second half of the orientation proxy.
- Val and test should agree. A gap would point at something split-specific rather than a property of D1.
