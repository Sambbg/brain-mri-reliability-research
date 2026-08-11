"""Statistical analysis of the seed sweep: internal-vs-shift correlation, and inference
on the D3C glioma prediction rates.

This is the first consumer of src/stats. It reads the 15 runs of run set
2026-08-sweep-a and produces:

Part 1, correlation. Internal test macro-F1 against D3C slice-level glioma prediction
rate, pooled over all 15 runs, within each architecture, and pooled after removing
architecture means. The three answers can disagree, and the pooled one is the least
trustworthy: architecture is a confounder, so a pooled correlation mixes the
between-architecture relationship with the within-architecture one and can even reverse
its sign relative to both (Simpson's paradox). The architecture-centred correlation is
the estimate that answers "does a better internal score predict a worse shifted-domain
rate, holding architecture fixed".

Part 2, inference on D3C.
  - Patient-clustered bootstrap CI for every one of the 15 glioma prediction rates.
    Slices are five per patient and highly correlated, so a slice-level interval would
    be far too narrow.
  - McNemar with Holm correction for the three pairwise model comparisons at each seed.
    The models score identical slices, so the comparison is paired.
  - Random-intercept logistic regression, glioma_predicted ~ model + (1|patient), fitted
    per seed with E001 as the reference level, so the model[E002] coefficient is the
    E001-vs-E002 contrast directly.

Run from the repository root:

    python src/evaluation/analyse_seed_sweep_statistics.py
"""

from datetime import datetime
from pathlib import Path
import json
import math
import sys

import numpy as np
import pandas as pd
from scipy.stats import norm, pearsonr, spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "stats"))

from clustered_bootstrap import clustered_bootstrap_ci, intraclass_correlation  # noqa: E402
from mcnemar import mcnemar_family  # noqa: E402
from mixed_effects import fit_d3c_glioma_model  # noqa: E402


EXPERIMENTS = (
    ("E001", "ResNet18", "experiments/E001_D1_resnet18_baseline"),
    ("E002", "EfficientNet-B0", "experiments/E002_D1_efficientnet_b0_baseline"),
    ("E003", "ViT-B/16", "experiments/E003_D1_vit_b16_baseline"),
)
SEEDS = (42, 43, 44, 45, 46)
REFERENCE_MODEL = "E001"

REPORT_PATH = Path("reports/experiments/D3C_seed_sweep_statistics.md")
RUNS_CSV = Path("reports/experiments/tables/seed_sweep_runs.csv")
BOOTSTRAP_CSV = Path("reports/experiments/tables/d3c_bootstrap_intervals.csv")
MCNEMAR_CSV = Path("reports/experiments/tables/d3c_mcnemar_holm.csv")
MIXED_CSV = Path("reports/experiments/tables/d3c_mixed_effects.csv")

BOOTSTRAP_RESAMPLES = 2000
BOOTSTRAP_SEED = 20260812
QUADRATURE_NODES = 31


def seed_dir(directory, seed):
    return Path(directory) / f"seed{seed}"


def load_runs():
    """One row per run: internal macro-F1 and D3C rate, plus the run's provenance."""
    rows = []

    for experiment_id, architecture, directory in EXPERIMENTS:
        for seed in SEEDS:
            base = seed_dir(directory, seed)
            final = json.loads((base / "final_results.json").read_text())
            shift = json.loads((base / "d3c_domain_shift_metrics.json").read_text())
            provenance = json.loads((base / "provenance.json").read_text())

            rows.append({
                "experiment_id": experiment_id,
                "architecture": architecture,
                "seed": seed,
                "run_id": provenance["run_id"],
                "test_macro_f1": final["test_macro_f1"],
                "d3c_glioma_rate": shift["glioma_prediction_rate"],
                "d3c_slices": shift["n_slices"],
                "d3c_patients": shift["n_patients"],
            })

    frame = pd.DataFrame(rows)

    run_ids = set(frame["run_id"])
    if len(run_ids) != 1:
        raise RuntimeError(f"Runs span more than one run set: {sorted(run_ids)}")

    return frame


def load_predictions(seed):
    """Slice-level glioma predictions for the three models at one seed, aligned.

    Merged on output_image_path rather than assumed to be row-aligned: McNemar is a
    paired test and silently mispairing rows would invalidate it.
    """
    merged = None

    for experiment_id, _, directory in EXPERIMENTS:
        path = seed_dir(directory, seed) / "d3c_predictions.csv"
        frame = pd.read_csv(path, usecols=["output_image_path", "patient_id", "pred_label"])
        frame[experiment_id] = (frame["pred_label"] == "glioma").astype(int)
        frame = frame[["output_image_path", "patient_id", experiment_id]]

        if merged is None:
            merged = frame
        else:
            merged = merged.merge(
                frame.drop(columns=["patient_id"]), on="output_image_path", how="inner"
            )

    expected = len(pd.read_csv(
        seed_dir(EXPERIMENTS[0][2], seed) / "d3c_predictions.csv", usecols=["output_image_path"]
    ))
    if len(merged) != expected:
        raise RuntimeError(
            f"Seed {seed}: models do not cover identical slices "
            f"({len(merged)} matched of {expected}). Paired tests would be invalid."
        )

    return merged


