"""Compute online scores for a method on a manufacturer and evaluate alarm operating points."""
from __future__ import annotations
import os, time
import numpy as np
import pandas as pd
from ..data import predist as P
from . import continuous as C
from ..models import online as O

SCORES = os.path.join(os.path.dirname(__file__), "..", "..", "results", "scores")


def score_path(method, m):
    return os.path.join(SCORES, method, f"m{m}")


def compute_scores(method: str, m: int, scorer, subs=None, overwrite=False):
    """scorer(X, lab) -> pd.Series of normalised scores (1.0 = per-model threshold)."""
    out = score_path(method, m); os.makedirs(out, exist_ok=True)
    for s in (subs or P.substations(m)):
        f = os.path.join(out, f"s{s}.parquet")
        if os.path.exists(f) and not overwrite:
            continue
        X = P.load_substation(m, s)
        lab = C.substation_labels(m, s, X.index)
        t0 = time.time()
        sc = scorer(X, lab)
        pd.DataFrame({"score": sc.astype(float)}).to_parquet(f)
        print(f"{method} m{m} s{s} {time.time()-t0:.0f}s", flush=True)


def load_scores(method, m, s):
    return pd.read_parquet(os.path.join(score_path(method, m), f"s{s}.parquet"))["score"]


def operating_curve(method, m, taus=(1.0,), c_grid=None, subs=None):
    """Return DataFrame: tau, c_thr, recall, fa_per_sub_year, ... over all substations of manufacturer m."""
    c_grid = c_grid or [1, 2, 3, 6, 9, 12, 18, 24, 36, 48, 72, 96, 144, 216, 288]
    rows = []
    cache = []
    for s in (subs or P.substations(m)):
        sc = load_scores(method, m, s)
        lab = C.substation_labels(m, s, sc.index)
        cache.append((sc, lab))
    for tau in taus:
        cnt = [(O.criticality_counter(sc, tau), sc.index, lab) for sc, lab in cache]
        for c in c_grid:
            res = [C.evaluate_substation(pd.Series(k >= c, index=idx), lab) for k, idx, lab in cnt]
            r = C.summarise(res); r.update(tau=tau, c_thr=c); rows.append(r)
    return pd.DataFrame(rows)
