#!/usr/bin/env python3
"""
Generate manuscript-ready tables and figures from the seed sweep.

Companion to consolidate_sweep_results.py. That script produces the headline
result set; this one produces the supporting tables and figures the manuscript
needs: per-class performance, confusion matrices, calibration before and after
temperature scaling, reliability diagrams, and probe prediction distributions ?
all aggregated across seeds with dispersion, never a single seed.

Run from the repo root:
    python scripts/generate_sweep_figures_tables.py

Outputs to reports/experiments/consolidated/:
    tables/*.csv and tables/*.md
    figures/*.png and figures/*.pdf
"""

import csv
import json
import os
import statistics as st
import sys
from datetime import datetime
from pathlib import Path

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    HAVE_MPL = True
except ImportError:
    HAVE_MPL = False
    print("matplotlib/numpy not found ? tables will be written, figures skipped.")

EXPERIMENTS = Path("experiments")
OUT = Path("reports/experiments/consolidated")
TABLES = OUT / "tables"
FIGURES = OUT / "figures"

ARCH = {"E001": "ResNet18", "E002": "EfficientNet-B0", "E003": "ViT-B/16"}
CLASSES = ["glioma", "meningioma", "notumor", "pituitary"]
CLASS_LABELS = ["Glioma", "Meningioma", "No tumour", "Pituitary"]
COLOURS = {"E001": "#3B6FB6", "E002": "#2E9E83", "E003": "#D2691E"}


# ----------------------------------------------------------------- loading

def seed_dirs():
    """Yield (exp_id, seed, path) for every run in the sweep."""
    if not EXPERIMENTS.is_dir():
        sys.exit("No experiments/ directory. Run this from the repo root.")
    for exp_dir in sorted(p for p in EXPERIMENTS.iterdir() if p.is_dir()):
        exp_id = exp_dir.name.split("_")[0]
        if exp_id not in ARCH:
            continue
        for sd in sorted(p for p in exp_dir.iterdir() if p.is_dir()):
            if sd.name.startswith("seed"):
                yield exp_id, int(sd.name.replace("seed", "")), sd


def load_json(path):
    if not Path(path).exists():
        return None
    with open(path) as fh:
        return json.load(fh)


def ms(values, dp=4):
    """mean ± sd, or a single value if only one."""
    vals = [v for v in values if v is not None]
    if not vals:
        return "?"
    if len(vals) == 1:
        return f"{vals[0]:.{dp}f}"
    return f"{st.mean(vals):.{dp}f} ± {st.stdev(vals):.{dp}f}"


def write_csv(path, rows):
    if not rows:
        return
    keys = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    print(f"  {path}")


def write_md(path, lines):
    with open(path, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"  {path}")


# ------------------------------------------------------- per-class metrics

def per_class_table():
    """Per-class precision, recall, F1 aggregated over seeds."""
    acc = {}
    for exp_id, seed, sd in seed_dirs():
        fr = load_json(sd / "final_results.json")
        if not fr:
            continue
        report = fr.get("classification_report", {})
        for cls in CLASSES:
            if cls not in report:
                continue
            key = (exp_id, cls)
            acc.setdefault(key, {"precision": [], "recall": [],
                                 "f1": [], "support": []})
            acc[key]["precision"].append(report[cls].get("precision"))
            acc[key]["recall"].append(report[cls].get("recall"))
            acc[key]["f1"].append(report[cls].get("f1-score"))
            acc[key]["support"].append(report[cls].get("support"))

    rows, md = [], []
    md.append("# Per-class internal performance (D1 test)")
    md.append("")
    md.append("Mean ± SD across seeds 42-46. Run set `2026-08-sweep-a`.")
    md.append("")
    md.append("| Architecture | Class | Precision | Recall | F1 | Support |")
    md.append("|---|---|---|---|---|---|")

    for exp_id in sorted(ARCH):
        for cls, label in zip(CLASSES, CLASS_LABELS):
            key = (exp_id, cls)
            if key not in acc:
                continue
            d = acc[key]
            rows.append({
                "experiment_id": exp_id,
                "architecture": ARCH[exp_id],
                "class": cls,
                "n_seeds": len(d["f1"]),
                "precision_mean": round(st.mean(d["precision"]), 4),
                "precision_sd": round(st.stdev(d["precision"]), 4)
                if len(d["precision"]) > 1 else 0,
                "recall_mean": round(st.mean(d["recall"]), 4),
                "recall_sd": round(st.stdev(d["recall"]), 4)
                if len(d["recall"]) > 1 else 0,
                "f1_mean": round(st.mean(d["f1"]), 4),
                "f1_sd": round(st.stdev(d["f1"]), 4)
                if len(d["f1"]) > 1 else 0,
                "support": int(d["support"][0]) if d["support"] else None,
            })
            md.append(f"| {ARCH[exp_id]} | {label} | {ms(d['precision'])} | "
                      f"{ms(d['recall'])} | {ms(d['f1'])} | "
                      f"{int(d['support'][0]) if d['support'] else '?'} |")

    write_csv(TABLES / "per_class_internal_performance.csv", rows)
    write_md(TABLES / "per_class_internal_performance.md", md)
    return rows


