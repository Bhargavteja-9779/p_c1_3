# Supporting Information

**Stopping Cycle-Life Tests Early With Guaranteed Error Rates: Distribution-Free Sequential Screening of Lithium-Ion Cells From Truncated Test Campaigns**

## S1 Experiments, splits and seeds

Table S1 lists every experiment. Split seeds are `seed_base + offset + i` with `seed_base = 20261115` and experiment offsets fixed in `code/experiments/suite.py`; they were fixed before any experiment was run. E9 and E10 were added after the design freeze to answer questions about protocol novelty and training-conditional validity; they are reported as additional analyses.

| ID | Purpose | Base model(s) | Splits per configuration | Output file |
|---|---|---|---|---|
| E1 | Main comparison of screening rules | Elastic net | 1,000 per data set | results/raw/E1_*_splits.csv |
| E2 | Base predictors | Logistic, GBR, RF, GP, CNN | 1,000 (logistic), 200 (GBR, RF, GP), 30 (CNN) | results/raw/E2_models_splits.csv |
| E3 | Checkpoint-grid ablation | Elastic net | 200 | results/raw/E3_ablation_grid_splits.csv |
| E4 | Calibration/training size, feature noise | Elastic net | 200 | results/raw/E4_robustness_splits.csv |
| E5 | Batch and laboratory shift | Elastic net | 200 | results/raw/E5_shift_splits.csv |
| E6 | Run time and memory | All | 5 repetitions | results/raw/E6_compute.csv |
| E7 | Sensitivity to alpha, beta and L* | Elastic net | 200 | results/raw/E7_sensitivity_splits.csv |
| E8 | Error analysis | Elastic net (from E1) | - | results/E8_percell_*.csv |
| E9 | Protocol-disjoint splits (MATR/CLO) | Elastic net | 200 | results/raw/E9_protocol_grouped_splits.csv |
| E10 | Training-conditional (PAC) calibration | Elastic net | 200 | results/raw/E10_pac_splits.csv |

: **Table S1.** Experiments, base models, number of random splits per configuration and output files. Splits of different experiments use disjoint seed ranges fixed before running.


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

: **Table S2.** Main results for all screening rules (E1, elastic net). Mean over splits of the false-pass rate (FPR, bad cells), false-reject rate (FRR, good cells) with upper 95% confidence limits, accuracy, share decided by the model, cycling time saved and mean cycles to decision.


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

: **Table S3.** Cell-level paired comparison of time to decision between the proposed rule and each comparator (E1). Positive saving differences favour the proposed rule. Wilcoxon signed-rank p-values, Holm-adjusted p-values and matched-pairs rank-biserial correlations.


| dataset | model | method | fpr mean | frr mean | accuracy mean | early rate mean | time saving mean | n splits |
|---|---|---|---|---|---|---|---|---|
| HUST | cnn | gauss | 0.183 | 0.25 | 0.786 | 0.972 | 0.888 | 30 |
| HUST | cnn | naive | 0.293 | 0.253 | 0.726 | 0.988 | 0.938 | 30 |
| HUST | cnn | proposed | 0.0701 | 0.113 | 0.912 | 0.667 | 0.546 | 30 |
| HUST | cnn | single_k100 | 0.0651 | 0.128 | 0.907 | 0.381 | 0.347 | 30 |
| HUST | en | gauss | 0.0815 | 0.136 | 0.893 | 0.79 | 0.69 | 1000 |
| HUST | en | naive | 0.286 | 0.214 | 0.75 | 0.975 | 0.932 | 1000 |
| HUST | en | proposed | 0.0682 | 0.0736 | 0.929 | 0.605 | 0.507 | 1000 |
| HUST | en | single_k100 | 0.0708 | 0.0791 | 0.925 | 0.415 | 0.383 | 1000 |
| HUST | gbr | gauss | 0.0745 | 0.114 | 0.906 | 0.796 | 0.621 | 200 |
| HUST | gbr | naive | 0.273 | 0.26 | 0.733 | 0.975 | 0.92 | 200 |
| HUST | gbr | proposed | 0.0792 | 0.0696 | 0.925 | 0.709 | 0.518 | 200 |
| HUST | gbr | single_k100 | 0.0801 | 0.093 | 0.914 | 0.392 | 0.36 | 200 |
| HUST | gp | gauss | 0.274 | 0.362 | 0.684 | 0.992 | 0.935 | 200 |
| HUST | gp | naive | 0.343 | 0.31 | 0.673 | 0.984 | 0.93 | 200 |
| HUST | gp | proposed | 0.0729 | 0.0794 | 0.924 | 0.518 | 0.407 | 200 |
| HUST | gp | single_k100 | 0.0809 | 0.0772 | 0.92 | 0.34 | 0.315 | 200 |
| HUST | logit | naive | 0.304 | 0.22 | 0.737 | 0.966 | 0.923 | 1000 |
| HUST | logit | proposed | 0.0768 | 0.0763 | 0.923 | 0.465 | 0.4 | 1000 |
| HUST | logit | single_k100 | 0.0766 | 0.0748 | 0.924 | 0.353 | 0.327 | 1000 |
| HUST | rf | gauss | 0.021 | 0.0337 | 0.972 | 0.648 | 0.383 | 200 |
| HUST | rf | naive | 0.24 | 0.229 | 0.766 | 0.967 | 0.882 | 200 |
| HUST | rf | proposed | 0.0645 | 0.0715 | 0.932 | 0.751 | 0.52 | 200 |
| HUST | rf | single_k100 | 0.0873 | 0.0817 | 0.916 | 0.439 | 0.403 | 200 |
| MATR+CLO | cnn | gauss | 0.0857 | 0.0808 | 0.917 | 0.963 | 0.887 | 30 |
| MATR+CLO | cnn | naive | 0.149 | 0.165 | 0.844 | 1 | 0.958 | 30 |
| MATR+CLO | cnn | proposed | 0.0698 | 0.0872 | 0.923 | 0.887 | 0.8 | 30 |
| MATR+CLO | cnn | single_k100 | 0.0961 | 0.0556 | 0.925 | 0.894 | 0.744 | 30 |
| MATR+CLO | en | gauss | 0.0458 | 0.0425 | 0.956 | 0.867 | 0.775 | 1000 |
| MATR+CLO | en | naive | 0.145 | 0.158 | 0.85 | 0.998 | 0.954 | 1000 |
| MATR+CLO | en | proposed | 0.0676 | 0.0803 | 0.927 | 0.867 | 0.783 | 1000 |
| MATR+CLO | en | single_k100 | 0.0819 | 0.0604 | 0.93 | 0.948 | 0.796 | 1000 |
| MATR+CLO | gbr | gauss | 0.0408 | 0.0522 | 0.954 | 0.838 | 0.748 | 200 |
| MATR+CLO | gbr | naive | 0.145 | 0.156 | 0.85 | 0.998 | 0.957 | 200 |
| MATR+CLO | gbr | proposed | 0.0713 | 0.0765 | 0.926 | 0.88 | 0.803 | 200 |
| MATR+CLO | gbr | single_k100 | 0.078 | 0.0716 | 0.925 | 0.901 | 0.751 | 200 |
| MATR+CLO | gp | gauss | 0.0848 | 0.104 | 0.905 | 0.969 | 0.909 | 200 |
| MATR+CLO | gp | naive | 0.145 | 0.162 | 0.847 | 1 | 0.958 | 200 |
| MATR+CLO | gp | proposed | 0.0751 | 0.0725 | 0.926 | 0.874 | 0.798 | 200 |
| MATR+CLO | gp | single_k100 | 0.0836 | 0.0596 | 0.929 | 0.934 | 0.783 | 200 |
| MATR+CLO | logit | naive | 0.145 | 0.162 | 0.847 | 0.998 | 0.953 | 1000 |
| MATR+CLO | logit | proposed | 0.0687 | 0.0717 | 0.93 | 0.793 | 0.675 | 1000 |
| MATR+CLO | logit | single_k100 | 0.0877 | 0.0635 | 0.925 | 0.88 | 0.731 | 1000 |
| MATR+CLO | rf | gauss | 0.0208 | 0.0425 | 0.968 | 0.744 | 0.643 | 200 |
| MATR+CLO | rf | naive | 0.149 | 0.174 | 0.839 | 0.996 | 0.954 | 200 |
| MATR+CLO | rf | proposed | 0.0659 | 0.0893 | 0.922 | 0.882 | 0.805 | 200 |
| MATR+CLO | rf | single_k100 | 0.0781 | 0.0711 | 0.925 | 0.896 | 0.749 | 200 |

