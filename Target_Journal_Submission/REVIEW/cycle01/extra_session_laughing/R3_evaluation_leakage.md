# Review R3 (cycle 01): evaluation methodology and data leakage

Reviewer role: ML evaluation methodologist. Scope: split construction, feature computation (look-ahead), preprocessing, the normalisation scale s_k, hyper-parameter selection, seeds, the definitions of time saved and error rates, and the E5/E9/E10 split functions. All paths are relative to `Target_Journal_Submission/`. Line numbers refer to the files as committed at review time.

## Summary

I read `code/src/batscreen/**` and `code/experiments/{suite,analysis,figures}.py` line by line. I also ran small read-only checks against `data/features/*.npz` and `results/raw/*.csv`.

**No leakage that would invalidate the headline error-rate results was found.** These parts are clean:
- Features at checkpoint k use cycles <= k only.
- Imputation and standardisation are fitted on training cells only.
- s_k comes from training-set cross-validation.
- Calibration uses only Z and scores before L\*.
- Calibration and test cells in E1 are drawn uniformly at random from the same pool.
- No split has an empty class denominator (`n_bad`, `n_good` >= 1 in every results CSV).
- No HUST cell, and no MATR/CLO cell, dies before the first checkpoint (T_min = 148 and 1,142). Cells that die between checkpoints are handled consistently in `simulate` (rejected by observation and charged T) and in calibration (P_i is the maximum over alive checkpoints; dead bad cells count as -inf for the single-checkpoint rule).

The main problems are with interpretation and inference, not leakage:
1. Most "validity" experiments are exchangeable by construction, so they cannot fail except through a code bug. They are presented as empirical confirmation.
2. The E9 protocol-disjoint result is attributed to Proposition 1, but the theorem does not cover group-level assignment.
3. The "truncated campaign" framing hides the fact that the main predictor is trained on cells cycled to end of life.
4. The cell-level paired tests treat dependent per-cell averages as independent, so the p-values are far too small.

There are also some latent or minor issues: a latent look-ahead in the HUST fallback, unpaired E1 vs E2 comparisons, an optimistic CNN/EN scale, a vacuous b3 recalibration and several text errors.

**Recommendation: major revision.** None of the fixes changes the central theorem or E1 numbers. Most need only text and analysis changes, not new experiments.

## Issues

### 1. (Major) Most validity experiments are guaranteed by construction and are presented as empirical confirmation

- **Location:** Abstract; Section 4.2 ("The trajectory-calibrated rule met both error targets"); Section 4.4 ("the data agree"); Section 4.6 (cross-lab and recalibration); Section 5 (iii).
- **Code:** `code/src/batscreen/evaluation/runner.py:17-31` (`stratified_split`).
- **Evidence:**
  - Given the training set, the calibration and test cells are a uniformly random partition of the remaining pool (runner.py:29-31). They are therefore exactly exchangeable within class. By Proposition 1, the split-averaged FPR and FRR are then at most alpha and beta, for any predictor and any feature noise applied to both sets.
  - The same holds for:
    - E2 (all predictors);
    - E3, E7 and E10;
    - E4 calibration/training fraction and noise "both";
    - E5 `target_cal` (suite.py:153-156: calibration and test drawn at random within the same target batch and class);
    - E5 cross-lab (suite.py:190-199: HUST calibration and test drawn at random within class from the HUST pool).
  - So the "validity" in Table 2, Table S4 and the sentence "a model trained in one laboratory and calibrated in the other was valid" are mathematical consequences of the split design plus correct code. They are not evidence about real deployments.
  - My check: the exact expected bound mean((n0+1-r0)/(n0+1)) over the realised n0 of E1 is 0.081 (MATR/CLO) and 0.076 (HUST). The observed values are 0.068 and 0.068.
  - Only these experiments test anything beyond the theorem: E5 `source_cal` (actual batch shift), E4 test-only noise, and partly E9 (see Issue 2).
