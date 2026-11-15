# Research design (frozen before the full experiments)

Frozen: 2026-11-15, after a pilot of 100 random splits (seeds 1000-1099, elastic net,
MATR+CLO and HUST; 50 splits logistic). The pilot was used only to (i) find and fix a
feature-extraction defect (single-cycle Q(V) glitches at non-standard cycles, fixed by a
5-cycle median window that uses no future cycles) and (ii) check run time. The method,
thresholds, metrics and statistical tests below were not changed after seeing pilot
efficiency numbers. Final experiments use seeds derived from `seed_base = 20261115`,
disjoint from the pilot seeds. Pilot numbers are not reported as results.

## Hypothesis

H. For early screening of lithium-ion cells against a cycle-life specification L*, a
sequential rule whose pass/reject thresholds are calibrated on the *maximum over
checkpoints* of normalised model scores (trajectory calibration) keeps the per-cell
false-pass and false-reject probabilities at or below pre-set levels alpha, beta under
data-dependent early termination, whereas per-checkpoint calibration does not; it
achieves this with calibration cells cycled only to min(T, L*), and still shortens
testing substantially relative to observing every cell to L*.

## Research questions -> experiments

| RQ | Question | Experiment |
|---|---|---|
| RQ1 | Are false-pass/false-reject rates controlled at nominal levels under sequential early stopping, and how much do naive sequential and uncalibrated rules violate them? | E1 main (1000 splits per dataset) |
| RQ2 | How much cycling is saved relative to full observation, a fixed single checkpoint, Bonferroni, Bayesian/parametric rules and full-lifetime conformal intervals? | E1, E2 |
| RQ3 | Which components matter (trajectory max, score normalisation, multiple looks/grid, class-conditional calibration, full-lifetime vs truncated training)? | E3 ablation |
| RQ4 | How robust are validity and efficiency to calibration-set size, measurement noise, class imbalance (L*), training-set size, alpha/beta? | E4 robustness, E7 sensitivity |
| RQ5 | Do guarantees survive batch shift and a change of laboratory, and can a few target cells (cycled only to L*) restore validity? | E5 generalisation |
| RQ6 | What does the method cost computationally? | E6 |
| RQ7 | Which cells are mis-screened and why? | E8 error analysis |

## Data and splits

* MATR+CLO: 169 LFP/graphite A123 APR18650M1A cells (124 Severson et al. 2019 + 45
  Attia et al. 2020), lifetimes 148-2237 cycles; main L* = 750 (near the median 761).
* HUST: 77 cells of the same type (Ma et al. 2022), different lab and discharge
  protocols, lifetimes 1142-2689; main L* = 1900 (median 1875).
* Unit = cell. Random partitions stratified by (dataset, class Z): MATR+CLO
  train/cal/test = 50/25/25 %; HUST 40/30/30 % (keeps >= 9 cells per class in
  calibration, the minimum for alpha = 0.1 because ceil((n+1)(1-alpha)) <= n requires n >= 9).
* Checkpoints: MATR+CLO {20,30,...,100,120,...,200,250,300}; HUST {20,...,100,150,200,
  300,400,500,600,800,1000}. All < L*.

## Methods compared (same base model, same splits)

| ID | Rule | Error control |
|---|---|---|
| proposed | trajectory (max) calibration of normalised scores, all checkpoints | finite-sample, class-conditional, stopping-valid |
| naive | per-checkpoint conformal thresholds at level alpha, first crossing | none under stopping |
| bonf | per-checkpoint at alpha/M | valid, conservative |
| single_k100 | class-conditional conformal at cycle 100 only | valid |
| point_k100 | Severson-style point prediction at cycle 100 vs L* | none |
| gauss | normalised score vs z_{1-alpha} (parametric, uncalibrated) — for GP this is the Bayesian posterior-probability rule | none |
| interval_traj | trajectory-valid conformal lower/upper bounds on lifetime (needs full lifetimes for calibration) | marginal |
| traj_unnorm | ablation: proposed without score normalisation | valid |

Base predictors: elastic net (main), logistic regression on Z (truncated training), gradient
boosting, random forest, Gaussian process, 1-D CNN on dQ(V)/dV(q) curves + scalar features.

## Metrics

False-pass rate among bad test cells (FPR), false-reject rate among good test cells (FRR),
accuracy, share decided by the model before L*, mean cycles to decision, fractional cycling
time saved = 1 - sum(time to decision) / sum(min(T, L*)), calibration/training campaign
cell-cycles and wall-clock (max cycles).

## Statistics

* Validity: mean FPR/FRR over splits with 95% CI; share of splits above nominal level
  (expected to be non-zero; the guarantee is in expectation).
* Efficiency comparisons: cell-level average time to decision across the splits in which the
  cell was a test cell; paired Wilcoxon signed-rank test (cells = independent units),
  Holm correction across baselines; effect size = matched-pairs rank-biserial correlation
  and median paired difference; bootstrap (cells resampled, 10,000 draws) 95% CI for the
  difference in mean time saved.
