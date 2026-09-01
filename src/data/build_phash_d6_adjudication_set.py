"""
Build a blind adjudication set for within-class pHash pairs at Hamming 6.

The threshold sensitivity audit found 371 within-class near-duplicate pairs that
straddle the train/test boundary of the frozen split at Hamming 6, against zero
at the operating threshold of 4. Whether that is contamination or matcher noise
cannot be settled by counting; the pairs have to be looked at.

This produces a blind sample so that looking at them yields a rate rather than
an impression.

  positives  40 pairs drawn from the 371, stratified to the class distribution
             of the full set
  null       40 pairs at the same distance and the same class distribution that
             do NOT cross the boundary, both endpoints in the same assigned
             split

The two groups are interleaved under one shuffle and labelled with opaque ids.
The key is written to a separate file. Scoring the sheet without opening the key
gives a false-positive rate for within-class matches at Hamming 6: if the
adjudicator cannot tell the groups apart, the boundary-crossing pairs are noise
and the frozen split is sound at 6; if the positives are reliably judged
duplicates and the null pairs are not, the split leaks.

Two deviations from a naive design, both necessary for the blind to hold:

  * The null is drawn at distance 6 exactly, not 5 to 7. Every D1 pHash has
    exactly 32 of its 64 bits set, a property of the median split used to
    compute it, so the Hamming distance between any two hashes is always even
    and odd distances do not occur. All 371 positives sit at exactly 6. A null
    spanning 5 to 7 would therefore be identifiable from the printed distance
    alone.
  * Filenames are printed. Their Tr-/Te- prefixes name the *original* folder,
    not the assigned split, and carry almost no information about it: 14.5% of
    Te- images and 15.1% of Tr- images are in the test partition. Checked
    before deciding to show them.

Run from the repo root:
    python src/data/build_phash_d6_adjudication_set.py
"""

from pathlib import Path
import hashlib
import subprocess

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

D1_PHASH = Path("data/processed/D1_manifest_deduplicated_phash.csv")
SPLIT_CSV = Path("data/splits/D1_leakage_aware_split.csv")
EXPECTED_SPLIT_SHA256 = "944ce00e4be958f3688a0996f6fb928fc7717e7c2804abb8000f28976efe0d43"

OUT_DIR = Path("reports/datasets/phash_d6_adjudication")
PAIRS_DIR = OUT_DIR / "pairs"
CONTACT_SHEET = OUT_DIR / "contact_sheet.pdf"
WORKSHEET_CSV = OUT_DIR / "adjudication_worksheet.csv"
KEY_CSV = OUT_DIR / "blind_key.csv"
REPORT = OUT_DIR / "README.md"

TARGET_DISTANCE = 6
N_PER_GROUP = 40
SEED = 42

FONT_PATH = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
FONT_BOLD_PATH = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
HEADER_PX = 78
GAP_PX = 16
BACKGROUND = (255, 255, 255)
TEXT = (20, 20, 20)


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


def load_d1():
    frame = pd.read_csv(D1_PHASH)
    frame = frame[frame.phash.notna() & (frame.phash != "ERROR")].reset_index(drop=True)

    split = pd.read_csv(SPLIT_CSV)
    frame["assigned"] = frame.filepath.map(dict(zip(split.filepath, split.assigned_split)))

    if frame.assigned.isna().any():
        raise RuntimeError("Some manifest rows are absent from the frozen split.")

    hashes = np.array([int(str(h), 16) for h in frame.phash], dtype=np.uint64)

    weights = np.bitwise_count(hashes)
    if not (weights == 32).all():
        raise RuntimeError(
            "Not every hash has 32 bits set. The even-distance property this "
            "sampling design relies on does not hold; revisit the null distance."
        )

    return frame, hashes


def all_pairs(hashes, max_distance, chunk=1024):
    out_i, out_j, out_d = [], [], []
    for start in range(0, len(hashes), chunk):
        block = hashes[start:start + chunk]
        distance = np.bitwise_count(block[:, None] ^ hashes[None, :]).astype(np.int16)
        rows = np.arange(start, start + len(block))[:, None]
        cols = np.arange(len(hashes))[None, :]
        bi, bj = np.nonzero((distance <= max_distance) & (cols > rows))
        out_i.append(bi + start)
        out_j.append(bj)
        out_d.append(distance[bi, bj])
    return np.concatenate(out_i), np.concatenate(out_j), np.concatenate(out_d)


