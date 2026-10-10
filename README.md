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

Column meanings: `methodology/docs/DATA.md` ("Schema"). Times are good to about +-10 s; `segment_s` is the time from
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
_Last sync: 2026-10-10 01:08 UTC · 6,451 arrivals · 2 service days · newest arrival 2026-10-09 18:35:40 (Chicago time)_

| Service day | Arrivals | Routes | Files |
|---|---:|---:|---|
| 2026-10-09 | 2,849 | 14 | [data/arrivals/2026-10-09/](data/arrivals/2026-10-09) |
| 2026-10-08 | 3,602 | 13 | [data/arrivals/2026-10-08/](data/arrivals/2026-10-08) |

Routes on 2026-10-09:

| Route | Arrivals | File |
|---|---:|---|
| Midway Metra | 461 | [midway-metra.csv](data/arrivals/2026-10-09/midway-metra.csv) |
| 53rd Street Express | 425 | [53rd-street-express.csv](data/arrivals/2026-10-09/53rd-street-express.csv) |
| Downtown Campus Connector | 409 | [downtown-campus-connector.csv](data/arrivals/2026-10-09/downtown-campus-connector.csv) |
| Apostolic/Drexel | 320 | [apostolic-drexel.csv](data/arrivals/2026-10-09/apostolic-drexel.csv) |
| Friend Center/Metra | 320 | [friend-center-metra.csv](data/arrivals/2026-10-09/friend-center-metra.csv) |
| Apostolic | 254 | [apostolic.csv](data/arrivals/2026-10-09/apostolic.csv) |
| Red Line/Arts Block | 254 | [red-line-arts-block.csv](data/arrivals/2026-10-09/red-line-arts-block.csv) |
| Drexel | 143 | [drexel.csv](data/arrivals/2026-10-09/drexel.csv) |
| Central | 111 | [central.csv](data/arrivals/2026-10-09/central.csv) |
| East | 57 | [east.csv](data/arrivals/2026-10-09/east.csv) |
| South | 51 | [south.csv](data/arrivals/2026-10-09/south.csv) |
| North | 34 | [north.csv](data/arrivals/2026-10-09/north.csv) |
| Regents Express | 7 | [regents-express.csv](data/arrivals/2026-10-09/regents-express.csv) |
| South Loop Shuttle | 3 | [south-loop-shuttle.csv](data/arrivals/2026-10-09/south-loop-shuttle.csv) |
<!-- SYNC:END -->
