"""Round 6 (pre-registered H6a-d): continuous vs balanced-event protocol on CARE wind SCADA.
Leave-one-farm-out (LOFO) operating points; event protocol on all CARE events; selection test; resolution."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from scipy.stats import kendalltau, spearmanr, binom, beta
from src.data import care
from src.evaluation import continuous as C, care_eval as CE, event_protocol as EP
from src.evaluation.runner import TAU_GRID
from src.models import online as O

METHODS = [m for m in ["temp3s", "sigma3", "iforest", "ae", "ae_cond"] if len(sys.argv) < 2 or m in sys.argv[1].split(",")]
C_GRID = [1, 2, 3, 6, 9, 12, 18, 24, 36, 48, 72, 96, 144, 216, 288]
BUDGETS = (1, 2, 4)
OUT = "results/round6"; os.makedirs(OUT, exist_ok=True)
ASSETS = [(f, a) for f in care.FARMS for a in care.assets(f)]
rng = np.random.default_rng(0)


def per_asset(meth):
    """dict (f,a) -> (counter per tau, index, labels, score)"""
    d = {}
    for f, a in ASSETS:
        sc = CE.load_scores(meth, f, a); lab = CE.labels(f, a, sc.index)
        d[(f, a)] = ({t: O.criticality_counter(sc, t) for t in TAU_GRID}, sc.index, lab, sc)
    return d


def curve(D):
    """per (tau, c, asset) evaluation results"""
    R = {}
    for (f, a), (cnt, idx, lab, _) in D.items():
        for t in TAU_GRID:
            for c in C_GRID:
                R[(t, c, f, a)] = C.evaluate_substation(pd.Series(cnt[t] >= c, index=idx), lab)
    return R


def summ(R, t, c, keys):
    return C.summarise([R[(t, c, f, a)] for f, a in keys])


def choose(R, keys, B):
    best = None
    for t in TAU_GRID:
        for c in C_GRID:
            s = summ(R, t, c, keys)
            if s["fa_per_sub_year"] <= B and (best is None or (s["recall"], -s["fa_per_sub_year"]) > (best[0]["recall"], -best[0]["fa_per_sub_year"])):
                best = (s, t, c)
    return best


def event_windows():
    rows = []
    for f in care.FARMS:
        E = care.events(f)
        for r in E.itertuples():
            rows.append({"farm": f, "asset": r.asset, "event_id": r.event_id, "start": r.event_start, "end": r.event_end,
                         "y": int(r.event_label == "anomaly")})
    return pd.DataFrame(rows)


EV = event_windows()
cont_rows, lofo_ops, ev_rows, sel_rows = [], {}, [], []
for meth in METHODS:
    D = per_asset(meth); R = curve(D)
    allkeys = list(D)
    # in-sample and LOFO operating points
    for B in BUDGETS:
        s, t, c = choose(R, allkeys, B) or ({"recall": 0.0}, None, None)
        cont_rows.append({"method": meth, "budget": B, "mode": "in_sample", "tau": t, "c_thr": c, **s})
        res, ops = [], {}
        for hold in care.FARMS:
            tr = [k for k in allkeys if k[0] != hold]; te = [k for k in allkeys if k[0] == hold]
            ch = choose(R, tr, B)
            t2, c2 = (ch[1], ch[2]) if ch else (TAU_GRID[-1], C_GRID[-1])
            ops[hold] = (t2, c2); res += [R[(t2, c2, f, a)] for f, a in te]
        lofo_ops[(meth, B)] = ops
        cont_rows.append({"method": meth, "budget": B, "mode": "lofo", "tau": str(ops), "c_thr": None, **C.summarise(res)})
    # event protocol
    mx = []
    for e in EV.itertuples():
        cnt, idx, lab, sc = D[(e.farm, e.asset)]
        w = (idx >= e.start) & (idx < e.end)
        mx.append({t: int(cnt[t][w].max()) if w.any() else 0 for t in TAU_GRID} | {"cov": float(sc[w].notna().mean()) if w.any() else 0.0})
    M = pd.DataFrame(mx)
    g = [dict(EP.metrics((M[t].values >= c).astype(int), EV.y.values), tau=t, c_thr=c) for t in TAU_GRID for c in C_GRID]
    G = pd.DataFrame(g); best = G.sort_values(["f05", "recall"], ascending=False).iloc[0]
    # at LOFO B=2 points (farm-specific)
    ops = lofo_ops[(meth, 2)]
    pred = np.array([int(M.loc[i, ops[e.farm][0]] >= ops[e.farm][1]) for i, e in enumerate(EV.itertuples())])
    atb2 = EP.metrics(pred, EV.y.values)
    lo = [r for r in cont_rows if r["method"] == meth and r["budget"] == 2 and r["mode"] == "lofo"][0]
    ev_rows.append({"method": meth, "E_best_f05": best.f05, "E_best_prec": best.precision, "E_best_rec": best.recall,
                    "E_atB2_f05": atb2["f05"], "E_atB2_prec": atb2["precision"], "E_atB2_rec": atb2["recall"],
                    "cont_rec_B2": lo["recall"], "cont_fa_B2": lo["fa_per_sub_year"], "cont_prec_B2": lo["alarm_precision"],
                    "n_events": len(EV), "n_anomaly": int(EV.y.sum()), "mean_cov": M["cov"].mean()})
    # selection test at LOFO B=2 points: normal events vs random eligible windows of the same length distribution
    NE = EV[EV.y == 0]; lens = (NE.end - NE.start).values
    def hit(f, a, s0, s1):
        cnt, idx, lab, sc = D[(f, a)]; t, c = ops[f]; w = (idx >= s0) & (idx < s1)
        return (bool((cnt[t][w] >= c).any()), float(sc[w].notna().mean()) if w.any() else 0.0)
    for e in NE.itertuples():
        h = hit(e.farm, e.asset, e.start, e.end); sel_rows.append({"method": meth, "kind": "normal_event", "farm": e.farm, "asset": e.asset, "a": h[0], "cov": h[1]})
    n = 0
    while n < 2000:
        f, a = ASSETS[rng.integers(len(ASSETS))]; lab = D[(f, a)][2]; L = pd.Timedelta(lens[rng.integers(len(lens))])
        s0 = (lab.start + (lab.end - lab.start) * rng.random()).floor("D"); s1 = s0 + L
        if s1 > lab.end: continue
        blocked = lab.exclusions + list(zip(lab.targets.win_start, lab.targets.report))
        if any(s0 < y and x < s1 for x, y in blocked): continue
        h = hit(f, a, s0, s1); sel_rows.append({"method": meth, "kind": "random", "farm": f, "asset": a, "a": h[0], "cov": h[1]}); n += 1
    print(meth, ev_rows[-1], flush=True)

pd.DataFrame(cont_rows).to_csv(f"{OUT}/care_continuous.csv", index=False)
Ev = pd.DataFrame(ev_rows); Ev["prec_inflation"] = Ev.E_best_prec / Ev.cont_prec_B2.replace(0, np.nan)
Ev.to_csv(f"{OUT}/care_protocol_compare.csv", index=False)
S = pd.DataFrame(sel_rows); S = S[S["cov"] > 0.5]; S.to_csv(f"{OUT}/care_selection_windows.csv", index=False)
ratio = S[S.kind == "normal_event"].a.mean() / S[S.kind == "random"].a.mean()
bs, gk = [], {k: v for k, v in S.groupby(["farm", "asset"])}
keys = list(gk)
for _ in range(2000):
    Z = pd.concat([gk[keys[i]] for i in rng.integers(len(keys), size=len(keys))])
    b = Z[Z.kind == "random"].a.mean(); a_ = Z[Z.kind == "normal_event"].a.mean()
    if b > 0 and a_ == a_: bs.append(a_ / b)
p = lambda lam: 1 - np.exp(-lam * 14 / 365.25)   # CARE normal events are ~2 weeks
def power(n, l0, l1, a=0.05):
    k = int(binom.isf(a, n, p(l0))) + 1
    while binom.sf(k - 1, n, p(l0)) > a: k += 1
    return binom.sf(k - 1, n, p(l1))
nN = int((EV.y == 0).sum())
kt = kendalltau(Ev.E_best_f05, Ev.cont_rec_B2)
summary = {"kendall_tau": kt.statistic, "kendall_p": kt.pvalue, "spearman": spearmanr(Ev.E_best_f05, Ev.cont_rec_B2).statistic,
           "H6a_supported": bool(kt.statistic < 0.5), "H6b_min_inflation": Ev.prec_inflation.min(),
           "H6b_supported": bool((Ev.prec_inflation >= 5).all()),
           "H6c_ratio": ratio, "H6c_ci_lo": np.percentile(bs, 2.5), "H6c_ci_hi": np.percentile(bs, 97.5),
           "H6c_supported": bool(np.percentile(bs, 97.5) < 1),
           "n_normal_events": nN, "H6d_power_1v2": power(nN, 1, 2), "H6d_power_1v4": power(nN, 1, 4),
           "H6d_supported": bool(power(nN, 1, 2) < 0.5),
           "zero_fp_upper95_lambda": -np.log(1 - beta.ppf(0.95, 1, nN)) * 365.25 / 14}
pd.Series(summary).to_csv(f"{OUT}/care_summary.csv")
print(Ev.round(3).to_string(index=False)); print(pd.DataFrame(cont_rows)[["method", "budget", "mode", "recall", "fa_per_sub_year", "alarm_precision"]].round(3).to_string(index=False)); print(summary)
