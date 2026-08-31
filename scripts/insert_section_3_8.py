"""
Insert the dataset-intrinsic confounds section into the manuscript.

The section is numbered 3.8, and the existing 3.8 becomes 3.9.

Reads:  reports/experiments/SECTION_3_8_DATASET_CONFOUNDS.md
        reports/Gonzalves_BrainMRI_Reliability_Paper_final.docx
Writes: reports/Gonzalves_BrainMRI_Reliability_Paper_final.docx  (in place)

In place, like insert_table_1.py. The _final document has accumulated edits that
do not exist in _with_figures, so regenerating it from upstream would discard
them. See the note in insert_paper_tables.py.

What it does:

  * inserts the section body before the "Integrated Interpretation" heading,
    which is where it belongs -- it qualifies the internal measurement, so it
    has to precede the synthesis
  * renders the two markdown tables as boxed grey "INSERT TABLE 12/13"
    placeholders in the same style as the original placeholders, so
    insert_paper_tables.py can build them, with their captions beneath
  * renumbers the existing 3.8 to 3.9
  * appends the methods footnote as the last paragraph of 2.9

The trailing "Notes on this draft" section of the source file is editorial
correspondence, not manuscript text, and is not inserted.

Idempotent: aborts if the section is already present.
"""

from pathlib import Path
import re
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

SOURCE_MD = Path("reports/experiments/SECTION_3_8_DATASET_CONFOUNDS.md")
DOCX = Path("reports/Gonzalves_BrainMRI_Reliability_Paper_final.docx")

# Heading text of the section that 3.9 is inserted before, and which is then
# renumbered. Matched on the number and the leading words so a reworded title
# still resolves.
ANCHOR_HEADING_RE = re.compile(r"^3\.8\s+Integrated Interpretation")
RENUMBERED_TO = "3.9"

# The methods footnote is the final paragraph of 2.9, so it is inserted before
# the heading that follows that section.
FOOTNOTE_ANCHOR_RE = re.compile(r"^2\.10\s")

FONT_NAME = "Times New Roman"
BODY_PT = 11.0
HEADING2_PT = 12.0
HEADING3_PT = 11.0
CAPTION_PT = 10.0
PLACEHOLDER_PT = 10.0

BODY_SPACE_AFTER_PT = 8.0
CAPTION_SPACE_AFTER_PT = 5.0

# Matches the original boxed placeholders: 1/2 pt grey rule on all four sides.
PLACEHOLDER_BORDER_COLOUR = "999999"
PLACEHOLDER_BORDER_SIZE = "6"
PLACEHOLDER_TEXT_COLOUR = "666666"
PLACEHOLDER_SPACING_TWIPS = "160"


def set_run(run, *, size_pt, bold=False, italic=False, colour=None):
    run.font.name = FONT_NAME
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic

    if colour is not None:
        run.font.color.rgb = RGBColor.from_string(colour)

    # East Asian font binding, so Word does not substitute for the run.
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), FONT_NAME)


def add_markdown_runs(paragraph, text, *, size_pt, italic=False):
    """Render a line of markdown, honouring **bold** spans."""
    for index, segment in enumerate(text.split("**")):
        if not segment:
            continue
        run = paragraph.add_run(segment)
        set_run(run, size_pt=size_pt, bold=index % 2 == 1, italic=italic)


def add_body(anchor, text):
    para = anchor.insert_paragraph_before()
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    para.paragraph_format.space_after = Pt(BODY_SPACE_AFTER_PT)
    add_markdown_runs(para, text, size_pt=BODY_PT)
    return para


def find_style(document, name):
    """
    Resolve a style by display name.

    document.styles[name] raises on this file even though the style exists:
    python-docx matches on the raw w:name in styles.xml, which for built-in
    headings is "heading 2" rather than the "Heading 2" the API reports back.
    Iterating and comparing the mapped .name sidesteps that.
    """
    for style in document.styles:
        if style.name == name:
            return style
    return None


