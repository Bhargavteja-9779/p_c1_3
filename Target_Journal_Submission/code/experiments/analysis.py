"""Analysis stage: statistics, E8 error analysis, tables (Markdown + CSV) and the
machine-readable summaries results/metrics.json, results/statistics.json,
results/raw_results.csv. Every number used in the manuscript is written here."""
from __future__ import annotations
import glob, json, os
import numpy as np
import pandas as pd
from batscreen.statistics.tests import validity_summary, per_cell_times, paired_comparisons
from batscreen.evaluation.runner import load_features

METHOD_LABEL = {"proposed": "Proposed (trajectory-calibrated)", "naive": "Naive sequential conformal",
                "bonf": "Bonferroni sequential conformal", "single_k100": "Single checkpoint (cycle 100) conformal",
                "point_k100": "Point prediction at cycle 100", "gauss": "Parametric/Bayesian threshold",
                "interval_traj": "Conformal lifetime interval (full-lifetime calibration)",
                "traj_unnorm": "Proposed without score normalisation"}
DS_LABEL = {"matr_clo": "MATR+CLO", "hust": "HUST"}


def _raw(cfg, name):
    p = os.path.join(cfg["paths"]["results"], "raw", name)
    return pd.read_csv(p) if os.path.exists(p) else None


def _md(df, path, floatfmt=".3f"):
    with open(path, "w") as f:
        f.write(df.to_markdown(index=False, floatfmt=floatfmt))
    df.to_csv(path.replace(".md", ".csv"), index=False)


