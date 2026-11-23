# PROGRESS

## Current phase
STEP 2-3: method fixed (factorial framing); M1 rebuild + seeds, then locked M2 evaluation

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

- 2026-11-23 (session 2, branch claude/stoic-carson-8teuw3): rebuilt env; D6 rounds 3-4 done (log).
  Round 3 (daily unit, conformal budgets, under-delivery) all falsified. Round 4: dropping the primary-return
  loop (comfort-only SRCR-C) cuts FA ~55% and gives ~10x fewer FA than AE at matched recall. BUT the
  one-line comfort rule and own-history comfort 3-sigma are statistically indistinguishable from SRCR-C
  (paired per-fault ranks, scripts/paired_ranks.py). Protocol amendments A1-A3 added.
- PIVOT (decided 2026-11-23): core contribution = factorial explanation of false alarms, not a new ML model:
  factors (i) WHAT is monitored (comfort loops vs all signals), (ii) REPRESENTATION (relative to setpoint vs
  absolute signals), (iii) MODEL (rule / own-history stats / fleet quantile ML / AE). Cells already available:
  rule, loop3s_c, srcr-C (comfort x relative); loop3s, srcr gate_1s_local (all loops x relative);
  sigma3, iforest, qnbm, ae, ae_cond (all x absolute); ae_comfort (comfort x absolute).

- 2026-11-23 (session 3, branch claude/youthful-meitner-qelzen): fast-forwarded onto stoic-carson; NEXT ACTION
  items 2 (A4), 3 (mechanism) and novelty map were already done there. Fresh container: data + cache rebuilt;
  ALL M1 factorial cells being regenerated (logs results/logs/r_*.log). The previous session's ae_comfort and
  qnbm M1 runs never finished (logs stop at s17/s19).

- USER DECISION 2026-11-23 (session 3): journal = Energy and AI (confirmed by user, 72-day/IF still
  UNVERIFIED). Priority: NO desk rejection; paper must match the journal level (journal_level_profile.md).
  Desk-check targets (must all hold before writing is called done):
  * >= 2 data populations: M1 (35 subs, dev) + M2 (58 subs, other manufacturer, locked) -> cross-manufacturer test
  * >= 8 baselines incl. published AE benchmark (have 10 factorial cells), ablation of SRCR components
    (gate / one-sided / local / p_ret), seeds 0-9 for fleet model, Wilcoxon + McNemar + cluster bootstrap, Holm
  * public code + run_all.py, ~10 figures, 3-4 main tables, 45-55 verified references, ~8-9k words
  * framing = systematic evaluation + finding (journal pattern #5) with a usable method, NOT "new ML model";
    title pattern "[...] for [task] in district heating substations"; abstract ~230 words, single paragraph
  * Reviewer-Zero: "simpler method works" is answered head-on (it is the finding), not hidden

- USER 2026-11-23: manuscript must state "Code will be made available on request.", no funding, no competing interests (verbatim, see
  manuscript/declarations.md. The repo still gets README + run_all.py + tests (for reviewers on request).

- References: manuscript/novelty_refs.bib (51, Crossref-verified from novelty map) + background_refs.bib/.csv
  (39; ISA-18.2 and EEMUA 191 UNVERIFIED/no DOI; Holm 1979 + Demsar 2006 no resolvable DOI). Hermans 2024
  (10.1016/j.segy.2024.100159: seasonal model error + quantile thresholds on DH substations) is CLOSE to SRCR ->
  must be discussed in related work. Gueck 2024 CARE score: check full text before citing its definition.

- Session 3 rebuild check: srcr_comp seed 0 reproduces round 4 EXACTLY (SRCR-C 0.321/0.357/0.357 at
  0.654/1.436/1.436 FA/sub-yr; gate+1s+local 0.214/0.321/0.357). Seeds 1-9 M1 chain launched (r_srcr_seed*.log).

## NEXT ACTION (rewritten session 3)
Running in background (check results/scores/<name>/m{1,2} file counts; M1 = 35, M2 = 58 files):
  M1: ae_comfort, ae_cond, qnbm (xargs pool), srcr_comp_seed1..9 (+variants) chain.
  M2: rule/sigma3/loop3s/loop3s_c, then (after M1 pool) ae, ae_comfort, ae_cond, iforest, qnbm, run_m2_fleet 0.
  If a container restart kills them: rerun the same commands; compute_scores skips finished substations.
1. When M1 complete: matched_recall + paired_ranks for all cells (M1 table); seed summary for SRCR (1-9).
2. run_m2_fleet.py 1..9; then scripts/m2_evaluate.py 2 EXACTLY ONCE (log it in novelty_escalation_log).
3. Pre-registered v1 secondary analyses still owed (report all, incl. negative): cold start by days of own
   history (important: M2 median series = 182 d), missing loops, temporal sensitivity (fleet trained < 2018),
   efficiency (train/score time), fleet-level impact (alarms/week for 93 subs), PreDist event protocol
   (F0.5/earliness) for comparability, error analysis by fault label. Disclose: v1 said 24 evaluable M2
   faults, harness counts 25; v1 B6 fleet-pooled AE was not run (say so or run it).
4. Figures (~10) + tables (3-4) from real data; manuscript (manuscript/), reviews REVIEW/, docx + cover letter.

## Resume notes (saved 2026-11-23 before account switch)
- Results/scores and data cache are NOT in git (large). On a new machine: run
  `bash Target_Journal_Submission/code/scripts/download_data.sh`, then `python3 code/scripts/build_cache.py`,
  then regenerate scores (download_data.sh now creates data/raw itself): run_online_method.py ae 1 / ae_cond 1, run_srcr_cv.py 1, run_online_method.py intent 1 /
  delivery 1, run_srcr_components.py 0, round2_variants.py srcr_comp (all from Target_Journal_Submission/code).
  pip deps: scikit-learn scipy lightgbm torch(cpu) pyarrow tabulate pypdf matplotlib.
- Novelty-map candidate abstracts saved: journal_selection/novelty_candidates.csv (37 papers).
- User asked (pending reply): verify Energy and AI submission-to-acceptance + IF/quartile; may supply
  author guidelines PDF, author details, extra DH data.
