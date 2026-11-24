# FAILURE / LIMITATION — the locked test set (manufacturer M2) was evaluated twice (written at the time)
Reading the merged history we found that two sessions, each unaware of the other, ran the "single" locked M2
evaluation: the youthful-meitner lineage on 2026-11-23 (~14:10-14:34 UTC, code/results/locked_m2_*.csv) and the
focused-wozniak lineage on 2026-11-24 (~00:58 UTC, code/results/m2/). Both were negative for every detector we had
proposed (e.g. SRCR-C recall 0.00 at the budget in locked_m2_tests.csv; C2 = rule OR AE recall 0.04 at B=1 in
m2/m2_locked_table.csv). Because both results were negative, the double access did not produce a favourable
selection, but M2 can no longer serve as a blind test. We decided (state/decisions.md D-03) to treat every new M2
number as post hoc and to disclose the double access in the paper. The newest lineage had planned a third M2 run;
we cancelled it.
