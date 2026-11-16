# Supporting Information

**Stopping Cycle-Life Tests Early With Guaranteed Error Rates: Distribution-Free Sequential Screening of Lithium-Ion Cells From Truncated Test Campaigns**

## S1 Experiments, splits and seeds

Table S1 lists every experiment. Split seeds are `seed_base + offset + i` with `seed_base = 20261115` and experiment offsets fixed in `code/experiments/suite.py`; they were fixed before any experiment was run. E9 and E10 were added after the design freeze to answer questions about protocol novelty and training-conditional validity; they are reported as additional analyses.

| ID | Purpose | Base model(s) | Splits per configuration | Output file |
|---|---|---|---|---|
| E1 | Main comparison of screening rules | Elastic net | 1,000 per dataset | results/raw/E1_*_splits.csv |
| E2 | Base predictors | Logistic, GBR, RF, GP, CNN | 1,000 (logistic), 200 (GBR, RF, GP), 30 (CNN) | results/raw/E2_models_splits.csv |
| E3 | Checkpoint-grid ablation | Elastic net | 200 | results/raw/E3_ablation_grid_splits.csv |
| E4 | Calibration/training size, feature noise | Elastic net | 200 | results/raw/E4_robustness_splits.csv |
| E5 | Batch and laboratory shift | Elastic net | 200 | results/raw/E5_shift_splits.csv |
| E6 | Run time and memory | all | 5 repetitions | results/raw/E6_compute.csv |
| E7 | Sensitivity to alpha, beta and L* | Elastic net | 200 | results/raw/E7_sensitivity_splits.csv |
| E8 | Error analysis | Elastic net (from E1) | — | results/E8_percell_*.csv |
| E9 | Protocol-disjoint splits (MATR/CLO) | Elastic net | 200 | results/raw/E9_protocol_grouped_splits.csv |
| E10 | Training-conditional (PAC) calibration | Elastic net | 200 | results/raw/E10_pac_splits.csv |

## S2 Data cleaning and labels

MATR/CLO: batch files `MATR_batch_20170512.mat` (b1), `20170630` (b2), `20180412` (b3) [1] and `20190124` (b4, CLO) [2]. Removed: b1 cells 8, 10, 12, 13, 22 (final discharge capacity 0.91–0.97 Ah, i.e. end of life never reached); b3 cells 2, 23, 32, 37, 42, 43 (noisy or incomplete channels; two have no cycle-life label). Merged: b1 cells 0–4 with their continuation records b2 cells 7, 8, 9, 15, 16 (the last capacity of each b1 record matches the first capacity of the continuation within 0.012 Ah, and the protocols coincide). Result: 124 MATR + 45 CLO = 169 cells; this reproduces the cell counts of the original studies. Placeholder cycles with empty $Q(V)$ arrays were treated as missing. CLO cells have no internal-resistance records, so resistance features were not used. Labels are the providers' cycle-life values.

HUST [3]: 77 pickled records (allow-listed unpickling of numpy/pandas objects only); each record stops when the discharge capacity reaches 0.88 Ah; cycle life = number of recorded cycles; discharge capacity per cycle from the provided `dq` field, which agrees with the integral of the measured current (correlation > 0.9999 on the cell checked).

## S3 Feature definitions

See Section 3.2 of the main text. All features at checkpoint $k$ use cycles $\le k$ only; this is enforced by a unit test (`code/tests/test_features.py`) that corrupts all data after cycle $k$ and checks that the features do not change.

## S4 Extended results