def add_heading(anchor, text, level, style):
    para = anchor.insert_paragraph_before()
    if style is not None:
        para.style = style
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = para.add_run(text)
    set_run(run, size_pt=HEADING2_PT if level == 2 else HEADING3_PT, bold=True)
    return para


def add_caption(anchor, text):
    para = anchor.insert_paragraph_before()
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    para.paragraph_format.space_after = Pt(CAPTION_SPACE_AFTER_PT)
    add_markdown_runs(para, text, size_pt=CAPTION_PT, italic=True)
    return para


def add_table_placeholder(anchor, text):
    """A boxed grey placeholder matching the ones the tables script consumes."""
    para = anchor.insert_paragraph_before()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    ppr = para._p.get_or_add_pPr()

    borders = OxmlElement("w:pBdr")
    for edge in ("top", "bottom", "left", "right"):
        element = OxmlElement(f"w:{edge}")
        element.set(qn("w:val"), "single")
        element.set(qn("w:color"), PLACEHOLDER_BORDER_COLOUR)
        element.set(qn("w:sz"), PLACEHOLDER_BORDER_SIZE)
        borders.append(element)
    ppr.append(borders)

    spacing = OxmlElement("w:spacing")
    spacing.set(qn("w:before"), PLACEHOLDER_SPACING_TWIPS)
    spacing.set(qn("w:after"), PLACEHOLDER_SPACING_TWIPS)
    ppr.append(spacing)

    run = para.add_run(text)
    set_run(
        run,
        size_pt=PLACEHOLDER_PT,
        bold=True,
        colour=PLACEHOLDER_TEXT_COLOUR,
    )
    return para


def parse_source(path):
    """
    Split the source into the section body and the methods footnote.

    The body is everything from the "## 3.9" heading to the horizontal rule that
    closes it. The footnote is the blockquote under "## Methods footnote". The
    "Notes on this draft" section is editorial and is dropped.
    """
    lines = path.read_text(encoding="utf-8").splitlines()

    try:
        start = next(
            i for i, line in enumerate(lines)
            if re.match(r"^##\s+3\.8\s", line)
        )
    except StopIteration:
        sys.exit(f"No '## 3.8' heading found in {path}")

    end = next(
        (i for i in range(start + 1, len(lines)) if lines[i].strip() == "---"),
        len(lines),
    )
    body_lines = lines[start:end]

    footnote_lines = []
    in_footnote = False
    for line in lines[end:]:
        if re.match(r"^##\s+Methods footnote", line):
            in_footnote = True
            continue
        if in_footnote:
            if line.strip() == "---" or line.startswith("## "):
                break
            if line.startswith(">"):
                footnote_lines.append(line.lstrip("> ").rstrip())

    footnote = " ".join(l for l in footnote_lines if l).strip()

    return body_lines, footnote


def build_blocks(body_lines):
    """
    Turn the markdown body into an ordered list of (kind, payload) blocks.

    Markdown tables collapse to a placeholder: the tables are rebuilt from source
    artefacts by insert_paper_tables.py, so carrying their literal text into the
    document would create a second, unmaintained copy of the numbers.
    """
    blocks = []
    paragraph = []
    table_number = 12

    def flush():
        if paragraph:
            blocks.append(("body", " ".join(paragraph)))
            paragraph.clear()

    index = 0
    while index < len(body_lines):
        line = body_lines[index].rstrip()
        stripped = line.strip()

        if not stripped:
            flush()
        elif stripped.startswith("|"):
            # Consume the whole markdown table and emit one placeholder.
            flush()
            while index < len(body_lines) and body_lines[index].strip().startswith("|"):
                index += 1
            blocks.append(("placeholder", table_number))
            table_number += 1
            continue
        elif re.match(r"^###\s+3\.8\.\d", stripped):
            flush()
            blocks.append(("heading3", re.sub(r"^###\s+", "", stripped)))
        elif re.match(r"^##\s+3\.8\s", stripped):
            flush()
            blocks.append(("heading2", re.sub(r"^##\s+", "", stripped)))
        elif re.match(r"^\*\*Table \d+\.\*\*", stripped):
            flush()
            caption = [stripped]
            index += 1
            while index < len(body_lines) and body_lines[index].strip():
                caption.append(body_lines[index].strip())
                index += 1
            blocks.append(("caption", " ".join(caption)))
            continue
        else:
            paragraph.append(stripped)

        index += 1

    flush()
    return blocks


