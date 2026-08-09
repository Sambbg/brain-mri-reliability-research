# D1 Perceptual Hash Report

## Input and Output

- Input manifest: `data\processed\D1_manifest_deduplicated.csv`
- Output manifest: `data\processed\D1_manifest_deduplicated_phash.csv`
- Total rows processed: 7013

## Hash Methods

- `phash`: perceptual hash, useful for visually similar image detection.
- `ahash`: average hash, simple global appearance hash.
- `dhash`: difference hash, edge/gradient-oriented hash.

## Summary

- Unique pHash values: 6212
- Unique aHash values: 3655
- Unique dHash values: 6161
- Errors: 0

## Interpretation

This report adds perceptual hash values to the exact-deduplicated manifest. The next step is to compare Hamming distances between pHash values to identify near-duplicate image pairs. Near-duplicates may indicate repeated slices, resized images, cropped copies, or other leakage risks that exact SHA256 cannot detect.
