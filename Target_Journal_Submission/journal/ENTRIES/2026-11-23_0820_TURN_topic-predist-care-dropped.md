RETROSPECTIVE entry reconstructed on 2026-11-24 from PROGRESS.md 'Decisions so far' (commit 3c1504f, 2026-11-23 08:20); not written at the time.

# Topic: PreDist chosen, CARE dropped

We dropped the CARE wind-turbine benchmark as a topic. The note gives the reason: "63 citing works, >=4 already do
conformal/drift-aware calibration -> incremental".

We took PreDist instead (Zenodo 19496480, CC-BY-4.0): 93 district-heating substations, 2 manufacturers, 73 faults,
55 efd_possible, 65 normal events. We noted these gaps in the baseline paper (arXiv 2511.14791):
- AE normal-behaviour model on hand-picked training windows;
- tuned on test events;
- balanced 50/50 evaluation;
- no continuous-monitoring false-alarm rate.

CARE came back later: practical-sagan pre-registered it as a second dataset (Round 6), see the escalation log.
