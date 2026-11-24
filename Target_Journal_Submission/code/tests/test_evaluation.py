"""Unit tests for the continuous-monitoring evaluation and the criticality counter (no dataset needed)."""
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from src.evaluation import continuous as C
from src.models.online import criticality_counter


def _lab(idx, targets=(), excl=()):
    T = pd.DataFrame({"event_id": list(range(len(targets))), "report": list(targets)})
    T["win_start"] = T["report"] - pd.Timedelta(days=C.WINDOW_DAYS)
    return C.SubstationLabels(1, 0, idx[0], idx[-1], T, list(excl))


def test_alarm_starts_refractory():
    idx = pd.date_range("2020-01-01", periods=6 * 24 * 3, freq="10min")
    a = pd.Series(False, index=idx)
    a.iloc[10:12] = True; a.iloc[20:22] = True          # second rise < 24 h later -> suppressed
    a.iloc[6 * 24 * 2:6 * 24 * 2 + 1] = True             # 48 h later -> counted
    s = C.alarm_starts(a)
    assert len(s) == 2 and s[0] == idx[10]


def test_detection_false_alarm_and_exclusion():
    idx = pd.date_range("2020-01-01", "2020-03-01", freq="10min")
    rep = pd.Timestamp("2020-02-15")
    ex = (pd.Timestamp("2020-01-20"), pd.Timestamp("2020-01-22"))
    a = pd.Series(False, index=idx)
    a[pd.Timestamp("2020-02-12")] = True                 # inside window -> detection (lead 72 h)
    a[pd.Timestamp("2020-01-21")] = True                 # inside exclusion -> ignored
    a[pd.Timestamp("2020-01-05")] = True                 # false alarm
    r = C.evaluate_substation(a, _lab(idx, [rep], [ex]))
    assert r["detections"][0]["detected"] and abs(r["detections"][0]["lead_h"] - 72) < 1e-9
    assert len(r["false_alarms"]) == 1
    # exposure excludes the 7-day window and the 2-day exclusion
    total_days = len(pd.Series(1, index=idx).resample("D").count())
    assert r["exposure_days"] == total_days - 7 - 2


def test_alarm_after_report_is_not_detection():
    idx = pd.date_range("2020-01-01", "2020-03-01", freq="10min")
    a = pd.Series(False, index=idx); a[pd.Timestamp("2020-02-15 01:00")] = True
    r = C.evaluate_substation(a, _lab(idx, [pd.Timestamp("2020-02-15")]))
    assert not r["detections"][0]["detected"] and len(r["false_alarms"]) == 1


def test_summarise_rates():
    res = [{"detections": [{"detected": True, "lead_h": 10.0}, {"detected": False, "lead_h": np.nan}],
            "false_alarms": [1, 2], "exposure_days": 365.25}]
    s = C.summarise(res)
    assert s["recall"] == 0.5 and s["fa_per_sub_year"] == 2 and s["median_lead_h"] == 10


def test_criticality_counter():
    sc = pd.Series([2, 2, np.nan, 0, 2, 0, 0, 0])
    assert criticality_counter(sc, 1.0).tolist() == [1, 2, 2, 1, 2, 1, 0, 0]
