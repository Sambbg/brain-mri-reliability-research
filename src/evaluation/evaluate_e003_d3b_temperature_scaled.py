from pathlib import Path
import json
from collections import Counter

import numpy as np
import pandas as pd

PREDICTIONS_CSV = Path("experiments/E003_D1_efficientnet_b0_baseline/d3b_predictions.csv")
TEMP_METRICS_JSON = Path("experiments/E003_D1_efficientnet_b0_baseline/temperature_scaling_metrics.json")

OUT_PREDICTIONS_CSV = Path("experiments/E003_D1_efficientnet_b0_baseline/d3b_temperature_scaled_predictions.csv")
OUT_METRICS_JSON = Path("experiments/E003_D1_efficientnet_b0_baseline/d3b_temperature_scaled_metrics.json")
REPORT_PATH = Path("reports/experiments/E003_D3B_temperature_scaled_results.md")

CLASS_NAMES = ["glioma", "meningioma", "notumor", "pituitary"]
LOGIT_COLS = [f"logit_{c}" for c in CLASS_NAMES]


def softmax(logits):
    logits = np.asarray(logits, dtype=np.float64)
    logits = logits - np.max(logits, axis=1, keepdims=True)
    exp_logits = np.exp(logits)
    return exp_logits / np.sum(exp_logits, axis=1, keepdims=True)


def entropy_from_probs(probs):
    probs = np.asarray(probs, dtype=np.float64)
    probs = np.clip(probs, 1e-12, 1.0)
    return -np.sum(probs * np.log(probs), axis=1)


def load_temperature():
    if not TEMP_METRICS_JSON.exists():
        raise FileNotFoundError(f"Missing temperature metrics file: {TEMP_METRICS_JSON}")

    with TEMP_METRICS_JSON.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Try common keys from our temperature scaling script.
    for key in ["temperature", "learned_temperature", "optimal_temperature"]:
        if key in data:
            return float(data[key])

    # Try nested structure if present.
    if "temperature_scaling" in data and "temperature" in data["temperature_scaling"]:
        return float(data["temperature_scaling"]["temperature"])

    raise KeyError(
        f"Could not find temperature key in {TEMP_METRICS_JSON}. "
        f"Available keys: {list(data.keys())}"
    )


def summarise(df, prefix):
    n = len(df)
    pred_counts = df[f"{prefix}_pred_label"].value_counts().to_dict()
    pred_props = {label: pred_counts.get(label, 0) / n for label in CLASS_NAMES}

    metrics = {
        "n_slices": int(n),
        "n_patients": int(df["patient_id"].nunique()),
        "n_series": int(df["series_instance_uid"].nunique()),
        "glioma_prediction_rate": float(pred_props["glioma"]),
        "mean_glioma_probability": float(df[f"{prefix}_prob_glioma"].mean()),
        "median_glioma_probability": float(df[f"{prefix}_prob_glioma"].median()),
        "mean_max_confidence": float(df[f"{prefix}_max_confidence"].mean()),
        "median_max_confidence": float(df[f"{prefix}_max_confidence"].median()),
        "mean_entropy": float(df[f"{prefix}_entropy"].mean()),
        "median_entropy": float(df[f"{prefix}_entropy"].median()),
        "prediction_counts": {
            label: int(pred_counts.get(label, 0)) for label in CLASS_NAMES
        },
        "prediction_proportions": {
            label: float(pred_props[label]) for label in CLASS_NAMES
        },
    }

    patient_majority = {}
    for patient_id, group in df.groupby("patient_id"):
        counts = group[f"{prefix}_pred_label"].value_counts()
        patient_majority[patient_id] = counts.index[0]

    patient_majority_counts = Counter(patient_majority.values())
    metrics["patient_majority_prediction_counts"] = {
        label: int(patient_majority_counts.get(label, 0)) for label in CLASS_NAMES
    }
    metrics["patient_majority_glioma_rate"] = float(
        patient_majority_counts.get("glioma", 0) / max(len(patient_majority), 1)
    )

    series_majority = {}
    for series_uid, group in df.groupby("series_instance_uid"):
        counts = group[f"{prefix}_pred_label"].value_counts()
        series_majority[series_uid] = counts.index[0]

    series_majority_counts = Counter(series_majority.values())
    metrics["series_majority_prediction_counts"] = {
        label: int(series_majority_counts.get(label, 0)) for label in CLASS_NAMES
    }
    metrics["series_majority_glioma_rate"] = float(
        series_majority_counts.get("glioma", 0) / max(len(series_majority), 1)
    )

    return metrics


