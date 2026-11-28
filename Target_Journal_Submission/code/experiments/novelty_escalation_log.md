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

<!-- [lineage merged-63cb0d0-lineages] -->
- 2026-11-23: after Amendment A1 freeze, M2 detector SCORES computed for all frozen methods (no evaluation yet).
- 2026-11-23: M2 score run crashed for sigma3 and IForest on a substation whose training window had no usable
  numeric column. Fix: such windows get no score (NaN), as with any model without training data. Does not touch
  M1 (never triggered) nor any frozen operating point. No M2 evaluation had been run.


<!-- [lineage practical-sagan] -->
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
Round 5 additions (still before any event-protocol number was computed):
 H5d (mechanism 1, selection): at each method's continuous B = 2 operating point, the share of hand-picked normal
     events with an alarm is LOWER than the share of randomly drawn eligible 7-day windows of normal time with an
     alarm (same substations, same scores; 2,000 random windows, seed 0). Supported if the pooled rate ratio
     (normal events / random windows) < 1 with a bootstrap CI excluding 1.
 H5e (mechanism 2, resolution; analytic, F19): with N normal weeks the event protocol cannot separate deployment
     false-alarm rates of 1 vs 4 per asset-year with >= 80% power unless N is >= several hundred; PreDist has
     65 normal events (M1 35). Computed exactly from the binomial model p_w = 1 - exp(-lambda * 7 / 365.25).

## Round 6 plan: F18 second dataset (written 2026-11-24 BEFORE any CARE score was computed)
Data: CARE to Compare (Zenodo 14958989, CC-BY-4.0): 3 wind farms, 36 turbines, 95 datasets (45 anomaly, 50 normal
events), 10-min SCADA. Overlapping datasets of one turbine agree exactly (checked: max abs diff 0.0), so each
turbine's datasets are merged into ONE continuous series (union of timestamps) -> ~50 turbine-years.
Continuous protocol (same code path as PreDist): burn-in 30 d; online per-turbine retraining every 90 d on up to
730 d of own past, training rows restricted to status_type_id == 0 (normal operation, CARE convention) and outside
known exclusions; detection window = CARE anomaly event [event_start, event_end); exclusion = [event_start - 14 d,
event_end + 2 d) outside the window; refractory 24 h; false alarms per turbine-year.
Methods (unchanged classes from PreDist, seed 0): sigma3, iforest, ae, ae_cond; plus temp3s = sigma3 on
temperature sensors only (domain-informed simple detector, the analogue of the DH rule). Same tau x c grid.
Operating points: leave-one-farm-out (choose on two farms, apply to the third) at B = 1, 2, 4 per turbine-year;
in-sample points reported as secondary.
Event protocol E on CARE: all 95 events, positive if alarm active in the event window; best F0.5 over the grid
(benchmark-style, in-sample) and at the LOFO B = 2 point.
 H6a: Kendall tau between E-best-F0.5 ranking and continuous recall@B=2 ranking < 0.5 (5 methods: descriptive).
 H6b: event precision (E-best) exceeds deployed alarm precision at B = 2 by >= 5x for every method.
 H6c: alarm rate on CARE normal events is lower than on random eligible 7-day normal windows (rate ratio < 1).
 H6d (resolution): 50 normal events -> power to separate 1 vs 2 FA/turbine-year < 0.5 (analytic, as H5e).

## Round 5 results (2026-11-24, M1; results/round5/protocol_compare_m1.csv, protocol_summary_m1.csv, event_grid_m1.csv)
64 events (29 target faults + 35 normal), same online scores for both protocols, 9 methods.
- H5a SUPPORTED: Kendall tau (benchmark-style best event F0.5 vs continuous recall at B=2) = 0.21 (p = 0.45),
  Spearman 0.32. When the event protocol uses each method's continuous B=2 operating point instead of
  test-tuned thresholds, Kendall tau rises to 0.64 -> most of the inversion comes from tuning thresholds on the
  balanced test events (the benchmark practice), not from the event windows themselves.
- H5b SUPPORTED: sigma3 (F0.5 0.84), loop3s (0.81) and IForest (0.79) beat the rule (0.75) on the event protocol,
  yet the rule has the highest continuous recall at B=2 (0.32 vs 0.25 / 0.25 / 0.18). Under the event protocol
  the plain three-sigma baseline is the BEST of 9 methods; under continuous monitoring it is mid-table.
- H5c SUPPORTED: event precision exceeds deployed alarm precision by 16x (rule) to 44x (qnbm) for every method
  (event precision 0.73-1.00 vs deployed 0.02-0.06).
- H5e (analytic, earlier): 65 normal weeks cannot separate 1 vs 2 FA/asset-yr (power 0.23).
Verdict round 5: primary gain of the STORY (a measured, explained ranking inversion), not of a method.

<!-- [lineage merged-main] -->