def fisher_interval(r, n, confidence=0.95):
    """Fisher z confidence interval for a Pearson correlation."""
    if n < 4 or not np.isfinite(r) or abs(r) >= 1.0:
        return (float("nan"), float("nan"))

    z = math.atanh(r)
    se = 1.0 / math.sqrt(n - 3)
    critical = float(norm.ppf(0.5 + confidence / 2.0))

    return (math.tanh(z - critical * se), math.tanh(z + critical * se))


def correlation_analysis(runs):
    results = []

    def record(label, x, y, n_effective, note):
        if len(x) < 3:
            return
        r, p = pearsonr(x, y)
        rho, p_rho = spearmanr(x, y)
        low, high = fisher_interval(r, n_effective)
        results.append({
            "grouping": label,
            "n": len(x),
            "pearson_r": r,
            "pearson_p": p,
            "pearson_ci_low": low,
            "pearson_ci_high": high,
            "spearman_rho": rho,
            "spearman_p": p_rho,
            "note": note,
        })

    record(
        "pooled (all 15 runs)",
        runs["test_macro_f1"].to_numpy(),
        runs["d3c_glioma_rate"].to_numpy(),
        len(runs),
        "confounded by architecture; reported for completeness only",
    )

    for experiment_id, architecture, _ in EXPERIMENTS:
        subset = runs[runs["experiment_id"] == experiment_id]
        record(
            f"{experiment_id} {architecture} (within, n=5)",
            subset["test_macro_f1"].to_numpy(),
            subset["d3c_glioma_rate"].to_numpy(),
            len(subset),
            "n=5, very low power; |r| must exceed about 0.88 for p<0.05",
        )

    centred = runs.copy()
    for column in ("test_macro_f1", "d3c_glioma_rate"):
        centred[column] = centred[column] - centred.groupby("experiment_id")[column].transform("mean")

    record(
        "architecture-centred (within-architecture pooled)",
        centred["test_macro_f1"].to_numpy(),
        centred["d3c_glioma_rate"].to_numpy(),
        len(centred) - len(EXPERIMENTS),
        "architecture means removed; this is the within-architecture estimate",
    )

    return pd.DataFrame(results)


def bootstrap_analysis(runs):
    rows = []

    for experiment_id, architecture, directory in EXPERIMENTS:
        for seed in SEEDS:
            frame = pd.read_csv(
                seed_dir(directory, seed) / "d3c_predictions.csv",
                usecols=["patient_id", "pred_label"],
            )
            values = (frame["pred_label"] == "glioma").astype(float).to_numpy()
            patients = frame["patient_id"].to_numpy()

            interval = clustered_bootstrap_ci(
                values, patients,
                n_resamples=BOOTSTRAP_RESAMPLES, seed=BOOTSTRAP_SEED,
            )
            icc = intraclass_correlation(values, patients)

            rows.append({
                "experiment_id": experiment_id,
                "architecture": architecture,
                "seed": seed,
                "glioma_rate": interval.estimate,
                "ci_low": interval.lower,
                "ci_high": interval.upper,
                "ci_width": interval.width,
                "icc": icc,
                "n_patients": interval.n_patients,
                "n_slices": interval.n_observations,
            })

    return pd.DataFrame(rows)


def mcnemar_analysis():
    rows = []

    for seed in SEEDS:
        predictions = load_predictions(seed)
        comparisons = [
            ("E001 vs E002", predictions["E001"].to_numpy(), predictions["E002"].to_numpy()),
            ("E001 vs E003", predictions["E001"].to_numpy(), predictions["E003"].to_numpy()),
            ("E002 vs E003", predictions["E002"].to_numpy(), predictions["E003"].to_numpy()),
        ]

        for result in mcnemar_family(comparisons):
            rows.append({
                "seed": seed,
                "comparison": result.label,
                "n_pairs": result.n_pairs,
                "b": result.b,
                "c": result.c,
                "n_discordant": result.n_discordant,
                "method": result.method,
                "p_value": result.p_value,
                "p_holm": result.p_value_adjusted,
                "significant_holm_0.05": result.p_value_adjusted < 0.05,
            })

    return pd.DataFrame(rows)


