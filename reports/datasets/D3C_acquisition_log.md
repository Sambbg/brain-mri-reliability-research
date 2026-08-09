# D3C Acquisition Log - UPENN-GBM Selected Series

## Acquisition Date
2026-08-09T23:26:31

## Dataset
UPENN-GBM

## Dataset Role
Glioma-focused external domain-shift candidate. This dataset is not a direct four-class external validation dataset for D1.

## Collection
`UPENN-GBM`

## Local Raw Path
`data/raw/D3C_upenn_gbm`

## Download Method
Downloaded selected SeriesInstanceUIDs using `tcia_utils.nbia.downloadSeries`.

```python
nbia.downloadSeries(series_uids, input_type='list', path='data/raw/D3C_upenn_gbm')
```

## Selection Rule
This script performs no selection of its own. It downloads exactly the SeriesInstanceUIDs listed in `reports/datasets/d3c_upenn_gbm_series_selection/selected_series_one_per_patient.csv`, which is produced by `src/data/select_d3c_upenn_gbm_series.py` according to `reports/datasets/D3C_sequence_selection_protocol.md`.

Priority applied by the selection step:

1. Preferred T1 post-contrast / contrast-enhanced anatomical series.
2. Secondary non-contrast T1 anatomical series.

## Selected Series Summary

- Selection manifest: `reports/datasets/d3c_upenn_gbm_series_selection/selected_series_one_per_patient.csv`
- Selected patients: 614
- Selected series: 614
- Series present on disk after download: 614
- Failed series: 0

## Selected Category Counts

| Category | Count |
|---|---:|
| preferred_t1_postcontrast | 568 |
| secondary_t1 | 46 |

## Download Metadata

- Download metadata rows: 614
- Download metadata file: `reports/datasets/d3c_selected_series_download/download_metadata.csv`

## Download Failures

None. All 614 selected series are present on disk, so the downloaded cohort matches the selected cohort exactly.

## Important Limitation

D3C contains glioma cases only. It must not be used to claim full four-class external validation. It will be used only for glioma-focused domain-shift confidence analysis.