- **Fix:**
  - Say explicitly in Section 3.6 and Section 4.2 that random splitting makes calibration and test cells exchangeable by design, so E1–E4, E7 and E10 validity is an implementation check.
  - Report the exact theoretical expectation next to each observed FPR/FRR, using the values above.
  - Present E5 `source_cal`, E4 test-noise and E9 as the informative stress tests.
  - Reword "the data agree" (Section 4.4) and "a model trained in one laboratory and calibrated in the other was valid" (Section 5) accordingly.
  - The efficiency comparisons are unaffected.
- **Requires rerun:** no.

### 2. (Major) E9 (protocol-disjoint) validity is attributed to Proposition 1, but group-level assignment is not covered by it

- **Location:** Section 4.6, `manuscript/src/part2_results.md:59` ("Because protocol groups were assigned to calibration and test at random, exchangeability holds at the level of protocols, and the guarantee held").
- **Code:** `code/experiments/suite.py:282-306`.
- **Evidence:**
  - `fn` (suite.py:294-300) assigns whole groups to calibration or test, using a coin flip with p = 0.5 per group. Groups contain 1–8 cells: 78 groups, 43 singletons, the largest with 8 cells.
  - Proposition 1 needs a new **cell** to be exchangeable with the calibration **cells** of its class. With clustered assignment this does not hold. Cells of the same protocol move together and have correlated scores, and calibration and test sizes are random (`n_test` 11–64, `n_cal` 21–73 in `results/raw/E9_protocol_grouped_splits.csv`).
  - Group exchangeability gives a guarantee for a group-level statistic, not for the per-cell FPR that is reported.
  - The per-split FPR standard deviation is 0.102 in E9 vs 0.083 in E1. 24.5% of E9 splits exceed 0.10.
  - Protocol labels are also not canonical:
    - `4.8C(80%)-4.8C` (b1, b2; 5 cells) and `4.8C(80%)-4.8C-newstructure` (b3; 4 cells) are different groups (groups are built at suite.py:291).
    - `4C(31%)-5` (b2) looks like a truncated `4C(31%)-5C`.
    - So nominally identical charging protocols can sit in both training and test.
- **Fix:**
  - State that the E9 result is empirical and not covered by Proposition 1. Alternatively, add a group-conformal variant (one trajectory statistic per protocol group, e.g. the group maximum, calibrated over groups) whose guarantee does cover this case.
  - Canonicalise protocol strings: decide whether "newstructure" is a different protocol, and justify the choice.
  - Report how many test cells share a nominal protocol with training cells.
- **Requires rerun:** no for the wording. A short E9 rerun (89 s) is needed if the labels are merged.

### 3. (Major) The "truncated campaign" claims omit that the main predictor's training cells are cycled to end of life

- **Location:** Title ("From Truncated Test Campaigns"); Abstract ("calibration campaigns ended 2.61 times sooner"); Section 4.3 "Truncated calibration"; Section 5 "Truncated campaigns".
- **Code:**
  - `runner.py:56`: the elastic net regresses `np.log10(T[a_tr])` with the full lifetime of every training cell.
  - `runner.py:177`: `trc = T[tr]` for regressors.
- **Evidence:**
  - `tables/T5_campaign_cost.md`, EN rows:
    - MATR/CLO: `train_wallclock` = 2,130 cycles vs `cal_wallclock` = 750.
    - HUST: 2,656 vs 1,900.
  - The longest campaign in the main experiment is therefore set by the training cells, not the calibration cells. If no historical data exist, the full campaign is not shortened at all.
  - The "time saved" metric (`procedure.py:146,154`) covers only test-cell cycling relative to min(T, L\*). Training and calibration cycling are not included.
  - The only fully truncated configuration (logistic regression, train_wallclock 750 and 1,900) saves about 10 points less.
- **Fix:**
  - Say in the Abstract and Section 4.3 that the main predictor was trained on cells cycled to EOL.
  - Report the total campaign wall-clock (training plus calibration) for EN vs logistic regression vs the interval rule.
  - Qualify the title and abstract claim: either "calibration needs only truncated cells", or lead with the fully truncated logistic numbers.
