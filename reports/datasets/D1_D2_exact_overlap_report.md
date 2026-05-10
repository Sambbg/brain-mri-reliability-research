# D1-D2 Exact SHA256 Overlap Report

## Input

- D1 manifest: `data/processed/D1_manifest_deduplicated.csv`
- D2 manifest: `data/processed/D2_manifest_deduplicated.csv`
- D1 rows: 7013
- D2 rows: 5950

## Summary

- Shared SHA256 hashes: 4740
- Exact overlap pairs: 4740
- Cross-class exact overlap pairs: 0

## Interpretation

Exact SHA256 overlap was detected between D1 and D2. This means at least some identical files appear in both datasets. D2 must not be treated as a fully independent external dataset unless overlapping images are removed or excluded.

## Example Exact Overlap Pairs

### Pair 1

- SHA256: `000b5af2922fff3ea689f3132b43538ffe9d01a8b9b2a09d4d0aa47ba94cda01`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_1021.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02342_me_sa_t1.jpg`

### Pair 2

- SHA256: `001a7183a8df5218efb182dca749921d7c6c946741f9f4af1cd73602aaf39a9f`
- D1: `Testing` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Testing/pituitary/Te-pi_96.jpg`
- D2: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00911_pi_co_t1.jpg`

### Pair 3

- SHA256: `001e83da30735f4854ad3e2d7f7e55e4f36c1549e907132a8d89252f929182e1`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_370.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01967_me_co_t1.jpg`

### Pair 4

- SHA256: `002f4403eb07288c2ebdffcd4a3247543f5fd976767223c3843e249ebfe45d49`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_1016.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00232_gl_ax_t1.jpg`

### Pair 5

- SHA256: `0031a6f69f5c0eaf538e696764d68923dc1d4514d8fe374ea7dbef85d9d739ca`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_836.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00239_gl_ax_t1.jpg`

### Pair 6

- SHA256: `0034cd2e65db88276e566890683873a175e7b3fc68089dc933a559599fdbee5f`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_52.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00855_gl_sa_t1.jpg`

### Pair 7

- SHA256: `003c315a304e6410f298abbcae5556e62e83f477f4b05e4682b379091ab8226e`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_371.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00866_gl_sa_t1.jpg`

### Pair 8

- SHA256: `00447a5e4dba64bb0e3e97c8c943131b85bd5c27aec22ca12cc3b824f20f53c6`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_993.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00152_gl_ax_t1.jpg`

### Pair 9

- SHA256: `004a43ea02804dc17a75caefa0ff36b7161849acd8f9d3dbdde54d75c1455639`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_785.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02328_me_sa_t1.jpg`

### Pair 10

- SHA256: `004f9655d6baf78b265cc9ae3766e250550d13a82e0405427dfc6fedc53af132`
- D1: `Testing` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Testing/pituitary/Te-pi_379.jpg`
- D2: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00831_pi_co_t1.jpg`

### Pair 11

- SHA256: `004fc7f2f08330c9489e7095ee49b960fbc8c5c50c23855117499271ecc28cc6`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1330.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04842_pi_sa_t1.jpg`

### Pair 12

- SHA256: `008d21cf043b4a4ae6c9e28459818fe93c07df9ff9d52126c9107b22818c0287`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_1247.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01688_me_co_t1.jpg`

### Pair 13

- SHA256: `008f7fea9cbb6d61aa406db657479bf8437355ffff3b894a807c8d7b81d7e628`
- D1: `Testing` / `glioma` / `data/raw/D1_nickparvar_kaggle/Testing/glioma/Te-gl_320.jpg`
- D2: `test` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/glioma/brisc2025_test_00012_gl_ax_t1.jpg`

### Pair 14

- SHA256: `0090827701d28f35c51a3f54f7eea25d866d86909fa491aec8a12fb51c56eeb5`
- D1: `Testing` / `glioma` / `data/raw/D1_nickparvar_kaggle/Testing/glioma/Te-gl_100.jpg`
- D2: `test` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/glioma/brisc2025_test_00046_gl_ax_t1.jpg`