<!-- [lineage focused-wozniak] (parallel session; merged 2026-11-24) -->
## Round 5 plan (written 2026-11-23 BEFORE running; user asked for more novelty; M2 still NOT evaluated)
Diagnosis: (i) the gain of C2 is small in absolute faults; (ii) "rule OR AE" reads as a mere combination with no
reason WHY the two are complementary; (iii) per-substation fixed thresholds may spend the fleet FA budget on a
few noisy substations. Three genuinely different fix families (all on M1 only; ideas 14-16):
 F17 Substation-calibrated alarm evidence (budget redistribution). Online, per substation and per 90-day block,
     map the raw score to its exceedance probability under the substation's OWN past scores (up to 365 d before
     the block, known exclusions removed): e = -log10 p. Same criticality counter; tau grid on e {2, 2.5, 3, 4},
     same c grid. Applied to rule, AE (seed 0) and their OR-fusion.
     H5a: calibrated rule OR calibrated AE reaches M1 recall >= 0.429 (12/28) at <= 2 FA/sub-yr (C2: 0.393).
     H5b: the FA share of the 5 noisiest substations falls versus uncalibrated C2 at B = 2.
 F16 Complementary-by-design learned partner: AE trained WITHOUT any loop measurement/setpoint column
     ("ae_noloop": drops every column containing "setpoint" and the secondary loop supply / DHW
     upper-storage temperatures (NOLOOP in run_online_method.py); keeps primary-side, return, valve, pump, flow signals), so it can only see hydraulic/primary/pressure behaviour the rule cannot.
     H5c: rule OR ae_noloop >= C2 recall at B = 2 on M1 (seed 0; seeds 0-4 if supported).
 F18 Pre-registered physics-based fault-signature taxonomy, tested ONLY on locked M2 (prediction, not fitting).
     Classes fixed from the fault label text before M2 evaluation:
       A supply-path restriction (shows as loop measurement below setpoint): primary motorised control valve
         (all 4 labels), differential pressure regulator (setting / defective), DHW storage charging pump,
         strainer poor flow, air in piping, temperature monitor/controller defective.
       B circulation / hydraulic integrity: heating-circuit pump failure, leakage, heat exchanger external
         leakage, safety relief valve water loss, low expansion-vessel pre-charge, shut-off valve closed.
       C intent error (wrong setpoint/parameter; the loop tracks a wrong target): control unit incorrect
         parameterisation.  U: unknown.
     H5d (M2): rule recall in class A > rule recall in classes B+C.
     H5e (M2): among faults detected by AE but not by the rule, the share in B+C exceeds the share of B+C among
     faults detected by the rule. Caveat: M1 detections were seen when writing this taxonomy, so only M2 counts.
 Multiplicity: ideas 14-16 counted (total 16). Any survivor becomes candidate C3 in protocol Amendment A2,
 written BEFORE m2_eval.py runs; C1/C2 stay as frozen.

## Round 5 results — F17 substation calibration (M1; results/round5/)
 cal_rule: B=1 0.250 @0.61, B=2 0.286 @1.96, B=4 0.286 (raw rule 0.286 / 0.321 / 0.321)
 cal_ae:   B=1 0.143, B=2 0.143 @0.85, B=4 0.250 (raw AE seed 0: 0.214 at B=2)
 cal_rule OR cal_ae (8x6 Pareto pairs): B=1 0.286, B=2 0.321 @1.07, B=4 0.357 (C2: 0.321 / 0.393 / 0.429)
 H5a FALSIFIED (0.321 < 0.429). H5b FALSIFIED: top-5 substations' FA share 0.376 (C2) -> 0.470 (calibrated).
 Reason (diagnosis): calibrating each substation against its own past makes a quiet, well-tuned substation
 alarm on small deviations that are normal fleet-wide, so the budget moves TO quiet substations instead of away
 from noisy ones; and faults in substations with a chronically poor history are pushed below threshold. Absolute,
 physically scaled evidence (Kelvin of shortfall) carries information that rank calibration discards.
 F17 dropped. Negative result kept for the paper ("own-history calibration hurts").

## Round 5 addition — F19 protocol-gap analysis (pre-registered 2026-11-23 before running; idea 17)
Same online scores, same alarm logic, two protocols. Event protocol (as in the dataset benchmark): fault events
(efd_possible, window = 7 d before report) and the dataset's predefined normal events (Event start-end); an event
is flagged if the alarm is active at any step in its window; event precision, recall, F0.5. Continuous protocol
as in protocol v1. For each of the 8 v1 methods (rule, sigma3, loop3s, iforest, qnbm, ae, ae_cond, srcr):
 (i) the (tau, c) maximising event F0.5 on M1 -> its continuous FA/sub-yr and recall (M1; M2 in locked eval);
 (ii) event precision vs continuous alarm precision at that point; (iii) Spearman correlation between the
 method ranking by best event F0.5 and by continuous recall at B = 2.
 H5f: the event-F0.5-optimal point exceeds 4 FA/sub-yr (2x the primary budget) for >= 5 of 8 methods (M1 and M2).
 H5g: event precision >= 5x continuous alarm precision for every method at the event-optimal point.
 H5h (exploratory): rank correlation < 0.5 (protocol choice changes which method looks best).

## Round 5 results — F19 protocol gap (M1; results/protocol_gap/m1_*.csv; 29 fault + ~35 normal events)
 At each method's event-F0.5-optimal (tau, c):  event precision | continuous alarm precision | continuous FA/sub-yr
  rule 1.00 | 0.045 | 1.2 ; sigma3 0.91 | 0.008 | 10.4 ; loop3s 0.94 | 0.008 | 11.1 ; iforest 0.93 | 0.004 | 18.3 ;
  qnbm 0.91 | 0.019 | 2.4 ; AE 0.74 | 0.008 | 10.7 ; AE-cond 0.73 | 0.006 | 13.9 ; SRCR 1.00 | 0.031 | 2.2
 H5f SUPPORTED on M1: 5/8 methods exceed 4 FA/sub-yr (10.4-18.3) at the event-optimal point.
 H5g SUPPORTED on M1: event precision is 22x-215x the continuous alarm precision (min 22x, rule).
 H5h (exploratory) SUPPORTED: Spearman rho = 0.40 (p = 0.32, n = 8) between event-F0.5 ranking and continuous
 recall@B=2 ranking. Event protocol ranks three-sigma best (F0.5 0.84) and the rule second-to-last (0.75);
 continuous protocol ranks the rule/SRCR best (0.321) and three-sigma mid (0.25).
 Meaning: a balanced event benchmark would pick detectors that, deployed on 93 substations, raise ~1,000 false
 alarms per year. This is the strongest finding so far (N5 + N7) and is tested on locked M2 in the final eval.

