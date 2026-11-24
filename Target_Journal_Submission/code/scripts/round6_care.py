"""Round 6 (pre-registered H6a-e, Amendment A1): balanced event protocol vs continuous protocol on CARE wind SCADA.
Usage: round6_care.py [seed_tag]     seed_tag: "0" (pre-registered run, default) or a confirmation seed (100..104).
Unseeded methods (sigma3, temp3s) are identical across seed tags. Writes results/round6/<tag>/.
Everything is computed from the online score files in results/scores_care/ (no model fitting here)."""
import sys, os, json; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from scipy.stats import kendalltau, spearmanr, binom, beta
from src.data import care
from src.evaluation import care_eval as CE, continuous as C
from src.models import online as O
from src.evaluation.runner import TAU_GRID

TAG = sys.argv[1] if len(sys.argv) > 1 else "0"
SEEDED = ("iforest", "ae", "ae_cond")
METHODS = ["temp3s", "sigma3", "iforest", "ae", "ae_cond"]
C_GRID = [1, 2, 3, 6, 9, 12, 18, 24, 36, 48, 72, 96, 144, 216, 288]
BUDGETS = (1, 2, 4)
NBOOT, RNG = 2000, np.random.default_rng(0)
OUT = f"results/round6/seed{TAG}"; os.makedirs(OUT, exist_ok=True)
name = lambda m: m if (TAG == "0" or m not in SEEDED) else f"{m}_seed{TAG}"
ASSETS = [(f, a) for f in care.FARMS for a in care.assets(f)]


def per_asset_tables(meth):
    """cont: one row per (asset, tau, c): n_tgt, n_det, n_fa, expo_days.  ev: one row per (asset, event, tau): max_cnt.
    Also per-asset alarm series are summarised for the random-window selection test (H6c)."""
    cont, ev, selw = [], [], {}
    for f, a in ASSETS:
        sc = CE.load_scores(name(meth), f, a)
        lab = CE.labels(f, a, sc.index)
        E = care.events(f); E = E[E.asset == a]
        for tau in TAU_GRID:
            cnt = pd.Series(O.criticality_counter(sc, tau), index=sc.index)
            for e in E.itertuples():
                w = (cnt.index >= e.event_start) & (cnt.index < e.event_end)
                ev.append({"farm": f, "asset": a, "event_id": e.event_id, "y": int(e.event_label == "anomaly"),
                           "tau": tau, "max_cnt": int(cnt[w].max()) if w.any() else 0,
                           "coverage": float(sc[w].notna().mean()) if w.any() else 0.0,
                           "len_d": (e.event_end - e.event_start).total_seconds() / 86400})
            for c in C_GRID:
                r = C.evaluate_substation(cnt >= c, lab)
                cont.append({"farm": f, "asset": a, "tau": tau, "c_thr": c, "n_tgt": len(r["detections"]),
                             "n_det": sum(d["detected"] for d in r["detections"]), "n_fa": len(r["false_alarms"]),
                             "expo_days": r["exposure_days"]})
        selw[(f, a)] = (sc, lab)
    return pd.DataFrame(cont), pd.DataFrame(ev), selw


def pool(df):
    g = df[["n_tgt", "n_det", "n_fa", "expo_days"]].sum()
    rec = g.n_det / g.n_tgt if g.n_tgt else np.nan
    fa = g.n_fa / (g.expo_days / 365.25) if g.expo_days else np.nan
    return rec, fa, g.n_det / max(1, g.n_det + g.n_fa)


def lofo_points(cont, B):
    """Leave-one-farm-out: (tau, c) maximising pooled recall s.t. FA/turbine-yr <= B on the other farms."""
    pts = {}
    for F in care.FARMS:
        tr = cont[cont.farm != F]
        best = None
        for (tau, c), g in tr.groupby(["tau", "c_thr"]):
            rec, fa, _ = pool(g)
            if fa <= B and (best is None or (rec, -fa) > (best[0], -best[1])):
                best = (rec, fa, tau, c)
        pts[F] = (best[2], best[3]) if best else (max(TAU_GRID), max(C_GRID))
    return pts


def apply_points(cont, pts, assets=None):
    rows = [cont[(cont.farm == F) & (cont.tau == t) & (cont.c_thr == c)] for F, (t, c) in pts.items()]
    d = pd.concat(rows)
    if assets is not None:  # bootstrap resample (with multiplicity)
        d = pd.concat([d[(d.farm == f) & (d.asset == a)] for f, a in assets])
    return d


def ev_metrics(pred, y, beta_=0.5):
    tp = int(((pred == 1) & (y == 1)).sum()); fp = int(((pred == 1) & (y == 0)).sum()); fn = int(((pred == 0) & (y == 1)).sum())
    p = tp / (tp + fp) if tp + fp else 0.0; r = tp / (tp + fn) if tp + fn else 0.0
    f = (1 + beta_**2) * p * r / (beta_**2 * p + r) if p + r else 0.0
    return p, r, f


