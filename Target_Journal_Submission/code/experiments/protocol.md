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
