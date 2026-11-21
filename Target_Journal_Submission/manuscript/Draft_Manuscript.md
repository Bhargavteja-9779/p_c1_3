# Stopping Cycle-Life Tests Early With Distribution-Free Error Control: Sequential Screening of Lithium-Ion Cells Calibrated on Truncated Test Campaigns

**Running title:** Early cycle-life screening with error control

**Authors:** Bhargav Teja^1,\*^, [Second Author]^1^

^1^ [Department], Vellore Institute of Technology, Vellore 632014, Tamil Nadu, India

\* Correspondence: Bhargav Teja, [e-mail address]

## Abstract

Early-cycle lifetime predictions of lithium-ion cells are increasingly used to stop cycling tests early, but the error rate of the resulting pass/fail decisions is rarely controlled, and re-checking predictions as cycling proceeds inflates it. We present a distribution-free sequential screening procedure that, at a series of early checkpoints, passes a cell, rejects it or keeps it on test. Pass and reject thresholds are calibrated on the maximum over checkpoints of normalised model scores of held-out calibration cells, which bounds the class-conditional false-pass and false-reject probabilities at user-chosen levels under any data-dependent stopping time, on average over calibration sets; calibration cells need to be cycled only to the specification. On 246 commercial LiFePO~4~/graphite cells from two laboratories (1,000 random splits per data set, nominal level 0.10), the false-pass and false-reject rates were 0.068 and 0.080 (MATR/CLO) and 0.068 and 0.074 (HUST), and 78.3% and 50.7% of the cycling needed to observe every cell to the specification was saved. For an individual calibration campaign at least one rate exceeded 0.10 in 51% and 43% of the splits. Sequential use of individually valid per-checkpoint thresholds exceeded the targets by up to 2.9 times. A single checkpoint chosen on training cells was as efficient as the sequential rule, so the benefit of trajectory calibration is valid control under repeated looks rather than faster screening. Truncation shortened the calibration campaign by factors of 2.61 and 1.38. Under batch shift the guarantees failed unless thresholds were recalibrated on cells of the new batch. The procedure works with any lifetime predictor and adds negligible computation.

**Keywords:** lithium-ion battery; cycle life; early prediction; battery testing; conformal prediction; sequential decision; uncertainty quantification

## 1 Introduction

Cycle-life testing is the slowest step in the development and qualification of lithium-ion cells. A cell that lasts 761 cycles under fast charging occupies a cycler channel for weeks to months before its end of life (EOL, conventionally 80% of nominal capacity) is observed, and design or protocol comparisons need many such cells because cell-to-cell variation in ageing is large even within one production batch [1–3]. Data-driven early prediction has therefore attracted sustained attention. Severson et al. showed that features derived from the first 100 cycles, chiefly the variance of the discharge-capacity curve difference between cycles 10 and 100, predict the cycle life of commercial LiFePO~4~/graphite cells with about 9% test error for their full model [1]; Attia et al. embedded such predictions in closed-loop optimisation of fast-charging protocols and cut the experimental time from more than 500 to 16 days [2]; and hierarchical Bayesian models predicted protocol lifetimes from a few cycles [4]. Later work refined features and knee prediction [5–7], used transfer or semi-supervised learning with unfinished cells [8–10], combined physics with learning [11], and built open benchmarks [12]. Reviews in this journal and elsewhere identify uncertainty-aware lifetime prediction as an open need [13–15].

In qualification and screening, however, the question asked of an early prediction is a decision: does this cell (or this design) meet a cycle-life specification $L^\ast$? Acting on a point prediction exposes the laboratory to an error rate that is unknown in advance. Ensemble, Gaussian-process or Bayesian uncertainty estimates [4,16–18] are model-dependent and are not guaranteed to be calibrated for a new set of cells. A second, less discussed problem is *repeated looking*. As cycling proceeds, engineers naturally re-evaluate the prediction and stop a test as soon as the prediction looks decisive. Even if each individual look controls its error, stopping at the first look that crosses a threshold inflates the overall error; this is the optional-stopping problem of sequential analysis [19,20]. Finally, the uncertainty methods that do carry finite-sample guarantees, such as conformal prediction intervals for lifetime [21–23], have so far been calibrated in battery work with cells cycled to EOL [24], which brings back the long test campaign that early prediction was meant to avoid.

### 1.1 Prior work and research gap

**Early cycle-life prediction.** Following Severson et al. [1], early prediction has been extended with feature studies [5], knee-point prediction [6,7], formation-stage diagnostics [25], deep transfer learning on cells with different discharge protocols [8], semi-supervised and incomplete-data learning [9,10], physics-informed networks [11], impedance-based features [26], benchmarks [12] and open data resources [27]. Work in *Battery Energy* on state-of-health estimation and cycle-life prediction likewise combines physically motivated features with machine learning and evaluates point accuracy [28–30]. These works report prediction error at a fixed checkpoint; none provides a decision rule with a pre-specified, guaranteed error rate.

**Uncertainty for battery lifetime.** Ensembles, Gaussian processes and Bayesian hierarchical models provide predictive distributions [4,16–18], whose calibration depends on the model being correct or on post-hoc recalibration without finite-sample guarantees; quantile regression forests give cycle-life ranges from early data [31]. Wu et al. [24] recently compared Bayesian, jackknife+, bootstrap and split-conformal intervals for early-cycle lifetime prediction on the MIT–Stanford cells; their intervals are computed at one fixed early checkpoint from cells cycled to end of life, and they are not used for stop/continue decisions. Conformal intervals have also been used for battery life prediction [32] and to calibrate early-warning decision thresholds [33]. Conformal prediction gives finite-sample, distribution-free coverage under exchangeability [21–23,34] and has recently been applied to state-of-health forecasting [35,36]. Evaluation practice for lifetime models under censoring and differing end-point definitions has also been examined [14,37].

**Statistical foundations.** Our thresholds are class-conditional order statistics, as in Neyman–Pearson classification [38], class-conditional set-valued classifiers [39] and conformal outlier testing [40]; calibrating decision thresholds with finite-sample error control is the subject of Learn-then-Test [41]. Conformalised survival analysis uses lifetimes truncated at a cut-off to obtain valid lower bounds under censoring [42–44]; conformal selection controls the false discovery rate when selecting units whose outcome exceeds a threshold [45]. Controlling error over repeated interim looks is the classical problem of group-sequential designs [46–49], and validity at arbitrary stopping times that of sequential testing, confidence sequences and anytime-valid inference [19,20,50]. Conformal guarantees at data-dependent stopping times have been developed for early-exit neural networks [51], early time-series classification [52] and spiking networks [53]; concurrent work proposes any-stage-valid sequential conformal prediction with less conservatism than Bonferroni corrections [54]. Calibrating on the maximum of a score over an index set is also how simultaneous conformal bands for functional data and trajectory-wide conformal regions are built [55–58], whereas multi-horizon conformal forecasting has used Bonferroni corrections over horizons [59].

**Gap.** Each ingredient needed for early screening exists in the statistics literature: class-conditional conformal thresholds control false-pass and false-reject probabilities, calibrating on the maximum of a score over an index set keeps validity across many looks, and calibrating on a class rather than a lifetime allows censoring at a fixed cut-off. What is missing in battery testing is a screening rule that combines them — one that controls the class-conditional false-pass and false-reject probabilities with finite-sample, distribution-free guarantees when the test is stopped at a data-dependent checkpoint, using calibration cells cycled only to the specification — together with an honest assessment of when such a rule saves cycling and when it does not. The contribution of this paper is that combination and assessment, not a new statistical principle.

### 1.2 Aim and contributions of this work

This paper addresses these three problems for early cycle-life screening. Its contributions are:

1. **Formulation.** Early screening is posed as a sequential decision at checkpoints $k_1<\dots<k_M<L^\ast$ with three outcomes (pass, reject, continue cycling) and two class-conditional error constraints: a cell that will not reach $L^\ast$ ("bad") is passed with probability at most $\alpha$, and a cell that will reach $L^\ast$ ("good") is rejected with probability at most $\beta$.
2. **Trajectory calibration with a finite-sample guarantee.** Pass and reject thresholds are calibrated on the *maximum over checkpoints* of normalised model scores of held-out calibration cells. The two error constraints then hold on average over calibration sets for any data-dependent stopping time, without distributional assumptions beyond exchangeability of cells, and each calibration cell needs to be cycled only to $\min(T,L^\ast)$ cycles, not to EOL. The guarantee holds for any base predictor, including one trained only on truncated data; a training-conditional variant is also given.
3. **Evaluation on two laboratories.** On 246 commercial LiFePO~4~/graphite cells from two laboratories (169 MATR/CLO cells [1,2] and 77 HUST cells [8]) and 1,000 random splits per dataset, we compare the procedure with single-checkpoint rules (fixed, or chosen on training cells), naive sequential, Bonferroni, Gaussian/Bayesian (with and without correction for repeated looks), point-prediction and lifetime-interval rules, and report five additional base predictors, checkpoint-grid ablations, robustness and sensitivity analyses, batch and laboratory transfer, and an error analysis, including the conditions under which the sequential rule does not help.
4. **Open, reproducible code** that regenerates every number, table and figure in this paper from the public raw data.

We stress what the paper does *not* claim: it does not propose a more accurate lifetime predictor, and its guarantees are statements about error *rates* over the population of cells exchangeable with the calibration cells, not about any individual cell.

## 2 Methods

### 2.1 Cells and cycling data

**MATR/CLO.** The 124 LiFePO~4~/graphite cells (A123 APR18650M1A, 1.1 Ah) of Severson et al. [1], cycled under 72 fast-charging policies with 4C discharge, and the 45 cells of the closed-loop-optimisation validation batch of Attia et al. [2], downloaded from data.matr.io. We applied the authors' cleaning steps and verified each against the data: five batch-1 cells that never reached EOL were removed; five batch-1 cells whose cycling continued in batch 2 were concatenated with their continuations (capacities match at the junction); six noisy batch-3 channels were removed. Cycle lives range from 148 to 2,237 cycles (median 761). **HUST.** The 77 cells of the same type tested by Ma et al. [8] with identical fast charging and 77 different multi-step discharge protocols, cycle lives 1,142–2,689 (median 1,875). The HUST files are Python pickles; they were read with an allow-listed unpickler that permits only numpy/pandas reconstruction functions. In both datasets the lifetime label is the cycle at which the discharge capacity first falls to 0.88 Ah (80% of the 1.1 Ah nominal capacity); we use the providers' labels. Because initial capacities and discharge protocols differ between the data sets (4C constant-current discharge for MATR/CLO, multi-step discharge for HUST), this fixed-capacity end point corresponds to different fractions of each cell's initial capacity and is not physically identical across the two data sets; the screening problem is therefore defined separately for each data set. The main specifications, $L^\ast=750$ (MATR/CLO) and $L^\ast=1900$ (HUST), are close to the median lifetimes, so that both classes are well represented; other values are studied in Section 3.6. Checkpoints are $\{20,30,\dots,100,120,140,160,180,200,250,300\}$ (MATR/CLO, $M=16$) and $\{20,30,\dots,100,150,200,300,400,500,600,800,1000\}$ (HUST, $M=17$). The data sets and the screening set-up are summarised in Table 1.

