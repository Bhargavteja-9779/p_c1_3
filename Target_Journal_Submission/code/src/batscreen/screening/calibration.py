"""Threshold calibration for sequential go/no-go screening.

Scores S[i, m] (higher = more evidence that cell i is "good", i.e. T_i >= L*) are
available at checkpoints k_1 < ... < k_M < L* for cells still alive at k_m (NaN
otherwise). A procedure passes cell i at the first m with S[i,m] > pass_thr[m], rejects
at the first m with S[i,m] < rej_thr[m], otherwise continues (and is finally decided by
observing min(T_i, L*) cycles).

Proposition (trajectory calibration, method="traj"). Let the calibration cells and a
new cell be exchangeable within their class (bad: T < L*, good: T >= L*). Let
P_i = max_m S[i,m] over alive checkpoints for bad calibration cells, and
lam = P_(r), r = ceil((n0+1)(1-alpha)) (lam = +inf if r > n0). Then for a new bad cell,
P(the procedure ever passes it) <= P(P_new > lam) <= alpha, for ANY rule that passes
only when S > lam (the stopping time may depend on the cell's own data, rejection
rules, or the operator). Symmetrically, with R_i = max_m (-S[i,m]) over good
calibration cells and mu = R_(r1), r1 = ceil((n1+1)(1-beta)), P(false reject) <= beta.
Calibration therefore needs, per cell, only Z_i = 1{T_i >= L*} and the scores at
checkpoints < L*, i.e. each calibration cell must be cycled only to min(T_i, L*).
"""
from __future__ import annotations
import math
import numpy as np


def conformal_upper(values, level):
    """Smallest t with rank guarantee P(V_new > t) <= 1 - level for exchangeable V."""
    v = np.sort(np.asarray(values, dtype=float))
    v = v[np.isfinite(v) | (v == -np.inf)]
    n = v.size
    if n == 0:
        return np.inf
    r = math.ceil((n + 1) * level)
    if r > n:
        return np.inf
    return v[r - 1]


def _traj_max(S, alive):
    X = np.where(alive, S, -np.inf)
    return X.max(axis=1)


def calibrate(S_cal, Z_cal, alpha, beta, method="traj", single_index=None):
    """Return (pass_thr[M], rej_thr[M]).

    method: 'traj'   - proposed max-statistic calibration (valid under stopping)
            'naive'  - per-checkpoint marginal calibration at level alpha (not valid
                       for sequential use; included as a baseline)
            'bonf'   - per-checkpoint calibration at alpha/M (valid, conservative)
            'single' - only checkpoint `single_index` is used (valid)
    """
    S_cal = np.asarray(S_cal, float)
    alive = np.isfinite(S_cal)
    M = S_cal.shape[1]
    bad, good = (Z_cal == 0), (Z_cal == 1)
    pass_thr = np.full(M, np.inf); rej_thr = np.full(M, -np.inf)
    if method == "traj":
        lam = conformal_upper(_traj_max(S_cal[bad], alive[bad]), 1 - alpha)
        mu = conformal_upper(_traj_max(-S_cal[good], alive[good]), 1 - beta)
        pass_thr[:] = lam; rej_thr[:] = -mu
    elif method in ("naive", "bonf"):
        a = alpha if method == "naive" else alpha / M
        b = beta if method == "naive" else beta / M
        for m in range(M):
            sb = S_cal[bad & alive[:, m], m]; sg = S_cal[good & alive[:, m], m]
            pass_thr[m] = conformal_upper(sb, 1 - a)
            rej_thr[m] = -conformal_upper(-sg, 1 - b)
    elif method == "single":
        m = single_index
        sb = S_cal[bad & alive[:, m], m]; sg = S_cal[good & alive[:, m], m]
        # bad cells that died before k_m can never be passed at m: they count as
        # non-exceedances (score -inf) so the guarantee is over all bad cells
        nb_dead = int((bad & ~alive[:, m]).sum())
        pass_thr[m] = conformal_upper(np.concatenate([sb, np.full(nb_dead, -np.inf)]), 1 - alpha)
        rej_thr[m] = -conformal_upper(-sg, 1 - beta)
    else:
        raise ValueError(method)
    return pass_thr, rej_thr


def fixed_thresholds(M, pass_value, rej_value):
    return np.full(M, float(pass_value)), np.full(M, float(rej_value))


def interval_calibrate(Yhat_cal, sig_cal, logT_cal, alive, alpha, beta):
    """Baseline needing full lifetimes: trajectory-valid conformal lower/upper bounds on
    log10 T. Pass iff lower bound >= log L*, reject iff upper bound < log L*.
    Returns quantiles (q_lo, q_hi) of normalised residuals; bounds are
    yhat - q_lo*sig and yhat + q_hi*sig."""
    r_lo = np.where(alive, (Yhat_cal - logT_cal[:, None]) / sig_cal, -np.inf).max(axis=1)
    r_hi = np.where(alive, (logT_cal[:, None] - Yhat_cal) / sig_cal, -np.inf).max(axis=1)
    return conformal_upper(r_lo, 1 - alpha), conformal_upper(r_hi, 1 - beta)
