from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.metrics import log_loss
import os

# Seed-scoped experiment directory. Training writes to <exp_dir>/seed<N>/, so a
# sweep does not overwrite itself. Set SEED to read a seed other than 42.
SEED_SUBDIR = "seed" + os.environ.get("SEED", "42")

PRED_PATH = Path(f"experiments/E002_D1_efficientnet_b0_baseline/{SEED_SUBDIR}/test_predictions.csv")
OUT_DIR = Path(f"experiments/E002_D1_efficientnet_b0_baseline/{SEED_SUBDIR}")
REPORT_PATH = Path("reports/experiments/E002_D1_calibration_results.md")

CLASS_NAMES = ["glioma", "meningioma", "notumor", "pituitary"]
PROB_COLS = [f"prob_{c}" for c in CLASS_NAMES]
N_BINS = 15


def normalize_probabilities(probs):
    probs = np.asarray(probs, dtype=np.float64)
    row_sums = probs.sum(axis=1, keepdims=True)

    if np.any(row_sums <= 0):
        raise ValueError("At least one probability row has non-positive sum.")

    return probs / row_sums


def expected_calibration_error(y_true, confidences, predictions, n_bins=15):
    y_true = np.asarray(y_true)
    confidences = np.asarray(confidences)
    predictions = np.asarray(predictions)

    bin_boundaries = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    rows = []

    for i in range(n_bins):
        lower = bin_boundaries[i]
        upper = bin_boundaries[i + 1]

        if i == 0:
            in_bin = (confidences >= lower) & (confidences <= upper)
        else:
            in_bin = (confidences > lower) & (confidences <= upper)

        count = int(np.sum(in_bin))

        if count == 0:
            rows.append({
                "bin": i + 1,
                "lower": lower,
                "upper": upper,
                "count": 0,
                "accuracy": np.nan,
                "confidence": np.nan,
                "gap": np.nan,
            })
            continue

        bin_accuracy = np.mean(y_true[in_bin] == predictions[in_bin])
        bin_confidence = np.mean(confidences[in_bin])
        gap = abs(bin_accuracy - bin_confidence)

        ece += (count / len(y_true)) * gap

        rows.append({
            "bin": i + 1,
            "lower": lower,
            "upper": upper,
            "count": count,
            "accuracy": bin_accuracy,
            "confidence": bin_confidence,
            "gap": gap,
        })

    return ece, pd.DataFrame(rows)


def multiclass_brier_score(y_true, probs, num_classes):
    y_onehot = np.eye(num_classes)[y_true]
    return np.mean(np.sum((probs - y_onehot) ** 2, axis=1))


