# Straight Bussing data

Ground-truth arrivals of the UChicago campus shuttles, collected by the unofficial
[Straight Bussing](https://github.com/blobberus/straight-bussing) tracker, plus the RouteKnower methodology
for learning drive and arrival times from them. **Updated automatically every 30 minutes.**

**See the bus movement:** https://blobberus.github.io/straight-bussing-data/ (pick a day and a route; each line
is one bus trip moving stop to stop over time; hover or tap a point for the stop and time).

## What is here
| Path | What |
|---|---|
| `data/arrivals/<service day>/<route>.csv` | one row per bus arriving at a stop (GitHub shows each file as a table). A service day runs 4:00 AM to 3:59 AM Chicago time, so late-night trips stay with their evening. |
| `data/latest.csv` | the newest 200 arrivals, all routes |
| `data/index.json` | days, routes and counts (used by the viewer) |
| `data/network/` | route colors, stop names and stop order from the public GTFS schedule |
| `methodology/` | `RouteKnower.md` (the experiment plan, test protocol, data targets, experiment log), `experiments/routeknower/` (experiment write-ups), and the data / algorithm / backtest docs |
| `algorithm-test/` | a test bench for arrival-time prediction: Passio, the timetable, boosted trees and a neural network scored against the current accuracy goal on the public forecast tables (trained on earlier days, tested on later ones), what makes buses come later than shown, and the conclusion (`algorithm-test/README.md`, `CONCLUSION.md`). Run it with `python algorithm-test/run_all.py` |
| `index.html`, `viewer.js`, `viewer.css` | the viewer page |
| `scripts/sync.py`, `scripts/test_sync.py`, `.github/workflows/sync.yml` | the sync that keeps all of this current, and its test (run before every rebuild) |

**What each column means, in plain English:** [`methodology/docs/DATA-GUIDE.md`](methodology/docs/DATA-GUIDE.md)
(with a worked example row and spreadsheet recipes). The prediction goal (the 10% rule), how predictions are scored and
the plan to improve them: [`methodology/docs/GOAL-AND-METHOD.md`](methodology/docs/GOAL-AND-METHOD.md). Technical details: `methodology/docs/DATA.md` ("Schema"). Times are good to about +-10 s; `segment_s` is the time from
the previous detected stop; `passio_pred_epoch` is the official app's prediction made at least 2 minutes earlier.

**Correction (2026-11-11):** from Oct 29 to Nov 11, 2026 the per-day files and `data/latest.csv` had the 15 columns of
the prediction file instead of the 25 arrival columns (no `source`, `segment_s`, `dwell_s`, `passio_pred_epoch`, stop
coordinates ...), and about 4,300 rows too many: the sync read a rotated prediction file as arrivals. Fixed; every
file was rewritten on Nov 11. A copy downloaded in that time should be downloaded again (app repo
docs/DATA-COLLECTION-LOG.md, DC-026).

## How it stays current
The app repo collects arrivals around the clock (GitHub Actions every 30 minutes plus a local collector) into its
public `data` branch. This repo's `sync` workflow pulls that branch and the methodology files every 30 minutes, splits
the data by day and route, and commits only what changed. The methodology's source of truth stays in the app repo
(edit it there); this copy follows within the hour.

Unofficial; not affiliated with the University of Chicago. The feed holds vehicle positions and predictions only:
no rider data. Official service information: 773.702.8181.

## Latest
<!-- SYNC:BEGIN -->
_Last sync: 2026-11-24 05:36 UTC · 145,131 arrivals · 47 service days · newest arrival 2026-11-23 23:25:14 (Chicago time)_

| Service day | Arrivals | Routes | Files |
|---|---:|---:|---|
| 2026-11-23 | 4,462 | 13 | [data/arrivals/2026-11-23/](data/arrivals/2026-11-23) |
| 2026-11-22 | 756 | 4 | [data/arrivals/2026-11-22/](data/arrivals/2026-11-22) |
| 2026-11-21 | 951 | 6 | [data/arrivals/2026-11-21/](data/arrivals/2026-11-21) |
| 2026-11-20 | 4,076 | 14 | [data/arrivals/2026-11-20/](data/arrivals/2026-11-20) |
| 2026-11-19 | 4,538 | 13 | [data/arrivals/2026-11-19/](data/arrivals/2026-11-19) |
| 2026-11-18 | 4,469 | 13 | [data/arrivals/2026-11-18/](data/arrivals/2026-11-18) |
| 2026-11-17 | 4,286 | 13 | [data/arrivals/2026-11-17/](data/arrivals/2026-11-17) |
| 2026-11-16 | 3,985 | 13 | [data/arrivals/2026-11-16/](data/arrivals/2026-11-16) |
| 2026-11-15 | 728 | 4 | [data/arrivals/2026-11-15/](data/arrivals/2026-11-15) |
| 2026-11-14 | 939 | 5 | [data/arrivals/2026-11-14/](data/arrivals/2026-11-14) |
| 2026-11-13 | 3,656 | 13 | [data/arrivals/2026-11-13/](data/arrivals/2026-11-13) |
| 2026-11-12 | 4,390 | 13 | [data/arrivals/2026-11-12/](data/arrivals/2026-11-12) |
| 2026-11-11 | 4,312 | 13 | [data/arrivals/2026-11-11/](data/arrivals/2026-11-11) |
| 2026-11-10 | 3,917 | 13 | [data/arrivals/2026-11-10/](data/arrivals/2026-11-10) |

Routes on 2026-11-23:

| Route | Arrivals | File |
|---|---:|---|
| Apostolic/Drexel | 742 | [apostolic-drexel.csv](data/arrivals/2026-11-23/apostolic-drexel.csv) |
| Downtown Campus Connector | 637 | [downtown-campus-connector.csv](data/arrivals/2026-11-23/downtown-campus-connector.csv) |
| Red Line/Arts Block | 586 | [red-line-arts-block.csv](data/arrivals/2026-11-23/red-line-arts-block.csv) |
| Midway Metra | 497 | [midway-metra.csv](data/arrivals/2026-11-23/midway-metra.csv) |
| 53rd Street Express | 438 | [53rd-street-express.csv](data/arrivals/2026-11-23/53rd-street-express.csv) |
| Friend Center/Metra | 361 | [friend-center-metra.csv](data/arrivals/2026-11-23/friend-center-metra.csv) |
| Apostolic | 273 | [apostolic.csv](data/arrivals/2026-11-23/apostolic.csv) |
| Drexel | 205 | [drexel.csv](data/arrivals/2026-11-23/drexel.csv) |
| Central | 204 | [central.csv](data/arrivals/2026-11-23/central.csv) |
| South | 197 | [south.csv](data/arrivals/2026-11-23/south.csv) |
| East | 175 | [east.csv](data/arrivals/2026-11-23/east.csv) |
| North | 93 | [north.csv](data/arrivals/2026-11-23/north.csv) |
| Regents Express | 54 | [regents-express.csv](data/arrivals/2026-11-23/regents-express.csv) |
<!-- SYNC:END -->
