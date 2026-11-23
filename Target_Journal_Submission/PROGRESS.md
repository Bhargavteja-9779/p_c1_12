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

## NEXT ACTION
1. Finish M1 scores: ae (default) + srcr (results/scores/*/m1, git-ignored; regenerate via scripts).
   Then compute operating curves (src/evaluation/runner.operating_curve) and compare at FA budget 2/sub-yr.
2. Run baselines on M1: rule, sigma3, iforest, loop3s, qnbm, ae_cond (scripts/run_online_method.py).
3. STEP 1 journal benchmark from Energy and AI papers via OpenAlex/arXiv (ScienceDirect blocked).
4. Novelty map (30 papers) + scorecard; D6 loop on M1 only.
