# Conclusion: a specialized model, not a language model (loose, 2026-11-01)

The owner asked for a loose conclusion: is it more worth it to train an individual algorithm or a deep-learning LLM to
interpret the bus arrival times? And which four things make buses arrive later than riders were told?

**Short answer: train a small, specialized model on the bus data (a small neural network or boosted trees; the two
are close). Training or prompting a large language model is not worth it. And no model, of any size, meets the goal
on today's inputs: the next real gain comes from better inputs about each bus, not from a bigger model.**

Data: the public forecast tables, October 12 to 30, 2026 (19 service days, 183,904 scored samples). Every model was
trained only on days before the day it predicted. Details and every number: [`README.md`](README.md) and `results/`.

## 1. Where things stand against the goal

Band B = inside the allowed error early (1 min under 20 min ahead, 2 min at 20 to 30, 3 min beyond) and at most 1% of
the lead late. Goal: most (50%) of predictions in band B, and never too late more often than Passio.

| Predictor (test days Oct 20 to 30) | 0-10 min | 10-15 | 15-20 | 20-30 | 30-45 | Too late vs Passio |
|---|---:|---:|---:|---:|---:|---|
| Passio (what riders see today) | 18.3% | 9.8% | 10.7% | 20.7% | 12.0% | (reference) |
| Printed timetable + current delay | 12.1% | 8.7% | 10.8% | 20.8% | 21.8% | +24 to +30 points up to 30 min: unsafe |
| Boosted trees, 15% quantile (`gbm_q15`) | 29.2% | 15.1% | 13.0% | 24.0% | 8.5% | +7.2 points under 10 min |
| Small neural network, 15% quantile (`deep_q15`) | 29.9% | 16.9% | 16.0% | 26.0% | 10.9% | +3.6 under 10 min, +1.9 at 15-20 |
| The same network tuned to the safety rule (`deep_safe`) | 26.8% | 14.7% | 15.0% | 26.2% | 13.3% | -1.3 to +0.9, all within noise |
| Network chasing band B (`deep_q30`) | 31.1% | 21.0% | 19.8% | 30.9% | 18.7% | +0.1 to +17.9: unsafe |

And the ceiling (results/09): fitted on data that **includes the answers** of the day it is graded on, which no real
model can do, the best of three model types reaches 31.9%, 23.1%, 22.5%, 33.5% and 24.0% on October 26 to 30 (Passio
16.8%, 9.5%, 10.1%, 19.4%, 11.9% on the same days).

So:
- **Nothing meets the goal at any lead.** The best safe model is about 1.5 times as often within the allowed error as
  Passio under 10 minutes and about 1.3 times at 20 to 30 minutes, but reaches only a quarter to a third of predictions
  where the goal asks for half.
- **A learned correction is clearly worth having**: `deep_safe` gains 4 to 9 points over Passio from 0 to 30 minutes
  ahead without being measurably more often too late.

## 2. Why a specialized model and not a language model

