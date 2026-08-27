#!/usr/bin/env python3
"""
D3C imaging-plane sensitivity analysis.

Eleven of the 610 D3C patients were flagged as oblique beyond 10 degrees
(reports/datasets/D3C_cohort_exclusion_report.md). Imaging plane is a plausible
alternative explanation for shifted-domain prediction behaviour, so this recomputes every
D3C behavioural metric on the sensitivity cohort with those patients dropped, and reports
the difference.

No retraining and no re-inference: this filters the saved per-slice predictions.

Run from the repo root:
    python scripts/d3c_plane_sensitivity.py

Outputs to reports/experiments/consolidated/:
    tables/d3c_plane_sensitivity.csv
    tables/d3c_plane_sensitivity.md
"""

import csv
import json
import statistics as st
import sys
from datetime import datetime
from pathlib import Path

EXPERIMENTS = Path("experiments")
MANIFEST = Path("data/processed/D3C_analysis_manifest.csv")
OUT = Path("reports/experiments/consolidated/tables")

ARCH = {"E001": "ResNet18", "E002": "EfficientNet-B0", "E003": "ViT-B/16"}
CLASSES = ["glioma", "meningioma", "notumor", "pituitary"]

# Fallback if the manifest carries no oblique flag column. Sourced from
# reports/datasets/D3C_cohort_exclusion_report.md.
FALLBACK_OBLIQUE = {
    "UPENN-GBM-00536", "UPENN-GBM-00570", "UPENN-GBM-00544", "UPENN-GBM-00532",
    "UPENN-GBM-00515", "UPENN-GBM-00452", "UPENN-GBM-00283", "UPENN-GBM-00506",
    "UPENN-GBM-00010", "UPENN-GBM-00331", "UPENN-GBM-00484",
}


def truthy(value):
    return str(value).strip().lower() in {"true", "1", "yes", "y", "t"}


def load_oblique_patients():
    """Patient IDs flagged oblique, from the manifest where possible."""
    if not MANIFEST.exists():
        print(f"  {MANIFEST} not found ? using the documented 11-patient list")
        return set(FALLBACK_OBLIQUE), "fallback list"

    with open(MANIFEST) as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        return set(FALLBACK_OBLIQUE), "fallback list"

    flag_col = next(
        (c for c in rows[0]
         if "oblique" in c.lower() and ("gt" in c.lower() or "flag" in c.lower())),
        None,
    )
    if flag_col is None:
        flag_col = next((c for c in rows[0] if "oblique" in c.lower()), None)

    id_col = next((c for c in rows[0] if c.lower() in
                   {"patient_id", "patientid", "patient"}), None)

    if flag_col is None or id_col is None:
        print("  no oblique flag column in the manifest ? using the documented list")
        return set(FALLBACK_OBLIQUE), "fallback list"

    oblique = set()
    for r in rows:
        value = r[flag_col]
        # Column may hold a boolean flag or a raw obliquity angle.
        if truthy(value):
            oblique.add(r[id_col])
        else:
            try:
                if float(value) > 10.0:
                    oblique.add(r[id_col])
            except (TypeError, ValueError):
                pass

    if not oblique:
        print("  manifest flagged no patients ? using the documented list")
        return set(FALLBACK_OBLIQUE), "fallback list"

    return oblique, f"manifest column `{flag_col}`"


