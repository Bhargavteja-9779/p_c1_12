import pandas as pd
from src.evaluation import continuous as C


def make_labels(idx, report, excl=()):
    W = pd.Timedelta(days=C.WINDOW_DAYS)
    t = pd.DataFrame({"event_id": [1], "report": [report], "win_start": [report - W]})
    return C.SubstationLabels(1, 1, idx.min() + pd.Timedelta(days=C.BURN_IN_DAYS), idx.max(), t, list(excl))