: **Table S4.** Validity and efficiency with different base predictors (E2 and the elastic net of E1).


| dataset | model | train cell cycles | train wallclock | cal cell cycles | cal wallclock |
|---|---|---|---|---|---|
| HUST | cnn | 5.89e+04 | 2.66e+03 | 4.02e+04 | 1.9e+03 |
| HUST | en | 5.88e+04 | 2.66e+03 | 4e+04 | 1.9e+03 |
| HUST | gbr | 5.88e+04 | 2.65e+03 | 4.01e+04 | 1.9e+03 |
| HUST | gp | 5.88e+04 | 2.65e+03 | 4.01e+04 | 1.9e+03 |
| HUST | logit | 5.39e+04 | 1.9e+03 | 4e+04 | 1.9e+03 |
| HUST | rf | 5.88e+04 | 2.65e+03 | 4.01e+04 | 1.9e+03 |
| MATR+CLO | cnn | 6.73e+04 | 2.12e+03 | 2.76e+04 | 750 |
| MATR+CLO | en | 6.73e+04 | 2.13e+03 | 2.75e+04 | 750 |
| MATR+CLO | gbr | 6.74e+04 | 2.12e+03 | 2.75e+04 | 750 |
| MATR+CLO | gp | 6.74e+04 | 2.12e+03 | 2.75e+04 | 750 |
| MATR+CLO | logit | 5.55e+04 | 750 | 2.74e+04 | 750 |
| MATR+CLO | rf | 6.74e+04 | 2.12e+03 | 2.75e+04 | 750 |
| HUST | cnn (interval, full-lifetime cal.) | – | – | 4.41e+04 | 2.65e+03 |
| HUST | en (interval, full-lifetime cal.) | – | – | 4.37e+04 | 2.63e+03 |
| HUST | gbr (interval, full-lifetime cal.) | – | – | 4.38e+04 | 2.64e+03 |
| HUST | gp (interval, full-lifetime cal.) | – | – | 4.38e+04 | 2.64e+03 |
| HUST | rf (interval, full-lifetime cal.) | – | – | 4.38e+04 | 2.64e+03 |
| MATR+CLO | cnn (interval, full-lifetime cal.) | – | – | 3.38e+04 | 2e+03 |
| MATR+CLO | en (interval, full-lifetime cal.) | – | – | 3.35e+04 | 1.96e+03 |
| MATR+CLO | gbr (interval, full-lifetime cal.) | – | – | 3.35e+04 | 1.98e+03 |
| MATR+CLO | gp (interval, full-lifetime cal.) | – | – | 3.35e+04 | 1.98e+03 |
| MATR+CLO | rf (interval, full-lifetime cal.) | – | – | 3.35e+04 | 1.98e+03 |

: **Table S5.** Cell-cycles and wall-clock cycles needed for the training and calibration campaigns (mean per split).


| dataset | grid | method | fpr mean | frr mean | early rate mean | time saving mean | n splits |
|---|---|---|---|---|---|---|---|
| HUST | all17 | naive | 0.289 | 0.212 | 0.978 | 0.936 | 200 |
| HUST | all17 | proposed | 0.0799 | 0.0751 | 0.619 | 0.526 | 200 |
| HUST | all17 | traj_unnorm | 0.0744 | 0.0767 | 0.553 | 0.497 | 200 |
| HUST | early_20to100 | naive | 0.243 | 0.191 | 0.839 | 0.819 | 200 |
| HUST | early_20to100 | proposed | 0.0687 | 0.0707 | 0.442 | 0.422 | 200 |
| HUST | early_20to100 | traj_unnorm | 0.0716 | 0.0716 | 0.447 | 0.428 | 200 |
| HUST | pair_100_1000 | naive | 0.133 | 0.116 | 0.875 | 0.596 | 200 |
| HUST | pair_100_1000 | proposed | 0.0793 | 0.075 | 0.672 | 0.47 | 200 |
| HUST | pair_100_1000 | traj_unnorm | 0.0824 | 0.0707 | 0.585 | 0.45 | 200 |
| HUST | single_100 | naive | 0.0849 | 0.0713 | 0.439 | 0.406 | 200 |
| HUST | single_100 | proposed | 0.0849 | 0.0713 | 0.439 | 0.406 | 200 |
| HUST | single_100 | traj_unnorm | 0.0849 | 0.0713 | 0.439 | 0.406 | 200 |
| HUST | single_1000 | naive | 0.0727 | 0.069 | 0.83 | 0.348 | 200 |
| HUST | single_1000 | proposed | 0.0727 | 0.069 | 0.83 | 0.348 | 200 |
| HUST | single_1000 | traj_unnorm | 0.0727 | 0.069 | 0.83 | 0.348 | 200 |
| HUST | single_300 | naive | 0.0745 | 0.0761 | 0.752 | 0.615 | 200 |
| HUST | single_300 | proposed | 0.0745 | 0.0761 | 0.752 | 0.615 | 200 |
| HUST | single_300 | traj_unnorm | 0.0745 | 0.0761 | 0.752 | 0.615 | 200 |
| HUST | sparse_100_300_600_1000 | naive | 0.175 | 0.141 | 0.949 | 0.798 | 200 |
| HUST | sparse_100_300_600_1000 | proposed | 0.0828 | 0.0774 | 0.712 | 0.568 | 200 |
| HUST | sparse_100_300_600_1000 | traj_unnorm | 0.0856 | 0.0724 | 0.653 | 0.544 | 200 |
| MATR+CLO | all16 | naive | 0.146 | 0.162 | 0.999 | 0.956 | 200 |
| MATR+CLO | all16 | proposed | 0.0676 | 0.075 | 0.875 | 0.794 | 200 |
| MATR+CLO | all16 | traj_unnorm | 0.0685 | 0.085 | 0.769 | 0.708 | 200 |
| MATR+CLO | early_20to100 | naive | 0.146 | 0.161 | 0.996 | 0.953 | 200 |
| MATR+CLO | early_20to100 | proposed | 0.066 | 0.0789 | 0.821 | 0.757 | 200 |
| MATR+CLO | early_20to100 | traj_unnorm | 0.0685 | 0.0845 | 0.748 | 0.691 | 200 |
| MATR+CLO | pair_100_300 | naive | 0.0885 | 0.0695 | 0.992 | 0.828 | 200 |
| MATR+CLO | pair_100_300 | proposed | 0.0704 | 0.072 | 0.958 | 0.788 | 200 |
| MATR+CLO | pair_100_300 | traj_unnorm | 0.0669 | 0.0717 | 0.951 | 0.788 | 200 |
| MATR+CLO | single_100 | naive | 0.0793 | 0.0598 | 0.957 | 0.806 | 200 |
| MATR+CLO | single_100 | proposed | 0.0793 | 0.0598 | 0.957 | 0.806 | 200 |
| MATR+CLO | single_100 | traj_unnorm | 0.0793 | 0.0598 | 0.957 | 0.806 | 200 |
| MATR+CLO | single_300 | naive | 0.0819 | 0.0471 | 0.957 | 0.52 | 200 |
| MATR+CLO | single_300 | proposed | 0.0865 | 0.0443 | 0.962 | 0.524 | 200 |
| MATR+CLO | single_300 | traj_unnorm | 0.0865 | 0.0443 | 0.962 | 0.524 | 200 |
| MATR+CLO | single_50 | naive | 0.0831 | 0.0762 | 0.899 | 0.819 | 200 |
| MATR+CLO | single_50 | proposed | 0.0831 | 0.0762 | 0.899 | 0.819 | 200 |
| MATR+CLO | single_50 | traj_unnorm | 0.0831 | 0.0762 | 0.899 | 0.819 | 200 |
| MATR+CLO | sparse_50_100_200_300 | naive | 0.0968 | 0.0967 | 0.995 | 0.908 | 200 |
| MATR+CLO | sparse_50_100_200_300 | proposed | 0.0706 | 0.0763 | 0.947 | 0.843 | 200 |
| MATR+CLO | sparse_50_100_200_300 | traj_unnorm | 0.0689 | 0.0782 | 0.933 | 0.84 | 200 |

