# PROGRESS

## Current phase
STEP 0: journal landscape and 72-day check (in progress)

## Decisions so far (with reasons)
- 2026-11-23: Acceptance time is measured from Crossref received/accepted dates (all articles of the last
  ~18 months, not only 20). Only publishers that deposit those dates can PASS the 72-day check:
  Springer Nature, Taylor & Francis, Wiley/Hindawi, IET. Elsevier/IEEE/SAGE/OUP = UNVERIFIED (risk).
- Compute is CPU-only, so the topic must be feasible with classical ML / small neural nets on public data.

- OpenAlex: cursor paging needs API key; page= paging works. 2212 journals (cit2y>4) -> 814 after scope keyword
  filter (`candidates_filtered.csv`).
- Springer journal pages (link.springer.com/journal/<id>) show JCR IF + median first-decision days when rendered
  with headless Chromium (`scripts/fetch_page.js`, run with NODE_PATH=$(npm root -g)). T&F/Wiley pages 403.

## NEXT ACTION
1. `scripts/acceptance_scan.py candidates_filtered.csv` (resumable; appends to acceptance_scan_summary.csv).
   If it was interrupted, rerun it from journal_selection/; it skips finished ISSNs.
2. Filter: median well < 72 and p75 <= 72, n_dated >= 20; check scope/IF; pick journal.
