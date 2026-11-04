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
| `scripts/sync.py`, `.github/workflows/sync.yml` | the sync that keeps all of this current |

**What each column means, in plain English:** [`methodology/docs/DATA-GUIDE.md`](methodology/docs/DATA-GUIDE.md)
(with a worked example row and spreadsheet recipes). The prediction goal (the 10% rule), how predictions are scored and
the plan to improve them: [`methodology/docs/GOAL-AND-METHOD.md`](methodology/docs/GOAL-AND-METHOD.md). Technical details: `methodology/docs/DATA.md` ("Schema"). Times are good to about +-10 s; `segment_s` is the time from
the previous detected stop; `passio_pred_epoch` is the official app's prediction made at least 2 minutes earlier.

## How it stays current
The app repo collects arrivals around the clock (GitHub Actions every 30 minutes plus a local collector) into its
public `data` branch. This repo's `sync` workflow pulls that branch and the methodology files every 30 minutes, splits
the data by day and route, and commits only what changed. The methodology's source of truth stays in the app repo
(edit it there); this copy follows within the hour.

Unofficial; not affiliated with the University of Chicago. The feed holds vehicle positions and predictions only:
no rider data. Official service information: 773.702.8181.

## Latest
<!-- SYNC:BEGIN -->
_Last sync: 2026-11-04 22:25 UTC · 88,177 arrivals · 28 service days · newest arrival 2026-11-04 16:02:35 (Chicago time)_

| Service day | Arrivals | Routes | Files |
|---|---:|---:|---|
| 2026-11-04 | 2,233 | 10 | [data/arrivals/2026-11-04/](data/arrivals/2026-11-04) |
| 2026-11-03 | 4,148 | 13 | [data/arrivals/2026-11-03/](data/arrivals/2026-11-03) |
| 2026-11-02 | 3,931 | 13 | [data/arrivals/2026-11-02/](data/arrivals/2026-11-02) |
| 2026-11-01 | 776 | 4 | [data/arrivals/2026-11-01/](data/arrivals/2026-11-01) |
| 2026-10-31 | 929 | 5 | [data/arrivals/2026-10-31/](data/arrivals/2026-10-31) |
| 2026-10-30 | 4,203 | 14 | [data/arrivals/2026-10-30/](data/arrivals/2026-10-30) |
| 2026-10-29 | 4,301 | 13 | [data/arrivals/2026-10-29/](data/arrivals/2026-10-29) |
| 2026-10-28 | 3,999 | 13 | [data/arrivals/2026-10-28/](data/arrivals/2026-10-28) |
| 2026-10-27 | 4,539 | 13 | [data/arrivals/2026-10-27/](data/arrivals/2026-10-27) |
| 2026-10-26 | 4,253 | 13 | [data/arrivals/2026-10-26/](data/arrivals/2026-10-26) |
| 2026-10-25 | 899 | 4 | [data/arrivals/2026-10-25/](data/arrivals/2026-10-25) |
| 2026-10-24 | 1,107 | 6 | [data/arrivals/2026-10-24/](data/arrivals/2026-10-24) |
| 2026-10-23 | 4,233 | 14 | [data/arrivals/2026-10-23/](data/arrivals/2026-10-23) |
| 2026-10-22 | 3,903 | 13 | [data/arrivals/2026-10-22/](data/arrivals/2026-10-22) |

Routes on 2026-11-04:

| Route | Arrivals | File |
|---|---:|---|
| Red Line/Arts Block | 385 | [red-line-arts-block.csv](data/arrivals/2026-11-04/red-line-arts-block.csv) |
| 53rd Street Express | 364 | [53rd-street-express.csv](data/arrivals/2026-11-04/53rd-street-express.csv) |
| Downtown Campus Connector | 288 | [downtown-campus-connector.csv](data/arrivals/2026-11-04/downtown-campus-connector.csv) |
| Midway Metra | 271 | [midway-metra.csv](data/arrivals/2026-11-04/midway-metra.csv) |
| Friend Center/Metra | 251 | [friend-center-metra.csv](data/arrivals/2026-11-04/friend-center-metra.csv) |
| Apostolic | 246 | [apostolic.csv](data/arrivals/2026-11-04/apostolic.csv) |
| Apostolic/Drexel | 215 | [apostolic-drexel.csv](data/arrivals/2026-11-04/apostolic-drexel.csv) |
| Drexel | 208 | [drexel.csv](data/arrivals/2026-11-04/drexel.csv) |
| North | 3 | [north.csv](data/arrivals/2026-11-04/north.csv) |
| East | 2 | [east.csv](data/arrivals/2026-11-04/east.csv) |
<!-- SYNC:END -->
