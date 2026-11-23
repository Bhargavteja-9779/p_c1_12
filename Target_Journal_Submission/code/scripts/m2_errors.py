"""Error analysis (descriptive, protocol v1 'error analysis'): which faults each frozen method detects at B = 2
(seed 0), pooled over M1 + M2. Reads results/m2/pooled_detections_B2.csv written by m2_eval.py.
Groups: reported problem (Problem EN), component (text before ':' in Fault label), efd_possible, monitoring
potential (tertiles). Also lists faults detected by C2 only / AE only / no method."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from src.data import predist as P

OUT = "results/m2"
det = pd.read_csv(f"{OUT}/pooled_detections_B2.csv", index_col=0)
meta = []
for m in (1, 2):
    f = P.faults(m).copy()
    f["key"] = [f"{m}_{e}" for e in f["Event ID"]]
    meta.append(f)
meta = pd.concat(meta).set_index("key").loc[det.index]
meta["component"] = meta["Fault label"].astype(str).str.split(":").str[0].str.strip()
meta["problem"] = meta["Problem EN"].astype(str).str.strip().str.lower()
mp = pd.to_numeric(meta["Monitoring potential"], errors="coerce")
meta["mon_pot"] = pd.qcut(mp, 3, labels=["low", "mid", "high"]).astype(str)
meta["manufacturer"] = meta["m"].astype(str)

rows = []
for g in ("manufacturer", "problem", "component", "efd_possible", "mon_pot"):
    for lev, idx in meta.groupby(g).groups.items():
        r = {"group": g, "level": str(lev), "n": len(idx)}
        for c in det.columns:
            r[c] = det.loc[idx, c].astype(bool).mean()
        rows.append(r)
tab = pd.DataFrame(rows)
tab.to_csv(f"{OUT}/error_analysis_B2.csv", index=False)
print(tab.round(2).to_string(index=False))

d = det.astype(bool)
other = [c for c in d.columns if c not in ("C2", "ae", "rule")]
lists = pd.DataFrame({
    "C2": d["C2"], "rule": d["rule"], "ae": d["ae"], "any_other": d[other].any(axis=1),
    "fault_label": meta["Fault label"], "problem": meta["problem"], "efd_possible": meta["efd_possible"]})
lists["category"] = np.select(
    [~d.any(axis=1), d["C2"] & ~d[other].any(axis=1), ~d["C2"] & d.any(axis=1)],
    ["missed_by_all", "C2_only_vs_others", "missed_by_C2_found_by_other"], "shared")
lists.to_csv(f"{OUT}/error_lists_B2.csv")
print(lists.category.value_counts().to_string())
