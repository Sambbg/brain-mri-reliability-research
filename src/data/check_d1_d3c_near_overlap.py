from pathlib import Path
from collections import Counter
import pandas as pd

D1_MANIFEST = Path("data/processed/D1_manifest_deduplicated_phash.csv")
D3C_MANIFEST = Path("data/processed/D3C_selected_slices_manifest_phash.csv")

REPORT_PATH = Path("reports/datasets/D1_D3C_near_overlap_report.md")
OUT_CSV = Path("reports/datasets/D1_D3C_near_overlap_pairs.csv")

PHASH_THRESHOLD = 4


def hex_to_int(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    try:
        return int(value, 16)
    except ValueError:
        return None


def hamming_distance_hex(a, b):
    ai = hex_to_int(a)
    bi = hex_to_int(b)

    if ai is None or bi is None:
        return None

    return (ai ^ bi).bit_count()


def main():
    if not D1_MANIFEST.exists():
        raise FileNotFoundError(f"Missing D1 pHash manifest: {D1_MANIFEST}")

    if not D3C_MANIFEST.exists():
        raise FileNotFoundError(f"Missing D3C pHash manifest: {D3C_MANIFEST}")

    d1 = pd.read_csv(D1_MANIFEST)
    d3c = pd.read_csv(D3C_MANIFEST)

    if "phash" not in d1.columns:
        raise ValueError("D1 manifest missing phash column.")

    if "phash" not in d3c.columns:
        raise ValueError("D3C manifest missing phash column.")

    d1_rows = d1[d1["phash"].notna() & (d1["phash"].astype(str).str.len() > 0)].copy()
    d3c_rows = d3c[d3c["phash"].notna() & (d3c["phash"].astype(str).str.len() > 0)].copy()

    pairs = []
    distance_counts = Counter()

    total_comparisons = len(d1_rows) * len(d3c_rows)

    print(f"D1 rows: {len(d1_rows)}")
    print(f"D3C rows: {len(d3c_rows)}")
    print(f"Total comparisons: {total_comparisons}")

    d3c_records = list(d3c_rows.to_dict("records"))

    for i, d1_row in enumerate(d1_rows.to_dict("records")):
        if i % 500 == 0:
            print(f"Comparing D1 row {i}/{len(d1_rows)}")

        d1_phash = d1_row.get("phash", "")

        for d3c_row in d3c_records:
            d3c_phash = d3c_row.get("phash", "")
            dist = hamming_distance_hex(d1_phash, d3c_phash)

            if dist is None:
                continue

            if dist <= PHASH_THRESHOLD:
                distance_counts[dist] += 1

                pairs.append({
                    "phash_distance": dist,
                    "d1_dataset_id": d1_row.get("dataset_id", ""),
                    "d1_split": d1_row.get("split", ""),
                    "d1_class_label": d1_row.get("class_label", ""),
                    "d1_filepath": d1_row.get("filepath", ""),
                    "d1_phash": d1_phash,
                    "d3c_dataset_id": d3c_row.get("dataset_id", ""),
                    "d3c_patient_id": d3c_row.get("patient_id", ""),
                    "d3c_series_instance_uid": d3c_row.get("series_instance_uid", ""),
                    "d3c_series_description": d3c_row.get("series_description", ""),
                    "d3c_slice_index_in_sorted_series": d3c_row.get("slice_index_in_sorted_series", ""),
                    "d3c_output_image_path": d3c_row.get("output_image_path", ""),
                    "d3c_label": d3c_row.get("label", ""),
                    "d3c_phash": d3c_phash,
                    "cross_class_pair": str(d1_row.get("class_label", "")) != str(d3c_row.get("label", "")),
                })

    out_df = pd.DataFrame(pairs)

    if not out_df.empty:
        out_df = out_df.sort_values(
            by=["phash_distance", "d1_class_label", "d3c_patient_id", "d1_filepath"],
            ascending=[True, True, True, True],
        )

    out_df.to_csv(OUT_CSV, index=False)

    cross_class_count = int(out_df["cross_class_pair"].sum()) if not out_df.empty else 0

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# D1-D3C pHash Near-Overlap Report\n\n")

        f.write("## Input\n\n")
        f.write(f"- D1 pHash manifest: `{D1_MANIFEST}`\n")
        f.write(f"- D3C pHash manifest: `{D3C_MANIFEST}`\n")
        f.write(f"- D1 rows compared: {len(d1_rows)}\n")
        f.write(f"- D3C rows compared: {len(d3c_rows)}\n")
        f.write(f"- Total comparisons: {total_comparisons}\n")
        f.write(f"- pHash Hamming distance threshold: <= {PHASH_THRESHOLD}\n\n")

        f.write("## Summary\n\n")
        f.write(f"- Near-overlap pairs found: {len(out_df)}\n")
        f.write(f"- Cross-class near-overlap pairs: {cross_class_count}\n")
        f.write(f"- Output CSV: `{OUT_CSV}`\n\n")

        f.write("## Distance Counts\n\n")
        if distance_counts:
            for distance, count in sorted(distance_counts.items()):
                f.write(f"- Distance {distance}: {count} pairs\n")
        else:
            f.write("- No near-overlap pairs found.\n")

        f.write("\n## Interpretation\n\n")
        if len(out_df) == 0:
            f.write(
                "No pHash near-overlap was detected between D1 and D3C at the selected threshold. "
                "This supports treating D3C as visually distinct from D1 for the planned domain-shift "
                "confidence analysis, although pHash cannot prove patient-level independence.\n"
            )
        else:
            f.write(
                "pHash near-overlap was detected between D1 and D3C. These pairs may represent visual similarity, "
                "hash collisions, shared source images, or similar anatomical slices. Manual review is required before "
                "making strong external-domain claims.\n"
            )

        f.write(
            "\nD3C remains a glioma-focused domain-shift dataset, not a full four-class external validation dataset.\n"
        )

        if not out_df.empty:
            f.write("\n## Example Near-Overlap Pairs\n\n")

            for idx, row in out_df.head(50).iterrows():
                f.write(f"### Pair {idx + 1}\n\n")
                f.write(f"- Distance: {row['phash_distance']}\n")
                f.write(
                    f"- D1: `{row['d1_split']}` / `{row['d1_class_label']}` / "
                    f"`{row['d1_filepath']}`\n"
                )
                f.write(
                    f"- D3C: `{row['d3c_patient_id']}` / `{row['d3c_series_description']}` / "
                    f"`{row['d3c_output_image_path']}`\n"
                )
                f.write(f"- Cross-class pair: `{row['cross_class_pair']}`\n\n")

    print(f"D1 rows compared: {len(d1_rows)}")
    print(f"D3C rows compared: {len(d3c_rows)}")
    print(f"Total comparisons: {total_comparisons}")
    print(f"Near-overlap pairs found: {len(out_df)}")
    print(f"Cross-class near-overlap pairs: {cross_class_count}")
    print(f"Report written to: {REPORT_PATH}")
    print(f"Pairs CSV written to: {OUT_CSV}")


if __name__ == "__main__":
    main()
