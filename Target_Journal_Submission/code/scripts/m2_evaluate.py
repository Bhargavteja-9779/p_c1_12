"""Pre-registered locked-test analysis (protocol A4 + A5). Written and committed BEFORE any M2 detector output.

Usage: m2_evaluate.py M [n_boot]
  M = 2 : the single locked evaluation (thresholds chosen on M1, applied unchanged to M2).
  M = 1 : dry run on development data (in-sample; only to test this code).

For every factorial cell the (tau, c_thr) chosen on M1 for budgets B in {1, 2, 4} is applied to manufacturer M.
Per-substation outcomes are tabulated once over the full (tau, c_thr) grid so that cluster bootstrap replicates
(resampling substations with replacement) are cheap re-weightings.
Outputs: results/locked_m{M}_*.csv
"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from scipy.stats import binomtest, wilcoxon
from src.data import predist as P
from src.evaluation import continuous as C, runner as R
from src.evaluation.diagnose import fault_ranks
from src.models import online as O

if __name__ == "__main__":  # guarded so CELLS/holm can be imported by later analyses
    M = int(sys.argv[1]); NBOOT = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
C_GRID = [1, 2, 3, 6, 9, 12, 18, 24, 36, 48, 72, 96, 144, 216, 288]
# label: (M1 score name, M2 score name, scope, representation, model)
CELLS = {"rule": ("rule", "rule", "comfort", "relative", "rule"),
         "loop3s_c": ("loop3s_c", "loop3s_c", "comfort", "relative", "own-history stats"),
         "srcr_c": ("srcr_comp__v_g1l_noret", "srcr_c", "comfort", "relative", "fleet quantile ML"),
         "loop3s": ("loop3s", "loop3s", "all", "relative", "own-history stats"),
         "srcr_all": ("srcr_comp__v_gate_1s_local", "srcr_all", "all", "relative", "fleet quantile ML"),
         "ae_comfort": ("ae_comfort", "ae_comfort", "comfort", "absolute", "AE"),
         "sigma3": ("sigma3", "sigma3", "all", "absolute", "own-history stats"),
         "iforest": ("iforest", "iforest", "all", "absolute", "iForest"),
         "qnbm": ("qnbm", "qnbm", "all", "absolute", "own quantile NBM"),
         "ae": ("ae", "ae", "all", "absolute", "AE"),
         "ae_cond": ("ae_cond", "ae_cond", "all", "absolute", "AE (conditional)")}
HF1 = [("srcr_c", "srcr_all"), ("loop3s_c", "loop3s"), ("ae_comfort", "ae")]
HF2 = [("loop3s_c", "ae_comfort"), ("srcr_c", "ae_comfort")]
HF3 = [("srcr_c", "rule"), ("srcr_c", "loop3s_c"), ("loop3s_c", "rule")]
BUDGETS = (1, 2, 4)
name_on = lambda cell, m: CELLS[cell][0] if m == 1 else CELLS[cell][1]


def tabulate(name, m):
    """Per (tau, c_thr, sub): n_fa, exposure_days; per (tau, c_thr, event): detected."""
    subs_rows, det_rows = [], []
    for s in P.substations(m):
        sc = R.load_scores(name, m, s); lab = C.substation_labels(m, s, sc.index)
        for tau in R.TAU_GRID:
            k = O.criticality_counter(sc, tau)
            for c in C_GRID:
                r = C.evaluate_substation(pd.Series(k >= c, index=sc.index), lab)
                subs_rows.append((tau, c, s, len(r["false_alarms"]), r["exposure_days"]))
                det_rows += [(tau, c, s, d["event_id"], d["detected"]) for d in r["detections"]]
    S = pd.DataFrame(subs_rows, columns=["tau", "c_thr", "sub", "n_fa", "expo"])
    D = pd.DataFrame(det_rows, columns=["tau", "c_thr", "sub", "event_id", "detected"])
    return S, D


def curve(S, D, w):
    """Operating curve under substation weights w (dict sub -> multiplicity)."""
    ws = S["sub"].map(w).fillna(0); wd = D["sub"].map(w).fillna(0)
    fa = (S.n_fa * ws).groupby([S.tau, S.c_thr]).sum(); ex = (S.expo * ws).groupby([S.tau, S.c_thr]).sum() / 365.25
    det = (D.detected * wd).groupby([D.tau, D.c_thr]).sum(); nf = wd.groupby([D.tau, D.c_thr]).sum()
    return pd.DataFrame({"recall": det / nf, "fa": fa / ex, "n_fa": fa, "expo_y": ex})


def min_fa_at(cv, r):
    ok = cv[cv.recall >= r - 1e-9]
    return ok.fa.min() if len(ok) else np.inf


def holm(p):
    p = np.asarray(p, float); o = np.argsort(p); adj = np.empty_like(p); run = 0
    for i, j in enumerate(o):
        run = max(run, min(1, (len(p) - i) * p[j])); adj[j] = run
    return adj


def main():
    rng = np.random.default_rng(20261123)
    # 1. operating points chosen on M1 (development)
    chosen = {}
    for cell in CELLS:
        t, _ = R.best_at_budgets(name_on(cell, 1), 1)
        chosen[cell] = {int(r.budget): (r.tau, int(r.c_thr), r.recall, r.fa_per_sub_year) for r in t.itertuples()}
    # 2. tabulate manufacturer M
    tab = {cell: tabulate(name_on(cell, M), M) for cell in CELLS}
    subs = P.substations(M); w1 = {s: 1 for s in subs}
    boots = [pd.Series(rng.choice(subs, len(subs))).value_counts().to_dict() for _ in range(NBOOT)]
    rows, detvec = [], {}
    for cell, (S, D) in tab.items():
        cv = curve(S, D, w1)
        for B in BUDGETS:
            tau, c, r1, f1 = chosen[cell][B]
            pt = cv.loc[(tau, c)]
            dd = D[(D.tau == tau) & (D.c_thr == c)].set_index("event_id")["detected"]
            detvec[(cell, B)] = dd
            bs = [curve(S, D, w).loc[(tau, c)] for w in boots[:500]]
            rows.append(dict(cell=cell, scope=CELLS[cell][2], representation=CELLS[cell][3], model=CELLS[cell][4],
                             budget=B, tau=tau, c_thr=c, m1_recall=r1, m1_fa=f1, recall=pt.recall,
                             n_detected=int(dd.sum()), n_faults=len(dd), fa_per_sub_year=pt.fa, n_fa=int(pt.n_fa),
                             fa_ci_lo=np.nanpercentile([b.fa for b in bs], 2.5), fa_ci_hi=np.nanpercentile([b.fa for b in bs], 97.5)))
    main_t = pd.DataFrame(rows); main_t.to_csv(f"results/locked_m{M}_operating_points.csv", index=False)
    print(main_t[["cell", "budget", "tau", "c_thr", "m1_recall", "m1_fa", "recall", "n_detected", "n_faults",
                  "fa_per_sub_year", "fa_ci_lo", "fa_ci_hi"]].round(3).to_string(index=False), flush=True)

    # 3. HF4 primary endpoint: recall at B = 2, SRCR-C vs every baseline
    out = []
    a = detvec[("srcr_c", 2)]
    for cell in CELLS:
        if cell == "srcr_c": continue
        b = detvec[(cell, 2)].reindex(a.index)
        n10, n01 = int((a & ~b).sum()), int((~a & b).sum())
        p = binomtest(n10, n10 + n01, 0.5).pvalue if n10 + n01 else 1.0
        Sa, Da = tab["srcr_c"]; Sb, Db = tab[cell]
        ta, ca = chosen["srcr_c"][2][:2]; tb, cb = chosen[cell][2][:2]
        diff = [curve(Sa, Da, w).loc[(ta, ca)].recall - curve(Sb, Db, w).loc[(tb, cb)].recall for w in boots[:1000]]
        out.append(dict(family="HF4", a="srcr_c", b=cell, recall_a=a.mean(), recall_b=b.mean(), a_only=n10, b_only=n01,
                        diff=a.mean() - b.mean(), diff_ci_lo=np.percentile(diff, 2.5), diff_ci_hi=np.percentile(diff, 97.5),
                        p_mcnemar=p))
    # 4. HF1 / HF2 / HF3: paired per-fault log-rank Wilcoxon + FA ratio at matched recall (cluster bootstrap)
    rk = {}
    def ranks(cell):
        if cell not in rk: rk[cell] = fault_ranks(name_on(cell, M), M)[0].set_index("event_id")["rank_frac"]
        return rk[cell]
    for fam, pairs in (("HF1", HF1), ("HF2", HF2), ("HF3", HF3)):
        for x, y in pairs:
            d = np.log10(ranks(x).clip(lower=1e-5)) - np.log10(ranks(y).clip(lower=1e-5))
            p = wilcoxon(d[d != 0]).pvalue if (d != 0).sum() else 1.0
            # matched recall r* = recall of x at its M1-chosen B = 2 operating point on M (fixed rule, A5)
            Sx, Dx = tab[x]; Sy, Dy = tab[y]
            rstar = curve(Sx, Dx, w1).loc[chosen[x][2][:2]].recall
            def ratio(w):
                fx, fy = curve(Sx, Dx, w), curve(Sy, Dy, w)
                # +0.5 false alarm continuity correction on both rates (A5)
                gx = fx[fx.recall >= rstar - 1e-9]; gy = fy[fy.recall >= rstar - 1e-9]
                if not len(gx): return np.nan
                if not len(gy): return np.inf
                vx = ((gx.n_fa + .5) / gx.expo_y).min(); vy = ((gy.n_fa + .5) / gy.expo_y).min()
                return np.log(vy / vx)
            lr = ratio(w1); bs = np.array([ratio(w) for w in boots])
            bs_f = np.where(np.isnan(bs), np.nan, bs)
            out.append(dict(family=fam, a=x, b=y, n=len(d), a_better=int((d < 0).sum()), b_better=int((d > 0).sum()),
                            median_rank_a=ranks(x).median(), median_rank_b=ranks(y).median(), p_wilcoxon=p,
                            matched_recall=rstar, fa_ratio_b_over_a=np.exp(lr),
                            ratio_ci_lo=np.exp(np.nanpercentile(bs_f, 2.5)), ratio_ci_hi=np.exp(np.nanpercentile(bs_f, 97.5)),
                            boot_unreached_b=int(np.isinf(bs).sum()), boot_unreached_a=int(np.isnan(bs).sum())))
    T = pd.DataFrame(out)
    for fam in ("HF1", "HF2", "HF4"):
        col = "p_mcnemar" if fam == "HF4" else "p_wilcoxon"
        i = T.family == fam; T.loc[i, "p_holm"] = holm(T.loc[i, col])
    T.to_csv(f"results/locked_m{M}_tests.csv", index=False)
    with pd.option_context("display.width", 250):
        print(T.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
