# PROGRESS

## Current phase
STEP 0: journal landscape and 72-day check (in progress)

## Decisions so far (with reasons)
- 2026-11-23: Acceptance time is measured from Crossref received/accepted dates (all articles of the last
  ~18 months, not only 20). Only publishers that deposit those dates can PASS the 72-day check:
  Springer Nature, Taylor & Francis, Wiley/Hindawi, IET. Elsevier/IEEE/SAGE/OUP = UNVERIFIED (risk).
- Compute is CPU-only, so the topic must be feasible with classical ML / small neural nets on public data.

- OpenAlex: cursor paging needs API key; page= paging works. 2212 journals (cit2y>4) -> 814 after scope keyword
  filter (`candidates_filtered.csv`).
- Springer journal pages (link.springer.com/journal/<id>) show JCR IF + median first-decision days when rendered
  with headless Chromium (`scripts/fetch_page.js`, run with NODE_PATH=$(npm root -g)). T&F/Wiley pages 403.

- Topic exploration (provisional, pending journal choice): CARE wind-turbine benchmark DROPPED (63 citing
  works, >=4 already do conformal/drift-aware calibration -> incremental). Leading candidate: PreDist district
  heating substations dataset (Zenodo 19496480, CC-BY-4.0, 93 substations, 2 manufacturers, 73 faults / 55
  efd_possible, 65 normal events). Baseline paper arXiv 2511.14791 (Energy 2026): AE NBM, hand-picked training
  windows, tuned on test events, balanced 50/50 eval (overstates precision), no continuous-monitoring false-alarm
  rate. Close competitors: Energy 2026 three-layer hybrid (doi 10.1016/j.energy.2026.142993), Energy&AI 2026 STST
  (10.1016/j.egyai.2026.100824), Expert Systems 2026 federated VAE (10.1111/exsy.70194).
- Pilot (code/experiments/pilot/pilot_signals.py): 44% of 54 faults show |z|>4 control-loop deviation in 7 d
  before report vs own 120-d baseline. Exploratory only; normal-day false-alarm rate not yet measured.

- STEP 0 DONE (2026-11-23): 841 journals scanned. No energy/AI journal at measurable publishers passes the
  72-day rule. SELECTED: Energy and AI (Elsevier, 2666-5468); 72-day status + IF/quartile UNVERIFIED (stated in
  journal_selection/selected_journal.md). Reserves: Smart Energy, Energy. Rejected: ESR (passes timing, poor fit).
- Topic: PreDist DH substations, proposed SRCR (setpoint-relative control-loop residuals + fleet quantile model)
  evaluated with a new continuous-monitoring protocol. M2 = LOCKED test (experiments/TEST_LOCK.md).
  Protocol v1 pre-registered: code/experiments/protocol.md.
- Code: code/src/{data/predist.py, evaluation/continuous.py, evaluation/runner.py, models/online.py, ae.py,
  baselines.py, srcr.py, features/loops.py}; scripts/run_online_method.py, run_srcr_cv.py, build_cache.py.
  Python 3.13 main env; official EnergyFaultDetector in /opt/efdenv (py3.12; recreate with
  `uv venv -p /usr/bin/python3.12 /opt/efdenv && VIRTUAL_ENV=/opt/efdenv uv pip install energy-fault-detector==0.8.1`).

- D6 round 0 done (see code/experiments/novelty_escalation_log.md). Round 1 running: intent + delivery channels
  (src/models/channels.py), fusion (src/models/fusion.py). Journal benchmark delegated to a sub-agent (writes
  journal_benchmark.csv, journal_level_profile.md, style_notes.md) — if missing after resume, redo STEP 1.

- STEP 1 DONE: journal_benchmark.csv (40 Energy and AI papers, 16 full text), level profile, style notes.
- D6 rounds 0-2 DONE (log in code/experiments/novelty_escalation_log.md). Best so far on M1:
  srcr_comp + compose(gate=True, one_sided=True, local=True): recall 0.321 at 1.48 FA/sub-yr; AE 0.214.
  Not yet 'remarkable'. Components: scripts/run_srcr_components.py; variants: scripts/round2_variants.py.