### Pair 15

- SHA256: `009b2b1341b0a533e329f431cd0c9f5b6b8fc774c6123ef359841c6b3890d5a4`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_547.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00204_gl_ax_t1.jpg`

### Pair 16

- SHA256: `009bb0f6f6174828718de2b4566718aabaf61e819e5676b175b04477d9cee02a`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_629.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04623_pi_sa_t1.jpg`

### Pair 17

- SHA256: `00a22f74323aa6ef3bbcd8a7894696d4ba2b1b7ed55b409c48457e07206dfadd`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_332.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00393_gl_ax_t1.jpg`

### Pair 18

- SHA256: `00c30197dc30f7dd8b029ebd3a700d0d63833a434fa54a1fa869c421494a7544`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1302.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03564_pi_ax_t1.jpg`

### Pair 19

- SHA256: `00cdc02ec1dcdaa9a7ddd44fa2a83d09a5aedadbee67bce4ea4109addeb92980`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_493.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01926_me_co_t1.jpg`

### Pair 20

- SHA256: `00ec18489c236cd41b1ad33c09ee73b530b916c2d03bce0c901a415fc75070d2`
- D1: `Testing` / `glioma` / `data/raw/D1_nickparvar_kaggle/Testing/glioma/Te-gl_236.jpg`
- D2: `test` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/glioma/brisc2025_test_00169_gl_sa_t1.jpg`

### Pair 21

- SHA256: `00fe0cad64b7ddabb0a2dd787e6186fcf39d11525969fce54cf7609377bee120`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_822.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04424_pi_co_t1.jpg`

### Pair 22

- SHA256: `0101f4332fd57e4812af6093f471cdfaf9db4bf976192c64fb4f0e169fb15787`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1293.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04767_pi_sa_t1.jpg`

### Pair 23

- SHA256: `010841515b9457161c3065e47b2b983ebf5883edb809e206b1d43a4c745ca8d6`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1325.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04585_pi_sa_t1.jpg`

### Pair 24

- SHA256: `010bc80bb8c8dac8251662c1dd9c23d3a210aff06ed5405503c34f0516e47ce0`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_440.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01705_me_co_t1.jpg`

### Pair 25

- SHA256: `010c57403f89a5c449e1a970875f435b9f2106cf8e8bcef3118849daa4b92cf3`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_45.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00544_gl_co_t1.jpg`

### Pair 26

- SHA256: `01338ffff1ed97698465eef56832b6f1b0c5dee1ca29c5bdee6170e0407ae3de`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_1203.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01334_me_ax_t1.jpg`

### Pair 27

- SHA256: `013fb05dc794ae389ed805767e26a11def0bff389c0e569f868be6ac8fd0a90f`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_881.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04539_pi_sa_t1.jpg`

### Pair 28

- SHA256: `0157ee63732747449bb5170ef1445aa91919c887ee01c866bc24655d464dfd81`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_207.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01322_me_ax_t1.jpg`

### Pair 29

- SHA256: `0162fd9079de0f2b2f6762ecac6fec41946175052bd3f7c2ceda5a08c9f0b64c`
- D1: `Testing` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Testing/pituitary/Te-pi_313.jpg`
- D2: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00846_pi_co_t1.jpg`

### Pair 30

- SHA256: `016b7ee664644ef3718bb33f63ec7e3d8fe9e8e625512ffe11c6ab73cb441494`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_294.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03745_pi_ax_t1.jpg`

### Pair 31

- SHA256: `0188e2a9b5e00ec418360252f5f6680497e439c232904950710eacebc6c19a61`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_544.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02190_me_sa_t1.jpg`

### Pair 32

