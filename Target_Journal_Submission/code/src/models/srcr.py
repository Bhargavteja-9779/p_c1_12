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


SP_OFF = 20.0  # a loop whose setpoint is <= 20 degC is OFF (heating off / frost protection)


def build_training(frames_by_sub, max_rows_per_sub=20000, seed=0, gate=False):
    """frames_by_sub: {sub: (X, lab)} -> {family: DataFrame of context+e} from normal periods."""
    rng = np.random.default_rng(seed)
    out = {}
    for s, (X, lab) in frames_by_sub.items():
        nm = normal_mask(X.index, lab)
        for name, y, ys in available_loops(X):
            f = loop_frame(X, name, y, ys)[nm].dropna(subset=["e", "sp"])
            if gate:
                f = f[f["sp"] > SP_OFF]
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

    def components(self, X: pd.DataFrame) -> pd.DataFrame:
        """Per-loop lower/upper normalised exceedances and the setpoint (for gating)."""
        out = pd.DataFrame(index=X.index)
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
            out[f"{name}__zl"] = pd.Series((lo - e) / np.maximum(md - lo, 0.5), index=f.index[ok])
            out[f"{name}__zh"] = pd.Series((e - hi) / np.maximum(hi - md, 0.5), index=f.index[ok])
            out[f"{name}__sp"] = f["sp"]
        return out


def compose(comp: pd.DataFrame, gate=True, one_sided=True, local=False, n0_days=14, win_days=60,
            min_scale=0.5, p_ret="both") -> pd.Series:
    """Combine loop components into one score (1 + z, max over loops).
    gate: ignore a loop while its setpoint <= SP_OFF. one_sided: heating/DHW loops score shortfall only.
    p_ret: "both" | "low" | "high" | "drop" (round 4: primary return limiter handling).
    local: fleet-prior -> local-posterior calibration of each loop's z with the substation's own PAST daily
    z values (robust median / MAD over the previous win_days days, shrinkage weight w = n / (n + n0_days))."""
    loops = sorted({c.split("__")[0] for c in comp.columns})
    best = np.full(len(comp), np.nan)
    for L in loops:
        zl, zh, sp = comp[f"{L}__zl"], comp[f"{L}__zh"], comp[f"{L}__sp"]
        if L == "p_ret":
            if p_ret == "drop":
                continue
            z = {"both": np.fmax(zl, zh), "low": zl, "high": zh}[p_ret]
        else:
            z = zl if one_sided else np.fmax(zl, zh)
        z = pd.Series(np.asarray(z, float), index=comp.index)
        if gate:
            z[sp.to_numpy() <= SP_OFF] = np.nan
        if local:
            d = z.resample("D").median()
            n = d.notna().astype(float).rolling(win_days, min_periods=1).sum().shift(1).fillna(0)
            med = d.rolling(win_days, min_periods=3).median().shift(1)
            mad = (d - med).abs().rolling(win_days, min_periods=3).median().shift(1) * 1.4826
            w = (n / (n + n0_days)).where(med.notna(), 0.0)
            mu = (w * med.fillna(0)).reindex(z.index, method="ffill").fillna(0).to_numpy()
            sc = ((1 - w) + w * np.maximum(mad.fillna(1.0), min_scale)).reindex(z.index, method="ffill").fillna(1).to_numpy()
            z = (z - mu) / sc
        best = np.fmax(best, 1.0 + z.to_numpy())
    return pd.Series(best, index=comp.index)
