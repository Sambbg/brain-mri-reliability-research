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
