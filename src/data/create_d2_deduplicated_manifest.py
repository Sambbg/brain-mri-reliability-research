from pathlib import Path
import csv
from collections import defaultdict

IN_PATH = Path("data/processed/D2_manifest.csv")
OUT_PATH = Path("data/processed/D2_manifest_deduplicated.csv")
REPORT_PATH = Path("reports/datasets/D2_deduplication_report.md")


def load_manifest(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Manifest not found: {path}")

    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    rows = load_manifest(IN_PATH)

    by_hash = defaultdict(list)
    for row in rows:
        by_hash[row["sha256"]].append(row)

    kept_rows = []
    removed_rows = []

    for sha, items in sorted(by_hash.items()):
        # Deterministic rule:
        # keep the first item after sorting by source_split, class_label, filepath.
        # This preserves reproducibility.
        sorted_items = sorted(
            items,
            key=lambda r: (r["source_split"], r["class_label"], r["filepath"])
        )

        kept_rows.append(sorted_items[0])

        for duplicate in sorted_items[1:]:
            removed = dict(duplicate)
            removed["duplicate_of_filepath"] = sorted_items[0]["filepath"]
            removed_rows.append(removed)

    fieldnames = [
        "dataset_id",
        "source_split",
        "class_label",
        "raw_class_label",
        "filepath",
        "filename",
        "extension",
        "file_size_bytes",
        "width",
        "height",
        "mode",
        "sha256",
    ]

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(kept_rows)

    original_count = len(rows)
    deduplicated_count = len(kept_rows)
    removed_count = len(removed_rows)

    split_counts = defaultdict(int)
    class_counts = defaultdict(int)

    for row in kept_rows:
        split_counts[row["source_split"]] += 1
        class_counts[(row["source_split"], row["class_label"])] += 1

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# D2 Deduplication Report\n\n")

        f.write("## Input and Output\n\n")
        f.write(f"- Input manifest: `{IN_PATH}`\n")
        f.write(f"- Output manifest: `{OUT_PATH}`\n\n")

        f.write("## Summary\n\n")
        f.write(f"- Original rows: {original_count}\n")
        f.write(f"- Deduplicated rows: {deduplicated_count}\n")
        f.write(f"- Removed duplicate rows: {removed_count}\n")
        f.write(f"- Unique SHA256 hashes retained: {len(by_hash)}\n\n")

        f.write("## Deduplication Rule\n\n")
        f.write(
            "Rows were grouped by exact SHA256 hash. For each duplicate group, "
            "one row was retained using a deterministic sort by source split, class label, and filepath. "
            "All remaining rows in the group were excluded from the deduplicated manifest.\n\n"
        )

        f.write("## Deduplicated Split Counts\n\n")
        for split, count in sorted(split_counts.items()):
            f.write(f"- {split}: {count}\n")

        f.write("\n## Deduplicated Class Counts\n\n")
        for (split, class_label), count in sorted(class_counts.items()):
            f.write(f"- {split} / {class_label}: {count}\n")

        f.write("\n## Interpretation\n\n")
        f.write(
            "The original D2 manifest contains exact duplicate images, including duplicates crossing "
            "the original train/test split. Therefore, the original BRISC train/test split should not be "
            "treated as a clean independent evaluation split. The deduplicated manifest should be used for "
            "future D2 analysis, but near-duplicate and D1-vs-D2 overlap checks are still required.\n"
        )

    print(f"Original rows: {original_count}")
    print(f"Deduplicated rows: {deduplicated_count}")
    print(f"Removed duplicate rows: {removed_count}")
    print(f"Output manifest: {OUT_PATH}")
    print(f"Report: {REPORT_PATH}")

    print("\nDeduplicated class counts:")
    for (split, class_label), count in sorted(class_counts.items()):
        print(f"{split} / {class_label}: {count}")


if __name__ == "__main__":
    main()
