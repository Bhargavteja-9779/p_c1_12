# Energy and AI (ISSN 2666-5468): quality bar for our early-fault-detection evaluation paper

Built 2026-11-24/25. Companion table: `energy_ai_papers_v2.csv` (39 papers). This file extends
`journal_selection/journal_benchmark.csv`, `journal_level_profile.md` and `style_notes.md` and does not repeat them.

## 0. Sample and sources (what was actually read)

- **Population.** OpenAlex source `S4210241048` (Energy and AI), publication date 2024-01-01 or later: 636 works, fetched on 2026-11-24.
- **Selection.** Each title and abstract was keyword-scored for topic proximity (fault, anomaly, condition monitoring, predictive maintenance, district heating, substation, wind/SCADA, HVAC/heat pump, false alarm, transfer, benchmark, reproducibility). I then hand-picked 39 papers:
  - 29 on fault detection, anomaly detection, CM or PdM in wind, district heating, HVAC/heat pumps, PV, batteries, fuel cells, engines and the grid;
  - 10 benchmark or evaluation papers (DH forecasting, transfer, audits, datasets).
- **Full texts read: 10, plus 1 partial.**
  - Typeset Elsevier versions from repositories: 100824 (Univ. Antwerp), 100366 (ETS Montreal), 100413 (HAL).
  - arXiv preprints: 100373, 100626, 100658, 100942, 100867, 100870.
  - Partial: 100819, from an earlier arXiv version with a different title.
- **Abstract only: 28.** Abstracts come from the OpenAlex `abstract_inverted_index`.
- **Blocked routes** (bot walls or forbidden): RWTH, UPC, NTNU/NVA, Kassel, PolyU, DiVA. ScienceDirect returns 403. The Elsevier text-mining API without a key returns metadata only.
- **Citations.** OpenAlex `cited_by_count` as of 2026-11-24.
- **How to read the CSV.** Every cell that comes from an abstract says so implicitly (`full_text_read = n`). Unknown values are `UNVERIFIED`.
- **Corpus-wide check.** I searched all 636 titles and abstracts:
  - "CARE" (the wind benchmark), "PreDist", "spectrum bias", "selection bias", "event-based" and "alarm budget" never appear.
  - "false-alarm" appears once, in a power-system security benchmark (10.1016/j.egyai.2026.100811), which is off-topic for us.
  - In the full texts I read, "false alarm" appears once, in passing (100366).

## (a) Top 5 papers and what makes them strong

Selection rule: topical relevance weighted by citations, with full text required so that the claims can be checked. The five most-cited papers in the set by raw count are 100413 (57), 100345 (54), 100366 (46), 100412 (43) and 100373 (32). Of these, only 100373 is close to our topic. The others are battery, fuel-cell and blade-imaging papers, and their strength is mostly a typeset package plus a single dataset (see the note after the table).

| # | DOI | Cites | Why it is in the top 5 |
|---|---|---|---|
| 1 | 10.1016/j.egyai.2026.100824 (van Dreven et al., DH substation self-supervised transformer) | 2 | **Our closest competitor.** It uses PreDist split per manufacturer (M1/M2), with M1<->M2 zero-shot transfer. |
| 2 | 10.1016/j.egyai.2024.100373 (Roelofs et al., AE transfer learning, wind) | 32 | The most-cited wind CM paper. It is a cross-turbine transfer study. |
| 3 | 10.1016/j.egyai.2025.100626 (Jonas & Meyer, CycleGAN transfer, wind) | 14 | A cross-turbine NBM transfer study across 7 wind farms. |
| 4 | 10.1016/j.egyai.2025.100658 (Mukhtar et al., reproducibility of HVAC FDD) | 17 | An evaluation-methodology paper in FDD with no method contribution. |
| 5 | 10.1016/j.egyai.2026.100942 (Spoek et al., TSFM heat-load evaluation) | 4 | A pure systematic-evaluation paper in DH with the strongest statistics in the set. |

### What they contain, concretely

