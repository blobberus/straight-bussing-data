#!/usr/bin/env python3
"""Scores every model in TRANSITION periods (a line's bus count changing) against normal periods, and on the rows of a
bus that is about to leave its line (owner, 2026-11-06: "Using this data, both add it to the bus prediction details so
that the algorithm can be tested against it"). Main repo: RouteKnower.md E29, data/labeled/transitions/.

Transitions come from the main repo's data/labeled/transitions/transitions.csv (one row per change: a bus leaving or
joining a line, labeled break / shift_end / route_switch / feed_drop / added_from_* / layover_swap). Forecast tables
built after 2026-11-06 carry the same facts as columns (transition_min, bus_leaves_min, ...); for older tables they are
joined here with the same definitions (tools/build_eta_dataset.py flag_transitions):
  transition_min  minutes from the nearest transition on the row's line (a lasting leave, or an add that is not the end
                  of a layover) to the query time, negative = still ahead; blank if none within 45 min
  bus_leaves_min  minutes from the query until this bus's own lasting leave from the row's line (0 to 45)
  added_recently  minutes since this bus joined the row's line (an add that is not a layover's end), if within 30
Groups (one sample per arrival and goal bin, the same rows for every model; models trained on earlier days only, as in
evaluate.py): normal = no transition on the line within 15 min of the query; transition = one within 15 min;
leave ahead = the row's bus leaves its line within 30 min of the query (its last stops before it goes); just added =
the bus joined its line at most 15 min before. A second table counts Passio's shown times that never came true
(label_status no_arrival) around buses that leave, from the whole tables.

  python algorithm-test/transitions.py [--models passio,timetable_delay,gbm_q15,deep_q15,deep_safe] [--test-days 11]
      [--transitions <path or URL>] [--out results/12-transitions]
"""
import argparse, io, json, sys, urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dataset as D          # noqa: E402
import evaluate as E         # noqa: E402
import predictors as P       # noqa: E402
import scoring as S          # noqa: E402

URL = "https://raw.githubusercontent.com/blobberus/straight-bussing/main/data/labeled/transitions/transitions.csv"
LASTING = {"break", "shift_end", "route_switch", "feed_drop"}
WINDOW_S = 2700
NEAR_S = 900


def read_transitions(src):
    if str(src).startswith("http"):
        with urllib.request.urlopen(src, timeout=120) as r:
            return pd.read_csv(io.BytesIO(r.read()), dtype=str, keep_default_na=False)
    return pd.read_csv(src, dtype=str, keep_default_na=False)


def join(df, tr):
    """Adds transition_min, bus_leaves_min, added_recently (definitions in the module docstring) where the table lacks
    them. In place; -> df."""
    tr = tr.copy()
    tr["epoch"] = tr["epoch"].astype("int64")
    real = tr[((tr["kind"] == "leave") & tr["label"].isin(LASTING)) | ((tr["kind"] == "add") & (tr["label"] != "layover_swap"))]
    by_route = {rid: np.sort(g["epoch"].to_numpy()) for rid, g in real.groupby("route_id")}
    lv = real[real["kind"] == "leave"]
    leaves = {k: np.sort(g["epoch"].to_numpy()) for k, g in lv.groupby(["route_id", "vehicle_id"])}
    ad = real[real["kind"] == "add"]
    adds = {k: np.sort(g["epoch"].to_numpy()) for k, g in ad.groupby(["route_id", "vehicle_id"])}
    q = df["query_epoch"].to_numpy("int64")
    rid = df["route_id"].astype(str).to_numpy()
    veh = df["vehicle_id"].astype(str).to_numpy()
    tmin, lmin, amin = np.full(len(df), np.nan), np.full(len(df), np.nan), np.full(len(df), np.nan)
    for i in range(len(df)):
        e = by_route.get(rid[i])
        if e is not None and len(e):
            j = np.searchsorted(e, q[i])
            best = None
            for k in (j - 1, j):
                if 0 <= k < len(e) and abs(e[k] - q[i]) <= WINDOW_S and (best is None or abs(e[k] - q[i]) < abs(best - q[i])):
                    best = e[k]
            if best is not None:
                tmin[i] = (q[i] - best) / 60
        e = leaves.get((rid[i], veh[i]))
        if e is not None:
            j = np.searchsorted(e, q[i])
            if j < len(e) and e[j] - q[i] <= WINDOW_S:
                lmin[i] = (e[j] - q[i]) / 60
        e = adds.get((rid[i], veh[i]))
        if e is not None:
            j = np.searchsorted(e, q[i], side="right")
            if j and q[i] - e[j - 1] <= 1800:
                amin[i] = (q[i] - e[j - 1]) / 60
    for col, v in (("transition_min", tmin), ("bus_leaves_min", lmin), ("added_recently", amin)):
        have = pd.to_numeric(df[col], errors="coerce") if col in df.columns else pd.Series(np.nan, index=df.index)
        df[col] = np.where(have.notna(), have, v)
    return df


def groups(df):
    t, l, a = df["transition_min"], df["bus_leaves_min"], df["added_recently"]
    return {"normal": t.isna() | (t.abs() > NEAR_S / 60), "transition": t.abs() <= NEAR_S / 60,
            "leave ahead (bus leaves within 30 min)": l <= 30, "just added (within 15 min)": a <= 15}


