# PROJECT_STATE  (read this first when resuming in a new session)

Last update: 2026-11-20 22:55 UTC (handover to new account). Branch: `claude/gifted-euler-vaa8g2`; keep committing and pushing to it.

## How to resume (new session / new account)
1. `cd Target_Journal_Submission/code && pip install -r requirements.txt`. The experiments need only the feature tables
   in `../data/features/*.npz`, which are in git. Raw data are NOT needed unless you rebuild the features.
2. Relaunch the full run. It resumes: finished chunks in `results/raw/chunks/` and finished experiment files are
   re-used.
   `setsid nohup python3 run_all.py --mode full --stages experiments analysis figures > ../results_full_stdout6.log 2>&1 &`
   E1-E11 are registered in `run_all.py`; E11 = physical interpretation (added 2026-11-20).
3. When `results/raw/` holds E2-E11 outputs, run `python3 ../manuscript/build_numbers.py`, then continue with the
   open tasks below.
4. Commit `results/raw/chunks/*.csv` regularly, so that chunks finished before an interruption are kept.

## Decisions (fixed)
* Target journal: **Battery Energy** (Wiley, eISSN 2768-1696). The user confirmed it on 2026-11-20 even though the
  median submission-to-acceptance time is 85-86 d, above their 72-d limit (see journal_selection/selected_journal.md).
* Topic: distribution-free sequential (trajectory-calibrated) screening of Li-ion cell cycle life with
  false-pass/false-reject guarantees under early stopping; calibration needs cells cycled only to L*.
* Data: MATR+CLO (169 cells, L*=750) and HUST (77 cells, L*=1900).
* User priorities: avoid desk rejection for low novelty or poor fit; write like accepted Battery Energy papers
  (Introduction, Methods, Results and Discussion, Conclusions; concrete numbers; physically motivated
  interpretation; practical test-time savings).

## Done
* Journal selection and the 72-d re-check; journal-paper benchmark (journal_selection/journal_benchmark.md).
* Code package, E1 (1,000 splits per dataset), E2 partial chunks, figures for E1.
* 2026-11-20:
  * new prior art cited: wu2026cai (Algorithms 2026, conformal intervals for early life), zhang2023range (IEEE TTE),
    lei2015functional, diquigiovanni2022bands;
  * E11 interpretation experiment + Fig15 + build_numbers keys E11.*; Graphical_Abstract figure;
  * manuscript restructured: 1 Introduction (1.1 prior work, 1.2 contributions), 2 Methods (2.1 data ... 2.6
    protocol), 3 Results and Discussion (3.1-3.3 written; 3.4-3.8 = {{SECTION_E2_E10}} placeholder still to write;
    3.9 physical basis written but claims must be checked against full E11; 3.10 error analysis; 3.11 implications;
    3.12 limitations), 4 Conclusions; proof moved to SI S5.

## Open tasks (in order)
1. Finish the full run (E2 HUST gbr/rf, E3, E4, E5, E6, E7, E9, E10, E11, analysis, figures).
2. Replace {{SECTION_E2_E10}} in manuscript/src/part2_results.md with subsections 3.4 base predictors (E2), 3.5 grid
   ablation (E3), 3.6 robustness + sensitivity (E4, E7), 3.7 batch/lab shift + protocol-disjoint (E5, E9),
   3.8 PAC (E10) + compute (E6). Use only {{KEY}} tokens from results/manuscript_numbers.json.
3. Fix the old "Section 4.x"/"Section 5" cross-references in parts 1-3: 4.3->3.4, 4.4->3.5, 4.5->3.6/3.8, 4.6->3.7,
   4.8->3.10, 5->3.11.
4. Citation fixes in literature/references_verified.json:
   * years: bte2024cnnlstm -> 2025 (print), sadinle2019lab -> 2019;
   * replace arXiv entries with the published versions:
     * jin2023selection: JMLR 24(244):1-41, 2023;
     * romano2019cqr: NeurIPS 32, 2019, pp. 3538-3548;
     * gibbs2021aci: NeurIPS 34, 2021;
     * pedregosa2011sklearn: JMLR 12:2825-2830, 2011;
     * gui2024adaptive: Biometrika 111(2):459-477, 2024, doi 10.1093/biomet/asad076;
     * tibshirani2019shift, jazbec2024earlyexit (NeurIPS 2023?), sesia2025dr, zhang2024batteryml (ICLR 2024?):
       VERIFY before changing;
   * hust_data and holm1979 entries have no metadata: complete them (Holm 1979, Scand. J. Statist. 6(2):65-70).
5. Render: `python3 manuscript/build/render.py --pdf --si`, then check with `manuscript/build/check_docx.py`.
6. Ten review rounds -> REVIEW/review_01..10.md + final_audit.md; fix the issues and rerun experiments where needed.
7. Final DOCX/PDF, cover letter (manuscript/src_cover), manifest, rejection-risk report, READY/NOT READY decision.

## Status at handover (22:55 UTC)
* Finished and committed: E1, E2 (all models), E3. E4 was running when the session ended. Relaunch the run command
  above; finished chunks are re-used, and E4-E11, analysis and figures will run.
* Section 3.4 (E2) is drafted in manuscript/drafts/sec3_4_base_predictors.md. Paste it in place of
  {{SECTION_E2_E10}}, before 3.5. Its claims were checked against the E2 results: valid with every model except
  CNN/HUST FRR 0.113 (30 splits); GP Bayesian rule HUST FPR 0.274 / FRR 0.362; trajectory rule beats single-cp100 with
  every model except EN on MATR/CLO.
* E3 finding, to be reported honestly in 3.5 and in the discussion:

  | Data set | Grid | Saved | FPR | FRR |
  |---|---|---|---|---|
  | MATR/CLO | dense 16-checkpoint grid | 79.4% | | |
  | MATR/CLO | sparse {50,100,200,300} | 84.3% | 0.071 | 0.076 |
  | MATR/CLO | single 50 | 81.9% | | |
  | HUST | dense 17-checkpoint grid | 52.6% | | |
  | HUST | sparse {100,300,600,1000} | 56.8% | | |
  | HUST | single 300 | 61.5% | | |

  Many looks cost efficiency. The best single checkpoint is unknown in advance and differs between data sets. Recommend
  a sparse grid. Optional extra experiment (E12): choose the grid by inner CV on training cells only, which keeps the
  guarantee.
* The background auto-commit script was in /tmp and is gone after a restart. Commit manually.

## Status 2026-11-21 13:00 UTC
* Run relaunched (log: Target_Journal_Submission/results_full_stdout6.log). It was at E4 HUST noise when this note was
  written.
* NEW E12 (grid chosen on training cells only; runner.select_grid_on_training; suite.e12_selected_grid; analysis
  T14/T15; build_numbers E12.*). It runs after the main run:
  `python3 run_all.py --mode full --stages experiments analysis figures --experiments E12` (log results_full_stdout7.log).
  If the session dies, relaunch the main command first (it resumes), then this one.
* Drafts ready in manuscript/drafts/: sec3_4_base_predictors.md, sec3_5_grid.md, sec3_6_robustness.md (E4 part
  written; E7 sensitivity still to add). Still to write: 3.7 shift (E5, E9), 3.8 PAC (E10) + compute (E6), the E12
  paragraph in 3.5, and the E7 paragraph in 3.6. Then assemble them in place of {{SECTION_E2_E10}}.
* E4 finding: noise on test cells only breaks validity for every rule (exchangeability violated). Report it as a
  limitation: calibrate on the same tester and protocol.
