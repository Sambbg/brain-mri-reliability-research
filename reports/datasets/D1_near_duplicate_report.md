# D1 Near-Duplicate Report

## Input

- Input manifest: `data/processed/D1_manifest_deduplicated_phash.csv`
- Rows compared: 7013
- pHash Hamming distance threshold: <= 4

## Summary

- Near-duplicate pairs found: 5125
- Cross-split near-duplicate pairs: 1926
- Cross-class near-duplicate pairs: 46

## Distance Counts

- Distance 0: 1447 pairs
- Distance 2: 1750 pairs
- Distance 4: 1928 pairs

## Interpretation

Cross-split near-duplicates were detected. This is a serious leakage warning because visually similar images may appear in both training and testing splits. These pairs should be manually reviewed before using the original split.

Cross-class near-duplicates were detected. These may indicate label noise, visual hash collisions, or genuinely similar images across classes. Manual review is required.

## Example Near-Duplicate Pairs

### Pair 1

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_641.jpg`
- B: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_310.jpg`

### Pair 2

- Distance: 2
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_641.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1026.jpg`

### Pair 3

- Distance: 0
- A: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_381.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_937.jpg`

### Pair 4

- Distance: 0
- A: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_381.jpg`
- B: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_3.jpg`

### Pair 5

- Distance: 2
- A: `Testing` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Testing/meningioma/Te-aug-me_42.jpg`
- B: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-aug-me_11.jpg`

### Pair 6

- Distance: 4
- A: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_370.jpg`
- B: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_730.jpg`

### Pair 7

- Distance: 4
- A: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_993.jpg`
- B: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_1325.jpg`

### Pair 8

- Distance: 4
- A: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_993.jpg`
- B: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_869.jpg`

### Pair 9

- Distance: 4
- A: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_993.jpg`
- B: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_273.jpg`

### Pair 10

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1157.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_631.jpg`

### Pair 11

- Distance: 2
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1157.jpg`
- B: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_305.jpg`

### Pair 12

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1157.jpg`
- B: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_257.jpg`

### Pair 13

- Distance: 2
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1157.jpg`
- B: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_15.jpg`

### Pair 14

- Distance: 2
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1157.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_309.jpg`

### Pair 15

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_386.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_347.jpg`

### Pair 16

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_386.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_365.jpg`

### Pair 17

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_386.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1203.jpg`

### Pair 18

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_386.jpg`
- B: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_134.jpg`

### Pair 19

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_386.jpg`
- B: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_58.jpg`

### Pair 20

- Distance: 2
- A: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_154.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_120.jpg`

### Pair 21

- Distance: 0
- A: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_154.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_971.jpg`

### Pair 22

- Distance: 2
- A: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_154.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_850.jpg`

### Pair 23

- Distance: 4
- A: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_332.jpg`
- B: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_629.jpg`

### Pair 24

- Distance: 4
- A: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_332.jpg`
- B: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_327.jpg`

### Pair 25

- Distance: 0
- A: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_37.jpg`
- B: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_73.jpg`

### Pair 26

- Distance: 0
- A: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_37.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_311.jpg`

### Pair 27

- Distance: 2
- A: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_37.jpg`
- B: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_302.jpg`

### Pair 28

- Distance: 2
- A: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_37.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1064.jpg`

### Pair 29

- Distance: 0
- A: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_37.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_742.jpg`

### Pair 30

- Distance: 2
- A: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_37.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_762.jpg`

### Pair 31

- Distance: 2
- A: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-aug-me_22.jpg`
- B: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_425.jpg`

### Pair 32

- Distance: 4
- A: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_493.jpg`
- B: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_475.jpg`

### Pair 33

- Distance: 4
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_590.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1231.jpg`

### Pair 34

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_590.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_285.jpg`

### Pair 35

- Distance: 4
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_590.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1074.jpg`

### Pair 36

- Distance: 4
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_590.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_578.jpg`

### Pair 37

- Distance: 4
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_590.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1221.jpg`

### Pair 38

- Distance: 4
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_590.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_55.jpg`

### Pair 39

- Distance: 4
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_590.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_398.jpg`

### Pair 40

- Distance: 4
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_590.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1199.jpg`

### Pair 41

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_982.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_724.jpg`

### Pair 42

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_982.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_542.jpg`

### Pair 43

- Distance: 4
- A: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1325.jpg`
- B: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_460.jpg`

### Pair 44

- Distance: 4
- A: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1325.jpg`
- B: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_593.jpg`

### Pair 45

- Distance: 4
- A: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_1203.jpg`
- B: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_1013.jpg`

### Pair 46

- Distance: 4
- A: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_881.jpg`
- B: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_809.jpg`

