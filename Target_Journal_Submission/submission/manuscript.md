---
title: "Benchmark scores do not show deployable fault detection: false-alarm burden and curated-normal bias on district heating and wind turbine data"
author: "[Author names and affiliations to be completed by the authors]"
---

<!-- Every number in this manuscript is traced to a committed result file; see submission/NUMBER_SOURCES.md. -->

# Highlights

- Balanced event benchmarks were replayed continuously on 35 substations and 36 wind turbines.
- Benchmark-chosen thresholds imply 6.7–16.7 false alarms per turbine-year.
- On district heating they imply 83–176 false-alarm days per substation-year.
- Curated normal periods attract 0.21–0.42 times the alarms of random normal time.
- Ranking shifts are consistent in direction but not significant under calibrated tests.

# Abstract

Public benchmarks for early fault detection in energy systems score detectors on short event windows. These windows are balanced between faults and hand-picked normal periods, and the decision thresholds are tuned on the events being scored. Operators, by contrast, run a detector continuously and with a fixed threshold. They judge it by the number of faults it finds within a tolerable number of false alarms. We measure the distance between these two views on two public, labelled benchmarks. The first is PreDist, with 35 district heating substations, and the second is CARE to Compare, with 36 wind turbines in three farms. We use a pre-registered panel of 15–17 detectors that ranges from z-scores to conditional autoencoders. The same online scores are evaluated under four protocols. These cross balanced event windows or continuous replay with thresholds tuned on the evaluated events or chosen out of sample. Thresholds that maximise the benchmark score imply 6.7–16.7 false alarms per turbine-year in continuous operation. On district heating they imply 83–176 false-alarm days per substation-year. Benchmark precision exceeds deployed alarm precision by 7.6–20.6 times. The curated normal periods are systematically quieter than ordinary operation: they attract alarms at 0.21 (95% CI 0.05–0.37) and 0.42 (0.27–0.61) times the rate of random normal windows. Agreement between benchmark and deployment-like detector rankings is low (Kendall τ 0.34 and 0.43). It is higher when thresholds are chosen out of sample (0.65 and 0.74), in all ten seed–dataset combinations. However, this ranking effect is not statistically established once the bootstrap is calibrated. We give a reporting checklist that makes benchmark results interpretable for deployment.

**Keywords:** fault detection; anomaly detection; evaluation protocol; false alarms; district heating; wind turbine SCADA

# Nomenclature

| Acronym | Meaning |
|---|---|
| AE | autoencoder |
| CH | continuous replay, out-of-sample thresholds (deployment-like reference) |
| CT | continuous replay, thresholds tuned in sample |
| DH | district heating |
| EH | event windows, out-of-sample thresholds |
| ET | event windows, thresholds tuned on the evaluated events (benchmark practice) |
| FA | false alarm |
| LOFO | leave-one-farm-out |
| NBM | normal-behaviour model |
| SCADA | supervisory control and data acquisition |

# 1. Introduction

Data-driven early fault detection is one of the most active applications of machine learning in energy systems. District heating substations and wind turbines are typical targets. Both record operational data at 10-minute resolution from many similar assets, faults are costly, and labelled faults are rare [21, 24, 32]. In district heating, undetected substation faults also raise return temperatures and the cost of low-temperature networks [22, 23, 33]. Most proposed detectors are unsupervised normal-behaviour models. They raise an alarm when the measured behaviour departs from the learned normal behaviour by more than a threshold [19, 24, 28].

A detector is only useful if operators can act on its alarms. Experience with industrial alarm systems shows that alarm floods are common and that a high alarm rate is itself a safety and cost problem [25, 26]. The operational question is therefore concrete. How many faults does the detector find before they are reported, at a number of false alarms per asset and year that the operator can follow up?

Public benchmarks answer a different question. The two labelled public datasets used here are typical. PreDist [1] and CARE to Compare [2] score detectors on short windows before known faults and on a similar number of hand-picked normal periods. The decision threshold is chosen to maximise an event-level F0.5 score on these same events. The PreDist authors state that this balanced design overestimates precision, because faults are far rarer in practice [1]. Studies of time-series anomaly detection outside energy have also shown three things:

- point-adjusted and tuned evaluation can mislead model rankings [3, 13];
- calibrating thresholds on test data biases results [5];
- low-false-alarm evaluation changes rankings [4].

