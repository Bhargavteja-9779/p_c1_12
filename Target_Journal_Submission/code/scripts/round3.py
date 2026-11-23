"""Round 3 (pre-registered in experiments/novelty_escalation_log.md): F10 daily decision unit, F13 substation
conformal FA-budget threshold, F12 under-delivery channel fused at the daily level. M1 development only.
Usage: round3.py [base_score_name]   (default srcr_comp__v_gate_1s_local)"""
import sys, os, math, json; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from src.data import predist as P
from src.evaluation import continuous as C, runner as R
from src.models import online as O
from src.models.srcr import normal_mask
from src.models.fusion import m1_folds, level

BASE = sys.argv[1] if len(sys.argv) > 1 else "srcr_comp__v_gate_1s_local"
M = 1
MIN_STEPS = 72          # >= half a day of valid 10-min scores
Q = 0.9                 # daily score = 90th percentile of 10-min scores
OWN_DAYS, MIN_OWN = 365, 60
HEAT_SEASON_T = 15.0
OUT = "results/round3"; os.makedirs(OUT, exist_ok=True)


def daily(sc: pd.Series) -> pd.Series:
    """Daily score stamped at the END of the day (decision available at 00:00 of the next day)."""
    g = sc.resample("D")
    d = g.quantile(Q).where(g.count() >= MIN_STEPS)
    d.index = d.index + pd.Timedelta(days=1)
    return d


def day_normal(d: pd.Series, lab) -> np.ndarray:
    """Normal-day mask using the whole label set (for fleet pools of OTHER substations only)."""
    mid = d.index - pd.Timedelta(hours=12)
    return normal_mask(mid, lab) & (mid >= lab.start)


def evaluate(alarm_by_sub: dict, labs: dict) -> tuple[dict, list]:
    res = [C.evaluate_substation(alarm_by_sub[s], labs[s]) for s in alarm_by_sub]
    return C.summarise(res), res


def to_alarm(d: pd.Series, mask) -> pd.Series:
    return pd.Series(np.asarray(mask, bool) & d.notna().to_numpy(), index=d.index)


def worst5_share(res, subs):
    fa = pd.Series([len(r["false_alarms"]) for r in res], index=subs).sort_values(ascending=False)
    return float(fa.iloc[:5].sum() / max(1, fa.sum())), fa


def sweep(D: dict, labs: dict, name: str, budgets=(1, 2, 4)):
    allv = np.concatenate([v.dropna().to_numpy() for v in D.values()])
    grid = np.unique(np.quantile(allv, np.concatenate([np.linspace(0.90, 0.99, 46), np.linspace(0.9905, 0.99995, 60)])))
    rows = []
    for th in grid:
        r, _ = evaluate({s: to_alarm(d, d.to_numpy() > th) for s, d in D.items()}, labs)
        r["threshold"] = th; rows.append(r)
    curve = pd.DataFrame(rows)
    best = []
    for B in budgets:
        ok = curve[curve.fa_per_sub_year <= B].sort_values(["recall", "fa_per_sub_year"], ascending=[False, True])
        r = ok.iloc[0].to_dict() if len(ok) else {"recall": 0.0}
        _, res = evaluate({s: to_alarm(d, d.to_numpy() > r.get("threshold", np.inf)) for s, d in D.items()}, labs)
        r["worst5_fa_share"] = worst5_share(res, list(D))[0]
        r.update(budget=B, method=name); best.append(r)
    curve["method"] = name
    return pd.DataFrame(best), curve


def conformal(D: dict, labs: dict, folds, B: float, fallback_when_k_gt_n=False):
    """F13. Own past normal days (known exclusions only) or, with < MIN_OWN own days, fleet pool."""
    alpha = B / 365.25
    alarms, src_count = {}, {"own": 0, "fleet": 0, "none": 0}
    for test in folds:
        train = [s for s in D if s not in test]
        pool = np.sort(np.concatenate([D[s][day_normal(D[s], labs[s])].dropna().to_numpy() for s in train]))
        kf = math.ceil((len(pool) + 1) * (1 - alpha))
        th_fleet = pool[kf - 1] if kf <= len(pool) else np.inf
        for s in test:
            d, lab = D[s], labs[s]
            vals, idx = d.to_numpy(), d.index
            th = np.full(len(d), np.inf)
            for i, t in enumerate(idx):
                if not np.isfinite(vals[i]):
                    continue
                lo = t - pd.Timedelta(days=OWN_DAYS)
                j0 = idx.searchsorted(lo); past = np.arange(j0, i)
                if len(past):
                    mid = idx[past] - pd.Timedelta(hours=12)
                    ok = np.isfinite(vals[past])
                    for a, b in O.known_exclusions(lab, t):
                        ok &= ~((mid >= a) & (mid < b))
                    own = np.sort(vals[past][ok])
                else:
                    own = np.array([])
                n = len(own)
                if n < MIN_OWN:
                    th[i] = th_fleet; src_count["fleet"] += 1
                else:
                    k = math.ceil((n + 1) * (1 - alpha))
                    if k <= n:
                        th[i] = own[k - 1]; src_count["own"] += 1
                    elif fallback_when_k_gt_n:
                        th[i] = th_fleet; src_count["fleet"] += 1
                    else:
                        src_count["none"] += 1
            alarms[s] = to_alarm(d, vals > th)
    return alarms, src_count


