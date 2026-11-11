#!/usr/bin/env python3
"""Tests for flagged.py: the scope grammar turned into row masks, and the loses / holds verdict. Offline, no data.

  python algorithm-test/test_flagged.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import flagged as F  # noqa: E402

ROWS = pd.DataFrame({
    "route_id": ["5704", "5704", "5704", "5704", "5699", "5704"],
    "stop_id": ["A", "B", "A", "A", "A", "C"],
    "vehicle_id": ["1", "2", "1", "3", "1", "1"],
    "service_day": ["2026-11-06", "2026-11-06", "2026-11-07", "2026-11-08", "2026-11-06", "2026-11-09"],
    "hour": [8, 15, 23, 0, 15, 18],
    "dow": [4, 4, 5, 6, 4, 0],
    "lead_s": [300.0, 750.0, 1500.0, 2250.0, 300.0, 1050.0],
    "tt_epoch": [1.0, np.nan, 1.0, np.nan, 1.0, 1.0],
})


def mask(scope, rid="5704"):
    m, skipped = F.slice_mask(ROWS, rid, scope)
    return list(np.flatnonzero(m)), skipped


def test_scope_filters():
    assert mask("") == ([0, 1, 2, 3, 5], [])
    assert mask("all") == ([0, 1, 2, 3, 5], [])
    assert mask("", "5699") == ([4], [])
    assert mask("stops=A") == ([0, 2, 3], [])
    assert mask("stops=A|C;vehicles=1") == ([0, 2, 5], [])
    assert mask("hours=15-19") == ([1, 5], [])
    assert mask("hours=23-01") == ([2, 3], [])                  # wraps past midnight
    assert mask("hours=8-9|18-19") == ([0, 5], [])
    assert mask("days=weekday") == ([0, 1, 5], [])
    assert mask("days=weekend") == ([2, 3], [])
    assert mask("days=sunday") == ([3], [])
    assert mask("days=mon") == ([5], [])
    assert mask("lead=10-30") == ([1, 2, 5], [])
    assert mask("trips=no_timetable") == ([1, 3], [])
    assert mask("trips=timetable") == ([0, 2, 5], [])
    assert mask("dates=2026-11-06|2026-11-09") == ([0, 1, 5], [])


def test_text_is_not_applied():
    rows, skipped = mask("note=downtown loop;Reynolds Club;color=red;stops=A")
    assert rows == [0, 2, 3] and skipped == ["note=downtown loop", "Reynolds Club", "color=red"], (rows, skipped)


def test_verdict():
    s = lambda bb, tl, n=100: {"band_b": bb, "too_late": tl, "n": n}
    sc = {"passio": {"0-10": s(0.20, 0.05), "10-15": s(0.10, 0.05)},
          "good": {"0-10": s(0.25, 0.05), "10-15": s(0.095, 0.055)},
          "worse_b": {"0-10": s(0.17, 0.05), "10-15": s(0.10, 0.05)},
          "later": {"0-10": s(0.30, 0.07), "10-15": s(0.12, 0.05)},
          "thin": {"0-10": s(0.01, 0.50, n=29)}}
    sc["thin"]["10-15"] = s(0.01, 0.5, n=10)
    assert F.verdict(sc, "passio")[0] == "reference"
    assert F.verdict(sc, "good") == ("holds", [])
    v, why = F.verdict(sc, "worse_b")
    assert v == "loses" and "band B 17.0% vs Passio 20.0% at 0-10 min" in why[0], why
    v, why = F.verdict(sc, "later")
    assert v == "loses" and "too late 7.0% vs Passio 5.0%" in why[0], why
    assert F.verdict(sc, "thin") == ("too few rows", [])


if __name__ == "__main__":
    n = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            n += 1
            print(f"ok   {name}")
    print(f"{n}/{n} passed")