- **Requires rerun:** no.

### 4. (Major) Cell-level Wilcoxon tests and bootstrap CIs treat dependent per-cell averages as independent

- **Location:** Section 3.6; Table 3; Section 4.3 (e.g. p = 1.0e-24, 1.2e-8, 0.00099).
- **Code:**
  - `code/src/batscreen/statistics/tests.py:37-47` (`per_cell_times`).
  - `tests.py:58-95` (`paired_comparisons`).
- **Evidence:**
  - Each cell's time is averaged over the splits in which it was a test cell. Its thresholds and model were fitted on the other 168 (or 76) cells, so the per-cell averages are strongly dependent.
  - The Wilcoxon test (tests.py:78) and the cell bootstrap (tests.py:84-87) assume independent cells. The p-values (1.2e-28 for MATR/CLO) and CIs are therefore anti-conservative with respect to generalisation to new cells.
  - The Limitations section concedes that split-to-split variation understates the variation across populations, but Table 3 still reports formal significance.
  - The two procedures also test different quantities. The Wilcoxon test concerns the distribution of per-cell time differences; the bootstrap concerns the ratio-of-sums saving. Example (Table 3, MATR/CLO, point prediction): Holm p = 0.16 while the 95% CI of the saving difference (-9.3 to -3.5) excludes 0.
- **Fix:** Use an inference procedure that accounts for resampling dependence, for example:
  - the corrected resampled t-test of Nadeau and Bengio on split-level paired differences;
  - a repeated K-fold with a variance correction;
  - or present Table 3 as descriptive (effect sizes and split-level SDs) and drop "significant".

  At minimum, align the test with the reported quantity (test the split-level paired difference in `time_saving`).
- **Requires rerun:** no. The split-level CSVs contain everything needed.

### 5. (Minor) E1 (elastic net) and E2 (other predictors) use disjoint seeds and different numbers of splits, so the predictor comparison is unpaired

- **Location:** Section 4.4; Table S4 (`tables/T4_base_models.md`); Table S1.
- **Code:**
  - `suite.py:12` (offsets E1 = 0, E2 = 100000).
  - `suite.py:72`: E2 runs logit, GP, CNN, GBR and RF but not EN.
  - `analysis.py:114-116` concatenates E1 EN with E2.
- **Evidence:**
  - In `tables/T5_campaign_cost.md`, the interval-rule `cal_cell_cycles` are identical for GBR, GP and RF (33,460), because they share E2 splits. EN has 33,547 because it ran on E1 splits.
  - The savings differences between EN (78.3%) and the other predictors (67.5–80.5%) therefore mix predictor effects with split sampling (1,000 vs 200 vs 30 splits).
- **Fix:** Add EN to E2 on the E2 seeds (about 1.7–2.6 s per split, 400 splits) and report paired differences.
- **Requires rerun:** yes (cheap).

### 6. (Minor) Latent look-ahead in the HUST feature fallback; the unit test and SI S3 overstate their coverage

- **Location:** `code/src/batscreen/preprocessing/features.py:94-97`, `:28-33`, `:75-76`; `code/tests/test_features.py`; SI S3 ("All features at checkpoint k use cycles <= k only; this is enforced by a unit test").
- **Evidence:**
  - `hust_features` falls back to `_nearest_valid(cell["vq"], cyc.index(k), 1)`. This shifts the **row index** of the stored curve array, whose rows are cycles 1..20, 30, 40, ..., 1000 (`scripts/preprocess.py:22`). A shift of +1 therefore uses cycle k+10 (or cycle 30 for k = 20): future data.
  - `_nearest_valid` with `window=1` (features.py:75-76) also tries +1..+3 cycles.
  - My check: the fallback was never triggered in the committed tables. There are 0 of 1,309 alive HUST cell-checkpoints where the CNN curve (no fallback) is NaN while the scalar features are finite. So the reported results are unaffected.
  - The unit test covers only `matr_features`. It does not cover `hust_features`, `difference_curve` or `build_feature_table`.
