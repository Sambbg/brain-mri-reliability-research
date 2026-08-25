#!/usr/bin/env python3
"""
Build one authoritative results set from the seed sweep.

Reads every experiments/<EXP>/seed<N>/ directory, verifies they belong to a single
run_id and split, and writes per-run and per-architecture summaries plus the
ranking-stability and correlation analyses.

Run from the repo root:
    python scripts/consolidate_sweep_results.py

Outputs to reports/experiments/consolidated/:
    sweep_runs_full.csv          one row per run (15 rows)
    architecture_summary.csv     one row per architecture, mean +/- sd
    ranking_stability.csv        distinct orderings per evaluation
    correlation_decomposition.csv  pooled / between / within
    CONSOLIDATED_RESULTS.md      human-readable report
"""

import csv
import json
import os
import statistics as st
import sys
from datetime import datetime
from itertools import combinations
from pathlib import Path

EXPERIMENTS = Path("experiments")
OUTDIR = Path("reports/experiments/consolidated")

ARCH_NAMES = {
    "E001": "ResNet18",
    "E002": "EfficientNet-B0",
    "E003": "ViT-B/16",
}


def load_runs():
    """Collect every seed directory into a flat list of run records."""
    runs = []
    if not EXPERIMENTS.is_dir():
        sys.exit(f"No {EXPERIMENTS}/ directory. Run this from the repo root.")

    for exp_dir in sorted(p for p in EXPERIMENTS.iterdir() if p.is_dir()):
        exp_id = exp_dir.name.split("_")[0]
        if exp_id not in ARCH_NAMES:
            continue

        for seed_dir in sorted(p for p in exp_dir.iterdir() if p.is_dir()):
            if not seed_dir.name.startswith("seed"):
                continue

            final = seed_dir / "final_results.json"
            if not final.exists():
                print(f"  skipping {seed_dir}: no final_results.json")
                continue

            with open(final) as fh:
                fr = json.load(fh)
            prov = fr.get("provenance", {})

            run = {
                "experiment_id": exp_id,
                "architecture": ARCH_NAMES[exp_id],
                "seed": int(seed_dir.name.replace("seed", "")),
                "run_id": prov.get("run_id", ""),
                "git_commit": prov.get("git_commit", "")[:12],
                "checkpoint_sha256": prov.get("checkpoint_sha256", "")[:12],
                "split_csv_sha256": prov.get("split_csv_sha256", ""),
                "best_epoch": fr.get("best_epoch"),
                "best_val_macro_f1": fr.get("best_val_macro_f1"),
                "test_accuracy": fr.get("test_accuracy"),
                "test_balanced_accuracy": fr.get("test_balanced_accuracy"),
                "test_macro_f1": fr.get("test_macro_f1"),
            }

            # per-class F1 from the classification report
            report = fr.get("classification_report", {})
            for cls in ("glioma", "meningioma", "notumor", "pituitary"):
                if cls in report:
                    run[f"f1_{cls}"] = report[cls].get("f1-score")
                    run[f"recall_{cls}"] = report[cls].get("recall")

            # calibration
            temp = seed_dir / "temperature_scaling_metrics.json"
            if temp.exists():
                with open(temp) as fh:
                    ts = json.load(fh)
                run["temperature"] = ts.get("learned_temperature")

            calib = seed_dir / "calibration_metrics.json"
            if calib.exists():
                with open(calib) as fh:
                    cm = json.load(fh)
                run["ece_raw"] = _dig(cm, "ece")
                run["nll_raw"] = _dig(cm, "nll")
                run["brier_raw"] = _dig(cm, "brier")

            # both shifted-domain probes
            for probe in ("d3b", "d3c"):
                path = seed_dir / f"{probe}_domain_shift_metrics.json"
                if not path.exists():
                    continue
                with open(path) as fh:
                    dm = json.load(fh)
                run[f"{probe}_glioma_rate"] = dm.get("glioma_prediction_rate")
                run[f"{probe}_patient_majority_rate"] = dm.get(
                    "patient_majority_glioma_rate")
                run[f"{probe}_mean_confidence"] = dm.get("mean_max_confidence")
                run[f"{probe}_mean_entropy"] = dm.get("mean_entropy")
                run[f"{probe}_mean_glioma_prob"] = dm.get("mean_glioma_probability")
                run[f"{probe}_median_glioma_prob"] = dm.get(
                    "median_glioma_probability")
                run[f"{probe}_n_slices"] = dm.get("n_slices")
                run[f"{probe}_n_patients"] = dm.get("n_patients")
                for cls, share in (dm.get("prediction_proportions") or {}).items():
                    run[f"{probe}_pred_{cls}"] = share

            runs.append(run)

    return runs


