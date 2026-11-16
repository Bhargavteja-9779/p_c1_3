"""Publication figures, drawn only from machine-generated result files.
Palette: validated categorical slots (blue, orange, aqua, yellow; dataviz reference
palette, light mode); baselines without a categorical role are neutral gray; the
proposed method is always blue. Output: PNG (300 dpi) + PDF for each figure."""
from __future__ import annotations
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, average_precision_score
from batscreen.evaluation.runner import load_features

BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
INK, INK2, GRID, GRAY = "#0b0b0b", "#52514e", "#e4e3df", "#9a9893"
M_COL = {"proposed": BLUE, "naive": ORANGE, "single_k100": AQUA, "gauss": YELLOW}
LBL = {"proposed": "Proposed", "naive": "Naive sequential", "bonf": "Bonferroni", "single_k100": "Single checkpoint (100)",
       "point_k100": "Point prediction (100)", "gauss": "Parametric threshold", "interval_traj": "Lifetime interval (full cal.)",
       "traj_unnorm": "Proposed, unnormalised"}
DS = {"matr_clo": ("MATR+CLO", "severson"), "hust": ("HUST", "vq")}
ORDER = ["proposed", "traj_unnorm", "single_k100", "interval_traj", "bonf", "gauss", "point_k100", "naive"]

plt.rcParams.update({"font.size": 8, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": GRID,
                     "grid.linewidth": 0.6, "axes.axisbelow": True, "legend.frameon": False, "savefig.dpi": 300,
                     "figure.dpi": 100, "lines.linewidth": 2, "pdf.fonttype": 42})


def _save(fig, cfg, name):
    d = cfg["paths"]["figures"]; os.makedirs(d, exist_ok=True)
    fig.savefig(os.path.join(d, name + ".png"), bbox_inches="tight"); fig.savefig(os.path.join(d, name + ".pdf"), bbox_inches="tight")
    plt.close(fig)


def _raw(cfg, n):
    p = os.path.join(cfg["paths"]["results"], "raw", n)
    return pd.read_csv(p) if os.path.exists(p) else None


def _F(cfg, ds, kind=None):
    return load_features(os.path.join(cfg["paths"]["features"], f"{ds}_{kind or DS[ds][1]}.npz"))


def fig_workflow(cfg):
    fig, ax = plt.subplots(figsize=(7.2, 2.9)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 3.4)
    boxes = [(0.05, "Cycling data\n(cycles 1 ... $k$)"),
             (2.05, "Checkpoint features\n$\\Delta Q(V)$, $\\Delta V(q)$,\ncapacity fade"),
             (4.05, "Base predictor $h_k$\n(trained on\ntraining cells)"),
             (6.05, "Normalised score\n$S_k=(h_k-\\log_{10}L^*)/s_k$"),
             (8.05, "Decision at $k$:\npass / reject /\ncontinue cycling")]
    for x, t in boxes:
        ax.add_patch(FancyBboxPatch((x, 1.95), 1.85, 1.2, boxstyle="round,pad=0.02,rounding_size=0.08", fc="#f0efec", ec=INK2, lw=0.8))
        ax.text(x + 0.925, 2.55, t, ha="center", va="center", fontsize=7, color=INK, linespacing=1.3)
    for x in [1.9, 3.9, 5.9, 7.9]:
        ax.annotate("", xy=(x + 0.15, 2.55), xytext=(x, 2.55), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1))
    ax.add_patch(FancyBboxPatch((0.1, 0.05), 9.8, 1.35, boxstyle="round,pad=0.02,rounding_size=0.08", fc="#cde2fb", ec=BLUE, lw=0.8))
    ax.text(5.0, 0.72, "Trajectory calibration on calibration cells cycled only to $\\min(T, L^*)$\n"
            "$\\hat\\lambda$ = rank quantile of $\\max_k S_k$ over bad cells;   $\\hat\\mu$ = rank quantile of $\\max_k(-S_k)$ over good cells\n"
            "pass if $S_k>\\hat\\lambda$, reject if $S_k<-\\hat\\mu$  $\\Rightarrow$  P(false pass | bad) $\\leq \\alpha$,  P(false reject | good) $\\leq \\beta$ for any stopping time",
            ha="center", va="center", fontsize=7, color=INK, linespacing=1.5)
    ax.annotate("", xy=(8.975, 1.93), xytext=(8.975, 1.42), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1))
    _save(fig, cfg, "Fig1_workflow")


