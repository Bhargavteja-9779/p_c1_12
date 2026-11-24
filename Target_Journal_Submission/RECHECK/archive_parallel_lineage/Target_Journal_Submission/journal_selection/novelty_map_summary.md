# Novelty map summary (SRCR on PreDist)

Source: `novelty_map.csv` (47 rows). Every field comes only from the abstracts in `novelty_candidates.csv` and `lit_raw.csv`, or from abstracts returned by the OpenAlex API (searched 2026-11-23). Full texts were not read; ScienceDirect is blocked. Anything not stated in an abstract is marked UNVERIFIED. Rows are cited by DOI.

Searches run (OpenAlex `search=`, page 1, 8 results each, plus `cites:` filters):
- conformal anomaly/false-alarm thresholds in condition monitoring
- fleet or population normal-behaviour models (wind, HVAC)
- setpoint-tracking residuals in HVAC and district heating (DH)
- works citing the PreDist paper (10.1016/j.energy.2026.141178) and the PreDist dataset (10.5281/zenodo.17522254)

I also ran one arXiv API query ("district heating" AND conformal/setpoint/PreDist). It returned nothing relevant.

## (a) The five closest papers

1. **PreDist benchmark, Energy 2026 (10.1016/j.energy.2026.141178).** It uses the same data and the same report-date labels with autoencoder normal-behaviour models scored on event windows. We differ in the residual target (measurement minus controller setpoint), in using a fleet zero-shot quantile model, and in a continuous protocol that counts false alarms per substation-year.
2. **Three-layer hybrid DH FDD, Energy 2026 (10.1016/j.energy.2026.142993).** This is the closest DH method. It combines regression residuals with mode rules "derived from the substation control strategy" and reports false-alarm rates and lead time before the customer report. Its models are built per substation and it reports two case studies. Whether it computes residuals against setpoints is UNVERIFIED, because the full text is blocked and must be checked.
3. **Fleet-wide residual model generation, Wind Energy 2025 (10.1002/we.70050).** It builds fleet-valid residual normal-behaviour models and tests them on unseen farms and manufacturers, which is our "fleet model, zero-shot" idea in wind. It does not use control setpoints, an alarm budget or DH data.
4. **Beyond three-sigma, Smart Energy 2024 (10.1016/j.segy.2024.100159).** It already uses conditional quantile-regression thresholds for DH substation residuals. Our difference is the residual definition (setpoint-relative), fleet training and labelled field evaluation, not the quantile idea itself.
5. **Shared nominal representation plus local radius calibration, CU Boulder 2026 (no DOI).** It shares one model across the fleet and calibrates a per-asset residual quantile, which mirrors our fleet-prior to local-calibration idea, but on bearings. We add empirical-Bayes shrinkage, setpoint residuals and DH field validation.

Close runners-up:
- Temporal conformal prediction for wind turbines (10.1088/1742-6596/3224/6/062054): turbine clustering plus conformal alert intervals on 40+ turbines.
- Chronologically calibrated conformal PCA on CARE (10.5194/wes-2026-145): identity-disjoint split with a conformal threshold.
- Heating-curve misconfiguration study (10.1016/j.segy.2026.100256): it cites PreDist and reports that per-substation conditional autoencoders overfit and miss gradual faults, which motivates our approach.

## (b) Novelty types

| Type | Can we claim it? | Evidence |
|---|---|---|
| N1 formulation | **Yes, core idea (to the best of our knowledge, based on this OpenAlex/arXiv search).** The monitoring target is the controller-setpoint tracking residual for each loop, gated by loop activity and kept one-sided for comfort shortfall. No DH abstract found does this. | Nearest: 10.1016/j.energy.2026.142993 (mode rules; residual target UNVERIFIED); 10.1016/j.apenergy.2019.114059 (mentions setpoints only as operating conditions) |
| N2 method | **Partial.** Already done: fleet or shared normal-behaviour models (10.1002/we.70050, 10.1016/j.egyai.2024.100373, CU Boulder row), conditional quantile thresholds (10.1016/j.segy.2024.100159, 10.1002/we.2375), and local recalibration of a shared model. Not found: the combination of zero-shot cross-fitted fleet quantiles, setpoint residuals and empirical-Bayes fleet-to-local shrinkage. | Claim it only as a combination with an ablation. |
| N3 theory | **No.** The split-conformal false-alarm guarantee is standard and already applied to alarms in 10.1080/09540091.2026.2707826, the ESREL conformal autoencoder, 10.48550/arxiv.2604.20122 and 10.48550/arxiv.2610.17962. | Do not claim. |
| N4 data/benchmark | **No.** The dataset belongs to 10.1016/j.energy.2026.141178. | Our continuous protocol could be released as a benchmark extension (N5), not N4. |
| N5 evaluation protocol | **Yes for DH, second claimable type.** Every 10-minute step is scored, false alarms are counted per substation-year, and recall is measured within 7 days before the report at a fixed false-alarm budget. Event-window protocols (PreDist, CARE 10.3390/data9120138) differ. | Analogues exist in other domains: identity-disjoint calibration (10.5194/wes-2026-145), matched false-alarm rate (10.21203/rs.3.rs-11370528/v1), duty cycle (10.48550/arxiv.2610.17962). Present ours as an adaptation, not a new concept. |
| N6 real-world validation | **Partial.** The data are real field data with service reports, but this is retrospective with no deployment. | Same level as PreDist. |
| N7 finding | **Pending.** It depends on experiments, for example whether the event-window benchmark overstates performance under continuous monitoring. | Cannot claim until result files exist. |

## (c) Direct threats to novelty

- **No paper found does setpoint-relative residuals scored by a fleet model in district heating.** Searches: OpenAlex queries on setpoint tracking residuals in HVAC/DH, DH controller setpoint deviation, and DHW setpoint fault detection; OpenAlex citing-works of PreDist; one arXiv query.
- **No paper found uses conformal or false-alarm-budget thresholds in district heating.** The query "district heating fault detection conformal" returned no conformal DH work.
- **CAUTION 1: 10.1016/j.energy.2026.142993 has not been checked against its full text.** Its "mode-based rules derived from the substation control strategy" could involve setpoint comparisons. It is per-substation and uses no fleet model or conformal step, but the full text must be read (Elsevier is blocked here; try an author preprint) before claiming N1.
- **CAUTION 2: fleet models plus conformal alerts already exist in wind turbines (10.1088/1742-6596/3224/6/062054).** "Fleet + conformal" must therefore not be claimed as new in general, only as new for DH control loops.
- **CAUTION 3: 10.1016/j.enbuild.2024.114009 (LSTM with adaptive threshold selection for DH sensors) has no abstract available.** It is UNVERIFIED and should be checked.
- Two 2026 works cite PreDist: 10.1016/j.segy.2026.100256 and 10.48550/arxiv.2611.04682. Neither uses setpoint residuals or false-alarm budgets, according to their abstracts.
