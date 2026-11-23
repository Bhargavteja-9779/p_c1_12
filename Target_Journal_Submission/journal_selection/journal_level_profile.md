# Energy and AI (ISSN 2666-5468): journal-level profile, 2024-2026 research articles

Built on 2026-11-23 from `journal_benchmark.csv` (40 research articles). Every number below comes only from values marked as verified in that file. `UNVERIFIED` and `NA` cells are left out, and each statistic says how many papers it rests on (n).

## Sample and sources

- **Population.** OpenAlex returns 628 works of type `article` in Energy and AI with a publication date of 2024-01-01 or later. I used `page=` paging and no cursor.
- **Selection.** I picked 40 articles that are not reviews, perspectives or editorials. Topic priority went first to fault detection, anomaly detection, condition monitoring and predictive maintenance (wind, PV, HVAC/VRF, heat pumps, district-heating substations, batteries, engines, grid). Next came district heating and building energy forecasting or control. The rest are other applied ML-for-energy papers that have an arXiv full text.
  - I dropped one candidate (10.1016/j.egyai.2024.100419) because its abstract calls itself a perspective.
- **Full text (16 papers, `source_used = arxiv_fulltext`).** I read the arXiv PDFs with pypdf. Twelve are author preprints and four are the published Elsevier-typeset version posted to arXiv (100538, 100586, 100726, 100884).
- **Abstracts only (24 papers).** These use the OpenAlex `abstract_inverted_index`.
- **Reference counts.** These are Crossref `reference-count` values for all 40 papers.
- **Not used.** ScienceDirect and Elsevier pages were not accessed.

### Caveats

- **Finding the arXiv versions.** arXiv API title search gave almost nothing (3 hits in 96 queries). The arXiv versions were found mainly through the arXiv locations that OpenAlex lists for each work.
- **The full-text subset is biased.** It covers only authors who post to arXiv. Those authors are likely to be ML-oriented and to share code more often than the journal as a whole.
- **Counts from preprints may differ from the final papers.** Figure and table counts come from the arXiv version, using the highest main-text Figure/Table number; appendix items such as A1 or S1 are excluded. Example: the 100373 preprint cites 13 references, but Crossref lists 31 for the published paper.
- **Page counts.** Journal page length is known only for the 4 Elsevier-typeset PDFs. Preprint page counts (17 to 65 pages) do not reflect journal length and are not used.

### Coding rules

- **n_baselines.** The number of comparison methods other than the method or methods of interest. In benchmark papers it counts only the methods the paper labels as baselines.
  - Example: 100870 benchmarks 9 deep models against 2 classical baselines, so it is coded 2.
- **ablation = yes.** The paper reports experiments that remove or swap components or feature groups of its own approach.
- **real_world_or_deployment_evidence = yes.** The method is evaluated on real field or operational data, or deployed or tested on real equipment such as a real house or HIL with a commercial unit. Lab cell cycling, emulators and simulations count as no.
- **Abstract-only rows.** "yes" means the abstract says so. "no" was entered only when the abstract makes the setting clear, for example a lab rig or simulation only. Otherwise the cell is `UNVERIFIED`.

## Experimental-rigour statistics

| Item | Median | Range (IQR) | n papers | Notes |
|---|---|---|---|---|
| Datasets per paper | **1** | 1-54 (IQR 1-2.5) | 29 | Full-text only: median **2** (1-54, IQR 1-5, n=15). The 54 is the FETS benchmark (100867). 16/29 use a single dataset. |
| Baselines per paper | **2.5** | 0-14 (IQR 1-5) | 22 | Full-text only: median **2** (0-13, n=15). Three papers have 13-14 baselines (100942, 100704, 100670). |
| Random seeds / repeated runs | 10 (only 3 values: 1, 10, 15) | 1-15 | 3 of 15 full texts | 12/15 full texts give no seed or repeat count. Reporting seeds is **not** the norm. |
| Formal statistical tests | - | - | 15 full texts (meta-study excluded) | **4/15 (27%)** run a significance test: Wilcoxon signed-rank; Friedman + Nemenyi; Friedman + Holm-Wilcoxon; critical-difference diagrams. Two of these also give bootstrap CIs. Two more abstract-only papers claim "statistically" better or best groups without naming a test. |
| Ablation study | - | - | 16 full texts | **3/16 (19%)** yes. Abstract-only papers: 4/24 mention one (lower bound). |
| Robustness / cross-dataset / cross-asset test | - | - | 16 full texts | **9/16 (56%)** yes. Abstract-only: 10/24 mention one (lower bound). |
| Real-world data or deployment evidence | - | - | 37 decidable | **26/37 (70%)** yes: full text 11/16, abstracts 15/21 decidable. |
| Code publicly available | - | - | 15 full texts decidable | **9/15 (60%)** yes; 1 more only promises a repository. Abstract-only: 1/24 states code availability. The full-text share is likely inflated by arXiv-posting authors. |
| Length (journal pages) | **16.5** | 11-19 | 4 | Only from Elsevier-typeset PDFs. Small n. |
| Figures (main text) | **10** | 1-17 (IQR 7-13) | 16 | Counted from arXiv versions. |
| Tables (main text) | **3.5** | 0-11 (IQR 2-9) | 16 | Counted from arXiv versions. Appendix tables are common in addition (up to 19). |
| References | **49.5** | 22-100 (IQR 36-61) | 40 | Crossref. Full-text subset median 52.5 (n=16). |

