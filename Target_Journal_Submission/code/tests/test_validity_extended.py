"""Added after review cycle 1 (R4-04/05): validity of both error rates when cells die before
checkpoints, the real splitter's exchangeability construction, and the L* > last checkpoint
precondition of the configured grids."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from batscreen.screening.calibration import calibrate
from batscreen.screening.procedure import simulate, metrics
from batscreen.evaluation.runner import stratified_split
from batscreen.utils import load_config


def _synthetic_dying(rng, n, ck, Ls=700.0):
    """Lifetimes spread widely so that many bad cells die before late checkpoints; scores of
    dead cells are NaN (as in the pipeline)."""
    M = len(ck)
    logT = rng.normal(np.log10(Ls), 0.30, n)
    T = 10 ** logT
    sc = np.linspace(0.35, 0.10, M)
    S = (logT[:, None] + rng.normal(0, 1, (n, M)) * sc - np.log10(Ls)) / sc
    alive = T[:, None] > np.asarray(ck)[None, :]
    return np.where(alive, S, np.nan), T


def test_both_rates_valid_with_early_deaths():
    rng = np.random.default_rng(1)
    ck = [100, 200, 300, 400, 500, 600]; Ls = 700.0
    fpr, frr, died = [], [], []
    for rep in range(500):
        S, T = _synthetic_dying(rng, 120, ck, Ls)
        Z = (T >= Ls).astype(int)
        cal, te = np.arange(60), np.arange(60, 120)
        pt, rt = calibrate(S[cal], Z[cal], 0.1, 0.1, "traj")
        r = simulate(S[te], T[te], ck, pt, rt, Ls)
        m = metrics(r, T[te], Ls); fpr.append(m["fpr"]); frr.append(m["frr"])
        died.append(np.mean(T < ck[-1]))
    assert np.mean(died) > 0.1  # the scenario really contains early deaths
    assert np.mean(fpr) <= 0.1 + 0.015, np.mean(fpr)
    assert np.mean(frr) <= 0.1 + 0.015, np.mean(frr)


def test_splitter_partitions_and_mixes_cal_test():
    strata = np.array(["a_0"] * 30 + ["a_1"] * 30 + ["b_0"] * 20 + ["b_1"] * 20)
    sp = stratified_split(strata, {"train": 0.5, "cal": 0.25, "test": 0.25}, seed=3)
    allc = np.concatenate([sp["train"], sp["cal"], sp["test"]])
    assert len(allc) == len(strata) == len(np.unique(allc))
    # training set is stratified exactly; calibration/test are drawn uniformly from the remainder
    for s in np.unique(strata):
        assert np.sum(strata[sp["train"]] == s) == round(0.5 * np.sum(strata == s))
    assert abs(len(sp["cal"]) - len(sp["test"])) <= 1


def test_configured_grids_end_before_Lstar():
    cfg = load_config(os.path.join(os.path.dirname(__file__), "..", "config", "default.yaml"))
    for ds, d in cfg["datasets"].items():
        assert max(d["checkpoints"]) < min(d["Lstar_sensitivity"] + [d["Lstar"]]), ds
