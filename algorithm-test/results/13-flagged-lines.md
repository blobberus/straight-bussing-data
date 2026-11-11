# Flagged lines: every model on each flagged slice

Test days: 2026-10-30 to 2026-11-09 (11 days, 83,002 samples; each model trained only on earlier days). Flags: the main repo's data/labeled/flags/flagged_lines.csv, 99 active (open or watch); each is the flag's line narrowed by its scope (README there). RouteKnower.md 6.4: a model that wins on average but loses on a flagged slice is not shipped.

## Which model loses where

Loses = in a bin with 30+ samples, band B more than 10% (relative) below Passio's, or too late more often than Passio by more than 1 point.

| model | flagged slices it loses on (ship gate: not shipped while any) |
|---|---|
| timetable_delay | `prediction_miss:first_stop_next_trip_times:4346`, `prediction_miss:large_early_miss:4346`, `prediction_miss:stops_without_predictions:4346`, `transition:position_jump:5702`, `prediction_miss:other_trip_times:6126`, `transition:after_hours:1078`, `prediction_miss:worse_when_behind:5701`, `prediction_miss:large_early_miss:1077`, `prediction_miss:stops_without_predictions:1077`, `prediction_miss:large_late_miss:5699`, `prediction_miss:large_late_miss:5715`, `display:false_hide_idle_serving_bus:1076`, `prediction_miss:large_early_miss:1076`, `transition:linger_not_in_service:1076`, `prediction_miss:worse_when_behind:1076`, `transition:after_hours:5702`, `display:bus_number_churn:5702`, `transition:staying_bus_late_after_drop:5702`, `transition:bunching_after_add:6126`, `prediction_miss:large_late_miss:6126`, `transition:off_route_drive:6126`, `transition:extra_bus_added:1078`, `prediction_miss:stops_without_predictions:1078`, `prediction_miss:worse_when_behind:1078`, `display:ghost_times_after_leave:5701`, `prediction_miss:stops_without_predictions:5701`, `transition:extra_bus_added:1077`, `prediction_miss:worse_when_behind:1077`, `transition:extra_bus_added:5700`, `prediction_miss:first_stop_next_trip_times:5700`, `transition:service_start_missing:5700`, `transition:timetable_add_missed:5703`, `prediction_miss:stops_without_predictions:1075`, `transition:timetable_add_missed:1075`, `prediction_miss:worse_when_behind:1075`, `transition:extra_bus_added:5699`, `display:ghost_bus_on_map:5699`, `display:ghost_times_after_leave:5699`, `transition:off_route_drive:1076`, `display:planner_recommends_leaving_bus:1076`, `display:false_hide_idle_serving_bus:1078`, `prediction_miss:large_late_miss:5701`, `prediction_miss:other_trip_times:5701`, `transition:staying_bus_late_after_drop:5701`, `transition:unscheduled_leave:5701`, `prediction_miss:worse_near_transitions:5700`, `prediction_miss:worse_when_behind:5700`, `prediction_miss:large_late_miss:5703`, `transition:service_start_late:5703`, `display:false_hide_gone_serving_bus:5699`, `prediction_miss:first_stop_next_trip_times:5699`, `transition:wrong_line_label:5699`, `prediction_miss:first_stop_next_trip_times:1076`, `transition:unscheduled_leave:1076` |
| gbm_q15 | `prediction_miss:large_early_miss:4346`, `prediction_miss:stops_without_predictions:4346`, `transition:position_jump:5702`, `prediction_miss:other_trip_times:6126`, `transition:after_hours:1078`, `transition:sparse_reporting:5704`, `prediction_miss:worse_when_behind:5701`, `prediction_miss:large_early_miss:1077`, `prediction_miss:large_late_miss:5699`, `prediction_miss:large_late_miss:5715`, `display:false_hide_idle_serving_bus:1076`, `prediction_miss:large_early_miss:1076`, `transition:linger_not_in_service:1076`, `prediction_miss:worse_when_behind:1076`, `transition:after_hours:5702`, `display:bus_number_churn:5702`, `transition:staying_bus_late_after_drop:5702`, `prediction_miss:large_late_miss:6126`, `transition:off_route_drive:6126`, `transition:extra_bus_added:1078`, `prediction_miss:stops_without_predictions:1078`, `prediction_miss:large_early_miss:5704`, `display:ghost_times_after_leave:5701`, `prediction_miss:stops_without_predictions:5701`, `transition:extra_bus_added:5700`, `transition:service_start_missing:5700`, `transition:timetable_add_missed:5703`, `prediction_miss:stops_without_predictions:1075`, `transition:timetable_add_missed:1075`, `prediction_miss:worse_when_behind:1075`, `transition:extra_bus_added:5699`, `display:ghost_bus_on_map:5699`, `display:ghost_times_after_leave:5699`, `transition:off_route_drive:1076`, `display:planner_recommends_leaving_bus:1076`, `prediction_miss:other_trip_times:5701`, `transition:staying_bus_late_after_drop:5701`, `transition:unscheduled_leave:5701`, `prediction_miss:worse_near_transitions:5700`, `prediction_miss:worse_when_behind:5700`, `prediction_miss:large_late_miss:5703`, `transition:service_start_late:5703`, `display:false_hide_gone_serving_bus:5699`, `transition:wrong_line_label:5699`, `transition:unscheduled_leave:1076` |
| deep_q15 | `prediction_miss:large_early_miss:4346`, `prediction_miss:stops_without_predictions:4346`, `transition:position_jump:5702`, `prediction_miss:other_trip_times:6126`, `display:planner_recommends_leaving_bus:5704`, `transition:sparse_reporting:5704`, `prediction_miss:worse_when_behind:5701`, `prediction_miss:large_late_miss:5699`, `prediction_miss:large_late_miss:5715`, `prediction_miss:large_early_miss:1076`, `transition:linger_not_in_service:1076`, `prediction_miss:worse_when_behind:1076`, `transition:after_hours:5702`, `display:bus_number_churn:5702`, `transition:staying_bus_late_after_drop:5702`, `transition:bunching_after_add:6126`, `prediction_miss:large_late_miss:6126`, `transition:off_route_drive:6126`, `transition:extra_bus_added:1078`, `prediction_miss:stops_without_predictions:1078`, `prediction_miss:worse_when_behind:1078`, `display:bus_number_churn:5704`, `transition:frozen_gps:5704`, `display:ghost_times_after_leave:5704`, `prediction_miss:large_early_miss:5704`, `prediction_miss:large_late_miss:5704`, `display:ghost_times_after_leave:5701`, `transition:extra_bus_added:1077`, `prediction_miss:worse_when_behind:1077`, `transition:extra_bus_added:5700`, `prediction_miss:first_stop_next_trip_times:5700`, `transition:service_start_missing:5700`, `transition:timetable_add_missed:5703`, `prediction_miss:stops_without_predictions:1075`, `transition:timetable_add_missed:1075`, `prediction_miss:worse_when_behind:1075`, `transition:extra_bus_added:5699`, `display:ghost_bus_on_map:5699`, `display:ghost_times_after_leave:5699`, `transition:off_route_drive:1076`, `display:planner_recommends_leaving_bus:1076`, `display:false_hide_idle_serving_bus:1078`, `display:ghost_bus_on_map:5704`, `prediction_miss:other_trip_times:5701`, `transition:staying_bus_late_after_drop:5701`, `transition:unscheduled_leave:5701`, `prediction_miss:worse_near_transitions:5700`, `prediction_miss:worse_when_behind:5700`, `prediction_miss:large_late_miss:5703`, `transition:service_start_late:5703`, `display:false_hide_gone_serving_bus:5699`, `transition:wrong_line_label:5699`, `transition:unscheduled_leave:1076` |
| deep_safe | `prediction_miss:large_early_miss:4346`, `transition:position_jump:5702`, `display:planner_recommends_leaving_bus:5704`, `transition:sparse_reporting:5704`, `prediction_miss:worse_when_behind:5701`, `prediction_miss:large_early_miss:1077`, `prediction_miss:large_late_miss:5699`, `prediction_miss:large_late_miss:5715`, `prediction_miss:large_early_miss:1076`, `transition:linger_not_in_service:1076`, `prediction_miss:worse_when_behind:1076`, `transition:after_hours:5702`, `display:bus_number_churn:5702`, `transition:staying_bus_late_after_drop:5702`, `transition:bunching_after_add:6126`, `prediction_miss:large_late_miss:6126`, `transition:off_route_drive:6126`, `transition:extra_bus_added:1078`, `display:bus_number_churn:5704`, `transition:frozen_gps:5704`, `display:ghost_times_after_leave:5704`, `prediction_miss:large_early_miss:5704`, `prediction_miss:large_late_miss:5704`, `display:ghost_times_after_leave:5701`, `prediction_miss:worse_when_behind:1077`, `transition:extra_bus_added:5700`, `transition:timetable_add_missed:5703`, `prediction_miss:stops_without_predictions:1075`, `transition:timetable_add_missed:1075`, `prediction_miss:worse_when_behind:1075`, `transition:extra_bus_added:5699`, `display:ghost_bus_on_map:5699`, `display:ghost_times_after_leave:5699`, `transition:off_route_drive:1076`, `display:planner_recommends_leaving_bus:1076`, `display:false_hide_idle_serving_bus:1078`, `display:ghost_bus_on_map:5704`, `prediction_miss:other_trip_times:5701`, `transition:staying_bus_late_after_drop:5701`, `transition:unscheduled_leave:5701`, `prediction_miss:large_late_miss:5703`, `transition:service_start_late:5703`, `display:false_hide_gone_serving_bus:5699`, `transition:wrong_line_label:5699`, `transition:unscheduled_leave:1076` |

## All rows (for comparison)

| rows | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | model |
|---|---|---:|---|---|---|---|---|---|
| (all rows) | all lines | 83,002 | 14.6% / 34.7% (24,120) | 10.9% / 18.8% (20,215) | 10.8% / 11.2% (18,304) | 22.4% / 8.2% (15,193) | 14.3% / 2.4% (5,170) | passio |
| (all rows) | all lines | 83,002 | 10.6% / 45.0% (24,120) | 8.4% / 38.6% (20,215) | 11.1% / 37.6% (18,304) | 21.4% / 33.8% (15,193) | 20.8% / 10.6% (5,170) | timetable_delay |
| (all rows) | all lines | 83,002 | 25.7% / 28.0% (24,120) | 14.2% / 15.2% (20,215) | 12.3% / 10.1% (18,304) | 24.3% / 6.3% (15,193) | 9.5% / 1.3% (5,170) | gbm_q15 |
| (all rows) | all lines | 83,002 | 28.9% / 22.6% (24,120) | 17.4% / 14.3% (20,215) | 16.2% / 11.1% (18,304) | 27.4% / 6.9% (15,193) | 8.8% / 0.8% (5,170) | deep_q15 |
| (all rows) | all lines | 83,002 | 27.2% / 18.0% (24,120) | 15.7% / 13.3% (20,215) | 15.4% / 11.1% (18,304) | 27.8% / 8.7% (15,193) | 12.1% / 1.5% (5,170) | deep_safe |

## Each flagged slice

Each cell: band B / too late (samples). Band B = inside the allowed error early to 1% of the lead late (the goal: 50% or more); too late = shown later than the bus came by more than 1% of the lead. Bins with fewer than 30 samples are shown in parentheses and never decide a verdict.

### prediction_miss:first_stop_next_trip_times:4346 (high, open)

53rd Street Express; scope: stops=8811|8628;lead=0-10;note=stop positions 1 2, 330 of 330 times the bus came later than shown (not applied: note=stop positions 1 2, 330 of 330 times the bus came later than shown); 115 samples. Flag: share of the times a screen showed only under another trip id of the same bus 5 min ahead (no own-trip time) that were large misses (more than 2 min either way), last 14 service days 1.0000 (all lines 0.5822).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | 53rd Street Express | 115 | 5.4% / 10.4% (115) |  |  |  |  | reference |
| timetable_delay | 53rd Street Express | 115 | 6.1% / 81.7% (115) |  |  |  |  | loses: too late 81.7% vs Passio 10.4% at 0-10 min |
| gbm_q15 | 53rd Street Express | 115 | 40.0% / 11.3% (115) |  |  |  |  | holds |
| deep_q15 | 53rd Street Express | 115 | 16.5% / 11.3% (115) |  |  |  |  | holds |
| deep_safe | 53rd Street Express | 115 | 13.9% / 7.0% (115) |  |  |  |  | holds |

### prediction_miss:large_early_miss:4346 (high, open)

53rd Street Express; scope: lead=5-20;stops=8589|8631|8632|161844|8612;note=last 14 days 21.7%, before them 1.4% (worse) (not applied: note=last 14 days 21.7%, before them 1.4% (worse)); 2,143 samples. Flag: share of Passio's times 5 to 30 min ahead that the bus beat by more than the large-miss threshold (2 min at 5 to 15 min ahead, 4 at 20, 5 at 30), last 14 service days 0.2166 (all lines 0.1098).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | 53rd Street Express | 2,143 | 0.2% / 98.9% (447) | 2.8% / 76.6% (868) | 5.9% / 8.6% (828) |  |  | reference |
| timetable_delay | 53rd Street Express | 2,143 | 45.9% / 9.2% (447) | 11.6% / 25.5% (868) | 7.3% / 75.4% (828) |  |  | loses: too late 75.4% vs Passio 8.6% at 15-20 min |
| gbm_q15 | 53rd Street Express | 2,143 | 17.0% / 51.5% (447) | 19.0% / 40.8% (868) | 11.8% / 12.0% (828) |  |  | loses: too late 12.0% vs Passio 8.6% at 15-20 min |
| deep_q15 | 53rd Street Express | 2,143 | 34.0% / 7.2% (447) | 20.2% / 14.2% (868) | 17.7% / 15.6% (828) |  |  | loses: too late 15.6% vs Passio 8.6% at 15-20 min |
| deep_safe | 53rd Street Express | 2,143 | 35.6% / 7.4% (447) | 17.8% / 14.2% (868) | 16.8% / 15.8% (828) |  |  | loses: too late 15.8% vs Passio 8.6% at 15-20 min |

### transition:service_end_early:4346 (high, open)

