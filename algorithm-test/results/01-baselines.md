# Baselines against the accuracy requirement

Test days: 2026-10-20 to 2026-10-30 (11 days, 109,376 samples; each model trained only on earlier days).

| model | lead | samples | band B (goal) | goal met | within allowed | too late | gross | median err | band B vs Passio (95% over days) | too late vs Passio | fallback |
|---|---|---:|---:|:---:|---:|---:|---:|---:|---|---|---:|
| passio | 0-10 min | 31,777 | 18.3% | no | 23.6% | 18.1% | 4.3% | -1.6 min | (reference) | (reference) | 0% |
| passio | 10-15 min | 26,523 | 9.8% | no | 13.9% | 12.6% | 12.0% | -3.2 min | (reference) | (reference) | 0% |
| passio | 15-20 min | 24,372 | 10.7% | no | 14.2% | 9.1% | 20.1% | -3.5 min | (reference) | (reference) | 0% |
| passio | 20-30 min | 20,289 | 20.7% | no | 25.8% | 6.8% | 22.1% | -4.2 min | (reference) | (reference) | 0% |
| passio | 30-45 min | 6,415 | 12.0% | no | 13.4% | 2.6% | 35.0% | -9.2 min | (reference) | (reference) | 0% |
| timetable | 0-10 min | 31,777 | 12.5% | no | 20.1% | 26.3% | 30.2% | -1.4 min | -5.8 pts (-8.1 to -4.1 pts) | +8.1 pts (+3.2 to +12.4 pts) | 10% |
| timetable | 10-15 min | 26,523 | 10.9% | no | 17.6% | 24.8% | 28.9% | -2.0 min | +1.1 pts (-0.7 to +2.2 pts) | +12.2 pts (+9.9 to +14.0 pts) | 11% |
| timetable | 15-20 min | 24,372 | 11.1% | no | 17.8% | 24.1% | 28.4% | -2.1 min | +0.4 pts (-1.5 to +1.5 pts) | +15.0 pts (+13.4 to +16.2 pts) | 11% |
| timetable | 20-30 min | 20,289 | 18.3% | no | 29.4% | 20.7% | 23.1% | -3.2 min | -2.4 pts (-6.1 to -0.2 pts) | +13.9 pts (+12.2 to +15.4 pts) | 13% |
| timetable | 30-45 min | 6,415 | 13.9% | no | 23.2% | 11.6% | 29.6% | -7.7 min | +1.9 pts (-0.7 to +4.0 pts) | +9.0 pts (+7.6 to +10.3 pts) | 36% |
| timetable_delay | 0-10 min | 31,777 | 12.1% | no | 19.6% | 42.5% | 15.2% | -0.8 min | -6.2 pts (-8.7 to -4.7 pts) | +24.4 pts (+18.9 to +28.9 pts) | 12% |
| timetable_delay | 10-15 min | 26,523 | 8.7% | no | 15.3% | 39.3% | 14.3% | -1.1 min | -1.1 pts (-3.8 to +0.7 pts) | +26.7 pts (+23.7 to +29.8 pts) | 13% |
| timetable_delay | 15-20 min | 24,372 | 10.8% | no | 18.6% | 39.0% | 15.7% | -0.8 min | +0.1 pts (-2.6 to +2.0 pts) | +29.8 pts (+27.5 to +32.9 pts) | 12% |
| timetable_delay | 20-30 min | 20,289 | 20.8% | no | 40.0% | 35.4% | 14.2% | -1.0 min | +0.1 pts (-3.5 to +2.4 pts) | +28.6 pts (+25.9 to +32.3 pts) | 14% |
| timetable_delay | 30-45 min | 6,415 | 21.8% | no | 24.2% | 8.2% | 24.5% | -5.8 min | +9.8 pts (+7.7 to +12.2 pts) | +5.6 pts (+3.7 to +7.9 pts) | 38% |

Goal: most predictions (50% or more) inside band B, the allowed error early (1 min under 20 min ahead, 2 min at 20 to 30, 3 min at 30 or more) to 1% of the lead late. Too late = shown later than the bus came by more than 1% of the lead (the ship gate: never more often than Passio). Errors: negative = the bus came later than predicted.
