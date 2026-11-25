# Blind novelty review, cycle 5 (independent reviewer)

Date: 2026-11-25. I read only the files in the request, plus the results files they point to (`code/results/plan_v2/*/seed*/{bootstrap,selection_per_detector}.csv`, `code/results/leak_sensitivity/verdict.json`). I did not open any author scorecard, decision log, HANDOFF, PROGRESS, USER_DIRECTIVES or journal-folder file.
All paths are relative to `Target_Journal_Submission/`. The previous blind review is `review/blind_novelty_score_cycle4.md`, which scored 13/25.

## What changed since cycle 4

Cycle 4 recommended a pre-registered 2x2 factorial. The project then ran it as `code/experiments/plan_v2.md`.
- **Design.** 15-17 detectors. Factors: event windows vs continuous replay, and tuned-on-evaluated-events vs out-of-sample thresholds.
- **Seeds and correction.** Seeds 0-4, with Holm over 4 seed-0 tests.
- **Additional files.** A reproducibility re-run and a leak-sensitivity check (log, "plan_v2 PreDist seed-0 RERUN", "G8 leak sensitivity").
- **Plan v3 arm 1.** It reproduces the window-level balanced protocol of the in-journal competitor 100824 (log, "plan_v3 arm 1").

### I checked the numbers against the CSV and JSON files

I recomputed every Kendall tau in `code/results/plan_v2/summary.md` from `*/seed*/cells.csv`.
- **They match.** PreDist seed 0: ET 0.181, EH 0.633, CT 0.828. CARE seed 0: ET 0.435, EH 0.744, CT 0.305. All 10 dataset-seed rows match.
- **The Holm table matches `summary.json`.** H7a rejected on both datasets, H7b on PreDist only.
- **Leaving out the degenerate CARE `iforest_pca` does not change the direction.** That detector gives 0 in EH, CT and CH. Without it, CARE tau is ET 0.389, EH 0.703, CT 0.180.

The checks also exposed three problems, used in the scores below.

**1. The bootstrap is strongly biased on CARE (`care/seed*/bootstrap.csv`).**
- **Seed 0 is badly off.** The bootstrap mean of tau_ET is 0.168, while the point estimate is 0.435. The bootstrap mean of the H7b difference is +0.309, while the point estimate is -0.130.
- **The primary test does not survive two other methods.** For the confirmatory CARE H7a test (seed 0, point 0.310), the bootstrap mean is 0.522, a bias of +0.21 in the favourable direction.
  - The pre-registered percentile test gives p = 0.0055.
  - The basic (reflected) bootstrap CI is about [-0.32, 0.48], which includes 0.
  - A null-centred bootstrap p is about 0.065.
  - A within-detector ET/EH label-swap permutation test I ran is descriptive and not pre-registered. It gives p = 0.12 on CARE, against 0.016 on PreDist.
- **What still holds.** The pre-registered test was run as written, so the Holm verdict is formally valid. But the CARE confirmation of H7a depends on a percentile bootstrap of a statistic that is re-tuned inside each resample, and that statistic is visibly biased.
- **PreDist H7a is less affected.** Its bias is +0.01 at seed 0.

**2. The "deployment-like" reference is coarse and fragile.**
- **CH is a small count.** On PreDist it is recall over 28 faults (1-8 detections), giving 7-9 distinct values across 17 detectors. On CARE it is 0-12 of 45 events. The rankings have many ties.
- **Fixing a leak changes the PreDist results** (`leak_sensitivity/verdict.json`: robust = false).
  - One detector's CH moves by 4/28.
  - tau_ET moves from 0.18 to 0.34.
  - The H7a difference falls from 0.45 to 0.31 (p 0.017).
- **tau_ET on CARE varies from 0.16 to 0.43 across seeds,** although only 4 of 15 detectors are re-seeded.

**3. The selection effect is still detector-dependent.**
- **The pooled ratio comes mainly from detectors with 0 hits.** On PreDist, 0/35 curated normal events alarm for 10 of 17 detectors (`predist1/seed0/selection_per_detector.csv`). The autoencoders do not follow the pattern: ae is 0.97 and ae_cond is 2.02.
- **On CARE, robust_z_max goes the other way,** with a ratio of 3.2.

## Scores

