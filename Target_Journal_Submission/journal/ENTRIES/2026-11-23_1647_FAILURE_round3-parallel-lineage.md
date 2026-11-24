RETROSPECTIVE entry reconstructed on 2026-11-24 from RECHECK/archive_parallel_lineage/Target_Journal_Submission/code/experiments/novelty_escalation_log.md 'Round 3 results' (wizardly-babbage, commit ce1b50a, 16:47); results/round3/round3_srcr_comp__v_gate_1s_local.csv; not written at the time.

# Round 3 (wizardly-babbage lineage): no gain

The parallel lineage did not know about stoic-carson's round 3 and ran its own version.

- H3a: the daily unit ties ("0.321 = R2 10-min 0.321") but with more false alarms (271 vs 186).
- H3b(iii) FALSIFIED: per-substation conformal thresholds give "recall 0.179 at B=2". They do equalise the burden
  (top-5 share 0.33 vs 0.66).
- H3c FALSIFIED: "-3 faults vs F10".

Stated diagnosis: "Own-past thresholds absorb slowly developing degradation (a fault's precursor becomes part of the
'normal' calibration set)".

This lineage's rounds 3-4 are missing from the merged escalation log. They survive only in the archived copy.
