"""Small 1-D CNN baseline on the dQ(V) / dV(q) difference curve plus scalar features.
Input columns: first `n_curve` columns = curve, rest = scalar features.
Scale = RMSE on a 20% validation part of the training cells (also used for early
stopping); the model is not refitted on the validation part."""
from __future__ import annotations
import numpy as np


class CNNModel:
    kind = "regression"
    n_curve = 100

    def __init__(self, seed=0, epochs=400, lr=3e-3, wd=1e-3, patience=60):
        self.seed, self.epochs, self.lr, self.wd, self.patience = seed, epochs, lr, wd, patience

    def _net(self, p):
        import torch.nn as nn
        import torch

        class Net(nn.Module):
            def __init__(s):
                super().__init__()
                s.conv = nn.Sequential(nn.Conv1d(1, 8, 5, padding=2), nn.ReLU(), nn.MaxPool1d(2),
                                       nn.Conv1d(8, 16, 5, padding=2), nn.ReLU(), nn.AdaptiveAvgPool1d(1))
                s.head = nn.Sequential(nn.Linear(16 + p, 32), nn.ReLU(), nn.Linear(32, 1))

            def forward(s, c, x):
                return s.head(torch.cat([s.conv(c.unsqueeze(1)).squeeze(-1), x], 1)).squeeze(-1)
        return Net()

    def _std(self, X, fit=False):
        c, x = X[:, :self.n_curve], X[:, self.n_curve:]
        if fit:
            self.cm, self.cs = np.nanmean(c), np.nanstd(c) + 1e-8
            self.xm, self.xs = np.nanmedian(x, 0), np.nanstd(x, 0) + 1e-8
        c = np.nan_to_num((c - self.cm) / self.cs)
        x = np.nan_to_num((x - self.xm) / self.xs)
        return c.astype(np.float32), x.astype(np.float32)

    def fit(self, X, y):
        import torch
        from ..utils import detect_device
        torch.manual_seed(self.seed); torch.set_num_threads(1)
        dev = detect_device()
        rng = np.random.default_rng(self.seed); idx = rng.permutation(len(y)); nv = max(4, int(0.2 * len(y)))
        va, tr = idx[:nv], idx[nv:]
        c, x = self._std(X[tr], fit=True); cv, xv = self._std(X[va])
        self.ym, self.ys = y[tr].mean(), y[tr].std() + 1e-8
        T = lambda a: torch.tensor(a, device=dev)
        net = self._net(x.shape[1]).to(dev)
        opt = torch.optim.Adam(net.parameters(), lr=self.lr, weight_decay=self.wd)
        yt = T(((y[tr] - self.ym) / self.ys).astype(np.float32))
        best, best_state, wait = np.inf, None, 0
        for ep in range(self.epochs):
            net.train(); opt.zero_grad()
            loss = ((net(T(c), T(x)) - yt) ** 2).mean(); loss.backward(); opt.step()
            net.eval()
            with torch.no_grad():
                pv = net(T(cv), T(xv)).cpu().numpy() * self.ys + self.ym
            v = float(np.sqrt(np.mean((pv - y[va]) ** 2)))
            if v < best - 1e-6:
                best, wait = v, 0; best_state = {k: t.clone() for k, t in net.state_dict().items()}
            else:
                wait += 1
                if wait > self.patience:
                    break
        net.load_state_dict(best_state); self.net, self.dev, self.scale = net, dev, best
        return self

    def predict(self, X):
        import torch
        c, x = self._std(X)
        with torch.no_grad():
            p = self.net(torch.tensor(c, device=self.dev), torch.tensor(x, device=self.dev)).cpu().numpy()
        return p * self.ys + self.ym, np.full(len(X), self.scale)