On wind SCADA data, recent studies report the following under leakage-controlled or cross-asset protocols [6–9]:

- optimistic same-asset thresholds;
- excessive false alarms;
- weak discrimination at an alarm budget.

What is missing is a measurement of how far the benchmark view is from deployment, on the benchmarks that the energy community actually uses. Such a measurement should replay every detector over the full continuous history of every asset. It should cover enough detectors for rank statistics, and the analysis plan should be fixed before the results are seen. The closest work in this journal uses PreDist with window-level scores and an upper-bound F1 [14]. Energy and AI has also published evaluation studies showing that aggregate scores can mislead model choice in forecasting [15] and that standard evaluation can overstate cross-laboratory generalisation [16]. This paper brings the same kind of scrutiny to fault-detection benchmarks.

We do not claim that the base-rate effect is new [10, 11] or that threshold leakage is new [3–5]. Our contributions are measurements and a reporting proposal:

1. **We quantify the false-alarm burden that benchmark-chosen thresholds imply in continuous operation.** The measurement covers two public energy benchmarks and 15–17 detectors. The resulting burdens range from 6.7 to 16.7 alarms per turbine-year and from 83 to 176 alarm days per substation-year.
2. **We identify and measure a selection effect in benchmark construction.** Curated normal periods are quieter than random normal time for 16 of 17 and 13 of 14 detectors. This holds in every seed, and it inflates benchmark precision beyond the base-rate effect.
3. **We test, with a pre-registered 2×2 factorial, whether threshold source or window design drives the gap between benchmark and deployment rankings.** We report that the effect is consistent in direction on both datasets. It is not statistically established once the bootstrap is calibrated, and we explain why rank-based claims of this kind need more detectors and events than current benchmarks provide.
4. **We propose a reporting checklist.** It lets a benchmark result be read in operator units.

Section 2 reviews related work. Section 3 describes the data and detectors, and Section 4 the protocols and statistics. Section 5 reports the results, Section 6 discusses implications and limitations, and Section 7 concludes.

# 2. Related work

**Benchmarks for early fault detection in energy systems.** CARE to Compare [2] provides SCADA data of 36 turbines from three wind farms. It has 95 labelled events: 44–45 anomalies and 50–51 normal periods, depending on the version. It also defines the CARE score, a weighted mean of four components:

- coverage, a pointwise F0.5;
- accuracy on normal periods;
- reliability, an event-wise F0.5;
- earliness.

PreDist [1] provides 10-minute data from 93 district heating substations of two controller manufacturers, labelled from service records. Its reliability score is an event-wise F0.5 over fault windows and normal events, with the threshold selected by cross-validation over the evaluated events. Both papers present the balanced event design as a deliberate choice for comparability, and PreDist explicitly notes the precision overestimate [1]. Van Dreven et al. [14] evaluate a self-supervised transformer on PreDist using window-level ROC-AUC and macro F1 at an oracle threshold. Other district heating studies report case studies, substation-level accuracy or sample-level false-alarm counts [18, 21, 24, 27, 28]. A drift-detection benchmark for district heating [17] and a reproducibility study of HVAC fault detection [20] in this journal also argue that evaluation design shapes reported performance.

**Evaluation pitfalls in anomaly detection.** The base-rate fallacy [10] and the weakness of ROC analysis on imbalanced data [11] are textbook issues. For time series, Kim et al. [3] showed that point adjustment produces misleading rankings, and Wu and Keogh [13] criticised unrealistic anomaly density in popular benchmarks. Cools et al. [5] showed that calibrating thresholds on the test set biases reported performance, and Salem and Ferrugem [4] showed that low-false-alarm evaluation changes detector rankings. Lavin and Ahmad [30] proposed a streaming benchmark that rewards early detection and penalises false positives.

**Wind turbine SCADA.** Recent CARE-based studies use leakage-controlled calibration [6], cross-asset conformal monitoring [8] and farm-specific models [9]. An unreviewed, pre-registered reproducibility study evaluates detectors at an alarm budget against random alarms and reports weak discrimination [7]. Our work differs in three ways. We replay benchmark-chosen thresholds over the full continuous record. We measure the curated-normal selection effect. We decompose ranking disagreement into threshold-source and window-design factors on two domains under one protocol.

**Statistical design of false-alarm tests.** False-alarm testing standards use binomial and Poisson power calculations to size such tests [12]. We use the same reasoning to show how little a benchmark's normal periods can certify about a deployed false-alarm rate.