| dataset | method | fpr mean | fpr ci hi | frr mean | frr ci hi | accuracy mean | early rate mean | time saving mean | mean time mean | n splits |
|---|---|---|---|---|---|---|---|---|---|---|
| HUST | Bonferroni sequential conformal | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1.74e+03 | 1000 |
| HUST | Parametric/Bayesian threshold | 0.0815 | 0.087 | 0.136 | 0.143 | 0.893 | 0.79 | 0.69 | 540 | 1000 |
| HUST | Conformal lifetime interval (full-lifetime calibration) | 0.00731 | 0.00901 | 0.0108 | 0.0128 | 0.991 | 0.278 | 0.195 | 1.4e+03 | 1000 |
| HUST | Naive sequential conformal | 0.286 | 0.295 | 0.214 | 0.223 | 0.75 | 0.975 | 0.932 | 119 | 1000 |
| HUST | Point prediction at cycle 100 | 0.237 | 0.246 | 0.367 | 0.377 | 0.701 | 1 | 0.942 | 100 | 1000 |
| HUST | Proposed (trajectory-calibrated) | 0.0682 | 0.074 | 0.0736 | 0.0803 | 0.929 | 0.605 | 0.507 | 857 | 1000 |
| HUST | Single checkpoint (cycle 100) conformal | 0.0708 | 0.0772 | 0.0791 | 0.0859 | 0.925 | 0.415 | 0.383 | 1.07e+03 | 1000 |
| HUST | Proposed without score normalisation | 0.0672 | 0.0728 | 0.0744 | 0.0809 | 0.929 | 0.534 | 0.476 | 910 | 1000 |
| MATR+CLO | Bonferroni sequential conformal | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 653 | 1000 |
| MATR+CLO | Parametric/Bayesian threshold | 0.0458 | 0.0485 | 0.0425 | 0.0454 | 0.956 | 0.867 | 0.775 | 147 | 1000 |
| MATR+CLO | Conformal lifetime interval (full-lifetime calibration) | 0.0166 | 0.0183 | 0.00975 | 0.0113 | 0.987 | 0.664 | 0.544 | 298 | 1000 |
| MATR+CLO | Naive sequential conformal | 0.145 | 0.151 | 0.158 | 0.164 | 0.85 | 0.998 | 0.954 | 29.9 | 1000 |
| MATR+CLO | Point prediction at cycle 100 | 0.0792 | 0.0825 | 0.0726 | 0.0758 | 0.924 | 1 | 0.847 | 100 | 1000 |
| MATR+CLO | Proposed (trajectory-calibrated) | 0.0676 | 0.0728 | 0.0803 | 0.0851 | 0.927 | 0.867 | 0.783 | 142 | 1000 |
| MATR+CLO | Single checkpoint (cycle 100) conformal | 0.0819 | 0.0872 | 0.0604 | 0.0644 | 0.93 | 0.948 | 0.796 | 133 | 1000 |
| MATR+CLO | Proposed without score normalisation | 0.0681 | 0.0731 | 0.0818 | 0.0866 | 0.925 | 0.752 | 0.689 | 203 | 1000 |

: **Table S1.** Main results for all screening rules (E1, elastic net). Mean over splits of the false-pass rate (FPR, bad cells), false-reject rate (FRR, good cells) with upper 95% confidence limits, accuracy, share decided by the model, cycling time saved and mean cycles to decision.


