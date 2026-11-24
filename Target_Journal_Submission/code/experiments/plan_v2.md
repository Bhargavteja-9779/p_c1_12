# plan_v2 — 2x2 protocol factorial with an enlarged detector panel (cycle 5)
Written 2026-11-24 ~17:45 UTC BEFORE any panel score was computed (results/scores_panel/ does not exist).
Reason (state/decisions.md D-17): score of record 13/25; blind reviewer: ranking claims rest on 5-9 methods with no
significant tau; suggested a 2x2 design (window design x threshold source) with ~20 detectors and seeds 0-4.
plan_v1 = protocol.md + amendments + Round 5/6 pre-registrations (unchanged; never edited in place).

## Data (all previously used, so this is a pre-registered EXPLORATORY analysis, not a blind test)
PreDist M1 (35 substations, development manufacturer) and CARE (36 turbines, 3 farms). M2 is not used (burned, D-03).
The 12 generic panel detectors have never been run on either dataset.

## Detector panel (fixed now; src/models/panel.py)
Generic (both datasets, one online pass, retrain every 90 d on own past, threshold = own 99th pct of training):
z_max, z_mean, robust_z_max, q_frac, pca_spe, pca_t2, maha_lw, knn_pca, lof_pca, gmm_pca, iforest_pca, ewma_z_max
(stochastic: knn_pca, lof_pca, gmm_pca, iforest_pca; seeds 0-4).
Plus existing detectors (seed 0 scores, identical in every seed's panel): PreDist rule, loop3s, qnbm, ae, ae_cond
(17 detectors); CARE temp3s, ae, ae_cond (15 detectors). sigma3 / iforest are excluded (near-duplicates of z_max /
iforest_pca, which would inflate n).

## Four cells per detector (same online scores, same alarm logic, same tau x c grid as before)
- ET  event windows, thresholds TUNED on the evaluated events: best event F0.5 over the grid (benchmark practice).
- EH  event windows, thresholds chosen OUT OF SAMPLE: event F0.5 at the held-out B = 2 point.
- CT  continuous replay, thresholds tuned IN SAMPLE: pooled recall at the best in-sample point with FA <= 2/asset-yr.
- CH  continuous replay, OUT-OF-SAMPLE thresholds = REFERENCE (deployment-like): pooled recall at the held-out B = 2 point.
Out-of-sample: CARE leave-one-farm-out; PreDist 5-fold substation CV (folds fixed by rng(0) permutation of the sorted
substation list). Events: CARE all 95 (window [start, end)); PreDist efd_possible faults (7 d before report) +
normal events. ONE fixed event set per dataset and seed: events whose window has >= 1 score of the panel member
z_max (a detector without a score there predicts "no alarm"), so all detectors are ranked on the same events.
Random windows (H7d) need >= 50% z_max score coverage. Holm is applied in scripts/plan_v2_summary.py over the
4 seed-0 p-values.

## Hypotheses (seed-0 panel primary; one-sided cluster bootstrap over assets, 2,000 resamples, rng(0); tuned
cells re-tuned inside each resample, held-out points fixed)
 H7a (threshold source): tau(EH, CH) - tau(ET, CH) > 0, CI excludes 0.
 H7b (window design):    tau(CT, CH) - tau(ET, CH) > 0, CI excludes 0.
 Holm over {H7a, H7b} x {PreDist M1, CARE} (4 tests), alpha 0.05.
 H7c (descriptive): share of the ET disagreement removed by out-of-sample thresholds:
     (tau_EH - tau_ET) / (1 - tau_ET), and by continuous replay: (tau_CT - tau_ET) / (1 - tau_ET).
 H7d (selection effect across the panel): pooled alarm-hit ratio (curated normal events / 2,000 random eligible
     normal windows of the event-type length: 7 d PreDist; CARE: length drawn from the normal-event lengths), at each
     detector's held-out B = 2 point, < 1 with CI excluding 1, per dataset; plus the share of detectors with ratio < 1.
 Robustness: seeds 1-4 (stochastic members re-seeded); each hypothesis reported as the number of seeds (of 5) in
 which it holds at the unadjusted 0.05 level; claimed as robust only if >= 4/5.
Multiplicity ledger: this plan adds 4 confirmatory tests + 2 descriptive families; recorded in variants_tried.csv.

## Compute
Panel: ~1 machine-h per seed for both datasets (smoke test: 3 s/fit PreDist, 13 s/fit CARE farm C, peak 2.5 GB).
5 seeds ~5 machine-h with 2 workers (cycle 5 budget 15 h). Analysis: scripts/plan_v2_analysis.py (committed
before the panel jobs are launched).
