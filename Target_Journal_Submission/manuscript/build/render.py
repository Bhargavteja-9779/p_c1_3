#!/usr/bin/env python3
"""Render the manuscript sources to DOCX (native Word equations) and PDF.

    python manuscript/build/render.py [--numbers results/manuscript_numbers.json] [--pdf] [--si]

Sources (relative to the Target_Journal_Submission root):
  manuscript/src/part*.md  main text, concatenated in lexical order
  manuscript/src/si*.md    Supporting Information (with --si)
Tokens:
  {{KEY}}                          value from the numbers JSON (build fails if missing)
  {{FIG:name|caption}}             figure figures/name.png (main);  {{SFIG:...}} in SI
  {{FIGREF:name}} / {{SFIGREF:name}}           -> "Figure n" / "Figure Sn"
  {{TABLE:csv|caption|colspec}}    table from CSV (main);  {{STABLE:...}} in SI
  {{TABREF:csv}} / {{STABREF:csv}}             -> "Table n" / "Table Sn"
  [@key] / [@k1; @k2]              numbered citations from literature/references_final.json
                                   (falls back to references_verified.json)
  $$ ... \\tag{n} $$                display equation with right-aligned number
colspec: comma-separated "column:Header:format", format in {.Nf, .Ng, pctN, int, s}.
"""
from __future__ import annotations
import argparse, copy, json, math, os, re, subprocess, sys
import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TOKEN = re.compile(r"\{\{([^{}]+)\}\}")
NUMTOKEN = re.compile(r"\{\{([A-Za-z0-9_.\-]+)\}\}")   # plain number keys (no ':')
OBJ_HEADS = ("FIG", "SFIG", "TABLE", "STABLE", "FIGREF", "SFIGREF", "TABREF", "STABREF")


def scan_objects(text):
    """Yield (start, end, content) of {{HEAD:...}} tokens; LaTeX braces inside are allowed
    (the token ends at the first '}}' reached with balanced single braces)."""
    i = 0
    while True:
        j = text.find("{{", i)
        if j < 0:
            return
        head = text[j + 2:].split(":", 1)[0]
        if head not in OBJ_HEADS or ":" not in text[j + 2:j + 2 + len(head) + 1]:
            i = j + 2; continue
        k, depth = j + 2, 0
        while k < len(text):
            if text.startswith("}}", k) and depth == 0:
                break
            if text[k] == "{": depth += 1
            elif text[k] == "}": depth -= 1
            k += 1
        else:
            raise BuildError(f"unterminated token near: {text[j:j + 60]}")
        yield j, k + 2, text[j + 2:k]
        i = k + 2


class BuildError(Exception):
    pass


DRAFT = {"on": False}  # --draft: show placeholders for missing results instead of failing (never for final builds)


# ----------------------------------------------------------------------------- helpers
def read_sources(pattern_prefix):
    d = os.path.join(ROOT, "manuscript", "src")
    files = sorted(f for f in os.listdir(d) if f.startswith(pattern_prefix) and f.endswith(".md"))
    return "\n\n".join(open(os.path.join(d, f), encoding="utf-8").read() for f in files), files


def load_refs():
    for name in ("references_final.json", "references_verified.json"):
        p = os.path.join(ROOT, "literature", name)
        if os.path.exists(p):
            return json.load(open(p, encoding="utf-8")), name
    raise BuildError("no reference file")


def fmt_value(v, fmt):
    if isinstance(v, str):
        return v
    if v is None or (isinstance(v, float) and not math.isfinite(v)):
        return "–"
    if fmt in ("", "s"):
        return str(v)
    if fmt == "int":
        return f"{int(round(v)):,}"
    if fmt.startswith("pct"):
        return f"{100 * v:.{int(fmt[3:] or 1)}f}"
    return format(v, fmt)


