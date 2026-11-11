#!/usr/bin/env python3
"""Asserts on scripts/sync.py (hermetic: a synthetic app-repo data branch and main in a temp folder). Run by sync.yml
before every rebuild, so a broken sync stops before it rewrites the public copy.
  python scripts/test_sync.py        -> prints 'ok N/N tests', exits 1 on failure"""
import csv, io, json, shutil, sys, tempfile, traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync as S

ARR = ("epoch,ts_utc,local_time,dow,hour,minute_of_day,route_id,route_name,trip_id,vehicle_id,stop_id,stop_name,"
       "stop_address,stop_lat,stop_lon,stop_index,prev_stop_id,dist_prev_m,prev_arrival_epoch,segment_s,speed_mps,"
       "dwell_s,passio_pred_epoch,passio_pred_lead_s,source").split(",")
PRED = ("epoch,local_time,route_id,route_name,trip_id,vehicle_id,stop_id,stop_name,stop_index,lead_target_s,"
        "pred_epoch,pred_made_epoch,pred_lead_s,pred_minus_actual_s,pred_seen_epoch").split(",")
TESTS = []


def test(fn):
    TESTS.append(fn)
    return fn


def row(epoch, local, route, veh, stop, idx, **kw):
    r = {c: "" for c in ARR}
    r.update(epoch=str(epoch), local_time=local, route_id="1077" if route == "East" else "1078", route_name=route,
             trip_id="T" + veh, vehicle_id=veh, stop_id=stop, stop_index=str(idx), segment_s="95", source="transition")
    r.update(kw)
    return r


def write(path, cols, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols, lineterminator="\n", extrasaction="ignore")
    w.writeheader()
    w.writerows(rows)
    path.write_text(buf.getvalue(), encoding="utf-8")


def setup(tmp):
    src, main, out = tmp / "src-data", tmp / "src-main", tmp / "out"
    gt = src / "data" / "ground_truth"
    old = [row(1792000000, "2026-10-13 15:46:40", "East", "V1", "S1", 1)]
    live = [row(1794300000, "2026-11-10 08:00:00", "East", "V1", "S2", 2),
            row(1794300100, "2026-11-10 08:01:40", "Central", "V2", "S3", 3),
            row(1794326400, "2026-11-11 01:20:00", "Central", "V2", "S4", 4)]          # night: Nov 10's service day
    write(gt / "archive" / "arrivals-20261020-0000.csv", ARR, old)
    write(gt / "arrivals.csv", ARR, live)
    preds = [dict({c: r.get(c, "") for c in PRED}, lead_target_s=str(t), pred_epoch=str(int(r["epoch"]) + 9))
             for r in old + live for t in (60, 300)]
    preds.append(dict(preds[0], epoch=str(int(preds[0]["epoch"]) + 4)))                   # a few seconds apart
    write(gt / "archive" / "predictions-20261029-2232.csv", PRED, preds)                     # sorts before arrivals
    (main / "web" / "data").mkdir(parents=True)
    (main / "web" / "data" / "routes.json").write_text("{}", encoding="utf-8")
    (main / "RouteKnower.md").write_text("plan\n", encoding="utf-8")
    out.mkdir()
    (out / "README.md").write_text("# copy\n<!-- SYNC:BEGIN -->\nold\n<!-- SYNC:END -->\n", encoding="utf-8")
    return src, main, out


def read(p):
    with open(p, encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        return r.fieldnames, list(r)


@test
def test_per_day_files_are_arrivals_only():
    tmp = Path(tempfile.mkdtemp(prefix="sync-test-"))
    try:
        src, main, out = setup(tmp)
        assert S.main(["--src-data", str(src), "--src-main", str(main), "--out", str(out)]) == 0
        files = sorted(p.relative_to(out / "data" / "arrivals").as_posix() for p in (out / "data" / "arrivals").rglob("*.csv"))
        assert files == ["2026-10-13/east.csv", "2026-11-10/central.csv", "2026-11-10/east.csv"], files
        for f in files:
            head, rows = read(out / "data" / "arrivals" / f)
            assert head == ARR, (f, head)                     # never the predictions header (DC-026)
            assert all(r["source"] == "transition" and r["segment_s"] == "95" for r in rows), rows
        assert len(read(out / "data" / "arrivals" / "2026-11-10" / "central.csv")[1]) == 2   # 1:20 AM stays with Nov 10
        idx = json.loads((out / "data" / "index.json").read_text(encoding="utf-8"))
        assert idx["rows"] == 4 and [d["day"] for d in idx["days"]] == ["2026-10-13", "2026-11-10"], idx
        assert read(out / "data" / "latest.csv")[0] == ARR
        assert (out / "methodology" / "RouteKnower.md").read_text(encoding="utf-8") == "plan\n"
        assert "2026-11-10 | 3" in (out / "README.md").read_text(encoding="utf-8")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


@test
def test_a_foreign_header_is_skipped_and_rerun_changes_nothing():
    tmp = Path(tempfile.mkdtemp(prefix="sync-test-"))
    try:
        src, main, out = setup(tmp)
        bad = src / "data" / "ground_truth" / "archive" / "arrivals-20261101-0000.csv"
        write(bad, PRED, [{"epoch": "1793000000", "local_time": "2026-10-25 05:00:00", "route_name": "East"}])
        S.main(["--src-data", str(src), "--src-main", str(main), "--out", str(out)])
        assert not (out / "data" / "arrivals" / "2026-10-25").exists()
        before = {p: p.read_bytes() for p in out.rglob("*") if p.is_file()}
        S.main(["--src-data", str(src), "--src-main", str(main), "--out", str(out)])
        after = {p: p.read_bytes() for p in out.rglob("*") if p.is_file()}
        assert before == after                                # write_if_changed: a rerun commits nothing
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    fails = 0
    for fn in TESTS:
        try:
            fn()
            print("pass", fn.__name__)
        except Exception:
            fails += 1
            print("FAIL", fn.__name__)
            traceback.print_exc()
    print(f"{'ok' if not fails else 'FAILED'} {len(TESTS) - fails}/{len(TESTS)} tests")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