- SHA256: `018e55314ac60df9796597db3911457bae576cf7faa6fc24fdb9c554ac0b854a`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_1193.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01977_me_co_t1.jpg`

### Pair 33

- SHA256: `018f28db4e60217f7a5dcef786bb91af1c9419493da17bc5ea91df614172e9de`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_216.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00791_gl_co_t1.jpg`

### Pair 34

- SHA256: `01b179180d59fcecce89e0cef642723566a22725b68fe2614112df65086d6fff`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_205.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00893_gl_sa_t1.jpg`

### Pair 35

- SHA256: `01b8c3e1318e688ffb4aa4d83b3ff6aebfffb0b85a00d30589cf8eff2903705f`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_942.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03685_pi_ax_t1.jpg`

### Pair 36

- SHA256: `01c89e6c28cd6a10563f2429fb48478638f7bee6b5086905f6b100ae9ff61666`
- D1: `Testing` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Testing/meningioma/Te-me_268.jpg`
- D2: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00538_me_sa_t1.jpg`

### Pair 37

- SHA256: `01cfe90cf0aab47f6490ef437197f7d20b3bef33dc17f45088a23c4e4da641a1`
- D1: `Testing` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Testing/pituitary/Te-pi_303.jpg`
- D2: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00797_pi_ax_t1.jpg`

### Pair 38

- SHA256: `01d058bfeb23f73a71cde96d01a5449d4bc7d07c5459ee758ab0c4c78013e824`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_57.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00899_gl_sa_t1.jpg`

### Pair 39

- SHA256: `01dec92345187c9787be63c2e315e16faf75fc826c5d85e50d419e0037a70820`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_723.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00575_gl_co_t1.jpg`

### Pair 40

- SHA256: `01e3ae35ad8a57942001111cd45a2d9e03adc1b7b0def3e2e974544dc3443ba2`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_1145.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02085_me_sa_t1.jpg`

### Pair 41

- SHA256: `01e69989dba1488ee15f4985d0cbe9439d22489e4955cb3573b0fa9612b9aba1`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_1020.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00882_gl_sa_t1.jpg`

### Pair 42

- SHA256: `01e9e945d414f2393b28b31868c26cab1a36437e53940f3c93d61b0e8197579a`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1022.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03804_pi_ax_t1.jpg`

### Pair 43

- SHA256: `01efcabecfbd8b570cde2bb44f8ea7d5f6beea33e81348d6022ca4618c6e6541`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_273.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00692_gl_co_t1.jpg`

### Pair 44

- SHA256: `01facbc64962bb3ba6d8d5a8cf9a2eb6d3754300449eab06aa1146369c032a8d`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_167.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04193_pi_co_t1.jpg`

### Pair 45

- SHA256: `0208fb1ef4e28eb7e80fa12fb16f0b5842c183bc23b9f28b4743cb47453f9199`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_341.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01199_me_ax_t1.jpg`

### Pair 46

- SHA256: `021ee6d047629e09d4a1ca7edb1618046e0f61ce996a8dea861af2143761c1bd`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_544.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04250_pi_co_t1.jpg`

### Pair 47

- SHA256: `022ccedb3605f096ce3b354706ac2f1fb1e035b063b6dcad04da7b04935b05ec`
- D1: `Testing` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Testing/meningioma/Te-me_168.jpg`
- D2: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00471_me_co_t1.jpg`

### Pair 48

- SHA256: `023547f7e1adcdf691e955853804b1b54b1270bf7c96f0705bab7087b2fbe425`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_1244.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01550_me_ax_t1.jpg`

### Pair 49

- SHA256: `024bdc364dc642a401ddca2ba91863d0f07055ed69594942b24d5f9724e2d737`
- D1: `Testing` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Testing/meningioma/Te-me_158.jpg`
- D2: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00297_me_ax_t1.jpg`

### Pair 50

