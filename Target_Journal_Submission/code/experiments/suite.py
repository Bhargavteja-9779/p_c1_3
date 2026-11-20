"""Experiments E1-E8. Every function writes machine-readable outputs to results/raw/.
Seeds: split seeds are seed_base + offset_e + i, fixed before running."""
from __future__ import annotations
import json, os, sys, time
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from batscreen.evaluation.runner import load_features, run_split, stratified_split
from batscreen.evaluation.parallel import run_many
from batscreen.models.base import MODELS

OFFSETS = dict(E1=0, E2=100000, E3=200000, E4=300000, E5=400000, E6=500000, E7=600000)
DS = {"matr_clo": "severson", "hust": "vq"}


def _feat(cfg, ds, kind=None):
    return load_features(os.path.join(cfg["paths"]["features"], f"{ds}_{kind or DS[ds]}.npz"))


def _seeds(cfg, exp, n):
    return [cfg["seed_base"] + OFFSETS[exp] + i for i in range(n)]


def _exists(cfg, name):
    """Resume support: an experiment output that already exists is not recomputed
    (delete the file, or pass --force to run_all.py, to recompute)."""
    return (not cfg.get("force", False)) and os.path.exists(os.path.join(cfg["paths"]["results"], "raw", name))


def _chunk(cfg, log, name, fn):
    """Checkpointing for long experiments: each (dataset x configuration) chunk is saved
    to results/raw/chunks/<name>.csv as soon as it finishes and is re-used on resume."""
    d = os.path.join(cfg["paths"]["results"], "raw", "chunks"); os.makedirs(d, exist_ok=True)
    p = os.path.join(d, name + ".csv")
    if os.path.exists(p) and not cfg.get("force", False):
        log.info(f"chunk {name}: exists, re-used"); return pd.read_csv(p)
    t = time.time(); df = fn(); df.to_csv(p, index=False); log.info(f"chunk {name}: {len(df)} rows in {time.time()-t:.0f}s")
    return df


def _save(df, cfg, name):
    d = os.path.join(cfg["paths"]["results"], "raw"); os.makedirs(d, exist_ok=True)
    p = os.path.join(d, name); df.to_csv(p, index=False, compression="gzip" if p.endswith(".gz") else None)
    return p


def e1_main(cfg, log):
    out = []
    for ds in DS:
        if _exists(cfg, f"E1_{ds}_splits.csv") and _exists(cfg, f"E1_{ds}_cells.csv.gz") and _exists(cfg, f"E1_{ds}_scores.csv.gz"):
            log.info(f"E1 {ds}: outputs exist, skipped (resume)"); continue
        d = cfg["datasets"][ds]; F = _feat(cfg, ds)
        t = time.time()
        df, cells = run_many(F, d["Lstar"], d["split"], cfg["alpha"], cfg["beta"], "en", _seeds(cfg, "E1", cfg["n_splits"]["en"]),
                             n_jobs=cfg["n_jobs"], keep_cells=True, keep_scores=True, tag=f"E1_{ds}")
        df["dataset"] = ds; cells["dataset"] = ds
        _save(df, cfg, f"E1_{ds}_splits.csv"); _save(cells, cfg, f"E1_{ds}_cells.csv.gz")
        _save(cells.attrs["scores"].assign(dataset=ds), cfg, f"E1_{ds}_scores.csv.gz")
        log.info(f"E1 {ds}: {len(df)} rows in {time.time()-t:.0f}s"); out.append(df)
    return pd.concat(out) if out else None


def e2_models(cfg, log):
    if _exists(cfg, "E2_models_splits.csv"):
        log.info("E2_models_splits.csv: exists, skipped (resume)"); return None
    out = []
    for ds in DS:
        d = cfg["datasets"][ds]; F = _feat(cfg, ds)
        for model in ["logit", "gp", "cnn", "gbr", "rf"]:
            def job(model=model, F=F, d=d, ds=ds):
                df, _ = run_many(F, d["Lstar"], d["split"], cfg["alpha"], cfg["beta"], model,
                                 _seeds(cfg, "E2", cfg["n_splits"][model]), n_jobs=cfg["n_jobs"], tag=f"E2_{ds}_{model}")
                df["dataset"] = ds; return df
            out.append(_chunk(cfg, log, f"E2_{ds}_{model}", job))
    df = pd.concat(out); _save(df, cfg, "E2_models_splits.csv"); return df


