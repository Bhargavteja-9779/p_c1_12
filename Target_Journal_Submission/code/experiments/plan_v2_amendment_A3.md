# plan_v2 Amendment A3 — full-panel burden, chance baselines, selection-effect confound checks (written BEFORE running)

Written 2026-11-28 ~04:12 UTC (commit time authoritative). Motivation: peer review of manuscript v2
(review/peer_review_v2.md): (i) the CARE burden came from a 5-detector Round-6 analysis and the PreDist burden from a
different (window-level) protocol; (ii) no chance baselines; (iii) the curated-normal effect could reflect season or
proximity to unreported faults. Inputs: plan_v2 cached tables, events, random windows and folds (same code path as
A2); no new scores. Datasets/versions: CARE (primary), PreDist leak-free (primary) and legacy (sensitivity); seed 0
primary, seeds 1-4 descriptive where tables exist.

A3.1 Full-panel burden at the benchmark-optimal point (descriptive).
 For each detector: ET point = (tau, c) maximising event F0.5 over the plan_v2 grid (ties: first in grid order).
 At that point, pooled over all assets of the continuous replay: FA per asset-year, deployed alarm precision
 = detected faults / (detected faults + false alarms), event precision on the benchmark events, and
 inflation = event precision / deployed alarm precision (undefined if no alarm). Report per detector, range, median.
A3.2 Chance baselines (analytic, descriptive).
 Always-alarm event F0.5: precision = fault events / all events, recall = 1.
 Random alarms at budget B (Poisson alarm starts at rate B per asset-year, independent of faults): expected recall =
 mean over fault events of 1 - exp(-B * L / 365.25), L = detection-window length in days (PreDist 7 d; CARE the event
 window). Compared with CH_B (A2 cells) for B in {0.5,1,2,4,8}: count detectors above the random-alarm recall.
A3.3 Selection-effect confound checks (pre-stated criterion).
 Same HITS as plan_v2 (held-out B = 2 points). Two alternative random-window sets:
  (a) season-matched: random windows re-weighted so that their calendar-month distribution (by window start)
      equals that of the curated normal events (weight = month share in normal events / month share in random
      windows; months absent from random windows dropped);
  (b) far-from-records: only random windows whose start and end are >= 30 days from every fault report and every
      exclusion interval of that asset.
 Pooled ratio (curated / random) with a 2,000-replicate cluster bootstrap over assets (hits fixed), rng(0).
 Criterion: the selection effect is "robust to the confound" for a dataset if the ratio is < 1 with CI upper < 1
 under BOTH (a) and (b). Reported either way.
Script: scripts/plan_v2_amendment_A3.py (committed with this file; run only afterwards).
