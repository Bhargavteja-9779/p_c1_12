# Journal verification: method, evidence and limitations (STEP 0, 2026-11-23)

## How acceptance time was measured
1. Candidate pool: OpenAlex sources hosted by Springer Nature, Taylor & Francis, Wiley (incl. Hindawi) and
   IET with 2-year mean citedness > 4 (a proxy for Impact Factor; NOT a JCR value): 2,212 journals.
   Scope keyword filter (computing, AI, data, engineering, energy, environment, health informatics, ...) -> 814,
   plus 51 hand-picked energy/buildings/AI journals (`handpicked_candidates.csv`). Scripts: `scripts/`.
2. For each journal, Crossref returned a RANDOM sample (`sample=100`) of research articles published from
   2025-05-23 to 2026-11-23 (18 months). Received and Accepted dates were read from the publisher-deposited
   "Article History" (Crossref `assertion` fields). Days = accepted - received.
3. 841 journals scanned; 637 had >= 20 dated articles. Per-journal median, p75, p90, max in
   `acceptance_scan_summary.csv`; all 57,051 article rows in `acceptance_scan_articles.csv`;
   shortlist article rows in `acceptance_time_evidence.csv`.
4. PASS rule (from the brief): median well under 72 d AND p75 <= 72 d.

## Limitations (stated honestly)
- Survivorship: only accepted, published papers are visible; rejected papers and withdrawn papers are unseen.
- "Received" may be the date of the original OR of a transferred submission; some publishers reset it after
  major revision. Days can therefore under-state the true submission-to-acceptance time.
- Elsevier, IEEE, SAGE, OUP do not deposit these dates in Crossref, and ScienceDirect pages are blocked from
  this environment (HTTP 403; browser-based retrieval was not permitted). Their acceptance times are UNVERIFIED.
- JCR (Clarivate) requires a subscription login; quartiles could not be read. Impact Factors were read from
  publisher journal pages where shown (Springer pages display the JIF released in 2025). Everything else
  is marked UNVERIFIED.

## Result
- Journals that strictly PASS the 72-day rule: Current Reviews in Musculoskeletal Medicine (clinical reviews;
  off-scope), Asian Journal of Civil Engineering (median 36.5, p75 69.25; no JIF shown on its Springer page),
  Environmental Systems Research (median 54, p75 72.0 exactly; JIF 5.1 (2025); scope = water/air/soil/biota).
- No energy-systems, building-energy or AI/data-science journal at a measurable publisher passes. Fastest
  energy-scope journal: Energy Informatics (median 70, p75 86; no JIF displayed -> likely not JCR-ranked).
  Building Simulation: JIF 6.9 (2025), median 91.5, p75 109. Most Q1-level energy/AI journals: 110-240 d median.
- Conclusion: for the feasible research domain (data-driven monitoring of energy systems on public data), the
  combination {JCR Q1, high IF, scope fit, verified p75 <= 72 d} is not attainable from the available evidence.
  Following the brief, the strongest defensible Q1 journal with excellent scope fit is selected and the unmet /
  unverifiable rule is stated (see selected_journal.md).
