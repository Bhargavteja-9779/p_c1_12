"""Round 8 (H8a-c): recall at an alarm-DAYS budget on M1, same grid; compare rankings."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from scipy.stats import kendalltau
from src.evaluation import runner as R
METHODS = ["rule", "sigma3", "loop3s", "iforest", "qnbm", "ae", "ae_cond", "underdel", "srcr_comp__v_gate_1s_local"]
os.makedirs("results/round8", exist_ok=True); rows = []; curves = []
for m in METHODS:
    cv = pd.concat([R.operating_curve(m, 1, taus=(t,)) for t in R.TAU_GRID], ignore_index=True); cv["method"] = m; curves.append(cv)
    for D in (4, 8, 16):
        ok = cv[cv.alarm_days_per_sub_year <= D].sort_values(["recall", "alarm_days_per_sub_year"], ascending=[False, True])
        r = ok.iloc[0].to_dict() if len(ok) else {"recall": 0.0}
        r.update(method=m, D=D); rows.append(r)
    print(m, [round(x["recall"], 3) for x in rows[-3:]], flush=True)
T = pd.DataFrame(rows); T.to_csv("results/round8/burden_days_m1.csv", index=False)
pd.concat(curves).to_csv("results/round8/curves_m1.csv", index=False)
S = pd.read_csv("results/m1_table.csv"); S = S[(S.budget == 2) & S.method.isin(METHODS)].set_index("method").recall
d8 = T[T.D == 8].set_index("method").recall
E7 = pd.read_csv("results/round7/estar_m1_seed1_n500.csv").set_index("method").Estar_recall
top = d8.max()
s = {"H8a_rule_recall_D8": d8["rule"], "H8a_top_D8": top, "H8a_supported": bool(d8["rule"] >= top),
     "kendall_start_vs_day": kendalltau(S[METHODS], d8[METHODS]).statistic, "H8b_supported": bool(kendalltau(S[METHODS], d8[METHODS]).statistic >= 0.5),
     "kendall_Estar_vs_day": kendalltau(E7[METHODS], d8[METHODS]).statistic, "H8c_supported": bool(kendalltau(E7[METHODS], d8[METHODS]).statistic >= 0.6)}
pd.Series(s).to_csv("results/round8/summary_m1.csv")
print(T[["method", "D", "recall", "fa_per_sub_year", "alarm_days_per_sub_year", "tau", "c_thr"]].round(3).to_string(index=False)); print(s)