# ---------------------------------------------------- confusion matrices

def confusion_matrices():
    """Mean confusion matrix per architecture, counts and row-normalised."""
    acc = {}
    for exp_id, seed, sd in seed_dirs():
        path = sd / "test_confusion_matrix.csv"
        if not path.exists():
            continue
        with open(path) as fh:
            for row in csv.DictReader(fh):
                true_cls = (row.get("") or row.get("index") or "").replace("true_", "")
                if true_cls not in CLASSES:
                    continue
                for pred_cls in CLASSES:
                    col = f"pred_{pred_cls}"
                    if col not in row:
                        continue
                    acc.setdefault(exp_id, {}).setdefault(
                        (true_cls, pred_cls), []).append(float(row[col]))

    rows, md = [], []
    md.append("# Internal confusion matrices (D1 test)")
    md.append("")
    md.append("Mean counts across seeds 42-46, with row-normalised proportions "
              "in brackets. Run set `2026-08-sweep-a`.")
    md.append("")

    matrices = {}
    for exp_id in sorted(acc):
        md.append(f"## {ARCH[exp_id]}")
        md.append("")
        md.append("| True \\ Predicted | " + " | ".join(CLASS_LABELS) + " |")
        md.append("|---|" + "---|" * len(CLASSES))

        mat = []
        for true_cls, true_label in zip(CLASSES, CLASS_LABELS):
            counts = [st.mean(acc[exp_id].get((true_cls, p), [0]))
                      for p in CLASSES]
            total = sum(counts) or 1
            mat.append(counts)
            cells = []
            for pred_cls, c in zip(CLASSES, counts):
                sds = acc[exp_id].get((true_cls, pred_cls), [0])
                sd_v = st.stdev(sds) if len(sds) > 1 else 0
                cells.append(f"{c:.1f} ± {sd_v:.1f} ({c / total:.3f})")
                rows.append({
                    "experiment_id": exp_id,
                    "architecture": ARCH[exp_id],
                    "true_class": true_cls,
                    "predicted_class": pred_cls,
                    "mean_count": round(c, 2),
                    "sd_count": round(sd_v, 2),
                    "row_proportion": round(c / total, 4),
                })
            md.append(f"| {true_label} | " + " | ".join(cells) + " |")
        md.append("")
        matrices[exp_id] = mat

    write_csv(TABLES / "internal_confusion_matrices.csv", rows)
    write_md(TABLES / "internal_confusion_matrices.md", md)
    return matrices


# ------------------------------------------------------------ calibration

