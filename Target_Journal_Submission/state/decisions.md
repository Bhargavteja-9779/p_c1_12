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
