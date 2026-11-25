# G8 leak sensitivity — PreDist M1 (written 2026-11-25 ~15:45 UTC, before any leak-free score exists)
Leak (RECHECK stage 5): the legacy exclusion rule treats a fault's exclusion interval as known 7 d after its
"Possible anomaly start", i.e. before the fault is reported. Leak-free rule (as CARE amendment A1): a fault
exclusion is known only at its report date; disturbances and curated known anomalies keep the legacy rule.
Switch: env PREDIST_EXCL_RULE=leakfree (src/evaluation/continuous.py; default legacy = all published numbers).
Affected fits (scripts/leak_affected.py 1 -> results/leak_sensitivity/affected_m1.csv): 4 of 588 retrain points,
substations 4 and 7 only (identical to RECHECK/stage5). M2 is not used (burned).

Procedure: in a scratch copy of code/ (scores of all other substations symlinked unchanged), rescore subs 4 and 7 with
the leak-free rule for every PreDist detector used by plan_v2/plan_v3 (rule, loop3s, qnbm, ae, ae_cond; panel seed 0),
then rerun plan_v2_analysis.py predist1 0 and plan_v3_window_arm.py predist1 unchanged.
Report: every headline quantity (tau_ET/EH/CT, H7a/b diff+CI+p, H7d ratio+CI, H8a-c, CH recall per detector) under
both rules, side by side (results/leak_sensitivity/compare.csv). No hypothesis is re-tested; this is a sensitivity
analysis. Criterion fixed in advance: conclusions are "robust to the leak" if every H7/H8 support verdict is unchanged
and no detector's CH recall changes by more than 1 fault (1/28 = 0.036).
