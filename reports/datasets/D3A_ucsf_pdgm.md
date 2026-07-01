# D3A Dataset Documentation ? UCSF-PDGM

## Dataset Name

UCSF-PDGM ? University of California San Francisco Preoperative Diffuse Glioma MRI Dataset

## Candidate ID

D3A

## Source

- Repository: The Cancer Imaging Archive, TCIA
- Collection name: UCSF-PDGM
- Source page: TCIA UCSF-PDGM collection
- Associated paper: The University of California San Francisco Preoperative Diffuse Glioma MRI Dataset

## Dataset Role in This Project

D3A is being investigated as a stronger external dataset candidate after D2/BRISC2025 was rejected as a clean independent external validation dataset due to massive overlap with D1.

D3A is not a direct replacement for D1 because it does not provide the same four-class structure:

- glioma
- meningioma
- pituitary
- notumor

Instead, D3A is a glioma-focused clinical MRI dataset. Its likely role is external domain-shift evaluation, glioma-focused reliability testing, or future tumour-vs-non-tumour/domain-shift analysis.

## Verified Source Facts

The TCIA source describes UCSF-PDGM as a dataset of adult patients with histopathologically confirmed grade II-IV diffuse gliomas who underwent preoperative MRI.

The associated publication reports 501 cases. The cases include diffuse gliomas with WHO grade distribution reported in the publication.

## Why D3A Is Being Investigated

D3A is stronger than another Kaggle-style dataset because:

1. It is hosted by TCIA.
2. It has clearer clinical provenance.
3. It has subject-level/case-level organisation.
4. It is based on histopathologically confirmed diffuse glioma cases.
5. It is less likely to be a simple repackaging of the D1/Kaggle/Figshare image pool.
6. It may support stronger publication-grade dataset-shift analysis.

## Major Limitation

D3A does not directly match the D1 four-class classification task.

D1 classes:

- glioma
- meningioma
- pituitary
- notumor

D3A expected class structure:

- diffuse glioma cases only

Therefore, D3A cannot be used naively as a four-class external test set.

## Possible Experimental Uses

### Option 1 ? Glioma-vs-non-glioma confidence stress test

Use D1-trained four-class model on D3A glioma cases and examine whether the model assigns high confidence to the glioma class.

Potential output:

- proportion predicted as glioma
- confidence distribution for glioma predictions
- misclassification distribution
- entropy / uncertainty on D3A images

Limitation:

D3A has no meningioma, pituitary, or notumor cases, so this is not full four-class external validation.

### Option 2 ? Domain-shift confidence audit

Use D3A as an out-of-distribution or domain-shift set relative to D1.

Potential output:

- confidence distribution
- entropy
- max softmax probability
- calibrated confidence behaviour
- whether model remains overconfident under domain shift

Limitation:

This evaluates reliability under shift, not standard classification accuracy across four classes.

### Option 3 ? Future glioma-only sub-study

Restrict the research question to glioma-focused reliability, possibly comparing D1 glioma images against D3A glioma cases.

Potential output:

- glioma detection reliability
- confidence shift between public 2D benchmark gliomas and TCIA gliomas

Limitation:

This would be a secondary analysis, not the main four-class experiment.

## Preliminary Decision

D3A is a strong candidate for domain-shift and glioma-focused external reliability analysis.

D3A is not suitable as a direct four-class external validation dataset.

## Required Checks Before Use

Before using D3A in experiments, the following must be completed:

1. Verify download/access method.
2. Document TCIA access and citation requirements.
3. Document dataset folder structure after download.
4. Create an acquisition log.
5. Create a D3A manifest.
6. Determine image format and preprocessing route.
7. Decide whether 2D slice extraction is required.
8. Define the label-mapping strategy.
9. Run D1-vs-D3A overlap checks if extracted images are comparable.
10. Write a D3A usage decision document.

## Important Risk

D3A may require non-trivial preprocessing because TCIA datasets are commonly distributed as DICOM studies rather than simple class-labelled JPEG folders.

This is scientifically stronger but technically harder than Kaggle image-folder datasets.

## Current Status

Candidate documented.

No data downloaded yet.

## Next Step

Verify TCIA download method and decide whether D3A acquisition is feasible within the project timeline.
