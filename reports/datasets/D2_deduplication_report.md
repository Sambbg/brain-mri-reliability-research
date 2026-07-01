# D2 Deduplication Report

## Input and Output

- Input manifest: `data/processed/D2_manifest.csv`
- Output manifest: `data/processed/D2_manifest_deduplicated.csv`

## Summary

- Original rows: 6000
- Deduplicated rows: 5950
- Removed duplicate rows: 50
- Unique SHA256 hashes retained: 5950

## Deduplication Rule

Rows were grouped by exact SHA256 hash. For each duplicate group, one row was retained using a deterministic sort by source split, class label, and filepath. All remaining rows in the group were excluded from the deduplicated manifest.

## Deduplicated Split Counts

- test: 995
- train: 4955

## Deduplicated Class Counts

- test / glioma: 253
- test / meningioma: 303
- test / notumor: 139
- test / pituitary: 300
- train / glioma: 1147
- train / meningioma: 1310
- train / notumor: 1058
- train / pituitary: 1440

## Interpretation

The original D2 manifest contains exact duplicate images, including duplicates crossing the original train/test split. Therefore, the original BRISC train/test split should not be treated as a clean independent evaluation split. The deduplicated manifest should be used for future D2 analysis, but near-duplicate and D1-vs-D2 overlap checks are still required.
