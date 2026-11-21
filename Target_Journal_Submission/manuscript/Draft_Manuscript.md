# Stopping Cycle-Life Tests Early With Guaranteed Error Rates: Distribution-Free Sequential Screening of Lithium-Ion Cells From Truncated Test Campaigns

**Running title:** Guaranteed early screening of cell cycle life

**Authors:** [Author 1]^1^, [Author 2]^1^, [Corresponding Author]^1,\*^

^1^ [Department, Institution, City, Postal code, Country]

\* Correspondence: [name], [e-mail address]

## Abstract

Early-cycle predictions of lithium-ion cell cycle life are increasingly used to stop long cycling tests early, but the error rate of the resulting pass/fail decisions is rarely controlled, and re-checking predictions as cycling proceeds inflates it. We present a distribution-free sequential screening procedure that, at a series of early checkpoints, passes a cell, rejects it or keeps it on test. Pass and reject thresholds are calibrated on the maximum over checkpoints of normalised model scores of held-out calibration cells. We prove that this bounds the probability of passing a cell that will not reach a cycle-life specification, and of rejecting one that will, at user-chosen levels under any data-dependent stopping time, and that calibration cells need to be cycled only to the specification rather than to end of life. On 246 commercial LiFePO~4~/graphite cells from two laboratories, with 1,000 random splits per data set and a nominal level of 0.10, the false-pass and false-reject rates were 0.068 and 0.080 (MATR/CLO) and 0.068 and 0.074 (HUST), while 78.3% and 50.7% of the cycling needed to observe every cell to the specification was saved; calibration campaigns ended 2.61 times sooner than with full-lifetime calibration. Sequential use of individually valid per-checkpoint thresholds exceeded the targets by up to 2.9 times, and parametric and point-prediction rules violated them on one data set. Under batch shift the guarantees failed without recalibration (false-reject rate up to 0.597) and were restored by recalibrating with 30 cells of the new batch cycled only to the specification. The procedure works with any lifetime predictor and adds negligible computation.

**Keywords:** lithium-ion battery; cycle life; early prediction; battery testing; conformal prediction; sequential decision; uncertainty quantification

## 1 Introduction

Cycle-life testing is the slowest step in the development and qualification of lithium-ion cells. A cell that lasts 761 cycles under fast charging occupies a cycler channel for weeks to months before its end of life (EOL, conventionally 80% of nominal capacity) is observed, and design or protocol comparisons need many such cells [1,2]. Data-driven early prediction has therefore attracted sustained attention. Severson et al. showed that features of the discharge-capacity curve difference between cycles 10 and 100 predict the cycle life of commercial LiFePO~4~/graphite cells with about 9% error [1]; Attia et al. embedded such predictions in closed-loop optimisation of fast-charging protocols and cut the experimental time from more than 500 to 16 days [2]; and hierarchical Bayesian models predicted protocol lifetimes from a few cycles [3]. Later work refined features and knee prediction [4–6], used transfer or semi-supervised learning with unfinished cells [7–9], combined physics with learning [10], and built open benchmarks [11]. Reviews in this journal and elsewhere identify uncertainty-aware lifetime prediction as an open need [12–14].

In qualification and screening, however, the question asked of an early prediction is a decision: does this cell (or this design) meet a cycle-life specification $L^\ast$? Acting on a point prediction exposes the laboratory to an error rate that is unknown in advance. Ensemble, Gaussian-process or Bayesian uncertainty estimates [3,15,16] are model-dependent and are not guaranteed to be calibrated for a new set of cells. A second, less discussed problem is *repeated looking*. As cycling proceeds, engineers naturally re-evaluate the prediction and stop a test as soon as the prediction looks decisive. Even if each individual look controls its error, stopping at the first look that crosses a threshold inflates the overall error; this is the optional-stopping problem of sequential analysis [17,18]. Finally, the uncertainty methods that do carry finite-sample guarantees, such as conformal prediction intervals for lifetime [19–21], are calibrated with cells cycled to EOL, which brings back the long test campaign that early prediction was meant to avoid.

This paper addresses these three problems for early cycle-life screening. Its contributions are:

1. **Formulation.** Early screening is posed as a sequential decision at checkpoints $k_1<\dots<k_M<L^\ast$ with three outcomes (pass, reject, continue cycling) and two class-conditional error constraints: a cell that will not reach $L^\ast$ ("bad") is passed with probability at most $\alpha$, and a cell that will reach $L^\ast$ ("good") is rejected with probability at most $\beta$.
2. **Trajectory calibration with a finite-sample guarantee.** Pass and reject thresholds are calibrated on the *maximum over checkpoints* of normalised model scores of held-out calibration cells. We prove that the two error constraints then hold for any data-dependent stopping time, without distributional assumptions beyond exchangeability of cells, and that each calibration cell needs to be cycled only to $\min(T,L^\ast)$ cycles, not to EOL. The guarantee holds for any base predictor, including one trained only on truncated data.
3. **Evaluation on two laboratories.** On 246 commercial LiFePO~4~/graphite cells from two laboratories (169 MATR/CLO cells [1,2] and 77 HUST cells [7]) and 1,000 random splits per dataset, we compare the procedure with fixed-checkpoint, naive sequential, Bonferroni, parametric/Bayesian and lifetime-interval rules, five additional base predictors, ablations, robustness and sensitivity analyses, batch and laboratory shift, and an error analysis.
4. **Open, reproducible code** that regenerates every number, table and figure in this paper from the public raw data.

We stress what the paper does *not* claim: it does not propose a more accurate lifetime predictor, and its guarantees are statements about error *rates* over the population of cells exchangeable with the calibration cells, not about any individual cell.

## 2 Related Work and Research Gap

**Early cycle-life prediction.** Following Severson et al. [1], early prediction has been extended with feature studies [4], knee-point prediction [5,6], formation-stage diagnostics [22], deep transfer learning on cells with different discharge protocols [7], semi-supervised and incomplete-data learning [8,9], physics-informed networks [10], impedance-based features [23] and benchmarks [11,24]. Papers in *Battery Energy* follow the same pattern of physically motivated features combined with machine learning and evaluated by point accuracy [25–27]. These works report prediction error at a fixed checkpoint; none provides a decision rule with a pre-specified, guaranteed error rate.

**Uncertainty for battery lifetime.** Ensembles, Gaussian processes and Bayesian hierarchical models provide predictive distributions [3,15,16], whose calibration depends on the model being correct. Conformal prediction gives finite-sample, distribution-free coverage under exchangeability [19–21,28] and has recently been applied to state-of-health forecasting [29,30]. Evaluation practice for lifetime models under censoring and differing end-point definitions has also been examined [13,31].

**Statistical foundations.** Our thresholds are class-conditional order statistics, as in Neyman–Pearson classification [32] and class-conditional set-valued classifiers [33]. Conformalised survival analysis uses lifetimes truncated at a cut-off to obtain valid lower bounds under censoring [34–36]; conformal selection controls the false discovery rate when selecting units whose outcome exceeds a threshold [37]. Sequential validity over multiple looks is the subject of sequential testing and confidence sequences [17,18] and, for early-exit neural networks, of anytime-valid nested prediction sets [38].

