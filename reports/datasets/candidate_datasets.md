# Candidate Datasets for Brain MRI Reliability Study

## Purpose

This document records candidate datasets before acquisition. The goal is to choose datasets based on source quality, licensing, class structure, leakage risk, and suitability for cross-dataset reliability testing.

## Selection Rule

At least two datasets are required before model training:

1. One development/source dataset for training, validation, and internal testing.
2. One independent external target dataset for cross-dataset evaluation.

## Candidate Dataset Table

## Candidate Dataset Table

| ID | Dataset Name | Source Link | Classes | Approx. Size | License / Terms | Patient IDs Available? | Original Split? | Candidate Role | Leakage Risk | Decision |
|---|---|---|---|---:|---|---|---|---|---|---|
| D1 | Brain Tumor MRI Dataset / Nickparvar Kaggle | Kaggle: masoudnickparvar/brain-tumor-mri-dataset | Glioma, Meningioma, Pituitary, No Tumor | 7,023 images | Kaggle terms; license must be confirmed from dataset page | No clear patient IDs | Yes, train/test folders reported | Development source candidate | High | Use cautiously |
| D2 | BRISC2025 | Kaggle + Figshare + Nature Scientific Data paper | Glioma, Meningioma, Pituitary, No Tumor; segmentation masks included | 6,000 T1-weighted MRI slices | Must confirm from Kaggle/Figshare page | No clear patient IDs from current summary | Yes, 5,000 train / 1,000 test reported | Curated target / segmentation-supported dataset | Medium-High | Use cautiously; possible source overlap with D1 |
| D3 | Figshare Brain Tumor Dataset / Cheng | Figshare DOI: 10.6084/m9.figshare.1512427.v5 | Meningioma, Glioma, Pituitary | 3,064 T1-weighted contrast-enhanced images from 233 patients | CC BY 4.0 reported | Yes, 233 patients reported | Not safely assumed; must inspect metadata | Optional tumour-only external target | Medium | Candidate |
## Minimum Dataset Pair Requirement

The first accepted pair must satisfy:

- Both datasets contain brain MRI tumour classification labels.
- Classes can be mapped consistently.
- Sources are independent enough to support dataset-shift testing.
- Dataset links and licenses are recorded.
- Data can be downloaded reproducibly.
- Obvious duplicates are checked before training.

## Notes
## Initial Dataset Assessment Notes

D1 is attractive because it contains four classes including "No Tumor", but it is high leakage risk because it is a heavily reused public 2D image dataset with unclear patient-level metadata.

D2 is attractive because it has radiologist/physician quality control and segmentation masks, but it may overlap with D1 because BRISC2025 was reportedly derived from the Kaggle Brain Tumor MRI Dataset before curation. Therefore, D2 cannot be treated as a fully independent external test set until duplicate detection is completed.

D3 is useful because it has patient-level information reported in the source description: 3,064 T1-weighted contrast-enhanced images from 233 patients. However, it lacks the "No Tumor" class, so it may only support a three-class tumour-only experiment or an auxiliary external test.
