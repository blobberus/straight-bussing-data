"""The accuracy requirement as code (same definitions as the main repo: tools/arrivals_lib.py shrink_tol,
tools/build_eta_dataset.py GROSS / SUMMARY_BINS, docs/GOAL-AND-METHOD.md).

err = predicted - actual, in seconds. Positive = the prediction was LATER than the bus: the bus came early and a rider
who trusted it can miss it (the dangerous direction). Negative = the bus came later than shown (the rider waits).
"""
import numpy as np

# Goal bins (seconds ahead): (low, high, name, sample point). Under 10 minutes the goal counts each arrival ONCE, at the
# row nearest 5 minutes ahead (owner 2026-10-17: no gaming by always showing "1 min"); the other bins take the row
# nearest the bin middle (30-45 capped at 45 min, so 37.5 min).
GOAL_BINS = (
    (0, 600, "0-10", 300.0),
    (600, 900, "10-15", 750.0),
    (900, 1200, "15-20", 1050.0),
    (1200, 1800, "20-30", 1500.0),
    (1800, 2701, "30-45", 2250.0),
)
MOST = 0.5   # "most predictions" must pass


def shrink_tol(lead):
    """Allowed |error| (s) at a lead of `lead` seconds: 3 min at >= 30 min, 2 min at >= 20 min, else 1 min."""
    lead = np.asarray(lead, dtype=float)
    return np.where(lead >= 1800, 180.0, np.where(lead >= 1200, 120.0, 60.0))


def gross(err, lead):
    """A gross miss: off by more than 10 minutes or half the lead (E19 rule): left out of pass rates, still counted."""
    return np.abs(np.asarray(err, float)) > np.maximum(600.0, 0.5 * np.asarray(lead, float))


def score(err, lead):
    """Every number the goal talks about, for one bin. err, lead: arrays (s). -> dict (rates are 0..1)."""
    err, lead = np.asarray(err, float), np.asarray(lead, float)
    n = len(err)
    if not n:
        return {"n": 0}
    g = gross(err, lead)
    ok = ~g
    k = max(int(ok.sum()), 1)
    tol = shrink_tol(lead)
    e, L, t = err[ok], lead[ok], tol[ok]
    return {
        "n": n,
        "gross": float(g.mean()),
        "shrink": float((np.abs(e) <= t).sum() / k),             # within the allowed error, either way
        "band_b": float(((e >= -t) & (e <= 0.01 * L)).sum() / k),  # allowed error early .. 1% of the lead late (the goal)
        "ten_pct": float((np.abs(e) <= 0.10 * L).sum() / k),       # the older 10% rule, for comparison
        "too_late": float((err > 0.01 * lead).mean()),             # shown later than the bus came by > 1% of the lead
        "median_err_s": float(np.median(e)) if len(e) else float("nan"),
        "mae_s": float(np.mean(np.abs(e))) if len(e) else float("nan"),
    }


def meets(s):
    """The goal for one bin: most predictions inside band B."""
    return s.get("n", 0) > 0 and s["band_b"] >= MOST