- SHA256: `025f23d258f09b625cffd1a37ebfd7e7510547ed57f6e021de27f9272512938e`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_21.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00177_gl_ax_t1.jpg`

### Pair 51

- SHA256: `026e8df9f23edbd0caa5c1f130587abede8609a95fe334391459f8853a9d5a66`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_164.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04231_pi_co_t1.jpg`

### Pair 52

- SHA256: `02765f73553bc49727595f00141ff335ff7522bf7e2d89276f00a3e495ada4ad`
- D1: `Testing` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Testing/pituitary/Te-pi_205.jpg`
- D2: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00906_pi_co_t1.jpg`

### Pair 53

- SHA256: `02799f7863d49de182357e72179f3cc4e65e70099355f2d5aa2e39d356e492d9`
- D1: `Testing` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Testing/pituitary/Te-pi_168.jpg`
- D2: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00827_pi_co_t1.jpg`

### Pair 54

- SHA256: `028223a7646098304286d6306082f93ce4c1611de933f52fff8c9f45e4f15b19`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_233.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01841_me_co_t1.jpg`

### Pair 55

- SHA256: `02a08fcf2dd0174628542caf95a31182cd15519ca4140a5b4ee938207dc8da02`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_740.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00422_gl_co_t1.jpg`

### Pair 56

- SHA256: `02bcfe2db34e22a055a6a8f81b40b2ba1f96870b34afa91799e76ad7fee33d07`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_823.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01697_me_co_t1.jpg`

### Pair 57

- SHA256: `02c81edf48c0a38a53e691eae33f4e580e9b7374687f97a6b866190aac54a798`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_250.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_01009_gl_sa_t1.jpg`

### Pair 58

- SHA256: `02c922f41d5a1c860e0ba4451c9d957f20e4f588d19c39450d161583fc696728`
- D1: `Testing` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Testing/meningioma/Te-me_13.jpg`
- D2: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00552_me_sa_t1.jpg`

### Pair 59

- SHA256: `02d29847c192393f63c611d44d3e536c967913583dbde3f65aa9dac967435ede`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_330.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04608_pi_sa_t1.jpg`

### Pair 60

- SHA256: `02d4fec0fd4a18bf63b64d7d87d22c63f2216c830db752108883afd5c59d4599`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_146.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03961_pi_ax_t1.jpg`

### Pair 61

- SHA256: `02d84c8f215bb8f8f94ad1456041dd8e0fd8e76097cecad324e06d40b429baf8`
- D1: `Training` / `notumor` / `data/raw/D1_nickparvar_kaggle/Training/notumor/Tr-no_686.jpg`
- D2: `train` / `notumor` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/no_tumor/brisc2025_train_02832_no_co_t1.jpg`

### Pair 62

- SHA256: `0305e36d5ac04ef1dbf19a9d271c5d5b181e1c6bd5daf67797a997c32b71f0ef`
- D1: `Testing` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Testing/meningioma/Te-me_166.jpg`
- D2: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00545_me_sa_t1.jpg`

### Pair 63

- SHA256: `0320f2ea582ad1dfaa9c05864360b873f5fec1fee3e35cf6b5e6237c53351497`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1345.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04537_pi_sa_t1.jpg`

### Pair 64

- SHA256: `032b9042ce369d8f4a72e6c7fef1b96253338b526d368b2bc2d88932c127eff1`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_873.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02228_me_sa_t1.jpg`

### Pair 65

- SHA256: `0348a950531d7a8f9b59744f07e5cc89275a64040e0c380b828c548dcd2653fe`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_1355.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00093_gl_ax_t1.jpg`

### Pair 66

- SHA256: `034fa02cddc4161d999241e4617fd1d1223249b8aeb76fd6f3e82349e33b41f0`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1326.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04579_pi_sa_t1.jpg`

### Pair 67

- SHA256: `0352d35b21998d26f81825ab1d8d110de51e9688c4215c5597fd077fac4a1f22`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_178.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04196_pi_co_t1.jpg`

