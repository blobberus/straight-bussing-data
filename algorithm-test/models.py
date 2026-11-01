"""Learned models (registered into predictors.REGISTRY on import). Each predicts the residual (real arrival - Passio's
time, seconds) and returns Passio's time + that residual."""
import numpy as np

import features as F
import scoring as S
from predictors import Predictor, register

BIN_MID = {b[2]: b[3] for b in S.GOAL_BINS}
PBIN_MID = {"p0-10": 300.0, "p10-15": 750.0, "p15-20": 1050.0, "p20-30": 1500.0, "p30+": 2250.0, "p?": 750.0}


def best_window(y, tol, late):
    """The correction c (s) that puts the most residuals y inside band B for this lead: a prediction passio + c passes
    when -tol <= c - y <= late, i.e. y in [c - late, c + tol]. Densest window of width tol + late. Ties: nearest 0."""
    v = np.sort(np.asarray(y, float))
    if not len(v):
        return 0.0
    w = tol + late
    j = np.searchsorted(v, v + w, side="right")
    cnt = j - np.arange(len(v))
    best = cnt.max()
    cands = v[cnt == best] + late          # left edge y = c - late  ->  c = y + late
    return float(cands[np.argmin(np.abs(cands))])


@register
class ShiftWindow(Predictor):
    """Individual algorithm v1: a learned correction per (route, stop, trip type, lead bin), chosen on earlier days to put
    the most predictions inside band B; groups with fewer than MIN samples back off to (route, trip type, bin), then
    (trip type, bin), then (bin)."""
    name = "shift_window"
    MIN = 30

    def _levels(self, f):
        nt = f["next_trip"].fillna(0).astype(int).astype(str)
        return [f["stop_key"] + "|" + nt + "|" + f["pbin"], f["route_id"] + "|" + nt + "|" + f["pbin"], nt + "|" + f["pbin"], f["pbin"]]

    def fit(self, train):
        f, y = F.frame(train), F.target(train)
        lead = f["pbin"].map(PBIN_MID).to_numpy(float)      # Passio's predicted lead (known), never the true lead
        tol, late = S.shrink_tol(lead), 0.01 * lead
        ok = ~S.gross(-y, lead)                      # gross misses do not steer the correction
        self.tables = []
        idx = np.flatnonzero(ok)
        for key in self._levels(f):
            tab = {}
            groups = key.iloc[idx].groupby(key.iloc[idx].to_numpy()).indices   # group -> positions within idx
            for g, pos in groups.items():
                if len(pos) >= self.MIN:
                    rows = idx[pos]
                    tab[g] = best_window(y[rows], tol[rows][0], late[rows][0])
            self.tables.append(tab)
        return self

    def predict(self, test):
        f = F.frame(test)
        c = np.full(len(test), np.nan)
        for key, tab in zip(self._levels(f), self.tables):   # most specific level first; fill only what is still open
            v = key.map(tab).to_numpy(float)
            c = np.where(np.isnan(c), v, c)
        return test["passio_epoch"].to_numpy(float) + np.nan_to_num(c, nan=0.0)


def target_encode(train_key, y, m=50):
    """Mean residual per category, shrunk toward the overall mean with m pseudo-samples (rare stops stay near it)."""
    import pandas as pd
    g = pd.DataFrame({"k": train_key.to_numpy(), "y": y}).groupby("k")["y"].agg(["sum", "count"])
    mu = float(np.mean(y))
    return ((g["sum"] + m * mu) / (g["count"] + m)).to_dict(), mu


class GBMQuantile(Predictor):
    """Individual algorithm v2: gradient-boosted trees predicting a quantile (TAU) of the residual from the features
    known at the query minute (features.py), route and stop as target-encoded lateness, the lead bin as its sample
    point is NOT used (it would leak the true lead); Passio's predicted lead is. A lower TAU keeps too-late predictions rare (about TAU of them land too late); a higher TAU chases band B."""
    TAU = 0.15
    ROUNDS = 120

    def _matrix(self, test):
        from gbm import QuantileGBM  # noqa: F401
        f = F.frame(test)
        X = f[F.NUMERIC].to_numpy(float)
        te_r = f["route_id"].map(self.enc_route).fillna(self.mu).to_numpy(float)
        te_s = f["stop_key"].map(self.enc_stop).fillna(self.mu).to_numpy(float)
        return np.column_stack([X, te_r, te_s])   # no lead-bin feature: it comes from the true lead (a leak)

    def fit(self, train):
        from gbm import QuantileGBM
        f, y = F.frame(train), F.target(train)
        lead = f["lead_passio"].to_numpy(float)
        ok = ~S.gross(-y, np.maximum(lead, 60.0))
        self.enc_route, self.mu = target_encode(f["route_id"][ok], y[ok])
        self.enc_stop, _ = target_encode(f["stop_key"][ok], y[ok])
        X = self._matrix(train)
        self.model = QuantileGBM(tau=self.TAU, rounds=self.ROUNDS).fit(X[ok], y[ok])
        return self

    def predict(self, test):
        return test["passio_epoch"].to_numpy(float) + self.model.predict(self._matrix(test))


@register
class GBMQ15(GBMQuantile):
    name = "gbm_q15"
    TAU = 0.15


@register
class GBMQ30(GBMQuantile):
    name = "gbm_q30"
    TAU = 0.30

# the deep-learning comparison registers itself too
import model_deep  # noqa: E402,F401
