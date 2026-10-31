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
_Last sync: 2026-10-31 01:57 UTC · 75,625 arrivals · 23 service days · newest arrival 2026-10-30 20:39:10 (Chicago time)_

| Service day | Arrivals | Routes | Files |
|---|---:|---:|---|
| 2026-10-30 | 3,668 | 14 | [data/arrivals/2026-10-30/](data/arrivals/2026-10-30) |
| 2026-10-29 | 4,301 | 13 | [data/arrivals/2026-10-29/](data/arrivals/2026-10-29) |
| 2026-10-28 | 3,999 | 13 | [data/arrivals/2026-10-28/](data/arrivals/2026-10-28) |
| 2026-10-27 | 4,539 | 13 | [data/arrivals/2026-10-27/](data/arrivals/2026-10-27) |
| 2026-10-26 | 4,253 | 13 | [data/arrivals/2026-10-26/](data/arrivals/2026-10-26) |
| 2026-10-25 | 899 | 4 | [data/arrivals/2026-10-25/](data/arrivals/2026-10-25) |
| 2026-10-24 | 1,107 | 6 | [data/arrivals/2026-10-24/](data/arrivals/2026-10-24) |
| 2026-10-23 | 4,233 | 14 | [data/arrivals/2026-10-23/](data/arrivals/2026-10-23) |
| 2026-10-22 | 3,903 | 13 | [data/arrivals/2026-10-22/](data/arrivals/2026-10-22) |
| 2026-10-21 | 4,267 | 13 | [data/arrivals/2026-10-21/](data/arrivals/2026-10-21) |
| 2026-10-20 | 3,943 | 13 | [data/arrivals/2026-10-20/](data/arrivals/2026-10-20) |
| 2026-10-19 | 4,399 | 13 | [data/arrivals/2026-10-19/](data/arrivals/2026-10-19) |
| 2026-10-18 | 747 | 4 | [data/arrivals/2026-10-18/](data/arrivals/2026-10-18) |
| 2026-10-17 | 1,063 | 5 | [data/arrivals/2026-10-17/](data/arrivals/2026-10-17) |

Routes on 2026-10-30:

| Route | Arrivals | File |
|---|---:|---|
| Red Line/Arts Block | 577 | [red-line-arts-block.csv](data/arrivals/2026-10-30/red-line-arts-block.csv) |
| Downtown Campus Connector | 502 | [downtown-campus-connector.csv](data/arrivals/2026-10-30/downtown-campus-connector.csv) |
| Midway Metra | 466 | [midway-metra.csv](data/arrivals/2026-10-30/midway-metra.csv) |
| Apostolic/Drexel | 464 | [apostolic-drexel.csv](data/arrivals/2026-10-30/apostolic-drexel.csv) |
| 53rd Street Express | 422 | [53rd-street-express.csv](data/arrivals/2026-10-30/53rd-street-express.csv) |
| Friend Center/Metra | 370 | [friend-center-metra.csv](data/arrivals/2026-10-30/friend-center-metra.csv) |
| Apostolic | 308 | [apostolic.csv](data/arrivals/2026-10-30/apostolic.csv) |
| Drexel | 154 | [drexel.csv](data/arrivals/2026-10-30/drexel.csv) |
| South | 139 | [south.csv](data/arrivals/2026-10-30/south.csv) |
| East | 82 | [east.csv](data/arrivals/2026-10-30/east.csv) |
| Central | 72 | [central.csv](data/arrivals/2026-10-30/central.csv) |
| North | 63 | [north.csv](data/arrivals/2026-10-30/north.csv) |
| Regents Express | 41 | [regents-express.csv](data/arrivals/2026-10-30/regents-express.csv) |
| South Loop Shuttle | 8 | [south-loop-shuttle.csv](data/arrivals/2026-10-30/south-loop-shuttle.csv) |
<!-- SYNC:END -->
