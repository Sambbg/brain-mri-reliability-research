# D1 Clever Hans probe - skull-outline ablation

Replication of experiment 4 of Wallis & Buvat (2022, *Medical Image Analysis* 77:102368) on the D1 leakage-aware split. Every image is binarised at native resolution -- pixels below 100 to 0, the rest to 255 -- which erases all internal tissue structure while preserving the head and skull outline. The 15 frozen checkpoints are evaluated on the result without retraining.

## Provenance

| Field | Value |
|---|---|
| Checkpoint run set | `2026-08-sweep-a` |
| Analysis commit | `9eb9550dca47eb4f44103eb07bcb8c463a61bdb9` |
| Tree dirty at analysis time | True |
| Seeds | 42, 43, 44, 45, 46 |
| Split csv sha256 | `944ce00e4be958f3688a0996f6fb928fc7717e7c2804abb8000f28976efe0d43` |
| Binarisation threshold | 100 |
| Binarisation stage | native resolution, before the 224x224 resize |

## Identity control

The intact condition is run through the same harness and compared against the `test_accuracy` recorded in each run's `final_results.json`. If these do not match, nothing else on this page can be trusted.

| Model | Seed | Recorded | Reproduced | Delta | Pass |
|---|---:|---:|---:|---:|:--:|
| E001 | 42 | 0.954329 | 0.954329 | 0.00e+00 | yes |
| E001 | 43 | 0.967650 | 0.967650 | 0.00e+00 | yes |
| E001 | 44 | 0.971456 | 0.971456 | 0.00e+00 | yes |
| E001 | 45 | 0.972407 | 0.972407 | 0.00e+00 | yes |
| E001 | 46 | 0.964795 | 0.964795 | 0.00e+00 | yes |
| E002 | 42 | 0.974310 | 0.974310 | 0.00e+00 | yes |
| E002 | 43 | 0.964795 | 0.964795 | 0.00e+00 | yes |
| E002 | 44 | 0.962892 | 0.962892 | 0.00e+00 | yes |
| E002 | 45 | 0.965747 | 0.965747 | 0.00e+00 | yes |
| E002 | 46 | 0.967650 | 0.967650 | 0.00e+00 | yes |
| E003 | 42 | 0.953378 | 0.953378 | 0.00e+00 | yes |
| E003 | 43 | 0.956232 | 0.956232 | 0.00e+00 | yes |
| E003 | 44 | 0.959087 | 0.959087 | 0.00e+00 | yes |
| E003 | 45 | 0.956232 | 0.956232 | 0.00e+00 | yes |
| E003 | 46 | 0.952426 | 0.952426 | 0.00e+00 | yes |

**All identity checks passed: yes**

## Val split

n = 1053 four-class, 801 three-class. Majority-class floor 0.2555 and 0.3358.

### Four classes (all of D1)

| Model | Intact acc | Outline acc | Retained | Intact F1 | Outline F1 |
|---|---:|---:|---:|---:|---:|
| E001 ResNet18 | 0.9664 +/- 0.0041 | 0.5086 +/- 0.1020 | 0.526 | 0.9664 +/- 0.0040 | 0.4342 +/- 0.1070 |
| E002 EfficientNet-B0 | 0.9770 +/- 0.0041 | 0.2955 +/- 0.0310 | 0.302 | 0.9772 +/- 0.0041 | 0.1912 +/- 0.0449 |
| E003 ViT-B/16 | 0.9620 +/- 0.0041 | 0.3290 +/- 0.0348 | 0.342 | 0.9621 +/- 0.0039 | 0.2482 +/- 0.0392 |

### Three Figshare-derived classes (glioma, meningioma, pituitary)

This is the faithful comparison with Wallis & Buvat, whose dataset had no notumor class. The models remain four-way, so a notumor prediction on these images counts as an error.

| Model | Intact acc | Outline acc | Retained | Intact F1 | Outline F1 |
|---|---:|---:|---:|---:|---:|
| E001 ResNet18 | 0.9720 +/- 0.0071 | 0.3800 +/- 0.1562 | 0.391 | 0.9753 +/- 0.0050 | 0.3940 +/- 0.1114 |
| E002 EfficientNet-B0 | 0.9785 +/- 0.0028 | 0.0749 +/- 0.0428 | 0.077 | 0.9802 +/- 0.0029 | 0.1178 +/- 0.0562 |
| E003 ViT-B/16 | 0.9673 +/- 0.0032 | 0.1398 +/- 0.0555 | 0.145 | 0.9702 +/- 0.0043 | 0.2009 +/- 0.0514 |