### Pair 68

- SHA256: `036c770275ee99660fd4d157a86baa843e8ce71848e182e62608ea758cf20637`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_641.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02417_me_sa_t1.jpg`

### Pair 69

- SHA256: `03778458c3d82abe8d8321a33cb39174e167e0657a3f2c0226f0bd786356ed08`
- D1: `Testing` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Testing/pituitary/Te-pi_395.jpg`
- D2: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00705_pi_ax_t1.jpg`

### Pair 70

- SHA256: `0387e6ee3b4a1219be979c1b1dc000cfa6ad105d3770738f7337ccefbc522ccb`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1319.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04443_pi_co_t1.jpg`

### Pair 71

- SHA256: `038db1bbb4895f343f748f586df291c6ad85a6e9f33f4823cb179c1f57dd276d`
- D1: `Testing` / `glioma` / `data/raw/D1_nickparvar_kaggle/Testing/glioma/Te-gl_123.jpg`
- D2: `test` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/glioma/brisc2025_test_00063_gl_ax_t1.jpg`

### Pair 72

- SHA256: `0393684019b077c8ca1612bffafae672b08a84ed5e66d5290eb93d541a9face9`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_373.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01669_me_co_t1.jpg`

### Pair 73

- SHA256: `03abfffad1040b692d33000086c2a2b1737f7ea025905d9dbd71176af2b57be4`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_16.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04073_pi_co_t1.jpg`

### Pair 74

- SHA256: `03be2cee7a4712d7d62ab5d0d2439577eca10c2d554c3a7e1cdf053a3a36507f`
- D1: `Testing` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Testing/meningioma/Te-me_85.jpg`
- D2: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00332_me_ax_t1.jpg`

### Pair 75

- SHA256: `03bf6187fa392665517d8aa2f50eccc5e487abc2e1fd7eba4d9366a645d7a804`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_133.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03725_pi_ax_t1.jpg`

### Pair 76

- SHA256: `03ce76b527d01938dde828aa4b9e3e882cee655017ea9ed27effa47790f184d2`
- D1: `Testing` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Testing/meningioma/Te-me_223.jpg`
- D2: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00491_me_sa_t1.jpg`

### Pair 77

- SHA256: `03dad77027ac10c2591e81b6cf40020a5ae088eca22d27675758dfc9184eae46`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1014.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04389_pi_co_t1.jpg`

### Pair 78

- SHA256: `03fe6e13a5a4204af20290f52deb08009caf10679b24bca5d2035e60576676a9`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_1107.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01730_me_co_t1.jpg`

### Pair 79

- SHA256: `040a415afd40cde551ea35ff4fad705011f381f0700de2479ed124c6392dc505`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_794.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02400_me_sa_t1.jpg`

### Pair 80

- SHA256: `0423469c6b0d771688530aa2670050b206dacb0a567ed453eb0f5c5b581997e7`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_1254.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00024_gl_ax_t1.jpg`

### Pair 81

- SHA256: `04362407f0b50f6d886cacd6003c3ec9a06a9f0c792034c2a0cdb9943e8cba90`
- D1: `Testing` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Testing/meningioma/Te-me_136.jpg`
- D2: `test` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/meningioma/brisc2025_test_00533_me_sa_t1.jpg`

### Pair 82

- SHA256: `043a2e8857ac164f6228500db9060a24c3b5ac99ffddcbc15c7342b09f35fbc9`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_839.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00402_gl_co_t1.jpg`

### Pair 83

- SHA256: `04519791dc2d4a84e7ea188f1fbe164a21f47b94b63fd9e6f8e398017bb0fd55`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_403.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02204_me_sa_t1.jpg`

### Pair 84

