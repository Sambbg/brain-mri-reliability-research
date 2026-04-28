from pathlib import Path
import csv
import random
from collections import defaultdict, Counter
import imagehash

IN_PATH = Path("data/processed/D1_manifest_deduplicated_phash.csv")
OUT_SPLIT_PATH = Path("data/splits/D1_leakage_aware_split.csv")
REPORT_PATH = Path("reports/datasets/D1_leakage_aware_split_report.md")

PHASH_DISTANCE_THRESHOLD = 4
SEED = 42

TARGET_PROPORTIONS = {
    "train": 0.70,
    "val": 0.15,
    "test": 0.15,
}


class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int):
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return

        if self.rank[root_a] < self.rank[root_b]:
            self.parent[root_a] = root_b
        elif self.rank[root_a] > self.rank[root_b]:
            self.parent[root_b] = root_a
        else:
            self.parent[root_b] = root_a
            self.rank[root_a] += 1


def load_manifest(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Manifest not found: {path}")

    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def hamming_distance(hash_a: str, hash_b: str) -> int:
    return imagehash.hex_to_hash(hash_a) - imagehash.hex_to_hash(hash_b)


def majority_label(rows):
    counts = Counter(row["class_label"] for row in rows)
    return counts.most_common(1)[0][0]


def assign_groups_to_splits(groups):
    """
    Greedy stratified group assignment.

    We group by majority class, then assign the largest groups first to the split
    with the largest current deficit for that class.
    """
    random.seed(SEED)

    split_rows = {name: [] for name in TARGET_PROPORTIONS}
    split_class_counts = {
        name: defaultdict(int) for name in TARGET_PROPORTIONS
    }

    groups_by_majority_class = defaultdict(list)

    for group_id, rows in groups.items():
        maj = majority_label(rows)
        groups_by_majority_class[maj].append((group_id, rows))

    for class_label, class_groups in groups_by_majority_class.items():
        random.shuffle(class_groups)
        class_groups.sort(key=lambda x: len(x[1]), reverse=True)

        total_class_rows = sum(len(rows) for _, rows in class_groups)

        target_class_counts = {
            split: total_class_rows * prop
            for split, prop in TARGET_PROPORTIONS.items()
        }

        for group_id, rows in class_groups:
            deficits = {}

            for split in TARGET_PROPORTIONS:
                current = split_class_counts[split][class_label]
                target = target_class_counts[split]
                deficits[split] = target - current

            chosen_split = max(deficits, key=deficits.get)

            for row in rows:
                new_row = dict(row)
                new_row["leakage_group_id"] = str(group_id)
                new_row["leakage_group_size"] = str(len(rows))
                new_row["leakage_group_majority_class"] = class_label
                new_row["assigned_split"] = chosen_split
                split_rows[chosen_split].append(new_row)

            split_class_counts[chosen_split][class_label] += len(rows)

    output_rows = []
    for split in ["train", "val", "test"]:
        output_rows.extend(split_rows[split])

    return output_rows, split_rows


def verify_no_near_duplicate_cross_split(rows):
    """
    Re-checks that no pHash-near-duplicate pair crosses the assigned split boundary.
    This is slow but acceptable for this dataset size.
    """
    valid_rows = [row for row in rows if row.get("phash") and row["phash"] != "ERROR"]

    cross_split_pairs = []
    total = len(valid_rows)

    for i in range(total):
        if i % 500 == 0:
            print(f"Verification comparing row {i}/{total}")

        row_i = valid_rows[i]

        for j in range(i + 1, total):
            row_j = valid_rows[j]

            if row_i["assigned_split"] == row_j["assigned_split"]:
                continue

            distance = hamming_distance(row_i["phash"], row_j["phash"])

            if distance <= PHASH_DISTANCE_THRESHOLD:
                cross_split_pairs.append({
                    "distance": distance,
                    "split_a": row_i["assigned_split"],
                    "class_a": row_i["class_label"],
                    "path_a": row_i["filepath"],
                    "split_b": row_j["assigned_split"],
                    "class_b": row_j["class_label"],
                    "path_b": row_j["filepath"],
                })

    return cross_split_pairs


def main():
    rows = load_manifest(IN_PATH)

    valid_rows = [row for row in rows if row.get("phash") and row["phash"] != "ERROR"]

    print(f"Rows loaded: {len(rows)}")
    print(f"Rows with valid pHash: {len(valid_rows)}")

    uf = UnionFind(len(valid_rows))

    for i in range(len(valid_rows)):
        if i % 500 == 0:
            print(f"Grouping row {i}/{len(valid_rows)}")

        for j in range(i + 1, len(valid_rows)):
            distance = hamming_distance(valid_rows[i]["phash"], valid_rows[j]["phash"])

            if distance <= PHASH_DISTANCE_THRESHOLD:
                uf.union(i, j)

    groups = defaultdict(list)

    for idx, row in enumerate(valid_rows):
        root = uf.find(idx)
        groups[root].append(row)

    output_rows, split_rows = assign_groups_to_splits(groups)

    OUT_SPLIT_PATH.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(output_rows[0].keys())

    with OUT_SPLIT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Split written to: {OUT_SPLIT_PATH}")
    print("Now verifying no cross-split near-duplicate leakage...")

    cross_split_pairs = verify_no_near_duplicate_cross_split(output_rows)

    split_counts = Counter(row["assigned_split"] for row in output_rows)
    class_split_counts = Counter(
        (row["assigned_split"], row["class_label"]) for row in output_rows
    )

    group_sizes = [len(items) for items in groups.values()]
    mixed_label_groups = {
        gid: items for gid, items in groups.items()
        if len({row["class_label"] for row in items}) > 1
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# D1 Leakage-Aware Split Report\n\n")

        f.write("## Input and Output\n\n")
        f.write(f"- Input manifest: `{IN_PATH}`\n")
        f.write(f"- Output split file: `{OUT_SPLIT_PATH}`\n")
        f.write(f"- Random seed: {SEED}\n")
        f.write(f"- pHash Hamming distance threshold: <= {PHASH_DISTANCE_THRESHOLD}\n\n")

        f.write("## Summary\n\n")
        f.write(f"- Rows loaded: {len(rows)}\n")
        f.write(f"- Rows assigned: {len(output_rows)}\n")
        f.write(f"- Leakage groups created: {len(groups)}\n")
        f.write(f"- Largest leakage group size: {max(group_sizes)}\n")
        f.write(f"- Mixed-label leakage groups: {len(mixed_label_groups)}\n")
        f.write(f"- Cross-split near-duplicate pairs after splitting: {len(cross_split_pairs)}\n\n")

        f.write("## Assigned Split Counts\n\n")
        for split in ["train", "val", "test"]:
            f.write(f"- {split}: {split_counts[split]}\n")

        f.write("\n## Assigned Split Counts by Class\n\n")
        for split in ["train", "val", "test"]:
            f.write(f"### {split}\n\n")
            for class_label in sorted({row["class_label"] for row in output_rows}):
                f.write(f"- {class_label}: {class_split_counts[(split, class_label)]}\n")
            f.write("\n")

        f.write("## Verification\n\n")
        if cross_split_pairs:
            f.write(
                "Warning: cross-split near-duplicate pairs remain after leakage-aware splitting. "
                "This indicates a bug or an overly complex grouping issue that requires investigation.\n\n"
            )
        else:
            f.write(
                "No pHash-near-duplicate pairs crossed the assigned train/validation/test split boundary "
                "at the selected threshold. This does not prove patient-level independence, but it removes "
                "the detected pHash-based near-duplicate leakage from the split.\n\n"
            )

        f.write("## Interpretation\n\n")
        f.write(
            "This split should be preferred over the original Kaggle Training/Testing folders for internal D1 experiments. "
            "The original split had substantial pHash-based cross-split near-duplicate risk. This leakage-aware split groups "
            "near-duplicate images together before assigning train, validation, and test partitions.\n\n"
        )

        f.write("## Caveats\n\n")
        f.write(
            "- pHash grouping may over-group visually similar but genuinely distinct MRI slices.\n"
            "- Patient-level identifiers are still unavailable.\n"
            "- This split is cleaner than the original Kaggle split but is not a substitute for independent external validation.\n"
            "- Publication-grade generalisation claims still require an external dataset.\n"
        )

    print(f"Rows assigned: {len(output_rows)}")
    print(f"Leakage groups: {len(groups)}")
    print(f"Largest group size: {max(group_sizes)}")
    print(f"Mixed-label groups: {len(mixed_label_groups)}")
    print(f"Cross-split near-duplicate pairs after splitting: {len(cross_split_pairs)}")
    print(f"Report written to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