| # | Dimension | Score | Justification |
|---|---|---|---|
| 1 | Differentiation from closest prior work | **2** | **Unchanged.** The concepts are already published.<br>• PreDist concedes the inflation and suggests random normal events (`literature/claim_table.md` C1; `literature/selection_effect_claim.md`).<br>• Cools 2026, Haneef 2026 and Liu 2026 already show test-set or same-asset threshold calibration inflating results and changing rankings, Liu and Haneef on CARE (C3).<br>• Spectrum bias is textbook.<br>**What is new.** A pre-registered decomposition that isolates threshold source from window design, run on two energy benchmarks. A panel-wide selection-effect measurement. The W-bal finding against 100824: 83-174 false-alarm days per substation-year at the oracle threshold (log, "plan_v3 arm 1").<br>**Why still 2.** This is a sharper measurement of known biases, not a new phenomenon. It is close to 3 only within Energy and AI, where `literature/journal_quality_bar.md` (e) finds no protocol-comparison paper. |
| 2 | Mechanism / explanation | **3** | **Stronger than cycle 4.** The tau 0.21 -> 0.64 anecdote (n = 9) is now a 2x2 decomposition on 15-17 detectors. Out-of-sample thresholds remove 40-68% of the ET disagreement on PreDist and 55% on CARE (H7c).<br>**But three problems remain.**<br>• **H7a is partly built in.** EH uses exactly the same held-out B = 2 threshold as the CH reference, and its fault-event recall is almost the same quantity as CH recall. So "EH agrees better with CH" partly follows from the design (`plan_v2.md`, cell definitions).<br>• **The window factor reverses on CARE without an explanation.** On CARE, CT is lower than ET in all 5 seeds. The likely cause is LOFO calibration failure, since thresholds overshoot the budget (ae_cond reaches 7.8 FA per turbine-year, log "Round 6 RESULTS"). The paper does not test this.<br>• **The selection effect does not hold for the AEs on PreDist.** |
| 3 | Evidence strength | **3** | **Up from 2.**<br>• H7a-d were pre-registered before any panel score existed (`plan_v2.md`).<br>• Holm was applied, and the PreDist seed-0 re-run is byte-identical.<br>• 5 seeds, 2 datasets, 2,000 cluster bootstraps.<br>• H7b on CARE is reported honestly as failed (0/5).<br>**Why not 4.**<br>• **The CARE H7a confirmation does not survive** a bias-corrected bootstrap or a permutation test (see check 1 above).<br>• **The "robust in 5/5 seeds" claims are not independent replications.** Only 4 stochastic members are re-seeded, and the other 11-13 detectors are identical in every seed.<br>• **The detector pool has near-duplicates.** z_max, z_mean, ewma_z_max, robust_z_max and q_frac form one family, and there are 6 PCA-space variants. The effective n is well below 15-17, and no inference is made over detectors.<br>• **The leak sensitivity fails the authors' own pre-registered robustness criterion** (`leak_sensitivity/verdict.json`).<br>• **The history is compromised.** M2 was burned twice, and the ledger has 82 variants with 15 M2 touches (`state/variants_tried_summary.md`).<br>• **The chance-level results are thin.** On M2, nothing beats chance after Holm except sigma3 at some budgets (`code/results/chance_level.csv`). |
| 4 | Breadth | **3** | **Wider than cycle 4.**<br>• Two domains (district heating and wind).<br>• 35 + 36 assets, with 64 and 95 events.<br>• 15-17 detectors from rule, statistical, PCA, density, kNN/LOF, IForest and AE families.<br>• Cross-manufacturer transfer, at an earlier stage.<br>**What is still missing.** No strong modern model (transformer, TSFM) is in the panel, although 100824 uses 5 strong time-series classifiers. Positives are few (28 and 45), and CARE farms do not have verified manufacturers. |
| 5 | Practical / scientific significance | **3** | **What operators and benchmark builders can use.**<br>• Benchmark-tuned thresholds imply 6.7-16.7 FA per turbine-year on CARE and 10-18 FA per substation-year on PreDist.<br>• Under W-bal oracle thresholds, every detector implies 83-174 false-alarm days per substation-year.<br>• Balanced-event recall of 0.69-0.84 shrinks to 0.04-0.29 under CH.<br>• Curated normal weeks are 2-3x quieter than random weeks.<br>**What limits it.**<br>• The "tolerable 1-2 FA/asset-yr" anchor is still unsourced (C2, UNVERIFIED).<br>• The constructive fix, the E* protocol, was falsified (log, "Round 7 results").<br>• No reporting rule or protocol has yet been validated as the deliverable.<br>• The transfer part largely repeats concurrent CARE work (Song, Vural, Haneef). |

**Total: 14 / 25. Not "VERY STRONG"** (below 20, with one dimension below 3).

| Dimension | Cycle 4 | Cycle 5 |
|---|---|---|
| Differentiation | 2 | 2 |
| Mechanism | 3 | 3 |
| Evidence | 2 | 3 |
| Breadth | 3 | 3 |
| Significance | 3 | 3 |
| **Total** | **13** | **14** |