def ev_best(ev):
    best = None
    for tau, g in ev.groupby("tau"):
        y = g.y.values; mc = g.max_cnt.values
        for c in C_GRID:
            p, r, f = ev_metrics((mc >= c).astype(int), y)
            if best is None or (f, r) > (best[2], best[1]):
                best = (p, r, f, tau, c)
    return best


def selection_test(selw, pts, ev, n=2000, length_matched=False):
    """H6c: alarm-hit rate on CARE normal events vs random eligible windows of normal time (same assets, same scores)."""
    normal = ev[(ev.y == 0) & (ev.tau == TAU_GRID[0])]
    lens = normal.len_d.values
    rng = np.random.default_rng(0)
    hits_evt, hits_rnd, per_asset = [], [], {}
    keys = list(selw); cc = {}
    for i in range(n):
        f, a = keys[rng.integers(len(keys))]
        sc, lab = selw[(f, a)]; tau, c = pts[f]
        L = pd.Timedelta(days=float(rng.choice(lens)) if length_matched else 7.0)
        lo, hi = lab.start, lab.end - L
        if hi <= lo:
            continue
        s = lo + (hi - lo) * rng.random()
        blocked = list(zip(lab.targets.win_start, lab.targets.report)) + lab.exclusions
        if any(a0 < s + L and s < b0 for a0, b0 in blocked):
            continue
        w = (sc.index >= s) & (sc.index < s + L)
        if not w.any() or sc[w].notna().mean() < 0.5:
            continue
        if (f, a, tau) not in cc: cc[(f, a, tau)] = O.criticality_counter(sc, tau)
        cnt = cc[(f, a, tau)]
        hits_rnd.append((f, a, int(cnt[w].max() >= c)))
    for e in normal.itertuples():
        tau, c = pts[e.farm]
        g = ev[(ev.asset == e.asset) & (ev.farm == e.farm) & (ev.event_id == e.event_id) & (ev.tau == tau)]
        hits_evt.append((e.farm, e.asset, int(g.max_cnt.iloc[0] >= c)))
    he = pd.DataFrame(hits_evt, columns=["farm", "asset", "hit"]); hr = pd.DataFrame(hits_rnd, columns=["farm", "asset", "hit"])
    rr = he.hit.mean() / hr.hit.mean() if hr.hit.mean() > 0 else np.nan
    boots = []
    A = sorted(set(map(tuple, he[["farm", "asset"]].values)) | set(map(tuple, hr[["farm", "asset"]].values)))
    for _ in range(NBOOT):
        smp = [A[j] for j in RNG.integers(len(A), size=len(A))]
        e_ = pd.concat([he[(he.farm == f) & (he.asset == a)] for f, a in smp]); r_ = pd.concat([hr[(hr.farm == f) & (hr.asset == a)] for f, a in smp])
        if len(e_) and len(r_) and r_.hit.mean() > 0:
            boots.append(e_.hit.mean() / r_.hit.mean())
    lo, hi = (np.percentile(boots, [2.5, 97.5]) if boots else (np.nan, np.nan))
    return {"normal_event_hit_rate": he.hit.mean(), "random_window_hit_rate": hr.hit.mean(), "n_normal_events": len(he),
            "n_random_windows": len(hr), "rate_ratio": rr, "rr_ci_lo": lo, "rr_ci_hi": hi}


def power(n, l0, l1, L, a=0.05):
    p = lambda lam: 1 - np.exp(-lam * L / 365.25)
    k = int(binom.isf(a, n, p(l0))) + 1
    while binom.sf(k - 1, n, p(l0)) > a: k += 1
    return binom.sf(k - 1, n, p(l1))


