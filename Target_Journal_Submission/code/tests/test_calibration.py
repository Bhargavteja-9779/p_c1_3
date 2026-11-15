"""Finite-sample validity checks of the calibration rules on synthetic exchangeable data."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from batscreen.screening.calibration import calibrate, conformal_upper
from batscreen.screening.procedure import simulate, metrics


def _synthetic(rng, n, M=12, Lstar=1.0):
    logT = rng.normal(0, 0.25, n)
    T = 10 ** logT * 700
    noise_scale = np.linspace(0.30, 0.10, M)  # predictions sharpen as cycles accumulate
    S = (logT[:, None] + rng.normal(0, 1, (n, M)) * noise_scale - np.log10(700)) / noise_scale
    return S, T


def test_conformal_upper_rank():
    v = np.arange(1, 20)  # n = 19
    assert conformal_upper(v, 0.9) == 18  # ceil(20*0.9)=18th smallest
    assert conformal_upper(np.arange(5), 0.9) == np.inf  # ceil(6*0.9)=6 > 5


def test_traj_valid_naive_inflated():
    rng = np.random.default_rng(0)
    ck = list(range(20, 140, 10)); Ls = 700.0
    fpr = {"traj": [], "naive": [], "bonf": []}
    for rep in range(400):
        S, T = _synthetic(rng, 120)
        Z = (T >= Ls).astype(int)
        cal, te = np.arange(60), np.arange(60, 120)
        for meth in fpr:
            pt, rt = calibrate(S[cal], Z[cal], 0.1, 0.1, meth)
            r = simulate(S[te], T[te], ck, pt, rt, Ls)
            fpr[meth].append(metrics(r, T[te], Ls)["fpr"])
    m = {k: np.mean(v) for k, v in fpr.items()}
    assert m["traj"] <= 0.1 + 0.015, m
    assert m["bonf"] <= 0.1 + 0.015, m
    assert m["naive"] > m["traj"], m


if __name__ == "__main__":
    test_conformal_upper_rank(); test_traj_valid_naive_inflated(); print("ok")
