# Individual algorithm (boosted trees) vs deep learning (neural network), same rows

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
| gbm_q30 | 0-10 min | 31,777 | 29.7% | no | 49.9% | 41.1% | 3.3% | -0.3 min | +11.4 pts (+8.3 to +14.2 pts) | +22.9 pts (+20.9 to +24.7 pts) | 0% |
| gbm_q30 | 10-15 min | 26,523 | 19.8% | no | 30.6% | 27.6% | 5.8% | -1.1 min | +10.0 pts (+8.4 to +11.4 pts) | +15.0 pts (+13.6 to +16.7 pts) | 0% |
| gbm_q30 | 15-20 min | 24,372 | 19.0% | no | 28.0% | 20.2% | 10.2% | -1.6 min | +8.3 pts (+7.0 to +9.4 pts) | +11.1 pts (+9.8 to +12.8 pts) | 0% |
| gbm_q30 | 20-30 min | 20,289 | 30.6% | no | 41.0% | 13.1% | 11.8% | -2.4 min | +9.9 pts (+7.8 to +11.4 pts) | +6.3 pts (+5.0 to +8.3 pts) | 0% |
| gbm_q30 | 30-45 min | 6,415 | 17.4% | no | 19.8% | 3.4% | 26.3% | -7.0 min | +5.4 pts (+3.9 to +7.0 pts) | +0.8 pts (+0.1 to +1.5 pts) | 0% |
| deep_q30 | 0-10 min | 31,777 | 31.1% | no | 50.6% | 36.0% | 2.5% | -0.4 min | +12.8 pts (+10.4 to +14.5 pts) | +17.9 pts (+14.3 to +20.9 pts) | 0% |
| deep_q30 | 10-15 min | 26,523 | 21.0% | no | 33.2% | 25.8% | 5.6% | -1.1 min | +11.2 pts (+9.9 to +12.2 pts) | +13.2 pts (+10.6 to +16.1 pts) | 0% |
| deep_q30 | 15-20 min | 24,372 | 19.8% | no | 29.9% | 20.9% | 9.7% | -1.5 min | +9.2 pts (+8.0 to +10.1 pts) | +11.8 pts (+10.0 to +14.2 pts) | 0% |
| deep_q30 | 20-30 min | 20,289 | 30.9% | no | 41.7% | 13.4% | 11.5% | -2.4 min | +10.2 pts (+7.4 to +12.4 pts) | +6.6 pts (+4.9 to +8.9 pts) | 0% |
| deep_q30 | 30-45 min | 6,415 | 18.7% | no | 21.3% | 2.7% | 25.5% | -6.7 min | +6.7 pts (+4.6 to +9.0 pts) | +0.1 pts (-1.3 to +1.5 pts) | 0% |

Goal: most predictions (50% or more) inside band B, the allowed error early (1 min under 20 min ahead, 2 min at 20 to 30, 3 min at 30 or more) to 1% of the lead late. Too late = shown later than the bus came by more than 1% of the lead (the ship gate: never more often than Passio). Errors: negative = the bus came later than predicted.
