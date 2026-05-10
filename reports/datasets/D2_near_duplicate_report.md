# D2 Near-Duplicate Report

## Input

- Input manifest: `data/processed/D2_manifest_deduplicated_phash.csv`
- Rows compared: 5950
- pHash Hamming distance threshold: <= 4

## Summary

- Near-duplicate pairs found: 1270
- Cross-split near-duplicate pairs: 419
- Cross-class near-duplicate pairs: 23

## Distance Counts

- Distance 0: 138 pairs
- Distance 2: 290 pairs
- Distance 4: 842 pairs

## Interpretation

Cross-split near-duplicates were detected inside D2. This indicates that the original BRISC train/test split should not be treated as independent. These pairs should be considered leakage risks unless manually reviewed.

Cross-class near-duplicates were detected. These may reflect hash collisions, visually similar slices, or label-quality concerns. Manual review is required before making strong claims.

## Example Near-Duplicate Pairs

### Pair 1

- Distance: 4
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01967_me_co_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01968_me_co_t1.jpg`

### Pair 2

- Distance: 4
- A: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00152_gl_ax_t1.jpg`
- B: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00153_gl_ax_t1.jpg`

### Pair 3

- Distance: 4
- A: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00152_gl_ax_t1.jpg`
- B: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00154_gl_ax_t1.jpg`

### Pair 4

- Distance: 4
- A: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00152_gl_ax_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01494_me_ax_t1.jpg`

### Pair 5

- Distance: 4
- A: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00393_gl_ax_t1.jpg`
- B: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00391_gl_ax_t1.jpg`

### Pair 6

- Distance: 4
- A: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00393_gl_ax_t1.jpg`
- B: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00392_gl_ax_t1.jpg`

### Pair 7

- Distance: 4
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01926_me_co_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01925_me_co_t1.jpg`

### Pair 8

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04585_pi_sa_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04586_pi_sa_t1.jpg`

### Pair 9

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04585_pi_sa_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04545_pi_sa_t1.jpg`

### Pair 10

- Distance: 4
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01334_me_ax_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01333_me_ax_t1.jpg`

### Pair 11

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04539_pi_sa_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04541_pi_sa_t1.jpg`

### Pair 12

- Distance: 4
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01322_me_ax_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01323_me_ax_t1.jpg`

### Pair 13

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03745_pi_ax_t1.jpg`
- B: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00750_pi_ax_t1.jpg`

### Pair 14

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03745_pi_ax_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03746_pi_ax_t1.jpg`

### Pair 15

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03745_pi_ax_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03744_pi_ax_t1.jpg`

### Pair 16

- Distance: 4
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01977_me_co_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01976_me_co_t1.jpg`

### Pair 17

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03685_pi_ax_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03684_pi_ax_t1.jpg`

### Pair 18

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03685_pi_ax_t1.jpg`
- B: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00730_pi_ax_t1.jpg`

### Pair 19

- Distance: 4
- A: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00882_gl_sa_t1.jpg`
- B: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00883_gl_sa_t1.jpg`

### Pair 20

- Distance: 4
- A: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00882_gl_sa_t1.jpg`
- B: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00881_gl_sa_t1.jpg`

### Pair 21

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03804_pi_ax_t1.jpg`
- B: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00769_pi_ax_t1.jpg`

### Pair 22

- Distance: 4
- A: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00692_gl_co_t1.jpg`
- B: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00693_gl_co_t1.jpg`

### Pair 23

- Distance: 2
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04231_pi_co_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04230_pi_co_t1.jpg`

### Pair 24

- Distance: 2
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04231_pi_co_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04232_pi_co_t1.jpg`

### Pair 25

- Distance: 4
- A: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00906_pi_co_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04449_pi_co_t1.jpg`

### Pair 26

- Distance: 4
- A: `train` / `notumor` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/no_tumor/brisc2025_train_03323_no_sa_t1.jpg`
- B: `train` / `notumor` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/no_tumor/brisc2025_train_03284_no_sa_t1.jpg`

### Pair 27

- Distance: 2
- A: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00093_gl_ax_t1.jpg`
- B: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00094_gl_ax_t1.jpg`

### Pair 28

- Distance: 4
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02417_me_sa_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02416_me_sa_t1.jpg`

