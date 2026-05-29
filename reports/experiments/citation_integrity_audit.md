# Citation Integrity Audit

## Purpose

This audit checks whether citation placeholders used in the manuscript are traceable to the reference tracking files.

## Files Checked

- Manuscript: `reports/experiments/manuscript_draft_v1.md`
- Reference search table: `reports/experiments/references_search_table.md`
- Reference list placeholders: `reports/experiments/reference_list_placeholders.md`

## Citation Placeholders Used in Manuscript

- `REF-BMRI-001`
- `REF-BMRI-002`
- `REF-BMRI-003`
- `REF-BMRI-004`
- `REF-CAL-001`
- `REF-CAL-002`
- `REF-CAL-003`
- `REF-LEAK-001`
- `REF-LEAK-002`
- `REF-LEAK-003`
- `REF-LEAK-004`
- `REF-REPORT-001`
- `REF-SHIFT-001`
- `REF-SHIFT-002`
- `REF-SHIFT-003`

## Missing From Reference Search Table

None. All manuscript citation placeholders are present in the reference search table.

## Missing From Reference List Placeholders

None. All manuscript citation placeholders are present in the reference list placeholder file.

## Verified Status

PASS: All manuscript citation placeholders are traceable.

## References Not Yet Used in Manuscript

These references exist in the tracking files but have not yet been inserted into the manuscript. This is not automatically a problem.

### Present in search table but not manuscript

- `REF-REPORT-002`
- `REF-REPORT-003`
- `REF-SHIFT-004`
- `REF-UNC-001`
- `REF-UNC-002`
- `REF-UNC-003`
- `REF-UNC-004`
- `REF-UNC-005`

### Present in reference list but not manuscript

- `REF-REPORT-002`
- `REF-REPORT-003`
- `REF-SHIFT-004`
- `REF-UNC-001`
- `REF-UNC-002`
- `REF-UNC-003`
- `REF-UNC-004`
- `REF-UNC-005`

## Interpretation

The manuscript should only use references that are present in both the reference search table and the reference list placeholder file.

Unused references should not be forced into the manuscript unless they support a specific claim.
