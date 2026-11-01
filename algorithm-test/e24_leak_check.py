#!/usr/bin/env python3
"""Check of the main repo's E24 "headroom" table (docs/TEN-PERCENT-SHORTFALLS.md section 6), which found that a learned
constant shift lifts Passio to about 50% on the 10% rule. That shift was grouped by the goal bin and scaled by the lead,
both measured from the REAL arrival, which a rider's phone cannot know (the same leak fixed in this bench on 2026-11-01).

Two versions of the same shift, learned on earlier days only and scored on the bench's test days:
  as in E24   grouped by the true-lead bin, shift = share x the true lead, learned on the scoreboard samples
  leak-free   grouped by the bin of Passio's predicted lead, shift = share x Passio's lead, learned on every query minute
Scored with E24's measures: the 10% rule, band B as E24 read it (10% of the lead early to 1% late) and too late.

  python algorithm-test/e24_leak_check.py [--test-days 11] [--out results/10-e24-leak-check]
"""
import argparse, sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dataset as D       # noqa: E402
import features as F      # noqa: E402
import scoring as S       # noqa: E402

BINS = [b[2] for b in S.GOAL_BINS]
TARGETS = {"10% rule": (-0.10, 0.10), "band B (10% early to 1% late)": (-0.10, 0.01)}
MIN_N = 30


def best_share(rel, lo, hi):
    """The share s putting the most rel values inside [s + lo, s + hi]; ties nearest 0 (E24 best_shift)."""
    v = np.sort(rel)
    j = np.searchsorted(v, v + (hi - lo), side="right")
    cnt = j - np.arange(len(v))
    cands = v[cnt == cnt.max()] - lo
    return float(cands[np.argmin(np.abs(cands))])


def keys(df, binc):
    seg = np.where(df["next_trip"].fillna(0) == 1, "next", "cur")
    r, st, b = df["route_name"].astype(str), df["stop_id"].astype(str), df[binc].astype(str)
    return [r + "|" + st + "|" + seg + "|" + b, r + "|" + seg + "|" + b, pd.Series(seg, index=df.index) + "|" + b]


def learn(train, binc, lead, lo, hi):
    e = (train["passio_epoch"] - train["actual_epoch"]).to_numpy(float)
    ld = np.maximum(train[lead].to_numpy(float), 60.0)
    ok = ~S.gross(e, ld)
    rel = pd.Series(e / ld, index=train.index)[ok]
    tabs = []
    for k in keys(train, binc):
        k = k[ok]
        tabs.append({g: best_share(rel.loc[idx].to_numpy(), lo, hi) for g, idx in k.groupby(k).groups.items() if len(idx) >= MIN_N})
    return tabs


def apply(test, tabs, binc):
    s = np.full(len(test), np.nan)
    for k, tab in zip(keys(test, binc), tabs):
        s = np.where(np.isnan(s), k.map(tab).to_numpy(float), s)
    return np.nan_to_num(s, nan=0.0)


def measures(e, ld):
    g = S.gross(e, ld)
    k = max(int((~g).sum()), 1)
    return ((np.abs(e[~g]) <= 0.10 * ld[~g]).sum() / k, ((e[~g] >= -0.10 * ld[~g]) & (e[~g] <= 0.01 * ld[~g])).sum() / k,
            (e > 0.01 * ld).mean())


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--test-days", type=int, default=11)
    ap.add_argument("--out", default="results/10-e24-leak-check")
    a = ap.parse_args(argv)
    sample, train_all = D.load_all(), D.load_train_all()
    for df in (sample, train_all):
        f = F.frame(df)
        df["pbin"], df["lead_passio"] = f["pbin"].str[1:], f["lead_passio"]
    days = sorted(sample["service_day"].unique())
    test_days = days[-a.test_days:]
    res = {}
    for d in test_days:
        test = sample[sample["service_day"] == d]
        e = (test["passio_epoch"] - test["actual_epoch"]).to_numpy(float)
        ld = test["lead_s"].to_numpy(float)
        res.setdefault(("Passio as shown", ""), []).append((test["bin"].to_numpy(), e, ld))
        for t, (lo, hi) in TARGETS.items():
            leaky = apply(test, learn(sample[sample["service_day"] < d], "bin", "lead_s", lo, hi), "bin") * ld
            fair = apply(test, learn(train_all[train_all["service_day"] < d], "pbin", "lead_passio", lo, hi), "pbin") \
                * np.maximum(test["lead_passio"].to_numpy(float), 60.0)
            res.setdefault(("as in E24 (leaks the real arrival)", t), []).append((test["bin"].to_numpy(), e - leaky, ld))
            res.setdefault(("leak-free", t), []).append((test["bin"].to_numpy(), e - fair, ld))
        print(f"{d}: done", file=sys.stderr)
    lines = ["# E24 headroom check: the same learned shift with and without the real arrival", "",
             f"Test days {test_days[0]} to {test_days[-1]}, learned on earlier days only. Each cell: 10% rule / band B as E24 "
             "read it (10% of the lead early to 1% late) / too late (shown later than the bus came by more than 1% of the lead).", "",
             "| version | shift tuned for | " + " | ".join(f"{b} min" for b in BINS) + " |", "|---|---|" + "---|" * len(BINS)]
    for (name, t), parts in res.items():
        bins = np.concatenate([p[0] for p in parts])
        e = np.concatenate([p[1] for p in parts])
        ld = np.concatenate([p[2] for p in parts])
        cells = []
        for b in BINS:
            m = bins == b
            p10, bb, tl = measures(e[m], ld[m])
            cells.append(f"{100 * p10:.0f}% / {100 * bb:.0f}% / {100 * tl:.0f}%")
        lines.append(f"| {name} | {t} | " + " | ".join(cells) + " |")
    md = "\n".join(lines) + "\n"
    print(md)
    (HERE / a.out).with_suffix(".md").write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()
