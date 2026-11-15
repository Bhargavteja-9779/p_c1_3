# Battery Energy (Wiley, eISSN 2768-1696): benchmark of how well its data-driven battery health and lifetime papers are made

Prepared 2026-11-15 for the planned submission on *distribution-free (conformal) lower
prediction bounds for Li-ion cycle life from early cycles, calibrated with right-censored
test campaigns and valid under sequential early termination* (MATR/CLO and HUST LFP data).

---

## 0. Sources, scope and limits (read first)

* **Source.** `journal_papers/battery_energy_relevant.json`, built by
  `scripts/journal_papers.py` from the Crossref REST API (`/journals/2768-1696/works`).
  Crossref lists **422** works for the journal. A keyword regex on title and abstract
  (SOH, lifetime, RUL, degradation, ageing, SOC, BMS, machine learning, neural, EIS, ...)
  kept **31** papers. All 31 have a Crossref-deposited abstract. All 31 abstracts were read
  in full.
* **Full texts were NOT accessible.** Wiley Online Library returned **HTTP 403** to automated
  requests for both `/doi/full/` and `/doi/pdf/` (tested 2026-11-15 on 10.1002/bte2.70124),
  which matches the earlier finding in `journal_verification.md`. **Everything below comes from
  abstracts and Crossref metadata only.** "Not stated in abstract" means only that: the full
  text may well contain baselines, statistics, data details or code links that the abstract
  leaves out. The benchmark is therefore a *lower bound* on the evidence these papers contain.
* **Conventions.** Text in quotation marks is copied from the abstract. **Obs.** = our own
  observation about what the abstract does or does not say, not a claim by the authors.
  **[inference, unverified]** = our interpretation, not confirmed by the abstract.
  "n/s" = not stated in abstract.
* **Metadata caveats.**
  * *Cites* is Crossref `is-referenced-by-count` at harvest time. It is usually lower than
    Scopus or Google Scholar counts, and older papers have had longer to collect citations.
  * The harvest script stored at most the first 6 authors.
  * *Days* = Crossref `accepted` minus `received`, in calendar days. It includes revision
    rounds. For a transferred manuscript, "received" may be the transfer date.
  * The keyword filter is not a full census: a data-driven paper whose title and abstract
    match none of the keywords would be missing.

---

## 1. Selection (22 of 31)

| Group | Definition | Papers (ID = index in the JSON `relevant` list) |
|---|---|---|
| **A** | Data-driven or ML work on state, health or lifetime (original research) | BE-02, BE-03, BE-07, BE-10, BE-16, BE-21, BE-22, BE-23, BE-28 (9) |
| **B** | Model-based state estimation, control, stochastic BESS modelling | BE-19, BE-24, BE-25, BE-26 (4) |
| **C** | Experimental or physics-based degradation, ageing and cycle-life diagnostics | BE-01, BE-04, BE-06, BE-08, BE-15 (5) |
| **D** | Reviews and perspectives on ML, BMS, lifetime and prognostics | BE-11, BE-18, BE-20, BE-27 (4) |

**Excluded (9) as materials or off-topic for state, health or lifetime:**
* BE-00 molybdate supercapacitor review, 10.1002/bte2.20240073
* BE-05 X-ray imaging review, 10.1002/bte2.20230043
* BE-09 LiFePO4 hydrothermal-synthesis review, 10.1002/bte2.20250021
* BE-12 ASSB failure-mechanism review, 10.1002/bte2.70112
* BE-13 ethanol biosensor ML, 10.1002/bte2.20240044
* BE-14 2D-perovskite phase classification, 10.1002/bte2.20240040
* BE-17 Ni-rich cathode phase in thermal runaway, 10.1002/bte2.20220036
* BE-29 perovskite solar-cell high-throughput review, 10.1002/bte2.70127
* BE-30 ASSB interface review, 10.1002/bte2.70137

*Note:* BE-14, although off-topic, is the **only one of the 31 abstracts** that states a
validation protocol: "10-fold stratified cross-validation", Optuna tuning, SHAP and "balance
accuracy (0.83) on independent test data set". So the journal has published ML work that
spells out its validation protocol.

---

## 2. Overview of the 22 selected papers

