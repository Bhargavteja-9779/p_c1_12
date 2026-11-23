"""SRCR on one manufacturer with grouped K-fold cross-fitting over substations (fleet model never sees the
scored substation)."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from src.data import predist as P
from src.evaluation import continuous as C, runner as R
from src.models.srcr import FleetQuantileModel, build_training
m = int(sys.argv[1]); K = 5; name = sys.argv[2] if len(sys.argv) > 2 else "srcr"
subs = P.substations(m)
data = {s: (lambda X: (X, C.substation_labels(m, s, X.index)))(P.load_substation(m, s)) for s in subs}
rng = np.random.default_rng(0); perm = rng.permutation(subs); folds = [sorted(perm[k::K]) for k in range(K)]
out = R.score_path(name, m); os.makedirs(out, exist_ok=True)
for k, test in enumerate(folds):
    train = build_training({s: data[s] for s in subs if s not in test})
    mdl = FleetQuantileModel().fit(train)
    for s in test:
        sc = mdl.score(data[s][0])
        pd.DataFrame({"score": sc.astype(float)}).to_parquet(os.path.join(out, f"s{s}.parquet"))
    print("fold", k, "done", flush=True)
