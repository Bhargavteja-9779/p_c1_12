RETROSPECTIVE entry reconstructed on 2026-11-24 from code/experiments/novelty_escalation_log.md M2 access log (both lineages); commits 309057d (13:30) and 63cb0d0 (18:29); not written at the time.

# Three-sigma and IForest crash on short M2 series

While computing M2 scores, before any M2 metric, three-sigma and IForest crashed on a substation whose training window
had no usable signal (M2 substation 33, very short series).

Fix: such windows get no score (NaN). The log notes that this code path never triggered on M1.

Each lineage met and fixed the same crash on its own: youthful-meitner at 13:30, wizardly-babbage at 18:29.
