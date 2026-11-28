# Hostile prior-art re-check (2026-11-28)

Scope: the revised headline claims (A) false-alarm burden and precision inflation of benchmark-optimal thresholds, (B) selection/spectrum bias of curated "normal" periods, (C) out-of-sample threshold selection and ranking agreement. This builds on `claim_table.md` and `selection_effect_claim.md` (2026-11-24); items recorded there are not repeated unless their status changed.
Sources: OpenAlex, Crossref and arXiv APIs only. ScienceDirect, Semantic Scholar and Google Scholar were not used. 51 logged query records: 1 citation-graph query, 30 OpenAlex, 5 Crossref, 13 arXiv, plus 2 arXiv id lookups and DOI verifications (not counted). Each paper below was judged from its abstract (OpenAlex `abstract_inverted_index` or arXiv summary); no full texts were read in this pass. Every DOI in the tables resolved on Crossref (`api.crossref.org/works/<doi>`), or on doi.org for the DataCite DOIs of arXiv and Zenodo items.

## 1. Citation graph (works citing PreDist or CARE)

- PreDist: OpenAlex W7159838334. The arXiv 2511.14791 record is merged into it. 6 citing works.
- CARE to Compare: OpenAlex W4404700659. The arXiv 2404.10320 record is merged into it. 69 citing works.
- Total: 75 records, against 70 (64 + 6) on 2026-11-24. All 75 abstracts were screened by keyword (false alarm, threshold, alarm, normal event, benchmark, precision, deploy, continuous, selection, bias, realistic). The 15 that matched or looked related were read in full abstract.

**Records new since 2026-11-24, or not in claim_table/selection_effect, that were screened:**

| DOI / id | Year | Posted (OA created) | Overlap | Note (one sentence) |
|---|---|---|---|---|
| 10.63330/armv2n11-032 (Neres et al., Aurum Rev. Multidisc.) | 2026 | 2026-11-26 | none | Uses CARE gearbox and generator events with statistical temperature limits. It is retrospective and has no FA-rate or benchmark-protocol analysis. |
| 10.14488/enegep2026_tn_wpg_436_2154_54471 (Guimarães & Melani, ENEGEP) | 2026 | 2026-11-02 | none | Compares LSTM with LSTM-AE on SCADA and says LSTM has a "lower false-alarm rate". There is no continuous or per-year FA analysis. |
| 10.1016/j.egyai.2026.100959 (Tahavori & Shaker, *Energy and AI*) | 2026 | 2026-11-07 | weak C | A review of time-series foundation models that calls for "leakage-aware evaluation" and local calibration. It has no experiment on benchmark thresholds. Worth citing because it appeared in the target journal. |
| 10.5281/zenodo.24004701 (scada-schema) | 2026 | 2026-11-07 | none | A data-format standard. |
| 10.3390/en19225537 (Bousla et al., *Energies*) | 2026 | 2026-11-18 | indirect A | Monte Carlo O&M study. It finds "about three quarters of the PdM advantage stems from the assumed warning time and detection performance". Detection performance is an input assumption there and is not measured. It is citable as motivation that FA and detection rates drive PdM value. |
| 10.23919/aeit72316.2026.11779339 (AEIT 2026) | 2026 | 2026-11-19 | none | Simulated FOWLTY benchmark with event-level delays. |
| "Architecture-Level Fusion of SCADA and ERA5 ..." (thesis, no DOI) | 2026 | 2026-08-07 | none | Reports winter precision on CARE and false-positive reduction. It uses a pointwise, test-set protocol with no per-year burden. **UNVERIFIED** (no DOI). |
| "Applying Agentic AI for PdM ... Offshore Wind" (no DOI) and two Tsetlin-machine CARE papers (no DOI) | 2025-2026 | 2026-11-20 | none | Method papers. **UNVERIFIED** (no DOI). |
| 10.1109/access.2026.3694778 (Benabdesselam et al., *IEEE Access*) | 2026 | 2026-05-20 | weak A | 207 turbines and 3 manufacturers, with "false positive rate below 21%" at the event level. It does not convert this to a rate per turbine-year. |
| 10.3390/s26175585 (Ma et al., *Sensors*) | 2026 | 2026-09-02 | weak C | Finds that "ranking can transfer, but operating thresholds require plant-specific calibration". The data are TEP and a wind-farm simulator, not CARE or PreDist. |
| 10.1109/sege70974.2026.11738938 | 2026 | 2026-10-27 | none | Uses a single CARE event only as a consistency check. |

