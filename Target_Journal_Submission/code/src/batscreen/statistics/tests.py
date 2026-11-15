"""Statistical analysis of screening results.

Unit of analysis for efficiency comparisons = cell. Each cell's time to decision is
averaged over the random splits in which it was a test cell; methods are compared on
the same cells with a paired Wilcoxon signed-rank test (Holm-corrected across
comparisons), matched-pairs rank-biserial correlation as effect size and a cell-level
bootstrap CI of the difference in fractional time saved.
Validity: mean error rate over splits with a normal-approximation 95% CI (Monte-Carlo
error of the expectation) and the pooled binomial (Clopper-Pearson) interval."""
from __future__ import annotations
import numpy as np
import pandas as pd
from scipy import stats


def validity_summary(df, alpha, beta, by=("model", "method")):
    out = []
    for key, g in df.groupby(list(by)):
        r = dict(zip(by, key if isinstance(key, tuple) else (key,)))
        n = len(g)
        for e, lvl in (("fpr", alpha), ("frr", beta)):
            m, s = g[e].mean(), g[e].std(ddof=1) if n > 1 else 0.0
            r[f"{e}_mean"] = m; r[f"{e}_ci_lo"] = m - 1.96 * s / np.sqrt(n); r[f"{e}_ci_hi"] = m + 1.96 * s / np.sqrt(n)
            r[f"{e}_share_above"] = float((g[e] > lvl).mean())
        k_fp, n_b = g["false_pass"].sum(), g["n_bad"].sum()
        k_fr, n_g = g["false_reject"].sum(), g["n_good"].sum()
        r["fpr_pooled"] = k_fp / n_b; r["frr_pooled"] = k_fr / n_g
        r["fpr_pooled_cp_hi"] = stats.beta.ppf(0.975, k_fp + 1, n_b - k_fp) if k_fp < n_b else 1.0
        r["frr_pooled_cp_hi"] = stats.beta.ppf(0.975, k_fr + 1, n_g - k_fr) if k_fr < n_g else 1.0
        for c in ("accuracy", "early_rate", "time_saving", "mean_time"):
            r[f"{c}_mean"] = g[c].mean(); r[f"{c}_sd"] = g[c].std(ddof=1) if n > 1 else 0.0
        r["n_splits"] = n
        out.append(r)
    return pd.DataFrame(out)


def per_cell_times(cells_df, T, Lstar):
    """Average time-to-decision and error indicators per (method, cell)."""
    d = cells_df.copy()
    d["T"] = T[d["cell"].values]
    d["good"] = d["T"] >= Lstar
    d["false_pass"] = (d["decision"] == 1) & ~d["good"]
    d["false_reject"] = (d["decision"] == -1) & d["good"]
    d["full_cost"] = np.minimum(d["T"], Lstar)
    return d.groupby(["model", "method", "cell"]).agg(time=("time", "mean"), full_cost=("full_cost", "first"),
                                                     fp=("false_pass", "mean"), fr=("false_reject", "mean"),
                                                     early=("by_model", "mean"), n=("time", "size")).reset_index()


def holm(pvals):
    p = np.asarray(pvals, float); order = np.argsort(p); m = len(p)
    adj = np.empty(m); run = 0.0
    for r, i in enumerate(order):
        run = max(run, min(1.0, (m - r) * p[i])); adj[i] = run
    return adj


def paired_comparisons(pc, reference="proposed", n_boot=10000, seed=0):
    """Compare reference vs every other method of the same model on per-cell mean time."""
    rows = []
    rng = np.random.default_rng(seed)
    for model, g in pc.groupby("model"):
        piv = g.pivot(index="cell", columns="method", values="time")
        cost = g.groupby("cell")["full_cost"].first().reindex(piv.index).values
        if reference not in piv:
            continue
        for meth in piv.columns:
            if meth == reference:
                continue
            a, b = piv[reference].values, piv[meth].values
            ok = np.isfinite(a) & np.isfinite(b)
            a, b, c = a[ok], b[ok], cost[ok]
            d = a - b
            nz = d[d != 0]
            if nz.size == 0:
                p, rbc = 1.0, 0.0
            else:
                w = stats.wilcoxon(a, b, zero_method="wilcox")
                p = float(w.pvalue)
                ranks = stats.rankdata(np.abs(nz))
                rbc = float((ranks[nz > 0].sum() - ranks[nz < 0].sum()) / ranks.sum())
            # bootstrap CI of difference in fractional time saved (positive = reference saves more)
            sav = lambda x, cc: 1 - x.sum() / cc.sum()
            bs = []
            for _ in range(n_boot):
                i = rng.integers(0, len(a), len(a))
                bs.append(sav(a[i], c[i]) - sav(b[i], c[i]))
            rows.append(dict(model=model, reference=reference, comparator=meth, n_cells=int(len(a)),
                             mean_time_ref=a.mean(), mean_time_comp=b.mean(), median_diff=float(np.median(d)),
                             saving_diff=sav(a, c) - sav(b, c), saving_diff_ci_lo=float(np.percentile(bs, 2.5)),
                             saving_diff_ci_hi=float(np.percentile(bs, 97.5)), wilcoxon_p=p, rank_biserial=rbc))
    out = pd.DataFrame(rows)
    if len(out):
        out["p_holm"] = np.concatenate([holm(g["wilcoxon_p"].values) for _, g in out.groupby("model")]) if out["model"].nunique() == 1 else out.groupby("model")["wilcoxon_p"].transform(lambda s: holm(s.values))
    return out
