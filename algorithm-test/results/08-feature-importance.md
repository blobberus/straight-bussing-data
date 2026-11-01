# Feature importance: what the specialized model (gbm_q15) leans on

Fitted on 2026-10-12 to 2026-10-25, tested on 2026-10-26 to 2026-10-30 (57,007 samples, all goal bins pooled). Band B: gbm_q15 18.9% (too late 16.9%), Passio 13.8% (too late 13.1%).

Shuffling an input breaks its link to the answer; the drop in band B is what the model loses without it.

| input | what it is | band B drop when shuffled | too late change | share of tree splits |
|---|---|---:|---:|---:|
| tt_minus_passio | timetable time minus Passio's time | +3.31 pts | -0.26 pts | 7% |
| stop (target-encoded lateness) | how much later than Passio this stop usually comes | +1.93 pts | +2.94 pts | 8% |
| stops_away | stops between the bus and the stop | +1.89 pts | +1.73 pts | 9% |
| route (target-encoded lateness) | how much later than Passio this route usually comes | +1.57 pts | -0.42 pts | 7% |
| lead_passio | Passio's predicted minutes ahead | +1.38 pts | +0.25 pts | 16% |
| hour_cos | time of day (cosine) | +1.28 pts | +0.62 pts | 6% |
| delay_s | bus's current delay against the timetable | +1.26 pts | +0.29 pts | 6% |
| hour_sin | time of day (sine) | +1.01 pts | -0.34 pts | 6% |
| lead_ttd | timetable + current delay, minutes ahead | +0.77 pts | -0.48 pts | 3% |
| lead_tt | timetable minutes ahead | +0.69 pts | -0.71 pts | 3% |
| dist_m | distance along the route | +0.55 pts | +0.79 pts | 6% |
| standing_s | how long the bus has stood still | +0.42 pts | +0.36 pts | 3% |
| stop_index | position of the stop on the trip | +0.35 pts | +0.17 pts | 8% |
| last_age_s | age of the last GPS report | +0.23 pts | +0.01 pts | 4% |
| speed_mps | bus speed | +0.21 pts | +0.01 pts | 3% |
| next_trip | arrival is on the bus's next trip | +0.06 pts | +0.08 pts | 1% |
| weekend | weekend | +0.00 pts | +0.00 pts | 1% |
| visit_rank | which visit of the stop on a loop | +0.00 pts | +0.00 pts | 0% |
| crosses_terminal | bus passes the end of the line first | -0.03 pts | +0.04 pts | 1% |
| passio_age_s | age of Passio's prediction | -0.10 pts | -0.01 pts | 2% |
