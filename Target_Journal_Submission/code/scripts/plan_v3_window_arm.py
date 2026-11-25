"""plan_v3 arm 1 (experiments/plan_v3.md): window-level oracle-threshold protocol vs deployment reference.
Usage: plan_v3_window_arm.py {predist1|care}   (seed-0 panel; needs results/plan_v2/<ds>/seed0/ch_per_asset.csv)
Writes results/plan_v3/<ds>/. Committed before it was run on real scores."""
import sys, os, json; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from scipy.stats import kendalltau
from sklearn.metrics import roc_auc_score
from src.models.panel import GENERIC

DS = sys.argv[1]; SEED = 0; NBOOT = 2000
OUT = f"results/plan_v3/{DS}"; os.makedirs(OUT, exist_ok=True)
if DS == "care":
    from src.data import care
    from src.evaluation import care_eval as CE
    ASSETS = [(f, a) for f in care.FARMS for a in care.assets(f)]; aname = lambda k: f"{k[0]}_{k[1]}"
    EXTRA = ["temp3s", "ae", "ae_cond"]
    load = lambda d, k: (pd.read_parquet(f"results/scores_panel/care/seed0/{d}/{aname(k)}.parquet")["score"] if d in GENERIC else CE.load_scores(d, *k))
    labels = lambda k, idx: CE.labels(k[0], k[1], idx)
else:
    from src.data import predist as P
    from src.evaluation import continuous as C, runner as R
    M = int(DS[-1]); ASSETS = P.substations(M); aname = lambda s: f"s{s}"
    EXTRA = ["rule", "loop3s", "qnbm", "ae", "ae_cond"]
    load = lambda d, s: (pd.read_parquet(f"results/scores_panel/{DS}/seed0/{d}/s{s}.parquet")["score"] if d in GENERIC else R.load_scores(d, M, s))
    labels = lambda s, idx: C.substation_labels(M, s, idx)
DETS = GENERIC + EXTRA


def days(k):
    """day table for one asset: index day, y (1 faulty / 0 normal), dropped otherwise; based on z_max coverage."""
    sc = load("z_max", k); lab = labels(k, sc.index)
    sc = sc[(sc.index >= lab.start) & (sc.index <= lab.end)]
    cov = sc.notna().groupby(sc.index.floor("D")).mean()
    D = pd.DataFrame({"cov": cov}); D = D[D["cov"] >= 0.5]
    tw = list(zip(lab.targets.win_start, lab.targets.report))
    ov = lambda d, iv: any(a < d + pd.Timedelta(days=1) and d < b for a, b in iv)
    D["y"] = [1 if ov(d, tw) else (0 if not ov(d, lab.exclusions) else -1) for d in D.index]
    return D[D.y >= 0]


DAYS = {aname(k): days(k) for k in ASSETS}
rows = []
for k in ASSETS:
    n = aname(k); D = DAYS[n]
    for d in DETS:
        try:
            sc = load(d, k)
        except FileNotFoundError:
            sc = pd.Series(np.nan, index=D.index)
        mx = sc.groupby(sc.index.floor("D")).max().reindex(D.index)
        for day, y, v in zip(D.index, D.y, mx.values):
            rows.append((d, n, day, y, v))
T = pd.DataFrame(rows, columns=["det", "asset", "day", "y", "s"]); T["s"] = T.s.fillna(-1.0)
base = T[T.det == DETS[0]][["asset", "day", "y"]].reset_index(drop=True)
rng = np.random.default_rng(0)
fault_idx = base.index[base.y == 1]; norm_idx = base.index[base.y == 0]
bal_idx = np.concatenate([fault_idx, rng.choice(norm_idx, size=min(len(fault_idx), len(norm_idx)), replace=False)])
BAL = np.zeros(len(base), bool); BAL[bal_idx] = True
asset_years = {a: (g.y == 0).sum() / 365.25 for a, g in base.groupby("asset")}