The remaining citing works are method, application or review papers (fault classifiers, forecasting, GNNs, LLM alerting, inspection imagery). None of them mentions false alarms per asset-year, curated normal periods versus ordinary operation, or threshold selection versus deployment ranking. Already-known citing papers were re-checked and keep their status: Song 2026 (zenodo.23902231), scada-fault-bench (zenodo.24164281), Haneef 2026, Liu WES-D 2026, Vural 2026, arXiv 2611.25252 and arXiv 2611.04682.

## 2. Query log

| # | Source | Query | Filter | Hits |
|---|---|---|---|---|
| 1 | openalex | cites:W7159838334 (PreDist) / cites:W4404700659 (CARE), all pages | cites | 75 |
| 2 | openalex | curated normal periods anomaly detection benchmark bias |  | 3635 |
| 3 | openalex | hand-picked normal data false alarm underestimated |  | 2200 |
| 4 | openalex | spectrum bias fault detection benchmark |  | 17380 |
| 5 | openalex | selection bias negative samples anomaly detection evaluation |  | 106236 |
| 6 | openalex | false alarms per turbine per year SCADA |  | 880 |
| 7 | openalex | false alarm rate continuous operation wind turbine condition monitoring |  | 4209 |
| 8 | openalex | acceptable false alarm rate condition monitoring operators |  | 17230 |
| 9 | openalex | tolerable false alarm rate predictive maintenance |  | 3130 |
| 10 | openalex | alarm fatigue district heating fault detection |  | 324 |
| 11 | openalex | benchmark threshold optimistic deployment false alarm burden anomaly detection |  | 491 |
| 12 | openalex | evaluation on all normal operation versus selected normal windows anomaly detection |  | 70153 |
| 13 | openalex | alarm rate per operator per hour EEMUA 191 |  | 49 |
| 14 | openalex | ISA-18.2 alarm management rate benchmark |  | 131 |
| 15 | crossref | overview industrial alarm systems alarm overloading EEMUA |  | 5820882 |
| 16 | crossref | alarm flood one alarm per ten minutes operator standard |  | 1915538 |
| 17 | crossref | false alarm cost wind turbine condition monitoring operator trust |  | 2154498 |
| 18 | crossref | curated normal windows benchmark optimistic false positive rate |  | 1534304 |
| 19 | crossref | false alarms per year district heating substation fault detection |  | 2969674 |
| 20 | openalex | "alarms per 10 minutes" |  | 33 |
| 21 | openalex | "one alarm per 10 minutes" |  | 3 |
| 22 | openalex | "alarms per operator" EEMUA |  | 7 |
| 23 | openalex | "150 alarms per day" |  | 3 |
| 24 | openalex | "false alarms per turbine" |  | 1 |
| 25 | openalex | "false alarm per year" condition monitoring |  | 51 |
| 26 | openalex | "false alarms per year" wind |  | 23 |
| 27 | openalex | "per turbine per year" false alarms |  | 38 |
| 28 | openalex | "false alarm rate" acceptable wind turbine operators |  | 303 |
| 29 | openalex | "alarms per week" condition monitoring |  | 28 |
| 30 | openalex | "acceptable false alarm rate" maintenance |  | 124 |
| 31 | openalex | "tolerable false alarm" |  | 160 |
| 32 | arxiv | all:"false alarm" AND all:"wind turbine" AND all:SCADA |  | 0 |
| 33 | arxiv | all:"CARE to Compare" |  | 22 |
| 34 | arxiv | all:PreDist |  | 5 |
| 35 | arxiv | all:"district heating" AND all:"false alarm" |  | 1 |
| 36 | arxiv | abs:"anomaly detection" AND abs:benchmark AND abs:"selection bias" |  | 0 |
| 37 | arxiv | abs:"anomaly detection" AND abs:"normal" AND abs:"curated" AND abs:"false positive" |  | 1 |
| 38 | arxiv | abs:"alarm budget" |  | 17 |
| 39 | arxiv | abs:"false alarms per" AND abs:"year" |  | 3 |
| 40 | arxiv | abs:"wind turbine" AND abs:"false alarms" |  | 2 |
| 41 | arxiv | abs:"wind turbine" AND abs:"anomaly detection" AND abs:"threshold" AND abs:"evaluation" |  | 1 |
| 42 | arxiv | abs:"district heating" AND abs:"fault detection" |  | 3 |
| 43 | arxiv | abs:"anomaly detection" AND abs:"benchmark" AND abs:"spectrum bias" |  | 0 |
| 44 | arxiv | abs:"anomaly detection" AND abs:"deployment" AND abs:"precision" AND abs:"prevalence" |  | 2 |
| 45 | openalex | wind turbine early fault detection evaluation false alarms continuous operation | from_publication_date:2026-06-01 | 356 |
| 46 | openalex | anomaly detection benchmark ranking deployment threshold selection held-out | from_publication_date:2026-06-01 | 2372 |
| 47 | openalex | district heating substation fault detection false alarms deployment | from_publication_date:2026-06-01 | 18 |
| 48 | openalex | normal operation windows selection anomaly benchmark easier than random | from_publication_date:2026-06-01 | 1600 |
| 49 | openalex | SCADA anomaly detection precision realistic prevalence | from_publication_date:2026-06-01 | 83 |
| 50 | openalex | HVAC fault detection diagnostics false alarm rate evaluation methodology acceptable |  | 479 |
| 51 | openalex | "false alarm rate" fault detection diagnostics air handling unit evaluation |  | 1000 |