| Data set | Source | Cells | Protocols | Min. life | Median life | Max. life | $L^\ast$ | Bad share | Checkpoints | Split (%) |
|---|---|---|---|---|---|---|---|---|---|---|
| MATR | Severson et al. 2019 | 124 | 69 | 148 | 736 | 2,237 | 750 | 50.8 | 16 (20-300 cycles) | 50/25/25 |
| CLO | Attia et al. 2020 | 45 | 9 | 443 | 774 | 1,166 | 750 | 40.0 | 16 (20-300 cycles) | 50/25/25 |
| HUST | Ma et al. 2022 | 77 | 77 | 1,142 | 1875 | 2,689 | 1,900 | 51.9 | 17 (20-1000 cycles) | 40/30/30 |

: **Table 1.** Data sets and screening set-up. All cells are LiFePO~4~/graphite A123 APR18650M1A cells (1.1 Ah). Bad share: fraction of cells with cycle life below $L^\ast$. Split: training/calibration/test percentages per random split.


### 2.2 Screening problem

Let cell $i$ have cycle life $T_i$ (number of cycles until the discharge capacity first reaches 80% of nominal) and let $L^\ast$ be the specification. The cell is *good* if $T_i \ge L^\ast$ ($Z_i=1$) and *bad* otherwise ($Z_i=0$). Measurements become available cycle by cycle. At checkpoints $k_1<\dots<k_M<L^\ast$ a cell that is still alive ($T_i>k_m$) yields a feature vector $X_i^{(m)}$ computed only from cycles $1,\dots,k_m$. A screening rule decides at each checkpoint to *pass* the cell (stop cycling, declare it good), *reject* it (stop, declare it bad) or *continue*. A cell that fails before a checkpoint is rejected by observation, and a cell still undecided after $k_M$ is cycled until $\min(T_i,L^\ast)$, which reveals its class without error. The targets are

$$ \mathrm{P}(\text{rule passes cell } i \mid Z_i=0)\le\alpha,\qquad \mathrm{P}(\text{rule rejects cell } i \mid Z_i=1)\le\beta, $$

EQNUMMARK(1)


with as few cycles as possible spent before a decision. The decision unit is the individual cell. This matches situations in which cells of the same type are cycled side by side and each test can be stopped separately — pruning a test matrix of charging protocols or operating conditions, or grading cells for a downstream use — but not lot-level qualification, where a decision about a whole production lot is required and which calls for different statistics.

### 2.3 Early-cycle features, base predictors and normalised scores

For each checkpoint a base predictor $h_m$ is trained on a training set of cells alive at $k_m$. In the main experiments $h_m$ is an elastic net [60] regressing $\log_{10}T$ on the checkpoint features, with penalty and mixing parameter selected by five-fold cross-validation inside the training set. The *normalised score* of cell $i$ at checkpoint $m$ is

$$ S_i^{(m)}=\frac{h_m\!\left(X_i^{(m)}\right)-\log_{10}L^\ast}{s_m}, $$

EQNUMMARK(2)


where $s_m$ is the out-of-fold root-mean-square error of $h_m$ on the training cells (taken from the same cross-validation, so no additional fits are needed). Because $s_m$ is the minimum cross-validated error over the penalty grid, it is slightly optimistic: in the main experiment the root-mean-square error on test cells exceeded $s_m$ by 2–26% depending on the checkpoint. The conformal rules below calibrate on the scores themselves and do not rely on $s_m$ being an accurate error estimate; the Gaussian comparator does. Large positive $S$ is evidence that the cell is good. Normalisation puts checkpoints with very different prediction accuracy on a common scale. Other base predictors are used in Section 3.4: L2-regularised logistic regression on $Z$ (score = logit; trained only on $Z$, i.e. on cells cycled to $\min(T,L^\ast)$), gradient-boosted trees and random forests [61] (scale = out-of-fold RMSE), a Gaussian process with automatic relevance determination [62] (scale = posterior standard deviation of each cell), and a one-dimensional convolutional network on the capacity-difference curve plus the scalar features (scale = RMSE on a 20% validation part of the training cells).

**Features.** For the MATR/CLO cells we generalise the features of Severson et al. [1] from cycle 100 to checkpoint $k$: the logarithms of the absolute minimum, variance, skewness and kurtosis of $\Delta Q_{k-10}(V)=Q_k(V)-Q_{10}(V)$; the discharge capacity at cycle 2; the maximum capacity minus that at cycle 2; slope and intercept of a linear fit to capacity over cycles $2,\dots,k$ and slope over the last 10 cycles; the capacity change between cycles 10 and $k$; the mean charge time of cycles 2–6; and the mean of the per-cycle maximum temperature. Internal-resistance features were not used because the CLO cells have no resistance records. During data auditing we found that some cycles are non-standard (rest or diagnostic steps), producing single-cycle glitches in $Q(V)$; $Q_k(V)$ and $Q_{10}(V)$ are therefore element-wise medians over cycles $k-4,\dots,k$ and $8,\dots,12$, which uses no cycle after $k$. The HUST cells were discharged with multi-step protocols, so $Q(V)$ is not single-valued; we use the analogous statistics of $\Delta V_{k-10}(q)=V_k(q)-V_{10}(q)$ on a grid of discharged capacity $q\in[0.02,0.85]$ Ah together with the same capacity-trajectory features. A unit test verifies that features at checkpoint $k$ are unchanged when all data after cycle $k$ are altered.

### 2.4 Trajectory calibration

A separate set of calibration cells, disjoint from the training cells, is scored with the trained $h_m$. Let $\mathcal B$ ($n_0$ cells) and $\mathcal G$ ($n_1$ cells) be the bad and good calibration cells. For every calibration cell define the trajectory statistics

$$ P_i=\max_{m:\,T_i>k_m} S_i^{(m)}\quad(i\in\mathcal B),\qquad R_i=\max_{m} \left(-S_i^{(m)}\right)\quad(i\in\mathcal G), $$

EQNUMMARK(3)


(with $P_i=-\infty$ if a bad cell fails before $k_1$). The thresholds are the order statistics

$$ \hat\lambda=P_{(r_0)},\qquad \hat\mu=R_{(r_1)}, $$

EQNUMMARK(4)


where $P_{(r)}$ is the $r$-th smallest value, $r_0$ is the smallest integer not less than $(n_0+1)(1-\alpha)$, $r_1$ is the smallest integer not less than $(n_1+1)(1-\beta)$, and an index larger than the sample size gives $+\infty$ (the rule then never passes, or never rejects). At checkpoint $m$ a cell still alive is passed if $S^{(m)}>\hat\lambda$, rejected if $S^{(m)}<-\hat\mu$ and otherwise kept on test.

**Proposition 1.** *Let the training cells be fixed, and suppose that the bad calibration cells and a new bad cell are exchangeable, and likewise the good calibration cells and a new good cell. Then for the new cell*
$$\mathrm{P}(\text{passed at some checkpoint}\mid Z=0)\le\alpha,\qquad \mathrm{P}(\text{rejected by the model at some checkpoint}\mid Z=1)\le\beta,$$
*for every rule that passes only when $S^{(m)}>\hat\lambda$ and rejects only when $S^{(m)}<-\hat\mu$, whatever its stopping time — in particular, whatever order the two checks are applied in, and whether or not an operator stops a test early without a decision.*

The proof (Supporting Information, Section S5) is short: a bad cell can be passed only if its trajectory maximum $P$ exceeds $\hat\lambda$, and by exchangeability the rank of $P$ among the calibration maxima is uniform, so this happens with probability at most $\alpha$ whatever the stopping time.

**Remarks.** (i) *Truncated calibration.* $P_i$, $R_i$ and $Z_i$ require only cycles up to $\min(T_i,L^\ast)$ because $k_M<L^\ast$; calibration cells never need to be cycled to EOL. This follows from calibrating on the class $Z$ rather than on the lifetime and is the deterministic (administrative) special case of the censoring device of conformalised survival analysis [42], with the cut-off at $L^\ast$; no censoring weights are needed. It is shared by any class-conditional conformal rule, including the single-checkpoint rule below. The regression base predictor is still trained on cells with known lifetimes; if the base predictor is a classifier of $Z$, training cells also need only $\min(T_i,L^\ast)$ cycles. (ii) *Why the maximum.* Calibrating each checkpoint separately at level $\alpha$ ("naive sequential") controls each look but not the first crossing, whose error can approach $M\alpha$; Bonferroni calibration at $\alpha/M$ restores validity but, with tens of calibration cells, gives $\hat\lambda=+\infty$ whenever $(n_0+1)(1-\alpha/M)>n_0$, i.e. whenever $n_0<M/\alpha-1$ (fewer than 159 bad calibration cells for $M=16$ and $\alpha=0.1$). The maximum statistic accounts for the dependence between looks exactly; it is the conformal counterpart of the max-type scores used for simultaneous validity over trajectories [57,58] and of the boundaries of group-sequential designs [49]. (iii) *Scope.* The guarantee is marginal over calibration and test cells and conditional on the class; realised error rates in any one batch of test cells fluctuate around it, and it says nothing about cells that are not exchangeable with the calibration cells (Section 3.7). Passing is possible only if $(n_0+1)(1-\alpha)\le n_0$, i.e. $n_0\ge(1-\alpha)/\alpha$ (at least 9 bad calibration cells for $\alpha=0.1$, 19 for $\alpha=0.05$). Because the guarantee averages over calibration sets, the error probability *conditional on a particular calibration set* exceeds $\alpha$ with appreciable probability (Table S15); realised error rates in individual splits are reported alongside the means. (iv) *Training-conditional (PAC) variant.* Replacing $r_0$ by the smallest $r$ with $F_{\mathrm{Beta}}(1-\alpha;\,r,\,n_0+1-r)\le\delta$ (and likewise $r_1$) gives thresholds for which the conditional false-pass probability exceeds $\alpha$ with probability at most $\delta$ over the draw of calibration cells [21,23]. This requires i.i.d. calibration cells and continuous scores, and a finite rank exists only for $n_0\ge22$ at $\alpha=\delta=0.10$. We use $\delta=0.10$.

### 2.5 Comparison rules

All rules use the same base predictor, splits and cells. *Naive sequential*: per-checkpoint thresholds from the bad (good) calibration cells alive at that checkpoint at level $\alpha$ ($\beta$). *Bonferroni*: the same at $\alpha/M$ and $\beta/M$. *Single checkpoint*: class-conditional thresholds at cycle 100 only (valid, Proposition 1 with $M=1$); in Section 3.5 the single checkpoint is also chosen per split from the training cells only, which keeps the guarantee. *Point prediction at cycle 100*: pass if the predicted lifetime is at least $L^\ast$, otherwise reject [1] (no error control). *Gaussian threshold at every look*: pass if $S^{(m)}>z_{1-\alpha}$ and reject if $S^{(m)}<-z_{1-\beta}$ at every checkpoint, i.e. a Gaussian predictive-bound rule without correction for repeated looks; for the Gaussian process it is the Bayesian rule "posterior probability of being good above $1-\alpha$ / below $\beta$". A multiplicity-corrected version uses $z_{1-\alpha/M}$ and $z_{1-\beta/M}$ (Section 3.6). *Lifetime interval*: trajectory-valid split-conformal lower and upper bounds on $\log_{10}T$ from normalised residuals [22], pass if the lower bound is at least $\log_{10}L^\ast$ and reject if the upper bound is below it; this rule needs calibration cells cycled to EOL and controls the miscoverage of the lifetime bound over all cells rather than the class-conditional error, so it spends far less than the nominal error budget and serves as a reference for lifetime-interval practice rather than as a like-for-like competitor. *Proposed without normalisation*: Equations (3)–(4) applied to $h_m-\log_{10}L^\ast$.

