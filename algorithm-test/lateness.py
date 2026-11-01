#!/usr/bin/env python3
"""Who makes buses arrive later than riders were told? Late minutes = how much later the bus came than Passio's time
on display (0 when it came on time or early), one sample per arrival and goal bin (dataset.load_all), every day.
Each table ranks a dimension by its share of all late minutes; the four biggest perpetrators are picked from them.

  python algorithm-test/lateness.py [--out results/07-lateness]
"""
import argparse, sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dataset as D   # noqa: E402


def situation(s):
    nt = s["next_trip"].fillna(0) == 1
    term = s["crosses_terminal"].fillna(0) == 1
    stand = s["standing_s"].fillna(0) >= 300
    out = np.where(nt & stand, "next trip, bus standing at the end of its line (layover)",
          np.where(nt, "next trip, bus still finishing its run",
          np.where(term, "current trip, through the end of the line",
                   "current trip, stops still ahead on this run")))
    return pd.Series(out, index=s.index)


def delay_bucket(s):
    d = s["delay_s"]
    return pd.Series(np.select([d.isna(), d < -120, d <= 120, d <= 300, d <= 600], ["no timetable (frequency trips) or unknown",
                     "more than 2 min early", "on time (within 2 min)", "2 to 5 min late", "5 to 10 min late"],
                     "more than 10 min late"), index=s.index)


def hour_bucket(s):
    h = s["hour"]
    return pd.Series(np.select([h < 7, h < 10, h < 15, h < 19, h < 22], ["5 to 7 AM", "7 to 10 AM", "10 AM to 3 PM", "3 to 7 PM",
                     "7 to 10 PM"], "10 PM to 5 AM"), index=s.index)


def table(s, key, title, top=8):
    late = s["late_min"]
    g = pd.DataFrame({"k": key, "late": late, "big": late > 3}).groupby("k").agg(samples=("late", "size"),
        late_min=("late", "sum"), mean=("late", "mean"), big=("big", "mean"))
    g["share"] = g["late_min"] / late.sum()
    g = g.sort_values("late_min", ascending=False).head(top)
    lines = [f"### {title}", "", "| | samples | share of all late minutes | late per sample (min) | more than 3 min late |",
             "|---|---:|---:|---:|---:|"]
    for k, r in g.iterrows():
        lines.append(f"| {k} | {int(r.samples):,} | {100 * r.share:.1f}% | {r['mean']:.1f} | {100 * r.big:.0f}% |")
    return lines + [""], g


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", default="results/07-lateness")
    a = ap.parse_args(argv)
    s = D.load_all()
    s = s.assign(late_min=np.maximum(0.0, (s["actual_epoch"] - s["passio_epoch"]) / 60.0))
    total = s["late_min"].sum()
    out = ["# Lateness perpetrators: what makes buses come later than riders were told", "",
           f"{s['service_day'].min()} to {s['service_day'].max()}, {len(s):,} samples (one per arrival and lead range). "
           f"{100 * (s['late_min'] > 0).mean():.0f}% of samples came later than shown, {total:,.0f} late minutes in total, "
           f"{s['late_min'].mean():.1f} per sample.", ""]
    tabs = {}
    for name, key in [("route", s["route_name"]), ("situation", situation(s)), ("delay", delay_bucket(s)),
                      ("hour", hour_bucket(s)), ("stop", s["route_name"] + ": " + s["stop_name"]),
                      ("route_situation", s["route_name"] + ", " + situation(s))]:
        title = {"route": "By route", "situation": "By what the bus is doing", "delay": "By the bus's current delay against the timetable",
                 "hour": "By time of day", "stop": "By stop (route: stop)", "route_situation": "By route and what the bus is doing"}[name]
        lines, g = table(s, key, title)
        out += lines
        tabs[name] = g
    md = "\n".join(out) + "\n"
    print(md)
    (HERE / a.out).with_suffix(".md").write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()
