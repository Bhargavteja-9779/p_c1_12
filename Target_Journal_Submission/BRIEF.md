# Research brief (condensed from the user's original prompt, v2 "novelty-first")

Goal: find, build, test, review, revise and package ONE research project that solves a REAL-LIFE problem and
is novel enough to pass the editor's desk check at a high-quality Q1 journal. The agent chooses topic,
dataset, model, gap and journal. Do NOT write the paper first. Earlier papers by the user were desk-rejected
for "not enough novelty": if novelty is weak, change the idea, do not hide it with writing.

## Integrity (never break)
No fabricated results, citations, datasets, p-values, novelty, journal data or acceptance times. Experiments
not run never appear as results. No "SOTA"/"first" without proof ("to the best of our knowledge, based on our
search of [databases, dates]"). Seeds, baselines, metrics fixed before results; never weaken baselines.
Report negative results. Unavailable tool/data -> say so, mark UNVERIFIED. Every paper number comes from a
machine-generated result file. No copied text.

## Journal constraints
- Submission-to-acceptance <= 72 days. Measure: >= 20 recent articles (12-18 months) received/accepted dates ->
  `journal_selection/acceptance_time_evidence.csv` (title, DOI, received, accepted, days). PASS only if median
  well under 72 AND 75th percentile <= 72. Label first-decision time separately. Note survivorship limitation.
- JCR-indexed, Q1, high IF. Publishers: OUP, CUP, Elsevier, Springer Nature, Wiley, T&F, IEEE, ACM, SAGE, IET.
  NO MDPI, no predatory/doubtful journals. Scope fit beats IF and speed.
- >= 10 candidates internally; record JCR status, quartile, IF, category, publisher, ISSN, scope, APC, length,
  data/code rules. Record final choice: journal/publisher/ISSN/JCR/quartile/IF/category/median & p75 days/
  first decision/APC/scope fit/author rules/top rejection risks. If no journal meets all rules, choose the
  strongest and list the unmet rule.

## Part B: journal level and style
- `journal_benchmark.csv`: >= 25 recent papers (title, year, problem type, setting, datasets & size,
  #baselines, #datasets, #seeds, stats tests, ablation, robustness/cross-dataset, real-world evidence, code,
  length, #figs/tables, #refs, claimed novelty).
- `journal_level_profile.md`: medians; my paper must meet or exceed them (top quartile on baselines, datasets,
  real-world validation). `style_notes.md`: title/abstract/intro/contribution patterns, in own words.
- Plain English: short sentences, common words, active voice, define terms once, no hype.

## Part C: real problem
>= 15 candidate problems with one-sentence story: "[Who] struggles with [what], which costs [harm], because
current methods [specific failure]. We [built]. It [measured improvement], and we show why."
Real-Problem Test: named stakeholder; cited cost; documented failure of current methods; legal data;
real-world measure; journal fit. Desk-rejection stress test (incremental? known model on known data? mere
combination? invented problem? simpler method works? gain vanishes under stats? small/easy data? leakage?
depth? generality?).

## Part D: novelty engine
- `novelty_map.csv`: >= 30 closest papers (paper, year, venue, problem, method, data, claimed novelty, what
  they don't do, how mine differs in one sentence).
- Need >= 2 novelty types (N1 formulation, N2 method, N3 theory, N4 data/benchmark, N5 evaluation protocol,
  N6 real-world validation, N7 finding), one a core scientific idea.
- Scorecard 0-5 each: distance from closest 5; problem strength; idea depth; evidence; generality; journal-level
  match. < 22/30 or any < 3 -> redesign before coding.
- "Reviewer Number Zero": 3 hardest desk-reject sentences + evidence-based reply.
- D6 Novelty Escalation Loop (log in `experiments/novelty_escalation_log.md`): diagnose weakest point ->
  >= 5 genuinely different fix families -> check against novelty map -> pre-write hypotheses -> fair tests
  (same seeds/splits/budget) -> keep only if helps on held-out across seeds with a reason -> re-score.
  "Remarkable" = big real-world gain; stable statistically supported step-change (CI excludes 0, effect size);
  2-sentence reusable idea; explains WHY; works beyond one dataset/under shift; beats fairly tuned baselines at
  equal/lower cost; scorecard >= 26 with distance and evidence >= 4.
  Stop after checklist met + hostile review, or 6 rounds without gain (then change problem). After two full
  restarts with nothing remarkable: deliver honest strongest version labelled "NOT REMARKABLE".
  Validation set for choosing ideas; locked test touched once per final candidate; count all ideas tried,
  correct for multiple comparisons; report search in paper.

## Part E-G: plan, data, experiments
Story spine (problem, prior attempts, why not enough, idea, test, findings incl. failures, meaning in
real-world units, limits). Pilot evidence of baseline failure. Hypothesis + 3-5 RQs. Pre-register
`experiments/protocol.md` (dated): baselines (classical, conventional ML, standard DL, strong recent, SOTA,
lightweight), ablation, robustness, generalisation, efficiency, sensitivity, error analysis, real-world impact;
metrics, seeds (>= 5, 10 preferred), splits, equal tuning budget, stats tests. Leakage audit before training.
Project layout: README, requirements.txt, environment.yml, config/, data/, experiments/, scripts/, tests/,
src/{data,preprocessing,models,training,evaluation,statistics,visualization}, results/, figures/, tables/.
`run_all.py --mode quick|full` regenerates all results, figures, tables, stats. Auto-detect CPU/CUDA/MPS.
Unit tests. Stats: paired tests, Wilcoxon, McNemar, permutation, bootstrap CI, effect sizes, correction.

## Part H-K: writing, audits, reviews, package
Figures from real data only. Manuscript in the journal's format and learned style; intro opens with real
problem and cost; 3-4 contributions each tied to an experiment; Limitations; Data/Code availability;
declarations. Audits: claim-evidence, citation (verify DOIs), plagiarism. Desk-check against journal
checklist. Reviews saved as `REVIEW/review_01..10.md` + `review_stakeholder.md` (general; novelty; stats;
ML/code; external validity; cost; writing; competing researcher; associate editor; final hostile;
stakeholder), each FATAL/MAJOR/MODERATE/MINOR, then fix the research. Final: consistency audit,
reproducibility audit, `Final_Manuscript.docx` (+PDF), `cover_letter.docx`, `risk_report.md`, decision
READY FOR SUBMISSION / NOT READY.

Output folder: `Target_Journal_Submission/` with journal_selection/, manuscript/, code/, results/, figures/,
tables/, supplementary/, REVIEW/.

Show the user only: selected journal + 72-day evidence, one-sentence story, novelty scorecard, final package.
Keep `PROGRESS.md` updated after each phase. USER REQUIREMENT: commit and push after every step, so another
account can say "continue" and resume here.
