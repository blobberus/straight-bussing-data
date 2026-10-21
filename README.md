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
_Last sync: 2026-10-21 17:50 UTC · 39,624 arrivals · 14 service days · newest arrival 2026-10-21 12:49:19 (Chicago time)_

| Service day | Arrivals | Routes | Files |
|---|---:|---:|---|
| 2026-10-21 | 1,682 | 8 | [data/arrivals/2026-10-21/](data/arrivals/2026-10-21) |
| 2026-10-20 | 3,704 | 13 | [data/arrivals/2026-10-20/](data/arrivals/2026-10-20) |
| 2026-10-19 | 4,070 | 13 | [data/arrivals/2026-10-19/](data/arrivals/2026-10-19) |
| 2026-10-18 | 729 | 4 | [data/arrivals/2026-10-18/](data/arrivals/2026-10-18) |
| 2026-10-17 | 1,027 | 5 | [data/arrivals/2026-10-17/](data/arrivals/2026-10-17) |
| 2026-10-16 | 3,994 | 14 | [data/arrivals/2026-10-16/](data/arrivals/2026-10-16) |
| 2026-10-15 | 3,805 | 13 | [data/arrivals/2026-10-15/](data/arrivals/2026-10-15) |
| 2026-10-14 | 3,995 | 13 | [data/arrivals/2026-10-14/](data/arrivals/2026-10-14) |
| 2026-10-13 | 3,998 | 13 | [data/arrivals/2026-10-13/](data/arrivals/2026-10-13) |
| 2026-10-12 | 4,000 | 13 | [data/arrivals/2026-10-12/](data/arrivals/2026-10-12) |
| 2026-10-11 | 784 | 4 | [data/arrivals/2026-10-11/](data/arrivals/2026-10-11) |
| 2026-10-10 | 1,022 | 5 | [data/arrivals/2026-10-10/](data/arrivals/2026-10-10) |
| 2026-10-09 | 3,256 | 14 | [data/arrivals/2026-10-09/](data/arrivals/2026-10-09) |
| 2026-10-08 | 3,558 | 13 | [data/arrivals/2026-10-08/](data/arrivals/2026-10-08) |

Routes on 2026-10-21:

| Route | Arrivals | File |
|---|---:|---|
| Red Line/Arts Block | 287 | [red-line-arts-block.csv](data/arrivals/2026-10-21/red-line-arts-block.csv) |
| 53rd Street Express | 248 | [53rd-street-express.csv](data/arrivals/2026-10-21/53rd-street-express.csv) |
| Downtown Campus Connector | 241 | [downtown-campus-connector.csv](data/arrivals/2026-10-21/downtown-campus-connector.csv) |
| Midway Metra | 227 | [midway-metra.csv](data/arrivals/2026-10-21/midway-metra.csv) |
| Apostolic | 212 | [apostolic.csv](data/arrivals/2026-10-21/apostolic.csv) |
| Drexel | 208 | [drexel.csv](data/arrivals/2026-10-21/drexel.csv) |
| Friend Center/Metra | 166 | [friend-center-metra.csv](data/arrivals/2026-10-21/friend-center-metra.csv) |
| Apostolic/Drexel | 93 | [apostolic-drexel.csv](data/arrivals/2026-10-21/apostolic-drexel.csv) |
<!-- SYNC:END -->
