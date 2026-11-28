# Peer review: "Benchmark scores do not show deployable fault detection: false-alarm burden and curated-normal bias on district heating and wind turbine data" (manuscript v2, 2026-11-28)

Reviewer role: external referee for *Energy and AI*. Sources read: submission/manuscript.md, all six figures in submission/figures/*.png, submission/NUMBER_SOURCES.md, the result files it points to (under code/results/), the pre-registrations code/experiments/plan_v2.md, plan_v2_amendment_A1.md and plan_v2_amendment_A2.md (plus plan_v3.md and leak_sensitivity.md, which NUMBER_SOURCES relies on), code/experiments/novelty_escalation_log.md (cited by NUMBER_SOURCES as the source of Round 6 and power numbers), and literature/claim_table.md, literature/prior_art_recheck_2026-11-28.md and literature/journal_quality_bar.md. I did not open the authors' self-assessment files.

---

## 1. Summary of the paper

The paper asks how far the standard evaluation of early-fault-detection benchmarks is from deployment. The standard view uses balanced event windows with curated normal periods and thresholds tuned on the scored events. Deployment means continuous operation with a fixed threshold and a tolerable false-alarm budget. On two public labelled benchmarks, PreDist (35 district-heating substations, 29 faults) and CARE to Compare (36 turbines, 45 anomalies), a pre-registered panel of 15–17 detectors is scored from the same online scores under a 2×2 protocol design (event windows or continuous replay, crossed with thresholds tuned in sample or chosen out of sample).

The authors report three main results:
- **Burden.** Benchmark-optimal thresholds imply 6.7–16.7 false alarms per turbine-year and 83–176 false-alarm days per substation-year.
- **Curated-normal bias.** Curated normal periods draw alarms at 0.21–0.42 times the rate of random normal windows.
- **Ranking.** The benchmark winner is rarely the deployment winner across budgets.

A pre-registered test of what drives the ranking disagreement (threshold source and window design) is honestly reported as not established under calibrated tests. The paper ends with a six-item reporting checklist.

## 2. Recommendation: **major revision**

The question fits the journal well. Its quality bar shows that *Energy and AI* publishes audit-style evaluation papers that "quantify how far standard practice misleads" and close with a reporting rule (100856, 100936, 100788, 100658). No paper in the journal, and none of the 75 works citing PreDist or CARE, replays benchmark thresholds over continuous operation or compares curated with random normal periods. The pre-registration, the calibrated re-tests, the leak correction and the candid negative result are well above the rigour of most fault-detection papers in this journal.

The paper is not acceptable in its current form, for four reasons:
- **Internal consistency and accuracy.** Some headline claims are specific to one seed or over-generalised. Some numbers do not match the source files. The leak-sensitivity outcome is misdescribed. A placeholder tag remains in the text. Several pre-registered hypotheses that failed are not reported.
- **Comparability of the two burden numbers.** They come from different protocols, and for CARE from a five-detector side analysis rather than the panel. The PreDist number does not measure the benchmark's own practice.
- **Missing chance and trivial references.** Without them the reader cannot tell which deployed recalls of 0–32% are better than random alarms at the same rate.
- **Presentation below the journal's evaluation papers.** There is no dataset table, no timeline figure, no lead-time analysis, no graphical abstract, 37 references against a typical 60–90, and 6 figures against a median of about 10.

Most of this can be fixed without new data, so a major revision, not a rejection, is the fair verdict.

## 3. Novelty score (rubric, 0–5 each)

| Dimension | Score | Reason |
|---|---|---|
| Differentiation from prior work | 3 | The measurements are new for energy benchmarks: continuous replay of benchmark thresholds, FA per asset-year, and the curated-versus-random normal ratio. The concepts are not new: base rate, threshold leakage, low-FA re-ranking and spectrum bias. The paper says so for base rate and leakage, but not for spectrum bias (comment M7). Song 2026 [7] and Haneef 2026 [8] overlap the alarm-budget and cross-asset parts on CARE and deserve a sharper contrast. |
| Mechanism / explanation | 2 | The burden is explained by base rate and in-sample tuning, which is textbook. The curated-normal effect is measured but not explained. There is no analysis of why curated periods are quieter (season, operating regime, data coverage, unlabelled faults in random windows), and the effect varies by detector (ae_cond 2.45, robust_z_max 3.20) without explanation. The ranking mechanism is a negative result. |
| Evidence strength | 3 | The study is pre-registered, uses cluster-bootstrap CIs, calibrated re-tests, multiple seeds and a leak-free re-run reproduced on a second machine. Against this: the CARE burden uses 5 non-panel detectors; the seeds mostly do not re-seed the detectors; leak-free PreDist has only 3 seeds; there is no chance baseline; and several reported numbers do not match the files (Section 4.3). |
| Breadth | 3 | Two asset classes and 15–17 detectors from 6 families. There is no modern deep or foundation-model detector, no lead-time or earliness analysis, the second PreDist manufacturer is excluded, and the PreDist burden is computed under a different protocol from CARE. |
| Significance | 3 | The result is directly useful to benchmark maintainers and operators: the checklist and FA per asset-year as a reporting unit. The impact is limited by the small event counts and the inconclusive ranking result. |
| **Total** | **14 / 25** | |

## 4. Comments

### 4.1 Major comments

**M1. Seed-specific and over-generalised ranking claims in the Highlights and Abstract.** The fifth highlight reads: "The benchmark winner ranks 13th of 17 in deployment at two false alarms per year." This holds only for leak-free PreDist seed 0, where the winner is loop3s:
- in leak-free seed 2, the benchmark winner is knn_pca, and it ranks **1st** at B = 2 and 2nd at B = 1 (amendment_A2/predist1_leakfree_seed2.json, D1_regret);
- in all five legacy seeds, the winner is pca_spe, ranking 6th to 15th.

The identity of the "benchmark winner" changes with the seed and with the leak fix because the top ET scores are separated by 0.01–0.02 (loop3s 0.843, lof_pca 0.826, maha_lw/gmm_pca 0.825). This instability is itself a finding worth reporting. However, a single rank must not be a highlight.
- *Action:* replace the highlight with the multi-seed statement ("outside the deployment top three at 60–100% of budgets in every seed–dataset run"). Report the winner's identity and rank per seed in a supplementary table. Discuss the near-ties in ET explicitly.

**M2. "Choosing thresholds out of sample improves agreement in every seed" depends on the reference, and the reference is partly mechanical.**
- Against CH (B = 2) the claim holds. However, Amendment A2 itself notes that "EH and CH share the identical held-out threshold, which partly builds in H7a". The manuscript does not tell the reader this.
- Against the multi-budget reference CHA, the claim fails in at least one seed: legacy PreDist seed 3 has τ(EH, CHA) = 0.473 < τ(ET, CHA) = 0.492. In leak-free seed 0 the gain is only 0.43 → 0.48 (H9a diff 0.055, p = 0.41).

*Action:*
- state the shared-threshold coupling in Section 5.5 and in the Fig. 2 caption;
- qualify the abstract sentence ("against the B = 2 reference");
- report the CHA-based per-seed differences next to the CH-based ones.

**M3. The two burden numbers are not comparable, and the PreDist one does not measure the benchmark's own practice.**
- *CARE.* The 6.7–16.7 FA/turbine-year comes from Round 6 (results/round6/seed0/), which covers five detectors: temp3s, sigma3, iforest, ae, ae_cond. Two of these (sigma3 and the Round-6 iforest) are not in the pre-registered panel. plan_v2 explicitly excluded them as near-duplicates, and the Round-6 iforest has ET 0.603 against 0.586 for the panel's iforest_pca. Section 3.2 never describes a "three-sigma" detector for CARE.
- *PreDist.* The 83–176 FA-days/substation-year is computed under a window-level, balanced, oracle-macro-F1 protocol in the style of van Dreven et al. [14] (plan_v3). It is not computed under the PreDist benchmark's own event-F0.5 practice. Highlight 3 nevertheless says "the same practice implies…".
- *Units.* The two numbers use different units: alarm starts versus alarm-days.
- *Earlier event-F0.5 numbers exist.* novelty_escalation_log.md records an earlier PreDist analysis at event-F0.5 benchmark points (1.2–18.3 FA/substation-year on an older detector set). It is not reported.

*Action:*
- compute the CARE burden at the ET point for all 15 panel detectors, and the PreDist burden at the ET (event F0.5) point for all 17 detectors, both in FA starts per asset-year with cluster CIs. The cached per-detector grids should make this feasible without new data;
- report the van-Dreven-style FA-days as a separate, clearly labelled second protocol;
- reword Highlight 3 and the abstract accordingly;
- give the precision-inflation factor for PreDist too, or say why it is CARE-only.

**M4. Chance and trivial references are missing.** For the event cells, an "always alarm" detector already scores event F0.5 ≈ 0.53 on CARE (45/95 positives) and ≈ 0.51 on PreDist (29/64). The CARE ET range of 0.57–0.69 is therefore only slightly above trivial, which weakens "every detector looks useful". For CH, random alarms at B = 2 FA/asset-year already hit a 7-day window with probability of about 1 − exp(−2·7/365) ≈ 0.04, and more for longer CARE events. Several deployed recalls (0.04–0.11) may not differ from chance.

*Action:* add an always-alarm row to Table 2 and a random-alarm-at-matched-realised-rate reference (with CI) to Table 2 and Fig. 5. State how many detectors beat chance at each budget. This needs no new data.

**M5. Fidelity of "benchmark practice" (ET).**
- *CARE.* The CARE score combines pointwise F0.5, accuracy on normal periods, event F0.5 and earliness. ET uses only event F0.5.
- *PreDist.* PreDist picks its threshold by 5-fold CV over the evaluated events, not fully in sample.

The ET cell is therefore a stylised benchmark, not the published scoring. *Action:* either compute the official CARE score and the PreDist CV-over-events threshold for every detector and show that the conclusions hold, or rename ET (for example "event-window, in-sample tuned") and discuss the difference in Section 4.1.

**M6. Not all pre-registered outcomes are reported, and the leak sensitivity is misdescribed.**
- *Leak sensitivity.* The pre-registered leak-sensitivity criterion (experiments/leak_sensitivity.md) was "robust only if every H7/H8 verdict is unchanged and no detector's CH changes by more than 1 fault". verdict.json gives `robust: false`: H8c flipped, and lof_pca changed by 4 faults. Section 6.3 says only "Every conclusion kept its direction". That statement is true for the headline directions, but it hides a pre-registered failure.
- *H8a.* The pre-registered prevalence-drop hypothesis is not supported (min drop 0.123 < 0.15) and is not mentioned.
- *H8c.* Under the leak-free rule, τ(W-bal, CH) = 0.217 with CI [−0.18, 0.50]. This is also not mentioned.
- *H6e.* The pre-registered "inflation CI lower bound > 5" hypothesis failed for sigma3 (lower bound 4.98, which the manuscript rounds to 5.0) and was undefined for iforest. It is not mentioned.
- *plan_v3 CARE arm.* plan_v3 pre-registered a CARE arm and Holm over H8a–c × 2 datasets. The CARE arm appears not to have been run, and this is not disclosed.

*Action:* add a short pre-registration ledger (Supplementary table) listing every pre-registered hypothesis with its verdict, and correct the leak sentence to state the pre-registered criterion and that it failed.

**M7. The curated-normal effect needs a mechanism and an alternative explanation.**
- *Alternative explanation.* The ratio is below 1 if curated periods are quieter. It is also below 1 if "random eligible normal" windows contain unreported faults. The paper notes elsewhere (Section 6.3) that the absence of a report does not mean no fault. These two readings have different implications: benchmark construction versus label incompleteness.
- *Confounds.* Season and operating state are obvious candidates. In district heating, summer weeks with heating off are quiet.
- *Small counts.* On PreDist the per-detector ratios rest on 0–3 hits out of 35 curated events (selection_per_detector.csv).

*Action:*
- stratify or match the random windows by month and operating regime;
- exclude random windows within ±X days of any service record, fault, disturbance or exclusion interval;
- report the per-detector counts with exact CIs;
- relate the effect to the spectrum-bias and case-control literature (Ransohoff & Feinstein 1978; Lijmer 1999; Rutjes 2006), which is listed in the authors' own claim_table but not cited.

Contribution 2 says "We identify… a selection effect". It should say that the known spectrum or case-control bias is measured for the first time in energy fault-detection benchmarks.

**M8. Seeds and the robustness claim.**
- plan_v2 states that only knn_pca, lof_pca, gmm_pca and iforest_pca are stochastic, and that the AEs are seed-0 in every panel. The AE rows are indeed identical across seeds.
- However, pca_spe, pca_t2 and maha_lw also change across seeds, both in ET and in CH. For example, PreDist pca_spe ET is 0.824 in seed 0 and 0.843 in seed 2, and CARE pca_t2 CH ranges from 0.089 to 0.200. The manuscript does not explain this.
- Leak-free PreDist exists for seeds 0, 2 and 3 only (seed 1 is empty), and A2 leak-free for seeds 0 and 2 only.

*Action:* explain what a "seed" changes. Re-seed the two AEs or state clearly that the AE training variance is not covered. Complete the leak-free seeds, or state the number of seeds behind every claim, and remove the "[LEAKFREE_SEEDS_PENDING]" tag (Section 5.3).

**M9. Operator-relevant outputs that are missing.**
- *Lead time.* There is no lead time or earliness, although CARE scores earliness and operators value it.
- *Cost of operation.* There is no compute cost or latency.
- *Qualitative evidence.* There is no qualitative example (score and threshold timelines before a documented fault, with false alarms marked). The journal's best evaluation papers include these (quality bar §(d) items 3, 16 and 17).
- *Budget calibration.* "Held-out calibration does not reliably deliver the target budget" is based on medians over detectors. Half of the PreDist detectors may still exceed the target.

*Action:* add median lead time of detected faults per budget, one timeline figure per dataset, and the full distribution (or interquartile range) of realised FA rates per budget.

### 4.2 Minor comments

1. Section 4.2 says the pre-registered test used "Holm's correction over the two datasets". plan_v2 applies Holm over four tests ({H7a, H7b} × {PreDist, CARE}). Please correct.
2. Section 5.6 refers to "The 65 normal 7-day windows of PreDist". The study data (M1) contain 35 curated normal events. 65 is the full PreDist (M1 + the excluded M2; novelty_escalation_log.md, H5e). Recompute the power for 35, which will be lower, or state that the figure refers to the full public benchmark.
3. Section 3.1 gives 29 faults, but recall denominators are 28 (CH values are multiples of 1/28, and Section 6.3 says "4 of 28 faults"). Explain which fault is not replayable.
4. Section 5.5 says "the increase appears in all five seeds of both datasets". For PreDist this refers to the legacy rule; the leak-free version has 3 seeds. Say so.
5. Section 5.4 says "Across all ten seed–dataset runs". There are 12 A2 runs (5 CARE, 5 legacy, 2 leak-free). Specify which ten.
6. Abstract: "15–17 detectors… evaluated under four protocols". The burden results are not computed on this panel (M3). Align the wording.
7. Table 2 mixes PreDist "expert rule" and CARE "temp. 3σ" in one row. Split the row or footnote it. Add a family column.
8. The inflation factor for ae_cond uses a held-out point that realised 7.8 FA/turbine-year, not 2. Note that the deployed precision is measured at the realised, not the target, rate.
9. References: [6] is a WES Discussions preprint and should be labelled "preprint"; [7] is correctly labelled unreviewed. Add scada-fault-bench (10.5281/zenodo.24164281, "false alarm hours per year" on wind SCADA), which is listed in the authors' claim table, and the cross-domain "1–3 FA per stream-year manageable" analogues (Dórea 2013; Nocentini 2023) to Section 2.
10. Define every metric by an equation: event F0.5, FA per asset-year (alarm-start counting, exposure, exclusion intervals), the selection ratio, and CHA.
11. Nomenclature: τ denotes both the threshold (Section 3.2) and Kendall's tau. Use another symbol for the threshold, for example θ.
12. Section 6.1: "simple physically anchored rules can beat every learned detector" holds for PreDist B ≤ 1 at seed 0. On CARE the best detector at tight budgets is ae_cond. Qualify.
13. Data availability: give the exact dataset versions (CARE record version, PreDist DOI version) and the commit hash of the code.

### 4.3 Number check (spot-check against the files in NUMBER_SOURCES.md)

**Mismatches found:**

| # | Manuscript | Source file value | File |
|---|---|---|---|
| 1 | Table 2, PreDist ET robust_z_max **0.69**; text "ranges from **0.69** to 0.84" | 0.68493 → **0.68** | leak_sensitivity/leakfree_outputs/seed0/cells.csv |
| 2 | Table 2, PreDist ET maha_lw **0.83** | 0.82474 → **0.82** | same |
| 3 | Table 2, PreDist ET gmm_pca **0.83** | 0.82474 → **0.82** | same |
| 4 | Table 2, PreDist ET ewma_z_max **0.77** | 0.76471 → **0.76** | same |
| 5 | Table 2, CARE ET lof_pca **0.60** | 0.59459 → **0.59** | plan_v2/care/seed0/cells.csv |
| 6 | Section 5.6, "**65** normal 7-day windows of PreDist" (power 0.23) | Study data have 35 normal events (summary.json: n_events 64, 29 faults); 65 = M1 + M2 (novelty_escalation_log.md, H5e) | — |
| 7 | Section 6.3, "Every conclusion kept its direction" (implied robustness) | Pre-registered leak-sensitivity verdict `robust: false` (H8c flipped; max ΔCH = 4 faults) | leak_sensitivity/verdict.json |
| 8 | Section 4.2, Holm "over the two datasets" | Holm over 4 tests (thresholds 0.0125/0.0167/0.025/0.05) | plan_v2/summary.md, plan_v2.md |
| 9 | Section 5.3, "[LEAKFREE_SEEDS_PENDING]" placeholder left in text | leakfree_outputs/seed1/ is empty; seed4 absent | — |
| 10 | NUMBER_SOURCES.md numbers figures as "Fig. 4" (seed robustness) and "Fig. 3" (per-detector selection) | In the manuscript these are Fig. 6 and Fig. 4 | bookkeeping only |

Items 1–5 do not change any conclusion, because loop3s remains the PreDist ET winner at 0.84. They do show that Table 2 was not regenerated from the cited file.

**Numbers checked and confirmed (38):**
- *Table 2, other cells.* All other PreDist ET/CH values (z_max 0.75/0.21, z_mean 0.78/0.18, q_frac 0.73/0.07, pca_spe 0.82/0.14, pca_t2 0.78/0.25, knn 0.81/0.29, lof 0.83/0.29, gmm CH 0.32, iforest 0.77/0.29, rule 0.75/0.29, loop3s 0.84/0.11, qnbm 0.70/0.11, ae 0.73/0.14, ae_cond 0.74/0.07). All other CARE ET/CH values (z_mean 0.69/0.16, ae_cond 0.67/0.27, iforest 0.59/0.00, temp3s 0.66/0.16, etc.).
- *Ranges.* CH ranges 7–32% and 0–27%. CARE ET range 0.57–0.69.
- *τ values.* τ ET/EH/CT, PreDist leak-free 0.34/0.65/0.83; legacy ET 0.18; CARE 0.43/0.74/0.30.
- *Pre-registered p-values.* Leak-free 0.017 and 0.012; CARE 0.0055 and 0.15. All Holm decisions in Table 3 are correct under 4-test Holm.
- *A1 p-values.* T1/T2: 0.060/0.18, 0.007/0.092, 0.065/0.18, 0.68/0.61.
- *A2 p-values.* Seed-0 label-swap: 0.41, 0.16, 0.16, 0.11. CARE H9a p < 0.05 in 2/5 seeds and H9b in 0/5. LOFO: H9a 25/25 CARE and 5/6 leak-free PreDist; H9b positive in all drops.
- *τ(ET, CHA).* CARE −0.06 to 0.12; PreDist 0.43; legacy 0.30–0.49.
- *Benchmark winner.* PreDist ranks 15/12/13/3/2; CARE 4/4/4/4/7; outside the top three at 60–100% of budgets; expert rule 0.29 at B ≤ 4.
- *Realised FA medians.* 0.33/0.82/1.66 and 1.84/1.84/2.20.
- *Selection ratios.* 0.21 (0.05–0.37), legacy 0.30 (0.11–0.52), CARE 0.42 (0.27–0.61). Detectors below 1: 16/17 and 13/14. Ten PreDist zeros. ae_cond 2.45; robust_z_max 3.20. Leak-free seeds 0.18–0.23.
- *CARE burden.* 6.7 / 10.6 / 10.8 / 15.8 / 16.7. Inflation 7.6 (4.98–16.7) and 20.6 (13.5–37.4). Precision 0.55–0.84 versus 0.036–0.071.
- *PreDist burden.* 83–176 FA-days, median 135.5. Macro F1 0.50–0.53. 45,632 / 221 / 442 days.
- *Power and fleet figures.* Power 0.12 / 0.35 at 14.9 d. Fleet extrapolations 13,500 and 240–600.
- *Leak.* 4/588 refits, substations 4 and 7. CH fault counts 2–9 and 0–12. Dataset sizes 35/29/64 and 36/95/45.

## 5. Writing and presentation

- **Clarity.** The prose is clear, short-sentenced and largely free of hype. The 2×2 design is well explained by Fig. 1 and Table 1. The negative result in Section 5.5 is reported candidly and well, and Table 3 is a model of transparent reporting.
- **Structure compared with the journal's best evaluation papers** (100824, 100942, 100856):
  - *Present:* Introduction with a contribution list, related work, data, protocol, results, discussion with practical implications, limitations in bullets, a checklist, and a declarations block.
  - *Missing:* a dataset summary table, a methods table (family, parameters, stochastic yes/no), metric equations, a roadmap paragraph, a graphical abstract, a qualitative timeline figure, lead time, compute cost, and a pre-registration ledger.
  - *Below the bar:* references (37 against 60–90) and figures (6 against a median of about 10).
  - *Bullets in the body:* the extensive use of bullet lists in Results and Related work reads more like a report than a journal article. Convert most of them to prose.
- **Overstated claims:**
  - Highlight 5 and the abstract ranking sentence are seed-specific (M1).
  - "Same practice" in Highlight 3 is inaccurate (M3).
  - "Improves agreement in every seed" depends on the reference, which is partly built in (M2).
  - "Every detector looks useful" ignores the trivial baseline (M4).
  - "We identify… a selection effect" overlooks spectrum bias (M7).
  - Section 6.3's leak sentence hides a failed pre-registered criterion (M6).
- **Understated claims:**
  - The instability of the "benchmark winner" across seeds and the leak fix, with ET differences of 0.01–0.02 deciding the winner, is a strong argument for the paper's thesis and is not used.
  - The near-chance natural-prevalence macro F1 (0.50–0.53, i.e. "never alarm") is a striking result buried in one sentence.
- **Figures:**
  - Fig. 1: clear.
  - Fig. 2: shows percentile-bootstrap CIs that the authors themselves call biased. Show basic or null-centred CIs instead.
  - Fig. 3: informative. Leader lines (loop3s, z_mean) do not touch their points, and two CARE markers overlap.
  - Fig. 4: good. Annotate the per-detector hit counts (0–3 of 35).
  - Fig. 5: the most useful figure. Add a chance band and mark the B = 2 pre-registered budget. The PreDist "deployment winner" is the best by mean, which should be stated in the legend.
  - Fig. 6 (file fig5_seed_robustness.png): plots the biased legacy-rule p-values and adds little. Replace it with per-seed calibrated (T2/A2) p-values or per-seed τ differences. Rename the file to match its number.
- **Tables:** Table 2 needs the corrections in Section 4.3, chance rows and a family column. The CARE burden table in Section 5.2 is unnumbered. Number it and extend it to the panel (M3).

## 6. The three changes that would most improve the chance of acceptance (ordered by value per effort)

1. **Make every claim exact and complete (highest value, lowest effort; no new data).**
   - Correct the five Table 2 values, the "65" windows, the Holm description and the leak sentence. Remove the placeholder.
   - Rewrite Highlight 5 and the abstract ranking sentence as multi-seed statements.
   - Reword "same practice" for PreDist.
   - State the EH–CH shared-threshold coupling.
   - Add a pre-registration ledger with every verdict, including the failed H6e, H8a and H8c, the leak-robustness criterion and the unrun plan_v3 CARE arm.
   - Cite spectrum-bias prior work.

   *Feasible without new data:* yes, in full.

2. **Put both burden numbers and all rankings on the same footing, and add chance references (high value, moderate effort; no new data, re-analysis of cached scores and grids).**
   - Compute the ET-point burden (FA starts per asset-year, cluster CIs) and the inflation factor for all 15 CARE and all 17 PreDist panel detectors.
   - Report the van-Dreven-style FA-days as a clearly separate second protocol.
   - Add always-alarm and random-alarm-at-matched-rate baselines to Table 2 and Fig. 5.
   - Optionally compute the official CARE score and the PreDist CV-over-events threshold as a fidelity check of ET.

   *Feasible without new data:* yes. Only compute on existing scores is needed.

3. **Explain the curated-normal effect and bring the presentation to the journal's evaluation-paper standard (high value, moderate to high effort).**
   - Match the random windows by season and operating regime, and exclude windows near any service record (a label-noise control). Give exact per-detector counts.
   - Add a dataset table, metric equations, lead time per budget, one score-timeline figure per dataset and a graphical abstract.
   - Expand the references to about 60.
   - Complete the leak-free seeds, or clarify what a seed changes and re-seed the AEs.

   *Feasible without new data:* the analyses on PreDist and CARE are, since they use existing public data and cached scores. Completing the leak-free seeds and re-seeding the AEs needs new compute but no new data.
