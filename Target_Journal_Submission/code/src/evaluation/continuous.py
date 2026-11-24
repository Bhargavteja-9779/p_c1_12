"""Continuous fleet-monitoring evaluation for early fault detection (PreDist).

The benchmark paper evaluates detectors on 7-day windows (55 fault + 65 hand-picked normal events, 50/50).
Here every monitored 10-min step of every substation is scored, as an operator would experience it.

Definitions (fixed before any method was run; see experiments/protocol.md):
- Monitored span: from series start + BURN_IN_DAYS to series end.
- Target faults: faults.csv rows with efd_possible == True (first occurrence per report, as in the dataset).
- Detection window of a target fault: [report - WINDOW_DAYS, report). A fault is DETECTED if an alarm starts
  inside its window. Lead time = report - first alarm in the window.
- Exclusion intervals (alarms there count neither as true nor as false alarms):
    * every fault row (target or not): [min(anomaly start, report - WINDOW_DAYS), max(anomaly end, report + 1 d)]
    * every disturbance (fault report / task / activity): [start - 2 d, start + 2 d]
    * known unlabelled anomalies listed in the dataset README
- Alarm episodes: rising edges of the boolean alarm signal, with a REFRACTORY period after each alarm in which
  no new alarm is counted (an operator acknowledges an alarm and does not want it repeated for a day).
- False alarm: an alarm episode that starts outside all detection windows and exclusion intervals.
- Exposure: number of monitored days outside windows and exclusions -> false alarms per substation-year.
Known limitation: unreported faults exist in "normal" time, so false-alarm rates are upper bounds.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import pandas as pd
from ..data import predist as P

BURN_IN_DAYS = 30
WINDOW_DAYS = 7
REFRACTORY = pd.Timedelta(hours=24)


@dataclass
class SubstationLabels:
    m: int
    sub: int
    start: pd.Timestamp
    end: pd.Timestamp
    targets: pd.DataFrame          # columns: event_id, report, win_start
    exclusions: list               # list of (start, end)
    excl_known: list | None = None  # optional: time each exclusion becomes known (CARE amendment A1); None = legacy rule


def substation_labels(m: int, s: int, index: pd.DatetimeIndex) -> SubstationLabels:
    start = index.min() + pd.Timedelta(days=BURN_IN_DAYS)
    end = index.max()
    F = P.faults(m)
    F = F[F["sub"] == s]
    W = pd.Timedelta(days=WINDOW_DAYS)
    excl = []
    for _, r in F.iterrows():
        a0 = r["Possible anomaly start"] if pd.notna(r["Possible anomaly start"]) else r["Report date"] - W
        a0 = min(a0, r["Report date"] - W)
        a1 = r["Possible anomaly end"] if pd.notna(r["Possible anomaly end"]) else r["Report date"]
        a1 = max(a1, r["Report date"] + pd.Timedelta(days=1))
        excl.append((a0, a1))
    D = P.disturbances(m)
    for t in D.loc[D["sub"] == s, "Event start"].dropna():
        excl.append((t - pd.Timedelta(days=2), t + pd.Timedelta(days=2)))
    for (mm, ss, a, b) in P.KNOWN_ANOMALIES:
        if mm == m and ss == s:
            excl.append((pd.Timestamp(a) if a else index.min(), pd.Timestamp(b) if b else index.max()))
    T = F[F["efd_possible"] == True]
    targets = pd.DataFrame({"event_id": T["Event ID"].values, "report": T["Report date"].values})
    targets["win_start"] = targets["report"] - W
    # a target is evaluable only if its window lies inside the monitored span
    targets = targets[(targets["win_start"] >= start) & (targets["report"] <= end + pd.Timedelta(days=1))]
    return SubstationLabels(m, s, start, end, targets.reset_index(drop=True), excl)


def alarm_starts(alarm: pd.Series) -> pd.DatetimeIndex:
    """Rising edges of a boolean alarm series, with refractory suppression."""
    a = alarm.fillna(False).astype(bool)
    rising = a & ~a.shift(1, fill_value=False)
    out, last = [], None
    for t in a.index[rising.values]:
        if last is None or t - last >= REFRACTORY:
            out.append(t)
            last = t
    return pd.DatetimeIndex(out)


def _in_any(t, intervals) -> bool:
    return any(a <= t < b for a, b in intervals)


def evaluate_substation(alarm: pd.Series, lab: SubstationLabels) -> dict:
    """alarm: boolean series on the substation's 10-min index (True = alarm active)."""
    alarm = alarm[(alarm.index >= lab.start) & (alarm.index <= lab.end)]
    starts = alarm_starts(alarm)
    windows = list(zip(lab.targets["win_start"], lab.targets["report"]))
    det = []
    for _, r in lab.targets.iterrows():
        inside = starts[(starts >= r["win_start"]) & (starts < r["report"])]
        det.append({"m": lab.m, "sub": lab.sub, "event_id": r["event_id"], "report": r["report"],
                    "detected": len(inside) > 0,
                    "lead_h": (r["report"] - inside.min()).total_seconds() / 3600 if len(inside) else np.nan})
    fa = [t for t in starts if not _in_any(t, windows) and not _in_any(t, lab.exclusions)]
    # exposure in days: monitored days with data, outside windows/exclusions
    days = pd.Series(1, index=alarm.index).resample("D").count()
    days = days[days > 0].index
    blocked = windows + lab.exclusions
    exposure = sum(1 for d in days if not _in_any(d + pd.Timedelta(hours=12), blocked))
    return {"detections": det, "false_alarms": fa, "exposure_days": exposure}


def summarise(results: list[dict]) -> dict:
    det = pd.DataFrame([d for r in results for d in r["detections"]])
    n_fa = sum(len(r["false_alarms"]) for r in results)
    expo = sum(r["exposure_days"] for r in results)
    rec = det["detected"].mean() if len(det) else np.nan
    return {"n_faults": len(det), "recall": rec, "n_false_alarms": n_fa,
            "exposure_years": expo / 365.25, "fa_per_sub_year": n_fa / (expo / 365.25) if expo else np.nan,
            "median_lead_h": det.loc[det["detected"], "lead_h"].median() if len(det) else np.nan,
            "alarm_precision": det["detected"].sum() / max(1, det["detected"].sum() + n_fa)}
