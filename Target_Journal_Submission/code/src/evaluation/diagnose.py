"""Threshold-free diagnosis: for each target fault, the exceedance rank of its strongest pre-report day among
all normal substation-days of the fleet (daily score = a rolling aggregate of the 10-min score).
rank_frac = share of normal days with a daily score >= the fault's best window day (lower = more detectable).
A rank_frac of r means that a threshold catching this fault produces about r*365 false alarm-days per year."""
from __future__ import annotations
import numpy as np
import pandas as pd
from ..data import predist as P
from . import continuous as C
from .runner import load_scores


def daily(score: pd.Series, agg="mean6h"):
    s = score.copy()
    if agg == "mean6h":
        d = s.rolling("6h", min_periods=18).mean().resample("D").max()
    elif agg == "mean24h":
        d = s.rolling("24h", min_periods=72).mean().resample("D").max()
    elif agg == "max":
        d = s.resample("D").max()
    elif agg == "q90":
        d = s.resample("D").quantile(0.9)
    return d


def fault_ranks(method, m, agg="mean6h"):
    normal_days, fault_best = [], []
    for s in P.substations(m):
        sc = load_scores(method, m, s)
        lab = C.substation_labels(m, s, sc.index)
        d = daily(sc[(sc.index >= lab.start)], agg).dropna()
        blocked = list(zip(lab.targets["win_start"], lab.targets["report"])) + lab.exclusions
        nd = [v for t, v in d.items() if not any(a <= t + pd.Timedelta(hours=12) < b for a, b in blocked)]
        normal_days += nd
        for _, r in lab.targets.iterrows():
            w = d[(d.index >= r["win_start"].floor("D")) & (d.index < r["report"])]
            fault_best.append({"m": m, "sub": s, "event_id": r["event_id"], "best": w.max() if len(w) else np.nan})
    nd = np.sort(np.array(normal_days))
    fb = pd.DataFrame(fault_best)
    fb["rank_frac"] = [1 - np.searchsorted(nd, v, side="left") / len(nd) if v == v else 1.0 for v in fb["best"]]
    F = P.faults(m)[["Event ID", "Fault label", "Problem EN", "Monitoring potential"]].rename(columns={"Event ID": "event_id"})
    return fb.merge(F, on="event_id", how="left"), len(nd)
