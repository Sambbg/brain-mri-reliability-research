# D1 Exact Duplicate Report

## Input

- Manifest: `data/processed/D1_manifest.csv`
- Total manifest rows: 7200

## Summary

- Unique SHA256 hashes: 7013
- Duplicate hash groups: 153
- Images involved in duplicate groups: 340
- Cross-split duplicate groups: 0
- Cross-class duplicate groups: 0

## Interpretation

Exact duplicate SHA256 hashes were found. These must be investigated before training. Cross-split duplicates are especially serious because they can leak test information into training.

