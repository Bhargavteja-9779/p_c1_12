# Journal comparison v2 (Section 4; 2026-11-24)

Rules applied (hard rules from the user):
- **R1 Publisher**: reputable (Elsevier, Springer Nature, IEEE, ACM, Wiley, T&F, SAGE, IET, OUP, CUP). MDPI, Hindawi,
  Frontiers, other high-volume / questionable / delisted publishers excluded.
- **R2 JCR Q1** in its category. JCR needs a login; quartile/IF stated only if read on a public page opened here.
- **R3 Submission -> final acceptance <= 72 d**: median of Received->Accepted over >= 10 articles from the last 12-24
  months (computed here from article-level dates; first-decision time never used).

## How the days were measured
- **Elsevier** (no dates in Crossref, ScienceDirect = HTTP 403): Received/Accepted dates parsed from page 1-2 of
  repository copies of the published PDF found via OpenAlex (`pdf_url` not at sciencedirect/elsevier/arXiv),
  articles published 2025-05-23..2026-11-23, first <= 30 dated articles per journal.
  Scripts: `RECHECK/stage1/multi_journal_dates.py` (part 1), `journal_selection/v2_evidence/multi_journal_dates_v2.py`
  (part 2; identical logic, configurable output path). Energy and AI: `RECHECK/stage1/extract_dates.py`.
- **Springer Nature / Wiley / T&F / IET**: Crossref `assertion` fields (publisher-deposited Article History), random
  sample of up to 100 research articles. Scripts: `journal_selection/scripts/acceptance_scan.py` (18-month window) and
  `journal_selection/v2_evidence/crossref_assertion_dates.py` (24-month window, new titles).
- Evidence files (one row per article with DOI, received, accepted, days):
  - E0 `RECHECK/stage1/egyai_dates_from_pdfs.csv` (Energy and AI)
  - E1 `RECHECK/stage1/alt_journal_dates.csv` (10 Elsevier titles, part 1)
  - E2 `RECHECK/stage1/alt_journal_dates_part2.csv` (10 Elsevier titles, part 2, NEW today; summary
    `RECHECK/stage1/alt_journal_summary_part2.txt`; run logs `journal_selection/v2_evidence/log_*.txt`)
  - E3 `journal_selection/acceptance_scan_articles.csv` (Crossref, 841 journals; summary `acceptance_scan_summary.csv`)
  - E4 `journal_selection/v2_evidence/crossref_extra_dates.csv` (Crossref, 3 new titles, NEW today)
- IF / metrics read from publisher pages: `journal_selection/v2_evidence/springer_journal_pages_2026-11-24.txt`
  (rendered with `scripts/fetch_page.js`). Wiley/IET pages returned a Cloudflare challenge; ScienceDirect blocked.
- APC: OpenAlex source record `apc_usd` (`journal_selection/v2_evidence/openalex_source_metadata.tsv`); a secondary
  source, to be confirmed on the publisher site. "0" for Energy and Built Environment = society-funded OA per OpenAlex.

## Comparison table (sorted by verified median days)

Quartile column: no JCR page was readable, so every quartile is UNVERIFIED. IF given only where a publisher page was
opened today. JCR category = expected category, UNVERIFIED. Data/code policy: no Guide for Authors could be opened
(Elsevier/Wiley blocked); listed as UNVERIFIED unless noted.