- **Fix:**
  - Restrict the fallbacks to backward shifts (s <= 0).
  - Add no-look-ahead tests for `hust_features` and `difference_curve`.
  - Narrow the SI S3 claim to what is tested.
- **Requires rerun:** no. The committed features are unchanged because the fallback never fired.

### 7. (Minor) Feature design and evaluation design were adjusted using all cells and a first full run

- **Location:** Section 3.2 (window medians); Section 3.6 (discarded stratification); `EXPERIMENT_LOG.md` 16:00 and 16:42; `literature/research_design.md` lines 3-9.
- **Evidence:**
  - The 5-cycle median fix was chosen by looking at EN MAPE on 5 random 50/50 splits of all 169 cells (log 16:00). The data later used for testing therefore informed feature design.
  - The split design was changed after inspecting the first full E1 run (log 16:42), and the run was restarted "with identical seeds".
  - The change is theoretically justified and the guarantee is unaffected, because conformal calibration is post-hoc. Efficiency numbers may still be mildly optimistic.
- **Fix:**
  - In Section 3.6, state that the feature fix was selected on data overlapping the evaluation cells.
  - State that the final seeds were also used in the discarded run.
- **Requires rerun:** no.

### 8. (Minor) The normalisation scale s_k (EN) and the CNN scale are optimistically biased, which matters for the "parametric rule" comparison

- **Location:** Section 3.2, Eq. 2; Section 5 "Model-based uncertainty is not a substitute".
- **Code:**
  - `code/src/batscreen/models/base.py:36-42`.
  - `code/src/batscreen/models/cnn.py:164-186`.
- **Evidence:**
  - EN:
    - `make_pipeline(SimpleImputer, StandardScaler, ElasticNetCV)` fits the imputer and scaler on all training cells before ElasticNetCV's internal CV.
    - s_k is the CV error at the penalty that minimised that same CV error, which is biased low.
    - The folds are not grouped by protocol, although replicate cells of one protocol exist (CLO: 9 protocols x 5 cells; b3 up to 8).
  - CNN: `self.scale = best` is the validation RMSE of the epoch selected on that same validation set.
  - Validity is not affected, because the scale is fixed before calibration. However, the parametric/Bayesian rule `gauss` uses these scales as Gaussian sigma, so part of its failure (e.g. HUST CNN 0.183/0.250) may come from optimistic scales rather than from "model-based uncertainty" as such.
- **Fix:**
  - Note the bias.
  - Preferably compute s_k from nested or protocol-grouped out-of-fold residuals, at least for the `gauss` baseline, so that baseline is not handicapped.
- **Requires rerun:** no for the note. Yes if the baseline is recomputed.

### 9. (Minor) In E1, protocol replicates are shared across training, calibration and test, and batch is confounded with class; headline savings mix these effects

- **Location:** Abstract (78.3%); Section 4.3; `tables/E8_error_by_batch_matr_clo.md`.
- **Evidence:**
  - `stratified_split` stratifies by dataset x class only. Replicates of the same protocol therefore appear in training and test. `chargetime5` effectively encodes the protocol.
  - The E9 protocol-disjoint saving is 75.1% vs 78.3% in E1.
  - At L\* = 750, batch b2 is 43/43 bad and b3 is 3/40 bad.
  - From `results/E8_percell_matr_clo.csv`, b2 cells are decided after 41 cycles on average (91% saved), vs 72.6–77.7% saved for b1, b3 and b4. Much of the headline saving comes from one easy, all-bad batch.
- **Fix:**
  - Report the saving per batch.
  - Give the protocol-disjoint E9 number next to the E1 headline.
- **Requires rerun:** no.

### 10. (Minor) E5 batch-3 recalibration is vacuous for the false-pass rate, and target calibration cells are selected using labels

