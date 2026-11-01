# Per route: boosted trees and the network at the 15% quantile

Test days: 2026-10-20 to 2026-10-30 (11 days, 109,376 samples; each model trained only on earlier days).

| model | lead | samples | band B (goal) | goal met | within allowed | too late | gross | median err | band B vs Passio (95% over days) | too late vs Passio | fallback |
|---|---|---:|---:|:---:|---:|---:|---:|---:|---|---|---:|
| passio | 0-10 min | 31,777 | 18.3% | no | 23.6% | 18.1% | 4.3% | -1.6 min | (reference) | (reference) | 0% |
| passio | 10-15 min | 26,523 | 9.8% | no | 13.9% | 12.6% | 12.0% | -3.2 min | (reference) | (reference) | 0% |
| passio | 15-20 min | 24,372 | 10.7% | no | 14.2% | 9.1% | 20.1% | -3.5 min | (reference) | (reference) | 0% |
| passio | 20-30 min | 20,289 | 20.7% | no | 25.8% | 6.8% | 22.1% | -4.2 min | (reference) | (reference) | 0% |
| passio | 30-45 min | 6,415 | 12.0% | no | 13.4% | 2.6% | 35.0% | -9.2 min | (reference) | (reference) | 0% |
| gbm_q15 | 0-10 min | 31,777 | 29.2% | no | 42.2% | 25.4% | 2.9% | -0.9 min | +10.9 pts (+8.8 to +12.9 pts) | +7.2 pts (+5.5 to +8.7 pts) | 0% |
| gbm_q15 | 10-15 min | 26,523 | 15.1% | no | 21.7% | 15.0% | 6.8% | -2.1 min | +5.3 pts (+4.0 to +6.5 pts) | +2.4 pts (+1.4 to +3.6 pts) | 0% |
| gbm_q15 | 15-20 min | 24,372 | 13.0% | no | 17.4% | 9.8% | 12.2% | -2.8 min | +2.4 pts (+1.2 to +3.4 pts) | +0.6 pts (-0.2 to +1.6 pts) | 0% |
| gbm_q15 | 20-30 min | 20,289 | 24.0% | no | 28.2% | 5.5% | 14.7% | -3.7 min | +3.3 pts (+2.2 to +4.4 pts) | -1.3 pts (-2.1 to -0.6 pts) | 0% |
| gbm_q15 | 30-45 min | 6,415 | 8.5% | no | 9.5% | 1.9% | 31.1% | -8.3 min | -3.5 pts (-5.0 to -2.1 pts) | -0.7 pts (-1.5 to -0.1 pts) | 0% |
| deep_q15 | 0-10 min | 31,777 | 29.9% | no | 42.6% | 21.7% | 2.6% | -1.0 min | +11.6 pts (+10.2 to +12.8 pts) | +3.6 pts (-0.0 to +6.7 pts) | 0% |
| deep_q15 | 10-15 min | 26,523 | 16.9% | no | 24.2% | 13.9% | 6.9% | -2.0 min | +7.1 pts (+6.2 to +7.9 pts) | +1.3 pts (-1.4 to +4.3 pts) | 0% |
| deep_q15 | 15-20 min | 24,372 | 16.0% | no | 21.5% | 11.1% | 11.3% | -2.4 min | +5.3 pts (+4.1 to +6.6 pts) | +1.9 pts (+0.2 to +4.1 pts) | 0% |
| deep_q15 | 20-30 min | 20,289 | 26.0% | no | 31.3% | 6.3% | 13.7% | -3.4 min | +5.3 pts (+3.8 to +7.1 pts) | -0.5 pts (-2.1 to +1.3 pts) | 0% |
| deep_q15 | 30-45 min | 6,415 | 10.9% | no | 11.9% | 0.9% | 28.7% | -8.3 min | -1.1 pts (-3.8 to +1.5 pts) | -1.7 pts (-2.9 to -0.7 pts) | 0% |

Goal: most predictions (50% or more) inside band B, the allowed error early (1 min under 20 min ahead, 2 min at 20 to 30, 3 min at 30 or more) to 1% of the lead late. Too late = shown later than the bus came by more than 1% of the lead (the ship gate: never more often than Passio). Errors: negative = the bus came later than predicted.

## Per route (ship gate: no route more than 10% worse than Passio in band B)