Note: Crossref totals are those of `query.bibliographic`, which ranks rather than filters, so they are meaningless as counts. Only the top 10-12 results were screened. The arXiv API index returned fewer matches than expected for some quoted phrases. arXiv was therefore cross-checked through OpenAlex, which indexes arXiv DOIs.

## 3. Relevant papers found in this pass (DOI verified)

| DOI / arXiv | Year | Venue | Overlap | Difference from our paper (one sentence) |
|---|---|---|---|---|
| arXiv 2610.38786 (Blakely) | 2026 | arXiv preprint | C (partial), A (concept) | Process-industry security disturbances (simulated chemical process plus a sodium facility). It reads detection "at a declared false-alarm budget" and notes the plant gap is one "that in-sample thresholds likely understate". It is not energy CM, not CARE or PreDist, and has no curated-normal analysis. |
| 10.53365/nrfhh.1524 (Gandhi) | 2026 | Nat. Resour. Hum. Health | C (concept) | Quantifies leakage modes, including threshold selection, on a *simulated* fed-batch benchmark (F1 inflated by 0.103). It is not about ranking agreement and not about energy. |
| 10.1038/s41598-026-78345-0 (Farmani et al.) | 2026 | Sci. Rep. | C (concept) | An IDS benchmarking framework with "threshold dynamics" and drift-aware online evaluation. It is a generic cyber-security framework with no event-versus-continuous protocol comparison. |
| 10.1109/icmla69890.2026.00037 (Szklarzewski et al.) | 2026 | ICMLA | B (weak) | Visual inspection. It says "curated academic benchmarks" overstate stability and that "nominal-data quality affects deployment". It is image AD and does not measure the alarm rate on curated versus random normal data. |
| 10.37965/jdmd.2026.1653 (Wang et al.) | 2026 | J. Dyn. Monit. Diagn. | A (weak) | Kaplan hydro turbine with 365 days of field SCADA, reporting the "routine false alarms" fraction (0.030872 to 0.000441). It is a single method, not a benchmark critique. |
| arXiv 2610.04392 (Heckler-Kram et al., VAND 4.0) | 2026 | arXiv / CVPR-W | A (concept) | Calls existing AD benchmarks "saturated and often unrealistic" and releases a low-prevalence dataset. It is image AD with no precision-inflation measurement. |
| 10.3390/en15197317 (Teixeira, Sanz-Bobi et al.) | 2022 | Energies | A (weak) | Reduces false alarms in wind normal-behaviour models with multi-agent cooperation. It gives no FA-per-year budget. |
| 10.1049/rpg2.13104 (Liu et al.) | 2024 | IET RPG | A (weak) | A wind generator fault diagnosis review that proposes "a qualitative and quantitative assessment of algorithm performance using false alarm rates". The abstract gives no numeric budget. |
| 10.1016/j.egyai.2026.100959 | 2026 | Energy and AI | C (weak) | See Section 1. |
| 10.3390/en19225537 | 2026 | Energies | A (indirect) | See Section 1. |

