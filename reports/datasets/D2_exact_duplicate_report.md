# D2 Exact Duplicate Report

## Input

- Manifest: `data/processed/D2_manifest.csv`
- Total manifest rows: 6000

## Summary

- Unique SHA256 hashes: 5950
- Duplicate hash groups: 46
- Images involved in duplicate groups: 96
- Cross-split duplicate groups: 7
- Cross-class duplicate groups: 0

## Interpretation

Exact duplicate SHA256 hashes were found within D2. These must be investigated before using D2 for external evaluation. Cross-split duplicates are especially serious.

## Cross-Split Duplicate Groups

### Group 1

- SHA256: `960155b05ea8f0ddcbcd3a5e29905c2a4b55832f03e5b7d6491c73955960d278`

- `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01210_me_ax_t1.jpg`
- `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00344_me_ax_t1.jpg`

### Group 2

- SHA256: `f3d00bbb942117c2fb62466414d3c466ca283b678200fe87424e4128b80b2dba`

- `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01304_me_ax_t1.jpg`
- `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00352_me_ax_t1.jpg`

### Group 3

- SHA256: `39f4f7b252d7809d8d3d2e4521607de2195bf0f66c0592587b1cebd632aac640`

- `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03705_pi_ax_t1.jpg`
- `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00737_pi_ax_t1.jpg`

### Group 4

- SHA256: `08690b76457b2b44d58682cece62ec951ef6d30d935ce07df852e97d44434680`

- `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03749_pi_ax_t1.jpg`
- `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00751_pi_ax_t1.jpg`

### Group 5

- SHA256: `3e802dd22f483ce4d442fe2c7f1890c1c810ec8c1131b364fd4e4593bf0f268a`

- `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04176_pi_co_t1.jpg`
- `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04177_pi_co_t1.jpg`
- `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04178_pi_co_t1.jpg`
- `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00825_pi_co_t1.jpg`

### Group 6

- SHA256: `02799f7863d49de182357e72179f3cc4e65e70099355f2d5aa2e39d356e492d9`

- `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04194_pi_co_t1.jpg`
- `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00827_pi_co_t1.jpg`

### Group 7

- SHA256: `b5e17076d1427e41a618f92bc72100c1be4df26608223512aac51c911ac1eb88`

- `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04218_pi_co_t1.jpg`
- `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00834_pi_co_t1.jpg`