def fig_lifetimes(cfg):
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.4))
    for ax, ds in zip(axs, DS):
        F = _F(cfg, ds); T = F["lifetime"]; Ls = cfg["datasets"][ds]["Lstar"]
        if ds == "matr_clo":
            groups = [("MATR (Severson et al.)", T[F["dataset"] == "MATR"], BLUE), ("CLO (Attia et al.)", T[F["dataset"] == "CLO"], ORANGE)]
        else:
            groups = [("HUST (Ma et al.)", T, BLUE)]
        bins = np.linspace(T.min() * 0.95, T.max() * 1.02, 25)
        ax.hist([g[1] for g in groups], bins=bins, stacked=True, color=[g[2] for g in groups], label=[g[0] for g in groups],
                edgecolor="white", linewidth=0.8)
        ax.axvline(Ls, color=INK, lw=1.2, ls="--"); ax.text(Ls, ax.get_ylim()[1] * 0.97, f" $L^*$ = {Ls}", va="top", ha="left", fontsize=7, color=INK)
        ax.set_xlabel("Cycle life T (cycles to 80% of nominal capacity)"); ax.set_ylabel("Cells")
        ax.set_title(f"{DS[ds][0]} (n = {len(T)})", fontsize=8.5, color=INK, loc="left")
        ax.legend(fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=2)
    fig.tight_layout(); _save(fig, cfg, "Fig2_lifetime_distributions")


def fig_accuracy(cfg):
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.4))
    for ax, ds in zip(axs, DS):
        sc = _raw(cfg, f"E1_{ds}_scores.csv.gz")
        if sc is None:
            continue
        F = _F(cfg, ds); T = F["lifetime"].astype(float); ck = F["checkpoints"]
        sc["T"] = T[sc.cell.values]; sc["ape"] = np.abs(10 ** sc.yhat - sc["T"]) / sc["T"]; sc["k"] = ck[sc.m.values]
        g = sc.groupby("k").agg(mape=("ape", "mean"), scale=("scale", "mean")).reset_index()
        ax.plot(g.k, 100 * g.mape, "-o", color=BLUE, ms=4, label="MAPE of cycle-life prediction (%)")
        ax.plot(g.k, 100 * (10 ** g.scale - 1), "-s", color=ORANGE, ms=4, label="Score scale s_k (as % error)")
        ax.set_xlabel("Checkpoint k (cycles observed)"); ax.set_ylabel("%"); ax.set_title(DS[ds][0], fontsize=8.5, loc="left", color=INK)
        ax.legend(fontsize=7)
    fig.tight_layout(); _save(fig, cfg, "Fig3_base_model_accuracy")


def _validity_table(df, alpha, beta):
    g = df.groupby("method").agg(fpr=("fpr", "mean"), fpr_sd=("fpr", "std"), frr=("frr", "mean"), frr_sd=("frr", "std"),
                                 sav=("time_saving", "mean"), n=("fpr", "size")).reset_index()
    g["fpr_ci"] = 1.96 * g.fpr_sd / np.sqrt(g.n); g["frr_ci"] = 1.96 * g.frr_sd / np.sqrt(g.n)
    g["valid"] = (g.fpr - g.fpr_ci <= alpha) & (g.frr - g.frr_ci <= beta)
    return g


