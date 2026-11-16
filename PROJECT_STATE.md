# PROJECT_STATE

Last update: 2026-11-16 09:12 UTC

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

## Next steps (exact)
1. Monitor relaunched full run (log: Target_Journal_Submission/results_full_stdout2.log).
2. Parallel agents: citation audit + reference list; manuscript render/DOCX pipeline.
3. When results complete: build_numbers -> results/discussion sections -> first full manuscript.
4. Ten-reviewer cycle 1 (agents), consolidate, fix, rerun affected experiments; further cycles.
5. DOCX/PDF, cover letter, audits, manifest, risk report, decision.
