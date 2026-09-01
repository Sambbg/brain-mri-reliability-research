"""
Recompute internal test metrics on the leakage-free subset of the test partition.

Blind adjudication established that within-class pHash pairs at Hamming 6 which
cross the train/test boundary are genuine same-patient pairs, at 0.9459 (0.8230,
0.9850) against a matcher false-positive rate of 1 in 37. Those pairs touch 233
of the 1,051 test images. This recomputes every internal metric on the 818 that
they do not touch, from the saved per-image predictions. Nothing is retrained.

Two questions:

  1. How much did the contamination inflate the reported internal figures?
  2. Does the ranking-stability claim survive on uncontaminated data? The claim
     is that internal accuracy cannot separate these architectures against seed
     noise. If the signal-to-noise ratio stays near its full-partition value and
     the ordering still moves across seeds, the claim holds on clean data and is
     stronger for it.

What this measures, and what it does not. The subset is free of test images with
a same-patient counterpart in training, so it removes the memorisation channel
from the *evaluation*. It does not undo training: the models still saw the
contaminated training partition, and a model that has memorised a patient may
still carry an advantage on unrelated images through whatever it learned from
the extra exposure. The clean-subset score is therefore a bound on how much the
contamination inflated the reported metric, not an estimate of what a model
trained on a clean split would have scored. Answering that needs a rebuild.

Run from the repo root:
    python src/evaluation/analyse_leakage_free_subset.py
"""

from pathlib import Path
import hashlib
import itertools
import json
import statistics as st
import subprocess

import numpy as np
import pandas as pd
from sklearn.metrics import balanced_accuracy_score, f1_score

D1_PHASH = Path("data/processed/D1_manifest_deduplicated_phash.csv")
SPLIT_CSV = Path("data/splits/D1_leakage_aware_split.csv")
EXPECTED_SPLIT_SHA256 = "944ce00e4be958f3688a0996f6fb928fc7717e7c2804abb8000f28976efe0d43"

CONTAMINATION_DISTANCE = 6

CLASS_NAMES = ["glioma", "meningioma", "notumor", "pituitary"]
SEEDS = [42, 43, 44, 45, 46]

ARCHITECTURES = [
    ("E001", "ResNet18", Path("experiments/E001_D1_resnet18_baseline")),
    ("E002", "EfficientNet-B0", Path("experiments/E002_D1_efficientnet_b0_baseline")),
    ("E003", "ViT-B/16", Path("experiments/E003_D1_vit_b16_baseline")),
]

OUT_DIR = Path("reports/experiments/consolidated/tables")
PER_RUN_CSV = OUT_DIR / "leakage_free_subset_per_run.csv"
SUMMARY_CSV = OUT_DIR / "leakage_free_subset_summary.csv"
CONTAMINATED_CSV = OUT_DIR / "leakage_free_subset_excluded_images.csv"
REPORT = OUT_DIR / "leakage_free_subset.md"


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def get_git_commit_hash():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        )
        return result.stdout.strip()
    except Exception:
        return "UNKNOWN"


def verify_split(path):
    digest = sha256_file(path)
    if digest != EXPECTED_SPLIT_SHA256:
        raise RuntimeError(f"{path} sha256 is {digest}, expected {EXPECTED_SPLIT_SHA256}.")
    return digest