: **Table S6.** Checkpoint-grid ablation (E3).


| dataset | factor | level | method | fpr mean | frr mean | time saving mean | n splits |
|---|---|---|---|---|---|---|---|
| HUST | cal_fraction | 0.2 | gauss | 0.0788 | 0.128 | 0.679 | 200 |
| HUST | cal_fraction | 0.2 | naive | 0.18 | 0.0714 | 0.381 | 200 |
| HUST | cal_fraction | 0.2 | proposed | 0.041 | 0.0212 | 0.197 | 200 |
| HUST | cal_fraction | 0.2 | single_k100 | 0.0347 | 0.0153 | 0.135 | 200 |
| HUST | cal_fraction | 0.3 | gauss | 0.0797 | 0.132 | 0.681 | 200 |
| HUST | cal_fraction | 0.3 | naive | 0.306 | 0.208 | 0.934 | 200 |
| HUST | cal_fraction | 0.3 | proposed | 0.0751 | 0.0645 | 0.519 | 200 |
| HUST | cal_fraction | 0.3 | single_k100 | 0.0878 | 0.073 | 0.41 | 200 |
| HUST | cal_fraction | 0.4 | gauss | 0.0751 | 0.127 | 0.679 | 200 |
| HUST | cal_fraction | 0.4 | naive | 0.292 | 0.188 | 0.943 | 200 |
| HUST | cal_fraction | 0.4 | proposed | 0.0613 | 0.0529 | 0.495 | 200 |
| HUST | cal_fraction | 0.4 | single_k100 | 0.072 | 0.0548 | 0.372 | 200 |
| HUST | noise_both | 0.1 | gauss | 0.133 | 0.198 | 0.789 | 200 |
| HUST | noise_both | 0.1 | naive | 0.314 | 0.226 | 0.937 | 200 |
| HUST | noise_both | 0.1 | proposed | 0.0806 | 0.0686 | 0.464 | 200 |
| HUST | noise_both | 0.1 | single_k100 | 0.0799 | 0.0797 | 0.373 | 200 |
| HUST | noise_both | 0.25 | gauss | 0.242 | 0.289 | 0.892 | 200 |
| HUST | noise_both | 0.25 | naive | 0.32 | 0.238 | 0.938 | 200 |
| HUST | noise_both | 0.25 | proposed | 0.0727 | 0.077 | 0.336 | 200 |
| HUST | noise_both | 0.25 | single_k100 | 0.0778 | 0.0847 | 0.324 | 200 |
| HUST | noise_both | 0.5 | gauss | 0.304 | 0.345 | 0.938 | 200 |
| HUST | noise_both | 0.5 | naive | 0.332 | 0.257 | 0.941 | 200 |
| HUST | noise_both | 0.5 | proposed | 0.0729 | 0.0745 | 0.228 | 200 |
| HUST | noise_both | 0.5 | single_k100 | 0.0801 | 0.0807 | 0.288 | 200 |
| HUST | noise_both | 1 | gauss | 0.332 | 0.391 | 0.966 | 200 |
| HUST | noise_both | 1 | naive | 0.354 | 0.285 | 0.94 | 200 |
| HUST | noise_both | 1 | proposed | 0.072 | 0.0767 | 0.173 | 200 |
| HUST | noise_both | 1 | single_k100 | 0.0793 | 0.0812 | 0.24 | 200 |
| HUST | noise_test | 0.1 | gauss | 0.133 | 0.196 | 0.789 | 200 |
| HUST | noise_test | 0.1 | naive | 0.332 | 0.228 | 0.947 | 200 |
| HUST | noise_test | 0.1 | proposed | 0.128 | 0.102 | 0.62 | 200 |
| HUST | noise_test | 0.1 | single_k100 | 0.0959 | 0.0894 | 0.426 | 200 |
| HUST | noise_test | 0.25 | gauss | 0.24 | 0.285 | 0.893 | 200 |
| HUST | noise_test | 0.25 | naive | 0.363 | 0.247 | 0.96 | 200 |
| HUST | noise_test | 0.25 | proposed | 0.275 | 0.187 | 0.798 | 200 |
| HUST | noise_test | 0.25 | single_k100 | 0.139 | 0.139 | 0.482 | 200 |
| HUST | noise_test | 0.5 | gauss | 0.308 | 0.343 | 0.938 | 200 |
| HUST | noise_test | 0.5 | naive | 0.39 | 0.269 | 0.971 | 200 |
| HUST | noise_test | 0.5 | proposed | 0.368 | 0.269 | 0.892 | 200 |
| HUST | noise_test | 0.5 | single_k100 | 0.2 | 0.194 | 0.547 | 200 |
| HUST | noise_test | 1 | gauss | 0.328 | 0.372 | 0.966 | 200 |
| HUST | noise_test | 1 | naive | 0.41 | 0.287 | 0.98 | 200 |
| HUST | noise_test | 1 | proposed | 0.43 | 0.313 | 0.946 | 200 |
| HUST | noise_test | 1 | single_k100 | 0.259 | 0.258 | 0.627 | 200 |
| HUST | train_fraction | 0.2 | gauss | 0.16 | 0.214 | 0.757 | 200 |
| HUST | train_fraction | 0.2 | naive | 0.285 | 0.219 | 0.881 | 200 |
| HUST | train_fraction | 0.2 | proposed | 0.0677 | 0.0732 | 0.374 | 200 |
| HUST | train_fraction | 0.2 | single_k100 | 0.0677 | 0.0613 | 0.283 | 200 |
| HUST | train_fraction | 0.3 | gauss | 0.117 | 0.149 | 0.712 | 200 |
| HUST | train_fraction | 0.3 | naive | 0.308 | 0.197 | 0.91 | 200 |
| HUST | train_fraction | 0.3 | proposed | 0.0781 | 0.0601 | 0.445 | 200 |
| HUST | train_fraction | 0.3 | single_k100 | 0.0796 | 0.0639 | 0.345 | 200 |
| HUST | train_fraction | 0.4 | gauss | 0.0797 | 0.132 | 0.681 | 200 |
| HUST | train_fraction | 0.4 | naive | 0.306 | 0.208 | 0.934 | 200 |
| HUST | train_fraction | 0.4 | proposed | 0.0751 | 0.0645 | 0.519 | 200 |
| HUST | train_fraction | 0.4 | single_k100 | 0.0878 | 0.073 | 0.41 | 200 |
| MATR+CLO | cal_fraction | 0.1 | gauss | 0.0495 | 0.0429 | 0.78 | 200 |
| MATR+CLO | cal_fraction | 0.1 | naive | 0.108 | 0.172 | 0.605 | 200 |
| MATR+CLO | cal_fraction | 0.1 | proposed | 0.0449 | 0.0503 | 0.411 | 200 |
| MATR+CLO | cal_fraction | 0.1 | single_k100 | 0.0395 | 0.0488 | 0.415 | 200 |
| MATR+CLO | cal_fraction | 0.15 | gauss | 0.05 | 0.0424 | 0.78 | 200 |
| MATR+CLO | cal_fraction | 0.15 | naive | 0.135 | 0.153 | 0.921 | 200 |
| MATR+CLO | cal_fraction | 0.15 | proposed | 0.0674 | 0.0621 | 0.711 | 200 |
| MATR+CLO | cal_fraction | 0.15 | single_k100 | 0.0736 | 0.0485 | 0.739 | 200 |
| MATR+CLO | cal_fraction | 0.2 | gauss | 0.0513 | 0.0426 | 0.78 | 200 |
| MATR+CLO | cal_fraction | 0.2 | naive | 0.134 | 0.155 | 0.946 | 200 |
| MATR+CLO | cal_fraction | 0.2 | proposed | 0.0617 | 0.0636 | 0.721 | 200 |
| MATR+CLO | cal_fraction | 0.2 | single_k100 | 0.0715 | 0.0559 | 0.761 | 200 |
| MATR+CLO | cal_fraction | 0.25 | gauss | 0.0514 | 0.0418 | 0.781 | 200 |
| MATR+CLO | cal_fraction | 0.25 | naive | 0.144 | 0.159 | 0.953 | 200 |
| MATR+CLO | cal_fraction | 0.25 | proposed | 0.0747 | 0.0761 | 0.802 | 200 |
| MATR+CLO | cal_fraction | 0.25 | single_k100 | 0.0943 | 0.0491 | 0.802 | 200 |
| MATR+CLO | noise_both | 0.1 | gauss | 0.0671 | 0.0683 | 0.834 | 200 |
| MATR+CLO | noise_both | 0.1 | naive | 0.151 | 0.172 | 0.955 | 200 |
| MATR+CLO | noise_both | 0.1 | proposed | 0.0721 | 0.0739 | 0.788 | 200 |
| MATR+CLO | noise_both | 0.1 | single_k100 | 0.0909 | 0.0535 | 0.795 | 200 |
| MATR+CLO | noise_both | 0.25 | gauss | 0.114 | 0.125 | 0.909 | 200 |
| MATR+CLO | noise_both | 0.25 | naive | 0.164 | 0.19 | 0.955 | 200 |
| MATR+CLO | noise_both | 0.25 | proposed | 0.0711 | 0.0655 | 0.724 | 200 |
| MATR+CLO | noise_both | 0.25 | single_k100 | 0.0873 | 0.0716 | 0.754 | 200 |
| MATR+CLO | noise_both | 0.5 | gauss | 0.157 | 0.206 | 0.937 | 200 |
| MATR+CLO | noise_both | 0.5 | naive | 0.188 | 0.208 | 0.952 | 200 |
| MATR+CLO | noise_both | 0.5 | proposed | 0.0695 | 0.0632 | 0.583 | 200 |
| MATR+CLO | noise_both | 0.5 | single_k100 | 0.0805 | 0.0832 | 0.637 | 200 |
| MATR+CLO | noise_both | 1 | gauss | 0.248 | 0.305 | 0.949 | 200 |
| MATR+CLO | noise_both | 1 | naive | 0.236 | 0.258 | 0.943 | 200 |
| MATR+CLO | noise_both | 1 | proposed | 0.0738 | 0.0636 | 0.36 | 200 |
| MATR+CLO | noise_both | 1 | single_k100 | 0.0775 | 0.0863 | 0.43 | 200 |
| MATR+CLO | noise_test | 0.1 | gauss | 0.0667 | 0.0704 | 0.833 | 200 |
| MATR+CLO | noise_test | 0.1 | naive | 0.16 | 0.187 | 0.956 | 200 |
| MATR+CLO | noise_test | 0.1 | proposed | 0.0883 | 0.101 | 0.837 | 200 |
| MATR+CLO | noise_test | 0.1 | single_k100 | 0.0975 | 0.0524 | 0.8 | 200 |
| MATR+CLO | noise_test | 0.25 | gauss | 0.11 | 0.131 | 0.91 | 200 |
| MATR+CLO | noise_test | 0.25 | naive | 0.179 | 0.226 | 0.959 | 200 |
| MATR+CLO | noise_test | 0.25 | proposed | 0.126 | 0.163 | 0.897 | 200 |
| MATR+CLO | noise_test | 0.25 | single_k100 | 0.107 | 0.0836 | 0.798 | 200 |
| MATR+CLO | noise_test | 0.5 | gauss | 0.152 | 0.195 | 0.937 | 200 |
| MATR+CLO | noise_test | 0.5 | naive | 0.221 | 0.283 | 0.961 | 200 |
| MATR+CLO | noise_test | 0.5 | proposed | 0.167 | 0.246 | 0.934 | 200 |
| MATR+CLO | noise_test | 0.5 | single_k100 | 0.146 | 0.15 | 0.799 | 200 |
| MATR+CLO | noise_test | 1 | gauss | 0.234 | 0.3 | 0.949 | 200 |
| MATR+CLO | noise_test | 1 | naive | 0.31 | 0.352 | 0.963 | 200 |
| MATR+CLO | noise_test | 1 | proposed | 0.24 | 0.345 | 0.951 | 200 |
| MATR+CLO | noise_test | 1 | single_k100 | 0.233 | 0.257 | 0.812 | 200 |
| MATR+CLO | train_fraction | 0.2 | gauss | 0.0597 | 0.0755 | 0.797 | 200 |
| MATR+CLO | train_fraction | 0.2 | naive | 0.156 | 0.168 | 0.95 | 200 |
| MATR+CLO | train_fraction | 0.2 | proposed | 0.0657 | 0.0694 | 0.704 | 200 |
| MATR+CLO | train_fraction | 0.2 | single_k100 | 0.0801 | 0.0586 | 0.772 | 200 |
| MATR+CLO | train_fraction | 0.3 | gauss | 0.0532 | 0.0617 | 0.796 | 200 |
| MATR+CLO | train_fraction | 0.3 | naive | 0.144 | 0.173 | 0.952 | 200 |
| MATR+CLO | train_fraction | 0.3 | proposed | 0.0644 | 0.0758 | 0.753 | 200 |
| MATR+CLO | train_fraction | 0.3 | single_k100 | 0.0736 | 0.0588 | 0.781 | 200 |
| MATR+CLO | train_fraction | 0.4 | gauss | 0.0535 | 0.0468 | 0.786 | 200 |
| MATR+CLO | train_fraction | 0.4 | naive | 0.15 | 0.169 | 0.954 | 200 |
| MATR+CLO | train_fraction | 0.4 | proposed | 0.0735 | 0.0772 | 0.794 | 200 |
| MATR+CLO | train_fraction | 0.4 | single_k100 | 0.0827 | 0.0569 | 0.794 | 200 |
| MATR+CLO | train_fraction | 0.5 | gauss | 0.0514 | 0.0418 | 0.781 | 200 |
| MATR+CLO | train_fraction | 0.5 | naive | 0.144 | 0.159 | 0.953 | 200 |
| MATR+CLO | train_fraction | 0.5 | proposed | 0.0747 | 0.0761 | 0.802 | 200 |
| MATR+CLO | train_fraction | 0.5 | single_k100 | 0.0943 | 0.0491 | 0.802 | 200 |

