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

## Round 3 plan (hypotheses written BEFORE running, 2026-11-23, new machine; M1 only)
Diagnosis carried from round 2: recall differences are 1-3 faults (n=28) and cannot carry the paper; the
better-powered and operator-relevant quantity is the false-alarm rate, and in particular whether an operator
can SET it in advance (alarm budget) and get it on unseen substations / an unseen manufacturer.
Families tested this round (ideas #8-#11):
 F10 Daily decision unit: D_d = 95th percentile of the 10-min composed SRCR score (gate+1s+local) over day d
     (NaN if < 72 valid steps); alarm active during day d+1 if D_d > thr (causal; consecutive alarm days merge
     into one episode, then 24 h refractory as before).
 F13 Fleet conformal alarm budget: thr = empirical (1 - alpha) quantile of D over NORMAL days of the training
     folds' substations (cross-fitted, never the substation itself), alpha = B / 365.25 for budget B false
     alarms per substation-year. Zero-shot (no own history needed). Same rule applied to the AE baseline
     (AE score daily 95th percentile) so the comparison is fair.
 F13b Substation-adaptive conformal: thr_s(d) = max(fleet thr, own-past (1 - alpha) quantile of D over the
     substation's previous normal days, used only once >= 1/alpha own normal days exist).
 F12 Under-delivery channel: delivery channel restricted to 'low' heat power / flow during heating season
     (outdoor 24 h mean < 12 degC), mapped to a fleet-calibrated level and fused by max with the execution
     channel at the daily unit.
 F11 Second domain (LBNL AHU FDD data) -> deferred: checked only for reachability this round.
Pre-registered hypotheses:
 H3a (F10): daily unit + threshold sweep reaches recall >= 0.321 at <= 2 FA/sub-yr AND needs >= 30% fewer
      false alarms than the 10-min counter version at matched recall 0.214. Falsified if either fails.
 H3b (F13): on held-out folds the realised FA/sub-yr for B in {1, 2, 4} lies in [0.5 B, 1.25 B] for SRCR;
      reported for AE too (no hypothesis on AE). Falsified if any budget falls outside.
 H3c (F13b): adaptive conformal lowers the share of false alarms coming from the 5 worst substations by
      >= 15 percentage points vs fleet conformal at B = 2, with <= 1 lost detection. Falsified otherwise.
 H3d (F12): under-delivery fusion adds >= 2 detected faults at the realised <= 2 FA/sub-yr point over F10
      alone. Falsified otherwise.

## Round 3 results (2026-11-23, M1 development; results/round3_*.csv, src/evaluation/daily.py)
Ideas counted so far: 7 + #8 daily unit, #9 fleet conformal budget, #10 adaptive conformal, #11 under-delivery
fusion = 11. (Round-2 numbers reproduced exactly on the rebuilt machine: 0.321 recall at 1.48 FA/sub-yr.)
- H3a FALSIFIED: daily unit best recall at <= 2 FA/sub-yr = 0.286 (10-min counter 0.321); at recall 0.214 it
  needs 1.56 FA/sub-yr vs 0.40 for the counter (worse, not better).
- H3b FALSIFIED (narrowly): realised FA/sub-yr with cross-fitted fleet conformal thresholds: B=1 -> 0.79,
  B=2 -> 1.33, B=4 -> 1.96 (0.49 B, just below the 0.5 B bound). Budgets are respected (never exceeded), but
  conservative because consecutive alarm days merge into one episode.
- H3c FALSIFIED: adaptive thresholds reduce top-5 share only 0.87 -> 0.83 at B=2 and lose 1 detection
  (0.179 -> 0.143) while halving false alarms.
- H3d FALSIFIED: under-delivery fusion at <= 2 FA/sub-yr gives recall 0.214 (vs 0.286 for exec alone, daily
  unit). Under-delivery alone: 0.107 at 0.48 FA/sub-yr.
- Most important observation: false alarms are extremely concentrated. At budgets <= 1/sub-yr, 5 of 35
  substations produce 90-100% of SRCR false alarms. Next step: check whether these are unlabelled persistent
  anomalies (label noise in 'normal' time) and whether AE flags the same substations.

## Round 4 plan (hypotheses written BEFORE running, 2026-11-23; M1 only)
Diagnosis: in raw components, the primary-return limiter loop (p_ret, two-sided) has the highest exceedance
rate (sub 18: 1.5% of steps z>3; sub 35: 0.9%, all in the heating season) while comfort loops rarely exceed.
High primary return temperature is an efficiency problem that customers do not report (no comfort loss), so
it is plausibly NOT a target-fault signal. Families:
 F15 Comfort-only execution channel: drop p_ret (keep hc*, dhw_* shortfall, gated, local-calibrated).
 F16 p_ret low-side only (return far BELOW limit = valve stuck closed / no flow) kept, high side dropped.
 F17 CUSUM alarm logic on z: S_t = max(0, S_{t-1} + min(z_t, 10) - k), alarm while S_t >= h; k in {0,1,2},
     h on a 12-value grid matched to the counter grid budget (same number of operating points per method).
 H4a: F15 or F16 reduces M1 false alarms by >= 30% at matched recall 0.214 vs gate+1s+local, with no lost
      detection at the <= 2 FA/sub-yr operating point (recall stays >= 0.321). Falsified otherwise.
 H4b: F17 raises recall at <= 2 FA/sub-yr by >= 0.07 (2 faults) over the counter for the best variant of H4a.

## Round 4 results (2026-11-23, M1 development; results/round2_srcr_comp_v_g1l_noret-v_g1l_retlow.csv,
## results/round4_cusum_*.csv, results/matched_recall_r4_vs_ae.csv)
Ideas counted so far: 11 + #12 comfort-only (drop p_ret), #13 p_ret low-side only, #14 CUSUM = 14.
- H4a SUPPORTED: comfort-only (gate + one-sided + local, p_ret dropped) needs 0.18 FA/sub-yr for recall 0.214
  (gate+1s+local: 0.40, -55%) and keeps recall 0.357 at <= 2 FA/sub-yr (no lost detection).
  Recall at budgets B = 1/2/4: 0.321 / 0.357 / 0.357 (0.65 / 1.44 / 1.44 FA/sub-yr realised).
  p_ret low-side only: 0.286 / 0.357 / 0.393 — between the two.
- H4b FALSIFIED: CUSUM on the comfort-only score reaches only 0.286 at <= 2 FA/sub-yr (counter 0.357).
- Versus AE (re-run on this machine, same grid): minimum FA/sub-yr to reach recall 0.214: AE 1.78 vs
  comfort-only SRCR 0.18 (~10x); recall 0.321: AE 5.63 vs 0.65 (~8.7x). Recall at <= 1 FA/sub-yr: 0.321 vs 0.143.
- Interpretation (to test, not yet claimed): the primary return limiter reacts to efficiency problems
  (high return temperature) that do not reach customers and are not reported; scoring only the loops that
  carry comfort makes alarms match what customers report. This is a 2-sentence reusable idea:
  "Score only the control loops whose failure the stakeholder experiences, relative to the controller's own
  setpoint, with a fleet model that needs no own history."
- DECISION: fix the method candidate = SRCR-C (comfort loops, gated, one-sided, fleet-prior -> local
  calibration, criticality counter). Next: seeds 0-9, all baselines on M1, novelty map + scorecard, then the
  single locked evaluation on M2.
