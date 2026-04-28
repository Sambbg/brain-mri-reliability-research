# D1 Acquisition Log — Nickparvar Kaggle Brain Tumor MRI Dataset

## Acquisition Date

2026-04-29

## Dataset

Brain Tumor MRI Dataset / Nickparvar Kaggle

## Kaggle Slug

masoudnickparvar/brain-tumor-mri-dataset

## Local Raw Path

data/raw/D1_nickparvar_kaggle/

## Download Method

Downloaded using Kaggle API.

Command used:

    kaggle datasets download -d masoudnickparvar/brain-tumor-mri-dataset -p data/raw/D1_nickparvar_kaggle

## Extraction Method

Command used:

    cd data/raw/D1_nickparvar_kaggle
    unzip brain-tumor-mri-dataset.zip

During extraction, the archive prompted for replacement because files already existed. The option N was selected to avoid overwriting existing extracted files.

## Observed Folder Structure

data/raw/D1_nickparvar_kaggle/

- Training/
  - glioma/
  - meningioma/
  - notumor/
  - pituitary/

- Testing/
  - glioma/
  - meningioma/
  - notumor/
  - pituitary/

## File Count Summary

| Item | Count / Size |
|---|---:|
| Training images | 5,600 |
| Testing images | 1,600 |
| Total images | 7,200 |
| Raw folder size | 332M |

## Training Counts

| Class | Count |
|---|---:|
| glioma | 1,400 |
| meningioma | 1,400 |
| notumor | 1,400 |
| pituitary | 1,400 |
| Total | 5,600 |

## Testing Counts

| Class | Count |
|---|---:|
| glioma | 400 |
| meningioma | 400 |
| notumor | 400 |
| pituitary | 400 |
| Total | 1,600 |

## Initial Assessment

The dataset is exactly balanced across the four classes in both the Training and Testing folders. This makes it convenient for initial model development, but it also reinforces the need for leakage checks because the dataset appears highly curated.

This dataset is suitable as a first development benchmark. It is not sufficient by itself as evidence of clinical reliability.

## Leakage Risk Status

Current leakage risk: High.

Reasons:

- Public 2D image benchmark.
- No confirmed patient-level identifiers.
- Possible duplicate or near-duplicate images across train/test folders.
- Possible overlap with other public brain MRI datasets.
- Very high class balance suggests curation rather than raw clinical sampling.

## Reproducibility Notes

Raw dataset files are excluded from Git using .gitignore.

The dataset acquisition was documented before model training.

The current verified raw dataset size is:

332M

The current verified image count is:

Training: 5,600
Testing: 1,600
Total: 7,200

## Next Required Step

Generate a formal image manifest containing:

- filepath;
- split;
- class label;
- image dimensions;
- file extension;
- file size;
- SHA256 hash;
- later perceptual hash.

After manifest generation, perform duplicate and leakage checks before using the dataset for model training.
