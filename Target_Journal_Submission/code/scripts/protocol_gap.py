"""Elevation round 1 (pre-registered in RECHECK/stage4/preregistration_E.md): protocol gap E1, E2 and T1.

Re-scores EXISTING online score streams of the frozen factorial cells under
  (a) the PreDist balanced event protocol (arXiv 2511.14791, Sec. 4.3): 7-day fault windows ending at the report,
      the dataset's 7-day normal events, eventwise F0.5, C_thr chosen by max F0.5 on the same manufacturer;
  (b) the continuous protocol (src/evaluation/continuous.py) at the same (tau, C_thr);
and compares the alarm rate on hand-picked normal events with that on ALL eligible normal substation-weeks.
Usage: protocol_gap.py  -> results/protocol_gap_*.csv
"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np, pandas as pd
from scipy.stats import binomtest, beta, kendalltau
from src.data import predist as P
from src.evaluation import continuous as C, runner as R
from src.models import online as O

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")
sys.path.insert(0, HERE)
from m2_evaluate import CELLS, name_on, holm  # same cell -> score-stream map as the locked analysis

C_GRID = np.arange(1, 289)
W = pd.Timedelta(days=7)
WEEKS_PER_YEAR = 365.25 / 7


def fbeta(p, r, b=0.5):
    return 0 if p + r == 0 else (1 + b * b) * p * r / (b * b * p + r)


def event_scores(cell, m, tau):
    """Max criticality inside each fault window, each normal event, and each eligible normal week."""
    name = name_on(cell, m); NE = P.normal_events(m)
    fault, normal, weeks, cache = [], [], [], {}
    for s in P.substations(m):
        sc = R.load_scores(name, m, s); lab = C.substation_labels(m, s, sc.index)
        k = pd.Series(O.criticality_counter(sc, tau), index=sc.index)
        cache[s] = (k, lab, sc)
        for _, r in lab.targets.iterrows():
            fault.append((s, r["event_id"], k[(k.index >= r["win_start"]) & (k.index < r["report"])].max()))
        for _, r in NE[NE["sub"] == s].iterrows():
            sel = (k.index >= r["Event start"]) & (k.index < r["Event end"])
            normal.append((s, r["Event ID"], k[sel].max() if sel.any() else 0, sc[sel].notna().mean() if sel.any() else 0))
        blocked = list(zip(lab.targets["win_start"], lab.targets["report"])) + lab.exclusions
        t = lab.start
        while t + W <= lab.end:
            if not any(a < t + W and t < b for a, b in blocked):
                sel = (k.index >= t) & (k.index < t + W)
                if sc[sel].notna().mean() > 0.5 and sel.sum() > 0.5 * 7 * 144:
                    weeks.append((s, t, k[sel].max()))
            t += W
    F = pd.DataFrame(fault, columns=["sub", "event_id", "kmax"]).fillna(0)
    N = pd.DataFrame(normal, columns=["sub", "event_id", "kmax", "coverage"]).fillna(0)
    Wk = pd.DataFrame(weeks, columns=["sub", "week", "kmax"]).fillna(0)
    return F, N, Wk, cache


def event_metrics(F, N, c):
    tp = (F.kmax >= c).sum(); fp = (N.kmax >= c).sum()
    p = tp / (tp + fp) if tp + fp else 0.0; r = tp / len(F)
    return p, r, fbeta(p, r), tp, fp


def choose_c(F, N):
    best = None
    for c in C_GRID:
        p, r, f, *_ = event_metrics(F, N, c)
        key = (f, r, -c)
        if best is None or key > best[0]:
            best = (key, c)
    return int(best[1])


def cv_f05(F, N, rng, folds=5):
    """5-fold CV stratified by label (as in the PreDist paper): mean held-out F0.5 of the train-fold choice."""
    fi = rng.permutation(len(F)) % folds; ni = rng.permutation(len(N)) % folds; out = []
    for f in range(folds):
        c = choose_c(F[fi != f], N[ni != f])
        out.append(event_metrics(F[fi == f], N[ni == f], c)[2])
    return float(np.mean(out))


def main():
    ops = pd.read_csv(os.path.join(RES, "locked_m2_operating_points.csv"))
    rng = np.random.default_rng(20261123)
    rows, e2 = [], []
    for m in (1, 2):
        for cell in CELLS:
            tau = float(ops[(ops.cell == cell) & (ops.budget == 2)].tau.iloc[0])
            F, N, Wk, cache = event_scores(cell, m, tau)
            c = choose_c(F, N)
            p, r, f, tp, fp = event_metrics(F, N, c)
            # pointwise accuracy on normal events (share of steps with no active alarm)
            acc = []
            for _, rr in P.normal_events(m).iterrows():
                if rr["sub"] not in cache: continue
                k = cache[rr["sub"]][0]; sel = (k.index >= rr["Event start"]) & (k.index < rr["Event end"])
                if sel.any(): acc.append(float((k[sel] < c).mean()))
            res = [C.evaluate_substation(pd.Series(kk.values >= c, index=kk.index), lab) for kk, lab, _ in cache.values()]
            cs = C.summarise(res)
            n_tp = int(round(cs["recall"] * cs["n_faults"]))
            q_hand = fp / len(N); q_all = float((Wk.kmax >= c).mean())
            k_all = int((Wk.kmax >= c).sum())
            pi = len(F) / (len(F) + len(Wk))  # share of fault weeks among evaluable substation-weeks
            rows.append(dict(m=m, cell=cell, tau=tau, c_thr=c, ev_precision=p, ev_recall=r, ev_f05=f,
                             ev_f05_cv=cv_f05(F, N, rng), ev_tp=tp, ev_fp=fp, n_fault_events=len(F),
                             n_normal_events=len(N), normal_event_coverage=N.coverage.mean(),
                             pointwise_acc_normal=np.mean(acc),
                             cont_recall=cs["recall"], cont_n_faults=cs["n_faults"], cont_tp=n_tp,
                             cont_fa=cs["n_false_alarms"], cont_fa_per_sub_year=cs["fa_per_sub_year"],
                             cont_alarm_precision=n_tp / max(1, n_tp + cs["n_false_alarms"]),
                             fa_per_true_detection=cs["n_false_alarms"] / n_tp if n_tp else np.inf,
                             q_hand=q_hand, q_all=q_all, n_weeks=len(Wk), k_weeks=k_all,
                             alarm_weeks_per_year_all=q_all * WEEKS_PER_YEAR,
                             prevalence_fault_weeks=pi,
                             precision_at_prevalence=(r * pi) / (r * pi + q_all * (1 - pi)) if r * pi + q_all > 0 else np.nan))
            e2.append(dict(m=m, cell=cell, n_hand=len(N), k_hand=fp, q_hand=q_hand, q_all=q_all,
                           p_binom_less=binomtest(fp, len(N), q_all, alternative="less").pvalue if 0 < q_all < 1 else 1.0))
            print(rows[-1], flush=True)
    G = pd.DataFrame(rows); E2 = pd.DataFrame(e2); E2["p_holm"] = holm(E2.p_binom_less)
    G.to_csv(os.path.join(RES, "protocol_gap_e1.csv"), index=False); E2.to_csv(os.path.join(RES, "protocol_gap_e2.csv"), index=False)
    # H-E3: rank agreement between event F0.5 and continuous recall at budget 2 (locked M1-chosen points)
    h3 = []
    for m in (1, 2):
        g = G[G.m == m].set_index("cell")
        if m == 2:
            rec = ops[ops.budget == 2].set_index("cell").recall
        else:
            rec = ops[ops.budget == 2].set_index("cell").m1_recall
        t, p = kendalltau(g.ev_f05, rec.reindex(g.index))
        h3.append(dict(m=m, kendall_tau=t, p=p))
    pd.DataFrame(h3).to_csv(os.path.join(RES, "protocol_gap_e3.csv"), index=False)
    # T1: certification table (analytic, Clopper-Pearson one-sided 95%)
    t1 = []
    for n in (30, 35, 65, 100, 156, 300, 1000):
        qu = 1 - 0.05 ** (1 / n)
        t1.append(dict(n_normal_weeks_zero_fp=n, q_upper95=qu, alarm_weeks_per_year_upper95=qu * WEEKS_PER_YEAR))
    for B in (0.5, 1, 2, 4):
        t1.append(dict(budget_alarm_weeks_per_year=B, n_required=int(np.ceil(np.log(0.05) / np.log(1 - B / WEEKS_PER_YEAR)))))
    pd.DataFrame(t1).to_csv(os.path.join(RES, "protocol_gap_t1.csv"), index=False)
    print(pd.DataFrame(h3)); print(E2)


if __name__ == "__main__":
    main()