def fig_validity_efficiency(cfg):
    a, b = cfg["alpha"], cfg["beta"]
    fig, axs = plt.subplots(2, 2, figsize=(7.4, 5.2), sharey="row")
    for j, ds in enumerate(DS):
        df = _raw(cfg, f"E1_{ds}_splits.csv")
        if df is None:
            continue
        g = _validity_table(df, a, b).set_index("method").reindex([m for m in ORDER if m in set(df.method)])
        y = np.arange(len(g))[::-1]
        ax = axs[0, j]
        ax.errorbar(g.fpr, y + 0.15, xerr=g.fpr_ci, fmt="o", color=BLUE, ms=5, lw=1.2, label="False-pass rate (bad cells)")
        ax.errorbar(g.frr, y - 0.15, xerr=g.frr_ci, fmt="s", color=ORANGE, ms=5, lw=1.2, label="False-reject rate (good cells)")
        ax.axvline(a, color=INK, ls="--", lw=1); ax.text(a, len(g) - 0.4, " nominal 0.10", fontsize=7, color=INK)
        ax.set_yticks(y); ax.set_yticklabels([LBL[m] for m in g.index]); ax.set_xlabel("Error rate (mean over splits, 95% CI)")
        ax.set_title(f"{DS[ds][0]}: validity", fontsize=8.5, loc="left", color=INK)
        if j == 1:
            ax.legend(fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2)
        ax = axs[1, j]
        cols = [BLUE if m == "proposed" else GRAY for m in g.index]
        ax.barh(y, 100 * g.sav, color=cols, height=0.6)
        for yy, (m, r) in zip(y, g.iterrows()):
            ax.text(100 * r.sav + 1, yy, f"{100*r.sav:.1f}%" + ("" if r.valid else "  (error > nominal)"), va="center", fontsize=6.8, color=INK)
        ax.set_yticks(y); ax.set_yticklabels([LBL[m] for m in g.index]); ax.set_xlim(0, 135)
        ax.set_xlabel("Cycling time saved (%)")
        ax.set_title(f"{DS[ds][0]}: efficiency", fontsize=8.5, loc="left", color=INK)
    fig.tight_layout(); _save(fig, cfg, "Fig4_validity_and_efficiency")


def fig_decision_time(cfg):
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.5))
    for ax, ds in zip(axs, DS):
        c = _raw(cfg, f"E1_{ds}_cells.csv.gz")
        if c is None:
            continue
        Ls = cfg["datasets"][ds]["Lstar"]; T = _F(cfg, ds)["lifetime"].astype(float)
        grid = np.linspace(0, Ls, 300)
        for m, col, lab in [("proposed", BLUE, "Proposed"), ("single_k100", AQUA, "Single checkpoint (100)"), ("naive", ORANGE, "Naive sequential (invalid)")]:
            t = c[c.method == m].time.values
            ax.plot(grid, [(t <= x).mean() for x in grid], color=col, label=lab)
        full = np.minimum(T[c[c.method == "proposed"].cell.values], Ls)
        ax.plot(grid, [(full <= x).mean() for x in grid], color=GRAY, ls="--", label="Observe to min(T, L*)")
        ax.set_xlabel("Cycles completed"); ax.set_ylabel("Share of test cells decided"); ax.set_ylim(0, 1.02)
        ax.set_title(DS[ds][0], fontsize=8.5, loc="left", color=INK)
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, fontsize=7, loc="lower center", ncol=4, bbox_to_anchor=(0.5, -0.06))
    fig.tight_layout(); _save(fig, cfg, "Fig5_decision_time")


def fig_trajectories(cfg):
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.7))
    for ax, ds in zip(axs, DS):
        sc, sp = _raw(cfg, f"E1_{ds}_scores.csv.gz"), _raw(cfg, f"E1_{ds}_splits.csv")
        if sc is None:
            continue
        F = _F(cfg, ds); T = F["lifetime"].astype(float); ck = F["checkpoints"]; Ls = cfg["datasets"][ds]["Lstar"]
        s0 = sorted(sc.split.unique())[0]; d = sc[sc.split == s0]
        r = sp[(sp.split == s0) & (sp.method == "proposed")].iloc[0]
        cells = d.cell.unique()
        rng = np.random.default_rng(0); pick = rng.choice(cells, size=min(8, len(cells)), replace=False)
        for cidx in pick:
            dd = d[d.cell == cidx].sort_values("m"); good = T[cidx] >= Ls
            ax.plot(ck[dd.m.values], dd.S, "-", color=BLUE if good else ORANGE, lw=1.2, alpha=0.9)
        ax.axhline(r.pass_thr, color=INK, lw=1, ls="--"); ax.axhline(r.rej_thr, color=INK, lw=1, ls=":")
        ax.text(ck[-1], r.pass_thr, " pass", va="bottom", ha="right", fontsize=7); ax.text(ck[-1], r.rej_thr, " reject", va="top", ha="right", fontsize=7)
        ax.plot([], [], color=BLUE, label=f"good cell (T >= {Ls})"); ax.plot([], [], color=ORANGE, label=f"bad cell (T < {Ls})")
        ax.set_xscale("log"); ax.set_xlabel("Checkpoint k (cycles, log scale)"); ax.set_ylabel("Normalised score S_k")
        ax.set_title(f"{DS[ds][0]}: 8 test cells, split {s0}", fontsize=8.5, loc="left", color=INK); ax.legend(fontsize=6.8, loc="lower left")
    fig.tight_layout(); _save(fig, cfg, "Fig6_score_trajectories")