| # | Journal | Publisher | ISSN | JCR category (expected, UNVERIFIED) | Quartile | IF (2025 release) | Scope fit | n | Median d | p75 d | Range d | Evidence | APC USD (OpenAlex) | R1 | R2 Q1 | R3 <=72 d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Environmental Systems Research | Springer Nature | 2193-2697 | Environmental Sciences | UNVERIFIED | 5.1 (Springer page, prior check: journal_comparison.md) | Poor: water/air/soil/biota, no energy-system monitoring | 87 | 54 | 72 | 21-290 | E3 | 2690 | PASS | UNVERIFIED (doubtful) | PASS |
| 2 | Energy Informatics | Springer Nature (SpringerOpen) | 2520-8942 | Energy & Fuels / CS-Interdisc. | UNVERIFIED | **none displayed** on journal page (page shows only "submission to first decision 13 days") | Excellent: data analytics, AI for energy systems | 97 | 70 | 86 | 25-368 | E3 | 1490 | PASS | **FAIL/UNVERIFIED** (no JIF shown -> no evidence of JCR ranking) | PASS (12-month subset n=46: 74 -> borderline) |
| 3 | Energy Conversion and Management: X | Elsevier | 2590-1745 | Energy & Fuels; Thermodynamics | UNVERIFIED | UNVERIFIED | Moderate: energy conversion/thermal systems; data-driven FDD evaluation is peripheral | 30 | 73 | 164.75 | 12-254 | E2 | 3170 | PASS | UNVERIFIED | FAIL (by 1 d; 12-month subset n=16: 101.5) |
| 4 | Applied Thermal Engineering | Elsevier | 1359-4311 | Thermodynamics; Energy & Fuels | UNVERIFIED | UNVERIFIED | Weak-moderate: thermal equipment; DH substations borderline, wind SCADA off-scope | 30 | 83 | 99.75 | 49-265 | E2 | 3660 | PASS | UNVERIFIED | FAIL |
| 5 | **Energy and AI** (incumbent) | Elsevier | 2666-5468 | Energy & Fuels; CS-AI | UNVERIFIED | UNVERIFIED | **Excellent**: AI for energy systems; published DH FDD papers (HEAT 2025, STST 2026) | 25 | 89 | 141 | 33-565 | E0 | 3630 | PASS | UNVERIFIED | FAIL (12-month subset n=17: 84) |
| 6 | Building Simulation | Springer Nature / Tsinghua UP | 1996-3599 | Construction & Building Tech.; Thermodynamics | UNVERIFIED | **6.9** (Springer page opened today) | Good: building energy systems, FDD | 100 | 91.5 | 109.25 | 15-209 | E3 | 4090 | PASS | UNVERIFIED | FAIL |
| 7 | Results in Engineering | Elsevier | 2590-1230 | Engineering, Multidisciplinary | UNVERIFIED | UNVERIFIED | Moderate: broad engineering | 25 | 93 | 105 | 11-308 | E1 | 1940 | PASS | UNVERIFIED | FAIL |
| 8 | Building and Environment | Elsevier | 0360-1323 | Construction & Building Tech.; Eng. Civil | UNVERIFIED | UNVERIFIED | Moderate: building environment; DH substations borderline, wind off-scope | 30 | 104.5 | 138.75 | 17-217 | E2 | 4280 | PASS | UNVERIFIED | FAIL |
| 9 | Energy and Buildings | Elsevier | 0378-7788 | Construction & Building Tech.; Energy & Fuels | UNVERIFIED | UNVERIFIED | Very good for DH substations; wind part off-scope | 30 | 122 | 166.25 | 69-619 | E1 | 4260 | PASS | UNVERIFIED | FAIL |
| 10 | Energy | Elsevier | 0360-5442 | Energy & Fuels; Thermodynamics | UNVERIFIED | UNVERIFIED | Very good (published the PreDist benchmark) | 30 | 124 | 189 | 37-312 | E1 | 4260 | PASS | UNVERIFIED | FAIL |
| 11 | Journal of Building Engineering | Elsevier | 2352-7102 | Construction & Building Tech. | UNVERIFIED | UNVERIFIED | Moderate | 26 | 126 | 196 | 46-438 | E2 | 3940 | PASS | UNVERIFIED | FAIL |
| 12 | Smart Energy | Elsevier | 2666-9552 | Energy & Fuels | UNVERIFIED | UNVERIFIED | Very good (DH FDD published) | 10 | 127.5 | 250.25 | 53-332 | E1 | 2750 | PASS | UNVERIFIED | FAIL |
| 13 | Energy Nexus | Elsevier | 2772-4271 | Energy & Fuels | UNVERIFIED | UNVERIFIED | Moderate | 11 | 137 | 221.5 | 82-287 | E2 | 2200 | PASS | UNVERIFIED | FAIL |
| 14 | Energy Strategy Reviews | Elsevier | 2211-467X | Energy & Fuels | UNVERIFIED | UNVERIFIED | Poor (policy/strategy) | 30 | 140 | 270.5 | 51-1140 | E2 | 4180 | PASS | UNVERIFIED | FAIL |
| 15 | Applied Energy | Elsevier | 0306-2619 | Energy & Fuels; Eng. Chemical | UNVERIFIED | UNVERIFIED | Very good | 30 | 149.5 | 187 | 49-416 | E1 | 4430 | PASS | UNVERIFIED | FAIL |
| 16 | Advanced Engineering Informatics | Elsevier | 1474-0346 | CS-AI; Eng. Multidisc. | UNVERIFIED | UNVERIFIED | Good (industrial informatics) | 14 | 150.5 | 187.5 | 24-346 | E1 | 3560 | PASS | UNVERIFIED | FAIL |
| 17 | Journal of Intelligent Manufacturing | Springer Nature | 0956-5515 | CS-AI; Eng. Manufacturing | UNVERIFIED | **7.7** (Springer page opened today) | Weak: manufacturing, not energy systems | 100 | 151 | 217.5 | 49-450 | E3 | 3290 | PASS | UNVERIFIED | FAIL |
| 18 | IET Renewable Power Generation | IET (Wiley-hosted) | 1752-1416 | Energy & Fuels; Eng. Elec. | UNVERIFIED | UNVERIFIED (Cloudflare) | Moderate (wind part only) | 97 | 159 | 214 | 21-795 | E3 | 3500 | PASS | UNVERIFIED | FAIL |
| 19 | Quality and Reliability Engineering International | Wiley | 0748-8017 | Eng. Industrial; OR | UNVERIFIED | UNVERIFIED | Moderate (monitoring/alarm evaluation) | 97 | 169 | 246 | 4-698 | E4 | UNVERIFIED | PASS | UNVERIFIED | FAIL |
| 20 | Expert Systems with Applications | Elsevier | 0957-4174 | CS-AI; OR | UNVERIFIED | UNVERIFIED | Moderate (applied ML) | 30 | 176 | 282 | 31-637 | E2 | 3500 | PASS | UNVERIFIED | FAIL |
| 21 | Reliability Engineering & System Safety | Elsevier | 0951-8320 | Eng. Industrial; OR | UNVERIFIED | UNVERIFIED | Good (reliability/maintenance evaluation) | 30 | 192 | 237.75 | 38-363 | E2 | 4830 | PASS | UNVERIFIED | FAIL |
| 22 | Science and Technology for the Built Environment | T&F | 2374-4731 | Construction & Building Tech.; Thermodynamics | UNVERIFIED | UNVERIFIED | Good (HVAC/DH FDD) | 97 | 193 | 268 | 64-633 | E4 | UNVERIFIED | PASS | UNVERIFIED | FAIL |
| 23 | Wind Energy | Wiley | 1095-4244 | Energy & Fuels; Eng. Mech. | UNVERIFIED | UNVERIFIED (Cloudflare) | Moderate (wind part only) | 84 | 212 | 296 | 84-1032 | E3 | 3730 | PASS | UNVERIFIED | FAIL |
| 24 | Knowledge-Based Systems | Elsevier | 0950-7051 | CS-AI | UNVERIFIED | UNVERIFIED | Moderate (applied ML) | 24 | 249.5 | 359.25 | 57-1068 | E2 | 3430 | PASS | UNVERIFIED | FAIL |
| 25 | IISE Transactions | T&F | 2472-5854 | Eng. Industrial; OR | UNVERIFIED | UNVERIFIED | Moderate | 99 | 326 | 436.5 | 42-1238 | E4 | UNVERIFIED | PASS | UNVERIFIED | FAIL |