No paper found in this pass (or in the 2026-11-24 pass) replays benchmark-optimal thresholds over the full continuous history of CARE or PreDist, reports FA per turbine-year or FA days per substation-year, or measures a precision inflation factor. No paper compares alarm rates on curated normal events with those on random normal operation of the same assets. No paper tests whether out-of-sample threshold selection improves agreement between benchmark and deployment rankings.

## 4. Tolerable / acceptable false-alarm-rate sources

**No source was found for a tolerable FA budget per turbine-year or per substation-year** (wind, district heating or HVAC FDD), in this pass or the previous one. What exists:

| Source (verified DOI) | Domain | Exact statement (from abstract) | Usability for our paper |
|---|---|---|---|
| Reising, Downs & Bayn 2004, *Proc. HFES Annual Meeting* 48(10), 10.1177/154193120404801009 | Process-industry control rooms (EEMUA 191) | "The Engineering Equipment and Materials User Association (EEMUA) recently published recommendations for average and peak alarm rates of 1 alarm per 10 minutes during normal operations and no more than 10 alarms per 10 minutes following an upset condition, respectively. However, these recommendations have been made in the absence of human performance studies or theory." ... "Results suggest that these EEMUA recommendations are in line with human performance limits." | **Best citable secondary source for the EEMUA 191 figure.** It is a per-*operator* console rate, so it bounds total alarm load and is not a per-asset CM budget. It can be used for an order-of-magnitude analyst-workload argument, labelled as an analogy. |
| Goetz 2017, SPE/IADC Drilling Conf., 10.2118/184659-MS | Offshore drilling control alarms | "Table 1 from Principles for Alarm System Design, February 2001, YA - 711, Norwegian [Petroleum Directorate] Alarm Rate Consequence: 1 alarm per minute Very Likely to be unacceptable; 1 alarm per 2 minutes Likely to be over-demanding; 1 alarm per 5 minutes Manageable; 1 alarm per 10 minutes Very likely to be acceptable" ... "Other recognized standards including ISA 18.2 and EEMUA 191 mirror these expectations." | Secondary source for the NPD YA-711 table. Same caveat: per-operator console alarms. |
| Uhack 2010, LSU thesis, 10.31390/gradschool_theses.4148 | Pipeline control rooms | "a severe operator performance reduction ... was observed when the alarm rate was increased from ten alarms per ten minutes ... to twenty alarms per ten minutes." | Empirical support for upper alarm-rate limits. Control room, not CM. |
| Dórea et al. 2013, *PLoS ONE*, 10.1371/journal.pone.0082183 | Veterinary syndromic surveillance | "the number of false alarms per year when the approach was applied to real data was considered manageable (between 1 and 3 per year for each of ten syndromic groups monitored)." | **The only numeric "manageable FA per year per monitored stream" statement found.** It is from another domain, but it is the closest analogue to a per-asset-year budget. It can be cited as an analogy only. |
| Nocentini et al. 2023, *Landslides*, 10.1007/s10346-023-02176-7 | Landslide early warning | "A calibration phase was performed to minimize the impact of false alarms, allowing at least one false alarm per year over the moderate criticality level." | A design-choice FA/yr budget in an early-warning system. Analogy only. |
| Nickerson 1997, *JASA* 101(5), 10.1121/1.418570 | Machinery CBM / prognostics | "a methodology for setting acceptable false alarm rates for both diagnostics and prognostics is presented" | Gives a method, not a number. Useful to justify deriving the budget from costs. |
| Koops 2018, PHM Society Europe, 10.36001/phme.2018.v4i1.460 | Aircraft-engine PdM | "a general cost-benefit analysis based on the ROC curve ... allows deducing application-specific requirements on the failure prediction quality for achieving a net benefit" | Supports presenting results as a function of the FA budget or cost ratio rather than one fixed tolerable number. |
| Wang et al. 2016, *IEEE T-ASE*, 10.1109/TASE.2015.2464234 | Industrial alarm systems (thermal power plant) | "most existing industrial alarm systems suffer from poor performance, noticeably having too many alarms to be handled by operators" | Alarm-overload motivation. No number in the abstract. |
| Howard 2007, *Measurement and Control* 40(8), 10.1177/002029400704000805 | EEMUA 191, 2nd ed. | Launch note; no abstract available. | Confirms EEMUA 191 2nd ed. (2007) exists as a publication. The standard itself (EEMUA Publication 191; ANSI/ISA-18.2-2016; IEC 62682) has no DOI and was not accessible. Quoting its tables directly is therefore **UNVERIFIED** here. Commonly cited ISA-18.2 figures ("~150 alarms/day very likely acceptable, ~300 maximum manageable") were **not verified** from any accessible source in this session. |
| Already in claim_table: NIST TN 2118, 10.6028/nist.tn.2118 | Radiation portal monitors | FA-rate testing requirements and alarm fatigue. | Method for testing an FA requirement. |