## Round 5 results — F16 complementary-by-design partner (M1, seed 0; results/round5/*ae_noloop*)
 ae_noloop alone: B=1 0.071, B=2 0.071 @0.36, B=4 0.179 (AE seed 0: 0.214 at B=2) -> much weaker alone.
 rule OR ae_noloop (6x4 Pareto pairs): B=1 0.357 @0.71 ; B=2 0.393 @1.44 ; B=4 0.429 @3.33
 (C2 = rule OR AE: 0.321 / 0.393 / 0.429).
 H5c formally SUPPORTED as a tie at B = 2 (0.393 = 0.393), +1 fault at B = 1. No gain over C2 at the primary
 budget, so F16 is NOT promoted to a candidate (seed extension not run; counted as tried). Mechanistic reading:
 an AE that never sees loop temperatures/setpoints is a poor detector alone but adds as much to the rule as the
 full AE does -> the AE's added value comes from non-loop (hydraulic/primary) signals. Supports the F18 taxonomy
 hypothesis; to be tested on M2 via H5d/H5e.
Round 5 summary: ideas 14-17 tried (F17 negative, F16 tie, F18 pre-registered for M2, F19 strong on M1).
Ideas total: 17. Candidates for M2 unchanged (C1, C2); F18 + F19 added as pre-registered M2 analyses (Amendment A2).
- 2026-11-24T00:58Z: LOCKED M2 EVALUATION run (scripts/m2_eval.py, single run) after Amendment A2; all 17 methods x 58 M2 score files verified readable.

## LOCKED M2 RESULTS (2026-11-24, single run; results/m2/, logs/m2_eval.log)
M2: 25 evaluable target faults, 58 substations, 85.5 exposure-years. M1-chosen operating points applied unchanged.
 Recall at B=2 (M1 -> M2): C2 0.393 -> 0.080 ; rule 0.321 -> 0.080 ; AE 0.214 -> 0.040 ; three-sigma 0.250 -> 0.280 ;
 qnbm 0.179 -> 0.200 ; loop3s 0.250 -> 0.080 ; iforest 0.179 -> 0.080 ; AE-cond 0.143 -> 0.000 ; SRCR 0.321 -> 0.000.
 Seeds 0-9, B=2, M2: C2 0.088 +- 0.025 ; AE 0.076 +- 0.048.  Achieved M2 FA/sub-yr at B=2: C2 1.26, rule 0.58, AE 1.89.
 Pooled M1+M2 (53 faults, B=2, seed 0): C2 0.245 vs AE 0.132 (d = +0.113, 95% CI 0.000-0.231, McNemar p = 0.109,
 Holm 0.766); C2 vs rule +0.038 (CI -0.057-0.132); C2 vs AE-cond +0.170 (CI 0.075-0.282, p 0.012, Holm 0.094).
 NO comparison survives Holm. PRIMARY HYPOTHESIS (C2 better than baselines, transferring to M2) NOT SUPPORTED.
F18 on M2: H5d FALSIFIED (rule recall class A 0.09 vs B+C 0.10); H5e FALSIFIED (1 AE-only fault, class U/A).
 Underpowered: the rule detects 2/25 M2 faults.
POST-HOC diagnostic (scripts/diag_loops.py; NOT used to change any method): 44/58 M2 substations expose only the
 HC1 loop (no DHW loops) vs 9/35 on M1; median rule shortfall -0.10 K on M2 vs +0.65 K on M1 (M2 loops track above
 setpoint); the M1 rule thresholds spend only 0.58 of the 2 FA/sub-yr budget on M2.
Verdict so far: the rule/C2 advantage is manufacturer-specific. The honest paper is now about evaluation and
transfer: (i) protocol gap (F19, M2 pending), (ii) M1-tuned detectors lose most recall on a second manufacturer,
(iii) ranking of methods is not stable across manufacturers.

## F19 protocol gap on LOCKED M2 (results/protocol_gap/m2_*; 26 fault + 30 normal events evaluable)
 Event-optimal point (chosen on M2 itself, i.e. the best case for the event protocol) -> continuous FA/sub-yr:
  three-sigma 3.2, quantile NBM 5.4, AE 6.7, AE-cond 8.6, IForest 12.7, rule 13.8, loop3s 19.3, SRCR 112.6.
 H5f SUPPORTED on M2: 7/8 methods > 4 FA/sub-yr (M1: 5/8).
 H5g SUPPORTED on M2: event precision 39x-274x the continuous alarm precision (M1: 22x-215x).
 H5h (exploratory) rho = 0.26 (M1 0.40): the event protocol does not rank methods as deployment does.
 Curve-level endpoint (normalised area, FA 0-6; descriptive): M1 C2 0.386 > SRCR 0.310 > rule 0.308 > ... ;
  M2 three-sigma 0.254 > qnbm 0.196 > loop3s 0.142 > rule 0.130 ~ C2 0.129 ; Spearman M1 vs M2 = 0.30 (n = 9).
FINAL STATUS OF ESCALATION LOOP (17 ideas, 5 rounds): no detector gain survives the locked test. What survives,
pre-registered and replicated on both manufacturers: the protocol gap (N5 + N7). Story pivots to an evaluation
paper: "balanced event benchmarks misjudge early fault detection; continuous budgeted evaluation + cross-
manufacturer transfer show what operators would actually get". Proposed methods reported as negative results.
<!-- [end parallel lineages] -->

<!-- [lineage peaceful-planck] (parallel session; merged 2026-11-24) -->
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
<!-- [end parallel lineages] -->

