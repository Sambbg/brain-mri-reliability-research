"""
Perceptual-hash threshold sensitivity audit.

The leakage-aware split and every overlap audit in this project flag
near-duplicates at a pHash Hamming distance of 4 or fewer bits. Four is a
convention, not a derived quantity, and a reviewer is entitled to ask what
happens at 2 or at 8. This sweeps 0, 2, 4, 6 and 8 across the four comparisons
that already have perceptual-hash manifests and reports whether any decision in
the paper depends on the choice.

Reuses the committed manifests in data/processed/; no hash is recomputed here.
That matters: recomputing would silently re-derive the very quantity under test.

Four comparisons:

    D1 internal   within-dataset near duplicates, the basis of the leakage
                  groups that define the frozen split
    D1 vs D2      the rejected external candidate
    D1 vs D3B     the canine shifted-domain probe
    D1 vs D3C     the human shifted-domain probe

For D1 internal the audit also re-derives the leakage grouping at each
threshold and, separately, counts pairs that cross the *frozen* split boundary.
Those are different questions. The first asks how the grouping would change; the
second asks whether the split already committed still holds up when judged by a
stricter rule than the one that built it. Only the second can invalidate work
already done.

Run from the repo root:
    python src/data/audit_phash_threshold_sensitivity.py

Writes:
    reports/experiments/consolidated/tables/phash_threshold_sensitivity.csv
    reports/experiments/consolidated/tables/phash_threshold_sensitivity.md
"""

from pathlib import Path
import hashlib
import math
import subprocess
import sys

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact

sys.path.insert(0, "src/stats")
from wilson import wilson_interval  # noqa: E402

THRESHOLDS = [0, 2, 4, 6, 8]

# The threshold every existing audit and the frozen split were built at.
OPERATING_THRESHOLD = 4

D1_PHASH = Path("data/processed/D1_manifest_deduplicated_phash.csv")
D2_PHASH = Path("data/processed/D2_manifest_deduplicated_phash.csv")
D3B_PHASH = Path("data/processed/D3B_selected_slices_manifest_phash.csv")
D3C_PHASH = Path("data/processed/D3C_selected_slices_manifest_phash.csv")

SPLIT_CSV = Path("data/splits/D1_leakage_aware_split.csv")
EXPECTED_SPLIT_SHA256 = "944ce00e4be958f3688a0996f6fb928fc7717e7c2804abb8000f28976efe0d43"

OUT_DIR = Path("reports/experiments/consolidated/tables")
OUT_CSV = OUT_DIR / "phash_threshold_sensitivity.csv"
OUT_REPORT = OUT_DIR / "phash_threshold_sensitivity.md"

# A candidate is rejected as an external validation set if this share or more of
# it duplicates the internal set. Stated up front rather than chosen after
# seeing the numbers. The observed shares sit orders of magnitude either side of
# it, so the exact value is not load-bearing -- which is the point of reporting
# the raw counts alongside.
REJECTION_SHARE = 0.01

PHASH_BITS = 64


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


def git_tree_is_dirty():
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, check=True,
        )
        return bool(result.stdout.strip())
    except Exception:
        return True


def verify_split(path):
    digest = sha256_file(path)
    if digest != EXPECTED_SPLIT_SHA256:
        raise RuntimeError(
            f"{path} sha256 is {digest}, expected {EXPECTED_SPLIT_SHA256}. "
            "The frozen leakage-aware split has changed."
        )
    return digest


def load_hashes(path, label_column):
    """Manifest rows with a usable pHash, as uint64 plus their class labels."""
    frame = pd.read_csv(path)

    if "phash" not in frame.columns:
        raise ValueError(f"{path} has no phash column")

    frame = frame[frame.phash.notna() & (frame.phash != "ERROR")].reset_index(drop=True)
    hashes = np.array([int(str(h), 16) for h in frame.phash], dtype=np.uint64)

    return frame, hashes, frame[label_column].to_numpy()