# 3. Data and detectors

## 3.1 Datasets

**PreDist** [1] (CC BY 4.0) contains data from 93 German district heating substations. We use the 35 substations of the first controller manufacturer, about 144 substation-years of 10-minute data. The 58 substations of the second manufacturer were used in an earlier locked transfer test that was evaluated more than once. They are therefore excluded from all analyses here (Section 6.3). There are 29 early-detectable fault reports. The detection window is the 7 days before each report, as defined by the dataset [1]. The 35 curated normal events come from the dataset's event list.

**CARE to Compare** [2] contains 36 turbines in three farms and 95 events: 45 anomalies and 50 normal periods in the version used. The event windows are those of the dataset.

## 3.2 Detector panel

The panel was fixed before any score was computed (pre-registration plan_v2; Supplementary S2). It has 12 generic detectors that run on both datasets:

- per-signal maximum and mean z-scores, a robust z-score, an EWMA z-score and a quantile-exceedance fraction;
- PCA residual (SPE) and Hotelling T²;
- Ledoit–Wolf Mahalanobis distance;
- k-nearest-neighbour, LOF and GMM scores on PCA components;
- an isolation forest on PCA components [29].

The panel also includes dataset-specific detectors from earlier rounds. On PreDist these are an expert control-loop rule, a loop-residual three-sigma statistic, an own-history quantile NBM [28], the PreDist benchmark autoencoder [1] and a conditional autoencoder. On CARE they are a temperature three-sigma statistic, an autoencoder and a conditional autoencoder.

Every detector is trained online on the asset's own past: it is retrained every 90 days, and its nominal threshold is the 99th percentile of its training scores. Stochastic detectors were run with seeds 0–4. All detectors share one alarm logic. A persistence counter increases when the score exceeds τ and decreases otherwise, and an alarm is active while the counter is at least c. The (τ, c) grid is the same for every detector.

# 4. Evaluation protocols and statistics

## 4.1 Four protocols

Each detector's online score series is evaluated in a 2×2 design (Table 1).

The **window design** is either:

- *event windows*: the benchmark's fault windows and curated normal events, with an event counted as flagged if an alarm is active anywhere in its window; or
- *continuous replay*: every monitored step of every asset, counting alarm starts outside fault windows and exclusion intervals as false alarms per asset-year.

The **threshold source** is either:

- *tuned on the evaluated events*: the (τ, c) that maximises event F0.5, or recall at ≤ 2 FA per asset-year in the continuous case; or
- *out of sample*: the point chosen on held-out assets at a budget of B = 2 FA per asset-year. On CARE the held-out set is defined by leave-one-farm-out; on PreDist by 5-fold substation cross-validation with fixed folds.

The CH cell (continuous replay, out-of-sample thresholds) is the deployment-like reference.

**Table 1.** The four protocol cells.

| | Thresholds tuned on evaluated events | Thresholds chosen out of sample |
|---|---|---|
| **Event windows** | ET (benchmark practice): event F0.5 | EH: event F0.5 at held-out B = 2 point |
| **Continuous replay** | CT: recall at in-sample point with ≤ 2 FA/asset-yr | **CH (reference)**: recall at held-out B = 2 point |

## 4.2 Hypotheses and pre-registration

All hypotheses and the analysis script were committed before any panel score existed (plan_v2). They are:

- **H7a, threshold source:** τ(EH, CH) − τ(ET, CH) > 0.
- **H7b, window design:** τ(CT, CH) − τ(ET, CH) > 0.
- **H7d, selection effect:** the pooled alarm-hit rate on curated normal events divided by the rate on 2,000 random eligible normal windows of matched length is below 1.

τ is Kendall's tau between the per-detector scores of two cells. Tests are one-sided, using a cluster bootstrap over assets with 2,000 replicates [31, 34]. Tuned cells are re-tuned inside each replicate. Holm's correction is applied over {H7a, H7b} × {PreDist, CARE}. Robustness counts the seeds, out of 5, in which each hypothesis holds.

After a blind internal review found the percentile bootstrap biased towards H7a, we pre-registered Amendment A1 before running it. A1 adds two tests:

- T1, a null-centred bootstrap;
- T2, an exact within-detector label-swap randomisation test.

A result is called *confirmed* only if both T1 and T2 reject after Holm.

