from pathlib import Path
import csv
from collections import defaultdict
import imagehash

D1_PATH = Path("data/processed/D1_manifest_deduplicated_phash.csv")
D2_PATH = Path("data/processed/D2_manifest_deduplicated_phash.csv")
REPORT_PATH = Path("reports/datasets/D1_D2_near_overlap_report.md")

PHASH_DISTANCE_THRESHOLD = 4


def load_manifest(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Manifest not found: {path}")

    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def hamming_distance(hash_a: str, hash_b: str) -> int:
    return imagehash.hex_to_hash(hash_a) - imagehash.hex_to_hash(hash_b)


def main():
    d1_rows = load_manifest(D1_PATH)
    d2_rows = load_manifest(D2_PATH)

    d1_valid = [row for row in d1_rows if row.get("phash") and row["phash"] != "ERROR"]
    d2_valid = [row for row in d2_rows if row.get("phash") and row["phash"] != "ERROR"]

    near_pairs = []
    cross_class_pairs = []
    distance_counts = defaultdict(int)

    total_comparisons = len(d1_valid) * len(d2_valid)
    print(f"D1 rows: {len(d1_valid)}")
    print(f"D2 rows: {len(d2_valid)}")
    print(f"Total comparisons: {total_comparisons}")

    for i, d1 in enumerate(d1_valid):
        if i % 500 == 0:
            print(f"Comparing D1 row {i}/{len(d1_valid)}")

        for d2 in d2_valid:
            distance = hamming_distance(d1["phash"], d2["phash"])

            if distance <= PHASH_DISTANCE_THRESHOLD:
                pair = {
                    "distance": distance,
                    "d1_split": d1.get("split", ""),
                    "d1_class": d1["class_label"],
                    "d1_path": d1["filepath"],
                    "d2_split": d2.get("source_split", ""),
                    "d2_class": d2["class_label"],
                    "d2_path": d2["filepath"],
                }

                near_pairs.append(pair)
                distance_counts[distance] += 1

                if d1["class_label"] != d2["class_label"]:
                    cross_class_pairs.append(pair)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# D1-D2 pHash Near-Overlap Report\n\n")

        f.write("## Input\n\n")
        f.write(f"- D1 pHash manifest: `{D1_PATH}`\n")
        f.write(f"- D2 pHash manifest: `{D2_PATH}`\n")
        f.write(f"- D1 rows compared: {len(d1_valid)}\n")
        f.write(f"- D2 rows compared: {len(d2_valid)}\n")
        f.write(f"- pHash Hamming distance threshold: <= {PHASH_DISTANCE_THRESHOLD}\n\n")

        f.write("## Summary\n\n")
        f.write(f"- Near-overlap pairs found: {len(near_pairs)}\n")
        f.write(f"- Cross-class near-overlap pairs: {len(cross_class_pairs)}\n\n")

        f.write("## Distance Counts\n\n")
        for distance, count in sorted(distance_counts.items()):
            f.write(f"- Distance {distance}: {count} pairs\n")

        f.write("\n## Interpretation\n\n")

        if near_pairs:
            f.write(
                "pHash near-overlap was detected between D1 and D2. "
                "This suggests possible visual overlap, reused source images, adjacent slices, or hash collisions. "
                "D2 should not be treated as a clean independent external dataset until these overlaps are handled or manually reviewed.\n\n"
            )
        else:
            f.write(
                "No pHash near-overlap was detected between D1 and D2 at the selected threshold. "
                "This supports using D2 as a stronger external target candidate, although patient-level independence still cannot be proven without metadata.\n\n"
            )

        if cross_class_pairs:
            f.write(
                "Cross-class near-overlap pairs were detected. These require manual review because they may indicate label inconsistency, visually similar slices, or pHash false positives.\n\n"
            )

        f.write("## Example Near-Overlap Pairs\n\n")

        for idx, pair in enumerate(near_pairs[:100], start=1):
            f.write(f"### Pair {idx}\n\n")
            f.write(f"- Distance: {pair['distance']}\n")
            f.write(f"- D1: `{pair['d1_split']}` / `{pair['d1_class']}` / `{pair['d1_path']}`\n")
            f.write(f"- D2: `{pair['d2_split']}` / `{pair['d2_class']}` / `{pair['d2_path']}`\n\n")

    print(f"D1 rows compared: {len(d1_valid)}")
    print(f"D2 rows compared: {len(d2_valid)}")
    print(f"Near-overlap pairs found: {len(near_pairs)}")
    print(f"Cross-class near-overlap pairs: {len(cross_class_pairs)}")
    print(f"Report written to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
