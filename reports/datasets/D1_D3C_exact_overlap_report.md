# D1-D3C Exact Overlap Report

## Input

- D1 manifest: `data\processed\D1_manifest_deduplicated.csv`
- D3C manifest: `data\processed\D3C_selected_slices_manifest_phash.csv`
- D1 rows: 7013
- D3C rows: 2845

## Summary

- Shared SHA256 hashes: 0
- Exact overlap pairs: 0
- Output CSV: `reports\datasets\D1_D3C_exact_overlap_pairs.csv`

## Interpretation

No exact SHA256 overlap was detected between D1 deduplicated images and D3C converted central-slice PNG images. This is expected because D3C images were generated from DICOM conversion and are unlikely to be byte-identical to D1 JPEG images. Near-overlap testing using perceptual hashes is still required.
