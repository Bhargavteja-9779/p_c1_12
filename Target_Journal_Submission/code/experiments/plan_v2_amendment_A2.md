# plan_v2 Amendment A2 — operator budget sweep, area-like reference, family robustness (written BEFORE running)

Written 2026-11-28 ~03:40 UTC (commit time authoritative). Motivation (blind review cycle 5, Amendment A1 result):
(i) the CH reference is a single budget (B = 2) and tie-bound (2-12 detected events per detector); (ii) EH and CH
share the identical held-out threshold, which partly builds in H7a; (iii) the panel has near-duplicate members; (iv)
B = 2 FA/asset-yr has no operator source. A2 uses only the cached per-detector tables of plan_v2 (no new scores,
same events, same folds, same alarm logic).

Definitions (per dataset, per seed):
- Budgets BS = {0.5, 1, 2, 4, 8} FA per asset-year. For each budget, held-out points per fold exactly as plan_v2
  (PreDist 5-fold substations, CARE leave-one-farm-out); CH_B = pooled held-out recall at budget B.
- Area-like reference CHA = mean of CH_B over BS (less tie-bound; uses 5 thresholds, 4 of them not used by EH).
- Realised held-out FA per asset-year at each B is reported (calibration of the budget).
Hypotheses (one-sided):
 H9a (threshold source vs area reference): tau(EH, CHA) - tau(ET, CHA) > 0.
 H9b (window design vs area reference):    tau(CT, CHA) - tau(ET, CHA) > 0.
 Test: within-detector label swap (as A1 T2), 20,000 permutations, rng(0). Holm over {H9a, H9b} x {PreDist, CARE}
 at seed 0, alpha 0.05. Robustness: seeds (of 5) with unadjusted p < 0.05; claimed robust only if >= 4/5.
 PreDist primary = leak-free (D-30) for every seed where leak-free tables exist; otherwise legacy, labelled.
Descriptive (no tests):
 D1 Operator regret: at each budget, CH_B of the detector that is best on the benchmark (max ET) vs the best CH_B;
    share of budgets at which the benchmark-best detector is outside the top 3 by CH_B.
 D2 Leave-one-family-out: recompute the H9a and H9b differences with each family removed. Families (fixed now):
    zscore {z_max, z_mean, robust_z_max, ewma_z_max, q_frac}; linear {pca_spe, pca_t2, maha_lw};
    density {knn_pca, lof_pca, gmm_pca, iforest_pca}; physics/expert {rule, loop3s, temp3s}; nbm {qnbm};
    autoencoder {ae, ae_cond}. Report the sign of each difference.
 D3 Family-level medians: per family, median ET and median CHA.
Script: scripts/plan_v2_amendment_A2.py (committed with this file; run only afterwards).