def table_markdown(csv_rel, colspec, caption):
    p = os.path.join(ROOT, csv_rel)
    if not os.path.exists(p):
        if DRAFT["on"]:
            return f"**[DRAFT: table {csv_rel} not yet generated]**\n\n: {caption}\n"
        raise BuildError(f"table file missing: {csv_rel}")
    df = pd.read_csv(p)
    cols = []
    if colspec.strip():
        for item in colspec.split(","):
            parts = item.split(":")
            if len(parts) < 3:
                raise BuildError(f"bad colspec item '{item}' in {csv_rel}")
            col, header, fmt = parts[0], ":".join(parts[1:-1]), parts[-1]
            if col not in df.columns:
                raise BuildError(f"column '{col}' not in {csv_rel}")
            cols.append((col, header, fmt))
    else:
        for c in df.columns:
            cols.append((c, c.replace("_", " "), ".3g" if pd.api.types.is_float_dtype(df[c]) else "s"))
    head = "| " + " | ".join(h for _, h, _ in cols) + " |"
    sep = "|" + "|".join("---" for _ in cols) + "|"
    rows = []
    for _, r in df.iterrows():
        cells = []
        for c, _, f in cols:
            v = r[c]
            cells.append(fmt_value(v if not (isinstance(v, float) and math.isnan(v)) else None, f).replace("|", "/"))
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join([head, sep] + rows) + f"\n\n: {caption}\n"


# ----------------------------------------------------------------------------- resolution
def number_objects(text, kinds):
    """Order of first appearance of FIG/TABLE objects (by the object token itself)."""
    order = {k: [] for k in kinds}
    for _, _, tok in scan_objects(text):
        head = tok.split(":", 1)[0]
        if head in kinds:
            key = tok[len(head) + 1:].split("|")[0].strip()
            if key not in order[head]:
                order[head].append(key)
    return order


def resolve(text, numbers, objs, prefix_map, refs_state, doc="main"):
    """Replace number tokens first, then figure/table/reference tokens."""
    missing = []
    text = resolve_inline(text, numbers, missing)
    out, last = [], 0
    for a, b, tok in list(scan_objects(text)):
        out.append(text[last:a]); out.append(object_token(tok.strip(), objs, prefix_map)); last = b
    out.append(text[last:])
    if missing:
        raise BuildError("missing number keys: " + ", ".join(sorted(set(missing))))
    return "".join(out)


def object_token(tok, objs, prefix_map):
    head = tok.split(":", 1)[0]
    if head in ("FIG", "SFIG"):
        name, cap = tok.split(":", 1)[1].split("|", 1)
        n = objs[head].index(name.strip()) + 1
        lab = f"Figure {prefix_map[head]}{n}."
        path = os.path.join(ROOT, "figures", name.strip() + ".png")
        if not os.path.exists(path):
            if DRAFT["on"]:
                return f"**[DRAFT: {lab} {name.strip()} not yet generated]** {cap.strip()}"
            raise BuildError(f"figure missing: {path}")
        return f"![**{lab}** {cap.strip()}]({path}){{width=6.3in}}"
    if head in ("TABLE", "STABLE"):
        parts = tok.split(":", 1)[1].split("|")
        csv_rel, cap = parts[0].strip(), parts[1].strip()
        colspec = "|".join(parts[2:]) if len(parts) > 2 else ""
        n = objs[head].index(csv_rel) + 1
        return table_markdown(csv_rel, colspec, f"**Table {prefix_map[head]}{n}.** {cap}")
    key = tok.split(":", 1)[1].strip()
    kind = {"FIGREF": "FIG", "SFIGREF": "SFIG", "TABREF": "TABLE", "STABREF": "STABLE"}[head]
    for k in (kind, kind[1:] if kind.startswith("S") else "S" + kind):
        if k in objs and key in objs[k]:
            return f"{'Figure' if 'FIG' in k else 'Table'} {prefix_map[k]}{objs[k].index(key) + 1}"
    raise BuildError(f"unresolved reference {tok}")


def resolve_inline(s, numbers, missing):
    def r(m):
        k = m.group(1).strip()
        if k not in numbers:
            if DRAFT["on"]:
                return f"[[{k}]]"
            missing.append(k); return "??"
        return str(numbers[k])
    return NUMTOKEN.sub(r, s)


CITE = re.compile(r"\[(@[^\]]+)\]")


def compress(nums):
    nums = sorted(set(nums)); out = []; i = 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append(f"{nums[i]}–{nums[j]}" if j - i >= 2 else ",".join(str(x) for x in nums[i:j + 1]))
        i = j + 1
    return ",".join(out)


def number_citations(text, refs, state):
    def r(m):
        keys = [k.strip().lstrip("@") for k in m.group(1).split(";")]
        ns = []
        for k in keys:
            if k not in refs or not refs[k] or not refs[k].get("verified", False):
                raise BuildError(f"unknown or unverified citation key: {k}")
            if k not in state["order"]:
                state["order"].append(k)
            ns.append(state["order"].index(k) + 1)
        return "[" + compress(ns) + "]"
    return CITE.sub(r, text)


