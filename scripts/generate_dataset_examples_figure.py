#!/usr/bin/env python3
"""
Figure 8: representative images from each dataset.

The manuscript contains seven figures and no brain MRI. A reader is asked to
accept "cross-species shift" and "same-species shift" as descriptions without
seeing what they look like, and to accept that D2 is a repackaging of D1 without
seeing a duplicate pair. This figure supplies both.

Panel (a): a grid of representative images, one row per dataset role.
    D1   four images, one per class
    D2   four images, chosen from those byte-identical to D1
    D3B  four canine slices
    D3C  four human glioblastoma slices

Panel (b): a matched duplicate pair, one D1 image beside its byte-identical D2
    counterpart, with the shared SHA-256 prefix printed beneath. 4,740 is a
    number; two identical pictures is an argument.

Images are selected deterministically from the committed manifests, and every
selected file is recorded in a CSV alongside the figure so that any example can
be traced back to its source record.

Run from the repo root:
    python scripts/generate_dataset_examples_figure.py

Optional:
    --no-duplicate-panel    skip panel (b) if the D2 files are not present
    --seed N                change the deterministic selection

Writes to reports/experiments/consolidated/paper_figures/:
    figure_8_dataset_examples.png / .pdf
    figure_8_source_images.csv
"""

import argparse
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required:  pip install Pillow")

OUT = Path("reports/experiments/consolidated/paper_figures")

D1_SPLIT = Path("data/splits/D1_leakage_aware_split.csv")
D2_MANIFEST_CANDIDATES = [
    Path("data/processed/D2_manifest_deduplicated.csv"),
    Path("data/processed/D2_manifest.csv"),
]
D3B_MANIFEST_CANDIDATES = [
    Path("data/processed/D3B_selected_slices_manifest_phash.csv"),
    Path("data/processed/D3B_selected_slices_manifest.csv"),
]
D3C_MANIFEST_CANDIDATES = [
    Path("data/processed/D3C_analysis_manifest.csv"),
    Path("data/processed/D3C_selected_slices_manifest_phash.csv"),
]

CLASS_ORDER = ["glioma", "meningioma", "notumor", "pituitary"]
CLASS_LABEL = {"glioma": "Glioma", "meningioma": "Meningioma",
               "notumor": "No tumour", "pituitary": "Pituitary"}

# match the styling of the other paper figures
plt.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42,
    "font.family": "serif",
    "font.serif": ["Liberation Serif", "DejaVu Serif"],
    "font.size": 9, "axes.titlesize": 9, "axes.labelsize": 9,
    "figure.dpi": 300, "savefig.dpi": 300,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
})
MM = 1 / 25.4
DOUBLE_COL = 190 * MM


def first_existing(paths):
    for p in paths:
        if p.exists():
            return p
    return None


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def col(rows, *names):
    """Find a column by exact name then by substring."""
    if not rows:
        return None
    for n in names:
        if n in rows[0]:
            return n
    for c in rows[0]:
        lc = c.lower()
        if any(n.lower() in lc for n in names):
            return c
    return None


def load_image(path):
    """Load as greyscale float array, or None if unreadable."""
    try:
        with Image.open(path) as im:
            return np.asarray(im.convert("L"), dtype=float)
    except Exception:
        return None


def resolve(p):
    """Try the path as given, then relative to the repo root."""
    cand = Path(p)
    if cand.exists():
        return cand
    for prefix in ("", "data/raw/", "data/processed/"):
        alt = Path(prefix) / p
        if alt.exists():
            return alt
    return None


def pick_d1(rng):
    """One image per class from the training partition."""
    if not D1_SPLIT.exists():
        return []
    rows = read_csv(D1_SPLIT)
    c_path = col(rows, "filepath", "path")
    c_class = col(rows, "class_label", "label", "class")
    c_split = col(rows, "assigned_split", "split")
    c_hash = col(rows, "sha256")
    out = []
    for cls in CLASS_ORDER:
        pool = [r for r in rows
                if (r.get(c_class) or "").strip().lower() == cls
                and (r.get(c_split) or "").strip().lower() == "train"]
        rng.shuffle(pool)
        for r in pool:
            path = resolve(r[c_path])
            if path and load_image(path) is not None:
                out.append({"dataset": "D1", "label": CLASS_LABEL[cls],
                            "path": str(path), "sha256": r.get(c_hash, "")})
                break
    return out