def run(cfg, log):
    R, TB = cfg["paths"]["results"], cfg["paths"]["tables"]
    os.makedirs(TB, exist_ok=True)
    a, b = cfg["alpha"], cfg["beta"]
    metrics, statsj = {}, {}
    allraw = []
    # ---------------- T1: data sets and screening set-up (from the feature tables and config)
    rows = []
    for ds, kind in (("matr_clo", "severson"), ("hust", "vq")):
        F = load_features(os.path.join(cfg["paths"]["features"], f"{ds}_{kind}.npz")); T = F["lifetime"].astype(float)
        d = cfg["datasets"][ds]
        for sub in (["MATR", "CLO"] if ds == "matr_clo" else ["HUST"]):
            m = F["dataset"] == sub
            rows.append(dict(data_set=sub, source={"MATR": "Severson et al. 2019", "CLO": "Attia et al. 2020", "HUST": "Ma et al. 2022"}[sub],
                             cells=int(m.sum()), chemistry="LFP/graphite (A123 APR18650M1A, 1.1 Ah)",
                             protocols={"MATR": "fast charging (various), 4C discharge", "CLO": "multi-step fast charging (CLO), 4C discharge",
                                        "HUST": "5C/1C CC-CV charging, multi-step discharge (various)"}[sub],
                             n_protocols=int(len(np.unique(F["policy"][m]))),
                             T_min=int(T[m].min()), T_median=float(np.median(T[m])), T_max=int(T[m].max()),
                             Lstar=int(d["Lstar"]), bad_share=float((T[m] < d["Lstar"]).mean()),
                             checkpoints=f"{len(d['checkpoints'])} ({min(d['checkpoints'])}-{max(d['checkpoints'])} cycles)",
                             split=f"{int(100*d['split']['train'])}/{int(100*d['split']['cal'])}/{int(100*d['split']['test'])}"))
    _md(pd.DataFrame(rows), os.path.join(TB, "T1_datasets.md"))
    # ---------------- E1 main
    e1 = []
    for ds in ("matr_clo", "hust"):
        df = _raw(cfg, f"E1_{ds}_splits.csv")
        if df is None:
            continue
        e1.append(df); allraw.append(df.assign(experiment="E1"))
        v = validity_summary(df, a, b, by=("method",)); v.insert(0, "dataset", ds)
        metrics[f"E1_{ds}"] = v.set_index("method").to_dict(orient="index")
        F = load_features(os.path.join(cfg["paths"]["features"], f"{ds}_{'severson' if ds == 'matr_clo' else 'vq'}.npz"))
        T = F["lifetime"].astype(float); Ls = cfg["datasets"][ds]["Lstar"]
        cells = pd.read_csv(os.path.join(R, "raw", f"E1_{ds}_cells.csv.gz"))
        pc = per_cell_times(cells, T, Ls)
        comp = paired_comparisons(pc, "proposed", n_boot=10000 if cfg["n_splits"]["en"] >= 100 else 500)
        statsj[f"E1_{ds}_paired"] = comp.to_dict(orient="records")
        statsj[f"E1_{ds}_validity"] = v.to_dict(orient="records")
        # E8 error analysis from per-cell outcomes
        pcp = pc[pc.method == "proposed"].copy()
        pcp["log_ratio"] = np.log10(T[pcp.cell.values] / Ls); pcp["batch"] = F["batch"][pcp.cell.values]
        pcp["policy"] = F["policy"][pcp.cell.values]; pcp["cell_id"] = F["cell_id"][pcp.cell.values]; pcp["T"] = T[pcp.cell.values]
        bins = [-np.inf, -0.2, -0.1, -0.05, 0, 0.05, 0.1, 0.2, np.inf]
        pcp["margin_bin"] = pd.cut(pcp.log_ratio, bins).astype(str)
        err = pcp.groupby("margin_bin", sort=False).agg(n_cells=("cell", "size"), false_pass_freq=("fp", "mean"),
                                                         false_reject_freq=("fr", "mean"), early_decision=("early", "mean"),
                                                         mean_cycles=("time", "mean")).reset_index()
        cats = pd.cut(pd.Series(bins[:-1]) + 1e-9, bins)  # one representative per bin, in numeric order
        order = {str(c): i for i, c in enumerate(cats)}
        err["o"] = err.margin_bin.map(order); err = err.sort_values("o").drop(columns="o")
        _md(err, os.path.join(TB, f"E8_error_by_margin_{ds}.md"))
        byb = pcp.groupby("batch").agg(n_cells=("cell", "size"), false_pass_freq=("fp", "mean"), false_reject_freq=("fr", "mean"),
                                       early=("early", "mean")).reset_index()
        _md(byb, os.path.join(TB, f"E8_error_by_batch_{ds}.md"))
        worst = pcp.assign(err=pcp.fp + pcp.fr).sort_values("err", ascending=False).head(10)[
            ["cell_id", "batch", "policy", "T", "log_ratio", "fp", "fr", "early", "time", "n"]]
        _md(worst, os.path.join(TB, f"E8_worst_cells_{ds}.md"))
        pcp.to_csv(os.path.join(R, f"E8_percell_{ds}.csv"), index=False)
        statsj[f"E8_{ds}_spearman_abs_margin_vs_error"] = dict(zip(["rho", "p"], map(float, __import__("scipy").stats.spearmanr(
            np.abs(pcp.log_ratio), pcp.fp + pcp.fr))))
        # confusion counts aggregated over splits
        cm = cells.assign(good=T[cells.cell.values] >= Ls).groupby(["method", "good", "decision"]).size().unstack(fill_value=0)
        cm.to_csv(os.path.join(R, f"E1_{ds}_confusion.csv"))
    if e1:
        e1 = pd.concat(e1)
        t = validity_summary(e1, a, b, by=("dataset", "method"))
        t["method"] = t["method"].map(METHOD_LABEL); t["dataset"] = t["dataset"].map(DS_LABEL)
        cols = ["dataset", "method", "fpr_mean", "fpr_ci_hi", "frr_mean", "frr_ci_hi", "accuracy_mean", "early_rate_mean",
                "time_saving_mean", "mean_time_mean", "n_splits"]
        _md(t[cols], os.path.join(TB, "T2_main_results.md"))
        comp_all = []
        for ds in ("matr_clo", "hust"):
            c = pd.DataFrame(statsj.get(f"E1_{ds}_paired", []))
            if len(c):
                c.insert(0, "dataset", DS_LABEL[ds]); comp_all.append(c)
        if comp_all:
            c = pd.concat(comp_all); c["comparator"] = c["comparator"].map(METHOD_LABEL)
            _md(c[["dataset", "comparator", "n_cells", "mean_time_ref", "mean_time_comp", "saving_diff", "saving_diff_ci_lo",
                   "saving_diff_ci_hi", "wilcoxon_p", "p_holm", "rank_biserial"]], os.path.join(TB, "T3_paired_efficiency.md"), ".4g")
    # ---------------- E2 base models
    e2 = _raw(cfg, "E2_models_splits.csv")
    if e2 is not None:
        allraw.append(e2.assign(experiment="E2"))
        e1m = e1[e1.method.isin(["proposed", "naive", "single_k100", "gauss", "interval_traj"])] if len(e1) else None
        both = pd.concat([e2, e1m]) if e1m is not None else e2
        v = validity_summary(both, a, b, by=("dataset", "model", "method"))
        v = v[v.method.isin(["proposed", "naive", "single_k100", "gauss"])]
        v["dataset"] = v["dataset"].map(DS_LABEL)
        _md(v[["dataset", "model", "method", "fpr_mean", "frr_mean", "accuracy_mean", "early_rate_mean", "time_saving_mean",
               "n_splits"]], os.path.join(TB, "T4_base_models.md"))
        metrics["E2"] = v.to_dict(orient="records")
        camp = both[both.method == "proposed"].groupby(["dataset", "model"])[["train_cell_cycles", "train_wallclock",
                                                                             "cal_cell_cycles", "cal_wallclock"]].mean().reset_index()
        interval = both[both.method == "interval_traj"].groupby(["dataset", "model"])[["cal_cell_cycles", "cal_wallclock"]].mean().reset_index()
        interval["model"] = interval["model"] + " (interval, full-lifetime cal.)"
        camp = pd.concat([camp, interval]); camp["dataset"] = camp["dataset"].map(DS_LABEL)
        _md(camp, os.path.join(TB, "T5_campaign_cost.md"), ".0f"); metrics["campaign_cost"] = camp.to_dict(orient="records")
    # ---------------- E3 ablation
    e3 = _raw(cfg, "E3_ablation_grid_splits.csv")
    if e3 is not None:
        allraw.append(e3.assign(experiment="E3"))
        v = validity_summary(e3, a, b, by=("dataset", "grid", "method")); v["dataset"] = v["dataset"].map(DS_LABEL)
        _md(v[["dataset", "grid", "method", "fpr_mean", "frr_mean", "early_rate_mean", "time_saving_mean", "n_splits"]],
            os.path.join(TB, "T6_ablation_grid.md"))
        metrics["E3"] = v.to_dict(orient="records")
    # ---------------- E4 robustness
    e4 = _raw(cfg, "E4_robustness_splits.csv")
    if e4 is not None:
        allraw.append(e4.assign(experiment="E4"))
        v = validity_summary(e4, a, b, by=("dataset", "factor", "level", "method")); v["dataset"] = v["dataset"].map(DS_LABEL)
        _md(v[["dataset", "factor", "level", "method", "fpr_mean", "frr_mean", "time_saving_mean", "n_splits"]],
            os.path.join(TB, "T7_robustness.md"))
        metrics["E4"] = v.to_dict(orient="records")
    # ---------------- E5 shift
    e5 = _raw(cfg, "E5_shift_splits.csv")
    if e5 is not None:
        allraw.append(e5.assign(experiment="E5"))
        v = validity_summary(e5, a, b, by=("experiment", "target", "scenario", "n_target_cal", "method"))
        _md(v[["experiment", "target", "scenario", "n_target_cal", "method", "fpr_mean", "fpr_ci_hi", "frr_mean", "frr_ci_hi",
               "time_saving_mean", "n_splits"]], os.path.join(TB, "T8_shift.md"))
        metrics["E5"] = v.to_dict(orient="records")
    # ---------------- E6 compute
    e6 = _raw(cfg, "E6_compute.csv")
    if e6 is not None:
        g = e6.groupby(["dataset", "model"]).agg({c: "mean" for c in e6.columns if c not in ("dataset", "model", "rep")}).reset_index()
        g["dataset"] = g["dataset"].map(DS_LABEL); _md(g, os.path.join(TB, "T9_compute.md"), ".4g"); metrics["E6"] = g.to_dict(orient="records")
    # ---------------- E7 sensitivity
    e7 = _raw(cfg, "E7_sensitivity_splits.csv")
    if e7 is not None:
        allraw.append(e7.assign(experiment="E7"))
        v = validity_summary(e7, a, b, by=("dataset", "factor", "alpha", "beta", "Lstar", "method"))
        # nominal levels differ per row: recompute exceedance shares against own alpha/beta
        rows = []
        for key, g in e7.groupby(["dataset", "factor", "alpha", "beta", "Lstar", "method"]):
            rows.append(dict(zip(["dataset", "factor", "alpha", "beta", "Lstar", "method"], key),
                             fpr_mean=g.fpr.mean(), frr_mean=g.frr.mean(), fpr_le_alpha=g.fpr.mean() <= key[2] + 1.96 * g.fpr.std() / np.sqrt(len(g)),
                             frr_le_beta=g.frr.mean() <= key[3] + 1.96 * g.frr.std() / np.sqrt(len(g)), time_saving_mean=g.time_saving.mean(),
                             bad_share=g.n_bad.sum() / (g.n_bad.sum() + g.n_good.sum()), n_splits=len(g)))
        v = pd.DataFrame(rows); v["dataset"] = v["dataset"].map(DS_LABEL)
        _md(v, os.path.join(TB, "T10_sensitivity.md")); metrics["E7"] = v.to_dict(orient="records")
    # ---------------- E9 protocol-grouped (added after design freeze)
    e9 = _raw(cfg, "E9_protocol_grouped_splits.csv")
    if e9 is not None:
        allraw.append(e9.assign(experiment="E9"))
        v = validity_summary(e9, a, b, by=("method",)); v.insert(0, "dataset", "MATR+CLO (protocol-disjoint)")
        _md(v[["dataset", "method", "fpr_mean", "fpr_ci_hi", "frr_mean", "frr_ci_hi", "accuracy_mean", "early_rate_mean",
               "time_saving_mean", "n_splits"]], os.path.join(TB, "T11_protocol_grouped.md"))
        metrics["E9"] = v.to_dict(orient="records")
    # ---------------- E10 PAC (added after design freeze) + analytic table
    e10 = _raw(cfg, "E10_pac_splits.csv")
    if e10 is not None:
        allraw.append(e10.assign(experiment="E10"))
        rows = []
        for key, g in e10.groupby(["dataset", "cal_design", "method"]):
            rows.append(dict(dataset=DS_LABEL[key[0]], cal_design=key[1], method=key[2], fpr_mean=g.fpr.mean(), frr_mean=g.frr.mean(),
                             fpr_split_above_alpha=float((g.fpr > a + 1e-12).mean()), frr_split_above_beta=float((g.frr > b + 1e-12).mean()),
                             never_pass=float(np.isinf(g.pass_thr).mean()), time_saving_mean=g.time_saving.mean(),
                             n_cal_bad=g.n_cal_bad.mean(), n_cal_good=g.n_cal_good.mean(), n_splits=len(g)))
        v = pd.DataFrame(rows); _md(v, os.path.join(TB, "T12_pac.md")); metrics["E10"] = v.to_dict(orient="records")
    # ---------------- E12 training-selected grid (added after E3)
    e12 = _raw(cfg, "E12_selected_grid_splits.csv")
    if e12 is not None:
        allraw.append(e12.assign(experiment="E12"))
        v = validity_summary(e12, a, b, by=("dataset", "method")); v["dataset"] = v["dataset"].map(DS_LABEL)
        sel = e12.groupby(["dataset", "grid_selected"]).size().rename("n").reset_index()
        sel["share"] = sel["n"] / sel.groupby("dataset")["n"].transform("sum"); sel["dataset"] = sel["dataset"].map(DS_LABEL)
        _md(v[["dataset", "method", "fpr_mean", "fpr_ci_hi", "frr_mean", "frr_ci_hi", "early_rate_mean", "time_saving_mean", "n_splits"]],
            os.path.join(TB, "T14_selected_grid.md"))
        _md(sel, os.path.join(TB, "T15_selected_grid_choices.md"))
        metrics["E12"] = v.to_dict(orient="records")
        if e3 is not None:  # paired with E3 (same split seeds): selected grid vs the pre-registered dense grid
            from scipy.stats import wilcoxon
            for ds in ("matr_clo", "hust"):
                dense = "all16" if ds == "matr_clo" else "all17"
                x = e12[e12.dataset == ds].set_index("split").time_saving
                y = e3[(e3.dataset == ds) & (e3.grid == dense) & (e3.method == "proposed")].set_index("split").time_saving
                j = x.index.intersection(y.index); dlt = (x[j] - y[j])
                rng = np.random.default_rng(0); bs = [rng.choice(dlt.values, len(dlt)).mean() for _ in range(10000)]
                statsj[f"E12_{ds}_vs_dense"] = dict(n_splits=int(len(j)), mean_diff=float(dlt.mean()), ci_lo=float(np.percentile(bs, 2.5)),
                                                   ci_hi=float(np.percentile(bs, 97.5)), wilcoxon_p=float(wilcoxon(dlt).pvalue) if (dlt != 0).any() else 1.0,
                                                   unit="split (paired by seed)")
    from scipy.stats import beta as _beta
    from batscreen.screening.calibration import pac_rank
    rows = []
    for n0 in [9, 10, 15, 20, 25, 30, 40, 60, 100]:
        r = int(np.ceil((n0 + 1) * (1 - a)))
        p_exceed = float(_beta.cdf(1 - a, r, n0 + 1 - r)) if r <= n0 else 0.0
        rows.append(dict(n_calibration_cells_in_class=n0, marginal_rank=r if r <= n0 else None,
                         P_conditional_error_above_alpha=p_exceed,
                         pac_rank_delta_0_1=pac_rank(n0, 1 - a, 0.1), pac_rank_delta_0_2=pac_rank(n0, 1 - a, 0.2)))
    t = pd.DataFrame(rows); _md(t, os.path.join(TB, "T13_conditional_error_analytic.md")); statsj["T13_analytic"] = t.to_dict(orient="records")
    if allraw:
        pd.concat(allraw, ignore_index=True).to_csv(os.path.join(R, "raw_results.csv"), index=False)
    json.dump(metrics, open(os.path.join(R, "metrics.json"), "w"), indent=1, default=float)
    json.dump(statsj, open(os.path.join(R, "statistics.json"), "w"), indent=1, default=float)
    log.info("analysis written")
