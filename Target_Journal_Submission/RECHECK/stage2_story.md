# Stage 2: problem story (re-checked)

## Is the problem real? Who, where, what cost (each with a verified source)
| Element | Statement | Evidence (verified DOI, Crossref) |
|---|---|---|
| WHO | District-heating (DH) utility operators and maintenance staff who monitor fleets of customer substations remotely | Neumayer et al. 2023, 10.1016/j.energy.2023.127569 (survey: early detection is crucial; labelled data lacking) |
| SETTING | Hundreds of substations, 10-min controller data, faults reported by customers (PreDist: 93 substations, 2 controller manufacturers, 73 faults) | PreDist dataset paper, arXiv 2511.14791 / 10.1016/j.energy.2026.141178; Zenodo 19496480 |
| HOW COMMON | Faults found in 74% of 135 Swedish substations by threshold methods on meter data | Gadd & Werner 2015, 10.1016/j.apenergy.2015.07.061 |
| HARM 1 (energy/cost) | Substation faults raise return temperatures; low temperatures need fault-free substations; high temperatures raise heat supply cost and block renewable/excess heat | Gadd & Werner 2014, 10.1016/j.apenergy.2014.09.022; Averfalk & Werner 2020, 10.1016/j.energy.2019.116727 |
| HARM 2 (people) | Faults are typically found only when the customer complains (cold home / no hot water) | PreDist paper (faults = customer reports; goal "detect before the customer reports") |
| HARM 3 (operators) | Too many alarms overload operators; alarm floods are a known failure of alarm systems | Wang et al. 2016, 10.1109/TASE.2015.2464234; Beebe et al. 2013, 10.1002/prs.11539 |
| NOT AVAILABLE | A verified monetary cost per site visit or per missed fault for DH | None found -> decision-level results are expressed as alarms per true detection and alarm-weeks per substation-year, not money |

## Why current methods fail (to be fair to them)
Published DH detectors (autoencoder normal-behaviour models, hybrid rule/ML systems) are evaluated on balanced
sets of fault windows and hand-picked normal weeks, or on case studies. The PreDist authors themselves note that the
balanced protocol overestimates reliability. Such protocols do not give (i) alarms per substation-year in continuous
operation, (ii) a test on substations of another controller manufacturer with thresholds frozen in advance, or
(iii) a comparison with random alarms at the same alarm rate. Without these, an operator cannot tell how many site
visits a detector will cause, or whether it will work on the next fleet.

## One-paragraph story (evidence-backed; numbers filled from result files)
District-heating operators who supervise hundreds of customer substations struggle to find faults before the
customer reports a cold home. Faults are common and they raise network temperatures, which costs energy and blocks
low-temperature heat sources, while operators can follow up only a few alarms per substation each year.
Current fault detectors are scored on balanced sets of fault weeks and hand-picked normal weeks, so their
reported precision says little about the alarm load in daily operation or about a new fleet. We score eleven
detectors on every 10-minute step of 93 substations, fix all thresholds on one controller manufacturer and test them
once, as pre-registered, on the other. On the new manufacturer the best detector catches 7 of 25 faults at under
four false alarms per substation-year, and only 3 of 33 detector settings beat random alarms raised at the same rate.
We show why (start-up artefacts, seasonal false alarms, rankings that do not transfer) and give a simple rule for how
many normal weeks a benchmark needs before it can certify an alarm budget.
[protocol-gap sentence to be added only if H-E1 is supported]

Sources of numbers: 7/25 -> code/results/locked_m2_operating_points.csv (sigma3, budget 2 and 4);
3/33 -> code/results/chance_level.csv; rule for normal weeks -> code/results/protocol_gap_t1.csv (analytic).

## First-page check
No manuscript existed after the first run (only section 03 draft). The title, abstract and introduction will be
written in Stage 7 from this paragraph. Check after Stage 7: title + abstract + first intro paragraph must contain
WHO (DH operators), WHAT (fault detection before customer report), HARM (energy + alarm load), FAILURE (balanced
protocols, no cross-manufacturer test), IDEA (continuous, budgeted, locked cross-manufacturer benchmark with a
random-alarm reference), RESULT (7/25; 3/33; certification rule).
