# Review cycle 1 — shared brief for all reviewers

You are one of ten independent reviewers of a manuscript prepared for submission to *Battery Energy* (Wiley).
Each reviewer has a different lens (given in your own prompt). Be rigorous and adversarial: your job is to
find real problems before the journal's reviewers do, not to praise. Do not soften findings.

## Paper
"Stopping Cycle-Life Tests Early With Guaranteed Error Rates: Distribution-Free Sequential Screening of
Lithium-Ion Cells From Truncated Test Campaigns". At checkpoints (e.g. cycle 20..300) a cell is passed,
rejected or kept on test; thresholds are calibrated on the maximum over checkpoints of normalised model
scores of calibration cells, which bounds false-pass/false-reject probabilities under data-dependent stopping,
and calibration cells need only be cycled to min(T, L*). Data: MATR/CLO (169 cells) and HUST (77 cells).

## Where things are (root: /home/user/p_c1_3/Target_Journal_Submission)
* Rendered manuscript (read this first): manuscript/Draft_Manuscript.md (numbers filled in),
  manuscript/Supporting_Information.md; PDF: manuscript/Draft_Manuscript.pdf (33 pp).
* Manuscript sources with {{TOKENS}}: manuscript/src/*.md; numbers: results/manuscript_numbers.json, built by
  manuscript/build_numbers.py; render: manuscript/build/render.py.
* Code: code/ (package code/src/batscreen; screening/calibration.py, screening/procedure.py,
  evaluation/runner.py, preprocessing/features.py, data/*.py; experiments/suite.py, analysis.py, figures.py;
  run_all.py; config/default.yaml; tests/).
* Results: results/raw/*.csv(.gz) and results/raw/chunks/ (split-level), results/metrics.json,
  results/statistics.json, tables/*.md|csv, figures/*.png. Experiment log: ../EXPERIMENT_LOG.md.
* Literature: literature/ (references_verified.json, literature_matrix.md, research_design.md, topic_selection.md).
* Journal choice: journal_selection/selected_journal.md.
* Raw data are NOT present in this container (features in data/features/*.npz are).
* Python env is installed (numpy, scipy, sklearn, torch, pandas). You may run code and small checks
  (4 CPU cores shared with nine other reviewers: keep jobs short, < 5 min, no full re-runs).

## Rules
* Do NOT modify any file except your own report. Write ONLY REVIEW/cycle01/<your id>.md.
* Every finding: ID (e.g. R3-07), severity (CRITICAL = invalidates a claim or result / MAJOR = a journal
  reviewer would require a change / MINOR / NIT), location (file:line or section), evidence (quote, number,
  command output), and a concrete fix. Verify before reporting: re-read the code or recompute the number.
  Mark anything you could not verify as UNVERIFIED.
* End the report with: overall recommendation (accept / minor / major / reject) as if you were a journal
  reviewer, and the 3 changes that matter most.
* Your final message back should be a ≤150-word summary: counts by severity and the top 3 findings.