def fig_ablation(cfg):
    e3 = _raw(cfg, "E3_ablation_grid_splits.csv")
    if e3 is None:
        return
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.8))
    for ax, ds in zip(axs, DS):
        d = e3[e3.dataset == ds]
        g = d.groupby(["grid", "method"]).agg(sav=("time_saving", "mean"), fpr=("fpr", "mean"), frr=("frr", "mean")).reset_index()
        grids = list(dict.fromkeys(d.grid)); y = np.arange(len(grids))[::-1]
        for off, m, col in [(0.2, "proposed", BLUE), (0, "traj_unnorm", AQUA), (-0.2, "naive", ORANGE)]:
            gg = g[g.method == m].set_index("grid").reindex(grids)
            ax.barh(y + off, 100 * gg.sav, height=0.18, color=col, label=LBL[m])
            for yy, (gname, r) in zip(y, gg.iterrows()):
                ax.text(100 * r.sav + 1, yy + off, f"FP {r.fpr:.2f} / FR {r.frr:.2f}", va="center", fontsize=5.6, color=INK2)
        ax.set_yticks(y); ax.set_yticklabels(grids, fontsize=7); ax.set_xlim(0, 140); ax.set_xlabel("Cycling time saved (%)")
        ax.set_title(DS[ds][0], fontsize=8.5, loc="left", color=INK)
        if ds == "hust":
            ax.legend(fontsize=6.5, loc="lower right")
    fig.tight_layout(); _save(fig, cfg, "Fig7_ablation_checkpoint_grid")


def fig_robustness(cfg):
    e4, e7 = _raw(cfg, "E4_robustness_splits.csv"), _raw(cfg, "E7_sensitivity_splits.csv")
    if e4 is None:
        return
    factors = [("cal_fraction", "Calibration fraction"), ("train_fraction", "Training fraction"),
               ("noise_both", "Feature noise, cal.+test (x SD)"), ("noise_test", "Feature noise, test only (x SD)")]
    fig, axs = plt.subplots(2, 4, figsize=(7.4, 3.8))
    for i, ds in enumerate(DS):
        for j, (f, lab) in enumerate(factors):
            ax = axs[i, j]; d = e4[(e4.dataset == ds) & (e4.factor == f)]
            for m in ["proposed", "naive", "single_k100", "gauss"]:
                g = d[d.method == m].groupby("level").agg(fpr=("fpr", "mean"), frr=("frr", "mean")).reset_index()
                ax.plot(g.level, np.maximum(g.fpr, g.frr), "-o", ms=3.5, color=M_COL[m], lw=1.5, label=LBL[m])
            ax.axhline(0.1, color=INK, ls="--", lw=0.9)
            ax.set_xlabel(lab, fontsize=7); ax.tick_params(labelsize=6.5)
            if j == 0:
                ax.set_ylabel(f"{DS[ds][0]}\nmax(FPR, FRR)", fontsize=7)
    axs[0, 0].legend(fontsize=5.8, loc="upper right")
    fig.tight_layout(); _save(fig, cfg, "Fig8_robustness")
    if e7 is not None:
        fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.5))
        for ax, ds in zip(axs, DS):
            d = e7[(e7.dataset == ds) & (e7.factor == "Lstar") & (e7.method == "proposed")]
            g = d.groupby("Lstar").agg(fpr=("fpr", "mean"), frr=("frr", "mean"), sav=("time_saving", "mean")).reset_index()
            x = np.arange(len(g))
            ax.bar(x - 0.2, g.fpr, 0.35, color=BLUE, label="False-pass rate"); ax.bar(x + 0.2, g.frr, 0.35, color=ORANGE, label="False-reject rate")
            for xx, r in zip(x, g.itertuples()):
                ax.text(xx, max(r.fpr, r.frr) + 0.01, f"saved {100*r.sav:.0f}%", ha="center", fontsize=7, color=INK)
            ax.axhline(0.1, color=INK, ls="--", lw=0.9); ax.set_xticks(x); ax.set_xticklabels([f"L* = {int(v)}" for v in g.Lstar])
            ax.set_ylim(0, 0.16); ax.set_ylabel("Error rate"); ax.set_title(f"{DS[ds][0]}: proposed, alpha = beta = 0.1", fontsize=8.5, loc="left", color=INK)
            ax.legend(fontsize=7, loc="upper left")
        fig.tight_layout(); _save(fig, cfg, "Fig9_sensitivity_Lstar")