def calibration_table():
    """Calibration before and after temperature scaling, across seeds."""
    acc = {}
    for exp_id, seed, sd in seed_dirs():
        ts = load_json(sd / "temperature_scaling_metrics.json")
        if not ts:
            continue
        raw = ts.get("raw_test_metrics", {})
        scaled = ts.get("temperature_scaled_test_metrics", {})
        d = acc.setdefault(exp_id, {k: [] for k in [
            "temperature", "ece_raw", "ece_scaled", "nll_raw", "nll_scaled",
            "brier_raw", "brier_scaled", "gap_raw", "gap_scaled"]})
        d["temperature"].append(ts.get("learned_temperature"))
        d["ece_raw"].append(raw.get("ece_15_bins"))
        d["ece_scaled"].append(scaled.get("ece_15_bins"))
        d["nll_raw"].append(raw.get("negative_log_likelihood"))
        d["nll_scaled"].append(scaled.get("negative_log_likelihood"))
        d["brier_raw"].append(raw.get("brier_score"))
        d["brier_scaled"].append(scaled.get("brier_score"))
        d["gap_raw"].append(raw.get("confidence_accuracy_gap"))
        d["gap_scaled"].append(scaled.get("confidence_accuracy_gap"))

    rows, md = [], []
    md.append("# Internal calibration before and after temperature scaling")
    md.append("")
    md.append("Mean ± SD across seeds 42-46 on the D1 test split. Lower is "
              "better for all four metrics. Run set `2026-08-sweep-a`.")
    md.append("")
    md.append("**The learned temperature is a property of the checkpoint, not "
              "the architecture** ? it varies materially across seeds, so it is "
              "reported with dispersion rather than as a single value.")
    md.append("")
    md.append("| Architecture | T | ECE raw ? scaled | NLL raw ? scaled | "
              "Brier raw ? scaled | Conf?acc gap raw ? scaled |")
    md.append("|---|---|---|---|---|---|")

    for exp_id in sorted(acc):
        d = acc[exp_id]
        rows.append({
            "experiment_id": exp_id,
            "architecture": ARCH[exp_id],
            "n_seeds": len(d["temperature"]),
            **{f"{k}_{s}": round(f(d[k]), 4)
               for k in d for s, f in
               [("mean", st.mean),
                ("sd", lambda v: st.stdev(v) if len(v) > 1 else 0)]},
            "temperature_min": round(min(d["temperature"]), 4),
            "temperature_max": round(max(d["temperature"]), 4),
        })
        md.append(
            f"| {ARCH[exp_id]} | {ms(d['temperature'])} "
            f"[{min(d['temperature']):.4f}?{max(d['temperature']):.4f}] "
            f"| {ms(d['ece_raw'])} ? {ms(d['ece_scaled'])} "
            f"| {ms(d['nll_raw'])} ? {ms(d['nll_scaled'])} "
            f"| {ms(d['brier_raw'])} ? {ms(d['brier_scaled'])} "
            f"| {ms(d['gap_raw'])} ? {ms(d['gap_scaled'])} |")

    write_csv(TABLES / "internal_calibration.csv", rows)
    write_md(TABLES / "internal_calibration.md", md)
    return acc


# ------------------------------------------------- probe prediction shares