def _grids(ck):
    ck = list(ck); idx = lambda ks: [ck.index(k) for k in ks if k in ck]
    if max(ck) <= 300:
        g = {"all16": list(range(len(ck))), "early_20to100": idx(range(20, 101, 10)),
             "sparse_50_100_200_300": idx([50, 100, 200, 300]), "pair_100_300": idx([100, 300]),
             "single_100": idx([100]), "single_50": idx([50]), "single_300": idx([300])}
    else:
        g = {"all17": list(range(len(ck))), "early_20to100": idx(range(20, 101, 10)),
             "sparse_100_300_600_1000": idx([100, 300, 600, 1000]), "pair_100_1000": idx([100, 1000]),
             "single_100": idx([100]), "single_300": idx([300]), "single_1000": idx([1000])}
    return g


def e3_ablation(cfg, log, n=None):
    """Checkpoint-grid ablation; all grids evaluated on the same splits and fitted models."""
    if _exists(cfg, "E3_ablation_grid_splits.csv"):
        log.info("E3_ablation_grid_splits.csv: exists, skipped (resume)"); return None
    out = []
    n = n or cfg.get("n_splits_secondary", max(1, cfg["n_splits"]["en"] // 3))
    for ds in DS:
        d = cfg["datasets"][ds]; F = _feat(cfg, ds)
        variants = [dict(tag=g, grid=g, ck_subset=sub, methods=["proposed", "naive", "traj_unnorm"])
                    for g, sub in _grids(F["checkpoints"]).items()]
        def job(F=F, d=d, ds=ds, variants=variants):
            df, _ = run_many(F, d["Lstar"], d["split"], cfg["alpha"], cfg["beta"], "en", _seeds(cfg, "E3", n),
                             n_jobs=cfg["n_jobs"], variants=variants)
            df["dataset"] = ds; return df
        out.append(_chunk(cfg, log, f"E3_{ds}", job))
    df = pd.concat(out); _save(df, cfg, "E3_ablation_grid_splits.csv"); return df


def e4_robustness(cfg, log, n=None):
    if _exists(cfg, "E4_robustness_splits.csv"):
        log.info("E4_robustness_splits.csv: exists, skipped (resume)"); return None
    out = []
    n = n or cfg.get("n_splits_secondary", max(1, cfg["n_splits"]["en"] // 3))
    meths = ["proposed", "naive", "single_k100", "gauss"]
    for ds in DS:
        d = cfg["datasets"][ds]; F = _feat(cfg, ds); base = d["split"]
        cal_grid = [0.10, 0.15, 0.20, 0.25] if ds == "matr_clo" else [0.20, 0.30, 0.40]
        for cf in cal_grid:
            fr = dict(train=base["train"], cal=cf, test=round(1 - base["train"] - cf, 3))
            def job(fr=fr, F=F, d=d, ds=ds, cf=cf):
                df, _ = run_many(F, d["Lstar"], fr, cfg["alpha"], cfg["beta"], "en", _seeds(cfg, "E4", n), n_jobs=cfg["n_jobs"], methods=meths)
                df["dataset"] = ds; df["factor"] = "cal_fraction"; df["level"] = cf; return df
            out.append(_chunk(cfg, log, f"E4_{ds}_cal_{cf}", job))
        tr_grid = [0.2, 0.3, 0.4, 0.5] if ds == "matr_clo" else [0.2, 0.3, 0.4]
        for tf in tr_grid:
            fr = dict(train=tf, cal=base["cal"], test=round(1 - tf - base["cal"], 3))
            def job(fr=fr, F=F, d=d, ds=ds, tf=tf):
                df, _ = run_many(F, d["Lstar"], fr, cfg["alpha"], cfg["beta"], "en", _seeds(cfg, "E4", n), n_jobs=cfg["n_jobs"], methods=meths)
                df["dataset"] = ds; df["factor"] = "train_fraction"; df["level"] = tf; return df
            out.append(_chunk(cfg, log, f"E4_{ds}_train_{tf}", job))
        variants = [dict(tag=f"noise_{w}_{lv}", factor=f"noise_{w}", level=lv, noise=lv, noise_on=w, methods=meths)
                    for w in ["both", "test"] for lv in [0.1, 0.25, 0.5, 1.0]]
        def job(F=F, d=d, ds=ds, variants=variants, base=base):
            df, _ = run_many(F, d["Lstar"], base, cfg["alpha"], cfg["beta"], "en", _seeds(cfg, "E4", n), n_jobs=cfg["n_jobs"],
                             variants=variants)
            df["dataset"] = ds; return df
        out.append(_chunk(cfg, log, f"E4_{ds}_noise", job))
        log.info(f"E4 {ds} done")
    df = pd.concat(out); _save(df, cfg, "E4_robustness_splits.csv"); return df


def _batch_split_fn(F, Lstar, source, target, scenario, n_t, train_frac=0.6):
    b = F["batch"]; T = F["lifetime"]; Z = (T >= Lstar).astype(int)
    src = np.where(np.isin(b, source))[0]; tgt = np.where(np.isin(b, target))[0]

    def fn(seed):
        rng = np.random.default_rng(seed)
        s = rng.permutation(src); ntr = int(round(train_frac * len(s)))
        tr, src_cal = np.sort(s[:ntr]), np.sort(s[ntr:])
        if scenario == "source_cal":
            return dict(train=tr, cal=src_cal, test=np.sort(tgt))
        # target recalibration: n_t target cells (stratified by class) cycled only to L*
        t_good, t_bad = rng.permutation(tgt[Z[tgt] == 1]), rng.permutation(tgt[Z[tgt] == 0])
        frac = len(t_good) / len(tgt); ng = int(round(n_t * frac)); nb = n_t - ng
        cal = np.sort(np.r_[t_good[:ng], t_bad[:nb]])
        return dict(train=tr, cal=cal, test=np.sort(np.setdiff1d(tgt, cal)))
    return fn


def _combined_capacity(cfg):
    A, B = _feat(cfg, "matr_clo", "capacity"), _feat(cfg, "hust", "capacity")
    common = [k for k in A["checkpoints"] if k in set(B["checkpoints"])]
    ia = [list(A["checkpoints"]).index(k) for k in common]; ib = [list(B["checkpoints"]).index(k) for k in common]
    F = {"X": np.concatenate([A["X"][:, ia], B["X"][:, ib]]), "checkpoints": np.array(common),
         "lifetime": np.r_[A["lifetime"], B["lifetime"]], "dataset": np.r_[A["dataset"], B["dataset"]],
         "batch": np.r_[A["batch"], B["batch"]], "cell_id": np.r_[A["cell_id"], B["cell_id"]], "names": A["names"]}
    return F, len(A["lifetime"])


def e5_shift(cfg, log, n=None):
    if _exists(cfg, "E5_shift_splits.csv"):
        log.info("E5_shift_splits.csv: exists, skipped (resume)"); return None
    out = []
    n = n or cfg.get("n_splits_secondary", max(1, cfg["n_splits"]["en"] // 3))
    meths = ["proposed", "naive", "single_k100", "gauss", "point_k100"]
    d = cfg["datasets"]["matr_clo"]; F = _feat(cfg, "matr_clo")
    for target in [["b3"], ["b4"]]:
        for scen, nt in [("source_cal", 0), ("target_cal", 20), ("target_cal", 30)]:
            fn = _batch_split_fn(F, d["Lstar"], ["b1", "b2"], target, scen, nt)
            def job(fn=fn, target=target, scen=scen, nt=nt):
                df, _ = run_many(F, d["Lstar"], None, cfg["alpha"], cfg["beta"], "en", _seeds(cfg, "E5", n), n_jobs=cfg["n_jobs"],
                                 methods=meths, split_fn=fn)
                df["experiment"] = "batch_shift"; df["target"] = "+".join(target); df["scenario"] = scen; df["n_target_cal"] = nt
                return df
            out.append(_chunk(cfg, log, f"E5_batch_{'+'.join(target)}_{scen}_{nt}", job))
    # cross-laboratory: capacity-trajectory features only (protocol-agnostic)
    F2, n_src = _combined_capacity(cfg); Ls = cfg["datasets"]["hust"]["Lstar"]; T2 = F2["lifetime"]; Z2 = (T2 >= Ls).astype(int)
    src = np.arange(n_src); tgt = np.arange(n_src, len(T2))
    for scen in ["source_model_target_cal", "target_model_target_cal"]:
        def fn(seed, scen=scen):
            rng = np.random.default_rng(seed)
            g, b = rng.permutation(tgt[Z2[tgt] == 1]), rng.permutation(tgt[Z2[tgt] == 0])
            parts = {}
            for name, arr in (("g", g), ("b", b)):
                k = len(arr); n_tr = int(round(0.4 * k)); n_ca = int(round(0.3 * k))
                parts[name] = (arr[:n_tr], arr[n_tr:n_tr + n_ca], arr[n_tr + n_ca:])
            tr_t = np.r_[parts["g"][0], parts["b"][0]]; ca = np.r_[parts["g"][1], parts["b"][1]]; te = np.r_[parts["g"][2], parts["b"][2]]
            tr = src if scen.startswith("source") else tr_t
            return dict(train=np.sort(tr), cal=np.sort(ca), test=np.sort(te))
        def job(fn=fn, scen=scen):
            df, _ = run_many(F2, Ls, None, cfg["alpha"], cfg["beta"], "en", _seeds(cfg, "E5", n), n_jobs=cfg["n_jobs"],
                             methods=meths, split_fn=fn)
            df["experiment"] = "cross_lab"; df["target"] = "HUST"; df["scenario"] = scen; df["n_target_cal"] = -1
            return df
        out.append(_chunk(cfg, log, f"E5_xlab_{scen}", job))
    df = pd.concat(out); _save(df, cfg, "E5_shift_splits.csv"); return df


_MEM_SNIPPET = """
import sys, resource, json
sys.path.insert(0, 'src')
from batscreen.evaluation.runner import load_features, run_split
F = load_features(sys.argv[1]); base = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
run_split(F, float(sys.argv[2]), json.loads(sys.argv[3]), 0.1, 0.1, sys.argv[4], 1, methods=['proposed'])
print(json.dumps(dict(peak_mb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, base_mb=base / 1024)))
"""


def e6_compute(cfg, log, reps=5):
    """Wall-clock per split (all checkpoints: fit + score + calibrate + decide), single
    process; peak resident memory of a fresh process running one split; cost of the
    calibration/decision step alone for growing calibration sets."""
    if _exists(cfg, "E6_compute.csv"):
        log.info("E6_compute.csv: exists, skipped (resume)"); return None
    import subprocess
    rows = []
    for ds in DS:
        d = cfg["datasets"][ds]; F = _feat(cfg, ds)
        fpath = os.path.join(cfg["paths"]["features"], f"{ds}_{DS[ds]}.npz")
        for model in ["en", "logit", "gbr", "rf", "gp", "cnn"]:
            out = subprocess.run([sys.executable, "-c", _MEM_SNIPPET, fpath, str(d["Lstar"]), json.dumps(d["split"]), model],
                                 capture_output=True, text=True, check=True).stdout.strip().splitlines()[-1]
            mem = json.loads(out)
            for r in range(reps):
                seed = cfg["seed_base"] + OFFSETS["E6"] + r
                t0 = time.perf_counter()
                run_split(F, d["Lstar"], d["split"], cfg["alpha"], cfg["beta"], model, seed, methods=["proposed"])
                rows.append(dict(dataset=ds, model=model, rep=r, split_seconds=time.perf_counter() - t0,
                                 peak_rss_mb=mem["peak_mb"], n_checkpoints=len(F["checkpoints"])))
        from batscreen.screening.calibration import calibrate
        from batscreen.screening.procedure import simulate
        rng = np.random.default_rng(0); M = len(F["checkpoints"])
        for n_cal in [40, 400, 4000]:
            S = rng.normal(size=(n_cal, M)); Z = rng.integers(0, 2, n_cal); T = rng.uniform(100, 2000, 1000)
            t0 = time.perf_counter(); pt, rt = calibrate(S, Z, 0.1, 0.1, "traj"); t1 = time.perf_counter()
            simulate(rng.normal(size=(1000, M)), T, F["checkpoints"], pt, rt, d["Lstar"]); t2 = time.perf_counter()
            rows.append(dict(dataset=ds, model=f"calibration_only_n{n_cal}", rep=0, split_seconds=t1 - t0,
                             decide_seconds_per_1000_cells=t2 - t1, n_checkpoints=M))
        log.info(f"E6 {ds} done")
    df = pd.DataFrame(rows); _save(df, cfg, "E6_compute.csv"); return df


def e7_sensitivity(cfg, log, n=None):
    if _exists(cfg, "E7_sensitivity_splits.csv"):
        log.info("E7_sensitivity_splits.csv: exists, skipped (resume)"); return None
    out = []
    n = n or cfg.get("n_splits_secondary", max(1, cfg["n_splits"]["en"] // 3))
    meths = ["proposed", "naive", "single_k100", "gauss"]
    for ds in DS:
        d = cfg["datasets"][ds]; F = _feat(cfg, ds)
        variants = [dict(tag=f"ab_{a}_{b}", alpha=a, beta=b, methods=meths) for a, b in [(0.05, 0.05), (0.1, 0.1), (0.2, 0.2), (0.05, 0.2)]]
        def job_ab(F=F, d=d, ds=ds, variants=variants):
            df, _ = run_many(F, d["Lstar"], d["split"], cfg["alpha"], cfg["beta"], "en", _seeds(cfg, "E7", n), n_jobs=cfg["n_jobs"],
                             variants=variants)
            df["dataset"] = ds; df["factor"] = "alpha_beta"; df["Lstar"] = d["Lstar"]; return df
        out.append(_chunk(cfg, log, f"E7_{ds}_ab", job_ab))
        for Ls in d["Lstar_sensitivity"]:
            def job_L(F=F, d=d, ds=ds, Ls=Ls):
                df, _ = run_many(F, Ls, d["split"], cfg["alpha"], cfg["beta"], "en", _seeds(cfg, "E7", n), n_jobs=cfg["n_jobs"], methods=meths)
                df["dataset"] = ds; df["factor"] = "Lstar"; df["alpha"] = cfg["alpha"]; df["beta"] = cfg["beta"]; df["Lstar"] = Ls; return df
            out.append(_chunk(cfg, log, f"E7_{ds}_L{Ls}", job_L))
        log.info(f"E7 {ds} done")
    df = pd.concat(out); _save(df, cfg, "E7_sensitivity_splits.csv"); return df


# ---------------------------------------------------------------------------
# Additional analyses added after the design freeze (anticipating reviewer questions);
# reported as such in the manuscript.
OFFSETS.update(E9=700000, E10=800000)


def e9_protocol_grouped(cfg, log, n=None):
    """MATR+CLO with charging protocols disjoint between training, calibration and test:
    whole protocol groups are assigned (50% of groups to training; remaining groups split
    at random between calibration and test). HUST needs no such experiment because every
    HUST cell has its own discharge protocol."""
    if _exists(cfg, "E9_protocol_grouped_splits.csv"):
        log.info("E9 exists, skipped (resume)"); return None
    n = n or cfg.get("n_splits_secondary", 200)
    d = cfg["datasets"]["matr_clo"]; F = _feat(cfg, "matr_clo")
    groups = np.array([f"{ds}:{p}" for ds, p in zip(F["dataset"], F["policy"])])
    ug = np.unique(groups)

    def fn(seed):
        rng = np.random.default_rng(seed)
        g = rng.permutation(ug); ntr = int(round(0.5 * len(g)))
        g_tr, rest = g[:ntr], g[ntr:]
        to_cal = rng.random(len(rest)) < 0.5
        idx = lambda gs: np.sort(np.where(np.isin(groups, gs))[0])
        return dict(train=idx(g_tr), cal=idx(rest[to_cal]), test=idx(rest[~to_cal]))
    def job():
        df, _ = run_many(F, d["Lstar"], None, cfg["alpha"], cfg["beta"], "en", _seeds(cfg, "E9", n), n_jobs=cfg["n_jobs"],
                         methods=["proposed", "naive", "single_k100", "gauss", "point_k100"], split_fn=fn)
        df["dataset"] = "matr_clo"; df["n_groups"] = len(ug); return df
    df = _chunk(cfg, log, "E9_matr_clo", job)
    _save(df, cfg, "E9_protocol_grouped_splits.csv"); log.info(f"E9 done ({len(ug)} protocol groups)"); return df


def e10_pac(cfg, log, n=None):
    """Training-conditional (PAC) variant: rank chosen so that P(conditional error > alpha)
    <= 0.1 under the Beta law of conformal coverage; default and enlarged calibration sets."""
    if _exists(cfg, "E10_pac_splits.csv"):
        log.info("E10 exists, skipped (resume)"); return None
    n = n or cfg.get("n_splits_secondary", 200)
    out = []
    big = {"matr_clo": dict(train=0.35, cal=0.45, test=0.20), "hust": dict(train=0.3, cal=0.5, test=0.2)}
    for ds in DS:
        d = cfg["datasets"][ds]; F = _feat(cfg, ds)
        for tag, fr in (("default", d["split"]), ("large_cal", big[ds])):
            def job(F=F, d=d, ds=ds, tag=tag, fr=fr):
                df, _ = run_many(F, d["Lstar"], fr, cfg["alpha"], cfg["beta"], "en", _seeds(cfg, "E10", n), n_jobs=cfg["n_jobs"],
                                 methods=["proposed", "traj_pac", "single_k100"])
                df["dataset"] = ds; df["cal_design"] = tag; return df
            out.append(_chunk(cfg, log, f"E10_{ds}_{tag}", job))
        log.info(f"E10 {ds} done")
    df = pd.concat(out); _save(df, cfg, "E10_pac_splits.csv"); return df


def e11_interpretation(cfg, log, n=None):
    """Descriptive physical interpretation (added 2026-11-20, after the main results; it
    makes no claim about screening performance). For each checkpoint, (a) Spearman
    correlation of every feature with log10 cycle life over all cells alive at the
    checkpoint, and (b) standardised elastic-net coefficients over the training sets of
    the first n E1 splits (same seeds as E1), i.e. which signals the screening scores use
    at early and late checkpoints."""
    from scipy.stats import spearmanr
    if _exists(cfg, "E11_coefficients.csv") and _exists(cfg, "E11_correlations.csv"):
        log.info("E11 exists, skipped (resume)"); return None
    n = n or cfg.get("n_splits_secondary", 200)
    coefs, cors = [], []
    for ds in DS:
        d = cfg["datasets"][ds]; F = _feat(cfg, ds); T = F["lifetime"].astype(float)
        names = [str(x) for x in F["names"]]
        for m, k in enumerate(F["checkpoints"]):
            alive = T > k
            for j, nm in enumerate(names):
                x = F["X"][alive, m, j]; ok = np.isfinite(x)
                r = spearmanr(x[ok], np.log10(T[alive][ok])).statistic if ok.sum() > 5 else np.nan
                cors.append(dict(dataset=ds, checkpoint=int(k), feature=nm, spearman=r, n_cells=int(ok.sum())))
        strata = np.array([f"{a}_{int(t >= d['Lstar'])}" for a, t in zip(F["dataset"], T)])
        def job(F=F, d=d, ds=ds, T=T, names=names, strata=strata):
            from joblib import Parallel, delayed
            def one(seed):
                tr = stratified_split(strata, d["split"], seed)["train"]; rows = []
                for m, k in enumerate(F["checkpoints"]):
                    a = tr[T[tr] > k]
                    if len(a) < 10: continue
                    mdl = MODELS["en"](seed=seed + 7919 * m).fit(F["X"][a, m, :], np.log10(T[a]))
                    c = mdl.pipe[-1].coef_
                    rows += [dict(dataset=ds, seed=seed, checkpoint=int(k), feature=nm, coef=float(c[j])) for j, nm in enumerate(names)]
                return rows
            res = Parallel(n_jobs=cfg["n_jobs"])(delayed(one)(s) for s in _seeds(cfg, "E1", n))
            return pd.DataFrame([r for rr in res for r in rr])
        coefs.append(_chunk(cfg, log, f"E11_{ds}", job))
    _save(pd.DataFrame(cors), cfg, "E11_correlations.csv"); _save(pd.concat(coefs), cfg, "E11_coefficients.csv")
    log.info("E11 done")
