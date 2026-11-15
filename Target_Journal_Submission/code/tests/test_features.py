"""Features at checkpoint k must not depend on cycles > k (no look-ahead leakage)."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from batscreen.preprocessing.features import matr_features, capacity_features


def _fake_cell(rng, n=400):
    q = 1.07 - 0.0002 * np.arange(n) + rng.normal(0, 1e-4, n)
    qdlin = np.stack([np.linspace(1.05, 0, 1000) - 0.0001 * c + rng.normal(0, 1e-5, 1000) for c in range(n)]).astype(np.float32)
    return dict(qdlin=qdlin, summary_QDischarge=q, summary_chargetime=np.full(n, 10.0), summary_Tmax=np.full(n, 35.0), lifetime=900.0)


def test_no_lookahead():
    rng = np.random.default_rng(0)
    c = _fake_cell(rng); k = 100
    f1 = matr_features(c, k)
    c2 = {key: (v.copy() if isinstance(v, np.ndarray) else v) for key, v in c.items()}
    c2["qdlin"][k:] += 0.5; c2["summary_QDischarge"][k:] *= 0.5; c2["summary_Tmax"][k:] = 99.0  # corrupt the future
    f2 = matr_features(c2, k)
    for key in f1:
        assert np.isclose(f1[key], f2[key], equal_nan=True), key


def test_capacity_features_finite():
    rng = np.random.default_rng(1)
    f = capacity_features(_fake_cell(rng)["summary_QDischarge"], 50)
    assert all(np.isfinite(v) for v in f.values())
