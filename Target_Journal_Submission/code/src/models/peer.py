"""Round 5 (pre-registered in experiments/novelty_escalation_log.md): peer-relative daily channels.

Each substation-day is compared with the SAME day's distribution over the OTHER substations of the fleet
(leave-one-out robust median and 1.4826 x MAD). No own history and no training. Weather and season are shared
by peers on the same day and cancel. A daily score is computed at the end of day d and used on day d + 1
(causal). Scores are z / 3 so that 1.0 = three robust peer standard deviations (same convention as baselines).
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from ..features.loops import available_loops

SP_OFF = 20.0
MIN_PEERS = 5
# feature: (direction of a fault: +1 = high is bad, -1 = low is bad)
PHYS = {"dT": -1, "t_ret": +1, "dhw_q10": -1}
COMFORT = {"short": +1}
OWN = {"dT_chg": -1, "flow_chg": +1}


def daily_features(X: pd.DataFrame) -> pd.DataFrame:
    """Daily physics and comfort features of one substation (index = calendar day)."""
    f = pd.DataFrame(index=X.index)
    on = X["p_net_meter_heat_power"] > 0.5 if "p_net_meter_heat_power" in X else pd.Series(True, index=X.index)
    if {"p_net_supply_temperature", "p_net_return_temperature"} <= set(X):
        f["dT"] = (X["p_net_supply_temperature"] - X["p_net_return_temperature"]).where(on)
        f["t_ret"] = X["p_net_return_temperature"].where(on)
    if "p_net_meter_flow" in X:
        f["flow"] = X["p_net_meter_flow"]
    if "s_dhw_upper_storage_temperature" in X:
        f["dhw"] = X["s_dhw_upper_storage_temperature"]
    short = None
    for name, y, ys in available_loops(X):
        if name == "p_ret":
            continue
        s = (X[ys] - X[y]).where(X[ys] > SP_OFF)
        short = s if short is None else np.fmax(short, s)
    if short is not None:
        f["short"] = short
    D = pd.DataFrame(index=f.resample("D").size().index)
    if "dT" in f:
        D["dT"] = f["dT"].resample("D").median()
        D["t_ret"] = f["t_ret"].resample("D").median()
    if "dhw" in f:
        D["dhw_q10"] = f["dhw"].resample("D").quantile(0.1)
    if "short" in f:
        D["short"] = f["short"].rolling("6h", min_periods=18).mean().resample("D").max()
    # own-trajectory change (F21): today vs robust median of the previous 14 days
    for c, src in (("dT_chg", "dT"), ("flow_chg", None)):
        v = D["dT"] if src == "dT" and "dT" in D else (f["flow"].resample("D").median() if src is None and "flow" in f else None)
        if v is None:
            continue
        med = v.rolling(14, min_periods=7).median().shift(1)
        mad = (v - med).abs().rolling(14, min_periods=7).median().shift(1) * 1.4826
        D[c] = (v - med) / np.maximum(mad, 0.5)
    return D


def peer_z(daily: dict, feats: dict) -> dict:
    """daily: {sub: DataFrame}. Returns {sub: DataFrame of signed peer z (positive = fault direction)}."""
    out = {s: pd.DataFrame(index=d.index) for s, d in daily.items()}
    for feat, sign in feats.items():
        W = pd.DataFrame({s: d[feat] for s, d in daily.items() if feat in d})
        if W.empty:
            continue
        for s in W.columns:
            peers = W.drop(columns=s)
            n = peers.notna().sum(1)
            med = peers.median(1)
            mad = (peers.sub(med, axis=0)).abs().median(1) * 1.4826
            z = sign * (W[s] - med) / np.maximum(mad, 1e-3 + 0.05 * med.abs())
            out[s][feat] = z.where(n >= MIN_PEERS)
    return out


def own_z(daily: dict, feats: dict) -> dict:
    return {s: pd.DataFrame({f: sg * d[f] for f, sg in feats.items() if f in d}, index=d.index) for s, d in daily.items()}


def to_steps(zday: pd.DataFrame, index: pd.DatetimeIndex) -> pd.Series:
    """Daily max-z -> score z/3 on the 10-min index, available from the NEXT day (causal)."""
    if zday.shape[1] == 0:
        return pd.Series(np.nan, index=index)
    d = zday.max(1, skipna=True) / 3.0
    d.index = d.index + pd.Timedelta(days=1)
    return d.reindex(index.floor("D")).set_axis(index)