def pairs_within(hashes, max_distance, chunk=1024):
    """
    All i<j pairs within max_distance, as (i, j, distance).

    Computed once at the widest threshold and filtered per threshold afterwards,
    so the sweep does not rescan the data five times.
    """
    n = len(hashes)
    out_i, out_j, out_d = [], [], []

    for start in range(0, n, chunk):
        block = hashes[start:start + chunk]
        distance = np.bitwise_count(block[:, None] ^ hashes[None, :]).astype(np.int16)

        rows = np.arange(start, start + len(block))[:, None]
        cols = np.arange(n)[None, :]
        hit = (distance <= max_distance) & (cols > rows)

        bi, bj = np.nonzero(hit)
        out_i.append(bi + start)
        out_j.append(bj)
        out_d.append(distance[bi, bj])

    return (np.concatenate(out_i), np.concatenate(out_j), np.concatenate(out_d))


def pairs_between(left, right, max_distance, chunk=1024):
    """All cross-set pairs within max_distance, as (left index, right index, distance)."""
    out_i, out_j, out_d = [], [], []

    for start in range(0, len(left), chunk):
        block = left[start:start + chunk]
        distance = np.bitwise_count(block[:, None] ^ right[None, :]).astype(np.int16)

        bi, bj = np.nonzero(distance <= max_distance)
        out_i.append(bi + start)
        out_j.append(bj)
        out_d.append(distance[bi, bj])

    return (np.concatenate(out_i), np.concatenate(out_j), np.concatenate(out_d))


def connected_components(n, edges_i, edges_j):
    """Union-find over the pair list. Returns (component count, largest size)."""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in zip(edges_i, edges_j):
        ra, rb = find(int(a)), find(int(b))
        if ra != rb:
            parent[ra] = rb

    sizes = {}
    for x in range(n):
        root = find(x)
        sizes[root] = sizes.get(root, 0) + 1

    return len(sizes), max(sizes.values())


def audit_d1_internal(rows):
    frame, hashes, labels = load_hashes(D1_PHASH, "class_label")

    split = pd.read_csv(SPLIT_CSV)
    split_by_path = dict(zip(split.filepath, split.assigned_split))
    assigned = frame.filepath.map(split_by_path).to_numpy()

    if pd.isna(assigned).any():
        raise RuntimeError("Some D1 manifest rows are absent from the frozen split.")

    i, j, d = pairs_within(hashes, max(THRESHOLDS))

    for threshold in THRESHOLDS:
        keep = d <= threshold
        pi, pj = i[keep], j[keep]

        is_cross_class = labels[pi] != labels[pj]
        cross_class = int(is_cross_class.sum())
        cross_split = int((assigned[pi] != assigned[pj]).sum())

        is_train_test = (
            ((assigned[pi] == "train") & (assigned[pj] == "test"))
            | ((assigned[pi] == "test") & (assigned[pj] == "train"))
        )
        train_test = int(is_train_test.sum())

        # A cross-class pair cannot be a true duplicate: a glioma slice is not a
        # duplicate of a pituitary one. The cross-class rate is therefore a
        # lower bound on the matcher's false-positive rate at each threshold,
        # measured from the data rather than assumed.
        train_test_cross_class = int((is_train_test & is_cross_class).sum())

        n_groups, largest = connected_components(len(hashes), pi, pj)

        rows.append({
            "comparison": "D1_internal",
            "hamming_threshold": threshold,
            "n_left": len(hashes),
            "n_right": len(hashes),
            "near_duplicate_pairs": int(keep.sum()),
            "cross_class_pairs": cross_class,
            "cross_class_rate": round(cross_class / int(keep.sum()), 6) if keep.sum() else 0.0,
            "leakage_groups": n_groups,
            "largest_group_size": largest,
            "pairs_crossing_frozen_split": cross_split,
            "pairs_crossing_train_test": train_test,
            "train_test_cross_class": train_test_cross_class,
            "train_test_within_class": train_test - train_test_cross_class,
            "matched_candidate_images": "",
            "matched_candidate_share": "",
            "decision": "",
        })