- SHA256: `046b9b75be07703df500622fef3bd9c49a1386ea6f4325f730c91489856db016`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_1280.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01918_me_co_t1.jpg`

### Pair 85

- SHA256: `046d5c9778b50b9b16df3b053817af4112fb4b2c7caeadc5ea074db83a6a8fbd`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_1273.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_03851_pi_ax_t1.jpg`

### Pair 86

- SHA256: `0471a53479c15eb66eddcebf9bc3100c13334f532215415b6807c59fc53e4bf0`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_405.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02043_me_sa_t1.jpg`

### Pair 87

- SHA256: `04758129e4627093abd84496c8c6326b62f022202b3adde150d294d35f5b47dd`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_1285.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00536_gl_co_t1.jpg`

### Pair 88

- SHA256: `047fc922c230ca65a7aabc45c2295abb8d0f6e1407b5c2a49db7194ec9b1efd7`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_529.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00797_gl_co_t1.jpg`

### Pair 89

- SHA256: `04988ea9700c3a21a60aa075e3f0615550b0372f75326462f3c9b2e300b4f0e2`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_948.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00936_gl_sa_t1.jpg`

### Pair 90

- SHA256: `049f628e90a618faa7038e5bbd06e8cf564aff2138d8ae090e3116158279e6d3`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_568.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04503_pi_sa_t1.jpg`

### Pair 91

- SHA256: `04a160bcbcc9c401ab07f39f2df0447d3a9c59c2b57b4a969316b46417046a55`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_1293.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01813_me_co_t1.jpg`

### Pair 92

- SHA256: `04afbe78bbaf1181c42852737194bd674f8ab99a973dc715b590e8584886cd77`
- D1: `Testing` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Testing/pituitary/Te-pi_162.jpg`
- D2: `test` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/test/pituitary/brisc2025_test_00863_pi_co_t1.jpg`

### Pair 93

- SHA256: `04c2311c9584390845a23eb5a9340a8fe8f42dea2c88050490e6396a5aaae324`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_734.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00011_gl_ax_t1.jpg`

### Pair 94

- SHA256: `04c801927f76ea1db923da5c311315c9c48d672da9355db5d30ffc05b8801b14`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_559.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04112_pi_co_t1.jpg`

### Pair 95

- SHA256: `052302e135d5193b0dc257615d4159155366c7691911cf494d881dde0b377bcf`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_791.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02142_me_sa_t1.jpg`

### Pair 96

- SHA256: `05302f1769113dcaf7e079654c98cdb81ae628ee6980073cfdf6d15324d9a0ea`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_731.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02440_me_sa_t1.jpg`

### Pair 97

- SHA256: `053980449dbdc2afd6b1dc58c4982d6c43466accabf7393e830008b6111b612e`
- D1: `Training` / `glioma` / `data/raw/D1_nickparvar_kaggle/Training/glioma/Tr-gl_889.jpg`
- D2: `train` / `glioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/glioma/brisc2025_train_00963_gl_sa_t1.jpg`

### Pair 98

- SHA256: `055e3d6a3fc9cabbf9ae22b9f9fd2fc669dc22161962a22256bf41a37d35102d`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_348.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_02038_me_sa_t1.jpg`

### Pair 99

- SHA256: `05730c1b2603d901d540a8f923fa3db4ebaf6513e21fd385ae4a8aee0539682c`
- D1: `Training` / `meningioma` / `data/raw/D1_nickparvar_kaggle/Training/meningioma/Tr-me_201.jpg`
- D2: `train` / `meningioma` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/meningioma/brisc2025_train_01920_me_co_t1.jpg`

### Pair 100

- SHA256: `058826b9810d817cc1a658890fd576f3c00421905db94192d3bd741061855a5e`
- D1: `Training` / `pituitary` / `data/raw/D1_nickparvar_kaggle/Training/pituitary/Tr-pi_388.jpg`
- D2: `train` / `pituitary` / `data/raw/D2_brisc2025/brisc2025/classification_task/train/pituitary/brisc2025_train_04755_pi_sa_t1.jpg`

