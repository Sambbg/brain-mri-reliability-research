# Canonical Reference List ? 45 references

Curated for *Reliability Evaluation of Brain MRI Tumour Classification Models Under
Calibration and Dataset Shift*, revised for the seed-sweep result set
(`2026-08-sweep-a`).

**This list supersedes both earlier reference sets:** the 66-entry list in the proposal
PDF and the 23-entry `reference_list_placeholders.md` used by the Run A manuscript draft.

Selection principle: every reference here supports a claim the revised study actually
makes. References supporting only the withdrawn ordering-reversal claim have been
dropped; references supporting the new seed-variance claim have been added.

`[V]` = metadata verified this session. `[ ]` = still to verify.

---

## 1. Datasets and benchmark provenance (5)

**[ ] 1.** Bakas, S., Sako, C., Akbari, H., Bilello, M., Sotiras, A., Shukla, G., Rudie,
J. D., Flores Santamaría, N., Fathi Kazerooni, A., Pati, S., Rathore, S., Mamourian, E.,
Ha, S. M., Parker, W., Doshi, J., Baid, U., Bergman, M., Binder, Z. A., Verma, R., ?
Davatzikos, C. (2022). The University of Pennsylvania glioblastoma (UPenn-GBM) cohort:
Advanced MRI, clinical, genomics, & radiomics. *Scientific Data, 9*, 453.
https://doi.org/10.1038/s41597-022-01560-7
? D3C source.

**[V] 2.** Amin, S. B., Anderson, K. J., Boudreau, C. E., Martinez-Ledesma, E.,
Kocakavuk, E., Johnson, K. C., Barthel, F. P., Varn, F. S., Kassab, C., Ling, X., Kim,
H., Barter, M., Lau, C. C., Yee Ngan, C., Chapman, M., Koehler, J. W., Miller, A. D.,
Long, J. P., Miller, C. R., ? Verhaak, R. G. W. (2020). *Canine glioma characterization
project for ICDC (ICDC-Glioma) 01* [Data set]. The Cancer Imaging Archive.
https://doi.org/10.7937/TCIA.SVQT-Q016
? D3B source. Verified against TCIA: 57 subjects with MR, CC BY 4.0. **The collection
name "ICDC-Glioma" is correct** ? delete the footnote claiming otherwise.

**[ ] 3.** Cheng, J. (2016). *Brain tumor dataset* [Data set]. figshare.
https://doi.org/10.6084/m9.figshare.1512427
? Upstream source of D1's tumour classes.

**[ ] 4.** Nickparvar, M. (2021). *Brain tumor MRI dataset* [Data set]. Kaggle.
https://doi.org/10.34740/kaggle/dsv/2645886
? D1. **Check the DOI** ? the proposal prints `264588685`, which has extra digits.

**[ ] 5.** Fateh, A., Rezvani, Y., Moayedi, S., Rezvani, S., Fateh, F., Fateh, M., &
Abolghasemi, V. (2025). BRISC: Annotated dataset for brain tumor segmentation and
classification [Preprint]. arXiv. https://arxiv.org/abs/2506.14318
? D2, rejected after overlap audit. **Check for a published version, and check whether
the authors document derivation from Nickparvar** ? if they do, reframe your finding as
an interoperability warning rather than a contamination discovery.

*Dropped: Hamada (2020) Br35H and Clark (2013) TCIA. Cite in text as data sources
without full entries unless a specific claim depends on them.*

---

## 2. Architectures (4)

**[ ] 6.** He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep residual learning for image
recognition. *CVPR*, 770?778. https://doi.org/10.1109/CVPR.2016.90

**[ ] 7.** Tan, M., & Le, Q. (2019). EfficientNet: Rethinking model scaling for
convolutional neural networks. *ICML, 97*, 6105?6114.

**[ ] 8.** Dosovitskiy, A., Beyer, L., Kolesnikov, A., Weissenborn, D., Zhai, X.,
Unterthiner, T., Dehghani, M., Minderer, M., Heigold, G., Gelly, S., Uszkoreit, J., &
Houlsby, N. (2021). An image is worth 16×16 words: Transformers for image recognition at
scale. *ICLR*.

