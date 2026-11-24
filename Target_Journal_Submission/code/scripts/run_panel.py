"""plan_v2: score the generic detector panel online on one dataset. Idempotent (skips existing files).
Usage: run_panel.py care SEED k/n     |   run_panel.py predist1 SEED k/n
Writes results/scores_panel/<dataset>/seed<SEED>/<member>/<asset>.parquet. Same online protocol as all other
detectors (src/models/online.py: 90-day retraining on up to 730 d of own past, known exclusions only; CARE: rows
with status 0 only, leak-free exclusion rule A1)."""
import sys, os, time; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from src.models import online as O
from src.models.panel import Panel, GENERIC

ds, seed = sys.argv[1], int(sys.argv[2]); k, n = map(int, sys.argv[3].split("/"))
OUT = f"results/scores_panel/{ds}/seed{seed}"
if ds == "care":
    from src.data import care
    from src.evaluation import care_eval as CE
    jobs = [(f"{f}_{a}", (f, a)) for f in care.FARMS for a in care.assets(f)]
    load = lambda key: care.load_asset(*key)
    labf = lambda key, idx: CE.labels(key[0], key[1], idx)
else:
    from src.data import predist as P
    from src.evaluation import continuous as C
    m = int(ds[-1]); jobs = [(f"s{s}", s) for s in P.substations(m)]
    load = lambda s: P.load_substation(m, s) if hasattr(P, "load_substation") else P.load(m, s)
    labf = lambda s, idx: C.substation_labels(m, s, idx)
jobs = jobs[k::n]
for name, key in jobs:
    paths = {mm: f"{OUT}/{mm}/{name}.parquet" for mm in GENERIC}
    if all(os.path.exists(p) for p in paths.values()):
        continue
    t0 = time.time(); X = load(key); lab = labf(key, X.index)
    status = X["status_type_id"] if "status_type_id" in X else None
    Xf = X.drop(columns=["status_type_id"], errors="ignore")
    scores = {mm: pd.Series(np.nan, index=X.index) for mm in GENERIC}
    t = lab.start
    while t <= lab.end:
        t_next = t + pd.Timedelta(days=O.RETRAIN_DAYS)
        trm = O.train_mask(X.index, t, lab)
        te = (X.index >= t) & (X.index < t_next)
        if te.any() and trm.sum() >= O.MIN_TRAIN_DAYS * 144 * 0.5:
            tr = Xf.loc[trm]
            if status is not None:
                ok = (status.loc[trm] == 0).to_numpy()
                if ok.sum() >= 1000:
                    tr = tr.loc[ok]
            pm = Panel(seed).fit(tr)
            for mm, v in pm.score_all(Xf.loc[te]).items():
                scores[mm].loc[te] = v
        t = t_next
    for mm, p in paths.items():
        os.makedirs(os.path.dirname(p), exist_ok=True)
        pd.DataFrame({"score": scores[mm].astype(float)}).to_parquet(p)
    print(ds, seed, name, X.shape, f"{time.time()-t0:.0f}s", flush=True)
