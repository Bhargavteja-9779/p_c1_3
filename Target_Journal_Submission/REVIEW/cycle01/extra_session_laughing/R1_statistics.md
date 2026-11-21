# Review R1 (statistics / conformal prediction), cycle 01

Manuscript: "Stopping Cycle-Life Tests Early With Guaranteed Error Rates: Distribution-Free Sequential Screening of Lithium-Ion Cells From Truncated Test Campaigns" (Battery Energy).
Line numbers refer to `manuscript/Draft_Manuscript.md`.

## Summary

The paper calibrates pass and reject thresholds as class-conditional split-conformal order statistics of each calibration cell's maximum normalised score over the checkpoints where it is alive (Eq. 3–4). Proposition 1 says that any rule passing only when S > lambda-hat (rejecting only when S < -mu-hat) has false-pass probability <= alpha and false-reject probability <= beta under any stopping time. Calibration cells need only be cycled to min(T, L*).

**Theory.** Proposition 1 and its proof are correct. The containment argument {passed at some checkpoint} ⊆ {P_new > P_(r0)} is valid. The rank bound (n0+1-r0)/(n0+1) <= alpha is right. Ties are handled conservatively by the strict inequality, and bad cells that die before k1 are correctly coded as -inf. The limits n0 >= (1-alpha)/alpha (9 cells) and n0 < M/alpha - 1 (159 cells for Bonferroni, M = 16) are also correct.

**Code.** The code matches the Methods:
- `conformal_upper` uses r = ceil((n+1)·level) and returns +inf when r > n. I checked n = 1..400 for alpha in {0.1, 0.05, 0.2, 0.1/16, 0.1/17}: there are no floating-point rounding errors in the ceiling.
- `simulate` decides with strict inequalities, treats a cell as alive at k_m when T > k_m, checks pass before reject, and sends undecided cells to observation.
- The "never decides" case (+inf / -inf thresholds) works as described.

**Empirical check.** Using the stored E1 test-cell scores, I recomputed P(P_new > lambda-hat | bad) directly:

| Data set | Bad side: empirical | Bad side: exact level | Good side: empirical | Good side: exact level |
|---|---|---|---|---|
| MATR/CLO | 0.082 | 0.081 | 0.086 | 0.084 |
| HUST | 0.072 | 0.076 | 0.078 | 0.078 |

The exact level is E[(n0+1-r0)/(n0+1)] over the realised calibration class sizes. The implementation therefore does exactly what the theory says.

**Problems.** The problems are in how the results are interpreted and reported, not in the method:
- The manuscript's explanation of why realised error rates fall below 0.10 is wrong.
- The comparison with the analytic conditional-error table (E10 vs Table S13) compares different quantities.
- The confidence intervals cover only Monte-Carlo error but are used for population-level statements.
- In Table 3, the test and the effect estimate measure different things and sometimes point in opposite directions.
- The lifetime-interval baseline is called "valid" in a sense that conformal theory does not give.
- The batch-shift "restored validity" claim rests partly on vacuous cases with one or two bad cells.

## Recommendation

**Minor revision.** The method, the proof and the code are sound, and the headline numbers reproduce from the raw CSVs. Issues 1–6 must be fixed before submission, but all of them can be fixed by rewriting text and re-analysing the existing result files. No new experiments are needed.

## Issues

### 1. (Major) The explanation of why error rates are below nominal is incorrect
**Location:** Section 4.2, line 152 ("The rates are below the nominal 0.10 because the maximum statistic is conservative when the scores of later checkpoints add little beyond earlier ones"); Section 4.5, line 204 ("because the trajectory maximum is conservative").

**Evidence.** For continuous scores the trajectory maximum is not conservative: P(P_new > P_(r0)) = (n0+1-r0)/(n0+1) exactly. The gap to 0.10 has two sources.
- **(a) Discreteness of the order statistic at small n0.**
  - MATR/CLO: n0 = 12–28, mean 19.95. Averaged over the realised n0, the exact level is 0.081 for false passes and 0.084 for false rejects.
  - HUST: n0 = 7–17, mean 11.9. The exact level is 0.076 and 0.078. Passing is impossible in 2.3% of splits and rejecting in 5.8%.
  - Example: with n0 = 12, r0 = 12 and the exact level is 1/13 = 0.077.