**1. 100824: 17 typeset pages, 7 figures, 8 tables.**
- **Front matter.** Graphical abstract, plus 5 highlights.
- **Structure.** Introduction (with research question and a 4-bullet contribution list), Related work, Data sources, Methods, Experimental setup (Experiments EXP1-3 and Baselines), Results (with **6.4 "DH field implications"** and **6.5 "Limitations"**, 4 bullets), Conclusion and future work.
- **Data.** 6 datasets: lab, simulation and 4 field datasets (CSDH 250 substations, PreDist M1/M2 with 93 substations, BDH 36 centres). Two are private.
- **Baselines.** 5 strong time-series classifiers (InceptionTime, MiniRocket, MLSTM-FCN, TST, TSSequencerPlus), with a parameter-count table.
- **Statistics.** Repeated stratified CV with seeds, 95% CIs, Friedman test followed by paired Wilcoxon tests, and Cohen's d.
- **Ablation.** A component ablation (Table 7).
- **Other analyses.** A standard split vs a substation-out split (Table 8), and UMAP embedding plots.
- **Candour.** It reports where its own method loses to baselines.
- **Weaknesses we can exploit.**
  - The protocol is window-level classification with fault ratios of 20-83%.
  - F1 is "upper-bound macro F1", i.e. computed with an oracle threshold.
  - There is no time-based false-alarm rate and no continuous monitoring.
  - It acknowledges that "the absence of a report does not guarantee fault-free operation" but does not quantify the effect.
  - No code link.

**2. 100373: arXiv version, 7 figures, 0 tables.**
- A nomenclature list.
- Two offshore wind farms (240 and 30 sensors) and 3 failure case studies.
- Thresholds tuned on the F0.5 score ("to prioritise precision over recall"), plus a criticality measure over time.
- Short and focused, with a single baseline.
- **Its strength is the question** (does transfer work across turbines?) and the use of real failures, not the rigour: there are no statistics and no code.

**3. 100626: arXiv version, 10 figures, 2 tables.**
- **Contributions.** Explicit roman-numeral contribution list with a "first to" claim.
- **Data.** 7 turbines from 7 wind farms, giving 28 domain pairs.
- **Scarcity sweep.** Data-scarcity levels from 1 to 8 weeks.
- **Outputs.** Qualitative anomaly-score timelines against logged incidents. Code is public.
- **Caveat.** The F1 measures agreement with an abundant-data NBM, not with fault labels. The authors note that they "cannot determine" whether some high scores are "false positives or identified but unlogged abnormal states."

**4. 100658: arXiv version, 13 figures, 2 tables.**
- A coded corpus of 65 FDD studies.
- A strong headline number in the abstract (72% of studies do not state data availability).
- A policy-style closing that calls for guidelines.
- Code and data released.
- **Why it matters for us.** It proves that the journal publishes **pure evaluation and meta-science in FDD**.

**5. 100942: arXiv version, 8 figures, 9 tables.**
- 13 trained baselines.
- 95% block-bootstrap CIs and critical-difference diagrams.
- Ablations and sensitivity analyses (covariates, context length, resolution, weather-forecast realism).
- Cross-network transfer, with one public external network.
- A Limitations subsection.
- Code plus Zenodo.

### Recurring strength markers across the top 5 and the typeset papers

- **Graphical abstract and highlights.** All 3 typeset PDFs I read have both (100824, 100366, 100413).
- **A framework or pipeline figure.** Fig. 1 in 100824 is a two-stage pipeline overview.
- **Data in a table.** A table summarising datasets (type, availability, resolution, number of samples, fault ratio) and a table of methods (family, parameters).
- **Two kinds of results.** Quantitative tables with mean ± CI, plus qualitative timelines before documented failures (100373, 100626).
- **A practical section.** An explicit deployment or field-implications section (100824 §6.4), or latency figures (100525 reports 14/12/24 ms inference; 100366 reports processing time).

**Note on the high-citation, off-topic papers** (100413, 100366): both are short, typeset at 10-13 pages, use one dataset, have no statistical tests and make data available only "on request". Their citations reflect the topic (batteries, blade imaging), not rigour. They are not the bar for rigour.

## (b) Typical structure, length, abstract, highlights, contributions and tone

- **Sections.** Introduction (with a contribution list and a roadmap paragraph), Related work, Data, Method or Protocol, Experimental setup (including baselines and metrics), Results, Discussion or field implications, Limitations, Conclusion and future work. Back matter: CRediT, competing interests, data availability (with code availability as a separate heading in 100413), and a generative-AI declaration (2025-26).
  - Benchmark papers sometimes separate Results and Discussion (100867 states an "IMRaD + CRISP-DM" structure).
