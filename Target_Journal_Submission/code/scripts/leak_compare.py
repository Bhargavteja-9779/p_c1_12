"""G8 sensitivity (experiments/leak_sensitivity.md): compare plan_v2/plan_v3 PreDist outputs under the legacy and the
leak-free exclusion rule. Usage: leak_compare.py LEAKFREE_CODE_DIR  -> results/leak_sensitivity/{compare.csv,cells.csv,verdict.json}"""
import sys, os, json
import pandas as pd

LF = sys.argv[1]
OUT = "results/leak_sensitivity"; os.makedirs(OUT, exist_ok=True)
v2 = "results/plan_v2/predist1/seed0/summary.json"; v3 = "results/plan_v3/predist1/summary.json"
A2, B2 = json.load(open(v2)), json.load(open(f"{LF}/{v2}"))
A3, B3 = json.load(open(v3)), json.load(open(f"{LF}/{v3}"))
rows = []
for src, A, B in (("plan_v2", A2, B2), ("plan_v3", A3, B3)):
    for k in A:
        if k in ("dataset", "seed"): continue
        rows.append({"source": src, "quantity": k, "legacy": json.dumps(A[k]), "leakfree": json.dumps(B.get(k)),
                     "identical": A[k] == B.get(k)})
pd.DataFrame(rows).to_csv(f"{OUT}/compare.csv", index=False)
cA = pd.read_csv("results/plan_v2/predist1/seed0/cells.csv").set_index("detector")
cB = pd.read_csv(f"{LF}/results/plan_v2/predist1/seed0/cells.csv").set_index("detector")
C = cA.join(cB, lsuffix="_legacy", rsuffix="_leakfree")
for c in ("ET", "EH", "CT", "CH"): C[f"d_{c}"] = C[f"{c}_leakfree"] - C[f"{c}_legacy"]
C.to_csv(f"{OUT}/cells.csv")
flags = [k for k in ("H7d_supported",) if A2[k] != B2[k]] + [k for k in ("H8a_supported", "H8b_supported", "H8c_supported") if A3[k] != B3[k]]
# H7a/H7b support at the unadjusted one-sided 0.05 level (Holm uses CARE too; reported separately)
for h in ("H7a", "H7b"):
    if (A2[f"{h}_p"] < 0.05) != (B2[f"{h}_p"] < 0.05): flags.append(h)
max_dch = float(C["d_CH"].abs().max())
verdict = {"verdict_flips": flags, "max_abs_CH_change": max_dch, "ch_one_fault": 1 / 28,
           "robust": (not flags) and max_dch <= 1 / 28 + 1e-9}
json.dump(verdict, open(f"{OUT}/verdict.json", "w"), indent=1)
print(C[[c for c in C.columns if c.startswith("d_")]].round(3).to_string())
print(pd.DataFrame(rows).query("not identical").to_string(index=False))
print(json.dumps(verdict, indent=1))
