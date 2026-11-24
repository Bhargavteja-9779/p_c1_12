<!-- DRAFT (session 3). Results-independent sections. Every number is from code/results/dataset_summary.md or the code. -->

## 3. Data

### 3.1 The PreDist dataset
We use PreDist [REF dataset paper 10.1016/j.energy.2026.141178; Zenodo 10.5281/zenodo.19496480], a public, CC-BY-4.0 dataset of operational data from 93 customer substations of a German district heating network, recorded at 10-min resolution and labelled from the operator's service records. Substations come from two controller manufacturers, which record different signal sets and controller logic. Table 1 summarises both populations.

**Table 1.** Data used in this study (computed from the raw files).

| | Manufacturer 1 (development) | Manufacturer 2 (locked test) |
|---|---|---|
| Substations | 35 | 58 |
| Period covered | 2012-03 to 2020-07 | 2015-10 to 2020-04 |
| Series length, days, median (range) | 1708 (236-3043) | 182 (33-1632) |
| Substation-years of data | 144 | 95 |
| Signals per substation (median) | 15 | 16 |
| Fault reports / early-detectable / evaluable target faults | 33 / 29 / 28 | 40 / 26 / 25 |
| Disturbance records (reports, tasks, activities) | 165 | 163 |
| Substations with heating-circuit / DHW-supply / DHW-storage / primary-return loop | 35 / 25 / 17 / 14 | 58 / 14 / 13 / 19 |

Each fault report carries the report date, an optional expert-estimated anomaly start and end, a fault label, and a flag stating whether the fault was judged detectable from the recorded signals before the report (`efd_possible`). Following the dataset authors, the target faults are the early-detectable ones. A target is *evaluable* when its 7-day detection window lies inside the monitored span of its substation (Section 5.1). The most frequent target labels are incorrect parameterisation of the control unit (8 of 29) and heating-circuit pump failure (4) for manufacturer 1, and leakage (5), incorrect setting of the differential-pressure regulator (4) and unknown (4) for manufacturer 2.

### 3.2 Development and locked test split
All method development used manufacturer 1 (M1) only. Manufacturer 2 (M2) was locked before any detector was run (lock file dated 2026-11-23, Supplementary S1): no model, threshold or idea was chosen with M2 data, and every final method was evaluated on M2 once, using alarm parameters chosen on M1. This makes the M2 result a test of transfer to a different controller manufacturer, a different signal set and, as Table 1 shows, much shorter histories (median 182 days against 1708 days on M1). An exploratory pilot printed per-fault signal statistics for both manufacturers before the lock; no detector, threshold or model was fitted in it, and it is disclosed in Supplementary S1.

## 4. Methods

### 4.1 Control loops of a substation
A substation controller states what it wants and the plant shows what it delivers. For each control loop *l* we pair a measurement *y_l(t)* with its setpoint *s_l(t)* and use the tracking residual

  e_l(t) = y_l(t) − s_l(t).   (1)

PreDist contains up to six such loops (Table 1): the heating-circuit supply temperature (hc1 and, where present, two sub-circuits), the domestic hot water (DHW) supply and storage temperatures, and the primary return temperature with its limiter setpoint (p_ret). A loop is used for a substation when both signals are available for more than 20% of the time. We call the heating-circuit and DHW loops *comfort loops*, because their failure is what a customer experiences (cold radiators, cold tap water). The primary-return limiter is an *efficiency loop*: a high return temperature costs the network money but is not felt by the customer.

The motivation for (1) is that benign changes of intent (night set-back, heating-curve edits, summer shut-down, service staff changing a setpoint) move measurement and setpoint together, while faults in pumps, valves, regulators and heat exchangers break the loop and make e_l drift, typically as a persistent *shortfall* (e_l < 0).

### 4.2 Detectors compared
All detectors receive the same raw signals, the same exclusion intervals and the same alarm logic (Section 4.4), and each outputs a score normalised so that 1.0 is its own nominal threshold. They are grouped by three factors (Table 2): **scope** (comfort loops only, or all signals), **representation** (relative to the setpoint, or absolute signal values) and **model** (rule, own-history statistics, own-history ML, autoencoder, fleet-shared ML).

**Table 2.** Factorial design: 11 detector cells.

| Scope | Representation | Model | Cell |
|---|---|---|---|
| comfort | relative | expert rule | Rule |
| comfort | relative | own-history statistics | Loop-3σ-C |
| comfort | relative | fleet quantile ML | SRCR-C (proposed) |
| all loops | relative | own-history statistics | Loop-3σ |
| all loops | relative | fleet quantile ML | SRCR-all |
| comfort | absolute | autoencoder | AE-comfort |
| all signals | absolute | own-history statistics | 3σ |
| all signals | absolute | isolation forest | iForest |
| all signals | absolute | own-history quantile NBM | qNBM |
| all signals | absolute | autoencoder (benchmark) | AE |
| all signals | absolute | conditional autoencoder | AE-cond |

