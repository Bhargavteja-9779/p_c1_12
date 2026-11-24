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

## Round 1 results (2026-11-23, M1 development)
Ideas counted so far: #1 SRCR-v0, #2 intent channel, #3 delivery channel, #4 max-fusion (3 variants + AE).
- Threshold-free (faults with best pre-report day in top 2% of 45k normal days): execution 9/28, intent 4,
  delivery 4, AE 2, union of 3 channels 16.
- H1a FALSIFIED: intent channel brings only 1/11 parameterisation faults below 2% (event 49).
- H1b SUPPORTED (narrowly): delivery channel brings pump failure 47 (0.11%) and leakage 10 (1.4%) below 2%.
- H1c FALSIFIED: recall at <=2 FA/sub-yr: fused3 0.25, exec+delivery 0.18, exec+intent 0.25, fused+AE 0.18,
  SRCR-v0 0.25, AE (tau swept) 0.21. Max-fusion adds false alarms as fast as detections.
- Diagnosis of false alarms (SRCR-v0, tau 3, c 48): 214 FAs, 5 of 35 substations produce 72%, 18 produce none.
  AE: 223 FAs spread over 32 substations. Inspection: (i) summer, HC1 setpoint 10 degC = heating OFF while
  supply floats at 22-31 degC (sub 35); (ii) substation-specific control style: setpoint swinging 59-76 degC
  within a day (sub 17); (iii) normal DHW storage dips 5 K below setpoint during draw-off (sub 18).

## Round 2 plan (hypotheses written BEFORE running)
 F8 Loop-activity gating (physics): a loop whose setpoint <= 20 degC is OFF; its residual is undefined.
 F7 Fleet-prior -> local-posterior calibration (hierarchical / empirical Bayes): the fleet z of each loop is
    recentred and rescaled with the substation's OWN past (robust median/MAD of daily z over the previous
    60 days, no labels used), weighted by w = n/(n+14) with n = days of own history (zero-shot when n=0).
 F9 Comfort-aligned one-sided residual: for heating and DHW loops only shortfall (measurement below setpoint)
    is scored; the primary return limiter keeps both sides.
 H2a: F8 cuts SRCR false alarms by >= 30% at the round-0 operating point with no lost detection.
 H2b: F7 (+F8) raises M1 recall at <= 2 FA/sub-yr by >= 0.10 absolute over SRCR-v0 (0.25 -> >= 0.35).
 H2c: F9 cuts false alarms by >= 20% at a fixed operating point with <= 1 lost detection.

## Round 2 results (2026-11-23, M1 development; results/round2_srcr_comp.csv)
Ideas counted so far: 4 + #5 gating, #6 local (fleet-prior -> local-posterior) calibration, #7 one-sided = 7
families; 6 composed variants evaluated.
- Recall at <=2 FA/sub-yr: base 0.214, gate 0.250, gate+1s 0.286, gate+local 0.250, gate+1s+local 0.321,
  1s+local 0.321. AE (tau swept) 0.214.
- H2a SUPPORTED: at tau 4 / c_thr 48, gating cuts false alarms 239 -> 121 (-49%) at equal recall (0.214).
- H2c SUPPORTED: one-sided cuts 121 -> 86 (-29%) at equal recall.
- H2b FALSIFIED at the pre-set threshold: best variant +0.071 recall over SRCR-v0 (needed +0.10).
- Strongest effect is on false alarms at matched recall: gate+1s+local reaches recall 0.214 at 0.40 FA/sub-yr;
  AE needs 1.78 FA/sub-yr for the same recall (~4.5x more). Recall differences remain 1-3 faults (n=28): not
  remarkable yet.
- Search for additional labelled DH data (HuggingFace, Zenodo): none besides PreDist. Candidate second domain
  for generality of the setpoint-relative principle: LBNL building FDD datasets (OpenEI, AHU with setpoints).

## Round 3 candidates (to pre-register before running)
 F10 Daily decision unit (operator morning report) instead of 10-min criticality counter.
 F11 Second domain (LBNL AHU FDD) to test whether gated/one-sided/fleet-calibrated setpoint residuals generalise.
 F12 Delivery channel restricted to under-delivery + gating by heating season, fused only with exec channel.
 F13 Substation-level conformal threshold for a guaranteed FA budget (theory, N3).
 F14 Change primary endpoint emphasis to false alarms at matched recall (better powered; pre-register as
     secondary, already listed in protocol amendments).

