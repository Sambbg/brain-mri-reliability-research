# D3C Skull-Stripping Audit

Generated: 2026-08-10T02:30:09

## Question

The project recorded D3C as 100 per cent Processed_CaPTk and treated skull stripping as a cohort-wide confound. A visual check of `UPENN-GBM-00331` showed intact skull, scalp and orbits. This audit tests, quantitatively and cohort-wide, whether D3C images retain extracranial anatomy.

## Method

Skull stripping leaves a hard mask boundary: beyond the brain surface every pixel is exactly zero and no bright tissue remains. An intact head on T1 shows a bright scalp-fat ring outside a darker skull layer.

The primary measurement is radial, taken about the centroid of the non-zero region and scaled by that region's own 99th-percentile radius, so it is independent of image size, head size, and whether the head reaches the image border:

- **Air exactly zero**: among pixels below an Otsu threshold, the fraction that are exactly zero. Skull stripping is a masking operation, so a stripped image has an air region of exactly zero, while an unstripped acquisition carries genuine noise there. This is the decisive test.
- **Corner non-zero fraction**: the same question asked of the four image corners, independent of any threshold.
- **Bright outer fraction**: pixels between 0.75 and 1.10 of the tissue radius that exceed the brain-core median. On T1 the scalp fat outside the skull is brighter than brain, so this is the anatomical corroboration.

A first attempt scaled the radial annulus by the *non-zero* radius rather than by an Otsu tissue radius. Background noise made that mask reach the image corners, so the annulus sampled air rather than scalp and the metric was uninformative for both cohorts. It was replaced before any conclusion was drawn.

Corner and border-band statistics are reported as secondary evidence only: a border band is uninformative when the head does not reach the image edge.

An image counts as *background masked*, and so consistent with skull stripping, when its air region is at least 98% exactly zero and its corners at most 2% non-zero. Anything else retains extracranial signal, as does any image with at least 5% of outer pixels brighter than the brain core. Distributions are given below so the conclusion can be checked without relying on those thresholds.

## Samples

- D3C: 40 series sampled at random (seed 20260810) from the analysis cohort, central slice (rank 3) of each. `UPENN-GBM-00331` is included by construction.
- D3C source DICOM: the same 40 slices read from the source DICOM and normalised identically to the conversion, to rule out the PNG conversion as the cause.
- D1: 40 glioma images sampled at random from the deduplicated manifest, matched on class because D3C is glioma-only.

## Headline Result

| Sample | Retaining extracranial anatomy | of n | Share |
|---|---:|---:|---:|
| D3C, converted PNG | 40 | 40 | 1.0000 |
| D3C, source DICOM | 40 | 40 | 1.0000 |
| D1 glioma | 40 | 40 | 1.0000 |

## Metric Distributions

Median, with interquartile range and full range.

| Metric | D3C PNG | D3C DICOM | D1 |
|---|---|---|---|
| Air region exactly zero (1.0 = masked) | 0.262 [0.197-0.332] (0.122-0.685) | 0.262 [0.197-0.332] (0.122-0.685) | 0.373 [0.073-0.451] (0.049-0.839) |
| Corner non-zero fraction | 0.540 [0.449-0.608] (0.000-0.912) | 0.540 [0.449-0.608] (0.000-0.912) | 0.280 [0.000-0.862] (0.000-0.922) |
| Outer pixels brighter than brain core | 0.256 [0.224-0.304] (0.054-0.367) | 0.256 [0.224-0.304] (0.054-0.367) | 0.198 [0.137-0.233] (0.052-0.379) |
| Fraction of exactly-zero pixels | 0.145 [0.120-0.183] (0.062-0.440) | 0.145 [0.120-0.183] (0.062-0.440) | 0.233 [0.044-0.305] (0.025-0.443) |
| Border band 99th percentile intensity | 17.500 [12.000-139.000] (3.000-239.000) | 17.500 [12.000-139.000] (3.000-239.000) | 36.000 [3.000-86.250] (1.000-255.000) |

## The Series That Prompted This: UPENN-GBM-00331

| Source | Air exactly zero | Corner non-zero | Bright outer | Verdict |
|---|---:|---:|---:|---|
| converted PNG | 0.551 | 0.018 | 0.226 | retains extracranial |
| source DICOM | 0.551 | 0.018 | 0.226 | retains extracranial |

## Interpretation

D3C images retain extracranial anatomy cohort-wide. The `Processed_CaPTk` label does not imply skull stripping here: CaPTk preprocessing covers reorientation, co-registration and resampling, and the stripping step evidently was not applied to the DICOM series distributed in this collection. The source DICOM measurements match the converted PNGs, so this is a property of the data and not of the conversion.

**The skull-stripping confound recorded for D3C is not supported by the data and should be withdrawn** from CLAUDE.md, SESSION_NOTES.md and any manuscript text that repeats it. D3C and D1 should be compared on the measurements above rather than on the assumption.

## Limitations

- These are intensity and geometry proxies, not a segmentation. They establish whether tissue exists beyond the brain surface, not what that tissue is.
- The samples are 40 series and 40 images. They are adequate for a cohort-wide qualitative claim only if the effect is close to uniform, which the ranges above allow the reader to judge.
- D1 images are lossy JPEGs of unknown provenance and prior processing; a difference between D1 and D3C on these metrics is not by itself evidence about acquisition.
- Per-image values are in `reports/datasets/D3C_skull_stripping_audit_measurements.csv`.
