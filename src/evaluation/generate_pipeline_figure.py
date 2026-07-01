from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


OUT_DIR = Path("reports/experiments/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def add_box(ax, x, y, w, h, text, fontsize=8.5):
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        linewidth=1.2,
        facecolor="white",
        edgecolor="black",
    )
    ax.add_patch(box)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        wrap=True,
    )


def add_arrow(ax, x1, y1, x2, y2):
    arrow = FancyArrowPatch(
        (x1, y1),
        (x2, y2),
        arrowstyle="->",
        mutation_scale=12,
        linewidth=1.1,
        color="black",
    )
    ax.add_patch(arrow)


def main():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")

    ax.text(
        7,
        7.55,
        "Figure 1. Reliability-First Evaluation Pipeline",
        ha="center",
        va="center",
        fontsize=15,
        fontweight="bold",
    )

    w = 2.25
    h = 0.78

    # Row 1: D1 internal workflow
    add_box(ax, 0.5, 6.2, w, h, "D1 dataset\nmanifest creation")
    add_box(ax, 3.1, 6.2, w, h, "Exact duplicate\naudit")
    add_box(ax, 5.7, 6.2, w, h, "Leakage-aware\ntrain/val/test split")
    add_box(ax, 8.3, 6.2, w, h, "Train E001/E002/E003\non D1")
    add_box(ax, 10.9, 6.2, w, h, "Internal D1\nclassification metrics")

    # Row 2: calibration
    add_box(ax, 3.1, 4.65, w, h, "Internal D1\ncalibration metrics")
    add_box(ax, 5.7, 4.65, w, h, "Temperature scaling\nfit on validation logits")
    add_box(ax, 8.3, 4.65, w, h, "Temperature-scaled\nD1 test evaluation")

    # Row 3: external dataset audit
    add_box(ax, 0.5, 3.1, w, h, "Candidate external\nD2")
    add_box(ax, 3.1, 3.1, w, h, "D1-D2 exact +\npHash overlap audit")
    add_box(ax, 5.7, 3.1, w, h, "Reject D2 as\nclean external evidence")

    add_box(ax, 8.3, 3.1, w, h, "D3B ICDC-Glioma\nseries selection")
    add_box(ax, 10.9, 3.1, w, h, "DICOM inspection +\ncentral-slice conversion")

    # Row 4: D3B evaluation
    add_box(ax, 3.1, 1.55, w, h, "D1-D3B exact +\npHash overlap audit")
    add_box(ax, 5.7, 1.55, w, h, "D3B domain-shift\nprediction analysis")
    add_box(ax, 8.3, 1.55, w, h, "D3B temperature-scaled\nconfidence analysis")
    add_box(ax, 10.9, 1.55, w, h, "Cross-model\nreliability comparison")

    # Arrows row 1
    add_arrow(ax, 2.75, 6.59, 3.1, 6.59)
    add_arrow(ax, 5.35, 6.59, 5.7, 6.59)
    add_arrow(ax, 7.95, 6.59, 8.3, 6.59)
    add_arrow(ax, 10.55, 6.59, 10.9, 6.59)

    # Calibration branch
    add_arrow(ax, 12.0, 6.2, 4.2, 5.43)
    add_arrow(ax, 5.35, 5.04, 5.7, 5.04)
    add_arrow(ax, 7.95, 5.04, 8.3, 5.04)

    # D2 branch
    add_arrow(ax, 2.75, 3.49, 3.1, 3.49)
    add_arrow(ax, 5.35, 3.49, 5.7, 3.49)

    # D3B branch
    add_arrow(ax, 10.55, 3.49, 10.9, 3.49)
    add_arrow(ax, 12.0, 3.1, 4.2, 2.33)
    add_arrow(ax, 5.35, 1.94, 5.7, 1.94)
    add_arrow(ax, 7.95, 1.94, 8.3, 1.94)
    add_arrow(ax, 10.55, 1.94, 10.9, 1.94)

    ax.text(
        7,
        0.65,
        "Reliability claim requires: leakage-aware splitting + overlap auditing + calibration + domain-shift testing.",
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold",
    )

    png_path = OUT_DIR / "figure_1_reliability_pipeline.png"
    pdf_path = OUT_DIR / "figure_1_reliability_pipeline.pdf"

    fig.savefig(png_path, dpi=300, bbox_inches="tight")
    fig.savefig(pdf_path, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved: {png_path}")
    print(f"Saved: {pdf_path}")


if __name__ == "__main__":
    main()