def format_ref(rec):
    if rec.get("formatted"):
        return rec["formatted"]
    names = []
    for a in rec.get("authors", []):
        if "," in a:
            fam, giv = [x.strip() for x in a.split(",", 1)]
        else:
            parts = a.split(); fam, giv = parts[-1], " ".join(parts[:-1])
        ini = " ".join(p[0] + "." for p in re.split(r"[\s-]+", giv) if p)
        names.append((ini + " " + fam).strip())
    au = ", ".join(names) if names else ""
    title = rec.get("title", "").rstrip(".")
    venue = rec.get("venue", "")
    bits = [f"{au}, {title}, *{venue}*" if venue else f"{au}, {title}"]
    tail = f" {rec.get('year')}" if rec.get("year") else ""
    if rec.get("volume"):
        tail += f", {rec['volume']}"
    if rec.get("pages"):
        tail += f", {rec['pages']}"
    s = bits[0] + tail + "."
    if rec.get("doi"):
        s += f" https://doi.org/{rec['doi']}"
    elif rec.get("arxiv"):
        s += f" arXiv:{rec['arxiv']}"
    return s


def equations(text):
    """$$ body \\tag{n} $$ -> display equation followed by a marker paragraph."""
    def r(m):
        body = m.group(1)
        t = re.search(r"\\tag\{([^}]*)\}", body)
        if not t:
            return m.group(0)
        body = body.replace(t.group(0), "").strip()
        return f"$$ {body} $$\n\nEQNUMMARK({t.group(1)})\n"
    return re.sub(r"\$\$(.+?)\$\$", r, text, flags=re.S)


