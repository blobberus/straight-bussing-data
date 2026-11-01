#!/usr/bin/env python3
"""Learning curve: does more training data help? For each of the last 5 test days, fit each model on only the last K
earlier days (K = 3, 6, 9, all) and score band B against the goal. Steady gains with K = keep collecting data first.

  python algorithm-test/learning_curve.py [--models gbm_q15,deep_q15] [--out results/06-learning-curve]
"""
import argparse, sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dataset as D       # noqa: E402
import evaluate as E      # noqa: E402
import models             # noqa: E402,F401
import predictors as P    # noqa: E402
import scoring as S       # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--models", default="gbm_q15,deep_q15")
    ap.add_argument("--out", default="results/06-learning-curve")
    a = ap.parse_args(argv)
    sample, train_all = D.load_all(), D.load_train_all()
    days = sorted(sample["service_day"].unique())
    test_days = days[-5:]
    names = [n.strip() for n in a.models.split(",")]
    rows = []
    for k in (3, 6, 9, None):
        parts = []
        for d in test_days:
            earlier = [x for x in days if x < d]
            keep = set(earlier if k is None else earlier[-k:])
            tr = train_all[train_all["service_day"].isin(keep)]
            parts.append(E.run([P.REGISTRY[n] for n in names], sample[sample["service_day"] == d], [d], tr, log=lambda *_: None))
        df = pd.concat(parts, ignore_index=True)
        for n in names + ["passio"]:
            col = "pred_" + n if n != "passio" else "passio_epoch"
            for b in ("0-10", "10-15", "20-30"):
                g = df[df["bin"] == b]
                s = S.score((g[col] - g["actual_epoch"]).to_numpy(), g["lead_s"].to_numpy())
                rows.append((n, "all" if k is None else str(k), b, s["band_b"], s["too_late"]))
        print(f"K={k}: done", file=sys.stderr)
    lines = ["# Learning curve: band B by number of training days", "",
             f"Test days {test_days[0]} to {test_days[-1]}; each model fitted on only the last K earlier days.", "",
             "| model | training days | 0-10 min band B | 10-15 min band B | 20-30 min band B | too late (0-10 / 10-15 / 20-30) |",
             "|---|---|---:|---:|---:|---|"]
    tab = {}
    for n, k, b, bb, tl in rows:
        tab.setdefault((n, k), {})[b] = (bb, tl)
    for (n, k), v in tab.items():
        if n == "passio" and k != "3":
            continue
        lab = "(no training)" if n == "passio" else k
        lines.append(f"| {n} | {lab} | " + " | ".join(f"{100 * v[b][0]:.1f}%" for b in ("0-10", "10-15", "20-30")) + " | "
                     + " / ".join(f"{100 * v[b][1]:.1f}%" for b in ("0-10", "10-15", "20-30")) + " |")
    md = "\n".join(lines) + "\n"
    print(md)
    (HERE / a.out).with_suffix(".md").write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()