## 4.3 Alarm-burden measurements

The burden measurements were pre-registered in earlier rounds.

**CARE.** For each detector we compute:

- the benchmark-optimal (τ, c);
- its continuous FA rate per turbine-year;
- the inflation factor, i.e. event precision divided by deployed alarm precision, at the leave-one-farm-out B = 2 point, with cluster-bootstrap CIs.

**PreDist.** We compute the oracle threshold that maximises macro F1 on a balanced window-level set, in the style of [14]. This set contains 442 asset-days, with all 221 faulty days. We report the false-alarm days per substation-year that this threshold implies over all 45,632 asset-days.

## 4.4 Leakage control

A legacy exclusion rule in the PreDist pipeline let 4 of 588 model refits (substations 4 and 7) see the timing of future fault reports. All PreDist numbers reported as primary use the corrected, leak-free rule (Supplementary S4). The legacy values are shown as a sensitivity analysis. CARE used the leak-free rule from the start.

# 5. Results

## 5.1 Benchmark scores and deployment-like recall

Under benchmark practice (ET), every detector looks useful (Table 2). Event F0.5 is 0.69–0.84 on PreDist and 0.57–0.69 on CARE. Under the deployment-like reference (CH), the same detectors find 7–32% of PreDist faults and 0–27% of CARE anomalies at about 2 false alarms per asset-year.

The detector with the best benchmark score is not the best deployed detector (Fig. 2):

- On PreDist the benchmark favours the loop-residual three-sigma statistic (ET 0.84), which reaches CH recall of 0.11. The GMM detector reaches CH recall of 0.32.
- On CARE the benchmark favours the mean z-score (0.69, CH 0.16), while the conditional autoencoder has the highest CH recall (0.27).

**Table 2.** Benchmark score (ET, event F0.5) and deployment-like recall (CH, continuous, out-of-sample threshold, B = 2) per detector, seed 0. PreDist uses the leak-free rule.

| Detector | PreDist ET | PreDist CH | CARE ET | CARE CH |
|---|---|---|---|---|
| z_max | 0.75 | 0.21 | 0.58 | 0.24 |
| z_mean | 0.78 | 0.18 | 0.69 | 0.16 |
| robust_z_max | 0.69 | 0.11 | 0.57 | 0.04 |
| q_frac | 0.73 | 0.07 | 0.64 | 0.11 |
| pca_spe | 0.82 | 0.14 | 0.60 | 0.16 |
| pca_t2 | 0.78 | 0.25 | 0.60 | 0.11 |
| maha_lw | 0.83 | 0.18 | 0.65 | 0.13 |
| knn_pca | 0.81 | 0.29 | 0.60 | 0.09 |
| lof_pca | 0.83 | 0.29 | 0.60 | 0.09 |
| gmm_pca | 0.83 | 0.32 | 0.61 | 0.11 |
| iforest_pca | 0.77 | 0.29 | 0.59 | 0.00 |
| ewma_z_max | 0.77 | 0.18 | 0.60 | 0.16 |
| expert rule / temp. 3σ | 0.75 | 0.29 | 0.66 | 0.16 |
| loop-residual 3σ | 0.84 | 0.11 | – | – |
| quantile NBM | 0.70 | 0.11 | – | – |
| autoencoder | 0.73 | 0.14 | 0.67 | 0.18 |
| conditional AE | 0.74 | 0.07 | 0.67 | 0.27 |

## 5.2 False-alarm burden at benchmark-chosen thresholds

**CARE.** At the thresholds that maximise the benchmark score, continuous operation yields the following false-alarm rates:

| Detector | False alarms per turbine-year |
|---|---|
| Temperature three-sigma | 6.7 |
| Isolation forest | 10.6 |
| Three-sigma | 10.8 |
| Conditional autoencoder | 15.8 |
| Autoencoder | 16.7 |

Event precision at the benchmark point is 0.55–0.84. Deployed alarm precision at the out-of-sample B = 2 point is 0.036–0.071. The resulting inflation factors are 7.6 (95% CI 5.0–16.7) to 20.6 (13.5–37.4) for the four detectors that raise alarms. The isolation forest raises no alarm at its held-out point, so its ratio is undefined and is reported as such.

