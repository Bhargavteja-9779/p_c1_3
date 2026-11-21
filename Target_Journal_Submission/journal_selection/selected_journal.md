# Selected target journal

| Field | Record |
|---|---|
| TARGET JOURNAL | **Battery Energy** (eISSN 2768-1696) |
| PUBLISHER | John Wiley & Sons, in partnership with Xijing University; gold open access (CC BY 4.0) since 2022 |
| JCR STATUS | Indexed in Web of Science Core Collection — Emerging Sources Citation Index (ESCI); also Ei Compendex (Wiley journal page as quoted in search results). Clarivate JCR itself could not be accessed (subscription). |
| JCR QUARTILE | Q1 according to secondary sources (VU Amsterdam publishing guide citing JCR 2023: "Q1 in several categories"; journalmetrics.org: JCR Q1). **Not verified directly in Clarivate JCR.** |
| JOURNAL IMPACT FACTOR | 11.1 (most recent value shown on the Wiley journal page; earlier 9.9 for 2024 and 9.0 in JCR 2023). Clarivate value not directly verified. |
| JCR SUBJECT CATEGORY | **Unverified** (secondary sources suggest energy/electrochemistry/materials categories). |
| VERIFIED REVIEW/DECISION TIMELINE | Time to first decision: not available from any verifiable source. DOAJ lists "average weeks from submission to publication: 10". |
| VERIFIED ACCEPTANCE TIMELINE | Computed from Crossref article-history dates (submission -> final acceptance, includes revisions): median **66.5 d** (2024, n=48), **85 d** (2025, n=93), **86 d** (2026 to 15 Nov, n=79); share accepted within 100 days 81% / 70% / 65%. Data-driven papers in the journal-paper benchmark: median 100 d (range 39-183). Population statistic only — not a guarantee for any manuscript. |
| APC | DOAJ: up to USD 3,000 / GBP 2,500 / EUR 2,880; some aggregators list up to USD 3,500; Wiley waiver/discount policy applies. Confirm on the Wiley page at submission. |
| SCOPE FIT | Batteries and energy storage, including battery management, health diagnostics, degradation and lifetime prediction (DOAJ keywords + published data-driven SOH/lifetime papers, e.g. 10.1002/bte2.20240036, 10.1002/bte2.70011, 10.1002/bte2.70124, 10.1002/bte2.70136). |
| RESEARCH FIT | Our study (statistically guaranteed early screening of Li-ion cell cycle life that shortens cycling campaigns) addresses battery testing/qualification, a core battery-engineering cost. Two reviews published in the journal (10.1002/bte2.70136, 10.1002/bte2.70099) explicitly identify uncertainty-aware lifetime prediction as an open need. |
| KEY AUTHOR GUIDELINES | Wiley author-guidelines page (https://onlinelibrary.wiley.com/page/journal/27681696/homepage/author-guidelines) returned HTTP 403 to every automated tool, so the exact current rules could **not** be read. Known from DOAJ: single-anonymous peer review, plagiarism screening, CC BY licence, ScholarOne submission (mc.manuscriptcentral.com/batteryenergy per a search result), a journal Word template "BTE2-article-template" exists. Manuscript prepared to Wiley's standard requirements for its open-access research journals: title page, abstract, keywords, numbered sections, numbered references, Acknowledgments, Author Contributions, Conflict of Interest statement, Data Availability Statement, figures >= 300 dpi. **Must be checked against the live guideline page before submission.** |
| KEY REJECTION RISKS | (1) Editors may view a statistics/ML method as outside an electrochemistry-heavy readership -> mitigated by framing around test-campaign cost and by electrochemically interpretable features. (2) All datasets are LFP/graphite A123 cells (no cross-chemistry claim possible). (3) Prior early-prediction literature is large (Severson 2019, Attia 2020, many follow-ups) -> contribution must be clearly the *guarantee + test-time* layer, not a better point predictor. (4) Moderate sample sizes (169 + 77 cells). (5) Formatting rules not verified (403). |

Selection rationale (short): among 69 journals whose acceptance times could be computed
from primary metadata, only six had a median <= 100 days; of those, Battery Energy is the
only Q1 journal whose scope contains data-driven battery prognostics and whose published
papers include comparable work. Full comparison: `journal_comparison.md`;
verification details: `journal_verification.md`; journal-paper benchmark:
`journal_benchmark.md`.

## Update 2026-11-20: 72-day acceptance constraint (user requirement)

The user set a maximum of 72 days from submission to final acceptance. A re-check against Crossref
article-history dates (`scripts/acceptance_recheck_2026.py`, output in `data/acceptance_recheck_2026-11-20.txt`)
gives these Battery Energy medians: **85 d (2025, n = 93)** and **86 d (2026, n = 79)**. Only 45% (2025) and
41% (2026) of papers were accepted within 72 days. Battery Energy therefore does **not** meet the 72-day constraint
on its recent median; only its 2024 median (66.5 d, n = 48) was below 72 d.

The extra candidates screened on 2026-11-20 did no better:
* Wiley journals: Advanced Science 115 d, Advanced Intelligent Systems 125 d, EcoMat 97 d, Batteries & Supercaps 78 d,
  Energy Technology 117 d, Int. J. Energy Research 162 d, Carbon Neutralization 90 d, Advanced Energy Materials 88 d
  (all 2026 medians).
* Energy & Environmental Materials met the constraint (69 d), but its scope fit for data-driven prognostics was poor.
* Elsevier journals: acceptance times could not be measured, because sciencedirect.com and elsevier.com returned
  HTTP 403 and Elsevier deposits no history dates in Crossref.
* IOP, OUP and RSC journals: no acceptance times found, because they deposit no history dates in Crossref.

**Decision: the user confirmed Battery Energy on 2026-11-20 ("Battery Energy is fine").** The 72-day target is
recorded as NOT met by the journal's recent median. Faster acceptance is possible but not guaranteed (about 41-45% of
recent papers were accepted within 72 days).
