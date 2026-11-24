"""Per-substation baselines with a common interface: fit(X_train) / score(X) -> array, where 1.0 corresponds
to the model's own alarm threshold (so the same alarm logic and tau grid apply to every method)."""
from __future__ import annotations
import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.ensemble import IsolationForest
from ..features.loops import available_loops, loop_frame

EXCLUDE_COUNTERS = ("p_net_meter_energy", "p_net_meter_volume")  # cumulative counters, not states


def numeric_cols(X, min_avail=0.2):
    return [c for c in X.columns if c not in EXCLUDE_COUNTERS and X[c].notna().mean() > min_avail
            and X[c].nunique(dropna=True) > 2]


class RuleShortfall:
    """B1 expert rule: a heating loop delivers k Kelvin less than its setpoint. Score = shortfall / k.
    Persistence 'for more than h hours' is applied by the shared criticality counter (h = c_thr * 10 min)."""
    def __init__(self, k=5.0):
        self.k = k

    def fit(self, X):
        return self

    def score(self, X):
        best = np.full(len(X), np.nan)
        for name, y, ys in available_loops(X):
            if name == "p_ret":
                continue
            short = (X[ys] - X[y]).to_numpy(float) / self.k
            best = np.fmax(best, short)
        return best


class ThreeSigma:
    """B2: per-signal z-score on own history; score = max_j |z_j| / 3."""
    def fit(self, X):
        self.cols = numeric_cols(X)
        self.mu, self.sd = X[self.cols].mean(), X[self.cols].std() + 1e-6
        return self

    def score(self, X):
        if not self.cols:  # no signal usable in the training window (very short M2 series): no score
            return np.full(len(X), np.nan)
        Z = ((X[self.cols] - self.mu) / self.sd).abs().to_numpy(float)
        return np.nanmax(np.where(np.isnan(Z), -np.inf, Z), 1).clip(min=0) / 3.0


class IForest:
    """B3: Isolation Forest per substation; threshold = 99th percentile of training scores."""
    def __init__(self, seed=0, max_rows=50000):
        self.seed, self.max_rows = seed, max_rows

    def fit(self, X):
        self.cols = numeric_cols(X)
        if not self.cols:  # no usable signal in the training window: score() returns NaN
            return self
        Z = X[self.cols]
        self.mu = Z.mean()
        Z = Z.fillna(self.mu).to_numpy(float)
        rng = np.random.default_rng(self.seed)
        if len(Z) > self.max_rows:
            Z = Z[rng.choice(len(Z), self.max_rows, replace=False)]
        self.m = IsolationForest(n_estimators=100, random_state=self.seed, n_jobs=1).fit(Z)
        self.thr = np.quantile(-self.m.score_samples(Z), 0.99)
        return self

    def score(self, X):
        if not self.cols:
            return np.full(len(X), np.nan)
        Z = X[self.cols].fillna(self.mu).to_numpy(float)
        return -self.m.score_samples(Z) / self.thr


class LoopThreeSigma:
    """B7: setpoint-relative residual per loop, z-scored on the substation's OWN history (no fleet model)."""
    def fit(self, X):
        self.stats = {}
        for name, y, ys in available_loops(X):
            e = (X[y] - X[ys])
            if e.notna().sum() > 100:
                self.stats[name] = (e.mean(), e.std() + 0.5)
        return self

    def score(self, X):
        best = np.full(len(X), np.nan)
        for name, y, ys in available_loops(X):
            if name in self.stats:
                mu, sd = self.stats[name]
                best = np.fmax(best, (np.abs((X[y] - X[ys]) - mu) / sd).to_numpy(float) / 3.0)
        return best