- **(b) Competing rejection.** A bad cell whose maximum would eventually cross lambda-hat can be rejected (S < -mu-hat) at an earlier checkpoint.
  - From `results/raw/E1_*_scores.csv.gz` and the `pass_thr` column, the empirical P(P_new > lambda-hat | bad) is 0.082 (MATR/CLO) and 0.072 (HUST). This matches (a).
  - The realised FPR is 0.068 on both data sets. The difference from 0.082 / 0.072 is caused by (b), not by the max statistic.

**Fix.**
- Replace both sentences with this decomposition.
- In Table 2 or the text, report the exact finite-sample level E[(n0+1-r0)/(n0+1)] next to the realised rates.
- Add a short remark after Proposition 1: for continuous, tie-free scores and a rule without a competing rejection, the bound is attained, P = (n0+1-r0)/(n0+1) >= alpha - 1/(n0+1).
- Remark (ii) can then say plainly that the maximum is tight, not merely valid.

### 2. (Major) The E10 comparison with the analytic Table S13 compares different quantities; the PAC shares are partly vacuous
**Location:** Section 4.5, line 204; Table S12; Table S13 and its caption; Discussion (i), line 237.

**Evidence.**
- Table S13 gives P(conditional error > alpha) for the calibration-conditional probability 1 - F(P_(r0)) ~ Beta(n0+1-r0, r0). For n0 = 20 this is 0.392 (correct).
- The "share of splits with realised FPR > 0.10" is a different quantity. With about 20 bad test cells it means >= 3 false passes, so it adds binomial test-set noise and discreteness to the conditional error.
- A simulation of conditional error ~ 1 - Beta(19, 2) followed by Binomial(20, ·) gives a share of 0.30. The observed shares are 0.285 (E10) and 0.257 (E1, MATR/CLO), so they agree with the correct reference. They are not "below the analytic probabilities because the maximum is conservative".
- On HUST (default design), the PAC variant's 0% share is trivial: the rule never passes and never rejects (never_pass = 1.0, FPR = FRR = 0).
- With enlarged calibration sets on MATR/CLO, 11% / 11.5% of PAC splits have realised error above alpha. This is above delta = 0.1, which is again expected only because of test-set noise. The text does not mention it.

**Fix.**
- Compare the realised shares with a reference that includes test-set sampling (Beta–Binomial with the actual n0 and test class sizes).
- Better still, estimate the calibration-conditional error per split directly from the stored scores, as the share of the pooled bad test cells whose P exceeds that split's lambda-hat.
- State that the PAC result on HUST is vacuous.
- The Table S13 caption should say "calibration-conditional", not "training-conditional".

### 3. (Major) The confidence intervals cover only Monte-Carlo error but are used for population claims
**Location:** Section 3.6, line 113; Table 2 ("FPR upper", "FRR upper"); Sections 4.2, 4.4 and 4.5; `validity_summary` in `code/src/batscreen/statistics/tests.py`.

**Evidence.**
- All 1,000 splits reuse the same 169 or 77 cells. The normal-approximation CI of the mean over splits therefore measures only the randomness of the partitions of a fixed finite data set. It does not measure uncertainty about the error rate on a new population of cells; the Limitations section concedes this.
- The text nevertheless uses these intervals inferentially:
  - "violated the false-reject target on HUST (0.136, upper confidence limit 0.143)";
  - the CNN on HUST, 0.113 (0.060–0.166), "is consistent with the nominal level";
  - E7's `fpr_le_alpha` flag (mean <= alpha + 1.96·SE) is used as a validity criterion.
- The code also computes a pooled Clopper–Pearson bound (`fpr_pooled_cp_hi`). This treats the roughly 20,000 test decisions as independent Bernoulli trials, which they are not. It is not reported, but it should not be used.

