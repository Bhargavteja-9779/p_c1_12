"""Online (deployment-realistic) runner for per-substation detectors.

At each retraining time t_k (every RETRAIN_DAYS from monitoring start) a detector is fitted on the substation's
history in [t_k - MAX_TRAIN_DAYS, t_k - GAP_DAYS) minus exclusion intervals that are KNOWN at time t_k
(disturbances/faults reported before t_k). It then scores [t_k, t_{k+1}). No future information is used:
no hand-picked training windows, no knowledge of upcoming reports.
"""
from __future__ import annotations
import numpy as np
import pandas as pd

RETRAIN_DAYS = 90
MAX_TRAIN_DAYS = 730
MIN_TRAIN_DAYS = 14
GAP_DAYS = 0


def known_exclusions(lab, t):
    """Exclusion intervals whose triggering report/disturbance happened before time t, clipped at t."""
    out = []
    for a, b in lab.exclusions:
        # an exclusion is known once its anchor (start + 2 d for disturbances / report for faults) has passed;
        # conservative: known if its end <= t, or its start < t - 7 d (report already filed)
        if b <= t or a < t - pd.Timedelta(days=7):
            out.append((a, min(b, t)))
    return out


def train_mask(index, t, lab):
    lo = t - pd.Timedelta(days=MAX_TRAIN_DAYS)
    hi = t - pd.Timedelta(days=GAP_DAYS)
    m = (index >= max(lo, index.min() + pd.Timedelta(days=7))) & (index < hi)
    for a, b in known_exclusions(lab, t):
        m &= ~((index >= a) & (index < b))
    return m


def run_online(X: pd.DataFrame, lab, make_detector) -> pd.Series:
    """X: feature frame on the 10-min index. make_detector(): object with fit(Xtr) and score(Xte)->array
    (higher = more anomalous, already normalised so that 1.0 = training threshold).
    Returns a score series over the monitored span (NaN before the first possible fit)."""
    scores = pd.Series(np.nan, index=X.index)
    t = lab.start
    while t <= lab.end:
        t_next = t + pd.Timedelta(days=RETRAIN_DAYS)
        trm = train_mask(X.index, t, lab)
        te = (X.index >= t) & (X.index < t_next)
        if te.any() and trm.sum() >= MIN_TRAIN_DAYS * 144 * 0.5:
            det = make_detector()
            det.fit(X.loc[trm])
            scores.loc[te] = det.score(X.loc[te])
        t = t_next
    return scores


def criticality_counter(score: pd.Series, tau: float = 1.0) -> np.ndarray:
    """EnergyFaultDetector-style criticality counter: +1 when score>tau, -1 otherwise (floored at 0);
    NaN scores (no model yet) keep the counter. An alarm is active while counter >= c_thr."""
    v = score.values
    c = 0
    out = np.zeros(len(v), dtype=np.int32)
    for i, x in enumerate(v):
        if x == x:
            c = c + 1 if x > tau else max(0, c - 1)
        out[i] = c
    return out
