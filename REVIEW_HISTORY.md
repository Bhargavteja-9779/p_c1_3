# REVIEW_HISTORY

## Pre-review (before review cycle 1)
* 2026-11-15 16:42 — self-detected evaluation flaw: calibration/test sets stratified separately broke exact within-class
  exchangeability (single-checkpoint FPR 0.101 vs exact theory 0.095). Fixed in runner.stratified_split; all main
  experiments rerun.
* 2026-11-16 09:12 — workflow prep-audit-build launched (3-lens methods/code pre-review with adversarial verification,
  citation and claim audit, two novelty sweeps).

## Review cycles
(Each cycle: ten independent reviewer agents -> consolidation -> fixes -> re-experimentation -> manuscript revision.
Files: Target_Journal_Submission/REVIEW/cycleNN/.)
