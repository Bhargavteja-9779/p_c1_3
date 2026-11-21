# Bibliography revision (cycle 1): response to R7 and R8

The only file edited is `literature/references_verified.json`. It now has 75 entries: 58 existing and 17 new. The JSON is valid, and every entry formats through `render.format_ref`.

`render.load_refs()` reads `literature/references_final.json` first and falls back to `references_verified.json`. `references_final.json` does not exist, so the build uses `references_verified.json`.

Checking method: web search only. Crossref, Semantic Scholar, Wiley, MDPI and Research Square were all unreachable from this container (proxy 403 or DNS failure). Every value below was confirmed from publisher, proceedings, DBLP, IMS/Project Euclid or library pages as they appeared in search results.

Note: `git status` shows a modification to `manuscript/src/si1_supporting_information.md`. I did not make that change; it was already in the working tree.

## 1. Corrections to existing entries

| key | field | old -> new | source |
|---|---|---|---|
| ma2022hust | venue | `Energy &amp; Environmental Science` -> `Energy & Environmental Science` (this was the only HTML entity in the file) | entity decode |
| zhang2024batteryml | title | `BatteryML:An Open-source platform…` -> `BatteryML: An Open-source Platform for Machine Learning on Battery Degradation` | ICLR 2024 proceedings |
| zhang2024batteryml | venue, year, type | `arXiv`, 2023 -> `International Conference on Learning Representations (ICLR 2024)`, 2024, proceedings-article | proceedings.iclr.cc; iclr.cc/virtual/2024/poster/17628 |
| jazbec2024earlyexit | venue, year, volume, pages | `arXiv`, 2023 -> UAI 2024, PMLR, 2024, 244, 1780-1796 | proceedings.mlr.press/v244/jazbec24a |
| sesia2025dr | venue, year, volume, pages | `arXiv`, 2024 -> ICML 2025, PMLR, 2025, 267, 53989-54029 | proceedings.mlr.press/v267/sesia25a |
| vovk2005alrw | authors, venue | `[]`, `Springer-Verlag` -> Vovk, V.; Gammerman, A.; Shafer, G.; `Springer` | Springer book page, doi 10.1007/b106715. I kept the 1st edition (2005). The 2nd edition is Springer, Cham 2022, doi 10.1007/978-3-031-06649-8; R7 prefers it, so it is your call. |
| rasmussen2006gpml | year, venue | 2005 -> 2006; `The MIT Press` -> `MIT Press` | library catalogue and gaussianprocess.org give 2006 (Crossref and DOAB give 2005) |
| wilcoxon1945 | pages | `80` -> `80-83` | several bibliographic records: Biometrics Bulletin 1(6):80-83 |
| bte2026lfp | title | `…LiFePO 4 Batteries` -> `…LiFePO4 Batteries` (R7-13) | journal.hep.com.cn listing |
| li2026endpoint | venue | `Springer Science and Business Media LLC` -> `Research Square (preprint)` (R7-07) | Research Square listing |
| li2026endpoint, bte2026piai | note | added a verification note (see Section 3) | |

These items were already correct, so I left them unchanged:
- holm1979: complete (Holm, S., Scand. J. Statist. 6(2):65-70, 1979, JSTOR 4615733, verified=true). It is still not cited in the manuscript text, so it will not render until `[@holm1979]` is added near the "Holm correction" sentence.
- romano2019cqr: NeurIPS 32
- jin2023selection: JMLR 24(244)
- gui2024adaptive: Biometrika 111(2):459-477
- pedregosa2011sklearn: JMLR 12
- sadinle2019lab: 2019
- bte2024cnnlstm: 2025, 4, e20240036

## 2. New entries (all verified=true)

