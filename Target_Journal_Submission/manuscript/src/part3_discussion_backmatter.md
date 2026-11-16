## 5 Discussion

**Repeated looks must be paid for.** The most consequential result for practice is the behaviour of the naive sequential rule. Each of its per-checkpoint thresholds is a valid conformal threshold, and a practitioner who re-evaluates a prediction every few cycles and stops at the first confident call is implicitly using it. Its error rates were {{E1.mc.naive.fpr}} (false pass) and {{E1.mc.naive.frr}} (false reject) on MATR/CLO and {{E1.h.naive.fpr}} and {{E1.h.naive.frr}} on HUST at a nominal 0.10 — the optional-stopping inflation known from sequential analysis [@wald1945sprt; @howard2021cs] appears in battery screening at a practically relevant scale. Calibrating on the maximum over checkpoints removes this inflation at a cost that the data show to be modest, because scores of the same cell at successive checkpoints are strongly dependent; Bonferroni's union bound ignores that dependence and, with tens of calibration cells, never reached a decision.

**Truncated campaigns.** Because the class-conditional thresholds depend only on whether each calibration cell reached $L^\ast$, calibration cells can be retired at $\min(T,L^\ast)$. In our MATR/CLO splits this shortened the calibration campaign from {{C.mc.cal_wall_full}} to {{C.mc.cal_wall_trunc}} cycles of wall-clock time (the longest-running calibration cell), a factor of {{C.mc.cal_wall_ratio}}, and on HUST from {{C.h.cal_wall_full}} to {{C.h.cal_wall_trunc}} cycles. The lifetime-interval rule, which needs cells cycled to end of life, was also less efficient, because its marginal guarantee covers both tails of the lifetime distribution rather than the side that matters for each class. When the base predictor itself is a classifier of $Z$, training cells can be truncated as well; this kept the error guarantees but cost efficiency (Section 4.3), so the choice is between a shorter preparatory campaign and faster screening.

**One checkpoint or many?** On MATR/CLO a single, well-chosen checkpoint at cycle 100 was competitive with the sequential rule, while on HUST, whose cells live longer and whose informative checkpoints come later, the sequential rule saved clearly more cycling (Section 4.2). The sequential rule decided most clear-cut cells long before cycle 100 (median time to decision {{E1.mc.proposed.time_median}} cycles on MATR/CLO) but sent more borderline cells to full observation. The single-checkpoint rule requires choosing the checkpoint in advance; the grid ablation (Section 4.4) shows that the best fixed checkpoint differs between datasets, which a sequential rule does not need to know. In practice, a sparse grid that includes the checkpoint at which early-cycle features become informative is a reasonable default.

**Model-based uncertainty is not a substitute.** The parametric rule with Gaussian thresholds on the same normalised scores was conservative on MATR/CLO but exceeded the false-reject target on HUST, and the point-prediction rule of Severson et al. had no control at all ({{E1.h.point_k100.fpr}} and {{E1.h.point_k100.frr}} on HUST). The same model, used with different decision thresholds, can therefore be either wasteful or unsafe depending on the data set; rank-based calibration adapts to the data at hand.

**What the guarantee does and does not mean.** Proposition 1 bounds error *rates* averaged over calibration and test draws from an exchangeable population. Three consequences matter for users. (i) For a given calibration set the conditional error can exceed the target: with 20 bad calibration cells, the probability that the conditional false-pass probability exceeds 0.10 is {{PAC.p_exceed_n20}}% ({{STABREF:tables/T13_conditional_error_analytic.csv}}); a training-conditional (PAC) variant removes this at the price of needing at least 22 calibration cells per class (Section 4.5). (ii) The guarantee is class-conditional, not cell-conditional: cells whose lifetime is close to $L^\ast$ carry most of the errors (Section 4.8), as expected for any screening rule. (iii) Exchangeability is an assumption about how the calibration cells were obtained; it is plausible for cells drawn from the same production lot and tested under the same protocol family, and it failed under batch and laboratory shift in our experiments unless a few target cells were used for recalibration (Section 4.6).

