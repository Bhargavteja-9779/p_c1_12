# Fresh public test datasets for early fault / anomaly detection on energy assets

Compiled 2026-11-24. Sources: Zenodo REST API (record metadata and file lists), figshare API,
OpenAlex, raw GitHub READMEs. Nothing larger than 50 MB was downloaded; only small README /
metadata files were read. Excluded by brief: PreDist (Zenodo 19496480), CARE to Compare
(Zenodo 14958989 / 15846963 / 10958774).

Legend: VERIFIED = read on the record page or API; UNVERIFIED = not confirmed from a primary
page (stated from the record text only, or the site was unreachable).

## Ranking (top 3 by fit: real faults, wind / DH / HVAC, size)

1. **Hill of Towie wind farm open dataset** (Zenodo 22662930, v2.1.0). 21 turbines x about 10 years, 10-min SCADA,
   alarm log with Siemens alarm codes, plus shutdown durations from RES operator logs. CC BY 4.0. Year
   zips are 0.55 to 1.6 GB each, about 14.9 GB for 2016-2026 without fastlog/LiDAR. It has the most
   asset-years of any candidate (about 215), so false alarms per asset-year come out tight. Caveat: the
   labels are alarm codes, not confirmed component failures.
2. **Fuhrländer FL2500** (figshare 10.6084/m9.figshare.25201631; GitHub alecuba16/fuhrlander;
   Sci Data 2024, doi:10.1038/s41597-024-03067-9). 5 turbines x 3 years, 5-min, 312 variables, alarm events
   with system/subsystem. 353 MB. A different OEM, era and country from CARE, and it is small.
   Caveat: only about 15 asset-years.
3. **Kelmarsh (6 turbines) + Penmanshiel (14 turbines)** (Zenodo 16807551 / 16807304). 10-min SCADA
   and status/event logs for 2016-2024, CC BY 4.0, 3.8 GB + 7.5 GB. About 170 asset-years. Caveat: the
   events are Greenbyte status codes with no maintenance log, so failure events have to be derived.

No candidate fully meets requirement (2) with maintenance-confirmed failures. PreDist and CARE are the
only public sets we found with logbook-confirmed failures. All three picks above are "alarm/status-log"
labels and need a documented, pre-registered rule to turn alarms into fault events
(e.g. stopping alarms of component subsystems, excluding weather/grid/curtailment codes).

## Candidate table

