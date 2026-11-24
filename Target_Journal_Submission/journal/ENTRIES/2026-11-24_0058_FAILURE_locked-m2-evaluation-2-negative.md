RETROSPECTIVE entry reconstructed on 2026-11-24 from code/experiments/novelty_escalation_log.md focused-wozniak 'LOCKED M2 RESULTS' (log time 2026-11-24T00:58Z; commit a1a0a78, 01:13); results/m2/m2_locked_table.csv, results/m2/pooled_paired_B2.csv; not written at the time.

# Locked M2 evaluation #2 (focused-wozniak): negative

scripts/m2_eval.py was run once (after Amendment A2).

Recall at B=2, M1 -> M2:
- "C2 0.393 -> 0.080";
- "rule 0.321 -> 0.080";
- "AE 0.214 -> 0.040".

Other results:
- Pooled M1+M2: "C2 0.245 vs AE 0.132 ... Holm 0.766". "NO comparison survives Holm."
- F18 taxonomy: H5d and H5e FALSIFIED. The rule detects 2/25 M2 faults.
- Post hoc diagnostic: "44/58 M2 substations expose only the HC1 loop (no DHW loops) vs 9/35 on M1".
