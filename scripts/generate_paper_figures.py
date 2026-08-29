#!/usr/bin/env python3
"""
Generate all manuscript figures from the seed-sweep artefacts.

Every figure is built directly from experiments/<EXP>/seed<N>/, not from any
intermediate summary, so a figure cannot disagree with the runs that produced it.
Figure numbering matches the manuscript.

    Figure 1  System architecture (schematic)
    Figure 2  Per-seed internal performance with signal-to-noise
    Figure 3  Reliability diagrams, raw and temperature-scaled
    Figure 4  Internal near-parity beside shifted-domain divergence
    Figure 5  Predicted-class distribution on both probes
    Figure 6  Glioma prediction rate against mean maximum confidence
    Figure 7  Correlation decomposition

Run from the repo root:
    python scripts/generate_paper_figures.py

Outputs 300 dpi PNG and vector PDF to reports/experiments/consolidated/paper_figures/.
"""

import csv
import json
import statistics as st
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

EXPERIMENTS = Path("experiments")
OUT = Path("reports/experiments/consolidated/paper_figures")

ARCH = {"E001": "ResNet18", "E002": "EfficientNet-B0", "E003": "ViT-B/16"}
ORDER = ["E001", "E002", "E003"]
CLASSES = ["glioma", "meningioma", "notumor", "pituitary"]
CLASS_LABELS = ["Glioma", "Meningioma", "No tumour", "Pituitary"]

# Colourblind-safe (Okabe-Ito), distinguishable in greyscale
COLOUR = {"E001": "#0072B2", "E002": "#009E73", "E003": "#D55E00"}
MARKER = {"E001": "o", "E002": "s", "E003": "^"}

# Publication styling
plt.rcParams.update({
    # Type 42 (TrueType) rather than the matplotlib default Type 3.
    # Type 3 text is not Unicode-mappable and is rejected by IEEE PDF eXpress
    # and flagged by several publishers. This is not optional for submission.
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "font.family": "serif",
    "font.serif": ["Liberation Serif", "DejaVu Serif"],
    # keep maths in the same family so one figure uses one typeface
    "mathtext.fontset": "custom",
    "mathtext.rm": "Liberation Serif",
    "mathtext.it": "Liberation Serif:italic",
    "mathtext.bf": "Liberation Serif:bold",
    "mathtext.cal": "Liberation Serif:italic",
    "mathtext.sf": "Liberation Serif",
    "mathtext.tt": "Liberation Serif",
    "font.size": 9,
    "axes.labelsize": 9,
    "axes.titlesize": 9.5,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "axes.linewidth": 0.8,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linewidth": 0.5,
    "axes.axisbelow": True,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
})

MM = 1 / 25.4  # millimetres to inches; journals specify column widths in mm
SINGLE_COL = 90 * MM
DOUBLE_COL = 190 * MM


# ----------------------------------------------------------------- loading

