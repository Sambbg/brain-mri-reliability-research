# D1-D3B pHash Near-Overlap Report

## Input

- D1 pHash manifest: `data/processed/D1_manifest_deduplicated_phash.csv`
- D3B pHash manifest: `data/processed/D3B_selected_slices_manifest_phash.csv`
- D1 rows compared: 7013
- D3B rows compared: 265
- Total comparisons: 1858445
- pHash Hamming distance threshold: <= 4

## Summary

- Near-overlap pairs found: 0
- Cross-class near-overlap pairs: 0
- Output CSV: `reports/datasets/D1_D3B_near_overlap_pairs.csv`

## Distance Counts

- No near-overlap pairs found.

## Interpretation

No pHash near-overlap was detected between D1 and D3B at the selected threshold. This supports treating D3B as visually distinct from D1 for the planned domain-shift confidence analysis, although pHash cannot prove patient-level independence.

D3B remains a glioma-focused domain-shift dataset, not a full four-class external validation dataset.