- **Location:** Section 4.6 "Recalibration ... restored validity"; `suite.py:142-157`.
- **Evidence:**
  - b3 has only 3 bad cells out of 40. With n_t = 20 or 30, `_batch_split_fn` puts 2 bad cells in calibration, so the pass threshold is always +inf, and leaves 1 bad test cell.
  - The b3 `target_cal` FPR is therefore 0.000 by construction (E5 CSV: `n_bad` = 1.0, `n_cal_bad` = 2.0).
  - The calibration subset is stratified using the labels of all target cells (suite.py:153-155). This is harmless for class-conditional validity, but it is not implementable before the target cells have been cycled.
  - The source domain (b1+b2) is 60/84 bad, unlike either target.
- **Fix:**
  - Limit the "restored validity" claim to b4 (n_t = 30: 0.075 and 0.046 on 15 test cells, 6 bad).
  - State that b3 cannot test false-pass control.
  - Describe the stratified target sampling as such.
- **Requires rerun:** no.

### 11. (Minor) Text and table errors in the evaluation description

- **Evidence:**
  - Section 3.6 (`Draft_Manuscript.md:113`) says "other experiments 200–333 (Table S1)". `config/default.yaml` sets `n_splits_secondary: 200`, all secondary CSVs have 200 splits per configuration, and the CNN has 30. Nothing has 333.
  - Table 1 "Protocols = 77" for HUST is computed from cell IDs (`data/hust.py:307` sets `policy=cid`; `analysis.py:47` counts unique policies). It is not verified protocol metadata, so cite Ma et al. for it.
  - Table 2 (857 cycles; split-averaged) and Table 3 (854; per-cell average) report the proposed rule's mean time with different averaging. Define both.
  - `config/default.yaml` comment "keeps >= 9 cells per class for calibration" is outdated after the split fix. In E1 HUST, `n_cal_bad` < 9 in 2.3% and `n_cal_good` < 9 in 5.8% of splits (infinite thresholds there). Report this in Section 4.2 or Section 4.5.
  - Figure 2 MAPE is pooled over the cells alive at each k (`figures.py:91-93`). The population changes slightly with k (169 -> 167 MATR/CLO cells at k = 300). On cells alive at all checkpoints, MATR/CLO MAPE at k = 20 is 22.9%, not 28.6%. Mention this or use a fixed population.
- **Requires rerun:** no.

## Items verified as correct (no action)

- **Features:**
  - MATR window medians use cycles k-4..k and 8..12 (`features.py:63-74`).
  - Capacity features use `qd[:k]` (`features.py:45-53`).
  - Glitch interpolation uses only cycles <= k.
  - `tmax_mean` uses `[1:k]` and charge time uses cycles 2–6.
  - There are no alive cells with missing features (0 such rows in either table).
- **Preprocessing:** imputer, scaler and model are fitted on training cells alive at k (`runner.py:41-58`). The feature-noise SD comes from training cells (`runner.py:57,75`).
- **Calibration:**
  - Thresholds use only calibration cells (`runner.py:160-172`) and Z.
  - Good cells are always alive at every checkpoint, because k_M < L\*.
  - Dead bad cells are handled consistently for `traj` (`calibration.py:56-58`, -inf) and `single` (`calibration.py:93-96`).
- **Metrics:**
  - FPR and FRR denominators are the bad and good test cells.
  - No split has a zero denominator (minimum `n_bad` across all CSVs is 1, in E5 b3).
  - Time saved = 1 - sum(time)/sum(min(T, L\*)) per split. Cells that fail before a checkpoint are charged T, and cells undecided after k_M are charged min(T, L\*), consistently in the numerator and denominator.
- **PAC (E10):** `pac_rank` uses the Beta(r, n+1-r) coverage law correctly. Calibration sets are the default or enlarged fractions with E10's own seeds.
- **E5 cross-lab:** the source model is trained on all MATR/CLO cells, and HUST calibration and test cells are disjoint from HUST training cells.
- **Seeds:** offsets per experiment are disjoint and splits are deterministic given the seed. Variants within one run share fits by design (`runner.py:103-134`).
