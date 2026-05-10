# D2 Usage Decision ? BRISC2025

## Decision Date
2026-05-10

## Dataset
D2 ? BRISC2025 / BRISC Annotated Dataset for Brain Tumor Segmentation and Classification

## Initial Intended Role
D2 was selected as a candidate external target dataset for cross-dataset evaluation because it contains the same four broad classes as D1:

- glioma
- meningioma
- pituitary
- no tumour

## Decision
Do not treat D2/BRISC2025 as a clean independent external validation dataset against D1.

D2 may be used only as a secondary public-dataset audit case or as a source for a carefully filtered overlap-aware subset.

## Reason

D2 showed substantial internal quality issues and substantial overlap risk with D1.

## D2 Internal Exact Duplicate Audit

| Item | Count |
|---|---:|
| Original D2 rows | 6,000 |
| Unique SHA256 hashes | 5,950 |
| Duplicate hash groups | 46 |
| Images involved in duplicate groups | 96 |
| Cross-split duplicate groups | 7 |
| Cross-class duplicate groups | 0 |

Interpretation:

The original BRISC train/test split contains exact duplicate images crossing the train/test boundary. Therefore, the original BRISC split should not be treated as a clean independent benchmark split.

## D2 Internal Near-Duplicate Audit

After exact deduplication, pHash near-duplicate checking found:

| Item | Count |
|---|---:|
| Rows compared | 5,950 |
| Near-duplicate pairs found | 1,270 |
| Cross-split near-duplicate pairs | 419 |
| Cross-class near-duplicate pairs | 23 |

Interpretation:

The original BRISC train/test split also contains substantial pHash-based cross-split near-duplicate risk.

## D1-D2 Near-Overlap Audit

A pHash D1-vs-D2 near-overlap audit was performed using Hamming distance threshold `<= 4`.

| Item | Count |
|---|---:|
| D1 rows compared | 7,013 |
| D2 rows compared | 5,950 |
| Near-overlap pairs found | 7,290 |
| Cross-class near-overlap pairs | 68 |
| Distance 0 pairs | 5,037 |
| Distance 2 pairs | 564 |
| Distance 4 pairs | 1,689 |

Interpretation:

D2 has substantial visual overlap with D1. This may reflect reused public source images, resized/reformatted copies, adjacent slices, or pHash collisions. Regardless of the exact cause, D2 cannot be used as strong independent external validation against D1 without filtering or manual review.

## Consequence for Experiments

D2 should not be used as the main external test dataset for publication-grade claims.

Acceptable uses:

1. Demonstrate dataset recycling/overlap risk in public brain MRI benchmarks.
2. Test overlap-filtering methods.
3. Build a filtered D2 subset after excluding D1-overlapping images.
4. Use only as a secondary stress-test with clear limitations.

Unacceptable use:

1. Reporting D1-trained model performance on raw D2 as if it proves external generalisation.
2. Using the original BRISC train/test split as if it is clean.
3. Claiming D2 is fully independent from D1.

## Next Required Step

Find or construct a stronger external dataset candidate with less overlap against D1, or create a D2 overlap-filtered subset and clearly label it as filtered public-dataset evaluation rather than fully independent clinical validation.
