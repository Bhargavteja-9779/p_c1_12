# Energy and AI: the quality bar we have to meet or beat

Built 2026-11-24. Companion data: `literature/journal_quality_papers.csv` (34 papers). This file builds on `journal_selection/journal_benchmark.csv` (40 papers, 16 read in full), `journal_level_profile.md` and `style_notes.md`, and does not repeat them. Every number below comes from a source I opened (OpenAlex, Crossref, Semantic Scholar, or a PDF I read). Anything I could not check is marked UNVERIFIED.

## 0. Sample, sources and caveats

### How the papers were chosen

- **Group A, the most-cited papers (16).**
  - **Window.** Crossref `filter=issn:2666-5468,from-pub-date:2024-06-01,type:journal-article` returns 601 items. I ranked them by OpenAlex `cited_by_count`, retrieved on 2026-11-24.
  - **Exclusions.** I left out reviews, overviews, perspectives and surveys: 100419, 100424, 100375, 100378, 100406, 100361, 100455, 100514, 100518 and 100508.
  - **What is left.** The top 15 research articles, plus 100414 (number 16) because it had a repository PDF. In the end, that PDF returned HTTP 503.
  - **Example of the citation sources disagreeing.** Six highly cited 2024 papers (100347, 100368, 100372, 100360, 100371, 100345) have a Crossref issue date of 2024-05, so they fall outside the window and are not included.
- **Group B, the papers closest to our topic (18).** These come from a keyword screen of all 600 OpenAlex 2024+ articles in the journal. The keywords were fault, anomaly, condition monitoring, wind turbine, district heating, substation, benchmark, HVAC, reliability and diagnosis. I kept the papers about fault or anomaly detection, wind, district heating, and evaluation or benchmarking methodology. 7 of the 18 are also in `journal_benchmark.csv`.
- **DOI checks.** All 34 DOIs resolve on Crossref, and Crossref lists the container as *Energy and AI*.

### Citation counts

The CSV gives three counts for each paper: OpenAlex, Crossref `is-referenced-by-count` and Semantic Scholar, all retrieved on 2026-11-24. They differ a lot. For example, 100444 has 139 in OpenAlex, 119 in Crossref and 113 in Semantic Scholar.

### Full text

I could read **6 of the 34** in full.

- **Published Elsevier PDFs in institutional repositories (3):**
  - 100824 (Univ. Antwerp);
  - 100397 (Coventry);
  - 100366 (ETS Montreal).
- **arXiv author versions (3):**
  - 100571;
  - 100975 (v1);
  - 100450 (posted 2022 and revised later).
- **Why the rest are abstract-only (28):**
  - ScienceDirect PDF links return 403.
  - The HAL copies (100380, 100413) return a bot-check page.
  - DiVA (100548) timed out, and UPM (100414) returned 503.
  - There are no arXiv or Zenodo copies.

Every row for those 28 papers is coded from the OpenAlex abstract only. Their structure, figure and table counts, and statistics columns are "UNVERIFIED (abstract only)".

Together with the 16 full texts in `journal_benchmark.csv`, **22 distinct Energy and AI papers have now been read in full**. 100824 was abstract-only before and is now full text.

### Caveats

- **Preprints vs published versions.** Counts taken from preprints (100571, 100975, 100450) may differ from the published versions. Their page counts are preprint pages and are not used as journal length.
- **Citations do not measure rigour.** The most-cited papers are mostly forecasting or materials papers with thin evaluation (see Section 2). "Best" in this file therefore means two things: highest-cited (Group A) and most rigorous on our topic (the Group B exemplars 100824, 100975, 100788, 100722 and 100856, plus 100942, 100867, 100870 and 100704 from the earlier benchmark).

## 1. What a top Energy and AI paper contains

