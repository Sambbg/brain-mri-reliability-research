from pathlib import Path
import csv

D1_PATH = Path("data/processed/D1_manifest_deduplicated.csv")
D2_PATH = Path("data/processed/D2_manifest_deduplicated.csv")
REPORT_PATH = Path("reports/datasets/D1_D2_exact_overlap_report.md")


def load_manifest(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Manifest not found: {path}")

    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    d1_rows = load_manifest(D1_PATH)
    d2_rows = load_manifest(D2_PATH)

    d1_by_hash = {}
    for row in d1_rows:
        d1_by_hash.setdefault(row["sha256"], []).append(row)

    d2_by_hash = {}
    for row in d2_rows:
        d2_by_hash.setdefault(row["sha256"], []).append(row)

    shared_hashes = sorted(set(d1_by_hash.keys()) & set(d2_by_hash.keys()))

    overlap_pairs = []

    for sha in shared_hashes:
        for d1 in d1_by_hash[sha]:
            for d2 in d2_by_hash[sha]:
                overlap_pairs.append({
                    "sha256": sha,
                    "d1_split": d1.get("split", ""),
                    "d1_class": d1["class_label"],
                    "d1_path": d1["filepath"],
                    "d2_split": d2.get("source_split", ""),
                    "d2_class": d2["class_label"],
                    "d2_path": d2["filepath"],
                })

    cross_class_pairs = [
        pair for pair in overlap_pairs
        if pair["d1_class"] != pair["d2_class"]
    ]

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# D1-D2 Exact SHA256 Overlap Report\n\n")

        f.write("## Input\n\n")
        f.write(f"- D1 manifest: `{D1_PATH}`\n")
        f.write(f"- D2 manifest: `{D2_PATH}`\n")
        f.write(f"- D1 rows: {len(d1_rows)}\n")
        f.write(f"- D2 rows: {len(d2_rows)}\n\n")

        f.write("## Summary\n\n")
        f.write(f"- Shared SHA256 hashes: {len(shared_hashes)}\n")
        f.write(f"- Exact overlap pairs: {len(overlap_pairs)}\n")
        f.write(f"- Cross-class exact overlap pairs: {len(cross_class_pairs)}\n\n")

        f.write("## Interpretation\n\n")

        if overlap_pairs:
            f.write(
                "Exact SHA256 overlap was detected between D1 and D2. "
                "This means at least some identical files appear in both datasets. "
                "D2 must not be treated as a fully independent external dataset unless overlapping images are removed or excluded.\n\n"
            )
        else:
            f.write(
                "No exact SHA256 overlap was detected between D1 and D2. "
                "This reduces one overlap concern, but it does not rule out resized, cropped, compressed, or visually near-duplicate images. "
                "A pHash-based D1-D2 near-overlap audit is still required.\n\n"
            )

        if cross_class_pairs:
            f.write(
                "Cross-class exact overlaps were detected. This is a serious label consistency warning and requires manual review.\n\n"
            )

        f.write("## Example Exact Overlap Pairs\n\n")

        for idx, pair in enumerate(overlap_pairs[:100], start=1):
            f.write(f"### Pair {idx}\n\n")
            f.write(f"- SHA256: `{pair['sha256']}`\n")
            f.write(f"- D1: `{pair['d1_split']}` / `{pair['d1_class']}` / `{pair['d1_path']}`\n")
            f.write(f"- D2: `{pair['d2_split']}` / `{pair['d2_class']}` / `{pair['d2_path']}`\n\n")

    print(f"D1 rows: {len(d1_rows)}")
    print(f"D2 rows: {len(d2_rows)}")
    print(f"Shared SHA256 hashes: {len(shared_hashes)}")
    print(f"Exact overlap pairs: {len(overlap_pairs)}")
    print(f"Cross-class exact overlap pairs: {len(cross_class_pairs)}")
    print(f"Report written to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
