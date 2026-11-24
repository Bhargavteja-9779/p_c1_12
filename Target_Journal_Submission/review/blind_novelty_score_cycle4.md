# Blind novelty review, cycle 4 (independent reviewer)

Date: 2026-11-24. I read only the files listed in the request. I did not open any author scorecard, decision log, PROGRESS or HANDOFF file, or the journal folder.
All paths below are relative to `Target_Journal_Submission/`.

## Scores

| # | Dimension | Score | Justification |
|---|---|---|---|
| 1 | Differentiation from closest prior work | **2** | Prior work already covers each mechanism. PreDist concedes the precision overestimate under its 50/50 split. Kim 2022, Salem & Ferrugem 2026, Cools 2026 and Liu 2026 show that protocol and threshold leakage change rankings, and Song 2026, Vural and Haneef report cross-farm failure on CARE (`literature/claim_table.md`, C1/C3/C5). Spectrum bias is a known concept that PreDist itself proposed testing (`literature/selection_effect_claim.md`). What remains new is quantification on two energy benchmarks, plus PreDist cross-manufacturer transfer. That is narrow and incremental. |
| 2 | Mechanism / explanation | **3** | Three mechanisms are identified: the base rate, tuning thresholds on the evaluated events, and quieter curated negatives. The tuning effect rests on one ablation: tau rises from 0.21 to 0.64 with n = 9 and p = 0.45 (log, "Round 5 results (2026-11-24, M1"). The selection effect is detector-dependent on PreDist: both autoencoders give ratios of about 1.0 ("H5d RESULT"). The transfer failure is explained only by post hoc diagnostics (loop availability, cold start; "LOCKED M2 RESULTS"). |
| 3 | Evidence strength | **2** | Some results are solid. The inflation CIs sit well above 5 on PreDist M1 ("PreDist M1 protocol-gap bootstrap CIs"), and CARE round 6 was pre-registered. Much else is weak: CARE uses seed 0 only (`results/round6/seed0/summary.json`); every ranking-change tau is non-significant (p = 0.45, n = 5 and 9); H6e failed; and the H5d CI code was added after the first run. On multiplicity, M2 was opened twice by unaware sessions, there are 15 M2 touches and 82 variant rows, and the scorecard was written after the test (`state/variants_tried_summary.md`). Every M2 number after the first evaluation is post hoc, including the M2 protocol gap whose event point was chosen on M2 itself (`results/protocol_gap/m2_gap.csv`). |
| 4 | Breadth | **3** | The study covers two domains (district heating and wind), two control-unit manufacturers, 3 farms (36 turbines) and 5-9 detectors. The fault counts are small: 25-29 per PreDist split and 45 on CARE. The rule detects 2/25 on M2. Only one stochastic seed was run on CARE, and IForest gives no alarms there at its LOFO point. |
| 5 | Practical / scientific significance | **3** | Operators and benchmark designers can use these numbers. They include FA per asset-year at benchmark-chosen thresholds (6.7-16.7 on CARE, 3.2-112.6 on M2), the 16-274x precision inflation, and power of 0.12-0.35 to resolve 1 vs 2 FA/yr. The "tolerable ~1-2 FA/asset-yr" reference is unsourced (UNVERIFIED, `claim_table.md` C2). The transfer result mostly repeats concurrent CARE work. On M2 only sigma3 and qnbm beat chance after Holm, and sigma3's apparent success is a cold-start artefact (`results/chance_level.csv`; log "LOCKED M2 RESULTS"). |

**Total: 13 / 25. Not "VERY STRONG"** (below 20, and two dimensions are below 3).

## Three biggest weaknesses
1. **Low differentiation.** Each headline effect is a textbook or already-published mechanism. PreDist itself acknowledges the inflation and suggests random normal events. Song, Haneef and Liu cover ranking changes and transfer on CARE. The paper is a careful measurement of known biases, not a new finding.
2. **Compromised and thin confirmatory evidence.** The held-out M2 was evaluated twice, and every M2 protocol-gap number is post hoc. The CARE confirmation is one seed. The ranking-inversion claim (C3) has tau 0.21-0.40 with p = 0.45, so it is not statistically established on either benchmark. Multiplicity across 82 variants and three lineages is large, and the reported ranges mix comparisons. For example, "16-274x" combines the in-sample-B2 baseline with the same-point baseline across M1 and M2.
3. **The core "mechanism" claims are under-identified.** The "most of the inversion comes from tuning on evaluated events" decomposition rests on one point estimate of tau from 9 methods without a CI. The selection effect fails for the autoencoders on PreDist (ratio about 1.0). The transfer failure is explained only after the fact, and the FA-budget reference is unsourced.

## Most valuable additional experiment (feasible on 4 CPU cores in < 10 h, public data)
**A pre-registered 2x2 decomposition with a larger detector pool and multiple seeds, run on CARE and PreDist M1.**
- **Factors.** Evaluation unit: balanced event windows vs continuous replay. Threshold source: tuned on the evaluated events vs set from held-out normal operation, using LOFO/LOSO at a fixed FA budget.
- **Detector pool.** About 20 cheap configurations, for example sigma-k, quantile NBM, IForest, PCA/T2, kNN distance and small AEs over a few hyperparameters. Run seeds 0-4 for the stochastic ones.
- **Statistics.** Report Kendall tau for each cell with a bootstrap or permutation CI over detectors and events. Test the "threshold-source" main effect against the "event-window" main effect directly. Apply Holm across the pre-registered contrasts.

This turns C3 from a non-significant n = 5/9 anecdote into a powered, identified mechanism replicated on both benchmarks. It also fixes the single-seed CARE weakness. It should raise Mechanism and Evidence by about 1 point each, honestly, without touching M2. It does not fix Differentiation. Only a result that contradicts or goes beyond Song/Haneef/PreDist can do that.