## Round 6 Amendment A1 + confirmation plan (cycle 4, written 2026-11-24 ~04:05 UTC BEFORE any CARE score exists)
State: no CARE detector output has ever been computed or inspected (CARE zip still downloading; results/scores_care
does not exist). The M2 locked test is burned (evaluated twice by parallel lineages; state/decisions.md D-03), so
CARE is the only unseen data and serves as the confirmation dataset.
A1 (leak fix, CARE path only): an exclusion interval is "known" to the online trainer only once its report time
(event_end) has passed (src/models/online.py known_exclusions with lab.excl_known); the anomaly window
[event_start, event_end) of past events is also removed from later training. PreDist path unchanged (legacy rule)
so committed PreDist numbers stay reproducible; the PreDist leak (4/982 fits) is reported separately.
Confirmation seeds: SEEDS_CONFIRM = [100,101,102,103,104] (fixed in MASTER_PROMPT v2 before any CARE output) for
the seeded detectors iforest, ae, ae_cond, in this priority order (ae, iforest, ae_cond) as compute allows; seed 0
is the pre-registered Round-6 run. Unseeded: sigma3, temp3s.
Added hypothesis (G5 analogue, D-05):
 H6e: for every method (seed 0), the precision-inflation ratio (best-F0.5 event precision / continuous alarm
      precision at the LOFO B = 2 point) has a 95% percentile-bootstrap CI (2,000 resamples of turbines,
      seed 0) with lower bound > 5; one-sided bootstrap p-values for "ratio <= 5", Holm-corrected over the
      5 methods. On confirmation seeds: report mean +- sd over seeds of the ratio, of Kendall tau (H6a) and of
      the selection rate ratio (H6c); H6e must hold for >= 4/5 confirmation seeds of each seeded method.
 Same bootstrap CI (resampling substations) is computed DESCRIPTIVELY for PreDist M1 and M2 (both already seen;
 labelled post hoc).
Analysis code: scripts/round6_care.py (committed before it is first run on real CARE scores).

