#!/usr/bin/env bash
# Resume the full experiment run in a fresh container/account.
# Completed chunks (results/raw/chunks/*.csv) and finished experiment files are re-used;
# only missing work is recomputed. Raw data is NOT needed (feature tables are in git).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
pip install --break-system-packages -q numpy==2.5.3 scipy==1.18.1 scikit-learn==1.9.1 pandas h5py pyyaml joblib matplotlib tabulate python-docx pytest
pip install --break-system-packages -q torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu
cd "$ROOT/Target_Journal_Submission/code"
python3 -m pytest -q tests
n=$(ls ../results_full_stdout*.log 2>/dev/null | wc -l); LOG="../results_full_stdout$((n+1)).log"
setsid nohup python3 run_all.py --mode full --stages experiments analysis figures > "$LOG" 2>&1 < /dev/null &
echo "run started, log: Target_Journal_Submission/${LOG#../}"
