# Submission package and honest assessment (2026-11-25)

Target journal: **Energy and AI** (Elsevier, ISSN 2666-5468).
The package is `submission/manuscript.md` and `submission/manuscript.docx`, with figures in `submission/figures/`. Every number is traced in `NUMBER_SOURCES.md`, and the 34 references were checked by DOI in `references_crossref.txt`.

## 1. Bottom line

**This is the most defensible version of the paper. It is NOT certain, or even likely, to be accepted as is.**
- Of the project's 11 quality gates, the two hard ones still fail:
  - novelty (G3): 14/25 by blind review, against a target of 20;
  - review time (G1): Energy and AI's verified median is 89 days from receipt to acceptance, against the 72-day rule.
- The independent blind reviewer predicts **major revision, with some risk of rejection**.
- I have not inflated any claim to improve the odds. A reviewer who checks the numbers will find them correct, which is what protects the paper.

## 2. What improved in this round (cycles 4 → 5)

| Before (cycle 4) | Now (cycle 5) |
|---|---|
| Ranking claim rested on 5–9 detectors, with tau p = 0.45 | 15–17-detector pre-registered panel; 2×2 factorial separating threshold source from window design; 5 seeds on both datasets |
| CARE confirmation used seed 0 only | CARE seeds 0–4 complete |
| Statistics used an uncorrected percentile bootstrap | Holm-corrected pre-registered test, plus a calibrated amendment (null-centred bootstrap and label-swap test) that was pre-registered before it was run |
| PreDist leakage was unquantified | Leak quantified (4/588 refits); leak-free results are primary and legacy results are a sensitivity check |
| Selection effect failed for the autoencoders on PreDist | Selection effect holds for 16/17 (PreDist) and 13/14 (CARE) detectors, and for the pooled panel in 5/5 seeds |
| Manuscript framed as a method paper (SRCR-C), which failed on the locked test | Reframed as an evaluation paper with 4 figures, 3 tables, 34 DOI-checked references, a reporting checklist and a limitations section |
| Results were not reproducible on a new machine | PreDist seed 0 reproduced byte-for-byte on a fresh container |

**What did not survive.** Under the calibrated tests, the claim that "out-of-sample thresholds restore the ranking, confirmed on two domains" is **not established**:
- CARE: T1 p = 0.065, T2 p = 0.18;
- PreDist leak-free: T2 p = 0.18.

The paper reports this openly as "consistent in direction (10/10 seed–dataset combinations), not statistically established".

## 3. Comparison with papers in the same journal

Source: `literature/journal_quality_bar.md`. That file covers 34 Energy and AI papers from 2024–2026, 6 of them read in full.

| Element | Typical Energy and AI paper | Best evaluation papers (100824, 100975) | This manuscript |
|---|---|---|---|
| Datasets | Median 1 | 6 DH datasets, 4 of them public (100824) | 2 public domains (DH + wind) |
| Baselines / detectors | Median 2–2.5 | 5 (100824) | 15–17 |
| Seeds | Reported in 3/15 | 3 fixed seeds (100975) | 5 seeds |
| Significance tests | 4/15 full texts; 0/16 most-cited | Friedman + Wilcoxon + CIs (100824); Diebold-Mariano (100975) | Cluster bootstrap + Holm + calibrated amendment |
| Pre-registration | Not observed | Not observed | Yes, with commit-dated plans |
| Leakage control stated | Rare | Yes (100975: information boundary) | Yes, leak quantified |
| Limitations section | 3/16 | Yes | Yes, specific |
| Negative results reported | Rare | Yes (100722, 100975) | Yes, the main ranking test fails A1 |
| Code / data | Mostly "on request" | Zenodo (100975) | Public data; code to be archived on Zenodo (authors to create the DOI) |

**Where it can beat those papers.**
- Statistical honesty: pre-registration, calibrated tests and failures reported.
- Breadth of the detector panel.
- Operator units: false alarms per asset-year, and the cost to a 100-substation fleet.

**Closest same-journal paper: 100824 (van Dreven 2026), which uses PreDist.** It evaluates on balanced daily windows at an oracle threshold. This paper measures that the same style of oracle threshold implies 83–176 false-alarm days per substation-year. That is a direct, constructive contribution which complements 100824.

**Style precedent: 100975 and 100856.** Energy and AI has published papers whose main message is that standard evaluation misleads model choice. This supports the topic fitting the journal.

## 4. Why it could be accepted, and why it could be rejected

**For acceptance:**
1. The topic fits the journal. Energy and AI publishes evaluation and audit papers, and no paper in its corpus compares benchmark protocols with deployment protocols for fault detection.
2. The burden numbers are concrete, operator-relevant and large:
   - 6.7–16.7 false alarms per turbine-year;
   - 83–176 alarm days per substation-year;
   - 7.6–20.6 times precision inflation.
3. The selection effect is a measured bias in how the benchmarks were built, and it is robust across seeds.
4. The rigour is above the journal's median on every element in the table above.

**For rejection (what reviewers will say):**
1. Novelty is incremental. The base-rate effect and threshold leakage are known; PreDist itself concedes the precision overestimate; Cools, Salem, Haneef, Liu and Song cover parts of the argument.
2. The ranking analysis, the most "scientific" part, is not significant under calibrated tests.
3. There is no foundation-model or transformer baseline.
4. The 2 false alarms per asset-year budget has no operator source.
5. The second PreDist manufacturer is excluded because an earlier locked test on it was evaluated more than once.

## 5. What would raise the acceptance odds (in order of value per effort)

1. **Group near-duplicate detectors into families and add an area-under-curve reference.** The reviewer suggests this. It is a few CPU hours, with a pre-registered amendment A2, and it may or may not rescue the ranking test.
2. **Add one modern baseline**, for example a small transformer or a pretrained time-series model, to the panel.
3. **Report recall over a sweep of false-alarm budgets (0.5–8 per asset-year)** instead of the single assumed budget.
4. **Create the Zenodo archive and add the authors' details, CRediT and the competing-interest statement.** Only the authors can do this.
5. **Consider a journal whose review time passes the 72-day rule.** Energy Informatics (Springer) has a verified median of 70 days, but its impact factor and quartile are UNVERIFIED. The current choice fails that rule.

## 6. Status of the compute

- PreDist leak-free robustness seeds 1–4 are running (`scripts/leak_seed_chain.sh`).
- When they finish, Fig. 4 and the robustness sentences can switch from legacy to leak-free.
- The paper's conclusions do not depend on them.
