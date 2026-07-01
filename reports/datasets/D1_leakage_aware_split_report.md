# D1 Leakage-Aware Split Report

## Input and Output

- Input manifest: `data/processed/D1_manifest_deduplicated_phash.csv`
- Output split file: `data/splits/D1_leakage_aware_split.csv`
- Random seed: 42
- pHash Hamming distance threshold: <= 4

## Summary

- Rows loaded: 7013
- Rows assigned: 7013
- Leakage groups created: 4755
- Largest leakage group size: 24
- Mixed-label leakage groups: 25
- Cross-split near-duplicate pairs after splitting: 0

## Assigned Split Counts

- train: 4909
- val: 1053
- test: 1051

## Assigned Split Counts by Class

### train

- glioma: 1248
- meningioma: 1250
- notumor: 1178
- pituitary: 1233

### val

- glioma: 269
- meningioma: 267
- notumor: 252
- pituitary: 265

### test

- glioma: 269
- meningioma: 267
- notumor: 251
- pituitary: 264

## Verification

No pHash-near-duplicate pairs crossed the assigned train/validation/test split boundary at the selected threshold. This does not prove patient-level independence, but it removes the detected pHash-based near-duplicate leakage from the split.

## Interpretation

This split should be preferred over the original Kaggle Training/Testing folders for internal D1 experiments. The original split had substantial pHash-based cross-split near-duplicate risk. This leakage-aware split groups near-duplicate images together before assigning train, validation, and test partitions.

## Caveats

- pHash grouping may over-group visually similar but genuinely distinct MRI slices.
- Patient-level identifiers are still unavailable.
- This split is cleaner than the original Kaggle split but is not a substitute for independent external validation.
- Publication-grade generalisation claims still require an external dataset.