: **Table S7.** Robustness to calibration-set size, training-set size and feature noise (E4).


| experiment | target | scenario | n target cal | method | fpr mean | fpr ci hi | frr mean | frr ci hi | time saving mean | n splits |
|---|---|---|---|---|---|---|---|---|---|---|
| batch_shift | b3 | source_cal | 0 | gauss | 0.02 | 0.031 | 0.805 | 0.831 | 0.964 | 200 |
| batch_shift | b3 | source_cal | 0 | naive | 0.14 | 0.173 | 0.637 | 0.694 | 0.954 | 200 |
| batch_shift | b3 | source_cal | 0 | point_k100 | 0.055 | 0.0722 | 0.0746 | 0.0865 | 0.865 | 200 |
| batch_shift | b3 | source_cal | 0 | proposed | 0.128 | 0.152 | 0.48 | 0.535 | 0.919 | 200 |
| batch_shift | b3 | source_cal | 0 | single_k100 | 0.227 | 0.252 | 0.0118 | 0.0165 | 0.833 | 200 |
| batch_shift | b3 | target_cal | 20 | gauss | 0.035 | 0.0605 | 0.813 | 0.839 | 0.965 | 200 |
| batch_shift | b3 | target_cal | 20 | naive | 0 | 0 | 0.223 | 0.245 | 0.233 | 200 |
| batch_shift | b3 | target_cal | 20 | point_k100 | 0.075 | 0.112 | 0.0737 | 0.0862 | 0.866 | 200 |
| batch_shift | b3 | target_cal | 20 | proposed | 0 | 0 | 0.0492 | 0.0583 | 0.0598 | 200 |
| batch_shift | b3 | target_cal | 20 | single_k100 | 0 | 0 | 0.0532 | 0.0633 | 0.0738 | 200 |
| batch_shift | b3 | target_cal | 30 | gauss | 0.035 | 0.0605 | 0.798 | 0.828 | 0.964 | 200 |
| batch_shift | b3 | target_cal | 30 | naive | 0 | 0 | 0.293 | 0.316 | 0.323 | 200 |
| batch_shift | b3 | target_cal | 30 | point_k100 | 0.075 | 0.112 | 0.0683 | 0.0827 | 0.865 | 200 |
| batch_shift | b3 | target_cal | 30 | proposed | 0 | 0 | 0.0628 | 0.0758 | 0.0987 | 200 |
| batch_shift | b3 | target_cal | 30 | single_k100 | 0 | 0 | 0.0683 | 0.0824 | 0.122 | 200 |
| batch_shift | b4 | source_cal | 0 | gauss | 0.0128 | 0.019 | 0.945 | 0.962 | 0.966 | 200 |
| batch_shift | b4 | source_cal | 0 | naive | 0.187 | 0.227 | 0.704 | 0.765 | 0.931 | 200 |
| batch_shift | b4 | source_cal | 0 | point_k100 | 0.361 | 0.383 | 0.0956 | 0.121 | 0.856 | 200 |
| batch_shift | b4 | source_cal | 0 | proposed | 0.152 | 0.178 | 0.597 | 0.658 | 0.881 | 200 |
| batch_shift | b4 | source_cal | 0 | single_k100 | 0.479 | 0.505 | 0.0415 | 0.0591 | 0.784 | 200 |
| batch_shift | b4 | target_cal | 20 | gauss | 0.012 | 0.0181 | 0.943 | 0.962 | 0.966 | 200 |
| batch_shift | b4 | target_cal | 20 | naive | 0 | 0 | 0.473 | 0.497 | 0.581 | 200 |
| batch_shift | b4 | target_cal | 20 | point_k100 | 0.354 | 0.378 | 0.0957 | 0.123 | 0.856 | 200 |
| batch_shift | b4 | target_cal | 20 | proposed | 0 | 0 | 0.0797 | 0.0958 | 0.0945 | 200 |
| batch_shift | b4 | target_cal | 20 | single_k100 | 0 | 0 | 0.0783 | 0.092 | 0.23 | 200 |
| batch_shift | b4 | target_cal | 30 | gauss | 0.0125 | 0.0198 | 0.942 | 0.962 | 0.966 | 200 |
| batch_shift | b4 | target_cal | 30 | naive | 0.25 | 0.276 | 0.222 | 0.244 | 0.921 | 200 |
| batch_shift | b4 | target_cal | 30 | point_k100 | 0.341 | 0.37 | 0.101 | 0.131 | 0.856 | 200 |
| batch_shift | b4 | target_cal | 30 | proposed | 0.075 | 0.0923 | 0.0456 | 0.0585 | 0.268 | 200 |
| batch_shift | b4 | target_cal | 30 | single_k100 | 0.06 | 0.0729 | 0.055 | 0.0682 | 0.425 | 200 |
| cross_lab | HUST | source_model_target_cal | -1 | gauss | 0.0337 | 0.0515 | 0.95 | 0.969 | 0.987 | 200 |
| cross_lab | HUST | source_model_target_cal | -1 | naive | 0.314 | 0.34 | 0.245 | 0.269 | 0.675 | 200 |
| cross_lab | HUST | source_model_target_cal | -1 | point_k100 | 0.519 | 0.551 | 0.605 | 0.631 | 0.942 | 200 |
| cross_lab | HUST | source_model_target_cal | -1 | proposed | 0.08 | 0.0955 | 0.0705 | 0.0846 | 0.239 | 200 |
| cross_lab | HUST | source_model_target_cal | -1 | single_k100 | 0.0779 | 0.0936 | 0.0832 | 0.0976 | 0.248 | 200 |
| cross_lab | HUST | target_model_target_cal | -1 | gauss | 0.0242 | 0.0317 | 0.0555 | 0.0641 | 0.334 | 200 |
| cross_lab | HUST | target_model_target_cal | -1 | naive | 0.234 | 0.255 | 0.139 | 0.157 | 0.828 | 200 |
| cross_lab | HUST | target_model_target_cal | -1 | point_k100 | 0.212 | 0.23 | 0.303 | 0.325 | 0.942 | 200 |
| cross_lab | HUST | target_model_target_cal | -1 | proposed | 0.0804 | 0.0959 | 0.0695 | 0.0819 | 0.47 | 200 |
| cross_lab | HUST | target_model_target_cal | -1 | single_k100 | 0.0792 | 0.0955 | 0.0695 | 0.0823 | 0.414 | 200 |

