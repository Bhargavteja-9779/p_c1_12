"""plan_v2 detector panel: generic unsupervised detectors computed in ONE pass per training window.
Every member returns a score where 1.0 = its own 99th percentile on the training window (same convention as
baselines.py), so the shared criticality counter and tau grid apply unchanged. Fixed in plan_v2 BEFORE any panel
score was computed. Stochastic members take a seed."""
from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.covariance import LedoitWolf
from sklearn.neighbors import NearestNeighbors, LocalOutlierFactor
from sklearn.mixture import GaussianMixture
from sklearn.ensemble import IsolationForest
from .baselines import numeric_cols

GENERIC = ["z_max", "z_mean", "robust_z_max", "q_frac", "pca_spe", "pca_t2", "maha_lw", "knn_pca",
           "lof_pca", "gmm_pca", "iforest_pca", "ewma_z_max"]
STOCHASTIC = {"knn_pca", "lof_pca", "gmm_pca", "iforest_pca"}
MAX_FIT_ROWS = 20000


def _q99(v):
    v = v[np.isfinite(v)]
    return np.quantile(v, 0.99) + 1e-9 if len(v) else 1.0


class Panel:
    def __init__(self, seed=0, members=GENERIC):
        self.seed, self.members = seed, list(members)

    def fit(self, X: pd.DataFrame):
        self.cols = numeric_cols(X)
        if not self.cols:
            return self
        Z = X[self.cols]
        self.mu, self.sd = Z.mean(), Z.std() + 1e-6
        self.med = Z.median(); self.mad = (Z - self.med).abs().median() * 1.4826 + 1e-6
        self.lo, self.hi = Z.quantile(0.005), Z.quantile(0.995)
        S = ((Z - self.mu) / self.sd).fillna(0.0).to_numpy(np.float32)
        rng = np.random.default_rng(self.seed)
        Sf = S[rng.choice(len(S), MAX_FIT_ROWS, replace=False)] if len(S) > MAX_FIT_ROWS else S
        k = min(20, Sf.shape[1], max(1, len(Sf) - 1))
        self.pca = PCA(n_components=min(k, Sf.shape[1]), random_state=0).fit(Sf)
        cum = np.cumsum(self.pca.explained_variance_ratio_)
        self.kp = int(min(len(cum), np.searchsorted(cum, 0.90) + 1))
        P = self.pca.transform(Sf)
        self.pvar = self.pca.explained_variance_[: self.kp] + 1e-9
        self.lw = LedoitWolf().fit(Sf) if Sf.shape[1] <= 400 else None  # high-dim: Mahalanobis on 20 PCs
        self.lw_pc = LedoitWolf().fit(P)
        Pk = P[:, : self.kp]
        sub = Pk[rng.choice(len(Pk), min(5000, len(Pk)), replace=False)]
        self.nn = NearestNeighbors(n_neighbors=5).fit(sub)
        self.lof = LocalOutlierFactor(n_neighbors=20, novelty=True).fit(sub)
        self.gmm = GaussianMixture(n_components=min(4, len(sub) // 50 + 1), covariance_type="full",
                                   reg_covar=1e-4, random_state=self.seed).fit(sub)
        self.ifo = IsolationForest(n_estimators=100, random_state=self.seed, n_jobs=1).fit(Pk)
        self.thr = {}
        raw = self._raw(X.iloc[-MAX_FIT_ROWS:])  # contiguous tail of the training window (EWMA needs contiguity)
        for m, v in raw.items():
            self.thr[m] = _q99(v)
        return self

    def _raw(self, X):
        Zr = X[self.cols]
        A = ((Zr - self.mu) / self.sd)
        S = A.fillna(0.0).to_numpy(np.float32); Aa = A.abs().to_numpy(float)
        out = {}
        with np.errstate(all="ignore"):
            out["z_max"] = np.nanmax(np.where(np.isnan(Aa), -np.inf, Aa), 1)
            out["z_mean"] = np.nanmean(Aa, 1)
            R = ((Zr - self.med) / self.mad).abs().to_numpy(float)
            out["robust_z_max"] = np.nanmax(np.where(np.isnan(R), -np.inf, R), 1)
            out["q_frac"] = ((Zr < self.lo) | (Zr > self.hi)).mean(1).to_numpy(float)
            P = self.pca.transform(S); Pk = P[:, : self.kp]
            rec = Pk @ self.pca.components_[: self.kp]
            out["pca_spe"] = ((S - rec) ** 2).sum(1)
            out["pca_t2"] = (Pk ** 2 / self.pvar).sum(1)
            out["maha_lw"] = self.lw.mahalanobis(S) if self.lw is not None else self.lw_pc.mahalanobis(P)
            out["knn_pca"] = self.nn.kneighbors(Pk)[0].mean(1)
            out["lof_pca"] = -self.lof.score_samples(Pk)
            out["gmm_pca"] = -self.gmm.score_samples(Pk)
            out["iforest_pca"] = -self.ifo.score_samples(Pk)
            ew = pd.DataFrame(Aa, index=X.index).ewm(halflife=6, ignore_na=True).mean().to_numpy(float)
            out["ewma_z_max"] = np.nanmax(np.where(np.isnan(ew), -np.inf, ew), 1)
        return {m: np.asarray(v, float) for m, v in out.items() if m in self.members}

    def score_all(self, X) -> dict:
        if not self.cols:
            return {m: np.full(len(X), np.nan) for m in self.members}
        raw = self._raw(X)
        return {m: (v / self.thr[m]).clip(min=0) for m, v in raw.items()}