**Fix.**
- Call these intervals "Monte-Carlo (split-resampling) intervals" everywhere, including table headers.
- State explicitly that the reference for "valid" is the finite-sample level of Issue 1, and define one validity criterion used throughout.
- For population-level statements, especially the claims that the parametric and point-prediction rules are invalid, add uncertainty at the cell level, e.g. a cell-cluster bootstrap of the per-cell error frequencies in `results/E8_percell_*.csv`.
- Remove the Clopper–Pearson code or mark it as not valid.

### 4. (Major) In Table 3 the paired tests and the effect estimates measure different things and sometimes disagree in direction
**Location:** Table 3 (lines 162–179) and the text after it (line 182); `paired_comparisons` in `tests.py`.

**Evidence.**
- The Wilcoxon test and the rank-biserial r use per-cell differences in absolute cycles to decision. The "Saved diff." column and its bootstrap CI use a ratio of sums, which gives most weight to long-lived cells. The two can disagree (`results/statistics.json`):
  - **MATR/CLO, parametric rule.** Saved diff. = +0.8 points in favour of the proposed rule (CI -1.4 to 3.2), and the mean time is 141.7 vs 146.9. Yet the median paired difference is +7.5 cycles, r = +0.31 and Holm p = 0.0015, which significantly favours the *parametric* rule.
  - **MATR/CLO, point prediction.** The bootstrap CI (-9.3 to -3.5) excludes 0, but Holm p = 0.16. The median difference (-19.6 cycles) favours the proposed rule while r = +0.15 favours the comparator.
- None of these disagreements is explained.
- The per-cell averages are not independent: cells share training sets, calibration thresholds and splits. P-values such as 1.2e-28 come from a normal approximation and carry false precision.
- A small inconsistency: Table 2 gives a Bonferroni HUST mean of 1,737 and a proposed-rule mean of 857 cycles; Table 3 and the text give 1,739 and 854. These are split-weighted and cell-weighted averages, and the text mixes them ("mean 857 instead of 1,739").

**Fix.**
- Use one estimand for both the test and the CI. Either test the per-cell *fractional* time, t_i / min(T_i, L*), and report its Hodges–Lehmann shift with a CI, or bootstrap a p-value for the ratio-of-sums difference.
- Report very small p-values as "< 10^-10".
- Add a sentence that the cells are not independent, so the tests are descriptive.
- Discuss the MATR/CLO parametric case explicitly.
- Use one averaging scheme for the cycle means in the text.

### 5. (Major) The lifetime-interval rule is called valid in a sense conformal theory does not support
**Location:** Section 4.2, line 152 ("... and the lifetime-interval rule were also valid, as Proposition 1 (with M=1) and conformal theory imply").

**Evidence.**
- Trajectory-valid lower and upper bounds give P(lower bound > log T at some look) <= alpha *marginally*. A false pass implies such a violation, so the theory gives P(pass and bad) <= alpha, i.e. P(pass | bad) <= alpha / P(bad), which is about 0.2.
- `interval_calibrate` in `calibration.py` mixes good and bad cells in one residual quantile, as described in Section 3.4.
- The observed rates (0.017, 0.010) are low, but this is an empirical result, not a consequence of the theory. Section 3.4 itself says the rule "controls the error marginally rather than per class".

**Fix.** Say that the interval rule's class-conditional rates were below 0.10 *empirically*, and that its guarantee is on the joint (marginal) probability only.

### 6. (Major) The batch-shift "restored validity" claim rests partly on degenerate cases
**Location:** Abstract (line 13, "restored by recalibrating with 30 cells of the new batch"); Section 4.6, line 210; Discussion, line 237.

