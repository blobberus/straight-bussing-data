# Findings: an index for agents (updated weekly)

Owner, 2026-11-06: "retry which bus will leave after applicable intervals of new data collected and revise it. Give me
an updating xlsx file to reference for other agents (put this in the data repo along with your other findings)."

**Start here:** [`straight-bussing-findings.xlsx`](straight-bussing-findings.xlsx) (one tab per finding, an index tab
first) or the same tables as CSV in [`csv/`](csv/). Rebuilt every Monday about 17:41 UTC (GitHub may start it late) and
by hand by [`.github/workflows/findings.yml`](../.github/workflows/findings.yml), which runs
[`run_findings.py`](run_findings.py) (fetch + rerun + evaluate) and [`build_workbook.py`](build_workbook.py). The last
run's dates and counts: [`last_run.json`](last_run.json). App repo = github.com/blobberus/straight-bussing (read-only
here: the workflow clones it; nothing is written to it or to its `data` branch).

Unofficial; not affiliated with the University of Chicago. Official service information: 773.702.8181.

## The findings, in a few lines each

| Tab / file | What it says | Where it comes from |
|---|---|---|
| **`flagged_lines`**, `csv/flagged_lines.csv`, [`FLAGGED-LINES.md`](FLAGGED-LINES.md) | **Read first.** The lines whose data behaves oddly, one row per line and problem: odd bus behavior at transition times, large prediction misses, what the shipped display showed riders; where and when (`scope`: stops, hours, days, buses, minutes ahead), the line's number against all lines, severity, evidence, and `agent_action` (what a model or app agent must do). Model agents score every open or watch flag as its own slice (`algorithm-test` step 13); app agents read it before changing a display rule and never hide a bus on a flag alone. | App repo `data/labeled/flags/` (README there: schema, severity, duties), merged by `tools/flag_lines.py` from RouteKnower E30, E31, E32; per-line summary `docs/FLAGGED-LINES.md`. Refreshed here every week: `run_findings.py` reruns E30 and E31 on the archived days and merges them (E32 needs a browser: the app repo's reviewed `display_flags.csv` is used as is), so this tab can be a week newer than the app repo's copy |
| [`service_seen/service_seen.json`](service_seen/) (no tab) | Per line and day type: when its buses are really seen starting and ending service, bus by bus (Bus 1, Bus 2, ... in the order they first report: median, 10th to 90th percentile, days), their breaks and the timetable's listed hours; plus every usual move of a bus from one line to another (when, where, the label it carries on the way). The reasoning is inside the file. | App repo `tools/build_service_seen.py` (RouteKnower E33) rerun here every week on all archived days. The app loads the app repo's `web/data/service_seen.json`: adopt this copy there by hand after a look (docs/DATA.md "Seen service windows") |
| [`flags/collection_flags.csv`](flags/), [`collection/`](collection/) (no tab; the flags are in `flagged_lines`) | Per line: where the **collected data** itself is less complete or less right than on the other lines (rows only the GPS saw, stops Passio never names, rows without a Passio time, buses under another line's label all day, stops the collector rarely logs although the buses pass them, listed hours with no bus, report gaps, frozen GPS), and the evidence per day, line, stop and wrong-label episode | App repo `tools/collection_flags.py` (category `collection`; README `data/labeled/collection/README.md` has the measures and the severity rule) rerun here every week on all archived days (about 30 s). Adopt it in the app repo with the flags: `collection/` into `data/labeled/collection/`, `flags/collection_flags.csv` into `data/labeled/flags/`, then `python tools/flag_lines.py` |
| [`hidden_buses/hidden_buses.csv`](hidden_buses/) (no tab) | Every episode in which the app's display rules hid a bus, or its times, while Passio still had times for it: rule (off_route, idle, gone, not_operating = the shipped reshow after a hide, held = the owner's "times off until it reports again" once the code has it), line, bus, minutes, stops with times, whether those times came true and whether the bus came to serve within 15 min. The `#` lines at the top explain it. | App repo RouteKnower E32: this run replays every archived day through the app repo's own `web/js` (`E32-scripts/inputs.py` + `replay.py` in headless Edge, no planner samples, about 7 s a day) and writes it with `hidden_buses.py`; the reviewed copy is the app repo's `data/labeled/hidden_buses/` (README there). Skipped without a browser (last_run.json `hidden_buses` says why) |
| `transitions`, `csv/transitions.csv` | Every time a line's bus count changed (a bus leaving for a break, its shift end, another line or off the map; a bus joining from the garage, a break or another line): which bus, where it left or joined, where it went or came from, how long, whether Passio kept predicting it, replacement bus. | App repo RouteKnower.md E29, `experiments/routeknower/E29-scripts/transitions.py`; the reviewed copy is the app repo's `data/labeled/transitions/` (README there: labels and columns) |
| `transition_spots`, `transition_summary` | The usual leave / join places and times per line, and counts per line and hour (e.g. Apostolic bus 4322's half-hour break at South Campus Residence Hall at 8:43 AM; the Downtown Campus Connector's midday breaks). | same |
| `leave_windows` | Per line, day type and stop: the clock windows in which a bus making its last stop there left on 3 days or more, with the in-sample precision (low: a window says a bus of the line usually leaves, not which). The forecast table's `break_window` / `leave_spot_dist_m` use the app repo's copy. | `transition_rules.py --windows-out` |
| `leave_eval_history`, [`leave_eval_history.csv`](leave_eval_history.csv) | **Can the app tell which bus will leave?** One row per signal per weekly run, on the newest 7 days held out. So far: no (best about a third of flagged visits; the same bus on the same run 91% but on 11 visits). The last row per run is the app's shipped GONE rule (drop the times of a bus silent for 15 min): about 99% of the times it drops never came true. | `transition_rules.py` with an expanding window (below) |
| `eos_not_layover`, `eos_linger_spots`, `eos_line_summary` | Where buses linger at the end of a trip or a shift (the buses "in front of Regenstein" at 11:50 PM), breaks, shift ends, garage returns; per line. The app hides idle buses that are not in service. | RouteKnower E28, `experiments/routeknower/E28-scripts/endofservice.py`; full per-day files in the app repo's `data/labeled/end_of_service/` |
| `lines_most_affected` | The five lines most affected by idle, off-route and unpredictable buses (Downtown Campus Connector, Apostolic/Drexel, Red Line/Arts Block, East, Midway Metra) and the numbers behind the ranking. | App repo `docs/LINES-MOST-AFFECTED.md` |
| `off_route` | Buses that do not follow their route: how far and how long buses in service leave their line, and the shipped hide rules (E27, then E27b: more than a block off, still tracked). | App repo RouteKnower.md E27 / E27b, docs/ARCHITECTURE.md "Buses that do not follow their route" |
| `experiment_log` | Every RouteKnower experiment (data, result, decision). | App repo RouteKnower.md section 11 |
| `forecast_bench` | Arrival-time predictors against the owner's accuracy goal (Passio, timetable, boosted trees, small networks), the four biggest lateness perpetrators, and every model in transition periods (section 6). | This repo's `algorithm-test/CONCLUSION.md`, `results/12-transitions.md` |
| `collection_anomalies` | Data-collection errors and checkups (DC-001 to the newest, and each numbered item of a checkup such as DC-023). | App repo `docs/DATA-COLLECTION-LOG.md` |

