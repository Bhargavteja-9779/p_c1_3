# Topic discovery and selection record (Phases 1, 2, 4)

All prior-art searches were run with `litsearch.py` (Crossref + arXiv), the Semantic
Scholar / OpenAlex APIs where not rate-limited, and web search. Papers named below were
checked to exist (DOIs/arXiv IDs in `references_verified.json` where cited in the paper).

## 1. Candidate directions considered (internal screen)

Journal shortlist constraint: the verified <= 100-day journals are all materials /
energy / manufacturing journals, so candidates were generated for (a) battery data
science (Battery Energy) and (b) ML for additive manufacturing (Virtual and Physical
Prototyping), plus generic ML candidates that could be framed in either.

| # | Candidate | Data | Main reason for rejection / status |
|---|---|---|---|
| 1 | Censoring-aware (survival) early cycle-life prediction from truncated test campaigns | MATR, HUST | **Rejected — crowded.** Incomplete/unlabelled-cell learning already published: Zhai et al. 2025 (J. Energy Chem., 10.1016/j.jechem.2025.03.011), Guo et al. 2024 (Joule, 10.1016/j.joule.2024.02.020); survival framing in a 2026 SSRN preprint (time-varying Cox network, 18 datasets) and censoring/endpoint evaluation in Li et al. 2026 (Research Square, 10.21203/rs.3.rs-11508938/v1). |
| 2 | Lab-shift few-shot recalibration of lifetime models | MATR->HUST | Rejected as main topic: label-budget adaptation already studied (Li et al. 2026); kept as a sub-experiment. |
| 3 | Physics-structured ML for electrolyte conductivity (Casteel-Amis x VTF) | CALiSol-23 | **Rejected — prior art**: NMI 2025 formulation model already embeds an empirical conductivity equation; also NeurIPS 2025 geometric mixture models, npj CM 2025, Nat. Comput. Sci. 2026. |
| 4 | Physics-scaled hybrid melt-pool geometry model across alloys (MeltpoolNet) | MeltpoolNet | Rejected — crowded (Add. Manuf. Lett. 2024 feature engineering, Appl. Sci. 2025 physics augmentation, IMECE 2023 scaling-law comparison, 2021 two-level PIML, withdrawn 2025 residual-ML preprint). |
| 5 | Study-heterogeneity (mixed-effects) learning on literature-compiled AM data | MeltpoolNet | Rejected — 2026 wave of "grouped validation + conformal calibration" papers on literature data (Information 2026, chemRxiv 2026, Machines 2026); data small/noisy. |
| 6 | Monotone/ordinal process-window classifier + conformal sets | MeltpoolNet classification (1,249 pts, ~16 studies) | Rejected — too little independent data; analytical threshold models exist (Appl. Sci. 2021). |
| 7 | AM fatigue life with run-outs (censored) | none public of adequate size | Rejected — no open S-N dataset with run-outs found. |
| 8 | Conformal UQ for battery SOH estimation | many | Rejected — active (several 2025-2026 conformal-SOH preprints). |
| 9 | Partial-charging-curve SOH estimation | many | Rejected — saturated. |
| 10 | Knee-point prediction | MATR | Rejected — several papers incl. UQ (IEEE TTE 2024). |
| 11 | Leakage audit of battery ML evaluation | multiple | Rejected as main topic (evaluation-only; partly covered by 2026 preprints). |
| 12 | EIS frequency selection for fast SOH | Cambridge EIS | Rejected — existing work, data limited to one lab. |
| 13 | Degradation-mode-informed early lifetime prediction | MATR | Rejected — physics-ML hybrids common (e.g. Wang et al. 2024 Nat. Commun.). |
| 14 | Lattice metamaterial surrogate (self-generated FEM) | simulation only | Rejected — no physical validation, crowded. |
| 15 | L-PBF acoustic-emission cross-material monitoring | EMPA AE data | Rejected — dominated by the data owners' own transfer-learning papers. |
| 16 | **Statistically guaranteed sequential screening of cell cycle life (early go/no-go decisions with error control), calibrated with test campaigns truncated at the specification** | MATR (124) + CLO (45); HUST (77) | **Selected** (see below). |

## 2. Stress test of the selected topic (editor's questions)

