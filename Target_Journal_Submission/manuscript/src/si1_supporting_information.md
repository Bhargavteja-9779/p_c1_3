# Supporting Information

**Stopping Cycle-Life Tests Early With Distribution-Free Error Control: Sequential Screening of Lithium-Ion Cells Calibrated on Truncated Test Campaigns**

## S1 Experiments, splits and seeds

Table S1 lists every experiment. Split seeds are `seed_base + offset + i` with `seed_base = 20261115` and experiment offsets fixed in `code/experiments/suite.py`; they were fixed before any experiment was run. E9 and E10 were added after the design freeze to answer questions about protocol novelty and training-conditional validity; E11 (physical interpretation) and E12 (grid selection on training cells, motivated by the E3 result) were added after the main results. All four are reported as additional analyses.

| ID | Purpose | Base model(s) | Splits per configuration | Output file |
|---|---|---|---|---|
| E1 | Main comparison of screening rules | Elastic net | {{CFG.n_main}} per dataset | results/raw/E1_*_splits.csv |
| E2 | Base predictors | Logistic, GBR, RF, GP, CNN | {{CFG.n_logit}} (logistic), {{CFG.n_gbr}} (GBR, RF, GP), {{CFG.n_cnn}} (CNN) | results/raw/E2_models_splits.csv |
| E3 | Checkpoint-grid ablation | Elastic net | {{CFG.n_secondary}} | results/raw/E3_ablation_grid_splits.csv |
| E4 | Calibration/training size, feature noise | Elastic net | {{CFG.n_secondary}} | results/raw/E4_robustness_splits.csv |
| E5 | Batch and laboratory shift | Elastic net | {{CFG.n_secondary}} | results/raw/E5_shift_splits.csv |
| E6 | Run time and memory | all | 5 repetitions | results/raw/E6_compute.csv |
| E7 | Sensitivity to alpha, beta and L* | Elastic net | {{CFG.n_secondary}} | results/raw/E7_sensitivity_splits.csv |
| E8 | Error analysis | Elastic net (from E1) | — | results/E8_percell_*.csv |
| E9 | Protocol-disjoint splits (MATR/CLO) | Elastic net | {{CFG.n_secondary}} | results/raw/E9_protocol_grouped_splits.csv |
| E10 | Training-conditional (PAC) calibration | Elastic net | {{CFG.n_secondary}} | results/raw/E10_pac_splits.csv |
| E11 | Physical interpretation: feature–lifetime correlations and elastic-net coefficients (descriptive) | Elastic net | {{CFG.n_secondary}} training sets (E1 seeds) | results/raw/E11_*.csv |
| E12 | Checkpoint grid chosen on training cells only (added after E3) | Elastic net | {{CFG.n_secondary}} (E3 seeds) | results/raw/E12_selected_grid_splits.csv |

## S2 Data cleaning and labels

MATR/CLO: batch files `MATR_batch_20170512.mat` (b1), `20170630` (b2), `20180412` (b3) [@severson2019] and `20190124` (b4, CLO) [@attia2020]. Removed: b1 cells 8, 10, 12, 13, 22 (final discharge capacity 0.91–0.97 Ah, i.e. end of life never reached); b3 cells 2, 23, 32, 37, 42, 43 (noisy or incomplete channels; two have no cycle-life label). Merged: b1 cells 0–4 with their continuation records b2 cells 7, 8, 9, 15, 16 (the last capacity of each b1 record matches the first capacity of the continuation within 0.012 Ah, and the protocols coincide). Result: 124 MATR + 45 CLO = 169 cells; this reproduces the cell counts of the original studies. Placeholder cycles with empty $Q(V)$ arrays were treated as missing. CLO cells have no internal-resistance records, so resistance features were not used. Labels are the providers' cycle-life values.

HUST [@ma2022hust]: 77 pickled records (allow-listed unpickling of numpy/pandas objects only); each record stops when the discharge capacity reaches 0.88 Ah; cycle life = number of recorded cycles; discharge capacity per cycle from the provided `dq` field, which agrees with the integral of the measured current (correlation > 0.9999 on the cell checked).

## S3 Feature definitions

See Section 2.3 of the main text. All features at checkpoint $k$ use cycles $\le k$ only; this is enforced by a unit test (`code/tests/test_features.py`) that corrupts all data after cycle $k$ and checks that the features do not change.

## S4 Extended results

