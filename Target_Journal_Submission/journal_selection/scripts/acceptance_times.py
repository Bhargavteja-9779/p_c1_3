"""Empirical submission-to-acceptance times from primary bibliographic metadata.

Two independent sources are used:
  * PubMed E-utilities: <History><PubMedPubDate PubStatus="received"/"accepted">
  * Crossref REST API: Springer Nature "ArticleHistory" assertions (received/accepted)

Usage: python acceptance_times.py --pubmed "Name|ISSN" ... --crossref "Name|ISSN" ...
Outputs a CSV row per journal with n, median, IQR, mean, share <= 100 days.
Only original research articles with both dates are counted; dates before 2000 or
negative intervals are discarded as metadata errors.
"""
import argparse, csv, datetime as dt, json, statistics, sys, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

UA = {"User-Agent": "journal-timeline-audit/1.0 (research; contact withheld)"}

def get(url, tries=4):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:  # noqa
            time.sleep(2 * (k + 1))
    raise RuntimeError(url)

def summarise(name, issn, source, days):
    days = sorted(d for d in days if 0 <= d <= 1500)
    if not days:
        return dict(journal=name, issn=issn, source=source, n=0)
    q = statistics.quantiles(days, n=4) if len(days) > 3 else [days[0], days[len(days)//2], days[-1]]
    return dict(journal=name, issn=issn, source=source, n=len(days),
                median=statistics.median(days), q1=q[0], q3=q[2],
                mean=round(statistics.mean(days), 1),
                share_le_60=round(sum(d <= 60 for d in days) / len(days), 3),
                share_le_100=round(sum(d <= 100 for d in days) / len(days), 3))

def pubmed(name, issn, years=("2025",), cap=600):
    term = f'"{issn}"[ISSN] AND ({" OR ".join(y + "[dp]" for y in years)}) AND journal article[pt] NOT review[pt] NOT editorial[pt] NOT comment[pt] NOT erratum[pt]'
    u = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + urllib.parse.urlencode(
        dict(db="pubmed", term=term, retmax=cap, retmode="json", sort="pub_date"))
    ids = json.loads(get(u))["esearchresult"]["idlist"]
    days = []
    for i in range(0, len(ids), 150):
        x = get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + urllib.parse.urlencode(
            dict(db="pubmed", id=",".join(ids[i:i+150]), retmode="xml")))
        root = ET.fromstring(x)
        for art in root.findall(".//PubmedArticle"):
            h = {}
            for p in art.findall(".//History/PubMedPubDate"):
                try:
                    h[p.get("PubStatus")] = dt.date(int(p.findtext("Year")), int(p.findtext("Month")), int(p.findtext("Day")))
                except Exception:
                    pass
            if "received" in h and "accepted" in h and h["received"].year >= 2000:
                days.append((h["accepted"] - h["received"]).days)
        time.sleep(0.4)
    return summarise(name, issn, "PubMed:" + "+".join(years), days)

def parse_date(s):
    for fmt in ("%d %B %Y", "%d %b %Y", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(s.strip(), fmt).date()
        except Exception:
            pass
    return None

def crossref(name, issn, start="2025-01-01", end="2025-12-31", cap=600):
    days, cursor, seen = [], "*", 0
    while seen < cap:
        u = (f"https://api.crossref.org/journals/{issn}/works?" + urllib.parse.urlencode(dict(
            filter=f"from-pub-date:{start},until-pub-date:{end},type:journal-article",
            rows=200, cursor=cursor, select="DOI,assertion")))
        m = json.loads(get(u))["message"]
        items = m["items"]
        if not items:
            break
        for it in items:
            a = {x.get("name"): x.get("value") for x in it.get("assertion", [])}
            r, acc = parse_date(a.get("received", "") or ""), parse_date(a.get("accepted", "") or "")
            if r and acc and r.year >= 2000:
                days.append((acc - r).days)
        seen += len(items)
        cursor = m.get("next-cursor")
        time.sleep(0.3)
    return summarise(name, issn, f"Crossref:{start[:4]}", days)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pubmed", nargs="*", default=[])
    ap.add_argument("--crossref", nargs="*", default=[])
    ap.add_argument("--years", default="2025")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rows = []
    for s in a.pubmed:
        n, i = s.split("|"); r = pubmed(n, i, tuple(a.years.split(","))); rows.append(r); print(r, flush=True)
    for s in a.crossref:
        n, i = s.split("|"); r = crossref(n, i); rows.append(r); print(r, flush=True)
    keys = ["journal", "issn", "source", "n", "median", "q1", "q3", "mean", "share_le_60", "share_le_100"]
    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); [w.writerow(r) for r in rows]