def probe_tables():
    """Prediction distribution and confidence on each probe, across seeds."""
    acc = {}
    for exp_id, seed, sd in seed_dirs():
        for probe in ("d3b", "d3c"):
            dm = load_json(sd / f"{probe}_domain_shift_metrics.json")
            if not dm:
                continue
            d = acc.setdefault((exp_id, probe), {
                "glioma_rate": [], "patient_majority": [],
                "mean_conf": [], "mean_entropy": [],
                "mean_glioma_prob": [], "median_glioma_prob": [],
                "n_slices": [], "n_patients": [],
                **{f"pred_{c}": [] for c in CLASSES}})
            d["glioma_rate"].append(dm.get("glioma_prediction_rate"))
            d["patient_majority"].append(dm.get("patient_majority_glioma_rate"))
            d["mean_conf"].append(dm.get("mean_max_confidence"))
            d["mean_entropy"].append(dm.get("mean_entropy"))
            d["mean_glioma_prob"].append(dm.get("mean_glioma_probability"))
            d["median_glioma_prob"].append(dm.get("median_glioma_probability"))
            d["n_slices"].append(dm.get("n_slices"))
            d["n_patients"].append(dm.get("n_patients"))
            for cls, share in (dm.get("prediction_proportions") or {}).items():
                if f"pred_{cls}" in d:
                    d[f"pred_{cls}"].append(share)

    # temperature-scaled behaviour
    scaled = {}
    for exp_id, seed, sd in seed_dirs():
        for probe in ("d3b", "d3c"):
            tm = load_json(sd / f"{probe}_temperature_scaled_metrics.json")
            if not tm:
                continue
            d = scaled.setdefault((exp_id, probe), {
                "rate_raw": [], "rate_scaled": [],
                "conf_raw": [], "conf_scaled": [],
                "entropy_raw": [], "entropy_scaled": []})
            for tag, key in (("raw", "raw"), ("scaled", "temperature_scaled")):
                blk = tm.get(key, {})
                d[f"rate_{tag}"].append(blk.get("glioma_prediction_rate"))
                d[f"conf_{tag}"].append(blk.get("mean_max_confidence"))
                d[f"entropy_{tag}"].append(blk.get("mean_entropy"))

    rows, md = [], []
    md.append("# Shifted-domain prediction behaviour")
    md.append("")
    md.append("Mean ± SD across seeds 42-46. Run set `2026-08-sweep-a`.")
    md.append("")
    md.append("Neither probe reproduces the four-class D1 label structure, so "
              "these are prediction and confidence behaviour under shift, not "
              "diagnostic accuracy.")
    md.append("")

    for probe, name in (("d3b", "D3B ? cross-species (canine)"),
                        ("d3c", "D3C ? same-species (human)")):
        present = [(e, p) for (e, p) in acc if p == probe]
        if not present:
            continue
        n_pat = acc[present[0]]["n_patients"][0]
        n_sli = acc[present[0]]["n_slices"][0]
        md.append(f"## {name}")
        md.append("")
        md.append(f"{n_pat} patients, {n_sli} slices.")
        md.append("")
        md.append("| Architecture | Slice glioma rate | Patient-majority | "
                  "Mean confidence | Mean entropy | Median glioma prob |")
        md.append("|---|---|---|---|---|---|")
        for exp_id in sorted(ARCH):
            key = (exp_id, probe)
            if key not in acc:
                continue
            d = acc[key]
            md.append(f"| {ARCH[exp_id]} | {ms(d['glioma_rate'])} | "
                      f"{ms(d['patient_majority'])} | {ms(d['mean_conf'])} | "
                      f"{ms(d['mean_entropy'])} | {ms(d['median_glioma_prob'])} |")
            rows.append({
                "experiment_id": exp_id, "architecture": ARCH[exp_id],
                "probe": probe.upper(), "n_seeds": len(d["glioma_rate"]),
                "n_patients": n_pat, "n_slices": n_sli,
                "glioma_rate_mean": round(st.mean(d["glioma_rate"]), 4),
                "glioma_rate_sd": round(st.stdev(d["glioma_rate"]), 4),
                "patient_majority_mean": round(st.mean(d["patient_majority"]), 4),
                "mean_confidence": round(st.mean(d["mean_conf"]), 4),
                "mean_entropy": round(st.mean(d["mean_entropy"]), 4),
                **{f"pred_{c}_mean": round(st.mean(d[f"pred_{c}"]), 4)
                   for c in CLASSES if d[f"pred_{c}"]},
            })
        md.append("")
        md.append("Predicted-class distribution across the four D1 classes:")
        md.append("")
        md.append("| Architecture | " + " | ".join(CLASS_LABELS) + " |")
        md.append("|---|" + "---|" * len(CLASSES))
        for exp_id in sorted(ARCH):
            key = (exp_id, probe)
            if key not in acc:
                continue
            d = acc[key]
            md.append(f"| {ARCH[exp_id]} | " +
                      " | ".join(ms(d[f"pred_{c}"], 3) for c in CLASSES) + " |")
        md.append("")

        if any(p == probe for (_, p) in scaled):
            md.append("Temperature scaling on this probe. Predictions are "
                      "unchanged by construction ? scaling is monotonic in the "
                      "logits ? so only confidence moves:")
            md.append("")
            md.append("| Architecture | Glioma rate raw ? scaled | "
                      "Confidence raw ? scaled | Entropy raw ? scaled |")
            md.append("|---|---|---|---|")
            for exp_id in sorted(ARCH):
                key = (exp_id, probe)
                if key not in scaled:
                    continue
                s = scaled[key]
                md.append(f"| {ARCH[exp_id]} | {ms(s['rate_raw'])} ? "
                          f"{ms(s['rate_scaled'])} | {ms(s['conf_raw'])} ? "
                          f"{ms(s['conf_scaled'])} | {ms(s['entropy_raw'])} ? "
                          f"{ms(s['entropy_scaled'])} |")
            md.append("")

    write_csv(TABLES / "probe_prediction_behaviour.csv", rows)
    write_md(TABLES / "probe_prediction_behaviour.md", md)
    return acc


# ---------------------------------------------------- reliability diagrams

