# Prior-art check: negative-sample selection effect (curated normal events vs ordinary operation)

Date: 2026-11-24. Searches: 45 queries (30 OpenAlex, 6 Crossref, 9 arXiv), plus every work citing CARE (64) and PreDist (6) in OpenAlex screened by title. Details are in `prior_art_selection_effect.json`.

## Verdict: new for energy and early fault detection; not new as a concept

- **The concept is established.** Medicine calls it spectrum bias, or the case-control (healthy-controls) design bias, in diagnostic-accuracy studies. Ransohoff & Feinstein 1978 named it. Lijmer et al. 1999 measured it: RDOR 3.0 (95% CI 2.0-4.5) for a diseased group against separate controls. Rutjes et al. 2006 found RDOR 4.9 for severe cases with healthy controls, with a wide CI. In ML, Ben-Hur & Noble 2006 showed that constrained negatives "make the task easier" and bias accuracy upward.
- **Nobody has measured it in energy.** No paper was found that compares false-alarm rates on curated normal events with random ordinary-operation windows from the same assets. This holds for wind, district heating (DH), PV and buildings.

## Closest prior work

1. **PreDist (10.1016/j.energy.2026.141178, arXiv 2511.14791v2). This is the closest work.**
   - It describes its normal events as pre-defined, "selected across all seasons" and "free from maintenance tasks and faults".
   - Limitation 2 says normal events "could be refined to better represent all stable operating regimes across seasons and control modes". It suggests evaluating "on randomly selected events" as future work.
   - It does not run that check or quantify any gap. It also does not say in which direction the bias goes.
2. **CARE (10.3390/data9120138).**
   - Normal labels were "determined by a combination of feedback of the wind farm operators, manual inspection of the data, and expert knowledge".
   - The paper does not discuss whether these events are representative.
   - It reports 51 normal datasets, but Zenodo v6 has 50. Fix this in our text.

## The difference, in one sentence

PreDist proposes random normal events as future work and the medical literature shows that selected controls inflate specificity; we are the first to measure, with the same detectors and thresholds, that curated normal events in public energy early-fault-detection benchmarks draw far fewer alarms than random ordinary-operation windows from the same assets (16% vs 37%; rate ratio 0.30-0.61, bootstrap CIs below 1).

## Recommended wording

> "Beyond the 50/50 base rate, the benchmarks' negatives are themselves selected. CARE's normal events were chosen using operator feedback, manual inspection and expert knowledge, and PreDist's were chosen to be free of faults and maintenance. With the same detector and threshold, alarms hit 16% of CARE's normal events but 37% of randomly drawn eligible 7-day windows of ordinary operation (rate ratio 0.30-0.61 across four detectors). This is the energy-benchmark counterpart of spectrum bias in diagnostic-accuracy studies. Case-control designs with selected controls overestimate accuracy (Ransohoff & Feinstein 1978; Lijmer et al. 1999; Rutjes et al. 2006). PreDist's authors already suggested evaluating on randomly selected normal events (Limitation 2); we carry out that check and quantify the gap."

- **Do not claim** that we discovered that selected negatives bias evaluation.
- **Do claim** the first quantification for these benchmarks.
- **Credit PreDist** for raising the idea.

## Which medical concept to cite

- **Main citation:** spectrum bias from a case-control design (diseased cases against selected healthy controls).
  - Cite Ransohoff & Feinstein 1978 (NEJM, 10.1056/nejm197810262991705) for the concept.
  - Cite Lijmer et al. 1999 (JAMA, 10.1001/jama.282.11.1061) for the measured inflation.
- **Optional extras:**
  - Rutjes et al. 2006 (CMAJ, 10.1503/cmaj.050090): healthy controls.
  - QUADAS-2 (10.7326/0003-4819-155-8-201110180-00009): its "patient selection" domain.
  - Mulherin & Miller 2002: use "spectrum effect" if a neutral term is preferred.
- **ML bridge:** Ben-Hur & Noble 2006 (10.1186/1471-2105-7-s1-s2).
- **Corrections to the brief's citations:** the Rutjes paper found is CMAJ 2006, not 2005. The Fourure et al. 2021 abstract could not be retrieved, so treat it as UNVERIFIED.
