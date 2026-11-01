"""Deep-learning comparison: a PyTorch network on the same inputs and target as the boosted trees.

Inputs: the 18 numeric features (standardized; missing -> 0 plus a missing flag per feature) and learned embeddings for
route (4), stop (8) and Passio's lead bin (3). Network: 3 hidden layers (128, 128, 64), ReLU, dropout 0.1. Loss:
pinball at TAU on the residual in minutes. Adam, 6 epochs, batch 2048, fixed seed. CPU only.
"""
import numpy as np
import torch
from torch import nn

import features as F
import scoring as S
from predictors import Predictor, register


class Net(nn.Module):
    def __init__(self, n_num, n_route, n_stop, n_pbin):
        super().__init__()
        self.er, self.es, self.ep = nn.Embedding(n_route, 4), nn.Embedding(n_stop, 8), nn.Embedding(n_pbin, 3)
        self.mlp = nn.Sequential(nn.Linear(2 * n_num + 15, 128), nn.ReLU(), nn.Dropout(0.1),
                                 nn.Linear(128, 128), nn.ReLU(), nn.Dropout(0.1),
                                 nn.Linear(128, 64), nn.ReLU(), nn.Linear(64, 1))

    def forward(self, x, r, s, p):
        return self.mlp(torch.cat([x, self.er(r), self.es(s), self.ep(p)], dim=1)).squeeze(1)


class DeepQuantile(Predictor):
    TAU = 0.15
    EPOCHS = 6

    def _index(self, keys, vocab):
        return torch.tensor([vocab.get(k, 0) for k in keys], dtype=torch.long)

    def _inputs(self, f):
        X = f[F.NUMERIC].to_numpy(float)
        miss = np.isnan(X).astype(np.float32)
        Z = np.nan_to_num((X - self.mu) / self.sd).astype(np.float32)
        x = torch.tensor(np.hstack([Z, miss]))
        return x, self._index(f["route_id"], self.vr), self._index(f["stop_key"], self.vs), self._index(f["pbin"], self.vp)

    def fit(self, train):
        torch.manual_seed(7)
        np.random.seed(7)
        f, y = F.frame(train), F.target(train)
        ok = ~S.gross(-y, np.maximum(f["lead_passio"].to_numpy(float), 60.0))
        f, y = f[ok], y[ok] / 60.0
        X = f[F.NUMERIC].to_numpy(float)
        self.mu, self.sd = np.nanmean(X, axis=0), np.nanstd(X, axis=0) + 1e-6
        self.mu, self.sd = np.nan_to_num(self.mu), np.where(np.isnan(self.sd), 1.0, self.sd)
        self.vr = {k: i + 1 for i, k in enumerate(sorted(f["route_id"].unique()))}
        self.vs = {k: i + 1 for i, k in enumerate(sorted(f["stop_key"].unique()))}
        self.vp = {k: i + 1 for i, k in enumerate(sorted(f["pbin"].unique()))}
        x, r, s, p = self._inputs(f)
        t = torch.tensor(y, dtype=torch.float32)
        self.net = Net(len(F.NUMERIC), len(self.vr) + 1, len(self.vs) + 1, len(self.vp) + 1)
        opt = torch.optim.Adam(self.net.parameters(), lr=1e-3)
        n, tau = len(t), self.TAU
        self.net.train()
        for _ in range(self.EPOCHS):
            perm = torch.randperm(n)
            for i in range(0, n, 2048):
                b = perm[i:i + 2048]
                d = t[b] - self.net(x[b], r[b], s[b], p[b])
                loss = torch.mean(torch.maximum(tau * d, (tau - 1) * d))   # pinball
                opt.zero_grad()
                loss.backward()
                opt.step()
        return self

    def predict(self, test):
        self.net.eval()
        with torch.no_grad():
            out = self.net(*self._inputs(F.frame(test))).numpy() * 60.0
        return test["passio_epoch"].to_numpy(float) + out


@register
class DeepQ15(DeepQuantile):
    name = "deep_q15"
    TAU = 0.15


@register
class DeepQ30(DeepQuantile):
    name = "deep_q30"
    TAU = 0.30