### Pair 47

- Distance: 4
- A: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_207.jpg`
- B: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_735.jpg`

### Pair 48

- Distance: 4
- A: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_294.jpg`
- B: `Testing` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Testing/pituitary/Te-pi_83.jpg`

### Pair 49

- Distance: 4
- A: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_294.jpg`
- B: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_131.jpg`

### Pair 50

- Distance: 4
- A: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_294.jpg`
- B: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1162.jpg`

### Pair 51

- Distance: 4
- A: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_1193.jpg`
- B: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_618.jpg`

### Pair 52

- Distance: 2
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_632.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_417.jpg`

### Pair 53

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_632.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_263.jpg`

### Pair 54

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_632.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_22.jpg`

### Pair 55

- Distance: 2
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_632.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1358.jpg`

### Pair 56

- Distance: 2
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_632.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_162.jpg`

### Pair 57

- Distance: 2
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_632.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_853.jpg`

### Pair 58

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_170.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_929.jpg`

### Pair 59

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_170.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_117.jpg`

### Pair 60

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_170.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_687.jpg`

### Pair 61

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_170.jpg`
- B: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_228.jpg`

### Pair 62

- Distance: 4
- A: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_942.jpg`
- B: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1173.jpg`

### Pair 63

- Distance: 4
- A: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_942.jpg`
- B: `Testing` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Testing/pituitary/Te-pi_3.jpg`

### Pair 64

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_908.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_171.jpg`

### Pair 65

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_908.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_415.jpg`

### Pair 66

- Distance: 4
- A: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_68.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_690.jpg`

### Pair 67

- Distance: 0
- A: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_68.jpg`
- B: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_264.jpg`

### Pair 68

- Distance: 0
- A: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_68.jpg`
- B: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_323.jpg`

### Pair 69

- Distance: 2
- A: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_68.jpg`
- B: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_184.jpg`

### Pair 70

- Distance: 4
- A: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_68.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_355.jpg`

### Pair 71

- Distance: 4
- A: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_68.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1.jpg`

### Pair 72

- Distance: 4
- A: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_68.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_403.jpg`

### Pair 73

- Distance: 2
- A: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_68.jpg`
- B: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_283.jpg`

### Pair 74

- Distance: 4
- A: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_68.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_45.jpg`

### Pair 75

- Distance: 4
- A: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_68.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_227.jpg`

### Pair 76

- Distance: 4
- A: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_68.jpg`
- B: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_338.jpg`

### Pair 77

- Distance: 4
- A: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_1020.jpg`
- B: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_606.jpg`

### Pair 78

- Distance: 4
- A: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_1020.jpg`
- B: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_958.jpg`

### Pair 79

- Distance: 4
- A: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1022.jpg`
- B: `Testing` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Testing/pituitary/Te-pi_51.jpg`

### Pair 80

- Distance: 4
- A: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_273.jpg`
- B: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_796.jpg`

### Pair 81

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1364.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_799.jpg`

### Pair 82

- Distance: 2
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1364.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_50.jpg`

### Pair 83

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1364.jpg`
- B: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_242.jpg`

### Pair 84

- Distance: 2
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1364.jpg`
- B: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_266.jpg`

### Pair 85

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1364.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_876.jpg`

### Pair 86

- Distance: 4
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_61.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_659.jpg`

### Pair 87

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_61.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_748.jpg`

### Pair 88

- Distance: 2
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_61.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1121.jpg`

### Pair 89

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_61.jpg`
- B: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_281.jpg`

### Pair 90

- Distance: 4
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_61.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_484.jpg`

### Pair 91

- Distance: 0
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_61.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1347.jpg`

### Pair 92

- Distance: 2
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_61.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1346.jpg`

### Pair 93

- Distance: 4
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_61.jpg`
- B: `Testing` / `notumor` / `data/raw/D1_nickparvar_kaggle/Testing/notumor/Te-no_45.jpg`

### Pair 94

- Distance: 0
- A: `Testing` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Testing/meningioma/Te-me_158.jpg`
- B: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_1194.jpg`

### Pair 95

- Distance: 2
- A: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_164.jpg`
- B: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_910.jpg`

### Pair 96

- Distance: 2
- A: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_164.jpg`
- B: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_88.jpg`

### Pair 97

- Distance: 4
- A: `Testing` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Testing/pituitary/Te-pi_205.jpg`
- B: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_702.jpg`

### Pair 98

- Distance: 4
- A: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_1165.jpg`
- B: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_1315.jpg`

### Pair 99

- Distance: 4
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1185.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_33.jpg`

### Pair 100

- Distance: 2
- A: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_1185.jpg`
- B: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_390.jpg`

