"""CARE to Compare wind SCADA (Zenodo 14958989): one continuous 10-min series per turbine (union of datasets)."""
from __future__ import annotations
import os, glob
from functools import lru_cache
import pandas as pd
ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "data")
RAW = os.path.join(ROOT, "raw", "care", "x", "Care_To_Compare")
CACHE = os.path.join(ROOT, "cache", "care")
FARMS = ("A", "B", "C")


def _fdir(f): return os.path.join(RAW, f"farm_{f}", f"Wind Farm {f}")


@lru_cache(maxsize=None)
def events(f: str) -> pd.DataFrame:
    e = pd.read_csv(os.path.join(_fdir(f), "event_info.csv"), sep=";")
    for c in ("event_start", "event_end"):
        e[c] = pd.to_datetime(e[c], format="%d.%m.%Y %H:%M")
    e = e.rename(columns={"asset_id": "asset"}); e["farm"] = f
    return e


def assets(f: str) -> list[int]:
    return sorted(events(f).asset.unique().tolist())


@lru_cache(maxsize=None)
def temperature_cols(f: str) -> tuple:
    d = pd.read_csv(os.path.join(_fdir(f), "feature_description.csv"), sep=";", encoding="latin1")
    names = d[d.description.str.contains("emperature", na=False) & ~d.description.str.contains("mbient", na=False)].sensor_name
    return tuple(names)


def load_asset(f: str, a: int) -> pd.DataFrame:
    os.makedirs(CACHE, exist_ok=True)
    cp = os.path.join(CACHE, f"{f}_{a}.parquet")
    if os.path.exists(cp):
        return pd.read_parquet(cp)
    E = events(f)
    parts = []
    for i in E[E.asset == a].event_id:
        x = pd.read_csv(os.path.join(_fdir(f), "datasets", f"{i}.csv"), sep=";")
        x["time_stamp"] = pd.to_datetime(x["time_stamp"]); parts.append(x.set_index("time_stamp"))
    X = pd.concat(parts); X = X[~X.index.duplicated()].sort_index()
    X = X.drop(columns=["asset_id", "id", "train_test"]).astype(float)
    X.to_parquet(cp)
    return X
