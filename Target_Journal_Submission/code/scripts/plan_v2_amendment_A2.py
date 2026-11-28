"""plan_v2 Amendment A2 (experiments/plan_v2_amendment_A2.md). Usage: plan_v2_amendment_A2.py {predist1|care} SEED
Env A2_VERSION (label, e.g. leakfree/legacy/primary), A2_OUT (absolute output dir). Run with cwd = the code tree whose
results/plan_v2/<ds>/cache holds the tables (main tree, or the leak-free scratch tree). Reuses the plan_v2 setup code
verbatim (events, random windows, folds, cached tables); no new scores, no model fitting."""
import os, sys, json
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plan_v2_analysis.py")
code = open(SRC).read()
head = code[:code.index("tab = {d: tables(d) for d in DETS}")]
os.environ.setdefault("PLANV2_NBOOT", "0")
sys.argv = [SRC] + sys.argv[1:3]
g = {"__file__": SRC, "__name__": "planv2_head"}
exec(compile(head, SRC, "exec"), g)
np, pd, kendalltau = g["np"], g["pd"], g["kendalltau"]
DETS, A, FOLD, NF, T, CN, DS, SEED = (g[k] for k in ["DETS", "A", "FOLD", "NF", "T", "CN", "DS", "SEED"])
pooled, cells = g["pooled"], g["cells"]
BS = [0.5, 1.0, 2.0, 4.0, 8.0]
FAM = {"zscore": ["z_max", "z_mean", "robust_z_max", "ewma_z_max", "q_frac"], "linear": ["pca_spe", "pca_t2", "maha_lw"],
       "density": ["knn_pca", "lof_pca", "gmm_pca", "iforest_pca"], "physics_expert": ["rule", "loop3s", "temp3s"],
       "nbm": ["qnbm"], "autoencoder": ["ae", "ae_cond"]}
VER = os.environ.get("A2_VERSION", "main"); OUTD = os.environ.get("A2_OUT", "results/plan_v2/amendment_A2")
os.makedirs(OUTD, exist_ok=True)


def best_point_b(cont, w, b):
    rec, fa = pooled(cont, w); ok = fa <= b
    if not ok.any(): return (T - 1, CN - 1)
    sc = np.where(ok, rec * 1e6 - fa, -np.inf); return np.unravel_index(np.argmax(sc), sc.shape)


ones = np.ones(A); rows = []
for d in DETS:
    cont, evm, rwm = g["tables"](d)
    et, eh, ct, ch, _ = cells(cont, evm, ones)
    r = {"detector": d, "ET": et, "EH": eh, "CT": ct, "CH": ch}
    for b in BS:
        pts = {f: best_point_b(cont, ones * (FOLD != f), b) for f in range(NF)}
        gg = sum(np.tensordot(ones * (FOLD == f), cont[:, pts[f][0], pts[f][1]], axes=(0, 0)) for f in range(NF))
        r[f"CH_{b}"] = gg[1] / max(gg[0], 1e-9); r[f"FA_{b}"] = gg[2] / max(gg[3] / 365.25, 1e-9)
        r[f"ndet_{b}"] = int(gg[1])
    r["CHA"] = float(np.mean([r[f"CH_{b}"] for b in BS])); rows.append(r)
X = pd.DataFrame(rows)
X.to_csv(f"{OUTD}/{DS}_{VER}_seed{SEED}_cells.csv", index=False)
kt = lambda a, b: kendalltau(a, b).statistic


def label_swap(x, y, ref, n=20000):
    d_hat = kt(y, ref) - kt(x, ref); rng = np.random.default_rng(0); cnt = 0
    for _ in range(n):
        s = rng.random(len(x)) < 0.5
        cnt += (kt(np.where(s, x, y), ref) - kt(np.where(s, y, x), ref)) >= d_hat - 1e-12
    return float(d_hat), (1 + cnt) / (n + 1)


res = {"dataset": DS, "seed": SEED, "version": VER, "n_detectors": len(X)}
for c in ["ET", "EH", "CT"]: res[f"tau_{c}_CHA"] = float(kt(X[c], X.CHA))
for h, a, b in [("H9a", "ET", "EH"), ("H9b", "ET", "CT")]:
    dh, p = label_swap(X[a].to_numpy(float), X[b].to_numpy(float), X.CHA.to_numpy(float))
    res[f"{h}_diff"], res[f"{h}_p_labelswap"] = dh, p
# D1 operator regret
top = X.ET.idxmax(); reg = []
for b in BS:
    order = X[f"CH_{b}"].rank(ascending=False, method="min")
    reg.append({"B": b, "bench_best": X.detector[top], "bench_best_CH": float(X.loc[top, f"CH_{b}"]),
                "best_CH": float(X[f"CH_{b}"].max()), "best_det": X.detector[X[f"CH_{b}"].idxmax()],
                "bench_best_rank": int(order[top]), "median_FA_realised": float(X[f"FA_{b}"].median())})
res["D1_regret"] = reg
res["D1_share_budgets_bench_best_outside_top3"] = float(np.mean([r["bench_best_rank"] > 3 for r in reg]))
# D2 leave-one-family-out
lofo = {}
for fam, mem in FAM.items():
    Y = X[~X.detector.isin(mem)]
    if len(Y) == len(X): continue
    lofo[fam] = {"H9a_diff": float(kt(Y.EH, Y.CHA) - kt(Y.ET, Y.CHA)), "H9b_diff": float(kt(Y.CT, Y.CHA) - kt(Y.ET, Y.CHA))}
res["D2_leave_one_family_out"] = lofo
# D3 family medians
res["D3_family_median"] = {fam: {"ET": float(X[X.detector.isin(m)].ET.median()), "CHA": float(X[X.detector.isin(m)].CHA.median())}
                          for fam, m in FAM.items() if X.detector.isin(m).any()}
json.dump(res, open(f"{OUTD}/{DS}_{VER}_seed{SEED}.json", "w"), indent=1, default=float)
print(json.dumps(res, indent=1, default=float)[:3000])
