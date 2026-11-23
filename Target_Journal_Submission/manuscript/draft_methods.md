# DRAFT — outcome-independent sections (data, evaluation protocol, methods)

Status: written 2026-11-23 while M2 scores were computing, BEFORE any M2 evaluation. No result numbers here.
Results, introduction and discussion are written only after `scripts/m2_eval.py` has run once.
All numbers below come from the dataset description, `experiments/protocol.md` or code constants.

## 2 Data

We use PreDist v1 (Zenodo record 19496480, CC-BY-4.0), released by Fraunhofer IEE with the utility enercity.
It holds 10-minute operational data of 93 district heating (DH) substations from two manufacturers:
manufacturer 1 (M1, 35 substations, about 144 substation-years) and manufacturer 2 (M2, 58 substations,
about 95 substation-years). Each substation logs primary-side temperatures, flow and heat meter values,
secondary-side heating-circuit (HC) and domestic hot water (DHW) temperatures with their setpoints, and
controller states. The dataset lists customer-reported faults with report date, free-text description,
fault label, whether early detection is judged possible (`efd_possible`), and a monitoring-potential score.
It also lists other disturbances (service tasks, activities) and hand-picked normal events.

We treat a fault as a target if `efd_possible` is true and its 7-day detection window lies inside the
monitored span of its substation. This gives 29 target faults on M1 and 24 on M2 [CHECK against
m2_locked_table.csv n_faults before submission].

Split. M1 is the development set: every idea, hyperparameter and alarm threshold was chosen on M1.
M2 is a locked test set. Its detector outputs were not computed until the final candidates were frozen
(protocol Amendment A1), and it was evaluated once. M1 and M2 differ in controller hardware, signal set and
naming, so M2 tests transfer of the alarm settings across manufacturers.

## 3 Evaluation protocol: continuous fleet monitoring

The benchmark protocol of the dataset scores fixed 7-day windows: fault windows and the same number of
hand-picked normal windows. This balanced design hides how often an operator would be disturbed by false
alarms during normal months, which is the main cost of a monitoring system. We therefore score every
10-minute step of every substation, as a control room would see it.

- Monitored span: series start + 30 days (burn-in) to series end.
- Detection window of a target fault: the 7 days before the customer report. A fault is detected if an alarm
  starts in its window. Lead time = report time − first alarm start in the window.
- Exclusion intervals: around every fault row (target or not), from min(anomaly start, report − 7 d) to
  max(anomaly end, report + 1 d); ±2 days around every listed disturbance; and the unlabelled anomalies named in
  the dataset README. Alarms there count neither as true nor as false.
- Alarm episodes: rising edges of the alarm signal, with a 24-hour refractory period (an acknowledged alarm is
  not repeated within a day).
- False alarm: an alarm episode that starts outside all detection windows and exclusion intervals.
- Exposure: monitored days (with data) outside windows and exclusions. False-alarm rate (FA/sub-yr) = false
  alarms / exposure in years.

Faults that customers never reported may exist in normal time, so FA/sub-yr is an upper bound.

Primary metric: fault recall at a budget of B = 2 FA/sub-yr. For a 93-substation fleet this is about
3.6 alarms per week that turn out to be false. Secondary: recall at B = 1 and B = 4; normalised area under
the best-recall-versus-FA curve for FA in [0, 6]; median lead time; alarm precision.

Alarm logic shared by all methods. Each detector returns a score normalised so that 1.0 is its own training
threshold. A criticality counter (as in the EnergyFaultDetector package) increases by one at each step with
score > τ and decreases by one otherwise, floored at zero; missing scores leave it unchanged. An alarm is
active while the counter is at least c_thr. Every method gets the same grid: c_thr ∈ {1, 2, 3, 6, 9, 12, 18,
24, 36, 48, 72, 96, 144, 216, 288} steps and τ ∈ {1, 1.5, 2, 3}. For each budget, the (τ, c_thr) pair with
the highest M1 recall subject to FA/sub-yr ≤ B is chosen and then applied to M2 unchanged; the FA rate that M2
actually reaches is reported, not assumed.

Online training. Per-substation models are retrained every 90 days on up to 730 days of that substation's
own past, leaving out exclusion intervals already known at retraining time, and need at least 14 days of
training data. Scores before the first possible fit are missing. No model sees future data.

## 4 Methods compared

All methods receive the same raw signals, exclusions, alarm logic, grid and evaluation.

- Expert setpoint-shortfall rule (B1). For each HC and DHW loop present (supply temperature vs its setpoint,
  DHW storage temperature vs its setpoint), the score is (setpoint − measurement)/k with k = 5 K; the
  substation score is the maximum over loops. Persistence ("for more than h hours") comes from the shared
  counter. It has no learned parameters.
- Three-sigma (B2): per-signal z-score on own history; score = max |z| / 3.
- Isolation Forest (B3): per substation, 100 trees, threshold = 99th percentile of training scores.
- Autoencoder normal-behaviour model (B4), the dataset's benchmark method re-implemented after the
  EnergyFaultDetector configuration: denoising autoencoder, latent size 0.65 × inputs, Adam (lr 4.5e-4), 10
  epochs, Mahalanobis reconstruction-error score, 99th-percentile threshold; plus a time-conditioned variant.
- Own-history quantile normal-behaviour model (B5): LightGBM quantile regressions (1 %, 50 %, 99 %) of five
  key signals on outdoor temperature, primary supply temperature and calendar context.
- Loop three-sigma (B7): the setpoint residual of each loop z-scored on own history (two-sided).
- SRCR (ablation of our initial proposal): a fleet-shared conditional quantile model of setpoint residuals,
  gated to steady operation, one-sided, trained on all M1 substations and transferred to M2.
- C2 = B1 OR B4: an alarm is raised if either the rule or the autoencoder alarms. The FA budget is split
  between the two by choosing, on M1, the pair of operating points (each from its own Pareto front) with the
  highest recall subject to combined FA/sub-yr ≤ B.

Seeds 0-9 for every stochastic method; C2 operating points are re-selected per autoencoder seed on M1.

## 5 Statistics

Units: fault events for recall, substations for false-alarm rates. Pooled M1 + M2 paired comparisons at
B = 2 (seed 0): paired cluster bootstrap over substations (10,000 resamples) for the difference in recall and
in FA/sub-yr, exact McNemar test on faults, Holm correction across baselines. All 13 ideas tried during
development (log: experiments/novelty_escalation_log.md) are reported.

## TODO after M2
- Results, error analysis, curves, cost translation, scorecard, Reviewer Number Zero, introduction, discussion,
  limitations (unreported faults, two manufacturers from one utility, small number of faults).