| ID | DOI | First author (year) | Topic | Data (as stated in abstract) | Headline numbers in abstract | Cites | Received → Accepted (days) |
|---|---|---|---|---|---|---|---|
| BE-02 | 10.1002/bte2.20240036 | Xiao (2024) | CNN-LSTM SOH from charging-voltage deviation | n/s | none | 25 | 2024-08-27 → 2024-12-05 (100) |
| BE-03 | 10.1002/bte2.20240088 | Zhao (2025) | 2-D CNN prediction of dendrite growth | n/s | none | 21 | 2024-11-14 → 2025-02-28 (106) |
| BE-07 | 10.1002/bte2.20250006 | Thomas (2025) | NN capacity/SOH from a few selected EIS frequencies | "publicly available data set" (unnamed); "simulated cell" | MAPE as low as 0.94 %; EIS time −93 % | 13 | 2025-01-31 → 2025-03-11 (39) |
| BE-10 | 10.1002/bte2.70011 | Lyu (2025) | Dual GPR + transfer learning + particle filter, pack SOH | Univ. of Maryland open cell data + private packs | mean RMSE 0.87 (unit n/s) | 10 | 2024-12-30 → 2025-02-18 (50) |
| BE-16 | 10.1002/bte2.70073 | Qays (2026) | HFF-GRU-H∞ SoC estimation + cell balancing | "real-world" profiles (source n/s); 3 cells balanced | 0.043 % SoC error; 0.477 s; pack life +27.7 % | 8 | 2025-05-28 → 2025-11-27 (183) |
| BE-21 | 10.1002/bte2.70122 | Warren (2026) | Tree models on in situ EIS, solid-state cells | in situ EIS (source/size n/s) | R² > 0.99; 5 features keep sub-percent accuracy; ms-scale | 4 | 2026-02-05 → 2026-04-22 (76) |
| BE-22 | 10.1002/bte2.20250019 | Khoury (2025) | ANN-based EMS to preserve BESS SOH | n/s | MAE 6.43 %; SOH 33 % vs 20 %; blackout −56 % (−5203 h) | 3 | 2025-04-02 → 2025-05-22 (50) |
| BE-23 | 10.1002/bte2.20250052 | Rajabzadeh (2025) | Exp. smoothing + LSTM + DLSA tuning, RUL/EoL | NASA PCoE | capacity error < ±0.002 Ah | 2 | 2025-06-27 → 2025-10-07 (102) |
| BE-28 | 10.1002/bte2.70124 | Kee (2026) | Temperature features + GBM, LFP cycle life | open-source, 96,700 cycles, LFP/graphite, fast charging | no accuracy number | 1 | 2026-01-22 → 2026-05-07 (105) |
| BE-24 | 10.1002/bte2.70072 | Nohra (2026) | H∞/H2 (LMI) + sliding-mode SOC/SOH | numerical simulation (UDDS, US06, HWFET) | none | 2 | 2025-08-21 → 2025-11-28 (99) |
| BE-25 | 10.1002/bte2.70093 | Asadi (2026) | 2nd-order sliding-mode observer SoC | theory + simulation | none | 2 | 2025-10-28 → 2026-01-23 (87) |
| BE-26 | 10.1002/bte2.70080 | Gebennini (2026) | Markov-chain BESS with SOC-dependent efficiency | illustrative numerical study | none | 2 | 2025-10-23 → 2025-12-17 (55) |
| BE-19 | 10.1002/bte2.70075 | Iqbal (2025) | Multi-agent hierarchical SoC balancing, DC ship microgrid | Simulink + HIL | none | 6 | 2025-10-01 → 2025-12-08 (68) |
| BE-01 | 10.1002/bte2.20220052 | Ando (2023) | Sulfide all-solid-state cell degradation (100 °C cycling) | prototype cell(s), number n/s | none (100 °C test) | 26 | 2022-10-05 → 2022-12-12 (68) |
| BE-04 | 10.1002/bte2.20210001 | Rahil (2022) | Second-life PHEV pack in grid duty cycles | one retired PHEV pack tested | untracked time 4 %, 14 %, 11 % vs 2 % limit; 6 h 23 min of 10 h | 19 | 2021-08-17 → 2022-03-08 (203) |
| BE-06 | 10.1002/bte2.20250043 | Chen (2025) | Electrochem.-mechanical model with side reactions, high-T life | aged cells + high-T cycling data (size n/s) | none | 15 | 2025-06-08 → 2025-09-28 (112) |
| BE-08 | 10.1002/bte2.70008 | Yang (2025) | Overdischarge depth vs ageing and thermal safety, NCM523 | NCM523/graphite cells (number n/s) | capacity decay 38.2 % at 0.5 V cut-off | 11 | 2024-12-18 → 2025-02-11 (55) |
| BE-15 | 10.1002/bte2.20240107 | Wang (2025) | Separator geometry vs Zn-anode cycle life | Zn-metal cells (number n/s) | none | 8 | 2024-12-09 → 2025-03-14 (95) |
| BE-11 | 10.1002/bte2.70099 | Ametefe (2026) | Perspective: system-level intelligent battery systems | review (184 refs) | none | 10 | 2026-01-07 → 2026-02-16 (40) |
| BE-18 | 10.1002/bte2.70067 | Helaley (2025) | Review: chemical-engineering principles in BMS safety | review (39 refs) | >60 °C; SoH up to +20 % (reported by the review) | 6 | 2025-09-14 → 2025-11-18 (65) |
| BE-20 | 10.1002/bte2.70136 | Sulaima (2026) | Review: physics-informed AI for degradation/lifetime | review (145 refs) | none | 6 | 2026-02-05 → 2026-06-10 (125) |
| BE-27 | 10.1002/bte2.70149 | Maddipatla (2026) | Review: early detection of thermal runaway | review (134 refs) | none | 2 | 2026-01-27 → 2026-08-12 (197) |

---

## 3. Per-paper records (abstract-based)

Every record covers 16 fields:
1. research problem
2. gap claimed
3. novelty
4. methodological contribution
5. dataset
6. experimental design
7. baselines
8. quantitative results
9. ablation
10. statistical validation
11. robustness
12. generalization
13. computational complexity
14. limitations
15. reproducibility/code
16. fit

Fields that the abstract does not address are grouped under **Not stated in abstract**.

### Group A: Data-driven state, health and lifetime papers

#### BE-02 · Xiao et al. 2024: "A CNN-LSTM Method Based on Voltage Deviation for Predicting the State of Health of Lithium-Ion Batteries"
DOI 10.1002/bte2.20240036 · cites 25 · refs 51 · 100 days
* **Problem:** SOH estimation of LIBs for reliable and safe BMS operation.
* **Gap claimed:** despite deep-learning advances, "the intricate nature of the battery degradation process poses a challenge in accurately simulating it using measurement data."
* **Novelty (claimed):** a new input, the "charging voltage deviation": the gap between the charging voltage and its average over each cycle. The authors argue it is "rooted in the electrochemical reactions that lead to capacity decay and voltage fluctuations."
* **Method:** a CNN-LSTM hybrid. In each cycle a CNN extracts capacity features from sequential charging data (voltage deviation, current, charging duration). An LSTM then models the long-term dependencies of capacity to predict SOH.
* **Experimental design:** "experimental results" are mentioned; the design is n/s.
* **Quantitative results:** none. The abstract says only that the model "simplifies the computational complexity" and "significantly enhances the precision".
* **Computational complexity:** claimed to be lower; not quantified.
* **Not stated in abstract:** dataset (source, public or own, size); named baselines (Obs.: "enhances" implies a comparator that is not named); ablation; statistical validation (Obs.: "significantly" is used without a stated test); robustness; generalization; limitations; code.
* **Fit:** core BMS SOH estimation with deep learning and a physically motivated feature. It is the most cited data-driven paper in the set.