class OwnQuantileNBM:
    """B5: own-history quantile-regression normal-behaviour model (in the spirit of 'beyond three-sigma'):
    for each key signal, LightGBM quantile models (1%, 50%, 99%) given outdoor temperature and time context.
    Score = max over signals of the normalised band exceedance (1 + z, as in SRCR)."""
    TARGETS = ["p_net_return_temperature", "s_hc1_supply_temperature", "p_net_meter_heat_power",
               "p_hc1_return_temperature", "s_dhw_upper_storage_temperature"]

    def __init__(self, seed=0, max_rows=30000):
        self.seed, self.max_rows = seed, max_rows

    @staticmethod
    def _ctx(X):
        idx = X.index
        hr = idx.hour + idx.minute / 60
        c = pd.DataFrame({"hs": np.sin(2 * np.pi * hr / 24), "hc": np.cos(2 * np.pi * hr / 24),
                          "dw": idx.dayofweek, "ds": np.sin(2 * np.pi * idx.dayofyear / 365.25),
                          "dc": np.cos(2 * np.pi * idx.dayofyear / 365.25)}, index=idx)
        if "outdoor_temperature" in X:
            c["to"] = X["outdoor_temperature"]
        if "p_net_supply_temperature" in X:
            c["tps"] = X["p_net_supply_temperature"]
        return c

    def fit(self, X):
        C = self._ctx(X)
        rng = np.random.default_rng(self.seed)
        self.models = {}
        for t in self.TARGETS:
            if t not in X or X[t].notna().mean() < 0.2:
                continue
            ok = X[t].notna().to_numpy()
            idx = np.flatnonzero(ok)
            if len(idx) > self.max_rows:
                idx = np.sort(rng.choice(idx, self.max_rows, replace=False))
            ms = []
            for a in (0.01, 0.5, 0.99):
                m = lgb.LGBMRegressor(objective="quantile", alpha=a, n_estimators=100, learning_rate=0.05,
                                      num_leaves=15, min_child_samples=100, random_state=self.seed,
                                      verbose=-1, n_jobs=1)
                m.fit(C.iloc[idx], X[t].iloc[idx]); ms.append(m)
            self.models[t] = ms
        return self

    def score(self, X):
        C = self._ctx(X)
        best = np.full(len(X), np.nan)
        for t, (lo_m, md_m, hi_m) in self.models.items():
            lo, md, hi = lo_m.predict(C), md_m.predict(C), hi_m.predict(C)
            y = X[t].to_numpy(float)
            z = np.maximum((lo - y) / np.maximum(md - lo, 0.5), (y - hi) / np.maximum(hi - md, 0.5))
            best = np.fmax(best, 1.0 + z)
        return best


COMFORT_LOOPS = ("hc1", "hc1_1", "hc1_2", "dhw_sup", "dhw_sto")


def comfort_columns():
    """Secondary-side comfort signals (loop measurements and setpoints) plus outdoor temperature."""
    from ..features.loops import LOOPS
    return [c for name, y, ys in LOOPS if name in COMFORT_LOOPS for c in (y, ys)] + ["outdoor_temperature"]


class LoopThreeSigmaComfort:
    """B7c (added 2026-11-23, amendment A2): the comfort-only, gated, one-sided version of B7, i.e. SRCR-C
    WITHOUT the fleet quantile model and local calibration (own-history mean/sd of the shortfall residual)."""
    SP_OFF = 20.0

    def fit(self, X):
        self.stats = {}
        for name, y, ys in available_loops(X):
            if name not in COMFORT_LOOPS:
                continue
            on = X[ys] > self.SP_OFF
            e = (X[y] - X[ys])[on]
            if e.notna().sum() > 100:
                self.stats[name] = (e.mean(), e.std() + 0.5)
        return self

    def score(self, X):
        best = np.full(len(X), np.nan)
        for name, y, ys in available_loops(X):
            if name in self.stats:
                mu, sd = self.stats[name]
                z = ((mu - (X[y] - X[ys])) / sd).where(X[ys] > self.SP_OFF).to_numpy(float)
                best = np.fmax(best, z / 3.0)
        return best
