"""CARE continuous protocol: labels in the same structure as PreDist so continuous.evaluate_substation and
online.run_online are reused unchanged (see novelty_escalation_log.md, round 6)."""
from __future__ import annotations
import os
import numpy as np
import pandas as pd
from ..data import care
from .continuous import SubstationLabels, BURN_IN_DAYS

SCORES = os.path.join(os.path.dirname(__file__), "..", "..", "results", "scores_care")


def labels(f: str, a: int, index: pd.DatetimeIndex) -> SubstationLabels:
    start = index.min() + pd.Timedelta(days=BURN_IN_DAYS); end = index.max()
    E = care.events(f); E = E[(E.asset == a) & (E.event_label == "anomaly")]
    excl = []
    for r in E.itertuples():
        excl.append((r.event_start - pd.Timedelta(days=14), r.event_start))
        excl.append((r.event_end, r.event_end + pd.Timedelta(days=2)))
    t = pd.DataFrame({"event_id": E.event_id.values, "report": E.event_end.values, "win_start": E.event_start.values})
    t = t[(t.win_start >= start) & (t.report <= end + pd.Timedelta(days=1))]
    return SubstationLabels(f, a, start, end, t.reset_index(drop=True), excl)


def all_anomaly_events(f, a, index):
    """Targets including those before burn-in end (for diagnostics)."""
    E = care.events(f); return E[(E.asset == a) & (E.event_label == "anomaly")]


class StatusFiltered:
    """Fit only on status_type_id == 0 rows; drop the status column from features."""
    def __init__(self, det, cols=None):
        self.det, self.cols = det, cols

    def _X(self, X):
        X = X.drop(columns=["status_type_id"], errors="ignore")
        return X[[c for c in X.columns if c in self.cols]] if self.cols is not None else X

    def fit(self, X):
        Xn = X[X["status_type_id"] == 0] if "status_type_id" in X else X
        if len(Xn) < 1000:
            Xn = X
        self.det.fit(self._X(Xn)); return self

    def score(self, X):
        return self.det.score(self._X(X))


def score_path(method, f, a):
    return os.path.join(SCORES, method, f"{f}_{a}.parquet")


def load_scores(method, f, a):
    return pd.read_parquet(score_path(method, f, a))["score"]
