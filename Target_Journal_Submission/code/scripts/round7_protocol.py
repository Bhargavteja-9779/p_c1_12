"""Round 7 (H7a): corrected event protocol E* on PreDist M1. Threshold fixed on calibration random weeks (seed 0)
to a weekly FP rate p* = 1 - exp(-B*7/365.25); evaluated on fault windows + evaluation random weeks (seed s).
No fault event is used to choose thresholds. Usage: round7_protocol.py [eval_seed=1] [n_weeks=500]"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from scipy.stats import kendalltau
from src.data import predist as P
from src.evaluation import continuous as C, runner as R, event_protocol as E
from src.evaluation.runner import TAU_GRID
from src.models import online as O

es = int(sys.argv[1]) if len(sys.argv) > 1 else 1
NW = int(sys.argv[2]) if len(sys.argv) > 2 else 500
m, B = 1, 2
METHODS = ["rule", "sigma3", "loop3s", "iforest", "qnbm", "ae", "ae_cond", "underdel", "srcr_comp__v_gate_1s_local"]
C_GRID = [1, 2, 3, 6, 9, 12, 18, 24, 36, 48, 72, 96, 144, 216, 288]
W = pd.Timedelta(days=7); pstar = 1 - np.exp(-B * 7 / 365.25)
subs = P.substations(m)
labs = {s: C.substation_labels(m, s, R.load_scores("rule", m, s).index) for s in subs}


def weeks(seed, n):
    rng = np.random.default_rng(seed); out = []
    while len(out) < n:
        s = subs[rng.integers(len(subs))]; lab = labs[s]
        a = (lab.start + (lab.end - lab.start) * rng.random()).floor("D"); b = a + W
        if b > lab.end: continue
        bl = lab.exclusions + list(zip(lab.targets.win_start, lab.targets.report))
        if any(a < y and x < b for x, y in bl): continue
        out.append((s, a))
    return out


CAL, EVW = weeks(0, NW), weeks(es, NW)
FW = [(s, r.win_start, r.report) for s in subs for r in labs[s].targets.itertuples()]
T = pd.read_csv("results/m1_table.csv")
rows = []
for meth in METHODS:
    cnt = {}
    for s in subs:
        sc = R.load_scores(meth, m, s)
        cnt[s] = ({t: O.criticality_counter(sc, t) for t in TAU_GRID}, sc.index, sc.notna().values)
    def mx(s, a, b):
        k, idx, ok = cnt[s]; w = (idx >= a) & (idx < b)
        return ({t: (int(k[t][w].max()) if w.any() else 0) for t in TAU_GRID}, ok[w].mean() if w.any() else 0)
    cal = [mx(s, a, a + W) for s, a in CAL]; cal = [x[0] for x in cal if x[1] > 0.5]
    ev = [mx(s, a, a + W) for s, a in EVW]; ev = [x[0] for x in ev if x[1] > 0.5]
    fw = [mx(s, a, b)[0] for s, a, b in FW]
    best = None
    for t in TAU_GRID:
        for c in C_GRID:
            rate = np.mean([x[t] >= c for x in cal])
            if rate <= pstar and (best is None or (rate, -t, -c) > (best[0], -best[1], -best[2])):
                best = (rate, t, c)
    if best is None:   # no grid point reaches p*: recall 0, as in runner.best_at_budgets
        rate, t, c, rec, fpr = np.nan, np.nan, np.nan, 0.0, np.nan
    else:
        rate, t, c = best
        rec = np.mean([x[t] >= c for x in fw]); fpr = np.mean([x[t] >= c for x in ev])
    op = T[(T.method == meth) & (T.budget == 2)].iloc[0]
    rows.append({"method": meth, "tau": t, "c_thr": c, "cal_week_fp": rate, "eval_week_fp": fpr, "Estar_recall": rec,
                 "n_fault_windows": len(fw), "n_eval_weeks": len(ev), "cont_rec_B2": op.recall})
    print(rows[-1], flush=True)
D = pd.DataFrame(rows); os.makedirs("results/round7", exist_ok=True)
D.to_csv(f"results/round7/estar_m1_seed{es}_n{NW}.csv", index=False)
old = pd.read_csv("results/round5/protocol_compare_m1.csv")
kt = kendalltau(D.Estar_recall, D.cont_rec_B2); kto = kendalltau(old.E_best_f05, old.cont_rec_B2)
s = {"kendall_Estar_vs_cont": kt.statistic, "p": kt.pvalue, "kendall_benchmark_vs_cont": kto.statistic, "pstar": pstar,
     "H7a_supported": bool(kt.statistic >= 0.7)}
pd.Series(s).to_csv(f"results/round7/estar_summary_m1_seed{es}_n{NW}.csv"); print(D.round(3).to_string(index=False)); print(s)
