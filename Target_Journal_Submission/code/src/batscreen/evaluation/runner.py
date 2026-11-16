"""Split-level experiment engine: fit per-checkpoint models on training cells, score
calibration/test cells, calibrate each screening method, simulate decisions."""
from __future__ import annotations
import math
import numpy as np
from scipy.stats import norm
from ..models.base import MODELS
from ..screening.calibration import calibrate, interval_calibrate
from ..screening.procedure import simulate, metrics


def load_features(path):
    z = np.load(path, allow_pickle=False)
    return {k: z[k] for k in z.files}


def stratified_split(strata, fractions, seed):
    """Training cells are drawn within strata (dataset x class) so every model sees all
    groups; calibration and test cells are then drawn uniformly at random from the
    remaining pool. This keeps calibration and test cells exactly exchangeable (within
    each class), which the finite-sample guarantee requires; stratifying them separately
    with rounding would give different group mixtures in the two sets."""
    rng = np.random.default_rng(seed)
    tr, pool = [], []
    for s in np.unique(strata):
        ii = rng.permutation(np.where(strata == s)[0])
        n_tr = int(round(fractions["train"] * len(ii)))
        tr += list(ii[:n_tr]); pool += list(ii[n_tr:])
    pool = rng.permutation(np.array(pool, int))
    n_ca = int(round(fractions["cal"] / (fractions["cal"] + fractions["test"]) * len(pool)))
    return {"train": np.array(sorted(tr), int), "cal": np.sort(pool[:n_ca]), "test": np.sort(pool[n_ca:])}


def _design(F, m, model, feature_mask):
    X = F["X"][:, m, :] if feature_mask is None else F["X"][:, m, feature_mask]
    if model == "cnn":
        X = np.concatenate([F["C"][:, m, :], X], axis=1)
    return X


def fit_models(F, T, Lstar, tr, model, seed, feature_mask=None):
    """Fit one model per checkpoint on training cells alive at that checkpoint."""
    fitted = {}
    for m, k in enumerate(F["checkpoints"]):
        X = _design(F, m, model, feature_mask)
        a_tr = tr[T[tr] > k]
        if len(a_tr) < 10:
            continue
        mdl = MODELS[model](seed=seed + 7919 * m)
        if mdl.kind == "classifier":
            z = (T[a_tr] >= Lstar).astype(int)
            if z.min() == z.max():
                continue
            mdl.fit(X[a_tr], z)
        else:
            mdl.fit(X[a_tr], np.log10(T[a_tr]))
        fitted[m] = (mdl, np.nanstd(X[a_tr], axis=0))
    return fitted


def predict_models(F, T, fitted, ev, model, seed, feature_mask=None, noise=None, noise_rows=None):
    """yhat, scale [len(ev), M] (NaN where dead). noise = SD multiple of training-feature SD
    added at prediction time to rows `noise_rows` (boolean over ev; default all)."""
    M = len(F["checkpoints"])
    yhat = np.full((len(ev), M), np.nan); scale = np.full((len(ev), M), np.nan)
    rng = np.random.default_rng(seed + 104729)
    for m, k in enumerate(F["checkpoints"]):
        ev_alive = T[ev] > k
        if m not in fitted or ev_alive.sum() == 0:
            continue
        mdl, sd = fitted[m]
        Xe = _design(F, m, model, feature_mask)[ev[ev_alive]].copy()
        if noise:
            rows = np.ones(len(Xe), bool) if noise_rows is None else noise_rows[ev_alive]
            Xe[rows] += rng.normal(0, 1, Xe[rows].shape) * sd * noise
        y, sc = mdl.predict(Xe)
        yhat[ev_alive, m] = y; scale[ev_alive, m] = sc
    return yhat, scale


def fit_predict(F, T, Lstar, tr, ev, model, seed, feature_mask=None, noise=None, noise_rows=None):
    fitted = fit_models(F, T, Lstar, tr, model, seed, feature_mask)
    return predict_models(F, T, fitted, ev, model, seed, feature_mask, noise, noise_rows)


def method_specs(model_kind, m_ref, alpha, beta):
    """Which score matrix and which calibration each method uses."""
    za, zb = norm.ppf(1 - alpha), norm.ppf(1 - beta)
    if model_kind == "classifier":
        return {"proposed": ("raw", "traj"), "naive": ("raw", "naive"), "single_k100": ("raw", "single")}
    return {
        "proposed": ("norm", "traj"),
        "traj_unnorm": ("raw", "traj"),
        "naive": ("norm", "naive"),
        "bonf": ("norm", "bonf"),
        "single_k100": ("norm", "single"),
        "point_k100": ("raw", ("fixed_at", m_ref, 0.0, 0.0)),
        "gauss": ("norm", ("fixed", za, -zb)),
        "interval_traj": ("norm", "interval"),
    }