def stratified_targets(class_counts, total):
    """Largest-remainder allocation, so the sample matches the population shape."""
    grand = sum(class_counts.values())
    exact = {c: total * n / grand for c, n in class_counts.items()}
    floors = {c: int(v) for c, v in exact.items()}

    remaining = total - sum(floors.values())
    order = sorted(exact, key=lambda c: (exact[c] - floors[c], c), reverse=True)

    for c in order[:remaining]:
        floors[c] += 1

    return floors


def load_font(path, size):
    try:
        return ImageFont.truetype(str(path), size)
    except Exception:
        return ImageFont.load_default()


def render_pair(pair_id, row_a, row_b, distance, out_path):
    """Side by side at native resolution, with a labelled header."""
    image_a = Image.open(row_a.filepath).convert("RGB")
    image_b = Image.open(row_b.filepath).convert("RGB")

    width = image_a.width + image_b.width + 3 * GAP_PX
    height = max(image_a.height, image_b.height) + HEADER_PX + GAP_PX
    width = max(width, 640)

    canvas = Image.new("RGB", (width, height), BACKGROUND)
    canvas.paste(image_a, (GAP_PX, HEADER_PX))
    canvas.paste(image_b, (GAP_PX * 2 + image_a.width, HEADER_PX))

    draw = ImageDraw.Draw(canvas)
    bold = load_font(FONT_BOLD_PATH, 22)
    plain = load_font(FONT_PATH, 15)

    draw.text((GAP_PX, 10), f"{pair_id}", font=bold, fill=TEXT)
    draw.text(
        (GAP_PX + 130, 13),
        f"class: {row_a.class_label}    pHash Hamming distance: {distance}",
        font=plain, fill=TEXT,
    )
    draw.text(
        (GAP_PX, 44),
        f"A: {row_a.filename}  ({image_a.width}x{image_a.height})     "
        f"B: {row_b.filename}  ({image_b.width}x{image_b.height})",
        font=plain, fill=TEXT,
    )

    canvas.save(out_path)
    return canvas


