# Novelty escalation log (D6). Development data = M1 only. M2 locked.

Ideas tried are counted cumulatively (for multiple-comparison reporting). Results here are DEVELOPMENT
results (M1, cross-fitted over substations); they are used for idea selection only.

## Round 0 (2026-11-23) — first working version
- Idea #1: SRCR-v0 = execution channel only: setpoint-relative tracking residuals of all available loops,
  fleet-shared LightGBM quantile band (2/50/98%), 5-fold grouped cross-fitting; criticality-counter alarms.
- Baseline reference: AE (PreDist benchmark re-implementation), online retraining every 90 days.
- Result (M1, 28 evaluable faults, ~125 substation-years exposure):
  - AE: recall 0.07-0.11 at 2.0-2.7 FA/sub-yr; 0.43 at 13.6-19.6 FA/sub-yr (paper-like operating point
    c_thr 12-18 gives ~14-20 FA/sub-yr, i.e. ~25-35 false alarms per week for a 93-substation fleet).
  - SRCR-v0: recall 0.29 at 2.4 FA/sub-yr (tau 3, c_thr 36); 0.39 at 5.1.
- Diagnosis (threshold-free rank of each fault's best pre-report day among 45k normal substation-days):
  - SRCR-v0 catches loop-breaking hardware faults (valve actuator, controller defective, DHW charging pump,
    differential pressure regulator) at rank < 2%.
  - Misses: (a) control-unit parameterisation faults (11/28) — the setpoint itself is wrong, tracking is fine;
    (b) heating-pump failures and leakages — need delivered-heat / hydraulic evidence.
  - AE catches some (a) and (b) cases (events 12, 18, 47, 53) -> complementary failure modes.

## Round 1 plan (hypotheses written BEFORE running)
Candidate families (>= 5, different):
 F1 Intent channel (problem formulation/representation): setpoint plausibility = deviation of the HC1/DHW
    setpoint from the substation's own learned heating curve (setpoint vs outdoor temperature) and from a
    fleet comfort floor.
 F2 Delivery channel (physics representation): energy-signature residual = heat power vs outdoor temperature
    and time context, own history quantile band -> under-delivery (pumps, regulators, closed valves) and
    over-consumption/flow (leakage).
 F3 Calibrated channel fusion (inference): each channel converted to a fleet-calibrated exceedance level
    (normal-day quantile estimated on training folds only), fused by maximum.
 F4 Integrated-deficit alarm logic (inference): degree-hour integration instead of a criticality counter.
 F5 Weak-label supervised ranker using maintenance disturbances (learning signal).
 F6 Substation-level conformal calibration of the alarm threshold for a guaranteed FA budget (theory).
Pre-registered hypotheses for the top three (F1, F2, F3):
 H1a: F1 brings >= 3 of the 11 parameterisation faults below rank 2%. Falsified otherwise.
 H1b: F2 brings >= 2 of {pump failures 5, 24, 47; leakages 10, 65} below rank 2%. Falsified otherwise.
 H1c: Fusion F3 (execution + intent + delivery) raises M1 recall at 2 FA/sub-yr by >= 0.10 absolute over
      SRCR-v0, while keeping each channel's contribution non-zero in ablation. Falsified otherwise.
