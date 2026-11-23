"""SRCR: Setpoint-Relative Control-loop Residuals with a fleet-shared conditional quantile model.

For each loop family a LightGBM quantile model learns, from OTHER substations' normal operation, the band
[q_lo, q_hi] of the tracking residual e = measurement - setpoint given operating context (setpoint level and
recent setpoint changes, outdoor and primary supply temperature, time of day/year). A substation is scored
without any own history ("zero-shot"):
    z = max( (q_lo - e) / (q_med - q_lo), (e - q_hi) / (q_hi - q_med) ),  score = 1 + z (score > 1 = outside band)
The substation score is the maximum over its available loops.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import lightgbm as lgb
from ..features.loops import available_loops, loop_frame, CONTEXT

FAMILY = {"hc1": "hc", "hc1_1": "hc", "hc1_2": "hc", "dhw_sup": "dhw_sup", "dhw_sto": "dhw_sto", "p_ret": "p_ret"}
ALPHAS = (0.02, 0.5, 0.98)
LGB_PARAMS = dict(n_estimators=200, learning_rate=0.05, num_leaves=31, min_child_samples=200,
                  subsample=0.8, subsample_freq=1, colsample_bytree=0.9, verbose=-1, n_jobs=2)


def normal_mask(index, lab):
    m = np.ones(len(index), bool)
    for a, b in lab.exclusions:
        m &= ~((index >= a) & (index < b))
    for _, r in lab.targets.iterrows():
        m &= ~((index >= r["win_start"]) & (index < r["report"]))
    return m


def build_training(frames_by_sub, max_rows_per_sub=20000, seed=0):
    """frames_by_sub: {sub: (X, lab)} -> {family: DataFrame of context+e} from normal periods."""
    rng = np.random.default_rng(seed)
    out = {}
    for s, (X, lab) in frames_by_sub.items():
        nm = normal_mask(X.index, lab)
        for name, y, ys in available_loops(X):
            f = loop_frame(X, name, y, ys)[nm].dropna(subset=["e", "sp"])
            if len(f) > max_rows_per_sub:
                f = f.iloc[np.sort(rng.choice(len(f), max_rows_per_sub, replace=False))]
            out.setdefault(FAMILY[name], []).append(f)
    return {k: pd.concat(v) for k, v in out.items()}


class FleetQuantileModel:
    def __init__(self, seed=0):
        self.seed = seed
        self.models = {}

    def fit(self, train):
        for fam, f in train.items():
            self.models[fam] = []
            for a in ALPHAS:
                mdl = lgb.LGBMRegressor(objective="quantile", alpha=a, random_state=self.seed, **LGB_PARAMS)
                mdl.fit(f[CONTEXT], f["e"])
                self.models[fam].append(mdl)
        return self

    def score(self, X: pd.DataFrame) -> pd.Series:
        best = pd.Series(np.nan, index=X.index)
        for name, y, ys in available_loops(X):
            fam = FAMILY[name]
            if fam not in self.models:
                continue
            f = loop_frame(X, name, y, ys)
            ok = f["e"].notna() & f["sp"].notna()
            if not ok.any():
                continue
            lo, md, hi = (m.predict(f.loc[ok, CONTEXT]) for m in self.models[fam])
            e = f.loc[ok, "e"].values
            z = np.maximum((lo - e) / np.maximum(md - lo, 0.5), (e - hi) / np.maximum(hi - md, 0.5))
            sc = pd.Series(1.0 + z, index=f.index[ok])
            best = pd.Series(np.fmax(best.values, sc.reindex(X.index).values), index=X.index)
        return best
