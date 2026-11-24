"""Balanced event-window protocol of the PreDist benchmark (re-implemented from the paper's description).

Events: target faults (efd_possible == True; window [report - 7 d, report)) and the dataset's normal events
(normal_events.csv windows [Event start, Event end)). An event is predicted anomalous if the method's alarm
(criticality counter >= c_thr) is active at any step inside the window. Metrics: eventwise precision, recall,
F0.5. The method scores are the SAME online scores used by the continuous protocol, so the two protocols differ
only in how alarms are counted, not in the models.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from ..data import predist as P
from ..models import online as O
from . import runner as R

WINDOW = pd.Timedelta(days=7)


def events(m: int) -> pd.DataFrame:
    F = P.faults(m)
    F = F[F["efd_possible"] == True]
    f = pd.DataFrame({"sub": F["sub"].values, "event_id": F["Event ID"].values, "start": F["Report date"].values - WINDOW,
                      "end": F["Report date"].values, "y": 1})
    N = P.normal_events(m)
    n = pd.DataFrame({"sub": N["sub"].values, "event_id": N["Event ID"].values, "start": N["Event start"].values,
                      "end": N["Event end"].values, "y": 0})
    return pd.concat([f, n], ignore_index=True)


def max_counter_per_event(method: str, m: int, taus) -> pd.DataFrame:
    """For each event and tau: max criticality counter inside the window and share of window with a score."""
    E = events(m)
    rows = []
    for s, g in E.groupby("sub"):
        try:
            sc = R.load_scores(method, m, int(s))
        except FileNotFoundError:
            sc = None
        for tau in taus:
            cnt = pd.Series(O.criticality_counter(sc, tau), index=sc.index) if sc is not None else None
            for _, e in g.iterrows():
                if cnt is None:
                    mx, cov = 0, 0.0
                else:
                    w = (cnt.index >= e.start) & (cnt.index < e.end)
                    mx = int(cnt[w].max()) if w.any() else 0
                    cov = float(sc[w].notna().mean()) if w.any() else 0.0
                rows.append({"sub": s, "event_id": e.event_id, "y": e.y, "tau": tau, "max_cnt": mx, "coverage": cov})
    return pd.DataFrame(rows)


def metrics(pred: np.ndarray, y: np.ndarray, beta=0.5) -> dict:
    tp = int(((pred == 1) & (y == 1)).sum()); fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum())
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f = (1 + beta**2) * p * r / (beta**2 * p + r) if p + r else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "precision": p, "recall": r, "f05": f}


def grid(mc: pd.DataFrame, c_grid) -> pd.DataFrame:
    rows = []
    for tau, g in mc.groupby("tau"):
        for c in c_grid:
            r = metrics((g.max_cnt.values >= c).astype(int), g.y.values); r.update(tau=tau, c_thr=c); rows.append(r)
    return pd.DataFrame(rows)