## Lineage note (added 2026-11-24 cycle 4; nothing above was edited)
Sections above come from several parallel lineages. The wizardly-babbage lineage's OWN rounds 3-4 (origin of
candidate C2 = rule OR AE and the C1/C2 freeze, protocol Amendment A1 of that lineage) are not in this merged file;
they are preserved verbatim in RECHECK/archive_parallel_lineage/Target_Journal_Submission/code/experiments/.
Idea numbers and hypothesis labels (#8-14, H5a-h, F16-22) mean different things in different lineages; the
authoritative cross-lineage count is state/variants_tried.csv (82 rows, 64 distinct ideas).

## Round 6 RESULTS — CARE seed 0 (pre-registered; run once 2026-11-24 ~15:2x UTC; results/round6/seed0/)
Script unchanged since commit 8e79130 (before any CARE score existed). 36 turbines, 95 events (45 anomaly, 50 normal).
| method | E-best F0.5 | E-best prec | LOFO rec@B2 | LOFO FA@B2 | LOFO prec@B2 | inflation | 95% CI | cont FA at E-best | sel. rate ratio |
| temp3s | 0.661 | 0.842 | 0.156 | 2.44 | 0.064 | 13.1 | 8.1-25.8 | 6.7 | 0.304 |
| sigma3 | 0.566 | 0.545 | 0.200 | 2.80 | 0.071 | 7.6 | 4.98-16.7 | 10.8 | 0.610 |
| iforest | 0.603 | 0.708 | 0.000 | 0.00 | 0.000 | undefined (no alarms) | - | 10.6 | undefined |
| ae | 0.667 | 0.733 | 0.178 | 4.09 | 0.045 | 16.4 | 9.9-35.2 | 16.7 | 0.430 |
| ae_cond | 0.667 | 0.733 | 0.267 | 7.76 | 0.036 | 20.6 | 13.5-37.4 | 15.8 | 0.435 |
- H6a SUPPORTED: Kendall tau 0.32 (p = 0.45; n = 5, descriptive); tau at LOFO B2 points 0.40.
- H6b SUPPORTED for the 4 methods with defined deployed precision (min 7.6x); IForest's LOFO B2 point raises no
  alarm at all (0/0), so its ratio is undefined (reported, not patched).
- H6c SUPPORTED for 4/4 evaluable methods: alarm hit rate on the benchmark's normal events 0.16 (ae) vs 0.37 on
  random eligible 7-day normal windows; rate ratios 0.30-0.61, all bootstrap CIs < 1 (upper 0.70-0.80).
  Length-matched secondary: ratio 0.34 for ae (CI 0.15-0.57). => the benchmark's hand-picked normal periods are
  systematically quieter than ordinary normal operation (a selection effect in benchmark construction).
- H6d SUPPORTED: power to separate 1 vs 2 FA/turbine-yr with 50 normal events = 0.12 (7-d windows), 0.35 (mean
  normal-event length 14.9 d).
- H6e NOT SUPPORTED as pre-registered: sigma3's CI lower bound is 4.98 (< 5) and IForest is undefined. The other
  three methods have lower bounds 8.1-13.5 with Holm p < 0.05.
- Unplanned observations: LOFO thresholds overshoot the budget on the held-out farm (ae_cond 7.8 FA/turbine-yr at
  B = 2; ae 4.1); benchmark-chosen points imply 6.7-16.7 FA/turbine-yr in continuous operation.

## H5d RESULT — PreDist M1 selection test (pre-registered; run 2026-11-24 ~16:3x UTC; results/round5/selection_m1*.csv)
Normal events (35) vs 2,000 random eligible normal 7-day windows, same scores, each method's M1 B=2 point.
Pooled ratio 0.466, cluster-bootstrap 95% CI 0.20-0.73 -> H5d SUPPORTED (pre-registered criterion; the CI code
was added after the first run because the original script omitted it, D-15; per-method numbers reproduced exactly).
Per method: rule 0/35 vs 0.031; loop3s 0 vs 0.040; underdel 0/22 vs 0.052; srcr_comp 0 vs 0.050; iforest 0.24
(CI 0-0.76); qnbm 0.22 (0-0.69); sigma3 0.57 (0-1.33); ae 0.997 (0.25-1.80); ae_cond 1.07 (0-2.20).
Reading: the curated normal weeks are quieter for the rule-based and statistical detectors but NOT for the two
autoencoders, whose alarms on normal weeks match random normal time. Together with CARE (H6c, all 4 evaluable
methods incl. both AEs < 1), the selection effect replicates on two benchmarks but is detector-dependent on PreDist.

## PreDist M1 protocol-gap bootstrap CIs (DESCRIPTIVE, post hoc; results/protocol_gap/m1_ci.csv)
Point estimates reproduce m1_gap.csv exactly. Inflation at the SAME benchmark-chosen point: 22-215x, 95% CI lower
bounds 13.4 (rule) to 120 (iforest), all > 5. Inflation vs the in-sample B=2 point: 16-44x, CI lower bounds
3.0 (rule), 9.2-17.4 for the other 7. Continuous FA/sub-yr at benchmark-chosen points: sigma3 10.4 (8.6-12.3),
iforest 18.3 (14.4-54.0), ae 10.7 (5.7-34.2), loop3s 11.1 (4.0-43.6); rule 1.2, qnbm 2.4, srcr 2.2 stay low.

## plan_v2 — PreDist M1, seed 0 (primary), run 2026-11-24 ~22:40 UTC (script unchanged since pre-registration commit 39cecca)
Output: results/plan_v2/predist1/seed0/{summary.json,cells.csv,bootstrap.csv,selection_per_detector.csv}; log logs/planv2_predist1_s0.log.
17 detectors, 35 substations, 64 events (29 fault), 2,000 random windows, 2,000 cluster-bootstrap resamples.
- Kendall tau vs CH (deployment-like reference): ET 0.181, EH 0.633, CT 0.828.
- H7a (threshold source) diff 0.452, 95% CI [0.101, 0.837], one-sided p 0.0045.
- H7b (window design)    diff 0.647, 95% CI [0.019, 0.865], one-sided p 0.0215.
  Holm over the 4 tests {H7a,H7b} x {PreDist, CARE} is applied only after CARE seed 0 (plan_v2.md); verdict PENDING.
  (Holm thresholds for ranks 1-4: 0.0125, 0.0167, 0.025, 0.05; final decision via scripts/plan_v2_summary.py.)
- H7c (descriptive): share of ET disagreement removed by out-of-sample thresholds 0.552; by continuous windows 0.790.
- H7d (selection effect): pooled alarm-hit ratio curated-normal / random 0.300, CI [0.113, 0.516] (< 1);
  16/17 detectors (0.94) have ratio < 1. SUPPORTED (script verdict).
- Recall table (ET/EH/CT/CH): balanced event windows give 0.69-0.84 recall for every detector; deployment-like CH
  gives 0.04-0.29. ae_cond (most sophisticated) is LAST under CH (0.036) but mid-pack under ET.

### 2026-11-25 01:12 UTC — plan_v2 PreDist seed 0: reproducibility check (G9)
On a fresh container (D-26), all PreDist M1 inputs and panel seed-0 scores were regenerated from raw data and
`scripts/plan_v2_analysis.py predist1 0` was re-run. All four outputs in results/plan_v2/predist1/seed0
(bootstrap.csv, cells.csv, selection_per_detector.csv, summary.json) are byte-identical to the committed versions
(empty git diff). H7a/H7b/H7d seed-0 PreDist numbers are therefore reproducible end-to-end. No new test.

### 2026-11-25 01:28 UTC — plan_v2 PreDist robustness seed 1 (results/plan_v2/predist1/seed1)
tau_ET 0.156, tau_EH 0.727, tau_CT 0.715. H7a diff 0.571 (CI 0.214-0.903), p 0.0015; H7b diff 0.559
(CI 0.040-0.892), p 0.016; H7d pooled ratio 0.290 (CI 0.111-0.497), 16/17 detectors < 1 -> supported.
H7c shares: threshold 0.68, window 0.66. Counts toward the >= 4/5 robustness rule (seed 1: H7a yes, H7b yes, H7d yes).

### 2026-11-25 01:41 UTC — plan_v2 PreDist robustness seed 2 (results/plan_v2/predist1/seed2)
tau_ET 0.134, tau_EH 0.644, tau_CT 0.818. H7a diff 0.510 (CI 0.132-0.886), p 0.0045; H7b diff 0.684
(CI -0.027-0.906), p 0.031; H7d ratio 0.277 (CI 0.095-0.511), 16/17 detectors < 1 -> supported.
Note: for H7b the one-sided p (0.031) is < 0.05 but the reported two-sided 95% CI includes 0. The pre-registered
robustness rule counts unadjusted p < 0.05, so seed 2 counts for H7b; the manuscript must report this seed as
borderline (CI includes 0) rather than as clean support.

### 2026-11-25 01:55 UTC — plan_v2 PreDist robustness seed 3 (results/plan_v2/predist1/seed3)
tau_ET 0.283, tau_EH 0.569, tau_CT 0.756. H7a diff 0.287 (CI 0.024-0.740), p 0.018; H7b diff 0.473
(CI 0.005-0.777), p 0.0225; H7d ratio 0.317 (CI 0.118-0.554), 16/17 detectors < 1 -> supported.
Smallest effects so far (tau_ET highest of seeds 0-3); all three still hold. PreDist tally after 4 seeds:
H7a 4/4, H7b 4/4 (seed 2 borderline CI), H7d 4/4 -> robustness rule (>= 4/5) already met for PreDist.

### 2026-11-25 02:08 UTC — plan_v2 PreDist robustness seed 4 + PreDist tally (seeds 0-4 complete)
Seed 4: tau_ET 0.259, tau_EH 0.596, tau_CT 0.756. H7a diff 0.337 (CI 0.021-0.732), p 0.021; H7b diff 0.498
(CI -0.025-0.799), p 0.0325; H7d ratio 0.300 (CI 0.110-0.510), 16/17 < 1 -> supported.
PreDist robustness (unadjusted one-sided p < 0.05, pre-registered rule >= 4/5):
  H7a 5/5 (p 0.0045, 0.0015, 0.0045, 0.018, 0.021)  -> robust
  H7b 5/5 (p 0.0215, 0.016, 0.031, 0.0225, 0.0325) -> robust by the rule, BUT two-sided 95% CI includes 0 in
      seeds 2 and 4; report H7b on PreDist as "robust by the pre-registered rule, effect imprecise".
  H7d 5/5 (pooled ratio 0.28-0.32; 16/17 detectors < 1 in every seed) -> robust
H7c (descriptive): out-of-sample thresholds remove 40-68% of the ET ranking disagreement; continuous replay 66-79%.
Confirmatory Holm step (4 seed-0 tests incl. CARE) still pending CARE seed 0.

### 2026-11-25 08:02 UTC — plan_v2 CARE seed 0 + CONFIRMATORY HOLM STEP (scripts/plan_v2_summary.py, verbatim)
CARE seed 0 (15 detectors, 36 turbines, 95 events, 45 faults): tau_ET 0.435, tau_EH 0.744, tau_CT 0.305.
H7a diff 0.310 (CI 0.144-0.935), p 0.0055. H7b diff -0.130 (CI -0.286-0.858), p 0.1495. H7d ratio 0.424
(CI 0.265-0.614), 13/14 detectors < 1 -> supported. H7c: threshold share 0.548, window share -0.230.
Holm (alpha 0.05, 4 seed-0 tests):
| test | p (one-sided) | Holm threshold | H0 rejected |
| H7a_predist1 | 0.0045 | 0.0125 | True |
| H7b_predist1 | 0.0215 | 0.0250 | True |
| H7a_care | 0.0055 | 0.0167 | True |
| H7b_care | 0.1495 | 0.0500 | False |
Interpretation (pre-registered framing): threshold source (H7a: tuning thresholds on the evaluated events) distorts
detector rankings on BOTH energy domains -> confirmatory, cross-domain. Window design (H7b) is supported on PreDist
only; on CARE continuous replay with in-sample thresholds agrees LESS with deployment than event-window ET does
(negative diff, window share -0.23) -> H7b does NOT generalize and must be reported as dataset-dependent.
Selection effect (H7d, descriptive per plan) holds on both datasets. CARE robustness seeds 1-4 pending (queue).

### 2026-11-25 09:40 UTC — plan_v2 CARE robustness seeds 1-4 (chain DONE) — FINAL plan_v2 tally
CARE seeds 1-4: H7a p 0.0125 / 0.004 / 0.002 / 0.011 (all CIs exclude 0); H7b p 0.135 / 0.111 / 0.1045 / 0.1455
(not supported; CT tau 0.23-0.29 < ET in every seed); H7d ratio 0.413-0.428, CI upper <= 0.616, supported 4/4.
FINAL (pre-registered rule >= 4/5): PreDist H7a 5/5, H7b 5/5 (imprecise), H7d 5/5; CARE H7a 5/5, H7b 0/5, H7d 5/5.
Claims of record: threshold-source effect robust and Holm-confirmed on two domains; selection effect robust on two
domains; window-design effect PreDist-only (reverses on CARE).

<!-- [lineage practical-sagan-account4] (parallel session; merged 2026-11-24) -->
- H5d SUPPORTED (results/round5/selection_m1.csv, selection_pooled_m1.csv): at each method's B=2 operating point,
  hand-picked normal events carry alarms at 0.43x the rate of 2,000 random eligible normal weeks (pooled over 9
  methods; cluster bootstrap 95% CI 0.18-0.68). For rule, loop3s, underdel and SRCR NONE of the 35 normal events
  alarms, while 3-11% of random normal weeks do. Exception: AE / AE-cond ratio ~1.0. Mechanism: the benchmark's
  normal weeks are easier than typical operation, so event-protocol precision is inflated beyond the base-rate
  effect alone.

## Round 7 plan: F22 corrected ("deployment-calibrated") event protocol (written 2026-11-25 BEFORE computing it)
Diagnosis after round 5: the balanced protocol fails for three separable reasons, each measured: (i) thresholds
tuned on the test events (tau 0.21 -> 0.64 when fixed), (ii) hand-picked easy normal weeks (H5d, ratio 0.43),
(iii) too few normal weeks to resolve FA rates (H5e). Constructive fix, cheap enough for any benchmark that has
continuous data: E* = same fault windows, but (a) normal windows = N_rand random eligible weeks drawn uniformly over
all monitored normal time (N_rand chosen by the H5e power rule; here 500), (b) each method's threshold is fixed
BEFORE scoring the evaluated events, at the point whose random-week alarm rate on a DISJOINT calibration set of
random weeks matches a target weekly FP rate p* = 1 - exp(-B * 7 / 365.25), B = 2 (no test-event tuning), (c) report
recall at that fixed weekly FP rate (not F0.5 on a 50/50 set).
 H7a: Kendall tau between E* recall ranking and continuous recall@B=2 ranking >= 0.7 on PreDist M1 (9 methods),
      vs 0.21 for the benchmark protocol.
 H7b: the same holds on CARE (5 methods; descriptive) with tau >= 0.6.
 H7c (cost): E* needs only event windows + random weeks (no full continuous replay); its ranking agrees with
      continuous evaluation while the benchmark protocol does not, on both datasets.
Seeds: random weeks seed 0 (calibration) and seed 1 (evaluation); sensitivity seeds 2-5.

## Round 7 results (2026-11-25; results/round7/estar_m1_seed1_n500.csv)
- H7a FALSIFIED: Kendall tau(E* recall, continuous recall@B2) = 0.32 (p = 0.27) vs 0.21 for the benchmark protocol.
  Detail handling (not pre-specified): if no grid point reaches p*, recall = 0 (as runner.best_at_budgets);
  this happened for sigma3. iforest and underdel reached only rate 0 points -> recall 0.
- Diagnosis: E* measures "alarm ACTIVE at any time in a random week", while the continuous protocol counts alarm
  STARTS (rising edges, 24 h refractory). sigma3 never gets its weekly active-rate below 3.8% on the grid yet
  has only 1.37 alarm starts per sub-yr at its B=2 point -> its alarms persist for long periods. A stuck alarm
  counts as ONE false alarm under the start-based definition. This exposes a weakness in OUR primary protocol:
  alarm burden should also be measured as alarm-active time, not only alarm starts.
- Not supported -> E* in this form is not a contribution. Lesson kept for round 8.

## Round 8 plan: alarm-burden definition robustness (written BEFORE computing)
R8 = primary-endpoint robustness of the continuous protocol: burden measured as ALARM-DAYS per sub-yr (distinct
calendar days with the alarm active at any time, outside windows/exclusions), budgets D in {4, 8, 16} days/sub-yr;
operating point per method chosen on M1 over the same grid to maximise recall s.t. alarm-days <= D.
 H8a: the rule is first or tied-first in recall at D = 8 (the main finding survives the stricter burden measure).
 H8b: Kendall tau between start-based (B=2) and day-based (D=8) method rankings >= 0.5.
 H8c: E* (round 7) recall ranking agrees better with the day-based continuous ranking (tau >= 0.6) than with the
      start-based one (0.32) -> confirms the diagnosis.

## Round 8 results (2026-11-25; results/round8/burden_days_m1.csv, curves_m1.csv, summary_m1.csv)
Recall at an ALARM-DAYS budget (M1, 28 faults), D = 4 / 8 / 16 alarm-days per sub-yr:
  rule 0.286 / 0.321 / 0.321 ; SRCR(gate,1s,local) 0.214 / 0.357 / 0.357 ; loop3s 0.143 / 0.214 / 0.321 ;
  sigma3 0 / 0.107 / 0.250 ; AE (benchmark) 0 / 0.036 / 0.214 ; AE-cond 0.036 / 0.143 / 0.214 ;
  qnbm 0 / 0 / 0.214 ; IForest 0 / 0 / 0 ; underdel 0.071 / 0.143 / 0.250.
- H8a FALSIFIED in its strict form: SRCR (0.357) beats the rule (0.321) by ONE fault at D = 8. The broader pattern
  is stronger than under start-counting: the two setpoint-relative one-sided detectors are the only ones above
  0.22 at D <= 8; the benchmark AE detects 1/28 faults at 8 alarm-days per sub-yr.
- H8b SUPPORTED: Kendall tau (start-based B=2 vs day-based D=8 ranking) = 0.68.
- H8c SUPPORTED: E* (round 7) agrees with the day-based ranking (tau 0.61) far better than with the start-based
  ranking (0.32) -> diagnosis confirmed: the cheap random-week protocol E* tracks alarm-active burden.
- Consequence: report BOTH burden measures in the paper; the generic learned NBMs (AE, IForest, quantile NBM) are
  "persistent alarmers": few alarm starts, many alarm-days. Physically anchored residuals do not have this problem.
<!-- [end parallel lineages] -->

## plan_v2 PreDist seed-0 RERUN (reproducibility, D-29), 2026-11-25 ~15:25 UTC
New container, regenerated scores: summary.json, cells.csv, bootstrap.csv, selection_per_detector.csv identical to the
committed files (git diff empty). New file ch_per_asset.csv (input of plan_v3 arm 1).

## plan_v3 arm 1 — PreDist M1 (pre-registered, script unchanged since f09c88e), 2026-11-25 ~15:30 UTC
Output: results/plan_v3/predist1/{summary.json,window_arm.csv}; log logs/planv3_predist1.log.
45,632 asset-days, 221 faulty; W-bal 442 days. 17 detectors.
- H8a NOT SUPPORTED: min prevalence drop 0.123 < 0.15 (robust_z_max); 14/17 detectors drop >= 0.15
  (W-bal oracle macro F1 0.53-0.63 -> 0.35-0.44 on W-nat at the same threshold).
- H8b SUPPORTED: at the W-bal-optimal threshold every detector (17/17) implies >= 10 false-alarm days per
  substation-year: range 83-174, median 125.
- H8c NOT SUPPORTED: Kendall tau (W-bal oracle F1 vs CH) 0.246, CI [-0.122, 0.575]; upper bound not < 0.5.
- Descriptive: W-nat ORACLE macro F1 is 0.500-0.526 for every detector (~chance level for macro F1 on 0.5% prevalence:
  the best natural-prevalence threshold is effectively "never alarm"). W-bal AUROC 0.53-0.66.
Holm over H8a-c x 2 datasets pending CARE arm 1 (needs CARE seed-0 extras + panel seed 0).

## G8 leak sensitivity — PreDist M1 seed 0 (experiments/leak_sensitivity.md), 2026-11-25 ~20:55 UTC
Leak-free rule rescored subs 4 and 7 for all 17 detectors; score changes confined to the 4 affected refit periods
(checked: 0 changed steps outside them). Outputs: results/leak_sensitivity/{compare.csv,cells.csv,verdict.json,leakfree_outputs/}.
PRE-REGISTERED CRITERION: NOT ROBUST (verdict.json robust=false): H8c flips (not supported -> supported: tau 0.217,
CI [-0.177, 0.497]) and max |delta CH| = 0.143 (lof_pca, 4 faults; also gmm_pca 2, pca_t2/knn_pca/ae_cond 1).
Direction of every conclusion unchanged:
- tau_ET 0.181 -> 0.344, tau_EH 0.633 -> 0.652, tau_CT 0.828 -> 0.834.
- H7a diff 0.452 -> 0.307, CI [0.016, 0.773], p 0.0045 -> 0.017; H7b diff 0.647 -> 0.489, CI [0.043, 0.752], p 0.0215 -> 0.012.
  Holm (with CARE seed-0 p 0.0055 / 0.1495 unchanged) still rejects H7a_predist1, H7b_predist1, H7a_care; H7b_care not.
- H7d ratio 0.300 -> 0.207 (CI [0.052, 0.372]); still supported. H8a still not supported, H8b still supported.
Reading: two substations (one efd_possible fault, sub 7 event 67) move tau_ET by 0.16 and one detector's deployment
recall by 4/28. The headline effects (out-of-sample thresholds and continuous replay restore the ranking; selection
effect) survive; individual detector numbers and the borderline H8c do not. Rank statistics on 17 detectors x 28
faults are fragile; the paper must say so and report the leak-free numbers as primary for PreDist (D-30).

### 2026-11-25 ~21:50 UTC (corrected; commit time authoritative) — plan_v2 Amendment A1 RESULTS (pre-registered in 324f9e9 before running; results/plan_v2/amendment_A1/)
Seed 0, one-sided p (pre-registered percentile | T1 null-centred bootstrap | T2 within-detector label swap):
  H7a CARE 0.0055 | 0.065 | 0.184 ; H7a PreDist leak-free 0.017 | n/a (no bootstrap file) | 0.184 ;
  H7a PreDist legacy 0.0045 | 0.0075 | 0.076 ; H7b PreDist leak-free 0.012 | n/a | 0.092 ;
  H7b PreDist legacy 0.0215 | 0.0015 | 0.027 ; H7b CARE 0.1495 | 0.680 | 0.612.
Holm T2 (leak-free PreDist + CARE): no test rejected. Holm T1 (legacy PreDist + CARE): PreDist H7a and H7b rejected,
CARE H7a and H7b not. Robustness (T1 and T2 both < 0.05): CARE H7a 0/5, H7b 0/5; PreDist legacy H7a 2/5, H7b 3/5.
VERDICT (A1 decision rule): H7a and H7b are NOT "confirmed under A1" on any dataset. The pre-registered Holm result
(3/4 rejected) stands as the plan_v2 result of record but is reported together with A1, and the paper must not claim
that the threshold-source or window-design effect on RANKINGS is statistically established. With 15-17 detectors and
a tie-bound reference (1-12 detected faults), rank-agreement contrasts are underpowered. What remains claimable:
descriptive tau pattern (EH > ET on both datasets in 10/10 seed-dataset cells), protocol gap / FA burden at
benchmark-chosen thresholds, and the selection effect (H7d).

### 2026-11-28 ~03:38 UTC — plan_v2 Amendment A2 RESULTS (pre-registered c881aea; results/plan_v2/amendment_A2/)
Area-like reference CHA = mean CH recall over B in {0.5,1,2,4,8}. Label-swap one-sided p (20,000 perms):
 CARE seeds 0-4: H9a p 0.158/0.125/0.019/0.053/0.015; H9b p 0.110/0.092/0.056/0.138/0.070.
 PreDist LEGACY seeds 0-4 (leak-free pending): H9a p 0.355/0.344/0.451/0.531/0.399; H9b p 0.183/0.158/0.243/0.222/0.065.
 Holm seed 0 (CARE + PreDist legacy): nothing rejected. Robustness (>= 4/5 needed): CARE H9a 2/5, H9b 0/5; PreDist 0/5.
 -> H9a, H9b NOT supported. Ranking-mechanism claims remain unestablished (consistent with A1).
Descriptive (robust across all 10 runs):
 D0 tau(ET, CHA): CARE -0.06..0.12 (benchmark ranking ~uninformative about multi-budget deployment ranking);
    PreDist 0.30..0.49. tau(EH,CHA) CARE 0.44..0.65; tau(CT,CHA) CARE 0.43..0.51, PreDist 0.59..0.73.
 D1 benchmark-best detector outside the deployment top-3 at 60-100% of the 5 budgets in every run
    (PreDist s0: pca_spe rank 6/8/10/13/2 at B 0.5/1/2/4/8; CARE s0: z_mean rank 4/4/4/4/7).
    Realised held-out FA (median over detectors) at B 0.5/1/2/4/8: CARE s0 1.84/1.84/2.20/3.39/6.76 (overshoot at
    low budgets); PreDist s0 0.33/0.81/1.66/2.87/5.73 (within budget).
 D2 leave-one-family-out: H9a diff positive in 25/25 CARE and 23/30 PreDist family drops; H9b positive in 25/25 and 30/30.

### 2026-11-28 03:58 UTC — leak-free PreDist seed 0 re-generated on a second container (G9)
Panel seed-0 scores of subs 4 and 7 rescored with PREDIST_EXCL_RULE=leakfree; plan_v2_analysis.py predist1 0 run in an
isolated root. cells.csv, summary.json and selection_per_detector.csv identical to the committed leak-free outputs
(produced on another container 2026-11-25). bootstrap.csv (not saved then) added to leakfree_outputs/seed0.
Leak-free seed 2 done by the chain (03:49). Seed 1 failed (race with a duplicate chain, killed); re-run pending.

### 2026-11-28 ~04:20 UTC — A1 + A2 on leak-free PreDist seed 0 (primary)
A1 (now computable with the regenerated leak-free bootstrap): H7a T1 0.060, T2 0.184; H7b T1 0.0070, T2 0.092.
Holm T1 rejects only PreDist H7b; Holm T2 rejects nothing -> no test "confirmed under A1" (unchanged verdict).
A2 leak-free seed 0: tau(ET,CHA) 0.43, tau(EH,CHA) 0.48, tau(CT,CHA) 0.72; H9a p 0.410, H9b p 0.162 (seed 2: 0.366,
0.153). Benchmark winner loop3s ranks 15/12/13/3/2 of 17 by deployment recall at B 0.5/1/2/4/8 (outside top-3 at 3/5
budgets); deployment winner at B <= 1 is the expert rule (recall 0.286). Realised held-out FA median 0.33/0.82/1.66/3.08/5.39.
