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

## NEXT ACTION (saved 2026-11-23 for account switch)
Stage status: 1 nearly done (journal: Energy and AI FAILS 72 d; 10/20 alternatives scanned, all FAIL, see
stage1/alt_journal_summary_partial.md); 2 done; 3 done; 4 round 1 partly done (H-E4 supported, T1 done; H-E1/E2/E3
and random-label test need M2 scores); 5 partly (12/12 M1 points reproduced; leak found); 6.1 done; 7 started
(manuscript/sections/01_introduction.md, figures via code/scripts/make_figures.py); 8-10 not started.

On a NEW machine (container is lost; scores are not in git):
1. git fetch origin && fast-forward onto the newest claude/* branch (this one: claude/peaceful-planck-2kznjo).
2. Clean env (README route): python3 -m venv /opt/recheck_env; /opt/recheck_env/bin/pip install torch --index-url
   https://download.pytorch.org/whl/cpu; /opt/recheck_env/bin/pip install -r code/requirements.txt
3. From code/: nohup /opt/recheck_env/bin/python run_all.py --mode full --jobs 4 > ../RECHECK/logs/run_all_full.log 2>&1 &
   (~10 h; it was at ae_cond M2 when saved: all M1 single-substation cells done except ae_comfort partly).
4. Finish alt-journal scan: cd RECHECK/stage1 && python3 multi_journal_dates.py "Energy Conversion and Management: X"
   "Journal of Building Engineering" "Energy Strategy Reviews" "Applied Thermal Engineering" "Expert Systems with
   Applications" "Knowledge-Based Systems" "Reliability Engineering & System Safety" "Building and Environment"
   "Energy Nexus" "Energy and Built Environment"  (NOTE: script overwrites alt_journal_dates.csv -> change output
   name first, e.g. alt_journal_dates_part2.csv). Then write stage1/stage1_journal_report.md and decide: if none
   passes, keep Energy and AI (best fit) and state the 72-day FAIL plainly in the final report (do not hide it).
5. After run_all: compare results/locked_m2_*.csv with git HEAD (git diff --stat code/results); then run
   scripts/protocol_gap.py, scripts/random_label.py, scripts/chance_level.py (venv python); evaluate H-E1..H-E3
   against RECHECK/stage4/preregistration_E.md; log in RECHECK/novelty_elevation_log.md.
6. Fix leak in src/models/online.py known_exclusions (fault exclusion known only after its report date); re-score
   M1 subs 4 and 7 for per-substation methods; report delta (RECHECK/stage5/).
7. Stage 5 rest: seeds summary, efficiency table from logs, error analysis; Stage 4 scorecard; Stage 7 full
   manuscript + DOCX; Stage 8 reviews R1-R6; Stage 9 audit; Stage 10 final_recheck_report.md.
Pending from user: author names, affiliations, CRediT.