#### BE-03 · Zhao et al. 2025: "Insights Into Dendritic Growth Mechanisms in Batteries: A Combined Machine Learning and Computational Study"
DOI 10.1002/bte2.20240088 · cites 21 · refs 63 · 106 days
* **Problem:** understanding and predicting dendrite growth, which causes short circuits, performance degradation, "reduced cycle life" and abnormal exothermic events.
* **Gap claimed:** stated in general terms only: understanding dendrite growth "has become a key challenge".
* **Novelty / method:** two 2-D CNN models used "along with computational methods". CNN-1 uses standard CNN techniques. CNN-2 "integrates additional physical parameters to enhance model robustness".
* **Baselines / ablation:** CNN-2 is compared with CNN-1. Obs.: this works as an ablation of the physical-parameter inputs; no external baseline is named.
* **Quantitative results:** none. The abstract claims CNN-2 "significantly enhances prediction accuracy" with "high accuracy and sensitivity".
* **Robustness:** the stated design goal of CNN-2; no robustness test is described.
* **Not stated in abstract:** data source and type (simulated or experimental), chemistry, size; statistical validation; generalization; complexity; limitations; code.
* **Fit:** ML applied to a degradation and safety mechanism. Highly cited despite a qualitative abstract.

#### BE-07 · Thomas, Weatherspoon & Nelson 2025: "Localized EIS Data for Capacity and SOH Prediction With Neural Networks"
DOI 10.1002/bte2.20250006 · cites 13 · refs 23 · 39 days
* **Problem:** estimating capacity and SOH over the cycle life while cutting EIS acquisition time.
* **Gap claimed:** acquiring current-voltage data "directly builds up degradation within the cell". Physics-based methods "require high computational power". EIS is slow, "especially at lower frequencies".
* **Novelty / method:** feature extraction that keeps the subset of EIS frequencies "mostly correlated with degradation", followed by neural-network prediction of capacity and SOH. The authors also highlight a "single-cell model for battery test bench applications".
* **Dataset:** "a publicly available data set" (name, chemistry and size n/s). The SOH result refers to "a simulated cell".
* **Quantitative results:** SOH "as low as 0.94% MAPE using the two most correlated frequencies in the charge transfer (CT) region". EIS acquisition time reduced "by 93% for this case".
* **Ablation:** Obs.: the result rests on choosing a frequency subset (two frequencies); no formal ablation is described.
* **Computational complexity:** reported as measurement-time saving (93 %); compute cost n/s.
* **Limitations:** the authors limit the 93 % to "this case". Obs.: single-cell scope.
* **Not stated in abstract:** baselines; statistical validation; robustness; cross-dataset generalization; code.
* **Fit:** SOH estimation with a practical test-bench benefit. Fastest acceptance in Group A (39 days).

#### BE-10 · Lyu et al. 2025: "Transfer Learning-Based Data-Fusion Model Framework for State of Health Estimation of Power Battery Packs"
DOI 10.1002/bte2.70011 · cites 10 · refs 35 · 50 days
* **Problem:** SOH estimation for EV power-battery packs.
* **Gap claimed:** "the absence of a universal aging model for power batteries".
* **Novelty / method:** two ageing features from constant-current charging data via incremental capacity analysis (ICA). A "flexible data-driven aging model" built from dual Gaussian process regressions with transfer learning. A particle filter adaptively fuses the ageing features and the output capacity, giving "closed-loop" SOH estimation.
* **Dataset:** "open-source battery cell data set from the University of Maryland" plus "private battery packs" (sizes n/s).
* **Experimental design:** "battery pack aging experiments validate the proposed method".
* **Baselines / ablation:** "transfer learning effectively improves estimation accuracy". Obs.: implies a with/without-TL comparison; no other baseline is named.
* **Quantitative results:** "mean root mean square error (RMSE) of 0.87" (unit n/s).
* **Generalization:** public cell data used as the source and private packs as the target. Obs.: this is the **only cross-dataset element among the nine Group A abstracts**.
* **Not stated in abstract:** statistical validation; robustness; complexity; limitations; code. Obs.: GPR and particle filters yield predictive distributions by construction, but the abstract reports only RMSE, with no intervals or coverage.
* **Fit:** BMS SOH estimation, cell-to-pack transfer.

#### BE-16 · Qays et al. 2026: "State of Charge Estimation of EV Secondary Battery Pack Using Hybrid Hedge Feedforward Feedback-Based Gated Recurrent Unit to Extend Lifespan"
DOI 10.1002/bte2.70073 · cites 8 · refs 40 · 183 days
* **Problem:** SoC estimation and charge balancing in parallel-connected cells to extend pack life.
* **Gap claimed:** "underexplored challenges associated with circulating currents" that can overheat packs, shorten their life or cause thermal runaway.
* **Novelty / method:** "hedge feedforward feedback-based gated recurrent unit with H∞ controller (HFF-GRU-H∞)". SoC balancing of three cells through a bidirectional DC/DC converter under H∞ robust control.
* **Dataset / design:** "various real-world charging and discharging profiles" (source and size n/s); "experimental results".
* **Baselines:** "nine widely-applied deep-learning algorithms" (not named in abstract) and "existing methods" for determination time.
* **Quantitative results:** SoC capacity estimation error "reduced to 0.043%". Determination time "0.477 s". Pack lifespan "extended by 27.7%".
* **Computational complexity:** 0.477 s determination time.
* **Not stated in abstract:** ablation; statistical validation; robustness tests; generalization; limitations; code. Obs.: the abstract does not say whether the 27.7 % life extension was measured or projected.
* **Fit:** BMS state estimation and balancing. Slowest acceptance in Group A (183 days).

