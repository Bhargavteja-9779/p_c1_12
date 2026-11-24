# Selected journal v2 (Section 4; 2026-11-24)

| Item | Value |
|---|---|
| TARGET JOURNAL | **Energy and AI** (unchanged from v1) |
| PUBLISHER | Elsevier (gold OA, CC BY) - passes R1 |
| ISSN | 2666-5468 |
| JCR CATEGORY | UNVERIFIED (expected: Energy & Fuels; Computer Science, Artificial Intelligence) |
| QUARTILE | UNVERIFIED (JCR login unavailable; ScienceDirect homepage returns HTTP 403). Proxy only: OpenAlex 2-yr mean citedness 12.71, h-index 78 (`v2_evidence/openalex_source_metadata.tsv`) |
| IMPACT FACTOR | UNVERIFIED |
| RECEIVED -> ACCEPTED | **median 89 d, p75 141 d, range 33-565 d, n = 25** (articles published 2025-07-01..2026-10-24; accepted 2025-06-13..2026-10-20). Last-12-months subset (accepted >= 2025-11-24): median 84 d, range 33-235, n = 17. 36% of the 25 articles were accepted within 72 d. |
| EVIDENCE | `RECHECK/stage1/egyai_dates_from_pdfs.csv` (dates parsed from repository PDFs by `RECHECK/stage1/extract_dates.py`) |
| APC | USD 3,630 (OpenAlex `apc_usd`; confirm on the journal site) - UNVERIFIED at publisher |
| DATA/CODE POLICY | UNVERIFIED (Guide for Authors not reachable); plan a data-availability statement + public code anyway |
| SCOPE FIT | Excellent: AI/data-driven methods for energy systems; publishes district-heating fault-detection work (HEAT 2025, STST 2026) that our protocol critique engages with directly. |

## Rules it fails (stated exactly)
1. **R3 (submission -> final acceptance <= 72 d): FAIL.** Verified median 89 d (n = 25); 84 d over the last 12 months (n = 17).
2. **R2 (JCR Q1): UNVERIFIED** - not shown to fail, but not confirmable from any public page opened here.
R1 (reputable publisher): PASS.

## Why it stays the choice (no journal meets all rules)
- 25 legitimate candidates evaluated (`journal_comparison_v2.md`); none passes R1+R2+R3 with evidence.
- The two titles with median <= 72 d fail on other hard rules: **Energy Informatics** (Springer Nature, median 70 d,
  p75 86, n = 97; 74 d over the last 12 months) shows **no Impact Factor** on its journal page
  (`v2_evidence/springer_journal_pages_2026-11-24.txt`), so it has no evidence of JCR ranking and cannot be called Q1;
  **Environmental Systems Research** (54 d) is off-scope.
- The closest Elsevier energy titles are not clearly faster: **Energy Conversion and Management: X** 73 d (n = 30, p75 165)
  but 101.5 d over the last 12 months (n = 16), and its scope (energy conversion technology) is a weak fit for a
  detector-evaluation study; **Applied Thermal Engineering** 83 d (n = 30, p75 99.75), weak fit (no wind/ML focus).
  The 6-16 d differences to Energy and AI are within sampling noise at n = 25-30, so evidence does not clearly favour
  switching away from the best-fitting journal. Building Simulation (JIF 6.9 verified on its Springer page) is slower
  (91.5 d).
- If the author ranks R2 below R3, the only defensible fast alternative is Energy Informatics (accepting that it has no
  JIF evidence). If R3 must be met at all costs within a Q1-candidate set, no option was found.

## DOIs used for Energy and AI (25; received -> accepted, days)
| DOI | Received | Accepted | Days |
|---|---|---|---|
| 10.1016/j.egyai.2025.100585 | 2025-04-02 | 2025-07-31 | 120 |
| 10.1016/j.egyai.2025.100540 | 2025-02-27 | 2025-06-13 | 106 |
| 10.1016/j.egyai.2025.100547 | 2025-04-03 | 2025-06-21 | 79 |
| 10.1016/j.egyai.2025.100575 | 2025-03-07 | 2025-07-26 | 141 |
| 10.1016/j.egyai.2025.100570 | 2024-12-05 | 2025-07-19 | 226 |
| 10.1016/j.egyai.2025.100637 | 2025-08-14 | 2025-10-24 | 71 |
| 10.1016/j.egyai.2026.100702 | 2025-11-21 | 2026-02-13 | 84 |
| 10.1016/j.egyai.2026.100695 | 2025-06-24 | 2026-02-07 | 228 |
| 10.1016/j.egyai.2026.100729 | 2025-10-06 | 2026-03-23 | 168 |
| 10.1016/j.egyai.2026.100808 | 2026-03-05 | 2026-06-09 | 96 |
| 10.1016/j.egyai.2025.100635 | 2025-06-02 | 2025-10-24 | 144 |
| 10.1016/j.egyai.2025.100641 | 2024-04-10 | 2025-10-27 | 565 |
| 10.1016/j.egyai.2026.100802 | 2025-10-17 | 2026-06-09 | 235 |
| 10.1016/j.egyai.2026.100680 | 2025-09-15 | 2026-01-04 | 111 |
| 10.1016/j.egyai.2026.100768 | 2026-03-30 | 2026-05-02 | 33 |
| 10.1016/j.egyai.2026.100760 | 2026-02-28 | 2026-04-21 | 52 |
| 10.1016/j.egyai.2026.100783 | 2026-02-23 | 2026-05-21 | 87 |
| 10.1016/j.egyai.2026.100791 | 2026-04-03 | 2026-05-26 | 53 |
| 10.1016/j.egyai.2026.100824 | 2026-05-06 | 2026-06-23 | 48 |
| 10.1016/j.egyai.2026.100827 | 2026-05-20 | 2026-06-23 | 34 |
| 10.1016/j.egyai.2026.100899 | 2026-07-02 | 2026-09-05 | 65 |
| 10.1016/j.egyai.2026.100934 | 2026-08-01 | 2026-10-05 | 65 |
| 10.1016/j.egyai.2026.100923 | 2026-08-18 | 2026-09-27 | 40 |
| 10.1016/j.egyai.2026.100921 | 2026-06-30 | 2026-09-27 | 89 |
| 10.1016/j.egyai.2026.100946 | 2026-06-05 | 2026-10-20 | 137 |

DOIs for every alternative are in the per-article evidence files listed in `journal_comparison_v2.md`
(E1 `RECHECK/stage1/alt_journal_dates.csv`, E2 `RECHECK/stage1/alt_journal_dates_part2.csv`,
E3 `journal_selection/acceptance_scan_articles.csv`, E4 `journal_selection/v2_evidence/crossref_extra_dates.csv`).

## Before submission (author)
Open the Energy and AI homepage in a normal browser and record JIF, JCR category/quartile (or Clarivate MJL entry),
APC and the "submission to acceptance" metric; replace the UNVERIFIED cells above.