def dig(obj, key):
    """First value for `key` at any nesting depth."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key and not isinstance(v, (dict, list)):
                return v
            if isinstance(v, dict):
                found = dig(v, key)
                if found is not None:
                    return found
    return None


def load_runs():
    """One record per run, read straight from the per-seed artefacts."""
    if not EXPERIMENTS.is_dir():
        sys.exit("No experiments/ directory. Run this from the repo root.")

    runs = []
    for exp_dir in sorted(p for p in EXPERIMENTS.iterdir() if p.is_dir()):
        exp_id = exp_dir.name.split("_")[0]
        if exp_id not in ARCH:
            continue
        for sd in sorted(p for p in exp_dir.iterdir() if p.is_dir()):
            if not sd.name.startswith("seed"):
                continue
            final = sd / "final_results.json"
            if not final.exists():
                continue

            with open(final) as fh:
                fr = json.load(fh)
            rec = {
                "exp": exp_id,
                "arch": ARCH[exp_id],
                "seed": int(sd.name.replace("seed", "")),
                "macro_f1": fr.get("test_macro_f1"),
                "accuracy": fr.get("test_accuracy"),
            }

            ts = sd / "temperature_scaling_metrics.json"
            if ts.exists():
                with open(ts) as fh:
                    t = json.load(fh)
                rec["temperature"] = t.get("learned_temperature")

            for probe in ("d3b", "d3c"):
                dm = sd / f"{probe}_domain_shift_metrics.json"
                if dm.exists():
                    with open(dm) as fh:
                        d = json.load(fh)
                    rec[f"{probe}_rate"] = d.get("glioma_prediction_rate")
                    rec[f"{probe}_conf"] = d.get("mean_max_confidence")
                    rec[f"{probe}_entropy"] = d.get("mean_entropy")
                    rec[f"{probe}_median_glioma"] = d.get("median_glioma_probability")
                    props = d.get("prediction_proportions") or {}
                    for cls in CLASSES:
                        rec[f"{probe}_pred_{cls}"] = props.get(cls)
            runs.append(rec)

    if not runs:
        sys.exit("No runs found under experiments/.")
    return runs


def load_reliability():
    """Count-weighted reliability bins pooled across seeds."""
    acc = {}
    for exp_dir in sorted(p for p in EXPERIMENTS.iterdir() if p.is_dir()):
        exp_id = exp_dir.name.split("_")[0]
        if exp_id not in ARCH:
            continue
        for sd in sorted(p for p in exp_dir.iterdir() if p.is_dir()):
            if not sd.name.startswith("seed"):
                continue
            for tag, fname in (("raw", "test_reliability_bins.csv"),
                               ("scaled",
                                "test_temperature_scaled_reliability_bins.csv")):
                path = sd / fname
                if not path.exists():
                    continue
                with open(path) as fh:
                    for row in csv.DictReader(fh):
                        try:
                            n = float(row["count"])
                        except (KeyError, ValueError):
                            continue
                        if n == 0 or not row.get("accuracy"):
                            continue
                        b = int(row["bin"])
                        d = acc.setdefault((exp_id, tag), {}).setdefault(
                            b, {"n": 0.0, "acc": 0.0, "conf": 0.0})
                        d["n"] += n
                        d["acc"] += float(row["accuracy"]) * n
                        d["conf"] += float(row["confidence"]) * n
    return acc


def vals(runs, exp_id, key):
    return [r[key] for r in runs if r["exp"] == exp_id and r.get(key) is not None]


def snr(runs, key):
    """Between-architecture spread over mean within-architecture SD."""
    means, sds = {}, {}
    for e in ORDER:
        v = vals(runs, e, key)
        if len(v) > 1:
            means[e], sds[e] = st.mean(v), st.stdev(v)
    if len(means) < 2:
        return None
    spread = max(means.values()) - min(means.values())
    mean_sd = st.mean(list(sds.values()))
    return spread / mean_sd if mean_sd else None


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = st.mean(xs), st.mean(ys)
    num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    den = (sum((a - mx) ** 2 for a in xs) * sum((b - my) ** 2 for b in ys)) ** 0.5
    return num / den if den else None


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf"):
        path = OUT / f"{name}.{ext}"
        fig.savefig(path)
        print(f"  {path}")
    plt.close(fig)


def check_fonts():
    """Confirm no Type 3 fonts were emitted. Requires pdffonts (poppler-utils)."""
    import shutil
    import subprocess
    if not shutil.which("pdffonts"):
        print("\n  pdffonts not found; skipping font check.")
        print("  Install poppler-utils to verify no Type 3 fonts were emitted.")
        return
    bad = []
    for pdf in sorted(OUT.glob("*.pdf")):
        out = subprocess.run(["pdffonts", str(pdf)],
                             capture_output=True, text=True).stdout
        if "Type 3" in out:
            bad.append(pdf.name)
    if bad:
        print("\n  WARNING: Type 3 fonts found in: " + ", ".join(bad))
        print("  These are rejected by IEEE PDF eXpress and flagged by other")
        print("  publishers. Check that pdf.fonttype is set to 42.")
    else:
        print("\n  Font check passed: no Type 3 fonts in any PDF.")


# ------------------------------------------------- Figure 1: architecture

def figure_1_architecture():
    """Schematic pipeline. Not data-driven; drawn for consistency of style."""
    fig, ax = plt.subplots(figsize=(DOUBLE_COL, 105 * MM))
    ax.set_xlim(0, 100)
    ax.set_ylim(-10, 118)
    ax.axis("off")

    def box(x, y, w, h, text, fc="#F2F2F2", ec="#333333", size=7.6, bold=False):
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.6,rounding_size=1.2",
            facecolor=fc, edgecolor=ec, linewidth=0.9))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=size, weight="bold" if bold else "normal", linespacing=1.35)

    def diamond(x, y, w, h, text):
        ax.add_patch(plt.Polygon(
            [(x + w / 2, y + h), (x + w, y + h / 2), (x + w / 2, y), (x, y + h / 2)],
            facecolor="#FFF4E0", edgecolor="#333333", linewidth=0.9))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=7.2, linespacing=1.3)

    def arrow(x1, y1, x2, y2, label=None, lx=0, ly=0):
        ax.add_patch(FancyArrowPatch(
            (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=9,
            linewidth=0.9, color="#333333",
            connectionstyle="arc3,rad=0", shrinkA=1, shrinkB=1))
        if label:
            ax.text((x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly, label,
                    fontsize=6.8, ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none"))

    # Stage 1: data
    box(2, 104, 26, 10, "D1 internal\n(four-class, 7,013)", fc="#DCE9F5")
    box(31, 104, 22, 10, "D2 candidate\nexternal set", fc="#DCE9F5")
    box(56, 104, 20, 10, "D3B probe\n(canine)", fc="#DCE9F5")
    box(79, 104, 19, 10, "D3C probe\n(human)", fc="#DCE9F5")

    # Stage 2: preparation
    box(2, 88, 26, 10, "Exact + perceptual\ndeduplication")
    box(56, 88, 42, 10, "Series selection and\ncentral-slice extraction")

    arrow(15, 104, 15, 98)
    arrow(67, 104, 67, 98)
    arrow(88, 104, 88, 98)

    # Stage 3: audit
    box(20, 73, 60, 9, "Contamination audit against D1\n(SHA-256 exact + pHash near-duplicate)", bold=True)
    arrow(15, 88, 30, 82)
    arrow(42, 104, 50, 82)
    arrow(77, 88, 62, 82)

    diamond(33, 58, 34, 12, "Independent of D1?")
    arrow(50, 73, 50, 70)

    box(2, 58, 27, 10, "Reject D2\n(4,740 byte-identical)", fc="#F8DCDC")
    box(71, 58, 27, 10, "Retain as\nshifted-domain probes", fc="#DDF0E4")
    arrow(33, 64, 29, 64, "No", 0, 2.6)
    arrow(67, 64, 71, 64, "Yes", 0, 2.6)

    # Stage 4: split and training
    box(14, 43, 40, 9, "Leakage-aware split 70/15/15\n(whole near-duplicate groups)")
    arrow(15, 88, 15, 52)

    box(14, 28, 40, 10, "Train ResNet18 \u00b7 EfficientNet-B0 \u00b7 ViT-B/16\n5 seeds each \u2192 15 runs", fc="#E8E2F5", bold=True)
    arrow(34, 43, 34, 38)

    box(60, 28, 38, 10, "Per-run provenance\n(commit \u00b7 seed \u00b7 split \u00b7 checkpoint)")
    arrow(54, 33, 60, 33)

    # Stage 5: evaluation
    box(2, 12, 29, 10, "Layer 1\nInternal classification")
    box(35, 12, 29, 10, "Layer 2\nCalibration \u00B1 scaling")
    box(68, 12, 30, 10, "Layer 3\nShifted-domain behaviour")
    arrow(24, 28, 16, 22)
    arrow(34, 28, 49, 22)
    arrow(44, 28, 83, 22)
    arrow(85, 58, 92, 22)

    box(20, -8, 60, 8, "Reliability evidence: performance, dispersion across seeds,\ncalibration, and behaviour under shift", fc="#EDEDED", bold=True)
    arrow(16, 12, 34, 0.5)
    arrow(49, 12, 50, 0.5)
    arrow(83, 12, 66, 0.5)

    save(fig, "figure_1_system_architecture")


# --------------------------------------- Figure 2: internal per-seed spread

def figure_2_internal(runs):
    fig, ax = plt.subplots(figsize=(SINGLE_COL, 68 * MM))
    rng = np.random.default_rng(42)

    for i, e in enumerate(ORDER):
        v = vals(runs, e, "macro_f1")
        jitter = rng.uniform(-0.09, 0.09, len(v))
        ax.scatter(np.full(len(v), i) + jitter, v, s=26, color=COLOUR[e],
                   marker=MARKER[e], alpha=0.75, edgecolor="white", linewidth=0.5,
                   zorder=3)
        mean, sd = st.mean(v), st.stdev(v)
        ax.hlines(mean, i - 0.26, i + 0.26, color=COLOUR[e], linewidth=2.0, zorder=4)
        ax.add_patch(plt.Rectangle((i - 0.26, mean - sd), 0.52, 2 * sd,
                                   facecolor=COLOUR[e], alpha=0.13, zorder=1))

    ratio = snr(runs, "macro_f1")
    means = [st.mean(vals(runs, e, "macro_f1")) for e in ORDER]
    spread = max(means) - min(means)
    mean_sd = st.mean([st.stdev(vals(runs, e, "macro_f1")) for e in ORDER])

    ax.set_xticks(range(3))
    ax.set_xticklabels([ARCH[e] for e in ORDER], rotation=12, ha="right")
    ax.set_ylabel("Internal test macro-F1")
    ax.set_ylim(0.948, 0.978)
    ax.text(0.98, 0.04,
            f"spread = {spread:.4f}\nmean seed SD = {mean_sd:.4f}\nSNR = {ratio:.2f}",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=7.4,
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#999999", lw=0.6))
    save(fig, "figure_2_internal_seed_spread")


# ------------------------------------------- Figure 3: reliability diagrams

def figure_3_reliability(rel):
    fig, axes = plt.subplots(1, 3, figsize=(DOUBLE_COL, 62 * MM), sharey=True)
    for ax, e in zip(axes, ORDER):
        ax.plot([0, 1], [0, 1], "--", color="#888888", linewidth=0.8,
                label="Perfect calibration", zorder=1)
        for tag, style, lbl in (("raw", "-", "Raw"),
                                ("scaled", "--", "Temperature-scaled")):
            bins = rel.get((e, tag))
            if not bins:
                continue
            conf, acc = [], []
            for b, d in sorted(bins.items()):
                if d["n"] < 5:
                    continue
                conf.append(d["conf"] / d["n"])
                acc.append(d["acc"] / d["n"])
            ax.plot(conf, acc, style, marker=MARKER[e], markersize=3.4,
                    linewidth=1.3, color=COLOUR[e],
                    markerfacecolor=COLOUR[e] if tag == "raw" else "white",
                    label=lbl, zorder=3)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xlabel("Confidence")
        ax.set_title(f"({chr(97 + ORDER.index(e))}) {ARCH[e]}", loc="left")
        ax.set_aspect("equal", adjustable="box")
        ax.legend(loc="upper left", frameon=True, framealpha=0.9)
    axes[0].set_ylabel("Accuracy")
    save(fig, "figure_3_reliability_diagrams")


# ----------------------------- Figure 4: internal versus shifted-domain

def figure_4_internal_vs_shift(runs):
    fig, ax = plt.subplots(figsize=(DOUBLE_COL * 0.72, 68 * MM))
    groups = [("Internal\nmacro-F1", "macro_f1"),
              ("D3B glioma rate\n(canine, n = 53)", "d3b_rate"),
              ("D3C glioma rate\n(human, n = 610)", "d3c_rate")]
    x = np.arange(len(groups))
    width = 0.26

    for i, e in enumerate(ORDER):
        means = [st.mean(vals(runs, e, k)) for _, k in groups]
        sds = [st.stdev(vals(runs, e, k)) for _, k in groups]
        ax.bar(x + (i - 1) * width, means, width, yerr=sds, capsize=2.5,
               label=ARCH[e], color=COLOUR[e], edgecolor="white", linewidth=0.5,
               error_kw=dict(linewidth=0.9, ecolor="#333333"), zorder=2)

    for j, (_, k) in enumerate(groups):
        ax.text(j, 1.02, f"SNR {snr(runs, k):.2f}", ha="center", va="bottom",
                fontsize=7.4, style="italic", color="#444444")

    ax.set_xticks(x)
    ax.set_xticklabels([g[0] for g in groups])
    ax.set_ylabel("Score / prediction rate")
    ax.set_ylim(0, 1.10)
    ax.legend(loc="upper right", ncol=1, frameon=True)
    save(fig, "figure_4_internal_vs_shifted_domain")


# ------------------------------ Figure 5: predicted-class distribution

def figure_5_prediction_distribution(runs):
    fig, axes = plt.subplots(1, 2, figsize=(DOUBLE_COL, 66 * MM), sharey=True)
    for ax, (probe, title) in zip(axes, (("d3b", "(a) D3B \u2014 canine, 53 patients"),
                                         ("d3c", "(b) D3C \u2014 human, 610 patients"))):
        x = np.arange(len(CLASSES))
        width = 0.26
        for i, e in enumerate(ORDER):
            means, sds = [], []
            for c in CLASSES:
                v = vals(runs, e, f"{probe}_pred_{c}")
                means.append(st.mean(v) if v else 0)
                sds.append(st.stdev(v) if len(v) > 1 else 0)
            ax.bar(x + (i - 1) * width, means, width, yerr=sds, capsize=2,
                   label=ARCH[e], color=COLOUR[e], edgecolor="white",
                   linewidth=0.5, error_kw=dict(linewidth=0.8, ecolor="#333333"),
                   zorder=2)
        ax.set_xticks(x)
        ax.set_xticklabels(CLASS_LABELS, rotation=18, ha="right")
        ax.set_title(title, loc="left")
        ax.set_ylim(0, 0.95)
    axes[0].set_ylabel("Share of slices")
    axes[0].legend(loc="upper right", frameon=True)
    save(fig, "figure_5_prediction_distribution")


# ------------------- Figure 6: glioma rate against maximum confidence

def figure_6_confidence_inversion(runs):
    fig, ax = plt.subplots(figsize=(SINGLE_COL * 1.25, 78 * MM))

    for e in ORDER:
        rates = vals(runs, e, "d3c_rate")
        confs = vals(runs, e, "d3c_conf")
        ax.scatter(rates, confs, s=34, color=COLOUR[e], marker=MARKER[e],
                   alpha=0.7, edgecolor="white", linewidth=0.6,
                   label=f"{ARCH[e]} (n = {len(rates)})", zorder=3)
        ax.scatter([st.mean(rates)], [st.mean(confs)], s=115, color=COLOUR[e],
                   marker=MARKER[e], edgecolor="black", linewidth=1.0, zorder=4)

    all_r = [r["d3c_rate"] for r in runs if r.get("d3c_rate") is not None]
    all_c = [r["d3c_conf"] for r in runs if r.get("d3c_conf") is not None]
    r_val = pearson(all_r, all_c)
    fit = np.polyfit(all_r, all_c, 1)
    xs = np.linspace(min(all_r), max(all_r), 50)
    ax.plot(xs, np.polyval(fit, xs), ":", color="#555555", linewidth=1.1,
            label=f"Pooled fit (r = {r_val:+.3f})", zorder=2)

    ax.set_xlabel("D3C glioma prediction rate")
    ax.set_ylabel("Mean maximum confidence")
    ax.margins(x=0.06, y=0.12)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.20), ncol=2,
              frameon=False, fontsize=7.6, handletextpad=0.4, columnspacing=1.2)
    ax.text(0.98, 0.97, "Large markers:\narchitecture means",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=7, style="italic", color="#555555")
    save(fig, "figure_6_confidence_inversion")


# ------------------------------ Figure 7: correlation decomposition

def figure_7_simpson(runs):
    fig, axes = plt.subplots(1, 2, figsize=(DOUBLE_COL, 72 * MM))

    for ax, (probe, title) in zip(axes, (("d3c", "(a) D3C \u2014 human probe"),
                                         ("d3b", "(b) D3B \u2014 canine probe"))):
        arch_x, arch_y = {}, {}
        for e in ORDER:
            xs = vals(runs, e, "macro_f1")
            ys = vals(runs, e, f"{probe}_rate")
            arch_x[e], arch_y[e] = st.mean(xs), st.mean(ys)
            ax.scatter(xs, ys, s=32, color=COLOUR[e], marker=MARKER[e],
                       alpha=0.72, edgecolor="white", linewidth=0.6,
                       label=ARCH[e], zorder=3)
            # within-architecture fit
            if len(xs) > 2:
                f = np.polyfit(xs, ys, 1)
                gx = np.linspace(min(xs), max(xs), 20)
                ax.plot(gx, np.polyval(f, gx), "-", color=COLOUR[e],
                        linewidth=1.1, alpha=0.85, zorder=2)

        # between-architecture line through the three means
        mx = [arch_x[e] for e in ORDER]
        my = [arch_y[e] for e in ORDER]
        ax.scatter(mx, my, s=120, facecolor="none", edgecolor="black",
                   linewidth=1.2, zorder=5)
        f = np.polyfit(mx, my, 1)
        gx = np.linspace(min(mx), max(mx), 20)
        ax.plot(gx, np.polyval(f, gx), "--", color="black", linewidth=1.2,
                alpha=0.75, label="Between-architecture", zorder=4)

        # correlations
        all_x = [r["macro_f1"] for r in runs if r.get(f"{probe}_rate") is not None]
        all_y = [r[f"{probe}_rate"] for r in runs if r.get(f"{probe}_rate") is not None]
        r_pool = pearson(all_x, all_y)
        r_between = pearson(mx, my)
        cx = [r["macro_f1"] - arch_x[r["exp"]] for r in runs
              if r.get(f"{probe}_rate") is not None]
        cy = [r[f"{probe}_rate"] - arch_y[r["exp"]] for r in runs
              if r.get(f"{probe}_rate") is not None]
        r_within = pearson(cx, cy)

        ax.set_xlabel("Internal test macro-F1")
        ax.set_title(title, loc="left")
        ax.text(0.02, 0.97,
                f"pooled  $r$ = {r_pool:+.3f}\n"
                f"between $r$ = {r_between:+.3f}\n"
                f"within  $r$ = {r_within:+.3f}",
                transform=ax.transAxes, va="top", ha="left", fontsize=7.4,
                bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#999999", lw=0.6))

    axes[0].set_ylabel("Glioma prediction rate")
    axes[0].legend(loc="lower right", frameon=True, fontsize=7,
                   framealpha=0.93, handletextpad=0.4)
    save(fig, "figure_7_correlation_decomposition")


# -------------------------------------------------------------- provenance

def write_manifest(runs):
    """Record which runs produced the figures, so they can be traced."""
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "figure_source_manifest.csv", "w", newline="") as fh:
        keys = ["exp", "arch", "seed", "macro_f1", "accuracy", "temperature",
                "d3b_rate", "d3b_conf", "d3c_rate", "d3c_conf",
                "d3c_median_glioma"]
        w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(runs, key=lambda r: (r["exp"], r["seed"])))
    print(f"  {OUT / 'figure_source_manifest.csv'}")



def write_captions(runs):
    """Emit caption text defining error bars, n, and axis choices."""
    n_runs = len(runs)
    n_seeds = len({r["seed"] for r in runs})
    lines = [
        "# Figure captions",
        "",
        "Error bars and axis choices are stated explicitly. Reviewers routinely",
        "query figures where these are left undefined.",
        "",
        "**Figure 1.** System architecture of the reliability-first evaluation",
        "framework. Datasets are prepared and audited for contamination against the",
        "internal dataset D1; a candidate failing the audit is excluded from any",
        "external-validation role. Three architectures are trained on the fixed",
        "leakage-aware split at five seeds each, and evaluation proceeds across",
        "internal, calibration and shifted-domain layers.",
        "",
        "**Figure 2.** Internal test macro-F1 for each of the "
        f"{n_runs} runs, grouped by",
        "architecture. Points are individual runs with horizontal jitter applied for",
        "visibility; horizontal bars are architecture means and shaded bands span",
        f"\u00B11 standard deviation across the {n_seeds} seeds. **The vertical axis is",
        "truncated to 0.948-0.978** to resolve differences that are small in absolute",
        "terms; this truncation is the point of the figure, since the between-",
        "architecture spread is only 2.52 times the mean within-architecture standard",
        "deviation.",
        "",
        "**Figure 3.** Reliability diagrams on the internal test partition, pooled",
        f"across {n_seeds} seeds per architecture and weighted by bin count. Solid lines",
        "with filled markers are raw probabilities; dashed lines with open markers are",
        "temperature-scaled. The diagonal indicates perfect calibration. Bins",
        "containing fewer than five predictions are omitted.",
        "",
        "**Figure 4.** Internal test macro-F1 and shifted-domain glioma prediction",
        f"rate for the three architectures. Bars are means across {n_seeds} seeds and error",
        "bars are \u00B11 standard deviation. The signal-to-noise ratio above each group is",
        "the between-architecture spread divided by the mean within-architecture",
        "standard deviation (equation 10); values near or below 2 indicate that the",
        "evaluation does not resolve the architectures against seed variation.",
        "",
        "**Figure 5.** Distribution of predicted classes on the two shifted-domain",
        f"probes. Bars are means across {n_seeds} seeds and error bars are \u00B11 standard",
        "deviation. All architectures were evaluated on identical slices, so",
        "between-architecture differences reflect learned behaviour rather than slice",
        "selection.",
        "",
        "**Figure 6.** Human-probe glioma prediction rate against mean maximum",
        f"confidence for each of the {n_runs} runs. Small markers are individual runs;",
        "large outlined markers are architecture means. The dotted line is the",
        "least-squares fit pooled across all runs. Confidence increases as glioma",
        "recognition falls.",
        "",
        "**Figure 7.** Internal test macro-F1 against shifted-domain glioma prediction",
        f"rate for the {n_runs} runs. Coloured lines are within-architecture least-squares",
        "fits; the dashed black line is the fit through the three architecture means,",
        "shown as large open circles. On the human probe (a) the between-architecture",
        "association is positive while the within-architecture association is negative,",
        "a Simpson\u2019s paradox. On the canine probe (b) both are positive.",
        "",
    ]
    with open(OUT / "figure_captions.md", "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"  {OUT / 'figure_captions.md'}")


def main():
    print("Loading runs from per-seed artefacts...")
    runs = load_runs()
    print(f"  {len(runs)} runs "
          f"({len({r['exp'] for r in runs})} architectures "
          f"\u00D7 {len({r['seed'] for r in runs})} seeds)")

    print("Loading reliability bins...")
    rel = load_reliability()

    print("Generating figures:")
    figure_1_architecture()
    figure_2_internal(runs)
    figure_3_reliability(rel)
    figure_4_internal_vs_shift(runs)
    figure_5_prediction_distribution(runs)
    figure_6_confidence_inversion(runs)
    figure_7_simpson(runs)
    write_manifest(runs)

    write_captions(runs)
    check_fonts()

    print("\nDone. Figures are 300 dpi PNG and vector PDF (Type 42 fonts).")
    print("Captions written to figure_captions.md \u2014 these define the error")
    print("bars and axis truncation, which reviewers ask about if omitted.")


if __name__ == "__main__":
    main()