def score_table(df, names):
    lines = ["| model | group | " + " | ".join(f"{b} band B / too late (n)" for b in E.BINS) + " |",
             "|---|---|" + "---|" * len(E.BINS)]
    js = {}
    for n in names:
        for g, m in groups(df).items():
            cells = []
            for b in E.BINS:
                sub = df[m & (df["bin"] == b)]
                if len(sub) < 30:
                    cells.append(f"(n={len(sub)})")
                    continue
                s = S.score((sub["pred_" + n] - sub["actual_epoch"]).to_numpy(), sub["lead_s"].to_numpy())
                cells.append(f"{100 * s['band_b']:.1f}% / {100 * s['too_late']:.1f}% ({s['n']:,})")
                js.setdefault(n, {}).setdefault(g, {})[b] = {k: s[k] for k in ("n", "band_b", "too_late", "gross", "median_err_s")}
            lines.append(f"| {n} | {g} | " + " | ".join(cells) + " |")
    return "\n".join(lines), js


def phantom_table(days, tr, cache=None):
    """Passio's shown times that never came true (no_arrival rows) among all its shown times, by the bus's state:
    up to 45 min before it leaves its line for good, up to 45 min after, otherwise. Whole tables, every minute."""
    tr = tr[(tr["kind"] == "leave") & tr["label"].isin(LASTING)].copy()
    tr["epoch"] = tr["epoch"].astype("int64")
    leaves = {v: np.sort(g["epoch"].to_numpy()) for v, g in tr.groupby("vehicle_id")}
    cnt = {k: [0, 0] for k in ("before leaving (45 min)", "after leaving (45 min)", "otherwise")}
    for d in days:
        p = Path(cache or HERE / "cache") / f"eta-{d}.csv.gz"
        t = pd.read_csv(p, usecols=["query_epoch", "vehicle_id", "passio_status", "label_status"], dtype=str,
                        keep_default_na=False)
        t = t[t["passio_status"] == "shown"]
        q = t["query_epoch"].astype("int64").to_numpy()
        v = t["vehicle_id"].to_numpy()
        ph = (t["label_status"] == "no_arrival").to_numpy()
        for i in range(len(t)):
            e = leaves.get(v[i])
            k = "otherwise"
            if e is not None:
                j = np.searchsorted(e, q[i])
                if j < len(e) and e[j] - q[i] <= WINDOW_S:
                    k = "before leaving (45 min)"
                elif j and q[i] - e[j - 1] <= WINDOW_S:
                    k = "after leaving (45 min)"
            cnt[k][0] += 1
            cnt[k][1] += int(ph[i])
    lines = ["| bus state | Passio times shown (bus-minute x stop) | never came true |", "|---|---:|---:|"]
    for k, (n, x) in cnt.items():
        lines.append(f"| {k} | {n:,} | {100 * x / max(1, n):.1f}% |")
    return "\n".join(lines), {k: {"shown": n, "never": x} for k, (n, x) in cnt.items()}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--models", default="passio,timetable_delay,gbm_q15,deep_q15,deep_safe")
    ap.add_argument("--test-days", type=int, default=11)
    ap.add_argument("--transitions", default=URL)
    ap.add_argument("--out", default="results/12-transitions")
    a = ap.parse_args(argv)
    import models  # noqa: F401  (registers the learned models)
    tr = read_transitions(a.transitions)
    sample = join(D.load_all(), tr)
    days = sorted(sample["service_day"].unique())
    test_days = days[-a.test_days:]
    names = [n.strip() for n in a.models.split(",") if n.strip()]
    if "passio" not in names:
        names.insert(0, "passio")
    df = E.run([P.REGISTRY[n] for n in names], sample, test_days, join(D.load_train_all(), tr))
    tab, js = score_table(df, names)
    ph, pj = phantom_table(test_days, tr)
    g = groups(df)
    share = {k: f"{100 * m.mean():.1f}%" for k, m in g.items()}
    md = "\n".join([
        "# Transition periods: every model when a line's bus count changes", "",
        f"Test days: {test_days[0]} to {test_days[-1]} ({len(test_days)} days, {len(df):,} samples; each model trained only "
        "on earlier days). Transitions: the main repo's data/labeled/transitions/transitions.csv (RouteKnower E29).", "",
        "Share of samples: " + ", ".join(f"{k} {v}" for k, v in share.items()) + ".", "",
        "Each cell: band B (the goal: most predictions inside it) / too late (shown later than the bus came by more than "
        "1% of the lead) and the samples.", "", tab, "",
        "## Passio's times that never came true, around buses that leave their line", "",
        "From the whole tables of the test days (every minute, every stop Passio showed for a bus). A bus that leaves its "
        "line stops serving it; Passio keeps showing it (79% of lasting leaves, E29). The main repo's app now drops a "
        "bus's times once it has sent no report for 15 min (web/js/core/transition.js).", "", ph, ""])
    print(md)
    out = HERE / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.with_suffix(".md").write_text(md, encoding="utf-8")
    out.with_suffix(".json").write_text(json.dumps({"scores": js, "phantom": pj, "share": share}, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
