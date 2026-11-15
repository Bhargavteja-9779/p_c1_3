"""Minimal literature search helper (Crossref + arXiv). Prints year | venue | title | DOI | citations."""
import json, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
UA = {"User-Agent": "litsearch/1.0 (academic research)"}
def get(u):
    for k in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60) as r: return r.read()
        except Exception: time.sleep(3*(k+1))
    return b"{}"
def crossref(q, n=15, frm=None):
    p = dict(**{"query.bibliographic": q}, rows=n, select="DOI,title,container-title,issued,is-referenced-by-count,type")
    if frm: p["filter"] = f"from-pub-date:{frm}"
    d = json.loads(get("https://api.crossref.org/works?" + urllib.parse.urlencode(p)) or b"{}")
    for it in d.get("message", {}).get("items", []):
        if it.get("type") not in ("journal-article", "proceedings-article", "posted-content"): continue
        y = (it.get("issued", {}).get("date-parts") or [[None]])[0][0]
        print(f"{y} | {(it.get('container-title') or [''])[0][:38]} | {(it.get('title') or [''])[0][:120]} | {it['DOI']} | c={it.get('is-referenced-by-count')}")
def arxiv(q, n=10):
    x = get("http://export.arxiv.org/api/query?" + urllib.parse.urlencode(dict(search_query=q, max_results=n, sortBy="relevance")))
    ns = {"a": "http://www.w3.org/2005/Atom"}
    for e in ET.fromstring(x).findall("a:entry", ns):
        print(f"{e.findtext('a:published', namespaces=ns)[:4]} | arXiv | {' '.join(e.findtext('a:title', namespaces=ns).split())[:120]} | {e.findtext('a:id', namespaces=ns)}")
if __name__ == "__main__":
    src, q = sys.argv[1], sys.argv[2]
    frm = sys.argv[3] if len(sys.argv) > 3 else None
    (crossref(q, frm=frm) if src == "cr" else arxiv(q))