#### BE-21 · Warren et al. 2026: "Real-Time, Interpretable Diagnostics for Solid-State Batteries via Machine Learning on In Situ Impedance Spectra"
DOI 10.1002/bte2.70122 · cites 4 · refs 10 · 76 days
* **Problem:** EIS is "difficult to interpret in real time" for solid-state cells.
* **Novelty / method:** a "lightweight, interpretable diagnostic framework". Spectra are encoded into feature vectors, and "tree-based multi-output regressors" predict SoC and cycle index.
* **Dataset:** in situ EIS of solid-state cells (own or public and size n/s).
* **Quantitative results:** "R² > 0.99" for SoC and cycle index. Retraining on "only five key features maintains sub-percent accuracy". "millisecond-scale" monitoring.
* **Ablation:** reduction to five features (Obs.: an ablation-like test).
* **Interpretability:** feature importance links mid-frequency responses to cathode degradation and low-frequency responses to anode degradation.
* **Computational complexity:** millisecond-scale inference, "suitable for embedded" BMS.
* **Not stated in abstract:** baselines; statistical validation; robustness; generalization; limitations; code. Obs.: only 10 references, so likely a short-format paper (article type is not in the metadata).
* **Fit:** ML diagnostics plus interpretability for BMS.

#### BE-22 · Khoury et al. 2025: "Development of an Intelligent Energy Management System to Improve BESS State of Health"
DOI 10.1002/bte2.20250019 · cites 3 · refs 21 · 50 days
* **Problem:** in a PV + BESS + diesel microgrid, the energy-management (EMS) strategy affects BESS SOH and RUL.
* **Novelty / method:** an intelligent EMS (iEMS) with "predictive artificial neural network (ANN) control power dispatch strategy". It uses a "6-h prediction on blackout occurrence" and non-critical load shedding.
* **Baselines:** "classical EMS".
* **Quantitative results:**
  * "MAE = 6.43%".
  * SOH preserved "to 33% (an increase of 45% compared to classical EMS)", against 20 % with classical EMS.
  * Blackout occurrence "decreased by 56% (−5203 h)" compared with 11,899 h for classical EMS.
* **Obs. (uncertain):** the abstract does not explain the basis of the percentages. They cannot be reproduced from the absolute figures it gives (for example, 5203/11,899 ≈ 44 %).
* **Not stated in abstract:** whether the data are simulated or field data; data size; ablation; statistics; robustness; generalization; complexity; limitations; code.
* **Fit:** management aimed at SOH and lifetime.

#### BE-23 · Rajabzadeh et al. 2025: "A Hybrid Exponential Smoothing and LSTM Approach With Double Lightning Search for Enhanced Prediction of Lithium-Ion Battery Remaining Useful Life"
DOI 10.1002/bte2.20250052 · cites 2 · refs 44 · 102 days
* **Problem:** RUL and end-of-life (EoL) prediction.
* **Gap claimed:** no specific gap stated.
* **Novelty / method:** a pipeline of exponential-smoothing denoising, sequence construction, double lightning search algorithm (DLSA) hyperparameter optimization and iterative LSTM modelling.
* **Dataset:** "NASA Prognostics Center of Excellence" Li-ion data (cells and size n/s).
* **Quantitative results:** "average error of under ±0.002 ampere-hours in capacity prediction".
* **Statistical validation:** "assessed using basic statistical measures" (unspecified). No seeds or confidence intervals mentioned.
* **Robustness:** accuracy is claimed "even when there is much noise", and DLSA is said to safeguard "against fluctuating degradation rates". No dedicated test is described.
* **Computational complexity:** "Systematic sampling and normalization make calculations faster"; not quantified.
* **Not stated in abstract:** baselines; ablation; generalization; limitations; code.
* **Fit:** RUL prognostics on a public benchmark.

#### BE-28 · Kee et al. 2026: "Degradation-Informed Temperature Analysis for Cycle Life Prediction of LiFePO4 Batteries" (closest neighbour to our paper)
DOI 10.1002/bte2.70124 · cites 1 · refs 36 · 105 days
* **Problem:** cycle-life prediction under fast charging.
* **Gap claimed:** conventional prognostics rely on electrochemical measurements (capacity fade, internal resistance) that "often require specialized testing protocols and limit practical applicability".
* **Novelty:** temperature as "a non-electrochemical and readily accessible signal". A hypothesis "informed by density functional theory" links the accumulation of internal resistance to heat generation and temperature behaviour.
* **Dataset:** "large open-source dataset comprising 96,700 cycles of commercial LiFePO₄/graphite cells subjected to diverse fast-charging protocols". The dataset name and number of cells are n/s. **[inference, unverified]** The description is consistent with the public MATR (Severson et al.) fast-charging LFP data that we also plan to use.
* **Method:** temperature features extracted separately from charge and discharge temperature curves; gradient boosting machine (GBM) cycle-life models; Shapley-value analysis.
* **Baselines / ablation:** charge-only vs discharge-only vs combined features. Discharge-derived features "significantly outperform" charge-derived ones, and the combination "yields the highest predictive accuracy". No external baseline (for example capacity or resistance features) is named.
* **Quantitative results:** no accuracy number in the abstract.
* **Interpretability:** SHAP shows that discharge temperature features dominate.
* **Not stated in abstract:**
  * whether prediction uses early cycles only
  * train/test protocol
  * statistical validation (Obs.: "significantly" is used without a stated test)
  * uncertainty or intervals
  * cross-dataset generalization
  * complexity, limitations, code
* **Fit:** same target (cycle life), same chemistry and probably the same public data as our paper. It must be cited and contrasted.

### Group B: Model-based estimation, control and stochastic modelling

#### BE-24 · Nohra et al. 2026: "A New Approach for Estimation of Lithium-Ion Battery State of Charge and Health Using Mixed H∞/H2 Control With Sliding Mode Observer"
DOI 10.1002/bte2.70072 · cites 2 · refs 41 · 99 days
* **Problem:** robust real-time SOC and SOH estimation under ageing, unmodelled dynamics and temperature fluctuations.
* **Novelty / method:** an H∞/H2 controller with pole placement built with LMI techniques, plus a sliding-mode estimator for SoH, described as "a novel combination". The disturbance-matrix structure is optimized, and changes in internal resistances, capacitances and actual capacity are taken into account.
* **Design / robustness:** "numerical simulations" under UDDS, US06 and HWFET schedules with varied internal properties.
* **Quantitative results:** none.
* **Not stated in abstract:** baselines; ablation; statistics; generalization; complexity; limitations; code. Obs.: the abstract says "validated under real-world circumstances", but the validation it describes is simulation only.
* **Fit:** BMS state estimation (control-theory based).

