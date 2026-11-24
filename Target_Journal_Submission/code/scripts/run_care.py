"""Score one method on all CARE turbines with the online runner. Usage: run_care.py METHOD [seed] [k/n]"""
import sys, os, time; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import torch; torch.set_num_threads(1)
import pandas as pd
from src.data import care
from src.evaluation import care_eval as CE
from src.models import online as O, baselines as B
from src.models.ae import AEDetector
method = sys.argv[1]; seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
part = sys.argv[3] if len(sys.argv) > 3 else None
jobs = [(f, a) for f in care.FARMS for a in care.assets(f)]
if part: k, n = map(int, part.split("/")); jobs = jobs[k::n]
name = method if seed == 0 else f"{method}_seed{seed}"
for f, a in jobs:
    out = CE.score_path(name, f, a)
    if os.path.exists(out): continue
    os.makedirs(os.path.dirname(out), exist_ok=True)
    X = care.load_asset(f, a); lab = CE.labels(f, a, X.index)
    tcols = [c for c in X.columns if any(c == t or c.startswith(t + "_") and c[len(t) + 1:] in ("avg", "max", "min", "std") for t in care.temperature_cols(f))]
    mk = {"sigma3": lambda: CE.StatusFiltered(B.ThreeSigma()),
          "temp3s": lambda: CE.StatusFiltered(B.ThreeSigma(), cols=[c for c in tcols if c.endswith("avg") or c in care.temperature_cols(f)]),
          "iforest": lambda: CE.StatusFiltered(B.IForest(seed)),
          "ae": lambda: CE.StatusFiltered(AEDetector(conditional=False, seed=seed)),
          "ae_cond": lambda: CE.StatusFiltered(AEDetector(conditional=True, seed=seed))}[method]
    t0 = time.time(); sc = O.run_online(X, lab, mk)
    pd.DataFrame({"score": sc.astype(float)}).to_parquet(out)
    print(name, f, a, X.shape, f"{time.time()-t0:.0f}s", flush=True)
