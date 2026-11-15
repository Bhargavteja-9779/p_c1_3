"""Checkpoint features computed only from cycles <= checkpoint k (no look-ahead).

MATR/CLO ("severson" set, generalising the 'full model' of Severson et al. 2019 from
cycle 100 to an arbitrary checkpoint k):
  dq_min, dq_var, dq_skew, dq_kurt : log10|.| of min/variance/skewness/kurtosis of
                                      dQ_k-10(V) = Q_k(V) - Q_10(V), where Q_k(V) is the
                                      element-wise median over cycles k-4..k and Q_10(V)
                                      the median over cycles 8..12 (glitch-robust)
  q2, qmax_minus_q2               : discharge capacity at cycle 2 and max(Q_d[2..k]) - Q_d[2]
  fade_slope, fade_intercept      : linear fit of Q_d over cycles 2..k
  fade_slope_late                 : linear fit of Q_d over the last 10 cycles up to k
  chargetime5                     : mean charge time of cycles 2..6
  tmax_mean                       : mean of per-cycle max temperature, cycles 2..k
  (IR features of Severson et al. are NOT used: the CLO batch has no IR records.)
HUST ("vq" set): the same capacity-trajectory features plus statistics of
  dV_k-10(q) = V_k(q) - V_10(q) on a discharged-capacity grid (HUST uses multi-stage
  discharge so Q(V) is not single-valued; V(q) is).
"capacity" set: capacity-trajectory features only (protocol-agnostic; used cross-lab).
"""
from __future__ import annotations
import numpy as np
from scipy import stats

EPS = 1e-8
CAP_FEATS = ["q2", "qmax_minus_q2", "fade_slope", "fade_intercept", "fade_slope_late", "dq_k_10"]


def _nearest_valid(arr, idx, max_shift=3):
    for s in [0, -1, 1, -2, 2, -3, 3][: 2 * max_shift + 1]:
        j = idx + s
        if 0 <= j < arr.shape[0] and np.all(np.isfinite(arr[j])):
            return arr[j]
    return None


def _clean_qd(q):
    q = np.asarray(q, dtype=float).copy()
    bad = ~np.isfinite(q) | (q < 0.5) | (q > 1.3)
    if bad.any():  # replace glitches (zeros / spikes) by linear interpolation
        good = np.where(~bad)[0]
        q[bad] = np.interp(np.where(bad)[0], good, q[good])
    return q


def capacity_features(qd, k):
    q = _clean_qd(qd[:k])  # cycles 1..k (index 0 = cycle 1)
    c = np.arange(1, k + 1)
    seg = slice(1, k)  # cycles 2..k
    slope, intercept = np.polyfit(c[seg], q[seg], 1)
    late = slice(max(1, k - 10), k)
    slope_late = np.polyfit(c[late], q[late], 1)[0]
    return dict(q2=q[1], qmax_minus_q2=np.max(q[seg]) - q[1], fade_slope=slope,
                fade_intercept=intercept, fade_slope_late=slope_late, dq_k_10=q[k - 1] - q[9])


def _curve_stats(d, prefix):
    return {f"{prefix}_min": np.log10(np.abs(np.min(d)) + EPS),
            f"{prefix}_var": np.log10(np.var(d) + EPS),
            f"{prefix}_skew": np.log10(np.abs(stats.skew(d)) + EPS),
            f"{prefix}_kurt": np.log10(np.abs(stats.kurtosis(d)) + EPS)}


def _window_median(arr, lo, hi):
    """Element-wise median of valid curves for cycles lo..hi (1-based, inclusive).
    Some cycles are non-standard (rest/diagnostic steps) and give single-cycle glitches
    in Q(V); the 5-cycle median removes them without using any cycle > hi."""
    rows = [arr[j - 1] for j in range(lo, hi + 1) if 1 <= j <= arr.shape[0] and np.all(np.isfinite(arr[j - 1]))]
    return np.median(np.stack(rows), axis=0) if len(rows) >= 3 else None


def matr_features(cell, k, window=5):
    qdlin = cell["qdlin"]
    if window > 1:
        a, b = _window_median(qdlin, k - window + 1, k), _window_median(qdlin, 8, 12)
    else:
        a, b = _nearest_valid(qdlin, k - 1), _nearest_valid(qdlin, 9)
    if a is None or b is None:
        return None
    f = _curve_stats(a - b, "dq")
    f.update(capacity_features(cell["summary_QDischarge"], k))
    s = cell
    ct = np.asarray(s["summary_chargetime"][1:6], dtype=float)
    f["chargetime5"] = float(np.nanmean(np.where((ct > 0) & (ct < 100), ct, np.nan)))
    tm = np.asarray(s["summary_Tmax"][1:k], dtype=float)
    f["tmax_mean"] = float(np.nanmean(np.where((tm > 20) & (tm < 60), tm, np.nan)))
    return f


def hust_features(cell, k):
    cyc = list(cell["vq_cycles"])
    if k not in cyc or 10 not in cyc:
        return None
    a, b = cell["vq"][cyc.index(k)], cell["vq"][cyc.index(10)]
    if not (np.all(np.isfinite(a)) and np.all(np.isfinite(b))):
        a = _nearest_valid(cell["vq"], cyc.index(k), 1); b = _nearest_valid(cell["vq"], cyc.index(10), 1)
        if a is None or b is None:
            return None
    f = _curve_stats(a - b, "dv")
    f["dv_mean"] = float(np.mean(a - b))
    f.update(capacity_features(cell["summary_QDischarge"], k))
    return f


def difference_curve(cell, k, kind, n_points=100):
    """Down-sampled dQ_k-10(V) (MATR, window medians) or dV_k-10(q) (HUST) for the CNN."""
    if kind == "severson":
        a, b = _window_median(cell["qdlin"], k - 4, k), _window_median(cell["qdlin"], 8, 12)
    elif kind == "vq":
        cyc = list(cell["vq_cycles"])
        if k not in cyc:
            return None
        a, b = cell["vq"][cyc.index(k)], cell["vq"][cyc.index(10)]
    else:
        return None
    if a is None or b is None or not (np.all(np.isfinite(a)) and np.all(np.isfinite(b))):
        return None
    d = a - b
    idx = np.linspace(0, d.size - 1, n_points).round().astype(int)
    return d[idx].astype(np.float32)


def build_curve_table(cells, checkpoints, kind, n_points=100):
    C = np.full((len(cells), len(checkpoints), n_points), np.nan, dtype=np.float32)
    for i, c in enumerate(cells):
        for m, k in enumerate(checkpoints):
            if c["lifetime"] > k:
                d = difference_curve(c, k, kind, n_points)
                if d is not None:
                    C[i, m] = d
    return C


def build_feature_table(cells, checkpoints, kind):
    """Return dict k -> (feature matrix [n_cells x p] with NaN rows for dead/missing, names)."""
    out = {}
    for k in checkpoints:
        rows, names = [], None
        for c in cells:
            if c["lifetime"] <= k:  # cell already reached end of life: no prediction needed
                rows.append(None); continue
            if kind == "severson":
                f = matr_features(c, k)
            elif kind == "vq":
                f = hust_features(c, k)
            elif kind == "capacity":
                f = capacity_features(c["summary_QDischarge"], k)
            else:
                raise ValueError(kind)
            if f is not None and names is None:
                names = list(f.keys())
            rows.append(f)
        X = np.full((len(cells), len(names)), np.nan)
        for i, f in enumerate(rows):
            if f is not None:
                X[i] = [f[n] for n in names]
        out[k] = (X, names)
    return out
