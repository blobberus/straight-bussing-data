# Algorithm test: can a learned model meet the accuracy goal?

A self-contained test bench for arrival-time prediction on the Straight Bussing data (owner, 2026-11-01: "Based on the
current bus data, construct a test algorithm in the data repo and run a test on the current accuracy requirements. Come
to a loose conclusion as to if it would be more worth it to train an individual algorithm or a deep learning llm to
interpret these bus arrival times. Also construct a list of the 4 biggest arrival lateness perpetrators.")

**The answer is in [`CONCLUSION.md`](CONCLUSION.md).** In short: nothing tested meets the goal (the best safe model has
15 to 27% of predictions inside the allowed error, goal 50%; even fits that see the answers stay under 34%); a small
purpose-built model is worth it and a language model is not; what holds accuracy back is the inputs, not the size of
the model.

## What it does

1. Downloads the public forecast tables (`eta-<day>.csv.gz`, one row per minute x bus x stop it reaches in the next 45
   minutes, with Passio's prediction, the timetable and what really happened) from the main repo's releases.
2. Scores every predictor against the **current accuracy requirement**, the owner's 10 minute shrink (see below), with
   the same sampling as the project's daily scoreboard: one sample per arrival and lead range.
3. Compares Passio (what riders see today), the timetable, timetable + current delay, a specialized learned model
   (boosted trees) and a deep-learning model (a neural network), each trained only on earlier days and tested on later
   ones.
4. Ranks what makes buses arrive later than riders were told.

## The accuracy requirement (owner, October 17, 2026)

| How far ahead | Allowed error |
|---|---|
| 30 minutes or more | 3 minutes |
| 20 to 30 minutes | 2 minutes |
| under 20 minutes | 1 minute (under 10 minutes measured once per arrival, about 5 minutes ahead) |

"Most" predictions should pass, and almost none should be too late (the 1% rule, reading B: at most 1% of the lead
later than the bus really came). Passing both = **band B**: from the allowed error early to 1% of the lead late. The
ship gate adds: never too late more often than Passio, and no route more than 10% worse. Full text: the main repo's
`docs/GOAL-AND-METHOD.md`.

## Results

Data: October 12 to 30, 2026 (19 service days; Passio's predictions are recorded from October 12). Unless a file says
otherwise, the test days are October 20 to 30 and every model is trained only on days before the one it predicts.

| File | Question | Finding |
|---|---|---|
| [01-baselines](results/01-baselines.md) | How do Passio and the timetable do? | Passio's band B: 18%, 10%, 11%, 21%, 12% (0-10, 10-15, 15-20, 20-30, 30-45 min). The timetable is too late far more often. |
| [02-shift-window](results/02-shift-window.md) | (first try, superseded) | Inflated by a leak; kept only as a record. |
| [03-learned-fixed](results/03-learned-fixed.md) | Can a learned correction help? | Boosted trees (15% quantile): 29%, 15%, 13%, 24%, 9%; better than Passio up to 30 min, but too late more often under 15 min. |
| [04-trees-vs-deep](results/04-trees-vs-deep.md) | Trees or a neural network? | The network: 30%, 17%, 16%, 26%, 11%, ahead of the trees by 1 to 3 points and less often too late. |
| [05-by-route](results/05-by-route.md) | Is any route worse than Passio? | The network: none by more than 10%. The trees: three routes at 20-30 min. |
| [06-learning-curve](results/06-learning-curve.md) | Does more data help? | The trees stop improving after 6 days; the network keeps gaining. |
| [07-lateness](results/07-lateness.md) | Who makes buses come later than shown? | The four biggest perpetrators (below). |
| [08-feature-importance](results/08-feature-importance.md) | What does the model lean on? | The timetable-vs-Passio gap, the stop, stops away; the bus's motion adds little. |
| [09-ceiling](results/09-ceiling.md) | How good could any model get with these inputs? | Even fitted on the answers, about a third at best. |
| [10-e24-leak-check](results/10-e24-leak-check.md) | Was the main repo's older headroom estimate (E24) leaky? | Yes; up to 10 points too high, same verdict. |
| [11-safe-setting](results/11-safe-setting.md) | Can the network obey the "never too late more often than Passio" rule? | Nearly: `deep_safe` 27%, 15%, 15%, 26%, 13%, too late within noise of Passio in every bin. The best candidate so far. |
| [12-transitions](results/12-transitions.md) | How do the models do when a line's bus count changes (a bus leaving for a break, its shift end or another line, or joining)? | Every predictor is worse within 15 min of a change at 10 to 45 min ahead (Passio 21% to 12% at 20-30 min, the safe network 28% to 20%); the models keep their lead over Passio. 70% of Passio's times for a bus about to leave never came true. Test days Oct 26 to Nov 5. |

### The four biggest lateness perpetrators (results/07)

Ranked by excess late minutes: how many more minutes later than shown the group's buses came than the same number of
average samples would have.

1. **Trips with no timetable** (91% of them the Downtown Campus Connector): 6.8% of all late minutes in excess; Passio
   is inside band B for only 7% of them.
2. **Buses already more than 10 minutes behind the timetable** (Apostolic/Drexel most of all): 4.3%; band B 8%.
3. **The Red Line/Arts Block**: 3.1%; band B 5.5%, under 1% at Washington Park Arts Incubator and Garfield & Wabash.
4. **The afternoon rush, 3 to 7 PM**: 2.6%; band B 10%.

## How to run

Python 3.11 (what it was run with) with numpy and pandas; PyTorch for the neural network (CPU is enough). No scikit-learn needed:
the boosted trees are in `gbm.py`.

```
python algorithm-test/run_all.py --checks     # fetch the data, run the tests and the scoreboard check
python algorithm-test/run_all.py              # everything, in order (about an hour on a laptop)
python algorithm-test/run_all.py --only 07    # one step
python algorithm-test/evaluate.py --models passio,gbm_q15,deep_q15 --by-route   # your own comparison
```

The tables (about 6 MB per service day, 118 MB for October 12 to 30) go to `algorithm-test/cache/` (not committed).

## Files

| File | What |
|---|---|
| `fetch.py` | downloads the forecast tables |
| `scoring.py`, `test_scoring.py` | the accuracy requirement as code, and its tests |
| `dataset.py`, `validate.py` | loading and sampling (one sample per arrival and lead range); `validate.py` checks every cell against the main repo's daily scoreboard |
| `predictors.py` | Passio, timetable, timetable + delay, and the registry every model joins |
| `features.py` | the inputs a model may use: only what is known at the minute of the prediction |
| `models.py`, `gbm.py`, `test_gbm.py` | the specialized models: a per-stop correction and quantile boosted trees (numpy only) |
| `model_deep.py` | the neural networks (PyTorch) |
| `test_leak.py` | proves no model looks at the real arrival (scrambles it and checks the predictions do not move) |
| `evaluate.py` | rolling-origin evaluation with confidence intervals over days, per route on request |
| `learning_curve.py`, `lateness.py`, `importance.py`, `ceiling.py`, `e24_leak_check.py` | the other experiments |
| `transitions.py` | every model in transition periods vs normal ones and on buses about to leave (joins the main repo's `data/labeled/transitions/transitions.csv`; RouteKnower E29) |
| `run_all.py` | runs everything in order |

## Caveats

- 19 days, autumn quarter only, no snow yet. Rerun as the data grows (`run_all.py`).
- The first two learned runs leaked the real arrival through the lead range (fixed 2026-11-01; `test_leak.py` now
  guards it). Results from before the fix are marked superseded.
- `deep_safe` (results/11) has five quantiles set by hand from results/04, which used the same test days: slightly
  optimistic.
- The sample is the scoreboard's (one prediction per arrival and lead range), not every prediction a rider sees.

Unofficial; not affiliated with the University of Chicago. Official service information: 773.702.8181.
