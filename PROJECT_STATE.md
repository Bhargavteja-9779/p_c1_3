# PROJECT_STATE

Last update: 2026-11-21 11:30 UTC (session 3)

## HOW TO RESUME IN A NEW SESSION / ACCOUNT (read first)
1. `git checkout claude/awesome-cori-k15frg && git pull`
2. If the experiment run is not finished (check the last lines of the newest
   `Target_Journal_Submission/results_full_stdout*.log` for `INFO finished`):
   `bash tools/resume_run.sh` (installs pinned packages, runs tests, restarts the run;
   finished chunks in `results/raw/chunks/` and finished `results/raw/E*_splits.csv` are re-used).
   Optionally `setsid nohup bash tools/autosave.sh >/dev/null 2>&1 &` to auto-commit/push every 10 min.
3. Raw data is NOT needed: feature tables are in `Target_Journal_Submission/data/features/`.
4. Then continue with "Next steps" below.

## Run status (session 3, 2026-11-21)
* Container was reset; packages reinstalled at the versions of the earlier run.
* Relaunched 10:52 UTC (log results_full_stdout5.log). E1 reused; E2 completed 11:18 (all models);
  E3 completed ~11:25; E4-E7, E9, E10, analysis, figures pending at time of writing.
* Reference fixes (holm1979, hust_data, romano2019cqr, pedregosa2011sklearn) and Fig. 1 placed in Methods 3.3.
* Note: REVIEW/ outputs of the session-2 workflow (prep-audit-build) were lost with the container; not in git.

## Selected target journal
Battery Energy (Wiley; eISSN 2768-1696). See Target_Journal_Submission/journal_selection/.

## Selected topic
Distribution-free sequential screening of Li-ion cell cycle life: early pass/reject decisions
with guaranteed false-pass/false-reject rates under data-dependent early termination, calibrated
with campaigns truncated at the specification L*.

## Data
* MATR+CLO (169 cells; data.matr.io) and HUST (77 cells; Mendeley nsc7hnsg4s) downloaded to
  /home/user/data_raw (NOT in git; re-download with code/src/batscreen/data/download.py).
* Processed caches: /home/user/data_raw/processed/*.npz (scripts/preprocess.py).
* Feature tables (in git): Target_Journal_Submission/data/features/*.npz.

## Code
Target_Journal_Submission/code (package batscreen, run_all.py quick/full).

## Experiment status
* Pilot (seeds 1000-1099) done; design frozen in literature/research_design.md.
* 16:42 evaluation flaw (calibration/test exchangeability) fixed; full run restarted 16:45.
* E1 MATR+CLO finished 16:53 (results/raw/E1_matr_clo_*). The session worker was restarted
  afterwards (process killed, files intact). Suite made resumable (existing outputs skipped);
  E1 HUST finished 22:21; container restarted again (usage-limit pause) and E2 was lost.
* 09:11 Nov 16: full run relaunched with per-chunk checkpoints (log: results_full_stdout3.log).
* Manuscript draft part 1 (front matter, introduction, related work, methods) in
  Target_Journal_Submission/manuscript/src/.

## Agents / workflows
* 09:12 workflow `prep-audit-build` (run wf_15c1a175-b64): build pipeline (manuscript/build/), bibliography verification
  (literature/references_final.json, REVIEW/citation_audit_bibliography.md), claim checks (REVIEW/citation_audit_claims.md),
  novelty sweeps (REVIEW/novelty_sweep_*.md), 3-lens methods/code pre-review (REVIEW/prereview_*.md) with adversarial
  verification of serious findings. Resume: Workflow({scriptPath: <session workflows dir>/prep-audit-build-wf_15c1a175-b64.js,
  resumeFromRunId: "wf_15c1a175-b64"}).

## Next steps (exact)
1. Finish the full run (see resume instructions above).
2. Parallel agents: citation audit + reference list; manuscript render/DOCX pipeline.
3. When results complete: build_numbers -> results/discussion sections -> first full manuscript.
4. Ten-reviewer cycle 1 (agents), consolidate, fix, rerun affected experiments; further cycles.
5. DOCX/PDF, cover letter, audits, manifest, risk report, decision.
