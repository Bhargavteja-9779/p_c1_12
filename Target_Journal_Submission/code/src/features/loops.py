"""Setpoint-relative control-loop features for district heating substations.

A substation controller states what it wants (setpoint) and the plant shows what it delivers (measurement).
Benign changes of intent (users or service staff change setpoints, day/night modes, heating curves) move both,
so the tracking residual e = measurement - setpoint stays small. Faults in valves, pumps, regulators,
strainers or heat exchangers break the loop and make e drift, typically as a persistent shortfall.

LOOPS lists (name, measurement column, setpoint column). Only pairs present in a substation are used.
"""
from __future__ import annotations
import numpy as np
import pandas as pd

LOOPS = [
    ("hc1", "s_hc1_supply_temperature", "s_hc1_supply_temperature_setpoint"),
    ("hc1_1", "s_hc1.1_supply_temperature", "s_hc1.1_supply_temperature_setpoint"),
    ("hc1_2", "s_hc1.2_supply_temperature", "s_hc1.2_supply_temperature_setpoint"),
    ("dhw_sup", "s_dhw_supply_temperature", "s_dhw_supply_temperature_setpoint"),
    ("dhw_sto", "s_dhw_upper_storage_temperature", "s_dhw_upper_storage_temperature_setpoint"),
    ("p_ret", "p_hc1_return_temperature", "p_hc1_return_temperature_setpoint"),
]
MIN_AVAIL = 0.2


def available_loops(X: pd.DataFrame) -> list[tuple[str, str, str]]:
    out = []
    for name, y, ys in LOOPS:
        if y in X and ys in X and X[y].notna().mean() > MIN_AVAIL and X[ys].notna().mean() > MIN_AVAIL:
            out.append((name, y, ys))
    return out


def _reg(X: pd.DataFrame) -> pd.DataFrame:
    """Reindex to a regular 10-min grid so that lags are time-correct (gaps stay NaN)."""
    idx = pd.date_range(X.index.min().floor("10min"), X.index.max().ceil("10min"), freq="10min")
    return X.reindex(X.index.round("10min")).groupby(level=0).first().reindex(idx)


def loop_frame(X: pd.DataFrame, name: str, y: str, ys: str) -> pd.DataFrame:
    """Per-step residual and context for one loop, on the substation's original index."""
    R = _reg(X)
    sp = R[ys]
    f = pd.DataFrame(index=R.index)
    f["e"] = R[y] - sp
    f["sp"] = sp
    f["dsp_1h"] = sp - sp.shift(6)
    f["dsp_6h"] = sp - sp.shift(36)
    f["sp_max_6h"] = sp.rolling(36, min_periods=1).max() - sp
    f["t_out"] = R["outdoor_temperature"] if "outdoor_temperature" in R else np.nan
    f["t_out_24h"] = f["t_out"].rolling(144, min_periods=12).mean()
    f["t_ps"] = R["p_net_supply_temperature"] if "p_net_supply_temperature" in R else np.nan
    f["headroom"] = f["t_ps"] - sp       # primary supply above the requested secondary temperature
    hr = R.index.hour + R.index.minute / 60
    f["hod_s"], f["hod_c"] = np.sin(2 * np.pi * hr / 24), np.cos(2 * np.pi * hr / 24)
    f["doy_s"], f["doy_c"] = np.sin(2 * np.pi * R.index.dayofyear / 365.25), np.cos(2 * np.pi * R.index.dayofyear / 365.25)
    f["loop"] = name
    return f.reindex(X.index)


CONTEXT = ["sp", "dsp_1h", "dsp_6h", "sp_max_6h", "t_out", "t_out_24h", "t_ps", "headroom",
           "hod_s", "hod_c", "doy_s", "doy_c"]