**Gap.** For early screening of battery cycle life, no existing method (i) controls per-cell false-pass and false-reject probabilities with finite-sample, distribution-free guarantees, (ii) remains valid when the test is stopped at a data-dependent time, and (iii) can be calibrated without cycling calibration cells to end of life. Our procedure adapts the order-statistic arguments above to this setting; its novelty lies in the formulation and in the trajectory-wise calibration that makes the guarantee hold under sequential stopping with calibration data truncated at $L^\ast$, together with an extensive experimental characterisation on public battery data.

## 3 Methods

### 3.1 Problem formulation

Let cell $i$ have cycle life $T_i$ (number of cycles until the discharge capacity first reaches 80% of nominal) and let $L^\ast$ be the specification. The cell is *good* if $T_i \ge L^\ast$ ($Z_i=1$) and *bad* otherwise ($Z_i=0$). Measurements become available cycle by cycle. At checkpoints $k_1<\dots<k_M<L^\ast$ a cell that is still alive ($T_i>k_m$) yields a feature vector $X_i^{(m)}$ computed only from cycles $1,\dots,k_m$. A screening rule decides at each checkpoint to *pass* the cell (stop cycling, declare it good), *reject* it (stop, declare it bad) or *continue*. A cell that fails before a checkpoint is rejected by observation, and a cell still undecided after $k_M$ is cycled until $\min(T_i,L^\ast)$, which reveals its class without error. The targets are

$$ \mathrm{P}(\text{rule passes cell } i \mid Z_i=0)\le\alpha,\qquad \mathrm{P}(\text{rule rejects cell } i \mid Z_i=1)\le\beta, $$

EQNUMMARK(1)


with as few cycles as possible spent before a decision.

### 3.2 Base predictors and normalised scores

For each checkpoint a base predictor $h_m$ is trained on a training set of cells alive at $k_m$. In the main experiments $h_m$ is an elastic net [39] regressing $\log_{10}T$ on the checkpoint features, with penalty and mixing parameter selected by five-fold cross-validation inside the training set. The *normalised score* of cell $i$ at checkpoint $m$ is

$$ S_i^{(m)}=\frac{h_m\!\left(X_i^{(m)}\right)-\log_{10}L^\ast}{s_m}, $$

EQNUMMARK(2)


where $s_m$ is the out-of-fold root-mean-square error of $h_m$ on the training cells (taken from the same cross-validation, so no additional fits are needed). Large positive $S$ is evidence that the cell is good. Normalisation puts checkpoints with very different prediction accuracy on a common scale. Other base predictors are used in Section 4.3: L2-regularised logistic regression on $Z$ (score = logit; trained only on $Z$, i.e. on cells cycled to $\min(T,L^\ast)$), gradient-boosted trees and random forests [40] (scale = out-of-fold RMSE), a Gaussian process with automatic relevance determination [41] (scale = posterior standard deviation of each cell), and a one-dimensional convolutional network on the capacity-difference curve plus the scalar features (scale = RMSE on a 20% validation part of the training cells).

**Features.** For the MATR/CLO cells we generalise the features of Severson et al. [1] from cycle 100 to checkpoint $k$: the logarithms of the absolute minimum, variance, skewness and kurtosis of $\Delta Q_{k-10}(V)=Q_k(V)-Q_{10}(V)$; the discharge capacity at cycle 2; the maximum capacity minus that at cycle 2; slope and intercept of a linear fit to capacity over cycles $2,\dots,k$ and slope over the last 10 cycles; the capacity change between cycles 10 and $k$; the mean charge time of cycles 2–6; and the mean of the per-cycle maximum temperature. Internal-resistance features were not used because the CLO cells have no resistance records. During data auditing we found that some cycles are non-standard (rest or diagnostic steps), producing single-cycle glitches in $Q(V)$; $Q_k(V)$ and $Q_{10}(V)$ are therefore element-wise medians over cycles $k-4,\dots,k$ and $8,\dots,12$, which uses no cycle after $k$. The HUST cells were discharged with multi-step protocols, so $Q(V)$ is not single-valued; we use the analogous statistics of $\Delta V_{k-10}(q)=V_k(q)-V_{10}(q)$ on a grid of discharged capacity $q\in[0.02,0.85]$ Ah together with the same capacity-trajectory features. A unit test verifies that features at checkpoint $k$ are unchanged when all data after cycle $k$ are altered.

### 3.3 Trajectory calibration

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

*Proof.* If a bad cell is passed at checkpoint $m$, it was alive at $k_m$ and $S^{(m)}>\hat\lambda$, hence its trajectory statistic $P_{\text{new}}\ge S^{(m)}>\hat\lambda$. The event therefore implies $P_{\text{new}}>P_{(r_0)}$. By exchangeability the rank of $P_{\text{new}}$ among $P_1,\dots,P_{n_0},P_{\text{new}}$ is uniformly distributed (ties broken at random), so $\mathrm{P}(P_{\text{new}}>P_{(r_0)})\le (n_0+1-r_0)/(n_0+1)\le\alpha$. The argument for good cells is identical with $R$ and $\hat\mu$. Because the event "passed at some checkpoint" is contained in $\{P_{\text{new}}>\hat\lambda\}$ irrespective of when or why the procedure stops, the bound holds for any stopping time. $\square$

**Remarks.** (i) *Truncated calibration.* $P_i$, $R_i$ and $Z_i$ require only cycles up to $\min(T_i,L^\ast)$ because $k_M<L^\ast$; calibration cells never need to be cycled to EOL. If the base predictor is a classifier of $Z$, training cells also need only $\min(T_i,L^\ast)$ cycles. (ii) *Why the maximum.* Calibrating each checkpoint separately at level $\alpha$ ("naive sequential") controls each look but not the first crossing, whose error can approach $M\alpha$; Bonferroni calibration at $\alpha/M$ restores validity but, with tens of calibration cells, gives $\hat\lambda=+\infty$ whenever $(n_0+1)(1-\alpha/M)>n_0$, i.e. whenever $n_0<M/\alpha-1$ (fewer than 159 bad calibration cells for $M=16$ and $\alpha=0.1$). The maximum statistic accounts for the dependence between looks exactly. (iii) *Scope.* The guarantee is marginal over calibration and test cells and conditional on the class; realised error rates in any one batch of test cells fluctuate around it, and it says nothing about cells that are not exchangeable with the calibration cells (Section 4.6). Passing is possible only if $(n_0+1)(1-\alpha)\le n_0$, i.e. $n_0\ge(1-\alpha)/\alpha$ (at least 9 bad calibration cells for $\alpha=0.1$).

### 3.4 Comparison rules

All rules use the same base predictor, splits and cells. *Naive sequential*: per-checkpoint thresholds from the bad (good) calibration cells alive at that checkpoint at level $\alpha$ ($\beta$). *Bonferroni*: the same at $\alpha/M$ and $\beta/M$. *Single checkpoint*: class-conditional thresholds at cycle 100 only (valid, Proposition 1 with $M=1$). *Point prediction at cycle 100*: pass if the predicted lifetime is at least $L^\ast$, otherwise reject [1] (no error control). *Parametric threshold*: pass if $S^{(m)}>z_{1-\alpha}$ and reject if $S^{(m)}<-z_{1-\beta}$, i.e. a Gaussian predictive-bound rule; for the Gaussian process it is the Bayesian rule "posterior probability of being good above $1-\alpha$ / below $\beta$". *Lifetime interval*: trajectory-valid split-conformal lower and upper bounds on $\log_{10}T$ from normalised residuals [20], pass if the lower bound is at least $\log_{10}L^\ast$ and reject if the upper bound is below it; this rule needs calibration cells cycled to EOL and controls the error marginally rather than per class. *Proposed without normalisation*: Equations (3)–(4) applied to $h_m-\log_{10}L^\ast$.

