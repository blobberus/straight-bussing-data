#!/usr/bin/env python3
"""Rebuild every result in order: fetch the data, run the checks, then each experiment (01, 03 to 13) into results/.

  python algorithm-test/run_all.py            everything (about an hour on a laptop CPU; the deep models take most of it)
  python algorithm-test/run_all.py --only 07  one step (its number)
  python algorithm-test/run_all.py --checks   only the tests and the scoreboard check

Stops at the first failing step. 02 is not rerun: it is kept only as the record of a leaky first try. The committed
results used October 12 to 30, 2026; fetch takes every day through yesterday, so a fresh run uses more days and its numbers
move (pass --to 2026-10-30 with an empty cache to reproduce them).
"""
import argparse, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

CHECKS = [
    ("fetch", ["fetch.py"]),
    ("scoring tests", ["test_scoring.py"]),
    ("tree tests", ["test_gbm.py"]),
    ("scoreboard check", ["validate.py"]),
    ("leak guard", ["test_leak.py"]),
    ("flagged-slice tests", ["test_flagged.py"]),
]
STEPS = [
    ("01", ["evaluate.py", "--models", "passio,timetable,timetable_delay", "--out", "results/01-baselines",
            "--title", "Baselines against the accuracy requirement"]),
    ("03", ["evaluate.py", "--models", "passio,shift_window,gbm_q15,gbm_q30", "--out", "results/03-learned-fixed",
            "--title", "Learned models after the leak fixes: per-stop correction and boosted trees"]),
    ("04", ["evaluate.py", "--models", "passio,gbm_q15,deep_q15,gbm_q30,deep_q30", "--out", "results/04-trees-vs-deep",
            "--title", "Individual algorithm (boosted trees) vs deep learning (neural network), same rows"]),
    ("05", ["evaluate.py", "--models", "passio,gbm_q15,deep_q15", "--by-route", "--out", "results/05-by-route",
            "--title", "Per route: boosted trees and the network at the 15% quantile"]),
    ("06", ["learning_curve.py"]),
    ("07", ["lateness.py"]),
    ("08", ["importance.py"]),
    ("09", ["ceiling.py"]),
    ("10", ["e24_leak_check.py"]),
    ("11", ["evaluate.py", "--models", "passio,deep_q15,deep_safe", "--out", "results/11-safe-setting",
            "--title", "A network tuned to the ship gate's safety rule: never too late more often than Passio"]),
    ("12", ["transitions.py"]),
    ("13", ["flagged.py"]),           # every model on each flagged line (main repo data/labeled/flags/)
]


def run(label, args):
    print(f"== {label}: python {' '.join(args)}", flush=True)
    r = subprocess.run([sys.executable, str(HERE / args[0]), *args[1:]], cwd=HERE)
    if r.returncode:
        sys.exit(f"{label} failed (exit {r.returncode})")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--only", help="run one experiment step by its number, e.g. 07")
    ap.add_argument("--checks", action="store_true", help="run only the data fetch, tests and scoreboard check")
    ap.add_argument("--to", help="last service day to fetch (default: yesterday)")
    a = ap.parse_args(argv)
    if a.to:
        CHECKS[0] = ("fetch", ["fetch.py", "--to", a.to])
    if a.only:
        steps = [s for s in STEPS if s[0] == a.only]
        if not steps:
            sys.exit(f"no step {a.only}; steps: {', '.join(s[0] for s in STEPS)}")
        for s in steps:
            run(*s)
        return
    for c in CHECKS:
        run(*c)
    if not a.checks:
        for s in STEPS:
            run(*s)


if __name__ == "__main__":
    main()
