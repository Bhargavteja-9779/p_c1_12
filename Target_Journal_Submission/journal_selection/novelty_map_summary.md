# Novelty map summary (2026-11-23)

Source: `novelty_map.csv`, 59 rows. 37 input candidates plus 22 papers added from OpenAlex search, each with an abstract we actually retrieved.
- 56 rows have an abstract. 3 input candidates have no abstract in the input, Crossref or OpenAlex (10.1016/j.apenergy.2017.08.035, 10.1007/978-3-031-74738-0_23, 10.1016/j.enbuild.2024.114009). They are kept with closeness = NA and are not assessed.
- Closeness distribution: 4 (2 rows), 3 (9), 2 (28), 1 (17), NA (3). 39 rows are DH/HVAC/condition-monitoring work at closeness 2 or higher.
- doi_verified = yes for 51 rows: the Crossref /works/<doi> lookup returned a matching title. It is "no" for 8 rows: 3 have no DOI, and 5 have DataCite DOIs (arXiv, Zenodo, Fraunhofer-Publica) that Crossref returns as 404, or no DOI at all (the PreDist talk).
- All fields come from abstracts only. Full texts were not read because ScienceDirect is blocked. "What they don't do" therefore means "not reported in the abstract".

## Five closest papers
1. **Enabling predictive maintenance in DH substations: labelled dataset and FD evaluation framework** (Energy 2026, 10.1016/j.energy.2026.141178), closeness 4. Same dataset (PreDist: 93 substations, 2 manufacturers), and its autoencoder (EnergyFaultDetector) is our benchmark. Its evaluation uses fault events vs predefined normal events (normal-behaviour accuracy, eventwise F0.5, earliness). Its abstract explicitly claims "few false alarms" and "operationally meaningful evaluation". The companion PreDist talk (Fraunhofer-Publica 2026, no DOI) repeats these results.
2. **Challenges in detection of heating curve misconfiguration: an empirical study** (Smart Energy 2026, 10.1016/j.segy.2026.100256), closeness 3. A conditional-autoencoder normal-behaviour model is evaluated against customer reports of insufficient heat. It catches abrupt hardware faults but treats gradual heating-curve drift as normal. This is close to our comfort and mechanism story. The abstract does not name the dataset. A related Fraunhofer thesis is 10.24406/publica-9049.
3. **Towards automation of FDD for DH substations: a three-layer hybrid approach** (Energy 2026, 10.1016/j.energy.2026.142993), closeness 3. It combines ML regression residuals, mode-based rules derived from the substation control strategy, and boundary thresholds. It reports false alarm rates of 0.27% and 0.01% in two case studies. This is the nearest to our "expert rule relative to the controller" class.
4. **Fault detection for DH substations: beyond three-sigma approaches** (Smart Energy 2024, 10.1016/j.segy.2024.100159), closeness 3. It shows that field residuals are seasonal and not Gaussian, and it proposes quantile-regression thresholds. This overlaps our seasonal-regime mechanism and our quantile-ML model class.
5. **Chronologically calibrated PCA for wind-turbine SCADA: a leakage-controlled CARE v6 benchmark** (WES Discussions 2026, 10.5194/wes-2026-145), closeness 3. It uses an identity-disjoint locked test set and reports false-positive-event burden. This is the nearest protocol analogue, but in wind. Other close wind papers are the persistence-based alarm confirmation paper (10.3390/s26123896), the CARE to Compare paper (10.3390/data9120138) and the drift-aware assurance paper (10.21203/rs.3.rs-10269372/v1).

## Has anyone already done our contribution?
Based on our search of Crossref/OpenAlex on 2026-11-23 with the queries listed below, using abstracts only:
- **Continuous-monitoring evaluation with false alarms per substation-year on DH:** no paper found. DH studies report the following instead:
  - event-based scores (PreDist paper);
  - case-study false-alarm *rates* (three-layer hybrid);
  - substation-level sensitivity and specificity (HEAT, SHEDAD);
  - ranking or average precision (power-signature ranking, changepoint score, arXiv 2611.04682);
  - post-hoc filtering of too many detections (Chernoff anomaly indexing, 10.1016/j.applthermaleng.2023.120964).
