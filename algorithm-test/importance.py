#!/usr/bin/env python3
"""Which inputs does the specialized model lean on? Fit gbm_q15 on every day before the last N test days, then for each
input shuffle that column in the test rows and measure how much band B (the goal) drops. A large drop = the model needs
that input; near zero = it adds nothing. Split counts from the trees are listed too (a rougher measure).

  python algorithm-test/importance.py [--test-days 5] [--out results/08-feature-importance]
"""
import argparse, sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dataset as D       # noqa: E402
import features as F      # noqa: E402
import models as M        # noqa: E402
import scoring as S       # noqa: E402

NAMES = F.NUMERIC + ["route (target-encoded lateness)", "stop (target-encoded lateness)"]
PLAIN = {
    "lead_passio": "Passio's predicted minutes ahead", "lead_tt": "timetable minutes ahead",
    "lead_ttd": "timetable + current delay, minutes ahead", "tt_minus_passio": "timetable time minus Passio's time",
    "passio_age_s": "age of Passio's prediction", "stops_away": "stops between the bus and the stop",
    "dist_m": "distance along the route", "delay_s": "bus's current delay against the timetable",
    "standing_s": "how long the bus has stood still", "speed_mps": "bus speed", "last_age_s": "age of the last GPS report",
    "next_trip": "arrival is on the bus's next trip", "crosses_terminal": "bus passes the end of the line first",
    "visit_rank": "which visit of the stop on a loop", "stop_index": "position of the stop on the trip",
    "hour_sin": "time of day (sine)", "hour_cos": "time of day (cosine)", "weekend": "weekend",
    NAMES[-2]: "how much later than Passio this route usually comes", NAMES[-1]: "how much later than Passio this stop usually comes",
}


def band(pred, s):
    sc = S.score(pred - s["actual_epoch"].to_numpy(float), s["lead_s"].to_numpy(float))
    return sc["band_b"], sc["too_late"]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--test-days", type=int, default=5)
    ap.add_argument("--out", default="results/08-feature-importance")
    a = ap.parse_args(argv)
    sample, train_all = D.load_all(), D.load_train_all()
    days = sorted(sample["service_day"].unique())
    test_days = days[-a.test_days:]
    test = sample[sample["service_day"].isin(test_days)]
    m = M.GBMQ15().fit(train_all[train_all["service_day"] < test_days[0]])
    X = m._matrix(test)
    passio = test["passio_epoch"].to_numpy(float)
    base_b, base_l = band(passio + m.model.predict(X), test)
    ref_b, ref_l = band(passio, test)
    rng = np.random.default_rng(7)
    splits = m.model.importance()
    rows = []
    for j, name in enumerate(NAMES):
        Xp = X.copy()
        Xp[:, j] = Xp[rng.permutation(len(Xp)), j]
        b, l = band(passio + m.model.predict(Xp), test)
        rows.append((base_b - b, l - base_l, splits.get(j, 0), name))
        print(f"  {name}: band B -{100 * (base_b - b):.2f} pts", file=sys.stderr)
    rows.sort(key=lambda r: -r[0])
    total_splits = max(sum(splits.values()), 1)
    lines = ["# Feature importance: what the specialized model (gbm_q15) leans on", "",
             f"Fitted on {days[0]} to {days[days.index(test_days[0]) - 1]}, tested on {test_days[0]} to {test_days[-1]} "
             f"({len(test):,} samples, all goal bins pooled). Band B: gbm_q15 {100 * base_b:.1f}% (too late {100 * base_l:.1f}%), "
             f"Passio {100 * ref_b:.1f}% (too late {100 * ref_l:.1f}%).", "",
             "Shuffling an input breaks its link to the answer; the drop in band B is what the model loses without it.", "",
             "| input | what it is | band B drop when shuffled | too late change | share of tree splits |",
             "|---|---|---:|---:|---:|"]
    for db, dl, sp, name in rows:
        lines.append(f"| {name} | {PLAIN.get(name, '')} | {100 * db:+.2f} pts | {100 * dl:+.2f} pts | {100 * sp / total_splits:.0f}% |")
    md = "\n".join(lines) + "\n"
    print(md)
    (HERE / a.out).with_suffix(".md").write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()