**Evidence.** From `results/raw/E5_shift_splits.csv`, proposed rule:
- **Batch 3, source calibration.** Every split has the same 3 bad test cells, so the reported failure of the FPR side (0.128) rests on three cells.
- **Batch 3, target recalibration with 20 or 30 cells.** The calibration set always has exactly 2 bad cells, so passing is impossible (pass_thr = +inf in 100% of splits). The test set always has exactly 1 bad cell. FPR = 0 here is automatic, not evidence of restored validity.
- **CLO, 20 target cells.** 8 bad calibration cells; again the rule never passes.
- **CLO, 30 target cells.** The only informative case. Its 12 bad and 18 good calibration cells and 6 bad and 9 good test cells per split all come from the same 45 CLO cells, and the test cells are drawn from those 45 in every split.

The abstract's general statement rests on this one configuration.

**Fix.**
- Report per-class calibration and test counts in Table S8.
- State that the batch-3 and n = 20 cases cannot pass by construction.
- Limit the abstract and Discussion to "for the CLO batch, 30 recalibration cells (12 bad) restored the targets on the remaining 15 cells".
- Note that the batch-3 FPR results are based on 3 cells.

### 7. (Minor) Proposition 1: state the probability space and the attained level more precisely
**Location:** Eq. 1 (line ~48) and Proposition 1 with its proof (lines 86–90).

**Points to add:**
- **Probability space and conditioning.** The probability is over the joint draw of the calibration cells and the test cell, given the training set and given n0 (or n1). Without conditioning on n0, the bound still holds as an average over n0.
- **Exchangeability.** It is simpler to assume that all calibration and test cells are exchangeable; within-class exchangeability given the labels then follows.
- **Finite-population reading of the experiments.** In the experiments the guarantee is a randomisation guarantee over random partitions of a fixed pool. This is why `stratified_split` draws calibration and test cells from one pool, which is correct and worth stating.
- **Proof step on ties.** "Ties broken at random" is unnecessary. P_new > P_(r0) means P_new strictly exceeds at least r0 calibration values, so its rank is >= r0+1 under any tie-breaking.
- **Lower bound.** Add the matching lower bound for continuous scores (see Issue 1).

### 8. (Minor) The PAC variant is not defined in the Methods
**Location:** Section 3 (absent); Section 4.5, line 204; `pac_rank` in `calibration.py`.

**Evidence.**
- The PAC rank is r_delta = min{r : F_Beta(r, n+1-r)(1-alpha) <= delta}, with delta = 0.1 hard-coded. The minimum class size of 22 follows from 0.9^n <= 0.1.
- The Beta law of the coverage requires i.i.d. sampling from a superpopulation, not only exchangeability. In the finite-pool resampling experiment it holds only approximately.
- This order-statistic rule is the Neyman–Pearson umbrella algorithm of ref. [32], in its binomial form.

**Fix.** Add a short Methods paragraph covering:
- the rank formula;
- delta = 0.1;
- the i.i.d. assumption;
- the n >= 22 condition;
- the link to ref. [32].

### 9. (Minor) Protocol-grouped splits (E9) are not covered by Proposition 1 as stated
**Location:** Section 4.6, line 212 ("exchangeability holds at the level of protocols, and the guarantee held").

**Evidence.**
- `e9_protocol_grouped` assigns whole protocol groups to calibration or test, and MATR protocols contain several cells.
- Cells are then exchangeable only as clusters, not individually, so the cell-level rank argument does not apply directly. Calibration with clustered data can be anti-conservative or conservative.

**Fix.** Say that the observed validity (0.073 / 0.088) is empirical. Note that a formal guarantee would need a group-level argument, e.g. one cell or one maximum per protocol group.

### 10. (Minor) The CNN validity claim rests on 30 splits; the Methods misstate the split counts
**Location:** Section 3.6, line 113 ("other experiments 200–333 (Table S1)"); Section 4.4, line 188; Table S1.

**Evidence.**
- Table S1 and `config/default.yaml` give 30 splits for the CNN and 1,000 for logistic regression; both fall outside "200–333".
- The CNN's HUST FRR of 0.113 (Monte-Carlo CI 0.060–0.166) cannot support "consistent with the nominal level" beyond saying the data cannot exclude it.

