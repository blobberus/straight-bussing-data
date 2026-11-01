# E24 headroom check: the same learned shift with and without the real arrival

Test days 2026-10-20 to 2026-10-30, learned on earlier days only. Each cell: 10% rule / band B as E24 read it (10% of the lead early to 1% late) / too late (shown later than the bus came by more than 1% of the lead).

| version | shift tuned for | 0-10 min | 10-15 min | 15-20 min | 20-30 min | 30-45 min |
|---|---|---|---|---|---|---|
| Passio as shown |  | 9% / 6% / 18% | 17% / 13% / 13% | 25% / 19% / 9% | 31% / 25% / 7% | 14% / 13% / 3% |
| as in E24 (leaks the real arrival) | 10% rule | 32% / 18% / 53% | 46% / 25% / 45% | 50% / 27% / 38% | 55% / 31% / 35% | 47% / 27% / 30% |
| leak-free | 10% rule | 22% / 12% / 43% | 38% / 21% / 40% | 47% / 27% / 33% | 52% / 32% / 25% | 38% / 27% / 11% |
| as in E24 (leaks the real arrival) | band B (10% early to 1% late) | 31% / 19% / 45% | 44% / 28% / 33% | 46% / 32% / 25% | 51% / 38% / 21% | 43% / 30% / 20% |
| leak-free | band B (10% early to 1% late) | 21% / 12% / 40% | 37% / 23% / 32% | 44% / 30% / 24% | 46% / 35% / 14% | 32% / 25% / 7% |