def macro_f1(y, pred):
    out = []
    for c in (1, 0):
        tp = ((pred == c) & (y == c)).sum(); fp = ((pred == c) & (y != c)).sum(); fn = ((pred != c) & (y == c)).sum()
        out.append(2 * tp / (2 * tp + fp + fn) if tp + fp + fn else 0.0)
    return float(np.mean(out))


def oracle(y, s):
    best = (-1, None)
    for t in np.unique(np.quantile(s, np.linspace(0.5, 0.999, 120))):
        f = macro_f1(y, (s > t).astype(int))
        if f > best[0]: best = (f, t)
    return best


S = {d: T[T.det == d].s.values for d in DETS}; y = base.y.values; a_of = base.asset.values
res = []
for d in DETS:
    s = S[d]
    f_bal, t = oracle(y[BAL], s[BAL])
    f_nat_same = macro_f1(y, (s > t).astype(int))
    f_nat_orc, _ = oracle(y, s)
    fp_days = ((s > t) & (y == 0)); fa_day_rate = fp_days.sum() / ((y == 0).sum() / 365.25)
    auc = roc_auc_score(y[BAL], s[BAL]) if len(set(y[BAL])) == 2 else np.nan
    res.append({"detector": d, "W_bal_oracle_macroF1": f_bal, "W_nat_macroF1_same_thr": f_nat_same,
                "W_nat_oracle_macroF1": f_nat_orc, "prevalence_drop": f_bal - f_nat_same,
                "fa_days_per_asset_year": fa_day_rate, "auroc_bal": auc, "thr": t})
Rw = pd.DataFrame(res)
CH = pd.read_csv(f"results/plan_v2/{DS}/seed0/ch_per_asset.csv")
ch = CH.groupby("detector")[["n_tgt", "n_det"]].sum(); ch["CH"] = ch.n_det / ch.n_tgt.clip(lower=1e-9)
Rw = Rw.merge(ch[["CH"]], left_on="detector", right_index=True)
Rw.to_csv(f"{OUT}/window_arm.csv", index=False)
tau = kendalltau(Rw.W_bal_oracle_macroF1, Rw.CH).statistic
# cluster bootstrap over assets for tau (oracle re-tuned within resample; CH from per-asset contributions)
names = sorted(DAYS); bs = []
chp = {(r.detector, r.asset): (r.n_tgt, r.n_det) for r in CH.itertuples()}
for b in range(NBOOT):
    pick = rng.choice(names, len(names)); w = pd.Series(pick).value_counts()
    idx = np.concatenate([np.repeat(np.where(a_of == a)[0], c) for a, c in w.items()])
    bi = idx[BAL[idx]]
    if len(set(y[bi])) < 2: continue
    fb = [oracle(y[bi], S[d][bi])[0] for d in DETS]
    chb = [sum(chp[(d, a)][1] * c for a, c in w.items()) / max(1e-9, sum(chp[(d, a)][0] * c for a, c in w.items())) for d in DETS]
    bs.append(kendalltau(fb, chb).statistic)
    if b == 499 and DS == "care": pass
summ = {"dataset": DS, "n_days": int(len(base)), "n_faulty_days": int(y.sum()), "n_bal": int(BAL.sum()),
        "H8a_min_drop": float(Rw.prevalence_drop.min()), "H8a_supported": bool((Rw.prevalence_drop >= 0.15).all()),
        "H8b_share_ge10": float((Rw.fa_days_per_asset_year >= 10).mean()), "H8b_supported": bool((Rw.fa_days_per_asset_year >= 10).mean() >= 2 / 3),
        "H8c_tau": float(tau), "H8c_ci": [float(np.nanpercentile(bs, 2.5)), float(np.nanpercentile(bs, 97.5))], "n_boot": len(bs)}
summ["H8c_supported"] = bool(summ["H8c_ci"][1] < 0.5)
json.dump(summ, open(f"{OUT}/summary.json", "w"), indent=1)
print(Rw.round(3).to_string(index=False)); print(json.dumps(summ, indent=1))
