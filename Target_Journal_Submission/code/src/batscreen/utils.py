"""Configuration, seeding, hardware detection and logging helpers."""
from __future__ import annotations
import json, logging, os, platform, random, re, time
import numpy as np
import yaml


def load_config(path):
    with open(path) as f:
        cfg = yaml.safe_load(f)
    if "inherit" in cfg:
        base = load_config(os.path.join(os.path.dirname(path), cfg.pop("inherit")))
        for k, v in cfg.items():
            base[k] = v
        cfg = base
    # ${VAR:-default} expansion in paths
    for k, v in cfg.get("paths", {}).items():
        m = re.match(r"\$\{(\w+):-(.*)\}", str(v))
        if m:
            cfg["paths"][k] = os.environ.get(m.group(1), m.group(2))
    return cfg


def set_seed(seed):
    random.seed(seed); np.random.seed(seed % (2**32 - 1))
    try:
        import torch
        torch.manual_seed(seed); torch.use_deterministic_algorithms(True, warn_only=True)
    except ImportError:
        pass


def detect_device():
    """CPU / CUDA / Apple-Silicon MPS detection (used only by the CNN baseline)."""
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda"
        if getattr(torch.backends, "mps", None) is not None and torch.backends.mps.is_available():
            return "mps"
    except ImportError:
        pass
    return "cpu"


def environment_info():
    import sklearn, scipy
    info = dict(python=platform.python_version(), platform=platform.platform(), numpy=np.__version__,
                scipy=scipy.__version__, sklearn=sklearn.__version__, cpu_count=os.cpu_count(), device=detect_device())
    try:
        import torch; info["torch"] = torch.__version__
    except ImportError:
        pass
    return info


def get_logger(name, logfile=None):
    log = logging.getLogger(name)
    if not log.handlers:
        log.setLevel(logging.INFO)
        fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        h = logging.StreamHandler(); h.setFormatter(fmt); log.addHandler(h)
        if logfile:
            os.makedirs(os.path.dirname(logfile), exist_ok=True)
            fh = logging.FileHandler(logfile); fh.setFormatter(fmt); log.addHandler(fh)
    return log