{{STABLE:tables/T2_main_results.csv|Main results for all screening rules (E1, elastic net). Mean over splits of the false-pass rate (FPR, bad cells), false-reject rate (FRR, good cells) with upper 95% confidence limits, accuracy, share decided by the model, cycling time saved and mean cycles to decision.|}}

{{STABLE:tables/T3_paired_efficiency.csv|Cell-level paired comparison of time to decision between the proposed rule and each comparator (E1). Positive saving differences favour the proposed rule. Wilcoxon signed-rank p-values, Holm-adjusted p-values and matched-pairs rank-biserial correlations.|}}

{{STABLE:tables/T4_base_models.csv|Validity and efficiency with different base predictors (E2 and the elastic net of E1).|}}

{{STABLE:tables/T5_campaign_cost.csv|Cell-cycles and wall-clock cycles needed for the training and calibration campaigns (mean per split).|}}

{{STABLE:tables/T6_ablation_grid.csv|Checkpoint-grid ablation (E3).|}}

{{STABLE:tables/T7_robustness.csv|Robustness to calibration-set size, training-set size and feature noise (E4).|}}

{{STABLE:tables/T8_shift.csv|Batch shift and laboratory shift (E5).|}}

{{STABLE:tables/T9_compute.csv|Computational cost (E6).|}}

{{STABLE:tables/T10_sensitivity.csv|Sensitivity to the error levels and to the specification L* (E7).|}}

{{STABLE:tables/T11_protocol_grouped.csv|Protocol-disjoint splits on MATR/CLO (E9).|}}

{{STABLE:tables/T12_pac.csv|Training-conditional (PAC) calibration (E10).|}}

{{STABLE:tables/T14_selected_grid.csv|Trajectory rule with the checkpoint grid chosen on training cells only (E12).|}}

{{STABLE:tables/T15_selected_grid_choices.csv|Grids chosen by the training-only selection in E12 (share of splits).|}}

{{STABLE:tables/T13_conditional_error_analytic.csv|Conditional (training-conditional) error of marginally calibrated thresholds. For $n$ calibration cells of a class and $\alpha=0.10$: the rank used by the marginal rule, the probability that the conditional error probability of the resulting threshold exceeds $\alpha$ (Beta$(r,n+1-r)$ law of conformal coverage for continuous scores), and the rank required for a PAC guarantee with $\delta=0.1$ and $\delta=0.2$ (empty: impossible with $n$ cells).|}}

{{STABLE:tables/E8_error_by_margin_matr_clo.csv|Error analysis by distance of the true lifetime from the specification, MATR/CLO (proposed rule, E1).|}}

{{STABLE:tables/E8_error_by_margin_hust.csv|Error analysis by distance of the true lifetime from the specification, HUST (proposed rule, E1).|}}

{{STABLE:tables/E8_worst_cells_matr_clo.csv|The ten MATR/CLO cells with the highest error frequency across splits (proposed rule).|}}

{{STABLE:tables/E8_worst_cells_hust.csv|The ten HUST cells with the highest error frequency across splits (proposed rule).|}}

{{SFIG:Fig6_score_trajectories|Normalised score trajectories of eight randomly chosen test cells in one split, with the calibrated pass and reject thresholds of the proposed rule.}}

{{SFIG:Fig12_confusion_matrices|Row-normalised decision matrices (true class versus decision) pooled over all splits of E1.}}

{{SFIG:Fig13_roc_pr|Discrimination of the normalised score between good and bad cells at three checkpoints (pooled test cells of E1): ROC and precision–recall curves.}}

{{SFIG:Fig14_compute|Run time per split and peak memory of the base predictors (E6).}}

## S5 Proof of Proposition 1

Notation as in Section 2.4 of the main text.

*Proof.* If a bad cell is passed at checkpoint $m$, it was alive at $k_m$ and $S^{(m)}>\hat\lambda$, hence its trajectory statistic $P_{\text{new}}\ge S^{(m)}>\hat\lambda$. The event therefore implies $P_{\text{new}}>P_{(r_0)}$. By exchangeability the rank of $P_{\text{new}}$ among $P_1,\dots,P_{n_0},P_{\text{new}}$ is uniformly distributed (ties broken at random), so $\mathrm{P}(P_{\text{new}}>P_{(r_0)})\le (n_0+1-r_0)/(n_0+1)\le\alpha$. The argument for good cells is identical with $R$ and $\hat\mu$. Because the event "passed at some checkpoint" is contained in $\{P_{\text{new}}>\hat\lambda\}$ irrespective of when or why the procedure stops, the bound holds for any stopping time. $\square$
