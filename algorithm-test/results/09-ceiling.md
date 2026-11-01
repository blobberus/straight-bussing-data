# Ceiling: models fitted on data that includes the day they are graded on

Test days 2026-10-26 to 2026-10-30. Every model here has seen the answers of the day it is scored on, so these numbers are an upper bound for what the same inputs can give, not a result. shift_window picks its corrections to put the most predictions inside band B directly; the q30 models aim at the 30% quantile.

## Fitted on the graded day alone

| model | 0-10 min band B | 10-15 min band B | 15-20 min band B | 20-30 min band B | 30-45 min band B | too late (0-10 / 10-15 / 15-20 / 20-30 / 30-45) |
|---|---:|---:|---:|---:|---:|---|
| passio (no fitting, reference) | 16.8% | 9.5% | 10.1% | 19.4% | 11.9% | 23.3% / 13.3% / 8.7% / 5.5% / 1.7% |
| shift_window | 28.7% | 17.6% | 20.5% | 31.5% | 24.0% | 29.9% / 24.7% / 21.8% / 12.2% / 4.8% |
| gbm_q30 | 31.9% | 23.1% | 22.5% | 33.5% | 22.3% | 33.4% / 21.6% / 17.0% / 11.5% / 2.6% |
| deep_q30 | 22.9% | 15.6% | 16.6% | 25.5% | 18.2% | 37.6% / 22.0% / 15.9% / 11.0% / 2.5% |

## Fitted on every earlier day plus the graded day

| model | 0-10 min band B | 10-15 min band B | 15-20 min band B | 20-30 min band B | 30-45 min band B | too late (0-10 / 10-15 / 15-20 / 20-30 / 30-45) |
|---|---:|---:|---:|---:|---:|---|
| passio (no fitting, reference) | 16.8% | 9.5% | 10.1% | 19.4% | 11.9% | 23.3% / 13.3% / 8.7% / 5.5% / 1.7% |
| shift_window | 24.3% | 14.1% | 18.9% | 32.2% | 23.9% | 35.4% / 29.8% / 25.3% / 14.0% / 6.9% |
| gbm_q30 | 26.9% | 19.1% | 18.3% | 30.7% | 17.7% | 43.3% / 27.6% / 19.2% / 11.3% / 2.8% |
| deep_q30 | 30.8% | 22.2% | 20.3% | 31.7% | 18.0% | 35.6% / 23.2% / 19.1% / 11.7% / 2.2% |

Fitted on one day, the network gets few training steps (6 passes over about a day's rows) and is undertrained, so its first-table numbers understate it; the second table is its fair ceiling.

Goal: 50% band B in every bin.
