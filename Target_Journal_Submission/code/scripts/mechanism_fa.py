"""Mechanism of false alarms (M1): conditions in the 24 h before each false-alarm start, versus random
normal times of the same substations. Usage: mechanism_fa.py METHOD TAU C_THR"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from src.data import predist as P
from src.evaluation import continuous as C, runner as R
from src.models import online as O
from src.features.loops import available_loops
meth, tau, cthr = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
rng = np.random.default_rng(0); rows = []
def cond(X, t, s):
    w = X[(X.index >= t - pd.Timedelta(hours=24)) & (X.index < t)]
    sp = w.get("s_hc1_supply_temperature_setpoint")
    out = {"sub": s, "sp_jump_10K": bool(sp is not None and (sp.max() - sp.min()) >= 10),
           "heating_off": bool(sp is not None and sp.median() <= 20),
           "comfort_short_5K": False, "p_ret_above_sp_5K": False,
           "summer": t.month in (5, 6, 7, 8, 9)}
    for name, y, ys in available_loops(w):
        d = (w[ys] - w[y])
        if name == "p_ret":
            out["p_ret_above_sp_5K"] |= bool(((w[y] - w[ys]) > 5).rolling(6).min().max() == 1)
        else:
            out["comfort_short_5K"] |= bool(((d > 5) & (w[ys] > 20)).rolling(6).min().max() == 1)
    return out
for s in P.substations(1):
    sc = R.load_scores(meth, 1, s); lab = C.substation_labels(1, s, sc.index)
    r = C.evaluate_substation(pd.Series(O.criticality_counter(sc, tau) >= cthr, index=sc.index), lab)
    X = P.load_substation(1, s)
    for t in r["false_alarms"]:
        rows.append(dict(kind="false_alarm", **cond(X, t, s)))
    days = pd.date_range(lab.start.ceil("D"), lab.end.floor("D"), freq="D")
    blocked = list(zip(lab.targets["win_start"], lab.targets["report"])) + lab.exclusions
    days = [d for d in days if not C._in_any(d, blocked)]
    for t in rng.choice(days, min(len(days), 30), replace=False):
        rows.append(dict(kind="random_normal", **cond(X, pd.Timestamp(t) + pd.Timedelta(hours=int(rng.integers(24))), s)))
d = pd.DataFrame(rows)
t = d.groupby("kind")[["sp_jump_10K", "heating_off", "comfort_short_5K", "p_ret_above_sp_5K", "summer"]].mean()
t["n"] = d.groupby("kind").size(); t["n_subs"] = d.groupby("kind")["sub"].nunique()
print(meth, tau, cthr); print(t.round(3).to_string())
t.to_csv(f"results/mechanism_fa_{meth}.csv")
