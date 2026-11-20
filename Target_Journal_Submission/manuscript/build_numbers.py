"""Build results/manuscript_numbers.json: every number quoted in the manuscript, computed
from the machine-generated result files (results/raw/*.csv, results/statistics.json,
results/run_config.json, data/features/*.npz). The manuscript sources reference these
values only through {{KEY}} tokens; render.py refuses to build if a token is missing.
Usage: python manuscript/build_numbers.py [--root Target_Journal_Submission]"""
from __future__ import annotations
import argparse, json, math, os, sys
import numpy as np
import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "code", "src"))
from batscreen.evaluation.runner import load_features  # noqa: E402

N = {}


def put(key, value, fmt):
    if value is None or (isinstance(value, float) and not np.isfinite(value)):
        N[key] = "n/a"; return
    if fmt == "pct1":
        N[key] = f"{100 * value:.1f}"
    elif fmt == "pct0":
        N[key] = f"{100 * value:.0f}"
    elif fmt == "int":
        N[key] = f"{int(round(value)):,}"
    elif fmt == "p":
        N[key] = ("< 10^-300^" if value == 0 else (f"{value:.2g}" if value >= 1e-3 else
                  "{:.1f} × 10^{}^".format(value / 10 ** math.floor(math.log10(value)), int(math.floor(math.log10(value))))))
    else:
        N[key] = format(value, fmt)


def split_stats(prefix, g, alpha=0.1, beta=0.1):
    n = len(g)
    for e in ("fpr", "frr"):
        m, s = g[e].mean(), g[e].std(ddof=1) if n > 1 else 0.0
        put(f"{prefix}.{e}", m, ".3f"); put(f"{prefix}.{e}_lo", m - 1.96 * s / np.sqrt(n), ".3f")
        put(f"{prefix}.{e}_hi", m + 1.96 * s / np.sqrt(n), ".3f")
        put(f"{prefix}.{e}_above", float((g[e] > (alpha if e == "fpr" else beta) + 1e-12).mean()), "pct0")
    put(f"{prefix}.acc", g["accuracy"].mean(), ".3f"); put(f"{prefix}.early", g["early_rate"].mean(), "pct1")
    put(f"{prefix}.sav", g["time_saving"].mean(), "pct1"); put(f"{prefix}.sav_sd", g["time_saving"].std(ddof=1), "pct1")
    put(f"{prefix}.time", g["mean_time"].mean(), "int"); put(f"{prefix}.nsplits", n, "int")
    if "n_cal_bad" in g:
        put(f"{prefix}.ncal_bad", g["n_cal_bad"].mean(), ".1f"); put(f"{prefix}.ncal_good", g["n_cal_good"].mean(), ".1f")
    if "pass_thr" in g:
        pt = g["pass_thr"].replace([np.inf, -np.inf], np.nan)
        put(f"{prefix}.never_pass", float(np.isinf(g["pass_thr"]).mean()), "pct0")
        put(f"{prefix}.lam_med", pt.median(), ".2f")


def raw(name):
    p = os.path.join(ROOT, "results", "raw", name)
    return pd.read_csv(p) if os.path.exists(p) else None