## Test split

n = 1051 four-class, 800 three-class. Majority-class floor 0.2559 and 0.3362.

### Four classes (all of D1)

| Model | Intact acc | Outline acc | Retained | Intact F1 | Outline F1 |
|---|---:|---:|---:|---:|---:|
| E001 ResNet18 | 0.9661 +/- 0.0073 | 0.4974 +/- 0.0994 | 0.515 | 0.9662 +/- 0.0071 | 0.4251 +/- 0.1044 |
| E002 EfficientNet-B0 | 0.9671 +/- 0.0044 | 0.2991 +/- 0.0332 | 0.309 | 0.9673 +/- 0.0043 | 0.1978 +/- 0.0467 |
| E003 ViT-B/16 | 0.9555 +/- 0.0026 | 0.3305 +/- 0.0323 | 0.346 | 0.9557 +/- 0.0024 | 0.2479 +/- 0.0364 |

### Three Figshare-derived classes (glioma, meningioma, pituitary)

This is the faithful comparison with Wallis & Buvat, whose dataset had no notumor class. The models remain four-way, so a notumor prediction on these images counts as an error.

| Model | Intact acc | Outline acc | Retained | Intact F1 | Outline F1 |
|---|---:|---:|---:|---:|---:|
| E001 ResNet18 | 0.9720 +/- 0.0106 | 0.3715 +/- 0.1511 | 0.382 | 0.9759 +/- 0.0092 | 0.3868 +/- 0.1071 |
| E002 EfficientNet-B0 | 0.9732 +/- 0.0037 | 0.0823 +/- 0.0472 | 0.085 | 0.9754 +/- 0.0037 | 0.1273 +/- 0.0588 |
| E003 ViT-B/16 | 0.9637 +/- 0.0029 | 0.1357 +/- 0.0510 | 0.141 | 0.9665 +/- 0.0041 | 0.1962 +/- 0.0462 |

## Per-class recall under the ablation (test split)

Which classes survive binarisation matters. Retained accuracy concentrated in one class is a different finding from retained accuracy spread across all four.

| Model | Condition | glioma | meningioma | notumor | pituitary |
|---|---|---:|---:|---:|---:|
| E001 | intact | 0.9613 +/- 0.0090 | 0.9693 +/- 0.0148 | 0.9474 +/- 0.0103 | 0.9856 +/- 0.0098 |
| E001 | skull_outline | 0.5212 +/- 0.3487 | 0.5753 +/- 0.1242 | 0.8988 +/- 0.0753 | 0.0129 +/- 0.0288 |
| E002 | intact | 0.9539 +/- 0.0119 | 0.9768 +/- 0.0125 | 0.9474 +/- 0.0086 | 0.9894 +/- 0.0049 |
| E002 | skull_outline | 0.0290 +/- 0.0225 | 0.2172 +/- 0.1269 | 0.9904 +/- 0.0121 | 0.0000 +/- 0.0000 |
| E003 | intact | 0.9517 +/- 0.0112 | 0.9603 +/- 0.0063 | 0.9291 +/- 0.0044 | 0.9795 +/- 0.0124 |
| E003 | skull_outline | 0.1048 +/- 0.0639 | 0.3011 +/- 0.1719 | 0.9514 +/- 0.0334 | 0.0000 +/- 0.0000 |

## Collapse diagnostic (test split)

Accuracy alone cannot distinguish two opposite situations: a model reading a real signal from the outline, and a model pushed off-distribution that dumps every image into one class. The predicted-class distribution separates them. Under the intact condition the four classes are near-equally represented in the test split, so a balanced prediction distribution is the expectation for a model that is still discriminating.

| Model | Condition | glioma | meningioma | notumor | pituitary | Max share | Modal class |
|---|---|---:|---:|---:|---:|---:|---|
| E001 | intact | 0.254 | 0.265 | 0.232 | 0.249 | 0.265 | meningioma |
| E001 | skull_outline | 0.247 | 0.198 | 0.552 | 0.003 | 0.569 | notumor |
| E002 | intact | 0.252 | 0.268 | 0.229 | 0.251 | 0.270 | meningioma |
| E002 | skull_outline | 0.019 | 0.068 | 0.913 | 0.000 | 0.913 | notumor |
| E003 | intact | 0.257 | 0.265 | 0.226 | 0.253 | 0.269 | glioma |
| E003 | skull_outline | 0.035 | 0.111 | 0.854 | 0.000 | 0.854 | notumor |