*Rule.* The expert rule of practice: a comfort loop delivers more than k = 5 K below its setpoint; score = shortfall / k. "For more than h hours" is provided by the shared persistence counter (Section 4.4).

*3σ and Loop-3σ.* Per-signal (3σ) or per-loop-residual (Loop-3σ) absolute z-scores from the substation's own training data, divided by 3. Loop-3σ-C restricts Loop-3σ to comfort loops, ignores a loop while its setpoint is at or below 20 °C (heating off or frost protection), and scores only shortfall.

*iForest.* Isolation forest [REF Liu 2008] with 100 trees per substation on all numeric non-counter signals (mean-imputed, at most 50 000 training rows); score divided by the 99th percentile of training scores.

*qNBM.* An own-history quantile normal-behaviour model in the spirit of [REF Hermans 2024]: for five key signals, LightGBM [REF Ke 2017] quantile models (1%, 50%, 99%) conditioned on outdoor temperature, primary supply temperature and calendar features; the score is the normalised band exceedance (Eq. 3).

*AE, AE-cond, AE-comfort.* The autoencoder normal-behaviour model of the PreDist benchmark [REF 10.1016/j.energy.2026.141178], re-implemented with the published M1 configuration: hidden layers 64-32, latent size 0.65 × number of inputs, learning rate 4.5·10⁻⁴, input noise 0.05, batch 256, Mahalanobis distance of the reconstruction error, threshold at the 99th percentile of training scores, and the EnergyFaultDetector preprocessing (columns with more than 80% missing or constant removed, mean imputation, 0.1/99.9 percentile clipping, standard scaling). AE-cond adds hour-of-day and day-of-week encodings to encoder and decoder; AE-comfort uses only comfort-loop signals and outdoor temperature.

All per-substation detectors are trained *online* (Section 4.4); they need the substation's own history.

### 4.3 Proposed: setpoint-relative comfort-loop residuals with a fleet quantile model (SRCR-C)
SRCR-C asks, for each comfort loop and each 10-min step, whether the tracking residual (1) lies outside the band that *other* substations show in normal operation under the same context.

*Fleet quantile model.* For each loop family (heating circuit, DHW supply, DHW storage, primary return) three LightGBM quantile regressors (α = 0.02, 0.5, 0.98; 200 trees, learning rate 0.05, 31 leaves, at least 200 samples per leaf) are fitted on normal-operation residuals pooled across training substations, with context features: setpoint level, setpoint change over 1 h and 6 h, distance below the 6-h setpoint maximum, outdoor temperature and its 24-h mean, primary supply temperature, headroom (primary supply minus setpoint), and hour-of-day and day-of-year encodings. Training excludes all fault windows and exclusion intervals and, with gating, steps whose setpoint is at or below 20 °C; at most 20 000 rows per substation are sampled. Because the model is fleet-shared, a new substation is scored from its first day without any own history.

*Normalised exceedance.* With predicted quantiles q_lo, q_med, q_hi,

  z_l^−(t) = (q_lo − e_l) / max(q_med − q_lo, 0.5 K),   z_l^+(t) = (e_l − q_hi) / max(q_hi − q_med, 0.5 K).   (2)

*Composition.* The substation score is

  S(t) = 1 + max_{l ∈ comfort loops, s_l(t) > 20 °C} ẑ_l^−(t),   (3)

i.e. only comfort loops, only while the loop is on (gating), and only the shortfall side (one-sided). The primary-return loop is dropped.

*Local calibration.* ẑ_l is z_l^− recentred and rescaled with the substation's own *past* daily medians: over the previous 60 days, robust centre m and scale (1.4826 × MAD, at least 0.5), mixed with the fleet prior (centre 0, scale 1) by a shrinkage weight w = n/(n + 14), where n is the number of past days with data. With no history, w = 0 and the fleet model is used unchanged; only past data are used, so the score is causal.

*SRCR-all* is the same model with the primary-return loop kept (two-sided). The components of Eq. (3) (gating, one-sided scoring, local calibration, loop scope) are ablated in Section 6.

*Cross-fitting on M1.* On M1 the fleet model is cross-fitted: substations are split into 5 groups, and each substation is scored by a model trained on the other 4 groups, so no substation is ever scored by a model that saw its own data. For the locked test, one model per seed is trained on all M1 normal data and applied unchanged to M2.

