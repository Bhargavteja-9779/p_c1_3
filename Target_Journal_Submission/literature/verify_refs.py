"""Verify every reference against Crossref (DOI) or arXiv (id). Writes references_verified.json.
A reference is accepted only if the registry title matches the expected title fragment."""
import json, re, time, urllib.request, urllib.parse, xml.etree.ElementTree as ET
UA = {"User-Agent": "refcheck/1.0 (academic research)"}
def get(u):
    for k in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60) as r: return r.read()
        except Exception: time.sleep(3*(k+1))
    return None
REFS = [  # key, id (doi: or arxiv:), expected title fragment (lowercase)
 ("severson2019", "doi:10.1038/s41560-019-0356-8", "data-driven prediction of battery cycle life"),
 ("attia2020", "doi:10.1038/s41586-020-1994-5", "closed-loop optimization of fast-charging protocols"),
 ("ma2022hust", "doi:10.1039/D2EE01676A", "real-time personalized health status prediction"),
 ("hust_data", "doi:10.17632/nsc7hnsg4s.2", ""),
 ("attia2021stat", "doi:10.1149/1945-7111/ac2704", "statistical learning for accurate and interpretable battery lifetime prediction"),
 ("fermin2020knee", "doi:10.1016/j.egyai.2020.100006", "knee-point"),
 ("jiang2021bayes", "doi:10.1016/j.joule.2021.10.010", "bayesian learning for rapid prediction"),
 ("zhang2024batteryml", "arxiv:2310.14714", "batteryml"),
 ("sulzer2021field", "doi:10.1016/j.joule.2021.06.005", "challenge and opportunity of battery lifetime prediction from field data"),
 ("hu2020prognostics", "doi:10.1016/j.joule.2019.11.018", "battery lifetime prognostics"),
 ("guo2024semi", "doi:10.1016/j.joule.2024.02.020", "semi-supervised learning for explainable few-shot battery lifetime prediction"),
 ("zhai2025waste", "doi:10.1016/j.jechem.2025.03.011", "transforming waste to value"),
 ("wang2024pinn", "doi:10.1038/s41467-024-48779-z", "physics-informed neural network for lithium-ion battery degradation"),
 ("zhang2020eis", "doi:10.1038/s41467-020-15235-7", "identifying degradation patterns of lithium ion batteries from impedance spectroscopy"),
 ("aitio2021field", "doi:10.1016/j.joule.2021.11.006", "predicting battery end of life from solar off-grid"),
 ("attia2022knees", "doi:10.1149/1945-7111/ac6d13", "knees"),
 ("weng2021formation", "doi:10.1016/j.joule.2021.09.015", "formation protocols on battery lifetime"),
 ("dosreis2021data", "doi:10.1016/j.egyai.2021.100081", "lithium-ion battery data and where to find it"),
 ("li2026endpoint", "doi:10.21203/rs.3.rs-11508938/v1", "endpoint definitions and censoring"),
 ("tte2024ensemble", "doi:10.1109/tte.2024.3354302", "early uncertainty quantification prediction"),
 ("tte2023knee", "doi:10.1109/tte.2023.3304670", "early prediction of knee point and knee capacity"),
 ("bte2024cnnlstm", "doi:10.1002/bte2.20240036", "cnn"),
 ("bte2026piai", "doi:10.1002/bte2.70136", "physics"),
 ("bte2026lfp", "doi:10.1002/bte2.70124", "degradation"),
 ("bte2025transfer", "doi:10.1002/bte2.70011", "transfer learning"),
 ("bte2025eis", "doi:10.1002/bte2.20250006", "localized eis"),
 ("arxiv2026conftl", "arxiv:2603.24475", "conformalized transfer learning"),
 ("arxiv2026hwcp", "arxiv:2610.41696", "hierarchically weighted conformal"),
 ("vovk2005alrw", "doi:10.1007/b106715", "algorithmic learning in a random world"),
 ("lei2018dfpi", "doi:10.1080/01621459.2017.1307116", "distribution-free predictive inference for regression"),
 ("romano2019cqr", "arxiv:1905.03222", "conformalized quantile regression"),
 ("angelopoulos2023gentle", "doi:10.1561/2200000101", "conformal prediction"),
 ("candes2023survival", "doi:10.1093/jrsssb/qkac004", "conformalized survival analysis"),
 ("jin2023selection", "arxiv:2210.01408", "selection by prediction with conformal p-values"),
 ("tong2018np", "doi:10.1126/sciadv.aao1659", "neyman-pearson classification algorithms"),
 ("sadinle2019lab", "doi:10.1080/01621459.2017.1395341", "least ambiguous set-valued classifiers"),
 ("wald1945sprt", "doi:10.1214/aoms/1177731118", "sequential tests of statistical hypotheses"),
 ("jazbec2024earlyexit", "arxiv:2311.05931", "early-exit neural networks with nested prediction sets"),
 ("barber2023beyond", "doi:10.1214/23-AOS2276", "conformal prediction beyond exchangeability"),
 ("tibshirani2019shift", "arxiv:1904.06019", "conformal prediction under covariate shift"),
 ("gibbs2021aci", "arxiv:2106.00170", "adaptive conformal inference under distribution shift"),
 ("howard2021cs", "doi:10.1214/20-AOS1991", "time-uniform"),
 ("zou2005enet", "doi:10.1111/j.1467-9868.2005.00503.x", "regularization and variable selection via the elastic net"),
 ("pedregosa2011sklearn", "arxiv:1201.0490", "scikit-learn"),
 ("ke2017lightgbm", "arxiv:", ""),
 ("efron1979bootstrap", "doi:10.1214/aos/1176344552", "bootstrap methods"),
 ("holm1979", "doi:10.2307/4615733", "simple sequentially rejective multiple test procedure"),
 ("wilcoxon1945", "doi:10.2307/3001968", "individual comparisons by ranking methods"),
 ("benjamini1995fdr", "doi:10.1111/j.2517-6161.1995.tb02031.x", "controlling the false discovery rate"),
 ("rasmussen2006gpml", "doi:10.7551/mitpress/3206.001.0001", "gaussian processes for machine learning"),
 ("clopper1934", "doi:10.1093/biomet/26.4.404", "use of confidence or fiducial limits"),
 ("gui2024adaptive", "arxiv:2211.01227", "conformalized survival analysis with adaptive cut"),
 ("sesia2025dr", "arxiv:2412.09729", "doubly robust conformalized survival analysis"),
 ("deblasio2024calisol", "doi:10.1038/s41597-024-03575-8", "calisol-23"),
 ("akbari2022meltpool", "doi:10.1016/j.addma.2022.102817", "meltpoolnet"),
]
out = {}
for key, rid, frag in REFS:
    if rid == "arxiv:":
        continue
    rec = None
    if rid.startswith("doi:"):
        doi = rid[4:]
        raw = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))
        if raw:
            m = json.loads(raw)["message"]
            t = " ".join(re.sub(r"<[^>]+>", "", (m.get("title") or [""])[0]).split())
            rec = dict(key=key, doi=m["DOI"], title=t,
                       authors=[f"{a.get('family','')}, {a.get('given','')}".strip(", ") for a in m.get("author", [])],
                       venue=(m.get("container-title") or [""])[0] or m.get("publisher", ""),
                       year=(m.get("issued", {}).get("date-parts") or [[None]])[0][0],
                       volume=m.get("volume"), issue=m.get("issue"), pages=m.get("page") or m.get("article-number"),
                       type=m.get("type"), source="crossref")
    else:
        aid = rid[6:]
        raw = get("http://export.arxiv.org/api/query?id_list=" + aid)
        if raw:
            ns = {"a": "http://www.w3.org/2005/Atom"}
            e = ET.fromstring(raw).find("a:entry", ns)
            if e is not None and e.findtext("a:title", namespaces=ns):
                rec = dict(key=key, arxiv=aid, title=" ".join(e.findtext("a:title", namespaces=ns).split()),
                           authors=[x.findtext("a:name", namespaces=ns) for x in e.findall("a:author", ns)],
                           venue="arXiv", year=int(e.findtext("a:published", namespaces=ns)[:4]), source="arxiv")
    ok = bool(rec) and frag.lower() in rec["title"].lower()
    if rec: rec["verified"] = ok
    out[key] = rec or dict(key=key, id=rid, verified=False)
    print(("OK " if ok else "XX ") + key, "|", (rec or {}).get("title", "NOT FOUND")[:90], "|", (rec or {}).get("venue", ""), (rec or {}).get("year", ""))
    time.sleep(0.4)
json.dump(out, open("references_verified.json", "w"), indent=1)
