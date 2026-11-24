RETROSPECTIVE entry reconstructed on 2026-11-24 from code/experiments/novelty_escalation_log.md peaceful-planck section 'LOCKED M2 RESULT' (commits c970923 14:10 and ee3c15d 14:34); results/locked_m2_operating_points.csv, results/locked_m2_tests.csv; not written at the time.

# Locked M2 evaluation #1 (youthful-meitner): negative

scripts/m2_evaluate.py 2 2000 was run once. The start was logged at 14:10 and the result at 14:34.

Recall at B = 2 (n = 25): "sigma3 0.28, qnbm 0.20, ae_comfort 0.12, rule 0.08, loop3s_c 0.08, loop3s 0.08, iforest 0.08,
ae 0.04, srcr_c 0.00, srcr_all 0.00, ae_cond 0.00".

- HF4 FAILED.
- HF1 was not supported on M2.
- HF2 reversed.
- HF3: SRCR-C ranks worse than the rule (p = 0.0003).

A post hoc check found that development rankings do not transfer: Spearman M1 vs M2 is "B=1 -0.33, B=2 -0.15,
B=4 0.07".

The log: "M2 is now burned for method selection."