def _dig(obj, key):
    """Find the first value for `key` at any nesting depth."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key and not isinstance(v, (dict, list)):
                return v
            if isinstance(v, dict):
                found = _dig(v, key)
                if found is not None:
                    return found
    return None


def check_consistency(runs):
    """Refuse to summarise runs that are not comparable."""
    problems = []

    run_ids = {r["run_id"] for r in runs if r["run_id"]}
    if len(run_ids) > 1:
        problems.append(f"Multiple run_ids present: {sorted(run_ids)}")

    splits = {r["split_csv_sha256"] for r in runs if r["split_csv_sha256"]}
    if len(splits) > 1:
        problems.append(f"Multiple split hashes present: {len(splits)} distinct")

    by_arch = {}
    for r in runs:
        by_arch.setdefault(r["experiment_id"], []).append(r["seed"])
    seed_sets = {tuple(sorted(v)) for v in by_arch.values()}
    if len(seed_sets) > 1:
        problems.append(f"Architectures have different seed sets: {by_arch}")

    for probe in ("d3b", "d3c"):
        cohorts = {r.get(f"{probe}_n_patients") for r in runs
                   if r.get(f"{probe}_n_patients")}
        if len(cohorts) > 1:
            problems.append(f"{probe.upper()} evaluated on different cohorts: {cohorts}")
        missing = [f"{r['experiment_id']}/seed{r['seed']}" for r in runs
                   if r.get(f"{probe}_glioma_rate") is None]
        if missing:
            problems.append(f"{probe.upper()} missing for: {missing}")

    return problems


def summarise(runs, metrics):
    """Mean, sd and range per architecture for each metric."""
    out = []
    for exp_id in sorted(ARCH_NAMES):
        sub = [r for r in runs if r["experiment_id"] == exp_id]
        if not sub:
            continue
        row = {"experiment_id": exp_id, "architecture": ARCH_NAMES[exp_id],
               "n_seeds": len(sub)}
        for m in metrics:
            vals = [r[m] for r in sub if r.get(m) is not None]
            if len(vals) < 2:
                continue
            row[f"{m}_mean"] = round(st.mean(vals), 4)
            row[f"{m}_sd"] = round(st.stdev(vals), 4)
            row[f"{m}_min"] = round(min(vals), 4)
            row[f"{m}_max"] = round(max(vals), 4)
        out.append(row)
    return out


def ranking_stability(runs, metric):
    """How often does the architecture ordering change across seeds?"""
    seeds = sorted({r["seed"] for r in runs})
    orderings = []
    for seed in seeds:
        at_seed = [r for r in runs if r["seed"] == seed and r.get(metric) is not None]
        if len(at_seed) < 2:
            continue
        ordered = sorted(at_seed, key=lambda r: -r[metric])
        orderings.append(tuple(r["experiment_id"] for r in ordered))

    counts = {}
    for o in orderings:
        counts[o] = counts.get(o, 0) + 1

    winners = {}
    for o in orderings:
        winners[o[0]] = winners.get(o[0], 0) + 1

    return {
        "metric": metric,
        "n_seeds": len(orderings),
        "distinct_orderings": len(counts),
        "orderings": {" > ".join(o): n for o, n in
                      sorted(counts.items(), key=lambda kv: -kv[1])},
        "top_ranked_counts": winners,
    }


def signal_to_noise(runs, metric):
    """Between-architecture spread against mean within-architecture seed SD."""
    means, sds, ranges = {}, {}, {}
    for exp_id in ARCH_NAMES:
        vals = [r[metric] for r in runs
                if r["experiment_id"] == exp_id and r.get(metric) is not None]
        if len(vals) < 2:
            continue
        means[exp_id] = st.mean(vals)
        sds[exp_id] = st.stdev(vals)
        ranges[exp_id] = (min(vals), max(vals))

    if len(means) < 2:
        return None

    spread = max(means.values()) - min(means.values())
    mean_sd = st.mean(sds.values()) if hasattr(sds.values(), "__len__") \
        else st.mean(list(sds.values()))
    mean_sd = st.mean(list(sds.values()))

    overlaps = []
    for a, b in combinations(sorted(means), 2):
        ra, rb = ranges[a], ranges[b]
        overlaps.append({
            "pair": f"{a} vs {b}",
            "overlap": not (ra[1] < rb[0] or rb[1] < ra[0]),
            "range_a": f"[{ra[0]:.4f}, {ra[1]:.4f}]",
            "range_b": f"[{rb[0]:.4f}, {rb[1]:.4f}]",
        })

    return {
        "metric": metric,
        "between_architecture_spread": round(spread, 4),
        "mean_within_architecture_sd": round(mean_sd, 4),
        "signal_to_noise": round(spread / mean_sd, 2) if mean_sd else None,
        "pairwise": overlaps,
    }


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = st.mean(xs), st.mean(ys)
    num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    den = (sum((a - mx) ** 2 for a in xs) * sum((b - my) ** 2 for b in ys)) ** 0.5
    return num / den if den else None


def correlation_decomposition(runs, x_metric, y_metric):
    """Pooled vs between-architecture vs within-architecture correlation."""
    valid = [r for r in runs
             if r.get(x_metric) is not None and r.get(y_metric) is not None]
    if len(valid) < 3:
        return None

    xs = [r[x_metric] for r in valid]
    ys = [r[y_metric] for r in valid]

    arch_x, arch_y = {}, {}
    for exp_id in ARCH_NAMES:
        sub = [r for r in valid if r["experiment_id"] == exp_id]
        if sub:
            arch_x[exp_id] = st.mean([r[x_metric] for r in sub])
            arch_y[exp_id] = st.mean([r[y_metric] for r in sub])

    cx = [r[x_metric] - arch_x[r["experiment_id"]] for r in valid]
    cy = [r[y_metric] - arch_y[r["experiment_id"]] for r in valid]

    return {
        "x": x_metric,
        "y": y_metric,
        "n_runs": len(valid),
        "r_pooled": round(pearson(xs, ys), 4),
        "r_between_architecture": round(
            pearson(list(arch_x.values()), list(arch_y.values())), 4),
        "r_within_architecture": round(pearson(cx, cy), 4),
    }


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
    print(f"  wrote {path}")


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)

    print("Loading runs...")
    runs = load_runs()
    print(f"  {len(runs)} runs found")

    problems = check_consistency(runs)

    print("Summarising...")
    internal_metrics = ["test_macro_f1", "test_accuracy",
                        "test_balanced_accuracy", "temperature", "best_epoch"]
    probe_metrics = []
    for probe in ("d3b", "d3c"):
        probe_metrics += [f"{probe}_glioma_rate",
                          f"{probe}_patient_majority_rate",
                          f"{probe}_mean_confidence",
                          f"{probe}_mean_entropy"]

    summary = summarise(runs, internal_metrics + probe_metrics)

    rankings = [ranking_stability(runs, m) for m in
                ("test_macro_f1", "d3b_glioma_rate", "d3c_glioma_rate")]
    rankings = [r for r in rankings if r]

    snrs = [signal_to_noise(runs, m) for m in
            ("test_macro_f1", "d3b_glioma_rate", "d3c_glioma_rate")]
    snrs = [s for s in snrs if s]

    corrs = []
    for probe in ("d3b", "d3c"):
        c = correlation_decomposition(runs, "test_macro_f1", f"{probe}_glioma_rate")
        if c:
            corrs.append(c)

    write_csv(OUTDIR / "sweep_runs_full.csv", runs)
    write_csv(OUTDIR / "architecture_summary.csv", summary)
    write_csv(OUTDIR / "ranking_stability.csv", [
        {"metric": r["metric"], "n_seeds": r["n_seeds"],
         "distinct_orderings": r["distinct_orderings"],
         "orderings": "; ".join(f"{k} ({v})" for k, v in r["orderings"].items()),
         "top_ranked_counts": "; ".join(
             f"{k}:{v}" for k, v in sorted(r["top_ranked_counts"].items()))}
        for r in rankings])
    write_csv(OUTDIR / "signal_to_noise.csv", [
        {"metric": s["metric"],
         "between_architecture_spread": s["between_architecture_spread"],
         "mean_within_architecture_sd": s["mean_within_architecture_sd"],
         "signal_to_noise": s["signal_to_noise"],
         "pairs_overlapping": sum(1 for p in s["pairwise"] if p["overlap"]),
         "pairs_total": len(s["pairwise"])}
        for s in snrs])
    write_csv(OUTDIR / "correlation_decomposition.csv", corrs)

    write_report(runs, summary, rankings, snrs, corrs, problems)
    print("\nDone. See", OUTDIR / "CONSOLIDATED_RESULTS.md")


def write_report(runs, summary, rankings, snrs, corrs, problems):
    L = []
    A = L.append

    A("# Consolidated Seed-Sweep Results")
    A("")
    A(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    run_ids = sorted({r["run_id"] for r in runs if r["run_id"]})
    A(f"Run set: {', '.join(run_ids) or 'unrecorded'}")
    A(f"Runs: {len(runs)} "
      f"({len({r['experiment_id'] for r in runs})} architectures x "
      f"{len({r['seed'] for r in runs})} seeds)")
    A("")
    A("**This file is the authoritative result set.** Any table reporting a single "
      "seed, or the Run A / Run B numbers, is superseded.")
    A("")

    A("## Provenance check")
    A("")
    if problems:
        A("**PROBLEMS FOUND ? do not report these numbers until resolved:**")
        A("")
        for p in problems:
            A(f"- {p}")
    else:
        A("All runs share one run_id, one split hash, an identical seed set, and "
          "identical probe cohorts. Both probes present for every run.")
    A("")

    for probe in ("d3b", "d3c"):
        cohorts = {(r.get(f"{probe}_n_patients"), r.get(f"{probe}_n_slices"))
                   for r in runs if r.get(f"{probe}_n_patients")}
        for n_pat, n_sli in cohorts:
            A(f"- {probe.upper()} cohort: {n_pat} patients, {n_sli} slices")
    A("")

    A("## Per-run results")
    A("")
    A("| Exp | Arch | Seed | macro-F1 | D3B rate | D3C rate | T | commit |")
    A("|---|---|---|---|---|---|---|---|")
    for r in sorted(runs, key=lambda r: (r["experiment_id"], r["seed"])):
        A(f"| {r['experiment_id']} | {r['architecture']} | {r['seed']} | "
          f"{_f(r.get('test_macro_f1'))} | {_f(r.get('d3b_glioma_rate'))} | "
          f"{_f(r.get('d3c_glioma_rate'))} | {_f(r.get('temperature'))} | "
          f"`{r.get('git_commit', '')}` |")
    A("")

    A("## Per-architecture summary (mean +/- sd over seeds)")
    A("")
    A("| Arch | n | Internal macro-F1 | D3B glioma rate | D3C glioma rate |")
    A("|---|---|---|---|---|")
    for s in summary:
        A(f"| {s['architecture']} | {s['n_seeds']} | "
          f"{_ms(s, 'test_macro_f1')} | {_ms(s, 'd3b_glioma_rate')} | "
          f"{_ms(s, 'd3c_glioma_rate')} |")
    A("")

    A("## Ranking stability")
    A("")
    A("How often the architecture ordering changes between seeds. A stable "
      "evaluation gives one ordering; an unstable one gives many.")
    A("")
    A("| Evaluation | Seeds | Distinct orderings | Breakdown |")
    A("|---|---|---|---|")
    for r in rankings:
        A(f"| {r['metric']} | {r['n_seeds']} | {r['distinct_orderings']} | "
          f"{'; '.join(f'{k} ({v})' for k, v in r['orderings'].items())} |")
    A("")

    A("## Signal to noise")
    A("")
    A("Between-architecture spread divided by the mean within-architecture seed SD. "
      "Below ~2 the architecture differences are not resolvable against seed variation.")
    A("")
    A("| Evaluation | Spread | Mean seed SD | S/N | Overlapping pairs |")
    A("|---|---|---|---|---|")
    for s in snrs:
        A(f"| {s['metric']} | {s['between_architecture_spread']} | "
          f"{s['mean_within_architecture_sd']} | **{s['signal_to_noise']}** | "
          f"{sum(1 for p in s['pairwise'] if p['overlap'])}/{len(s['pairwise'])} |")
    A("")
    for s in snrs:
        A(f"**{s['metric']}** pairwise ranges:")
        A("")
        for p in s["pairwise"]:
            verdict = "overlap" if p["overlap"] else "separated"
            A(f"- {p['pair']}: {verdict} ? {p['range_a']} vs {p['range_b']}")
        A("")

    A("## Correlation decomposition")
    A("")
    A("Internal macro-F1 against shifted-domain glioma rate, pooled across runs, "
      "between architecture means, and within architecture after centring. A sign "
      "change between the between- and within- terms is Simpson's paradox.")
    A("")
    A("| Probe | n | r pooled | r between-arch | r within-arch |")
    A("|---|---|---|---|---|")
    for c in corrs:
        A(f"| {c['y'].replace('_glioma_rate', '').upper()} | {c['n_runs']} | "
          f"{c['r_pooled']:+.3f} | {c['r_between_architecture']:+.3f} | "
          f"{c['r_within_architecture']:+.3f} |")
    A("")

    A("## Superseded numbers")
    A("")
    A("Do not report these. They are retained as the historical record only.")
    A("")
    A("| Source | What it contains |")
    A("|---|---|")
    A("| Run A (Ubuntu) | internal, calibration, D3B; no D3C |")
    A("| Run B (Windows) | D3C on the earlier 569-patient cohort |")
    A("| `tables/table_2`, `table_4` | a single seed presented as the result |")
    A("| `tables/table_6` | Run B D3C, superseded cohort |")
    A("")

    with open(OUTDIR / "CONSOLIDATED_RESULTS.md", "w") as fh:
        fh.write("\n".join(L) + "\n")
    print(f"  wrote {OUTDIR / 'CONSOLIDATED_RESULTS.md'}")


def _f(v):
    return f"{v:.4f}" if isinstance(v, (int, float)) else "?"


def _ms(s, m):
    if f"{m}_mean" not in s:
        return "?"
    return f"{s[f'{m}_mean']:.4f} ± {s[f'{m}_sd']:.4f}"


if __name__ == "__main__":
    main()