#### BE-25 · Asadi et al. 2026: "Accurate State of Charge Estimation in Lithium-Ion Batteries by Second-Order Sliding Mode Observer"
DOI 10.1002/bte2.70093 · cites 2 · refs 45 · 87 days
* **Problem / gap:** first-order sliding-mode observers "suffer from chattering and slow convergence".
* **Novelty / method:** a finite-time second-order sliding-mode observer on an equivalent-circuit model, with an analytically derived "closed-form expression for the finite convergence time".
* **Baselines:** Extended Kalman Filter and traditional SMO.
* **Results:** "higher estimation accuracy and faster convergence while maintaining lower computational complexity". No numbers.
* **Design:** "Theoretical analysis and simulation".
* **Robustness:** claimed against modelling uncertainties and measurement noise.
* **Not stated in abstract:** experimental data; ablation; statistics; generalization; limitations; code.
* **Fit:** BMS SoC estimation with an analytical guarantee (convergence time).

#### BE-26 · Gebennini et al. 2026: "Capturing State-of-Charge-Dependent Efficiency in Battery Energy Storage Systems: A Bernoulli Model Approach"
DOI 10.1002/bte2.70080 · cites 2 · refs 44 · 55 days
* **Problem / gap:** conventional stochastic BESS models "assume constant charging and discharging efficiencies".
* **Novelty / method:** a discrete-time, discrete-state Markov chain with SOC-dependent transition probabilities and charge-acceptance limits, and a "closed-form analytical solution for the steady-state probability distribution".
* **Design:** "illustrative numerical study".
* **Baselines:** ideal and constant-efficiency models.
* **Results:** qualitative. When charge acceptance is limited at high SOC ("e.g., for State Of Health preservation"), probability mass concentrates in an intermediate range.
* **Computational complexity:** "computationally efficient".
* **Not stated in abstract:** empirical data; numbers; statistics; generalization; limitations; code.
* **Fit:** analytical probabilistic modelling. Obs.: it shows that the journal accepts mathematically oriented contributions.

#### BE-19 · Iqbal et al. 2025: "A Robust Multi-Agent Based Hierarchical Control Strategy for SoC Balancing and Power Management in DC Shipboard Microgrids"
DOI 10.1002/bte2.70075 · cites 6 · refs 41 · 68 days
* **Problem:** current sharing, power-flow management and bus-voltage regulation in DC shipboard microgrids.
* **Novelty / method:**
  * an adaptive SoC-based current sharing (ASCS) layer;
  * an average voltage drop restoration (AVDR) layer;
  * a multi-agent consensus (MAC) algorithm.
* **Design / robustness:** "comprehensive stability analysis"; MATLAB/Simulink simulations; "Star Sim-based hardware-in-the-loop (HIL)" validation.
* **Generalization:** "scalability" is claimed.
* **Not stated in abstract:** baselines; numbers; statistics; complexity (the authors say only that communication overhead is minimized); limitations; code.
* **Fit:** SoC-based management.

### Group C: Experimental and physics-based degradation and lifetime papers

#### BE-01 · Ando et al. 2023: "Degradation mechanism of all-solid-state lithium-ion batteries with argyrodite Li7−xPS6−xClx sulfide through high-temperature cycling test"
DOI 10.1002/bte2.20220052 · cites 26 · refs 45 · 68 days
* **Problem / gap:** degradation mechanisms and analysis methods of sulfide solid-state cells are "poorly understood".
* **Method:** charge/discharge cycling at 100 °C (accelerated degradation), plus disassembly analysis before and after.
* **Data:** an argyrodite-type sulfide prototype cell (number n/s).
* **Results:** four degradation modes that "appear to occur simultaneously":
  1. solid-electrolyte oxidation at the positive electrode (recovers capacity, increases resistance);
  2. solid-electrolyte reduction at the negative electrode;
  3. lithium deposition;
  4. positive-electrode capacity loss.
* **Not stated in abstract:** replicates; numbers; statistics; generalization; code.
* **Fit:** degradation diagnostics (accelerated testing).

#### BE-04 · Rahil et al. 2022: "Investigating the possibility of using second-life batteries for grid applications"
DOI 10.1002/bte2.20210001 · cites 19 · refs 23 · 203 days
* **Problem:** whether a retired PHEV battery meets grid-service requirements.
* **Method:** a reference capacity test (SOH, SOC, durability), then duty-cycle tests for peak shaving, frequency regulation, PV smoothing and renewable-energy (RE) firming.
* **Data:** one retired PHEV pack (abstract: "a PHEV battery", "the pack").
* **Baseline:** pass criterion of 2 % untracked time.
* **Results:**
  * peak shaving: satisfied;
  * frequency regulation: partially met, untracked time 4 % (vs 2 %);
  * PV smoothing: untracked time 14 %;
  * RE firming: untracked time 11 %, and the cycle failed because SOC reached its maximum safety limit after "6 h and 23 min" of a 10 h duty cycle.
* **Not stated in abstract:** replicates; statistics; generalization; code.
* **Fit:** SOH and second-life application testing. Longest acceptance in the set (203 days).

#### BE-06 · Chen et al. 2025: "Electrochemical Modeling and Degradation Analysis of Lithium-Ion Batteries in High Temperature Environments"
DOI 10.1002/bte2.20250043 · cites 15 · refs 75 · 112 days
* **Problem:** predicting cycle life and elucidating side reactions at high temperature.
* **Novelty / method:**
  1. a "simplified electrochemical-mechanical coupling model";
  2. multiscale characterization of aged cells, identifying "five types of side reactions" (examples given: SEI growth, cracking of negative-electrode particles, electrolyte oxidation, decomposition/deposition of active materials);
  3. a life-prediction model built from these side reactions.
* **Validation:** "high temperature cycling data".
* **Findings:** electrolyte decomposition and loss of active material are the primary causes of degradation at high temperature.
* **Not stated in abstract:** chemistry; temperatures; number of cells; accuracy numbers; baselines; statistics; generalization; complexity; code.
* **Fit:** physics-based life prediction.

