"""
Replace the patient-level leakage caveat in section 2.2 with the measured figure.

Reads:  reports/Gonzalves_BrainMRI_Reliability_Paper_final.docx
Writes: reports/Gonzalves_BrainMRI_Reliability_Paper_final.docx  (in place)

The manuscript acknowledged that the leakage-aware split controls image-level
and group-level duplication rather than patient-level duplication, which was
correct but unquantified. The threshold sensitivity audit and the blind
adjudication that followed it now put a number on the residual: at a Hamming
distance of 6, one step looser than the threshold the split was built at, 371
within-class pairs cross the train/test boundary, and blind adjudication against
a distance- and class-matched control found them real at 0.9459 (0.8230,
0.9850), against a matcher false-positive rate of 1 in 37. That places roughly
220 of the 1,051 test images, about 21%, in the position of having a
same-patient counterpart in training.

The replacement states the figure and its provenance without overclaiming: the
estimate rests on visual adjudication because D1 ships no patient identifiers,
and the report says so.

Idempotent: aborts if the paragraph has already been replaced.
"""

from pathlib import Path
import sys

from docx import Document
from docx.shared import Pt

DOCX = Path("reports/Gonzalves_BrainMRI_Reliability_Paper_final.docx")

FIND_PREFIX = "Because D1 is distributed without patient-level identifiers"
SENTINEL = "a blind adjudication of 40 such pairs"

REPLACEMENT = (
    "Because D1 is distributed without patient-level identifiers, this procedure "
    "controls leakage at the level of images and near-duplicate groups rather "
    "than at the patient level, and the residual was quantified rather than "
    "assumed to be small. Repeating the near-duplicate audit at a Hamming "
    "distance of 6, one step looser than the threshold used to build the split, "
    "identified 371 within-class pairs that cross the train/test boundary, "
    "against none at the operating threshold. A blind adjudication of 40 such "
    "pairs against 40 distance- and class-matched pairs drawn from "
    "within a single partition found the two groups indistinguishable, at 0.9459 "
    "(0.8230, 0.9850) and 0.9730 (0.8618, 0.9952) respectively, a difference of "
    "-0.0270 (-0.1520, +0.0909). Because both rates sit near ceiling rather than "
    "near zero, this indicates an accurate matcher rather than an indiscriminate "
    "one, with a false-positive rate of 1 in 37 estimated from the within-"
    "partition group. Those 371 pairs involve 233 of the 1,051 test images, so "
    "approximately 220 test images, close to 21% of the partition, have a "
    "same-patient counterpart in the training partition. Since the dataset "
    "carries no patient identifiers, same-patient status is a visual judgement "
    "and the absolute rate should be read accordingly, though the comparison "
    "between groups was made blind and is not sensitive to where that criterion "
    "was set. Internal performance is accordingly not interpreted as evidence of "
    "patient-level generalisation, and the internal figures reported below "
    "should be read as inflated by an amount this design bounds but does not "
    "eliminate."
)


def main():
    if not DOCX.exists():
        sys.exit(f"Manuscript not found: {DOCX}")

    document = Document(str(DOCX))

    target = next(
        (p for p in document.paragraphs if p.text.strip().startswith(FIND_PREFIX)),
        None,
    )
    if target is None:
        sys.exit(f"No paragraph starting {FIND_PREFIX!r} found.")

    if SENTINEL in target.text:
        sys.exit("The paragraph already carries the measured figure; nothing to do.")

    print("Replacing:\n  " + target.text.strip()[:200] + "\n")

    # Keep the first run's formatting, which carries the body font and size, and
    # drop the rest rather than restyling from constants.
    template = target.runs[0]
    font_name = template.font.name
    font_size = template.font.size

    for run in list(target.runs):
        run._element.getparent().remove(run._element)

    run = target.add_run(REPLACEMENT)
    run.font.name = font_name
    run.font.size = font_size if font_size is not None else Pt(11)

    document.save(str(DOCX))

    print("With:\n  " + target.text.strip()[:200] + "...\n")
    print(f"Saved: {DOCX}")


if __name__ == "__main__":
    main()
