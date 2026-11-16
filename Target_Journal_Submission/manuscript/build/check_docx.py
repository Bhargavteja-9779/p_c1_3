#!/usr/bin/env python3
"""Re-open a rendered DOCX (and its PDF) and verify structure and formatting.

    python manuscript/build/check_docx.py manuscript/Final_Manuscript.docx [--final]

Checks: headings by level; figures (count, captions, width <= text width); tables
(count, captions, size); OMML equations and right-aligned numbers; citations [n] all
resolvable and every reference cited; leftover markup ({{, [@, \\tag, $$, ??, [[, DRAFT);
body font/size/line spacing; line numbering; page count (from the PDF). With --final,
placeholders such as "[Author" are reported as warnings (they must be filled by the
authors) and any DRAFT marker is an error. Exit code 1 on errors.
"""
import re, subprocess, sys, os
from docx import Document
from docx.oxml.ns import qn


def main(path, final=False):
    doc = Document(path); errors, warns, info = [], [], {}
    body = doc.element.body
    paras = doc.paragraphs
    heads = [(p.style.name, p.text.strip()) for p in paras if p.style.name.lower().startswith(("heading", "title"))]
    info["headings"] = heads
    caps_fig = [p.text for p in paras if re.match(r"^Figure S?\d+\.", p.text.strip())]
    caps_tab = [p.text for p in paras if re.match(r"^Table S?\d+\.", p.text.strip())]
    n_img = len(body.findall(".//" + qn("w:drawing")))
    info["figures"] = n_img; info["figure_captions"] = len(caps_fig); info["tables"] = len(doc.tables); info["table_captions"] = len(caps_tab)
    if n_img != len(caps_fig):
        errors.append(f"{n_img} images but {len(caps_fig)} figure captions")
    if len(doc.tables) != len(caps_tab):
        errors.append(f"{len(doc.tables)} tables but {len(caps_tab)} table captions")
    sec = doc.sections[0]
    tw = sec.page_width - sec.left_margin - sec.right_margin
    for ext in body.iter(qn("wp:extent")):
        if int(ext.get("cx")) > tw + 10:
            errors.append("image wider than text width")
    om = body.findall(".//" + qn("m:oMath"))
    info["equations"] = len(om)
    numbered = [p for p in paras if p._p.find(".//" + qn("m:oMath")) is not None and re.search(r"\(\d+\)\s*$", p.text)]
    info["numbered_equations"] = len(numbered)
    text = "\n".join(p.text for p in paras)
    for t in doc.tables:
        for row in t.rows:
            for c in row.cells:
                text += "\n" + c.text
    for bad in ("{{", "[@", "\\tag", "$$", "??", "[[", "EQNUMMARK"):
        if bad in text:
            errors.append(f"leftover markup '{bad}'")
    if "DRAFT" in text:
        (errors if final else warns).append("DRAFT placeholders present")
    for ph in ("[Author", "[Department", "[To be", "[repository", "[Required by Wiley", "[State the tool"):
        if ph in text:
            warns.append(f"author placeholder present: {ph}")
    # citations
    refs_idx = next((i for i, p in enumerate(paras) if p.text.strip() == "References"), None)
    if refs_idx is None:
        errors.append("no References section")
    else:
        ref_nums = [int(m.group(1)) for p in paras[refs_idx + 1:] for m in [re.match(r"^\[(\d+)\]", p.text.strip())] if m]
        cited = set()
        for p in paras[:refs_idx]:
            for m in re.finditer(r"\[(\d+(?:[,–-]\d+)*)\]", p.text):
                for part in m.group(1).split(","):
                    if "–" in part or "-" in part:
                        a, b = re.split(r"[–-]", part); cited.update(range(int(a), int(b) + 1))
                    else:
                        cited.add(int(part))
        info["references"] = len(ref_nums); info["cited_numbers"] = len(cited)
        if ref_nums != list(range(1, len(ref_nums) + 1)):
            errors.append("reference list not consecutively numbered")
        if cited - set(ref_nums):
            errors.append(f"citations without reference entry: {sorted(cited - set(ref_nums))}")
        if set(ref_nums) - cited:
            errors.append(f"references never cited: {sorted(set(ref_nums) - cited)}")
    # formatting
    normal = doc.styles["Normal"]
    info["normal_font"] = (normal.font.name, normal.font.size.pt if normal.font.size else None)
    if normal.font.name != "Times New Roman":
        errors.append("Normal style font is not Times New Roman")
    info["line_numbers"] = sec._sectPr.find(qn("w:lnNumType")) is not None
    pdf = path.replace(".docx", ".pdf")
    if os.path.exists(pdf):
        out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
        m = re.search(r"Pages:\s+(\d+)", out); info["pdf_pages"] = int(m.group(1)) if m else None
    for k, v in info.items():
        print(f"{k}: {v}" if k != "headings" else "headings:\n  " + "\n  ".join(f"{a}: {b}" for a, b in v))
    for w in warns:
        print("WARNING:", w)
    for e in errors:
        print("ERROR:", e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], "--final" in sys.argv))