#### BE-08 · Yang, Wang & Xie 2025: "Influence of Overdischarge Depth on the Aging and Thermal Safety of LiNi0.5Co0.2Mn0.3O2/Graphite Cells"
DOI 10.1002/bte2.70008 · cites 11 · refs 38 · 55 days
* **Problem:** ageing and thermal safety at different overdischarge cut-off voltages.
* **Method:** electrochemical tests, quantitative degradation-mode analysis, disassembly, physicochemical characterization, DSC and thermal-runaway behaviour.
* **Results:**
  * capacity decay rate of 38.2 % at a 0.5 V cut-off;
  * conductive loss and lithium-inventory loss are the main ageing causes;
  * Cu current-collector dissolution;
  * reduced anode thermal stability;
  * earlier thermal runaway with lower onset and peak temperatures.
* **Not stated in abstract:** number of cells; replicates; statistics; code.
* **Fit:** ageing mechanism and safety diagnostics.

#### BE-15 · Wang et al. 2025: "Features of Separator Configuration in Determining the Cycle Life of Zn Metal Anode"
DOI 10.1002/bte2.20240107 · cites 8 · refs 28 · 95 days
* **Problem / gap:** how glass-fibre separator geometry affects cycle life of Zn-metal batteries; "the underlying mechanisms remain unclear".
* **Finding:** cycle life is set by a competition between internal short circuits from Zn dendrites and deteriorating charge transfer. Which mechanism dominates depends on current density and capacity.
* **Not stated in abstract:** numbers; sample sizes; statistics; code.
* **Fit:** determinants of cycle life (non-Li-ion).

### Group D: Reviews and perspectives

#### BE-11 · Ametefe et al. 2026: "Intelligent Battery Systems: System-Level Integration of Data-Driven Learning, Optimisation and Predictive Management" (perspective)
DOI 10.1002/bte2.70099 · cites 10 · refs 184 · 40 days
* **Gap claimed:** "most extant studies emphasise individual algorithms or isolated prediction tasks"; reliable deployment "receives limited attention".
* **Contribution:** a system-level view that integrates sensing, learning, optimization and management. It covers deployment constraints (sensing fidelity, data representativeness, interpretability, scalability, embedded compatibility) and draws on "Evidence from fast charging studies and grid-scale deployments".
* **Key statement for us:** it highlights "early and diverse sensing, physics-informed learning, uncertainty-aware decision processes and deployment-oriented model design".
* **Not applicable / not stated:** data, baselines, statistics, code (review).

#### BE-18 · Helaley, Khan & Sajid 2025: "Integrating Chemical Engineering Principles Into Battery Management Systems for Enhanced Safety and Reliability in Energy Storage" (review)
DOI 10.1002/bte2.70067 · cites 6 · refs 39 · 65 days
* **Scope:** thermal-runaway modes; passive thermal management with phase-change materials vs active air cooling; BMS architectures; SoH; sodium-ion, lead-acid and nickel chemistries.
* **Numbers reported by the review:** passive protection "can reduce propagation temperatures by more than 60°C"; smart BMS algorithms "improve the State of Health (SoH) by up to 20%" compared with conventional protocols.
* **Not applicable / not stated:** primary data, statistics, code.

#### BE-20 · Sulaima et al. 2026: "Physics-Informed Artificial Intelligence for Battery Degradation, Aging, and Lifetime Prediction" (review)
DOI 10.1002/bte2.70136 · cites 6 · refs 145 · 125 days
* **Gap claimed:** AI approaches perform well in the short term, but "many remain data-driven and show limited robustness under long-term cycling, operating-regime shifts, and extrapolation beyond training data". Physics models face "computational cost, parameter uncertainty, and scalability". Earlier reviews treat these topics separately.
* **Contribution:** a "unified multiscale synthesis linking degradation physics, PIAI model construction, uncertainty quantification, structured validation, and BMS/digital-twin deployment". It also proposes a "five-layer framework for trustworthy battery lifetime prediction".
* **Relevance to us:** the strongest statement in this journal that lifetime prediction needs uncertainty quantification and structured validation. Directly citable as motivation.

#### BE-27 · Maddipatla, Kwon, Jeevarajan & Pecht 2026: "Prognostic Approaches for Early Detection of Thermal Runaway in Lithium-Ion Batteries" (review)
DOI 10.1002/bte2.70149 · cites 2 · refs 134 · 197 days
* **Scope:** early-detection indicators (voltage, current, impedance, SOC, temperature, force, strain, pressure, acoustic, gas). Methods are compared on trigger type, advance warning, "detection accuracy (minimizing false positives and false negatives)", compatibility, implementation complexity and practicality. Also covers intervention strategies.
* **Relevance to us [our interpretation]:** it evaluates methods by error-type trade-offs and lead time, which is analogous to our trade-off between miscoverage and test time saved.

---

## 4. Evidence matrix for the 18 original-research papers (abstract level)

Legend:
* **Y** = stated in the abstract
* **c** = claimed qualitatively, with no number or test described
* **–** = not stated in the abstract (it may still be in the full text)

