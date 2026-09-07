#!/usr/bin/env python3
"""
Baseline glioma-propensity control for the D3C result.

The manuscript reports that the three architectures assign human glioblastoma
slices to the glioma class at very different rates (0.674 / 0.514 / 0.264), and
treats that separation as behaviour under shift. That inference assumes the
architectures do not simply differ in how readily they assign anything to the
glioma class.

This script tests that assumption. If ResNet18 also predicts glioma most often
on the internal test set, the D3C ordering may be recovering an internal
disposition rather than a property of behaviour under shift.

Three quantities are computed per run:

  1. Internal glioma prediction rate on the full D1 test partition.
     What share of all test images does the model assign to glioma?

  2. Internal off-target glioma rate on non-glioma D1 test images.
     Of the images that are NOT glioma, what share does the model call glioma?
     This is the cleanest measure of glioma-ward bias, because it excludes the
     glioma images the model is supposed to assign there.

  3. D3C glioma assignment rate, as reported in the manuscript.

Interpretation:

  - If the internal off-target rate ranks the architectures the same way the
    D3C rate does, the D3C separation is confounded with class propensity and
    the manuscript's inference needs qualifying.
  - If the internal off-target rates are close together while the D3C rates
    diverge, propensity does not explain the separation and the finding holds.

Run from the repo root:
    python scripts/check_glioma_propensity.py

Writes to reports/experiments/consolidated/:
    glioma_propensity_control.csv
    glioma_propensity_control.md
"""

import csv
import json
import statistics as st
import sys
from pathlib import Path

EXPERIMENTS = Path("experiments")
OUT = Path("reports/experiments/consolidated")

ARCH = {"E001": "ResNet18", "E002": "EfficientNet-B0", "E003": "ViT-B/16"}
ORDER = ["E001", "E002", "E003"]


def seed_dirs():
    if not EXPERIMENTS.is_dir():
        sys.exit("No experiments/ directory. Run this from the repo root.")
    for exp_dir in sorted(p for p in EXPERIMENTS.iterdir() if p.is_dir()):
        exp_id = exp_dir.name.split("_")[0]
        if exp_id not in ARCH:
            continue
        for sd in sorted(p for p in exp_dir.iterdir() if p.is_dir()):
            if sd.name.startswith("seed"):
                yield exp_id, int(sd.name.replace("seed", "")), sd


def read_csv(path):
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def collect():
    runs = []
    for exp_id, seed, sd in seed_dirs():
        test = read_csv(sd / "test_predictions.csv")
        d3c = read_csv(sd / "d3c_predictions.csv")
        d3b = read_csv(sd / "d3b_predictions.csv")
        if not test or not d3c:
            print(f"  skipping {exp_id}/seed{seed}: missing predictions")
            continue

        n_test = len(test)
        pred_glioma = sum(1 for r in test if r["pred_label"] == "glioma")

        non_glioma = [r for r in test if r["true_label"] != "glioma"]
        off_target = sum(1 for r in non_glioma if r["pred_label"] == "glioma")

        true_glioma = [r for r in test if r["true_label"] == "glioma"]
        glioma_recall = (sum(1 for r in true_glioma if r["pred_label"] == "glioma")
                         / len(true_glioma)) if true_glioma else None

        # mean predicted glioma probability over all internal test images:
        # a soft measure of glioma-ward disposition that does not depend on
        # which class happened to win the argmax
        probs = [float(r["prob_glioma"]) for r in test if r.get("prob_glioma")]

        runs.append({
            "experiment_id": exp_id,
            "architecture": ARCH[exp_id],
            "seed": seed,
            "n_test": n_test,
            "internal_glioma_rate": pred_glioma / n_test,
            "internal_off_target_glioma_rate": off_target / len(non_glioma),
            "internal_glioma_recall": glioma_recall,
            "internal_mean_glioma_prob": st.mean(probs) if probs else None,
            "d3c_glioma_rate": sum(1 for r in d3c if r["pred_label"] == "glioma") / len(d3c),
            "d3b_glioma_rate": (sum(1 for r in d3b if r["pred_label"] == "glioma") / len(d3b))
                               if d3b else None,
        })
    return runs


def summarise(runs, key):
    out = {}
    for e in ORDER:
        vals = [r[key] for r in runs if r["experiment_id"] == e and r.get(key) is not None]
        if len(vals) > 1:
            out[e] = (st.mean(vals), st.stdev(vals))
    return out


def ordering(summary):
    return " > ".join(ARCH[e] for e in sorted(summary, key=lambda e: -summary[e][0]))