### 2.6 Experimental protocol and statistics

The cell is the unit of analysis. In each random split, training cells are drawn within strata defined by dataset and class (50% of MATR/CLO cells, 40% of HUST cells), and the remaining cells are divided uniformly at random into calibration and test cells (MATR/CLO 25%/25%, HUST 30%/30%). Drawing calibration and test cells from the same pool makes them exchangeable, as Proposition 1 requires (an earlier version that stratified the calibration and test sets separately produced slightly different group mixtures in the two sets and an error rate marginally above the theoretical value; it was discarded). Every experiment uses split seeds fixed before running; the main experiment (E1) uses 1,000 splits per dataset, the other experiments 200 splits per configuration (CNN: 30), with designs listed in Table S1: E2 base predictors; E3 checkpoint grids; E4 calibration and training set size and feature noise; E5 batch shift (model and calibration from MATR batches 1–2, test on batch 3 or CLO, with or without recalibration on target cells) and laboratory transfer (MATR/CLO model, HUST calibration); E6 computation; E7 error levels and specification; E9 protocol-disjoint splits; E10 PAC calibration; E11 physical interpretation of early decisions; E12 checkpoint grid chosen on training cells; E13 multiplicity-corrected Gaussian rule, Bonferroni on sparse grids and persistent per-cell noise. E9–E13 were added after the design was fixed (E12 and E13 in response to internal review) and are reported as such. Metrics are the false-pass rate among bad test cells (FPR), the false-reject rate among good test cells (FRR), accuracy, the share of cells decided by the model before $\min(T,L^\ast)$, the mean number of cycles to a decision, and the fraction of cycling time saved relative to cycling every test cell to $\min(T,L^\ast)$. Validity is assessed by the mean FPR and FRR over splits with normal-approximation 95% confidence intervals and the share of splits in which the realised FPR, the realised FRR, or either, exceeded the nominal level. Because the splits re-use the same finite set of cells, the split-level confidence intervals describe Monte-Carlo error and understate the variation across independent cell populations. For efficiency comparisons each cell's time to decision is averaged over the splits in which it was a test cell; methods are compared on these per-cell averages with paired Wilcoxon signed-rank tests [63], Holm correction over comparators [64], matched-pairs rank-biserial correlation as effect size, and a bootstrap [65] (10,000 resamples) 95% CI for the difference in time saved, resampling cells on HUST (each cell has its own discharge protocol) and charging-protocol groups on MATR/CLO, whose cells share protocols. The experimental design, including all methods, metrics and tests, was fixed after a 100-split pilot (disjoint seeds) used only to detect data defects and estimate run time. Computations ran on four CPU cores with Python 3.13.18, scikit-learn 1.9.1 and PyTorch 2.15.0.


## 3 Results and Discussion

### 3.1 Data and base predictors

![**Figure 1.** Cycle-life distributions of the two data sets and the specifications used in the main experiments. MATR/CLO: 124 cells of Severson et al. and 45 cells of the CLO validation batch of Attia et al.; HUST: 77 cells of Ma et al. Dashed lines: $L^\ast$ = 750 and 1,900 cycles; 48% and 52% of the cells, respectively, are bad.](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig2_lifetime_distributions.png){width=6.3in}

The specifications split both data sets roughly in half (Figure 1). The accuracy of the elastic-net predictor improved steadily with the number of observed cycles (Figure 2): on the test cells of all MATR/CLO splits, the mean absolute percentage error of the predicted cycle life fell from 28.6% at 20 cycles to 11.2% at 100 cycles and 7.1% at 300 cycles; on HUST it was 15.2%, 14.0% and 7.4% at 20, 100 and 1000 cycles. The error at 100 cycles on MATR/CLO is close to the 9.1% reported by Severson et al. for their full model on a fixed split [1], although our pooled data, random splits and feature set (no resistance features) differ from theirs. The score scale $s_k$ tracks the decrease of prediction error, which is what normalisation (Equation 2) exploits.

![**Figure 2.** Accuracy of the per-checkpoint elastic-net predictor on test cells, pooled over all splits of experiment E1: mean absolute percentage error (MAPE) of the predicted cycle life and the score scale $s_k$ (expressed as a percentage error, $10^{s_k}-1$).](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig3_base_model_accuracy.png){width=6.3in}

### 3.2 Validity of the screening decisions

![**Figure 3.** Validity (top) and efficiency (bottom) of the screening rules in experiment E1 (1,000 random splits per data set, elastic net, $\alpha=\beta=0.10$). Top: mean false-pass rate among bad test cells and false-reject rate among good test cells with 95% confidence intervals; the dashed line marks the nominal level. Bottom: cycling time saved relative to cycling every test cell to $\min(T,L^\ast)$; rules whose error rate exceeds the nominal level are labelled.](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig4_validity_and_efficiency.png){width=6.3in}

| Data set | Rule | FPR | FPR upper | FRR | FRR upper | Accuracy | Early | Saved | Cycles to decision |
|---|---|---|---|---|---|---|---|---|---|
| HUST | Bonferroni sequential conformal | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.0 | 0.0 | 1737 |
| HUST | Parametric/Bayesian threshold | 0.081 | 0.087 | 0.136 | 0.143 | 0.893 | 79.0 | 69.0 | 540 |
| HUST | Conformal lifetime interval (full-lifetime calibration) | 0.007 | 0.009 | 0.011 | 0.013 | 0.991 | 27.8 | 19.5 | 1398 |
| HUST | Naive sequential conformal | 0.286 | 0.295 | 0.214 | 0.223 | 0.750 | 97.5 | 93.2 | 119 |
| HUST | Point prediction at cycle 100 | 0.237 | 0.246 | 0.367 | 0.377 | 0.701 | 100.0 | 94.2 | 100 |
| HUST | Proposed (trajectory-calibrated) | 0.068 | 0.074 | 0.074 | 0.080 | 0.929 | 60.5 | 50.7 | 857 |
| HUST | Single checkpoint (cycle 100) conformal | 0.071 | 0.077 | 0.079 | 0.086 | 0.925 | 41.5 | 38.3 | 1073 |
| HUST | Proposed without score normalisation | 0.067 | 0.073 | 0.074 | 0.081 | 0.929 | 53.4 | 47.6 | 910 |
| MATR+CLO | Bonferroni sequential conformal | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.0 | 0.0 | 653 |
| MATR+CLO | Parametric/Bayesian threshold | 0.046 | 0.049 | 0.043 | 0.045 | 0.956 | 86.7 | 77.5 | 147 |
| MATR+CLO | Conformal lifetime interval (full-lifetime calibration) | 0.017 | 0.018 | 0.010 | 0.011 | 0.987 | 66.4 | 54.4 | 298 |
| MATR+CLO | Naive sequential conformal | 0.145 | 0.151 | 0.158 | 0.164 | 0.850 | 99.8 | 95.4 | 30 |
| MATR+CLO | Point prediction at cycle 100 | 0.079 | 0.083 | 0.073 | 0.076 | 0.924 | 100.0 | 84.7 | 100 |
| MATR+CLO | Proposed (trajectory-calibrated) | 0.068 | 0.073 | 0.080 | 0.085 | 0.927 | 86.7 | 78.3 | 142 |
| MATR+CLO | Single checkpoint (cycle 100) conformal | 0.082 | 0.087 | 0.060 | 0.064 | 0.930 | 94.8 | 79.6 | 133 |
| MATR+CLO | Proposed without score normalisation | 0.068 | 0.073 | 0.082 | 0.087 | 0.925 | 75.2 | 68.9 | 203 |

: **Table 2.** Screening results of experiment E1 (elastic net, 1,000 random splits per data set, $\alpha=\beta=0.10$). FPR: false-pass rate among bad test cells; FRR: false-reject rate among good test cells; "upper" = upper limit of the 95% confidence interval of the mean over splits; early: share of test cells decided by the model before $\min(T,L^\ast)$; saved: fraction of cycling time saved relative to cycling every test cell to $\min(T,L^\ast)$.


The trajectory-calibrated rule met both error targets on both data sets (Figure 3, Table 2). On MATR/CLO its mean false-pass rate was 0.068 (95% CI 0.063–0.073) and its false-reject rate 0.080 (0.076–0.085); on HUST they were 0.068 (0.062–0.074) and 0.074 (0.067–0.080). With the realised calibration-set sizes, the rank rule attains an exact level of 0.081 (false pass) and 0.084 (false reject) on MATR/CLO and 0.076 and 0.078 on HUST rather than 0.10, because the order statistic moves in steps of $1/(n_0+1)$; for continuous scores the bound of Proposition 1 is otherwise tight, so the maximum over checkpoints is not conservative. The realised rates fall slightly below these levels because some bad cells are rejected (and some good cells passed) before their trajectory maximum would have crossed the opposite threshold. As the theory predicts, the bound holds on average rather than in every split: the realised false-pass rate exceeded 0.10 in 26% (MATR/CLO) and 21% (HUST) of the splits, with about 20.0 and 11.9 bad cells, respectively, in the test sets' companion calibration sets. The single-checkpoint conformal rule and the proposed rule without normalisation were also valid, as Proposition 1 (with $M=1$, respectively without normalisation) implies. The lifetime-interval rule had even lower class-conditional error rates, but this is an empirical finding: its marginal coverage guarantee bounds only the joint probability of a wrong decision, not the error rate within each class.

The rules without a valid calibration behaved very differently. Using individually valid per-checkpoint thresholds sequentially (naive sequential) inflated the false-pass rate to 0.145 on MATR/CLO and 0.286 on HUST, and the false-reject rate to 0.158 and 0.214 — up to 2.9 times the nominal level. The Severson-style point rule at cycle 100 happened to stay below 0.10 on MATR/CLO (0.079 and 0.073) but not on HUST (0.237 and 0.367). The parametric rule with Gaussian thresholds on the same normalised scores was conservative on MATR/CLO (0.046, 0.043) and violated the false-reject target on HUST (0.136, upper confidence limit 0.143). Bonferroni calibration never passed or rejected a cell, because with about 20.0 bad and 22.0 good calibration cells the required order statistic at level $\alpha/M$ does not exist.

### 3.3 Testing time saved

![**Figure 4.** Share of test cells decided as a function of the number of cycles completed (all splits of E1). The proposed rule decides most cells within the first few checkpoints and sends the remainder to observation; the single-checkpoint rule decides at cycle 100; the naive sequential rule decides almost every cell early but violates the error targets; the dashed line is full observation to $\min(T,L^\ast)$.](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig5_decision_time.png){width=6.3in}

