"""F19 protocol-gap analysis (pre-registered, novelty_escalation_log.md round 5). Usage: protocol_gap.py M
Event protocol (dataset benchmark style) vs continuous protocol, same scores and alarm logic.
Writes results/protocol_gap/m{M}_event_curves.csv, m{M}_gap.csv, m{M}_rank.json."""
import sys, os, json; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from scipy.stats import spearmanr
from src.data import predist as P
from src.evaluation import continuous as C, runner as R
from src.models import online as O

M = int(sys.argv[1])
METHODS = ["rule", "sigma3", "loop3s", "iforest", "qnbm", "ae", "ae_cond", "srcr_comp__v_gate_1s_local"]
C_GRID = [1, 2, 3, 6, 9, 12, 18, 24, 36, 48, 72, 96, 144, 216, 288]
OUT = "results/protocol_gap"; os.makedirs(OUT, exist_ok=True)
W = pd.Timedelta(days=C.WINDOW_DAYS)


def events(m):
    F = P.faults(m); F = F[F.efd_possible == True]
    ev = [(r["sub"], f"f{r['Event ID']}", r["Report date"] - W, r["Report date"], 1) for _, r in F.iterrows()]
    N = P.normal_events(m)
    ev += [(r["sub"], f"n{r['Event ID']}", r["Event start"], r["Event end"], 0) for _, r in N.iterrows()]
    return pd.DataFrame(ev, columns=["sub", "eid", "a", "b", "fault"])


def f05(p, r):
    return 1.25 * p * r / (0.25 * p + r) if (p + r) > 0 else 0.0


def event_curve(method, m, taus):
    E = events(m); rows = []
    flags = {(t, c): [] for t in taus for c in C_GRID}
    keep = []
    for s, g in E.groupby("sub"):
        try:
            sc = R.load_scores(method, m, s)
        except FileNotFoundError:
            continue
        cnt = {t: O.criticality_counter(sc, t) for t in taus}
        for _, e in g.iterrows():
            w = (sc.index >= e.a) & (sc.index < e.b)
            if not w.any() or np.isnan(sc.values[w]).all():
                continue  # no score in window -> not evaluable
            keep.append((e.eid, e.fault))
            for t in taus:
                mx = cnt[t][w].max()
                for c in C_GRID:
                    flags[(t, c)].append(mx >= c)
    y = np.array([k[1] for k in keep], bool)
    for (t, c), f in flags.items():
        f = np.array(f, bool)
        tp, fp = (f & y).sum(), (f & ~y).sum()
        p = tp / (tp + fp) if tp + fp else 0.0; r = tp / y.sum()
        rows.append({"method": method, "tau": t, "c_thr": c, "ev_precision": p, "ev_recall": r, "ev_f05": f05(p, r),
                     "n_fault_ev": int(y.sum()), "n_normal_ev": int((~y).sum())})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    ev_rows, gap, cont_best = [], [], {}
    for meth in METHODS:
        ec = event_curve(meth, M, R.TAU_GRID); ev_rows.append(ec)
        _, cc = R.best_at_budgets(meth, M)  # continuous curve over the same grid
        best = ec.sort_values(["ev_f05", "ev_recall"], ascending=False).iloc[0]
        c = cc[(cc.tau == best.tau) & (cc.c_thr == best.c_thr)].iloc[0]
        ok = cc[cc.fa_per_sub_year <= 2]
        cont_best[meth] = ok.recall.max() if len(ok) else 0.0
        gap.append({"method": meth, "tau": best.tau, "c_thr": int(best.c_thr), "ev_f05": best.ev_f05,
                    "ev_precision": best.ev_precision, "ev_recall": best.ev_recall,
                    "cont_recall": c.recall, "cont_fa_per_sub_year": c.fa_per_sub_year,
                    "cont_alarm_precision": c.alarm_precision,
                    "precision_ratio": best.ev_precision / c.alarm_precision if c.alarm_precision > 0 else np.inf,
                    "cont_recall_at_B2": cont_best[meth]})
        print(pd.DataFrame(gap[-1:]).round(3).to_string(index=False, header=len(gap) == 1), flush=True)
    pd.concat(ev_rows).to_csv(f"{OUT}/m{M}_event_curves.csv", index=False)
    G = pd.DataFrame(gap); G.to_csv(f"{OUT}/m{M}_gap.csv", index=False)
    rho, p = spearmanr(G.ev_f05, G.cont_recall_at_B2)
    res = {"spearman_rho": rho, "p": p, "n_methods": len(G),
           "H5f_n_methods_over_4FA": int((G.cont_fa_per_sub_year > 4).sum()),
           "H5g_min_precision_ratio": float(G.precision_ratio.min())}
    json.dump(res, open(f"{OUT}/m{M}_rank.json", "w"), indent=1)
    print(res)