def spread_snr(summary):
    means = [m for m, _ in summary.values()]
    sds = [s for _, s in summary.values()]
    spread = max(means) - min(means)
    mean_sd = st.mean(sds)
    return spread, mean_sd, (spread / mean_sd if mean_sd else float("inf"))


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    print("Reading predictions...")
    runs = collect()
    if not runs:
        sys.exit("No runs found.")
    print(f"  {len(runs)} runs")

    keys = [
        ("internal_glioma_rate", "Internal glioma prediction rate (all test images)"),
        ("internal_off_target_glioma_rate", "Internal off-target glioma rate (non-glioma images only)"),
        ("internal_mean_glioma_prob", "Internal mean predicted glioma probability"),
        ("internal_glioma_recall", "Internal glioma recall"),
        ("d3c_glioma_rate", "D3C glioma assignment rate"),
        ("d3b_glioma_rate", "D3B glioma assignment rate"),
    ]

    summaries = {k: summarise(runs, k) for k, _ in keys}

    with open(OUT / "glioma_propensity_control.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(runs[0]))
        w.writeheader()
        w.writerows(sorted(runs, key=lambda r: (r["experiment_id"], r["seed"])))
    print(f"  wrote {OUT / 'glioma_propensity_control.csv'}")

    # ---- verdict ----
    d3c_order = ordering(summaries["d3c_glioma_rate"])
    off_order = ordering(summaries["internal_off_target_glioma_rate"])
    internal_order = ordering(summaries["internal_glioma_rate"])
    same_as_off = d3c_order == off_order
    same_as_all = d3c_order == internal_order

    off_spread, off_sd, off_snr = spread_snr(summaries["internal_off_target_glioma_rate"])
    d3c_spread, d3c_sd, d3c_snr = spread_snr(summaries["d3c_glioma_rate"])

    L = []
    A = L.append
    A("# Baseline glioma-propensity control")
    A("")
    A("The D3C result reports that the three architectures assign human glioblastoma")
    A("slices to the glioma class at very different rates. That is interpreted as")
    A("behaviour under shift. This check tests the competing explanation: that the")
    A("architectures simply differ in how readily they assign anything to glioma.")
    A("")
    A("The decisive measure is the **off-target glioma rate** on the internal test")
    A("set: of the D1 test images that are not glioma, what share does each model")
    A("assign to glioma anyway? That isolates glioma-ward bias from glioma")
    A("competence.")
    A("")

    A("## Results, mean +/- SD across five seeds")
    A("")
    A("| Measure | " + " | ".join(ARCH[e] for e in ORDER) + " | Ordering |")
    A("|---|---|---|---|---|")
    for k, label in keys:
        s = summaries[k]
        if not s:
            continue
        cells = " | ".join(f"{s[e][0]:.4f} ± {s[e][1]:.4f}" if e in s else "?"
                           for e in ORDER)
        A(f"| {label} | {cells} | {ordering(s)} |")
    A("")

    A("## Separation")
    A("")
    A("| Measure | Between-arch spread | Mean seed SD | SNR |")
    A("|---|---|---|---|")
    A(f"| Internal off-target glioma rate | {off_spread:.4f} | {off_sd:.4f} | {off_snr:.2f} |")
    A(f"| D3C glioma assignment rate | {d3c_spread:.4f} | {d3c_sd:.4f} | {d3c_snr:.2f} |")
    A("")

    A("## Verdict")
    A("")
    if same_as_off:
        A("**The D3C ordering matches the internal off-target ordering.**")
        A("")
        A(f"- D3C: {d3c_order}")
        A(f"- Internal off-target: {off_order}")
        A("")
        A("Baseline glioma propensity is therefore a live confound for the D3C")
        A("result. The architectures that assign more D3C slices to glioma are the")
        A("same ones that assign more non-glioma internal images to glioma. The")
        A("manuscript cannot attribute the D3C separation to behaviour under shift")
        A("without controlling for this.")
        A("")
        ratio = d3c_spread / off_spread if off_spread else float("inf")
        A(f"The D3C spread ({d3c_spread:.4f}) is {ratio:.1f} times the internal")
        A(f"off-target spread ({off_spread:.4f}). If that ratio is large, propensity")
        A("explains only part of the separation and the finding survives in")
        A("qualified form; if it is close to 1, the D3C result may be largely a")
        A("restatement of internal class bias.")
    else:
        A("**The D3C ordering does not match the internal off-target ordering.**")
        A("")
        A(f"- D3C: {d3c_order}")
        A(f"- Internal off-target: {off_order}")
        A("")
        A("Baseline glioma propensity does not explain the D3C separation. The")
        A("architectures that assign more D3C slices to glioma are not the ones most")
        A("disposed to assign non-glioma internal images to glioma, so the separation")
        A("is a property of behaviour under shift rather than of a class prior.")
        A("")
        A("This strengthens the manuscript's central result and should be reported.")
    A("")
    A(f"Ordering by internal glioma rate over all test images: {internal_order}")
    A(f"(matches D3C ordering: {'yes' if same_as_all else 'no'})")
    A("")

    A("## Reporting")
    A("")
    A("Whichever way this resolves, it belongs in the manuscript. A reviewer who")
    A("thinks of the propensity explanation will ask for exactly this table, and it")
    A("costs two sentences in Section 3.4 plus one row in a supplementary table.")
    A("")

    with open(OUT / "glioma_propensity_control.md", "w") as fh:
        fh.write("\n".join(L) + "\n")
    print(f"  wrote {OUT / 'glioma_propensity_control.md'}")

    print()
    print(f"D3C ordering:              {d3c_order}")
    print(f"Internal off-target:       {off_order}")
    print(f"Internal all-images:       {internal_order}")
    print()
    print(f"Off-target spread {off_spread:.4f} (SNR {off_snr:.2f})")
    print(f"D3C spread        {d3c_spread:.4f} (SNR {d3c_snr:.2f})")
    print()
    if same_as_off:
        print("CONFOUNDED: propensity is a live explanation. See the report.")
    else:
        print("CLEAN: propensity does not explain the D3C separation.")


if __name__ == "__main__":
    main()