**Fix.**
- Correct the Methods sentence.
- Phrase the CNN result as inconclusive, or run more CNN splits if the authors want the claim.

### 11. (Minor) Test-only noise is drawn independently at each checkpoint, which inflates the effect on the maximum
**Location:** Section 4.7, line ~219; `predict_models` in `runner.py`.

**Evidence.** The noise is redrawn independently at each checkpoint. Real measurement-chain differences are largely persistent in time, and independent draws make it as likely as possible that a noisy maximum crosses a threshold.

**Fix.** State this. Optionally, add a persistent (per-cell) noise variant in a later revision.

### 12. (Minor) Inconsistent or unclear numbers and wording
- E1 exceedance shares are 26% and 21% (line 152); E10 gives 28% and 24% (line 204). Both are correct for their own split sets, but the text does not say they come from different experiments.
- "about 20.0 and 11.9 bad cells, respectively, in the test sets' companion calibration sets" (line 152): rephrase as "with on average 20.0 and 11.9 bad calibration cells".
- Table 2 vs Table 3 cycle means (1,737 vs 1,739; 857 vs 854): see Issue 4.
- Reference [19] has no authors; it should be V. Vovk, A. Gammerman, G. Shafer.

### 13. (Minor) Code robustness and wording of the scale definition
- **`conformal_upper` silently drops NaN and +inf values.**
  - A +inf calibration score (e.g. a zero scale) would be removed, lowering the threshold, which is anti-conservative.
  - Dropping NaN changes n. (This is harmless here: `_traj_max` never returns NaN, and the naive rule pre-filters on `alive`.)
  - Raise an error on +inf or NaN instead.
- **`pac_upper` does not apply the same filter,** so the two functions are inconsistent.
- **`metrics` sets FPR = 0 when a test set has no bad cells** (`max(bad.sum(), 1)`). This never happened in the reported runs (I checked that n_bad > 0 in every E1 and E5 split), but such splits should be excluded explicitly (NaN) rather than counted as zero.
- **The elastic-net scale s_m is not strictly "out-of-fold RMSE".** It is the CV-minimised mean fold MSE, with imputation and standardisation fitted on all training cells before the CV. This does not affect validity, since s_m depends only on the training cells, but Section 3.2 should describe it accurately ("cross-validated RMSE at the selected penalty").

### 14. (Minor) Related statistical literature for the max-statistic calibration
**Location:** Section 2, line ~40, and Remark (ii).

**Evidence.** Calibrating a sup- or max-type nonconformity score over a trajectory to get simultaneous validity is established. Examples the authors should verify and cite:
- functional conformal bands: Lei, Rinaldo & Wasserman 2015, Ann. Math. Artif. Intell.; Diquigiovanni, Fontana & Vantini 2022, J. Multivariate Anal.;
- multi-horizon conformal forecasting: Stankevičiūtė, Alaa & van der Schaar 2021, NeurIPS (which uses Bonferroni).

**Fix.** Cite these and phrase the novelty as using this construction for class-conditional sequential screening with truncated calibration, as the Gap paragraph already partly does.

## Checks performed (read-only)
- Recomputed the E1 summaries from `results/raw/E1_*_splits.csv`:
  - FPR/FRR means of 0.068/0.080 (MATR/CLO) and 0.068/0.074 (HUST) reproduce.
  - The shares above 0.10 are 0.257 and 0.213.
  - No split has zero test cells in either class.
- Recomputed P(P_new > lambda-hat) and P(R_new > mu-hat) from `E1_*_scores.csv.gz`, and the exact level E[(n0+1-r0)/(n0+1)] (Issue 1).
- Simulated the Beta–Binomial reference for the realised exceedance share (Issue 2).
- Inspected the paired statistics in `results/statistics.json` (Issue 4).
- Inspected `E5_shift_splits.csv` for class counts per scenario (Issue 6).
- Checked the floating-point behaviour of the rank ceil((n+1)(1-alpha)).
