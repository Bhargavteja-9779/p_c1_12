# Author novelty score, cycle 5 (written BEFORE the blind review; MASTER_PROMPT 6.3)

Date: 2026-11-25 ~08:15 UTC. Evidence available: plan_v2 PreDist seeds 0-4, CARE seed 0, Holm step
(code/experiments/novelty_escalation_log.md, results/plan_v2/summary.md). CARE robustness seeds 1-4 still running;
this score is NOT revised upward after they finish unless a dimension changes for a stated reason.

| # | Dimension | Cycle 4 (blind, of record) | Cycle 5 author | Reason for change |
|---|---|---|---|---|
| 1 | Differentiation | 2 | **2** | Unchanged. Threshold leakage changing rankings is published (Kim 2022, Salem & Ferrugem 2026, Cools 2026, Liu 2026). New: a 2x2 decomposition showing the threshold-source effect replicates across two energy domains while the window-design effect does not (reverses on CARE). That is a sharper statement than prior work but not a new phenomenon. |
| 2 | Mechanism | 3 | **4** | The factorial identifies the mechanism: out-of-sample thresholds raise tau(ET->EH vs CH) on both datasets (Holm-significant), window design only on PreDist. Selection effect now holds for 16/17 (PreDist) and 13/14 (CARE) detectors, answering the "AEs ratio ~1" objection at panel level. |
| 3 | Evidence | 2 | **3** | Pre-registered, Holm-corrected, 15-17 detector panels, 5 seeds on PreDist (H7a/H7b/H7d 5/5). Still: exploratory data (both datasets used before), CARE 1 seed at writing, H7b CI includes 0 in 2/5 PreDist seeds, legacy M2 multiplicity remains in the project history. |
| 4 | Breadth | 3 | **3** | Two domains, 36+35 assets, 15-17 detectors; fault counts still small (29 / 45). |
| 5 | Significance | 3 | **3** | Practical advice (set thresholds out of sample; do not trust curated normal events) is clear but modest; FA-budget reference still UNVERIFIED. |

**Author total: 15 / 25.** G3 (>= 20, no dimension < 3) FAILS: differentiation 2.
Expected consequence (pre-stated so a later result cannot be oversold): plan_v2 fixed mechanism/evidence as the cycle-4
reviewer predicted (+1 each) and did not fix differentiation. Without a result that goes beyond Kim/Salem/Cools/Liu/
Song/Haneef/PreDist, G3 cannot pass; next step per D-17/D-19/D-21 is plan_v3 (new angle targeting differentiation) or
the honest-exit analysis paper.
