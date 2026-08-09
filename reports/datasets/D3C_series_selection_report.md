# D3C Series Selection - UPENN-GBM (human)

Selected one T1 series per patient (post-contrast preferred).

## Output Manifest

- Manifest: `reports/datasets/d3c_upenn_gbm_series_selection/selected_series_one_per_patient.csv`
- sha256: `fc6deef35438027d6b76fdc323b5a4d96538312dd2da8f4a93afb40f3488761c`
- Selected series: 614
- Patients covered: 614
- Series returned by TCIA: 3680

This manifest is the single source of truth for the D3C cohort. The download, inspection and conversion steps read it and refuse to process any series it does not list. Quote the sha256 above when reporting D3C results, so the cohort behind a number is verifiable.

## Determinism

The selection does not depend on the order TCIA returns series in:

- Sort keys `PatientID`, `selection_priority`, `ImageCount_numeric` (descending), `SeriesInstanceUID` form a total order, because SeriesInstanceUID is unique per series and is asserted to be so.
- `kind="mergesort"` is a stable sort, so equal keys never permute.
- One row per patient is taken with `drop_duplicates(keep="first")`, which returns whole rows. `groupby().first()` is not used: it takes the first non-null value of each column independently and can compose an output row from several different series.
- Manifest columns are written in a fixed order, so the sha256 depends only on the selected content and not on the key order of the API response.

## Selection Category Counts, All Series

| Category | Count |
|---|---:|
| excluded_dwi_adc | 581 |
| excluded_perfusion | 490 |
| excluded_t2_flair | 1319 |
| preferred_t1_postcontrast | 605 |
| secondary_t1 | 685 |

## Selected Category Counts

| Category | Count |
|---|---:|
| preferred_t1_postcontrast | 568 |
| secondary_t1 | 46 |

## Limitation

D3C contains glioma cases only. It must not be used to claim full four-class external validation.
