#!/usr/bin/env python3
"""Weekly findings refresh (owner, 2026-11-06: "retry which bus will leave after applicable intervals of new data
collected and revise it. Give me an updating xlsx file to reference for other agents"). Run by
.github/workflows/findings.yml every week and by hand; read-only on the app repo and its data branch.

Each run:
 1. fetches every archived service day from the app repo's releases (`data-archive-YYYY-MM`: raw-polls, pred-updates,
    gtfs; only days whose raw polls are archived) into --dl (kept between runs by the workflow cache), plus the data
    branch's arrivals.csv / alerts.csv / bus_changes.csv;
 2. reruns the app repo's own scripts on all of it (read-only checkout, --live): RouteKnower E29
    `experiments/routeknower/E29-scripts/transitions.py` (every bus count transition, labeled) and E28
    `experiments/routeknower/E28-scripts/endofservice.py` (where buses linger at the end of a trip or shift);
 3. re-evaluates "which bus will leave" with an EXPANDING window (`transition_rules.py --train-to <last day - 7>`: train
    on every day up to 7 days before the newest, test on the newest 7 days, nothing of the test days seen in training)
    and re-learns the leave windows;
 4. appends one row per signal to findings/leave_eval_history.csv and decides READINESS (below); a ready signal writes
    findings/leave_ready.md, which the workflow turns into ONE issue "Leave prediction ready for review". Nothing here
    changes the app: shipping a leave rule stays a reviewed change (app repo RouteKnower.md E29, "Retry procedure");
 5. refreshes the FLAGGED LINES (owner, 2026-11-11: "Create or indicate wherever appropriate for another agent to analyze
    and notice and account for this data. Flag these lines"): reruns RouteKnower E30 (odd bus behavior at transition
    times: `E30-scripts/run_odd.py` + `flags.py`) and E31 (large prediction misses: `E31-scripts/misses.py` +
    `flags.py`) on the same days, keeps the app repo's reviewed copy of any producer file it cannot rerun (E32's display
    flags need a browser) or whose rerun fails, and merges them with the app repo's `tools/flag_lines.py` into
    findings/csv/flagged_lines.csv + findings/FLAGGED-LINES.md (first_flagged kept from last week's copy; a flag no
    longer reported becomes resolved); the rerun producer files go to findings/flags/ for the app repo to adopt. Nothing is written to the app repo: its data/labeled/flags/ stays the reviewed copy;
 6. rebuilds findings/straight-bussing-findings.xlsx and its CSV copies in findings/csv/ (build_workbook.py; the
    flagged_lines tab comes first);
 7. refreshes the HIDDEN BUSES (owner, 2026-11-11: "Keep hidden bus times off until it reports again. If passio is
    still reporting them, add them to a hidden bus file in the data"): replays every archived day through the app
    repo's own display code (RouteKnower E32 `inputs.py` + `replay.py` in headless Edge, no planner samples) and writes
    findings/hidden_buses/hidden_buses.csv with `hidden_buses.py` (the app repo's reviewed copy is
    data/labeled/hidden_buses/). Skipped, with the reason in last_run.json, when the scripts or a browser are missing
    or a one-day smoke replay fails; capped at HIDDEN_BUDGET_S so it can never take the rest of the run down.

READY (a signal, all must hold): the data reaches READY_MIN_DATA_TO (3 weeks past the first evaluation's
2026-11-05); held-out precision >= 0.90 AND recall >= 0.20 on >= 30 flagged visits; precision on the training days
>= 0.85 (it held in-sample too, not a lucky week); and the same was true in the previous run on an earlier week of data
(data at least 5 days older; a rerun on the same days never counts twice), so 2 consecutive weeks.
Why: E25 asked 90% at 15 min; a rule that flags a bus serving the rider's ride must be rare (rider safety first); 30
visits keep a 90% estimate's 95% interval above about 75%; 20% recall is the least that changes what riders see.

  python findings/run_findings.py --live <app repo checkout> --src-data <app repo data-branch checkout> \
      --dl <download cache> --out findings [--work <scratch>] [--skip-fetch] [--skip-eos] [--skip-flags]
      [--eta-dir <folder of eta-<day>.csv.gz for E31; default --dl>] [--skip-hidden]
"""
import argparse, csv, json, os, shutil, subprocess, sys, time, urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = "blobberus/straight-bussing"
FIRST_DAY = "2026-10-10"
TEST_DAYS = 7
READY_MIN_DATA_TO = "2026-11-26"
READY_PRECISION, READY_RECALL, READY_MIN_FLAGGED, READY_TRAIN_PRECISION = 0.90, 0.20, 30, 0.85
HISTORY_COLS = ["run_utc", "data_from", "data_to", "days", "train_to", "test_from", "test_to", "signal", "kind",
                "test_flagged", "test_hits", "test_precision", "test_recall", "train_flagged", "train_precision",
                "train_recall", "test_visits_base_rate", "meets_criteria", "consecutive_runs", "ready", "note"]