## Typical novelty claimed

The novelty is almost always **methodological-applied**. A known ML family is adapted or combined and then shown to work on one specific energy asset or problem. Recurring patterns:

1. **Physics-guided or hybrid models.** Examples: physics-guided memory network, physics-informed clustering + SHAP/LIME, noise-resilient physics-guided FDD classifiers, mechanics-consistent speed-invariant autoencoder.
2. **Learning with scarce labels or scarce data.** Transfer learning between turbines, CycleGAN domain mapping, self-supervised or contrastive pretraining, semi-supervised learning, synthetic data or generative augmentation (diffusion, TimeGAN, normalizing flow, capacity-fade generator).
3. **Unsupervised normal-behaviour or anomaly models that need only healthy data.** Autoencoders, isolation forest variants, SVDD, clustering with peer or neighbour comparison.
4. **Foundation models and LLMs applied to energy tasks.** Zero-shot TSFM evaluation, an LLM agent for maintenance, LLM-based HVAC control.
5. **Systematic benchmarks or evaluation frameworks.** Examples: concept-drift detectors in district heating, smart-meter deep models, TSFM benchmark over 54 datasets, ensemble decomposition, a reproducibility audit.
6. **Field or experimental validation as the contribution in itself.** Examples: real-house EMS validation, heat-pump evaporator FDD rig, HIL digital twin.

"First to ..." claims are common (seen in 100626, 100658 and 100448). Interpretability or explainability (SHAP, LIME, Grad-CAM, policy probing) is often added as a secondary contribution.

## Applied vs theoretical balance

- **Applied.** All 40 sampled papers are applied or empirical. One is a meta-research study (100658).
- **Formal theory.** A formal component appears only as a supplement, in 3 papers: universal-approximation-type theorems in 100538, grounding and consistency proofs in 100828, and theoretical analysis of the augmentation in 100862.
- **Typical paper.** The usual article is a method paired with a case study on real or lab data. Pure theory papers did not appear in the sample.

## To meet or exceed the median, a paper should have ...

- **Data.** At least **2 datasets**, or at least 2 sites or assets (median 1 overall, 2 among full texts). Ideally one of them is real operational or field data, since about 70% of papers have real-world evidence.
- **Baselines.** At least **3 baselines** (median 2-2.5). Include one simple or classical reference (rule, persistence, threshold or classical ML) and one current deep or foundation-model method. The strongest papers compare 8-14 methods.
- **Robustness.** A **robustness or cross-dataset / cross-asset test**, such as transfer to unseen turbines, substations or networks, noise stress tests, or data-scarcity levels (56% of full texts).
- **Ablation.** An **ablation** of the proposed components. Only about 19% do this, so it is an easy way to stand out.
- **Statistics.** Repeated runs with stated seeds and **a significance test** (Wilcoxon / Friedman-Nemenyi / bootstrap CIs). Only about 27% run a test and 3/15 report seeds, so this would be above the norm.
- **Code.** **Public code** (GitHub + Zenodo DOI) and a data-availability statement. 60% of arXiv-posting authors share code, and the journal's back matter has a data-availability slot.
- **Size.** About **10 figures, 3-4 main tables, 45-55 references**, and roughly 16-17 typeset journal pages (based on only 4 papers).
- **Deployment evidence.** Some practical or deployment discussion: latency or compute cost, edge or online use, or a case study showing early detection before a documented failure.
