"""G8 sensitivity: list PreDist fits whose training mask differs between the legacy and the leak-free exclusion rule.
Usage: leak_affected.py M  -> results/leak_sensitivity/affected_m{M}.csv"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import pandas as pd
from src.data import predist as P
from src.evaluation import continuous as C
from src.models import online as O
m = int(sys.argv[1]); rows = []; nfits = 0
for s in P.substations(m):
    X = P.load_substation(m, s) if hasattr(P, "load_substation") else P.load(m, s)
    os.environ["PREDIST_EXCL_RULE"] = "legacy"; L0 = C.substation_labels(m, s, X.index)
    os.environ["PREDIST_EXCL_RULE"] = "leakfree"; L1 = C.substation_labels(m, s, X.index)
    t = L0.start
    while t <= L0.end:
        a, b = O.train_mask(X.index, t, L0), O.train_mask(X.index, t, L1)
        nfits += 1
        if (a != b).any():
            rows.append({"m": m, "sub": s, "retrain_t": t, "n_rows_legacy": int(a.sum()), "n_rows_leakfree": int(b.sum())})
        t += pd.Timedelta(days=O.RETRAIN_DAYS)
os.makedirs("results/leak_sensitivity", exist_ok=True)
D = pd.DataFrame(rows); D.to_csv(f"results/leak_sensitivity/affected_m{m}.csv", index=False)
print(D.to_string(index=False)); print("fits checked", nfits, "affected", len(D), "subs", sorted(D["sub"].unique()) if len(D) else [])
