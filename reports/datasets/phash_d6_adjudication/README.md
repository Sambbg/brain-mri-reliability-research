# Blind adjudication set: within-class pHash pairs at Hamming 6

The threshold sensitivity audit (`reports/experiments/consolidated/tables/phash_threshold_sensitivity.md`) found 371 within-class near-duplicate pairs that cross the train/test boundary of the frozen split at Hamming 6, against zero at the operating threshold of 4. Counting cannot settle whether those are real duplicates. This set exists so that looking at them produces a rate instead of an impression.

## What is in the sample

| Group | n | Definition |
|---|---:|---|
| `crossing` | 40 | Within-class, distance 6, one endpoint in train and one in test. Drawn from 371. |
| `same_split` | 40 | Within-class, distance 6, both endpoints in the same assigned split. Drawn from 1730. |

Both groups are stratified to the class distribution of the full crossing population: {'pituitary': 13, 'glioma': 10, 'notumor': 9, 'meningioma': 8}. The two are interleaved under a single shuffle at seed 42 and labelled PAIR_01 to PAIR_80.

## Why the null is at distance 6 exactly

Every D1 pHash has exactly 32 of its 64 bits set, which the median split used to compute it guarantees. The Hamming distance between two equal-weight vectors is always even, so odd distances cannot occur, and the observed distances are only 0, 2, 4 and 6. All 371 crossing pairs sit at exactly 6. A null drawn from 5 to 7 would therefore have been identifiable from the printed distance alone, and the comparison would not have been blind. The script asserts the 32-bit property and aborts if it ever stops holding.

A consequence worth carrying back to the sensitivity audit: because distances are always even, thresholds 1, 3, 5 and 7 behave identically to 0, 2, 4 and 6. The sweep already reported is exhaustive over the range, not a sample of it.

## Why filenames are shown

The `Tr-` and `Te-` prefixes name the original download folder, not the assigned split, and predict it barely at all: 14.5% of `Te-` images and 15.1% of `Tr-` images are in the test partition. Printing them does not unblind the sample. The assigned split is in the key only.

## How to score it

1. Open `contact_sheet.pdf` (80 pages, one pair per page, both images at native resolution).
2. For each pair, record one of four verdicts in the `verdict` column of `adjudication_worksheet.csv`.
3. Only then open `blind_key.csv`.

| Verdict | Meaning | Counts as leakage? |
|---|---|---|
| `same_image` | The same slice, differing only by rescaling, re-encoding or minor cropping. | Yes |
| `same_patient` | Different slices, but evidently the same patient and acquisition: the skull outline, ventricles and gross anatomy correspond while the tumour or the slice level differs. | **Yes** |
| `distinct` | Two different patients that merely resemble each other. | No |
| `unsure` | Cannot tell. | Counted separately |

**The `same_patient` category is the one that matters and is easy to score wrongly.** A leakage-aware split has to separate patients, not images. Two adjacent slices from one series sitting either side of the train/test boundary are contamination even though the images are plainly not identical, and a binary duplicate/distinct rubric would score them as clean. Judge patient identity, not image identity.

The quantity of interest is the leakage rate -- `same_image` plus `same_patient` -- in each group, and the difference between them. If the two groups come out at materially the same rate, then Hamming 6 flags the same kind of thing on both sides of the boundary, the boundary-crossing count is matcher noise, and the frozen split is sound at 6. If the `crossing` group is higher, the split leaks at 6 and the internal metrics carry contamination the audit at threshold 4 did not detect.

Note that the `same_split` group is not a pure negative control. Its pairs can perfectly well be the same patient -- that is exactly what the leakage-aware grouping is supposed to achieve, keeping a patient's images together on one side. A high `same_patient` rate in that group is the split working, not failing. The comparison is therefore between rates, not against zero.

Note the asymmetry in what the two outcomes cost. A null result closes the limitation. A positive result does not invalidate the study on its own, because it would have to be weighed against how many pairs are involved -- 371 pairs across 7,013 images -- but it would need reporting and quantifying rather than a footnote.

## Provenance

| Field | Value |
|---|---|
| git_commit | `83a30618925862cd96dbe65c50f76a3c04ae7d98` |
| split_csv_sha256 | `944ce00e4be958f3688a0996f6fb928fc7717e7c2804abb8000f28976efe0d43` |
| d1_phash_sha256 | `a8d581c6b5edd3136e6661973179e6688591bade6121156ccd0a1b2a6bff2be8` |
| seed | `42` |
| distance | `6` |

Sampled composition: {'crossing': 40, 'same_split': 40}, classes {'pituitary': 26, 'glioma': 20, 'notumor': 18, 'meningioma': 16}.
