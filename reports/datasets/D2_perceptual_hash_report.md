# D2 Perceptual Hash Report

## Input and Output

- Input manifest: `data/processed/D2_manifest_deduplicated.csv`
- Output manifest: `data/processed/D2_manifest_deduplicated_phash.csv`
- Total rows processed: 5950

## Hash Methods

- `phash`: perceptual hash, useful for visually similar image detection.
- `ahash`: average hash, simple global appearance hash.
- `dhash`: difference hash, edge/gradient-oriented hash.

## Summary

- Unique pHash values: 5830
- Unique aHash values: 3919
- Unique dHash values: 5817
- Errors: 0

## Interpretation

This report adds perceptual hash values to the exact-deduplicated D2 manifest. The next step is to compare pHash Hamming distances to identify near-duplicate image pairs within D2 and then compare D2 against D1 to detect possible dataset overlap.
