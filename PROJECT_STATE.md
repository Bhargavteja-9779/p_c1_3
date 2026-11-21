# PROJECT_STATE

Last update: 2026-11-21 08:00 UTC

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

* 2026-11-21 07:58: new container (raw data and prep-audit-build workflow outputs gone; REVIEW/ never committed).
  Deps reinstalled; full run resumed from chunks (log: results_full_stdout5.log). Raw data not needed (features in git).

## Agents / workflows
* 09:12 workflow `prep-audit-build` (run wf_15c1a175-b64): build pipeline (manuscript/build/), bibliography verification
  (literature/references_final.json, REVIEW/citation_audit_bibliography.md), claim checks (REVIEW/citation_audit_claims.md),
  novelty sweeps (REVIEW/novelty_sweep_*.md), 3-lens methods/code pre-review (REVIEW/prereview_*.md) with adversarial
  verification of serious findings. Resume: Workflow({scriptPath: <session workflows dir>/prep-audit-build-wf_15c1a175-b64.js,
  resumeFromRunId: "wf_15c1a175-b64"}).

## Next steps (exact)
1. Full run (resumed 2026-11-21 07:58, log results_full_stdout5.log): E2 remaining chunks (hust gbr, rf),
   then E3, E4, E5, E6, E7, E9, E10, analysis, figures. If the container was reset: follow CLAUDE.md step 3
   (completed chunks in results/raw/chunks are re-used).
2. When results complete: `python manuscript/build_numbers.py` -> write Results for E2-E10 in
   manuscript/src/part2_results.md (only E1 written) -> update Discussion (part3) -> render via manuscript/build/render.py.
3. Redo the lost pre-review/citation audit (prep-audit-build); save outputs to Target_Journal_Submission/REVIEW/ and commit.
4. Ten-reviewer cycle 1 (agents), consolidate, fix, rerun affected experiments; further cycles.
5. DOCX/PDF, cover letter, audits, manifest, risk report, decision.
