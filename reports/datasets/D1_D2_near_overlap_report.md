# D1-D2 pHash Near-Overlap Report

## Input

- D1 pHash manifest: `data/processed/D1_manifest_deduplicated_phash.csv`
- D2 pHash manifest: `data/processed/D2_manifest_deduplicated_phash.csv`
- D1 rows compared: 7013
- D2 rows compared: 5950
- pHash Hamming distance threshold: <= 4

## Summary

- Near-overlap pairs found: 7290
- Cross-class near-overlap pairs: 68

## Distance Counts

- Distance 0: 5037 pairs
- Distance 2: 564 pairs
- Distance 4: 1689 pairs

## Interpretation

pHash near-overlap was detected between D1 and D2. This suggests possible visual overlap, reused source images, adjacent slices, or hash collisions. D2 should not be treated as a clean independent external dataset until these overlaps are handled or manually reviewed.

Cross-class near-overlap pairs were detected. These require manual review because they may indicate label inconsistency, visually similar slices, or pHash false positives.

## Example Near-Overlap Pairs

### Pair 1

- Distance: 0
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_1021.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02342_me_sa_t1.jpg`

### Pair 2

- Distance: 0
- D1: `Testing` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Testing/pituitary/Te-pi_96.jpg`
- D2: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00911_pi_co_t1.jpg`

### Pair 3

- Distance: 0
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_370.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01967_me_co_t1.jpg`

### Pair 4

- Distance: 4
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_370.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01968_me_co_t1.jpg`

### Pair 5

- Distance: 0
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_1016.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00232_gl_ax_t1.jpg`

### Pair 6

- Distance: 0
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_836.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00239_gl_ax_t1.jpg`

### Pair 7

- Distance: 0
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_52.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00855_gl_sa_t1.jpg`

### Pair 8

- Distance: 0
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_371.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00866_gl_sa_t1.jpg`

### Pair 9

- Distance: 0
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_993.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00152_gl_ax_t1.jpg`

### Pair 10

- Distance: 4
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_993.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00153_gl_ax_t1.jpg`

### Pair 11

- Distance: 4
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_993.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00154_gl_ax_t1.jpg`

### Pair 12

- Distance: 4
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_993.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01494_me_ax_t1.jpg`

### Pair 13

- Distance: 0
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_785.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02328_me_sa_t1.jpg`

### Pair 14

- Distance: 0
- D1: `Testing` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Testing/pituitary/Te-pi_379.jpg`
- D2: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00831_pi_co_t1.jpg`

### Pair 15

- Distance: 0
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1330.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04842_pi_sa_t1.jpg`

### Pair 16

- Distance: 0
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_1247.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01688_me_co_t1.jpg`

### Pair 17

- Distance: 0
- D1: `Testing` / `glioma` / `data/raw/D1_nickparvar_kaggle/Testing/glioma/Te-gl_320.jpg`
- D2: `test` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/glioma/brisc2025_test_00012_gl_ax_t1.jpg`

### Pair 18

- Distance: 0
- D1: `Testing` / `glioma` / `data/raw/D1_nickparvar_kaggle/Testing/glioma/Te-gl_100.jpg`
- D2: `test` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/glioma/brisc2025_test_00046_gl_ax_t1.jpg`

### Pair 19

- Distance: 0
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_547.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00204_gl_ax_t1.jpg`

### Pair 20

- Distance: 0
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_629.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04623_pi_sa_t1.jpg`

### Pair 21

- Distance: 0
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_332.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00393_gl_ax_t1.jpg`

### Pair 22

- Distance: 4
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_332.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00391_gl_ax_t1.jpg`

### Pair 23

- Distance: 4
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_332.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00392_gl_ax_t1.jpg`

### Pair 24

- Distance: 0
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1302.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03564_pi_ax_t1.jpg`

### Pair 25

- Distance: 2
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-aug-me_22.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02403_me_sa_t1.jpg`

### Pair 26

- Distance: 0
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_493.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01926_me_co_t1.jpg`