### 3.5 Data

**MATR/CLO.** The 124 LiFePO~4~/graphite cells (A123 APR18650M1A, 1.1 Ah) of Severson et al. [1], cycled under 72 fast-charging policies with 4C discharge, and the 45 cells of the closed-loop-optimisation validation batch of Attia et al. [2], downloaded from data.matr.io. We applied the authors' cleaning steps and verified each against the data: five batch-1 cells that never reached EOL were removed; five batch-1 cells whose cycling continued in batch 2 were concatenated with their continuations (capacities match at the junction); six noisy batch-3 channels were removed. Cycle lives range from 148 to 2,237 cycles (median 761). **HUST.** The 77 cells of the same type tested by Ma et al. [7] with identical fast charging and 77 different multi-step discharge protocols, cycle lives 1,142–2,689 (median 1,875). The HUST files are Python pickles; they were read with an allow-listed unpickler that permits only numpy/pandas reconstruction functions. Both datasets record data until the discharge capacity reaches 0.88 Ah (80% of nominal), and we use the providers' lifetime labels. The main specifications, $L^\ast=750$ (MATR/CLO) and $L^\ast=1900$ (HUST), are close to the median lifetimes, so that both classes are well represented; other values are studied in Section 4.5. Checkpoints are $\{20,30,\dots,100,120,140,160,180,200,250,300\}$ (MATR/CLO, $M=16$) and $\{20,30,\dots,100,150,200,300,400,500,600,800,1000\}$ (HUST, $M=17$). The data sets and the screening set-up are summarised in Table 1.

| Data set | Source | Cells | Protocols | Min. life | Median life | Max. life | $L^\ast$ | Bad share | Checkpoints | Split (%) |
|---|---|---|---|---|---|---|---|---|---|---|
| MATR | Severson et al. 2019 | 124 | 69 | 148 | 736 | 2,237 | 750 | 50.8 | 16 (20-300 cycles) | 50/25/25 |
| CLO | Attia et al. 2020 | 45 | 9 | 443 | 774 | 1,166 | 750 | 40.0 | 16 (20-300 cycles) | 50/25/25 |
| HUST | Ma et al. 2022 | 77 | 77 | 1,142 | 1875 | 2,689 | 1,900 | 51.9 | 17 (20-1000 cycles) | 40/30/30 |

: **Table 1.** Data sets and screening set-up. All cells are LiFePO~4~/graphite A123 APR18650M1A cells (1.1 Ah). Bad share: fraction of cells with cycle life below $L^\ast$. Split: training/calibration/test percentages per random split.


### 3.6 Experimental protocol and statistics

The cell is the unit of analysis. In each random split, training cells are drawn within strata defined by dataset and class (50% of MATR/CLO cells, 40% of HUST cells), and the remaining cells are divided uniformly at random into calibration and test cells (MATR/CLO 25%/25%, HUST 30%/30%). Drawing calibration and test cells from the same pool makes them exchangeable, as Proposition 1 requires (an earlier version that stratified the calibration and test sets separately produced slightly different group mixtures in the two sets and an error rate marginally above the theoretical value; it was discarded). Every experiment uses split seeds fixed before running; the main experiment uses 1,000 splits per dataset, other experiments 200–333 (Table S1). Metrics are the false-pass rate among bad test cells (FPR), the false-reject rate among good test cells (FRR), accuracy, the share of cells decided by the model before $\min(T,L^\ast)$, the mean number of cycles to a decision, and the fraction of cycling time saved relative to cycling every test cell to $\min(T,L^\ast)$. Validity is assessed by the mean FPR and FRR over splits with normal-approximation 95% confidence intervals (Monte-Carlo error) and the share of splits exceeding the nominal level. For efficiency comparisons each cell's time to decision is averaged over the splits in which it was a test cell; methods are compared on these per-cell averages with paired Wilcoxon signed-rank tests [42], Holm correction over comparators, matched-pairs rank-biserial correlation as effect size, and a cell-level bootstrap [43] (10,000 resamples) 95% CI for the difference in time saved. The experimental design, including all methods, metrics and tests, was fixed after a 100-split pilot (disjoint seeds) used only to detect data defects and estimate run time. Computations ran on four CPU cores with Python 3.13.18, scikit-learn 1.9.1 and PyTorch 2.15.0.


## 4 Results

### 4.1 Data and base predictors

![**Figure 1.** Cycle-life distributions of the two data sets and the specifications used in the main experiments. MATR/CLO: 124 cells of Severson et al. and 45 cells of the CLO validation batch of Attia et al.; HUST: 77 cells of Ma et al. Dashed lines: $L^\ast$ = 750 and 1,900 cycles; 48% and 52% of the cells, respectively, are bad.](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig2_lifetime_distributions.png){width=6.3in}

The specifications split both data sets roughly in half (Figure 1). The accuracy of the elastic-net predictor improved steadily with the number of observed cycles (Figure 2): on the test cells of all MATR/CLO splits, the mean absolute percentage error of the predicted cycle life fell from 28.6% at 20 cycles to 11.2% at 100 cycles and 7.1% at 300 cycles; on HUST it was 15.2%, 14.0% and 7.4% at 20, 100 and 1000 cycles. The error at 100 cycles on MATR/CLO is close to the 9.1% reported by Severson et al. for their full model on a fixed split [1], although our pooled data, random splits and feature set (no resistance features) differ from theirs. The score scale $s_k$ tracks the decrease of prediction error, which is what normalisation (Equation 2) exploits.

![**Figure 2.** Accuracy of the per-checkpoint elastic-net predictor on test cells, pooled over all splits of experiment E1: mean absolute percentage error (MAPE) of the predicted cycle life and the score scale $s_k$ (expressed as a percentage error, $10^{s_k}-1$).](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig3_base_model_accuracy.png){width=6.3in}

### 4.2 Validity of the screening decisions

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


The trajectory-calibrated rule met both error targets on both data sets (Figure 3, Table 2). On MATR/CLO its mean false-pass rate was 0.068 (95% CI 0.063–0.073) and its false-reject rate 0.080 (0.076–0.085); on HUST they were 0.068 (0.062–0.074) and 0.074 (0.067–0.080). The rates are below the nominal 0.10 because the maximum statistic is conservative when the scores of later checkpoints add little beyond earlier ones. As the theory predicts, the bound holds on average rather than in every split: the realised false-pass rate exceeded 0.10 in 26% (MATR/CLO) and 21% (HUST) of the splits, with about 20.0 and 11.9 bad cells, respectively, in the test sets' companion calibration sets. The single-checkpoint conformal rule, the proposed rule without normalisation and the lifetime-interval rule were also valid, as Proposition 1 (with $M=1$) and conformal theory imply.

The rules without a valid calibration behaved very differently. Using individually valid per-checkpoint thresholds sequentially (naive sequential) inflated the false-pass rate to 0.145 on MATR/CLO and 0.286 on HUST, and the false-reject rate to 0.158 and 0.214 — up to 2.9 times the nominal level. The Severson-style point rule at cycle 100 happened to stay below 0.10 on MATR/CLO (0.079 and 0.073) but not on HUST (0.237 and 0.367). The parametric rule with Gaussian thresholds on the same normalised scores was conservative on MATR/CLO (0.046, 0.043) and violated the false-reject target on HUST (0.136, upper confidence limit 0.143). Bonferroni calibration never passed or rejected a cell, because with about 20.0 bad and 22.0 good calibration cells the required order statistic at level $\alpha/M$ does not exist.

