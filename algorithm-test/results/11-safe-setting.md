# A network tuned to the ship gate's safety rule: never too late more often than Passio

Test days: 2026-10-20 to 2026-10-30 (11 days, 109,376 samples; each model trained only on earlier days).

| model | lead | samples | band B (goal) | goal met | within allowed | too late | gross | median err | band B vs Passio (95% over days) | too late vs Passio | fallback |
|---|---|---:|---:|:---:|---:|---:|---:|---:|---|---|---:|
| passio | 0-10 min | 31,777 | 18.3% | no | 23.6% | 18.1% | 4.3% | -1.6 min | (reference) | (reference) | 0% |
| passio | 10-15 min | 26,523 | 9.8% | no | 13.9% | 12.6% | 12.0% | -3.2 min | (reference) | (reference) | 0% |
| passio | 15-20 min | 24,372 | 10.7% | no | 14.2% | 9.1% | 20.1% | -3.5 min | (reference) | (reference) | 0% |
| passio | 20-30 min | 20,289 | 20.7% | no | 25.8% | 6.8% | 22.1% | -4.2 min | (reference) | (reference) | 0% |
| passio | 30-45 min | 6,415 | 12.0% | no | 13.4% | 2.6% | 35.0% | -9.2 min | (reference) | (reference) | 0% |
| deep_q15 | 0-10 min | 31,777 | 29.9% | no | 42.6% | 21.7% | 2.6% | -1.0 min | +11.6 pts (+10.2 to +12.8 pts) | +3.6 pts (-0.0 to +6.7 pts) | 0% |
| deep_q15 | 10-15 min | 26,523 | 16.9% | no | 24.2% | 13.9% | 6.9% | -2.0 min | +7.1 pts (+6.2 to +7.9 pts) | +1.3 pts (-1.4 to +4.3 pts) | 0% |
| deep_q15 | 15-20 min | 24,372 | 16.0% | no | 21.5% | 11.1% | 11.3% | -2.4 min | +5.3 pts (+4.1 to +6.6 pts) | +1.9 pts (+0.2 to +4.1 pts) | 0% |
| deep_q15 | 20-30 min | 20,289 | 26.0% | no | 31.3% | 6.3% | 13.7% | -3.4 min | +5.3 pts (+3.8 to +7.1 pts) | -0.5 pts (-2.1 to +1.3 pts) | 0% |
| deep_q15 | 30-45 min | 6,415 | 10.9% | no | 11.9% | 0.9% | 28.7% | -8.3 min | -1.1 pts (-3.8 to +1.5 pts) | -1.7 pts (-2.9 to -0.7 pts) | 0% |
| deep_safe | 0-10 min | 31,777 | 26.8% | no | 36.6% | 16.8% | 2.8% | -1.2 min | +8.5 pts (+7.7 to +9.4 pts) | -1.3 pts (-5.0 to +1.8 pts) | 0% |
| deep_safe | 10-15 min | 26,523 | 14.7% | no | 20.5% | 11.6% | 7.7% | -2.4 min | +4.9 pts (+3.9 to +5.8 pts) | -1.0 pts (-3.3 to +1.3 pts) | 0% |
| deep_safe | 15-20 min | 24,372 | 15.0% | no | 20.0% | 10.0% | 12.6% | -2.6 min | +4.4 pts (+3.2 to +5.6 pts) | +0.9 pts (-0.5 to +2.5 pts) | 0% |
| deep_safe | 20-30 min | 20,289 | 26.2% | no | 32.3% | 7.3% | 14.6% | -3.3 min | +5.5 pts (+3.9 to +6.8 pts) | +0.5 pts (-1.0 to +2.5 pts) | 0% |
| deep_safe | 30-45 min | 6,415 | 13.3% | no | 15.1% | 1.9% | 29.4% | -7.8 min | +1.3 pts (-1.4 to +4.1 pts) | -0.8 pts (-2.0 to +0.4 pts) | 0% |

Goal: most predictions (50% or more) inside band B, the allowed error early (1 min under 20 min ahead, 2 min at 20 to 30, 3 min at 30 or more) to 1% of the lead late. Too late = shown later than the bus came by more than 1% of the lead (the ship gate: never more often than Passio). Errors: negative = the bus came later than predicted.
