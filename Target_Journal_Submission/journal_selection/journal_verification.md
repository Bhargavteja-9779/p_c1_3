# Journal verification record

Date of verification: 2026-11-15. All timeline numbers below were computed by
`scripts/acceptance_times.py` from primary bibliographic metadata and are stored as
CSV files in `data/`. Nothing in this file is typed in by hand from memory.

## 1. How acceptance timelines were verified

Publisher pages (ScienceDirect, Wiley Online Library, Springer Link, OUP Academic,
tandfonline) block automated access from this environment (HTTP 403 / bot challenge),
so publisher-reported "journal insights" numbers could only be seen through search
snippets of third-party sites. Instead of relying on those, the actual
**submission-to-acceptance** interval was computed per article from two primary sources:

| Source | Field used | Journals it covers |
|---|---|---|
| PubMed E-utilities | `<History><PubMedPubDate PubStatus="received">` and `"accepted"` | PubMed-indexed journals (OUP bioinformatics titles, Elsevier biomedical-computing titles, Patterns, J Cheminformatics) |
| Crossref REST API | Article-history assertions `received` / `accepted` | Springer Nature, Taylor & Francis, Wiley (incl. IET/CAAI), ACM |

Definition used throughout: **acceptance time = accepted date − received date**, in
calendar days, per article; summary = median, IQR, mean, share of articles accepted
within 60 and 100 days. This is *submission-to-final-acceptance* (it includes revision
rounds) — it is **not** time to first decision, and not acceptance-to-publication.

Limitations of the method:
* "received" is the date the publisher records as received; for transferred
  manuscripts it may be the transfer date, which shortens the apparent interval.
* Elsevier, IEEE, IOP, ACS, RSC, SAGE and Cambridge do not deposit history dates in
  Crossref, and most of their engineering journals are not PubMed-indexed, so their
  timelines could **not** be independently verified (classified UNVERIFIED).
* A median is a population statistic. It does not predict the timeline of any
  individual manuscript; roughly 30% of 2025 Battery Energy articles took >100 days.

## 2. Result of the screen (69 journals with usable data)

Only six journals had a verified median <= 100 days, all in materials/energy/
manufacturing (2025 publication year):

| Journal | Publisher | n | Median (d) | IQR (d) | Share <= 100 d |
|---|---|---|---|---|---|
| Energy & Environmental Materials | Wiley | 224 | 60.5 | 43-86 | 0.84 |
| Virtual and Physical Prototyping | Taylor & Francis | 225 | 67 | 53-90 | 0.80 |
| Science and Technology of Advanced Materials | Taylor & Francis | 100 | 78 | 56-100 | 0.76 |
| InfoMat | Wiley | 108 | 79.5 | 58.5-113 | 0.66 |
| **Battery Energy** | **Wiley** | **93** | **85** | **52.5-107** | **0.70** |
| Carbon Energy | Wiley | 180 | 88 | 66-118 | 0.63 |

All OUP, Elsevier (PubMed-indexed), Springer Nature, ACM and the other T&F/Wiley
journals screened had medians above 100 days (fastest non-materials journals:
Briefings in Bioinformatics 117 d, JAMIA 118 d, J. Cheminformatics 131 d,
Scientific Reports 135 d). Full tables: `data/pubmed_timelines_2025.csv`,
`data/crossref_springer_timelines_2025.csv`, `data/crossref_tf_wiley_acm_timelines_2025.csv`.

## 3. Battery Energy — year-by-year check (`data/crossref_finalists_by_year.csv`)

| Publication year | n | Median | IQR | Mean | Share <= 60 d | Share <= 100 d |
|---|---|---|---|---|---|---|
| 2024 | 48 | 66.5 | 49-96 | 73.9 | 0.40 | 0.81 |
| 2025 | 93 | 85 | 52.5-107 | 85.4 | 0.32 | 0.70 |
| 2026 (to 15 Nov) | 79 | 86 | 40-136 | 91.1 | 0.34 | 0.65 |

Interpretation: the median has stayed below 100 days in all three years, but it has
drifted upward and the upper quartile now exceeds 100 days. The 100-day target is met
*in median*, not guaranteed.

## 4. Journal metrics — what could and could not be verified

| Item | Value | Evidence | Status |
|---|---|---|---|
| Publisher | John Wiley & Sons, in partnership with Xijing University (China) | DOAJ API record; ISSN portal record (via search) | Verified |
| eISSN | 2768-1696 | DOAJ, Crossref | Verified |
| Open access since | 2022 (CC BY 4.0, author retains copyright) | DOAJ | Verified |
| Peer review | Single anonymous peer review; plagiarism screening | DOAJ | Verified |
| Preservation | CLOCKSS, Portico | DOAJ | Verified |
| APC | DOAJ lists max USD 3,000 / GBP 2,500 / EUR 2,880; other aggregators list up to USD 3,500; waivers available | DOAJ (primary listing) | Partly verified — confirm on Wiley page at submission |
| JCR indexing | Web of Science **Emerging Sources Citation Index (ESCI)** (+ Ei Compendex) | Wiley journal page, as quoted by search results | Verified via publisher text seen in search snippet; Clarivate JCR itself not accessible |
| Journal Impact Factor | 11.1 (most recent value on Wiley page); earlier values 9.9 (2024) and 9.0 (2023 JCR) | Wiley page (search snippet); ResearchGate; VU Amsterdam publishing guide | Value consistent across sources; Clarivate JCR not directly accessible |
| JCR quartile | Q1 (VU Amsterdam guide citing JCR 2023: Q1 in several categories; journalmetrics.org: Q1) | Secondary sources | **Not directly verified in Clarivate JCR** (subscription database) |
| JCR subject categories | Not confirmed (secondary sources suggest energy/electrochemistry/materials categories) | — | **UNVERIFIED** |
| Scope | DOAJ keywords: batteries, energy storage, energy conversion, advanced energy materials, electrocatalysis, photocatalysis. Published papers include data-driven SOH/lifetime work (e.g. 10.1002/bte2.20240036, 10.1002/bte2.20250006, 10.1002/bte2.70011, 10.1002/bte2.70136, 10.1002/bte2.70099) | DOAJ + Crossref | Verified that data-driven battery-health papers are published |
| Author guidelines | Wiley page https://onlinelibrary.wiley.com/page/journal/27681696/homepage/author-guidelines (template "BTE2-article-template") | Page returns HTTP 403 to automated tools | **Could not be read**; must be checked manually before submission |
| Legitimacy / integrity | Wiley imprint, DOAJ-listed, COPE-style policies (plagiarism check, archiving); no retraction cluster found in Crossref titles | DOAJ, Crossref | No concern identified |

## 5. Runner-up

Virtual and Physical Prototyping (Taylor & Francis; JIF 9.8 for 2025 and Q1 best
quartile per the T&F journal page as quoted by search; SCIE; verified median 72 / 67 /
65 days for 2024/2025/2026). It is the stronger journal on verification and
history, but its scope (additive manufacturing / prototyping) did not fit any topic in
which a defensible novel contribution could be built from public data (melt-pool and AM
property ML on literature-compiled data is now crowded; see
`../literature/topic_selection.md`).