- **Length.**
  - Typeset pages: 10 (100366), 13 (100413), 17 (100824). The earlier profile gives 11-19, median 16.5.
  - Figures: median 10 main-text figures.
  - Tables: 3-9 main tables (benchmarks have more, e.g. 100870 has 11 and 100942 has 9).
  - References: 45-90. Benchmark and evaluation papers sit at the top: 100867 has 86 references, 100658 has 88, 100788 has 82 and 100971 has 92.
- **Abstract.** One paragraph of about 220-300 words. Order: context, gap, "This study/paper ...", setting, several hard numbers, then a practical implication.
  - Evaluation papers end on a normative sentence. Examples from abstracts: "Lab-aware evaluation should therefore be a standard component of ML reporting, not an optional addition." (100856); "Benchmark objectives should disclose their implied violation price alongside any reported energy saving." (100936).
- **Highlights.** 4-5 bullets of about 10-15 words, mixing method and finding statements. Verbatim from 100824: "Evaluated in-depth, from lab and synthetic data, to multiple real-world DH networks."; "Cross-domain transfer is feasible, but currently asymmetric."
  - 100366's highlights are hype-heavy ("Revolutionizing wind energy maintenance ..."). Avoid this style.
- **How contributions are listed.** 3-4 bullets, or roman or arabic numerals, introduced by "The main contributions of this paper are:" or "Our contributions are as follows:". Verbatim examples:
  1. "We provide a broad empirical reference for DH substation fault detection using six datasets spanning controlled laboratory emulations, synthetic benchmarks, and field deployments." (100824)
  2. "Our study is the first to investigate and demonstrate domain mapping for unsupervised anomaly detection with time series for WT fault detection." (100626)
  3. "We provide a systematic evaluation of two TSFMs, TabPFN-TS and Chronos-2, for probabilistic heat load forecasting in DHNs." (100942)
  4. "A benchmark of recent TSFMs in univariate, covariate-informed, and fine-tuned modes against task-specifically tuned XGBoost and random forest." (100867)
  5. "An empirical benchmark of nine forecasting architectures, including linear, MLP-based, convolutional, and Transformer-based models, alongside classical baselines (SARIMA, naïve seasonal) on two real-world smart meter datasets." (100870)
- **Tone.**
  - Assertive in abstracts and highlights.
  - Hedged, effect-size-aware wording in the best bodies. 100824 writes "we refrain from making strong pairwise claims for this dataset and interpret differences primarily through effect sizes and CI".
  - Limitations are given as bullets or a short subsection.

## (c) How evaluation and benchmark (non-method) papers frame their contribution here

They exist and are increasing in 2026. Ten of the 39 are coded as benchmark-evaluation or meta-research. Their framing follows a repeatable template:

1. **Name an evaluation gap, not a model gap.** Examples:
   - "a systematic, use-case-differentiated evaluation is still missing" (100867 abstract);
   - "lacking application-specific benchmarks with documented ground truth" (100788);
   - within-lab R² "can diverge sharply from cross-laboratory predictive performance" (100856);
   - benchmark weights "imply a price ... rarely stated or checked" (100936).
2. **Provide a protocol or framework as the contribution.** Examples:
   - a "standardized evaluation protocol ... isolates detection accuracy from downstream model adaptation" (100788);
   - a "diagnostic framework" plus a pass threshold, LOLO R² > 0 (100856);
   - a taxonomy plus a dataset collection (100867).
3. **Quantify how far the standard practice misleads.** 100856 shows within-lab R² of 0.44 collapsing to LOLO R² of -3.05. 100936 shows that none of 102 policies held the thermal band.
4. **Close with a reporting recommendation** addressed to the community.
5. **Back the evidence with statistics, robustness and released code.** 100942, 100870 and 100867 all use Friedman/Wilcoxon or bootstrap and release code.

**Implication.** Our paper should be framed as "deployment-faithful evaluation exposes a protocol gap", with a protocol, a quantified gap and a normative reporting rule. The 100856/100936/100788 audit-style framing is the in-journal precedent. A "new detector" framing is not.

## (d) Checklist: at or above the best of these papers