| dataset | comparator | n cells | mean time ref | mean time comp | saving diff | saving diff ci lo | saving diff ci hi | wilcoxon p | p holm | rank biserial |
|---|---|---|---|---|---|---|---|---|---|---|
| MATR+CLO | Bonferroni sequential conformal | 169 | 142 | 653 | 0.783 | 0.756 | 0.81 | 1.75e-29 | 1.22e-28 | -1 |
| MATR+CLO | Parametric/Bayesian threshold | 169 | 142 | 147 | 0.00787 | -0.0144 | 0.0317 | 0.000516 | 0.00155 | 0.308 |
| MATR+CLO | Conformal lifetime interval (full-lifetime calibration) | 169 | 142 | 298 | 0.24 | 0.203 | 0.277 | 2.59e-25 | 1.04e-24 | -0.922 |
| MATR+CLO | Naive sequential conformal | 169 | 142 | 29.9 | -0.171 | -0.197 | -0.146 | 1.75e-29 | 1.22e-28 | 1 |
| MATR+CLO | Point prediction at cycle 100 | 169 | 142 | 100 | -0.0639 | -0.0932 | -0.0353 | 0.0818 | 0.164 | 0.154 |
| MATR+CLO | Single checkpoint (cycle 100) conformal | 169 | 142 | 133 | -0.013 | -0.0341 | 0.00694 | 0.361 | 0.361 | -0.081 |
| MATR+CLO | Proposed without score normalisation | 169 | 142 | 204 | 0.095 | 0.0804 | 0.11 | 1.31e-25 | 6.54e-25 | -0.931 |
| HUST | Bonferroni sequential conformal | 77 | 854 | 1.74e+03 | 0.509 | 0.458 | 0.56 | 2.46e-14 | 1.72e-13 | -1 |
| HUST | Parametric/Bayesian threshold | 77 | 854 | 536 | -0.183 | -0.202 | -0.164 | 2.46e-14 | 1.72e-13 | 1 |
| HUST | Conformal lifetime interval (full-lifetime calibration) | 77 | 854 | 1.4e+03 | 0.312 | 0.288 | 0.336 | 2.46e-14 | 1.72e-13 | -1 |
| HUST | Naive sequential conformal | 77 | 854 | 118 | -0.423 | -0.469 | -0.377 | 2.46e-14 | 1.72e-13 | 1 |
| HUST | Point prediction at cycle 100 | 77 | 854 | 100 | -0.433 | -0.486 | -0.38 | 2.46e-14 | 1.72e-13 | 1 |
| HUST | Single checkpoint (cycle 100) conformal | 77 | 854 | 1.07e+03 | 0.124 | 0.0918 | 0.157 | 6.2e-09 | 1.24e-08 | -0.762 |
| HUST | Proposed without score normalisation | 77 | 854 | 906 | 0.03 | 0.0147 | 0.0451 | 0.000992 | 0.000992 | -0.432 |

: **Table S2.** Cell-level paired comparison of time to decision between the proposed rule and each comparator (E1). Positive saving differences favour the proposed rule. Wilcoxon signed-rank p-values, Holm-adjusted p-values and matched-pairs rank-biserial correlations.


**[DRAFT: table tables/T4_base_models.csv not yet generated]**

: **Table S3.** Validity and efficiency with different base predictors (E2 and the elastic net of E1).


**[DRAFT: table tables/T5_campaign_cost.csv not yet generated]**

: **Table S4.** Cell-cycles and wall-clock cycles needed for the training and calibration campaigns (mean per split).


**[DRAFT: table tables/T6_ablation_grid.csv not yet generated]**

: **Table S5.** Checkpoint-grid ablation (E3).


**[DRAFT: table tables/T7_robustness.csv not yet generated]**

: **Table S6.** Robustness to calibration-set size, training-set size and feature noise (E4).


**[DRAFT: table tables/T8_shift.csv not yet generated]**

: **Table S7.** Batch shift and laboratory shift (E5).


**[DRAFT: table tables/T9_compute.csv not yet generated]**

: **Table S8.** Computational cost (E6).


**[DRAFT: table tables/T10_sensitivity.csv not yet generated]**

: **Table S9.** Sensitivity to the error levels and to the specification L* (E7).


**[DRAFT: table tables/T11_protocol_grouped.csv not yet generated]**

: **Table S10.** Protocol-disjoint splits on MATR/CLO (E9).


**[DRAFT: table tables/T12_pac.csv not yet generated]**

: **Table S11.** Training-conditional (PAC) calibration (E10).


| n calibration cells in class | marginal rank | P conditional error above alpha | pac rank delta 0 1 | pac rank delta 0 2 |
|---|---|---|---|---|
| 9.0 | 9.0 | 0.387 | – | – |
| 10.0 | 10.0 | 0.349 | – | – |
| 15.0 | 15.0 | 0.206 | – | – |
| 20.0 | 19.0 | 0.392 | – | 20 |
| 25.0 | 24.0 | 0.271 | 25 | 25 |
| 30.0 | 28.0 | 0.411 | 30 | 29 |
| 40.0 | 37.0 | 0.423 | 39 | 39 |
| 60.0 | 55.0 | 0.437 | 58 | 57 |
| 100.0 | 91.0 | 0.451 | 95 | 94 |

