"""Run calibration, temperature scaling and the D3B/D3C evaluations across every seed.

Sequencing is not arbitrary. The temperature-scaling scripts call ensure_clean_git(),
so they must run while the tree is clean; every other step dirties it. Each
(seed, architecture) group therefore runs temperature scaling first, then the five steps
that do not care about tree state, then commits once. That is 15 commits rather than 90.

Dependencies within a group:

    temperature_scaling      checkpoint + split          -> temperature_scaling_metrics.json
    calibration              test_predictions.csv        -> calibration_metrics.json
    d3b / d3c                checkpoint + manifest       -> d3*_domain_shift_metrics.json
    d3b / d3c temp-scaled    the above + temperature     -> d3*_temperature_scaled_metrics.json

Resumable: a step whose output already exists is skipped, so an interrupted run can be
restarted without repeating work.

Run from the repository root:

    python scripts/run_eval_sweep.py
    python scripts/run_eval_sweep.py --dry-run
    python scripts/run_eval_sweep.py --seeds 43 44
"""

from datetime import datetime, timedelta
from pathlib import Path
import argparse
import os
import subprocess
import sys
import time


SEEDS = (42, 43, 44, 45, 46)

EXPERIMENTS = (
    ("E001", "resnet18", "e001", "experiments/E001_D1_resnet18_baseline"),
    ("E002", "efficientnet_b0", "e002", "experiments/E002_D1_efficientnet_b0_baseline"),
    ("E003", "vit_b_16", "e003", "experiments/E003_D1_vit_b16_baseline"),
)

# (label, script template, output marker). Order is the execution order; temperature
# scaling is first because it is the only step that requires a clean tree.
STEPS = (
    ("temperature_scaling", "src/calibration/{s}_temperature_scaling.py",
     "temperature_scaling_metrics.json"),
    ("calibration", "src/evaluation/evaluate_{s}_calibration.py",
     "calibration_metrics.json"),
    ("d3b", "src/evaluation/evaluate_{s}_on_d3b.py",
     "d3b_domain_shift_metrics.json"),
    ("d3c", "src/evaluation/evaluate_{s}_on_d3c.py",
     "d3c_domain_shift_metrics.json"),
    ("d3b_temp_scaled", "src/evaluation/evaluate_{s}_d3b_temperature_scaled.py",
     "d3b_temperature_scaled_metrics.json"),
    ("d3c_temp_scaled", "src/evaluation/evaluate_{s}_d3c_temperature_scaled.py",
     "d3c_temperature_scaled_metrics.json"),
)


def git(*args, check=True):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=check)


def working_tree_is_clean():
    return not git("status", "--porcelain").stdout.strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, nargs="+", default=list(SEEDS))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not Path("src/calibration/e001_temperature_scaling.py").exists():
        raise SystemExit("Run this from the repository root.")

    groups = [(seed, exp) for seed in args.seeds for exp in EXPERIMENTS]

    if args.dry_run:
        for seed, (experiment_id, architecture, stem, directory) in groups:
            seed_dir = Path(directory) / f"seed{seed}"
            todo = [
                label for label, _, marker in STEPS
                if not (seed_dir / marker).exists()
            ]
            print(f"{experiment_id} {architecture} seed {seed}: "
                  f"{len(todo)}/{len(STEPS)} steps to run {todo}")
        return 0

    if not working_tree_is_clean():
        raise SystemExit(
            "Working tree is not clean. The temperature-scaling scripts call "
            "ensure_clean_git() and would abort.\n" + git("status", "--porcelain").stdout
        )

    started = time.monotonic()
    ran = skipped = 0

    for seed, (experiment_id, architecture, stem, directory) in groups:
        seed_dir = Path(directory) / f"seed{seed}"
        print(f"\n=== {experiment_id} {architecture} seed {seed} "
              f"{datetime.now().isoformat(timespec='seconds')} ===")

        if not (seed_dir / "best_model.pt").exists():
            raise SystemExit(
                f"Missing checkpoint {seed_dir / 'best_model.pt'}. Run the seed sweep "
                "first."
            )

        for label, template, marker in STEPS:
            if (seed_dir / marker).exists():
                print(f"    skip {label} (already present)")
                skipped += 1
                continue

            script = template.format(s=stem)
            step_started = time.monotonic()

            result = subprocess.run(
                [sys.executable, script],
                env=dict(os.environ, SEED=str(seed)),
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                sys.stdout.write(result.stdout[-3000:])
                sys.stderr.write(result.stderr[-3000:])
                raise SystemExit(
                    f"\n{experiment_id} seed {seed} step {label} failed with exit code "
                    f"{result.returncode}. Stopping so the failure is not buried. Fix "
                    "and re-run; completed steps are skipped."
                )

            elapsed = timedelta(seconds=round(time.monotonic() - step_started))
            print(f"    {label} in {elapsed}")
            ran += 1

        git("add", "experiments", "reports")
        if git("diff", "--cached", "--name-only").stdout.strip():
            message = (
                f"{experiment_id} {architecture} seed {seed}: calibration, temperature "
                f"scaling, D3B and D3C evaluation\n\n"
                f"Produced by scripts/run_eval_sweep.py. D3C uses the analysis cohort "
                f"(610 series / 3050 slices) after the documented non-axial exclusion.\n"
            )
            subprocess.run(["git", "commit", "-q", "-m", message], check=True)
            print(f"    committed {git('rev-parse', '--short', 'HEAD').stdout.strip()}")

        if not working_tree_is_clean():
            raise SystemExit(
                "Tree still dirty after commit; the next temperature-scaling step would "
                "abort.\n" + git("status", "--porcelain").stdout
            )

    total = timedelta(seconds=round(time.monotonic() - started))
    print(f"\nEvaluation sweep complete: {ran} steps run, {skipped} skipped, in {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