**[ ] 9.** Pinto, F., Torr, P. H. S., & Dokania, P. K. (2022). An impartial take to the
CNN vs transformer robustness contest. *ECCV*, LNCS 13673, 466?480.
https://doi.org/10.1007/978-3-031-19778-9_27
? Supports treating the CNN/transformer question as unsettled.

---

## 3. Data leakage and benchmark contamination (8)

**[V] 10.** Wallis, D., & Buvat, I. (2022). Clever Hans effect found in a widely used
brain tumour MRI dataset. *Medical Image Analysis*.
https://doi.org/10.1016/j.media.2022.102368
? **Essential and currently missing.** Shows high tumour classification accuracy is
achievable on this benchmark *with no information about the tumour itself*, arising from
implicit radiologist input in 2D slice selection, and notes no other paper using the
dataset mentions the bias. Directly supports your claim that internal macro-F1 on this
benchmark does not measure what the field assumes. 42 citations.

**[V] 11.** Yagis, E., Atnafu, S. W., García Seco de Herrera, A., Marzi, C., Scheda, R.,
Giannelli, M., Tessa, C., Citi, L., & Diciotti, S. (2021). Effect of data leakage in
brain MRI classification using 2D convolutional neural networks. *Scientific Reports,
11*, 22544. https://doi.org/10.1038/s41598-021-01681-w
? **Correct your figures.** Slice-level splitting inflated accuracy by 30% (OASIS), 29%
(ADNI), 48% (PPMI) and 55% (a local de-novo PD Versilia dataset). The proposal attributes
the 29?55% range to "OASIS, ADNI, and PPMI" ? the 55% is Versilia, a fourth dataset. The
randomly-labelled result (?96% slice-level vs 50% subject-level) is correct as stated.

**[V] 12.** Cassidy, B., Kendrick, C., Brodzicki, A., Jaworek-Korjakowska, J., & Yap, M.
H. (2022). Analysis of the ISIC image datasets: Usage, benchmarks and recommendations.
*Medical Image Analysis, 75*, 102305. https://doi.org/10.1016/j.media.2021.102305
? 14,310 duplicates removed from training; best AUC 0.80 after removal. **Check the
year** ? indexed as 2021 online, volume 75 is the January 2022 issue.

**[V] 13.** Saifullah, M., et al. (2025). Reliable brain tumor classification without
metadata: A step-by-step guideline with duplicate removal. *IEEE ICTAI 2025*.
? **Add.** pHash de-duplication on the same benchmark family, with before/after
comparison using EfficientNetB0 and InceptionV3. An independent concordant audit ? cite
it as replication rather than claiming your duplicate finding as novel.

**[V] 14.** Lu, D., et al. (2026). MTA-Swin: A multi-token attention Swin Transformer for
brain tumor classification with leakage-free MRI benchmarking. *Journal of Medical
Systems*.
? **Add.** Documents duplicate-induced leakage in widely used brain tumour MRI datasets
and reduces the 7,023-image set to 3,522 unique scans. The closest published work to your
contamination audit. Also reports accuracy over three random seeds.

**[ ] 15.** Kapoor, S., & Narayanan, A. (2023). Leakage and the reproducibility crisis in
machine-learning-based science. *Patterns, 4*(9), 100804.
https://doi.org/10.1016/j.patter.2023.100804
? You quote: 17 fields, 294 papers, eight leakage types.

**[V] 16.** Rosenblatt, M., Tejavibulya, L., Jiang, R., Noble, S., & Scheinost, D.
(2024). Data leakage inflates prediction performance in connectome-based machine learning
models. *Nature Communications, 15*, 1829. https://doi.org/10.1038/s41467-024-46150-w
? Verified. Five forms of leakage; feature selection and repeated subjects inflate most;
small datasets worst affected. 168 citations.

**[ ] 17.** Barz, B., & Denzler, J. (2020). Do we train on test data? Purging CIFAR of
near-duplicates. *Journal of Imaging, 6*(6), 41. https://doi.org/10.3390/jimaging6060041
? You quote: 3.3% and 10% test duplicates; 9?14% accuracy reduction.

