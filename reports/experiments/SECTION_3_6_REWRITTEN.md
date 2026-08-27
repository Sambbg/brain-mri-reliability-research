# §3.6 Training and Implementation ? rewritten

*Replaces the existing §3.6 in full. The current text describes single-run training and
explicitly disclaims variance estimates, which is no longer accurate.*

---

## 3.6 Training and Implementation

All models were fine-tuned on the D1 leakage-aware training partition and monitored on the
validation partition (Section 3.3), following a common training procedure. The elements
that define the procedure were held fixed across the three architectures: each model was
optimised with AdamW using a weight decay of 1×10??, trained with a standard multi-class
cross-entropy loss for a maximum of 20 epochs, and subject to early stopping. The learning
rate and batch size were the only training settings allowed to vary between architectures,
and were set to values appropriate to each model family, as described below. All settings
were specified in per-experiment configuration files rather than hard-coded, so that each
training run is fully described by a version-controlled configuration.

Model selection and early stopping were both governed by the macro-averaged F1 score on
the validation set. After every epoch the model was evaluated on the validation partition,
the checkpoint achieving the highest validation macro-F1 was retained as the final model,
and training was halted if the validation macro-F1 did not improve for five consecutive
epochs. Macro-averaged F1 was chosen as the monitoring criterion so that all four classes
contributed equally to model selection regardless of any residual class imbalance. No
learning-rate scheduler was applied; the learning rate was held constant throughout
training for each model.

### 3.6.1 Repeated training runs

Each architecture was trained five times, once at each of five random seeds (42, 43, 44,
45, 46), giving fifteen runs in total. All fifteen used the identical leakage-aware split
described in Section 3.3, identified by its SHA-256 hash, and the identical preprocessing
path described in Section 3.3.3. The seed was supplied to each run as an explicit
parameter rather than fixed globally, and was applied to the Python, NumPy and PyTorch
random number generators for both CPU and CUDA, to seeded DataLoader worker
initialisation, and to a seeded generator for shuffling, so that a run is reproducible
from its seed and configuration alone.

Repeating each configuration across seeds is a requirement of the study's design rather
than a robustness check added afterwards. The comparison being made is between
architectures, and a single run per architecture cannot distinguish a difference in
architecture from a difference in random initialisation and data ordering. Published
evidence indicates this distinction is not academic in medical imaging: repeated-seed
studies of segmentation and diagnostic classification report that the best-performing seed
of an algorithm can significantly outperform a substantial fraction of other seeds of the
same algorithm, and that a statistically significant difference between methods is
therefore a weak indicator of a true difference between them (Åkesson et al., 2024; Bosma
et al., 2023; Picard, 2021). Section 4.3 shows that this applies directly here: the spread
between architecture means in internal macro-F1 is only 2.52 times the mean seed-induced
standard deviation.

All quantities reported in Chapter 4 are therefore means with standard deviations across
the five seeds, and no result is reported from a single run. Where a single seed behaves
unusually, it is reported as such rather than averaged away or excluded (Section 4.9).

No cross-validation or hyperparameter search was performed. Learning rate and batch size
were set per architecture to conventional values for each model family and were not tuned,
so the study compares competently trained representatives of each family rather than
optimally tuned ones.

| Model | Batch size | Learning rate | Weight decay | Optimiser | Max epochs | Early-stop patience | Seeds |
|---|---|---|---|---|---|---|---|
| ResNet18 | 32 | 1×10?? | 1×10?? | AdamW | 20 | 5 | 42?46 |
| EfficientNet-B0 | 32 | 1×10?? | 1×10?? | AdamW | 20 | 5 | 42?46 |
| ViT-B/16 | 16 | 5×10?? | 1×10?? | AdamW | 20 | 5 | 42?46 |

**Table 3.6.** Training hyperparameters. Optimiser, weight decay, maximum epochs,
early-stopping patience, loss function and seed set were identical across architectures;
learning rate and batch size were set per architecture.

The learning rate and batch size differed by architecture because a single setting is not
equally appropriate across convolutional networks and transformers. The two convolutional
models were trained with a learning rate of 1×10?? and a batch size of 32, whereas
ViT-B/16 was trained with a smaller learning rate of 5×10?? and a batch size of 16. A
reduced learning rate is conventional when fine-tuning vision transformers, which are more
sensitive to large update steps than convolutional networks, and the smaller batch size
also reflected the memory footprint of the transformer on the available 12 GB GPU. The
comparison therefore holds the data, split, preprocessing, optimiser, loss, training
budget, early-stopping rule, model-selection criterion, seed set and evaluation protocol
fixed across the three models, while permitting the minimal architecture-appropriate
adjustment needed for each to train competently. Reliability differences are interpreted
against a shared training procedure rather than against identical numerical
hyperparameters, and the differing learning rate and batch size are noted as a factor that
a fully controlled comparison would ideally also equalise.

### 3.6.2 Run provenance

Each run wrote its outputs to a seed-scoped directory, so that runs of the same
architecture at different seeds could not overwrite one another. Alongside its metrics and
predictions, every run recorded a provenance record containing the run-set identifier, the
architecture, the seed, the git commit of the code that produced it, the SHA-256 hash of
the data-split file, and the SHA-256 hash of the resulting model checkpoint. This binds
every reported value to the exact code, data partition and trained weights that produced
it.

The summary generation described in Section 3.9 verifies these records before producing
any aggregate: it requires that all runs entering a summary share a single run-set
identifier, an identical split hash, matching seed sets across architectures, and
identical evaluation cohorts, and refuses to produce a summary otherwise. This check
exists because an earlier stage of the project assembled reported values from more than one
set of trained checkpoints, which is discussed in Section 5.2.

### 3.6.3 Computational environment

All experiments were run on a single desktop workstation with an NVIDIA GeForce RTX 3060
GPU (12 GB VRAM), an AMD Ryzen 5 5500G CPU, and 16 GB of system memory, under Ubuntu
22.04.5 LTS. Models were implemented in PyTorch 2.11.0 with torchvision 0.26.0 under
Python 3.10.12 and CUDA 13.0. Supporting steps used established libraries: scikit-learn
1.7.2 for classification and calibration metrics, ImageHash 4.3.2 for perceptual hashing
in the contamination audit (Section 3.4), and pydicom 3.0.2 with tcia_utils 3.3.1 for
DICOM handling and retrieval of the shifted-domain probes (Section 3.3). The precise
library versions and the git commit associated with each experiment were recorded as part
of the reproducibility procedure described in Section 3.9.

---

## Notes on what changed

**Removed.** The paragraph beginning "Each model was trained once, under the single fixed
seed, without repeated runs, cross-validation, or hyperparameter search," and the sentence
"All reported quantities are therefore single-run point estimates rather than averages over
multiple training runs, and no training-time variance or confidence intervals are
available." Both are now false.

**Removed.** "To support reproducibility, a single global random seed of 42 was set for
the Python, NumPy, and PyTorch (CPU and CUDA) random number generators at the start of
every run." The seed is now a run parameter.

**Added.** §3.6.1 on repeated runs, with the justification for why repetition is required
by the design rather than optional. §3.6.2 on provenance recording and the consistency
guard. §3.6.3 gathers the environment description that was previously trailing the section.

**Three new citations** ? Åkesson et al. (2024), Bosma et al. (2023), Picard (2021). All
three are in `CANONICAL_REFERENCES_45.md` §6, and all three are verified. They belong here
because a methods section asserting that repeated runs are necessary should say on what
evidence.

**Cross-reference added** to §5.2, so a reader encountering the provenance guard learns why
it exists rather than wondering.
