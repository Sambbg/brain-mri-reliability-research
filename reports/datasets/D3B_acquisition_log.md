# D3B Acquisition Log ? ICDC-Glioma Selected Series

## Acquisition Date
2026-05-12T16:10:00

## Dataset
ICDC-Glioma

## Dataset Role
Glioma-focused external domain-shift candidate. This dataset is not a direct four-class external validation dataset for D1.

## Collection
`ICDC-Glioma`

## Local Raw Path
`data/raw/D3B_icdc_glioma`

## Download Method
Downloaded selected SeriesInstanceUIDs using `tcia_utils.nbia.downloadSeries`.

```python
nbia.downloadSeries(series_uids, input_type='list', path='data/raw/D3B_icdc_glioma')
```

## Selection Rule
At most one eligible T1-like series was selected per patient according to `reports/datasets/D3B_sequence_selection_protocol.md`.

Priority:

1. Preferred T1 post-contrast / contrast-enhanced anatomical series.
2. Secondary non-contrast T1 anatomical series.

## Selected Series Summary

- Selected patients: 53
- Selected series: 53

## Selected Category Counts

| Category | Count |
|---|---:|
| preferred_t1_postcontrast | 28 |
| secondary_t1 | 25 |

## Download Metadata

- Download metadata rows: 53
- Download metadata file: `reports/datasets/d3b_selected_series_download/download_metadata.csv`

## Important Limitation

D3B contains glioma cases only. It must not be used to claim full four-class external validation. It will be used only for glioma-focused domain-shift confidence analysis.
