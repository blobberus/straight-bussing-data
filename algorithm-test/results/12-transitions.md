# Transition periods: every model when a line's bus count changes

Test days: 2026-10-26 to 2026-11-05 (11 days, 101,853 samples; each model trained only on earlier days). Transitions: the main repo's data/labeled/transitions/transitions.csv (RouteKnower E29).

Share of samples: normal 81.5%, transition 18.5%, leave ahead (bus leaves within 30 min) 1.8%, just added (within 15 min) 3.4%.

Each cell: band B (the goal: most predictions inside it) / too late (shown later than the bus came by more than 1% of the lead) and the samples.

| model | group | 0-10 band B / too late (n) | 10-15 band B / too late (n) | 15-20 band B / too late (n) | 20-30 band B / too late (n) | 30-45 band B / too late (n) |
|---|---|---|---|---|---|---|
| passio | normal | 15.7% / 28.6% (24,255) | 10.4% / 15.7% (20,298) | 10.3% / 9.5% (18,669) | 21.0% / 7.4% (15,231) | 14.1% / 2.0% (4,515) |
| passio | transition | 15.0% / 27.2% (5,495) | 6.8% / 14.0% (4,339) | 7.6% / 10.3% (3,821) | 12.1% / 4.2% (3,306) | 6.1% / 2.2% (1,924) |
| passio | leave ahead (bus leaves within 30 min) | 12.8% / 24.9% (896) | 8.2% / 13.7% (488) | 6.9% / 9.0% (324) | 24.4% / 5.3% (152) | (n=16) |
| passio | just added (within 15 min) | 18.9% / 31.5% (1,139) | 5.6% / 15.4% (788) | 7.5% / 11.9% (636) | 18.2% / 7.4% (554) | 7.0% / 5.9% (339) |
| timetable_delay | normal | 11.3% / 45.5% (24,255) | 8.8% / 39.9% (20,298) | 11.2% / 39.7% (18,669) | 21.0% / 36.9% (15,231) | 23.7% / 10.8% (4,515) |
| timetable_delay | transition | 13.0% / 40.8% (5,495) | 7.3% / 33.6% (4,339) | 10.4% / 28.4% (3,821) | 17.8% / 18.2% (3,306) | 10.6% / 6.1% (1,924) |
| timetable_delay | leave ahead (bus leaves within 30 min) | 12.9% / 35.5% (896) | 4.9% / 27.5% (488) | 11.8% / 23.1% (324) | 14.3% / 34.2% (152) | (n=16) |
| timetable_delay | just added (within 15 min) | 17.4% / 38.2% (1,139) | 4.3% / 31.9% (788) | 10.3% / 30.3% (636) | 27.4% / 24.2% (554) | 15.2% / 11.2% (339) |
| gbm_q15 | normal | 26.5% / 28.9% (24,255) | 14.8% / 15.4% (20,298) | 12.7% / 9.7% (18,669) | 24.2% / 5.9% (15,231) | 9.6% / 0.8% (4,515) |
| gbm_q15 | transition | 24.5% / 29.0% (5,495) | 13.3% / 15.9% (4,339) | 10.1% / 10.9% (3,821) | 15.7% / 4.5% (3,306) | 6.2% / 3.3% (1,924) |
| gbm_q15 | leave ahead (bus leaves within 30 min) | 24.6% / 26.5% (896) | 10.1% / 15.4% (488) | 7.3% / 9.6% (324) | 25.4% / 3.9% (152) | (n=16) |
| gbm_q15 | just added (within 15 min) | 25.9% / 33.6% (1,139) | 10.3% / 16.2% (788) | 10.7% / 10.2% (636) | 18.9% / 7.0% (554) | 6.0% / 4.7% (339) |
| deep_q15 | normal | 28.1% / 23.1% (24,255) | 17.2% / 13.9% (20,298) | 15.9% / 10.8% (18,669) | 27.1% / 6.1% (15,231) | 8.4% / 0.4% (4,515) |
| deep_q15 | transition | 25.9% / 23.7% (5,495) | 14.4% / 14.2% (4,339) | 13.5% / 11.0% (3,821) | 19.0% / 6.0% (3,306) | 11.4% / 1.9% (1,924) |
| deep_q15 | leave ahead (bus leaves within 30 min) | 25.8% / 22.5% (896) | 17.6% / 14.8% (488) | 9.3% / 9.0% (324) | 22.6% / 5.3% (152) | (n=16) |
| deep_q15 | just added (within 15 min) | 27.6% / 27.1% (1,139) | 12.9% / 15.4% (788) | 13.2% / 12.9% (636) | 21.2% / 9.4% (554) | 11.5% / 3.2% (339) |
| deep_safe | normal | 25.7% / 18.1% (24,255) | 15.1% / 12.0% (20,298) | 14.9% / 10.0% (18,669) | 27.7% / 7.2% (15,231) | 11.0% / 0.6% (4,515) |
| deep_safe | transition | 24.1% / 19.3% (5,495) | 13.9% / 11.8% (4,339) | 12.2% / 10.5% (3,821) | 19.5% / 6.8% (3,306) | 12.1% / 3.8% (1,924) |
| deep_safe | leave ahead (bus leaves within 30 min) | 22.9% / 18.8% (896) | 12.9% / 12.7% (488) | 7.4% / 9.3% (324) | 21.3% / 5.3% (152) | (n=16) |
| deep_safe | just added (within 15 min) | 26.8% / 22.5% (1,139) | 13.0% / 13.5% (788) | 14.1% / 11.8% (636) | 21.8% / 10.1% (554) | 15.1% / 4.1% (339) |

## Passio's times that never came true, around buses that leave their line

From the whole tables of the test days (every minute, every stop Passio showed for a bus). A bus that leaves its line stops serving it; Passio keeps showing it (79% of lasting leaves, E29). The main repo's app now drops a bus's times once it has sent no report for 15 min (web/js/core/transition.js).

| bus state | Passio times shown (bus-minute x stop) | never came true |
|---|---:|---:|
| before leaving (45 min) | 95,380 | 70.0% |
| after leaving (45 min) | 28,498 | 55.7% |
| otherwise | 934,024 | 35.5% |
