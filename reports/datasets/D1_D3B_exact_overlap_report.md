# D1-D3B Exact Overlap Report

## Input

- D1 manifest: `data/processed/D1_manifest_deduplicated.csv`
- D3B manifest: `data/processed/D3B_selected_slices_manifest_phash.csv`
- D1 rows: 7013
- D3B rows: 265

## Summary

- Shared SHA256 hashes: 0
- Exact overlap pairs: 0
- Output CSV: `reports/datasets/D1_D3B_exact_overlap_pairs.csv`

## Interpretation

No exact SHA256 overlap was detected between D1 deduplicated images and D3B converted central-slice PNG images. This is expected because D3B images were generated from DICOM conversion and are unlikely to be byte-identical to D1 JPEG images. Near-overlap testing using perceptual hashes is still required.