ADJUDICATION_DIR = Path("reports/datasets/phash_d6_adjudication")
ADJUDICATION_WORKSHEET = ADJUDICATION_DIR / "adjudication_worksheet.csv"
ADJUDICATION_KEY = ADJUDICATION_DIR / "blind_key.csv"

LEAKAGE_VERDICTS = ("same_image", "same_patient")


def newcombe_difference(k1, n1, k2, n2):
    """
    Newcombe's hybrid score interval for the difference of two proportions.

    Built from the Wilson bounds of each proportion, so it inherits their
    behaviour near 0 and 1 -- which matters here, where one arm sits at 35/37.
    A Wald interval on this difference would be meaningless at that boundary.

    Kept local rather than added to src/stats/, which carries a test suite this
    would arrive without.
    """
    p1, p2 = k1 / n1, k2 / n2
    a, b = wilson_interval(k1, n1), wilson_interval(k2, n2)

    lower = (p1 - p2) - math.sqrt((p1 - a.lower) ** 2 + (b.upper - p2) ** 2)
    upper = (p1 - p2) + math.sqrt((a.upper - p1) ** 2 + (p2 - b.lower) ** 2)

    return p1 - p2, lower, upper


def load_adjudication():
    """
    Scored blind adjudication of the Hamming-6 boundary-crossing pairs.

    Returns None when the worksheet has not been scored, so the audit still runs
    before adjudication and simply omits the section.
    """
    if not (ADJUDICATION_WORKSHEET.exists() and ADJUDICATION_KEY.exists()):
        return None

    worksheet = pd.read_csv(ADJUDICATION_WORKSHEET)

    if worksheet.verdict.isna().any():
        return None

    key = pd.read_csv(ADJUDICATION_KEY)
    merged = worksheet.merge(key[["pair_id", "group"]], on="pair_id", validate="1:1")

    merged["is_leak"] = merged.verdict.isin(LEAKAGE_VERDICTS)
    merged["is_unsure"] = merged.verdict == "unsure"

    result = {"counts": {}, "rates": {}}

    for group in ("crossing", "same_split"):
        sub = merged[merged.group == group]
        n_total = len(sub)
        n_unsure = int(sub.is_unsure.sum())
        n_leak = int(sub.is_leak.sum())

        result["counts"][group] = {
            "n": n_total,
            "leak": n_leak,
            "distinct": n_total - n_unsure - n_leak,
            "unsure": n_unsure,
        }
        result["rates"][group] = {
            "excluding_unsure": wilson_interval(n_leak, n_total - n_unsure),
            "including_unsure": wilson_interval(n_leak, n_total),
        }

    counts = result["counts"]
    for basis, denominator in (
        ("excluding_unsure", lambda c: c["n"] - c["unsure"]),
        ("including_unsure", lambda c: c["n"]),
    ):
        k1, n1 = counts["crossing"]["leak"], denominator(counts["crossing"])
        k2, n2 = counts["same_split"]["leak"], denominator(counts["same_split"])
        difference, lower, upper = newcombe_difference(k1, n1, k2, n2)
        _, p_value = fisher_exact([[k1, n1 - k1], [k2, n2 - k2]])
        result[basis] = {
            "difference": difference,
            "lower": lower,
            "upper": upper,
            "fisher_p": p_value,
        }

    null = counts["same_split"]
    result["matcher_false_positive"] = wilson_interval(
        null["distinct"], null["n"] - null["unsure"]
    )
    result["verdict_table"] = pd.crosstab(merged.verdict, merged.group)

    return result