**Recommended workflow.** (1) Fix $L^\ast$, $\alpha$, $\beta$ and the checkpoint grid before testing. (2) Train a base predictor on any available historical cells (full-lifetime or truncated). (3) Cycle a calibration set of at least ten bad and ten good cells (preferably more than 22 of each for training-conditional control) from the population to be screened, to $\min(T,L^\ast)$ only. (4) Screen new cells sequentially with the trajectory-calibrated thresholds. (5) Recalibrate whenever the cell population, tester or protocol family changes.

## 6 Limitations

* **One chemistry.** All {{D.n_total}} cells are LiFePO~4~/graphite 18650 cells of one type, from two laboratories. We tried to add cells of other chemistries, but the NCA/NCM data of Zhu et al. (Zenodo) and the NMC data of RWTH Aachen were not reachable from our computing environment (HTTP 403 and an interactive browser challenge), and the Sandia data available through BatteryArchive involve partial-depth cycling with many cells not reaching end of life. The guarantee itself does not depend on chemistry, but the efficiency results may.
* **Exchangeability and shift.** The guarantees require the calibration cells to be exchangeable with the cells being screened, and Section 4.6 shows that they can fail under batch or laboratory shift without recalibration.
* **Marginal, class-conditional guarantee** (see Section 5); conditional error can exceed the target for a particular calibration set unless the PAC variant is used.
* **Retrospective evaluation.** Results come from repeated random splits of finite public data sets, not from a prospective screening campaign; the splits re-use the same cells, so split-to-split variation understates the variation across independent cell populations.
* **Cost model.** Time saved is measured in cell-cycles relative to cycling each cell to $\min(T,L^\ast)$; channel scheduling, rest periods and reference performance tests are not modelled.
* **Lifetime labels** are those of the data providers (first cycle at 80% of nominal capacity); other end-of-life definitions change the class labels [@li2026endpoint].

## 7 Conclusions

Early cycle-life predictions are routinely used to make go/no-go decisions, but the error rate of those decisions is rarely controlled, and the common practice of re-checking predictions as cycling proceeds silently inflates it. We showed that calibrating pass and reject thresholds on the maximum over checkpoints of normalised model scores gives finite-sample, distribution-free bounds on the false-pass and false-reject probabilities that hold under any stopping time, and that the calibration needs cells cycled only to the specification. On {{D.n_total}} commercial LiFePO~4~/graphite cells from two laboratories, the rule met its error targets with {{CFG.alpha}} nominal levels while cutting cycling by {{E1.mc.proposed.sav}}% (MATR/CLO) and {{E1.h.proposed.sav}}% (HUST) relative to cycling every cell to the specification, whereas naive sequential use of valid per-checkpoint thresholds exceeded the targets by up to a factor of {{RATIO.naive_max}}. The procedure is a thin layer on top of any lifetime predictor, costs milliseconds to run, and is released with code that reproduces every result.

## Acknowledgments

[To be completed by the authors.] We thank the providers of the public data sets used in this study: the Toyota Research Institute, Massachusetts Institute of Technology and Stanford University teams who released the MATR/CLO data (data.matr.io), and Ma et al. (Huazhong University of Science and Technology) for the HUST data.

## Author Contributions (CRediT)

[To be completed by the authors, e.g.: Conceptualization; Methodology; Software; Validation; Formal analysis; Investigation; Data curation; Writing – original draft; Writing – review & editing; Visualization.]

## Conflict of Interest Statement

[To be confirmed by the authors.] The authors declare no conflicts of interest.

## Funding

[To be completed by the authors.]

## Data Availability Statement

The raw data analysed in this study are openly available: MATR/CLO cycling data at https://data.matr.io/1/ (Severson et al. [@severson2019]; Attia et al. [@attia2020]) and HUST data at Mendeley Data, https://doi.org/10.17632/nsc7hnsg4s.2 (Ma et al. [@ma2022hust]). The checkpoint feature tables derived from them, all split-level results, statistics, tables and figures, and the complete code that regenerates them (`python run_all.py --mode full`) are available at [repository URL / archival DOI to be inserted at submission].

## Ethics Statement

This study used only previously published battery cycling data; it involved no human participants, animals or personal data.

## Use of Generative AI

[Required by Wiley policy — to be completed accurately by the authors.] The study design, code, analyses and draft text were produced with the assistance of a generative-AI agent. [State the tool, the tasks it performed, and the human verification of code, results, citations and text.] The authors take full responsibility for the content.
