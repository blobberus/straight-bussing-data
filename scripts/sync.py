#!/usr/bin/env python3
"""Mirror the shuttle data and the RouteKnower methodology from github.com/blobberus/straight-bussing into this
repository. Run every 30 minutes by .github/workflows/sync.yml (public source, no token needed). Stdlib only.

  python scripts/sync.py --src-data <clone of the 'data' branch> --src-main <clone of 'main'> --out .

Writes (only files whose content changed are rewritten, so git records real changes only):
  data/arrivals/<service-day>/<route>.csv  one file per service day and route (GitHub shows files < 512 KB as a table);
                                           a service day runs 4:00 AM to 3:59 AM Chicago time, so night routes stay
                                           with the evening they started
  data/latest.csv                          the newest 200 arrivals (all routes)
  data/index.json                          days, routes, counts, newest arrival, sync time (used by index.html)
  data/network/{routes,stops,route_stops}.json   route colors, stop names and stop order (from the app's GTFS data)
  methodology/                             RouteKnower.md, experiments/routeknower/**, docs DATA / DATA-GUIDE / GOAL-AND-METHOD / ALGORITHMS / BACKTEST
  README.md                                the summary block between the SYNC markers
The source of truth stays in the app repo: edit methodology there; this copy follows within the hour.
"""
import argparse, csv, io, json, re, shutil
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

SOURCE = "https://github.com/blobberus/straight-bussing"
KEY = ("vehicle_id", "trip_id", "stop_id", "stop_index", "epoch")
METHODOLOGY = ["RouteKnower.md", "experiments/routeknower", "docs/DATA.md", "docs/DATA-GUIDE.md", "docs/GOAL-AND-METHOD.md", "docs/ALGORITHMS.md", "docs/BACKTEST.md"]
NETWORK = ["routes.json", "stops.json", "route_stops.json"]
CUTOFF_HOUR = 4


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "unknown").lower()).strip("-") or "unknown"


def service_day(local_time):
    """'2026-10-09 01:12:00' -> '2026-10-08' (before 4 AM belongs to the previous evening's service)."""
    try:
        t = datetime.strptime(local_time[:19], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return local_time[:10] or "unknown"
    return (t - timedelta(days=1)).strftime("%Y-%m-%d") if t.hour < CUTOFF_HOUR else t.strftime("%Y-%m-%d")


def read_rows(src_data):
    gt = Path(src_data) / "data" / "ground_truth"
    files = sorted((gt / "archive").glob("*.csv")) + [gt / "arrivals.csv"]
    header, rows, seen = None, [], set()
    for f in files:
        if not f.exists():
            continue
        with open(f, newline="", encoding="utf-8") as fh:
            r = csv.DictReader(fh)
            header = header or r.fieldnames
            for row in r:
                k = tuple(row.get(c, "") for c in KEY)
                if k in seen or not row.get("epoch"):
                    continue
                seen.add(k)
                rows.append(row)
    rows.sort(key=lambda x: float(x["epoch"]))
    return header or [], rows


def write_if_changed(path, text):
    path = Path(path)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return True


def to_csv(header, rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=header, extrasaction="ignore", lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def copy_tree_if_changed(src, dst):
    changed = 0
    src = Path(src)
    items = [src] if src.is_file() else [p for p in src.rglob("*") if p.is_file()]
    for p in items:
        rel = p.name if src.is_file() else p.relative_to(src)
        target = Path(dst) / rel
        data = p.read_bytes()
        if target.exists() and target.read_bytes() == data:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        changed += 1
    return changed


def readme_block(idx):
    days = idx["days"][-14:][::-1]
    lines = [f"_Last sync: {idx['synced']} UTC · {idx['rows']:,} arrivals · {len(idx['days'])} service days · "
             f"newest arrival {idx['newest'] or 'none yet'} (Chicago time)_", "",
             "| Service day | Arrivals | Routes | Files |", "|---|---:|---:|---|"]
    for d in days:
        lines.append(f"| {d['day']} | {d['rows']:,} | {len(d['routes'])} | [data/arrivals/{d['day']}/](data/arrivals/{d['day']}) |")
    if days:
        latest = days[0]
        lines += ["", f"Routes on {latest['day']}:", "", "| Route | Arrivals | File |", "|---|---:|---|"]
        for name, r in sorted(latest["routes"].items(), key=lambda kv: -kv[1]["rows"]):
            lines.append(f"| {name} | {r['rows']:,} | [{Path(r['file']).name}]({r['file']}) |")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src-data", required=True)
    ap.add_argument("--src-main", required=True)
    ap.add_argument("--out", default=".")
    a = ap.parse_args(argv)
    out = Path(a.out)
    header, rows = read_rows(a.src_data)
    by = defaultdict(lambda: defaultdict(list))
    for r in rows:
        by[service_day(r.get("local_time", ""))][r.get("route_name") or r.get("route_id") or "unknown"].append(r)
    changed, days = 0, []
    for day in sorted(by):
        entry = {"day": day, "rows": 0, "routes": {}}
        for route, rs in sorted(by[day].items()):
            f = f"data/arrivals/{day}/{slug(route)}.csv"
            changed += write_if_changed(out / f, to_csv(header, rs))
            entry["routes"][route] = {"file": f, "rows": len(rs), "route_id": rs[0].get("route_id", "")}
            entry["rows"] += len(rs)
        days.append(entry)
    changed += write_if_changed(out / "data/latest.csv", to_csv(header, rows[-200:]))
    for name in NETWORK:
        src = Path(a.src_main) / "web" / "data" / name
        if src.exists():
            changed += write_if_changed(out / "data/network" / name, src.read_text(encoding="utf-8"))
    for rel in METHODOLOGY:
        src = Path(a.src_main) / rel
        if src.exists():
            dst = out / "methodology" / (rel if src.is_dir() else rel)
            changed += copy_tree_if_changed(src, dst if src.is_dir() else dst.parent)
    idx = {"synced": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"), "source": SOURCE, "rows": len(rows),
           "newest": rows[-1].get("local_time", "") if rows else "", "cutoff_hour": CUTOFF_HOUR, "days": days}
    # index.json changes every run (sync time); only rewrite it when the data itself changed or it is missing
    if changed or not (out / "data/index.json").exists():
        write_if_changed(out / "data/index.json", json.dumps(idx, indent=1))
        readme = out / "README.md"
        text = readme.read_text(encoding="utf-8") if readme.exists() else ""
        block = "<!-- SYNC:BEGIN -->\n" + readme_block(idx) + "\n<!-- SYNC:END -->"
        text = re.sub(r"<!-- SYNC:BEGIN -->.*?<!-- SYNC:END -->", lambda m: block, text, flags=re.S) if "<!-- SYNC:BEGIN -->" in text else text + "\n" + block + "\n"
        write_if_changed(readme, text)
    print(f"{len(rows)} arrivals, {len(days)} service days, {changed} files changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