| ID | Public data | Data size stated | External baseline named | Accuracy/effect number | Ablation-like comparison | Statistical validation (seeds/CI/tests) | Robustness test | Cross-dataset | Efficiency claim | Interpretability | Uncertainty / intervals | Code |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BE-02 | – | – | – | – | – | – | – | – | c | – | – | – |
| BE-03 | – | – | – | – | Y (CNN-1 vs CNN-2) | – | c | – | – | c | – | – |
| BE-07 | Y | – | – | Y | c (frequency subset) | – | – | – | Y (−93 % time) | – | – | – |
| BE-10 | Y (+ private) | – | – | Y | Y (± TL) | – | – | Y (cell → pack) | c | – | – | – |
| BE-16 | – | – | Y (9 DL models, unnamed) | Y | – | – | – | – | Y (0.477 s) | – | – | – |
| BE-21 | – | – | – | Y | Y (5 features) | – | – | – | Y (ms-scale) | Y | – | – |
| BE-22 | – | – | Y (classical EMS) | Y | – | – | – | – | – | – | – | – |
| BE-23 | Y (NASA) | – | – | Y | – | c ("basic statistical measures") | c | – | c | – | – | – |
| BE-28 | Y | Y (96,700 cycles) | – | – | Y (charge/discharge/combined) | – | – | – | – | Y (SHAP) | – | – |
| BE-24 | – (simulation) | – | – | – | – | – | Y (3 drive cycles, parameter variation) | – | – | – | – | – |
| BE-25 | – (simulation) | – | Y (EKF, SMO) | – | – | – | c | – | c | – | – | – |
| BE-26 | – (numerical) | – | Y (ideal / constant-efficiency) | – | – | – | – | – | c | – | – | – |
| BE-19 | – (Simulink/HIL) | – | – | – | – | – | Y (stability analysis) | – | – | – | – | – |
| BE-01 | – | – | – | – | – | – | – | – | – | – | – | – |
| BE-04 | – | Y (one pack) | Y (2 % criterion) | Y | – | – | – | – | – | – | – | – |
| BE-06 | – | – | – | – | – | – | – | – | – | – | – | – |
| BE-08 | – | – | – | Y | – | – | – | – | – | – | – | – |
| BE-15 | – | – | – | – | – | – | – | – | – | – | – | – |

Keyword checks across **all 31** abstracts, by script:
* **Zero hits:** "conformal", "censor", "truncat", "coverage", "quantile", "confidence", "Bayes", "seed", "p-value", "generaliz/generalis", "GitHub". "code" matches only the word "encodes" in BE-28, so no abstract mentions code availability.
* **"cross-validation"/"fold":** only BE-14 (excluded).
* **"uncertain":** only BE-11 and BE-20 (reviews) and BE-25 ("modeling uncertainties").
* **Early-cycle prediction:** no abstract mentions predicting from the first N cycles.

---

## 5. Synthesis

### 5.1 Level of novelty published
* In Group A the typical novelty is **a new or physically motivated input signal paired with a standard or hybrid ML model**:
  * voltage deviation + CNN-LSTM (BE-02);
  * selected EIS frequencies + NN (BE-07);
  * ICA features + GPR/TL/PF (BE-10);
  * temperature features + GBM (BE-28);
  * EIS features + tree models (BE-21).
* Another common pattern is **a new combination of known components**: ES + LSTM + metaheuristic tuning (BE-23); GRU + H∞ (BE-16); H∞/H2 + SMO (BE-24, "a novel combination").
* Purely methodological contributions with formal guarantees are rare. The only analytical results are BE-25 (closed-form convergence time) and BE-26 (closed-form steady-state distribution). None concerns prediction intervals or statistical validity.
* **No abstract among the 31 addresses distribution-free or conformal prediction, censored or truncated data, coverage guarantees, or early-cycle lifetime bounds.** Reviews BE-20 and BE-11 explicitly name uncertainty quantification, structured validation and uncertainty-aware decisions as open needs.

### 5.2 How sophisticated the methods are
Mostly mid-level, off-the-shelf ML: CNN, LSTM, GRU, GPR, GBM, tree ensembles, ANN. The extra sophistication comes from hybridization (filters, controllers, transfer learning, metaheuristics) rather than new learning theory. Interpretability (SHAP, feature importance) appears in 2026 papers (BE-21, BE-28). Probabilistic models appear (GPR + particle filter in BE-10; Markov chain in BE-26), but no abstract reports calibrated uncertainty.

### 5.3 How deep the experiments go (as visible in abstracts)
* **Single dataset** in every Group A paper except BE-10 (public cells plus private packs).
* **Public data** is explicitly stated in 4 of 9 Group A papers: BE-07, BE-10, BE-23 (NASA PCoE), BE-28.
* **Dataset size** is stated in 1 of 9 (BE-28: 96,700 cycles). **Number of cells** is stated in 0 of 9.
* Group B validation is **simulation only** or **simulation + HIL**.
* Group C is physical testing, but the number of cells or replicates is not stated in any abstract (BE-04 implies a single pack).

### 5.4 Common baselines
External baselines are named in only 2 of 9 Group A abstracts: BE-16 ("nine widely-applied deep-learning algorithms") and BE-22 ("classical EMS"). In Group B they are EKF and first-order SMO (BE-25) and idealized models (BE-26). Internal or ablation-type comparisons are more common: CNN-1 vs CNN-2 (BE-03), with/without TL (BE-10), 5-feature retraining (BE-21), charge vs discharge features (BE-28).

### 5.5 How results are presented
* One or two **headline point-accuracy numbers** are the norm in 6 of 9 Group A abstracts: MAPE 0.94 % (BE-07), RMSE 0.87 (BE-10), 0.043 % (BE-16), R² > 0.99 (BE-21), MAE 6.43 % (BE-22), < ±0.002 Ah (BE-23).
* These are often paired with a **practical-benefit number**: −93 % EIS acquisition time (BE-07), 0.477 s (BE-16), +27.7 % pack life (BE-16), −56 % blackouts (BE-22).
* Three Group A abstracts give no numbers at all (BE-02, BE-03, BE-28).
* Units or bases are sometimes missing or unclear: RMSE unit in BE-10; percentage bases in BE-22.

### 5.6 How much statistical evidence and generalization testing appear
* **Statistical evidence: essentially none at abstract level.**
  * 0 of 22 abstracts mention repeated runs or seeds, confidence intervals, significance tests or cross-validation.
  * "Significantly" is used without a stated test (BE-02, BE-03, BE-24, BE-25, BE-28).
* **Generalization:** one cross-dataset transfer (BE-10, cell to pack), no cross-chemistry test, and no out-of-distribution evaluation stated.
* **Reproducibility:** no abstract mentions code or data-processing availability.
* Caveat: full texts may contain more. They could not be checked (HTTP 403).

