#!/usr/bin/env python3
"""Check that this bench reproduces the project's official scoreboard: Passio's sample size, gross misses and passes
under the 10 minute shrink, per day and goal bin, against data/eta/summary.csv on the main repo's data branch.

  python algorithm-test/validate.py   (exit 1 on any mismatch)
"""
import csv, io, sys, urllib.request

import numpy as np

import dataset as D
import scoring as S

SUMMARY = "https://raw.githubusercontent.com/blobberus/straight-bussing/data/data/eta/summary.csv"


def official():
    with urllib.request.urlopen(SUMMARY, timeout=60) as r:
        rows = list(csv.DictReader(io.StringIO(r.read().decode("utf-8"))))
    return {(r["service_day"], r["lead_bin"]): r for r in rows
            if r["source"] == "passio" and r["route"] == "ALL" and r["segment"] == "all"}


def main():
    off, bad, checked = official(), 0, 0
    for day in D.days_in():
        s = D.sample(D.load_day(day))
        for _, _, name, _ in S.GOAL_BINS:
            o = off.get((day, name))
            b = s[s["bin"] == name]
            if o is None or b.empty:
                continue
            err = (b["passio_epoch"] - b["actual_epoch"]).to_numpy()
            lead = b["lead_s"].to_numpy()
            g = S.gross(err, lead)
            mine = (len(b), int(g.sum()), int((np.abs(err[~g]) <= S.shrink_tol(lead[~g])).sum()))
            theirs = (int(o["n"]), int(o["gross"]), int(o["pass_shrink"]))
            checked += 1
            if mine != theirs:
                bad += 1
                print(f"MISMATCH {day} {name}: bench {mine} vs scoreboard {theirs}")
    print(f"{checked} day x bin cells checked, {bad} mismatches")
    sys.exit(1 if bad or not checked else 0)


if __name__ == "__main__":
    main()