def reliability_data():
    """Pool reliability bins across seeds, weighted by bin count."""
    acc = {}
    for exp_id, seed, sd in seed_dirs():
        for tag, fname in (("raw", "test_reliability_bins.csv"),
                           ("scaled", "test_temperature_scaled_reliability_bins.csv")):
            path = sd / fname
            if not path.exists():
                continue
            with open(path) as fh:
                for row in csv.DictReader(fh):
                    try:
                        count = float(row["count"])
                    except (KeyError, ValueError):
                        continue
                    if count == 0 or not row.get("accuracy"):
                        continue
                    b = int(row["bin"])
                    d = acc.setdefault((exp_id, tag), {}).setdefault(
                        b, {"lower": float(row["lower"]),
                            "upper": float(row["upper"]),
                            "count": 0.0, "acc_w": 0.0, "conf_w": 0.0})
                    d["count"] += count
                    d["acc_w"] += float(row["accuracy"]) * count
                    d["conf_w"] += float(row["confidence"]) * count

    rows = []
    for (exp_id, tag), bins in sorted(acc.items()):
        for b, d in sorted(bins.items()):
            rows.append({
                "experiment_id": exp_id, "architecture": ARCH[exp_id],
                "variant": tag, "bin": b,
                "lower": round(d["lower"], 4), "upper": round(d["upper"], 4),
                "total_count": int(d["count"]),
                "accuracy": round(d["acc_w"] / d["count"], 4),
                "confidence": round(d["conf_w"] / d["count"], 4),
                "gap": round((d["conf_w"] - d["acc_w"]) / d["count"], 4),
            })
    write_csv(TABLES / "reliability_bins_pooled.csv", rows)
    return acc


# ----------------------------------------------------------------- figures

def save(fig, name):
    for ext in ("png", "pdf"):
        path = FIGURES / f"{name}.{ext}"
        fig.savefig(path, dpi=200, bbox_inches="tight")
        print(f"  {path}")
    plt.close(fig)