On MATR/CLO the proposed rule decided 86.7% of the test cells from their early cycles and saved 78.3% of the cycling needed to observe every cell to $\min(T,L^\ast)$ (mean 142 cycles per cell instead of 653); half of the cells were decided within 40 cycles and 78% by cycle 100 (Figure 4). On HUST, whose cells live longer and where the specification is 1,900 cycles, it decided 60.5% of the cells early and saved 50.7% (mean 857 instead of 1,739 cycles).

| Data set | Comparator | Cells | Proposed (cycles) | Comparator (cycles) | Saved diff. | CI low | CI high | p (Holm) | r |
|---|---|---|---|---|---|---|---|---|---|
| MATR+CLO | Bonferroni sequential conformal | 169 | 142 | 653 | 78.3 | 74.7 | 81.9 | 1.2e-13 | -1.00 |
| MATR+CLO | Parametric/Bayesian threshold | 169 | 142 | 147 | 0.8 | -2.1 | 4.4 | 0.14 | 0.24 |
| MATR+CLO | Conformal lifetime interval (full-lifetime calibration) | 169 | 142 | 298 | 24.0 | 19.3 | 28.7 | 2.5e-13 | -0.98 |
| MATR+CLO | Naive sequential conformal | 169 | 142 | 30 | -17.1 | -20.5 | -13.7 | 1.2e-13 | 1.00 |
| MATR+CLO | Point prediction at cycle 100 | 169 | 142 | 100 | -6.4 | -10.2 | -2.4 | 0.51 | -0.09 |
| MATR+CLO | Single checkpoint (cycle 100) conformal | 169 | 142 | 133 | -1.3 | -3.9 | 1.5 | 0.01 | -0.38 |
| MATR+CLO | Proposed without score normalisation | 169 | 142 | 204 | 9.5 | 7.7 | 11.4 | 1.4e-13 | -0.99 |
| HUST | Bonferroni sequential conformal | 77 | 854 | 1739 | 50.9 | 45.8 | 56.0 | 1.7e-13 | -1.00 |
| HUST | Parametric/Bayesian threshold | 77 | 854 | 536 | -18.3 | -20.2 | -16.4 | 1.7e-13 | 1.00 |
| HUST | Conformal lifetime interval (full-lifetime calibration) | 77 | 854 | 1396 | 31.2 | 28.8 | 33.6 | 1.7e-13 | -1.00 |
| HUST | Naive sequential conformal | 77 | 854 | 118 | -42.3 | -46.9 | -37.7 | 1.7e-13 | 1.00 |
| HUST | Point prediction at cycle 100 | 77 | 854 | 100 | -43.3 | -48.6 | -38.0 | 1.7e-13 | 1.00 |
| HUST | Single checkpoint (cycle 100) conformal | 77 | 854 | 1070 | 12.4 | 9.2 | 15.7 | 1.2e-08 | -0.76 |
| HUST | Proposed without score normalisation | 77 | 854 | 906 | 3.0 | 1.5 | 4.5 | 0.00099 | -0.43 |

: **Table 3.** Cell-level paired comparison of the time to decision of the proposed rule with each comparator (E1). Each cell's time to decision is averaged over the splits in which it was a test cell. "Saved diff." = time saved by the proposed rule minus that of the comparator (percentage points; positive favours the proposed rule) with a cell-bootstrap 95% CI; Wilcoxon signed-rank test with Holm correction; $r$ = matched-pairs rank-biserial correlation of the time difference (negative = proposed rule faster).


Among the valid rules, the proposed rule saved more cycling than the lifetime-interval rule on both data sets (by 24.0 and 31.2 percentage points; Holm-adjusted $p$ = 2.5 × 10^-13^ and 1.7 × 10^-13^; Table 3), and more than the unnormalised variant (by 9.5 and 3.0 points). Against the single-checkpoint rule the result depended on the data set: on HUST the proposed rule saved 12.4 points more (95% CI 9.2 to 15.7; $p$ = 1.2 × 10^-8^; $r$ = -0.76), whereas on MATR/CLO the difference was -1.3 points (95% CI -3.9 to 1.5; $p$ = 0.01), i.e. not significant. The rules that saved more time than the proposed one — naive sequential, point prediction and, on HUST, the parametric rule — did so by violating at least one error target on at least one data set.

**Truncated calibration.** Because the proposed thresholds need only each calibration cell's class, the calibration campaign ended after at most $L^\ast$ cycles: a mean of 750 wall-clock cycles per split on MATR/CLO versus 1,958 for the full-lifetime calibration of the interval rule (factor 2.61), and 1,900 versus 2,630 on HUST (factor 1.38). Total calibration cell-cycles fell by factors of 1.22 and 1.09.

### 3.4 Other base predictors

| Data set | Model | Rule | FPR | FRR | Early | Saved | Splits |
|---|---|---|---|---|---|---|---|
| HUST | cnn | gauss | 0.183 | 0.250 | 97.2 | 88.8 | 30 |
| HUST | cnn | naive | 0.293 | 0.253 | 98.8 | 93.8 | 30 |
| HUST | cnn | proposed | 0.070 | 0.113 | 66.7 | 54.6 | 30 |
| HUST | cnn | single_k100 | 0.065 | 0.128 | 38.1 | 34.7 | 30 |
| HUST | en | gauss | 0.081 | 0.136 | 79.0 | 69.0 | 1,000 |
| HUST | en | naive | 0.286 | 0.214 | 97.5 | 93.2 | 1,000 |
| HUST | en | proposed | 0.068 | 0.074 | 60.5 | 50.7 | 1,000 |
| HUST | en | single_k100 | 0.071 | 0.079 | 41.5 | 38.3 | 1,000 |
| HUST | gbr | gauss | 0.074 | 0.114 | 79.6 | 62.1 | 200 |
| HUST | gbr | naive | 0.273 | 0.260 | 97.5 | 92.0 | 200 |
| HUST | gbr | proposed | 0.079 | 0.070 | 70.9 | 51.8 | 200 |
| HUST | gbr | single_k100 | 0.080 | 0.093 | 39.2 | 36.0 | 200 |
| HUST | gp | gauss | 0.274 | 0.362 | 99.2 | 93.5 | 200 |
| HUST | gp | naive | 0.343 | 0.310 | 98.4 | 93.0 | 200 |
| HUST | gp | proposed | 0.073 | 0.079 | 51.8 | 40.7 | 200 |
| HUST | gp | single_k100 | 0.081 | 0.077 | 34.0 | 31.5 | 200 |
| HUST | logit | naive | 0.304 | 0.220 | 96.6 | 92.3 | 1,000 |
| HUST | logit | proposed | 0.077 | 0.076 | 46.5 | 40.0 | 1,000 |
| HUST | logit | single_k100 | 0.077 | 0.075 | 35.3 | 32.7 | 1,000 |
| HUST | rf | gauss | 0.021 | 0.034 | 64.8 | 38.3 | 200 |
| HUST | rf | naive | 0.240 | 0.229 | 96.7 | 88.2 | 200 |
| HUST | rf | proposed | 0.064 | 0.071 | 75.1 | 52.0 | 200 |
| HUST | rf | single_k100 | 0.087 | 0.082 | 43.9 | 40.3 | 200 |
| MATR+CLO | cnn | gauss | 0.086 | 0.081 | 96.3 | 88.7 | 30 |
| MATR+CLO | cnn | naive | 0.149 | 0.165 | 100.0 | 95.8 | 30 |
| MATR+CLO | cnn | proposed | 0.070 | 0.087 | 88.7 | 80.0 | 30 |
| MATR+CLO | cnn | single_k100 | 0.096 | 0.056 | 89.4 | 74.4 | 30 |
| MATR+CLO | en | gauss | 0.046 | 0.043 | 86.7 | 77.5 | 1,000 |
| MATR+CLO | en | naive | 0.145 | 0.158 | 99.8 | 95.4 | 1,000 |
| MATR+CLO | en | proposed | 0.068 | 0.080 | 86.7 | 78.3 | 1,000 |
| MATR+CLO | en | single_k100 | 0.082 | 0.060 | 94.8 | 79.6 | 1,000 |
| MATR+CLO | gbr | gauss | 0.041 | 0.052 | 83.8 | 74.8 | 200 |
| MATR+CLO | gbr | naive | 0.145 | 0.156 | 99.8 | 95.7 | 200 |
| MATR+CLO | gbr | proposed | 0.071 | 0.076 | 88.0 | 80.3 | 200 |
| MATR+CLO | gbr | single_k100 | 0.078 | 0.072 | 90.1 | 75.1 | 200 |
| MATR+CLO | gp | gauss | 0.085 | 0.104 | 96.9 | 90.9 | 200 |
| MATR+CLO | gp | naive | 0.145 | 0.162 | 100.0 | 95.8 | 200 |
| MATR+CLO | gp | proposed | 0.075 | 0.073 | 87.4 | 79.8 | 200 |
| MATR+CLO | gp | single_k100 | 0.084 | 0.060 | 93.4 | 78.3 | 200 |
| MATR+CLO | logit | naive | 0.145 | 0.162 | 99.8 | 95.3 | 1,000 |
| MATR+CLO | logit | proposed | 0.069 | 0.072 | 79.3 | 67.5 | 1,000 |
| MATR+CLO | logit | single_k100 | 0.088 | 0.063 | 88.0 | 73.1 | 1,000 |
| MATR+CLO | rf | gauss | 0.021 | 0.042 | 74.4 | 64.3 | 200 |
| MATR+CLO | rf | naive | 0.149 | 0.174 | 99.6 | 95.4 | 200 |
| MATR+CLO | rf | proposed | 0.066 | 0.089 | 88.2 | 80.5 | 200 |
| MATR+CLO | rf | single_k100 | 0.078 | 0.071 | 89.6 | 74.9 | 200 |

: **Table 4.** Validity and efficiency of the screening rules with different base predictors (E2; elastic net from E1). FPR: false-pass rate among bad test cells; FRR: false-reject rate among good test cells; saved: fraction of cycling saved relative to observing every test cell to $\min(T,L^\ast)$. For the Gaussian process the parametric rule is the Bayesian posterior-probability rule. Number of splits: 1,000 (elastic net, logistic), 200 (GBR, RF, GP) and 30 (CNN).


The guarantee of Proposition 1 does not depend on the base predictor, and the experiments agree (Table 4). With logistic regression, gradient-boosted trees, random forests, a Gaussian process and a convolutional network, the proposed rule kept both mean error rates at or below the nominal 0.10 in every case except the CNN on HUST, whose false-reject rate of 0.113 (upper 95% limit 0.166) rests on only 30 splits and is compatible with the target within Monte-Carlo error. The naive sequential rule exceeded the targets with every model. The choice of model mattered for efficiency, not for validity: on MATR/CLO the trajectory rule saved 80.3% (GBR), 80.5% (RF), 79.8% (GP) and 80.0% (CNN) of the cycling, more than the single-checkpoint rule with the same model (75.1%, 74.9%, 78.3% and 74.4%), so on MATR/CLO a fixed checkpoint at cycle 100 was as efficient as the sequential rule only with the elastic net and more efficient only with logistic regression (73.1% against 67.5%). On HUST the trajectory rule saved more than the single-checkpoint rule with every model.

