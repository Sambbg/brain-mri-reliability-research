# D2 Acquisition Log - BRISC2025

## Acquisition Date
2026-05-10

## Dataset
BRISC2025 / BRISC Annotated Dataset for Brain Tumor Segmentation and Classification

## Kaggle Slug
briscdataset/brisc2025

## Local Raw Path
data/raw/D2_brisc2025/

## Download Method
Downloaded using Kaggle API:
kaggle datasets download -d briscdataset/brisc2025 -p data/raw/D2_brisc2025

## Extraction Method
Extracted using:
cd data/raw/D2_brisc2025
unzip brisc2025.zip
cd ~/research

A repeated unzip command was accidentally run after extraction. The overwrite prompt appeared and replacement was declined. Existing files were not intentionally overwritten.

## Observed Folder Structure
data/raw/D2_brisc2025/
- brisc2025.zip
- brisc2025/
  - README.md
  - classification_task/
    - train/
      - glioma/
      - meningioma/
      - no_tumor/
      - pituitary/
    - test/
      - glioma/
      - meningioma/
      - no_tumor/
      - pituitary/
  - segmentation_task/
    - train/images/
    - train/masks/
    - test/images/
    - test/masks/

## Total Raw File Summary
- Total files under raw D2 folder: 15,592
- Raw folder size: 547M
- Downloaded archive size: 251M

## Classification Task Counts
- Train: 5,000
- Test: 1,000
- Total: 6,000

## Classification Train Counts
- glioma: 1,147
- meningioma: 1,329
- no_tumor: 1,067
- pituitary: 1,457
- Total: 5,000

## Classification Test Counts
- glioma: 254
- meningioma: 306
- no_tumor: 140
- pituitary: 300
- Total: 1,000

## README Notes
The dataset README describes BRISC2025 as a curated, expert-annotated T1 MRI dataset for both multi-class classification and pixel-wise segmentation.

The README reports:
- 6,000 T1-weighted MRI slices.
- 5,000 training images and 1,000 test images.
- Four classes: glioma, meningioma, pituitary tumour, and no tumour.
- Pixel-wise segmentation masks reviewed by radiologists.
- Axial, coronal, and sagittal image planes.
- File naming convention including split, tumour type, anatomical view, and sequence.

## Important Dataset-Quality Observation
The README describes the dataset as having a balanced classification split. However, local file counts show class imbalance, especially in the test split:
- test no_tumor: 140
- test meningioma: 306
- test pituitary: 300
- test glioma: 254

Therefore, this project will not assume BRISC2025 is class-balanced. Evaluation should use macro-F1, balanced accuracy, per-class recall, and calibration metrics rather than accuracy alone.

## Preliminary Leakage Risk Status
Current leakage risk: Medium-High.

Reasons:
1. Public dataset.
2. Collated or inspired by existing public brain MRI datasets.
3. Possible overlap with D1 or other public sources.
4. Patient identifiers not yet confirmed.
5. README claims balance, but local class counts show imbalance.
6. External-test validity requires D1-vs-D2 exact and near-duplicate overlap checks.

## Reproducibility Notes
Raw dataset files are excluded from Git using .gitignore.

This acquisition log documents D2 before manifest generation and before model evaluation.

## Next Required Step
Generate a D2 classification manifest containing filepath, split, class label, image dimensions, file extension, file size, SHA256 hash, and perceptual hash.
