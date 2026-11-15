"""Loader for the HUST LFP dataset: Ma et al., "Real-time personalized health status
prediction of lithium-ion batteries using deep transfer learning", Energy Environ.
Sci. 15, 4083-4094 (2022), doi:10.1039/D2EE01676A; data: Mendeley Data
doi:10.17632/nsc7hnsg4s.2 (77 A123 APR18650M1A cells, 1.1 Ah, identical 5C-1C CC-CV
charging and 77 different multi-stage discharge protocols).

Each pickle holds {cell_id: {"rul": {cycle: remaining}, "dq": {cycle: Qd in mAh},
"data": {cycle: DataFrame}}}. Records stop when discharge capacity reaches 0.88 Ah
(80% of nominal), the same end-of-life convention as the MATR data; the lifetime
label is the number of recorded cycles (== rul at cycle 1).
Discharge curves are represented as V(q) on a fixed grid of discharged capacity q.
"""
from __future__ import annotations
import glob
import os
import numpy as np
from .safe_pickle import safe_load

Q_GRID = np.linspace(0.02, 0.85, 400)  # Ah, inside the range of every pre-EOL cycle


def _vq_curve(df):
    m = df["Status"].astype(str).str.contains("discharge").values
    g = df[m]
    cap = g["Capacity (mAh)"].values / 1000.0
    v = g["Voltage (V)"].values
    q = cap.max() - cap  # discharged capacity, monotone non-decreasing
    order = np.argsort(q, kind="stable")
    q, v = q[order], v[order]
    q, idx = np.unique(q, return_index=True)
    v = v[idx]
    if q.size < 10 or q.max() < Q_GRID[-1]:
        return np.full(Q_GRID.size, np.nan, dtype=np.float32)
    return np.interp(Q_GRID, q, v).astype(np.float32)


def load_hust(extracted_dir: str, curve_cycles):
    """curve_cycles: iterable of cycle numbers at which V(q) curves are stored."""
    cells = []
    curve_cycles = sorted(set(int(c) for c in curve_cycles))
    for fn in sorted(glob.glob(os.path.join(extracted_dir, "*.pkl"))):
        cid = os.path.splitext(os.path.basename(fn))[0]
        d = safe_load(fn)[cid]
        ks = sorted(d["data"].keys())
        qd = np.array([float(d["dq"][k]) / 1000.0 for k in ks])
        life = float(d["rul"][ks[0]])
        assert ks[0] == 1 and len(ks) == int(life), (cid, ks[0], len(ks), life)
        curves = np.full((len(curve_cycles), Q_GRID.size), np.nan, dtype=np.float32)
        for j, c in enumerate(curve_cycles):
            if c in d["data"]:
                curves[j] = _vq_curve(d["data"][c])
        # charge time and mean discharge voltage per cycle are cheap extra signals
        cells.append(dict(cell_id=f"HUST_{cid}", dataset="HUST", batch="HUST", policy=cid,
                          lifetime=life, summary={"QDischarge": qd}, vq=curves,
                          vq_cycles=np.array(curve_cycles)))
    return cells