KINDS = ("raw-polls-{}.jsonl.gz", "pred-updates-{}.jsonl.gz", "gtfs-{}.zip", "eta-{}.csv.gz")   # eta: E31 features
FLAG_FILES = {"transition": "transition_flags.csv", "prediction_miss": "prediction_flags.csv", "display": "display_flags.csv"}
E32 = "experiments/routeknower/E32-scripts"
HIDDEN_BUDGET_S = 45 * 60      # the whole hidden-bus replay (inputs + replay of every day) stops after this


def log(*a):
    print(*a, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- 1. inputs
def api(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    tok = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def archived_assets():
    """{asset name: download URL} of every data-archive release of the app repo."""
    out = {}
    for rel in api(f"https://api.github.com/repos/{REPO}/releases?per_page=100"):
        if not str(rel.get("tag_name", "")).startswith("data-archive-"):
            continue
        page = 1
        while True:
            got = api(f"https://api.github.com/repos/{REPO}/releases/{rel['id']}/assets?per_page=100&page={page}")
            for a in got:
                out[a["name"]] = a["browser_download_url"]
            if len(got) < 100:
                break
            page += 1
    return out


def download(url, dest):
    tmp = dest.with_suffix(dest.suffix + ".part")
    for i in range(4):
        try:
            with urllib.request.urlopen(url, timeout=180) as r:
                tmp.write_bytes(r.read())
            tmp.replace(dest)
            return
        except OSError as ex:
            log(f"  retry {dest.name}: {ex}")
            time.sleep(5 * (i + 1))
    raise SystemExit(f"could not download {url}")


def fetch(dl, src_data):
    """Archived days into dl (files already there are kept), the data branch's CSVs copied. -> sorted days."""
    dl.mkdir(parents=True, exist_ok=True)
    assets = archived_assets()
    days = sorted(n[10:20] for n in assets if n.startswith("raw-polls-") and n[10:20] >= FIRST_DAY)
    got = 0
    for d in days:
        for k in KINDS:
            n = k.format(d)
            if n in assets and not (dl / n).exists():
                download(assets[n], dl / n)
                got += 1
    gt = Path(src_data) / "data" / "ground_truth"
    for f in ("arrivals.csv", "alerts.csv", "bus_changes.csv", "predictions.csv"):
        shutil.copy2(gt / f, dl / f)
    for p in sorted((gt / "archive").glob("predictions-*.csv")):    # older predictions (E30, E31), oldest first
        shutil.copy2(p, dl / p.name)
    log(f"fetch: {len(days)} archived days, {got} new files")
    return days


# ---------------------------------------------------------------- 2-3. the app repo's scripts
def run(live, script, *args):
    cmd = [sys.executable, str(Path(live) / script), *map(str, args)]
    log("$", " ".join(cmd))
    r = subprocess.run(cmd, cwd=live)
    if r.returncode:
        raise RuntimeError(f"{script} failed ({r.returncode})")


# ---------------------------------------------------------------- 4. history and readiness
def read_history(path):
    if not path.exists():
        return []
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def history_rows(res, days, train_to, run_utc, prev):
    """One row per leave signal (and one for the shipped gone rule) from transition_rules.py's JSON."""
    A = res["A_about_to_leave"]
    test_days = A.get("test_days") or []
    last_ok = {}
    cutoff = (date.fromisoformat(days[-1]) - timedelta(days=5)).isoformat()
    earlier = [r for r in prev if r.get("data_to", "") <= cutoff]      # a run on an earlier week of data (reruns of
    if earlier:                                                        # the same week never count twice)
        last_run = max(r["run_utc"] for r in earlier)
        last_ok = {r["signal"]: r for r in earlier if r["run_utc"] == last_run}
    rows = []
    for sig, sc in A["rules"].items():
        te, tr = sc["test"], sc["train"]
        meets = bool(days[-1] >= READY_MIN_DATA_TO and (te["precision"] or 0) >= READY_PRECISION
                     and te["recall"] >= READY_RECALL and te["flagged"] >= READY_MIN_FLAGGED
                     and (tr["precision"] or 0) >= READY_TRAIN_PRECISION)
        p = last_ok.get(sig)
        consec = (int(p["consecutive_runs"]) + 1 if p and p.get("meets_criteria") == "1" else 1) if meets else 0
        rows.append({"run_utc": run_utc, "data_from": days[0], "data_to": days[-1], "days": len(days), "train_to": train_to,
                     "test_from": test_days[0] if test_days else "", "test_to": test_days[-1] if test_days else "",
                     "signal": sig, "kind": "about_to_leave", "test_flagged": te["flagged"], "test_hits": te["leave"],
                     "test_precision": "" if te["precision"] is None else te["precision"], "test_recall": te["recall"],
                     "train_flagged": tr["flagged"], "train_precision": "" if tr["precision"] is None else tr["precision"],
                     "train_recall": tr["recall"], "test_visits_base_rate": A["base_rate"], "meets_criteria": int(meets),
                     "consecutive_runs": consec, "ready": int(consec >= 2), "note": ""})
    top = A.get("network_top_k_precision")
    if isinstance(top, dict):
        rows.append({"run_utc": run_utc, "data_from": days[0], "data_to": days[-1], "days": len(days), "train_to": train_to,
                     "test_from": test_days[0] if test_days else "", "test_to": test_days[-1] if test_days else "",
                     "signal": "small_network_top20", "kind": "about_to_leave", "test_flagged": 20,
                     "test_precision": top["test"].get("20", ""), "train_flagged": 20,
                     "train_precision": top["train"].get("20", ""), "meets_criteria": 0, "consecutive_runs": 0,
                     "ready": 0, "note": "top-k only (no threshold); never qualifies by itself"})
    g = res["B_gone"]
    gt, gr = g.get("test", {}).get("15min_feed_alive_regular", {}), g.get("train", {}).get("15min_feed_alive_regular", {})
    rows.append({"run_utc": run_utc, "data_from": days[0], "data_to": days[-1], "days": len(days), "train_to": train_to,
                 "test_from": test_days[0] if test_days else "", "test_to": test_days[-1] if test_days else "",
                 "signal": "gone_15min_feed_alive_regular (shipped)", "kind": "gone_rule",
                 "test_flagged": gt.get("prediction_minutes_dropped", ""), "test_precision": gt.get("never_served", ""),
                 "train_flagged": gr.get("prediction_minutes_dropped", ""), "train_precision": gr.get("never_served", ""),
                 "meets_criteria": "", "consecutive_runs": "", "ready": "",
                 "note": "flagged = prediction-minutes dropped; precision = share that never came true (web/js/core/transition.js)"})
    return rows


def write_history(path, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HISTORY_COLS, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in HISTORY_COLS})


def ready_text(rows):
    ready = [r for r in rows if str(r.get("ready")) == "1"]
    if not ready:
        return None
    lines = ["Automatic weekly re-evaluation (data repo `findings/run_findings.py`, workflow `findings.yml`): these "
             "\"which bus will leave\" signals met the readiness rule two runs in a row (held-out precision >= 90%, recall "
             ">= 20%, >= 30 flagged visits, training precision >= 85%, data through " + READY_MIN_DATA_TO + " or later).",
             "", "| signal | data | test days | flagged | precision | recall | train precision |", "|---|---|---|---:|---:|---:|---:|"]
    for r in ready:
        lines.append(f"| {r['signal']} | {r['data_from']} to {r['data_to']} | {r['test_from']} to {r['test_to']} | "
                     f"{r['test_flagged']} | {float(r['test_precision']):.1%} | {float(r['test_recall']):.1%} | "
                     f"{float(r['train_precision']):.1%} |")
    lines += ["", "Nothing changed in the app. To review and ship, follow the app repo's RouteKnower.md E29 "
              "\"Retry procedure\" (rerun the evaluation locally, port the rule to web core + Kit with golden tests, "
              "owner review). History: `findings/leave_eval_history.csv`, workbook `findings/straight-bussing-findings.xlsx`."]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- 5. flagged lines
def refresh_flags(live, dl, tdir, eos, work, out, days, eta_dir=None):
    """Reruns the flag producers (E30, E31) into work/flags, keeps the app repo's reviewed copy of every producer file
    not rerun (or whose rerun failed), and merges them into out/csv/flagged_lines.csv + out/FLAGGED-LINES.md with the
    app repo's tools/flag_lines.py. -> {"refreshed": [...], "kept": [...], "failed": {category: error}, "active": n}, or None
    when the merge itself failed (the workbook then shows the app repo's registry)."""
    fdir = work / "flags"
    if fdir.exists():
        shutil.rmtree(fdir)
    fdir.mkdir(parents=True)
    app = Path(live) / "data" / "labeled" / "flags"
    for f in FLAG_FILES.values():                          # each producer's previous file (its own first_flagged)
        if (app / f).exists():
            shutil.copy2(app / f, fdir / f)
    res = {"refreshed": [], "kept": [], "failed": {}}
    e30 = work / "e30"
    try:                                                   # E30: odd bus behavior at transition times
        run(live, "experiments/routeknower/E30-scripts/run_odd.py", "--dl", dl, "--e28", eos, "--transitions",
            tdir / "transitions.csv", "--out", tdir, "--work", e30 / "days", "--json", e30 / "e30.json")
        run(live, "experiments/routeknower/E30-scripts/flags.py", "--tables", tdir, "--json", e30 / "e30.json",
            "--out", fdir / FLAG_FILES["transition"])
        res["refreshed"].append("transition")
    except (RuntimeError, OSError) as ex:
        res["failed"]["transition"] = str(ex)
        log(f"E30 flags not refreshed (the app repo's copy is kept): {ex}")
    e31 = work / "e31"
    try:                                                   # E31: lines with large prediction misses
        preds = sorted(Path(dl).glob("predictions-*.csv")) + [Path(dl) / "predictions.csv"]
        run(live, "experiments/routeknower/E31-scripts/misses.py", "--predictions", *preds, "--arrivals",
            Path(dl) / "arrivals.csv", "--eta-dir", eta_dir or dl, "--pred-updates", dl, "--bus-changes",
            Path(dl) / "bus_changes.csv", "--transitions", tdir / "transitions.csv", "--to", days[-1], "--out", e31)
        run(live, "experiments/routeknower/E31-scripts/flags.py", "--tables", e31, "--out",
            fdir / FLAG_FILES["prediction_miss"])
        res["refreshed"].append("prediction_miss")
    except (RuntimeError, OSError) as ex:
        res["failed"]["prediction_miss"] = str(ex)
        log(f"E31 flags not refreshed (the app repo's copy is kept): {ex}")
    res["kept"] = [c for c, f in FLAG_FILES.items() if c not in res["refreshed"] and (fdir / f).exists()]
    reg = Path(out) / "csv" / "flagged_lines.csv"
    prev = reg if reg.exists() else app / "flagged_lines.csv"
    try:
        run(live, "tools/flag_lines.py", "--flags-dir", fdir, "--prev", prev, "--out", work / "flagged_lines.csv",
            "--md", work / "FLAGGED-LINES.md")
    except RuntimeError as ex:
        log(f"flagged lines not merged (the workbook keeps the app repo's registry): {ex}")
        return None
    reg.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(work / "flagged_lines.csv", reg)
    pub = Path(out) / "flags"                              # this run's producer files, for the app repo to adopt
    pub.mkdir(parents=True, exist_ok=True)
    for c, f in FLAG_FILES.items():
        if c in res["refreshed"]:
            shutil.copy2(fdir / f, pub / f)
        elif (pub / f).exists():                           # never leave last week's file looking fresh
            (pub / f).unlink()
    head, _, body = (work / "FLAGGED-LINES.md").read_text(encoding="utf-8").partition("\n")
    note = (f"> **Weekly refresh** ({datetime.now(timezone.utc):%Y-%m-%d}) by `findings/run_findings.py` in this repo. "
            f"Rerun on the archived days: {', '.join(res['refreshed']) or 'none'}; kept from the app repo: "
            f"{', '.join(res['kept']) or 'none'}. Machine-readable copy: `findings/csv/flagged_lines.csv` (the workbook's "
            "first tab); the rerun producer files are in `findings/flags/` (to adopt them in the app repo: copy them "
            "into its `data/labeled/flags/`, run `python tools/flag_lines.py`, review the new and resolved flags, commit). "
            "The paths below name the app repo, whose `data/labeled/flags/` is the reviewed copy and whose README there "
            "says what every agent must do about a flag.\n")
    with open(Path(out) / "FLAGGED-LINES.md", "w", encoding="utf-8", newline="") as f:
        f.write(head + "\n\n" + note + body)
    with open(reg, encoding="utf-8", newline="") as f:
        res["active"] = sum(r["status"] in ("open", "watch") for r in csv.DictReader(f))
    return res


# ---------------------------------------------------------------- 7. hidden buses (E32 replay)
def timed(live, timeout, script, *args):
    """run() with a time limit (seconds); False when it failed or ran out of time."""
    cmd = [sys.executable, str(Path(live) / script), *map(str, args)]
    log("$", " ".join(cmd[:8]), "..." if len(cmd) > 8 else "")
    try:
        return subprocess.run(cmd, cwd=live, timeout=max(1, timeout)).returncode == 0
    except subprocess.TimeoutExpired:
        log(f"{script}: stopped after {timeout:.0f} s")
        return False


def refresh_hidden(live, dl, work, out, days, budget_s=HIDDEN_BUDGET_S):
    """E32 replay of every archived day through the app repo's web/js (headless Edge: env EDGE, or msedge on PATH),
    then hidden_buses.py -> out/hidden_buses/hidden_buses.csv. -> what happened, for last_run.json. The app repo's
    data/labeled/hidden_buses/ stays the reviewed copy (adopt this one there by copying it, after a look at its
    TOTALS line)."""
    live, dl = Path(live), Path(dl)
    if not (live / E32 / "hidden_buses.py").exists():
        return {"skipped": "the app repo has no E32 hidden_buses.py"}
    t_end = time.time() + budget_s
    w, r = work / "e32" / "work", work / "e32" / "results"
    w.mkdir(parents=True, exist_ok=True)
    need = ("raw-polls-{}.jsonl.gz", "pred-updates-{}.jsonl.gz", "gtfs-{}.zip")
    ok = [d for d in days if all((dl / k.format(d)).exists() for k in need)]
    if not ok:
        return {"skipped": "no day with raw polls, prediction updates and a timetable"}
    built = []
    for d in ok:                                            # one call per day: a bad day cannot stop the others
        if time.time() > t_end:
            break
        if timed(live, min(300, t_end - time.time()), f"{E32}/inputs.py", "--dl", dl, "--alerts", dl / "alerts.csv",
                 "--days", d, "--out", w):
            built.append(d)
    if not built:
        return {"skipped": "inputs.py built no day"}
    if not timed(live, min(600, t_end - time.time()), f"{E32}/replay.py", "--work", w, "--results", r, "--days",
                 built[-1], "--plan", 0, "--jobs", 1, "--timeout", 400):
        return {"skipped": f"the one-day smoke replay ({built[-1]}) failed: no browser, or the page did not run"}
    full = timed(live, t_end - time.time(), f"{E32}/replay.py", "--work", w, "--results", r, "--days", *built,
                 "--plan", 0, "--jobs", 3, "--timeout", 600)
    replayed = [d for d in built if (r / f"{d}.json").exists()]
    sha = subprocess.run(["git", "-C", str(live), "rev-parse", "--short", "HEAD"], capture_output=True,
                         text=True).stdout.strip() or "unknown"
    dest = Path(out) / "hidden_buses" / "hidden_buses.csv"
    if not timed(live, 900, f"{E32}/hidden_buses.py", "--work", w, "--results", r, "--arrivals", dl / "arrivals.csv",
                 "--from", replayed[0], "--to", replayed[-1], "--rules", f"main@{sha}", "--out", dest,
                 "--json", work / "e32" / "hidden.json"):
        return {"skipped": "hidden_buses.py failed", "replayed": len(replayed)}
    per = json.loads((work / "e32" / "hidden.json").read_text(encoding="utf-8")).get("per_line", {})
    return {"file": dest.relative_to(Path(out).parent).as_posix(), "rules": f"main@{sha}", "days": len(replayed),
            "from": replayed[0], "to": replayed[-1], "not_replayed": [d for d in ok if d not in replayed],
            "all_days_replayed": bool(full) and len(replayed) == len(ok),
            "episodes": {k: sum(v.get(k, 0) for v in per.values())
                         for k in ("off_route", "idle", "gone", "held", "not_operating")}}


# ---------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--live", required=True, help="app repo checkout (main): its scripts and docs are read, never changed")
    ap.add_argument("--src-data", required=True, help="app repo data-branch checkout (data/ground_truth/*.csv)")
    ap.add_argument("--dl", required=True)
    ap.add_argument("--out", default=str(HERE))
    ap.add_argument("--work")
    ap.add_argument("--skip-fetch", action="store_true")
    ap.add_argument("--skip-eos", action="store_true", help="use the app repo's committed end-of-service files")
    ap.add_argument("--skip-flags", action="store_true", help="do not rerun E30 / E31 (the workbook shows the app repo's flags)")
    ap.add_argument("--eta-dir", help="folder with eta-<day>.csv.gz for E31 (default: --dl)")
    ap.add_argument("--skip-hidden", action="store_true", help="do not replay E32 for the hidden-bus file")
    a = ap.parse_args(argv)
    live, out, dl = Path(a.live).resolve(), Path(a.out).resolve(), Path(a.dl).resolve()
    work = Path(a.work or out / ".work").resolve()
    work.mkdir(parents=True, exist_ok=True)
    days = (sorted(p.name[10:20] for p in dl.glob("raw-polls-*.jsonl.gz") if p.name[10:20] >= FIRST_DAY)
            if a.skip_fetch else fetch(dl, a.src_data))
    run_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    tdir = work / "transitions"
    run(live, "experiments/routeknower/E29-scripts/transitions.py", "--dl", dl, "--out", tdir, "--json", work / "e29.json")
    eos = work / "eos"
    if not a.skip_eos:
        try:
            run(live, "experiments/routeknower/E28-scripts/endofservice.py", "--dl", dl, "--out", eos, "--json", work / "e28.json")
        except RuntimeError as ex:
            log(f"end of service skipped: {ex}")
            eos = None
    if a.skip_eos or eos is None or not (eos / "summary.csv").exists():
        eos = live / "data" / "labeled" / "end_of_service"
    train_to = (date.fromisoformat(days[-1]) - timedelta(days=TEST_DAYS)).isoformat()
    run(live, "experiments/routeknower/E29-scripts/transition_rules.py", "--dl", dl, "--transitions",
        tdir / "transitions.csv", "--train-to", train_to, "--windows-out", tdir / "leave_windows.csv",
        "--json", work / "e29b.json")
    res = json.loads((work / "e29b.json").read_text(encoding="utf-8"))
    hist_path = out / "leave_eval_history.csv"
    prev = read_history(hist_path)
    new = history_rows(res, days, train_to, run_utc, prev)
    write_history(hist_path, prev + new)
    rt = ready_text(new)
    ready_path = out / "leave_ready.md"
    if rt:
        ready_path.write_text(rt, encoding="utf-8")
    elif ready_path.exists():
        ready_path.unlink()
    meta = {"run_utc": run_utc, "data_from": days[0], "data_to": days[-1], "days": len(days), "train_to": train_to,
            "test_days": res["A_about_to_leave"].get("test_days"), "ready_signals": [r["signal"] for r in new if str(r["ready"]) == "1"],
            "readiness_rule": {"min_data_to": READY_MIN_DATA_TO, "precision": READY_PRECISION, "recall": READY_RECALL,
                               "min_flagged": READY_MIN_FLAGGED, "train_precision": READY_TRAIN_PRECISION, "consecutive_runs": 2},
            "transitions": json.loads((work / "e29.json").read_text(encoding="utf-8")).get("by_kind_label"),
            "end_of_service_source": str(eos.relative_to(live)) if str(eos).startswith(str(live)) else "rebuilt this run"}
    flags = None if a.skip_flags else refresh_flags(live, dl, tdir, eos, work, out, days, a.eta_dir)
    meta["flags_source"] = "refreshed" if flags else "app repo"
    meta["flags"] = flags
    sys.path.insert(0, str(HERE))
    import build_workbook as W
    W.build(out, live, tdir, eos, Path(out).parent, meta)
    meta["hidden_buses"] = {"skipped": "--skip-hidden"} if a.skip_hidden else refresh_hidden(live, dl, work, out, days)
    (out / "last_run.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    log(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
