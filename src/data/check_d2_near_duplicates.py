from pathlib import Path
import csv
from collections import defaultdict
import imagehash

IN_PATH = Path("data/processed/D2_manifest_deduplicated_phash.csv")
REPORT_PATH = Path("reports/datasets/D2_near_duplicate_report.md")

PHASH_DISTANCE_THRESHOLD = 4


def load_manifest(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Manifest not found: {path}")

    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def hamming_distance(hash_a: str, hash_b: str) -> int:
    return imagehash.hex_to_hash(hash_a) - imagehash.hex_to_hash(hash_b)


def main():
    rows = load_manifest(IN_PATH)

    valid_rows = [row for row in rows if row.get("phash") and row["phash"] != "ERROR"]

    near_pairs = []
    cross_split_pairs = []
    cross_class_pairs = []

    total = len(valid_rows)

    for i in range(total):
        row_i = valid_rows[i]

        if i % 500 == 0:
            print(f"Comparing row {i}/{total}")

        for j in range(i + 1, total):
            row_j = valid_rows[j]

            distance = hamming_distance(row_i["phash"], row_j["phash"])

            if distance <= PHASH_DISTANCE_THRESHOLD:
                pair = {
                    "distance": distance,
                    "split_a": row_i["source_split"],
                    "class_a": row_i["class_label"],
                    "path_a": row_i["filepath"],
                    "split_b": row_j["source_split"],
                    "class_b": row_j["class_label"],
                    "path_b": row_j["filepath"],
                }

                near_pairs.append(pair)

                if row_i["source_split"] != row_j["source_split"]:
                    cross_split_pairs.append(pair)

                if row_i["class_label"] != row_j["class_label"]:
                    cross_class_pairs.append(pair)

    distance_counts = defaultdict(int)
    for pair in near_pairs:
        distance_counts[pair["distance"]] += 1

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# D2 Near-Duplicate Report\n\n")

        f.write("## Input\n\n")
        f.write(f"- Input manifest: `{IN_PATH}`\n")
        f.write(f"- Rows compared: {total}\n")
        f.write(f"- pHash Hamming distance threshold: <= {PHASH_DISTANCE_THRESHOLD}\n\n")

        f.write("## Summary\n\n")
        f.write(f"- Near-duplicate pairs found: {len(near_pairs)}\n")
        f.write(f"- Cross-split near-duplicate pairs: {len(cross_split_pairs)}\n")
        f.write(f"- Cross-class near-duplicate pairs: {len(cross_class_pairs)}\n\n")

        f.write("## Distance Counts\n\n")
        for distance, count in sorted(distance_counts.items()):
            f.write(f"- Distance {distance}: {count} pairs\n")

        f.write("\n## Interpretation\n\n")
        if cross_split_pairs:
            f.write(
                "Cross-split near-duplicates were detected inside D2. This indicates that the original BRISC train/test split "
                "should not be treated as independent. These pairs should be considered leakage risks unless manually reviewed.\n\n"
            )
        else:
            f.write(
                "No cross-split near-duplicates were detected at the selected pHash threshold. "
                "This reduces one internal leakage concern, but does not prove patient-level independence.\n\n"
            )

        if cross_class_pairs:
            f.write(
                "Cross-class near-duplicates were detected. These may reflect hash collisions, visually similar slices, or label-quality concerns. "
                "Manual review is required before making strong claims.\n\n"
            )

        f.write("## Example Near-Duplicate Pairs\n\n")
        for idx, pair in enumerate(near_pairs[:100], start=1):
            f.write(f"### Pair {idx}\n\n")
            f.write(f"- Distance: {pair['distance']}\n")
            f.write(f"- A: `{pair['split_a']}` / `{pair['class_a']}` / `{pair['path_a']}`\n")
            f.write(f"- B: `{pair['split_b']}` / `{pair['class_b']}` / `{pair['path_b']}`\n\n")

    print(f"Rows compared: {total}")
    print(f"Near-duplicate pairs found: {len(near_pairs)}")
    print(f"Cross-split near-duplicate pairs: {len(cross_split_pairs)}")
    print(f"Cross-class near-duplicate pairs: {len(cross_class_pairs)}")
    print(f"Report written to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
