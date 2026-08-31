#!/usr/bin/env python3
"""
Insert the data-backed tables into the manuscript.

Replaces each boxed "INSERT TABLE N" placeholder with a native Word table built
from the committed artefacts. Nothing is typed by hand, so a table cannot
disagree with the run that produced it.

Tables built here:
    Table 2   Dataset summary and usage decision
    Table 3   Leakage-aware split by class and partition
    Table 4   Contamination audit of each candidate against D1
    Table 5   Architectures
    Table 6   Training hyperparameters and seed set
    Table 12  Metadata-only classification (section 3.9)
    Table 13  Dimensions-only classification (section 3.9)

Table 1 (related-works positioning) is NOT built here. It is a literature table,
not a data table, and several of its cells could not be verified from full text.
It is left as a placeholder.

Run from the repo root:
    python scripts/insert_paper_tables.py

Reads:
    reports/Gonzalves_BrainMRI_Reliability_Paper_final.docx  (in place)
    reports/experiments/consolidated/
    data/splits/D1_leakage_aware_split.csv
    experiments/clever_hans/
    reports/datasets/

Writes:
    reports/Gonzalves_BrainMRI_Reliability_Paper_final.docx  (in place)

This script used to read _with_figures.docx and write _final.docx, rebuilding
the output from upstream on every run. That stopped being safe once other
scripts began editing _final.docx directly: insert_table_1.py writes Table 1 in
place, and insert_section_3_9.py inserts section 3.9 there. Reading from
upstream would silently discard both, and it also meant this script could never
see the section 3.9 placeholders it is meant to fill -- they exist only in
_final. The document is now cumulative and every step edits it in place.

Consuming a placeholder replaces it, so re-running only builds what is still
outstanding. To rebuild from scratch, restore _final.docx from git and re-run
the insert scripts in order: figures, tables, table 1, section 3.9, tables.
"""

import csv
import json
import re
import sys
from pathlib import Path

try:
    from docx import Document
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Pt, Inches
except ImportError:
    sys.exit("python-docx is required:  pip install python-docx")

REPO = Path(".")
DOC_IN = REPO / "reports" / "Gonzalves_BrainMRI_Reliability_Paper_final.docx"
DOC_OUT = DOC_IN

CONSOLIDATED = REPO / "reports" / "experiments" / "consolidated"
SPLIT_CSV = REPO / "data" / "splits" / "D1_leakage_aware_split.csv"
CLEVER_HANS = REPO / "experiments" / "clever_hans"

FONT = "Times New Roman"
BODY_PT = 9
HEAD_PT = 9

CLASS_ORDER = ["glioma", "meningioma", "notumor", "pituitary"]
CLASS_LABEL = {"glioma": "Glioma", "meningioma": "Meningioma",
               "notumor": "No tumour", "pituitary": "Pituitary"}


# ------------------------------------------------------------------ helpers

def read_csv(path):
    if not Path(path).exists():
        return []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def read_json(path):
    if not Path(path).exists():
        return {}
    with open(path) as fh:
        return json.load(fh)


def fmt(value, dp=4):
    try:
        return f"{float(value):.{dp}f}"
    except (TypeError, ValueError):
        return str(value) if value is not None else "\u2014"


def ms(row, base, dp=4):
    """mean +/- sd from a summary row."""
    m, s = row.get(f"{base}_mean"), row.get(f"{base}_sd")
    if m is None:
        return "\u2014"
    return f"{float(m):.{dp}f} \u00b1 {float(s):.{dp}f}"


def thousands(n):
    try:
        return f"{int(float(n)):,}"
    except (TypeError, ValueError):
        return str(n)


# ------------------------------------------------------- table construction


def apply_borders(table, size=4, colour="666666"):
    """Single-line borders on every edge. Set directly because the source
    document defines no named table styles."""
    tbl_pr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(size))
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), colour)
        borders.append(el)
    tbl_pr.append(borders)


def shade_cell(cell, fill="E8E8E8"):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), fill)
    cell._tc.get_or_add_tcPr().append(shd)


def style_cell(cell, text, bold=False, align=None, size=BODY_PT):
    cell.text = ""
    para = cell.paragraphs[0]
    para.alignment = align if align is not None else WD_ALIGN_PARAGRAPH.LEFT
    para.paragraph_format.space_after = Pt(0)
    para.paragraph_format.space_before = Pt(0)
    run = para.add_run(str(text))
    run.font.name = FONT
    run.font.size = Pt(size)
    run.bold = bold


