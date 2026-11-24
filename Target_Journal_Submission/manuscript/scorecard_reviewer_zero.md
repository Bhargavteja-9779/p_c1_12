# Novelty scorecard and Reviewer Number Zero (after the locked M2 test, 2026-11-24)

Story (one sentence): District heating operators who deploy early-fault detectors are disturbed by false alarms,
which costs technician time and trust, because published detectors are judged on balanced sets of hand-picked
7-day windows that hide those alarms. We scored 8 detectors on 93 real substations under continuous, budgeted
monitoring and across two manufacturers. The balanced benchmark overstated alarm precision 22-274x and chose
settings that give 3-113 false alarms per substation-year (operators tolerate about 2), and no detector, including
our own, kept its advantage on a second manufacturer.

| Criterion (0-5) | Score | Reason |
|---|---|---|
| Distance from closest work | 3 | PreDist benchmark uses event windows; continuous FA/sub-yr protocols exist in other domains (wind, telecom). New for DH, and first quantified gap on this benchmark (to the best of our knowledge, OpenAlex/arXiv search 2026-11-23). |
| Problem strength | 4 | Real utility data, customer-reported faults, alarm fatigue is a named operator problem. |
| Idea depth | 3 | Evaluation insight, explained mechanistically (base rates, threshold transfer, loop availability); no new model survives. |
| Evidence | 4 | Pre-registered, locked test, replicated on 2 manufacturers, 8 methods, 10 seeds, paired stats, 17 ideas reported. |
| Generality | 3 | One dataset, two manufacturers, one utility. Mechanism (base-rate dilution) is general. |
| Journal-level match | 3 | Energy and AI publishes "systematic evaluation/benchmark" papers; no new method lowers fit. |
| **Total** | **20/30** | Below the brief's 22 threshold and below 26 "remarkable". Label: **NOT REMARKABLE** as a method paper; honest evaluation paper. |

## Reviewer Number Zero
1. "This is a negative result with no new method; the editor will say not enough novelty."
   Reply: the contribution is the measured protocol gap, pre-registered and replicated on a locked second
   manufacturer (22-274x precision overstatement; 5/8 and 7/8 methods above 4 FA/sub-yr). This changes how every
   PreDist-style result should be read. Risk remains HIGH for desk rejection at Energy and AI.
2. "Of course balanced precision is higher than prevalence-weighted precision; this is base-rate arithmetic."
   Reply: partly true, so the paper must go beyond precision: (i) the event protocol picks DIFFERENT operating
   points and a different method ranking (rho 0.26-0.40); (ii) the false-alarm load at those points is measured on
   real normal operation, not assumed; (iii) threshold transfer across manufacturers fails. Still a real weakness.
3. "Only 53 target faults; nothing is significant."
   Reply: true for recall differences (stated). The protocol-gap effects are an order of magnitude and hold for every
   method on both manufacturers; add bootstrap CIs over substations for the FA rates and precision ratios before
   submission.