**[V] 18.** Truong, T., Khun Jush, F., & Lenga, M. (2023). Benchmarking pretrained vision
embeddings for near- and duplicate detection in medical images. *IEEE ISBI 2024*.
? **Update the citation** ? now published at ISBI 2024, not an arXiv preprint. Mean
sensitivity 0.9645, specificity 0.8559.

*Dropped: Adimoolam (aerial imagery, off-domain), Abhishek, Tampu, Veetil, Samala,
Bernett. Retain Yagis and Rosenblatt as the medical-imaging leakage evidence; the others
padded Table 2.3 without adding argument.*

---

## 4. Calibration and confidence (6)

**[ ] 19.** Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of
modern neural networks. *ICML, 70*, 1321?1330.

**[ ] 20.** Kull, M., Perello-Nieto, M., Kängsepp, M., Silva Filho, T., Song, H., &
Flach, P. (2019). Beyond temperature scaling: Obtaining well-calibrated multi-class
probabilities with Dirichlet calibration. *NeurIPS, 32*, 12295?12305.
? Supports classwise-ECE. **You cite this but do not implement it** ? either implement or
soften the claim.

**[ ] 21.** Naeini, M. P., Cooper, G. F., & Hauskrecht, M. (2015). Obtaining well
calibrated probabilities using Bayesian binning. *AAAI*.
? Recovered from the repo placeholder list. Original ECE binning formulation; belongs in
§3.7.2.

**[ ] 22.** Mukhoti, J., Kulharia, V., Sanyal, A., Golodetz, S., Torr, P. H. S., &
Dokania, P. K. (2020). Calibrating deep neural networks using focal loss. *NeurIPS, 33*,
15288?15299.

**[ ] 23.** Karandikar, A., Cain, N., Tran, D., Lakshminarayanan, B., Shlens, J., Mozer,
M. C., & Roelofs, B. (2021). Soft calibration objectives for neural networks. *NeurIPS,
34*, 29768?29779.
? Post-hoc rescaling degrades under shift ? supports your §4.5/4.6 finding.

**[ ] 24.** Xiong, M., Deng, A., Koh, P. W., Wu, J., Li, S., Xu, J., & Hooi, B. (2023).
Proximity-informed calibration for deep neural networks. *NeurIPS, 36*, 68511?68538.
? Overconfidence on atypical inputs persists after temperature scaling; transformers more
susceptible. Supports your ViT-B/16 result.

*Dropped: Chanda (2025) preprint, Wang (2021), Brier (1950). Brier can be cited in text
without a full entry.*

---

## 5. Dataset shift and external validation (7)

**[ ] 25.** Zech, J. R., Badgeley, M. A., Liu, M., Costa, A. B., Titano, J. J., &
Oermann, E. K. (2018). Variable generalization performance of a deep learning model to
detect pneumonia in chest radiographs. *PLOS Medicine, 15*(11), e1002683.
https://doi.org/10.1371/journal.pmed.1002683
? You quote: 99.95% source-hospital identification.

**[ ] 26.** Yu, A. C., Mohajer, B., & Eng, J. (2022). External validation of deep learning
algorithms for radiologic diagnosis: A systematic review. *Radiology: Artificial
Intelligence, 4*(3), e210064. https://doi.org/10.1148/ryai.210064
? You quote: 83 studies, 81% decreased, 49% modest, 24% substantial.

**[V] 27.** Musa, A., Prasad, R., Onwualu, P., & Hernandez, M. (2026). A systematic review
of cross-population shifts in medical imaging analysis with deep learning. *Big Data and
Cognitive Computing, 10*(3), 76. https://doi.org/10.3390/bdcc10030076
? Verified. 50 studies, 10?25% degradation on unseen populations, mitigation gains 5?15%
and not supported by external validation. Your quoted figures match.

**[ ] 28.** Mårtensson, G., Ferreira, D., Granberg, T., Cavallin, L., Oppedal, K.,
Padovani, A., ? Westman, E. (2020). The reliability of a deep learning model in clinical
out-of-distribution MRI data: A multicohort study. *Medical Image Analysis, 66*, 101714.
https://doi.org/10.1016/j.media.2020.101714

