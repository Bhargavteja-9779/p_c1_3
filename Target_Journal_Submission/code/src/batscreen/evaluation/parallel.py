"""Run many splits in parallel (joblib, all CPU cores) and collect results."""
from __future__ import annotations
import os
import pandas as pd
from joblib import Parallel, delayed
from .runner import run_split

CELL_COLS = ["split", "model", "method", "cell", "decision", "by_model", "time", "m_idx"]


def run_many(F, Lstar, fractions, alpha, beta, model, seeds, n_jobs=-1, keep_cells=False, **kw):
    out = Parallel(n_jobs=n_jobs, backend="loky")(
        delayed(run_split)(F, Lstar, fractions, alpha, beta, model, s, keep_cells=keep_cells, **kw) for s in seeds)
    rows = [r for o in out for r in o[0]]
    cells = [c for o in out for c in o[1] if c[2] != "__score__"]
    scores = [c for o in out for c in o[1] if c[2] == "__score__"]
    cdf = pd.DataFrame(cells, columns=CELL_COLS)
    if scores:
        cdf.attrs["scores"] = pd.DataFrame(scores, columns=["split", "model", "_", "cell", "m", "S", "yhat", "scale"]).drop(columns="_")
    return pd.DataFrame(rows), cdf