: **Table S8.** Batch shift and laboratory shift (E5).


| dataset | model | split seconds | peak rss mb | n checkpoints | decide seconds per 1000 cells |
|---|---|---|---|---|---|
| HUST | calibration_only_n40 | 7.18e-05 | – | 17 | 0.025 |
| HUST | calibration_only_n400 | 0.000139 | – | 17 | 0.022 |
| HUST | calibration_only_n4000 | 0.00222 | – | 17 | 0.0218 |
| HUST | cnn | 4.63 | 881 | 17 | – |
| HUST | en | 2.55 | 881 | 17 | – |
| HUST | gbr | 10.7 | 881 | 17 | – |
| HUST | gp | 1.42 | 881 | 17 | – |
| HUST | logit | 1.79 | 881 | 17 | – |
| HUST | rf | 18.5 | 881 | 17 | – |
| MATR+CLO | calibration_only_n40 | 6.02e-05 | – | 16 | 0.0238 |
| MATR+CLO | calibration_only_n400 | 0.000101 | – | 16 | 0.0222 |
| MATR+CLO | calibration_only_n4000 | 0.000603 | – | 16 | 0.0226 |
| MATR+CLO | cnn | 6.24 | 856 | 16 | – |
| MATR+CLO | en | 1.69 | 856 | 16 | – |
| MATR+CLO | gbr | 11.2 | 856 | 16 | – |
| MATR+CLO | gp | 4.47 | 856 | 16 | – |
| MATR+CLO | logit | 1.52 | 856 | 16 | – |
| MATR+CLO | rf | 19.1 | 856 | 16 | – |