Big tables: the workbook keeps the non-layover end-of-service episodes only (the full per-day files are in the app
repo); everything else is complete.

## The weekly retry of "which bus will leave"

Each run trains on every archived day up to 7 days before the newest and tests on the newest 7 days (an expanding
window: the test days are never seen in training; training rows use the other training days only). Signals: the line's
learned leave window at the stop (+- 15 min), the same trip id, Passio showing nothing beyond the stop, the number of
buses on the line, the same bus at the same stop and time on earlier days, and a small network (top-k only, when
PyTorch is installed; CI has none).

**Ready for review** (a signal, all must hold, `run_findings.py`):
- the data reaches **2026-11-26** or later (3 weeks more than the first evaluation's Nov 5);
- held-out **precision >= 90%** and **recall >= 20%** on **>= 30 flagged visits**;
- precision on the training days **>= 85%** (it held in-sample too, not one lucky week);
- the same in the **previous run on an earlier week of data** (data at least 5 days older; a rerun on the same days
  never counts twice), so 2 consecutive weeks.

Why these numbers: rider safety comes first, so a rule that steers a rider away from a bus that does serve their ride
must be rare (E25 asked 90% at 15 min); 30 flagged visits keep a 90% estimate's 95% interval above about 75%; under 20%
recall a rule changes almost nothing a rider sees. Thanksgiving Break (Nov 23 to 27) runs reduced service: a signal
that only holds across it should be read with care.

When a signal is ready the workflow opens (or updates) ONE issue in this repo, **"Leave prediction ready for review"**,
with the numbers. **It never changes the app.** Shipping is a reviewed change in the app repo; the procedure and the
exact commands are in the app repo's RouteKnower.md, "E29 retry procedure". In short:
1. Reproduce locally (app repo): `python experiments/routeknower/E28-scripts/fetch.py --out <dl> --from 2026-10-10
   --to <newest archived day>`, then `python experiments/routeknower/E29-scripts/transitions.py --dl <dl> --out
   data/labeled/transitions`, then `python experiments/routeknower/E29-scripts/transition_rules.py --dl <dl>
   --transitions data/labeled/transitions/transitions.csv --train-to <newest day - 7> --windows-out
   data/labeled/transitions/leave_windows.csv --json e29.json`, and check the signal's numbers.
2. Port it as a pure rule (web `core/transition.js` + Kit `Transition.swift`, golden tests from real polls), used only by
   the planner / trip options / next bus (never the map), with a learned table that carries its listed hours and a
   `valid_until`, like `web/data/idle.json`.
3. Owner review, full browser suite, iOS CI, one commit.

The hidden-bus step (since 2026-11-11) runs last: E32 `inputs.py` per day, a one-day smoke replay, then every day (3 browsers at a time; the whole step stops after 45 min), then `hidden_buses.py --rules main@<app repo commit>` (first run 2026-11-11: 31 days replayed in about 2.5 min, headless Edge 156). To adopt the result in the app repo, copy `hidden_buses/hidden_buses.csv` into its `data/labeled/hidden_buses/`, read the TOTALS line, then commit.

## Refresh by hand

```
gh workflow run findings.yml -R blobberus/straight-bussing-data         # the full weekly run (about 10 min; Nov 11: 9.5)
python findings/build_workbook.py --live <app repo checkout>            # only rebuild the workbook from findings/csv
python findings/run_findings.py --live <app repo checkout> --src-data <app repo data-branch checkout> --dl <cache> --out findings
```

The flag step reruns E30 (`experiments/routeknower/E30-scripts/run_odd.py` + `flags.py`, about 2.5 min on GitHub's runner) and E31
(`E31-scripts/misses.py` + `flags.py`, about 1.5 min; it reads the eta tables, which the fetch now downloads too, and
the data branch's `predictions.csv` + `archive/predictions-*.csv`), then the app repo's `tools/flag_lines.py`, which
writes `csv/flagged_lines.csv` and the per-line summary [`FLAGGED-LINES.md`](FLAGGED-LINES.md) (headed by a note on
what was rerun). Since 2026-11-13 it also reruns the app repo's `tools/collection_flags.py` (per-line issues in the
collected data, category `collection`; about 30 s) on the same days. The rerun producer files themselves go to
[`flags/`](flags/) (`transition_flags.csv`, `prediction_flags.csv`, `collection_flags.csv`, with the collection evidence
in [`collection/`](collection/); a producer that failed has none there): an app agent adopts a refresh by copying them
into the app repo's `data/labeled/flags/` (and `collection/` into its `data/labeled/collection/`), running
`python tools/flag_lines.py` there and reviewing the new and resolved flags before committing. A producer that fails keeps the app repo's copy of its flags (the run log says so; `last_run.json`
`flags`), so a failure never marks flags resolved. `--skip-flags` leaves the app repo's registry in the tab.

Packages: numpy and openpyxl (Python 3.11). The workflow keeps the downloaded archive days in the Actions cache, so a
run downloads only the new days.