def figure_internal_vs_shift(runs_by_arch):
    """Internal near-parity against divergent shifted-domain behaviour."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
    exps = sorted(ARCH)
    x = np.arange(3)
    width = 0.25

    ax = axes[0]
    groups = [("Internal\nmacro-F1", "test_macro_f1"),
              ("D3B glioma rate\n(canine)", "d3b_glioma_rate"),
              ("D3C glioma rate\n(human)", "d3c_glioma_rate")]
    for i, exp_id in enumerate(exps):
        means = [st.mean(runs_by_arch[exp_id][m]) for _, m in groups]
        sds = [st.stdev(runs_by_arch[exp_id][m]) for _, m in groups]
        ax.bar(x + (i - 1) * width, means, width, yerr=sds, capsize=4,
               label=ARCH[exp_id], color=COLOURS[exp_id])
    ax.set_xticks(x)
    ax.set_xticklabels([g[0] for g in groups])
    ax.set_ylabel("Score / prediction rate")
    ax.set_ylim(0, 1.05)
    ax.set_title("(a) Interchangeable internally, divergent under shift",
                 fontsize=11, loc="left")
    ax.legend(fontsize=9)
    ax.grid(axis="y", alpha=0.3)

    ax = axes[1]
    for exp_id in exps:
        vals = runs_by_arch[exp_id]
        for probe, xpos in (("d3b_glioma_rate", 0), ("d3c_glioma_rate", 1)):
            ax.scatter([xpos] * len(vals[probe]), vals[probe],
                       color=COLOURS[exp_id], alpha=0.45, s=28, zorder=3)
        ax.plot([0, 1],
                [st.mean(vals["d3b_glioma_rate"]),
                 st.mean(vals["d3c_glioma_rate"])],
                "o-", color=COLOURS[exp_id], linewidth=2.2,
                markersize=8, label=ARCH[exp_id], zorder=4)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["D3B\n(canine, n=53)", "D3C\n(human, n=610)"])
    ax.set_ylabel("Slice-level glioma prediction rate")
    ax.set_ylim(0, 0.9)
    ax.set_title("(b) Ordering is preserved; per-seed spread differs",
                 fontsize=11, loc="left")
    ax.legend(fontsize=9)
    ax.grid(axis="y", alpha=0.3)

    save(fig, "fig_internal_vs_shifted_domain")


def figure_seed_spread(runs_by_arch):
    """Seed variation against between-architecture separation."""
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))
    panels = [("Internal macro-F1", "test_macro_f1", (0.94, 0.98)),
              ("D3B glioma rate", "d3b_glioma_rate", (0, 0.7)),
              ("D3C glioma rate", "d3c_glioma_rate", (0, 0.9))]

    for ax, (title, metric, ylim) in zip(axes, panels):
        means = {e: st.mean(runs_by_arch[e][metric]) for e in ARCH}
        sds = {e: st.stdev(runs_by_arch[e][metric]) for e in ARCH}
        spread = max(means.values()) - min(means.values())
        snr = spread / st.mean(list(sds.values()))

        for i, exp_id in enumerate(sorted(ARCH)):
            vals = runs_by_arch[exp_id][metric]
            ax.scatter([i] * len(vals), vals, color=COLOURS[exp_id],
                       alpha=0.55, s=46, zorder=3)
            ax.hlines(means[exp_id], i - 0.28, i + 0.28,
                      color=COLOURS[exp_id], linewidth=2.6, zorder=4)
        ax.set_xticks(range(3))
        ax.set_xticklabels([ARCH[e] for e in sorted(ARCH)],
                           rotation=20, ha="right", fontsize=9)
        ax.set_ylim(*ylim)
        ax.set_title(f"{title}\nS/N = {snr:.2f}", fontsize=10)
        ax.grid(axis="y", alpha=0.3)

    axes[0].set_ylabel("Value (one point per seed)")
    fig.suptitle("Between-architecture separation against seed variation",
                 fontsize=12, y=1.02)
    save(fig, "fig_seed_spread")


def figure_reliability(rel):
    """Reliability diagrams, raw and temperature-scaled."""
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.4))
    for ax, exp_id in zip(axes, sorted(ARCH)):
        ax.plot([0, 1], [0, 1], "k--", linewidth=1, alpha=0.5,
                label="Perfect calibration")
        for tag, style, label in (("raw", "o-", "Raw"),
                                  ("scaled", "s--", "Temperature-scaled")):
            bins = rel.get((exp_id, tag))
            if not bins:
                continue
            conf, acc = [], []
            for b, d in sorted(bins.items()):
                if d["count"] < 5:
                    continue
                conf.append(d["conf_w"] / d["count"])
                acc.append(d["acc_w"] / d["count"])
            ax.plot(conf, acc, style, markersize=5, linewidth=1.6, label=label)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xlabel("Confidence")
        ax.set_title(ARCH[exp_id], fontsize=11)
        ax.grid(alpha=0.3)
        ax.legend(fontsize=8, loc="upper left")
    axes[0].set_ylabel("Accuracy")
    fig.suptitle("Reliability diagrams, D1 test, pooled across seeds 42-46",
                 fontsize=12, y=1.02)
    save(fig, "fig_reliability_diagrams")


def figure_probe_distribution(probe_acc):
    """Where shifted-domain predictions land across the four D1 classes."""
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.4))
    for ax, (probe, name) in zip(axes, (("d3b", "D3B ? canine, n=53"),
                                        ("d3c", "D3C ? human, n=610"))):
        x = np.arange(len(CLASSES))
        width = 0.25
        for i, exp_id in enumerate(sorted(ARCH)):
            key = (exp_id, probe)
            if key not in probe_acc:
                continue
            d = probe_acc[key]
            means = [st.mean(d[f"pred_{c}"]) if d[f"pred_{c}"] else 0
                     for c in CLASSES]
            sds = [st.stdev(d[f"pred_{c}"]) if len(d[f"pred_{c}"]) > 1 else 0
                   for c in CLASSES]
            ax.bar(x + (i - 1) * width, means, width, yerr=sds, capsize=3,
                   label=ARCH[exp_id], color=COLOURS[exp_id])
        ax.set_xticks(x)
        ax.set_xticklabels(CLASS_LABELS, fontsize=9)
        ax.set_ylabel("Share of slices")
        ax.set_ylim(0, 1.0)
        ax.set_title(name, fontsize=11)
        ax.legend(fontsize=9)
        ax.grid(axis="y", alpha=0.3)
    fig.suptitle("Predicted-class distribution on glioma-only probes "
                 "(mean ± SD across seeds)", fontsize=12, y=1.02)
    save(fig, "fig_probe_prediction_distribution")


def figure_confusion(matrices):
    """Row-normalised mean confusion matrices."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))
    for ax, exp_id in zip(axes, sorted(ARCH)):
        mat = np.array(matrices[exp_id], dtype=float)
        norm = mat / mat.sum(axis=1, keepdims=True)
        im = ax.imshow(norm, cmap="Blues", vmin=0, vmax=1)
        for i in range(len(CLASSES)):
            for j in range(len(CLASSES)):
                ax.text(j, i, f"{mat[i, j]:.0f}\n({norm[i, j]:.1%})",
                        ha="center", va="center", fontsize=8,
                        color="white" if norm[i, j] > 0.5 else "black")
        ax.set_xticks(range(len(CLASSES)))
        ax.set_yticks(range(len(CLASSES)))
        ax.set_xticklabels(CLASS_LABELS, rotation=35, ha="right", fontsize=8)
        ax.set_yticklabels(CLASS_LABELS, fontsize=8)
        ax.set_xlabel("Predicted")
        ax.set_title(ARCH[exp_id], fontsize=11)
    axes[0].set_ylabel("True")
    fig.colorbar(im, ax=axes, fraction=0.015, label="Row proportion")
    fig.suptitle("Internal confusion matrices, mean counts across seeds 42-46",
                 fontsize=12, y=1.03)
    save(fig, "fig_confusion_matrices")


