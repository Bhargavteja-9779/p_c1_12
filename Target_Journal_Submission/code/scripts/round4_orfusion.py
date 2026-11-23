"""Round 4 F15 (pre-registered): budget-split OR-fusion of the expert rule with a learned detector on M1.
Each method's operating points (tau, c_thr) are restricted to its own Pareto front on M1 (recall vs FA);
all pairs are evaluated and the best pair at each budget is reported.
Usage: round4_orfusion.py PARTNER[,PARTNER...]"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from src.data import predist as P
from src.evaluation import continuous as C, runner as R
from src.models import online as O

M = 1
BUDGETS = (1, 2, 4)
curves = pd.read_csv("Target_Journal_Submission/code/results/m1_curves.csv" if not os.path.exists("results/m1_curves.csv") else "results/m1_curves.csv")


def pareto(method, fa_max=6.0):
    g = curves[(curves.method == method) & (curves.fa_per_sub_year <= fa_max)].sort_values(["fa_per_sub_year", "recall"], ascending=[True, False])
    out, best = [], -1
    for _, r in g.iterrows():
        if r.recall > best:
            out.append((r.tau, int(r.c_thr))); best = r.recall
    return out


def alarms(method, pts):
    """{(tau,c): {sub: bool Series}}"""
    out = {p: {} for p in pts}
    for s in P.substations(M):
        sc = R.load_scores(method, M, s)
        cnt = {t: O.criticality_counter(sc, t) for t in {p[0] for p in pts}}
        for p in pts:
            out[p][s] = pd.Series(cnt[p[0]] >= p[1], index=sc.index)
    return out


labs = {}
for s in P.substations(M):
    idx = R.load_scores("rule", M, s).index
    labs[s] = C.substation_labels(M, s, idx)

rule_pts = pareto("rule")
A_rule = alarms("rule", rule_pts)
rows = []
for partner in sys.argv[1].split(","):
    pts = pareto(partner)
    A_p = alarms(partner, pts)
    print(partner, "pareto points:", len(rule_pts), "x", len(pts), flush=True)
    for pr in rule_pts:
        for pp in pts:
            res = []
            for s in P.substations(M):
                a = A_rule[pr][s]
                b = A_p[pp][s].reindex(a.index, fill_value=False)
                res.append(C.evaluate_substation(a | b, labs[s]))
            r = C.summarise(res)
            r.update(partner=partner, rule_tau=pr[0], rule_c=pr[1], p_tau=pp[0], p_c=pp[1])
            rows.append(r)
full = pd.DataFrame(rows)
os.makedirs("results/round4", exist_ok=True)
full.to_csv(f"results/round4/orfusion_grid_{sys.argv[1].replace(',', '_')}.csv", index=False)
best = []
for partner, g in full.groupby("partner"):
    for B in BUDGETS:
        ok = g[g.fa_per_sub_year <= B].sort_values(["recall", "fa_per_sub_year"], ascending=[False, True])
        r = ok.iloc[0].to_dict(); r["budget"] = B; best.append(r)
best = pd.DataFrame(best)
best.to_csv(f"results/round4/orfusion_best_{sys.argv[1].replace(',', '_')}.csv", index=False)
print(best[["partner", "budget", "rule_tau", "rule_c", "p_tau", "p_c", "recall", "fa_per_sub_year", "n_false_alarms", "median_lead_h"]].round(3).to_string(index=False))