53rd Street Express; scope: hours=18-19;days=weekday;note=before Nov 6 89.474, from Nov 6 66.667 (2 episodes) (not applied: note=before Nov 6 89.474, from Nov 6 66.667 (2 episodes)); 43 samples. Flag: service days whose last bus left more than 15 min before the line's listed end, per 100 spans 86.364 (all lines 27.793).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | 53rd Street Express | 43 | (4.3% / 8.3% (24)) | (0.0% / 7.7% (13)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | reference |
| timetable_delay | 53rd Street Express | 43 | (4.3% / 87.5% (24)) | (0.0% / 92.3% (13)) | (0.0% / 75.0% (4)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | too few rows |
| gbm_q15 | 53rd Street Express | 43 | (8.7% / 16.7% (24)) | (8.3% / 7.7% (13)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | too few rows |
| deep_q15 | 53rd Street Express | 43 | (26.1% / 0.0% (24)) | (16.7% / 0.0% (13)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | too few rows |
| deep_safe | 53rd Street Express | 43 | (17.4% / 0.0% (24)) | (16.7% / 0.0% (13)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | too few rows |

### prediction_miss:stops_without_predictions:4346 (high, open)

53rd Street Express; scope: stops=8811|8628|138837;lead=0-10;note=a time at any lead 1 to 30 min ahead 47%, before the last 14 days 87% of 843 arrivals had one 5 min ahead (not applied: note=a time at any lead 1 to 30 min ahead 47%, before the last 14 days 87% of 843 arrivals had one 5 min ahead); 276 samples. Flag: share of arrivals at the scope's stops with a Passio time on display 5 min ahead, last 14 service days 0.0833 (all lines 0.6594).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | 53rd Street Express | 276 | 9.3% / 15.2% (276) |  |  |  |  | reference |
| timetable_delay | 53rd Street Express | 276 | 16.2% / 63.4% (276) |  |  |  |  | loses: too late 63.4% vs Passio 15.2% at 0-10 min |
| gbm_q15 | 53rd Street Express | 276 | 30.1% / 22.5% (276) |  |  |  |  | loses: too late 22.5% vs Passio 15.2% at 0-10 min |
| deep_q15 | 53rd Street Express | 276 | 27.5% / 21.4% (276) |  |  |  |  | loses: too late 21.4% vs Passio 15.2% at 0-10 min |
| deep_safe | 53rd Street Express | 276 | 26.4% / 12.0% (276) |  |  |  |  | holds |

### transition:feed_drop_mid_route:5702 (high, open)

Apostolic; scope: vehicles=4322;hours=6-9;days=weekday;stops=8623;note=before Nov 6 2.789, from Nov 6 0.647 (1 episodes), top spot South Campus Resident Hall (54 of 64) (not applied: note=before Nov 6 2.789, from Nov 6 0.647 (1 episodes), top spot South Campus Resident Hall (54 of 64)); 0 samples. Flag: buses vanishing from the feed while moving on the line (5 min or more), per 10 bus-hours inside transition windows (30 min around a bus count change, a shift change, a listed start or end, a timetable step) 2.512 (all lines 0.958).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Apostolic | 0 |  |  |  |  |  | no rows |
| timetable_delay | Apostolic | 0 |  |  |  |  |  | no rows |
| gbm_q15 | Apostolic | 0 |  |  |  |  |  | no rows |
| deep_q15 | Apostolic | 0 |  |  |  |  |  | no rows |
| deep_safe | Apostolic | 0 |  |  |  |  |  | no rows |

### transition:position_jump:5702 (high, open)

Apostolic; scope: vehicles=4322;hours=5-9;days=weekday;note=before Nov 6 4.135, from Nov 6 1.295 (4 episodes), top spot Woodlawn Ave & 61st St (34 of 98) (not applied: note=before Nov 6 4.135, from Nov 6 1.295 (4 episodes), top spot Woodlawn Ave & 61st St (34 of 98)); 373 samples. Flag: position jumps (500 m or more in one report, faster than 35 m/s), per 10 bus-hours inside transition windows (30 min around a bus count change, a shift change, a listed start or end, a timetable step) 3.768 (all lines 1.242).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Apostolic | 373 | 21.8% / 9.5% (95) | 0.0% / 19.2% (78) | 0.0% / 18.5% (81) | 9.7% / 8.7% (92) | (14.3% / 0.0% (27)) | reference |
| timetable_delay | Apostolic | 373 | 13.4% / 58.9% (95) | 22.4% / 44.9% (78) | 24.3% / 43.2% (81) | 36.4% / 43.5% (92) | (22.7% / 0.0% (27)) | loses: band B 13.4% vs Passio 21.8% at 0-10 min; too late 58.9% vs Passio 9.5% at 0-10 min; too late 44.9% vs Passio 19.2% at 10-15 min; too late 43.2% vs Passio 18.5% at 15-20 min; too late 43.5% vs Passio 8.7% at 20-30 min |
| gbm_q15 | Apostolic | 373 | 40.4% / 14.7% (95) | 0.0% / 20.5% (78) | 0.0% / 18.5% (81) | 16.9% / 8.7% (92) | (0.0% / 0.0% (27)) | loses: too late 14.7% vs Passio 9.5% at 0-10 min; too late 20.5% vs Passio 19.2% at 10-15 min |
| deep_q15 | Apostolic | 373 | 32.3% / 12.6% (95) | 0.0% / 20.5% (78) | 0.0% / 18.5% (81) | 17.9% / 8.7% (92) | (42.9% / 0.0% (27)) | loses: too late 12.6% vs Passio 9.5% at 0-10 min; too late 20.5% vs Passio 19.2% at 10-15 min |
| deep_safe | Apostolic | 373 | 33.9% / 12.6% (95) | 0.0% / 20.5% (78) | 0.0% / 18.5% (81) | 30.4% / 9.8% (92) | (57.1% / 0.0% (27)) | loses: too late 12.6% vs Passio 9.5% at 0-10 min; too late 20.5% vs Passio 19.2% at 10-15 min; too late 9.8% vs Passio 8.7% at 20-30 min |

### prediction_miss:stops_without_predictions:5702 (high, open)

Apostolic; scope: stops=8613;lead=0-10;note=a time at any lead 1 to 30 min ahead 9%, before the last 14 days 81% of 293 arrivals had one 5 min ahead (not applied: note=a time at any lead 1 to 30 min ahead 9%, before the last 14 days 81% of 293 arrivals had one 5 min ahead); 12 samples. Flag: share of arrivals at the scope's stops with a Passio time on display 5 min ahead, last 14 service days 0.0442 (all lines 0.6594).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Apostolic | 12 | (50.0% / 8.3% (12)) |  |  |  |  | reference |
| timetable_delay | Apostolic | 12 | (8.3% / 91.7% (12)) |  |  |  |  | too few rows |
| gbm_q15 | Apostolic | 12 | (50.0% / 8.3% (12)) |  |  |  |  | too few rows |
| deep_q15 | Apostolic | 12 | (58.3% / 16.7% (12)) |  |  |  |  | too few rows |
| deep_safe | Apostolic | 12 | (41.7% / 16.7% (12)) |  |  |  |  | too few rows |

### prediction_miss:other_trip_times:6126 (high, open)

Apostolic/Drexel; scope: stops=8609;lead=0-10;note=stop positions 5, 75 of 109 times the bus came later than shown (not applied: note=stop positions 5, 75 of 109 times the bus came later than shown); 339 samples. Flag: share of the times a screen showed only under another trip id of the same bus 5 min ahead (no own-trip time) that were large misses (more than 2 min either way), last 14 service days 0.7431 (all lines 0.5822).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Apostolic/Drexel | 339 | 12.3% / 31.6% (339) |  |  |  |  | reference |
| timetable_delay | Apostolic/Drexel | 339 | 8.6% / 28.6% (339) |  |  |  |  | loses: band B 8.6% vs Passio 12.3% at 0-10 min |
| gbm_q15 | Apostolic/Drexel | 339 | 32.4% / 38.6% (339) |  |  |  |  | loses: too late 38.6% vs Passio 31.6% at 0-10 min |
| deep_q15 | Apostolic/Drexel | 339 | 29.6% / 41.0% (339) |  |  |  |  | loses: too late 41.0% vs Passio 31.6% at 0-10 min |
| deep_safe | Apostolic/Drexel | 339 | 34.4% / 32.4% (339) |  |  |  |  | holds |

### transition:service_end_early:6126 (high, open)

Apostolic/Drexel; scope: hours=0-1;days=weekday;note=before Nov 6 94.737, from Nov 6 100.0 (3 episodes) (not applied: note=before Nov 6 94.737, from Nov 6 100.0 (3 episodes)); 0 samples. Flag: service days whose last bus left more than 15 min before the line's listed end, per 100 spans 95.455 (all lines 27.793).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Apostolic/Drexel | 0 |  |  |  |  |  | no rows |
| timetable_delay | Apostolic/Drexel | 0 |  |  |  |  |  | no rows |
| gbm_q15 | Apostolic/Drexel | 0 |  |  |  |  |  | no rows |
| deep_q15 | Apostolic/Drexel | 0 |  |  |  |  |  | no rows |
| deep_safe | Apostolic/Drexel | 0 |  |  |  |  |  | no rows |

### prediction_miss:stops_without_predictions:6126 (high, open)

Apostolic/Drexel; scope: stops=225834;lead=0-10;note=a time at any lead 1 to 30 min ahead 3%, before the last 14 days 68% of 97 arrivals had one 5 min ahead (not applied: note=a time at any lead 1 to 30 min ahead 3%, before the last 14 days 68% of 97 arrivals had one 5 min ahead); 12 samples. Flag: share of arrivals at the scope's stops with a Passio time on display 5 min ahead, last 14 service days 0.0021 (all lines 0.6594).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Apostolic/Drexel | 12 | (25.0% / 8.3% (12)) |  |  |  |  | reference |
| timetable_delay | Apostolic/Drexel | 12 | (0.0% / 100.0% (12)) |  |  |  |  | too few rows |
| gbm_q15 | Apostolic/Drexel | 12 | (41.7% / 33.3% (12)) |  |  |  |  | too few rows |
| deep_q15 | Apostolic/Drexel | 12 | (16.7% / 25.0% (12)) |  |  |  |  | too few rows |
| deep_safe | Apostolic/Drexel | 12 | (25.0% / 16.7% (12)) |  |  |  |  | too few rows |

### transition:after_hours:1078 (high, open)

Central; scope: hours=23-24;note=before Nov 6 3.596, from Nov 6 4.449 (4 episodes), top spot Operator garage (20 of 44) (not applied: note=before Nov 6 3.596, from Nov 6 4.449 (4 episodes), top spot Operator garage (20 of 44)); 157 samples. Flag: bus reporting under the line's label more than 15 min after (30 min before) its listed hours, per 10 bus-hours inside transition windows (30 min around a bus count change, a shift change, a listed start or end, a timetable step) 3.688 (all lines 0.491).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Central | 157 | 0.0% / 85.5% (69) | 10.0% / 67.4% (46) | (7.1% / 56.5% (23)) | (10.0% / 38.9% (18)) | (0.0% / 100.0% (1)) | reference |
| timetable_delay | Central | 157 | 8.3% / 4.3% (69) | 0.0% / 6.5% (46) | (11.1% / 8.7% (23)) | (0.0% / 11.1% (18)) | (0.0% / 0.0% (1)) | loses: band B 0.0% vs Passio 10.0% at 10-15 min |
| gbm_q15 | Central | 157 | 13.3% / 49.3% (69) | 0.0% / 52.2% (46) | (23.1% / 26.1% (23)) | (20.0% / 5.6% (18)) | (0.0% / 100.0% (1)) | loses: band B 0.0% vs Passio 10.0% at 10-15 min |
| deep_q15 | Central | 157 | 27.3% / 37.7% (69) | 34.1% / 32.6% (46) | (23.8% / 13.0% (23)) | (20.0% / 0.0% (18)) | (0.0% / 100.0% (1)) | holds |
| deep_safe | Central | 157 | 28.8% / 39.1% (69) | 26.8% / 43.5% (46) | (26.3% / 21.7% (23)) | (9.1% / 5.6% (18)) | (0.0% / 100.0% (1)) | holds |

### prediction_miss:large_early_miss:1078 (high, open)

Central; scope: lead=5-20;stops=140016|141862|140009|140012;hours=22-05;note=last 14 days 24.1%, before them 4.5% (worse) (not applied: note=last 14 days 24.1%, before them 4.5% (worse)); 81 samples. Flag: share of Passio's times 5 to 30 min ahead that the bus beat by more than the large-miss threshold (2 min at 5 to 15 min ahead, 4 at 20, 5 at 30), last 14 service days 0.2407 (all lines 0.1098).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Central | 81 | 0.0% / 100.0% (39) | (0.0% / 91.3% (23)) | (31.2% / 26.3% (19)) |  |  | reference |
| timetable_delay | Central | 81 | 0.0% / 0.0% (39) | (0.0% / 21.7% (23)) | (11.8% / 73.7% (19)) |  |  | holds |
| gbm_q15 | Central | 81 | 25.7% / 48.7% (39) | (10.5% / 56.5% (23)) | (31.6% / 21.1% (19)) |  |  | holds |
| deep_q15 | Central | 81 | 20.5% / 35.9% (39) | (31.8% / 21.7% (23)) | (47.4% / 21.1% (19)) |  |  | holds |
| deep_safe | Central | 81 | 30.8% / 30.8% (39) | (39.1% / 34.8% (23)) | (52.6% / 21.1% (19)) |  |  | holds |

### prediction_miss:other_trip_times:1078 (high, open)

Central; scope: stops=8634|8635|140009;lead=0-10;note=stop positions 7 8 9, 212 of 213 times the bus came earlier than shown (not applied: note=stop positions 7 8 9, 212 of 213 times the bus came earlier than shown); 435 samples. Flag: share of the times a screen showed only under another trip id of the same bus 5 min ahead (no own-trip time) that were large misses (more than 2 min either way), last 14 service days 0.9953 (all lines 0.5822).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Central | 435 | 1.9% / 97.2% (435) |  |  |  |  | reference |
| timetable_delay | Central | 435 | 5.3% / 7.8% (435) |  |  |  |  | holds |
| gbm_q15 | Central | 435 | 13.6% / 85.3% (435) |  |  |  |  | holds |
| deep_q15 | Central | 435 | 35.7% / 26.4% (435) |  |  |  |  | holds |
| deep_safe | Central | 435 | 33.4% / 26.4% (435) |  |  |  |  | holds |

### display:planner_recommends_leaving_bus:5704 (high, open)

Downtown Campus Connector; scope: note=after the rules shipped (2026-11-06 to 2026-11-10): 14.7 vs all lines 5.7, 349 events (not applied: note=after the rules shipped (2026-11-06 to 2026-11-10): 14.7 vs all lines 5.7, 349 events); 9,308 samples. Flag: percent of the planner's live bus legs (sampled stop pairs every 5 min, core/planner.js plan()) whose bus never boarded on the line or logged no arrival near the rider's stop (left the line first) 17.8 (all lines 7.1).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Downtown Campus Connector | 9,308 | 4.8% / 37.5% (1,661) | 9.8% / 27.2% (1,858) | 11.9% / 20.4% (1,940) | 14.5% / 5.6% (1,942) | 5.7% / 2.0% (1,907) | reference |
| timetable_delay | Downtown Campus Connector | 9,308 | 4.8% / 37.5% (1,661) | 9.8% / 27.2% (1,858) | 11.9% / 20.4% (1,940) | 14.5% / 5.6% (1,942) | 5.7% / 2.0% (1,907) | holds |
| gbm_q15 | Downtown Campus Connector | 9,308 | 17.5% / 26.6% (1,661) | 16.3% / 22.9% (1,858) | 14.5% / 13.6% (1,940) | 13.7% / 4.9% (1,942) | 6.1% / 2.4% (1,907) | holds |
| deep_q15 | Downtown Campus Connector | 9,308 | 19.8% / 19.4% (1,661) | 17.7% / 15.6% (1,858) | 14.0% / 12.7% (1,940) | 18.3% / 6.7% (1,942) | 9.1% / 1.3% (1,907) | loses: too late 6.7% vs Passio 5.6% at 20-30 min |
| deep_safe | Downtown Campus Connector | 9,308 | 17.6% / 17.2% (1,661) | 18.3% / 15.3% (1,858) | 13.7% / 13.5% (1,940) | 17.2% / 8.3% (1,942) | 10.4% / 2.9% (1,907) | loses: too late 8.3% vs Passio 5.6% at 20-30 min |

### transition:service_end_early:5704 (high, open)

Downtown Campus Connector; scope: hours=22-23;days=weekday;note=before Nov 6 100.0, from Nov 6 100.0 (3 episodes) (not applied: note=before Nov 6 100.0, from Nov 6 100.0 (3 episodes)); 3 samples. Flag: service days whose last bus left more than 15 min before the line's listed end, per 100 spans 100 (all lines 27.793).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Downtown Campus Connector | 3 | (0.0% / 100.0% (3)) |  |  |  |  | reference |
| timetable_delay | Downtown Campus Connector | 3 | (0.0% / 100.0% (3)) |  |  |  |  | too few rows |
| gbm_q15 | Downtown Campus Connector | 3 | (0.0% / 33.3% (3)) |  |  |  |  | too few rows |
| deep_q15 | Downtown Campus Connector | 3 | (33.3% / 0.0% (3)) |  |  |  |  | too few rows |
| deep_safe | Downtown Campus Connector | 3 | (0.0% / 0.0% (3)) |  |  |  |  | too few rows |

### transition:sparse_reporting:5704 (high, open)

Downtown Campus Connector; scope: vehicles=12647;days=weekday;note=before Nov 6 0.398, from Nov 6 0.596 (11 episodes), top spot E Randolph St & S Michigan Ave (3 of 58) (not applied: note=before Nov 6 0.398, from Nov 6 0.596 (11 episodes), top spot E Randolph St & S Michigan Ave (3 of 58)); 1,127 samples. Flag: bus reporting only every few minutes (gaps of 5 min or more), per 10 bus-hours inside transition windows (30 min around a bus count change, a shift change, a listed start or end, a timetable step) 0.426 (all lines 0.201).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Downtown Campus Connector | 1,127 | 7.0% / 36.8% (190) | 11.8% / 22.5% (218) | 12.0% / 15.1% (239) | 8.6% / 4.1% (241) | 7.9% / 1.7% (239) | reference |
| timetable_delay | Downtown Campus Connector | 1,127 | 7.0% / 36.8% (190) | 11.8% / 22.5% (218) | 12.0% / 15.1% (239) | 8.6% / 4.1% (241) | 7.9% / 1.7% (239) | holds |
| gbm_q15 | Downtown Campus Connector | 1,127 | 20.2% / 25.8% (190) | 16.3% / 22.0% (218) | 18.5% / 9.6% (239) | 8.7% / 5.0% (241) | 6.7% / 1.7% (239) | loses: band B 6.7% vs Passio 7.9% at 30-45 min |
| deep_q15 | Downtown Campus Connector | 1,127 | 19.8% / 18.4% (190) | 18.8% / 13.8% (218) | 12.2% / 6.7% (239) | 15.7% / 5.0% (241) | 4.5% / 1.7% (239) | loses: band B 4.5% vs Passio 7.9% at 30-45 min |
| deep_safe | Downtown Campus Connector | 1,127 | 16.0% / 16.3% (190) | 22.8% / 12.8% (218) | 16.9% / 7.1% (239) | 13.6% / 5.8% (241) | 10.2% / 1.7% (239) | loses: too late 5.8% vs Passio 4.1% at 20-30 min |

### prediction_miss:stops_without_predictions:5704 (high, open)

Downtown Campus Connector; scope: stops=140009|151794|155005|132965|155006|132963|132964;lead=0-10;note=a time at any lead 1 to 30 min ahead 37%, before the last 14 days 89% of 2722 arrivals had one 5 min ahead (not applied: note=a time at any lead 1 to 30 min ahead 37%, before the last 14 days 89% of 2722 arrivals had one 5 min ahead); 211 samples. Flag: share of arrivals at the scope's stops with a Passio time on display 5 min ahead, last 14 service days 0.0226 (all lines 0.6594).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Downtown Campus Connector | 211 | 0.0% / 4.3% (211) |  |  |  |  | reference |
| timetable_delay | Downtown Campus Connector | 211 | 0.0% / 4.3% (211) |  |  |  |  | holds |
| gbm_q15 | Downtown Campus Connector | 211 | 1.5% / 2.4% (211) |  |  |  |  | holds |
| deep_q15 | Downtown Campus Connector | 211 | 2.6% / 3.3% (211) |  |  |  |  | holds |
| deep_safe | Downtown Campus Connector | 211 | 1.9% / 3.8% (211) |  |  |  |  | holds |

### prediction_miss:worse_when_behind:5701 (high, open)

Drexel; scope: lead=5-30;note=delay_s > 600 in the forecast table (not applied: note=delay_s > 600 in the forecast table); 1,618 samples. Flag: large-miss rate (goal leads) while the bus ran more than 10 min behind the timetable divided by the rate otherwise on the same line, all days 1.7904 (all lines 1.2148).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Drexel | 1,618 | 14.9% / 2.1% (335) | 14.3% / 2.6% (502) | 13.1% / 2.0% (551) | 21.5% / 0.0% (230) |  | reference |
| timetable_delay | Drexel | 1,618 | 6.8% / 63.3% (335) | 22.8% / 33.3% (502) | 35.7% / 36.8% (551) | 52.2% / 18.7% (230) |  | loses: band B 6.8% vs Passio 14.9% at 0-10 min; too late 63.3% vs Passio 2.1% at 0-10 min; too late 33.3% vs Passio 2.6% at 10-15 min; too late 36.8% vs Passio 2.0% at 15-20 min; too late 18.7% vs Passio 0.0% at 20-30 min |
| gbm_q15 | Drexel | 1,618 | 24.7% / 6.3% (335) | 12.1% / 2.8% (502) | 5.6% / 1.5% (551) | 15.6% / 0.0% (230) |  | loses: too late 6.3% vs Passio 2.1% at 0-10 min; band B 12.1% vs Passio 14.3% at 10-15 min; band B 5.6% vs Passio 13.1% at 15-20 min; band B 15.6% vs Passio 21.5% at 20-30 min |
| deep_q15 | Drexel | 1,618 | 23.2% / 6.0% (335) | 14.9% / 4.6% (502) | 19.5% / 4.0% (551) | 38.3% / 1.3% (230) |  | loses: too late 6.0% vs Passio 2.1% at 0-10 min; too late 4.6% vs Passio 2.6% at 10-15 min; too late 4.0% vs Passio 2.0% at 15-20 min; too late 1.3% vs Passio 0.0% at 20-30 min |
| deep_safe | Drexel | 1,618 | 19.7% / 5.1% (335) | 14.2% / 4.8% (502) | 17.0% / 3.4% (551) | 37.9% / 0.9% (230) |  | loses: too late 5.1% vs Passio 2.1% at 0-10 min; too late 4.8% vs Passio 2.6% at 10-15 min; too late 3.4% vs Passio 2.0% at 15-20 min |

### prediction_miss:large_early_miss:1077 (high, open)

East; scope: lead=5-15;stops=140013|8578|140014|140015;hours=22-05;note=last 14 days 17.9%, before them 2.9% (worse) (not applied: note=last 14 days 17.9%, before them 2.9% (worse)); 188 samples. Flag: share of Passio's times 5 to 30 min ahead that the bus beat by more than the large-miss threshold (2 min at 5 to 15 min ahead, 4 at 20, 5 at 30), last 14 service days 0.1788 (all lines 0.1098).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | East | 188 | 1.4% / 90.5% (74) | 25.8% / 34.2% (114) |  |  |  | reference |
| timetable_delay | East | 188 | 2.7% / 47.3% (74) | 6.1% / 70.2% (114) |  |  |  | loses: band B 6.1% vs Passio 25.8% at 10-15 min; too late 70.2% vs Passio 34.2% at 10-15 min |
| gbm_q15 | East | 188 | 28.4% / 31.1% (74) | 19.0% / 24.6% (114) |  |  |  | loses: band B 19.0% vs Passio 25.8% at 10-15 min |
| deep_q15 | East | 188 | 29.7% / 10.8% (74) | 23.9% / 20.2% (114) |  |  |  | holds |
| deep_safe | East | 188 | 25.7% / 8.1% (74) | 12.4% / 20.2% (114) |  |  |  | loses: band B 12.4% vs Passio 25.8% at 10-15 min |

### prediction_miss:stops_without_predictions:1077 (high, open)

East; scope: stops=8633|8634|8635;lead=0-10;note=a time at any lead 1 to 30 min ahead 8%, before the last 14 days 76% of 698 arrivals had one 5 min ahead (not applied: note=a time at any lead 1 to 30 min ahead 8%, before the last 14 days 76% of 698 arrivals had one 5 min ahead); 43 samples. Flag: share of arrivals at the scope's stops with a Passio time on display 5 min ahead, last 14 service days 0.0607 (all lines 0.6594).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | East | 43 | 0.0% / 14.0% (43) |  |  |  |  | reference |
| timetable_delay | East | 43 | 0.0% / 20.9% (43) |  |  |  |  | loses: too late 20.9% vs Passio 14.0% at 0-10 min |
| gbm_q15 | East | 43 | 5.1% / 7.0% (43) |  |  |  |  | holds |
| deep_q15 | East | 43 | 7.9% / 7.0% (43) |  |  |  |  | holds |
| deep_safe | East | 43 | 4.9% / 7.0% (43) |  |  |  |  | holds |

### display:false_hide_offroute_serving_bus:5700 (high, open)

Friend Center/Metra; scope: hours=18-21;vehicles=4325|4313;stops=8612;note=after the rules shipped (2026-11-06 to 2026-11-10): 68.2 vs all lines 24.4, 88 events (not applied: note=after the rules shipped (2026-11-06 to 2026-11-10): 68.2 vs all lines 24.4, 88 events); 11 samples. Flag: percent of minutes core/offroute.js hid a bus (and its times) that then logged an arrival on the line within 15 min 53.1 (all lines 19.6).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Friend Center/Metra | 11 | (0.0% / 100.0% (2)) | (0.0% / 100.0% (2)) | (0.0% / 0.0% (3)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) | reference |
| timetable_delay | Friend Center/Metra | 11 | (0.0% / 50.0% (2)) | (0.0% / 50.0% (2)) | (0.0% / 33.3% (3)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) | too few rows |
| gbm_q15 | Friend Center/Metra | 11 | (0.0% / 100.0% (2)) | (0.0% / 50.0% (2)) | (0.0% / 0.0% (3)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) | too few rows |
| deep_q15 | Friend Center/Metra | 11 | (0.0% / 100.0% (2)) | (0.0% / 100.0% (2)) | (0.0% / 0.0% (3)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) | too few rows |
| deep_safe | Friend Center/Metra | 11 | (0.0% / 100.0% (2)) | (0.0% / 50.0% (2)) | (0.0% / 0.0% (3)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) | too few rows |

### transition:after_hours:5703 (high, open)

Midway Metra; scope: hours=19-20;days=weekday;note=before Nov 6 1.039, from Nov 6 1.058 (5 episodes), top spot Operator garage (6 of 32) (not applied: note=before Nov 6 1.039, from Nov 6 1.058 (5 episodes), top spot Operator garage (6 of 32)); 4 samples. Flag: bus reporting under the line's label more than 15 min after (30 min before) its listed hours, per 10 bus-hours inside transition windows (30 min around a bus count change, a shift change, a listed start or end, a timetable step) 1.041 (all lines 0.491).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Midway Metra | 4 | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) |  | reference |
| timetable_delay | Midway Metra | 4 | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) |  | too few rows |
| gbm_q15 | Midway Metra | 4 | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) |  | too few rows |
| deep_q15 | Midway Metra | 4 | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) |  | too few rows |
| deep_safe | Midway Metra | 4 | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) |  | too few rows |

### prediction_miss:large_late_miss:5699 (high, open)

Red Line/Arts Block; scope: lead=5-45;note=last 14 days 79.6%, before them 79.5% (same) (not applied: note=last 14 days 79.6%, before them 79.5% (same)); 6,867 samples. Flag: share of Passio's times 5 to 30 min ahead that the bus came later than by more than the large-miss threshold (2 min at 5 to 15 min ahead, 4 at 20, 5 at 30), last 14 service days 0.7956 (all lines 0.5529).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Red Line/Arts Block | 6,867 | 8.8% / 8.2% (1,258) | 2.3% / 8.7% (2,180) | 3.2% / 8.8% (1,909) | 7.1% / 6.1% (1,398) | 2.3% / 0.0% (122) | reference |
| timetable_delay | Red Line/Arts Block | 6,867 | 9.9% / 21.0% (1,258) | 10.8% / 24.2% (2,180) | 12.1% / 11.3% (1,909) | 7.0% / 3.9% (1,398) | 1.5% / 1.6% (122) | loses: too late 21.0% vs Passio 8.2% at 0-10 min; too late 24.2% vs Passio 8.7% at 10-15 min; too late 11.3% vs Passio 8.8% at 15-20 min; band B 1.5% vs Passio 2.3% at 30-45 min; too late 1.6% vs Passio 0.0% at 30-45 min |
| gbm_q15 | Red Line/Arts Block | 6,867 | 27.5% / 16.5% (1,258) | 6.2% / 7.4% (2,180) | 3.8% / 6.1% (1,909) | 4.8% / 1.9% (1,398) | 0.0% / 0.0% (122) | loses: too late 16.5% vs Passio 8.2% at 0-10 min; band B 4.8% vs Passio 7.1% at 20-30 min; band B 0.0% vs Passio 2.3% at 30-45 min |
| deep_q15 | Red Line/Arts Block | 6,867 | 29.6% / 13.3% (1,258) | 13.2% / 7.0% (2,180) | 8.1% / 4.9% (1,909) | 7.6% / 1.3% (1,398) | 0.0% / 0.0% (122) | loses: too late 13.3% vs Passio 8.2% at 0-10 min; band B 0.0% vs Passio 2.3% at 30-45 min |
| deep_safe | Red Line/Arts Block | 6,867 | 26.3% / 9.9% (1,258) | 10.1% / 5.6% (2,180) | 6.9% / 5.4% (1,909) | 7.7% / 1.6% (1,398) | 0.0% / 0.0% (122) | loses: too late 9.9% vs Passio 8.2% at 0-10 min; band B 0.0% vs Passio 2.3% at 30-45 min |

### prediction_miss:stops_without_predictions:5699 (high, open)

Red Line/Arts Block; scope: stops=138836;lead=0-10;note=a time at any lead 1 to 30 min ahead 6%, before the last 14 days 92% of 461 arrivals had one 5 min ahead (not applied: note=a time at any lead 1 to 30 min ahead 6%, before the last 14 days 92% of 461 arrivals had one 5 min ahead); 12 samples. Flag: share of arrivals at the scope's stops with a Passio time on display 5 min ahead, last 14 service days 0.0198 (all lines 0.6594).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Red Line/Arts Block | 12 | (25.0% / 8.3% (12)) |  |  |  |  | reference |
| timetable_delay | Red Line/Arts Block | 12 | (25.0% / 33.3% (12)) |  |  |  |  | too few rows |
| gbm_q15 | Red Line/Arts Block | 12 | (58.3% / 33.3% (12)) |  |  |  |  | too few rows |
| deep_q15 | Red Line/Arts Block | 12 | (58.3% / 33.3% (12)) |  |  |  |  | too few rows |
| deep_safe | Red Line/Arts Block | 12 | (25.0% / 50.0% (12)) |  |  |  |  | too few rows |

### prediction_miss:large_late_miss:5715 (high, open)

