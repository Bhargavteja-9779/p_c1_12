# plan_v3 — arm 1: window-level oracle-threshold protocol (in the style of van Dreven et al. 2026)
Written 2026-11-25 ~13:40 UTC BEFORE any arm-1 metric was computed. plan_v1/v2 unchanged.
Reason: D-22 — the target journal published a PreDist M1/M2 study (10.1016/j.egyai.2026.100824) that scores daily
windows (20-83% faulty) with an oracle-threshold macro F1 and reports no false-alarm rate over time. Re-running that
style of protocol on the same data and detectors shows readers of this journal how far it is from deployment.
Not an exact reproduction (their code is not public): we implement the protocol as described (daily windows,
balanced-ish evaluation set, macro F1 at the best threshold) and say so.

## Data and detectors
Same as plan_v2 (PreDist M1 and CARE; panel members seed 0 + existing detectors; scores from results/scores_panel and
results/scores*). Pre-registered exploratory analysis on data already used (M2 not used).

## Protocol W (window-level, oracle threshold)
- Unit: calendar day per asset inside the monitored span, kept if >= 50% of its steps have a score.
- Faulty day: overlaps a target detection window (PreDist: [report - 7 d, report) of efd_possible faults; CARE:
  [event_start, event_end) of anomaly events). Normal day: overlaps no target window and no exclusion interval.
- Day score: maximum score of the day (detector's own scale; 1.0 = its training 99th percentile).
- Evaluation sets: W-bal = all faulty days + normal days drawn at random (rng(0)) so that faulty days are 50% of the
  set; W-nat = all faulty and normal days (natural prevalence).
- Metric (as in the reference protocol): macro F1 at the threshold that maximises it on the evaluated set (oracle);
  also AUROC.
## Hypotheses
 H8a: oracle macro F1 on W-bal exceeds macro F1 on W-nat at the SAME (W-bal-optimal) threshold for every detector,
      by >= 0.15 absolute (prevalence effect), per dataset.
 H8b: at its W-bal-optimal threshold, each detector's day-level false-positive rate on W-nat implies >= 10 false
      alarm days per asset-year for >= 2/3 of detectors (operational load hidden by W).
 H8c: Kendall tau between detector rankings by W-bal oracle macro F1 and by the plan_v2 reference CH (continuous,
      out-of-sample thresholds, recall at B = 2) is < 0.5, with a cluster-bootstrap CI (assets, 2,000, rng(0)).
 Holm over H8a-c x 2 datasets for the inferential parts (H8c CI upper bound < 0.5 counts as support).
Script: scripts/plan_v3_window_arm.py (committed before it is run on real scores).