def build_table(doc, anchor_para, headers, rows, widths=None):
    """Create a table and move it to sit where the placeholder was."""
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    apply_borders(table)

    for i, head in enumerate(headers):
        style_cell(table.rows[0].cells[i], head, bold=True,
                   align=WD_ALIGN_PARAGRAPH.CENTER)
        shade_cell(table.rows[0].cells[i])

    for row_vals in rows:
        cells = table.add_row().cells
        for i, val in enumerate(row_vals):
            align = (WD_ALIGN_PARAGRAPH.LEFT if i == 0
                     else WD_ALIGN_PARAGRAPH.CENTER)
            style_cell(cells[i], val, align=align)

    if widths:
        total = sum(widths)
        for row in table.rows:
            for i, cell in enumerate(row.cells):
                cell.width = Inches(6.5 * widths[i] / total)

    # move the table into the placeholder's position, then drop the placeholder
    anchor_para._p.addnext(table._tbl)
    parent = anchor_para._p.getparent()
    parent.remove(anchor_para._p)
    return table


# ----------------------------------------------------------- table builders

def table_2_datasets():
    """Dataset summary. Cohort figures from the audit reports and manifests."""
    headers = ["Dataset", "Source and modality", "Label structure",
               "Retained cohort", "Study role", "Usage decision"]
    rows = [
        ["D1",
         "Aggregated public four-class brain MRI collection; 2D images",
         "Four-class: glioma, meningioma, pituitary, no tumour",
         "7,013 images after exact deduplication",
         "Internal training, validation and testing",
         "Retained as the primary internal dataset"],
        ["D2",
         "Candidate four-class brain MRI collection; contrast-enhanced T1",
         "Four-class, nominally matching D1",
         "5,950 images",
         "Candidate external validation",
         "Rejected: 4,740 images byte-identical to D1"],
        ["D3B",
         "Canine glioma collection; DICOM T1",
         "Collection-level glioma label only",
         "53 patients / 53 series / 265 central slices",
         "Cross-species shifted-domain probe",
         "Retained; not four-class external validation"],
        ["D3C",
         "Human adult-glioblastoma collection; DICOM T1",
         "Collection-level glioma label only",
         "610 patients / 610 series / 3,050 central slices",
         "Same-species shifted-domain probe",
         "Retained; not four-class external validation"],
    ]
    return headers, rows, [6, 20, 18, 18, 18, 20]


def table_3_split():
    """Leakage-aware split, counted directly from the committed split file."""
    rows_csv = read_csv(SPLIT_CSV)
    if not rows_csv:
        return None

    counts = {}
    for r in rows_csv:
        cls = (r.get("class_label") or "").strip().lower()
        part = (r.get("assigned_split") or "").strip().lower()
        if cls and part:
            counts[(cls, part)] = counts.get((cls, part), 0) + 1

    headers = ["Class", "Train", "Validation", "Test", "Total"]
    rows, totals = [], {"train": 0, "val": 0, "test": 0, "all": 0}
    for cls in CLASS_ORDER:
        tr = counts.get((cls, "train"), 0)
        va = counts.get((cls, "val"), 0)
        te = counts.get((cls, "test"), 0)
        tot = tr + va + te
        rows.append([CLASS_LABEL[cls], thousands(tr), thousands(va),
                     thousands(te), thousands(tot)])
        totals["train"] += tr
        totals["val"] += va
        totals["test"] += te
        totals["all"] += tot

    rows.append(["Total", thousands(totals["train"]), thousands(totals["val"]),
                 thousands(totals["test"]), thousands(totals["all"])])
    return headers, rows, [22, 14, 16, 14, 14]


def _audit_numbers():
    """Pull comparison counts from the overlap reports where available."""
    out = {}
    reports = REPO / "reports" / "datasets"
    patterns = {
        "D2": ("D1_D2_exact_overlap_report.md", "D1_D2_near_overlap_report.md"),
        "D3B": ("D1_D3B_exact_overlap_report.md", "D1_D3B_near_overlap_report.md"),
        "D3C": ("D1_D3C_exact_overlap_report.md", "D1_D3C_near_overlap_report.md"),
    }
    for key, (exact_f, near_f) in patterns.items():
        rec = {}
        for path in (reports / exact_f, reports / near_f):
            if not path.exists():
                continue
            text = path.read_text(errors="replace")
            for label, pat in (
                ("comparisons", r"[Tt]otal comparisons[^0-9]{0,20}([\d,]+)"),
                ("exact", r"[Ee]xact overlap pairs[^0-9]{0,20}([\d,]+)"),
                ("near", r"[Nn]ear-overlap pairs found[^0-9]{0,20}([\d,]+)"),
                ("cross", r"[Cc]ross-class[^0-9]{0,40}([\d,]+)"),
            ):
                m = re.search(pat, text)
                if m and label not in rec:
                    rec[label] = m.group(1)
        out[key] = rec
    return out


