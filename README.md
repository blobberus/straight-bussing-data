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
_Last sync: 2026-10-29 00:31 UTC · 62,928 arrivals · 21 service days · newest arrival 2026-10-28 19:24:48 (Chicago time)_

| Service day | Arrivals | Routes | Files |
|---|---:|---:|---|
| 2026-10-28 | 3,164 | 13 | [data/arrivals/2026-10-28/](data/arrivals/2026-10-28) |
| 2026-10-27 | 4,151 | 13 | [data/arrivals/2026-10-27/](data/arrivals/2026-10-27) |
| 2026-10-26 | 3,925 | 13 | [data/arrivals/2026-10-26/](data/arrivals/2026-10-26) |
| 2026-10-25 | 856 | 4 | [data/arrivals/2026-10-25/](data/arrivals/2026-10-25) |
| 2026-10-24 | 1,065 | 6 | [data/arrivals/2026-10-24/](data/arrivals/2026-10-24) |
| 2026-10-23 | 3,944 | 14 | [data/arrivals/2026-10-23/](data/arrivals/2026-10-23) |
| 2026-10-22 | 3,757 | 13 | [data/arrivals/2026-10-22/](data/arrivals/2026-10-22) |
| 2026-10-21 | 4,124 | 13 | [data/arrivals/2026-10-21/](data/arrivals/2026-10-21) |
| 2026-10-20 | 3,704 | 13 | [data/arrivals/2026-10-20/](data/arrivals/2026-10-20) |
| 2026-10-19 | 4,070 | 13 | [data/arrivals/2026-10-19/](data/arrivals/2026-10-19) |
| 2026-10-18 | 729 | 4 | [data/arrivals/2026-10-18/](data/arrivals/2026-10-18) |
| 2026-10-17 | 1,027 | 5 | [data/arrivals/2026-10-17/](data/arrivals/2026-10-17) |
| 2026-10-16 | 3,994 | 14 | [data/arrivals/2026-10-16/](data/arrivals/2026-10-16) |
| 2026-10-15 | 3,805 | 13 | [data/arrivals/2026-10-15/](data/arrivals/2026-10-15) |

Routes on 2026-10-28:

| Route | Arrivals | File |
|---|---:|---|
| Red Line/Arts Block | 533 | [red-line-arts-block.csv](data/arrivals/2026-10-28/red-line-arts-block.csv) |
| Downtown Campus Connector | 457 | [downtown-campus-connector.csv](data/arrivals/2026-10-28/downtown-campus-connector.csv) |
| Midway Metra | 455 | [midway-metra.csv](data/arrivals/2026-10-28/midway-metra.csv) |
| 53rd Street Express | 404 | [53rd-street-express.csv](data/arrivals/2026-10-28/53rd-street-express.csv) |
| Apostolic/Drexel | 337 | [apostolic-drexel.csv](data/arrivals/2026-10-28/apostolic-drexel.csv) |
| Friend Center/Metra | 296 | [friend-center-metra.csv](data/arrivals/2026-10-28/friend-center-metra.csv) |
| Apostolic | 280 | [apostolic.csv](data/arrivals/2026-10-28/apostolic.csv) |
| Drexel | 187 | [drexel.csv](data/arrivals/2026-10-28/drexel.csv) |
| South | 68 | [south.csv](data/arrivals/2026-10-28/south.csv) |
| East | 56 | [east.csv](data/arrivals/2026-10-28/east.csv) |
| Central | 40 | [central.csv](data/arrivals/2026-10-28/central.csv) |
| North | 39 | [north.csv](data/arrivals/2026-10-28/north.csv) |
| Regents Express | 12 | [regents-express.csv](data/arrivals/2026-10-28/regents-express.csv) |
<!-- SYNC:END -->