**12 of 15 checkpoints put more than half of all test images into a single class under the ablation.**

## Per-checkpoint detail

Accuracies carry 95% Wilson intervals. These describe sampling error within a single checkpoint's evaluation over a fixed image set; they are **not** seed variation, which is a different quantity and is reported as a standard deviation in the tables above. A different seed is a different model, not a further draw from the same binomial, so the two must not be conflated or pooled.

For reference the three-class chance floor on test is 0.3362 (0.3044, 0.3697). An ablated accuracy whose interval falls entirely *below* that floor is not weak evidence of a weak signal; it is evidence the model has been pushed off distribution, since always naming the largest class would have scored higher.

| Model | Seed | Split | Condition | Acc 4c (95% CI) | Acc 3c (95% CI) | F1 (4c) | F1 (3c) |
|---|---:|---|---|---|---|---:|---:|
| E001 | 42 | test | intact | 0.9543 (0.9400, 0.9654) | 0.9575 (0.9412, 0.9694) | 0.9546 | 0.9631 |
| E001 | 42 | test | skull_outline | 0.3616 (0.3331, 0.3911) | 0.1762 (0.1514, 0.2042) | 0.2723 | 0.2270 |
| E001 | 42 | val | intact | 0.9658 (0.9530, 0.9752) | 0.9713 (0.9573, 0.9808) | 0.9660 | 0.9732 |
| E001 | 42 | val | skull_outline | 0.3761 (0.3473, 0.4057) | 0.1885 (0.1629, 0.2171) | 0.2851 | 0.2371 |
| E001 | 43 | test | intact | 0.9676 (0.9551, 0.9768) | 0.9750 (0.9617, 0.9838) | 0.9677 | 0.9787 |
| E001 | 43 | test | skull_outline | 0.5243 (0.4940, 0.5543) | 0.4113 (0.3777, 0.4457) | 0.4496 | 0.4037 |
| E001 | 43 | val | intact | 0.9668 (0.9541, 0.9760) | 0.9738 (0.9603, 0.9828) | 0.9667 | 0.9769 |
| E001 | 43 | val | skull_outline | 0.5461 (0.5159, 0.5759) | 0.4157 (0.3821, 0.4502) | 0.4633 | 0.4016 |
| E001 | 44 | test | intact | 0.9715 (0.9595, 0.9799) | 0.9788 (0.9662, 0.9867) | 0.9715 | 0.9819 |
| E001 | 44 | test | skull_outline | 0.5690 (0.5388, 0.5986) | 0.4675 (0.4332, 0.5021) | 0.4905 | 0.4551 |
| E001 | 44 | val | intact | 0.9658 (0.9530, 0.9752) | 0.9725 (0.9588, 0.9818) | 0.9660 | 0.9738 |
| E001 | 44 | val | skull_outline | 0.5726 (0.5426, 0.6022) | 0.4782 (0.4437, 0.5128) | 0.4931 | 0.4662 |
| E001 | 45 | test | intact | 0.9724 (0.9607, 0.9807) | 0.9838 (0.9724, 0.9905) | 0.9723 | 0.9856 |
| E001 | 45 | test | skull_outline | 0.6013 (0.5714, 0.6305) | 0.5437 (0.5091, 0.5780) | 0.5383 | 0.5035 |
| E001 | 45 | val | intact | 0.9725 (0.9607, 0.9808) | 0.9813 (0.9693, 0.9886) | 0.9724 | 0.9831 |
| E001 | 45 | val | skull_outline | 0.6192 (0.5895, 0.6480) | 0.5643 (0.5297, 0.5982) | 0.5579 | 0.5242 |
| E001 | 46 | test | intact | 0.9648 (0.9519, 0.9744) | 0.9650 (0.9499, 0.9757) | 0.9650 | 0.9700 |
| E001 | 46 | test | skull_outline | 0.4310 (0.4014, 0.4612) | 0.2587 (0.2296, 0.2902) | 0.3747 | 0.3446 |
| E001 | 46 | val | intact | 0.9611 (0.9476, 0.9712) | 0.9613 (0.9456, 0.9726) | 0.9610 | 0.9698 |
| E001 | 46 | val | skull_outline | 0.4292 (0.3997, 0.4593) | 0.2534 (0.2245, 0.2847) | 0.3715 | 0.3408 |
| E002 | 42 | test | intact | 0.9743 (0.9629, 0.9823) | 0.9788 (0.9662, 0.9867) | 0.9744 | 0.9807 |
| E002 | 42 | test | skull_outline | 0.2712 (0.2452, 0.2988) | 0.0425 (0.0306, 0.0588) | 0.1582 | 0.0760 |
| E002 | 42 | val | intact | 0.9820 (0.9720, 0.9884) | 0.9813 (0.9693, 0.9886) | 0.9820 | 0.9838 |
| E002 | 42 | val | skull_outline | 0.2716 (0.2456, 0.2993) | 0.0424 (0.0305, 0.0587) | 0.1581 | 0.0757 |
| E002 | 43 | test | intact | 0.9648 (0.9519, 0.9744) | 0.9725 (0.9587, 0.9818) | 0.9649 | 0.9743 |
| E002 | 43 | test | skull_outline | 0.3520 (0.3238, 0.3814) | 0.1575 (0.1339, 0.1844) | 0.2729 | 0.2213 |
| E002 | 43 | val | intact | 0.9734 (0.9618, 0.9815) | 0.9750 (0.9617, 0.9838) | 0.9736 | 0.9769 |
| E002 | 43 | val | skull_outline | 0.3447 (0.3166, 0.3740) | 0.1436 (0.1210, 0.1696) | 0.2647 | 0.2102 |
| E002 | 44 | test | intact | 0.9629 (0.9497, 0.9727) | 0.9700 (0.9557, 0.9798) | 0.9632 | 0.9719 |
| E002 | 44 | test | skull_outline | 0.3073 (0.2802, 0.3359) | 0.0950 (0.0766, 0.1173) | 0.2070 | 0.1397 |
| E002 | 44 | val | intact | 0.9772 (0.9663, 0.9846) | 0.9788 (0.9663, 0.9867) | 0.9774 | 0.9795 |
| E002 | 44 | val | skull_outline | 0.3067 (0.2796, 0.3353) | 0.0886 (0.0709, 0.1103) | 0.2024 | 0.1303 |
| E002 | 45 | test | intact | 0.9657 (0.9529, 0.9752) | 0.9700 (0.9557, 0.9798) | 0.9661 | 0.9726 |
| E002 | 45 | test | skull_outline | 0.2721 (0.2461, 0.2998) | 0.0450 (0.0327, 0.0617) | 0.1606 | 0.0811 |
| E002 | 45 | val | intact | 0.9725 (0.9607, 0.9808) | 0.9763 (0.9633, 0.9848) | 0.9727 | 0.9782 |
| E002 | 45 | val | skull_outline | 0.2716 (0.2456, 0.2993) | 0.0424 (0.0305, 0.0587) | 0.1574 | 0.0764 |
| E002 | 46 | test | intact | 0.9676 (0.9551, 0.9768) | 0.9750 (0.9617, 0.9838) | 0.9678 | 0.9775 |
| E002 | 46 | test | skull_outline | 0.2931 (0.2663, 0.3213) | 0.0712 (0.0554, 0.0912) | 0.1903 | 0.1184 |
| E002 | 46 | val | intact | 0.9801 (0.9697, 0.9869) | 0.9813 (0.9693, 0.9886) | 0.9802 | 0.9825 |
| E002 | 46 | val | skull_outline | 0.2830 (0.2566, 0.3110) | 0.0574 (0.0433, 0.0758) | 0.1735 | 0.0963 |
| E003 | 42 | test | intact | 0.9534 (0.9389, 0.9646) | 0.9613 (0.9455, 0.9726) | 0.9537 | 0.9631 |
| E003 | 42 | test | skull_outline | 0.2950 (0.2682, 0.3232) | 0.0862 (0.0687, 0.1077) | 0.2098 | 0.1498 |
| E003 | 42 | val | intact | 0.9630 (0.9498, 0.9728) | 0.9700 (0.9558, 0.9798) | 0.9630 | 0.9725 |
| E003 | 42 | val | skull_outline | 0.2858 (0.2594, 0.3139) | 0.0836 (0.0664, 0.1049) | 0.2026 | 0.1461 |
| E003 | 43 | test | intact | 0.9562 (0.9421, 0.9670) | 0.9663 (0.9513, 0.9767) | 0.9565 | 0.9676 |
| E003 | 43 | test | skull_outline | 0.3463 (0.3182, 0.3756) | 0.1588 (0.1351, 0.1857) | 0.2676 | 0.2217 |
| E003 | 43 | val | intact | 0.9601 (0.9465, 0.9704) | 0.9663 (0.9514, 0.9767) | 0.9602 | 0.9694 |
| E003 | 43 | val | skull_outline | 0.3571 (0.3287, 0.3865) | 0.1735 (0.1489, 0.2013) | 0.2797 | 0.2378 |
| E003 | 44 | test | intact | 0.9591 (0.9453, 0.9695) | 0.9663 (0.9513, 0.9767) | 0.9588 | 0.9723 |
| E003 | 44 | test | skull_outline | 0.3225 (0.2950, 0.3514) | 0.1125 (0.0924, 0.1363) | 0.2430 | 0.1851 |
| E003 | 44 | val | intact | 0.9687 (0.9563, 0.9776) | 0.9713 (0.9573, 0.9808) | 0.9686 | 0.9762 |
| E003 | 44 | val | skull_outline | 0.3181 (0.2907, 0.3469) | 0.1111 (0.0912, 0.1348) | 0.2412 | 0.1864 |
| E003 | 45 | test | intact | 0.9562 (0.9421, 0.9670) | 0.9650 (0.9499, 0.9757) | 0.9564 | 0.9675 |
| E003 | 45 | test | skull_outline | 0.3111 (0.2839, 0.3398) | 0.1075 (0.0879, 0.1309) | 0.2198 | 0.1616 |
| E003 | 45 | val | intact | 0.9601 (0.9465, 0.9704) | 0.9638 (0.9485, 0.9747) | 0.9603 | 0.9657 |
| E003 | 45 | val | skull_outline | 0.3124 (0.2852, 0.3411) | 0.1111 (0.0912, 0.1348) | 0.2214 | 0.1648 |
| E003 | 46 | test | intact | 0.9524 (0.9378, 0.9637) | 0.9600 (0.9441, 0.9715) | 0.9529 | 0.9620 |
| E003 | 46 | test | skull_outline | 0.3777 (0.3489, 0.4074) | 0.2137 (0.1867, 0.2435) | 0.2994 | 0.2626 |
| E003 | 46 | val | intact | 0.9582 (0.9444, 0.9687) | 0.9650 (0.9499, 0.9757) | 0.9586 | 0.9671 |
| E003 | 46 | val | skull_outline | 0.3713 (0.3427, 0.4009) | 0.2197 (0.1924, 0.2497) | 0.2961 | 0.2693 |

