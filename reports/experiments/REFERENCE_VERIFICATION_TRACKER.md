# Reference List ? Verification Tracker

66 references extracted from the thesis PDF. Triaged by verification priority.

**Tier 3** ? a specific number is quoted in your text from this source. A reviewer can
check these in one click, and a wrong figure is worse than a wrong citation.
**Tier 2** ? recent, obscure, or preprint. Verify metadata.
**Tier 1** ? canonical and heavily cited. Metadata is stable; spot-check only.

Status key: `[ ]` unverified · `[?]` verified · `[!]` discrepancy found

---

## Already verified

- [?] **Amin, S. B., et al. (2020).** Canine glioma characterization project for ICDC
  (ICDC-Glioma) 01 [Data set]. The Cancer Imaging Archive.
  `10.7937/TCIA.SVQT-Q016`
  ? Real. **The name "ICDC-Glioma" is CORRECT.** Table 2.1 footnote d says it is
  incorrect and must be replaced ? that footnote is wrong and should be deleted.
  Collection has 57 subjects with MR; your 53 after T1 selection is consistent.
  CC BY 4.0, updated 2021/01/12.

- [?] **Musa, A., Prasad, R., Onwualu, P., & Hernandez, M. (2026).** A systematic review
  of cross-population shifts in medical imaging analysis with deep learning. *Big Data
  and Cognitive Computing, 10*(3), 76. `10.3390/bdcc10030076`
  ? Real. Published 4 March 2026. Your quoted "10% to 25%" degradation and "50 studies"
  both match the abstract.

- [?] **Aresta, S., et al. (2026).** Advancing brain tumor diagnosis using deep learning:
  A systematic review on glioma segmentation and classification on multiparametric MRI
  [Preprint]. medRxiv. `10.64898/2026.01.13.26344038`
  ? Real. The unusual `10.64898` prefix is medRxiv's new openRxiv prefix, not an error.
  31 studies of 310 screened, 2022?2025. Preregistered on OSF (osf.io/8tvez).

---

## Tier 3 ? you quote a specific figure from these (15)

- [ ] **Yagis, E., et al. (2021).** Effect of data leakage in brain MRI classification
  using 2D convolutional neural networks. *Scientific Reports, 11*, 22544.
  `10.1038/s41598-021-01681-w`
  ? **You quote:** slice-level splitting inflates accuracy by "approximately 29% to 55%"
  across OASIS, ADNI and PPMI; randomly labelled data reached "roughly 96%" under
  slice-level but "the expected 50%" under subject-level.

- [ ] **Kouli, O., et al. (2022).** *(cited in text, absent from reference list ? see
  Missing section below)*
  ? **You quote:** "only about 30% of studies performed any external validation."

- [ ] **Yu, A. C., Mohajer, B., & Eng, J. (2022).** External validation of deep learning
  algorithms for radiologic diagnosis: A systematic review. *Radiology: Artificial
  Intelligence, 4*(3), e210064. `10.1148/ryai.210064`
  ? **You quote:** 83 studies; "81% reported some decrease", "49% ... at least a modest
  decrease and 24% a substantial decrease."

- [ ] **Barz, B., & Denzler, J. (2020).** Do we train on test data? Purging CIFAR of
  near-duplicates. *Journal of Imaging, 6*(6), 41. `10.3390/jimaging6060041`
  ? **You quote:** "3.3% and 10%" test-set duplicates in CIFAR-10/100; removing them
  reduced accuracy by "9% to 14%".

- [ ] **Cassidy, B., et al. (2022).** Analysis of the ISIC image datasets: Usage,
  benchmarks and recommendations. *Medical Image Analysis, 75*, 102305.
  `10.1016/j.media.2021.102305`
  ? **You quote:** "14,310 duplicate images removed from the training set."

- [ ] **Zech, J. R., et al. (2018).** Variable generalization performance of a deep
  learning model to detect pneumonia in chest radiographs. *PLOS Medicine, 15*(11),
  e1002683. `10.1371/journal.pmed.1002683`
  ? **You quote:** networks identified the source hospital with "99.95% accuracy."

- [ ] **Veetil, I. K., et al. (2024).** An analysis of data leakage and generalizability
  in MRI based classification of Parkinson's disease using explainable 2D CNNs.
  *Digital Signal Processing, 147*, 104407. `10.1016/j.dsp.2024.104407`
  ? **You quote:** inflation "up to 67% and 30%" for slice-level and longitudinal leakage.