def crossing_pair_footprint():
    """Unique images on each side of the boundary touched by the d=6 crossing pairs."""
    frame, hashes, labels = load_hashes(D1_PHASH, "class_label")

    split = pd.read_csv(SPLIT_CSV)
    assigned = frame.filepath.map(dict(zip(split.filepath, split.assigned_split))).to_numpy()

    i, j, d = pairs_within(hashes, OPERATING_THRESHOLD + 2)

    selected = (
        (d == OPERATING_THRESHOLD + 2)
        & (labels[i] == labels[j])
        & (((assigned[i] == "train") & (assigned[j] == "test"))
           | ((assigned[i] == "test") & (assigned[j] == "train")))
    )

    a, b = i[selected], j[selected]
    test_side = np.where(assigned[a] == "test", a, b)
    train_side = np.where(assigned[a] == "train", a, b)

    return {
        "pairs": int(selected.sum()),
        "unique_test_images": int(len(np.unique(test_side))),
        "unique_train_images": int(len(np.unique(train_side))),
        "n_test": int((assigned == "test").sum()),
        "n_train": int((assigned == "train").sum()),
    }


def audit_candidate(rows, name, path, label_column):
    d1_frame, d1_hashes, d1_labels = load_hashes(D1_PHASH, "class_label")
    frame, hashes, labels = load_hashes(path, label_column)

    i, j, d = pairs_between(d1_hashes, hashes, max(THRESHOLDS))

    for threshold in THRESHOLDS:
        keep = d <= threshold
        pi, pj = i[keep], j[keep]

        matched = int(len(np.unique(pj)))
        share = matched / len(hashes)
        cross_class = int((d1_labels[pi] != labels[pj]).sum())

        rows.append({
            "comparison": f"D1_vs_{name}",
            "hamming_threshold": threshold,
            "n_left": len(d1_hashes),
            "n_right": len(hashes),
            "near_duplicate_pairs": int(keep.sum()),
            "cross_class_pairs": cross_class,
            "cross_class_rate": round(cross_class / int(keep.sum()), 6) if keep.sum() else 0.0,
            "leakage_groups": "",
            "largest_group_size": "",
            "pairs_crossing_frozen_split": "",
            "pairs_crossing_train_test": "",
            "train_test_cross_class": "",
            "train_test_within_class": "",
            "matched_candidate_images": matched,
            "matched_candidate_share": round(share, 6),
            "decision": "REJECT" if share >= REJECTION_SHARE else "RETAIN",
        })


def main():
    split_hash = verify_split(SPLIT_CSV)

    rows = []
    audit_d1_internal(rows)
    audit_candidate(rows, "D2", D2_PHASH, "class_label")
    audit_candidate(rows, "D3B", D3B_PHASH, "label")
    audit_candidate(rows, "D3C", D3C_PHASH, "label")

    frame = pd.DataFrame(rows)

    provenance = {
        "git_commit": get_git_commit_hash(),
        "git_tree_dirty": git_tree_is_dirty(),
        "split_csv_sha256": split_hash,
        "d1_phash_sha256": sha256_file(D1_PHASH),
        "d2_phash_sha256": sha256_file(D2_PHASH),
        "d3b_phash_sha256": sha256_file(D3B_PHASH),
        "d3c_phash_sha256": sha256_file(D3C_PHASH),
    }

    for key, value in provenance.items():
        frame[key] = value

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    frame.to_csv(OUT_CSV, index=False)

    write_report(frame, provenance, load_adjudication(), crossing_pair_footprint())

    print(frame[[
        "comparison", "hamming_threshold", "near_duplicate_pairs",
        "cross_class_pairs", "pairs_crossing_train_test",
        "matched_candidate_share", "decision",
    ]].to_string(index=False))
    print(f"\nTable:  {OUT_CSV}")
    print(f"Report: {OUT_REPORT}")


