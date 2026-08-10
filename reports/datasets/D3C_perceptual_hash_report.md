# D3C Perceptual Hash Report

## Input and Output

- Input manifest: `data/processed/D3C_selected_slices_manifest.csv`
- Output manifest: `data/processed/D3C_selected_slices_manifest_phash.csv`
- Total rows processed: 3070
- Errors: 0

## Hash Methods

- `phash`: lightweight perceptual hash based on low-frequency DCT coefficients.
- `ahash`: average hash.
- `dhash`: difference hash.
- `sha256_recomputed`: exact file hash of the converted PNG image.

## Summary

- Unique pHash values: 2563
- Unique aHash values: 948
- Unique dHash values: 2779
- Hashing errors: 0

## Interpretation

This report adds exact and perceptual hashes to the D3C converted central-slice manifest. The next step is to compare D3C against D1 using exact SHA256 overlap and pHash near-overlap checks. This is required before using D3C for domain-shift evaluation.
