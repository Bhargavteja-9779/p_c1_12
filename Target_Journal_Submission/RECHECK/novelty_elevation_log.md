# Novelty elevation log (RECHECK, Prompt 2)

Ideas tried before this run: 19 (code/experiments/novelty_escalation_log.md, rounds 0-5, all reported).
User decision from the first run: Option A (honest benchmark), no further detector development. This run
therefore elevates novelty through evaluation science (protocol, chance reference, certification bound,
decision-level burden), which Prompt 2 lists explicitly (Q5, Q9, Q10, Q11), not through new detectors.
Running count of hypotheses tested in this run is kept at the bottom (for multiple-comparison reporting).

## Round 1 (2026-11-23)
Weakest point: "distance from prior work" (2/5). The benchmark finding is about one dataset; the PreDist
authors already concede their balanced protocol "overestimates" reliability (arXiv 2511.14791 p. 19-20).

Ideas generated (families):
1. Protocol gap: re-score identical score streams under the published event protocol vs continuous (new protocol).
2. Certification bound: what a balanced protocol with n normal events can certify (theory, Clopper-Pearson).
3. Random-alarm reference at matched FA rate (new evaluation baseline / sanity reference).
4. Representativeness of hand-picked normal events vs all normal weeks (benchmark fix).
5. Decision-level burden: false alarms per true detection, site visits per caught fault (problem formulation tied to cost).
6. Borrowed from clinical alarm research: alarm "positive predictive value" and alarms per patient-day mapped to
   alarms per substation-year (other field).
7. Abstain/defer: cells only alarm when two independent cells agree (inference idea). NOT run: would be a new
   detector, conflicts with Option A, and M2 is no longer blind.
8. Test-time adaptation of thresholds per manufacturer from normal data only (inference idea). NOT run, same reason.
Literature check for 1-6: delegated hostile search (RECHECK/stage3). Point-adjust and range-metric critiques
exist for generic TSAD; random-baseline comparisons exist in TSAD evaluation literature; nothing found yet for
DH or for converting balanced event protocols to operational burden. To be confirmed by stage3 report.

Pre-registration: RECHECK/stage4/preregistration_E.md (H-E1..H-E4), committed before running.

### Results so far
- H-E4 (chance level), script code/scripts/chance_level.py -> code/results/chance_level.csv:
  M1 27/33 cell x budget points above a random-alarm baseline at the same FA rate (Holm 0.05; M1 thresholds are
  in-sample). M2 (held-out manufacturer) 3/33: sigma3 at budgets 2 and 4 (7/25 vs chance 0.035-0.058),
  qnbm at budget 2 (5/25 vs 0.027). The published AE (1-2/25), conditional AE (0-3/25), SRCR-C (0/25) and the
  comfort rule (1-2/25) are not distinguishable from random alarms on M2. SUPPORTED.
- H-E1, H-E2, H-E3: pending (need full score rerun).

## Hypothesis count in this run
H-E1, H-E2 (22 internal tests, Holm), H-E3, H-E4 (66 internal tests, Holm), random-label permutation check.

### T1 certification bound (analytic; code/scripts/protocol_gap.py writes results/protocol_gap_t1.csv)
With zero false positives on n normal weeks, the one-sided 95% Clopper-Pearson upper bound on the weekly alarm
probability gives at most 52.18*q_u alarm-weeks per substation-year: n=30 (PreDist M2 normal events) -> 4.96;
n=35 (M1) -> 4.28; n=65 (both) -> 2.35. Certifying <= 1 alarm-week/sub-yr needs n >= 155 clean normal weeks
(<= 2: 77; <= 4: 38; <= 0.5: 312). The statistics are classical (Clopper & Pearson 1934; "rule of three",
Hanley & Lippman-Hand 1983, both Crossref-verified); the contribution is applying them to benchmark design for
fault detection, which no paper found so far does (pending stage3 report).
