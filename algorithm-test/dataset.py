"""Load the forecast tables and draw the evaluation sample.

One forecast-table row = (query minute t, bus, one of its arrivals in the next 45 min). Rows of one arrival are near
copies, so (like the main repo's daily scoreboard, tools/build_eta_dataset.py summary()) every arrival gives ONE sample
per goal bin: the row whose lead is nearest the bin's sample point. Here the sample is drawn among rows where Passio
showed a time, so every predictor is scored on the same rows (scoring rule 6: same rows for every predictor).
"""
from pathlib import Path

import numpy as np
import pandas as pd

from scoring import GOAL_BINS

HERE = Path(__file__).resolve().parent
NUM = ["query_epoch", "dow", "hour", "stop_index", "visit_rank", "next_trip", "stops_away", "dist_m", "crosses_terminal",
       "last_age_s", "speed_mps", "standing_s", "delay_s", "actual_epoch", "lead_s", "passio_epoch", "passio_age_s",
       "tt_epoch", "ttd_epoch", "bus_change_min", "leaving_bus"]
TXT = ["service_day", "day_type", "cal_regime", "vehicle_id", "route_id", "route_name", "trip_id", "stop_id", "stop_name",
       "label_status", "passio_status"]


def days_in(cache=None):
    """Service days with a cached table, sorted."""
    return sorted(p.name[4:14] for p in Path(cache or HERE / "cache").glob("eta-*.csv.gz"))


def load_day(day, cache=None):
    """Arrived rows of one day's table, numeric columns as floats (blank = NaN). Older tables lack the newer columns."""
    p = Path(cache or HERE / "cache") / f"eta-{day}.csv.gz"
    df = pd.read_csv(p, dtype=str, keep_default_na=False)
    df = df[df["label_status"] == "arrived"].copy()
    for c in NUM:
        df[c] = pd.to_numeric(df[c], errors="coerce") if c in df.columns else np.nan
    for c in TXT:
        if c not in df.columns:
            df[c] = ""
    df = df[df["lead_s"] > 0]
    df["akey"] = df["vehicle_id"] + "|" + df["stop_id"] + "|" + df["actual_epoch"].astype("int64").astype(str)
    return df


def sample(df, require="passio_epoch"):
    """One row per (arrival, goal bin): nearest the bin's sample point, among rows where `require` is present.
    -> DataFrame with a 'bin' column (bin name)."""
    have = df[df[require].notna()] if require else df
    parts = []
    for lo, hi, name, mid in GOAL_BINS:
        b = have[(have["lead_s"] >= lo) & (have["lead_s"] < hi)].copy()
        if b.empty:
            continue
        b["_d"] = (b["lead_s"] - mid).abs()
        b = b.sort_values(["akey", "_d", "query_epoch"]).drop_duplicates("akey", keep="first")
        b["bin"] = name
        parts.append(b.drop(columns="_d"))
    return pd.concat(parts, ignore_index=True) if parts else df.iloc[0:0].assign(bin="")


def load_sample(days, cache=None, require="passio_epoch"):
    """The evaluation sample of several days, concatenated."""
    return pd.concat([sample(load_day(d, cache), require) for d in days], ignore_index=True)


def load_all(cache=None, require="passio_epoch", refresh=False):
    """The evaluation sample of every cached day, kept in cache/sample-<first>-<last>.pkl so experiments start fast."""
    days = days_in(cache)
    if not days:
        raise SystemExit("no forecast tables in the cache: run fetch.py first")
    p = Path(cache or HERE / "cache") / f"sample-{days[0]}-{days[-1]}-{require or 'all'}.pkl"
    if p.exists() and not refresh:
        return pd.read_pickle(p)
    s = load_sample(days, cache, require)
    s.to_pickle(p)
    return s


def load_train_all(frac=0.25, seed=7, cache=None, refresh=False):
    """The TRAINING table: rows where Passio showed a time, at every query minute (a random `frac` of them per day),
    NOT picked by the true lead. Training on the scoreboard sample would let a model learn that the true lead sits at
    5 / 12.5 / 17.5 / 25 / 37.5 minutes and snap to it (a leak); real queries come at any minute. Cached as a pickle."""
    days = days_in(cache)
    p = Path(cache or HERE / "cache") / f"train-{days[0]}-{days[-1]}-{frac}-{seed}.pkl"
    if p.exists() and not refresh:
        return pd.read_pickle(p)
    rng = np.random.default_rng(seed)
    parts = []
    for d in days:
        df = load_day(d, cache)
        df = df[df["passio_epoch"].notna()]
        parts.append(df[rng.random(len(df)) < frac])
    t = pd.concat(parts, ignore_index=True)
    t["bin"] = ""          # no goal bin on training rows: it would come from the true lead
    t.to_pickle(p)
    return t
