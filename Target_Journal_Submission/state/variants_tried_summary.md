# Variants tried: summary of `state/variants_tried.csv`

Reconstructed on 2026-11-24 from the merged logs and the git history. Times are UTC commit times unless the log
gives a time itself. No numbers were recomputed: every key number is copied from a log, or (where marked "file:")
read from the named result file.

## Lineage map (from `git log --graph`)
- **trunk**: commits up to 107bb1a (2026-11-23 09:23). It covers topic choice, the pilot, and rounds 0-2. All lineages inherit it.
- Fork 1, chain stoic-carson (10:16-11:05) -> youthful-meitner (12:41-15:14) -> peaceful-planck (18:42-19:18, RECHECK).
- Fork 2, wizardly-babbage (= sweet-bell, 16:09-18:29, up to 63cb0d0). Two lineages then branched from 63cb0d0 without knowing about each other:
  - focused-wozniak (2026-11-23 19:27 - 2026-11-24 01:15);
  - practical-sagan (2026-11-24 03:02-03:43).
- Idea numbers (#8, #9, ...) and hypothesis labels (H3a, H5a, ...) were reused by different lineages for **different** ideas. The ledger therefore uses its own IDs, V001-V081.

## Totals
| Count | Value |
|---|---|
| Rows (idea / variant / analysis families, all lineages) | **81** |
| Rows without `duplicate_of` (distinct ideas) | 64 |
| Proposed-detector rows / of which actually run (not `not-run`/`dropped`) | 37 / 29 |
| Distinct proposed-detector ideas actually run | 24 |
| Analysis rows / protocol rows / topic rows / baseline rows | 37 / 3 / 2 / 2 |
| Outcomes | falsified 26, supported 17, descriptive 19, not-run 14, dropped 3, tie 2 |
| Rows with `evaluated_on_test = yes` (touched M2 outcomes or M2 fault data) | **15** |

`descriptive` is an outcome value we added. It marks analyses that had no falsifiable hypothesis, such as baseline tables, a mechanism analysis or an analytic bound.

The lineages counted their own ideas as follows:
- youthful-meitner chain: "19 ideas" (escalation log, peaceful-planck section, round 5).
- wizardly-babbage -> focused-wozniak: "17 ideas, 5 rounds" (escalation log, focused-wozniak section).
- practical-sagan: gave no count.

These counts share ideas #1-#7. Their ideas #8-#14 are different ideas under the same numbers. A paper reporting "N ideas tried" should use this ledger, not either lineage's own count.

## Per lineage
| Lineage | Rows | falsified | supported | tie | descriptive | not-run | dropped | M2 touches |
|---|---|---|---|---|---|---|---|---|
| trunk | 16 | 3 | 4 | 0 | 4 | 4 | 1 | 1 (pre-lock pilot) |
| stoic-carson | 14 | 6 | 1 | 0 | 5 | 1 | 1 | 0 |
| wizardly-babbage | 11 | 5 | 2 | 1 | 2 | 1 | 0 | 0 |
| youthful-meitner | 15 | 9 | 2 | 0 | 4 | 0 | 0 | 8 |
| peaceful-planck | 10 | 0 | 2 | 0 | 2 | 5 | 1 | 1 |
| focused-wozniak | 8 | 3 | 2 | 1 | 2 | 0 | 0 | 5 |
| practical-sagan | 7 | 0 | 4 | 0 | 0 | 3 | 0 | 0 |

## Every row that touched M2 (evaluated_on_test = yes)
| ID | Lineage | Date (UTC) | What |
|---|---|---|---|
| V003 | trunk | 2026-11-23 ~08:20 (commit 3c1504f) | Exploratory pilot printed control-loop z-scores for M2 faults **before** the test lock. Disclosed in TEST_LOCK.md |
| V041-V044 | youthful-meitner | 2026-11-23 14:10-14:34 | **LOCKED M2 EVALUATION #1** (HF1-HF4, 11 cells; scripts/m2_evaluate.py 2 2000) |
| V045 | youthful-meitner | 2026-11-23 14:34 | Post hoc rank transfer M1 vs M2 |
| V046-V048 | youthful-meitner | 2026-11-23 14:48 | Pre-registered secondary analyses on M2: cold start, pooled ranks, by label |
| V056 | peaceful-planck | 2026-11-23 18:53 | H-E4 chance level on M2, which reuses the locked #1 results (3/33) |
| V065 | focused-wozniak | 2026-11-24 00:58 | F19 protocol gap on M2. The event-optimal point was chosen on M2 itself |
| V075 | focused-wozniak | 2026-11-24 00:58 | F18 taxonomy tested on M2 |
| V076 | focused-wozniak | 2026-11-24 00:58 | **LOCKED M2 EVALUATION #2**: C1, C2 and all baselines, seeds 0-9, pooled tests (scripts/m2_eval.py) |
| V077 | focused-wozniak | 2026-11-24 ~01:15 | Curve-level endpoint, M1 vs M2 |
| V078 | focused-wozniak | 2026-11-24 ~01:13 | Post hoc loop-availability diagnostic on M2 |

## Locked M2 evaluations (the test set was opened twice)
1. **youthful-meitner, 2026-11-23.** Commits mark the start (14:10:38, "Log: locked M2 evaluation started (single run)") and the logged result (14:34:14).
   - Frozen set: protocol A4/A5 (SRCR-C plus 10 factorial cells).
   - Result: negative. SRCR-C 0/25; HF4 failed.
   - Files: code/results/locked_m2_operating_points.csv, locked_m2_tests.csv, logs/LOCKED_m2.log.
2. **focused-wozniak, 2026-11-24.** The log time is "2026-11-24T00:58Z"; results were committed at 01:13:54 and 01:15:02.
   - Frozen set: protocol Amendment A1/A2 (C1 rule, C2 rule OR AE) plus F18 and F19.
   - Result: negative. "C2 0.393 -> 0.080".
   - Files: code/results/m2/, code/results/protocol_gap/m2_*, logs/m2_eval.log.
   - This lineage descends from wizardly-babbage (63cb0d0). Its round-5 plan says "M2 still NOT evaluated", so it did not know about evaluation #1.
   - peaceful-planck had already noted at 18:49 on 2026-11-23 (commit 5438c8a) that C2 "can no longer be evaluated blind on M2" (RECHECK/PROGRESS.md). That note was on a different branch.

**Planned but not run:**
- practical-sagan's NEXT ACTION item 5, "Then locked M2: scripts/m2_eval.py ONCE", would have been a third evaluation. state/decisions.md D-2026-11-24-03 cancelled it.
- peaceful-planck's NEXT ACTION item 5 plans further M2 runs (protocol_gap, random_label) labelled as secondary.

**M2 access that produced no outcome metrics:**
- M2 column / loop availability checks: A4, and the commit "M2 loop availability checked" at 17:01.
- M2 score computations:
  - youthful-meitner, from 13:15;
  - wizardly-babbage, from 18:06;
  - the current cycle-4 queue (state/queue.json).

## Integrity issues found while building the ledger
1. **The test set was used twice.** Two sessions that did not know about each other each ran a "single" locked M2 evaluation. Both were negative. Neither M2 result can be called a blind confirmation. Every later M2 number (V056, V065, V077, V078) is post hoc.
2. **The merged escalation log drops part of wizardly-babbage.** That lineage's rounds 3-4 (daily unit, per-substation conformal, and the OR-fusion that created candidate C2) are not in the merged `code/experiments/novelty_escalation_log.md`. Its unlabelled rounds 3-4 section is the stoic-carson version. The wizardly text survives only in RECHECK/archive_parallel_lineage/.../novelty_escalation_log.md, which is identical to git 63cb0d0.
3. **The T1 result file is missing.** The certification-bound numbers (V057) cite `results/protocol_gap_t1.csv`, but that file was never committed in any branch. The numbers exist only in RECHECK/novelty_elevation_log.md.
4. **Users made conflicting decisions in different lineages.**
   - youthful-meitner: the user chose option A, "Do NOT develop further methods".
   - focused-wozniak: "user asked for more novelty", and it ran three more detector ideas.
   - practical-sagan: "keep iterating until novelty is very strong".
5. **No scorecard before coding.** BRIEF.md requires a novelty scorecard before coding (< 22/30 -> redesign). The only scorecard found is dated after the locked test: 20/30, manuscript/scorecard_reviewer_zero.md.
6. **Labels were reused.** The same hypothesis labels (H5a-H5h) and family labels (F16-F22) mean different things in three lineages. Use the V-IDs when citing.
