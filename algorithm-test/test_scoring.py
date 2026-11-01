#!/usr/bin/env python3
"""Tests for scoring.py: python algorithm-test/test_scoring.py"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scoring as S  # noqa: E402

tests = []
test = tests.append


@test
def allowed_error_steps_down_with_the_lead():
    assert list(S.shrink_tol([300, 1199, 1200, 1799, 1800, 2700])) == [60, 60, 120, 120, 180, 180]


@test
def gross_is_ten_minutes_or_half_the_lead():
    assert list(S.gross([599, 601, -1300, 1100], [300, 300, 2400, 2400])) == [False, True, True, False]


@test
def band_b_allows_early_up_to_the_allowed_error_but_late_only_one_percent():
    # at 25 min ahead: 2 min early passes, 15 s late passes (1% of 1500 s), 16 s late does not
    s = S.score([-120, 15, 16, -121], [1500] * 4)
    assert s["band_b"] == 0.5 and s["shrink"] == 0.75, s
    assert s["too_late"] == 0.5


@test
def gross_misses_leave_the_pass_rate_but_are_counted():
    s = S.score([0, 0, 2000], [300, 300, 300])
    assert s["gross"] == 1 / 3 and s["shrink"] == 1.0 and s["n"] == 3


@test
def most_means_at_least_half():
    assert S.meets({"n": 10, "band_b": 0.5}) and not S.meets({"n": 10, "band_b": 0.49}) and not S.meets({"n": 0})


@test
def bins_match_the_scoreboard():
    assert [b[2] for b in S.GOAL_BINS] == ["0-10", "10-15", "15-20", "20-30", "30-45"]
    assert [b[3] for b in S.GOAL_BINS] == [300.0, 750.0, 1050.0, 1500.0, 2250.0]


if __name__ == "__main__":
    bad = 0
    for t in tests:
        try:
            t()
            print("pass", t.__name__)
        except AssertionError as e:
            bad += 1
            print("FAIL", t.__name__, e)
    print("ok" if not bad else "FAILED", f"{len(tests) - bad}/{len(tests)}")
    sys.exit(1 if bad else 0)