## Round 3 plan (hypotheses written BEFORE running; 2026-11-23, new machine, scores regenerated from code)
Base score for all round-3 variants: srcr_comp composed with gate + one-sided + local (round-2 best, "R2").
 F10 Daily decision unit (inference/protocol): one decision per substation-day ("morning report").
     Daily score D = 90th percentile of the 10-min score within the calendar day (>= 72 valid steps), alarm
     raised at the END of the day (00:00 next day; conservative for lead time). Threshold swept on M1.
 F13 Substation-level conformal threshold (theory): alarm on day d if D_d > q_(1-alpha) of the substation's OWN
     past normal daily scores (previous 365 days, known exclusions removed; split-conformal rank rule
     k = ceil((n+1)(1-alpha))). If n < 60 own days, the calibration set is the pooled daily scores of the OTHER
     cross-fitting folds' substations (fleet prior). alpha = B / 365 per day for budget B FA/sub-yr.
     Guarantee (exchangeable normal days): P(false alarm on a normal day) <= alpha -> E[FA/sub-yr] <= B.
 F12 Under-delivery channel: delivery channel restricted to the low side of heat power (one-sided), and only
     on heating-season days (24-h mean outdoor temperature < 15 degC); fused with R2 at the daily level by
     max of fleet-calibrated surprise levels (as fusion.py, daily).
 H3a (F10): at <= 2 FA/sub-yr, daily unit recall >= R2 10-min recall (0.321); falsified if lower.
 H3b (F13): (i) achieved M1 FA/sub-yr within [0.5B, 1.5B] for B in {1, 2, 4} (calibration validity);
     (ii) share of false alarms from the 5 worst substations drops from 72% (round 1) to < 40%;
     (iii) recall at the B = 2 conformal setting >= 0.36. Falsified per item.
 H3c (F12): adding the under-delivery channel to F10 raises detected faults at <= 2 FA/sub-yr by >= 2
     (absolute count) versus F10 alone. Falsified otherwise.
 F11 (second domain, LBNL AHU) deferred to round 4: needs a separate data pipeline.

## Round 3 results (2026-11-23, M1 development; results/round3/round3_srcr_comp__v_gate_1s_local.csv)
Reproducibility: all M1 scores regenerated from code on a new machine; round-2 table reproduced exactly.
Ideas counted so far: 7 + #8 daily unit, #9 conformal per-substation threshold (+1 post-hoc fallback variant,
counted), #10 under-delivery channel = 10 families (11 with the post-hoc variant).
- H3a SUPPORTED only weakly (no gain): daily unit recall at <=2 FA/sub-yr 0.321 = R2 10-min 0.321, but with more
  false alarms (271 vs 186). B=1: 0.214 = 0.214; B=4: 0.357 = 0.357. The daily unit is an equivalent, simpler
  operator interface, not an improvement.
- H3b (i) PARTLY FALSIFIED: achieved FA/sub-yr 0.40 (B=1, below 0.5B because 70% of days have too little own
  history for alpha=1/365), 1.45 (B=2, valid), 3.14 (B=4, valid). (ii) SUPPORTED: share of false alarms from the
  5 worst substations 0.33 (B=2) vs 0.66 with a global daily threshold. (iii) FALSIFIED: recall 0.179 at B=2
  (post-hoc fleet fallback: 0.214). Conformal thresholds equalise the alarm burden but cost recall.
