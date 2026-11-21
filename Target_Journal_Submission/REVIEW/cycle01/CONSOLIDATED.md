# Review cycle 1 — consolidated findings and decisions

Ten independent reviews (R1 theory, R2 battery domain, R3 experimental design, R4 code, R5 reproducibility,
R6 numbers, R7 citations, R8 novelty, R9 presentation, R10 sceptical editor), written against the draft of
2026-11-21 02:10 (old section numbering 4.x/5). Since then the manuscript was merged with the restructured version
(3 Results and Discussion, 3.1-3.12; proof in SI S5). Recommendations: 3 minor (R1, R4, R5, R7 minor), 6 major.
No CRITICAL finding. Core theory (Prop. 1, ranks, truncation, PAC minimum n=22) and code verified correct
(R1, R4); headline numbers reproduce bit-identically from a clean clone (R5) and from raw data (R3, R6).

Severity in brackets = highest given by any reviewer; "×n" = number of reviewers raising it independently.

## A. Claims that must change (no new experiment)
| ID | Issue | Raised by | Decision |
|---|---|---|---|
| A1 | "Guaranteed error rates" overclaims a marginal guarantee; FRR>0.10 in 31%/24% of splits not reported; ≥1 rate >0.10 in 51%/43% | R10-01, R1, R4-07 [MAJOR ×3] | Retitle ("distribution-free error control"); report per-split exceedance for FPR, FRR and either; abstract states the guarantee is on average over calibration sets |
| A2 | Laboratory-shift failure never tested (E5 cross-lab always calibrates on HUST) | R3-01, R6-01, R10-05 [MAJOR ×3] | Remove the lab-shift failure claim everywhere; say cross-lab with target calibration stayed valid |
| A3 | "Every rule failed on later batches" false (point rule valid on b3); b3 rates rest on 1-3 fixed bad test cells; "restored validity" trivial when rule cannot pass | R3-02, R6-02/03, R10-05 [MAJOR ×3] | Correct sentence; report n bad/good test cells per arm; say which arms cannot pass |
| A4 | PAC variant used but never defined | R1-01, R6-06, R9-02 (+R3-07) [MAJOR ×4] | Define in Methods 2.4 (rank, δ=0.10, i.i.d. assumption, n≥22); explain E10 metric is a split-level proxy |
| A5 | Wrong explanation for rates < 0.10 ("max is conservative"); bound nearly tight; gap = bad cells rejected/failing first | R1-02 [MAJOR] | Rewrite with attained rank level (0.081/0.076) |
| A6 | Calibration speed-up quoted only for MATR/CLO (2.61; HUST 1.38) and ignores training cells cycled to EOL (whole campaign ≈1.04×); cost metric mixes wall-clock and cell-cycles | R3-06, R6-05, R9-04, R10-04, R2-02 [MAJOR ×5] | Quote both data sets; state that the saving applies to the calibration campaign and that the regression model's training cells still need EOL (or use the truncated classifier); define cell-cycles vs wall-clock; report share of splits in which the screening campaign ends before L* |
| A7 | Efficiency comparisons: point and parametric rules valid and as fast on MATR/CLO; parametric faster per cell (Wilcoxon) | R6-04, R3-04, R10-02 [MAJOR ×3] | State plainly; abstract no longer implies the proposed rule is the fastest valid rule |
| A8 | Parametric rule has no multiplicity correction and uses an optimistically small s_k; its failures are partly the repeated-looks effect | R3-04, R4-01, R10-03 [MAJOR ×3] | Rename "Gaussian threshold at every look"; add multiplicity-aware Gaussian comparator (B2); state s_k bias; soften "model-based uncertainty is not a substitute" |
| A9 | Interval rule targets a stricter goal (realised 5-10× below target); truncation advantage is shared with conformalised survival methods | R3-05, R10-03, R7-03, R8-03 [MAJOR ×4] | Say so explicitly; credit truncation to classifying on Z / Candès et al.; drop it as a novelty claim |
| A10 | Novelty/gap overstated; closest prior art missing (sequential/any-stage conformal, max-over-time scores, Learn-then-Test, group-sequential designs, battery conformal work) | R7-02/03, R8-01..04, R10-10, R2-05 [MAJOR ×4] | Rewrite 1.1 gap: contribution = applying trajectory (max-statistic) calibration to battery screening with truncated calibration + extensive empirical characterisation; cite only prior art verified to exist |
| A11 | "Per-cell" guarantee vs class-conditional | R8-04 | Use "class-conditional" consistently |
| A12 | MATR/CLO batch confound; per-batch error rates above 0.10 (b1 good FRR 0.157, CLO bad FPR 0.132) | R2-03 [MAJOR] | Report per-batch rates (computed from E1 cells); discuss as conditional-on-subgroup limitation |
| A13 | EOL definition described as same convention but means different things physically | R2-04 [MAJOR] | Correct description |
| A14 | Use case: per-cell screening vs lot/design qualification | R2-01, R10-08 [MAJOR ×2] | State the decision unit and the use cases explicitly (test-matrix pruning, cell grading); acknowledge lot-level qualification as different problem |
| A15 | Cell-level Wilcoxon/bootstrap ignore protocol clustering; tests disagree | R1-03, R3-03 [MAJOR ×2] | Protocol-cluster bootstrap for MATR/CLO (HUST: cells have distinct protocols); report where conclusions change |
| A16 | E9 described as satisfying the guarantee | R4-02 | Describe as stress test outside the assumptions |
| A17 | Methods omit E3-E12 designs; "200–333 splits" wrong | R3-09, R6, R9, R5 | Methods 2.6 lists designs; fix split counts |

## B. New or extended experiments
| ID | What | Why | Cost |
|---|---|---|---|
| B1 | Fair single-checkpoint comparator: checkpoint chosen on training cells only. Computed from E12's training-only grid estimates restricted to single-checkpoint grids, looked up in E3 (same split seeds) | R10-02/03, R8-05 [MAJOR ×3] | none (post hoc, valid) |
| B2 | Multiplicity-aware Gaussian rule (z at α/M, β/M) | R3-04, R10-03 | add method; run on E1 seeds, 200 splits (E13) |
| B3 | Bonferroni on sparse 2-4-checkpoint grids | R10-03, R8-05 | add `bonf` to E3 methods; rerun E3 (~5 min) |
| B4 | Correlated (per-cell constant) test-only noise | R3-08 | add E4 variant |
| B5 | Per-split exceedance and per-batch rates | A1, A12 | analysis only |

## C. Presentation (R9, R6)
Method intuition + cite Fig. 1; m/k notation; tables readable in PDF (main tables trimmed, SI tables formatted with
readable column names); SI numbering; figure file names vs numbers; code labels in figures; Fig. 9 caption; cut
~1,000-1,500 words; abstract numbers.

## D. References (R7)
Holm 1979 cited; published versions instead of arXiv (partly done on gifted-euler); Vovk authors; verify #14, #31;
Severson 9.1% statement (full model, one outlier excluded).

## E. Reproducibility (R5)
`run_all.py --mode full` from a clone reuses committed results: document `--force` and print a clear message; add
LICENSE (MIT, per README); pin versions (requirements-lock.txt from the environment used; Python 3.13); document
pandoc + LibreOffice (+ libreoffice-math) for render.py; Data Availability placeholder (needs archive DOI from the
authors).