## How to read this

- Outline accuracy near intact accuracy would mean internal performance is substantially attributable to something other than tumour appearance.
- Outline accuracy at or below the majority-class floor, **combined with a collapsed prediction distribution**, means something weaker and different: the binarised images are simply outside the distribution these models were trained on. That is a statement about the ablation, not about D1.
- Accuracy *below* the majority floor is the clearest sign of collapse. A model retaining any usable signal cannot do worse than always naming the largest class; a model dumping everything into a small class can.
- A high four-class number alongside a floor-level three-class number is **not** slice-selection bias. It indicates the notumor class is separable on image-level properties, which follows from its coming from a different source in the merge. See the metadata-feature probe (`D1_clever_hans_metadata_features.md`) and its geometry control.
- The val and test splits should agree. A gap between them would point at something split-specific rather than a property of D1.

## Scope limit of this experiment

These 15 checkpoints were trained on intact images and are evaluated here on binarised ones without retraining, as specified. That makes this a weaker test than it may appear, and the direction of the weakness matters: **a null result here is not evidence that D1 is free of the bias Wallis & Buvat describe.** Distribution shift alone can destroy accuracy regardless of what the models were reading, and the collapse diagnostic above shows whether that is what happened.

Establishing what a skull outline alone supports on D1 requires training a classifier on binarised images, which this experiment does not do. The metadata-feature probe (`D1_clever_hans_metadata_features.md`) does fit its classifier from scratch on non-tumour features, and is therefore the load-bearing evidence of the two.

The full text of Wallis & Buvat (2022) is paywalled and it was not verified whether their experiment 4 trained on the binarised images or evaluated pre-trained models on them. If they trained, this experiment is not a replication of theirs and the two results are not comparable.
