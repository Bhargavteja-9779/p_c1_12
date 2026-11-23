# PROGRESS

## Current phase
STEP 0: journal landscape and 72-day check (in progress)

## Decisions so far (with reasons)
- 2026-11-23: Acceptance time is measured from Crossref received/accepted dates (all articles of the last
  ~18 months, not only 20). Only publishers that deposit those dates can PASS the 72-day check:
  Springer Nature, Taylor & Francis, Wiley/Hindawi, IET. Elsevier/IEEE/SAGE/OUP = UNVERIFIED (risk).
- Compute is CPU-only, so the topic must be feasible with classical ML / small neural nets on public data.

## NEXT ACTION
1. Build candidate journal list from OpenAlex (`journal_selection/scripts/oa_list.py`; the `topics`
   select or `works_count` filter gave HTTP 401, so simplify the query).
2. Compute received-to-accepted stats per ISSN from Crossref -> acceptance_time_evidence.csv.