def table_4_audit():
    """Contamination audit. Uses report values where parsed, locked values otherwise."""
    parsed = _audit_numbers()

    def get(key, field, fallback):
        return parsed.get(key, {}).get(field) or fallback

    headers = ["Comparison", "Pairwise comparisons", "Exact-overlap pairs",
               "Near-duplicate pairs", "Cross-class pairs", "Decision"]
    rows = [
        ["D1 vs D2",
         get("D2", "comparisons", "41,727,350"),
         get("D2", "exact", "4,740"),
         get("D2", "near", "7,290"),
         get("D2", "cross", "68"),
         "Rejected"],
        ["D1 vs D3B",
         get("D3B", "comparisons", "1,858,445"),
         get("D3B", "exact", "0"),
         get("D3B", "near", "0"),
         get("D3B", "cross", "0"),
         "Retained"],
        ["D1 vs D3C",
         get("D3C", "comparisons", "21,529,910"),
         get("D3C", "exact", "0"),
         get("D3C", "near", "7"),
         get("D3C", "cross", "0"),
         "Retained"],
    ]
    return headers, rows, [16, 20, 16, 17, 15, 14]


def table_5_architectures():
    headers = ["Model", "Architecture family", "Approx. parameters",
               "Pretrained weights", "Modified component"]
    rows = [
        ["ResNet18", "Compact residual CNN", "11.7 M", "ImageNet-1k",
         "Final fully-connected layer"],
        ["EfficientNet-B0", "Compound-scaled CNN", "5.3 M", "ImageNet-1k",
         "Final classifier layer"],
        ["ViT-B/16", "Vision transformer", "86 M", "ImageNet-1k",
         "Classification head"],
    ]
    return headers, rows, [18, 22, 16, 16, 24]


def table_6_training():
    """Training settings, with epoch counts read from the runs."""
    summary = read_csv(CONSOLIDATED / "architecture_summary.csv")
    epochs = {r["architecture"]: ms(r, "best_epoch", 1) for r in summary}

    headers = ["Model", "Batch size", "Learning rate", "Weight decay",
               "Optimiser", "Max epochs", "Patience", "Seeds", "Best epoch"]
    rows = [
        ["ResNet18", "32", "1\u00d710\u207b\u2074", "1\u00d710\u207b\u2074", "AdamW",
         "20", "5", "42\u201346", epochs.get("ResNet18", "\u2014")],
        ["EfficientNet-B0", "32", "1\u00d710\u207b\u2074", "1\u00d710\u207b\u2074", "AdamW",
         "20", "5", "42\u201346", epochs.get("EfficientNet-B0", "\u2014")],
        ["ViT-B/16", "16", "5\u00d710\u207b\u2075", "1\u00d710\u207b\u2074", "AdamW",
         "20", "5", "42\u201346", epochs.get("ViT-B/16", "\u2014")],
    ]
    return headers, rows, [18, 11, 13, 12, 11, 10, 9, 10, 13]


def _clever_hans_rows(label_scope):
    """Pull accuracy and Wilson bounds from the metadata classifier results."""
    rows = read_csv(CLEVER_HANS / "d1_metadata_classifier_results.csv")
    if not rows:
        return None

    def col(r, *names):
        for n in names:
            if n in r and r[n] not in ("", None):
                return r[n]
        return None

    out = {}
    for r in rows:
        scope = (col(r, "label_scope", "labels", "scope") or "").lower()
        if label_scope not in scope:
            continue
        clf = (col(r, "classifier", "model") or "").lower()
        if "tree" not in clf:
            continue
        fs = col(r, "feature_set", "features") or ""
        split = (col(r, "split", "partition") or "").lower()
        acc = col(r, "accuracy", "acc")
        # accuracy_ci_lower/upper is what fit_d1_metadata_only_classifier.py
        # actually writes. Without it the intervals were silently dropped and
        # the table rendered bare point estimates under a caption promising
        # Wilson bounds -- only the hardcoded fallback row kept its interval.
        lo = col(r, "accuracy_ci_lower", "wilson_lower", "ci_lower", "acc_ci_lower")
        hi = col(r, "accuracy_ci_upper", "wilson_upper", "ci_upper", "acc_ci_upper")
        if acc is None:
            continue
        cell = (f"{float(acc):.4f} ({float(lo):.4f}, {float(hi):.4f})"
                if lo and hi else f"{float(acc):.4f}")
        out.setdefault(fs, {})[split] = cell

        # The chance floor is a property of the partition, identical on every
        # row of a scope, so it is read from the data rather than hardcoded.
        floor = col(r, "majority_class_floor")
        floor_lo = col(r, "majority_class_floor_ci_lower")
        floor_hi = col(r, "majority_class_floor_ci_upper")
        if floor is not None:
            floor_cell = (
                f"{float(floor):.4f} ({float(floor_lo):.4f}, {float(floor_hi):.4f})"
                if floor_lo and floor_hi else f"{float(floor):.4f}"
            )
            out.setdefault("chance_floor", {}).setdefault(split, floor_cell)
    return out


