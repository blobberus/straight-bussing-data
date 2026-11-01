#!/usr/bin/env python3
"""Ceiling test: how good can ANY model get with these inputs? Each model is fitted on data that includes the day it is
graded on (it sees the answers, which no real model can), two ways: on that day alone (all of its fitting is about the
graded day) and on every earlier day plus that day (more data, answers included). If even these cheating fits stay far
below the goal, a bigger or smarter model on the same inputs cannot meet it either; better inputs are needed.

  python algorithm-test/ceiling.py [--models shift_window,gbm_q30,deep_q30] [--test-days 5] [--out results/09-ceiling]
"""
import argparse, sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dataset as D       # noqa: E402
import models             # noqa: E402,F401
import predictors as P    # noqa: E402
import scoring as S       # noqa: E402

BINS = [b[2] for b in S.GOAL_BINS]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--models", default="shift_window,gbm_q30,deep_q30")
    ap.add_argument("--test-days", type=int, default=5)
    ap.add_argument("--out", default="results/09-ceiling")
    a = ap.parse_args(argv)
    sample, train_all = D.load_all(), D.load_train_all()
    days = sorted(sample["service_day"].unique())[-a.test_days:]
    names = [n.strip() for n in a.models.split(",")]
    lines = ["# Ceiling: models fitted on data that includes the day they are graded on", "",
             f"Test days {days[0]} to {days[-1]}. Every model here has seen the answers of the day it is scored on, so these "
             "numbers are an upper bound for what the same inputs can give, not a result. shift_window picks its "
             "corrections to put the most predictions inside band B directly; the q30 models aim at the 30% quantile.", ""]
    for label, pick in (("the graded day alone", lambda tr, d: tr[tr["service_day"] == d]),
                        ("every earlier day plus the graded day", lambda tr, d: tr[tr["service_day"] <= d])):
        parts = []
        for d in days:
            test = sample[sample["service_day"] == d].copy()
            fit_rows = pick(train_all, d)
            for n in names:
                test["pred_" + n] = P.REGISTRY[n]().fit(fit_rows).predict(test)
            parts.append(test)
            print(f"{label}, {d}: done", file=sys.stderr)
        df = pd.concat(parts, ignore_index=True)
        lines += [f"## Fitted on {label}", "",
                  "| model | " + " | ".join(f"{b} min band B" for b in BINS) + " | too late (" + " / ".join(BINS) + ") |",
                  "|---|" + "---:|" * len(BINS) + "---|"]
        for n in ["passio"] + names:
            col = "passio_epoch" if n == "passio" else "pred_" + n
            sc = {b: S.score((g[col] - g["actual_epoch"]).to_numpy(), g["lead_s"].to_numpy()) for b, g in df.groupby("bin")}
            lab = "passio (no fitting, reference)" if n == "passio" else n
            lines.append(f"| {lab} | " + " | ".join(f"{100 * sc[b]['band_b']:.1f}%" for b in BINS) + " | "
                         + " / ".join(f"{100 * sc[b]['too_late']:.1f}%" for b in BINS) + " |")
        lines.append("")
    lines += ["Fitted on one day, the network gets few training steps (6 passes over about a day's rows) and is undertrained, "
              "so its first-table numbers understate it; the second table is its fair ceiling.", "",
              f"Goal: {100 * S.MOST:.0f}% band B in every bin."]
    md = "\n".join(lines) + "\n"
    print(md)
    (HERE / a.out).with_suffix(".md").write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()