Recommendation: keep the FA budget as a swept parameter (e.g. 1, 2, 5, 12 FA per asset-year) and report results as curves. Cite EEMUA 191 via Reising et al. 2004 and NPD YA-711 via Goetz 2017 only for a workload conversion. For example, a 1-alarm-per-10-minutes console limit is a ceiling on *total* alarms per analyst and says nothing directly about CM site visits. Cite Dórea 2013 and Nocentini 2023 as cross-domain examples of "~1-3 FA per monitored unit per year judged manageable". Do **not** present any "1-2 FA/turbine-year is tolerable" figure as an established wind or DH industry norm; no source supports it.

## 5. Verdict per claim

| Claim | Verdict | Reasoning |
|---|---|---|
| **A** Benchmark-optimal thresholds imply 6.7-16.7 FA/turbine-yr and 83-176 FA days/substation-yr; benchmark precision overstates deployed precision 7.6-20.6x | **Novel as measurement; narrowed as concept (unchanged from 2026-11-24)** | The base-rate mechanism is textbook (Axelsson; Saito & Rehmsmeier), and PreDist itself concedes that precision is overestimated under its 50/50 split. No paper, including all 75 citing works, replays CARE or PreDist thresholds over continuous operation or reports per-asset-year burdens. The phrase should be "we quantify the overestimation acknowledged by Roelofs et al.". |
| **B** Curated normal periods attract alarms at 0.21-0.42x the rate of random normal operation for nearly all of 15-17 detectors | **Novel in energy / fault-detection benchmarks; concept established elsewhere (unchanged)** | Spectrum or case-control bias is classic in diagnostic medicine (Ransohoff & Feinstein 1978; Lijmer 1999; Rutjes 2006). ML analogues exist (Ben-Hur & Noble 2006). A new weak non-energy echo is Szklarzewski et al. 2026 ("nominal-data quality affects deployment", image AD, not measured). No energy or time-series benchmark paper measures curated-versus-random normal alarm rates, and PreDist only says normal events "could be refined". |
| **C** Out-of-sample threshold selection improves benchmark-deployment rank agreement (direction consistent, not significant) | **Narrowed / largely already done in concept** | Threshold leakage and test-set calibration bias are established (Cools et al. 2026; Kim et al. AAAI 2022; Liu WES-D 2026 on CARE; Haneef 2026; Salem & Ferrugem 2026). New concept-level echoes are Blakely arXiv 2610.38786 ("in-sample thresholds likely understate"), Gandhi 2026 (threshold-selection leakage) and Ma et al. 2026 ("operating thresholds require plant-specific calibration"). The specific test (rank agreement between event benchmark and continuous deployment, with vs without out-of-sample thresholds, on CARE and PreDist) was not found. Because the effect is not significant, C should be a secondary or supporting result, not a headline. |

**Bottom line:** no paper found already does A or B on PreDist or CARE (or on any energy benchmark). The threat level is unchanged from 2026-11-24, with Song 2026 (Zenodo, unreviewed) still the closest for A and C. No wind or district-heating tolerable-FA source exists in the accessible literature. The citable anchors are EEMUA 191 (via 10.1177/154193120404801009), NPD YA-711 (via 10.2118/184659-MS) and the cross-domain "1-3 FA/yr per monitored stream manageable" (10.1371/journal.pone.0082183), each labelled as an analogy.