def summarise(rows):
    """Behavioural metrics over a set of per-slice prediction rows."""
    if not rows:
        return None

    n = len(rows)
    glioma = sum(1 for r in rows if r["pred_label"] == "glioma")

    by_patient = {}
    for r in rows:
        by_patient.setdefault(r["patient_id"], []).append(r["pred_label"])
    majority_glioma = sum(
        1 for preds in by_patient.values()
        if max(set(preds), key=preds.count) == "glioma"
    )

    conf = [float(r["max_confidence"]) for r in rows]
    ent = [float(r["entropy"]) for r in rows]
    gp = [float(r["glioma_probability"]) for r in rows]

    out = {
        "n_slices": n,
        "n_patients": len(by_patient),
        "glioma_rate": glioma / n,
        "patient_majority_rate": majority_glioma / len(by_patient),
        "mean_confidence": st.mean(conf),
        "mean_entropy": st.mean(ent),
        "mean_glioma_prob": st.mean(gp),
        "median_glioma_prob": st.median(gp),
    }
    for cls in CLASSES:
        out[f"pred_{cls}"] = sum(1 for r in rows if r["pred_label"] == cls) / n
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    print("Loading oblique flags...")
    oblique, source = load_oblique_patients()
    print(f"  {len(oblique)} patients flagged oblique (source: {source})")

    print("Reading predictions...")
    results = {}
    for exp_dir in sorted(p for p in EXPERIMENTS.iterdir() if p.is_dir()):
        exp_id = exp_dir.name.split("_")[0]
        if exp_id not in ARCH:
            continue
        for sd in sorted(p for p in exp_dir.iterdir() if p.is_dir()):
            if not sd.name.startswith("seed"):
                continue
            path = sd / "d3c_predictions.csv"
            if not path.exists():
                continue
            with open(path) as fh:
                rows = list(csv.DictReader(fh))
            kept = [r for r in rows if r["patient_id"] not in oblique]
            results[(exp_id, int(sd.name.replace("seed", "")))] = {
                "full": summarise(rows),
                "sens": summarise(kept),
            }

    if not results:
        sys.exit("No d3c_predictions.csv found under experiments/.")
    print(f"  {len(results)} runs")

    any_run = next(iter(results.values()))
    n_full, n_sens = any_run["full"]["n_slices"], any_run["sens"]["n_slices"]
    p_full, p_sens = any_run["full"]["n_patients"], any_run["sens"]["n_patients"]

    rows_csv = []
    for (exp_id, seed), d in sorted(results.items()):
        row = {"experiment_id": exp_id, "architecture": ARCH[exp_id], "seed": seed}
        for tag, key in (("full", "full"), ("sensitivity", "sens")):
            for metric, value in d[key].items():
                row[f"{tag}_{metric}"] = (
                    round(value, 4) if isinstance(value, float) else value
                )
        row["delta_glioma_rate"] = round(
            d["sens"]["glioma_rate"] - d["full"]["glioma_rate"], 4)
        rows_csv.append(row)

    with open(OUT / "d3c_plane_sensitivity.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows_csv[0]))
        w.writeheader()
        w.writerows(rows_csv)
    print(f"  wrote {OUT / 'd3c_plane_sensitivity.csv'}")

    # per-architecture aggregation
    agg = {}
    for exp_id in ARCH:
        runs = [d for (e, _), d in results.items() if e == exp_id]
        if not runs:
            continue
        agg[exp_id] = {}
        for tag in ("full", "sens"):
            for metric in ("glioma_rate", "patient_majority_rate",
                           "mean_confidence", "mean_entropy"):
                vals = [r[tag][metric] for r in runs]
                agg[exp_id][f"{tag}_{metric}_mean"] = st.mean(vals)
                agg[exp_id][f"{tag}_{metric}_sd"] = st.stdev(vals)

    L = []
    A = L.append
    A("# D3C imaging-plane sensitivity analysis")
    A("")
    A(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    A("")
    A(f"Eleven of the {p_full} D3C patients carry series acquired more than 10 degrees "
      "from axial. Imaging plane is a plausible alternative explanation for the "
      "shifted-domain prediction behaviour reported in Section 4.6, so every D3C "
      "behavioural metric is recomputed with those patients removed.")
    A("")
    A(f"Full cohort: {p_full} patients / {n_full} slices. "
      f"Sensitivity cohort: {p_sens} patients / {n_sens} slices "
      f"({p_full - p_sens} patients, {n_full - n_sens} slices removed).")
    A("")
    A(f"Oblique flags sourced from: {source}. This filters saved per-slice "
      "predictions; no model was retrained or re-run.")
    A("")

    A("## Glioma prediction rate, full versus sensitivity cohort")
    A("")
    A("| Architecture | Full cohort | Oblique dropped | Difference |")
    A("|---|---|---|---|")
    max_shift = 0.0
    for exp_id in sorted(agg):
        a = agg[exp_id]
        d = a["sens_glioma_rate_mean"] - a["full_glioma_rate_mean"]
        max_shift = max(max_shift, abs(d))
        A(f"| {ARCH[exp_id]} | "
          f"{a['full_glioma_rate_mean']:.4f} ± {a['full_glioma_rate_sd']:.4f} | "
          f"{a['sens_glioma_rate_mean']:.4f} ± {a['sens_glioma_rate_sd']:.4f} | "
          f"{d:+.4f} |")
    A("")

    A("## Patient-majority glioma rate")
    A("")
    A("| Architecture | Full cohort | Oblique dropped | Difference |")
    A("|---|---|---|---|")
    for exp_id in sorted(agg):
        a = agg[exp_id]
        d = a["sens_patient_majority_rate_mean"] - a["full_patient_majority_rate_mean"]
        A(f"| {ARCH[exp_id]} | "
          f"{a['full_patient_majority_rate_mean']:.4f} ± "
          f"{a['full_patient_majority_rate_sd']:.4f} | "
          f"{a['sens_patient_majority_rate_mean']:.4f} ± "
          f"{a['sens_patient_majority_rate_sd']:.4f} | {d:+.4f} |")
    A("")

    A("## Confidence and entropy")
    A("")
    A("| Architecture | Confidence full ? dropped | Entropy full ? dropped |")
    A("|---|---|---|")
    for exp_id in sorted(agg):
        a = agg[exp_id]
        A(f"| {ARCH[exp_id]} | "
          f"{a['full_mean_confidence_mean']:.4f} ? "
          f"{a['sens_mean_confidence_mean']:.4f} | "
          f"{a['full_mean_entropy_mean']:.4f} ? "
          f"{a['sens_mean_entropy_mean']:.4f} |")
    A("")

    # ordering check
    full_order = sorted(agg, key=lambda e: -agg[e]["full_glioma_rate_mean"])
    sens_order = sorted(agg, key=lambda e: -agg[e]["sens_glioma_rate_mean"])
    A("## Architecture ordering")
    A("")
    A(f"- Full cohort: {' > '.join(ARCH[e] for e in full_order)}")
    A(f"- Oblique dropped: {' > '.join(ARCH[e] for e in sens_order)}")
    A(f"- Ordering preserved: **{'yes' if full_order == sens_order else 'NO'}**")
    A("")

    A("## Interpretation")
    A("")
    if full_order == sens_order and max_shift < 0.02:
        A(f"Removing the {p_full - p_sens} oblique patients changes the mean glioma "
          f"prediction rate by at most {max_shift:.4f} and leaves the architecture "
          "ordering unchanged. The between-architecture separation reported in Section "
          "4.6 is therefore not an artefact of imaging plane, and the full cohort is "
          "retained for the primary analysis.")
    elif full_order == sens_order:
        A(f"The architecture ordering is unchanged, but the mean glioma prediction rate "
          f"moves by up to {max_shift:.4f}. Report both cohorts and state the difference.")
    else:
        A("**The architecture ordering changes when oblique patients are removed.** "
          "Imaging plane cannot be dismissed as an explanation and both cohorts must be "
          "reported prominently.")
    A("")
    A("Because the sensitivity cohort is a strict subset of the full cohort and the "
      "eleven removed patients are a small fraction of the total, this analysis bounds "
      "the plane effect rather than eliminating it. Obliquity below the 10-degree "
      "threshold is not controlled.")
    A("")

    with open(OUT / "d3c_plane_sensitivity.md", "w") as fh:
        fh.write("\n".join(L) + "\n")
    print(f"  wrote {OUT / 'd3c_plane_sensitivity.md'}")

    print()
    print(f"Ordering preserved: {full_order == sens_order}")
    print(f"Largest shift in mean glioma rate: {max_shift:.4f}")


if __name__ == "__main__":
    main()