- Baselines rule/sigma3/loop3s/iforest/qnbm launched on M1 (check results/scores/<name>/m1 has 35 files;
  rerun scripts/run_online_method.py <name> 1 if not).

## Session 2026-11-23 (account 2)
- New machine: data + cache rebuilt, M1 scores regenerating (logs results/logs/regen). Round 3 pre-registered;
  scripts/round3.py written (F10 daily, F13 conformal, F12 underdel = new channel "underdel"). Novelty map
  delegated (journal_selection/novelty_map.csv + novelty_map_summary.md).

- Novelty map DONE: journal_selection/novelty_map.csv (47 rows) + novelty_map_summary.md. Claimable: N1 (setpoint
  residual + gating + one-sided), N5 (continuous FA/sub-yr protocol); partial N2, N6; NOT N3 (split-conformal FA
  guarantees are standard; fleet+conformal exists for wind, 10.1088/1742-6596/3224/6/062054), NOT N4. To check:
  full text of 10.1016/j.energy.2026.142993 (control-strategy mode rules) and 10.1016/j.enbuild.2024.114009.

## NEXT ACTION (updated 2026-11-25, account 4)
Branch: claude/practical-sagan-m0onar. User: keep improving until novelty scorecard is top level; Frontiers OK.

DONE this account (all in code/experiments/novelty_escalation_log.md, results in code/results/round5..8):
- R5: H5a-d SUPPORTED on M1. Benchmark-style event protocol ranks 9 detectors almost independently of continuous
  deployment ranking (Kendall 0.21); three-sigma is best on events, mid-table in deployment; event precision
  inflated 16-44x; hand-picked normal weeks alarm 0.43x as often as random normal weeks (CI 0.18-0.68).
- R7: corrected protocol E* FALSIFIED vs start-based ranking (0.32) -> diagnosis: alarm starts vs active time.
- R8: alarm-DAYS burden: setpoint-relative rule/SRCR 0.32/0.36 recall at 8 alarm-days/sub-yr; benchmark AE 0.04,
  IForest 0. H8b (tau 0.68), H8c (E* vs day-based 0.61) supported; H8a narrowly falsified (SRCR > rule by 1 fault).
- R6 script ready (scripts/round6_care.py); temp3s-only run: CARE normal events alarm 0.11x random windows.
- Background (if lost: rerun): CARE scoring `cat scripts/care_jobs.txt | xargs -P 2 ...` (farm C needs ~2.5 GB/job:
  max 2 parallel!), PreDist `cat scripts/resume_predist.txt | xargs -P 2 ...` (M2 jobs + AE seeds 3-9 M1).
- Sub-agents (if their files are missing, redo): journal_selection/novelty_map_protocol.csv + _summary.md
  (evaluation-critique literature), journal_selection/acceptance_time_evidence_frontiers.csv + frontiers_summary.md.
NEXT: (1) when CARE scores done: python3 scripts/round6_care.py -> H6a-d; also alarm-days on CARE.
(2) bootstrap CIs for Kendall tau (R5, R8). (3) locked M2: m2_eval.py once + round5_protocol.py 2 + round8 on M2.
(4) re-score novelty; Reviewer Number Zero; then manuscript.

(older) TO DO on the new machine (scores are NOT in git; all background jobs of account 3 are lost):
1. Setup (from code/): pip install scikit-learn scipy lightgbm pyarrow tabulate pypdf matplotlib pandas statsmodels;
   pip install torch --index-url https://download.pytorch.org/whl/cpu; bash scripts/download_data.sh;
   python3 scripts/build_cache.py   (~5 min download + 1 min cache)
