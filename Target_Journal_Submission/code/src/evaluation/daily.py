"""Daily decision unit and conformal alarm budgets (D6 round 3, pre-registered in novelty_escalation_log.md).

D_d = 95th percentile of a method's 10-min score over day d (NaN if fewer than MIN_STEPS valid steps).
An alarm is active during day d+1 when D_d exceeds the threshold (causal: decided at the end of day d).
Fleet conformal budget: thr = (1 - alpha) empirical quantile of D over NORMAL days of calibration substations,
alpha = B / 365.25 for a budget of B false alarms per substation-year (split-conformal style, finite-sample
corrected: the ceil((n + 1)(1 - alpha))-th smallest value).
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from . import continuous as C

Q = 0.95
MIN_STEPS = 72


def daily(score: pd.Series) -> pd.Series:
    g = score.resample("D")
    d = g.quantile(Q)
    return d.where(g.count() >= MIN_STEPS)


def normal_days(D: pd.Series, lab) -> pd.Series:
    """Daily values of days that are monitored and outside all windows and exclusion intervals."""
    blocked = list(zip(lab.targets["win_start"], lab.targets["report"])) + lab.exclusions
    keep = [(d >= lab.start.normalize()) and not C._in_any(d + pd.Timedelta(hours=12), blocked) for d in D.index]
    return D[np.array(keep, bool)].dropna()


def conformal_threshold(values: np.ndarray, alpha: float) -> float:
    v = np.sort(np.asarray(values, float)); n = len(v)
    k = int(np.ceil((n + 1) * (1 - alpha)))
    return np.inf if k > n else v[k - 1]


def alarm_from_daily(D: pd.Series, thr, index: pd.DatetimeIndex) -> pd.Series:
    """thr: scalar or Series indexed like D (threshold valid for deciding on day d). Alarm on day d+1."""
    flag = (D > thr).fillna(False)
    flag.index = flag.index + pd.Timedelta(days=1)
    return pd.Series(flag.reindex(index.normalize()).fillna(False).to_numpy(bool), index=index)


def adaptive_threshold(D: pd.Series, fleet_thr: float, alpha: float) -> pd.Series:
    """max(fleet thr, own-past (1-alpha) quantile of ALL previous daily values; no labels used), once enough
    own days exist (n >= 1/alpha)."""
    v = D.to_numpy(float); out = np.full(len(v), fleet_thr)
    need = int(np.ceil(1 / alpha))
    hist = []
    for i, x in enumerate(v):
        if len(hist) >= need:
            out[i] = max(fleet_thr, conformal_threshold(np.array(hist), alpha))
        if x == x:
            hist.append(x)
    return pd.Series(out, index=D.index)