**PreDist.** At the oracle threshold of the balanced window protocol, every one of the 17 detectors implies at least 10 false-alarm days per substation-year. The range is 83–176 days, with a median of 135. At natural prevalence (0.5% faulty days), the best achievable macro F1 is 0.50–0.53 for every detector. This is essentially the score of never raising an alarm.

## 5.3 Selection effect in curated normal periods

Curated normal events attract far fewer alarms than ordinary normal operation (Fig. 3). We compared each detector's alarm-hit rate on the curated events with its rate on 2,000 random eligible normal windows, at its held-out B = 2 point. The pooled ratio is:

- 0.21 (95% CI 0.05–0.37) on PreDist (leak-free; legacy 0.30, 0.11–0.52);
- 0.42 (0.27–0.61) on CARE.

The ratio is below 1 for 16 of 17 PreDist detectors and 13 of 14 evaluable CARE detectors. H7d holds in 5 of 5 seeds on CARE and in 5 of 5 seeds on PreDist (seeds 1–4 with the legacy rule; leak-free seed 0).

The effect is detector-dependent:

- On PreDist, ten detectors raise no alarm at all on the 35 curated normal events. The conditional autoencoder (2.45) and the autoencoder (0.76) are the exceptions.
- On CARE, the robust z-score is the exception (3.20).

Because curated normal periods are easier than typical operation, benchmark precision is inflated beyond what the base rate alone explains.

## 5.4 What drives ranking disagreement?

Kendall's τ between the benchmark ranking (ET) and the deployment-like ranking (CH) is low (Fig. 1): 0.34 on PreDist (legacy 0.18) and 0.43 on CARE. Choosing thresholds out of sample (EH) raises it to 0.65 and 0.74. Replaying continuously with in-sample thresholds (CT) raises it on PreDist (0.83) but lowers it on CARE (0.30). The EH > ET pattern appears in all 5 seeds on both datasets (PreDist seeds 1–4: legacy rule).

With the pre-registered percentile bootstrap, Holm rejects three of the four tests (Table 3): H7a on both datasets and H7b on PreDist. H7b on CARE is not rejected in any seed.

Under the calibrated tests of Amendment A1, neither effect is confirmed on either dataset. For H7a, the CARE p-values are 0.065 (T1) and 0.18 (T2), and the PreDist leak-free label-swap p-value is 0.18. We therefore report the threshold-source effect as **consistent in direction but not statistically established**.

Two features of the design limit power:

- With 15–17 detectors, τ has few distinct values.
- The CH reference counts only 2–9 detected faults per detector on PreDist and 0–12 on CARE, so many detectors are tied.

Fig. 4 shows the per-seed p-values of the pre-registered test.

**Table 3.** Ranking-disagreement tests, seed 0, one-sided p-values. Pre-registered = percentile cluster bootstrap with the Holm decision of record; T1 = null-centred bootstrap; T2 = within-detector label swap (Amendment A1). PreDist leak-free has no saved bootstrap replicates, so T1 is given for the legacy run.

| Test | Pre-registered p (Holm) | T1 | T2 |
|---|---|---|---|
| H7a PreDist (leak-free / legacy) | 0.017 / 0.0045 (rejected) | – / 0.0075 | 0.18 / 0.076 |
| H7b PreDist (leak-free / legacy) | 0.012 / 0.0215 (rejected) | – / 0.0015 | 0.092 / 0.027 |
| H7a CARE | 0.0055 (rejected) | 0.065 | 0.18 |
| H7b CARE | 0.1495 (not rejected) | 0.68 | 0.61 |

## 5.5 How much can a benchmark certify?

A benchmark with *n* normal windows can say little about a deployed false-alarm rate. The 65 normal 7-day windows of PreDist give power 0.23 to distinguish 1 from 2 false alarms per asset-year. The 50 normal periods of CARE give power 0.12 with 7-day windows, or 0.35 at their actual mean length of 14.9 days. Even a perfect event score therefore cannot certify an operator's alarm budget.

# 6. Discussion

## 6.1 Implications for practice

For an operator of 100 substations, the PreDist oracle threshold implies roughly 13,500 false-alarm days per year (median 135 per substation). For a 36-turbine fleet, the CARE benchmark-chosen thresholds imply 240–600 false alarms per year. In both cases the benchmark score gives no warning.

Three practical rules follow:

1. Choose thresholds on assets or periods that are not evaluated.
2. Report recall at a stated false-alarm budget per asset-year, measured by continuous replay.
3. Report the false-alarm rate on random normal time, not only on curated normal periods.

