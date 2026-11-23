"""Threshold-free paired comparison of two methods over the same target faults (M1): per-fault rank_frac of
the best pre-report day among normal substation-days (diagnose.fault_ranks, agg=mean6h). Wilcoxon signed-rank
on log10(rank_frac) and sign counts. Usage: paired_ranks.py A B [A2,B2 ...]"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from scipy.stats import wilcoxon
from src.evaluation.diagnose import fault_ranks
cache = {}
def ranks(m):
    if m not in cache: cache[m] = fault_ranks(m, 1)[0].set_index("event_id")["rank_frac"]
    return cache[m]
rows = []
for pair in sys.argv[1:]:
    a, b = pair.split(",")
    ra, rb = ranks(a), ranks(b)
    la, lb = np.log10(ra.clip(lower=1e-5)), np.log10(rb.clip(lower=1e-5))
    d = la - lb
    p = wilcoxon(d[d != 0]).pvalue if (d != 0).sum() > 0 else 1.0
    rows.append(dict(a=a, b=b, n=len(d), a_better=int((d < 0).sum()), b_better=int((d > 0).sum()),
                     median_rank_a=ra.median(), median_rank_b=rb.median(), a_top2pct=int((ra <= .02).sum()),
                     b_top2pct=int((rb <= .02).sum()), wilcoxon_p=p))
t = pd.DataFrame(rows); print(t.round(4).to_string(index=False))
t.to_csv("results/paired_ranks_latest.csv", index=False)
