"""Harvest all Battery Energy articles from Crossref; keep those about battery
health/degradation/lifetime/state estimation/management/modelling; save metadata and
abstracts (when deposited) for the journal-quality benchmark."""
import json, re, time, urllib.parse, urllib.request
UA = {"User-Agent": "journal-benchmark/1.0 (academic research)"}
def get(u):
    for k in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60) as r: return json.loads(r.read())
        except Exception: time.sleep(3 * (k + 1))
items, cursor = [], "*"
while True:
    m = get("https://api.crossref.org/journals/2768-1696/works?" + urllib.parse.urlencode(dict(
        rows=200, cursor=cursor, select="DOI,title,abstract,author,published,is-referenced-by-count,type,assertion,references-count")))["message"]
    if not m["items"]: break
    items += m["items"]; cursor = m["next-cursor"]; time.sleep(0.5)
pat = re.compile(r"state of health|state-of-health|\bSOH\b|lifetime|life prediction|cycle life|remaining useful|RUL|degradation|aging|ageing|prognos|diagnos|state of charge|state-of-charge|\bSOC\b|battery management|machine learning|deep learning|neural|data-driven|data driven|equivalent circuit|electrochemical model|impedance spectr|capacity estimation|capacity fade|knee", re.I)
rel = []
for it in items:
    t = re.sub(r"<[^>]+>", "", (it.get("title") or [""])[0]); t = " ".join(t.split())
    ab = " ".join(re.sub(r"<[^>]+>", " ", it.get("abstract", "")).split())
    if pat.search(t) or (ab and re.search(r"machine learning|state of health|lifetime prediction|remaining useful", ab, re.I)):
        a = {x.get("name"): x.get("value") for x in it.get("assertion", [])}
        rel.append(dict(doi=it["DOI"], title=t, year=it["published"]["date-parts"][0][0], cites=it.get("is-referenced-by-count"),
                        n_refs=it.get("references-count"), received=a.get("received"), accepted=a.get("accepted"),
                        authors=", ".join(f"{x.get('given','')} {x.get('family','')}".strip() for x in it.get("author", [])[:6]),
                        abstract=ab))
rel.sort(key=lambda r: -(r["cites"] or 0))
json.dump(dict(total_articles=len(items), relevant=rel), open("journal_papers/battery_energy_relevant.json", "w"), indent=1)
print("total", len(items), "relevant", len(rel), "with abstract", sum(bool(r["abstract"]) for r in rel))
for r in rel[:60]: print(r["cites"], r["year"], r["doi"], r["title"][:100])