Regents Express; scope: lead=5-30;note=last 14 days 70.5%, before them 57.7% (worse) (not applied: note=last 14 days 70.5%, before them 57.7% (worse)); 575 samples. Flag: share of Passio's times 5 to 30 min ahead that the bus came later than by more than the large-miss threshold (2 min at 5 to 15 min ahead, 4 at 20, 5 at 30), last 14 service days 0.7048 (all lines 0.5529).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Regents Express | 575 | 12.5% / 27.1% (107) | 14.7% / 7.1% (168) | 16.5% / 5.4% (167) | 16.4% / 2.3% (133) |  | reference |
| timetable_delay | Regents Express | 575 | 11.1% / 8.4% (107) | 13.3% / 4.8% (168) | 1.5% / 1.8% (167) | 4.2% / 0.8% (133) |  | loses: band B 11.1% vs Passio 12.5% at 0-10 min; band B 1.5% vs Passio 16.5% at 15-20 min; band B 4.2% vs Passio 16.4% at 20-30 min |
| gbm_q15 | Regents Express | 575 | 11.8% / 28.0% (107) | 2.0% / 0.6% (168) | 3.5% / 1.2% (167) | 7.3% / 0.8% (133) |  | loses: band B 2.0% vs Passio 14.7% at 10-15 min; band B 3.5% vs Passio 16.5% at 15-20 min; band B 7.3% vs Passio 16.4% at 20-30 min |
| deep_q15 | Regents Express | 575 | 11.4% / 24.3% (107) | 5.6% / 1.2% (168) | 7.3% / 1.8% (167) | 8.1% / 0.8% (133) |  | loses: band B 5.6% vs Passio 14.7% at 10-15 min; band B 7.3% vs Passio 16.5% at 15-20 min; band B 8.1% vs Passio 16.4% at 20-30 min |
| deep_safe | Regents Express | 575 | 13.3% / 21.5% (107) | 6.8% / 1.8% (168) | 6.9% / 1.8% (167) | 8.8% / 1.5% (133) |  | loses: band B 6.8% vs Passio 14.7% at 10-15 min; band B 6.9% vs Passio 16.5% at 15-20 min; band B 8.8% vs Passio 16.4% at 20-30 min |

### display:false_hide_idle_serving_bus:1076 (high, open)

South; scope: hours=21-22|23-24;stops=8631|8633;note=after the rules shipped (2026-11-06 to 2026-11-10): 96.4 vs all lines 37.0, 27 events (not applied: note=after the rules shipped (2026-11-06 to 2026-11-10): 96.4 vs all lines 37.0, 27 events); 158 samples. Flag: percent of minutes core/idle.js hid a still bus that then logged an arrival on the line within 15 min 47.4 (all lines 23.6).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | South | 158 | 4.0% / 76.4% (55) | 11.8% / 49.0% (49) | (11.8% / 28.6% (28)) | (11.1% / 21.1% (19)) | (0.0% / 0.0% (7)) | reference |
| timetable_delay | South | 158 | 10.0% / 76.4% (55) | 4.7% / 79.6% (49) | (20.8% / 53.6% (28)) | (43.8% / 10.5% (19)) | (0.0% / 0.0% (7)) | loses: band B 4.7% vs Passio 11.8% at 10-15 min; too late 79.6% vs Passio 49.0% at 10-15 min |
| gbm_q15 | South | 158 | 24.1% / 21.8% (55) | 2.6% / 26.5% (49) | (11.8% / 14.3% (28)) | (0.0% / 5.3% (19)) | (0.0% / 0.0% (7)) | loses: band B 2.6% vs Passio 11.8% at 10-15 min |
| deep_q15 | South | 158 | 41.8% / 16.4% (55) | 13.0% / 22.4% (49) | (8.7% / 14.3% (28)) | (10.0% / 5.3% (19)) | (0.0% / 0.0% (7)) | holds |
| deep_safe | South | 158 | 16.4% / 16.4% (55) | 11.6% / 22.4% (49) | (0.0% / 17.9% (28)) | (20.0% / 5.3% (19)) | (0.0% / 0.0% (7)) | holds |

### prediction_miss:large_early_miss:1076 (high, open)

South; scope: lead=5-15;stops=8652|8633|8630|8631;hours=22-05;note=last 14 days 9.9%, before them 13.6% (better) (not applied: note=last 14 days 9.9%, before them 13.6% (better)); 194 samples. Flag: share of Passio's times 5 to 30 min ahead that the bus beat by more than the large-miss threshold (2 min at 5 to 15 min ahead, 4 at 20, 5 at 30), all service days 0.1183 (all lines 0.0694).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | South | 194 | 7.1% / 80.0% (75) | 20.0% / 48.7% (119) |  |  |  | reference |
| timetable_delay | South | 194 | 8.1% / 84.0% (75) | 4.4% / 82.4% (119) |  |  |  | loses: too late 84.0% vs Passio 80.0% at 0-10 min; band B 4.4% vs Passio 20.0% at 10-15 min; too late 82.4% vs Passio 48.7% at 10-15 min |
| gbm_q15 | South | 194 | 24.7% / 28.0% (75) | 6.9% / 22.7% (119) |  |  |  | loses: band B 6.9% vs Passio 20.0% at 10-15 min |
| deep_q15 | South | 194 | 34.7% / 13.3% (75) | 11.5% / 23.5% (119) |  |  |  | loses: band B 11.5% vs Passio 20.0% at 10-15 min |
| deep_safe | South | 194 | 17.3% / 12.0% (75) | 10.9% / 21.0% (119) |  |  |  | loses: band B 10.9% vs Passio 20.0% at 10-15 min |

### transition:linger_not_in_service:1076 (high, open)

South; scope: hours=20-24;note=before Nov 6 8.163, from Nov 6 8.477 (9 episodes), top spot Burton-Judson Courts (38 of 80) (not applied: note=before Nov 6 8.163, from Nov 6 8.477 (9 episodes), top spot Burton-Judson Courts (38 of 80)); 2,407 samples. Flag: bus still for 5 min or more on the map but not in service (E28 break, end of shift, garage return, never served), per 10 bus-hours inside transition windows (30 min around a bus count change, a shift change, a listed start or end, a timetable step) 8.198 (all lines 2.528).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | South | 2,407 | 19.4% / 43.6% (854) | 19.7% / 20.9% (584) | 20.7% / 8.5% (473) | 35.5% / 7.9% (404) | 20.0% / 0.0% (92) | reference |
| timetable_delay | South | 2,407 | 6.1% / 66.2% (854) | 5.8% / 38.4% (584) | 8.6% / 22.0% (473) | 31.1% / 19.1% (404) | 19.0% / 21.7% (92) | loses: band B 6.1% vs Passio 19.4% at 0-10 min; too late 66.2% vs Passio 43.6% at 0-10 min; band B 5.8% vs Passio 19.7% at 10-15 min; too late 38.4% vs Passio 20.9% at 10-15 min; band B 8.6% vs Passio 20.7% at 15-20 min; too late 22.0% vs Passio 8.5% at 15-20 min; band B 31.1% vs Passio 35.5% at 20-30 min; too late 19.1% vs Passio 7.9% at 20-30 min; too late 21.7% vs Passio 0.0% at 30-45 min |
| gbm_q15 | South | 2,407 | 27.4% / 20.5% (854) | 8.6% / 8.9% (584) | 10.6% / 1.9% (473) | 24.1% / 3.2% (404) | 2.5% / 0.0% (92) | loses: band B 8.6% vs Passio 19.7% at 10-15 min; band B 10.6% vs Passio 20.7% at 15-20 min; band B 24.1% vs Passio 35.5% at 20-30 min; band B 2.5% vs Passio 20.0% at 30-45 min |
| deep_q15 | South | 2,407 | 28.7% / 21.4% (854) | 13.7% / 11.0% (584) | 12.9% / 6.6% (473) | 32.1% / 7.4% (404) | 2.6% / 0.0% (92) | loses: band B 13.7% vs Passio 19.7% at 10-15 min; band B 12.9% vs Passio 20.7% at 15-20 min; band B 2.6% vs Passio 20.0% at 30-45 min |
| deep_safe | South | 2,407 | 22.4% / 16.9% (854) | 13.0% / 9.9% (584) | 13.9% / 6.1% (473) | 31.9% / 8.2% (404) | 2.5% / 0.0% (92) | loses: band B 13.0% vs Passio 19.7% at 10-15 min; band B 13.9% vs Passio 20.7% at 15-20 min; band B 31.9% vs Passio 35.5% at 20-30 min; band B 2.5% vs Passio 20.0% at 30-45 min |

### prediction_miss:worse_when_behind:1076 (high, open)

South; scope: lead=5-30;note=delay_s > 600 in the forecast table (not applied: note=delay_s > 600 in the forecast table); 4,193 samples. Flag: large-miss rate (goal leads) while the bus ran more than 10 min behind the timetable divided by the rate otherwise on the same line, all days 1.5409 (all lines 1.2148).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | South | 4,193 | 17.4% / 35.0% (823) | 19.1% / 22.5% (1,304) | 21.1% / 8.6% (1,104) | 38.4% / 6.5% (962) |  | reference |
| timetable_delay | South | 4,193 | 6.1% / 64.0% (823) | 5.7% / 38.1% (1,304) | 8.8% / 21.3% (1,104) | 29.6% / 15.6% (962) |  | loses: band B 6.1% vs Passio 17.4% at 0-10 min; too late 64.0% vs Passio 35.0% at 0-10 min; band B 5.7% vs Passio 19.1% at 10-15 min; too late 38.1% vs Passio 22.5% at 10-15 min; band B 8.8% vs Passio 21.1% at 15-20 min; too late 21.3% vs Passio 8.6% at 15-20 min; band B 29.6% vs Passio 38.4% at 20-30 min; too late 15.6% vs Passio 6.5% at 20-30 min |
| gbm_q15 | South | 4,193 | 28.2% / 15.8% (823) | 12.1% / 10.1% (1,304) | 12.2% / 2.3% (1,104) | 31.4% / 2.0% (962) |  | loses: band B 12.1% vs Passio 19.1% at 10-15 min; band B 12.2% vs Passio 21.1% at 15-20 min; band B 31.4% vs Passio 38.4% at 20-30 min |
| deep_q15 | South | 4,193 | 32.1% / 15.6% (823) | 16.7% / 10.7% (1,304) | 15.1% / 5.8% (1,104) | 38.4% / 4.5% (962) |  | loses: band B 16.7% vs Passio 19.1% at 10-15 min; band B 15.1% vs Passio 21.1% at 15-20 min |
| deep_safe | South | 4,193 | 24.5% / 12.0% (823) | 16.2% / 9.7% (1,304) | 15.7% / 5.3% (1,104) | 39.5% / 5.8% (962) |  | loses: band B 16.2% vs Passio 19.1% at 10-15 min; band B 15.7% vs Passio 21.1% at 15-20 min |

### prediction_miss:large_early_miss:5716 (high, open)

South Loop Shuttle; scope: lead=5-45;stops=141882;note=last 14 days 41.8%, before them 21.2% (worse) (not applied: note=last 14 days 41.8%, before them 21.2% (worse)); 44 samples. Flag: share of Passio's times 5 to 30 min ahead that the bus beat by more than the large-miss threshold (2 min at 5 to 15 min ahead, 4 at 20, 5 at 30), all service days 0.2872 (all lines 0.0694).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | South Loop Shuttle | 44 | (0.0% / 100.0% (4)) | (50.0% / 93.3% (15)) | (0.0% / 93.8% (16)) | (0.0% / 85.7% (7)) | (0.0% / 50.0% (2)) | reference |
| timetable_delay | South Loop Shuttle | 44 | (0.0% / 100.0% (4)) | (0.0% / 100.0% (15)) | (0.0% / 93.8% (16)) | (0.0% / 57.1% (7)) | (0.0% / 50.0% (2)) | too few rows |
| gbm_q15 | South Loop Shuttle | 44 | (0.0% / 100.0% (4)) | (0.0% / 93.3% (15)) | (0.0% / 93.8% (16)) | (0.0% / 85.7% (7)) | (0.0% / 50.0% (2)) | too few rows |
| deep_q15 | South Loop Shuttle | 44 | (0.0% / 100.0% (4)) | (0.0% / 93.3% (15)) | (0.0% / 93.8% (16)) | (0.0% / 85.7% (7)) | (0.0% / 50.0% (2)) | too few rows |
| deep_safe | South Loop Shuttle | 44 | (0.0% / 100.0% (4)) | (0.0% / 100.0% (15)) | (0.0% / 93.8% (16)) | (0.0% / 85.7% (7)) | (0.0% / 50.0% (2)) | too few rows |

### transition:after_hours:5702 (medium, open)

Apostolic; scope: hours=10-11;days=weekday;note=before Nov 6 1.827, from Nov 6 4.531 (8 episodes), top spot Operator garage (4 of 29) (not applied: note=before Nov 6 1.827, from Nov 6 4.531 (8 episodes), top spot Operator garage (4 of 29)); 133 samples. Flag: bus reporting under the line's label more than 15 min after (30 min before) its listed hours, per 10 bus-hours inside transition windows (30 min around a bus count change, a shift change, a listed start or end, a timetable step) 2.177 (all lines 0.491).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Apostolic | 133 | 6.7% / 0.0% (45) | 0.0% / 0.0% (40) | 0.0% / 0.0% (37) | (0.0% / 0.0% (11)) |  | reference |
| timetable_delay | Apostolic | 133 | 2.3% / 22.2% (45) | 0.0% / 5.0% (40) | 24.0% / 13.5% (37) | (0.0% / 9.1% (11)) |  | loses: band B 2.3% vs Passio 6.7% at 0-10 min; too late 22.2% vs Passio 0.0% at 0-10 min; too late 5.0% vs Passio 0.0% at 10-15 min; too late 13.5% vs Passio 0.0% at 15-20 min |
| gbm_q15 | Apostolic | 133 | 15.0% / 2.2% (45) | 0.0% / 0.0% (40) | 0.0% / 0.0% (37) | (0.0% / 0.0% (11)) |  | loses: too late 2.2% vs Passio 0.0% at 0-10 min |
| deep_q15 | Apostolic | 133 | 12.5% / 2.2% (45) | 0.0% / 0.0% (40) | 0.0% / 0.0% (37) | (0.0% / 0.0% (11)) |  | loses: too late 2.2% vs Passio 0.0% at 0-10 min |
| deep_safe | Apostolic | 133 | 7.3% / 2.2% (45) | 0.0% / 0.0% (40) | 0.0% / 0.0% (37) | (0.0% / 0.0% (11)) |  | loses: too late 2.2% vs Passio 0.0% at 0-10 min |

### display:bus_number_churn:5702 (medium, open)

Apostolic; scope: hours=05-10;vehicles=4538;note=after the rules shipped (2026-11-06 to 2026-11-10): 17.1 vs all lines 14.7, 21 events (not applied: note=after the rules shipped (2026-11-06 to 2026-11-10): 17.1 vs all lines 14.7, 21 events); 1,689 samples. Flag: Bus 1 / Bus 2 swaps per 10 service hours (a bus shown in two polls in a row whose number changed) 34.33 (all lines 16.53).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Apostolic | 1,689 | 27.3% / 10.1% (445) | 12.4% / 5.5% (384) | 12.2% / 5.8% (379) | 25.4% / 2.8% (351) | 24.7% / 0.8% (130) | reference |
| timetable_delay | Apostolic | 1,689 | 5.1% / 70.3% (445) | 10.7% / 53.6% (384) | 11.7% / 49.1% (379) | 23.4% / 45.0% (351) | 16.8% / 42.3% (130) | loses: band B 5.1% vs Passio 27.3% at 0-10 min; too late 70.3% vs Passio 10.1% at 0-10 min; band B 10.7% vs Passio 12.4% at 10-15 min; too late 53.6% vs Passio 5.5% at 10-15 min; too late 49.1% vs Passio 5.8% at 15-20 min; too late 45.0% vs Passio 2.8% at 20-30 min; band B 16.8% vs Passio 24.7% at 30-45 min; too late 42.3% vs Passio 0.8% at 30-45 min |
| gbm_q15 | Apostolic | 1,689 | 30.5% / 22.2% (445) | 16.7% / 16.9% (384) | 15.7% / 9.5% (379) | 28.7% / 3.7% (351) | 17.1% / 0.8% (130) | loses: too late 22.2% vs Passio 10.1% at 0-10 min; too late 16.9% vs Passio 5.5% at 10-15 min; too late 9.5% vs Passio 5.8% at 15-20 min; band B 17.1% vs Passio 24.7% at 30-45 min |
| deep_q15 | Apostolic | 1,689 | 31.5% / 20.9% (445) | 16.1% / 18.8% (384) | 11.7% / 13.7% (379) | 27.5% / 5.7% (351) | 11.8% / 0.8% (130) | loses: too late 20.9% vs Passio 10.1% at 0-10 min; too late 18.8% vs Passio 5.5% at 10-15 min; too late 13.7% vs Passio 5.8% at 15-20 min; too late 5.7% vs Passio 2.8% at 20-30 min; band B 11.8% vs Passio 24.7% at 30-45 min |
| deep_safe | Apostolic | 1,689 | 27.7% / 17.5% (445) | 13.8% / 16.7% (384) | 12.9% / 12.4% (379) | 32.1% / 8.0% (351) | 16.9% / 2.3% (130) | loses: too late 17.5% vs Passio 10.1% at 0-10 min; too late 16.7% vs Passio 5.5% at 10-15 min; too late 12.4% vs Passio 5.8% at 15-20 min; too late 8.0% vs Passio 2.8% at 20-30 min; band B 16.9% vs Passio 24.7% at 30-45 min; too late 2.3% vs Passio 0.8% at 30-45 min |

### display:false_hide_gone_serving_bus:5702 (medium, open)

Apostolic; scope: hours=05-10;vehicles=4322;stops=8612;note=after the rules shipped (2026-11-06 to 2026-11-10): 100.0 vs all lines 9.9, 9 events (not applied: note=after the rules shipped (2026-11-06 to 2026-11-10): 100.0 vs all lines 9.9, 9 events); 68 samples. Flag: percent of minutes core/transition.js GONE dropped a bus's times (no report for 15 min) and the bus then logged an arrival on the line within 15 min 94.1 (all lines 16.3).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Apostolic | 68 | (25.0% / 11.1% (18)) | (0.0% / 12.5% (16)) | (7.7% / 12.5% (16)) | (41.7% / 13.3% (15)) | (0.0% / 0.0% (3)) | reference |
| timetable_delay | Apostolic | 68 | (18.8% / 61.1% (18)) | (21.4% / 56.2% (16)) | (21.4% / 56.2% (16)) | (26.7% / 53.3% (15)) | (0.0% / 0.0% (3)) | too few rows |
| gbm_q15 | Apostolic | 68 | (0.0% / 11.1% (18)) | (12.5% / 12.5% (16)) | (6.7% / 12.5% (16)) | (50.0% / 13.3% (15)) | (0.0% / 0.0% (3)) | too few rows |
| deep_q15 | Apostolic | 68 | (10.0% / 5.6% (18)) | (0.0% / 12.5% (16)) | (0.0% / 12.5% (16)) | (46.2% / 6.7% (15)) | (0.0% / 0.0% (3)) | too few rows |
| deep_safe | Apostolic | 68 | (14.3% / 5.6% (18)) | (0.0% / 12.5% (16)) | (0.0% / 12.5% (16)) | (38.5% / 13.3% (15)) | (0.0% / 0.0% (3)) | too few rows |

### transition:staying_bus_late_after_drop:5702 (medium, open)

Apostolic; scope: hours=10-11;days=weekday;note=staying bus 14.7 min vs 6.2 min at other times, 42 times from 21 drops, late by 3 min or more 92.9 vs 60.6 percent, top spot Wyler Pavilion (1 of 3) (not applied: note=staying bus 14.7 min vs 6.2 min at other times, 42 times from 21 drops, late by 3 min or more 92.9 vs 60.6 percent, top spot Wyler Pavilion (1 of 3)); 133 samples. Flag: mean absolute error of the staying bus's Passio times 10 to 20 min ahead in the 45 min after a 2-to-1 drop, divided by the line's at other times 2.37 (all lines 0.956).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Apostolic | 133 | 6.7% / 0.0% (45) | 0.0% / 0.0% (40) | 0.0% / 0.0% (37) | (0.0% / 0.0% (11)) |  | reference |
| timetable_delay | Apostolic | 133 | 2.3% / 22.2% (45) | 0.0% / 5.0% (40) | 24.0% / 13.5% (37) | (0.0% / 9.1% (11)) |  | loses: band B 2.3% vs Passio 6.7% at 0-10 min; too late 22.2% vs Passio 0.0% at 0-10 min; too late 5.0% vs Passio 0.0% at 10-15 min; too late 13.5% vs Passio 0.0% at 15-20 min |
| gbm_q15 | Apostolic | 133 | 15.0% / 2.2% (45) | 0.0% / 0.0% (40) | 0.0% / 0.0% (37) | (0.0% / 0.0% (11)) |  | loses: too late 2.2% vs Passio 0.0% at 0-10 min |
| deep_q15 | Apostolic | 133 | 12.5% / 2.2% (45) | 0.0% / 0.0% (40) | 0.0% / 0.0% (37) | (0.0% / 0.0% (11)) |  | loses: too late 2.2% vs Passio 0.0% at 0-10 min |
| deep_safe | Apostolic | 133 | 7.3% / 2.2% (45) | 0.0% / 0.0% (40) | 0.0% / 0.0% (37) | (0.0% / 0.0% (11)) |  | loses: too late 2.2% vs Passio 0.0% at 0-10 min |

### transition:bunching_after_add:6126 (medium, open)

Apostolic/Drexel; scope: hours=17-19;days=weekday;stops=8612;note=before Nov 6 8.889, from Nov 6 22.222 (2 episodes), top spot Goldblatt Pavilion (7 of 10) (not applied: note=before Nov 6 8.889, from Nov 6 22.222 (2 episodes), top spot Goldblatt Pavilion (7 of 10)); 221 samples. Flag: joins after which the new bus ran within 2 min of another at 3 stops in 30 min, per 100 joins that are not a layover 10.101 (all lines 4.045).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Apostolic/Drexel | 221 | 5.7% / 5.6% (71) | 0.0% / 0.0% (60) | 0.0% / 0.0% (58) | (0.0% / 0.0% (28)) | (0.0% / 0.0% (4)) | reference |
| timetable_delay | Apostolic/Drexel | 221 | 4.4% / 94.4% (71) | 0.0% / 95.0% (60) | 3.8% / 91.4% (58) | (12.0% / 75.0% (28)) | (0.0% / 0.0% (4)) | loses: band B 4.4% vs Passio 5.7% at 0-10 min; too late 94.4% vs Passio 5.6% at 0-10 min; too late 95.0% vs Passio 0.0% at 10-15 min; too late 91.4% vs Passio 0.0% at 15-20 min |
| gbm_q15 | Apostolic/Drexel | 221 | 5.6% / 5.6% (71) | 1.7% / 0.0% (60) | 0.0% / 0.0% (58) | (0.0% / 0.0% (28)) | (0.0% / 0.0% (4)) | holds |
| deep_q15 | Apostolic/Drexel | 221 | 12.7% / 11.3% (71) | 1.7% / 1.7% (60) | 5.7% / 0.0% (58) | (0.0% / 0.0% (28)) | (0.0% / 0.0% (4)) | loses: too late 11.3% vs Passio 5.6% at 0-10 min; too late 1.7% vs Passio 0.0% at 10-15 min |
| deep_safe | Apostolic/Drexel | 221 | 5.6% / 8.5% (71) | 0.0% / 1.7% (60) | 3.8% / 0.0% (58) | (0.0% / 0.0% (28)) | (0.0% / 0.0% (4)) | loses: too late 8.5% vs Passio 5.6% at 0-10 min; too late 1.7% vs Passio 0.0% at 10-15 min |

