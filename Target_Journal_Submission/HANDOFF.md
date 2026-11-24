# HANDOFF — read this first (project/ = Target_Journal_Submission/)

Last updated: 2026-11-24 ~04:05 UTC (cycle 4, session on branch `claude/eloquent-shannon-czmqnz`).
Branch rule: work on the newest `claude/*` branch that contains all others. On 2026-11-24 ALL remote claude/*
branches were merged into `claude/eloquent-shannon-czmqnz` (verified: every one is an ancestor of HEAD).
If you are a new session on another branch: `git fetch origin && git merge origin/claude/eloquent-shannon-czmqnz`
(or the newest descendant), resolve, then continue here.

## NEXT ACTION
1. `python3 scripts/status.py`. If the container is new (no tmux "queue", no code/data/), run the
   NEW-MACHINE steps below first.
2. When group `c4care_seed0` is done: `cd code && python3 scripts/round6_care.py 0` (pre-registered H6a-e; the script
   was committed BEFORE any CARE score existed). Record verdicts verbatim in code/experiments/novelty_escalation_log.md
   and a RESULT/SURPRISE/FAILURE journal entry. Do NOT edit the script after seeing results except to fix a crash
   (log any fix as a deviation).
3. When `c4care_confirm` finishes (or the cycle budget stops it): `python3 scripts/round6_care.py <seed>` for
   each completed seed in 100..104; summarise mean +- sd (H6e confirmation rule in the log).
4. When `c4predist` is done: write+run `code/scripts/protocol_gap_ci.py` = bootstrap CIs (resample substations)
   of the PreDist M1/M2 precision-inflation ratios and FA rates at event-optimal points (DESCRIPTIVE, post hoc);
   run `scripts/round5_selection.py` (H5d) on M1; fix the PreDist leak (RECHECK NEXT ACTION 6) as a sensitivity run.
5. Then: scripts/final_report.py + scripts/audit_numbers.py (not written yet), novelty re-score + blind reviewer
   agent, manuscript (story style, Section 9) from journal/ + results, review panel (Section 10).

## One-line summaries
- Journal: Energy and AI (Elsevier, ISSN 2666-5468) — FAILS the 72-day rule (verified median 89 d, n=25,
  RECHECK/stage1); Q1/IF UNVERIFIED (JCR login). Re-selection under MASTER_PROMPT v2 in progress
  (journal_selection/journal_comparison_v2.md, selected_journal_v2.md — written by a sub-agent this session).
- Topic: deployment-realistic (continuous, false-alarm-budgeted) evaluation of early fault detectors in energy
  systems, vs the balanced event-window benchmarks used in the literature. Data: PreDist (93 district-heating
  substations, 2 manufacturers) + CARE to Compare (36 wind turbines, 3 farms).
- Hypothesis: balanced event benchmarks overstate deployed alarm precision by >= 5x, choose operating points with
  unusable false-alarm rates, and can invert detector rankings; this replicates on a second energy domain.

## What is running
- tmux session `queue`: `python3 scripts/queue_runner.py run --workers 4` (Layer A). Groups: c4predist (PreDist
  M1+M2 score regeneration, 44 jobs), c4care_prep (unzip + cache CARE; waits for the download), c4care_seed0
  (14 jobs, pre-registered Round 6), c4care_confirm (60 jobs: ae, iforest, ae_cond x seeds 100-104 x 4 parts).
- Background download: CARE zip -> code/data/raw/care/Care_To_Compare.zip (log logs/setup_care.log; "CAREDL" = done).
- Supervisor (Layer B): NOT running (see Known problems).

## Compute (state/budget.json = live, gitignored; state/budget_snapshot.json = committed copy, refresh with cp before each commit)
Cycle 4: see `scripts/status.py` (budget 15 machine-h/cycle, global ceiling 120 h). Cycles 1-3 compute was never
ledgered (UNVERIFIED, not counted). Hardware: 4-core CPU, 15 GB RAM, no GPU.

## Gate status (Section 7) — cycle 4 start
| Gate | Status | Evidence / reason |
|---|---|---|
| G1 Journal | FAIL (stated) | v2 done (journal_selection/selected_journal_v2.md, 25 journals): Energy and AI kept; median 89 d (n=25; last 12 mo 84 d) > 72 d; Q1 UNVERIFIED. Only Energy Informatics (Springer, 70 d, n=97) passes timing but shows no IF (Q1 fails/UNVERIFIED). |
| G2 Prior art | PARTIAL | state/novelty_ledger.json: 164 queries, 176 papers, 158 opened (abstract level; 1 full text). Claim-targeted hostile search running (literature/claim_table.md) |
| G3 Novelty >= 20/25 | FAIL so far | last score 20/30 on the brief's old scale (manuscript/scorecard_reviewer_zero.md); needs re-score on the /25 scale + blind reviewer after CARE |
| G4 Baselines | PARTIAL | 8 detectors incl. the dataset paper's AE reproduced on the same protocol; exact reproduction of published PreDist numbers not possible (their protocol tuned on test events) — gap explained in protocol.md |
| G5 Main effect | UNKNOWN | applied to the protocol-gap effect (D-05); CARE confirmation pending |
| G6 Ablation | N/A-PARTIAL | evaluation paper: "components" = protocol ingredients (test-tuned thresholds vs event windows; Kendall tau 0.21 -> 0.64 when thresholds are not test-tuned, round 5) |
| G7 Generalization | PENDING | PreDist M1 + M2 done (gap replicates); CARE running |
| G8 Leakage | PARTIAL | leak found (4/982 PreDist fits, RECHECK/stage5); fixed for CARE (A1); PreDist sensitivity run pending |
| G9 Reproducibility | PARTIAL | clean-env re-run reproduced 12/12 M1 operating points exactly (RECHECK stage 5); fresh-clone test of final tables pending |
| G10 Review | NOT STARTED | |
| G11 Audit | NOT STARTED | scripts/audit_numbers.py to be written |

## Last decisions (full list: state/decisions.md)
D-01 project/ = Target_Journal_Submission · D-02 all lineages merged · D-03 M2 test burned (evaluated twice) ·
D-04 budget unit = machine-hour · D-05 G5 applied to protocol-gap effect · D-06 SEEDS_CONFIRM on CARE ·
D-07 Frontiers excluded (v2 rules) · D-08 supervisor not started in cloud container.

## Last failures (details: journal/ENTRIES, code/experiments/novelty_escalation_log.md)
1. Locked M2: proposed SRCR-C recall 0/25 (youthful lineage, 2026-11-23). 2. Locked M2: C1/C2 recall 0.04 at B=1-2
(focused lineage, 2026-11-24). 3. Integrity: M2 evaluated twice by unaware parallel sessions. 4. On M2 only 3/33
operating points beat random alarms (chance_level.csv). 5. F17 own-history calibration hurt (0.321 < 0.429).
6. Round 5 peer-relative channels falsified (youthful). 7. Round 3 daily unit / conformal / under-delivery falsified.
8. CUSUM falsified (round 4). 9. Energy and AI fails 72 d. 10. Leakage in known_exclusions (4/982 fits).

## Commands (run from Target_Journal_Submission/)
- Status: `python3 scripts/status.py`
- Logs: `tail -f logs/queue_runner.log`; per job `logs/jobs/<job_id>.log`; supervisor `logs/supervisor.log`
- Stop compute: `tmux kill-session -t queue` (jobs keep running; to kill them too: `pkill -f run_online_method; pkill -f run_care`)
- Resume compute: `tmux new-session -d -s queue "python3 scripts/queue_runner.py run --workers 4 >> logs/queue_runner.log 2>&1"`
  (adopts still-running jobs; never redoes done jobs; scripts skip existing outputs)
- Add jobs: `python3 scripts/queue_runner.py add --group NAME --file code/scripts/LIST.txt [--priority N] [--after GROUP]`
- Autostart (own machine only): `bash scripts/install_autostart.sh install [--with-supervisor]`; remove: `bash scripts/install_autostart.sh remove`
- Supervisor stop: `touch state/STOP_SUPERVISOR`

## NEW-MACHINE steps (scores/data are NOT in git)
1. `cd code && pip install torch --index-url https://download.pytorch.org/whl/cpu && pip install -r requirements.txt statsmodels`
2. `bash scripts/download_data.sh && python3 scripts/build_cache.py` (PreDist, ~2 min)
3. CARE: `mkdir -p data/raw/care && curl -L -o data/raw/care/Care_To_Compare.zip "https://zenodo.org/records/14958989/files/Care_To_Compare.zip?download=1" && echo CAREDL >> ../logs/setup_care.log` (~6 GB, ~30 min)
4. `cp state/budget_snapshot.json state/budget.json` (restore the compute ledger), then `cd .. && python3 scripts/queue_runner.py reset-running` then start the queue (Resume compute). state/queue.json
   lists jobs marked done on the OLD machine: set them back to pending first:
   `python3 -c "import json;q=json.load(open('state/queue.json'));[j.update(status='pending',attempts=0) for j in q['jobs']];json.dump(q,open('state/queue.json','w'),indent=1)"`
   (done jobs whose outputs exist finish in seconds).

## Known problems
- Layer B: a `claude` CLI exists, but this is an ephemeral cloud container and an interactive session already works
  in this checkout, so the supervisor was NOT started (two agents would edit the same files). Auto-restart therefore
  does NOT work here: after a usage limit or account switch, paste BOOTSTRAP_PROMPT.txt manually.
- Container is reclaimed after inactivity: everything not pushed is lost (scores, data, caches are regenerable).
- results/scores*/ and data/ are gitignored (large). Result tables/CSVs/JSON ARE committed.
- M2 is burned as a test set (D-03). Never present a new M2 number as blind.
- T1 certification-bound numbers are UNVERIFIED (results/protocol_gap_t1.csv never committed); recompute or drop.
- Wizardly lineage rounds 3-4 only in RECHECK/archive_parallel_lineage/ (pointer at end of escalation log).
- PreDist leak (known_exclusions legacy rule) still in the PreDist path; sensitivity run pending.

## Where things are
- Brief/rules: BRIEF.md (old brief), MASTER_PROMPT.md (current). History: PROGRESS.md (all lineages), RECHECK/.
- Protocol + pre-registrations: code/experiments/protocol.md, novelty_escalation_log.md, TEST_LOCK.md.
- Code: code/src (data, evaluation, models, features), code/scripts, code/tests; queue: scripts/queue_runner.py.
- Results: code/results/ (m1_*, m2/, locked_m2_*, protocol_gap/, round5/, round6/ (CARE), chance_level.csv).
- Manuscript drafts: manuscript/ (sections/, scorecard_reviewer_zero.md, declarations, bib files).
- Journal choice: journal_selection/. Prior art: RECHECK/stage3/, journal_selection/novelty_map*.csv, state/novelty_ledger.json.
- Diary: journal/ENTRIES/. Ledgers: state/variants_tried.csv, state/decisions.md.
- Archived conflicting files of parallel lineages: archive/lineage_peaceful_planck/, RECHECK/archive_parallel_lineage/.
