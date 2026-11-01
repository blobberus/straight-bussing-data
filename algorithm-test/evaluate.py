#!/usr/bin/env python3
"""Rolling-origin evaluation against the accuracy requirement.

  python algorithm-test/evaluate.py --models passio,timetable,timetable_delay [--test-days 11] [--out results/NAME]

For every test day (the last N service days), each model is fitted on the training table (every query minute, not
picked by the true lead: dataset.load_train_all) of all EARLIER days only and predicts that day's scoreboard sample; a model's missing predictions fall back to Passio's time (counted as "fallback"). Results per goal
bin: the scoring.py numbers, whether the goal is met (most predictions inside band B), and the change in band B and in
"too late" against Passio with a 95% interval from resampling whole test days (days are the unit of noise).
"""
import argparse, json, random, sys, time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dataset as D          # noqa: E402
import scoring as S          # noqa: E402
import predictors as P       # noqa: E402

BINS = [b[2] for b in S.GOAL_BINS]


def run(models, sample, test_days, train_table, log=print):
    """-> DataFrame of test rows with one predicted-epoch column per model ('pred_<name>') and 'fb_<name>' flags."""
    out = []
    for d in test_days:
        train, test = train_table[train_table["service_day"] < d], sample[sample["service_day"] == d].copy()
        for m in models:
            t0 = time.time()
            p = m().fit(train).predict(test)
            fb = np.isnan(p)
            test["pred_" + m.name] = np.where(fb, test["passio_epoch"].to_numpy(float), p)
            test["fb_" + m.name] = fb
            log(f"  {d} {m.name}: {len(test)} rows, {fb.mean():.0%} fallback, {time.time() - t0:.1f} s")
        out.append(test)
    return pd.concat(out, ignore_index=True)


def per_day_rates(df, col):
    """{day: (band_b passes, non-gross n, too-late count, n)} for one bin's rows and one prediction column."""
    res = {}
    for d, g in df.groupby("service_day"):
        err = (g[col] - g["actual_epoch"]).to_numpy()
        lead = g["lead_s"].to_numpy()
        gr = S.gross(err, lead)
        tol = S.shrink_tol(lead)
        e, L, t = err[~gr], lead[~gr], tol[~gr]
        res[d] = (int(((e >= -t) & (e <= 0.01 * L)).sum()), int((~gr).sum()), int((err > 0.01 * lead).sum()), len(err))
    return res


def boot_diff(a, b, k=0, boots=2000, seed=7):
    """95% interval over days of rate(a) - rate(b), where a, b are per_day_rates dicts; k=0 band B, k=2 too late."""
    days = sorted(set(a) & set(b))
    if len(days) < 2:
        return None
    den = 1 if k == 0 else 3
    rnd = random.Random(seed)
    sims = []
    for _ in range(boots):
        pick = [rnd.choice(days) for _ in days]
        ra = sum(a[d][k] for d in pick) / max(sum(a[d][den] for d in pick), 1)
        rb = sum(b[d][k] for d in pick) / max(sum(b[d][den] for d in pick), 1)
        sims.append(ra - rb)
    sims.sort()
    return sims[int(0.025 * len(sims))], sims[int(0.975 * len(sims)) - 1]


