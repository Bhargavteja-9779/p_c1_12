import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from src.models.srcr import compose


def _comp():
    idx = pd.date_range("2024-01-01", periods=4, freq="10min")
    return pd.DataFrame({"hc1__zl": [0, 3, 0, 0], "hc1__zh": [5, 0, 0, 0], "hc1__sp": [50, 50, 15, 50],
                         "p_ret__zl": [0, 0, 0, 0], "p_ret__zh": [0, 0, 0, 9], "p_ret__sp": [60, 60, 60, 60]}, index=idx)


def test_one_sided_ignores_overshoot_and_drop_removes_p_ret():
    s = compose(_comp(), gate=True, one_sided=True, local=False, p_ret="drop")
    assert s.iloc[0] == 1.0 and s.iloc[1] == 4.0 and np.isnan(s.iloc[2]) and s.iloc[3] == 1.0


def test_p_ret_both_kept():
    s = compose(_comp(), gate=True, one_sided=True, local=False, p_ret="both")
    assert s.iloc[3] == 10.0