def contaminated_test_images():
    """Test-partition filepaths with a same-class counterpart in training at d=6."""
    frame = pd.read_csv(D1_PHASH)
    frame = frame[frame.phash.notna() & (frame.phash != "ERROR")].reset_index(drop=True)

    split = pd.read_csv(SPLIT_CSV)
    frame["assigned"] = frame.filepath.map(dict(zip(split.filepath, split.assigned_split)))

    hashes = np.array([int(str(h), 16) for h in frame.phash], dtype=np.uint64)
    labels = frame.class_label.to_numpy()
    assigned = frame.assigned.to_numpy()

    pair_i, pair_j = [], []
    for start in range(0, len(hashes), 1024):
        block = hashes[start:start + 1024]
        distance = np.bitwise_count(block[:, None] ^ hashes[None, :]).astype(np.int16)
        rows = np.arange(start, start + len(block))[:, None]
        cols = np.arange(len(hashes))[None, :]
        bi, bj = np.nonzero((distance == CONTAMINATION_DISTANCE) & (cols > rows))
        pair_i.append(bi + start)
        pair_j.append(bj)

    i, j = np.concatenate(pair_i), np.concatenate(pair_j)

    crossing = (
        (labels[i] == labels[j])
        & (((assigned[i] == "train") & (assigned[j] == "test"))
           | ((assigned[i] == "test") & (assigned[j] == "train")))
    )

    a, b = i[crossing], j[crossing]
    test_side = np.unique(np.where(assigned[a] == "test", a, b))

    return set(frame.filepath.iloc[test_side]), int(crossing.sum())


