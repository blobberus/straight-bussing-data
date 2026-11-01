#!/usr/bin/env python3
"""Tests for gbm.py on synthetic data: python algorithm-test/test_gbm.py"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gbm import QuantileGBM  # noqa: E402

tests = []
test = tests.append


def data(n=6000, seed=1):
    rng = np.random.default_rng(seed)
    X = rng.uniform(0, 10, (n, 3))
    X[rng.random(n) < 0.1, 2] = np.nan                  # some missing values
    y = np.where(X[:, 0] > 5, 300.0, 60.0) + rng.normal(0, 30, n)   # a step in feature 0, noise elsewhere
    return X, y


@test
def learns_the_step_and_ignores_noise_features():
    X, y = data()
    m = QuantileGBM(tau=0.5, rounds=60).fit(X, y)
    p = m.predict(np.array([[2.0, 5.0, 5.0], [8.0, 5.0, np.nan]]))
    assert abs(p[0] - 60) < 15 and abs(p[1] - 300) < 15, p
    imp = m.importance()
    assert imp.get(0, 0) > imp.get(1, 0) and imp.get(0, 0) > imp.get(2, 0), imp


@test
def quantile_tau_is_respected():
    X, y = data(seed=2)
    for tau in (0.1, 0.5, 0.9):
        m = QuantileGBM(tau=tau, rounds=80).fit(X, y)
        share = float(np.mean(y < m.predict(X)))
        assert abs(share - tau) < 0.04, (tau, share)


if __name__ == "__main__":
    bad = 0
    for t in tests:
        try:
            t()
            print("pass", t.__name__)
        except AssertionError as e:
            bad += 1
            print("FAIL", t.__name__, e)
    print("ok" if not bad else "FAILED", f"{len(tests) - bad}/{len(tests)}")
    sys.exit(1 if bad else 0)
