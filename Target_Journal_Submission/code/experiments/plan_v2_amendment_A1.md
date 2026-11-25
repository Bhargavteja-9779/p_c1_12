# plan_v2 Amendment A1 — calibrated tests for H7a/H7b (written 2026-11-25 ~21:45 UTC, BEFORE running them; time corrected afterwards, the commit 324f9e9 timestamp is authoritative)

Reason: the blind reviewer (review/blind_novelty_score_cycle5.md) showed that the pre-registered percentile bootstrap
is biased in favour of H7a (tuned cells are re-tuned inside each resample, which inflates their in-sample optimism
in a way that is not centred on the point estimate). The pre-registered Holm result stays the result of record for
plan_v2 and is reported unchanged. This amendment adds two calibrated tests; the paper reports both and claims
"confirmed" for a dataset only if the amendment also holds.

Inputs: committed files only, no new scores. Per dataset and seed: summary.json (point estimates), bootstrap.csv
(2,000 cluster-bootstrap replicates of dA = tau_EH - tau_ET and dB = tau_CT - tau_ET), cells.csv (per-detector
ET, EH, CT, CH).

Tests (one-sided, H1: d > 0), per dataset and seed:
 T1 Null-centred bootstrap: p = (1 + #{b : (d_b - mean(d_b)) >= d_hat}) / (B + 1). Also the basic-bootstrap 95% CI
    [2 d_hat - q97.5, 2 d_hat - q2.5].
 T2 Within-detector label swap (exact randomisation over the detector panel): for each of 20,000 permutations,
    independently swap the two compared cell values (ET<->EH for H7a; ET<->CT for H7b) of each detector with
    probability 1/2, recompute Kendall tau of each cell with CH, and the statistic d. p = (1 + #{d_perm >= d_hat}) /
    (N + 1). rng(0). Ties: scipy.stats.kendalltau (tau-b), as in plan_v2_analysis.py.
Decision (per hypothesis): seed-0 p-values of T1 and T2 each Holm-corrected over the 4 tests {H7a,H7b} x
{PreDist, CARE}, alpha 0.05. "Confirmed under A1" iff BOTH T1 and T2 reject after Holm. Robustness: number of seeds
(of 5) with T1 and T2 both < 0.05 unadjusted.
PreDist: primary = leak-free (D-30). T2 uses the leak-free cells.csv. T1 needs bootstrap.csv, which exists for the
legacy run only (leak-free seed-0 bootstrap.csv was not saved); T1 for PreDist leak-free is computed when the
leak-free bootstrap is regenerated, and the legacy T1 is reported meanwhile, labelled legacy.
Script: scripts/plan_v2_amendment_A1.py (written with this file, run only after both are committed).