- Diagnosis: top-5 FA substations (35, 21, 18, 33, 8) hold 66% of FAs but only 6/28 target faults; Spearman
  rho(FA count, target faults) = 0.30 (p = 0.08). Own-past thresholds absorb slowly developing degradation
  (a fault's precursor becomes part of the 'normal' calibration set) -> lost detections.
- H3c FALSIFIED: R2 + under-delivery at <=2 FA/sub-yr recall 0.214 (-3 faults vs F10). Post-hoc observation
  (NOT pre-registered, not claimable): at B=4 the fusion reaches 0.464 vs 0.357 (+3 faults).
- Verdict round 3: no gain on the primary endpoint. Rounds without primary gain: 1 (r1), 0 (r2: FA gain),
  1 (r3). Not remarkable yet.

## Diagnosis after round 3: full M1 baseline table (results/m1_table.csv, m1_curves.csv; same tau/c grid for all)
Min FA/sub-yr needed to reach recall 0.214 / 0.286 / 0.321 (6 / 8 / 9 of 28 faults):
  B1 rule (HC/DHW shortfall vs setpoint, no learning) 0.15 / 1.08 / 1.08 ; SRCR R2 0.40 / 1.48 / 1.48 ;
  sigma3 1.35 / 2.74 / 2.74 ; loop3s 1.12 / 3.56 / 3.56 ; AE (benchmark) 1.78 / 5.63 / 5.63 ;
  AE-cond 2.25 / 4.05 / 4.05 ; IForest 2.42 / 18.3 / 18.3 ; qnbm 1.89(0.179) / 3.70(0.321).
- THE EXPERT RULE DOMINATES EVERY LEARNED METHOD, INCLUDING SRCR. Rule and SRCR detect exactly the same 9 faults
  (44, 57, 1, 62, 38, 7, 69, 15, 10); SRCR adds no detection and more false alarms. The fleet quantile model is
  therefore NOT a contribution on M1. What carries the signal is the setpoint-relative, one-sided (shortfall)
  representation itself, which the rule already has.
- AE detects 6 faults, 4 of which neither rule nor SRCR detect: 20 (safety valve water loss), 53 (shut-off valve
  closed), 49 (DHW night-mode parameterisation), 47 (heating pump blocked). Union rule|AE = 13/28.
- Consequence for the story (honest pivot, N5 + N7): under deployment-realistic continuous evaluation, a
  transparent setpoint-shortfall rule beats the published deep NBM benchmark by ~5x fewer false alarms at equal
  recall, and the learned model's value lies in a COMPLEMENTARY fault set (hydraulic / pump / valve faults that
  do not show as a tracking shortfall).

## Round 4 plan (hypotheses written BEFORE running)
 F15 Budget-split OR-fusion: alarm = rule alarm OR learned-detector alarm; the FA budget B is split between the
     two by choosing the pair of operating points (each from its own Pareto front on M1) maximising recall subject
     to combined FA <= B. Partners pre-registered: AE (benchmark), underdel, qnbm (3 ideas, all counted).
 F16 Residualised learned detector: train/score the AE only on time when the rule is quiet... (NOT run in round 4;
     listed for round 5 if F15 supported).
 H4a: best F15 pair reaches recall >= 0.393 (11/28) at <= 2 FA/sub-yr (rule alone: 0.321). Falsified otherwise.
 H4b: the rule+AE pair alone reaches >= 0.357 (10/28) at <= 2 FA/sub-yr. Falsified otherwise.
 Multiplicity: 3 partners x 3 budgets reported; final candidate tested once on M2.

## Round 4 results (2026-11-23, M1; results/round4/orfusion_best_ae_underdel_qnbm.csv)
Ideas counted: 10 + 3 OR-fusion partners = 13 (+1 post-hoc conformal variant).
Pareto points per method: rule 6, AE 8, underdel 6, qnbm 9 -> 48 / 36 / 54 pairs searched (extra tuning freedom
vs single methods: optimism to be checked on M2).
 B=1: rule+AE 0.321 @0.50 ; rule+qnbm 0.321 @0.72 ; rule+underdel 0.321 @0.66   (rule alone 0.286 @0.35)
 B=2: rule+AE 0.393 @1.44 ; rule+qnbm 0.393 @1.98 ; rule+underdel 0.357 @1.33   (rule alone 0.321 @1.08)
 B=4: rule+AE 0.429 @2.02 ; rule+qnbm 0.393 @1.98 ; rule+underdel 0.429 @2.92   (rule alone 0.321)
- H4a SUPPORTED: rule+AE and rule+qnbm reach 0.393 (11/28) at <= 2 FA/sub-yr.
- H4b SUPPORTED: rule+AE 0.393 >= 0.357.
- Effect sizes are small in absolute faults (+2 over rule, +5 over AE alone at B=2; n = 28) -> needs bootstrap
  CIs, seeds 0-9 for AE, and the locked M2 test before any claim.
- Candidate final methods (frozen after this round): C1 = rule alone; C2 = rule OR AE with M1-chosen operating
  points per budget. Both need no cross-manufacturer model transfer (rule has no parameters to learn; AE is
  per-substation online) -> only the operating points transfer from M1 to M2.

