# EXPERIMENT_LOG

| Time (UTC) | Event |
|---|---|
| 15:31-15:39 | Downloaded MATR (4 batches, 10.9 GB) and HUST (1.19 GB); sizes match server Content-Length. |
| 15:47-15:52 | Preprocessing. First run failed: placeholder cycles with 2-element Qdlin arrays (fixed: keep NaN). Second run failed lifetime check: some batch-2 cells were cycled past EOL (check relaxed to lifetime <= len+2). |
| 15:56 | OOM when loading npz member-by-member (fixed: decompress each member once). |
| 15:58 | IR features dropped: CLO batch has no IR records (all zeros). |
| 16:00 | Defect found: Q(V) features at checkpoints 200/250 decorrelated from lifetime in CLO/batch-2 because specific cycles are non-standard (single-cycle glitches). Fix: element-wise median of Q(V) over cycles k-4..k (no look-ahead) and 8..12 for the reference. EN MAPE then decreases monotonically with checkpoint (30% at 20 cycles, 10.9% at 100, 7.2% at 300; 5 random 50/50 splits). |
| 16:02 | Pilot, 100 splits (seeds 1000-1099), EN, MATR+CLO L*=750: proposed FPR .066 FRR .075 saving .827; naive .148/.152; single_k100 .089/.047 .820; gauss .042/.041 .778; interval .012/.014 .560; bonf never decides. |
| 16:05 | Pilot HUST (100 splits), EN, L*=1900: proposed .068/.087 saving .527; single_k100 .071/.106 .423; gauss .092/.138; point_k100 .237/.395; naive .274/.258. Logit (truncated training) MATR 50 splits: proposed .074/.080 saving .719. |
| 16:10 | 40-split checks GBR (.105/.084) and GP (.089/.090) for the proposed rule; single split 3 hard for all models (EN .25 FPR) -> split variability, not a bug. |
| 16:30 | Quick mode end-to-end OK. Runner refactored to fit once per split and evaluate variants (grids, noise, alpha/beta); equivalence verified on split 1000. |
| 16:33 | FULL RUN started (seed_base 20261115). |
| 16:42 | **Evaluation flaw found and fixed.** In the first full E1 run, the single-checkpoint conformal rule had FPR 0.101 (95% CI 0.096-0.107), above its exact theoretical value (~0.095). Cause: calibration and test sets were both stratified by (dataset x class) with rounding, so the MATR/CLO mixture among bad cells differed between calibration and test, breaking within-class exchangeability. Fix: stratify only the training set; draw calibration/test uniformly from the remaining pool. Check (400 splits): single_k100 FPR 0.090 +- 0.009 vs exact theory 0.083. Aborted run deleted; full run restarted 16:46 with identical seeds. |
| 16:53 | E1 MATR+CLO completed (1000 splits, 449 s). |
| ~17:00-21:50 | Session worker restarted; background run killed (E1 HUST onward lost). Files intact. |
| 21:52 | Suite made resumable (outputs that exist are skipped; --force recomputes). Relaunched E1(HUST)-E7 + analysis + figures with setsid. |
| 22:21 (Nov 15) | E1 HUST completed (1000 splits, 1702 s under heavy CPU contention). E2 started. |
| 22:2x-09:03 | Container restarted (usage-limit pause); E2 lost; the three helper agents stopped by the usage limit before producing output. |
| 09:05 (Nov 16) | All long experiments now checkpoint per (dataset x configuration) chunk in results/raw/chunks/; quick-mode smoke test of E1-E10 + analysis passed. |
| 09:11 | Full run relaunched (E1 reused; E2, E3, E4, E5, E6, E7, E9, E10, analysis, figures). Secondary experiments use 200 splits (n_splits_secondary). E9 (protocol-disjoint splits) and E10 (PAC calibration) added after the design freeze. |
| 07:58-09:50 (Nov 21) | New container; full run resumed from chunks: E2 1614 s, E3 252 s, E4 2092 s, E5 697 s, E6 524 s, E7 924 s, E9 89 s, E10 516 s; analysis + all figures OK. build_numbers: 6915 values. |
