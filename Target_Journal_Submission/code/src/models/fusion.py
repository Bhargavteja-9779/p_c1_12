"""Fleet-calibrated fusion of channel scores.

Each channel's raw score is mapped to a common 'surprise level' L = -log10 P_normal(score >= s), where
P_normal is the empirical distribution of that channel's score during NORMAL operation of the TRAINING-fold
substations (cross-fitted: a substation is never calibrated with its own data). The fused score is the
maximum level over channels, so every channel contributes alarms at the same normal-operation rate.
"""
from __future__ import annotations
import os
import numpy as np
import pandas as pd
from ..data import predist as P
from ..evaluation import continuous as C
from ..evaluation.runner import load_scores, score_path
from .srcr import normal_mask

MAX_PER_SUB = 50000


def _normal_values(channel, m, subs, seed=0):
    rng = np.random.default_rng(seed)
    vals = []
    for s in subs:
        sc = load_scores(channel, m, s)
        lab = C.substation_labels(m, s, sc.index)
        v = sc[normal_mask(sc.index, lab) & (sc.index >= lab.start)].dropna().to_numpy()
        if len(v) > MAX_PER_SUB:
            v = rng.choice(v, MAX_PER_SUB, replace=False)
        vals.append(v)
    return np.sort(np.concatenate(vals))


def level(scores: np.ndarray, normal_sorted: np.ndarray) -> np.ndarray:
    n = len(normal_sorted)
    k = n - np.searchsorted(normal_sorted, scores, side="left")  # number of normal values >= s
    p = (k + 1) / (n + 1)
    out = -np.log10(p)
    out[np.isnan(scores)] = np.nan
    return out


def fuse(channels, m, folds, name, train_m=None, train_subs=None):
    """folds: list of substation lists (cross-fitting within m). If train_m is given (transfer), calibrate on
    all substations of train_m instead and score every substation of m."""
    out = score_path(name, m); os.makedirs(out, exist_ok=True)
    groups = [(P.substations(m), train_subs)] if train_m else [(f, [s for g in folds if g is not f for s in g]) for f in folds]
    for test, train in groups:
        cal = {c: _normal_values(c, train_m or m, train) for c in channels}
        for s in test:
            lv = None
            for c in channels:
                sc = load_scores(c, m, s)
                L = pd.Series(level(sc.to_numpy(float), cal[c]), index=sc.index)
                lv = L if lv is None else pd.Series(np.fmax(lv.values, L.reindex(lv.index).values), index=lv.index)
            pd.DataFrame({"score": lv}).to_parquet(os.path.join(out, f"s{s}.parquet"))


def m1_folds(K=5, seed=0):
    subs = P.substations(1)
    perm = np.random.default_rng(seed).permutation(subs)
    return [sorted(perm[k::K]) for k in range(K)]
