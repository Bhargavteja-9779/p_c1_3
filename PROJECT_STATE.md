# PROJECT_STATE

Last update: 2026-11-15 16:35 UTC

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
* Full run started 16:33 (E1-E7 + analysis) -> results/, tables/.

## Next steps
1. Wait for full run; write figures module; inspect results.
2. Literature matrix; manuscript draft (Wiley/Battery Energy structure).
3. Review cycles (10 reviewer perspectives), revisions, DOCX, cover letter, audits.