: **Table S9.** Computational cost (E6).


| dataset | factor | alpha | beta | Lstar | method | fpr mean | frr mean | fpr le alpha | frr le beta | time saving mean | bad share | n splits |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HUST | Lstar | 0.1 | 0.1 | 1600 | gauss | 0.322 | 0.0175 | False | True | 0.797 | 0.237 | 200 |
| HUST | Lstar | 0.1 | 0.1 | 1600 | naive | 0.0075 | 0.309 | True | False | 0.411 | 0.237 | 200 |
| HUST | Lstar | 0.1 | 0.1 | 1600 | proposed | 0.0025 | 0.063 | True | True | 0.155 | 0.237 | 200 |
| HUST | Lstar | 0.1 | 0.1 | 1600 | single_k100 | 0.005 | 0.0681 | True | True | 0.13 | 0.237 | 200 |
| HUST | Lstar | 0.1 | 0.1 | 1900 | gauss | 0.0854 | 0.142 | True | False | 0.688 | 0.521 | 200 |
| HUST | Lstar | 0.1 | 0.1 | 1900 | naive | 0.297 | 0.23 | False | False | 0.941 | 0.521 | 200 |
| HUST | Lstar | 0.1 | 0.1 | 1900 | proposed | 0.0731 | 0.081 | True | True | 0.532 | 0.521 | 200 |
| HUST | Lstar | 0.1 | 0.1 | 1900 | single_k100 | 0.0715 | 0.0904 | True | True | 0.395 | 0.521 | 200 |
| HUST | Lstar | 0.1 | 0.1 | 2200 | gauss | 0.0256 | 0.298 | True | False | 0.827 | 0.732 | 200 |
| HUST | Lstar | 0.1 | 0.1 | 2200 | naive | 0.367 | 0.00417 | False | True | 0.531 | 0.732 | 200 |
| HUST | Lstar | 0.1 | 0.1 | 2200 | proposed | 0.065 | 0.00167 | True | True | 0.2 | 0.732 | 200 |
| HUST | Lstar | 0.1 | 0.1 | 2200 | single_k100 | 0.063 | 0.00167 | True | True | 0.19 | 0.732 | 200 |
| HUST | alpha_beta | 0.05 | 0.05 | 1900 | gauss | 0.0493 | 0.0834 | True | False | 0.522 | 0.521 | 200 |
| HUST | alpha_beta | 0.05 | 0.05 | 1900 | naive | 0 | 0 | True | True | 0 | 0.521 | 200 |
| HUST | alpha_beta | 0.05 | 0.05 | 1900 | proposed | 0 | 0 | True | True | 0 | 0.521 | 200 |
| HUST | alpha_beta | 0.05 | 0.05 | 1900 | single_k100 | 0 | 0 | True | True | 0 | 0.521 | 200 |
| HUST | alpha_beta | 0.05 | 0.2 | 1900 | gauss | 0.0345 | 0.274 | True | False | 0.752 | 0.521 | 200 |
| HUST | alpha_beta | 0.05 | 0.2 | 1900 | naive | 0 | 0.537 | True | False | 0.697 | 0.521 | 200 |
| HUST | alpha_beta | 0.05 | 0.2 | 1900 | proposed | 0 | 0.186 | True | True | 0.388 | 0.521 | 200 |
| HUST | alpha_beta | 0.05 | 0.2 | 1900 | single_k100 | 0 | 0.192 | True | True | 0.324 | 0.521 | 200 |
| HUST | alpha_beta | 0.1 | 0.1 | 1900 | gauss | 0.0854 | 0.142 | True | False | 0.688 | 0.521 | 200 |
| HUST | alpha_beta | 0.1 | 0.1 | 1900 | naive | 0.297 | 0.23 | False | False | 0.941 | 0.521 | 200 |
| HUST | alpha_beta | 0.1 | 0.1 | 1900 | proposed | 0.0731 | 0.081 | True | True | 0.532 | 0.521 | 200 |
| HUST | alpha_beta | 0.1 | 0.1 | 1900 | single_k100 | 0.0715 | 0.0904 | True | True | 0.395 | 0.521 | 200 |
| HUST | alpha_beta | 0.2 | 0.2 | 1900 | gauss | 0.148 | 0.249 | True | False | 0.884 | 0.521 | 200 |
| HUST | alpha_beta | 0.2 | 0.2 | 1900 | naive | 0.322 | 0.279 | False | False | 0.982 | 0.521 | 200 |
| HUST | alpha_beta | 0.2 | 0.2 | 1900 | proposed | 0.141 | 0.164 | True | True | 0.759 | 0.521 | 200 |
| HUST | alpha_beta | 0.2 | 0.2 | 1900 | single_k100 | 0.174 | 0.186 | True | True | 0.653 | 0.521 | 200 |
| MATR+CLO | Lstar | 0.1 | 0.1 | 550 | gauss | 0.1 | 0.014 | True | True | 0.798 | 0.282 | 200 |
| MATR+CLO | Lstar | 0.1 | 0.1 | 550 | naive | 0.191 | 0.141 | False | False | 0.925 | 0.282 | 200 |
| MATR+CLO | Lstar | 0.1 | 0.1 | 550 | proposed | 0.0693 | 0.0845 | True | True | 0.775 | 0.282 | 200 |
| MATR+CLO | Lstar | 0.1 | 0.1 | 550 | single_k100 | 0.066 | 0.0613 | True | True | 0.776 | 0.282 | 200 |
| MATR+CLO | Lstar | 0.1 | 0.1 | 750 | gauss | 0.0519 | 0.0357 | True | True | 0.776 | 0.478 | 200 |
| MATR+CLO | Lstar | 0.1 | 0.1 | 750 | naive | 0.144 | 0.154 | False | False | 0.955 | 0.478 | 200 |
| MATR+CLO | Lstar | 0.1 | 0.1 | 750 | proposed | 0.0665 | 0.0695 | True | True | 0.794 | 0.478 | 200 |
| MATR+CLO | Lstar | 0.1 | 0.1 | 750 | single_k100 | 0.0895 | 0.0545 | True | True | 0.8 | 0.478 | 200 |
| MATR+CLO | Lstar | 0.1 | 0.1 | 900 | gauss | 0.0382 | 0.105 | True | True | 0.712 | 0.726 | 200 |
| MATR+CLO | Lstar | 0.1 | 0.1 | 900 | naive | 0.207 | 0.197 | False | False | 0.931 | 0.726 | 200 |
| MATR+CLO | Lstar | 0.1 | 0.1 | 900 | proposed | 0.0806 | 0.0761 | True | True | 0.697 | 0.726 | 200 |
| MATR+CLO | Lstar | 0.1 | 0.1 | 900 | single_k100 | 0.0934 | 0.0605 | True | True | 0.668 | 0.726 | 200 |
| MATR+CLO | alpha_beta | 0.05 | 0.05 | 750 | gauss | 0.0291 | 0.0168 | True | True | 0.666 | 0.478 | 200 |
| MATR+CLO | alpha_beta | 0.05 | 0.05 | 750 | naive | 0.0885 | 0.126 | False | False | 0.795 | 0.478 | 200 |
| MATR+CLO | alpha_beta | 0.05 | 0.05 | 750 | proposed | 0.0337 | 0.0252 | True | True | 0.538 | 0.478 | 200 |
| MATR+CLO | alpha_beta | 0.05 | 0.05 | 750 | single_k100 | 0.0361 | 0.0327 | True | True | 0.572 | 0.478 | 200 |
| MATR+CLO | alpha_beta | 0.05 | 0.2 | 750 | gauss | 0.0247 | 0.0939 | True | True | 0.761 | 0.478 | 200 |
| MATR+CLO | alpha_beta | 0.05 | 0.2 | 750 | naive | 0.0584 | 0.371 | True | False | 0.889 | 0.478 | 200 |
| MATR+CLO | alpha_beta | 0.05 | 0.2 | 750 | proposed | 0.0262 | 0.171 | True | True | 0.69 | 0.478 | 200 |
| MATR+CLO | alpha_beta | 0.05 | 0.2 | 750 | single_k100 | 0.0361 | 0.147 | True | True | 0.686 | 0.478 | 200 |
| MATR+CLO | alpha_beta | 0.1 | 0.1 | 750 | gauss | 0.0519 | 0.0357 | True | True | 0.776 | 0.478 | 200 |
| MATR+CLO | alpha_beta | 0.1 | 0.1 | 750 | naive | 0.144 | 0.154 | False | False | 0.955 | 0.478 | 200 |
| MATR+CLO | alpha_beta | 0.1 | 0.1 | 750 | proposed | 0.0665 | 0.0695 | True | True | 0.794 | 0.478 | 200 |
| MATR+CLO | alpha_beta | 0.1 | 0.1 | 750 | single_k100 | 0.0895 | 0.0545 | True | True | 0.8 | 0.478 | 200 |
| MATR+CLO | alpha_beta | 0.2 | 0.2 | 750 | gauss | 0.0791 | 0.0899 | True | True | 0.895 | 0.478 | 200 |
| MATR+CLO | alpha_beta | 0.2 | 0.2 | 750 | naive | 0.206 | 0.19 | True | True | 0.967 | 0.478 | 200 |
| MATR+CLO | alpha_beta | 0.2 | 0.2 | 750 | proposed | 0.136 | 0.145 | True | True | 0.942 | 0.478 | 200 |
| MATR+CLO | alpha_beta | 0.2 | 0.2 | 750 | single_k100 | 0.191 | 0.023 | True | True | 0.847 | 0.478 | 200 |

