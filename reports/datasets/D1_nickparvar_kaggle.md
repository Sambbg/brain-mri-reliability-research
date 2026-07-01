# Dataset Documentation — D1 Nickparvar Kaggle Brain Tumor MRI Dataset

## Dataset Name
Brain Tumor MRI Dataset / Nickparvar Kaggle

## Dataset Role
Development source candidate

## Source
- Platform: Kaggle
- Dataset slug: `masoudnickparvar/brain-tumor-mri-dataset`
- Source URL: https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset
- Download date: TBD
- DOI: Not identified from current documentation
- Paper citation: TBD / not identified from dataset page

## License and Usage Terms
- License: Must be confirmed from Kaggle dataset page before use
- Academic use allowed: TBD
- Redistribution allowed: TBD
- Notes: Do not redistribute raw dataset files unless the Kaggle license permits it.

## Dataset Description
This is a public 2D brain MRI image dataset for tumour classification. It contains four diagnostic classes:

1. Glioma
2. Meningioma
3. Pituitary tumour
4. No tumour

Current source snippets report the dataset as containing approximately 7,023 to 7,200 images. The exact number must be verified after download by counting files locally.

## Classes

| Class Label | Meaning | Number of Images |
|---|---|---:|
| glioma | Glioma tumour MRI images | TBD after download |
| meningioma | Meningioma tumour MRI images | TBD after download |
| pituitary | Pituitary tumour MRI images | TBD after download |
| no_tumor | No tumour MRI images | TBD after download |

## File Structure

Expected structure based on common Kaggle layout:

```text
brain-tumor-mri-dataset/
├── Training/
│   ├── glioma/
│   ├── meningioma/
│   ├── notumor/
│   └── pituitary/
└── Testing/
    ├── glioma/
    ├── meningioma/
    ├── notumor/
    └── pituitary/


## Exact Duplicate Audit Result

An exact SHA256 duplicate audit was performed after manifest generation.

Results:

| Item | Count |
|---|---:|
| Original manifest rows | 7,200 |
| Unique SHA256 hashes | 7,013 |
| Duplicate hash groups | 153 |
| Images involved in duplicate groups | 340 |
| Cross-split duplicate groups | 0 |
| Cross-class duplicate groups | 0 |
| Rows removed in deduplicated manifest | 187 |
| Deduplicated manifest rows | 7,013 |

Interpretation:

No exact SHA256 duplicates were found across Training and Testing folders, so there is no exact hash-level evidence of train-test leakage. However, 187 duplicate rows were removed from the dataset, confirming repeated-image bias within the dataset. The deduplicated manifest should be preferred for future training and evaluation.

The class most affected was the Training `notumor` class, which decreased from 1,400 to 1,281 images after exact deduplication. This confirms that the original perfect class balance was partly artificial and should not be treated as evidence of dataset quality.


## Near-Duplicate Audit Result

A perceptual-hash near-duplicate audit was performed on the exact-deduplicated D1 manifest using pHash Hamming distance threshold `<= 4`.

Results:

| Item | Count |
|---|---:|
| Deduplicated rows compared | 7,013 |
| Near-duplicate pairs found | 5,125 |
| Cross-split near-duplicate pairs | 1,926 |
| Cross-class near-duplicate pairs | 46 |
| pHash distance 0 pairs | 1,447 |
| pHash distance 2 pairs | 1,750 |
| pHash distance 4 pairs | 1,928 |

Interpretation:

This is a serious leakage warning. The original D1 Training/Testing split cannot be treated as a clean independent evaluation split because many visually similar images occur across the original split boundary. Exact SHA256 checks did not detect cross-split duplicates, but perceptual hashing revealed substantial cross-split similarity.

Therefore, D1 should be used only as a development/source dataset after deduplication and leakage-aware splitting. The original Kaggle Testing folder should not be used as strong evidence of generalisation.

Important caveat:

pHash near-duplicate detection can produce false positives, especially for structurally similar MRI slices. However, the number of cross-split near-duplicate pairs is large enough that the original split should be considered high risk unless manually reviewed or replaced by a cleaner split strategy.





## Leakage-Aware Split Result

A leakage-aware split was created from the exact-deduplicated perceptual-hash manifest.

Split construction used:

- Input manifest: `data/processed/D1_manifest_deduplicated_phash.csv`
- Output split file: `data/splits/D1_leakage_aware_split.csv`
- Random seed: 42
- pHash Hamming distance threshold: `<= 4`
- Target split proportions: 70% train, 15% validation, 15% test

Results:

| Item | Count |
|---|---:|
| Rows assigned | 7,013 |
| Leakage groups created | 4,755 |
| Largest leakage group size | 24 |
| Mixed-label leakage groups | 25 |
| Cross-split near-duplicate pairs after splitting | 0 |

Assigned split counts:

| Split | Count |
|---|---:|
| Train | 4,909 |
| Validation | 1,053 |
| Test | 1,051 |

Interpretation:

This leakage-aware split should be preferred over the original Kaggle Training/Testing folders for internal D1 experiments. The original split showed substantial pHash-based cross-split near-duplicate risk, whereas the new split groups near-duplicate images before assigning train, validation, and test partitions.

Caveat:

This split reduces detected pHash-based leakage, but it does not prove patient-level independence because patient identifiers are unavailable.
