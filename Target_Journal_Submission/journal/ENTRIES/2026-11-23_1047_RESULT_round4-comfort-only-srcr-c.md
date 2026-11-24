RETROSPECTIVE entry reconstructed on 2026-11-24 from code/experiments/novelty_escalation_log.md 'Round 4 results' (commit b695787, 10:47); results/round2_srcr_comp_v_g1l_noret-v_g1l_retlow.csv, results/matched_recall_r4_vs_ae.csv; not written at the time.

# Round 4: dropping the primary-return loop (SRCR-C)

Stated diagnosis before the round: the primary-return limiter loop has the highest exceedance rate and reacts to
efficiency problems that customers do not report.

- H4a SUPPORTED: comfort-only "needs 0.18 FA/sub-yr for recall 0.214 (gate+1s+local: 0.40, -55%)".
- Versus AE: "AE 1.78 vs comfort-only SRCR 0.18 (~10x)".
- H4b FALSIFIED: CUSUM "reaches only 0.286 at <= 2 FA/sub-yr (counter 0.357)".

We fixed SRCR-C as the method candidate.