Model-based uncertainty did not provide control either. The Bayesian rule of the Gaussian process, which passes a cell when its posterior probability of reaching $L^\ast$ exceeds $1-\alpha$, had false-pass and false-reject rates of 0.274 and 0.362 on HUST and a false-reject rate of 0.104 on MATR/CLO: the posterior was over-confident for cells unlike the training cells. Logistic regression, trained only on the class of each cell and therefore on training cells cycled to $\min(T,L^\ast)$ rather than to end of life, gave valid decisions but saved less cycling (67.5% on MATR/CLO and 40.0% on HUST) than the elastic net trained on full lifetimes (78.3% and 50.7%). A laboratory that has no full-lifetime history can therefore start screening with a truncated training campaign, at the cost of less efficient decisions.

### 3.5 How many checkpoints?

![**Figure 5.** Checkpoint-grid ablation (E3, 200 splits per data set, elastic net). Cycling saved by the trajectory-calibrated rule for different checkpoint grids, together with the false-pass and false-reject rates; the naive sequential rule is shown for reference. With a single checkpoint all rules coincide.](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig7_ablation_checkpoint_grid.png){width=6.3in}

The number of looks trades flexibility against conservativeness (Figure 5; Table S6). Every grid kept both error rates of the trajectory rule below 0.10, whereas the naive sequential rule became more invalid as looks were added: on HUST its false-pass rate rose from 0.085 with one checkpoint to 0.133 with two, 0.175 with four and 0.289 with all 17. For efficiency, the dense grids of the main experiment were not optimal. On MATR/CLO a sparse grid of cycles 50, 100, 200 and 300 saved 84.3% of the cycling, against 79.4% with all 16 checkpoints and 81.9% with the best single checkpoint (cycle 50). On HUST the sparse grid (cycles 100, 300, 600, 1000) saved 56.8% against 52.6% with all 17 checkpoints, but a single checkpoint at cycle 300 saved more (61.5%). Bonferroni calibration, which never decided with the dense grids, decided only with two checkpoints on MATR/CLO (cycles 100 and 300; no pass in 24% of the splits, 63.2% saved against 78.8% for the trajectory rule on the same grid) and never with four checkpoints or on HUST (E13): splitting $\alpha$ over the looks requires calibration sets several times larger than the maximum statistic does. Each additional checkpoint raises the calibrated thresholds, because the maximum of more scores is larger; checkpoints that add little information therefore cost efficiency. The best single checkpoint, however, differed between the data sets (cycle 50 for MATR/CLO, cycle 300 for HUST; cycle 100 was a poor choice for HUST, 40.6%), and it cannot be chosen on the calibration cells without voiding the guarantee. It can, however, be chosen on the training cells, which leaves calibration and test cells exchangeable. A sparse grid of three to five checkpoints spread over the period in which the early-cycle features become informative (Section 3.9) was the most robust choice across both data sets; we report the dense grids in the main experiment because they were fixed before the experiments were run.

**Choosing the grid on training cells (E12).** To compare the rules fairly, we chose the grid in every split from the candidates of E3 using the training cells only: out-of-fold scores of the training cells (five-fold cross-fitting) were used to calibrate each candidate grid and to measure its cycling saving on the same cells and evaluated the choice on the untouched calibration and test cells (same splits as E3). Restricted to multi-checkpoint grids, the selection picked the sparse grid most often (sparse 50 100 200 300 in 64% of the MATR/CLO splits, sparse 100 300 600 1000 in 52% on HUST) and saved 80.6% and 53.5% of the cycling with error rates of 0.064/0.074 and 0.076/0.076. Restricted to single checkpoints, it picked cycle 50 on MATR/CLO and cycle 300 on HUST in most splits and saved 80.6% and 55.7%. The paired difference between the two was 0.1 percentage points on MATR/CLO (95% CI -1.6 to 1.6) and -2.2 points on HUST (-5.1 to 0.7). **A single checkpoint chosen on training cells was therefore as efficient as the sequential rule on both data sets**; the advantage of the sequential rule over the single-checkpoint rule in Section 3.3 (12.1 points on HUST) is an advantage over a checkpoint fixed at cycle 100, and a training-selected checkpoint removes it (15.1 points gained over cycle 100). The value of trajectory calibration is thus not higher efficiency than a well-chosen single look, but valid error control when a laboratory looks at its cells repeatedly — which naive practice does, with the error inflation shown above — and the freedom to stop at any checkpoint without fixing one in advance.

### 3.6 Robustness and sensitivity

