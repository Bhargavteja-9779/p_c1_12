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

- Stage 5 early check: fresh clean-env scores reproduce 12/12 committed M1 operating points of rule, sigma3, loop3s,
  loop3s_c EXACTLY. Leakage found: fault exclusions treated as known before their report (src/models/online.py
  known_exclusions); 4/982 fits, M1 subs 4 and 7 only; M2 unaffected (stage5/stage5_leak_exclusions.csv).
- Stage 4 round 1 pre-registered (stage4/preregistration_E.md). H-E4 SUPPORTED: on M2 only 3/33 operating
  points beat random alarms at the same FA rate (code/results/chance_level.csv); M1 27/33 (in-sample).
- Stage 2 story written (stage2_story.md). Stage 6.1 references re-verified (stage6/); EEMUA 191 dropped.
- Stage 3 DONE: stage3/novelty_map_v2.csv (135 rows), prior_art_report.md, close_calls_verified.md (2 close calls verified; claims narrowed).
- Stage 1 alt-journal scan (stage1/multi_journal_dates.py, 20 Elsevier journals) running: Results in Engineering
  median 93 / p75 105 (n=25), Smart Energy 127.5 / 250 (n=10): both FAIL.

- LIVE FILES untracked while jobs run (remove from .gitignore and force-add when done): stage1/alt.log, stage1/alt_journal_dates.csv, stage3/raw/, logs/run_all_full.log.

## NEXT ACTION
1. Wait for run_all full (log logs/run_all_full.log); then compare ALL committed numbers (m2_evaluate output vs
   results/locked_m2_*.csv in git), run scripts/protocol_gap.py and scripts/random_label.py (venv python).
2. Fix exclusion leakage (knowledge time = report date), re-score M1 subs 4, 7, report delta.
3. Finish stage1 report when alt scan ends; Stage 3 merge when agent reports; then Stage 4 scorecard, Stage 7 writing.
