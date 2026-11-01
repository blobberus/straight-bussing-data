#!/usr/bin/env python3
"""Leak guard: a model's predictions must not depend on anything derived from the real arrival.

  python algorithm-test/test_leak.py

For every learned model: fit on a few training days, predict one test day twice, the second time with the goal bin,
the true lead and the real arrival scrambled in the test rows. Any difference = the model peeks at the answer.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dataset as D          # noqa: E402
import models                # noqa: E402,F401
import predictors as P       # noqa: E402

LEAKY = ["bin", "lead_s", "actual_epoch"]


def main():
    sample, train_all = D.load_all(), D.load_train_all()
    days = sorted(sample["service_day"].unique())
    d = days[-1]
    train = train_all[(train_all["service_day"] < d) & (train_all["service_day"] >= days[-4])]
    test = sample[sample["service_day"] == d].head(3000).copy()
    rng = np.random.default_rng(1)
    scrambled = test.copy()
    for c in LEAKY:
        scrambled[c] = scrambled[c].to_numpy()[rng.permutation(len(scrambled))]
    bad = 0
    for name, cls in P.REGISTRY.items():
        m = cls().fit(train)
        a, b = m.predict(test), m.predict(scrambled)
        same = np.allclose(np.nan_to_num(a), np.nan_to_num(b))
        print(("pass" if same else "LEAK"), name)
        bad += not same
    print("ok" if not bad else "FAILED", f"{len(P.REGISTRY) - bad}/{len(P.REGISTRY)} models do not peek")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