### 4.3 Testing time saved

![**Figure 4.** Share of test cells decided as a function of the number of cycles completed (all splits of E1). The proposed rule decides most cells within the first few checkpoints and sends the remainder to observation; the single-checkpoint rule decides at cycle 100; the naive sequential rule decides almost every cell early but violates the error targets; the dashed line is full observation to $\min(T,L^\ast)$.](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig5_decision_time.png){width=6.3in}

On MATR/CLO the proposed rule decided 86.7% of the test cells from their early cycles and saved 78.3% of the cycling needed to observe every cell to $\min(T,L^\ast)$ (mean 142 cycles per cell instead of 653); half of the cells were decided within 40 cycles and 78% by cycle 100 (Figure 4). On HUST, whose cells live longer and where the specification is 1,900 cycles, it decided 60.5% of the cells early and saved 50.7% (mean 857 instead of 1,739 cycles).

| Data set | Comparator | Cells | Proposed (cycles) | Comparator (cycles) | Saved diff. | CI low | CI high | p (Holm) | r |
|---|---|---|---|---|---|---|---|---|---|
| MATR+CLO | Bonferroni sequential conformal | 169 | 142 | 653 | 78.3 | 75.6 | 81.0 | 1.2e-28 | -1.00 |
| MATR+CLO | Parametric/Bayesian threshold | 169 | 142 | 147 | 0.8 | -1.4 | 3.2 | 0.0015 | 0.31 |
| MATR+CLO | Conformal lifetime interval (full-lifetime calibration) | 169 | 142 | 298 | 24.0 | 20.3 | 27.7 | 1e-24 | -0.92 |
| MATR+CLO | Naive sequential conformal | 169 | 142 | 30 | -17.1 | -19.7 | -14.6 | 1.2e-28 | 1.00 |
| MATR+CLO | Point prediction at cycle 100 | 169 | 142 | 100 | -6.4 | -9.3 | -3.5 | 0.16 | 0.15 |
| MATR+CLO | Single checkpoint (cycle 100) conformal | 169 | 142 | 133 | -1.3 | -3.4 | 0.7 | 0.36 | -0.08 |
| MATR+CLO | Proposed without score normalisation | 169 | 142 | 204 | 9.5 | 8.0 | 11.0 | 6.5e-25 | -0.93 |
| HUST | Bonferroni sequential conformal | 77 | 854 | 1739 | 50.9 | 45.8 | 56.0 | 1.7e-13 | -1.00 |
| HUST | Parametric/Bayesian threshold | 77 | 854 | 536 | -18.3 | -20.2 | -16.4 | 1.7e-13 | 1.00 |
| HUST | Conformal lifetime interval (full-lifetime calibration) | 77 | 854 | 1396 | 31.2 | 28.8 | 33.6 | 1.7e-13 | -1.00 |
| HUST | Naive sequential conformal | 77 | 854 | 118 | -42.3 | -46.9 | -37.7 | 1.7e-13 | 1.00 |
| HUST | Point prediction at cycle 100 | 77 | 854 | 100 | -43.3 | -48.6 | -38.0 | 1.7e-13 | 1.00 |
| HUST | Single checkpoint (cycle 100) conformal | 77 | 854 | 1070 | 12.4 | 9.2 | 15.7 | 1.2e-08 | -0.76 |
| HUST | Proposed without score normalisation | 77 | 854 | 906 | 3.0 | 1.5 | 4.5 | 0.00099 | -0.43 |

: **Table 3.** Cell-level paired comparison of the time to decision of the proposed rule with each comparator (E1). Each cell's time to decision is averaged over the splits in which it was a test cell. "Saved diff." = time saved by the proposed rule minus that of the comparator (percentage points; positive favours the proposed rule) with a cell-bootstrap 95% CI; Wilcoxon signed-rank test with Holm correction; $r$ = matched-pairs rank-biserial correlation of the time difference (negative = proposed rule faster).


Among the valid rules, the proposed rule saved more cycling than the lifetime-interval rule on both data sets (by 24.0 and 31.2 percentage points; Holm-adjusted $p$ = 1.0 × 10^-24^ and 1.7 × 10^-13^; Table 3), and more than the unnormalised variant (by 9.5 and 3.0 points). Against the single-checkpoint rule the result depended on the data set: on HUST the proposed rule saved 12.4 points more (95% CI 9.2 to 15.7; $p$ = 1.2 × 10^-8^; $r$ = -0.76), whereas on MATR/CLO the difference was -1.3 points (95% CI -3.4 to 0.7; $p$ = 0.36), i.e. not significant. The rules that saved more time than the proposed one — naive sequential, point prediction and, on HUST, the parametric rule — did so by violating at least one error target on at least one data set.

**Truncated calibration.** Because the proposed thresholds need only each calibration cell's class, the calibration campaign ended after at most $L^\ast$ cycles: a mean of 750 wall-clock cycles per split on MATR/CLO versus 1,958 for the full-lifetime calibration of the interval rule (factor 2.61), and 1,900 versus 2,630 on HUST (factor 1.38). Total calibration cell-cycles fell by factors of 1.22 and 1.09.

### 4.4 Base predictors and checkpoint grid

**Other base predictors (E2).** The guarantee does not depend on the base predictor, and the data agree (Table S4). With logistic regression trained on truncated cells, gradient boosting, random forests, Gaussian-process regression and a one-dimensional CNN, the proposed rule's mean false-pass rate ranged from 0.066 to 0.075 on MATR/CLO and from 0.064 to 0.079 on HUST, and its false-reject rate from 0.072 to 0.089 and from 0.070 to 0.113. The one mean above 0.10 — the CNN on HUST, 0.113 (95% CI 0.060–0.166) — comes from only 30 splits and is consistent with the nominal level. The naive sequential rule exceeded both targets with every predictor (false-pass rate 0.145–0.149 on MATR/CLO and 0.240–0.343 on HUST), and the parametric rule was unsafe with several predictors (HUST Gaussian process: 0.274 and 0.362; HUST CNN: 0.183 and 0.250). The predictor mattered for efficiency: on MATR/CLO the saved cycling ranged from 67.5% (logistic regression on truncated training cells) to 80.5% (random forest), against 78.3% for the elastic net; on HUST from 40.0% to 54.6% against 50.7%. Truncating the training cells as well as the calibration cells therefore keeps the guarantee but costs about ten percentage points of savings.

