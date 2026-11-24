"""Unit tests for the continuous-monitoring evaluation and alarm logic (synthetic data, no dataset needed)."""
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from src.evaluation import continuous as C
from src.models.online import criticality_counter
from scripts_helpers import make_labels


def test_counter_rises_and_decays():
    s = pd.Series([2, 2, 2, 0, 0, np.nan, 2])
    assert list(criticality_counter(s, 1.0)) == [1, 2, 3, 2, 1, 1, 2]


def test_refractory_suppresses_repeats():
    idx = pd.date_range("2024-01-01", periods=6 * 48, freq="10min")
    a = pd.Series(False, index=idx)
    a.iloc[[10, 30, 200]] = True          # 10 and 30 within 24 h -> one alarm; 200 (> 24 h later) -> second
    assert len(C.alarm_starts(a)) == 2


def test_detection_false_alarm_and_exposure():
    idx = pd.date_range("2024-01-01", "2024-04-01", freq="10min")
    lab = make_labels(idx, report=pd.Timestamp("2024-03-01"))
    a = pd.Series(False, index=idx)
    a[pd.Timestamp("2024-02-27 12:00")] = True   # inside the 7-day window -> detection
    a[pd.Timestamp("2024-02-10 12:00")] = True   # outside -> false alarm
    r = C.evaluate_substation(a, lab)
    assert r["detections"][0]["detected"] and abs(r["detections"][0]["lead_h"] - 60) < 1e-9
    assert len(r["false_alarms"]) == 1
    # monitored days 2024-01-31 .. 2024-04-01 = 62; window [02-23, 03-01) blocks 7 days
    assert r["exposure_days"] == 55


def test_alarm_in_exclusion_is_ignored():
    idx = pd.date_range("2024-01-01", "2024-04-01", freq="10min")
    lab = make_labels(idx, report=pd.Timestamp("2024-03-20"), excl=[(pd.Timestamp("2024-02-05"), pd.Timestamp("2024-02-08"))])
    a = pd.Series(False, index=idx); a[pd.Timestamp("2024-02-06")] = True
    assert len(C.evaluate_substation(a, lab)["false_alarms"]) == 0