rows, details = [], {}
for meth in METHODS:
    cont, ev, selw = per_asset_tables(meth)
    cont.to_csv(f"{OUT}/cont_grid_{meth}.csv", index=False); ev.to_csv(f"{OUT}/event_maxcnt_{meth}.csv", index=False)
    r = {"method": meth, "score_name": name(meth)}
    for B in BUDGETS:
        pts = lofo_points(cont, B); d = apply_points(cont, pts)
        rec, fa, prec = pool(d)
        r.update({f"lofo_rec_B{B}": rec, f"lofo_fa_B{B}": fa, f"lofo_prec_B{B}": prec, f"lofo_pts_B{B}": json.dumps({k: [float(v[0]), int(v[1])] for k, v in pts.items()})})
        if B == 2: pts2 = pts
    p, rc, f, tau, c = ev_best(ev)
    r.update({"E_best_prec": p, "E_best_rec": rc, "E_best_f05": f, "E_best_tau": tau, "E_best_c": c})
    # event protocol at the LOFO B=2 points (per farm)
    pe = np.array([int(g.max_cnt >= pts2[g.farm][1]) for g in ev[ev.apply(lambda x: x.tau == pts2[x.farm][0], axis=1)].itertuples()])
    ye = ev[ev.apply(lambda x: x.tau == pts2[x.farm][0], axis=1)].y.values
    p2, r2, f2 = ev_metrics(pe, ye); r.update({"E_atB2_prec": p2, "E_atB2_rec": r2, "E_atB2_f05": f2})
    # continuous consequences of the benchmark-chosen point (same (tau,c) on all farms)
    rec_e, fa_e, prec_e = pool(cont[(cont.tau == tau) & (cont.c_thr == c)])
    r.update({"cont_rec_at_Ebest": rec_e, "cont_fa_at_Ebest": fa_e, "cont_prec_at_Ebest": prec_e})
    r["prec_inflation"] = p / r["lofo_prec_B2"] if r["lofo_prec_B2"] > 0 else np.inf
    # H6e bootstrap over assets (event-protocol best point re-tuned inside each resample, LOFO points fixed)
    bs = []
    for _ in range(NBOOT):
        smp = [ASSETS[j] for j in RNG.integers(len(ASSETS), size=len(ASSETS))]
        evb = pd.concat([ev[(ev.farm == f_) & (ev.asset == a_)] for f_, a_ in smp])
        if evb.y.sum() == 0:
            continue
        pb = ev_best(evb)[0]; _, _, cpb = pool(apply_points(cont, pts2, smp))
        bs.append(pb / cpb if cpb > 0 else np.inf)
    bs = np.array(bs)
    r.update({"infl_ci_lo": float(np.percentile(bs, 2.5)), "infl_ci_hi": float(np.percentile(bs, 97.5)),
              "infl_p_le5": float((bs <= 5).mean()), "n_boot": len(bs)})
    r.update({f"sel_{k}": v for k, v in selection_test(selw, pts2, ev).items()})
    r.update({f"selLM_{k}": v for k, v in selection_test(selw, pts2, ev, length_matched=True).items()})
    r["n_events"] = int((ev.tau == TAU_GRID[0]).sum()); r["n_anomaly_events"] = int(ev[ev.tau == TAU_GRID[0]].y.sum())
    r["mean_event_coverage"] = float(ev.coverage.mean())
    rows.append(r); print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()}, flush=True)

R = pd.DataFrame(rows)
# Holm over methods for H6e (one-sided bootstrap p for ratio <= 5)
o = np.argsort(R.infl_p_le5.values); m = len(R); holm = np.empty(m); run = 0
for i, j in enumerate(o):
    run = max(run, min(1, (m - i) * R.infl_p_le5.values[j])); holm[j] = run
R["infl_p_holm"] = holm
R.to_csv(f"{OUT}/protocol_compare_care.csv", index=False)
kt = kendalltau(R.E_best_f05, R.lofo_rec_B2); sp = spearmanr(R.E_best_f05, R.lofo_rec_B2)
kt2 = kendalltau(R.E_atB2_f05, R.lofo_rec_B2)
n_norm = int(R.n_events.iloc[0] - R.n_anomaly_events.iloc[0])
normal_len = pd.read_csv(f"{OUT}/event_maxcnt_{METHODS[0]}.csv").query("y == 0 and tau == @TAU_GRID[0]").len_d
summ = {"tag": TAG, "kendall_tau_Ebest_vs_lofoB2": kt.statistic, "kendall_p": kt.pvalue, "spearman": sp.statistic,
        "kendall_tau_EatB2_vs_lofoB2": kt2.statistic, "H6a_supported": bool(kt.statistic < 0.5),
        "H6b_min_inflation": float(R.prec_inflation.min()), "H6b_supported": bool((R.prec_inflation >= 5).all()),
        "H6c_rate_ratios": R.sel_rate_ratio.round(3).tolist(), "H6c_ci_hi": R.sel_rr_ci_hi.round(3).tolist(),
        "H6c_supported_methods": int(((R.sel_rate_ratio < 1) & (R.sel_rr_ci_hi < 1)).sum()),
        "H6d_n_normal_events": n_norm, "H6d_power_1v2_7d": power(n_norm, 1, 2, 7.0),
        "H6d_power_1v2_meanlen": power(n_norm, 1, 2, float(normal_len.mean())), "normal_event_mean_len_d": float(normal_len.mean()),
        "H6d_supported": bool(power(n_norm, 1, 2, 7.0) < 0.5),
        "H6e_min_ci_lo": float(R.infl_ci_lo.min()), "H6e_supported": bool(((R.infl_ci_lo > 5) & (R.infl_p_holm < 0.05)).all())}
json.dump(summ, open(f"{OUT}/summary.json", "w"), indent=1, default=float)
print(R[["method", "E_best_f05", "E_best_prec", "lofo_rec_B2", "lofo_fa_B2", "lofo_prec_B2", "prec_inflation", "infl_ci_lo", "infl_ci_hi", "cont_fa_at_Ebest", "sel_rate_ratio"]].round(3).to_string(index=False))
print(json.dumps(summ, indent=1, default=float))
