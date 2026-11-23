"""Minimum false-alarm rate needed to reach each recall level (counter grid, M1). Usage: matched_recall.py M1,M2,..."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import pandas as pd
from src.evaluation import runner as R
rows = []
for meth in sys.argv[1].split(","):
    _, cur = R.best_at_budgets(meth, 1)
    for r in (0.107, 0.143, 0.179, 0.214, 0.25, 0.286, 0.321, 0.357):
        ok = cur[cur.recall >= r - 1e-9]
        rows.append(dict(method=meth, recall=r, min_fa=ok.fa_per_sub_year.min() if len(ok) else None))
t = pd.DataFrame(rows).pivot(index="recall", columns="method", values="min_fa")
print(t.round(2).to_string()); t.to_csv(f"results/matched_recall_{sys.argv[2] if len(sys.argv) > 2 else 'latest'}.csv")
