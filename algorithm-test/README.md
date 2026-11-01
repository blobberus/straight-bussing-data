# Algorithm test: can a learned model meet the accuracy goal?

A self-contained test bench for arrival-time prediction on the Straight Bussing data (owner, 2026-11-01: "Based on the
current bus data, construct a test algorithm in the data repo and run a test on the current accuracy requirements. Come
to a loose conclusion as to if it would be more worth it to train an individual algorithm or a deep learning llm to
interpret these bus arrival times. Also construct a list of the 4 biggest arrival lateness perpetrators.")

## What it does

1. Downloads the public forecast tables (`eta-<day>.csv.gz`, one row per minute x bus x stop it reaches in the next 45
   minutes, with Passio's prediction, the timetable and what really happened) from the main repo's releases.
2. Scores every predictor against the **current accuracy requirement**, the owner's 10 minute shrink (see below), with
   the same sampling as the project's daily scoreboard: one sample per arrival and lead range.
3. Compares Passio (what riders see today), the timetable, timetable + current delay, a specialized learned model and a
   deep-learning model, trained only on earlier days and tested on later ones.
4. Ranks what makes buses arrive later than riders were told.

## The accuracy requirement (owner, October 17, 2026)

| How far ahead | Allowed error |
|---|---|
| 30 minutes or more | 3 minutes |
| 20 to 30 minutes | 2 minutes |
| under 20 minutes | 1 minute (under 10 minutes measured once per arrival, about 5 minutes ahead) |

"Most" predictions should pass, and almost none should be too late (the 1% rule, reading B: at most 1% of the lead
later than the bus really came). Full text: the main repo's `docs/GOAL-AND-METHOD.md`.

Status: in progress (2026-11-01). Results and the conclusion will be in `results/` and `CONCLUSION.md`.