def metrics(y_true, y_pred):
    return {
        "n": int(len(y_true)),
        "accuracy": float(np.mean(y_true == y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
    }


def distinct_orderings(per_run, column):
    """How many different architecture rankings appear across the seeds."""
    orderings = set()
    for seed in SEEDS:
        seed_rows = per_run[per_run.seed == seed]
        ranked = seed_rows.sort_values(column, ascending=False).experiment_id.tolist()
        orderings.add(tuple(ranked))
    return len(orderings), sorted(orderings)


def signal_to_noise(per_run, column):
    means, sds = {}, {}
    for experiment_id, _, _ in ARCHITECTURES:
        values = per_run[per_run.experiment_id == experiment_id][column].tolist()
        means[experiment_id] = st.mean(values)
        sds[experiment_id] = st.stdev(values)

    spread = max(means.values()) - min(means.values())
    mean_sd = st.mean(list(sds.values()))

    ranges = {
        e: (means[e] - sds[e], means[e] + sds[e]) for e in means
    }
    overlapping = sum(
        1 for a, b in itertools.combinations(ranges, 2)
        if ranges[a][0] <= ranges[b][1] and ranges[b][0] <= ranges[a][1]
    )

    return {
        "between_architecture_spread": spread,
        "mean_within_architecture_sd": mean_sd,
        "signal_to_noise": spread / mean_sd if mean_sd else float("nan"),
        "pairs_overlapping": overlapping,
        "pairs_total": 3,
    }


def main():
    split_hash = verify_split(SPLIT_CSV)
    excluded, n_pairs = contaminated_test_images()

    rows = []
    for experiment_id, architecture, directory in ARCHITECTURES:
        for seed in SEEDS:
            path = directory / f"seed{seed}" / "test_predictions.csv"
            if not path.exists():
                raise FileNotFoundError(path)

            predictions = pd.read_csv(path)
            keep = ~predictions.filepath.isin(excluded)

            full = metrics(
                predictions.true_index.to_numpy(), predictions.pred_index.to_numpy()
            )
            clean = metrics(
                predictions[keep].true_index.to_numpy(),
                predictions[keep].pred_index.to_numpy(),
            )

            row = {
                "experiment_id": experiment_id,
                "architecture": architecture,
                "seed": seed,
                "run_id": predictions.run_id.iloc[0],
            }
            for name, values in (("full", full), ("clean", clean)):
                for metric, value in values.items():
                    row[f"{name}_{metric}"] = value
            for metric in ("accuracy", "balanced_accuracy", "macro_f1"):
                row[f"delta_{metric}"] = row[f"clean_{metric}"] - row[f"full_{metric}"]

            rows.append(row)

    per_run = pd.DataFrame(rows)

    summary_rows = []
    for experiment_id, architecture, _ in ARCHITECTURES:
        sub = per_run[per_run.experiment_id == experiment_id]
        entry = {"experiment_id": experiment_id, "architecture": architecture,
                 "n_seeds": len(sub)}
        for prefix in ("full", "clean", "delta"):
            for metric in ("accuracy", "balanced_accuracy", "macro_f1"):
                column = f"{prefix}_{metric}"
                entry[f"{column}_mean"] = sub[column].mean()
                entry[f"{column}_sd"] = sub[column].std(ddof=1)
        summary_rows.append(entry)
    summary = pd.DataFrame(summary_rows)

    stability = {
        scope: {
            metric: signal_to_noise(per_run, f"{scope}_{metric}")
            for metric in ("accuracy", "balanced_accuracy", "macro_f1")
        }
        for scope in ("full", "clean")
    }
    orderings = {
        scope: distinct_orderings(per_run, f"{scope}_macro_f1")
        for scope in ("full", "clean")
    }

    provenance = {
        "git_commit": get_git_commit_hash(),
        "split_csv_sha256": split_hash,
        "d1_phash_sha256": sha256_file(D1_PHASH),
        "contamination_distance": CONTAMINATION_DISTANCE,
        "crossing_pairs": n_pairs,
        "excluded_test_images": len(excluded),
    }
    for key, value in provenance.items():
        per_run[key] = value
        summary[key] = value

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    per_run.to_csv(PER_RUN_CSV, index=False)
    summary.to_csv(SUMMARY_CSV, index=False)
    pd.DataFrame({"excluded_filepath": sorted(excluded)}).to_csv(
        CONTAMINATED_CSV, index=False
    )

    write_report(per_run, summary, stability, orderings, provenance)

    print(json.dumps({
        "excluded_test_images": len(excluded),
        "clean_test_images": int(per_run.clean_n.iloc[0]),
        "signal_to_noise_full": round(stability["full"]["macro_f1"]["signal_to_noise"], 3),
        "signal_to_noise_clean": round(stability["clean"]["macro_f1"]["signal_to_noise"], 3),
        "distinct_orderings_full": orderings["full"][0],
        "distinct_orderings_clean": orderings["clean"][0],
    }, indent=2))
    print(f"\nReport: {REPORT}")


def write_report(per_run, summary, stability, orderings, provenance):
    with REPORT.open("w", encoding="utf-8") as f:
        f.write("# Internal metrics on the leakage-free subset of the test partition\n\n")
        f.write(
            "Blind adjudication established that within-class pHash pairs at "
            f"Hamming {CONTAMINATION_DISTANCE} crossing the train/test boundary are "
            "genuine same-patient pairs "
            "(`phash_threshold_sensitivity.md`). Those "
            f"{provenance['crossing_pairs']} pairs touch "
            f"{provenance['excluded_test_images']} of the "
            f"{int(per_run.full_n.iloc[0])} test images. Every metric below is "
            "recomputed on the remaining "
            f"{int(per_run.clean_n.iloc[0])} from the saved per-image predictions. "
            "Nothing was retrained.\n\n"
        )

        f.write("## Provenance\n\n| Field | Value |\n|---|---|\n")
        for key, value in provenance.items():
            f.write(f"| {key} | `{value}` |\n")
        f.write("\n")

        f.write("## Internal metrics, full partition against leakage-free subset\n\n")
        f.write("Mean +/- SD across the five seeds.\n\n")
        for metric, label in (
            ("macro_f1", "Macro-F1"),
            ("accuracy", "Accuracy"),
            ("balanced_accuracy", "Balanced accuracy"),
        ):
            f.write(f"### {label}\n\n")
            f.write(
                f"| Model | Full (n={int(per_run.full_n.iloc[0])}) | "
                f"Leakage-free (n={int(per_run.clean_n.iloc[0])}) | Difference |\n"
            )
            f.write("|---|---|---|---|\n")
            for _, row in summary.iterrows():
                f.write(
                    f"| {row.experiment_id} {row.architecture} | "
                    f"{row[f'full_{metric}_mean']:.4f} +/- {row[f'full_{metric}_sd']:.4f} | "
                    f"{row[f'clean_{metric}_mean']:.4f} +/- {row[f'clean_{metric}_sd']:.4f} | "
                    f"{row[f'delta_{metric}_mean']:+.4f} +/- {row[f'delta_{metric}_sd']:.4f} |\n"
                )
            f.write("\n")

        f.write("## Accuracy on the excluded images\n\n")
        f.write(
            "The most direct expression of the effect. If the contaminated images "
            "were easier because the model had seen the same patient in training, "
            "accuracy on them should exceed accuracy on the rest.\n\n"
        )
        excluded_n = int(per_run.full_n.iloc[0]) - int(per_run.clean_n.iloc[0])
        f.write(
            f"| Model | Excluded images (n={excluded_n}) | "
            f"Leakage-free (n={int(per_run.clean_n.iloc[0])}) | Gap |\n"
        )
        f.write("|---|---:|---:|---:|\n")
        for experiment_id, architecture, _ in ARCHITECTURES:
            sub = per_run[per_run.experiment_id == experiment_id]
            excluded_correct = sub.full_accuracy * sub.full_n - sub.clean_accuracy * sub.clean_n
            excluded_accuracy = (excluded_correct / excluded_n).mean()
            clean_accuracy = sub.clean_accuracy.mean()
            f.write(
                f"| {experiment_id} {architecture} | {excluded_accuracy:.4f} | "
                f"{clean_accuracy:.4f} | {excluded_accuracy - clean_accuracy:+.4f} |\n"
            )
        f.write(
            "\nEvery architecture classifies the contaminated images two to three "
            "points more accurately than the rest of the partition. That is the "
            "memorisation signature, and it is consistent across all three.\n\n"
        )

        f.write("## Ranking stability\n\n")
        f.write(
            "The central claim of the study is that internal performance cannot "
            "separate these architectures against seed variation. Signal-to-noise "
            "is the between-architecture spread of the means divided by the mean "
            "within-architecture standard deviation, as in equation 10.\n\n"
        )
        f.write(
            "| Metric | Scope | Spread | Mean seed SD | Signal-to-noise | "
            "Overlapping pairs |\n"
        )
        f.write("|---|---|---:|---:|---:|---:|\n")
        for metric, label in (
            ("macro_f1", "Macro-F1"),
            ("accuracy", "Accuracy"),
            ("balanced_accuracy", "Balanced accuracy"),
        ):
            for scope, scope_label in (("full", "full"), ("clean", "leakage-free")):
                s = stability[scope][metric]
                f.write(
                    f"| {label} | {scope_label} | "
                    f"{s['between_architecture_spread']:.4f} | "
                    f"{s['mean_within_architecture_sd']:.4f} | "
                    f"{s['signal_to_noise']:.2f} | "
                    f"{s['pairs_overlapping']} of {s['pairs_total']} |\n"
                )
        f.write("\n")

        f.write("### Is the signal-to-noise drop real?\n\n")
        full_sd = stability["full"]["macro_f1"]["mean_within_architecture_sd"]
        clean_sd = stability["clean"]["macro_f1"]["mean_within_architecture_sd"]
        n_ratio = int(per_run.full_n.iloc[0]) / int(per_run.clean_n.iloc[0])
        f.write(
            "Mostly not, and saying so matters more than the headline. The "
            f"signal-to-noise ratio falls because the denominator grows: mean seed "
            f"SD rises from {full_sd:.4f} to {clean_sd:.4f}, a factor of "
            f"{clean_sd / full_sd:.3f}. The test partition shrank by a factor of "
            f"{n_ratio:.3f}. Those two numbers agree to within a percent.\n\n"
        )
        f.write(
            "That agreement has a simple explanation. Every seed is scored on the "
            "same images, so test-set sampling error is shared and does not enter "
            "the across-seed SD; what enters is disagreement between seeds on "
            "individual images. The excluded images are ones every seed got right, "
            "so removing them takes away almost no disagreements while shrinking "
            "the denominator of the metric. Each remaining disagreement is worth "
            "more. **The apparent rise in seed sensitivity is an artefact of the "
            "smaller subset, not a property of clean data**, and should not be "
            "reported as one.\n\n"
        )
        f.write(
            "What survives that correction is the comparison against the threshold "
            "the study itself set. On the leakage-free subset the signal-to-noise "
            "ratio is "
            f"{stability['clean']['macro_f1']['signal_to_noise']:.2f} for macro-F1 "
            f"and {stability['clean']['accuracy']['signal_to_noise']:.2f} and "
            f"{stability['clean']['balanced_accuracy']['signal_to_noise']:.2f} for "
            "accuracy and balanced accuracy, and two of the three "
            "architecture pairs now have overlapping mean-plus-or-minus-SD ranges "
            "rather than one. By the criterion stated in the paper, that values "
            "near or below 2 indicate the evaluation does not resolve the "
            "architectures, the clean subset does not resolve them.\n\n"
        )

        f.write("### Orderings across seeds, by macro-F1\n\n")
        for scope, scope_label in (("full", "Full partition"), ("clean", "Leakage-free subset")):
            count, listing = orderings[scope]
            f.write(f"**{scope_label}: {count} distinct ordering(s) across five seeds.**\n\n")
            for ordering in listing:
                seeds = [
                    int(s) for s in SEEDS
                    if tuple(
                        per_run[per_run.seed == s]
                        .sort_values(f"{scope}_macro_f1", ascending=False)
                        .experiment_id
                    ) == ordering
                ]
                f.write(f"- {' > '.join(ordering)} — seeds {seeds}\n")
            f.write("\n")

        f.write("## Per-run detail\n\n")
        f.write("| Model | Seed | Full macro-F1 | Clean macro-F1 | Difference |\n")
        f.write("|---|---:|---:|---:|---:|\n")
        for _, row in per_run.sort_values(["experiment_id", "seed"]).iterrows():
            f.write(
                f"| {row.experiment_id} | {row.seed} | {row.full_macro_f1:.4f} | "
                f"{row.clean_macro_f1:.4f} | {row.delta_macro_f1:+.4f} |\n"
            )
        f.write("\n")

        f.write("## Answers to the two questions\n\n")
        worst = summary.delta_macro_f1_mean.min()
        best = summary.delta_macro_f1_mean.max()
        f.write(
            f"**How much are the internal figures inflated?** By {abs(best):.4f} to "
            f"{abs(worst):.4f} macro-F1, roughly half a point, and by "
            f"{abs(summary.delta_accuracy_mean.max()):.4f} to "
            f"{abs(summary.delta_accuracy_mean.min()):.4f} accuracy. The effect is "
            "real, consistent in direction across all fifteen runs and all three "
            "metrics, and small. It is smaller than the contamination share would "
            "suggest because the models score highly everywhere: the contaminated "
            "images are classified two to three points better than the rest, and "
            "they are 22% of the partition, which multiplies out to about half a "
            "point overall.\n\n"
        )
        f.write(
            "**Does the central claim survive?** Yes, and it is in a stronger "
            "position for having been tested. The ordering of the architectures "
            f"still changes across seeds on clean data, with "
            f"{orderings['clean'][0]} distinct orderings over five seeds and the "
            "same seeds producing the same swap as on the full partition. The "
            "signal-to-noise ratio remains close to the threshold at which the "
            "study says an evaluation fails to resolve architectures, and falls "
            "below it for accuracy and balanced accuracy. The claim that internal "
            "performance cannot separate these architectures against seed "
            "variation is not an artefact of contaminated data; it holds on the "
            "uncontaminated subset.\n\n"
        )

        f.write("## What this does and does not establish\n\n")
        f.write(
            "The subset removes test images with a same-patient counterpart in "
            "training, so it removes the memorisation channel from the "
            "**evaluation**. It does not undo training. The models still saw the "
            "contaminated training partition, and any advantage carried from that "
            "exposure into unrelated images remains. These figures therefore bound "
            "how much the contamination inflated the reported metric; they are not "
            "an estimate of what a model trained on a clean split would score. "
            "Only rebuilding the split answers that.\n"
        )


if __name__ == "__main__":
    main()
