"""Autoencoder normal-behaviour model, re-implemented in PyTorch following the PreDist benchmark
(Roelofs et al., Energy 2026, Table 3, manufacturer M1): hidden layers 64-32, latent = 0.65 x n_features,
lr 4.5e-4, input noise 0.05, batch 256, Mahalanobis anomaly score, threshold = 99th percentile of training
scores. Preprocessing as EnergyFaultDetector: drop columns with >80% NaN or constant, mean imputation,
standard scaling, 0.1/99.9 percentile clipping. Optional conditional time features (hour/day-of-week, sin/cos)
are appended to encoder and decoder inputs (conditional AE).
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import torch
from torch import nn

DEVICE = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")


def time_features(idx: pd.DatetimeIndex) -> np.ndarray:
    h = (idx.hour + idx.minute / 60.0) / 24.0
    w = idx.dayofweek / 7.0
    return np.stack([np.sin(2 * np.pi * h), np.cos(2 * np.pi * h), np.sin(2 * np.pi * w), np.cos(2 * np.pi * w)], 1)


class _Net(nn.Module):
    def __init__(self, d, latent, cond, hidden=(64, 32)):
        super().__init__()
        enc, k = [], d + cond
        for h in hidden:
            enc += [nn.Linear(k, h), nn.ReLU()]; k = h
        enc += [nn.Linear(k, latent)]
        dec, k = [], latent + cond
        for h in reversed(hidden):
            dec += [nn.Linear(k, h), nn.ReLU()]; k = h
        dec += [nn.Linear(k, d)]
        self.enc, self.dec = nn.Sequential(*enc), nn.Sequential(*dec)

    def forward(self, x, c):
        z = self.enc(torch.cat([x, c], 1)) if c.shape[1] else self.enc(x)
        return self.dec(torch.cat([z, c], 1)) if c.shape[1] else self.dec(z)


class AEDetector:
    def __init__(self, conditional=False, latent_frac=0.65, lr=4.5e-4, noise=0.05, batch=256, epochs=10,
                 score_type="mahalanobis", q=0.99, seed=0, max_rows=60000, drop_cols=()):
        self.__dict__.update(locals()); del self.__dict__["self"]

    def _prep(self, X):
        Z = X[self.cols].to_numpy(float)
        Z = np.clip(Z, self.lo, self.hi)
        Z = np.where(np.isnan(Z), self.mu, Z)
        return ((Z - self.mu) / self.sd).astype(np.float32)

    def fit(self, X: pd.DataFrame):
        torch.manual_seed(self.seed); rng = np.random.default_rng(self.seed)
        nan_frac = X.isna().mean()
        cols = [c for c in X.columns if nan_frac[c] <= 0.8 and X[c].nunique(dropna=True) > 1
                and not any(d in c for d in self.drop_cols)]
        self.cols = cols
        Z = X[cols].to_numpy(float)
        self.lo, self.hi = np.nanpercentile(Z, 0.1, 0), np.nanpercentile(Z, 99.9, 0)
        Zc = np.clip(Z, self.lo, self.hi)
        self.mu = np.nanmean(Zc, 0); self.sd = np.nanstd(Zc, 0) + 1e-6
        Z = self._prep(X)
        C = time_features(X.index).astype(np.float32) if self.conditional else np.zeros((len(Z), 0), np.float32)
        if len(Z) > self.max_rows:  # subsample for CPU budget (same rule for every per-substation model)
            sel = np.sort(rng.choice(len(Z), self.max_rows, replace=False)); Z, C = Z[sel], C[sel]
        d = Z.shape[1]
        self.net = _Net(d, max(1, int(round(self.latent_frac * d))), C.shape[1]).to(DEVICE)
        opt = torch.optim.Adam(self.net.parameters(), lr=self.lr)
        Zt, Ct = torch.from_numpy(Z), torch.from_numpy(C)
        n = len(Zt)
        for _ in range(self.epochs):
            perm = torch.randperm(n)
            for i in range(0, n, self.batch):
                b = perm[i:i + self.batch]
                xb = Zt[b] + self.noise * torch.randn_like(Zt[b])
                loss = ((self.net(xb, Ct[b]) - Zt[b]) ** 2).mean()
                opt.zero_grad(); loss.backward(); opt.step()
        E = self._err(Z, C)
        if self.score_type == "mahalanobis":
            cov = np.cov(E, rowvar=False) + 1e-6 * np.eye(E.shape[1])
            self.icov = np.linalg.pinv(np.atleast_2d(cov)); self.emu = E.mean(0)
        s = self._raw(E)
        self.thr = np.quantile(s, self.q) + 1e-12
        return self

    def _err(self, Z, C):
        with torch.no_grad():
            R = self.net(torch.from_numpy(Z), torch.from_numpy(C)).numpy()
        return R - Z

    def _raw(self, E):
        if self.score_type == "mahalanobis":
            D = E - self.emu
            return np.sqrt(np.maximum(np.einsum("ij,jk,ik->i", D, self.icov, D), 0))
        return np.sqrt((E ** 2).mean(1))

    def score(self, X: pd.DataFrame) -> np.ndarray:
        Z = self._prep(X)
        C = time_features(X.index).astype(np.float32) if self.conditional else np.zeros((len(Z), 0), np.float32)
        return self._raw(self._err(Z, C)) / self.thr