def main():
    split_hash = verify_split(SPLIT_CSV)
    frame, hashes = load_d1()

    labels = frame.class_label.to_numpy()
    assigned = frame.assigned.to_numpy()

    i, j, d = all_pairs(hashes, TARGET_DISTANCE)

    at_distance = d == TARGET_DISTANCE
    within_class = labels[i] == labels[j]
    crosses = (
        ((assigned[i] == "train") & (assigned[j] == "test"))
        | ((assigned[i] == "test") & (assigned[j] == "train"))
    )
    same_split = assigned[i] == assigned[j]

    positive = np.nonzero(at_distance & within_class & crosses)[0]
    null = np.nonzero(at_distance & within_class & same_split)[0]

    print(f"Positive population (crossing, within-class, d={TARGET_DISTANCE}): {len(positive)}")
    print(f"Null population (same split, within-class, d={TARGET_DISTANCE}):  {len(null)}")

    rng = np.random.default_rng(SEED)

    population_classes = pd.Series(labels[i][positive]).value_counts().to_dict()
    targets = stratified_targets(population_classes, N_PER_GROUP)
    print(f"Stratified targets per class: {targets}")

    def sample_stratified(candidate_idx, targets):
        chosen = []
        candidate_classes = labels[i][candidate_idx]
        for class_name in sorted(targets):
            want = targets[class_name]
            pool = candidate_idx[candidate_classes == class_name]
            if len(pool) < want:
                raise RuntimeError(
                    f"Null pool for {class_name} has {len(pool)} pairs, need {want}."
                )
            chosen.append(rng.choice(pool, size=want, replace=False))
        return np.concatenate(chosen)

    positive_sample = sample_stratified(positive, targets)
    null_sample = sample_stratified(null, targets)

    records = []
    for group, sample in (("crossing", positive_sample), ("same_split", null_sample)):
        for pair_index in sample:
            a, b = int(i[pair_index]), int(j[pair_index])
            records.append({
                "group": group,
                "index_a": a,
                "index_b": b,
                "distance": int(d[pair_index]),
                "class_label": labels[a],
                "split_a": assigned[a],
                "split_b": assigned[b],
            })

    order = rng.permutation(len(records))
    records = [records[k] for k in order]

    for position, record in enumerate(records, start=1):
        record["pair_id"] = f"PAIR_{position:02d}"

    PAIRS_DIR.mkdir(parents=True, exist_ok=True)
    pages = []

    for record in records:
        row_a = frame.iloc[record["index_a"]]
        row_b = frame.iloc[record["index_b"]]
        record["filename_a"] = row_a.filename
        record["filename_b"] = row_b.filename
        record["filepath_a"] = row_a.filepath
        record["filepath_b"] = row_b.filepath

        page = render_pair(
            record["pair_id"], row_a, row_b, record["distance"],
            PAIRS_DIR / f"{record['pair_id']}.png",
        )
        pages.append(page)

    pages[0].save(
        CONTACT_SHEET, "PDF", resolution=100.0,
        save_all=True, append_images=pages[1:],
    )

    provenance = {
        "git_commit": get_git_commit_hash(),
        "split_csv_sha256": split_hash,
        "d1_phash_sha256": sha256_file(D1_PHASH),
        "seed": SEED,
        "distance": TARGET_DISTANCE,
    }

    table = pd.DataFrame(records)

    worksheet = table[[
        "pair_id", "class_label", "distance", "filename_a", "filename_b",
    ]].copy()
    # same_image | same_patient | distinct | unsure -- see README. The
    # same_patient category is the load-bearing one: a leakage-aware split
    # separates patients, not images.
    worksheet["verdict"] = ""
    worksheet["notes"] = ""
    worksheet.to_csv(WORKSHEET_CSV, index=False)

    key = table[[
        "pair_id", "group", "class_label", "distance",
        "split_a", "split_b", "filename_a", "filename_b",
        "filepath_a", "filepath_b", "index_a", "index_b",
    ]].copy()
    for name, value in provenance.items():
        key[name] = value
    key.to_csv(KEY_CSV, index=False)

    write_report(table, provenance, len(positive), len(null), targets)

    print(f"\nContact sheet: {CONTACT_SHEET} ({len(pages)} pages)")
    print(f"Worksheet:     {WORKSHEET_CSV}  (blind)")
    print(f"Key:           {KEY_CSV}        (do not open before scoring)")
    print(f"Report:        {REPORT}")