def mixed_effects_analysis():
    rows = []

    for seed in SEEDS:
        predictions = load_predictions(seed)

        long = pd.concat([
            pd.DataFrame({
                "glioma": predictions[experiment_id],
                "model": experiment_id,
                "patient": predictions["patient_id"],
            })
            for experiment_id, _, _ in EXPERIMENTS
        ], ignore_index=True)

        fit = fit_d3c_glioma_model(
            long["glioma"].to_numpy(),
            long["model"].tolist(),
            long["patient"].to_numpy(),
            reference_model=REFERENCE_MODEL,
            n_quadrature=QUADRATURE_NODES,
        )

        for term in fit.terms:
            low = term.estimate - 1.959964 * term.std_error
            high = term.estimate + 1.959964 * term.std_error
            rows.append({
                "seed": seed,
                "term": term.name,
                "estimate_log_odds": term.estimate,
                "std_error": term.std_error,
                "z": term.z_value,
                "p_value": term.p_value,
                "odds_ratio": term.odds_ratio,
                "or_ci_low": math.exp(low),
                "or_ci_high": math.exp(high),
                "patient_sd": fit.group_sd,
                "icc": fit.icc,
                "converged": fit.converged,
                "n_observations": fit.n_observations,
                "n_patients": fit.n_groups,
            })

    return pd.DataFrame(rows)


def write_report(runs, correlations, bootstrap, mcnemar, mixed):
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    contrast_term = f"model[E002]"
    e002 = mixed[mixed["term"] == contrast_term]

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# D3C Seed Sweep Statistics\n\n")
        f.write(f"Generated: {datetime.now().isoformat(timespec='seconds')}\n\n")
        f.write(
            f"Run set `{runs['run_id'].iloc[0]}`, {len(runs)} runs "
            f"({len(EXPERIMENTS)} architectures x {len(SEEDS)} seeds). D3C analysis "
            f"cohort: {int(runs['d3c_patients'].iloc[0])} patients, "
            f"{int(runs['d3c_slices'].iloc[0])} slices.\n\n"
        )

        f.write("## Part 1: Internal Performance against Shifted-Domain Behaviour\n\n")
        f.write(
            "Pearson r with a Fisher-z interval, and Spearman rho. Read the "
            "architecture-centred row, not the pooled one: architecture is a confounder, "
            "and a pooled correlation mixes the between-architecture relationship with "
            "the within-architecture one.\n\n"
        )
        f.write("| Grouping | n | Pearson r | 95% CI | p | Spearman rho | p |\n")
        f.write("|---|---:|---:|---|---:|---:|---:|\n")
        for _, row in correlations.iterrows():
            f.write(
                f"| {row['grouping']} | {row['n']} | {row['pearson_r']:.3f} | "
                f"[{row['pearson_ci_low']:.3f}, {row['pearson_ci_high']:.3f}] | "
                f"{row['pearson_p']:.4f} | {row['spearman_rho']:.3f} | "
                f"{row['spearman_p']:.4f} |\n"
            )
        f.write("\nNotes:\n\n")
        for _, row in correlations.iterrows():
            f.write(f"- {row['grouping']}: {row['note']}\n")

        f.write("\n## Part 2a: Patient-Clustered Bootstrap Intervals\n\n")
        f.write(
            f"{BOOTSTRAP_RESAMPLES} resamples of patients, not slices. Each patient "
            "contributes five correlated slices, so a slice-level interval would be too "
            "narrow by roughly the design effect.\n\n"
        )
        f.write("| Model | Seed | Glioma rate | 95% CI | Width | ICC |\n")
        f.write("|---|---:|---:|---|---:|---:|\n")
        for _, row in bootstrap.iterrows():
            f.write(
                f"| {row['experiment_id']} {row['architecture']} | {row['seed']} | "
                f"{row['glioma_rate']:.4f} | [{row['ci_low']:.4f}, {row['ci_high']:.4f}] | "
                f"{row['ci_width']:.4f} | {row['icc']:.3f} |\n"
            )

        f.write("\n## Part 2b: McNemar with Holm Correction\n\n")
        f.write(
            "Paired over identical slices, corrected across the three comparisons within "
            "each seed.\n\n"
        )
        f.write("| Seed | Comparison | b | c | Discordant | Method | p | Holm p | Sig. |\n")
        f.write("|---|---|---:|---:|---:|---|---:|---:|---|\n")
        for _, row in mcnemar.iterrows():
            f.write(
                f"| {row['seed']} | {row['comparison']} | {row['b']} | {row['c']} | "
                f"{row['n_discordant']} | {row['method']} | {row['p_value']:.3e} | "
                f"{row['p_holm']:.3e} | {'yes' if row['significant_holm_0.05'] else 'no'} |\n"
            )

        f.write("\n## Part 2c: Random-Intercept Logistic Regression\n\n")
        f.write(
            "`glioma_predicted ~ model + (1|patient)`, fitted per seed with E001 as the "
            "reference level. The `model[E002]` coefficient is therefore the E001-vs-E002 "
            "contrast: a log odds ratio for predicting glioma, holding the patient fixed.\n\n"
        )
        f.write("| Seed | Term | log OR | SE | OR | 95% CI | p | Patient SD | ICC |\n")
        f.write("|---|---|---:|---:|---:|---|---:|---:|---:|\n")
        for _, row in mixed.iterrows():
            f.write(
                f"| {row['seed']} | {row['term']} | {row['estimate_log_odds']:.4f} | "
                f"{row['std_error']:.4f} | {row['odds_ratio']:.4f} | "
                f"[{row['or_ci_low']:.4f}, {row['or_ci_high']:.4f}] | "
                f"{row['p_value']:.3e} | {row['patient_sd']:.3f} | {row['icc']:.3f} |\n"
            )

        f.write("\n## The E001 vs E002 Contrast\n\n")
        f.write(
            "The paper's central comparison. Internally these two models are separated "
            "by 0.0011 macro-F1, a fraction of their seed-to-seed spread, and they swap "
            "rank between seeds. Under shift:\n\n"
        )
        f.write("| Seed | OR (E002 vs E001) | 95% CI | p | Direction |\n")
        f.write("|---|---:|---|---:|---|\n")
        for _, row in e002.iterrows():
            direction = "E002 lower" if row["odds_ratio"] < 1 else "E002 higher"
            f.write(
                f"| {row['seed']} | {row['odds_ratio']:.4f} | "
                f"[{row['or_ci_low']:.4f}, {row['or_ci_high']:.4f}] | "
                f"{row['p_value']:.3e} | {direction} |\n"
            )

        consistent = (e002["odds_ratio"] < 1).all() or (e002["odds_ratio"] > 1).all()
        all_significant = (e002["p_value"] < 0.05).all()
        f.write(
            f"\nDirection consistent across all {len(e002)} seeds: "
            f"{'yes' if consistent else 'no'}. "
            f"Significant at every seed: {'yes' if all_significant else 'no'}.\n"
        )

        f.write("\n## Limitations\n\n")
        f.write(
            "- The within-architecture correlations have n=5. They are descriptive; "
            "|r| must exceed about 0.88 to reach p<0.05 at that size.\n"
            "- The mixed model is fitted per seed. Pooling seeds would need a second "
            "random effect for seed, which is not implemented.\n"
            "- Quadrature is fixed at "
            f"{QUADRATURE_NODES} nodes and is not adaptive; stability against node count "
            "was checked at this data shape in the src/stats test suite.\n"
            "- D3C carries no slice-level ground truth. These are prediction rates under "
            "shift, not accuracy.\n"
        )


