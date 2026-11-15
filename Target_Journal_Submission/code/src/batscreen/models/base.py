"""Per-checkpoint base predictors. Each returns, for every cell, a prediction of
log10 lifetime (regressors) or a logit of P(T >= L*) (classifier), plus a
per-checkpoint scale used to normalise scores. Training uses only cells alive at the
checkpoint. Imputation/standardisation are fitted on training cells only."""
from __future__ import annotations
import warnings
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ElasticNetCV, LogisticRegressionCV
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel
from sklearn.model_selection import KFold, cross_val_predict
from sklearn.exceptions import ConvergenceWarning

warnings.filterwarnings("ignore", category=ConvergenceWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


def _prep():
    return [SimpleImputer(strategy="median"), StandardScaler()]


class ENModel:
    """Elastic net on log10 lifetime (Severson et al. 2019 style). Scale = out-of-fold
    RMSE from the internal CV at the selected penalty (no extra fits)."""
    kind = "regression"

    def __init__(self, seed=0):
        self.seed = seed

    def fit(self, X, y):
        en = ElasticNetCV(l1_ratio=[0.1, 0.5, 0.9, 1.0], alphas=40, cv=KFold(5, shuffle=True, random_state=self.seed),
                          max_iter=20000, random_state=self.seed)
        self.pipe = make_pipeline(*_prep(), en).fit(X, y)
        mse = en.mse_path_  # [n_l1, n_alpha, n_folds]
        li = list(en.l1_ratio).index(en.l1_ratio_)
        ai = int(np.argmin(np.abs(en.alphas_[li] - en.alpha_)))
        self.scale = float(np.sqrt(mse[li, ai].mean()))
        return self

    def predict(self, X):
        return self.pipe.predict(X), np.full(len(X), self.scale)


class _OOFScaleModel:
    kind = "regression"

    def fit(self, X, y):
        est = self._make()
        oof = cross_val_predict(make_pipeline(*_prep(), est), X, y, cv=KFold(5, shuffle=True, random_state=self.seed))
        self.scale = float(np.sqrt(np.mean((oof - y) ** 2)))
        self.pipe = make_pipeline(*_prep(), self._make()).fit(X, y)
        return self

    def predict(self, X):
        return self.pipe.predict(X), np.full(len(X), self.scale)


class GBRModel(_OOFScaleModel):
    def __init__(self, seed=0):
        self.seed = seed

    def _make(self):
        return GradientBoostingRegressor(n_estimators=300, max_depth=2, learning_rate=0.05, subsample=0.8,
                                         random_state=self.seed)


class RFModel(_OOFScaleModel):
    def __init__(self, seed=0):
        self.seed = seed

    def _make(self):
        return RandomForestRegressor(n_estimators=300, min_samples_leaf=3, max_features=0.5, random_state=self.seed, n_jobs=1)


class GPModel:
    """GP regression (ARD RBF + white noise); returns posterior mean and std per cell."""
    kind = "regression"

    def __init__(self, seed=0):
        self.seed = seed

    def fit(self, X, y):
        p = X.shape[1]
        k = ConstantKernel(1.0, (1e-3, 1e2)) * RBF(np.ones(p), (1e-2, 1e3)) + WhiteKernel(1e-2, (1e-5, 1))
        gp = GaussianProcessRegressor(kernel=k, normalize_y=True, n_restarts_optimizer=1, random_state=self.seed)
        self.pipe = make_pipeline(*_prep(), gp).fit(X, y)
        return self

    def predict(self, X):
        Xt = self.pipe[:-1].transform(X)
        mu, sd = self.pipe[-1].predict(Xt, return_std=True)
        return mu, np.maximum(sd, 1e-6)


class LogitModel:
    """L2 logistic regression on Z = 1{T >= L*}; needs only truncated (to L*) data.
    Score = decision function (logit); scale = 1."""
    kind = "classifier"

    def __init__(self, seed=0):
        self.seed = seed

    def fit(self, X, z):
        clf = LogisticRegressionCV(Cs=10, cv=KFold(5, shuffle=True, random_state=self.seed), max_iter=5000)
        self.pipe = make_pipeline(*_prep(), clf).fit(X, z)
        return self

    def predict(self, X):
        return self.pipe.decision_function(X), np.ones(len(X))


from .cnn import CNNModel  # noqa: E402

MODELS = {"en": ENModel, "gbr": GBRModel, "rf": RFModel, "gp": GPModel, "logit": LogitModel, "cnn": CNNModel}
