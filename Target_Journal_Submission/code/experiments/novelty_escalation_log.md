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

## Desk-rejection check after round 4: "does a simpler method work?" (2026-11-23, M1; results/matched_recall_fast_baselines.csv)
Minimum FA/sub-yr needed to reach a recall level (same tau x c_thr grid for all):
| recall | SRCR-C | rule (comfort shortfall > 5 K) | loop3s_c (own-history, comfort, gated, 1-sided) | loop3s | sigma3 | AE |
| 0.214  | 0.18   | 0.15 | 0.14 | 1.12 | 1.35 | 1.78 |
| 0.250  | 0.60   | 0.17 | 0.44 | 1.62 | 1.37 | 2.15 |
| 0.321  | 0.65   | 1.08 | 3.53 | 3.56 | 2.74 | 5.63 |
| 0.357  | 1.44   | 11.5 | 20.5 | 3.84 | 5.06 | 5.63 |
- HONEST FINDING: the large gain over AE comes mostly from WHAT is monitored (comfort loops, relative to the
  setpoint), not from the fleet model. The expert rule is as good as SRCR-C up to recall 0.25. SRCR-C is only
  better at higher recall (0.321-0.357), i.e. 1-2 extra faults (n = 28) — not statistically remarkable.
- Consequence for the paper: the learned fleet model cannot be sold as the core novelty. Candidate core
  contribution shifts to an evaluation finding (N5 + N7): under deployment-realistic continuous monitoring,
  deep normal-behaviour models (the published benchmark) raise ~10x more false alarms than a setpoint-relative
  comfort rule at equal recall. This must be confirmed on the locked M2 and against ae_comfort / ae_cond /
  iforest / qnbm (running).

## Mechanism of false alarms (2026-11-23, M1; scripts/mechanism_fa.py, results/mechanism_fa_*.csv)
Conditions in the 24 h before each false-alarm start vs 1050 random normal times (30 per substation):
| condition (24 h before)                   | AE FA (n=223, 32 subs) | SRCR-C FA (n=180, 20 subs) | random normal |
| summer month (May-Sep)                    | 0.61 | 0.15 | 0.41 |
| heating off (median HC1 setpoint <= 20 C) | 0.23 | 0.04 | 0.10 |
| comfort shortfall > 5 K for >= 1 h        | 0.17 | 0.93 | 0.18 |
| setpoint range >= 10 K                    | 0.65 | 0.82 | 0.63 |
- AE false alarms are enriched for seasonal regime changes (summer, heating off) and NOT for comfort
  shortfall (0.17 ~ base 0.18): they flag changes of operating regime, not loss of service.
- 93% of SRCR-C 'false alarms' coincide with a physically real shortfall (supply > 5 K below an active
  setpoint for >= 1 h) that was not reported. They are verifiable service deviations (or unreported faults),
  i.e. actionable for an operator, which an AE alarm is not. To report as finding; not proof of faults.

## Novelty map (2026-11-23; journal_selection/novelty_map.csv, 59 rows, 39 with closeness >= 2; summary md)
Built from abstracts + Crossref/OpenAlex only (ScienceDirect blocked). Claim limits found:
- PreDist paper (10.1016/j.energy.2026.141178) already speaks of "few false alarms": we must not claim to be
  first to consider false alarms; our claim = every-step scoring, FA per substation-year, recall at a fixed
  budget, cross-manufacturer locked test.
- Heating-curve misconfiguration papers (10.1016/j.segy.2026.100256, 10.24406/publica-9049) report AE MISSES
  of comfort-relevant drift; we report AE FALSE ALARMS and test the scoped alternative. Cite both.
- Seasonal residual behaviour is known (10.1016/j.segy.2024.100159): frame our mechanism as empirical
  attribution on labelled DH data. Locked-test / alarm-burden protocols exist for wind turbines: protocol
  novelty holds only "for DH substations". Control-strategy rules exist (10.1016/j.energy.2026.142993): the
  new part is the controlled factorial on a public benchmark.
- 10.1016/j.egyai.2026.100824 (STST): OpenAlex reference list (66 refs, checked 2026-11-23 session 3) cites neither the PreDist paper (W7159838334) nor the Zenodo record (W7105746820); abstract: six datasets, supervised F1 0.77-0.98, no continuous-monitoring FA rate. Use of PreDist: probably not, UNVERIFIED (full text blocked).

