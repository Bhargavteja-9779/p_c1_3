# Review R2 (battery testing and degradation), cycle 01

**Manuscript:** "Stopping Cycle-Life Tests Early With Guaranteed Error Rates: Distribution-Free Sequential Screening of Lithium-Ion Cells From Truncated Test Campaigns" (Battery Energy)

**Recommendation:** Major revision

## Summary

The authors calibrate pass and reject thresholds on the maximum over checkpoints of normalised lifetime-predictor scores. Calibration uses held-out cells cycled only to min(T, L*), and the resulting class-conditional false-pass and false-reject probabilities are bounded under any stopping time. The statistics are sound, and the naive-sequential result is a useful warning for practice: re-checking a prediction until it looks decisive inflates the error rate to 0.145–0.286 at a nominal 0.10. The code is careful (no look-ahead test, audited cleaning) and the experiment set is broad.

From a battery-testing point of view, the practical claims go beyond what the data support. The main concerns:

1. In MATR/CLO and HUST, lifetime varies mostly between protocols, not from cell to cell. The headline task is therefore protocol discrimination, not production screening of nominally identical cells.
2. The realistic deployment case is a new batch, which needs recalibration. There the savings fall from 78% to 10–27%, and the per-batch recalibration has a wall-clock cost that the paper does not discuss.
3. The cost accounting leaves out the calibration and training campaigns, channel hours and campaign wall-clock time. On a net basis, one split's calibration costs more cell-cycles than screening that split's test cells saves.
4. L* is placed at the median. Real specifications sit in the lower tail, where the "≥ 9 bad calibration cells" requirement becomes very costly.
5. The end-of-life labels are rate-dependent and protocol-dependent. The data cleaning removes censored cells, which contradicts the paper's own truncation argument.

None of these points invalidates the method. They do require reframing the claims, adding analyses, and in some cases running new experiments.

Checks I ran (read-only, on the result CSVs) are reported with each issue.

---

## Issues

### 1. (Critical) The screening task is mostly protocol discrimination, not cell screening; within-protocol performance is unknown
**Location:** Title; Abstract; Sec. 1 (contributions); Sec. 3.2 (features `chargetime5`, `tmax_mean`); Sec. 3.5; Sec. 5 "What the guarantee does and does not mean" (iii), "plausible for cells drawn from the same production lot".

**Evidence:**
- From `results/E8_percell_matr_clo.csv` (policy column), the pooled within-policy variance of log10 T over the 35 policies with more than one cell (126 cells) is 0.0048. The total variance across all 169 cells is 0.029, so within-protocol variation is about 17% of the lifetime variance. About 83% is explained by which protocol a cell ran.
- In HUST, every one of the 77 cells has its own discharge protocol (Table 1: 77 protocols), so all of its lifetime variation is between protocols.
- Two features are direct protocol fingerprints: `chargetime5` (mean charge time of cycles 2–6) and `tmax_mean` (`code/src/batscreen/preprocessing/features.py`, lines 82–85). They are available from cycle 6, which fits the observation that half of the MATR/CLO cells are decided within 40 cycles (Sec. 4.3), before any capacity fade.
- In production screening and lot qualification, all cells run the same protocol. The relevant variance is the 17% within-protocol part, and the paper gives no evidence about it.

**Fix:**
- Reframe the title, abstract and Sec. 5 around screening of test conditions or designs (protocol screening), or demonstrate cell-level screening.
- Add a within-protocol analysis. Options: (a) remove `chargetime5`, `tmax_mean` and any other protocol-identifying inputs and rerun E1; (b) define L* relative to each protocol's median, or use the CLO batch (9 protocols × 5 cells), and report what can be decided from cell-to-cell variation alone; (c) report feature importance at the checkpoints where most decisions occur (20–40 cycles).
- Remove the "same production lot" plausibility claim unless (a) or (b) supports it.

### 2. (Critical) The realistic deployment scenario (a new batch) gives far smaller savings and needs a per-batch calibration delay that is not discussed
**Location:** Abstract (final sentences); Sec. 4.6; Sec. 5 (iii) and "Recommended workflow" step 5; Sec. 7.