def main():
    if not SOURCE_MD.exists():
        sys.exit(f"Source not found: {SOURCE_MD}")
    if not DOCX.exists():
        sys.exit(f"Manuscript not found: {DOCX}")

    body_lines, footnote = parse_source(SOURCE_MD)
    blocks = build_blocks(body_lines)

    document = Document(str(DOCX))

    # Guard on the section's own heading text, not on its number: the number the
    # inserted section takes and the number the anchor is renumbered to are
    # adjacent, so a numeric check would fire on the renamed anchor instead.
    section_heading = next(
        (payload for kind, payload in blocks if kind == "heading2"), None
    )
    if section_heading is None:
        sys.exit("The source has no section heading to insert.")

    if any(p.text.strip() == section_heading for p in document.paragraphs):
        sys.exit(
            f"{section_heading!r} is already present. Refusing to insert it "
            "twice; restore the document from git if you need to redo this."
        )

    anchor = next(
        (p for p in document.paragraphs if ANCHOR_HEADING_RE.match(p.text.strip())),
        None,
    )
    if anchor is None:
        sys.exit("Could not find the '3.8 Integrated Interpretation' heading.")

    heading2_style = find_style(document, "Heading 2")
    heading3_style = find_style(document, "Heading 3")

    if heading2_style is None:
        sys.exit("The document has no 'Heading 2' style to match.")

    inserted = {"heading2": 0, "heading3": 0, "body": 0, "caption": 0, "placeholder": []}

    for kind, payload in blocks:
        if kind == "heading2":
            add_heading(anchor, payload, 2, heading2_style)
        elif kind == "heading3":
            add_heading(anchor, payload, 3, heading3_style)
        elif kind == "body":
            add_body(anchor, payload)
        elif kind == "caption":
            add_caption(anchor, payload.replace("**", ""))
        elif kind == "placeholder":
            add_table_placeholder(
                anchor,
                f"INSERT TABLE {payload} — built by "
                f"scripts/insert_paper_tables.py from experiments/clever_hans/",
            )
            inserted["placeholder"].append(payload)
            continue
        inserted[kind] += 1

    # Renumber the anchor itself. Its run text carries the number.
    old_heading = anchor.text.strip()
    for run in anchor.runs:
        if "3.8" in run.text:
            run.text = run.text.replace("3.8", RENUMBERED_TO, 1)
            break
    new_heading = anchor.text.strip()

    # Methods footnote as the final paragraph of 2.9.
    footnote_anchor = next(
        (p for p in document.paragraphs if FOOTNOTE_ANCHOR_RE.match(p.text.strip())),
        None,
    )
    footnote_added = False
    if footnote and footnote_anchor is not None:
        add_body(footnote_anchor, footnote)
        footnote_added = True

    document.save(str(DOCX))

    print(f"Inserted into {DOCX}\n")
    print(f"  section headings : {inserted['heading2']}")
    print(f"  subsections      : {inserted['heading3']}")
    print(f"  body paragraphs  : {inserted['body']}")
    print(f"  captions         : {inserted['caption']}")
    print(f"  table placeholders: {inserted['placeholder']}")
    print(f"  methods footnote inserted into 2.9: {footnote_added}")
    print(f"\n  renumbered: {old_heading!r} -> {new_heading!r}")


if __name__ == "__main__":
    main()
