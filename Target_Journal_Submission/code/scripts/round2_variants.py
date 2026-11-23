"""Compose SRCR variants from stored components and evaluate at FA budgets (M1 development)."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import pandas as pd
from src.data import predist as P
from src.evaluation import runner as R
from src.models.srcr import compose
VARIANTS = {"v_base": dict(gate=False, one_sided=False, local=False),
            "v_gate": dict(gate=True, one_sided=False, local=False),
            "v_gate_1s": dict(gate=True, one_sided=True, local=False),
            "v_gate_local": dict(gate=True, one_sided=False, local=True),
            "v_gate_1s_local": dict(gate=True, one_sided=True, local=True),
            "v_1s_local": dict(gate=False, one_sided=True, local=True),
            "v_g1l_noret": dict(gate=True, one_sided=True, local=True, p_ret="drop"),
            "v_g1l_retlow": dict(gate=True, one_sided=True, local=True, p_ret="low")}
src = sys.argv[1] if len(sys.argv) > 1 else "srcr_comp"
names = sys.argv[2].split(",") if len(sys.argv) > 2 else list(VARIANTS)
res = []
for v in names:
    name = f"{src}__{v}"; out = R.score_path(name, 1); os.makedirs(out, exist_ok=True)
    for s in P.substations(1):
        comp = pd.read_parquet(os.path.join(R.score_path(src, 1), f"s{s}.parquet"))
        pd.DataFrame({"score": compose(comp, **VARIANTS[v])}).to_parquet(os.path.join(out, f"s{s}.parquet"))
    t, _ = R.best_at_budgets(name, 1)
    res.append(t); print(t[["method", "budget", "tau", "c_thr", "recall", "fa_per_sub_year", "n_false_alarms"]].round(3).to_string(index=False), flush=True)
pd.concat(res).to_csv(f"results/round2_{src}_{'-'.join(names)}.csv" if len(sys.argv) > 2 else f"results/round2_{src}.csv", index=False)