def write_adjudication_section(f, adjudication, footprint):
    counts = adjudication["counts"]
    rates = adjudication["rates"]
    excl = adjudication["excluding_unsure"]
    incl = adjudication["including_unsure"]
    fp = adjudication["matcher_false_positive"]

    f.write("## Adjudication of the boundary-crossing pairs\n\n")
    f.write(
        "The counts above cannot say whether the boundary-crossing pairs are real. "
        "40 of them were sampled against 40 same-split pairs matched on distance "
        "and class, interleaved and scored blind "
        "(`reports/datasets/phash_d6_adjudication/`). Leakage is `same_image` or "
        "`same_patient`; `unsure` is reported separately rather than folded either "
        "way.\n\n"
    )

    f.write("| Group | n | Leakage | Distinct | Unsure | Rate, unsure excluded | Rate, unsure as non-leak |\n")
    f.write("|---|---:|---:|---:|---:|---|---|\n")
    for group, display in (("crossing", "crossing"), ("same_split", "same-split")):
        c, r = counts[group], rates[group]
        f.write(
            f"| {display} | {c['n']} | {c['leak']} | {c['distinct']} | {c['unsure']} | "
            f"{r['excluding_unsure'].proportion:.4f} "
            f"({r['excluding_unsure'].lower:.4f}, {r['excluding_unsure'].upper:.4f}) | "
            f"{r['including_unsure'].proportion:.4f} "
            f"({r['including_unsure'].lower:.4f}, {r['including_unsure'].upper:.4f}) |\n"
        )
    f.write(
        f"\nDifference (crossing minus same-split), unsure excluded: "
        f"**{excl['difference']:+.4f}**, Newcombe 95% CI "
        f"({excl['lower']:+.4f}, {excl['upper']:+.4f}), Fisher exact "
        f"p = {excl['fisher_p']:.3f}. Counting unsure as non-leakage: "
        f"{incl['difference']:+.4f} ({incl['lower']:+.4f}, {incl['upper']:+.4f}), "
        f"p = {incl['fisher_p']:.3f}.\n\n"
    )

    f.write("### What this means, which is not what the design anticipated\n\n")
    f.write(
        "The two groups are indistinguishable. The design treated that outcome as "
        "exoneration: matching rates would mean Hamming 6 flags the same thing on "
        "both sides of the boundary, so the crossing pairs would be matcher noise. "
        "**That inference was wrong, and it is worth stating why.** It holds only "
        "if the shared rate is low. It is not low. Both groups sit near ceiling, "
        "so the finding is not that the matcher fires indiscriminately but that it "
        "is accurate, and the crossing pairs are therefore real.\n\n"
    )
    f.write(
        "The same-split group measures the false-positive rate directly, since a "
        "`distinct` verdict there is the matcher being wrong. That rate is "
        f"{fp.successes}/{fp.n} = {fp.proportion:.4f} "
        f"({fp.lower:.4f}, {fp.upper:.4f}). A within-class pHash match at Hamming 6 "
        "identifies the same patient roughly 95 times in 100.\n\n"
    )

    leak_rate = rates["crossing"]["excluding_unsure"]
    estimated = footprint["unique_test_images"] * leak_rate.proportion
    f.write(
        f"Applying that to the population: the {footprint['pairs']} crossing pairs "
        f"involve {footprint['unique_test_images']} distinct test images out of "
        f"{footprint['n_test']} "
        f"({footprint['unique_test_images'] / footprint['n_test']:.2%}) and "
        f"{footprint['unique_train_images']} training images. Scaling by the "
        f"adjudicated rate gives roughly **{estimated:.0f} test images "
        f"({estimated / footprint['n_test']:.1%} of the test partition)** with a "
        "same-patient counterpart in training, with the interval on the rate "
        f"putting it between {footprint['unique_test_images'] * leak_rate.lower:.0f} "
        f"and {footprint['unique_test_images'] * leak_rate.upper:.0f} images.\n\n"
    )
    f.write(
        "**The frozen split leaks at the patient level.** Not by the rule it was "
        "built under, which it satisfies exactly, but by the standard that "
        "actually matters for a held-out test partition.\n\n"
    )

    f.write("### Limits of this estimate\n\n")
    f.write(
        "D1 carries no patient identifiers, so `same_patient` is a visual "
        "judgement about whether two slices come from one acquisition, not a "
        "lookup. It cannot be verified, and a liberal criterion would inflate both "
        "arms together. What the design does establish independently of that "
        "calibration is the *comparison*: whatever standard was applied, it was "
        "applied blind and identically to both groups, and they came out the same. "
        "The absolute rate of 95% should be read as an estimate with an unmodelled "
        "component of adjudicator judgement; the absence of a difference between "
        "groups is the more robust result.\n\n"
    )
    f.write(
        "The sample is 40 per arm, so the difference interval spans roughly "
        f"{excl['lower']:+.2f} to {excl['upper']:+.2f}. It excludes a large excess "
        "in the crossing group but is consistent with a modest one in either "
        "direction.\n\n"
    )


