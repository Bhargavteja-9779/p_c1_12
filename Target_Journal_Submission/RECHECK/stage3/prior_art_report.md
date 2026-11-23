# Stage 3: hostile prior-art recheck (2026-11-23)

Output table: `novelty_map_v2.csv`. It has **135 distinct papers/records**: the 59 existing rows (E01-E59) and 76 new rows (N01-N76).
Raw API responses are in `raw/`. The per-query hit counts are in `raw/query_log.tsv`, and the abstracts used are in `raw/candidates.json`. Scripts are in `scripts/`.

## 1. Method and honesty notes
- Every new row comes from a record we retrieved through one of these sources: the OpenAlex `/works` search, OpenAlex `/works/doi:`, the Crossref `/works`, the arXiv export API, the Zenodo API, the DataCite API, GitHub search or Google Patents.
- `what_they_do` comes from the retrieved abstract only. We did not read full texts.
- 6 rows have closeness = NA because no abstract could be retrieved: E03, E09, E13, N04, N21 and N63.
- **DOI re-check.**
  - All 56 existing DOIs resolve. Crossref holds 52 of them and DataCite holds 4 (arXiv, Zenodo, Fraunhofer-Publica). Each title matches at a ratio of 1.00, so none of them has the earlier "doi_verified = no" status any more.
  - 3 existing rows have no DOI.
  - All new DOIs are verified in Crossref or DataCite. 6 new rows have no DOI and are identified by their OpenAlex ID.
- **OpenAlex hit counts** are relevance-search totals and include many weak matches. We screened only the top 15-25 results per query, sorted by relevance. The counts show the size of the search space, not the number of relevant papers.
- **Many rows are on the 2025-11 to 2026-11 window.** We did not try to check whether each record's content holds up beyond its abstract. Code-only Zenodo records stand in for papers that may not yet be published: N52 (threshold transfer), N31 (fleet NBM) and N24 (impact-weighted HVAC; DataCite resolves the version DOI 10.5281/zenodo.23736320, and Zenodo search returned the sibling version 23863311). Their row text marks this.

## 2. Sources and queries
| Source | Status | Queries (hit counts in `raw/query_log.tsv`) |
|---|---|---|
| OpenAlex search | reachable | 66 queries. 6 used a publication-date filter: 3 for >= 2025-11-01 on DH fault/anomaly/autoencoder, 2 for >= 2025-11-01 on AD evaluation/ranking, and 1 for >= 2026-03-01 on "district heating substation" |
| OpenAlex citation graph (`cites:`) | reachable | works citing the PreDist paper (6), its arXiv version (same 6), the Zenodo records 17522255 (2), 17522254 (0) and 19496480 (0), and CARE (64) |
| Crossref | reachable | 2 bibliographic queries for >= 2025-11-01, plus DOI lookups for all rows |
| arXiv API | reachable | 22 queries, 10 of them sorted by submission date, plus ID lookups |
| DataCite API | reachable | verification of arXiv, Zenodo and Fraunhofer DOIs |
| Zenodo API | reachable | 5 dataset queries, plus record lookups |
| GitHub search | reachable | 11 repository queries. Individual repository contents were blocked by session policy, so only names and descriptions were used |
| Google Patents (xhr endpoint) | reachable | 2 queries. This was keyword screening only and is not a systematic patent search |
| Web search | reachable | 3 queries. Nothing new beyond the PreDist preprint, the Zenodo page and the earlier DH papers |
| **Semantic Scholar API** | **unreachable** (HTTP 429 on 4 attempts over about 1 h) | none |
| **IEEE Xplore** | **unreachable** (418) | covered only through Crossref/OpenAlex metadata |
| **ACM Digital Library** | **unreachable** (403) | covered only through Crossref/OpenAlex metadata |
| **Google Scholar** | **unreachable** (403) | none |
| **ScienceDirect** | **unreachable** (403) | Elsevier abstracts were taken from OpenAlex. Some Elsevier records have no abstract there (E03, E13, N21, N63) |
| dblp | blocked by bot check | none |
| Scopus / Web of Science / JCR | not available (login) | none |

