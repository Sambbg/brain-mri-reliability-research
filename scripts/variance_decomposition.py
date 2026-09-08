#!/usr/bin/env python3
"""
Variance decomposition for the architecture comparison.

The manuscript characterises how well each evaluation separates the three
architectures using a signal-to-noise ratio: the between-architecture spread
divided by the mean within-architecture standard deviation across seeds. That
ratio is defined by this study and has no distributional theory behind it, so a
reader cannot judge whether a value of 2.52 is small without taking the
manuscript's word for it.

This script replaces it with a standard analysis of the same design.

The design is balanced: three architectures, five seeds, every seed appearing
once with every architecture. That is a randomised complete block design with
architecture as the treatment and seed as the block, and it has an exact
classical treatment:

    y_ij = mu + alpha_i + b_j + e_ij        b_j ~ N(0, s_b^2),  e_ij ~ N(0, s_e^2)

Reported per evaluation:

  - F test for the architecture effect, with degrees of freedom and p value
  - Variance components for seed and residual, from expected mean squares
  - The share of total variance attributable to each
  - Partial eta squared and omega squared for the architecture effect
  - Pairwise architecture contrasts with Holm-corrected p values and 95%
    confidence intervals on the differences
  - The manuscript's signal-to-noise ratio alongside, so the two can be compared

Blocking on seed is what makes this the right analysis rather than a one-way
ANOVA: the same five seeds are used for every architecture, so the runs are
paired across architectures and treating them as independent would discard that.

Run from the repo root:
    python scripts/variance_decomposition.py

Writes to reports/experiments/consolidated/:
    variance_decomposition.csv
    variance_decomposition.md
"""

import csv
import json
import itertools
import sys
from pathlib import Path

import numpy as np
from scipy import stats

EXPERIMENTS = Path("experiments")
OUT = Path("reports/experiments/consolidated")

ARCH = {"E001": "ResNet18", "E002": "EfficientNet-B0", "E003": "ViT-B/16"}
ORDER = ["E001", "E002", "E003"]

METRICS = [
    ("macro_f1", "Internal test macro-F1"),
    ("d3b", "D3B glioma assignment rate (canine, n = 53)"),
    ("d3c", "D3C glioma assignment rate (human, n = 610)"),
]


def dig(obj, key):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key and not isinstance(v, (dict, list)):
                return v
            if isinstance(v, dict):
                found = dig(v, key)
                if found is not None:
                    return found
    return None


def load():
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
            fr = sd / "final_results.json"
            if not fr.exists():
                continue
            with open(fr) as fh:
                data = json.load(fh)
            rec = {"exp": exp_id, "seed": int(sd.name.replace("seed", "")),
                   "macro_f1": data.get("test_macro_f1")}
            for probe in ("d3b", "d3c"):
                p = sd / f"{probe}_domain_shift_metrics.json"
                if p.exists():
                    with open(p) as fh:
                        rec[probe] = dig(json.load(fh), "glioma_prediction_rate")
            runs.append(rec)
    return runs


def build_matrix(runs, metric):
    """Rows = architectures, columns = seeds. Returns (matrix, seeds)."""
    seeds = sorted({r["seed"] for r in runs})
    M = np.full((len(ORDER), len(seeds)), np.nan)
    for r in runs:
        if r.get(metric) is None:
            continue
        i = ORDER.index(r["exp"])
        j = seeds.index(r["seed"])
        M[i, j] = r[metric]
    return M, seeds


def rcbd(M):
    """Randomised complete block design ANOVA on a balanced a x b matrix."""
    a, b = M.shape                      # a treatments, b blocks
    grand = M.mean()
    row_means = M.mean(axis=1)          # architecture means
    col_means = M.mean(axis=0)          # seed means

    ss_treat = b * np.sum((row_means - grand) ** 2)
    ss_block = a * np.sum((col_means - grand) ** 2)
    ss_total = np.sum((M - grand) ** 2)
    ss_error = ss_total - ss_treat - ss_block

    df_treat, df_block = a - 1, b - 1
    df_error = df_treat * df_block

    ms_treat = ss_treat / df_treat
    ms_block = ss_block / df_block
    ms_error = ss_error / df_error

    f_treat = ms_treat / ms_error
    f_block = ms_block / ms_error
    p_treat = 1 - stats.f.cdf(f_treat, df_treat, df_error)
    p_block = 1 - stats.f.cdf(f_block, df_block, df_error)

    # variance components from expected mean squares
    var_block = max((ms_block - ms_error) / a, 0.0)
    var_error = ms_error
    # treatment is fixed, so its "variance" is a quadratic form, reported as
    # the added variance component for comparability only
    var_treat = max((ms_treat - ms_error) / b, 0.0)
    var_total = var_treat + var_block + var_error

    eta_p = ss_treat / (ss_treat + ss_error)
    omega = max((ss_treat - df_treat * ms_error) / (ss_total + ms_error), 0.0)

    return {
        "a": a, "b": b, "grand": grand, "row_means": row_means,
        "ss_treat": ss_treat, "ss_block": ss_block, "ss_error": ss_error,
        "ss_total": ss_total,
        "df_treat": df_treat, "df_block": df_block, "df_error": df_error,
        "ms_treat": ms_treat, "ms_block": ms_block, "ms_error": ms_error,
        "f_treat": f_treat, "p_treat": p_treat,
        "f_block": f_block, "p_block": p_block,
        "var_treat": var_treat, "var_block": var_block, "var_error": var_error,
        "var_total": var_total,
        "eta_p": eta_p, "omega": omega,
    }