### display:false_hide_offroute_serving_bus:6126 (medium, open)

Apostolic/Drexel; scope: hours=18-21;vehicles=4331;stops=8609;note=after the rules shipped (2026-11-06 to 2026-11-10): 56.6 vs all lines 24.4, 141 events (not applied: note=after the rules shipped (2026-11-06 to 2026-11-10): 56.6 vs all lines 24.4, 141 events); 20 samples. Flag: percent of minutes core/offroute.js hid a bus (and its times) that then logged an arrival on the line within 15 min 37.0 (all lines 19.6).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Apostolic/Drexel | 20 | (0.0% / 18.2% (11)) | (0.0% / 0.0% (7)) | (0.0% / 0.0% (2)) |  |  | reference |
| timetable_delay | Apostolic/Drexel | 20 | (0.0% / 18.2% (11)) | (0.0% / 14.3% (7)) | (0.0% / 0.0% (2)) |  |  | too few rows |
| gbm_q15 | Apostolic/Drexel | 20 | (0.0% / 9.1% (11)) | (0.0% / 0.0% (7)) | (0.0% / 0.0% (2)) |  |  | too few rows |
| deep_q15 | Apostolic/Drexel | 20 | (27.3% / 0.0% (11)) | (0.0% / 0.0% (7)) | (0.0% / 0.0% (2)) |  |  | too few rows |
| deep_safe | Apostolic/Drexel | 20 | (9.1% / 0.0% (11)) | (0.0% / 0.0% (7)) | (0.0% / 0.0% (2)) |  |  | too few rows |

### transition:feed_drop_mid_route:6126 (medium, open)

Apostolic/Drexel; scope: vehicles=4322;days=weekday;stops=8623;note=before Nov 6 1.842, from Nov 6 0 (0 episodes), top spot South Campus Resident Hall (70 of 81) (not applied: note=before Nov 6 1.842, from Nov 6 0 (0 episodes), top spot South Campus Resident Hall (70 of 81)); 0 samples. Flag: buses vanishing from the feed while moving on the line (5 min or more), per 10 bus-hours inside transition windows (30 min around a bus count change, a shift change, a listed start or end, a timetable step) 1.622 (all lines 0.958).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Apostolic/Drexel | 0 |  |  |  |  |  | no rows |
| timetable_delay | Apostolic/Drexel | 0 |  |  |  |  |  | no rows |
| gbm_q15 | Apostolic/Drexel | 0 |  |  |  |  |  | no rows |
| deep_q15 | Apostolic/Drexel | 0 |  |  |  |  |  | no rows |
| deep_safe | Apostolic/Drexel | 0 |  |  |  |  |  | no rows |

### prediction_miss:large_late_miss:6126 (medium, open)

Apostolic/Drexel; scope: lead=5-45;note=last 14 days 66.9%, before them 65.5% (same) (not applied: note=last 14 days 66.9%, before them 65.5% (same)); 8,536 samples. Flag: share of Passio's times 5 to 30 min ahead that the bus came later than by more than the large-miss threshold (2 min at 5 to 15 min ahead, 4 at 20, 5 at 30), last 14 service days 0.6687 (all lines 0.5529).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Apostolic/Drexel | 8,536 | 12.6% / 25.7% (1,779) | 9.1% / 9.6% (2,860) | 8.2% / 7.2% (2,026) | 16.4% / 3.3% (1,384) | 2.5% / 0.4% (487) | reference |
| timetable_delay | Apostolic/Drexel | 8,536 | 4.3% / 55.8% (1,779) | 5.9% / 43.6% (2,860) | 8.7% / 34.3% (2,026) | 28.5% / 33.2% (1,384) | 21.5% / 36.3% (487) | loses: band B 4.3% vs Passio 12.6% at 0-10 min; too late 55.8% vs Passio 25.7% at 0-10 min; band B 5.9% vs Passio 9.1% at 10-15 min; too late 43.6% vs Passio 9.6% at 10-15 min; too late 34.3% vs Passio 7.2% at 15-20 min; too late 33.2% vs Passio 3.3% at 20-30 min; too late 36.3% vs Passio 0.4% at 30-45 min |
| gbm_q15 | Apostolic/Drexel | 8,536 | 20.6% / 16.1% (1,779) | 10.2% / 6.6% (2,860) | 6.0% / 6.1% (2,026) | 12.7% / 2.5% (1,384) | 2.3% / 0.2% (487) | loses: band B 6.0% vs Passio 8.2% at 15-20 min; band B 12.7% vs Passio 16.4% at 20-30 min |
| deep_q15 | Apostolic/Drexel | 8,536 | 23.1% / 19.2% (1,779) | 12.2% / 10.5% (2,860) | 14.5% / 7.5% (2,026) | 13.6% / 2.3% (1,384) | 1.9% / 0.0% (487) | loses: band B 13.6% vs Passio 16.4% at 20-30 min; band B 1.9% vs Passio 2.5% at 30-45 min |
| deep_safe | Apostolic/Drexel | 8,536 | 22.4% / 13.9% (1,779) | 10.5% / 10.3% (2,860) | 14.1% / 7.1% (2,026) | 14.0% / 2.7% (1,384) | 1.6% / 0.0% (487) | loses: band B 14.0% vs Passio 16.4% at 20-30 min; band B 1.6% vs Passio 2.5% at 30-45 min |

### transition:off_route_drive:6126 (medium, open)

Apostolic/Drexel; scope: hours=16-21;days=weekday;note=before Nov 6 5.603, from Nov 6 4.817 (25 episodes), top spot 63rd & Ellis (84 of 270) (not applied: note=before Nov 6 5.603, from Nov 6 4.817 (25 episodes), top spot 63rd & Ellis (84 of 270)); 4,433 samples. Flag: bus more than 250 m from its line and its learned corridor (45 s, 2 reports) inside its listed hours, per 10 bus-hours inside transition windows (30 min around a bus count change, a shift change, a listed start or end, a timetable step) 5.509 (all lines 3.487).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Apostolic/Drexel | 4,433 | 12.3% / 25.0% (1,621) | 3.6% / 4.3% (1,222) | 2.2% / 5.0% (824) | 4.6% / 0.7% (566) | 0.0% / 0.5% (200) | reference |
| timetable_delay | Apostolic/Drexel | 4,433 | 7.2% / 57.2% (1,621) | 6.2% / 44.8% (1,222) | 10.3% / 37.5% (824) | 32.6% / 36.9% (566) | 18.2% / 39.0% (200) | loses: band B 7.2% vs Passio 12.3% at 0-10 min; too late 57.2% vs Passio 25.0% at 0-10 min; too late 44.8% vs Passio 4.3% at 10-15 min; too late 37.5% vs Passio 5.0% at 15-20 min; too late 36.9% vs Passio 0.7% at 20-30 min; too late 39.0% vs Passio 0.5% at 30-45 min |
| gbm_q15 | Apostolic/Drexel | 4,433 | 23.0% / 16.2% (1,621) | 5.2% / 4.3% (1,222) | 1.1% / 4.5% (824) | 1.2% / 0.2% (566) | 0.0% / 0.5% (200) | loses: band B 1.1% vs Passio 2.2% at 15-20 min; band B 1.2% vs Passio 4.6% at 20-30 min |
| deep_q15 | Apostolic/Drexel | 4,433 | 25.9% / 19.0% (1,621) | 7.0% / 4.7% (1,222) | 8.3% / 3.3% (824) | 2.1% / 0.5% (566) | 1.0% / 0.0% (200) | loses: band B 2.1% vs Passio 4.6% at 20-30 min |
| deep_safe | Apostolic/Drexel | 4,433 | 23.6% / 14.4% (1,621) | 5.8% / 4.0% (1,222) | 7.1% / 3.4% (824) | 2.5% / 0.5% (566) | 1.0% / 0.0% (200) | loses: band B 2.5% vs Passio 4.6% at 20-30 min |

### transition:wrong_line_label:6126 (medium, open)

Apostolic/Drexel; scope: vehicles=4331;hours=18-19;days=weekday;note=before Nov 6 0.691, from Nov 6 0.85 (3 episodes), top spot Goldblatt Pavilion (9 of 23) (not applied: note=before Nov 6 0.691, from Nov 6 0.85 (3 episodes), top spot Goldblatt Pavilion (9 of 23)); 62 samples. Flag: bus labeled this line while it drove another line's road for 30 min or more, per 10 bus-hours inside transition windows (30 min around a bus count change, a shift change, a listed start or end, a timetable step) 0.71 (all lines 0.301).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Apostolic/Drexel | 62 | 0.0% / 22.2% (36) | (10.0% / 0.0% (18)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (4)) |  | reference |
| timetable_delay | Apostolic/Drexel | 62 | 0.0% / 13.9% (36) | (50.0% / 0.0% (18)) | (50.0% / 50.0% (4)) | (50.0% / 50.0% (4)) |  | holds |
| gbm_q15 | Apostolic/Drexel | 62 | 2.8% / 16.7% (36) | (0.0% / 0.0% (18)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (4)) |  | holds |
| deep_q15 | Apostolic/Drexel | 62 | 5.6% / 11.1% (36) | (0.0% / 0.0% (18)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (4)) |  | holds |
| deep_safe | Apostolic/Drexel | 62 | 5.6% / 8.3% (36) | (0.0% / 0.0% (18)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (4)) |  | holds |

### transition:extra_bus_added:1078 (medium, open)

Central; scope: hours=18-20;note=before Nov 6 64.706, from Nov 6 0 (0 episodes), top spot Reynolds Club (4 of 11) (not applied: note=before Nov 6 64.706, from Nov 6 0 (0 episodes), top spot Reynolds Club (4 of 11)); 1,824 samples. Flag: buses joining the line above its listed bus count (no timetable change), per 100 joins that are not a layover 61.111 (all lines 21.236).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Central | 1,824 | 9.1% / 63.8% (473) | 13.5% / 15.9% (408) | 12.9% / 3.6% (412) | 31.1% / 3.3% (421) | 12.0% / 0.0% (110) | reference |
| timetable_delay | Central | 1,824 | 3.9% / 23.0% (473) | 0.0% / 56.9% (408) | 2.6% / 73.1% (412) | 15.0% / 67.2% (421) | 12.9% / 2.7% (110) | loses: band B 3.9% vs Passio 9.1% at 0-10 min; band B 0.0% vs Passio 13.5% at 10-15 min; too late 56.9% vs Passio 15.9% at 10-15 min; band B 2.6% vs Passio 12.9% at 15-20 min; too late 73.1% vs Passio 3.6% at 15-20 min; band B 15.0% vs Passio 31.1% at 20-30 min; too late 67.2% vs Passio 3.3% at 20-30 min; too late 2.7% vs Passio 0.0% at 30-45 min |
| gbm_q15 | Central | 1,824 | 20.8% / 41.4% (473) | 16.6% / 12.3% (408) | 16.6% / 9.2% (412) | 35.8% / 5.9% (421) | 2.5% / 0.0% (110) | loses: too late 9.2% vs Passio 3.6% at 15-20 min; too late 5.9% vs Passio 3.3% at 20-30 min; band B 2.5% vs Passio 12.0% at 30-45 min |
| deep_q15 | Central | 1,824 | 27.9% / 22.2% (473) | 18.1% / 15.7% (408) | 18.1% / 9.5% (412) | 34.5% / 5.5% (421) | 5.6% / 0.0% (110) | loses: too late 9.5% vs Passio 3.6% at 15-20 min; too late 5.5% vs Passio 3.3% at 20-30 min; band B 5.6% vs Passio 12.0% at 30-45 min |
| deep_safe | Central | 1,824 | 25.4% / 20.1% (473) | 16.0% / 15.4% (408) | 14.5% / 9.2% (412) | 35.0% / 7.6% (421) | 6.7% / 0.0% (110) | loses: too late 9.2% vs Passio 3.6% at 15-20 min; too late 7.6% vs Passio 3.3% at 20-30 min; band B 6.7% vs Passio 12.0% at 30-45 min |

### prediction_miss:stops_without_predictions:1078 (medium, open)

Central; scope: stops=141882|8584|8644|8597;lead=0-10;note=a time at any lead 1 to 30 min ahead 73%, before the last 14 days 66% of 708 arrivals had one 5 min ahead (not applied: note=a time at any lead 1 to 30 min ahead 73%, before the last 14 days 66% of 708 arrivals had one 5 min ahead); 278 samples. Flag: share of arrivals at the scope's stops with a Passio time on display 5 min ahead, last 14 service days 0.1243 (all lines 0.6594).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Central | 278 | 16.6% / 50.4% (278) |  |  |  |  | reference |
| timetable_delay | Central | 278 | 16.0% / 62.2% (278) |  |  |  |  | loses: too late 62.2% vs Passio 50.4% at 0-10 min |
| gbm_q15 | Central | 278 | 16.6% / 54.7% (278) |  |  |  |  | loses: too late 54.7% vs Passio 50.4% at 0-10 min |
| deep_q15 | Central | 278 | 17.6% / 55.0% (278) |  |  |  |  | loses: too late 55.0% vs Passio 50.4% at 0-10 min |
| deep_safe | Central | 278 | 21.2% / 47.5% (278) |  |  |  |  | holds |

### prediction_miss:worse_when_behind:1078 (medium, open)

Central; scope: lead=5-30;note=delay_s > 600 in the forecast table (not applied: note=delay_s > 600 in the forecast table); 4,850 samples. Flag: large-miss rate (goal leads) while the bus ran more than 10 min behind the timetable divided by the rate otherwise on the same line, all days 1.3071 (all lines 1.2148).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Central | 4,850 | 10.6% / 59.2% (786) | 13.8% / 25.4% (1,265) | 14.0% / 12.1% (1,337) | 32.7% / 10.7% (1,462) |  | reference |
| timetable_delay | Central | 4,850 | 1.2% / 26.1% (786) | 0.2% / 51.5% (1,265) | 1.6% / 73.7% (1,337) | 14.9% / 71.4% (1,462) |  | loses: band B 1.2% vs Passio 10.6% at 0-10 min; band B 0.2% vs Passio 13.8% at 10-15 min; too late 51.5% vs Passio 25.4% at 10-15 min; band B 1.6% vs Passio 14.0% at 15-20 min; too late 73.7% vs Passio 12.1% at 15-20 min; band B 14.9% vs Passio 32.7% at 20-30 min; too late 71.4% vs Passio 10.7% at 20-30 min |
| gbm_q15 | Central | 4,850 | 19.0% / 37.8% (786) | 16.6% / 18.1% (1,265) | 19.0% / 11.1% (1,337) | 39.2% / 6.7% (1,462) |  | holds |
| deep_q15 | Central | 4,850 | 23.5% / 26.7% (786) | 21.5% / 20.3% (1,265) | 20.8% / 13.4% (1,337) | 38.8% / 6.5% (1,462) |  | loses: too late 13.4% vs Passio 12.1% at 15-20 min |
| deep_safe | Central | 4,850 | 24.7% / 22.9% (786) | 19.8% / 20.2% (1,265) | 19.1% / 12.7% (1,337) | 39.4% / 9.0% (1,462) |  | holds |

### display:bus_number_churn:5704 (medium, open)

Downtown Campus Connector; scope: note=after the rules shipped (2026-11-06 to 2026-11-10): 120.42 vs all lines 14.7, 569 events (not applied: note=after the rules shipped (2026-11-06 to 2026-11-10): 120.42 vs all lines 14.7, 569 events); 9,308 samples. Flag: Bus 1 / Bus 2 swaps per 10 service hours (a bus shown in two polls in a row whose number changed) 119.35 (all lines 16.53).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Downtown Campus Connector | 9,308 | 4.8% / 37.5% (1,661) | 9.8% / 27.2% (1,858) | 11.9% / 20.4% (1,940) | 14.5% / 5.6% (1,942) | 5.7% / 2.0% (1,907) | reference |
| timetable_delay | Downtown Campus Connector | 9,308 | 4.8% / 37.5% (1,661) | 9.8% / 27.2% (1,858) | 11.9% / 20.4% (1,940) | 14.5% / 5.6% (1,942) | 5.7% / 2.0% (1,907) | holds |
| gbm_q15 | Downtown Campus Connector | 9,308 | 17.5% / 26.6% (1,661) | 16.3% / 22.9% (1,858) | 14.5% / 13.6% (1,940) | 13.7% / 4.9% (1,942) | 6.1% / 2.4% (1,907) | holds |
| deep_q15 | Downtown Campus Connector | 9,308 | 19.8% / 19.4% (1,661) | 17.7% / 15.6% (1,858) | 14.0% / 12.7% (1,940) | 18.3% / 6.7% (1,942) | 9.1% / 1.3% (1,907) | loses: too late 6.7% vs Passio 5.6% at 20-30 min |
| deep_safe | Downtown Campus Connector | 9,308 | 17.6% / 17.2% (1,661) | 18.3% / 15.3% (1,858) | 13.7% / 13.5% (1,940) | 17.2% / 8.3% (1,942) | 10.4% / 2.9% (1,907) | loses: too late 8.3% vs Passio 5.6% at 20-30 min |

### transition:frozen_gps:5704 (medium, open)

Downtown Campus Connector; scope: days=weekday;note=before Nov 6 0.142, from Nov 6 0 (0 episodes), top spot Unnamed (41.8102, -87.5905) (5 of 16) (not applied: note=before Nov 6 0.142, from Nov 6 0 (0 episodes), top spot Unnamed (41.8102, -87.5905) (5 of 16)); 9,308 samples. Flag: GPS frozen at one point for 5 min while the bus moved, per 10 bus-hours inside transition windows (30 min around a bus count change, a shift change, a listed start or end, a timetable step) 0.122 (all lines 0.055).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Downtown Campus Connector | 9,308 | 4.8% / 37.5% (1,661) | 9.8% / 27.2% (1,858) | 11.9% / 20.4% (1,940) | 14.5% / 5.6% (1,942) | 5.7% / 2.0% (1,907) | reference |
| timetable_delay | Downtown Campus Connector | 9,308 | 4.8% / 37.5% (1,661) | 9.8% / 27.2% (1,858) | 11.9% / 20.4% (1,940) | 14.5% / 5.6% (1,942) | 5.7% / 2.0% (1,907) | holds |
| gbm_q15 | Downtown Campus Connector | 9,308 | 17.5% / 26.6% (1,661) | 16.3% / 22.9% (1,858) | 14.5% / 13.6% (1,940) | 13.7% / 4.9% (1,942) | 6.1% / 2.4% (1,907) | holds |
| deep_q15 | Downtown Campus Connector | 9,308 | 19.8% / 19.4% (1,661) | 17.7% / 15.6% (1,858) | 14.0% / 12.7% (1,940) | 18.3% / 6.7% (1,942) | 9.1% / 1.3% (1,907) | loses: too late 6.7% vs Passio 5.6% at 20-30 min |
| deep_safe | Downtown Campus Connector | 9,308 | 17.6% / 17.2% (1,661) | 18.3% / 15.3% (1,858) | 13.7% / 13.5% (1,940) | 17.2% / 8.3% (1,942) | 10.4% / 2.9% (1,907) | loses: too late 8.3% vs Passio 5.6% at 20-30 min |

### display:ghost_times_after_leave:5704 (medium, open)

Downtown Campus Connector; scope: note=2026-10-10 to 2026-11-10: 6.5 vs all lines 4.6 (not applied: note=2026-10-10 to 2026-11-10: 6.5 vs all lines 4.6); 9,308 samples. Flag: percent of bus-minutes with times on display (1 to 30 min ahead) from a bus that then logged no arrival on the line until 15 min after its last displayed time (shipped rules) 6.0 (all lines 3.9).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Downtown Campus Connector | 9,308 | 4.8% / 37.5% (1,661) | 9.8% / 27.2% (1,858) | 11.9% / 20.4% (1,940) | 14.5% / 5.6% (1,942) | 5.7% / 2.0% (1,907) | reference |
| timetable_delay | Downtown Campus Connector | 9,308 | 4.8% / 37.5% (1,661) | 9.8% / 27.2% (1,858) | 11.9% / 20.4% (1,940) | 14.5% / 5.6% (1,942) | 5.7% / 2.0% (1,907) | holds |
| gbm_q15 | Downtown Campus Connector | 9,308 | 17.5% / 26.6% (1,661) | 16.3% / 22.9% (1,858) | 14.5% / 13.6% (1,940) | 13.7% / 4.9% (1,942) | 6.1% / 2.4% (1,907) | holds |
| deep_q15 | Downtown Campus Connector | 9,308 | 19.8% / 19.4% (1,661) | 17.7% / 15.6% (1,858) | 14.0% / 12.7% (1,940) | 18.3% / 6.7% (1,942) | 9.1% / 1.3% (1,907) | loses: too late 6.7% vs Passio 5.6% at 20-30 min |
| deep_safe | Downtown Campus Connector | 9,308 | 17.6% / 17.2% (1,661) | 18.3% / 15.3% (1,858) | 13.7% / 13.5% (1,940) | 17.2% / 8.3% (1,942) | 10.4% / 2.9% (1,907) | loses: too late 8.3% vs Passio 5.6% at 20-30 min |

### prediction_miss:large_early_miss:5704 (medium, open)

Downtown Campus Connector; scope: lead=5-30;stops=151793|151792|132967;note=last 14 days 15.6%, before them 3.2% (worse) (not applied: note=last 14 days 15.6%, before them 3.2% (worse)); 1,896 samples. Flag: share of Passio's times 5 to 30 min ahead that the bus beat by more than the large-miss threshold (2 min at 5 to 15 min ahead, 4 at 20, 5 at 30), last 14 service days 0.1555 (all lines 0.1098).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Downtown Campus Connector | 1,896 | 2.7% / 97.4% (304) | 10.4% / 80.1% (542) | 15.5% / 63.8% (530) | 17.0% / 15.6% (520) |  | reference |
| timetable_delay | Downtown Campus Connector | 1,896 | 2.7% / 97.4% (304) | 10.4% / 80.1% (542) | 15.5% / 63.8% (530) | 17.0% / 15.6% (520) |  | holds |
| gbm_q15 | Downtown Campus Connector | 1,896 | 17.1% / 56.6% (304) | 16.8% / 58.3% (542) | 15.1% / 38.7% (530) | 14.8% / 13.7% (520) |  | loses: band B 14.8% vs Passio 17.0% at 20-30 min |
| deep_q15 | Downtown Campus Connector | 1,896 | 25.4% / 37.5% (304) | 17.6% / 33.4% (542) | 12.5% / 33.0% (530) | 18.5% / 15.6% (520) |  | loses: band B 12.5% vs Passio 15.5% at 15-20 min |
| deep_safe | Downtown Campus Connector | 1,896 | 22.7% / 33.9% (304) | 19.9% / 34.9% (542) | 12.3% / 36.6% (530) | 17.2% / 21.0% (520) |  | loses: band B 12.3% vs Passio 15.5% at 15-20 min; too late 21.0% vs Passio 15.6% at 20-30 min |

### prediction_miss:large_late_miss:5704 (medium, open)