- [ ] **Tampu, I. E., Eklund, A., & Haj-Hosseini, N. (2022).** Inflation of test accuracy
  due to data leakage in deep learning-based classification of OCT images. *Scientific
  Data, 9*, 580. `10.1038/s41597-022-01618-6`
  ? **You quote:** MCC inflated by "0.07 to 0.43".

- [ ] **Samala, R. K., et al. (2020).** Hazards of data leakage in machine learning.
  *SPIE Medical Imaging 2020*, 11314, 1131320. `10.1117/12.2549313`
  ? **You quote:** validation AUC "0.99" against an independent test ceiling of "?0.72".

- [ ] **Adimoolam, Y. K., Poullis, C., & Averkiou, M. (2023).** Data leakage detection and
  de-duplication in large scale geospatial image datasets [Preprint]. arXiv:2304.02296
  ? **You quote:** "roughly 93% of the validation split was also present in the training
  split." **Also check whether this has since been published** ? cite the journal version
  if so.

- [ ] **Kapoor, S., & Narayanan, A. (2023).** Leakage and the reproducibility crisis in
  machine-learning-based science. *Patterns, 4*(9), 100804.
  `10.1016/j.patter.2023.100804`
  ? **You quote:** leakage in "17 distinct fields", "294 papers", "eight leakage types".

- [ ] **Nagendran, M., et al. (2020).** Artificial intelligence versus clinicians.
  *BMJ, 368*, m689. `10.1136/bmj.m689`
  ? **You quote:** high risk of bias in "58 of 81"; data and code unavailable in "95% and
  93%"; "61 of 81" claimed comparable performance; "38%" acknowledged need for
  prospective evaluation.

- [ ] **Andaur Navarro, C. L., et al. (2021).** Completeness of reporting of clinical
  prediction models developed using supervised machine learning. *BMC Medical Research
  Methodology, 21*, 12. `10.1186/s12874-021-01469-6`
  ? **You quote:** median TRIPOD adherence "approximately 38.7%".
  ? **Check the DOI.** A 2021 article numbered 21:12 with a `-01469-6` suffix is worth
  confirming; suffix and article number sometimes diverge in BMC citations.

- [ ] **Bhandari, A., et al. (2023).** Assessment of AI reporting methodology in glioma
  MRI studies using CLAIM. *Neuroradiology, 65*, 907?913.
  `10.1007/s00234-023-03146-5`
  ? **You quote:** mean CLAIM score "20 out of 42".

- [ ] **Mårtensson, G., et al. (2020).** The reliability of a deep learning model in
  clinical out-of-distribution MRI data. *Medical Image Analysis, 66*, 101714.
  `10.1016/j.media.2020.101714`
  ? **You quote:** "more than 3,000 scans".

- [ ] **Ong Ly, C., et al. (2024).** Shortcut learning in medical AI hinders
  generalization. *npj Digital Medicine, 7*, 124. `10.1038/s41746-024-01118-4`
  ? **You quote:** performance overestimated "by up to 20% on average".

- [ ] **Reyes, D., & Sánchez, J. (2024).** Performance of convolutional neural networks
  for the classification of brain tumors using MRI. *Heliyon, 10*(3), e25468.
  `10.1016/j.heliyon.2024.e25468`
  ? **You quote:** ">2,260 coincident images" Figshare?Kaggle overlap, and best internal
  accuracy 98.70%. **This underpins your D2 argument ? verify carefully.**

---

## Tier 2 ? recent, obscure, or preprint (24)