**Evidence:**
- `tables/T8_shift.md`, recalibrated rows. With 30 CLO (b4) cells, the proposed rule saves 26.8%. With 20 b4 cells it saves 9.4%, and on b3 it saves 6.0% (20 cells) and 9.9% (30 cells).
- In the same b4 setting with 30 target cells, the single-checkpoint rule saves 42.5% with FPR/FRR 0.060/0.055. The proposed rule is therefore not the most efficient valid rule in the realistic case.
- The abstract reports 78.3% (pooled random splits) and says that recalibration "restored" the guarantee, but omits the 26.8% saving.
- Recalibration needs the calibration cells' classes, so the thresholds for a new batch exist only after the good calibration cells reach L* cycles. Cells started together with the calibration cells gain nothing: by the time thresholds exist, they have also run L* cycles. Savings apply only to cells from the same population started later, which is a staggered-lot workflow the paper should state explicitly.
- Workflow step 5 ("recalibrate whenever the production batch ... changes") therefore means a delay of L* cycles plus about 30 or more cells to L* for every batch.

**Fix:**
- Put the recalibrated savings (and the single-checkpoint comparison) in the abstract and conclusions next to the pooled numbers.
- Add a timeline diagram or analysis of when decisions become possible for a new batch.
- Discuss under which test-lab workflows (continuous flow of cells from a stable process, staggered starts) the method saves time.

### 3. (Major) The cost model omits calibration and training campaigns, channel hours and campaign wall-clock time; the headline "2.61 times sooner" is a max-lifetime artefact
**Location:** Abstract ("calibration campaigns ended 2.61 times sooner"); Sec. 4.3 "Truncated calibration"; Sec. 5 "Truncated campaigns"; Limitations "Cost model".

**Evidence:** From `results/raw/E1_*_splits.csv`, proposed rule:
- **MATR/CLO:**
  - Calibration costs 27,471 cell-cycles per split (mean).
  - Screening the 42 test cells saves 21,497 cell-cycles (42 × (653 − 142)).
  - Break-even is about 51 screened cells (median over splits), i.e. more than the test set.
  - Training cells cost a further 67,309 cell-cycles, cycled to EOL with a mean wall-clock of 2,130 cycles.
- **HUST:**
  - Calibration costs 40,025 cell-cycles per split.
  - Screening saves 20,230 cell-cycles.
  - Break-even is about 44 cells, versus 23 test cells.
- **Campaign wall-clock:** the last test-cell decision in a split happens at L* in 73% (MATR/CLO) and 90% (HUST) of splits. A test batch started together therefore finishes no earlier. The savings are channel-time savings, which pay off only if freed channels are reused.
- **"2.61 times sooner"** is max(T_cal) / L*. It depends on the longest-lived calibration cell. Total calibration cell-cycles fell by only 1.22 and 1.09 times (Sec. 4.3).
- **Cycles are not hours:** cycle duration depends on the charge protocol (MATR) and the multi-stage discharge (HUST), so the cycle-based savings are not channel-hour savings. RPTs, rests and channel scheduling are not modelled (Limitations).

**Fix:**
- Report net cost (training + calibration + screening) as a function of the number of screened cells, and give the break-even number.
- Report campaign wall-clock time (time of the last decision) next to mean time to decision.
- Convert cycles to channel-hours using the recorded per-cycle test time.
- Replace the 2.61 figure in the abstract with the total cell-cycle factor, or present both.
- Discuss RPT overhead: in a real campaign, intermediate RPTs every N cycles fix the possible checkpoint grid.

### 4. (Major) The choice of L* near the median is unrealistic for qualification; tail specifications make class-conditional calibration very costly
**Location:** Sec. 3.5 ("close to the median lifetimes, so that both classes are well represented"); Sec. 4.5 E7; Remark (iii); Recommended workflow step 3.

**Evidence:**
- Bad shares in E7 are 29% / 48% / 73% (MATR/CLO, L* = 550/750/900) and 25% / 52% / 74% (HUST, 1,600/1,900/2,200), computed from `E8_percell_*.csv`.
- Specifications in qualification and warranty work sit in the lower tail, where a few percent of cells are bad.
- Passing requires at least 9 bad calibration cells at α = 0.10, and the PAC variant needs 22 or more. A practitioner cannot choose how many bad cells end up in the calibration set: the calibration set must have about 9/π_bad cells. At π_bad = 5% that is 180 or more cells cycled to L*, and about 440 for the PAC variant.
- Already at π_bad = 25% (HUST, L* = 1,600) the rule passed no cell in 98% of splits.
- The workflow statement "at least ten bad and ten good cells" hides this dependence on prevalence.

**Fix:**
- Add an experiment with L* at the 10th and 20th lifetime percentiles. Also run asymmetric levels (α < β, since a false pass is usually costlier than a false reject).
- Express the calibration-size requirement as a function of bad-cell prevalence in the text and in the workflow.
- Discuss options for rare bad cells, for example one-sided screening (reject-only or pass-only) or stratified or enriched calibration with prevalence weighting.

