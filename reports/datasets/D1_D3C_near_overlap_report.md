# D1-D3C pHash Near-Overlap Report

## Input

- D1 pHash manifest: `data\processed\D1_manifest_deduplicated_phash.csv`
- D3C pHash manifest: `data\processed\D3C_selected_slices_manifest_phash.csv`
- D1 rows compared: 7013
- D3C rows compared: 2845
- Total comparisons: 19951985
- pHash Hamming distance threshold: <= 4

## Summary

- Near-overlap pairs found: 7
- Cross-class near-overlap pairs: 0
- Output CSV: `reports\datasets\D1_D3C_near_overlap_pairs.csv`

## Distance Counts

- Distance 2: 2 pairs
- Distance 4: 5 pairs

## Interpretation

pHash near-overlap was detected between D1 and D3C. These pairs may represent visual similarity, hash collisions, shared source images, or similar anatomical slices. Manual review is required before making strong external-domain claims.

D3C remains a glioma-focused domain-shift dataset, not a full four-class external validation dataset.

## Example Near-Overlap Pairs

### Pair 1

- Distance: 2
- D1: `Training` / `glioma` / `data\raw\D1_nickparvar_kaggle\Training\glioma\Tr-gl_1089.jpg`
- D3C: `UPENN-GBM-00331` / `AX T1 MPRAGE ISOTROPIC: Processed_CaPTk` / `data\processed\D3C_upenn_gbm_selected_slices\UPENN-GBM-00331\UPENN-GBM-00331__353321641459__central01_idx0094.png`
- Cross-class pair: `False`

### Pair 2

- Distance: 2
- D1: `Training` / `glioma` / `data\raw\D1_nickparvar_kaggle\Training\glioma\Tr-gl_827.jpg`
- D3C: `UPENN-GBM-00331` / `AX T1 MPRAGE ISOTROPIC: Processed_CaPTk` / `data\processed\D3C_upenn_gbm_selected_slices\UPENN-GBM-00331\UPENN-GBM-00331__353321641459__central01_idx0094.png`
- Cross-class pair: `False`

### Pair 4

- Distance: 4
- D1: `Training` / `glioma` / `data\raw\D1_nickparvar_kaggle\Training\glioma\Tr-gl_1208.jpg`
- D3C: `UPENN-GBM-00281` / `AX T1 MPRAGE ISOTROPIC: Processed_CaPTk` / `data\processed\D3C_upenn_gbm_selected_slices\UPENN-GBM-00281\UPENN-GBM-00281__358075619439__central01_idx0094.png`
- Cross-class pair: `False`

### Pair 5

- Distance: 4
- D1: `Training` / `glioma` / `data\raw\D1_nickparvar_kaggle\Training\glioma\Tr-gl_1208.jpg`
- D3C: `UPENN-GBM-00281` / `AX T1 MPRAGE ISOTROPIC: Processed_CaPTk` / `data\processed\D3C_upenn_gbm_selected_slices\UPENN-GBM-00281\UPENN-GBM-00281__358075619439__central02_idx0095.png`
- Cross-class pair: `False`

### Pair 6

- Distance: 4
- D1: `Training` / `glioma` / `data\raw\D1_nickparvar_kaggle\Training\glioma\Tr-gl_1208.jpg`
- D3C: `UPENN-GBM-00281` / `AX T1 MPRAGE ISOTROPIC: Processed_CaPTk` / `data\processed\D3C_upenn_gbm_selected_slices\UPENN-GBM-00281\UPENN-GBM-00281__358075619439__central04_idx0097.png`
- Cross-class pair: `False`

### Pair 7

- Distance: 4
- D1: `Training` / `glioma` / `data\raw\D1_nickparvar_kaggle\Training\glioma\Tr-gl_1208.jpg`
- D3C: `UPENN-GBM-00281` / `AX T1 MPRAGE ISOTROPIC: Processed_CaPTk` / `data\processed\D3C_upenn_gbm_selected_slices\UPENN-GBM-00281\UPENN-GBM-00281__358075619439__central05_idx0098.png`
- Cross-class pair: `False`

### Pair 3

- Distance: 4
- D1: `Training` / `glioma` / `data\raw\D1_nickparvar_kaggle\Training\glioma\Tr-gl_127.jpg`
- D3C: `UPENN-GBM-00331` / `AX T1 MPRAGE ISOTROPIC: Processed_CaPTk` / `data\processed\D3C_upenn_gbm_selected_slices\UPENN-GBM-00331\UPENN-GBM-00331__353321641459__central01_idx0094.png`
- Cross-class pair: `False`