| Element | Evidence (n = papers where it could be checked) | Source |
|---|---|---|
| **Highlights** | 3/3 new typeset PDFs (100397, 100366 and 100824 have 5 bullets each). 7/16 benchmark full texts (all 4 typeset ones). Never seen in an author preprint, so it is added at production or required at submission. | PDFs |
| **Graphical abstract** | 3/3 new typeset PDFs, 6/16 benchmark. Always a pipeline or overview figure. | PDFs |
| **Keywords** | 6/6 new full texts; 16/16 benchmark. | PDFs |
| **Nomenclature / acronym box** | 2/6 new (100397 has symbols + abbreviations, 100975 has an acronym box); 2/16 benchmark (100373, 100448). | PDFs |
| **Explicit contribution list** | 3/6 new use bullets: 100824 ("The main contributions of this paper are:", 4 bullets starting with "We introduce / We provide / We derive"), 100571 (subsection "1.1. Contributions", 4 bullets with bold lead-ins) and 100450 (bold lead-ins). 100975 states its 3 contributions in one closing paragraph. 100397 and 100366 have no list. Benchmark: at least 11/16 have a list. | PDFs |
| **Roadmap paragraph** ("Section 2 reviews ...") | 100824, 100571 and 100975 have one. | PDFs |
| **Separate Related-work section** | 3/6 new (100824, 100571, 100975); 11/16 benchmark. | PDFs |
| **Dedicated Limitations subsection** | 3/6 new: 100824 §6.5, 100975 §6.5, and 100571 §5.4 "Key Findings and Limitations". 3/16 benchmark. Evaluation-type papers tend to have one; method papers usually do not. | PDFs |
| **"Implications for practice" subsection** | 100975 §6.4, and 100824 §6.4 "DH field implications". | PDFs |
| **Back matter** | CRediT 4/4 of the new typeset or near-final texts that I checked (100397, 100366, 100824, 100975). Data availability 4/6. Generative-AI declaration 3/6 (100571, 100450, 100975). 100975 names "Open AI Codex and Anthropic Claude" for code assistance. | PDFs |
| **Typeset length** | New: 10 (100366), 14 (100397), 17 (100824). Pooled with the benchmark's 11, 16, 17 and 19 pages: **median 16 pages, range 10-19 (n = 7)**. | PDFs |
| **Main-text figures** | New full texts: 8, 9, 15, 7, 10 and 11, **median 9.5**. Benchmark median 10 (n = 16). | PDFs |
| **Main-text tables** | New: 6, 11, 11, 8, 7 and 4, **median 7.5**. Benchmark median 3.5. Appendix tables are common in addition, e.g. 100975 has A.8-A.12. | PDFs |
| **References (Crossref)** | All 34: **median 48.5** (IQR 38.75-66.25, range 22-89). Group A median 45, Group B median 53. The evaluation exemplars have 72 (100824), 69 (100975) and 89 (100788). | Crossref |
| **Title** | Median 14 words in A and 14.5 in B. A colon appears in 4/16 Group A titles and 10/18 Group B titles. In Group B the "Topic: specific claim" form is common (100856, 100963, 100788, 100824). | OpenAlex |
| **Abstract** | Single paragraph. Median 208 words (A) and 215 words (B), range 149-276. Numbers in the abstract: 13/16 A and 8/18 B contain a percentage. A "this paper/we propose / introduce / develop" sentence appears in 9/16 A and 15/18 B. | OpenAlex |
| **Review time (one data point)** | 100824 prints "Received 6 May 2026; revised 14 June 2026; accepted 23 June 2026", which is 48 days from receipt to acceptance. Elsevier dates are not in Crossref, so other papers are UNVERIFIED. | PDF |

## 2. How much evidence papers provide

### Typical paper vs the best papers