Downtown Campus Connector; scope: lead=5-45;note=last 14 days 67.5%, before them 69.8% (same) (not applied: note=last 14 days 67.5%, before them 69.8% (same)); 8,627 samples. Flag: share of Passio's times 5 to 30 min ahead that the bus came later than by more than the large-miss threshold (2 min at 5 to 15 min ahead, 4 at 20, 5 at 30), last 14 service days 0.6747 (all lines 0.5529).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Downtown Campus Connector | 8,627 | 5.4% / 34.7% (980) | 9.8% / 27.2% (1,858) | 11.9% / 20.4% (1,940) | 14.5% / 5.6% (1,942) | 5.7% / 2.0% (1,907) | reference |
| timetable_delay | Downtown Campus Connector | 8,627 | 5.4% / 34.7% (980) | 9.8% / 27.2% (1,858) | 11.9% / 20.4% (1,940) | 14.5% / 5.6% (1,942) | 5.7% / 2.0% (1,907) | holds |
| gbm_q15 | Downtown Campus Connector | 8,627 | 17.4% / 23.2% (980) | 16.3% / 22.9% (1,858) | 14.5% / 13.6% (1,940) | 13.7% / 4.9% (1,942) | 6.1% / 2.4% (1,907) | holds |
| deep_q15 | Downtown Campus Connector | 8,627 | 20.9% / 16.4% (980) | 17.7% / 15.6% (1,858) | 14.0% / 12.7% (1,940) | 18.3% / 6.7% (1,942) | 9.1% / 1.3% (1,907) | loses: too late 6.7% vs Passio 5.6% at 20-30 min |
| deep_safe | Downtown Campus Connector | 8,627 | 17.9% / 14.6% (980) | 18.3% / 15.3% (1,858) | 13.7% / 13.5% (1,940) | 17.2% / 8.3% (1,942) | 10.4% / 2.9% (1,907) | loses: too late 8.3% vs Passio 5.6% at 20-30 min |

### transition:after_hours:5701 (medium, open)

