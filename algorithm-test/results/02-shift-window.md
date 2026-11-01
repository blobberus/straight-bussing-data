# Individual algorithm v1: learned band-B correction per stop

Test days: 2026-10-20 to 2026-10-30 (11 days, 109,376 samples; each model trained only on earlier days).

| model | lead | samples | band B (goal) | goal met | within allowed | too late | gross | median err | band B vs Passio (95% over days) | too late vs Passio | fallback |
|---|---|---:|---:|:---:|---:|---:|---:|---:|---|---|---:|
| passio | 0-10 min | 31,777 | 18.3% | no | 23.6% | 18.1% | 4.3% | -1.6 min | (reference) | (reference) | 0% |
| passio | 10-15 min | 26,523 | 9.8% | no | 13.9% | 12.6% | 12.0% | -3.2 min | (reference) | (reference) | 0% |
| passio | 15-20 min | 24,372 | 10.7% | no | 14.2% | 9.1% | 20.1% | -3.5 min | (reference) | (reference) | 0% |
| passio | 20-30 min | 20,289 | 20.7% | no | 25.8% | 6.8% | 22.1% | -4.2 min | (reference) | (reference) | 0% |
| passio | 30-45 min | 6,415 | 12.0% | no | 13.4% | 2.6% | 35.0% | -9.2 min | (reference) | (reference) | 0% |
| shift_window | 0-10 min | 31,777 | 34.0% | no | 51.7% | 37.6% | 4.3% | -0.3 min | +15.7 pts (+11.2 to +19.5 pts) | +19.4 pts (+18.6 to +20.2 pts) | 0% |
| shift_window | 10-15 min | 26,523 | 22.9% | no | 36.5% | 35.8% | 7.5% | -0.5 min | +13.1 pts (+10.1 to +15.6 pts) | +23.3 pts (+22.4 to +24.2 pts) | 0% |
| shift_window | 15-20 min | 24,372 | 19.7% | no | 31.6% | 31.0% | 10.8% | -0.9 min | +9.0 pts (+7.2 to +10.6 pts) | +21.9 pts (+21.2 to +22.8 pts) | 0% |
| shift_window | 20-30 min | 20,289 | 32.6% | no | 46.1% | 23.8% | 10.3% | -1.4 min | +11.9 pts (+9.5 to +13.8 pts) | +17.0 pts (+15.7 to +18.2 pts) | 0% |
| shift_window | 30-45 min | 6,415 | 26.5% | no | 39.1% | 22.5% | 15.7% | -2.7 min | +14.5 pts (+10.6 to +17.8 pts) | +19.9 pts (+16.8 to +23.8 pts) | 0% |

Goal: most predictions (50% or more) inside band B, the allowed error early (1 min under 20 min ahead, 2 min at 20 to 30, 3 min at 30 or more) to 1% of the lead late. Too late = shown later than the bus came by more than 1% of the lead (the ship gate: never more often than Passio). Errors: negative = the bus came later than predicted.