: **Table S12.** Conditional (training-conditional) error of marginally calibrated thresholds. For $n$ calibration cells of a class and $\alpha=0.10$: the rank used by the marginal rule, the probability that the conditional error probability of the resulting threshold exceeds $\alpha$ (Beta$(r,n+1-r)$ law of conformal coverage for continuous scores), and the rank required for a PAC guarantee with $\delta=0.1$ and $\delta=0.2$ (empty: impossible with $n$ cells).


| margin bin | n cells | false pass freq | false reject freq | early decision | mean cycles |
|---|---|---|---|---|---|
| (-inf, -0.2] | 20 | 0.0374 | 0 | 0.999 | 34.8 |
| (-0.2, -0.1] | 32 | 0.0112 | 0 | 0.99 | 44.9 |
| (-0.1, -0.05] | 12 | 0.0467 | 0 | 0.854 | 145 |
| (0.05, 0.1] | 28 | 0 | 0.0578 | 0.813 | 193 |
| (0.1, 0.2] | 26 | 0 | 0.0169 | 0.91 | 120 |
| (0.2, inf] | 11 | 0 | 0.0874 | 0.987 | 40.8 |
| (0.0, 0.05] | 23 | 0 | 0.169 | 0.678 | 290 |
| (-0.05, 0.0] | 17 | 0.215 | 0 | 0.693 | 261 |

: **Table S13.** Error analysis by distance of the true lifetime from the specification, MATR/CLO (proposed rule, E1).


| margin bin | n cells | false pass freq | false reject freq | early decision | mean cycles |
|---|---|---|---|---|---|
| (-inf, -0.2] | 2 | 0.103 | 0 | 0.965 | 210 |
| (-0.2, -0.1] | 14 | 0.00668 | 0 | 0.836 | 491 |
| (-0.1, -0.05] | 9 | 0.0757 | 0 | 0.451 | 1.07e+03 |
| (0.05, 0.1] | 13 | 0 | 0.045 | 0.634 | 875 |
| (0.1, 0.2] | 10 | 0 | 0.0434 | 0.814 | 495 |
| (-0.05, 0.0] | 15 | 0.117 | 0 | 0.364 | 1.2e+03 |
| (0.0, 0.05] | 14 | 0 | 0.124 | 0.515 | 1.03e+03 |

: **Table S14.** Error analysis by distance of the true lifetime from the specification, HUST (proposed rule, E1).


| cell id | batch | policy | T | log ratio | fp | fr | early | time | n |
|---|---|---|---|---|---|---|---|---|---|
| b1c19 | b1 | 5.4C(70%)-3C | 788 | 0.0215 | 0 | 0.826 | 0.83 | 161 | 264 |
| b4c20 | b4 | 3.6-6-5.6-4.755 | 748 | -0.00116 | 0.802 | 0 | 0.802 | 189 | 268 |
| b4c8 | b4 | 4.4-5.6-5.2-4.252 | 678 | -0.0438 | 0.703 | 0 | 0.715 | 221 | 256 |
| b3c17 | b3 | 5.3C(54%)-4C-newstructure | 1.32e+03 | 0.244 | 0 | 0.699 | 0.972 | 45.9 | 246 |
| b2c1 | b2 | 2C(10%)-6C | 148 | -0.705 | 0.695 | 0 | 1 | 24 | 243 |
| b4c3 | b4 | 8-4.4-4.4-3.94 | 778 | 0.0159 | 0 | 0.626 | 0.769 | 228 | 238 |
| b1c7 | b1 | 4.8C(80%)-4.8C | 870 | 0.0645 | 0 | 0.587 | 0.917 | 104 | 254 |
| b1c34 | b1 | 7C(30%)-3.6C | 742 | -0.00466 | 0.576 | 0 | 0.621 | 332 | 224 |
| b1c33 | b1 | 6C(60%)-3C | 757 | 0.00403 | 0 | 0.539 | 0.649 | 298 | 245 |
| b1c11 | b1 | 5.4C(50%)-3C | 788 | 0.0215 | 0 | 0.494 | 0.894 | 131 | 265 |

