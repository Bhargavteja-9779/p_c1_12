# Pre-registration: elevation round 1 (protocol gap + certification bound)

Written 2026-11-23 BEFORE any number below was computed. Committed to git before the script was run.

## Why (weakest novelty point)
Scorecard item "distance from prior work" and Q9/Q11: the benchmark story ("rankings do not transfer") is a
finding about one dataset. The PreDist authors themselves write that their balanced event protocol overestimates
reliability (arXiv 2511.14791, p. 19-20) but they do not quantify it. A reusable, quantified fix to the standard
evaluation, plus a formal statement of what a balanced event protocol can certify, would be new and usable by others.

## Experiments
E1 Protocol gap. For every factorial cell whose online score streams exist (rule, loop3s, loop3s_c, sigma3,
   iforest, qnbm, ae, ae_cond, ae_comfort, srcr_c, srcr_all), on M1 and M2 separately:
   (a) PreDist event protocol, reimplemented from the paper: fault events = our evaluable target faults
       (efd_possible, first occurrence), test window [report - 7 d, report); normal events = normal_events.csv
       (7-day windows). Event positive if the criticality counter reaches C_thr inside the window.
       tau fixed at the cell's M1 budget-2 tau (locked_m2_operating_points.csv). C_thr chosen on the SAME
       manufacturer by maximising eventwise F0.5 over the grid 1..288 (this mirrors the paper, which tuned on its
       evaluation events; it is deliberately the published protocol, not our recommendation).
       Report eventwise precision, recall, F0.5, pointwise accuracy on normal events.
   (b) Continuous protocol (ours) at the SAME (tau, C_thr): recall, false alarms per substation-year,
       alarm precision TP/(TP+FA), false alarms per true detection.
E2 Representativeness of hand-picked normal events. q_hand = share of the dataset's normal events with an
   alarm; q_all = share of ALL eligible normal substation-weeks (non-overlapping 7-day blocks inside the monitored
   span, outside detection windows and exclusion intervals) with an alarm, same (tau, C_thr).
T1 Certification bound (analytic, Clopper-Pearson): with n normal events and k false positives, the 95% upper
   bound on the weekly alarm probability q is q_u; the implied operator burden in alarm-weeks per substation-year
   is 52.18 q_u. Minimum n with k = 0 to certify a budget of B alarm-weeks per year: n >= ln(0.05)/ln(1 - B/52.18).
   Precision at realistic prevalence pi (fault weeks / all substation-weeks, measured on the data):
   P(pi) = R pi / (R pi + q (1 - pi)).

## Hypotheses and what would prove them wrong
H-E1 (primary): For the published-style AE cells (ae, ae_cond) the event protocol reports eventwise precision
   >= 0.8 while continuous alarm precision at the same threshold is <= 0.2 on both manufacturers.
   FALSIFIED if continuous alarm precision > 0.2 for either AE cell on either manufacturer, or if event
   precision < 0.8 (then the inflation claim is not supported in our reimplementation).
H-E2: q_all > q_hand for the majority (>= 7 of 11) of cells on each manufacturer (hand-picked normal weeks are
   easier than typical normal weeks). FALSIFIED if q_all <= q_hand for >= 5 of 11 cells on either manufacturer.
   Test: per cell, exact binomial test of k_hand ~ Bin(n_hand, q_all); report Holm-corrected p over 22 tests.
H-E3: the ranking of cells by event-protocol F0.5 does not agree with the ranking by continuous recall at
   2 FA/sub-yr (Kendall tau < 0.5 on each manufacturer). FALSIFIED if tau >= 0.5 on both.
Decision rule: E1/E2/T1 enter the paper as a contribution only if H-E1 holds. All results are reported either way.

## Integrity
- No method is changed. Only existing score streams are re-scored. M2 has been opened before (locked run of
  session 3); E1/E2 on M2 are secondary analyses of frozen methods, labelled as such.
- Number of hypotheses in this round: 3 (plus 22 binomial tests inside H-E2, Holm-corrected).

## Addendum (2026-11-23, before running; Stage 5 sanity checks)
H-E4 (chance-level check): a detector that raises alarms at random (Poisson) at its achieved false-alarm rate
   f (per substation-year) "detects" a fault with probability p0 = 1 - exp(-f * 7 / 365.25) (any alarm start in the
   7-day window). For every cell and budget, test observed detections k of n faults against Bin(n, p0)
   (one-sided, Holm over all cells x budgets x manufacturers). Expectation: on M1 most cells exceed chance;
   on M2 several cells are NOT distinguishable from random alarms. Reported whatever the outcome.
Random-label test: move every target fault's 7-day window to a random eligible normal week of the same
   substation (200 permutations, seed 20261123) and recompute recall at the locked operating points; the
   permutation recall must be close to p0. A detector whose real recall lies inside the permutation
   distribution has no demonstrated skill on that manufacturer.
Fault-exclusion leakage found in src/models/online.py (fault exclusion "known" before its report; 4/982 fits,
   M1 subs 4 and 7 only; list in RECHECK/stage5/stage5_leak_exclusions.csv). Fix after the clean rerun; re-score
   M1 subs 4 and 7 and report the change.