def write_report(table, provenance, n_positive, n_null, targets):
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with REPORT.open("w", encoding="utf-8") as f:
        f.write("# Blind adjudication set: within-class pHash pairs at Hamming 6\n\n")
        f.write(
            "The threshold sensitivity audit "
            "(`reports/experiments/consolidated/tables/phash_threshold_sensitivity.md`) "
            f"found {n_positive} within-class near-duplicate pairs that cross the "
            "train/test boundary of the frozen split at Hamming 6, against zero at "
            "the operating threshold of 4. Counting cannot settle whether those are "
            "real duplicates. This set exists so that looking at them produces a "
            "rate instead of an impression.\n\n"
        )

        f.write("## What is in the sample\n\n")
        f.write("| Group | n | Definition |\n|---|---:|---|\n")
        f.write(
            f"| `crossing` | {N_PER_GROUP} | Within-class, distance 6, one endpoint "
            f"in train and one in test. Drawn from {n_positive}. |\n"
        )
        f.write(
            f"| `same_split` | {N_PER_GROUP} | Within-class, distance 6, both "
            f"endpoints in the same assigned split. Drawn from {n_null}. |\n\n"
        )
        f.write(
            f"Both groups are stratified to the class distribution of the full "
            f"crossing population: {targets}. The two are interleaved under a "
            f"single shuffle at seed {provenance['seed']} and labelled PAIR_01 to "
            f"PAIR_{2 * N_PER_GROUP}.\n\n"
        )

        f.write("## Why the null is at distance 6 exactly\n\n")
        f.write(
            "Every D1 pHash has exactly 32 of its 64 bits set, which the median "
            "split used to compute it guarantees. The Hamming distance between two "
            "equal-weight vectors is always even, so odd distances cannot occur, "
            "and the observed distances are only 0, 2, 4 and 6. All "
            f"{n_positive} crossing pairs sit at exactly 6. A null drawn from 5 to "
            "7 would therefore have been identifiable from the printed distance "
            "alone, and the comparison would not have been blind. The script "
            "asserts the 32-bit property and aborts if it ever stops holding.\n\n"
        )
        f.write(
            "A consequence worth carrying back to the sensitivity audit: because "
            "distances are always even, thresholds 1, 3, 5 and 7 behave identically "
            "to 0, 2, 4 and 6. The sweep already reported is exhaustive over the "
            "range, not a sample of it.\n\n"
        )

        f.write("## Why filenames are shown\n\n")
        f.write(
            "The `Tr-` and `Te-` prefixes name the original download folder, not "
            "the assigned split, and predict it barely at all: 14.5% of `Te-` "
            "images and 15.1% of `Tr-` images are in the test partition. Printing "
            "them does not unblind the sample. The assigned split is in the key "
            "only.\n\n"
        )

        f.write("## How to score it\n\n")
        f.write(
            f"1. Open `contact_sheet.pdf` ({2 * N_PER_GROUP} pages, one pair per "
            "page, both images at native resolution).\n"
            "2. For each pair, record one of four verdicts in the `verdict` column "
            "of `adjudication_worksheet.csv`.\n"
            "3. Only then open `blind_key.csv`.\n\n"
        )
        f.write("| Verdict | Meaning | Counts as leakage? |\n|---|---|---|\n")
        f.write(
            "| `same_image` | The same slice, differing only by rescaling, "
            "re-encoding or minor cropping. | Yes |\n"
        )
        f.write(
            "| `same_patient` | Different slices, but evidently the same patient "
            "and acquisition: the skull outline, ventricles and gross anatomy "
            "correspond while the tumour or the slice level differs. | **Yes** |\n"
        )
        f.write(
            "| `distinct` | Two different patients that merely resemble each "
            "other. | No |\n"
        )
        f.write("| `unsure` | Cannot tell. | Counted separately |\n\n")
        f.write(
            "**The `same_patient` category is the one that matters and is easy to "
            "score wrongly.** A leakage-aware split has to separate patients, not "
            "images. Two adjacent slices from one series sitting either side of the "
            "train/test boundary are contamination even though the images are "
            "plainly not identical, and a binary duplicate/distinct rubric would "
            "score them as clean. Judge patient identity, not image identity.\n\n"
        )
        f.write(
            "The quantity of interest is the leakage rate -- `same_image` plus "
            "`same_patient` -- in each group, and the difference between them. If "
            "the two groups come out at materially the same rate, then Hamming 6 "
            "flags the same kind of thing on both sides of the boundary, the "
            "boundary-crossing count is matcher noise, and the frozen split is "
            "sound at 6. If the `crossing` group is higher, the split leaks at 6 "
            "and the internal metrics carry contamination the audit at threshold 4 "
            "did not detect.\n\n"
        )
        f.write(
            "Note that the `same_split` group is not a pure negative control. Its "
            "pairs can perfectly well be the same patient -- that is exactly what "
            "the leakage-aware grouping is supposed to achieve, keeping a patient's "
            "images together on one side. A high `same_patient` rate in that group "
            "is the split working, not failing. The comparison is therefore between "
            "rates, not against zero.\n\n"
        )
        f.write(
            "Note the asymmetry in what the two outcomes cost. A null result "
            "closes the limitation. A positive result does not invalidate the "
            "study on its own, because it would have to be weighed against how "
            "many pairs are involved -- 371 pairs across 7,013 images -- but it "
            "would need reporting and quantifying rather than a footnote.\n\n"
        )

        f.write("## Provenance\n\n| Field | Value |\n|---|---|\n")
        for name, value in provenance.items():
            f.write(f"| {name} | `{value}` |\n")
        f.write(
            f"\nSampled composition: "
            f"{table.group.value_counts().to_dict()}, "
            f"classes {table.class_label.value_counts().to_dict()}.\n"
        )


if __name__ == "__main__":
    main()