### 4.4 Online training and alarm logic (all detectors)
*Online training.* Per-substation detectors are retrained every 90 days on at most 730 days of the substation's own past, excluding exclusion intervals that were already known at the retraining time (a fault report whose window started more than 7 days earlier, or a closed interval). No hand-picked training windows and no knowledge of future reports are used. A model is fitted once at least 7 days of training data exist; earlier steps have no score.

*Persistence (criticality) counter.* As in the PreDist benchmark and EnergyFaultDetector, a counter k(t) increases by 1 when S(t) > τ and decreases by 1 (floored at 0) otherwise; missing scores leave it unchanged. An alarm is active while k(t) ≥ c. All detectors share the same grid τ ∈ {1, 1.5, 2, 3, 4} × c ∈ {1, 2, 3, 6, 9, 12, 18, 24, 36, 48, 72, 96, 144, 216, 288} steps (10 min to 48 h of net exceedance), 75 operating points per detector.

## 5. Evaluation protocol

### 5.1 Continuous monitoring
The benchmark evaluation of PreDist scores 7-day windows around 55 fault events and 65 hand-picked normal events, balanced 50/50. An operator, however, sees every step of every substation, every day. We therefore score every monitored 10-min step of every substation after a 30-day burn-in:

- *Detection.* A target fault is detected if an alarm starts within the 7 days before its report; lead time = report time − first alarm start in the window.
- *Alarm episodes.* Alarm starts are rising edges of the alarm signal; a new start within 24 h of the previous one is not counted (an acknowledged alarm is not repeated within a day).
- *Exclusions.* Alarms in intervals around every fault report (from the earlier of the expert anomaly start and the window start to the later of the anomaly end and report + 1 day), around every disturbance record (± 2 days), and in the anomalies listed as known in the dataset documentation count neither as true nor as false alarms.
- *False alarm.* An alarm start outside all detection windows and exclusions.
- *Exposure.* Monitored days whose midday lies outside windows and exclusions; false alarms are reported per substation-year.

Unreported faults exist in "normal" time, so measured false-alarm rates are upper bounds; Section 7 examines what the false alarms are.

### 5.2 Endpoints and operating points
The primary endpoint is fault recall at a false-alarm budget of B = 2 false alarms per substation-year; B = 1 and B = 4 are secondary. For each detector and budget, the operating point (τ, c) with the highest M1 recall subject to a false-alarm rate ≤ B is chosen on M1 and applied unchanged to M2, where the realised false-alarm rate is reported. Threshold-free comparisons use, for each fault, the rank of its strongest pre-report day among all normal substation-days of the population (daily score = maximum over the day of the 6-h rolling mean); a rank fraction r means that a threshold catching the fault would produce about 365·r false-alarm days per substation-year.

### 5.3 Pre-registered hypotheses and statistics
The protocol (Supplementary S2) was fixed before any detector was run, and every later amendment is dated; amendments A4 and A5 fixed the hypotheses below and the full analysis code before any M2 detector output existed.

- **HF1 (scope).** Comfort-scope cells need fewer false alarms than all-signal cells with the same representation and model (SRCR-C vs SRCR-all; Loop-3σ-C vs Loop-3σ; AE-comfort vs AE).
- **HF2 (representation).** Comfort/relative cells beat the comfort/absolute cell (Loop-3σ-C and SRCR-C vs AE-comfort).
- **HF3 (model).** Within comfort/relative, differences between rule, own-history statistics and the fleet model are reported with confidence intervals; no equivalence is claimed.
- **HF4 (primary endpoint).** Recall at B = 2 on M2, SRCR-C vs every other cell.

HF1-HF3 use the paired per-fault Wilcoxon signed-rank test on log₁₀ rank fractions and the ratio of false-alarm rates at matched recall (the recall reached by the first method of the pair at its M1-chosen B = 2 operating point; rates with a +0.5 false-alarm continuity correction), with 95% confidence intervals from a cluster bootstrap over substations (2000 replicates). HF4 uses the exact McNemar test on per-fault detections and a cluster-bootstrap CI of the recall difference. Holm correction is applied within HF1, HF2 and HF4. The fleet model is run with seeds 0-9 (seed 0 is the pre-specified primary analysis); per-substation stochastic baselines use seed 0.

### 5.4 Development history
Method development on M1 followed a logged escalation loop with hypotheses written before each round (Supplementary S3). Fourteen ideas were tried; those falsified include a daily decision unit, conformal false-alarm budgets, under-delivery fusion and CUSUM alarm logic. They are reported in Section 6 to make the search visible.
