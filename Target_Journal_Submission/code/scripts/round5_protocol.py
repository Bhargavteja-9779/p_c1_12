"""Round 5 (pre-registered H5a-c): balanced event protocol vs continuous protocol on M1, same scores.
Usage: round5_protocol.py [m]   (m = 1 development; m = 2 only inside the locked evaluation)"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from scipy.stats import kendalltau, spearmanr
from src.evaluation import event_protocol as E
from src.evaluation.runner import TAU_GRID

m = int(sys.argv[1]) if len(sys.argv) > 1 else 1
METHODS = ["rule", "sigma3", "loop3s", "iforest", "qnbm", "ae", "ae_cond", "underdel", "srcr_comp__v_gate_1s_local"]
C_GRID = [1, 2, 3, 6, 9, 12, 18, 24, 36, 48, 72, 96, 144, 216, 288]
OUT = f"results/round5"; os.makedirs(OUT, exist_ok=True)
T = pd.read_csv("results/m1_table.csv")
rows, grids = [], []
for meth in METHODS:
    mc = E.max_counter_per_event(meth, m, TAU_GRID)
    g = E.grid(mc, C_GRID); g["method"] = meth; grids.append(g)
    best = g.sort_values(["f05", "recall"], ascending=False).iloc[0]
    op = T[(T.method == meth) & (T.budget == 2)].iloc[0]
    g2 = g[(g.tau == op.tau) & (g.c_thr == op.c_thr)].iloc[0]
    rows.append({"method": meth, "E_best_f05": best.f05, "E_best_prec": best.precision, "E_best_rec": best.recall,
                 "E_best_tau": best.tau, "E_best_c": best.c_thr,
                 "E_atB2_f05": g2.f05, "E_atB2_prec": g2.precision, "E_atB2_rec": g2.recall,
                 "cont_rec_B2": op.recall, "cont_fa_B2": op.fa_per_sub_year, "cont_prec_B2": op.alarm_precision,
                 "n_events": len(mc) // len(TAU_GRID), "n_fault_events": int(mc[mc.tau == TAU_GRID[0]].y.sum()),
                 "mean_coverage": mc.coverage.mean()})
    print(rows[-1], flush=True)
R = pd.DataFrame(rows)
R["prec_inflation"] = R.E_best_prec / R.cont_prec_B2
R.to_csv(f"{OUT}/protocol_compare_m{m}.csv", index=False)
pd.concat(grids).to_csv(f"{OUT}/event_grid_m{m}.csv", index=False)
kt = kendalltau(R.E_best_f05, R.cont_rec_B2); sp = spearmanr(R.E_best_f05, R.cont_rec_B2)
kt2 = kendalltau(R.E_atB2_f05, R.cont_rec_B2)
rule = R[R.method == "rule"].iloc[0]
inv = R[(R.method != "rule") & (R.E_best_f05 > rule.E_best_f05) & (R.cont_rec_B2 < rule.cont_rec_B2)].method.tolist()
summ = {"kendall_tau_Ebest_vs_contB2": kt.statistic, "kendall_p": kt.pvalue, "spearman": sp.statistic,
        "kendall_tau_EatB2_vs_contB2": kt2.statistic,
        "H5a_supported": bool(kt.statistic < 0.5), "H5b_inverted_methods": ";".join(inv), "H5b_supported": len(inv) > 0,
        "H5c_min_inflation": R.prec_inflation.min(), "H5c_supported": bool((R.prec_inflation >= 5).all())}
pd.Series(summ).to_csv(f"{OUT}/protocol_summary_m{m}.csv")
print(R.round(3).to_string(index=False)); print(summ)