### Pair 27

- Distance: 4
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_493.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01925_me_co_t1.jpg`

### Pair 28

- Distance: 0
- D1: `Testing` / `glioma` / `data/raw/D1_nickparvar_kaggle/Testing/glioma/Te-gl_236.jpg`
- D2: `test` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/glioma/brisc2025_test_00169_gl_sa_t1.jpg`

### Pair 29

- Distance: 0
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_822.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04424_pi_co_t1.jpg`

### Pair 30

- Distance: 0
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1293.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04767_pi_sa_t1.jpg`

### Pair 31

- Distance: 0
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1325.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04585_pi_sa_t1.jpg`

### Pair 32

- Distance: 4
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1325.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04586_pi_sa_t1.jpg`

### Pair 33

- Distance: 4
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1325.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04545_pi_sa_t1.jpg`

### Pair 34

- Distance: 0
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_440.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01705_me_co_t1.jpg`

### Pair 35

- Distance: 0
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_45.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00544_gl_co_t1.jpg`

### Pair 36

- Distance: 0
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_1203.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01334_me_ax_t1.jpg`

### Pair 37

- Distance: 4
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_1203.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01333_me_ax_t1.jpg`

### Pair 38

- Distance: 0
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_881.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04539_pi_sa_t1.jpg`

### Pair 39

- Distance: 4
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_881.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04541_pi_sa_t1.jpg`

### Pair 40

- Distance: 0
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_207.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01322_me_ax_t1.jpg`

### Pair 41

- Distance: 4
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_207.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01323_me_ax_t1.jpg`

### Pair 42

- Distance: 0
- D1: `Testing` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Testing/pituitary/Te-pi_313.jpg`
- D2: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00846_pi_co_t1.jpg`

### Pair 43

- Distance: 0
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_294.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03745_pi_ax_t1.jpg`

### Pair 44

- Distance: 4
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_294.jpg`
- D2: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00750_pi_ax_t1.jpg`

### Pair 45

- Distance: 4
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_294.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03746_pi_ax_t1.jpg`

### Pair 46

- Distance: 4
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_294.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03744_pi_ax_t1.jpg`

### Pair 47

- Distance: 0
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_544.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02190_me_sa_t1.jpg`

### Pair 48

- Distance: 0
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_1193.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01977_me_co_t1.jpg`

### Pair 49

- Distance: 4
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_1193.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01976_me_co_t1.jpg`

### Pair 50

- Distance: 0
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_216.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00791_gl_co_t1.jpg`

### Pair 51

- Distance: 0
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_205.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00893_gl_sa_t1.jpg`

### Pair 52

- Distance: 0
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_942.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03685_pi_ax_t1.jpg`

### Pair 53

- Distance: 4
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_942.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03684_pi_ax_t1.jpg`

### Pair 54

- Distance: 4
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_942.jpg`
- D2: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00730_pi_ax_t1.jpg`

### Pair 55

- Distance: 0
- D1: `Testing` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Testing/meningioma/Te-me_268.jpg`
- D2: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00538_me_sa_t1.jpg`

### Pair 56

- Distance: 0
- D1: `Testing` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Testing/pituitary/Te-pi_303.jpg`
- D2: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00797_pi_ax_t1.jpg`

### Pair 57

- Distance: 0
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_57.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00899_gl_sa_t1.jpg`

### Pair 58

- Distance: 0
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_723.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00575_gl_co_t1.jpg`

### Pair 59

- Distance: 0
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_1145.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02085_me_sa_t1.jpg`

### Pair 60

- Distance: 0
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_1020.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00882_gl_sa_t1.jpg`

### Pair 61

- Distance: 4
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_1020.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00883_gl_sa_t1.jpg`

### Pair 62

- Distance: 4
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_1020.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00881_gl_sa_t1.jpg`

### Pair 63

- Distance: 0
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1022.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03804_pi_ax_t1.jpg`

### Pair 64

- Distance: 4
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1022.jpg`
- D2: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00769_pi_ax_t1.jpg`