| Question | Answer |
|---|---|
| Too incremental? | The contribution is not a better point predictor. It is a decision layer with finite-sample guarantees for a question battery labs actually face ("can we stop cycling this cell and still bound the chance of a wrong pass/fail call?"). No battery paper found provides distribution-free error control for early termination. |
| Already solved? | Early prediction (Severson 2019; Attia 2020; Jiang 2021) gives point predictions or Bayesian posteriors without frequentist error guarantees and evaluates at a fixed checkpoint. UQ papers (IEEE TTE 2023/2024) give intervals without coverage guarantees, and none addresses optional stopping. |
| Merely combining techniques? | Partly built from known statistical ingredients (class-conditional split conformal / Neyman-Pearson thresholds; max-statistic calibration for simultaneous validity). The scientific contributions are the formulation for cycle-life screening, the proof that calibration needs only cells cycled to the specification, the trajectory-normalised calibration, and the quantified test-time/accuracy trade-off on public data. This must be stated honestly in the paper. |
| Objective demonstration possible? | Yes: realised false-pass / false-reject rates over many random splits vs nominal levels; cycles to decision; calibration-campaign duration. |
| Strong baselines? | Full observation; Severson-style fixed-checkpoint point prediction; fixed-checkpoint conformal; naive per-checkpoint sequential conformal; Bonferroni sequential; Bayesian (GP) posterior-threshold sequential rule; several base predictors. |
| Simpler method gives same result? | Tested explicitly (fixed checkpoint, Bonferroni, naive). If the proposed calibration is not better than Bonferroni, that is reported. |
| Real gap? | Yes for the battery domain (search in section 4). Methodologically related work exists outside batteries and is cited (early-exit nested sets, conformal selection, conformalized survival analysis). |
| Engineering only? | Includes a formal guarantee (proposition + proof) and controlled experiments. |
| Dataset too small? | 169 + 77 cells is small in ML terms but large for full-lifetime cycling data; conformal guarantees are finite-sample, and evaluation uses many random splits and cell-level statistics. |
| Leakage risk? | Unit = cell; splits by cell; features use only cycles <= checkpoint; hyper-parameters chosen inside training folds; scale normalisers estimated on training cells only. |
| Improvement vanishes under statistics? | Validity is the primary claim (checked against nominal levels with Monte-Carlo CIs); efficiency claims are tested with paired cell-level tests. |
| Useful beyond one dataset? | Evaluated on two labs (MATR/CLO Stanford-MIT-TRI and HUST) with different protocols; batch-shift and cross-lab experiments test where guarantees break. |
| Enough depth for a journal article? | 8+ experiments, ablations, robustness, generalization, error analysis. |

## 3. Final topic

**Working title:** Distribution-free sequential screening of lithium-ion cell cycle life:
early go/no-go decisions with guaranteed error rates from test campaigns truncated at the
specification.

## 4. Novelty map (prior-art defence)

| Existing work | What it contributes | What it does not do |
|---|---|---|
| Severson et al. 2019 (Nature Energy) | Early-cycle features (dQ(V)) + elastic net; ~9% error at cycle 100; 2-class classification at cycle 5 | No error-rate guarantees; fixed checkpoint; needs full-lifetime training data |
| Attia et al. 2020 (Nature) | Early prediction inside Bayesian optimisation of charging protocols, cutting experiment time | Uses predictions as noisy objectives; no per-cell decision guarantee |
| Jiang et al. 2021 (Joule) | Hierarchical Bayesian prediction of protocol lifetime after few cycles | Bayesian posteriors (model-dependent calibration); protocol-level, not cell-level error control |
| Attia et al. 2021 (JES); Paulson et al. 2022; Fermín-Cueto 2020 | Feature studies, knee prediction | Point predictions |
| IEEE TTE 2023/2024 (knee/RUL with UQ) | Ensembles/Bayesian intervals | No finite-sample coverage; no stopping validity |
| Guo 2024 (Joule); Zhai 2025 (J. Energy Chem.) | Use unlabelled/incomplete cells to improve point prediction | No decision guarantees |
| Li et al. 2026 (preprint) | Endpoint and censoring definitions for fair evaluation | Evaluation protocol, not a decision procedure |
| Conformal SOH preprints (arXiv 2603.24475, 2610.41696) | Conformal intervals for SOH forecasting | SOH not lifetime screening; no sequential/stopping validity; no truncated-calibration result |
| Candès et al. 2023 (JRSSB) conformalized survival analysis | Lower prediction bounds under censoring | Not sequential; not battery |
| Jin & Candès 2023 (JMLR) conformal selection | FDR-controlled selection with conformal p-values | Single time point; FDR not per-cell error |
| Jazbec et al. 2024 early-exit nested sets | Anytime-valid nested prediction sets across exits of a network | Generic ML; not screening with two error types; not battery |
| Tong et al. 2018 (Sci. Adv.) NP classification | Class-conditional type-I error control | Static, single feature set |
| Wald 1945 SPRT | Sequential tests with error control | Needs a likelihood model; we use distribution-free rank calibration over ML scores |
| **This work** | Two-sided sequential screening with class-conditional false-pass/false-reject control valid under the data-dependent stopping time; calibration (and optionally training) from campaigns truncated at the specification L*; quantified test-time savings on two labs | — |