def main():
    cfg = json.load(open(os.path.join(ROOT, "results", "run_config.json")))
    env = cfg["environment"]; c = cfg["config"]
    N["ENV.python"] = env["python"]; N["ENV.sklearn"] = env["sklearn"]; N["ENV.torch"] = env.get("torch", "n/a").split("+")[0]
    N["ENV.cpu"] = str(env["cpu_count"])
    a, b = c["alpha"], c["beta"]
    # ---- data facts
    Fm = load_features(os.path.join(ROOT, "data", "features", "matr_clo_severson.npz"))
    Fh = load_features(os.path.join(ROOT, "data", "features", "hust_vq.npz"))
    Tm, Th = Fm["lifetime"].astype(float), Fh["lifetime"].astype(float)
    Lm, Lh = c["datasets"]["matr_clo"]["Lstar"], c["datasets"]["hust"]["Lstar"]
    put("D.n_mc", len(Tm), "int"); put("D.n_matr", int((Fm["dataset"] == "MATR").sum()), "int")
    put("D.n_clo", int((Fm["dataset"] == "CLO").sum()), "int"); put("D.n_hust", len(Th), "int"); put("D.n_total", len(Tm) + len(Th), "int")
    for k, T, L in (("mc", Tm, Lm), ("h", Th, Lh)):
        put(f"D.{k}.T_min", T.min(), "int"); put(f"D.{k}.T_med", np.median(T), "int"); put(f"D.{k}.T_max", T.max(), "int")
        put(f"D.{k}.Lstar", L, "int"); put(f"D.{k}.bad_share", (T < L).mean(), "pct0"); put(f"D.{k}.n_bad", (T < L).sum(), "int")
        put(f"D.{k}.mean_full_cost", np.minimum(T, L).mean(), "int")
    put("D.mc.M", len(Fm["checkpoints"]), "int"); put("D.h.M", len(Fh["checkpoints"]), "int")
    put("CFG.alpha", a, ".2f"); put("CFG.beta", b, ".2f"); put("CFG.n_main", c["n_splits"]["en"], "int")
    put("CFG.n_secondary", c.get("n_splits_secondary", 0), "int")
    for m, v in c["n_splits"].items():
        put(f"CFG.n_{m}", v, "int")
    # ---- E1
    stats_json = os.path.join(ROOT, "results", "statistics.json")
    S = json.load(open(stats_json)) if os.path.exists(stats_json) else {}
    for ds, key in (("matr_clo", "mc"), ("hust", "h")):
        df = raw(f"E1_{ds}_splits.csv")
        if df is None:
            continue
        for m, g in df.groupby("method"):
            split_stats(f"E1.{key}.{m}", g, a, b)
        prop = df[df.method == "proposed"]
        put(f"C.{key}.cal_cycles_trunc", prop.cal_cell_cycles.mean(), "int"); put(f"C.{key}.cal_wall_trunc", prop.cal_wallclock.mean(), "int")
        it = df[df.method == "interval_traj"]
        put(f"C.{key}.cal_cycles_full", it.cal_cell_cycles.mean(), "int"); put(f"C.{key}.cal_wall_full", it.cal_wallclock.mean(), "int")
        put(f"C.{key}.cal_cycles_ratio", it.cal_cell_cycles.mean() / prop.cal_cell_cycles.mean(), ".2f")
        put(f"C.{key}.cal_wall_ratio", it.cal_wallclock.mean() / prop.cal_wallclock.mean(), ".2f")
        put(f"C.{key}.train_cycles_full", prop.train_cell_cycles.mean(), "int"); put(f"C.{key}.train_wall_full", prop.train_wallclock.mean(), "int")
        for r in S.get(f"E1_{ds}_paired", []):
            p = f"P.{key}.{r['comparator']}"
            put(p + ".diff", r["saving_diff"], "pct1"); put(p + ".lo", r["saving_diff_ci_lo"], "pct1"); put(p + ".hi", r["saving_diff_ci_hi"], "pct1")
            put(p + ".p", r["wilcoxon_p"], "p"); put(p + ".padj", r["p_holm"], "p"); put(p + ".r", r["rank_biserial"], ".2f")
            put(p + ".n", r["n_cells"], "int"); put(p + ".t_ref", r["mean_time_ref"], "int"); put(p + ".t_comp", r["mean_time_comp"], "int")
        sp = S.get(f"E8_{ds}_spearman_abs_margin_vs_error")
        if sp:
            put(f"E8.{key}.rho", sp["rho"], ".2f"); put(f"E8.{key}.p", sp["p"], "p")
        pc = os.path.join(ROOT, "results", f"E8_percell_{ds}.csv")
        if os.path.exists(pc):
            d = pd.read_csv(pc)
            near = np.abs(d.log_ratio) < 0.05; far = np.abs(d.log_ratio) >= 0.1
            put(f"E8.{key}.err_near", (d.fp + d.fr)[near].mean(), ".3f"); put(f"E8.{key}.err_far", (d.fp + d.fr)[far].mean(), ".3f")
            put(f"E8.{key}.n_near", near.sum(), "int"); put(f"E8.{key}.share_err_near", (d.fp + d.fr)[near].sum() / max((d.fp + d.fr).sum(), 1e-12), "pct0")
            put(f"E8.{key}.cells_any_error", ((d.fp + d.fr) > 0).mean(), "pct0")
    # ---- E2 base models
    e2 = raw("E2_models_splits.csv")
    if e2 is not None:
        for (ds, model, m), g in e2.groupby(["dataset", "model", "method"]):
            split_stats(f"E2.{'mc' if ds == 'matr_clo' else 'h'}.{model}.{m}", g, a, b)
        for ds, key in (("matr_clo", "mc"), ("hust", "h")):
            lg = e2[(e2.dataset == ds) & (e2.model == "logit") & (e2.method == "proposed")]
            if len(lg):
                put(f"C.{key}.train_cycles_trunc", lg.train_cell_cycles.mean(), "int"); put(f"C.{key}.train_wall_trunc", lg.train_wallclock.mean(), "int")
    # ---- E3
    e3 = raw("E3_ablation_grid_splits.csv")
    if e3 is not None:
        for (ds, grid, m), g in e3.groupby(["dataset", "grid", "method"]):
            split_stats(f"E3.{'mc' if ds == 'matr_clo' else 'h'}.{grid}.{m}", g, a, b)
    # ---- E4
    e4 = raw("E4_robustness_splits.csv")
    if e4 is not None:
        for (ds, f, lv, m), g in e4.groupby(["dataset", "factor", "level", "method"]):
            split_stats(f"E4.{'mc' if ds == 'matr_clo' else 'h'}.{f}.{lv:g}.{m}", g, a, b)
    # ---- E5
    e5 = raw("E5_shift_splits.csv")
    if e5 is not None:
        for (ex, tg, sc, nt, m), g in e5.groupby(["experiment", "target", "scenario", "n_target_cal", "method"]):
            case = (f"{tg}_{'source' if sc == 'source_cal' else 'target' + str(int(nt))}" if ex == "batch_shift"
                    else f"xlab_{'source' if sc.startswith('source') else 'target'}")
            split_stats(f"E5.{case}.{m}", g, a, b)
    # ---- E6
    e6 = raw("E6_compute.csv")
    if e6 is not None:
        for (ds, model), g in e6.groupby(["dataset", "model"]):
            k = f"E6.{'mc' if ds == 'matr_clo' else 'h'}.{model}"
            put(k + ".sec", g.split_seconds.mean(), ".2g" if g.split_seconds.mean() < 1 else ".1f")
            if "peak_rss_mb" in g and g.peak_rss_mb.notna().any():
                put(k + ".mem", g.peak_rss_mb.mean(), "int")
            if "decide_seconds_per_1000_cells" in g and g.decide_seconds_per_1000_cells.notna().any():
                put(k + ".decide_ms", 1000 * g.decide_seconds_per_1000_cells.mean(), ".2f"); put(k + ".cal_ms", 1000 * g.split_seconds.mean(), ".3f")
    # ---- E7
    e7 = raw("E7_sensitivity_splits.csv")
    if e7 is not None:
        for (ds, f, al, be, Ls, m), g in e7.groupby(["dataset", "factor", "alpha", "beta", "Lstar", "method"]):
            key = "mc" if ds == "matr_clo" else "h"
            tag = f"ab_{al:g}_{be:g}" if f == "alpha_beta" else f"L{int(Ls)}"
            split_stats(f"E7.{key}.{tag}.{m}", g, al, be)
    # ---- inflation of the naive sequential rule relative to the nominal level
    worst = []
    for ds in ("matr_clo", "hust"):
        df = raw(f"E1_{ds}_splits.csv")
        if df is not None:
            g = df[df.method == "naive"]
            worst += [g.fpr.mean() / a, g.frr.mean() / b]
    if worst:
        put("RATIO.naive_max", max(worst), ".1f")
    # ---- base-model accuracy by checkpoint (test cells of E1, pooled over splits)
    for ds, key, F in (("matr_clo", "mc", Fm), ("hust", "h", Fh)):
        sc = raw(f"E1_{ds}_scores.csv.gz")
        if sc is None:
            continue
        T = F["lifetime"].astype(float); ck = F["checkpoints"]
        sc["ape"] = np.abs(10 ** sc.yhat - T[sc.cell.values]) / T[sc.cell.values]
        for m, g in sc.groupby("m"):
            put(f"E1ACC.{key}.k{int(ck[m])}", g.ape.mean(), "pct1")
            put(f"E1ACC.{key}.scale_k{int(ck[m])}", 10 ** g.scale.mean() - 1, "pct1")
    # ---- decision-time shares (E1 cells)
    for ds, key, Lx in (("matr_clo", "mc", Lm), ("hust", "h", Lh)):
        cells = raw(f"E1_{ds}_cells.csv.gz")
        if cells is None:
            continue
        for m, g in cells.groupby("method"):
            for k in (50, 100, 200, 300, 500, 1000):
                if k < Lx:
                    put(f"E1.{key}.{m}.dec_by_{k}", float((g.time <= k).mean()), "pct0")
            put(f"E1.{key}.{m}.time_median", float(g.time.median()), "int")
    # ---- E9 protocol-disjoint
    e9 = raw("E9_protocol_grouped_splits.csv")
    if e9 is not None:
        for m, g in e9.groupby("method"):
            split_stats(f"E9.mc.{m}", g, a, b)
        put("E9.n_groups", e9.n_groups.iloc[0], "int")
    # ---- E10 PAC
    e10 = raw("E10_pac_splits.csv")
    if e10 is not None:
        for (ds, design, m), g in e10.groupby(["dataset", "cal_design", "method"]):
            split_stats(f"E10.{'mc' if ds == 'matr_clo' else 'h'}.{design}.{m}", g, a, b)
    # ---- E11 physical interpretation (descriptive)
    r11, c11 = raw("E11_correlations.csv"), raw("E11_coefficients.csv")
    if r11 is not None and c11 is not None:
        for ds, key in (("matr_clo", "mc"), ("hust", "h")):
            r = r11[r11.dataset == ds]
            for (k, f), g in r.groupby(["checkpoint", "feature"]):
                put(f"E11.{key}.rho.{f}.k{int(k)}", g.spearman.iloc[0], ".2f")
            for k, g in r.groupby("checkpoint"):
                put(f"E11.{key}.maxabs.k{int(k)}", g.spearman.abs().max(), ".2f")
            c = c11[c11.dataset == ds].groupby(["checkpoint", "feature"]).coef.agg(lambda v: np.mean(np.abs(v))).unstack()
            share = c.div(c.sum(axis=1), axis=0)
            for k in c.index:
                put(f"E11.{key}.top.k{int(k)}", c.loc[k].idxmax(), "s"); put(f"E11.{key}.topshare.k{int(k)}", share.loc[k].max(), "pct0")
                for f in c.columns:
                    put(f"E11.{key}.share.{f}.k{int(k)}", share.loc[k, f], "pct0")
    from scipy.stats import beta as _beta
    for n0 in (9, 10, 15, 20, 25, 30, 40, 60):
        r = int(np.ceil((n0 + 1) * (1 - a)))
        put(f"PAC.p_exceed_n{n0}", float(_beta.cdf(1 - a, r, n0 + 1 - r)) if r <= n0 else 0.0, "pct0")
    out = os.path.join(ROOT, "results", "manuscript_numbers.json")
    old = json.load(open(out)) if os.path.exists(out) else {}
    for k in ("ABSTRACT",):  # text blocks written by the authors are kept
        if k in old:
            N.setdefault(k, old[k])
    json.dump(dict(sorted(N.items())), open(out, "w"), indent=0, ensure_ascii=False)
    print(f"{len(N)} values -> {out}")


if __name__ == "__main__":
    main()