- [ ] Abdar, M., et al. (2021). *Computers in Biology and Medicine, 135*, 104418. `10.1016/j.compbiomed.2021.104418`
- [ ] Abhishek, K., Jain, A., & Hamarneh, G. (2024). *Scientific Data, 11*, 1054. `10.1038/s41597-024-03721-2`
- [ ] Bakas, S., et al. (2022). UPenn-GBM cohort. *Scientific Data, 9*, 453. `10.1038/s41597-022-01560-7` ? **your D3C source; verify**
- [ ] Bernett, J., Blumenthal, D. B., & List, M. (2024). *Nature Methods, 21*, 1444?1453. `10.1038/s41592-024-02362-y`
- [ ] Chanda, A., et al. (2025). arXiv:2509.24951 ? **preprint; check for journal version**
- [ ] Collins, G. S., et al. (2024). TRIPOD+AI. *BMJ, 385*, e078378. `10.1136/bmj-2023-078378`
- [ ] Disci, R., Gurcan, F., & Soylu, A. (2025). *Cancers, 17*(1), 121. `10.3390/cancers17010121`
- [ ] Elhadidy, M. S., et al. (2025). *Computers in Biology and Medicine, 188*, 109872. `10.1016/j.compbiomed.2025.109872`
- [ ] Fateh, A., et al. (2025). BRISC. arXiv:2506.14318 ? **your D2 source. Check whether it now has a Scientific Data descriptor; if so cite that, and check whether the authors document derivation from Nickparvar**
- [ ] ?lgün, E. G., & Dener, M. (2025). *Neural Computing and Applications, 37*, 28779?28801. `10.1007/s00521-025-11626-3` ? **Table 2.2 marks this "NV: full text unavailable". Either obtain it or keep it excluded from counts**
- [ ] Joshi, A., et al. (2023). IITCEE. `10.1109/IITCEE57236.2023.10091044`
- [ ] Karandikar, A., et al. (2021). NeurIPS 34, 29768?29779.
- [ ] Kilim, O., et al. (2022). *Scientific Reports, 12*, 21302. `10.1038/s41598-022-23990-4`
- [ ] Koçak, B., et al. (2023). *European Radiology, 33*, 8888?8898. `10.1007/s00330-023-09871-y`
- [ ] Kurz, A., et al. (2022). *JMIR Medical Informatics, 10*(8), e36427. `10.2196/36427`
- [ ] Linmans, J., et al. (2023). *Medical Image Analysis, 83*, 102655. `10.1016/j.media.2022.102655`
- [ ] Loftus, T. J., et al. (2022). *PLOS Digital Health, 1*(8), e0000085. `10.1371/journal.pdig.0000085`
- [ ] Matta, S., et al. (2024). *Computers in Biology and Medicine, 183*, 109256. `10.1016/j.compbiomed.2024.109256`
- [ ] Maurício, J., Domingues, I., & Bernardino, J. (2023). *Applied Sciences, 13*(9), 5521. `10.3390/app13095521`
- [ ] Mehrtens, H. A., et al. (2023). *Medical Image Analysis, 89*, 102914. `10.1016/j.media.2023.102914`
- [ ] Pohjonen, J., et al. (2022). arXiv:2206.15274 ? **preprint; check for journal version**
- [ ] Rosenblatt, M., et al. (2024). *Nature Communications, 15*, 1829. `10.1038/s41467-024-46150-w`
- [ ] Shelmerdine, S. C., et al. (2021). *BMJ Health & Care Informatics, 28*(1), e100385. `10.1136/bmjhci-2021-100385`
- [ ] Takahashi, S., et al. (2024). *Journal of Medical Systems, 48*, 84. `10.1007/s10916-024-02105-8`
- [ ] Truong, T., Khun Jush, F., & Lenga, M. (2023). arXiv:2312.07273 ? **preprint; check**
- [ ] Vimala, B. B., et al. (2023). *Scientific Reports, 13*, 23029. `10.1038/s41598-023-50505-6`
- [ ] Xie, Y., et al. (2022). *Diagnostics, 12*(8), 1850. `10.3390/diagnostics12081850`
- [ ] Xiong, M., et al. (2023). NeurIPS 36, 68511?68538.
- [ ] Zulfiqar, F., Bajwa, U. I., & Mehmood, Y. (2023). *Biomedical Signal Processing and Control, 84*, 104777. `10.1016/j.bspc.2023.104777`

---

## Tier 1 ? canonical, spot-check only (17)