| Dimension | Typical (journal medians from the earlier benchmark, n stated there) | Most-cited Group A (abstract evidence, n = 16) | Best-in-class on rigour (full text read) |
|---|---|---|---|
| **Datasets / sites** | Median 1 (full texts: 2) | Mostly 1-2. 100444 (most cited, 139) reports one PV setting; 100413 one public battery set | **6** DH datasets, 4 public and 2 private (100824). **18** heating datasets (100722, abstract). **54** (100867) |
| **Baselines** | Median 2-2.5 | 0-6. 100380 has 3, 100434 has 2, 100474 has 1 | **5** strong TS classifiers from one library (100824). 13-14 (100942, 100704). **8** detectors (100788, abstract) |
| **Seeds / repeats** | Reported in 3/15 full texts | Not stated in any abstract | 100975 fixes 3 seeds (42, 7, 101). 100824 reports mean ± 95% CI over repeated seeds and repeated stratified CV, but the number of repeats is UNVERIFIED |
| **Significance tests** | 4/15 full texts (27%) | **0/16** abstracts mention a statistical test | 100824: Friedman (α = 0.05) + paired Wilcoxon + Cohen's d + 95% CIs. 100975: Diebold-Mariano with HAC lag. 100942: CD diagrams + block-bootstrap CIs. 100870: Friedman + Holm-Wilcoxon |
| **Ablation** | 3/16 full texts | 0/16 abstracts mention one | 100824 component ablation (Table 7). 100975 grouped-information ablation |
| **Leakage-safe / out-of-sample protocol stated** | Not coded before | Not visible in abstracts | 100975: "common pre-auction information boundary and rolling-origin design" over a full held-out calendar year, with validation in the prior half-year. 100824 standardises using training-split statistics only |
| **Public code** | 9/15 full texts (arXiv-biased) | **0/16** abstracts mention code. The only public artefact is a web tool (100414) | 100975: Zenodo DOI. 100571: GitHub. 100819: GitHub with data and models (abstract). 100824: no code statement; data partly public |
| **Data availability** | Slot present in 9/16 | n/a | "Data will be made available on request" appears in 100397 and 100366 (both top-cited). 100824 gives a split public/private statement |

### What this means for us

- **Citations do not reward rigour in this journal.** The most-cited wind fault-detection paper in the window is 100366 (46 citations). It uses one lab dataset, 2 baselines, a single 80% training split, no statistics, and data only on request, and its highlights claim "100 % accuracy". The evaluation-heavy papers (100824, 100975, 100788) are too new to have citations yet.
- **What exceeding the best papers means.** The rigour bar to exceed is set by 100824 and 100975, which have:
  - several datasets, some of them public;
  - at least 5 strong baselines;
  - paired non-parametric tests with effect sizes and CIs;
  - fixed seeds;
  - an ablation;
  - a leakage-safe protocol;
  - archived code;
  - a dedicated limitations subsection.

## 3. Writing style

All quotes are 25 words or fewer and come from text I read. The DOI suffix is given; the prefix is 10.1016/j.egyai.

### Patterns to follow

- **Evaluation papers lead with the gap between the reported metric and the decision that matters.**
  - 100975 (full text) frames its whole contribution as "evidence that aggregate rankings are uninformative about price-spike reliability".
  - In its practice section it says "model selection on CRPS or marginal coverage is insufficient and can be actively misleading."
  - This is the same logical shape as our claim: balanced event-window scores mislead deployed alarm precision and rankings.
- **Failure-of-standard-evaluation papers make a prescriptive closing statement.**
  - 100856 (abstract): "Lab-aware evaluation should therefore be a standard component of ML reporting, not an optional addition."
  - It also gives a concrete pass/fail criterion ("requires LOLO R² > 0").
- **Scope is stated honestly, and competitive baselines are credited.**
  - 100824 (abstract) concedes that "CNN-based and hybrid baselines remain highly competitive in cleaner or more separable regimes".
  - Its introduction justifies breadth "to move beyond maximising accuracy on a single curated dataset".
- **Label-quality limitations are stated specifically.**
  - 100824 §6.5: "the absence of a report does not guarantee fault-free operation".
  - This applies directly to PreDist and CARE labels, and we should say the same.
- **Mechanism statements, not just scores.**
  - 100975: "Recalibration and combination therefore address different failures and are not substitutes."
  - Each finding comes with a structural reason.
- **Null and negative results are reported openly.**
  - 100722 (abstract) reports that static features yield "only minor, often statistically non-significant, and sometimes slightly negative effects".
  - 100975 reports a "non-significant 4.4% difference" in CRPS.
- **Benchmark protocols are described by what they isolate.**
  - 100788 (abstract) says its protocol "isolates detection accuracy from downstream model adaptation effectiveness".
  - It reports a sobering headline number ("Maximum MCC of 0.32").
- **Contribution lists.** Typically 3-4 bullets, each starting with a verb ("We introduce...", "We provide...", "We derive...", from 100824), or with a bold noun phrase (100571, 100450).

### Patterns to avoid

These appear in highly cited papers, but they conflict with our integrity rules and would weaken an evaluation paper:

- Hype in highlights. 100366: "Revolutionizing wind energy maintenance ..." and "Flawless fault Detection, achieving 100 % accuracy ...".
- Unsupported superlatives in abstracts:
  - 100450: "remarkable accuracy (96% classification, 2.3% MAPE)";
  - 100645: "This work presents a milestone ...";
  - 100459: "achieves state-of-the-art performance".
- "Novel", "first" and "state-of-the-art" in abstracts: 3, 7 and 4 of the 34 respectively (OpenAlex abstracts). We use them only if Section 6 literature evidence supports them (MASTER_PROMPT rule 7).

## 4. Checklist: what our manuscript must have to be at or above the best papers

Each item gives the bar it beats or matches.

1. **A headline finding stated as a measured ranking inversion and precision gap, in the abstract and the highlights.** Give numbers from result files, for example deployed alarm precision vs balanced-window precision, and how many detector-pair rankings flip. Bar: 100975's "aggregate rankings are uninformative" framing, which has no ranking-flip count.
2. **A protocol section that defines the "information boundary" of deployment.** It should cover:
   - continuous replay;
   - thresholds fixed out-of-sample, on a validation period, before test;
   - false-alarm budget per asset per unit time;
   - no event-window balancing;
   - a side-by-side table: balanced-benchmark protocol vs deployment protocol.

   Bar: 100975 §3-4 (information boundary, rolling origin). 100824 evaluates PreDist only as balanced-ish daily-window classification at 20-32% fault prevalence.
3. **At least 2 domains with public data and DOIs: PreDist (DH substations) and CARE to Compare (wind).** Bar: median 1 dataset; 100824 uses 6 datasets but only 4 are public. We should list exact subsets, assets, events and prevalence in one dataset table, as in 100824 Table 2.
4. **A detector panel of at least 5.** It should include a simple rule or threshold baseline, classical unsupervised detectors and at least one modern deep model, with equal tuning budgets logged. Bar: 5 in 100824; 3 in 100828.
5. **Paired statistics across assets and events.** Use a Friedman test with Holm-corrected Wilcoxon, or a CD diagram; effect sizes; block or event-level bootstrap 95% CIs on precision, alarms per asset-year and detection delay; seeds fixed before test and reported. Bar: 100824 (Friedman + Wilcoxon + d + CI) and 100975 (DM + 3 fixed seeds). We exceed it only if the CIs cover the deployment metrics themselves, not just AUC or F1.
6. **A sensitivity analysis that turns each protocol choice on and off.** The choices are balancing, threshold leakage and window length. This is the evaluation-paper version of an ablation, and it shows which choice drives the overstatement. Bar: 100824 Table 7 and the 100975 grouped ablation; both are 19% or less of the journal.
7. **An operator-unit translation in an "Implications for practice" subsection.** For example: alarms per 100 substations per month at a fixed recall, and what a false-alarm budget implies. Bar: 100975 §6.4 converts errors to GBP/MWh.
8. **A dedicated Limitations / threats-to-validity subsection.** It should be specific, covering:
   - label noise (unreported faults, as worded in 100824);
   - limited event counts and wide CIs;
   - only 2 domains;
   - detector-panel coverage.

   Bar: 3/16 benchmark full texts + 100824 + 100975. A threats-to-validity format would be above everything observed so far.
9. **Code and data archived with a Zenodo DOI, plus a Data availability statement, a CRediT section to be completed by the authors, and a GenAI declaration.** Bar: 100975 (Zenodo). The top-cited papers mostly offer data "on request".
10. **A reporting recommendation or minimum-reporting checklist for FDD benchmarks.** It should be prescriptive, as in 100856, and cover what any FDD paper should report: prevalence, threshold source, alarms per asset-time, event-level CIs.
11. **The submission package.** Aim for:
    - highlights: 3-5 bullets, quantified, with no hype words;
    - a graphical abstract: a pipeline figure contrasting the two protocols;
    - 4-8 keywords;
    - an acronym nomenclature box (NBM, SCADA, DH, FDD, FAR...).

    Target size: about 9-10 main figures, 5-8 main tables, 50-70 references, about 16 typeset pages.