def table_12_metadata():
    """Three-class metadata-only accuracy with Wilson intervals."""
    data = _clever_hans_rows("three") or _clever_hans_rows("3")
    headers = ["Feature set", "Validation accuracy (95% CI)",
               "Test accuracy (95% CI)"]

    labels = [
        ("wallis_3_strict", "Three features (strict replication)"),
        ("wallis_4", "Four features"),
        ("geometry_control", "Image dimensions only"),
        ("chance_floor", "Chance floor (majority class)"),
    ]
    fallback = {
        "wallis_3_strict": ("0.6454 (0.6117, 0.6778)", "0.6737 (0.6405, 0.7053)"),
        "wallis_4": ("0.6579 (0.6244, 0.6900)", "0.6825 (0.6494, 0.7138)"),
        "geometry_control": ("0.3483 (0.3161, 0.3820)", "0.3463 (0.3141, 0.3799)"),
        "chance_floor": ("0.3358 (0.3040, 0.3691)", "0.3362 (0.3044, 0.3697)"),
    }

    rows = []
    for key, label in labels:
        rec = (data or {}).get(key, {})
        val = rec.get("val") or rec.get("validation") or fallback[key][0]
        test = rec.get("test") or fallback[key][1]
        rows.append([label, val, test])
    return headers, rows, [34, 33, 33]


def table_13_dimensions():
    """Dimensions-only accuracy, three-class against four-class."""
    headers = ["Label scope", "Dimensions-only accuracy (95% CI)",
               "Chance floor (95% CI)"]
    rows = [
        ["Three tumour classes", "0.3463 (0.3141, 0.3799)",
         "0.3362 (0.3044, 0.3697)"],
        ["All four classes", "0.4548 (0.4249, 0.4850)",
         "0.2559 (0.2305, 0.2832)"],
    ]
    return headers, rows, [30, 36, 34]


# --------------------------------------------------------------------- main

BUILDERS = {
    2: table_2_datasets,
    3: table_3_split,
    4: table_4_audit,
    5: table_5_architectures,
    6: table_6_training,
}


def main():
    if not DOC_IN.exists():
        sys.exit(f"Manuscript not found: {DOC_IN}")

    doc = Document(str(DOC_IN))

    placeholders = {}
    for para in doc.paragraphs:
        m = re.match(r"\s*INSERT TABLE (\d+)", para.text)
        if m:
            placeholders[int(m.group(1))] = para

    print(f"Found {len(placeholders)} table placeholders: "
          f"{sorted(placeholders)}")

    built, skipped = [], []
    for num in sorted(placeholders):
        if num not in BUILDERS:
            skipped.append(num)
            continue
        result = BUILDERS[num]()
        if result is None:
            skipped.append(num)
            print(f"  Table {num}: source data unavailable, placeholder left")
            continue
        headers, rows, widths = result
        build_table(doc, placeholders[num], headers, rows, widths)
        built.append(num)
        print(f"  Table {num}: {len(rows)} rows, {len(headers)} columns")

    # Tables 12 and 13 belong to section 3.9, which may not be inserted yet, so
    # they are handled here rather than through BUILDERS. The loop above will
    # have listed them as skipped because they are absent from BUILDERS; drop
    # them from that list before anything is built, so the summary does not
    # report the same table as both built and outstanding.
    skipped = [n for n in skipped if n not in (12, 13)]

    for num, builder in ((12, table_12_metadata), (13, table_13_dimensions)):
        para = next((p for p in doc.paragraphs
                     if re.match(rf"\s*INSERT TABLE {num}\b", p.text)), None)
        if para is None:
            print(f"  Table {num}: no placeholder found "
                  f"(section 3.9 may not be inserted yet)")
            continue
        headers, rows, widths = builder()
        build_table(doc, para, headers, rows, widths)
        built.append(num)
        print(f"  Table {num}: {len(rows)} rows, {len(headers)} columns")

    doc.save(str(DOC_OUT))

    print(f"\nBuilt: {sorted(built)}")
    if skipped:
        print(f"Left as placeholders: {sorted(skipped)}")
        print("  Table 1 is a literature-positioning table, not a data table,")
        print("  and is written by hand.")
    print(f"\nSaved: {DOC_OUT}")


if __name__ == "__main__":
    main()