: **Table S10.** Sensitivity to the error levels and to the specification L* (E7).


| dataset | method | fpr mean | fpr ci hi | frr mean | frr ci hi | accuracy mean | early rate mean | time saving mean | n splits |
|---|---|---|---|---|---|---|---|---|---|
| MATR+CLO (protocol-disjoint) | gauss | 0.0556 | 0.0643 | 0.0629 | 0.0715 | 0.941 | 0.879 | 0.786 | 200 |
| MATR+CLO (protocol-disjoint) | naive | 0.168 | 0.185 | 0.182 | 0.201 | 0.833 | 0.988 | 0.945 | 200 |
| MATR+CLO (protocol-disjoint) | point_k100 | 0.0772 | 0.0876 | 0.0859 | 0.095 | 0.92 | 1 | 0.846 | 200 |
| MATR+CLO (protocol-disjoint) | proposed | 0.0733 | 0.0874 | 0.0877 | 0.101 | 0.924 | 0.833 | 0.751 | 200 |
| MATR+CLO (protocol-disjoint) | single_k100 | 0.0868 | 0.102 | 0.0597 | 0.0706 | 0.931 | 0.925 | 0.776 | 200 |

: **Table S11.** Protocol-disjoint splits on MATR/CLO (E9).


| dataset | cal design | method | fpr mean | frr mean | fpr split above alpha | frr split above beta | never pass | time saving mean | n cal bad | n cal good | n splits |
|---|---|---|---|---|---|---|---|---|---|---|---|
| HUST | default | proposed | 0.072 | 0.0664 | 0.245 | 0.225 | 0.045 | 0.488 | 11.9 | 11.1 | 200 |
| HUST | default | single_k100 | 0.0738 | 0.0739 | 0.255 | 0.26 | 0.045 | 0.385 | 11.9 | 11.1 | 200 |
| HUST | default | traj_pac | 0 | 0 | 0 | 0 | 1 | 0 | 11.9 | 11.1 | 200 |
| HUST | large_cal | proposed | 0.0785 | 0.0686 | 0.355 | 0.315 | 0 | 0.492 | 20.2 | 18.8 | 200 |
| HUST | large_cal | single_k100 | 0.0912 | 0.072 | 0.41 | 0.33 | 0 | 0.387 | 20.2 | 18.8 | 200 |
| HUST | large_cal | traj_pac | 0.0162 | 0 | 0.06 | 0 | 0.805 | 0.0633 | 20.2 | 18.8 | 200 |
| MATR+CLO | default | proposed | 0.0675 | 0.0772 | 0.285 | 0.275 | 0 | 0.785 | 20 | 22 | 200 |
| MATR+CLO | default | single_k100 | 0.0841 | 0.055 | 0.31 | 0.175 | 0 | 0.793 | 20 | 22 | 200 |
| MATR+CLO | default | traj_pac | 0.0111 | 0.027 | 0.045 | 0.08 | 0.75 | 0.281 | 20 | 22 | 200 |
| MATR+CLO | large_cal | proposed | 0.0686 | 0.0742 | 0.3 | 0.31 | 0 | 0.808 | 36.8 | 40.2 | 200 |
| MATR+CLO | large_cal | single_k100 | 0.0886 | 0.0633 | 0.41 | 0.26 | 0 | 0.83 | 36.8 | 40.2 | 200 |
| MATR+CLO | large_cal | traj_pac | 0.0275 | 0.0346 | 0.11 | 0.115 | 0 | 0.563 | 36.8 | 40.2 | 200 |