### 5. (Major) The quality-relevant metric (bad cells among passed cells) is not reported
**Location:** Sec. 3.6 metrics; Table 2; Sec. 5.

**Evidence:**
- A test lab or customer cares about the share of passed cells that will fail the spec (escape rate, 1 − PPV), not about P(pass | bad).
- From `E1_*_cells.csv.gz` joined with lifetimes, the share of bad cells among model-passed cells is 6.1% per split on average (7.5% pooled) on MATR/CLO and 9.5% (12.0% pooled) on HUST. These values hold at about 50% prevalence.
- The escape rate depends strongly on prevalence, and α does not control it.

**Fix:** Report the escape rate and its dependence on prevalence. State clearly that α bounds the class-conditional rate, not the defect rate in the passed population. If needed, point to conformal selection / FDR control [37] as the alternative for that target.

### 6. (Major) End-of-life labels are rate-dependent and protocol-dependent; sensitivity to the EOL definition is missing
**Location:** Sec. 3.1 (T = first cycle at 80% of nominal); Sec. 3.5 ("Both datasets record data until ... 0.88 Ah"); `code/src/batscreen/data/hust.py` (label = number of recorded cycles); Limitations last bullet.

**Evidence:**
- MATR capacity is the 4C cycling discharge capacity, and HUST capacity is measured under 77 different multi-stage discharge protocols. Neither is an RPT capacity at a reference rate and temperature, as IEC 61960 / IEC 62660-1 style cycle-life definitions use.
- "80% at 4C" and "80% under protocol X" are not the same state of health for different cells, so part of the label difference between protocols comes from the rate-capacity effect, not from degradation.
- Label noise near L* drives many errors. The worst false passes include b4c20 with T = 748 (falsely passed in 80% of its test splits) and b4c8 with T = 678. The worst false rejects include b1c19 with T = 788 (83%) and b4c3 with T = 778 (`E8_percell_matr_clo.csv`).
- A few cycles of label uncertainty, or a different EOL convention, would flip these cells' classes.

**Fix:**
- Discuss the rate-dependence of the labels.
- Add a sensitivity analysis in which labels come from a different EOL threshold (e.g. 85% and 90%, or a knee-onset definition). These labels can be recomputed from the stored capacity trajectories.
- State that L* must be defined on the same capacity measurement that the test lab uses.

### 7. (Major) Data cleaning removes right-censored cells, which contradicts the paper's own truncation argument
**Location:** Sec. 3.5 ("five batch-1 cells that never reached EOL were removed"); SI S2 (b1 cells 8, 10, 12, 13, 22; final capacity 0.91–0.97 Ah).

**Evidence:**
- The paper's key practical claim is that a cell's class requires only min(T, L*) cycles. Yet cells whose tests ended before EOL were dropped rather than labelled. If they ran 750 or more cycles, their class at L* = 750 is known: good.
- Dropping them removes long-lived good cells from batch 1. This shifts the class balance and removes exactly the kind of cells (unfinished tests) that a real campaign produces.
- The shortest cell (b2c1, 148 cycles), which drives far-from-L* false passes (Sec. 4.8), is a known anomaly in the original data set. Its treatment should be discussed.

**Fix:**
- Report each removed cell's cycle count. Include censored cells with min(T_cens, L*) ≥ L* as good calibration, test and training cells for classification-type predictors, and rerun E1.
- Alternatively, justify the exclusion explicitly as a departure from the truncated-data philosophy.
- Discuss whether b2c1 is a test artefact.

### 8. (Major) Batch confounding in the pooled MATR/CLO data inflates the pooled results
**Location:** Sec. 3.5, 3.6 (random splits pooled over batches b1–b4); Sec. 4.2–4.3.

**Evidence:**
- From `E8_percell_matr_clo.csv`, the bad share at L* = 750 is 41% (b1), 100% (b2, max T = 713), 8% (b3) and 40% (b4).
- The MATR batches differ in protocol families and in test procedure (for example, rest periods and temperature-measurement set-up differ between batches). Batch membership is therefore a strong class predictor, and `tmax_mean` and `chargetime5` can encode it.
- Pooled random splits make calibration and test exchangeable by construction. E5 shows the guarantee then fails across batches (FRR 0.48 / 0.60).
- The headline efficiency therefore partly reflects batch identification.

