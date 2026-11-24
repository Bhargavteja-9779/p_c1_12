# SURPRISE / TURN — the hostile prior-art search narrowed every headline claim (written at the time)
We expected the protocol-gap finding to be our strongest novelty. The claim-targeted search (literature/claim_table.md,
literature/prior_art_cycle4.json; 84 distinct phrasings, 61 papers opened) found:
- The PreDist paper itself (10.1016/j.energy.2026.141178) states that its balanced 50/50 reliability score
  overestimates precision; the base-rate mechanism is textbook (Axelsson 1999/2000). Our C1 is a measurement of an
  acknowledged effect, not a discovery.
- On CARE, cross-farm failure and near-random discrimination at an alarm budget are already reported in an
  unreviewed, pre-registered study (Song 2026, Zenodo 10.5281/zenodo.23902232, deposited 2026-11-03; we opened the
  record ourselves) and in Haneef et al. 2026 (10.3390/info17090930). "Protocol choice changes rankings" is
  established in time-series AD (Kim et al. AAAI 2022) and claimed for low-false-alarm evaluation (Salem & Ferrugem 2026).
- The binomial power argument (C4) is standard (NIST TN 2118).
- We have no source for "operators tolerate about 1-2 false alarms per asset-year"; it was used in our scorecard.
What survives: (i) measured inflation factors on both public energy benchmarks with one replay code base;
(ii) the decomposition showing that tuning thresholds on the evaluated events causes most of the ranking inversion
(round 5: Kendall tau 0.21 -> 0.64); (iii) cross-control-unit-manufacturer failure on PreDist incl. matched-FA random
alarms (3/33 above chance on M2); (iv) still untested: whether the benchmarks' hand-picked normal events are easier
than random normal time (H5d/H6c, a benchmark-construction selection effect) — if supported and not in prior art,
this is the most specific new finding we can earn.
