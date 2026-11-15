"""Loader for the MIT/Stanford/TRI fast-charging dataset (data.matr.io/1).

Batches 2017-05-12, 2017-06-30, 2018-04-12 are the 124-cell dataset of
Severson et al., Nature Energy 4, 383-391 (2019), doi:10.1038/s41560-019-0356-8.
Batch 2019-01-24 contains the 45 CLO validation cells of Attia et al., Nature 578,
397-402 (2020), doi:10.1038/s41586-020-1994-5.

Cleaning follows the authors' public loading script and was re-verified on the data
(see ``verify_cleaning``):
* batch 1 cells 8, 10, 12, 13, 22 never reached 80% of nominal capacity -> removed;
* batch 1 cells 0-4 continued cycling in batch 2 (cells 7, 8, 9, 15, 16): their
  summary arrays are concatenated and the continuation cells removed from batch 2;
* batch 3 cells 2, 23, 32, 37, 42, 43 are noisy/incomplete channels -> removed.
Cycle numbering: summary index j <-> cycle j+1; ``cycles`` index j <-> cycle j+1.
Lifetime label = dataset field ``cycle_life`` (+ continuation length for merged cells).
"""
from __future__ import annotations
import numpy as np
import h5py

BATCH_FILES = {
    "b1": "MATR_batch_20170512.mat",
    "b2": "MATR_batch_20170630.mat",
    "b3": "MATR_batch_20180412.mat",
    "b4": "MATR_batch_20190124.mat",  # CLO (Attia et al. 2020)
}
REMOVE = {"b1": [8, 10, 12, 13, 22], "b2": [7, 8, 9, 15, 16], "b3": [2, 23, 32, 37, 42, 43], "b4": []}
CONTINUATION = {0: 7, 1: 8, 2: 9, 3: 15, 4: 16}  # b1 cell -> b2 continuation cell
SUMMARY_KEYS = ["QDischarge", "QCharge", "IR", "Tavg", "Tmax", "Tmin", "chargetime"]


def _str(f, ref):
    return "".join(chr(int(x)) for x in f[ref][()].ravel())


def _summary(f, ref):
    g = f[ref]
    return {k: np.asarray(g[k][0, :], dtype=np.float64) for k in SUMMARY_KEYS}


def _cycle_life(f, ref):
    a = f[ref][()].ravel()
    return float(a[0]) if a.size else np.nan


def load_matr(raw_dir: str, max_cycle: int = 300, batches=("b1", "b2", "b3", "b4")):
    """Return list of cell dicts with merged summaries and Qdlin for cycles 1..max_cycle."""
    files = {b: h5py.File(f"{raw_dir}/{BATCH_FILES[b]}", "r") for b in batches}
    b2_cont = {}
    if "b1" in batches and "b2" in batches:
        f2 = files["b2"]["batch"]
        for b1i, b2i in CONTINUATION.items():
            b2_cont[b1i] = (_summary(files["b2"], f2["summary"][b2i, 0]), _cycle_life(files["b2"], f2["cycle_life"][b2i, 0]))
    cells = []
    for b in batches:
        f = files[b]; B = f["batch"]
        for i in range(B["summary"].shape[0]):
            if i in REMOVE[b]:
                continue
            summ = _summary(f, B["summary"][i, 0])
            life = _cycle_life(f, B["cycle_life"][i, 0])
            if b == "b1" and i in b2_cont:
                s2, l2 = b2_cont[i]
                summ = {k: np.concatenate([summ[k], s2[k]]) for k in SUMMARY_KEYS}
                life = life + l2 - 1  # field = n_cycles + 1 in both files; see verify_cleaning
            cyc = f[B["cycles"][i, 0]]
            n_avail = cyc["Qdlin"].shape[0]
            K = min(max_cycle, n_avail)
            qdlin = np.full((max_cycle, 1000), np.nan, dtype=np.float32)
            for j in range(K):
                arr = np.asarray(f[cyc["Qdlin"][j, 0]][()], dtype=np.float32).ravel()
                if arr.size == 1000:  # a few placeholder cycles hold 2-element empty arrays
                    qdlin[j] = arr
            cells.append(dict(cell_id=f"{b}c{i}", dataset="MATR" if b != "b4" else "CLO", batch=b,
                              policy=_str(f, B["policy_readable"][i, 0]), lifetime=life,
                              summary=summ, qdlin=qdlin))
    vdlin = np.asarray(files[batches[0]]["batch"]["Vdlin"][()]).ravel() if "Vdlin" in files[batches[0]]["batch"] else None
    if vdlin is None or vdlin.size != 1000:
        vdlin = np.linspace(3.6, 2.0, 1000)
    for f in files.values():
        f.close()
    return cells, vdlin


def verify_cleaning(cells):
    """Sanity checks used in the data audit (raises AssertionError on failure)."""
    ids = [c["cell_id"] for c in cells]
    assert len(ids) == len(set(ids))
    n = {d: sum(c["dataset"] == d for c in cells) for d in ("MATR", "CLO")}
    assert n["MATR"] == 124, n
    assert n["CLO"] == 45, n
    for c in cells:
        q = c["summary"]["QDischarge"]
        assert np.isfinite(c["lifetime"]) and c["lifetime"] > 100
        # some batch-2 cells were cycled beyond end of life, so records may be longer
        assert c["lifetime"] <= len(q) + 2, (c["cell_id"], len(q), c["lifetime"])
    return n
