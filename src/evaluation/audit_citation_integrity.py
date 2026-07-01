from pathlib import Path
import re


MANUSCRIPT = Path("reports/experiments/manuscript_draft_v1.md")
SEARCH_TABLE = Path("reports/experiments/references_search_table.md")
REFERENCE_LIST = Path("reports/experiments/reference_list_placeholders.md")
OUT = Path("reports/experiments/citation_integrity_audit.md")


REF_PATTERN = re.compile(r"REF-[A-Z]+-\d{3}")


def extract_refs(path: Path):
    if not path.exists():
        return set()
    return set(REF_PATTERN.findall(path.read_text(encoding="utf-8")))


def main():
    manuscript_refs = extract_refs(MANUSCRIPT)
    search_table_refs = extract_refs(SEARCH_TABLE)
    reference_list_refs = extract_refs(REFERENCE_LIST)

    missing_from_search_table = sorted(manuscript_refs - search_table_refs)
    missing_from_reference_list = sorted(manuscript_refs - reference_list_refs)

    unused_in_manuscript_from_search = sorted(search_table_refs - manuscript_refs)
    unused_in_manuscript_from_reference_list = sorted(reference_list_refs - manuscript_refs)

    lines = []
    lines.append("# Citation Integrity Audit")
    lines.append("")
    lines.append("## Purpose")
    lines.append("")
    lines.append("This audit checks whether citation placeholders used in the manuscript are traceable to the reference tracking files.")
    lines.append("")
    lines.append("## Files Checked")
    lines.append("")
    lines.append(f"- Manuscript: `{MANUSCRIPT}`")
    lines.append(f"- Reference search table: `{SEARCH_TABLE}`")
    lines.append(f"- Reference list placeholders: `{REFERENCE_LIST}`")
    lines.append("")
    lines.append("## Citation Placeholders Used in Manuscript")
    lines.append("")
    if manuscript_refs:
        for ref in sorted(manuscript_refs):
            lines.append(f"- `{ref}`")
    else:
        lines.append("No `REF-*` placeholders found in the manuscript.")
    lines.append("")

    lines.append("## Missing From Reference Search Table")
    lines.append("")
    if missing_from_search_table:
        for ref in missing_from_search_table:
            lines.append(f"- `{ref}`")
    else:
        lines.append("None. All manuscript citation placeholders are present in the reference search table.")
    lines.append("")

    lines.append("## Missing From Reference List Placeholders")
    lines.append("")
    if missing_from_reference_list:
        for ref in missing_from_reference_list:
            lines.append(f"- `{ref}`")
    else:
        lines.append("None. All manuscript citation placeholders are present in the reference list placeholder file.")
    lines.append("")

    lines.append("## Verified Status")
    lines.append("")
    if not missing_from_search_table and not missing_from_reference_list:
        lines.append("PASS: All manuscript citation placeholders are traceable.")
    else:
        lines.append("FAIL: Some manuscript citation placeholders are not traceable.")
    lines.append("")

    lines.append("## References Not Yet Used in Manuscript")
    lines.append("")
    lines.append("These references exist in the tracking files but have not yet been inserted into the manuscript. This is not automatically a problem.")
    lines.append("")
    lines.append("### Present in search table but not manuscript")
    lines.append("")
    if unused_in_manuscript_from_search:
        for ref in unused_in_manuscript_from_search:
            lines.append(f"- `{ref}`")
    else:
        lines.append("None.")
    lines.append("")

    lines.append("### Present in reference list but not manuscript")
    lines.append("")
    if unused_in_manuscript_from_reference_list:
        for ref in unused_in_manuscript_from_reference_list:
            lines.append(f"- `{ref}`")
    else:
        lines.append("None.")
    lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append("The manuscript should only use references that are present in both the reference search table and the reference list placeholder file.")
    lines.append("")
    lines.append("Unused references should not be forced into the manuscript unless they support a specific claim.")
    lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    print("")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