- **Comfort-scoped / setpoint-relative monitoring compared with autoencoders:** no paper found that makes this comparison. The heating-curve CAE paper and its thesis show that the AE *misses* comfort-relevant drift, but they do not test a setpoint-relative or comfort-scoped alternative. They also do not measure false alarms per substation-year.
- **Factorial scope x representation x model class:** no paper found. Single-factor relatives exist:
  - persistence and decision rule (wind, 10.3390/s26123896);
  - multi-turbine residual representation (10.3390/en15082806);
  - rule-filtered residuals (HVAC, 10.12688/openreseurope.19029.1).
- **AE false alarms tied to regime changes:** the idea is partly prior work.
  - Seasonal non-i.i.d. residuals: 10.1016/j.segy.2024.100159.
  - Change points breaking normal-behaviour models: 10.5194/wes-5-1375-2020.
  - Detectors reacting to operational variability: 10.3390/s26123896.

## Risks to our novelty claims
1. **Do not claim to be "first to consider false alarms" on PreDist.** The PreDist paper already uses an eventwise F-score aimed at few false alarms, plus normal-event accuracy. Our claim must be narrower: we score every 10-min step of every substation, report false alarms per substation-year and recall at a fixed budget, and use a cross-manufacturer locked test.
2. **The heating-curve CAE paper (2026) overlaps our mechanism narrative.** It finds that the AE treats comfort-relevant drift as normal. We should cite it and stress the difference: it reports AE misses, while we report AE false alarms and test the scoped/setpoint-relative alternative. Check whether it uses PreDist data; the abstract does not say.
3. **The seasonal mechanism is not new on its own** (beyond-three-sigma, wind change-point work). Frame our mechanism as an empirical attribution on labelled DH data, set against comfort alarms that coincide with real setpoint shortfalls.
4. **Locked tests and alarm-burden accounting already exist in wind** (CARE-based papers 2024-2026). Claim protocol novelty "for DH substations" only.
5. **The three-layer hybrid already uses control-strategy rules** with low false-alarm rates. Our rule class is not new on its own. The novelty is the controlled factorial and the public benchmark.
6. **Unverified:**
   - whether "From lab to practice" (10.1016/j.egyai.2026.100824) uses PreDist (it surfaced in an "enercity" query); [session 3: its OpenAlex reference list cites neither the PreDist paper nor the Zenodo record; still UNVERIFIED because it surfaced for "enercity" — treat as possible PreDist user and cite it as such only if confirmed]
   - the 3 papers without abstracts, including the 2024 Energy and Buildings LSTM adaptive-threshold sensor FDD paper, which may discuss false alarms.
   Check these full texts before submission.

## Queries used (OpenAlex /works?search=..., per_page=25; DOI lookups on Crossref /works/<doi>)
"district heating substation fault detection"; "false alarm rate fault detection HVAC evaluation"; "alarm fatigue fault detection buildings"; "normal behaviour model autoencoder false alarms"; "setpoint tracking control loop performance monitoring fault detection"; "fleet transfer learning fault detection buildings"; "PreDist district heating dataset"; "district heating fault detection false alarms";
"district heating autoencoder anomaly detection substations"; "automated fault detection diagnostics false positives field evaluation buildings"; "space heating control loop fault detection setpoint deviation"; "district heating anomaly detection seasonal concept drift"; "EnergyFaultDetector autoencoder district heating"; "district heating insufficient heat customer complaint detection"; "district heating substation secondary side supply temperature setpoint deviation fault"; "heating curve district heating substation anomaly detection autoencoder";
"fault detection evaluation false alarms per year operational deployment"; "district heating substation continuous monitoring evaluation false positive rate"; "wind turbine normal behaviour model false alarm seasonal"; "building HVAC fault detection comfort setpoint deviation rule-based residual"; "PreDist"; "enercity district heating substations"; "comfort control loop monitoring district heating substation"; "false alarms per year fault detection substation".