def write_report(temperature, raw_metrics, scaled_metrics):
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# E003 on D3B — Temperature-Scaled Domain-Shift Evaluation\n\n")

        f.write("## Experiment\n\n")
        f.write(
            "E003 EfficientNet-B0 trained on D1, evaluated on D3B ICDC-Glioma central slices. "
            "The temperature value was learned previously using the D1 validation set only.\n\n"
        )

        f.write("## Inputs\n\n")
        f.write(f"- Raw D3B predictions: `{PREDICTIONS_CSV}`\n")
        f.write(f"- Temperature metrics: `{TEMP_METRICS_JSON}`\n")
        f.write(f"- Learned temperature: `{temperature:.6f}`\n")
        f.write(f"- Slices evaluated: {scaled_metrics['n_slices']}\n")
        f.write(f"- Patients represented: {scaled_metrics['n_patients']}\n")
        f.write(f"- Series represented: {scaled_metrics['n_series']}\n\n")

        f.write("## Critical Interpretation Rule\n\n")
        f.write(
            "D3B is glioma-focused and does not contain the full four-class label set. "
            "This is not four-class external accuracy. It is a domain-shift confidence and "
            "prediction-distribution analysis.\n\n"
        )

        f.write("## Raw vs Temperature-Scaled Metrics\n\n")
        f.write("| Metric | Raw softmax | Temperature-scaled |\n")
        f.write("|---|---:|---:|\n")
        f.write(f"| Glioma prediction rate, slice-level | {raw_metrics['glioma_prediction_rate']:.4f} | {scaled_metrics['glioma_prediction_rate']:.4f} |\n")
        f.write(f"| Mean glioma probability | {raw_metrics['mean_glioma_probability']:.4f} | {scaled_metrics['mean_glioma_probability']:.4f} |\n")
        f.write(f"| Median glioma probability | {raw_metrics['median_glioma_probability']:.4f} | {scaled_metrics['median_glioma_probability']:.4f} |\n")
        f.write(f"| Mean max confidence | {raw_metrics['mean_max_confidence']:.4f} | {scaled_metrics['mean_max_confidence']:.4f} |\n")
        f.write(f"| Median max confidence | {raw_metrics['median_max_confidence']:.4f} | {scaled_metrics['median_max_confidence']:.4f} |\n")
        f.write(f"| Mean entropy | {raw_metrics['mean_entropy']:.4f} | {scaled_metrics['mean_entropy']:.4f} |\n")
        f.write(f"| Median entropy | {raw_metrics['median_entropy']:.4f} | {scaled_metrics['median_entropy']:.4f} |\n")
        f.write(f"| Patient-majority glioma rate | {raw_metrics['patient_majority_glioma_rate']:.4f} | {scaled_metrics['patient_majority_glioma_rate']:.4f} |\n")
        f.write(f"| Series-majority glioma rate | {raw_metrics['series_majority_glioma_rate']:.4f} | {scaled_metrics['series_majority_glioma_rate']:.4f} |\n")

        f.write("\n## Slice-Level Prediction Distribution\n\n")
        f.write("| Class | Raw count | Raw proportion | Scaled count | Scaled proportion |\n")
        f.write("|---|---:|---:|---:|---:|\n")
        for label in CLASS_NAMES:
            f.write(
                f"| {label} | "
                f"{raw_metrics['prediction_counts'][label]} | "
                f"{raw_metrics['prediction_proportions'][label]:.4f} | "
                f"{scaled_metrics['prediction_counts'][label]} | "
                f"{scaled_metrics['prediction_proportions'][label]:.4f} |\n"
            )

        f.write("\n## Patient-Level Majority Prediction Distribution\n\n")
        f.write("| Class | Raw patient count | Scaled patient count |\n")
        f.write("|---|---:|---:|\n")
        for label in CLASS_NAMES:
            f.write(
                f"| {label} | "
                f"{raw_metrics['patient_majority_prediction_counts'][label]} | "
                f"{scaled_metrics['patient_majority_prediction_counts'][label]} |\n"
            )

        f.write("\n## Interpretation\n\n")
        f.write(
            "Temperature scaling changes confidence values but does not retrain the model or change the underlying "
            "feature representation. If the prediction distribution remains unstable across D3B, this indicates that "
            "the issue is not merely calibration; it reflects domain-shift sensitivity in the trained classifier.\n"
        )


def main():
    if not PREDICTIONS_CSV.exists():
        raise FileNotFoundError(f"Missing predictions file: {PREDICTIONS_CSV}")

    df = pd.read_csv(PREDICTIONS_CSV)

    for col in LOGIT_COLS:
        if col not in df.columns:
            raise ValueError(f"Missing logit column: {col}")

    temperature = load_temperature()
    logits = df[LOGIT_COLS].to_numpy(dtype=np.float64)

    raw_probs = softmax(logits)
    scaled_probs = softmax(logits / temperature)

    # Add raw columns using recomputed probabilities for consistency.
    raw_pred_indices = np.argmax(raw_probs, axis=1)
    scaled_pred_indices = np.argmax(scaled_probs, axis=1)

    for idx, class_name in enumerate(CLASS_NAMES):
        df[f"raw_prob_{class_name}"] = raw_probs[:, idx]
        df[f"scaled_prob_{class_name}"] = scaled_probs[:, idx]

    df["raw_pred_index"] = raw_pred_indices
    df["raw_pred_label"] = [CLASS_NAMES[i] for i in raw_pred_indices]
    df["raw_max_confidence"] = np.max(raw_probs, axis=1)
    df["raw_entropy"] = entropy_from_probs(raw_probs)

    df["scaled_pred_index"] = scaled_pred_indices
    df["scaled_pred_label"] = [CLASS_NAMES[i] for i in scaled_pred_indices]
    df["scaled_max_confidence"] = np.max(scaled_probs, axis=1)
    df["scaled_entropy"] = entropy_from_probs(scaled_probs)

    df.to_csv(OUT_PREDICTIONS_CSV, index=False)

    raw_metrics = summarise(df, "raw")
    scaled_metrics = summarise(df, "scaled")

    metrics = {
        "temperature": float(temperature),
        "raw": raw_metrics,
        "temperature_scaled": scaled_metrics,
    }

    with OUT_METRICS_JSON.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    write_report(temperature, raw_metrics, scaled_metrics)

    print("D3B temperature-scaled evaluation complete.")
    print(json.dumps(metrics, indent=2))
    print(f"Predictions saved to: {OUT_PREDICTIONS_CSV}")
    print(f"Metrics saved to: {OUT_METRICS_JSON}")
    print(f"Report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