def contrasts(M, res):
    """Pairwise architecture differences with Holm-corrected p and 95% CI."""
    b, ms_error, df_error = res["b"], res["ms_error"], res["df_error"]
    se = np.sqrt(2 * ms_error / b)
    tcrit = stats.t.ppf(0.975, df_error)

    out = []
    for i, j in itertools.combinations(range(len(ORDER)), 2):
        diff = res["row_means"][i] - res["row_means"][j]
        t = diff / se
        p = 2 * (1 - stats.t.cdf(abs(t), df_error))
        out.append({"i": ORDER[i], "j": ORDER[j], "diff": diff,
                    "se": se, "t": t, "p_raw": p,
                    "lo": diff - tcrit * se, "hi": diff + tcrit * se})

    # Holm correction
    order = sorted(range(len(out)), key=lambda k: out[k]["p_raw"])
    m = len(out)
    running = 0.0
    for rank, k in enumerate(order):
        adj = (m - rank) * out[k]["p_raw"]
        running = max(running, adj)
        out[k]["p_holm"] = min(running, 1.0)
    return out


def manuscript_snr(M):
    """The ratio the manuscript reports, for side-by-side comparison."""
    row_means = M.mean(axis=1)
    row_sds = M.std(axis=1, ddof=1)
    spread = row_means.max() - row_means.min()
    mean_sd = row_sds.mean()
    return spread, mean_sd, (spread / mean_sd if mean_sd else float("inf"))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    runs = load()
    if not runs:
        sys.exit("No runs found.")
    print(f"Loaded {len(runs)} runs")

    rows, blocks = [], {}

    for metric, label in METRICS:
        M, seeds = build_matrix(runs, metric)
        if np.isnan(M).any():
            print(f"  skipping {metric}: incomplete design")
            continue
        res = rcbd(M)
        cons = contrasts(M, res)
        spread, mean_sd, snr = manuscript_snr(M)
        blocks[metric] = (label, M, seeds, res, cons, spread, mean_sd, snr)

        rows.append({
            "evaluation": label,
            "F_architecture": round(res["f_treat"], 3),
            "df": f"{res['df_treat']},{res['df_error']}",
            "p_architecture": f"{res['p_treat']:.4f}",
            "F_seed_block": round(res["f_block"], 3),
            "p_seed_block": f"{res['p_block']:.4f}",
            "var_seed": f"{res['var_block']:.3e}",
            "var_residual": f"{res['var_error']:.3e}",
            "pct_var_seed": f"{100*res['var_block']/res['var_total']:.1f}",
            "pct_var_residual": f"{100*res['var_error']/res['var_total']:.1f}",
            "partial_eta_sq": round(res["eta_p"], 3),
            "omega_sq": round(res["omega"], 3),
            "manuscript_SNR": round(snr, 2),
        })

    with open(OUT / "variance_decomposition.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"  wrote {OUT / 'variance_decomposition.csv'}")

    # ------------------------------ report ------------------------------
    L = []
    A = L.append
    A("# Variance decomposition of the architecture comparison")
    A("")
    A("The manuscript reports a signal-to-noise ratio, defined as the")
    A("between-architecture spread divided by the mean within-architecture standard")
    A("deviation across seeds. That quantity is defined by this study and has no")
    A("distributional theory behind it, so a reader cannot judge whether 2.52 is")
    A("small without accepting the manuscript's interpretation.")
    A("")
    A("The design is balanced: three architectures, five seeds, every seed appearing")
    A("once with every architecture. That is a randomised complete block design with")
    A("architecture as the treatment and seed as the block, and it admits an exact")
    A("classical analysis. Blocking on seed is what makes this correct rather than a")
    A("one-way ANOVA: the same five seeds are used for every architecture, so runs")
    A("are paired across architectures.")
    A("")
    A("    y_ij = mu + alpha_i + b_j + e_ij,   b_j ~ N(0, s_b^2),  e_ij ~ N(0, s_e^2)")
    A("")

    A("## Summary")
    A("")
    A("| Evaluation | F (arch) | df | p | partial eta^2 | omega^2 | Manuscript SNR |")
    A("|---|---|---|---|---|---|---|")
    for metric, _ in METRICS:
        if metric not in blocks:
            continue
        label, M, seeds, res, cons, spread, mean_sd, snr = blocks[metric]
        A(f"| {label} | {res['f_treat']:.2f} | {res['df_treat']},{res['df_error']} | "
          f"{res['p_treat']:.4f} | {res['eta_p']:.3f} | {res['omega']:.3f} | {snr:.2f} |")
    A("")

    A("## Variance components")
    A("")
    A("Estimated from expected mean squares. The seed component is the variance")
    A("attributable to the random seed, shared across architectures within a run.")
    A("")
    A("| Evaluation | Seed variance | Residual variance | Seed share | Residual share |")
    A("|---|---|---|---|---|")
    for metric, _ in METRICS:
        if metric not in blocks:
            continue
        label, M, seeds, res, cons, spread, mean_sd, snr = blocks[metric]
        tot = res["var_block"] + res["var_error"]
        A(f"| {label} | {res['var_block']:.3e} | {res['var_error']:.3e} | "
          f"{100*res['var_block']/tot:.1f}% | {100*res['var_error']/tot:.1f}% |")
    A("")

    for metric, _ in METRICS:
        if metric not in blocks:
            continue
        label, M, seeds, res, cons, spread, mean_sd, snr = blocks[metric]
        A(f"## {label}")
        A("")
        A("### ANOVA table")
        A("")
        A("| Source | SS | df | MS | F | p |")
        A("|---|---|---|---|---|---|")
        A(f"| Architecture | {res['ss_treat']:.5e} | {res['df_treat']} | "
          f"{res['ms_treat']:.5e} | {res['f_treat']:.3f} | {res['p_treat']:.4f} |")
        A(f"| Seed (block) | {res['ss_block']:.5e} | {res['df_block']} | "
          f"{res['ms_block']:.5e} | {res['f_block']:.3f} | {res['p_block']:.4f} |")
        A(f"| Residual | {res['ss_error']:.5e} | {res['df_error']} | "
          f"{res['ms_error']:.5e} | | |")
        A(f"| Total | {res['ss_total']:.5e} | {res['a']*res['b']-1} | | | |")
        A("")

        A("### Pairwise contrasts")
        A("")
        A("| Comparison | Difference | 95% CI | t | p raw | p Holm |")
        A("|---|---|---|---|---|---|")
        for c in cons:
            sig = " *" if c["p_holm"] < 0.05 else ""
            A(f"| {ARCH[c['i']]} - {ARCH[c['j']]} | {c['diff']:+.4f} | "
              f"[{c['lo']:+.4f}, {c['hi']:+.4f}] | {c['t']:+.2f} | "
              f"{c['p_raw']:.4f} | {c['p_holm']:.4f}{sig} |")
        A("")
        ns = [c for c in cons if c["p_holm"] >= 0.05]
        if ns:
            A("Not separated after correction: " +
              "; ".join(f"{ARCH[c['i']]} vs {ARCH[c['j']]}" for c in ns) + ".")
        else:
            A("All pairwise differences remain significant after Holm correction.")
        A("")

    A("## Relation to the reported signal-to-noise ratio")
    A("")
    A("| Evaluation | Spread | Mean seed SD | SNR | F | p |")
    A("|---|---|---|---|---|---|")
    for metric, _ in METRICS:
        if metric not in blocks:
            continue
        label, M, seeds, res, cons, spread, mean_sd, snr = blocks[metric]
        A(f"| {label} | {spread:.4f} | {mean_sd:.4f} | {snr:.2f} | "
          f"{res['f_treat']:.2f} | {res['p_treat']:.4f} |")
    A("")
    A("The two quantities measure related things but are not interchangeable. The")
    A("signal-to-noise ratio compares the spread of architecture means against the")
    A("average scatter within an architecture; the F statistic compares the same")
    A("spread against residual variation after removing the seed effect, which is")
    A("the correct denominator for a blocked design. Where the seed effect is large,")
    A("the F test has more power than the ratio suggests, because blocking removes")
    A("that variation from the error term.")
    A("")
    A("Recommendation: report the F test, its p value and the pairwise contrasts as")
    A("the primary analysis, and retain the signal-to-noise ratio only as a")
    A("descriptive summary with its definition stated. That answers the objection")
    A("that the ratio and its threshold are defined by this study.")
    A("")

    with open(OUT / "variance_decomposition.md", "w") as fh:
        fh.write("\n".join(L) + "\n")
    print(f"  wrote {OUT / 'variance_decomposition.md'}")

    # ------------------------------ console ------------------------------
    print()
    for metric, _ in METRICS:
        if metric not in blocks:
            continue
        label, M, seeds, res, cons, spread, mean_sd, snr = blocks[metric]
        tot = res["var_block"] + res["var_error"]
        print(f"{label}")
        print(f"  architecture  F({res['df_treat']},{res['df_error']}) = "
              f"{res['f_treat']:.2f}, p = {res['p_treat']:.4f}, "
              f"partial eta^2 = {res['eta_p']:.3f}")
        print(f"  seed block    F({res['df_block']},{res['df_error']}) = "
              f"{res['f_block']:.2f}, p = {res['p_block']:.4f}, "
              f"seed share of random variance = {100*res['var_block']/tot:.1f}%")
        print(f"  manuscript SNR = {snr:.2f}")
        for c in cons:
            mark = "*" if c["p_holm"] < 0.05 else " "
            print(f"    {ARCH[c['i']]:<16} - {ARCH[c['j']]:<16} "
                  f"{c['diff']:+.4f}  p_holm {c['p_holm']:.4f} {mark}")
        print()


if __name__ == "__main__":
    main()
