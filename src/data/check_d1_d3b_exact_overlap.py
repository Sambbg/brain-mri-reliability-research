from pathlib import Path
import pandas as pd

D1_MANIFEST = Path("data/processed/D1_manifest_deduplicated.csv")
D3B_MANIFEST = Path("data/processed/D3B_selected_slices_manifest_phash.csv")

REPORT_PATH = Path("reports/datasets/D1_D3B_exact_overlap_report.md")
OUT_CSV = Path("reports/datasets/D1_D3B_exact_overlap_pairs.csv")


def main():
    if not D1_MANIFEST.exists():
        raise FileNotFoundError(f"Missing D1 manifest: {D1_MANIFEST}")

    if not D3B_MANIFEST.exists():
        raise FileNotFoundError(f"Missing D3B manifest: {D3B_MANIFEST}")

    d1 = pd.read_csv(D1_MANIFEST)
    d3b = pd.read_csv(D3B_MANIFEST)

    if "sha256" not in d1.columns:
        raise ValueError("D1 manifest missing sha256 column.")

    if "sha256_recomputed" not in d3b.columns:
        raise ValueError("D3B manifest missing sha256_recomputed column.")

    d1_hashes = set(d1["sha256"].dropna().astype(str))
    d3b_hashes = set(d3b["sha256_recomputed"].dropna().astype(str))

    shared_hashes = sorted(d1_hashes.intersection(d3b_hashes))

    rows = []

    if shared_hashes:
        d1_shared = d1[d1["sha256"].astype(str).isin(shared_hashes)].copy()
        d3b_shared = d3b[d3b["sha256_recomputed"].astype(str).isin(shared_hashes)].copy()

        for _, d1_row in d1_shared.iterrows():
            h = str(d1_row["sha256"])
            matches = d3b_shared[d3b_shared["sha256_recomputed"].astype(str) == h]

            for _, d3b_row in matches.iterrows():
                rows.append({
                    "sha256": h,
                    "d1_split": d1_row.get("split", ""),
                    "d1_class_label": d1_row.get("class_label", ""),
                    "d1_filepath": d1_row.get("filepath", ""),
                    "d3b_patient_id": d3b_row.get("patient_id", ""),
                    "d3b_series_instance_uid": d3b_row.get("series_instance_uid", ""),
                    "d3b_series_description": d3b_row.get("series_description", ""),
                    "d3b_output_image_path": d3b_row.get("output_image_path", ""),
                    "d3b_label": d3b_row.get("label", ""),
                })

    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUT_CSV, index=False)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# D1-D3B Exact Overlap Report\n\n")

        f.write("## Input\n\n")
        f.write(f"- D1 manifest: `{D1_MANIFEST}`\n")
        f.write(f"- D3B manifest: `{D3B_MANIFEST}`\n")
        f.write(f"- D1 rows: {len(d1)}\n")
        f.write(f"- D3B rows: {len(d3b)}\n\n")

        f.write("## Summary\n\n")
        f.write(f"- Shared SHA256 hashes: {len(shared_hashes)}\n")
        f.write(f"- Exact overlap pairs: {len(out_df)}\n")
        f.write(f"- Output CSV: `{OUT_CSV}`\n\n")

        f.write("## Interpretation\n\n")
        if len(out_df) == 0:
            f.write(
                "No exact SHA256 overlap was detected between D1 deduplicated images "
                "and D3B converted central-slice PNG images. This is expected because "
                "D3B images were generated from DICOM conversion and are unlikely to be "
                "byte-identical to D1 JPEG images. Near-overlap testing using perceptual "
                "hashes is still required.\n"
            )
        else:
            f.write(
                "Exact SHA256 overlap was detected. This would be serious and must be "
                "investigated before using D3B for evaluation.\n"
            )

        if len(out_df) > 0:
            f.write("\n## Example Exact Overlap Pairs\n\n")
            for idx, row in out_df.head(20).iterrows():
                f.write(f"### Pair {idx + 1}\n\n")
                f.write(f"- SHA256: `{row['sha256']}`\n")
                f.write(f"- D1: `{row['d1_split']}` / `{row['d1_class_label']}` / `{row['d1_filepath']}`\n")
                f.write(f"- D3B: `{row['d3b_patient_id']}` / `{row['d3b_series_description']}` / `{row['d3b_output_image_path']}`\n\n")

    print(f"D1 rows: {len(d1)}")
    print(f"D3B rows: {len(d3b)}")
    print(f"Shared SHA256 hashes: {len(shared_hashes)}")
    print(f"Exact overlap pairs: {len(out_df)}")
    print(f"Report written to: {REPORT_PATH}")
    print(f"Pairs CSV written to: {OUT_CSV}")


if __name__ == "__main__":
    main()