1. **The problem is a table of numbers, not text.** Each prediction is about 20 numbers known at that minute (Passio's
   time, the timetable, the bus's delay, stops away, distance, time of day, the stop) and one number to predict, with
   hundreds of thousands of labeled examples. That is exactly what purpose-built models do best. Benchmarks of models
   on tables (Grinsztajn, Oyallon and Varoquaux, NeurIPS 2022) find boosted trees usually ahead even of neural
   networks designed for tables; language models that read table rows as text are useful mainly when there are only a
   handful of examples (TabLLM, Hegselmann et al., AISTATS 2023). Here there are 180,000 scored samples and about
   300,000 training rows (a random quarter of 1.2 million query minutes).
2. **Model size is not what holds accuracy back.** Trees and the network land within 1 to 3 points of each other, and
   even fits that see the answers stay under 34% (section 1). A language model would get the same inputs, so it would
   meet the same ceiling, at far greater cost.
3. **It has to fit the app.** The website is static (no server) and the iPhone app sends nothing about the rider. The
   network tested here has 32,842 weights: a small file, plain arithmetic, microseconds per prediction, easy to port
   to the web code and to Swift, all on the phone. A language model needs a hosted GPU, costs money per prediction,
   adds seconds of delay to times that refresh every 10 to 20 seconds, and would mean sending live requests off the
   device.
4. **Safety needs a predictable model.** Rule one of the ship checklist is honesty about times. A specialized model's
   errors are measured, stable and reproducible (the network reran to the same numbers to the decimal) and can be
   checked for leaks (`test_leak.py`); a language model can give a fluent, confident number with no fixed link to its
   inputs, which is the dangerous kind of wrong.
5. **Where a language model could help, it is a small side job:** reading the operator's alert text ("bus out of
   service", "detour on 55th Street") into simple flags the specialized model uses. Alerts are rare and short; a few
   rules may do the same.

## 3. Trees or a small network?

Both count as "an individual algorithm". The **small network** is the lead candidate: 1 to 3 points ahead of the trees
in band B, less often too late, no route more than 10% worse than Passio (the trees fail three routes at 20 to 30
minutes, results/05), and it **keeps improving with more days** where the trees stop after about 6 (results/06). The
trees stay useful as a cross-check and are the simplest to explain. Neither is ready to ship: the goal is not met, and
`deep_safe`'s quantiles were set by hand from runs on the same test days.

## 4. The four biggest lateness perpetrators (results/07)

89% of samples came later than Passio showed: 955,266 late minutes over 183,904 samples. Ranked by **excess** late
minutes (beyond what the same number of average samples would have):

| # | Perpetrator | Excess late minutes | Passio band B in it / elsewhere | Why (from E20, E24, DC-020 and the tables) |
|---:|---|---:|---|---|
| 1 | **Trips with no timetable**, 91% of them the **Downtown Campus Connector** | 6.8% of all | 7.2% / 13.9% | Frequency trips: no printed time to fall back on, and Passio adds drive times with no time at stops on a long run downtown |
| 2 | **Buses already more than 10 minutes behind the timetable** (Apostolic/Drexel the most, 27%) | 4.3% | 7.6% / 14.1% | Passio starts the next trip at its printed time whatever the delay, so a late bus is shown on time again |
| 3 | **Red Line/Arts Block** | 3.1% | 5.5% / 13.8% | Worst at Washington Park Arts Incubator and Garfield & Wabash: about 10 minutes later than shown, 97 to 98% of samples off by more than 3 minutes |
| 4 | **The afternoon rush, 3 to 7 PM** | 2.6% | 10.2% / 14.0% | Likely traffic and crowded stops (not measured here: no traffic input yet) |

Even if all four did as well as everything else, Passio's band B would rise only from 12.9% to 17.5%: the shortfall is
everywhere, these are just the worst parts of it.

## 5. What would move the number

From the perpetrators and from what the model leans on (results/08: the timetable-vs-Passio gap and the stop matter;
the bus's own motion adds little), the inputs worth adding to the forecast tables, in order:

1. **Lateness carried into the next trip**: when a late bus will really leave the end of its line (layover length,
   how late it arrived there). Targets perpetrator 2.
2. **Spacing for frequency trips**: time since the last bus left the stop, distance to the bus ahead. Targets 1.
3. **Time spent at stops** (dwell) learned per stop and hour, including the two Red Line stops. Targets 3.
4. **Traffic and events** (the context data already collected) and **bus count changes** (`bus_changes.csv`, since
   October 30). Targets 4 and the 2-to-1 drops of DC-020.

Then rerun this bench (`python algorithm-test/run_all.py`) and the ceiling: if better inputs do not lift the ceiling
well past a third, the goal itself is worth a second look with the owner.

## 6. Transition time: when a line's bus count changes (results/12, added 2026-11-06)

The owner asked to log what buses do at transition time (a bus leaving a line for a break, its shift end or another
line, or a bus joining) and to test the algorithms against it. The main repo's RouteKnower E29 labeled every change of
October 10 to November 5 (`data/labeled/transitions/transitions.csv` there); `transitions.py` joins it to the samples
and scores every model on the same rows. Test days October 26 to November 5 (11 days, 101,853 samples; 18.5% of them
within 15 minutes of a transition on their line).

| Band B, normal / transition (within 15 min of a change) | 0-10 min | 10-15 | 15-20 | 20-30 | 30-45 |
|---|---|---|---|---|---|
| Passio | 15.7 / 15.0% | 10.4 / 6.8% | 10.3 / 7.6% | 21.0 / 12.1% | 14.1 / 6.1% |
| Timetable + delay | 11.3 / 13.0% | 8.8 / 7.3% | 11.2 / 10.4% | 21.0 / 17.8% | 23.7 / 10.6% |
| Boosted trees (`gbm_q15`) | 26.5 / 24.5% | 14.8 / 13.3% | 12.7 / 10.1% | 24.2 / 15.7% | 9.6 / 6.2% |
| Network (`deep_q15`) | 28.1 / 25.9% | 17.2 / 14.4% | 15.9 / 13.5% | 27.1 / 19.0% | 8.4 / 11.4% |
| Network, safe setting (`deep_safe`) | 25.7 / 24.1% | 15.1 / 13.9% | 14.9 / 12.2% | 27.7 / 19.5% | 11.0 / 12.1% |

- **Every predictor loses accuracy in transition time at 10 to 45 minutes ahead**, most at 20 to 30 minutes (Passio
  21.0% to 12.1%, the safe network 27.7% to 19.5%); under 10 minutes the difference is small. Too late is not higher
  there (Passio 4.2% vs 7.4% at 20-30). A long-range prediction made just before a bus leaves or joins is the weak spot.
- **The learned models keep their lead in transition time**: the safe network is ahead of Passio by 9.1, 7.1, 4.6, 7.4
  and 6.0 points there (vs 10.0, 4.7, 4.6, 6.7 and -3.1 in normal time), so transitions are not where they fail; they
  just do not fix them. Rows of a bus that leaves its line within 30 minutes (1.8% of samples) look like the rest.
- **Passio's times for buses around a leave are mostly false**: of everything Passio showed for a bus in the 45
  minutes before it left its line for good, 70.0% never came true (55.7% in the 45 minutes after; 35.5% for other
  buses). These rows are not in the scored sample (they have no arrival), which is why the main repo's app now drops
  the times of a bus that has sent no report for 15 minutes (`web/js/core/transition.js`: 98.8% of those times never
  came true).
- **What to try next**: give the models the transition columns the forecast tables carry from November 6
  (`transition_min` is ground truth and must never be a feature; `added_recently`, `break_window`,
  `leave_spot_dist_m`, `absent_s` are known live) and rerun this step; which bus is about to leave could not be told
  ahead reliably (E29: at best about 30% precision), so "a bus of this line usually leaves around now" is the realistic
  input, not "this bus leaves".

## 7. Flagged lines (results/13, added 2026-11-11)

The main repo's flagged-lines registry (`data/labeled/flags/flagged_lines.csv`: RouteKnower E30 odd bus behavior at
transition times, E31 large prediction misses) names 77 problems on 14 lines, each narrowed to its stops, hours, days,
buses and minutes ahead. Step 13 scores every model on each one as its own slice (test days October 30 to November 9;
a bin decides only with 30+ samples). RouteKnower 6.4: a model that loses on a flagged slice is not shipped.

- **No candidate passes.** Of 55 slices with enough rows, the safe network holds on 21 and loses on 34 (10 of them
  high severity); the trees lose on 38, the plain network on 42, timetable + delay on 46.
- **How it loses**: mostly too late more often than Passio (23 of the 34), for example Drexel when the bus is already
  behind (5.1% vs 2.1% under 10 min), Apostolic around GPS position jumps and the 53rd Street Express at 15-20 min
  (15.8% vs 8.6%); and band B well below Passio on South while a bus lingers out of service at night (13.0% vs 19.7%
  at 10-15 min), on Regents Express's late misses (about half of Passio's band B at 10 to 30 min) and on East and South
  early misses at 10-15 min.
- **Where it holds**: Central (5 flags), Friend Center/Metra (4), East (3); and 7 of the 8 flags about Passio showing a time
  only under another trip id of the same bus (Drexel is the exception: too late 10.7% vs 6.9% under 10 min).
- **What to try next**: the transition and coverage columns as inputs (section 6), then rerun step 13 after every
  weekly flag refresh (the data repo's `findings/run_findings.py` rebuilds the registry each Monday).

## 8. What this does not settle

- 19 days of autumn quarter: no snow, no exam weeks, no breaks yet.
- The sample is the scoreboard's (one prediction per arrival and lead range).
- The ceiling is an upper bound for three model types on these inputs, strong evidence but not a proof about every
  possible model.
- The two first learned runs leaked the real arrival (fixed the same day; `test_leak.py` guards it now). The same leak
  inflated the main repo's older E24 headroom numbers by up to 10 points (results/10); its verdict stands.

Unofficial; not affiliated with the University of Chicago. Official service information: 773.702.8181.