## M2 access log
- 2026-11-23 (session 3): candidate set + analysis frozen (protocol A4, A5; scripts/m2_evaluate.py committed).
  Started computing M2 SCORE FILES (rule, sigma3, loop3s, loop3s_c). No thresholds applied, no M2 metric
  inspected until all M1 cells and seeds are complete; then scripts/m2_evaluate.py 2 is run exactly once.
- Session-3 rebuild reproduced round-4 M1 numbers exactly (AE 1.78 / 5.63 FA/sub-yr at recall 0.214 / 0.321;
  SRCR-C 0.18 / 0.65). New on M1: iForest needs 2.42 / 18.29 (worse than AE).
- 2026-11-23 (session 3) BUG FIX during M2 score computation, no metric inspected: ThreeSigma and IForest
  crashed when no signal passed the 20%-availability filter in a training window (M2 substation 33, very short
  series). Fix: such a model returns no score (NaN) for that retraining period, as for any missing data.
  Code path never triggered on M1 (M1 scores unchanged). sigma3 M2 recomputed for the remaining substations.
- 2026-11-23 (session 3) DRY RUN of scripts/m2_evaluate.py on M1 (in-sample, development only; files
  results/DRYRUN_insample_m1_*.csv). Code runs end-to-end (27 min, 2000 boots). M1 in-sample: no HF4 contrast
  significant at n = 28; HF1 threshold-free: SRCR-C vs SRCR-all 23/28 faults better, p = 0.009; AE-comfort vs
  AE p = 0.040; Loop-3s-C vs Loop-3s p = 0.060. Power warning: n = 25 on M2 -> the pooled M1+M2 secondary
  analysis (A4) is needed for adequate power; report both, primary stays M2.
- 2026-11-23 (session 3) LOCKED EVALUATION: all 11 cells scored on M2 (seed 0, 58/58 substations each).
  scripts/m2_evaluate.py 2 2000 run ONCE now (code as committed for A5 + the logged NaN bug fix). Output:
  results/locked_m2_operating_points.csv, results/locked_m2_tests.csv, results/logs/LOCKED_m2.log.
- LOCKED M2 RESULT (2026-11-23, session 3; results/locked_m2_*.csv): NEGATIVE for the proposed method.
  Recall at B = 2 (M1-chosen thresholds), n = 25: sigma3 0.28, qnbm 0.20, ae_comfort 0.12, rule 0.08,
  loop3s_c 0.08, loop3s 0.08, iforest 0.08, ae 0.04, srcr_c 0.00, srcr_all 0.00, ae_cond 0.00.
  HF4 (SRCR-C >= baselines) FAILED: SRCR-C worse than sigma3 (McNemar p = 0.016 raw) and qnbm (0.0625).
  HF1 (scope) not supported on M2 (p 0.37 / 0.93 / 0.28). HF2: SRCR-C vs AE-comfort reversed (AE-comfort
  better, p = 0.016). HF3: SRCR-C ranks worse than rule (p = 0.0003) and loop3s_c (0.003).
  Realised FA rates stayed near budget for most methods (calibration transfer OK; detection transfer failed).
  This result is final for the pre-registered analysis; M2 is now burned for method selection.
- Post hoc descriptive: Spearman rank correlation of M1 (in-sample) vs M2 (locked) recall across the 11 cells: B=1 -0.33, B=2 -0.15, B=4 0.07 (all p > 0.3): development rankings do not transfer.
- SECONDARY (pre-registered; results/secondary_*.csv), 2026-11-23 session 3:
  * Cold start: 7/25 M2 target faults occur < 90 d after the substation's first record (M1: 2/28). sigma3's 7
    M2 detections: 5 are < 90 d faults (median history 70 d); its FA rate in that bin is 2.94/sub-yr on M2,
    8.75 on M1. After 90 d no method exceeds 2/18 M2 faults at B = 2. Apparent M2 winners = start-up artefact.
  * Pooled M1+M2 threshold-free ranks (n = 53): scope effect supported for fleet model (SRCR-C vs SRCR-all
    41/10, p = 0.016) and AE (AE-comfort vs AE 35/18, p = 0.021); Loop-3s-C vs Loop-3s p = 0.10.
    Fleet model worse than own-history comfort statistic (p = 0.031) and rule (p = 0.080).
  * By label: leakage (7) and heating-circuit pump failure (6) are almost never caught by comfort-scoped
    methods; AE / qNBM / sigma3 catch 1-2 each.

