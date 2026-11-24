# RESULT / SURPRISE — CARE confirmation, seed 0 (written at the time)
We ran the pre-registered Round-6 analysis once (results/round6/seed0/summary.json, protocol_compare_care.csv).
The protocol gap replicates on wind turbines: event precision exceeds deployed alarm precision 7.6x-20.6x, and the
thresholds the event protocol picks would raise 6.7-16.7 false alarms per turbine-year. But our stricter G5-style
test (H6e: CI lower bound > 5 for every method) FAILED: three-sigma's lower bound is 4.98, and IForest's
leave-one-farm-out operating point raised no alarm at all, so its ratio is undefined.
The surprise is H6c: the benchmark's own normal events are much quieter than ordinary normal operation. The AE
alarms on 16% of the 50 normal events but on 37% of 1,810 random normal 7-day windows of the same turbines
(rate ratio 0.43; 0.30-0.61 across the 4 evaluable methods; every CI below 1; length-matched 0.34). So a
balanced benchmark is optimistic for two reasons, not one: the 50/50 base rate, and normal periods that are
easier than real normal time. This is the first specific benchmark-construction effect we have found; it still
needs the PreDist test (H5d, pre-registered) and a prior-art check.