def report(df, names, title):
    lines = [f"# {title}", "", f"Test days: {df['service_day'].min()} to {df['service_day'].max()} "
             f"({df['service_day'].nunique()} days, {len(df):,} samples; each model trained only on earlier days).", "",
             "| model | lead | samples | band B (goal) | goal met | within allowed | too late | gross | median err | "
             "band B vs Passio (95% over days) | too late vs Passio | fallback |",
             "|---|---|---:|---:|:---:|---:|---:|---:|---:|---|---|---:|"]
    js = {}
    for name in names:
        for b in BINS:
            g = df[df["bin"] == b]
            if g.empty:
                continue
            s = S.score((g["pred_" + name] - g["actual_epoch"]).to_numpy(), g["lead_s"].to_numpy())
            ref = S.score((g["passio_epoch"] - g["actual_epoch"]).to_numpy(), g["lead_s"].to_numpy())
            a, r = per_day_rates(g, "pred_" + name), per_day_rates(g, "passio_epoch")
            ci = boot_diff(a, r, 0) if name != "passio" else None
            cl = boot_diff(a, r, 2) if name != "passio" else None
            fmt = lambda c: f"{100 * c[0]:+.1f} to {100 * c[1]:+.1f} pts" if c else ""
            lines.append(f"| {name} | {b} min | {s['n']:,} | {100 * s['band_b']:.1f}% | {'yes' if S.meets(s) else 'no'} | "
                         f"{100 * s['shrink']:.1f}% | {100 * s['too_late']:.1f}% | {100 * s['gross']:.1f}% | "
                         f"{s['median_err_s'] / 60:+.1f} min | "
                         f"{(100 * (s['band_b'] - ref['band_b'])):+.1f} pts ({fmt(ci)}) | "
                         f"{(100 * (s['too_late'] - ref['too_late'])):+.1f} pts ({fmt(cl)}) | {g['fb_' + name].mean():.0%} |"
                         if name != "passio" else
                         f"| {name} | {b} min | {s['n']:,} | {100 * s['band_b']:.1f}% | {'yes' if S.meets(s) else 'no'} | "
                         f"{100 * s['shrink']:.1f}% | {100 * s['too_late']:.1f}% | {100 * s['gross']:.1f}% | "
                         f"{s['median_err_s'] / 60:+.1f} min | (reference) | (reference) | 0% |")
            js.setdefault(name, {})[b] = {**s, "band_b_vs_passio_ci": ci, "too_late_vs_passio_ci": cl}
    lines += ["", "Goal: most predictions (50% or more) inside band B, the allowed error early (1 min under 20 min ahead, "
              "2 min at 20 to 30, 3 min at 30 or more) to 1% of the lead late. Too late = shown later than the bus came by "
              "more than 1% of the lead (the ship gate: never more often than Passio). Errors: negative = the bus came "
              "later than predicted."]
    return "\n".join(lines) + "\n", js


def by_route(df, names, bins=("0-10", "10-15", "20-30")):
    """Ship gate rule 3: no route more than 10% worse than Passio. Band B (and too late) per route, model vs Passio."""
    lines = ["", "## Per route (ship gate: no route more than 10% worse than Passio in band B)", "",
             "| route | lead | samples | Passio band B | " + " | ".join(f"{n} band B" for n in names if n != "passio") +
             " | Passio too late | " + " | ".join(f"{n} too late" for n in names if n != "passio") + " |",
             "|---|---|---:|---:|" + "---:|" * (2 * (len(names) - 1) + 1)]
    worse = []
    for (route, b), g in df.groupby(["route_name", "bin"]):
        if b not in bins or len(g) < 300:
            continue
        lead = g["lead_s"].to_numpy()
        sc = {n: S.score((g["pred_" + n] - g["actual_epoch"]).to_numpy(), lead) for n in names}
        ref = sc["passio"]["band_b"]
        cells_b, cells_l = [], []
        for n in names:
            if n == "passio":
                continue
            v = sc[n]["band_b"]
            flag = " (worse by >10%)" if v < 0.9 * ref else ""
            if flag:
                worse.append(f"{n} on {route} at {b} min")
            cells_b.append(f"{100 * v:.1f}%{flag}")
            cells_l.append(f"{100 * sc[n]['too_late']:.1f}%")
        lines.append(f"| {route} | {b} min | {len(g):,} | {100 * ref:.1f}% | " + " | ".join(cells_b) +
                     f" | {100 * sc['passio']['too_late']:.1f}% | " + " | ".join(cells_l) + " |")
    lines += ["", "Worse than Passio by more than 10% (relative): " + ("; ".join(worse) if worse else "none") + "."]
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--models", default="passio,timetable,timetable_delay")
    ap.add_argument("--test-days", type=int, default=11)
    ap.add_argument("--out", default="")
    ap.add_argument("--title", default="Algorithm test")
    ap.add_argument("--by-route", action="store_true", help="add the per-route table (ship gate rule 3)")
    a = ap.parse_args(argv)
    import models  # noqa: F401  (registers the learned models)
    sample = D.load_all()
    days = sorted(sample["service_day"].unique())
    test_days = days[-a.test_days:]
    names = [n.strip() for n in a.models.split(",") if n.strip()]
    if "passio" not in names:
        names.insert(0, "passio")
    df = run([P.REGISTRY[n] for n in names], sample, test_days, D.load_train_all())
    md, js = report(df, names, a.title)
    if a.by_route:
        md += by_route(df, names)
    print(md)
    if a.out:
        out = HERE / a.out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.with_suffix(".md").write_text(md, encoding="utf-8")
        out.with_suffix(".json").write_text(json.dumps(js, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
