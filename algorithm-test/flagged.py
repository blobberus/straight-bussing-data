#!/usr/bin/env python3
"""Scores every model on the FLAGGED LINES as separate slices (owner, 2026-11-11: "Create or indicate wherever
appropriate for another agent to analyze and notice and account for this data. Flag these lines"). Main repo:
data/labeled/flags/flagged_lines.csv (merged by tools/flag_lines.py from RouteKnower E30 odd transitions, E31 large
prediction misses, E32 display replay; README there = the schema and what every agent must do), RouteKnower.md 6.4:
a model that wins on average but loses on a flagged slice is not shipped.

Each active flag (status open or watch) is one slice: the flag's line, narrowed by its scope (the README's grammar:
stops=, hours= (the query's Chicago hour), days=, vehicles=, lead= (minutes ahead), trips=no_timetable|timetable,
dates=; note= and free text are never filters and are listed as "not applied"). Every model is scored on the same
rows of the slice (the evaluate.py sample: one sample per arrival and goal bin; models trained on earlier days only)
per goal bin, against Passio on the same rows. A model LOSES on a slice when, in a bin with at least MIN_N samples, its
band B is more than 10% (relative) below Passio's (ship gate 6.6 rule 3) or it is too late more often than Passio by
more than 1 point (the 1% rule must not get worse; an early bus is a missed bus).

The flags were measured on days that can overlap the test days. That is fine here: a flag only picks which rows to
look at, it is never a model input (as a feature it would leak, RouteKnower 6.2).

  python algorithm-test/flagged.py [--models passio,timetable_delay,gbm_q15,deep_q15,deep_safe] [--test-days 11]
      [--flags <path or URL>] [--out results/13-flagged-lines]
"""
import argparse, io, json, sys, urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import scoring as S          # noqa: E402

URL = "https://raw.githubusercontent.com/blobberus/straight-bussing/main/data/labeled/flags/flagged_lines.csv"
ACTIVE = ("open", "watch")
MIN_N = 30
BINS = [b[2] for b in S.GOAL_BINS]
DOW = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6, "saturday": 5, "sunday": 6}
FILTERS = ("stops", "hours", "days", "vehicles", "lead", "trips", "dates")


def read_flags(src):
    if str(src).startswith("http"):
        with urllib.request.urlopen(src, timeout=120) as r:
            return pd.read_csv(io.BytesIO(r.read()), dtype=str, keep_default_na=False)
    return pd.read_csv(src, dtype=str, keep_default_na=False)


def parse_scope(scope):
    """'stops=1|2;hours=15-19;note=x' -> ({key: [values]} of the filter keys, [parts not applied])."""
    out, skipped = {}, []
    s = (scope or "").strip()
    if s.lower() in ("", "all"):
        return out, skipped
    for tok in (t.strip() for t in s.split(";")):
        if not tok:
            continue
        k, _, v = tok.partition("=")
        k = k.strip().lower()
        vals = [x.strip() for x in v.split("|") if x.strip()]
        if "=" not in tok or k not in FILTERS or not vals:
            skipped.append(tok)
            continue
        out.setdefault(k, []).extend(vals)
    return out, skipped


def _hours_mask(hour, ranges):
    m = np.zeros(len(hour), bool)
    for r in ranges:
        a, b = (int(x) for x in r.split("-"))
        m |= ((hour >= a) & (hour < b)) if a < b else ((hour >= a) | (hour < b % 24))
    return m