def main():
    if not PRED_PATH.exists():
        raise FileNotFoundError(f"Predictions file not found: {PRED_PATH}")

    df = pd.read_csv(PRED_PATH)

    required_cols = {"true_index", "pred_index"} | set(PROB_COLS)
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in prediction CSV: {missing}")

    y_true = df["true_index"].to_numpy()
    y_pred = df["pred_index"].to_numpy()

    raw_probs = df[PROB_COLS].to_numpy(dtype=np.float64)
    raw_row_sums = raw_probs.sum(axis=1)

    probs = normalize_probabilities(raw_probs)
    normalized_row_sums = probs.sum(axis=1)

    confidences = np.max(probs, axis=1)

    accuracy = np.mean(y_true == y_pred)
    mean_confidence = np.mean(confidences)
    confidence_accuracy_gap = mean_confidence - accuracy

    ece, reliability_df = expected_calibration_error(
        y_true=y_true,
        confidences=confidences,
        predictions=y_pred,
        n_bins=N_BINS,
    )

    nll = log_loss(y_true, probs, labels=list(range(len(CLASS_NAMES))))
    brier = multiclass_brier_score(y_true, probs, num_classes=len(CLASS_NAMES))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    reliability_csv = OUT_DIR / "test_reliability_bins.csv"
    metrics_json = OUT_DIR / "calibration_metrics.json"

    reliability_df.to_csv(reliability_csv, index=False)

    metrics = {
        "n_samples": int(len(df)),
        "accuracy": float(accuracy),
        "mean_confidence": float(mean_confidence),
        "confidence_accuracy_gap": float(confidence_accuracy_gap),
        "ece_15_bins": float(ece),
        "brier_score": float(brier),
        "negative_log_likelihood": float(nll),
        "n_bins": N_BINS,
        "raw_probability_row_sum_min": float(raw_row_sums.min()),
        "raw_probability_row_sum_max": float(raw_row_sums.max()),
        "normalized_probability_row_sum_min": float(normalized_row_sums.min()),
        "normalized_probability_row_sum_max": float(normalized_row_sums.max()),
    }

    with metrics_json.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# E002 - Calibration Evaluation Results\n\n")

        f.write("## Experiment\n\n")
        f.write("E002 - D1 EfficientNet-B0 internal leakage-aware baseline\n\n")

        f.write("## Input\n\n")
        f.write(f"- Prediction file: `{PRED_PATH}`\n")
        f.write(f"- Samples evaluated: {len(df)}\n")
        f.write(f"- Number of reliability bins: {N_BINS}\n\n")

        f.write("## Probability Normalization Check\n\n")
        f.write(
            "Softmax probabilities were re-normalized after CSV loading to avoid minor floating-point "
            "row-sum warnings during NLL calculation.\n\n"
        )

        f.write("| Quantity | Value |\n")
        f.write("|---|---:|\n")
        f.write(f"| Raw probability row-sum minimum | {raw_row_sums.min():.10f} |\n")
        f.write(f"| Raw probability row-sum maximum | {raw_row_sums.max():.10f} |\n")
        f.write(f"| Normalized probability row-sum minimum | {normalized_row_sums.min():.10f} |\n")
        f.write(f"| Normalized probability row-sum maximum | {normalized_row_sums.max():.10f} |\n\n")

        f.write("## Calibration Metrics\n\n")
        f.write("| Metric | Value |\n")
        f.write("|---|---:|\n")
        f.write(f"| Accuracy | {accuracy:.4f} |\n")
        f.write(f"| Mean confidence | {mean_confidence:.4f} |\n")
        f.write(f"| Confidence - accuracy gap | {confidence_accuracy_gap:.4f} |\n")
        f.write(f"| Expected Calibration Error, 15 bins | {ece:.4f} |\n")
        f.write(f"| Brier score | {brier:.4f} |\n")
        f.write(f"| Negative Log-Likelihood | {nll:.4f} |\n\n")

        f.write("## Reliability Bin Table\n\n")
        f.write("| Bin | Confidence range | Count | Accuracy | Mean confidence | Gap |\n")
        f.write("|---:|---|---:|---:|---:|---:|\n")

        for _, row in reliability_df.iterrows():
            if row["count"] == 0:
                f.write(
                    f"| {int(row['bin'])} | "
                    f"{row['lower']:.2f}-{row['upper']:.2f} | "
                    f"0 | NA | NA | NA |\n"
                )
            else:
                f.write(
                    f"| {int(row['bin'])} | "
                    f"{row['lower']:.2f}-{row['upper']:.2f} | "
                    f"{int(row['count'])} | "
                    f"{row['accuracy']:.4f} | "
                    f"{row['confidence']:.4f} | "
                    f"{row['gap']:.4f} |\n"
                )

        f.write("\n## Interpretation\n\n")
        f.write(
            "This calibration evaluation measures whether the EfficientNet-B0 model's predicted confidence "
            "matches empirical correctness on the leakage-aware D1 test split. These results are internal "
            "to D1 and should not be interpreted as external reliability evidence.\n\n"
        )

        if confidence_accuracy_gap > 0:
            f.write(
                f"The model is overconfident on this internal test set: mean confidence is "
                f"{mean_confidence:.4f}, while accuracy is {accuracy:.4f}. "
                f"The confidence-accuracy gap is {confidence_accuracy_gap:.4f}.\n\n"
            )
        else:
            f.write(
                f"The model is underconfident on this internal test set: mean confidence is "
                f"{mean_confidence:.4f}, while accuracy is {accuracy:.4f}. "
                f"The confidence-accuracy gap is {confidence_accuracy_gap:.4f}.\n\n"
            )

        f.write(
            "The next step is to apply post-hoc temperature scaling using the validation set only, "
            "then evaluate the calibrated model on the held-out D1 test set.\n"
        )

    print("Calibration metrics:")
    print(json.dumps(metrics, indent=2))
    print(f"Reliability bins saved to: {reliability_csv}")
    print(f"Metrics saved to: {metrics_json}")
    print(f"Report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
