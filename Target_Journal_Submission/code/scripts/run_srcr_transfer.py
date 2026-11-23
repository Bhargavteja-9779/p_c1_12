"""SRCR ablation on M2 (Amendment A1): gated fleet quantile model trained on ALL M1 substations (seed 0), applied
to every M2 substation; composed with gate + one-sided + local."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import pandas as pd
from src.data import predist as P
from src.evaluation import continuous as C, runner as R
from src.models.srcr import FleetQuantileModel, build_training, compose
data = {s: (lambda X: (X, C.substation_labels(1, s, X.index)))(P.load_substation(1, s)) for s in P.substations(1)}
mdl = FleetQuantileModel(seed=0).fit(build_training(data, seed=0, gate=True))
out = R.score_path("srcr_comp__v_gate_1s_local", 2); os.makedirs(out, exist_ok=True)
for s in P.substations(2):
    comp = mdl.components(P.load_substation(2, s))
    pd.DataFrame({"score": compose(comp, gate=True, one_sided=True, local=True)}).to_parquet(os.path.join(out, f"s{s}.parquet"))
    print("srcr m2", s, flush=True)