- [ ] Cheng, J. (2016). Brain tumor dataset. figshare. `10.6084/m9.figshare.1512427`
- [ ] Clark, K., et al. (2013). TCIA. *Journal of Digital Imaging, 26*(6), 1045?1057. `10.1007/s10278-013-9622-7`
- [ ] Collins, G. S., et al. (2015). TRIPOD. *Circulation, 131*(2), 211?219. `10.1161/CIRCULATIONAHA.114.014508`
- [ ] Dosovitskiy, A., et al. (2021). ViT. ICLR.
- [ ] Gal, Y., & Ghahramani, Z. (2016). MC dropout. ICML 48, 1050?1059.
- [ ] Guo, C., et al. (2017). On calibration of modern neural networks. ICML 70, 1321?1330.
- [ ] Hamada, A. (2020). Br35H. Kaggle.
- [ ] He, K., et al. (2016). ResNet. CVPR, 770?778. `10.1109/CVPR.2016.90`
- [ ] Kull, M., et al. (2019). Dirichlet calibration. NeurIPS 32, 12295?12305.
- [ ] Lakshminarayanan, B., Pritzel, A., & Blundell, C. (2017). Deep ensembles. NeurIPS 30, 6402?6413.
- [ ] Mongan, J., Moy, L., & Kahn, C. E. (2020). CLAIM. *Radiology: AI, 2*(2), e200029. `10.1148/ryai.2020200029`
- [ ] Mukhoti, J., et al. (2020). Focal loss calibration. NeurIPS 33, 15288?15299.
- [ ] Nickparvar, M. (2021). Brain tumor MRI dataset. Kaggle. `10.34740/kaggle/dsv/2645886` ? **note: the thesis prints `10.34740/kaggle/dsv/264588685`, which has three extra digits. Check.**
- [ ] Norgeot, B., et al. (2020). MI-CLAIM. *Nature Medicine, 26*, 1320?1324. `10.1038/s41591-020-1041-y`
- [ ] Pinto, F., Torr, P. H. S., & Dokania, P. K. (2022). ECCV, LNCS 13673, 466?480. `10.1007/978-3-031-19778-9_27`
- [ ] Shah, H. A., et al. (2022). *IEEE Access, 10*, 65426?65438. `10.1109/ACCESS.2022.3184113`
- [ ] Tan, M., & Le, Q. (2019). EfficientNet. ICML 97, 6105?6114.
- [ ] Wang, D.-B., Feng, L., & Zhang, M.-L. (2021). NeurIPS 34, 11809?11820.

---

## Cited in text but missing from the reference list

- [ ] **Kouli, O., et al. (2022).** Cited five times (§1.1, §2.2.2, §2.8) for the claim
  that "only about 30% of studies performed any external validation" ? a figure the
  literature review leans on heavily. **Not in the reference list.** Add it.
- [ ] **Quiñonero-Candela et al.** ? referenced conceptually in §2.5 discussion of
  covariate versus concept shift; check whether a citation is needed.

---

## Should be added before journal submission

Not currently cited. Each closes a gap a reviewer would otherwise raise.

- [ ] **Wallis, D., & Buvat, I. (2022).** Clever Hans effect found in a widely used brain
  tumour MRI dataset. *Medical Image Analysis*. ? Shows high accuracy achievable on this
  benchmark with no tumour information, from radiologist slice selection. **Required
  citation**; strengthens your argument that internal macro-F1 does not measure what the
  field assumes.
- [ ] **Åkesson, J., et al. (2024).** Random effects during training. *Computers in
  Biology and Medicine*. ? nnU-Net, 50 seeds, brain tumour among the tasks. Direct
  precedent for your seed-variance result.
- [ ] **Teney, D., et al. (2022).** ID and OOD performance are sometimes inversely
  correlated on real-world datasets. ? Closest ancestor of your Simpson's paradox result.
- [ ] **Bosma, J., et al. (2023).** Reproducibility of training deep learning models for
  medical image analysis. ? The classification-side counterpart to Åkesson.
- [ ] **Christodoulou, E., et al.** False promises in medical imaging AI. ? Pre-written
  motivation for your central claim.
- [ ] **Mehra, A., et al. (2024).** Agreement-on-the-line for foundation models. ?
  Seed-level structure in ID?OOD predictability under light fine-tuning; closest to your
  mechanism.
- [ ] **Zech, J. R., et al. (2019).** Individual predictions matter. ? 50 seeds on
  CheXNet; image-level variability not reflected in test-set AUC.
- [ ] **Picard, D. (2021).** torch.manual_seed(3407). ? Canonical outlier-seed citation.
- [ ] **arXiv 2511.02453** ? Accounting for underspecification in statistical claims of
  model superiority. **Direct competitor for your positioning.** Decide whether you extend
  it or compete with it, and cite either way.

---

## Discrepancies found so far

| Reference | Issue |
|---|---|
| Amin et al. (2020) | Table 2.1 footnote d claims "ICDC-Glioma" is incorrect. It is correct. Delete the footnote. |
| Nickparvar (2021) | Thesis DOI `10.34740/kaggle/dsv/264588685` appears to have extra digits. Kaggle DSV identifiers are typically 7 digits. |
| Kouli et al. (2022) | Cited repeatedly; absent from the reference list. |
| ?lgün & Dener (2025) | Marked "not verified, full text unavailable" in Table 2.2 and excluded from counts. Either obtain it or state the exclusion in the caption. |