def main():
    runs = load_runs()
    RUNS_CSV.parent.mkdir(parents=True, exist_ok=True)
    runs.to_csv(RUNS_CSV, index=False)

    print("Part 1: correlation")
    correlations = correlation_analysis(runs)
    print(correlations[["grouping", "n", "pearson_r", "pearson_p", "spearman_rho"]].to_string(index=False))

    print("\nPart 2a: patient-clustered bootstrap")
    bootstrap = bootstrap_analysis(runs)
    bootstrap.to_csv(BOOTSTRAP_CSV, index=False)
    print(f"  {len(bootstrap)} intervals, median width {bootstrap['ci_width'].median():.4f}, "
          f"median ICC {bootstrap['icc'].median():.3f}")

    print("\nPart 2b: McNemar with Holm")
    mcnemar = mcnemar_analysis()
    mcnemar.to_csv(MCNEMAR_CSV, index=False)
    print(f"  {len(mcnemar)} comparisons, "
          f"{int(mcnemar['significant_holm_0.05'].sum())} significant after Holm")

    print("\nPart 2c: random-intercept logistic regression")
    mixed = mixed_effects_analysis()
    mixed.to_csv(MIXED_CSV, index=False)
    contrast = mixed[mixed["term"] == "model[E002]"]
    for _, row in contrast.iterrows():
        print(f"  seed {row['seed']}: OR(E002 vs E001) = {row['odds_ratio']:.4f} "
              f"[{row['or_ci_low']:.4f}, {row['or_ci_high']:.4f}], p = {row['p_value']:.3e}")

    write_report(runs, correlations, bootstrap, mcnemar, mixed)
    print(f"\nReport: {REPORT_PATH}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
