# pHash threshold sensitivity audit

Every near-duplicate audit in this project flags pairs at a pHash Hamming distance of 4 bits or fewer. That value is a convention rather than a derived quantity, so this sweeps 0, 2, 4, 6, 8 across all four comparisons and reports whether any decision depends on it. Hashes are read from the committed manifests and are not recomputed.

## Provenance

| Field | Value |
|---|---|
| git_commit | `ed0a8d53a31ceba7ee1c8ae7cff1d20038207590` |
| git_tree_dirty | `True` |
| split_csv_sha256 | `944ce00e4be958f3688a0996f6fb928fc7717e7c2804abb8000f28976efe0d43` |
| d1_phash_sha256 | `a8d581c6b5edd3136e6661973179e6688591bade6121156ccd0a1b2a6bff2be8` |
| d2_phash_sha256 | `228cf6e7a06129358b7c67238957a9339df79fd924dccc2e953da7ffc511152f` |
| d3b_phash_sha256 | `b835ed8cfdebc467e22d8741a3e04ae52cd567e8ab967a6529a844bd1aed03d7` |
| d3c_phash_sha256 | `d4f1bdfd8ac68fe806d7ab354b9a95d6a8276e5fa4e151a933592b13add1834f` |
| Rejection criterion | candidate match share >= 1% |

## D1 internal

`leakage_groups` and `largest_group_size` describe the grouping that *would* be derived at each threshold. `pairs_crossing_train_test` is a different and more important quantity: it counts near-duplicate pairs that straddle the train/test boundary of the **frozen split already in use**, which was built at threshold 4. A non-zero value there means the committed split leaks when judged by a stricter rule.

| Threshold | Pairs | Cross-class | Cross-class rate | Leakage groups | Largest group | Cross-split | Train/test | of which cross-class |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1447 | 2 | 0.14% | 6212 | 14 | 0 | 0 | 0 |
| 2 | 3197 | 11 | 0.34% | 5639 | 19 | 0 | 0 | 0 |
| 4 **<-- operating** | 5125 | 46 | 0.90% | 4755 | 24 | 0 | 0 | 0 |
| 6 | 7931 | 345 | 4.35% | 3425 | 175 | 857 | 415 | 44 |
| 8 | 13860 | 1951 | 14.08% | 1877 | 2751 | 3012 | 1456 | 276 |

**The frozen split leaks at threshold 6 and above**: 415 near-duplicate pairs straddle the train/test boundary, against zero at 0, 2 and 4. The split was built at threshold 4 and is leakage-free by that definition, but a reviewer applying a looser rule would find contamination.

The specificity argument below does **not** dispose of this. Of those 415 pairs, 44 are cross-class and therefore certainly spurious, but 371 are within-class, where the hash agreeing to within 6 bits is at least consistent with a true near-duplicate. Those have not been inspected image by image, so the honest position is that the frozen split is verified clean at threshold 4 and unverified above it, not that the pairs at 6 are known to be artefacts.

## Candidate datasets

| Comparison | Threshold | Pairs | Cross-class | Matched images | Share of candidate | Decision |
|---|---:|---:|---:|---:|---:|---|
| D1_vs_D2 | 0 | 5037 | 2 | 4744 | 79.7311% | REJECT |
| D1_vs_D2 | 2 | 5601 | 13 | 4746 | 79.7647% | REJECT |
| D1_vs_D2 | 4 | 7290 | 68 | 4755 | 79.9160% | REJECT |
| D1_vs_D2 | 6 | 11059 | 614 | 4795 | 80.5882% | REJECT |
| D1_vs_D2 | 8 | 20760 | 3392 | 4891 | 82.2017% | REJECT |
| D1_vs_D3B | 0 | 0 | 0 | 0 | 0.0000% | RETAIN |
| D1_vs_D3B | 2 | 0 | 0 | 0 | 0.0000% | RETAIN |
| D1_vs_D3B | 4 | 0 | 0 | 0 | 0.0000% | RETAIN |
| D1_vs_D3B | 6 | 0 | 0 | 0 | 0.0000% | RETAIN |
| D1_vs_D3B | 8 | 24 | 21 | 13 | 4.9057% | REJECT |
| D1_vs_D3C | 0 | 0 | 0 | 0 | 0.0000% | RETAIN |
| D1_vs_D3C | 2 | 2 | 0 | 1 | 0.0326% | RETAIN |
| D1_vs_D3C | 4 | 7 | 0 | 5 | 0.1629% | RETAIN |
| D1_vs_D3C | 6 | 158 | 81 | 87 | 2.8339% | REJECT |
| D1_vs_D3C | 8 | 1161 | 689 | 450 | 14.6580% | REJECT |

