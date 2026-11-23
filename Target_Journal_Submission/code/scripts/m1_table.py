"""M1 development table: best recall at FA budgets (10-min criticality counter, shared tau/c grid) + FA at
matched recall, for all methods with complete score sets."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import pandas as pd
from src.data import predist as P
from src.evaluation import runner as R
methods = sys.argv[1].split(",")
rows, curves = [], []
for m in methods:
    if len(os.listdir(R.score_path(m, 1))) < len(P.substations(1)):
        print("incomplete", m); continue
    t, c = R.best_at_budgets(m, 1); c["method"] = m
    rows.append(t); curves.append(c)
    print(t[["method", "budget", "tau", "c_thr", "recall", "fa_per_sub_year", "median_lead_h"]].round(3).to_string(index=False, header=False), flush=True)
pd.concat(rows).to_csv("results/m1_table.csv", index=False)
C = pd.concat(curves)
C.to_csv("results/m1_curves.csv", index=False)
out = []
for r in (0.143, 0.214, 0.286, 0.321):
    for m, g in C.groupby("method"):
        ok = g[g.recall >= r - 1e-9]
        out.append({"method": m, "recall_target": r, "min_fa_per_sub_year": ok.fa_per_sub_year.min() if len(ok) else float("nan")})
print(pd.DataFrame(out).pivot(index="method", columns="recall_target", values="min_fa_per_sub_year").round(2))
