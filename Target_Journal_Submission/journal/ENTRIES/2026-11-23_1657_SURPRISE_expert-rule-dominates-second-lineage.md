RETROSPECTIVE entry reconstructed on 2026-11-24 from RECHECK/archive_parallel_lineage/Target_Journal_Submission/code/experiments/novelty_escalation_log.md 'Diagnosis after round 3' (commit abd64ad, 16:57); results/m1_table.csv; not written at the time.

# The other lineage finds the same thing: the expert rule dominates

On the full M1 baseline table, the minimum FA/sub-yr to reach recall 0.214 / 0.286 / 0.321 was:
- rule: 0.15 / 1.08 / 1.08;
- SRCR R2: 0.40 / 1.48 / 1.48;
- AE: 1.78 / 5.63 / 5.63.

Log: "THE EXPERT RULE DOMINATES EVERY LEARNED METHOD, INCLUDING SRCR." The rule and SRCR detect exactly the same 9
faults. AE detects 4 faults that neither of them detects.

This matches the stoic-carson surprise from 10:53, reached independently.