2. PreDist scores: `cat scripts/regen_all_jobs.txt | xargs -P 4 -I{} sh -c "python3 {}"` (M1 all methods + AE seeds 0-9
   + all M2 jobs; ~3-5 h), plus `python3 scripts/run_online_method.py underdel 1`,
   `python3 scripts/run_srcr_components.py 0 && python3 scripts/round2_variants.py srcr_comp`.
   (Measured: M1 non-AE methods + AE seed 0 finish in ~1 h.)
3. As soon as M1 methods + srcr_comp exist: python3 scripts/round5_protocol.py 1 ; python3 scripts/round5_selection.py
   -> record H5a-d verdicts in the escalation log.
4. CARE: download Zenodo 14958989 (Care_To_Compare.zip, 6 GB) to code/data/raw/care/, unzip to raw/care/x/, then
   unzip each "Wind Farm X.zip" into raw/care/x/Care_To_Compare/farm_X/ (19 GB unpacked; delete zips).
   Then `cat scripts/care_jobs.txt | xargs -P 2 -I{} sh -c "python3 {}"`. Still to WRITE: scripts/round6_care.py
   (LOFO operating points at B=1,2,4 using C.evaluate_substation with care_eval.labels; event protocol on all 95
   CARE events; random-window selection test; resolution for 50 normal events) -> H6a-d.
5. Then locked M2: scripts/m2_eval.py ONCE (+ round5_protocol.py 2 inside the same locked run), m2_curves.py.
6. Re-score novelty (scorecard), Reviewer Number Zero, decide story: likely "deployment-realistic evaluation
   overturns benchmark conclusions in energy fault detection" (N5 + N7 + analytic resolution result), with
   DH + wind evidence, plus rule OR AE as practical method.

## Resume notes (saved 2026-11-23, account switch #2)
- Scores/data are NOT in git. On a new machine, from Target_Journal_Submission/code:
  1. pip install scikit-learn scipy lightgbm pyarrow tabulate pypdf matplotlib pandas;
     pip install torch --index-url https://download.pytorch.org/whl/cpu
  2. bash scripts/download_data.sh && python3 scripts/build_cache.py
  3. M1 scores (needed by m2_eval): run_online_method.py {rule,sigma3,loop3s,iforest,qnbm,ae,ae_cond,underdel} 1;
     ae 1 k/4 SEED for seeds 1-9; run_srcr_components.py 0; round2_variants.py srcr_comp.
     (M1 tables results/m1_table*.csv, m1_curves*.csv, round4/*.csv ARE in git, so op points need no recompute.)
  4. M2 scores (frozen methods): see job list in NEXT ACTION item 1; run 4 in parallel (xargs -P 4).
     sigma3/iforest M2 crash (no usable columns) FIXED in baselines.py; rerun them on M2.
     Session 2 ended with M2 partially done (rule, loop3s complete) - all M2 must be recomputed on a new machine.
  5. Then scripts/m2_eval.py ONCE, scripts/m2_curves.py.
- Run time on 4 CPU cores: M1 regen ~2 h, AE seeds M1 ~2 h, M2 all ~3 h.
- Branches: work pushed to both claude/sweet-bell-5gq62v and claude/wizardly-babbage-182x46 (identical).

## Older resume notes (session 1)
- Results/scores and data cache are NOT in git (large). On a new machine: run
  `bash Target_Journal_Submission/code/scripts/download_data.sh`, then `python3 code/scripts/build_cache.py`,
  then regenerate scores: run_online_method.py ae 1 / ae_cond 1, run_srcr_cv.py 1, run_online_method.py intent 1 /
  delivery 1, run_srcr_components.py 0, round2_variants.py srcr_comp (all from Target_Journal_Submission/code).
  pip deps: scikit-learn scipy lightgbm torch(cpu) pyarrow tabulate pypdf matplotlib.
- Novelty-map candidate abstracts saved: journal_selection/novelty_candidates.csv (37 papers).
- User asked (pending reply): verify Energy and AI submission-to-acceptance + IF/quartile; may supply
  author guidelines PDF, author details, extra DH data.
