"""plan_v2 summary: Holm over the 4 seed-0 confirmatory tests and seed robustness (seeds 0-4). Reads only
results/plan_v2/<ds>/seed<s>/summary.json. Writes results/plan_v2/summary_all.csv and verdicts.json."""
import json, os, numpy as np, pandas as pd

rows = []
for ds in ("predist1", "care"):
    for s in range(5):
        p = f"results/plan_v2/{ds}/seed{s}/summary.json"
        if os.path.exists(p):
            d = json.load(open(p)); rows.append({"ds": ds, "seed": s, **{k: d[k] for k in ("tau_ET", "tau_EH", "tau_CT", "H7a_diff", "H7a_p", "H7b_diff", "H7b_p", "H7c_share_threshold", "H7c_share_window", "sel_ratio", "H7d_supported", "H7d_share_detectors_ratio_lt1", "n_detectors", "n_events")}, "H7a_ci": d["H7a_ci"], "H7b_ci": d["H7b_ci"], "H7d_ci": d["H7d_ci"]})
D = pd.DataFrame(rows); os.makedirs("results/plan_v2", exist_ok=True); D.to_csv("results/plan_v2/summary_all.csv", index=False)
v = {}
s0 = D[D.seed == 0]
tests = [(f"H7a_{r.ds}", r.H7a_p) for r in s0.itertuples()] + [(f"H7b_{r.ds}", r.H7b_p) for r in s0.itertuples()]
order = np.argsort([p for _, p in tests]); m = len(tests); run = 0; holm = {}
for i, j in enumerate(order):
    run = max(run, min(1.0, (m - i) * tests[j][1])); holm[tests[j][0]] = run
for name, p in tests:
    ds = name.split("_", 1)[1]; h = name.split("_")[0]
    seeds = D[D.ds == ds]
    v[name] = {"p_seed0": p, "p_holm": holm[name], "supported_seed0": holm[name] < 0.05,
               "seeds_supported_unadj": int((seeds[f"{h}_p"] < 0.05).sum()), "n_seeds": len(seeds),
               "robust": bool(holm[name] < 0.05 and (seeds[f"{h}_p"] < 0.05).sum() >= 4)}
for ds in D.ds.unique():
    seeds = D[D.ds == ds]
    v[f"H7d_{ds}"] = {"supported_seed0": bool(seeds[seeds.seed == 0].H7d_supported.iloc[0]) if (seeds.seed == 0).any() else None,
                      "seeds_supported": int(seeds.H7d_supported.sum()), "n_seeds": len(seeds)}
json.dump(v, open("results/plan_v2/verdicts.json", "w"), indent=1, default=float)
print(D.drop(columns=["H7a_ci", "H7b_ci", "H7d_ci"]).round(3).to_string(index=False)); print(json.dumps(v, indent=1, default=float))