![**Figure 6.** Robustness of the screening rules (E4, 200 splits per configuration, elastic net). Larger of the mean false-pass and false-reject rates as a function of the calibration-set fraction, the training-set fraction and Gaussian feature noise (in multiples of each feature's training standard deviation) added either to calibration and test cells alike or to test cells only. Dashed line: nominal level 0.10. Cycling saved is given in Table S7.](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig8_robustness.png){width=6.3in}

**Calibration and training set size.** The guarantee held for every calibration and training fraction tested (Figure 6; Table S7); what changed was efficiency. With only 10% of the MATR/CLO cells (about 8.3 bad and 8.7 good cells) used for calibration, the rule saved 41.1% of the cycling instead of 80.2% with 25%, because with fewer than nine cells of a class the required order statistic does not exist and the rule cannot pass (or reject) at all in some splits. On HUST, a calibration fraction of 20% (about 7.9 bad cells) reduced the saving to 19.7%. Smaller training sets lowered efficiency gradually (MATR/CLO 70.4% with 20% training cells versus 80.2% with 50%) without affecting validity. In practice, about 10–15 cells of each class are needed in the calibration set before the rule becomes efficient.

**Measurement noise.** When Gaussian noise was added to the features of calibration and test cells alike, the two remained exchangeable and the trajectory rule stayed valid at every noise level (false-pass rate 0.074 and false-reject rate 0.064 on MATR/CLO with noise of one standard deviation), while its saving fell from 78.8% to 36.0%: noisier scores lead to wider thresholds and later decisions. The parametric rule, whose thresholds do not adapt to the data, became invalid (0.248 and 0.305). Noise added to the test cells only — a model of screening cells on a noisier tester than the calibration cells — broke exchangeability, and from a quarter of a standard deviation upward every rule exceeded at least one target on MATR/CLO: the trajectory rule reached 0.126 and 0.163 at a quarter of a standard deviation and 0.240 and 0.345 at one standard deviation. The sequential rule was more sensitive to such a mismatch than the single-checkpoint rule, because every additional look gives the extra noise another chance to cross a threshold: on HUST, at a quarter of a standard deviation, the false-pass rate was 0.275 for the trajectory rule and 0.139 for the single-checkpoint rule. The same held when the test-only noise was a persistent per-cell offset, identical at every checkpoint, rather than an independent draw per checkpoint (E13): at a quarter of a standard deviation the trajectory rule reached 0.124 and 0.148 on MATR/CLO and 0.232 and 0.191 on HUST, against 0.105/0.086 and 0.140/0.139 for the single-checkpoint rule. Calibration cells must therefore be measured on the same equipment and protocol as the cells being screened, and the calibration should be repeated when the tester changes; Section 3.7 shows the same requirement, and the effect of recalibrating with a few target cells, for batch and laboratory shift.

**Specification and error levels (E7).** Moving $L^\ast$ changes the class balance (Figure S1; Table S10). On MATR/CLO the trajectory rule stayed valid for $L^\ast$ = 550, 750 and 900 cycles (cycling saved 77.5%, 79.4% and 69.7%). On HUST, with $L^\ast$ = 1,600 only about 5.6 calibration cells were bad, too few to pass any cell at $\alpha$ = 0.10 (no pass in 98% of the splits), and with $L^\ast$ = 2,200 only about 5.8 were good; the rule remained valid but saved only 15.5% and 20.0%. The uncorrected Gaussian rule violated one of the targets at both alternative specifications on HUST (false-pass rate 0.322 at 1,600; false-reject rate 0.298 at 2,200). Stricter error levels need more calibration cells: at $\alpha=\beta=0.05$ at least 19 cells per class are required, so the rule decided nothing early on HUST (about 12.0 cells per class) and saved 53.8% on MATR/CLO with error rates 0.034 and 0.025. At $\alpha=\beta=0.20$ it was valid on both data sets and saved 94.2% and 75.9%.

### 3.7 Batch shift, laboratory shift and unseen protocols

![**Figure 7.** Screening under distribution shift (E5, 200 splits per case, elastic net). Batch shift: models trained and calibrated on MATR batches b1 and b2 and applied to batch b3 or to the CLO batch b4, either with the source calibration cells or after recalibration with 20 or 30 cells of the target batch cycled to $L^\ast$ only. Laboratory shift: capacity-trajectory features only, MATR/CLO model or HUST model, calibrated on HUST cells and tested on other HUST cells ($L^\ast$ = 1,900). Points: mean error rates with 95% confidence intervals.](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig10_distribution_shift.png){width=6.3in}

The guarantee rests on exchangeability between calibration and screened cells, and the shift experiments show what happens without it (Figure 7; Table S8). The MATR batches differ strongly: with $L^\ast$ = 750 cycles, all 43 cells of b2 but only 3 of the 40 cells of b3 and 18 of the 45 CLO cells are bad, because the batches were cycled with different protocol sets. A model trained and calibrated on b1 and b2 and applied to b3 without recalibration rejected about half of the good b3 cells (false-reject rate 0.480); its false-pass rate of 0.128 rests on the 3.0 bad cells of b3 and is therefore imprecise. On the CLO batch b4 the false-reject rate was 0.597. The naive and Gaussian rules failed similarly, the single-checkpoint rule exchanged a low false-reject rate for a false-pass rate of 0.479 on b4, and the point-prediction rule happened to stay within the targets on b3 but passed 0.361 of the bad b4 cells — an uncalibrated rule can look safe on one batch and fail on the next.

Recalibration with target cells cycled only to $L^\ast$, keeping the source model, is informative only where the target calibration set contains enough cells of each class. With 30 CLO cells (about 12.0 bad and 18.0 good; 6.0 bad and 9.0 good test cells per split) the error rates were 0.075 and 0.046 and 26.8% of the cycling was saved; given the small test sets this is consistent with, but only weakly supports, restored validity. With 20 CLO cells (about 8.0 bad) and for b3 (about 2.0 bad cells among 20 or 30), fewer than the nine cells needed for a pass threshold were available, so the rule never passed a cell early (100% of the splits) and its zero false-pass rate holds by construction; it saved 6.0–9.4% of the cycling. The Gaussian rule, recalibrated in the same way, kept a false-reject rate above 0.79.

Across laboratories, a model trained on MATR/CLO capacity trajectories and recalibrated on HUST cells was valid on the remaining HUST cells (false-pass 0.080, false-reject 0.070), although it saved only 23.9% of the cycling against 47.0% for a model trained on HUST cells. Recalibration on the target population therefore transfers validity even when the base model comes from another laboratory; efficiency still depends on how well the model fits the new cells.

When whole charging protocols were held out, so that no protocol of a test cell was seen in training or calibration (E9, 78 protocol groups of MATR/CLO), the trajectory rule had false-pass and false-reject rates of 0.073 and 0.088 and saved 75.1% of the cycling. This is a stress test outside the assumptions of Proposition 1, because cells sharing a protocol are not exchangeable with cells of other protocols; that the rates stayed near the targets suggests that, for protocols drawn at random from the same design space, protocol-level exchangeability is enough in practice. It does not cover protocols outside that space.

### 3.8 Calibration-set-conditional control and computation

**How often a single campaign misses the target.** Proposition 1 bounds error rates on average over calibration sets. For one particular calibration set the conditional false-pass probability can exceed $\alpha$, and with tens of calibration cells it does so often: in the main experiment the realised false-pass rate on the test cells exceeded 0.10 in 26% (MATR/CLO) and 21% (HUST) of the splits, the false-reject rate in 31% and 24%, and at least one of the two in 51% and 43%. Part of this is test-set sampling noise (about 20.0 bad and 22.0 good test cells per split on MATR/CLO), and part is the variability of the calibrated threshold itself: for 20 calibration cells of a class, the probability that the conditional error probability of a marginally calibrated threshold exceeds $\alpha=0.10$ is 39% (Table S15). The single-checkpoint and lifetime-interval rules share this property; it is inherent to marginal conformal guarantees with small calibration sets.

**Training-conditional (PAC) calibration.** The PAC variant of Section 2.4 ($\delta=0.10$) targets this directly, at a large cost in efficiency (Table S12). On MATR/CLO, with about 20.0 bad and 22.0 good calibration cells, it lowered the mean error rates to 0.011 and 0.027 and saved 28.1% of the cycling instead of 78.5%; with about 36.8 bad and 40.2 good calibration cells it saved 56.3% (marginal rule 80.8%). On HUST, with about 11.9 cells per class, no finite PAC threshold exists (at least 22 are needed at $\alpha=\delta=0.10$) and the rule never decided; with about 20.2 per class it passed no cell in 80% of the splits and saved 6.3%. The share of splits in which the realised test-set error exceeded 0.10 fell to 4% (false pass) and 8% (false reject) on MATR/CLO. This split-level share is only a proxy for the PAC property, because the realised rate on 20–40 test cells also varies with the test sample; it is consistent with, but does not verify, the $\delta=0.10$ bound. Calibration-set-conditional control is therefore practical only with several tens of calibration cells per class; with fewer, users should accept the marginal guarantee and plan for the per-campaign variability reported above.

**Computational cost.** The screening layer itself is negligible (Table S9): calibrating the two thresholds took 0.069 ms for 40 calibration cells and 0.735 ms for 4,000, and deciding 1,000 cells over all checkpoints took about 33.65 ms on one CPU core. The cost of the procedure is that of training the per-checkpoint base predictors once per calibration campaign: on MATR/CLO, 2.0 s per split for the elastic net (all 16 checkpoints, including internal cross-validation), 5.0 s for the Gaussian process, 7.7 s for the CNN, and 22.3 s for the random forest. Peak memory of a process running one split was about 856 MB for every model, dominated by the imported numerical libraries. Even the slowest model needs well under a minute per calibration campaign, against the days to months of cycling that the screening saves, so computation is not a constraint in a test laboratory.

### 3.9 Physical basis of early decisions

![**Figure 8.** Which early-cycle signals carry the screening decision (E11). Top: Spearman correlation between each feature and $\log_{10}$ cycle life over all cells alive at each checkpoint. Bottom: mean absolute standardised elastic-net coefficient of the four most used features over the training sets of 200 E1 splits; the dashed line sums all other features. Features are ordered by their largest coefficient.](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig15_interpretation.png){width=6.3in}

The time at which a cell can be decided is set by when its early-cycle data begin to separate long- from short-lived cells (Figure 8). On MATR/CLO no feature correlated with cycle life by more than |ρ| = 0.32 at cycle 20. From cycle 40 onwards the variance of $\Delta Q_{k-10}(V)$ became the dominant signal (ρ = -0.74 at cycle 40, -0.85 at cycle 100), and from cycle 100 it carried the largest share of the elastic-net weight (49% at cycle 100). Severson et al. linked this change in the shape of the discharge voltage curve to degradation modes, such as loss of active material, that are not yet visible as capacity fade [1]. This timing matches the decision profile of the proposed rule: most MATR/CLO cells were decided between cycles 40 and 100 (Figure 4). Capacity-fade features (slope of the capacity trajectory, $Q_k-Q_{10}$) correlated with lifetime only after about 200 cycles, i.e. after most decisions had been taken.

The HUST cells behaved differently. Their early signal came mainly from the initial capacity at cycle 2 (ρ = 0.53) and the intercept of the capacity trajectory (ρ = 0.61 at cycle 100), i.e. from cell-to-cell differences present at the start of life rather than from degradation. The statistics of $\Delta V(q)$, the HUST analogue of $\Delta Q(V)$, were only moderately informative (|ρ| ≤ 0.61 for any feature at cycle 100), and the capacity-fade features became strongly informative only after about 600 cycles (ρ = 0.81 for the fade slope at cycle 800). This is why the HUST cells were decided later and why less cycling was saved there than on MATR/CLO. A plausible reason is that every HUST cell was discharged with a different multi-step protocol, which changes the voltage-curve signatures that the MATR/CLO features exploit; we could not test this explanation directly. The comparison shows that the efficiency of any early-screening rule is limited by when the electrochemical signal appears, whereas the error guarantee does not depend on it.

### 3.10 Error analysis

![**Figure 9.** Error frequency of the proposed rule for each cell, across the splits in which the cell was a test cell (E1), against the distance of its cycle life from the specification, $\log_{10}(T/L^\ast)$. Bad cells (left) can only be falsely passed; good cells (right) can only be falsely rejected.](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig11_error_analysis.png){width=6.3in}

Errors concentrated near the specification (Figure 9): the Spearman correlation between $|\log_{10}(T/L^\ast)|$ and a cell's error frequency was -0.45 on MATR/CLO ($p$ = 1.2 × 10^-9^) and -0.44 on HUST ($p$ = 5.2 × 10^-5^). Cells within 0.05 decades of $L^\ast$ (about ±12% in cycle life) had a mean error frequency of 0.189 on MATR/CLO compared with 0.028 for cells more than 0.1 decades away, and they accounted for 62% of all errors. Errors far from $L^\ast$ came from a few cells whose early-cycle behaviour was not representative of their lifetime (Table S18): the shortest-lived MATR cell (148 cycles) failed abruptly after early cycles that resembled those of ordinary cells and was falsely passed in most splits in which it was tested, and one long-lived cell (1,315 cycles) was falsely rejected in most splits because its early capacity-difference signature resembled that of short-lived cells. No early-cycle screening rule can classify such cells correctly from these features; the guarantee bounds how often such cells are mis-screened in aggregate but cannot identify them. On HUST the most frequent errors involved cells within about 6% of $L^\ast$ (Table S19).


### 3.11 Implications for cycle-life testing

**Repeated looks must be paid for.** The most consequential result for practice is the behaviour of the naive sequential rule. Each of its per-checkpoint thresholds is a valid conformal threshold, and a practitioner who re-evaluates a prediction every few cycles and stops at the first confident call is implicitly using it. Its error rates were 0.145 (false pass) and 0.158 (false reject) on MATR/CLO and 0.286 and 0.214 on HUST at a nominal 0.10 — the optional-stopping inflation known from sequential analysis [19,20] appears in battery screening at a practically relevant scale. Calibrating on the maximum over checkpoints removes this inflation at a cost that the data show to be modest, because scores of the same cell at successive checkpoints are strongly dependent; Bonferroni's union bound ignores that dependence and, with tens of calibration cells, reached decisions only on a two-checkpoint grid (Section 3.5).

**Truncated campaigns.** Because the class-conditional thresholds depend only on whether each calibration cell reached $L^\ast$, calibration cells can be retired at $\min(T,L^\ast)$ — the same observation that underlies conformal methods for censored lifetimes [42]. In our splits this shortened the calibration campaign (wall-clock time of the longest-running calibration cell) from 1,958 to 750 cycles on MATR/CLO (factor 2.61) and from 2,630 to 1,900 cycles on HUST (factor 1.38); the total cell-cycles of the calibration campaign fell less, by factors of 1.22 and 1.09. The saving applies to the calibration campaign only: a regression base predictor still needs training cells cycled to end of life. A classifier of $Z$ trained on truncated cells removes that requirement as well, and kept the error guarantees but saved about ten percentage points less cycling (Section 3.4). The lifetime-interval rule, which needs calibration cells cycled to end of life, was less efficient, partly because it targets a stricter, two-sided goal: its realised class-conditional error rates were five to ten times below the target.

**One checkpoint or many?** With a checkpoint fixed in advance at cycle 100, the sequential rule saved as much cycling as the single-checkpoint rule on MATR/CLO and clearly more on HUST, whose informative checkpoints come later (Section 3.3). That advantage disappeared when the single checkpoint was chosen on the training cells (Section 3.5): a training-selected single checkpoint and a training-selected sequential grid saved the same cycling on both data sets. Trajectory calibration is therefore not a way to screen faster than a well-chosen single look. Its value is that it keeps the error rates valid when a laboratory looks at its cells repeatedly and stops at the first confident call — what the naive rule does, with error rates up to 2.9 times the target — and that it lets the laboratory stop at whichever checkpoint the data allow without committing to one in advance. In practice, a sparse grid chosen on training cells is a reasonable default.

**Model-based uncertainty.** A Gaussian threshold applied at every look to the same normalised scores was conservative on MATR/CLO but exceeded the false-reject target on HUST, and the point-prediction rule of Severson et al. had no control on HUST (0.237 and 0.367). Part of the Gaussian rule's failure is the repeated-looks effect, because it applies an uncorrected threshold at every checkpoint, and part is that the score scale $s_k$ estimated on training residuals is optimistic; both are properties of how model-based uncertainty is typically used for early decisions. Correcting the Gaussian threshold for the number of looks (Bonferroni over the checkpoints, E13) made it valid on both data sets (0.012/0.007 and 0.008/0.017) but so conservative that it saved only 46.8% and 22.8% of the cycling, against 78.1% and 50.8% for the trajectory rule on the same splits. The same model, used with different decision thresholds, can be either wasteful or unsafe depending on the data set, whereas rank-based calibration adapts to the data at hand.

**What the guarantee does and does not mean.** Proposition 1 bounds error *rates* averaged over calibration and test draws from an exchangeable population. Three consequences matter for users. (i) For a given calibration set the conditional error can exceed the target: with 20 bad calibration cells, the probability that the conditional false-pass probability exceeds 0.10 is 39% (Table S15); a training-conditional (PAC) variant removes this at the price of needing at least 22 calibration cells per class (Section 3.8). (ii) The guarantee is class-conditional, not cell-conditional: cells whose lifetime is close to $L^\ast$ carry most of the errors (Section 3.10), as expected for any screening rule. (iii) Exchangeability is an assumption about how the calibration cells were obtained; it is plausible for cells drawn from the same production lot and measured with the same equipment. In our experiments it failed when a later batch was screened with thresholds calibrated on earlier batches, and recalibration with target cells cycled only to $L^\ast$ was needed; a model trained in one laboratory and calibrated in the other stayed valid (Section 3.7). Extra noise on the screened cells alone also broke the guarantee (Section 3.6), so calibration and screening must share the measurement chain.

**Recommended workflow.** (1) Fix $L^\ast$, $\alpha$ and $\beta$ before testing, and choose a sparse checkpoint grid on training cells only. (2) Train a base predictor on any available historical cells (full-lifetime or truncated). (3) Cycle a calibration set of at least ten bad and ten good cells (preferably more than 22 of each for training-conditional control) from the population to be screened, to $\min(T,L^\ast)$ only. (4) Screen new cells sequentially with the trajectory-calibrated thresholds. (5) Recalibrate whenever the cell population, production batch or measurement equipment changes.

### 3.12 Limitations

* **One chemistry.** All 246 cells are LiFePO~4~/graphite 18650 cells of one type, from two laboratories. We tried to add cells of other chemistries, but the NCA/NCM data of Zhu et al. (Zenodo) and the NMC data of RWTH Aachen were not reachable from our computing environment (HTTP 403 and an interactive browser challenge), and the Sandia data available through BatteryArchive involve partial-depth cycling with many cells not reaching end of life. The guarantee itself does not depend on chemistry, but the efficiency results may.
* **Exchangeability and shift.** The guarantees require the calibration cells to be exchangeable with the cells being screened. Section 3.7 shows that they fail under batch shift without recalibration (laboratory shift was tested only with recalibration on the target laboratory), and Section 3.6 that extra measurement noise on the screened cells alone breaks them; the sequential rule was more sensitive to such noise than a single-checkpoint rule.
* **Marginal, class-conditional guarantee** (see Section 3.11); conditional error can exceed the target for a particular calibration set unless the PAC variant is used.
* **Retrospective evaluation.** Results come from repeated random splits of finite public data sets, not from a prospective screening campaign; the splits re-use the same cells, so split-to-split variation understates the variation across independent cell populations.
* **Cost model.** Time saved is measured in cell-cycles relative to cycling each cell to $\min(T,L^\ast)$; channel scheduling, rest periods and reference performance tests are not modelled.
* **Lifetime labels** are those of the data providers (first cycle at 80% of nominal capacity); other end-of-life definitions change the class labels [37].

## 4 Conclusions

Early cycle-life predictions are routinely used to make go/no-go decisions, but the error rate of those decisions is rarely controlled, and the common practice of re-checking predictions as cycling proceeds silently inflates it. We showed that calibrating pass and reject thresholds on the maximum over checkpoints of normalised model scores gives finite-sample, distribution-free bounds on the false-pass and false-reject probabilities that hold under any stopping time, and that the calibration needs cells cycled only to the specification. On 246 commercial LiFePO~4~/graphite cells from two laboratories, the rule met its error targets with 0.10 nominal levels while cutting cycling by 78.3% (MATR/CLO) and 50.7% (HUST) relative to cycling every cell to the specification, whereas naive sequential use of valid per-checkpoint thresholds exceeded the targets by up to a factor of 2.9. A single checkpoint chosen on training cells was as efficient, so the gain from trajectory calibration is valid error control under repeated looks and flexible stopping, not faster screening; the guarantee holds on average over calibration campaigns and requires recalibration when the cell population changes. The procedure is a thin layer on top of any lifetime predictor, costs milliseconds to run, and is released with code that reproduces every result.

## Acknowledgments

We thank the providers of the public data sets used in this study: the Toyota Research Institute, Massachusetts Institute of Technology and Stanford University teams who released the MATR/CLO data (data.matr.io), and Ma et al. (Huazhong University of Science and Technology) for the HUST data.

## Author Contributions (CRediT)

**Bhargav Teja:** Conceptualization; Methodology; Software; Validation; Formal analysis; Investigation; Data curation; Visualization; Writing – original draft; Writing – review & editing. **[Second Author]:** Supervision.

## Conflict of Interest Statement

The authors declare no conflicts of interest.

## Funding

This research received no specific grant from any funding agency in the public, commercial or not-for-profit sectors.

## Data Availability Statement

The raw data analysed in this study are openly available: MATR/CLO cycling data at https://data.matr.io/1/ (Severson et al. [1]; Attia et al. [2]) and HUST data at Mendeley Data, https://doi.org/10.17632/nsc7hnsg4s.2 (Ma et al. [8]). The checkpoint feature tables derived from them, all split-level results, statistics, tables and figures, and the complete code that regenerates them (`python run_all.py --mode full`) are available at [repository URL / archival DOI to be inserted at submission].

## Ethics Statement

This study used only previously published battery cycling data; it involved no human participants, animals or personal data.

## Use of Generative AI

[Required by Wiley policy — to be completed accurately by the authors.] The study design, code, analyses and draft text were produced with the assistance of a generative-AI agent. [State the tool, the tasks it performed, and the human verification of code, results, citations and text.] The authors take full responsibility for the content.


## References

[1] K. A. Severson, P. M. Attia, N. Jin, N. Perkins, B. Jiang, Z. Yang, M. H. Chen, M. Aykol, P. K. Herring, D. Fraggedakis, M. Z. Bazant, S. J. Harris, W. C. Chueh, R. D. Braatz, Data-driven prediction of battery cycle life before capacity degradation, *Nature Energy* 2019, 4, 383-391. https://doi.org/10.1038/s41560-019-0356-8

[2] P. M. Attia, A. Grover, N. Jin, K. A. Severson, T. M. Markov, Y. H. Liao, M. H. Chen, B. Cheong, N. Perkins, Z. Yang, P. K. Herring, M. Aykol, S. J. Harris, R. D. Braatz, S. Ermon, W. C. Chueh, Closed-loop optimization of fast-charging protocols for batteries with machine learning, *Nature* 2020, 578, 397-402. https://doi.org/10.1038/s41586-020-1994-5

[3] T. Baumhöfer, M. Brühl, S. Rothgang, D. U. Sauer, Production caused variation in capacity aging trend and correlation to initial cell performance, *Journal of Power Sources* 2014, 247, 332-338. https://doi.org/10.1016/j.jpowsour.2013.08.108

[4] B. Jiang, W. E. Gent, F. Mohr, S. Das, M. D. Berliner, M. Forsuelo, H. Zhao, P. M. Attia, A. Grover, P. K. Herring, M. Z. Bazant, S. J. Harris, S. Ermon, W. C. Chueh, R. D. Braatz, Bayesian learning for rapid prediction of lithium-ion battery-cycling protocols, *Joule* 2021, 5, 3187-3203. https://doi.org/10.1016/j.joule.2021.10.010

[5] P. M. Attia, K. A. Severson, J. D. Witmer, Statistical Learning for Accurate and Interpretable Battery Lifetime Prediction, *Journal of The Electrochemical Society* 2021, 168, 090547. https://doi.org/10.1149/1945-7111/ac2704

[6] P. Fermín-Cueto, E. McTurk, M. Allerhand, E. Medina-Lopez, M. F. Anjos, J. Sylvester, G. dos Reis, Identification and machine learning prediction of knee-point and knee-onset in capacity degradation curves of lithium-ion cells, *Energy and AI* 2020, 1, 100006. https://doi.org/10.1016/j.egyai.2020.100006

[7] P. M. Attia, A. Bills, F. Brosa Planella, P. Dechent, G. dos Reis, M. Dubarry, P. Gasper, R. Gilchrist, S. Greenbank, D. Howey, O. Liu, E. Khoo, Y. Preger, A. Soni, S. Sripad, A. G. Stefanopoulou, V. Sulzer, Review—“Knees” in Lithium-Ion Battery Aging Trajectories, *Journal of The Electrochemical Society* 2022, 169, 060517. https://doi.org/10.1149/1945-7111/ac6d13

[8] G. Ma, S. Xu, B. Jiang, C. Cheng, X. Yang, Y. Shen, T. Yang, Y. Huang, H. Ding, Y. Yuan, Real-time personalized health status prediction of lithium-ion batteries using deep transfer learning, *Energy & Environmental Science* 2022, 15, 4083-4094. https://doi.org/10.1039/d2ee01676a

[9] N. Guo, S. Chen, J. Tao, Y. Liu, J. Wan, X. Li, Semi-supervised learning for explainable few-shot battery lifetime prediction, *Joule* 2024, 8, 1820-1836. https://doi.org/10.1016/j.joule.2024.02.020

[10] X. Zhai, G. Liu, T. Lu, S. Chen, Y. Liu, J. Wan, X. Li, Transforming waste to value: Enhancing battery lifetime prediction using incomplete data samples, *Journal of Energy Chemistry* 2025, 106, 642-649. https://doi.org/10.1016/j.jechem.2025.03.011

[11] F. Wang, Z. Zhai, Z. Zhao, Y. Di, X. Chen, Physics-informed neural network for lithium-ion battery degradation stable modeling and prognosis, *Nature Communications* 2024, 15, 4332. https://doi.org/10.1038/s41467-024-48779-z

[12] H. Zhang, X. Gui, S. Zheng, Z. Lu, Y. Li, J. Bian, BatteryML: An Open-source Platform for Machine Learning on Battery Degradation, *International Conference on Learning Representations (ICLR 2024)* 2024. arXiv:2310.14714

[13] X. Hu, L. Xu, X. Lin, M. Pecht, Battery Lifetime Prognostics, *Joule* 2020, 4, 310-346. https://doi.org/10.1016/j.joule.2019.11.018

[14] V. Sulzer, P. Mohtat, A. Aitio, S. Lee, Y. T. Yeh, F. Steinbacher, M. U. Khan, J. W. Lee, J. B. Siegel, A. G. Stefanopoulou, D. A. Howey, The challenge and opportunity of battery lifetime prediction from field data, *Joule* 2021, 5, 1934-1955. https://doi.org/10.1016/j.joule.2021.06.005

[15] M. F. Sulaima, S. Arora, R. Frischer, H. Namazi, Physics‐Informed Artificial Intelligence for Battery Degradation, Aging, and Lifetime Prediction, *Battery Energy* 2026, 5, e70136. https://doi.org/10.1002/bte2.70136

[16] J. Hu, L. Wu, Early Uncertainty Quantification Prediction of Lithium-Ion Battery Remaining Useful Life With Transformer Ensemble Model, *IEEE Transactions on Transportation Electrification* 2024, 10, 8618-8629. https://doi.org/10.1109/tte.2024.3354302

[17] Y. Ke, Y. Jiang, R. Zhu, W. Peng, X. Tan, Early Prediction of Knee Point and Knee Capacity for Fast-Charging Lithium-Ion Battery With Uncertainty Quantification and Calibration, *IEEE Transactions on Transportation Electrification* 2024, 10, 2873-2885. https://doi.org/10.1109/tte.2023.3304670

[18] R. R. Richardson, M. A. Osborne, D. A. Howey, Gaussian process regression for forecasting battery state of health, *Journal of Power Sources* 2017, 357, 209-219. https://doi.org/10.1016/j.jpowsour.2017.05.004

[19] A. Wald, Sequential Tests of Statistical Hypotheses, *The Annals of Mathematical Statistics* 1945, 16, 117-186. https://doi.org/10.1214/aoms/1177731118

[20] S. R. Howard, A. Ramdas, J. McAuliffe, J. Sekhon, Time-uniform, nonparametric, nonasymptotic confidence sequences, *The Annals of Statistics* 2021, 49, 1055-1080. https://doi.org/10.1214/20-aos1991

[21] V. Vovk, A. Gammerman, G. Shafer, Algorithmic Learning in a Random World, *Springer* 2005. https://doi.org/10.1007/b106715

[22] J. Lei, M. G’Sell, A. Rinaldo, R. J. Tibshirani, L. Wasserman, Distribution-Free Predictive Inference for Regression, *Journal of the American Statistical Association* 2018, 113, 1094-1111. https://doi.org/10.1080/01621459.2017.1307116

[23] A. N. Angelopoulos, S. Bates, Conformal Prediction: A Gentle Introduction, *Foundations and Trends® in Machine Learning* 2023, 16, 494-591. https://doi.org/10.1561/2200000101

[24] K. Wu, X. Wu, H. Shi, M. He, Uncertainty-Aware Early Battery Life Prediction with Composite-Kernel Gaussian Process Regression and Conformalized Adaptive Intervals, *Algorithms* 2026, 19, 535. https://doi.org/10.3390/a19070535

[25] A. Weng, P. Mohtat, P. M. Attia, V. Sulzer, S. Lee, G. Less, A. Stefanopoulou, Predicting the impact of formation protocols on battery lifetime immediately after manufacturing, *Joule* 2021, 5, 2971-2992. https://doi.org/10.1016/j.joule.2021.09.015

[26] Y. Zhang, Q. Tang, Y. Zhang, J. Wang, U. Stimming, A. A. Lee, Identifying degradation patterns of lithium ion batteries from impedance spectroscopy using machine learning, *Nature Communications* 2020, 11, 1706. https://doi.org/10.1038/s41467-020-15235-7

[27] G. dos Reis, C. Strange, M. Yadav, S. Li, Lithium-ion battery data and where to find it, *Energy and AI* 2021, 5, 100081. https://doi.org/10.1016/j.egyai.2021.100081

[28] F. Xiao, W. Yang, Y. Ding, X. Li, K. Zhang, J. Liu, A CNN‐LSTM Method Based on Voltage Deviation for Predicting the State of Health of Lithium‐Ion Batteries, *Battery Energy* 2025, 4, e20240036. https://doi.org/10.1002/bte2.20240036

[29] Z. Lyu, X. Wei, L. Wu, C. Liu, Transfer Learning‐Based Data‐Fusion Model Framework for State of Health Estimation of Power Battery Packs, *Battery Energy* 2025, 4, e70011. https://doi.org/10.1002/bte2.70011

[30] J. Kee, S. Lee, J. Hwang, S. Yoon, S. Han, D. Kim, Degradation-Informed Temperature Analysis for Cycle Life Prediction of LiFePO4 Batteries, *Battery Energy* 2026, 5, e70124. https://doi.org/10.1002/bte2.70124

[31] H. Zhang, Y. Su, F. Altaf, T. Wik, S. Gros, Interpretable Battery Cycle Life Range Prediction Using Early Cell Degradation Data, *IEEE Transactions on Transportation Electrification* 2023, 9, 2669-2682. https://doi.org/10.1109/tte.2022.3226683

[32] M. Liu, Y. Wang, W. Li, J. Cao, F. Yang, Toward reliable battery life prediction: A hybrid data-driven framework with uncertainty quantification, *Energy Engineering* 2026, 123. https://doi.org/10.32604/ee.2026.074783

[33] D. C. Li, Early detection of short-term performance degradation in electric vehicle lithium-ion batteries via physics-guided multi-sensor fusion and deep learning, *Batteries* 2026, 12, 116. https://doi.org/10.3390/batteries12040116

[34] Y. Romano, E. Patterson, E. J. Candès, Conformalized Quantile Regression, *Advances in Neural Information Processing Systems* 2019, 32, 3538-3548. arXiv:1905.03222

[35] S. F. d. Silva, M. F. Ozkan, F. E. Idrissi, M. Canova, Conformalized Transfer Learning for Li-ion Battery State of Health Forecasting under Manufacturing and Usage Variability, *arXiv* 2026. arXiv:2603.24475

[36] X. Liu, From fleet trajectories to single-cell promises: hierarchically weighted conformal prediction for battery SOH monitoring, *arXiv* 2026. arXiv:2610.41696

[37] J. Li, W. Li, T. Li, Endpoint definitions and censoring in battery lifetime prediction across sources, *Research Square (preprint)* 2026. https://doi.org/10.21203/rs.3.rs-11508938/v1

[38] X. Tong, Y. Feng, J. J. Li, Neyman-Pearson classification algorithms and NP receiver operating characteristics, *Science Advances* 2018, 4, eaao1659. https://doi.org/10.1126/sciadv.aao1659

[39] M. Sadinle, J. Lei, L. Wasserman, Least Ambiguous Set-Valued Classifiers With Bounded Error Levels, *Journal of the American Statistical Association* 2019, 114, 223-234. https://doi.org/10.1080/01621459.2017.1395341

[40] S. Bates, E. Candès, L. Lei, Y. Romano, M. Sesia, Testing for outliers with conformal p-values, *The Annals of Statistics* 2023, 51, 149-178. https://doi.org/10.1214/22-AOS2244

[41] A. N. Angelopoulos, S. Bates, E. J. Candès, M. I. Jordan, L. Lei, Learn then test: Calibrating predictive algorithms to achieve risk control, *The Annals of Applied Statistics* 2025, 19, 1641-1662. https://doi.org/10.1214/24-AOAS1998

[42] E. Candès, L. Lei, Z. Ren, Conformalized survival analysis, *Journal of the Royal Statistical Society Series B: Statistical Methodology* 2023, 85, 24-45. https://doi.org/10.1093/jrsssb/qkac004

[43] Y. Gui, R. Hore, Z. Ren, R. F. Barber, Conformalized survival analysis with adaptive cutoffs, *Biometrika* 2024, 111, 459-477. https://doi.org/10.1093/biomet/asad076

[44] M. Sesia, V. Svetnik, Doubly Robust Conformalized Survival Analysis with Right-Censored Data, *Proceedings of the 42nd International Conference on Machine Learning (ICML 2025), PMLR* 2025, 267, 53989-54029. arXiv:2412.09729

[45] Y. Jin, E. J. Candès, Selection by Prediction with Conformal p-values, *Journal of Machine Learning Research* 2023, 24, 1-41. arXiv:2210.01408

[46] S. J. Pocock, Group sequential methods in the design and analysis of clinical trials, *Biometrika* 1977, 64, 191-199. https://doi.org/10.1093/biomet/64.2.191

[47] P. C. O'Brien, T. R. Fleming, A multiple testing procedure for clinical trials, *Biometrics* 1979, 35, 549-556. https://doi.org/10.2307/2530245

[48] K. K. G. Lan, D. L. DeMets, Discrete sequential boundaries for clinical trials, *Biometrika* 1983, 70, 659-663. https://doi.org/10.2307/2336502

[49] C. Jennison, B. W. Turnbull, Group Sequential Methods with Applications to Clinical Trials, *Chapman & Hall/CRC, Boca Raton* 2000.

[50] A. Ramdas, P. Grünwald, V. Vovk, G. Shafer, Game-theoretic statistics and safe anytime-valid inference, *Statistical Science* 2023, 38, 576-601. https://doi.org/10.1214/23-STS894

[51] M. Jazbec, P. Forré, S. Mandt, D. Zhang, E. Nalisnick, Early-Exit Neural Networks with Nested Prediction Sets, *Proceedings of the 40th Conference on Uncertainty in Artificial Intelligence (UAI 2024), PMLR* 2024, 244, 1780-1796. arXiv:2311.05931

[52] L. Ringel, R. Cohen, D. Freedman, M. Elad, Y. Romano, Early time classification with accumulated accuracy gap control, *Proceedings of the 41st International Conference on Machine Learning (ICML 2024), PMLR* 2024, 235, 42584-42600. arXiv:2402.00857

[53] J. Chen, S. Park, O. Simeone, Knowing when to stop: Delay-adaptive spiking neural network classifiers with reliability guarantees, *IEEE Journal of Selected Topics in Signal Processing* 2025, 19, 88-102. https://doi.org/10.1109/JSTSP.2024.3431996

[54] W. Li, N. Qiao, X. Guo, W. Sun, COINS: Any-stage-valid and utility-oriented sequential conformal prediction, *arXiv* 2026. arXiv:2609.07112

[55] J. Lei, A. Rinaldo, L. Wasserman, A conformal prediction approach to explore functional data, *Annals of Mathematics and Artificial Intelligence* 2015, 74, 29-43. https://doi.org/10.1007/s10472-013-9366-6

[56] J. Diquigiovanni, M. Fontana, S. Vantini, Conformal prediction bands for multivariate functional data, *Journal of Multivariate Analysis* 2022, 189, 104879. https://doi.org/10.1016/j.jmva.2021.104879

[57] L. Lindemann, X. Qin, J. V. Deshmukh, G. J. Pappas, Conformal prediction for STL runtime verification, *Proceedings of the ACM/IEEE 14th International Conference on Cyber-Physical Systems (ICCPS 2023)* 2023, 142-153. https://doi.org/10.1145/3576841.3585927

[58] M. Cleaveland, I. Lee, G. J. Pappas, L. Lindemann, Conformal prediction regions for time series using linear complementarity programming, *Proceedings of the AAAI Conference on Artificial Intelligence* 2024, 38, 20984-20992. https://doi.org/10.1609/aaai.v38i19.30089

[59] K. Stankeviciute, A. M. Alaa, M. van der Schaar, Conformal Time-series Forecasting, *Advances in Neural Information Processing Systems* 2021, 34.

[60] H. Zou, T. Hastie, Regularization and Variable Selection Via the Elastic Net, *Journal of the Royal Statistical Society Series B: Statistical Methodology* 2005, 67, 301-320. https://doi.org/10.1111/j.1467-9868.2005.00503.x

[61] F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, M. Blondel, A. Müller, J. Nothman, G. Louppe, P. Prettenhofer, R. Weiss, V. Dubourg, J. Vanderplas, A. Passos, D. Cournapeau, M. Brucher, M. Perrot, É. Duchesnay, Scikit-learn: Machine Learning in Python, *Journal of Machine Learning Research* 2011, 12, 2825-2830. arXiv:1201.0490

[62] C. E. Rasmussen, C. K. I. Williams, Gaussian Processes for Machine Learning, *MIT Press* 2006. https://doi.org/10.7551/mitpress/3206.001.0001

[63] F. Wilcoxon, Individual Comparisons by Ranking Methods, *Biometrics Bulletin* 1945, 1, 80-83. https://doi.org/10.2307/3001968

[64] S. Holm, A simple sequentially rejective multiple test procedure, *Scandinavian Journal of Statistics* 1979, 6, 65-70.

[65] B. Efron, Bootstrap Methods: Another Look at the Jackknife, *The Annals of Statistics* 1979, 7, 1-26. https://doi.org/10.1214/aos/1176344552