Drexel; scope: hours=10-11;days=weekday;note=before Nov 6 1.322, from Nov 6 3.267 (3 episodes), top spot Rockefeller Chapel (3 of 11) (not applied: note=before Nov 6 1.322, from Nov 6 3.267 (3 episodes), top spot Rockefeller Chapel (3 of 11)); 16 samples. Flag: bus reporting under the line's label more than 15 min after (30 min before) its listed hours, per 10 bus-hours inside transition windows (30 min around a bus count change, a shift change, a listed start or end, a timetable step) 1.61 (all lines 0.491).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Drexel | 16 | (0.0% / 0.0% (6)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | reference |
| timetable_delay | Drexel | 16 | (0.0% / 33.3% (6)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | too few rows |
| gbm_q15 | Drexel | 16 | (0.0% / 16.7% (6)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | too few rows |
| deep_q15 | Drexel | 16 | (0.0% / 33.3% (6)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | too few rows |
| deep_safe | Drexel | 16 | (0.0% / 16.7% (6)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | too few rows |

### display:ghost_times_after_leave:5701 (medium, open)

Drexel; scope: hours=09-11;note=2026-10-10 to 2026-11-10: 2.4 vs all lines 4.6 (not applied: note=2026-10-10 to 2026-11-10: 2.4 vs all lines 4.6); 418 samples. Flag: percent of bus-minutes with times on display (1 to 30 min ahead) from a bus that then logged no arrival on the line until 15 min after its last displayed time (shipped rules) 5.9 (all lines 3.9).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Drexel | 418 | 19.2% / 6.8% (207) | 12.9% / 3.0% (100) | 10.2% / 4.9% (82) | (8.3% / 0.0% (25)) | (0.0% / 0.0% (4)) | reference |
| timetable_delay | Drexel | 418 | 10.6% / 64.7% (207) | 20.5% / 31.0% (100) | 32.9% / 35.4% (82) | (29.4% / 8.0% (25)) | (0.0% / 0.0% (4)) | loses: band B 10.6% vs Passio 19.2% at 0-10 min; too late 64.7% vs Passio 6.8% at 0-10 min; too late 31.0% vs Passio 3.0% at 10-15 min; too late 35.4% vs Passio 4.9% at 15-20 min |
| gbm_q15 | Drexel | 418 | 30.1% / 12.1% (207) | 15.4% / 3.0% (100) | 9.8% / 2.4% (82) | (0.0% / 0.0% (25)) | (0.0% / 0.0% (4)) | loses: too late 12.1% vs Passio 6.8% at 0-10 min |
| deep_q15 | Drexel | 418 | 26.8% / 14.0% (207) | 12.7% / 5.0% (100) | 12.9% / 4.9% (82) | (7.1% / 0.0% (25)) | (0.0% / 0.0% (4)) | loses: too late 14.0% vs Passio 6.8% at 0-10 min; too late 5.0% vs Passio 3.0% at 10-15 min |
| deep_safe | Drexel | 418 | 25.6% / 11.6% (207) | 14.9% / 6.0% (100) | 10.2% / 4.9% (82) | (7.1% / 0.0% (25)) | (0.0% / 0.0% (4)) | loses: too late 11.6% vs Passio 6.8% at 0-10 min; too late 6.0% vs Passio 3.0% at 10-15 min |

### transition:off_route_drive:5701 (medium, open)

Drexel; scope: hours=10-11;days=weekday;note=before Nov 6 5.667, from Nov 6 6.533 (6 episodes), top spot Apostolic Lot (10 of 36) (not applied: note=before Nov 6 5.667, from Nov 6 6.533 (6 episodes), top spot Apostolic Lot (10 of 36)); 16 samples. Flag: bus more than 250 m from its line and its learned corridor (45 s, 2 reports) inside its listed hours, per 10 bus-hours inside transition windows (30 min around a bus count change, a shift change, a listed start or end, a timetable step) 5.795 (all lines 3.487).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Drexel | 16 | (0.0% / 0.0% (6)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | reference |
| timetable_delay | Drexel | 16 | (0.0% / 33.3% (6)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | too few rows |
| gbm_q15 | Drexel | 16 | (0.0% / 16.7% (6)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | too few rows |
| deep_q15 | Drexel | 16 | (0.0% / 33.3% (6)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | too few rows |
| deep_safe | Drexel | 16 | (0.0% / 16.7% (6)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (4)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | too few rows |

### prediction_miss:stops_without_predictions:5701 (medium, open)

Drexel; scope: stops=8612|8613;lead=0-10;note=a time at any lead 1 to 30 min ahead 85%, before the last 14 days 64% of 597 arrivals had one 5 min ahead (not applied: note=a time at any lead 1 to 30 min ahead 85%, before the last 14 days 64% of 597 arrivals had one 5 min ahead); 306 samples. Flag: share of arrivals at the scope's stops with a Passio time on display 5 min ahead, last 14 service days 0.1849 (all lines 0.6594).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Drexel | 306 | 35.0% / 14.1% (306) |  |  |  |  | reference |
| timetable_delay | Drexel | 306 | 7.8% / 76.1% (306) |  |  |  |  | loses: band B 7.8% vs Passio 35.0% at 0-10 min; too late 76.1% vs Passio 14.1% at 0-10 min |
| gbm_q15 | Drexel | 306 | 44.0% / 16.3% (306) |  |  |  |  | loses: too late 16.3% vs Passio 14.1% at 0-10 min |
| deep_q15 | Drexel | 306 | 42.3% / 13.7% (306) |  |  |  |  | holds |
| deep_safe | Drexel | 306 | 41.2% / 12.7% (306) |  |  |  |  | holds |

### transition:extra_bus_added:1077 (medium, open)

East; scope: hours=18-21;stops=8579;note=before Nov 6 66.667, from Nov 6 80.0 (4 episodes), top spot Reynolds Club (10 of 16) (not applied: note=before Nov 6 66.667, from Nov 6 80.0 (4 episodes), top spot Reynolds Club (10 of 16)); 176 samples. Flag: buses joining the line above its listed bus count (no timetable change), per 100 joins that are not a layover 69.565 (all lines 21.236).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | East | 176 | 0.0% / 0.0% (52) | 0.0% / 2.2% (46) | 0.0% / 0.0% (43) | 0.0% / 0.0% (30) | (0.0% / 0.0% (5)) | reference |
| timetable_delay | East | 176 | 26.9% / 0.0% (52) | 0.0% / 0.0% (46) | 0.0% / 4.7% (43) | 0.0% / 0.0% (30) | (0.0% / 0.0% (5)) | loses: too late 4.7% vs Passio 0.0% at 15-20 min |
| gbm_q15 | East | 176 | 7.7% / 0.0% (52) | 6.7% / 2.2% (46) | 0.0% / 0.0% (43) | 0.0% / 0.0% (30) | (0.0% / 0.0% (5)) | holds |
| deep_q15 | East | 176 | 3.8% / 1.9% (52) | 6.7% / 4.3% (46) | 16.3% / 2.3% (43) | 10.7% / 0.0% (30) | (0.0% / 0.0% (5)) | loses: too late 1.9% vs Passio 0.0% at 0-10 min; too late 4.3% vs Passio 2.2% at 10-15 min; too late 2.3% vs Passio 0.0% at 15-20 min |
| deep_safe | East | 176 | 3.8% / 0.0% (52) | 11.1% / 2.2% (46) | 20.9% / 0.0% (43) | 25.9% / 0.0% (30) | (0.0% / 0.0% (5)) | holds |

### prediction_miss:other_trip_times:1077 (medium, open)

East; scope: stops=140014;lead=0-10;note=stop positions 9, 35 of 40 times the bus came earlier than shown (not applied: note=stop positions 9, 35 of 40 times the bus came earlier than shown); 146 samples. Flag: share of the times a screen showed only under another trip id of the same bus 5 min ahead (no own-trip time) that were large misses (more than 2 min either way), last 14 service days 0.8750 (all lines 0.5822).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | East | 146 | 2.8% / 96.6% (146) |  |  |  |  | reference |
| timetable_delay | East | 146 | 2.8% / 11.0% (146) |  |  |  |  | holds |
| gbm_q15 | East | 146 | 21.9% / 21.2% (146) |  |  |  |  | holds |
| deep_q15 | East | 146 | 28.8% / 19.2% (146) |  |  |  |  | holds |
| deep_safe | East | 146 | 19.2% / 17.1% (146) |  |  |  |  | holds |

### prediction_miss:worse_when_behind:1077 (medium, open)

East; scope: lead=5-30;note=delay_s > 600 in the forecast table (not applied: note=delay_s > 600 in the forecast table); 4,691 samples. Flag: large-miss rate (goal leads) while the bus ran more than 10 min behind the timetable divided by the rate otherwise on the same line, all days 1.3994 (all lines 1.2148).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | East | 4,691 | 10.2% / 58.7% (786) | 16.3% / 23.9% (1,438) | 11.4% / 6.8% (1,303) | 26.4% / 6.1% (1,164) |  | reference |
| timetable_delay | East | 4,691 | 2.9% / 21.9% (786) | 0.7% / 41.9% (1,438) | 3.1% / 59.2% (1,303) | 18.0% / 60.5% (1,164) |  | loses: band B 2.9% vs Passio 10.2% at 0-10 min; band B 0.7% vs Passio 16.3% at 10-15 min; too late 41.9% vs Passio 23.9% at 10-15 min; band B 3.1% vs Passio 11.4% at 15-20 min; too late 59.2% vs Passio 6.8% at 15-20 min; band B 18.0% vs Passio 26.4% at 20-30 min; too late 60.5% vs Passio 6.1% at 20-30 min |
| gbm_q15 | East | 4,691 | 23.1% / 24.3% (786) | 15.4% / 9.7% (1,438) | 12.4% / 6.7% (1,303) | 29.6% / 5.0% (1,164) |  | holds |
| deep_q15 | East | 4,691 | 26.5% / 23.3% (786) | 17.8% / 14.5% (1,438) | 16.2% / 8.8% (1,303) | 32.5% / 4.6% (1,164) |  | loses: too late 8.8% vs Passio 6.8% at 15-20 min |
| deep_safe | East | 4,691 | 22.9% / 19.3% (786) | 16.4% / 13.0% (1,438) | 15.7% / 9.0% (1,303) | 32.4% / 7.3% (1,164) |  | loses: too late 9.0% vs Passio 6.8% at 15-20 min; too late 7.3% vs Passio 6.1% at 20-30 min |

### transition:after_hours:5700 (medium, open)

Friend Center/Metra; scope: hours=21-22;days=weekday;note=before Nov 6 1.531, from Nov 6 3.391 (3 episodes), top spot Operator garage (5 of 12) (not applied: note=before Nov 6 1.531, from Nov 6 3.391 (3 episodes), top spot Operator garage (5 of 12)); 12 samples. Flag: bus reporting under the line's label more than 15 min after (30 min before) its listed hours, per 10 bus-hours inside transition windows (30 min around a bus count change, a shift change, a listed start or end, a timetable step) 1.873 (all lines 0.491).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Friend Center/Metra | 12 | (0.0% / 0.0% (5)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (2)) | reference |
| timetable_delay | Friend Center/Metra | 12 | (0.0% / 0.0% (5)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (2)) | too few rows |
| gbm_q15 | Friend Center/Metra | 12 | (0.0% / 0.0% (5)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (2)) | too few rows |
| deep_q15 | Friend Center/Metra | 12 | (0.0% / 0.0% (5)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (2)) | too few rows |
| deep_safe | Friend Center/Metra | 12 | (0.0% / 0.0% (5)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (2)) | too few rows |

### transition:extra_bus_added:5700 (medium, open)

Friend Center/Metra; scope: days=weekday;stops=8612;note=before Nov 6 92.308, from Nov 6 100.0 (2 episodes), top spot Goldblatt Pavilion (7 of 14) (not applied: note=before Nov 6 92.308, from Nov 6 100.0 (2 episodes), top spot Goldblatt Pavilion (7 of 14)); 643 samples. Flag: buses joining the line above its listed bus count (no timetable change), per 100 joins that are not a layover 93.333 (all lines 21.236).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Friend Center/Metra | 643 | 32.9% / 38.2% (157) | 13.2% / 40.8% (152) | 13.2% / 35.7% (154) | 24.8% / 25.0% (144) | 16.7% / 11.1% (36) | reference |
| timetable_delay | Friend Center/Metra | 643 | 12.2% / 15.9% (157) | 1.4% / 32.9% (152) | 3.5% / 32.5% (154) | 13.8% / 29.2% (144) | 28.6% / 5.6% (36) | loses: band B 12.2% vs Passio 32.9% at 0-10 min; band B 1.4% vs Passio 13.2% at 10-15 min; band B 3.5% vs Passio 13.2% at 15-20 min; band B 13.8% vs Passio 24.8% at 20-30 min; too late 29.2% vs Passio 25.0% at 20-30 min |
| gbm_q15 | Friend Center/Metra | 643 | 17.9% / 28.0% (157) | 7.5% / 31.6% (152) | 6.8% / 27.3% (154) | 18.5% / 18.1% (144) | 33.3% / 2.8% (36) | loses: band B 17.9% vs Passio 32.9% at 0-10 min; band B 7.5% vs Passio 13.2% at 10-15 min; band B 6.8% vs Passio 13.2% at 15-20 min; band B 18.5% vs Passio 24.8% at 20-30 min |
| deep_q15 | Friend Center/Metra | 643 | 30.3% / 40.1% (157) | 17.2% / 32.9% (152) | 14.8% / 24.7% (154) | 24.4% / 15.3% (144) | 10.5% / 0.0% (36) | loses: too late 40.1% vs Passio 38.2% at 0-10 min; band B 10.5% vs Passio 16.7% at 30-45 min |
| deep_safe | Friend Center/Metra | 643 | 27.6% / 33.8% (157) | 13.2% / 29.6% (152) | 15.4% / 23.4% (154) | 26.1% / 20.1% (144) | 15.8% / 0.0% (36) | loses: band B 27.6% vs Passio 32.9% at 0-10 min |

### prediction_miss:first_stop_next_trip_times:5700 (medium, open)

Friend Center/Metra; scope: stops=8613;lead=0-10;note=stop positions 1, 38 of 67 times the bus came earlier than shown (not applied: note=stop positions 1, 38 of 67 times the bus came earlier than shown); 148 samples. Flag: share of the times a screen showed only under another trip id of the same bus 5 min ahead (no own-trip time) that were large misses (more than 2 min either way), last 14 service days 0.9701 (all lines 0.5822).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Friend Center/Metra | 148 | 8.6% / 4.7% (148) |  |  |  |  | reference |
| timetable_delay | Friend Center/Metra | 148 | 5.1% / 72.3% (148) |  |  |  |  | loses: band B 5.1% vs Passio 8.6% at 0-10 min; too late 72.3% vs Passio 4.7% at 0-10 min |
| gbm_q15 | Friend Center/Metra | 148 | 10.4% / 4.7% (148) |  |  |  |  | holds |
| deep_q15 | Friend Center/Metra | 148 | 14.1% / 6.1% (148) |  |  |  |  | loses: too late 6.1% vs Passio 4.7% at 0-10 min |
| deep_safe | Friend Center/Metra | 148 | 8.5% / 5.4% (148) |  |  |  |  | holds |

### transition:off_route_drive:5700 (medium, open)

Friend Center/Metra; scope: hours=18-21;days=weekday;stops=8614;note=before Nov 6 5.102, from Nov 6 7.913 (11 episodes), top spot Apostolic Lot (30 of 53) (not applied: note=before Nov 6 5.102, from Nov 6 7.913 (11 episodes), top spot Apostolic Lot (30 of 53)); 0 samples. Flag: bus more than 250 m from its line and its learned corridor (45 s, 2 reports) inside its listed hours, per 10 bus-hours inside transition windows (30 min around a bus count change, a shift change, a listed start or end, a timetable step) 5.62 (all lines 3.487).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Friend Center/Metra | 0 |  |  |  |  |  | no rows |
| timetable_delay | Friend Center/Metra | 0 |  |  |  |  |  | no rows |
| gbm_q15 | Friend Center/Metra | 0 |  |  |  |  |  | no rows |
| deep_q15 | Friend Center/Metra | 0 |  |  |  |  |  | no rows |
| deep_safe | Friend Center/Metra | 0 |  |  |  |  |  | no rows |

### transition:service_start_missing:5700 (medium, open)

Friend Center/Metra; scope: hours=5-6;note=before Nov 6 29.63, from Nov 6 40.0 (2 episodes) (not applied: note=before Nov 6 29.63, from Nov 6 40.0 (2 episodes)); 504 samples. Flag: listed spans with no bus in their first 60 min, per 100 spans 31.25 (all lines 7.629).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Friend Center/Metra | 504 | 22.9% / 16.0% (131) | 11.2% / 11.1% (126) | 5.2% / 11.3% (115) | 18.2% / 7.3% (110) | (10.0% / 0.0% (22)) | reference |
| timetable_delay | Friend Center/Metra | 504 | 5.6% / 48.1% (131) | 9.5% / 40.5% (126) | 8.8% / 40.9% (115) | 17.3% / 25.5% (110) | (38.1% / 9.1% (22)) | loses: band B 5.6% vs Passio 22.9% at 0-10 min; too late 48.1% vs Passio 16.0% at 0-10 min; band B 9.5% vs Passio 11.2% at 10-15 min; too late 40.5% vs Passio 11.1% at 10-15 min; too late 40.9% vs Passio 11.3% at 15-20 min; too late 25.5% vs Passio 7.3% at 20-30 min |
| gbm_q15 | Friend Center/Metra | 504 | 30.5% / 16.0% (131) | 5.6% / 9.5% (126) | 6.1% / 7.8% (115) | 21.8% / 2.7% (110) | (0.0% / 0.0% (22)) | loses: band B 5.6% vs Passio 11.2% at 10-15 min |
| deep_q15 | Friend Center/Metra | 504 | 29.8% / 19.8% (131) | 14.4% / 11.1% (126) | 7.8% / 9.6% (115) | 21.8% / 3.6% (110) | (0.0% / 0.0% (22)) | loses: too late 19.8% vs Passio 16.0% at 0-10 min |
| deep_safe | Friend Center/Metra | 504 | 26.0% / 15.3% (131) | 12.0% / 9.5% (126) | 7.8% / 7.0% (115) | 24.5% / 5.5% (110) | (4.8% / 0.0% (22)) | holds |

### transition:service_end_early:5703 (medium, open)

Midway Metra; scope: hours=10-11;days=weekday;note=before Nov 6 44.737, from Nov 6 50.0 (3 episodes) (not applied: note=before Nov 6 44.737, from Nov 6 50.0 (3 episodes)); 7 samples. Flag: service days whose last bus left more than 15 min before the line's listed end, per 100 spans 45.455 (all lines 27.793).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Midway Metra | 7 | (0.0% / 0.0% (3)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) |  |  | reference |
| timetable_delay | Midway Metra | 7 | (0.0% / 0.0% (3)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) |  |  | too few rows |
| gbm_q15 | Midway Metra | 7 | (0.0% / 0.0% (3)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) |  |  | too few rows |
| deep_q15 | Midway Metra | 7 | (0.0% / 0.0% (3)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) |  |  | too few rows |
| deep_safe | Midway Metra | 7 | (0.0% / 0.0% (3)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) |  |  | too few rows |

### transition:timetable_add_missed:5703 (medium, open)

Midway Metra; scope: hours=8-10;days=weekday;note=before Nov 6 65.789, from Nov 6 50.0 (6 episodes) (not applied: note=before Nov 6 65.789, from Nov 6 50.0 (6 episodes)); 1,840 samples. Flag: timetable steps up (one more bus per hour) with no bus joining within 45 min, per 100 steps up 63.636 (all lines 42.174).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Midway Metra | 1,840 | 19.3% / 4.7% (705) | 3.4% / 0.0% (503) | 0.4% / 0.0% (367) | 0.0% / 0.0% (212) | 0.0% / 0.0% (53) | reference |
| timetable_delay | Midway Metra | 1,840 | 20.1% / 47.9% (705) | 12.8% / 33.6% (503) | 18.1% / 24.5% (367) | 7.5% / 18.4% (212) | 0.0% / 35.8% (53) | loses: too late 47.9% vs Passio 4.7% at 0-10 min; too late 33.6% vs Passio 0.0% at 10-15 min; too late 24.5% vs Passio 0.0% at 15-20 min; too late 18.4% vs Passio 0.0% at 20-30 min; too late 35.8% vs Passio 0.0% at 30-45 min |
| gbm_q15 | Midway Metra | 1,840 | 29.2% / 20.9% (705) | 8.8% / 2.8% (503) | 0.0% / 0.3% (367) | 0.0% / 0.0% (212) | 0.0% / 0.0% (53) | loses: too late 20.9% vs Passio 4.7% at 0-10 min; too late 2.8% vs Passio 0.0% at 10-15 min; band B 0.0% vs Passio 0.4% at 15-20 min |
| deep_q15 | Midway Metra | 1,840 | 29.8% / 19.7% (705) | 11.0% / 7.6% (503) | 4.8% / 0.5% (367) | 0.6% / 0.5% (212) | 0.0% / 0.0% (53) | loses: too late 19.7% vs Passio 4.7% at 0-10 min; too late 7.6% vs Passio 0.0% at 10-15 min |
| deep_safe | Midway Metra | 1,840 | 27.8% / 16.2% (705) | 7.6% / 6.2% (503) | 2.8% / 0.3% (367) | 1.9% / 0.0% (212) | 0.0% / 0.0% (53) | loses: too late 16.2% vs Passio 4.7% at 0-10 min; too late 6.2% vs Passio 0.0% at 10-15 min |

### transition:wrong_line_label:5703 (medium, open)

Midway Metra; scope: hours=19-20;days=weekday;note=before Nov 6 0.692, from Nov 6 0.705 (3 episodes), top spot 60th & Cottage Grove (4 of 18) (not applied: note=before Nov 6 0.692, from Nov 6 0.705 (3 episodes), top spot 60th & Cottage Grove (4 of 18)); 4 samples. Flag: bus labeled this line while it drove another line's road for 30 min or more, per 10 bus-hours inside transition windows (30 min around a bus count change, a shift change, a listed start or end, a timetable step) 0.694 (all lines 0.301).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Midway Metra | 4 | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) |  | reference |
| timetable_delay | Midway Metra | 4 | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) |  | too few rows |
| gbm_q15 | Midway Metra | 4 | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) |  | too few rows |
| deep_q15 | Midway Metra | 4 | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) |  | too few rows |
| deep_safe | Midway Metra | 4 | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) |  | too few rows |

### transition:joining_bus_no_predictions:1075 (medium, open)

North; scope: hours=16-17;stops=8579;note=before Nov 6 34.7, from Nov 6 63.6 (n 22), this line's other arrivals 17.4, top spot Reynolds Club (4 of 6) (not applied: note=before Nov 6 34.7, from Nov 6 63.6 (n 22), this line's other arrivals 17.4, top spot Reynolds Club (4 of 6)); 85 samples. Flag: share of a joining bus's arrivals in its first 30 min on the line with no Passio time (percent) 43.66 (all lines 26.97).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | North | 85 | (0.0% / 0.0% (22)) | (0.0% / 9.5% (21)) | (0.0% / 9.5% (21)) | (5.9% / 10.5% (19)) | (0.0% / 0.0% (2)) | reference |
| timetable_delay | North | 85 | (0.0% / 9.1% (22)) | (0.0% / 4.8% (21)) | (0.0% / 4.8% (21)) | (13.3% / 10.5% (19)) | (100.0% / 0.0% (2)) | too few rows |
| gbm_q15 | North | 85 | (0.0% / 0.0% (22)) | (0.0% / 9.5% (21)) | (0.0% / 9.5% (21)) | (0.0% / 10.5% (19)) | (0.0% / 0.0% (2)) | too few rows |
| deep_q15 | North | 85 | (0.0% / 0.0% (22)) | (0.0% / 9.5% (21)) | (0.0% / 9.5% (21)) | (5.3% / 10.5% (19)) | (0.0% / 0.0% (2)) | too few rows |
| deep_safe | North | 85 | (0.0% / 0.0% (22)) | (0.0% / 9.5% (21)) | (0.0% / 9.5% (21)) | (5.3% / 10.5% (19)) | (0.0% / 0.0% (2)) | too few rows |

### prediction_miss:stops_without_predictions:1075 (medium, open)

North; scope: stops=8633|8634|8635;lead=0-10;note=a time at any lead 1 to 30 min ahead 33%, before the last 14 days 58% of 718 arrivals had one 5 min ahead (not applied: note=a time at any lead 1 to 30 min ahead 33%, before the last 14 days 58% of 718 arrivals had one 5 min ahead); 172 samples. Flag: share of arrivals at the scope's stops with a Passio time on display 5 min ahead, last 14 service days 0.2087 (all lines 0.6594).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | North | 172 | 3.2% / 8.1% (172) |  |  |  |  | reference |
| timetable_delay | North | 172 | 11.7% / 53.5% (172) |  |  |  |  | loses: too late 53.5% vs Passio 8.1% at 0-10 min |
| gbm_q15 | North | 172 | 14.0% / 15.1% (172) |  |  |  |  | loses: too late 15.1% vs Passio 8.1% at 0-10 min |
| deep_q15 | North | 172 | 8.5% / 16.3% (172) |  |  |  |  | loses: too late 16.3% vs Passio 8.1% at 0-10 min |
| deep_safe | North | 172 | 8.9% / 12.2% (172) |  |  |  |  | loses: too late 12.2% vs Passio 8.1% at 0-10 min |

### transition:timetable_add_missed:1075 (medium, open)

North; scope: hours=21-22;note=before Nov 6 77.778, from Nov 6 100.0 (5 episodes) (not applied: note=before Nov 6 77.778, from Nov 6 100.0 (5 episodes)); 324 samples. Flag: timetable steps up (one more bus per hour) with no bus joining within 45 min, per 100 steps up 81.25 (all lines 42.174).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | North | 324 | 14.4% / 39.8% (103) | 18.4% / 34.5% (87) | 13.7% / 26.7% (75) | 31.1% / 40.8% (49) | (25.0% / 60.0% (10)) | reference |
| timetable_delay | North | 324 | 2.3% / 49.5% (103) | 0.0% / 47.1% (87) | 3.4% / 49.3% (75) | 25.8% / 49.0% (49) | (11.1% / 60.0% (10)) | loses: band B 2.3% vs Passio 14.4% at 0-10 min; too late 49.5% vs Passio 39.8% at 0-10 min; band B 0.0% vs Passio 18.4% at 10-15 min; too late 47.1% vs Passio 34.5% at 10-15 min; band B 3.4% vs Passio 13.7% at 15-20 min; too late 49.3% vs Passio 26.7% at 15-20 min; band B 25.8% vs Passio 31.1% at 20-30 min; too late 49.0% vs Passio 40.8% at 20-30 min |
| gbm_q15 | North | 324 | 13.9% / 19.4% (103) | 4.8% / 11.5% (87) | 12.5% / 12.0% (75) | 35.6% / 22.4% (49) | (87.5% / 0.0% (10)) | loses: band B 4.8% vs Passio 18.4% at 10-15 min |
| deep_q15 | North | 324 | 22.0% / 34.0% (103) | 13.3% / 19.5% (87) | 19.2% / 14.7% (75) | 37.8% / 20.4% (49) | (37.5% / 0.0% (10)) | loses: band B 13.3% vs Passio 18.4% at 10-15 min |
| deep_safe | North | 324 | 26.3% / 23.3% (103) | 13.6% / 16.1% (87) | 15.1% / 16.0% (75) | 37.8% / 22.4% (49) | (50.0% / 0.0% (10)) | loses: band B 13.6% vs Passio 18.4% at 10-15 min |

### prediction_miss:worse_when_behind:1075 (medium, open)

North; scope: lead=5-30;note=delay_s > 600 in the forecast table (not applied: note=delay_s > 600 in the forecast table); 2,102 samples. Flag: large-miss rate (goal leads) while the bus ran more than 10 min behind the timetable divided by the rate otherwise on the same line, all days 1.4803 (all lines 1.2148).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | North | 2,102 | 20.4% / 38.6% (381) | 21.5% / 30.6% (657) | 17.2% / 21.5% (604) | 27.2% / 19.8% (460) |  | reference |
| timetable_delay | North | 2,102 | 0.9% / 36.5% (381) | 0.5% / 33.2% (657) | 4.6% / 30.6% (604) | 23.2% / 38.9% (460) |  | loses: band B 0.9% vs Passio 20.4% at 0-10 min; band B 0.5% vs Passio 21.5% at 10-15 min; too late 33.2% vs Passio 30.6% at 10-15 min; band B 4.6% vs Passio 17.2% at 15-20 min; too late 30.6% vs Passio 21.5% at 15-20 min; band B 23.2% vs Passio 27.2% at 20-30 min; too late 38.9% vs Passio 19.8% at 20-30 min |
| gbm_q15 | North | 2,102 | 10.3% / 18.6% (381) | 10.8% / 14.5% (657) | 10.0% / 10.8% (604) | 30.7% / 10.7% (460) |  | loses: band B 10.3% vs Passio 20.4% at 0-10 min; band B 10.8% vs Passio 21.5% at 10-15 min; band B 10.0% vs Passio 17.2% at 15-20 min |
| deep_q15 | North | 2,102 | 25.1% / 35.7% (381) | 17.2% / 21.3% (657) | 14.1% / 15.7% (604) | 28.9% / 10.0% (460) |  | loses: band B 17.2% vs Passio 21.5% at 10-15 min; band B 14.1% vs Passio 17.2% at 15-20 min |
| deep_safe | North | 2,102 | 29.3% / 26.2% (381) | 17.6% / 19.8% (657) | 13.6% / 16.1% (604) | 29.6% / 13.0% (460) |  | loses: band B 17.6% vs Passio 21.5% at 10-15 min; band B 13.6% vs Passio 17.2% at 15-20 min |

### transition:extra_bus_added:5699 (medium, open)

Red Line/Arts Block; scope: hours=10-14;days=weekday;note=before Nov 6 50.0, from Nov 6 58.824 (10 episodes), top spot Logan Center (14 of 60) (not applied: note=before Nov 6 50.0, from Nov 6 58.824 (10 episodes), top spot Logan Center (14 of 60)); 1,445 samples. Flag: buses joining the line above its listed bus count (no timetable change), per 100 joins that are not a layover 51.282 (all lines 21.236).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Red Line/Arts Block | 1,445 | 6.9% / 18.2% (570) | 0.3% / 0.0% (371) | 0.0% / 0.0% (284) | 0.0% / 0.0% (204) | (0.0% / 0.0% (16)) | reference |
| timetable_delay | Red Line/Arts Block | 1,445 | 10.3% / 18.8% (570) | 8.5% / 18.6% (371) | 16.6% / 3.9% (284) | 8.3% / 2.0% (204) | (0.0% / 0.0% (16)) | loses: too late 18.6% vs Passio 0.0% at 10-15 min; too late 3.9% vs Passio 0.0% at 15-20 min; too late 2.0% vs Passio 0.0% at 20-30 min |
| gbm_q15 | Red Line/Arts Block | 1,445 | 28.6% / 22.3% (570) | 3.8% / 0.8% (371) | 0.0% / 0.0% (284) | 0.0% / 0.0% (204) | (0.0% / 0.0% (16)) | loses: too late 22.3% vs Passio 18.2% at 0-10 min |
| deep_q15 | Red Line/Arts Block | 1,445 | 29.2% / 20.2% (570) | 9.7% / 3.5% (371) | 3.3% / 0.7% (284) | 5.9% / 0.0% (204) | (0.0% / 0.0% (16)) | loses: too late 20.2% vs Passio 18.2% at 0-10 min; too late 3.5% vs Passio 0.0% at 10-15 min |
| deep_safe | Red Line/Arts Block | 1,445 | 26.9% / 16.7% (570) | 8.0% / 2.2% (371) | 3.5% / 0.0% (284) | 4.4% / 0.0% (204) | (0.0% / 0.0% (16)) | loses: too late 2.2% vs Passio 0.0% at 10-15 min |

### display:ghost_bus_on_map:5699 (medium, open)

Red Line/Arts Block; scope: hours=10-11|19-21;vehicles=4331|4315;note=2026-10-10 to 2026-11-10: 4.1 vs all lines 2.3 (not applied: note=2026-10-10 to 2026-11-10: 4.1 vs all lines 2.3); 206 samples. Flag: percent of map-badge minutes from a bus that logged no arrival on its line within 20 min before or after 4.2 (all lines 1.9).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Red Line/Arts Block | 206 | 8.1% / 20.2% (99) | 0.0% / 0.0% (47) | (0.0% / 0.0% (28)) | (0.0% / 0.0% (21)) | (0.0% / 0.0% (11)) | reference |
| timetable_delay | Red Line/Arts Block | 206 | 21.3% / 8.1% (99) | 0.0% / 6.4% (47) | (0.0% / 3.6% (28)) | (0.0% / 0.0% (21)) | (0.0% / 0.0% (11)) | loses: too late 6.4% vs Passio 0.0% at 10-15 min |
| gbm_q15 | Red Line/Arts Block | 206 | 27.3% / 24.2% (99) | 0.0% / 2.1% (47) | (0.0% / 0.0% (28)) | (0.0% / 0.0% (21)) | (0.0% / 0.0% (11)) | loses: too late 24.2% vs Passio 20.2% at 0-10 min; too late 2.1% vs Passio 0.0% at 10-15 min |
| deep_q15 | Red Line/Arts Block | 206 | 25.3% / 27.3% (99) | 17.8% / 8.5% (47) | (17.6% / 7.1% (28)) | (0.0% / 0.0% (21)) | (0.0% / 0.0% (11)) | loses: too late 27.3% vs Passio 20.2% at 0-10 min; too late 8.5% vs Passio 0.0% at 10-15 min |
| deep_safe | Red Line/Arts Block | 206 | 25.3% / 20.2% (99) | 14.0% / 2.1% (47) | (21.4% / 0.0% (28)) | (0.0% / 0.0% (21)) | (0.0% / 0.0% (11)) | loses: too late 2.1% vs Passio 0.0% at 10-15 min |

### display:ghost_times_after_leave:5699 (medium, open)

Red Line/Arts Block; scope: hours=10-12|19-22;vehicles=4331|4315;note=2026-10-10 to 2026-11-10: 6.6 vs all lines 4.6 (not applied: note=2026-10-10 to 2026-11-10: 6.6 vs all lines 4.6); 348 samples. Flag: percent of bus-minutes with times on display (1 to 30 min ahead) from a bus that then logged no arrival on the line until 15 min after its last displayed time (shipped rules) 6.5 (all lines 3.9).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Red Line/Arts Block | 348 | 8.8% / 24.6% (171) | 0.0% / 0.0% (79) | 0.0% / 0.0% (49) | 0.0% / 0.0% (35) | (0.0% / 0.0% (14)) | reference |
| timetable_delay | Red Line/Arts Block | 348 | 24.0% / 6.4% (171) | 1.9% / 6.3% (79) | 15.8% / 2.0% (49) | 33.3% / 0.0% (35) | (0.0% / 0.0% (14)) | loses: too late 6.3% vs Passio 0.0% at 10-15 min; too late 2.0% vs Passio 0.0% at 15-20 min |
| gbm_q15 | Red Line/Arts Block | 348 | 31.8% / 25.7% (171) | 0.0% / 1.3% (79) | 0.0% / 0.0% (49) | 0.0% / 0.0% (35) | (0.0% / 0.0% (14)) | loses: too late 25.7% vs Passio 24.6% at 0-10 min; too late 1.3% vs Passio 0.0% at 10-15 min |
| deep_q15 | Red Line/Arts Block | 348 | 25.3% / 25.7% (171) | 10.8% / 5.1% (79) | 9.1% / 4.1% (49) | 0.0% / 0.0% (35) | (0.0% / 0.0% (14)) | loses: too late 25.7% vs Passio 24.6% at 0-10 min; too late 5.1% vs Passio 0.0% at 10-15 min; too late 4.1% vs Passio 0.0% at 15-20 min |
| deep_safe | Red Line/Arts Block | 348 | 24.7% / 19.3% (171) | 8.3% / 1.3% (79) | 10.0% / 0.0% (49) | 0.0% / 0.0% (35) | (0.0% / 0.0% (14)) | loses: too late 1.3% vs Passio 0.0% at 10-15 min |

### transition:after_hours:5715 (medium, open)

Regents Express; scope: vehicles=12648;hours=21-22;days=weekday;note=before Nov 6 6.313, from Nov 6 4.243 (5 episodes), top spot Operator garage (5 of 25) (not applied: note=before Nov 6 6.313, from Nov 6 4.243 (5 episodes), top spot Operator garage (5 of 25)); 6 samples. Flag: bus reporting under the line's label more than 15 min after (30 min before) its listed hours, per 10 bus-hours inside transition windows (30 min around a bus count change, a shift change, a listed start or end, a timetable step) 5.97 (all lines 0.491).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Regents Express | 6 | (0.0% / 50.0% (2)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (2)) |  | reference |
| timetable_delay | Regents Express | 6 | (0.0% / 50.0% (2)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (2)) |  | too few rows |
| gbm_q15 | Regents Express | 6 | (0.0% / 50.0% (2)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (2)) |  | too few rows |
| deep_q15 | Regents Express | 6 | (100.0% / 0.0% (2)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (2)) |  | too few rows |
| deep_safe | Regents Express | 6 | (100.0% / 0.0% (2)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (2)) |  | too few rows |

### prediction_miss:stops_without_predictions:5715 (medium, open)

Regents Express; scope: stops=8643;lead=0-10;note=a time at any lead 1 to 30 min ahead 36%, before the last 14 days 67% of 36 arrivals had one 5 min ahead (not applied: note=a time at any lead 1 to 30 min ahead 36%, before the last 14 days 67% of 36 arrivals had one 5 min ahead); 7 samples. Flag: share of arrivals at the scope's stops with a Passio time on display 5 min ahead, last 14 service days 0.1515 (all lines 0.6594).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Regents Express | 7 | (0.0% / 0.0% (7)) |  |  |  |  | reference |
| timetable_delay | Regents Express | 7 | (0.0% / 14.3% (7)) |  |  |  |  | too few rows |
| gbm_q15 | Regents Express | 7 | (0.0% / 0.0% (7)) |  |  |  |  | too few rows |
| deep_q15 | Regents Express | 7 | (0.0% / 0.0% (7)) |  |  |  |  | too few rows |
| deep_safe | Regents Express | 7 | (0.0% / 0.0% (7)) |  |  |  |  | too few rows |

### transition:off_route_drive:1076 (medium, open)

South; scope: hours=22-1;note=before Nov 6 6.566, from Nov 6 2.826 (4 episodes), top spot Regents Park Apartments (11 of 54) (not applied: note=before Nov 6 6.566, from Nov 6 2.826 (4 episodes), top spot Regents Park Apartments (11 of 54)); 1,185 samples. Flag: bus more than 250 m from its line and its learned corridor (45 s, 2 reports) inside its listed hours, per 10 bus-hours inside transition windows (30 min around a bus count change, a shift change, a listed start or end, a timetable step) 6.149 (all lines 3.487).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | South | 1,185 | 17.7% / 47.1% (444) | 18.5% / 25.2% (290) | 17.1% / 12.8% (227) | 28.1% / 13.1% (191) | 46.7% / 0.0% (33) | reference |
| timetable_delay | South | 1,185 | 7.7% / 68.0% (444) | 6.9% / 43.4% (290) | 6.9% / 30.0% (227) | 26.4% / 27.2% (191) | 18.2% / 36.4% (33) | loses: band B 7.7% vs Passio 17.7% at 0-10 min; too late 68.0% vs Passio 47.1% at 0-10 min; band B 6.9% vs Passio 18.5% at 10-15 min; too late 43.4% vs Passio 25.2% at 10-15 min; band B 6.9% vs Passio 17.1% at 15-20 min; too late 30.0% vs Passio 12.8% at 15-20 min; too late 27.2% vs Passio 13.1% at 20-30 min; band B 18.2% vs Passio 46.7% at 30-45 min; too late 36.4% vs Passio 0.0% at 30-45 min |
| gbm_q15 | South | 1,185 | 23.0% / 24.3% (444) | 6.8% / 14.1% (290) | 15.1% / 3.5% (227) | 19.8% / 6.8% (191) | 7.1% / 0.0% (33) | loses: band B 6.8% vs Passio 18.5% at 10-15 min; band B 15.1% vs Passio 17.1% at 15-20 min; band B 19.8% vs Passio 28.1% at 20-30 min; band B 7.1% vs Passio 46.7% at 30-45 min |
| deep_q15 | South | 1,185 | 23.7% / 23.6% (444) | 11.0% / 16.9% (290) | 11.8% / 11.9% (227) | 21.6% / 14.1% (191) | 0.0% / 0.0% (33) | loses: band B 11.0% vs Passio 18.5% at 10-15 min; band B 11.8% vs Passio 17.1% at 15-20 min; band B 21.6% vs Passio 28.1% at 20-30 min; too late 14.1% vs Passio 13.1% at 20-30 min; band B 0.0% vs Passio 46.7% at 30-45 min |
| deep_safe | South | 1,185 | 17.9% / 19.4% (444) | 9.2% / 16.6% (290) | 10.4% / 11.0% (227) | 18.2% / 15.2% (191) | 0.0% / 0.0% (33) | loses: band B 9.2% vs Passio 18.5% at 10-15 min; band B 10.4% vs Passio 17.1% at 15-20 min; band B 18.2% vs Passio 28.1% at 20-30 min; too late 15.2% vs Passio 13.1% at 20-30 min; band B 0.0% vs Passio 46.7% at 30-45 min |

### display:planner_recommends_leaving_bus:1076 (medium, open)

South; scope: hours=17-24;note=after the rules shipped (2026-11-06 to 2026-11-10): 9.2 vs all lines 5.7, 195 events (not applied: note=after the rules shipped (2026-11-06 to 2026-11-10): 9.2 vs all lines 5.7, 195 events); 4,758 samples. Flag: percent of the planner's live bus legs (sampled stop pairs every 5 min, core/planner.js plan()) whose bus never boarded on the line or logged no arrival near the rider's stop (left the line first) 10.8 (all lines 7.1).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | South | 4,758 | 20.1% / 41.5% (1,565) | 19.3% / 21.8% (1,137) | 21.1% / 8.4% (964) | 38.7% / 6.8% (842) | 28.0% / 0.0% (250) | reference |
| timetable_delay | South | 4,758 | 6.2% / 63.8% (1,565) | 6.1% / 37.6% (1,137) | 8.8% / 21.0% (964) | 29.2% / 15.7% (842) | 23.8% / 11.6% (250) | loses: band B 6.2% vs Passio 20.1% at 0-10 min; too late 63.8% vs Passio 41.5% at 0-10 min; band B 6.1% vs Passio 19.3% at 10-15 min; too late 37.6% vs Passio 21.8% at 10-15 min; band B 8.8% vs Passio 21.1% at 15-20 min; too late 21.0% vs Passio 8.4% at 15-20 min; band B 29.2% vs Passio 38.7% at 20-30 min; too late 15.7% vs Passio 6.8% at 20-30 min; band B 23.8% vs Passio 28.0% at 30-45 min; too late 11.6% vs Passio 0.0% at 30-45 min |
| gbm_q15 | South | 4,758 | 31.5% / 22.7% (1,565) | 12.1% / 9.1% (1,137) | 12.0% / 2.1% (964) | 31.6% / 2.3% (842) | 9.6% / 0.0% (250) | loses: band B 12.1% vs Passio 19.3% at 10-15 min; band B 12.0% vs Passio 21.1% at 15-20 min; band B 31.6% vs Passio 38.7% at 20-30 min; band B 9.6% vs Passio 28.0% at 30-45 min |
| deep_q15 | South | 4,758 | 32.7% / 23.0% (1,565) | 17.4% / 10.1% (1,137) | 15.4% / 6.0% (964) | 39.0% / 5.1% (842) | 8.3% / 0.0% (250) | loses: band B 15.4% vs Passio 21.1% at 15-20 min; band B 8.3% vs Passio 28.0% at 30-45 min |
| deep_safe | South | 4,758 | 26.7% / 17.6% (1,565) | 16.5% / 9.4% (1,137) | 16.2% / 5.3% (964) | 39.1% / 6.5% (842) | 9.4% / 0.0% (250) | loses: band B 16.5% vs Passio 19.3% at 10-15 min; band B 16.2% vs Passio 21.1% at 15-20 min; band B 9.4% vs Passio 28.0% at 30-45 min |

### transition:linger_not_in_service:5716 (medium, open)

South Loop Shuttle; scope: stops=8579;note=before Nov 6 8.335, from Nov 6 5.195 (1 episodes), top spot Reynolds Club (6 of 13) (not applied: note=before Nov 6 8.335, from Nov 6 5.195 (1 episodes), top spot Reynolds Club (6 of 13)); 47 samples. Flag: bus still for 5 min or more on the map but not in service (E28 break, end of shift, garage return, never served), per 10 bus-hours inside transition windows (30 min around a bus count change, a shift change, a listed start or end, a timetable step) 7.672 (all lines 2.528).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | South Loop Shuttle | 47 | (25.0% / 33.3% (6)) | (50.0% / 20.0% (10)) | (0.0% / 54.5% (11)) | (0.0% / 60.0% (10)) | (42.9% / 60.0% (10)) | reference |
| timetable_delay | South Loop Shuttle | 47 | (0.0% / 50.0% (6)) | (10.0% / 60.0% (10)) | (11.1% / 72.7% (11)) | (25.0% / 30.0% (10)) | (0.0% / 40.0% (10)) | too few rows |
| gbm_q15 | South Loop Shuttle | 47 | (0.0% / 33.3% (6)) | (0.0% / 20.0% (10)) | (0.0% / 54.5% (11)) | (20.0% / 40.0% (10)) | (16.7% / 50.0% (10)) | too few rows |
| deep_q15 | South Loop Shuttle | 47 | (0.0% / 50.0% (6)) | (22.2% / 20.0% (10)) | (0.0% / 54.5% (11)) | (12.5% / 40.0% (10)) | (14.3% / 0.0% (10)) | too few rows |
| deep_safe | South Loop Shuttle | 47 | (0.0% / 50.0% (6)) | (22.2% / 30.0% (10)) | (0.0% / 54.5% (11)) | (0.0% / 50.0% (10)) | (28.6% / 10.0% (10)) | too few rows |

### transition:off_route_drive:5716 (medium, open)

South Loop Shuttle; scope: vehicles=4538;hours=22-2;note=before Nov 6 9.724, from Nov 6 10.39 (2 episodes), top spot Operator garage (7 of 19) (not applied: note=before Nov 6 9.724, from Nov 6 10.39 (2 episodes), top spot Operator garage (7 of 19)); 17 samples. Flag: bus more than 250 m from its line and its learned corridor (45 s, 2 reports) inside its listed hours, per 10 bus-hours inside transition windows (30 min around a bus count change, a shift change, a listed start or end, a timetable step) 9.864 (all lines 3.487).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | South Loop Shuttle | 17 | (0.0% / 100.0% (2)) | (0.0% / 66.7% (3)) | (0.0% / 33.3% (3)) | (25.0% / 50.0% (4)) | (40.0% / 40.0% (5)) | reference |
| timetable_delay | South Loop Shuttle | 17 | (0.0% / 50.0% (2)) | (50.0% / 33.3% (3)) | (66.7% / 0.0% (3)) | (66.7% / 25.0% (4)) | (0.0% / 40.0% (5)) | too few rows |
| gbm_q15 | South Loop Shuttle | 17 | (0.0% / 100.0% (2)) | (0.0% / 66.7% (3)) | (0.0% / 33.3% (3)) | (0.0% / 50.0% (4)) | (20.0% / 20.0% (5)) | too few rows |
| deep_q15 | South Loop Shuttle | 17 | (0.0% / 100.0% (2)) | (0.0% / 66.7% (3)) | (0.0% / 33.3% (3)) | (25.0% / 0.0% (4)) | (0.0% / 0.0% (5)) | too few rows |
| deep_safe | South Loop Shuttle | 17 | (0.0% / 100.0% (2)) | (0.0% / 66.7% (3)) | (0.0% / 33.3% (3)) | (0.0% / 25.0% (4)) | (50.0% / 0.0% (5)) | too few rows |

### display:planner_recommends_leaving_bus:5716 (medium, open)

South Loop Shuttle; scope: hours=00-01|18-24;vehicles=4324|4327;note=after the rules shipped (2026-11-06 to 2026-11-10): 1.6 vs all lines 5.7, 3 events (not applied: note=after the rules shipped (2026-11-06 to 2026-11-10): 1.6 vs all lines 5.7, 3 events); 61 samples. Flag: percent of the planner's live bus legs (sampled stop pairs every 5 min, core/planner.js plan()) whose bus never boarded on the line or logged no arrival near the rider's stop (left the line first) 14.5 (all lines 7.1).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | South Loop Shuttle | 61 | (0.0% / 84.6% (13)) | (0.0% / 60.0% (10)) | (0.0% / 58.3% (12)) | (33.3% / 61.5% (13)) | (40.0% / 38.5% (13)) | reference |
| timetable_delay | South Loop Shuttle | 61 | (0.0% / 53.8% (13)) | (0.0% / 60.0% (10)) | (0.0% / 50.0% (12)) | (0.0% / 30.8% (13)) | (12.5% / 30.8% (13)) | too few rows |
| gbm_q15 | South Loop Shuttle | 61 | (0.0% / 84.6% (13)) | (0.0% / 60.0% (10)) | (0.0% / 58.3% (12)) | (0.0% / 53.8% (13)) | (0.0% / 38.5% (13)) | too few rows |
| deep_q15 | South Loop Shuttle | 61 | (20.0% / 76.9% (13)) | (0.0% / 60.0% (10)) | (0.0% / 58.3% (12)) | (9.1% / 38.5% (13)) | (7.7% / 7.7% (13)) | too few rows |
| deep_safe | South Loop Shuttle | 61 | (0.0% / 76.9% (13)) | (0.0% / 60.0% (10)) | (0.0% / 58.3% (12)) | (20.0% / 46.2% (13)) | (0.0% / 15.4% (13)) | too few rows |

### display:false_hide_idle_serving_bus:1078 (low, watch)

Central; scope: hours=20-22;stops=8579;note=after the rules shipped (2026-11-06 to 2026-11-10): None vs all lines 37.0, 0 events (not applied: note=after the rules shipped (2026-11-06 to 2026-11-10): None vs all lines 37.0, 0 events); 116 samples. Flag: percent of minutes core/idle.js hid a still bus that then logged an arrival on the line within 15 min 36.3 (all lines 23.6).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Central | 116 | 5.0% / 7.3% (41) | 2.7% / 2.6% (38) | (0.0% / 3.8% (26)) | (10.0% / 0.0% (10)) | (0.0% / 0.0% (1)) | reference |
| timetable_delay | Central | 116 | 0.0% / 2.4% (41) | 0.0% / 0.0% (38) | (0.0% / 3.8% (26)) | (33.3% / 40.0% (10)) | (0.0% / 0.0% (1)) | loses: band B 0.0% vs Passio 5.0% at 0-10 min; band B 0.0% vs Passio 2.7% at 10-15 min |
| gbm_q15 | Central | 116 | 12.2% / 4.9% (41) | 2.6% / 0.0% (38) | (0.0% / 0.0% (26)) | (0.0% / 0.0% (10)) | (0.0% / 0.0% (1)) | holds |
| deep_q15 | Central | 116 | 12.2% / 4.9% (41) | 23.7% / 10.5% (38) | (19.2% / 3.8% (26)) | (0.0% / 0.0% (10)) | (0.0% / 0.0% (1)) | loses: too late 10.5% vs Passio 2.6% at 10-15 min |
| deep_safe | Central | 116 | 12.2% / 4.9% (41) | 18.4% / 15.8% (38) | (15.4% / 7.7% (26)) | (0.0% / 0.0% (10)) | (0.0% / 0.0% (1)) | loses: too late 15.8% vs Passio 2.6% at 10-15 min |

### display:ghost_bus_on_map:5704 (low, watch)

Downtown Campus Connector; scope: note=after the rules shipped (2026-11-06 to 2026-11-10): 3.0 vs all lines 1.9, 387 events (not applied: note=after the rules shipped (2026-11-06 to 2026-11-10): 3.0 vs all lines 1.9, 387 events); 9,308 samples. Flag: percent of map-badge minutes from a bus that logged no arrival on its line within 20 min before or after 3.9 (all lines 2.3).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Downtown Campus Connector | 9,308 | 4.8% / 37.5% (1,661) | 9.8% / 27.2% (1,858) | 11.9% / 20.4% (1,940) | 14.5% / 5.6% (1,942) | 5.7% / 2.0% (1,907) | reference |
| timetable_delay | Downtown Campus Connector | 9,308 | 4.8% / 37.5% (1,661) | 9.8% / 27.2% (1,858) | 11.9% / 20.4% (1,940) | 14.5% / 5.6% (1,942) | 5.7% / 2.0% (1,907) | holds |
| gbm_q15 | Downtown Campus Connector | 9,308 | 17.5% / 26.6% (1,661) | 16.3% / 22.9% (1,858) | 14.5% / 13.6% (1,940) | 13.7% / 4.9% (1,942) | 6.1% / 2.4% (1,907) | holds |
| deep_q15 | Downtown Campus Connector | 9,308 | 19.8% / 19.4% (1,661) | 17.7% / 15.6% (1,858) | 14.0% / 12.7% (1,940) | 18.3% / 6.7% (1,942) | 9.1% / 1.3% (1,907) | loses: too late 6.7% vs Passio 5.6% at 20-30 min |
| deep_safe | Downtown Campus Connector | 9,308 | 17.6% / 17.2% (1,661) | 18.3% / 15.3% (1,858) | 13.7% / 13.5% (1,940) | 17.2% / 8.3% (1,942) | 10.4% / 2.9% (1,907) | loses: too late 8.3% vs Passio 5.6% at 20-30 min |

### display:ghost_bus_on_map:5701 (low, watch)

Drexel; scope: hours=09-11;vehicles=4324;note=2026-10-10 to 2026-11-10: 0.5 vs all lines 2.3 (not applied: note=2026-10-10 to 2026-11-10: 0.5 vs all lines 2.3); 38 samples. Flag: percent of map-badge minutes from a bus that logged no arrival on its line within 20 min before or after 3.0 (all lines 1.9).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Drexel | 38 | (0.0% / 0.0% (14)) | (0.0% / 0.0% (8)) | (0.0% / 0.0% (10)) | (0.0% / 0.0% (5)) | (0.0% / 0.0% (1)) | reference |
| timetable_delay | Drexel | 38 | (50.0% / 35.7% (14)) | (0.0% / 25.0% (8)) | (0.0% / 30.0% (10)) | (0.0% / 40.0% (5)) | (0.0% / 0.0% (1)) | too few rows |
| gbm_q15 | Drexel | 38 | (9.1% / 0.0% (14)) | (0.0% / 0.0% (8)) | (0.0% / 0.0% (10)) | (0.0% / 0.0% (5)) | (0.0% / 0.0% (1)) | too few rows |
| deep_q15 | Drexel | 38 | (0.0% / 0.0% (14)) | (0.0% / 0.0% (8)) | (0.0% / 0.0% (10)) | (0.0% / 0.0% (5)) | (0.0% / 0.0% (1)) | too few rows |
| deep_safe | Drexel | 38 | (9.1% / 0.0% (14)) | (0.0% / 0.0% (8)) | (0.0% / 0.0% (10)) | (0.0% / 0.0% (5)) | (0.0% / 0.0% (1)) | too few rows |

### prediction_miss:large_late_miss:5701 (low, watch)

Drexel; scope: lead=5-45;stops=8611;note=last 14 days 62.9%, before them 49.4% (worse) (not applied: note=last 14 days 62.9%, before them 49.4% (worse)); 391 samples. Flag: share of Passio's times 5 to 30 min ahead that the bus came later than by more than the large-miss threshold (2 min at 5 to 15 min ahead, 4 at 20, 5 at 30), last 14 service days 0.6287 (all lines 0.5529).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Drexel | 391 | 0.0% / 0.0% (70) | 0.0% / 0.0% (141) | 0.0% / 0.0% (107) | 0.0% / 0.0% (36) | 0.0% / 0.0% (37) | reference |
| timetable_delay | Drexel | 391 | 9.1% / 11.4% (70) | 4.5% / 12.1% (141) | 35.2% / 33.6% (107) | 16.7% / 5.6% (36) | 3.4% / 2.7% (37) | loses: too late 11.4% vs Passio 0.0% at 0-10 min; too late 12.1% vs Passio 0.0% at 10-15 min; too late 33.6% vs Passio 0.0% at 15-20 min; too late 5.6% vs Passio 0.0% at 20-30 min; too late 2.7% vs Passio 0.0% at 30-45 min |
| gbm_q15 | Drexel | 391 | 1.5% / 0.0% (70) | 0.0% / 0.0% (141) | 0.0% / 0.0% (107) | 0.0% / 0.0% (36) | 0.0% / 0.0% (37) | holds |
| deep_q15 | Drexel | 391 | 1.4% / 0.0% (70) | 0.0% / 0.0% (141) | 0.0% / 0.0% (107) | 0.0% / 0.0% (36) | 0.0% / 0.0% (37) | holds |
| deep_safe | Drexel | 391 | 0.0% / 0.0% (70) | 0.0% / 0.0% (141) | 0.0% / 0.0% (107) | 0.0% / 0.0% (36) | 0.0% / 0.0% (37) | holds |

### prediction_miss:other_trip_times:5701 (low, watch)

Drexel; scope: stops=8609;lead=0-10;note=stop positions 6, 19 of 50 times the bus came later than shown (not applied: note=stop positions 6, 19 of 50 times the bus came later than shown); 131 samples. Flag: share of the times a screen showed only under another trip id of the same bus 5 min ahead (no own-trip time) that were large misses (more than 2 min either way), last 14 service days 0.4000 (all lines 0.5822).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Drexel | 131 | 28.8% / 6.9% (131) |  |  |  |  | reference |
| timetable_delay | Drexel | 131 | 8.3% / 74.0% (131) |  |  |  |  | loses: band B 8.3% vs Passio 28.8% at 0-10 min; too late 74.0% vs Passio 6.9% at 0-10 min |
| gbm_q15 | Drexel | 131 | 44.4% / 24.4% (131) |  |  |  |  | loses: too late 24.4% vs Passio 6.9% at 0-10 min |
| deep_q15 | Drexel | 131 | 47.6% / 16.8% (131) |  |  |  |  | loses: too late 16.8% vs Passio 6.9% at 0-10 min |
| deep_safe | Drexel | 131 | 41.3% / 10.7% (131) |  |  |  |  | loses: too late 10.7% vs Passio 6.9% at 0-10 min |

### transition:staying_bus_late_after_drop:5701 (low, watch)

Drexel; scope: hours=9-10;days=weekday;note=staying bus 8.8 min vs 5.2 min at other times, 44 times from 19 drops, late by 3 min or more 88.6 vs 45.1 percent, top spot Midway Plaisance & Cottage Grove (1 of 4) (not applied: note=staying bus 8.8 min vs 5.2 min at other times, 44 times from 19 drops, late by 3 min or more 88.6 vs 45.1 percent, top spot Midway Plaisance & Cottage Grove (1 of 4)); 402 samples. Flag: mean absolute error of the staying bus's Passio times 10 to 20 min ahead in the 45 min after a 2-to-1 drop, divided by the line's at other times 1.688 (all lines 0.956).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Drexel | 402 | 19.5% / 7.0% (201) | 12.9% / 3.1% (96) | 10.2% / 5.1% (78) | (8.3% / 0.0% (24)) | (0.0% / 0.0% (3)) | reference |
| timetable_delay | Drexel | 402 | 10.8% / 65.7% (201) | 20.5% / 32.3% (96) | 32.9% / 37.2% (78) | (29.4% / 8.3% (24)) | (0.0% / 0.0% (3)) | loses: band B 10.8% vs Passio 19.5% at 0-10 min; too late 65.7% vs Passio 7.0% at 0-10 min; too late 32.3% vs Passio 3.1% at 10-15 min; too late 37.2% vs Passio 5.1% at 15-20 min |
| gbm_q15 | Drexel | 402 | 30.5% / 11.9% (201) | 15.4% / 3.1% (96) | 9.8% / 2.6% (78) | (0.0% / 0.0% (24)) | (0.0% / 0.0% (3)) | loses: too late 11.9% vs Passio 7.0% at 0-10 min |
| deep_q15 | Drexel | 402 | 27.2% / 13.4% (201) | 12.7% / 5.2% (96) | 12.9% / 5.1% (78) | (7.1% / 0.0% (24)) | (0.0% / 0.0% (3)) | loses: too late 13.4% vs Passio 7.0% at 0-10 min; too late 5.2% vs Passio 3.1% at 10-15 min |
| deep_safe | Drexel | 402 | 26.0% / 11.4% (201) | 14.9% / 6.2% (96) | 10.2% / 5.1% (78) | (7.1% / 0.0% (24)) | (0.0% / 0.0% (3)) | loses: too late 11.4% vs Passio 7.0% at 0-10 min; too late 6.2% vs Passio 3.1% at 10-15 min |

### transition:unscheduled_leave:5701 (low, watch)

Drexel; scope: hours=9-10;days=weekday;note=before Nov 6 85.0, from Nov 6 100.0 (3 episodes), top spot Burton-Judson Courts (NE Corner) (6 of 20) (not applied: note=before Nov 6 85.0, from Nov 6 100.0 (3 episodes), top spot Burton-Judson Courts (NE Corner) (6 of 20)); 402 samples. Flag: lasting leaves the timetable does not have that leave the line below its listed bus count for 15 min, per 100 lasting leaves 86.957 (all lines 51.913).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Drexel | 402 | 19.5% / 7.0% (201) | 12.9% / 3.1% (96) | 10.2% / 5.1% (78) | (8.3% / 0.0% (24)) | (0.0% / 0.0% (3)) | reference |
| timetable_delay | Drexel | 402 | 10.8% / 65.7% (201) | 20.5% / 32.3% (96) | 32.9% / 37.2% (78) | (29.4% / 8.3% (24)) | (0.0% / 0.0% (3)) | loses: band B 10.8% vs Passio 19.5% at 0-10 min; too late 65.7% vs Passio 7.0% at 0-10 min; too late 32.3% vs Passio 3.1% at 10-15 min; too late 37.2% vs Passio 5.1% at 15-20 min |
| gbm_q15 | Drexel | 402 | 30.5% / 11.9% (201) | 15.4% / 3.1% (96) | 9.8% / 2.6% (78) | (0.0% / 0.0% (24)) | (0.0% / 0.0% (3)) | loses: too late 11.9% vs Passio 7.0% at 0-10 min |
| deep_q15 | Drexel | 402 | 27.2% / 13.4% (201) | 12.7% / 5.2% (96) | 12.9% / 5.1% (78) | (7.1% / 0.0% (24)) | (0.0% / 0.0% (3)) | loses: too late 13.4% vs Passio 7.0% at 0-10 min; too late 5.2% vs Passio 3.1% at 10-15 min |
| deep_safe | Drexel | 402 | 26.0% / 11.4% (201) | 14.9% / 6.2% (96) | 10.2% / 5.1% (78) | (7.1% / 0.0% (24)) | (0.0% / 0.0% (3)) | loses: too late 11.4% vs Passio 7.0% at 0-10 min; too late 6.2% vs Passio 3.1% at 10-15 min |

### prediction_miss:worse_near_transitions:5700 (low, watch)

Friend Center/Metra; scope: lead=5-30;note=transitions = data/labeled/transitions/transitions.csv (E29) (not applied: note=transitions = data/labeled/transitions/transitions.csv (E29)); 6,764 samples. Flag: large-miss rate (goal leads) within 30 min of a change in the line's bus count divided by the rate otherwise on the same line, all days 1.1971 (all lines 1.1718).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Friend Center/Metra | 6,764 | 23.4% / 25.7% (1,056) | 18.2% / 25.3% (1,949) | 18.7% / 24.7% (1,905) | 35.0% / 23.1% (1,854) |  | reference |
| timetable_delay | Friend Center/Metra | 6,764 | 5.2% / 62.4% (1,056) | 7.9% / 42.9% (1,949) | 13.0% / 36.5% (1,905) | 27.8% / 35.8% (1,854) |  | loses: band B 5.2% vs Passio 23.4% at 0-10 min; too late 62.4% vs Passio 25.7% at 0-10 min; band B 7.9% vs Passio 18.2% at 10-15 min; too late 42.9% vs Passio 25.3% at 10-15 min; band B 13.0% vs Passio 18.7% at 15-20 min; too late 36.5% vs Passio 24.7% at 15-20 min; band B 27.8% vs Passio 35.0% at 20-30 min; too late 35.8% vs Passio 23.1% at 20-30 min |
| gbm_q15 | Friend Center/Metra | 6,764 | 26.2% / 28.4% (1,056) | 15.8% / 21.2% (1,949) | 13.3% / 20.2% (1,905) | 39.0% / 16.1% (1,854) |  | loses: too late 28.4% vs Passio 25.7% at 0-10 min; band B 15.8% vs Passio 18.2% at 10-15 min; band B 13.3% vs Passio 18.7% at 15-20 min |
| deep_q15 | Friend Center/Metra | 6,764 | 30.0% / 28.7% (1,056) | 20.5% / 22.6% (1,949) | 20.7% / 19.5% (1,905) | 38.6% / 14.8% (1,854) |  | loses: too late 28.7% vs Passio 25.7% at 0-10 min |
| deep_safe | Friend Center/Metra | 6,764 | 28.1% / 23.4% (1,056) | 19.1% / 22.0% (1,949) | 19.5% / 19.7% (1,905) | 38.2% / 18.7% (1,854) |  | holds |

### prediction_miss:worse_when_behind:5700 (low, watch)

Friend Center/Metra; scope: lead=5-30;note=delay_s > 600 in the forecast table (not applied: note=delay_s > 600 in the forecast table); 6,764 samples. Flag: large-miss rate (goal leads) while the bus ran more than 10 min behind the timetable divided by the rate otherwise on the same line, all days 1.2317 (all lines 1.2148).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Friend Center/Metra | 6,764 | 23.4% / 25.7% (1,056) | 18.2% / 25.3% (1,949) | 18.7% / 24.7% (1,905) | 35.0% / 23.1% (1,854) |  | reference |
| timetable_delay | Friend Center/Metra | 6,764 | 5.2% / 62.4% (1,056) | 7.9% / 42.9% (1,949) | 13.0% / 36.5% (1,905) | 27.8% / 35.8% (1,854) |  | loses: band B 5.2% vs Passio 23.4% at 0-10 min; too late 62.4% vs Passio 25.7% at 0-10 min; band B 7.9% vs Passio 18.2% at 10-15 min; too late 42.9% vs Passio 25.3% at 10-15 min; band B 13.0% vs Passio 18.7% at 15-20 min; too late 36.5% vs Passio 24.7% at 15-20 min; band B 27.8% vs Passio 35.0% at 20-30 min; too late 35.8% vs Passio 23.1% at 20-30 min |
| gbm_q15 | Friend Center/Metra | 6,764 | 26.2% / 28.4% (1,056) | 15.8% / 21.2% (1,949) | 13.3% / 20.2% (1,905) | 39.0% / 16.1% (1,854) |  | loses: too late 28.4% vs Passio 25.7% at 0-10 min; band B 15.8% vs Passio 18.2% at 10-15 min; band B 13.3% vs Passio 18.7% at 15-20 min |
| deep_q15 | Friend Center/Metra | 6,764 | 30.0% / 28.7% (1,056) | 20.5% / 22.6% (1,949) | 20.7% / 19.5% (1,905) | 38.6% / 14.8% (1,854) |  | loses: too late 28.7% vs Passio 25.7% at 0-10 min |
| deep_safe | Friend Center/Metra | 6,764 | 28.1% / 23.4% (1,056) | 19.1% / 22.0% (1,949) | 19.5% / 19.7% (1,905) | 38.2% / 18.7% (1,854) |  | holds |

### display:false_hide_gone_serving_bus:5703 (low, watch)

Midway Metra; scope: hours=10-11|18-20;vehicles=12646|12648;stops=8655;note=after the rules shipped (2026-11-06 to 2026-11-10): 65.4 vs all lines 9.9, 17 events (not applied: note=after the rules shipped (2026-11-06 to 2026-11-10): 65.4 vs all lines 9.9, 17 events); 18 samples. Flag: percent of minutes core/transition.js GONE dropped a bus's times (no report for 15 min) and the bus then logged an arrival on the line within 15 min 48.0 (all lines 16.3).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Midway Metra | 18 | (16.7% / 0.0% (6)) | (16.7% / 0.0% (6)) | (16.7% / 0.0% (6)) |  |  | reference |
| timetable_delay | Midway Metra | 18 | (0.0% / 100.0% (6)) | (0.0% / 33.3% (6)) | (83.3% / 16.7% (6)) |  |  | too few rows |
| gbm_q15 | Midway Metra | 18 | (66.7% / 16.7% (6)) | (33.3% / 0.0% (6)) | (50.0% / 0.0% (6)) |  |  | too few rows |
| deep_q15 | Midway Metra | 18 | (50.0% / 16.7% (6)) | (33.3% / 0.0% (6)) | (33.3% / 0.0% (6)) |  |  | too few rows |
| deep_safe | Midway Metra | 18 | (50.0% / 16.7% (6)) | (33.3% / 0.0% (6)) | (16.7% / 16.7% (6)) |  |  | too few rows |

### prediction_miss:large_late_miss:5703 (low, watch)

Midway Metra; scope: lead=10-45;note=last 14 days 63.4%, before them 69.9% (same) (not applied: note=last 14 days 63.4%, before them 69.9% (same)); 4,985 samples. Flag: share of Passio's times 5 to 30 min ahead that the bus came later than by more than the large-miss threshold (2 min at 5 to 15 min ahead, 4 at 20, 5 at 30), last 14 service days 0.6341 (all lines 0.5529).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Midway Metra | 4,985 |  | 5.9% / 5.2% (2,306) | 4.9% / 3.7% (1,803) | 4.8% / 0.0% (695) | 0.0% / 0.0% (181) | reference |
| timetable_delay | Midway Metra | 4,985 |  | 17.0% / 43.5% (2,306) | 23.1% / 40.3% (1,803) | 17.2% / 24.6% (695) | 4.3% / 24.9% (181) | loses: too late 43.5% vs Passio 5.2% at 10-15 min; too late 40.3% vs Passio 3.7% at 15-20 min; too late 24.6% vs Passio 0.0% at 20-30 min; too late 24.9% vs Passio 0.0% at 30-45 min |
| gbm_q15 | Midway Metra | 4,985 |  | 15.9% / 8.7% (2,306) | 12.4% / 3.9% (1,803) | 2.0% / 0.0% (695) | 0.0% / 0.0% (181) | loses: too late 8.7% vs Passio 5.2% at 10-15 min; band B 2.0% vs Passio 4.8% at 20-30 min |
| deep_q15 | Midway Metra | 4,985 |  | 18.5% / 11.8% (2,306) | 17.2% / 4.9% (1,803) | 6.3% / 0.4% (695) | 0.0% / 0.0% (181) | loses: too late 11.8% vs Passio 5.2% at 10-15 min; too late 4.9% vs Passio 3.7% at 15-20 min |
| deep_safe | Midway Metra | 4,985 |  | 15.7% / 8.6% (2,306) | 15.5% / 5.3% (1,803) | 6.2% / 0.3% (695) | 0.0% / 0.0% (181) | loses: too late 8.6% vs Passio 5.2% at 10-15 min; too late 5.3% vs Passio 3.7% at 15-20 min |

### transition:service_start_late:5703 (low, watch)

Midway Metra; scope: hours=15-16;days=weekday;note=before Nov 6 26.316, from Nov 6 33.333 (2 episodes) (not applied: note=before Nov 6 26.316, from Nov 6 33.333 (2 episodes)); 299 samples. Flag: listed spans whose first bus came more than 15 min after the listed start, per 100 spans 27.273 (all lines 16.894).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Midway Metra | 299 | 9.1% / 72.3% (101) | 13.8% / 20.7% (92) | 13.6% / 19.7% (71) | (47.6% / 0.0% (27)) | (0.0% / 0.0% (8)) | reference |
| timetable_delay | Midway Metra | 299 | 13.9% / 52.5% (101) | 7.2% / 42.4% (92) | 27.9% / 15.5% (71) | (45.5% / 11.1% (27)) | (20.0% / 0.0% (8)) | loses: band B 7.2% vs Passio 13.8% at 10-15 min; too late 42.4% vs Passio 20.7% at 10-15 min |
| gbm_q15 | Midway Metra | 299 | 9.0% / 73.3% (101) | 12.0% / 32.6% (92) | 12.3% / 14.1% (71) | (5.0% / 0.0% (27)) | (0.0% / 0.0% (8)) | loses: band B 12.0% vs Passio 13.8% at 10-15 min; too late 32.6% vs Passio 20.7% at 10-15 min |
| deep_q15 | Midway Metra | 299 | 17.0% / 67.3% (101) | 11.2% / 40.2% (92) | 12.1% / 16.9% (71) | (34.8% / 0.0% (27)) | (0.0% / 0.0% (8)) | loses: band B 11.2% vs Passio 13.8% at 10-15 min; too late 40.2% vs Passio 20.7% at 10-15 min; band B 12.1% vs Passio 13.6% at 15-20 min |
| deep_safe | Midway Metra | 299 | 22.0% / 57.4% (101) | 13.8% / 28.3% (92) | 10.8% / 16.9% (71) | (30.4% / 0.0% (27)) | (0.0% / 0.0% (8)) | loses: too late 28.3% vs Passio 20.7% at 10-15 min; band B 10.8% vs Passio 13.6% at 15-20 min |

### display:false_hide_idle_serving_bus:1075 (low, watch)

North; scope: hours=18-19|23-24;vehicles=4313|4317;stops=8579;note=after the rules shipped (2026-11-06 to 2026-11-10): 69.4 vs all lines 37.0, 43 events (not applied: note=after the rules shipped (2026-11-06 to 2026-11-10): 69.4 vs all lines 37.0, 43 events); 64 samples. Flag: percent of minutes core/idle.js hid a still bus that then logged an arrival on the line within 15 min 61.6 (all lines 23.6).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | North | 64 | (15.8% / 21.1% (19)) | (0.0% / 50.0% (18)) | (0.0% / 33.3% (15)) | (0.0% / 18.2% (11)) | (0.0% / 0.0% (1)) | reference |
| timetable_delay | North | 64 | (0.0% / 42.1% (19)) | (7.1% / 44.4% (18)) | (0.0% / 40.0% (15)) | (0.0% / 18.2% (11)) | (0.0% / 0.0% (1)) | too few rows |
| gbm_q15 | North | 64 | (5.3% / 10.5% (19)) | (13.3% / 22.2% (18)) | (15.4% / 6.7% (15)) | (11.1% / 9.1% (11)) | (0.0% / 0.0% (1)) | too few rows |
| deep_q15 | North | 64 | (5.3% / 26.3% (19)) | (5.6% / 33.3% (18)) | (0.0% / 13.3% (15)) | (9.1% / 9.1% (11)) | (0.0% / 0.0% (1)) | too few rows |
| deep_safe | North | 64 | (5.3% / 26.3% (19)) | (11.1% / 33.3% (18)) | (7.1% / 20.0% (15)) | (9.1% / 18.2% (11)) | (0.0% / 0.0% (1)) | too few rows |

### display:false_hide_gone_serving_bus:5699 (low, watch)

Red Line/Arts Block; scope: hours=15-18|21-22;vehicles=12648|4319;note=2026-10-10 to 2026-11-10: 8.9 vs all lines 16.3 (not applied: note=2026-10-10 to 2026-11-10: 8.9 vs all lines 16.3); 152 samples. Flag: percent of minutes core/transition.js GONE dropped a bus's times (no report for 15 min) and the bus then logged an arrival on the line within 15 min 23.6 (all lines 9.9).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Red Line/Arts Block | 152 | 7.8% / 21.2% (52) | 0.0% / 2.8% (36) | 0.0% / 0.0% (33) | (0.0% / 0.0% (27)) | (0.0% / 0.0% (4)) | reference |
| timetable_delay | Red Line/Arts Block | 152 | 12.2% / 13.5% (52) | 18.8% / 16.7% (36) | 3.2% / 3.0% (33) | (0.0% / 0.0% (27)) | (0.0% / 0.0% (4)) | loses: too late 16.7% vs Passio 2.8% at 10-15 min; too late 3.0% vs Passio 0.0% at 15-20 min |
| gbm_q15 | Red Line/Arts Block | 152 | 26.9% / 19.2% (52) | 2.9% / 5.6% (36) | 9.7% / 0.0% (33) | (0.0% / 0.0% (27)) | (0.0% / 0.0% (4)) | loses: too late 5.6% vs Passio 2.8% at 10-15 min |
| deep_q15 | Red Line/Arts Block | 152 | 25.0% / 25.0% (52) | 8.6% / 8.3% (36) | 6.5% / 0.0% (33) | (4.0% / 0.0% (27)) | (0.0% / 0.0% (4)) | loses: too late 25.0% vs Passio 21.2% at 0-10 min; too late 8.3% vs Passio 2.8% at 10-15 min |
| deep_safe | Red Line/Arts Block | 152 | 34.6% / 9.6% (52) | 8.6% / 5.6% (36) | 3.2% / 0.0% (33) | (4.0% / 0.0% (27)) | (0.0% / 0.0% (4)) | loses: too late 5.6% vs Passio 2.8% at 10-15 min |

### prediction_miss:first_stop_next_trip_times:5699 (low, watch)

Red Line/Arts Block; scope: stops=67599|8650|67600;lead=0-10;note=stop positions 1 2 3, 112 of 246 times the bus came later than shown (not applied: note=stop positions 1 2 3, 112 of 246 times the bus came later than shown); 796 samples. Flag: share of the times a screen showed only under another trip id of the same bus 5 min ahead (no own-trip time) that were large misses (more than 2 min either way), last 14 service days 0.5325 (all lines 0.5822).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Red Line/Arts Block | 796 | 10.9% / 56.7% (796) |  |  |  |  | reference |
| timetable_delay | Red Line/Arts Block | 796 | 6.3% / 69.8% (796) |  |  |  |  | loses: band B 6.3% vs Passio 10.9% at 0-10 min; too late 69.8% vs Passio 56.7% at 0-10 min |
| gbm_q15 | Red Line/Arts Block | 796 | 23.4% / 51.9% (796) |  |  |  |  | holds |
| deep_q15 | Red Line/Arts Block | 796 | 31.5% / 37.6% (796) |  |  |  |  | holds |
| deep_safe | Red Line/Arts Block | 796 | 31.9% / 29.5% (796) |  |  |  |  | holds |

### transition:wrong_line_label:5699 (low, watch)

Red Line/Arts Block; scope: hours=15-21;days=weekday;note=before Nov 6 0.517, from Nov 6 0.436 (2 episodes), top spot 59th & Ellis (2 of 17) (not applied: note=before Nov 6 0.517, from Nov 6 0.436 (2 episodes), top spot 59th & Ellis (2 of 17)); 2,978 samples. Flag: bus labeled this line while it drove another line's road for 30 min or more, per 10 bus-hours inside transition windows (30 min around a bus count change, a shift change, a listed start or end, a timetable step) 0.506 (all lines 0.301).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Red Line/Arts Block | 2,978 | 8.2% / 22.5% (1,010) | 3.2% / 5.3% (773) | 4.4% / 4.9% (649) | 11.3% / 3.6% (472) | 0.0% / 0.0% (74) | reference |
| timetable_delay | Red Line/Arts Block | 2,978 | 13.3% / 17.6% (1,010) | 10.2% / 19.7% (773) | 11.4% / 11.6% (649) | 5.8% / 5.9% (472) | 0.0% / 2.7% (74) | loses: too late 19.7% vs Passio 5.3% at 10-15 min; too late 11.6% vs Passio 4.9% at 15-20 min; band B 5.8% vs Passio 11.3% at 20-30 min; too late 5.9% vs Passio 3.6% at 20-30 min; too late 2.7% vs Passio 0.0% at 30-45 min |
| gbm_q15 | Red Line/Arts Block | 2,978 | 24.4% / 23.6% (1,010) | 6.9% / 4.5% (773) | 3.4% / 2.2% (649) | 2.8% / 0.2% (472) | 0.0% / 0.0% (74) | loses: too late 23.6% vs Passio 22.5% at 0-10 min; band B 3.4% vs Passio 4.4% at 15-20 min; band B 2.8% vs Passio 11.3% at 20-30 min |
| deep_q15 | Red Line/Arts Block | 2,978 | 26.1% / 20.3% (1,010) | 10.8% / 6.2% (773) | 7.5% / 2.3% (649) | 5.2% / 0.8% (472) | 0.0% / 0.0% (74) | loses: band B 5.2% vs Passio 11.3% at 20-30 min |
| deep_safe | Red Line/Arts Block | 2,978 | 23.1% / 15.3% (1,010) | 7.8% / 4.9% (773) | 5.4% / 2.8% (649) | 5.0% / 1.3% (472) | 0.0% / 0.0% (74) | loses: band B 5.0% vs Passio 11.3% at 20-30 min |

### display:false_hide_gone_serving_bus:5715 (low, watch)

Regents Express; scope: hours=20-22;vehicles=12648;stops=8643;note=after the rules shipped (2026-11-06 to 2026-11-10): 100.0 vs all lines 9.9, 5 events (not applied: note=after the rules shipped (2026-11-06 to 2026-11-10): 100.0 vs all lines 9.9, 5 events); 12 samples. Flag: percent of minutes core/transition.js GONE dropped a bus's times (no report for 15 min) and the bus then logged an arrival on the line within 15 min 89.2 (all lines 16.3).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Regents Express | 12 | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (3)) | (0.0% / 0.0% (3)) | reference |
| timetable_delay | Regents Express | 12 | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (3)) | (0.0% / 0.0% (3)) | too few rows |
| gbm_q15 | Regents Express | 12 | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (3)) | (0.0% / 0.0% (3)) | too few rows |
| deep_q15 | Regents Express | 12 | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (3)) | (0.0% / 0.0% (3)) | too few rows |
| deep_safe | Regents Express | 12 | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (2)) | (0.0% / 0.0% (3)) | (0.0% / 0.0% (3)) | too few rows |