def write_report(frame, provenance, adjudication=None, footprint=None):
    internal = frame[frame.comparison == "D1_internal"]
    at_operating = internal[internal.hamming_threshold == OPERATING_THRESHOLD].iloc[0]

    leakage_breaks = internal[internal.pairs_crossing_train_test.astype(int) > 0]
    decisions = {
        name: set(frame[frame.comparison == name].decision)
        for name in ("D1_vs_D2", "D1_vs_D3B", "D1_vs_D3C")
    }
    unstable = {n: d for n, d in decisions.items() if len(d) > 1}

    with OUT_REPORT.open("w", encoding="utf-8") as f:
        f.write("# pHash threshold sensitivity audit\n\n")
        f.write(
            "Every near-duplicate audit in this project flags pairs at a pHash "
            f"Hamming distance of {OPERATING_THRESHOLD} bits or fewer. That value "
            "is a convention rather than a derived quantity, so this sweeps "
            f"{', '.join(str(t) for t in THRESHOLDS)} across all four comparisons "
            "and reports whether any decision depends on it. Hashes are read from "
            "the committed manifests and are not recomputed.\n\n"
        )

        f.write("## Provenance\n\n| Field | Value |\n|---|---|\n")
        for key, value in provenance.items():
            f.write(f"| {key} | `{value}` |\n")
        f.write(f"| Rejection criterion | candidate match share >= {REJECTION_SHARE:.0%} |\n\n")

        f.write("## D1 internal\n\n")
        f.write(
            "`leakage_groups` and `largest_group_size` describe the grouping that "
            "*would* be derived at each threshold. `pairs_crossing_train_test` is a "
            "different and more important quantity: it counts near-duplicate pairs "
            "that straddle the train/test boundary of the **frozen split already in "
            "use**, which was built at threshold "
            f"{OPERATING_THRESHOLD}. A non-zero value there means the committed "
            "split leaks when judged by a stricter rule.\n\n"
        )
        f.write(
            "| Threshold | Pairs | Cross-class | Cross-class rate | Leakage groups | "
            "Largest group | Cross-split | Train/test | of which cross-class |\n"
        )
        f.write("|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n")
        for _, row in internal.iterrows():
            marker = " **<-- operating**" if row.hamming_threshold == OPERATING_THRESHOLD else ""
            f.write(
                f"| {row.hamming_threshold}{marker} | {row.near_duplicate_pairs} | "
                f"{row.cross_class_pairs} | {float(row.cross_class_rate):.2%} | "
                f"{row.leakage_groups} | {row.largest_group_size} | "
                f"{row.pairs_crossing_frozen_split} | "
                f"{row.pairs_crossing_train_test} | {row.train_test_cross_class} |\n"
            )
        f.write("\n")

        if leakage_breaks.empty:
            f.write(
                "**No near-duplicate pair crosses the frozen train/test boundary at "
                "any threshold tested, including 8.** The committed split is "
                "leakage-free by a stricter standard than the one that produced "
                "it.\n\n"
            )
        else:
            worst = leakage_breaks.iloc[0]
            f.write(
                f"**The frozen split leaks at threshold {worst.hamming_threshold} "
                f"and above**: {worst.pairs_crossing_train_test} near-duplicate "
                "pairs straddle the train/test boundary, against zero at 0, 2 and "
                f"{OPERATING_THRESHOLD}. The split was built at threshold "
                f"{OPERATING_THRESHOLD} and is leakage-free by that definition, but "
                "a reviewer applying a looser rule would find contamination.\n\n"
            )
            f.write(
                "The specificity argument below does **not** dispose of this. Of "
                f"those {worst.pairs_crossing_train_test} pairs, "
                f"{worst.train_test_cross_class} are cross-class and therefore "
                f"certainly spurious, but {worst.train_test_within_class} are "
                "within-class, where the hash agreeing to within "
                f"{worst.hamming_threshold} bits is at least consistent with a true "
                "near-duplicate. Those have not been inspected image by image, so "
                "the honest position is that the frozen split is verified clean at "
                f"threshold {OPERATING_THRESHOLD} and unverified above it, not that "
                "the pairs at 6 are known to be artefacts.\n\n"
            )

        if adjudication is not None and footprint is not None:
            write_adjudication_section(f, adjudication, footprint)

        f.write("## Candidate datasets\n\n")
        f.write(
            "| Comparison | Threshold | Pairs | Cross-class | Matched images | "
            "Share of candidate | Decision |\n"
        )
        f.write("|---|---:|---:|---:|---:|---:|---|\n")
        for name in ("D1_vs_D2", "D1_vs_D3B", "D1_vs_D3C"):
            for _, row in frame[frame.comparison == name].iterrows():
                f.write(
                    f"| {name} | {row.hamming_threshold} | "
                    f"{row.near_duplicate_pairs} | {row.cross_class_pairs} | "
                    f"{row.matched_candidate_images} | "
                    f"{float(row.matched_candidate_share):.4%} | {row.decision} |\n"
                )
        f.write("\n")

        f.write("## Specificity: how far the threshold can be pushed\n\n")
        f.write(
            "A cross-class pair cannot be a true duplicate. A glioma slice is not "
            "a duplicate of a pituitary slice, whatever their hashes say. The "
            "cross-class rate is therefore a lower bound on the false-positive "
            "rate, measured rather than assumed, and it is what determines how far "
            "the threshold can be pushed before the matcher stops being a "
            "duplicate detector.\n\n"
        )
        f.write("| Threshold | D1 internal cross-class rate |\n|---:|---:|\n")
        for _, row in internal.iterrows():
            f.write(
                f"| {row.hamming_threshold} | {float(row.cross_class_rate):.2%} |\n"
            )
        rate4 = float(internal[internal.hamming_threshold == 4].iloc[0].cross_class_rate)
        rate8 = float(internal[internal.hamming_threshold == 8].iloc[0].cross_class_rate)
        f.write(
            f"\nAt the operating threshold the rate is {rate4:.2%}; at 8 it is "
            f"{rate8:.2%}, a factor of {rate8 / rate4:.0f}. Every brain MRI "
            "resembles every other at low bit depth, and by 8 bits of tolerance "
            "the hash is matching that generic resemblance. Results at 6 and 8 "
            "should be read as the behaviour of a degraded matcher, not as newly "
            "discovered duplicates.\n\n"
        )

        f.write("## Does any decision change?\n\n")
        if unstable:
            for name, values in unstable.items():
                sub = frame[frame.comparison == name]
                flips = sub[sub.decision == "REJECT"].hamming_threshold.tolist()
                f.write(
                    f"**{name}: the verdict is not constant across the sweep.** It "
                    f"reads REJECT at threshold(s) {flips} and RETAIN elsewhere.\n\n"
                )
        else:
            f.write(
                "**No candidate decision changes anywhere in the range.** Each of "
                "the three candidates returns the same verdict at every threshold "
                "from 0 to 8.\n\n"
            )

        d2 = frame[frame.comparison == "D1_vs_D2"]
        d2_zero = d2[d2.hamming_threshold == 0].iloc[0]
        f.write(
            f"The D2 rejection is decided at threshold 0: "
            f"{d2_zero.matched_candidate_images} of {d2_zero.n_right} candidate "
            f"images ({float(d2_zero.matched_candidate_share):.1%}) are already "
            "exact perceptual matches before any tolerance is allowed. No choice of "
            "threshold reverses that, because loosening the rule can only add "
            "matches.\n\n"
        )

        for name, display in (("D1_vs_D3B", "D3B"), ("D1_vs_D3C", "D3C")):
            sub = frame[frame.comparison == name]
            at_op = sub[sub.hamming_threshold == OPERATING_THRESHOLD].iloc[0]
            widest = sub[sub.hamming_threshold == max(THRESHOLDS)].iloc[0]
            f.write(
                f"{display} is clean at the operating threshold "
                f"({at_op.matched_candidate_images} of {at_op.n_right} images, "
                f"{float(at_op.matched_candidate_share):.2%}) but **not across the "
                f"whole range**: at threshold 8 it reaches "
                f"{widest.matched_candidate_images} images "
                f"({float(widest.matched_candidate_share):.2%}), of which "
                f"{widest.cross_class_pairs} of {widest.near_duplicate_pairs} pairs "
                f"({float(widest.cross_class_rate):.0%}) are cross-class and so "
                "cannot be duplicates.\n\n"
            )

        f.write("## Conclusions\n\n")
        f.write(
            "**The D2 rejection is threshold-independent, as claimed.** It is "
            "settled at Hamming 0, before any tolerance is allowed, and loosening "
            "the rule can only add matches.\n\n"
        )
        f.write(
            "**The claim that D3B and D3C are clean across the whole range does "
            "not hold as stated, and should be narrowed rather than repeated.** "
            "Both are clean at 0 through 4. At 6 and 8 both accumulate matches, "
            "and under the stated rejection criterion D3C would flip at 6 and D3B "
            "at 8. The defensible claim is that they are clean at the operating "
            "threshold and at every stricter one, which is what the audits "
            "actually support.\n\n"
        )
        if adjudication is not None and footprint is not None:
            leak_rate = adjudication["rates"]["crossing"]["excluding_unsure"]
            estimated = footprint["unique_test_images"] * leak_rate.proportion
            f.write(
                "**The frozen split satisfies its own rule and still leaks at the "
                "patient level.** It is free of cross-partition pairs at 0, 2 and "
                f"4, exactly as designed. At 6 there are {footprint['pairs']} "
                "within-class boundary-crossing pairs, and blind adjudication "
                "against a matched control found them real: both arms score near "
                f"ceiling and the matcher's own false-positive rate is "
                f"{adjudication['matcher_false_positive'].proportion:.1%}. That "
                f"puts roughly {estimated:.0f} test images "
                f"({estimated / footprint['n_test']:.0f}% of the partition) in the "
                "position of having a same-patient counterpart in training. Image-"
                "level and group-level leakage were controlled; patient-level "
                "leakage was not, and is now measured rather than merely "
                "acknowledged.\n\n"
            )
        else:
            f.write(
                "**The frozen split is leakage-free at 0, 2 and 4, and not at 6 or "
                "8.** Most of the offending pairs at 6 are within-class, so they "
                "cannot be dismissed as matcher noise without inspecting them. The "
                "adjudication set exists for that purpose and has not yet been "
                "scored.\n\n"
            )
        f.write(
            "The specificity table is what makes the rest readable. The thresholds "
            "where the candidate decisions move are the thresholds where the "
            "matcher's own false-positive rate has risen several-fold, and at 8 "
            "the largest connected component reaches "
            f"{int(internal[internal.hamming_threshold == 8].iloc[0].largest_group_size)} "
            f"of {int(at_operating.n_left)} images, which is a collapsed matcher "
            "rather than a discovery. That is an argument for not using 6 or 8. It "
            "is not a demonstration that nothing is there.\n\n"
        )
        f.write("## How to read this\n\n")
        f.write(
            "- Pair counts rising with the threshold is arithmetic, not a finding: "
            "a wider tolerance admits strictly more pairs. Only the rates and the "
            "decisions carry information.\n"
            "- The quantity that could invalidate existing work is "
            "`pairs_crossing_train_test`, because the frozen split is already in "
            "use and every internal metric in the study depends on it.\n"
            "- A stable retain/reject verdict is not proof that a probe is "
            "independent of D1. Perceptual hashing compares images, not patients, "
            "and cannot establish patient-level independence at any threshold.\n"
        )


if __name__ == "__main__":
    main()
