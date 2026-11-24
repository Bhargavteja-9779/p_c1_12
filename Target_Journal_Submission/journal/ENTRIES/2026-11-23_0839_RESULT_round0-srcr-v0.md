RETROSPECTIVE entry reconstructed on 2026-11-24 from code/experiments/novelty_escalation_log.md 'Round 0' (commit c50331b, 08:39); not written at the time.

# Round 0: first SRCR version on M1

Result on M1 (28 evaluable faults):
- SRCR-v0: "recall 0.29 at 2.4 FA/sub-yr (tau 3, c_thr 36); 0.39 at 5.1".
- AE baseline: "recall 0.07-0.11 at 2.0-2.7 FA/sub-yr".

Stated diagnosis:
- SRCR-v0 catches loop-breaking hardware faults.
- It misses control-unit parameterisation faults (11/28), where "the setpoint itself is wrong".
- It misses heating-pump failures and leakages.
- AE catches some of these, so the two have complementary failure modes.
