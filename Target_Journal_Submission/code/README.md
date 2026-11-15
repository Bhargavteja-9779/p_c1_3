# batscreen — distribution-free sequential screening of Li-ion cell cycle life

Code for the manuscript *"Stopping cycle-life tests early with guaranteed error rates:
distribution-free sequential screening of lithium-ion cells from truncated test
campaigns"* (submitted to *Battery Energy*).

The method decides, at a sequence of early checkpoints (e.g. after 20, 30, ..., 300
cycles), whether a cell will meet a cycle-life specification L* (pass), will not
(reject), or needs more cycles (continue). Thresholds are calibrated on the
maximum over checkpoints of normalised model scores, which bounds the per-cell
false-pass and false-reject probabilities by alpha and beta under *any* data-dependent
stopping time, and needs calibration cells cycled only to min(T, L*).

## 1. Installation

```bash
conda env create -f environment.yml && conda activate batscreen
```
or
```bash
pip install -r requirements.txt
```
Python >= 3.10. CPU is sufficient (all paper results were produced on 4 CPU cores);
`batscreen.utils.detect_device()` uses CUDA or Apple-Silicon MPS for the CNN baseline if
available.

## 2. Data

Both datasets are public and downloaded by script (no registration):

| Dataset | Cells | Source | Size |
|---|---|---|---|
| MATR (Severson et al., Nat. Energy 2019) + CLO (Attia et al., Nature 2020) | 124 + 45 | https://data.matr.io/1/ (4 `.mat` batch files) | 10.9 GB |
| HUST (Ma et al., Energy Environ. Sci. 2022) | 77 | Mendeley Data doi:10.17632/nsc7hnsg4s.2 | 1.2 GB |

```bash
export BATSCREEN_RAW=/path/with/15GB/free           # default /home/user/data_raw
export BATSCREEN_PROCESSED=$BATSCREEN_RAW/processed
python -c "import sys; sys.path.insert(0,'src'); from batscreen.data.download import download_all; download_all('$BATSCREEN_RAW')"
python scripts/preprocess.py --raw $BATSCREEN_RAW --out $BATSCREEN_PROCESSED   # ~1 min, ~250 MB RAM
python scripts/build_features.py                                              # writes ../data/features/*.npz
```
`run_all.py` performs these steps automatically if the caches are missing. The
checkpoint feature tables used in the paper are already included in
`../data/features/` (small), so experiments can be re-run without the raw data.

Data cleaning (documented in `src/batscreen/data/matr.py`, verified in code):
Severson batch-1 cells 8, 10, 12, 13, 22 removed (never reached end of life); batch-1
cells 0-4 merged with their batch-2 continuations; batch-3 cells 2, 23, 32, 37, 42, 43
removed (noisy/incomplete channels); internal-resistance features not used because the
CLO batch has no IR records. HUST pickles are read with an allow-listed unpickler
(`src/batscreen/data/safe_pickle.py`).

## 3. Reproduce everything

```bash
python run_all.py --mode quick    # pipeline check, ~10 min, writes ../results_quick etc.
python run_all.py --mode full     # all reported experiments, ~1.5-2 h on 4 cores
```
Outputs: `../results/` (raw split-level CSVs in `raw/`, `metrics.json`, `statistics.json`,
`raw_results.csv`, logs in `experiment_logs/`), `../tables/` (Markdown + CSV),
`../figures/` (PNG 300 dpi + PDF). The manuscript numbers are produced by
`../manuscript/build_numbers.py` from these files.

| Experiment | Script function | Question |
|---|---|---|
| E1 | `experiments/suite.py:e1_main` | validity and efficiency of all screening rules (elastic net, 1,000 splits per dataset) |
| E2 | `e2_models` | base predictors: logistic (truncated training), GBR, RF, GP, 1-D CNN |
| E3 | `e3_ablation` | checkpoint grids, normalisation, trajectory vs per-checkpoint calibration |
| E4 | `e4_robustness` | calibration-set size, training-set size, feature noise (cal+test vs test only) |
| E5 | `e5_shift` | batch shift (b1+b2 -> b3 / CLO) with/without target recalibration; MATR -> HUST |
| E6 | `e6_compute` | run time, peak memory |
| E7 | `e7_sensitivity` | alpha/beta, specification L* |
| E8 | `analysis.py` | error analysis per cell, batch, margin |

## 4. Using the method on your own cells

```python
from batscreen.screening.calibration import calibrate
from batscreen.screening.procedure import simulate
# S_cal: [n_cal, M] normalised scores (NaN after a cell's failure); Z_cal = 1{T >= L*}
pass_thr, rej_thr = calibrate(S_cal, Z_cal, alpha=0.1, beta=0.1, method="traj")
# at checkpoint m: pass if S > pass_thr[m]; reject if S < rej_thr[m]; else keep cycling
```

## 5. Tests

```bash
python -m pytest tests -q
```
`tests/test_calibration.py` checks finite-sample validity on synthetic exchangeable data
and that naive per-checkpoint calibration inflates the error; `tests/test_features.py`
checks that features at checkpoint k never use cycles > k.

## 6. Layout

```
code/
  run_all.py                 entry point (quick / full)
  config/                    default.yaml (full), quick.yaml
  scripts/                   preprocess.py, build_features.py
  src/batscreen/
    data/                    matr.py, hust.py, safe_pickle.py, download.py, processed.py
    preprocessing/features.py
    models/                  base.py (EN, logistic, GBR, RF, GP), cnn.py
    screening/               calibration.py (proposition + rules), procedure.py
    evaluation/              runner.py, parallel.py
    statistics/tests.py
  experiments/               suite.py (E1-E7), analysis.py (stats, tables, E8), figures.py
  tests/
```

## 7. License and citation
Code: MIT. Data: see the original licences of the dataset providers.