## USER DECISION (2026-11-23, session 3): option B = develop a new method on M1 after the locked M2 failure.
Integrity consequences (to be stated in the paper): M2 is no longer a clean test. Round 5 is MOTIVATED by the
M2 diagnosis (hydraulic fault types, start-up period, short histories). Any M2 evaluation of a round-5 method
is a DISCLOSED SECOND LOOK, run once, after the method is frozen and committed. Time-box: ONE round; if its
hypotheses fail on M1, stop and recommend option A.

## Round 5 plan (hypotheses written BEFORE any round-5 code was written, 2026-11-23; M1 only)
Diagnosis (from locked M2 + secondary analyses): comfort-loop scope misses hydraulic faults (leakage, pumps,
pressure regulators); own-history models are immature in a substation's first months; AE false alarms follow
seasonal regime. Novelty-map check: same-day peer comparison exists (HEAT, Energy and AI 2025; SHEDAD 2024;
multi-turbine reference 2022); changepoints on dT/flow exist (arXiv 2026). Any gain is incremental unless it is
large. Families (ideas #15-#19; total ideas tried becomes 19):
 F18 PEER-PHYS: daily physics features compared with the SAME DAY's distribution over the other substations
     of the fleet (robust median / 1.4826 MAD, leave-one-out): primary cooling dT (low side), primary return
     temperature (high side), DHW upper-storage 10th percentile (low side). No own history, no training;
     seasonal regime and weather are shared by peers and cancel. Daily score used from the NEXT day (causal).
 F19 PEER-COMFORT: same-day peer z of the daily HC1/DHW shortfall (gated, one-sided).
 F20 PEER-ALL: max of F18 and F19.
 F21 OWN-CHANGE: changepoint of daily dT and flow vs the substation's previous 14 days (robust z, own history).
 F22 FUSE: max(PEER-ALL, SRCR-C) with per-channel scaling fixed a priori (each channel score = z / 3).
Hypotheses (M1, n = 28; thresholds on the shared tau x c_thr grid; daily score broadcast to 10-min steps):
 H5a: PEER-PHYS ranks >= 3 more M1 faults within the top 2% of normal days than the best existing cell
      (threshold-free, diagnose.fault_ranks), with >= 2 of the gained faults hydraulic (leakage, pump,
      pressure regulator, valve). Falsified otherwise.
 H5b: the best of F18-F22 reaches M1 recall >= 0.43 (12/28) at <= 2 FA/sub-yr (best existing M1: 0.393
      at B = 4, 0.357 at B = 2). Falsified otherwise.
 If H5b is falsified the round fails -> recommend option A to the user.

## Round 5 results (2026-11-23, M1 development; results/round5_peer_m1.csv; scripts/round5_peer.py)
Ideas counted: 14 + #15 peer-phys, #16 peer-comfort, #17 peer-all, #18 own-change, #19 fuse = 19.
Faults in top 2% of normal days (threshold-free, n = 28): peer_phys 8, peer_comfort 10, peer_all 10,
own_change 3, fuse 12 | reference: SRCR-C 11, rule 11, loop3s_c 10, qnbm 7, sigma3 6, ae_comfort 6, ae 2.
Recall at <= 1 / 2 / 4 FA/sub-yr: peer_phys 0.179 / 0.179 / 0.179; peer_comfort 0.179 / 0.214 / 0.250;
peer_all 0.214 / 0.250 / 0.286; own_change 0.036 / 0.071 / 0.143; fuse 0.286 / 0.321 / 0.321.
- H5a FALSIFIED (peer_phys 8 < 11 + 3). Peer channels do rank hydraulic faults (leakage, DHW charging pump,
  primary valve, pressure regulator) in the top 2%, but not more faults overall than SRCR-C / rule.
- H5b FALSIFIED (best 0.321 < 0.43 at <= 2 FA/sub-yr).
- Round 5 FAILED. Per the pre-registered time-box: stop, no M2 second look, recommend option A.
