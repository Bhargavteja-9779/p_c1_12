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

## NEXT ACTION
1. Round 3 DONE (no primary gain; see log). Round 4: pre-register, then run (candidates in log).
2. Novelty map DONE; scorecard once the method is fixed.
3. Then seeds 0-9, full baselines table on M1, single locked evaluation on M2.

## Resume notes (saved 2026-11-23 before account switch)
- Results/scores and data cache are NOT in git (large). On a new machine: run
  `bash Target_Journal_Submission/code/scripts/download_data.sh`, then `python3 code/scripts/build_cache.py`,
  then regenerate scores: run_online_method.py ae 1 / ae_cond 1, run_srcr_cv.py 1, run_online_method.py intent 1 /
  delivery 1, run_srcr_components.py 0, round2_variants.py srcr_comp (all from Target_Journal_Submission/code).
  pip deps: scikit-learn scipy lightgbm torch(cpu) pyarrow tabulate pypdf matplotlib.
- Novelty-map candidate abstracts saved: journal_selection/novelty_candidates.csv (37 papers).
- User asked (pending reply): verify Energy and AI submission-to-acceptance + IF/quartile; may supply
  author guidelines PDF, author details, extra DH data.
