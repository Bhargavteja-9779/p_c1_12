"""D6 round 4 (F17): CUSUM alarm logic on the composed score z = score - 1 (M1). Usage: round4_cusum.py METHOD"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from src.data import predist as P
from src.evaluation import continuous as C, runner as R

def cusum(score, k):
    z = np.minimum(score.to_numpy(float) - 1.0, 10.0); S = 0.0; out = np.zeros(len(z))
    for i, x in enumerate(z):
        if x == x:
            S = max(0.0, S + x - k)
        out[i] = S
    return out

meth = sys.argv[1]; H = (2, 5, 10, 20, 40, 80, 120, 200, 300, 500, 800, 1200)
cache = []
for s in P.substations(1):
    sc = R.load_scores(meth, 1, s); cache.append((sc.index, C.substation_labels(1, s, sc.index), sc))
rows = []
for k in (0.0, 1.0, 2.0):
    S = [(idx, lab, cusum(sc, k)) for idx, lab, sc in cache]
    for h in H:
        r = C.summarise([C.evaluate_substation(pd.Series(v >= h, index=idx), lab) for idx, lab, v in S])
        r.update(method=meth + "__cusum", k=k, h=h); rows.append(r)
cur = pd.DataFrame(rows); cur.to_csv(f"results/round4_cusum_{meth}.csv", index=False)
for B in (1, 2, 4):
    ok = cur[cur.fa_per_sub_year <= B].sort_values(["recall", "fa_per_sub_year"], ascending=[False, True])
    print(B, ok.iloc[0][["k", "h", "recall", "fa_per_sub_year", "n_false_alarms"]].to_dict())
for r in (0.214, 0.286, 0.321, 0.357):
    ok = cur[cur.recall >= r - 1e-9]; print("recall", r, "min FA", round(ok.fa_per_sub_year.min(), 2) if len(ok) else None)