def run_split(F, Lstar, fractions, alpha, beta, model, split_seed, strata_key="dataset",
              keep_cells=False, feature_mask=None, methods=None, split_fn=None, ck_subset=None,
              noise=None, noise_on="both", tag=None, keep_scores=False, variants=None):
    """variants: optional list of dicts {tag, alpha, beta, ck_subset, methods, noise, noise_on}
    evaluated on the SAME split and the SAME fitted models (only calibration/decision or the
    prediction-time noise changes)."""
    T = F["lifetime"].astype(float); ck_all = F["checkpoints"]
    Z = (T >= Lstar).astype(int)
    if split_fn is None:
        strata = np.array([f"{a}_{b}" for a, b in zip(F[strata_key], Z)])
        sp = stratified_split(strata, fractions, split_seed)
    else:
        sp = split_fn(split_seed)
    tr, ca, te = sp["train"], sp["cal"], sp["test"]
    ev = np.concatenate([ca, te]); nC = len(ca)
    fitted = fit_models(F, T, Lstar, tr, model, split_seed, feature_mask)
    if variants is None:
        variants = [dict(tag=tag, alpha=alpha, beta=beta, ck_subset=ck_subset, methods=methods, noise=noise, noise_on=noise_on)]
    rows_all, cells_all, cache = [], [], {}
    for vi, v in enumerate(variants):
        nz, non = v.get("noise"), v.get("noise_on", "both")
        key = (nz, non)
        if key not in cache:
            noise_rows = np.r_[np.zeros(nC, bool), np.ones(len(te), bool)] if (nz and non == "test") else None
            cache[key] = predict_models(F, T, fitted, ev, model, split_seed, feature_mask, nz, noise_rows)
        yhat, scale = cache[key]
        r, c = _evaluate(F, T, Z, Lstar, tr, ca, te, nC, yhat, scale, model, split_seed, v.get("alpha", alpha), v.get("beta", beta),
                         v.get("ck_subset"), v.get("methods"), v.get("tag"), keep_cells, keep_scores and vi == 0)
        for row in r:
            row.update({k: (str(val) if k == "ck_subset" else val) for k, val in v.items() if k not in ("methods",)})
        rows_all += r; cells_all += c
    return rows_all, cells_all


def _evaluate(F, T, Z, Lstar, tr, ca, te, nC, yhat, scale, model, split_seed, alpha, beta, ck_subset, methods, tag,
              keep_cells, keep_scores):
    ck_all = F["checkpoints"]
    cols = np.arange(len(ck_all)) if ck_subset is None else np.array(ck_subset)
    yhat, scale, ck = yhat[:, cols], scale[:, cols], ck_all[cols]
    M = len(ck)
    kind = MODELS[model].kind
    raw = yhat - (0 if kind == "classifier" else math.log10(Lstar))
    S = {"raw": raw, "norm": raw / scale}
    m_ref = int(np.argmin(np.abs(ck - 100)))
    specs = method_specs(kind, m_ref, alpha, beta)
    if methods is not None and "traj_pac" in methods and kind != "classifier":  # opt-in only
        specs["traj_pac"] = ("norm", "traj_pac")
    if methods is not None:
        specs = {k: v for k, v in specs.items() if k in methods}
    rows, cell_rows = [], []
    if keep_scores:  # normalised scores of test cells at every checkpoint (method independent)
        for i, c in enumerate(te):
            for m in range(M):
                if np.isfinite(S["norm"][nC + i, m]):
                    cell_rows.append((split_seed, model, "__score__", int(c), m, float(S["norm"][nC + i, m]),
                                      float(yhat[nC + i, m]), float(scale[nC + i, m])))
    for name, (skey, cal) in specs.items():
        Sc, St = S[skey][:nC], S[skey][nC:]
        if cal in ("traj", "naive", "bonf", "traj_pac"):
            pt, rt = calibrate(Sc, Z[ca], alpha, beta, cal)
        elif cal == "single":
            pt, rt = calibrate(Sc, Z[ca], alpha, beta, "single", single_index=m_ref)
        elif cal == "interval":
            qlo, qhi = interval_calibrate(yhat[:nC], scale[:nC], np.log10(T[ca]), np.isfinite(yhat[:nC]), alpha, beta)
            pt, rt = np.full(M, qlo), np.full(M, -qhi)
        elif cal[0] == "fixed":
            pt, rt = np.full(M, cal[1]), np.full(M, cal[2])
        elif cal[0] == "fixed_at":
            pt, rt = np.full(M, np.inf), np.full(M, -np.inf)
            pt[cal[1]], rt[cal[1]] = cal[2], cal[3]
        res = simulate(St, T[te], ck, pt, rt, Lstar)
        met = metrics(res, T[te], Lstar)
        need_full = name == "interval_traj"
        cal_cycles = T[ca] if need_full else np.minimum(T[ca], Lstar)
        trc = np.minimum(T[tr], Lstar) if kind == "classifier" else T[tr]
        met.update(model=model, method=name, split=split_seed, tag=tag, n_cal=nC, n_test=len(te),
                   n_cal_bad=int((Z[ca] == 0).sum()), n_cal_good=int((Z[ca] == 1).sum()),
                   pass_thr=float(np.nanmin(pt)) if np.isfinite(pt).any() else np.inf,
                   rej_thr=float(np.nanmax(rt)) if np.isfinite(rt).any() else -np.inf,
                   cal_cell_cycles=float(cal_cycles.sum()), cal_wallclock=float(cal_cycles.max()) if nC else 0.0,
                   train_cell_cycles=float(trc.sum()), train_wallclock=float(trc.max()))
        rows.append(met)
        if keep_cells:
            for i, c in enumerate(te):
                cell_rows.append((split_seed, model, name, int(c), int(res["decision"][i]), bool(res["by_model"][i]),
                                  float(res["time"][i]), int(res["m_idx"][i])))
    return rows, cell_rows
