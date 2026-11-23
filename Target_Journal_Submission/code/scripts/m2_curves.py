"""Curve-level secondary endpoint (protocol v1/A1): normalised area under the best-recall-at-FA<=x step curve for
x in [0, 6] FA/sub-yr, per manufacturer, each method over the shared (tau, c_thr) grid; C2 over the M1 Pareto
pairs (rule x AE seed 0). Descriptive (the curve is optimised within each manufacturer)."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from src.data import predist as P
from src.evaluation import continuous as C, runner as R
from src.models import online as O

XMAX = 6.0
METHODS = ["rule", "sigma3", "loop3s", "iforest", "qnbm", "ae", "ae_cond", "srcr_comp__v_gate_1s_local"]
M1C = pd.read_csv("results/m1_curves.csv")


def area(curve: pd.DataFrame) -> float:
    xs = np.linspace(0, XMAX, 601)
    best = [curve.loc[curve.fa_per_sub_year <= x, "recall"].max() if (curve.fa_per_sub_year <= x).any() else 0.0 for x in xs]
    return float(np.trapezoid(best, xs) / XMAX)


def pareto_pts(method):
    g = M1C[(M1C.method == method) & (M1C.fa_per_sub_year <= XMAX)].sort_values(["fa_per_sub_year", "recall"], ascending=[True, False])
    out, b = [], -1
    for _, r in g.iterrows():
        if r.recall > b:
            out.append((r.tau, int(r.c_thr))); b = r.recall
    return out


rows = []
for m in (1, 2):
    curves = {}
    for meth in METHODS:
        _, c = R.best_at_budgets(meth, m)
        curves[meth] = c
        rows.append({"m": m, "method": meth, "auc_0_6": area(c)})
    # C2 pair grid (rule x AE seed 0 Pareto points of M1)
    pr, pa = pareto_pts("rule"), pareto_pts("ae")
    al = {}
    for meth, pts in (("rule", pr), ("ae", pa)):
        for s in P.substations(m):
            sc = R.load_scores(meth, m, s)
            for t in {p[0] for p in pts}:
                k = O.criticality_counter(sc, t)
                for p in pts:
                    if p[0] == t:
                        al[(meth, p, s)] = pd.Series(k >= p[1], index=sc.index)
    cr = []
    for p1 in pr:
        for p2 in pa:
            res = []
            for s in P.substations(m):
                a = al[("rule", p1, s)]
                res.append(C.evaluate_substation(a | al[("ae", p2, s)].reindex(a.index, fill_value=False),
                                                 C.substation_labels(m, s, a.index)))
            cr.append(C.summarise(res))
    rows.append({"m": m, "method": "C2_rule_or_ae", "auc_0_6": area(pd.DataFrame(cr))})
    print(pd.DataFrame(rows).round(3).to_string(index=False), flush=True)
os.makedirs("results/m2", exist_ok=True)
pd.DataFrame(rows).to_csv("results/m2/curve_auc.csv", index=False)
