"""Run the seed sweep: every architecture at every seed, under one RUN_ID.

Each training run writes to experiments/<experiment>/seed<N>/ and is committed before
the next run starts, because the trainers call ensure_clean_git() and experiment
artefacts are version-controlled (rule 6). Without a commit between runs the second run
would abort on a dirty tree.

The sweep is resumable. A (seed, architecture) pair whose provenance.json already
records this RUN_ID and that seed is skipped, so an interrupted sweep can be restarted
without repeating completed work or overwriting it.

Run from the repository root with RUN_ID set:

    RUN_ID=2026-08-sweep-a python scripts/run_seed_sweep.py
    RUN_ID=2026-08-sweep-a python scripts/run_seed_sweep.py --dry-run
    RUN_ID=2026-08-sweep-a python scripts/run_seed_sweep.py --seeds 43 44
"""

from datetime import datetime, timedelta
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
import time


SEEDS = (42, 43, 44, 45, 46)

TRAINERS = (
    ("E001", "resnet18", "src/training/train_e001_resnet18.py",
     "experiments/E001_D1_resnet18_baseline"),
    ("E002", "efficientnet_b0", "src/training/train_e002_efficientnet_b0.py",
     "experiments/E002_D1_efficientnet_b0_baseline"),
    ("E003", "vit_b_16", "src/training/train_e003_vit_b16.py",
     "experiments/E003_D1_vit_b16_baseline"),
)


def git(*args, check=True):
    return subprocess.run(
        ["git", *args], capture_output=True, text=True, check=check
    )


def working_tree_is_clean():
    return not git("status", "--porcelain").stdout.strip()


def require_run_id():
    run_id = os.environ.get("RUN_ID", "").strip()

    if not run_id:
        raise SystemExit(
            "RUN_ID is not set. Declare the sweep's run set explicitly, for example:\n"
            "  RUN_ID=2026-08-sweep-a python scripts/run_seed_sweep.py"
        )

    return run_id


def already_done(experiment_dir, seed, run_id):
    """True when this exact (run_id, seed) pair has already produced artefacts."""
    provenance_path = Path(experiment_dir) / f"seed{seed}" / "provenance.json"

    if not provenance_path.exists():
        return False

    try:
        with provenance_path.open(encoding="utf-8") as f:
            provenance = json.load(f)
    except (OSError, json.JSONDecodeError):
        return False

    return provenance.get("run_id") == run_id and provenance.get("seed") == seed


def commit_run(experiment_id, architecture, seed, run_id):
    """Commit this run's artefacts so the next run passes ensure_clean_git()."""
    git("add", "experiments")

    if not git("diff", "--cached", "--name-only").stdout.strip():
        # A byte-identical re-run leaves nothing staged. That is a valid outcome, not a
        # failure, but the tree must still be clean before the next run.
        print("    nothing to commit, artefacts byte-identical to the previous run")
        return

    message = (
        f"{experiment_id} {architecture} seed {seed}, run set {run_id}\n\n"
        f"Seed sweep run produced by scripts/run_seed_sweep.py.\n"
        f"Artefacts in experiments/*/seed{seed}/. Checkpoints are gitignored.\n"
    )
    subprocess.run(["git", "commit", "-q", "-m", message], check=True)

    head = git("rev-parse", "--short", "HEAD").stdout.strip()
    print(f"    committed {head}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--seeds", type=int, nargs="+", default=list(SEEDS),
        help=f"Seeds to run. Default {list(SEEDS)}.",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print what would run, change nothing.",
    )
    args = parser.parse_args()

    run_id = require_run_id()

    if not Path("src/training/train_e001_resnet18.py").exists():
        raise SystemExit("Run this from the repository root.")

    planned = [
        (seed, trainer) for seed in args.seeds for trainer in TRAINERS
    ]
    pending = [
        (seed, t) for seed, t in planned if not already_done(t[3], seed, run_id)
    ]

    print(f"Run set:  {run_id}")
    print(f"Seeds:    {args.seeds}")
    print(f"Runs:     {len(planned)} planned, {len(planned) - len(pending)} already "
          f"complete, {len(pending)} to run")

    if args.dry_run:
        for seed, (experiment_id, architecture, script, _) in pending:
            print(f"  would run {experiment_id} {architecture} at seed {seed}")
        return 0

    if not pending:
        print("Nothing to do.")
        return 0

    # ensure_clean_git() will reject the first run otherwise, and a dirty tree here
    # means uncommitted work that the sweep's own commits would silently absorb.
    if not working_tree_is_clean():
        raise SystemExit(
            "Working tree is not clean. Commit or stash before starting the sweep, "
            "otherwise unrelated changes are swept into the per-run commits:\n"
            + git("status", "--porcelain").stdout
        )

    started = time.monotonic()
    completed = 0

    for seed, (experiment_id, architecture, script, experiment_dir) in pending:
        label = f"{experiment_id} {architecture} seed {seed}"
        print(f"\n=== {label} "
              f"({completed + 1}/{len(pending)}) "
              f"{datetime.now().isoformat(timespec='seconds')} ===")

        run_started = time.monotonic()
        environment = dict(os.environ, RUN_ID=run_id)

        result = subprocess.run(
            [sys.executable, script, "--seed", str(seed)], env=environment
        )

        if result.returncode != 0:
            raise SystemExit(
                f"\n{label} failed with exit code {result.returncode}. The sweep is "
                "stopped so the failure is not buried under later runs. Fix it and "
                "re-run; completed runs will be skipped."
            )

        elapsed = timedelta(seconds=round(time.monotonic() - run_started))
        print(f"    trained in {elapsed}")

        commit_run(experiment_id, architecture, seed, run_id)

        if not working_tree_is_clean():
            raise SystemExit(
                f"Working tree still dirty after committing {label}. The next run "
                "would abort on ensure_clean_git(); stopping here instead.\n"
                + git("status", "--porcelain").stdout
            )

        completed += 1

    total = timedelta(seconds=round(time.monotonic() - started))
    print(f"\nSweep complete: {completed} runs in {total}, run set {run_id}")
    print("Per-seed tables can now be generated with, for example:")
    print("  SEED=43 python src/evaluation/generate_summary_tables.py")

    return 0


if __name__ == "__main__":
    sys.exit(main())