Not measurable (fewer than 10 dated articles): Energy and Built Environment (Elsevier; 4 repository PDFs, 1 dated,
83 d) -> R3 UNVERIFIED. Further Springer/Wiley/T&F/IET titles already scanned and failing R3 (Sustainable Energy
Research 74, IET Smart Grid 115, Journal of Building Performance Simulation 127, Complex & Intelligent Systems 143,
Engineering Applications of AI 232, ...) are in `acceptance_scan_summary.csv` and `RECHECK/stage1/alt_journal_summary_partial.md`.

Excluded by R1 before measurement: International Journal of Energy Research (Wiley, run through the Hindawi OA
platform), Journal of Energy / Journal of Renewable Energy / International Journal of Photoenergy (Hindawi), all
MDPI (Energies, Sensors, Buildings ...) and Frontiers titles. IEEE/SAGE/OUP titles (e.g. IEEE TII, IEEE TSTE, Structural
Health Monitoring) deposit no dates in Crossref and could not be measured -> R3 UNVERIFIED, so not tabled.

## Result
- **No candidate meets all three rules.** The only titles with median <= 72 d are Environmental Systems Research
  (off-scope, Q1 doubtful) and Energy Informatics (excellent scope, but no Impact Factor shown on its journal page,
  so no evidence it is JCR-ranked, let alone Q1).
- Closest energy-scope Elsevier titles: ECM: X 73 d (but 101.5 d over the last 12 months), Applied Thermal Engineering
  83 d, Energy and AI 89 d (84 d over the last 12 months). Differences of this size are within sampling noise for
  n = 25-30 (ranges 12-565 d).
- Caveats: survivorship (only published papers), "Received" may be a transfer/revision date, repository PDFs are a
  non-random subset of articles (those with an OA copy), small n for Elsevier titles. Quartiles and most IFs remain
  UNVERIFIED because JCR, ScienceDirect and Wiley pages could not be read.