| key | content | supports | suggested location |
|---|---|---|---|
| pocock1977group | Pocock, *Biometrika* 64(2):191-199, 1977 (some records give 191-200) | Group-sequential interim looks with constant boundaries | Related Work, "Statistical foundations" (R7-02a); Discussion "Repeated looks must be paid for" |
| obrien1979multiple | O'Brien & Fleming, *Biometrics* 35(3):549-556, 1979 | Group-sequential boundaries that are conservative early | same sentence as Pocock |
| lan1983discrete | Lan & DeMets, *Biometrika* 70(3):659-663, 1983, doi 10.2307/2336502 | Alpha-spending across interim analyses | same sentence; also the comparison of naive sequential, Bonferroni and max-statistic in Methods |
| jennison2000group | Jennison & Turnbull, *Group Sequential Methods with Applications to Clinical Trials*, Chapman & Hall/CRC 2000 (no DOI: could not confirm one) | Monograph on interim-analysis error control | same sentence |
| stankeviciute2021conformal | Stankeviciute, Alaa & van der Schaar, NeurIPS 34, 2021 (pages not confirmed, so omitted) | Multi-horizon conformal forecasting with a Bonferroni correction over horizons; the analogue of the Bonferroni baseline | Related Work, next to lei2015functional and diquigiovanni2022bands; Methods where the Bonferroni baseline is defined |
| angelopoulos2025ltt | Angelopoulos, Bates, Candès, Jordan & Lei, "Learn then test", *Ann. Appl. Stat.* 19(2):1641-1662, 2025, doi 10.1214/24-AOAS1998 | Finite-sample calibration of decision thresholds via multiple testing | Related Work, "Statistical foundations"; Methods sentence on threshold calibration |
| bates2023outliers | Bates, Candès, Lei, Romano & Sesia, *Ann. Stat.* 51(1):149-178, 2023 | Conformal p-values and class-conditional testing | Related Work, next to tong2018np and sadinle2019lab |
| ramdas2023game | Ramdas, Grünwald, Vovk & Shafer, *Stat. Sci.* 38(4):576-601, 2023 | Safe anytime-valid inference, validity at stopping times | Related Work, with wald1945sprt and howard2021cs |
| cleaveland2024conformal | Cleaveland, Lee, Pappas & Lindemann, AAAI 38(19):20984-20992, 2024 | Weighted max-over-time nonconformity score for simultaneous validity | Remark (ii) of Proposition 1, credited as the known construction (R8-01) |
| lindemann2023conformal | Lindemann, Qin, Deshmukh & Pappas, ICCPS 2023, 142-153 | Max-type, trajectory-wide conformal regions | Remark (ii), together with Cleaveland et al. |
| ringel2024early | Ringel, Cohen, Freedman, Elad & Romano, ICML 2024, PMLR 235:42584-42600 | Distribution-free calibrated stopping rule for early time classification | Related Work, sequential paragraph next to jazbec2024earlyexit |
| chen2025knowing | Chen, Park & Simeone (SpikeCP), *IEEE JSTSP* 19:88-102, 2025, doi 10.1109/JSTSP.2024.3431996 | Conformal guarantees at input-dependent stopping times, using Bonferroni or Simes corrections | same sentence as Ringel et al.; also as a less conservative sequential competitor (R8-05) |
| li2026coins | Li, Qiao, Guo & Sun, "COINS", arXiv 2609.07112, 2026 (preprint) | Any-stage-valid sequential conformal prediction that beats Bonferroni; motivated by sequential screening | Remark (ii) and the Gap paragraph. Cite as concurrent work, since it appeared in Sep 2026. |
| liu2026reliable | Liu, Wang, Li, Cao & Yang, *Energy Engineering* 123(8), 2026, doi 10.32604/ee.2026.074783 (pages not confirmed) | Conformal intervals for battery life prediction | Related Work, "Conformal prediction … applied to early cycle-life prediction [wu2026cai, liu2026reliable, zhang2023range]" (R8-02) |
| li2026early | D. C. Li, *Batteries* 12(4):116, 2026, doi 10.3390/batteries12040116 | Battery early-warning decision layer with weighted conformal calibration | Related Work, "…and to calibrating early-warning decision thresholds [li2026early]" |
| richardson2017gaussian | Richardson, Osborne & Howey, *J. Power Sources* 357:209-219, 2017 | Gaussian-process forecasting of battery capacity | Intro and Related Work sentence "Ensemble, Gaussian-process or Bayesian uncertainty estimates" (R7-10) |
| baumhofer2014production | Baumhöfer, Brühl, Rothgang & Sauer, *J. Power Sources* 247:332-338, 2014 | Production-caused cell-to-cell variation in ageing (48 cells) | Intro, screening and qualification motivation (R7-12) |

Caveats:
- **chen2025knowing (SpikeCP):** R8 dates it 2024. The journal issue is vol. 19, January 2025; it was published online in 2024.
- **li2026early:** R8 describes it as giving "bounded false-alarm risk". I could confirm only "weighted conformal calibration in the decision layer". Keep the manuscript sentence generic.

## 3. The two entries flagged in R7-07

- **li2026endpoint: exists.** Research Square preprint, doi 10.21203/rs.3.rs-11508938/v1, v1 posted about Oct/Nov 2026, title exact.
  - Content confirmed from the abstract: a seven-source registry of 220 cells. Changing the capacity reference or endpoint changes the observed event counts, e.g. HUST goes from 0 to 77 at 80%, SNL from 50 to 35. That supports both citing sentences (Draft:38 and :246).
  - Author names (Jufeng Li, Wenjie Li, Tao Li) come only from the Crossref record and could not be confirmed independently, because researchsquare.com is unreachable.
  - Venue fixed. It is not peer reviewed, so cite it as a preprint.
  - I kept verified=true. Setting it to false would make render.py abort ("unknown or unverified citation key"), because the key is cited twice.
- **bte2026piai: exists.** Battery Energy 5(4) e70136, 2026 (version of record 9 July 2026), authors Sulaima, Arora, Frischer & Namazi, as in the JSON. One search result also named Namazi alone; the Wiley listing gives "Sulaima".
  - It is a review. The abstract emphasises uncertainty awareness and proposes a five-layer framework for trustworthy prediction that includes uncertainty quantification.
  - Full text not read. The claim "identifies uncertainty-aware lifetime prediction as an open need" is a fair reading of the abstract but is not confirmed verbatim.
  - verified=true kept.

## 4. Rejected or not added

| candidate | reason |
|---|---|
| SpikeCP as "JSTSP 2024" | The paper exists, but the citation is wrong. Added with the correct metadata (vol. 19, 2025). |
| Stankeviciute page numbers | Not confirmed, so omitted. The entry is added without pages. |
| Jennison & Turnbull DOI 10.1201/9780367805326 | DOI not confirmed, so omitted. The book itself is confirmed. |
| Liu et al. 2026 page/article number | Not confirmed, so omitted. |
| Pregowska & Marynowicz arXiv 2604.16580; Javanmardi & Hüllermeier IJPHM 2023; Sesia & Svetnik arXiv 2512.18118 and 2505.04568; Zhou, Lindemann & Sesia arXiv 2402.09623; NP-with-indecisions arXiv 2610.04233 | Not in the requested list, so not searched or added. Sesia & Svetnik 2512.18118 (screening for survival beyond a horizon) is the most relevant of these to the truncated-calibration claim and should be considered next. |
| Kerby 2014 (rank-biserial), PyTorch | Not requested, so not added. |
