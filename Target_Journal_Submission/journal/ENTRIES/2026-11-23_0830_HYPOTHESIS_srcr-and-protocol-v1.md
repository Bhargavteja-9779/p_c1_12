RETROSPECTIVE entry reconstructed on 2026-11-24 from code/experiments/protocol.md v1 (commit cf4c7a2, 08:30) and TEST_LOCK.md (commit b9f7bea, 08:24); not written at the time.

# SRCR idea and pre-registered protocol v1

Proposed method: SRCR, setpoint-relative control-loop residuals scored by a fleet-shared conditional quantile model,
to be developed on M1 only.

Protocol v1:
- every 10-min step is scored;
- recall in the 7 days before the customer report;
- primary metric: recall at B = 2 false alarms per substation-year, with M1-chosen operating points applied unchanged
  to M2;
- M2 (58 substations) is locked as the test set and is to be evaluated "exactly once".
