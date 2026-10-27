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
_Last sync: 2026-10-27 04:59 UTC · 55,612 arrivals · 19 service days · newest arrival 2026-10-26 23:56:54 (Chicago time)_

| Service day | Arrivals | Routes | Files |
|---|---:|---:|---|
| 2026-10-26 | 3,924 | 13 | [data/arrivals/2026-10-26/](data/arrivals/2026-10-26) |
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
| 2026-10-14 | 3,995 | 13 | [data/arrivals/2026-10-14/](data/arrivals/2026-10-14) |
| 2026-10-13 | 3,998 | 13 | [data/arrivals/2026-10-13/](data/arrivals/2026-10-13) |

Routes on 2026-10-26:

| Route | Arrivals | File |
|---|---:|---|
| Apostolic/Drexel | 655 | [apostolic-drexel.csv](data/arrivals/2026-10-26/apostolic-drexel.csv) |
| Downtown Campus Connector | 587 | [downtown-campus-connector.csv](data/arrivals/2026-10-26/downtown-campus-connector.csv) |
| Red Line/Arts Block | 497 | [red-line-arts-block.csv](data/arrivals/2026-10-26/red-line-arts-block.csv) |
| 53rd Street Express | 418 | [53rd-street-express.csv](data/arrivals/2026-10-26/53rd-street-express.csv) |
| Midway Metra | 380 | [midway-metra.csv](data/arrivals/2026-10-26/midway-metra.csv) |
| Friend Center/Metra | 302 | [friend-center-metra.csv](data/arrivals/2026-10-26/friend-center-metra.csv) |
| Apostolic | 220 | [apostolic.csv](data/arrivals/2026-10-26/apostolic.csv) |
| Drexel | 203 | [drexel.csv](data/arrivals/2026-10-26/drexel.csv) |
| Central | 194 | [central.csv](data/arrivals/2026-10-26/central.csv) |
| East | 185 | [east.csv](data/arrivals/2026-10-26/east.csv) |
| South | 132 | [south.csv](data/arrivals/2026-10-26/south.csv) |
| North | 111 | [north.csv](data/arrivals/2026-10-26/north.csv) |
| Regents Express | 40 | [regents-express.csv](data/arrivals/2026-10-26/regents-express.csv) |
<!-- SYNC:END -->
