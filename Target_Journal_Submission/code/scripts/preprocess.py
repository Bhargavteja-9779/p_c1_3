"""Stage 1: raw files -> compact per-cell caches (npz, outside git) + lifetimes table.
Usage: python scripts/preprocess.py --raw /path/to/raw --out /path/to/processed"""
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from batscreen.data.matr import load_matr, verify_cleaning
from batscreen.data.hust import load_hust

ap = argparse.ArgumentParser()
ap.add_argument("--raw", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--max_cycle", type=int, default=300)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
t0 = time.time()
cells, vdlin = load_matr(f"{a.raw}/MATR", max_cycle=a.max_cycle)
print("MATR/CLO counts", verify_cleaning(cells), f"{time.time()-t0:.0f}s", flush=True)
np.savez_compressed(f"{a.out}/matr_clo.npz",
    cell_id=np.array([c["cell_id"] for c in cells]), dataset=np.array([c["dataset"] for c in cells]),
    batch=np.array([c["batch"] for c in cells]), policy=np.array([c["policy"] for c in cells]),
    lifetime=np.array([c["lifetime"] for c in cells]), vdlin=vdlin,
    qdlin=np.stack([c["qdlin"] for c in cells]),
    **{f"summary_{k}": np.array([c["summary"][k] for c in cells], dtype=object) for k in cells[0]["summary"]})
hust_cycles = list(range(1, 21)) + list(range(20, 1001, 10))
hc = load_hust(f"{a.raw}/HUST/extracted/our_data", hust_cycles)
print("HUST cells", len(hc), f"{time.time()-t0:.0f}s", flush=True)
np.savez_compressed(f"{a.out}/hust.npz",
    cell_id=np.array([c["cell_id"] for c in hc]), dataset=np.array([c["dataset"] for c in hc]),
    batch=np.array([c["batch"] for c in hc]), policy=np.array([c["policy"] for c in hc]),
    lifetime=np.array([c["lifetime"] for c in hc]), vq=np.stack([c["vq"] for c in hc]),
    vq_cycles=hc[0]["vq_cycles"], summary_QDischarge=np.array([c["summary"]["QDischarge"] for c in hc], dtype=object))
life = {c["cell_id"]: c["lifetime"] for c in cells + hc}
json.dump(life, open(f"{a.out}/lifetimes.json", "w"), indent=0)
print("done", f"{time.time()-t0:.0f}s")
