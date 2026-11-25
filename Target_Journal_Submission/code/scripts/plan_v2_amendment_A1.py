"""plan_v2 Amendment A1 (experiments/plan_v2_amendment_A1.md): null-centred bootstrap (T1) and within-detector
label-swap randomisation (T2) for H7a/H7b. Reads committed result files only. Run from code/."""
import json, os, numpy as np, pandas as pd
from scipy.stats import kendalltau

R = "results"; N_PERM = 20000; OUT = f"{R}/plan_v2/amendment_A1"; os.makedirs(OUT, exist_ok=True)


def tau(a, b):
    return kendalltau(a, b).statistic


def t2(cells, a, b):  # H1: tau(b, CH) - tau(a, CH) > 0
    x, y, ch = cells[a].to_numpy(float), cells[b].to_numpy(float), cells["CH"].to_numpy(float)
    d_hat = tau(y, ch) - tau(x, ch)
    rng = np.random.default_rng(0); cnt = 0
    for _ in range(N_PERM):
        s = rng.random(len(x)) < 0.5
        xx, yy = np.where(s, y, x), np.where(s, x, y)
        cnt += (tau(yy, ch) - tau(xx, ch)) >= d_hat - 1e-12
    return d_hat, (1 + cnt) / (N_PERM + 1)


def t1(boot, col, d_hat):
    d = boot[col].to_numpy(float)
    p = (1 + np.sum((d - d.mean()) >= d_hat)) / (len(d) + 1)
    q = np.percentile(d, [2.5, 97.5])
    return p, [2 * d_hat - q[1], 2 * d_hat - q[0]], float(d.mean())


rows = []
SRC = {("predist1", "legacy"): f"{R}/plan_v2/predist1/seed{{s}}", ("care", "primary"): f"{R}/plan_v2/care/seed{{s}}",
       ("predist1", "leakfree"): f"{R}/leak_sensitivity/leakfree_outputs/seed{{s}}"}
for (ds, ver), pat in SRC.items():
    for s in range(5):
        d = pat.format(s=s)
        if not os.path.exists(f"{d}/cells.csv"): continue
        cells = pd.read_csv(f"{d}/cells.csv"); summ = json.load(open(f"{d}/summary.json"))
        boot = pd.read_csv(f"{d}/bootstrap.csv") if os.path.exists(f"{d}/bootstrap.csv") else None
        for h, a, b, col in [("H7a", "ET", "EH", "dA"), ("H7b", "ET", "CT", "dB")]:
            d_hat, p2 = t2(cells, a, b)
            r = dict(dataset=ds, version=ver, seed=s, hyp=h, d_hat=d_hat, p_prereg=summ[f"{h}_p"], p_T2=p2)
            if boot is not None:
                p1, ci, m = t1(boot, col, d_hat); r.update(p_T1=p1, basic_ci_lo=ci[0], basic_ci_hi=ci[1], boot_mean=m)
            rows.append(r)
df = pd.DataFrame(rows); df.to_csv(f"{OUT}/tests.csv", index=False)


def holm(ps):
    o = np.argsort(ps); m = len(ps); rej = np.zeros(m, bool)
    for k, i in enumerate(o):
        if ps[i] <= 0.05 / (m - k): rej[i] = True
        else: break
    return rej


out = {}
for pd_ver in ["leakfree", "legacy"]:
    s0 = df[(df.seed == 0) & (((df.dataset == "predist1") & (df.version == pd_ver)) | (df.dataset == "care"))]
    s0 = s0.sort_values(["hyp", "dataset"]).reset_index(drop=True)
    res = {"tests": s0[["dataset", "hyp", "p_prereg", "p_T1", "p_T2"]].to_dict("records")}
    for t in ["p_T1", "p_T2"]:
        if s0[t].notna().all(): res[f"holm_{t}"] = dict(zip(s0.dataset + "_" + s0.hyp, holm(s0[t].to_numpy()).tolist()))
        else: res[f"holm_{t}"] = "not computable (bootstrap missing for this version)"
    out[f"predist_{pd_ver}"] = res
rob = {}
for (ds, ver), g in df.groupby(["dataset", "version"]):
    for h, gg in g.groupby("hyp"):
        both = (gg.p_T2 < 0.05) & ((gg.p_T1 < 0.05) if "p_T1" in gg and gg.p_T1.notna().all() else True)
        rob[f"{ds}_{ver}_{h}"] = f"{int(both.sum())}/{len(gg)} seeds (T2{' and T1' if 'p_T1' in gg and gg.p_T1.notna().all() else ' only'} < 0.05)"
out["robustness"] = rob
json.dump(out, open(f"{OUT}/summary.json", "w"), indent=1, default=str)
pd.set_option("display.width", 200)
print(df.round(4).to_string(index=False)); print(json.dumps(out, indent=1, default=str))