# ----------------------------------------------------------------------------- DOCX post-processing
def postprocess(docx_path, kind="main"):
    from docx import Document
    from docx.shared import Pt, Cm, RGBColor
    from docx.enum.text import WD_LINE_SPACING, WD_TAB_ALIGNMENT, WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    doc = Document(docx_path)
    styles_by_name = {s.name.lower(): s for s in doc.styles}

    class _St:  # case-insensitive style lookup (pandoc and python-docx differ in capitalisation)
        def __getitem__(self, k):
            return styles_by_name[k.lower()]

        def __iter__(self):
            return iter(styles_by_name.values())
    st = _St()
    def setfont(style, size, bold=None, italic=None, spacing=None, after=None, before=None):
        f = style.font; f.name = "Times New Roman"; f.size = Pt(size); f.color.rgb = RGBColor(0, 0, 0)
        rpr = style.element.get_or_add_rPr(); rf = rpr.find(qn("w:rFonts"))
        if rf is None:
            rf = OxmlElement("w:rFonts"); rpr.append(rf)
        for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rf.set(qn(a), "Times New Roman")
        for a in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
            if rf.get(qn(a)) is not None:
                del rf.attrib[qn(a)]
        if bold is not None: f.bold = bold
        if italic is not None: f.italic = italic
        pf = style.paragraph_format
        if spacing is not None:
            pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE if spacing == 2 else WD_LINE_SPACING.SINGLE
        if after is not None: pf.space_after = Pt(after)
        if before is not None: pf.space_before = Pt(before)
    for name in ("Normal", "Body Text", "First Paragraph", "Compact"):
        if name.lower() in styles_by_name:
            setfont(st[name], 12, spacing=2, after=0)
    heads = {"Heading 1": (16, True, False), "Heading 2": (14, True, False), "Heading 3": (12, True, False), "Heading 4": (12, True, True)}
    for name, (sz, b, it) in heads.items():
        if name.lower() in styles_by_name:
            setfont(st[name], sz, bold=b, italic=it, spacing=2, before=12, after=6)
    for name in ("Image Caption", "Table Caption", "Caption"):
        if name.lower() in styles_by_name:
            setfont(st[name], 10, italic=False, spacing=1, before=4, after=10)
    for name in ("Title",):
        if name.lower() in styles_by_name:
            setfont(st[name], 16, bold=True, spacing=1)
    # page set-up, line numbers, page numbers
    for sec in doc.sections:
        sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)  # A4
        sec.left_margin = sec.right_margin = sec.top_margin = sec.bottom_margin = Cm(2.5)
        sp = sec._sectPr
        if kind == "main" and sp.find(qn("w:lnNumType")) is None:
            ln = OxmlElement("w:lnNumType"); ln.set(qn("w:countBy"), "1"); ln.set(qn("w:restart"), "continuous"); ln.set(qn("w:distance"), "283")
            pgsz = sp.find(qn("w:pgMar"))
            (pgsz.addnext(ln) if pgsz is not None else sp.append(ln))
        p = sec.footer.paragraphs[0] if sec.footer.paragraphs else sec.footer.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fppr = p._p.get_or_add_pPr()
        if fppr.find(qn("w:suppressLineNumbers")) is None:
            fppr.append(OxmlElement("w:suppressLineNumbers"))
        if not p.runs:
            r = p.add_run(); f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
            it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = "PAGE"
            f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "end")
            r._r.append(f1); r._r.append(it); r._r.append(f2)
    text_width = doc.sections[0].page_width - doc.sections[0].left_margin - doc.sections[0].right_margin
    # flatten OMML delimiter objects (m:d) into plain bracket characters: LibreOffice draws
    # stretchy delimiters with wrong glyphs; plain characters render identically in Word
    def mrun(ch):
        r = OxmlElement("m:r"); t = OxmlElement("m:t"); t.text = ch; r.append(t); return r
    for d in list(doc.element.body.iter(qn("m:d"))):
        dpr = d.find(qn("m:dPr"))
        get = lambda tag, default: (dpr.find(qn(tag)).get(qn("m:val")) if dpr is not None and dpr.find(qn(tag)) is not None else default)
        beg, end, sep = get("m:begChr", "("), get("m:endChr", ")"), get("m:sepChr", "|")
        seq = [mrun(beg)] if beg else []
        es = d.findall(qn("m:e"))
        for i, e in enumerate(es):
            if i:
                seq.append(mrun(sep))
            seq.extend(list(e))
        if end:
            seq.append(mrun(end))
        parent = d.getparent(); idx = parent.index(d)
        for k, el in enumerate(seq):
            parent.insert(idx + k, el)
        parent.remove(d)
    body = doc.element.body
    paras = list(doc.paragraphs)
    # numbered equations: paragraph with oMathPara followed by EQNUMMARK(n)
    n_eq = 0
    for i, p in enumerate(paras):
        m = re.fullmatch(r"\s*EQNUMMARK\(([^)]*)\)\s*", p.text)
        if not m or i == 0:
            continue
        prev = paras[i - 1]
        omp = prev._p.find(".//" + qn("m:oMathPara"))
        if omp is None:
            raise BuildError("equation marker without preceding display equation")
        om = omp.find(qn("m:oMath"))
        newp = copy.deepcopy(prev._p)
        for ch in list(newp):
            if ch.tag != qn("w:pPr"):
                newp.remove(ch)
        ppr = newp.find(qn("w:pPr"))
        if ppr is None:
            ppr = OxmlElement("w:pPr"); newp.insert(0, ppr)
        tabs = OxmlElement("w:tabs")
        for pos, val in ((int(text_width / 2 / 635), "center"), (int(text_width / 635), "right")):
            t = OxmlElement("w:tab"); t.set(qn("w:val"), val); t.set(qn("w:pos"), str(pos)); tabs.append(t)
        ppr.append(tabs)
        def tabrun():
            r = OxmlElement("w:r"); r.append(OxmlElement("w:tab")); return r
        newp.append(tabrun()); newp.append(copy.deepcopy(om)); newp.append(tabrun())
        r = OxmlElement("w:r"); rpr = OxmlElement("w:rPr"); rf = OxmlElement("w:rFonts")
        rf.set(qn("w:ascii"), "Times New Roman"); rf.set(qn("w:hAnsi"), "Times New Roman"); rpr.append(rf); r.append(rpr)
        t = OxmlElement("w:t"); t.text = f"({m.group(1)})"; r.append(t); newp.append(r)
        prev._p.addprevious(newp)
        prev._p.getparent().remove(prev._p); p._p.getparent().remove(p._p)
        n_eq += 1
    # tables: booktabs rules, 9 pt, single spacing, bold header
    for tbl in doc.tables:
        tblPr = tbl._tbl.tblPr
        b = tblPr.find(qn("w:tblBorders"))
        if b is not None:
            tblPr.remove(b)
        b = OxmlElement("w:tblBorders")
        for edge, val in (("top", "single"), ("bottom", "single"), ("left", "nil"), ("right", "nil"), ("insideH", "nil"), ("insideV", "nil")):
            e = OxmlElement(f"w:{edge}"); e.set(qn("w:val"), val)
            if val == "single":
                e.set(qn("w:sz"), "8"); e.set(qn("w:space"), "0"); e.set(qn("w:color"), "000000")
            b.append(e)
        tblPr.append(b)
        for ri, row in enumerate(tbl.rows):
            for cell in row.cells:
                if ri == 0:
                    tcPr = cell._tc.get_or_add_tcPr(); tb = OxmlElement("w:tcBorders"); bt = OxmlElement("w:bottom")
                    bt.set(qn("w:val"), "single"); bt.set(qn("w:sz"), "6"); bt.set(qn("w:space"), "0"); bt.set(qn("w:color"), "000000")
                    tb.append(bt); tcPr.append(tb)
                for cp in cell.paragraphs:
                    cp.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
                    cp.paragraph_format.space_after = Pt(0)
                    for run in cp.runs:
                        run.font.size = Pt(9); run.font.name = "Times New Roman"
                        if ri == 0:
                            run.font.bold = True
    # first heading -> Title style; references hanging indent
    in_refs = False
    for p in doc.paragraphs:
        if p.style.name.lower().startswith("heading") and p.text.strip() == "References":
            in_refs = True; continue
        if in_refs and re.match(r"^\[\d+\]", p.text):
            pf = p.paragraph_format; pf.left_indent = Cm(0.9); pf.first_line_indent = Cm(-0.9)
            pf.line_spacing_rule = WD_LINE_SPACING.SINGLE; pf.space_after = Pt(4)
    first = next((p for p in doc.paragraphs if p.style.name.lower() == "heading 1"), None)
    if first is not None and "title" in styles_by_name:
        first.style = st["Title"]
    doc.save(docx_path)
    return n_eq


