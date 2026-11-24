# Resume instructions (read first)

This repo holds an autonomous research project. project/ = `Target_Journal_Submission/`.

On ANY start or when the user says "continue" / "try again":
1. Read `Target_Journal_Submission/HANDOFF.md` (NEXT ACTION), `Target_Journal_Submission/USER_DIRECTIVES.md`
   (standing user instructions: keep improving with new methods until top-notch; never ask permission; never stop
   at "good enough") and `Target_Journal_Submission/MASTER_PROMPT.md` (rules, gates, loop).
2. `git fetch origin`; work on the newest `claude/*` branch that contains all others (HANDOFF.md names it; merge if
   branches diverged). Run `python3 Target_Journal_Submission/scripts/status.py`; if the heartbeat is stale or tmux
   "queue" is missing, restart the queue (HANDOFF.md "Resume compute") before anything else.
3. Continue from NEXT ACTION. Do not restart finished work. Do not ask the user questions.
4. After EVERY meaningful step: update HANDOFF.md + state/, `git add -A && git commit`, push to the session branch.
5. Integrity rules (MASTER_PROMPT.md Section 1) are absolute: no fabricated results, citations or journal data;
   mark UNVERIFIED; the M2 test set is burned (state/decisions.md D-03).

Environment notes: CPU only (4 cores, ~15 GB RAM; CARE farm-C AE fits need ~6 GB -> queue --workers 2).
Worker restarts kill all processes: always check the heartbeat on wake-up. Crossref, OpenAlex, arXiv, Zenodo, PyPI
reachable; ScienceDirect 403; JCR needs login (IF/quartile = UNVERIFIED unless on a public page).