## 3. Ten closest papers (ranked)
| # | id | Paper | DOI / ID | Closeness |
|---|---|---|---|---|
| 1 | E11 | Enabling predictive maintenance in DH substations: labelled dataset and FD evaluation framework (Energy 2026) | 10.1016/j.energy.2026.141178 | 4 |
| 2 | E41 | Frühzeitige Fehlererkennung in Hausstationen: Erfahrungen aus dem Projekt PreDist (Fraunhofer talk 2026) | no DOI | 4 |
| 3 | N01 | Role of AI in improving the operation of DH systems in Finland (LUT thesis 2026, **uses PreDist**) | OpenAlex W7162615597; lutpub.lut.fi/handle/10024/172051 | 3 |
| 4 | E14 | From lab to practice: substation-invariant self-supervised transformer (Energy and AI 2026; **cites the PreDist Zenodo v1 record**) | 10.1016/j.egyai.2026.100824 | 3 (raised from 2) |
| 5 | N02 | Individualized drift detection in DH via persistence-based monitoring of model residuals (BuildSys 2026) | 10.1145/3744256.3812567 | 3 |
| 6 | E38 | Challenges in detection of heating curve misconfiguration (Smart Energy 2026; cites PreDist) | 10.1016/j.segy.2026.100256 | 3 |
| 7 | N52 | Threshold transfer and metric inflation in ICS anomaly detection (code record for a paper) | 10.5281/zenodo.23471990 | 3 |
| 8 | N53 | Low-false-alarm evaluation changes the ranking of multisensor anomaly detectors (2026) | 10.55972/spectrum.v27i1.439 | 3 |
| 9 | E12 | Towards automation of FDD for DH substations: three-layer hybrid (Energy 2026) | 10.1016/j.energy.2026.142993 | 3 |
| 10 | N30 | Uncertainty-calibrated residual conformal monitoring, cross-asset CARE v6 (Information 2026) | 10.3390/info17090930 | 3 |

Other papers at closeness 3 that did not make the top 10:
- E05, beyond three-sigma: 10.1016/j.segy.2024.100159
- E28, CARE v6 chronologically calibrated PCA: 10.5194/wes-2026-145
- N34, wind NBM x detector factorial: 10.1088/1742-6596/3224/6/062018
- N35, wind generalist vs knowledge-selected variables (the scope question): 10.3850/esrel2026061419_esrel26-p26195-cd
- N31, fleet NBM on unseen turbines with a frozen protocol (Zenodo code): 10.5281/zenodo.23932665
- E25 (CARE to Compare), E27, E29, E36, E39

## 4. Close calls
**CLOSE CALL 1: the PreDist paper (E11) and the PreDist talk (E41).** These are the same dataset and the same problem. Their AE (EnergyFaultDetector) is one of our 11 detectors.
- **What overlaps:**
  - a public benchmark of DH substation fault detectors on PreDist;
  - claims of "few false alarms" and "operationally meaningful evaluation";
  - a normal-event accuracy metric;
  - an eventwise F0.5 metric;
  - an earliness metric;
  - baselines on both manufacturers.
- **What does not overlap** (based on the abstract only, so full-text check required):
  - continuous scoring of every 10-min step;
  - false alarms per substation-year;
  - recall at fixed budgets of 1/2/4 FA per substation-year;
  - thresholds frozen on M1 and applied unchanged to M2, with a pre-registered lock;
  - the rank-transfer analysis;
  - the start-up artefact analysis;
  - the scope x representation x model-class factorial;
  - the protocol-vs-protocol comparison (balanced events vs continuous).

  These points become our contribution only if the full text of E11 does not already report per-substation-year alarm counts or cross-manufacturer threshold transfer.

**Near close call: the LUT thesis (N01).** It runs anomaly detection on PreDist with residual SPC charts and compares false alarms with a threshold method. It is a master thesis, and its abstract reports no labelled-fault recall at a fixed budget and no cross-manufacturer lock. It must be cited, and we must not claim to be "first to report false alarms on PreDist".

**Probable PreDist user: E14 (From lab to practice).** Its OpenAlex reference list contains the PreDist Zenodo v1 record (W7105749811). The abstract reports transfer that is "asymmetric across networks". This partly pre-empts "detectors do not transfer across domains" in DH, but across networks and for a supervised transformer rather than across manufacturers. This resolves the earlier UNVERIFIED flag towards "likely uses PreDist". The full text is still needed to confirm which PreDist subsets it uses.

**Other PreDist citers** found through the OpenAlex citation graph:
- arXiv 2610.01842: world-model benchmark; possibly uses PreDist as one of its datasets; not fault detection.
- 2610.05409: no PreDist use visible in the abstract.
- 10.1016/j.egyai.2026.100959: review.
- 10.1631/jzus.a2600093: review.
- E38 and E42.

None of them runs a continuous-monitoring alarm-budget benchmark.

**PreDist versus EnergyFaultDetector uses.** No paper in the 2025-11 to 2026-11 window runs a DH benchmark reporting false alarms per unit time. EnergyFaultDetector uses found in that window are all wind applications:
- N32: thesis applying it at an operator;
- N31: vendored as a scorer;
- GitHub `Selmakrgzz/SCADA_model`, which tests the framework.