### display:false_hide_offroute_serving_bus:5715 (low, watch)

Regents Express; scope: hours=18-19|21-22;vehicles=4322|12648;stops=8643;note=after the rules shipped (2026-11-06 to 2026-11-10): 0.0 vs all lines 24.4, 0 events (not applied: note=after the rules shipped (2026-11-06 to 2026-11-10): 0.0 vs all lines 24.4, 0 events); 6 samples. Flag: percent of minutes core/offroute.js hid a bus (and its times) that then logged an arrival on the line within 15 min 37.8 (all lines 19.6).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Regents Express | 6 | (0.0% / 0.0% (2)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (2)) |  | reference |
| timetable_delay | Regents Express | 6 | (0.0% / 0.0% (2)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (2)) |  | too few rows |
| gbm_q15 | Regents Express | 6 | (0.0% / 0.0% (2)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (2)) |  | too few rows |
| deep_q15 | Regents Express | 6 | (0.0% / 0.0% (2)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (2)) |  | too few rows |
| deep_safe | Regents Express | 6 | (0.0% / 0.0% (2)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (2)) |  | too few rows |

### transition:off_route_drive:5715 (low, watch)

Regents Express; scope: hours=21-22;days=weekday;stops=8661;note=before Nov 6 6.313, from Nov 6 4.243 (2 episodes), top spot Cottage Grove & 63rd (12 of 17) (not applied: note=before Nov 6 6.313, from Nov 6 4.243 (2 episodes), top spot Cottage Grove & 63rd (12 of 17)); 0 samples. Flag: bus more than 250 m from its line and its learned corridor (45 s, 2 reports) inside its listed hours, per 10 bus-hours inside transition windows (30 min around a bus count change, a shift change, a listed start or end, a timetable step) 5.97 (all lines 3.487).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | Regents Express | 0 |  |  |  |  |  | no rows |
| timetable_delay | Regents Express | 0 |  |  |  |  |  | no rows |
| gbm_q15 | Regents Express | 0 |  |  |  |  |  | no rows |
| deep_q15 | Regents Express | 0 |  |  |  |  |  | no rows |
| deep_safe | Regents Express | 0 |  |  |  |  |  | no rows |

