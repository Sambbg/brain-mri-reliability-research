from pathlib import Path
import csv
from collections import defaultdict

MANIFEST_PATH = Path("data/processed/D1_manifest.csv")
OUT_PATH = Path("reports/datasets/D1_exact_duplicate_report.md")


def load_manifest(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Manifest not found: {path}")

    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    rows = load_manifest(MANIFEST_PATH)

    by_hash = defaultdict(list)

    for row in rows:
        sha = row["sha256"]
        by_hash[sha].append(row)

    duplicate_groups = {
        sha: items for sha, items in by_hash.items()
        if len(items) > 1
    }

    total_duplicate_images = sum(len(items) for items in duplicate_groups.values())
    duplicate_group_count = len(duplicate_groups)

    cross_split_groups = {}
    cross_class_groups = {}

    for sha, items in duplicate_groups.items():
        splits = {item["split"] for item in items}
        classes = {item["class_label"] for item in items}

        if len(splits) > 1:
            cross_split_groups[sha] = items

        if len(classes) > 1:
            cross_class_groups[sha] = items

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUT_PATH.open("w", encoding="utf-8") as f:
        f.write("# D1 Exact Duplicate Report\n\n")
        f.write("## Input\n\n")
        f.write(f"- Manifest: `{MANIFEST_PATH}`\n")
        f.write(f"- Total manifest rows: {len(rows)}\n\n")

        f.write("## Summary\n\n")
        f.write(f"- Unique SHA256 hashes: {len(by_hash)}\n")
        f.write(f"- Duplicate hash groups: {duplicate_group_count}\n")
        f.write(f"- Images involved in duplicate groups: {total_duplicate_images}\n")
        f.write(f"- Cross-split duplicate groups: {len(cross_split_groups)}\n")
        f.write(f"- Cross-class duplicate groups: {len(cross_class_groups)}\n\n")

        f.write("## Interpretation\n\n")

        if duplicate_group_count == 0:
            f.write(
                "No exact SHA256 duplicates were found in the D1 manifest. "
                "This reduces one leakage concern, but it does not rule out near-duplicates, "
                "same-patient slices, resized duplicates, or source overlap with other datasets.\n\n"
            )
        else:
            f.write(
                "Exact duplicate SHA256 hashes were found. These must be investigated before training. "
                "Cross-split duplicates are especially serious because they can leak test information into training.\n\n"
            )

        if cross_split_groups:
            f.write("## Cross-Split Duplicate Groups\n\n")
            for idx, (sha, items) in enumerate(cross_split_groups.items(), start=1):
                f.write(f"### Group {idx}\n\n")
                f.write(f"- SHA256: `{sha}`\n\n")
                for item in items:
                    f.write(
                        f"- `{item['split']}` / `{item['class_label']}` / `{item['filepath']}`\n"
                    )
                f.write("\n")

        if cross_class_groups:
            f.write("## Cross-Class Duplicate Groups\n\n")
            for idx, (sha, items) in enumerate(cross_class_groups.items(), start=1):
                f.write(f"### Group {idx}\n\n")
                f.write(f"- SHA256: `{sha}`\n\n")
                for item in items:
                    f.write(
                        f"- `{item['split']}` / `{item['class_label']}` / `{item['filepath']}`\n"
                    )
                f.write("\n")

    print(f"Rows checked: {len(rows)}")
    print(f"Unique hashes: {len(by_hash)}")
    print(f"Duplicate hash groups: {duplicate_group_count}")
    print(f"Images in duplicate groups: {total_duplicate_images}")
    print(f"Cross-split duplicate groups: {len(cross_split_groups)}")
    print(f"Cross-class duplicate groups: {len(cross_class_groups)}")
    print(f"Report written to: {OUT_PATH}")


if __name__ == "__main__":
    main()
