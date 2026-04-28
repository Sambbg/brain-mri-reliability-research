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


