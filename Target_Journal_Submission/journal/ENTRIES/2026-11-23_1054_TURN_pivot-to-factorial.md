RETROSPECTIVE entry reconstructed on 2026-11-24 from PROGRESS.md session-2 note; commits 6a8a1a1 and a217de0 (10:54); code/experiments/protocol.md A4; not written at the time.

# Pivot: from new model to factorial explanation

A paired per-fault rank test found "fleet model adds no significant gain over comfort rule" (commit 6a8a1a1). From the
file results/paired_ranks_latest.csv: SRCR-C vs rule, 15 vs 13 faults better, wilcoxon_p 0.4514767527580261.

We pivoted. The core contribution became a factorial of three factors:
- SCOPE: comfort loops vs all signals;
- REPRESENTATION: relative to setpoint vs absolute;
- MODEL: rule / own-history statistics / fleet quantile ML / AE.

Amendment A4 pre-registered HF1-HF4 for M2, before any M2 detector output existed.
