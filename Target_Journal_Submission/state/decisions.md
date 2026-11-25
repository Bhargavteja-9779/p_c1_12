# Decisions log (newest at bottom). Earlier decisions (cycles 1-3): PROGRESS.md, RECHECK/PROGRESS.md,
# code/experiments/protocol.md, code/experiments/novelty_escalation_log.md.

## D-2026-11-24-01  project/ = Target_Journal_Submission/
Reason: all prior work (code, results, manuscript, journal selection) already lives there; moving it would break
paths in committed scripts. HANDOFF.md, BOOTSTRAP_PROMPT.txt, MASTER_PROMPT.md, state/, journal/ created there.

## D-2026-11-24-02  Consolidate all parallel lineages into one branch
Found 4 diverged lineages (practical-sagan newest; focused-wozniak; peaceful-planck incl. youthful-meitner and
stoic-carson). All merged into claude/eloquent-shannon-czmqnz (session branch). Doc conflicts: both sides kept,
labelled by lineage. Code conflicts: the 63cb0d0-lineage version kept, the other archived verbatim under
archive/lineage_peaceful_planck/. Every remote claude/* branch is now an ancestor of HEAD (verified).

## D-2026-11-24-03  The locked M2 test is BURNED; no further M2 confirmation is possible
The M2 (manufacturer 2) test set was evaluated in two lineages unaware of each other (2026-11-23 ~14:10 UTC,
2026-11-24 ~00:58 UTC). Both negative for every proposed detector. Consequences: (i) no new M2 "confirmation" run
will be presented as blind; (ii) practical-sagan's plan item "run m2_eval.py ONCE" is cancelled; (iii) all M2
numbers computed from now on are labelled post hoc / descriptive; (iv) the double access is disclosed in the paper.

## D-2026-11-24-04  Compute budget unit
No GPU. 1 budget hour = 1 machine wall-hour with >= 1 queue job running on the 4-core CPU (analogue of one
GPU-hour). CPU core-hours are also logged. Compute of cycles 1-3 was never ledgered: recorded as UNVERIFIED and
not counted (budget.json prior_note). Current cycle = 4 (cycles 1-3 = sessions of 2026-11-23/24).

## D-2026-11-24-05  Contribution type and how G5 is applied
Pivot #1 already happened in cycle 2 (user option A: method paper -> evaluation paper), so pivots used = 1/3.
The paper's main claim is an evaluation finding (novelty type D primary, C secondary): balanced event-window
benchmarks overstate deployed alarm precision and select operating points with unusable false-alarm rates, and
can invert detector rankings. There is no "proposed method" to beat a baseline, so G5 is applied to the claimed
effect: per method, precision-inflation ratio (event / continuous) with a 95% bootstrap CI (resampling
assets) whose lower bound exceeds 5 (pre-registered threshold from H5c/H6b), Holm-corrected over methods x
datasets, on a dataset whose outputs had not been seen when the hypothesis was fixed (CARE). Stated plainly in
the paper and FINAL_REPORT; not a claim that G5 passed in its original method-vs-baseline sense.

## D-2026-11-24-06  SEEDS_CONFIRM = [100,101,102,103,104] fixed now; used for CARE learned detectors
CARE (wind SCADA, Round 6) is the only data on which no detector output has been seen. Its seeded detectors
(IForest, AE, AE-cond) are run for seed 0 (pre-registered Round 6) and for SEEDS_CONFIRM as the confirmation run.
SEEDS_EXPLORE [0,1,2] used for PreDist AE re-generation (seeds 3-9 already have committed tables; not re-run).

## D-2026-11-24-07  Journal rules updated by the user
MASTER_PROMPT v2 excludes Frontiers (overrides the 2026-11-24 earlier remark that Frontiers is acceptable).
Journal re-selection under Section 4 delegated to a sub-agent (journal_selection/*_v2.md).

## D-2026-11-24-08  Layer B supervisor written but NOT started in the cloud container
A `claude` CLI exists, but this cloud container is ephemeral and an interactive agent is already working in the
same checkout; starting a second headless agent would make two agents edit the same files. The supervisor is
for a machine the user owns (scripts/install_autostart.sh install --with-supervisor). Stated in HANDOFF.md.

## D-2026-11-24-09  Generative-AI declaration is kept in the manuscript
manuscript/authors_declarations.md records an earlier user request (2026-11-23) to remove AI-tool mentions from
deliverables. MASTER_PROMPT v2 (newer) says to state AI assistance plainly if the journal requires it; Elsevier
(Energy and AI) requires a generative-AI declaration. Following the newer instruction and the journal policy: the
declaration stays (worded plainly, authors to confirm). Code comments/README need not mention tools.

## D-2026-11-24-10  Journal (Section 4) final for now: Energy and AI, failing the 72-day rule
25 legitimate journals evaluated (journal_selection/journal_comparison_v2.md). None passes all rules. Energy and AI
kept (best fit; median 89 d, n=25, range 33-565; Q1 UNVERIFIED). Closest on timing: Energy Informatics (Springer)
70 d (n=97) but no Impact Factor shown -> Q1 not met/UNVERIFIED; ECM:X 73 d (n=30), moderate fit. G1 = FAIL, stated.

## D-2026-11-24-11  Ledger findings acted on
- Multiplicity count for the paper = state/variants_tried.csv: 82 rows / 64 distinct ideas (24 distinct proposed
  detectors actually run); M2 touched 15 times (2 locked evaluations, 1 pre-lock pilot, rest post hoc).
- T1 certification-bound numbers (peaceful-planck lineage) cite results/protocol_gap_t1.csv, which was never
  committed anywhere -> T1 numbers are UNVERIFIED and must not appear in the paper unless recomputed.
- Conflicting user decisions across lineages ("option A, no more methods" vs "keep iterating"): the newest user
  instruction (MASTER_PROMPT v2, 2026-11-24) governs: keep cycling to the gates. This is consistent with an
  evaluation-paper focus; no new detector-method round is planned unless the Section 6.4 ladder calls for it.
- No pre-coding novelty score exists (only 20/30 after the locked test); stated as a limitation of the process.
- Novelty ledger: 158 papers opened at abstract level, 1 full text -> G2 "opened" counted at abstract level, stated.

## D-2026-11-24-12  Claims narrowed after hostile prior-art search (literature/claim_table.md)
- C1 reworded: "we quantify the overestimation acknowledged by Roelofs et al."; never call the base-rate mechanism new.
- C2: no operator-tolerable FA figure is sourced -> results reported as functions of the FA budget (B = 1, 2, 4);
  "operators tolerate ~2" removed unless a source is found (scorecard_reviewer_zero.md wording is superseded).
- C3: lead with the decomposition (thresholds tuned on evaluated events vs not) and tau with a bootstrap CI.
- C4: supporting design check citing NIST TN 2118, not a contribution.
- C5: "control-unit manufacturer" (PreDist); CARE = "wind farm"; Song 2026 / Haneef 2026 / Vural 2026 cited as
  concurrent evidence. CARE replication is reframed from "novel second domain" to "independent replication".
- Section 6.4 rung 1-2 (diagnose / mechanism): the selection-effect test H5d (PreDist M1, pre-registered) and H6c
  (CARE) become priority analyses; a dedicated prior-art search for that specific claim follows once results exist.

## D-2026-11-24-13  CARE compute: OOM fix and confirmation scope (deviation, logged before any CARE analysis)
- 6 seed-0 AE/AE-cond jobs and 1 confirm job were OOM-killed (farm C: 953 columns; one AE fit peaks ~6 GB (dmesg; 4.3 GB seen mid-run);
  4 parallel jobs + PreDist exceeded 15 GB). All processes then died at ~06:21 UTC (container paused/reclaimed
  while idle; runner heartbeat stale ~6 h). Fix: queue restarted with 3 workers; failed jobs re-queued. No code or
  analysis change; scores are deterministic per seed, so re-running does not change results.
- Farm-C AE fits take > 7 min per turbine; full confirmation (3 methods x 5 seeds) would need ~55 machine-h vs ~12.5 h
  left in cycle 4. Following the pre-registered "as compute allows, priority ae, iforest, ae_cond": iforest seeds
  100-104 (cheap) and ae seeds 100-102 first, ae 103-104 if budget remains; ae_cond confirmation NOT run
  (status skipped_compute). H6e confirmation is reported only for methods with >= 4 completed seeds; others are
  reported as incomplete. No CARE result had been inspected when this was decided (round6_care.py not yet run).
- 13:40 UTC: still OOM with 3 workers (6.0 GB peak, cgroup kill in dmesg) -> 2 workers.

## D-2026-11-24-14  Selection-effect claim: wording after prior-art check (literature/selection_effect_claim.md)
45 queries; 64 CARE-citing + 6 PreDist-citing works screened; no paper compares alarm rates on curated normal events
with random ordinary-operation windows in any energy domain. The concept is established in medicine (spectrum bias:
Ransohoff & Feinstein 1978; Lijmer et al. 1999 JAMA; Rutjes et al. 2006 CMAJ; QUADAS-2) and ML (Ben-Hur & Noble 2006).
PreDist's own Limitation 2 suggests evaluating on randomly selected events but does not run it. Wording: "we run the
random-window check suggested by Roelofs et al. and measure a spectrum-bias-like effect in energy benchmarks";
claim the first measurement, not the concept. Note CARE paper says 51 normal datasets, Zenodo v6 has 50 (we use 50).

## D-2026-11-24-15  H5d analysis completed with its missing pooled CI (deviation, logged)
round5_selection.py (pre-registered, commit 4c9860f) was run unchanged once (results/round5/selection_m1.csv;
copy of run 1 kept in scratch). Its pre-registered criterion is the POOLED ratio with a bootstrap CI excluding 1,
but the script printed only the point estimate (0.466). We appended code that computes exactly that CI (cluster
bootstrap over substations, separate RNG so the per-method numbers are reproduced) and saves per-window hits.
No window, threshold, method or score was changed.

## D-2026-11-24-16  Queue re-prioritised for the remaining cycle-4 budget (~9.3 machine-h at 5.66 used)
Order: CARE ae confirm seeds 100-102 (pre-registered confirmation) > PreDist M2 regeneration (rule..ae seed 0,
srcr transfer; needed for M2 protocol-gap CIs, descriptive) > CARE ae seeds 103-104 > PreDist AE M1/M2 seeds 1-2
(seed-robustness only; tables for seeds 1-9 already committed). Whatever the budget stop skips is reported.

## D-2026-11-24-17  G3 FAIL (score of record 13/25); Section 6.4 ladder -> plan_v2 (2x2 protocol factorial), no pivot
Author 16/25 (recorded first), blind reviewer 13/25 (review/blind_novelty_score_cycle4.md); lower score used.
Pivot conditions (6.5): (a) >= 2 cycles yes, (b) score <= 14 yes, (c) "no tractable mechanism" NO: the reviewer names
a tractable, cheap experiment. So no pivot. Next rung: experiments/plan_v2.md = pre-registered 2x2 factorial
(window design: event windows vs continuous replay) x (threshold source: tuned on evaluated events vs on held-out
normal operation) with an enlarged panel of cheap detectors and seeds 0-4, reporting Kendall tau with CIs and Holm.
Expected to raise mechanism/evidence, not differentiation, so G3 may still fail; if so the honest exit (11.7)
analysis paper is the likely outcome.

## D-2026-11-24-18  plan_v2 panel jobs queued (30 jobs, priority 3, ahead of remaining CARE AE confirm seeds)
Dry run of plan_v2_analysis.py on substitute scores (every panel member = sigma3; outputs in scratch, meaningless)
completed without error (18 min, tables dominate). Panel jobs are cheap (~2.5 machine-h) and target the failing gate
G3; CARE ae seeds 101-104 continue after them as budget allows. Compute is still booked to cycle 4 until its queue
drains; cycle 5 starts with the plan_v2 analysis.
- 18:57 UTC: second worker restart (~17:50) killed the queue; 936 panel files verified readable; queue restarted (2 workers).

## D-2026-11-24-19  New user directive (USER_DIRECTIVES.md): keep improving with new methods until top-notch
Saved verbatim-in-substance to USER_DIRECTIVES.md, referenced from CLAUDE.md, BOOTSTRAP_PROMPT.txt, HANDOFF.md.
Actions: (1) deeper benchmark of recent Energy and AI papers -> literature/journal_quality_bar.md (writing style,
structure, evidence depth, what a "top" paper there contains); (2) scout fresh public labelled datasets so that any
NEW method can be tested on data never seen (M2 burned, CARE seen); (3) after plan_v2, a method cycle (plan_v3)
targeted at the diagnosed failure modes, pre-registered, tested on the fresh data.

## D-2026-11-24-20  Fresh test dataset candidate: Hill of Towie (Zenodo 22662930 v2.1.0, CC BY 4.0)
Scouting (literature/fresh_datasets.md, 18 candidates): no public set beyond PreDist/CARE has maintenance-log fault
labels. Hill of Towie: 21 turbines, 2016-2026, 10-min SCADA + alarm log (tblAlarmLog) + operator downtime
(ShutdownDuration). Fault events must be DERIVED from alarm/downtime logs by a rule written and committed before any
detector output on this data is computed (labels may be inspected; detector outputs may not). Disk: yearly zips are
converted to compact per-turbine parquet and deleted. Song 2026 (Zenodo 23902232) also used it -> cite.

## D-2026-11-24-21  Hill of Towie fault labels are NOT credibly derivable; fresh-test plan revised
Inspected 2019 tblAlarmLog (labels only; no detector output exists): 657,395 alarms, 327 codes, only 12 codes have
descriptions (Hill_of_Towie_alarms_description.csv). Song 2026 used Hill of Towie only for a restart analysis
(kp_hot.py), so no published fault rule exists to adopt. A home-made code->fault rule would be weak and attackable.
Revised options for a fresh test of any plan_v3 method: (a) Fuhrlander FL2500 (alarm logs with system/subsystem
descriptions; Song's published long-stop list can be adopted and cited; small: 5 turbines, ~15 turbine-years);
(b) Hill of Towie only for false-alarm-rate estimation in normal operation (no fault labels needed: a long, clean
normal record measures FA per turbine-year precisely). Decide after the journal quality-bar report and plan_v2
results. 2019.zip kept (1.4 GB) for option (b).

<!-- [lineage eloquent-shannon] -->
- 2026-11-25 13:07 UTC: resumed after ~17.5 h stop (queue dead). Queue restarted (2 workers). GitHub push/fetch
  now refused (github_link_required: the user must reconnect GitHub at claude.ai); committing locally until fixed.

## D-2026-11-25-22  Journal quality bar received (literature/journal_quality_bar.md, 39 papers, 10 full texts)
- CORRECTION: van Dreven et al. 2026 (10.1016/j.egyai.2026.100824, Energy and AI) already test PreDist M1<->M2
  transfer (balanced daily windows, best-threshold F1, no FA rate over time). Our "first cross-manufacturer test on
  PreDist" wording is withdrawn (related-work draft corrected). Residual: locked budgeted thresholds + continuous
  operation + matched-rate random-alarm reference.
- In-journal gap confirmed: no Energy and AI paper since 2024 evaluates under continuous monitoring with a FA budget;
  "false-alarm" appears in 1 of 636 abstracts; none uses CARE. The journal publishes audit/evaluation papers
  (10.1016/j.egyai.2025.100658, 100856, 100936) -> evaluation framing is acceptable there.
- plan_v3 (next): (1) re-run van Dreven's protocol arm (daily windows, best-threshold F1, M1->M2) with our detectors
  on PreDist and quantify its gap to continuous budgeted monitoring (M2 numbers labelled post hoc; this measures
  protocols on fixed detectors, it does not select a method); (2) controlled manipulation of normal-period selection
  (checklist item 3); (3) robust operating-point selection as the constructive method; (4) the journal checklist
  (23 items) drives the manuscript: graphical abstract, numeric highlights, protocol figure, practical implications,
  limitations, Friedman/Wilcoxon + effect sizes, code DOI.
- 2026-11-25: plan_v3 arm 1 pre-registered (experiments/plan_v3.md, scripts/plan_v3_window_arm.py). plan_v2_analysis.py
  now also saves ch_per_asset.csv (added BEFORE plan_v2 was run on real scores; needed by plan_v3 bootstrap).

<!-- [lineage intelligent-dirac] (parallel session; merged 2026-11-24) -->

## D-2026-11-24-22  New container (session on branch claude/great-mccarthy-85gvo2): rebuild + re-prioritised queue
Container was new (no data, scores, tmux). Verified eloquent-shannon contains every other claude/* branch; fast-forwarded
claude/great-mccarthy-85gvo2 to it (this is now the working branch; eloquent-shannon is an ancestor). Rebuilt env,
PreDist cache, CARE download. Queue restored from queue_snapshot with all done/running jobs reset to pending and
priorities set so the plan_v2 analysis inputs come first: PreDist M1 rule/loop3s/qnbm/ae(seed0)/ae_cond (p8),
panel predist1 seeds 0-4 (p7), CARE prep (p10, waits for download), CARE seed0 temp3s/ae/ae_cond (p6), panel CARE
seeds 0-4 (p5, after c4care_prep). Not needed for plan_v2 and deferred (p<0): PreDist M2 regen, sigma3/iforest/
underdel/srcr comps, M1 AE seeds 1-2, CARE sigma3/iforest seed0, CARE confirm AE 101-104. skipped_compute stays.
Regeneration compute is booked to the ledger (it is real compute) even though it reproduces lost files.
Workers = 2 (CARE farm-C AE memory, D-13).

## D-2026-11-24-23  CARE prep failure (stale marker) fixed; quality-bar benchmark received
logs/setup_care.log (download-done marker "CAREDL") had been committed from the old machine, so prep_care.sh started
on a partial zip and failed 3x (BadZipFile). Zip now complete (verified by zipfile), prep re-queued; the marker is
now gitignored so it cannot leak to a new machine again. Sub-agent wrote literature/journal_quality_bar.md and
journal_quality_papers.csv (34 Energy and AI papers, 6 full text; checklist used for the manuscript).
Notable: 10.1016/j.egyai.2026.100824 also uses PreDist (daily-window classification, upper-bound F1) = closest
same-journal comparison; 10.1016/j.egyai.2026.100975 = structure template (aggregate scores mislead model choice).

## D-2026-11-24-24  New container again (session on branch claude/serene-galileo-2zsx2t)
Fast-forwarded to claude/great-mccarthy-85gvo2 (verified it contains every other claude/* branch). Rebuild started
(env, PreDist, CARE download). The D-23 marker fix had not worked: logs/setup_care.log was still tracked and the root
.gitignore pattern `logs/setup_care.log` only matched at repo root. Now untracked + ignored by its full path.
Queue restored from snapshot, all done/running reset to pending (outputs are gone on this machine).

## D-2026-11-24-25  plan_v2_summary.py written before CARE results
plan_v2.md names scripts/plan_v2_summary.py for the Holm step, but it was never written. Written now, after the PreDist
seed-0 analysis and before any CARE plan_v2 output exists. It only implements the pre-registered procedure (Holm
step-down over the 4 seed-0 one-sided p-values, alpha 0.05; robustness = seeds with unadjusted p < 0.05; robust iff
>= 4/5). PreDist seed-0 p-values were known when writing; they do not affect the procedure.

## D-2026-11-24-26  New container again (session on branch claude/intelligent-dirac-9fs327)
Verified claude/serene-galileo-2zsx2t contains every other claude/* branch; fast-forwarded
claude/intelligent-dirac-9fs327 to it (now the working branch; serene-galileo is an ancestor). Rebuild started (env,
PreDist, CARE download). Queue restored from queue_snapshot, done/running/failed reset to pending (outputs gone).
Committed result tables (e.g. results/plan_v2/predist1/seed0) are kept; regenerated scores must reproduce them
(seed-0 PreDist analysis will be re-run only as a reproducibility check, not as a new test).

## D-2026-11-25-27  Compute ledger advanced to cycle 5 (plan_v2)
plan_v2.md was pre-registered as the cycle-5 plan ("cycle 5 budget 15 h"), but the ledger (state/budget.json) was never
advanced and kept booking plan_v2 work to cycle 4. Cycle 4 is closed at 11.95 machine-h (includes regeneration after
three container rebuilds). From 2026-11-25 02:15 UTC all compute is booked to cycle 5 (15 h cap). Global ceiling
(120 h) unchanged and unaffected (it sums all cycles): 11.95 h ledgered so far. MAX_CYCLES 12: this is cycle 5.
<!-- [end parallel lineages] -->

## D-2026-11-25-28  Single writer: session on claude/great-mccarthy-85gvo2; queue rebuilt on this container
At 13:30 UTC six sessions of this account were running "continue" in parallel. The user chose this session to
continue ("Continue from here"); the others should stop. Working branch: claude/great-mccarthy-85gvo2 (contains
every claude/* branch incl. eloquent-shannon 3837ba1). Ledger: merged budget_snapshot + 0.87 machine-h (cycle 4) used
on this container on 2026-11-24 19:47-20:39 and missing from the merged ledger. Queue rebuilt from the merged
queue_snapshot (all statuses reset; jobs whose outputs exist finish instantly): CARE seed-0 temp3s/ae/ae_cond (p6) and
CARE panel seeds 0-4 (p5) are the real work; PreDist panel seeds 1-4 deprioritised (-1; already analysed and
committed). Running now: plan_v2 predist1 seed 0 rerun (reproducibility check vs committed summary.json; writes
ch_per_asset.csv needed by plan_v3 arm 1).

## D-2026-11-25-29  Single writer moves to the session on claude/serene-galileo-2zsx2t
User (to this session, 14:50 UTC): "check recent branch and continue from there". claude/great-mccarthy-85gvo2 contains
every claude/* branch; fast-forwarded serene-galileo to it (bdd0c2c). The D-28 writer had not pushed for 85 min
(checked 13:35 -> 15:00, no branch moved), so this session continues as the single writer on
claude/serene-galileo-2zsx2t. Ledger: merged snapshot + 1.54 machine-h (cycle 4) from this container 2026-11-24
22:50-23:52, missing from the merge. Queue restored from the merged snapshot (statuses reset; existing outputs finish
instantly). Restarted: queue (2 workers), scripts/care_seed_chain.sh (CARE plan_v2 seeds 1-4 + summary), PreDist
plan_v2 seed-0 rerun (reproducibility check by git diff vs committed tables; writes ch_per_asset.csv for plan_v3 arm 1).

## D-2026-11-25-30  PreDist: leak-free exclusion rule becomes PRIMARY; legacy reported as sensitivity
The G8 sensitivity run failed its pre-registered robustness criterion (H8c flips; lof_pca CH changes by 4 faults),
although every H7 conclusion and the Holm outcome are unchanged. Because the leak-free rule is the correct one (no
future information) and CARE already uses it (A1), PreDist analyses reported in the paper use the leak-free rule from
now on, with the legacy numbers shown as a sensitivity row; the switch from legacy to leak-free and its effect are
stated in the paper. This is a bug fix, not a re-analysis choice: it is applied to every PreDist analysis equally.
Consequences: (1) H8c is reported with both values and NOT claimed (borderline: CI upper 0.497 vs 0.575);
(2) PreDist robustness seeds 1-4 must be re-run leak-free (panel seeds 1-4 for subs 4 and 7 only + plan_v2 analysis;
needs panel predist1 seeds 1-4 scores, currently not on this container); (3) earlier M1 round tables (rounds 0-8)
are legacy and are only cited as development history, not as paper results.

## D-2026-11-25-31  Single writer moves to the session on claude/intelligent-dirac-9fs327
User (to this session, ~21:50 UTC): "recheck latest branch and recent progress" + asked for the final submission.
serene-galileo (D-29 writer) last pushed 20:47 UTC. Merged origin/claude/serene-galileo-2zsx2t into
claude/intelligent-dirac-9fs327 (conflict only in novelty_escalation_log.md, both sides kept). This branch adds
CARE plan_v2 robustness seeds 1-4 (done 09:40 UTC here; serene-galileo did not have them). From now on the single
writer is this session; other sessions should stop.
