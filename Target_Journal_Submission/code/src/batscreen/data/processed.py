"""Load the stage-1 caches written by scripts/preprocess.py."""
import numpy as np


def load_processed(path):
    z = np.load(path, allow_pickle=True)  # object arrays written by our own preprocess step
    arrs = {k: z[k] for k in z.files}      # decompress each member exactly once
    n = len(arrs["cell_id"])
    cells = []
    for i in range(n):
        c = {k: str(arrs[k][i]) for k in ("cell_id", "dataset", "batch", "policy")}
        c["lifetime"] = float(arrs["lifetime"][i])
        for key in arrs:
            if key.startswith("summary_"):
                c[key] = np.asarray(arrs[key][i], dtype=float)
        if "qdlin" in arrs:
            c["qdlin"] = arrs["qdlin"][i]
        if "vq" in arrs:
            c["vq"] = arrs["vq"][i]; c["vq_cycles"] = arrs["vq_cycles"]
        cells.append(c)
    return cells
