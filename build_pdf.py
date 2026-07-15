#!/usr/bin/env python3
"""Build the typeset PDF from paper.md (pure Python, no LaTeX/pandoc needed).

Pipeline: paper.md -> python-markdown (tables) -> academic HTML/CSS ->
xhtml2pdf (pisa) -> biomimetic-systems-paper.pdf. Figure references are
rewritten from .svg to the rasterized .png versions in figures/, which
xhtml2pdf can embed. Run with the cardvenv interpreter:

    ~/.brandbot/cardvenv/bin/python build_pdf.py
"""
import os
import re
import markdown
from xhtml2pdf import pisa

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "paper.md")
OUT = os.path.join(HERE, "biomimetic-systems-paper.pdf")

CSS = """
@page { size: letter; margin: 2.2cm 2.4cm; }
body { font-family: "Helvetica"; font-size: 10.5pt; line-height: 1.45; color: #111; }
h1 { font-size: 17pt; line-height: 1.25; margin: 0 0 4pt 0; color: #0b2a33; }
h2 { font-size: 13pt; margin: 16pt 0 4pt 0; color: #0b2a33; border-bottom: 1px solid #cfd8dc; padding-bottom: 2pt; }
h3 { font-size: 11pt; margin: 12pt 0 3pt 0; color: #123; }
p { margin: 0 0 7pt 0; text-align: justify; }
strong { color: #0b2a33; }
em { color: #333; }
hr { border: none; border-top: 1px solid #cfd8dc; margin: 10pt 0; }
img { width: 15cm; }
table { border-collapse: collapse; width: 100%; font-size: 9pt; margin: 6pt 0; }
th, td { border: 1px solid #b0bec5; padding: 3pt 5pt; text-align: left; vertical-align: top; }
th { background: #e0f2f1; color: #0b2a33; }
code { font-family: "Courier"; font-size: 9pt; background: #f2f4f5; }
a { color: #0b6b7a; text-decoration: none; }
.byline { font-size: 10pt; color: #333; }
"""


def main():
    with open(SRC, encoding="utf-8") as fh:
        text = fh.read()
    # Embed the rasterized figures rather than the source SVGs.
    text = re.sub(r"figures/(fig\d[\w-]*)\.svg", r"figures/\1.png", text)
    body = markdown.markdown(
        text,
        extensions=["tables", "sane_lists", "attr_list"],
    )
    html = (
        "<html><head><meta charset='utf-8'><style>"
        + CSS
        + "</style></head><body>"
        + body
        + "</body></html>"
    )
    with open(OUT, "wb") as out:
        result = pisa.CreatePDF(html, dest=out, path=HERE)
    if result.err:
        raise SystemExit(f"PDF build failed with {result.err} errors")
    print(f"Wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