Data and protocol
1. Two asset classes (DH substations on PreDist; wind on CARE to Compare). Report the number of assets, events and normal periods per dataset in one **dataset summary table** (type, availability, resolution, number of assets, number of events, normal-period share), as in 100824 Table 2.
2. Explicitly **position against 100824**, which uses the same PreDist M1/M2 data. Reproduce its window-level, balanced, oracle-threshold protocol as one arm. Then show what changes under continuous, false-alarm-budgeted monitoring.
3. Use a **time-based false-alarm metric** (alarms per asset-year or per 1000 h) at fixed budgets, plus detection rate and lead time. No paper in the set reports this.
4. Run **balanced-event vs continuous evaluation on the same data and the same models**, with rank-reversal analysis.
5. **Cross-manufacturer and cross-farm transfer** under the deployment protocol (train on M1, test on M2, and vice versa; across CARE farms). Report asymmetry, which 100824 found but only at window level.
6. A **selection (spectrum-bias) analysis**: quantify how curated normal periods inflate specificity, with a controlled manipulation and a dose-response plot. 100824 only names the label-noise issue.

Baselines and statistics
7. **At least 5 baselines**, including a trivial or rule baseline and a chance or permutation reference, plus classical NBM/AE and at least one strong modern model. Top papers use 5-14 baselines.
8. **Repeated seeds** (say how many), **95% bootstrap CIs** (block bootstrap over assets or events), Friedman + Wilcoxon/Holm or critical-difference diagrams, and **effect sizes**.
9. **Sensitivity and ablation of the protocol itself**: budget level, event-window definition, threshold-calibration period, and normal-period curation rule.
10. **Hedge wherever tests are not significant**, in the style of 100824's effect-size wording.

Presentation (Energy and AI conventions)
11. Graphical abstract, built around a protocol-gap figure (benchmark score vs deployment score).
12. 4-5 highlights of 10-15 words, each carrying a number. No hype words.
13. One-paragraph abstract of 220-280 words containing 3-4 hard numbers and a closing normative sentence.
14. Introduction ending in a research question, a 3-4 item contribution list that starts with verbs, and a roadmap.
15. **Framework or pipeline figure** (Fig. 1) showing the two protocols side by side.
16. **Qualitative timeline figures**: anomaly score vs threshold before documented faults, with false alarms marked (as in 100373/100626, but quantified).
17. An explicit **"Practical implications for operators"** section covering the alarm-budget trade-off, inspection cost and calibration data needed (compare 100824 §6.4). Also report compute cost and latency.
18. A **Limitations** subsection in bullet form, plus future work.
19. About 15-17 typeset pages, 8-12 figures, 4-9 tables and 60-90 references. Evaluation papers here run at about 80-90 references.
20. Code on GitHub **with a Zenodo DOI**, exact dataset versions and split files, and a data-availability statement. Both datasets are public, so the full study can be reproduced. This beats 100824, which has private data and no code link.
21. A **reporting-checklist table** for future FDD studies, which turns the 100658 critique into a positive tool.
22. Cite in-journal precedents in the introduction and related work: 100824, 100548, 100373, 100626, 100658, 100788, 100856, 100942.
23. Show **conservative nomenclature** (an acronym list) and define every metric by equation.

## (e) Gaps: what none of the 39 papers does that our study does

1. **Continuous monitoring with a false-alarm budget.** No paper evaluates fault detectors under a fixed alarm budget per asset-time. Evaluation is window or sample classification (100824, 100766, 100892), accuracy or F1 on lab rigs (100565, 100681, 100845), or agreement with a reference model (100626). Among all 636 abstracts, "false alarm" appears only in an off-topic grid-security paper.
2. **Protocol comparison as the result.** No paper puts balanced-event and deployment protocols side by side on the same data and models to measure how much the benchmark overstates field performance. 100856 does the analogous thing for perovskite materials ML, and 100936 for DRL cooling. **Nobody has done it for fault detection or condition monitoring.**
3. **Selection (spectrum) bias in curated normal periods.** 100824 and 100626 acknowledge unlogged faults and label noise qualitatively. None measures the effect of how normal periods are chosen.
4. **Two public, heterogeneous energy-asset benchmarks in one study.** No paper uses CARE to Compare. PreDist appears only in 100824, and only at window level. No paper crosses DH substations and wind turbines.
5. **Cross-manufacturer transfer under deployment metrics.** Transfer appears in 100373, 100626 and 100824, but always with classification or proxy metrics, never alarm rate or lead time at fixed budgets.

**Main in-journal threat.** 100824 already "provides a broad empirical reference" on PreDist M1/M2, including cross-manufacturer transfer. Our novelty claim has to rest on the **protocol** (continuous, budgeted, selection-aware), not on the datasets or on transfer alone.