def fig_shift(cfg):
    e5 = _raw(cfg, "E5_shift_splits.csv")
    if e5 is None:
        return
    e5 = e5.copy(); e5["case"] = np.where(e5.experiment == "batch_shift",
                                          "b1+b2 -> " + e5.target.astype(str) + ": " + e5.scenario + np.where(e5.n_target_cal > 0, " n=" + e5.n_target_cal.astype(str), ""),
                                          "MATR -> HUST: " + e5.scenario)
    cases = list(dict.fromkeys(e5.case))
    fig, axs = plt.subplots(1, 2, figsize=(7.4, 3.2), sharey=True)
    for ax, err, lab in [(axs[0], "fpr", "False-pass rate"), (axs[1], "frr", "False-reject rate")]:
        y = np.arange(len(cases))[::-1]
        for off, m in [(0.24, "proposed"), (0.08, "single_k100"), (-0.08, "gauss"), (-0.24, "naive")]:
            g = e5[e5.method == m].groupby("case")[err].agg(["mean", "std", "size"]).reindex(cases)
            ax.errorbar(g["mean"], y + off, xerr=1.96 * g["std"] / np.sqrt(g["size"]), fmt="o", ms=3.5, lw=1, color=M_COL[m], label=LBL[m])
        ax.axvline(0.1, color=INK, ls="--", lw=0.9); ax.set_xlabel(lab + " (95% CI)")
        ax.set_yticks(y); ax.set_yticklabels(cases, fontsize=6.3)
    axs[1].legend(fontsize=6.3, loc="lower right"); fig.tight_layout(); _save(fig, cfg, "Fig10_distribution_shift")


def fig_errors(cfg):
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.6))
    for ax, ds in zip(axs, DS):
        p = os.path.join(cfg["paths"]["results"], f"E8_percell_{ds}.csv")
        if not os.path.exists(p):
            continue
        d = pd.read_csv(p)
        ax.scatter(d.log_ratio[d.log_ratio < 0], d.fp[d.log_ratio < 0], s=10, color=ORANGE, label="bad cell: false-pass frequency", edgecolors="white", linewidths=0.4)
        ax.scatter(d.log_ratio[d.log_ratio >= 0], d.fr[d.log_ratio >= 0], s=10, color=BLUE, label="good cell: false-reject frequency", edgecolors="white", linewidths=0.4)
        ax.axvline(0, color=INK, lw=0.8); ax.set_xlabel("log10(T / L*)"); ax.set_ylabel("Error frequency across splits")
        ax.set_title(DS[ds][0], fontsize=8.5, loc="left", color=INK)
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, fontsize=7, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.06))
    fig.tight_layout(); _save(fig, cfg, "Fig11_error_analysis")


def fig_confusion(cfg):
    meths = ["proposed", "single_k100", "point_k100", "naive"]
    fig, axs = plt.subplots(2, 4, figsize=(7.2, 3.6))
    for i, ds in enumerate(DS):
        c = _raw(cfg, f"E1_{ds}_cells.csv.gz")
        if c is None:
            continue
        T = _F(cfg, ds)["lifetime"].astype(float); Ls = cfg["datasets"][ds]["Lstar"]
        c["good"] = T[c.cell.values] >= Ls
        for j, m in enumerate(meths):
            d = c[c.method == m]; ax = axs[i, j]; ax.grid(False)
            mat = np.array([[((~d.good) & (d.decision == -1)).sum(), ((~d.good) & (d.decision == 1)).sum()],
                            [(d.good & (d.decision == -1)).sum(), (d.good & (d.decision == 1)).sum()]], float)
            rown = mat / mat.sum(axis=1, keepdims=True)
            ax.imshow(rown, cmap=matplotlib.colors.LinearSegmentedColormap.from_list("b", ["#f0efec", "#256abf"]), vmin=0, vmax=1)
            for (r, q), v in np.ndenumerate(rown):
                ax.text(q, r, f"{v:.3f}", ha="center", va="center", fontsize=7, color="white" if v > 0.6 else INK)
            ax.set_xticks([0, 1]); ax.set_xticklabels(["reject", "pass"], fontsize=6.5); ax.set_yticks([0, 1])
            ax.set_yticklabels(["bad", "good"] if j == 0 else ["", ""], fontsize=6.5)
            ax.set_title(f"{DS[ds][0]}\n{LBL[m]}", fontsize=6.5, color=INK)
    fig.tight_layout(); _save(fig, cfg, "Fig12_confusion_matrices")