def slice_mask(df, route_id, scope):
    """-> (boolean mask over df's rows, [scope parts not applied])."""
    sc, skipped = parse_scope(scope)
    m = np.array(df["route_id"].astype(str) == str(route_id), dtype=bool)      # a writable copy (pandas 3 views are read-only)
    for k, vals in sc.items():
        if k == "stops":
            m &= df["stop_id"].astype(str).isin(vals).to_numpy()
        elif k == "vehicles":
            m &= df["vehicle_id"].astype(str).isin(vals).to_numpy()
        elif k == "dates":
            m &= df["service_day"].astype(str).isin(vals).to_numpy()
        elif k == "hours":
            m &= _hours_mask(pd.to_numeric(df["hour"], errors="coerce").fillna(-1).to_numpy(), vals)
        elif k == "lead":
            lead_min = df["lead_s"].to_numpy(float) / 60
            lm = np.zeros(len(df), bool)
            for r in vals:
                lo, hi = (float(x) for x in r.split("-"))
                lm |= (lead_min >= lo) & (lead_min < hi)
            m &= lm
        elif k == "days":
            dow = pd.to_numeric(df["dow"], errors="coerce").fillna(-1).to_numpy()
            dm = np.zeros(len(df), bool)
            for v in (x.lower() for x in vals):
                if v == "weekday":
                    dm |= (dow >= 0) & (dow <= 4)
                elif v == "weekend":
                    dm |= dow >= 5
                elif v in DOW:
                    dm |= dow == DOW[v]
                else:
                    skipped.append(f"days={v}")
            m &= dm
        elif k == "trips":
            tt = df["tt_epoch"].isna().to_numpy()
            tm = np.zeros(len(df), bool)
            for v in (x.lower() for x in vals):
                tm |= tt if v == "no_timetable" else ~tt if v == "timetable" else False
            m &= tm
    return m, skipped


def score_slice(g, names):
    """{model: {bin: score dict}} for one slice's rows (only bins with rows)."""
    out = {}
    for n in names:
        for b in BINS:
            sub = g[g["bin"] == b]
            if sub.empty:
                continue
            out.setdefault(n, {})[b] = S.score((sub["pred_" + n] - sub["actual_epoch"]).to_numpy(), sub["lead_s"].to_numpy())
    return out


def verdict(sc, name, min_n=MIN_N):
    """'loses' / 'holds' / 'too few rows' for one model on one slice against Passio (rules in the docstring)."""
    if name == "passio":
        return "reference", []
    why, scored = [], 0
    for b, s in sc.get(name, {}).items():
        ref = sc["passio"].get(b, {})
        if s.get("n", 0) < min_n:
            continue
        scored += 1
        if s["band_b"] < 0.9 * ref["band_b"]:
            why.append(f"band B {100 * s['band_b']:.1f}% vs Passio {100 * ref['band_b']:.1f}% at {b} min")
        if s["too_late"] > ref["too_late"] + 0.01:
            why.append(f"too late {100 * s['too_late']:.1f}% vs Passio {100 * ref['too_late']:.1f}% at {b} min")
    if not scored:
        return "too few rows", []
    return ("loses" if why else "holds"), why


