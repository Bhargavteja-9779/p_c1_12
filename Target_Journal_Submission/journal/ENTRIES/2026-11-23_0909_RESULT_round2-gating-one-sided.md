RETROSPECTIVE entry reconstructed on 2026-11-24 from code/experiments/novelty_escalation_log.md 'Round 2 results' (commit b13bb37, 09:09); results/round2_srcr_comp.csv; not written at the time.

# Round 2: gating and one-sided residuals cut false alarms

- H2a SUPPORTED: gating cuts false alarms "239 -> 121 (-49%) at equal recall (0.214)".
- H2c SUPPORTED: one-sided residuals cut them "121 -> 86 (-29%)".
- H2b FALSIFIED: "+0.071 recall over SRCR-v0 (needed +0.10)".

Best variant: gate+1s+local, "0.321" recall at <= 2 FA/sub-yr (results/round2_srcr_comp.csv).

Our own note: "Recall differences remain 1-3 faults (n=28): not remarkable yet."

At 09:23 the project forked into two lineages (commit 107bb1a is the last common commit).
