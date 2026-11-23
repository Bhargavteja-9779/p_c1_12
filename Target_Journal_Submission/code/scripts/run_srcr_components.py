"""Fit gated fleet quantile models with grouped 5-fold cross-fitting (M1) and store per-loop components."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from src.data import predist as P
from src.evaluation import continuous as C, runner as R
from src.models.srcr import FleetQuantileModel, build_training
from src.models.fusion import m1_folds
m = 1; seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
name = "srcr_comp" if seed == 0 else f"srcr_comp_seed{seed}"
subs = P.substations(m)
data = {s: (lambda X: (X, C.substation_labels(m, s, X.index)))(P.load_substation(m, s)) for s in subs}
out = R.score_path(name, m); os.makedirs(out, exist_ok=True)
for k, test in enumerate(m1_folds(seed=seed)):
    mdl = FleetQuantileModel(seed=seed).fit(build_training({s: data[s] for s in subs if s not in test}, seed=seed, gate=True))
    for s in test:
        mdl.components(data[s][0]).to_parquet(os.path.join(out, f"s{s}.parquet"))
    print("fold", k, flush=True)
