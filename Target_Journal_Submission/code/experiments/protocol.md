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

## Amendments (dated; original v1 analyses are still reported)
- A1 (2026-11-23, before round 2; recorded late on 2026-11-23): tau grid extended to {1, 1.5, 2, 3, 4} for
  ALL methods (runner.TAU_GRID). Evaluable M1 targets as computed by the harness = 28 (v1 text said 29).
- A2 (2026-11-23, after D6 round 4 on M1, before any M2 scoring): method candidate fixed as SRCR-C
  (comfort loops only, setpoint gating, one-sided shortfall, fleet-prior -> local calibration, criticality
  counter). Because "comfort-only" knowledge was found on M1, two baselines receive the same knowledge:
  B7c loop three-sigma restricted to comfort loops, gated and one-sided (own history, no fleet model) and
  B4c autoencoder restricted to comfort signals (loop measurements, setpoints, outdoor temperature).
- A3 (2026-11-23, added AFTER round-4 results were seen on M1, so labelled post hoc): secondary endpoint
  "minimum false alarms per substation-year needed to reach recall r" for r in the recall levels that both
  methods reach, with cluster-bootstrap CI over substations. The v1 primary endpoint (recall at B = 2) is
  unchanged and remains primary.
- A4 (2026-11-23, before ANY detector output on M2; only M2 column availability was checked: hc1 loop in
  58/58 substations, dhw_sup 14, dhw_sto 13, p_ret 19): FACTORIAL ANALYSIS fixed as the primary question.
  Cells: SCOPE {comfort loops, all signals} x REPRESENTATION {relative to setpoint, absolute} x MODEL.
    comfort x relative : rule (B1), loop3s_c (B7c), SRCR-C (fleet quantile ML)
    all     x relative : loop3s (B7), SRCR gate+1s+local with p_ret
    comfort x absolute : ae_comfort (B4c)
    all     x absolute : sigma3 (B2), iforest (B3), qnbm (B5), ae (B4), ae_cond (B4)
  M2 procedure: per-substation methods run online on M2 exactly as on M1; fleet models trained on ALL M1
  normal data (seeds 0-9), applied to M2 unchanged; every method uses its M1-chosen (tau, c_thr) for
  B in {1, 2, 4}; realised M2 FA rates reported. Pooled M1+M2 numbers reported as secondary.
  Pre-registered hypotheses (tested on M2, Holm-corrected within each family):
   HF1 SCOPE: at matched recall, comfort-scope cells need fewer false alarms than all-signal cells with the
       same representation and model class (SRCR-C vs SRCR-all; loop3s_c vs loop3s; ae_comfort vs ae):
       paired per-fault log-rank Wilcoxon, and FA ratio with cluster-bootstrap 95% CI excluding 1.
   HF2 REPRESENTATION: comfort x relative cells beat comfort x absolute (loop3s_c and SRCR-C vs ae_comfort).
   HF3 MODEL: within comfort x relative, model class matters little: we report rule vs loop3s_c vs SRCR-C
       differences with CIs; we do NOT claim equivalence (n too small), only absence/presence of a
       significant difference.
   HF4 PRIMARY ENDPOINT (v1): recall at B = 2 on M2, SRCR-C vs every baseline (McNemar exact + paired
       cluster bootstrap, Holm). Expected direction: SRCR-C >= AE; no hypothesis vs rule.
