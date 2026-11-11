#!/usr/bin/env python3
"""Builds findings/straight-bussing-findings.xlsx (one tab per finding, an index first) and a CSV copy of every tab in
findings/csv/, for agents and people without Excel. Called by run_findings.py after each weekly refresh; it can also run
alone on the files already there:

  python findings/build_workbook.py --live <app repo checkout> [--out findings]

Sources (all read-only): the flagged-lines registry (this run's refresh in findings/csv/flagged_lines.csv, else the
app repo's reviewed copy data/labeled/flags/flagged_lines.csv, tools/flag_lines.py), this run's transitions / leave
windows (findings/csv, rebuilt by the app repo's RouteKnower E29 scripts), the leave-prediction history (findings/leave_eval_history.csv), the end-of-service episodes (E28), the app
repo's docs/LINES-MOST-AFFECTED.md, RouteKnower.md (experiment log, off-route rows E27 / E27b),
docs/DATA-COLLECTION-LOG.md (anomalies), and this repo's algorithm-test/CONCLUSION.md + results/12-transitions.md.
"""
import argparse, csv, json, re, shutil
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
NUM = re.compile(r"^-?\d+(\.\d+)?$")
APP = "github.com/blobberus/straight-bussing"
DATA = "github.com/blobberus/straight-bussing-data"


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        r = list(csv.reader(f))
    return (r[0], r[1:]) if r else ([], [])


def write_csv(path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def md_tables(text):
    """Every markdown table in text -> [(heading above it, header, rows)]."""
    out, head, cur = [], "", None
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith("#"):
            head = s.lstrip("#").strip()
        if s.startswith("|") and s.endswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if cur is None:
                cur = [head, cells, []]
            elif all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                continue
            else:
                cur[2].append(cells)
        elif cur is not None:
            out.append(tuple(cur))
            cur = None
    if cur is not None:
        out.append(tuple(cur))
    return out


def tables_tab(text, names=None, note=""):
    """Markdown tables flattened into one sheet: table, then the columns of the widest table."""
    rows, width = [], 0
    for head, hdr, body in md_tables(text):
        if names and not any(n in head for n in names):
            continue
        rows.append([head] + hdr)
        rows += [[head] + r for r in body]
        rows.append([])
        width = max(width, len(hdr) + 1)
    header = ["table (first row of each block = its column names)"] + [f"c{i}" for i in range(1, width)]
    return header, rows


def experiment_rows(rk_text, ids=None):
    """RouteKnower.md section 11 rows (ID, date, data, result, decision)."""
    out = []
    for ln in rk_text.splitlines():
        m = re.match(r"^\| (E\d+[a-z]?) \|", ln)
        if not m or (ids and m.group(1) not in ids):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) >= 5:
            out.append(cells[:5])
    return ["id", "date", "data", "result", "decision"], out


def anomalies(dc_text):
    """docs/DATA-COLLECTION-LOG.md: one row per DC entry (id, title, status, summary) and per numbered item of the
    checkups that have them (e.g. DC-023 items 1 to 8)."""
    rows, cur = [], None
    blocks = re.split(r"^### ", dc_text, flags=re.M)[1:]
    for b in blocks:
        title = b.splitlines()[0].strip()
        m = re.match(r"(DC-\d+)\s+(.*)", title)
        if not m:
            continue
        dc, rest = m.group(1), m.group(2)
        st = re.search(r"\(([^()]*)\)\s*$", rest)
        body = "\n".join(b.splitlines()[1:])
        first = next((ln.strip() for ln in body.splitlines() if ln.strip()), "")
        rows.append([dc, "", rest, st.group(1) if st else "", first[:600]])
        for im in re.finditer(r"^\*\*(\d+)\.\s+(.*?)\*\*(.*)$", body, flags=re.M):
            t = im.group(2)
            s2 = re.search(r"\(([^()]*)\)\.?\s*$", t)
            rows.append([dc, im.group(1), t, s2.group(1) if s2 else "", im.group(3).strip()[:600]])
    return ["entry", "item", "title", "status", "first line"], rows


def eos_tabs(eos):
    """E28 end-of-service: non-layover episodes of every day (full per-day files stay in the app repo), linger spots,
    per-line summary."""
    hdr, rows = None, []
    for p in sorted(Path(eos).glob("20??-??-??.csv")):
        h, r = read_csv(p)
        hdr = hdr or ["service_day"] + h
        li = h.index("label") if "label" in h else None
        rows += [[p.stem] + x for x in r if li is None or x[li] != "layover"]
    spots = read_csv(Path(eos) / "linger_spots.csv") if (Path(eos) / "linger_spots.csv").exists() else ([], [])
    summ = read_csv(Path(eos) / "summary.csv") if (Path(eos) / "summary.csv").exists() else ([], [])
    return (hdr or [], rows), spots, summ


