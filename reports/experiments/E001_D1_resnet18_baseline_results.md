# E001 ? D1 ResNet18 Internal Leakage-Aware Baseline Results

## Experiment ID
E001

## Model
ResNet18, ImageNet-pretrained

## Dataset
D1 ? Nickparvar Kaggle Brain Tumor MRI Dataset

## Split
Leakage-aware D1 split:

| Split | Count |
|---|---:|
| Train | 4,909 |
| Validation | 1,053 |
| Test | 1,051 |

The split was created after exact duplicate removal and perceptual-hash near-duplicate grouping. The original Kaggle Training/Testing split was not used for this baseline.

## Environment

| Item | Value |
|---|---|
| Device | CUDA |
| GPU | NVIDIA GeForce RTX 3060 |
| PyTorch | 2.11.0+cu130 |
| CUDA | 13.0 |
| Git commit used for training | `1e58940d3617b674593a55ef97cd66a949c13154` |

## Training Configuration

| Setting | Value |
|---|---|
| Image size | 224 × 224 |
| Input channels | 3 |
| Grayscale handling | Converted to RGB |
| Optimizer | AdamW |
| Learning rate | 0.0001 |
| Weight decay | 0.0001 |
| Loss | Cross-entropy |
| Batch size | 32 |
| Max epochs | 20 |
| Early stopping | Enabled |
| Patience | 5 |
| Seed | 42 |

## Training Outcome

| Item | Value |
|---|---:|
| Best epoch | 8 |
| Best validation macro-F1 | 0.9704 |
| Early stopping epoch | 13 |

## Test Results

| Metric | Value |
|---|---:|
| Test loss | 0.1176 |
| Test accuracy | 0.9667 |
| Test balanced accuracy | 0.9662 |
| Test macro-F1 | 0.9666 |

## Per-Class Test Results

| Class | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| Glioma | 0.9886 | 0.9665 | 0.9774 | 269 |
| Meningioma | 0.9225 | 0.9813 | 0.9510 | 267 |
| Notumor | 0.9790 | 0.9283 | 0.9530 | 251 |
| Pituitary | 0.9812 | 0.9886 | 0.9849 | 264 |

## Confusion Matrix

| True / Predicted | Glioma | Meningioma | Notumor | Pituitary |
|---|---:|---:|---:|---:|
| Glioma | 260 | 5 | 4 | 0 |
| Meningioma | 2 | 262 | 1 | 2 |
| Notumor | 1 | 14 | 233 | 3 |
| Pituitary | 0 | 3 | 0 | 261 |

## Interpretation

This experiment confirms that the training pipeline is functional and that a standard CNN baseline can achieve strong internal performance on the D1 leakage-aware split.

However, this result must not be interpreted as evidence of clinical reliability. D1 remains a public 2D benchmark without patient identifiers. External dataset evaluation and calibration metrics are still required before reliability claims can be made.

## Key Observation

The weakest recall was observed for the `notumor` class. This should be monitored in later experiments because the `notumor` class was also strongly affected by duplicate removal during dataset cleaning.

## Next Required Experiments

1. Compute calibration metrics for E001:
   - Expected Calibration Error
   - Brier score
   - Negative Log-Likelihood
   - Reliability diagram

2. Repeat baseline with at least two additional seeds.

3. Acquire and process an independent external dataset.

4. Run train-D1/test-external evaluation.