### Pair 29

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04443_pi_co_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04441_pi_co_t1.jpg`

### Pair 30

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04443_pi_co_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04442_pi_co_t1.jpg`

### Pair 31

- Distance: 2
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01669_me_co_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01658_me_co_t1.jpg`

### Pair 32

- Distance: 0
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01669_me_co_t1.jpg`
- B: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00417_me_co_t1.jpg`

### Pair 33

- Distance: 2
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01669_me_co_t1.jpg`
- B: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00400_me_co_t1.jpg`

### Pair 34

- Distance: 0
- A: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00491_me_sa_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02014_me_sa_t1.jpg`

### Pair 35

- Distance: 4
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02400_me_sa_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02399_me_sa_t1.jpg`

### Pair 36

- Distance: 4
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02400_me_sa_t1.jpg`
- B: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00955_gl_sa_t1.jpg`

### Pair 37

- Distance: 4
- A: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00536_gl_co_t1.jpg`
- B: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00537_gl_co_t1.jpg`

### Pair 38

- Distance: 4
- A: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00797_gl_co_t1.jpg`
- B: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00798_gl_co_t1.jpg`

### Pair 39

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04503_pi_sa_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04504_pi_sa_t1.jpg`

### Pair 40

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04503_pi_sa_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04502_pi_sa_t1.jpg`

### Pair 41

- Distance: 2
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02038_me_sa_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02037_me_sa_t1.jpg`

### Pair 42

- Distance: 2
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02038_me_sa_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02036_me_sa_t1.jpg`

### Pair 43

- Distance: 2
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02038_me_sa_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02039_me_sa_t1.jpg`

### Pair 44

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04822_pi_sa_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04825_pi_sa_t1.jpg`

### Pair 45

- Distance: 4
- A: `train` / `notumor` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/no_tumor/brisc2025_train_02908_no_co_t1.jpg`
- B: `train` / `notumor` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/no_tumor/brisc2025_train_02922_no_co_t1.jpg`

### Pair 46

- Distance: 0
- A: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00398_me_co_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01656_me_co_t1.jpg`

### Pair 47

- Distance: 0
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02010_me_sa_t1.jpg`
- B: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00487_me_sa_t1.jpg`

### Pair 48

- Distance: 0
- A: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00404_me_co_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01661_me_co_t1.jpg`

### Pair 49

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03615_pi_ax_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03616_pi_ax_t1.jpg`

### Pair 50

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04060_pi_co_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04062_pi_co_t1.jpg`

### Pair 51

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04037_pi_co_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04036_pi_co_t1.jpg`

### Pair 52

- Distance: 4
- A: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_01089_gl_sa_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02280_me_sa_t1.jpg`

### Pair 53

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04771_pi_sa_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04772_pi_sa_t1.jpg`

### Pair 54

- Distance: 2
- A: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00134_gl_ax_t1.jpg`
- B: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00133_gl_ax_t1.jpg`

### Pair 55

- Distance: 4
- A: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_01112_gl_sa_t1.jpg`
- B: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_01113_gl_sa_t1.jpg`

### Pair 56

- Distance: 2
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01441_me_ax_t1.jpg`
- B: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00366_me_ax_t1.jpg`

### Pair 57

- Distance: 4
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01441_me_ax_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01413_me_ax_t1.jpg`

### Pair 58

- Distance: 2
- A: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00130_gl_ax_t1.jpg`
- B: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00126_gl_ax_t1.jpg`

### Pair 59

- Distance: 2
- A: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00130_gl_ax_t1.jpg`
- B: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00131_gl_ax_t1.jpg`

### Pair 60

- Distance: 4
- A: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00843_pi_co_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04263_pi_co_t1.jpg`

### Pair 61

- Distance: 4
- A: `train` / `notumor` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/no_tumor/brisc2025_train_03475_no_sa_t1.jpg`
- B: `train` / `notumor` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/no_tumor/brisc2025_train_03537_no_sa_t1.jpg`

### Pair 62

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04496_pi_sa_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04495_pi_sa_t1.jpg`

### Pair 63

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04496_pi_sa_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04497_pi_sa_t1.jpg`

### Pair 64

