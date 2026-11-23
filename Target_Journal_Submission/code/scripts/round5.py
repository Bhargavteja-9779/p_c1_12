"""Round 5 (pre-registered in experiments/novelty_escalation_log.md), M1 only unless stated.
  calib METHOD M      F17: online substation-calibrated evidence e = -log10 p, p = exceedance probability of the
                      raw score under the substation's own past scores (<= 365 d before each 90-day block,
                      known exclusions removed, >= 14 d needed). Stored as method 'cal_<METHOD>'.
  table METHOD[,..]   best recall at budgets on M1 over the shared c grid; tau grid depends on the score scale.
  fuse A B            budget-split OR-fusion of A and B on M1 (Pareto pairs), as in round 4.
  noisy A [B]         FA share of the 5 noisiest substations at B = 2 (H5b)."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from src.data import predist as P
from src.evaluation import continuous as C, runner as R
from src.models import online as O

REF_DAYS, MIN_REF_DAYS = 365, 14
CAL_TAUS = (2.0, 2.5, 3.0, 4.0)
BUDGETS = (1, 2, 4)
OUT = "results/round5"; os.makedirs(OUT, exist_ok=True)


def calibrate(raw: pd.Series, lab) -> pd.Series:
    idx, v = raw.index, raw.to_numpy(float)
    out = np.full(len(v), np.nan)
    t = lab.start
    while t <= lab.end:
        te = (idx >= t) & (idx < t + pd.Timedelta(days=O.RETRAIN_DAYS))
        ref = O.train_mask(idx, t, lab) & (idx >= t - pd.Timedelta(days=REF_DAYS)) & ~np.isnan(v)
        if te.any() and ref.sum() >= MIN_REF_DAYS * 144 * 0.5:
            r = np.sort(v[ref]); n = len(r)
            x = v[te]
            n_ge = n - np.searchsorted(r, x, side="left")
            e = -np.log10((1 + n_ge) / (1 + n))
            e[np.isnan(x)] = np.nan
            out[te] = e
        t += pd.Timedelta(days=O.RETRAIN_DAYS)
    return pd.Series(out, index=idx)


def taus_of(method):
    return CAL_TAUS if method.startswith("cal_") else R.TAU_GRID


def table(methods):
    rows, curves = [], []
    for m in methods:
        t, c = R.best_at_budgets(m, 1, taus=taus_of(m)); c["method"] = m
        rows.append(t); curves.append(c)
        print(t[["method", "budget", "tau", "c_thr", "recall", "fa_per_sub_year", "median_lead_h"]].round(3).to_string(index=False, header=False), flush=True)
    tag = "_".join(methods)
    pd.concat(rows).to_csv(f"{OUT}/m1_table_{tag}.csv", index=False)
    pd.concat(curves).to_csv(f"{OUT}/m1_curves_{tag}.csv", index=False)


def _curve(method):
    fs = [f for f in os.listdir(OUT) if f.startswith("m1_curves_")] + ["../m1_curves.csv", "../m1_curves_aeseeds.csv"]
    for f in fs:
        d = pd.read_csv(os.path.join(OUT, f))
        if (d.method == method).any():
            return d[d.method == method]
    raise SystemExit(f"no M1 curve for {method}: run 'table {method}' first")


def pareto(method, fa_max=6.0):
    g = _curve(method); g = g[g.fa_per_sub_year <= fa_max].sort_values(["fa_per_sub_year", "recall"], ascending=[True, False])
    out, best = [], -1
    for _, r in g.iterrows():
        if r.recall > best:
            out.append((float(r.tau), int(r.c_thr))); best = r.recall
    return out


def alarms(method, pts, m=1):
    out = {p: {} for p in pts}
    for s in P.substations(m):
        sc = R.load_scores(method, m, s)
        cnt = {t: O.criticality_counter(sc, t) for t in {p[0] for p in pts}}
        for p in pts:
            out[p][s] = pd.Series(cnt[p[0]] >= p[1], index=sc.index)
    return out


def labels(m=1):
    return {s: C.substation_labels(m, s, R.load_scores("rule", m, s).index) for s in P.substations(m)}


def fuse(a, b):
    labs = labels()
    pa, pb = pareto(a), pareto(b)
    A, Bm = alarms(a, pa), alarms(b, pb)
    rows = []
    for x in pa:
        for y in pb:
            res = [C.evaluate_substation(A[x][s] | Bm[y][s].reindex(A[x][s].index, fill_value=False), labs[s]) for s in labs]
            r = C.summarise(res); r.update(a=a, b=b, a_tau=x[0], a_c=x[1], b_tau=y[0], b_c=y[1]); rows.append(r)
    full = pd.DataFrame(rows)
    full.to_csv(f"{OUT}/fuse_grid_{a}__{b}.csv", index=False)
    best = []
    for B in BUDGETS:
        ok = full[full.fa_per_sub_year <= B].sort_values(["recall", "fa_per_sub_year"], ascending=[False, True])
        r = ok.iloc[0].to_dict(); r["budget"] = B; best.append(r)
    best = pd.DataFrame(best); best.to_csv(f"{OUT}/fuse_best_{a}__{b}.csv", index=False)
    print(f"pairs {len(pa)}x{len(pb)}")
    print(best[["budget", "a_tau", "a_c", "b_tau", "b_c", "recall", "fa_per_sub_year", "n_false_alarms", "median_lead_h"]].round(3).to_string(index=False))


def noisy(spec_a, spec_b=None):
    """spec = method:tau:c . FA share of the 5 noisiest substations."""
    labs = labels(); per = {}
    def al(spec, s):
        m, t, c = spec.split(":"); sc = R.load_scores(m, 1, s)
        return pd.Series(O.criticality_counter(sc, float(t)) >= int(c), index=sc.index)
    for s in labs:
        a = al(spec_a, s)
        if spec_b: a = a | al(spec_b, s).reindex(a.index, fill_value=False)
        per[s] = len(C.evaluate_substation(a, labs[s])["false_alarms"])
    v = pd.Series(per).sort_values(ascending=False)
    print(spec_a, spec_b, "total FA", v.sum(), "top5 share", round(v.iloc[:5].sum() / max(1, v.sum()), 3), "subs with 0 FA", (v == 0).sum())
    return v


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "calib":
        meth, m = sys.argv[2], int(sys.argv[3])
        def scorer(X, lab, meth=meth, m=m):
            raw = R.load_scores(meth, m, lab.sub)
            return calibrate(raw.reindex(X.index), lab)
        R.compute_scores(f"cal_{meth}", m, scorer)
    elif cmd == "table":
        table(sys.argv[2].split(","))
    elif cmd == "fuse":
        fuse(sys.argv[2], sys.argv[3])
    elif cmd == "noisy":
        noisy(*sys.argv[2:])