def report(df, flags, names):
    """-> (markdown, json) of every active flag's slice."""
    act = flags[flags["status"].isin(ACTIVE)] if len(flags) else flags
    allsc = score_slice(df, names)
    js = {"all_rows": allsc, "flags": {}}
    head = ["| model | line | slice samples | " + " | ".join(f"{b} min" for b in BINS) + " | verdict vs Passio |",
            "|---|---|---:|" + "---|" * len(BINS) + "---|"]
    L = ["Each cell: band B / too late (samples). Band B = inside the allowed error early to 1% of the lead late (the "
         f"goal: 50% or more); too late = shown later than the bus came by more than 1% of the lead. Bins with fewer than "
         f"{MIN_N} samples are shown in parentheses and never decide a verdict.", ""]
    summary, losers = [], {}
    for n in names:
        cells = []
        for b in BINS:
            s = allsc.get(n, {}).get(b)
            cells.append(f"{100 * s['band_b']:.1f}% / {100 * s['too_late']:.1f}% ({s['n']:,})" if s else "")
        summary.append(f"| (all rows) | all lines | {len(df):,} | " + " | ".join(cells) + f" | {n} |")
    for _, f in act.iterrows():
        m, skipped = slice_mask(df, f["route_id"], f["scope"])
        g = df[m]
        sc = score_slice(g, names)
        fj = {"route_id": f["route_id"], "route": f["route"], "category": f["category"], "severity": f["severity"],
              "scope": f["scope"], "not_applied": skipped, "rows": int(m.sum()), "scores": sc, "verdicts": {}}
        L += [f"### {f['flag_id']} ({f['severity']}, {f['status']})", "",
              f"{f['route']}; scope: {f['scope'] or 'the whole line'}" + (f" (not applied: {'; '.join(skipped)})" if skipped else "")
              + f"; {int(m.sum()):,} samples. Flag: {f['metric']} {f['value']}" + (f" (all lines {f['baseline']})" if f['baseline'] else "") + ".", "",
              head[0], head[1]]
        for n in names:
            cells = []
            for b in BINS:
                s = sc.get(n, {}).get(b)
                if not s:
                    cells.append("")
                    continue
                txt = f"{100 * s['band_b']:.1f}% / {100 * s['too_late']:.1f}% ({s['n']:,})"
                cells.append(txt if s["n"] >= MIN_N else f"({txt})")
            v, why = verdict(sc, n) if sc else ("no rows", [])
            fj["verdicts"][n] = {"verdict": v, "why": why}
            if v == "loses":
                losers.setdefault(n, []).append(f["flag_id"])
            L.append(f"| {n} | {f['route']} | {int(m.sum()):,} | " + " | ".join(cells) + f" | {v}" + (f": {'; '.join(why)}" if why else "") + " |")
        L.append("")
        js["flags"][f["flag_id"]] = fj
    lose = ["| model | flagged slices it loses on (ship gate: not shipped while any) |", "|---|---|"]
    for n in names:
        if n != "passio":
            lose.append(f"| {n} | {', '.join(f'`{x}`' for x in losers.get(n, [])) or 'none'} |")
    js["losers"] = losers
    return L, summary, head, lose, js


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--models", default="passio,timetable_delay,gbm_q15,deep_q15,deep_safe")
    ap.add_argument("--test-days", type=int, default=11)
    ap.add_argument("--flags", default=URL)
    ap.add_argument("--out", default="results/13-flagged-lines")
    a = ap.parse_args(argv)
    import dataset as D          # noqa: E402
    import evaluate as E         # noqa: E402
    import predictors as P       # noqa: E402
    import models  # noqa: F401  (registers the learned models)
    flags = read_flags(a.flags)
    act = flags[flags["status"].isin(ACTIVE)] if len(flags) else flags
    names = [n.strip() for n in a.models.split(",") if n.strip()]
    if "passio" not in names:
        names.insert(0, "passio")
    out = HERE / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    if act.empty:
        md = ("# Flagged lines: every model on each flagged slice\n\nNo active flags in the main repo's "
              "data/labeled/flags/flagged_lines.csv yet: nothing to score.\n")
        print(md)
        out.with_suffix(".md").write_text(md, encoding="utf-8")
        out.with_suffix(".json").write_text(json.dumps({"flags": {}}, indent=1), encoding="utf-8")
        return
    sample = D.load_all()
    days = sorted(sample["service_day"].unique())
    test_days = days[-a.test_days:]
    df = E.run([P.REGISTRY[n] for n in names], sample, test_days, D.load_train_all())
    L, summary, head, lose, js = report(df, flags, names)
    nflag = len(js["flags"])
    md = "\n".join([
        "# Flagged lines: every model on each flagged slice", "",
        f"Test days: {test_days[0]} to {test_days[-1]} ({len(test_days)} days, {len(df):,} samples; each model trained only "
        f"on earlier days). Flags: the main repo's data/labeled/flags/flagged_lines.csv, {nflag} active (open or watch); "
        "each is the flag's line narrowed by its scope (README there). RouteKnower.md 6.4: a model that wins on average "
        "but loses on a flagged slice is not shipped.", "",
        "## Which model loses where", "",
        f"Loses = in a bin with {MIN_N}+ samples, band B more than 10% (relative) below Passio's, or too late more often "
        "than Passio by more than 1 point.", "", *lose, "",
        "## All rows (for comparison)", "", head[0].replace("| model |", "| rows |", 1).replace("verdict vs Passio", "model"),
        head[1], *summary, "",
        "## Each flagged slice", "", *L])
    print(md)
    out.with_suffix(".md").write_text(md + "\n", encoding="utf-8")
    js["test_days"] = test_days
    out.with_suffix(".json").write_text(json.dumps(js, indent=1, default=float), encoding="utf-8")


if __name__ == "__main__":
    main()
