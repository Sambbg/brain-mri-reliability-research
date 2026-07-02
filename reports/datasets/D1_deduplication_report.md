# D1 Deduplication Report

## Input and Output

- Input manifest: `data\processed\D1_manifest.csv`
- Output manifest: `data\processed\D1_manifest_deduplicated.csv`

## Summary

- Original rows: 7200
- Deduplicated rows: 7013
- Removed duplicate rows: 187
- Unique SHA256 hashes retained: 7013

## Deduplication Rule

Rows were grouped by exact SHA256 hash. For each duplicate group, one row was retained using a deterministic sort by split, class label, and filepath. All remaining rows in the group were excluded from the deduplicated manifest.

## Deduplicated Split Counts

- Testing: 1584
- Training: 5429

## Deduplicated Class Counts

- Testing / glioma: 386
- Testing / meningioma: 398
- Testing / notumor: 400
- Testing / pituitary: 400
- Training / glioma: 1400
- Training / meningioma: 1386
- Training / notumor: 1281
- Training / pituitary: 1362

## Interpretation

The deduplicated manifest should be preferred for training and evaluation. The original manifest is retained for auditability. Exact duplicate removal reduces repeated-image bias, but it does not remove near-duplicates or same-patient adjacent slices.
