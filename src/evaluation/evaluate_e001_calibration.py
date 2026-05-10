from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.metrics import log_loss, brier_score_loss

PRED_PATH = Path("experiments/E001_D1_resnet18_baseline/test_predictions.csv")
OUT_DIR = Path("experiments/E001_D1_resnet18_baseline")
REPORT_PATH = Path("reports/experiments/E001_D1_calibration_results.md")

CLASS_NAMES = ["glioma", "meningioma", "notumor", "pituitary"]
PROB_COLS = [f"prob_{c}" for c in CLASS_NAMES]
N_BINS = 15


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

    y_true = df["true_index"].to_numpy()
    y_pred = df["pred_index"].to_numpy()
    probs = df[PROB_COLS].to_numpy()

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
    }

    with metrics_json.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# E001 ? Calibration Evaluation Results\n\n")

        f.write("## Experiment\n\n")
        f.write("E001 ? D1 ResNet18 internal leakage-aware baseline\n\n")

        f.write("## Input\n\n")
        f.write(f"- Prediction file: `{PRED_PATH}`\n")
        f.write(f"- Samples evaluated: {len(df)}\n")
        f.write(f"- Number of reliability bins: {N_BINS}\n\n")

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
            "This calibration evaluation measures whether the ResNet18 model's predicted confidence "
            "matches empirical correctness on the leakage-aware D1 test split. These results are still "
            "internal to D1 and should not be interpreted as external reliability evidence. The next step "
            "is to apply post-hoc calibration, especially temperature scaling, using the validation set only.\n"
        )

    print("Calibration metrics:")
    print(json.dumps(metrics, indent=2))
    print(f"Reliability bins saved to: {reliability_csv}")
    print(f"Metrics saved to: {metrics_json}")
    print(f"Report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
