"""H5d: are hand-picked normal events easier than random eligible normal weeks? (M1, B = 2 operating points)"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from src.data import predist as P
from src.evaluation import continuous as C, runner as R, event_protocol as E
from src.models import online as O
m = 1; rng = np.random.default_rng(0); W = pd.Timedelta(days=7)
METHODS = ["rule", "sigma3", "loop3s", "iforest", "qnbm", "ae", "ae_cond", "underdel", "srcr_comp__v_gate_1s_local"]
T = pd.read_csv("results/m1_table.csv")
NE = E.events(m); NE = NE[NE.y == 0]
# random eligible windows: start uniform over monitored span, window must avoid targets/exclusions and have scores
subs = P.substations(m); labs = {}
for s in subs:
    idx = R.load_scores("rule", m, s).index; labs[s] = C.substation_labels(m, s, idx)
def eligible(s, a):
    lab = labs[s]; b = a + W
    if a < lab.start or b > lab.end: return False
    blocked = lab.exclusions + list(zip(lab.targets.win_start, lab.targets.report))
    return not any(a < y and x < b for x, y in blocked)
wins = []
while len(wins) < 2000:
    s = subs[rng.integers(len(subs))]; lab = labs[s]
    a = lab.start + (lab.end - lab.start) * rng.random()
    a = a.floor("D")
    if eligible(s, a): wins.append((s, a))
rows = []; allw = []
for meth in METHODS:
    op = T[(T.method == meth) & (T.budget == 2)].iloc[0]
    al = {}
    for s in subs:
        sc = R.load_scores(meth, m, s); al[s] = (pd.Series(O.criticality_counter(sc, op.tau), index=sc.index) >= op.c_thr, sc.notna())
    def hit(s, a):
        a_, ok = al[s]; w = (a_.index >= a) & (a_.index < a + W)
        return (bool(a_[w].any()), float(ok[w].mean()) if w.any() else 0.0)
    ne = [hit(int(r.sub), r.start) + (int(r.sub),) for r in NE.itertuples()]
    rw = [hit(s, a) + (s,) for s, a in wins]
    ne = [x for x in ne if x[1] > 0.5]; rw = [x for x in rw if x[1] > 0.5]
    rn, rr = np.mean([x[0] for x in ne]), np.mean([x[0] for x in rw])
    # cluster bootstrap over substations of the rate ratio
    nes = pd.DataFrame(ne, columns=["a", "cov", "s"]); rws = pd.DataFrame(rw, columns=["a", "cov", "s"])
    allw.append(nes.assign(kind="normal_event", method=meth)); allw.append(rws.assign(kind="random", method=meth))
    bs = []
    for _ in range(2000):
        pick = rng.choice(subs, len(subs))
        a = pd.concat([nes[nes.s == k] for k in pick]); b = pd.concat([rws[rws.s == k] for k in pick])
        if len(a) and len(b) and b.a.mean() > 0: bs.append(a.a.mean() / b.a.mean())
    rows.append({"method": meth, "n_normal_events": len(ne), "alarm_rate_normal_events": rn, "n_random_windows": len(rw),
                 "alarm_rate_random_windows": rr, "rate_ratio": rn / rr if rr else np.nan,
                 "ratio_ci_lo": np.percentile(bs, 2.5), "ratio_ci_hi": np.percentile(bs, 97.5),
                 "expected_from_cont_fa": 1 - np.exp(-op.fa_per_sub_year * 7 / 365.25)})
    print(rows[-1], flush=True)
D = pd.DataFrame(rows); D.to_csv("results/round5/selection_m1.csv", index=False)
pool_n = (D.alarm_rate_normal_events * D.n_normal_events).sum() / D.n_normal_events.sum()
pool_r = (D.alarm_rate_random_windows * D.n_random_windows).sum() / D.n_random_windows.sum()
print(D.round(3).to_string(index=False)); print("pooled ratio", pool_n / pool_r)

A = pd.concat(allw); A.to_csv("results/round5/selection_windows_m1.csv", index=False)
bs = []
g = {k: v for k, v in A.groupby("s")}
for _ in range(2000):
    pick = rng.choice(subs, len(subs)); Z = pd.concat([g[k] for k in pick if k in g])
    a = Z[Z.kind == "normal_event"].a.mean(); b = Z[Z.kind == "random"].a.mean()
    if b > 0 and a == a: bs.append(a / b)
lo, hi = np.percentile(bs, [2.5, 97.5])
pd.Series({"pooled_ratio": pool_n / pool_r, "ci_lo": lo, "ci_hi": hi, "H5d_supported": bool(hi < 1)}).to_csv("results/round5/selection_pooled_m1.csv")
print("pooled", pool_n / pool_r, lo, hi)