### 5.7 What distinguishes the most-cited data-driven papers
The most cited are BE-02 (25), BE-03 (21), BE-07 (13), BE-10 (10) and BE-16 (8). What they share in their abstracts:
1. **A physically motivated representation as the selling point:** voltage deviation "rooted in the electrochemical reactions"; physical parameters added to the CNN; EIS frequencies in the charge-transfer region; ICA ageing features.
2. **A named hybrid architecture:** CNN-LSTM, CNN-1/CNN-2, dual GPR + TL + PF, HFF-GRU-H∞.
3. **A practical-efficiency hook:** reduced computational complexity, 93 % less EIS time, 0.477 s.
4. **Earlier publication** (2024 to early 2025), which gives more time to collect citations. This is a confound, and the counts are small.

They are **not** distinguished by statistical rigour, uncertainty quantification, code release or cross-dataset testing; none of these appears in their abstracts.

For context, the journal's most-cited items among the 31 are a materials review with an ML component (BE-00, 36 cites, excluded) and an experimental solid-state degradation study (BE-01, 26). Obs.: the readership is strongly materials- and electrochemistry-oriented.

### 5.8 Received → accepted (days, from Crossref)

| Set | n | Median | IQR* | Mean | Range | ≤ 100 days |
|---|---|---|---|---|---|---|
| All 31 keyword-matched | 31 | 87 | 50–106 | 87.6 | 15–203 | 20 |
| Selected 22 | 22 | 91 | 55–107.5 | 94.5 | 39–203 | 14 |
| Group A data-driven | 9 | **100** | 50–105.5 | 90.1 | 39–183 | 5 |
| Groups B + C (other original research) | 9 | 87 | 61.5–105.5 | 93.6 | 55–203 | 7 |
| Group D reviews | 4 | 95 | — | 106.8 | 40–197 | 2 |

\*Python `statistics.quantiles`, exclusive method.

Group A individually: BE-07 39, BE-10 50, BE-22 50, BE-21 76, BE-02 100, BE-23 102, BE-28 105, BE-03 106, BE-16 183. For comparison, the whole-journal 2025 median was 85 days (n = 93), according to `journal_verification.md`.

---

## 6. Implications for our paper: what we must exceed

**Positioning.** Within the 31 abstracts our contribution would be the **only** one offering distribution-free validity, censoring-aware calibration and guarantees under sequential early termination. BE-20 ("limited robustness ... extrapolation beyond training data"; uncertainty quantification; "structured validation") and BE-11 ("early ... sensing", "uncertainty-aware decision processes") give in-journal motivation to cite. **BE-28 is the closest neighbour**: LFP cycle life, open 96,700-cycle fast-charging data, GBM + SHAP, point prediction, no uncertainty stated. We should contrast a *certified lower bound* with *point accuracy* on what is probably the same data [inference, unverified]. If feasible, we can also use BE-28-style temperature features as an extra input to the predictor.

| Dimension | Bar visible in Battery Energy abstracts | What our paper should show (recommendation) |
|---|---|---|
| Novelty | New feature or hybrid ML combination; no uncertainty quantification | Formal finite-sample lower-bound guarantee under right-censoring and sequential early termination, with the theorem and assumptions stated plainly |
| Data | Usually one dataset; size rarely stated; 4/9 public | MATR + CLO + HUST, with cells, cycles, protocols and censoring fractions stated **in the abstract** |
| Baselines | 2/9 name an external baseline | At least 4 families: (i) point predictor + naive residual interval; (ii) quantile regression / GBM-quantile; (iii) GPR or Bayesian intervals; (iv) survival models for censored data (Kaplan–Meier / Cox / Weibull-AFT); (v) naive split conformal that drops censored cells or treats censoring times as failures (expected to over- or under-cover). Also report point accuracy of the underlying early-cycle predictor so readers can relate it to BE-28-type papers |
| Metrics | Single point-error metric (RMSE / MAPE / MAE / R²) | Empirical coverage vs nominal (marginal, and per dataset or protocol group); bound tightness (e.g. ratio of bound to true life, fraction of life certified); test-hours saved by early termination; plus RMSE/MAPE of the point model |
| Statistical evidence | None visible | Hundreds of random calibration/test splits; coverage reported with binomial or bootstrap CIs; full distribution of coverage across splits; seeds fixed and reported |
| Ablation | 4/9 do an internal comparison | Censoring rate, termination schedule and stopping rule, early-cycle window (number of cycles), calibration-set size, α, choice of score function |
| Generalization | 1/9 cross-dataset; 0 cross-chemistry | Train MATR → test CLO and HUST (cross-protocol and cross-lab). Say explicitly that all data are LFP, so **no cross-chemistry claim**; list it as a limitation |
| Efficiency | 6/9 make efficiency claims (3 quantified: BE-07, BE-16, BE-21) | Wall-clock cost of calibration (negligible vs training); headline "test time saved" number (this journal values practical savings, e.g. BE-07's −93 %) |
| Interpretability | 2/9 (2026 papers) | Optional: feature importance of early-cycle features, linked to degradation physics (the journal rewards physically motivated features, as in BE-02 and BE-07) |
| Reproducibility | 0/31 mention code | Public code, split seeds and preprocessing scripts. Easy to do and a clear point of difference |
| Abstract style | Concrete headline numbers plus a practical benefit | 2–3 numbers in the abstract, e.g. coverage at the nominal level, % test time saved, median certified fraction of cycle life |

**Risks and how to handle them**
* *Audience fit.* The readership is materials- and electrochemistry-heavy. Explain conformal calibration and censoring intuitively, using a figure of the test campaign and the bound. Frame the payoff as engineering value: shorter qualification and test campaigns, warranty and second-life screening (cf. BE-04), BMS reliability.
* *"Why not just better point accuracy?"* Show that strong point predictors with naive intervals miss nominal coverage, especially under censoring, while our bounds hold it.
* *Evidence asymmetry.* Our statistical evidence (repeated splits, CIs, cross-dataset) would clearly exceed everything visible in these abstracts. But the full texts could not be checked. **Before submission, obtain via institutional access the full texts of BE-28, BE-02, BE-07, BE-10 and BE-23** to confirm their validation depth and the dataset BE-28 used.
* *Timeline.* Group A median of 100 days from received to accepted (range 39–183). Plan for about 3–4 months; one in nine Group A papers took about 6 months.
