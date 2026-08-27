#!/usr/bin/env bash
#
# Apply the three outstanding repo housekeeping items:
#   1. Record the re-run overlap audit and the plane sensitivity result in CLAUDE.md
#   2. Correct the stale skull-stripping reference in the D3C exclusion report
#   3. Add the superseded audit count to SUPERSEDED_ARTIFACTS.md
#
# Idempotent: each step checks whether it has already been applied and skips if so.
#
# Run from the repo root:
#     bash scripts/apply_repo_housekeeping.sh

set -euo pipefail

if [ ! -d .git ] || [ ! -f CLAUDE.md ]; then
    echo "Run this from the repo root (~/research)." >&2
    exit 1
fi

echo "== 1. CLAUDE.md =="
if grep -q "21,529,910" CLAUDE.md; then
    echo "   already recorded, skipping"
else
    cat >> CLAUDE.md << 'EOF'

- **D1?D3C overlap audit re-run on the full cohort (August 2026).** The earlier audit
  covered the superseded 569-patient cohort and reported 19,951,985 comparisons, leaving
  roughly 205 slices unaudited. Re-run over all 3,070 converted slices: **21,529,910
  comparisons, 0 exact overlaps, 7 within-class glioma?glioma near-duplicate pairs, 0
  cross-class**. A separate check confirmed no pHash value is shared between patients, so
  all within-D3C collisions are between adjacent central slices of the same series. The
  analysis cohort is 3,050 slices from 610 patients, after excluding 4 non-axial series
  from the 614 converted. The audit therefore covers a superset of the evaluated data.
- **Imaging plane ruled out as a confound.** Eleven patients carry series more than 10
  degrees from axial. Dropping them shifts the mean D3C glioma prediction rate by at most
  0.0052 and preserves the architecture ordering, against a between-architecture spread of
  0.41. See `scripts/d3c_plane_sensitivity.py` and
  `reports/experiments/consolidated/tables/d3c_plane_sensitivity.md`.
- **Both D3C preprocessing confounds are now closed by measurement**, not argument: skull
  stripping (withdrawn, `reports/datasets/D3C_skull_stripping_audit.md`) and imaging plane
  (bounded, above). Residual differences ? CaPTk co-registration, resampling and intensity
  normalisation ? remain uncontrolled and belong in the limitations.
EOF
    echo "   appended"
fi

echo "== 2. D3C exclusion report =="
REPORT=reports/datasets/D3C_cohort_exclusion_report.md
if [ ! -f "$REPORT" ]; then
    echo "   $REPORT not found, skipping"
elif grep -q "superseded" "$REPORT"; then
    echo "   already corrected, skipping"
else
    cat >> "$REPORT" << 'EOF'

## Note (August 2026)

Two statements in the Limitation section above are superseded.

**Skull stripping.** The claim that a skull-stripping confound "applies to the whole
cohort" is withdrawn. Measured across 40 randomly sampled D3C series against 40 matched D1
glioma images, no D3C image has a masked background; the air region is 26.2% exactly zero
at the median where a mask would give a value near 1.0, image corners are 54.0% non-zero,
and 25.6% of outer-ring pixels exceed the brain-core median, which is the T1 scalp-fat
signature. The same measurements taken from the source DICOM match the converted PNGs,
ruling out the conversion step. D3C retains extracranial anatomy throughout and is less
masked than D1 (air exactly-zero 0.262 versus 0.373). See
`reports/datasets/D3C_skull_stripping_audit.md`.

**Plane sensitivity analysis.** The recommendation above to "report both" cohorts has been
implemented. Dropping the 11 oblique patients shifts the mean D3C glioma prediction rate by
at most 0.0052 across the five-seed sweep and preserves the architecture ordering, against
a between-architecture spread of 0.41. Imaging plane is therefore not a plausible
explanation for the shifted-domain separation. The full cohort is retained for the primary
analysis and the sensitivity result is reported alongside it. See
`scripts/d3c_plane_sensitivity.py` and
`reports/experiments/consolidated/tables/d3c_plane_sensitivity.md`.

What stands: excluding non-axial series removes a plane confound but does not make D3C a
four-class external validation set, and obliquity below the 10-degree threshold remains
uncontrolled.
EOF
    echo "   appended"
fi

echo "== 3. SUPERSEDED_ARTIFACTS.md =="
SUP=reports/experiments/SUPERSEDED_ARTIFACTS.md
if [ ! -f "$SUP" ]; then
    echo "   $SUP not found, skipping"
elif grep -q "19,951,985" "$SUP"; then
    echo "   already recorded, skipping"
else
    cat >> "$SUP" << 'EOF'

---

## Superseded audit figures

| Figure | Where it appears | Replacement |
|---|---|---|
| D1?D3C: 19,951,985 comparisons | Proposal Table 3.4, §3.4.3, §4.1 | **21,529,910** over 3,070 slices |
| D3C cohort 569 patients / 2,845 slices | Throughout the proposal | **610 patients / 3,050 slices** analysed; 614 / 3,070 audited |
| "approximately twenty million comparisons" | Proposal §5.1 | more than twenty-one million |

The original D1?D3C audit was run against the earlier 569-patient cohort, so roughly 205
slices from 41 patients were never compared against D1. The re-run covers all 3,070
converted slices, a superset of the 3,050 evaluated.

## Claims closed by measurement since the sweep

| Claim | Status |
|---|---|
| D3C is skull-stripped and therefore differs systematically from D1 | **Withdrawn.** D3C retains extracranial anatomy and is less masked than D1. |
| Imaging plane may explain the D3C shifted-domain separation | **Ruled out.** Dropping 11 oblique patients shifts the mean glioma rate by ?0.0052 and preserves the ordering. |
EOF
    echo "   appended"
fi

echo
echo "Done. Review with: git diff"
echo
echo "Then:"
echo "  git add CLAUDE.md $REPORT $SUP"
echo "  git commit -m 'Record the re-run audit and plane sensitivity across the handover docs'"
echo "  git push origin main"
