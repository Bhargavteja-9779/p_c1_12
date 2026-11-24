"""POST-HOC diagnostic (after the locked M2 run): availability of setpoint loops per manufacturer and rule-score
coverage in fault windows. Explains transfer failure; not used to change any method."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from src.data import predist as P
from src.evaluation import continuous as C, runner as R
from src.features.loops import available_loops
rows = []
for m in (1, 2):
    for s in P.substations(m):
        X = P.load_substation(m, s); sc = R.load_scores("rule", m, s)
        lab = C.substation_labels(m, s, sc.index)
        loops = [n for n, _, _ in available_loops(X) if n != "p_ret"]
        cov_f = [sc[(sc.index >= r.win_start) & (sc.index < r.report)].notna().mean() for r in lab.targets.itertuples()]
        rows.append({"m": m, "sub": s, "n_loops": len(loops), "loops": ",".join(loops),
                     "rule_score_coverage": sc.notna().mean(), "n_targets": len(lab.targets),
                     "target_window_coverage": np.mean(cov_f) if cov_f else np.nan,
                     "median_shortfall_K": float(np.nanmedian(sc.values) * 5) if sc.notna().any() else np.nan})
d = pd.DataFrame(rows); os.makedirs("results/diagnostics", exist_ok=True); d.to_csv("results/diagnostics/loops_by_sub.csv", index=False)
print(d.groupby("m").agg(subs=("sub", "size"), no_loop=("n_loops", lambda x: (x == 0).sum()), mean_loops=("n_loops", "mean"),
      cov=("rule_score_coverage", "mean"), tgt_cov=("target_window_coverage", "mean"), med_short=("median_shortfall_K", "median")).round(3))
print(d.groupby("m").loops.value_counts().head(20))