## Specificity: how far the threshold can be pushed

A cross-class pair cannot be a true duplicate. A glioma slice is not a duplicate of a pituitary slice, whatever their hashes say. The cross-class rate is therefore a lower bound on the false-positive rate, measured rather than assumed, and it is what determines how far the threshold can be pushed before the matcher stops being a duplicate detector.

| Threshold | D1 internal cross-class rate |
|---:|---:|
| 0 | 0.14% |
| 2 | 0.34% |
| 4 | 0.90% |
| 6 | 4.35% |
| 8 | 14.08% |

At the operating threshold the rate is 0.90%; at 8 it is 14.08%, a factor of 16. Every brain MRI resembles every other at low bit depth, and by 8 bits of tolerance the hash is matching that generic resemblance. Results at 6 and 8 should be read as the behaviour of a degraded matcher, not as newly discovered duplicates.

## Does any decision change?

**D1_vs_D3B: the verdict is not constant across the sweep.** It reads REJECT at threshold(s) [8] and RETAIN elsewhere.

**D1_vs_D3C: the verdict is not constant across the sweep.** It reads REJECT at threshold(s) [6, 8] and RETAIN elsewhere.

The D2 rejection is decided at threshold 0: 4744 of 5950 candidate images (79.7%) are already exact perceptual matches before any tolerance is allowed. No choice of threshold reverses that, because loosening the rule can only add matches.

D3B is clean at the operating threshold (0 of 265 images, 0.00%) but **not across the whole range**: at threshold 8 it reaches 13 images (4.91%), of which 21 of 24 pairs (88%) are cross-class and so cannot be duplicates.

D3C is clean at the operating threshold (5 of 3070 images, 0.16%) but **not across the whole range**: at threshold 8 it reaches 450 images (14.66%), of which 689 of 1161 pairs (59%) are cross-class and so cannot be duplicates.

## Conclusions

**The D2 rejection is threshold-independent, as claimed.** It is settled at Hamming 0, before any tolerance is allowed, and loosening the rule can only add matches.

**The claim that D3B and D3C are clean across the whole range does not hold as stated, and should be narrowed rather than repeated.** Both are clean at 0 through 4. At 6 and 8 both accumulate matches, and under the stated rejection criterion D3C would flip at 6 and D3B at 8. The defensible claim is that they are clean at the operating threshold and at every stricter one, which is what the audits actually support.

**The frozen split is leakage-free at 0, 2 and 4, and not at 6 or 8.** This is the one result that touches work already done. Most of the offending pairs at 6 are within-class, so they cannot be dismissed as matcher noise without inspecting them. Every internal metric in the study rests on this split, so the limitation belongs in the paper: the split is verified leakage-free under the stated matching rule and under stricter ones, and is not verified under looser ones.

The specificity table is what makes the rest readable. The thresholds where the candidate decisions move are the thresholds where the matcher's own false-positive rate has risen several-fold, and at 8 the largest connected component reaches 2751 of 7013 images, which is a collapsed matcher rather than a discovery. That is an argument for not using 6 or 8. It is not a demonstration that nothing is there.

## How to read this

- Pair counts rising with the threshold is arithmetic, not a finding: a wider tolerance admits strictly more pairs. Only the rates and the decisions carry information.
- The quantity that could invalidate existing work is `pairs_crossing_train_test`, because the frozen split is already in use and every internal metric in the study depends on it.
- A stable retain/reject verdict is not proof that a probe is independent of D1. Perceptual hashing compares images, not patients, and cannot establish patient-level independence at any threshold.
