"""Reproduce the full study.

    python run_all.py --mode quick     # pipeline check (minutes)
    python run_all.py --mode full      # all experiments reported in the paper (~2-3 h on 4 CPU cores)

Stages: data (download/preprocess if needed) -> features -> experiments E1-E7 ->
analysis (statistics, tables, E8 error analysis) -> figures. Use --stages to run a
subset, e.g. --stages analysis figures. Results go to ../results, ../tables, ../figures.
In quick mode outputs go to ../results_quick etc. so that full results are never
overwritten by a pipeline check.
"""
import argparse, json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "src")); sys.path.insert(0, os.path.join(HERE, "experiments"))
os.chdir(HERE)
from batscreen.utils import load_config, get_logger, environment_info, set_seed

ap = argparse.ArgumentParser()
ap.add_argument("--mode", choices=["quick", "full"], default="quick")
ap.add_argument("--stages", nargs="*", default=["data", "features", "experiments", "analysis", "figures"])
ap.add_argument("--experiments", nargs="*", default=["E1", "E2", "E3", "E4", "E5", "E6", "E7"])
ap.add_argument("--force", action="store_true", help="recompute experiments whose outputs already exist")
a = ap.parse_args()
cfg = load_config(f"config/{'default' if a.mode == 'full' else 'quick'}.yaml")
if a.mode == "quick":
    for k in ("results", "figures", "tables"):
        cfg["paths"][k] = cfg["paths"][k] + "_quick"
cfg["force"] = a.force
if cfg["n_jobs"] == -1:
    cfg["n_jobs"] = os.cpu_count()
for k in ("results", "figures", "tables"):
    os.makedirs(cfg["paths"][k], exist_ok=True)
log = get_logger("run_all", os.path.join(cfg["paths"]["results"], "experiment_logs", f"run_{a.mode}_{time.strftime('%Y%m%d_%H%M%S')}.log"))
log.info(f"mode={a.mode} stages={a.stages} env={json.dumps(environment_info())}")
set_seed(cfg["seed_base"])
json.dump(dict(mode=a.mode, config=cfg, environment=environment_info()),
          open(os.path.join(cfg["paths"]["results"], "run_config.json"), "w"), indent=1, default=str)

if "data" in a.stages:
    proc = cfg["paths"]["processed"]
    if not all(os.path.exists(os.path.join(proc, d["cache"])) for d in cfg["datasets"].values()):
        from batscreen.data.download import download_all
        log.info("downloading raw data (~12 GB) ..."); download_all(cfg["paths"]["raw"])
        subprocess.run([sys.executable, "scripts/preprocess.py", "--raw", cfg["paths"]["raw"], "--out", proc], check=True)
    else:
        log.info("processed caches present")
if "features" in a.stages:
    feats = [os.path.join(cfg["paths"]["features"], f"{ds}_{k}.npz") for ds, k in
             [("matr_clo", "severson"), ("matr_clo", "capacity"), ("hust", "vq"), ("hust", "capacity")]]
    if all(os.path.exists(f) for f in feats):
        log.info("feature tables present (delete data/features/*.npz to rebuild)")
    else:
        subprocess.run([sys.executable, "scripts/build_features.py", "--config", "config/default.yaml"], check=True)
if "experiments" in a.stages:
    import suite
    fns = dict(E1=suite.e1_main, E2=suite.e2_models, E3=suite.e3_ablation, E4=suite.e4_robustness,
               E5=suite.e5_shift, E6=lambda c, l: suite.e6_compute(c, l, reps=1 if a.mode == "quick" else 5),
               E7=suite.e7_sensitivity)
    for e in a.experiments:
        t = time.time(); log.info(f"--- {e} start"); fns[e](cfg, log); log.info(f"--- {e} done in {time.time()-t:.0f}s")
if "analysis" in a.stages:
    import analysis
    analysis.run(cfg, log)
if "figures" in a.stages:
    import figures
    figures.run(cfg, log)
log.info("finished")