# ----------------------------------------------------------------------------- main
def build(numbers_path, out_docx, want_pdf, want_si):
    numbers = json.load(open(numbers_path, encoding="utf-8"))
    refs, ref_file = load_refs()
    main_src, main_files = read_sources("part")
    si_all, si_files = read_sources("si")  # always parsed so main-text references to SI objects resolve
    si_src = si_all if want_si else ""
    objs = number_objects(main_src, ["FIG", "TABLE"]); objs.update(number_objects(si_all, ["SFIG", "STABLE"]))
    prefix = {"FIG": "", "TABLE": "", "SFIG": "S", "STABLE": "S"}
    outputs = {}
    state = {"order": []}
    for kind, src, out in (("main", main_src, out_docx), ("si", si_src, os.path.join(os.path.dirname(out_docx), "Supporting_Information.docx"))):
        if not src:
            continue
        text = resolve(src, numbers, objs, prefix, state, kind)
        text = equations(text)
        st = state if kind == "main" else {"order": []}
        text = number_citations(text, refs, st)
        if st["order"]:
            text += "\n\n## References\n\n" + "\n\n".join(f"[{i + 1}] {format_ref(refs[k])}" for i, k in enumerate(st["order"]))
        leftovers = [s for s in ("{{", "[@", "\\tag", "??") if s in text]
        if DRAFT["on"]:
            leftovers = [x for x in leftovers if x != "??"]
        if leftovers:
            raise BuildError(f"{kind}: unresolved markup {leftovers}")
        md = out.replace(".docx", ".md"); open(md, "w", encoding="utf-8").write(text)
        subprocess.run(["pandoc", md, "-f", "markdown+tex_math_dollars+superscript+subscript+pipe_tables+implicit_figures",
                        "-o", out, "--resource-path", ROOT], check=True)
        n_eq = postprocess(out, kind)
        outputs[kind] = dict(docx=out, md=md, equations_numbered=n_eq, citations=len(st["order"]))
        if want_pdf:
            subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", os.path.dirname(out), out],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            outputs[kind]["pdf"] = out.replace(".docx", ".pdf")
    outputs["reference_file"] = ref_file; outputs["sources"] = main_files + si_files
    return outputs


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--numbers", default=os.path.join(ROOT, "results", "manuscript_numbers.json"))
    ap.add_argument("--out", default=os.path.join(ROOT, "manuscript", "Final_Manuscript.docx"))
    ap.add_argument("--pdf", action="store_true"); ap.add_argument("--si", action="store_true")
    ap.add_argument("--draft", action="store_true", help="placeholders for missing results (review drafts only)")
    a = ap.parse_args(); DRAFT["on"] = a.draft
    if a.draft:
        a.out = a.out.replace("Final_Manuscript", "Draft_Manuscript")
    try:
        print(json.dumps(build(a.numbers, a.out, a.pdf, a.si), indent=1))
    except BuildError as e:
        print("BUILD FAILED:", e, file=sys.stderr); sys.exit(2)
