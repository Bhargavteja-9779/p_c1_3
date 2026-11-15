"""Sequential decision simulation and screening metrics."""
from __future__ import annotations
import numpy as np


def simulate(S, T, checkpoints, pass_thr, rej_thr, Lstar):
    """Return dict of arrays: decision (+1 pass, -1 reject), by_model (bool),
    time (cycles cycled until the decision), m_idx (checkpoint index or -1)."""
    n, M = S.shape
    dec = np.zeros(n, int); t = np.zeros(n); by_model = np.zeros(n, bool); midx = np.full(n, -1)
    for i in range(n):
        for m, k in enumerate(checkpoints):
            if T[i] <= k:  # failure observed before reaching checkpoint m
                dec[i], t[i] = -1, T[i]; break
            s = S[i, m]
            if np.isfinite(s) and s > pass_thr[m]:
                dec[i], t[i], by_model[i], midx[i] = 1, k, True, m; break
            if np.isfinite(s) and s < rej_thr[m]:
                dec[i], t[i], by_model[i], midx[i] = -1, k, True, m; break
        else:  # undecided after the last checkpoint: observe until failure or L*
            if T[i] < Lstar:
                dec[i], t[i] = -1, T[i]
            else:
                dec[i], t[i] = 1, Lstar
    return dict(decision=dec, by_model=by_model, time=t, m_idx=midx)


def metrics(res, T, Lstar):
    good = T >= Lstar; bad = ~good
    dec = res["decision"]
    fp = (dec == 1) & bad; fr = (dec == -1) & good
    full_cost = np.minimum(T, Lstar)
    return dict(
        n_bad=int(bad.sum()), n_good=int(good.sum()),
        false_pass=int(fp.sum()), false_reject=int(fr.sum()),
        fpr=fp.sum() / max(bad.sum(), 1), frr=fr.sum() / max(good.sum(), 1),
        accuracy=float(((dec == 1) == good).mean()),
        early_rate=float(res["by_model"].mean()),
        mean_time=float(res["time"].mean()),
        time_saving=float(1 - res["time"].sum() / full_cost.sum()),
    )