**[ ] 29.** Ong Ly, C., Unnikrishnan, B., Tadic, T., Patel, T., Duhamel, J., Kandel, S.,
Moayedi, Y., Brudno, M., Hope, A., Ross, H., & McIntosh, C. (2024). Shortcut learning in
medical AI hinders generalization. *npj Digital Medicine, 7*, 124.
https://doi.org/10.1038/s41746-024-01118-4
? Directly relevant to the source-confound hypothesis in your future work.

**[V] 30.** Miller, J., Taori, R., Raghunathan, A., Sagawa, S., Koh, P. W., Shankar, V.,
Liang, P., Carmon, Y., & Schmidt, L. (2021). Accuracy on the line: On the strong
correlation between out-of-distribution and in-distribution generalization. *ICML*.
? **Add.** 341 citations. The positive-correlation position your Simpson's paradox result
qualifies. You need this to say what you are pushing against.

**[ ] 31.** Kilim, O., Olar, A., Joó, T., Palicz, T., Pollner, P., & Csabai, I. (2022).
Physical imaging parameter variation drives domain shift. *Scientific Reports, 12*, 21302.
https://doi.org/10.1038/s41598-022-23990-4
? Supports the residual-preprocessing limitation for D3C.

*Dropped: Matta (2024), Pohjonen (2022) preprint, Xie (2022).*

---

## 6. Seed variance, underspecification, ranking stability (7)

**This section is new. It carries the study's central claim and was absent from both
earlier reference lists.**

**[V] 32.** Åkesson, J., et al. (2024). Random effects during training: Implications for
deep learning-based medical image segmentation. *Computers in Biology and Medicine*.
? **Essential.** nnU-Net, 50 seeds, three 3D tasks including brain tumour. The best seed
statistically significantly outperformed 0?76% of remaining seeds from the *same*
algorithm under hold-out validation, and 10?38% under 5-fold CV. Concludes a
statistically significant difference is "a weak and unreliable indicator of a true
performance difference between two learning algorithms." Your result is the
classification-side instance. 18 citations.

**[V] 33.** Teney, D., Lin, Y., Oh, S. J., & Abbasnejad, E. (2022). ID and OOD performance
are sometimes inversely correlated on real-world datasets. *NeurIPS*.
? **Essential ? closest ancestor of your Simpson's paradox result.** Shows inverse ID/OOD
correlations occur in real data, explains them in a minimal linear setting, and argues
past studies missed them through biased model selection. Concludes that studies using ID
performance for model selection "will necessarily miss the best-performing models." 69
citations.

**[V] 34.** Bosma, J., et al. (2023). Reproducibility of training deep learning models for
medical image analysis.
? **Add.** Three diagnostic tasks; retraining variance significant relative to data
variance; 15% of same-method comparisons produced spurious p < 0.05. The
classification-side counterpart to Åkesson.

**[V] 35.** Zech, J. R., Badgeley, M. A., Liu, M., Costa, A. B., Titano, J. J., & Oermann,
E. K. (2019). Individual predictions matter: Assessing the effect of data ordering in
training fine-tuned CNNs for medical imaging. *arXiv*.
? **Add.** CheXNet, 50 seeds. Substantial per-radiograph variability that "was not fully
reflected in the variability of AUC on a large test set" ? a precedent for aggregate
internal metrics hiding instability. Averaging 10 models cut variability by ~70%.

**[V] 36.** Picard, D. (2021). torch.manual_seed(3407) is all you need: On the influence
of random seeds in deep learning architectures for computer vision. *arXiv*.
? **Add.** Up to 10? seeds on CIFAR-10. Canonical citation for outlier seeds ? directly
relevant to your seed-42 finding. 142 citations.

**[V] 37.** Renard, F., Guedria, S., De Palma, N., & Vuillerme, N. (2020). Variability and
reproducibility in deep learning for medical image segmentation. *Scientific Reports*.
? **Add.** Taxonomy of variance sources; 209 citations. Frames your §3.6 methods
discussion.

**[ ] 38.** *Accounting for underspecification in statistical claims of model superiority*
(arXiv:2511.02453, MedEurIPS/NeurIPS 2025 workshop).
? **Add and position against.** Introduces an underspecification term for seed-induced
variance and quantifies by simulation how it inflates the evidence threshold needed to
claim outperformance. Yours is the empirical version of its simulated argument. Decide
explicitly whether you extend it or compete with it ? a reviewer will find it. **Verify
the full citation before submission.**

