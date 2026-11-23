"""LOCKED TEST (protocol A4): fleet quantile model trained on ALL M1 normal data, applied unchanged to M2.
Stores per-loop components and the composed SRCR-C (p_ret dropped) and SRCR-all (gate+1s+local) scores.
Usage: run_m2_fleet.py SEED"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import pandas as pd
from src.data import predist as P
from src.evaluation import continuous as C, runner as R
from src.models.srcr import FleetQuantileModel, build_training, compose
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
sfx = "" if seed == 0 else f"_seed{seed}"
train = {s: (lambda X: (X, C.substation_labels(1, s, X.index)))(P.load_substation(1, s)) for s in P.substations(1)}
mdl = FleetQuantileModel(seed=seed).fit(build_training(train, seed=seed, gate=True))
VAR = {"srcr_c": dict(gate=True, one_sided=True, local=True, p_ret="drop"),
       "srcr_all": dict(gate=True, one_sided=True, local=True)}
for s in P.substations(2):
    comp = mdl.components(P.load_substation(2, s))
    d = R.score_path("srcr_comp_m1to2" + sfx, 2); os.makedirs(d, exist_ok=True)
    comp.to_parquet(os.path.join(d, f"s{s}.parquet"))
    for v, kw in VAR.items():
        d = R.score_path(v + sfx, 2); os.makedirs(d, exist_ok=True)
        pd.DataFrame({"score": compose(comp, **kw)}).to_parquet(os.path.join(d, f"s{s}.parquet"))
print("done m2 seed", seed)