## 6.2 Implications for benchmark design and reporting

We propose that early fault detection papers report the following minimum set, in addition to any benchmark score:

- (i) the threshold source and the data it was chosen on;
- (ii) recall at fixed false-alarm budgets in continuous replay, with confidence intervals clustered by asset;
- (iii) the asset-years of normal exposure behind the false-alarm estimate;
- (iv) the alarm rate on random normal windows next to the curated normal events;
- (v) the number of detectors and events behind any ranking claim, with a calibrated test.

Items (ii)–(iv) need only the continuous data that both benchmarks already publish.

## 6.3 Limitations

- **Labels.** The absence of a fault report does not guarantee fault-free operation. Measured false-alarm rates are therefore upper bounds.
- **Event counts.** Fault events are few (29 on PreDist, 45 on CARE), and confidence intervals are wide.
- **Ranking claims.** The ranking analysis is underpowered. Its main contrast is not established under calibrated tests. Some panel members are close variants, so the seeds do not give fully independent replications. Only four panel members are stochastic.
- **Detector coverage.** The panel does not include a large pretrained foundation model.
- **Prior use of the data.** Both datasets had been used in earlier development rounds of this project, so all analyses here are pre-registered but exploratory, not blind.
- **Excluded manufacturer.** The second PreDist manufacturer was excluded because an earlier locked test on it was evaluated more than once.
- **Leakage fix.** Correcting a leak in the legacy PreDist exclusion rule changed individual detector results. One detector's recall changed by 4 of 28 faults. The direction of every conclusion was unchanged, and we report the leak-free numbers as primary.
- **Budget level.** We know of no published operator source for a tolerable alarm budget. Two false alarms per asset-year is therefore an assumption, not an operator requirement.

# 7. Conclusions

On two public energy benchmarks and 15–17 detectors, the balanced event-window view and the continuous, threshold-fixed view describe different detectors. Benchmark-chosen thresholds imply false-alarm burdens of 6.7–16.7 alarms per turbine-year and 83–176 alarm days per substation-year. Curated normal periods attract a fifth to two-fifths of the alarms of ordinary operation, so benchmark precision is inflated beyond the base-rate effect. Out-of-sample thresholds bring benchmark rankings closer to deployment rankings in every seed and on both datasets. With current benchmark sizes, however, this ranking effect cannot be established under calibrated tests. Reporting recall at a false-alarm budget in continuous replay, with thresholds chosen out of sample and random normal windows as controls, would make benchmark results meaningful for operators.

# Figures