### prediction_miss:first_stop_next_trip_times:1076 (low, watch)

South; scope: stops=8631;lead=0-10;note=stop positions 0 16, 12 of 39 times the bus came later than shown (not applied: note=stop positions 0 16, 12 of 39 times the bus came later than shown); 98 samples. Flag: share of the times a screen showed only under another trip id of the same bus 5 min ahead (no own-trip time) that were large misses (more than 2 min either way), last 14 service days 0.5641 (all lines 0.5822).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | South | 98 | 6.2% / 44.9% (98) |  |  |  |  | reference |
| timetable_delay | South | 98 | 18.3% / 59.2% (98) |  |  |  |  | loses: too late 59.2% vs Passio 44.9% at 0-10 min |
| gbm_q15 | South | 98 | 17.3% / 14.3% (98) |  |  |  |  | holds |
| deep_q15 | South | 98 | 32.7% / 14.3% (98) |  |  |  |  | holds |
| deep_safe | South | 98 | 23.5% / 7.1% (98) |  |  |  |  | holds |

### transition:unscheduled_leave:1076 (low, watch)

South; scope: hours=21-23;days=weekday;note=before Nov 6 92.857, from Nov 6 100.0 (1 episodes), top spot Midway Plaisance & Cottage Grove (3 of 14) (not applied: note=before Nov 6 92.857, from Nov 6 100.0 (1 episodes), top spot Midway Plaisance & Cottage Grove (3 of 14)); 756 samples. Flag: lasting leaves the timetable does not have that leave the line below its listed bus count for 15 min, per 100 lasting leaves 93.333 (all lines 51.913).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | South | 756 | 15.4% / 36.0% (247) | 16.4% / 11.7% (179) | 18.1% / 5.8% (156) | 27.5% / 4.0% (125) | 22.6% / 0.0% (49) | reference |
| timetable_delay | South | 756 | 11.5% / 60.3% (247) | 5.2% / 43.0% (179) | 8.1% / 34.6% (156) | 15.5% / 32.0% (125) | 18.9% / 24.5% (49) | loses: band B 11.5% vs Passio 15.4% at 0-10 min; too late 60.3% vs Passio 36.0% at 0-10 min; band B 5.2% vs Passio 16.4% at 10-15 min; too late 43.0% vs Passio 11.7% at 10-15 min; band B 8.1% vs Passio 18.1% at 15-20 min; too late 34.6% vs Passio 5.8% at 15-20 min; band B 15.5% vs Passio 27.5% at 20-30 min; too late 32.0% vs Passio 4.0% at 20-30 min; band B 18.9% vs Passio 22.6% at 30-45 min; too late 24.5% vs Passio 0.0% at 30-45 min |
| gbm_q15 | South | 756 | 28.3% / 13.0% (247) | 8.1% / 5.0% (179) | 15.6% / 1.9% (156) | 23.5% / 1.6% (125) | 3.2% / 0.0% (49) | loses: band B 8.1% vs Passio 16.4% at 10-15 min; band B 15.6% vs Passio 18.1% at 15-20 min; band B 23.5% vs Passio 27.5% at 20-30 min; band B 3.2% vs Passio 22.6% at 30-45 min |
| deep_q15 | South | 756 | 25.3% / 11.7% (247) | 6.3% / 8.9% (179) | 7.1% / 10.9% (156) | 20.5% / 11.2% (125) | 0.0% / 0.0% (49) | loses: band B 6.3% vs Passio 16.4% at 10-15 min; band B 7.1% vs Passio 18.1% at 15-20 min; too late 10.9% vs Passio 5.8% at 15-20 min; band B 20.5% vs Passio 27.5% at 20-30 min; too late 11.2% vs Passio 4.0% at 20-30 min; band B 0.0% vs Passio 22.6% at 30-45 min |
| deep_safe | South | 756 | 18.3% / 8.9% (247) | 8.8% / 7.8% (179) | 8.3% / 9.6% (156) | 16.5% / 12.8% (125) | 0.0% / 0.0% (49) | loses: band B 8.8% vs Passio 16.4% at 10-15 min; band B 8.3% vs Passio 18.1% at 15-20 min; too late 9.6% vs Passio 5.8% at 15-20 min; band B 16.5% vs Passio 27.5% at 20-30 min; too late 12.8% vs Passio 4.0% at 20-30 min; band B 0.0% vs Passio 22.6% at 30-45 min |

### display:false_hide_offroute_serving_bus:5716 (low, watch)

South Loop Shuttle; scope: hours=18-23;vehicles=4538;stops=8621;note=after the rules shipped (2026-11-06 to 2026-11-10): 0.0 vs all lines 24.4, 0 events (not applied: note=after the rules shipped (2026-11-06 to 2026-11-10): 0.0 vs all lines 24.4, 0 events); 13 samples. Flag: percent of minutes core/offroute.js hid a bus (and its times) that then logged an arrival on the line within 15 min 42.7 (all lines 19.6).

| model | line | slice samples | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min | verdict vs Passio |
|---|---|---:|---|---|---|---|---|---|
| passio | South Loop Shuttle | 13 | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (2)) | (0.0% / 50.0% (4)) | (0.0% / 20.0% (5)) | reference |
| timetable_delay | South Loop Shuttle | 13 | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (100.0% / 0.0% (2)) | (33.3% / 50.0% (4)) | (40.0% / 60.0% (5)) | too few rows |
| gbm_q15 | South Loop Shuttle | 13 | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (2)) | (0.0% / 50.0% (4)) | (20.0% / 0.0% (5)) | too few rows |
| deep_q15 | South Loop Shuttle | 13 | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (2)) | (0.0% / 25.0% (4)) | (0.0% / 0.0% (5)) | too few rows |
| deep_safe | South Loop Shuttle | 13 | (0.0% / 0.0% (1)) | (0.0% / 0.0% (1)) | (0.0% / 0.0% (2)) | (0.0% / 25.0% (4)) | (20.0% / 0.0% (5)) | too few rows |

