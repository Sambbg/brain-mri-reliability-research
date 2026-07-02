# D3C Acquisition Log ? UPENN-GBM Selected Series

## Acquisition Date
2026-07-02T18:04:19

## Dataset
UPENN-GBM

## Dataset Role
Glioma-focused external domain-shift candidate. This dataset is not a direct four-class external validation dataset for D1.

## Collection
`UPENN-GBM`

## Local Raw Path
`data\raw\D3C_upenn_gbm`

## Download Method
Downloaded selected SeriesInstanceUIDs using `tcia_utils.nbia.downloadSeries`.

```python
nbia.downloadSeries(series_uids, input_type='list', path='data/raw/D3C_upenn_gbm')
```

## Selection Rule
At most one eligible T1-like series was selected per patient according to `reports/datasets/D3C_sequence_selection_protocol.md`.

Priority:

1. Preferred T1 post-contrast / contrast-enhanced anatomical series.
2. Secondary non-contrast T1 anatomical series.

## Selected Series Summary

- Selected patients: 575
- Selected series: 575

## Selected Category Counts

| Category | Count |
|---|---:|
| preferred_t1_postcontrast | 35 |
| secondary_t1 | 540 |

## Download Metadata

- Download metadata rows: 569
- Download metadata file: `reports\datasets\d3c_selected_series_download\download_metadata.csv`

## Important Limitation

D3C contains glioma cases only. It must not be used to claim full four-class external validation. It will be used only for glioma-focused domain-shift confidence analysis.
