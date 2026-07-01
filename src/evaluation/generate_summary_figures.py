from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


TABLE_DIR = Path("reports/experiments/tables")
FIG_DIR = Path("reports/experiments/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)


def save_figure(fig, filename: str):
    png_path = FIG_DIR / f"{filename}.png"
    pdf_path = FIG_DIR / f"{filename}.pdf"

    fig.tight_layout()
    fig.savefig(png_path, dpi=300, bbox_inches="tight")
    fig.savefig(pdf_path, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved: {png_path}")
    print(f"Saved: {pdf_path}")


def clean_model_names(series):
    return (
        series.str.replace("E001 ", "", regex=False)
        .str.replace("E002 ", "", regex=False)
        .str.replace("E003 ", "", regex=False)
    )


def figure_2_internal_macro_f1():
    df = pd.read_csv(TABLE_DIR / "table_2_internal_performance.csv")
    labels = clean_model_names(df["Model"])

    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(labels, df["Test macro-F1"])

    ax.set_title("Internal D1 Test Macro-F1 Across Models")
    ax.set_ylabel("Macro-F1")
    ax.set_ylim(0.94, 0.975)

    for bar, value in zip(bars, df["Test macro-F1"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.4f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    save_figure(fig, "figure_2_internal_macro_f1")


def figure_3_internal_ece_before_after():
    df = pd.read_csv(TABLE_DIR / "table_3_internal_calibration.csv")
    labels = clean_model_names(df["Model"])

    x = range(len(df))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars1 = ax.bar([i - width / 2 for i in x], df["Raw ECE"], width, label="Raw")
    bars2 = ax.bar([i + width / 2 for i in x], df["Scaled ECE"], width, label="Temperature-scaled")

    ax.set_title("Internal D1 Calibration: ECE Before and After Temperature Scaling")
    ax.set_ylabel("Expected Calibration Error")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.legend()

    for bars in [bars1, bars2]:
        for bar in bars:
            value = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                value,
                f"{value:.4f}",
                ha="center",
                va="bottom",
                fontsize=8,
            )

    save_figure(fig, "figure_3_internal_ece_before_after")


def figure_4_d3b_glioma_prediction_rate():
    df = pd.read_csv(TABLE_DIR / "table_4_d3b_domain_shift.csv")
    labels = clean_model_names(df["Model"])

    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(labels, df["Slice-level glioma prediction rate"])

    ax.axhline(0.5, linestyle="--", linewidth=1)
    ax.set_title("D3B Glioma Prediction Rate Across Models")
    ax.set_ylabel("Slice-level glioma prediction rate")
    ax.set_ylim(0, 0.6)

    for bar, value in zip(bars, df["Slice-level glioma prediction rate"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.4f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    save_figure(fig, "figure_4_d3b_glioma_prediction_rate")


def figure_5_d3b_prediction_distribution():
    model_dirs = {
        "ResNet18": Path("experiments/E001_D1_resnet18_baseline/d3b_domain_shift_metrics.json"),
        "EfficientNet-B0": Path("experiments/E002_D1_efficientnet_b0_baseline/d3b_domain_shift_metrics.json"),
        "ViT-B/16": Path("experiments/E003_D1_vit_b16_baseline/d3b_domain_shift_metrics.json"),
    }

    import json

    rows = []
    for model, path in model_dirs.items():
        with path.open("r", encoding="utf-8") as f:
            metrics = json.load(f)
        proportions = metrics["prediction_proportions"]
        rows.append({
            "Model": model,
            "glioma": proportions.get("glioma", 0),
            "meningioma": proportions.get("meningioma", 0),
            "notumor": proportions.get("notumor", 0),
            "pituitary": proportions.get("pituitary", 0),
        })

    df = pd.DataFrame(rows)

    fig, ax = plt.subplots(figsize=(8, 4.8))
    bottom = [0] * len(df)

    for cls in ["glioma", "meningioma", "notumor", "pituitary"]:
        ax.bar(df["Model"], df[cls], bottom=bottom, label=cls)
        bottom = [b + v for b, v in zip(bottom, df[cls])]

    ax.set_title("D3B Prediction Distribution Across Models")
    ax.set_ylabel("Prediction proportion")
    ax.set_ylim(0, 1.0)
    ax.legend(loc="upper right")

    save_figure(fig, "figure_5_d3b_prediction_distribution")


def figure_6_d3b_confidence_entropy_scaled():
    df = pd.read_csv(TABLE_DIR / "table_5_d3b_temperature_scaled.csv")
    labels = clean_model_names(df["Model"])

    x = range(len(df))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars1 = ax.bar([i - width / 2 for i in x], df["Raw mean max confidence"], width, label="Raw")
    bars2 = ax.bar([i + width / 2 for i in x], df["Scaled mean max confidence"], width, label="Temperature-scaled")

    ax.set_title("D3B Mean Maximum Confidence Before and After Temperature Scaling")
    ax.set_ylabel("Mean maximum confidence")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 0.8)
    ax.legend()

    for bars in [bars1, bars2]:
        for bar in bars:
            value = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                value,
                f"{value:.4f}",
                ha="center",
                va="bottom",
                fontsize=8,
            )

    save_figure(fig, "figure_6_d3b_confidence_softening")


def main():
    figure_2_internal_macro_f1()
    figure_3_internal_ece_before_after()
    figure_4_d3b_glioma_prediction_rate()
    figure_5_d3b_prediction_distribution()
    figure_6_d3b_confidence_entropy_scaled()

    print("\nAll summary figures generated successfully.")
    print(f"Output directory: {FIG_DIR}")


if __name__ == "__main__":
    main()
