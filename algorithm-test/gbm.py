"""A small histogram gradient-boosted tree model for quantiles, numpy only (no scikit-learn / LightGBM here).

Loss: pinball at quantile tau. Each round fits a depth-limited tree to the negative gradient (tau where y > f, tau - 1
where y < f) by least squares on histogram bins, then sets each leaf to the tau-quantile of the current residuals in it
(the leaf renewal LightGBM uses for quantile objectives), times the learning rate. Missing values get their own bin.
"""
import numpy as np


class QuantileGBM:
    def __init__(self, tau=0.5, rounds=120, lr=0.1, depth=4, min_leaf=60, bins=48, subsample=0.8, seed=7):
        self.tau, self.rounds, self.lr, self.depth = tau, rounds, lr, depth
        self.min_leaf, self.nbins, self.subsample, self.seed = min_leaf, bins, subsample, seed

    # ------------------------------------------------------------ binning
    def _fit_bins(self, X):
        self.edges = []
        for j in range(X.shape[1]):
            col = X[:, j]
            col = col[~np.isnan(col)]
            if len(col) == 0:
                self.edges.append(np.array([]))
                continue
            qs = np.unique(np.quantile(col, np.linspace(0, 1, self.nbins + 1)[1:-1]))
            self.edges.append(qs)

    def _bin(self, X):
        B = np.zeros(X.shape, dtype=np.int32)          # 0 = missing, 1.. = value bins
        for j, e in enumerate(self.edges):
            col = X[:, j]
            nan = np.isnan(col)
            B[:, j] = np.where(nan, 0, np.searchsorted(e, np.nan_to_num(col), side="right") + 1)
        return B

    # ------------------------------------------------------------ trees
    def _grow(self, B, g, rows, depth):
        """-> nested tuple tree: ("leaf", rows) or ("split", feature, bin_threshold, left, right)."""
        if depth == self.depth or len(rows) < 2 * self.min_leaf:
            return ("leaf", rows)
        gs, n = g[rows], len(rows)
        tot = gs.sum()
        best = (0.0, None, None)
        nb = self.nbins + 2
        for j in range(B.shape[1]):
            b = B[rows, j]
            sg = np.bincount(b, weights=gs, minlength=nb)
            sc = np.bincount(b, minlength=nb).astype(float)
            cg, cc = np.cumsum(sg)[:-1], np.cumsum(sc)[:-1]
            ok = (cc >= self.min_leaf) & (n - cc >= self.min_leaf)
            if not ok.any():
                continue
            gain = np.where(ok, cg ** 2 / np.maximum(cc, 1) + (tot - cg) ** 2 / np.maximum(n - cc, 1) - tot ** 2 / n, -1)
            k = int(np.argmax(gain))
            if gain[k] > best[0]:
                best = (float(gain[k]), j, k)
        if best[1] is None:
            return ("leaf", rows)
        _, j, k = best
        left = rows[B[rows, j] <= k]
        right = rows[B[rows, j] > k]
        return ("split", j, k, self._grow(B, g, left, depth + 1), self._grow(B, g, right, depth + 1))

    def _leaves(self, tree, resid):
        if tree[0] == "leaf":
            rows = tree[1]
            return ("leaf", float(np.quantile(resid[rows], self.tau)) * self.lr if len(rows) else 0.0)
        return ("split", tree[1], tree[2], self._leaves(tree[3], resid), self._leaves(tree[4], resid))

    def _apply(self, tree, B):
        out = np.empty(len(B))
        stack = [(tree, np.arange(len(B)))]
        while stack:
            t, rows = stack.pop()
            if t[0] == "leaf":
                out[rows] = t[1]
                continue
            m = B[rows, t[1]] <= t[2]
            stack.append((t[3], rows[m]))
            stack.append((t[4], rows[~m]))
        return out

    # ------------------------------------------------------------ api
    def fit(self, X, y):
        X, y = np.asarray(X, float), np.asarray(y, float)
        self._fit_bins(X)
        B = self._bin(X)
        rng = np.random.default_rng(self.seed)
        self.base = float(np.quantile(y, self.tau))
        f = np.full(len(y), self.base)
        self.trees = []
        for _ in range(self.rounds):
            rows = np.flatnonzero(rng.random(len(y)) < self.subsample)
            g = np.where(y > f, self.tau, self.tau - 1.0)
            t = self._leaves(self._grow(B, g, rows, 0), y - f)
            f += self._apply(t, B)
            self.trees.append(t)
        return self

    def predict(self, X):
        B = self._bin(np.asarray(X, float))
        f = np.full(len(B), self.base)
        for t in self.trees:
            f += self._apply(t, B)
        return f

    def importance(self):
        """How often each feature splits (a rough importance)."""
        cnt = {}
        def walk(t):
            if t[0] == "split":
                cnt[t[1]] = cnt.get(t[1], 0) + 1
                walk(t[3]); walk(t[4])
        for t in self.trees:
            walk(t)
        return cnt