: **Table S15.** The ten MATR/CLO cells with the highest error frequency across splits (proposed rule).


| cell id | batch | policy | T | log ratio | fp | fr | early | time | n |
|---|---|---|---|---|---|---|---|---|---|
| HUST_1-5 | HUST | 1-5 | 1.97e+03 | 0.0159 | 0 | 0.582 | 0.61 | 975 | 287 |
| HUST_9-3 | HUST | 9-3 | 1.9e+03 | 0.00114 | 0 | 0.436 | 0.689 | 693 | 289 |
| HUST_6-5 | HUST | 6-5 | 2.18e+03 | 0.0593 | 0 | 0.291 | 0.408 | 1.29e+03 | 292 |
| HUST_4-2 | HUST | 4-2 | 1.78e+03 | -0.0278 | 0.284 | 0 | 0.315 | 1.26e+03 | 317 |
| HUST_8-7 | HUST | 8-7 | 2.05e+03 | 0.0324 | 0 | 0.261 | 0.498 | 1.04e+03 | 295 |
| HUST_3-7 | HUST | 3-7 | 2.48e+03 | 0.116 | 0 | 0.252 | 0.51 | 1.15e+03 | 298 |
| HUST_10-2 | HUST | 10-2 | 1.7e+03 | -0.0491 | 0.246 | 0 | 0.448 | 1.02e+03 | 281 |
| HUST_1-7 | HUST | 1-7 | 1.68e+03 | -0.054 | 0.242 | 0 | 0.487 | 1.03e+03 | 318 |
| HUST_1-6 | HUST | 1-6 | 1.14e+03 | -0.221 | 0.207 | 0 | 0.969 | 173 | 290 |
| HUST_6-3 | HUST | 6-3 | 1.8e+03 | -0.0225 | 0.187 | 0 | 0.221 | 1.42e+03 | 321 |

: **Table S16.** The ten HUST cells with the highest error frequency across splits (proposed rule).


![**Figure S1.** Normalised score trajectories of eight randomly chosen test cells in one split, with the calibrated pass and reject thresholds of the proposed rule.](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig6_score_trajectories.png){width=6.3in}

![**Figure S2.** Row-normalised decision matrices (true class versus decision) pooled over all splits of E1.](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig12_confusion_matrices.png){width=6.3in}

![**Figure S3.** Discrimination of the normalised score between good and bad cells at three checkpoints (pooled test cells of E1): ROC and precision–recall curves.](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig13_roc_pr.png){width=6.3in}

**[DRAFT: Figure S4. Fig14_compute not yet generated]** Run time per split and peak memory of the base predictors (E6).


## References

[1] K. A. Severson, P. M. Attia, N. Jin, N. Perkins, B. Jiang, Z. Yang, M. H. Chen, M. Aykol, P. K. Herring, D. Fraggedakis, M. Z. Bazant, S. J. Harris, W. C. Chueh, R. D. Braatz, Data-driven prediction of battery cycle life before capacity degradation, *Nature Energy* 2019, 4, 383-391. https://doi.org/10.1038/s41560-019-0356-8

[2] P. M. Attia, A. Grover, N. Jin, K. A. Severson, T. M. Markov, Y. H. Liao, M. H. Chen, B. Cheong, N. Perkins, Z. Yang, P. K. Herring, M. Aykol, S. J. Harris, R. D. Braatz, S. Ermon, W. C. Chueh, Closed-loop optimization of fast-charging protocols for batteries with machine learning, *Nature* 2020, 578, 397-402. https://doi.org/10.1038/s41586-020-1994-5

[3] G. Ma, S. Xu, B. Jiang, C. Cheng, X. Yang, Y. Shen, T. Yang, Y. Huang, H. Ding, Y. Yuan, Real-time personalized health status prediction of lithium-ion batteries using deep transfer learning, *Energy &amp; Environmental Science* 2022, 15, 4083-4094. https://doi.org/10.1039/d2ee01676a