## 5. External DH / building datasets with labelled faults
| Dataset | URL / DOI | Licence | Size | Labels |
|---|---|---|---|---|
| PreDist (ours) | 10.5281/zenodo.19496480 | CC-BY-4.0 | 267 MB zip; 93 substations, 2 manufacturers | fault reports, disturbances, normal events |
| LBNL building FDD datasets | 10.1038/s41597-023-02197-w | stated "open" in abstract; licence UNVERIFIED (not retrieved) | largest public HVAC faulted/fault-free set (simulation, lab, field) | fault type and severity per time series |
| AHU fault datasets for transfer learning (8 datasets) | 10.1038/s41597-025-06179-y | UNVERIFIED | 8 AHU datasets | faulted vs fault-free states |
| Real-world hospital AHU dataset | 10.5281/zenodo.23401404 | CC-BY-4.0 | 5 AHUs, about 280 MB xlsx | the abstract does not describe its labels (UNVERIFIED) |
| Industrial PID control-loop repository | 10.1021/acs.iecr.8b06354 (data online per abstract) | UNVERIFIED | industrial loops | verified loop faults (oscillation, stiction, etc.) |
| CARE to Compare (wind; analogue protocol) | 10.3390/data9120138; Zenodo 10.5281/zenodo.15846963 (cited in N31) | UNVERIFIED here | 36 turbines, 95 cases | anomaly events vs normal events |

**DH data without fault labels.** These are usable only for estimating false-alarm burden:
- **Serbian DH SCADA, Data in Brief:** 10.1016/j.dib.2025.111320. 5 substations, hourly, 2019-2024. Licence not retrieved.
- **Danish smart heat meters:** 3021 meters, 3 years hourly, CC-BY-4.0. Zenodo 10.5281/zenodo.6563114; paper 10.1038/s41597-022-01502-3.
- **IMOS-SWIL lab testbed:** 10.5281/zenodo.23127438. 29.9 h at 0.5 Hz, lab operating conditions only.
- **domOS Aalborg living lab:** 10.5281/zenodo.8289790. 147 homes, DH control and indoor climate. No licence in the Zenodo metadata.
- **Synthetic DH meter data:** 10.5281/zenodo.14936551. CC-BY-4.0, simulated.

The synthetic DH/DHC fault dataset paper (10.1016/j.energy.2023.128387) has no retrievable abstract, and data availability is UNVERIFIED.

**Conclusion:** we found no second public, field, labelled DH-substation fault dataset. The polito labelled dataset in E46 (Building Simulation 2023) and Leiria et al. may hold labels, but we found no open download, so this is UNVERIFIED. An external replication is therefore only possible on HVAC (LBNL) or wind (CARE), which are different domains.

## 6. Claims we can still make / claims we must drop
**Can still make** (no counter-example found in the sources searched, abstracts only):
1. This is the first continuous-monitoring evaluation on PreDist and on any DH substation benchmark that reports **false alarms per substation-year and recall at fixed alarm budgets**.
2. The first **pre-registered locked test with thresholds frozen on one manufacturer and applied to another** for DH fault detection.
3. Development rankings of DH fault detectors **do not transfer** across manufacturers. Similar non-transfer findings exist in other domains (N52, N53, N30, N56 mTSBench, N43 TSB-UAD), so we must present this as DH evidence for a known general phenomenon, not as a new phenomenon.
4. A **comfort-scoped / setpoint-relative versus all-signal** comparison on labelled DH data. The closest analogue is wind (N35, generalist vs specialist variables), so we must cite it.
5. Most hits in the held-out set are start-up artefacts (< 90 days). We found no prior report of this.
6. The dataset's balanced 50/50 event protocol overstates performance relative to continuous monitoring, **shown on PreDist**. Frame this as a domain instance of known prevalence and metric-inflation effects: base rate (N67, N68, N69), PA inflation (N40, N45), metric inflation under threshold transfer (N52).

**Must drop or soften:**
1. Do not say "first to consider false alarms on PreDist". E11 already measures normal-event accuracy and eventwise F0.5, and N01 reports false-alarm comparisons on PreDist.
2. Do not say "first to show anomaly-detector rankings change under low-false-alarm evaluation" or "rankings do not transfer" in general. N53, N54, N56, N61 and N52 cover this.
3. Do not say "first to show thresholds fail to transfer across sites/assets" in general. N52 (ICS plant releases), N30 (cross-turbine), N76 and N39 cover this. Restrict the claim to DH manufacturers.
4. Do not say "first cross-domain transfer study in DH fault detection". E14 already reports asymmetric transfer across DH networks, probably partly on PreDist.
5. Do not say "first factorial study of representation x detector". N34 does this in wind. Our claim is the scope x representation x model-class factorial in DH.
6. Do not call the seasonal regime-change mechanism new. E05, E50, N27 and N37 cover it. Present it as an empirical attribution on labelled DH faults.
7. Do not say "first DH study with own-history residual monitoring and persistence". N02 (182 DH meters) and E12 already do this.
8. Do not call the pre-registration or locked-test idea new in condition monitoring. E28 and N31 use a frozen protocol on CARE. Claim it for DH only.

**Must verify in full text before submission:**
- whether E11 reports alarm counts per substation or per year, or a cross-manufacturer threshold transfer;
- which datasets E14 and arXiv 2610.01842 take from PreDist;
- the content of the Fraunhofer record W7153690826 ("physics-informed ML anomaly detection of DH substations", no abstract, same institute as PreDist).