| # | Dataset | URL / DOI | Domain | Assets | Years | Res. | Labels | Normal volume | Licence | Size | Access | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Hill of Towie open dataset v2.1.0 | https://zenodo.org/records/22662930 (doi:10.5281/zenodo.22662930; v1 = 14870023) | Wind (Siemens SWT-2.3-VS-82, Scotland) | 21 | 2016-01 to 2026-04 | 10 min (+ ~1 Hz fastlog Jan-Apr 2026) | `tblAlarmLog` (stopping and non-stopping events with `Alarmcode`); `Hill_of_Towie_alarms_description.csv` maps only 12 selected codes (icing, high wind, pitch lubrication, cable untwist, ...); `ShutdownDuration.zip` = per-10-min downtime from SCADA + RES operator logs (v1 window, to 2024-08). Number of genuine component faults: UNVERIFIED (needs alarm log analysis) | about 215 turbine-years | CC BY 4.0 (VERIFIED) | about 29.7 GB in total; the 10-min year zips alone are about 14.9 GB (fastlog 11.9 GB and LiDAR 2.4 GB can be skipped) | Direct Zenodo download, no login (VERIFIED) | PARTIAL, best fit: real multi-asset alarm logs, but no maintenance/failure log, so fault labels must be derived from alarm codes |
| 2 | Fuhrländer FL2500 2.5 MW | https://doi.org/10.6084/m9.figshare.25201631 ; https://github.com/alecuba16/fuhrlander ; paper doi:10.1038/s41597-024-03067-9 | Wind (Spain, per literature; UNVERIFIED) | 5 (IDs 80-84) | 2012-2014 | 5 min, min/max/mean/std of 78 sensors (312 vars) | Alarm events with system, subsystem and description (VERIFIED from README / abstract). Number of failure-type alarms: UNVERIFIED | about 15 turbine-years | figshare: MIT; GitHub: EPL-2.0 (both VERIFIED; they differ) | 353 MB zip (figshare, VERIFIED) | Direct figshare download (ndownloader), no login | USABLE / PARTIAL: real alarm logs, small and easy, but few asset-years for FA/asset-year and the labels are alarms, not a failure log |
| 3 | Kelmarsh wind farm data (Cubico) | https://zenodo.org/records/16807551 | Wind (6 Senvion MM92, UK) | 6 | 2016-2024 | 10 min | "SCADA and events data" from Greenbyte (status/event files with stop/warning codes; exact schema UNVERIFIED, zips not opened because over 50 MB) | about 50 turbine-years | CC BY 4.0 (VERIFIED) | 3.84 GB (VERIFIED) | Direct Zenodo, no login | PARTIAL: status codes only, no maintenance log. Known structural defects are documented in Zenodo 23196733 / 23171808 (2023-2024 files) |
| 4 | Penmanshiel wind farm data (Cubico) | https://zenodo.org/records/16807304 | Wind (14 Senvion MM82, UK; no WT03) | 14 | 2016-2024 | 10 min | Same type as Kelmarsh (status/events) | about 120 turbine-years | CC BY 4.0 (VERIFIED) | 7.49 GB (VERIFIED) | Direct Zenodo, no login | PARTIAL (same reason as Kelmarsh) |
| 5 | Six-Month Monitoring Dataset, 10-turbine onshore wind farm, Greece (UNDERPIN; IEEE Data Descriptions 2025, doi:10.1109/ieeedata.2025.3574640) | https://zenodo.org/records/14546480 | Wind | 10 | 2020-01 to 2020-06 | SCADA (resolution UNVERIFIED) | Alarm and event logs (VERIFIED from description) | about 5 turbine-years | CC BY 4.0 | 181 MB (single xlsx) | Direct Zenodo | PARTIAL: real alarm logs, but only 6 months, so the FA/asset-year estimate is weak. Good as a small secondary test |
| 6 | CSIRO AHU fault-generation dataset | https://github.com/csiro-energy-systems/ahu-fault-detection-dataset | HVAC (2 AHUs, Newcastle, AU office) | 2 | Apr-Nov 2013 | BMS trend (UNVERIFIED) | 8 fault types imposed via BMS proxy points on real AHUs (duct leak, belt slip, stuck valves/dampers, sensor offset/failure) | under 1 asset-year | Data CC BY-SA 4.0 | git-LFS (size UNVERIFIED) | GitHub + git-lfs | NOT USABLE: under 5 assets, and the faults are deliberately injected |
| 7 | Hospital AHU dataset ("A Real-World HVAC Dataset ...") | https://zenodo.org/records/23401404 | HVAC (hospital AHUs) | 5 AHU files | UNVERIFIED | UNVERIFIED | Fault labels not stated in the record (UNVERIFIED) | UNVERIFIED | CC BY 4.0 | 282 MB (5 xlsx) | Direct Zenodo | PARTIAL / UNVERIFIED: 5 real AHUs, but label presence is unconfirmed; inspect before use |
| 8 | LBNL FDD datasets | https://data.openei.org/submissions/5763 (doi:10.25984/1881324); Sci Data doi:10.1038/s41597-023-02197-w | HVAC (AHU, RTU, VAV, FCU, chiller ...) | many (mostly simulated) | 1-year simulations per fault | 1 min typical (UNVERIFIED) | Fault type and severity labels; mostly simulation, plus lab and some in-situ experiments with imposed faults | Fault-free simulated year per configuration | OEDI open (licence UNVERIFIED) | UNVERIFIED | OEDI direct | NOT USABLE as a "real-fault" test: simulated or imposed faults, not naturally occurring failures |
| 9 | ASHRAE RP-1312 (AHU) / RP-1043 (chiller) | Distributed inside the LBNL FDD collection / ASHRAE | HVAC lab | 1 AHU pair / 1 chiller | 2007-ish / 1999-ish | 1 min / ~10 s | Imposed faults in a lab | Small | UNVERIFIED | small | via OEDI | NOT USABLE: single lab rig with imposed faults |
| 10 | EDP Open Data (wind failures) | https://www.edp.com/en/innovation/open-data/data now redirects to 404; opendata.edp.com unreachable (proxy 502) | Wind (5 turbines) | 5 | 2016-2017 | 10 min | Failure logbook | - | Platform terms (registration was historically required; UNVERIFIED) | - | Not reachable | NOT USABLE: unreachable, and it is the source of CARE Wind Farm A (overlap with data already used) |
| 11 | La Haute Borne (ENGIE) | opendata-renewables.engie.com (unreachable, proxy 502) | Wind | 4 | 2013-2020 (UNVERIFIED) | 10 min | No fault labels known | - | Etalab open licence (UNVERIFIED) | - | Not reachable | NOT USABLE: under 5 assets, no labels, site unreachable |
| 12 | SKAB | https://github.com/waico/SKAB (Kaggle doi:10.34740/kaggle/dsv/1693952) | Industrial water-circulation lab testbed | 1 rig, 34-35 experiments | short runs | 1 s | Annotated anomalies (induced) | Minutes to hours | GPL-3.0 | about 34 MB repo | GitHub direct | NOT USABLE: one lab rig, induced anomalies, no asset-years |
| 13 | DHDrift | https://zenodo.org/records/18128257 | District heating loads | 901 simulated series | 2020-2023 | 1 h | Synthetic concept-drift timings | - | CC BY 4.0 | 568 MB | Zenodo | NOT USABLE: synthetic, and drift rather than faults |
| 14 | Energy storage Li-ion real operation | https://zenodo.org/records/18471156 | BESS | multi-cell | UNVERIFIED | UNVERIFIED | No fault labels stated | - | CC BY 4.0 | 19 MB | Zenodo | NOT USABLE: no labels |
| 15 | scada-fault-bench / scada-schema (2026) | https://doi.org/10.5281/zenodo.24164281 ; 10.5281/zenodo.24004701 | Wind + PV | uses Kelmarsh, Penmanshiel, HoT, PVDAQ | - | - | Synthetic injected faults on open data; real labels only from CARE | - | MIT (code) | 4 MB | Zenodo | NOT USABLE as data (no new labels). Useful loaders for #1, #3, #4 |
| 16 | NREL PVDAQ / BR-PVGen (Zenodo 23739670) / Zenodo 17775544 PV inverter | various | PV | many | multi-year | 1-15 min | No timestamped fault/failure labels found | large | open | various | direct | NOT USABLE: no real fault labels. No public multi-inverter PV dataset with real failure logs was found |
| 17 | Kaggle "wind turbine SCADA alarms" sets | kaggle.com | Wind | - | - | - | - | - | - | - | Kaggle API returned 404 without credentials | UNVERIFIED: not checked (needs login); provenance of most Kaggle copies is unclear |
| 18 | Danish/Swedish open DH substation data with fault labels | - | DH | - | - | - | - | - | - | - | - | NOT FOUND: Zenodo searches found only PreDist (excluded), synthetic meter data (14936551) and DHDrift |

## Notes on related 2026 work using these sets

- Zenodo 23902232 (2026, "Detection without discrimination ...") already runs a blinded test on
  CARE, Kelmarsh/Penmanshiel, Hill of Towie and Fuhrländer. Raw data are not redistributed. Our use of
  these datasets is therefore not novel, and we should cite that work and compare with it.
- Zenodo 23646100 gives cleaned 10-min data for Kelmarsh, Penmanshiel and EDP 2016. Logged stops are removed, so it has no labels.
- Zenodo 23196733 / 23171808 document structural defects in the Kelmarsh 2023-2024 files. Check them before use.

## Practical recommendation

Use Hill of Towie as the primary fresh test set. Pre-register the rule that maps alarms to faults
(stopping alarms on component subsystems, excluding weather, grid and curtailment codes) before
looking at detector outputs. Report it as "alarm-derived events" and do not call them failures. Add
Fuhrländer as a second OEM. Use Kelmarsh/Penmanshiel mainly to estimate false alarms per asset-year
on long normal operation.
