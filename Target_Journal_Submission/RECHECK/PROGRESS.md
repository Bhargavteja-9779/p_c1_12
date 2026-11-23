# RECHECK PROGRESS (Prompt 2: re-verify and elevate)

Branch: claude/peaceful-planck-2kznjo. Started 2026-11-23.

## State found at start (honest)
- The first run did NOT finish. No manuscript, DOCX, cover letter or reviews existed. Two lineages had diverged
  at commit 107bb1a:
  * youthful-meitner lineage: locked M2 evaluation DONE (negative for the proposed SRCR-C), user decision
    "Option A = honest benchmark paper", draft sections 03 (data/methods), references, README, run_all.py.
  * wizardly/peaceful lineage (parallel, unaware of the other): froze different candidates (C1 rule, C2 rule OR AE)
    and had not run M2.
- Merged both. youthful lineage is canonical (it has the locked test and the user's decisions). Conflicting files
  of the parallel lineage are archived verbatim in RECHECK/archive_parallel_lineage/.
- INTEGRITY NOTE: because M2 was already opened in the youthful lineage, the parallel lineage's frozen C2
  (rule OR AE) can no longer be evaluated blind on M2. Any M2 number for C2 must be labelled post hoc.

## Stage status
- Stage 1 (journal): IN PROGRESS
- Stage 5 compute: `run_all.py --mode full` running in clean venv /opt/recheck_env (log RECHECK/logs/run_all_full.log)

## Log
- Bug R5-1 (FIXED): run_all.py called system `python3` for build_cache.py, so a clean install failed at step 1.
  Now uses sys.executable.
- Stage 1: first VERIFIED received->accepted data for Energy and AI (25 published PDFs from institutional
  repositories found via OpenAlex): median 89 d, p75 141 d; last 6 months (n=11) median 65, p75 92.5.
  -> FAILS the 72-day rule. Scanning alternative Elsevier journals with the same method (stage1/alt.log).

## NEXT ACTION
Finish the alternative-journal scan (stage1/multi_journal_dates.py), write stage1/stage1_journal_report.md,
decide journal; then Stage 2.
