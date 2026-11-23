"""Intent and delivery channels (own-history, online). Together with the fleet execution channel (srcr.py)
they decompose substation health into three physically distinct questions:
  INTENT    - is the controller asking for a plausible temperature?   (setpoint vs own heating curve)
  EXECUTION - does the plant deliver what the controller asks for?     (tracking residual, fleet model)
  DELIVERY  - does the building receive the usual heat for the weather? (heat-meter energy signature)
Each channel returns 1 + z, with z the normalised exceedance of a quantile band (score > 1 = outside band).
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import lightgbm as lgb

QPAR = dict(n_estimators=100, learning_rate=0.05, num_leaves=15, min_child_samples=100, verbose=-1, n_jobs=1)


def context(X: pd.DataFrame, weather=True) -> pd.DataFrame:
    idx = X.index
    hr = idx.hour + idx.minute / 60
    c = pd.DataFrame({"hs": np.sin(2 * np.pi * hr / 24), "hc": np.cos(2 * np.pi * hr / 24),
                      "dw": (idx.dayofweek >= 5).astype(float)}, index=idx)
    if weather and "outdoor_temperature" in X:
        to = X["outdoor_temperature"]
        c["to"] = to
        c["to24"] = to.rolling("24h", min_periods=12).mean()
    return c


class _Band:
    """Own-history conditional quantile band for one target."""
    def __init__(self, target, weather, sides, seed=0, alphas=(0.02, 0.5, 0.98), max_rows=30000, min_scale=0.5):
        self.t, self.weather, self.sides, self.seed = target, weather, sides, seed
        self.alphas, self.max_rows, self.min_scale = alphas, max_rows, min_scale

    def fit(self, X):
        y = X[self.t]
        C = context(X, self.weather)
        ok = np.flatnonzero(y.notna().to_numpy())
        rng = np.random.default_rng(self.seed)
        if len(ok) > self.max_rows:
            ok = np.sort(rng.choice(ok, self.max_rows, replace=False))
        self.ms = [lgb.LGBMRegressor(objective="quantile", alpha=a, random_state=self.seed, **QPAR)
                   .fit(C.iloc[ok], y.iloc[ok]) for a in self.alphas]
        return self

    def score(self, X):
        C = context(X, self.weather)
        lo, md, hi = (m.predict(C) for m in self.ms)
        y = X[self.t].to_numpy(float)
        zl = (lo - y) / np.maximum(md - lo, self.min_scale)
        zh = (y - hi) / np.maximum(hi - md, self.min_scale)
        z = {"low": zl, "high": zh, "both": np.maximum(zl, zh)}[self.sides]
        return 1.0 + z


class _MultiBand:
    SPECS = []  # (target, weather?, sides, min_scale)

    def __init__(self, seed=0):
        self.seed = seed

    def fit(self, X):
        self.bands = []
        for t, w, sides, ms in self.SPECS:
            if t in X and X[t].notna().mean() > 0.2 and X[t].nunique(dropna=True) > 3:
                self.bands.append(_Band(t, w, sides, self.seed, min_scale=ms).fit(X))
        return self

    def score(self, X):
        best = np.full(len(X), np.nan)
        for b in self.bands:
            best = np.fmax(best, b.score(X))
        return best


class IntentChannel(_MultiBand):
    """Setpoint plausibility: setpoints far from the substation's own heating curve / schedule."""
    SPECS = [("s_hc1_supply_temperature_setpoint", True, "both", 2.0),
             ("s_dhw_supply_temperature_setpoint", False, "both", 2.0),
             ("s_dhw_upper_storage_temperature_setpoint", False, "both", 2.0),
             ("p_hc1_return_temperature_setpoint", True, "both", 2.0)]


class DeliveryChannel(_MultiBand):
    """Energy signature: delivered heat power and primary flow vs weather; primary return temperature."""
    SPECS = [("p_net_meter_heat_power", True, "both", 1.0),
             ("p_net_meter_flow", True, "both", 10.0),
             ("p_net_return_temperature", True, "both", 1.0)]


class UnderDeliveryChannel(_MultiBand):
    """F12: heat power BELOW the substation's own weather-conditioned band (pumps, valves, regulators).
    Heating-season gating (24-h mean outdoor temperature < 15 degC) is applied at the daily level (round3.py)."""
    SPECS = [("p_net_meter_heat_power", True, "low", 1.0)]
