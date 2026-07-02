"""
Generate D3C summary tables and figures, plus a cross-dataset (D1 / D3B / D3C)
comparison. Companion to generate_summary_tables.py and generate_summary_figures.py;
does not modify the existing D3B generators. Reads metrics already written by the
D3C evaluation scripts.
"""
from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt

TABLE_DIR = Path("reports/experiments/tables")
FIG_DIR = Path("reports/experiments/figures")
TABLE_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

MODELS = {
    "E001 ResNet18": Path("experiments/E001_D1_resnet18_baseline"),
    "E002 EfficientNet-B0": Path("experiments/E002_D1_efficientnet_b0_baseline"),
    "E003 ViT-B/16": Path("experiments/E003_D1_vit_b16_baseline"),
}
SHORT = {"E001 ResNet18": "ResNet18", "E002 EfficientNet-B0": "EfficientNet-B0", "E003 ViT-B/16": "ViT-B/16"}
CLASSES = ["glioma", "meningioma", "notumor", "pituitary"]


def load_json(path):
    if not path.exists():
        raise FileNotFoundError("Missing required file: " + str(path))
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def r(x, n=4):
    return round(x, n) if isinstance(x, (int, float)) else x


def save_table(df, name):
    p = TABLE_DIR / (name + ".csv")
    df.to_csv(p, index=False)
    print("Saved:", p)


def save_figure(fig, name):
    fig.tight_layout()
    fig.savefig(FIG_DIR / (name + ".png"), dpi=300, bbox_inches="tight")
    fig.savefig(FIG_DIR / (name + ".pdf"), bbox_inches="tight")
    plt.close(fig)
    print("Saved:", FIG_DIR / (name + ".png"))


def table_d3c_domain_shift():
    rows = []
    for name, exp in MODELS.items():
        m = load_json(exp / "d3c_domain_shift_metrics.json")
        rows.append({
            "Model": name, "D3C slices": m.get("n_slices"), "D3C patients": m.get("n_patients"),
            "D3C series": m.get("n_series"),
            "Slice-level glioma prediction rate": r(m.get("glioma_prediction_rate")),
            "Patient-majority glioma rate": r(m.get("patient_majority_glioma_rate")),
            "Series-majority glioma rate": r(m.get("series_majority_glioma_rate")),
            "Mean glioma probability": r(m.get("mean_glioma_probability")),
            "Median glioma probability": r(m.get("median_glioma_probability")),
            "Mean max confidence": r(m.get("mean_max_confidence")),
            "Mean entropy": r(m.get("mean_entropy")),
        })
    save_table(pd.DataFrame(rows), "table_6_d3c_domain_shift")


def table_d3c_temperature_scaled():
    rows = []
    for name, exp in MODELS.items():
        m = load_json(exp / "d3c_temperature_scaled_metrics.json")
        raw, sc = m.get("raw", {}), m.get("temperature_scaled", {})
        rows.append({
            "Model": name, "Temperature": r(m.get("temperature")),
            "Raw glioma prediction rate": r(raw.get("glioma_prediction_rate")),
            "Scaled glioma prediction rate": r(sc.get("glioma_prediction_rate")),
            "Raw mean max confidence": r(raw.get("mean_max_confidence")),
            "Scaled mean max confidence": r(sc.get("mean_max_confidence")),
            "Raw mean entropy": r(raw.get("mean_entropy")),
            "Scaled mean entropy": r(sc.get("mean_entropy")),
        })
    save_table(pd.DataFrame(rows), "table_7_d3c_temperature_scaled")


def table_cross_dataset():
    rows = []
    for name, exp in MODELS.items():
        d3c = load_json(exp / "d3c_domain_shift_metrics.json")
        d3b = load_json(exp / "d3b_domain_shift_metrics.json")
        internal = load_json(exp / "final_results.json")
        f1 = internal.get("test_macro_f1", internal.get("macro_f1", internal.get("test_macro_f1_score")))
        rows.append({
            "Model": name,
            "D1 internal macro-F1": r(f1),
            "D3B glioma rate (canine)": r(d3b.get("glioma_prediction_rate")),
            "D3C glioma rate (human)": r(d3c.get("glioma_prediction_rate")),
        })
    save_table(pd.DataFrame(rows), "table_8_cross_dataset_comparison")
    return pd.DataFrame(rows)


def fig_d3c_glioma_rate():
    labels, rates = [], []
    for name, exp in MODELS.items():
        m = load_json(exp / "d3c_domain_shift_metrics.json")
        labels.append(SHORT[name]); rates.append(m.get("glioma_prediction_rate"))
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(labels, rates)
    ax.axhline(0.5, linestyle="--", linewidth=1)
    ax.set_title("D3C (Human) Glioma Prediction Rate Across Models")
    ax.set_ylabel("Slice-level glioma prediction rate"); ax.set_ylim(0, 1)
    for b, v in zip(bars, rates):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.02, f"{v:.4f}", ha="center")
    save_figure(fig, "figure_7_d3c_glioma_prediction_rate")


def fig_d3c_distribution():
    props = {}
    for name, exp in MODELS.items():
        m = load_json(exp / "d3c_domain_shift_metrics.json")
        props[SHORT[name]] = m.get("prediction_proportions", {})
    fig, ax = plt.subplots(figsize=(7, 4.5))
    labels = list(props.keys()); bottoms = [0] * len(labels)
    for cls in CLASSES:
        vals = [props[l].get(cls, 0) for l in labels]
        ax.bar(labels, vals, bottom=bottoms, label=cls)
        bottoms = [b + v for b, v in zip(bottoms, vals)]
    ax.set_title("D3C Prediction Distribution Across Models")
    ax.set_ylabel("Prediction proportion"); ax.set_ylim(0, 1); ax.legend()
    save_figure(fig, "figure_8_d3c_prediction_distribution")


def fig_cross_dataset(df):
    import numpy as np
    labels = [SHORT[m] for m in df["Model"]]
    x = np.arange(len(labels)); w = 0.25
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(x - w, df["D1 internal macro-F1"], w, label="D1 internal macro-F1")
    ax.bar(x, df["D3B glioma rate (canine)"], w, label="D3B glioma rate (canine)")
    ax.bar(x + w, df["D3C glioma rate (human)"], w, label="D3C glioma rate (human)")
    ax.set_xticks(x); ax.set_xticklabels(labels)
    ax.set_title("Internal Accuracy vs Shifted-Domain Glioma Prediction Rate")
    ax.set_ylabel("Score / rate"); ax.set_ylim(0, 1); ax.legend()
    save_figure(fig, "figure_9_cross_dataset_comparison")


def main():
    table_d3c_domain_shift()
    table_d3c_temperature_scaled()
    df = table_cross_dataset()
    fig_d3c_glioma_rate()
    fig_d3c_distribution()
    fig_cross_dataset(df)
    print("\nD3C summary tables and figures generated.")


if __name__ == "__main__":
    main()

