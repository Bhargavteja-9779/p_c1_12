# Resume instructions (read first)

This repo holds an autonomous research project (full brief: `Target_Journal_Submission/BRIEF.md`).

When the user says "continue":
1. Read `Target_Journal_Submission/PROGRESS.md`. Its "NEXT ACTION" section says exactly what to do next.
2. Continue from there. Do not restart finished phases.
3. After EVERY meaningful step: update PROGRESS.md, `git add -A && git commit`, and push to the
   session's own branch. Each new session gets a new claude/* branch: FIRST run `git fetch origin` and
   fast-forward onto the remote claude/* branch with the newest commit (history so far: wizardly-babbage-182x46
   -> stoic-carson-8teuw3 -> youthful-meitner-qelzen). The user may switch accounts at any time.
4. Integrity rules in BRIEF.md are absolute (no fabricated results, citations or journal data; mark UNVERIFIED).

Environment notes: CPU only (4 cores, 15 GB RAM). Crossref, OpenAlex, arXiv, UCI, Zenodo and PyPI reachable.
ScienceDirect pages blocked (403). JCR needs login, so IF/quartile = UNVERIFIED unless found on a public page.
Crossref `assertion` fields hold received/accepted dates for Springer Nature, T&F, Wiley/Hindawi, IET
(not Elsevier, IEEE, SAGE, OUP).
