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
