# Where every number in manuscript.md comes from (paths relative to Target_Journal_Submission/code/)

| Number(s) | Source file |
|---|---|
| ET / CH per detector (Table 2, Fig. 2); PreDist CH fault counts 2–9, CARE 0–12 | results/leak_sensitivity/leakfree_outputs/seed0/cells.csv; results/plan_v2/care/seed0/cells.csv |
| τ ET/EH/CT 0.34/0.65/0.83 (PreDist leak-free), 0.18/0.63/0.83 (legacy), 0.43/0.74/0.30 (CARE) | .../leakfree_outputs/seed0/summary.json; results/plan_v2/predist1/seed0/summary.json; results/plan_v2/care/seed0/summary.json |
| Pre-registered p, Holm decisions | results/plan_v2/summary.md, summary.json; leak-free p: leakfree_outputs/seed0/summary.json |
| T1 / T2 p-values (Table 3), A1 verdict | results/plan_v2/amendment_A1/tests.csv, summary.json (pre-registered in experiments/plan_v2_amendment_A1.md, commit 324f9e9) |
| Seed robustness, EH > ET in all seeds (Fig. 4) | results/plan_v2/{predist1,care}/seed{0..4}/summary.json |
| Selection ratio 0.21 (0.05–0.37), 0.30 (0.11–0.52), 0.42 (0.27–0.61); 16/17, 13/14; per detector (Fig. 3) | summary.json files above; selection_per_detector.csv |
| CARE 6.7–16.7 FA/turbine-yr, inflation 7.6 (5.0–16.7) to 20.6 (13.5–37.4), precision 0.55–0.84 vs 0.036–0.071 | results/round6/seed0/ (Round 6, pre-registered; table in experiments/novelty_escalation_log.md "Round 6 RESULTS") |
| PreDist 83–176 FA days/sub-yr (median 135), macro F1 0.50–0.53, 45,632 / 221 / 442 days | .../leakfree_outputs/seed0/window_arm.csv, plan_v3_summary.json |
| Power 0.23 (PreDist), 0.12 / 0.35 (CARE, 14.9 d) | experiments/novelty_escalation_log.md (H5e, H6d) |
| Leak: 4/588 refits, subs 4 and 7; lof_pca CH changes by 4/28 | results/leak_sensitivity/affected_m1.csv, compare.csv, verdict.json |
| Dataset sizes (35 substations, 144 sub-yr, 29 faults, 35 normal events; 36 turbines, 95 events, 45 anomalies) | results/dataset_summary.md; plan_v2 summary.json (n_assets, n_events, n_fault_events) |
| References [1]–[34] | submission/references_crossref.txt (Crossref API; [7] DataCite), built by DOI on 2026-11-25 |

## Added in version 2 (2026-11-28)
| Number(s) | Source file |
|---|---|
| Benchmark-winner deployment ranks (15/12/13/3/2 PreDist leak-free; 4/4/4/4/7 CARE), outside top-3 at 60-100% of budgets, realised FA medians (0.33/0.82/1.66; 1.84/1.84/2.20), expert rule 0.29 at B <= 4 | code/results/plan_v2/amendment_A2/{predist1_leakfree,care_primary,predist1_legacy}_seed*.json and *_cells.csv |
| tau(ET,CHA) CARE -0.06..0.12, PreDist 0.43 (legacy 0.30-0.49); A2 p-values; LOFO counts | same A2 JSON files |
| Leak-free T1/T2 (0.060/0.18; 0.007/0.092) | code/results/plan_v2/amendment_A1/tests.csv, summary.json (re-run 2026-11-28 with leak-free bootstrap) |
| Leak-free seeds 2-3 H7d ratios 0.18-0.23 | code/results/leak_sensitivity/leakfree_outputs/seed{2,3}/summary.json |
| Alarm-rate guidance (EEMUA via [35], YA-711 via [36]); review [37] | literature/prior_art_recheck_2026-11-28.md; Crossref-verified in references_crossref.txt |
| Fig. 1 (schematic), Fig. 5 (budget curves) | scripts/make_fig1_schematic.py; scripts/make_fig_operator_curves.py leakfree |
