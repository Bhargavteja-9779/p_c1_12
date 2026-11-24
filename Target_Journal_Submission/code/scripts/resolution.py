"""F19 / H5e: how many normal weeks does a balanced event protocol need to resolve deployment FA rates?
Model: alarms in normal time ~ Poisson(lambda per asset-year); a 7-day normal event is a false positive w.p.
p = 1 - exp(-lambda*7/365.25). Exact one-sided binomial test of H0: lambda = l0 vs H1: lambda = l1 (alpha 0.05)."""
import os, numpy as np, pandas as pd
from scipy.stats import binom, beta
os.makedirs("results/round5", exist_ok=True)
p = lambda lam: 1 - np.exp(-lam * 7 / 365.25)
def power(n, l0, l1, a=0.05):
    k = int(binom.isf(a, n, p(l0))) + 1          # reject H0 if FP count >= k
    while binom.sf(k - 1, n, p(l0)) > a: k += 1
    return binom.sf(k - 1, n, p(l1))
rows = []
for l0, l1 in [(1, 4), (1, 2), (0.5, 2), (2, 4)]:
    n = next(n for n in range(5, 20000) if power(n, l0, l1) >= 0.8)
    rows.append({"lambda0": l0, "lambda1": l1, "p_week0": p(l0), "p_week1": p(l1), "n_weeks_80pct_power": n,
                 "power_at_35": power(35, l0, l1), "power_at_65": power(65, l0, l1)})
# with 0 false positives among N normal events, the 95% upper bound on lambda
for N in (35, 65):
    pu = beta.ppf(0.95, 1, N)
    rows.append({"N_normal_events": N, "zero_fp_upper95_lambda_per_year": -np.log(1 - pu) * 365.25 / 7})
df = pd.DataFrame(rows); df.to_csv("results/round5/resolution.csv", index=False); print(df.round(3).to_string())