: **Table S12.** Training-conditional (PAC) calibration (E10).


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

: **Table S13.** Conditional (training-conditional) error of marginally calibrated thresholds. For $n$ calibration cells of a class and $\alpha=0.10$: the rank used by the marginal rule, the probability that the conditional error probability of the resulting threshold exceeds $\alpha$ (Beta$(r,n+1-r)$ law of conformal coverage for continuous scores), and the rank required for a PAC guarantee with $\delta=0.1$ and $\delta=0.2$ (empty: impossible with $n$ cells).


| margin bin | n cells | false pass freq | false reject freq | early decision | mean cycles |
|---|---|---|---|---|---|
| (-0.2, -0.1] | 32 | 0.0112 | 0 | 0.99 | 44.9 |
| (-0.1, -0.05] | 12 | 0.0467 | 0 | 0.854 | 145 |
| (-0.05, 0.0] | 17 | 0.215 | 0 | 0.693 | 261 |
| (0.0, 0.05] | 23 | 0 | 0.169 | 0.678 | 290 |
| (0.05, 0.1] | 28 | 0 | 0.0578 | 0.813 | 193 |
| (0.1, 0.2] | 26 | 0 | 0.0169 | 0.91 | 120 |
| (0.2, inf] | 11 | 0 | 0.0874 | 0.987 | 40.8 |
| (-inf, -0.2] | 20 | 0.0374 | 0 | 0.999 | 34.8 |

: **Table S14.** Error analysis by distance of the true lifetime from the specification, MATR/CLO (proposed rule, E1).


| margin bin | n cells | false pass freq | false reject freq | early decision | mean cycles |
|---|---|---|---|---|---|
| (-0.2, -0.1] | 14 | 0.00668 | 0 | 0.836 | 491 |
| (-0.1, -0.05] | 9 | 0.0757 | 0 | 0.451 | 1.07e+03 |
| (-0.05, 0.0] | 15 | 0.117 | 0 | 0.364 | 1.2e+03 |
| (0.0, 0.05] | 14 | 0 | 0.124 | 0.515 | 1.03e+03 |
| (0.05, 0.1] | 13 | 0 | 0.045 | 0.634 | 875 |
| (0.1, 0.2] | 10 | 0 | 0.0434 | 0.814 | 495 |
| (-inf, -0.2] | 2 | 0.103 | 0 | 0.965 | 210 |

: **Table S15.** Error analysis by distance of the true lifetime from the specification, HUST (proposed rule, E1).


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

: **Table S16.** The ten MATR/CLO cells with the highest error frequency across splits (proposed rule).


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

: **Table S17.** The ten HUST cells with the highest error frequency across splits (proposed rule).


![**Figure S1.** Normalised score trajectories of eight randomly chosen test cells in one split, with the calibrated pass and reject thresholds of the proposed rule.](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig6_score_trajectories.png){width=6.3in}

![**Figure S2.** Row-normalised decision matrices (true class versus decision) pooled over all splits of E1.](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig12_confusion_matrices.png){width=6.3in}

![**Figure S3.** Discrimination of the normalised score between good and bad cells at three checkpoints (pooled test cells of E1): ROC and precision–recall curves.](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig13_roc_pr.png){width=6.3in}

![**Figure S4.** Run time per split and peak memory of the base predictors (E6).](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig14_compute.png){width=6.3in}


## References

[1] K. A. Severson, P. M. Attia, N. Jin, N. Perkins, B. Jiang, Z. Yang, M. H. Chen, M. Aykol, P. K. Herring, D. Fraggedakis, M. Z. Bazant, S. J. Harris, W. C. Chueh, R. D. Braatz, Data-driven prediction of battery cycle life before capacity degradation, *Nature Energy* 2019, 4, 383-391. https://doi.org/10.1038/s41560-019-0356-8

[2] P. M. Attia, A. Grover, N. Jin, K. A. Severson, T. M. Markov, Y. H. Liao, M. H. Chen, B. Cheong, N. Perkins, Z. Yang, P. K. Herring, M. Aykol, S. J. Harris, R. D. Braatz, S. Ermon, W. C. Chueh, Closed-loop optimization of fast-charging protocols for batteries with machine learning, *Nature* 2020, 578, 397-402. https://doi.org/10.1038/s41586-020-1994-5

[3] G. Ma, S. Xu, B. Jiang, C. Cheng, X. Yang, Y. Shen, T. Yang, Y. Huang, H. Ding, Y. Yuan, Real-time personalized health status prediction of lithium-ion batteries using deep transfer learning, *Energy &amp; Environmental Science* 2022, 15, 4083-4094. https://doi.org/10.1039/d2ee01676a