#!/usr/bin/env python3
"""Download the public forecast tables (eta-<day>.csv.gz) from the main repo's releases into a local cache.

  python algorithm-test/fetch.py [--from 2026-10-12] [--to 2026-10-31] [--cache algorithm-test/cache]

Each service day is one file on the release data-archive-YYYY-MM of github.com/blobberus/straight-bussing (built by
tools/archive_day.py there). No login needed. Days that are missing (not archived yet) are skipped. Stdlib only.
"""
import argparse, sys, urllib.error, urllib.request
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = "https://github.com/blobberus/straight-bussing/releases/download"
FIRST_PASSIO_DAY = "2026-10-12"   # Passio's predictions are recorded from 2026-10-12 12:20 PM Chicago


def url_for(day):
    return f"{BASE}/data-archive-{day[:7]}/eta-{day}.csv.gz"


def days(a, b):
    d, end = date.fromisoformat(a), date.fromisoformat(b)
    while d <= end:
        yield d.isoformat()
        d += timedelta(days=1)


def fetch(day, cache):
    out = Path(cache) / f"eta-{day}.csv.gz"
    if out.exists() and out.stat().st_size > 0:
        return out
    try:
        with urllib.request.urlopen(url_for(day), timeout=120) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".part")
    tmp.write_bytes(data)
    tmp.replace(out)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--from", dest="start", default=FIRST_PASSIO_DAY)
    ap.add_argument("--to", dest="end", default=(date.today() - timedelta(days=1)).isoformat())
    ap.add_argument("--cache", default=str(HERE / "cache"))
    a = ap.parse_args(argv)
    got = 0
    for d in days(a.start, a.end):
        p = fetch(d, a.cache)
        print(f"{d}: {'missing' if p is None else p.name}", file=sys.stderr)
        got += p is not None
    print(f"{got} day(s) in {a.cache}", file=sys.stderr)


if __name__ == "__main__":
    main()
