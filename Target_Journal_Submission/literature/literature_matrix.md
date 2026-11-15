# Literature matrix (Phase 3)

Scope: early cycle-life prediction / screening of Li-ion cells, uncertainty quantification
for battery lifetime, and the statistical methods our procedure builds on. All entries are
in `references_verified.json` (DOI/arXiv verified against Crossref/arXiv). Cells marked
"n/c" = not checked (full text not accessed); we do not state details we did not verify.
Abstract-level details of Battery Energy papers are in
`../journal_selection/journal_benchmark.md`.

## A. Battery cycle-life prediction and testing

| Paper | Year / venue | Problem | Data (size) | Method | Uncertainty / error guarantee | Evaluation protocol | Gap relative to this work |
|---|---|---|---|---|---|---|---|
| Severson et al. | 2019, Nature Energy | Predict cycle life from early cycles | 124 LFP/graphite A123 cells, 72 fast-charge policies (public) | dQ(V) features between cycles 10 and 100, elastic net; also binary classification at cycle 5 | None (point prediction; classification accuracy) | Fixed train / primary test / secondary test split | Single fixed checkpoint, no error-rate control, full-lifetime labels needed |
| Attia et al. | 2020, Nature | Fast-charge protocol optimisation | Early-prediction model + Bayesian optimisation; 45-cell validation batch (public, used here as CLO) | Early prediction (cycle 100) feeding closed-loop BO | Prediction errors treated as noise in BO | Validation of top protocols | Protocol-level optimisation, not per-cell decisions with guaranteed error |
| Jiang et al. | 2021, Joule | Rapid protocol lifetime prediction | Fast-charge LFP data | Hierarchical Bayesian model using few early cycles | Bayesian posterior (model-dependent) | Held-out protocols | No frequentist / distribution-free guarantee; protocol-level |
| Attia et al. | 2021, J. Electrochem. Soc. | Interpretable lifetime prediction | Severson data | Statistical learning, feature analysis | n/c | n/c | Point prediction |
| Fermín-Cueto et al. | 2020, Energy and AI | Knee-point / knee-onset prediction | Severson data | ML on early-cycle features | n/c | n/c | Different target (knee), no decision guarantee |
| Ma et al. (HUST) | 2022, Energy Environ. Sci. | Personalised health-status prediction | 77 A123 cells, 77 discharge protocols (public, used here) | Deep transfer learning | n/c | n/c | Point prediction |
| Zhang et al. (BatteryML) | 2023, arXiv (ICLR 2024) | Open platform / benchmark | MATR, HUST, CALCE, RWTH, SNL, ... | Many baselines | No guarantee | Benchmark splits | Benchmarks point accuracy |
| Weng et al. | 2021, Joule | Lifetime impact of formation protocols | Own cells | Early diagnostics after formation | n/c | n/c | Different decision point (post-formation) |
| Guo et al. | 2024, Joule | Few-shot lifetime prediction | Public datasets | Semi-supervised learning with unlabelled cells | n/c | n/c | Uses incomplete cells for accuracy; no decision guarantee |
| Zhai et al. | 2025, J. Energy Chem. | Use incomplete (unfinished) cells | n/c | Incomplete-data learning | n/c | n/c | Point accuracy, not error-controlled screening |
| Li, Li, Li (preprint) | 2026, Research Square | Endpoints and censoring in evaluation | 7 sources, 220 cells | Evaluation procedure, calibration with few labels | Cohort-level error bounds | Exhaustive label allocations | Evaluation protocol, not a sequential decision rule |
| Sulzer et al. | 2021, Joule | Field-data lifetime prediction | Perspective | — | Discusses uncertainty and censoring | — | Motivation |
| Hu et al. | 2020, Joule | Lifetime prognostics review | Review | — | — | — | Motivation |
| IEEE TTE 2024 (transformer ensemble) | 2024, IEEE Trans. Transp. Electrif. | Early RUL with UQ | n/c | Ensemble | Ensemble intervals, no finite-sample guarantee | n/c | No guarantee, no stopping validity |
| IEEE TTE 2023/2024 (knee with UQ) | 2024, IEEE Trans. Transp. Electrif. | Early knee prediction with UQ | Fast-charge data | n/c | UQ without coverage guarantee | n/c | As above |
| Battery Energy 2026 (10.1002/bte2.70124) | 2026, Battery Energy | LFP cycle life from temperature features | n/c (abstract: ~96,700 cycles) | Gradient boosting | Not stated | n/c | Point prediction |
| Battery Energy 2026 review (10.1002/bte2.70136) | 2026, Battery Energy | Physics-informed AI for lifetime | Review | — | Calls for uncertainty-aware prediction | — | Motivation |
| Conformal SOH preprints (arXiv 2603.24475; 2610.41696) | 2026, arXiv | SOH forecasting with conformal intervals | Public data | Conformal prediction | Marginal coverage for SOH | n/c | Not lifetime screening; no sequential stopping, no truncated calibration |

## B. Statistical foundations

| Paper | Contribution used here |
|---|---|
| Vovk, Gammerman, Shafer (2005, book) | Conformal prediction; rank-based finite-sample validity under exchangeability |
| Lei et al. (2018, JASA) | Split conformal regression |
| Romano et al. (2019, NeurIPS / arXiv) | Conformalised quantile regression (related baseline family) |
| Angelopoulos & Bates (2023, Found. Trends ML) | Tutorial; split-conformal quantile rule |
| Sadinle, Lei, Wasserman (2019, JASA) | Class-conditional (Mondrian-type) set-valued classification with bounded error |
| Tong, Feng, Li (2018, Sci. Adv.) | Neyman-Pearson classification: type-I error control via order statistics |
| Candès, Lei, Ren (2023, JRSSB); Gui et al. (2022 arXiv); Sesia & Svetnik (2024 arXiv) | Conformal lower prediction bounds under censoring — related idea of using T truncated at a cut-off |
| Jin & Candès (2022/2023, arXiv/JMLR) | Conformal selection with FDR control (different error notion) |
| Jazbec et al. (2023, arXiv) | Anytime-valid nested prediction sets for early-exit networks — closest methodological relative (sequential validity over exits) |
| Howard et al. (2021, Ann. Stat.) | Time-uniform confidence sequences (anytime validity) |
| Wald (1945, Ann. Math. Stat.) | Sequential probability ratio test (likelihood-based sequential error control) |
| Barber et al. (2023, Ann. Stat.); Tibshirani et al. (2019); Gibbs & Candès (2021) | Conformal prediction under non-exchangeability / shift (context for the batch-shift results) |

## C. Gaps identified

* **Methodological**: no battery lifetime method gives *finite-sample, distribution-free*
  per-cell error control; none addresses validity when testing stops at a data-dependent
  time.
* **Experimental**: early-prediction studies evaluate at a fixed checkpoint and report point
  error; the error rate of an actual screening *decision* and the cycles it saves are rarely
  reported.
* **Data-acquisition**: calibration of interval methods needs full-lifetime cells; the fact
  that class-conditional screening needs only cells cycled to L* has not been exploited.
* **Statistical-validation**: single splits and best-run reporting are common; we use 1,000
  random splits, Monte-Carlo CIs and cell-level paired tests.
* **Generalisation**: guarantees under batch/lab shift are not studied.
