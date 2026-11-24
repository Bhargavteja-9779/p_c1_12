RETROSPECTIVE entry reconstructed on 2026-11-24 from RECHECK/PROGRESS.md 'Log' and RECHECK/stage4/preregistration_E.md addendum (commit 292efa7, 18:53); RECHECK/stage5/stage5_leak_exclusions.csv; not written at the time.

# Leakage in online retraining exclusions

src/models/online.py treated fault exclusions as known before their report date.

Affected: "4/982 fits, M1 subs 4 and 7 only; M2 unaffected" (RECHECK/stage5/stage5_leak_exclusions.csv).

The same check found that a clean environment reproduces 12/12 committed M1 operating points exactly. The fix and the
re-scoring of the two substations were still open at the last save.