---

## 7. Uncertainty estimation (4)

**[ ] 39.** Gal, Y., & Ghahramani, Z. (2016). Dropout as a Bayesian approximation. *ICML,
48*, 1050?1059.

**[ ] 40.** Lakshminarayanan, B., Pritzel, A., & Blundell, C. (2017). Simple and scalable
predictive uncertainty estimation using deep ensembles. *NeurIPS, 30*, 6402?6413.

**[ ] 41.** Mehrtens, H. A., Kurz, A., Bucher, T.-C., & Brinker, T. J. (2023).
Benchmarking common uncertainty estimation methods with histopathological images under
domain shift and label noise. *Medical Image Analysis, 89*, 102914.
https://doi.org/10.1016/j.media.2023.102914
? Uncertainty methods must be assessed under shift, not only in-distribution.

**[ ] 42.** Kurz, A., Hauser, K., Mehrtens, H. A., Krieghoff-Henning, E., Hekler, A.,
Kather, J. N., Fröhling, S., von Kalle, C., & Brinker, T. J. (2022). Uncertainty
estimation in medical image classification: Systematic review. *JMIR Medical Informatics,
10*(8), e36427. https://doi.org/10.2196/36427

*Dropped: Abdar (2021), Linmans (2023), Loftus (2022). Three uncertainty citations plus a
review is sufficient for a section you explicitly do not implement.*

---

## 8. Reporting standards (3)

**[ ] 43.** Mongan, J., Moy, L., & Kahn, C. E. (2020). Checklist for Artificial
Intelligence in Medical Imaging (CLAIM). *Radiology: Artificial Intelligence, 2*(2),
e200029. https://doi.org/10.1148/ryai.2020200029

**[ ] 44.** Collins, G. S., Moons, K. G. M., Dhiman, P., Riley, R. D., Beam, A. L., Van
Calster, B., ? Logullo, P. (2024). TRIPOD+AI statement. *BMJ, 385*, e078378.
https://doi.org/10.1136/bmj-2023-078378

**[ ] 45.** Bhandari, A., Scott, L., Weickhardt, A., & Kumar, A. (2023). Assessment of
artificial intelligence reporting methodology in glioma MRI studies using CLAIM.
*Neuroradiology, 65*, 907?913. https://doi.org/10.1007/s00234-023-03146-5
? Glioma-specific; mean CLAIM score 20/42, weakest on data collection, ground truth and
validation.

*Dropped: Collins (2015) original TRIPOD, Norgeot, Shelmerdine, Nagendran, Andaur Navarro,
Koçak. TRIPOD+AI supersedes the 2015 statement; the audit papers are interchangeable and
one glioma-specific example carries the argument.*

---

## What changed from the proposal's 66

**Added (10)** ? all supporting the revised claim:
Wallis & Buvat, Åkesson, Teney, Bosma, Zech 2019, Picard, Renard, Miller, Saifullah,
MTA-Swin, arXiv 2511.02453, Naeini.

**Dropped (~31)** ? mostly the comparison-table padding in §2.2.2 (Disci, Elhadidy, ?lgün,
Shah, Vimala, Zulfiqar, Reyes, Maurício, Takahashi) and redundant leakage or uncertainty
citations. **Keep 3?4 of the high-accuracy comparison studies to populate Table 2.2** ?
they establish the field-wide pattern ? but the current nine are more than the argument
needs.

**Kouli et al. (2022)** was cited five times in the proposal and appears in no reference
list. It carries the "only ~30% performed external validation" figure. **Either locate the
full citation and add it, or replace the claim with Yu et al. (2022) (#26), which reports
a comparable finding and is verified.**

---

## Verification status

| | Count |
|---|---|
| Verified this session | 14 |
| Canonical, spot-check only | 17 |
| Still to verify | 14 |

Priority: the eight references where you quote a specific figure ? #11 Yagis (correct the
dataset attribution), #12 Cassidy (check year), #15 Kapoor, #17 Barz, #25 Zech, #26 Yu,
#38 arXiv 2511.02453, #45 Bhandari.