12. **Mixed and negative results shown openly.** Examples: detectors whose ranking does not change, and cases where balanced and deployed metrics agree. Bar: 100722 and 100975 do this; most papers do not.
13. **A direct engagement with prior DH/PreDist results.** Explain why the window metrics in 100824 and HEAT (100548), which reports sensitivity and specificity, are not deployed alarm precision. Frame this as a measurement point, not an attack. Re-evaluate under our protocol only those methods we can actually reimplement; anything else is labelled as an argument, not a result.
14. **A title that names the claim and the setting, in "Topic: claim" form, 13-15 words, with no "novel".** This matches the journal's median title length of 13-14 words, and the colon form is used in 10/18 topic-close papers.

## 5. Papers to cite or compare against, and why

### Must cite and position against

| Paper | Why |
|---|---|
| **10.1016/j.egyai.2026.100824** (van Dreven et al. 2026, self-supervised transformer for low-label DH fault detection; full text) | Closest paper: same journal, same domain, and it uses PreDist (M1/M2) with window-level ROC-AUC and upper-bound macro F1. It is the natural "balanced benchmark" reference point. Cite its label-noise limitation as well. |
| **10.1016/j.egyai.2025.100548** (HEAT, DH substation clustering; abstract) | Same group. It reports sensitivity and specificity and claims to minimise false positives. We can contrast this with alarm precision under a budget. |
| **10.1016/j.egyai.2026.100788** (concept-drift detection benchmark in DH; abstract) | Closest benchmarking-methodology precedent in DH: a detector-centric protocol with robustness checks. We should frame our work as the analogous protocol for fault detectors. |
| **10.1016/j.egyai.2026.100975** (tail reliability, GB day-ahead prices; full text, arXiv v1) | Same type of claim in the same journal: aggregate scores mislead model selection. It is a style and structure template. |
| **10.1016/j.egyai.2026.100856** (cross-laboratory generalisation failure; abstract) | An Energy and AI precedent for "standard evaluation overstates real performance, and here is a diagnostic protocol". It supports the publishability of evaluation-failure papers in this journal. |
| **10.1016/j.egyai.2024.100373** and **10.1016/j.egyai.2025.100626** (wind autoencoder NBM transfer; generative transfer for new turbines; in journal_benchmark.csv, full text) | Wind normal-behaviour-model detectors in this journal. These are thresholded detectors whose evaluation our protocol applies to. |
| **10.1016/j.egyai.2025.100658** (reproducibility of ML-based HVAC FDD; benchmark full text) | Meta-research precedent on FDD reporting quality. It supports our reporting checklist. |

### Cite as context or contrast

- **10.1016/j.egyai.2026.100828** (LLM agent for wind condition monitoring). One documented failure, 24 queries, and baselines that include a fixed threshold and an isolation forest. It shows how thin event counts are in wind condition monitoring.
- **10.1016/j.egyai.2024.100366** (hyperspectral blade inspection, most-cited wind fault-detection paper). Lab data, single split, "100 % accuracy". Use it as context for why deployment-realistic evaluation is needed. Cite it neutrally.
- **10.1016/j.egyai.2026.100845** (heat-pump evaporator fault detection) and **10.1016/j.egyai.2026.100862** (speed-invariant gearbox autoencoder). These are residual- or threshold-based detectors where threshold choice is central, and 100862 claims "threshold-consistent health indicators".
- **10.1016/j.egyai.2026.100722** (heating-load transfer-learning benchmark over 18 datasets). A model for reporting non-significant effects at scale.
- **10.1016/j.egyai.2026.100942**, **10.1016/j.egyai.2026.100867** and **10.1016/j.egyai.2026.100870** (from journal_benchmark.csv). Statistical-reporting exemplars in the journal: CD diagrams, block bootstrap, Friedman/Nemenyi, Holm-Wilcoxon.

### Not needed

The Group A top-cited forecasting, materials and fuel-cell papers (100444, 100480, 100420, 100474, 100380, 100496, 100489, 100459, 100559, 100434, 100414) are off-topic. They are useful here only as style and length evidence.

### Before citing

Before any of these go into `paper/` references, re-open each one and check it under BRIEF integrity rules. Seven of the sources in this section (100548, 100788, 100856, 100828, 100845, 100862, 100722) are abstract-only, so any claim about their methods beyond the abstract must be marked UNVERIFIED.