| route | lead | samples | Passio band B | gbm_q15 band B | deep_q15 band B | Passio too late | gbm_q15 too late | deep_q15 too late |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 53rd Street Express | 0-10 min | 3,433 | 12.5% | 28.0% | 29.3% | 20.4% | 33.0% | 19.6% |
| 53rd Street Express | 10-15 min | 3,210 | 5.8% | 17.0% | 19.0% | 12.5% | 22.7% | 15.8% |
| 53rd Street Express | 20-30 min | 3,013 | 9.8% | 20.6% | 26.4% | 1.3% | 3.5% | 4.3% |
| Apostolic | 0-10 min | 2,032 | 18.2% | 33.1% | 30.8% | 5.4% | 15.6% | 13.7% |
| Apostolic | 10-15 min | 1,664 | 7.2% | 18.3% | 21.4% | 5.9% | 15.1% | 15.0% |
| Apostolic | 20-30 min | 1,508 | 22.0% | 27.9% | 25.4% | 2.1% | 2.5% | 3.2% |
| Apostolic/Drexel | 0-10 min | 4,692 | 14.8% | 22.3% | 23.9% | 17.5% | 22.0% | 22.6% |
| Apostolic/Drexel | 10-15 min | 3,671 | 9.5% | 9.6% | 12.9% | 10.8% | 9.8% | 11.1% |
| Apostolic/Drexel | 20-30 min | 2,354 | 18.9% | 16.2% (worse by >10%) | 17.4% | 3.4% | 2.2% | 2.0% |
| Central | 0-10 min | 1,828 | 21.2% | 30.5% | 34.6% | 29.4% | 36.7% | 30.7% |
| Central | 10-15 min | 1,487 | 9.4% | 16.0% | 16.6% | 17.7% | 26.0% | 25.8% |
| Central | 20-30 min | 1,472 | 23.6% | 27.4% | 25.7% | 8.6% | 11.1% | 17.3% |
| Downtown Campus Connector | 0-10 min | 3,321 | 21.4% | 28.6% | 28.9% | 16.6% | 22.7% | 21.9% |
| Downtown Campus Connector | 10-15 min | 2,901 | 5.8% | 15.6% | 14.0% | 13.0% | 20.6% | 19.3% |
| Downtown Campus Connector | 20-30 min | 2,546 | 3.2% | 14.5% | 18.4% | 5.7% | 7.3% | 9.2% |
| Drexel | 0-10 min | 1,413 | 27.8% | 37.8% | 38.4% | 6.4% | 17.1% | 14.5% |
| Drexel | 10-15 min | 968 | 20.0% | 26.6% | 24.0% | 2.6% | 3.9% | 5.1% |
| East | 0-10 min | 1,799 | 18.4% | 26.0% | 28.6% | 30.1% | 30.6% | 23.5% |
| East | 10-15 min | 1,677 | 15.7% | 20.8% | 19.9% | 18.2% | 16.2% | 15.8% |
| East | 20-30 min | 1,515 | 31.4% | 39.1% | 40.2% | 11.9% | 8.8% | 11.0% |
| Friend Center/Metra | 0-10 min | 2,880 | 26.0% | 32.4% | 34.8% | 18.9% | 23.5% | 20.3% |
| Friend Center/Metra | 10-15 min | 2,765 | 19.2% | 18.7% | 23.0% | 17.9% | 17.8% | 15.7% |
| Friend Center/Metra | 20-30 min | 2,630 | 38.5% | 40.8% | 43.4% | 14.5% | 10.7% | 8.2% |
| Midway Metra | 0-10 min | 3,478 | 18.3% | 31.8% | 30.4% | 13.6% | 29.4% | 23.4% |
| Midway Metra | 10-15 min | 2,789 | 4.0% | 13.5% | 13.5% | 4.1% | 8.2% | 9.4% |
| Midway Metra | 20-30 min | 1,029 | 3.0% | 2.2% (worse by >10%) | 4.4% | 1.0% | 0.4% | 1.0% |
| North | 0-10 min | 926 | 28.2% | 32.6% | 31.3% | 23.2% | 22.2% | 28.7% |
| North | 10-15 min | 825 | 23.4% | 21.1% | 25.5% | 21.2% | 11.5% | 14.3% |
| North | 20-30 min | 731 | 33.3% | 31.9% | 36.8% | 15.3% | 6.2% | 7.7% |
| Red Line/Arts Block | 0-10 min | 3,998 | 9.8% | 27.8% | 26.8% | 12.2% | 23.8% | 21.1% |
| Red Line/Arts Block | 10-15 min | 3,117 | 2.7% | 7.2% | 11.3% | 7.8% | 9.2% | 7.5% |
| Red Line/Arts Block | 20-30 min | 2,047 | 9.5% | 7.2% (worse by >10%) | 8.9% | 5.1% | 1.7% | 2.0% |
| South | 0-10 min | 1,703 | 24.0% | 33.5% | 34.7% | 37.2% | 25.7% | 23.1% |
| South | 10-15 min | 1,226 | 16.3% | 16.9% | 17.0% | 31.6% | 17.4% | 14.6% |
| South | 20-30 min | 949 | 35.7% | 36.0% | 34.8% | 13.3% | 6.3% | 7.0% |

Worse than Passio by more than 10% (relative): gbm_q15 on Apostolic/Drexel at 20-30 min; gbm_q15 on Midway Metra at 20-30 min; gbm_q15 on Red Line/Arts Block at 20-30 min.