![**Figure 5.** Checkpoint-grid ablation (E3, 200 splits per data set, elastic net): cycling time saved by the proposed rule, its unnormalised variant and the naive sequential rule for each grid. Grids with a single checkpoint make the three rules identical. The naive rule's savings are not comparable: it violates the error targets on HUST for every grid with more than one checkpoint and on MATR/CLO for the dense grids.](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig7_ablation_checkpoint_grid.png){width=6.3in}

**Checkpoint grid (E3).** With a single checkpoint the three rules coincide and are valid; every additional look inflated the naive rule's error and left the proposed rule valid (Figure 5, Table S6). On HUST the naive false-pass rate rose from 0.085 (one checkpoint) to 0.133 (two), 0.175 (four) and 0.289 (all 17), while the proposed rule stayed between 0.069 and 0.085. The grid affected efficiency more than validity. A sparse grid saved the most of all grids tested on MATR/CLO (84.3% with checkpoints 50, 100, 200 and 300, versus 79.4% with all 16), and a well-chosen single checkpoint can beat the full grid: on HUST a single look at cycle 300 saved 61.5%, compared with 52.6% for all 17 checkpoints, but a single look at cycle 100 or 1000 saved only 40.6% or 34.8%. The best of the single checkpoints tested differed between the data sets (cycle 50 on MATR/CLO, cycle 300 on HUST) and could not have been chosen without the data used for evaluation. Score normalisation mattered most with dense grids (MATR/CLO, all 16 checkpoints: 79.4% with and 70.8% without normalisation), where unnormalised early scores, whose spread is large, dominate the maximum.

### 4.5 Calibration-set size, error levels and training-conditional control

![**Figure 6.** Robustness (E4, 200 splits per setting): the larger of the mean false-pass and false-reject rates as a function of the calibration fraction, the training fraction, and Gaussian feature noise (in units of each feature's standard deviation) added to calibration and test cells or to test cells only. Dashed line: nominal level 0.10.](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig8_robustness.png){width=6.3in}

**Calibration and training size (E4).** The proposed rule stayed valid for every calibration and training fraction (Figure 6, Table S7). Small calibration sets did not break the guarantee but made the rule abstain: with about 8.3 bad calibration cells (MATR/CLO, calibration fraction 0.10) the order statistic needed to pass a cell often did not exist, so no cell was passed in 55% of the splits and the saving fell to 41.1% (from 80.2% at 0.25); on HUST with about 7.9 bad calibration cells the saving was 19.7%. Smaller training sets reduced the saving moderately (MATR/CLO: 70.4% with 20% of the cells for training, 80.2% with 50%). The parametric rule violated the false-reject target on HUST for every calibration fraction (≥ 0.127).

![**Figure 7.** Sensitivity to the specification (E7, proposed rule, $\alpha=\beta=0.10$, 200 splits): mean false-pass and false-reject rates and cycling time saved for three values of $L^\ast$ per data set.](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig9_sensitivity_Lstar.png){width=6.3in}

**Specification and error levels (E7).** Moving $L^\ast$ changes the class balance (Figure 7, Table S10). On MATR/CLO the rule stayed valid for $L^\ast$ = 550, 750 and 900 cycles (savings 77.5%, 79.4% and 69.7%). On HUST, with $L^\ast$ = 1,600 only about 5.6 calibration cells were bad, too few to pass any cell at $\alpha$ = 0.10 (no pass in 98% of the splits), and with $L^\ast$ = 2,200 only about 5.8 were good; the rule remained valid but saved only 15.5% and 20.0%. The parametric rule, by contrast, violated one of the targets at both alternative specifications on HUST (false-pass rate 0.322 at 1,600; false-reject rate 0.298 at 2,200). Stricter error levels need more calibration cells: at $\alpha=\beta=0.05$ the rule decided nothing early on HUST (about 12.0 cells per class; at least 19 are needed) and saved 53.8% on MATR/CLO with error rates 0.034 and 0.025. At $\alpha=\beta=0.20$ the rule was valid on both data sets (0.136/0.145 and 0.141/0.164) and saved 94.2% and 75.9%.

**Training-conditional control (E10).** The marginal guarantee allows the error of a particular calibration set to exceed the target: the realised false-pass rate of the proposed rule was above 0.10 in 28% of the MATR/CLO splits and 24% of the HUST splits (Table S12), somewhat below the analytic probabilities for continuous scores (Table S13; e.g. 39% for 20 cells), because the trajectory maximum is conservative. The PAC variant, which chooses the rank so that the conditional error exceeds $\alpha$ with probability at most 0.1, reduced these shares to 4% and 0%, but at a high price: with the default calibration sets (about 20.0 bad cells on MATR/CLO and 11.9 on HUST, fewer than the 22 required) it saved 28.1% on MATR/CLO and nothing on HUST. With enlarged calibration sets (about 36.8 and 20.2 bad cells) it saved 56.3% and 6.3%, against 80.8% and 49.2% for the marginal rule.

### 4.6 Distribution shift

![**Figure 8.** Batch and laboratory shift (E5, 200 splits per scenario): mean false-pass (left) and false-reject (right) rates with 95% confidence intervals. Batch shift: models trained and calibrated on MATR batches 1–2 and applied to batch 3 or the CLO batch (b4), either with source calibration or after recalibration with $n$ = 20 or 30 target cells cycled to $L^\ast$. Laboratory shift: capacity-trajectory features; HUST test cells screened with a model trained on MATR/CLO or on HUST, both calibrated with HUST cells. Dashed line: nominal level 0.10.](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig10_distribution_shift.png){width=6.3in}

**Batch shift (E5).** When a model trained and calibrated on the first two MATR batches was used to screen a later batch, the guarantee failed, as expected when calibration and test cells are not exchangeable (Figure 8, Table S8). The proposed rule falsely rejected 0.480 of the good cells of batch 3 and 0.597 of those of the CLO batch, and the single-checkpoint rule falsely passed 0.227 and 0.479 of the bad cells; every rule violated at least one target on at least one batch. Recalibration with target cells cycled only to $L^\ast$, keeping the source model, restored validity: with 30 CLO cells the error rates were 0.075 and 0.046, with a saving of 26.8%. With 20 target cells, or for batch 3, which contains few bad cells at this specification (about 2.0 among 20), the rule remained valid by passing no cell early and saved little (6.0–9.9%). The parametric rule, recalibrated in the same way, kept a false-reject rate above 0.79.

**Laboratory shift (E5) and unseen protocols (E9).** A model trained on MATR/CLO capacity trajectories and calibrated with HUST cells screened HUST cells validly (0.080 and 0.070), saving 23.9% compared with 47.0% when the model was trained on HUST cells as well; the point-prediction rule was invalid in both cases (0.519 and 0.605 with the MATR model). When whole charging protocols were held out — 78 protocol groups of MATR/CLO assigned to training, calibration or test — the proposed rule kept its targets (0.073, 95% CI 0.059–0.087; 0.088, 0.074–0.101) and saved 75.1%, while the naive rule again exceeded both (0.168 and 0.182; Table S11). Because protocol groups were assigned to calibration and test at random, exchangeability holds at the level of protocols, and the guarantee held although no test protocol appeared among the training or calibration cells. Calibration cells therefore have to come from the population being screened, but that population can span protocols not seen in training.

### 4.7 Measurement noise and computational cost

**Noise (E4).** Gaussian noise added to the features of calibration and test cells alike left the proposed rule valid at every level up to one feature standard deviation and only reduced the saving (MATR/CLO: 78.8% at 0.1 SD to 36.0% at 1 SD; HUST: 46.4% to 17.3%), whereas the parametric rule became invalid already at 0.25 SD (Figure 6). Noise added to the test cells only — a calibration set measured on a cleaner instrument than the cells screened — violates exchangeability, and it hurt the proposed rule more than the single-checkpoint rule, because the maximum over many noisy checkpoints is more likely to cross a threshold: at 0.25 SD the false-pass rates were 0.126 and 0.107 on MATR/CLO and 0.275 and 0.139 on HUST. Calibration and screening must use the same measurement chain.

**Cost (E6).** Fitting the elastic-net predictors for all checkpoints of one split took 1.7 s (MATR/CLO) and 2.6 s (HUST) on four CPU cores, and the slowest predictor, the random forest, 19.1 s and 18.5 s (Table S9, Figure S4). The calibration step itself took 0.603 ms even with 4,000 calibration cells, and screening 1,000 cells about 22.17 ms. The procedure adds no measurable cost to an existing prediction pipeline.

### 4.8 Error analysis

![**Figure 9.** Error frequency of the proposed rule for each cell, across the splits in which the cell was a test cell (E1), against the distance of its cycle life from the specification, $\log_{10}(T/L^\ast)$. Bad cells (left) can only be falsely passed; good cells (right) can only be falsely rejected.](/home/user/p_c1_3/Target_Journal_Submission/figures/Fig11_error_analysis.png){width=6.3in}

Errors concentrated near the specification (Figure 9): the Spearman correlation between $|\log_{10}(T/L^\ast)|$ and a cell's error frequency was -0.45 on MATR/CLO ($p$ = 1.2 × 10^-9^) and -0.44 on HUST ($p$ = 5.2 × 10^-5^). Cells within 0.05 decades of $L^\ast$ (about ±12% in cycle life) had a mean error frequency of 0.189 on MATR/CLO compared with 0.028 for cells more than 0.1 decades away, and they accounted for 62% of all errors. Errors far from $L^\ast$ came from a few cells whose early-cycle behaviour was not representative of their lifetime (Table S16): the shortest-lived MATR cell (148 cycles) failed abruptly after early cycles that resembled those of ordinary cells and was falsely passed in most splits in which it was tested, and one long-lived cell (1,315 cycles) was falsely rejected in most splits because its early capacity-difference signature resembled that of short-lived cells. No early-cycle screening rule can classify such cells correctly from these features; the guarantee bounds how often such cells are mis-screened in aggregate but cannot identify them. On HUST the most frequent errors involved cells within about 6% of $L^\ast$ (Table S17).


## 5 Discussion

**Repeated looks must be paid for.** The most consequential result for practice is the behaviour of the naive sequential rule. Each of its per-checkpoint thresholds is a valid conformal threshold, and a practitioner who re-evaluates a prediction every few cycles and stops at the first confident call is implicitly using it. Its error rates were 0.145 (false pass) and 0.158 (false reject) on MATR/CLO and 0.286 and 0.214 on HUST at a nominal 0.10 — the optional-stopping inflation known from sequential analysis [17,18] appears in battery screening at a practically relevant scale. Calibrating on the maximum over checkpoints removes this inflation at a cost that the data show to be modest, because scores of the same cell at successive checkpoints are strongly dependent; Bonferroni's union bound ignores that dependence and, with tens of calibration cells, never reached a decision.

**Truncated campaigns.** Because the class-conditional thresholds depend only on whether each calibration cell reached $L^\ast$, calibration cells can be retired at $\min(T,L^\ast)$. In our MATR/CLO splits this shortened the calibration campaign from 1,958 to 750 cycles of wall-clock time (the longest-running calibration cell), a factor of 2.61, and on HUST from 2,630 to 1,900 cycles. The lifetime-interval rule, which needs cells cycled to end of life, was also less efficient, because its marginal guarantee covers both tails of the lifetime distribution rather than the side that matters for each class. When the base predictor itself is a classifier of $Z$, training cells can be truncated as well; this kept the error guarantees but cost about ten percentage points of savings (Section 4.4), so the choice is between a shorter preparatory campaign and faster screening.

**One checkpoint or many?** On MATR/CLO a single, well-chosen checkpoint at cycle 100 was competitive with the sequential rule, while on HUST, whose cells live longer and whose informative checkpoints come later, the sequential rule saved clearly more cycling (Section 4.3). The sequential rule decided most clear-cut cells long before cycle 100 (median time to decision 40 cycles on MATR/CLO) but sent more borderline cells to full observation. The single-checkpoint rule requires choosing the checkpoint in advance; the grid ablation (Section 4.4) shows that the best fixed checkpoint differs between datasets (cycle 50 on MATR/CLO, cycle 300 on HUST), which a sequential rule does not need to know. A well-chosen single checkpoint can save more than a dense grid (61.5% versus 52.6% on HUST), but only with hindsight; a poorly chosen one saves much less (34.8% at cycle 1000). In practice, a sparse grid that includes the checkpoint at which early-cycle features become informative is a reasonable default.

**Model-based uncertainty is not a substitute.** The parametric rule with Gaussian thresholds on the same normalised scores was conservative on MATR/CLO but exceeded the false-reject target on HUST, and the point-prediction rule of Severson et al. had no control at all (0.237 and 0.367 on HUST). The same model, used with different decision thresholds, can therefore be either wasteful or unsafe depending on the data set; rank-based calibration adapts to the data at hand.

**What the guarantee does and does not mean.** Proposition 1 bounds error *rates* averaged over calibration and test draws from an exchangeable population. Three consequences matter for users. (i) For a given calibration set the conditional error can exceed the target: with 20 bad calibration cells, the probability that the conditional false-pass probability exceeds 0.10 is 39% (Table S13); a training-conditional (PAC) variant removes this at the price of needing at least 22 calibration cells per class (Section 4.5). (ii) The guarantee is class-conditional, not cell-conditional: cells whose lifetime is close to $L^\ast$ carry most of the errors (Section 4.8), as expected for any screening rule. (iii) Exchangeability is an assumption about how the calibration cells were obtained; it is plausible for cells drawn from the same production lot and measured with the same equipment. In our experiments the guarantee failed when a later batch was screened with thresholds calibrated on earlier batches, and recalibration with 30 target cells cycled only to $L^\ast$ restored it; a model trained in one laboratory and calibrated in the other was valid, and so were splits in which test protocols were absent from training and calibration (Section 4.6). Noise affecting only the screened cells also broke the guarantee (Section 4.7), so calibration and screening must share the measurement chain.

**Recommended workflow.** (1) Fix $L^\ast$, $\alpha$, $\beta$ and the checkpoint grid before testing. (2) Train a base predictor on any available historical cells (full-lifetime or truncated). (3) Cycle a calibration set of at least ten bad and ten good cells (preferably more than 22 of each for training-conditional control) from the population to be screened, to $\min(T,L^\ast)$ only. (4) Screen new cells sequentially with the trajectory-calibrated thresholds. (5) Recalibrate whenever the cell population, production batch or measurement equipment changes.

## 6 Limitations

* **One chemistry.** All 246 cells are LiFePO~4~/graphite 18650 cells of one type, from two laboratories. We tried to add cells of other chemistries, but the NCA/NCM data of Zhu et al. (Zenodo) and the NMC data of RWTH Aachen were not reachable from our computing environment (HTTP 403 and an interactive browser challenge), and the Sandia data available through BatteryArchive involve partial-depth cycling with many cells not reaching end of life. The guarantee itself does not depend on chemistry, but the efficiency results may.
* **Exchangeability and shift.** The guarantees require the calibration cells to be exchangeable with the cells being screened, and Sections 4.6 and 4.7 show that they fail under batch shift without recalibration and when screened cells are measured more noisily than calibration cells.
* **Marginal, class-conditional guarantee** (see Section 5); conditional error can exceed the target for a particular calibration set unless the PAC variant is used.
* **Retrospective evaluation.** Results come from repeated random splits of finite public data sets, not from a prospective screening campaign; the splits re-use the same cells, so split-to-split variation understates the variation across independent cell populations.
* **Cost model.** Time saved is measured in cell-cycles relative to cycling each cell to $\min(T,L^\ast)$; channel scheduling, rest periods and reference performance tests are not modelled.
* **Lifetime labels** are those of the data providers (first cycle at 80% of nominal capacity); other end-of-life definitions change the class labels [31].

## 7 Conclusions

Early cycle-life predictions are routinely used to make go/no-go decisions, but the error rate of those decisions is rarely controlled, and the common practice of re-checking predictions as cycling proceeds silently inflates it. We showed that calibrating pass and reject thresholds on the maximum over checkpoints of normalised model scores gives finite-sample, distribution-free bounds on the false-pass and false-reject probabilities that hold under any stopping time, and that the calibration needs cells cycled only to the specification. On 246 commercial LiFePO~4~/graphite cells from two laboratories, the rule met its error targets with 0.10 nominal levels while cutting cycling by 78.3% (MATR/CLO) and 50.7% (HUST) relative to cycling every cell to the specification, whereas naive sequential use of valid per-checkpoint thresholds exceeded the targets by up to a factor of 2.9. The procedure is a thin layer on top of any lifetime predictor, costs milliseconds to run, and is released with code that reproduces every result.

## Acknowledgments

[To be completed by the authors.] We thank the providers of the public data sets used in this study: the Toyota Research Institute, Massachusetts Institute of Technology and Stanford University teams who released the MATR/CLO data (data.matr.io), and Ma et al. (Huazhong University of Science and Technology) for the HUST data.

## Author Contributions (CRediT)

[To be completed by the authors, e.g.: Conceptualization; Methodology; Software; Validation; Formal analysis; Investigation; Data curation; Writing – original draft; Writing – review & editing; Visualization.]

## Conflict of Interest Statement

[To be confirmed by the authors.] The authors declare no conflicts of interest.

## Funding

[To be completed by the authors.]

## Data Availability Statement

The raw data analysed in this study are openly available: MATR/CLO cycling data at https://data.matr.io/1/ (Severson et al. [1]; Attia et al. [2]) and HUST data at Mendeley Data, https://doi.org/10.17632/nsc7hnsg4s.2 (Ma et al. [7]). The checkpoint feature tables derived from them, all split-level results, statistics, tables and figures, and the complete code that regenerates them (`python run_all.py --mode full`) are available at [repository URL / archival DOI to be inserted at submission].

## Ethics Statement

This study used only previously published battery cycling data; it involved no human participants, animals or personal data.

## Use of Generative AI

[Required by Wiley policy — to be completed accurately by the authors.] The study design, code, analyses and draft text were produced with the assistance of a generative-AI agent. [State the tool, the tasks it performed, and the human verification of code, results, citations and text.] The authors take full responsibility for the content.


## References

[1] K. A. Severson, P. M. Attia, N. Jin, N. Perkins, B. Jiang, Z. Yang, M. H. Chen, M. Aykol, P. K. Herring, D. Fraggedakis, M. Z. Bazant, S. J. Harris, W. C. Chueh, R. D. Braatz, Data-driven prediction of battery cycle life before capacity degradation, *Nature Energy* 2019, 4, 383-391. https://doi.org/10.1038/s41560-019-0356-8

[2] P. M. Attia, A. Grover, N. Jin, K. A. Severson, T. M. Markov, Y. H. Liao, M. H. Chen, B. Cheong, N. Perkins, Z. Yang, P. K. Herring, M. Aykol, S. J. Harris, R. D. Braatz, S. Ermon, W. C. Chueh, Closed-loop optimization of fast-charging protocols for batteries with machine learning, *Nature* 2020, 578, 397-402. https://doi.org/10.1038/s41586-020-1994-5

[3] B. Jiang, W. E. Gent, F. Mohr, S. Das, M. D. Berliner, M. Forsuelo, H. Zhao, P. M. Attia, A. Grover, P. K. Herring, M. Z. Bazant, S. J. Harris, S. Ermon, W. C. Chueh, R. D. Braatz, Bayesian learning for rapid prediction of lithium-ion battery-cycling protocols, *Joule* 2021, 5, 3187-3203. https://doi.org/10.1016/j.joule.2021.10.010

[4] P. M. Attia, K. A. Severson, J. D. Witmer, Statistical Learning for Accurate and Interpretable Battery Lifetime Prediction, *Journal of The Electrochemical Society* 2021, 168, 090547. https://doi.org/10.1149/1945-7111/ac2704

[5] P. Fermín-Cueto, E. McTurk, M. Allerhand, E. Medina-Lopez, M. F. Anjos, J. Sylvester, G. dos Reis, Identification and machine learning prediction of knee-point and knee-onset in capacity degradation curves of lithium-ion cells, *Energy and AI* 2020, 1, 100006. https://doi.org/10.1016/j.egyai.2020.100006

[6] P. M. Attia, A. Bills, F. Brosa Planella, P. Dechent, G. dos Reis, M. Dubarry, P. Gasper, R. Gilchrist, S. Greenbank, D. Howey, O. Liu, E. Khoo, Y. Preger, A. Soni, S. Sripad, A. G. Stefanopoulou, V. Sulzer, Review—“Knees” in Lithium-Ion Battery Aging Trajectories, *Journal of The Electrochemical Society* 2022, 169, 060517. https://doi.org/10.1149/1945-7111/ac6d13

[7] G. Ma, S. Xu, B. Jiang, C. Cheng, X. Yang, Y. Shen, T. Yang, Y. Huang, H. Ding, Y. Yuan, Real-time personalized health status prediction of lithium-ion batteries using deep transfer learning, *Energy &amp; Environmental Science* 2022, 15, 4083-4094. https://doi.org/10.1039/d2ee01676a

[8] N. Guo, S. Chen, J. Tao, Y. Liu, J. Wan, X. Li, Semi-supervised learning for explainable few-shot battery lifetime prediction, *Joule* 2024, 8, 1820-1836. https://doi.org/10.1016/j.joule.2024.02.020

[9] X. Zhai, G. Liu, T. Lu, S. Chen, Y. Liu, J. Wan, X. Li, Transforming waste to value: Enhancing battery lifetime prediction using incomplete data samples, *Journal of Energy Chemistry* 2025, 106, 642-649. https://doi.org/10.1016/j.jechem.2025.03.011

[10] F. Wang, Z. Zhai, Z. Zhao, Y. Di, X. Chen, Physics-informed neural network for lithium-ion battery degradation stable modeling and prognosis, *Nature Communications* 2024, 15, 4332. https://doi.org/10.1038/s41467-024-48779-z

[11] H. Zhang, X. Gui, S. Zheng, Z. Lu, Y. Li, J. Bian, BatteryML:An Open-source platform for Machine Learning on Battery Degradation, *arXiv* 2023. arXiv:2310.14714

[12] X. Hu, L. Xu, X. Lin, M. Pecht, Battery Lifetime Prognostics, *Joule* 2020, 4, 310-346. https://doi.org/10.1016/j.joule.2019.11.018

[13] V. Sulzer, P. Mohtat, A. Aitio, S. Lee, Y. T. Yeh, F. Steinbacher, M. U. Khan, J. W. Lee, J. B. Siegel, A. G. Stefanopoulou, D. A. Howey, The challenge and opportunity of battery lifetime prediction from field data, *Joule* 2021, 5, 1934-1955. https://doi.org/10.1016/j.joule.2021.06.005

[14] M. F. Sulaima, S. Arora, R. Frischer, H. Namazi, Physics‐Informed Artificial Intelligence for Battery Degradation, Aging, and Lifetime Prediction, *Battery Energy* 2026, 5, e70136. https://doi.org/10.1002/bte2.70136

[15] J. Hu, L. Wu, Early Uncertainty Quantification Prediction of Lithium-Ion Battery Remaining Useful Life With Transformer Ensemble Model, *IEEE Transactions on Transportation Electrification* 2024, 10, 8618-8629. https://doi.org/10.1109/tte.2024.3354302

[16] Y. Ke, Y. Jiang, R. Zhu, W. Peng, X. Tan, Early Prediction of Knee Point and Knee Capacity for Fast-Charging Lithium-Ion Battery With Uncertainty Quantification and Calibration, *IEEE Transactions on Transportation Electrification* 2024, 10, 2873-2885. https://doi.org/10.1109/tte.2023.3304670

[17] A. Wald, Sequential Tests of Statistical Hypotheses, *The Annals of Mathematical Statistics* 1945, 16, 117-186. https://doi.org/10.1214/aoms/1177731118

[18] S. R. Howard, A. Ramdas, J. McAuliffe, J. Sekhon, Time-uniform, nonparametric, nonasymptotic confidence sequences, *The Annals of Statistics* 2021, 49, 1055-1080. https://doi.org/10.1214/20-aos1991

[19] , Algorithmic Learning in a Random World, *Springer-Verlag* 2005. https://doi.org/10.1007/b106715

[20] J. Lei, M. G’Sell, A. Rinaldo, R. J. Tibshirani, L. Wasserman, Distribution-Free Predictive Inference for Regression, *Journal of the American Statistical Association* 2018, 113, 1094-1111. https://doi.org/10.1080/01621459.2017.1307116

[21] A. N. Angelopoulos, S. Bates, Conformal Prediction: A Gentle Introduction, *Foundations and Trends® in Machine Learning* 2023, 16, 494-591. https://doi.org/10.1561/2200000101

[22] A. Weng, P. Mohtat, P. M. Attia, V. Sulzer, S. Lee, G. Less, A. Stefanopoulou, Predicting the impact of formation protocols on battery lifetime immediately after manufacturing, *Joule* 2021, 5, 2971-2992. https://doi.org/10.1016/j.joule.2021.09.015

[23] Y. Zhang, Q. Tang, Y. Zhang, J. Wang, U. Stimming, A. A. Lee, Identifying degradation patterns of lithium ion batteries from impedance spectroscopy using machine learning, *Nature Communications* 2020, 11, 1706. https://doi.org/10.1038/s41467-020-15235-7

[24] G. dos Reis, C. Strange, M. Yadav, S. Li, Lithium-ion battery data and where to find it, *Energy and AI* 2021, 5, 100081. https://doi.org/10.1016/j.egyai.2021.100081

[25] F. Xiao, W. Yang, Y. Ding, X. Li, K. Zhang, J. Liu, A CNN‐LSTM Method Based on Voltage Deviation for Predicting the State of Health of Lithium‐Ion Batteries, *Battery Energy* 2024, 4, e20240036. https://doi.org/10.1002/bte2.20240036

[26] Z. Lyu, X. Wei, L. Wu, C. Liu, Transfer Learning‐Based Data‐Fusion Model Framework for State of Health Estimation of Power Battery Packs, *Battery Energy* 2025, 4, e70011. https://doi.org/10.1002/bte2.70011

[27] J. Kee, S. Lee, J. Hwang, S. Yoon, S. Han, D. Kim, Degradation‐Informed Temperature Analysis for Cycle Life Prediction of LiFePO 4 Batteries, *Battery Energy* 2026, 5, e70124. https://doi.org/10.1002/bte2.70124

[28] Y. Romano, E. Patterson, E. J. Candès, Conformalized Quantile Regression, *arXiv* 2019. arXiv:1905.03222

[29] S. F. d. Silva, M. F. Ozkan, F. E. Idrissi, M. Canova, Conformalized Transfer Learning for Li-ion Battery State of Health Forecasting under Manufacturing and Usage Variability, *arXiv* 2026. arXiv:2603.24475

[30] X. Liu, From fleet trajectories to single-cell promises: hierarchically weighted conformal prediction for battery SOH monitoring, *arXiv* 2026. arXiv:2610.41696

[31] J. Li, W. Li, T. Li, Endpoint definitions and censoring in battery lifetime prediction across sources, *Springer Science and Business Media LLC* 2026. https://doi.org/10.21203/rs.3.rs-11508938/v1

[32] X. Tong, Y. Feng, J. J. Li, Neyman-Pearson classification algorithms and NP receiver operating characteristics, *Science Advances* 2018, 4, eaao1659. https://doi.org/10.1126/sciadv.aao1659

[33] M. Sadinle, J. Lei, L. Wasserman, Least Ambiguous Set-Valued Classifiers With Bounded Error Levels, *Journal of the American Statistical Association* 2018, 114, 223-234. https://doi.org/10.1080/01621459.2017.1395341

[34] E. Candès, L. Lei, Z. Ren, Conformalized survival analysis, *Journal of the Royal Statistical Society Series B: Statistical Methodology* 2023, 85, 24-45. https://doi.org/10.1093/jrsssb/qkac004

[35] Y. Gui, R. Hore, Z. Ren, R. F. Barber, Conformalized survival analysis with adaptive cutoffs, *arXiv* 2022. arXiv:2211.01227

[36] M. Sesia, V. Svetnik, Doubly Robust Conformalized Survival Analysis with Right-Censored Data, *arXiv* 2024. arXiv:2412.09729

[37] Y. Jin, E. J. Candès, Selection by Prediction with Conformal p-values, *arXiv* 2022. arXiv:2210.01408

[38] M. Jazbec, P. Forré, S. Mandt, D. Zhang, E. Nalisnick, Early-Exit Neural Networks with Nested Prediction Sets, *arXiv* 2023. arXiv:2311.05931

[39] H. Zou, T. Hastie, Regularization and Variable Selection Via the Elastic Net, *Journal of the Royal Statistical Society Series B: Statistical Methodology* 2005, 67, 301-320. https://doi.org/10.1111/j.1467-9868.2005.00503.x

[40] F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, M. Blondel, A. Müller, J. Nothman, G. Louppe, P. Prettenhofer, R. Weiss, V. Dubourg, J. Vanderplas, A. Passos, D. Cournapeau, M. Brucher, M. Perrot, É. Duchesnay, Scikit-learn: Machine Learning in Python, *arXiv* 2012. arXiv:1201.0490

[41] C. E. Rasmussen, C. K. I. Williams, Gaussian Processes for Machine Learning, *The MIT Press* 2005. https://doi.org/10.7551/mitpress/3206.001.0001

[42] F. Wilcoxon, Individual Comparisons by Ranking Methods, *Biometrics Bulletin* 1945, 1, 80. https://doi.org/10.2307/3001968

[43] B. Efron, Bootstrap Methods: Another Look at the Jackknife, *The Annals of Statistics* 1979, 7, 1-26. https://doi.org/10.1214/aos/1176344552