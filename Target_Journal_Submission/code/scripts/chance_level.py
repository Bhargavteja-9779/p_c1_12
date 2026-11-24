"""H-E4 (pre-registered, RECHECK/stage4/preregistration_E.md): are detections above a random-alarm baseline
at the same achieved false-alarm rate? p0 = 1 - exp(-f * 7 / 365.25). One-sided exact binomial, Holm."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
from scipy.stats import binomtest
from m2_evaluate import holm
RES = os.path.join(os.path.dirname(__file__), "..", "results")
ops = pd.read_csv(os.path.join(RES, "locked_m2_operating_points.csv"))
N_M1 = 28  # evaluable M1 target faults (results/dataset_summary.md)
rows = []
for _, o in ops.iterrows():
    for m, rec, f, n in ((1, o.m1_recall, o.m1_fa, N_M1), (2, o.recall, o.fa_per_sub_year, o.n_faults)):
        k = int(round(rec * n)); p0 = 1 - np.exp(-f * 7 / 365.25)
        rows.append(dict(m=m, cell=o.cell, budget=o.budget, k=k, n=int(n), recall=rec, fa_per_sub_year=f,
                         chance_recall=p0, lift=rec / p0 if p0 else np.inf,
                         p=binomtest(k, int(n), p0, alternative="greater").pvalue))
d = pd.DataFrame(rows); d["p_holm"] = holm(d.p); d["above_chance_holm05"] = d.p_holm < 0.05
d.to_csv(os.path.join(RES, "chance_level.csv"), index=False)
print(d.round(4).to_string())
print(d.groupby("m").above_chance_holm05.agg(["sum", "size"]))