def autosize(ws, header, rows, cap=60):
    from openpyxl.utils import get_column_letter
    for i, h in enumerate(header, 1):
        n = max([len(str(h))] + [len(str(r[i - 1])) for r in rows[:400] if len(r) >= i])
        ws.column_dimensions[get_column_letter(i)].width = max(8, min(cap, n + 2))


def build(out, live, tdir, eos, data_root, meta=None, flags=None):
    """Write the workbook and the CSV copies. out: findings/; live: app repo checkout; tdir: this run's E29 folder
    (transitions.csv, transition_spots.csv, transition_summary.csv, leave_windows.csv; None = findings/csv already has
    them); eos: an E28 folder; data_root: this repo's root; flags: the flagged-lines registry (default: this run's
    findings/csv/flagged_lines.csv if a refresh wrote one, else the app repo's data/labeled/flags/flagged_lines.csv)."""
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill
    out, live, data_root = Path(out), Path(live), Path(data_root)
    cdir = out / "csv"
    cdir.mkdir(parents=True, exist_ok=True)
    if tdir:
        for f in ("transitions.csv", "transition_spots.csv", "transition_summary.csv", "leave_windows.csv"):
            shutil.copy2(Path(tdir) / f, cdir / f)
    rk = (live / "RouteKnower.md").read_text(encoding="utf-8")
    tabs = []      # (name, what, source, header, rows)
    app_fl = live / "data" / "labeled" / "flags" / "flagged_lines.csv"
    if flags:
        fl = Path(flags)
    elif (meta or {}).get("flags_source") == "refreshed" and (cdir / "flagged_lines.csv").exists():
        fl = cdir / "flagged_lines.csv"          # run_findings.py refreshed the producers and merged them this run
    else:
        fl = app_fl
    fsrc = (f"{APP} data/labeled/flags/flagged_lines.csv (reviewed copy; tools/flag_lines.py)" if fl == app_fl else
            f"{DATA} findings/csv/flagged_lines.csv (this run's refresh of the producers, merged by {APP} tools/flag_lines.py)")
    tabs.append(("flagged_lines", "READ FIRST: lines whose data behaves oddly (transition_flags E30, prediction_miss E31, "
                 "display E32), with where and when (scope), the line's number vs all lines, evidence and what an agent must "
                 "do (agent_action). Model agents: score every open / watch flag as its own slice (algorithm-test step 13); "
                 "app agents: read before changing a display rule, never hide a bus on a flag alone. Rules: app repo "
                 "data/labeled/flags/README.md, summary docs/FLAGGED-LINES.md",
                 fsrc, *(read_csv(fl) if fl.exists() else ([], []))))
    for name, f, what in (("transitions", "transitions.csv", "every bus count transition (a bus leaving or joining a line), labeled break / shift_end / route_switch / feed_drop / layover_swap / added_from_*, where and what the bus did (E29)"),
                          ("transition_spots", "transition_spots.csv", "named leave / join spots per line: events, days, typical clock times (E29)"),
                          ("transition_summary", "transition_summary.csv", "per line, day type and clock hour: leaves and joins by label (E29)"),
                          ("leave_windows", "leave_windows.csv", "learned windows in which a bus making its last stop at a stop left the line on >= 3 days; in-sample precision (E29, used by the forecast table's break_window)")):
        h, r = read_csv(cdir / f)
        tabs.append((name, what, f"{DATA} findings/csv/{f} (rebuilt weekly from {APP} experiments/routeknower/E29-scripts)", h, r))
    h, r = read_csv(out / "leave_eval_history.csv") if (out / "leave_eval_history.csv").exists() else ([], [])
    tabs.append(("leave_eval_history", "one row per signal per weekly run: can the app tell which bus will leave? (expanding window: train on all days up to 7 before the newest, test on the newest 7; ready = precision >= 90%, recall >= 20%, >= 30 flagged, train >= 85%, 2 runs in a row, data through 2026-11-26+); plus the shipped gone rule's precision",
                 f"{DATA} findings/leave_eval_history.csv", h, r))
    (eh, er), sp, sm = eos_tabs(eos)
    src = f"{APP} data/labeled/end_of_service/ (full per-day files)" if "end_of_service" in str(eos) else "rebuilt this run by E28 endofservice.py; full per-day files in " + f"{APP} data/labeled/end_of_service/"
    tabs.append(("eos_not_layover", "end-of-trip / end-of-shift dwell episodes that are not layovers (break, end_of_shift, garage_return, parked_never_served) (E28)", src, eh, er))
    tabs.append(("eos_linger_spots", "where buses linger at the end of a trip or shift, per spot (E28)", src, *sp))
    tabs.append(("eos_line_summary", "end-of-service episodes per line, idle minutes the app showed before E28 (E28)", src, *sm))
    lm = live / "docs" / "LINES-MOST-AFFECTED.md"
    tabs.append(("lines_most_affected", "the five lines most affected by idle / off-route / unpredictable buses and the numbers behind the ranking",
                 f"{APP} docs/LINES-MOST-AFFECTED.md", *(tables_tab(lm.read_text(encoding="utf-8")) if lm.exists() else ([], []))))
    tabs.append(("off_route", "buses that do not follow their route: the measurements and the shipped rules (E27, E27b)",
                 f"{APP} RouteKnower.md section 11 rows E27, E27b; docs/ARCHITECTURE.md \"Buses that do not follow their route\"",
                 *experiment_rows(rk, {"E27", "E27b"})))
    tabs.append(("experiment_log", "every RouteKnower experiment: data, result, decision", f"{APP} RouteKnower.md section 11", *experiment_rows(rk)))
    concl = data_root / "algorithm-test" / "CONCLUSION.md"
    r12 = data_root / "algorithm-test" / "results" / "12-transitions.md"
    text = (concl.read_text(encoding="utf-8") if concl.exists() else "") + "\n\n# results/12-transitions\n" + (r12.read_text(encoding="utf-8") if r12.exists() else "")
    tabs.append(("forecast_bench", "arrival-prediction bench: predictors against the accuracy goal, lateness perpetrators, transition periods (section 6)",
                 f"{DATA} algorithm-test/CONCLUSION.md, results/12-transitions.md", *tables_tab(text)))
    dc = live / "docs" / "DATA-COLLECTION-LOG.md"
    tabs.append(("collection_anomalies", "data-collection errors and checkups (DC entries and the numbered items of each checkup)",
                 f"{APP} docs/DATA-COLLECTION-LOG.md", *(anomalies(dc.read_text(encoding="utf-8")) if dc.exists() else ([], []))))
    meta = meta or {}
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    index = [["tab", "what it is", "source", "rows", "csv copy"]]
    for name, what, source, h, r in tabs:
        index.append([name, what, source, len(r), f"findings/csv/{name}.csv"])
    info = [["Straight Bussing findings workbook (unofficial; for agents and the owner)"], [f"Last updated: {now}"],
            [f"Data: {meta.get('data_from', '?')} to {meta.get('data_to', '?')} ({meta.get('days', '?')} archived service days); leave-prediction test days {', '.join(meta.get('test_days') or [])}"],
            [f"Ready leave signals this run: {', '.join(meta.get('ready_signals') or []) or 'none'} (the app never changes by itself; app repo RouteKnower.md E29 'Retry procedure')"],
            ["Refresh: data repo .github/workflows/findings.yml (weekly, Mondays about 17:41 UTC, and by hand) runs findings/run_findings.py; index of findings: findings/README.md"],
            []]
    wb = Workbook()
    ws = wb.active
    ws.title = "README"
    bold, fill = Font(bold=True), PatternFill("solid", fgColor="DDEBF7")
    for r in info:
        ws.append(r)
    ws["A1"].font = Font(bold=True, size=13)
    start = ws.max_row + 1
    for r in index:
        ws.append(r)
    for c in ws[start]:
        c.font, c.fill = bold, fill
    for col, wdt in zip("ABCDE", (22, 90, 70, 8, 34)):
        ws.column_dimensions[col].width = wdt
    write_csv(cdir / "README_index.csv", index[0], index[1:])
    for name, what, source, h, r in tabs:
        s = wb.create_sheet(name[:31])
        if not h:
            s.append(["(no data this run)"])
            continue
        s.append(h)
        for row in r:
            s.append([float(x) if isinstance(x, str) and NUM.match(x) and len(x) < 16 else x for x in row])
        for c in s[1]:
            c.font, c.fill = bold, fill
        s.freeze_panes = "A2"
        s.auto_filter.ref = s.dimensions
        autosize(s, h, r)
        if name not in ("transitions", "transition_spots", "transition_summary", "leave_windows"):
            write_csv(cdir / f"{name}.csv", h, r)
    wb.save(out / "straight-bussing-findings.xlsx")
    return [(t[0], len(t[4])) for t in tabs]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--live", required=True)
    ap.add_argument("--out", default=str(HERE))
    ap.add_argument("--eos", help="E28 folder (default: the app repo's data/labeled/end_of_service)")
    ap.add_argument("--flags", help="flagged-lines registry CSV (default: the app repo's data/labeled/flags/flagged_lines.csv)")
    a = ap.parse_args(argv)
    meta = json.loads((Path(a.out) / "last_run.json").read_text(encoding="utf-8")) if (Path(a.out) / "last_run.json").exists() else {}
    print(build(a.out, a.live, None, a.eos or Path(a.live) / "data" / "labeled" / "end_of_service", Path(a.out).resolve().parent, meta,
                a.flags))


if __name__ == "__main__":
    main()