# -------------------------------------------------------------------- main

def main():
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    print("Tables:")
    per_class_table()
    matrices = confusion_matrices()
    calibration_table()
    probe_acc = probe_tables()
    rel = reliability_data()

    runs_by_arch = {}
    for exp_id, seed, sd in seed_dirs():
        fr = load_json(sd / "final_results.json")
        d = runs_by_arch.setdefault(exp_id, {
            "test_macro_f1": [], "d3b_glioma_rate": [], "d3c_glioma_rate": []})
        if fr:
            d["test_macro_f1"].append(fr.get("test_macro_f1"))
        for probe in ("d3b", "d3c"):
            dm = load_json(sd / f"{probe}_domain_shift_metrics.json")
            if dm:
                d[f"{probe}_glioma_rate"].append(dm.get("glioma_prediction_rate"))

    if HAVE_MPL:
        print("Figures:")
        figure_internal_vs_shift(runs_by_arch)
        figure_seed_spread(runs_by_arch)
        figure_reliability(rel)
        figure_probe_distribution(probe_acc)
        figure_confusion(matrices)

    index = [
        "# Consolidated tables and figures",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "All values are aggregated across seeds 42-46 of run set "
        "`2026-08-sweep-a`. Nothing here reports a single seed.",
        "",
        "Supersedes everything in `reports/experiments/tables/` and "
        "`reports/experiments/figures/`, which report either a single seed "
        "or the Run A / Run B checkpoints.",
        "",
        "## Tables",
        "",
        "| File | Contents |",
        "|---|---|",
        "| `per_class_internal_performance` | Precision, recall, F1 per class "
        "per architecture |",
        "| `internal_confusion_matrices` | Mean confusion matrices with "
        "row proportions |",
        "| `internal_calibration` | ECE, NLL, Brier, confidence gap before and "
        "after temperature scaling |",
        "| `probe_prediction_behaviour` | D3B and D3C prediction shares, "
        "confidence, entropy, and temperature-scaled behaviour |",
        "| `reliability_bins_pooled` | Count-weighted reliability bins for "
        "the diagrams |",
        "",
        "## Figures",
        "",
        "| File | Contents |",
        "|---|---|",
        "| `fig_internal_vs_shifted_domain` | Internal near-parity beside "
        "shifted-domain divergence |",
        "| `fig_seed_spread` | Per-seed points with signal-to-noise per "
        "evaluation |",
        "| `fig_reliability_diagrams` | Calibration curves, raw and scaled |",
        "| `fig_probe_prediction_distribution` | Where probe predictions land "
        "across the four D1 classes |",
        "| `fig_confusion_matrices` | Internal confusion matrices |",
        "",
    ]
    write_md(OUT / "TABLES_AND_FIGURES_INDEX.md", index)
    print("\nDone.")


if __name__ == "__main__":
    main()