def fig_roc_pr(cfg):
    fig, axs = plt.subplots(2, 2, figsize=(7.2, 5.0))
    for j, ds in enumerate(DS):
        sc = _raw(cfg, f"E1_{ds}_scores.csv.gz")
        if sc is None:
            continue
        F = _F(cfg, ds); T = F["lifetime"].astype(float); ck = list(F["checkpoints"]); Ls = cfg["datasets"][ds]["Lstar"]
        sc["good"] = (T[sc.cell.values] >= Ls).astype(int)
        for k, col in zip([50, 100, 300] if ds == "matr_clo" else [100, 300, 1000], [ORANGE, AQUA, BLUE]):
            d = sc[sc.m == ck.index(k)]
            fpr, tpr, _ = roc_curve(d.good, d.S); auc = roc_auc_score(d.good, d.S)
            axs[0, j].plot(fpr, tpr, color=col, label=f"k = {k}: AUC {auc:.3f}")
            pr, rc, _ = precision_recall_curve(d.good, d.S); ap = average_precision_score(d.good, d.S)
            axs[1, j].plot(rc, pr, color=col, label=f"k = {k}: AP {ap:.3f}")
        axs[0, j].plot([0, 1], [0, 1], color=GRAY, lw=0.8, ls="--")
        axs[0, j].set_xlabel("False-positive rate (bad cells scored as good)"); axs[0, j].set_ylabel("True-positive rate")
        axs[1, j].set_xlabel("Recall (good cells)"); axs[1, j].set_ylabel("Precision")
        for ax in axs[:, j]:
            ax.legend(fontsize=7); ax.set_title(f"{DS[ds][0]}: score S_k vs class (pooled test cells)", fontsize=8, loc="left", color=INK)
    fig.tight_layout(); _save(fig, cfg, "Fig13_roc_pr")


def fig_compute(cfg):
    e6 = _raw(cfg, "E6_compute.csv")
    if e6 is None:
        return
    d = e6[~e6.model.str.startswith("calibration")].groupby(["dataset", "model"]).agg(s=("split_seconds", "mean"), mem=("peak_rss_mb", "mean")).reset_index()
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.4))
    models = ["en", "logit", "gp", "gbr", "rf", "cnn"]
    for ax, col, lab in [(axs[0], "s", "Seconds per split (fit all checkpoints, calibrate, decide)"), (axs[1], "mem", "Peak resident memory (MB)")]:
        x = np.arange(len(models))
        for off, ds, c in [(-0.2, "matr_clo", BLUE), (0.2, "hust", ORANGE)]:
            v = d[d.dataset == ds].set_index("model").reindex(models)[col]
            ax.bar(x + off, v, 0.38, color=c, label=DS[ds][0])
        ax.set_xticks(x); ax.set_xticklabels(models); ax.set_ylabel(lab, fontsize=7)
        if col == "s":
            ax.set_yscale("log")
        ax.legend(fontsize=7)
    fig.tight_layout(); _save(fig, cfg, "Fig14_compute")


def run(cfg, log):
    for f in [fig_workflow, fig_lifetimes, fig_accuracy, fig_validity_efficiency, fig_decision_time, fig_trajectories,
              fig_ablation, fig_robustness, fig_shift, fig_errors, fig_confusion, fig_roc_pr, fig_compute]:
        try:
            f(cfg); log.info(f"figure {f.__name__} ok")
        except Exception as e:  # report, never hide
            log.error(f"figure {f.__name__} FAILED: {e!r}")
            raise