- Distance: 4
- A: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00072_gl_ax_t1.jpg`
- B: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00073_gl_ax_t1.jpg`

### Pair 65

- Distance: 0
- A: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00323_me_ax_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01253_me_ax_t1.jpg`

### Pair 66

- Distance: 2
- A: `train` / `notumor` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/no_tumor/brisc2025_train_03378_no_sa_t1.jpg`
- B: `train` / `notumor` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/no_tumor/brisc2025_train_03225_no_sa_t1.jpg`

### Pair 67

- Distance: 4
- A: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00984_pi_sa_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04955_pi_sa_t1.jpg`

### Pair 68

- Distance: 4
- A: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00984_pi_sa_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04987_pi_sa_t1.jpg`

### Pair 69

- Distance: 2
- A: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00984_pi_sa_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04950_pi_sa_t1.jpg`

### Pair 70

- Distance: 4
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01276_me_ax_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01280_me_ax_t1.jpg`

### Pair 71

- Distance: 4
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01937_me_co_t1.jpg`
- B: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00459_me_co_t1.jpg`

### Pair 72

- Distance: 0
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02007_me_sa_t1.jpg`
- B: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00484_me_sa_t1.jpg`

### Pair 73

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04867_pi_sa_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04864_pi_sa_t1.jpg`

### Pair 74

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04867_pi_sa_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04865_pi_sa_t1.jpg`

### Pair 75

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04736_pi_sa_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04735_pi_sa_t1.jpg`

### Pair 76

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04003_pi_co_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03970_pi_co_t1.jpg`

### Pair 77

- Distance: 4
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01496_me_ax_t1.jpg`
- B: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00381_me_ax_t1.jpg`

### Pair 78

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04652_pi_sa_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04646_pi_sa_t1.jpg`

### Pair 79

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04739_pi_sa_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04738_pi_sa_t1.jpg`

### Pair 80

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04739_pi_sa_t1.jpg`
- B: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00916_pi_sa_t1.jpg`

### Pair 81

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04739_pi_sa_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04740_pi_sa_t1.jpg`

### Pair 82

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04451_pi_co_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04452_pi_co_t1.jpg`

### Pair 83

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03545_pi_ax_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03546_pi_ax_t1.jpg`

### Pair 84

- Distance: 0
- A: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00263_me_ax_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01262_me_ax_t1.jpg`

### Pair 85

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03604_pi_ax_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03603_pi_ax_t1.jpg`

### Pair 86

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04097_pi_co_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04096_pi_co_t1.jpg`

### Pair 87

- Distance: 2
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02080_me_sa_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02029_me_sa_t1.jpg`

### Pair 88

- Distance: 4
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01178_me_ax_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01177_me_ax_t1.jpg`

### Pair 89

- Distance: 2
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01795_me_co_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01647_me_co_t1.jpg`

### Pair 90

- Distance: 2
- A: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00326_me_ax_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01155_me_ax_t1.jpg`

### Pair 91

- Distance: 4
- A: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00549_gl_co_t1.jpg`
- B: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00550_gl_co_t1.jpg`

### Pair 92

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03847_pi_ax_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03840_pi_ax_t1.jpg`

### Pair 93

- Distance: 4
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01476_me_ax_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01477_me_ax_t1.jpg`

### Pair 94

- Distance: 2
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04958_pi_sa_t1.jpg`
- B: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00987_pi_sa_t1.jpg`

### Pair 95

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04958_pi_sa_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04956_pi_sa_t1.jpg`

### Pair 96

- Distance: 4
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02113_me_sa_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02112_me_sa_t1.jpg`

### Pair 97

- Distance: 4
- A: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00069_gl_ax_t1.jpg`
- B: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00070_gl_ax_t1.jpg`

### Pair 98

- Distance: 2
- A: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02317_me_sa_t1.jpg`
- B: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02316_me_sa_t1.jpg`

### Pair 99

- Distance: 4
- A: `train` / `notumor` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/no_tumor/brisc2025_train_03166_no_sa_t1.jpg`
- B: `train` / `notumor` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/no_tumor/brisc2025_train_03141_no_sa_t1.jpg`

### Pair 100

- Distance: 4
- A: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03634_pi_ax_t1.jpg`
- B: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03635_pi_ax_t1.jpg`