**Fix:** Report E1 per batch (E8 already has per-batch error tables; add per-batch savings). Add a leave-one-batch-out calibration-and-test analysis in the main text. Test whether removing `tmax_mean` and `chargetime5` changes the saving (see Issue 1).

### 9. (Minor) The noise robustness test is not physically interpretable
**Location:** Sec. 4.7 "Noise (E4)"; Fig. 6.

**Evidence:**
- Noise is added in units of each feature's standard deviation (0.1–1 SD). This is not tied to any cycler, thermocouple or channel specification.
- Real measurement-chain differences are systematic: channel-to-channel current offset, thermocouple contact, chamber temperature drift. The six batch-3 channels removed as noisy (SI S2) are an example of exactly this.

**Fix:** Inject perturbations at the raw-signal level (e.g. ±1 mV voltage, 0.05% current gain error, ±1 °C temperature offset, single-channel bias) and recompute features. Alternatively, express the current noise levels in physical units, and call it what it is: an exchangeability stress test.

### 10. (Minor) "Early" checkpoints on HUST reach 53% of the specification
**Location:** Sec. 3.5 (HUST checkpoints up to 1,000 cycles at L* = 1,900); Sec. 4.3.

**Evidence:** The HUST grid extends to 1,000 cycles. The best single checkpoint was cycle 300 (61.5% saved, Sec. 4.4). Mean time to decision is 857 cycles.

**Fix:** Report the share decided by cycle 100 and by cycle 300 for HUST. Avoid calling decisions at 800–1,000 cycles "early-cycle" decisions.

### 11. (Minor) The laboratory-shift claim overstates generality
**Location:** Sec. 4.6 "Laboratory shift"; Sec. 5 (iii).

**Evidence:** Both laboratories tested the same A123 APR18650M1A cell type. The "shift" is mainly a change of charge/discharge protocol family and test equipment, not of cell design or manufacturer. The point-prediction rule was still badly invalid (0.519 / 0.605), and the valid proposed rule saved only 23.9%.

**Fix:** Call this "cross-laboratory, same cell type". State that cross-manufacturer and cross-chemistry transfer is untested.

### 12. (Minor) The chemistry limitation is weakly argued and unprofessionally worded
**Location:** Sec. 6, first bullet.

**Evidence:**
- The bullet says other data sets were "not reachable from our computing environment (HTTP 403 and an interactive browser challenge)". This is not a scientific reason, and reviewers will read it as a convenience sample.
- The more important point is missing: the ΔQ(V) / ΔV(q) features exploit LFP's flat plateau and fast-charge plating signatures. NMC, NCA and Si-containing anodes show different knee mechanisms and a different capacity-fade onset, so efficiency, and the number of bad calibration cells available at a given L*, may differ substantially.

**Fix:** Remove the access wording. Explain why only LFP was used. Name the specific data sets that would test transfer (e.g. NMC/NCA cycling sets, Sandia) as future work, and discuss the chemistry-specific feature assumptions.

### 13. (Minor) The recommended workflow lacks practitioner guidance
**Location:** Sec. 5 "Recommended workflow".

**Evidence:**
- Step 2 ("train on any available historical cells") ignores the efficiency loss from out-of-population training: 23.9% vs 47.0% in cross-laboratory training (Sec. 4.6).
- Step 3 ignores prevalence (Issue 4).
- No guidance is given on choosing α versus β from the costs of a false pass and a false reject.
- No guidance is given on aligning checkpoints with the RPT schedule.

**Fix:** Expand the workflow with these points and a worked example: number of cells, calibration duration, expected break-even (Issue 3).

### 14. (Minor) Small inconsistencies
**Location:** Sec. 3.5, Table 1, Tables 2–3, Sec. 4.3, Sec. 1, references.

**Evidence and fixes:**
- Sec. 3.5 says "72 fast-charging policies". Table 1 lists 69 MATR protocols (+9 CLO = 78 groups in E9). State that 72 is the original count and 69 remain after cleaning.
- Table 1 HUST median "1875" is unformatted; the other values use thousands separators ("1,875").
- Proposed-rule mean cycles differ between Table 2 and Table 3 (857 vs 854 on HUST; Bonferroni 1,737 vs 1,739), and Sec. 4.3 mixes them ("857 instead of 1,739"). Explain the split-mean versus cell-mean averaging, or use one consistently.
- The introduction's "weeks to months" should give the per-cycle duration, so readers can convert cycles to time.
- Reference [19] has no authors (Vovk, Gammerman, Shafer).