### Pair 65

- Distance: 0
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_273.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00692_gl_co_t1.jpg`

### Pair 66

- Distance: 4
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_273.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00693_gl_co_t1.jpg`

### Pair 67

- Distance: 0
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_167.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04193_pi_co_t1.jpg`

### Pair 68

- Distance: 0
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_341.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01199_me_ax_t1.jpg`

### Pair 69

- Distance: 0
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_544.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04250_pi_co_t1.jpg`

### Pair 70

- Distance: 0
- D1: `Testing` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Testing/meningioma/Te-me_168.jpg`
- D2: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00471_me_co_t1.jpg`

### Pair 71

- Distance: 0
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_1244.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01550_me_ax_t1.jpg`

### Pair 72

- Distance: 0
- D1: `Testing` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Testing/meningioma/Te-me_158.jpg`
- D2: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00297_me_ax_t1.jpg`

### Pair 73

- Distance: 0
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_21.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00177_gl_ax_t1.jpg`

### Pair 74

- Distance: 0
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_164.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04231_pi_co_t1.jpg`

### Pair 75

- Distance: 2
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_164.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04230_pi_co_t1.jpg`

### Pair 76

- Distance: 2
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_164.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04232_pi_co_t1.jpg`

### Pair 77

- Distance: 0
- D1: `Testing` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Testing/pituitary/Te-pi_205.jpg`
- D2: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00906_pi_co_t1.jpg`

### Pair 78

- Distance: 4
- D1: `Testing` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Testing/pituitary/Te-pi_205.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04449_pi_co_t1.jpg`

### Pair 79

- Distance: 4
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_1165.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00447_gl_co_t1.jpg`

### Pair 80

- Distance: 0
- D1: `Testing` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Testing/pituitary/Te-pi_168.jpg`
- D2: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00827_pi_co_t1.jpg`

### Pair 81

- Distance: 0
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_233.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01841_me_co_t1.jpg`

### Pair 82

- Distance: 0
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_740.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00422_gl_co_t1.jpg`

### Pair 83

- Distance: 0
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_823.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01697_me_co_t1.jpg`

### Pair 84

- Distance: 0
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_250.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_01009_gl_sa_t1.jpg`

### Pair 85

- Distance: 0
- D1: `Testing` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Testing/meningioma/Te-me_13.jpg`
- D2: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00552_me_sa_t1.jpg`

### Pair 86

- Distance: 0
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_330.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04608_pi_sa_t1.jpg`

### Pair 87

- Distance: 0
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_146.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03961_pi_ax_t1.jpg`

### Pair 88

- Distance: 0
- D1: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_686.jpg`
- D2: `train` / `notumor` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/no_tumor/brisc2025_train_02832_no_co_t1.jpg`

### Pair 89

- Distance: 0
- D1: `Testing` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Testing/meningioma/Te-me_166.jpg`
- D2: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00545_me_sa_t1.jpg`

### Pair 90

- Distance: 0
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1345.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04537_pi_sa_t1.jpg`

### Pair 91

- Distance: 0
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_873.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02228_me_sa_t1.jpg`

### Pair 92

- Distance: 0
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_1355.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00093_gl_ax_t1.jpg`

### Pair 93

- Distance: 2
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_1355.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00094_gl_ax_t1.jpg`

### Pair 94

- Distance: 0
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1326.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04579_pi_sa_t1.jpg`

### Pair 95

- Distance: 0
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_178.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04196_pi_co_t1.jpg`

### Pair 96

- Distance: 0
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_641.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02417_me_sa_t1.jpg`

### Pair 97

- Distance: 4
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_641.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02416_me_sa_t1.jpg`

### Pair 98

- Distance: 0
- D1: `Testing` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Testing/pituitary/Te-pi_395.jpg`
- D2: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00705_pi_ax_t1.jpg`

### Pair 99

- Distance: 0
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1319.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04443_pi_co_t1.jpg`

### Pair 100

- Distance: 4
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1319.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04441_pi_co_t1.jpg`

