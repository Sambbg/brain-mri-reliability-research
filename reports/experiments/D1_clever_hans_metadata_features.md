# D1 Clever Hans probe - metadata-only feature classifier

Replication of experiment 5 of Wallis & Buvat (2022, *Medical Image Analysis* 77:102368) on the D1 leakage-aware split. A trivial classifier is fitted on features that cannot encode tumour appearance, trained on the train split and scored on val and test. No CNN is involved and nothing is retrained.

## Provenance

| Field | Value |
|---|---|
| Analysis commit | `89fd350588250d9515bf224a5101a9f0e23efbc5` |
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

Majority-class floor: 0.2555.

| Feature set | Classifier | Val acc | Test acc | Test macro-F1 |
|---|---|---:|---:|---:|
| `wallis_4` | decision_tree | 0.6306 | 0.6118 | 0.6157 |
| `wallis_4` | logistic_regression | 0.5679 | 0.5480 | 0.5456 |
| `wallis_3_strict` | decision_tree | 0.5062 | 0.5186 | 0.5053 |
| `wallis_3_strict` | logistic_regression | 0.4255 | 0.4434 | 0.4166 |
| `frac_zero_sensitivity` | decision_tree | 0.6448 | 0.6327 | 0.6183 |
| `frac_zero_sensitivity` | logistic_regression | 0.5394 | 0.5309 | 0.5249 |
| `shape_only` | decision_tree | 0.5299 | 0.5224 | 0.5087 |
| `shape_only` | logistic_regression | 0.4843 | 0.4843 | 0.4821 |
| `geometry_control` | decision_tree | 0.4568 | 0.4548 | 0.3559 |
| `geometry_control` | logistic_regression | 0.4274 | 0.4329 | 0.3364 |

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

Majority-class floor: 0.3358.

| Feature set | Classifier | Val acc | Test acc | Test macro-F1 |
|---|---|---:|---:|---:|
| `wallis_4` | decision_tree | 0.6579 | 0.6825 | 0.6861 |
| `wallis_4` | logistic_regression | 0.5693 | 0.5575 | 0.5546 |
| `wallis_3_strict` | decision_tree | 0.6454 | 0.6737 | 0.6766 |
| `wallis_3_strict` | logistic_regression | 0.4744 | 0.5088 | 0.5027 |
| `frac_zero_sensitivity` | decision_tree | 0.6866 | 0.6700 | 0.6684 |
| `frac_zero_sensitivity` | logistic_regression | 0.5718 | 0.5575 | 0.5543 |
| `shape_only` | decision_tree | 0.5194 | 0.5138 | 0.5078 |
| `shape_only` | logistic_regression | 0.4906 | 0.4925 | 0.4917 |
| `geometry_control` | decision_tree | 0.3483 | 0.3463 | 0.2089 |
| `geometry_control` | logistic_regression | 0.3308 | 0.3325 | 0.1859 |

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

## How to read this

- A three-class test accuracy approaching the CNN comparator means D1 inherits the Figshare slice-selection bias, and internal accuracy is not evidence that the models read tumours.
- A four-class accuracy far above the three-class one is driven by notumor, which comes from a different source in nickparvar's merge. Compare it against `geometry_control`: if image dimensions alone reach the same accuracy, the effect is source-of-file bias, which is a different limitation from the one Wallis & Buvat describe.
- `wallis_3_strict` is the number to quote when claiming a replication; `wallis_4` adds the second half of the orientation proxy.
- Val and test should agree. A gap would point at something split-specific rather than a property of D1.