![**Fig. 1.** Kendall's τ between each protocol cell and the deployment-like ranking (CH), seed 0, with 95% cluster-bootstrap intervals. Orange: benchmark practice (ET). Hollow markers: PreDist leak-free point estimates (primary). The calibrated tests of Amendment A1 do not establish the EH − ET difference (Table 3).](figures/fig2_tau_by_cell.png)

![**Fig. 2.** Benchmark score (ET, event F0.5 with thresholds tuned on the evaluated events) against deployment-like recall (CH) for every detector, seed 0. The best benchmark detector is not the best deployed detector on either dataset.](figures/fig3_benchmark_vs_deployment.png)

![**Fig. 3.** Selection effect: the ratio of each detector's alarm-hit rate on curated normal events to its rate on 2,000 random normal windows, at its held-out B = 2 operating point. Values below 1 mean the curated normal periods are quieter than ordinary operation. PreDist leak-free.](figures/fig4_selection_effect.png)

![**Fig. 4.** One-sided p-values of the pre-registered percentile-bootstrap tests per seed (dashed line: 0.05). PreDist seeds use the legacy exclusion rule. Under the calibrated tests (Table 3) these effects are not confirmed.](figures/fig5_seed_robustness.png)

# Declarations

**Data availability.** PreDist (doi:10.5281/zenodo.19496480) and CARE to Compare (Zenodo record 14958989) are public. All code, pre-registrations, logs and result tables will be archived with a DOI on Zenodo upon acceptance [to be created by the authors].

**CRediT author statement.** [To be completed by the authors.]

**Declaration of competing interest.** [To be completed by the authors.]

**Declaration of generative AI and AI-assisted technologies in the writing process.** During the preparation of this work the authors used Anthropic Claude for code assistance, analysis and drafting. The authors reviewed and edited the content and take full responsibility for it. [Authors to confirm.]

**Funding.** [To be completed by the authors.]

# References

[1] Roelofs C.M., Bastidas E.G., Hugo T., Faulstich S., Cadenbach A., Enabling predictive maintenance in district heating substations: A labelled dataset and fault detection evaluation framework based on service data, Energy, 355 (2026) 141178. https://doi.org/10.1016/j.energy.2026.141178

[2] Gück C., Roelofs C.M.A., Faulstich S., CARE to Compare: A Real-World Benchmark Dataset for Early Fault Detection in Wind Turbine Data, Data, 9 (2024) 138. https://doi.org/10.3390/data9120138

[3] Kim S., Choi K., Choi H., Lee B., Yoon S., Towards a Rigorous Evaluation of Time-Series Anomaly Detection, Proceedings of the AAAI Conference on Artificial Intelligence, 36 (2022) 7194-7201. https://doi.org/10.1609/aaai.v36i7.20680

[4] Salem M., Ferrugem A., Low-False-Alarm Evaluation Changes the Ranking of Multisensor Anomaly Detectors, Spectrum, 27 (2026). https://doi.org/10.55972/spectrum.v27i1.439

[5] Cools A., Stassin S., Mahmoudi S., The Threshold Paradox: Why Calibrating on the Test Set Introduces Bias in Anomaly Detection, Proceedings of the 21st International Conference on Computer Vision Theory and Applications (2026) 475-482. https://doi.org/10.5220/0014392600004084

[6] Liu J., Chen J., Wang C., Chronologically calibrated PCA for wind-turbine SCADA health monitoring: a leakage-controlled CARE v6 benchmark, Copernicus GmbH (2026). https://doi.org/10.5194/wes-2026-145

[7] Song S.B., Reproducibility package for "Detection without discrimination: a blinded, pre-registered test of pre-fault signals in public wind-turbine SCADA data", Zenodo (2026), unreviewed (verified via DataCite). https://doi.org/10.5281/zenodo.23902231

[8] Haneef Z., Umar M., Saleem F., Ullah I., Aqeel K., Siddique M.F., Uncertainty-Calibrated Residual Conformal Monitoring of Wind Turbine SCADA Data for Cross-Asset Anomaly Detection Under Distribution Shift, Information, 17 (2026) 930. https://doi.org/10.3390/info17090930

[9] Vural B., Farm-Specific Anomaly Detection in Wind Turbine SCADA Data, 2026 11th International Conference on Computer Science and Engineering (UBMK) (2026) 1017-1022. https://doi.org/10.1109/ubmk71847.2026.11745258

[10] Axelsson S., The base-rate fallacy and the difficulty of intrusion detection, ACM Transactions on Information and System Security, 3 (2000) 186-205. https://doi.org/10.1145/357830.357849

[11] Saito T., Rehmsmeier M., The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets, PLOS ONE, 10 (2015) e0118432. https://doi.org/10.1371/journal.pone.0118432

[12] Leber D.D., Pibida L., False Alarm Testing for Radiation Detection Systems, National Institute of Standards and Technology (2020). https://doi.org/10.6028/nist.tn.2118

[13] Wu R., Keogh E., Current Time Series Anomaly Detection Benchmarks are Flawed and are Creating the Illusion of Progress, IEEE Transactions on Knowledge and Data Engineering (2021) 1-1. https://doi.org/10.1109/tkde.2021.3112126

[14] van Dreven J., Cheddad A., Ghazi A.N., Alawadi S., Koussa J.A., Vanhoudt D. et al., From lab to practice: Towards a substation-invariant self-supervised transformer for low-label fault detection in district heating, Energy and AI, 25 (2026) 100824. https://doi.org/10.1016/j.egyai.2026.100824

[15] Agrawal A., O'Sullivan A., Tail reliability of machine-learning probabilistic forecasts in the GB day-ahead electricity market, Energy and AI, 26 (2026) 100975. https://doi.org/10.1016/j.egyai.2026.100975

[16] Kim M., Lee J., Chun H.W., Shin E.S., Choi H., Kang D. et al., Cross-laboratory generalization failure in perovskite solar cell machine learning: A diagnostic protocol and evaluation threshold, Energy and AI, 25 (2026) 100856. https://doi.org/10.1016/j.egyai.2026.100856

[17] Derzsi K., Klingebiel J., Müller D., Concept drift detection in district heating: A characterization framework and detector-centric benchmark, Energy and AI, 25 (2026) 100788. https://doi.org/10.1016/j.egyai.2026.100788

[18] van Dreven J., Cheddad A., Ghazi A.N., Alawadi S., Al Koussa J., Vanhoudt D., HEAT: Hierarchical-constrained Encoder-Assisted Time series clustering for fault detection in district heating substations, Energy and AI, 21 (2025) 100548. https://doi.org/10.1016/j.egyai.2025.100548

[19] Roelofs C.M., Gück C., Faulstich S., Transfer learning applications for autoencoder-based anomaly detection in wind turbines, Energy and AI, 17 (2024) 100373. https://doi.org/10.1016/j.egyai.2024.100373

[20] Mukhtar A., Hadwiger M., Wotawa F., Schweiger G., Reproducibility of machine learning-based fault detection and diagnosis for HVAC systems in buildings: An empirical study, Energy and AI, 22 (2025) 100658. https://doi.org/10.1016/j.egyai.2025.100658

[21] Gadd H., Werner S., Fault detection in district heating substations, Applied Energy, 157 (2015) 51-59. https://doi.org/10.1016/j.apenergy.2015.07.061

[22] Lund H., Werner S., Wiltshire R., Svendsen S., Thorsen J.E., Hvelplund F. et al., 4th Generation District Heating (4GDH), Energy, 68 (2014) 1-11. https://doi.org/10.1016/j.energy.2014.02.089

[23] Werner S., International review of district heating and cooling, Energy, 137 (2017) 617-631. https://doi.org/10.1016/j.energy.2017.04.045

[24] Neumayer M., Stecher D., Grimm S., Maier A., Bücker D., Schmidt J., Fault and anomaly detection in district heating substations: A survey on methodology and data sets, Energy, 276 (2023) 127569. https://doi.org/10.1016/j.energy.2023.127569

[25] Wang J., Yang F., Chen T., Shah S.L., An Overview of Industrial Alarm Systems: Main Causes for Alarm Overloading, Research Status, and Open Problems, IEEE Transactions on Automation Science and Engineering, 13 (2016) 1045-1061. https://doi.org/10.1109/tase.2015.2464234

[26] Beebe D., Ferrer S., Logerot D., The Connection of peak alarm rates to plant incidents and what you can do to minimize, Process Safety Progress, 32 (2012) 72-77. https://doi.org/10.1002/prs.11539

[27] Månsson S., Johansson Kallioniemi P., Thern M., Van Oevelen T., Sernhed K., Faults in district heating customer installations and ways to approach them: Experiences from Swedish utilities, Energy, 180 (2019) 163-174. https://doi.org/10.1016/j.energy.2019.04.220

[28] Hermans C., Al Koussa J., Van Oevelen T., Vanhoudt D., Fault detection for district heating substations: Beyond three-sigma approaches, Smart Energy, 16 (2024) 100159. https://doi.org/10.1016/j.segy.2024.100159

[29] Liu F.T., Ting K.M., Zhou Z., Isolation Forest, 2008 Eighth IEEE International Conference on Data Mining (2008) 413-422. https://doi.org/10.1109/icdm.2008.17

[30] Lavin A., Ahmad S., Evaluating Real-Time Anomaly Detection Algorithms -- The Numenta Anomaly Benchmark, 2015 IEEE 14th International Conference on Machine Learning and Applications (ICMLA) (2015) 38-44. https://doi.org/10.1109/icmla.2015.141

[31] Field C.A., Welsh A.H., Bootstrapping Clustered Data, Journal of the Royal Statistical Society Series B: Statistical Methodology, 69 (2007) 369-390. https://doi.org/10.1111/j.1467-9868.2007.00593.x

[32] Tautz‐Weinert J., Watson S.J., Using SCADA data for wind turbine condition monitoring – a review, IET Renewable Power Generation, 11 (2016) 382-394. https://doi.org/10.1049/iet-rpg.2016.0248

[33] Gadd H., Werner S., Achieving low return temperatures from district heating substations, Applied Energy, 136 (2014) 59-67. https://doi.org/10.1016/j.apenergy.2014.09.022

[34] Efron B., Bootstrap Methods: Another Look at the Jackknife, The Annals of Statistics, 7 (1979) 1-26. https://doi.org/10.1214/aos/1176344552
