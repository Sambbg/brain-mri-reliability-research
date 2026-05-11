# D3B Sequence Selection Protocol ? ICDC-Glioma

## Purpose

This document defines how MRI series will be selected from the ICDC-Glioma TCIA collection before any DICOM images are downloaded or used for analysis.

The purpose is to avoid uncontrolled data acquisition and prevent biased or irreproducible slice selection.

## Dataset Candidate

D3B ? ICDC-Glioma

## Current Metadata Probe Result

A TCIA/NBIA metadata probe using `tcia-utils` returned:

| Item | Count |
|---|---:|
| Patients | 57 |
| Studies | 58 |
| Series | 650 |

All returned series had modality `MR`.

## Role of D3B in This Project

D3B is not a direct four-class external validation dataset.

D1 classes:

- glioma
- meningioma
- pituitary
- notumor

D3B is glioma-focused. Therefore, D3B can support:

1. Glioma-focused external domain-shift evaluation.
2. Confidence analysis of a D1-trained four-class classifier on clinically sourced glioma MRI.
3. Out-of-distribution or domain-shift reliability testing.
4. A secondary glioma-only analysis.

D3B must not be presented as a clean four-class external validation dataset.

## Core Selection Principle

Only clinically meaningful brain MRI series that are reasonably comparable to D1/D2 image appearance should be considered.

Because D1 consists of 2D brain MRI slices from public benchmark folders, the closest D3B sequence category is likely T1-weighted post-contrast / contrast-enhanced T1 MRI.

## Preferred Series Types

Prefer series descriptions containing terms such as:

- T1+C
- T1 +C
- T1 POST
- T1 POST CONTRAST
- T1 CE
- T1C
- T1 GD
- MPRAGE +C
- MP RAGE +C
- MP RAGE FS +C
- RAGE +C
- POST
- Ax_T1_fl2d post
- Sag_T1_fl2d post

These are likely to represent T1-weighted contrast-enhanced imaging or post-contrast anatomical imaging.

## Secondary Acceptable Series Types

If post-contrast T1 is unavailable for a patient, consider non-contrast T1 anatomical series:

- T1 Axial
- T1 Sagittal
- T1 Coronal
- T1 FLAIR
- T1 SE
- T1 TRANS
- T1 SAG
- T1 AX

These should be marked separately from post-contrast series.

## Excluded Series Types

Exclude series that are unlikely to be comparable to D1 or are not suitable for simple 2D classification benchmarking:

### Localizer / Scout
- localizer
- scout
- locator
- 3 plane locator
- BRAIN/SCOUT

### Diffusion / ADC / Trace
- DWI
- ADC
- TRACE
- DIFFUSION
- DTI

### T2 / FLAIR-only
- T2
- FLAIR
- T2 FLAIR
- T2STAR
- GRE T2
- PD

These may be clinically useful but should not be mixed with T1-based images in the first D3B evaluation.

### Spine or Non-Brain
- spine
- cervical
- lumbar
- thoracic

### Derived or Secondary Captures
- screen save
- created from
- reformatted
- secondary capture
- subtraction-only if original post-contrast is available

## Patient-Level Rule

To prevent one patient with many series from dominating the evaluation, select at most one primary eligible series per patient for the first D3B experiment.

Priority order:

1. Post-contrast T1 / T1+C / MPRAGE +C
2. Non-contrast T1 anatomical
3. Exclude patient if no eligible T1-like series exists

## Slice Selection Rule

The first D3B experiment should not use every slice from every series blindly.

Possible slice selection strategies:

### Option A ? Middle-slice selection
Select a fixed number of central slices from each eligible series.

Example:

- choose 5 central slices per selected series

Strength:
- simple and reproducible

Weakness:
- may miss tumour-containing slices

### Option B ? Entropy/tissue-content selection
Select slices with the highest non-background content or image entropy.

Strength:
- more likely to select diagnostically meaningful slices

Weakness:
- more complex and may introduce preprocessing bias

### Option C ? Manual tumour-region selection
Manually inspect and select tumour-visible slices.

Strength:
- clinically meaningful

Weakness:
- not scalable and introduces human selection bias

## Initial Decision

For the first reproducible D3B probe, use Option A:

- one eligible T1 post-contrast series per patient where available;
- 5 central slices per selected series;
- save selected slices as reproducible PNG/JPG images;
- record the original PatientID, StudyInstanceUID, SeriesInstanceUID, slice index, and source DICOM filename.

## Required Manifest Fields

The D3B manifest must include:

- dataset_id
- patient_id
- study_instance_uid
- series_instance_uid
- modality
- series_description
- selected_sequence_category
- slice_index
- total_slices_in_series
- filepath
- source_dicom_path
- image_width
- image_height
- file_size_bytes
- sha256
- phash
- ahash
- dhash
- label
- label_source

## Label Strategy

For the initial D3B experiment, all selected images should be labelled as:

- glioma

Label source:

- collection-level diagnosis / glioma collection identity

This is not equivalent to slice-level tumour annotation. The limitation must be explicitly documented.

## Evaluation Strategy

D3B should be used to answer:

> When a D1-trained four-class model is applied to clinically sourced glioma MRI slices, how often does it predict glioma, and how confident is it?

Metrics:

- proportion predicted as glioma
- mean glioma probability
- mean maximum softmax confidence
- entropy
- prediction distribution across all four D1 classes
- raw vs temperature-scaled confidence comparison

Avoid reporting ordinary four-class accuracy because D3B does not contain all four D1 classes.

## Risks

1. D3B is glioma-only.
2. DICOM preprocessing choices may affect image appearance.
3. Series descriptions are heterogeneous.
4. Slice-level tumour visibility is not guaranteed.
5. Collection-level glioma labels are not the same as image-level tumour labels.
6. Results should be interpreted as domain-shift confidence analysis, not complete diagnostic validation.

## Next Step

Create a script that reads the ICDC-Glioma series metadata and identifies eligible T1/post-contrast candidate series using the rules in this protocol.
