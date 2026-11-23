"""PreDist loader: harmonised 10-min operational data, events and exclusion intervals.

Units are harmonised to M1 conventions: energy kWh, volume m3, power kW, flow l/h.
Categorical status/mode columns are mapped to numbers (on=1/off=0; mode codes kept as category codes).
"""
from __future__ import annotations
import os
from functools import lru_cache
import numpy as np
import pandas as pd

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "data")
RAW = os.path.join(ROOT, "raw", "predist")
CACHE = os.path.join(ROOT, "cache")

# unit factors for M2 -> M1 conventions
M2_UNITS = {"p_net_meter_energy": 1e-3, "p_net_meter_heat_power": 1e-3,
            "p_net_meter_flow": 1e-3, "p_net_meter_volume": 1e-6}
MODE_WORDS = {"TAG": 2.0, "NACHT": 1.0, "STANDBY": 0.0}
ON_WORDS = {"EIN": 1.0, "AN": 1.0, "ON": 1.0, "1": 1.0, "AUS": 0.0, "OFF": 0.0, "0": 0.0}


def _mdir(m: int) -> str:
    return os.path.join(RAW, f"manufacturer {m}")


def substations(m: int) -> list[int]:
    fs = os.listdir(os.path.join(_mdir(m), "operational_data"))
    return sorted(int(f.split("_")[1].split(".")[0]) for f in fs if f.endswith(".csv"))


def load_substation(m: int, s: int) -> pd.DataFrame:
    """Return harmonised 10-min data indexed by timestamp (cached as parquet)."""
    os.makedirs(CACHE, exist_ok=True)
    cp = os.path.join(CACHE, f"m{m}_s{s}.parquet")
    if os.path.exists(cp):
        return pd.read_parquet(cp)
    d = pd.read_csv(os.path.join(_mdir(m), "operational_data", f"substation_{s}.csv"), sep=";", low_memory=False)
    d["timestamp"] = pd.to_datetime(d["timestamp"], format="mixed")
    d = d.drop_duplicates("timestamp").set_index("timestamp").sort_index()
    out = pd.DataFrame(index=d.index)
    for c in d.columns:
        x = d[c]
        if not pd.api.types.is_numeric_dtype(x):
            num = pd.to_numeric(x, errors="coerce")
            if num.notna().mean() >= 0.5 * x.notna().mean():
                x = num
            else:
                xs = x.astype(str).str.strip().str.upper()
                if set(xs.dropna().unique()) - {"NAN"} <= set(ON_WORDS):
                    x = xs.map(ON_WORDS)
                else:  # control-unit modes, ordinal by heating intensity
                    x = xs.map(MODE_WORDS)
        x = x.astype(float)
        if m == 2 and c in M2_UNITS:
            x = x * M2_UNITS[c]
        out[c] = x
    out.to_parquet(cp)
    return out


@lru_cache(maxsize=None)
def faults(m: int) -> pd.DataFrame:
    f = pd.read_csv(os.path.join(_mdir(m), "faults.csv"), sep=";")
    for c in ["Report date", "Possible anomaly start", "Possible anomaly end", "Training start", "Training end"]:
        f[c] = pd.to_datetime(f[c], format="mixed", errors="coerce")
    f["m"] = m
    return f.rename(columns={"substation ID": "sub"})


@lru_cache(maxsize=None)
def normal_events(m: int) -> pd.DataFrame:
    n = pd.read_csv(os.path.join(_mdir(m), "normal_events.csv"), sep=";")
    for c in ["Event start", "Event end", "Training start", "Training end"]:
        n[c] = pd.to_datetime(n[c], format="mixed", errors="coerce")
    n["m"] = m
    return n.rename(columns={"substation ID": "sub"})


@lru_cache(maxsize=None)
def disturbances(m: int) -> pd.DataFrame:
    d = pd.read_csv(os.path.join(_mdir(m), "disturbances.csv"), sep=";")
    d["Event start"] = pd.to_datetime(d["Event start"], format="mixed", errors="coerce")
    d["m"] = m
    return d.rename(columns={"substation ID": "sub"})


@lru_cache(maxsize=None)
def configuration(m: int) -> pd.DataFrame:
    c = pd.read_csv(os.path.join(_mdir(m), "configuration_types.csv"), sep=";")
    return c.rename(columns={"substation ID": "sub"})


# Known unlabelled anomalies listed in the dataset README (>24 h). 'start'/'end' = series bounds.
KNOWN_ANOMALIES = [
    (1, 1, None, "2018-07-20"), (1, 19, None, "2016-06-30"), (1, 21, "2019-10-01", None),
    (1, 33, "2018-10-01", "2018-11-30"), (1, 33, "2020-03-01", "2020-03-31"),
    (2, 22, "2019-09-16", "2019-09-25"), (2, 22, "2020-02-11", "2020-03-17"),
    (2, 41, "2017-04-01", "2017-12-31"), (2, 34, "2017-09-01", None),
]
