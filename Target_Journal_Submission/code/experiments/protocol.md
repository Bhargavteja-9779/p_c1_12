# Pre-registered experimental protocol — v1

Date fixed: 2026-11-23 (before any detector score was computed or inspected).
Later versions may ADD experiments; any change to items below is logged with date and reason in the
"Amendments" section, and the original v1 analysis is still reported.

## Data and splits
- Dataset: PreDist v1 (Zenodo 19496480, CC-BY-4.0): 93 district heating substations, 10-min data,
  manufacturers M1 (35 substations, 144 substation-years) and M2 (58 substations, 95 substation-years).
- DEVELOPMENT = M1. LOCKED TEST = M2 (see TEST_LOCK.md). Final candidates are trained/calibrated on M1 only
  and applied to M2 exactly once ("cross-manufacturer transfer").
- Within M1, fleet (cross-substation) models use grouped 5-fold cross-fitting over substations
  (seed 0 permutation); a substation's scores never come from a model trained on its own data.
- Per-substation models (baselines) are trained online: retrain every 90 days on up to 730 days of the
  substation's own past, excluding exclusion intervals already known at retraining time.
- Sensitivity analysis (temporal leakage control for fleet models): train fleet models only on data before
  2018-01-01 and evaluate after that date.

## Primary evaluation: continuous fleet monitoring (src/evaluation/continuous.py)
- Every monitored 10-min step after a 30-day burn-in is scored; detection window = 7 days before the
  customer report; alarms refractory for 24 h; exclusion intervals around all fault reports, disturbances and
  README-listed known anomalies. Target faults: efd_possible == True with the window inside the monitored span
  (M1: 29, M2: 24 evaluable as computed by the harness; total 53).
- Primary metric: fault recall (share of target faults with an alarm in the 7 days before the report) at a
  false-alarm budget of B = 2 false alarms per substation-year. Secondary: recall at B = 1 and B = 4;
  area under the recall-vs-false-alarm curve for B in [0, 6] (normalised); median lead time of detected
  faults; alarm precision (true alarms / all counted alarms).
- Operating point selection: each method's alarm parameters (criticality threshold c_thr and score threshold
  tau) are chosen on M1 to maximise recall subject to FA/sub-year <= B. On M2 the M1-chosen operating point
  is applied unchanged (tests calibration transfer); the M2 FA rate actually achieved is reported.
- Secondary evaluation: the original PreDist event protocol (7-day windows, 50/50 fault vs normal events,
  eventwise F0.5, earliness) for comparability with the benchmark paper.

## Methods (all receive the same raw signals, same exclusions, same evaluation, same tuning budget)
- B1 Rule: expert rule "HC1 supply temperature more than k K below setpoint for more than h hours".
- B2 Three-sigma per signal on own history (classical statistical baseline).
- B3 Isolation Forest per substation (conventional ML).
- B4 Autoencoder NBM = PreDist benchmark (EnergyFaultDetector configuration re-implemented; default and
  conditional variants). Validated against the official package on the event protocol.
- B5 Quantile-regression NBM on own history (Smart Energy 2024 "beyond three-sigma" idea).
- B6 Fleet-pooled autoencoder (cross-substation pretraining, a transfer-learning baseline).
- B7 Lightweight: per-loop residual three-sigma (setpoint-relative but without the fleet model) — ablation-type.
- Proposed: SRCR family (setpoint-relative residuals + fleet-shared conditional quantile model), developed
  through the novelty-escalation loop on M1 only.
- Tuning budget: each method gets the same alarm-parameter grid (c_thr in {1,2,3,6,9,12,18,24,36,48,72,96,
  144,216,288}, tau in {1, 1.5, 2, 3}) and at most 20 configurations of model hyperparameters evaluated on M1.

## Seeds and uncertainty
- Seeds 0-9 for every stochastic method (model init, subsampling, fold permutation for fleet models).
  Report mean ± SD over seeds.
- Unit of analysis for inference = fault event (recall) and substation (false-alarm rate). 95% CIs by
  cluster bootstrap over substations (10,000 resamples). Paired comparisons proposed vs each baseline at the
  same budget: paired cluster bootstrap of the recall difference and exact McNemar test on faults;
  Holm correction across baselines. Effect sizes: recall difference and odds ratio of detection.
- All ideas tried in the escalation loop are counted and reported.

## Robustness / generalisation / other analyses
- Cold start: performance as a function of days of own history available (0-14, 14-90, 90-365, >365 d).
- Missing signals: drop DHW or primary-return loops; drop outdoor temperature.
- Cross-manufacturer: M1 -> M2 (locked). Temporal sensitivity as above.
- Error analysis by fault label and monitoring potential; case studies (detected by proposed only, by AE only,
  by neither).
- Efficiency: training and scoring time per substation-year, model size.
- Real-world impact: for a 93-substation fleet, expected alarms per week and complaints pre-empted per year
  at each budget; technician visits per pre-empted complaint.

## Amendment A1 (2026-11-23) — candidate freeze before the locked M2 evaluation
Reason: the novelty-escalation loop on M1 (rounds 0-4, 13 ideas, log in novelty_escalation_log.md) showed that
the fleet SRCR model is dominated by the expert rule B1; the best development candidate is a budget-split
OR-fusion of B1 with B4 (AE). The original v1 analyses (all baselines, SRCR) are still reported.
Frozen final candidates:
 - C1 = B1 rule (k = 5 K, HC/DHW loops, shortfall only), M1-chosen (tau, c_thr) per budget.
 - C2 = B1 OR B4 (alarm if either alarms); (rule_tau, rule_c, ae_tau, ae_c) chosen on M1 per budget and per AE
   seed from the Pareto fronts (results/round4/orfusion_best_*.csv). On M2 the AE of seed k uses seed k's M1
   operating points; report mean +- SD over seeds 0-9 and seed 0 for the paired tests.
 - All v1 baselines (B1-B5, B7, AE-cond) at their M1-chosen operating points; SRCR (gate + one-sided + local)
   as an ablation, its fleet model trained on ALL M1 substations (seed 0) and applied to M2 (transfer).
Primary M2 analysis: recall at B = 2 with M1 operating points unchanged; achieved M2 FA/sub-yr reported.
Pooled M1+M2 inference (52 faults, 93 substations): paired cluster bootstrap + exact McNemar + Holm, C2 vs
each baseline and C1 vs AE; curve-level endpoint = normalised area under recall vs FA/sub-yr for FA in [0, 6]
(each method's own operating curve over the shared grid; M2 part uses the full M2 curve - descriptive only).
M2 is evaluated exactly once with these frozen specifications; any deviation is logged.

## Amendment A2 (2026-11-24) — analyses added before the locked M2 evaluation
Reason: round 5 (log: novelty_escalation_log.md). M2 detector outputs still NOT evaluated. Candidates C1/C2 unchanged.
Added, pre-registered, run on M2 together with m2_eval.py:
 - F19 protocol-gap analysis (scripts/protocol_gap.py 2): hypotheses H5f, H5g, H5h as written in the log.
 - F18 fault-signature taxonomy (classes A/B/C/U fixed in the log): H5d, H5e, tested on M2 faults only.
Negative/neutral round-5 ideas (F17 calibration, F16 ae_noloop) are reported as development results, not tested on M2.