def pick_d2(rng, d1_hashes):
    """Images from D2 that are byte-identical to something in D1."""
    man = first_existing(D2_MANIFEST_CANDIDATES)
    if not man:
        return []
    rows = read_csv(man)
    c_path = col(rows, "filepath", "path")
    c_class = col(rows, "class_label", "label", "class")
    c_hash = col(rows, "sha256")
    shared = [r for r in rows if r.get(c_hash) in d1_hashes]
    if not shared:
        shared = rows
    out, seen = [], set()
    rng.shuffle(shared)
    for r in shared:
        cls = (r.get(c_class) or "").strip().lower()
        if cls in seen or cls not in CLASS_ORDER:
            continue
        path = resolve(r[c_path])
        if path and load_image(path) is not None:
            out.append({"dataset": "D2", "label": CLASS_LABEL.get(cls, cls),
                        "path": str(path), "sha256": r.get(c_hash, "")})
            seen.add(cls)
        if len(out) == 4:
            break
    return out


def pick_probe(rng, candidates, name, n=4):
    man = first_existing(candidates)
    if not man:
        return []
    rows = read_csv(man)
    c_path = col(rows, "output_image_path", "png_path", "filepath", "output_path")
    c_pat = col(rows, "patient_id", "PatientID", "patient")
    if not c_path:
        return []
    # one slice per patient, distinct patients
    by_patient = {}
    for r in rows:
        pid = r.get(c_pat, "")
        by_patient.setdefault(pid, []).append(r)
    pids = sorted(by_patient)
    rng.shuffle(pids)
    out = []
    for pid in pids:
        r = by_patient[pid][len(by_patient[pid]) // 2]     # central slice
        path = resolve(r[c_path])
        if path and load_image(path) is not None:
            out.append({"dataset": name, "label": pid[:20],
                        "path": str(path), "sha256": r.get("sha256", "")})
        if len(out) == n:
            break
    return out


def find_duplicate_pair(d1_rows, d2_man):
    """One D1 image and its byte-identical D2 counterpart."""
    if not d2_man:
        return None
    c1_path = col(d1_rows, "filepath", "path")
    c1_hash = col(d1_rows, "sha256")
    d1_by_hash = {r[c1_hash]: r for r in d1_rows if r.get(c1_hash)}

    rows2 = read_csv(d2_man)
    c2_path = col(rows2, "filepath", "path")
    c2_hash = col(rows2, "sha256")

    for r2 in rows2:
        h = r2.get(c2_hash)
        if h in d1_by_hash:
            p1 = resolve(d1_by_hash[h][c1_path])
            p2 = resolve(r2[c2_path])
            if p1 and p2:
                a, b = load_image(p1), load_image(p2)
                if a is not None and b is not None:
                    return {"hash": h, "d1": (str(p1), a), "d2": (str(p2), b)}
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--no-duplicate-panel", action="store_true")
    args = ap.parse_args()

    import random
    rng = random.Random(args.seed)
    OUT.mkdir(parents=True, exist_ok=True)

    if not D1_SPLIT.exists():
        sys.exit(f"{D1_SPLIT} not found. Run this from the repo root.")

    d1_rows = read_csv(D1_SPLIT)
    c_hash = col(d1_rows, "sha256")
    d1_hashes = {r[c_hash] for r in d1_rows if r.get(c_hash)}

    print("Selecting images...")
    rows_by_ds = {
        "D1": pick_d1(rng),
        "D2": pick_d2(rng, d1_hashes),
        "D3B": pick_probe(rng, D3B_MANIFEST_CANDIDATES, "D3B"),
        "D3C": pick_probe(rng, D3C_MANIFEST_CANDIDATES, "D3C"),
    }
    for k, v in rows_by_ds.items():
        print(f"  {k}: {len(v)} images")

    present = [k for k in ("D1", "D2", "D3B", "D3C") if rows_by_ds[k]]
    if not present:
        sys.exit("No images could be located. Check that the raw datasets are present.")

    dup = None
    if not args.no_duplicate_panel:
        dup = find_duplicate_pair(d1_rows, first_existing(D2_MANIFEST_CANDIDATES))
        print(f"  duplicate pair: {'found' if dup else 'not found'}")

    ROW_NOTE = {
        "D1": "Internal, four classes\n7,013 images",
        "D2": "Rejected candidate\n4,740 byte-identical to D1",
        "D3B": "Cross-species probe\n53 canine patients",
        "D3C": "Same-species probe\n610 human GBM patients",
    }

    ncol = 4
    nrow = len(present)
    height = (46 * nrow + (52 if dup else 0)) * MM
    fig = plt.figure(figsize=(DOUBLE_COL, height))

    if dup:
        gs = fig.add_gridspec(nrow + 1, ncol, height_ratios=[1] * nrow + [1.15],
                              hspace=0.30, wspace=0.06)
    else:
        gs = fig.add_gridspec(nrow, ncol, hspace=0.30, wspace=0.06)

    manifest = []
    for r, ds in enumerate(present):
        for c in range(ncol):
            ax = fig.add_subplot(gs[r, c])
            ax.set_xticks([]); ax.set_yticks([])
            for sp in ax.spines.values():
                sp.set_linewidth(0.6); sp.set_color("#666666")
            if c < len(rows_by_ds[ds]):
                rec = rows_by_ds[ds][c]
                img = load_image(rec["path"])
                ax.imshow(img, cmap="gray", aspect="equal")
                ax.set_title(rec["label"], fontsize=7.5, pad=2.5)
                manifest.append(rec)
            else:
                ax.text(0.5, 0.5, "not available", ha="center", va="center",
                        fontsize=7, color="#999999", transform=ax.transAxes)
            if c == 0:
                ax.set_ylabel(f"$\\bf{{{ds}}}$\n{ROW_NOTE[ds]}",
                              fontsize=7.5, rotation=0, ha="right", va="center",
                              labelpad=44)

    if dup:
        for c, key in enumerate(("d1", "d2")):
            ax = fig.add_subplot(gs[nrow, c])
            path, img = dup[key]
            ax.imshow(img, cmap="gray", aspect="equal")
            ax.set_xticks([]); ax.set_yticks([])
            for sp in ax.spines.values():
                sp.set_linewidth(1.1); sp.set_color("#A94442")
            ax.set_title(f"{key.upper()}: {Path(path).name[:26]}", fontsize=7.5, pad=2.5)
        ax = fig.add_subplot(gs[nrow, 2:])
        ax.axis("off")
        ax.text(0.02, 0.62,
                "Byte-identical pair", fontsize=9, fontweight="bold",
                transform=ax.transAxes, va="center")
        ax.text(0.02, 0.34,
                f"shared SHA-256  {dup['hash'][:32]}...\n"
                "4,740 of D2's 5,950 images match D1 in this way",
                fontsize=7.5, transform=ax.transAxes, va="center", family="monospace")
        manifest.append({"dataset": "duplicate pair D1", "label": "",
                         "path": dup["d1"][0], "sha256": dup["hash"]})
        manifest.append({"dataset": "duplicate pair D2", "label": "",
                         "path": dup["d2"][0], "sha256": dup["hash"]})

    for ext in ("png", "pdf"):
        p = OUT / f"figure_8_dataset_examples.{ext}"
        fig.savefig(p)
        print(f"  {p}")
    plt.close(fig)

    with open(OUT / "figure_8_source_images.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["dataset", "label", "path", "sha256"])
        w.writeheader(); w.writerows(manifest)
    print(f"  {OUT / 'figure_8_source_images.csv'}")

    print()
    print("Caption:")
    print("Figure 8. Representative images from each dataset role. D1 is the internal")
    print("four-class dataset; D2 is the candidate external set rejected after auditing;")
    print("D3B and D3C are the cross-species and same-species shifted-domain probes. The")
    print("lower panel shows one D1 image beside its byte-identical D2 counterpart,")
    print("sharing a SHA-256 hash. Probe images are reproduced under CC BY 4.0.")
    print()
    print("Check the licence terms for the internal dataset before including its images.")


if __name__ == "__main__":
    main()
