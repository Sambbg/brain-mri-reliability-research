# D3B Perceptual Hash Report

## Input and Output

- Input manifest: `data/processed/D3B_selected_slices_manifest.csv`
- Output manifest: `data/processed/D3B_selected_slices_manifest_phash.csv`
- Total rows processed: 265
- Errors: 0

## Hash Methods

- `phash`: lightweight perceptual hash based on low-frequency DCT coefficients.
- `ahash`: average hash.
- `dhash`: difference hash.
- `sha256_recomputed`: exact file hash of the converted PNG image.

## Summary

- Unique pHash values: 244
- Unique aHash values: 176
- Unique dHash values: 251
- Hashing errors: 0

## Interpretation

This report adds exact and perceptual hashes to the D3B converted central-slice manifest. The next step is to compare D3B against D1 using exact SHA256 overlap and pHash near-overlap checks. This is required before using D3B for domain-shift evaluation.