if __name__ == "__main__":
    subs = P.substations(M)
    folds = m1_folds()
    labs, D = {}, {}
    for s in subs:
        sc = R.load_scores(BASE, M, s)
        labs[s] = C.substation_labels(M, s, sc.index)
        D[s] = daily(sc)
    summary = {}
    # ---- F10: daily unit, global threshold
    t10, c10 = sweep(D, labs, "F10_daily")
    print(t10[["method", "budget", "threshold", "recall", "fa_per_sub_year", "n_false_alarms", "worst5_fa_share"]].round(3).to_string(index=False), flush=True)
    # ---- 10-min reference worst-5 share for R2 at B=2
    tab, _ = R.best_at_budgets(BASE, M, budgets=(2,))
    r = tab.iloc[0]
    res = []
    for s in subs:
        sc = R.load_scores(BASE, M, s)
        k = O.criticality_counter(sc, r["tau"])
        res.append(C.evaluate_substation(pd.Series(k >= r["c_thr"], index=sc.index), labs[s]))
    summary["R2_10min_B2"] = {"recall": float(r["recall"]), "fa": float(r["fa_per_sub_year"]),
                              "worst5_fa_share": worst5_share(res, subs)[0]}
    print("R2 10-min at B=2:", summary["R2_10min_B2"], flush=True)
    # ---- F13: conformal per-substation thresholds
    rows = []
    for fb in (False, True):
        for B in (1, 2, 4):
            al, cnt = conformal(D, labs, folds, B, fallback_when_k_gt_n=fb)
            r, res = evaluate(al, labs)
            w5, fa = worst5_share(res, subs)
            r.update(method="F13_conformal" + ("_fallback(post-hoc)" if fb else ""), budget=B, worst5_fa_share=w5,
                     frac_days_own=cnt["own"] / max(1, sum(cnt.values())), frac_days_none=cnt["none"] / max(1, sum(cnt.values())))
            rows.append(r)
    t13 = pd.DataFrame(rows)
    print(t13[["method", "budget", "recall", "fa_per_sub_year", "n_false_alarms", "worst5_fa_share", "frac_days_own", "frac_days_none"]].round(3).to_string(index=False), flush=True)
    # ---- F12: under-delivery channel (heating season), fused at the daily level by surprise levels
    t12 = None
    if all(os.path.exists(os.path.join(R.score_path("underdel", M), f"s{s}.parquet")) for s in subs):
        U = {}
        for s in subs:
            u = R.load_scores("underdel", M, s)
            to24 = P.load_substation(M, s)["outdoor_temperature"].resample("D").mean()
            to24.index = to24.index + pd.Timedelta(days=1)
            du = daily(u)
            U[s] = du.where(to24.reindex(du.index) < HEAT_SEASON_T)
        F = {}
        for test in folds:
            train = [s for s in subs if s not in test]
            cal = {k: np.sort(np.concatenate([X[s][day_normal(X[s], labs[s])].dropna().to_numpy() for s in train]))
                   for k, X in (("R2", D), ("U", U))}
            for s in test:
                l1 = level(D[s].to_numpy(float), cal["R2"])
                l2 = level(U[s].reindex(D[s].index).to_numpy(float), cal["U"])
                F[s] = pd.Series(np.fmax(l1, l2), index=D[s].index)
        t12, c12 = sweep(F, labs, "F12_daily_R2+underdel")
        tu, cu = sweep(U, labs, "underdel_alone_daily")
        t12 = pd.concat([t12, tu])
        print(t12[["method", "budget", "threshold", "recall", "fa_per_sub_year", "n_false_alarms", "worst5_fa_share"]].round(3).to_string(index=False), flush=True)
    else:
        print("underdel scores missing; F12 skipped", flush=True)
    out = pd.concat([x for x in (t10, t13, t12) if x is not None], ignore_index=True)
    out.to_csv(f"{OUT}/round3_{BASE}.csv", index=False)
    c10.to_csv(f"{OUT}/curve_F10_{BASE}.csv", index=False)
    json.dump(summary, open(f"{OUT}/summary_{BASE}.json", "w"), indent=1)
