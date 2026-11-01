"""Learned models (registered into predictors.REGISTRY on import). Each predicts the residual (real arrival - Passio's
time, seconds) and returns Passio's time + that residual."""
import numpy as np

import features as F
import scoring as S
from predictors import Predictor, register

BIN_MID = {b[2]: b[3] for b in S.GOAL_BINS}


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
        return [f["stop_key"] + "|" + nt + "|" + f["bin"], f["route_id"] + "|" + nt + "|" + f["bin"], nt + "|" + f["bin"], f["bin"]]

    def fit(self, train):
        f, y = F.frame(train), F.target(train)
        lead = f["bin"].map(BIN_MID).to_numpy(float)
        tol, late = S.shrink_tol(lead), 0.01 * lead
        ok = ~S.gross(-y, lead)                      # gross misses do not steer the correction
        self.tables = []
        for key in self._levels(f):
            tab = {}
            k = key.to_numpy()
            for g in np.unique(k[ok]):
                m = ok & (k == g)
                if m.sum() >= self.MIN:
                    tab[g] = best_window(y[m], tol[m][0], late[m][0])
            self.tables.append(tab)
        return self

    def predict(self, test):
        f = F.frame(test)
        keys = [k.to_numpy() for k in self._levels(f)]
        c = np.zeros(len(test))
        for i in range(len(test)):
            for lvl, tab in enumerate(self.tables):
                v = tab.get(keys[lvl][i])
                if v is not None:
                    c[i] = v
                    break
        return test["passio_epoch"].to_numpy(float) + c