The factorial was the right experiment and was run cleanly. Mechanism did not rise because one factor (window design) reversed on CARE, and the other (threshold source) is partly coupled to the reference by construction.

## Three biggest weaknesses

**1. The cross-domain confirmation of the headline mechanism (H7a on CARE) is statistically fragile.**
- **The bootstrap is biased in the favourable direction.** The percentile bootstrap of a re-tuned rank statistic is biased by about +0.21 on CARE seed 0. A basic-bootstrap CI and a label-swap permutation test both fail to exclude 0 (p of about 0.07 and 0.12). These are my own unregistered checks, described above.
- **PreDist is the more solid case, but it also wobbles.** It depends on a fault label that a leak fix shifts (diff 0.45 -> 0.31).
- **The claim cannot be stated without that context.** A statistically literate referee will recompute this. "Holm-confirmed on two domains" must not be stated without these caveats.

**2. The design partly decides its own conclusion, and the reference is coarse.**
- **The EH-CH coupling.** EH shares the held-out threshold, and almost the fault-recall definition, with the CH reference. That makes "threshold source dominates" partly mechanical.
- **CH is a poor reference.** It counts 1-12 detected faults across a correlated detector pool, so it has many ties and moves with single labels.
- **The second factor reversed on CARE (H7b 0/5).** So the clean "two separable causes" story holds only on PreDist.

**3. Differentiation remains incremental.**
- **Each phenomenon is already published or conceded.** Threshold leakage changing rankings, base-rate inflation and selected-negative bias are all in prior work. This includes the PreDist paper itself and concurrent CARE work: Song, unreviewed; Haneef; Liu, a preprint.
- **What the paper adds.** Careful measurement, which is not a new mechanism and not a validated fix. E* was falsified, and the plan_v3 window-arm hypotheses H8a and H8c were not supported.
- **The integrity history must be disclosed at length.** M2 was opened twice, and there are 82 variants. That disclosure weakens any confirmatory framing.

## (a) Would Energy and AI accept this as is? Likely decision and why

**No. The most likely decision is major revision, with some risk of rejection** if a reviewer from the concurrent CARE/PreDist community sees it.

**Why the topic fits.** The journal clearly publishes pure evaluation and audit papers: 100658, 100856, 100936 and 100942 in `literature/journal_quality_bar.md`. No paper in its 636-work corpus compares balanced-event and deployment protocols or uses CARE. The paper also targets a weakness of 100824, which uses an oracle macro F1 on PreDist, so the fit and the "gap" pitch are good.

**Where it falls short of the journal's evaluation papers.** The best of them (100942, 100824) pair their claims with critical-difference or Friedman/Wilcoxon statistics over strong modern baselines, and with clean ablations. This study does not yet match them on three points:
- **Statistics.** The headline inference is fragile under alternative bootstrap or permutation methods, and the reference metric depends on 28 and 45 positives.
- **Baselines.** There is no modern deep or foundation-model detector in the panel.
- **Constructive output.** The protocol fix was falsified, and the deployment-cost anchor (1-2 FA/yr) is unsourced.

**What reviewers will ask for.** A calibrated test, de-duplicated detectors, a modern baseline, a sourced alarm budget or a budget sweep, and a reporting checklist. Those are fixable in a major revision. Acceptance as is is unlikely.

## (b) Single most valuable change before submission

**Re-establish the H7a claim with a calibrated, detector-aware test, and report the result whichever way it falls.**

**Before any re-analysis.** Pre-register an amendment.

**The re-analysis.**
- **Data.** Use the leak-free PreDist data as primary.
- **Detector pool.** Collapse near-duplicate detectors into families: one z-score, one PCA-space, one density, one kNN/LOF, IForest, the rule, qnbm, ae and ae_cond. Alternatively, report the result at both granularities.
- **Inference.** Replace the percentile bootstrap with:
  - a bias-corrected (BCa or basic) bootstrap, or a double bootstrap, over assets that re-tunes inside each resample;
  - plus a within-detector permutation test of the ET/EH labels;
  - plus a leave-one-detector-family-out check.
- **Second reference.** Add a less tie-bound reference: area under the recall-FA curve over B in [0.5, 6], or alarm-days.

**What follows from the outcome.**
- **If H7a survives on both datasets,** it becomes the paper's defensible core claim, the one thing a referee cannot dismantle in an afternoon.
- **If it fails on CARE,** the paper must be re-framed now as a PreDist-anchored finding with a CARE replication of the selection and inflation effects. That is still publishable, but only if stated honestly.

**Cost.** This uses existing scores, so it needs only CPU minutes.
