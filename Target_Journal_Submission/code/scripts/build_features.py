"""Stage 2: processed caches -> checkpoint feature tables (small, committed to git)."""
import argparse, json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from batscreen.utils import load_config
from batscreen.data.processed import load_processed
from batscreen.preprocessing.features import build_feature_table, build_curve_table

ap = argparse.ArgumentParser(); ap.add_argument("--config", default="config/default.yaml")
a = ap.parse_args(); cfg = load_config(a.config)
out_dir = cfg["paths"]["features"]; os.makedirs(out_dir, exist_ok=True)
for name, d in cfg["datasets"].items():
    cells = load_processed(os.path.join(cfg["paths"]["processed"], d["cache"]))
    kinds = [d["features"], "capacity"]
    for kind in kinds:
        tab = build_feature_table(cells, d["checkpoints"], kind)
        names = tab[d["checkpoints"][0]][1]
        X = np.stack([tab[k][0] for k in d["checkpoints"]], axis=1)  # [n, M, p]
        extra = {}
        if kind in ("severson", "vq"):
            extra["C"] = build_curve_table(cells, d["checkpoints"], kind)
        np.savez_compressed(os.path.join(out_dir, f"{name}_{kind}.npz"), X=X, names=np.array(names), **extra,
                            checkpoints=np.array(d["checkpoints"]),
                            cell_id=np.array([c["cell_id"] for c in cells]), dataset=np.array([c["dataset"] for c in cells]),
                            batch=np.array([c["batch"] for c in cells]), policy=np.array([c["policy"] for c in cells]),
                            lifetime=np.array([c["lifetime"] for c in cells]))
        alive = np.array([[c["lifetime"] > k for k in d["checkpoints"]] for c in cells])
        miss = np.isnan(X).any(axis=2) & alive
        print(name, kind, X.shape, "alive-but-missing rows:", int(miss.sum()), "feature NaN share among alive: %.4f" % np.isnan(X[alive]).mean())