## M1 development statistics at B = 2 (results/stats/m1_paired_B2.csv; cluster bootstrap 10k over 35 substations,
## exact McNemar on 28 faults, Holm over baselines)
- C2 (rule OR AE) vs AE benchmark: +0.179 recall (95% CI 0.000 to 0.350), 6 vs 1 discordant faults, p = 0.125
  (Holm 0.625), FA -0.34/sub-yr (CI -0.75 to 0.08). vs rule: +0.071 (CI -0.067 to 0.227), p = 0.625.
- C1 (rule) vs AE: +0.107 (CI -0.133 to 0.333) at 0.69 fewer FA/sub-yr (CI -1.72 to 0.67).
- No comparison survives Holm at n = 28 faults. Recall-at-budget is underpowered on one manufacturer; the
  primary inference must pool M1 + M2 (52 faults) and use the paired curve-level secondary endpoint (normalised
  area under recall-vs-FA for B in [0, 6]) as pre-registered. Not remarkable on M1 alone.

## Seeds 0-9 on M1 (AE retrained per seed; rule deterministic; C2 operating points re-selected per seed on M1)
 recall mean +- SD (min-max) over 10 seeds:
  AE alone  B=1 0.13 (seeds 1-9: 0.127+-0.026) ; B=2 0.183+-0.045 (0.107-0.250; seed 0 = 0.214) ; B=4 0.313+-0.024
  C2 rule OR AE  B=1 0.343+-0.018 (0.321-0.357) ; B=2 0.382+-0.017 (0.357-0.393) ; B=4 0.429+-0.024 (0.393-0.464)
  rule alone B=1 0.286 ; B=2 0.321 ; B=4 0.321
 C2 >= rule in 10/10 seeds at every budget; C2 - AE at B=2 ~ +0.20 in every seed. Stable across seeds.
 Files: results/m1_table_aeseeds.csv, results/round4/orfusion_best_ae_seed1_..._ae_seed9.csv

## M2 access log
- 2026-11-23: after Amendment A1 freeze, M2 detector SCORES computed for all frozen methods (no evaluation yet).
- 2026-11-23: M2 score run crashed for sigma3 and IForest on a substation whose training window had no usable
  numeric column. Fix: such windows get no score (NaN), as with any model without training data. Does not touch
  M1 (never triggered) nor any frozen operating point. No M2 evaluation had been run.

## Round 5 plan (written 2026-11-24 BEFORE computing any event-protocol number; account 3)
Diagnosis: the method story (rule, rule OR AE) is useful but not remarkable; the strongest candidate core idea
is an evaluation FINDING (N5 + N7): the published balanced event-window protocol may rank detectors differently
from deployment-realistic continuous monitoring. If true and explained, this is a reusable 2-sentence idea:
"Balanced event benchmarks score each detector on a few hand-picked normal weeks, so they cannot see the
false-alarm rate per asset-year that decides whether a detector is usable; rankings under the two protocols
can disagree." It needs (i) a measured ranking disagreement, (ii) a mechanism, (iii) a second dataset.
Fix families considered: F17 protocol-inversion study (this round); F18 second dataset (CARE wind SCADA,
Zenodo 14958989, 6 GB) for generality; F19 analytical base-rate model linking event F0.5 to deployed
precision; F20 residualised AE (F16, deferred); F21 per-fault-type routing (rule vs AE by loop activity).
Event protocol E (re-implemented from the PreDist paper description): events = target faults (window
[report - 7 d, report)) + normal_events.csv windows; event predicted positive if the criticality counter of the
method's online score reaches c_thr at any step in the window; eventwise precision/recall/F0.5; both
(a) benchmark-style: best F0.5 over the SAME (tau, c_thr) grid tuned on the evaluated manufacturer's events,
(b) at the method's M1 continuous operating point for B = 2.
Methods: rule, sigma3, loop3s, iforest, qnbm, ae, ae_cond, srcr_comp__v_gate_1s_local, underdel (seed 0), M1.
 H5a: Kendall tau between method rankings by E-(a) F0.5 and by continuous recall at B = 2 is < 0.5.
 H5b: at least one learned detector scores a higher E-(a) F0.5 than the rule although the rule has higher
      continuous recall at B = 2 (a ranking inversion of the benchmark's own detector family vs the rule).
 H5c: for every method, event precision under E-(a) exceeds deployed alarm precision (continuous, B = 2) by
      a factor >= 5.
All three falsifiable; reported regardless of outcome. M2 events are evaluated only inside the locked M2 run.
